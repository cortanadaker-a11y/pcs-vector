"""PCS finance calculator — inputs + clear Soldier-ready output."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import list_bah_installations
from services.dla_rates import get_dla_rate
from services.housing_allowances import compare_housing_packages
from services.installation_data import (
    SUPPORTED_INSTALLATIONS,
    get_family_market_rent,
    get_installation_data,
)
from services.utility_costs import get_utility_costs_for_installation

YOS_OPTIONS = list(range(0, 41))
_NONE_CURRENT = "— Skip (new post only) —"
CALC_SNAPSHOT_KEY = "bah_calc_snapshot"


def _money(n: int | None) -> str:
    if n is None:
        return "—"
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,}"


def _money_html(n: int | None) -> str:
    """Money for st.html() blocks (real $ — not markdown/LaTeX)."""
    return _money(n)


def _render_html(block: str) -> None:
    """Render HTML without Streamlit markdown/LaTeX (fixes broken $ and raw tags)."""
    st.html(block)


def _deps_label(n: int) -> str:
    if n == 0:
        return "0 dependents"
    if n == 5:
        return "5+ dependents"
    return f"{n} dependent{'s' if n != 1 else ''}"


def get_calculator_snapshot() -> dict[str, Any] | None:
    snap = st.session_state.get(CALC_SNAPSHOT_KEY)
    return dict(snap) if isinstance(snap, dict) and snap.get("pay_grade") else None


def _store_snapshot(data: dict[str, Any]) -> None:
    st.session_state[CALC_SNAPSHOT_KEY] = data


def _util_mid(areas: list[dict[str, Any]]) -> int | None:
    if not areas:
        return None
    lows, highs = [], []
    for a in areas:
        tot = a.get("total_utilities_usd_mo") or {}
        if tot.get("low") is not None and tot.get("high") is not None:
            lows.append(int(tot["low"]))
            highs.append(int(tot["high"]))
    if not lows:
        return None
    return int(round((sum(lows) / len(lows) + sum(highs) / len(highs)) / 2))


def _arrive_cash(rent_mid: int | None, dla_usd: float | None, util_mid: int | None) -> dict[str, int]:
    """Move-in estimate from typical market rent (not BAH − utilities)."""
    rent = int(rent_mid or 0)
    util = int(util_mid or 0)
    dla = int(round(float(dla_usd or 0)))
    deposit = rent
    first_month = rent + util
    gross = deposit + first_month
    return {
        "deposit": deposit,
        "first_month": first_month,
        "util": util,
        "dla": dla,
        "net": max(gross - dla, 0),
        "gross": gross,
    }


def _system_chip(system: str) -> str:
    if system == "OHA":
        return "OHA + COLA"
    if system == "BAH_PLUS_COLA":
        return "BAH + COLA"
    return "BAH"


def _pct_change(old: int, new: int) -> int | None:
    if old == 0:
        return None
    return int(round(((new - old) / old) * 100))


def _dla_html(amount: float | None) -> str:
    if amount is None:
        return "—"
    return _money_html(int(round(amount)))


def _scenario_rows(
    *,
    rent_budget: int,
    market_low: int,
    market_mid: int,
    market_high: int,
    util_mid: int | None,
) -> list[dict[str, Any]]:
    """BAH/OHA vs low/mid/high rent (+ utils) leftover scenarios."""
    util = int(util_mid or 0)
    rows = []
    for label, rent in (("Cheaper", market_low), ("Typical", market_mid), ("Higher", market_high)):
        all_in = rent + util
        left = rent_budget - all_in
        rows.append(
            {
                "label": label,
                "rent": rent,
                "utils": util,
                "all_in": all_in,
                "left": left,
            }
        )
    return rows


def render_bah_calculator() -> None:
    installations = list_bah_installations()
    if list(installations) != list(SUPPORTED_INSTALLATIONS):
        installations = list(SUPPORTED_INSTALLATIONS)
    if not installations:
        return

    grades = [g for g in RANK_PAY_GRADES if g != "Other"]

    with st.container(border=True):
        st.markdown('<p class="pcs-bah-section-label">Will dependents move with you?</p>', unsafe_allow_html=True)
        dep_mode = st.radio(
            "Will dependents move with you?",
            options=["Yes — with dependents", "No — without dependents"],
            horizontal=True,
            key="bah_calc_dep_mode",
            label_visibility="collapsed",
        )
        with_dependents = dep_mode.startswith("Yes")

        r1, r2, r3 = st.columns([1.25, 1.0, 1.1])
        with r1:
            pay_grade = st.selectbox(
                "Pay grade",
                options=grades,
                index=grades.index("E-5") if "E-5" in grades else 0,
                format_func=lambda g: f"{g} — {PAY_GRADE_TO_RANK.get(g, g)}",
                key="bah_calc_grade",
            )
        with r2:
            yos = st.selectbox(
                "Years of service",
                options=YOS_OPTIONS,
                index=4,
                key="bah_calc_yos",
                help="Needed for COLA if you are going overseas or to Hawaii / Puerto Rico.",
            )
        with r3:
            if with_dependents:
                num_deps = st.selectbox(
                    "How many dependents?",
                    options=[1, 2, 3, 4, 5],
                    index=0,
                    format_func=_deps_label,
                    key="bah_calc_num_deps",
                    help="Spouse and children moving with you.",
                )
            else:
                num_deps = 0
                st.selectbox(
                    "How many dependents?",
                    options=["None"],
                    disabled=True,
                    key="bah_calc_num_deps_disabled",
                )

        if "bah_calc_gaining" not in st.session_state:
            st.session_state.bah_calc_gaining = (
                "Fort Bragg, NC" if "Fort Bragg, NC" in installations else installations[0]
            )

        d1, d2 = st.columns(2)
        with d1:
            current_raw = st.selectbox(
                "Current post",
                options=[_NONE_CURRENT] + installations,
                key="bah_calc_current",
                help="Optional. Pick your current post to compare money at both places.",
            )
            current = None if current_raw == _NONE_CURRENT else current_raw
        with d2:
            gaining = st.selectbox(
                "New post",
                options=installations,
                key="bah_calc_gaining",
                help="Where you are going (your gaining station).",
            )

        barracks_on = False
        if not with_dependents:
            barracks_on = st.checkbox(
                "I live in the barracks with a meal card (this can lower COLA)",
                value=False,
                key="bah_calc_barracks",
            )

        result = compare_housing_packages(
            pay_grade=pay_grade,
            with_dependents=with_dependents,
            gaining_installation=gaining,
            current_installation=current,
            years_of_service=int(yos),
            num_dependents=int(num_deps),
            barracks_meal_card=barracks_on,
        )
        pkg = result["gaining"]

        if not pkg.get("found") or pkg.get("total_monthly_usd") is None:
            _store_snapshot({"pay_grade": pay_grade})
            st.warning(
                f"We do not have 2026 rates for {pay_grade} at {gaining}. "
                "Try another post, or confirm the amount with finance."
            )
            return

        system = pkg.get("housing_system") or "BAH"
        housing = int(pkg["housing_monthly_usd"] or 0)
        cola = int(pkg.get("cola_monthly_usd") or 0)
        total = int(pkg["total_monthly_usd"])
        is_oconus = system in ("OHA", "BAH_PLUS_COLA")
        util_ctx = get_utility_costs_for_installation(gaining, is_oconus=is_oconus)
        areas = util_ctx.get("areas") or []
        util_mid = _util_mid(areas)
        oha_rent = int(pkg["oha_rent_max_usd"]) if pkg.get("oha_rent_max_usd") is not None else None
        market = get_family_market_rent(gaining, num_dependents=int(num_deps))
        market_mid = int(market["mid_usd"])
        market_low = int(market["low_usd"])
        market_high = int(market["high_usd"])
        bedrooms = int(market["bedrooms"])
        # Allowance that pays rent (BAH / OHA ceiling) — not COLA
        rent_budget = int(oha_rent) if system == "OHA" and oha_rent is not None else housing

        cur = result.get("current")
        delta = result.get("monthly_delta_usd")
        annual = result.get("annual_delta_usd")
        if not (current and cur and cur.get("found") and delta is not None):
            delta = None
            annual = None

        system_chip = _system_chip(system)
        rank_label = PAY_GRADE_TO_RANK.get(pay_grade, pay_grade)
        dep_label = _deps_label(int(num_deps))

        dla = get_dla_rate(pay_grade, with_dependents=with_dependents)
        dla_amt = float(dla["dla_usd"]) if dla.get("found") else None
        arrive = _arrive_cash(market_mid, dla_amt, util_mid)
        move_in = arrive["gross"] if market_mid else 0
        dla_covers = bool(arrive["dla"] and move_in and arrive["dla"] >= move_in)
        move_gap_label = "DLA covers this" if dla_covers else _money(arrive["net"])

        _store_snapshot(
            {
                "pay_grade": pay_grade,
                "years_of_service": int(yos),
                "num_dependents": int(num_deps),
                "gaining_installation": gaining,
                "current_installation": current,
                "barracks_meal_card": barracks_on,
                "housing_monthly_usd": housing,
                "cola_monthly_usd": cola,
                "total_monthly_usd": total,
                "housing_system": system,
                "market_rent_mid_usd": market_mid,
                "market_rent_low_usd": market_low,
                "market_rent_high_usd": market_high,
                "market_bedrooms": bedrooms,
                "dla_usd": dla_amt,
                "arrive_cash_net_usd": arrive["net"],
            }
        )

        if system == "OHA":
            primary_k = "OHA rent maximum"
            primary_v = _money_html(oha_rent)
        else:
            primary_k = "BAH"
            primary_v = _money_html(housing)

        util_n = int(util_mid or 0)
        all_in_mid = market_mid + util_n
        leftover_mid = rent_budget - all_in_mid
        bed_label = f"{bedrooms}-bedroom"
        if leftover_mid >= 0:
            fit_line = (
                f"A typical {bed_label} plus utilities runs about {_money_html(all_in_mid)}/month. "
                f"That leaves about {_money_html(leftover_mid)}/month from your {safe_html(primary_k)}."
            )
            fit_tone = "fit"
        else:
            fit_line = (
                f"A typical {bed_label} plus utilities runs about {_money_html(all_in_mid)}/month. "
                f"That is about {_money_html(abs(leftover_mid))}/month more than your {safe_html(primary_k)}. "
                f"Look for rentals closer to {_money_html(market_low)}–{_money_html(market_high)}/month."
            )
            fit_tone = "tight"

        gap_html = (
            safe_html(move_gap_label)
            if move_gap_label == "DLA covers this"
            else _money_html(arrive["net"])
        )

        _render_html(
            f"""
            <div class="pcs-sticky-results">
                <div class="pcs-out-label">{safe_html(gaining)} · {safe_html(system_chip)}</div>
                <div class="pcs-out-dual">
                    <div class="pcs-out-dual-primary">
                        <div class="pcs-out-dual-k">{safe_html(primary_k)}</div>
                        <div class="pcs-out-dual-v">{primary_v}<span>/month</span></div>
                    </div>
                    <div class="pcs-out-dual-secondary">
                        <div class="pcs-out-dual-k">Typical {bed_label} rent nearby</div>
                        <div class="pcs-out-dual-v-sm">{_money_html(market_low)}–{_money_html(market_high)}</div>
                        <div class="pcs-out-dual-sub">About {_money_html(market_mid)}/month in the middle · {safe_html(dep_label)}</div>
                    </div>
                </div>
                <div class="pcs-out-fit pcs-out-fit-{fit_tone}">{fit_line}</div>
                <div class="pcs-sticky-results-meta pcs-out-profile">
                    {safe_html(pay_grade)} · {safe_html(rank_label)} · {safe_html(dep_label)} · {int(yos)} years of service
                    · total {_money_html(total)}/month
                    {f'· COLA {_money_html(cola)}/month' if cola else ''}
                </div>
                <div class="pcs-sticky-results-grid pcs-sticky-results-grid-4">
                    <div><b>Utilities (typical)</b><br>{_money_html(util_n) if util_n else '—'}</div>
                    <div><b>DLA (one-time)</b><br>{_dla_html(dla_amt)}</div>
                    <div><b>Typical move-in cost</b><br>{_money_html(move_in) if move_in else '—'}</div>
                    <div><b>Still need after DLA</b><br>{gap_html}</div>
                </div>
            </div>
            """
        )

        scenarios = _scenario_rows(
            rent_budget=rent_budget,
            market_low=market_low,
            market_mid=market_mid,
            market_high=market_high,
            util_mid=util_mid,
        )
        scen_html = ""
        for s in scenarios:
            tone = "ok" if s["left"] >= 0 else "short"
            if s["left"] >= 0:
                left_lbl = f"+{_money_html(s['left'])}"
                left_word = " left over"
            else:
                left_lbl = _money_html(s["left"])
                left_word = " short"
            scen_html += (
                f'<div class="pcs-scen pcs-scen-{tone}">'
                f'<div class="pcs-scen-k">{s["label"]} rent</div>'
                f'<div class="pcs-scen-rent">{_money_html(s["rent"])}/month</div>'
                f'<div class="pcs-scen-sub">Plus utilities {_money_html(s["utils"])} '
                f'= {_money_html(s["all_in"])}/month total</div>'
                f'<div class="pcs-scen-left">{left_lbl}<span>{left_word}</span></div>'
                f"</div>"
            )
        _render_html(
            f"""
            <div class="pcs-scen-wrap">
                <div class="pcs-scen-title">
                    What you have left from {safe_html(primary_k)} if rent is low, typical, or high
                </div>
                <div class="pcs-scen-grid">{scen_html}</div>
            </div>
            """
        )

        if system == "OHA":
            util_oha = pkg.get("oha_utility_usd")
            _render_html(
                f"""
                <div class="pcs-out-split">
                    <div class="pcs-out-split-item"><span>OHA rent maximum</span><strong>{_money_html(oha_rent)}</strong></div>
                    <div class="pcs-out-split-item"><span>OHA utilities</span><strong>{_money_html(int(util_oha) if util_oha else None)}</strong></div>
                    <div class="pcs-out-split-item"><span>COLA</span><strong>{_money_html(cola)}</strong></div>
                </div>
                """
            )
        elif system == "BAH_PLUS_COLA" and cola:
            st.caption(
                f"COLA is about {_money(cola)}/month for higher day-to-day costs. "
                "Do not count on it for rent."
            )

        if current and cur and cur.get("found") and delta is not None:
            tone = "up" if delta > 0 else ("down" if delta < 0 else "flat")
            curr_tot = int(cur["total_monthly_usd"])
            pct = _pct_change(curr_tot, total)
            pct_txt = f"{pct:+d}%" if pct is not None else ""
            bar_pct = min(max(int(round((total / curr_tot) * 100)), 4), 100) if curr_tot else 50

            cur_market = get_family_market_rent(current, num_dependents=int(num_deps))
            cur_mid = int(cur_market["mid_usd"])
            market_delta = market_mid - cur_mid
            pressure = int(delta) - market_delta

            if market_delta < -50:
                market_note = (
                    f"A typical {bed_label} also costs less at the new post "
                    f"(about {_money_html(cur_mid)}/month now → {_money_html(market_mid)}/month there, "
                    f"{_money_html(market_delta)}/month)."
                )
            elif market_delta > 50:
                market_note = (
                    f"A typical {bed_label} costs more at the new post "
                    f"(about {_money_html(cur_mid)}/month now → {_money_html(market_mid)}/month there, "
                    f"+{_money_html(market_delta)}/month)."
                )
            else:
                market_note = (
                    f"A typical {bed_label} costs about the same "
                    f"(about {_money_html(cur_mid)}/month → {_money_html(market_mid)}/month)."
                )

            if pressure < -100:
                pressure_note = (
                    f"Overall, housing may feel about {_money_html(abs(pressure))}/month tighter "
                    "after you account for both your allowance and local rents."
                )
            elif pressure > 100:
                pressure_note = (
                    f"Overall, housing may feel about {_money_html(pressure)}/month easier "
                    "after you account for both your allowance and local rents."
                )
            else:
                pressure_note = (
                    "Overall, the change in your allowance and the change in local rents "
                    "roughly cancel out."
                )

            checks = []
            if leftover_mid >= 0:
                checks.append(
                    f"With a typical rent plus utilities, you keep about "
                    f"<strong>{_money_html(leftover_mid)}/month</strong> from your {safe_html(primary_k)}."
                )
            else:
                checks.append(
                    f"A typical rent plus utilities is about "
                    f"<strong>{_money_html(abs(leftover_mid))}/month</strong> more than your "
                    f"{safe_html(primary_k)}. Look at cheaper places."
                )
            if dla_covers:
                checks.append(
                    f"DLA (about {_dla_html(dla_amt)}) can cover a typical move-in "
                    f"(about {_money_html(move_in)}). Still keep some extra cash — "
                    "some leases want first and last month plus a deposit."
                )
            elif move_in:
                checks.append(
                    f"Plan on about {_money_html(arrive['net'])} of your own money for move-in "
                    "after DLA, using a typical rent."
                )

            checks_html = "".join(f"<li>{c}</li>" for c in checks)
            _render_html(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone} pcs-out-compare">
                    <div class="pcs-out-compare-title">Comparing your current post to your new post</div>
                    <div class="pcs-out-vs">
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Current post</div>
                            <div class="pcs-out-vs-v">{_money_html(curr_tot)}<span>/month</span></div>
                            <div class="pcs-out-vs-s">{safe_html(current)}</div>
                        </div>
                        <div class="pcs-out-vs-mid">
                            <div class="pcs-out-vs-delta">{_money_html(int(delta))}/month</div>
                            <div class="pcs-out-vs-yr">{safe_html(pct_txt)} · {_money_html(int(annual or 0))}/year</div>
                        </div>
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">New post</div>
                            <div class="pcs-out-vs-v">{_money_html(total)}<span>/month</span></div>
                            <div class="pcs-out-vs-s">{safe_html(gaining)}</div>
                        </div>
                    </div>
                    <div class="pcs-out-bar-wrap">
                        <div class="pcs-out-bar-track">
                            <div class="pcs-out-bar-fill pcs-out-bar-{tone}" style="width:{bar_pct}%;"></div>
                        </div>
                        <div class="pcs-out-bar-labels">
                            <span>0%</span>
                            <span>New post is about {bar_pct}% of your current total</span>
                            <span>100%</span>
                        </div>
                    </div>
                    <div class="pcs-out-compare-action">
                        <b>Local rents:</b> {market_note} {pressure_note}
                    </div>
                    <div class="pcs-out-checks-title">What to do next</div>
                    <ul class="pcs-out-checks">{checks_html}</ul>
                </div>
                """
            )
        else:
            checks = []
            if leftover_mid >= 0:
                checks.append(
                    f"With a typical rent plus utilities, you keep about "
                    f"<strong>{_money_html(leftover_mid)}/month</strong> from your {safe_html(primary_k)}."
                )
            else:
                checks.append(
                    f"A typical rent plus utilities is about "
                    f"<strong>{_money_html(abs(leftover_mid))}/month</strong> more than your "
                    f"{safe_html(primary_k)}."
                )
            if dla_covers:
                checks.append(
                    f"DLA (about {_dla_html(dla_amt)}) can cover a typical move-in "
                    f"(about {_money_html(move_in)})."
                )
            elif move_in:
                checks.append(
                    f"Plan on about {_money_html(arrive['net'])} of your own money for move-in after DLA."
                )
            checks.append(
                "Pick your current post above if you want to see how the new post compares."
            )
            checks_html = "".join(f"<li>{c}</li>" for c in checks)
            _render_html(
                f"""
                <div class="pcs-out-arrive">
                    <div class="pcs-out-checks-title">What to do next</div>
                    <ul class="pcs-out-checks">{checks_html}</ul>
                </div>
                """
            )

        info = get_installation_data(gaining) or {}
        with st.expander(f"Neighborhoods and utility details for {gaining}", expanded=False):
            notes = (info.get("notes") or "").strip()
            if notes:
                st.markdown(notes)
            areas_list = info.get("major_areas") or []
            commute = (info.get("commute_notes") or "").strip()
            if areas_list:
                st.caption("Common areas: " + ", ".join(areas_list[:4]))
            if commute:
                st.caption("Commute notes: " + commute)
            if areas:
                st.markdown("**Utilities off post, by area**")
                st.caption((util_ctx.get("as_of") or "2026") + " · typical three-bedroom planning ranges")
                rows = []
                for a in areas[:4]:
                    tot = a.get("total_utilities_usd_mo") or {}
                    e = a.get("electric_usd_mo") or {}
                    gas = a.get("gas_or_heat_usd_mo") or {}
                    rows.append(
                        {
                            "Area": a.get("name", "—"),
                            "Electric": f"${e.get('low', 0)}–${e.get('high', 0)}",
                            "Heat / gas": f"${gas.get('low', 0)}–${gas.get('high', 0)}",
                            "Total / month": f"${tot.get('low', 0)}–${tot.get('high', 0)}",
                        }
                    )
                st.dataframe(rows, use_container_width=True, hide_index=True)
                if areas[0].get("season_note"):
                    st.caption(areas[0]["season_note"])

        st.caption(
            "BAH, OHA, COLA, and DLA come from DoD planning tables. "
            "Rent and utility numbers are estimates based on family size. "
            "Confirm everything on your LES and with finance before you sign a lease or buy."
        )

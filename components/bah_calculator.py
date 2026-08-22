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
_NONE_CURRENT = "— Skip comparison —"
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
    for label, rent in (("Low", market_low), ("Mid", market_mid), ("High", market_high)):
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
        st.markdown('<p class="pcs-bah-section-label">Dependents</p>', unsafe_allow_html=True)
        dep_mode = st.radio(
            "Dependents status",
            options=["With dependents", "Without dependents"],
            horizontal=True,
            key="bah_calc_dep_mode",
            label_visibility="collapsed",
        )
        with_dependents = dep_mode == "With dependents"

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
                help="Used for COLA overseas and in Hawaii / Puerto Rico.",
            )
        with r3:
            if with_dependents:
                num_deps = st.selectbox(
                    "Number of dependents",
                    options=[1, 2, 3, 4, 5],
                    index=0,
                    format_func=_deps_label,
                    key="bah_calc_num_deps",
                    help="Spouse and kids PCSing with you (sets COLA count).",
                )
            else:
                num_deps = 0
                st.selectbox(
                    "Number of dependents",
                    options=["None — without dependents rate"],
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
                "Coming from",
                options=[_NONE_CURRENT] + installations,
                key="bah_calc_current",
                help="Your current post — optional, for side-by-side compare.",
            )
            current = None if current_raw == _NONE_CURRENT else current_raw
        with d2:
            gaining = st.selectbox(
                "Going to",
                options=installations,
                key="bah_calc_gaining",
                help="Your gaining post — this is the money picture that matters most.",
            )

        barracks_on = False
        if not with_dependents:
            barracks_on = st.checkbox(
                "Barracks + meal card (reduces COLA)",
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
            st.warning(f"No 2026 package for {pay_grade} at {gaining}. Try another post or check finance.")
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
        move_gap_label = "Covered by DLA" if dla_covers else _money(arrive["net"])

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
            primary_k = "OHA rent ceiling"
            primary_v = _money_html(oha_rent)
        else:
            primary_k = "BAH"
            primary_v = _money_html(housing)

        util_n = int(util_mid or 0)
        # All-in at mid market: does allowance cover rent + utilities?
        all_in_mid = market_mid + util_n
        leftover_mid = rent_budget - all_in_mid
        if leftover_mid >= 0:
            fit_line = (
                f"At mid-market {bedrooms}BR + utils (~{_money_html(all_in_mid)}/mo), "
                f"you keep ~{_money_html(leftover_mid)}/mo from your {safe_html(primary_k)}."
            )
            fit_tone = "fit"
        else:
            fit_line = (
                f"At mid-market {bedrooms}BR + utils (~{_money_html(all_in_mid)}/mo), "
                f"you’re ~{_money_html(abs(leftover_mid))}/mo short of your {safe_html(primary_k)} — "
                f"favor the low end of {_money_html(market_low)}–{_money_html(market_high)}."
            )
            fit_tone = "tight"

        gap_html = safe_html(move_gap_label) if move_gap_label == "Covered by DLA" else _money_html(
            arrive["net"]
        )

        _render_html(
            f"""
            <div class="pcs-sticky-results">
                <div class="pcs-out-label">{safe_html(gaining)} · {safe_html(system_chip)}</div>
                <div class="pcs-out-dual">
                    <div class="pcs-out-dual-primary">
                        <div class="pcs-out-dual-k">{safe_html(primary_k)}</div>
                        <div class="pcs-out-dual-v">{primary_v}<span>/mo</span></div>
                    </div>
                    <div class="pcs-out-dual-secondary">
                        <div class="pcs-out-dual-k">Typical {bedrooms}BR market</div>
                        <div class="pcs-out-dual-v-sm">{_money_html(market_low)}–{_money_html(market_high)}</div>
                        <div class="pcs-out-dual-sub">mid ~{_money_html(market_mid)} · {safe_html(dep_label)}</div>
                    </div>
                </div>
                <div class="pcs-out-fit pcs-out-fit-{fit_tone}">{fit_line}</div>
                <div class="pcs-sticky-results-meta pcs-out-profile">
                    {safe_html(pay_grade)} · {safe_html(rank_label)} · {safe_html(dep_label)} · {int(yos)} YOS
                    · full package {_money_html(total)}/mo
                    {f'· COLA {_money_html(cola)}/mo' if cola else ''}
                </div>
                <div class="pcs-sticky-results-grid pcs-sticky-results-grid-4">
                    <div><b>Utils (mid)</b><br>{_money_html(util_n) if util_n else '—'}</div>
                    <div><b>DLA</b><br>{_dla_html(dla_amt)}</div>
                    <div><b>Move-in</b><br>{_money_html(move_in) if move_in else '—'}</div>
                    <div><b>Cash gap</b><br>{gap_html}</div>
                </div>
            </div>
            """
        )

        # What-if: low / mid / high rent against the same allowance
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
            left_lbl = (
                f"+{_money_html(s['left'])}" if s["left"] >= 0 else _money_html(s["left"])
            )
            scen_html += (
                f'<div class="pcs-scen pcs-scen-{tone}">'
                f'<div class="pcs-scen-k">{s["label"]} rent</div>'
                f'<div class="pcs-scen-rent">{_money_html(s["rent"])}/mo</div>'
                f'<div class="pcs-scen-sub">+ utils {_money_html(s["utils"])} = {_money_html(s["all_in"])}</div>'
                f'<div class="pcs-scen-left">{left_lbl}<span> left</span></div>'
                f"</div>"
            )
        _render_html(
            f"""
            <div class="pcs-scen-wrap">
                <div class="pcs-scen-title">If you rent low / mid / high — leftover from {safe_html(primary_k)}</div>
                <div class="pcs-scen-grid">{scen_html}</div>
            </div>
            """
        )

        if system == "OHA":
            util_oha = pkg.get("oha_utility_usd")
            _render_html(
                f"""
                <div class="pcs-out-split">
                    <div class="pcs-out-split-item"><span>Rent ceiling</span><strong>{_money_html(oha_rent)}</strong></div>
                    <div class="pcs-out-split-item"><span>OHA utilities</span><strong>{_money_html(int(util_oha) if util_oha else None)}</strong></div>
                    <div class="pcs-out-split-item"><span>COLA</span><strong>{_money_html(cola)}</strong></div>
                </div>
                """
            )
        elif system == "BAH_PLUS_COLA" and cola:
            st.caption(f"COLA {_money(cola)}/mo is for day-to-day costs — don’t spend it on rent.")

        # Post package compare + same-size market at both posts
        if current and cur and cur.get("found") and delta is not None:
            tone = "up" if delta > 0 else ("down" if delta < 0 else "flat")
            curr_tot = int(cur["total_monthly_usd"])
            pct = _pct_change(curr_tot, total)
            pct_txt = f"{pct:+d}%" if pct is not None else ""
            bar_pct = min(max(int(round((total / curr_tot) * 100)), 4), 100) if curr_tot else 50

            cur_market = get_family_market_rent(current, num_dependents=int(num_deps))
            cur_mid = int(cur_market["mid_usd"])
            market_delta = market_mid - cur_mid
            # Housing pressure: allowance change vs rent-market change
            pressure = int(delta) - market_delta

            if market_delta < -50:
                market_note = (
                    f"Typical {bedrooms}BR mid is also cheaper at the new post "
                    f"({_money_html(cur_mid)} → {_money_html(market_mid)}, {_money_html(market_delta)}/mo)."
                )
            elif market_delta > 50:
                market_note = (
                    f"Typical {bedrooms}BR mid is more expensive at the new post "
                    f"({_money_html(cur_mid)} → {_money_html(market_mid)}, +{_money_html(market_delta)}/mo)."
                )
            else:
                market_note = (
                    f"Typical {bedrooms}BR mid is similar "
                    f"({_money_html(cur_mid)} → {_money_html(market_mid)})."
                )

            if pressure < -100:
                pressure_note = (
                    f"Net housing pressure rises ~{_money_html(abs(pressure))}/mo "
                    "(allowance drop vs local rent change)."
                )
            elif pressure > 100:
                pressure_note = (
                    f"Net housing pressure eases ~{_money_html(pressure)}/mo "
                    "(allowance vs local rent change)."
                )
            else:
                pressure_note = "Net housing pressure (allowance vs local rent) is roughly flat."

            checks = []
            if leftover_mid >= 0:
                checks.append(
                    f"At mid rent + utils you keep ~<strong>{_money_html(leftover_mid)}/mo</strong> "
                    f"from {safe_html(primary_k)}"
                )
            else:
                checks.append(
                    f"Mid rent + utils runs ~<strong>{_money_html(abs(leftover_mid))}/mo</strong> "
                    f"over {safe_html(primary_k)} — shop low"
                )
            if dla_covers:
                checks.append(
                    f"DLA (~{_dla_html(dla_amt)}) can cover typical move-in (~{_money_html(move_in)}) — keep a buffer"
                )
            elif move_in:
                checks.append(
                    f"Plan ~{_money_html(arrive['net'])} beyond DLA for move-in at mid market"
                )

            checks_html = "".join(f"<li>{c}</li>" for c in checks)
            _render_html(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone} pcs-out-compare">
                    <div class="pcs-out-compare-title">Allowance: {safe_html(current)} → {safe_html(gaining)}</div>
                    <div class="pcs-out-vs">
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Coming from</div>
                            <div class="pcs-out-vs-v">{_money_html(curr_tot)}<span>/mo</span></div>
                            <div class="pcs-out-vs-s">{safe_html(current)}</div>
                        </div>
                        <div class="pcs-out-vs-mid">
                            <div class="pcs-out-vs-delta">{_money_html(int(delta))}/mo</div>
                            <div class="pcs-out-vs-yr">{safe_html(pct_txt)} · {_money_html(int(annual or 0))}/yr</div>
                        </div>
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Going to</div>
                            <div class="pcs-out-vs-v">{_money_html(total)}<span>/mo</span></div>
                            <div class="pcs-out-vs-s">{safe_html(gaining)}</div>
                        </div>
                    </div>
                    <div class="pcs-out-bar-wrap">
                        <div class="pcs-out-bar-track">
                            <div class="pcs-out-bar-fill pcs-out-bar-{tone}" style="width:{bar_pct}%;"></div>
                        </div>
                        <div class="pcs-out-bar-labels">
                            <span>0</span>
                            <span>New ≈ {bar_pct}% of old package</span>
                            <span>100%</span>
                        </div>
                    </div>
                    <div class="pcs-out-compare-action">
                        <b>Local rents ({bedrooms}BR):</b> {market_note} {pressure_note}
                    </div>
                    <div class="pcs-out-checks-title">Your next moves</div>
                    <ul class="pcs-out-checks">{checks_html}</ul>
                </div>
                """
            )
        else:
            checks = []
            if leftover_mid >= 0:
                checks.append(
                    f"Mid rent + utils: keep ~<strong>{_money_html(leftover_mid)}/mo</strong> "
                    f"from {safe_html(primary_k)}"
                )
            else:
                checks.append(
                    f"Mid rent + utils: ~<strong>{_money_html(abs(leftover_mid))}/mo</strong> "
                    f"over {safe_html(primary_k)}"
                )
            if dla_covers:
                checks.append(
                    f"DLA (~{_dla_html(dla_amt)}) can cover typical move-in (~{_money_html(move_in)})"
                )
            elif move_in:
                checks.append(f"Move-in cash beyond DLA: ~{_money_html(arrive['net'])}")
            checks.append("Set Coming from to compare allowances and local rents to your current post")
            checks_html = "".join(f"<li>{c}</li>" for c in checks)
            _render_html(
                f"""
                <div class="pcs-out-arrive">
                    <div class="pcs-out-checks-title">Your next moves</div>
                    <ul class="pcs-out-checks">{checks_html}</ul>
                </div>
                """
            )

        info = get_installation_data(gaining) or {}
        with st.expander(f"Neighborhoods & utility detail — {gaining}", expanded=False):
            notes = (info.get("notes") or "").strip()
            if notes:
                st.markdown(notes)
            areas_list = info.get("major_areas") or []
            commute = (info.get("commute_notes") or "").strip()
            if areas_list:
                st.caption("Common areas: " + ", ".join(areas_list[:4]))
            if commute:
                st.caption("Commute: " + commute)
            if areas:
                st.markdown("**Off-post utilities by area**")
                st.caption((util_ctx.get("as_of") or "2026") + " · typical 3BR planning")
                rows = []
                for a in areas[:4]:
                    tot = a.get("total_utilities_usd_mo") or {}
                    e = a.get("electric_usd_mo") or {}
                    gas = a.get("gas_or_heat_usd_mo") or {}
                    rows.append(
                        {
                            "Area": a.get("name", "—"),
                            "Electric": f"${e.get('low', 0)}–${e.get('high', 0)}",
                            "Heat": f"${gas.get('low', 0)}–${gas.get('high', 0)}",
                            "Total/mo": f"${tot.get('low', 0)}–${tot.get('high', 0)}",
                        }
                    )
                st.dataframe(rows, use_container_width=True, hide_index=True)
                if areas[0].get("season_note"):
                    st.caption(areas[0]["season_note"])

        st.caption(
            "BAH/OHA/COLA/DLA from DoD planning tables. Market rents & utilities are planning ranges "
            "sized to your dependents — verify LES, finance / DTMO, and local listings before you sign."
        )

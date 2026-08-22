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


def _dla_display(amount: float | None) -> str:
    if amount is None:
        return "—"
    return _money(int(round(amount)))


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
        # Compare allowance that pays rent (BAH / OHA ceiling) to market mid
        rent_budget = int(oha_rent) if system == "OHA" and oha_rent is not None else housing
        vs_market = rent_budget - market_mid

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

        # Primary: official-ish allowance vs local market for this family size
        if system == "OHA":
            primary_k = "OHA rent ceiling"
            primary_v = _money(oha_rent)
        else:
            primary_k = "BAH"
            primary_v = _money(housing)

        if vs_market >= 0:
            fit_line = (
                f"Typical {bedrooms}BR mid (~{_money(market_mid)}) fits under your "
                f"{'ceiling' if system == 'OHA' else 'BAH'} with ~{_money(vs_market)}/mo left "
                f"(before utilities)."
            )
            fit_tone = "fit"
        else:
            fit_line = (
                f"Typical {bedrooms}BR mid (~{_money(market_mid)}) runs "
                f"~{_money(abs(vs_market))}/mo over your "
                f"{'OHA ceiling' if system == 'OHA' else 'BAH'} — shop the low end "
                f"({_money(market_low)}–{_money(market_high)}) or stretch the budget."
            )
            fit_tone = "tight"

        st.markdown(
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
                        <div class="pcs-out-dual-v-sm">{_money(market_low)}–{_money(market_high)}</div>
                        <div class="pcs-out-dual-sub">mid ~{_money(market_mid)}/mo · {safe_html(dep_label)}</div>
                    </div>
                </div>
                <div class="pcs-out-fit pcs-out-fit-{fit_tone}">{fit_line}</div>
                <div class="pcs-sticky-results-meta pcs-out-profile">
                    {safe_html(pay_grade)} · {safe_html(rank_label)} · {safe_html(dep_label)} · {int(yos)} YOS
                    · package {_money(total)}/mo ({_money(total * 12)}/yr)
                </div>
                <div class="pcs-sticky-results-grid">
                    <div><b>DLA</b><br>{safe_html(_dla_display(dla_amt))}</div>
                    <div><b>Typical move-in</b><br>{_money(move_in) if move_in else '—'}</div>
                    <div><b>Cash gap</b><br>{safe_html(move_gap_label)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if system == "OHA":
            util = pkg.get("oha_utility_usd")
            st.markdown(
                f"""
                <div class="pcs-out-split">
                    <div class="pcs-out-split-item"><span>Rent ceiling</span><strong>{_money(oha_rent)}</strong></div>
                    <div class="pcs-out-split-item"><span>OHA utilities</span><strong>{_money(int(util) if util else None)}</strong></div>
                    <div class="pcs-out-split-item"><span>COLA</span><strong>{_money(cola)}</strong></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif system == "BAH_PLUS_COLA":
            st.markdown(
                f"""
                <div class="pcs-out-split">
                    <div class="pcs-out-split-item"><span>BAH</span><strong>{_money(housing)}</strong></div>
                    <div class="pcs-out-split-item"><span>COLA</span><strong>{_money(cola)}</strong></div>
                    <div class="pcs-out-split-item"><span>Combined</span><strong>{_money(total)}</strong></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 2) Compare with % + bar; 3) checklist instead of prose walls
        if current and cur and cur.get("found") and delta is not None:
            tone = "up" if delta > 0 else ("down" if delta < 0 else "flat")
            curr_tot = int(cur["total_monthly_usd"])
            pct = _pct_change(curr_tot, total)
            pct_txt = f"{pct:+d}%" if pct is not None else ""
            # Bar fill: new as % of old (capped 100 for display when higher)
            bar_pct = min(max(int(round((total / curr_tot) * 100)), 4), 100) if curr_tot else 50

            checks = []
            checks.append(
                f"Rent search: typical {bedrooms}BR near {safe_html(gaining)} is "
                f"<strong>{_money(market_low)}–{_money(market_high)}/mo</strong> "
                f"(your {primary_k} is {primary_v}/mo)"
            )
            if abs(int(delta)) >= 100:
                direction = "less" if delta < 0 else "more"
                checks.append(
                    f"vs {safe_html(current)}: {_money(abs(int(delta)))}/mo {direction} "
                    f"(~{_money(abs(int(annual or 0)))}/yr)"
                )
            if dla_covers:
                checks.append(
                    f"Move-in: DLA (~{_dla_display(dla_amt)}) can cover typical deposit + first month "
                    f"at mid market (~{_money(move_in)}) — buffer for first+last / travel"
                )
            elif arrive["dla"] and move_in:
                checks.append(
                    f"Move-in: plan ~{_money(arrive['net'])} beyond DLA "
                    f"(~{_money(move_in)} at mid-market rent + utils)"
                )
            elif move_in:
                checks.append(f"Move-in: plan ~{_money(move_in)} at mid-market rent + utils")

            checks_html = "".join(f"<li>{c}</li>" for c in checks)
            st.markdown(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone} pcs-out-compare">
                    <div class="pcs-out-compare-title">vs {safe_html(current)}</div>
                    <div class="pcs-out-vs">
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Coming from</div>
                            <div class="pcs-out-vs-v">{_money(curr_tot)}<span>/mo</span></div>
                            <div class="pcs-out-vs-s">{safe_html(current)}</div>
                        </div>
                        <div class="pcs-out-vs-mid">
                            <div class="pcs-out-vs-delta">{_money(int(delta))}/mo</div>
                            <div class="pcs-out-vs-yr">{safe_html(pct_txt)} · {_money(int(annual or 0))}/yr</div>
                        </div>
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Going to</div>
                            <div class="pcs-out-vs-v">{_money(total)}<span>/mo</span></div>
                            <div class="pcs-out-vs-s">{safe_html(gaining)}</div>
                        </div>
                    </div>
                    <div class="pcs-out-bar-wrap" title="New package relative to old">
                        <div class="pcs-out-bar-track">
                            <div class="pcs-out-bar-fill pcs-out-bar-{tone}" style="width:{bar_pct}%;"></div>
                        </div>
                        <div class="pcs-out-bar-labels">
                            <span>0</span>
                            <span>New ≈ {bar_pct}% of old package</span>
                            <span>100%</span>
                        </div>
                    </div>
                    <div class="pcs-out-checks-title">Your next moves</div>
                    <ul class="pcs-out-checks">{checks_html}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            checks = [
                f"Rent search: typical {bedrooms}BR is "
                f"<strong>{_money(market_low)}–{_money(market_high)}/mo</strong> "
                f"vs your {primary_k} {primary_v}/mo"
            ]
            if dla_covers:
                checks.append(
                    f"Move-in: DLA (~{_dla_display(dla_amt)}) can cover typical ~{_money(move_in)} — keep a buffer"
                )
            elif move_in:
                gap = arrive["net"] if arrive["dla"] else move_in
                checks.append(f"Move-in: plan ~{_money(gap)} beyond any DLA at mid-market rent")
            checks_html = "".join(f"<li>{c}</li>" for c in checks)
            st.markdown(
                f"""
                <div class="pcs-out-arrive">
                    <div class="pcs-out-checks-title">Your next moves</div>
                    <ul class="pcs-out-checks">{checks_html}</ul>
                    <span class="pcs-out-arrive-note">Set Coming from to compare against your current post. Market rents are planning ranges.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Local intel / utilities only (no copy-paste blurb)
        info = get_installation_data(gaining) or {}
        with st.expander(f"Local intel & utilities — {gaining}", expanded=False):
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
                st.markdown("**Off-post utilities** (typical 3BR)")
                st.caption(
                    (util_ctx.get("as_of") or "2026")
                    + (f" · mid ~{_money(util_mid)}/mo" if util_mid else "")
                )
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

        st.caption("Planning figures · verify LES / finance / DTMO before you sign.")

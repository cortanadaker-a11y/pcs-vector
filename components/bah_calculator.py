"""Compact sticky PCS finance calculator."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import list_bah_installations
from services.dla_rates import format_dla_usd, get_dla_rate
from services.housing_allowances import compare_housing_packages, get_housing_package
from services.installation_data import SUPPORTED_INSTALLATIONS, get_installation_data
from services.utility_costs import get_utility_costs_for_installation

YOS_OPTIONS = list(range(0, 41))
_NONE_CURRENT = "— Skip —"
_DEP_OPTIONS = [0, 1, 2, 3, 4, 5]
_QUICK_POSTS = [
    "Fort Bragg, NC",
    "Fort Hood, TX",
    "Fort Campbell, KY",
    "Joint Base Lewis-McChord, WA",
    "Camp Humphreys, South Korea",
    "USAG Rheinland-Pfalz, Germany",
]
CALC_SNAPSHOT_KEY = "bah_calc_snapshot"


def _money(n: int | None) -> str:
    if n is None:
        return "—"
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,}"


def _deps_label(n: int) -> str:
    if n == 0:
        return "0 deps"
    if n == 5:
        return "5+ deps"
    return f"{n} dep{'s' if n != 1 else ''}"


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


def _rent_target(
    *,
    system: str,
    housing: int,
    util_mid: int | None,
    oha_rent_max: int | None,
) -> int | None:
    if system == "OHA":
        return int(oha_rent_max) if oha_rent_max is not None else (int(housing) if housing else None)
    if util_mid and util_mid > 0:
        return max(int(housing) - int(util_mid), 0)
    return int(housing) if housing else None


def _arrive_cash(rent_tgt: int | None, dla_usd: float | None, util_mid: int | None) -> dict[str, int]:
    rent = int(rent_tgt or 0)
    util = int(util_mid or 0)
    dla = int(round(float(dla_usd or 0)))
    deposit = rent
    first_month = rent + util
    gross = deposit + first_month
    return {
        "deposit": deposit,
        "first_month": first_month,
        "dla": dla,
        "net": max(gross - dla, 0),
    }


def _spouse_blurb(
    *,
    gaining: str,
    total: int,
    system_chip: str,
    rent_tgt: int | None,
    delta: int | None,
    current: str | None,
    dla_usd: float | None,
) -> str:
    parts = [
        f"Hey — PCS money for {gaining}: ~{_money(total)}/mo ({system_chip}).",
    ]
    if rent_tgt is not None:
        parts.append(f"Rent target ~{_money(rent_tgt)}/mo.")
    if current and delta is not None:
        parts.append(f"Δ {_money(int(delta))}/mo vs {current}.")
    if dla_usd:
        parts.append(f"DLA ~{format_dla_usd(dla_usd)} one-time.")
    parts.append("PCS Vector — Built For Soldiers; By Soldiers.")
    return " ".join(parts)


def render_bah_calculator() -> None:
    installations = list_bah_installations()
    if list(installations) != list(SUPPORTED_INSTALLATIONS):
        installations = list(SUPPORTED_INSTALLATIONS)
    if not installations:
        return

    grades = [g for g in RANK_PAY_GRADES if g != "Other"]
    quick = [p for p in _QUICK_POSTS if p in installations]

    with st.container(border=True):
        if quick:
            row1, row2 = quick[:3], quick[3:6]
            for row_i, row in enumerate((row1, row2)):
                if not row:
                    continue
                cols = st.columns(3)
                for i, post in enumerate(row):
                    with cols[i]:
                        label = post.split(",")[0].replace("Joint Base ", "JB ")
                        if st.button(label, key=f"quick_{row_i}_{i}", use_container_width=True):
                            st.session_state.bah_calc_gaining = post
                            st.rerun()

        c1, c2, c3 = st.columns([1.3, 0.7, 0.9])
        with c1:
            pay_grade = st.selectbox(
                "Grade",
                options=grades,
                index=grades.index("E-5") if "E-5" in grades else 0,
                format_func=lambda g: f"{g} — {PAY_GRADE_TO_RANK.get(g, g)}",
                key="bah_calc_grade",
            )
        with c2:
            yos = st.selectbox("YOS", options=YOS_OPTIONS, index=4, key="bah_calc_yos")
        with c3:
            num_deps = st.selectbox(
                "Deps",
                options=_DEP_OPTIONS,
                index=1,
                format_func=_deps_label,
                key="bah_calc_num_deps",
            )

        if "bah_calc_gaining" not in st.session_state:
            st.session_state.bah_calc_gaining = (
                "Fort Bragg, NC" if "Fort Bragg, NC" in installations else installations[0]
            )

        d1, d2, d3 = st.columns([1.2, 1.2, 0.45])
        with d1:
            gaining = st.selectbox("Going to", options=installations, key="bah_calc_gaining")
        with d2:
            current_raw = st.selectbox(
                "Coming from",
                options=[_NONE_CURRENT] + installations,
                key="bah_calc_current",
            )
            current = None if current_raw == _NONE_CURRENT else current_raw
        with d3:
            st.write("")
            st.write("")
            if st.button("⇄", use_container_width=True, key="bah_swap", help="Swap posts"):
                g = st.session_state.get("bah_calc_gaining")
                c = st.session_state.get("bah_calc_current")
                if c and c != _NONE_CURRENT:
                    st.session_state.bah_calc_gaining = c
                    st.session_state.bah_calc_current = g
                else:
                    st.session_state.bah_calc_current = g
                st.rerun()

        with_dependents = int(num_deps) > 0
        barracks_on = False
        if not with_dependents:
            barracks_on = st.checkbox("Barracks + meal card", value=False, key="bah_calc_barracks")

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
            st.warning(f"No 2026 package for {pay_grade} at {gaining}.")
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
        rent_tgt = _rent_target(
            system=system, housing=housing, util_mid=util_mid, oha_rent_max=oha_rent
        )

        cur = result.get("current")
        delta = result.get("monthly_delta_usd")
        annual = result.get("annual_delta_usd")
        if not (current and cur and cur.get("found") and delta is not None):
            delta = None
            annual = None

        if system == "OHA":
            system_chip = "OHA+COLA"
        elif system == "BAH_PLUS_COLA":
            system_chip = "BAH+COLA"
        else:
            system_chip = "BAH"

        dla = get_dla_rate(pay_grade, with_dependents=with_dependents)
        dla_amt = float(dla["dla_usd"]) if dla.get("found") else None
        arrive = _arrive_cash(rent_tgt, dla_amt, util_mid)

        share = f"{pay_grade} @ {gaining}: {_money(total)}/mo ({system_chip})"
        if current and delta is not None:
            share += f" · Δ {_money(int(delta))}/mo vs {current}"
        if rent_tgt is not None:
            share += f" · rent ~{_money(rent_tgt)}"

        spouse = _spouse_blurb(
            gaining=gaining,
            total=total,
            system_chip=system_chip,
            rent_tgt=rent_tgt,
            delta=int(delta) if delta is not None else None,
            current=current,
            dla_usd=dla_amt,
        )

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
                "rent_target_usd": rent_tgt,
                "dla_usd": dla_amt,
                "arrive_cash_net_usd": arrive["net"],
                "share_line": share,
                "spouse_blurb": spouse,
            }
        )

        # Sticky results strip
        delta_bit = f" · Δ {_money(int(delta))}/mo" if delta is not None else ""
        st.markdown(
            f"""
            <div class="pcs-sticky-results">
                <div class="pcs-sticky-results-main">
                    <span class="pcs-sticky-results-amt">{_money(total)}</span>
                    <span class="pcs-sticky-results-unit">/mo</span>
                    <span class="pcs-sticky-results-meta">{safe_html(system_chip)} · {safe_html(gaining)}{safe_html(delta_bit)}</span>
                </div>
                <div class="pcs-sticky-results-grid">
                    <div><b>Rent</b> {_money(rent_tgt)}</div>
                    <div><b>DLA</b> {safe_html(format_dla_usd(dla_amt) if dla_amt is not None else '—')}</div>
                    <div><b>Arrive</b> {_money(arrive['net'])}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Compact breakdown
        if system == "OHA":
            util = pkg.get("oha_utility_usd")
            b1, b2, b3 = st.columns(3)
            b1.metric("Rent ceiling", _money(oha_rent))
            b2.metric("OHA utils", _money(int(util) if util else None))
            b3.metric("COLA", _money(cola))
        elif system == "BAH_PLUS_COLA":
            b1, b2, b3 = st.columns(3)
            b1.metric("BAH", _money(housing))
            b2.metric("COLA", _money(cola))
            b3.metric("Total", _money(total))
        else:
            alt_with = get_housing_package(
                gaining, pay_grade, with_dependents=True, years_of_service=int(yos), num_dependents=1
            )
            alt_without = get_housing_package(
                gaining, pay_grade, with_dependents=False, years_of_service=int(yos), num_dependents=0
            )
            aw = alt_with.get("housing_monthly_usd")
            awo = alt_without.get("housing_monthly_usd")
            if aw is not None and awo is not None:
                b1, b2, b3 = st.columns(3)
                b1.metric("With deps", _money(int(aw)))
                b2.metric("Without", _money(int(awo)))
                b3.metric("Diff", _money(int(aw) - int(awo)))

        if current and cur and cur.get("found") and delta is not None:
            tone = "up" if delta > 0 else ("down" if delta < 0 else "flat")
            st.markdown(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone} pcs-delta-tight">
                    <strong>{_money(int(delta))}/mo</strong> · {_money(int(annual or 0))}/yr
                    · {safe_html(current)} → {safe_html(gaining)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        info = get_installation_data(gaining) or {}
        with st.expander("More: intel · utilities · share", expanded=False):
            notes = (info.get("notes") or "").strip()
            if notes:
                st.markdown(f"**{gaining}** — {notes}")
            areas_list = info.get("major_areas") or []
            if areas_list:
                st.caption("Areas: " + ", ".join(areas_list[:4]))
            if areas:
                st.caption(
                    (util_ctx.get("as_of") or "2026")
                    + (f" · mid utils ~{_money(util_mid)}" if util_mid else "")
                )
                rows = []
                for a in areas[:3]:
                    tot = a.get("total_utilities_usd_mo") or {}
                    rows.append(
                        {
                            "Area": a.get("name", "—"),
                            "Total/mo": f"${tot.get('low', 0)}–${tot.get('high', 0)}",
                        }
                    )
                st.dataframe(rows, use_container_width=True, hide_index=True)
            st.caption("Copy to text")
            st.code(spouse, language=None)
            st.code(share, language=None)

        st.caption("Planning figures · verify LES / finance / DTMO")

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
_NONE_CURRENT = "— Skip —"
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


def _package_side_html(pkg: dict[str, Any], *, side_label: str) -> str:
    """Spell out BAH / OHA / COLA lines + total for one post in the compare panel."""
    install = safe_html(str(pkg.get("installation") or "—"))
    system = pkg.get("housing_system") or "BAH"
    housing = pkg.get("housing_monthly_usd")
    cola = int(pkg.get("cola_monthly_usd") or 0)
    total = pkg.get("total_monthly_usd")
    cola_idx = pkg.get("cola_index")

    rows: list[str] = []
    if system == "OHA":
        rent = pkg.get("oha_rent_max_usd")
        util = pkg.get("oha_utility_usd")
        rows.append('<div class="pcs-pkg-sys">Overseas Housing Allowance (OHA) + COLA</div>')
        if rent is not None:
            rows.append(
                f'<div class="pcs-pkg-row"><span>OHA rent max</span>'
                f"<strong>{_money_html(int(rent))}/mo</strong></div>"
            )
        if util is not None:
            rows.append(
                f'<div class="pcs-pkg-row"><span>OHA utilities</span>'
                f"<strong>{_money_html(int(util))}/mo</strong></div>"
            )
        if housing is not None:
            rows.append(
                f'<div class="pcs-pkg-row"><span>OHA housing total</span>'
                f"<strong>{_money_html(int(housing))}/mo</strong></div>"
            )
        if cola_idx is None and cola == 0:
            rows.append(
                '<div class="pcs-pkg-row"><span>COLA (Cost of Living)</span>'
                "<strong>$0/mo</strong></div>"
                '<div class="pcs-pkg-note">No COLA at this locality right now</div>'
            )
        else:
            idx_bit = f" (index {cola_idx})" if cola_idx is not None else ""
            rows.append(
                f'<div class="pcs-pkg-row"><span>COLA (Cost of Living){safe_html(idx_bit)}</span>'
                f"<strong>{_money_html(cola)}/mo</strong></div>"
            )
    elif system == "BAH_PLUS_COLA":
        rows.append(
            '<div class="pcs-pkg-sys">Basic Allowance for Housing (BAH) + COLA</div>'
        )
        rows.append(
            f'<div class="pcs-pkg-row"><span>BAH</span>'
            f"<strong>{_money_html(int(housing) if housing is not None else None)}/mo</strong></div>"
        )
        idx_bit = f" (index {cola_idx})" if cola_idx is not None else ""
        rows.append(
            f'<div class="pcs-pkg-row"><span>COLA (Cost of Living){safe_html(idx_bit)}</span>'
            f"<strong>{_money_html(cola)}/mo</strong></div>"
        )
    else:
        rows.append('<div class="pcs-pkg-sys">Basic Allowance for Housing (BAH)</div>')
        rows.append(
            f'<div class="pcs-pkg-row"><span>BAH</span>'
            f"<strong>{_money_html(int(housing) if housing is not None else None)}/mo</strong></div>"
        )
        if cola:
            rows.append(
                f'<div class="pcs-pkg-row"><span>COLA (Cost of Living)</span>'
                f"<strong>{_money_html(cola)}/mo</strong></div>"
            )

    rows.append(
        f'<div class="pcs-pkg-total"><span>Total</span>'
        f"<strong>{_money_html(int(total) if total is not None else None)}/mo</strong></div>"
    )

    return (
        f'<div class="pcs-pkg-side">'
        f'<div class="pcs-pkg-side-k">{safe_html(side_label)}</div>'
        f'<div class="pcs-pkg-side-loc">{install}</div>'
        f'{"".join(rows)}'
        f"</div>"
    )


def render_bah_calculator() -> None:
    installations = list_bah_installations()
    if list(installations) != list(SUPPORTED_INSTALLATIONS):
        installations = list(SUPPORTED_INSTALLATIONS)
    if not installations:
        return

    grades = [g for g in RANK_PAY_GRADES if g != "Other"]

    with st.container(border=True):
        st.markdown(
            """
            <div class="pcs-calc-intro">
                <div class="pcs-calc-intro-kicker">PCS finance calculator</div>
                <div class="pcs-calc-intro-title">What will housing look like at your new post?</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="pcs-bah-section-label">You &amp; your family</p>', unsafe_allow_html=True)
        dep_mode = st.radio(
            "Dependents",
            options=["With dependents", "Without dependents"],
            horizontal=True,
            key="bah_calc_dep_mode",
            label_visibility="collapsed",
        )
        with_dependents = dep_mode.startswith("With")

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
                    "Dependents",
                    options=[1, 2, 3, 4, 5],
                    index=0,
                    format_func=_deps_label,
                    key="bah_calc_num_deps",
                )
            else:
                num_deps = 0
                st.selectbox(
                    "Dependents",
                    options=["None"],
                    disabled=True,
                    key="bah_calc_num_deps_disabled",
                )

        if "bah_calc_gaining" not in st.session_state:
            st.session_state.bah_calc_gaining = (
                "Fort Bragg, NC" if "Fort Bragg, NC" in installations else installations[0]
            )

        st.markdown('<p class="pcs-bah-section-label">Where you are going</p>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            current_raw = st.selectbox(
                "Current post (optional)",
                options=[_NONE_CURRENT] + installations,
                key="bah_calc_current",
                help="Optional — compare pay and rent pressure to your new post.",
            )
            current = None if current_raw == _NONE_CURRENT else current_raw
        with d2:
            gaining = st.selectbox(
                "New post",
                options=installations,
                key="bah_calc_gaining",
            )

        barracks_on = False
        if not with_dependents:
            barracks_on = st.checkbox(
                "Barracks + meal card (can lower COLA)",
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
            st.warning(f"No 2026 rates for {pay_grade} at {gaining}. Try another post or ask finance.")
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
            primary_k = "OHA rent max"
            primary_v = _money_html(oha_rent)
        else:
            primary_k = "BAH"
            primary_v = _money_html(housing)

        util_n = int(util_mid or 0)
        all_in_mid = market_mid + util_n
        leftover_mid = rent_budget - all_in_mid
        bed_label = f"{bedrooms}BR"
        if leftover_mid >= 0:
            fit_line = (
                f"Typical {bed_label} + utilities ≈ {_money_html(all_in_mid)}/mo — "
                f"<strong>{_money_html(leftover_mid)}/mo</strong> left in {safe_html(primary_k)}."
            )
            fit_tone = "fit"
        else:
            fit_line = (
                f"Typical {bed_label} + utilities ≈ {_money_html(all_in_mid)}/mo — "
                f"<strong>{_money_html(abs(leftover_mid))}/mo</strong> over {safe_html(primary_k)}. "
                f"Shop closer to {_money_html(market_low)}–{_money_html(market_high)}."
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
                        <div class="pcs-out-dual-v">{primary_v}<span>/mo</span></div>
                    </div>
                    <div class="pcs-out-dual-secondary">
                        <div class="pcs-out-dual-k">Typical {bed_label} rent</div>
                        <div class="pcs-out-dual-v-sm">{_money_html(market_low)}–{_money_html(market_high)}</div>
                        <div class="pcs-out-dual-sub">Mid {_money_html(market_mid)} · {safe_html(dep_label)}</div>
                    </div>
                </div>
                <div class="pcs-out-fit pcs-out-fit-{fit_tone}">{fit_line}</div>
                <div class="pcs-sticky-results-meta pcs-out-profile">
                    {safe_html(pay_grade)} · {safe_html(rank_label)} · {safe_html(dep_label)} · {int(yos)} YOS
                    · total {_money_html(total)}/mo
                    {f'· COLA {_money_html(cola)}' if cola else ''}
                </div>
                <div class="pcs-sticky-results-grid pcs-sticky-results-grid-4">
                    <div><b>Utilities</b><br>{_money_html(util_n) if util_n else '—'}</div>
                    <div><b>DLA</b><br>{_dla_html(dla_amt)}</div>
                    <div><b>Move-in cash</b><br>{_money_html(move_in) if move_in else '—'}</div>
                    <div><b>Still need</b><br>{gap_html}</div>
                </div>
            </div>
            """
        )

        # Spell out package parts for OCONUS / HI / PR / AK
        if system == "OHA":
            util_oha = pkg.get("oha_utility_usd")
            if pkg.get("cola_index") is not None:
                cola_note = f"COLA · index {pkg.get('cola_index')}"
            else:
                cola_note = "No COLA at this locality right now"
            _render_html(
                f"""
                <div class="pcs-out-split">
                    <div class="pcs-out-split-item">
                        <span>OHA rent max</span>
                        <strong>{_money_html(oha_rent)}</strong>
                        <div class="pcs-pkg-note">Overseas Housing Allowance</div>
                    </div>
                    <div class="pcs-out-split-item">
                        <span>OHA utilities</span>
                        <strong>{_money_html(int(util_oha) if util_oha else None)}</strong>
                    </div>
                    <div class="pcs-out-split-item">
                        <span>COLA</span>
                        <strong>{_money_html(cola)}</strong>
                        <div class="pcs-pkg-note">{safe_html(cola_note)}</div>
                    </div>
                </div>
                <div class="pcs-pkg-grand">
                    <span>Total (OHA housing + COLA)</span>
                    <strong>{_money_html(total)}/mo</strong>
                </div>
                """
            )
        elif system == "BAH_PLUS_COLA":
            cola_note = (
                f"COLA · index {pkg.get('cola_index')} · not for rent"
                if pkg.get("cola_index") is not None
                else "COLA · not for rent"
            )
            _render_html(
                f"""
                <div class="pcs-out-split">
                    <div class="pcs-out-split-item">
                        <span>BAH</span>
                        <strong>{_money_html(housing)}</strong>
                        <div class="pcs-pkg-note">Basic Allowance for Housing</div>
                    </div>
                    <div class="pcs-out-split-item">
                        <span>COLA</span>
                        <strong>{_money_html(cola)}</strong>
                        <div class="pcs-pkg-note">{safe_html(cola_note)}</div>
                    </div>
                    <div class="pcs-out-split-item">
                        <span>Total</span>
                        <strong>{_money_html(total)}</strong>
                        <div class="pcs-pkg-note">BAH + COLA</div>
                    </div>
                </div>
                """
            )

        if current and cur and cur.get("found") and delta is not None:
            tone = "up" if delta > 0 else ("down" if delta < 0 else "flat")
            curr_tot = int(cur["total_monthly_usd"])
            pct = _pct_change(curr_tot, total)
            pct_txt = f"{pct:+d}%" if pct is not None else ""

            cur_market = get_family_market_rent(current, num_dependents=int(num_deps))
            cur_mid = int(cur_market["mid_usd"])
            market_delta = market_mid - cur_mid
            pressure = int(delta) - market_delta

            if market_delta < -50:
                market_note = (
                    f"Typical {bed_label} rent also drops "
                    f"({_money_html(cur_mid)} → {_money_html(market_mid)})."
                )
            elif market_delta > 50:
                market_note = (
                    f"Typical {bed_label} rent rises "
                    f"({_money_html(cur_mid)} → {_money_html(market_mid)})."
                )
            else:
                market_note = f"Typical {bed_label} rent is about the same ({_money_html(market_mid)})."

            if pressure < -100:
                pressure_note = f"Net: about {_money_html(abs(pressure))}/mo tighter."
            elif pressure > 100:
                pressure_note = f"Net: about {_money_html(pressure)}/mo easier."
            else:
                pressure_note = "Net: allowance and rent changes roughly even out."

            tip = ""
            if dla_covers:
                tip = f"DLA (~{_dla_html(dla_amt)}) can cover a typical move-in (~{_money_html(move_in)})."
            elif move_in and arrive["net"]:
                tip = f"Plan ~{_money_html(arrive['net'])} of your own cash after DLA."

            left = _package_side_html(cur, side_label="Current")
            right = _package_side_html(pkg, side_label="New")
            _render_html(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone} pcs-out-compare">
                    <div class="pcs-out-compare-title">Current vs new — side by side</div>
                    <div class="pcs-pkg-grid">
                        {left}
                        <div class="pcs-pkg-mid">
                            <div class="pcs-pkg-mid-delta">{_money_html(int(delta))}/mo</div>
                            <div class="pcs-pkg-mid-sub">{safe_html(pct_txt)}</div>
                            <div class="pcs-pkg-mid-sub">{_money_html(int(annual or 0))}/yr</div>
                        </div>
                        {right}
                    </div>
                    <div class="pcs-out-compare-action">
                        {market_note} {pressure_note}
                        {f'<br>{tip}' if tip else ''}
                    </div>
                </div>
                """
            )
        else:
            st.caption("Pick a Current post above to compare both locations side by side.")

        info = get_installation_data(gaining) or {}
        with st.expander(f"Local areas & utility ranges — {gaining}", expanded=False):
            notes = (info.get("notes") or "").strip()
            if notes:
                st.markdown(notes)
            areas_list = info.get("major_areas") or []
            commute = (info.get("commute_notes") or "").strip()
            if areas_list:
                st.caption("Nearby: " + ", ".join(areas_list[:4]))
            if commute:
                st.caption(commute)
            if areas:
                st.caption(
                    (util_ctx.get("as_of") or "2026")
                    + " · typical off-post bills (electric, heat/gas, water/trash, internet)"
                )
                if not util_ctx.get("found", True):
                    st.caption("Using a regional estimate — local bills can differ.")
                rows = []
                for a in areas[:5]:
                    tot = a.get("total_utilities_usd_mo") or {}
                    e = a.get("electric_usd_mo") or {}
                    gas = a.get("gas_or_heat_usd_mo") or {}
                    w = a.get("water_trash_usd_mo") or {}
                    net = a.get("internet_usd_mo") or {}
                    rows.append(
                        {
                            "Area": a.get("name", "—"),
                            "Electric": f"${e.get('low', 0)}–${e.get('high', 0)}",
                            "Heat / gas": f"${gas.get('low', 0)}–${gas.get('high', 0)}",
                            "Water / trash": f"${w.get('low', 0)}–${w.get('high', 0)}",
                            "Internet": f"${net.get('low', 0)}–${net.get('high', 0)}",
                            "Total / mo": f"${tot.get('low', 0)}–${tot.get('high', 0)}",
                        }
                    )
                st.dataframe(rows, use_container_width=True, hide_index=True)
                if areas[0].get("season_note"):
                    st.caption(areas[0]["season_note"])
                if system == "OHA":
                    st.caption(
                        "OHA already includes a utilities allowance in your package above — "
                        "use this table to compare real-world bills."
                    )

        st.caption("Planning figures only · verify on your LES / with finance before you sign a lease.")

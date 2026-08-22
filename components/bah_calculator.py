"""PCS finance calculator — inputs + clear Soldier-ready output."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import list_bah_installations
from services.dla_rates import format_dla_usd, get_dla_rate
from services.housing_allowances import compare_housing_packages
from services.installation_data import SUPPORTED_INSTALLATIONS, get_installation_data
from services.utility_costs import get_utility_costs_for_installation

YOS_OPTIONS = list(range(0, 41))
_NONE_CURRENT = "— Skip comparison —"
_DEP_OPTIONS = [0, 1, 2, 3, 4, 5]
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
        "util": util,
        "dla": dla,
        "net": max(gross - dla, 0),
    }


def _system_plain(system: str) -> tuple[str, str]:
    """Return (short chip, one-line plain English)."""
    if system == "OHA":
        return (
            "OHA + COLA",
            "Overseas: OHA covers rent up to a ceiling + utilities; COLA helps with everyday costs — not rent.",
        )
    if system == "BAH_PLUS_COLA":
        return (
            "BAH + COLA",
            "Hawaii / Puerto Rico style: BAH is your housing check; COLA helps with higher day-to-day costs.",
        )
    return (
        "BAH",
        "Flat monthly U.S. housing allowance. Rent and most utilities come out of this number.",
    )


def _spouse_blurb(
    *,
    gaining: str,
    total: int,
    system_chip: str,
    rent_tgt: int | None,
    delta: int | None,
    current: str | None,
    dla_usd: float | None,
    arrive_net: int | None,
) -> str:
    parts = [
        f"Hey — PCS housing money for {gaining}: {_money(total)}/mo ({system_chip}).",
    ]
    if rent_tgt is not None:
        parts.append(f"Aim for rent around {_money(rent_tgt)}/mo.")
    if current and delta is not None:
        parts.append(f"That’s {_money(int(delta))}/mo vs {current}.")
    if dla_usd:
        parts.append(f"DLA planning {format_dla_usd(dla_usd)} one-time when authorized.")
    if arrive_net is not None:
        parts.append(f"Rough cash to arrive ready: ~{_money(arrive_net)} after DLA.")
    parts.append("PCS Vector — Built For Soldiers; By Soldiers.")
    return " ".join(parts)


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
        rent_tgt = _rent_target(
            system=system, housing=housing, util_mid=util_mid, oha_rent_max=oha_rent
        )

        cur = result.get("current")
        delta = result.get("monthly_delta_usd")
        annual = result.get("annual_delta_usd")
        if not (current and cur and cur.get("found") and delta is not None):
            delta = None
            annual = None

        system_chip, system_plain = _system_plain(system)
        rank_label = PAY_GRADE_TO_RANK.get(pay_grade, pay_grade)
        dep_label = _deps_label(int(num_deps))

        dla = get_dla_rate(pay_grade, with_dependents=with_dependents)
        dla_amt = float(dla["dla_usd"]) if dla.get("found") else None
        arrive = _arrive_cash(rent_tgt, dla_amt, util_mid)

        share = f"{pay_grade} @ {gaining}: {_money(total)}/mo ({system_chip})"
        if current and delta is not None:
            share += f" · {_money(int(delta))}/mo vs {current}"
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
            arrive_net=arrive["net"] if rent_tgt else None,
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

        # ── Loop 1: Primary result ──
        st.markdown(
            f"""
            <div class="pcs-sticky-results">
                <div class="pcs-out-label">{safe_html(gaining)} · {safe_html(system_chip)}</div>
                <div class="pcs-sticky-results-main">
                    <span class="pcs-sticky-results-amt">{_money(total)}</span>
                    <span class="pcs-sticky-results-unit">/mo total</span>
                </div>
                <div class="pcs-sticky-results-meta pcs-out-profile">
                    {safe_html(pay_grade)} · {safe_html(rank_label)} · {safe_html(dep_label)} · {int(yos)} years of service
                    · {_money(total * 12)}/year
                </div>
                <div class="pcs-out-plain">{safe_html(system_plain)}</div>
                <div class="pcs-sticky-results-grid">
                    <div><b>Rent target</b><br>{_money(rent_tgt)}/mo</div>
                    <div><b>DLA (one-time)</b><br>{safe_html(format_dla_usd(dla_amt) if dla_amt is not None else '—')}</div>
                    <div><b>Move-in gap</b><br>{
                        'Covered by DLA'
                        if arrive['dla'] and rent_tgt and arrive['dla'] >= (arrive['deposit'] + arrive['first_month'])
                        else _money(arrive['net'])
                    }</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Package breakdown (only when it adds info beyond the total)
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

        # Post-to-post compare — what changed + what to do
        if current and cur and cur.get("found") and delta is not None:
            tone = "up" if delta > 0 else ("down" if delta < 0 else "flat")
            curr_tot = int(cur["total_monthly_usd"])
            rent_line = (
                f"Shop rent at or under <strong>{_money(rent_tgt)}/mo</strong> at {safe_html(gaining)}."
                if rent_tgt
                else f"Use the rent target above for {safe_html(gaining)}."
            )
            if delta < -100:
                do_next = (
                    f"Housing check drops {_money(abs(int(delta)))}/mo "
                    f"(~{_money(abs(int(annual or 0)))}/yr). {rent_line} "
                    "Don’t carry your old rent level forward."
                )
            elif delta > 100:
                do_next = (
                    f"Housing check rises {_money(int(delta))}/mo "
                    f"(~{_money(int(annual or 0))}/yr). {rent_line} "
                    "Keep the surplus — don’t inflate lifestyle on day one."
                )
            else:
                do_next = (
                    f"Totals are close. {rent_line} "
                    "Local rent and utilities still decide how it feels."
                )
            st.markdown(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone} pcs-out-compare">
                    <div class="pcs-out-compare-title">Post comparison</div>
                    <div class="pcs-out-vs">
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Coming from</div>
                            <div class="pcs-out-vs-v">{_money(curr_tot)}<span>/mo</span></div>
                            <div class="pcs-out-vs-s">{safe_html(current)}</div>
                        </div>
                        <div class="pcs-out-vs-mid">
                            <div class="pcs-out-vs-delta">{_money(int(delta))}/mo</div>
                            <div class="pcs-out-vs-yr">{_money(int(annual or 0))}/yr</div>
                        </div>
                        <div class="pcs-out-vs-col">
                            <div class="pcs-out-vs-k">Going to</div>
                            <div class="pcs-out-vs-v">{_money(total)}<span>/mo</span></div>
                            <div class="pcs-out-vs-s">{safe_html(gaining)}</div>
                        </div>
                    </div>
                    <div class="pcs-out-compare-action"><b>What to do:</b> {do_next}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Move-in cushion — honest about DLA covering costs
        if rent_tgt and rent_tgt > 0:
            move_in = arrive["deposit"] + arrive["first_month"]
            dla_v = arrive["dla"]
            if dla_v and dla_v >= move_in:
                cushion_html = (
                    f"<b>Move-in cushion:</b> Typical deposit + first month ≈ {_money(move_in)}. "
                    f"DLA planning ({_money(dla_v)}) can cover that — "
                    f"<strong>you may not need extra cash for a basic move-in</strong> if DLA hits on time. "
                    f"Still keep a buffer: some leases want first + last + deposit, plus travel costs."
                )
            elif dla_v:
                short = move_in - dla_v
                cushion_html = (
                    f"<b>Move-in cushion:</b> Typical deposit + first month ≈ {_money(move_in)}. "
                    f"DLA planning ({_money(dla_v)}) leaves about <strong>{_money(short)}</strong> "
                    f"to cover from savings or a travel advance. Confirm DLA timing with finance."
                )
            else:
                cushion_html = (
                    f"<b>Move-in cushion:</b> Plan about <strong>{_money(move_in)}</strong> "
                    f"for deposit + first month (rent + utilities). No DLA figure on file for this profile."
                )
            st.markdown(
                f"""
                <div class="pcs-out-arrive">
                    {cushion_html}
                    <span class="pcs-out-arrive-note">Assumes ~1× rent deposit and mid-range utilities. Leases vary.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Intel + share
        info = get_installation_data(gaining) or {}
        with st.expander(f"Local intel, utilities & text-to-share — {gaining}", expanded=False):
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
                st.markdown("**Off-post utilities** (typical 3BR planning ranges)")
                st.caption(
                    (util_ctx.get("as_of") or "2026")
                    + (f" · mid ~{_money(util_mid)}/mo" if util_mid else "")
                    + " · verify with landlord"
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
            st.markdown("**Copy for spouse / battle buddy**")
            st.code(spouse, language=None)

        st.caption("Planning figures only — verify on your LES and with finance / DTMO before you sign.")

"""PCS finance calculator — inputs + clear Soldier-ready output."""

from __future__ import annotations

from typing import Any

import streamlit as st
import streamlit.components.v1 as components

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


def _housing_face(pkg: dict[str, Any]) -> tuple[int | None, str]:
    """Primary housing allowance shown in comparisons (real tables — not partner ×0.82)."""
    system = pkg.get("housing_system") or "BAH"
    if system == "OHA" and pkg.get("oha_rent_max_usd") is not None:
        return int(pkg["oha_rent_max_usd"]), "OHA rent max"
    if pkg.get("housing_monthly_usd") is not None:
        label = "BAH" if system != "OHA" else "OHA housing"
        return int(pkg["housing_monthly_usd"]), label
    return None, "BAH"


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
        return "0"
    if n == 5:
        return "5+"
    return str(int(n))


def _wrap_inputs_panel() -> None:
    """Wrap Streamlit input widgets in a partner-style nested panel."""
    components.html(
        """
<script>
(function () {
  var doc = window.parent.document;
  function wrap() {
    var start = doc.getElementById("pcs-inputs-start");
    var end = doc.getElementById("pcs-inputs-end");
    if (!start || !end) return;
    var existing = doc.getElementById("pcs-inputs-panel");
    if (existing && existing.contains(start) && existing.contains(end)) return;
    if (existing) {
      try { existing.replaceWith.apply(existing, Array.from(existing.childNodes)); } catch (e) {}
    }
    var panel = doc.createElement("div");
    panel.id = "pcs-inputs-panel";
    panel.className = "pcs-partner-panel pcs-partner-inputs";

    // Collect nodes from start through end across Streamlit element wrappers
    var nodes = [];
    var root = start.closest('[data-testid="stVerticalBlock"]') || start.parentNode;
    if (!root) return;
    var collecting = false;
    var kids = Array.from(root.children);
    kids.forEach(function (el) {
      if (el.contains(start) || el === start) collecting = true;
      if (collecting) nodes.push(el);
      if (el.contains(end) || el === end) collecting = false;
    });
    if (!nodes.length) return;
    nodes[0].parentNode.insertBefore(panel, nodes[0]);
    nodes.forEach(function (el) { panel.appendChild(el); });
  }
  wrap();
  [80, 250, 600].forEach(function (ms) { setTimeout(wrap, ms); });
})();
</script>
        """,
        height=0,
    )


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

    st.markdown('<div id="pcs-inputs-start"></div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    with r1:
        pay_grade = st.selectbox(
            "Rank",
            options=grades,
            index=grades.index("E-5") if "E-5" in grades else 0,
            format_func=lambda g: f"{g} — {PAY_GRADE_TO_RANK.get(g, g)}",
            key="bah_calc_grade",
        )
    with r2:
        num_deps = st.selectbox(
            "Dependents",
            options=[0, 1, 2, 3, 4, 5],
            index=1,
            format_func=_deps_label,
            key="bah_calc_deps_n",
        )
        with_dependents = int(num_deps) > 0
    with r3:
        yos = st.selectbox(
            "YOS",
            options=YOS_OPTIONS,
            index=4,
            key="bah_calc_yos",
            help="Used for COLA overseas and in Hawaii / Puerto Rico.",
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
            help="Skip = target post only. Pick a post to compare BAH.",
        )
        current = None if current_raw == _NONE_CURRENT else current_raw
    with d2:
        gaining = st.selectbox(
            "Target post",
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

    st.markdown('<div id="pcs-inputs-end"></div>', unsafe_allow_html=True)
    _wrap_inputs_panel()

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

    new_face, new_face_k = _housing_face(pkg)
    util_n = int(util_mid or 0)
    bed_label = f"{bedrooms}BR"
    all_in_mid = market_mid + util_n
    leftover_mid = rent_budget - all_in_mid
    if leftover_mid >= 0:
        fit_line = (
            f"Typical {bed_label} + utilities ≈ {_money_html(all_in_mid)}/mo — "
            f"<strong>{_money_html(leftover_mid)}/mo</strong> left in {safe_html(new_face_k)}."
        )
        fit_tone = "fit"
    else:
        fit_line = (
            f"Typical {bed_label} + utilities ≈ {_money_html(all_in_mid)}/mo — "
            f"<strong>{_money_html(abs(leftover_mid))}/mo</strong> over {safe_html(new_face_k)}. "
            f"Shop closer to {_money_html(market_low)}–{_money_html(market_high)}."
        )
        fit_tone = "tight"

    gap_txt = (
        safe_html(move_gap_label)
        if move_gap_label == "DLA covers this"
        else (_money_html(arrive["net"]) if arrive.get("net") is not None else "—")
    )

    has_compare = bool(current and cur and cur.get("found"))
    cur_face = None
    cur_rent_lo = cur_rent_hi = cur_util_n = cur_mid = None
    if has_compare:
        cur_face, _cur_k = _housing_face(cur)
        cur_is_oconus = (cur.get("housing_system") or "") in ("OHA", "BAH_PLUS_COLA")
        cur_util_ctx = get_utility_costs_for_installation(current, is_oconus=cur_is_oconus)
        cur_util_n = _util_mid(cur_util_ctx.get("areas") or []) or 0
        cur_market = get_family_market_rent(current, num_dependents=int(num_deps))
        cur_rent_lo = int(cur_market["low_usd"])
        cur_rent_hi = int(cur_market["high_usd"])
        cur_mid = int(cur_market["mid_usd"])

    # Partner-style header: big BAH → BAH (or single target when Skip)
    if has_compare and cur_face is not None and new_face is not None:
        bah_delta = int(new_face) - int(cur_face)
        if bah_delta > 0:
            delta_cls, delta_txt = "pcs-delta-up", f"+{_money_html(bah_delta)}/mo"
        elif bah_delta < 0:
            delta_cls, delta_txt = "pcs-delta-down", f"-{_money_html(abs(bah_delta))}/mo"
        else:
            delta_cls, delta_txt = "pcs-delta-flat", "$0/mo"
        arrow_html = f"""
        <div class="pcs-partner-arrow">
            <span class="pcs-partner-arrow-amt muted">{_money_html(cur_face)}</span>
            <span class="pcs-partner-arrow-glyph">➔</span>
            <span class="pcs-partner-arrow-amt">{_money_html(new_face)}</span>
        </div>
        <div class="pcs-partner-delta-row">
            <span>Monthly {safe_html(new_face_k)} delta</span>
            <span class="pcs-bah-delta-badge {delta_cls}">{delta_txt}</span>
        </div>
        """
        if cur_mid and cur_mid > 0:
            rent_pct = int(round(((market_mid - cur_mid) / cur_mid) * 100))
            if rent_pct < 0:
                roll_cls, roll_txt = "pcs-roll-down", f"{abs(rent_pct)}% CHEAPER"
            elif rent_pct > 0:
                roll_cls, roll_txt = "pcs-roll-up", f"{rent_pct}% MORE EXP."
            else:
                roll_cls, roll_txt = "pcs-roll-flat", "EQUAL COST"
            rollup_html = f"""
            <div class="pcs-partner-rollup">
                <span>Typical rent pressure</span>
                <span class="pcs-partner-rollup-badge {roll_cls}">{roll_txt}</span>
            </div>
            """
        else:
            rollup_html = ""
        left_rent = f"{_money_html(cur_rent_lo)}–{_money_html(cur_rent_hi)}"
        left_util = f"{_money_html(int(cur_util_n or 0))}/mo"
        left_dla = "—"
        left_need = "—"
    else:
        arrow_html = f"""
        <div class="pcs-partner-arrow pcs-partner-arrow-solo">
            <span class="pcs-partner-arrow-amt">{_money_html(new_face)}<span class="pcs-partner-per">/mo</span></span>
        </div>
        <div class="pcs-partner-delta-row">
            <span>{safe_html(new_face_k)} · {safe_html(gaining)}</span>
            <span class="pcs-bah-delta-badge pcs-delta-flat">{safe_html(pay_grade)} · {safe_html(dep_label)}</span>
        </div>
        """
        rollup_html = ""
        left_rent = "—"
        left_util = "—"
        left_dla = "—"
        left_need = "—"

    _render_html(
        f"""
        <div class="pcs-partner-panel pcs-partner-results">
            {arrow_html}
            {rollup_html}
            <div class="pcs-partner-breakdown">
                <div class="pcs-partner-breakdown-title">Itemized expense breakdown</div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_rent}</span>
                    <span class="pcs-est-label">Typical rent (est.)</span>
                    <span class="pcs-est-side pcs-est-side-new">{_money_html(market_low)}–{_money_html(market_high)}</span>
                </div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_util}</span>
                    <span class="pcs-est-label">Utilities (est.)</span>
                    <span class="pcs-est-side pcs-est-side-new">{(_money_html(util_n) + '/mo') if util_n else '—'}</span>
                </div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_dla}</span>
                    <span class="pcs-est-label">DLA</span>
                    <span class="pcs-est-side pcs-est-side-new">{_dla_html(dla_amt)}</span>
                </div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_need}</span>
                    <span class="pcs-est-label">Still need after DLA</span>
                    <span class="pcs-est-side pcs-est-side-new">{gap_txt}</span>
                </div>
            </div>
            <div class="pcs-out-fit pcs-out-fit-{fit_tone}">{fit_line}</div>
            <div class="pcs-partner-meta">
                {safe_html(pay_grade)} · {safe_html(rank_label)} · {safe_html(dep_label)} · {int(yos)} YOS
                · total {_money_html(total)}/mo
                {f'· COLA {_money_html(cola)}' if cola else ''}
                · move-in {_money_html(move_in) if move_in else '—'}
            </div>
        </div>
        """
    )

    detail_bits: list[str] = []
    if system in ("OHA", "BAH_PLUS_COLA"):
        detail_bits.append(_package_side_html(pkg, side_label="Target package"))
    if has_compare and cur:
        detail_bits.append(_package_side_html(cur, side_label="Current package"))
        if delta is not None:
            detail_bits.append(
                f'<div class="pcs-partner-meta">Package total delta: '
                f"{_money_html(int(delta))}/mo"
                f"{f' · {_money_html(int(annual))}/yr' if annual is not None else ''}"
                f"</div>"
            )

    info = get_installation_data(gaining) or {}
    with st.expander("More detail · package & local utilities", expanded=False):
        if detail_bits:
            _render_html("".join(detail_bits))
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

    st.caption("Planning figures · verify LES / finance before you sign.")

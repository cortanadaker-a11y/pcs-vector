"""PCS finance calculator — inputs + clear Soldier-ready output."""

from __future__ import annotations

from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from components.form_options import RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import list_bah_installations
from services.dla_rates import get_dla_rate
from services.gas_prices import get_gas_price_for_installation
from services.housing_allowances import compare_housing_packages
from services.installation_data import (
    SUPPORTED_INSTALLATIONS,
    get_family_market_rent,
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


def wrap_dom_panel(
    *,
    start_id: str,
    end_id: str,
    panel_id: str,
    panel_class: str = "pcs-partner-panel",
) -> None:
    """Wrap Streamlit blocks between markers into one visual panel."""
    components.html(
        f"""
<script>
(function () {{
  var doc = window.parent.document;
  var startId = {start_id!r};
  var endId = {end_id!r};
  var panelId = {panel_id!r};
  var panelClass = {panel_class!r};
  function wrap() {{
    var start = doc.getElementById(startId);
    var end = doc.getElementById(endId);
    if (!start || !end) return;
    // Never unwrap/rebuild — remounting Streamlit widgets crashes on rerun
    if (doc.getElementById(panelId)) return;
    var panel = doc.createElement("div");
    panel.id = panelId;
    panel.className = panelClass;
    var root = start.closest('[data-testid="stVerticalBlock"]') || start.parentNode;
    if (!root) return;
    var nodes = [];
    var collecting = false;
    Array.from(root.children).forEach(function (el) {{
      if (el.contains(start) || el === start) collecting = true;
      if (collecting) nodes.push(el);
      if (el.contains(end) || el === end) collecting = false;
    }});
    if (!nodes.length) return;
    nodes[0].parentNode.insertBefore(panel, nodes[0]);
    nodes.forEach(function (el) {{ panel.appendChild(el); }});
  }}
  wrap();
  [100, 300].forEach(function (ms) {{ setTimeout(wrap, ms); }});
}})();
</script>
        """,
        height=0,
    )


def _wrap_inputs_panel() -> None:
    wrap_dom_panel(
        start_id="pcs-inputs-start",
        end_id="pcs-inputs-end",
        panel_id="pcs-inputs-panel",
        panel_class="pcs-face-section pcs-face-section-inputs",
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


def _system_chip(system: str, *, barracks: bool = False, cola: int = 0) -> str:
    if barracks:
        return "Barracks + COLA" if int(cola or 0) > 0 else "Barracks"
    if system == "OHA":
        return "OHA + COLA"
    if system == "BAH_PLUS_COLA":
        return "BAH + COLA"
    return "BAH"


def _dla_html(amount: float | None) -> str:
    if amount is None:
        return "—"
    return _money_html(int(round(amount)))


def render_bah_calculator() -> None:
    installations = list_bah_installations()
    if list(installations) != list(SUPPORTED_INSTALLATIONS):
        installations = list(SUPPORTED_INSTALLATIONS)
    if not installations:
        return

    grades = [g for g in RANK_PAY_GRADES if g != "Other"]

    # Inputs well starts here — brand lives above the calculator card on home
    st.markdown('<div id="pcs-inputs-start"></div>', unsafe_allow_html=True)

    if "bah_calc_gaining" not in st.session_state:
        st.session_state.bah_calc_gaining = (
            "Fort Bragg, NC" if "Fort Bragg, NC" in installations else installations[0]
        )
    # Default Current like the HTML demo (comparison visible immediately)
    if "bah_calc_current" not in st.session_state:
        default_cur = "Fort Campbell, KY"
        if default_cur not in installations or default_cur == st.session_state.bah_calc_gaining:
            default_cur = next(
                (p for p in installations if p != st.session_state.bah_calc_gaining),
                _NONE_CURRENT,
            )
        st.session_state.bah_calc_current = default_cur

    r1, r2, r3 = st.columns(3)
    with r1:
        pay_grade = st.selectbox(
            "Rank",
            options=grades,
            index=grades.index("E-5") if "E-5" in grades else 0,
            format_func=lambda g: g,
            key="bah_calc_grade",
        )
    with r2:
        num_deps_raw = st.selectbox(
            "Dependents",
            options=[0, 1, 2, 3, 4, 5],
            index=0,
            format_func=_deps_label,
            key="bah_calc_deps_n",
        )
        try:
            num_deps = int(num_deps_raw)
        except (TypeError, ValueError):
            num_deps = 0
        num_deps = max(0, min(5, num_deps))
        with_dependents = num_deps > 0
    with r3:
        yos = st.selectbox(
            "Years of service",
            options=YOS_OPTIONS,
            index=4,
            key="bah_calc_yos",
        )

    d1, d2 = st.columns(2)
    with d1:
        current_raw = st.selectbox(
            "Current Post",
            options=[_NONE_CURRENT] + installations,
            key="bah_calc_current",
            help="Pick a post to compare. Use Skip compare for target only.",
        )
        current = None if current_raw == _NONE_CURRENT else current_raw
    with d2:
        gaining = st.selectbox(
            "Target Post",
            options=installations,
            key="bah_calc_gaining",
        )

    # Always render this widget (never mount/unmount) — toggling it with
    # dependents was crashing Streamlit on rerun.
    barracks_on = st.checkbox(
        "Barracks + meal card (no BAH)",
        value=False,
        key="bah_calc_barracks",
        disabled=with_dependents,
        help="Single Soldiers in the barracks do not get BAH or OHA. Meal card replaces BAS. OCONUS COLA is reduced.",
    )
    if with_dependents:
        barracks_on = False

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
        if (pkg.get("housing_system") or "") == "OHA":
            loc = pkg.get("locality") or gaining
            idx = pkg.get("cola_index")
            cola_bit = f" COLA index is {idx}." if idx is not None else ""
            st.warning(
                f"{gaining} uses OHA (not BAH). Look up the current rent ceiling and "
                f"utility allowance at the DTMO OHA Rate Lookup for {loc}.{cola_bit} "
                "Do not use a CONUS BAH figure for this post."
            )
        else:
            st.warning(
                f"No 2026 rates for {pay_grade} at {gaining}. Try another post or ask finance."
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

    cur = result.get("current")
    delta = result.get("monthly_delta_usd")
    if not (current and cur and cur.get("found") and delta is not None):
        delta = None

    dep_label = _deps_label(int(num_deps))

    dla = get_dla_rate(pay_grade, with_dependents=with_dependents)
    dla_amt = float(dla["dla_usd"]) if dla.get("found") else None
    arrive = _arrive_cash(market_mid, dla_amt, util_mid)

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

    # Per-side systems (Germany OHA+COLA → Jackson BAH must compare TOTALS)
    tgt_barracks = bool(pkg.get("in_government_quarters"))
    cur_barracks = bool(has_compare and cur and cur.get("in_government_quarters"))
    cur_sys = (cur.get("housing_system") or "BAH") if (has_compare and cur) else None
    cur_cola_preview = int(cur.get("cola_monthly_usd") or 0) if (has_compare and cur) else 0
    system_chip = _system_chip(system, barracks=tgt_barracks, cola=cola)
    cur_sys_chip = (
        _system_chip(cur_sys, barracks=cur_barracks, cola=cur_cola_preview) if cur_sys else ""
    )
    cur_total = (
        int(cur["total_monthly_usd"])
        if has_compare and cur and cur.get("total_monthly_usd") is not None
        else None
    )

    cur_oha_rent = cur_oha_util = None
    cur_bah = None
    cur_cola = 0
    if has_compare and cur:
        if cur_sys == "OHA":
            if cur.get("oha_rent_max_usd") is not None:
                cur_oha_rent = int(cur["oha_rent_max_usd"])
            if cur.get("oha_utility_usd") is not None:
                cur_oha_util = int(cur["oha_utility_usd"])
        else:
            if cur.get("housing_monthly_usd") is not None:
                cur_bah = int(cur["housing_monthly_usd"])
        cur_cola = int(cur.get("cola_monthly_usd") or 0)

    oha_util = int(pkg["oha_utility_usd"]) if pkg.get("oha_utility_usd") is not None else None
    cola_idx = pkg.get("cola_index")
    tgt_bah = housing if system != "OHA" else None
    tgt_oha_rent = oha_rent if system == "OHA" else None

    # Arrow + delta = Total package (includes OHA util + COLA) — never OHA-rent vs BAH
    if has_compare and cur_total is not None:
        pkg_delta = int(total) - int(cur_total)
        if pkg_delta > 0:
            delta_cls, delta_txt = "pcs-delta-up", f"+{_money_html(pkg_delta)}/mo"
        elif pkg_delta < 0:
            delta_cls, delta_txt = "pcs-delta-down", f"-{_money_html(abs(pkg_delta))}/mo"
        else:
            delta_cls, delta_txt = "pcs-delta-flat", "$0/mo"
        arrow_html = f"""
        <div class="pcs-partner-arrow">
            <div class="pcs-partner-arrow-col">
                <div class="pcs-partner-arrow-loc">Current · {safe_html(cur_sys_chip)}</div>
                <span class="pcs-partner-arrow-amt muted">{_money_html(cur_total)}</span>
            </div>
            <span class="pcs-partner-arrow-glyph">➔</span>
            <div class="pcs-partner-arrow-col pcs-partner-arrow-col-new">
                <div class="pcs-partner-arrow-loc">Target · {safe_html(system_chip)}</div>
                <span class="pcs-partner-arrow-amt">{_money_html(total)}</span>
            </div>
        </div>
        <div class="pcs-partner-delta-row">
            <span>Monthly total package</span>
            <span class="pcs-bah-delta-badge {delta_cls}">{delta_txt}</span>
        </div>
        """
        # COL index = typical rent mid + utilities (same figures as the rows above)
        cur_col = int(cur_mid or 0) + int(cur_util_n or 0)
        tgt_col = int(market_mid or 0) + int(util_n or 0)
        if cur_col > 0:
            col_pct = int(round(((tgt_col - cur_col) / cur_col) * 100))
            if col_pct < 0:
                roll_cls, roll_txt = "pcs-roll-down", f"{abs(col_pct)}% lower"
            elif col_pct > 0:
                roll_cls, roll_txt = "pcs-roll-up", f"{col_pct}% higher"
            else:
                roll_cls, roll_txt = "pcs-roll-flat", "about the same"
            rollup_html = f"""
            <div class="pcs-partner-rollup">
                <span>New Cost of Living Index</span>
                <span class="pcs-partner-rollup-mids">{_money_html(cur_col)} → {_money_html(tgt_col)}</span>
                <span class="pcs-partner-rollup-badge {roll_cls}">{roll_txt}</span>
            </div>
            """
        else:
            rollup_html = ""
        left_rent = f"{_money_html(cur_rent_lo)} – {_money_html(cur_rent_hi)}"
        left_util = f"{_money_html(int(cur_util_n or 0))}/mo"
        left_gas = (get_gas_price_for_installation(current) or {}).get("label") or "—"
    else:
        arrow_html = f"""
        <div class="pcs-partner-arrow pcs-partner-arrow-solo">
            <div class="pcs-partner-arrow-col pcs-partner-arrow-col-new">
                <div class="pcs-partner-arrow-loc">Target · {safe_html(system_chip)}</div>
                <span class="pcs-partner-arrow-amt">{_money_html(total)}</span>
            </div>
        </div>
        <div class="pcs-partner-delta-row">
            <span>{safe_html(gaining)}</span>
            <span class="pcs-bah-delta-badge pcs-delta-flat">{_money_html(total)}/mo total</span>
        </div>
        """
        rollup_html = ""
        left_rent = "—"
        left_util = "—"
        left_gas = "—"

    right_rent = f"{_money_html(market_low)} – {_money_html(market_high)}"
    right_util = f"{_money_html(util_n)}/mo" if util_n else "—"
    right_gas = (get_gas_price_for_installation(gaining) or {}).get("label") or "—"

    # Allowance rows: show each line only if it applies to Current and/or Target
    allowance_rows = ""
    either_oha = (cur_sys == "OHA") or (system == "OHA")
    either_bah = (cur_sys in ("BAH", "BAH_PLUS_COLA") if cur_sys else False) or (
        system in ("BAH", "BAH_PLUS_COLA")
    )
    if either_oha:
        allowance_rows += f"""
        <div class="pcs-est-row">
            <span class="pcs-est-side">{_money_html(cur_oha_rent) if cur_oha_rent is not None else '—'}</span>
            <span class="pcs-est-label">OHA rent max</span>
            <span class="pcs-est-side pcs-est-side-new">{_money_html(tgt_oha_rent) if tgt_oha_rent is not None else '—'}</span>
        </div>
        <div class="pcs-est-row">
            <span class="pcs-est-side">{_money_html(cur_oha_util) if cur_oha_util is not None else '—'}</span>
            <span class="pcs-est-label">OHA utilities</span>
            <span class="pcs-est-side pcs-est-side-new">{_money_html(oha_util) if oha_util is not None else '—'}</span>
        </div>
        """
    if either_bah:
        allowance_rows += f"""
        <div class="pcs-est-row">
            <span class="pcs-est-side">{_money_html(cur_bah) if cur_bah is not None else '—'}</span>
            <span class="pcs-est-label">BAH</span>
            <span class="pcs-est-side pcs-est-side-new">{_money_html(tgt_bah) if tgt_bah is not None else '—'}</span>
        </div>
        """
    show_cola = (
        either_oha
        or system == "BAH_PLUS_COLA"
        or (cur_sys == "BAH_PLUS_COLA")
        or cola > 0
        or cur_cola > 0
    )
    if show_cola:
        cola_note = ""
        if system in ("OHA", "BAH_PLUS_COLA") and cola_idx is not None:
            cola_note = f" · index {cola_idx}"
        elif system == "BAH" and cola == 0 and (cur_cola > 0 or cur_sys == "OHA"):
            cola_note = " · none at target"
        elif system == "OHA" and cola == 0:
            cola_note = " · none at this location"
        if has_compare and cur_sys in ("OHA", "BAH_PLUS_COLA"):
            left_cola = _money_html(cur_cola)
        elif has_compare and cur_cola > 0:
            left_cola = _money_html(cur_cola)
        else:
            left_cola = "—"
        allowance_rows += f"""
        <div class="pcs-est-row">
            <span class="pcs-est-side">{left_cola}</span>
            <span class="pcs-est-label">COLA{safe_html(cola_note)}</span>
            <span class="pcs-est-side pcs-est-side-new">{_money_html(cola)}/mo</span>
        </div>
        """
    left_total = _money_html(cur_total) if cur_total is not None else "—"
    allowance_rows += f"""
        <div class="pcs-est-row pcs-est-row-emph">
            <span class="pcs-est-side">{left_total}</span>
            <span class="pcs-est-label">Total package</span>
            <span class="pcs-est-side pcs-est-side-new">{_money_html(total)}/mo</span>
        </div>
    """

    _render_html(
        f"""
        <div class="pcs-face-section pcs-face-section-results pcs-partner-results">
            {arrow_html}
            <div class="pcs-partner-breakdown">
                <div class="pcs-est-heads-live"><span>Current</span><span></span><span>Target</span></div>
                <div class="pcs-partner-breakdown-title">Allowances (official tables)</div>
                {allowance_rows}
                <div class="pcs-partner-breakdown-title">Local costs &amp; move-in (estimates)</div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_rent}</span>
                    <span class="pcs-est-label">Typical {bed_label} rent</span>
                    <span class="pcs-est-side pcs-est-side-new">{right_rent}</span>
                </div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_util}</span>
                    <span class="pcs-est-label">Utilities</span>
                    <span class="pcs-est-side pcs-est-side-new">{right_util}</span>
                </div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">{left_gas}</span>
                    <span class="pcs-est-label">Avg gas</span>
                    <span class="pcs-est-side pcs-est-side-new">{right_gas}</span>
                </div>
                <div class="pcs-est-row">
                    <span class="pcs-est-side">—</span>
                    <span class="pcs-est-label">DLA (one-time)</span>
                    <span class="pcs-est-side pcs-est-side-new">{_dla_html(dla_amt)}</span>
                </div>
                {rollup_html}
            </div>
        </div>
        """
    )



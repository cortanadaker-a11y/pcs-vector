"""Homepage 2026 BAH calculator widget."""

from __future__ import annotations

import streamlit as st

from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import compare_bah, get_bah_effective_date, list_bah_installations

# Years of service does not change BAH (rank + dependents + location do).
YOS_OPTIONS = [
    "Under 2 years",
    "2–3 years",
    "4–5 years",
    "6–7 years",
    "8–9 years",
    "10–11 years",
    "12–13 years",
    "14–15 years",
    "16–17 years",
    "18–19 years",
    "20+ years",
]

_NONE_CURRENT = "— Skip comparison (gaining post only) —"
_WITH = "With dependents"
_WITHOUT = "Without dependents"


def _money(n: int | None) -> str:
    if n is None:
        return "—"
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,}"


def _resolve_dependents(deps_value: str) -> bool:
    """Map UI label to boolean. Must not use startswith('With') — Without also starts with With."""
    return deps_value.strip() == _WITH


def render_bah_calculator() -> None:
    """Interactive BAH calculator for the homepage."""
    installations = list_bah_installations()
    if not installations:
        return

    grades = [g for g in RANK_PAY_GRADES if g != "Other"]
    effective = get_bah_effective_date()

    st.markdown(
        f"""
        <div class="pcs-bah-wrap">
            <div class="pcs-bah-header">
                <div class="pcs-bah-badge">2026 rates · free tool</div>
                <h3>BAH Calculator</h3>
                <p class="pcs-bah-sub">
                    Plug in your rank and dependents, pick your posts, and see your monthly
                    housing allowance — plus how much it changes when you PCS.
                    Effective {safe_html(effective)}.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<p class="pcs-bah-section-label">Your profile</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.1, 1.1, 1.2])
        with c1:
            pay_grade = st.selectbox(
                "Pay grade",
                options=grades,
                index=grades.index("E-5") if "E-5" in grades else 0,
                format_func=lambda g: f"{g} — {PAY_GRADE_TO_RANK.get(g, g)}",
                key="bah_calc_grade",
            )
        with c2:
            yos = st.selectbox(
                "Years of service",
                options=YOS_OPTIONS,
                index=2,
                key="bah_calc_yos",
                help="BAH does not change with years of service. Only rank, dependents, and location set your rate.",
            )
        with c3:
            deps = st.radio(
                "Dependents",
                options=[_WITH, _WITHOUT],
                horizontal=True,
                key="bah_calc_deps",
            )

        st.markdown('<p class="pcs-bah-section-label">Duty stations</p>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            gaining = st.selectbox(
                "New post (gaining)",
                options=installations,
                index=installations.index("Fort Bragg, NC")
                if "Fort Bragg, NC" in installations
                else 0,
                key="bah_calc_gaining",
            )
        with d2:
            current_options = [_NONE_CURRENT] + installations
            current_raw = st.selectbox(
                "Current post (optional compare)",
                options=current_options,
                key="bah_calc_current",
                help="Leave as skip to only see BAH at your new installation.",
            )
            current = None if current_raw == _NONE_CURRENT else current_raw

        # Exact match only — "Without dependents".startswith("With") is True and was a bug.
        with_dependents = _resolve_dependents(deps)
        result = compare_bah(
            pay_grade=pay_grade,
            with_dependents=with_dependents,
            gaining_installation=gaining,
            current_installation=current,
        )

        gain = result["gaining"]
        gain_amt = gain.get("monthly_usd")

        if not gain.get("found") or gain_amt is None:
            st.warning(
                f"No 2026 BAH rate on file for {pay_grade} at {gaining}. "
                "Try another post or verify with finance."
            )
            return

        rank_label = PAY_GRADE_TO_RANK.get(pay_grade, pay_grade)
        dep_label = "with dependents" if with_dependents else "without dependents"
        dep_chip = "WITH DEPS" if with_dependents else "NO DEPS"
        gain_int = int(gain_amt)

        # Side-by-side with/without preview so users see both rates for this grade+post
        from services.bah_rates import get_bah_monthly

        alt_with = get_bah_monthly(gaining, pay_grade, with_dependents=True)
        alt_without = get_bah_monthly(gaining, pay_grade, with_dependents=False)

        st.markdown(
            f"""
            <div class="pcs-bah-result" data-deps="{safe_html(dep_chip)}">
                <div class="pcs-bah-result-top">
                    <div class="pcs-bah-result-label">Monthly BAH · {safe_html(gaining)}</div>
                    <span class="pcs-bah-chip pcs-bah-chip-{'with' if with_dependents else 'without'}">{safe_html(dep_chip)}</span>
                </div>
                <div class="pcs-bah-result-amount">{_money(gain_int)}<span>/mo</span></div>
                <div class="pcs-bah-result-meta">
                    {safe_html(pay_grade)} ({safe_html(rank_label)}) · {safe_html(dep_label)} ·
                    {safe_html(yos)}
                </div>
                <div class="pcs-bah-result-annual">
                    {_money(gain_int * 12)} / year housing allowance
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Dual-rate strip — always shows both so toggle change is obvious
        if alt_with is not None and alt_without is not None:
            active_with = "pcs-bah-pair-active" if with_dependents else ""
            active_without = "pcs-bah-pair-active" if not with_dependents else ""
            st.markdown(
                f"""
                <div class="pcs-bah-pair">
                    <div class="pcs-bah-pair-card {active_with}">
                        <div class="pcs-bah-pair-k">With dependents</div>
                        <div class="pcs-bah-pair-v">{_money(int(alt_with))}/mo</div>
                    </div>
                    <div class="pcs-bah-pair-card {active_without}">
                        <div class="pcs-bah-pair-k">Without dependents</div>
                        <div class="pcs-bah-pair-v">{_money(int(alt_without))}/mo</div>
                    </div>
                    <div class="pcs-bah-pair-card pcs-bah-pair-diff">
                        <div class="pcs-bah-pair-k">Dependent difference</div>
                        <div class="pcs-bah-pair-v">{_money(int(alt_with) - int(alt_without))}/mo</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        curr = result.get("current")
        delta = result.get("monthly_delta_usd")
        if current and curr and curr.get("found") and curr.get("monthly_usd") is not None and delta is not None:
            curr_amt = int(curr["monthly_usd"])
            annual = int(result.get("annual_delta_usd") or 0)
            if delta > 0:
                tone = "up"
                headline = f"+{_money(delta)}/mo more at your new post"
                detail = (
                    f"{curr['installation']} → {gaining}: "
                    f"{_money(curr_amt)} becomes {_money(gain_int)}. "
                    f"About {_money(annual)} more per year."
                )
            elif delta < 0:
                tone = "down"
                headline = f"{_money(delta)}/mo less at your new post"
                detail = (
                    f"{curr['installation']} → {gaining}: "
                    f"{_money(curr_amt)} becomes {_money(gain_int)}. "
                    f"About {_money(annual)} less per year — budget the drop before you move."
                )
            else:
                tone = "flat"
                headline = "Same BAH at both posts"
                detail = (
                    f"{curr['installation']} and {gaining} both pay "
                    f"{_money(gain_int)}/mo for your grade and dependency status."
                )

            st.markdown(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone}">
                    <div class="pcs-bah-delta-title">{safe_html(headline)}</div>
                    <div class="pcs-bah-delta-detail">{safe_html(detail)}</div>
                    <div class="pcs-bah-delta-grid">
                        <div class="pcs-bah-delta-cell">
                            <div class="pcs-bah-delta-k">Current</div>
                            <div class="pcs-bah-delta-v">{_money(curr_amt)}/mo</div>
                            <div class="pcs-bah-delta-s">{safe_html(str(curr["installation"]))}</div>
                        </div>
                        <div class="pcs-bah-delta-arrow" aria-hidden="true">→</div>
                        <div class="pcs-bah-delta-cell">
                            <div class="pcs-bah-delta-k">New post</div>
                            <div class="pcs-bah-delta-v">{_money(gain_int)}/mo</div>
                            <div class="pcs-bah-delta-s">{safe_html(gaining)}</div>
                        </div>
                        <div class="pcs-bah-delta-cell">
                            <div class="pcs-bah-delta-k">Change</div>
                            <div class="pcs-bah-delta-v">{_money(int(delta))}</div>
                            <div class="pcs-bah-delta-s">{_money(annual)} / year</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif current:
            st.info(
                f"No comparison rate for {pay_grade} at {current}. "
                "BAH at your gaining post is shown above."
            )

        st.caption(
            "BAH uses pay grade, dependency status, and Military Housing Area — not years of service. "
            "2026 planning rates for supported installations. "
            "Verify with finance or the official DTMO BAH calculator before signing a lease."
        )

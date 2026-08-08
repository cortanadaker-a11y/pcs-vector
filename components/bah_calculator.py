"""Homepage 2026 BAH calculator widget."""

from __future__ import annotations

import streamlit as st

from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import compare_bah, get_bah_effective_date, list_bah_installations

# Years of service does not change BAH (rank + dependents + location do).
# Shown so Soldiers can pick a realistic profile when reading the result.
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


def _money(n: int | None) -> str:
    if n is None:
        return "—"
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,}"


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
                <h3>2026 BAH Calculator</h3>
                <p class="pcs-bah-sub">
                    See your monthly Basic Allowance for Housing at your next post —
                    and the change from where you are now. Rates effective {safe_html(effective)}.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            pay_grade = st.selectbox(
                "Pay grade / rank",
                options=grades,
                index=grades.index("E-5") if "E-5" in grades else 0,
                format_func=lambda g: f"{g} — {PAY_GRADE_TO_RANK.get(g, g)}",
                key="bah_calc_grade",
            )
            yos = st.selectbox(
                "Years of service",
                options=YOS_OPTIONS,
                index=2,
                key="bah_calc_yos",
                help="BAH is not based on years of service — only rank, dependents, and location. "
                "YOS is for your context when planning the rest of your pay.",
            )
        with c2:
            deps = st.radio(
                "Dependents",
                options=["With dependents", "Without dependents"],
                horizontal=True,
                key="bah_calc_deps",
            )
            gaining = st.selectbox(
                "Gaining installation (new post)",
                options=installations,
                index=installations.index("Fort Bragg, NC")
                if "Fort Bragg, NC" in installations
                else 0,
                key="bah_calc_gaining",
            )

        show_compare = st.checkbox(
            "Compare to my current post (show monthly difference)",
            value=True,
            key="bah_calc_compare",
        )
        current = None
        if show_compare:
            current = st.selectbox(
                "Current installation (losing post)",
                options=[_NONE_CURRENT] + installations,
                key="bah_calc_current",
            )
            if current == _NONE_CURRENT:
                current = None

        with_dependents = deps.startswith("With")
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

        st.markdown(
            f"""
            <div class="pcs-bah-result">
                <div class="pcs-bah-result-label">Your BAH at {safe_html(gaining)}</div>
                <div class="pcs-bah-result-amount">{_money(int(gain_amt))}<span>/mo</span></div>
                <div class="pcs-bah-result-meta">
                    {safe_html(pay_grade)} ({safe_html(rank_label)}) · {safe_html(dep_label)} ·
                    {safe_html(yos)} · effective {safe_html(str(result["effective_date"]))}
                </div>
                <div class="pcs-bah-result-annual">
                    About {_money(int(gain_amt) * 12)} per year in housing allowance
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        curr = result.get("current")
        delta = result.get("monthly_delta_usd")
        if show_compare and curr and curr.get("found") and curr.get("monthly_usd") is not None and delta is not None:
            curr_amt = int(curr["monthly_usd"])
            annual = int(result.get("annual_delta_usd") or 0)
            if delta > 0:
                tone = "up"
                headline = f"You gain {_money(delta)}/mo at your new post"
                detail = (
                    f"From {curr['installation']} ({_money(curr_amt)}/mo) → "
                    f"{gaining} ({_money(int(gain_amt))}/mo). "
                    f"That's about {_money(annual)} more per year."
                )
            elif delta < 0:
                tone = "down"
                headline = f"You receive {_money(delta)}/mo less at your new post"
                detail = (
                    f"From {curr['installation']} ({_money(curr_amt)}/mo) → "
                    f"{gaining} ({_money(int(gain_amt))}/mo). "
                    f"Plan for about {_money(annual)} less per year."
                )
            else:
                tone = "flat"
                headline = "Same BAH at both posts"
                detail = (
                    f"{curr['installation']} and {gaining} both pay "
                    f"{_money(int(gain_amt))}/mo for your grade and dependency status."
                )

            st.markdown(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone}">
                    <div class="pcs-bah-delta-title">{safe_html(headline)}</div>
                    <div class="pcs-bah-delta-detail">{safe_html(detail)}</div>
                    <div class="pcs-bah-delta-grid">
                        <div>
                            <div class="pcs-bah-delta-k">Current</div>
                            <div class="pcs-bah-delta-v">{_money(curr_amt)}/mo</div>
                            <div class="pcs-bah-delta-s">{safe_html(str(curr["installation"]))}</div>
                        </div>
                        <div class="pcs-bah-delta-arrow">→</div>
                        <div>
                            <div class="pcs-bah-delta-k">New post</div>
                            <div class="pcs-bah-delta-v">{_money(int(gain_amt))}/mo</div>
                            <div class="pcs-bah-delta-s">{safe_html(gaining)}</div>
                        </div>
                        <div>
                            <div class="pcs-bah-delta-k">Monthly change</div>
                            <div class="pcs-bah-delta-v">{_money(int(delta))}</div>
                            <div class="pcs-bah-delta-s">{_money(annual)} / year</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif show_compare and current:
            st.info(
                f"No comparison rate for {pay_grade} at {current}. "
                "BAH at your gaining post is shown above."
            )

        st.caption(
            "BAH is set by pay grade, dependency status, and Military Housing Area — not years of service. "
            "Figures are 2026 planning rates for supported installations. "
            "Always verify with your finance office or the official DTMO BAH calculator before signing a lease."
        )

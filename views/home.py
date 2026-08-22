"""Home — calculator-first PCS finance hub + buy/rent referral hook."""

from __future__ import annotations

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import HERO, TRUST_SIGNALS
from components.html_utils import safe_html
from services.installation_data import SUPPORTED_INSTALLATIONS


def _render_hero() -> None:
    n = len(SUPPORTED_INSTALLATIONS)
    st.markdown(
        f"""
        <div class="pcs-hero">
            <div class="pcs-brand-kicker">{safe_html(HERO["kicker"])}</div>
            <div class="pcs-brand-title">PCS Vector</div>
            <h1 class="pcs-hero-headline">{safe_html(HERO["headline"])}</h1>
            <p class="pcs-hero-body">{safe_html(HERO["subheadline"])}</p>
            <div class="pcs-hero-stats">
                <span class="pcs-hero-stat"><strong>{n}</strong> posts</span>
                <span class="pcs-hero-stat"><strong>BAH · OHA · COLA</strong></span>
                <span class="pcs-hero-stat"><strong>Free</strong> calculator</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_trust_bar() -> None:
    badges = TRUST_SIGNALS["badges"][:3]
    badges_html = "".join(f'<span class="pcs-trust-badge">{safe_html(b)}</span>' for b in badges)
    st.markdown(
        f"""
        <div class="pcs-trust-banner">{safe_html(TRUST_SIGNALS["banner"])}</div>
        <div class="pcs-trust-row">{badges_html}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_value_strip() -> None:
    st.markdown(
        """
        <div class="pcs-flow" style="margin:0.75rem 0 0.25rem 0;">
            <div class="pcs-flow-step">
                <div class="pcs-flow-num">1</div>
                <div class="pcs-flow-title">Enter your profile</div>
                <div class="pcs-flow-desc">Grade, years of service, dependents, current &amp; gaining posts.</div>
            </div>
            <div class="pcs-flow-arrow">→</div>
            <div class="pcs-flow-step">
                <div class="pcs-flow-num">2</div>
                <div class="pcs-flow-title">See the money</div>
                <div class="pcs-flow-desc">BAH / OHA / COLA package, vs current post, utilities &amp; DLA planning.</div>
            </div>
            <div class="pcs-flow-arrow">→</div>
            <div class="pcs-flow-step">
                <div class="pcs-flow-num">3</div>
                <div class="pcs-flow-title">Find a place</div>
                <div class="pcs-flow-desc">Ready to buy or rent at the new post? We’ll connect you.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_referral_hook() -> None:
    """Buy/rent referral CTA — uses calculator destination when available."""
    snap = get_calculator_snapshot()
    dest = (snap or {}).get("gaining_installation") or "your gaining post"
    total = (snap or {}).get("total_monthly_usd")
    grade = (snap or {}).get("pay_grade")

    context_bits = []
    if grade:
        context_bits.append(str(grade))
    if total is not None:
        context_bits.append(f"~${int(total):,}/mo housing package")
    context_line = " · ".join(context_bits) if context_bits else "Run the calculator above first for a tighter match."

    st.markdown("### Next step: buy or rent at the new post")
    st.markdown(
        f"You’ve got the allowance picture for **{dest}**. "
        "When you’re ready to look at houses or rentals that fit that budget, "
        "we can connect you with a vetted partner who works military PCS moves."
    )
    st.caption(context_line)

    with st.container(border=True):
        st.markdown("**Get a housing referral**")
        st.caption("Free to request. We’ll follow up about buy vs rent options near your gaining station.")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", key="referral_name", placeholder="First and last")
        with c2:
            email = st.text_input("Email", key="referral_email", placeholder="you@email.com")
        interest = st.radio(
            "I’m interested in",
            options=["Renting", "Buying", "Not sure yet — show me options"],
            horizontal=True,
            key="referral_interest",
        )
        notes = st.text_area(
            "Anything we should know? (optional)",
            key="referral_notes",
            placeholder="Timeline, must-haves, school zones, pets…",
            height=80,
        )
        if st.button("Request referral →", type="primary", use_container_width=True, key="referral_submit"):
            if not (email or "").strip() or "@" not in (email or ""):
                st.error("Enter a valid email so we can reach you.")
            else:
                st.session_state.referral_lead = {
                    "name": (name or "").strip(),
                    "email": (email or "").strip(),
                    "interest": interest,
                    "notes": (notes or "").strip(),
                    "gaining_installation": dest,
                    "pay_grade": grade,
                    "housing_package_usd": total,
                    "calculator": snap,
                }
                st.success(
                    f"Got it — we’ll follow up about housing near **{dest}**. "
                    "Check your email (and spam) for next steps."
                )
                st.caption("Built For Soldiers; By Soldiers · No payment required for a referral request.")


def _render_faq() -> None:
    items = [
        {
            "q": "Is this free?",
            "a": "Yes. The calculator is free. Housing referrals are free to request.",
        },
        {
            "q": "What’s the difference between BAH, OHA, and COLA?",
            "a": (
                "**BAH** (Basic Allowance for Housing) is a flat monthly CONUS rate by zip, grade, and dependents. "
                "**OHA** (Overseas Housing Allowance) pays actual rent up to a ceiling + utilities overseas. "
                "**COLA** (Cost of Living Allowance) helps with higher day-to-day costs OCONUS and depends on "
                "grade, years of service, dependents, and location index."
            ),
        },
        {
            "q": "Are these official rates?",
            "a": (
                "They’re planning figures aligned to current DoD / DTMO tables. "
                "Always verify on your LES and with finance before you sign a lease or buy."
            ),
        },
        {
            "q": "What about utilities?",
            "a": (
                "After you pick a gaining post, the calculator shows off-post utility planning ranges "
                "(electric, heat/gas, water/trash, internet) by nearby areas when we have them on file."
            ),
        },
    ]
    st.markdown("### Questions")
    for item in items:
        with st.expander(item["q"], expanded=False):
            st.markdown(item["a"])


def render_home() -> None:
    """Calculator-centered hub for PCS finance + housing referral."""
    _render_hero()
    _render_trust_bar()
    _render_value_strip()

    st.markdown("<br>", unsafe_allow_html=True)
    render_bah_calculator()

    st.markdown("<br>", unsafe_allow_html=True)
    _render_referral_hook()

    st.markdown("<br>", unsafe_allow_html=True)
    _render_faq()

    st.markdown(
        """
        <div class="pcs-footer">
            PCS Vector — Built For Soldiers; By Soldiers<br>
            Always verify BAH, OHA, COLA, and entitlements with your finance office / DTMO.
        </div>
        """,
        unsafe_allow_html=True,
    )

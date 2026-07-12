"""Home / landing page for PCS Vector."""

import streamlit as st

from components.content import (
    DIY_VS_VECTOR,
    HERO,
    HOW_IT_WORKS_STEPS,
    OUTCOME_BENEFITS,
    PAIN_POINTS,
    PRICING_INCLUDES,
    REPORT_HIGHLIGHTS,
    REPORT_SECTIONS,
    TESTIMONIAL,
    TRUST_SIGNALS,
    WHY_25,
)
from components.faq import render_faq
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def _cta_block(price: str, *, cta_id: str = "bottom") -> None:
    """Reusable pricing + CTA column."""
    includes_html = "".join(f"<li>{item}</li>" for item in PRICING_INCLUDES)
    st.markdown(
        f"""
        <div class="pcs-pricing-box">
            <div class="pcs-price">{price}</div>
            <div class="pcs-price-sub">one-time · per report · no subscription</div>
            <div class="pcs-price-guarantee">Less than a tank of gas · More than a week of PCS stress</div>
            <ul class="pcs-price-includes">{includes_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Your PCS Plan", type="primary", use_container_width=True, key=f"cta_primary_{cta_id}"):
        navigate_to("input")
    if st.button("Already paid? Retrieve your report", use_container_width=True, key=f"cta_retrieve_{cta_id}"):
        navigate_to("retrieve")
    st.caption("Secure payment via Stripe · Independent tool · Not affiliated with DoD")


def _render_hero(price: str) -> None:
    st.markdown(
        f"""
        <div class="pcs-hero">
            <div class="pcs-brand-kicker">{HERO["kicker"]}</div>
            <div class="pcs-brand-title">PCS Vector</div>
            <h1 class="pcs-hero-headline">{HERO["headline"]}</h1>
            <p class="pcs-hero-body">{HERO["subheadline"]}</p>
            <p class="pcs-hero-outcomes">{HERO["outcome_line"]}</p>
            <div class="pcs-hero-stats">
                <span class="pcs-hero-stat"><strong>8</strong> decision sections</span>
                <span class="pcs-hero-stat"><strong>6–8</strong> min intake</span>
                <span class="pcs-hero-stat"><strong>{price}</strong> one-time</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_trust_signals() -> None:
    badges = "".join(f'<span class="pcs-trust-badge">{b}</span>' for b in TRUST_SIGNALS["badges"])
    st.markdown(
        f"""
        <div class="pcs-trust-banner">{TRUST_SIGNALS["banner"]}</div>
        <div class="pcs-trust-row">{badges}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_pain_section() -> None:
    st.markdown("### The PCS decisions you can't afford to wing")
    st.caption("Most families don't lack information — they lack a sequenced plan before deadlines hit.")
    cols = st.columns(3)
    for col, pain in zip(cols, PAIN_POINTS):
        with col:
            st.markdown(
                f"""
                <div class="pcs-pain-card">
                    <h4>{pain["title"]}</h4>
                    <p>{pain["desc"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_outcomes() -> None:
    st.markdown("### What you walk away with")
    st.caption("Outcomes that matter to NCOs, officers, and spouses — not feature bullets.")
    cols = st.columns(3)
    for col, benefit in zip(cols, OUTCOME_BENEFITS):
        with col:
            st.markdown(
                f"""
                <div class="pcs-outcome-card">
                    <div class="pcs-outcome-icon">{benefit["icon"]}</div>
                    <h3>{benefit["title"]}</h3>
                    <p>{benefit["desc"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_comparison() -> None:
    st.markdown("### DIY research vs. one decision-grade plan")
    rows = "".join(
        f"""
        <tr>
            <td class="pcs-cmp-topic">{row["label"]}</td>
            <td class="pcs-cmp-diy">{row["diy"]}</td>
            <td class="pcs-cmp-vector">{row["vector"]}</td>
        </tr>
        """
        for row in DIY_VS_VECTOR
    )
    st.markdown(
        f"""
        <div class="pcs-comparison-wrap">
            <table class="pcs-comparison">
                <thead>
                    <tr>
                        <th></th>
                        <th>On your own</th>
                        <th>PCS Vector</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_how_it_works(price: str) -> None:
    st.markdown("### How it works")
    st.caption("Four steps from stressed to structured — most families finish the form in one sitting.")
    steps_html = '<div class="pcs-flow">'
    for i, step in enumerate(HOW_IT_WORKS_STEPS):
        desc = step["desc"].replace("$25", price)
        steps_html += f"""
        <div class="pcs-flow-step">
            <div class="pcs-flow-num">{step["num"]}</div>
            <div class="pcs-flow-title">{step["title"]}</div>
            <div class="pcs-flow-desc">{desc}</div>
        </div>
        """
        if i < len(HOW_IT_WORKS_STEPS) - 1:
            steps_html += '<div class="pcs-flow-arrow">→</div>'
    steps_html += "</div>"
    st.markdown(steps_html, unsafe_allow_html=True)


def _render_report_sections() -> None:
    st.markdown("### Inside your 8-section strategic plan")
    st.caption("Every report follows this structure — personalized to your rank, family, and gaining installation.")

    cols = st.columns(2)
    for i, section in enumerate(REPORT_SECTIONS):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="pcs-section-item">
                    <span class="pcs-section-num">{section["num"]}</span>
                    <div>
                        <strong>{section["title"]}</strong><br>
                        <span class="pcs-section-desc-inline">{section["desc"]}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_example_highlights() -> None:
    st.markdown("### What the guidance sounds like")
    st.caption("Illustrative lines from real report outputs — yours is built from your answers.")

    for quote in REPORT_HIGHLIGHTS:
        st.markdown(f'<div class="pcs-highlight">{quote}</div>', unsafe_allow_html=True)

    t = TESTIMONIAL
    st.markdown(
        f"""
        <div class="pcs-testimonial">
            <p>"{t["quote"]}"</p>
            <span>— {t["attribution"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_why_25(price: str) -> None:
    points_html = "".join(
        f"""
        <div class="pcs-why-point">
            <strong>{p["title"]}</strong>
            <p>{p["desc"]}</p>
        </div>
        """
        for p in WHY_25["points"]
    )
    st.markdown(
        f"""
        <div class="pcs-why-box">
            <h3>{WHY_25["headline"].replace("$25", price)}</h3>
            <p class="pcs-why-intro">{WHY_25["intro"]}</p>
            {points_html}
            <p class="pcs-why-roi">{WHY_25["roi_line"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_mid_cta(price: str) -> None:
    st.markdown(
        f"""
        <div class="pcs-mid-cta">
            <div class="pcs-mid-cta-text">
                <strong>Ready to stop researching and start deciding?</strong>
                <span>Your personalized plan — {price}, minutes after checkout.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Get My PCS Plan →", type="primary", use_container_width=True, key="mid_cta"):
        navigate_to("input")


def render_home() -> None:
    """Render the conversion-focused landing page."""
    price = get_price_display()

    # 1. Hero + trust
    _render_hero(price)
    _render_trust_signals()
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Early CTA (above the fold follow-through)
    cta_top_l, cta_top_c, cta_top_r = st.columns([1, 2, 1])
    with cta_top_c:
        if st.button("Start Your PCS Plan →", type="primary", use_container_width=True, key="hero_cta"):
            navigate_to("input")
        st.caption(f"One-time {price} · 6–8 minute form · PDF emailed to you")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Pain → outcomes → comparison
    _render_pain_section()
    st.markdown("<br>", unsafe_allow_html=True)
    _render_outcomes()
    st.markdown("<br>", unsafe_allow_html=True)
    _render_comparison()
    st.markdown("<br>", unsafe_allow_html=True)

    # 4. How it works
    _render_how_it_works(price)
    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Mid-page CTA
    _render_mid_cta(price)
    st.markdown("<br>", unsafe_allow_html=True)

    # 6. Report structure + social proof
    _render_report_sections()
    st.markdown("<br>", unsafe_allow_html=True)
    _render_example_highlights()
    st.markdown("<br>", unsafe_allow_html=True)

    # 7. Why $25 + final pricing CTA
    _render_why_25(price)
    st.markdown("<br>", unsafe_allow_html=True)

    cta_l, cta_c, cta_r = st.columns([1, 2, 1])
    with cta_c:
        _cta_block(price, cta_id="bottom")

    st.markdown("<br>", unsafe_allow_html=True)
    render_faq("Questions before you start")

    st.markdown(
        """
        <div class="pcs-footer">
            PCS Vector is an independent planning tool built for Army families.<br>
            Always verify BAH rates and entitlements with your finance office.
        </div>
        """,
        unsafe_allow_html=True,
    )
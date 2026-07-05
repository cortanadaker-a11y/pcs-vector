"""Home / landing page for PCS Vector."""

import streamlit as st

from components.content import (
    HOW_IT_WORKS_STEPS,
    REPORT_HIGHLIGHTS,
    REPORT_SECTIONS,
    VALUE_PROPS,
)
from components.faq import render_faq
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def _render_how_it_works(price: str) -> None:
    st.markdown("### How it works")
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


def _render_trust_signals() -> None:
    st.markdown(
        """
        <div class="pcs-trust-row">
            <span class="pcs-trust-badge">Built by a serving Army officer</span>
            <span class="pcs-trust-badge">Used by military families</span>
            <span class="pcs-trust-badge">Secure Stripe checkout</span>
            <span class="pcs-trust-badge">Instant PDF download</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_report_sections() -> None:
    st.markdown("### Your 8-section strategic plan")
    st.caption("Every report follows this structure — personalized to your family and duty station.")

    cols = st.columns(2)
    for i, section in enumerate(REPORT_SECTIONS):
        target = cols[i % 2]
        with target:
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
    st.markdown("### Example insights from real reports")
    st.caption("Illustrative highlights — your plan is built from your family's answers.")

    for quote in REPORT_HIGHLIGHTS:
        st.markdown(f'<div class="pcs-highlight">{quote}</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="pcs-testimonial">
            <p>“We had orders to Bragg and no idea where to start with schools and BAH.
            This gave us a clear plan my husband and I could actually follow — worth every penny.”</p>
            <span>— Army spouse, E-6 family · Fort Liberty PCS</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    """Render the conversion-focused landing page."""
    price = get_price_display()

    st.markdown(
        f"""
        <div class="pcs-hero">
            <div class="pcs-badge">CONUS Army PCS Planning</div>
            <h1>Your PCS game plan — ready before the boxes are packed</h1>
            <p>
                Stop juggling Facebook threads and guesswork. PCS Vector turns your family's
                situation into a clear, personalized strategic plan — housing, schools, spouse
                career, finances, and a 30-day action checklist — for <strong>{price}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_trust_signals()
    st.markdown("<br>", unsafe_allow_html=True)

    _render_how_it_works(price)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Why families choose PCS Vector")
    v1, v2, v3 = st.columns(3)
    for col, prop in zip([v1, v2, v3], VALUE_PROPS):
        with col:
            st.markdown(
                f"""
                <div class="pcs-card">
                    <h3>{prop["title"]}</h3>
                    <p>{prop["desc"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    _render_report_sections()

    st.markdown("<br>", unsafe_allow_html=True)
    _render_example_highlights()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### What makes this worth $25?")
        st.markdown(
            f"""
            A PCS affects your **housing budget, spouse's career, kids' schools, and timeline**
            for the next 2–3 years. One wrong lease or missed school deadline can cost far more
            than {price}.

            PCS Vector gives you a **single, spouse-readable plan** you can act on today —
            not another generic checklist.
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    cta_left, cta_center, cta_right = st.columns([1, 2, 1])
    with cta_center:
        st.markdown(
            f"""
            <div class="pcs-pricing-box">
                <div class="pcs-price">{price}</div>
                <div class="pcs-price-sub">one-time · per report · no subscription</div>
                <ul class="pcs-price-includes">
                    <li>Full 8-section personalized plan</li>
                    <li>Fort Liberty, Fort Cavazos & Fort Drum local depth</li>
                    <li>Professional PDF download</li>
                    <li>Generated in minutes after payment</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Start Your PCS Plan", type="primary", use_container_width=True):
            navigate_to("input")

        st.caption("Secure payment via Stripe · Not affiliated with the DoD")

    st.markdown("<br>", unsafe_allow_html=True)
    render_faq()

    st.markdown(
        """
        <div class="pcs-footer">
            PCS Vector is an independent planning tool for Army families.<br>
            Always verify BAH rates and entitlements with your finance office.
        </div>
        """,
        unsafe_allow_html=True,
    )
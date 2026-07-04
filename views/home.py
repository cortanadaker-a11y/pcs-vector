"""Home / landing page for PCS Vector."""

import streamlit as st

from services.stripe_payment import get_price_display


def render_home() -> None:
    """Render the welcome landing page."""
    price = get_price_display()

    st.markdown(
        """
        <div class="pcs-hero">
            <div class="pcs-badge">CONUS Army PCS Planning</div>
            <h1>Navigate your next move with confidence</h1>
            <p>
                PCS Vector creates a personalized strategic plan tailored to your
                family's needs — housing, schools, timelines, and local insights
                for your new duty station.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### How it works")
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        st.markdown("**1. Tell us about your move**  \n6–8 minute form")
    with step2:
        st.markdown(f"**2. Secure checkout**  \n{price} via Stripe")
    with step3:
        st.markdown("**3. AI-built plan**  \n8-section strategic report")
    with step4:
        st.markdown("**4. Download PDF**  \nShare with your spouse")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="pcs-card">
                <h3>Personalized</h3>
                <p>
                    Every report is built around your family's unique situation —
                    kids, pets, career, budget, and timeline.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="pcs-card">
                <h3>Local expertise</h3>
                <p>
                    Deep guidance for Fort Liberty (Ft Bragg) and Fort Drum —
                    neighborhoods, schools, BAH, and spouse employment.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="pcs-card">
                <h3>Actionable plan</h3>
                <p>
                    Housing tradeoffs, DITY guidance, a 30-day action plan,
                    and prioritized next steps from orders to move-in day.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### What's included in your report")
        inc1, inc2 = st.columns(2)
        with inc1:
            st.markdown(
                "- Executive summary & recommended strategy  \n"
                "- Spouse career & childcare plan  \n"
                "- Housing strategy & BAH comparison  \n"
                "- Financial opportunities & DITY/PPM notes"
            )
        with inc2:
            st.markdown(
                "- First 30 days action plan  \n"
                "- Schools, pets & logistics  \n"
                "- Timeline & key decisions  \n"
                "- Prioritized next steps + PDF export"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    cta_left, cta_center, cta_right = st.columns([1, 2, 1])

    with cta_center:
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <div class="pcs-price">{price} <span>per report · one-time payment</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Start New Report", type="primary", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()

        st.caption("Secure payment via Stripe. Not affiliated with the U.S. Department of Defense.")

    st.markdown(
        """
        <div class="pcs-footer">
            PCS Vector is an independent planning tool for Army families.
        </div>
        """,
        unsafe_allow_html=True,
    )
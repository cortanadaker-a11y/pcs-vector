"""Sidebar navigation for PCS Vector."""

import streamlit as st

from components.progress import STEPS

PAGE_LABELS = {
    "home": "Home",
    "input": "Input Form",
    "report": "Report",
}


def render_sidebar() -> str:
    """Render sidebar navigation and return the selected page."""
    with st.sidebar:
        st.markdown("## PCS Vector")
        st.caption("Personalized PCS strategic plans for Army families.")
        st.caption("Built by a serving Army officer · $25/report")

        st.divider()

        page = st.radio(
            "Navigate",
            options=["home", "input", "report"],
            format_func=lambda p: PAGE_LABELS[p],
            key="nav_page",
            label_visibility="collapsed",
        )

        st.divider()

        with st.expander("About this service", expanded=False):
            st.markdown(
                """
                **PCS Vector** helps CONUS Army families plan their move
                with confidence.

                - Personalized 8-section strategic report
                - Optimized for Ft Bragg & Ft Drum
                - $25 per report (Stripe Checkout)
                - Professional PDF download
                """
            )

        st.divider()
        st.caption("CONUS Army moves only")

    return page
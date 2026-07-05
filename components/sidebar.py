"""Sidebar navigation for PCS Vector."""

import streamlit as st

from components.progress import STEPS

PAGE_LABELS = {
    "home": "Home",
    "input": "Input Form",
    "report": "Report",
}


def sync_nav_before_sidebar() -> None:
    """Align sidebar widget state before it renders (must run before render_sidebar)."""
    if "nav_page" not in st.session_state:
        st.session_state.nav_page = st.session_state.page
    if st.session_state.pop("_sync_nav_from_page", False):
        st.session_state.nav_page = st.session_state.page


def set_page(page: str) -> None:
    """Set active page before sidebar renders (e.g. payment redirect)."""
    st.session_state.page = page
    st.session_state.nav_page = page


def navigate_to(page: str) -> None:
    """Navigate from a button after sidebar has already rendered."""
    st.session_state.page = page
    st.session_state._sync_nav_from_page = True
    st.rerun()


def render_sidebar() -> str:
    """Render sidebar navigation and return the selected page."""
    with st.sidebar:
        st.markdown("## PCS Vector")
        st.caption("Personalized PCS strategic plans for Army families.")
        st.caption("Built by a serving Army officer · $25/report")

        st.divider()

        st.radio(
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
                - Optimized for Fort Bragg & Fort Hood
                - $25 per report (Stripe Checkout)
                - Professional PDF download
                """
            )

        st.divider()
        st.caption("CONUS Army moves only")

    return st.session_state.nav_page
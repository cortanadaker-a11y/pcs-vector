"""Sidebar navigation for PCS Vector."""

import streamlit as st

from components.progress import STEPS
from components.scroll import request_scroll_to_top

PAGE_LABELS = {
    "home": "Home",
    "input": "Input Form",
    "report": "Report",
    "retrieve": "Retrieve Report",
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
    if page == "input":
        st.session_state.form_step = 0
    request_scroll_to_top()
    st.rerun()


def render_sidebar() -> str:
    """Render sidebar navigation and return the selected page."""
    with st.sidebar:
        st.markdown("## PCS Vector")
        st.caption("Your PCS game plan — ready before the boxes are packed.")
        st.caption("Built by Soldiers for Soldiers and their families")

        st.divider()

        st.radio(
            "Navigate",
            options=["home", "input", "report", "retrieve"],
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
                - Optimized for Fort Bragg, Fort Hood, Fort Drum & Fort Gordon
                - $25 per report (Stripe Checkout)
                - PDF emailed automatically after payment
                - Retrieve paid reports with your order reference
                """
            )

        st.divider()
        st.caption("CONUS Army moves only")

    return st.session_state.nav_page
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
        st.caption("Decision-grade PCS planning for Army families.")
        st.caption("Built For Soldiers; By Soldiers")

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
                **PCS Vector** turns your family's PCS inputs into a
                personalized strategic plan — housing, schools, spouse career,
                finances, and sequenced next steps.

                - 8-section decision-grade report
                - 22 major CONUS Army installations
                - $25 one-time (Stripe Checkout)
                - PDF emailed automatically
                - Retrieve anytime with your order reference
                """
            )

        st.divider()
        st.caption("CONUS Army moves only")

    return st.session_state.nav_page
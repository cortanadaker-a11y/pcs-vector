"""Sidebar navigation for PCS Vector."""

import streamlit as st

from components.scroll import request_scroll_to_top

PAGE_LABELS = {
    "home": "Home",
    "input": "Build your plan",
    "report": "Your report",
    "retrieve": "Retrieve report",
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
        st.caption("Personalized PCS plans for Army families.")
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

        with st.expander("About", expanded=False):
            st.markdown(
                """
                **PCS Vector** builds a decision-grade PCS plan for your family —
                housing, schools, spouse career, cash flow, and first 30 days.

                - 8-section personalized report
                - Major CONUS Army installations
                - One-time payment · PDF emailed
                - Retrieve anytime with your order reference
                """
            )

        st.caption("CONUS Army moves only")

    return st.session_state.nav_page

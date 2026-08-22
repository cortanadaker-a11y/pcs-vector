"""Sidebar for PCS Vector (single-page calculator)."""

from __future__ import annotations

import streamlit as st

from services.installation_data import SUPPORTED_INSTALLATIONS


def sync_nav_before_sidebar() -> None:
    st.session_state.page = "home"
    st.session_state.nav_page = "home"


def set_page(page: str) -> None:
    st.session_state.page = "home"
    st.session_state.nav_page = "home"


def navigate_to(page: str) -> None:
    st.session_state.page = "home"
    st.session_state.nav_page = "home"
    st.rerun()


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## PCS Vector")
        st.caption("Built For Soldiers; By Soldiers")
        st.divider()
        st.markdown(
            f"Free BAH / OHA / COLA calculator · **{len(SUPPORTED_INSTALLATIONS)}** posts · "
            "utilities · DLA · buy/rent referral"
        )
        st.caption("Always verify with finance / DTMO.")
    return "home"

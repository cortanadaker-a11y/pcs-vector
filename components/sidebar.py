"""Sidebar for PCS Vector (single-page calculator experience)."""

from __future__ import annotations

import streamlit as st

from services.installation_data import SUPPORTED_INSTALLATIONS


def sync_nav_before_sidebar() -> None:
    """No-op kept for compatibility with older call sites."""
    st.session_state.page = "home"
    st.session_state.nav_page = "home"


def set_page(page: str) -> None:
    """Force home — multi-page nav is retired."""
    st.session_state.page = "home"
    st.session_state.nav_page = "home"


def navigate_to(page: str) -> None:
    """Stay on home (legacy callers safe)."""
    st.session_state.page = "home"
    st.session_state.nav_page = "home"
    st.rerun()


def render_sidebar() -> str:
    """Brand + about only — no page navigation."""
    with st.sidebar:
        st.markdown("## PCS Vector")
        st.caption("PCS finance clarity for Army families.")
        st.caption("Built For Soldiers; By Soldiers")

        st.divider()

        st.markdown(
            f"""
            Compare **BAH / OHA / COLA** across **{len(SUPPORTED_INSTALLATIONS)}** posts,
            see local **utility** ranges, and get help finding a place to **buy or rent**
            at your gaining station.
            """
        )

        with st.expander("About", expanded=False):
            st.markdown(
                """
                **PCS Vector** is a one-stop shop for Soldiers getting ready to PCS:

                - Compare current vs new post housing packages
                - CONUS **BAH** · Foreign **OHA + COLA** · HI/PR **BAH + COLA**
                - Off-post utility planning ranges by area
                - **Dislocation Allowance (DLA)** planning figures
                - Referral help when you're ready to buy or rent

                Always verify entitlements with finance / DTMO before you spend.
                """
            )

        st.caption("Army PCS · CONUS & OCONUS")

    return "home"

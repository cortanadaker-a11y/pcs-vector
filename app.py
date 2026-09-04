"""
PCS Vector — PCS finance clarity for Army Soldiers.

Single-page app centered on the housing allowance calculator:
compare current vs gaining post (BAH / OHA / COLA), see local utility ranges,
and get connected for buy/rent at the new location.
"""

import logging

import streamlit as st

from components.scroll import (
    render_boot_at_top,
    render_dropdown_scroll_fix,
    render_page_top_anchor,
    render_scroll_to_top,
)
from components.sidebar import render_sidebar
from components.styles import apply_styles
from views.home import render_home

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pcs_vector")

st.set_page_config(
    page_title="PCS Vector — Free Army PCS BAH Calculator (2026)",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": (
            "PCS Vector is a free Army PCS finance calculator for BAH, OHA, COLA, "
            "rent, utilities, and gas. Built For Soldiers; By Soldiers. "
            "Not affiliated with the U.S. Department of Defense."
        ),
    },
)

apply_styles()
# Main-document scroll (st.html) — do NOT use bottom components.html iframes;
# those are what yank the phone viewport halfway down the page.
render_boot_at_top()
render_dropdown_scroll_fix()

st.session_state.page = "home"
render_sidebar()
render_page_top_anchor()
render_home()
render_scroll_to_top()
# Final pass after content/widgets mount (still st.html, no iframe).
render_boot_at_top()

"""
PCS Vector — PCS finance clarity for Army Soldiers.

Single-page app centered on the housing allowance calculator:
compare current vs gaining post (BAH / OHA / COLA), see local utility ranges,
and get connected for buy/rent at the new location.
"""

import logging

import streamlit as st

from components.scroll import (
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
    page_title="PCS Vector — PCS Finance Calculator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": (
            "PCS Vector helps Soldiers who are about to PCS understand housing money "
            "and local costs. Built For Soldiers; By Soldiers."
        ),
    },
)

apply_styles()
render_dropdown_scroll_fix()

st.session_state.page = "home"
render_sidebar()
render_page_top_anchor()
render_home()
render_scroll_to_top()

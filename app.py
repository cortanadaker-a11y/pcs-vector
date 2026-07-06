"""
PCS Vector — Personalized PCS strategic plans for Army families.

CONUS Army moves only. Optimized for Fort Bragg, Fort Hood, Fort Drum, and Fort Gordon.

Payment flow:
  Home → Input Form → Stripe Checkout ($25) → Report (Grok + PDF)

The report is NEVER generated before payment_verified is True.
handle_payment_callback() runs on every load to process Stripe redirect URLs.
"""

import logging
import streamlit as st

from components.form_state import init_form_state
from components.payment_handler import handle_payment_callback, init_payment_state
from components.progress import render_progress_indicator
from components.sidebar import render_sidebar, sync_nav_before_sidebar
from components.startup_checks import render_config_warnings
from components.scroll import render_dropdown_scroll_fix, render_page_top_anchor, render_scroll_to_top, request_scroll_to_top
from components.styles import apply_styles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pcs_vector")
from views.home import render_home
from views.input_form import render_input_form
from views.order_lookup import render_order_lookup
from views.report import render_report

st.set_page_config(
    page_title="PCS Vector",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "PCS Vector generates personalized PCS strategic plans for "
            "CONUS Army families at $25 per report."
        ),
    },
)

apply_styles()
render_dropdown_scroll_fix()

if "page" not in st.session_state:
    st.session_state.page = "home"

init_form_state()
init_payment_state()

# Process Stripe redirect (?payment=success|cancelled) before rendering any page.
handle_payment_callback()

if "report_markdown" not in st.session_state:
    st.session_state.report_markdown = None

if "report_error" not in st.session_state:
    st.session_state.report_error = None

sync_nav_before_sidebar()
sidebar_page = render_sidebar()
render_config_warnings()

if sidebar_page != st.session_state.page:
    st.session_state.page = sidebar_page
    request_scroll_to_top()

current_page = st.session_state.page

render_progress_indicator(current_page)
render_page_top_anchor()

if current_page == "home":
    render_home()
elif current_page == "input":
    render_input_form()
elif current_page == "report":
    render_report()
elif current_page == "retrieve":
    render_order_lookup()

# Scroll after content renders so the DOM is ready.
render_scroll_to_top()
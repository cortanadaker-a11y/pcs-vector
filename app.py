"""
PCS Vector — Personalized PCS strategic plans for Army families.

CONUS Army moves only. Optimized for Ft Bragg and Ft Drum.

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
from components.sidebar import render_sidebar
from components.startup_checks import render_config_warnings
from components.styles import apply_styles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pcs_vector")
from views.home import render_home
from views.input_form import render_input_form
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

sidebar_page = render_sidebar()
render_config_warnings()

if sidebar_page != st.session_state.page:
    st.session_state.page = sidebar_page

current_page = st.session_state.page

render_progress_indicator(current_page)

if current_page == "home":
    render_home()
elif current_page == "input":
    render_input_form()
elif current_page == "report":
    render_report()
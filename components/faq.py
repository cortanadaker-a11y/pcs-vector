"""FAQ section for PCS Vector."""

import streamlit as st

from components.content import FAQ_ITEMS
from components.html_utils import safe_markdown


def render_faq(title: str = "Frequently asked questions") -> None:
    """Render expandable FAQ items."""
    st.markdown(f"### {title}")
    for item in FAQ_ITEMS:
        with st.expander(safe_markdown(item["q"]), expanded=False):
            st.markdown(safe_markdown(item["a"]))
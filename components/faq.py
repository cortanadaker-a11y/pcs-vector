"""FAQ section for PCS Vector."""

import streamlit as st

from components.content import FAQ_ITEMS


def render_faq(title: str = "Frequently asked questions") -> None:
    """Render expandable FAQ items."""
    st.markdown(f"### {title}")
    for item in FAQ_ITEMS:
        with st.expander(item["q"], expanded=False):
            st.markdown(item["a"])
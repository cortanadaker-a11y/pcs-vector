"""Premium loading UI while Grok generates a report."""

from __future__ import annotations

import streamlit as st

from components.content import REPORT_GENERATION_STEPS, REPORT_SECTIONS
from components.form_state import resolved_gaining_installation
from components.html_utils import safe_html


def _destination_label(form_data: dict | None) -> str:
    if not form_data:
        return "your gaining installation"
    gaining = resolved_gaining_installation(form_data)
    return gaining or "your gaining installation"


def render_generation_loading_panel(form_data: dict | None = None) -> None:
    """Show a premium static progress panel during report generation."""
    destination = _destination_label(form_data)
    steps_html = "".join(
        f'<div class="pcs-gen-step">'
        f'<span class="pcs-gen-step-dot"></span>'
        f'<span>{safe_html(step["label"])}</span>'
        f"</div>"
        for step in REPORT_GENERATION_STEPS
    )
    sections_html = "".join(
        f'<span class="pcs-gen-section-chip">{s["num"]}. {safe_html(s["title"].split("&")[0].strip())}</span>'
        for s in REPORT_SECTIONS
    )
    st.markdown(
        f"""
        <div class="pcs-gen-panel">
            <div class="pcs-gen-panel-head">
                <div class="pcs-gen-panel-title">Building your PCS strategic plan</div>
                <div class="pcs-gen-panel-sub">Personalized for <strong>{safe_html(destination)}</strong></div>
            </div>
            <div class="pcs-gen-progress-track"><div class="pcs-gen-progress-bar"></div></div>
            <div class="pcs-gen-steps">{steps_html}</div>
            <div class="pcs-gen-sections-label">8 sections in your report</div>
            <div class="pcs-gen-sections">{sections_html}</div>
            <div class="pcs-gen-foot">Usually ready in under 60 seconds · PDF emailed automatically</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
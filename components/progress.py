"""Multi-step progress indicator for the PCS report flow."""

import streamlit as st

STEPS = [
    {"id": "home", "label": "Welcome", "number": 1},
    {"id": "input", "label": "Your Details", "number": 2},
    {"id": "report", "label": "Your Report", "number": 3},
]

STEP_ORDER = [step["id"] for step in STEPS]


def get_step_index(page: str) -> int:
    """Return the zero-based index of a page in the flow."""
    try:
        return STEP_ORDER.index(page)
    except ValueError:
        return 0


def render_progress_indicator(current_page: str) -> None:
    """Render a horizontal step indicator for the report workflow."""
    if current_page == "home":
        return

    current_index = get_step_index(current_page)

    steps_html = '<div class="pcs-steps">'
    for i, step in enumerate(STEPS):
        if i > 0:
            connector_class = "completed" if i <= current_index else ""
            steps_html += f'<div class="pcs-step-connector {connector_class}"></div>'

        if i < current_index:
            state_class = "completed"
            circle_content = "✓"
        elif i == current_index:
            state_class = "active"
            circle_content = str(step["number"])
        else:
            state_class = ""
            circle_content = str(step["number"])

        steps_html += f"""
        <div class="pcs-step {state_class}">
            <div class="pcs-step-circle">{circle_content}</div>
            <div class="pcs-step-label">{step["label"]}</div>
        </div>
        """

    steps_html += "</div>"
    st.markdown(steps_html, unsafe_allow_html=True)
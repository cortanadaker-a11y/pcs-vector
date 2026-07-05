"""Session state helpers for PCS input form data."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.form_options import PRIORITY_CHOICES, PRIORITY_LABELS

MULTISELECT_FORM_KEYS = (
    "child_age_ranges",
    "pet_types",
    "housing_must_haves_selected",
    "concern_flags",
)

FORM_DEFAULTS: dict[str, Any] = {
    "rank_pay_grade": "E-5",
    "rank_title": "",
    "current_installation_preset": "Fort Hood, TX",
    "current_installation_other": "",
    "gaining_installation": "Fort Bragg, NC",
    "gaining_installation_other": "",
    "move_window": "3–6 months",
    "move_flexibility": "Somewhat flexible (±2 weeks)",
    "spouse_career_field": "Not currently working — seeking employment",
    "spouse_career_other": "",
    "num_children": 0,
    "child_age_ranges": [],
    "has_pets": "No pets",
    "pet_types": [],
    "pet_details": "",
    "housing_preference": "Open to either — best overall fit",
    "budget_mode": "Optimize for best value",
    "budget_preset": "$1,600 – $2,000/mo",
    "max_monthly_budget": 1800,
    "housing_must_haves_selected": [],
    "housing_must_haves_other": "",
    "primary_priority": "Minimizing total costs",
    "secondary_priority": "Fastest possible resettlement",
    "other_priorities": "",
    "num_vehicles": "1",
    "dity_interest": "Maybe — run the numbers for me",
    "concern_flags": [],
    "specific_concerns": "",
    "form_submitted": False,
}


def init_form_state() -> None:
    """Initialize form fields in session state if missing."""
    if "form_data" not in st.session_state:
        st.session_state.form_data = FORM_DEFAULTS.copy()


def get_form_value(key: str) -> Any:
    """Read a single form value from session state."""
    return st.session_state.form_data.get(key, FORM_DEFAULTS.get(key))


def set_form_value(key: str, value: Any) -> None:
    """Write a single form value to session state."""
    st.session_state.form_data[key] = value


def _multiselect_widget_key(form_key: str) -> str:
    return f"ms_{form_key}"


def clear_multiselect_widget_state() -> None:
    """Reset widget-bound multiselect keys (e.g. after restoring saved form data)."""
    for key in MULTISELECT_FORM_KEYS:
        st.session_state.pop(_multiselect_widget_key(key), None)


def render_multiselect(
    label: str,
    options: list[str],
    form_key: str,
    *,
    help: str | None = None,
) -> list[str]:
    """Render a multiselect bound to a stable widget key to avoid dropped selections."""
    widget_key = _multiselect_widget_key(form_key)
    if widget_key not in st.session_state:
        stored = get_form_value(form_key) or []
        st.session_state[widget_key] = [item for item in stored if item in options]

    kwargs: dict[str, Any] = {"options": options, "key": widget_key}
    if help:
        kwargs["help"] = help
    selected = st.multiselect(label, **kwargs)
    set_form_value(form_key, selected)
    return selected


def reset_multiselect(form_key: str) -> None:
    """Clear a multiselect field and its widget state."""
    st.session_state[_multiselect_widget_key(form_key)] = []
    set_form_value(form_key, [])


def apply_restored_form_data(form_data: dict[str, Any]) -> None:
    """Apply form data recovered from Stripe and refresh multiselect widget state."""
    st.session_state.form_data = form_data
    clear_multiselect_widget_state()


def collect_form_from_widgets() -> dict[str, Any]:
    """Return the current widget-backed form payload."""
    return st.session_state.form_data.copy()


def resolved_current_installation(data: dict[str, Any]) -> str:
    preset = data.get("current_installation_preset", "")
    if preset == "Other installation":
        return data.get("current_installation_other", "").strip()
    return preset


def resolved_spouse_career(data: dict[str, Any]) -> str:
    field = data.get("spouse_career_field", "")
    if field == "Other field":
        return data.get("spouse_career_other", "").strip() or "Other (not specified)"
    return field


def resolved_housing_must_haves(data: dict[str, Any]) -> str:
    parts = list(data.get("housing_must_haves_selected") or [])
    other = data.get("housing_must_haves_other", "").strip()
    if other:
        parts.append(other)
    return ", ".join(parts) if parts else "None specified"


def resolved_concerns(data: dict[str, Any]) -> str:
    flags = data.get("concern_flags") or []
    extra = data.get("specific_concerns", "").strip()
    parts = list(flags)
    if extra:
        parts.append(extra)
    return "; ".join(parts) if parts else "None noted"


def priority_summary(data: dict[str, Any]) -> dict[str, str]:
    """Return primary/secondary priority labels for display and prompts."""
    return {
        "Primary priority": data.get("primary_priority", ""),
        "Secondary priority": data.get("secondary_priority", ""),
    }


def priority_rank_scores(data: dict[str, Any]) -> dict[str, int]:
    """Map legacy priority keys to scores for any downstream use."""
    primary = data.get("primary_priority", "")
    secondary = data.get("secondary_priority", "")
    scores = {label: 2 for label in PRIORITY_CHOICES}
    for label in PRIORITY_CHOICES:
        if label == primary:
            scores[label] = 5
        elif label == secondary:
            scores[label] = 4
    key_map = {
        "Spouse career / quick employment": "spouse_career",
        "Minimizing total costs": "minimize_costs",
        "Fastest possible resettlement": "fast_resettlement",
        "School quality": "school_quality",
    }
    return {
        PRIORITY_LABELS[key]: scores[label]
        for label, key in key_map.items()
    }


def validate_form(data: dict[str, Any]) -> list[str]:
    """Return a list of validation error messages."""
    errors: list[str] = []

    if not data.get("rank_pay_grade"):
        errors.append("Select a pay grade.")

    if data.get("rank_pay_grade") == "Other" and not data.get("rank_title", "").strip():
        errors.append("Enter your rank or title when pay grade is Other.")

    if not resolved_current_installation(data):
        errors.append("Select or enter your current Army installation.")

    gaining = data.get("gaining_installation", "")
    if gaining == "Other CONUS installation" and not data.get(
        "gaining_installation_other", ""
    ).strip():
        errors.append("Enter your gaining installation when Other is selected.")

    if data.get("spouse_career_field") == "Other field" and not data.get(
        "spouse_career_other", ""
    ).strip():
        errors.append("Describe your spouse's field when Other is selected.")

    if data.get("has_pets") == "Yes — we have pets" and not (
        data.get("pet_types") or data.get("pet_details", "").strip()
    ):
        errors.append("Select pet type(s) or add brief pet details.")

    if data.get("budget_mode") == "Set a monthly budget cap":
        if data.get("budget_preset") == "Custom amount":
            budget = data.get("max_monthly_budget", 0)
            if not budget or budget <= 0:
                errors.append("Enter a monthly housing budget greater than $0.")

    primary = data.get("primary_priority", "")
    secondary = data.get("secondary_priority", "")
    if primary and secondary and primary == secondary:
        errors.append("Choose different primary and secondary priorities.")

    num_children = data.get("num_children", 0)
    if num_children > 0 and not data.get("child_age_ranges"):
        errors.append("Select at least one child age range.")

    return errors


def resolved_gaining_installation(data: dict[str, Any]) -> str:
    """Return the display name for the gaining installation."""
    if data.get("gaining_installation") == "Other CONUS installation":
        return data.get("gaining_installation_other", "").strip()
    return data.get("gaining_installation", "")


def budget_display(data: dict[str, Any]) -> str:
    if data.get("budget_mode") == "Optimize for best value":
        return "Optimize for best value"
    preset = data.get("budget_preset", "")
    if preset == "Custom amount":
        return f"${int(data.get('max_monthly_budget', 0)):,}/mo max"
    return preset
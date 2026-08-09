"""Session state helpers for PCS input form data."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.form_options import PRIORITY_CHOICES, PRIORITY_LABELS, rank_for_pay_grade

MULTISELECT_FORM_KEYS = (
    "child_age_ranges",
    "pet_types",
    "housing_must_haves_selected",
    "concern_flags",
)

NUMBER_WIDGET_KEYS = (
    "num_children",
    "num_dependents",
    "years_of_service",
    "max_monthly_budget",
    "spouse_monthly_income_usd",
)

FORM_DEFAULTS: dict[str, Any] = {
    "first_name": "",
    "last_name": "",
    "email": "",
    "rank_pay_grade": "E-5",
    "rank_title": "Sergeant",
    "years_of_service": 4,
    "current_installation_preset": "Fort Hood, TX",
    "current_installation_other": "",
    "gaining_installation": "Fort Bragg, NC",
    "gaining_installation_other": "",
    "move_window": "1–3 months",
    "move_flexibility": "Fixed — must align with reporting date",
    "family_status": "Married / with dependents",
    "spouse_career_field": "Not currently working — seeking employment",
    "spouse_career_other": "",
    "spouse_monthly_income_usd": 0,  # 0 = not provided (optional)
    "num_dependents": 1,
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


def sync_rank_from_pay_grade(data: dict[str, Any] | None = None) -> None:
    """Keep rank_title aligned with pay grade (no manual entry for standard grades)."""
    if data is None:
        data = st.session_state.get("form_data", {})
    pay_grade = data.get("rank_pay_grade", "")
    if pay_grade and pay_grade != "Other":
        data["rank_title"] = rank_for_pay_grade(pay_grade)


def init_form_state() -> None:
    """Initialize form fields in session state if missing."""
    if "form_data" not in st.session_state:
        st.session_state.form_data = FORM_DEFAULTS.copy()
    else:
        # Backfill keys added in newer releases (e.g. email) for existing sessions.
        for key, default in FORM_DEFAULTS.items():
            st.session_state.form_data.setdefault(key, default)
    sync_rank_from_pay_grade(st.session_state.form_data)


def get_form_value(key: str) -> Any:
    """Read a single form value from session state."""
    return st.session_state.form_data.get(key, FORM_DEFAULTS.get(key))


def set_form_value(key: str, value: Any) -> None:
    """Write a single form value to session state."""
    st.session_state.form_data[key] = value


def _multiselect_widget_key(form_key: str) -> str:
    return f"ms_{form_key}"


def _number_widget_key(form_key: str) -> str:
    return f"num_{form_key}"


def clear_multiselect_widget_state() -> None:
    """Reset widget-bound multiselect keys (e.g. after restoring saved form data)."""
    for key in MULTISELECT_FORM_KEYS:
        st.session_state.pop(_multiselect_widget_key(key), None)


def clear_number_widget_state() -> None:
    """Reset widget-bound number inputs."""
    for key in NUMBER_WIDGET_KEYS:
        st.session_state.pop(_number_widget_key(key), None)


def render_number_input(
    label: str,
    form_key: str,
    *,
    min_value: int,
    max_value: int,
    step: int = 1,
    help_text: str | None = None,
) -> int:
    """Render a number input bound to a stable widget key."""
    widget_key = _number_widget_key(form_key)
    if widget_key not in st.session_state:
        st.session_state[widget_key] = int(get_form_value(form_key) or 0)

    value = st.number_input(
        label,
        min_value=min_value,
        max_value=max_value,
        step=step,
        key=widget_key,
        help=help_text,
    )
    int_value = int(value)
    set_form_value(form_key, int_value)
    return int_value


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
    merged = FORM_DEFAULTS.copy()
    merged.update(form_data)
    st.session_state.form_data = merged
    clear_multiselect_widget_state()
    clear_number_widget_state()


# Widget keys used by the multi-step plan form (must stay in sync with input_form.py).
_FORM_WIDGET_KEYS = (
    "form_rank_pay_grade",
    "form_rank_title_other",
    "form_family_status",
    "form_email_input",
    "form_current_installation",
    "form_gaining_installation",
)


def clear_form_widget_state() -> None:
    """Drop form widget keys so they re-seed from form_data on next render."""
    for key in _FORM_WIDGET_KEYS:
        st.session_state.pop(key, None)
    clear_number_widget_state()
    clear_multiselect_widget_state()


def apply_calculator_snapshot_to_form(snapshot: dict[str, Any]) -> str:
    """Pre-fill plan form from homepage housing calculator. Returns banner text."""
    from components.form_options import (
        CURRENT_INSTALLATIONS,
        GAINING_INSTALLATIONS,
        rank_for_pay_grade,
    )
    from services.installation_data import SUPPORTED_INSTALLATIONS

    init_form_state()
    data = st.session_state.form_data

    pay_grade = str(snapshot.get("pay_grade") or data.get("rank_pay_grade") or "E-5")
    yos = int(snapshot.get("years_of_service") if snapshot.get("years_of_service") is not None else 4)
    yos = max(0, min(40, yos))
    num_deps = int(snapshot.get("num_dependents") if snapshot.get("num_dependents") is not None else 0)
    num_deps = max(0, min(5, num_deps))

    gaining = str(snapshot.get("gaining_installation") or "").strip()
    current = snapshot.get("current_installation")
    current_s = str(current).strip() if current else ""

    data["rank_pay_grade"] = pay_grade
    if pay_grade != "Other":
        data["rank_title"] = rank_for_pay_grade(pay_grade)
    data["years_of_service"] = yos
    data["num_dependents"] = num_deps if num_deps > 0 else 0

    if num_deps <= 0:
        data["family_status"] = "Single (no dependents)"
        data["spouse_career_field"] = "N/A — single Soldier"
        data["spouse_career_other"] = ""
        data["spouse_monthly_income_usd"] = 0
        data["num_children"] = 0
        data["child_age_ranges"] = []
    else:
        data["family_status"] = "Married / with dependents"
        # Spouse counts as 1; remainder treated as children (editable on form).
        data["num_children"] = max(0, num_deps - 1)
        if str(data.get("spouse_career_field") or "").startswith("N/A"):
            data["spouse_career_field"] = "Not currently working — seeking employment"

    if gaining and gaining in GAINING_INSTALLATIONS:
        data["gaining_installation"] = gaining
        data["gaining_installation_other"] = ""
    elif gaining and gaining in SUPPORTED_INSTALLATIONS:
        data["gaining_installation"] = gaining
        data["gaining_installation_other"] = ""

    if current_s and current_s in CURRENT_INSTALLATIONS:
        data["current_installation_preset"] = current_s
        data["current_installation_other"] = ""
    elif current_s and current_s in SUPPORTED_INSTALLATIONS:
        data["current_installation_preset"] = current_s
        data["current_installation_other"] = ""

    total = snapshot.get("total_monthly_usd")
    if total is not None:
        try:
            total_i = int(total)
            if total_i > 0:
                # Seed housing budget so step 2 is not a cold start.
                data["max_monthly_budget"] = total_i
                data["budget_mode"] = "Set a monthly budget cap"
                data["budget_preset"] = "Custom amount"
        except (TypeError, ValueError):
            pass

    if snapshot.get("barracks_meal_card") and num_deps == 0:
        note = "Barracks + meal card (reduced OCONUS COLA ~63%) — confirm housing plan."
        existing = str(data.get("specific_concerns") or "").strip()
        if note not in existing:
            data["specific_concerns"] = f"{existing}\n{note}".strip() if existing else note

    sync_rank_from_pay_grade(data)
    st.session_state.form_data = data
    clear_form_widget_state()

    # Seed number widgets immediately so first paint matches.
    st.session_state[_number_widget_key("years_of_service")] = yos
    st.session_state[_number_widget_key("num_dependents")] = max(1, num_deps) if num_deps > 0 else 0
    st.session_state[_number_widget_key("num_children")] = int(data.get("num_children") or 0)
    if data.get("max_monthly_budget") is not None:
        st.session_state[_number_widget_key("max_monthly_budget")] = int(data["max_monthly_budget"])

    st.session_state["form_rank_pay_grade"] = pay_grade
    st.session_state["form_family_status"] = data["family_status"]
    if data.get("gaining_installation"):
        st.session_state["form_gaining_installation"] = data["gaining_installation"]
    if data.get("current_installation_preset"):
        st.session_state["form_current_installation"] = data["current_installation_preset"]

    bits = [pay_grade, f"{yos} YOS"]
    if num_deps <= 0:
        bits.append("single / 0 dependents")
    else:
        bits.append(f"{num_deps} dependent{'s' if num_deps != 1 else ''}")
    if gaining:
        bits.append(f"→ {gaining}")
    if current_s:
        bits.append(f"from {current_s}")
    if total is not None:
        try:
            bits.append(f"~${int(total):,}/mo housing package")
        except (TypeError, ValueError):
            pass

    banner = (
        "**Calculator details applied.** We pre-filled your plan with: "
        + " · ".join(bits)
        + ". Review and complete the remaining fields — nothing is locked."
    )
    st.session_state["calculator_carryover_banner"] = banner
    st.session_state["calculator_carryover_active"] = True
    return banner


def start_plan_from_calculator(*, require_snapshot: bool = False) -> None:
    """Navigate to the plan form, carrying calculator fields when available."""
    from components.bah_calculator import get_calculator_snapshot
    from components.sidebar import navigate_to

    snap = get_calculator_snapshot()
    if snap:
        apply_calculator_snapshot_to_form(snap)
    elif require_snapshot:
        st.session_state["calculator_carryover_banner"] = (
            "Open the housing calculator above first — then we can pre-fill your plan."
        )
    navigate_to("input")


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


FORM_STEPS: tuple[tuple[str, str], ...] = (
    ("Move & Family", "basics"),
    ("Housing & Priorities", "housing"),
    ("Logistics & Notes", "logistics"),
)

# Soldier-facing time estimates and "why this step" copy (shown on form wizard).
FORM_STEP_META: dict[int, dict[str, str]] = {
    0: {
        "time": "~2–3 min",
        "why": "We need posts, timeline, and family size so BAH/OHA and spouse plan match your reality.",
        "need": "Orders (or expected gaining post), pay grade, YOS, and who is moving with you.",
    },
    1: {
        "time": "~2 min",
        "why": "Housing preference and priorities drive the recommendation in Section 1 of your plan.",
        "need": "Rough budget comfort and what matters most this PCS (career, schools, cost, speed).",
    },
    2: {
        "time": "~1–2 min",
        "why": "Vehicles, DITY interest, and concerns shape logistics and risk flags in the report.",
        "need": "Vehicle count and anything unique (EFMP, dual-military, tight timeline, pets).",
    },
}


def init_form_step() -> None:
    if "form_step" not in st.session_state:
        st.session_state.form_step = 0


def validate_form_step(step: int, data: dict[str, Any]) -> list[str]:
    """Validate fields for a single wizard step before advancing."""
    errors: list[str] = []

    if step == 0:
        if not data.get("first_name", "").strip():
            errors.append("Enter your first name.")

        if not data.get("last_name", "").strip():
            errors.append("Enter your last name.")

        from services.email_delivery import normalize_email

        if not normalize_email(data.get("email", "")):
            errors.append("Enter a valid email — your report and PDF will be sent here.")

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

        num_children = int(data.get("num_children") or 0)
        if num_children > 0 and not data.get("child_age_ranges"):
            errors.append("Select at least one child age range.")

        if data.get("has_pets") == "Yes — we have pets" and not (
            data.get("pet_types") or data.get("pet_details", "").strip()
        ):
            errors.append("Select pet type(s) or add brief pet details.")

    elif step == 1:
        if data.get("budget_mode") == "Set a monthly budget cap":
            if data.get("budget_preset") == "Custom amount":
                budget = data.get("max_monthly_budget", 0)
                if not budget or budget <= 0:
                    errors.append("Enter a monthly housing budget greater than $0.")

        primary = data.get("primary_priority", "")
        secondary = data.get("secondary_priority", "")
        if primary and secondary and primary == secondary:
            errors.append("Choose different primary and secondary priorities.")

    return errors


def validate_form(data: dict[str, Any]) -> list[str]:
    """Return a list of validation error messages for the full form."""
    errors: list[str] = []
    for step in range(len(FORM_STEPS)):
        errors.extend(validate_form_step(step, data))
    return errors


def resolved_gaining_installation(data: dict[str, Any]) -> str:
    """Return the display name for the gaining installation."""
    gaining = data.get("gaining_installation", "")
    if gaining in ("Other CONUS installation", "Other OCONUS installation"):
        return data.get("gaining_installation_other", "").strip()
    return gaining


def budget_display(data: dict[str, Any]) -> str:
    if data.get("budget_mode") == "Optimize for best value":
        return "Optimize for best value"
    preset = data.get("budget_preset", "")
    if preset == "Custom amount":
        return f"${int(data.get('max_monthly_budget', 0)):,}/mo max"
    return preset
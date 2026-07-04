"""PCS Vector input form — family and move details."""

import streamlit as st

from components.form_options import (
    BUDGET_MODES,
    BUDGET_PRESETS,
    CHILD_AGE_RANGES,
    CONCERN_FLAGS,
    CURRENT_INSTALLATIONS,
    DITY_OPTIONS,
    GAINING_INSTALLATIONS,
    HOUSING_MUST_HAVES,
    HOUSING_PREFERENCES,
    MOVE_FLEXIBILITY,
    MOVE_WINDOWS,
    PET_OPTIONS,
    PET_TYPES,
    PRIORITY_CHOICES,
    RANK_PAY_GRADES,
    SPOUSE_CAREER_FIELDS,
    VEHICLE_COUNTS,
)
from components.form_state import collect_form_from_widgets, get_form_value, set_form_value, validate_form
from components.payment_handler import start_checkout_redirect
from views.payment_cancelled import render_payment_cancelled_banner
from services.stripe_payment import StripePaymentError, create_checkout_session, get_price_display


def _option_index(options: list[str], value: str, default: int = 0) -> int:
    try:
        return options.index(value)
    except ValueError:
        return default


def _section_header(title: str, description: str) -> None:
    st.markdown(f'<p class="pcs-section-title">{title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="pcs-section-desc">{description}</p>', unsafe_allow_html=True)


def _render_move_basics() -> None:
    _section_header(
        "1. Move Basics",
        "Where you're coming from, where you're headed, and your timeline.",
    )

    col_rank, col_title = st.columns([1, 2])
    with col_rank:
        set_form_value(
            "rank_pay_grade",
            st.selectbox(
                "Pay grade",
                options=RANK_PAY_GRADES,
                index=_option_index(RANK_PAY_GRADES, get_form_value("rank_pay_grade")),
                help="Your current pay grade. Choose Other if not listed.",
            ),
        )
    with col_title:
        set_form_value(
            "rank_title",
            st.text_input(
                "Rank / title",
                value=get_form_value("rank_title"),
                placeholder="e.g., Captain, Sergeant First Class",
                help="Optional for most grades; required if you selected Other.",
            ),
        )

    col_current, col_gaining = st.columns(2)
    with col_current:
        set_form_value(
            "current_installation_preset",
            st.selectbox(
                "Current Army installation",
                options=CURRENT_INSTALLATIONS,
                index=_option_index(
                    CURRENT_INSTALLATIONS, get_form_value("current_installation_preset")
                ),
            ),
        )
    with col_gaining:
        set_form_value(
            "gaining_installation",
            st.selectbox(
                "Gaining Army installation",
                options=GAINING_INSTALLATIONS,
                index=_option_index(
                    GAINING_INSTALLATIONS, get_form_value("gaining_installation")
                ),
                help="Best local data for Fort Liberty and Fort Drum.",
            ),
        )

    if get_form_value("current_installation_preset") == "Other installation":
        set_form_value(
            "current_installation_other",
            st.text_input(
                "Current installation name",
                value=get_form_value("current_installation_other"),
                placeholder="e.g., Fort Johnson, LA",
            ),
        )

    if get_form_value("gaining_installation") == "Other CONUS installation":
        set_form_value(
            "gaining_installation_other",
            st.text_input(
                "Other gaining installation",
                value=get_form_value("gaining_installation_other"),
                placeholder="e.g., Fort Eisenhower, GA",
            ),
        )

    col_window, col_flex = st.columns(2)
    with col_window:
        set_form_value(
            "move_window",
            st.selectbox(
                "Target move window",
                options=MOVE_WINDOWS,
                index=_option_index(MOVE_WINDOWS, get_form_value("move_window")),
            ),
        )
    with col_flex:
        set_form_value(
            "move_flexibility",
            st.selectbox(
                "Date flexibility",
                options=MOVE_FLEXIBILITY,
                index=_option_index(MOVE_FLEXIBILITY, get_form_value("move_flexibility")),
            ),
        )


def _render_family_situation() -> None:
    _section_header(
        "2. Family Situation",
        "Help us factor in employment, schools, and pets.",
    )

    set_form_value(
        "spouse_career_field",
        st.selectbox(
            "Spouse profession / field",
            options=SPOUSE_CAREER_FIELDS,
            index=_option_index(SPOUSE_CAREER_FIELDS, get_form_value("spouse_career_field")),
            help="Pick the closest match — we'll tailor job-market advice.",
        ),
    )

    if get_form_value("spouse_career_field") == "Other field":
        set_form_value(
            "spouse_career_other",
            st.text_input(
                "Describe spouse field",
                value=get_form_value("spouse_career_other"),
                placeholder="e.g., Real estate agent, military contractor",
            ),
        )

    col_children, col_ages = st.columns([1, 2])
    with col_children:
        set_form_value(
            "num_children",
            st.number_input(
                "Number of children",
                min_value=0,
                max_value=12,
                value=int(get_form_value("num_children")),
                step=1,
            ),
        )
    with col_ages:
        if get_form_value("num_children") > 0:
            current_ages = get_form_value("child_age_ranges") or []
            set_form_value(
                "child_age_ranges",
                st.multiselect(
                    "Children's age ranges",
                    options=CHILD_AGE_RANGES,
                    default=[a for a in current_ages if a in CHILD_AGE_RANGES],
                ),
            )
        else:
            set_form_value("child_age_ranges", [])
            st.caption("No children — school planning will be lighter.")

    set_form_value(
        "has_pets",
        st.radio(
            "Pets",
            options=PET_OPTIONS,
            index=_option_index(PET_OPTIONS, get_form_value("has_pets")),
            horizontal=True,
        ),
    )

    if get_form_value("has_pets") == "Yes — we have pets":
        set_form_value(
            "pet_types",
            st.multiselect(
                "Pet type(s)",
                options=PET_TYPES,
                default=[p for p in (get_form_value("pet_types") or []) if p in PET_TYPES],
            ),
        )
        set_form_value(
            "pet_details",
            st.text_input(
                "Pet notes (optional)",
                value=get_form_value("pet_details"),
                placeholder="e.g., breed restrictions, 2 cats",
            ),
        )
    else:
        set_form_value("pet_types", [])
        set_form_value("pet_details", "")


def _render_housing_budget() -> None:
    _section_header(
        "3. Housing & Budget",
        "Your living preferences and spending comfort zone.",
    )

    set_form_value(
        "housing_preference",
        st.radio(
            "Housing preference",
            options=HOUSING_PREFERENCES,
            index=_option_index(HOUSING_PREFERENCES, get_form_value("housing_preference")),
        ),
    )

    set_form_value(
        "budget_mode",
        st.radio(
            "Housing budget approach",
            options=BUDGET_MODES,
            index=_option_index(BUDGET_MODES, get_form_value("budget_mode")),
            horizontal=True,
        ),
    )

    if get_form_value("budget_mode") == "Set a monthly budget cap":
        set_form_value(
            "budget_preset",
            st.select_slider(
                "Monthly budget range",
                options=BUDGET_PRESETS,
                value=get_form_value("budget_preset")
                if get_form_value("budget_preset") in BUDGET_PRESETS
                else "$1,600 – $2,000/mo",
            ),
        )
        preset = get_form_value("budget_preset")
        if preset == "Under $1,200/mo":
            set_form_value("max_monthly_budget", 1200)
        elif preset == "$1,200 – $1,600/mo":
            set_form_value("max_monthly_budget", 1600)
        elif preset == "$1,600 – $2,000/mo":
            set_form_value("max_monthly_budget", 2000)
        elif preset == "$2,000+/mo":
            set_form_value("max_monthly_budget", 2200)
        else:
            set_form_value(
                "max_monthly_budget",
                st.number_input(
                    "Custom monthly cap ($)",
                    min_value=0,
                    max_value=10000,
                    value=int(get_form_value("max_monthly_budget") or 0),
                    step=50,
                ),
            )
    else:
        set_form_value("max_monthly_budget", 0)

    set_form_value(
        "housing_must_haves_selected",
        st.multiselect(
            "Housing must-haves",
            options=HOUSING_MUST_HAVES,
            default=[
                h
                for h in (get_form_value("housing_must_haves_selected") or [])
                if h in HOUSING_MUST_HAVES
            ],
            help="Select all that apply.",
        ),
    )
    set_form_value(
        "housing_must_haves_other",
        st.text_input(
            "Other must-haves (optional)",
            value=get_form_value("housing_must_haves_other"),
            placeholder="e.g., single-story, no carpet",
        ),
    )


def _render_priorities() -> None:
    _section_header(
        "4. Priorities",
        "Pick what matters most — we'll weight your plan toward these two.",
    )

    col_primary, col_secondary = st.columns(2)
    with col_primary:
        set_form_value(
            "primary_priority",
            st.selectbox(
                "Primary priority",
                options=PRIORITY_CHOICES,
                index=_option_index(PRIORITY_CHOICES, get_form_value("primary_priority")),
            ),
        )
    with col_secondary:
        secondary_options = [
            p for p in PRIORITY_CHOICES if p != get_form_value("primary_priority")
        ]
        current_secondary = get_form_value("secondary_priority")
        if current_secondary not in secondary_options:
            current_secondary = secondary_options[0] if secondary_options else ""
        set_form_value(
            "secondary_priority",
            st.selectbox(
                "Secondary priority",
                options=secondary_options,
                index=_option_index(secondary_options, current_secondary),
            ),
        )

    set_form_value(
        "other_priorities",
        st.text_area(
            "Other priorities (optional)",
            value=get_form_value("other_priorities"),
            placeholder="e.g., Stay near family, need EFMP accommodations",
            height=80,
        ),
    )


def _render_logistics() -> None:
    _section_header(
        "5. Logistics",
        "Moving practicalities that affect timing and cost.",
    )

    col_vehicles, col_dity = st.columns(2)
    with col_vehicles:
        set_form_value(
            "num_vehicles",
            st.selectbox(
                "Number of vehicles",
                options=VEHICLE_COUNTS,
                index=_option_index(VEHICLE_COUNTS, str(get_form_value("num_vehicles"))),
            ),
        )
    with col_dity:
        set_form_value(
            "dity_interest",
            st.radio(
                "DITY / PPM move interest",
                options=DITY_OPTIONS,
                index=_option_index(DITY_OPTIONS, get_form_value("dity_interest")),
            ),
        )


def _render_specific_concerns() -> None:
    _section_header(
        "6. Specific Concerns",
        "Flag anything that should shape your plan.",
    )

    set_form_value(
        "concern_flags",
        st.multiselect(
            "Common concerns",
            options=CONCERN_FLAGS,
            default=[c for c in (get_form_value("concern_flags") or []) if c in CONCERN_FLAGS],
        ),
    )
    set_form_value(
        "specific_concerns",
        st.text_area(
            "Additional context (optional)",
            value=get_form_value("specific_concerns"),
            placeholder="Anything else — custody schedules, medical needs, dual-military timing",
            height=100,
        ),
    )


def render_input_form() -> None:
    """Render the full PCS input form."""
    st.markdown("## Tell us about your move")
    price = get_price_display()
    st.markdown(
        f"Most families finish in **6–8 minutes**. After checkout (**{price}** one-time), "
        "you'll receive your full 8-section plan and PDF download."
    )
    st.caption(
        "Your answers stay in this browser session only — used to generate your report. "
        "We don't sell your data. Payment is handled securely by Stripe."
    )

    if st.session_state.get("payment_cancelled"):
        render_payment_cancelled_banner()
        st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.get("report_error"):
        st.error(st.session_state.report_error)

    tab_basics, tab_family, tab_rest = st.tabs(
        ["Move & Family", "Housing & Priorities", "Logistics & Notes"]
    )

    with tab_basics:
        with st.container(border=True):
            _render_move_basics()
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            _render_family_situation()

    with tab_family:
        with st.container(border=True):
            _render_housing_budget()
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            _render_priorities()

    with tab_rest:
        with st.container(border=True):
            _render_logistics()
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            _render_specific_concerns()

    st.markdown("<br>", unsafe_allow_html=True)

    col_back, col_spacer, col_generate = st.columns([1, 2, 1])

    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    with col_generate:
        if st.button(
            f"Proceed to Payment — {price}",
            type="primary",
            use_container_width=True,
        ):
            form_data = collect_form_from_widgets()
            errors = validate_form(form_data)

            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save form for use after Stripe redirect (same browser session).
                form_data["form_submitted"] = True
                st.session_state.form_data = form_data
                st.session_state.report_markdown = None
                st.session_state.report_error = None
                st.session_state.payment_verified = False
                st.session_state.stripe_checkout_session_id = None

                try:
                    checkout_url, session_id = create_checkout_session()
                    st.session_state.stripe_checkout_session_id = session_id
                    st.session_state.payment_message = None
                    start_checkout_redirect(checkout_url)
                except StripePaymentError as exc:
                    st.error(str(exc))
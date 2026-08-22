"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import TRUST_SIGNALS
from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.installation_data import SUPPORTED_INSTALLATIONS
from services.referral_lead import (
    INTEREST_OPTIONS,
    REFERRAL_COLUMNS,
    build_prefill_url,
    build_referral_row,
    format_dependents_label,
    format_rank_label,
    format_rent_range,
    google_form_configured,
    submit_referral_to_google_form,
)


def _render_header() -> None:
    st.markdown(
        f"""
        <div class="pcs-hero pcs-hero-compact">
            <div class="pcs-brand-title">PCS Vector</div>
            <div class="pcs-hero-tag">{safe_html(TRUST_SIGNALS["banner"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_referral_hook() -> None:
    snap = get_calculator_snapshot() or {}
    dest_default = snap.get("gaining_installation") or ""
    grade_default = snap.get("pay_grade") or "E-5"
    num_deps = int(snap.get("num_dependents") or 0)
    with_deps = num_deps > 0
    deps_default = format_dependents_label(
        with_dependents=with_deps, num_dependents=num_deps
    )
    rank_default = format_rank_label(
        grade_default, PAY_GRADE_TO_RANK.get(str(grade_default))
    )
    rent_range_default = format_rent_range(
        snap.get("market_rent_low_usd"),
        snap.get("market_rent_high_usd"),
        snap.get("market_rent_mid_usd"),
    )

    installs = list(SUPPORTED_INSTALLATIONS)
    if dest_default and dest_default not in installs:
        installs = [dest_default] + installs

    st.markdown(
        """
        <div class="pcs-ref-card">
            <div class="pcs-ref-kicker">Free · takes under a minute</div>
            <h3 class="pcs-ref-title">Ready to find a place?</h3>
            <p class="pcs-ref-body">
                You’ve got the money picture. Tell us where you’re headed and we’ll
                connect you with someone who helps Soldiers rent or buy — no cost to you.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        if "referral_destination" not in st.session_state and dest_default:
            st.session_state.referral_destination = dest_default
        if "referral_rank" not in st.session_state and rank_default:
            st.session_state.referral_rank = rank_default
        if "referral_dependents" not in st.session_state:
            st.session_state.referral_dependents = deps_default
        if "referral_rent_range" not in st.session_state and rent_range_default:
            st.session_state.referral_rent_range = rent_range_default

        destination = st.selectbox(
            "Destination",
            options=installs,
            key="referral_destination",
            help="Your new post (from the calculator).",
        )

        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input(
                "First Name",
                key="referral_first_name",
                placeholder="First name",
            )
        with c2:
            last_name = st.text_input(
                "Last Name",
                key="referral_last_name",
                placeholder="Last name",
            )

        grades = [g for g in RANK_PAY_GRADES if g != "Other"]
        rank_options = [format_rank_label(g, PAY_GRADE_TO_RANK.get(g)) for g in grades]
        if rank_default and rank_default not in rank_options:
            rank_options = [rank_default] + rank_options
        rank = st.selectbox("Rank", options=rank_options, key="referral_rank")

        dep_options = [
            "Without dependents",
            "With dependents (1)",
            "With dependents (2)",
            "With dependents (3)",
            "With dependents (4)",
            "With dependents (5+)",
        ]
        if deps_default not in dep_options:
            dep_options = [deps_default] + dep_options
        dependents = st.selectbox(
            "Dependents",
            options=dep_options,
            key="referral_dependents",
            help="Collected in-app — add this question to the Google Form to sync it.",
        )

        email_address = st.text_input(
            "Email address",
            key="referral_email_address",
            placeholder="you@email.com",
            help="Collected in-app — add this question to the Google Form to sync it.",
        )

        rent_buy_not_sure = st.radio(
            "Rent/Buy/Not Sure",
            options=list(INTEREST_OPTIONS),
            horizontal=True,
            key="referral_rent_buy_not_sure",
        )

        rent_range = st.text_input(
            "Rent Range",
            key="referral_rent_range",
            placeholder="$1,200–$1,650/mo",
            help="Prefills from the calculator’s typical rent band for your family size.",
        )

        st.caption("Free referral · Built For Soldiers; By Soldiers · We won’t spam you.")

        if st.button(
            "Get my free housing referral →",
            type="primary",
            use_container_width=True,
            key="referral_submit",
        ):
            row = build_referral_row(
                destination=str(destination or ""),
                first_name=first_name or "",
                last_name=last_name or "",
                rank=str(rank or ""),
                rent_buy_not_sure=str(rent_buy_not_sure or ""),
                rent_range=rent_range or "",
                dependents=str(dependents or ""),
                email_address=email_address or "",
            )

            if not row["First Name"] or not row["Last Name"]:
                st.error("Enter your first and last name.")
            elif not row["Email address"] or "@" not in row["Email address"]:
                st.error("Enter a valid email address.")
            elif not row["Destination"]:
                st.error("Pick a destination.")
            else:
                st.session_state.referral_lead = {**row, "calculator": snap}
                prefill = build_prefill_url(row)

                ok = False
                msg = ""
                if google_form_configured():
                    ok, msg = submit_referral_to_google_form(row)

                if ok:
                    st.success(
                        f"You’re in — we’ll follow up about housing near **{row['Destination']}**."
                    )
                else:
                    st.success("Almost done — confirm on the Google Form (1 click).")
                    st.link_button(
                        "Submit housing referral on Google Form →",
                        prefill,
                        type="primary",
                        use_container_width=True,
                    )
                    if msg:
                        st.caption(msg)
                    st.caption(
                        "Your answers are pre-filled. Click Submit on the Form page."
                    )

                with st.expander("What we captured", expanded=False):
                    st.json(
                        {
                            k: row[k]
                            for k in list(REFERRAL_COLUMNS)
                            + ["Dependents", "Email address"]
                        }
                    )


def _render_faq() -> None:
    with st.expander("FAQ", expanded=False):
        st.markdown(
            "**Free?** Yes.\n\n"
            "**BAH** — Flat U.S. housing pay. Keep the leftover if rent is lower.\n\n"
            "**OHA** — Overseas: actual rent up to a max, plus utilities.\n\n"
            "**COLA** — Extra for higher daily costs overseas, Alaska, Hawaii, and Puerto Rico. Not for rent.\n\n"
            "**DLA** — One-time move money when authorized. Confirm with finance.\n\n"
            "**Rent estimates** — Planning ranges by family size (1–4 bedrooms), not official rates.\n\n"
            "**Official?** Allowances from DoD tables — verify on your LES before you sign."
        )


def render_home() -> None:
    _render_header()
    render_bah_calculator()
    _render_referral_hook()
    _render_faq()
    st.caption("PCS Vector — Built For Soldiers; By Soldiers · Verify with finance before you spend.")

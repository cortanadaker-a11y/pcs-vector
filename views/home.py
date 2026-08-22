"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import TRUST_SIGNALS
from components.form_options import PAY_GRADE_TO_RANK
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
        # Always take Rank + Dependents from the live calculator (no re-entry)
        rank = rank_default
        dependents = deps_default

        st.caption(
            f"From calculator: {rank or '—'} · {dependents}"
            + (f" · {dest_default}" if dest_default else "")
        )

        if "referral_destination" not in st.session_state and dest_default:
            st.session_state.referral_destination = dest_default
        # Keep rent range in sync with calculator when it changes
        if rent_range_default:
            st.session_state.referral_rent_range = rent_range_default

        destination = st.selectbox(
            "Destination",
            options=installs,
            key="referral_destination",
            help="Your new post from the calculator (change only if needed).",
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

        email_address = st.text_input(
            "Email address",
            key="referral_email_address",
            placeholder="you@email.com",
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
            help="From the calculator’s typical rent band for your family size.",
        )

        st.caption("Free referral · Built For Soldiers; By Soldiers · We won’t spam you.")

        if st.button(
            "Get my free housing referral →",
            type="primary",
            use_container_width=True,
            key="referral_submit",
        ):
            # Re-read calculator snapshot at submit so rank/deps stay current
            live = get_calculator_snapshot() or snap
            live_grade = live.get("pay_grade") or grade_default
            live_deps_n = int(live.get("num_dependents") or 0)
            live_rank = format_rank_label(
                str(live_grade), PAY_GRADE_TO_RANK.get(str(live_grade))
            )
            live_deps = format_dependents_label(
                with_dependents=live_deps_n > 0, num_dependents=live_deps_n
            )
            live_dest = live.get("gaining_installation") or destination
            live_rent = format_rent_range(
                live.get("market_rent_low_usd"),
                live.get("market_rent_high_usd"),
                live.get("market_rent_mid_usd"),
            ) or (rent_range or "")

            row = build_referral_row(
                destination=str(destination or live_dest or ""),
                first_name=first_name or "",
                last_name=last_name or "",
                rank=live_rank,
                rent_buy_not_sure=str(rent_buy_not_sure or ""),
                rent_range=live_rent,
                dependents=live_deps,
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

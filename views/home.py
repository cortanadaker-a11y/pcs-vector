"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import TRUST_SIGNALS
from components.form_options import PAY_GRADE_TO_RANK
from components.html_utils import safe_html
from services.referral_lead import (  # noqa: I001
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


def _calc_fields_from_snap(snap: dict) -> dict[str, str]:
    """Pull Destination / Rank / Dependents / Rent Range from calculator snapshot."""
    grade = str(snap.get("pay_grade") or "E-5")
    num_deps = int(snap.get("num_dependents") or 0)
    return {
        "destination": str(snap.get("gaining_installation") or "").strip(),
        "rank": format_rank_label(grade, PAY_GRADE_TO_RANK.get(grade)),
        "dependents": format_dependents_label(
            with_dependents=num_deps > 0, num_dependents=num_deps
        ),
        "rent_range": format_rent_range(
            snap.get("market_rent_low_usd"),
            snap.get("market_rent_high_usd"),
            snap.get("market_rent_mid_usd"),
        ),
    }


def _render_referral_hook() -> None:
    snap = get_calculator_snapshot() or {}
    calc = _calc_fields_from_snap(snap)

    st.markdown(
        """
        <div class="pcs-ref-card">
            <div class="pcs-ref-kicker">Free · under a minute</div>
            <h3 class="pcs-ref-title">Ready to find a place?</h3>
            <p class="pcs-ref-body">
                We’ll connect you with someone who helps Soldiers rent or buy.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        if not calc["destination"]:
            st.info("Run the calculator above first — Destination, Rank, and Dependents come from there.")

        # Always mirror calculator (no re-entry for Destination / Rank / Dependents)
        st.markdown("##### From your calculator")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"**Destination**  \n{calc['destination'] or '—'}")
            st.markdown(f"**Rank**  \n{calc['rank'] or '—'}")
        with m2:
            st.markdown(f"**Dependents**  \n{calc['dependents'] or '—'}")
            if calc["rent_range"]:
                st.markdown(f"**Rent range**  \n{calc['rent_range']}")

        st.divider()
        st.markdown("##### Your contact info")

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

        # Prefill rent range from calculator; allow tweak
        if calc["rent_range"] and st.session_state.get("referral_rent_range_src") != calc["rent_range"]:
            st.session_state.referral_rent_range = calc["rent_range"]
            st.session_state.referral_rent_range_src = calc["rent_range"]

        rent_range = st.text_input(
            "Rent Range",
            key="referral_rent_range",
            placeholder="$1,200–$1,650/mo",
            help="Filled from the calculator — change if you want a different target.",
        )

        st.caption("Free · Built For Soldiers; By Soldiers")

        if st.button(
            "Get my free housing referral →",
            type="primary",
            use_container_width=True,
            key="referral_submit",
        ):
            live = get_calculator_snapshot() or snap
            live_calc = _calc_fields_from_snap(live)

            row = build_referral_row(
                destination=live_calc["destination"],
                first_name=first_name or "",
                last_name=last_name or "",
                rank=live_calc["rank"],
                rent_buy_not_sure=str(rent_buy_not_sure or ""),
                rent_range=(rent_range or live_calc["rent_range"] or ""),
                dependents=live_calc["dependents"],
                email_address=email_address or "",
            )

            if not live_calc["destination"]:
                st.error("Set New post in the calculator above first.")
            elif not row["First Name"] or not row["Last Name"]:
                st.error("Enter your first and last name.")
            elif not row["Email address"] or "@" not in row["Email address"]:
                st.error("Enter a valid email address.")
            else:
                st.session_state.referral_lead = {**row, "calculator": live}
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
                    st.caption("Answers are pre-filled. Click Submit on the Form.")

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

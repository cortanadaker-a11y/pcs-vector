"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import TRUST_SIGNALS
from components.form_options import PAY_GRADE_TO_RANK
from components.html_utils import safe_html
from services.referral_lead import (
    INTEREST_OPTIONS,
    build_one_click_submit_html,
    build_prefill_url,
    build_referral_row,
    format_dependents_label,
    format_rank_label,
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
    """Carry-over fields from what the Soldier entered in the calculator."""
    grade = str(snap.get("pay_grade") or "")
    num_deps = int(snap.get("num_dependents") or 0)
    return {
        "destination": str(snap.get("gaining_installation") or "").strip(),
        "rank": format_rank_label(grade, PAY_GRADE_TO_RANK.get(grade)) if grade else "",
        "dependents": format_dependents_label(
            with_dependents=num_deps > 0, num_dependents=num_deps
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
            st.info(
                "Use the calculator above first — your New post, Rank, and Dependents "
                "carry over automatically."
            )

        st.markdown("##### From your calculator")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Destination**  \n{calc['destination'] or '—'}")
        with c2:
            st.markdown(f"**Rank**  \n{calc['rank'] or '—'}")
        with c3:
            st.markdown(f"**Dependents**  \n{calc['dependents'] or '—'}")

        st.divider()
        st.markdown("##### How we reach you")

        n1, n2 = st.columns(2)
        with n1:
            first_name = st.text_input(
                "First Name",
                key="referral_first_name",
                placeholder="First name",
            )
        with n2:
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

                # One click: browser POSTs to Google Form (and opens confirmation tab)
                st.html(
                    build_one_click_submit_html(row),
                    unsafe_allow_javascript=True,
                )
                st.success(
                    f"You’re in — we’ll follow up about housing near **{row['Destination']}**."
                )
                st.caption(
                    "A Google tab should open with your referral. "
                    "Allow pop-ups for this site if you don’t see it. "
                    f"[Backup: open pre-filled form]({build_prefill_url(row)})"
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

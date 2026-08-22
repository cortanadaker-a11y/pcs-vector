"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import TRUST_SIGNALS
from components.html_utils import safe_html


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
    snap = get_calculator_snapshot()
    dest = (snap or {}).get("gaining_installation") or "your new post"
    total = (snap or {}).get("total_monthly_usd")
    grade = (snap or {}).get("pay_grade")
    system = (snap or {}).get("housing_system") or "BAH"
    market_mid = (snap or {}).get("market_rent_mid_usd")
    bedrooms = (snap or {}).get("market_bedrooms")
    arrive = (snap or {}).get("arrive_cash_net_usd")

    bits = []
    if grade:
        bits.append(str(grade))
    if total is not None:
        bits.append(f"about ${int(total):,}/month {system}")
    if market_mid is not None and bedrooms is not None:
        bits.append(f"typical {int(bedrooms)}-bedroom rent about ${int(market_mid):,}")
    if arrive is not None and arrive > 0:
        bits.append(f"still need about ${int(arrive):,} after DLA for move-in")
    elif arrive == 0:
        bits.append("DLA may cover a typical move-in")
    meta = " · ".join(bits) if bits else "Based on the numbers from the calculator above"

    st.markdown(
        f"""
        <div class="pcs-ref-card">
            <div class="pcs-ref-kicker">Free · no obligation</div>
            <h3 class="pcs-ref-title">Need help finding a place near {safe_html(dest)}?</h3>
            <p class="pcs-ref-body">
                We can connect you with someone who helps military families buy or rent.
                There is no charge to request a referral.
            </p>
            <div class="pcs-ref-meta">{safe_html(meta)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", key="referral_name", placeholder="First and last name")
        with c2:
            email = st.text_input("Email", key="referral_email", placeholder="you@email.com")
        interest = st.radio(
            "I want to",
            options=["Rent", "Buy", "Not sure yet"],
            horizontal=True,
            key="referral_interest",
        )
        notes = st.text_input(
            "Anything else we should know? (optional)",
            key="referral_notes",
            placeholder="Report date, pets, schools…",
        )
        st.caption("We will not spam you. Built For Soldiers; By Soldiers.")
        if st.button("Request a free referral →", type="primary", use_container_width=True, key="referral_submit"):
            if not (email or "").strip() or "@" not in (email or ""):
                st.error("Please enter a valid email so we can reach you.")
            else:
                st.session_state.referral_lead = {
                    "name": (name or "").strip(),
                    "email": (email or "").strip(),
                    "interest": interest,
                    "notes": (notes or "").strip(),
                    "gaining_installation": dest,
                    "pay_grade": grade,
                    "housing_package_usd": total,
                    "market_rent_mid_usd": market_mid,
                    "market_bedrooms": bedrooms,
                    "arrive_cash_net_usd": arrive,
                    "calculator": snap,
                }
                st.success(f"Thanks — we will follow up about housing near **{dest}**.")
                st.caption("Built For Soldiers; By Soldiers")


def _render_faq() -> None:
    with st.expander("Common questions", expanded=False):
        st.markdown(
            "**Is this free?** Yes. The calculator and housing referrals are free.\n\n"
            "**What is BAH?** Basic Allowance for Housing — a flat monthly housing payment "
            "for most U.S. posts. If rent is less than BAH, you usually keep the difference.\n\n"
            "**What is OHA?** Overseas Housing Allowance — for foreign posts. It pays your actual rent "
            "up to a maximum, plus a utilities allowance.\n\n"
            "**What is COLA?** Cost of Living Allowance — extra money for higher day-to-day costs "
            "overseas (and in Hawaii / Puerto Rico). It is not meant for rent.\n\n"
            "**What is DLA?** Dislocation Allowance — one-time money for a move when you are authorized. "
            "Confirm with finance. It is not a travel advance you have to pay back.\n\n"
            "**Where do the rent numbers come from?** They are planning estimates for a home size based "
            "on how many dependents you have (1 to 4 bedrooms). They are not official rates.\n\n"
            "**Are the allowance numbers official?** BAH, OHA, COLA, and DLA come from DoD planning tables. "
            "Always check your LES and confirm with finance before you sign a lease or buy."
        )


def render_home() -> None:
    _render_header()
    render_bah_calculator()
    _render_referral_hook()
    _render_faq()
    st.caption(
        "PCS Vector — Built For Soldiers; By Soldiers. "
        "Always confirm BAH, OHA, COLA, and DLA with your finance office before you spend."
    )

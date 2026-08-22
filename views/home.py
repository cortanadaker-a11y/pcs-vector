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
        bits.append(f"${int(total):,}/mo {system}")
    if market_mid is not None and bedrooms is not None:
        bits.append(f"{int(bedrooms)}BR ~${int(market_mid):,}")
    if arrive is not None and arrive > 0:
        bits.append(f"~${int(arrive):,} needed after DLA")
    meta = " · ".join(bits) if bits else "From your calculator results"

    st.markdown(
        f"""
        <div class="pcs-ref-card">
            <div class="pcs-ref-kicker">Free referral</div>
            <h3 class="pcs-ref-title">Buy or rent near {safe_html(dest)}</h3>
            <p class="pcs-ref-body">We’ll connect you with a partner who works military PCS moves.</p>
            <div class="pcs-ref-meta">{safe_html(meta)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name", key="referral_name", placeholder="First and last")
        with c2:
            email = st.text_input("Email", key="referral_email", placeholder="you@email.com")
        interest = st.radio(
            "I want to",
            options=["Rent", "Buy", "Not sure"],
            horizontal=True,
            key="referral_interest",
        )
        notes = st.text_input(
            "Notes (optional)",
            key="referral_notes",
            placeholder="Report date, pets, schools…",
        )
        if st.button("Request free referral →", type="primary", use_container_width=True, key="referral_submit"):
            if not (email or "").strip() or "@" not in (email or ""):
                st.error("Enter a valid email.")
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
                st.success(f"Got it — we’ll follow up about housing near **{dest}**.")


def _render_faq() -> None:
    with st.expander("FAQ", expanded=False):
        st.markdown(
            "**Free?** Yes.\n\n"
            "**BAH** — Flat U.S. housing pay. Keep the leftover if rent is lower.\n\n"
            "**OHA** — Overseas: actual rent up to a max, plus utilities.\n\n"
            "**COLA** — Extra for higher daily costs overseas / HI / PR. Not for rent.\n\n"
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

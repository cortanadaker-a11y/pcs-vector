"""Payment gate UI when report access requires checkout."""

import streamlit as st

from components.payment_handler import retry_checkout_from_saved_form
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def render_payment_required() -> None:
    """Show paywall with option to start or resume Stripe Checkout."""
    price = get_price_display()

    st.markdown("## Almost there — unlock your plan")
    st.markdown(
        f"Your answers are saved in this session. One-time payment of **{price}** unlocks the full "
        "8-section plan and PDF — no subscription, no upsells."
    )

    with st.container(border=True):
        st.markdown(f"**What you get for {price}**")
        st.markdown(
            "- Plan written for *your* posts, rank, and family — not a generic checklist  \n"
            "- Housing call with 2026 BAH / OHA + COLA math  \n"
            "- Spouse career, schools/childcare, cash-flow pressure  \n"
            "- First 30 days with decision gates + commander brief line  \n"
            "- PDF emailed so you can forward it to your spouse tonight"
        )

    if st.button(f"Pay {price} — unlock my plan", type="primary", use_container_width=True):
        retry_checkout_from_saved_form()

    st.caption("Secure Stripe checkout · Built For Soldiers; By Soldiers")
    if st.button("Already paid? Retrieve report", use_container_width=True, key="paywall_retrieve"):
        navigate_to("retrieve")

"""Payment gate UI when report access requires checkout."""

import streamlit as st

from components.payment_handler import retry_checkout_from_saved_form
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def render_payment_required() -> None:
    """Show paywall with option to start or resume Stripe Checkout."""
    price = get_price_display()

    st.markdown("## Complete payment to unlock your plan")
    st.markdown(
        f"Your answers are saved. Pay **{price}** once for your personalized "
        "8-section plan and PDF — no subscription."
    )

    with st.container(border=True):
        st.markdown(f"**PCS Vector Report — {price}**")
        st.markdown(
            "- Personalized strategy for your posts and family  \n"
            "- Housing & BAH tradeoffs · spouse career · schools  \n"
            "- 30-day action plan with decision gates  \n"
            "- PDF emailed automatically after generation"
        )

    if st.button(f"Pay {price} — unlock report", type="primary", use_container_width=True):
        retry_checkout_from_saved_form()

    st.caption("Secure checkout via Stripe. If you already paid, use Retrieve report.")
    if st.button("Already paid? Retrieve report", use_container_width=True, key="paywall_retrieve"):
        navigate_to("retrieve")

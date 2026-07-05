"""Payment gate UI when report access requires checkout."""

import streamlit as st

from components.payment_handler import retry_checkout_from_saved_form
from services.stripe_payment import get_price_display


def render_payment_required() -> None:
    """Show paywall with option to start or resume Stripe Checkout."""
    price = get_price_display()

    st.markdown("## Almost there — complete your payment")
    st.markdown(
        f"Your move details are saved. Pay **{price}** once to unlock your personalized "
        "8-section strategic plan and professional PDF."
    )
    st.info(
        "No subscription. One payment → one report. If checkout was interrupted, "
        "use the button below — you won't need to re-enter your answers.",
        icon="ℹ️",
    )

    with st.container(border=True):
        st.markdown(f"### PCS Vector Report — {price}")
        st.markdown(
            "- 8-section personalized PCS strategic plan  \n"
            "- Fort Liberty, Fort Cavazos & Fort Drum-specific guidance  \n"
            "- BAH and housing tradeoff analysis  \n"
            "- Spouse career, schools, and 30-day action plan  \n"
            "- Professional PDF export"
        )

    if st.button(f"Proceed to Payment — {price}", type="primary", use_container_width=True):
        retry_checkout_from_saved_form()
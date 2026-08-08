"""UI shown when the user cancels Stripe Checkout — easy retry without losing form data."""

import streamlit as st

from components.payment_handler import retry_checkout_from_saved_form
from services.stripe_payment import get_price_display


def render_payment_cancelled_banner() -> None:
    """Prominent retry panel on the input form after a cancelled checkout."""
    price = get_price_display()

    st.markdown(
        """
        <div class="pcs-payment-cancelled">
            <strong>Checkout cancelled</strong><br>
            Your answers are still saved. Review anything you need, then retry payment —
            you won't re-enter the form.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_msg, col_retry = st.columns([2, 1])
    with col_msg:
        st.caption(f"{price} one-time · secure Stripe checkout")
    with col_retry:
        if st.button(
            f"Retry payment — {price}",
            type="primary",
            use_container_width=True,
            key="retry_payment_cancelled",
        ):
            retry_checkout_from_saved_form()

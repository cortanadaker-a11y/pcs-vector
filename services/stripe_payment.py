"""Stripe Checkout integration for PCS Vector.

Payment flow (Streamlit + hosted Checkout):
  1. User submits form → we save form_data to session_state (report NOT generated yet).
  2. create_checkout_session() opens Stripe's hosted payment page ($25).
  3. On success, Stripe redirects to APP_BASE_URL/?payment=success&session_id=...
  4. handle_payment_callback() (in app.py) verifies the session server-side.
  5. Only after payment_verified=True does the report page call Grok + enable PDF.
"""

from __future__ import annotations

import stripe

from services.stripe_config import (
    REPORT_PRICE_CENTS,
    REPORT_PRICE_DISPLAY,
    REPORT_PRODUCT_DESCRIPTION,
    REPORT_PRODUCT_NAME,
    StripeConfigError,
    get_app_base_url,
    get_stripe_secret_key,
)


class StripePaymentError(Exception):
    """Raised when Stripe payment operations fail."""


def _configure_stripe() -> None:
    try:
        stripe.api_key = get_stripe_secret_key()
    except StripeConfigError as exc:
        raise StripePaymentError(str(exc)) from exc


def create_checkout_session() -> tuple[str, str]:
    """Create a hosted Stripe Checkout session.

    Returns:
        (checkout_url, session_id) — redirect the user to checkout_url.
    """
    _configure_stripe()

    # Stripe substitutes {CHECKOUT_SESSION_ID} on redirect after payment.
    base_url = get_app_base_url()
    success_url = f"{base_url}/?payment=success&session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{base_url}/?payment=cancelled"

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": REPORT_PRICE_CENTS,
                        "product_data": {
                            "name": REPORT_PRODUCT_NAME,
                            "description": REPORT_PRODUCT_DESCRIPTION,
                        },
                    },
                    "quantity": 1,
                }
            ],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"product": "pcs_vector_report"},
        )
    except stripe.error.StripeError as exc:
        raise StripePaymentError(f"Could not start checkout: {exc.user_message or exc}") from exc

    if not session.url or not session.id:
        raise StripePaymentError("Stripe returned an invalid checkout session.")

    return session.url, session.id


def verify_checkout_session(session_id: str) -> bool:
    """Server-side verification — never trust the URL alone.

    Retrieves the session from Stripe and confirms payment_status == 'paid'.
    """
    if not session_id:
        return False

    _configure_stripe()

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as exc:
        raise StripePaymentError(
            f"Could not verify payment: {exc.user_message or exc}"
        ) from exc

    return session.payment_status == "paid"


def get_price_display() -> str:
    """Return formatted price for UI labels."""
    return REPORT_PRICE_DISPLAY


def format_order_reference(session_id: str) -> str:
    """Build a short, human-friendly order reference from a Checkout session ID."""
    if not session_id:
        return "N/A"
    suffix = session_id.replace("cs_test_", "").replace("cs_live_", "")[-8:].upper()
    return f"PCS-{suffix}"


def get_checkout_receipt(session_id: str) -> dict[str, str]:
    """Fetch receipt details for the post-payment confirmation screen."""
    _configure_stripe()
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.StripeError as exc:
        raise StripePaymentError(
            f"Could not load payment receipt: {exc.user_message or exc}"
        ) from exc

    amount = ""
    if session.amount_total is not None:
        amount = f"${session.amount_total / 100:.2f}"

    return {
        "order_reference": format_order_reference(session_id),
        "amount_paid": amount or REPORT_PRICE_DISPLAY,
        "payment_status": session.payment_status or "unknown",
        "customer_email": session.customer_details.email if session.customer_details else "",
    }
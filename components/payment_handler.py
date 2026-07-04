"""Handle Stripe Checkout return URLs and payment session state.

Session-state contract:
  - form_data: saved before checkout; survives the Stripe redirect in the same browser session
  - payment_verified: True only after Stripe session is verified server-side
  - stripe_checkout_session_id: paid Checkout session ID (re-verified on report/PDF actions)
  - payment_order_ref: short confirmation reference shown after successful payment
  - payment_cancelled: True when user returns from Stripe without paying (retry UX on input form)
  - report_markdown: None until payment_verified; Grok runs on report page with loading UI
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from services.stripe_payment import (
    StripePaymentError,
    format_order_reference,
    get_checkout_receipt,
    verify_checkout_session,
)


def init_payment_state() -> None:
    """Initialize payment-related session state keys."""
    defaults = {
        "payment_verified": False,
        "stripe_checkout_session_id": None,
        "payment_order_ref": None,
        "payment_amount_display": None,
        "payment_completed_at": None,
        "payment_cancelled": False,
        "payment_message": None,
        "payment_message_type": None,  # success | warning | error | info
        "show_payment_success_screen": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _set_payment_message(message: str, msg_type: str = "info") -> None:
    st.session_state.payment_message = message
    st.session_state.payment_message_type = msg_type


def handle_payment_callback() -> None:
    """Process Stripe success/cancel query params on every app load (app.py calls this early).

    Stripe redirects to:
      - ?payment=success&session_id=cs_test_...  → verify → unlock report generation
      - ?payment=cancelled                        → show retry message, keep form_data
    """
    payment = st.query_params.get("payment")
    if not payment:
        return

    if payment == "success":
        session_id = st.query_params.get("session_id", "")
        try:
            if verify_checkout_session(session_id):
                receipt = get_checkout_receipt(session_id)
                st.session_state.payment_verified = True
                st.session_state.stripe_checkout_session_id = session_id
                st.session_state.payment_order_ref = receipt["order_reference"]
                st.session_state.payment_amount_display = receipt["amount_paid"]
                st.session_state.payment_completed_at = datetime.now().strftime(
                    "%B %d, %Y at %I:%M %p"
                )
                st.session_state.payment_cancelled = False
                st.session_state.show_payment_success_screen = True
                st.session_state.report_markdown = None
                st.session_state.page = "report"
                _set_payment_message(None, "success")
            else:
                st.session_state.payment_verified = False
                _set_payment_message(
                    "Payment is still processing. Wait a moment and refresh, or try checkout again.",
                    "warning",
                )
                st.session_state.page = "input"
        except StripePaymentError as exc:
            st.session_state.payment_verified = False
            _set_payment_message(str(exc), "error")
            st.session_state.page = "input"

    elif payment == "cancelled":
        st.session_state.payment_verified = False
        st.session_state.payment_cancelled = True
        st.session_state.page = "input"
        _set_payment_message(None, "warning")

    _clear_payment_query_params()


def _clear_payment_query_params() -> None:
    """Remove payment query params so reruns don't re-trigger verification."""
    try:
        qp = dict(st.query_params)
        for key in ("payment", "session_id"):
            qp.pop(key, None)
        st.query_params.from_dict(qp)
    except Exception:
        pass


def is_payment_verified() -> bool:
    """Quick check: user completed checkout in this session."""
    if not st.session_state.get("payment_verified"):
        return False
    return bool(st.session_state.get("stripe_checkout_session_id"))


def require_payment() -> bool:
    """Re-verify with Stripe before report generation, PDF export, or regenerate.

    Invalidates local payment_verified if Stripe no longer reports 'paid'.
    """
    if not is_payment_verified():
        return False

    session_id = st.session_state.get("stripe_checkout_session_id", "")
    try:
        paid = verify_checkout_session(session_id)
        if not paid:
            st.session_state.payment_verified = False
        return paid
    except StripePaymentError:
        st.session_state.payment_verified = False
        return False


def clear_payment_success_screen() -> None:
    """Hide the one-time post-payment welcome screen after report is ready."""
    st.session_state.show_payment_success_screen = False


def get_order_reference() -> str:
    ref = st.session_state.get("payment_order_ref")
    if ref:
        return ref
    session_id = st.session_state.get("stripe_checkout_session_id", "")
    return format_order_reference(session_id) if session_id else "N/A"


def start_checkout_redirect(checkout_url: str) -> None:
    """Redirect browser to Stripe's hosted Checkout page."""
    st.session_state.payment_cancelled = False
    safe_url = checkout_url.replace('"', "%22")
    st.markdown(
        f'<meta http-equiv="refresh" content="0;url={safe_url}">',
        unsafe_allow_html=True,
    )
    st.info("Redirecting to secure Stripe checkout…")
    st.link_button(
        "Continue to Secure Checkout ($25)",
        checkout_url,
        type="primary",
        use_container_width=True,
    )


def retry_checkout_from_saved_form() -> None:
    """Shared helper: create a new Checkout session without re-entering the form."""
    from services.stripe_payment import StripePaymentError, create_checkout_session

    try:
        checkout_url, session_id = create_checkout_session()
        st.session_state.stripe_checkout_session_id = session_id
        st.session_state.payment_message = None
        st.session_state.payment_cancelled = False
        start_checkout_redirect(checkout_url)
    except StripePaymentError as exc:
        st.error(str(exc))
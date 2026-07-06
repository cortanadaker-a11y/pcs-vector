"""Handle Stripe Checkout return URLs and payment session state.

Post-payment form restore priority (most reliable first):
  1. form_data already in Streamlit session (same browser tab survived redirect)
  2. checkout_form_backups in Streamlit session (pre-redirect in-browser copy)
  3. Server-side store keyed by stripe_checkout_session_id
  4. Server-side draft keyed by pcs_draft in Stripe metadata
  5. Stripe Checkout / PaymentIntent metadata unpack
"""

from __future__ import annotations

import json
import logging
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from components.form_state import apply_restored_form_data, get_form_value
from components.sidebar import set_page
from services.form_persistence import finalize_restored_form
from services.stripe_payment import (
    StripePaymentError,
    format_order_reference,
    get_checkout_receipt,
    restore_form_data_from_checkout,
    verify_checkout_session,
)

logger = logging.getLogger(__name__)


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
        "form_restore_failed": False,
        "customer_email": None,
        "delivery_email": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _query_param(key: str, default: str = "") -> str:
    """Read a single query param value across Streamlit versions."""
    value = st.query_params.get(key, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value or default


def save_checkout_form_backup(session_id: str, form_data: dict) -> None:
    """Keep a session-scoped copy keyed by Checkout session ID."""
    backups = st.session_state.setdefault("checkout_form_backups", {})
    backups[session_id] = form_data.copy()


def _restore_from_session_backup(session_id: str) -> bool:
    backups = st.session_state.get("checkout_form_backups", {})
    restored = backups.get(session_id)
    if restored:
        finalized = finalize_restored_form(restored) or restored
        if finalized.get("form_submitted"):
            return _apply_restored_payload(session_id, finalized)
    return False


def _apply_restored_payload(session_id: str, restored: dict) -> bool:
    finalized = finalize_restored_form(restored) or restored
    if not finalized or not finalized.get("form_submitted"):
        return False

    apply_restored_form_data(finalized)
    save_checkout_form_backup(session_id, finalized)
    from components.report_delivery import sync_delivery_email_from_form

    sync_delivery_email_from_form()
    st.session_state.form_restore_failed = False
    return True


def restore_form_data_after_payment(session_id: str, *, force_external: bool = False) -> bool:
    """Restore submitted form answers after Stripe redirect.

    When force_external=True (recovery / order lookup), skip in-browser shortcuts
    and reload from server storage + Stripe — the paths that survive a new tab.
    """
    if not session_id:
        return False

    # 1) Same Streamlit session still has the submitted form (best case).
    if not force_external and get_form_value("form_submitted"):
        st.session_state.form_restore_failed = False
        return True

    # 2) Pre-redirect in-browser copy (fast, no network).
    if not force_external and _restore_from_session_backup(session_id):
        return True

    # 3–5) Server store → draft → Stripe metadata.
    restored: dict | None = None
    try:
        restored = restore_form_data_from_checkout(session_id)
    except StripePaymentError as exc:
        logger.warning("External restore failed for %s: %s", session_id, exc)

    if _apply_restored_payload(session_id, restored or {}):
        return True

    # Retry in-browser backup after external paths (handles ordering edge cases).
    if not force_external and _restore_from_session_backup(session_id):
        return True

    return False


def activate_paid_order(
    session_id: str,
    *,
    order_reference: str = "",
    amount_paid: str = "",
    customer_email: str = "",
) -> bool:
    """Bind a verified paid Stripe order into this browser session."""
    from services.email_delivery import normalize_email

    st.session_state.payment_verified = True
    st.session_state.stripe_checkout_session_id = session_id
    st.session_state.payment_order_ref = order_reference or format_order_reference(session_id)
    if amount_paid:
        st.session_state.payment_amount_display = amount_paid
    st.session_state.payment_cancelled = False
    if not st.session_state.get("payment_completed_at"):
        st.session_state.payment_completed_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    normalized_email = normalize_email(customer_email)
    if normalized_email:
        st.session_state.customer_email = normalized_email
        if not st.session_state.get("delivery_email"):
            st.session_state.delivery_email = normalized_email

    restored = restore_form_data_after_payment(session_id, force_external=True)
    st.session_state.form_restore_failed = not restored
    return restored


def sync_payment_receipt(session_id: str | None = None) -> None:
    """Refresh order reference and amount from Stripe when session state is incomplete."""
    session_id = session_id or st.session_state.get("stripe_checkout_session_id", "")
    if not session_id:
        return
    try:
        receipt = get_checkout_receipt(session_id)
    except StripePaymentError:
        return
    st.session_state.payment_order_ref = receipt["order_reference"]
    if receipt.get("amount_paid"):
        st.session_state.payment_amount_display = receipt["amount_paid"]
    if receipt.get("customer_email"):
        from services.email_delivery import normalize_email

        email = normalize_email(receipt["customer_email"])
        if email:
            st.session_state.customer_email = email
            if not st.session_state.get("delivery_email"):
                st.session_state.delivery_email = email


def attempt_generate_from_order_reference() -> bool:
    """Recovery path: re-verify payment and reload form data from all external stores."""
    if not require_payment():
        return False

    session_id = st.session_state.get("stripe_checkout_session_id", "")
    if not session_id:
        return False

    sync_payment_receipt(session_id)

    if restore_form_data_after_payment(session_id, force_external=True):
        st.session_state.report_markdown = None
        st.session_state.report_error = None
        return True

    st.session_state.form_restore_failed = True
    return False


def ensure_form_data_restored() -> bool:
    """Best-effort restore of form data for a verified payment in this session."""
    if get_form_value("form_submitted"):
        return True
    session_id = st.session_state.get("stripe_checkout_session_id", "")
    if not session_id or not st.session_state.get("payment_verified"):
        return False
    return restore_form_data_after_payment(session_id)


def _set_payment_message(message: str | None, msg_type: str = "info") -> None:
    st.session_state.payment_message = message
    st.session_state.payment_message_type = msg_type


def handle_payment_callback() -> None:
    """Process Stripe success/cancel query params on every app load (app.py calls this early)."""
    payment = _query_param("payment")
    if not payment:
        return

    clear_checkout_redirect()

    if payment == "success":
        session_id = _query_param("session_id", "")
        try:
            if verify_checkout_session(session_id):
                receipt = get_checkout_receipt(session_id)
                st.session_state.payment_verified = True
                st.session_state.stripe_checkout_session_id = session_id
                st.session_state.payment_order_ref = receipt["order_reference"]
                st.session_state.payment_amount_display = receipt["amount_paid"]
                if receipt.get("customer_email"):
                    from services.email_delivery import normalize_email

                    email = normalize_email(receipt["customer_email"])
                    if email:
                        st.session_state.customer_email = email
                        if not st.session_state.get("delivery_email"):
                            st.session_state.delivery_email = email
                st.session_state.payment_completed_at = datetime.now().strftime(
                    "%B %d, %Y at %I:%M %p"
                )
                st.session_state.payment_cancelled = False
                st.session_state.report_markdown = None
                st.session_state.report_error = None
                st.session_state._auto_recovery_attempted = False

                restored = restore_form_data_after_payment(session_id)
                if not restored:
                    restored = restore_form_data_after_payment(session_id, force_external=True)

                st.session_state.form_restore_failed = not restored
                set_page("report")
                st.session_state._sync_nav_from_page = True
                if restored:
                    _set_payment_message(None, "success")
                else:
                    _set_payment_message(
                        "Payment confirmed. We are restoring your answers — "
                        "your report will generate automatically when ready.",
                        "info",
                    )
            else:
                st.session_state.payment_verified = False
                _set_payment_message(
                    "Payment is still processing. Wait a moment and refresh, or try checkout again.",
                    "warning",
                )
                set_page("input")
        except StripePaymentError as exc:
            st.session_state.payment_verified = False
            _set_payment_message(str(exc), "error")
            set_page("input")

    elif payment == "cancelled":
        st.session_state.payment_verified = False
        st.session_state.payment_cancelled = True
        set_page("input")
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
    """Re-verify with Stripe before report generation, PDF export, or regenerate."""
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


def get_order_reference() -> str:
    ref = st.session_state.get("payment_order_ref")
    if ref:
        return ref
    session_id = st.session_state.get("stripe_checkout_session_id", "")
    return format_order_reference(session_id) if session_id else "N/A"


def queue_checkout_redirect(checkout_url: str, session_id: str) -> None:
    """Save checkout details and rerun so redirect runs before the form re-renders."""
    from services.checkout_form_store import save_checkout_form

    st.session_state.payment_cancelled = False
    st.session_state.stripe_checkout_session_id = session_id
    st.session_state.payment_message = None
    st.session_state.checkout_redirect_url = checkout_url
    form_data = st.session_state.get("form_data")
    if form_data and form_data.get("form_submitted"):
        save_checkout_form_backup(session_id, form_data)
        # Re-save to server immediately before redirect (belt-and-suspenders).
        save_checkout_form(session_id, form_data)
    st.rerun()


def clear_checkout_redirect() -> None:
    """Clear any pending Stripe redirect state."""
    st.session_state.pop("checkout_redirect_url", None)


def render_checkout_redirect() -> bool:
    """Render Stripe redirect UI. Returns True when a redirect is pending."""
    checkout_url = st.session_state.get("checkout_redirect_url")
    if not checkout_url:
        return False

    st.markdown("## Redirecting to secure checkout")
    st.info("Taking you to Stripe to complete your $25 payment…")

    url_js = json.dumps(checkout_url)
    components.html(
        f"""<!DOCTYPE html>
        <html><body>
        <script>
            (function() {{
                var target = {url_js};
                try {{
                    window.top.location.href = target;
                }} catch (err) {{
                    window.location.href = target;
                }}
            }})();
        </script>
        </body></html>""",
        height=0,
    )
    st.link_button(
        "Continue to Secure Checkout ($25)",
        checkout_url,
        type="primary",
        use_container_width=True,
    )
    st.caption("If you are not redirected automatically, click the button above.")
    return True


def retry_checkout_from_saved_form() -> None:
    """Shared helper: create a new Checkout session without re-entering the form."""
    from services.stripe_payment import StripePaymentError, create_checkout_session

    form_data = st.session_state.get("form_data")
    if not form_data or not form_data.get("form_submitted"):
        st.error("Complete the form before retrying payment.")
        return

    try:
        checkout_url, session_id = create_checkout_session(form_data)
        queue_checkout_redirect(checkout_url, session_id)
    except StripePaymentError as exc:
        st.error(str(exc))
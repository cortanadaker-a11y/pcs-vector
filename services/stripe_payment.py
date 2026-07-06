"""Stripe Checkout integration for PCS Vector.

Payment flow (Streamlit + hosted Checkout):
  1. User submits form → we save form_data to session_state (report NOT generated yet).
  2. create_checkout_session() stores form_data server-side (session_id key) AND in
     Stripe metadata (backup), then opens hosted payment ($25).
  3. On success, Stripe redirects to APP_BASE_URL/?payment=success&session_id=...
  4. handle_payment_callback() verifies payment, then restores form_data:
       server store → Stripe metadata → in-browser session backup.
  5. Only after payment_verified=True does the report page call Grok + enable PDF.
"""

from __future__ import annotations

import logging
import secrets

import stripe

logger = logging.getLogger(__name__)

from services.checkout_form_store import (
    load_checkout_draft,
    load_checkout_form,
    save_checkout_draft,
    save_checkout_form,
)
from services.order_lookup import save_order_index
from services.form_persistence import (
    normalize_stripe_metadata,
    pack_form_data_for_stripe,
    unpack_form_data_from_stripe,
    verify_packed_metadata,
)
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


def create_checkout_session(form_data: dict | None = None) -> tuple[str, str]:
    """Create a hosted Stripe Checkout session.

    Form data is stored in two places for post-payment restore:
      1. Server-side store keyed by session_id (primary — no size limits)
      2. Stripe Checkout + PaymentIntent metadata (backup)

    Returns:
        (checkout_url, session_id) — redirect the user to checkout_url.
    """
    _configure_stripe()

    # Stripe substitutes {CHECKOUT_SESSION_ID} on redirect after payment.
    base_url = get_app_base_url()
    success_url = f"{base_url}/?payment=success&session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{base_url}/?payment=cancelled"

    draft_id = secrets.token_hex(16) if form_data else ""
    server_backup_ok = False

    if form_data:
        # Save BEFORE Stripe session creation so we have a restore key even if
        # the post-create session_id save fails (multi-worker / ephemeral disk).
        server_backup_ok = save_checkout_draft(draft_id, form_data)

    metadata = (
        pack_form_data_for_stripe(form_data)
        if form_data
        else {"product": "pcs_vector_report"}
    )
    if draft_id:
        metadata["pcs_draft"] = draft_id

    metadata_ok = True
    if form_data:
        metadata_ok = verify_packed_metadata(metadata, form_data)
        if not metadata_ok and not server_backup_ok:
            raise StripePaymentError(
                "Could not prepare your form answers for checkout. "
                "Please try again."
            )
        if not metadata_ok:
            logger.warning(
                "Stripe metadata round-trip check failed for draft %s; "
                "relying on server-side draft/session storage.",
                draft_id,
            )

    checkout_kwargs: dict = {}
    if form_data:
        email = (form_data.get("email") or "").strip()
        if email:
            checkout_kwargs["customer_email"] = email

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
            metadata=metadata,
            # Duplicate form payload on the PaymentIntent as a second restore path.
            payment_intent_data={"metadata": metadata},
            **checkout_kwargs,
        )
    except stripe.error.StripeError as exc:
        raise StripePaymentError(f"Could not start checkout: {exc.user_message or exc}") from exc

    if not session.url or not session.id:
        raise StripePaymentError("Stripe returned an invalid checkout session.")

    # Map PCS-XXXXXXXX → session_id for public order lookup in new browser sessions.
    save_order_index(session.id)

    # Also key the same payload by Checkout session_id for post-payment restore.
    if form_data:
        session_saved = save_checkout_form(session.id, form_data)
        server_backup_ok = server_backup_ok or session_saved
        if not server_backup_ok:
            logger.warning(
                "Server-side form backup failed for session %s (draft %s); "
                "restore will rely on Stripe metadata.",
                session.id,
                draft_id,
            )

    if form_data:
        try:
            retrieved = stripe.checkout.Session.retrieve(session.id)
            stored = normalize_stripe_metadata(retrieved.metadata)
            if not verify_packed_metadata(stored, form_data):
                logger.warning(
                    "Stripe session %s metadata mismatch after retrieve; "
                    "post-payment restore will rely on server-side store.",
                    session.id,
                )
        except stripe.error.StripeError as exc:
            logger.warning("Could not verify stored checkout metadata: %s", exc)

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


def _unpack_form_from_session_object(session: stripe.checkout.Session) -> dict | None:
    """Try session metadata, then PaymentIntent metadata."""
    restored = unpack_form_data_from_stripe(normalize_stripe_metadata(session.metadata))
    if restored and restored.get("form_submitted"):
        return restored

    payment_intent = session.payment_intent
    if not payment_intent:
        return None

    if isinstance(payment_intent, str):
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent)
        except stripe.error.StripeError as exc:
            logger.warning("Could not load PaymentIntent for restore: %s", exc)
            return None

    restored = unpack_form_data_from_stripe(normalize_stripe_metadata(payment_intent.metadata))
    if restored and restored.get("form_submitted"):
        logger.info("Restored form data from PaymentIntent metadata.")
        return restored
    return None


def restore_form_data_from_stripe_metadata(session_id: str) -> dict | None:
    """Load form answers from Stripe Checkout / PaymentIntent metadata (backup path)."""
    if not session_id:
        return None

    _configure_stripe()
    try:
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=["payment_intent"],
        )
    except stripe.error.StripeError as exc:
        raise StripePaymentError(
            f"Could not restore form data: {exc.user_message or exc}"
        ) from exc

    restored = _unpack_form_from_session_object(session)
    if restored:
        logger.info("Restored form data from Stripe metadata for session %s", session_id)
    return restored


def restore_form_data_from_checkout(session_id: str) -> dict | None:
    """Restore form answers for a paid Checkout session.

    Priority:
      1. Server-side store keyed by session_id
      2. Server-side draft keyed by pcs_draft in Stripe metadata
      3. Stripe session / PaymentIntent metadata unpack
    """
    if not session_id:
        return None

    stored = load_checkout_form(session_id)
    if stored:
        logger.info("Restored form data from server-side store for session %s", session_id)
        return stored

    _configure_stripe()
    try:
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=["payment_intent"],
        )
    except stripe.error.StripeError as exc:
        raise StripePaymentError(
            f"Could not restore form data: {exc.user_message or exc}"
        ) from exc

    safe_metadata = normalize_stripe_metadata(session.metadata)
    draft_id = safe_metadata.get("pcs_draft", "")
    if draft_id:
        draft_data = load_checkout_draft(draft_id)
        if draft_data:
            logger.info(
                "Restored form data from server-side draft %s for session %s",
                draft_id,
                session_id,
            )
            save_checkout_form(session_id, draft_data)
            return draft_data

    restored = _unpack_form_from_session_object(session)
    if restored:
        logger.info("Restored form data from Stripe metadata for session %s", session_id)
        save_checkout_form(session_id, restored)
        if draft_id:
            save_checkout_draft(draft_id, restored)
        return restored

    return None


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
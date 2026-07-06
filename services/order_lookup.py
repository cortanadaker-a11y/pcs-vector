"""Resolve human-friendly Order References (PCS-XXXXXXXX) to Stripe Checkout sessions.

Users see a short order reference after payment. This module maps that reference back
to the full Checkout session_id so they can retrieve a report in a new browser tab.

Lookup priority:
  1. Local order index written at checkout time (fast, reliable)
  2. Stripe Checkout session search by matching reference suffix (fallback)
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

ORDER_REF_PATTERN = re.compile(r"^PCS-[A-Z0-9]{8}$")
DEFAULT_TTL_SECONDS = 72 * 3600  # match checkout form store TTL
_STRIPE_SEARCH_MAX_SESSIONS = 250


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_index_dir() -> Path:
    index_dir = _project_root() / "data" / "order_index"
    index_dir.mkdir(parents=True, exist_ok=True)
    return index_dir


def normalize_order_reference(raw: str) -> str | None:
    """Normalize user input to PCS-XXXXXXXX or return None if invalid."""
    if not raw:
        return None

    cleaned = raw.strip().upper().replace(" ", "").replace("_", "-")
    if cleaned.startswith("PCS") and not cleaned.startswith("PCS-"):
        cleaned = cleaned.replace("PCS", "PCS-", 1)

    if not cleaned.startswith("PCS-"):
        suffix = re.sub(r"[^A-Z0-9]", "", cleaned)
        if len(suffix) == 8:
            cleaned = f"PCS-{suffix}"
        else:
            return None

    return cleaned if ORDER_REF_PATTERN.match(cleaned) else None


def save_order_index(session_id: str, *, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> bool:
    """Record order reference → session_id mapping at checkout creation."""
    from services.stripe_payment import format_order_reference

    order_ref = format_order_reference(session_id)
    if order_ref == "N/A":
        return False

    path = get_index_dir() / f"{order_ref}.json"
    payload = {
        "order_reference": order_ref,
        "session_id": session_id,
        "saved_at": time.time(),
        "ttl_seconds": ttl_seconds,
    }
    try:
        temp_path = path.with_suffix(".json.tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, separators=(",", ":"), sort_keys=True)
        temp_path.replace(path)
        return True
    except OSError as exc:
        logger.warning("Could not save order index for %s: %s", order_ref, exc)
        return False


def _read_index_payload(order_ref: str) -> dict[str, Any] | None:
    path = get_index_dir() / f"{order_ref}.json"
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload if isinstance(payload, dict) else None
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not read order index %s: %s", order_ref, exc)
        return None


def _index_expired(payload: dict[str, Any], *, ttl_seconds: int) -> bool:
    saved_at = float(payload.get("saved_at", 0) or 0)
    stored_ttl = int(payload.get("ttl_seconds", ttl_seconds) or ttl_seconds)
    if saved_at <= 0:
        return True
    return time.time() > saved_at + stored_ttl


def resolve_session_id_from_index(
    order_ref: str,
    *,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> str | None:
    """Load session_id from the local order index file."""
    payload = _read_index_payload(order_ref)
    if not payload:
        return None
    if _index_expired(payload, ttl_seconds=ttl_seconds):
        try:
            (get_index_dir() / f"{order_ref}.json").unlink(missing_ok=True)
        except OSError:
            pass
        return None
    session_id = payload.get("session_id")
    return str(session_id) if session_id else None


def resolve_session_id_from_stripe(order_ref: str) -> str | None:
    """Search recent paid Stripe Checkout sessions for a matching order reference."""
    import stripe

    from services.stripe_config import StripeConfigError, get_stripe_secret_key
    from services.stripe_payment import format_order_reference

    try:
        stripe.api_key = get_stripe_secret_key()
    except StripeConfigError as exc:
        logger.warning("Stripe not configured for order lookup: %s", exc)
        return None

    created_gte = int(time.time()) - DEFAULT_TTL_SECONDS
    scanned = 0

    try:
        sessions = stripe.checkout.Session.list(
            limit=100,
            status="complete",
            created={"gte": created_gte},
        )
        for session in sessions.auto_paging_iter():
            scanned += 1
            if scanned > _STRIPE_SEARCH_MAX_SESSIONS:
                break
            if session.payment_status != "paid":
                continue
            if format_order_reference(session.id) == order_ref:
                logger.info("Resolved %s via Stripe search → %s", order_ref, session.id)
                save_order_index(session.id)
                return session.id
    except stripe.error.StripeError as exc:
        logger.warning("Stripe order search failed for %s: %s", order_ref, exc)

    return None


def resolve_session_id_from_order_reference(order_ref: str) -> str | None:
    """Resolve PCS-XXXXXXXX to a Checkout session_id."""
    normalized = normalize_order_reference(order_ref)
    if not normalized:
        return None

    session_id = resolve_session_id_from_index(normalized)
    if session_id:
        return session_id

    return resolve_session_id_from_stripe(normalized)


@dataclass
class OrderLookupResult:
    """Outcome of looking up an order reference."""

    success: bool
    message: str
    order_reference: str = ""
    session_id: str = ""
    payment_status: str = ""
    amount_paid: str = ""
    customer_email: str = ""


def lookup_paid_order(order_ref: str) -> OrderLookupResult:
    """Verify a paid order exists for an order reference (does not mutate session state)."""
    from services.stripe_payment import (
        StripePaymentError,
        format_order_reference,
        get_checkout_receipt,
        verify_checkout_session,
    )

    normalized = normalize_order_reference(order_ref)
    if not normalized:
        return OrderLookupResult(
            success=False,
            message="Enter a valid order reference like PCS-ABC12XYZ (from your payment confirmation).",
        )

    session_id = resolve_session_id_from_order_reference(normalized)
    if not session_id:
        return OrderLookupResult(
            success=False,
            message=(
                f"We could not find order **{normalized}**. "
                "Double-check the reference from your Stripe receipt or confirmation screen. "
                "Orders are available for 72 hours after purchase."
            ),
            order_reference=normalized,
        )

    try:
        if not verify_checkout_session(session_id):
            receipt = get_checkout_receipt(session_id)
            return OrderLookupResult(
                success=False,
                message=(
                    f"Order **{normalized}** was found but payment is not complete yet "
                    f"(status: {receipt.get('payment_status', 'unknown')}). "
                    "Wait a moment and try again."
                ),
                order_reference=normalized,
                session_id=session_id,
                payment_status=receipt.get("payment_status", ""),
            )

        receipt = get_checkout_receipt(session_id)

        return OrderLookupResult(
            success=True,
            message="Payment verified. You can generate your report — no additional charge.",
            order_reference=receipt.get("order_reference") or format_order_reference(session_id),
            session_id=session_id,
            payment_status=receipt.get("payment_status", "paid"),
            amount_paid=receipt.get("amount_paid", ""),
            customer_email=receipt.get("customer_email", ""),
        )
    except StripePaymentError as exc:
        return OrderLookupResult(
            success=False,
            message=str(exc),
            order_reference=normalized,
            session_id=session_id,
        )
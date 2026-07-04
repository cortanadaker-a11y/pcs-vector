"""Stripe and app URL configuration for PCS Vector.

API keys are NEVER hardcoded. Load order:
  1. `.streamlit/secrets.toml`  (local dev + Streamlit Cloud App Secrets)
  2. Environment variables

Copy secrets.toml.example → secrets.toml (local) or paste into Streamlit Cloud Secrets.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)


class StripeConfigError(Exception):
    """Raised when required Stripe configuration is missing."""


REPORT_PRICE_CENTS = 2500  # $25.00 USD
REPORT_PRICE_DISPLAY = "$25"
REPORT_PRODUCT_NAME = "PCS Vector Strategic Plan"
REPORT_PRODUCT_DESCRIPTION = (
    "Personalized 8-section PCS strategic plan with PDF export for Army families."
)


def _from_streamlit_secrets(key_path: str) -> str | None:
    """Safely read a nested key from st.secrets, e.g. 'stripe.secret_key'."""
    try:
        import streamlit as st

        node = st.secrets
        for part in key_path.split("."):
            node = node[part]
        value = str(node).strip() if node else ""
        return value or None
    except Exception:
        return None


def _runtime_app_url() -> str | None:
    """Detect the public app URL at runtime (works on Streamlit Community Cloud)."""
    try:
        import streamlit as st

        if hasattr(st, "context") and hasattr(st.context, "headers"):
            headers = st.context.headers
            host = headers.get("X-Forwarded-Host") or headers.get("Host")
            proto = headers.get("X-Forwarded-Proto", "https")
            if host and "localhost" not in host:
                return f"{proto}://{host}".rstrip("/")
    except Exception:
        pass
    return None


def get_stripe_secret_key() -> str:
    """Resolve Stripe secret key from secrets.toml or environment."""
    key = _from_streamlit_secrets("stripe.secret_key") or os.environ.get(
        "STRIPE_SECRET_KEY", ""
    ).strip()
    if not key:
        raise StripeConfigError(
            "Stripe isn't configured yet. Add [stripe] secret_key to Streamlit Secrets "
            "(Settings → Secrets) or see DEPLOYMENT.md / PRELAUNCH.md."
        )
    return key


def get_stripe_publishable_key() -> str:
    """Resolve Stripe publishable key from secrets.toml or environment."""
    key = _from_streamlit_secrets("stripe.publishable_key") or os.environ.get(
        "STRIPE_PUBLISHABLE_KEY", ""
    ).strip()
    if not key:
        raise StripeConfigError(
            "Stripe publishable key not found. Add [stripe] publishable_key to Streamlit Secrets."
        )
    return key


def get_app_base_url() -> str:
    """Public app URL for Stripe redirect callbacks.

    Priority:
      1. secrets.toml / env (recommended — set explicitly after first deploy)
      2. Runtime detection from request headers (Streamlit Cloud fallback)
      3. localhost (local development only)
    """
    configured = (
        _from_streamlit_secrets("pcs_vector.app_url")
        or os.environ.get("PCS_VECTOR_APP_URL", "")
    ).strip().rstrip("/")

    if configured:
        return configured

    runtime = _runtime_app_url()
    if runtime:
        logger.info("Using runtime-detected app URL for Stripe redirects: %s", runtime)
        return runtime

    return "http://localhost:8501"
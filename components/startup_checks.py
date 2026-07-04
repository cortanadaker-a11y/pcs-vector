"""Startup configuration checks for local dev and Streamlit Cloud."""

from __future__ import annotations

import streamlit as st

from services.grok_config import GrokConfigError, get_grok_api_key
from services.stripe_config import StripeConfigError, get_app_base_url, get_stripe_secret_key


def check_configuration() -> dict[str, bool | str]:
    """Return configuration status for required secrets."""
    status: dict[str, bool | str] = {
        "stripe_secret": False,
        "grok_api": False,
        "app_url": get_app_base_url(),
        "errors": [],
    }

    try:
        get_stripe_secret_key()
        status["stripe_secret"] = True
    except StripeConfigError as exc:
        status["errors"].append(str(exc))

    try:
        get_grok_api_key()
        status["grok_api"] = True
    except GrokConfigError as exc:
        status["errors"].append(str(exc))

    if status["app_url"] == "http://localhost:8501":
        status["errors"].append(
            "Using localhost app URL. Set pcs_vector.app_url in secrets after deploying "
            "so Stripe payment redirects work in production."
        )

    return status


def render_config_warnings() -> None:
    """Show non-blocking configuration warnings in the sidebar."""
    status = check_configuration()
    missing = not status["stripe_secret"] or not status["grok_api"]

    if missing:
        with st.sidebar:
            st.error("Configuration incomplete")
            for err in status["errors"]:
                if "localhost" not in err:
                    st.caption(f"• {err}")
            st.caption("See DEPLOYMENT.md for setup instructions.")
    elif any("localhost" in e for e in status["errors"]):
        with st.sidebar:
            st.warning("Set pcs_vector.app_url in secrets for production Stripe redirects.")
            st.caption(f"Current: {status['app_url']}")
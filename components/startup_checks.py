"""Startup configuration checks for local dev and Streamlit Cloud."""

from __future__ import annotations

import streamlit as st

from services.email_delivery import get_smtp_config, is_email_configured
from services.grok_config import GrokConfigError, get_grok_api_key
from services.stripe_config import StripeConfigError, get_app_base_url, get_stripe_secret_key


def check_configuration() -> dict[str, bool | str]:
    """Return configuration status for required secrets."""
    status: dict[str, bool | str] = {
        "stripe_secret": False,
        "grok_api": False,
        "email_configured": False,
        "email_from": "",
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

    if is_email_configured():
        status["email_configured"] = True
        cfg = get_smtp_config() or {}
        status["email_from"] = str(cfg.get("from_address") or "")
    else:
        status["errors"].append(
            "Email delivery is not configured. Add [email] SMTP settings in secrets "
            "so PDF reports are emailed automatically after payment."
        )

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

    with st.sidebar:
        if missing:
            st.error("Configuration incomplete")
            for err in status["errors"]:
                if "localhost" not in err and "Email delivery" not in err:
                    st.caption(f"• {err}")
            st.caption("See DEPLOYMENT.md or PRELAUNCH.md for setup.")
        elif any("localhost" in e for e in status["errors"]):
            st.warning("Set pcs_vector.app_url in secrets for production Stripe redirects.")
            st.caption(f"Current: {status['app_url']}")

        if status["email_configured"]:
            st.caption(f"📧 Email connected · {status['email_from']}")
        else:
            st.warning("PDF email not connected")
            st.caption(
                "Add `[email]` SMTP settings in Streamlit secrets "
                "(see DEPLOYMENT.md → Email delivery)."
            )
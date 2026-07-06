"""Email delivery for PCS Vector PDF reports.

PDFs are always available for on-site download after payment. Email is an additional
delivery channel when SMTP is configured in Streamlit secrets — we use the address
collected by Stripe at checkout when available.
"""

from __future__ import annotations

import logging
import os
import re
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

logger = logging.getLogger(__name__)

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmailDeliveryError(Exception):
    """Raised when report email cannot be sent."""


def _from_streamlit_secrets(key_path: str) -> str | None:
    try:
        import streamlit as st

        node = st.secrets
        for part in key_path.split("."):
            node = node[part]
        value = str(node).strip() if node else ""
        return value or None
    except Exception:
        return None


def get_smtp_config() -> dict[str, Any] | None:
    """Load SMTP settings from secrets.toml or environment. None if not configured."""
    host = _from_streamlit_secrets("email.smtp_host") or os.environ.get("PCS_EMAIL_SMTP_HOST", "").strip()
    user = _from_streamlit_secrets("email.smtp_user") or os.environ.get("PCS_EMAIL_SMTP_USER", "").strip()
    password = _from_streamlit_secrets("email.smtp_password") or os.environ.get(
        "PCS_EMAIL_SMTP_PASSWORD", ""
    ).strip()
    from_address = _from_streamlit_secrets("email.from_address") or os.environ.get(
        "PCS_EMAIL_FROM_ADDRESS", ""
    ).strip()
    port_raw = _from_streamlit_secrets("email.smtp_port") or os.environ.get("PCS_EMAIL_SMTP_PORT", "587")
    use_tls_raw = _from_streamlit_secrets("email.use_tls") or os.environ.get("PCS_EMAIL_USE_TLS", "true")

    if not host or not from_address:
        return None

    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        port = 587

    use_tls = str(use_tls_raw).strip().lower() in ("1", "true", "yes", "on")

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from_address": from_address,
        "use_tls": use_tls,
    }


def is_email_configured() -> bool:
    """True when SMTP host and from_address are available."""
    return get_smtp_config() is not None


def normalize_email(raw: str) -> str | None:
    email = (raw or "").strip().lower()
    return email if _EMAIL_PATTERN.match(email) else None


def send_report_pdf_email(
    to_email: str,
    pdf_bytes: bytes,
    *,
    order_reference: str = "",
    family_name: str = "",
    pdf_filename: str = "pcs-vector-report.pdf",
) -> None:
    """Send the generated PDF as an email attachment."""
    recipient = normalize_email(to_email)
    if not recipient:
        raise EmailDeliveryError("Enter a valid email address.")

    if not pdf_bytes:
        raise EmailDeliveryError("PDF is not ready yet — generate your report first.")

    config = get_smtp_config()
    if not config:
        raise EmailDeliveryError(
            "Email delivery is not configured on this server. "
            "Download your PDF from the report page instead."
        )

    greeting = f"Hi {family_name}," if family_name else "Hi,"
    order_line = f"\nOrder reference: {order_reference}" if order_reference else ""

    body = (
        f"{greeting}\n\n"
        "Your PCS Vector strategic plan is attached as a PDF. "
        "You can also return to the app anytime with your order reference "
        "to view or download your report again — no extra charge."
        f"{order_line}\n\n"
        "Thank you for using PCS Vector.\n"
        "— PCS Vector"
    )

    message = MIMEMultipart()
    message["Subject"] = "Your PCS Vector report (PDF attached)"
    message["From"] = config["from_address"]
    message["To"] = recipient
    message.attach(MIMEText(body, "plain", "utf-8"))

    attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    attachment.add_header("Content-Disposition", "attachment", filename=pdf_filename)
    message.attach(attachment)

    try:
        with smtplib.SMTP(config["host"], config["port"], timeout=30) as server:
            if config["use_tls"]:
                server.starttls(context=ssl.create_default_context())
            if config["user"] and config["password"]:
                server.login(config["user"], config["password"])
            server.sendmail(config["from_address"], [recipient], message.as_string())
    except (OSError, smtplib.SMTPException) as exc:
        logger.warning("Failed to email PDF to %s: %s", recipient, exc)
        raise EmailDeliveryError(
            "We could not send the email right now. Please try again or download the PDF below."
        ) from exc

    logger.info("Emailed PCS Vector PDF to %s (order %s)", recipient, order_reference or "n/a")
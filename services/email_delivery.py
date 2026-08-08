"""Email delivery for PCS Vector PDF reports.

PDFs are always available for on-site download after payment. Email is an additional
delivery channel when SMTP is configured in Streamlit secrets.
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
from email.utils import formataddr, formatdate, make_msgid, parseaddr
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
    reply_to = _from_streamlit_secrets("email.reply_to") or os.environ.get(
        "PCS_EMAIL_REPLY_TO", ""
    ).strip()
    port_raw = _from_streamlit_secrets("email.smtp_port") or os.environ.get("PCS_EMAIL_SMTP_PORT", "587")
    use_tls_raw = _from_streamlit_secrets("email.use_tls") or os.environ.get("PCS_EMAIL_USE_TLS", "true")
    use_ssl_raw = _from_streamlit_secrets("email.use_ssl") or os.environ.get("PCS_EMAIL_USE_SSL", "")

    if not host or not from_address:
        return None

    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        port = 587

    use_tls = str(use_tls_raw).strip().lower() in ("1", "true", "yes", "on")
    # Port 465/2465 = implicit SSL (Resend SMTPS). Override with email.use_ssl if set.
    if str(use_ssl_raw).strip():
        use_ssl = str(use_ssl_raw).strip().lower() in ("1", "true", "yes", "on")
    else:
        use_ssl = port in (465, 2465)

    # Resend / API-key providers: strip spaces from password
    if password:
        password = password.replace(" ", "").strip()

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "from_address": from_address,
        "reply_to": reply_to or None,
        "use_tls": use_tls and not use_ssl,
        "use_ssl": use_ssl,
        "provider": "resend" if "resend.com" in host.lower() else "smtp",
    }


def is_email_configured() -> bool:
    """True when SMTP host and from_address are available."""
    return get_smtp_config() is not None


def normalize_email(raw: str) -> str | None:
    email = (raw or "").strip().lower()
    return email if _EMAIL_PATTERN.match(email) else None


def _build_bodies(
    *,
    family_name: str,
    order_reference: str,
) -> tuple[str, str]:
    """Return (plain_text, html) bodies tuned for deliverability."""
    first = (family_name or "").strip().split()[0] if (family_name or "").strip() else ""
    greeting = f"Hi {first}," if first else "Hi,"
    order_plain = f"\nOrder reference: {order_reference}\n" if order_reference else "\n"
    order_html = (
        f'<p style="margin:12px 0;color:#454540;">Order reference: '
        f"<strong>{order_reference}</strong></p>"
        if order_reference
        else ""
    )

    plain = (
        f"{greeting}\n\n"
        "Thanks for purchasing PCS Vector. Your personalized PCS strategic plan is attached "
        "as a PDF.\n\n"
        "You can also open the app anytime with your order reference to view or download "
        "the report again — no extra charge."
        f"{order_plain}\n"
        "If this landed in spam, mark it as Not spam and add this address to your contacts "
        "so future plans arrive in your inbox.\n\n"
        "— PCS Vector\n"
        "Built For Soldiers; By Soldiers\n"
    )

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>PCS Vector</title></head>
<body style="margin:0;padding:0;background:#f4f2ee;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#1c1c1a;">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border:1px solid #e0ddd6;border-radius:12px;padding:28px 24px;">
    <p style="margin:0 0 8px 0;font-size:12px;letter-spacing:0.08em;text-transform:uppercase;color:#4a7c64;font-weight:700;">PCS Vector</p>
    <p style="margin:0 0 16px 0;font-size:16px;line-height:1.5;">{greeting}</p>
    <p style="margin:0 0 12px 0;font-size:15px;line-height:1.6;">
      Thanks for purchasing PCS Vector. Your personalized PCS strategic plan is attached as a PDF.
    </p>
    <p style="margin:0 0 12px 0;font-size:15px;line-height:1.6;">
      You can also open the app anytime with your order reference to view or download the report again — no extra charge.
    </p>
    {order_html}
    <p style="margin:16px 0 0 0;font-size:13px;line-height:1.5;color:#6b6b66;">
      If this landed in spam, mark it as Not spam and add this address to your contacts so future plans arrive in your inbox.
    </p>
    <p style="margin:20px 0 0 0;font-size:14px;line-height:1.5;">— PCS Vector<br>
    <span style="color:#6b6b66;font-size:12px;">Built For Soldiers; By Soldiers</span></p>
  </div>
</body>
</html>
"""
    return plain, html


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

    from_display, from_addr = parseaddr(config["from_address"])
    if not from_addr:
        from_addr = config["from_address"]
        from_display = "PCS Vector"
    if not from_display:
        from_display = "PCS Vector"

    reply_to = config.get("reply_to") or from_addr
    domain = from_addr.split("@")[-1] if "@" in from_addr else "localhost"

    plain, html = _build_bodies(family_name=family_name, order_reference=order_reference)

    # multipart/mixed → alternative (plain+html) + PDF attachment
    message = MIMEMultipart("mixed")
    message["Subject"] = (
        f"Your PCS Vector plan is ready — {order_reference}"
        if order_reference
        else "Your PCS Vector plan is ready"
    )
    message["From"] = formataddr((from_display, from_addr))
    message["To"] = recipient
    message["Reply-To"] = reply_to
    message["Date"] = formatdate(localtime=True)
    message["Message-ID"] = make_msgid(domain=domain)
    message["MIME-Version"] = "1.0"
    # Helps some filters treat this as a one-to-one transactional message
    message["X-Auto-Response-Suppress"] = "OOF, AutoReply"
    message["Auto-Submitted"] = "auto-generated"
    if order_reference:
        message["X-PCS-Order"] = order_reference
        # Resend SMTP: prevent duplicate sends if a retry happens
        if config.get("provider") == "resend":
            message["Resend-Idempotency-Key"] = f"pcs-vector/{order_reference}"

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(plain, "plain", "utf-8"))
    alt.attach(MIMEText(html, "html", "utf-8"))
    message.attach(alt)

    attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    attachment.add_header("Content-Disposition", "attachment", filename=pdf_filename)
    attachment.add_header("Content-Type", "application/pdf", name=pdf_filename)
    message.attach(attachment)

    try:
        _send_via_smtp(config, from_addr, recipient, message.as_string())
    except (OSError, smtplib.SMTPException) as exc:
        logger.warning("Failed to email PDF to %s: %s", recipient, exc)
        detail = str(exc)
        hint = ""
        if config.get("provider") == "resend":
            hint = (
                " Resend tip: From must be on a verified domain (or onboarding@resend.dev "
                "for testing), and smtp_password must be your API key (user = resend)."
            )
        raise EmailDeliveryError(
            "We could not send the email right now. Please try again or download the PDF below."
            + (f" ({detail})" if detail else "")
            + hint
        ) from exc

    logger.info(
        "Emailed PCS Vector PDF to %s (order %s, provider=%s)",
        recipient,
        order_reference or "n/a",
        config.get("provider", "smtp"),
    )


def _send_via_smtp(
    config: dict[str, Any],
    from_addr: str,
    recipient: str,
    payload: str,
) -> None:
    """Connect via SSL (465) or STARTTLS (587) and send."""
    ctx = ssl.create_default_context()
    if config.get("use_ssl"):
        with smtplib.SMTP_SSL(config["host"], config["port"], timeout=30, context=ctx) as server:
            if config["user"] and config["password"]:
                server.login(config["user"], config["password"])
            server.sendmail(from_addr, [recipient], payload)
        return

    with smtplib.SMTP(config["host"], config["port"], timeout=30) as server:
        if config.get("use_tls"):
            server.starttls(context=ctx)
        if config["user"] and config["password"]:
            server.login(config["user"], config["password"])
        server.sendmail(from_addr, [recipient], payload)

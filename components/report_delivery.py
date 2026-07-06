"""Automatic PDF email delivery after successful report generation (Option B)."""

from __future__ import annotations

import streamlit as st

from components.payment_handler import get_order_reference
from services.email_delivery import (
    EmailDeliveryError,
    is_email_configured,
    normalize_email,
    send_report_pdf_email,
)


def get_preferred_delivery_email() -> str:
    """Email for PDF delivery: form field → session override → Stripe checkout email."""
    form_data = st.session_state.get("form_data", {})
    form_email = normalize_email(form_data.get("email", ""))
    if form_email:
        return form_email

    override = st.session_state.get("delivery_email", "")
    if override:
        return override

    return st.session_state.get("customer_email", "") or ""


def sync_delivery_email_from_form() -> None:
    """Keep session delivery_email aligned with the form email field."""
    form_data = st.session_state.get("form_data", {})
    email = normalize_email(form_data.get("email", ""))
    if email:
        st.session_state.delivery_email = email


def _email_already_sent(order_ref: str) -> bool:
    return st.session_state.get("pdf_email_sent_for_order") == order_ref


def _mark_email_sent(order_ref: str, recipient: str) -> None:
    st.session_state.pdf_email_sent_for_order = order_ref
    st.session_state.delivery_email = recipient


def auto_email_pdf_after_generation(pdf_bytes: bytes, pdf_filename: str) -> bool:
    """Automatically email the PDF once per order after successful report generation."""
    if not pdf_bytes:
        return False

    order_ref = get_order_reference()
    if _email_already_sent(order_ref):
        return True

    sync_delivery_email_from_form()
    recipient = normalize_email(get_preferred_delivery_email())
    if not recipient:
        st.session_state.pdf_email_delivery_error = (
            "No email address on file. Enter your email on the form or use **Retrieve Report**."
        )
        return False

    if not is_email_configured():
        st.session_state.pdf_email_delivery_error = (
            "Automatic email is not configured on this server. Download your PDF below."
        )
        return False

    form_data = st.session_state.get("form_data", {})
    family_name = (
        f"{form_data.get('first_name', '').strip()} {form_data.get('last_name', '').strip()}".strip()
    )

    try:
        send_report_pdf_email(
            recipient,
            pdf_bytes,
            order_reference=order_ref,
            family_name=family_name,
            pdf_filename=pdf_filename,
        )
    except EmailDeliveryError as exc:
        st.session_state.pdf_email_delivery_error = str(exc)
        return False

    _mark_email_sent(order_ref, recipient)
    st.session_state.pop("pdf_email_delivery_error", None)
    return True


def render_pdf_delivery_status(pdf_bytes: bytes, pdf_filename: str) -> None:
    """Show automatic email delivery status and a resend option if needed."""
    order_ref = get_order_reference()
    preferred = get_preferred_delivery_email()
    auto_sent = _email_already_sent(order_ref)
    delivery_error = st.session_state.get("pdf_email_delivery_error")

    with st.container(border=True):
        st.markdown("### PDF delivery")
        st.markdown(
            "After your report is generated, your **PDF is automatically emailed** to the address "
            "you entered on the form. You can also download it below anytime."
        )

        if auto_sent and preferred:
            st.success(
                f"Your PDF has been emailed to **{preferred}** (order **{order_ref}**).",
                icon="📧",
            )
            st.caption("Check spam/junk if it does not arrive within a few minutes.")
        elif delivery_error:
            st.warning(delivery_error, icon="⚠️")

        if not is_email_configured():
            st.info(
                "Email delivery requires server configuration. Save your order reference "
                f"**{order_ref}** and download the PDF below.",
                icon="ℹ️",
            )
            return

        if auto_sent:
            if st.button("Resend PDF to my email", use_container_width=True, key="resend_pdf_email_btn"):
                st.session_state.pdf_email_sent_for_order = None
                if auto_email_pdf_after_generation(pdf_bytes, pdf_filename):
                    st.rerun()
            return

        # Auto-send failed or was skipped — offer one-click resend.
        if pdf_bytes and preferred and st.button(
            "Send PDF to my email now",
            type="primary",
            use_container_width=True,
            key="send_pdf_email_btn",
        ):
            if auto_email_pdf_after_generation(pdf_bytes, pdf_filename):
                st.rerun()
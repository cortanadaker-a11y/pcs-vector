"""Post-payment confirmation and report-generation loading UI."""

from __future__ import annotations

import streamlit as st

from components.payment_handler import get_order_reference
from services.stripe_payment import get_price_display


def render_payment_confirmation_banner() -> None:
    """Compact confirmation shown above the report after payment and generation succeed."""
    order_ref = get_order_reference()
    amount = st.session_state.get("payment_amount_display") or get_price_display()
    completed_at = st.session_state.get("payment_completed_at", "")

    caption = f"Order **{order_ref}** · **{amount}** paid"
    if completed_at:
        caption += f" · {completed_at}"

    st.success(f"Payment confirmed. {caption}", icon="✅")


def generate_report_with_loading(generate_fn) -> str | None:
    """Run Grok report generation inside a visible loading status block."""
    with st.status(
        "Generating your personalized PCS Vector report…",
        expanded=True,
    ) as status:
        st.write("Reviewing your move details and priorities…")
        st.write("Analyzing housing, BAH, and local neighborhoods…")
        st.write("Building spouse career and school recommendations…")
        st.write("Finalizing your action plan and timeline…")
        try:
            report = generate_fn()
            status.update(
                label="Report ready!",
                state="complete",
                expanded=False,
            )
            return report
        except Exception as exc:
            status.update(
                label="Report generation failed",
                state="error",
                expanded=True,
            )
            raise exc
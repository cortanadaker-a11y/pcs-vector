"""Post-payment confirmation and report-generation loading UI."""

from __future__ import annotations

import streamlit as st

from components.payment_handler import (
    attempt_generate_from_order_reference,
    get_order_reference,
    sync_payment_receipt,
)
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def render_payment_confirmation_banner() -> None:
    """Compact confirmation shown above the report after payment and generation succeed."""
    order_ref = get_order_reference()
    amount = st.session_state.get("payment_amount_display") or get_price_display()
    completed_at = st.session_state.get("payment_completed_at", "")

    caption = f"Order **{order_ref}** · **{amount}** paid"
    if completed_at:
        caption += f" · {completed_at}"

    delivery_email = st.session_state.get("form_data", {}).get("email", "")
    email_note = f" · PDF will be emailed to **{delivery_email}**" if delivery_email else ""
    st.success(f"Payment confirmed. {caption}{email_note}", icon="✅")


def render_order_reference_recovery() -> None:
    """Clean fallback when payment succeeded but form answers were not restored yet."""
    sync_payment_receipt()

    order_ref = get_order_reference()
    amount = st.session_state.get("payment_amount_display") or get_price_display()
    completed_at = st.session_state.get("payment_completed_at", "")

    st.success("Payment confirmed — your order is ready.", icon="✅")

    with st.container(border=True):
        st.markdown("### Order Reference")
        st.markdown(f"## `{order_ref}`")
        st.caption(f"{amount} paid" + (f" · {completed_at}" if completed_at else ""))

        st.markdown(
            "Your payment is complete. Use the button below to pull your saved answers "
            "from this order and generate your personalized PCS report — your PDF will be "
            "emailed automatically — **no additional charge**."
        )

        if st.button(
            "Generate my report now",
            type="primary",
            use_container_width=True,
            key="recovery_generate_report",
        ):
            with st.spinner("Restoring your answers and preparing your report…"):
                if attempt_generate_from_order_reference():
                    st.rerun()
                else:
                    st.error(
                        "We could not restore your form answers from this order. "
                        "Please try again in a moment, or use **Retrieve Report** with your "
                        f"order reference **{order_ref}**."
                    )

        st.caption(
            "Lost this tab? Open **Retrieve Report** in the sidebar (or below) and enter "
            f"**{order_ref}** — you will not be charged again."
        )
        if st.button(
            "Open Retrieve Report page",
            use_container_width=True,
            key="recovery_open_lookup",
        ):
            st.session_state.lookup_order_input = order_ref
            navigate_to("retrieve")


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
"""Post-payment success and report-generation loading UI."""

from __future__ import annotations

import streamlit as st

from components.payment_handler import get_order_reference
from services.stripe_payment import get_price_display


def render_payment_success_screen() -> None:
    """Show confirmation after Stripe payment, before/during Grok report generation."""
    order_ref = get_order_reference()
    amount = st.session_state.get("payment_amount_display") or get_price_display()
    completed_at = st.session_state.get("payment_completed_at", "")

    st.markdown(
        f"""
        <div class="pcs-payment-success">
            <div class="pcs-payment-success-icon">✓</div>
            <h2>Payment Successful</h2>
            <p>Thank you for your purchase. Your personalized PCS Vector report is on the way.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Order reference", order_ref)
    with col_b:
        st.metric("Amount paid", amount)
    with col_c:
        st.metric("Status", "Confirmed")

    if completed_at:
        st.caption(f"Payment completed {completed_at}")

    st.markdown(
        """
        <div class="pcs-generating-note">
            <strong>What happens next</strong><br>
            We're building your 8-section strategic plan — housing, schools, spouse career,
            finances, and a 30-day action checklist tailored to your move.
        </div>
        """,
        unsafe_allow_html=True,
    )


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
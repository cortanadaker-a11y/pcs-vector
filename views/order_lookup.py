"""Public order-reference lookup — retrieve a paid report in a new browser session."""

from __future__ import annotations

import streamlit as st

from components.payment_handler import activate_paid_order
from components.sidebar import navigate_to
from services.order_lookup import lookup_paid_order, normalize_order_reference


def _query_param(key: str, default: str = "") -> str:
    value = st.query_params.get(key, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value or default


def _clear_lookup_query_params() -> None:
    try:
        qp = dict(st.query_params)
        for key in ("order", "ref"):
            qp.pop(key, None)
        st.query_params.from_dict(qp)
    except Exception:
        pass


def render_order_lookup() -> None:
    """Let users enter PCS-XXXXXXXX to unlock a paid report without re-paying."""
    st.markdown("## Retrieve your report")
    st.markdown(
        "Already paid? Enter your **order reference** (e.g. `PCS-ABC12XYZ`) "
        "to open your plan and PDF — **no extra charge**."
    )

    prefilled = _query_param("order") or _query_param("ref")
    if prefilled and "lookup_order_input" not in st.session_state:
        st.session_state.lookup_order_input = prefilled

    with st.container(border=True):
        order_input = st.text_input(
            "Order reference",
            placeholder="PCS-ABC12XYZ",
            help="On your payment confirmation and Stripe receipt email.",
            key="lookup_order_input",
        )

        if st.button("Retrieve my report", type="primary", use_container_width=True):
            normalized = normalize_order_reference(order_input)
            if not normalized:
                st.error("Enter a valid order reference like PCS-ABC12XYZ.")
                return

            with st.spinner("Verifying your order…"):
                result = lookup_paid_order(normalized)

            if not result.success:
                st.error(result.message)
                return

            restored = activate_paid_order(
                result.session_id,
                order_reference=result.order_reference,
                amount_paid=result.amount_paid,
                customer_email=result.customer_email,
            )

            from components.report_delivery import sync_delivery_email_from_form

            sync_delivery_email_from_form()

            st.session_state.report_markdown = None
            st.session_state.report_error = None

            if restored:
                st.success(
                    f"Order **{result.order_reference}** verified. Opening your report…",
                    icon="✅",
                )
            else:
                st.warning(
                    f"Payment confirmed for **{result.order_reference}**. "
                    "On the next screen, tap **Generate my report now** — no re-charge.",
                    icon="⚠️",
                )

            _clear_lookup_query_params()
            navigate_to("report")

        st.caption(
            "Find your reference on the payment confirmation screen or in your Stripe receipt. "
            "Your PDF is also emailed to the address from the form."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_home, col_input = st.columns(2)
    with col_home:
        if st.button("← Home", use_container_width=True):
            navigate_to("home")
    with col_input:
        if st.button("Start a new plan", use_container_width=True):
            navigate_to("input")

"""Report / post-purchase view for PCS Vector.

After payment the full plan lives in the PDF (download + email).
This page stays short: confirmation, housing snapshot, delivery, done.
"""

from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from components.form_state import (
    budget_display,
    priority_summary,
    resolved_concerns,
    resolved_current_installation,
    resolved_gaining_installation,
    resolved_housing_must_haves,
    resolved_spouse_career,
)
from components.html_utils import safe_html
from components.payment_handler import (
    attempt_generate_from_order_reference,
    ensure_form_data_restored,
    get_order_reference,
    is_payment_verified,
    require_payment,
)
from components.report_delivery import auto_email_pdf_after_generation, render_pdf_delivery_status
from components.sidebar import navigate_to
from services.pdf_generator import PDFGenerationError, build_pdf_metadata, generate_pdf_report
from services.report_generator import GrokAPIError, generate_report
from views.payment_gate import render_payment_required
from views.post_payment import (
    generate_report_with_loading,
    render_order_reference_recovery,
    render_payment_confirmation_banner,
)


def _render_submitted_summary() -> None:
    data = st.session_state.get("form_data", {})
    if not data.get("form_submitted"):
        return

    gaining = resolved_gaining_installation(data)
    rank_display = data.get("rank_pay_grade", "")
    if data.get("rank_title"):
        rank_display = f"{rank_display} — {data['rank_title']}"

    with st.expander("Your submitted details", expanded=False):
        family_name = f"{data.get('first_name', '').strip()} {data.get('last_name', '').strip()}".strip()
        if family_name:
            st.markdown(f"**Prepared for:** {family_name}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Move**")
            st.markdown(
                f"- **Rank:** {rank_display}  \n"
                f"- **From:** {resolved_current_installation(data)}  \n"
                f"- **To:** {gaining}  \n"
                f"- **Window:** {data.get('move_window', '—')}"
            )

            st.markdown("**Family**")
            children = data.get("num_children", 0)
            child_line = f"{children} child{'ren' if children != 1 else ''}"
            if children and data.get("child_age_ranges"):
                child_line += f" ({', '.join(data['child_age_ranges'])})"
            if data.get("has_pets") == "Yes — we have pets":
                pets = ", ".join(data.get("pet_types") or []) or "Yes"
            else:
                pets = "No"

            st.markdown(
                f"- **Spouse:** {resolved_spouse_career(data)}  \n"
                f"- **Children:** {child_line}  \n"
                f"- **Pets:** {pets}"
            )

        with col2:
            st.markdown("**Housing & priorities**")
            st.markdown(
                f"- **Preference:** {data.get('housing_preference', '—')}  \n"
                f"- **Budget:** {budget_display(data)}  \n"
                f"- **Must-haves:** {resolved_housing_must_haves(data)}"
            )
            for label, value in priority_summary(data).items():
                st.markdown(f"- {label}: **{value}**")

        concerns = resolved_concerns(data)
        if concerns != "None noted":
            st.markdown(f"**Concerns:** {concerns}")


@st.cache_data(show_spinner=False)
def _cached_pdf(report_text: str, metadata_json: str) -> bytes:
    """Cache PDF bytes for identical report content within a session."""
    metadata = json.loads(metadata_json) if metadata_json else None
    return generate_pdf_report(report_text, metadata)


def _build_pdf_bytes(report: str) -> bytes:
    """Generate PDF bytes — requires live Stripe payment verification."""
    if not require_payment():
        return b""

    form_data = st.session_state.get("form_data", {})
    metadata = build_pdf_metadata(form_data)
    metadata_json = json.dumps(metadata, sort_keys=True)

    try:
        with st.spinner("Preparing your PDF…"):
            return _cached_pdf(report, metadata_json)
    except PDFGenerationError as exc:
        st.warning(f"PDF export issue: {exc}. Try regenerating.")
        try:
            return generate_pdf_report(report, metadata)
        except PDFGenerationError:
            return b""


def _generate_report_if_paid() -> str | None:
    """Generate Grok report only after Stripe re-verification passes."""
    if not require_payment():
        st.error("Payment verification failed. Please complete checkout again.")
        return None

    data = st.session_state.get("form_data", {})
    if not data.get("form_submitted"):
        return None

    cached = st.session_state.get("report_markdown")
    if cached:
        return cached

    try:
        report = generate_report_with_loading(lambda: generate_report(data), form_data=data)
        st.session_state.report_markdown = report
        st.session_state.report_error = None
        return report
    except GrokAPIError as exc:
        st.session_state.report_error = str(exc)
        return None


def _family_display_name(form_data: dict) -> str:
    first = (form_data.get("first_name") or "").strip()
    last = (form_data.get("last_name") or "").strip()
    return f"{first} {last}".strip()


def _render_success_header(form_data: dict) -> None:
    family = _family_display_name(form_data)
    gaining = resolved_gaining_installation(form_data)
    title = f"{family}'s PCS plan is ready" if family else "Your PCS plan is ready"
    st.markdown(f"## {title}")
    st.markdown(
        f"Personalized for **{safe_html(gaining)}**. "
        "Your full 8-section plan is in the PDF — download it or open the email.",
        unsafe_allow_html=True,
    )


def _render_bah_summary_banner(form_data: dict) -> None:
    """Compact housing snapshot (full detail is in the PDF)."""
    try:
        meta = build_pdf_metadata(form_data)
        gain = meta.get("bah_gaining_amount")
        delta = meta.get("bah_monthly_delta")
        system = str(meta.get("housing_system") or "BAH")
        if system == "OHA":
            amount_label = "OHA + COLA"
        elif system == "BAH_PLUS_COLA":
            amount_label = "BAH + COLA"
        else:
            amount_label = "BAH"
        amount = f"${int(gain):,}/mo" if gain is not None else "—"
        if delta is not None:
            d = int(delta)
            if d > 0:
                delta_html = f'<div class="pcs-bah-report-delta up">+${d:,}/mo vs current post</div>'
            elif d < 0:
                delta_html = (
                    f'<div class="pcs-bah-report-delta down">−${abs(d):,}/mo vs current post</div>'
                )
            else:
                delta_html = (
                    '<div class="pcs-bah-report-delta flat">Same total as current post</div>'
                )
        else:
            delta_html = ""

        st.markdown(
            f"""
            <div class="pcs-bah-report-banner">
                <div class="pcs-bah-report-amount">{safe_html(amount)} {safe_html(amount_label)} at new post</div>
                {delta_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        return


def _render_howto_compact() -> None:
    st.markdown(
        """
        <div class="pcs-report-howto">
            <strong>How to use the PDF:</strong>
            Read Section 1 with your spouse → hit every Gate before you sign →
            run Section 5 day-by-day → use Section 8 as your short checklist.
            Verify BAH/OHA with finance / TMO.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_report() -> None:
    """Post-purchase: confirm payment, deliver PDF — do not dump the full report body."""

    if st.session_state.get("report_error"):
        st.error(st.session_state.report_error)

    if is_payment_verified():
        ensure_form_data_restored()

    form_data = st.session_state.get("form_data", {})
    form_submitted = form_data.get("form_submitted")

    if form_submitted and not is_payment_verified():
        render_payment_required()
        _render_footer_nav()
        return

    if is_payment_verified() and not form_submitted:
        if ensure_form_data_restored():
            form_data = st.session_state.get("form_data", {})
            form_submitted = form_data.get("form_submitted")
            if form_submitted:
                st.session_state.form_restore_failed = False
                st.rerun()

        if not st.session_state.get("_auto_recovery_attempted"):
            st.session_state._auto_recovery_attempted = True
            if attempt_generate_from_order_reference():
                st.rerun()

        form_data = st.session_state.get("form_data", {})
        form_submitted = form_data.get("form_submitted")
        if not form_submitted:
            st.session_state.form_restore_failed = True

    if is_payment_verified() and not form_submitted:
        render_order_reference_recovery()
        _render_footer_nav()
        return

    if not form_submitted:
        st.markdown("## Your report")
        st.markdown(
            "No plan is ready in this browser session yet. Takes about **3–5 minutes** to fill the form, "
            "then one-time checkout unlocks your personalized plan PDF."
        )
        with st.container(border=True):
            st.markdown(
                "**What you'll get**  \n"
                "- Clear housing call with BAH/OHA math  \n"
                "- Spouse career + first 30 days  \n"
                "- PDF emailed so you can share with your spouse"
            )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(
                "Build your plan →",
                type="primary",
                use_container_width=True,
                key="report_empty_build",
            ):
                navigate_to("input")
        with col_b:
            if st.button(
                "Already paid? Retrieve",
                use_container_width=True,
                key="report_empty_retrieve",
            ):
                navigate_to("retrieve")
        return

    # Paid path: generate plan for PDF/email only — keep the page simple.
    report = _generate_report_if_paid()

    if not report:
        if is_payment_verified():
            st.warning("We couldn't generate your report yet. Use Regenerate or edit your details.")
            if st.button("Regenerate plan", type="primary", use_container_width=True, key="regen_fail"):
                if require_payment():
                    try:
                        with st.spinner("Generating your plan…"):
                            st.session_state.report_markdown = generate_report(
                                st.session_state.form_data
                            )
                        st.session_state.report_error = None
                        st.rerun()
                    except GrokAPIError as exc:
                        st.session_state.report_error = str(exc)
                        st.error(str(exc))
        _render_footer_nav()
        return

    date_stamp = datetime.now().strftime("%Y%m%d")
    pdf_filename = f"pcs-vector-report-{date_stamp}.pdf"
    pdf_bytes = _build_pdf_bytes(report)
    pdf_ready = bool(pdf_bytes)

    if pdf_ready:
        auto_email_pdf_after_generation(pdf_bytes, pdf_filename)

    render_payment_confirmation_banner()
    _render_success_header(form_data)
    _render_bah_summary_banner(form_data)
    _render_howto_compact()

    # Primary action: PDF download
    st.download_button(
        label="Download your PDF plan",
        data=pdf_bytes if pdf_ready else b"",
        file_name=pdf_filename,
        mime="application/pdf",
        type="primary",
        use_container_width=True,
        disabled=not pdf_ready,
        key="report_download_pdf",
    )

    if pdf_ready:
        render_pdf_delivery_status(pdf_bytes, pdf_filename)
    else:
        st.error("PDF could not be built. Tap Regenerate below, or contact support with your order reference.")

    order_ref = get_order_reference()
    st.caption(
        f"Save order **{order_ref}** — use **Retrieve report** anytime on a new phone or browser."
    )

    _render_submitted_summary()

    with st.expander("Need a new copy or having trouble?", expanded=False):
        st.caption("Only use regenerate if the PDF is missing or clearly wrong — it uses another AI generation.")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Regenerate plan", use_container_width=True, key="report_regen"):
                if not require_payment():
                    st.error("Payment verification failed. Complete checkout again.")
                else:
                    try:
                        with st.spinner("Regenerating your plan…"):
                            st.session_state.report_markdown = generate_report(
                                st.session_state.form_data
                            )
                        st.session_state.report_error = None
                        st.session_state.pop("pdf_email_sent_for_order", None)
                        st.rerun()
                    except GrokAPIError as exc:
                        st.session_state.report_error = str(exc)
                        st.error(str(exc))
        with col_b:
            if require_payment() and report:
                st.download_button(
                    label="Download plain text backup",
                    data=report,
                    file_name=f"pcs-vector-report-{date_stamp}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key="report_download_md",
                )

    st.caption("Always verify BAH/OHA and entitlements with your finance office.")
    _render_footer_nav()


def _render_footer_nav() -> None:
    st.markdown('<div class="pcs-form-nav-rule" aria-hidden="true"></div>', unsafe_allow_html=True)
    col_back, col_home = st.columns(2)
    with col_back:
        if st.button("← Edit details", use_container_width=True, key="report_nav_edit"):
            navigate_to("input")
    with col_home:
        if st.button("Home", use_container_width=True, key="report_nav_home"):
            navigate_to("home")

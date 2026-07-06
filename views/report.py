"""Report view page for PCS Vector."""

import json
from datetime import datetime

import streamlit as st

from components.sidebar import navigate_to
from components.form_state import (
    budget_display,
    priority_summary,
    resolved_concerns,
    resolved_current_installation,
    resolved_gaining_installation,
    resolved_housing_must_haves,
    resolved_spouse_career,
)
from components.payment_handler import (
    attempt_generate_from_order_reference,
    ensure_form_data_restored,
    is_payment_verified,
    require_payment,
)
from services.pdf_generator import PDFGenerationError, build_pdf_metadata, generate_pdf_report
from services.report_generator import GrokAPIError, generate_report
from views.payment_gate import render_payment_required
from components.report_delivery import auto_email_pdf_after_generation, render_pdf_delivery_status
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
                f"- **Window:** {data.get('move_window', '—')}  \n"
                f"- **Flexibility:** {data.get('move_flexibility', '—')}"
            )

            st.markdown("**Family**")
            children = data.get("num_children", 0)
            child_line = f"{children} child{'ren' if children != 1 else ''}"
            if children and data.get("child_age_ranges"):
                child_line += f" ({', '.join(data['child_age_ranges'])})"
            if data.get("has_pets") == "Yes — we have pets":
                pets = ", ".join(data.get("pet_types") or [])
                if data.get("pet_details"):
                    pets = f"{pets} — {data['pet_details']}" if pets else data["pet_details"]
                pets = pets or "Yes"
            else:
                pets = "No"

            st.markdown(
                f"- **Spouse:** {resolved_spouse_career(data)}  \n"
                f"- **Children:** {child_line}  \n"
                f"- **Pets:** {pets}"
            )

        with col2:
            st.markdown("**Housing**")
            st.markdown(
                f"- **Preference:** {data.get('housing_preference', '—')}  \n"
                f"- **Budget:** {budget_display(data)}  \n"
                f"- **Must-haves:** {resolved_housing_must_haves(data)}"
            )

            st.markdown("**Priorities**")
            for label, value in priority_summary(data).items():
                st.markdown(f"- {label}: **{value}**")

            st.markdown("**Logistics**")
            st.markdown(
                f"- **Vehicles:** {data.get('num_vehicles', '—')}  \n"
                f"- **DITY / PPM:** {data.get('dity_interest', '—')}"
            )

        concerns = resolved_concerns(data)
        if concerns != "None noted" or data.get("other_priorities"):
            st.markdown("**Notes**")
            if data.get("other_priorities"):
                st.markdown(f"- *Other priorities:* {data['other_priorities']}")
            if concerns != "None noted":
                st.markdown(f"- *Concerns:* {concerns}")


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
        st.warning(f"PDF export issue: {exc}. Try regenerating the report.")
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
        report = generate_report_with_loading(lambda: generate_report(data))
        st.session_state.report_markdown = report
        st.session_state.report_error = None
        return report
    except GrokAPIError as exc:
        st.session_state.report_error = str(exc)
        return None


def render_report() -> None:
    """Render the Grok-generated PCS strategic plan."""
    st.markdown("## Your PCS Strategic Plan")

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
        # Try all restore paths (including external stores) before showing recovery UI.
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
        st.info("Start on the home page, complete the form, then proceed to payment.")
        with st.container(border=True):
            st.markdown(
                "Your plan includes 8 personalized sections — housing & BAH analysis, "
                "spouse career, schools, finances, a 30-day action plan, and a PDF download."
            )
        _render_footer_nav()
        return

    # Paid: generate immediately (loading UI) then show report + PDF on the same page.
    report = _generate_report_if_paid()

    if not report:
        if is_payment_verified():
            st.warning(
                "We couldn't generate your report. Use Regenerate below or edit your details."
            )
        _render_footer_nav()
        return

    render_payment_confirmation_banner()
    _render_submitted_summary()

    date_stamp = datetime.now().strftime("%Y%m%d")
    md_filename = f"pcs-vector-report-{date_stamp}.md"
    pdf_filename = f"pcs-vector-report-{date_stamp}.pdf"

    pdf_bytes = _build_pdf_bytes(report)
    pdf_ready = bool(pdf_bytes)

    if pdf_ready:
        auto_email_pdf_after_generation(pdf_bytes, pdf_filename)

    col_pdf, col_md, col_regen = st.columns([1.2, 1, 1])

    with col_pdf:
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes if pdf_ready else b"",
            file_name=pdf_filename,
            mime="application/pdf",
            type="primary",
            use_container_width=True,
            disabled=not pdf_ready,
        )

    with col_md:
        if not require_payment():
            st.caption("Payment verification required for downloads.")
        else:
            st.download_button(
                label="Download Markdown",
                data=report,
                file_name=md_filename,
                mime="text/markdown",
                use_container_width=True,
            )

    with col_regen:
        if st.button("Regenerate Report", use_container_width=True):
            if not require_payment():
                st.error("Payment verification failed. Please complete checkout again.")
            else:
                try:
                    with st.spinner("Regenerating your report with Grok…"):
                        st.session_state.report_markdown = generate_report(
                            st.session_state.form_data
                        )
                    st.session_state.report_error = None
                    st.rerun()
                except GrokAPIError as exc:
                    st.session_state.report_error = str(exc)
                    st.error(str(exc))

    if pdf_ready:
        render_pdf_delivery_status(pdf_bytes, pdf_filename)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(report)

    st.caption("Generated by Grok AI for PCS Vector. Verify BAH and entitlements with your finance office.")

    _render_footer_nav()


def _render_footer_nav() -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    col_back, col_spacer, col_home = st.columns([1, 2, 1])

    with col_back:
        if st.button("← Edit Details", use_container_width=True):
            navigate_to("input")

    with col_home:
        if st.button("Back to Home", use_container_width=True):
            navigate_to("home")
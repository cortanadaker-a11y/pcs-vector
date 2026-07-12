"""Home / landing page for PCS Vector."""

import streamlit as st

from components.content import (
    AUDIENCE_STRIP,
    CTA,
    DIY_VS_VECTOR,
    HERO,
    HOW_IT_WORKS_STEPS,
    MOTIVATION_CLOSE,
    MOTIVATION_RALLY,
    OUTCOME_BENEFITS,
    PAIN_POINTS,
    PRICING_INCLUDES,
    REPORT_HIGHLIGHTS,
    REPORT_SECTIONS,
    SPOUSE_SHARE_TEASE,
    TESTIMONIAL,
    TRUST_SIGNALS,
    WHY_25,
)
from components.faq import render_faq
from components.report_preview import render_report_preview
from components.html_utils import safe_html, safe_markdown
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def _with_price(text: str, price: str) -> str:
    """Substitute placeholder price and escape for HTML."""
    return safe_html(text.replace("$25", price))


def _cta_block(price: str, *, cta_id: str = "bottom") -> None:
    """Reusable pricing + CTA column."""
    price_safe = safe_html(price)
    includes_html = "".join(f"<li>{safe_html(item)}</li>" for item in PRICING_INCLUDES)
    st.markdown(
        f"""
        <div class="pcs-pricing-box">
            <div class="pcs-price">{price_safe}</div>
            <div class="pcs-price-sub">one-time · per report · no subscription</div>
            <div class="pcs-price-guarantee">Less than a tank of gas · More than a week of PCS stress</div>
            <ul class="pcs-price-includes">{includes_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(CTA["primary"], type="primary", use_container_width=True, key=f"cta_primary_{cta_id}"):
        navigate_to("input")
    if st.button("Already paid? Retrieve your report", use_container_width=True, key=f"cta_retrieve_{cta_id}"):
        navigate_to("retrieve")
    st.caption("Secure Stripe checkout · Built For Soldiers; By Soldiers")


def _render_hero(price: str) -> None:
    price_safe = safe_html(price)
    st.markdown(
        f"""
        <div class="pcs-hero">
            <div class="pcs-brand-kicker">{safe_html(HERO["kicker"])}</div>
            <div class="pcs-brand-title">PCS Vector</div>
            <h1 class="pcs-hero-headline">{safe_html(HERO["headline"])}</h1>
            <p class="pcs-hero-body">{safe_html(HERO["subheadline"])}</p>
            <p class="pcs-hero-outcomes">{safe_html(HERO["outcome_line"])}</p>
            <div class="pcs-hero-stats">
                <span class="pcs-hero-stat"><strong>8</strong> decision sections</span>
                <span class="pcs-hero-stat"><strong>6–8</strong> min intake</span>
                <span class="pcs-hero-stat"><strong>{price_safe}</strong> one-time</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_trust_signals() -> None:
    badges = "".join(f'<span class="pcs-trust-badge">{safe_html(b)}</span>' for b in TRUST_SIGNALS["badges"])
    st.markdown(
        f"""
        <div class="pcs-trust-banner">{safe_html(TRUST_SIGNALS["banner"])}</div>
        <div class="pcs-trust-row">{badges}</div>
        <div class="pcs-audience-strip">{safe_html(AUDIENCE_STRIP)}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_rally(block: dict, *, css_class: str = "pcs-rally") -> None:
    punch = block.get("punch", "")
    punch_html = f'<p class="pcs-rally-punch">{safe_html(punch)}</p>' if punch else ""
    st.markdown(
        f"""
        <div class="{css_class}">
            <h3>{safe_html(block["headline"])}</h3>
            <p class="pcs-rally-body">{safe_html(block["body"])}</p>
            {punch_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_pain_section() -> None:
    st.markdown("### The stakes are higher than another move")
    cols = st.columns(3)
    for col, pain in zip(cols, PAIN_POINTS):
        with col:
            st.markdown(
                f"""
                <div class="pcs-pain-card">
                    <h4>{safe_html(pain["title"])}</h4>
                    <p>{safe_html(pain["desc"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_outcomes() -> None:
    st.markdown("### What changes when you have a real plan")
    cols = st.columns(3)
    for col, benefit in zip(cols, OUTCOME_BENEFITS):
        with col:
            st.markdown(
                f"""
                <div class="pcs-outcome-card">
                    <div class="pcs-outcome-icon">{safe_html(benefit["icon"])}</div>
                    <h3>{safe_html(benefit["title"])}</h3>
                    <p>{safe_html(benefit["desc"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_comparison() -> None:
    st.markdown("### Stop piecing it together. Start executing.")
    cells = [
        '<div class="pcs-cmp-h pcs-cmp-topic"></div>',
        '<div class="pcs-cmp-h">On your own</div>',
        '<div class="pcs-cmp-h pcs-cmp-h-vector">PCS Vector</div>',
    ]
    for row in DIY_VS_VECTOR:
        cells.append(f'<div class="pcs-cmp-topic">{safe_html(row["label"])}</div>')
        cells.append(f'<div class="pcs-cmp-diy">{safe_html(row["diy"])}</div>')
        cells.append(f'<div class="pcs-cmp-vector">{safe_html(row["vector"])}</div>')
    grid = "".join(cells)
    st.markdown(
        f"""
        <div class="pcs-comparison-wrap">
            <div class="pcs-comparison-grid">{grid}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_how_it_works(price: str) -> None:
    st.markdown("### Four steps. One plan. Done tonight.")
    steps_html = '<div class="pcs-flow">'
    for i, step in enumerate(HOW_IT_WORKS_STEPS):
        desc = _with_price(step["desc"], price)
        steps_html += f"""
        <div class="pcs-flow-step">
            <div class="pcs-flow-num">{safe_html(step["num"])}</div>
            <div class="pcs-flow-title">{safe_html(step["title"])}</div>
            <div class="pcs-flow-desc">{desc}</div>
        </div>
        """
        if i < len(HOW_IT_WORKS_STEPS) - 1:
            steps_html += '<div class="pcs-flow-arrow">→</div>'
    steps_html += "</div>"
    st.markdown(steps_html, unsafe_allow_html=True)


def _render_report_sections() -> None:
    st.markdown("### Your complete strategic plan — all eight sections")

    cols = st.columns(2)
    for i, section in enumerate(REPORT_SECTIONS):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="pcs-section-item">
                    <span class="pcs-section-num">{section["num"]}</span>
                    <div>
                        <strong>{safe_html(section["title"])}</strong><br>
                        <span class="pcs-section-desc-inline">{safe_html(section["desc"])}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_example_highlights() -> None:
    st.markdown("### This is the kind of clarity you get")
    st.caption(safe_markdown(SPOUSE_SHARE_TEASE))

    for quote in REPORT_HIGHLIGHTS:
        st.markdown(f'<div class="pcs-highlight">{safe_html(quote)}</div>', unsafe_allow_html=True)

    t = TESTIMONIAL
    st.markdown(
        f"""
        <div class="pcs-testimonial">
            <p>&ldquo;{safe_html(t["quote"])}&rdquo;</p>
            <span>— {safe_html(t["attribution"])}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_why_25(price: str) -> None:
    # Streamlit markdown breaks when multiple <p> tags are nested in one HTML block —
    # use div-based markup throughout this section.
    points_html = "".join(
        f'<div class="pcs-why-point">'
        f'<strong>{safe_html(p["title"])}</strong>'
        f'<div class="pcs-why-point-desc">{safe_html(p["desc"])}</div>'
        f"</div>"
        for p in WHY_25["points"]
    )
    punch = MOTIVATION_RALLY.get("punch", "")
    punch_html = (
        f'<div class="pcs-why-punch">{safe_html(punch)}</div>' if punch else ""
    )
    st.markdown(
        f'<div class="pcs-why-box">'
        f'<h3>{_with_price(WHY_25["headline"], price)}</h3>'
        f'<div class="pcs-why-intro">{safe_html(WHY_25["intro"])}</div>'
        f"{points_html}"
        f'<div class="pcs-why-roi">{safe_html(WHY_25["roi_line"])}</div>'
        f"{punch_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


def _render_mid_cta(price: str) -> None:
    st.markdown(
        f"""
        <div class="pcs-mid-cta">
            <div class="pcs-mid-cta-text">
                <strong>{safe_html(MOTIVATION_CLOSE["headline"])}</strong>
                <span>{_with_price(MOTIVATION_CLOSE["body"], price)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(CTA["mid"], type="primary", use_container_width=True, key="mid_cta"):
        navigate_to("input")


def render_home() -> None:
    """Render the conversion-focused landing page."""
    price = get_price_display()

    _render_hero(price)
    _render_trust_signals()

    cta_top_l, cta_top_c, cta_top_r = st.columns([1, 2, 1])
    with cta_top_c:
        if st.button(CTA["hero"], type="primary", use_container_width=True, key="hero_cta"):
            navigate_to("input")
        st.caption(safe_markdown(CTA["caption"].replace("$25", price)))

    st.markdown("<br>", unsafe_allow_html=True)
    _render_rally(MOTIVATION_RALLY)
    st.markdown("<br>", unsafe_allow_html=True)

    _render_pain_section()
    st.markdown("<br>", unsafe_allow_html=True)
    _render_outcomes()
    st.markdown("<br>", unsafe_allow_html=True)
    _render_comparison()
    st.markdown("<br>", unsafe_allow_html=True)

    _render_how_it_works(price)
    st.markdown("<br>", unsafe_allow_html=True)

    render_report_preview()
    st.markdown("<br>", unsafe_allow_html=True)

    _render_mid_cta(price)
    st.markdown("<br>", unsafe_allow_html=True)

    _render_report_sections()
    st.markdown("<br>", unsafe_allow_html=True)
    _render_example_highlights()
    st.markdown("<br>", unsafe_allow_html=True)

    _render_why_25(price)
    st.markdown("<br>", unsafe_allow_html=True)

    cta_l, cta_c, cta_r = st.columns([1, 2, 1])
    with cta_c:
        _cta_block(price, cta_id="bottom")

    st.markdown("<br>", unsafe_allow_html=True)
    render_faq("Questions before you start")

    st.markdown(
        """
        <div class="pcs-footer">
            PCS Vector — Built For Soldiers; By Soldiers<br>
            Always verify BAH rates and entitlements with your finance office.
        </div>
        """,
        unsafe_allow_html=True,
    )
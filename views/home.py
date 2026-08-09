"""Home / landing page for PCS Vector."""

import streamlit as st

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import (
    CTA,
    DIY_VS_VECTOR,
    HERO,
    HOW_IT_WORKS_STEPS,
    PRICING_INCLUDES,
    TESTIMONIAL,
    TRUST_SIGNALS,
)
from components.faq import render_faq
from components.form_state import start_plan_from_calculator
from components.html_utils import safe_html, safe_markdown
from components.report_preview import render_report_preview
from components.sidebar import navigate_to
from services.stripe_payment import get_price_display


def _with_price(text: str, price: str) -> str:
    """Substitute placeholder price and escape for HTML."""
    return safe_html(text.replace("$25", price))


def _cta_block(price: str, *, cta_id: str = "bottom") -> None:
    """Pricing box + primary CTA."""
    price_safe = safe_html(price)
    includes_html = "".join(f"<li>{safe_html(item)}</li>" for item in PRICING_INCLUDES)
    st.markdown(
        f"""
        <div class="pcs-pricing-box">
            <div class="pcs-price">{price_safe}</div>
            <div class="pcs-price-sub">one-time · per report · no subscription</div>
            <div class="pcs-price-guarantee">Less than a tank of gas · more clarity than a week of Facebook threads</div>
            <ul class="pcs-price-includes">{includes_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(CTA["primary"], type="primary", use_container_width=True, key=f"cta_primary_{cta_id}"):
        # Carry calculator fields when the user already ran the housing tool.
        start_plan_from_calculator(require_snapshot=False)
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
            <div class="pcs-hero-stats">
                <span class="pcs-hero-stat"><strong>8</strong> decision sections</span>
                <span class="pcs-hero-stat"><strong>6–8</strong> min intake</span>
                <span class="pcs-hero-stat"><strong>{price_safe}</strong> one-time</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_trust_bar() -> None:
    """Compact trust row — banner + 3 badges only."""
    # Prefer the highest-signal badges; skip filler.
    keep = {"By Soldiers, for families", "Secure Stripe checkout", "PDF emailed to you"}
    badges = [b for b in TRUST_SIGNALS["badges"] if b in keep]
    if len(badges) < 3:
        badges = TRUST_SIGNALS["badges"][:3]
    badges_html = "".join(f'<span class="pcs-trust-badge">{safe_html(b)}</span>' for b in badges)
    st.markdown(
        f"""
        <div class="pcs-trust-banner">{safe_html(TRUST_SIGNALS["banner"])}</div>
        <div class="pcs-trust-row">{badges_html}</div>
        """,
        unsafe_allow_html=True,
    )


def _render_how_it_works(price: str) -> None:
    st.markdown("### How it works")
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


def _render_comparison() -> None:
    st.markdown("### Why not just use free checklists?")
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


def _render_testimonial() -> None:
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


def render_home() -> None:
    """Lean homepage: hero → BAH → product proof → buy → FAQ."""
    price = get_price_display()

    # 1. Hook
    _render_hero(price)
    _render_trust_bar()

    cta_top_l, cta_top_c, cta_top_r = st.columns([1, 2, 1])
    with cta_top_c:
        if st.button(CTA["hero"], type="primary", use_container_width=True, key="hero_cta"):
            start_plan_from_calculator(require_snapshot=False)
        st.caption(safe_markdown(CTA["caption"].replace("$25", price)))

    # 2. Immediate value tool (high engagement, early)
    st.markdown("<br>", unsafe_allow_html=True)
    render_bah_calculator()

    # Soft CTA after free tool — convert while intent is high; carry calculator → form
    cta_bah_l, cta_bah_c, cta_bah_r = st.columns([1, 2, 1])
    with cta_bah_c:
        snap = get_calculator_snapshot()
        if st.button(
            "Turn this into a full PCS plan →",
            type="primary",
            use_container_width=True,
            key="bah_mid_cta",
        ):
            start_plan_from_calculator(require_snapshot=False)
        if snap:
            grade = snap.get("pay_grade", "")
            gaining = snap.get("gaining_installation", "")
            total = snap.get("total_monthly_usd")
            deps = snap.get("num_dependents", 0)
            yos = snap.get("years_of_service", "")
            total_bit = f" · ~${int(total):,}/mo package" if total is not None else ""
            st.caption(
                f"Carries **{grade}**, {yos} YOS, {deps} dep(s), **{gaining}**"
                f"{total_bit} into the form · full plan · {price} one-time"
            )
        else:
            st.caption(f"Full 8-section plan · {price} one-time · PDF emailed")

    # 3. Product path + proof
    st.markdown("<br>", unsafe_allow_html=True)
    _render_how_it_works(price)

    st.markdown("<br>", unsafe_allow_html=True)
    render_report_preview()

    st.markdown("<br>", unsafe_allow_html=True)
    _render_comparison()

    st.markdown("<br>", unsafe_allow_html=True)
    _render_testimonial()

    # 4. Convert
    st.markdown("<br>", unsafe_allow_html=True)
    cta_l, cta_c, cta_r = st.columns([1, 2, 1])
    with cta_c:
        _cta_block(price, cta_id="bottom")

    # 5. Objections
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

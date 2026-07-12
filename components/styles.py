"""Global styling for PCS Vector."""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Libre+Baskerville:ital,wght@0,700;1,400&display=swap');

    :root {
        --pcs-ink: #1c1c1a;
        --pcs-navy: #2a4a3f;
        --pcs-navy-light: #3d6556;
        --pcs-slate: #454540;
        --pcs-muted: #6b6b66;
        --pcs-bg: #f4f2ee;
        --pcs-surface: #ffffff;
        --pcs-accent: #4a7c64;
        --pcs-accent-soft: #5b8f72;
        --pcs-accent-hover: #3d6652;
        --pcs-gold: #9a8468;
        --pcs-border: #e0ddd6;
        --pcs-success: #2d6a4f;
        --pcs-shadow: 0 12px 40px rgba(28, 28, 26, 0.07);
        --pcs-radius: 14px;
        --pcs-hero-dark: #1a2e28;
    }

    .stApp {
        background: linear-gradient(180deg, #faf9f7 0%, var(--pcs-bg) 40%, #ebe8e2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--pcs-ink);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f7f5f1 100%);
        border-right: 1px solid var(--pcs-border);
        box-shadow: 4px 0 24px rgba(28, 28, 26, 0.04);
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        color: var(--pcs-navy);
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    [data-testid="stSidebar"] .stCaption {
        color: var(--pcs-muted);
    }

    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 3rem;
        max-width: 920px;
    }

    #pcs-page-top {
        height: 0;
        margin: 0;
        padding: 0;
    }

    /* ── Hero / brand ── */
    .pcs-hero {
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 55%, #345947 100%);
        border-radius: 20px;
        padding: 2.75rem 2.25rem 2.5rem 2.25rem;
        color: white;
        margin-bottom: 1.25rem;
        box-shadow: var(--pcs-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }

    .pcs-hero::before {
        content: "";
        position: absolute;
        top: -40%;
        right: -15%;
        width: 55%;
        height: 140%;
        background: radial-gradient(circle, rgba(91, 143, 114, 0.18) 0%, transparent 70%);
        pointer-events: none;
    }

    .pcs-brand-kicker {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.72);
        margin-bottom: 0.65rem;
    }

    .pcs-brand-title {
        font-family: 'Libre Baskerville', Georgia, serif;
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -0.02em;
        color: #ffffff !important;
        margin: 0 0 0.85rem 0;
    }

    .pcs-hero-headline {
        font-size: 1.55rem !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
        letter-spacing: -0.02em;
        color: rgba(255, 255, 255, 0.96) !important;
        margin: 0 0 1rem 0 !important;
        max-width: 36rem;
    }

    .pcs-hero-body {
        font-size: 1.05rem;
        line-height: 1.65;
        color: rgba(255, 255, 255, 0.82) !important;
        margin: 0 0 1rem 0;
        max-width: 40rem;
    }

    .pcs-hero-outcomes {
        font-size: 0.88rem;
        font-weight: 600;
        color: rgba(181, 210, 192, 0.95) !important;
        letter-spacing: 0.02em;
        margin: 0 0 1.25rem 0;
        max-width: 40rem;
    }

    .pcs-hero-stats {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem 1.25rem;
        padding-top: 0.25rem;
    }

    .pcs-hero-stat {
        font-size: 0.82rem;
        color: rgba(255, 255, 255, 0.75);
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 999px;
        padding: 0.35rem 0.85rem;
    }

    .pcs-hero-stat strong {
        color: #ffffff;
        font-weight: 800;
    }

    /* ── Trust ── */
    .pcs-trust-banner {
        display: block;
        text-align: center;
        background: var(--pcs-surface);
        border: 2px solid var(--pcs-navy);
        border-radius: 999px;
        padding: 0.7rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 12px rgba(42, 74, 63, 0.08);
    }

    .pcs-rally {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-left: 4px solid var(--pcs-accent-soft);
        border-radius: var(--pcs-radius);
        padding: 1.5rem 1.65rem;
        box-shadow: 0 4px 20px rgba(28, 28, 26, 0.05);
    }

    .pcs-rally h3 {
        color: var(--pcs-navy);
        font-size: 1.15rem;
        font-weight: 800;
        margin: 0 0 0.65rem 0;
        line-height: 1.35;
    }

    .pcs-rally-body {
        color: var(--pcs-slate);
        font-size: 0.95rem;
        line-height: 1.65;
        margin: 0 0 0.75rem 0;
    }

    .pcs-rally-punch {
        color: var(--pcs-accent);
        font-size: 0.92rem;
        font-weight: 700;
        margin: 0;
        font-style: italic;
    }

    .pcs-trust-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin: 0.25rem 0 0.5rem 0;
    }

    .pcs-trust-badge {
        display: inline-block;
        background: var(--pcs-surface);
        color: var(--pcs-slate);
        font-size: 0.76rem;
        font-weight: 600;
        padding: 0.38rem 0.8rem;
        border-radius: 999px;
        border: 1px solid var(--pcs-border);
        box-shadow: 0 2px 6px rgba(15, 28, 46, 0.04);
    }

    /* ── Cards & sections ── */
    .pcs-card {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: var(--pcs-radius);
        padding: 1.35rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(15, 28, 46, 0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }

    .pcs-card:hover {
        box-shadow: 0 8px 24px rgba(15, 28, 46, 0.07);
    }

    .pcs-card h3 {
        color: var(--pcs-navy);
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 0.45rem 0;
    }

    .pcs-card p {
        color: var(--pcs-slate);
        font-size: 0.92rem;
        line-height: 1.6;
        margin: 0;
    }

    .pcs-pain-card {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-top: 3px solid var(--pcs-accent-soft);
        border-radius: var(--pcs-radius);
        padding: 1.15rem 1.2rem;
        height: 100%;
        box-shadow: 0 4px 14px rgba(15, 28, 46, 0.04);
    }

    .pcs-pain-card h4 {
        color: var(--pcs-navy);
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.45rem 0;
        line-height: 1.35;
    }

    .pcs-pain-card p {
        color: var(--pcs-slate);
        font-size: 0.86rem;
        line-height: 1.55;
        margin: 0;
    }

    .pcs-outcome-card {
        background: linear-gradient(180deg, #ffffff 0%, #f7f6f3 100%);
        border: 1px solid var(--pcs-border);
        border-radius: var(--pcs-radius);
        padding: 1.35rem 1.25rem;
        height: 100%;
        box-shadow: 0 4px 16px rgba(15, 28, 46, 0.04);
    }

    .pcs-outcome-icon {
        color: var(--pcs-accent-soft);
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .pcs-outcome-card h3 {
        color: var(--pcs-navy);
        font-size: 1rem;
        font-weight: 700;
        margin: 0 0 0.45rem 0;
    }

    .pcs-outcome-card p {
        color: var(--pcs-slate);
        font-size: 0.88rem;
        line-height: 1.58;
        margin: 0;
    }

    .pcs-comparison-wrap {
        overflow-x: auto;
        border: 1px solid var(--pcs-border);
        border-radius: var(--pcs-radius);
        background: var(--pcs-surface);
        box-shadow: 0 4px 16px rgba(15, 28, 46, 0.04);
    }

    .pcs-comparison {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }

    .pcs-comparison th {
        background: var(--pcs-navy);
        color: white;
        font-weight: 700;
        padding: 0.75rem 1rem;
        text-align: left;
    }

    .pcs-comparison th:first-child {
        border-radius: 13px 0 0 0;
    }

    .pcs-comparison th:last-child {
        border-radius: 0 13px 0 0;
        background: var(--pcs-navy-light);
    }

    .pcs-comparison td {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid var(--pcs-border);
        vertical-align: top;
        line-height: 1.5;
    }

    .pcs-comparison tr:last-child td {
        border-bottom: none;
    }

    .pcs-cmp-topic {
        font-weight: 700;
        color: var(--pcs-navy);
        width: 28%;
    }

    .pcs-cmp-diy {
        color: var(--pcs-muted);
        width: 36%;
    }

    .pcs-cmp-vector {
        color: var(--pcs-ink);
        font-weight: 600;
        background: rgba(91, 143, 114, 0.08);
        width: 36%;
    }

    .pcs-why-box {
        background: linear-gradient(135deg, #f0f7f3 0%, #faf9f7 50%, #ffffff 100%);
        border: 1px solid rgba(91, 143, 114, 0.35);
        border-radius: 18px;
        padding: 1.65rem 1.75rem;
        box-shadow: 0 8px 28px rgba(42, 74, 63, 0.08);
    }

    .pcs-why-box h3 {
        color: var(--pcs-navy);
        font-size: 1.2rem;
        font-weight: 800;
        margin: 0 0 0.65rem 0;
    }

    .pcs-why-intro {
        color: var(--pcs-slate);
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0 0 1rem 0;
    }

    .pcs-why-point {
        margin-bottom: 0.85rem;
        padding-left: 0.15rem;
    }

    .pcs-why-point strong {
        display: block;
        color: var(--pcs-navy);
        font-size: 0.92rem;
        margin-bottom: 0.2rem;
    }

    .pcs-why-point p {
        color: var(--pcs-slate);
        font-size: 0.88rem;
        line-height: 1.55;
        margin: 0;
    }

    .pcs-why-roi {
        color: var(--pcs-accent);
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0.75rem 0 0 0;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(91, 143, 114, 0.25);
    }

    .pcs-why-punch {
        color: var(--pcs-navy);
        font-size: 0.88rem;
        font-weight: 600;
        font-style: italic;
        margin: 0.65rem 0 0 0;
    }

    .pcs-mid-cta {
        background: linear-gradient(135deg, var(--pcs-navy) 0%, var(--pcs-navy-light) 100%);
        border-radius: 16px;
        padding: 1.35rem 1.5rem;
        text-align: center;
        box-shadow: var(--pcs-shadow);
        margin-bottom: 0.5rem;
    }

    .pcs-mid-cta-text strong {
        display: block;
        color: #ffffff;
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
    }

    .pcs-mid-cta-text span {
        color: rgba(255, 255, 255, 0.78);
        font-size: 0.88rem;
    }

    .pcs-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        margin-bottom: 1rem;
        letter-spacing: 0.04em;
    }

    /* ── Pricing ── */
    .pcs-pricing-box {
        background: var(--pcs-surface);
        border: 2px solid var(--pcs-navy);
        border-radius: 18px;
        padding: 1.65rem 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: var(--pcs-shadow);
    }

    .pcs-price {
        font-size: 2.65rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.03em;
    }

    .pcs-price-sub {
        color: var(--pcs-muted);
        font-size: 0.88rem;
        margin-bottom: 0.45rem;
    }

    .pcs-price-guarantee {
        color: var(--pcs-accent-hover);
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.01em;
    }

    .pcs-price-includes {
        text-align: left;
        color: var(--pcs-slate);
        font-size: 0.9rem;
        margin: 0;
        padding-left: 1.25rem;
        line-height: 1.75;
    }

    /* ── Steps / flow ── */
    .pcs-steps {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin: 0 0 2rem 0;
        padding: 1.25rem 1rem;
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: var(--pcs-radius);
        box-shadow: 0 4px 16px rgba(15, 28, 46, 0.04);
    }

    .pcs-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        max-width: 180px;
    }

    .pcs-step-circle {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.88rem;
        border: 2px solid var(--pcs-border);
        background: var(--pcs-surface);
        color: var(--pcs-muted);
        z-index: 1;
    }

    .pcs-step.active .pcs-step-circle {
        background: var(--pcs-navy);
        border-color: var(--pcs-navy);
        color: white;
        box-shadow: 0 4px 12px rgba(21, 42, 69, 0.25);
    }

    .pcs-step.completed .pcs-step-circle {
        background: var(--pcs-success);
        border-color: var(--pcs-success);
        color: white;
    }

    .pcs-step-label {
        margin-top: 0.5rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--pcs-muted);
        text-align: center;
    }

    .pcs-step.active .pcs-step-label { color: var(--pcs-navy); }
    .pcs-step.completed .pcs-step-label { color: var(--pcs-success); }

    .pcs-step-connector {
        flex: 1;
        height: 2px;
        background: var(--pcs-border);
        margin: 0 -0.5rem;
        margin-bottom: 1.75rem;
        max-width: 80px;
    }

    .pcs-step-connector.completed { background: var(--pcs-success); }

    .pcs-flow {
        display: flex;
        align-items: flex-start;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.35rem;
        padding: 1rem 0;
    }

    .pcs-flow-step {
        text-align: center;
        flex: 1;
        min-width: 120px;
        max-width: 160px;
    }

    .pcs-flow-num {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: var(--pcs-navy);
        color: white;
        font-weight: 700;
        font-size: 0.92rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 10px rgba(21, 42, 69, 0.2);
    }

    .pcs-flow-title {
        font-weight: 700;
        color: var(--pcs-navy);
        font-size: 0.88rem;
        margin-bottom: 0.2rem;
    }

    .pcs-flow-desc {
        color: var(--pcs-muted);
        font-size: 0.8rem;
        line-height: 1.45;
    }

    .pcs-flow-arrow {
        color: var(--pcs-muted);
        font-size: 1.2rem;
        padding-top: 0.55rem;
        flex-shrink: 0;
    }

    @media (max-width: 720px) {
        .pcs-brand-title { font-size: 2.25rem; }
        .pcs-hero-headline { font-size: 1.28rem !important; }
        .pcs-hero { padding: 2rem 1.35rem; }
        .pcs-flow-arrow { display: none; }
        .pcs-flow-step { min-width: 46%; max-width: 48%; }
        .pcs-comparison { font-size: 0.8rem; }
        .pcs-comparison th, .pcs-comparison td { padding: 0.6rem 0.65rem; }
    }

    /* ── Form ── */
    .pcs-section-title {
        color: var(--pcs-navy);
        font-size: 1.12rem;
        font-weight: 700;
        margin: 0 0 0.25rem 0;
    }

    .pcs-section-desc {
        color: var(--pcs-muted);
        font-size: 0.88rem;
        margin: 0 0 1rem 0;
        line-height: 1.5;
    }

    .pcs-email-block {
        background: linear-gradient(135deg, #f0f7f3 0%, #faf9f7 100%);
        border: 1px solid rgba(91, 143, 114, 0.35);
        border-left: 4px solid var(--pcs-accent-soft);
        border-radius: 12px;
        padding: 1rem 1.1rem 0.35rem 1.1rem;
        margin: 0.75rem 0 1rem 0;
    }

    .pcs-email-block-title {
        color: var(--pcs-navy);
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
    }

    .pcs-email-block-caption {
        color: var(--pcs-accent-hover);
        font-size: 0.84rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }

    .pcs-form-steps { margin: 0 0 1.5rem 0; }

    .pcs-form-nav {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 16px;
        padding: 1.25rem 1.5rem 1.5rem 1.5rem;
        margin-top: 0.75rem;
        box-shadow: var(--pcs-shadow);
    }

    .pcs-form-nav-title {
        color: var(--pcs-navy);
        font-size: 0.92rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        text-align: center;
    }

    .pcs-form-nav div[data-testid="stButton"] > button {
        min-height: 3rem;
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid var(--pcs-border);
    }

    .pcs-form-nav div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--pcs-navy) 0%, var(--pcs-navy-light) 100%);
        border: none;
        color: white;
        box-shadow: 0 6px 16px rgba(21, 42, 69, 0.2);
    }

    /* ── Content blocks ── */
    .pcs-section-item {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
        padding: 0.7rem 0;
        border-bottom: 1px solid var(--pcs-border);
    }

    .pcs-section-num {
        background: var(--pcs-navy);
        color: white;
        font-weight: 700;
        font-size: 0.72rem;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .pcs-section-desc-inline {
        color: var(--pcs-muted);
        font-size: 0.84rem;
    }

    .pcs-highlight {
        background: var(--pcs-surface);
        border-left: 3px solid var(--pcs-accent-soft);
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: var(--pcs-slate);
        font-size: 0.9rem;
        font-style: italic;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 8px rgba(15, 28, 46, 0.03);
    }

    .pcs-testimonial {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: var(--pcs-radius);
        padding: 1.35rem 1.5rem;
        margin-top: 1rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(15, 28, 46, 0.04);
    }

    .pcs-testimonial p {
        color: var(--pcs-slate);
        font-size: 0.94rem;
        font-style: italic;
        margin: 0 0 0.5rem 0;
        line-height: 1.55;
    }

    .pcs-testimonial span {
        color: var(--pcs-muted);
        font-size: 0.8rem;
    }

    .pcs-footer {
        text-align: center;
        color: var(--pcs-muted);
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid var(--pcs-border);
        margin-top: 2rem;
    }

    .pcs-payment-cancelled {
        background: #f7f5f1;
        border: 1px solid var(--pcs-border);
        border-left: 4px solid var(--pcs-gold);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: var(--pcs-slate);
        font-size: 0.95rem;
        line-height: 1.55;
    }

    /* ── Streamlit widgets ── */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--pcs-accent-soft) 0%, var(--pcs-accent) 100%);
        border: none;
        font-weight: 700;
        border-radius: 10px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 4px 14px rgba(74, 124, 100, 0.3);
        color: #ffffff !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--pcs-accent) 0%, var(--pcs-accent-hover) 100%);
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(61, 102, 82, 0.35);
    }

    h1, h2, h3 {
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
    }

    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: var(--pcs-radius);
        border-color: var(--pcs-border);
        box-shadow: 0 2px 10px rgba(15, 28, 46, 0.03);
    }
</style>
"""


def apply_styles() -> None:
    """Inject global CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
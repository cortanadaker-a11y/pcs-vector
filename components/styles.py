"""Global styling for PCS Vector."""

import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

    :root {
        --pcs-navy: #1e3a5f;
        --pcs-navy-light: #2d5a8a;
        --pcs-slate: #4a5568;
        --pcs-muted: #718096;
        --pcs-bg: #f7f9fc;
        --pcs-surface: #ffffff;
        --pcs-accent: #c45c26;
        --pcs-accent-hover: #a34a1e;
        --pcs-border: #e2e8f0;
        --pcs-success: #2f855a;
    }

    .stApp {
        background: linear-gradient(180deg, var(--pcs-bg) 0%, #eef2f7 100%);
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] {
        background: var(--pcs-surface);
        border-right: 1px solid var(--pcs-border);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--pcs-navy);
    }

    .pcs-hero {
        background: linear-gradient(135deg, var(--pcs-navy) 0%, var(--pcs-navy-light) 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(30, 58, 95, 0.15);
    }

    .pcs-hero h1 {
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
        color: white !important;
    }

    .pcs-hero p {
        font-size: 1.1rem;
        opacity: 0.92;
        margin: 0;
        line-height: 1.6;
        color: rgba(255, 255, 255, 0.95) !important;
    }

    .pcs-card {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(30, 58, 95, 0.04);
    }

    .pcs-card h3 {
        color: var(--pcs-navy);
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }

    .pcs-card p {
        color: var(--pcs-slate);
        font-size: 0.95rem;
        line-height: 1.55;
        margin: 0;
    }

    .pcs-badge {
        display: inline-block;
        background: rgba(30, 58, 95, 0.08);
        color: var(--pcs-navy);
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        margin-bottom: 1rem;
        letter-spacing: 0.02em;
    }

    .pcs-price {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--pcs-navy);
    }

    .pcs-price span {
        font-size: 0.95rem;
        font-weight: 500;
        color: var(--pcs-muted);
    }

    .pcs-steps {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin: 0 0 2rem 0;
        padding: 1.25rem 1rem;
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(30, 58, 95, 0.04);
    }

    .pcs-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        max-width: 180px;
        position: relative;
    }

    .pcs-step-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
        border: 2px solid var(--pcs-border);
        background: var(--pcs-surface);
        color: var(--pcs-muted);
        z-index: 1;
        transition: all 0.2s ease;
    }

    .pcs-step.active .pcs-step-circle {
        background: var(--pcs-navy);
        border-color: var(--pcs-navy);
        color: white;
    }

    .pcs-step.completed .pcs-step-circle {
        background: var(--pcs-success);
        border-color: var(--pcs-success);
        color: white;
    }

    .pcs-step-label {
        margin-top: 0.5rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--pcs-muted);
        text-align: center;
    }

    .pcs-step.active .pcs-step-label {
        color: var(--pcs-navy);
        font-weight: 600;
    }

    .pcs-step.completed .pcs-step-label {
        color: var(--pcs-success);
    }

    .pcs-step-connector {
        flex: 1;
        height: 2px;
        background: var(--pcs-border);
        margin: 0 -0.5rem;
        margin-bottom: 1.75rem;
        max-width: 80px;
    }

    .pcs-step-connector.completed {
        background: var(--pcs-success);
    }

    .pcs-placeholder {
        text-align: center;
        padding: 3rem 2rem;
        color: var(--pcs-muted);
    }

    .pcs-placeholder-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }

    .pcs-footer {
        text-align: center;
        color: var(--pcs-muted);
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid var(--pcs-border);
        margin-top: 2rem;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        background: var(--pcs-accent);
        border: none;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        transition: background 0.2s ease;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: var(--pcs-accent-hover);
        border: none;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 960px;
    }

    .pcs-section-title {
        color: var(--pcs-navy);
        font-size: 1.15rem;
        font-weight: 600;
        margin: 0 0 0.25rem 0;
    }

    .pcs-section-desc {
        color: var(--pcs-muted);
        font-size: 0.9rem;
        margin: 0 0 1rem 0;
        line-height: 1.5;
    }

    .pcs-form-hint {
        color: var(--pcs-muted);
        font-size: 0.85rem;
        margin-top: -0.25rem;
    }

    .pcs-payment-success {
        background: linear-gradient(135deg, #edf7f0 0%, #f7f9fc 100%);
        border: 1px solid #c6e6d0;
        border-radius: 14px;
        padding: 1.75rem 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    .pcs-payment-success-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: var(--pcs-success);
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .pcs-payment-success h2 {
        color: var(--pcs-navy);
        font-size: 1.5rem;
        margin: 0 0 0.5rem 0;
    }

    .pcs-payment-success p {
        color: var(--pcs-slate);
        margin: 0;
        font-size: 1rem;
    }

    .pcs-generating-note {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: var(--pcs-slate);
        font-size: 0.95rem;
        line-height: 1.55;
        margin-top: 0.5rem;
    }

    .pcs-payment-cancelled {
        background: #fff8f0;
        border: 1px solid #f0d9c0;
        border-left: 4px solid var(--pcs-accent);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        color: var(--pcs-slate);
        font-size: 0.95rem;
        line-height: 1.55;
    }
</style>
"""


def apply_styles() -> None:
    """Inject global CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
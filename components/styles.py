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
        padding-top: 0.35rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 820px;
    }

    /* Kill Streamlit's default top gap */
    .block-container > div:first-child {
        padding-top: 0 !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        gap: 0.35rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding-top: 0.55rem !important;
        padding-bottom: 0.55rem !important;
    }

    .pcs-hero-compact {
        padding: 2rem 1.85rem 1.65rem 1.85rem !important;
        margin-bottom: 0.85rem !important;
    }

    .pcs-hero-compact .pcs-brand-title {
        font-size: 2.75rem;
        margin-bottom: 0.85rem;
    }

    .pcs-hero-compact .pcs-hero-tag {
        margin-bottom: 0;
        font-size: 0.78rem;
        padding: 0.4rem 0.95rem;
    }

    .pcs-sticky-results {
        position: sticky;
        top: 0.35rem;
        z-index: 998;
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 100%);
        color: #fff;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin: 0.45rem 0 0.55rem 0;
        box-shadow: 0 10px 28px rgba(28, 28, 26, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .pcs-sticky-results-main {
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.35rem 0.55rem;
        margin-bottom: 0.45rem;
    }

    .pcs-sticky-results-amt {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
    }

    .pcs-sticky-results-unit {
        font-size: 0.95rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
    }

    .pcs-sticky-results-meta {
        font-size: 0.78rem;
        color: rgba(255, 255, 255, 0.78);
        font-weight: 600;
    }

    .pcs-sticky-results-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.45rem;
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.65rem;
        line-height: 1.35;
    }

    .pcs-sticky-results-grid-4 {
        grid-template-columns: repeat(4, 1fr);
    }

    @media (max-width: 640px) {
        .pcs-sticky-results-grid-4 {
            grid-template-columns: 1fr 1fr;
        }
    }

    .pcs-scen-wrap {
        margin: 0 0 0.65rem 0;
    }

    .pcs-scen-title {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin-bottom: 0.4rem;
    }

    .pcs-scen-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.45rem;
    }

    @media (max-width: 640px) {
        .pcs-scen-grid {
            grid-template-columns: 1fr;
        }
    }

    .pcs-scen {
        border-radius: 10px;
        border: 1px solid var(--pcs-border);
        padding: 0.65rem 0.75rem;
        background: var(--pcs-surface);
    }

    .pcs-scen-ok {
        border-color: #c8ddd0;
        background: #f0f7f3;
    }

    .pcs-scen-short {
        border-color: #e8cfc4;
        background: #faf4f1;
    }

    .pcs-scen-k {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin-bottom: 0.2rem;
    }

    .pcs-scen-rent {
        font-size: 1.1rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
    }

    .pcs-scen-sub {
        font-size: 0.75rem;
        color: var(--pcs-slate);
        margin: 0.15rem 0 0.35rem 0;
    }

    .pcs-scen-left {
        font-size: 0.95rem;
        font-weight: 800;
        color: var(--pcs-navy);
    }

    .pcs-scen-short .pcs-scen-left {
        color: #9a4a2e;
    }

    .pcs-scen-ok .pcs-scen-left {
        color: var(--pcs-success);
    }

    .pcs-scen-left span {
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--pcs-muted);
        margin-left: 0.15rem;
    }

    .pcs-sticky-results-grid b {
        color: #c5ebd4;
        font-weight: 700;
        font-size: 0.68rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .pcs-out-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 0.45rem;
    }

    .pcs-out-dual {
        display: grid;
        grid-template-columns: 1.35fr 1fr;
        gap: 0.75rem;
        align-items: end;
        margin-bottom: 0.45rem;
    }

    @media (max-width: 640px) {
        .pcs-out-dual {
            grid-template-columns: 1fr;
        }
    }

    .pcs-out-dual-k {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: rgba(197, 235, 212, 0.9);
        margin-bottom: 0.2rem;
    }

    .pcs-out-dual-v {
        font-size: 2.15rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        color: #fff;
    }

    .pcs-out-dual-v span,
    .pcs-out-dual-v-sm span {
        font-size: 0.95rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
        margin-left: 0.2rem;
    }

    .pcs-out-dual-v-sm {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.05;
        color: rgba(255, 255, 255, 0.95);
    }

    .pcs-out-dual-sub {
        font-size: 0.78rem;
        color: rgba(255, 255, 255, 0.65);
        margin-top: 0.2rem;
    }

    .pcs-out-fit {
        font-size: 0.84rem;
        line-height: 1.45;
        margin: 0.35rem 0 0.45rem 0;
        padding: 0.55rem 0.7rem;
        border-radius: 8px;
    }

    .pcs-out-fit-fit {
        background: rgba(168, 212, 188, 0.18);
        color: #c5ebd4;
        border: 1px solid rgba(168, 212, 188, 0.35);
    }

    .pcs-out-fit-tight {
        background: rgba(240, 196, 180, 0.15);
        color: #f0d0c0;
        border: 1px solid rgba(240, 196, 180, 0.35);
    }

    .pcs-out-bar-wrap {
        margin: 0.35rem 0 0.75rem 0;
    }

    .pcs-out-bar-track {
        height: 8px;
        background: #e8e4dc;
        border-radius: 999px;
        overflow: hidden;
    }

    .pcs-out-bar-fill {
        height: 100%;
        border-radius: 999px;
        background: var(--pcs-accent);
    }

    .pcs-out-bar-up { background: var(--pcs-success); }
    .pcs-out-bar-down { background: #b85c38; }
    .pcs-out-bar-flat { background: var(--pcs-gold); }

    .pcs-out-bar-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.68rem;
        color: var(--pcs-muted);
        margin-top: 0.25rem;
    }

    .pcs-out-checks-title {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.35rem;
    }

    .pcs-out-checks {
        margin: 0;
        padding-left: 1.15rem;
        font-size: 0.88rem;
        color: var(--pcs-slate);
        line-height: 1.45;
    }

    .pcs-out-checks li {
        margin-bottom: 0.3rem;
    }

    .pcs-out-checks strong {
        color: var(--pcs-navy);
    }

    .pcs-out-profile {
        display: block !important;
        margin-top: 0.35rem !important;
        margin-bottom: 0.45rem;
    }

    .pcs-out-plain {
        font-size: 0.82rem;
        color: rgba(255, 255, 255, 0.82);
        line-height: 1.45;
        margin-bottom: 0.15rem;
    }

    .pcs-out-compare {
        padding: 0.75rem 0.95rem !important;
        margin: 0.45rem 0 0.55rem 0 !important;
    }

    .pcs-out-compare-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--pcs-navy);
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }

    .pcs-out-compare-action {
        font-size: 0.88rem;
        color: var(--pcs-slate);
        line-height: 1.45;
        margin-bottom: 0.55rem;
    }

    .pcs-out-vs {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        gap: 0.65rem;
        align-items: center;
        margin: 0.55rem 0 0.65rem 0;
    }

    @media (max-width: 640px) {
        .pcs-out-vs {
            grid-template-columns: 1fr;
            text-align: center;
        }
    }

    .pcs-out-vs-k {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin-bottom: 0.15rem;
    }

    .pcs-out-vs-v {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .pcs-out-vs-v span {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--pcs-muted);
        margin-left: 0.15rem;
    }

    .pcs-out-vs-s {
        font-size: 0.78rem;
        color: var(--pcs-slate);
        margin-top: 0.15rem;
        line-height: 1.3;
    }

    .pcs-out-vs-mid {
        text-align: center;
        padding: 0 0.35rem;
    }

    .pcs-out-vs-delta {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--pcs-navy);
    }

    .pcs-out-vs-yr {
        font-size: 0.75rem;
        color: var(--pcs-muted);
        margin-top: 0.15rem;
    }

    .pcs-out-split {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.45rem;
        margin: 0 0 0.55rem 0;
    }

    @media (max-width: 640px) {
        .pcs-out-split {
            grid-template-columns: 1fr;
        }
    }

    .pcs-out-split-item {
        background: #f7f5f1;
        border: 1px solid var(--pcs-border);
        border-radius: 10px;
        padding: 0.55rem 0.7rem;
    }

    .pcs-out-split-item span {
        display: block;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin-bottom: 0.15rem;
    }

    .pcs-out-split-item strong {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--pcs-navy);
    }

    .pcs-out-arrive {
        background: #eef4f0;
        border: 1px solid #c8ddd0;
        border-left: 4px solid var(--pcs-accent);
        border-radius: 10px;
        padding: 0.7rem 0.9rem;
        margin: 0 0 0.55rem 0;
        font-size: 0.86rem;
        color: var(--pcs-navy);
        line-height: 1.45;
    }

    .pcs-out-arrive-note {
        display: block;
        margin-top: 0.3rem;
        font-size: 0.76rem;
        color: var(--pcs-muted);
        font-weight: 400;
    }

    .pcs-delta-tight {
        padding: 0.55rem 0.75rem !important;
        margin: 0.35rem 0 0.45rem 0 !important;
        font-size: 0.88rem;
        line-height: 1.35;
    }

    @media (max-width: 640px) {
        .pcs-sticky-results {
            top: 3.1rem;
        }
        .pcs-sticky-results-amt {
            font-size: 1.55rem;
        }
        .pcs-sticky-results-grid {
            grid-template-columns: 1fr;
        }
    }

    #pcs-page-top {
        height: 0;
        margin: 0;
        padding: 0;
    }

    /* ── Hero / brand ── */
    .pcs-hero {
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 55%, #345947 100%);
        border-radius: 18px;
        padding: 1.85rem 1.75rem 1.65rem 1.75rem;
        color: white;
        margin-bottom: 0.85rem;
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
        font-size: 2.45rem;
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -0.02em;
        color: #ffffff !important;
        margin: 0 0 0.55rem 0;
    }

    .pcs-hero-headline {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        letter-spacing: -0.02em;
        color: rgba(255, 255, 255, 0.96) !important;
        margin: 0 0 0.55rem 0 !important;
        max-width: 34rem;
    }

    .pcs-hero-body {
        font-size: 0.95rem;
        line-height: 1.5;
        color: rgba(255, 255, 255, 0.82) !important;
        margin: 0 0 0.75rem 0;
        max-width: 36rem;
    }

    .pcs-hero-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #c5ebd4;
        background: rgba(168, 212, 188, 0.12);
        border: 1px solid rgba(168, 212, 188, 0.35);
        border-radius: 999px;
        padding: 0.35rem 0.85rem;
        margin: 0 0 0.85rem 0;
    }

    .pcs-hero-path {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.35rem 0.55rem;
        margin-top: 1rem;
        padding-top: 0.85rem;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        font-size: 0.78rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.78);
        letter-spacing: 0.02em;
    }

    .pcs-hero-path-sep {
        color: rgba(168, 212, 188, 0.7);
        font-weight: 700;
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

    .pcs-audience-strip {
        text-align: center;
        font-size: 0.88rem;
        line-height: 1.55;
        color: var(--pcs-muted);
        max-width: 40rem;
        margin: 0.75rem auto 0.25rem auto;
        padding: 0 0.5rem;
    }

    .pcs-pay-reassurance {
        background: #f0f6f2;
        border: 1px solid #c8ddd0;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-top: 0.75rem;
        font-size: 0.88rem;
        line-height: 1.55;
        color: var(--pcs-slate);
    }

    .pcs-spouse-share-callout {
        background: linear-gradient(135deg, #f7f5f1 0%, #eef4f0 100%);
        border: 1px solid var(--pcs-border);
        border-left: 4px solid var(--pcs-accent);
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin: 1rem 0 0.5rem 0;
    }

    .pcs-spouse-share-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.45rem;
    }

    .pcs-spouse-share-text {
        font-size: 0.95rem;
        line-height: 1.6;
        color: var(--pcs-ink);
        font-style: italic;
    }

    /* ── BAH calculator ── */
    .pcs-bah-wrap {
        margin-top: 0.25rem;
    }

    .pcs-bah-badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        background: #eef4f0;
        border: 1px solid #c8ddd0;
        border-radius: 999px;
        padding: 0.22rem 0.65rem;
        margin-bottom: 0.55rem;
    }

    .pcs-bah-header h3 {
        color: var(--pcs-navy);
        font-size: 1.25rem;
        font-weight: 800;
        margin: 0 0 0.3rem 0;
        letter-spacing: -0.025em;
    }

    .pcs-bah-sub {
        color: var(--pcs-muted);
        font-size: 0.88rem;
        line-height: 1.45;
        margin: 0 0 0.55rem 0;
        max-width: 36rem;
    }

    .pcs-bah-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin: 0 0 0.65rem 0;
    }

    .pcs-bah-chip-mini {
        font-size: 0.72rem;
        color: var(--pcs-slate);
        background: #f7f5f1;
        border: 1px solid var(--pcs-border);
        border-radius: 999px;
        padding: 0.28rem 0.7rem;
        line-height: 1.3;
    }

    .pcs-bah-chip-mini b {
        color: var(--pcs-accent);
        font-weight: 800;
        margin-right: 0.2rem;
    }

    .pcs-bah-share {
        background: linear-gradient(135deg, #f7f5f1 0%, #eef4f0 100%);
        border: 1px solid #c8ddd0;
        border-radius: 10px;
        padding: 0.75rem 0.95rem;
        margin: 0.65rem 0 0.55rem 0;
    }

    .pcs-bah-share-label {
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.25rem;
    }

    .pcs-bah-share-line {
        font-size: 0.92rem;
        font-weight: 700;
        color: var(--pcs-navy);
        letter-spacing: -0.01em;
        line-height: 1.4;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .pcs-bah-tip {
        background: #eef4f0;
        border: 1px solid #c8ddd0;
        border-left: 4px solid var(--pcs-accent);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin: 0 0 0.85rem 0;
    }

    .pcs-bah-tip-title {
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.3rem;
    }

    .pcs-bah-tip-body {
        font-size: 0.9rem;
        color: var(--pcs-navy);
        line-height: 1.5;
        font-weight: 600;
    }

    .pcs-bah-tip-sub {
        margin-top: 0.35rem;
        font-size: 0.8rem;
        color: var(--pcs-slate);
        line-height: 1.45;
        font-weight: 400;
    }

    .pcs-bah-plan-card {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 12px;
        padding: 0.95rem 1.1rem;
        margin: 0 0 0.75rem 0;
    }

    .pcs-bah-plan-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: var(--pcs-navy);
        margin-bottom: 0.35rem;
        letter-spacing: -0.02em;
    }

    .pcs-bah-plan-amount {
        font-size: 1.35rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }

    .pcs-bah-plan-body {
        font-size: 0.85rem;
        color: var(--pcs-slate);
        line-height: 1.5;
    }

    .pcs-bah-next {
        background: #faf9f7;
        border: 1px dashed #c8ddd0;
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin: 0.5rem 0 0.25rem 0;
        font-size: 0.88rem;
        color: var(--pcs-slate);
        line-height: 1.5;
    }

    .pcs-bah-next strong {
        color: var(--pcs-navy);
    }

    .pcs-bah-section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin: 0.35rem 0 0.55rem 0;
    }

    .pcs-bah-result {
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 100%);
        border-radius: 14px;
        padding: 1.2rem 1.35rem 1.15rem 1.35rem;
        color: #fff;
        margin: 1rem 0 0.75rem 0;
        box-shadow: var(--pcs-shadow);
    }

    .pcs-bah-result-top {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        margin-bottom: 0.35rem;
    }

    .pcs-bah-result-label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.72);
    }

    .pcs-bah-chip {
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        padding: 0.22rem 0.55rem;
        border-radius: 6px;
    }

    .pcs-bah-chip-with {
        background: rgba(168, 212, 188, 0.25);
        color: #c5ebd4;
        border: 1px solid rgba(168, 212, 188, 0.45);
    }

    .pcs-bah-chip-without {
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .pcs-bah-result-amount {
        font-size: 2.65rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.05;
    }

    .pcs-bah-result-amount span {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
        margin-left: 0.2rem;
    }

    .pcs-bah-result-meta {
        margin-top: 0.45rem;
        font-size: 0.82rem;
        color: rgba(255, 255, 255, 0.78);
        line-height: 1.45;
    }

    .pcs-bah-result-annual {
        margin-top: 0.55rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: #a8d4bc;
    }

    .pcs-bah-pair {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.55rem;
        margin: 0 0 0.85rem 0;
    }

    @media (max-width: 640px) {
        .pcs-bah-pair {
            grid-template-columns: 1fr;
        }
    }

    .pcs-bah-pair-card {
        background: #f7f5f1;
        border: 1px solid var(--pcs-border);
        border-radius: 10px;
        padding: 0.7rem 0.85rem;
        transition: border-color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
    }

    .pcs-bah-pair-active {
        background: #eef4f0;
        border-color: var(--pcs-accent);
        box-shadow: 0 0 0 1px var(--pcs-accent);
    }

    .pcs-bah-pair-diff {
        background: #faf9f7;
    }

    .pcs-bah-pair-k {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin-bottom: 0.2rem;
    }

    .pcs-bah-pair-v {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
    }

    .pcs-bah-delta {
        border-radius: 12px;
        padding: 1rem 1.15rem;
        margin: 0 0 0.75rem 0;
        border: 1px solid var(--pcs-border);
        background: var(--pcs-surface);
    }

    .pcs-bah-delta-up {
        border-left: 4px solid var(--pcs-success);
        background: #f0f7f3;
    }

    .pcs-bah-delta-down {
        border-left: 4px solid #b85c38;
        background: #faf4f1;
    }

    .pcs-bah-delta-flat {
        border-left: 4px solid var(--pcs-gold);
    }

    .pcs-bah-delta-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--pcs-navy);
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .pcs-bah-delta-detail {
        font-size: 0.88rem;
        color: var(--pcs-slate);
        line-height: 1.5;
        margin-bottom: 0.85rem;
    }

    .pcs-bah-delta-grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr 1fr;
        gap: 0.65rem;
        align-items: start;
    }

    @media (max-width: 640px) {
        .pcs-bah-delta-grid {
            grid-template-columns: 1fr 1fr;
        }
        .pcs-bah-delta-arrow {
            display: none;
        }
    }

    .pcs-bah-delta-k {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
    }

    .pcs-bah-delta-v {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
    }

    .pcs-bah-delta-s {
        font-size: 0.75rem;
        color: var(--pcs-muted);
        line-height: 1.35;
    }

    .pcs-bah-delta-arrow {
        font-size: 1.25rem;
        color: var(--pcs-accent);
        font-weight: 700;
        text-align: center;
        padding-top: 0.85rem;
    }

    .pcs-bah-report-banner {
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 100%);
        border-radius: 12px;
        padding: 0.95rem 1.15rem;
        color: #fff;
        margin: 0.65rem 0 0.85rem 0;
        box-shadow: var(--pcs-shadow);
    }

    .pcs-bah-report-amount {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }

    .pcs-bah-report-delta {
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .pcs-bah-report-delta.up { color: #a8d4bc; }
    .pcs-bah-report-delta.down { color: #f0c4b4; }
    .pcs-bah-report-delta.flat { color: rgba(255,255,255,0.8); }

    .pcs-bah-report-text {
        font-size: 0.88rem;
        line-height: 1.5;
        color: rgba(255, 255, 255, 0.9);
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

    .pcs-comparison-grid {
        display: grid;
        grid-template-columns: 28% 36% 36%;
        width: 100%;
        font-size: 0.88rem;
    }

    .pcs-cmp-h {
        background: var(--pcs-navy);
        color: white;
        font-weight: 700;
        padding: 0.75rem 1rem;
        text-align: left;
    }

    .pcs-cmp-h:first-child {
        border-radius: 13px 0 0 0;
    }

    .pcs-cmp-h-vector {
        border-radius: 0 13px 0 0;
        background: var(--pcs-navy-light);
    }

    .pcs-comparison-grid > .pcs-cmp-topic,
    .pcs-comparison-grid > .pcs-cmp-diy,
    .pcs-comparison-grid > .pcs-cmp-vector {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid var(--pcs-border);
        vertical-align: top;
        line-height: 1.5;
    }

    .pcs-comparison-grid > .pcs-cmp-topic:nth-last-child(3),
    .pcs-comparison-grid > .pcs-cmp-diy:nth-last-child(2),
    .pcs-comparison-grid > .pcs-cmp-vector:last-child {
        border-bottom: none;
    }

    .pcs-cmp-topic {
        font-weight: 700;
        color: var(--pcs-navy);
    }

    .pcs-cmp-diy {
        color: var(--pcs-muted);
    }

    .pcs-cmp-vector {
        color: var(--pcs-ink);
        font-weight: 600;
        background: rgba(91, 143, 114, 0.08);
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

    .pcs-why-point-desc {
        color: var(--pcs-slate);
        font-size: 0.88rem;
        line-height: 1.55;
        margin: 0;
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

    .pcs-flow-slim {
        padding: 0.35rem 0 0.85rem 0;
        margin-bottom: 0.15rem;
        background: transparent;
    }

    .pcs-flow-step {
        text-align: center;
        flex: 1;
        min-width: 100px;
        max-width: 150px;
    }

    .pcs-flow-slim .pcs-flow-step {
        max-width: 140px;
    }

    .pcs-flow-num {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--pcs-navy);
        color: white;
        font-weight: 700;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.35rem;
        box-shadow: 0 4px 10px rgba(21, 42, 69, 0.2);
    }

    .pcs-flow-title {
        font-weight: 700;
        color: var(--pcs-navy);
        font-size: 0.82rem;
        margin-bottom: 0.1rem;
    }

    .pcs-flow-desc {
        color: var(--pcs-muted);
        font-size: 0.72rem;
        line-height: 1.35;
    }

    .pcs-flow-arrow {
        color: var(--pcs-muted);
        font-size: 1.05rem;
        padding-top: 0.4rem;
        flex-shrink: 0;
    }

    .pcs-section-label {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin: 0.5rem 0 0.35rem 0;
    }

    .pcs-ref-card {
        margin: 1.25rem 0 0.55rem 0;
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-left: 4px solid var(--pcs-accent);
        border-radius: 12px;
        padding: 1rem 1.15rem;
        box-shadow: 0 4px 16px rgba(28, 28, 26, 0.04);
    }

    .pcs-ref-kicker {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.25rem;
    }

    .pcs-ref-title {
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        color: var(--pcs-navy) !important;
        margin: 0 0 0.35rem 0 !important;
        letter-spacing: -0.02em;
        line-height: 1.25 !important;
    }

    .pcs-ref-body {
        font-size: 0.9rem;
        color: var(--pcs-slate);
        line-height: 1.45;
        margin: 0 0 0.35rem 0;
        max-width: 36rem;
    }

    .pcs-ref-meta {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--pcs-muted);
    }

    .pcs-bottom-line {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 12px;
        padding: 0.95rem 1.1rem;
        margin: 0 0 0.75rem 0;
        box-shadow: 0 4px 16px rgba(28, 28, 26, 0.04);
    }

    .pcs-bottom-line-title {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.65rem;
    }

    .pcs-bottom-line-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.55rem;
        margin-bottom: 0.65rem;
    }

    @media (max-width: 640px) {
        .pcs-bottom-line-grid {
            grid-template-columns: 1fr;
        }
    }

    .pcs-bottom-line-cell {
        background: #f7f5f1;
        border-radius: 8px;
        padding: 0.55rem 0.7rem;
    }

    .pcs-bottom-line-k {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin-bottom: 0.15rem;
    }

    .pcs-bottom-line-v {
        font-size: 1.05rem;
        font-weight: 800;
        color: var(--pcs-navy);
        letter-spacing: -0.02em;
    }

    .pcs-bottom-line-note {
        font-size: 0.84rem;
        color: var(--pcs-slate);
        line-height: 1.45;
    }

    .pcs-bah-result-wow {
        animation: pcs-result-in 0.45s ease-out;
    }

    @keyframes pcs-result-in {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .pcs-hero-wow::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, transparent 40%, rgba(255,255,255,0.04) 50%, transparent 60%);
        pointer-events: none;
    }

    .pcs-arrive {
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 100%);
        color: #fff;
        border-radius: 12px;
        padding: 1.05rem 1.15rem;
        margin: 0 0 0.75rem 0;
        box-shadow: var(--pcs-shadow);
        animation: pcs-result-in 0.5s ease-out;
    }

    .pcs-arrive-title {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(197, 235, 212, 0.9);
        margin-bottom: 0.35rem;
    }

    .pcs-arrive-amount {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 0.45rem;
    }

    .pcs-arrive-amount span {
        font-size: 0.95rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.7);
        margin-left: 0.25rem;
    }

    .pcs-arrive-math {
        font-size: 0.82rem;
        color: rgba(255, 255, 255, 0.82);
        line-height: 1.5;
        margin-bottom: 0.4rem;
    }

    .pcs-arrive-math strong {
        color: #c5ebd4;
    }

    .pcs-arrive-sub {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.65);
        line-height: 1.45;
    }

    .pcs-post-intel {
        background: #f7f5f1;
        border: 1px solid var(--pcs-border);
        border-radius: 12px;
        padding: 0.9rem 1.05rem;
        margin: 0 0 0.75rem 0;
    }

    .pcs-post-intel-title {
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--pcs-accent);
        margin-bottom: 0.35rem;
    }

    .pcs-post-intel-body {
        font-size: 0.88rem;
        color: var(--pcs-ink);
        line-height: 1.5;
        margin-bottom: 0.45rem;
    }

    .pcs-post-intel-meta {
        font-size: 0.8rem;
        color: var(--pcs-slate);
        line-height: 1.45;
        margin-top: 0.25rem;
    }

    .pcs-post-intel-meta b {
        color: var(--pcs-navy);
    }

    .pcs-share-pair-label {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--pcs-muted);
        margin: 0.75rem 0 0.35rem 0;
    }

    .pcs-swap-spacer {
        height: 1.65rem;
    }

    @media (max-width: 720px) {
        .pcs-brand-title { font-size: 2rem; }
        .pcs-hero-headline { font-size: 1.18rem !important; }
        .pcs-hero { padding: 1.45rem 1.2rem; }
        .pcs-flow-arrow { display: none; }
        .pcs-flow-step { min-width: 46%; max-width: 48%; }
        .pcs-comparison-grid { font-size: 0.8rem; }
        .pcs-comparison-grid > .pcs-cmp-h,
        .pcs-comparison-grid > .pcs-cmp-topic,
        .pcs-comparison-grid > .pcs-cmp-diy,
        .pcs-comparison-grid > .pcs-cmp-vector { padding: 0.6rem 0.65rem; }
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

    .pcs-rank-auto {
        color: var(--pcs-slate);
        font-size: 0.9rem;
        margin: -0.35rem 0 0.85rem 0;
        line-height: 1.4;
    }

    .pcs-rank-auto strong {
        color: var(--pcs-navy);
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

    /* Per-step soldier context (time, why, what to have handy) */
    .pcs-step-context {
        background: linear-gradient(135deg, #f7faf8 0%, #f0f7f3 100%);
        border: 1px solid rgba(91, 143, 114, 0.28);
        border-left: 4px solid var(--pcs-accent);
        border-radius: 12px;
        padding: 0.85rem 1.1rem 0.75rem 1.1rem;
        margin: 0 0 1.15rem 0;
    }

    .pcs-step-context-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-bottom: 0.55rem;
    }

    .pcs-step-context-chip {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: var(--pcs-navy);
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(91, 143, 114, 0.35);
        border-radius: 999px;
        padding: 0.22rem 0.65rem;
    }

    .pcs-step-context-chip.muted {
        color: var(--pcs-muted);
        font-weight: 600;
        border-color: var(--pcs-border);
        background: rgba(255, 255, 255, 0.65);
    }

    .pcs-step-context-why,
    .pcs-step-context-need {
        margin: 0.25rem 0 0 0;
        font-size: 0.88rem;
        line-height: 1.5;
        color: var(--pcs-slate);
    }

    .pcs-step-context-need {
        color: var(--pcs-muted);
        font-size: 0.84rem;
    }

    /* Report reading guide */
    .pcs-report-howto {
        background: #f0f7f3;
        border: 1px solid rgba(91, 143, 114, 0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0 1rem 0;
        font-size: 0.9rem;
        line-height: 1.5;
        color: var(--pcs-slate);
    }

    /* Thin divider above Home/Next — no empty card (Streamlit can't wrap widgets in HTML). */
    .pcs-form-nav-rule {
        height: 0;
        border: none;
        border-top: 1px solid var(--pcs-border);
        margin: 1.35rem 0 1rem 0;
        padding: 0;
        background: transparent;
        box-shadow: none;
    }

    /* Larger touch targets on phone (gate traffic / one-handed use) */
    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
            padding-top: 0.85rem;
        }

        .pcs-hero {
            padding: 1.75rem 1.25rem 1.5rem 1.25rem;
            border-radius: 16px;
        }

        .pcs-brand-title {
            font-size: 2.15rem;
        }

        .pcs-hero-headline {
            font-size: 1.25rem !important;
        }

        div[data-testid="stButton"] > button {
            min-height: 3rem;
            font-size: 1rem;
        }

        .pcs-bah-result-amount {
            font-size: 1.85rem;
        }

        .pcs-step-context {
            padding: 0.75rem 0.85rem;
        }
    }

    /* Hide Streamlit's empty markdown element if a stray wrapper ever reappears */
    .element-container:has(> div > .pcs-form-nav:empty),
    div[data-testid="stMarkdownContainer"]:has(> .pcs-form-nav:empty) {
        display: none !important;
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

    /* ── Report preview (homepage) ── */
    .pcs-preview-wrap {
        margin: 0.5rem 0 1rem 0;
    }

    .pcs-preview-header h3 {
        color: var(--pcs-navy);
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.02em;
    }

    .pcs-preview-sub {
        color: var(--pcs-muted);
        font-size: 0.92rem;
        line-height: 1.55;
        margin: 0 0 1rem 0;
        max-width: 42rem;
    }

    .pcs-preview-doc {
        background: var(--pcs-surface);
        border: 1px solid var(--pcs-border);
        border-radius: 16px;
        box-shadow: var(--pcs-shadow);
        overflow: hidden;
    }

    .pcs-preview-doc-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.65rem;
        padding: 0.65rem 1.1rem;
        background: #f7f5f1;
        border-bottom: 1px solid var(--pcs-border);
        font-size: 0.78rem;
    }

    .pcs-preview-doc-badge {
        background: var(--pcs-navy);
        color: #fff;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        font-size: 0.68rem;
    }

    .pcs-preview-doc-meta {
        color: var(--pcs-muted);
        font-weight: 500;
    }

    .pcs-preview-doc-title {
        font-family: 'Libre Baskerville', Georgia, serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--pcs-navy);
        padding: 1rem 1.25rem 0.25rem 1.25rem;
    }

    .pcs-preview-section {
        padding: 0.65rem 1.25rem 0.85rem 1.25rem;
        border-bottom: 1px solid #f0ede8;
    }

    .pcs-preview-section-head {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.45rem;
    }

    .pcs-preview-section-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.45rem;
        height: 1.45rem;
        border-radius: 50%;
        background: var(--pcs-accent);
        color: #fff;
        font-size: 0.72rem;
        font-weight: 700;
        flex-shrink: 0;
    }

    .pcs-preview-section-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: var(--pcs-navy);
    }

    .pcs-preview-section-body p {
        margin: 0 0 0.45rem 0;
        font-size: 0.86rem;
        line-height: 1.55;
        color: var(--pcs-slate);
    }

    .pcs-preview-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8rem;
        margin-top: 0.35rem;
    }

    .pcs-preview-table th,
    .pcs-preview-table td {
        border: 1px solid var(--pcs-border);
        padding: 0.4rem 0.55rem;
        text-align: left;
    }

    .pcs-preview-table th {
        background: #f7f5f1;
        color: var(--pcs-navy);
        font-weight: 600;
    }

    .pcs-preview-blur-zone {
        position: relative;
        min-height: 9rem;
        background: linear-gradient(180deg, #faf9f7 0%, #eef2ef 100%);
    }

    .pcs-preview-blur-fade {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2.5rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, transparent 100%);
        pointer-events: none;
    }

    .pcs-preview-blur-content {
        position: relative;
        padding: 1.5rem 1.25rem 1.25rem 1.25rem;
        text-align: center;
    }

    .pcs-preview-blur-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: var(--pcs-navy);
        margin: 0 0 0.65rem 0;
    }

    .pcs-preview-blur-list {
        list-style: none;
        padding: 0;
        margin: 0 0 0.65rem 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.4rem 0.75rem;
        filter: blur(3px);
        opacity: 0.65;
        user-select: none;
    }

    .pcs-preview-blur-list li {
        font-size: 0.78rem;
        color: var(--pcs-muted);
    }

    .pcs-preview-blur-num {
        font-weight: 700;
        margin-right: 0.25rem;
    }

    .pcs-preview-blur-note {
        font-size: 0.8rem;
        color: var(--pcs-accent);
        font-weight: 600;
        margin: 0;
    }

    /* ── Report generation loading ── */
    .pcs-gen-panel {
        background: linear-gradient(145deg, var(--pcs-hero-dark) 0%, var(--pcs-navy) 100%);
        border-radius: 16px;
        padding: 1.35rem 1.4rem 1.2rem 1.4rem;
        color: #fff;
        margin-bottom: 1rem;
        box-shadow: var(--pcs-shadow);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .pcs-gen-panel-title {
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    .pcs-gen-panel-sub {
        font-size: 0.88rem;
        color: rgba(255, 255, 255, 0.78);
        margin-top: 0.25rem;
    }

    .pcs-gen-panel-sub strong {
        color: rgba(255, 255, 255, 0.95);
    }

    .pcs-gen-progress-track {
        height: 4px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 999px;
        margin: 1rem 0 0.85rem 0;
        overflow: hidden;
    }

    .pcs-gen-progress-bar {
        height: 100%;
        width: 35%;
        background: linear-gradient(90deg, var(--pcs-accent-soft), #8fc4a8);
        border-radius: 999px;
        animation: pcs-gen-slide 2.2s ease-in-out infinite;
    }

    @keyframes pcs-gen-slide {
        0% { transform: translateX(-100%); width: 30%; }
        50% { width: 55%; }
        100% { transform: translateX(320%); width: 30%; }
    }

    .pcs-gen-steps {
        display: grid;
        gap: 0.45rem;
        margin-bottom: 0.85rem;
    }

    .pcs-gen-step {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-size: 0.84rem;
        color: rgba(255, 255, 255, 0.88);
    }

    .pcs-gen-step-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--pcs-accent-soft);
        flex-shrink: 0;
        animation: pcs-gen-pulse 1.4s ease-in-out infinite;
    }

    .pcs-gen-step:nth-child(2) .pcs-gen-step-dot { animation-delay: 0.15s; }
    .pcs-gen-step:nth-child(3) .pcs-gen-step-dot { animation-delay: 0.3s; }
    .pcs-gen-step:nth-child(4) .pcs-gen-step-dot { animation-delay: 0.45s; }
    .pcs-gen-step:nth-child(5) .pcs-gen-step-dot { animation-delay: 0.6s; }
    .pcs-gen-step:nth-child(6) .pcs-gen-step-dot { animation-delay: 0.75s; }

    @keyframes pcs-gen-pulse {
        0%, 100% { opacity: 0.45; transform: scale(0.85); }
        50% { opacity: 1; transform: scale(1.15); }
    }

    .pcs-gen-sections-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(255, 255, 255, 0.55);
        margin-bottom: 0.4rem;
    }

    .pcs-gen-sections {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-bottom: 0.75rem;
    }

    .pcs-gen-section-chip {
        font-size: 0.68rem;
        font-weight: 600;
        padding: 0.22rem 0.5rem;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: rgba(255, 255, 255, 0.82);
    }

    .pcs-gen-foot {
        font-size: 0.78rem;
        color: rgba(255, 255, 255, 0.6);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding-top: 0.65rem;
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
        font-size: 0.75rem;
        padding: 1.35rem 0 0.75rem 0;
        border-top: 1px solid var(--pcs-border);
        margin-top: 1.25rem;
        line-height: 1.5;
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
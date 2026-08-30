"""Global styling for PCS Vector — single finished visual system (UI only)."""

import streamlit as st

# 8 locked tokens + thin derived set. Applied app-wide.
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    /* Loop 1 + Loop 7 — locked palette */
    --pcs-bg: #121E16;
    --pcs-card: #1C2D22;
    --pcs-raised: #24362C;
    --pcs-text: #FFFFFF;
    --pcs-muted: #A3ADB6;
    --pcs-gold: #D4AF37;
    --pcs-orange: #EA580C;
    --pcs-success: #34D399;
    --pcs-danger: #F87171;

    /* Derived (keep sparse) */
    --pcs-orange-hover: #C2410C;
    --pcs-border: rgba(255, 255, 255, 0.10);
    --pcs-border-strong: rgba(255, 255, 255, 0.16);
    --pcs-panel: rgba(0, 0, 0, 0.38);
    --pcs-panel-deep: rgba(0, 0, 0, 0.55);
    --pcs-control: rgba(0, 0, 0, 0.48);
    --pcs-text-dim: #C8D0D8;
    --pcs-shadow: 0 20px 44px rgba(0, 0, 0, 0.48);
    --pcs-radius: 18px;
    --pcs-radius-sm: 14px;
    --pcs-tap: 44px;
    --pcs-space: 8px;

    /* Legacy aliases */
    --pcs-card-2: var(--pcs-raised);
    --pcs-ink: var(--pcs-text);
    --pcs-navy: var(--pcs-card);
    --pcs-navy-light: var(--pcs-raised);
    --pcs-slate: var(--pcs-text-dim);
    --pcs-surface: var(--pcs-card);
    --pcs-accent: var(--pcs-gold);
    --pcs-accent-soft: #E0C25A;
    --pcs-accent-hover: #B8962E;
    --pcs-army-deep: var(--pcs-bg);
    --pcs-army-card: var(--pcs-card);
    --pcs-army-gold: var(--pcs-gold);
    --pcs-hero-dark: var(--pcs-bg);
    --pcs-control-text: var(--pcs-text);
    --pcs-gold-soft: #E0C25A;
}

/* ═══════════════════════════════════════════
   Loop 1 — Kill Streamlit chrome (global)
   ═══════════════════════════════════════════ */
html, body, .stApp, .main,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stHeader"],
header[data-testid="stHeader"],
section.main > div {
    background: var(--pcs-bg) !important;
    color: var(--pcs-text) !important;
}

html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-tap-highlight-color: transparent;
    overflow-x: hidden !important;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    background: transparent !important;
}

/* Hide Deploy / menu chrome noise when possible */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: var(--pcs-bg) !important;
    height: 2.4rem;
}

[data-testid="stSidebar"] {
    background: #0E1712 !important;
    border-right: 1px solid var(--pcs-border);
}
[data-testid="stSidebar"] .stMarkdown h2 {
    color: var(--pcs-text) !important;
    font-weight: 800;
    letter-spacing: -0.03em;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--pcs-muted) !important;
}

.block-container {
    padding-top: calc(var(--pcs-space) * 1) !important;
    padding-bottom: calc(var(--pcs-space) * 14) !important;
    padding-left: calc(var(--pcs-space) * 1.5) !important;
    padding-right: calc(var(--pcs-space) * 1.5) !important;
    max-width: 36rem;
}
.block-container > div:first-child { padding-top: 0 !important; }

div[data-testid="stVerticalBlock"] > div { gap: calc(var(--pcs-space) * 0.5); }

/* Markdown / body copy */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: var(--pcs-text-dim) !important;
}
[data-testid="stMarkdownContainer"] strong {
    color: var(--pcs-text) !important;
    font-weight: 800;
}
.stCaption, [data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: var(--pcs-muted) !important;
}

/* Alerts */
[data-testid="stAlert"] {
    background: var(--pcs-panel) !important;
    color: var(--pcs-text) !important;
    border: 1px solid var(--pcs-border) !important;
    border-radius: var(--pcs-radius-sm) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background: var(--pcs-card) !important;
    border: 1px solid var(--pcs-border) !important;
    border-radius: var(--pcs-radius-sm) !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] p,
[data-testid="stExpander"] span {
    color: var(--pcs-text-dim) !important;
}

/* Global form controls — kill cream/white defaults */
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: var(--pcs-control) !important;
    border: 1px solid var(--pcs-border-strong) !important;
    border-radius: var(--pcs-radius-sm) !important;
    min-height: var(--pcs-tap) !important;
    color: var(--pcs-text) !important;
    box-shadow: none !important;
}
[data-baseweb="select"] *,
[data-testid="stSelectbox"] * {
    color: var(--pcs-text) !important;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: var(--pcs-control) !important;
    border: 1px solid var(--pcs-border-strong) !important;
    border-radius: var(--pcs-radius-sm) !important;
    min-height: var(--pcs-tap) !important;
    color: var(--pcs-text) !important;
    font-weight: 600 !important;
    caret-color: var(--pcs-gold);
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: var(--pcs-muted) !important;
    opacity: 0.85;
}

/* Dropdown menus (portaled) */
[data-baseweb="popover"] ul,
[data-baseweb="menu"],
ul[role="listbox"],
li[role="option"] {
    background-color: var(--pcs-card) !important;
    color: var(--pcs-text) !important;
    border-color: var(--pcs-border) !important;
}
li[role="option"]:hover,
li[aria-selected="true"] {
    background-color: var(--pcs-raised) !important;
}

[data-testid="stWidgetLabel"] p,
label p {
    color: var(--pcs-muted) !important;
    font-size: 0.65rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label {
    color: var(--pcs-text-dim) !important;
    min-height: var(--pcs-tap);
    align-items: center !important;
}

/* ═══════════════════════════════════════════
   Loop 2 — Typography
   ═══════════════════════════════════════════ */
h1, h2, h3, h4 {
    color: var(--pcs-text) !important;
    font-weight: 800 !important;
    letter-spacing: -0.025em;
    line-height: 1.2;
}
h1 { font-size: 1.35rem !important; margin-bottom: 0.35rem !important; }
h2 { font-size: 1.15rem !important; margin-bottom: 0.3rem !important; }
h3 { font-size: 1rem !important; }

.pcs-face-brand {
    text-align: center;
    padding: 0 0 calc(var(--pcs-space) * 0.5) 0;
}
.pcs-face-brand .pcs-brand-title {
    font-size: 1rem;
    font-weight: 900;
    color: var(--pcs-text);
    letter-spacing: -0.03em;
    line-height: 1.1;
}
.pcs-face-tagline {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--pcs-gold);
    margin-top: 0.2rem;
}
.pcs-face-mini,
.pcs-hero-pills { display: none !important; }
.pcs-calc-top { margin: 0 0 calc(var(--pcs-space) * 0.25) 0; }

.pcs-section-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--pcs-text);
    margin: calc(var(--pcs-space) * 0.5) 0 calc(var(--pcs-space) * 0.25) 0;
}
.pcs-section-desc {
    font-size: 0.8rem;
    color: var(--pcs-muted) !important;
    line-height: 1.45;
    margin: 0 0 calc(var(--pcs-space) * 1) 0;
}
.pcs-section-desc strong { color: var(--pcs-text) !important; }

/* ═══════════════════════════════════════════
   Buttons — one orange primary
   ═══════════════════════════════════════════ */
div[data-testid="stForm"] button[kind="primary"],
button[kind="primary"],
div[data-testid="stButton"] > button[kind="primary"] {
    background: var(--pcs-orange) !important;
    border: 1px solid var(--pcs-orange-hover) !important;
    color: #fff !important;
    font-weight: 900 !important;
    letter-spacing: -0.01em;
    border-radius: var(--pcs-radius-sm) !important;
    min-height: var(--pcs-tap) !important;
    box-shadow: 0 8px 20px rgba(234, 88, 12, 0.28) !important;
}
div[data-testid="stForm"] button[kind="primary"]:hover,
button[kind="primary"]:hover,
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: var(--pcs-orange-hover) !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]),
button[kind="secondary"] {
    background: var(--pcs-raised) !important;
    border: 1px solid var(--pcs-border-strong) !important;
    color: var(--pcs-text) !important;
    font-weight: 700 !important;
    border-radius: var(--pcs-radius-sm) !important;
    min-height: var(--pcs-tap) !important;
}

/* ═══════════════════════════════════════════
   Loop 3 — Cards / instrument
   ═══════════════════════════════════════════ */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--pcs-card) !important;
    border: 1px solid var(--pcs-border) !important;
    border-radius: var(--pcs-radius) !important;
    box-shadow: var(--pcs-shadow) !important;
    padding: calc(var(--pcs-space) * 1.5) !important;
}

/* Calculator face: transparent host; shell is the card */
[data-testid="stVerticalBlockBorderWrapper"].pcs-calc-face,
[data-testid="stVerticalBlockBorderWrapper"].pcs-calc-dark {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
    max-width: 36rem;
    margin: calc(var(--pcs-space) * 0.5) auto calc(var(--pcs-space) * 1) auto !important;
}

#pcs-face-marker,
#pcs-calc-marker {
    height: 0; margin: 0; padding: 0; overflow: hidden;
}

/* Single finished card (Loop 7: no gold ring — white/10 only) */
.pcs-dbl-shell {
    background: var(--pcs-card) !important;
    border: 1px solid var(--pcs-border-strong) !important;
    border-radius: var(--pcs-radius) !important;
    padding: calc(var(--pcs-space) * 1.25) !important;
    box-shadow: var(--pcs-shadow) !important;
    max-width: 36rem;
    margin: 0 auto !important;
}
.pcs-dbl-pad {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
}
.pcs-dbl-inner {
    display: block;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

#pcs-inputs-panel,
.pcs-face-section-inputs {
    background: var(--pcs-panel) !important;
    border: 1px solid var(--pcs-border) !important;
    border-bottom: none !important;
    border-radius: var(--pcs-radius-sm) var(--pcs-radius-sm) 0 0 !important;
    padding: calc(var(--pcs-space) * 1.25) !important;
    margin: 0 !important;
}

.pcs-face-section-results,
.pcs-partner-results {
    background: var(--pcs-panel-deep) !important;
    border-left: 1px solid var(--pcs-border) !important;
    border-right: 1px solid var(--pcs-border) !important;
    border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 0 !important;
    padding: calc(var(--pcs-space) * 1.25) !important;
    margin: 0 !important;
}

#pcs-match-panel,
.pcs-face-section-match {
    background: var(--pcs-panel) !important;
    border: 1px solid var(--pcs-border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--pcs-radius-sm) var(--pcs-radius-sm) !important;
    padding: calc(var(--pcs-space) * 1.25) !important;
    margin: 0 !important;
}

.pcs-calc-face [data-testid="stVerticalBlock"] > div { gap: 4px; }
.pcs-calc-face [data-testid="stHorizontalBlock"] {
    gap: 6px !important;
    flex-wrap: nowrap !important;
}
.pcs-calc-face [data-testid="column"],
.pcs-calc-face [data-testid="stSelectbox"],
.pcs-calc-face [data-baseweb="select"] {
    min-width: 0 !important;
    max-width: 100% !important;
    overflow: hidden !important;
}

/* Rank label only gets gold (small labels) */
.pcs-calc-face [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stWidgetLabel"] p {
    color: var(--pcs-gold) !important;
}

.pcs-calc-face [data-baseweb="select"] > div {
    border-color: var(--pcs-border-strong) !important;
}

/* ═══════════════════════════════════════════
   Loop 5 — Money engagement
   ═══════════════════════════════════════════ */
.pcs-partner-arrow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    padding: 0 2px 10px 2px;
    border-bottom: 1px solid var(--pcs-border);
    margin-bottom: 8px;
}
.pcs-partner-arrow-solo { justify-content: center; }
.pcs-partner-arrow-col { flex: 1; min-width: 0; text-align: left; }
.pcs-partner-arrow-col-new { text-align: right; }
.pcs-partner-arrow-solo .pcs-partner-arrow-col-new { text-align: center; }

.pcs-partner-arrow-loc {
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--pcs-muted);
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.pcs-partner-arrow-amt {
    font-size: clamp(1.65rem, 8vw, 2.2rem);
    font-weight: 900;
    color: var(--pcs-text);
    letter-spacing: -0.045em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.pcs-partner-arrow-amt.muted {
    color: #9AA3AC;
    font-size: clamp(1.3rem, 6.5vw, 1.75rem);
}
.pcs-partner-arrow-glyph {
    flex-shrink: 0;
    color: var(--pcs-gold);
    font-size: 1.25rem;
    font-weight: 900;
    padding: 0 2px;
}

.pcs-partner-delta-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin: 4px 0 10px 0;
}
.pcs-partner-delta-row > span:first-child {
    font-size: 0.58rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--pcs-muted);
}

.pcs-bah-delta-badge {
    display: inline-flex;
    align-items: center;
    font-size: 0.8rem;
    font-weight: 900;
    padding: 5px 10px;
    border-radius: 8px;
    letter-spacing: -0.01em;
    font-variant-numeric: tabular-nums;
}
.pcs-delta-up {
    background: rgba(52, 211, 153, 0.14);
    color: var(--pcs-success);
    border: 1px solid rgba(52, 211, 153, 0.32);
}
.pcs-delta-down {
    background: rgba(248, 113, 113, 0.12);
    color: var(--pcs-danger);
    border: 1px solid rgba(248, 113, 113, 0.32);
}
.pcs-delta-flat {
    background: rgba(255, 255, 255, 0.06);
    color: var(--pcs-text-dim);
    border: 1px solid var(--pcs-border);
}

.pcs-surplus-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    background: rgba(0, 0, 0, 0.32);
    border: 1px solid var(--pcs-border);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 0 0 6px 0;
}
.pcs-surplus-row > span:first-child {
    font-size: 0.58rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--pcs-gold);
    line-height: 1.3;
}
.pcs-surplus-badge {
    flex-shrink: 0;
    font-size: 0.72rem;
    font-weight: 900;
    padding: 4px 8px;
    border-radius: 6px;
    font-variant-numeric: tabular-nums;
}
.pcs-surplus-pos {
    background: rgba(52, 211, 153, 0.14);
    color: var(--pcs-success);
    border: 1px solid rgba(52, 211, 153, 0.28);
}
.pcs-surplus-neg {
    background: rgba(248, 113, 113, 0.12);
    color: var(--pcs-danger);
    border: 1px solid rgba(248, 113, 113, 0.28);
}
.pcs-surplus-flat {
    background: rgba(255, 255, 255, 0.05);
    color: var(--pcs-text-dim);
    border: 1px solid var(--pcs-border);
}

.pcs-cue-line {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--pcs-muted) !important;
    margin: 0 0 10px 0;
    line-height: 1.35;
}
.pcs-cue-line strong {
    color: var(--pcs-text) !important;
    font-weight: 800;
}

.pcs-partner-rollup {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 6px 8px;
    background: rgba(0, 0, 0, 0.36);
    border: 1px solid var(--pcs-border);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 0 0 10px 0;
    font-size: 0.72rem;
}
.pcs-partner-rollup > span:first-child {
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--pcs-muted);
    width: 100%;
}
.pcs-partner-rollup-mids {
    font-weight: 800;
    color: var(--pcs-text);
    font-variant-numeric: tabular-nums;
}
.pcs-partner-rollup-badge {
    font-size: 0.62rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 3px 7px;
    border-radius: 6px;
}
.pcs-roll-down {
    background: rgba(52, 211, 153, 0.14);
    color: var(--pcs-success);
    border: 1px solid rgba(52, 211, 153, 0.28);
}
.pcs-roll-up {
    background: rgba(248, 113, 113, 0.12);
    color: var(--pcs-danger);
    border: 1px solid rgba(248, 113, 113, 0.28);
}
.pcs-roll-flat {
    background: rgba(255, 255, 255, 0.05);
    color: var(--pcs-text-dim);
    border: 1px solid var(--pcs-border);
}

.pcs-partner-breakdown {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.pcs-partner-breakdown-title {
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--pcs-muted);
    margin: 6px 0 2px 0;
}
.pcs-est-heads-live {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 6px;
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--pcs-muted);
    padding: 0 2px;
}
.pcs-est-heads-live span:last-child {
    text-align: right;
    color: var(--pcs-text-dim);
}

.pcs-est-row {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 6px;
    background: rgba(0, 0, 0, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 10px;
    min-height: 42px;
}
.pcs-est-row-emph {
    border-color: rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.04);
}
.pcs-est-side {
    font-size: 0.76rem;
    font-weight: 700;
    color: #9AA3AC;
    font-variant-numeric: tabular-nums;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.pcs-est-side-new {
    text-align: right;
    color: var(--pcs-text);
    font-weight: 800;
}
.pcs-est-label {
    font-size: 0.52rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--pcs-muted);
    text-align: center;
    line-height: 1.25;
    max-width: 7.2rem;
}
.pcs-est-row-emph .pcs-est-label { color: var(--pcs-text-dim); }

.pcs-partner-foot {
    margin-top: 10px;
    font-size: 0.6rem;
    font-weight: 600;
    color: var(--pcs-muted);
    text-align: center;
    line-height: 1.4;
}

/* FAQ */
.pcs-faq-grid { display: grid; gap: 6px; }
.pcs-faq-item {
    display: flex;
    flex-direction: column;
    gap: 2px;
    background: rgba(0, 0, 0, 0.26);
    border: 1px solid var(--pcs-border);
    border-radius: 10px;
    padding: 8px 10px;
}
.pcs-faq-item strong {
    font-size: 0.7rem;
    color: var(--pcs-gold);
    font-weight: 800;
}
.pcs-faq-item span {
    font-size: 0.74rem;
    color: var(--pcs-text-dim);
    line-height: 1.35;
}

.pcs-footer {
    text-align: center;
    color: var(--pcs-muted);
    font-size: 0.68rem;
    padding: 12px 0 4px 0;
    border-top: 1px solid var(--pcs-border);
    margin-top: 10px;
    line-height: 1.45;
}
.pcs-footer strong { color: var(--pcs-text); font-weight: 800; }
.pcs-footer span { display: block; margin-top: 2px; }

/* ═══════════════════════════════════════════
   Loop 6 — Cross-page skin
   ═══════════════════════════════════════════ */
.pcs-step-context {
    background: var(--pcs-card);
    border: 1px solid var(--pcs-border);
    border-radius: var(--pcs-radius-sm);
    padding: 12px;
    margin: 0 0 12px 0;
}
.pcs-step-context-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 8px;
}
.pcs-step-context-chip {
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 5px 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.06);
    color: var(--pcs-text-dim);
    border: 1px solid var(--pcs-border);
}
.pcs-step-context-chip:first-child {
    background: rgba(212, 175, 55, 0.12);
    color: var(--pcs-gold);
    border-color: rgba(212, 175, 55, 0.25);
}
.pcs-step-context-chip.muted {
    background: rgba(255, 255, 255, 0.05);
    color: var(--pcs-muted);
}
.pcs-step-context-why,
.pcs-step-context-need {
    font-size: 0.76rem;
    color: var(--pcs-text-dim);
    line-height: 1.4;
    margin: 4px 0 0 0;
}

.pcs-form-steps, .pcs-steps {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2px;
    margin: 4px 0 12px 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
.pcs-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    min-width: 2.5rem;
    flex: 1;
}
.pcs-step-circle {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-weight: 900;
    background: var(--pcs-control);
    color: var(--pcs-muted);
    border: 1px solid var(--pcs-border);
}
.pcs-step.active .pcs-step-circle,
.pcs-step.current .pcs-step-circle {
    background: var(--pcs-orange);
    color: #fff;
    border-color: var(--pcs-orange-hover);
}
.pcs-step.done .pcs-step-circle,
.pcs-step.completed .pcs-step-circle {
    background: rgba(52, 211, 153, 0.18);
    color: var(--pcs-success);
    border-color: rgba(52, 211, 153, 0.35);
}
.pcs-step-connector.completed {
    background: rgba(52, 211, 153, 0.45);
}
.pcs-step-label {
    font-size: 0.52rem;
    font-weight: 700;
    color: var(--pcs-muted);
    text-align: center;
    line-height: 1.2;
}
.pcs-step-connector {
    flex: 0.35;
    height: 2px;
    background: var(--pcs-border);
    margin-bottom: 16px;
}
.pcs-form-nav-rule {
    border: none;
    border-top: 1px solid var(--pcs-border);
    margin: 12px 0;
}

.pcs-payment-cancelled {
    background: var(--pcs-card) !important;
    border: 1px solid var(--pcs-border) !important;
    border-left: 3px solid var(--pcs-gold) !important;
    border-radius: var(--pcs-radius-sm) !important;
    padding: 12px 14px !important;
    color: var(--pcs-text-dim) !important;
    font-size: 0.86rem;
    line-height: 1.5;
}
.pcs-payment-cancelled strong {
    color: var(--pcs-text);
    font-weight: 800;
}
.pcs-pay-reassurance {
    font-size: 0.72rem;
    color: var(--pcs-muted);
    text-align: center;
    margin-top: 8px;
}

.pcs-bah-report-banner {
    background: var(--pcs-panel-deep);
    border: 1px solid var(--pcs-border);
    border-radius: var(--pcs-radius-sm);
    padding: 12px 14px;
    margin: 8px 0 12px 0;
}
.pcs-bah-report-amount {
    font-size: 1.7rem;
    font-weight: 900;
    color: var(--pcs-text);
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
}
.pcs-bah-report-delta {
    font-size: 0.78rem;
    font-weight: 800;
    margin-top: 4px;
}
.pcs-report-howto {
    background: var(--pcs-card);
    border: 1px solid var(--pcs-border);
    border-radius: var(--pcs-radius-sm);
    padding: 12px;
    color: var(--pcs-text-dim);
    font-size: 0.78rem;
    line-height: 1.45;
}
.pcs-rank-auto { font-size: 0.72rem; color: var(--pcs-muted); }

.pcs-gen-panel {
    background: var(--pcs-card);
    border: 1px solid var(--pcs-border);
    border-radius: var(--pcs-radius);
    padding: 14px;
    box-shadow: var(--pcs-shadow);
}
.pcs-gen-panel-title {
    font-size: 1rem;
    font-weight: 900;
    color: var(--pcs-text);
}
.pcs-gen-panel-sub {
    font-size: 0.76rem;
    color: var(--pcs-muted);
    margin-top: 4px;
}
.pcs-gen-progress-track {
    height: 6px;
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 10px;
}
.pcs-gen-progress-bar {
    height: 100%;
    background: var(--pcs-orange);
    border-radius: 999px;
}
.pcs-gen-sections-label {
    font-size: 0.55rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--pcs-muted);
    margin-top: 12px;
}
.pcs-gen-section-chip {
    display: inline-block;
    font-size: 0.64rem;
    font-weight: 700;
    color: var(--pcs-text-dim);
    background: rgba(0,0,0,0.32);
    border: 1px solid var(--pcs-border);
    border-radius: 999px;
    padding: 3px 8px;
    margin: 4px 4px 0 0;
}
.pcs-gen-steps { display: flex; gap: 8px; margin-top: 12px; }
.pcs-gen-step {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 0.68rem;
    color: var(--pcs-muted);
}
.pcs-gen-step-dot {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background: var(--pcs-border-strong);
}
.pcs-gen-foot {
    font-size: 0.66rem;
    color: var(--pcs-muted);
    margin-top: 10px;
}

.pcs-preview-wrap,
.pcs-preview-doc {
    background: var(--pcs-card);
    border: 1px solid var(--pcs-border);
    border-radius: var(--pcs-radius-sm);
    overflow: hidden;
}
.pcs-preview-header,
.pcs-preview-doc-bar {
    padding: 10px 12px;
    border-bottom: 1px solid var(--pcs-border);
}
.pcs-preview-doc-title,
.pcs-preview-sub { color: var(--pcs-text); font-weight: 800; }
.pcs-preview-doc-meta,
.pcs-preview-doc-badge { color: var(--pcs-muted); font-size: 0.68rem; }
.pcs-preview-section {
    padding: 10px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.pcs-preview-section-num { color: var(--pcs-gold); font-weight: 900; font-size: 0.68rem; }
.pcs-preview-section-title { color: var(--pcs-text); font-weight: 800; font-size: 0.84rem; }
.pcs-preview-section-body,
.pcs-preview-blur-content,
.pcs-preview-blur-note,
.pcs-preview-blur-list { color: var(--pcs-text-dim); font-size: 0.76rem; }
.pcs-preview-blur-fade { background: linear-gradient(transparent, var(--pcs-card)); }
.pcs-preview-blur-label { color: var(--pcs-gold); font-weight: 800; font-size: 0.7rem; }
.pcs-preview-table { width: 100%; font-size: 0.74rem; color: var(--pcs-text-dim); }

html.pcs-has-sticky-ref .block-container {
    padding-bottom: calc(var(--pcs-space) * 16) !important;
}

hr { border-color: var(--pcs-border) !important; }
.pcs-results-kicker,
.pcs-face-divider,
.pcs-panel-label,
.pcs-match-body { display: none !important; }

/* ═══════════════════════════════════════════
   Loop 4 — Mobile 390px first
   ═══════════════════════════════════════════ */
@media (max-width: 430px) {
    .block-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
        padding-top: 4px !important;
        padding-bottom: 118px !important;
    }
    .pcs-dbl-shell {
        padding: 10px !important;
        border-radius: 16px !important;
    }
    .pcs-partner-arrow-amt {
        font-size: clamp(1.45rem, 9vw, 1.85rem);
    }
    .pcs-partner-arrow-amt.muted {
        font-size: clamp(1.15rem, 7vw, 1.45rem);
    }
    .pcs-est-label { font-size: 0.48rem; max-width: 5.5rem; }
    .pcs-est-side { font-size: 0.68rem; }
    .pcs-calc-face [data-testid="stHorizontalBlock"] { gap: 4px !important; }
    .pcs-face-brand .pcs-brand-title { font-size: 0.95rem; }
    #pcs-inputs-panel,
    .pcs-face-section-inputs,
    .pcs-face-section-results,
    #pcs-match-panel {
        padding: 10px !important;
    }
}

.stApp, .block-container, .pcs-calc-face, .pcs-dbl-shell {
    overflow-x: hidden !important;
    max-width: 100vw;
}
</style>
"""


def apply_styles() -> None:
    """Inject global CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

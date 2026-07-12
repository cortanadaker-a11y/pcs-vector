"""Helpers for safe HTML and Streamlit markdown rendering."""

from __future__ import annotations

import html


def safe_html(text: str) -> str:
    """Escape text for HTML blocks and neutralize Streamlit LaTeX ($...$)."""
    return html.escape(text, quote=False).replace("$", "&#36;")


def safe_markdown(text: str) -> str:
    """Escape dollar signs so Streamlit does not treat them as LaTeX."""
    return text.replace("$", r"\$")
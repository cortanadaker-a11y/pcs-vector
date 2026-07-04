"""Grok API configuration — loaded from secrets.toml or environment variables."""

from __future__ import annotations

import os


class GrokConfigError(Exception):
    """Raised when required Grok configuration is missing."""


GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_MODEL = "grok-3"
GROK_TIMEOUT_SECONDS = 120


def _from_streamlit_secrets(key_path: str) -> str | None:
    try:
        import streamlit as st

        node = st.secrets
        for part in key_path.split("."):
            node = node[part]
        value = str(node).strip() if node else ""
        return value or None
    except Exception:
        return None


def get_grok_api_key() -> str:
    """Resolve Grok API key from secrets.toml or environment."""
    key = _from_streamlit_secrets("grok.api_key") or os.environ.get("GROK_API_KEY", "").strip()
    if not key:
        raise GrokConfigError(
            "Grok API key not found. Add [grok] api_key to `.streamlit/secrets.toml` "
            "or set the GROK_API_KEY environment variable."
        )
    return key
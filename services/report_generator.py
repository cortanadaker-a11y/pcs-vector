"""Grok-powered PCS strategic report generator."""

from __future__ import annotations

from typing import Any

from services.grok_client import GrokAPIError, call_grok
from services.prompts import SYSTEM_PROMPT, build_user_prompt


def generate_report(form_data: dict[str, Any]) -> str:
    """Generate a full markdown PCS report via the Grok API."""
    user_prompt = build_user_prompt(form_data)
    report = call_grok(SYSTEM_PROMPT, user_prompt)
    return _normalize_report(report)


def _normalize_report(report: str) -> str:
    """Ensure the report opens with the expected title heading."""
    text = report.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("markdown"):
            text = text[8:].strip()
    if not text.startswith("# PCS Vector"):
        text = f"# PCS Vector Strategic Plan\n\n{text}"
    return text


__all__ = ["generate_report", "GrokAPIError"]
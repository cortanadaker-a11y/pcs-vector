"""xAI Grok API client for PCS Vector report generation."""

from __future__ import annotations

import json
import logging
from typing import Any

import requests

from services.grok_config import (
    GROK_API_URL,
    GROK_MODEL,
    GROK_TIMEOUT_SECONDS,
    GrokConfigError,
    get_grok_api_key,
)

logger = logging.getLogger(__name__)


class GrokAPIError(Exception):
    """Raised when the Grok API returns an error or unexpected response."""


def call_grok(system_prompt: str, user_prompt: str) -> str:
    """Send a chat completion request to Grok and return assistant text."""
    try:
        api_key = get_grok_api_key()
    except GrokConfigError as exc:
        raise GrokAPIError(str(exc)) from exc

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: dict[str, Any] = {
        "model": GROK_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
        "max_completion_tokens": 6000,
    }

    try:
        response = requests.post(
            GROK_API_URL,
            headers=headers,
            json=payload,
            timeout=GROK_TIMEOUT_SECONDS,
        )
    except requests.Timeout as exc:
        logger.warning("Grok API request timed out")
        raise GrokAPIError(
            "The report request timed out. Please try again in a moment."
        ) from exc
    except requests.RequestException as exc:
        logger.warning("Grok API request failed: %s", exc)
        raise GrokAPIError(
            "Could not reach the Grok API. Check your internet connection and try again."
        ) from exc

    if response.status_code != 200:
        detail = _extract_error_detail(response)
        logger.warning("Grok API error %s: %s", response.status_code, detail)
        raise GrokAPIError(
            f"Grok API error ({response.status_code}): {detail}"
        )

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        raise GrokAPIError(
            "Received an unexpected response format from the Grok API."
        ) from exc

    if not content or not str(content).strip():
        raise GrokAPIError("Grok returned an empty report. Please try again.")

    return str(content).strip()


def _extract_error_detail(response: requests.Response) -> str:
    try:
        body = response.json()
        if isinstance(body, dict) and "error" in body:
            err = body["error"]
            if isinstance(err, dict):
                return err.get("message", str(err))
            return str(err)
        return response.text[:300]
    except Exception:
        return response.text[:300] or "Unknown error"
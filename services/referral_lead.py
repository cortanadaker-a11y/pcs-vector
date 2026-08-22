"""Housing referral leads — structured for Google Form / Sheet columns.

Google Form column headers (exact):
  Location | First name | Last name | Rank | Dependents | Email address | Rent / Buy / Not sure

Wire-up (Streamlit secrets):

  [google_form]
  form_action_url = "https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse"
  # Paste entry.XXXX IDs from a prefilled link (see VIEWFORM → Get pre-filled link)
  entry_location = "entry.111111"
  entry_first_name = "entry.222222"
  entry_last_name = "entry.333333"
  entry_rank = "entry.444444"
  entry_dependents = "entry.555555"
  entry_email_address = "entry.666666"
  entry_rent_buy_not_sure = "entry.777777"
"""

from __future__ import annotations

import logging
import os
from typing import Any
from urllib.parse import urlencode

import requests

logger = logging.getLogger("pcs_vector.referral")

# Exact headers to use on the Google Form / linked Sheet
REFERRAL_COLUMNS = (
    "Location",
    "First name",
    "Last name",
    "Rank",
    "Dependents",
    "Email address",
    "Rent / Buy / Not sure",
)

# Internal keys ↔ Form column headers
FIELD_KEYS = {
    "location": "Location",
    "first_name": "First name",
    "last_name": "Last name",
    "rank": "Rank",
    "dependents": "Dependents",
    "email_address": "Email address",
    "rent_buy_not_sure": "Rent / Buy / Not sure",
}

INTEREST_OPTIONS = ("Rent", "Buy", "Not sure")


def build_referral_row(
    *,
    location: str,
    first_name: str,
    last_name: str,
    rank: str,
    dependents: str,
    email_address: str,
    rent_buy_not_sure: str,
) -> dict[str, str]:
    """Return a row dict keyed by Google Form / Sheet column headers."""
    interest = (rent_buy_not_sure or "").strip()
    if interest not in INTEREST_OPTIONS:
        interest = "Not sure"
    return {
        "Location": (location or "").strip(),
        "First name": (first_name or "").strip(),
        "Last name": (last_name or "").strip(),
        "Rank": (rank or "").strip(),
        "Dependents": (dependents or "").strip(),
        "Email address": (email_address or "").strip(),
        "Rent / Buy / Not sure": interest,
    }


def format_dependents_label(*, with_dependents: bool, num_dependents: int) -> str:
    if not with_dependents or num_dependents <= 0:
        return "Without dependents"
    n = int(num_dependents)
    if n >= 5:
        return "With dependents (5+)"
    return f"With dependents ({n})"


def format_rank_label(pay_grade: str | None, rank_name: str | None = None) -> str:
    grade = (pay_grade or "").strip()
    name = (rank_name or "").strip()
    if grade and name and name != grade:
        return f"{grade} — {name}"
    return grade or name or ""


def _from_secrets(path: str) -> str | None:
    try:
        import streamlit as st

        node: Any = st.secrets
        for part in path.split("."):
            if part not in node:
                return None
            node = node[part]
        val = str(node).strip()
        return val or None
    except Exception:
        return None


def google_form_configured() -> bool:
    url = _from_secrets("google_form.form_action_url") or os.environ.get(
        "PCS_GOOGLE_FORM_ACTION_URL", ""
    )
    return bool(url and "formResponse" in url)


def _entry_map() -> dict[str, str]:
    """Map column header → Google Form entry.ID."""
    mapping = {}
    pairs = (
        ("Location", "entry_location"),
        ("First name", "entry_first_name"),
        ("Last name", "entry_last_name"),
        ("Rank", "entry_rank"),
        ("Dependents", "entry_dependents"),
        ("Email address", "entry_email_address"),
        ("Rent / Buy / Not sure", "entry_rent_buy_not_sure"),
    )
    for header, secret_key in pairs:
        eid = _from_secrets(f"google_form.{secret_key}") or os.environ.get(
            f"PCS_GOOGLE_FORM_{secret_key.upper()}", ""
        )
        if eid:
            mapping[header] = eid.strip()
    return mapping


def submit_referral_to_google_form(row: dict[str, str]) -> tuple[bool, str]:
    """POST a referral row to a Google Form formResponse endpoint.

    Returns (ok, message).
    """
    url = _from_secrets("google_form.form_action_url") or os.environ.get(
        "PCS_GOOGLE_FORM_ACTION_URL", ""
    ).strip()
    if not url or "formResponse" not in url:
        return False, "Google Form is not configured yet."

    entries = _entry_map()
    missing = [h for h in REFERRAL_COLUMNS if h not in entries]
    if missing:
        return False, f"Google Form entry IDs missing for: {', '.join(missing)}"

    payload = {entries[h]: row.get(h, "") for h in REFERRAL_COLUMNS}
    try:
        # Google Forms expects form-urlencoded body; 200 even on success (often CORS-like)
        resp = requests.post(
            url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
            allow_redirects=True,
        )
        if resp.status_code >= 400:
            logger.warning("Google Form submit failed: %s %s", resp.status_code, resp.text[:200])
            return False, f"Form submit failed (HTTP {resp.status_code})."
        return True, "Submitted to Google Form."
    except requests.RequestException as exc:
        logger.exception("Google Form submit error")
        return False, f"Could not reach Google Form: {exc}"


def row_as_mapping_preview(row: dict[str, str]) -> str:
    """Human-readable preview for mapping / debugging."""
    lines = [f"{h}: {row.get(h, '')}" for h in REFERRAL_COLUMNS]
    return "\n".join(lines)


__all__ = [
    "FIELD_KEYS",
    "INTEREST_OPTIONS",
    "REFERRAL_COLUMNS",
    "build_referral_row",
    "format_dependents_label",
    "format_rank_label",
    "google_form_configured",
    "row_as_mapping_preview",
    "submit_referral_to_google_form",
]

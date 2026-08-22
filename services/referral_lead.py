"""Housing referral leads — mapped to the PCS Vector Google Form.

Live Form:
  https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform

Form questions → entry IDs:
  Destination          → entry.159372216
  First Name           → entry.1546051705
  Last Name            → entry.1445033394
  Rank                 → entry.1001940560
  Rent/Buy/Not Sure    → entry.1608004035

(Rent Range removed from the app — do not send.)
Not on Form yet (still collected in-app): Dependents, Email address.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any
from urllib.parse import urlencode

import requests

logger = logging.getLogger("pcs_vector.referral")

# Fields we POST / prefill to the Google Form
REFERRAL_COLUMNS = (
    "Destination",
    "First Name",
    "Last Name",
    "Rank",
    "Rent/Buy/Not Sure",
)

EXTRA_COLUMNS = (
    "Dependents",
    "Email address",
)

INTEREST_OPTIONS = ("Rent", "Buy", "Not sure")

_DEFAULT_FORM_ACTION = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/formResponse"
)
_DEFAULT_ENTRIES = {
    "Destination": "entry.159372216",
    "First Name": "entry.1546051705",
    "Last Name": "entry.1445033394",
    "Rank": "entry.1001940560",
    "Rent/Buy/Not Sure": "entry.1608004035",
}


def build_referral_row(
    *,
    destination: str,
    first_name: str,
    last_name: str,
    rank: str,
    rent_buy_not_sure: str,
    dependents: str = "",
    email_address: str = "",
) -> dict[str, str]:
    """Return a row dict keyed by Form question titles (+ extras)."""
    interest = (rent_buy_not_sure or "").strip()
    if interest not in INTEREST_OPTIONS:
        low = interest.lower()
        if "rent" in low:
            interest = "Rent"
        elif "buy" in low:
            interest = "Buy"
        else:
            interest = "Not sure"
    return {
        "Destination": (destination or "").strip(),
        "First Name": (first_name or "").strip(),
        "Last Name": (last_name or "").strip(),
        "Rank": (rank or "").strip(),
        "Rent/Buy/Not Sure": interest,
        "Dependents": (dependents or "").strip(),
        "Email address": (email_address or "").strip(),
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
    url = (
        _from_secrets("google_form.form_action_url")
        or os.environ.get("PCS_GOOGLE_FORM_ACTION_URL", "")
        or _DEFAULT_FORM_ACTION
    )
    return bool(url and "formResponse" in url)


def _form_action_url() -> str:
    return (
        _from_secrets("google_form.form_action_url")
        or os.environ.get("PCS_GOOGLE_FORM_ACTION_URL", "")
        or _DEFAULT_FORM_ACTION
    ).strip()


def _entry_map() -> dict[str, str]:
    secret_keys = {
        "Destination": "entry_destination",
        "First Name": "entry_first_name",
        "Last Name": "entry_last_name",
        "Rank": "entry_rank",
        "Rent/Buy/Not Sure": "entry_rent_buy_not_sure",
        "Dependents": "entry_dependents",
        "Email address": "entry_email_address",
    }
    mapping = dict(_DEFAULT_ENTRIES)
    for header, secret_key in secret_keys.items():
        eid = _from_secrets(f"google_form.{secret_key}") or os.environ.get(
            f"PCS_GOOGLE_FORM_{secret_key.upper()}", ""
        )
        if eid:
            mapping[header] = eid.strip()
    return mapping


def build_prefill_url(row: dict[str, str]) -> str:
    """Build a Google Form pre-filled link (Soldier clicks Submit once)."""
    view = _form_action_url().replace("/formResponse", "/viewform")
    entries = _entry_map()
    params: dict[str, str] = {"usp": "pp_url"}
    for header in REFERRAL_COLUMNS:
        eid = entries.get(header)
        if eid:
            params[eid] = row.get(header, "")
    for header in EXTRA_COLUMNS:
        eid = entries.get(header)
        if eid and row.get(header):
            params[eid] = row.get(header, "")
    return f"{view}?{urlencode(params)}"


def submit_referral_to_google_form(row: dict[str, str]) -> tuple[bool, str]:
    """POST mapped calculator + contact fields to Google Form."""
    url = _form_action_url()
    if not url or "formResponse" not in url:
        return False, "Google Form is not configured yet."

    entries = _entry_map()
    payload: dict[str, str] = {}
    for header in REFERRAL_COLUMNS:
        eid = entries.get(header)
        if eid:
            payload[eid] = row.get(header, "")

    for header in EXTRA_COLUMNS:
        eid = entries.get(header)
        if eid and row.get(header):
            payload[eid] = row.get(header, "")

    if not payload:
        return False, "No Google Form entry IDs configured."

    try:
        view = url.replace("/formResponse", "/viewform")
        session = requests.Session()
        html = session.get(view, timeout=15).text
        fbzx_m = re.search(r'name="fbzx"\s+value="([^"]+)"', html)
        if fbzx_m:
            payload["fbzx"] = fbzx_m.group(1)
            payload["fvv"] = "1"
            payload["pageHistory"] = "0"
            payload["submissionTimestamp"] = "-1"

        resp = session.post(
            url,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": view,
                "Origin": "https://docs.google.com",
            },
            timeout=15,
            allow_redirects=True,
        )
        body = (resp.text or "").lower()
        if resp.status_code < 400 and (
            "response has been recorded" in body or "your response" in body
        ):
            return True, "Submitted to Google Form."
        if resp.status_code >= 400:
            logger.warning("Google Form submit failed: %s %s", resp.status_code, resp.text[:200])
            return False, f"Form submit failed (HTTP {resp.status_code})."
        return True, "Submitted to Google Form."
    except requests.RequestException as exc:
        logger.exception("Google Form submit error")
        return False, f"Could not reach Google Form: {exc}"


__all__ = [
    "EXTRA_COLUMNS",
    "INTEREST_OPTIONS",
    "REFERRAL_COLUMNS",
    "build_prefill_url",
    "build_referral_row",
    "format_dependents_label",
    "format_rank_label",
    "google_form_configured",
    "submit_referral_to_google_form",
]

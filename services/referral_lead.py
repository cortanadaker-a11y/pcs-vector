"""Housing referral leads — Google Form handoff.

Live Form:
  https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform

Form questions → entry IDs:
  Email Address            → entry.1162277939
  Destination              → entry.159372216
  First Name               → entry.1546051705
  Last Name                → entry.1445033394
  Rank                     → entry.1001940560
  Number of Dependents     → entry.1983274092
  Rent/Buy/Not Sure        → entry.1608004035
"""

from __future__ import annotations

import logging
import os
from typing import Any
from urllib.parse import urlencode

import requests

logger = logging.getLogger("pcs_vector.referral")

# Fields sent on the pre-filled Google Form URL
REFERRAL_COLUMNS = (
    "Email address",
    "Destination",
    "First Name",
    "Last Name",
    "Rank",
    "Number of Dependents",
    "Rent/Buy/Not Sure",
)

EXTRA_COLUMNS: tuple[str, ...] = ()

INTEREST_OPTIONS = ("Rent", "Buy", "Not sure")

_DEFAULT_FORM_ACTION = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/formResponse"
)
_DEFAULT_ENTRIES = {
    "Email address": "entry.1162277939",
    "Destination": "entry.159372216",
    "First Name": "entry.1546051705",
    "Last Name": "entry.1445033394",
    "Rank": "entry.1001940560",
    "Number of Dependents": "entry.1983274092",
    "Rent/Buy/Not Sure": "entry.1608004035",
}


def build_referral_row(
    *,
    destination: str,
    first_name: str,
    last_name: str,
    rank: str,
    rent_buy_not_sure: str,
    num_dependents: int = 0,
    email_address: str = "",
) -> dict[str, str]:
    """Row keyed by Form question titles (+ email for Apps Script / future Form field)."""
    interest = (rent_buy_not_sure or "").strip()
    if interest not in INTEREST_OPTIONS:
        low = interest.lower()
        if "rent" in low:
            interest = "Rent"
        elif "buy" in low:
            interest = "Buy"
        else:
            interest = "Not sure"
    deps_n = max(0, int(num_dependents))
    return {
        "Destination": (destination or "").strip(),
        "First Name": (first_name or "").strip(),
        "Last Name": (last_name or "").strip(),
        "Rank": (rank or "").strip(),
        # Form field is "Number of Dependents" — send a plain number
        "Number of Dependents": str(deps_n),
        "Rent/Buy/Not Sure": interest,
        "Email address": (email_address or "").strip(),
        # Friendly label for UI / Apps Script
        "Dependents": format_dependents_label(
            with_dependents=deps_n > 0, num_dependents=deps_n
        ),
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


def _form_action_url() -> str:
    return (
        _from_secrets("google_form.form_action_url")
        or os.environ.get("PCS_GOOGLE_FORM_ACTION_URL", "")
        or _DEFAULT_FORM_ACTION
    ).strip()


def _apps_script_url() -> str:
    return (
        _from_secrets("google_form.apps_script_url")
        or os.environ.get("PCS_GOOGLE_APPS_SCRIPT_URL", "")
        or ""
    ).strip()


def _entry_map() -> dict[str, str]:
    secret_keys = {
        "Email address": "entry_email_address",
        "Destination": "entry_destination",
        "First Name": "entry_first_name",
        "Last Name": "entry_last_name",
        "Rank": "entry_rank",
        "Number of Dependents": "entry_dependents",
        "Rent/Buy/Not Sure": "entry_rent_buy_not_sure",
    }
    mapping = dict(_DEFAULT_ENTRIES)
    for header, secret_key in secret_keys.items():
        eid = _from_secrets(f"google_form.{secret_key}") or os.environ.get(
            f"PCS_GOOGLE_FORM_{secret_key.upper()}", ""
        )
        if eid:
            mapping[header] = eid.strip()
    return mapping


def _payload_pairs(row: dict[str, str]) -> list[tuple[str, str]]:
    entries = _entry_map()
    pairs: list[tuple[str, str]] = []
    for header in REFERRAL_COLUMNS:
        eid = entries.get(header)
        if eid:
            pairs.append((eid, row.get(header, "")))
    for header in EXTRA_COLUMNS:
        eid = entries.get(header)
        if eid and row.get(header):
            pairs.append((eid, row.get(header, "")))
    return pairs


def build_prefill_url(row: dict[str, str]) -> str:
    """Google Form URL with calculator + contact fields filled."""
    view = _form_action_url().replace("/formResponse", "/viewform")
    params: dict[str, str] = {"usp": "pp_url"}
    for eid, value in _payload_pairs(row):
        params[eid] = value
    return f"{view}?{urlencode(params)}"


def submit_referral_via_apps_script(row: dict[str, str]) -> tuple[bool, str]:
    url = _apps_script_url()
    if not url:
        return False, "Apps Script webhook not configured."
    try:
        resp = requests.post(url, json=row, timeout=20)
        if resp.status_code >= 400:
            return False, f"Apps Script HTTP {resp.status_code}"
        return True, "Saved via Apps Script."
    except requests.RequestException as exc:
        logger.exception("Apps Script submit failed")
        return False, str(exc)


def build_redirect_to_form_html(row: dict[str, str]) -> str:
    """Send the browser to the pre-filled Google Form (same tab)."""
    import json as _json

    prefill = build_prefill_url(row)
    prefill_js = _json.dumps(prefill)
    return f"""
<div style="font-family:system-ui,sans-serif;font-size:0.95rem;color:#2a4a3f;padding:0.35rem 0;">
  Opening Google Form with your info filled in…
</div>
<script>
(function () {{
  var url = {prefill_js};
  function go(u) {{
    try {{ window.top.location.assign(u); return; }} catch (e1) {{}}
    try {{ window.parent.location.assign(u); return; }} catch (e2) {{}}
    try {{ window.location.assign(u); return; }} catch (e3) {{}}
    window.open(u, "_blank", "noopener,noreferrer");
  }}
  go(url);
}})();
</script>
"""


__all__ = [
    "EXTRA_COLUMNS",
    "INTEREST_OPTIONS",
    "REFERRAL_COLUMNS",
    "build_prefill_url",
    "build_redirect_to_form_html",
    "build_referral_row",
    "format_dependents_label",
    "format_rank_label",
    "submit_referral_via_apps_script",
]

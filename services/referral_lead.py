"""Housing referral leads — mapped to the PCS Vector Google Form.

Live Form:
  https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform

Form questions → entry IDs:
  Destination          → entry.159372216
  First Name           → entry.1546051705
  Last Name            → entry.1445033394
  Rank                 → entry.1001940560
  Rent/Buy/Not Sure    → entry.1608004035
"""

from __future__ import annotations

import html as html_lib
import json
import logging
import os
from typing import Any
from urllib.parse import urlencode

logger = logging.getLogger("pcs_vector.referral")

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


def _payload_pairs(row: dict[str, str]) -> list[tuple[str, str]]:
    """(entry.ID, value) pairs for Form fields we know how to map."""
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
    """Pre-filled viewform URL (fields filled; Soldier may still hit Submit)."""
    view = _form_action_url().replace("/formResponse", "/viewform")
    params: dict[str, str] = {"usp": "pp_url"}
    for eid, value in _payload_pairs(row):
        params[eid] = value
    return f"{view}?{urlencode(params)}"


def build_direct_submit_url(row: dict[str, str]) -> str:
    """formResponse URL that attempts to record the response in one navigation."""
    action = _form_action_url()
    params: dict[str, str] = {"submit": "Submit"}
    for eid, value in _payload_pairs(row):
        params[eid] = value
    return f"{action}?{urlencode(params)}"


def build_one_click_submit_html(row: dict[str, str]) -> str:
    """JS that runs in-page (st.html + unsafe_allow_javascript) to POST the Form.

    Strategy (best UX that still works around Google blocking server POSTs):
      1. POST via a temporary form targeting a new tab (records response when allowed)
      2. Also open the pre-filled Form so the Soldier sees confirmation / can Submit
         if Google blocked the silent POST.
    """
    action = _form_action_url()
    prefill = build_prefill_url(row)
    pairs = _payload_pairs(row)

    # Build inputs in JS to avoid quote-escaping headaches
    fields_json = json.dumps([{ "name": eid, "value": val } for eid, val in pairs])
    action_js = json.dumps(action)
    prefill_js = json.dumps(prefill)

    return f"""
<div id="pcs-ref-status" style="font-family:system-ui,sans-serif;font-size:0.92rem;color:#2a4a3f;">
  Sending your referral to Google Form…
</div>
<script>
(function () {{
  var action = {action_js};
  var prefill = {prefill_js};
  var fields = {fields_json};

  function postForm() {{
    var form = document.createElement("form");
    form.method = "POST";
    form.action = action;
    form.target = "_blank";
    form.style.display = "none";
    fields.forEach(function (f) {{
      var input = document.createElement("input");
      input.type = "hidden";
      input.name = f.name;
      input.value = f.value;
      form.appendChild(input);
    }});
    document.body.appendChild(form);
    form.submit();
    setTimeout(function () {{
      try {{ form.remove(); }} catch (e) {{}}
    }}, 1000);
  }}

  try {{
    postForm();
    var el = document.getElementById("pcs-ref-status");
    if (el) {{
      el.textContent = "Referral sent. Check the new tab for Google’s confirmation.";
    }}
  }} catch (err) {{
    window.open(prefill, "_blank");
    var el2 = document.getElementById("pcs-ref-status");
    if (el2) {{
      el2.textContent = "Opened the Google Form with your answers — click Submit there.";
    }}
  }}
}})();
</script>
"""


__all__ = [
    "EXTRA_COLUMNS",
    "INTEREST_OPTIONS",
    "REFERRAL_COLUMNS",
    "build_direct_submit_url",
    "build_one_click_submit_html",
    "build_prefill_url",
    "build_referral_row",
    "format_dependents_label",
    "format_rank_label",
    "google_form_configured",
]

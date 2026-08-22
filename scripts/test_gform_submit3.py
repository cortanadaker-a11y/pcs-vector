#!/usr/bin/env python3
import re
from html.parser import HTMLParser

import requests

view = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform"
)
url = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/formResponse"
)

s = requests.Session()
html = s.get(view, timeout=20).text

# Collect all input name=value from the form
names = re.findall(
    r'<input[^>]+name="([^"]+)"[^>]*(?:value="([^"]*)")?',
    html,
    flags=re.I,
)
print("inputs found", len(names))
for n, v in names:
    if n.startswith("entry.") or n in {"fbzx", "fvv", "pageHistory", "submissionTimestamp", "draftResponse", "partialResponse"}:
        print(f"  {n}={v}")

# Build payload from hidden fields + our answers using entry names present in HTML
payload = {}
for n, v in names:
    if n.startswith("entry.") or n in {"fbzx", "fvv", "pageHistory", "submissionTimestamp"}:
        payload[n] = v or ""

# Fill entries we know - try both id sets if present
candidates = {
    "Destination": ["entry.159372216", "entry.1848213003"],
    "First Name": ["entry.1546051705", "entry.223229278"],
    "Last Name": ["entry.1445033394", "entry.112196602"],
    "Rank": ["entry.1001940560", "entry.223086250"],
    "Rent/Buy/Not Sure": ["entry.1608004035", "entry.2134536278"],
    "Rent Range": ["entry.132029913", "entry.1672369468"],
}
values = {
    "Destination": "Fort Bragg, NC",
    "First Name": "Test",
    "Last Name": "Soldier",
    "Rank": "E-5",
    "Rent/Buy/Not Sure": "Rent",
    "Rent Range": "1200-1600",
}

# Prefer entry ids that appear in HTML inputs
html_entries = {n for n, _ in names if n.startswith("entry.")}
print("html entry names", html_entries)

for label, eids in candidates.items():
    chosen = None
    for eid in eids:
        if eid in html_entries or True:
            chosen = eid
            break
    # Prefer nested (first in list) if not in html
    for eid in eids:
        if eid in html_entries:
            chosen = eid
            break
    if chosen is None:
        chosen = eids[0]
    payload[chosen] = values[label]
    print("using", label, chosen)

# Ensure control fields
if "fvv" not in payload:
    payload["fvv"] = "1"
if "pageHistory" not in payload:
    payload["pageHistory"] = "0"

r = s.post(url, data=payload, timeout=20, headers={"Referer": view})
print("status", r.status_code, "final", r.url)
print("has submitted", "Your response has been recorded" in r.text or "submitted" in r.text.lower())
# Save for inspection
open("/tmp/gform_resp.html", "w").write(r.text)
# look for freebirdFormviewerViewResponseConfirmationMessage
if "Confirmation" in r.text or "recorded" in r.text.lower():
    print("SUCCESS marker found")
else:
    # print title
    t = re.search(r"<title>([^<]+)", r.text)
    print("title", t.group(1) if t else None)

#!/usr/bin/env python3
import re
import requests

base = "https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg"
view = base + "/viewform"
post = base + "/formResponse"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://docs.google.com",
    "Referer": view,
}

s = requests.Session()
html = s.get(view, headers=headers, timeout=20).text
fbzx = re.search(r'name="fbzx"\s+value="([^"]+)"', html).group(1)
print("fbzx", fbzx)

# Try nested IDs with full browser-like POST
payload = {
    "entry.159372216": "Fort Bragg, NC",
    "entry.1546051705": "Test",
    "entry.1445033394": "Soldier",
    "entry.1001940560": "E-5 — Sergeant",
    "entry.1608004035": "Rent",
    "entry.132029913": "$1,200–$1,650/mo",
    "fvv": "1",
    "partialResponse": "[null,null,\"" + fbzx + "\"]",
    "pageHistory": "0",
    "fbzx": fbzx,
    "submissionTimestamp": "-1",
}
r = s.post(post, data=payload, headers=headers, timeout=20)
print("status", r.status_code)
print("recorded", "response has been recorded" in r.text.lower())
# dump interesting bits
open("/tmp/gform5.html","w").write(r.text)
# freebird error
for pat in [
    r'freebirdFormviewerViewError[^"]*',
    r'"errorMessage"[^,]+',
    r'data-error[^>]*>',
]:
    ms = re.findall(pat, r.text)
    if ms:
        print(pat, ms[:5])

# Check required flag: [[entryId, null, 1]] means required - all are required
# Maybe Rent/Buy needs exact choice from a list? Type 0 is short answer so free text OK.

# Try ONLY destination to see if any entry works
for eid in ["159372216", "1848213003", "1546051705", "223229278"]:
    p = {"entry." + eid: "x", "fvv": "1", "fbzx": fbzx, "pageHistory": "0", "submissionTimestamp": "-1"}
    rr = s.post(post, data=p, headers=headers, timeout=20)
    print("solo", eid, rr.status_code, "recorded" in rr.text.lower())

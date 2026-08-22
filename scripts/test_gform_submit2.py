#!/usr/bin/env python3
import re
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
m = re.search(r"FB_PUBLIC_LOAD_DATA_\s*=\s*(.+?);\s*</script>", html, re.S)
print("fb", bool(m), "html", len(html))
data = m.group(1) if m else ""

# fbzx token often required
fbzx = None
for pat in [
    r'name="fbzx" value="([^"]+)"',
    r'"fbzx"\s*,\s*"([^"]+)"',
    r'fbzx["\s:]+(-?\d+)',
]:
    mm = re.search(pat, html)
    if mm:
        fbzx = mm.group(1)
        print("fbzx via", pat, fbzx)
        break

# Look for choice options near Rent
idx = data.find("Rent/Buy")
print("near rent", data[idx : idx + 250] if idx >= 0 else "none")

payload = {
    "entry.159372216": "Fort Bragg, NC",
    "entry.1546051705": "Test",
    "entry.1445033394": "Soldier",
    "entry.1001940560": "E-5",
    "entry.1608004035": "Rent",
    "entry.132029913": "1200-1600",
}
if fbzx:
    payload["fbzx"] = fbzx
    payload["fvv"] = "1"
    payload["pageHistory"] = "0"
    payload["submissionTimestamp"] = "-1"

r = s.post(url, data=payload, timeout=20, allow_redirects=True)
print("status", r.status_code, "len", len(r.text), "url", r.url)
# Extract error message if any
for needle in ["error", "Error", "required", "closed", "not accepting", "invalid"]:
    if needle.lower() in r.text.lower():
        print("found", needle)
# try to find human text
texts = re.findall(r">([^<]{15,120})<", r.text)
for t in texts:
    if any(x in t.lower() for x in ["error", "required", "closed", "invalid", "something"]):
        print("TEXT", t.strip()[:120])

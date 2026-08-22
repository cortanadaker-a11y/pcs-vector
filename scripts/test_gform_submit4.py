#!/usr/bin/env python3
import re
import requests

base = "https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg"
view = base + "/viewform"
post = base + "/formResponse"

s = requests.Session()
html = s.get(view, timeout=20).text
fbzx = re.search(r'name="fbzx"\s+value="([^"]*)"', html)
fbzx_val = fbzx.group(1) if fbzx else ""
print("fbzx raw", repr(fbzx_val))
# sometimes value set by JS from FB data
m = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.+?);\s*</script>', html, re.S)
# try alternate fbzx locations
for pat in [r'["\']fbzx["\']\s*:\s*["\']([^"\']+)["\']', r'fbzx",(-?\d+)']:
    mm = re.search(pat, html)
    if mm:
        print("alt", pat, mm.group(1))

# Try GET formResponse (prefill style) — if 200 with confirmation, IDs are right
params_a = {
    "entry.159372216": "Fort Bragg, NC",
    "entry.1546051705": "Test",
    "entry.1445033394": "Soldier",
    "entry.1001940560": "E-5",
    "entry.1608004035": "Rent",
    "entry.132029913": "1200-1600",
    "submit": "Submit",
}
params_b = {
    "entry.1848213003": "Fort Bragg, NC",
    "entry.223229278": "Test",
    "entry.112196602": "Soldier",
    "entry.223086250": "E-5",
    "entry.2134536278": "Rent",
    "entry.1672369468": "1200-1600",
    "submit": "Submit",
}

for name, params in [("A", params_a), ("B", params_b)]:
    r = s.get(post, params=params, timeout=20, allow_redirects=True)
    ok = "Your response has been recorded" in r.text or "response has been recorded" in r.text.lower()
    print(name, "GET", r.status_code, "recorded", ok, "url", r.url[:80])

# POST with both id sets combined?
combo = {**params_a, **params_b}
if fbzx_val:
    combo["fbzx"] = fbzx_val
combo["fvv"] = "1"
combo["pageHistory"] = "0"
r = s.post(post, data=combo, timeout=20, headers={"Referer": view})
ok = "recorded" in r.text.lower()
print("combo POST", r.status_code, "recorded", ok)

# Check if form accepts responses: look in FB data for closed flag
# data ends with flags - print last part
if m:
    print("tail", m.group(1)[-200:])

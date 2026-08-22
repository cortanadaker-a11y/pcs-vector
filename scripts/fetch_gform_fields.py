#!/usr/bin/env python3
import json
import re
import urllib.request

url = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform"
)
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
m = re.search(r"FB_PUBLIC_LOAD_DATA_\s*=\s*(.+?);\s*</script>", html, re.S)
data_str = m.group(1)
data = json.loads(data_str)
qs = data[1][1]
print(f"Question count: {len(qs)}")
print("All questions:")
for q in qs:
    title = q[1]
    block = q[4][0] if q[4] else None
    entry = block[0] if block else None
    print(f"  title={title!r} entry={entry} type={q[3]}")

# search for email anywhere in payload
low = data_str.lower()
for needle in ["email", "e-mail", "mail"]:
    if needle in low:
        idxs = [m.start() for m in re.finditer(needle, low)]
        print(f"\nfound '{needle}' at {idxs[:5]}")
        for i in idxs[:3]:
            print(" ", data_str[max(0, i - 40) : i + 80])

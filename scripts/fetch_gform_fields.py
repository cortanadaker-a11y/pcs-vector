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
open("/tmp/fbdata2.txt", "w").write(data_str)
data = json.loads(data_str)
qs = data[1][1]
print("Raw question blocks:")
for q in qs:
    print(json.dumps(q)[:300])
    print("---")
    title = q[1]
    # entry id is usually q[4][0][0] or q[4][0][1]
    block = q[4][0] if q[4] else None
    print("title:", repr(title), "block0:", block)

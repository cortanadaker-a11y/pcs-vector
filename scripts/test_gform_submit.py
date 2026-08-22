#!/usr/bin/env python3
import requests

url = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/formResponse"
)

A = {
    "entry.159372216": "Fort Bragg, NC",
    "entry.1546051705": "Test",
    "entry.1445033394": "Soldier",
    "entry.1001940560": "E-5",
    "entry.1608004035": "Rent",
    "entry.132029913": "$1200-$1600",
}
B = {
    "entry.1848213003": "Fort Bragg, NC",
    "entry.223229278": "Test",
    "entry.112196602": "Soldier",
    "entry.223086250": "E-5",
    "entry.2134536278": "Rent",
    "entry.1672369468": "$1200-$1600",
}

for name, payload in [("A nested", A), ("B outer", B)]:
    r = requests.post(url, data=payload, timeout=15, allow_redirects=True)
    snippet = r.text[:150].replace("\n", " ")
    print(name, r.status_code, snippet)

r2 = requests.get(
    "https://docs.google.com/forms/d/e/1FAIpQLSeok5DcRqIU9QhzOGXCGAVd8UbW21LNK_S601kzOwb4FJ1Wyg/viewform",
    timeout=15,
)
print("viewform", r2.status_code, len(r2.text))

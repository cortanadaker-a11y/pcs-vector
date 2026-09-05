#!/usr/bin/env python3
"""Rebuild data/bah_2026.json from official DTMO 2026 MHA tables.

Source dump: veteran.com 2026 BAH with/without-dependents tables (verbatim DTMO).
Each PCS Vector installation is mapped to its official Military Housing Area.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bah_2026.json"
SRC = Path(
    "/Users/zak/.grok/sessions/%2FUsers%2Fzak%2Fpcs-vector/"
    "01a06dc5-b6e6-7f11-aa5a-43503f7e03a7/web_fetch/2.md"
)

GRADES = [
    "E-1", "E-2", "E-3", "E-4", "E-5", "E-6", "E-7", "E-8", "E-9",
    "W-1", "W-2", "W-3", "W-4", "W-5",
    "O-1E", "O-2E", "O-3E", "O-1", "O-2", "O-3", "O-4", "O-5", "O-6", "O-7+",
]

# Duty-station → official 2026 MHA code (DTMO).
INSTALLATION_MHA: dict[str, str] = {
    "Aberdeen Proving Ground, MD": "MD127",
    "Anniston Army Depot, AL": "AL001",
    "Camp Atterbury, IN": "IN094",
    "Carlisle Barracks, PA": "PA247",
    "Detroit Arsenal, MI": "MI142",
    "Dugway Proving Ground, UT": "UT292",
    "Fort Barfoot, VA": "VA301",
    "Fort Belvoir, VA": "DC053",
    "Fort Benning, GA": "GA075",
    "Fort Bliss, TX": "TX279",
    "Fort Bragg, NC": "NC182",
    "Fort Campbell, KY": "KY106",
    "Fort Carson, CO": "CO046",
    "Fort Detrick, MD": "MD130",
    "Fort Drum, NY": "NY225",
    "Fort Gillem, GA": "GA071",
    "Fort Gordon, GA": "GA073",
    "Fort Greely, AK": "AK405",
    "Fort Hamilton, NY": "NY219",
    "Fort Hood, TX": "TX286",
    "Fort Huachuca, AZ": "AZ014",
    "Fort Hunter Liggett, CA": "CA039",
    "Fort Irwin, CA": "CA028",
    "Fort Jackson, SC": "SC260",
    "Fort Knox, KY": "KY110",
    "Fort Leavenworth, KS": "KS102",
    "Fort Lee, VA": "VA301",
    "Fort Leonard Wood, MO": "MO163",
    "Fort McCoy, WI": "WI318",
    "Fort McNair, DC": "DC053",
    "Fort Meade, MD": "MD133",
    "Fort Myer, VA": "DC053",
    "Fort Polk, LA": "LA115",
    "Fort Riley, KS": "KS100",
    "Fort Rucker, AL": "AL002",
    "Fort Sam Houston, TX": "TX285",
    "Fort Shafter, HI": "HI408",
    "Fort Sill, OK": "OK237",
    "Fort Stewart, GA": "GA080",
    "Fort Story, VA": "VA298",
    "Fort Wainwright, AK": "AK405",
    "Fort Walker, VA": "VA368",
    "Hunter Army Airfield, GA": "GA077",
    "Joint Base Elmendorf-Richardson, AK": "AK404",
    "Joint Base Langley-Eustis, VA": "VA297",
    "Joint Base Lewis-McChord, WA": "WA311",
    "Joint Base McGuire-Dix-Lakehurst, NJ": "NJ204",
    "Joint Base San Antonio, TX": "TX285",
    "Natick Soldier Systems Center, MA": "MA377",
    "Pentagon / National Capital Region, VA": "DC053",
    "Picatinny Arsenal, NJ": "NJ202",
    "Presidio of Monterey, CA": "CA039",
    "Redstone Arsenal, AL": "AL003",
    "Rock Island Arsenal, IL": "IL089",
    "Schofield Barracks, HI": "HI408",
    "Sierra Army Depot, CA": "NV213",
    "Tobyhanna Army Depot, PA": "PA254",
    "US Military Academy West Point, NY": "NY217",
    "White Sands Missile Range, NM": "NM209",
    "Yuma Proving Ground, AZ": "AZ016",
}


def parse_table(section: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip().replace("\\_", "_") for c in line.strip("|").split("|")]
        if not cols:
            continue
        mha = cols[0].replace(" ", "")
        if not re.match(r"^[A-Z]{2}\d{3}$", mha):
            continue
        name = cols[1]
        vals: list[int] = []
        for c in cols[2:]:
            n = re.sub(r"[^0-9]", "", c.split(".")[0] if c else "")
            if n:
                vals.append(int(n))
        if len(vals) < 24:
            raise SystemExit(f"incomplete row {mha} {name}: {len(vals)}")
        rec = {g: vals[i] for i, g in enumerate(GRADES)}
        rec["Other"] = rec["E-5"]
        rows[mha] = {"name": name, "rates": rec}
    return rows


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    with_part, wo_part = text.split("## 2026 BAH Rates Without Dependents", 1)
    with_rows = parse_table(with_part)
    wo_rows = parse_table(wo_part)
    assert len(with_rows) == 338 and len(wo_rows) == 338

    installations: dict[str, dict] = {}
    for name, mha in sorted(INSTALLATION_MHA.items()):
        if mha not in with_rows or mha not in wo_rows:
            raise SystemExit(f"missing MHA {mha} for {name}")
        installations[name] = {
            "mha": with_rows[mha]["name"],
            "mha_code": mha,
            "with_dependents": with_rows[mha]["rates"],
            "without_dependents": wo_rows[mha]["rates"],
        }

    out = {
        "effective_date": "2026-01-01",
        "source": (
            "DTMO 2026 BAH locality tables (with- and without-dependents), "
            "effective 1 Jan 2026. Mapped by official Military Housing Area, "
            "not ZIP of residence. Verify at finance / DTMO BAH calculator."
        ),
        "note": (
            "BAH is paid by duty-station MHA. Foreign OCONUS posts (Germany, "
            "Italy, Korea, Japan, Puerto Rico) use OHA, not these BAH rows. "
            "Alaska and Hawaii use BAH plus OCONUS COLA."
        ),
        "installations": installations,
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(installations)} installations)")


if __name__ == "__main__":
    main()

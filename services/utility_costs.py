"""Off-post utility cost planning ranges by installation / zip corridor.

Figures are monthly household planning ranges for a typical 3-bedroom off-post
rental (not on-post). Sourced from regional energy/water norms and PCS planning
data; always confirm with local providers and the lease.
"""

from __future__ import annotations

from typing import Any

# electric_low/high, gas_or_heat_low/high, water_trash_low/high, internet_low/high (USD/mo)
# total_low/high = sum of lows / sum of highs for quick BAH math.
_UTILITY_BY_INSTALL: dict[str, dict[str, Any]] = {
    "Fort Sam Houston, TX": {
        "areas": [
            {
                "name": "San Antonio NE / Schertz / Universal City",
                "zips": ["78154", "78148", "78233"],
                "electric": (120, 250),
                "gas_or_heat": (20, 55),
                "water_trash": (55, 100),
                "internet": (60, 95),
                "season_note": "Summer AC is the spike; many leases exclude electric — read the lease.",
            },
            {
                "name": "Converse / Live Oak corridor",
                "zips": ["78109", "78233"],
                "electric": (115, 240),
                "gas_or_heat": (20, 55),
                "water_trash": (50, 95),
                "internet": (55, 90),
                "season_note": "Confirm JBSA gate (Sam Houston vs Randolph) against commute fuel cost.",
            },
        ],
        "as_of": "2026 planning (San Antonio / JBSA)",
    },
    "Fort Hood, TX": {
        "areas": [
            {
                "name": "Killeen (76541 / 76542)",
                "zips": ["76541", "76542"],
                "electric": (140, 280),
                "gas_or_heat": (15, 45),
                "water_trash": (55, 95),
                "internet": (60, 90),
                "season_note": "Summer AC is the big swing — July/Aug often top of the electric range.",
            },
            {
                "name": "Harker Heights (76548)",
                "zips": ["76548"],
                "electric": (130, 260),
                "gas_or_heat": (15, 45),
                "water_trash": (55, 95),
                "internet": (60, 90),
                "season_note": "Similar to Killeen; newer builds may run slightly less electric.",
            },
            {
                "name": "Copperas Cove (76522)",
                "zips": ["76522"],
                "electric": (135, 270),
                "gas_or_heat": (15, 50),
                "water_trash": (50, 90),
                "internet": (55, 85),
                "season_note": "Plan the high end of electric if the home is older or poorly insulated.",
            },
        ],
        "as_of": "2026 planning (TX deregulated electric — shop rates; summer AC heavy)",
    },
    "Fort Bragg, NC": {
        "areas": [
            {
                "name": "Hope Mills / Fayetteville (28348)",
                "zips": ["28348", "28306"],
                "electric": (120, 220),
                "gas_or_heat": (40, 110),
                "water_trash": (50, 90),
                "internet": (60, 95),
                "season_note": "Summer humidity + winter heat both matter; gas heat spikes cold months.",
            },
            {
                "name": "Spring Lake (28390)",
                "zips": ["28390"],
                "electric": (125, 230),
                "gas_or_heat": (40, 115),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Close-in inventory; check if water is city vs well.",
            },
        ],
        "as_of": "2026 planning (Carolinas dual-season utilities)",
    },
    "Fort Campbell, KY": {
        "areas": [
            {
                "name": "Clarksville / 37042",
                "zips": ["37042", "37040"],
                "electric": (115, 210),
                "gas_or_heat": (45, 130),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Winter gas/electric heat is the expensive swing on the TN side.",
            },
            {
                "name": "Oak Grove / KY side (42262)",
                "zips": ["42262", "42223"],
                "electric": (120, 220),
                "gas_or_heat": (45, 135),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Confirm which state utilities and taxes apply before you sign.",
            },
        ],
        "as_of": "2026 planning (TN/KY split market)",
    },
    "Fort Drum, NY": {
        "areas": [
            {
                "name": "Evans Mills / Le Ray (13637)",
                "zips": ["13637", "13612"],
                "electric": (100, 180),
                "gas_or_heat": (120, 320),
                "water_trash": (50, 90),
                "internet": (60, 100),
                "season_note": "Winter heating dominates — propane/oil/gas can push total over $350/mo peak.",
            },
            {
                "name": "Watertown (13601)",
                "zips": ["13601", "13619"],
                "electric": (105, 190),
                "gas_or_heat": (110, 300),
                "water_trash": (55, 95),
                "internet": (60, 100),
                "season_note": "Ask for last winter's heating bills before you sign any lease.",
            },
        ],
        "as_of": "2026 planning (North Country winter heat risk)",
    },
    "Fort Bliss, TX": {
        "areas": [
            {
                "name": "Northeast El Paso / 79938",
                "zips": ["79938", "79934"],
                "electric": (100, 220),
                "gas_or_heat": (15, 40),
                "water_trash": (45, 85),
                "internet": (55, 85),
                "season_note": "Summer AC is the spike; desert nights help but older units still run high.",
            },
        ],
        "as_of": "2026 planning (El Paso summer AC)",
    },
    "Fort Benning, GA": {
        "areas": [
            {
                "name": "Columbus north (31909)",
                "zips": ["31909", "31907"],
                "electric": (130, 250),
                "gas_or_heat": (25, 70),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Summer humidity = high AC; check if electric is included in rent.",
            },
            {
                "name": "Phenix City, AL (36867)",
                "zips": ["36867"],
                "electric": (125, 240),
                "gas_or_heat": (25, 70),
                "water_trash": (50, 90),
                "internet": (55, 85),
                "season_note": "AL lease / GA school zoning still apply — utilities alone do not fix that risk.",
            },
        ],
        "as_of": "2026 planning (GA/AL humidity)",
    },
    "Fort Stewart, GA": {
        "areas": [
            {
                "name": "Hinesville (31313)",
                "zips": ["31313", "31324"],
                "electric": (140, 270),
                "gas_or_heat": (20, 60),
                "water_trash": (55, 95),
                "internet": (55, 90),
                "season_note": "Coastal humidity + storm season; renter insurance can run higher.",
            },
        ],
        "as_of": "2026 planning (coastal GA)",
    },
    "Fort Sill, OK": {
        "areas": [
            {
                "name": "Lawton west (73505)",
                "zips": ["73505", "73507"],
                "electric": (110, 210),
                "gas_or_heat": (30, 90),
                "water_trash": (50, 85),
                "internet": (50, 85),
                "season_note": "Tornado alley — budget renter insurance + hail rider, not just electric.",
            },
            {
                "name": "Cache (73527)",
                "zips": ["73527"],
                "electric": (105, 200),
                "gas_or_heat": (30, 90),
                "water_trash": (45, 80),
                "internet": (50, 80),
                "season_note": "Slightly lower inventory cost; verify commute fuel on top of utilities.",
            },
        ],
        "as_of": "2026 planning (SW Oklahoma)",
    },
    "Joint Base Lewis-McChord, WA": {
        "areas": [
            {
                "name": "DuPont (98327)",
                "zips": ["98327"],
                "electric": (90, 160),
                "gas_or_heat": (50, 140),
                "water_trash": (70, 120),
                "internet": (65, 100),
                "season_note": "Mild winters vs TX, but rain + mold risk — dehumidifier cost is real.",
            },
            {
                "name": "Lakewood (98439)",
                "zips": ["98439", "98498"],
                "electric": (95, 170),
                "gas_or_heat": (50, 145),
                "water_trash": (70, 120),
                "internet": (65, 100),
                "season_note": "Utility totals often higher than the South because water/sewer + internet are steep.",
            },
        ],
        "as_of": "2026 planning (PNW water/sewer + heat)",
    },
    "Fort Belvoir, VA": {
        "areas": [
            {
                "name": "Lorton / Springfield corridor",
                "zips": ["22079", "22150"],
                "electric": (110, 200),
                "gas_or_heat": (50, 150),
                "water_trash": (60, 110),
                "internet": (65, 100),
                "season_note": "Many NCR leases exclude utilities — read the lease; dual-season bills.",
            },
        ],
        "as_of": "2026 planning (NCR)",
    },
    "Fort Myer, VA": {
        "areas": [
            {
                "name": "Arlington / Alexandria",
                "zips": ["22202", "22301"],
                "electric": (100, 190),
                "gas_or_heat": (50, 160),
                "water_trash": (60, 120),
                "internet": (70, 110),
                "season_note": "High rent market; utilities often separate and not cheap.",
            },
        ],
        "as_of": "2026 planning (NCR urban)",
    },
    "Schofield Barracks, HI": {
        "areas": [
            {
                "name": "Wahiawa / Central Oahu",
                "zips": ["96786", "96789"],
                "electric": (180, 350),
                "gas_or_heat": (10, 30),
                "water_trash": (60, 120),
                "internet": (70, 110),
                "season_note": "Hawaii electric is high year-round; AC and dryer drive the bill.",
            },
        ],
        "as_of": "2026 planning (Oahu electric cost)",
    },
    "Camp Humphreys, South Korea": {
        "areas": [
            {
                "name": "Off-post near Humphreys / Pyeongtaek",
                "zips": [],
                "electric": (80, 180),
                "gas_or_heat": (60, 200),
                "water_trash": (30, 70),
                "internet": (30, 60),
                "season_note": "OHA utility allowance helps; winter floor heat can spike gas. Confirm what landlord includes.",
            },
        ],
        "as_of": "2026 planning (Korea off-post; OHA utility allowance separate)",
    },
    "Camp Casey, South Korea": {
        "areas": [
            {
                "name": "Dongducheon / off-post near Casey",
                "zips": [],
                "electric": (75, 170),
                "gas_or_heat": (70, 220),
                "water_trash": (30, 65),
                "internet": (30, 55),
                "season_note": "Cold winters; many unaccompanied tours. Confirm which utilities the landlord includes.",
            },
        ],
        "as_of": "2026 planning (Korea north of Seoul; OHA utility allowance separate)",
    },
    "Camp Zama, Japan": {
        "areas": [
            {
                "name": "Zama / Sagamihara corridor",
                "zips": [],
                "electric": (90, 200),
                "gas_or_heat": (50, 160),
                "water_trash": (35, 80),
                "internet": (40, 75),
                "season_note": "Japanese leases often split utilities; ask for prior-year bills. OHA utility allowance is separate.",
            },
        ],
        "as_of": "2026 planning (Camp Zama / Kanagawa)",
    },
    "USAG Italy, Italy": {
        "areas": [
            {
                "name": "Vicenza / nearby villages",
                "zips": [],
                "electric": (95, 190),
                "gas_or_heat": (70, 200),
                "water_trash": (35, 80),
                "internet": (35, 65),
                "season_note": "Winter heating matters; many Italian leases exclude utilities — get last 12 months of bills.",
            },
        ],
        "as_of": "2026 planning (Vicenza; OHA utility allowance separate)",
    },
    "Fort Shafter, HI": {
        "areas": [
            {
                "name": "Honolulu / Salt Lake / Aiea",
                "zips": ["96818", "96701"],
                "electric": (180, 360),
                "gas_or_heat": (10, 30),
                "water_trash": (60, 120),
                "internet": (70, 110),
                "season_note": "Hawaii electric is high year-round; AC and dryer drive the bill.",
            },
        ],
        "as_of": "2026 planning (Oahu / Shafter)",
    },
    "Fort Buchanan, PR": {
        "areas": [
            {
                "name": "Guaynabo / Bayamón / San Juan metro",
                "zips": ["00966", "00959"],
                "electric": (140, 280),
                "gas_or_heat": (10, 35),
                "water_trash": (40, 90),
                "internet": (50, 90),
                "season_note": "AC is the big cost; hurricane season can affect insurance and generator planning.",
            },
        ],
        "as_of": "2026 planning (San Juan metro)",
    },
    "Joint Base Elmendorf-Richardson, AK": {
        "areas": [
            {
                "name": "Anchorage NE / Eagle River",
                "zips": ["99504", "99577"],
                "electric": (110, 200),
                "gas_or_heat": (120, 320),
                "water_trash": (55, 110),
                "internet": (70, 120),
                "season_note": "Winter heating dominates; block heaters and higher fuel costs are real.",
            },
            {
                "name": "Anchorage midtown / south",
                "zips": ["99503", "99515"],
                "electric": (105, 190),
                "gas_or_heat": (110, 300),
                "water_trash": (55, 105),
                "internet": (70, 115),
                "season_note": "Ask for last winter’s heating bills before you sign.",
            },
        ],
        "as_of": "2026 planning (Anchorage / JBER)",
    },
    "Fort Wainwright, AK": {
        "areas": [
            {
                "name": "Fairbanks / North Pole",
                "zips": ["99701", "99705"],
                "electric": (120, 220),
                "gas_or_heat": (150, 400),
                "water_trash": (50, 100),
                "internet": (65, 110),
                "season_note": "Interior Alaska winters are extreme — heating can dwarf every other utility.",
            },
        ],
        "as_of": "2026 planning (Fairbanks)",
    },
    "Fort Greely, AK": {
        "areas": [
            {
                "name": "Delta Junction / on-post area",
                "zips": ["99737"],
                "electric": (130, 240),
                "gas_or_heat": (160, 420),
                "water_trash": (45, 95),
                "internet": (60, 120),
                "season_note": "Very limited off-post options; heating and connectivity are the main cost risks.",
            },
        ],
        "as_of": "2026 planning (Delta Junction / Greely)",
    },
    "USAG Wiesbaden, Germany": {
        "areas": [
            {
                "name": "Wiesbaden city / nearby villages",
                "zips": [],
                "electric": (100, 200),
                "gas_or_heat": (80, 220),
                "water_trash": (40, 90),
                "internet": (40, 70),
                "season_note": "Winter heating is the spike; many leases split utilities — get last 12 months of bills.",
            },
        ],
        "as_of": "2026 planning (Germany off-post; OHA utility allowance separate)",
    },
    "USAG Bavaria, Germany": {
        "areas": [
            {
                "name": "Vilseck / Grafenwoehr area",
                "zips": [],
                "electric": (95, 190),
                "gas_or_heat": (90, 240),
                "water_trash": (40, 85),
                "internet": (40, 70),
                "season_note": "Cold winters — ask for prior-year heating costs before signing.",
            },
        ],
        "as_of": "2026 planning (Bavaria)",
    },
    "USAG Rheinland-Pfalz, Germany": {
        "areas": [
            {
                "name": "Kaiserslautern / Landstuhl corridor",
                "zips": [],
                "electric": (100, 200),
                "gas_or_heat": (80, 220),
                "water_trash": (40, 90),
                "internet": (40, 70),
                "season_note": "KMC market is competitive; utilities often not in rent.",
            },
        ],
        "as_of": "2026 planning (KMC)",
    },
    "Fort Carson, CO": {
        "areas": [
            {
                "name": "Fountain / Widefield (80817)",
                "zips": ["80817", "80911"],
                "electric": (90, 170),
                "gas_or_heat": (50, 160),
                "water_trash": (55, 100),
                "internet": (60, 95),
                "season_note": "Winter heating is the swing; altitude + dry air — humidifiers help.",
            },
            {
                "name": "Colorado Springs south (80906)",
                "zips": ["80906", "80910"],
                "electric": (95, 180),
                "gas_or_heat": (55, 170),
                "water_trash": (60, 110),
                "internet": (65, 100),
                "season_note": "Newer builds often more efficient; ask for prior winter gas bills.",
            },
        ],
        "as_of": "2026 planning (Front Range dual-season)",
    },
    "Fort Riley, KS": {
        "areas": [
            {
                "name": "Junction City (66441)",
                "zips": ["66441"],
                "electric": (110, 210),
                "gas_or_heat": (40, 130),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Hot summers + cold winters — budget both AC and heat.",
            },
            {
                "name": "Manhattan / 66502",
                "zips": ["66502", "66503"],
                "electric": (105, 200),
                "gas_or_heat": (40, 125),
                "water_trash": (50, 95),
                "internet": (55, 95),
                "season_note": "Longer commute; confirm fuel cost on top of utilities.",
            },
        ],
        "as_of": "2026 planning (Flint Hills)",
    },
    "Joint Base San Antonio, TX": {
        "areas": [
            {
                "name": "San Antonio NE / Schertz / Universal City",
                "zips": ["78154", "78148", "78233"],
                "electric": (120, 250),
                "gas_or_heat": (20, 55),
                "water_trash": (55, 100),
                "internet": (60, 95),
                "season_note": "Summer AC is the spike; many leases exclude electric — read the lease.",
            },
            {
                "name": "Converse / Live Oak corridor",
                "zips": ["78109", "78233"],
                "electric": (115, 240),
                "gas_or_heat": (20, 55),
                "water_trash": (50, 95),
                "internet": (55, 90),
                "season_note": "Confirm JBSA gate against commute fuel cost.",
            },
        ],
        "as_of": "2026 planning (San Antonio / JBSA)",
    },
    "Fort Polk, LA": {
        "areas": [
            {
                "name": "Leesville (71446)",
                "zips": ["71446"],
                "electric": (140, 280),
                "gas_or_heat": (20, 55),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Humid summers = high AC; check if electric is included in rent.",
            },
        ],
        "as_of": "2026 planning (central LA humidity)",
    },
    "Fort Gordon, GA": {
        "areas": [
            {
                "name": "Grovetown / Augusta west (30813)",
                "zips": ["30813", "30909"],
                "electric": (125, 240),
                "gas_or_heat": (25, 75),
                "water_trash": (50, 90),
                "internet": (55, 90),
                "season_note": "Summer humidity drives AC; winter mild but still plan heat.",
            },
        ],
        "as_of": "2026 planning (CSRA / Augusta)",
    },
    "Fort Jackson, SC": {
        "areas": [
            {
                "name": "Columbia / Elgin corridor",
                "zips": ["29223", "29045"],
                "electric": (120, 230),
                "gas_or_heat": (30, 90),
                "water_trash": (50, 95),
                "internet": (55, 90),
                "season_note": "Hot humid summers; confirm water/trash vs HOA fees.",
            },
        ],
        "as_of": "2026 planning (Midlands SC)",
    },
}

# Climate-region fallbacks when installation is not in the table
_REGION_DEFAULTS: dict[str, dict[str, Any]] = {
    "hot_south": {
        "electric": (130, 270),
        "gas_or_heat": (15, 50),
        "water_trash": (50, 95),
        "internet": (55, 90),
        "season_note": "Summer AC usually dominates the bill.",
    },
    "cold_north": {
        "electric": (100, 180),
        "gas_or_heat": (100, 300),
        "water_trash": (50, 95),
        "internet": (60, 100),
        "season_note": "Winter heating is the expensive swing — get prior bills.",
    },
    "mixed": {
        "electric": (110, 210),
        "gas_or_heat": (40, 120),
        "water_trash": (50, 95),
        "internet": (55, 95),
        "season_note": "Budget for both summer AC and winter heat.",
    },
    "oconus_default": {
        "electric": (90, 200),
        "gas_or_heat": (60, 220),
        "water_trash": (35, 90),
        "internet": (35, 70),
        "season_note": "Off-post utilities vary widely; ask landlord for last year's bills. OHA utility allowance may offset part.",
    },
}


def _totals(area: dict[str, Any]) -> tuple[int, int]:
    keys = ("electric", "gas_or_heat", "water_trash", "internet")
    low = sum(int(area[k][0]) for k in keys)
    high = sum(int(area[k][1]) for k in keys)
    return low, high


def _normalize_area(area: dict[str, Any]) -> dict[str, Any]:
    low, high = _totals(area)
    return {
        "name": area["name"],
        "zips": list(area.get("zips") or []),
        "electric_usd_mo": {"low": area["electric"][0], "high": area["electric"][1]},
        "gas_or_heat_usd_mo": {"low": area["gas_or_heat"][0], "high": area["gas_or_heat"][1]},
        "water_trash_usd_mo": {"low": area["water_trash"][0], "high": area["water_trash"][1]},
        "internet_usd_mo": {"low": area["internet"][0], "high": area["internet"][1]},
        "total_utilities_usd_mo": {"low": low, "high": high},
        "season_note": area.get("season_note", ""),
    }


def get_utility_costs_for_installation(
    installation: str,
    *,
    climate_hint: str | None = None,
    is_oconus: bool = False,
) -> dict[str, Any]:
    """Return structured off-post utility ranges for the gaining post."""
    if installation in _UTILITY_BY_INSTALL:
        raw = _UTILITY_BY_INSTALL[installation]
        areas = [_normalize_area(a) for a in raw["areas"]]
        return {
            "installation": installation,
            "areas": areas,
            "as_of": raw.get("as_of", "2026 planning"),
            "disclaimer": (
                "Monthly planning ranges for a typical 3-bedroom off-post rental. "
                "Actual bills depend on house size, efficiency, and rates — verify with "
                "local providers and ask landlords for recent statements."
            ),
            "found": True,
        }

    # Fallback by climate
    if is_oconus:
        region = "oconus_default"
    elif climate_hint and "winter" in climate_hint.lower():
        region = "cold_north"
    elif climate_hint and any(x in climate_hint.lower() for x in ("summer", "heat", "ac", "desert")):
        region = "hot_south"
    else:
        region = "mixed"
    base = _REGION_DEFAULTS[region]
    area = _normalize_area(
        {
            "name": f"Off-post near {installation}",
            "zips": [],
            "electric": base["electric"],
            "gas_or_heat": base["gas_or_heat"],
            "water_trash": base["water_trash"],
            "internet": base["internet"],
            "season_note": base["season_note"],
        }
    )
    return {
        "installation": installation,
        "areas": [area],
        "as_of": "2026 regional planning fallback",
        "disclaimer": (
            "Installation-specific utility table not on file — using regional planning ranges. "
            "Confirm with local electric/gas/water and the lease."
        ),
        "found": False,
    }


def format_utility_table_markdown(utility_ctx: dict[str, Any]) -> str:
    """Markdown table for Grok prompt / report embedding."""
    lines = [
        "| Area / zip | Electric | Gas / heat | Water / trash | Internet | **Total / mo** |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for a in utility_ctx.get("areas") or []:
        e = a["electric_usd_mo"]
        g = a["gas_or_heat_usd_mo"]
        w = a["water_trash_usd_mo"]
        i = a["internet_usd_mo"]
        t = a["total_utilities_usd_mo"]
        lines.append(
            f"| {a['name']} | "
            f"${e['low']}–${e['high']} | "
            f"${g['low']}–${g['high']} | "
            f"${w['low']}–${w['high']} | "
            f"${i['low']}–${i['high']} | "
            f"**${t['low']}–${t['high']}** |"
        )
    return "\n".join(lines)


__all__ = [
    "format_utility_table_markdown",
    "get_utility_costs_for_installation",
]

"""Installation-specific reference data for PCS Vector report templates.

Uses traditional installation names only (Fort Bragg, Fort Hood, Fort Benning, etc.).
New official names (Fort Liberty, Fort Cavazos, Fort Moore, etc.) are accepted as aliases
and resolve to the traditional keys in INSTALLATION_DATA.

BAH figures in _RICH_PROFILES are planning fallbacks when bah_2026.json has no entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Priority = Literal["High", "Medium", "Low"]

# ---------------------------------------------------------------------------
# Canonical installation registry (traditional names)
# Keys use "Fort Name, ST" or "Joint Base ..., ST" format.
# ---------------------------------------------------------------------------

INSTALLATION_DATA: dict[str, dict[str, Any]] = {
    "Fort Bragg, NC": {
        "state": "NC",
        "priority": "High",
        "notes": "Very high PCS volume; 82nd Airborne and SF corridor. Spouse employment and school zoning drive most family decisions.",
        "major_areas": [
            "Hope Mills",
            "Spring Lake",
            "Fayetteville (north side)",
            "Raeford",
        ],
        "school_districts": [
            "Cumberland County Schools",
            "Harnett County Schools (verify zoning)",
        ],
        "commute_notes": "All-American Fwy and Bragg Blvd peak 0630–0800; pre-apply rentals from losing station in summer PCS.",
    },
    "Fort Hood, TX": {
        "state": "TX",
        "priority": "High",
        "notes": "Very high volume; III Armored Corps. Competitive Central Texas rental market; summer AC costs matter off-post.",
        "major_areas": [
            "Killeen",
            "Harker Heights",
            "Copperas Cove",
            "Nolanville",
        ],
        "school_districts": [
            "Killeen ISD",
            "Copperas Cove ISD",
        ],
        "commute_notes": "US-190 and Trimmier Rd gates back up at peak; Copperas Cove offers strong BAH surplus with longer drive.",
    },
    "Fort Bliss, TX": {
        "state": "TX",
        "priority": "High",
        "notes": "High volume; 1st Armored Division and WBAMC. Desert market favors off-post BAH surplus; verify unit gate (main vs east).",
        "major_areas": [
            "Northeast El Paso",
            "Horizon City",
            "West El Paso",
            "Sunland Park (NM)",
        ],
        "school_districts": [
            "El Paso ISD",
            "Socorro ISD",
            "Ysleta ISD",
        ],
        "commute_notes": "US-54 and Loop 375 choke at rush; monsoon season (Jul–Sep) can add 15–20 min unpredictably.",
    },
    "Fort Campbell, KY": {
        "state": "KY/TN",
        "priority": "High",
        "notes": "High volume; 101st Airborne. Straddles KY/TN line — school district and state tax differ by side of post.",
        "major_areas": [
            "Clarksville, TN",
            "Oak Grove, KY",
            "Hopkinsville, KY",
            "Fort Campbell North housing",
        ],
        "school_districts": [
            "Clarksville-Montgomery County Schools (TN)",
            "Christian County Schools (KY)",
            "Fort Campbell Schools (on-post DODEA)",
        ],
        "commute_notes": "Madam Walker / Fort Campbell Blvd rush peaks with division cycles; TN side has more inventory, KY side quieter.",
    },
    "Fort Stewart, GA": {
        "state": "GA",
        "priority": "High",
        "notes": "High volume; 3rd Infantry Division. Coastal Georgia humidity and hurricane season affect utilities and insurance.",
        "major_areas": [
            "Hinesville",
            "Richmond Hill",
            "Pooler",
            "Savannah suburbs (west)",
        ],
        "school_districts": [
            "Liberty County Schools",
            "Bryan County Schools",
        ],
        "commute_notes": "GA-119 and US-84 gate corridors; Richmond Hill popular for schools but adds 20–25 min.",
    },
    "Fort Benning, GA": {
        "state": "GA",
        "priority": "High",
        "notes": "High volume; Maneuver Center of Excellence. Heavy training tempo; spouse jobs cluster in Columbus and Phenix City.",
        "major_areas": [
            "Columbus, GA",
            "Phenix City, AL",
            "Midland / Upatoi corridor",
        ],
        "school_districts": [
            "Muscogee County Schools (GA)",
            "Russell County Schools (AL — Phenix City)",
        ],
        "commute_notes": "US-280 and Victory Drive peak with basic training graduations; AL leases require GA school zoning check.",
    },
    "Fort Jackson, SC": {
        "state": "SC",
        "priority": "High",
        "notes": "High volume; TRADOC initial entry training. Constant PCS churn; Columbia metro offers spouse job depth.",
        "major_areas": [
            "Columbia (northeast / Forest Acres)",
            "Elgin",
            "Blythewood",
            "Lexington",
        ],
        "school_districts": [
            "Richland School District Two",
            "Lexington County School District One",
        ],
        "commute_notes": "I-77 and Forest Drive congestion; Blythewood popular for schools, verify gate-to-barracks commute for sponsors.",
    },
    "Fort Sill, OK": {
        "state": "OK",
        "priority": "High",
        "notes": "High volume; Fires Center of Excellence. Lawton market is affordable; wind and hail affect insurance off-post.",
        "major_areas": [
            "Lawton",
            "Cache",
            "Medicine Park",
        ],
        "school_districts": [
            "Lawton Public Schools",
            "Cache Public Schools",
        ],
        "commute_notes": "Sheridan Road and Fort Sill Blvd are main arteries; shorter commutes than most CONUS posts.",
    },
    "Fort Leavenworth, KS": {
        "state": "KS",
        "priority": "Medium",
        "notes": "Medium-high volume; CGSC and staff college. Officer-heavy; on-post housing culture strong; KC metro 40 min north.",
        "major_areas": [
            "Leavenworth",
            "Lansing",
            "Basehor",
            "Platte City, MO",
        ],
        "school_districts": [
            "Leavenworth USD 453",
            "Lansing USD 469",
        ],
        "commute_notes": "Historic post with tight housing market; US-73 bridge traffic spikes with school calendar.",
    },
    "Fort Riley, KS": {
        "state": "KS",
        "priority": "Medium",
        "notes": "Medium-high volume; 1st Infantry Division. Manhattan (K-State) offers spouse jobs; tornado season awareness.",
        "major_areas": [
            "Junction City",
            "Manhattan",
            "Ogden",
        ],
        "school_districts": [
            "Geary County Schools (USD 475)",
            "Manhattan-Ogden USD 383",
        ],
        "commute_notes": "Fort Riley Blvd and I-70 interchange peak with division deployments; Manhattan commute 20–30 min.",
    },
    "Fort Carson, CO": {
        "state": "CO",
        "priority": "Medium",
        "notes": "Medium-high volume; 4th Infantry Division. Elevation and wildfire smoke affect health; Colorado Springs market competitive.",
        "major_areas": [
            "Colorado Springs (south / Security-Widefield)",
            "Fountain",
            "Pueblo West",
        ],
        "school_districts": [
            "Fountain-Fort Carson School District 8",
            "Harrison School District 2",
            "Widefield School District 3",
        ],
        "commute_notes": "I-25 and Academy Blvd rush; verify gate (Main vs Gate 20) against unit location on post.",
    },
    "Joint Base Lewis-McChord, WA": {
        "state": "WA",
        "priority": "High",
        "notes": "High volume; I Corps and 62nd AW. Rain, traffic, and tight Pierce County rental market define PCS planning.",
        "major_areas": [
            "Lakewood",
            "DuPont",
            "Puyallup",
            "Yelm",
        ],
        "school_districts": [
            "Clover Park School District",
            "Steilacoom Historical School District",
            "Yelm Community Schools",
        ],
        "commute_notes": "I-5 and SR-507 choke points; DuPont walkable to Madigan but inventory turns fast in summer.",
    },
    "Fort Drum, NY": {
        "state": "NY",
        "priority": "Medium",
        "notes": "Medium volume; 10th Mountain Division. Winter weather and heating costs are primary off-post risk factors.",
        "major_areas": [
            "Evans Mills",
            "Carthage",
            "Watertown",
            "Le Ray",
        ],
        "school_districts": [
            "Indian River Central School District",
            "Watertown City School District",
        ],
        "commute_notes": "Route 11 lake-effect closures Oct–Apr; build 30-min winter commute buffer.",
    },
    "Fort Gordon, GA": {
        "state": "GA",
        "priority": "Medium",
        "notes": "Medium-high volume; cyber and signal school hub. Augusta metro growing; Columbia County schools are top draw.",
        "major_areas": [
            "Evans",
            "Grovetown",
            "Martinez",
            "West Augusta",
        ],
        "school_districts": [
            "Columbia County Schools",
            "Richmond County Schools",
        ],
        "commute_notes": "Gordon Hwy and Gate 1 peak 0630–0730; Evans adds 15–20 min but better school ratings.",
    },
    "Fort Huachuca, AZ": {
        "state": "AZ",
        "priority": "Medium",
        "notes": "Medium volume; intelligence and unmanned systems school. Sierra Vista market small; Tucson 70 min for spouse jobs.",
        "major_areas": [
            "Sierra Vista",
            "Huachuca City",
            "Hereford",
        ],
        "school_districts": [
            "Sierra Vista Unified School District",
            "Fry Elementary area (verify zoning)",
        ],
        "commute_notes": "Buffalo Soldier Gate and AZ-90; monsoon flooding on low crossings; remote spouse may need Tucson commute.",
    },
    "Fort Irwin, CA": {
        "state": "CA",
        "priority": "Medium",
        "notes": "Medium volume; National Training Center. Isolated desert post — most families live on-post or in Barstow; spouse jobs limited.",
        "major_areas": [
            "Barstow",
            "On-post housing (primary)",
            "Victorville (long commute)",
        ],
        "school_districts": [
            "Silver Valley Unified (on-post / Barstow area)",
            "Barstow Unified (off-post)",
        ],
        "commute_notes": "I-15 NTC gate run is 35+ min from Barstow; heat and wind drive high AC and vehicle wear.",
    },
    "Fort Polk, LA": {
        "state": "LA",
        "priority": "Medium",
        "notes": "Medium volume; JRTC. Rural market; Leesville and DeRidder are main off-post options with limited spouse employment.",
        "major_areas": [
            "Leesville",
            "DeRidder",
            "New Llano",
        ],
        "school_districts": [
            "Vernon Parish School District",
            "Beauregard Parish (DeRidder)",
        ],
        "commute_notes": "US-171 and LA-28; hurricane season Jun–Nov; limited rental inventory spikes before rotation cycles.",
    },
    "Fort Knox, KY": {
        "state": "KY",
        "priority": "Medium",
        "notes": "Medium volume; Human Resources Command and cadet command. Radcliff/Elizabethtown corridor; Louisville 40 min north.",
        "major_areas": [
            "Radcliff",
            "Elizabethtown",
            "Vine Grove",
            "Louisville (south end)",
        ],
        "school_districts": [
            "Hardin County Schools",
            "Elizabethtown Independent",
        ],
        "commute_notes": "US-31W Dixie Highway peak with Fort Knox gate; Radcliff closest but school ratings vary by neighborhood.",
    },
    "Fort Leonard Wood, MO": {
        "state": "MO",
        "priority": "Medium",
        "notes": "Medium volume; Maneuver Support Center. Training post with steady churn; Waynesville and St. Robert are hub towns.",
        "major_areas": [
            "Waynesville",
            "St. Robert",
            "Lebanon",
        ],
        "school_districts": [
            "Waynesville R-VI School District",
            "Laquey R-V School District",
        ],
        "commute_notes": "I-44 and MO-17 gate rush with basic training cycles; St. Robert has most retail and spouse service jobs.",
    },
    "Fort McCoy, WI": {
        "state": "WI",
        "priority": "Low",
        "notes": "Lower volume; training and mobilization platform. Many PCS are short tours; Sparta and Tomah are primary off-post towns.",
        "major_areas": [
            "Sparta",
            "Tomah",
            "On-post quarters (limited)",
        ],
        "school_districts": [
            "Sparta Area School District",
            "Tomah Area School District",
        ],
        "commute_notes": "Rural I-90 corridor; winter road maintenance good but black ice common Nov–Mar.",
    },
    "Fort Rucker, AL": {
        "state": "AL",
        "priority": "Medium",
        "notes": "Medium volume; Army aviation center. Enterprise and Daleville dominate off-post; spouse jobs in healthcare and schools.",
        "major_areas": [
            "Enterprise",
            "Daleville",
            "Ozark",
        ],
        "school_districts": [
            "Enterprise City Schools",
            "Dale County Schools",
        ],
        "commute_notes": "US-231 and Rucker Blvd; low cost of living but limited inventory near gates.",
    },
    "Fort Wainwright, AK": {
        "state": "AK",
        "priority": "Medium",
        "notes": "Special case — Alaska PCS. COLA and PPM weight restrictions apply; extreme cold, darkness, and limited road network off-post.",
        "major_areas": [
            "Fairbanks (north and west)",
            "North Pole",
            "On-post housing (high demand)",
        ],
        "school_districts": [
            "Fairbanks North Star Borough School District",
        ],
        "commute_notes": "Winter plug-in block heaters required; -40°F days cancel school and delay in-processing; PPM often ships via Seattle.",
    },
}

SUPPORTED_INSTALLATIONS: list[str] = sorted(
    INSTALLATION_DATA.keys(),
    key=lambda name: (
        0 if INSTALLATION_DATA[name]["priority"] == "High" else
        1 if INSTALLATION_DATA[name]["priority"] == "Medium" else 2,
        name,
    ),
)

# New official names → traditional keys (never expose new names in user-facing copy).
INSTALLATION_ALIASES: dict[str, str] = {
    "Fort Liberty, NC": "Fort Bragg, NC",
    "Fort Liberty (Fort Bragg), NC": "Fort Bragg, NC",
    "Fort Liberty (Ft Bragg, NC)": "Fort Bragg, NC",
    "Fort Cavazos, TX": "Fort Hood, TX",
    "Fort Cavazos (Fort Hood), TX": "Fort Hood, TX",
    "Fort Moore, GA": "Fort Benning, GA",
    "Fort Moore (Fort Benning), GA": "Fort Benning, GA",
    "Fort Johnson, LA": "Fort Polk, LA",
    "Fort Eisenhower, GA": "Fort Gordon, GA",
    "Fort Novosel, AL": "Fort Rucker, AL",
    # Short-name aliases (no state suffix).
    "Fort Bragg": "Fort Bragg, NC",
    "Fort Hood": "Fort Hood, TX",
    "Fort Bliss": "Fort Bliss, TX",
    "Fort Campbell": "Fort Campbell, KY",
    "Fort Stewart": "Fort Stewart, GA",
    "Fort Benning": "Fort Benning, GA",
    "Fort Jackson": "Fort Jackson, SC",
    "Fort Sill": "Fort Sill, OK",
    "Fort Leavenworth": "Fort Leavenworth, KS",
    "Fort Riley": "Fort Riley, KS",
    "Fort Carson": "Fort Carson, CO",
    "Joint Base Lewis-McChord": "Joint Base Lewis-McChord, WA",
    "JBLM": "Joint Base Lewis-McChord, WA",
    "Fort Drum": "Fort Drum, NY",
    "Fort Gordon": "Fort Gordon, GA",
    "Fort Huachuca": "Fort Huachuca, AZ",
    "Fort Irwin": "Fort Irwin, CA",
    "Fort Polk": "Fort Polk, LA",
    "Fort Knox": "Fort Knox, KY",
    "Fort Leonard Wood": "Fort Leonard Wood, MO",
    "Fort McCoy": "Fort McCoy, WI",
    "Fort Rucker": "Fort Rucker, AL",
    "Fort Wainwright": "Fort Wainwright, AK",
}


def _canonical_installation_name(name: str) -> str | None:
    """Resolve aliases and return the traditional INSTALLATION_DATA key, or None."""
    cleaned = (name or "").strip()
    if not cleaned:
        return None
    if cleaned in INSTALLATION_DATA:
        return cleaned
    if cleaned in INSTALLATION_ALIASES:
        return INSTALLATION_ALIASES[cleaned]
    # Try appending state from data if user passed short name with comma state.
    for key in INSTALLATION_DATA:
        short = key.rsplit(", ", 1)[0]
        if cleaned.lower() == short.lower():
            return key
    return None


def get_installation_data(name: str) -> dict[str, Any] | None:
    """Return installation metadata dict for a traditional or aliased name."""
    canonical = _canonical_installation_name(name)
    if canonical is None:
        return None
    return INSTALLATION_DATA.get(canonical)


# ---------------------------------------------------------------------------
# Rich profiles for report generation (detailed housing/BAH/childcare fields)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HousingMarket:
    on_post_pros: tuple[str, ...]
    on_post_cons: tuple[str, ...]
    off_post_areas: tuple[str, ...]
    avg_3br_rent_range: tuple[int, int]
    utility_note: str


@dataclass(frozen=True)
class InstallationProfile:
    key: str
    display_name: str
    short_name: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float
    nearby_zip_codes: tuple[str, ...]
    bah_rates: dict[str, int]
    housing: HousingMarket
    school_districts: tuple[str, ...]
    spouse_employment_notes: tuple[str, ...]
    childcare_notes: tuple[str, ...]
    spouse_programs: tuple[str, ...]
    vehicle_registration_note: str
    climate_note: str
    commute_hotspots: tuple[str, ...]
    priority: Priority = "Medium"
    notes: str = ""


# Planning BAH fallbacks (with dependents) when bah_2026.json has no entry.
_BAH_DEFAULT: dict[str, int] = {
    "E-1": 1500, "E-2": 1500, "E-3": 1500, "E-4": 1500,
    "E-5": 1650, "E-6": 1800, "E-7": 1950, "E-8": 2100, "E-9": 2200,
    "W-1": 1850, "W-2": 1950, "W-3": 2050, "W-4": 2150, "W-5": 2250,
    "O-1": 1700, "O-2": 1850, "O-3": 2100, "O-4": 2300, "O-5": 2500,
    "O-6": 2650, "O-7+": 2800, "Other": 1650,
}

_BAH_BRAGG: dict[str, int] = {
    "E-1": 1428, "E-2": 1428, "E-3": 1428, "E-4": 1506, "E-5": 1653,
    "E-6": 1716, "E-7": 1836, "E-8": 1896, "E-9": 1944,
    "W-1": 1716, "W-2": 1836, "W-3": 1920, "W-4": 2016, "W-5": 2088,
    "O-1": 1716, "O-2": 1836, "O-3": 2016, "O-4": 2184, "O-5": 2328,
    "O-6": 2496, "O-7+": 2688, "Other": 1653,
}

_BAH_HOOD: dict[str, int] = {
    "E-1": 1380, "E-2": 1380, "E-3": 1380, "E-4": 1458, "E-5": 1542,
    "E-6": 1602, "E-7": 1710, "E-8": 1770, "E-9": 1818,
    "W-1": 1602, "W-2": 1710, "W-3": 1794, "W-4": 1878, "W-5": 1950,
    "O-1": 1602, "O-2": 1710, "O-3": 1878, "O-4": 2034, "O-5": 2166,
    "O-6": 2322, "O-7+": 2502, "Other": 1542,
}

_BAH_DRUM: dict[str, int] = {
    "E-1": 1332, "E-2": 1332, "E-3": 1332, "E-4": 1404, "E-5": 1548,
    "E-6": 1608, "E-7": 1716, "E-8": 1776, "E-9": 1824,
    "W-1": 1608, "W-2": 1716, "W-3": 1800, "W-4": 1884, "W-5": 1956,
    "O-1": 1608, "O-2": 1716, "O-3": 1884, "O-4": 2040, "O-5": 2172,
    "O-6": 2328, "O-7+": 2508, "Other": 1548,
}

_BAH_GORDON: dict[str, int] = {
    "E-1": 1356, "E-2": 1356, "E-3": 1356, "E-4": 1428, "E-5": 1572,
    "E-6": 1632, "E-7": 1740, "E-8": 1800, "E-9": 1848,
    "W-1": 1632, "W-2": 1740, "W-3": 1824, "W-4": 1908, "W-5": 1980,
    "O-1": 1632, "O-2": 1740, "O-3": 1908, "O-4": 2064, "O-5": 2196,
    "O-6": 2352, "O-7+": 2532, "Other": 1572,
}

_BAH_BLISS: dict[str, int] = {
    "E-1": 1665, "E-2": 1665, "E-3": 1665, "E-4": 1665, "E-5": 1809,
    "E-6": 2148, "E-7": 2172, "E-8": 2187, "E-9": 2241,
    "W-1": 2169, "W-2": 2178, "W-3": 2205, "W-4": 2256, "W-5": 2334,
    "O-1": 1857, "O-2": 2145, "O-3": 2202, "O-4": 2352, "O-5": 2466,
    "O-6": 2484, "O-7+": 2496, "Other": 1809,
}

# Per-installation rent planning ranges (low, high) for 3BR off-post.
_RENT_BY_PRIORITY: dict[Priority, tuple[int, int]] = {
    "High": (1300, 1750),
    "Medium": (1200, 1650),
    "Low": (1000, 1400),
}

# Geo and extended report fields for installations with hand-tuned report data.
_RICH_PROFILE_EXTENSIONS: dict[str, dict[str, Any]] = {
    "Fort Bragg, NC": {
        "key": "bragg",
        "city": "Fayetteville",
        "zip_code": "28307",
        "latitude": 35.1410,
        "longitude": -79.0060,
        "nearby_zip_codes": ("28303", "28348", "28390", "28376"),
        "bah_rates": _BAH_BRAGG,
        "avg_3br_rent_range": (1450, 1850),
        "off_post_areas": (
            "Hope Mills (28348) & Spring Lake (28390) — strong BAH value, 15–25 min commute",
            "Fayetteville north side (28303) — more inventory, watch school zones",
            "Raeford (28376) — quieter, longer commute, often lower rent",
        ),
        "utility_note": "Plan $150–$250/mo for electric/water off-post in summer months.",
        "spouse_employment_notes": (
            "Cape Fear Valley Health, Cumberland County Schools, and retail along Skibo Rd hire steadily",
            "Remote work viable with good broadband in Hope Mills / Fayetteville suburbs",
            "NC teaching license reciprocity available — start licensure packet early (4–8 weeks typical)",
        ),
        "childcare_notes": (
            "Fort Bragg CDC waitlists: 30–90 days for school-age; infant/toddler slots often 60–120 days",
            "Family Child Care (FCC) homes in Hope Mills/Spring Lake often have 2–4 week openings",
            "Submit CDC request (DD Form 2606) same day orders drop; ask ACS for current wait times",
        ),
        "spouse_programs": (
            "MSEP and My Career Advancement Account (MyCAA) for licensure/certification costs",
            "Hiring Our Heroes fellowship and ACS spouse employment workshops at Soldier Support Center",
        ),
        "vehicle_registration_note": "NC DMV: register within 30 days of establishing residency; bring title, insurance, and military orders.",
        "climate_note": "Mild winters; summer humidity drives higher AC costs off-post.",
        "commute_hotspots": ("All-American Fwy", "Bragg Blvd", "Murchison Rd gate"),
    },
    "Fort Hood, TX": {
        "key": "hood",
        "city": "Killeen",
        "zip_code": "76544",
        "latitude": 31.1349,
        "longitude": -97.7756,
        "nearby_zip_codes": ("76541", "76548", "76522", "76542"),
        "bah_rates": _BAH_HOOD,
        "avg_3br_rent_range": (1250, 1650),
        "off_post_areas": (
            "Killeen east side (76541) — most inventory, verify school zones",
            "Harker Heights (76548) — family-friendly, 10–20 min to main gates",
            "Copperas Cove (76522) — quieter, strong BAH value, 15–25 min commute",
        ),
        "utility_note": "Plan $175–$275/mo for electric/water off-post in peak summer AC months.",
        "spouse_employment_notes": (
            "Carl R. Darnall Army Medical Center, Killeen ISD, and on-post NAF roles",
            "Retail and service hiring along Veterans Memorial Blvd and Market Heights",
            "Remote work viable with good broadband in Harker Heights / Copperas Cove (200+ Mbps common)",
        ),
        "childcare_notes": (
            "Fort Hood CDC waitlists: 45–90 days for infants; school-age often 30–60 days in summer PCS surge",
            "FCC providers in Harker Heights and Copperas Cove are the fastest backup",
            "Submit CDC paperwork at in-processing; priority categories apply for dual-military and deployed sponsors",
        ),
        "spouse_programs": (
            "ACS Employment Readiness Program and Fort Hood Spouse Employment Center",
            "MSEP partners include CRDAMC and Killeen ISD for expedited hiring",
        ),
        "vehicle_registration_note": "Texas: register within 30 days; no state income tax but property tax applies to vehicles in some counties.",
        "climate_note": "Hot summers drive higher AC costs off-post; mild winters rarely spike heating bills.",
        "commute_hotspots": ("US-190", "Trimmier Rd", "Clear Creek Rd gate"),
    },
    "Fort Bliss, TX": {
        "key": "bliss",
        "city": "El Paso",
        "zip_code": "79916",
        "latitude": 31.8130,
        "longitude": -106.4220,
        "nearby_zip_codes": ("79925", "79928", "79938", "79934"),
        "bah_rates": _BAH_BLISS,
        "avg_3br_rent_range": (1250, 1650),
        "off_post_areas": (
            "Northeast El Paso (79925) — 10–20 min to main gates, strong school options",
            "Horizon City / East El Paso (79928) — newer builds, fenced yards common",
            "West El Paso / Sunland Park corridor (79922) — verify commute to unit area",
        ),
        "utility_note": "Plan $120–$200/mo electric in summer; water is modest in desert climate.",
        "spouse_employment_notes": (
            "William Beaumont Army Medical Center and Fort Bliss NAF health roles hire steadily",
            "El Paso Children's Hospital and Las Palmas Del Sol hire nurses with TX endorsement",
            "Federal civilian roles at Bliss and border agencies post on USAJOBS year-round",
        ),
        "childcare_notes": (
            "Fort Bliss CDC waitlists: 30–90 days school-age; infant/toddler often 60–120 days",
            "FCC homes in Northeast El Paso and Horizon City often open in 2–4 weeks",
            "Submit DD Form 2606 before departure — summer PCS surge adds 30+ days if delayed",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Bliss Spouse Employment Center",
            "MSEP partners include WBAMC and EPISD for expedited hiring",
            "MyCAA for spouse licensure and certification in healthcare/education fields",
        ),
        "vehicle_registration_note": "Texas: register within 30 days; no state income tax but vehicle property tax applies.",
        "climate_note": "Desert heat drives summer AC costs; monsoon season (Jul–Sep) can disrupt commutes.",
        "commute_hotspots": ("US-54", "Loop 375", "Cassidy Rd / Spur 601 gates"),
    },
    "Fort Drum, NY": {
        "key": "drum",
        "city": "Watertown",
        "zip_code": "13602",
        "latitude": 44.0520,
        "longitude": -75.7890,
        "nearby_zip_codes": ("13637", "13619", "13601", "13612"),
        "bah_rates": _BAH_DRUM,
        "avg_3br_rent_range": (1300, 1700),
        "off_post_areas": (
            "Evans Mills / Le Ray (13637) — shortest commute, moderate rents",
            "Carthage (13619) — family-friendly, 15–20 min to post",
            "Watertown (13601) — most inventory & services, verify commute tolerance",
        ),
        "utility_note": "Budget higher winter heating ($200–$350/mo peak) off-post.",
        "spouse_employment_notes": (
            "Samaritan Medical Center, Jefferson County schools, and on-post NAF roles",
            "NY nursing endorsement: 4–8 weeks typical; temporary permit possible in 2–3 weeks",
            "Remote work works well; winter travel for in-person roles needs planning",
        ),
        "childcare_notes": (
            "Fort Drum CDC infant/toddler waitlists routinely 3–6 months — submit DD 2606 immediately",
            "FCC homes in Evans Mills/Le Ray often have 2–4 week openings as parallel track",
            "Peak summer PCS surge can add 30+ days to any childcare slot",
        ),
        "spouse_programs": (
            "ACS Spouse Employment and Fort Drum Military Spouse Preference for on-post NAF roles",
            "MyCAA covers nursing CEU/certification costs where eligible",
        ),
        "vehicle_registration_note": "NY DMV: register within 30 days; emissions/safety inspection required.",
        "climate_note": "Lake-effect snow and heating costs are real budget factors.",
        "commute_hotspots": ("Route 11", "Route 26", "California Rd gate"),
    },
    "Fort Gordon, GA": {
        "key": "gordon",
        "city": "Augusta",
        "zip_code": "30905",
        "latitude": 33.4268,
        "longitude": -82.1460,
        "nearby_zip_codes": ("30907", "30809", "30909", "30813"),
        "bah_rates": _BAH_GORDON,
        "avg_3br_rent_range": (1350, 1750),
        "off_post_areas": (
            "Evans / Martinez (30809) — popular with military families, 15–20 min commute",
            "Grovetown (30813) — newer construction, verify gate drive time",
            "West Augusta (30907) — more inventory and services, watch school zones",
        ),
        "utility_note": "Plan $150–$225/mo for electric/water off-post in summer months.",
        "spouse_employment_notes": (
            "AU Health, Columbia County schools, and Augusta cyber/defense contractors hire steadily",
            "Remote work viable with strong broadband in Evans and Grovetown",
            "GA teaching/nursing license reciprocity available — start packet early (4–6 weeks typical)",
        ),
        "childcare_notes": (
            "Fort Gordon CDC waitlists: 30–75 days depending on age group; summer PCS surge tightens slots",
            "FCC providers in Evans/Martinez corridor are fastest backup for toddlers",
            "Submit CDC request at in-processing; dual-military families may qualify for priority",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Augusta cyber corridor MSEP hiring events",
            "MyCAA for spouse licensure and certification in healthcare/education fields",
        ),
        "vehicle_registration_note": "GA DMV: register within 30 days; TAVT applies to new residents registering vehicles.",
        "climate_note": "Hot, humid summers drive AC costs; mild winters with occasional ice on bridges.",
        "commute_hotspots": ("Gordon Hwy", "Jimmie Dyess Pkwy", "Gate 1 / Gate 3 corridors"),
    },
    "Fort Campbell, KY": {
        "key": "campbell",
        "city": "Clarksville",
        "zip_code": "42223",
        "latitude": 36.6530,
        "longitude": -87.4600,
        "nearby_zip_codes": ("37042", "37040", "42223", "42262"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1350, 1750),
        "off_post_areas": (
            "Clarksville, TN (37042) — most inventory, verify TN vs KY school zoning",
            "Oak Grove, KY (42223) — shorter commute, quieter neighborhoods",
            "Hopkinsville, KY (42240) — lower rent, 20–25 min to gates",
        ),
        "utility_note": "Plan $140–$220/mo electric; TN side inventory turns faster in summer PCS.",
        "spouse_employment_notes": (
            "Blanchfield Army Community Hospital, Clarksville-Montgomery County Schools, and trades contractors on TN side",
            "KY/TN licensure differs for trades and healthcare — verify state before applying",
            "Gate traffic on Madam Walker peaks with 101st cycles — factor spouse interview windows",
        ),
        "childcare_notes": (
            "Fort Campbell CDC waitlists: 30–90 days school-age; infant/toddler 60–120 days in summer surge",
            "FCC homes in Oak Grove and Clarksville often open in 2–4 weeks",
            "IEP transfers require district registrar meeting within 10 school days — book before lease signing",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Campbell Spouse Employment Center",
            "MSEP at Blanchfield and Clarksville-Montgomery County Schools",
            "MyCAA for trades certification and licensure costs",
        ),
        "vehicle_registration_note": "TN or KY registration depending on residence — 30-day rule applies in both states.",
        "climate_note": "Mild winters; humid summers; KY/TN line affects school district and state tax.",
        "commute_hotspots": ("Madam Walker Blvd", "Fort Campbell Blvd", "Wilma Rudolph Blvd"),
    },
    "Fort Benning, GA": {
        "key": "benning",
        "city": "Columbus",
        "zip_code": "31905",
        "latitude": 32.3540,
        "longitude": -84.9680,
        "nearby_zip_codes": ("31909", "31907", "36867", "31820"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1250, 1650),
        "off_post_areas": (
            "Columbus north / Midland (31909) — strong Muscogee County schools, 15–20 min",
            "Phenix City, AL (36867) — verify GA school zoning before signing AL lease",
            "Upatoi / east Columbus (31820) — quieter, longer commute",
        ),
        "utility_note": "Plan $150–$240/mo electric in summer humidity; AL leases need GA school check.",
        "spouse_employment_notes": (
            "Muscogee County Schools, Piedmont Columbus Regional, and Fort Benning NAF roles",
            "Heavy training tempo — spouse interviews best scheduled after 0900 to avoid graduation traffic",
            "MyCAA strong for spouse continuing education while sponsor in MCoE pipeline",
        ),
        "childcare_notes": (
            "Fort Benning CDC waitlists: 45–90 days infants; school-age 30–60 days",
            "EFMP coordination must transfer before housing lock — delays narrow on-post options",
            "IEP continuity requires Muscogee County registrar packet within first 10 school days",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Benning Spouse Employment Center",
            "MSEP at Piedmont and Muscogee County Schools",
        ),
        "vehicle_registration_note": "GA DMV: register within 30 days; AL residents working in GA still need school zoning clarity.",
        "climate_note": "Hot, humid summers; ice rare but training tempo drives gate delays year-round.",
        "commute_hotspots": ("US-280", "Victory Drive", "Interstate 185 gate corridors"),
    },
    "Fort Stewart, GA": {
        "key": "stewart",
        "city": "Hinesville",
        "zip_code": "31314",
        "latitude": 31.8690,
        "longitude": -81.6080,
        "nearby_zip_codes": ("31313", "31324", "31326", "31328"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1200, 1550),
        "off_post_areas": (
            "Hinesville (31313) — shortest commute, Liberty County schools",
            "Richmond Hill (31324) — stronger schools, 20–25 min, higher rent",
            "Pooler / west Savannah (31322) — more inventory, verify commute tolerance",
        ),
        "utility_note": "Plan $160–$260/mo electric in summer humidity; hurricane season affects insurance off-post.",
        "spouse_employment_notes": (
            "Liberty County Schools, Winn Army Community Hospital NAF, and Savannah retail corridor",
            "Retail and hospitality hire fast — part-time bridge roles common within 2–4 weeks",
        ),
        "childcare_notes": (
            "Fort Stewart CDC infant waitlists: 60–120 days — submit DD 2606 before departure",
            "FCC in Hinesville is fastest path for infant + preschool combo",
            "Hurricane season (Jun–Nov) can delay movers — build 5-day buffer into TLE plan",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Stewart Spouse Employment Center",
            "MSEP at Winn ACH and Liberty County Schools",
        ),
        "vehicle_registration_note": "GA DMV: register within 30 days; coastal county insurance rates vary.",
        "climate_note": "Coastal humidity and hurricane season affect utilities and insurance.",
        "commute_hotspots": ("GA-119", "US-84", "Gate 1 / Gate 2 corridors"),
    },
    "Fort Sill, OK": {
        "key": "sill",
        "city": "Lawton",
        "zip_code": "73503",
        "latitude": 34.6690,
        "longitude": -98.4010,
        "nearby_zip_codes": ("73505", "73507", "73527", "73501"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (950, 1300),
        "off_post_areas": (
            "Lawton west (73505) — most inventory, Lawton Public Schools",
            "Cache (73527) — quieter, 10–15 min, verify tornado shelter disclosure",
            "Medicine Park (73557) — scenic, limited inventory, longer commute",
        ),
        "utility_note": "Plan $120–$200/mo electric; wind/hail affect off-post insurance — get shelter clause in lease.",
        "spouse_employment_notes": (
            "Lawton Public Schools, Comanche County Memorial Hospital, and on-post NAF retail",
            "Retail and service roles often hire within 2–4 weeks — good bridge for part-time income",
        ),
        "childcare_notes": (
            "Fort Sill CDC infant/toddler waitlists: 45–90 days; school-age faster in off-peak PCS",
            "FCC in Lawton west side often has 2–3 week openings",
            "Ask landlords about tornado shelter or interior safe room — especially with infants",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and Fort Sill Spouse Employment Center",
            "MSEP at Comanche County Memorial and Lawton PSD",
        ),
        "vehicle_registration_note": "OK DMV: register within 30 days; lower cost of living but verify renter's insurance for hail.",
        "climate_note": "Tornado and hail season — verify shelter access and renter's insurance riders.",
        "commute_hotspots": ("Sheridan Road", "Fort Sill Blvd", "Quanah Rd gate"),
    },
    "Joint Base Lewis-McChord, WA": {
        "key": "jblm",
        "city": "Lakewood",
        "zip_code": "98433",
        "latitude": 47.1120,
        "longitude": -122.5860,
        "nearby_zip_codes": ("98439", "98327", "98374", "98597"),
        "bah_rates": _BAH_DEFAULT,
        "avg_3br_rent_range": (1850, 2400),
        "off_post_areas": (
            "DuPont (98327) — walkable to Madigan, inventory turns in days in summer",
            "Lakewood / Tillicum (98439) — more inventory, verify I-5 commute",
            "Yelm (98597) — lower rent, 25–35 min, Yelm Community Schools",
        ),
        "utility_note": "Plan $180–$280/mo electric; rain drives mold risk — inspect ventilation before signing.",
        "spouse_employment_notes": (
            "Madigan Army Medical Center, MultiCare, and Pierce County school districts",
            "WA nursing endorsement: 4–8 weeks; temp permit possible — start before departure",
            "Tight rental market — spouse job search should parallel housing, not follow it",
        ),
        "childcare_notes": (
            "JBLM CDC waitlists: 60–120 days infants; preschool 30–60 days in PCS surge",
            "FCC in DuPont and Lakewood often faster than CDC for preschoolers",
            "Rain and traffic compound commute — childcare near lease address reduces daily risk",
        ),
        "spouse_programs": (
            "ACS Employment Readiness and JBLM Spouse Employment Center",
            "MSEP at Madigan and Clover Park School District",
            "MyCAA for nursing CEU and certification",
        ),
        "vehicle_registration_note": "WA DOL: register within 30 days; no state income tax but rental market is competitive.",
        "climate_note": "Rain 8+ months — budget dehumidifier and mold prevention; winter dark affects morale.",
        "commute_hotspots": ("I-5", "SR-507", "DuPont gate / McChord Field gates"),
    },
}

_ON_POST_PROS = (
    "No rent out-of-pocket when assigned — BAH absorbed by housing",
    "Short commute and maintenance handled on-post",
    "Utilities often included in government housing",
)
_ON_POST_CONS = (
    "Waitlists spike before summer PCS season",
    "Limited floor-plan and neighborhood choice",
    "Older housing stock in some areas",
)


def _build_profile(canonical_name: str) -> InstallationProfile:
    """Build an InstallationProfile from INSTALLATION_DATA plus optional rich extensions."""
    data = INSTALLATION_DATA[canonical_name]
    rich = _RICH_PROFILE_EXTENSIONS.get(canonical_name, {})
    short_name = canonical_name.rsplit(", ", 1)[0]
    state = data["state"].split("/")[0]  # KY/TN → KY for profile state field
    priority: Priority = data["priority"]
    rent = rich.get("avg_3br_rent_range", _RENT_BY_PRIORITY[priority])

    major_areas = data["major_areas"]
    off_post = rich.get(
        "off_post_areas",
        tuple(f"{area} — verify school zoning and gate commute" for area in major_areas),
    )

    return InstallationProfile(
        key=rich.get("key", short_name.lower().replace(" ", "-").replace("joint-base-", "jb-")),
        display_name=canonical_name,
        short_name=short_name,
        city=rich.get("city", major_areas[0] if major_areas else ""),
        state=state,
        zip_code=rich.get("zip_code", ""),
        latitude=rich.get("latitude", 0.0),
        longitude=rich.get("longitude", 0.0),
        nearby_zip_codes=rich.get("nearby_zip_codes", ()),
        bah_rates=rich.get("bah_rates", _BAH_DEFAULT),
        housing=HousingMarket(
            on_post_pros=_ON_POST_PROS,
            on_post_cons=_ON_POST_CONS,
            off_post_areas=off_post,
            avg_3br_rent_range=rent,
            utility_note=rich.get(
                "utility_note",
                "Estimate $150–$250/mo utilities off-post; climate drives variance.",
            ),
        ),
        school_districts=tuple(data["school_districts"]),
        spouse_employment_notes=rich.get(
            "spouse_employment_notes",
            (
                f"Check hospital systems, school districts, and employers near {major_areas[0]}",
                "ACS Employment Readiness and MSEP available on-post",
            ),
        ),
        childcare_notes=rich.get(
            "childcare_notes",
            (
                "Submit DD Form 2606 same day orders drop",
                "FCC homes are typically faster than CDC for school-age and infants",
                "Contact ACS for current CDC waitlist estimates",
            ),
        ),
        spouse_programs=rich.get(
            "spouse_programs",
            (
                "ACS Employment Readiness Program and MSEP at most installations",
                "MyCAA for eligible spouse licensure and certification costs",
            ),
        ),
        vehicle_registration_note=rich.get(
            "vehicle_registration_note",
            f"Register vehicles within 30 days of establishing residency in {state}.",
        ),
        climate_note=rich.get("climate_note", data["notes"]),
        commute_hotspots=rich.get(
            "commute_hotspots",
            (data["commute_notes"][:80] + "…" if len(data["commute_notes"]) > 80 else data["commute_notes"],),
        ),
        priority=priority,
        notes=data["notes"],
    )


INSTALLATIONS: dict[str, InstallationProfile] = {
    name: _build_profile(name) for name in INSTALLATION_DATA
}

DEFAULT_INSTALLATION = InstallationProfile(
    key="generic",
    display_name="Your gaining installation",
    short_name="gaining installation",
    city="",
    state="",
    zip_code="",
    latitude=0.0,
    longitude=0.0,
    nearby_zip_codes=(),
    bah_rates=_BAH_DEFAULT,
    housing=HousingMarket(
        on_post_pros=_ON_POST_PROS[:2],
        on_post_cons=_ON_POST_CONS[:2],
        off_post_areas=(
            "Start research within a 30-minute gate-to-door commute",
            "Compare 3-bedroom rent to BAH before signing",
        ),
        avg_3br_rent_range=(1400, 1800),
        utility_note="Estimate utilities separately — they often decide on-post vs off-post value.",
    ),
    school_districts=("Verify district boundaries before lease signing",),
    spouse_employment_notes=(
        "Check local hospital systems, school districts, and remote-work feasibility",
    ),
    childcare_notes=(
        "Contact installation ACS for current CDC waitlist estimates",
        "FCC homes are typically the fastest backup for infants and toddlers",
    ),
    spouse_programs=(
        "ACS Employment Readiness Program and MSEP at most installations",
        "MyCAA for eligible spouse licensure and certification costs",
    ),
    vehicle_registration_note="Register vehicles within 30 days of establishing residency in the new state.",
    climate_note="Local weather affects utility costs and commute reliability.",
    commute_hotspots=("Main gate corridors at peak duty hours",),
    priority="Medium",
    notes="Generic fallback — add this installation to INSTALLATION_DATA for tailored guidance.",
)


# Approximate CONUS driving distances for DITY/PPM planning (miles, one-way).
MOVE_ROUTE_MILES: dict[tuple[str, str], int] = {
    ("Fort Hood, TX", "Fort Bragg, NC"): 1180,
    ("Fort Bragg, NC", "Fort Hood, TX"): 1180,
    ("Fort Gordon, GA", "Fort Drum, NY"): 980,
    ("Fort Drum, NY", "Fort Gordon, GA"): 980,
    ("Fort Bragg, NC", "Fort Drum, NY"): 780,
    ("Fort Drum, NY", "Fort Bragg, NC"): 780,
    ("Fort Hood, TX", "Fort Drum, NY"): 1580,
    ("Fort Gordon, GA", "Fort Bragg, NC"): 320,
    ("Fort Bragg, NC", "Fort Gordon, GA"): 320,
    ("Fort Hood, TX", "Fort Gordon, GA"): 860,
    ("Fort Gordon, GA", "Fort Hood, TX"): 860,
    ("Fort Bragg, NC", "Fort Bliss, TX"): 1680,
    ("Fort Bliss, TX", "Fort Bragg, NC"): 1680,
    ("Fort Bragg, NC", "Fort Benning, GA"): 280,
    ("Fort Benning, GA", "Fort Bragg, NC"): 280,
    ("Fort Bragg, NC", "Fort Campbell, KY"): 520,
    ("Fort Campbell, KY", "Fort Bragg, NC"): 520,
    ("Fort Hood, TX", "Fort Bliss, TX"): 620,
    ("Fort Bliss, TX", "Fort Hood, TX"): 620,
    ("Joint Base Lewis-McChord, WA", "Fort Hood, TX"): 2100,
    ("Fort Hood, TX", "Joint Base Lewis-McChord, WA"): 2100,
    ("Fort Benning, GA", "Fort Campbell, KY"): 380,
    ("Fort Campbell, KY", "Fort Benning, GA"): 380,
    ("Fort Bliss, TX", "Joint Base Lewis-McChord, WA"): 1850,
    ("Joint Base Lewis-McChord, WA", "Fort Bliss, TX"): 1850,
    ("Fort Leavenworth, KS", "Fort Bragg, NC"): 1050,
    ("Fort Bragg, NC", "Fort Leavenworth, KS"): 1050,
    ("Fort Stewart, GA", "Fort Sill, OK"): 1150,
    ("Fort Sill, OK", "Fort Stewart, GA"): 1150,
    ("Fort Hood, TX", "Fort Benning, GA"): 880,
    ("Fort Benning, GA", "Fort Hood, TX"): 880,
}


def build_move_context(current_label: str, gaining_label: str) -> dict:
    """Return move-distance context for DITY/TLE planning."""
    current = _canonical_installation_name(current_label) or current_label
    gaining = _canonical_installation_name(gaining_label) or gaining_label
    miles = MOVE_ROUTE_MILES.get((current, gaining))
    if miles is None:
        return {
            "origin": current_label,
            "destination": gaining_label,
            "approximate_miles_one_way": None,
            "dity_planning_note": (
                "Verify distance with TMO; for CONUS moves over 500 miles, "
                "full or partial DITY often nets $1,500–5,000 after expenses."
            ),
        }
    driving_days = max(2, round(miles / 500))
    return {
        "origin": current_label,
        "destination": gaining_label,
        "approximate_miles_one_way": miles,
        "estimated_driving_days": driving_days,
        "dity_planning_note": (
            f"~{miles} miles one-way ({driving_days} driving days). "
            "Partial DITY (HHG only) often nets $1,200–3,000; full DITY can add "
            "$1,500–4,000 if weight allowance is maximized — verify with TMO."
        ),
    }


def resolve_installation(gaining_label: str) -> InstallationProfile:
    """Return installation profile from form gaining-installation value."""
    canonical = _canonical_installation_name(gaining_label)
    if canonical and canonical in INSTALLATIONS:
        return INSTALLATIONS[canonical]
    return DEFAULT_INSTALLATION


def get_bah_estimate(pay_grade: str, profile: InstallationProfile) -> int:
    """Return monthly BAH with dependents (2026 DTMO rates when available)."""
    from services.bah_rates import get_bah_monthly

    live = get_bah_monthly(profile.display_name, pay_grade)
    if live is not None:
        return live
    return profile.bah_rates.get(pay_grade, profile.bah_rates.get("E-5", 1600))


def get_bah_reference(pay_grade: str, profile: InstallationProfile) -> dict:
    """Return BAH metadata including source and effective date."""
    from services.bah_rates import get_bah_rate

    ref = get_bah_rate(profile.display_name, pay_grade, with_dependents=True)
    if ref.get("found"):
        return ref
    amount = profile.bah_rates.get(pay_grade, profile.bah_rates.get("E-5", 1600))
    return {
        "monthly_usd": amount,
        "mha": profile.display_name,
        "effective_date": "planning-fallback",
        "source": "PCS Vector static fallback (update bah_2026.json)",
        "with_dependents": True,
        "found": True,
    }


def build_installation_context(profile: InstallationProfile, pay_grade: str) -> dict:
    """Serialize installation reference data for the Grok prompt."""
    bah_ref = get_bah_reference(pay_grade, profile)
    bah = bah_ref["monthly_usd"]
    rent_low, rent_high = profile.housing.avg_3br_rent_range
    base_data = get_installation_data(profile.display_name) or {}
    return {
        "installation": profile.display_name,
        "short_name": profile.short_name,
        "priority": profile.priority,
        "installation_notes": profile.notes or base_data.get("notes", ""),
        "location": {
            "city": profile.city,
            "state": profile.state,
            "zip_code": profile.zip_code,
            "latitude": profile.latitude,
            "longitude": profile.longitude,
            "nearby_zip_codes": list(profile.nearby_zip_codes),
        },
        "major_areas": base_data.get("major_areas", []),
        "commute_notes": base_data.get("commute_notes", ""),
        "estimated_bah_with_dependents_usd": bah,
        "bah_reference": bah_ref,
        "typical_3br_rent_range_usd": {"low": rent_low, "high": rent_high},
        "bah_surplus_if_rent_at_low": bah - rent_low,
        "bah_gap_if_rent_at_high": bah - rent_high,
        "on_post_pros": list(profile.housing.on_post_pros),
        "on_post_cons": list(profile.housing.on_post_cons),
        "off_post_areas_to_research": list(profile.housing.off_post_areas),
        "utility_note": profile.housing.utility_note,
        "school_districts": list(profile.school_districts),
        "spouse_employment_leads": list(profile.spouse_employment_notes),
        "childcare_waitlist_notes": list(profile.childcare_notes),
        "military_spouse_programs": list(profile.spouse_programs),
        "vehicle_registration_note": profile.vehicle_registration_note,
        "climate_and_cost_note": profile.climate_note,
        "commute_hotspots": list(profile.commute_hotspots),
        "housing_table_guidance": {
            "on_post_out_of_pocket_rent_usd": 0,
            "on_post_note": "Assigned government housing — BAH is absorbed; no monthly rent payment.",
            "use_rent_low_for_surplus_calc": bah - rent_low,
            "use_rent_high_for_shortfall_calc": bah - rent_high,
        },
    }


# ---------------------------------------------------------------------------
# HOW TO ADD A NEW INSTALLATION
# ---------------------------------------------------------------------------
# 1. Add an entry to INSTALLATION_DATA using the traditional name as the key
#    (e.g. "Fort Example, ST"). Required fields: state, priority (High/Medium/Low),
#    notes, major_areas, school_districts, commute_notes.
#
# 2. If the Army has renamed the post, add the new official name to
#    INSTALLATION_ALIASES pointing to your traditional key — never use the new
#    name in user-facing copy.
#
# 3. (Optional) Add hand-tuned report fields to _RICH_PROFILE_EXTENSIONS for
#    bases that need zip codes, BAH fallbacks, spouse/childcare detail, or
#    commute hotspots beyond the generic template.
#
# 4. (Optional) Add 2026 BAH rates to data/bah_2026.json so get_bah_estimate()
#    pulls live DTMO figures instead of planning fallbacks.
#
# 5. (Optional) Add MOVE_ROUTE_MILES pairs for common PCS corridors involving
#    the new installation (both directions).
#
# 6. Update components/form_options.py CURRENT_INSTALLATIONS and
#    GAINING_INSTALLATIONS from SUPPORTED_INSTALLATIONS if the post should
#    appear in the Streamlit dropdown.
#
# INSTALLATIONS and SUPPORTED_INSTALLATIONS rebuild automatically from
# INSTALLATION_DATA — no separate list maintenance required.
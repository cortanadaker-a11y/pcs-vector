"""Installation-specific reference data for report templates.

BAH figures are illustrative estimates for planning purposes (with dependents).
Replace with live DFAS data when connecting to external APIs.
"""

from __future__ import annotations

from dataclasses import dataclass


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
    legacy_name: str
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


# Estimated monthly BAH with dependents (2025–2026 planning figures)
_BAH_BRAGG: dict[str, int] = {
    "E-1": 1428,
    "E-2": 1428,
    "E-3": 1428,
    "E-4": 1506,
    "E-5": 1653,
    "E-6": 1716,
    "E-7": 1836,
    "E-8": 1896,
    "E-9": 1944,
    "W-1": 1716,
    "W-2": 1836,
    "W-3": 1920,
    "W-4": 2016,
    "W-5": 2088,
    "O-1": 1716,
    "O-2": 1836,
    "O-3": 2016,
    "O-4": 2184,
    "O-5": 2328,
    "O-6": 2496,
    "O-7+": 2688,
    "Other": 1653,
}

_BAH_HOOD: dict[str, int] = {
    "E-1": 1380,
    "E-2": 1380,
    "E-3": 1380,
    "E-4": 1458,
    "E-5": 1542,
    "E-6": 1602,
    "E-7": 1710,
    "E-8": 1770,
    "E-9": 1818,
    "W-1": 1602,
    "W-2": 1710,
    "W-3": 1794,
    "W-4": 1878,
    "W-5": 1950,
    "O-1": 1602,
    "O-2": 1710,
    "O-3": 1878,
    "O-4": 2034,
    "O-5": 2166,
    "O-6": 2322,
    "O-7+": 2502,
    "Other": 1542,
}

_BAH_DRUM: dict[str, int] = {
    "E-1": 1332,
    "E-2": 1332,
    "E-3": 1332,
    "E-4": 1404,
    "E-5": 1548,
    "E-6": 1608,
    "E-7": 1716,
    "E-8": 1776,
    "E-9": 1824,
    "W-1": 1608,
    "W-2": 1716,
    "W-3": 1800,
    "W-4": 1884,
    "W-5": 1956,
    "O-1": 1608,
    "O-2": 1716,
    "O-3": 1884,
    "O-4": 2040,
    "O-5": 2172,
    "O-6": 2328,
    "O-7+": 2508,
    "Other": 1548,
}

_BAH_GORDON: dict[str, int] = {
    "E-1": 1356,
    "E-2": 1356,
    "E-3": 1356,
    "E-4": 1428,
    "E-5": 1572,
    "E-6": 1632,
    "E-7": 1740,
    "E-8": 1800,
    "E-9": 1848,
    "W-1": 1632,
    "W-2": 1740,
    "W-3": 1824,
    "W-4": 1908,
    "W-5": 1980,
    "O-1": 1632,
    "O-2": 1740,
    "O-3": 1908,
    "O-4": 2064,
    "O-5": 2196,
    "O-6": 2352,
    "O-7+": 2532,
    "Other": 1572,
}

INSTALLATIONS: dict[str, InstallationProfile] = {
    "Fort Bragg, NC": InstallationProfile(
        key="bragg",
        display_name="Fort Bragg, NC",
        short_name="Fort Bragg",
        legacy_name="Fort Liberty",
        city="Fayetteville",
        state="NC",
        zip_code="28307",
        latitude=35.1410,
        longitude=-79.0060,
        nearby_zip_codes=("28303", "28348", "28390", "28376"),
        bah_rates=_BAH_BRAGG,
        housing=HousingMarket(
            on_post_pros=(
                "No rent out-of-pocket if BAH covers assigned housing",
                "Gated security and short commute to main cantonment",
                "Utilities often included in government housing",
            ),
            on_post_cons=(
                "Waitlists vary by bedroom count and season",
                "Older housing stock in some neighborhoods",
                "Less choice on layout compared to off-post rentals",
            ),
            off_post_areas=(
                "Hope Mills (28348) & Spring Lake (28390) — strong BAH value, 15–25 min commute",
                "Fayetteville north side (28303) — more inventory, watch school zones",
                "Raeford (28376) — quieter, longer commute, often lower rent",
            ),
            avg_3br_rent_range=(1450, 1850),
            utility_note="Plan $150–$250/mo for electric/water off-post in summer months.",
        ),
        school_districts=(
            "Cumberland County Schools (largest footprint near post)",
            "Harnett County (Raeford area — verify zoning before signing lease)",
            "Private options in Fayetteville corridor if school rating is top priority",
        ),
        spouse_employment_notes=(
            "Cape Fear Valley Health, Cumberland County Schools, and retail along Skibo Rd hire steadily",
            "Remote work viable with good broadband in Hope Mills / Fayetteville suburbs",
            "NC teaching license reciprocity available — start licensure packet early (4–8 weeks typical)",
        ),
        childcare_notes=(
            "Fort Bragg CDC waitlists: 30–90 days for school-age; infant/toddler slots often 60–120 days",
            "Family Child Care (FCC) homes in Hope Mills/Spring Lake often have 2–4 week openings",
            "Submit CDC request (DD Form 2606) same day orders drop; ask ACS for current wait times",
        ),
        spouse_programs=(
            "MSEP and My Career Advancement Account (MyCAA) for licensure/certification costs",
            "Hiring Our Heroes fellowship and ACS spouse employment workshops at Soldier Support Center",
        ),
        vehicle_registration_note="NC DMV: register within 30 days of establishing residency; bring title, insurance, and military orders.",
        climate_note="Mild winters; summer humidity drives higher AC costs off-post.",
        commute_hotspots=("All-American Fwy", "Bragg Blvd", "Murchison Rd gate"),
    ),
    "Fort Hood, TX": InstallationProfile(
        key="hood",
        display_name="Fort Hood, TX",
        short_name="Fort Hood",
        legacy_name="Fort Cavazos",
        city="Killeen",
        state="TX",
        zip_code="76544",
        latitude=31.1349,
        longitude=-97.7756,
        nearby_zip_codes=("76541", "76548", "76522", "76542"),
        bah_rates=_BAH_HOOD,
        housing=HousingMarket(
            on_post_pros=(
                "Predictable housing cost in a competitive Central Texas rental market",
                "Short commute to main cantonment and unit areas",
                "Maintenance handled on-post — helpful during high-tempo cycles",
            ),
            on_post_cons=(
                "Waitlists can spike before summer PCS season",
                "Older floor plans in some neighborhoods",
                "Less flexibility on layout compared to off-post rentals",
            ),
            off_post_areas=(
                "Killeen east side (76541) — most inventory, verify school zones",
                "Harker Heights (76548) — family-friendly, 10–20 min to main gates",
                "Copperas Cove (76522) — quieter, strong BAH value, 15–25 min commute",
            ),
            avg_3br_rent_range=(1250, 1650),
            utility_note="Plan $175–$275/mo for electric/water off-post in peak summer AC months.",
        ),
        school_districts=(
            "Killeen Independent School District (largest footprint near post)",
            "Copperas Cove Independent School District — popular with military families",
            "Private options in Harker Heights / Killeen corridor if ratings are top priority",
        ),
        spouse_employment_notes=(
            "Carl R. Darnall Army Medical Center, Killeen ISD, and on-post NAF roles",
            "Retail and service hiring along Veterans Memorial Blvd and Market Heights",
            "Remote work viable with good broadband in Harker Heights / Copperas Cove (200+ Mbps common)",
        ),
        childcare_notes=(
            "Fort Hood CDC waitlists: 45–90 days for infants; school-age often 30–60 days in summer PCS surge",
            "FCC providers in Harker Heights and Copperas Cove are the fastest backup",
            "Submit CDC paperwork at in-processing; priority categories apply for dual-military and deployed sponsors",
        ),
        spouse_programs=(
            "ACS Employment Readiness Program and Fort Hood Spouse Employment Center",
            "MSEP partners include CRDAMC and Killeen ISD for expedited hiring",
        ),
        vehicle_registration_note="Texas: register within 30 days; no state income tax but property tax applies to vehicles in some counties.",
        climate_note="Hot summers drive higher AC costs off-post; mild winters rarely spike heating bills.",
        commute_hotspots=("US-190", "Trimmier Rd", "Clear Creek Rd gate"),
    ),
    "Fort Drum, NY": InstallationProfile(
        key="drum",
        display_name="Fort Drum, NY",
        short_name="Fort Drum",
        legacy_name="Fort Drum",
        city="Watertown",
        state="NY",
        zip_code="13602",
        latitude=44.0520,
        longitude=-75.7890,
        nearby_zip_codes=("13637", "13619", "13601", "13612"),
        bah_rates=_BAH_DRUM,
        housing=HousingMarket(
            on_post_pros=(
                "Predictable housing cost — helpful in a tight winter rental market",
                "Snow removal and maintenance handled on-post",
                "Close to unit areas during high-tempo seasons",
            ),
            on_post_cons=(
                "Waitlists can spike before summer PCS season",
                "Older floor plans in some villages",
                "Limited off-post-equivalent amenities within walking distance",
            ),
            off_post_areas=(
                "Evans Mills / Le Ray (13637) — shortest commute, moderate rents",
                "Carthage (13619) — family-friendly, 15–20 min to post",
                "Watertown (13601) — most inventory & services, verify commute tolerance",
            ),
            avg_3br_rent_range=(1300, 1700),
            utility_note="Budget higher winter heating ($200–$350/mo peak) off-post.",
        ),
        school_districts=(
            "Indian River Central School District (popular with military families)",
            "Watertown City School District — more services, urban environment",
            "Carthage area schools — quieter, check bus routes if off-post",
        ),
        spouse_employment_notes=(
            "Samaritan Medical Center, Jefferson County schools, and on-post NAF roles",
            "NY nursing endorsement: 4–8 weeks typical; temporary permit possible in 2–3 weeks",
            "Remote work works well; winter travel for in-person roles needs planning",
        ),
        childcare_notes=(
            "Fort Drum CDC infant/toddler waitlists routinely 3–6 months — submit DD 2606 immediately",
            "FCC homes in Evans Mills/Le Ray often have 2–4 week openings as parallel track",
            "Peak summer PCS surge can add 30+ days to any childcare slot",
        ),
        spouse_programs=(
            "ACS Spouse Employment and Fort Drum Military Spouse Preference for on-post NAF roles",
            "MyCAA covers nursing CEU/certification costs where eligible",
        ),
        vehicle_registration_note="NY DMV: register within 30 days; emissions/safety inspection required — post auto skills center can assist.",
        climate_note="Lake-effect snow and heating costs are real budget factors — factor into off-post choice.",
        commute_hotspots=("Route 11", "Route 26", "California Rd gate"),
    ),
    "Fort Gordon, GA": InstallationProfile(
        key="gordon",
        display_name="Fort Gordon, GA",
        short_name="Fort Gordon",
        legacy_name="Fort Eisenhower",
        city="Augusta",
        state="GA",
        zip_code="30905",
        latitude=33.4268,
        longitude=-82.1460,
        nearby_zip_codes=("30907", "30809", "30909", "30813"),
        bah_rates=_BAH_GORDON,
        housing=HousingMarket(
            on_post_pros=(
                "Predictable housing cost near a growing Augusta metro market",
                "Short commute to cyber and signal school corridors",
                "Maintenance handled on-post during high-tempo training cycles",
            ),
            on_post_cons=(
                "Waitlists vary by bedroom count before summer PCS season",
                "Older floor plans in some neighborhoods",
                "Less inventory on-post than off-post in peak PCS windows",
            ),
            off_post_areas=(
                "Evans / Martinez (30809) — popular with military families, 15–20 min commute",
                "Grovetown (30813) — newer construction, verify gate drive time",
                "West Augusta (30907) — more inventory and services, watch school zones",
            ),
            avg_3br_rent_range=(1350, 1750),
            utility_note="Plan $150–$225/mo for electric/water off-post in summer months.",
        ),
        school_districts=(
            "Columbia County Schools (Evans / Grovetown — verify zoning before lease)",
            "Richmond County Schools (Augusta corridor — more services, varied ratings)",
            "Private options in Martinez / west Augusta if school rating is top priority",
        ),
        spouse_employment_notes=(
            "AU Health, Columbia County schools, and Augusta cyber/defense contractors hire steadily",
            "Remote work viable with strong broadband in Evans and Grovetown",
            "GA teaching/nursing license reciprocity available — start packet early (4–6 weeks typical)",
        ),
        childcare_notes=(
            "Fort Gordon CDC waitlists: 30–75 days depending on age group; summer PCS surge tightens slots",
            "FCC providers in Evans/Martinez corridor are fastest backup for toddlers",
            "Submit CDC request at in-processing; dual-military families may qualify for priority",
        ),
        spouse_programs=(
            "ACS Employment Readiness and Augusta cyber corridor MSEP hiring events",
            "MyCAA for spouse licensure and certification in healthcare/education fields",
        ),
        vehicle_registration_note="GA DMV: register within 30 days; TAVT (title ad valorem tax) applies to new residents registering vehicles.",
        climate_note="Hot, humid summers drive AC costs; mild winters with occasional ice on bridges.",
        commute_hotspots=("Gordon Hwy", "Jimmie Dyess Pkwy", "Gate 1 / Gate 3 corridors"),
    ),
}

# Map renamed or legacy labels to traditional installation keys used in the app.
INSTALLATION_ALIASES: dict[str, str] = {
    "Fort Liberty, NC": "Fort Bragg, NC",
    "Fort Liberty (Fort Bragg), NC": "Fort Bragg, NC",
    "Fort Liberty (Ft Bragg, NC)": "Fort Bragg, NC",
    "Fort Cavazos, TX": "Fort Hood, TX",
    "Fort Cavazos (Fort Hood), TX": "Fort Hood, TX",
    "Fort Eisenhower, GA": "Fort Gordon, GA",
    "Fort Benning, GA": "Fort Moore, GA",
}

DEFAULT_INSTALLATION = InstallationProfile(
    key="generic",
    display_name="Your gaining installation",
    short_name="gaining installation",
    legacy_name="",
    city="",
    state="",
    zip_code="",
    latitude=0.0,
    longitude=0.0,
    nearby_zip_codes=(),
    bah_rates=_BAH_BRAGG,
    housing=HousingMarket(
        on_post_pros=(
            "Simplifies housing cost math — often zero out-of-pocket rent",
            "Short commute and built-in community",
        ),
        on_post_cons=(
            "Availability depends on waitlists and bedroom count",
            "Less flexibility on floor plan and location",
        ),
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
}


def build_move_context(current_label: str, gaining_label: str) -> dict:
    """Return move-distance context for DITY/TLE planning."""
    current = INSTALLATION_ALIASES.get(current_label, current_label)
    gaining = INSTALLATION_ALIASES.get(gaining_label, gaining_label)
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
    canonical = INSTALLATION_ALIASES.get(gaining_label, gaining_label)
    return INSTALLATIONS.get(canonical, DEFAULT_INSTALLATION)


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
    return {
        "installation": profile.display_name,
        "short_name": profile.short_name,
        "legacy_name": profile.legacy_name,
        "location": {
            "city": profile.city,
            "state": profile.state,
            "zip_code": profile.zip_code,
            "latitude": profile.latitude,
            "longitude": profile.longitude,
            "nearby_zip_codes": list(profile.nearby_zip_codes),
        },
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
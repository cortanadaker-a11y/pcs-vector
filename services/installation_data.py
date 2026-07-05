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
    bah_rates: dict[str, int]
    housing: HousingMarket
    school_districts: tuple[str, ...]
    spouse_employment_notes: tuple[str, ...]
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

INSTALLATIONS: dict[str, InstallationProfile] = {
    "Fort Bragg, NC": InstallationProfile(
        key="bragg",
        display_name="Fort Bragg, NC",
        short_name="Fort Bragg",
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
                "Hope Mills & Spring Lake — strong BAH value, 15–25 min commute",
                "Fayetteville (north side) — more inventory, watch school zones",
                "Raeford — quieter, longer commute, often lower rent",
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
            "NC teaching license reciprocity available — start licensure packet early",
        ),
        climate_note="Mild winters; summer humidity drives higher AC costs off-post.",
        commute_hotspots=("All-American Fwy", "Bragg Blvd", "Murchison Rd gate"),
    ),
    "Fort Hood, TX": InstallationProfile(
        key="hood",
        display_name="Fort Hood, TX",
        short_name="Fort Hood",
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
                "Killeen (east side) — most inventory, verify school zones",
                "Harker Heights — family-friendly, 10–20 min to main gates",
                "Copperas Cove — quieter, strong BAH value, 15–25 min commute",
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
            "Remote work viable with good broadband in Harker Heights / Copperas Cove",
        ),
        climate_note="Hot summers drive higher AC costs off-post; mild winters rarely spike heating bills.",
        commute_hotspots=("US-190", "Trimmier Rd", "Clear Creek Rd gate"),
    ),
}

DEFAULT_INSTALLATION = InstallationProfile(
    key="generic",
    display_name="Your gaining installation",
    short_name="gaining installation",
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
    climate_note="Local weather affects utility costs and commute reliability.",
    commute_hotspots=("Main gate corridors at peak duty hours",),
)


def resolve_installation(gaining_label: str) -> InstallationProfile:
    """Return installation profile from form gaining-installation value."""
    return INSTALLATIONS.get(gaining_label, DEFAULT_INSTALLATION)


def get_bah_estimate(pay_grade: str, profile: InstallationProfile) -> int:
    """Return estimated monthly BAH with dependents."""
    return profile.bah_rates.get(pay_grade, profile.bah_rates.get("E-5", 1600))


def build_installation_context(profile: InstallationProfile, pay_grade: str) -> dict:
    """Serialize installation reference data for the Grok prompt."""
    bah = get_bah_estimate(pay_grade, profile)
    rent_low, rent_high = profile.housing.avg_3br_rent_range
    return {
        "installation": profile.display_name,
        "short_name": profile.short_name,
        "estimated_bah_with_dependents_usd": bah,
        "typical_3br_rent_range_usd": {"low": rent_low, "high": rent_high},
        "bah_surplus_if_rent_at_low": bah - rent_low,
        "bah_gap_if_rent_at_high": bah - rent_high,
        "on_post_pros": list(profile.housing.on_post_pros),
        "on_post_cons": list(profile.housing.on_post_cons),
        "off_post_areas_to_research": list(profile.housing.off_post_areas),
        "utility_note": profile.housing.utility_note,
        "school_districts": list(profile.school_districts),
        "spouse_employment_leads": list(profile.spouse_employment_notes),
        "climate_and_cost_note": profile.climate_note,
        "commute_hotspots": list(profile.commute_hotspots),
    }
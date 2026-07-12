"""Decision-grade synthesis — recommendations, spouse fast-tracks, risk chains."""

from __future__ import annotations

from typing import Any

from services.installation_data import InstallationProfile

# Week-by-week spouse employment fast-tracks keyed by installation + career field.
SPOUSE_FAST_TRACK: dict[str, dict[str, dict[str, Any]]] = {
    "Fort Bragg, NC": {
        "Federal / government civilian": {
            "critical_path": "USAJOBS referral preservation → MSEP flag → interview pipeline",
            "week_0_1": "Confirm USAJOBS referral status; notify HR of PCS orders; register MSEP.",
            "week_2_3": "Apply to Fort Bragg and Cumberland County federal roles; parallel NAF backup.",
            "week_4_6": "Interviews timed to on-post housing or short commute off-post.",
            "week_6_10": "Federal offer or NAF bridge role — 8–14 week pipeline typical.",
            "fastest_paycheck_path": "NAF admin role — 4–6 weeks while federal pipeline runs",
            "leverage_programs": ["MSEP", "Hiring Our Heroes", "ACS Employment Readiness"],
            "bottleneck": "Federal hiring freeze or lost referral — NAF is the income bridge, not optional.",
            "what_this_means": (
                "A 30-day PCS does not pause federal timelines — you must protect the referral "
                "from losing station while locking on-post housing to shorten the commute variable."
            ),
        },
        "K-12 education / teaching": {
            "critical_path": (
                "NC licensure packet → Cumberland lateral-entry → substitute pool → full contract"
            ),
            "week_0_1": (
                "Submit NC DPI reciprocity packet and Cumberland County lateral-entry application "
                "from losing station; register MyCAA same day (up to $4,000 for certs/fingerprinting)."
            ),
            "week_2_3": (
                "Complete fingerprinting and background check; apply to substitute pool — "
                "clearance typically 10–14 days, faster than full licensure."
            ),
            "week_4_6": (
                "Substitute days ($120–150/day) generate bridge income while lateral-entry processes; "
                "MSEP flags applications at Cumberland County HR."
            ),
            "week_6_10": (
                "First full contract paycheck if lateral-entry interview landed during May–July window; "
                "miss mid-August cutoff and you start the year as day-to-day sub only."
            ),
            "fastest_paycheck_path": "Substitute pool — first paid day possible in 2–3 weeks post-arrival",
            "leverage_programs": [
                "MyCAA — licensure and certification reimbursement",
                "MSEP — hiring preference at Cumberland County Schools",
                "Hiring Our Heroes — fellowship and corporate bridge roles",
                "ACS Employment Readiness — resume tailoring and interview scheduling",
            ],
            "bottleneck": (
                "NC licensure (4–8 weeks) gates full contracts; substitute is the income bridge "
                "but requires childcare coverage first."
            ),
            "what_this_means": (
                "Your spouse cannot wait for a full license before earning — the winning sequence is "
                "substitute pool + lateral-entry in parallel, not serial job applications after arrival."
            ),
        },
        "Healthcare / nursing": {
            "critical_path": "NC board endorsement → temp permit → Cape Fear Valley or Womack NAF",
            "week_0_1": "Submit NC endorsement packet; apply Cape Fear Valley and Womack NAF via MSEP.",
            "week_2_3": "Pursue temporary permit; NAF roles onboard faster than civilian hospital.",
            "week_4_6": "First paycheck likely from NAF or temp-permit clinical role.",
            "week_6_10": "Full endorsement clears; transition to permanent role.",
            "fastest_paycheck_path": "NAF health clinic — 4–6 weeks with MSEP preference",
            "leverage_programs": ["MSEP", "MyCAA for CEUs", "ACS Spouse Employment"],
            "bottleneck": "Board endorsement without temp permit = 6–8 week income gap.",
            "what_this_means": (
                "NAF is not a consolation prize — it is the fastest paycheck while civilian "
                "endorsement processes."
            ),
        },
    },
    "Fort Benning, GA": {
        "Student / continuing education": {
            "critical_path": "MyCAA registration → on-post housing with strong internet → quiet study window",
            "week_0_1": "Register MyCAA; apply on-post housing; verify master's program bandwidth requirements.",
            "week_2_3": "If off-post required, test ISP speeds at lease addresses; set up dedicated study space.",
            "week_4_6": "Stabilize routine — EFMP and school zoning must not disrupt study blocks.",
            "week_6_10": "Confirm therapy and IEP continuity so spouse can protect semester deadlines.",
            "fastest_paycheck_path": "N/A — focus is program continuity, not employment income",
            "leverage_programs": ["MyCAA for certification costs", "ACS Family Advocacy", "EFMP Family Support"],
            "bottleneck": "EFMP transfer delay or weak on-post internet forces off-post hunt that breaks study routine.",
            "what_this_means": (
                "This PCS is about protecting your spouse's semester and therapy schedule — "
                "housing choice is a study-environment decision, not just a commute calculation."
            ),
        },
    },
    "Fort Hood, TX": {
        "Remote / work-from-home professional": {
            "critical_path": "Zip-code fiber verification → lease with ISP install date → hotspot backup",
            "week_0_1": "Verify 200+ Mbps at target addresses in Harker Heights/Copperas Cove.",
            "week_2_3": "Schedule ISP install for day of lease start; activate mobile hotspot before departure.",
            "week_4_6": "Remote income uninterrupted if fiber live by day 7.",
            "week_6_10": "Stabilize; audit first electric bill against BAH assumptions.",
            "fastest_paycheck_path": "Remote role — 1–2 weeks if connectivity confirmed pre-arrival",
            "leverage_programs": ["ACS Employment Readiness", "MSEP at CRDAMC/Killeen ISD as backup"],
            "bottleneck": "ISP install delays of 5–10 days without pre-scheduling.",
            "what_this_means": (
                "Your PCS critical path is internet activation, not job applications — "
                "treat fiber confirmation like a reporting-date requirement."
            ),
        },
    },
    "Fort Campbell, KY": {
        "Trades / skilled labor": {
            "critical_path": "TN/KY license check → contractor pipeline → first paid job",
            "week_0_1": "Verify TN or KY trade license reciprocity; register with ACS and local contractor registries.",
            "week_2_3": "Apply to Clarksville-area contractors and on-post DPW subcontractor lists via MSEP.",
            "week_4_6": "First paid job likely from service/retail bridge if contractor pipeline slow.",
            "week_6_10": "Steady trades income if licensure and childcare locked in parallel.",
            "fastest_paycheck_path": "Retail/service bridge — 2–4 weeks while contractor paperwork clears",
            "leverage_programs": ["ACS Employment Readiness", "MSEP", "MyCAA for trade certifications"],
            "bottleneck": "KY/TN line affects license jurisdiction — wrong state filing adds 2–4 weeks.",
            "what_this_means": (
                "School zoning and gate commute pick your neighborhood — trades income follows "
                "where you can reliably get to job sites without burning 90 minutes on Madam Walker."
            ),
        },
    },
    "Joint Base Lewis-McChord, WA": {
        "Healthcare / nursing": {
            "critical_path": "WA endorsement → temp permit → Madigan NAF or MultiCare",
            "week_0_1": "Submit WA endorsement packet from losing station; apply Madigan NAF and MultiCare via MSEP.",
            "week_2_3": "Pursue temporary permit; NAF roles onboard faster than civilian hospital.",
            "week_4_6": "First paycheck from NAF or temp-permit clinical role if childcare locked.",
            "week_6_10": "Full endorsement clears; reassess commute after first rain-season month.",
            "fastest_paycheck_path": "Madigan NAF with Military Spouse Preference — 4–6 weeks",
            "leverage_programs": ["MSEP at Madigan", "MyCAA for CEUs", "ACS Spouse Employment"],
            "bottleneck": "Tight rental market + CDC wait — spouse cannot interview far from locked housing.",
            "what_this_means": (
                "Housing and licensure are the same decision — a lease in Yelm to save rent "
                "can cost six weeks of nursing income if Madigan commute fails in rain."
            ),
        },
    },
    "Fort Sill, OK": {
        "Retail / hospitality / service": {
            "critical_path": "Childcare lock → part-time bridge → full schedule",
            "week_0_1": "Submit DD 2606; scout FCC in Lawton west; spouse applies to Lawton retail hubs.",
            "week_2_3": "Part-time shifts at restaurants/retail while CDC slot processes.",
            "week_4_6": "Expand hours once infant FCC coverage confirmed.",
            "week_6_10": "Full schedule if childcare stable; audit tornado shelter in lease.",
            "fastest_paycheck_path": "Part-time retail/hospitality — 2–3 weeks with flexible shifts",
            "leverage_programs": ["ACS Employment Readiness", "MSEP at Comanche County Memorial"],
            "bottleneck": "Infant CDC wait without FCC bridge blocks any spouse work outside the home.",
            "what_this_means": (
                "Your fastest resettlement is childcare-first — spouse income is a bonus that "
                "only works once the infant has a seat, not before."
            ),
        },
    },
    "Fort Drum, NY": {
        "Healthcare / nursing": {
            "critical_path": "NY endorsement → temp permit → Samaritan or NAF clinic",
            "week_0_1": "Submit NY endorsement; apply Samaritan and Fort Drum NAF before departure.",
            "week_2_3": "Temp permit application — 2–3 weeks typical.",
            "week_4_6": "First paycheck from NAF or temp-permit role.",
            "week_6_10": "Full endorsement; evaluate on-post vs off-post winter commute.",
            "fastest_paycheck_path": "NAF clinic with Military Spouse Preference — 4–6 weeks",
            "leverage_programs": ["MyCAA for CEUs", "ACS Spouse Employment", "MSEP at Samaritan"],
            "bottleneck": "CDC infant/toddler waitlist blocks spouse work without FCC bridge.",
            "what_this_means": (
                "Childcare and licensure run in parallel — delaying DD 2606 until in-processing "
                "adds 30+ days to an already tight winter PCS."
            ),
        },
    },
}

# Primary recommendation templates by priority + housing preference.
PRIMARY_STRATEGY: dict[str, str] = {
    "Spouse career / quick employment": (
        "Lock off-post in {zips} before arrival, run {dity_mode} DITY, and sequence spouse "
        "employment through the fast-track path — housing location directly controls interview "
        "access and school zoning."
    ),
    "Minimizing total costs": (
        "Prioritize {housing_path} to maximize BAH surplus or on-post savings, execute {dity_mode} DITY for "
        "move profit, and cap rent at the low end of market to protect 6-month surplus."
    ),
    "Fastest possible resettlement": (
        "Pre-apply housing and submit all spouse/childcare paperwork from losing station; "
        "parallelize Soldier in-processing with spouse licensure so nothing runs serially."
    ),
    "School quality": (
        "Verify school zoning in writing before lease signature in {zips}; housing choice "
        "is the enrollment decision — everything else follows the address."
    ),
}

RISK_CHAINS: dict[str, tuple[str, ...]] = {
    "Fort Bragg, NC": (
        "Licensure delay past day 21 → no substitute income → $3,600 four-week gap compounds with deposit/TLE",
        "Housing not locked by day 15 → miss mid-August school transfer window → children start year unplaced",
        "CDC paperwork delayed → spouse cannot accept substitute days → employment timeline slips 4+ weeks",
        "Wrong-side-of-gate commute → 0630–0800 rush burns interview windows → spouse loses hiring priority",
    ),
    "Fort Hood, TX": (
        "On-post waitlist assumed verbally → family hotels 3+ weeks → TLE exhausts before BAH starts",
        "Fiber not verified pre-lease → remote spouse offline 5–10 days → income gap despite 'no licensure' field",
        "Killeen vs Copperas Cove ISD zoning error → school reassignment mid-year",
    ),
    "Fort Drum, NY": (
        "DD 2606 submitted at in-processing → CDC wait extends 30+ days → spouse cannot work",
        "Off-post lease without snow clause → winter commute failures → missed shifts",
        "Endorsement without temp permit → 6–8 week income gap in high-cost winter market",
    ),
    "Fort Gordon, GA": (
        "Evans lease without Columbia County zoning confirmation → school denial at registration",
        "TAVT surprise at DMV → $300–800 month-one hit erodes BAH surplus",
    ),
    "Fort Campbell, KY": (
        "TN/KY school zoning error → high school transfer denied mid-year → IEP continuity breaks",
        "Madam Walker commute underestimated → spouse misses trades job-site windows",
        "IEP not registered with district before lease → special ed services delayed 30+ days",
    ),
    "Joint Base Lewis-McChord, WA": (
        "WA endorsement delayed → 6–8 week nursing income gap in high-rent market",
        "Lease signed without mold/ventilation check → sick-kid cycle burns TLE days",
        "DuPont inventory missed → forced to Yelm with 35-min rain commute → childcare mismatch",
    ),
    "Fort Sill, OK": (
        "Infant CDC wait without FCC → spouse cannot take retail bridge shifts",
        "Lease without tornado shelter disclosure → insurance gap after hail event",
        "Housing hunt past day 10 → TLE exhausts before BAH aligns with low Lawton rent",
    ),
    "Fort Benning, GA": (
        "EFMP transfer incomplete → on-post only option → spouse loses Columbus job market access",
        "Phenix City AL lease without GA school confirmation → enrollment denied",
        "Graduation-week traffic → missed EFMP appointments → medical continuity gap",
    ),
}

HOUSING_ALTERNATIVES: dict[str, tuple[str, str]] = {
    "Fort Bragg, NC": (
        "Raeford (28376) — lower rent, longer commute, quieter schools if Hope Mills inventory dries up",
        "On-post bridge (30 days max) — only if off-post lease fails; BAH absorbed, waitlist risk remains",
    ),
    "Fort Hood, TX": (
        "Copperas Cove (76522) — strongest BAH surplus if Killeen inventory tight",
        "On-post — predictable cost during summer AC spike; call housing day orders drop",
    ),
    "Fort Drum, NY": (
        "Evans Mills/Le Ray off-post — faster inventory than Watertown; budget winter heating",
        "On-post — snow removal included; best for toddler CDC proximity",
    ),
    "Fort Gordon, GA": (
        "Grovetown (30813) — more inventory than Evans; verify Columbia County zoning",
        "On-post — shorter commute; school bus routes vary by village",
    ),
    "Fort Campbell, KY": (
        "Hopkinsville, KY — lower rent, longer commute; verify Christian County schools for IEP",
        "On-post DODEA — strongest IEP continuity if off-post zoning fails",
    ),
    "Joint Base Lewis-McChord, WA": (
        "Yelm — lower rent, longer commute; good if Madigan NAF is the target employer",
        "On-post — eliminates rain commute variable; waitlist risk in summer PCS",
    ),
    "Fort Sill, OK": (
        "Cache — quieter, lower rent; verify tornado shelter in lease",
        "On-post — fastest CDC path for infants; BAH absorbed",
    ),
    "Fort Benning, GA": (
        "Columbus north (31909) — Muscogee schools and EFMP services strongest",
        "On-post — best EFMP continuity; limited floor-plan choice",
    ),
}


def build_spouse_fast_track(
    installation: str,
    spouse_career_field: str,
    cashflow: dict[str, Any],
) -> dict[str, Any] | None:
    """Return week-by-week spouse employment synthesis for the prompt."""
    track = SPOUSE_FAST_TRACK.get(installation, {}).get(spouse_career_field)
    if not track:
        weeks = cashflow.get("weeks_to_spouse_first_paycheck", {})
        return {
            "critical_path": f"Standard hiring timeline for {spouse_career_field}",
            "fastest_paycheck_path": f"{weeks.get('low', 4)}–{weeks.get('high', 8)} weeks typical",
            "four_week_delay_cost_usd": cashflow.get("four_week_delay_cost_usd"),
            "what_this_means": (
                "Treat spouse employment as a sequenced operation, not a post-arrival errand — "
                "every week of delay has a dollar cost."
            ),
        }
    enriched = dict(track)
    enriched["weeks_to_first_paycheck"] = cashflow.get("weeks_to_spouse_first_paycheck")
    enriched["four_week_delay_cost_usd"] = cashflow.get("four_week_delay_cost_usd")
    enriched["estimated_income_gap_usd"] = cashflow.get("estimated_spouse_income_gap_usd")
    return enriched


def build_decision_context(
    *,
    profile: InstallationProfile,
    spouse_career_field: str,
    primary_priority: str,
    housing_preference: str,
    cashflow: dict[str, Any],
    dity_ctx: dict[str, Any],
    family_name: str,
    gaining: str,
) -> dict[str, Any]:
    """Assemble decision-grade synthesis block for Grok."""
    # Pull target zips from off-post area names (e.g. "Hope Mills (28348) & Spring Lake (28390)").
    import re

    zips_parts: list[str] = []
    for area in profile.housing.off_post_areas[:2]:
        zips_parts.extend(re.findall(r"\((\d{5})\)", area))
    # Deduplicate while preserving order.
    seen: set[str] = set()
    ordered = [z for z in zips_parts if not (z in seen or seen.add(z))]  # type: ignore[func-returns-value]
    zips = "/".join(ordered[:3]) if ordered else profile.zip_code
    dity_mode = dity_ctx.get("recommended_mode", "partial") if dity_ctx.get("applicable") else "government"
    housing_path = (
        "on-post assignment"
        if "On-post" in housing_preference
        else f"off-post in {profile.housing.off_post_areas[0].split('—')[0].strip()}"
    )

    strategy_template = PRIMARY_STRATEGY.get(
        primary_priority,
        PRIMARY_STRATEGY["Spouse career / quick employment"],
    )
    primary_rec = strategy_template.format(
        zips=zips,
        dity_mode=dity_mode,
        housing_path=housing_path,
    )

    alts = HOUSING_ALTERNATIVES.get(profile.display_name, ())
    risks = list(RISK_CHAINS.get(profile.display_name, ()))
    biggest_risk = risks[0] if risks else (
        f"Spouse income gap of ~${cashflow.get('estimated_spouse_income_gap_usd', 0):,} "
        f"colliding with move deposits before first paycheck"
    )

    fast_track = build_spouse_fast_track(profile.display_name, spouse_career_field, cashflow)

    return {
        "primary_recommendation": primary_rec,
        "ranked_alternatives": list(alts[:2]),
        "biggest_risk_or_dependency": biggest_risk,
        "risk_chain": risks,
        "spouse_fast_track": fast_track,
        "synthesis_directive": (
            f"For {family_name or 'this family'}: connect every section to "
            f"{primary_priority.lower()} — explain what each choice means in dollars and weeks, "
            f"not just what to do."
        ),
        "nco_opener": (
            f"I would run this PCS as a {primary_priority.lower()} operation — "
            f"everything else is supporting effort."
        ),
    }
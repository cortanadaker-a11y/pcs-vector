"""Rank- and installation-aware insights for soldier-facing report sections."""

from __future__ import annotations

from typing import Any

from services.installation_data import InstallationProfile

# Per-installation soldier-facing gotchas (not generic checklist items).
INSTALLATION_SOLDIER_INSIGHTS: dict[str, tuple[str, ...]] = {
    "Fort Bragg, NC": (
        "Hope Mills/Spring Lake inventory turns in 7–10 days during summer PCS — pre-apply rentals from losing station.",
        "Cumberland County Schools hiring peaks May–July; lateral-entry packets submitted before arrival get interview priority.",
        "All-American Fwy gate rush 0630–0800 — if spouse interviews off-post, schedule after 0900.",
        "ACS Relocation Readiness at Soldier Support Center is the fastest path to current CDC/FCC wait times.",
    ),
    "Fort Hood, TX": (
        "On-post housing waitlist spikes May–August — call housing office the day orders drop, not after arrival.",
        "Copperas Cove (76522) offers strongest BAH surplus; verify Killeen ISD vs Copperas Cove ISD zoning before lease.",
        "Summer AC bills off-post routinely hit $250+ — on-post removes that variable during high-tempo cycles.",
        "CRDAMC and Killeen ISD are MSEP partners — spouse applications get hiring preference flags.",
    ),
    "Fort Drum, NY": (
        "Winter PCS arrivals face lake-effect closures on Route 11 — build 30-min commute buffer Oct–Apr.",
        "Indian River Central is the default military-family school district; verify bus routes by on-post village.",
        "On-post snow removal is included; off-post winter heating can erase $200–350/mo of BAH surplus.",
        "CDC infant/toddler waitlists are the gating item — submit DD 2606 before departure, not at in-processing.",
    ),
    "Fort Gordon, GA": (
        "Columbia County (Evans/Grovetown) schools are top choice but zoning is strict — confirm address before lease.",
        "Cyber corridor hiring runs year-round; AU Health and defense contractors post roles on rolling 2-week cycles.",
        "Gate 1 and Gordon Hwy are peak chokepoints — off-post in Evans adds 15–20 min but better school ratings.",
        "GA TAVT vehicle tax hits new residents — budget $300–800 at registration depending on vehicle value.",
    ),
}

SCHOOL_ENROLLMENT_NOTES: dict[str, str] = {
    "Fort Bragg, NC": (
        "Cumberland County: register within 10 school days of establishing residency; "
        "summer transfer window closes mid-August for fall placement."
    ),
    "Fort Hood, TX": (
        "Killeen ISD: online pre-enrollment opens 3–4 weeks before start; "
        "proof of residency (lease + utility) required before class assignment."
    ),
    "Fort Drum, NY": (
        "Indian River Central: contact district registrar before arrival for military transfer packet; "
        "winter weather can delay bus-route confirmation — allow 5 extra days."
    ),
    "Fort Gordon, GA": (
        "Columbia County Schools: enrollment requires lease + 2 proof-of-residency documents; "
        "high-demand schools in Evans fill by early August."
    ),
}


CHILD_AGE_INSIGHTS: dict[str, str] = {
    "0–4 years": (
        "CDC/FCC is the gating item — school enrollment is not yet the bottleneck; "
        "prioritize childcare slot before housing aesthetics."
    ),
    "5–8 years": (
        "Elementary zoning verification is non-negotiable before lease signing; "
        "after-school care fills fast in July."
    ),
    "9–12 years": (
        "Middle-school zoning shifts more than elementary; confirm bus routes "
        "if living off-post beyond 15 minutes from gate."
    ),
    "13–17 years": (
        "High-school transfers may require course-credit review; contact registrar "
        "before arrival to avoid schedule gaps."
    ),
}

NEGOTIATION_TIPS: dict[str, str] = {
    "Fort Bragg, NC": "Ask for military clause (30-day orders termination) and cap pet deposit at one month's rent.",
    "Fort Hood, TX": "Request July/August utility cap or average-billing — summer AC spikes are negotiable in Copperas Cove.",
    "Fort Drum, NY": "Negotiate snow-removal clause off-post; on-post avoids this entirely.",
    "Fort Gordon, GA": "Ask for TAVT reimbursement awareness in lease — some landlords discount first month for military PCS.",
}


def build_child_context(child_age_ranges: list[str]) -> list[str]:
    """Return age-specific insights for sections 2 and 6."""
    return [
        CHILD_AGE_INSIGHTS[age]
        for age in child_age_ranges
        if age in CHILD_AGE_INSIGHTS
    ]


def build_soldier_context(
    profile: InstallationProfile,
    pay_grade: str,
    *,
    num_children: int,
    primary_priority: str,
) -> dict[str, Any]:
    """Assemble soldier-facing insight block for the Grok prompt."""
    insights = list(INSTALLATION_SOLDIER_INSIGHTS.get(profile.display_name, ()))
    school_note = SCHOOL_ENROLLMENT_NOTES.get(profile.display_name)

    is_field_grade = pay_grade in ("O-4", "O-5", "O-6", "O-7+", "E-8", "E-9")
    rank_note = (
        "Field-grade families often get faster on-post housing consideration — "
        "still submit DD 2606 and housing apps the day orders drop."
        if is_field_grade
        else "Junior NCO timeline is unforgiving — housing and finance are day-1 stops; "
        "do not house-hunt before in-processing clears TLE and BAH start date."
    )

    command_line = _command_briefing_line(primary_priority, profile.short_name, pay_grade)

    return {
        "installation_insights": insights,
        "school_enrollment_note": school_note if num_children > 0 else None,
        "negotiation_tip": NEGOTIATION_TIPS.get(profile.display_name),
        "rank_context_note": rank_note,
        "command_briefing_prompt": command_line,
    }


def _command_briefing_line(priority: str, short_name: str, pay_grade: str) -> str:
    """Template for the one-line commander conversation."""
    if "Spouse career" in priority:
        return (
            f"Commander brief: 'We are executing a {short_name} PCS with spouse employment "
            f"as the critical path — requesting {pay_grade} reporting flexibility only if "
            f"licensure/childcare slips past day 21.'"
        )
    if "Minimizing total costs" in priority:
        return (
            f"Commander brief: 'Move is cost-optimized via on-post/TLE/DITY sequencing — "
            f"no forecast impact to readiness; will confirm housing lock by day 10.'"
        )
    if "Fastest" in priority:
        return (
            f"Commander brief: 'Reporting on time; parallel-tracking housing and in-processing "
            f"to minimize family disruption — housing decision by day 7.'"
        )
    return (
        f"Commander brief: 'PCS plan locked for {short_name} — primary risk is housing/childcare "
        f"timing; mitigation in place before reporting date.'"
    )
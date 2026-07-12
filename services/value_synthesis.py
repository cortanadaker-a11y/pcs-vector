"""Value scorecard and synthesis — why this report beats a free checklist."""

from __future__ import annotations

from typing import Any


WALK_AWAY_RED_FLAGS: dict[str, tuple[str, ...]] = {
    "Fort Bragg, NC": (
        "Lease in Harnett County without written school-zone confirmation from Cumberland County registrar.",
        "Landlord refuses military clause or demands 12-month minimum with no PCS termination.",
        "Property on All-American Fwy side with 35+ min gate commute during peak — burns spouse interview windows.",
    ),
    "Fort Hood, TX": (
        "Off-post lease in Killeen east side without verifying Killeen ISD vs Copperas Cove ISD zoning.",
        "Rental without written utility-cap or average-billing — July/August bills can exceed $300.",
        "On-post waitlist 'estimated' verbally with no written position number from housing office.",
    ),
    "Fort Drum, NY": (
        "Off-post lease without snow-removal clause and no lake-effect commute buffer built in.",
        "Accepting Watertown rental for 'inventory' without calculating $200–350/mo winter heating erosion.",
        "Delaying DD 2606 until in-processing — summer surge adds 30+ days to CDC wait.",
    ),
    "Fort Gordon, GA": (
        "Signing Evans/Grovetown lease without Columbia County school zoning confirmation in writing.",
        "Ignoring GA TAVT vehicle tax at registration — surprise $300–800 hit in month one.",
        "Choosing west Augusta for inventory without testing Gordon Hwy gate commute at 0630.",
    ),
}

SPOUSE_SALARY_RANGES: dict[str, dict[str, str]] = {
    "Fort Bragg, NC": {
        "K-12 education / teaching": "$42K–$58K/yr (Cumberland County Schools; substitutes $120–150/day)",
        "Healthcare / nursing": "$58K–$78K/yr (Cape Fear Valley Health; NAF roles lower but faster)",
        "Remote / work-from-home professional": "No local cap — verify 200+ Mbps in 28348/28390",
    },
    "Fort Hood, TX": {
        "K-12 education / teaching": "$45K–$55K/yr (Killeen ISD; hiring peaks June–August)",
        "Healthcare / nursing": "$55K–$72K/yr (CRDAMC; traveler contracts higher short-term)",
        "Remote / work-from-home professional": "No local cap — Harker Heights/Copperas Cove fiber reliable",
    },
    "Fort Drum, NY": {
        "Healthcare / nursing": "$62K–$82K/yr (Samaritan Medical Center; temp permit bridges gap)",
        "K-12 education / teaching": "$48K–$62K/yr (Jefferson County / Indian River corridor)",
    },
    "Fort Gordon, GA": {
        "K-12 education / teaching": "$46K–$58K/yr (Columbia County Schools — competitive)",
        "Healthcare / nursing": "$56K–$74K/yr (AU Health; cyber corridor less relevant for nursing)",
        "Remote / work-from-home professional": "Strong in Evans/Grovetown — defense contractor spillover",
    },
}

GENERIC_CHECKLIST_GAPS: dict[str, str] = {
    "Spouse career / quick employment": (
        "Free checklists say 'apply for jobs.' This plan sequences licensure, substitute fast-path, "
        "and childcare so the spouse can actually accept an offer."
    ),
    "Minimizing total costs": (
        "Free checklists compare rent to BAH once. This plan models 6-month surplus, winter utilities, "
        "DITY net, and on-post absorption together."
    ),
    "Fastest possible resettlement": (
        "Free checklists list in-processing steps. This plan gates housing, internet, and TLE "
        "so nothing runs serially when it can run parallel."
    ),
    "School quality": (
        "Free checklists say 'research schools.' This plan ties zoning to lease address "
        "and enrollment deadlines to your move window."
    ),
}


def build_situation_snapshot(
    *,
    family_name: str,
    rank: str,
    current: str,
    gaining: str,
    spouse_career: str,
    num_children: int,
    primary_priority: str,
    move_window: str,
) -> str:
    """Three-sentence personalized opener for section 1."""
    who = family_name or "This family"
    kids = (
        f"{num_children} child(ren) requiring school/childcare sequencing"
        if num_children
        else "no dependents in school/childcare"
    )
    return (
        f"{who} ({rank}) is executing a {current} → {gaining} PCS within {move_window}, "
        f"with a spouse in {spouse_career} and {kids}. "
        f"The critical path is **{primary_priority.lower()}** — every recommendation below "
        f"serves that priority, not a generic PCS checklist. "
        f"This plan is built for decisions you cannot Google in one search."
    )


NINETY_DAY_WATCH: dict[str, tuple[str, ...]] = {
    "Fort Bragg, NC": (
        "Day 45: Confirm spouse has substitute or full contract — if not, escalate licensure packet.",
        "Day 60: Reconcile summer utility bills against BAH surplus assumptions.",
        "Day 90: If still on FCC bridge, re-submit CDC or negotiate after-school care for school year.",
    ),
    "Fort Hood, TX": (
        "Day 45: Verify on-post assignment stable or off-post lease renewal terms.",
        "Day 60: Audit first two electric bills — if >$250, reassess housing path.",
        "Day 90: Confirm spouse remote/income stream uninterrupted; test backup internet.",
    ),
    "Fort Drum, NY": (
        "Day 45: Winter heating bills arrive — compare on-post vs off-post cost assumptions.",
        "Day 60: CDC/FCC status check — if no slot, activate spouse remote or NAF bridge.",
        "Day 90: Route 11 commute stress test in first snow event — adjust if needed.",
    ),
    "Fort Gordon, GA": (
        "Day 45: School enrollment confirmed and bus route validated.",
        "Day 60: Spouse job pipeline check — cyber/healthcare hiring cycles move fast here.",
        "Day 90: TAVT/vehicle registration complete; no DMV penalties.",
    ),
}

EMPLOYER_TARGETS: dict[str, dict[str, list[str]]] = {
    "Fort Bragg, NC": {
        "K-12 education / teaching": [
            "Cumberland County Schools (HR — lateral entry & substitute)",
            "Cape Fear Valley Health (education-adjacent roles)",
        ],
        "Healthcare / nursing": ["Cape Fear Valley Health", "Womack Army Medical Center NAF"],
    },
    "Fort Hood, TX": {
        "Remote / work-from-home professional": ["N/A — verify fiber; backup: CRDAMC admin remote"],
        "Healthcare / nursing": ["Carl R. Darnall Army Medical Center", "Killeen ISD health aides"],
    },
    "Fort Drum, NY": {
        "Healthcare / nursing": ["Samaritan Medical Center", "Fort Drum NAF health clinic"],
    },
    "Fort Gordon, GA": {
        "Healthcare / nursing": ["AU Health", "Fort Eisenhower NAF"],
        "K-12 education / teaching": ["Columbia County Schools", "Richmond County Schools"],
    },
}


def _primary_path_monthly_value(
    *,
    bah_monthly: int,
    rent_low: int,
    housing_preference: str,
) -> tuple[int, str]:
    """Monthly dollar advantage of the recommended housing path."""
    if "On-post" in housing_preference:
        saved = rent_low
        return saved, f"on-post avoids ~${rent_low:,}/mo off-post rent at the low end"
    surplus = max(bah_monthly - rent_low, 0)
    return surplus, f"off-post at low-end rent yields ${surplus:,}/mo BAH surplus"


def build_value_scorecard(
    *,
    bah_monthly: int,
    rent_low: int,
    rent_high: int,
    housing_preference: str,
    months: int,
    dity_net: int,
    primary_priority: str,
) -> dict[str, Any]:
    """Precompute 6-month upside vs wrong-default path."""
    monthly_value, value_note = _primary_path_monthly_value(
        bah_monthly=bah_monthly,
        rent_low=rent_low,
        housing_preference=housing_preference,
    )
    six_month_value = monthly_value * months
    wrong_lease_cost = max(rent_high - bah_monthly, 0) * 3  # 3 months at over-BAH before breaking lease
    avoided_mistake = max(wrong_lease_cost, 800)

    total_upside = six_month_value + dity_net + avoided_mistake
    roi_multiple = round(total_upside / 25, 0)

    roi_note = (
        f"Following this plan's primary housing path yields ~${six_month_value:,} over {months} months "
        f"({value_note}), plus ~${dity_net:,} DITY net and ~${avoided_mistake:,} in avoided wrong-lease cost "
        f"— roughly **${total_upside:,} total {months}-month upside** vs a generic checklist "
        f"(~{int(roi_multiple)}x the $25 report cost)."
    )

    return {
        "planning_horizon_months": months,
        "monthly_value_usd": monthly_value,
        "six_month_value_usd": six_month_value,
        "value_note": value_note,
        "dity_net_included_usd": dity_net,
        "avoided_wrong_lease_cost_usd": avoided_mistake,
        "total_six_month_upside_usd": total_upside,
        "roi_statement": roi_note,
        "report_cost_usd": 25,
        "roi_multiple": int(roi_multiple),
        "generic_gap": GENERIC_CHECKLIST_GAPS.get(
            primary_priority,
            "Generic PCS lists do not connect your priorities to local bottlenecks and dollar math.",
        ),
    }


def build_value_context(
    *,
    installation: str,
    spouse_career_field: str,
    family_name: str,
    rank: str,
    current: str,
    gaining: str,
    num_children: int,
    primary_priority: str,
    move_window: str,
    housing_preference: str,
    bah_monthly: int,
    rent_low: int,
    rent_high: int,
    dity_net: int,
) -> dict[str, Any]:
    """Full value block for Grok prompt."""
    scorecard = build_value_scorecard(
        bah_monthly=bah_monthly,
        rent_low=rent_low,
        rent_high=rent_high,
        housing_preference=housing_preference,
        months=6,
        dity_net=dity_net,
        primary_priority=primary_priority,
    )
    salaries = SPOUSE_SALARY_RANGES.get(installation, {})
    employers = EMPLOYER_TARGETS.get(installation, {}).get(spouse_career_field, [])
    bad_default = (
        f"Without this plan: house-hunt on arrival, miss the {spouse_career_field.split('/')[0].strip().lower()} "
        f"hiring window, absorb a ${rent_high:,}/mo off-post mistake, and eat the full "
        f"${scorecard['avoided_wrong_lease_cost_usd']:,}+ wrong-lease cost before course-correcting."
    )
    spouse_share = (
        f"We're targeting {gaining} with a locked plan for {primary_priority.lower()} — "
        f"your job is {spouse_career_field.split('/')[0].strip().lower()} and mine is executing "
        f"the timeline in section 5 so we're not guessing."
    )
    return {
        "situation_snapshot": build_situation_snapshot(
            family_name=family_name,
            rank=rank,
            current=current,
            gaining=gaining,
            spouse_career=spouse_career_field,
            num_children=num_children,
            primary_priority=primary_priority,
            move_window=move_window,
        ),
        "value_scorecard": scorecard,
        "walk_away_red_flags": list(WALK_AWAY_RED_FLAGS.get(installation, ())),
        "ninety_day_watch": list(NINETY_DAY_WATCH.get(installation, ())),
        "top_employer_targets": employers,
        "local_salary_context": salaries.get(spouse_career_field),
        "why_not_free_checklist": scorecard["generic_gap"],
        "bad_default_path": bad_default,
        "spouse_share_line": spouse_share,
    }
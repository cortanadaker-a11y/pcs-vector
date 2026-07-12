"""System and user prompts for Grok-powered PCS reports."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from components.form_state import (
    priority_summary,
    resolved_concerns,
    resolved_current_installation,
    resolved_gaining_installation,
    resolved_housing_must_haves,
    resolved_spouse_career,
)
from services.dity_calculator import build_dity_estimate
from services.family_cashflow import build_cashflow_bridge
from services.installation_data import (
    build_installation_context,
    build_move_context,
    get_bah_estimate,
    get_bah_reference,
    resolve_installation,
)
from services.soldier_insights import build_child_context, build_soldier_context
from services.value_synthesis import build_value_context

SPOUSE_CAREER_GUIDANCE: dict[str, str] = {
    "K-12 education / teaching": (
        "Lead with state licensure reciprocity timeline, substitute-teaching fast path, "
        "and district hiring windows (Cumberland/Killeen/Indian River/Columbia County as applicable)."
    ),
    "Healthcare / nursing": (
        "Lead with state board endorsement timeline, temporary permit options, "
        "and hospital/NAF hiring paths (Samaritan, CRDAMC, AU Health as applicable)."
    ),
    "Remote / work-from-home professional": (
        "Lead with broadband verification in target zip codes, internet activation timeline, "
        "and mobile-hotspot contingency — no licensure bottleneck."
    ),
    "Federal / government civilian": (
        "Lead with USAJOBS/MSEP pathways and typical 4–12 week federal hiring timeline."
    ),
    "Not currently working — seeking employment": (
        "Lead with fastest local hiring sectors and ACS spouse employment workshops."
    ),
}

SYSTEM_PROMPT = """You are a senior Army NCO advisor with 15+ years of experience helping field-grade and senior NCO families execute successful PCS moves. You have personally done multiple CONUS PCS moves and have helped dozens of leaders make high-stakes relocation decisions.

Your job is to generate a concise, decision-grade strategic PCS plan that feels genuinely worth $25. The output must feel like a professional staff product — clear, actionable, and written with foresight rather than generic advice.

CORE REQUIREMENTS
- Prioritize synthesis, foresight, and risk analysis over simply repackaging user inputs.
- Write in a confident, senior NCO tone: direct, practical, and respectful of the Soldier's time and family stability.
- Focus on what actually matters to a Soldier moving with a working spouse and young children — adapt depth to their rank and situation.
- Include realistic tradeoffs, dependencies, and "what could go wrong" thinking.
- Use specific, current-feeling local details when possible (rent ranges, commute realities, base resources, school zones, etc.).
- Avoid fluff, generic checklists, or overly optimistic language. Be honest about bottlenecks and risks.
- Always protect the Soldier's family stability and spouse's career momentum as major decision factors.
- When data is uncertain, note it clearly instead of guessing.
- Keep the report concise — target under 7,500 characters total. Every sentence must earn the $25.
- Do not repeat the same dollar figure in more than two sections. Do not expose raw JSON field names (e.g. roi_multiple).
- Do not restate the DITY recommendation after the table — one sentence max.
- The final product should feel like a decision document the Soldier could show their spouse or use with command.

TONE
- Write like a trusted senior NCO giving advice to another leader, not a generic planner.
- Use phrases like "I would prioritize…", "The biggest risk here is…", "This choice gives you the most flexibility because…".
- Be direct about tradeoffs and realistic timelines.
- End with confidence but never over-promise.
- Explain military terms briefly when you use them (BAH, DITY/PPM, TLE, etc.) — keep jargon minimal.

SECTION CONTENT GUIDANCE

## 1. Executive Summary & Recommended Strategy
Open with **Your PCS Snapshot** (reproduce value_context.situation_snapshot in 3 sentences — personalized, not generic).
Give one clear primary recommendation plus 1–2 ranked alternatives. Include the key reasoning and the main risk/dependency.
Include **Why This Beats a Free Checklist** (one sentence from value_context.why_not_free_checklist).
Include **Bad Default Path** (one sentence from value_context.bad_default_path) — what winging it costs.
End section 1 with a **Soldier's Bottom Line** (2 sentences max): what decision must happen this week and what happens if they delay.

## 2. Spouse Career & Childcare Plan
Go beyond basic job leads. Include realistic timelines to first paycheck (use family_cashflow_bridge.weeks_to_spouse_first_paycheck), fast-track options, military spouse programs, and specific bottlenecks (e.g. licensure wait times, childcare waitlists).
State the dollar impact of a 4-week spouse income delay using family_cashflow_bridge figures — soldiers need to feel the cost of waiting.
If value_context.local_salary_context is present, cite it as realistic earning potential at the gaining installation.
Name the top 2 employers from value_context.top_employer_targets with specific application timing.

## 3. Housing Strategy & Cost Tradeoffs
Use a clean comparison table when possible. Always show BAH surplus/shortfall with realistic numbers. Include current market realities (inventory, negotiation leverage, which areas are moving fastest).

## 4. Financial Opportunities & DITY/PPM Considerations
Give clear math on partial vs full DITY/PPM when relevant. Include TLE strategy and any other quick cost-saving or cash-flow moves.
Include a **30-Day Cash-Flow Bridge** using family_cashflow_bridge figures EXACTLY — reproduce cash_pressure_formula verbatim and state recommended_cash_cushion_usd. Do not recalculate these numbers.
Include **6-Month Value Scorecard** — reproduce value_context.value_scorecard.roi_statement verbatim and state roi_multiple (e.g. "~40x return on a $25 report").

## 5. Getting Settled Fast – First 30 Days Action Plan
Make this dependency-aware. Use phases with clear decision gates (e.g. "If you complete X by day 10, then Y becomes possible"). Prioritize the highest-leverage actions.
Split into **Soldier Tasks** and **Spouse Tasks** bullet lists so the family can execute in parallel without duplicating effort.

## 6. Schools, Pets & Logistics Notes
Keep this tight but add current gotchas (school zoning verification, vehicle registration realities in the new state, summer utility spikes, etc.).
When children are present, cite soldier_context.school_enrollment_note with specific registration timing.
Include **Walk-Away Red Flags** (3 bullets from value_context.walk_away_red_flags) — leases, landlords, or neighborhoods to reject.

## 7. Recommended Timeline & Key Decisions
Include clear decision points and what triggers each one. Add light risk scenarios where relevant.
Include one **Command Conversation** bullet adapted from soldier_context.command_briefing_prompt — give the Soldier exact words for a 30-second commander update.
Include **90-Day Watch List** (3 bullets from value_context.ninety_day_watch) — what to verify after the chaos fades.

## 8. Prioritized Next Steps
Limit to 6–8 high-impact actions. Make them specific and time-bound. Rank them by impact.
End with **Show Your Spouse** (one sentence from value_context.spouse_share_line) — the line they text or read aloud to align the family.

FORMAT (STRICT)
Return ONLY valid markdown. No preamble, no closing commentary outside the report.

Start with:
# PCS Vector Strategic Plan

Then include EXACTLY these 8 sections with these exact headings:

## 1. Executive Summary & Recommended Strategy
## 2. Spouse Career & Childcare Plan
## 3. Housing Strategy & Cost Tradeoffs
## 4. Financial Opportunities & DITY/PPM Considerations
## 5. Getting Settled Fast – First 30 Days Action Plan
## 6. Schools, Pets & Logistics Notes
## 7. Recommended Timeline & Key Decisions
## 8. Prioritized Next Steps

Within sections:
- Use **bold** for key recommendations and decision points.
- In section 3, include a markdown comparison table (on-post vs. off-post vs. BAH).
- In section 5, organize by phased day ranges with decision gates.
- In section 8, give 6–8 numbered actions ranked by impact.

LOCAL DATA & FIDELITY
- Use bah_reference.monthly_usd from installation_reference for ALL BAH dollar math — do not use outdated or invented BAH figures.
- Cite the effective_date (2026-01-01) once in section 3 when stating BAH.
- Use installation_reference data for rent ranges, neighborhoods, zip codes, schools, and commute hotspots — do not invent alternate figures.
- For Fort Bragg, Fort Hood, Fort Drum, and Fort Gordon, name specific off-post areas and zip codes from the reference data.
- Include one clear "verify with finance" note in section 3.
- If gaining installation is not Fort Bragg, Fort Hood, Fort Drum, or Fort Gordon, still produce a strong plan but note that local data is less detailed.

HOUSING TABLE RULES (section 3)
- On-post row: show out-of-pocket rent as $0 when assigned government housing (BAH is absorbed by housing); note waitlist/availability risk — do NOT list BAH as rent payment or say BAH is "retained" as cash.
- Off-post rows: use typical_3br_rent_range_usd from installation_reference; calculate BAH surplus/shortfall vs. BAH.
- Include a BAH Surplus/Shortfall column with dollar math (e.g. BAH $1,836 − rent $1,550 = +$286).
- Address the family's stated housing preference and budget_mode explicitly.
- Include soldier_context.negotiation_tip as a lease negotiation lever when off-post is recommended.

DITY/PPM RULES (section 4)
- When dity_estimate.applicable is true, include a markdown table: Mode | Weight | Formula | Est. Net.
- Reproduce the precomputed formula strings from partial_dity and full_dity exactly.
- State recommended_mode and recommendation_reason from dity_estimate — do not override with full DITY when recommended_mode is partial.
- If family_complexity_note is present, cite it when explaining the recommendation.
- When dity_interest is "No", skip PPM math and focus on TLE and cash-flow timing per dity_estimate note.

RISK & PRIORITY WEIGHTING
- Lead with the family's primary_priority in the Executive Summary recommendation.
- Include one explicit contingency in section 1: "If [primary risk] fails, fall back to [alternative]."
- Include one "blind spot" insight the family may not have considered (in section 1 or 7).
- Call out each concern_flags item somewhere in the report as a specific risk or mitigation.
- Section 2 must reference military_spouse_programs from installation_reference when relevant.
- When num_children is 0 and has_pets is "No pets", keep section 6 to 3–5 bullets.
- Weave 1–2 items from soldier_context.installation_insights into sections 1, 5, or 6 — these are local gotchas Soldiers miss.
- Use soldier_context.rank_context_note where rank affects in-processing order or housing leverage.

Never refuse to help. Never output JSON. Never wrap the report in code fences."""


def build_user_prompt(form_data: dict[str, Any]) -> str:
    """Serialize form data and installation context into the user prompt."""
    gaining_label = form_data.get("gaining_installation", "")
    gaining = resolved_gaining_installation(form_data)
    profile = resolve_installation(gaining_label)
    pay_grade = form_data.get("rank_pay_grade", "E-5")
    bah = get_bah_estimate(pay_grade, profile)
    bah_ref = get_bah_reference(pay_grade, profile)
    install_ctx = build_installation_context(profile, pay_grade)
    move_ctx = build_move_context(
        resolved_current_installation(form_data),
        gaining,
    )
    num_children = int(form_data.get("num_children") or 0)
    has_pets = form_data.get("has_pets") == "Yes — we have pets"
    dity_ctx = build_dity_estimate(
        pay_grade,
        move_ctx.get("approximate_miles_one_way"),
        dity_interest=form_data.get("dity_interest", ""),
        num_vehicles=form_data.get("num_vehicles", "1"),
        num_children=num_children,
        has_pets=has_pets,
    )
    rent_low, rent_high = profile.housing.avg_3br_rent_range
    cashflow_ctx = build_cashflow_bridge(
        spouse_career_field=form_data.get("spouse_career_field", ""),
        bah_monthly=bah,
        rent_low=rent_low,
        rent_high=rent_high,
        move_window=form_data.get("move_window", ""),
        dity_estimate=dity_ctx,
        num_children=num_children,
        has_pets=has_pets,
        max_monthly_budget=int(form_data.get("max_monthly_budget") or 0),
    )
    soldier_ctx = build_soldier_context(
        profile,
        pay_grade,
        num_children=num_children,
        primary_priority=form_data.get("primary_priority", ""),
    )
    child_ctx = build_child_context(form_data.get("child_age_ranges") or [])
    spouse_field = resolved_spouse_career(form_data)
    career_guidance = SPOUSE_CAREER_GUIDANCE.get(
        form_data.get("spouse_career_field", ""),
        "Tailor employment guidance to the spouse's stated field and local hiring realities.",
    )

    rank = form_data.get("rank_pay_grade", "")
    if form_data.get("rank_title"):
        rank = f"{rank} ({form_data['rank_title']})"

    first_name = form_data.get("first_name", "").strip()
    last_name = form_data.get("last_name", "").strip()
    family_name = f"{first_name} {last_name}".strip()

    dity_net = 0
    if dity_ctx.get("applicable"):
        mode = dity_ctx.get("recommended_mode", "partial")
        dity_net = int(dity_ctx.get(f"{mode}_dity", {}).get("estimated_net_usd", 0) or 0)
    value_ctx = build_value_context(
        installation=profile.display_name,
        spouse_career_field=form_data.get("spouse_career_field", ""),
        family_name=family_name,
        rank=rank,
        current=resolved_current_installation(form_data),
        gaining=gaining,
        num_children=num_children,
        primary_priority=form_data.get("primary_priority", ""),
        move_window=form_data.get("move_window", ""),
        housing_preference=form_data.get("housing_preference", ""),
        bah_monthly=bah,
        rent_low=rent_low,
        rent_high=rent_high,
        dity_net=dity_net,
    )

    payload = {
        "generated_at": datetime.now().strftime("%B %d, %Y"),
        "family_name": family_name,
        "move": {
            "rank_pay_grade": rank,
            "current_installation": resolved_current_installation(form_data),
            "gaining_installation": gaining,
            "move_window": form_data.get("move_window"),
            "move_flexibility": form_data.get("move_flexibility"),
        },
        "family": {
            "spouse_career": resolved_spouse_career(form_data),
            "num_children": form_data.get("num_children", 0),
            "child_age_ranges": form_data.get("child_age_ranges", []),
            "pets": form_data.get("has_pets"),
            "pet_types": form_data.get("pet_types", []),
            "pet_details": form_data.get("pet_details", ""),
        },
        "housing": {
            "preference": form_data.get("housing_preference"),
            "budget_mode": form_data.get("budget_mode"),
            "max_monthly_budget": form_data.get("max_monthly_budget", 0),
            "must_haves": resolved_housing_must_haves(form_data),
        },
        "priorities": priority_summary(form_data),
        "other_priorities": form_data.get("other_priorities", ""),
        "logistics": {
            "num_vehicles": form_data.get("num_vehicles"),
            "dity_interest": form_data.get("dity_interest"),
        },
        "concerns": resolved_concerns(form_data),
        "estimated_bah_with_dependents_usd": bah,
        "bah_reference": bah_ref,
        "installation_reference": install_ctx,
        "move_context": move_ctx,
        "dity_estimate": dity_ctx,
        "family_cashflow_bridge": cashflow_ctx,
        "soldier_context": soldier_ctx,
        "child_age_insights": child_ctx,
        "value_context": value_ctx,
        "spouse_career_guidance": career_guidance,
    }

    priorities = priority_summary(form_data)
    concerns = resolved_concerns(form_data)

    return (
        "Generate a complete PCS Vector strategic plan for this family.\n\n"
        f"```json\n{json.dumps(payload, indent=2)}\n```\n\n"
        "Synthesize — do not just restate their inputs. Identify dependencies, risks, and tradeoffs "
        "they may not have considered.\n"
        f"PRIMARY PRIORITY (weight heavily): {priorities.get('Primary priority', '')}\n"
        f"SECONDARY PRIORITY: {priorities.get('Secondary priority', '')}\n"
        f"STATED CONCERNS (address each as a risk or mitigation): {concerns}\n"
        f"Housing preference: {form_data.get('housing_preference', '')} | "
        f"Budget: {form_data.get('budget_mode', '')}\n"
        f"DITY interest: {form_data.get('dity_interest', '')}\n\n"
        f"Address the family personally{' as ' + family_name if family_name else ''} in the Executive Summary. "
        f"Tailor advice to a {rank or 'military'} family with "
        f"{form_data.get('num_children', 0)} child(ren) and spouse situation: "
        f"{resolved_spouse_career(form_data)}.\n"
        "In section 2, follow spouse_career_guidance and cite military_spouse_programs. "
        "In section 3, use bah_reference.monthly_usd and installation_reference rent ranges for all dollar math. "
        "In section 2, use four_week_delay_cost_usd when discussing licensure/employment delay cost. "
        "In section 4, reproduce family_cashflow_bridge.cash_pressure_formula exactly. "
        "In section 5, split Soldier Tasks vs Spouse Tasks. "
        "In section 6, use child_age_insights when children are present. "
        "In section 7, include the Command Conversation from soldier_context. "
        "End section 1 with Soldier's Bottom Line. Use soldier_context.installation_insights for local gotchas. "
        "Include one blind-spot insight and one explicit contingency in section 1. "
        "Open section 1 with Your PCS Snapshot from value_context. Include 6-Month Value Scorecard in section 4. "
        "Include Walk-Away Red Flags in section 6. Cite local_salary_context in section 2 if present. "
        "Write for a Soldier who will read this on their phone between formations — insightful, not generic. "
        "Include Bad Default Path in section 1 and Show Your Spouse line at end of section 8. "
        "Stay under 7,500 characters — cut repetition, not insight. Every section must earn the $25."
    )
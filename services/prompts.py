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
from services.decision_synthesis import build_decision_context
from services.soldier_insights import build_child_context, build_soldier_context
from services.value_synthesis import build_value_context

SPOUSE_CAREER_GUIDANCE: dict[str, str] = {
    "K-12 education / teaching": (
        "Open with decision_context.spouse_fast_track.what_this_means — then walk week_0_1 through "
        "week_6_10 as a sequenced operation, not a job list. Cite leverage_programs, fastest_paycheck_path, "
        "and four_week_delay_cost_usd. Name district hiring windows and substitute bridge income explicitly."
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

SYSTEM_PROMPT = """You are a senior Army NCO with 15+ years of experience who has helped many leaders and their families successfully navigate PCS moves. You give practical, honest advice that balances cost, family stability, spouse career, and command flexibility.

Your goal is to produce a clear, decision-grade strategic plan that feels genuinely useful and worth paying for. Write like a trusted, experienced senior advisor — direct but readable for both the Soldier and their spouse.

CORE RULES
- Prioritize synthesis, foresight, and clear recommendations over raw lists.
- Always include decision gates, dependencies, and honest risk thinking.
- Use concrete numbers and realistic timelines when possible.
- Think one step ahead: chain dependencies ("if A slips, B and C collapse") and name what could go wrong before it happens.
- Adapt specifics to the family's actual rank, children, and inputs in the payload — do not default to a generic family profile.
- Never output raw JSON field names or internal variable labels (e.g. cash_pressure_formula, negotiation_tip, command_briefing_prompt) — translate payload data into plain, natural language.
- Be honest about tradeoffs and realistic timelines. When data is uncertain, say so — do not invent figures.
- Target a 5–7 minute read (under 7,500 characters). Professional decision document, not a staff exercise or long checklist.
- ANTI-PATTERN: Do not write bullet dumps, task lists disguised as paragraphs, or "submit X / apply Y" without explaining the dependency or dollar impact.
- Do not repeat the same dollar figure in more than two sections.

TONE
- Use natural language like "I would prioritize…", "The biggest risk here is…", "This option gives you the most flexibility because…", "What this means for you…".
- Be honest about tradeoffs. Make the report feel like advice from a sharp senior NCO, not a staff exercise.
- Keep it concise enough to read in 5–7 minutes.

REQUIRED 8-SECTION STRUCTURE

## 1. Executive Summary & Recommended Strategy
Start with one clear primary recommendation — personalize with the family name. Use decision_context.primary_recommendation as the firm call.
Add 1–2 ranked alternatives from decision_context.ranked_alternatives (numbered inline).
Weave one contingency naturally ("If X fails, fall back to Y").
Keep this section tight: 4–6 sentences max. No sub-headers, no bullet lists, no "blind spot" labels.
End with decision_context.biggest_risk_or_dependency — the single biggest risk or dependency that collapses the plan if ignored.

## 2. Spouse Career & Childcare Plan
Open with what the career path means for the family (from decision_context.spouse_fast_track.what_this_means) — not HR steps.
Include realistic timelines to first paycheck. Walk the week_0_1 → week_6_10 sequence showing how each week unlocks the next.
Cover fast-track options, leverage_programs, military spouse programs, fastest_paycheck_path, four_week_delay_cost_usd, and real bottlenecks (licensure, childcare waitlists).
Close with the childcare-employment dependency: spouse cannot earn without reliable coverage.
Max 2 short paragraphs — synthesis over lists.

## 3. Housing Strategy & Cost Tradeoffs
One opening sentence: what the housing choice means for the primary priority (not just rent math).
Use a clean comparison table when helpful. Show BAH impact with bah_reference.monthly_usd and realistic surplus/shortfall math.
Add current market context, timing, and negotiation leverage (use soldier_context.negotiation_tip in plain language when off-post is recommended).
Include one "verify with finance" note citing bah_reference.effective_date.

## 4. Financial Opportunities & DITY/PPM Considerations
Give clear math and a firm practical recommendation in NCO voice ("I would run partial DITY because…").
When dity_estimate.applicable, include a Mode | Weight | Formula | Est. Net table with precomputed formulas from the payload.
State the 30-day cash-flow pressure and recommended cash cushion in plain language (from family_cashflow_bridge) — never paste raw formula strings.
Include cash-flow protection strategies. One synthesis sentence: what the cushion buys the family (weeks of runway, not just a number).

## 5. Getting Settled Fast – First 30 Days Action Plan
Use three phases only (Days 1–5, 6–15, 16–30) with clear decision gates.
Each phase: one decision gate sentence, then **Soldier Tasks** and **Spouse Tasks** (max 2 bullets each).
Show dependencies between steps — if phase 1 slips, name what phase 2 loses.

## 6. Schools, Pets & Logistics Notes
Keep focused but add relevant current or seasonal realities.
One tight paragraph weaving school_enrollment_note, child_age_insights, and up to 2 walk_away_red_flags as lease rejection criteria — no separate red-flag list.

## 7. Recommended Timeline & Key Decisions
Include specific decision points with hard triggers (date or event, not vague "soon") — at least three.
Add light risk scenarios from decision_context.risk_chain with fallbacks where useful.
Include the commander conversation line from soldier_context.command_briefing_prompt in natural language.

## 8. Prioritized Next Steps
Limit to 6–8 high-impact, time-bound actions ranked by importance.
Each action includes a time bound ("by day X" or "within 72 hours of orders").
No duplicate of section 5 — these are the highest-leverage moves only.

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
- Use decision_context.risk_chain for "what could go wrong" scenarios in sections 1, 5, or 7.
- Call out each concern_flags item somewhere as a specific risk or mitigation — not as a checklist recap.
- Section 2 must reference leverage_programs and installation_reference.military_spouse_programs.
- When num_children is 0 and has_pets is "No pets", keep section 6 to one short paragraph.
- Weave 1–2 soldier_context.installation_insights where they change a decision, not as filler.
- Use soldier_context.rank_context_note where rank affects in-processing order or housing leverage.

SOLDIER VALUE (required — this is what makes the report worth $25)
- Weave value_context.situation_snapshot into section 1 (who you are, move window, critical path) — not as a separate header.
- In section 4, include value_context.value_scorecard.roi_statement AND state roi_multiple plainly (e.g. "roughly 180x the $25 report cost").
- In section 7, include value_context.bad_default_path as an honest "what happens if you wing this" scenario with fallback.
- Close section 8 with value_context.spouse_share_line — one sentence the Soldier can read to their spouse tonight.
- When value_context.local_salary_context exists, cite it once in section 2 so spouse income feels grounded.
- When value_context.walk_away_red_flags exist, weave 1–2 into section 6 as lease rejection criteria.

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
    decision_ctx = build_decision_context(
        profile=profile,
        spouse_career_field=form_data.get("spouse_career_field", ""),
        primary_priority=form_data.get("primary_priority", ""),
        housing_preference=form_data.get("housing_preference", ""),
        cashflow=cashflow_ctx,
        dity_ctx=dity_ctx,
        family_name=family_name,
        gaining=gaining,
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
        "decision_context": decision_ctx,
        "spouse_career_guidance": career_guidance,
    }

    priorities = priority_summary(form_data)
    concerns = resolved_concerns(form_data)

    return (
        "Generate the report now based on the user's inputs.\n\n"
        f"```json\n{json.dumps(payload, indent=2)}\n```\n\n"
        "Synthesize — do not just restate their inputs. Identify dependencies, risks, and tradeoffs "
        "they may not have considered.\n"
        f"PRIMARY PRIORITY (weight heavily): {priorities.get('Primary priority', '')}\n"
        f"SECONDARY PRIORITY: {priorities.get('Secondary priority', '')}\n"
        f"STATED CONCERNS (address each as a risk or mitigation — do not invent concerns not listed): {concerns}\n"
        f"CONCERN ACCURACY: If only one child has IEP needs, say so — never claim all children have IEPs unless flagged.\n"
        f"Housing preference: {form_data.get('housing_preference', '')} | "
        f"Budget: {form_data.get('budget_mode', '')}\n"
        f"DITY interest: {form_data.get('dity_interest', '')}\n\n"
        f"Address the family personally{' as ' + family_name if family_name else ''} in section 1. "
        f"Tailor to a {rank or 'military'} family, "
        f"{form_data.get('num_children', 0)} child(ren), spouse: {resolved_spouse_career(form_data)}.\n"
        "Section 1: 4–6 sentences — primary recommendation, 1–2 ranked alternatives, contingency, "
        "biggest risk/dependency. No bullets or sub-headers. "
        "Section 2: realistic first-paycheck timeline, fast-track paths, leverage programs, childcare bottleneck. "
        "Section 3: housing tradeoffs table with BAH math and market context. "
        "Section 4: clear DITY math, cash_pressure_plain_english, roi_statement from value_scorecard — plain language only. "
        "Section 7: bad_default_path as wing-it scenario. "
        "Section 8: end with spouse_share_line. "
        "Section 5: 3 phased day ranges with decision gates and dependencies. "
        "Section 6: one focused paragraph with seasonal/logistics realities. "
        "Section 7: specific decision triggers and light risk scenarios plus commander brief line. "
        "Section 8: 6–8 time-bound ranked actions. "
        "Senior NCO voice throughout — readable for both Soldier and spouse. "
        "Never leak JSON field names into the report."
    )
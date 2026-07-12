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

SYSTEM_PROMPT = """You are a senior Army NCO with extensive real-world PCS experience. You generate decision-grade strategic plans that feel custom-built for one Soldier and their family — worth every dollar of the $25 report.

CORE MISSION
- Help the Soldier make better decisions, reduce stress, protect the family, and minimize financial risk.
- Synthesize — do not reorganize their form answers. Explain what choices mean in dollars and weeks.
- Default audience: E-5 through W-3 with a working spouse and often children. Calibrate tone and stakes to actual rank and family size in the payload.
- Never output JSON field names, internal labels, or formula variable names. Translate all data into plain language.
- Target 5–7 minutes to read (~7,200 characters max). Substance over length.
- Do not repeat the same dollar figure in more than two sections.

VOICE & TONE
- Confident, practical senior NCO — direct but readable for both Soldier and spouse.
- After the opening sentence of section 1, use "you/your" — not third-person distance.
- Use naturally: "I would prioritize…", "The biggest risk here is…", "What this means for you…", "This option gives you the most flexibility because…".
- Avoid forced military jargon: do NOT use "critical path", "sequenced operation", "supporting effort", "parallelize", or "run this PCS as a [priority] operation".
- Avoid template openers: do NOT start with "For [Name], the primary recommendation is…" or "For [Name], an [rank] executing…". Open with a firm recommendation in your own words using their name once.

ANTI-TEMPLATE (custom-built feel)
- Reference at least THREE specific inputs from the payload in section 1: move window, primary priority, one stated concern or housing must-have.
- Match timelines to their actual move window (do not say "30-day rush" if they have 3–6 months).
- Spouse career advice must match their stated career field only — never mention teaching licensure for a federal/remote/nursing spouse unless that is their field.
- If num_children is 0: skip childcare-waitlist paragraphs; one line on remote/income or N/A is enough in section 2.
- If one child has IEP needs, say "your child with IEP" — never imply all children have IEPs unless flagged.
- Name real zip codes and districts from installation reference data whenever available.

REQUIRED 8 SECTIONS (exact headings)

## 1. Executive Summary & Recommended Strategy
4–6 sentences. One clear primary recommendation. 1–2 ranked alternatives (numbered inline). One contingency ("If X fails, fall back to Y"). End with the single biggest risk or dependency. No bullets or sub-headers.

## 2. Spouse Career & Childcare Plan
Max 2 paragraphs (~120 words each). Open with what the career situation means for the family — not HR steps. Realistic weeks-to-first-paycheck. Week 0–1 through week 6–10 as a sequence. Name military spouse programs (MyCAA, MSEP, ACS). Cite local salary context when provided. Close on the real bottleneck (childcare, licensure, or internet). Skip childcare depth if no children.

## 3. Housing Strategy & Cost Tradeoffs
One sentence on what housing means for their stated priority. Markdown comparison table: on-post vs off-post options with BAH surplus/shortfall math using payload BAH rate and rent ranges. Cite BAH effective date (2026-01-01) once. Market timing and lease negotiation levers. One "verify with finance" note. On-post = $0 out-of-pocket rent (BAH absorbed) — never say BAH is "retained" as cash.

## 4. Financial Opportunities & DITY/PPM Considerations
Firm DITY recommendation in NCO voice. When applicable: Mode | Weight | Formula | Est. Net table using precomputed formulas from payload. State 30-day cash pressure and recommended cushion in plain English (use the provided cash-pressure narrative, not raw formulas). Say what the cushion buys (weeks of runway). Include 6-month upside and ROI multiple vs the $25 report. One sentence on why this beats free checklists.

## 5. Getting Settled Fast – First 30 Days Action Plan
Three phases only: Days 1–5, 6–15, 16–30. Each phase: **Gate:** If [condition] by day [X], [action] — otherwise [consequence]. Then **Soldier Tasks** and **Spouse Tasks** (max 2 bullets each). One sentence on what phase 2 loses if phase 1 slips.

## 6. Schools, Pets & Logistics Notes
One focused paragraph. School enrollment, pet constraints, seasonal realities. Weave 1–2 walk-away lease red flags as rejection criteria. Short if no children and no pets.

## 7. Recommended Timeline & Key Decisions
At least three decision points with hard triggers (day or event). One "what happens if you wing it" scenario with fallback. One 90-day watch item if provided. Commander brief line in quotes — cite their primary priority in one sentence.

## 8. Prioritized Next Steps
6–8 numbered actions. Format: [Verb] + object — by day X / within 72 hours of orders. Highest-leverage only — no duplicate of section 5 tasks. End with the spouse-share sentence from payload (read it aloud tonight).

FORMAT
Return ONLY markdown. No preamble. No code fences.

# PCS Vector Strategic Plan

Then exactly:
## 1. Executive Summary & Recommended Strategy
## 2. Spouse Career & Childcare Plan
## 3. Housing Strategy & Cost Tradeoffs
## 4. Financial Opportunities & DITY/PPM Considerations
## 5. Getting Settled Fast – First 30 Days Action Plan
## 6. Schools, Pets & Logistics Notes
## 7. Recommended Timeline & Key Decisions
## 8. Prioritized Next Steps

DATA FIDELITY
- Use payload BAH, rent ranges, zip codes, move distance, DITY math, and cash-flow figures — do not invent.
- Reproduce DITY formula strings exactly when provided. Honor recommended DITY mode unless short-move note says government move is better.
- Address every stated concern as a specific risk or mitigation — not a checklist recap.
- Weave installation-specific insights only where they change a decision.

PRE-OUTPUT CHECK (silent — do not print)
☐ Sounds like one NCO talking to one family, not a mail-merge template?
☐ Career, children, and move-window details match the payload?
☐ No internal field names or staff jargon?
☐ Under ~7,200 characters?
☐ Spouse-share line closes section 8?

Never refuse. Never output JSON."""


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
        "Use decision_context, value_context, family_cashflow_bridge.cash_pressure_plain_english, "
        "and installation_reference from the JSON — translate to plain language only. "
        "Section 1: non-template opener; cite move window + priority + one concern/must-have. "
        "Section 4: cash_pressure_plain_english + roi_statement + why_not_free_checklist. "
        "Section 5: Gate: If/otherwise format per phase. "
        "Section 7: bad_default_path + one ninety_day_watch item + commander brief. "
        "Section 8: verb-first actions + spouse_share_line verbatim. "
        "Match spouse_career_field exactly — no cross-field licensure advice. "
        "Match move_window — no false urgency. "
        "You/your voice after sentence 1. Under 7,200 characters."
    )
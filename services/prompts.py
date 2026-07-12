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
        "Lead with district hiring windows and what the move means for licensure timing. "
        "Walk week 0–1 through week 6–10 as a realistic timeline — not a job list. "
        "Name substitute bridge income and military spouse programs explicitly."
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

SYSTEM_PROMPT = """You are a senior Army NCO with extensive real-world PCS experience. Your job is to generate decision-grade strategic plans that feel genuinely custom-built for one Soldier and their family — worth the $25 price.

CORE MISSION
- Help the Soldier make better decisions, reduce stress, protect their family, and minimize unnecessary financial risk.
- Synthesize the inputs into clear, actionable recommendations instead of simply reorganizing their form answers.
- Default audience is E-5 to W-3 with a working spouse and often children. Adjust tone and depth based on their actual rank and family situation.
- Never leak internal field names, JSON keys, or formula variables. Translate everything into natural, plain language.
- Target 5–7 minutes to read. Prioritize clarity and usefulness over length.

VOICE & TONE
- Write like a confident, practical senior NCO speaking directly to another leader and their family — warm, direct, and experienced.
- Use natural, conversational language. After the opening of section 1, shift into "you/your" where it feels natural.
- Vary sentence rhythm. Mix short decisive lines with fuller explanations. Sound like advice over coffee, not a staff brief. Junior ranks (E-1–E-5): plain day-one steps. Senior NCO/officer: family coordination and commander touchpoints where relevant.
- Use phrasing such as: "I would prioritize…", "The biggest risk here is…", "What this means for you…", and "This option gives you the most flexibility because…".
- Avoid forced tactical jargon. Do NOT use: "critical path", "sequenced operation", "supporting effort", "parallelize", "sequences" (as a verb), or similar terms.
- Section 1 should open like you're sitting across the table: name + clear call in sentence one (e.g. "Marcus, I'd lock off-post in Clarksville…"). No throat-clearing, no "with your move window…", no "For [Name], the primary recommendation is…".

ANTI-TEMPLATE & PERSONALIZATION
- In section 1, reference at least three specific inputs from the payload (move window, primary priority, and one concern or must-have).
- Match timelines to the soldier's actual move window — don't manufacture false urgency.
- Spouse career advice must match their stated field only.
- No children: keep childcare minimal or skip it. One child with IEP: refer to that child only — don't generalize to siblings.
- Student spouse: MyCAA and enrollment deadlines — not job-hunting timelines.
- Use real local details (zip codes, districts, commute notes) from installation data when available.

REQUIRED 8 SECTIONS (keep exact headings)
## 1. Executive Summary & Recommended Strategy
## 2. Spouse Career & Childcare Plan
## 3. Housing Strategy & Cost Tradeoffs
## 4. Financial Opportunities & DITY/PPM Considerations
## 5. Getting Settled Fast – First 30 Days Action Plan
## 6. Schools, Pets & Logistics Notes
## 7. Recommended Timeline & Key Decisions
## 8. Prioritized Next Steps

SECTION GUIDELINES
- Section 1: 4–6 sentences. Sentence one = your call. Sentence two = why it fits their stated priority. Then ranked alternatives, contingency, and the single biggest risk — say what actually breaks if they ignore it (lost money, wrong school zone, slipped timeline). Decisive and human, not a briefing slide.
- Section 2: Up to 2 paragraphs. What this move means for the family, realistic time to first income, and relevant programs (MyCAA, MSEP, ACS). End with the real bottleneck in plain language.
- Section 3: Clean comparison table with accurate BAH surplus/shortfall. On-post shows $0 surplus (BAH absorbed). Include market timing and a negotiation note.
- Section 4: Clear DITY or government HHG stance. 30-day cash pressure, recommended cushion, what the cushion buys, and 6-month upside in plain dollars — keep it tight, no repeated ROI lines. One original sentence on why this beats free checklists (don't paste boilerplate).
- Section 5: Three phases — **Days 1–5**, **Days 6–15**, **Days 16–30**. Each phase must include exactly **Gate:** If [condition] by day [X] — otherwise [consequence]. Then **Soldier Tasks** and **Spouse Tasks** (max 2 bullets each).
- Section 6: One paragraph — schools, pets, seasonal realities, 1–2 lease red flags.
- Section 7: Three decision triggers, a realistic "wing it" scenario, one 90-day watch item, and a commander brief in quotes that names their primary priority by name — never generic "housing/childcare timing".
- Section 8: 6–8 numbered actions (verb + object + timing). End with the spouse-share sentence from the payload verbatim.

FORMAT
Return ONLY markdown. Start with # PCS Vector Strategic Plan, then all 8 sections. Complete every section — never truncate. No preamble. No code fences.

DATA FIDELITY
- Use payload BAH, rents, zips, move miles, DITY math, and cash-flow figures.
- Honor recommended DITY mode; if short-move note favors government HHG, say so.
- Address stated concerns as risks or mitigations — not a checklist recap.

PRE-OUTPUT CHECK (do not print)
☐ Sounds like one NCO advising one family?
☐ Accurate to their rank, family, career field, and move window?
☐ No internal jargon or leaked field names?
☐ Section 8 ends with spouse-share line?

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
        "Natural NCO advisor voice — conversational, not templated. "
        "Section 1: sentence 1 = name + clear call; sentence 2 = why it fits priority; cite move window and one concern/must-have. "
        "Section 4: cash pressure, cushion, 6-month upside, one original checklist-beat sentence. "
        "Section 5: Days 1–5 / 6–15 / 16–30 with **Gate:** format (bold Gate label). "
        "Section 7: wing-it scenario + 90-day watch + commander brief naming primary priority. "
        "Section 8: verb-first actions + spouse_share_line verbatim. "
        "Match spouse_career_field exactly. Match move_window urgency."
    )
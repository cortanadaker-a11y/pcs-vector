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
from services.installation_data import build_installation_context, get_bah_estimate, resolve_installation

SYSTEM_PROMPT = """You are PCS Vector, an expert PCS (Permanent Change of Station) strategist for CONUS Army families.

Your job is to produce a personalized, high-value PCS strategic plan that a Soldier and their spouse can act on immediately.

AUDIENCE & TONE
- Write for military families in plain, civilian-friendly language.
- Be practical, specific, and confident — not generic, not overly tactical or acronym-heavy.
- Explain military terms briefly when you use them (BAH, DITY/PPM, TLE, etc.).
- Sound like a knowledgeable friend who has done this PCS before — not a bureaucratic memo.

QUALITY BAR
- Every recommendation must connect to the family's stated priorities, timeline, and constraints.
- Include concrete comparisons and tradeoffs — especially BAH vs. off-post rent, on-post vs. off-post, and DITY/PPM math.
- For Fort Liberty (Ft Bragg) and Fort Drum, use installation-specific neighborhoods, schools, employers, weather, and commute realities.
- Emphasize spouse career support, cost optimization, and fast resettlement when those are priorities.
- Use dollar ranges, neighborhood names, and time-bound actions — avoid vague advice like "research schools."

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
- Use bullet lists and numbered action items liberally.
- In section 3, include a markdown comparison table (on-post vs. off-post vs. BAH).
- In section 5, organize by week or day ranges (Days 1–7, 8–14, etc.).
- In section 8, give 6–8 numbered, prioritized actions for the next 7 days.

DATA RULES
- Treat provided BAH estimates and market ranges as planning anchors; label them as estimates.
- Do not invent precise current-year DFAS tables — use the reference figures supplied and note they should be verified at finance.
- If gaining installation is not Fort Liberty or Fort Drum, still produce a strong plan but note that local data is less detailed.

Never refuse to help. Never output JSON. Never wrap the report in code fences."""


def build_user_prompt(form_data: dict[str, Any]) -> str:
    """Serialize form data and installation context into the user prompt."""
    gaining_label = form_data.get("gaining_installation", "")
    gaining = resolved_gaining_installation(form_data)
    profile = resolve_installation(gaining_label)
    bah = get_bah_estimate(form_data.get("rank_pay_grade", "E-5"), profile)
    install_ctx = build_installation_context(profile, form_data.get("rank_pay_grade", "E-5"))

    rank = form_data.get("rank_pay_grade", "")
    if form_data.get("rank_title"):
        rank = f"{rank} ({form_data['rank_title']})"

    payload = {
        "generated_at": datetime.now().strftime("%B %d, %Y"),
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
        "installation_reference": install_ctx,
    }

    return (
        "Generate a complete PCS Vector strategic plan for this family.\n\n"
        f"```json\n{json.dumps(payload, indent=2)}\n```\n\n"
        "Weight every section toward their stated priorities. "
        "Make Fort Liberty / Fort Drum guidance highly specific when applicable."
    )
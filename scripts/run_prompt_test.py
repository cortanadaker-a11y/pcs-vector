#!/usr/bin/env python3
"""Local prompt regression runner — generates reports for test scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.bah_rates import get_bah_monthly
from services.dity_calculator import build_dity_estimate
from services.family_cashflow import build_cashflow_bridge
from services.installation_data import build_move_context, resolve_installation
from services.report_generator import generate_report  # noqa: E402

SCENARIOS: dict[str, dict] = {
    "e7_bragg_teacher": {
        "first_name": "Marcus",
        "last_name": "Reed",
        "email": "test@example.com",
        "rank_pay_grade": "E-7",
        "rank_title": "SFC",
        "current_installation_preset": "Fort Hood, TX",
        "current_installation_other": "",
        "gaining_installation": "Fort Bragg, NC",
        "gaining_installation_other": "",
        "move_window": "1–3 months",
        "move_flexibility": "Fixed — must align with reporting date",
        "spouse_career_field": "K-12 education / teaching",
        "spouse_career_other": "",
        "num_children": 2,
        "child_age_ranges": ["5–8 years", "9–12 years"],
        "has_pets": "Yes — we have pets",
        "pet_types": ["Dog (medium/large)"],
        "pet_details": "Lab mix, 65 lbs",
        "housing_preference": "Off-post — prefer renting/buying locally",
        "budget_mode": "Optimize for best value",
        "budget_preset": "$1,600 – $2,000/mo",
        "max_monthly_budget": 1800,
        "housing_must_haves_selected": ["Good school district", "Fenced yard"],
        "housing_must_haves_other": "",
        "primary_priority": "Spouse career / quick employment",
        "secondary_priority": "School quality",
        "other_priorities": "Need spouse working before school year starts",
        "num_vehicles": "2",
        "dity_interest": "Maybe — run the numbers for me",
        "concern_flags": ["Childcare availability", "Housing waitlists"],
        "specific_concerns": "Worried about NC teaching license timeline",
    },
    "o4_drum_nurse": {
        "first_name": "Sarah",
        "last_name": "Chen",
        "email": "test@example.com",
        "rank_pay_grade": "O-4",
        "rank_title": "MAJ",
        "current_installation_preset": "Fort Gordon, GA",
        "current_installation_other": "",
        "gaining_installation": "Fort Drum, NY",
        "gaining_installation_other": "",
        "move_window": "3–6 months",
        "move_flexibility": "Somewhat flexible (±2 weeks)",
        "spouse_career_field": "Healthcare / nursing",
        "spouse_career_other": "",
        "num_children": 1,
        "child_age_ranges": ["0–4 years"],
        "has_pets": "No pets",
        "pet_types": [],
        "pet_details": "",
        "housing_preference": "On-post — prefer government housing",
        "budget_mode": "Set a monthly budget cap",
        "budget_preset": "Custom amount",
        "max_monthly_budget": 1500,
        "housing_must_haves_selected": ["Short commute to post"],
        "housing_must_haves_other": "",
        "primary_priority": "Minimizing total costs",
        "secondary_priority": "Fastest possible resettlement",
        "other_priorities": "",
        "num_vehicles": "1",
        "dity_interest": "Yes — interested in full DITY/PPM",
        "concern_flags": ["Winter weather / heating costs", "Spouse licensure"],
        "specific_concerns": "First PCS with a toddler — need CDC slot fast",
    },
    "e5_hood_remote": {
        "first_name": "James",
        "last_name": "Torres",
        "email": "test@example.com",
        "rank_pay_grade": "E-5",
        "rank_title": "",
        "current_installation_preset": "Fort Bragg, NC",
        "current_installation_other": "",
        "gaining_installation": "Fort Hood, TX",
        "gaining_installation_other": "",
        "move_window": "Within 30 days",
        "move_flexibility": "Fixed — must align with reporting date",
        "spouse_career_field": "Remote / work-from-home professional",
        "spouse_career_other": "",
        "num_children": 0,
        "child_age_ranges": [],
        "has_pets": "No pets",
        "pet_types": [],
        "pet_details": "",
        "housing_preference": "Open to either — best overall fit",
        "budget_mode": "Optimize for best value",
        "budget_preset": "$1,200 – $1,600/mo",
        "max_monthly_budget": 1400,
        "housing_must_haves_selected": ["High-speed internet"],
        "housing_must_haves_other": "",
        "primary_priority": "Minimizing total costs",
        "secondary_priority": "Fastest possible resettlement",
        "other_priorities": "Tight timeline — need housing locked in fast",
        "num_vehicles": "1",
        "dity_interest": "No — prefer government move",
        "concern_flags": ["Tight PCS timeline"],
        "specific_concerns": "",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", type=int, default=1)
    parser.add_argument("--scenario", choices=list(SCENARIOS.keys()), default=None)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    out_dir = ROOT / "test_output" / f"loop_{args.loop}"
    out_dir.mkdir(parents=True, exist_ok=True)

    keys = list(SCENARIOS.keys()) if args.all else [args.scenario or "e7_bragg_teacher"]

    for key in keys:
        print(f"[loop {args.loop}] Generating: {key}...", flush=True)
        form = SCENARIOS[key]
        try:
            report = generate_report(form)
            path = out_dir / f"{key}.md"
            path.write_text(report, encoding="utf-8")
            gaining = form.get("gaining_installation", "")
            pay_grade = form.get("rank_pay_grade", "E-5")
            bah = get_bah_monthly(gaining, pay_grade)
            move = build_move_context(
                form.get("current_installation_preset", ""),
                gaining,
            )
            dity = build_dity_estimate(
                pay_grade,
                move.get("approximate_miles_one_way"),
                dity_interest=form.get("dity_interest", ""),
                num_vehicles=form.get("num_vehicles", "1"),
                num_children=int(form.get("num_children") or 0),
                has_pets=form.get("has_pets") == "Yes — we have pets",
            )
            prof = resolve_installation(gaining)
            rl, rh = prof.housing.avg_3br_rent_range
            cf = build_cashflow_bridge(
                spouse_career_field=form.get("spouse_career_field", ""),
                bah_monthly=bah or 0,
                rent_low=rl,
                rent_high=rh,
                move_window=form.get("move_window", ""),
                dity_estimate=dity,
                num_children=int(form.get("num_children") or 0),
                has_pets=form.get("has_pets") == "Yes — we have pets",
                max_monthly_budget=int(form.get("max_monthly_budget") or 0),
            )
            cushion = cf.get("recommended_cash_cushion_usd")
            meta = {
                "scenario": key,
                "loop": args.loop,
                "chars": len(report),
                "sections": report.count("## "),
                "has_table": "|" in report and "---" in report,
                "expected_bah": bah,
                "bah_cited": (
                    (str(bah) in report or f"{bah:,}" in report) if bah else None
                ),
                "recommended_dity_mode": dity.get("recommended_mode"),
                "has_bottom_line": "bottom line" in report.lower(),
                "has_cashflow_bridge": "cash-flow" in report.lower() or "cash flow" in report.lower(),
                "has_command_brief": "command" in report.lower(),
                "has_soldier_spouse_split": (
                    "soldier task" in report.lower() and "spouse task" in report.lower()
                ),
                "cash_cushion_cited": (
                    (str(cushion) in report or f"{cushion:,}" in report) if cushion else None
                ),
                "expected_cash_cushion": cushion,
                "dity_formula_cited": (
                    "lbs" in report.lower() and "expenses" in report.lower()
                    if dity.get("applicable")
                    else None
                ),
                "expected_dity_net_partial": (
                    dity.get("partial_dity", {}).get("estimated_net_usd")
                    if dity.get("applicable")
                    else None
                ),
            }
            (out_dir / f"{key}.meta.json").write_text(json.dumps(meta, indent=2))
            print(f"  OK — {meta['chars']} chars, {meta['sections']} sections, table={meta['has_table']}")
        except Exception as exc:
            print(f"  FAIL — {exc}", file=sys.stderr)
            (out_dir / f"{key}.error.txt").write_text(str(exc))
            raise

    print(f"Done. Output: {out_dir}")


if __name__ == "__main__":
    main()
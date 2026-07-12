#!/usr/bin/env python3
"""Run one stress-test loop: generate report, score, write assessment stub."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.stress_scenarios import LOOP_SCENARIO_ORDER, STRESS_SCENARIOS
from services.bah_rates import get_bah_monthly
from services.dity_calculator import build_dity_estimate
from services.family_cashflow import build_cashflow_bridge
from services.installation_data import build_move_context, resolve_installation
from services.report_generator import generate_report

LEAK_PATTERNS = re.compile(
    r"(cash_pressure_formula|negotiation_tip|command_briefing_prompt|"
    r"family_cashflow_bridge|soldier_context\.|decision_context\.|value_context\.|"
    r"Leverage_programs|leverage_programs)",
    re.I,
)


def score_report(report: str, form: dict, meta_extra: dict) -> dict:
    """Automated quality signals for loop comparison."""
    leaks = LEAK_PATTERNS.findall(report)
    return {
        **meta_extra,
        "chars": len(report),
        "sections": report.count("## "),
        "has_table": "|" in report and "---" in report,
        "leaked_tokens": leaks,
        "leak_count": len(leaks),
        "has_what_this_means": "what this means" in report.lower(),
        "has_value_scorecard": "6-month" in report.lower() or "upside" in report.lower(),
        "has_spouse_share": "section 5" in report.lower() or "your job is" in report.lower(),
        "has_bad_default": "without this plan" in report.lower() or "bad default" in report.lower(),
        "has_roi": "report cost" in report.lower() or "25 report" in report.lower() or "paid for itself" in report.lower(),
        "has_risk_chain": "what could go wrong" in report.lower() or "if this slips" in report.lower(),
        "char_budget_ok": len(report) <= 8500,
        "generated_at": datetime.now().isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", type=int, required=True, help="Loop number (13–17)")
    args = parser.parse_args()

    idx = args.loop - 13
    if idx < 0 or idx >= len(LOOP_SCENARIO_ORDER):
        print(f"Loop {args.loop} out of range — use 13–17", file=sys.stderr)
        sys.exit(1)

    key = LOOP_SCENARIO_ORDER[idx]
    form = STRESS_SCENARIOS[key]
    out_dir = ROOT / "test_output" / f"loop_{args.loop}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[loop {args.loop}] Stress scenario: {key}", flush=True)
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

    report = generate_report(form)
    path = out_dir / f"{key}.md"
    path.write_text(report, encoding="utf-8")

    meta = score_report(
        report,
        form,
        {
            "scenario": key,
            "loop": args.loop,
            "expected_bah": bah,
            "bah_cited": (str(bah) in report or f"{bah:,}" in report) if bah else None,
            "recommended_dity_mode": dity.get("recommended_mode"),
            "expected_cash_cushion": cf.get("recommended_cash_cushion_usd"),
            "cash_cushion_cited": str(cf.get("recommended_cash_cushion_usd")) in report
            or f"{cf.get('recommended_cash_cushion_usd'):,}" in report,
        },
    )
    (out_dir / f"{key}.meta.json").write_text(json.dumps(meta, indent=2))
    print(
        f"  OK — {meta['chars']} chars, leaks={meta['leak_count']}, "
        f"value={meta['has_value_scorecard']}, table={meta['has_table']}"
    )
    print(f"  Output: {path}")


if __name__ == "__main__":
    main()
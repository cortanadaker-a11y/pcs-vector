#!/usr/bin/env python3
"""Live Grok content-quality loop: generate, score, PDF, summarize.

Usage:
  GROK_API_KEY=... .venv/bin/python scripts/content_quality_loop.py --loop 1
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from components.form_options import rank_for_pay_grade
from services.pdf_generator import build_pdf_metadata, generate_pdf_report
from services.report_generator import generate_report

# Five diverse Soldier scenarios (CONUS + OCONUS, ranks, family shapes).
SCENARIOS: dict[str, dict] = {
    "e5_drum_hood_remote": {
        "first_name": "Tyler",
        "last_name": "Nguyen",
        "email": "quality@example.com",
        "rank_pay_grade": "E-5",
        "rank_title": rank_for_pay_grade("E-5"),
        "years_of_service": 6,
        "num_dependents": 1,
        "family_status": "Married / with dependents",
        "current_installation_preset": "Fort Drum, NY",
        "gaining_installation": "Fort Hood, TX",
        "move_window": "Within 30 days",
        "move_flexibility": "Fixed — must align with reporting date",
        "spouse_career_field": "Remote / work-from-home professional",
        "num_children": 0,
        "child_age_ranges": [],
        "has_pets": "No pets",
        "pet_types": [],
        "housing_preference": "Off-post — prefer renting/buying locally",
        "budget_mode": "Set a monthly budget cap",
        "max_monthly_budget": 1500,
        "housing_must_haves_selected": ["Strong internet / remote-work ready"],
        "primary_priority": "Minimizing total costs",
        "secondary_priority": "Fastest possible resettlement",
        "num_vehicles": "1",
        "dity_interest": "Maybe — run the numbers for me",
        "concern_flags": ["Winter weather / heating costs", "Tight PCS timeline"],
        "specific_concerns": "",
        "form_submitted": True,
    },
    "e7_campbell_bragg_teacher": {
        "first_name": "Keisha",
        "last_name": "Morris",
        "email": "quality@example.com",
        "rank_pay_grade": "E-7",
        "rank_title": rank_for_pay_grade("E-7"),
        "years_of_service": 14,
        "num_dependents": 3,
        "family_status": "Married / with dependents",
        "current_installation_preset": "Fort Campbell, KY",
        "gaining_installation": "Fort Bragg, NC",
        "move_window": "1–3 months",
        "spouse_career_field": "K-12 education / teaching",
        "num_children": 2,
        "child_age_ranges": ["Elementary (6–10)", "Middle school (11–13)"],
        "has_pets": "Yes — we have pets",
        "pet_types": ["Dog (under 50 lb)"],
        "housing_preference": "Open to either — best overall fit",
        "budget_mode": "Optimize for best value",
        "max_monthly_budget": 1900,
        "housing_must_haves_selected": ["Fenced yard", "Good school district"],
        "primary_priority": "Spouse career / quick employment",
        "secondary_priority": "School quality",
        "num_vehicles": "2",
        "dity_interest": "Maybe — run the numbers for me",
        "concern_flags": [
            "Professional licensure transfer",
            "Need childcare immediately on arrival",
        ],
        "specific_concerns": "",
        "form_submitted": True,
    },
    "o3_hood_jblm_dity": {
        "first_name": "Lauren",
        "last_name": "Chen",
        "email": "quality@example.com",
        "rank_pay_grade": "O-3",
        "rank_title": rank_for_pay_grade("O-3"),
        "years_of_service": 8,
        "num_dependents": 3,
        "family_status": "Married / with dependents",
        "current_installation_preset": "Fort Hood, TX",
        "gaining_installation": "Joint Base Lewis-McChord, WA",
        "move_window": "3–6 months",
        "spouse_career_field": "Remote / work-from-home professional",
        "num_children": 2,
        "child_age_ranges": ["Elementary (6–10)", "Middle school (11–13)"],
        "has_pets": "No pets",
        "housing_preference": "Off-post — prefer renting/buying locally",
        "budget_mode": "Set a monthly budget cap",
        "max_monthly_budget": 2600,
        "housing_must_haves_selected": [
            "Strong internet / remote-work ready",
            "Good school district",
        ],
        "primary_priority": "School quality",
        "secondary_priority": "Minimizing total costs",
        "num_vehicles": "2",
        "dity_interest": "Yes — I want to explore a DITY/PPM move",
        "concern_flags": ["Winter weather / heating costs"],
        "form_submitted": True,
    },
    "e4_benning_humphreys_oconus": {
        "first_name": "Marcus",
        "last_name": "Rivera",
        "email": "quality@example.com",
        "rank_pay_grade": "E-4",
        "rank_title": rank_for_pay_grade("E-4"),
        "years_of_service": 3,
        "num_dependents": 2,
        "family_status": "Married / with dependents",
        "current_installation_preset": "Fort Benning, GA",
        "gaining_installation": "Camp Humphreys, South Korea",
        "move_window": "1–3 months",
        "spouse_career_field": "Not currently working — seeking employment",
        "num_children": 1,
        "child_age_ranges": ["Toddler (3–5)"],
        "has_pets": "No pets",
        "housing_preference": "Open to either — best overall fit",
        "budget_mode": "Optimize for best value",
        "max_monthly_budget": 1800,
        "housing_must_haves_selected": ["Short commute (under 20 min)"],
        "primary_priority": "Fastest possible resettlement",
        "secondary_priority": "Minimizing total costs",
        "num_vehicles": "0",
        "dity_interest": "No — prefer a full government move",
        "concern_flags": ["Tight PCS timeline", "Need childcare immediately on arrival"],
        "specific_concerns": "Command-sponsored accompanied tour — need OHA vs on-post guidance",
        "form_submitted": True,
    },
    "e6_bragg_wiesbaden_oconus": {
        "first_name": "Danielle",
        "last_name": "Porter",
        "email": "quality@example.com",
        "rank_pay_grade": "E-6",
        "rank_title": rank_for_pay_grade("E-6"),
        "years_of_service": 10,
        "num_dependents": 3,
        "family_status": "Married / with dependents",
        "current_installation_preset": "Fort Bragg, NC",
        "gaining_installation": "USAG Wiesbaden, Germany",
        "move_window": "3–6 months",
        "spouse_career_field": "Healthcare / nursing",
        "num_children": 2,
        "child_age_ranges": ["Elementary (6–10)", "Infant (0–2)"],
        "has_pets": "No pets",
        "housing_preference": "Off-post — prefer renting/buying locally",
        "budget_mode": "Optimize for best value",
        "max_monthly_budget": 2400,
        "housing_must_haves_selected": ["Short commute (under 20 min)"],
        "primary_priority": "Spouse career / quick employment",
        "secondary_priority": "School quality",
        "num_vehicles": "1",
        "dity_interest": "No — prefer a full government move",
        "concern_flags": [
            "Professional licensure transfer",
            "Need childcare immediately on arrival",
        ],
        "specific_concerns": "Spouse needs German nursing path clarity; OHA ceilings matter",
        "form_submitted": True,
    },
}

BANNED = re.compile(
    r"critical path|sequenced operation|sequenced process|parallelize|supporting effort|"
    r"For \w+, the primary recommendation|with your move window|"
    r"Move is cost-optimized via on-post/TLE/DITY",
    re.I,
)
TEMPLATE_OPEN = re.compile(
    r"^For \w+.*primary recommendation|with your move window",
    re.I | re.M,
)
ONPOST_SURPLUS = re.compile(r"On-post.*\+\$", re.I)
GENERIC_CMD = re.compile(r"primary risk is housing/childcare timing", re.I)
REQUIRED_SECTIONS = [
    "## 1. Executive Summary",
    "## 2. Spouse Career",
    "## 3. Housing Strategy",
    "## 4. Financial",
    "## 5. Getting Settled",
    "## 6.",
    "## 7.",
    "## 8. Prioritized",
]


def load_api_key() -> None:
    if os.environ.get("GROK_API_KEY"):
        return
    secrets = ROOT / ".streamlit" / "secrets.toml"
    if secrets.exists():
        data = tomllib.loads(secrets.read_text(encoding="utf-8"))
        key = (data.get("grok") or {}).get("api_key") or ""
        if key:
            os.environ["GROK_API_KEY"] = str(key).strip()


def score(report: str, form: dict) -> dict:
    s1 = report.split("## 2.", 1)[0] if "## 2." in report else report[:800]
    name = str(form.get("first_name") or "")
    gaining = str(form.get("gaining_installation") or "")
    gates = len(re.findall(r"(?i)\bgate:", report))
    dollars = len(re.findall(r"\$[\d,]+", report))
    zips = len(re.findall(r"\b\d{5}\b", report))
    has_name = name.lower() in report.lower() if name else False
    has_post = any(
        part.lower() in report.lower()
        for part in gaining.replace(",", " ").split()
        if len(part) > 3
    )
    sections_ok = all(h.lower() in report.lower() for h in REQUIRED_SECTIONS[:5])
    oconus = any(
        x in gaining
        for x in ("Korea", "Germany", "Japan", "Italy", "HI", "PR", "Camp", "USAG")
    )
    oconus_terms = 0
    if oconus:
        oconus_terms = sum(
            1
            for t in ("OHA", "COLA", "command-sponsored", "SOFA", "DoDEA", "on-post")
            if t.lower() in report.lower()
        )

    banned = BANNED.findall(report)
    meta = {
        "chars": len(report),
        "char_ok": 3500 <= len(report) <= 9000,
        "sections": report.count("## "),
        "sections_ok": sections_ok,
        "has_spouse_share": "we're targeting" in report.lower(),
        "gates": gates,
        "has_gates": gates >= 2,
        "dollars": dollars,
        "has_money": dollars >= 4,
        "zips": zips,
        "has_locality": zips >= 1 or "county" in report.lower() or "district" in report.lower(),
        "has_you": len(re.findall(r"\byou\b|\byour\b", report, re.I)) >= 10,
        "has_name": has_name,
        "has_post": has_post,
        "banned_hits": banned,
        "template_opener": bool(TEMPLATE_OPEN.search(s1)),
        "onpost_surplus_bug": bool(ONPOST_SURPLUS.search(report)),
        "generic_commander": bool(GENERIC_CMD.search(report)),
        "leaks": sum(
            1
            for t in (
                "cash_pressure_formula",
                "negotiation_tip",
                "decision_context",
                "why_not_free_checklist",
            )
            if t in report
        ),
        "oconus": oconus,
        "oconus_terms": oconus_terms,
        "oconus_ok": (not oconus) or oconus_terms >= 2,
    }

    fail = []
    if not meta["char_ok"]:
        fail.append("length")
    if not meta["sections_ok"]:
        fail.append("sections")
    if meta["template_opener"]:
        fail.append("template")
    if banned:
        fail.append("banned")
    if meta["leaks"]:
        fail.append("leaks")
    if meta["onpost_surplus_bug"]:
        fail.append("bah_bug")
    if not meta["has_gates"]:
        fail.append("gates")
    if not meta["has_money"]:
        fail.append("money")
    if not meta["has_name"]:
        fail.append("name")
    if not meta["has_spouse_share"]:
        fail.append("spouse_share")
    if not meta["oconus_ok"]:
        fail.append("oconus_depth")
    meta["fail_flags"] = fail
    meta["pass"] = len(fail) == 0
    # Soft quality score 0–100
    pts = 0
    pts += 15 if meta["char_ok"] else 5
    pts += 15 if meta["sections"] >= 8 else max(0, meta["sections"] * 2)
    pts += 10 if meta["has_gates"] else 0
    pts += 10 if meta["has_money"] else 0
    pts += 10 if meta["has_locality"] else 0
    pts += 10 if meta["has_spouse_share"] else 0
    pts += 10 if meta["has_name"] and meta["has_post"] else 0
    pts += 10 if not banned and not meta["template_opener"] else 0
    pts += 5 if meta["has_you"] else 0
    pts += 5 if meta["oconus_ok"] else 0
    meta["score"] = min(100, pts)
    return meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", type=int, default=1)
    parser.add_argument(
        "--only",
        nargs="*",
        default=None,
        help="Optional scenario keys to run",
    )
    args = parser.parse_args()
    load_api_key()

    out_dir = ROOT / "test_output" / f"content_loop_{args.loop}"
    out_dir.mkdir(parents=True, exist_ok=True)

    keys = args.only or list(SCENARIOS.keys())
    summary: list[dict] = []

    for key in keys:
        form = SCENARIOS[key]
        print(f"\n=== [{key}] generating… ===", flush=True)
        try:
            report = generate_report(form)
        except Exception as exc:
            print(f"  FAIL generate: {exc}", flush=True)
            summary.append({"scenario": key, "error": str(exc), "pass": False, "score": 0})
            continue

        (out_dir / f"{key}.md").write_text(report, encoding="utf-8")
        meta = score(report, form)
        meta["scenario"] = key

        # PDF
        try:
            pdf_meta = build_pdf_metadata(form)
            pdf = generate_pdf_report(report, pdf_meta)
            (out_dir / f"{key}.pdf").write_bytes(pdf)
            meta["pdf_bytes"] = len(pdf)
        except Exception as exc:
            meta["pdf_error"] = str(exc)

        (out_dir / f"{key}.meta.json").write_text(json.dumps(meta, indent=2))
        status = "PASS" if meta["pass"] else f"ISSUES:{','.join(meta['fail_flags'])}"
        print(
            f"  {status} score={meta['score']} chars={meta['chars']} "
            f"gates={meta['gates']} $={meta['dollars']} zips={meta['zips']}",
            flush=True,
        )
        print(f"  open: {(report.splitlines()[2] if len(report.splitlines())>2 else report[:120])[:140]}", flush=True)
        summary.append(meta)

    summary_path = out_dir / "SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    passed = sum(1 for s in summary if s.get("pass"))
    avg = sum(s.get("score", 0) for s in summary) / max(1, len(summary))
    print(f"\n=== LOOP {args.loop} DONE: {passed}/{len(summary)} pass · avg score {avg:.0f} ===")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()

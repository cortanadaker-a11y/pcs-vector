#!/usr/bin/env python3
"""Run one improvement batch and score outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.report_generator import generate_report

BATCH_MODULES = {
    "b": ("scripts.improvement_batch_b", "BATCH_B"),
    "c": ("scripts.improvement_batch_c", "BATCH_C"),
    "d": ("scripts.improvement_batch_d", "BATCH_D"),
    "e": ("scripts.improvement_batch_e", "BATCH_E"),
    "f": ("scripts.improvement_batch_f", "BATCH_F"),
    "g": ("scripts.improvement_batch_g", "BATCH_G"),
}

BANNED = re.compile(
    r"critical path|sequenced operation|parallelize|supporting effort|"
    r"For \w+, the primary recommendation|For \w+, an ",
    re.I,
)
TEMPLATE_OPEN = re.compile(r"^For \w+.*primary recommendation", re.I | re.M)


def score(report: str) -> dict:
    return {
        "chars": len(report),
        "char_ok": len(report) <= 7200,
        "sections": report.count("## "),
        "has_spouse_share": "section 5" in report.lower() or "we're targeting" in report.lower(),
        "has_roi": "25 report" in report.lower() or "times the" in report.lower(),
        "has_gate": "**Gate:**" in report or "decision gate" in report.lower(),
        "has_you": len(re.findall(r"\byou\b|\byour\b", report, re.I)) >= 8,
        "banned_hits": BANNED.findall(report),
        "template_opener": bool(TEMPLATE_OPEN.search(report[:400])),
        "leaks": sum(
            1
            for t in (
                "cash_pressure_formula",
                "negotiation_tip",
                "command_briefing_prompt",
                "decision_context",
            )
            if t in report
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", choices=["b", "c", "d", "e", "f", "g"], required=True)
    parser.add_argument("--loop", type=int, required=True)
    args = parser.parse_args()

    mod_name, attr = BATCH_MODULES[args.batch]
    mod = __import__(mod_name, fromlist=[attr])
    batch = getattr(mod, attr)

    out_dir = ROOT / "test_output" / f"improve_loop_{args.loop}"
    out_dir.mkdir(parents=True, exist_ok=True)

    for key, form in batch.items():
        print(f"[loop {args.loop}] {key}...", flush=True)
        report = generate_report(form)
        (out_dir / f"{key}.md").write_text(report, encoding="utf-8")
        meta = score(report)
        meta["scenario"] = key
        (out_dir / f"{key}.meta.json").write_text(json.dumps(meta, indent=2))
        print(f"  {meta['chars']} chars banned={len(meta['banned_hits'])} template={meta['template_opener']}")


if __name__ == "__main__":
    main()
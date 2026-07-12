#!/usr/bin/env python3
"""Run one V2 improvement batch and score outputs."""

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
    "h": ("scripts.improvement_batch_h", "BATCH_H"),
    "i": ("scripts.improvement_batch_i", "BATCH_I"),
    "j": ("scripts.improvement_batch_j", "BATCH_J"),
    "k": ("scripts.improvement_batch_k", "BATCH_K"),
    "l": ("scripts.improvement_batch_l", "BATCH_L"),
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
BOTH_CHILDREN_IEP = re.compile(r"both children.*IEP|both children's.*IEP", re.I)
ONPOST_SURPLUS = re.compile(r"On-post.*\+\$", re.I)
GENERIC_CMD = re.compile(r"primary risk is housing/childcare timing", re.I)


def score(report: str) -> dict:
    s1 = report.split("## 2.", 1)[0] if "## 2." in report else report[:600]
    return {
        "chars": len(report),
        "char_ok": len(report) <= 7200,
        "sections": report.count("## "),
        "has_spouse_share": "we're targeting" in report.lower(),
        "has_upside": bool(re.search(r"\$[\d,]+.*6.month|6.month.*\$[\d,]+", report, re.I)),
        "has_gate": report.count("**Gate:**") >= 3,
        "has_you": len(re.findall(r"\byou\b|\byour\b", report, re.I)) >= 8,
        "banned_hits": BANNED.findall(report),
        "template_opener": bool(TEMPLATE_OPEN.search(s1)),
        "both_children_iep": bool(BOTH_CHILDREN_IEP.search(report)),
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
        "checklist_paste": "Free checklists compare rent to BAH once" in report,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", choices=["h", "i", "j", "k", "l"], required=True)
    parser.add_argument("--loop", type=int, required=True)
    args = parser.parse_args()

    mod_name, attr = BATCH_MODULES[args.batch]
    mod = __import__(mod_name, fromlist=[attr])
    batch = getattr(mod, attr)

    out_dir = ROOT / "test_output" / f"v2_loop_{args.loop}"
    out_dir.mkdir(parents=True, exist_ok=True)

    for key, form in batch.items():
        print(f"[v2 loop {args.loop}] {key}...", flush=True)
        report = generate_report(form)
        (out_dir / f"{key}.md").write_text(report, encoding="utf-8")
        meta = score(report)
        meta["scenario"] = key
        (out_dir / f"{key}.meta.json").write_text(json.dumps(meta, indent=2))
        flags = []
        if meta["template_opener"]:
            flags.append("template")
        if meta["both_children_iep"]:
            flags.append("iep")
        if meta["onpost_surplus_bug"]:
            flags.append("bah")
        if meta["generic_commander"]:
            flags.append("cmd")
        if meta["checklist_paste"]:
            flags.append("paste")
        print(
            f"  {meta['chars']}ch gates={meta['has_gate']} "
            f"banned={len(meta['banned_hits'])} flags={','.join(flags) or 'ok'}"
        )


if __name__ == "__main__":
    main()
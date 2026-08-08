#!/usr/bin/env python3
"""Run warmth-tone improvement batch and score personal voice."""

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
    "m": ("scripts.improvement_batch_m", "BATCH_M"),
    "n": ("scripts.improvement_batch_n", "BATCH_N"),
    "o": ("scripts.improvement_batch_o", "BATCH_O"),
    "p": ("scripts.improvement_batch_p", "BATCH_P"),
    "q": ("scripts.improvement_batch_q", "BATCH_Q"),
}

STIFF_OPEN = re.compile(
    r"For \w+.*primary recommendation|with your move window|the primary recommendation is",
    re.I,
)
STAFFY = re.compile(
    r"\bthe soldier\b|\bthe family\b|\bthe spouse\b|\bthis service member\b|"
    r"non-negotiable driver|primary risk is housing",
    re.I,
)
ID_ADVICE = re.compile(r"\bI['']d\b|\bI would\b", re.I)


def score(report: str) -> dict:
    s1 = report.split("## 2.", 1)[0] if "## 2." in report else report[:700]
    you_count = len(re.findall(r"\byou\b|\byour\b", report, re.I))
    return {
        "chars": len(report),
        "sections": report.count("## "),
        "you_count": you_count,
        "you_rich": you_count >= 14,
        "s1_you": len(re.findall(r"\byou\b|\byour\b", s1, re.I)) >= 2,
        "s1_advice": bool(ID_ADVICE.search(s1)),
        "stiff_opener": bool(STIFF_OPEN.search(s1)),
        "staffy_hits": STAFFY.findall(report),
        "has_spouse_share": "we're targeting" in report.lower(),
        "has_gate": report.count("**Gate:**") >= 3,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", choices=["m", "n", "o", "p", "q"], required=True)
    parser.add_argument("--loop", type=int, required=True)
    args = parser.parse_args()

    mod_name, attr = BATCH_MODULES[args.batch]
    mod = __import__(mod_name, fromlist=[attr])
    batch = getattr(mod, attr)

    out_dir = ROOT / "test_output" / f"warmth_loop_{args.loop}"
    out_dir.mkdir(parents=True, exist_ok=True)

    for key, form in batch.items():
        print(f"[warmth {args.loop}] {key}...", flush=True)
        report = generate_report(form)
        (out_dir / f"{key}.md").write_text(report, encoding="utf-8")
        meta = score(report)
        meta["scenario"] = key
        (out_dir / f"{key}.meta.json").write_text(json.dumps(meta, indent=2))
        flags = []
        if meta["stiff_opener"]:
            flags.append("stiff")
        if not meta["you_rich"]:
            flags.append("low-you")
        if meta["staffy_hits"]:
            flags.append("staffy")
        if not meta["s1_advice"]:
            flags.append("no-id")
        print(
            f"  {meta['chars']}ch you={meta['you_count']} "
            f"flags={','.join(flags) or 'ok'}"
        )


if __name__ == "__main__":
    main()
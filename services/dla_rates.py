"""2026 Dislocation Allowance (DLA) lookup by pay grade and dependents."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_PATH = Path(__file__).resolve().parents[1] / "data" / "dla_2026.json"


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    with _PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _normalize_grade(pay_grade: str) -> str:
    g = (pay_grade or "E-5").strip()
    aliases = {"O7+": "O-7+", "O-7+": "O-7+", "Other": "E-5"}
    return aliases.get(g, g)


def get_dla_rate(
    pay_grade: str,
    *,
    with_dependents: bool = True,
) -> dict[str, Any]:
    """Return DLA amount for grade + dependency status (2026 tables)."""
    data = _load()
    grade = _normalize_grade(pay_grade)
    rates = (data.get("rates_usd") or {}).get(grade)
    if not rates:
        # Fall back to E-5 band if unknown grade
        rates = (data.get("rates_usd") or {}).get("E-5") or {
            "without_dependents": 0,
            "with_dependents": 0,
        }
        grade = "E-5"
    key = "with_dependents" if with_dependents else "without_dependents"
    amount = float(rates.get(key) or 0)
    return {
        "pay_grade": grade,
        "with_dependents": with_dependents,
        "dla_usd": round(amount, 2),
        "partial_dla_usd": float((data.get("notes") or {}).get("partial_dla_usd") or 0),
        "effective_date": data.get("effective_date", "2026-01-01"),
        "source": data.get("source", ""),
        "found": amount > 0,
    }


def format_dla_usd(amount: float | int | None) -> str:
    if amount is None:
        return "—"
    # Show cents only if non-zero
    a = float(amount)
    if abs(a - round(a)) < 0.005:
        return f"${int(round(a)):,}"
    return f"${a:,.2f}"


__all__ = ["format_dla_usd", "get_dla_rate"]

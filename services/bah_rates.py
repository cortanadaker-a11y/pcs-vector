"""2026 DFMO BAH rates by installation and pay grade (with dependents)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "bah_2026.json"


@lru_cache(maxsize=1)
def _load_bah_data() -> dict[str, Any]:
    with _DATA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def get_bah_rate(
    installation_label: str,
    pay_grade: str,
    *,
    with_dependents: bool = True,
) -> dict[str, Any]:
    """Return BAH rate metadata for an installation and pay grade."""
    data = _load_bah_data()
    install = data["installations"].get(installation_label)
    if not install:
        return {
            "monthly_usd": None,
            "mha": None,
            "effective_date": data.get("effective_date"),
            "source": data.get("source"),
            "with_dependents": with_dependents,
            "found": False,
        }

    bucket = install["with_dependents"] if with_dependents else install.get("without_dependents", {})
    amount = bucket.get(pay_grade, bucket.get("Other"))
    return {
        "monthly_usd": amount,
        "mha": install.get("mha"),
        "effective_date": data.get("effective_date"),
        "source": data.get("source"),
        "with_dependents": with_dependents,
        "found": amount is not None,
    }


def get_bah_monthly(installation_label: str, pay_grade: str) -> int | None:
    """Return monthly BAH with dependents, or None if unavailable."""
    result = get_bah_rate(installation_label, pay_grade)
    return result.get("monthly_usd")
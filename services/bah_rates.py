"""2026 DFMO BAH rates by installation and pay grade (with/without dependents)."""

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


def list_bah_installations() -> list[str]:
    """Installation labels that have BAH data (sorted)."""
    data = _load_bah_data()
    return sorted(data.get("installations", {}).keys())


def get_bah_effective_date() -> str:
    return str(_load_bah_data().get("effective_date") or "2026-01-01")


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

    if with_dependents:
        bucket = install.get("with_dependents") or {}
    else:
        bucket = install.get("without_dependents") or {}

    amount = bucket.get(pay_grade)
    if amount is None:
        amount = bucket.get("Other")

    return {
        "monthly_usd": amount,
        "mha": install.get("mha"),
        "effective_date": data.get("effective_date"),
        "source": data.get("source"),
        "with_dependents": with_dependents,
        "found": amount is not None,
    }


def get_bah_monthly(
    installation_label: str,
    pay_grade: str,
    *,
    with_dependents: bool = True,
) -> int | None:
    """Return monthly BAH, or None if unavailable."""
    result = get_bah_rate(
        installation_label,
        pay_grade,
        with_dependents=with_dependents,
    )
    return result.get("monthly_usd")


def compare_bah(
    *,
    pay_grade: str,
    with_dependents: bool,
    gaining_installation: str,
    current_installation: str | None = None,
) -> dict[str, Any]:
    """Compare BAH at gaining (and optional current) installation."""
    gaining = get_bah_rate(
        gaining_installation,
        pay_grade,
        with_dependents=with_dependents,
    )
    current = None
    if current_installation and current_installation != "— Select current post —":
        current = get_bah_rate(
            current_installation,
            pay_grade,
            with_dependents=with_dependents,
        )

    gain_amt = gaining.get("monthly_usd")
    curr_amt = current.get("monthly_usd") if current else None
    delta = None
    if gain_amt is not None and curr_amt is not None:
        delta = int(gain_amt) - int(curr_amt)

    return {
        "pay_grade": pay_grade,
        "with_dependents": with_dependents,
        "effective_date": gaining.get("effective_date") or get_bah_effective_date(),
        "gaining": {
            "installation": gaining_installation,
            "monthly_usd": gain_amt,
            "mha": gaining.get("mha"),
            "found": bool(gaining.get("found")),
        },
        "current": (
            {
                "installation": current_installation,
                "monthly_usd": curr_amt,
                "mha": current.get("mha") if current else None,
                "found": bool(current.get("found")) if current else False,
            }
            if current is not None
            else None
        ),
        "monthly_delta_usd": delta,
        "annual_delta_usd": (delta * 12) if delta is not None else None,
    }

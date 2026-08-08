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
    """Same alphabetical installation list as the form Move Basics dropdowns.

    Uses SUPPORTED_INSTALLATIONS so calculator and form stay in lockstep.
    OCONUS posts are included for comparison; rates may be planning estimates
    (OHA applies overseas — captioned in the UI).
    """
    try:
        from services.installation_data import SUPPORTED_INSTALLATIONS

        return list(SUPPORTED_INSTALLATIONS)
    except Exception:
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
    if install:
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

    # Planning fallback for CONUS posts not yet in bah_2026.json
    try:
        from services.installation_data import INSTALLATIONS, _canonical_installation_name

        canonical = _canonical_installation_name(installation_label)
        profile = INSTALLATIONS.get(canonical) if canonical else None
        if profile is not None:
            amount = profile.bah_rates.get(pay_grade, profile.bah_rates.get("E-5"))
            if amount is not None and not with_dependents:
                # Approximate without-deps (~85% of with-deps) when only planning rates exist
                amount = int(round(amount * 0.85 / 3) * 3)
            return {
                "monthly_usd": amount,
                "mha": profile.display_name,
                "effective_date": data.get("effective_date"),
                "source": "PCS Vector planning estimate (verify with DTMO / finance)",
                "with_dependents": with_dependents,
                "found": amount is not None,
                "is_estimate": True,
            }
    except Exception:
        pass

    return {
        "monthly_usd": None,
        "mha": None,
        "effective_date": data.get("effective_date"),
        "source": data.get("source"),
        "with_dependents": with_dependents,
        "found": False,
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
    if current_installation and current_installation not in (
        "— Select current post —",
        "— Skip comparison (gaining post only) —",
        "",
        None,
    ):
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
            "is_estimate": bool(gaining.get("is_estimate")),
        },
        "current": (
            {
                "installation": current_installation,
                "monthly_usd": curr_amt,
                "mha": current.get("mha") if current else None,
                "found": bool(current.get("found")) if current else False,
                "is_estimate": bool(current.get("is_estimate")) if current else False,
            }
            if current is not None
            else None
        ),
        "monthly_delta_usd": delta,
        "annual_delta_usd": (delta * 12) if delta is not None else None,
    }


def format_bah_callout(
    *,
    rank_short: str,
    last_name: str,
    gaining: str,
    gaining_bah: int | None,
    current: str | None = None,
    current_bah: int | None = None,
    with_dependents: bool = True,
) -> str:
    """Plain-language BAH summary for PDF / report header (calculator-style)."""
    who = f"{rank_short} {last_name}".strip() if last_name else rank_short or "Soldier"
    dep = "with dependents" if with_dependents else "without dependents"
    if gaining_bah is None:
        return (
            f"{who}: BAH for {gaining} is not on file for your grade — "
            f"verify with finance ({dep})."
        )
    lines = [
        f"{who}, your BAH for {gaining} is ${gaining_bah:,}/mo ({dep}).",
    ]
    if current and current_bah is not None:
        delta = gaining_bah - current_bah
        if delta > 0:
            lines.append(
                f"That is ${delta:,}/mo more than you currently receive at {current} "
                f"(${current_bah:,}/mo)."
            )
        elif delta < 0:
            lines.append(
                f"That is ${abs(delta):,}/mo less than you currently receive at {current} "
                f"(${current_bah:,}/mo)."
            )
        else:
            lines.append(
                f"That matches what you currently receive at {current} (${current_bah:,}/mo)."
            )
    return " ".join(lines)


def with_dependents_from_family_status(family_status: str) -> bool:
    """Single Soldiers use without-dependents BAH; married/with family use with-dependents."""
    status = (family_status or "").strip().lower()
    if status.startswith("single"):
        return False
    return True

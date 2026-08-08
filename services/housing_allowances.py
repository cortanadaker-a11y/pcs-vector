"""CONUS BAH + OCONUS OHA/COLA housing package lookups for calculator and PDF."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from services.bah_rates import (
    get_bah_effective_date,
    get_bah_rate,
    with_dependents_from_family_status,
)

_OCONUS_PATH = Path(__file__).resolve().parents[1] / "data" / "oconus_allowances_2026.json"


@lru_cache(maxsize=1)
def _load_oconus() -> dict[str, Any]:
    with _OCONUS_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def is_oconus_installation(name: str) -> bool:
    try:
        from services.installation_data import INSTALLATION_DATA, _canonical_installation_name

        key = _canonical_installation_name(name) or name
        meta = INSTALLATION_DATA.get(key) or {}
        return meta.get("theater") == "OCONUS"
    except Exception:
        return False


def get_oconus_record(name: str) -> dict[str, Any] | None:
    data = _load_oconus()
    if name in data.get("locations", {}):
        return data["locations"][name]
    try:
        from services.installation_data import _canonical_installation_name

        key = _canonical_installation_name(name)
        if key and key in data.get("locations", {}):
            return data["locations"][key]
    except Exception:
        pass
    return None


def get_housing_package(
    installation: str,
    pay_grade: str,
    *,
    with_dependents: bool = True,
) -> dict[str, Any]:
    """Return unified housing package: BAH or OHA + COLA when applicable."""
    dep_key = "with_dependents" if with_dependents else "without_dependents"
    oconus = get_oconus_record(installation)
    oconus_flag = is_oconus_installation(installation) or oconus is not None

    # --- Foreign OCONUS: OHA + COLA ---
    if oconus and oconus.get("housing_system") == "OHA":
        rent_bucket = (oconus.get("oha_rent_max_usd") or {}).get(dep_key) or {}
        rent_max = rent_bucket.get(pay_grade, rent_bucket.get("Other"))
        util = (oconus.get("oha_utility_usd") or {}).get(dep_key, 0) or 0
        cola_bucket = (oconus.get("cola_monthly_usd") or {}).get(dep_key) or {}
        cola = cola_bucket.get(pay_grade, cola_bucket.get("Other", 0)) or 0
        rent_max_i = int(rent_max) if rent_max is not None else None
        oha_total = (rent_max_i + int(util)) if rent_max_i is not None else None
        total = (oha_total + int(cola)) if oha_total is not None else None
        return {
            "installation": installation,
            "pay_grade": pay_grade,
            "with_dependents": with_dependents,
            "is_oconus": True,
            "housing_system": "OHA",
            "housing_label": "OHA (rent max + utilities)",
            "housing_monthly_usd": oha_total,
            "oha_rent_max_usd": rent_max_i,
            "oha_utility_usd": int(util),
            "cola_monthly_usd": int(cola),
            "cola_index": oconus.get("cola_index"),
            "total_monthly_usd": total,
            "locality": oconus.get("locality"),
            "country": oconus.get("country"),
            "currency_note": oconus.get("currency_note", ""),
            "effective_date": _load_oconus().get("effective_date", "2026-01-01"),
            "source": _load_oconus().get("source", ""),
            "found": rent_max_i is not None,
            "is_estimate": True,
            "disclaimer": (
                "OHA reimburses actual rent up to the locality max (plus utility allowance). "
                "COLA varies with pay, years of service, and dependents. Verify on LES / DTMO."
            ),
        }

    # --- Non-foreign OCONUS (HI/PR): BAH + COLA ---
    bah = get_bah_rate(installation, pay_grade, with_dependents=with_dependents)
    bah_amt = bah.get("monthly_usd")
    cola = 0
    cola_index = None
    housing_system = "BAH"
    locality = bah.get("mha")
    currency_note = ""
    disclaimer = "BAH rates from 2026 locality tables. Verify with finance / DTMO."
    is_est = bool(bah.get("is_estimate"))

    if oconus and oconus.get("housing_system") == "BAH_PLUS_COLA":
        cola_bucket = (oconus.get("cola_monthly_usd") or {}).get(dep_key) or {}
        cola = int(cola_bucket.get(pay_grade, cola_bucket.get("Other", 0)) or 0)
        cola_index = oconus.get("cola_index")
        housing_system = "BAH_PLUS_COLA"
        locality = oconus.get("locality") or locality
        currency_note = oconus.get("currency_note", "")
        disclaimer = (
            "This location uses BAH (not OHA) plus non-foreign OCONUS COLA. "
            "COLA is non-taxable and varies with pay/YOS/dependents. Verify on LES / DTMO."
        )
        oconus_flag = True

    total = None
    if bah_amt is not None:
        total = int(bah_amt) + int(cola)

    return {
        "installation": installation,
        "pay_grade": pay_grade,
        "with_dependents": with_dependents,
        "is_oconus": oconus_flag,
        "housing_system": housing_system,
        "housing_label": "BAH" if housing_system.startswith("BAH") else "OHA",
        "housing_monthly_usd": int(bah_amt) if bah_amt is not None else None,
        "oha_rent_max_usd": None,
        "oha_utility_usd": None,
        "cola_monthly_usd": int(cola),
        "cola_index": cola_index,
        "total_monthly_usd": total,
        "locality": locality,
        "country": (oconus or {}).get("country", "USA"),
        "currency_note": currency_note,
        "effective_date": bah.get("effective_date") or get_bah_effective_date(),
        "source": bah.get("source") or _load_oconus().get("source", ""),
        "found": bah_amt is not None,
        "is_estimate": is_est or (housing_system != "BAH" and cola > 0),
        "disclaimer": disclaimer,
    }


def compare_housing_packages(
    *,
    pay_grade: str,
    with_dependents: bool,
    gaining_installation: str,
    current_installation: str | None = None,
) -> dict[str, Any]:
    """Compare total housing package (BAH or OHA+COLA) between posts."""
    gaining = get_housing_package(
        gaining_installation, pay_grade, with_dependents=with_dependents
    )
    current = None
    if current_installation and current_installation not in (
        "— Select current post —",
        "— Skip comparison (gaining post only) —",
        "",
        None,
    ):
        current = get_housing_package(
            current_installation, pay_grade, with_dependents=with_dependents
        )

    g_tot = gaining.get("total_monthly_usd")
    c_tot = current.get("total_monthly_usd") if current else None
    delta = None
    if g_tot is not None and c_tot is not None:
        delta = int(g_tot) - int(c_tot)

    return {
        "pay_grade": pay_grade,
        "with_dependents": with_dependents,
        "gaining": gaining,
        "current": current,
        "monthly_delta_usd": delta,
        "annual_delta_usd": (delta * 12) if delta is not None else None,
        "effective_date": gaining.get("effective_date"),
    }


def format_housing_callout(
    *,
    rank_short: str,
    last_name: str,
    package: dict[str, Any],
    current_package: dict[str, Any] | None = None,
) -> str:
    """Plain-language housing + COLA summary for PDF / report."""
    who = f"{rank_short} {last_name}".strip() if last_name else rank_short or "Soldier"
    dep = "with dependents" if package.get("with_dependents") else "without dependents"
    install = package.get("installation") or "your new post"
    system = package.get("housing_system") or "BAH"

    housing = package.get("housing_monthly_usd")
    cola = int(package.get("cola_monthly_usd") or 0)
    total = package.get("total_monthly_usd")

    if housing is None:
        return (
            f"{who}: housing allowance for {install} is not fully on file — "
            f"verify OHA/BAH and COLA with finance ({dep})."
        )

    if system == "OHA":
        rent = package.get("oha_rent_max_usd")
        util = package.get("oha_utility_usd")
        parts = [
            f"{who}, at {install} you use OHA (not CONUS BAH) — planning max about "
            f"${housing:,}/mo ({dep})"
        ]
        if rent is not None and util is not None:
            parts[0] += f" (≈${int(rent):,} rent ceiling + ${int(util):,} utilities)"
        parts[0] += "."
        if cola:
            parts.append(f"Estimated COLA is about ${cola:,}/mo (index {package.get('cola_index', '—')}).")
            parts.append(f"Combined planning total ≈ ${int(total):,}/mo.")
        parts.append("OHA pays actual rent up to the max — confirm ceilings on DTMO / with housing.")
    elif system == "BAH_PLUS_COLA":
        parts = [
            f"{who}, your BAH for {install} is ${housing:,}/mo ({dep}).",
        ]
        if cola:
            parts.append(f"Estimated COLA is about ${cola:,}/mo (index {package.get('cola_index', '—')}).")
            parts.append(f"Combined BAH + COLA ≈ ${int(total):,}/mo.")
        else:
            parts.append("COLA may also apply — verify current index on your LES.")
    else:
        parts = [
            f"{who}, your BAH for {install} is ${housing:,}/mo ({dep}).",
        ]

    if current_package and current_package.get("total_monthly_usd") is not None and total is not None:
        cur_name = current_package.get("installation") or "your current post"
        cur_tot = int(current_package["total_monthly_usd"])
        delta = int(total) - cur_tot
        cur_h = current_package.get("housing_monthly_usd")
        cur_c = int(current_package.get("cola_monthly_usd") or 0)
        cur_label = "BAH/OHA+COLA"
        if current_package.get("housing_system") == "OHA":
            cur_detail = f"${cur_h:,}/mo OHA"
            if cur_c:
                cur_detail += f" + ${cur_c:,} COLA"
        elif current_package.get("housing_system") == "BAH_PLUS_COLA":
            cur_detail = f"${cur_h:,}/mo BAH"
            if cur_c:
                cur_detail += f" + ${cur_c:,} COLA"
        else:
            cur_detail = f"${cur_h:,}/mo BAH"

        if delta > 0:
            parts.append(
                f"That is ${delta:,}/mo more than your current package at {cur_name} "
                f"({cur_detail} ≈ ${cur_tot:,}/mo total)."
            )
        elif delta < 0:
            parts.append(
                f"That is ${abs(delta):,}/mo less than your current package at {cur_name} "
                f"({cur_detail} ≈ ${cur_tot:,}/mo total)."
            )
        else:
            parts.append(
                f"That matches your current total package at {cur_name} (≈ ${cur_tot:,}/mo)."
            )

    return " ".join(parts)


__all__ = [
    "compare_housing_packages",
    "format_housing_callout",
    "get_housing_package",
    "get_oconus_record",
    "is_oconus_installation",
    "with_dependents_from_family_status",
]

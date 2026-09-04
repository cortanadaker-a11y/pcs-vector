"""CONUS BAH + OCONUS OHA/COLA housing package lookups for calculator and PDF.

OCONUS COLA follows DoD FMR Vol 7A Ch 68:
  monthly ≈ spendable(annual base pay, # dependents) × (index − 100) / 100 / 12

OHA: rent ceiling + utility; without dependents = 90% rent + 75% utility (DTMO).
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from services.bah_rates import (
    get_bah_effective_date,
    get_bah_rate,
    with_dependents_from_family_status,
)

_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
_OCONUS_PATH = _DATA_DIR / "oconus_allowances_2026.json"
_COLA_TABLES_PATH = _DATA_DIR / "oconus_cola_tables_2026.json"

# Map form / UI pay grades onto 2026 base-pay table keys.
_GRADE_ALIASES = {
    "O-7+": "O-7",
    "O7+": "O-7",
    "Other": "E-5",
}


@lru_cache(maxsize=1)
def _load_oconus() -> dict[str, Any]:
    with _OCONUS_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def _load_cola_tables() -> dict[str, Any]:
    with _COLA_TABLES_PATH.open(encoding="utf-8") as fh:
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


def parse_years_of_service(value: Any, default: int = 4) -> int:
    """Normalize YOS from int, float, or UI labels like '4–5 years' / '20+'."""
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return max(0, min(40, int(value)))
    text = str(value).strip().lower()
    if "under" in text or text.startswith("<"):
        return 1
    if "20+" in text or "20 +" in text:
        return 20
    m = re.search(r"(\d+)", text)
    if m:
        return max(0, min(40, int(m.group(1))))
    return default


def resolve_num_dependents(
    *,
    with_dependents: bool | None = None,
    num_dependents: int | None = None,
    family_status: str | None = None,
    num_children: int | None = None,
) -> int:
    """Command-sponsored dependents for COLA (0–5+). Caps at 5 for the table."""
    if num_dependents is not None:
        return max(0, min(5, int(num_dependents)))

    if family_status is not None:
        status = (family_status or "").strip().lower()
        if status.startswith("single"):
            return 0
        kids = max(0, int(num_children or 0))
        # Spouse + children when married / with dependents
        return max(0, min(5, 1 + kids))

    if with_dependents is False:
        return 0
    if with_dependents is True:
        return 1
    return 0


def _normalize_pay_grade(pay_grade: str) -> str:
    g = (pay_grade or "E-5").strip()
    return _GRADE_ALIASES.get(g, g)


def _yos_pay_index(years_of_service: int, breakpoints: list[int]) -> int:
    yos = max(0, min(40, int(years_of_service)))
    if yos < 2:
        return 0
    if yos >= 40:
        return len(breakpoints) - 1
    idx = 0
    for i, bp in enumerate(breakpoints):
        if yos >= bp:
            idx = i
    return idx


def monthly_base_pay(pay_grade: str, years_of_service: int = 4) -> float | None:
    """2026 DFAS monthly basic pay for grade × YOS (for COLA spendable lookup)."""
    tables = _load_cola_tables()
    grade = _normalize_pay_grade(pay_grade)
    row = (tables.get("base_pay_monthly") or {}).get(grade)
    if not row:
        # Try without hyphen variants already handled; fall back E-5
        row = (tables.get("base_pay_monthly") or {}).get("E-5")
    if not row:
        return None
    bps = tables.get("yos_breakpoints") or [0, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    idx = _yos_pay_index(years_of_service, bps)
    if idx >= len(row):
        idx = len(row) - 1
    pay = float(row[idx] or 0)
    return pay if pay > 0 else None


def annual_spendable_income(annual_compensation: float, num_dependents: int) -> int:
    """Look up average annual spendable income (CY COLA table)."""
    tables = _load_cola_tables()
    deps = max(0, min(5, int(num_dependents)))
    annual = float(annual_compensation or 0)
    last = None
    for row in tables.get("spendable_table") or []:
        last = row
        if row["minIncome"] <= annual <= row["maxIncome"]:
            return int(row["spendable"][deps])
    if last:
        return int(last["spendable"][deps])
    return 0


def estimate_monthly_cola(
    pay_grade: str,
    *,
    years_of_service: int = 4,
    num_dependents: int = 0,
    cola_index: int | float | None = None,
    barracks_meal_card: bool = False,
) -> dict[str, Any]:
    """Estimate monthly OCONUS COLA from index + spendable income (planning)."""
    if cola_index is None:
        return {
            "cola_monthly_usd": 0,
            "cola_index": None,
            "annual_base_pay_usd": None,
            "annual_spendable_usd": None,
            "found": False,
            "note": "No COLA index for this location (or index at/below 100).",
        }

    index = float(cola_index)
    if index <= 100:
        return {
            "cola_monthly_usd": 0,
            "cola_index": int(index) if index == int(index) else index,
            "annual_base_pay_usd": None,
            "annual_spendable_usd": None,
            "found": True,
            "note": "Index at or below 100 — no COLA payable.",
        }

    monthly = monthly_base_pay(pay_grade, years_of_service)
    if monthly is None:
        return {
            "cola_monthly_usd": 0,
            "cola_index": int(index),
            "annual_base_pay_usd": None,
            "annual_spendable_usd": None,
            "found": False,
            "note": f"No base pay for {pay_grade} at {years_of_service} YOS.",
        }

    annual_pay = monthly * 12
    spendable = annual_spendable_income(annual_pay, num_dependents)
    cola = spendable * (index - 100) / 100.0 / 12.0
    if barracks_meal_card and int(num_dependents) == 0:
        cola *= 0.63
    cola_i = int(round(cola))
    if cola_i < 0:
        cola_i = 0

    return {
        "cola_monthly_usd": cola_i,
        "cola_index": int(index) if index == int(index) else index,
        "annual_base_pay_usd": int(round(annual_pay)),
        "monthly_base_pay_usd": round(monthly, 2),
        "annual_spendable_usd": spendable,
        "years_of_service": int(years_of_service),
        "num_dependents": max(0, min(5, int(num_dependents))),
        "found": True,
        "note": (
            f"Spendable ${spendable:,} × ({int(index)}−100)/100/12"
            + (" × 0.63 barracks" if barracks_meal_card and int(num_dependents) == 0 else "")
        ),
    }


def _oha_grade_key(pay_grade: str) -> str:
    g = _normalize_pay_grade(pay_grade)
    # OHA tables use O-1E style; map O-7+ already done
    if g in ("O-7", "O-8", "O-9", "O-10"):
        return "O-6"  # ceiling often tops at O-6 in locality tables; we store O-7+ = O-6
    return g


def _oha_amounts(
    oconus: dict[str, Any],
    pay_grade: str,
    *,
    with_dependents: bool,
) -> tuple[int | None, int | None, int | None]:
    """Return (rent_max_usd, util_usd, oha_total_usd)."""
    rent_local_map = oconus.get("oha_rent_local") or {}
    gkey = _oha_grade_key(pay_grade)
    rent_local = rent_local_map.get(gkey)
    if rent_local is None:
        rent_local = rent_local_map.get("E-5") or rent_local_map.get("Other")
    if rent_local is None:
        # Legacy shape: precomputed USD buckets
        dep_key = "with_dependents" if with_dependents else "without_dependents"
        bucket = (oconus.get("oha_rent_max_usd") or {}).get(dep_key) or {}
        rent_usd = bucket.get(pay_grade, bucket.get("Other"))
        util = (oconus.get("oha_utility_usd") or {}).get(dep_key)
        if rent_usd is None:
            return None, None, None
        util_i = int(util or 0)
        rent_i = int(rent_usd)
        return rent_i, util_i, rent_i + util_i

    fx = float(oconus.get("usd_per_local") or 0)
    util_local = float(oconus.get("oha_util_local") or 0)
    rent_f = float(oconus.get("oha_without_rent_factor") or 0.9)
    util_f = float(oconus.get("oha_without_util_factor") or 0.75)

    if not with_dependents:
        rent_local = float(rent_local) * rent_f
        util_local = util_local * util_f
    else:
        rent_local = float(rent_local)

    if fx <= 0:
        return None, None, None

    rent_usd = int(round(rent_local * fx))
    util_usd = int(round(util_local * fx))
    return rent_usd, util_usd, rent_usd + util_usd


def get_housing_package(
    installation: str,
    pay_grade: str,
    *,
    with_dependents: bool = True,
    years_of_service: int | str = 4,
    num_dependents: int | None = None,
    barracks_meal_card: bool = False,
) -> dict[str, Any]:
    """Return unified housing package: BAH or OHA + COLA when applicable."""
    yos = parse_years_of_service(years_of_service, default=4)
    if num_dependents is not None:
        deps_n = max(0, min(5, int(num_dependents)))
        with_dependents = deps_n > 0
    else:
        deps_n = resolve_num_dependents(with_dependents=with_dependents)
        with_dependents = deps_n > 0

    oconus = get_oconus_record(installation)
    oconus_flag = is_oconus_installation(installation) or oconus is not None
    root = _load_oconus()
    in_gov_q = bool(barracks_meal_card) and deps_n == 0
    barracks_note = (
        " Barracks + meal card: BAH/OHA is not paid in government quarters "
        "(BAH-Partial is a few dollars — shown as $0). Meal card replaces BAS. "
        "OCONUS COLA, if any, is reduced (~63%)."
    )

    # --- Foreign OCONUS: OHA + COLA ---
    if oconus and oconus.get("housing_system") == "OHA":
        rent_max, util, oha_total = _oha_amounts(
            oconus, pay_grade, with_dependents=with_dependents
        )
        cola_info = estimate_monthly_cola(
            pay_grade,
            years_of_service=yos,
            num_dependents=deps_n,
            cola_index=oconus.get("cola_index"),
            barracks_meal_card=barracks_meal_card,
        )
        cola = int(cola_info.get("cola_monthly_usd") or 0)
        found = oha_total is not None
        if in_gov_q and found:
            rent_max, util, oha_total = 0, 0, 0
        total = (oha_total + cola) if oha_total is not None else None
        disclaimer = (
            "OHA reimburses actual rent up to the locality max (plus utility allowance). "
            "Without dependents: 90% rent ceiling + 75% utility. "
            "COLA uses spendable income from grade, years of service, and # of dependents "
            "(DoD FMR Vol 7A Ch 68). Verify on LES / DTMO."
        )
        if in_gov_q:
            disclaimer += barracks_note
        return {
            "installation": installation,
            "pay_grade": pay_grade,
            "with_dependents": with_dependents,
            "num_dependents": deps_n,
            "years_of_service": yos,
            "is_oconus": True,
            "housing_system": "OHA",
            "housing_label": "Barracks (no OHA)" if in_gov_q else "OHA (rent max + utilities)",
            "housing_monthly_usd": oha_total,
            "oha_rent_max_usd": rent_max,
            "oha_utility_usd": util,
            "cola_monthly_usd": cola,
            "cola_index": oconus.get("cola_index"),
            "cola_detail": cola_info,
            "total_monthly_usd": total,
            "locality": oconus.get("locality"),
            "country": oconus.get("country"),
            "currency_note": oconus.get("currency_note", ""),
            "effective_date": oconus.get("oha_effective_date")
            or root.get("effective_date", "2026-01-01"),
            "source": root.get("source", ""),
            "found": found,
            "is_estimate": True,
            "in_government_quarters": in_gov_q,
            "disclaimer": disclaimer,
        }

    # --- Non-foreign OCONUS (HI/PR): BAH + COLA ---
    bah = get_bah_rate(installation, pay_grade, with_dependents=with_dependents)
    bah_amt = bah.get("monthly_usd")
    cola = 0
    cola_index = None
    cola_info: dict[str, Any] = {}
    housing_system = "BAH"
    locality = bah.get("mha")
    currency_note = ""
    disclaimer = "BAH rates from 2026 locality tables. Verify with finance / DTMO."
    is_est = bool(bah.get("is_estimate"))

    if oconus and oconus.get("housing_system") == "BAH_PLUS_COLA":
        cola_info = estimate_monthly_cola(
            pay_grade,
            years_of_service=yos,
            num_dependents=deps_n,
            cola_index=oconus.get("cola_index"),
            barracks_meal_card=barracks_meal_card,
        )
        cola = int(cola_info.get("cola_monthly_usd") or 0)
        cola_index = oconus.get("cola_index")
        housing_system = "BAH_PLUS_COLA"
        locality = oconus.get("locality") or locality
        currency_note = oconus.get("currency_note", "")
        disclaimer = (
            "This location uses BAH (not OHA) plus non-foreign OCONUS COLA. "
            "COLA = spendable income × (index−100)/100/12 (grade, YOS, # dependents). "
            "Verify on LES / DTMO."
        )
        oconus_flag = True
        is_est = True

    found = bah_amt is not None
    if in_gov_q and found:
        bah_amt = 0
        disclaimer += barracks_note

    total = None
    if bah_amt is not None:
        total = int(bah_amt) + int(cola)

    if in_gov_q:
        housing_label = "Barracks (no BAH)"
    elif housing_system.startswith("BAH"):
        housing_label = "BAH"
    else:
        housing_label = "OHA"

    return {
        "installation": installation,
        "pay_grade": pay_grade,
        "with_dependents": with_dependents,
        "num_dependents": deps_n,
        "years_of_service": yos,
        "is_oconus": oconus_flag,
        "housing_system": housing_system,
        "housing_label": housing_label,
        "housing_monthly_usd": int(bah_amt) if bah_amt is not None else None,
        "oha_rent_max_usd": None,
        "oha_utility_usd": None,
        "cola_monthly_usd": int(cola),
        "cola_index": cola_index,
        "cola_detail": cola_info,
        "total_monthly_usd": total,
        "locality": locality,
        "country": (oconus or {}).get("country", "USA"),
        "currency_note": currency_note,
        "effective_date": bah.get("effective_date") or get_bah_effective_date(),
        "source": bah.get("source") or root.get("source", ""),
        "found": found,
        "is_estimate": is_est,
        "in_government_quarters": in_gov_q,
        "disclaimer": disclaimer,
    }


def compare_housing_packages(
    *,
    pay_grade: str,
    with_dependents: bool = True,
    gaining_installation: str,
    current_installation: str | None = None,
    years_of_service: int | str = 4,
    num_dependents: int | None = None,
    barracks_meal_card: bool = False,
) -> dict[str, Any]:
    """Compare total housing package (BAH or OHA+COLA) between posts."""
    kwargs = dict(
        with_dependents=with_dependents,
        years_of_service=years_of_service,
        num_dependents=num_dependents,
        barracks_meal_card=barracks_meal_card,
    )
    gaining = get_housing_package(gaining_installation, pay_grade, **kwargs)
    current = None
    if current_installation and current_installation not in (
        "— Select current post —",
        "— Skip comparison (gaining post only) —",
        "",
        None,
    ):
        current = get_housing_package(current_installation, pay_grade, **kwargs)

    g_tot = gaining.get("total_monthly_usd")
    c_tot = current.get("total_monthly_usd") if current else None
    delta = None
    if g_tot is not None and c_tot is not None:
        delta = int(g_tot) - int(c_tot)

    return {
        "pay_grade": pay_grade,
        "with_dependents": with_dependents,
        "num_dependents": gaining.get("num_dependents"),
        "years_of_service": gaining.get("years_of_service"),
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
    deps_n = package.get("num_dependents")
    if deps_n is not None:
        dep = f"{int(deps_n)} dependent{'s' if int(deps_n) != 1 else ''}"
    else:
        dep = "with dependents" if package.get("with_dependents") else "without dependents"
    yos = package.get("years_of_service")
    yos_bit = f", {yos} YOS" if yos is not None else ""
    install = package.get("installation") or "your new post"
    system = package.get("housing_system") or "BAH"

    housing = package.get("housing_monthly_usd")
    cola = int(package.get("cola_monthly_usd") or 0)
    total = package.get("total_monthly_usd")

    if housing is None:
        return (
            f"{who}: housing allowance for {install} is not fully on file — "
            f"verify OHA/BAH and COLA with finance ({dep}{yos_bit})."
        )

    if package.get("in_government_quarters"):
        parts = [
            f"{who}, barracks + meal card at {install}: no BAH/OHA "
            f"(government quarters; {dep}{yos_bit})."
        ]
        if cola:
            parts.append(
                f"Estimated COLA is about ${cola:,}/mo (reduced barracks rate)."
            )
        parts.append("Confirm with housing and finance — BAH-Partial is a few dollars if anything.")
        if current_package and current_package.get("total_monthly_usd") is not None and total is not None:
            cur_name = current_package.get("installation") or "your current post"
            cur_tot = int(current_package["total_monthly_usd"])
            delta = int(total) - cur_tot
            if delta > 0:
                parts.append(
                    f"That is ${delta:,}/mo more than your current package at {cur_name} "
                    f"(≈ ${cur_tot:,}/mo total)."
                )
            elif delta < 0:
                parts.append(
                    f"That is ${abs(delta):,}/mo less than your current package at {cur_name} "
                    f"(≈ ${cur_tot:,}/mo total)."
                )
            else:
                parts.append(f"Same total package as {cur_name} (≈ ${cur_tot:,}/mo).")
        return " ".join(parts)

    if system == "OHA":
        rent = package.get("oha_rent_max_usd")
        util = package.get("oha_utility_usd")
        parts = [
            f"{who}, at {install} you use OHA (not CONUS BAH) — planning max about "
            f"${housing:,}/mo ({dep}{yos_bit})"
        ]
        if rent is not None and util is not None:
            parts[0] += f" (≈${int(rent):,} rent ceiling + ${int(util):,} utilities)"
        parts[0] += "."
        if cola:
            parts.append(
                f"Estimated COLA is about ${cola:,}/mo "
                f"(index {package.get('cola_index', '—')}, spendable-income formula)."
            )
            parts.append(f"Combined planning total ≈ ${int(total):,}/mo.")
        elif package.get("cola_index") is None:
            parts.append("No OCONUS COLA is currently indexed for this locality.")
        else:
            parts.append("Estimated COLA is $0 at the current index for your pay profile.")
        parts.append("OHA pays actual rent up to the max — confirm ceilings on DTMO / with housing.")
    elif system == "BAH_PLUS_COLA":
        parts = [
            f"{who}, your BAH for {install} is ${housing:,}/mo ({dep}{yos_bit}).",
        ]
        if cola:
            parts.append(
                f"Estimated COLA is about ${cola:,}/mo "
                f"(index {package.get('cola_index', '—')})."
            )
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
    "annual_spendable_income",
    "compare_housing_packages",
    "estimate_monthly_cola",
    "format_housing_callout",
    "get_housing_package",
    "get_oconus_record",
    "is_oconus_installation",
    "monthly_base_pay",
    "parse_years_of_service",
    "resolve_num_dependents",
    "with_dependents_from_family_status",
]

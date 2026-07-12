"""DITY/PPM planning estimates from rank weight allowance and move distance."""

from __future__ import annotations

from typing import Any

# JTR Table 5-1 style HHG weight allowances with dependents (lbs, CONUS planning).
HHG_WEIGHT_ALLOWANCE_LBS: dict[str, int] = {
    "E-1": 5000,
    "E-2": 5000,
    "E-3": 5000,
    "E-4": 7000,
    "E-5": 12000,
    "E-6": 13000,
    "E-7": 14000,
    "E-8": 15000,
    "E-9": 16000,
    "W-1": 13000,
    "W-2": 14000,
    "W-3": 15000,
    "W-4": 16000,
    "W-5": 17000,
    "O-1": 12000,
    "O-2": 13000,
    "O-3": 15000,
    "O-4": 16000,
    "O-5": 17500,
    "O-6": 18000,
    "O-7+": 18000,
    "Other": 12000,
}

# Calibrated gross GCC factor (lbs × miles × rate ≈ TMO ballpark for CONUS).
_GCC_FACTOR = 0.00062


def _estimate_expenses(miles: int, weight_lbs: int, *, full: bool) -> int:
    base = 2200 if full else 1600
    per_mile = 1.15 if full else 0.90
    weight_addon = int((weight_lbs / 1000) * (80 if full else 40))
    return int(base + (miles * per_mile) + weight_addon)


def _family_complexity(
    *,
    num_children: int,
    has_pets: bool,
    num_vehicles: str,
) -> tuple[int, str | None]:
    score = 0
    if num_children > 0:
        score += 2 if num_children >= 2 else 1
    if has_pets:
        score += 1
    if num_vehicles in ("2", "3+"):
        score += 1
    if score >= 3:
        return score, (
            "High family complexity (multiple children, pets, or second vehicle) — "
            "partial DITY usually beats full DITY on risk-adjusted net even when gross is lower."
        )
    if score >= 1:
        return score, (
            "Moderate family complexity — weigh partial DITY against full DITY load-out stress."
        )
    return score, None


def build_dity_estimate(
    pay_grade: str,
    miles: int | None,
    *,
    dity_interest: str,
    num_vehicles: str = "1",
    num_children: int = 0,
    has_pets: bool = False,
) -> dict[str, Any]:
    """Build a structured DITY/PPM estimate for the Grok prompt."""
    if dity_interest.startswith("No"):
        return {
            "applicable": False,
            "recommendation": "Government move — focus on TLE and cash-flow timing; skip PPM math.",
            "note": "No DITY estimate generated per user preference.",
        }

    if not miles or miles <= 0:
        return {
            "applicable": True,
            "authorized_weight_lbs": HHG_WEIGHT_ALLOWANCE_LBS.get(pay_grade, 12000),
            "note": "Distance unknown — request TMO PPM estimate before deciding.",
        }

    authorized = HHG_WEIGHT_ALLOWANCE_LBS.get(pay_grade, 12000)
    partial_weight = max(authorized // 2, 4000)
    full_weight = authorized

    def _scenario(weight: int, full: bool) -> dict[str, int | str]:
        gross = int(weight * miles * _GCC_FACTOR)
        expenses = _estimate_expenses(miles, weight, full=full)
        net = max(gross - expenses, 0)
        return {
            "weight_lbs": weight,
            "formula": f"({weight:,} lbs × {miles:,} mi × ${_GCC_FACTOR}) − ${expenses:,} expenses",
            "estimated_gross_payout_usd": gross,
            "estimated_expenses_usd": expenses,
            "estimated_net_usd": net,
        }

    partial = _scenario(partial_weight, full=False)
    full = _scenario(full_weight, full=True)

    complexity, complexity_note = _family_complexity(
        num_children=num_children,
        has_pets=has_pets,
        num_vehicles=num_vehicles,
    )

    wants_full = dity_interest.startswith("Yes")
    if wants_full:
        recommended = "full"
        reason = (
            "Full DITY maximizes weight allowance payout on this distance; "
            "verify with TMO and obtain empty/full weight tickets."
        )
    elif complexity >= 3:
        recommended = "partial"
        reason = (
            "Partial DITY (HHG only) preserves most net profit while avoiding "
            "full-truck family/Pet load-out risk on a long haul."
        )
    else:
        recommended = "partial" if partial["estimated_net_usd"] >= full["estimated_net_usd"] * 0.6 else "full"
        reason = (
            "Compare partial vs full using the formulas below; "
            "partial wins on flexibility when nets are close."
        )

    short_move_note = None
    if miles < 500 and partial["estimated_net_usd"] == 0:
        short_move_note = (
            f"At {miles} miles, PPM net is often near zero after expenses — "
            "government HHG may beat partial DITY on short CONUS hauls unless TMO shows positive net."
        )
        if recommended == "partial" and not wants_full:
            recommended = "government"
            reason = short_move_note

    return {
        "applicable": True,
        "authorized_weight_lbs": authorized,
        "distance_miles": miles,
        "partial_dity": partial,
        "full_dity": full,
        "recommended_mode": recommended,
        "recommendation_reason": reason,
        "short_move_note": short_move_note,
        "family_complexity_score": complexity,
        "family_complexity_note": complexity_note,
        "disclaimer": "Planning estimate only — confirm with transportation office PPM calculator before load-out.",
        "tle_note": "Claim max TLE days at gaining installation while housing finalizes.",
        "num_vehicles": num_vehicles,
    }
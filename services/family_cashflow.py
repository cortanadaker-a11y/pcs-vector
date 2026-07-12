"""PCS cash-flow bridge — income gaps, deposits, TLE, and net move cost."""

from __future__ import annotations

from typing import Any

# Planning assumptions for family cash-flow (conservative).
_WEEKLY_FAMILY_BASELINE_USD = 450
_SPOUSE_INCOME_LOSS_WEEKLY_EST: dict[str, int] = {
    "K-12 education / teaching": 900,
    "Healthcare / nursing": 1100,
    "Remote / work-from-home professional": 950,
    "Federal / government civilian": 850,
    "Retail / hospitality / service": 550,
    "Trades / skilled labor": 750,
    "Not currently working — seeking employment": 0,
    "Student / continuing education": 0,
    "Other field": 650,
}

_WEEKS_TO_FIRST_PAYCHECK: dict[str, tuple[int, int]] = {
    "K-12 education / teaching": (6, 10),
    "Healthcare / nursing": (4, 8),
    "Remote / work-from-home professional": (1, 2),
    "Federal / government civilian": (8, 14),
    "Not currently working — seeking employment": (6, 12),
}


def build_cashflow_bridge(
    *,
    spouse_career_field: str,
    bah_monthly: int,
    rent_low: int,
    rent_high: int,
    move_window: str,
    dity_estimate: dict[str, Any],
    num_children: int,
    has_pets: bool,
    max_monthly_budget: int,
) -> dict[str, Any]:
    """Estimate PCS cash-flow pressure for section 4."""
    loss_weekly = _SPOUSE_INCOME_LOSS_WEEKLY_EST.get(spouse_career_field, 650)
    weeks_range = _WEEKS_TO_FIRST_PAYCHECK.get(spouse_career_field, (4, 8))
    weeks_mid = sum(weeks_range) // 2

    target_rent = max_monthly_budget if max_monthly_budget > 0 else (rent_low + rent_high) // 2
    deposit = target_rent + (300 if has_pets else 0)
    tle_days = 10
    tle_est = 120 * tle_days  # ~$120/night planning figure

    spouse_gap = loss_weekly * weeks_mid if loss_weekly else 0
    move_baseline = _WEEKLY_FAMILY_BASELINE_USD * 4
    dity_net = 0
    if dity_estimate.get("applicable"):
        mode = dity_estimate.get("recommended_mode", "partial")
        bucket = dity_estimate.get(f"{mode}_dity", {})
        dity_net = int(bucket.get("estimated_net_usd", 0) or 0)

    four_week_delay = loss_weekly * 4 if loss_weekly else 0
    gross_outflow = deposit + tle_est + spouse_gap + move_baseline
    gross_inflow = dity_net + int(bah_monthly * 0.5)  # half-month BAH timing cushion
    net_pressure = max(gross_outflow - gross_inflow, 0)
    cushion = max(net_pressure + 1500, 2500)

    urgency = "high" if "30 days" in (move_window or "").lower() else "moderate"

    formula = (
        f"${deposit:,} deposit + ${tle_est:,} TLE + ${spouse_gap:,} spouse gap "
        f"− ${dity_net:,} DITY offset − ${int(bah_monthly * 0.5):,} half-month BAH "
        f"= ${net_pressure:,} net 30-day pressure"
    )

    return {
        "weeks_to_spouse_first_paycheck": {"low": weeks_range[0], "high": weeks_range[1]},
        "estimated_spouse_income_gap_usd": spouse_gap,
        "four_week_delay_cost_usd": four_week_delay,
        "estimated_deposit_and_fees_usd": deposit,
        "tle_days_authorized": tle_days,
        "estimated_tle_cost_usd": tle_est,
        "half_month_bah_cushion_usd": int(bah_monthly * 0.5),
        "dity_net_offset_usd": dity_net,
        "estimated_30_day_cash_pressure_usd": net_pressure,
        "recommended_cash_cushion_usd": cushion,
        "cash_pressure_formula": formula,
        "move_urgency": urgency,
        "insight": (
            f"Plan for {weeks_range[0]}–{weeks_range[1]} weeks before spouse income restarts "
            f"(~${spouse_gap:,} income gap at midpoint). A 4-week licensure delay alone costs "
            f"~${four_week_delay:,}. DITY net (~${dity_net:,}) and TLE offset pressure but do "
            f"not replace a ${deposit:,} deposit and ${tle_est:,} lodging window."
        ),
    }
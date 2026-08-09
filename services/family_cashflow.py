"""PCS cash-flow bridge — income gaps, deposits, TLE, and net move cost."""

from __future__ import annotations

from typing import Any

# Planning assumptions for family cash-flow (conservative).
_WEEKLY_FAMILY_BASELINE_USD = 450

# Timeline ranges only — never invent dollar income without user input.
_WEEKS_TO_FIRST_PAYCHECK: dict[str, tuple[int, int]] = {
    "K-12 education / teaching": (6, 10),
    "Healthcare / nursing": (4, 8),
    "Remote / work-from-home professional": (1, 2),
    "Federal / government civilian": (8, 14),
    "Not currently working — seeking employment": (6, 12),
    "Retail / hospitality / service": (4, 8),
    "Trades / skilled labor": (4, 8),
    "Student / continuing education": (0, 0),
    "N/A — single Soldier": (0, 0),
}


def _parse_optional_monthly_income(value: Any) -> int | None:
    """Return positive monthly USD, or None if blank / zero / invalid."""
    if value is None or value == "":
        return None
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        return None
    if n <= 0:
        return None
    return n


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
    spouse_monthly_income_usd: Any = None,
) -> dict[str, Any]:
    """Estimate PCS cash-flow pressure for section 4.

    Spouse income gap dollars are only computed when the user provides
    approximate monthly spouse income. Otherwise language stays qualitative.
    """
    weeks_range = _WEEKS_TO_FIRST_PAYCHECK.get(spouse_career_field, (4, 8))
    weeks_low, weeks_high = weeks_range
    weeks_mid = sum(weeks_range) // 2 if weeks_high else 0

    provided_monthly = _parse_optional_monthly_income(spouse_monthly_income_usd)
    spouse_income_provided = provided_monthly is not None

    if spouse_income_provided and weeks_mid > 0:
        # Monthly income → weekly × midpoint weeks until first paycheck
        loss_weekly = int(round(provided_monthly / 4.33))
        spouse_gap = loss_weekly * weeks_mid
        four_week_delay = loss_weekly * 4
    else:
        loss_weekly = 0
        spouse_gap = 0
        four_week_delay = 0

    target_rent = max_monthly_budget if max_monthly_budget > 0 else (rent_low + rent_high) // 2
    deposit = target_rent + (300 if has_pets else 0)
    tle_days = 10
    tle_est = 120 * tle_days  # ~$120/night planning figure

    move_baseline = _WEEKLY_FAMILY_BASELINE_USD * 4
    dity_net = 0
    if dity_estimate.get("applicable"):
        mode = dity_estimate.get("recommended_mode", "partial")
        if mode in ("partial", "full"):
            bucket = dity_estimate.get(f"{mode}_dity", {})
            dity_net = int(bucket.get("estimated_net_usd", 0) or 0)

    # Cash pressure without invented spouse dollars
    gross_outflow = deposit + tle_est + spouse_gap + move_baseline
    gross_inflow = dity_net + int(bah_monthly * 0.5)
    net_pressure = max(gross_outflow - gross_inflow, 0)
    cushion = max(net_pressure + 1500, 2500)

    urgency = "high" if "30 days" in (move_window or "").lower() else "moderate"

    if weeks_high == 0:
        gap_timing = "no typical spouse paycheck gap for this situation"
        gap_language = (
            "No spouse employment income gap is assumed for this family situation."
        )
    else:
        gap_timing = f"{weeks_low}–{weeks_high} weeks before a typical first paycheck"
        if spouse_income_provided:
            gap_language = (
                f"Using the spouse income you entered (~${provided_monthly:,}/mo), "
                f"plan for about {weeks_low}–{weeks_high} weeks without that paycheck "
                f"(roughly **${spouse_gap:,}** at the midpoint of that window). "
                f"A four-week delay alone is about **${four_week_delay:,}**."
            )
        else:
            gap_language = (
                f"Expect a **{weeks_low}–{weeks_high} week** gap before the first spouse paycheck "
                f"during licensing / job search / onboarding. "
                f"No dollar amount was provided for spouse income, so this plan does **not** invent a gap figure — "
                f"plan for a meaningful shortfall until work restarts."
            )

    if spouse_income_provided:
        formula = (
            f"${deposit:,} deposit + ${tle_est:,} TLE + ${spouse_gap:,} spouse gap "
            f"(from ~${provided_monthly:,}/mo) − ${dity_net:,} DITY offset "
            f"− ${int(bah_monthly * 0.5):,} half-month BAH = ${net_pressure:,} net 30-day pressure"
        )
        plain_english = (
            f"In the first 30 days, plan on roughly ${deposit:,} for deposit and move-in fees and "
            f"about ${tle_est:,} for Temporary Lodging Expense (TLE) lodging. "
            f"{gap_language} "
            f"Partial DITY (if you run it) offsets about ${dity_net:,}, "
            f"and half a month of BAH timing (~${int(bah_monthly * 0.5):,}) helps — "
            f"net pressure lands around **${net_pressure:,}**. Hold **${cushion:,}** liquid before you leave."
        )
        insight = (
            f"Plan for {gap_timing} "
            f"(~${spouse_gap:,} at midpoint using the income you entered). "
            f"DITY net (~${dity_net:,}) and TLE planning do not replace a ${deposit:,} deposit "
            f"and ${tle_est:,} lodging window."
        )
    else:
        formula = (
            f"${deposit:,} deposit + ${tle_est:,} TLE + spouse gap (not quantified — no income provided) "
            f"− ${dity_net:,} DITY offset − ${int(bah_monthly * 0.5):,} half-month BAH "
            f"= ${net_pressure:,} base pressure (excluding unstated spouse income)"
        )
        plain_english = (
            f"In the first 30 days, plan on roughly ${deposit:,} for deposit and move-in fees and "
            f"about ${tle_est:,} for Temporary Lodging Expense (TLE) lodging. "
            f"{gap_language} "
            f"Partial DITY (if you run it) offsets about ${dity_net:,}, "
            f"and half a month of BAH timing (~${int(bah_monthly * 0.5):,}) helps. "
            f"**Base** cash pressure without a stated spouse income figure is around **${net_pressure:,}** "
            f"(plus whatever you need to cover the paycheck gap). "
            f"Hold at least **${cushion:,}** liquid before you leave, and add more if spouse income will pause."
        )
        insight = (
            f"Plan for {gap_timing}. "
            f"No spouse monthly income was provided — do not invent a dollar gap. "
            f"Known fixed costs include ~${deposit:,} deposit and ~${tle_est:,} TLE; "
            f"DITY net (~${dity_net:,}) may offset some pressure."
        )

    return {
        "weeks_to_spouse_first_paycheck": {"low": weeks_low, "high": weeks_high},
        "spouse_monthly_income_usd_provided": provided_monthly,
        "spouse_income_provided": spouse_income_provided,
        "estimated_spouse_income_gap_usd": spouse_gap if spouse_income_provided else None,
        "four_week_delay_cost_usd": four_week_delay if spouse_income_provided else None,
        "spouse_gap_language": gap_language,
        "do_not_invent_spouse_income_dollars": not spouse_income_provided,
        "estimated_deposit_and_fees_usd": deposit,
        "tle_days_authorized": tle_days,
        "estimated_tle_cost_usd": tle_est,
        "half_month_bah_cushion_usd": int(bah_monthly * 0.5),
        "dity_net_offset_usd": dity_net,
        "estimated_30_day_cash_pressure_usd": net_pressure,
        "recommended_cash_cushion_usd": cushion,
        "cash_pressure_formula": formula,
        "cash_pressure_plain_english": plain_english,
        "move_urgency": urgency,
        "insight": insight,
    }

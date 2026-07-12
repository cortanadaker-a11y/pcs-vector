"""Post-process Grok output — strip leaked internal field names."""

from __future__ import annotations

import re

# Patterns → plain-language replacements when models leak payload keys.
_REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"family_cashflow_bridge\.cash_pressure_formula", re.I), "the 30-day cash pressure math"),
    (re.compile(r"cash_pressure_formula", re.I), "30-day cash pressure"),
    (re.compile(r"soldier_context\.negotiation_tip", re.I), "lease negotiation leverage"),
    (re.compile(r"negotiation_tip", re.I), "lease negotiation leverage"),
    (re.compile(r"command_briefing_prompt", re.I), "commander brief line"),
    (re.compile(r"decision_context\.\w+", re.I), ""),
    (re.compile(r"value_context\.\w+", re.I), ""),
    (re.compile(r"soldier_context\.\w+", re.I), ""),
    (re.compile(r"\bLeverage_programs\b"), "ACS and military spouse programs"),
    (re.compile(r"\bleverage_programs\b"), "ACS and military spouse programs"),
    (re.compile(r"\bcritical path\b", re.I), "main priority"),
    (re.compile(r"\bparallel-tracking\b", re.I), "running in parallel"),
    (re.compile(r"\bsequenced task\b", re.I), "timed sequence"),
    (re.compile(r"\bsequenced process\b", re.I), "step-by-step plan"),
    (re.compile(r"\bsequencing\b", re.I), "timing"),
    (re.compile(r"\bsequenced\b", re.I), "timed"),
    (re.compile(r"  +"), " "),
)


def sanitize_report(report: str) -> str:
    """Remove or rewrite common internal-token leaks in generated reports."""
    text = report
    for pattern, repl in _REPLACEMENTS:
        text = pattern.sub(repl, text)
    return text.strip()
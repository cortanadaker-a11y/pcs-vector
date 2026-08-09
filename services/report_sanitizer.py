"""Post-process Grok output — strip leaks and expand first-use acronyms."""

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
    (re.compile(r"\bLeverage_programs\b"), "Army Community Service (ACS) and military spouse programs"),
    (re.compile(r"\bleverage_programs\b"), "Army Community Service (ACS) and military spouse programs"),
    (re.compile(r"\bcritical path\b", re.I), "main priority"),
    (re.compile(r"\bparallel-tracking\b", re.I), "running in parallel"),
    (re.compile(r"\bsequenced task\b", re.I), "timed sequence"),
    (re.compile(r"\bsequenced process\b", re.I), "step-by-step plan"),
    (re.compile(r"\bsequencing\b", re.I), "timing"),
    (re.compile(r"\bsequenced\b", re.I), "timed"),
    (
        re.compile(
            r"Move is cost-optimized via on-post/TLE/DITY(?:\s+(?:timing|sequencing))?"
            r"[^.\"']*",
            re.I,
        ),
        "Housing and Temporary Lodging Expense (TLE) are locked to protect the family budget",
    ),
    (
        re.compile(
            r"primary risk is housing/childcare timing(?:; mitigation in place before reporting date)?",
            re.I,
        ),
        "family housing and settling timeline are the main risks, with mitigations before report date",
    ),
    (re.compile(r"  +"), " "),
)

# Expand bare acronyms on first use only (skip if already expanded nearby).
# Order matters: longer / more specific first.
_ACRONYM_EXPANSIONS: tuple[tuple[str, str], ...] = (
    ("MyCAA", "Military Spouse Career Advancement Account (MyCAA)"),
    ("MSEP", "Military Spouse Employment Partnership (MSEP)"),
    ("DoDEA", "Department of Defense Education Activity (DoDEA)"),
    ("DEERS", "Defense Enrollment Eligibility Reporting System (DEERS)"),
    ("EFMP", "Exceptional Family Member Program (EFMP)"),
    ("OHA", "Overseas Housing Allowance (OHA)"),
    ("COLA", "Cost of Living Allowance (COLA)"),
    ("BAH", "Basic Allowance for Housing (BAH)"),
    ("DLA", "Dislocation Allowance (DLA)"),
    ("HHG", "Household Goods (HHG)"),
    ("PPM", "Personally Procured Move (PPM)"),
    ("DITY", "Do-It-Yourself move (DITY)"),
    ("TLE", "Temporary Lodging Expense (TLE)"),
    ("TLA", "Temporary Lodging Allowance (TLA)"),
    ("TMO", "Transportation Management Office (TMO)"),
    ("LES", "Leave and Earnings Statement (LES)"),
    ("ACS", "Army Community Service (ACS)"),
    ("CDC", "Child Development Center (CDC)"),
    ("FCC", "Family Child Care (FCC)"),
    ("NAF", "Non-Appropriated Fund (NAF)"),
    ("PCS", "Permanent Change of Station (PCS)"),
)


def _already_expanded(text: str, full_phrase: str, pos: int) -> bool:
    """True if the expansion already appears before this position."""
    window = text[max(0, pos - 80) : pos + len(full_phrase) + 20]
    # e.g. "Army Community Service (ACS)" already present
    return full_phrase in text[: pos + 5] or full_phrase.split(" (")[0] in window


def expand_acronyms_first_use(text: str) -> str:
    """Replace first bare use of each acronym with Full Name (ACRONYM)."""
    result = text
    for acronym, expansion in _ACRONYM_EXPANSIONS:
        # Skip if expansion already exists anywhere
        if expansion in result:
            continue
        # Match bare acronym as whole word, not already inside parentheses form
        pattern = re.compile(rf"(?<![A-Za-z(]){re.escape(acronym)}(?![A-Za-z)])")
        m = pattern.search(result)
        if not m:
            continue
        if _already_expanded(result, expansion, m.start()):
            continue
        result = result[: m.start()] + expansion + result[m.end() :]
    return result


def ensure_checklist_essentials(text: str) -> str:
    """If section 8 lacks mailing-address or insurance items, append them."""
    # Only touch section 8 content
    if "## 8." not in text:
        return text
    parts = text.split("## 8.", 1)
    head, sec8 = parts[0], parts[1]
    lower = sec8.lower()
    additions: list[str] = []
    if not re.search(r"mail(ing)?\s+address|change of address|usps", lower):
        additions.append(
            "Update your mailing address (USPS change-of-address, bank, DEERS/ID card office, "
            "and any subscriptions) within the first week after you have a stable address."
        )
    if not re.search(r"insurance|renters?\s+insur|auto\s+insur", lower):
        additions.append(
            "Update or shop auto and renters insurance for the new state/post, and cancel "
            "old policies on the correct effective date so you are never double-paying or uncovered."
        )
    if not additions:
        return text

    # Insert before spouse-share closing paragraph if present
    lines = sec8.splitlines()
    insert_at = len(lines)
    for i, line in enumerate(lines):
        low = line.lower()
        if (
            "for both of us on the move" in low
            or "we're targeting" in low
            or "we're in this together" in low
            or "shared playbook" in low
        ):
            insert_at = i
            break

    # Find last numbered item to continue numbering
    last_n = 0
    for line in lines[:insert_at]:
        m = re.match(r"^(\d+)[\.\)]\s+", line.strip())
        if m:
            last_n = max(last_n, int(m.group(1)))

    new_lines = []
    for add in additions:
        last_n += 1
        new_lines.append(f"{last_n}. {add}")

    lines = lines[:insert_at] + new_lines + ([""] if insert_at < len(lines) else []) + lines[insert_at:]
    return head + "## 8." + "\n".join(lines)


def sanitize_report(report: str) -> str:
    """Remove leaks, expand first-use acronyms, ensure checklist essentials."""
    text = report
    for pattern, repl in _REPLACEMENTS:
        text = pattern.sub(repl, text)
    text = expand_acronyms_first_use(text)
    text = ensure_checklist_essentials(text)
    return text.strip()

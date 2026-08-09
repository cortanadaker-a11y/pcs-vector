"""Professional PDF export for PCS Vector reports — Soldier-first, plain English."""

from __future__ import annotations

import html
import io
import re
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Brand palette (matches PCS Vector web app — forest / stone)
NAVY = colors.HexColor("#2a4a3f")
NAVY_LIGHT = colors.HexColor("#3d6556")
ACCENT = colors.HexColor("#5b8f72")
ACCENT_SOFT = colors.HexColor("#e8f3ec")
SLATE = colors.HexColor("#454540")
MUTED = colors.HexColor("#6b6b66")
BORDER = colors.HexColor("#e0ddd6")
TABLE_HEADER_BG = colors.HexColor("#f0f7f3")
TABLE_ALT_BG = colors.HexColor("#faf9f7")
CALLOUT_AMBER_BG = colors.HexColor("#faf6ef")
CALLOUT_AMBER_EDGE = colors.HexColor("#9a8468")
CALLOUT_GATE_BG = colors.HexColor("#eef6f1")
CALLOUT_NAVY_BG = NAVY
WHITE = colors.white

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.65 * inch
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN  # ~7.2"

SECTION_PATTERN = re.compile(r"^##\s+(\d+)\.\s+(.+)$")
BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")
ITALIC_PATTERN = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
TABLE_SEP_PATTERN = re.compile(r"^\|[\s\-:|]+\|$")

# After which section numbers we inject insight callouts
_INJECT_AFTER_SECTION: dict[int, list[str]] = {
    1: ["tle_tla", "bah_start"],  # lodging + pay-start timing
    3: ["housing_allowances"],  # after housing strategy
    4: ["hhg_vs_ppm", "cash_cushion"],  # HHG/PPM + cash
    5: ["decision_discipline"],  # reinforce gates during first 30 days
}


class PDFGenerationError(Exception):
    """Raised when PDF generation fails."""


def generate_pdf_report(
    markdown_content: str,
    metadata: dict[str, Any] | None = None,
) -> bytes:
    """Convert a markdown PCS report into a styled PDF byte stream."""
    if not markdown_content or not markdown_content.strip():
        raise PDFGenerationError("Report content is empty — nothing to export.")

    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=MARGIN,
            rightMargin=MARGIN,
            topMargin=MARGIN + 0.32 * inch,
            bottomMargin=MARGIN + 0.28 * inch,
            title="PCS Vector Strategic Plan",
            author="PCS Vector",
        )

        styles = _build_styles()
        story: list[Any] = []
        report_date = datetime.now().strftime("%B %d, %Y")
        meta = metadata or {}

        story.extend(_build_cover_block(markdown_content, meta, report_date, styles))
        story.append(Spacer(1, 0.14 * inch))
        # Standard plain-English glossary strip (always present)
        story.append(_build_quick_reference_strip(meta, styles))
        story.append(Spacer(1, 0.16 * inch))
        story.extend(
            _parse_markdown_to_flowables(markdown_content, styles, metadata=meta)
        )
        story.append(Spacer(1, 0.12 * inch))
        story.append(_build_footer_disclaimer(styles))

        doc.build(
            story,
            onFirstPage=lambda c, d: _draw_page_frame(c, d, report_date),
            onLaterPages=lambda c, d: _draw_page_frame(c, d, report_date),
        )
        return buffer.getvalue()
    except PDFGenerationError:
        raise
    except Exception as exc:
        raise PDFGenerationError(f"Failed to generate PDF: {exc}") from exc


def _build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "PCSTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=NAVY,
            spaceAfter=6,
            alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "PCSSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=SLATE,
            spaceAfter=4,
        ),
        "section": ParagraphStyle(
            "PCSSection",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "PCSBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.2,
            textColor=SLATE,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "PCSBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=SLATE,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=3,
        ),
        "numbered": ParagraphStyle(
            "PCSNumbered",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=SLATE,
            leftIndent=12,
            spaceAfter=3,
        ),
        "table_cell": ParagraphStyle(
            "PCSTableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=SLATE,
        ),
        "table_header": ParagraphStyle(
            "PCSTableHeader",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11.5,
            textColor=NAVY,
        ),
        "meta_label": ParagraphStyle(
            "PCSMetaLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=NAVY,
        ),
        "meta_value": ParagraphStyle(
            "PCSMetaValue",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=SLATE,
        ),
        "callout_title": ParagraphStyle(
            "PCSCalloutTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=NAVY,
            spaceAfter=3,
        ),
        "callout_body": ParagraphStyle(
            "PCSCalloutBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=SLATE,
        ),
        "callout_title_light": ParagraphStyle(
            "PCSCalloutTitleLight",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=WHITE,
            spaceAfter=3,
        ),
        "callout_body_light": ParagraphStyle(
            "PCSCalloutBodyLight",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#e8f0eb"),
        ),
        "howto": ParagraphStyle(
            "PCSHowTo",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=SLATE,
        ),
        "howto_label": ParagraphStyle(
            "PCSHowToLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=NAVY,
            spaceAfter=2,
        ),
        "gate": ParagraphStyle(
            "PCSGate",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=NAVY,
        ),
        "gate_label": ParagraphStyle(
            "PCSGateLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=NAVY,
            spaceAfter=2,
        ),
        "spouse_share": ParagraphStyle(
            "PCSSpouseShare",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13,
            textColor=NAVY,
        ),
        "disclaimer": ParagraphStyle(
            "PCSDisclaimer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
        ),
    }


# ── Reusable insight callout boxes ──────────────────────────────────────────


def _make_callout(
    title: str,
    body_html: str,
    styles: dict[str, ParagraphStyle],
    *,
    width: float,
    variant: str = "green",
) -> Table:
    """Styled insight box. variant: green | amber | navy."""
    if variant == "navy":
        bg, edge = CALLOUT_NAVY_BG, CALLOUT_NAVY_BG
        t_style, b_style = styles["callout_title_light"], styles["callout_body_light"]
    elif variant == "amber":
        bg, edge = CALLOUT_AMBER_BG, CALLOUT_AMBER_EDGE
        t_style, b_style = styles["callout_title"], styles["callout_body"]
    else:
        bg, edge = ACCENT_SOFT, ACCENT
        t_style, b_style = styles["callout_title"], styles["callout_body"]

    inner = [
        [Paragraph(_escape(title), t_style)],
        [Paragraph(body_html, b_style)],
    ]
    box = Table(inner, colWidths=[width])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.8, edge),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
                ("TOPPADDING", (0, 1), (-1, -1), 1),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return box


def _callout_tle_tla(
    styles: dict[str, ParagraphStyle],
    width: float,
    *,
    housing_system: str | None = None,
    to_installation: str | None = None,
) -> Table:
    """Standard TLE vs TLA plain-English callout (always on the PDF)."""
    oconus = (housing_system or "") in ("OHA", "BAH_PLUS_COLA")
    loc = (to_installation or "").lower()
    if any(x in loc for x in ("korea", "germany", "japan", "italy", "hawaii", "hi", "pr", "camp ", "usag")):
        oconus = True

    if oconus:
        body = (
            "<b>Your move looks OCONUS-related — think TLA, not TLE.</b><br/><br/>"
            "<b>TLA</b> (Temporary Lodging <i>Allowance</i>) — hotel money while you "
            "settle <b>overseas</b> (and some non-foreign OCONUS). Rules and day limits "
            "differ by country; work it through finance / housing before you book long stays.<br/><br/>"
            "<b>TLE</b> (Temporary Lodging <i>Expense</i>) — the CONUS (stateside) version. "
            "Usually shorter (often ~10 days). Do <b>not</b> claim TLE for an OCONUS lodging "
            "period just because the acronym looks similar.<br/><br/>"
            "<b>Rule of thumb:</b> Stateside hotel during PCS → TLE. Overseas hotel → TLA."
        )
        title = "KNOW THIS: TLA vs TLE (OCONUS)"
    else:
        body = (
            "<b>TLE</b> (Temporary Lodging <i>Expense</i>) — hotel money for "
            "<b>CONUS</b> moves (stateside). Usually up to about 10 days; claim through "
            "finance with receipts. This is <b>not</b> BAH.<br/><br/>"
            "<b>TLA</b> (Temporary Lodging <i>Allowance</i>) — hotel money for "
            "<b>OCONUS</b> moves (overseas, and some non-foreign OCONUS posts). "
            "Different rule set and often a different day window.<br/><br/>"
            "<b>Rule of thumb:</b> CONUS = TLE. Overseas = TLA. Mixing them up is a "
            "common claim rejection — ask finance which one applies to <i>your</i> orders."
        )
        title = "KNOW THIS: TLE vs TLA"
    return _make_callout(title, body, styles, width=width, variant="amber")


def _callout_housing_allowances(
    metadata: dict[str, Any],
    styles: dict[str, ParagraphStyle],
    width: float,
) -> Table:
    """BAH / OHA / COLA in plain English, tuned to this Soldier's system."""
    system = str(metadata.get("housing_system") or "BAH")
    if system == "OHA":
        body = (
            "<b>OHA</b> (Overseas Housing Allowance) pays your <b>actual rent</b> "
            "up to a ceiling for your grade and location, plus a utility allowance. "
            "It is not a flat BAH-style payment — keep the lease and receipts.<br/><br/>"
            "<b>COLA</b> helps with higher grocery and daily costs. It changes with "
            "pay grade, years of service, number of dependents, and the local index.<br/><br/>"
            "Verify current ceilings on your LES and with housing / finance."
        )
        title = "YOUR POST: OHA + COLA (not BAH)"
    elif system == "BAH_PLUS_COLA":
        body = (
            "<b>BAH</b> covers housing (flat rate by zip and dependents). "
            "Hawaii / some territories also pay <b>COLA</b> for higher living costs — "
            "separate from BAH, non-taxable overseas COLA rules apply.<br/><br/>"
            "This is <b>not</b> foreign OHA. You do not submit rent receipts for BAH."
        )
        title = "YOUR POST: BAH + COLA"
    else:
        body = (
            "<b>BAH</b> (Basic Allowance for Housing) is a <b>flat monthly</b> amount "
            "based on your duty zip, pay grade, and with/without dependents. "
            "You keep the difference if rent is lower — and cover the gap if higher.<br/><br/>"
            "BAH is not the same as TLE (hotel). See the <b>BAH start vs report date</b> "
            "box for when money actually hits."
        )
        title = "KNOW THIS: BAH in plain English"
    return _make_callout(title, body, styles, width=width, variant="green")


def _callout_bah_start(styles: dict[str, ParagraphStyle], width: float) -> Table:
    """BAH / OHA start date vs report date — common finance confusion."""
    body = (
        "<b>Report date</b> = the day you must be at the new unit (on your orders).<br/><br/>"
        "<b>BAH / OHA start</b> = when housing money begins on your LES — often tied to "
        "departure from the old duty station, arrival, or when you stop government "
        "quarters, depending on your situation.<br/><br/>"
        "These are <b>not always the same day</b>. A gap can leave you covering rent or "
        "hotels out of pocket. Ask finance: <i>“When does my BAH/OHA start relative to "
        "my report date and TLE/TLA?”</i> before you sign a lease."
    )
    return _make_callout(
        "KNOW THIS: BAH/OHA start vs report date",
        body,
        styles,
        width=width,
        variant="amber",
    )


def _callout_hhg_vs_ppm(styles: dict[str, ParagraphStyle], width: float) -> Table:
    """Government HHG vs PPM/DITY with weight-ticket discipline."""
    body = (
        "<b>Government HHG</b> — the government (or contracted movers) packs and hauls "
        "your household goods. Lower stress; less control of dates; you do not get a "
        "PPM incentive payment.<br/><br/>"
        "<b>PPM / DITY</b> — you move the goods (yourself or a hired truck). The "
        "government may pay you based on <b>authorized weight × distance</b>. That is "
        "not free money until costs are covered.<br/><br/>"
        "<b>Weight tickets (required for PPM):</b> empty truck + loaded truck at "
        "certified scales. No tickets → no full payment. Run real numbers with "
        "<b>TMO</b> before you commit — short moves often favor government HHG."
    )
    return _make_callout(
        "KNOW THIS: HHG vs PPM + weight tickets",
        body,
        styles,
        width=width,
        variant="green",
    )


def _callout_dity_ppm(styles: dict[str, ParagraphStyle], width: float) -> Table:
    """Legacy alias — prefer hhg_vs_ppm for new injections."""
    return _callout_hhg_vs_ppm(styles, width)


def _callout_cash_cushion(styles: dict[str, ParagraphStyle], width: float) -> Table:
    body = (
        "Plan cash for: deposits, first month's rent, TLE/TLA hotels, "
        "food until pay hits, pet fees, and any spouse income gap.<br/><br/>"
        "The report's cash-pressure number is a planning target — "
        "not a guarantee. Finance office rules still apply."
    )
    return _make_callout("CASH BEFORE YOU LEAVE", body, styles, width=width, variant="amber")


def _callout_decision_discipline(styles: dict[str, ParagraphStyle], width: float) -> Table:
    body = (
        "Every <b>Decision Gate</b> in this plan is a hard stop — not a suggestion. "
        "If the gate fails (housing not locked, childcare open, license not filed), "
        "use the backup in the gate line the same day. Do not hope it works out.<br/><br/>"
        "Soldier owns orders, finance, TMO, and unit in-processing. "
        "Spouse owns job/school/childcare track when that is the family plan. "
        "Talk once a day for the first two weeks so tasks do not collide."
    )
    return _make_callout(
        "HOW TO USE THE GATES",
        body,
        styles,
        width=width,
        variant="green",
    )


def _get_insight_callout(
    key: str,
    metadata: dict[str, Any],
    styles: dict[str, ParagraphStyle],
    width: float,
) -> Table | None:
    if key == "tle_tla":
        return _callout_tle_tla(
            styles,
            width,
            housing_system=str(metadata.get("housing_system") or ""),
            to_installation=str(metadata.get("to_installation") or ""),
        )
    if key == "housing_allowances":
        return _callout_housing_allowances(metadata, styles, width)
    if key == "bah_start":
        return _callout_bah_start(styles, width)
    if key in ("hhg_vs_ppm", "dity_ppm"):
        return _callout_hhg_vs_ppm(styles, width)
    if key == "cash_cushion":
        return _callout_cash_cushion(styles, width)
    if key == "decision_discipline":
        return _callout_decision_discipline(styles, width)
    return None


def _build_quick_reference_strip(
    metadata: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> Table:
    """Two side-by-side callouts under the cover: TLE/TLA + housing type."""
    half = (CONTENT_WIDTH - 0.12 * inch) / 2
    left = _callout_tle_tla(
        styles,
        half,
        housing_system=str(metadata.get("housing_system") or ""),
        to_installation=str(metadata.get("to_installation") or ""),
    )
    right = _callout_housing_allowances(metadata, styles, half)
    row = Table([[left, right]], colWidths=[half, half])
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 6),
                ("LEFTPADDING", (1, 0), (1, 0), 6),
                ("RIGHTPADDING", (1, 0), (1, 0), 0),
            ]
        )
    )
    return row


def _build_gate_box(text: str, styles: dict[str, ParagraphStyle]) -> Table:
    """Decision gate as a full-width highlighted card."""
    cleaned = re.sub(r"^(\*\*)?gate:\s*", "", text.strip(), flags=re.I)
    cleaned = re.sub(r"(?i)\bgate:\s*", "", cleaned, count=1)
    inner = [
        [Paragraph("DECISION GATE — do not skip", styles["gate_label"])],
        [Paragraph(_format_inline(cleaned), styles["gate"])],
    ]
    box = Table(inner, colWidths=[CONTENT_WIDTH])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CALLOUT_GATE_BG),
                ("BOX", (0, 0), (-1, -1), 1.2, ACCENT),
                ("LINEBEFORE", (0, 0), (0, -1), 4, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (0, 0), 6),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
                ("TOPPADDING", (0, 1), (-1, -1), 2),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return box


def _build_spouse_share_box(text: str, styles: dict[str, ParagraphStyle]) -> Table:
    inner = [
        [Paragraph("SHARE WITH YOUR SPOUSE", styles["gate_label"])],
        [Paragraph(_format_inline(text), styles["spouse_share"])],
    ]
    box = Table(inner, colWidths=[CONTENT_WIDTH])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f5f1")),
                ("BOX", (0, 0), (-1, -1), 0.8, CALLOUT_AMBER_EDGE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return box


def _build_footer_disclaimer(styles: dict[str, ParagraphStyle]) -> Table:
    text = (
        "<b>Disclaimer:</b> This plan is decision support, not an official finance or legal determination. "
        "Always verify BAH, OHA, COLA, TLE/TLA, DITY/PPM, and weight allowances with your finance office, "
        "TMO, and current LES / DTMO tables before you spend money or sign a lease."
    )
    inner = [[Paragraph(text, styles["disclaimer"])]]
    box = Table(inner, colWidths=[CONTENT_WIDTH])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f4f1")),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return box


# ── Cover ───────────────────────────────────────────────────────────────────


def _build_cover_block(
    markdown_content: str,
    metadata: dict[str, Any] | None,
    report_date: str,
    styles: dict[str, ParagraphStyle],
) -> list[Any]:
    """Title, move summary (left), housing package callout (top right)."""
    flowables: list[Any] = []
    title_line = _extract_title(markdown_content)
    if metadata and metadata.get("family_name"):
        family = str(metadata["family_name"]).strip()
        if family:
            title_line = f"{family}'s PCS Strategic Plan"

    flowables.append(Paragraph(_format_inline(title_line), styles["title"]))
    flowables.append(
        Paragraph(
            f"<b>Report date:</b> {_escape(report_date)} · Built For Soldiers; By Soldiers · "
            f"Plain-English plan you can share tonight",
            styles["subtitle"],
        )
    )

    if metadata:
        move_lines = _metadata_lines(metadata)
        bah_cell = _bah_callout_cell(metadata, styles)
        meta_table = None
        if move_lines:
            meta_table = Table(move_lines, colWidths=[1.2 * inch, 2.5 * inch])
            meta_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ]
                )
            )

        if bah_cell is not None and meta_table is not None:
            outer = Table(
                [[meta_table, bah_cell]],
                colWidths=[3.85 * inch, 3.35 * inch],
            )
            outer.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ]
                )
            )
            flowables.append(Spacer(1, 0.05 * inch))
            flowables.append(outer)
        elif bah_cell is not None:
            flowables.append(Spacer(1, 0.05 * inch))
            flowables.append(bah_cell)
        elif meta_table is not None:
            flowables.append(Spacer(1, 0.06 * inch))
            flowables.append(meta_table)

    howto_inner = [
        [Paragraph("HOW TO USE THIS PLAN (5 minutes)", styles["howto_label"])],
        [
            Paragraph(
                "<b>1.</b> Read Section 1 with your spouse — agree on the main call. "
                "<b>2.</b> Treat every <b>Decision Gate</b> as a hard stop before you sign or spend. "
                "<b>3.</b> Run Section 5 day-by-day in the first month. "
                "<b>4.</b> Section 8 is your short checklist. "
                "Amber/green boxes explain TLE vs TLA, BAH/OHA start vs report date, "
                "HHG vs PPM/weight tickets, and how to treat Decision Gates.",
                styles["howto"],
            )
        ],
    ]
    howto_box = Table(howto_inner, colWidths=[CONTENT_WIDTH])
    howto_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT_SOFT),
                ("BOX", (0, 0), (-1, -1), 0.75, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (0, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
                ("TOPPADDING", (0, 1), (-1, -1), 1),
            ]
        )
    )
    flowables.append(Spacer(1, 0.08 * inch))
    flowables.append(howto_box)
    flowables.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceBefore=8, spaceAfter=4))
    return flowables


def _bah_callout_cell(
    metadata: dict[str, Any],
    styles: dict[str, ParagraphStyle],
) -> Table | None:
    """Top-right housing package callout."""
    callout = str(metadata.get("bah_callout") or "").strip()
    if not callout:
        return None

    gain = metadata.get("bah_gaining_amount")
    curr = metadata.get("bah_current_amount")
    delta = metadata.get("bah_monthly_delta")
    system = str(metadata.get("housing_system") or "BAH")

    if system == "OHA":
        header = "OHA + COLA package"
    elif system == "BAH_PLUS_COLA":
        header = "BAH + COLA package"
    else:
        header = "Your BAH at new post"
    if gain not in (None, ""):
        try:
            if system == "OHA":
                header = f"${int(gain):,}/mo OHA+COLA"
            elif system == "BAH_PLUS_COLA":
                header = f"${int(gain):,}/mo BAH+COLA"
            else:
                header = f"${int(gain):,}/mo BAH"
        except (TypeError, ValueError):
            pass

    delta_line = ""
    if delta not in (None, "") and curr not in (None, ""):
        try:
            d = int(delta)
            c = int(curr)
            if d > 0:
                delta_line = f"+${d:,}/mo vs current (${c:,} total)"
            elif d < 0:
                delta_line = f"−${abs(d):,}/mo vs current (${c:,} total)"
            else:
                delta_line = f"Same total as current (${c:,}/mo)"
        except (TypeError, ValueError):
            delta_line = ""

    body_style = ParagraphStyle(
        "BahCalloutBody",
        parent=styles["body"],
        fontSize=8,
        leading=10.5,
        textColor=WHITE,
    )
    head_style = ParagraphStyle(
        "BahCalloutHead",
        parent=styles["body"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=WHITE,
        spaceAfter=3,
    )
    sub_style = ParagraphStyle(
        "BahCalloutSub",
        parent=styles["body"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#a8d4bc"),
        spaceAfter=3,
    )
    label_style = ParagraphStyle(
        "BahCalloutLabel",
        parent=styles["body"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#c5ddd0"),
        spaceAfter=2,
    )

    inner: list[list[Any]] = [
        [Paragraph("HOUSING AT A GLANCE", label_style)],
        [Paragraph(_escape(header), head_style)],
    ]
    if delta_line:
        inner.append([Paragraph(_escape(delta_line), sub_style)])
    inner.append([Paragraph(_escape(callout), body_style)])

    box = Table(inner, colWidths=[3.2 * inch])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("BOX", (0, 0), (-1, -1), 0, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (0, 0), 8),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
                ("TOPPADDING", (0, 1), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -2), 1),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return box


def _metadata_lines(metadata: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    yos = metadata.get("years_of_service")
    deps = metadata.get("num_dependents")
    yos_label = f"{yos} years" if yos is not None and str(yos) != "" else ""
    if deps is not None and str(deps) != "":
        try:
            d = int(deps)
            deps_label = f"{d} dependent{'s' if d != 1 else ''}"
        except (TypeError, ValueError):
            deps_label = str(deps)
    else:
        deps_label = ""

    fields = [
        ("Prepared for", metadata.get("family_name", "")),
        ("Rank", metadata.get("rank", "")),
        ("YOS / family", " · ".join(x for x in (yos_label, deps_label) if x)),
        ("Moving from", metadata.get("from_installation", "")),
        ("Moving to", metadata.get("to_installation", "")),
        ("Move window", metadata.get("move_window", "")),
        ("Primary priority", metadata.get("primary_priority", "")),
    ]
    styles = _build_styles()
    for label, value in fields:
        if value:
            rows.append(
                [
                    Paragraph(_escape(label), styles["meta_label"]),
                    Paragraph(_format_inline(str(value)), styles["meta_value"]),
                ]
            )
    return rows


def _extract_title(markdown_content: str) -> str:
    for line in markdown_content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            return stripped[2:].strip()
    return "PCS Vector Strategic Plan"


# ── Body parse ──────────────────────────────────────────────────────────────


def _parse_markdown_to_flowables(
    markdown_content: str,
    styles: dict[str, ParagraphStyle],
    *,
    metadata: dict[str, Any] | None = None,
) -> list[Any]:
    """Parse markdown into flowables; inject insight callouts after key sections."""
    flowables: list[Any] = []
    lines = markdown_content.splitlines()
    i = 0
    skip_title = True
    meta = metadata or {}
    current_section = 0
    section_buffer: list[Any] = []

    def flush_section_with_callouts() -> None:
        nonlocal section_buffer
        if not section_buffer:
            return
        keys = _INJECT_AFTER_SECTION.get(current_section, [])
        if not keys:
            flowables.extend(section_buffer)
            section_buffer = []
            return

        flowables.extend(section_buffer)
        flowables.append(Spacer(1, 0.06 * inch))
        if len(keys) == 1:
            full = _get_insight_callout(keys[0], meta, styles, CONTENT_WIDTH)
            if full is not None:
                flowables.append(full)
        else:
            half = (CONTENT_WIDTH - 0.1 * inch) / 2
            pair = []
            for key in keys[:2]:
                b = _get_insight_callout(key, meta, styles, half)
                if b:
                    pair.append(b)
            if len(pair) == 2:
                row = Table([pair], colWidths=[half, half])
                row.setStyle(
                    TableStyle(
                        [
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("RIGHTPADDING", (0, 0), (0, 0), 5),
                            ("LEFTPADDING", (1, 0), (1, 0), 5),
                        ]
                    )
                )
                flowables.append(row)
            else:
                for b in pair:
                    flowables.append(b)
                    flowables.append(Spacer(1, 0.05 * inch))
        section_buffer = []

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()

        if not line:
            i += 1
            continue

        if skip_title and line.startswith("# ") and not line.startswith("## "):
            skip_title = False
            i += 1
            continue

        if line.startswith("## "):
            flush_section_with_callouts()
            section_match = SECTION_PATTERN.match(line)
            if section_match:
                num, title = section_match.groups()
                current_section = int(num)
                section_para = Paragraph(
                    f"{num}. {_format_inline(title)}",
                    styles["section"],
                )
                # Section header bar
                header_tbl = Table(
                    [[section_para]],
                    colWidths=[CONTENT_WIDTH],
                )
                header_tbl.setStyle(
                    TableStyle(
                        [
                            ("LINEBELOW", (0, 0), (-1, -1), 1.5, ACCENT),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                            ("TOPPADDING", (0, 0), (-1, -1), 2),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ]
                    )
                )
                section_buffer.append(KeepTogether([header_tbl, Spacer(1, 0.05 * inch)]))
            else:
                section_buffer.append(Paragraph(_format_inline(line[3:]), styles["section"]))
            i += 1
            continue

        if line.startswith("|") and "|" in line[1:]:
            table_lines, i = _collect_table(lines, i)
            table = _build_table(table_lines, styles)
            if table:
                section_buffer.append(Spacer(1, 0.04 * inch))
                section_buffer.append(table)
                section_buffer.append(Spacer(1, 0.06 * inch))
            continue

        if _is_bullet(line):
            bullet_items, i = _collect_bullets(lines, i)
            for item in bullet_items:
                section_buffer.append(
                    Paragraph(f"• {_format_inline(item)}", styles["bullet"])
                )
            continue

        if _is_numbered(line):
            numbered_items, i = _collect_numbered(lines, i)
            for idx, item in enumerate(numbered_items, start=1):
                section_buffer.append(
                    Paragraph(f"{idx}. {_format_inline(item)}", styles["numbered"])
                )
            continue

        paragraph_lines, i = _collect_paragraph(lines, i)
        text = " ".join(paragraph_lines).strip()
        if text:
            lower = text.lower().lstrip()
            if re.match(r"^(\*\*)?gate:", lower) or (
                re.search(r"\bgate:", lower) and len(text) < 320
            ):
                section_buffer.append(Spacer(1, 0.04 * inch))
                section_buffer.append(_build_gate_box(text, styles))
                section_buffer.append(Spacer(1, 0.06 * inch))
            elif "we're targeting" in lower and len(text) < 420:
                section_buffer.append(Spacer(1, 0.06 * inch))
                section_buffer.append(_build_spouse_share_box(text, styles))
            elif re.search(r"commander brief", lower) and len(text) < 900:
                m = re.search(
                    r"commander brief[:\s]+[\"“']?(.+?)[\"”']?\s*$",
                    text,
                    re.I,
                )
                if m:
                    brief_body = m.group(1).strip().strip("\"'“”")
                    prefix = text[: m.start()].strip()
                    if prefix and len(prefix) > 40:
                        section_buffer.append(
                            Paragraph(_format_inline(prefix), styles["body"])
                        )
                    section_buffer.append(
                        _make_callout(
                            "COMMANDER BRIEF (one line you can use)",
                            _format_inline(brief_body),
                            styles,
                            width=CONTENT_WIDTH,
                            variant="navy",
                        )
                    )
                else:
                    section_buffer.append(Paragraph(_format_inline(text), styles["body"]))
            else:
                section_buffer.append(Paragraph(_format_inline(text), styles["body"]))
        else:
            i += 1

    flush_section_with_callouts()
    return flowables


def _collect_table(lines: list[str], start: int) -> tuple[list[str], int]:
    collected: list[str] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("|") and "|" in stripped[1:]:
            if TABLE_SEP_PATTERN.match(stripped):
                i += 1
                continue
            collected.append(stripped)
            i += 1
        else:
            break
    return collected, i


def _build_table(table_lines: list[str], styles: dict[str, ParagraphStyle]) -> Table | None:
    if not table_lines:
        return None

    rows: list[list[str]] = []
    for line in table_lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells:
            rows.append(cells)

    if not rows:
        return None

    col_count = max(len(r) for r in rows)
    normalized: list[list[str]] = []
    for row in rows:
        padded = row + [""] * (col_count - len(row))
        normalized.append(padded[:col_count])

    col_width = CONTENT_WIDTH / col_count
    table_data: list[list[Any]] = []
    for r_idx, row in enumerate(normalized):
        style = styles["table_header"] if r_idx == 0 else styles["table_cell"]
        table_data.append([Paragraph(_format_inline(cell), style) for cell in row])

    table = Table(
        table_data,
        colWidths=[col_width] * col_count,
        repeatRows=1,
    )
    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for r in range(1, len(table_data)):
        if r % 2 == 0:
            commands.append(("BACKGROUND", (0, r), (-1, r), TABLE_ALT_BG))
    table.setStyle(TableStyle(commands))
    return table


def _is_bullet(line: str) -> bool:
    return line.startswith(("- ", "* ", "• "))


def _collect_bullets(lines: list[str], start: int) -> tuple[list[str], int]:
    items: list[str] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if _is_bullet(stripped):
            items.append(stripped[2:].strip())
            i += 1
        elif not stripped:
            i += 1
            break
        else:
            break
    return items, i


def _is_numbered(line: str) -> bool:
    return bool(re.match(r"^\d+[\.\)]\s+", line))


def _collect_numbered(lines: list[str], start: int) -> tuple[list[str], int]:
    items: list[str] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        match = re.match(r"^\d+[\.\)]\s+(.+)$", stripped)
        if match:
            items.append(match.group(1).strip())
            i += 1
        elif not stripped:
            i += 1
            break
        else:
            break
    return items, i


def _collect_paragraph(lines: list[str], start: int) -> tuple[list[str], int]:
    parts: list[str] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if (
            not stripped
            or stripped.startswith("## ")
            or stripped.startswith("|")
            or _is_bullet(stripped)
            or _is_numbered(stripped)
        ):
            break
        if stripped.startswith("# ") and not stripped.startswith("## "):
            break
        parts.append(stripped)
        i += 1
    return parts, i


def _format_inline(text: str) -> str:
    """Convert lightweight markdown inline styles to ReportLab XML."""
    safe = _escape(text)
    safe = BOLD_PATTERN.sub(r"<b>\1</b>", safe)
    safe = ITALIC_PATTERN.sub(r"<i>\1</i>", safe)
    safe = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", safe)
    return _sanitize_xml(safe)


def _escape(text: str) -> str:
    cleaned = text.replace("\u2014", "—").replace("\u2013", "–")
    cleaned = cleaned.replace("\xa0", " ")
    return html.escape(cleaned, quote=False)


def _sanitize_xml(text: str) -> str:
    return (
        text.replace("&nbsp;", " ")
        .replace("<br>", "<br/>")
        .replace("<br />", "<br/>")
    )


def _draw_page_frame(canvas, doc, report_date: str) -> None:
    """Header band and footer on each page."""
    canvas.saveState()
    header_y = PAGE_HEIGHT - 0.42 * inch
    footer_y = 0.38 * inch

    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_HEIGHT - 0.28 * inch, PAGE_WIDTH, 0.28 * inch, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.drawString(MARGIN, header_y, "PCS Vector")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN,
        header_y,
        "Your plan · plain English · verify with finance",
    )

    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, footer_y + 0.14 * inch, PAGE_WIDTH - MARGIN, footer_y + 0.14 * inch)

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGIN, footer_y, f"Generated {report_date}")
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN,
        footer_y,
        f"Page {canvas.getPageNumber()}",
    )
    canvas.setFont("Helvetica-Oblique", 7)
    canvas.drawCentredString(
        PAGE_WIDTH / 2,
        footer_y - 0.14 * inch,
        "Built For Soldiers; By Soldiers  ·  Not an official finance determination",
    )
    canvas.restoreState()


def build_pdf_metadata(form_data: dict[str, Any]) -> dict[str, Any]:
    """Extract cover metadata including BAH/OHA + COLA callout."""
    from components.form_options import rank_short_for_pay_grade
    from components.form_state import (
        resolved_current_installation,
        resolved_gaining_installation,
    )
    from services.housing_allowances import (
        compare_housing_packages,
        format_housing_callout,
        with_dependents_from_family_status,
    )

    pay_grade = str(form_data.get("rank_pay_grade", "") or "")
    rank = pay_grade
    if form_data.get("rank_title"):
        rank = f"{pay_grade} ({form_data['rank_title']})"

    first = str(form_data.get("first_name", "")).strip()
    last = str(form_data.get("last_name", "")).strip()
    family_name = f"{first} {last}".strip()

    current = resolved_current_installation(form_data)
    gaining = resolved_gaining_installation(form_data)
    family_status = str(form_data.get("family_status") or "Married / with dependents")
    with_deps = with_dependents_from_family_status(family_status)
    yos = form_data.get("years_of_service", 4)
    raw_deps = form_data.get("num_dependents")
    if raw_deps is None:
        if with_deps:
            raw_deps = 1 + int(form_data.get("num_children") or 0)
        else:
            raw_deps = 0
    num_deps = max(0, min(5, int(raw_deps)))

    pkg = compare_housing_packages(
        pay_grade=pay_grade or "E-5",
        with_dependents=with_deps,
        gaining_installation=gaining,
        current_installation=current or None,
        years_of_service=yos,
        num_dependents=num_deps,
    )
    gaining_pkg = pkg["gaining"]
    current_pkg = pkg.get("current")
    callout = format_housing_callout(
        rank_short=rank_short_for_pay_grade(pay_grade),
        last_name=last,
        package=gaining_pkg,
        current_package=current_pkg,
    )

    return {
        "family_name": family_name,
        "rank": rank,
        "from_installation": current,
        "to_installation": gaining,
        "move_window": str(form_data.get("move_window", "")),
        "primary_priority": str(form_data.get("primary_priority", "")),
        "family_status": family_status,
        "bah_callout": callout,
        "bah_gaining_amount": gaining_pkg.get("total_monthly_usd"),
        "bah_current_amount": (
            current_pkg.get("total_monthly_usd") if current_pkg else None
        ),
        "bah_monthly_delta": pkg.get("monthly_delta_usd"),
        "bah_with_dependents": with_deps,
        "num_dependents": num_deps,
        "years_of_service": gaining_pkg.get("years_of_service"),
        "housing_system": gaining_pkg.get("housing_system"),
        "cola_monthly_usd": gaining_pkg.get("cola_monthly_usd"),
        "cola_index": gaining_pkg.get("cola_index"),
    }

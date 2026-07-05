"""Professional PDF export for PCS Vector reports."""

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

# Brand palette (matches PCS Vector web app)
NAVY = colors.HexColor("#1e3a5f")
NAVY_LIGHT = colors.HexColor("#2d5a8a")
ACCENT = colors.HexColor("#c45c26")
SLATE = colors.HexColor("#4a5568")
MUTED = colors.HexColor("#718096")
BORDER = colors.HexColor("#e2e8f0")
TABLE_HEADER_BG = colors.HexColor("#eef2f7")
TABLE_ALT_BG = colors.HexColor("#f7f9fc")

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.72 * inch

SECTION_PATTERN = re.compile(r"^##\s+(\d+)\.\s+(.+)$")
BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")
ITALIC_PATTERN = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
TABLE_SEP_PATTERN = re.compile(r"^\|[\s\-:|]+\|$")


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
            topMargin=MARGIN + 0.35 * inch,
            bottomMargin=MARGIN + 0.25 * inch,
            title="PCS Vector Strategic Plan",
            author="PCS Vector",
        )

        styles = _build_styles()
        story: list[Any] = []
        report_date = datetime.now().strftime("%B %d, %Y")

        story.extend(_build_cover_block(markdown_content, metadata, report_date, styles))
        story.append(Spacer(1, 0.2 * inch))
        story.extend(_parse_markdown_to_flowables(markdown_content, styles))

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
            fontSize=22,
            leading=26,
            textColor=NAVY,
            spaceAfter=10,
            alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "PCSSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=SLATE,
            spaceAfter=6,
        ),
        "section": ParagraphStyle(
            "PCSSection",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=16,
            spaceAfter=8,
            borderPadding=0,
        ),
        "body": ParagraphStyle(
            "PCSBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=SLATE,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "PCSBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=SLATE,
            leftIndent=14,
            bulletIndent=0,
            spaceAfter=4,
        ),
        "numbered": ParagraphStyle(
            "PCSNumbered",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=SLATE,
            leftIndent=14,
            spaceAfter=4,
        ),
        "table_cell": ParagraphStyle(
            "PCSTableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=SLATE,
        ),
        "table_header": ParagraphStyle(
            "PCSTableHeader",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=NAVY,
        ),
        "meta_label": ParagraphStyle(
            "PCSMetaLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=NAVY,
        ),
        "meta_value": ParagraphStyle(
            "PCSMetaValue",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=SLATE,
        ),
    }


def _build_cover_block(
    markdown_content: str,
    metadata: dict[str, Any] | None,
    report_date: str,
    styles: dict[str, ParagraphStyle],
) -> list[Any]:
    """Build title and optional move summary above section content."""
    flowables: list[Any] = []
    title_line = _extract_title(markdown_content)

    flowables.append(Paragraph(_format_inline(title_line), styles["title"]))
    flowables.append(
        Paragraph(
            f"<b>Report date:</b> {_escape(report_date)}",
            styles["subtitle"],
        )
    )

    if metadata:
        move_lines = _metadata_lines(metadata)
        if move_lines:
            flowables.append(Spacer(1, 0.08 * inch))
            meta_table = Table(move_lines, colWidths=[1.35 * inch, 4.8 * inch])
            meta_table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ]
                )
            )
            flowables.append(meta_table)

    flowables.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceBefore=8, spaceAfter=4))
    return flowables


def _metadata_lines(metadata: dict[str, Any]) -> list[list[Any]]:
    """Build label/value rows for the cover summary."""
    rows: list[list[Any]] = []
    fields = [
        ("Prepared for", metadata.get("family_name", "")),
        ("Rank", metadata.get("rank", "")),
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


def _parse_markdown_to_flowables(
    markdown_content: str,
    styles: dict[str, ParagraphStyle],
) -> list[Any]:
    """Parse markdown lines into ReportLab flowables."""
    flowables: list[Any] = []
    lines = markdown_content.splitlines()
    i = 0
    skip_title = True

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
            section_match = SECTION_PATTERN.match(line)
            if section_match:
                num, title = section_match.groups()
                section_para = Paragraph(
                    f"{num}. {_format_inline(title)}",
                    styles["section"],
                )
                flowables.append(KeepTogether([section_para, Spacer(1, 0.04 * inch)]))
            else:
                flowables.append(Paragraph(_format_inline(line[3:]), styles["section"]))
            i += 1
            continue

        if line.startswith("|") and "|" in line[1:]:
            table_lines, i = _collect_table(lines, i)
            table = _build_table(table_lines, styles)
            if table:
                flowables.append(Spacer(1, 0.06 * inch))
                flowables.append(table)
                flowables.append(Spacer(1, 0.08 * inch))
            continue

        if _is_bullet(line):
            bullet_items, i = _collect_bullets(lines, i)
            for item in bullet_items:
                flowables.append(
                    Paragraph(f"• {_format_inline(item)}", styles["bullet"])
                )
            continue

        if _is_numbered(line):
            numbered_items, i = _collect_numbered(lines, i)
            for idx, item in enumerate(numbered_items, start=1):
                flowables.append(
                    Paragraph(f"{idx}. {_format_inline(item)}", styles["numbered"])
                )
            continue

        paragraph_lines, i = _collect_paragraph(lines, i)
        text = " ".join(paragraph_lines).strip()
        if text:
            flowables.append(Paragraph(_format_inline(text), styles["body"]))
        else:
            i += 1

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

    usable_width = PAGE_WIDTH - 2 * MARGIN
    col_width = usable_width / col_count

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
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
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
    """Escape text for ReportLab Paragraph XML."""
    cleaned = text.replace("\u2014", "—").replace("\u2013", "–")
    cleaned = cleaned.replace("\xa0", " ")
    return html.escape(cleaned, quote=False)


def _sanitize_xml(text: str) -> str:
    """Remove unsupported XML entities that may appear in model output."""
    return (
        text.replace("&nbsp;", " ")
        .replace("<br>", "<br/>")
        .replace("<br />", "<br/>")
    )


def _draw_page_frame(canvas, doc, report_date: str) -> None:
    """Draw header band and footer on each page."""
    canvas.saveState()
    header_y = PAGE_HEIGHT - 0.48 * inch
    footer_y = 0.42 * inch

    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_HEIGHT - 0.32 * inch, PAGE_WIDTH, 0.32 * inch, fill=1, stroke=0)

    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(MARGIN, header_y, "PCS Vector")

    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN,
        header_y,
        "Personalized PCS Strategic Plan",
    )

    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, footer_y + 0.12 * inch, PAGE_WIDTH - MARGIN, footer_y + 0.12 * inch)

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(MARGIN, footer_y - 0.02 * inch, f"Generated {report_date}")
    canvas.drawRightString(
        PAGE_WIDTH - MARGIN,
        footer_y - 0.02 * inch,
        f"Page {canvas.getPageNumber()}",
    )

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Oblique", 7)
    canvas.drawCentredString(
        PAGE_WIDTH / 2,
        footer_y - 0.16 * inch,
        "Independent planning tool — not affiliated with the U.S. Department of Defense",
    )

    canvas.restoreState()


def build_pdf_metadata(form_data: dict[str, Any]) -> dict[str, str]:
    """Extract cover metadata from session form data."""
    from components.form_state import (
        resolved_current_installation,
        resolved_gaining_installation,
    )

    rank = form_data.get("rank_pay_grade", "")
    if form_data.get("rank_title"):
        rank = f"{rank} ({form_data['rank_title']})"

    first = str(form_data.get("first_name", "")).strip()
    last = str(form_data.get("last_name", "")).strip()
    family_name = f"{first} {last}".strip()

    return {
        "family_name": family_name,
        "rank": rank,
        "from_installation": resolved_current_installation(form_data),
        "to_installation": resolved_gaining_installation(form_data),
        "move_window": str(form_data.get("move_window", "")),
        "primary_priority": str(form_data.get("primary_priority", "")),
    }
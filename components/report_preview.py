"""Static sample report preview for the homepage."""

from __future__ import annotations

import streamlit as st

from components.content import REPORT_PREVIEW
from components.html_utils import safe_html


def render_report_preview() -> None:
    """Render a document-style sample report so buyers know what they're getting."""
    p = REPORT_PREVIEW
    section_blocks: list[str] = []

    for block in p["visible_sections"]:
        body_html = "".join(f"<p>{safe_html(line)}</p>" for line in block["lines"])
        if block.get("table"):
            rows = "".join(
                f"<tr><td>{safe_html(r['label'])}</td>"
                f"<td>{safe_html(r['value'])}</td>"
                f"<td>{safe_html(r['note'])}</td></tr>"
                for r in block["table"]
            )
            body_html += (
                f'<table class="pcs-preview-table">'
                f"<thead><tr><th>Option</th><th>BAH impact</th><th>Notes</th></tr></thead>"
                f"<tbody>{rows}</tbody></table>"
            )
        section_blocks.append(
            f'<div class="pcs-preview-section">'
            f'<div class="pcs-preview-section-head">'
            f'<span class="pcs-preview-section-num">{block["num"]}</span>'
            f'<span class="pcs-preview-section-title">{safe_html(block["title"])}</span>'
            f"</div>"
            f'<div class="pcs-preview-section-body">{body_html}</div>'
            f"</div>"
        )

    blurred_items = "".join(
        f'<li><span class="pcs-preview-blur-num">{s["num"]}</span>{safe_html(s["title"])}</li>'
        for s in p["blurred_sections"]
    )

    st.markdown(
        f"""
        <div class="pcs-preview-wrap">
            <div class="pcs-preview-header">
                <h3>{safe_html(p["headline"])}</h3>
                <p class="pcs-preview-sub">{safe_html(p["subhead"])}</p>
            </div>
            <div class="pcs-preview-doc">
                <div class="pcs-preview-doc-bar">
                    <span class="pcs-preview-doc-badge">Sample report</span>
                    <span class="pcs-preview-doc-meta">{safe_html(p["sample_meta"])}</span>
                </div>
                <div class="pcs-preview-doc-title">PCS Vector Strategic Plan</div>
                {"".join(section_blocks)}
                <div class="pcs-preview-blur-zone">
                    <div class="pcs-preview-blur-fade"></div>
                    <div class="pcs-preview-blur-content">
                        <p class="pcs-preview-blur-label">+ 5 more personalized sections in your report</p>
                        <ul class="pcs-preview-blur-list">{blurred_items}</ul>
                        <p class="pcs-preview-blur-note">{safe_html(p["blur_note"])}</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
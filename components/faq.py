"""Crawlable Army PCS FAQ — visible HTML + FAQPage JSON-LD for SEO / LLMs."""

from __future__ import annotations

import json

import streamlit as st
import streamlit.components.v1 as components

from components.content import FAQ_ITEMS, FAQ_LEAD
from components.html_utils import safe_html

FAQ_TITLE = "Army PCS FAQ — BAH, OHA, COLA, DLA, and housing pay"
META_DESCRIPTION = (
    "Free Army PCS calculator: compare 2026 BAH, OHA, COLA, rent, utilities, "
    "and gas between duty stations. Built for Soldiers. Not affiliated with DoD."
)
CANONICAL_URL = "https://pcs-vector-hnfyzcpqmtty2mpwpztpbf.streamlit.app/"


def _faq_schema() -> dict:
    questions = []
    for item in FAQ_ITEMS:
        questions.append(
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
        )
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "name": "PCS Vector",
                "url": CANONICAL_URL,
                "applicationCategory": "FinanceApplication",
                "operatingSystem": "Web",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "description": META_DESCRIPTION,
                "audience": {
                    "@type": "Audience",
                    "audienceType": "U.S. Army Soldiers and military families",
                },
            },
            {
                "@type": "FAQPage",
                "name": FAQ_TITLE,
                "url": CANONICAL_URL,
                "mainEntity": questions,
            },
        ],
    }


def _inject_head() -> None:
    """Write JSON-LD + meta description onto the parent document (Streamlit iframe)."""
    schema_js = json.dumps(json.dumps(_faq_schema(), ensure_ascii=True))
    desc_js = json.dumps(META_DESCRIPTION)
    title_js = json.dumps(
        "PCS Vector — Free Army PCS BAH Calculator (2026) | OHA, COLA, Housing"
    )
    canon_js = json.dumps(CANONICAL_URL)
    components.html(
        f"""
<script>
(function () {{
  var doc = window.parent.document;
  var head = doc.head;
  function upsertMeta(attr, key, val) {{
    var sel = 'meta[' + attr + '="' + key + '"]';
    var el = head.querySelector(sel);
    if (!el) {{
      el = doc.createElement("meta");
      el.setAttribute(attr, key);
      head.appendChild(el);
    }}
    el.setAttribute("content", val);
  }}
  var title = {title_js};
  if (doc.title !== title) doc.title = title;
  upsertMeta("name", "description", {desc_js});
  upsertMeta("property", "og:title", title);
  upsertMeta("property", "og:description", {desc_js});
  upsertMeta("property", "og:type", "website");
  upsertMeta("property", "og:url", {canon_js});
  upsertMeta("name", "robots", "index, follow");
  var link = head.querySelector('link[rel="canonical"]');
  if (!link) {{
    link = doc.createElement("link");
    link.setAttribute("rel", "canonical");
    head.appendChild(link);
  }}
  link.setAttribute("href", {canon_js});
  var old = doc.getElementById("pcs-faq-jsonld");
  if (old) old.remove();
  var s = doc.createElement("script");
  s.type = "application/ld+json";
  s.id = "pcs-faq-jsonld";
  s.textContent = {schema_js};
  head.appendChild(s);
}})();
</script>
        """,
        height=0,
    )


def render_home_faq() -> None:
    """Collapsed FAQ in the UI; full Q&A stays in JSON-LD for crawlers / LLMs."""
    _inject_head()
    items_html = []
    for item in FAQ_ITEMS:
        items_html.append(
            "<article class='pcs-seo-faq-item' itemscope "
            "itemprop='mainEntity' itemtype='https://schema.org/Question'>"
            f"<h3 itemprop='name'>{safe_html(item['q'])}</h3>"
            "<div itemscope itemprop='acceptedAnswer' itemtype='https://schema.org/Answer'>"
            f"<p itemprop='text'>{safe_html(item['a'])}</p>"
            "</div></article>"
        )
    block = f"""
<section class="pcs-seo-faq" id="pcs-faq" aria-labelledby="pcs-faq-heading"
  itemscope itemtype="https://schema.org/FAQPage">
  <h2 id="pcs-faq-heading">{safe_html(FAQ_TITLE)}</h2>
  <p class="pcs-seo-faq-lead">{safe_html(FAQ_LEAD)}</p>
  {"".join(items_html)}
</section>
"""
    with st.container(key="pcs_faq_box"):
        with st.expander("FAQ — BAH, OHA, COLA & more", expanded=False):
            st.html(block)


def render_faq(title: str | None = None) -> None:
    render_home_faq()

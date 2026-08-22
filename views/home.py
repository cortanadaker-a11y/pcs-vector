"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import json
import re

import streamlit as st
import streamlit.components.v1 as components

from components.bah_calculator import get_calculator_snapshot, render_bah_calculator
from components.content import TRUST_SIGNALS
from components.form_options import PAY_GRADE_TO_RANK
from components.html_utils import safe_html
from services.referral_lead import (
    INTEREST_OPTIONS,
    build_redirect_to_form_html,
    build_referral_row,
    format_dependents_label,
    format_rank_label,
    submit_referral_via_apps_script,
)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _clean_email(raw: str | None) -> str:
    text = (raw or "").strip()
    for ch in ("\u200b", "\u200c", "\u200d", "\ufeff", "\xa0"):
        text = text.replace(ch, "")
    return text.strip()


def _is_valid_email(raw: str | None) -> bool:
    return bool(_EMAIL_RE.match(_clean_email(raw)))


def _render_header() -> None:
    st.markdown(
        f"""
        <div class="pcs-hero pcs-hero-compact">
            <div class="pcs-brand-title">PCS Vector</div>
            <div class="pcs-hero-tag">{safe_html(TRUST_SIGNALS["banner"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _deps_short(num_deps: int) -> str:
    n = max(0, int(num_deps))
    if n == 0:
        return "0 dependents"
    if n >= 5:
        return "5+ dependents"
    return f"{n} dependent{'s' if n != 1 else ''}"


def _calc_fields_from_snap(snap: dict) -> dict[str, str]:
    grade = str(snap.get("pay_grade") or "")
    num_deps = int(snap.get("num_dependents") or 0)
    return {
        "destination": str(snap.get("gaining_installation") or "").strip(),
        "rank": format_rank_label(grade, PAY_GRADE_TO_RANK.get(grade)) if grade else "",
        "dependents": format_dependents_label(
            with_dependents=num_deps > 0, num_dependents=num_deps
        ),
        "dependents_short": _deps_short(num_deps),
    }


def _short_dest(dest: str, max_len: int = 28) -> str:
    text = (dest or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def _render_sticky_referral_cta(calc: dict[str, str]) -> None:
    """Fixed bottom bar while scrolling the calculator — jumps to #pcs-referral."""
    dest = calc.get("destination") or ""
    if not dest:
        components.html(
            """<script>
            (function () {
              try {
                var el = window.parent.document.getElementById("pcs-sticky-ref-bar");
                if (el) el.remove();
                window.parent.document.documentElement.classList.remove("pcs-has-sticky-ref");
              } catch (e) {}
            })();
            </script>""",
            height=0,
        )
        return

    payload = {
        "dest": _short_dest(dest),
        "destFull": dest,
        "rank": calc.get("rank") or "—",
        "deps": calc.get("dependents_short") or calc.get("dependents") or "—",
    }
    data_js = json.dumps(payload)

    components.html(
        f"""
<script>
(function () {{
  var data = {data_js};
  var doc = window.parent.document;
  var root = doc.documentElement;

  var styleId = "pcs-sticky-ref-style";
  if (!doc.getElementById(styleId)) {{
    var css = doc.createElement("style");
    css.id = styleId;
    css.textContent = `
      html.pcs-has-sticky-ref [data-testid="stAppViewContainer"] {{
        padding-bottom: 4.75rem !important;
      }}
      #pcs-sticky-ref-bar {{
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        bottom: 0.85rem;
        z-index: 99999;
        width: min(780px, calc(100vw - 1.5rem));
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        padding: 0.65rem 0.85rem 0.65rem 1rem;
        border-radius: 14px;
        background: linear-gradient(145deg, #1a2e28 0%, #2a4a3f 100%);
        color: #fff;
        box-shadow: 0 12px 36px rgba(28, 28, 26, 0.28);
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
        transition: opacity 0.2s ease, transform 0.2s ease;
      }}
      #pcs-sticky-ref-bar.pcs-sticky-ref-hidden {{
        opacity: 0;
        pointer-events: none;
        transform: translateX(-50%) translateY(120%);
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-meta {{
        min-width: 0;
        flex: 1;
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-kicker {{
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(168, 212, 188, 0.95);
        margin-bottom: 0.15rem;
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-line {{
        font-size: 0.82rem;
        font-weight: 600;
        color: rgba(255,255,255,0.92);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-btn {{
        flex-shrink: 0;
        appearance: none;
        border: none;
        cursor: pointer;
        background: #fff;
        color: #1a2e28;
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: -0.01em;
        padding: 0.55rem 0.9rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-btn:hover {{
        background: #f4f2ee;
      }}
      @media (max-width: 560px) {{
        #pcs-sticky-ref-bar {{
          bottom: 0.55rem;
          padding: 0.55rem 0.65rem;
          gap: 0.5rem;
        }}
        #pcs-sticky-ref-bar .pcs-sticky-ref-line {{
          font-size: 0.74rem;
        }}
        #pcs-sticky-ref-bar .pcs-sticky-ref-btn {{
          font-size: 0.75rem;
          padding: 0.5rem 0.7rem;
        }}
      }}
    `;
    doc.head.appendChild(css);
  }}

  var bar = doc.getElementById("pcs-sticky-ref-bar");
  if (!bar) {{
    bar = doc.createElement("div");
    bar.id = "pcs-sticky-ref-bar";
    bar.setAttribute("role", "complementary");
    bar.setAttribute("aria-label", "Housing referral");
    doc.body.appendChild(bar);
  }}

  bar.innerHTML =
    '<div class="pcs-sticky-ref-meta">' +
      '<div class="pcs-sticky-ref-kicker">Housing help</div>' +
      '<div class="pcs-sticky-ref-line" title="' +
        String(data.destFull).replace(/"/g, "&quot;") +
      '">' +
        String(data.dest) + " · " + String(data.rank) + " · " + String(data.deps) +
      "</div>" +
    "</div>" +
    '<button type="button" class="pcs-sticky-ref-btn" id="pcs-sticky-ref-go">Find a place →</button>';

  root.classList.add("pcs-has-sticky-ref");

  function scrollToReferral() {{
    var target = doc.getElementById("pcs-referral");
    if (target && target.scrollIntoView) {{
      target.scrollIntoView({{ block: "start", behavior: "smooth" }});
      return;
    }}
    var main =
      doc.querySelector('[data-testid="stAppViewContainer"]') ||
      doc.querySelector("section.main");
    if (main) main.scrollTop = main.scrollHeight;
  }}

  var btn = doc.getElementById("pcs-sticky-ref-go");
  if (btn) {{
    btn.onclick = function (e) {{
      e.preventDefault();
      scrollToReferral();
    }};
  }}

  function setHidden(hidden) {{
    if (hidden) bar.classList.add("pcs-sticky-ref-hidden");
    else bar.classList.remove("pcs-sticky-ref-hidden");
  }}

  function getScrollRoot() {{
    return (
      doc.querySelector('[data-testid="stAppViewContainer"]') ||
      doc.querySelector("section.main") ||
      null
    );
  }}

  function watchReferral() {{
    var target = doc.getElementById("pcs-referral");
    if (!target) {{
      setHidden(false);
      return;
    }}
    if (bar._pcsIo) {{
      try {{ bar._pcsIo.disconnect(); }} catch (e) {{}}
    }}
    var scrollRoot = getScrollRoot();
    var io = new IntersectionObserver(
      function (entries) {{
        var entry = entries[0];
        setHidden(!!(entry && entry.isIntersecting && entry.intersectionRatio > 0.15));
      }},
      {{ root: scrollRoot, threshold: [0, 0.15, 0.35, 0.6, 1], rootMargin: "0px 0px -80px 0px" }}
    );
    io.observe(target);
    bar._pcsIo = io;
  }}

  watchReferral();
  [80, 250, 600].forEach(function (ms) {{
    setTimeout(watchReferral, ms);
  }});
}})();
</script>
        """,
        height=0,
    )


def _render_referral_hook() -> None:
    snap = get_calculator_snapshot() or {}
    calc = _calc_fields_from_snap(snap)

    dest = calc["destination"]
    dest_html = safe_html(dest) if dest else "your new post"
    rank_html = safe_html(calc["rank"] or "—")
    deps_short_html = safe_html(calc.get("dependents_short") or "—")
    ready = bool(dest)

    if ready:
        body_html = (
            f"We have verified military experts in <strong>{dest_html}</strong> "
            f"that can help you find a new home today."
        )
        summary_html = (
            f'<div class="pcs-ref-summary" title="Carried over from your calculator">'
            f"<span>{dest_html}</span>"
            f'<span class="pcs-ref-summary-sep">·</span>'
            f"<span>{rank_html}</span>"
            f'<span class="pcs-ref-summary-sep">·</span>'
            f"<span>{deps_short_html}</span>"
            f"</div>"
        )
    else:
        body_html = (
            "Set your New post above — then we’ll match you with verified military "
            "experts who can help you find a home today."
        )
        summary_html = ""

    with st.container(border=True):
        st.markdown(
            f"""
            <div id="pcs-referral" class="pcs-ref-head">
                <div class="pcs-ref-kicker">Free match · military housing pros</div>
                <div class="pcs-ref-title">Your next home is one step away</div>
                <p class="pcs-ref-body">{body_html}</p>
                {summary_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("referral_form", clear_on_submit=False):
            n1, n2 = st.columns(2)
            with n1:
                first_name = st.text_input(
                    "First Name",
                    key="referral_first_name",
                    placeholder="First name",
                )
            with n2:
                last_name = st.text_input(
                    "Last Name",
                    key="referral_last_name",
                    placeholder="Last name",
                )

            email_address = st.text_input(
                "Email address",
                key="referral_email_address",
                placeholder="you@email.com",
            )

            rent_buy_not_sure = st.radio(
                "Rent, buy, or not sure?",
                options=list(INTEREST_OPTIONS),
                horizontal=True,
                key="referral_rent_buy_not_sure",
            )

            st.caption("Free · Built For Soldiers; By Soldiers")
            submitted = st.form_submit_button(
                "Get my free housing referral →",
                type="primary",
                use_container_width=True,
                disabled=not ready,
            )

        if submitted:
            first_name = str(st.session_state.get("referral_first_name") or first_name or "")
            last_name = str(st.session_state.get("referral_last_name") or last_name or "")
            email_address = _clean_email(
                st.session_state.get("referral_email_address") or email_address
            )
            rent_buy_not_sure = str(
                st.session_state.get("referral_rent_buy_not_sure") or rent_buy_not_sure or ""
            )

            live = get_calculator_snapshot() or snap
            live_calc = _calc_fields_from_snap(live)

            live_deps_n = int(live.get("num_dependents") or 0)
            row = build_referral_row(
                destination=live_calc["destination"],
                first_name=first_name,
                last_name=last_name,
                rank=live_calc["rank"],
                rent_buy_not_sure=rent_buy_not_sure,
                num_dependents=live_deps_n,
                email_address=email_address,
            )

            if not live_calc["destination"]:
                st.error("Set New post in the calculator above first.")
            elif not row["First Name"].strip() or not row["Last Name"].strip():
                st.error("Enter your first and last name.")
            elif not _is_valid_email(row["Email address"]):
                st.error("Enter a valid email address (example: name@email.com).")
            else:
                st.session_state.referral_lead = {**row, "calculator": live}

                submit_referral_via_apps_script(row)

                st.html(
                    build_redirect_to_form_html(row),
                    unsafe_allow_javascript=True,
                )
                st.info(
                    "Taking you to the Google Form with your info filled in… "
                    "Click **Submit** on that page to finish."
                )

    _render_sticky_referral_cta(calc)


def _render_faq() -> None:
    with st.expander("FAQ", expanded=False):
        st.markdown(
            "**Free?** Yes.\n\n"
            "**BAH** — Flat U.S. housing pay. Keep the leftover if rent is lower.\n\n"
            "**OHA** — Overseas: actual rent up to a max, plus utilities.\n\n"
            "**COLA** — Extra for higher daily costs overseas, Alaska, Hawaii, and Puerto Rico. Not for rent.\n\n"
            "**DLA** — One-time move money when authorized. Confirm with finance.\n\n"
            "**Rent estimates** — Planning ranges by family size (1–4 bedrooms), not official rates.\n\n"
            "**Official?** Allowances from DoD tables — verify on your LES before you sign."
        )


def render_home() -> None:
    _render_header()
    render_bah_calculator()
    _render_referral_hook()
    _render_faq()
    st.caption("PCS Vector — Built For Soldiers; By Soldiers · Verify with finance before you spend.")

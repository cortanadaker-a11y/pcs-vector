"""Home — PCS finance calculator and housing referral."""

from __future__ import annotations

import json
import re

import streamlit as st
import streamlit.components.v1 as components

from components.bah_calculator import (
    get_calculator_snapshot,
    render_bah_calculator,
    wrap_dom_panel,
)
from components.faq import render_home_faq
from components.form_options import PAY_GRADE_TO_RANK
from components.html_utils import safe_html
from services.referral_lead import (
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


def _tag_page_face() -> None:
    """Mark the singular calculator face and force card color/padding in the live DOM."""
    st.markdown('<div id="pcs-face-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    components.html(
        """
<script>
(function () {
  var doc = window.parent.document;
  var CARD = "#314A3C";
  var FIELD = "#0B1210";  /* same dark chip as BAH/utilities rows */
  var PAD = "18px";  /* light-green frame around dark wells */
  var GAP = "8px";

  function force(el, prop, val) {
    if (el) el.style.setProperty(prop, val, "important");
  }

  function darkenFields(root) {
    /* Rank/posts + Wayfinder name/email — dark like BAH chips */
    var nodes = root.querySelectorAll(
      '#pcs-inputs-panel [data-baseweb="select"] > div, ' +
      '#pcs-inputs-panel [data-baseweb="select"] > div > div, ' +
      '#pcs-inputs-panel [data-testid="stSelectbox"] > div > div, ' +
      '#pcs-match-panel [data-baseweb="select"] > div, ' +
      '#pcs-match-panel [data-baseweb="select"] > div > div, ' +
      '#pcs-match-panel [data-testid="stSelectbox"] > div, ' +
      '#pcs-match-panel [data-testid="stSelectbox"] > div > div, ' +
      '#pcs-match-panel [data-testid="stTextInput"] input, ' +
      '.pcs-calc-face [data-testid="stTextInput"] input'
    );
    nodes.forEach(function (el) {
      force(el, "background", FIELD);
      force(el, "background-color", FIELD);
      force(el, "background-image", "none");
      force(el, "color", "#FFFFFF");
      force(el, "border-color", "rgba(255,255,255,0.18)");
    });
  }

  function collapseIframes(root) {
    root.querySelectorAll("iframe").forEach(function (frame) {
      force(frame, "height", "0");
      force(frame, "min-height", "0");
      force(frame, "margin", "0");
      force(frame, "padding", "0");
      force(frame, "border", "0");
      force(frame, "position", "absolute");
      force(frame, "opacity", "0");
      var host = frame.closest('[data-testid="stElementContainer"]') ||
                 frame.closest('[data-testid="element-container"]');
      if (host) {
        force(host, "height", "0");
        force(host, "min-height", "0");
        force(host, "margin", "0");
        force(host, "padding", "0");
        force(host, "overflow", "hidden");
      }
    });
  }

  function tightenWells(root) {
    var wells = root.querySelectorAll(
      "#pcs-inputs-panel, .pcs-face-section-inputs, .pcs-partner-results, .pcs-face-section-results, #pcs-match-panel, .pcs-face-section-match"
    );
    wells.forEach(function (well, i) {
      force(well, "margin-top", "0");
      force(well, "margin-bottom", i === wells.length - 1 ? "0" : GAP);
    });
  }

  function tag() {
    var marker = doc.getElementById("pcs-face-marker");
    if (!marker) return;
    var wrap =
      marker.closest('[data-testid="stVerticalBlockBorderWrapper"]') ||
      doc.querySelector(".st-key-pcs_calc_card") ||
      doc.querySelector('[class*="st-key-pcs_calc_card"]');
    if (!wrap) return;

    wrap.classList.add("pcs-calc-face");
    wrap.classList.add("pcs-calc-dark");
    force(wrap, "background", CARD);
    force(wrap, "background-color", CARD);
    force(wrap, "padding", PAD);
    force(wrap, "gap", "0");
    force(wrap, "row-gap", "0");

    var inner = wrap.firstElementChild;
    if (inner) {
      force(inner, "padding", "0");
      force(inner, "margin", "0");
      force(inner, "gap", "0");
      force(inner, "row-gap", "0");
      force(inner, "background", "transparent");
    }

    wrap.querySelectorAll('[data-testid="stVerticalBlock"]').forEach(function (vb) {
      force(vb, "gap", "0");
      force(vb, "row-gap", "0");
    });

    collapseIframes(wrap);
    tightenWells(wrap);
    darkenFields(wrap);
    doc.documentElement.classList.add("pcs-dark-app");
    doc.body.classList.add("pcs-dark-app");
  }

  var t = null;
  function schedule() {
    if (t) clearTimeout(t);
    t = setTimeout(tag, 40);
  }
  tag();
  [50, 150, 350, 700, 1400, 2500].forEach(function (ms) { setTimeout(tag, ms); });
  try {
    var obs = new MutationObserver(schedule);
    obs.observe(doc.body, { childList: true, subtree: true });
  } catch (e) {}
})();
</script>
        """,
        height=0,
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
        bottom: max(0.65rem, env(safe-area-inset-bottom));
        z-index: 99999;
        width: min(560px, calc(100vw - 1.25rem));
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.55rem;
        padding: 0.65rem 0.75rem;
        border-radius: 14px;
        background: #1C2D22;
        color: #FFFFFF;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.18);
        font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
        transition: opacity 0.2s ease, transform 0.2s ease;
        backdrop-filter: blur(8px);
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
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #F0D060;
        margin-bottom: 0.12rem;
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-line {{
        font-size: 0.8rem;
        font-weight: 700;
        color: #FFFFFF;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-btn {{
        flex-shrink: 0;
        appearance: none;
        border: none;
        cursor: pointer;
        background: #FB923C;
        color: #fff;
        font-weight: 900;
        font-size: 0.8rem;
        letter-spacing: -0.01em;
        padding: 0.55rem 0.85rem;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(251, 146, 60, 0.45);
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-btn:hover {{
        background: #F97316;
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
      '<div class="pcs-sticky-ref-kicker">Step 2 · Free housing help</div>' +
      '<div class="pcs-sticky-ref-line" title="' +
        String(data.destFull).replace(/"/g, "&quot;") +
      '">' +
        String(data.dest) + " · " + String(data.rank) + " · " + String(data.deps) +
      "</div>" +
    "</div>" +
    '<button type="button" class="pcs-sticky-ref-btn" id="pcs-sticky-ref-go">Get free help →</button>';

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
    ready = bool(dest)

    # Compact contact strip → orange CTA (not st.form — forms inject
    # "Press Enter to submit form" tooltips on every text field)
    st.markdown('<div id="pcs-match-start"></div><div id="pcs-referral"></div>', unsafe_allow_html=True)

    n1, n2 = st.columns(2)
    with n1:
        first_name = st.text_input(
            "First name",
            key="referral_first_name",
            placeholder="First",
        )
    with n2:
        email_address = st.text_input(
            "Email",
            key="referral_email_address",
            placeholder="you@email.com",
        )

    submitted = st.button(
        "Connect With A PCS Wayfinder ➔",
        type="primary",
        use_container_width=True,
        disabled=not ready,
        key="referral_submit_btn",
    )
    st.caption("PCS Wayfinders are our military-approved local agents — Free")

    if submitted:
        first_name = str(st.session_state.get("referral_first_name") or first_name or "")
        email_address = _clean_email(
            st.session_state.get("referral_email_address") or email_address
        )

        live = get_calculator_snapshot() or snap
        live_calc = _calc_fields_from_snap(live)

        live_deps_n = int(live.get("num_dependents") or 0)
        row = build_referral_row(
            destination=live_calc["destination"],
            first_name=first_name,
            rank=live_calc["rank"],
            num_dependents=live_deps_n,
            email_address=email_address,
        )

        if not live_calc["destination"]:
            st.error("Set New post in the calculator above first.")
        elif not row["First Name"].strip():
            st.error("Enter your first name.")
        elif not _is_valid_email(row["Email address"]):
            st.error("Enter a valid email address (example: name@email.com).")
        else:
            st.session_state.referral_lead = {**row, "calculator": live}

            submit_referral_via_apps_script(row)

            st.html(
                build_redirect_to_form_html(row),
                unsafe_allow_javascript=True,
            )
            st.success("Opening your pre-filled form — tap **Submit** on the next page.")

    st.markdown('<div id="pcs-match-end"></div>', unsafe_allow_html=True)
    wrap_dom_panel(
        start_id="pcs-match-start",
        end_id="pcs-match-end",
        panel_id="pcs-match-panel",
        panel_class="pcs-face-section pcs-face-section-match",
    )

    _render_sticky_referral_cta(calc)


def _render_faq() -> None:
    render_home_faq()


def render_home() -> None:
    # Loud brand ABOVE the calculator — card itself is pure instrument
    st.markdown(
        """
        <div class="pcs-page-brand">
            <div class="pcs-brand-title">PCS Vector</div>
            <div class="pcs-face-tagline">For Soldiers; By Soldiers</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True, key="pcs_calc_card"):
        _tag_page_face()
        render_bah_calculator()
        _render_referral_hook()

    _render_faq()
    st.markdown(
        """
        <div class="pcs-footer">
            <span>Verify LES / finance before you sign.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

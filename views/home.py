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


def _tag_page_face() -> None:
    """Mark calculator face, inject double-border CSS+DOM, kill blue labels."""
    st.markdown('<div id="pcs-face-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    components.html(
        """
<script>
(function () {
  var doc = window.parent.document;

  // Inject double-border CSS into parent (guaranteed to apply)
  var styleId = "pcs-dbl-frame-style";
  if (!doc.getElementById(styleId)) {
    var css = doc.createElement("style");
    css.id = styleId;
    css.textContent = `
      .pcs-dbl-shell {
        background: #1C2D22 !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-radius: 18px !important;
        padding: 10px !important;
        box-shadow: 0 20px 44px rgba(0, 0, 0, 0.48) !important;
        max-width: 36rem;
        margin: 0.35rem auto !important;
      }
      .pcs-dbl-pad {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
      }
      .pcs-dbl-inner {
        display: block;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
      }
      .pcs-calc-face [data-testid="stWidgetLabel"] p,
      .pcs-calc-face label p {
        color: #A3ADB6 !important;
      }
      .pcs-calc-face [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stWidgetLabel"] p {
        color: #D4AF37 !important;
      }
      /* Kill Streamlit light fills inside the instrument */
      .pcs-calc-face [data-baseweb="select"] > div,
      .pcs-calc-face input {
        background-color: rgba(0, 0, 0, 0.48) !important;
        color: #FFFFFF !important;
      }
    `;
    doc.head.appendChild(css);
  }

  function tag() {
    var marker = doc.getElementById("pcs-face-marker");
    if (!marker) return;
    var wrap = marker.closest('[data-testid="stVerticalBlockBorderWrapper"]');
    if (wrap) {
      wrap.classList.add("pcs-calc-face");
      wrap.classList.add("pcs-calc-dark");
      // Make wrapper transparent so dbl-shell is the visible frame
      wrap.style.setProperty("background", "transparent", "important");
      wrap.style.setProperty("border", "none", "important");
      wrap.style.setProperty("padding", "0", "important");
      wrap.style.setProperty("box-shadow", "none", "important");
      wrap.style.setProperty("outline", "none", "important");

      var shell = wrap.querySelector(".pcs-dbl-shell");
      if (!shell) {
        shell = doc.createElement("div");
        shell.className = "pcs-dbl-shell";
        var pad = doc.createElement("div");
        pad.className = "pcs-dbl-pad";
        var inner = doc.createElement("div");
        inner.className = "pcs-dbl-inner";
        while (wrap.firstChild) {
          inner.appendChild(wrap.firstChild);
        }
        pad.appendChild(inner);
        shell.appendChild(pad);
        wrap.appendChild(shell);
      } else {
        // Scoop late-arriving Streamlit siblings into the frame
        var inner = shell.querySelector(".pcs-dbl-inner");
        if (inner) {
          Array.from(wrap.children).forEach(function (child) {
            if (child !== shell) inner.appendChild(child);
          });
        }
      }
    }
    doc.documentElement.classList.add("pcs-dark-app");
    doc.body.classList.add("pcs-dark-app");
    // Force labels off Streamlit blue (#1e3a5f)
    doc.querySelectorAll(
      '.pcs-calc-face [data-testid="stWidgetLabel"] p, .pcs-calc-face label p, .pcs-calc-face label span'
    ).forEach(function (el) {
      if (el.closest('[data-testid="stCheckbox"]') || el.closest('[data-testid="stRadio"]')) {
        el.style.setProperty("color", "#C8D0D8", "important");
      } else {
        el.style.setProperty("color", "#A3ADB6", "important");
      }
    });
    doc.querySelectorAll(
      '.pcs-calc-face [data-testid="stHorizontalBlock"] > div:first-child [data-testid="stWidgetLabel"] p'
    ).forEach(function (el) {
      el.style.setProperty("color", "#D4AF37", "important");
    });
    // Force app chrome off cream / light defaults
    doc.documentElement.style.background = "#121E16";
    if (doc.body) doc.body.style.background = "#121E16";
    var app = doc.querySelector(".stApp");
    if (app) app.style.setProperty("background", "#121E16", "important");
  }
  tag();
  [40, 160, 400, 800, 1500].forEach(function (ms) { setTimeout(tag, ms); });
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
        padding-bottom: 6.5rem !important;
      }}
      html.pcs-has-sticky-ref .block-container {{
        padding-bottom: 8rem !important;
      }}
      #pcs-sticky-ref-bar {{
        position: fixed;
        left: 50%;
        transform: translateX(-50%);
        bottom: max(0.5rem, env(safe-area-inset-bottom));
        z-index: 99999;
        width: min(560px, calc(100vw - 1rem));
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        padding: 0.55rem 0.65rem;
        min-height: 52px;
        border-radius: 14px;
        background: #1C2D22;
        color: #FFFFFF;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.14);
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
        font-size: 0.6rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #D4AF37;
        margin-bottom: 0.1rem;
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-line {{
        font-size: 0.76rem;
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
        background: #EA580C;
        color: #fff;
        font-weight: 900;
        font-size: 0.78rem;
        letter-spacing: -0.01em;
        min-height: 44px;
        padding: 0.55rem 0.85rem;
        border-radius: 10px;
        box-shadow: 0 4px 14px rgba(234, 88, 12, 0.4);
      }}
      #pcs-sticky-ref-bar .pcs-sticky-ref-btn:hover {{
        background: #C2410C;
      }}
      @media (max-width: 430px) {{
        #pcs-sticky-ref-bar {{
          bottom: max(0.4rem, env(safe-area-inset-bottom));
          padding: 0.5rem 0.55rem;
          gap: 0.4rem;
        }}
        #pcs-sticky-ref-bar .pcs-sticky-ref-line {{
          font-size: 0.7rem;
        }}
        #pcs-sticky-ref-bar .pcs-sticky-ref-btn {{
          font-size: 0.72rem;
          padding: 0.5rem 0.65rem;
          min-height: 44px;
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
      '<div class="pcs-sticky-ref-kicker">Free housing match</div>' +
      '<div class="pcs-sticky-ref-line" title="' +
        String(data.destFull).replace(/"/g, "&quot;") +
      '">' +
        String(data.dest) + " · " + String(data.rank) + " · " + String(data.deps) +
      "</div>" +
    "</div>" +
    '<button type="button" class="pcs-sticky-ref-btn" id="pcs-sticky-ref-go">Get matched</button>';

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

    # Compact contact strip → orange CTA (PVector.html bottom pattern)
    st.markdown('<div id="pcs-match-start"></div><div id="pcs-referral"></div>', unsafe_allow_html=True)
    # Disable browser "Please fill out this field" / enter-to-submit tooltips
    components.html(
        """
<script>
(function () {
  var doc = window.parent.document;
  function disarm() {
    doc.querySelectorAll('form').forEach(function (f) {
      f.setAttribute('novalidate', 'novalidate');
      f.setAttribute('autocomplete', 'on');
    });
    doc.querySelectorAll('input').forEach(function (inp) {
      inp.removeAttribute('required');
      inp.setAttribute('aria-required', 'false');
    });
  }
  disarm();
  [50, 200, 500].forEach(function (ms) { setTimeout(disarm, ms); });
})();
</script>
        """,
        height=0,
    )

    with st.form("referral_form", clear_on_submit=False):
        n1, n2 = st.columns(2)
        with n1:
            first_name = st.text_input(
                "First name",
                key="referral_first_name",
                placeholder="First",
            )
        with n2:
            last_name = st.text_input(
                "Last name",
                key="referral_last_name",
                placeholder="Last",
            )

        email_address = st.text_input(
            "Email",
            key="referral_email_address",
            placeholder="you@email.com",
        )

        rent_buy_not_sure = st.selectbox(
            "Looking to…",
            options=list(INTEREST_OPTIONS),
            key="referral_rent_buy_not_sure",
        )

        submitted = st.form_submit_button(
            "Get matched ➔",
            type="primary",
            use_container_width=True,
            disabled=not ready,
        )
        st.caption("Free housing help · CONUS & OCONUS")

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
            st.success("Opening your pre-filled form — tap **Submit** on the next page.")

    with st.expander("FAQ — what these numbers mean", expanded=False):
        st.markdown(
            """
<div class="pcs-faq-grid">
  <div class="pcs-faq-item"><strong>Free?</strong><span>Yes — calculator and housing match.</span></div>
  <div class="pcs-faq-item"><strong>BAH</strong><span>U.S. housing pay. Keep leftover if rent is lower.</span></div>
  <div class="pcs-faq-item"><strong>OHA</strong><span>Overseas rent max + utilities allowance.</span></div>
  <div class="pcs-faq-item"><strong>COLA</strong><span>OCONUS daily-cost extra. Not for rent.</span></div>
  <div class="pcs-faq-item"><strong>DLA</strong><span>One-time move money when authorized.</span></div>
  <div class="pcs-faq-item"><strong>Estimates</strong><span>Rent/utilities are planning ranges.</span></div>
  <div class="pcs-faq-item"><strong>Rent % badge</strong><span>Typical rent mid change — not official COL.</span></div>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div id="pcs-match-end"></div>', unsafe_allow_html=True)
    wrap_dom_panel(
        start_id="pcs-match-start",
        end_id="pcs-match-end",
        panel_id="pcs-match-panel",
        panel_class="pcs-face-section pcs-face-section-match",
    )

    _render_sticky_referral_cta(calc)


def render_home() -> None:
    with st.container(border=True):
        _tag_page_face()
        render_bah_calculator()
        _render_referral_hook()
        st.markdown(
            """
            <div class="pcs-footer">
                <strong>PCS Vector</strong> · For Soldiers; By Soldiers
                <span>Verify LES / finance before you sign.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

"""Scroll helpers for page and widget UX."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

SCROLL_TO_TOP_FLAG = "_scroll_to_top"


def request_scroll_to_top() -> None:
    """Request a scroll-to-top on the next rerun."""
    st.session_state[SCROLL_TO_TOP_FLAG] = True


def _scroll_top_script(*, clear_hash: bool, aggressive: bool = False) -> str:
    clear = "true" if clear_hash else "false"
    aggressive_js = "true" if aggressive else "false"
    return f"""
<script>
(function () {{
  var doc = window.parent.document;
  var win = window.parent;
  var clearHash = {clear};
  var aggressive = {aggressive_js};

  function scrollAllToTop() {{
    try {{
      if (win.history && "scrollRestoration" in win.history) {{
        win.history.scrollRestoration = "manual";
      }}
    }} catch (err) {{}}

    if (clearHash) {{
      try {{
        var url = win.location;
        if (url.hash) {{
          win.history.replaceState(null, "", url.pathname + url.search);
        }}
      }} catch (err) {{}}
    }}

    try {{
      win.scrollTo({{ top: 0, left: 0, behavior: "instant" }});
    }} catch (err) {{
      try {{ win.scrollTo(0, 0); }} catch (e2) {{}}
    }}
    try {{
      if (doc.documentElement) doc.documentElement.scrollTop = 0;
      if (doc.body) doc.body.scrollTop = 0;
    }} catch (err) {{}}

    var selectors = [
      '[data-testid="stAppViewContainer"]',
      '[data-testid="stMain"]',
      '[data-testid="stMainBlockContainer"]',
      "section.main",
      ".main",
      ".block-container",
      '[data-testid="stAppViewBlockContainer"]',
    ];
    selectors.forEach(function (selector) {{
      doc.querySelectorAll(selector).forEach(function (el) {{
        try {{ el.scrollTop = 0; }} catch (e) {{}}
      }});
    }});

    var anchor = doc.getElementById("pcs-page-top");
    if (anchor && anchor.scrollIntoView) {{
      try {{
        anchor.scrollIntoView({{ block: "start", behavior: "instant" }});
      }} catch (err) {{
        try {{ anchor.scrollIntoView(true); }} catch (e2) {{}}
      }}
    }}

    // Stop Streamlit/widget autofocus from jumping mid-page on load
    if (aggressive) {{
      try {{
        var ae = doc.activeElement;
        if (ae && ae !== doc.body && typeof ae.blur === "function") {{
          var tag = (ae.tagName || "").toLowerCase();
          if (tag === "input" || tag === "select" || tag === "textarea" || ae.getAttribute("role") === "combobox") {{
            ae.blur();
          }}
        }}
      }} catch (err) {{}}
    }}
  }}

  scrollAllToTop();
  [0, 50, 100, 200, 400, 700, 1200, 2000].forEach(function (delay) {{
    setTimeout(scrollAllToTop, delay);
  }});

  if (aggressive) {{
    try {{
      win.addEventListener("pageshow", function () {{ scrollAllToTop(); }});
      win.addEventListener("load", function () {{ scrollAllToTop(); }});
      doc.addEventListener("DOMContentLoaded", function () {{ scrollAllToTop(); }});
    }} catch (err) {{}}
  }}
}})();
</script>
"""


def render_scroll_to_top() -> None:
    """Scroll the main view to the top when requested.

    Call this AFTER page content renders so the DOM is ready.
    Uses instant scroll first, then retries for Streamlit's async layout.
    """
    if not st.session_state.pop(SCROLL_TO_TOP_FLAG, False):
        return

    components.html(_scroll_top_script(clear_hash=False), height=0)


def render_boot_at_top() -> None:
    """On home load: strip hashes, disable scroll restoration, force top.

    Mobile Safari restores mid-page scroll; Streamlit widgets/iframes can also
    jump the viewport away from the title. Call at start AND end of the page.
    """
    components.html(
        _scroll_top_script(clear_hash=True, aggressive=True),
        height=0,
    )


def render_page_top_anchor() -> None:
    """Invisible anchor at the top of main content for scroll targeting."""
    st.markdown(
        '<div id="pcs-page-top" style="height:0;margin:0;padding:0;overflow:hidden;"></div>',
        unsafe_allow_html=True,
    )


def render_dropdown_scroll_fix() -> None:
    """Prevent page jump when select/multiselect popovers open; reset list scroll."""
    components.html(
        """<script>
            (function () {
                if (window.__pcsDropdownScrollFix) {
                    return;
                }
                window.__pcsDropdownScrollFix = true;

                const doc = window.parent.document;
                let savedMainScroll = 0;

                function getMainScrollEl() {
                    return (
                        doc.querySelector('[data-testid="stAppViewContainer"]') ||
                        doc.querySelector("section.main") ||
                        doc.querySelector(".main")
                    );
                }

                function saveScrollPosition() {
                    const main = getMainScrollEl();
                    savedMainScroll = main ? main.scrollTop : 0;
                }

                function restoreScrollPosition() {
                    const main = getMainScrollEl();
                    if (main) {
                        main.scrollTop = savedMainScroll;
                    }
                }

                function resetPopoverScroll() {
                    doc.querySelectorAll('[data-baseweb="popover"] ul').forEach(function (list) {
                        list.scrollTop = 0;
                    });
                }

                doc.addEventListener(
                    "mousedown",
                    function (event) {
                        const target = event.target;
                        if (
                            target.closest('[data-baseweb="select"]') ||
                            target.closest('[data-baseweb="popover"]') ||
                            target.closest('[data-testid="stMultiSelect"]') ||
                            target.closest('[data-testid="stSelectbox"]')
                        ) {
                            saveScrollPosition();
                        }
                    },
                    true
                );

                const observer = new MutationObserver(function () {
                    const popover = doc.querySelector('[data-baseweb="popover"]');
                    if (popover) {
                        resetPopoverScroll();
                        requestAnimationFrame(restoreScrollPosition);
                        setTimeout(restoreScrollPosition, 0);
                        setTimeout(restoreScrollPosition, 80);
                    }
                });

                observer.observe(doc.body, { childList: true, subtree: true });

                doc.addEventListener(
                    "click",
                    function () {
                        setTimeout(function () {
                            resetPopoverScroll();
                            restoreScrollPosition();
                        }, 0);
                    },
                    true
                );
            })();
        </script>""",
        height=0,
    )

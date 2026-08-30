"""Scroll helpers for page and widget UX."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

SCROLL_TO_TOP_FLAG = "_scroll_to_top"

# Injected into the MAIN document via st.html (no iframe → no scroll-to-iframe jump).
_BOOT_TOP_JS = """
<script>
(function () {
  if (window.__pcsBootTopInstalled) {
    // Still re-run a scroll pass on every Streamlit rerender
  } else {
    window.__pcsBootTopInstalled = true;
  }

  function scrollAllToTop() {
    try {
      if (history && "scrollRestoration" in history) {
        history.scrollRestoration = "manual";
      }
    } catch (err) {}

    try {
      if (location.hash) {
        history.replaceState(null, "", location.pathname + location.search);
      }
    } catch (err) {}

    try {
      window.scrollTo({ top: 0, left: 0, behavior: "instant" });
    } catch (err) {
      try { window.scrollTo(0, 0); } catch (e2) {}
    }
    try {
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
    } catch (err) {}

    var selectors = [
      '[data-testid="stAppViewContainer"]',
      '[data-testid="stMain"]',
      '[data-testid="stMainBlockContainer"]',
      "section.main",
      ".main",
      ".block-container",
      '[data-testid="stAppViewBlockContainer"]',
    ];
    selectors.forEach(function (selector) {
      document.querySelectorAll(selector).forEach(function (el) {
        try { el.scrollTop = 0; } catch (e) {}
      });
    });

    var anchor = document.getElementById("pcs-page-top");
    if (anchor && anchor.scrollIntoView) {
      try {
        anchor.scrollIntoView({ block: "start", behavior: "instant" });
      } catch (err) {
        try { anchor.scrollIntoView(true); } catch (e2) {}
      }
    }

    // Blur autofocused fields that pull the viewport mid-page
    try {
      var ae = document.activeElement;
      if (ae && ae !== document.body && typeof ae.blur === "function") {
        var tag = (ae.tagName || "").toLowerCase();
        if (
          tag === "input" ||
          tag === "select" ||
          tag === "textarea" ||
          tag === "button" ||
          ae.getAttribute("role") === "combobox" ||
          ae.getAttribute("role") === "listbox"
        ) {
          ae.blur();
        }
      }
    } catch (err) {}

    // Park zero-height component iframes off-screen so they can't steal scroll
    try {
      document.querySelectorAll("iframe").forEach(function (frame) {
        var h = frame.getAttribute("height");
        if (h === "0" || frame.clientHeight < 4) {
          frame.setAttribute("tabindex", "-1");
          frame.style.setProperty("position", "fixed", "important");
          frame.style.setProperty("left", "-9999px", "important");
          frame.style.setProperty("top", "0", "important");
          frame.style.setProperty("width", "0", "important");
          frame.style.setProperty("height", "0", "important");
          frame.style.setProperty("opacity", "0", "important");
          frame.style.setProperty("pointer-events", "none", "important");
          var host =
            frame.closest('[data-testid="stElementContainer"]') ||
            frame.closest('[data-testid="element-container"]');
          if (host) {
            host.style.setProperty("height", "0", "important");
            host.style.setProperty("min-height", "0", "important");
            host.style.setProperty("margin", "0", "important");
            host.style.setProperty("padding", "0", "important");
            host.style.setProperty("overflow", "hidden", "important");
          }
        }
      });
    } catch (err) {}
  }

  scrollAllToTop();
  [0, 50, 100, 200, 400, 800, 1500, 2500, 4000].forEach(function (delay) {
    setTimeout(scrollAllToTop, delay);
  });

  if (!window.__pcsBootTopListeners) {
    window.__pcsBootTopListeners = true;
    window.addEventListener("pageshow", function () { scrollAllToTop(); });
    window.addEventListener("load", function () { scrollAllToTop(); });
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "visible") scrollAllToTop();
    });
  }
})();
</script>
"""


def request_scroll_to_top() -> None:
    """Request a scroll-to-top on the next rerun."""
    st.session_state[SCROLL_TO_TOP_FLAG] = True


def _inject_main_doc_script(script_html: str) -> None:
    """Run JS in the main Streamlit document (avoids iframe scroll jumps)."""
    try:
        st.html(script_html)
    except Exception:
        st.markdown(script_html, unsafe_allow_html=True)


def render_scroll_to_top() -> None:
    """Scroll the main view to the top when requested."""
    if not st.session_state.pop(SCROLL_TO_TOP_FLAG, False):
        return
    _inject_main_doc_script(_BOOT_TOP_JS)


def render_boot_at_top() -> None:
    """Force the page to open at the top on load / phone reload.

    Uses st.html in the main document — NOT components.html iframes.
    Mid/bottom iframes are a common cause of “opens halfway down the page.”
    """
    _inject_main_doc_script(_BOOT_TOP_JS)


def render_page_top_anchor() -> None:
    """Invisible anchor at the top of main content for scroll targeting."""
    st.markdown(
        '<div id="pcs-page-top" style="height:0;margin:0;padding:0;overflow:hidden;" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )


def render_dropdown_scroll_fix() -> None:
    """Prevent page jump when select/multiselect popovers open; reset list scroll."""
    # Keep this as components.html (needs early parent hook); boot script parks iframes off-screen.
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

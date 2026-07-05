"""Scroll helpers for page and widget UX."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

SCROLL_TO_TOP_FLAG = "_scroll_to_top"


def request_scroll_to_top() -> None:
    """Request a scroll-to-top on the next rerun."""
    st.session_state[SCROLL_TO_TOP_FLAG] = True


def render_scroll_to_top() -> None:
    """Scroll the main view to the top when requested."""
    if not st.session_state.pop(SCROLL_TO_TOP_FLAG, False):
        return

    components.html(
        """<script>
            (function () {
                function scrollTop() {
                    try {
                        window.parent.scrollTo({ top: 0, left: 0, behavior: "smooth" });
                    } catch (err) {
                        window.parent.scrollTo(0, 0);
                    }
                    const main = window.parent.document.querySelector("section.main");
                    if (main) {
                        main.scrollTop = 0;
                    }
                }
                scrollTop();
                setTimeout(scrollTop, 120);
            })();
        </script>""",
        height=0,
    )


def render_dropdown_scroll_fix() -> None:
    """Reset BaseWeb select/multiselect popover scroll position when opened."""
    components.html(
        """<script>
            (function () {
                if (window.__pcsDropdownScrollFix) {
                    return;
                }
                window.__pcsDropdownScrollFix = true;

                function resetPopoverScroll() {
                    const doc = window.parent.document;
                    doc.querySelectorAll('[data-baseweb="popover"] ul').forEach(function (list) {
                        list.scrollTop = 0;
                    });
                }

                const observer = new MutationObserver(function () {
                    resetPopoverScroll();
                });

                observer.observe(window.parent.document.body, {
                    childList: true,
                    subtree: true,
                });

                window.parent.document.addEventListener("click", function () {
                    setTimeout(resetPopoverScroll, 0);
                }, true);
            })();
        </script>""",
        height=0,
    )
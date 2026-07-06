"""Scroll helpers for page and widget UX."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

SCROLL_TO_TOP_FLAG = "_scroll_to_top"


def request_scroll_to_top() -> None:
    """Request a scroll-to-top on the next rerun."""
    st.session_state[SCROLL_TO_TOP_FLAG] = True


def render_scroll_to_top() -> None:
    """Scroll the main view to the top when requested.

    Call this AFTER page content renders so the DOM is ready.
    Uses instant scroll first, then retries for Streamlit's async layout.
    """
    if not st.session_state.pop(SCROLL_TO_TOP_FLAG, False):
        return

    components.html(
        """<script>
            (function () {
                const doc = window.parent.document;

                function scrollAllToTop() {
                    try {
                        window.parent.scrollTo({ top: 0, left: 0, behavior: "auto" });
                    } catch (err) {
                        window.parent.scrollTo(0, 0);
                    }

                    const selectors = [
                        '[data-testid="stAppViewContainer"]',
                        '[data-testid="stMain"]',
                        "section.main",
                        ".main",
                        ".block-container",
                    ];

                    selectors.forEach(function (selector) {
                        doc.querySelectorAll(selector).forEach(function (el) {
                            el.scrollTop = 0;
                        });
                    });

                    const anchor = doc.getElementById("pcs-page-top");
                    if (anchor && anchor.scrollIntoView) {
                        anchor.scrollIntoView({ block: "start", behavior: "auto" });
                    }
                }

                scrollAllToTop();
                [50, 150, 350, 600].forEach(function (delay) {
                    setTimeout(scrollAllToTop, delay);
                });
            })();
        </script>""",
        height=0,
    )


def render_page_top_anchor() -> None:
    """Invisible anchor at the top of main content for scroll targeting."""
    st.markdown('<div id="pcs-page-top"></div>', unsafe_allow_html=True)


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
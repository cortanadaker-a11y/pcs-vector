"""
PCS Vector has moved to https://pcsvector.com/ (sole source as of 19 Oct 2026).

This Streamlit app is retired to a redirect page. The full calculator app is in git
history: tag `streamlit-final-2026-10-18`.

How the redirect works on Streamlit Community Cloud: the app document runs inside an
iframe (/~/+/) sandboxed WITHOUT allow-top-navigation, so window.top.location from the
app is blocked. All frames are same-origin, so the component instead injects a script
and a <meta http-equiv="refresh"> into the top-level (unsandboxed) document, which then
navigates itself. The big link opens pcsvector.com in a new tab
(allow-popups-to-escape-sandbox) if both are blocked.

The single canonical (https://pcsvector.com/) is written into the head of every
same-origin ancestor document. Streamlit Cloud serves Googlebot a prerendered snapshot
and adds its own canonical to pcsvector.streamlit.app; the script rewrites it.
"""

import json

import streamlit as st
import streamlit.components.v1 as components

SITE_URL = "https://pcsvector.com/"

st.set_page_config(
    page_title="PCS Vector has moved to pcsvector.com",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"""
<div style="text-align:center;padding:12vh 8px 0">
  <h1 style="font-size:2rem;line-height:1.25;margin:0 0 .6rem">PCS Vector has moved to pcsvector.com</h1>
  <p style="font-size:1.05rem;opacity:.85;margin:0 0 1.6rem">Same free calculator: BAH, OHA, COLA, rent, utilities and gas. Taking you there now&hellip;</p>
  <a href="{SITE_URL}" target="_blank" rel="noopener"
     style="display:inline-block;background:#EA580C;color:#fff;text-decoration:none;font-weight:700;
            font-size:1.35rem;padding:18px 34px;border-radius:12px">Go to pcsvector.com &#10132;</a>
  <p style="font-size:.85rem;opacity:.6;margin-top:1.4rem">Unofficial. Not affiliated with the U.S. Department of Defense.</p>
</div>
""",
    unsafe_allow_html=True,
)

_site_js = json.dumps(SITE_URL)
components.html(
    f"""
<script>
(function () {{
  var site = {_site_js};
  // Same-origin ancestors: Cloud wrapper (top) and the app document (parent); locally both are the same.
  var docs = [];
  [window.parent, window.top].forEach(function (w) {{
    try {{ if (w && w.document && docs.indexOf(w.document) === -1) docs.push(w.document); }} catch (e) {{}}
  }});
  docs.forEach(function (doc) {{
    var head = doc.head;
    function fixCanonical() {{
      var links = head.querySelectorAll('link[rel="canonical"]');
      if (!links.length) {{
        var link = doc.createElement("link");
        link.setAttribute("rel", "canonical");
        link.setAttribute("href", site);
        head.appendChild(link);
        return;
      }}
      // Exactly one canonical, pointing at the static site.
      for (var i = 0; i < links.length; i++) {{
        if (i === 0) {{ if (links[i].getAttribute("href") !== site) links[i].setAttribute("href", site); }}
        else links[i].remove();
      }}
    }}
    fixCanonical();
    var MO = doc.defaultView && doc.defaultView.MutationObserver;
    if (!doc.__pcsCanonObs && MO) {{
      doc.__pcsCanonObs = new MO(fixCanonical);
      doc.__pcsCanonObs.observe(head, {{ childList: true, subtree: true, attributes: true, attributeFilter: ["href"] }});
    }}
  }});
  // Redirect: run in the top-level document (not sandboxed). Keeps any ?query / #hash.
  var topDoc = docs[docs.length - 1];
  if (!topDoc || topDoc.__pcsRedirect) return;
  topDoc.__pcsRedirect = true;
  var loc = topDoc.defaultView.location;
  var dest = site + (loc.search || "") + (loc.hash || "");
  var meta = topDoc.createElement("meta");
  meta.setAttribute("http-equiv", "refresh");
  meta.setAttribute("content", "1;url=" + dest);
  topDoc.head.appendChild(meta);
  var s = topDoc.createElement("script");
  s.textContent = "location.replace(" + JSON.stringify(dest) + ");";
  topDoc.head.appendChild(s);
}})();
</script>
""",
    height=0,
)

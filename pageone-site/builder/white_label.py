# White label (Edwin, 12 Nov 2026): a short homepage section for agencies and resellers, and two live numbers on
# /clients/ (live white-label client sites, sites being built) read from the Controller's public clientCounts feed.
# PREVIEW ONLY until Edwin OKs it: with WL_LIVE = False the live pages stay as they are, and the build writes a
# noindex, nofollow copy of the homepage and /clients/ to WL_PREVIEW (not linked from the live site, not in any
# sitemap or llms file, because noindex pages are skipped by page()). Going live = set WL_LIVE = True and rebuild.
# Never name a white-label partner here (text, alt, schema, comments or file names).
# Run from build.py (exec) before showcase.py and the homepage.

WL_LIVE = False
WL_PREVIEW = "preview/pageone/white-label/"   # the "pageone" preview folder is skipped by the Controller's client import
WL_COUNTS_URL = API + "/clientCounts"          # returns only {ok, white_label_live, building}; no secret needed
WL_WA_TEXT = "Hi Edwin, I run an agency / resell websites. I'd like to know more about white label websites under my own brand."


def white_label_section():
    """Homepage block: heading, one or two short lines, WhatsApp CTA with a white-label prefill."""
    return f"""    <!-- WHITE LABEL: agencies and resellers -->
    <section class="section wl-band" id="white-label">
      <div class="wrap narrow">
        <p class="kicker reveal">For agencies and resellers</p>
        <h2 class="reveal">We welcome white label</h2>
        <p class="section-lead reveal">We build and run websites under your brand, with our daily Google and AI search work behind them. No Page One name on your client's site.</p>
        <div class="cta-row reveal">
          <a class="btn" href="{wa_src(WL_WA_TEXT, 'homepage, white label')}" target="_blank" rel="noopener" data-cta="whatsapp_home_white_label">Ask about white label</a>
        </div>
      </div>
    </section>

"""


WL_CSS = (" .wl-band{background:var(--bg-alt)} .wl-band .section-lead{margin-bottom:20px}"
          " .wl-counts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:0 0 28px}"
          " .wl-counts[hidden]{display:none} .wl-counts .kpi{padding:16px} .wl-counts .label{overflow-wrap:anywhere}")


def client_counts_block():
    """/clients/ block: two numbers, hidden until the Controller feed answers. No names, no domains."""
    return """        <div class="wl-counts" id="client-counts" hidden aria-live="polite">
          <div class="kpi"><div class="label">White-label client sites live</div><div class="value" data-count="white_label_live"></div></div>
          <div class="kpi"><div class="label">Client websites being built now</div><div class="value" data-count="building"></div></div>
        </div>
"""


# Shows the block only when the feed answers with two whole numbers; on any error or timeout it stays hidden.
WL_COUNTS_JS = """
  <script>(function(){var b=document.getElementById("client-counts");if(!b||!window.fetch)return;var c=window.AbortController?new AbortController():null;var t=setTimeout(function(){c&&c.abort()},5000);
fetch(\"""" + WL_COUNTS_URL + """\",{signal:c?c.signal:undefined}).then(function(r){return r.ok?r.json():null}).then(function(d){clearTimeout(t);if(!d||d.ok!==true)return;var ok=true;
b.querySelectorAll("[data-count]").forEach(function(e){var v=d[e.getAttribute("data-count")];if(typeof v!=="number"||v<0||Math.floor(v)!==v){ok=false}else{e.textContent=String(v)}});if(ok)b.hidden=false}).catch(function(){clearTimeout(t)});})();</script>"""


def wl_preview_links(html):
    """Inside the preview copy, the homepage's /clients/ links point at the preview /clients/ page."""
    return html.replace('href="/clients/"', f'href="/{WL_PREVIEW}clients/"')

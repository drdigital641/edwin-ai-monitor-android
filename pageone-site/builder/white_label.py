# White label (Edwin, 12 Nov 2026): a short homepage section for agencies and resellers, and two live numbers on
# /clients/ (live white-label client sites, sites being built) read from the Controller's public clientCounts feed.
# Edwin approved go-live 12 Nov 2026 9:41pm SGT (WL_LIVE = True). The "being built" number on the homepage and
# /clients/ (lead text, growth chart, marquee, portfolio line) also comes only from this feed: nothing is hard-coded,
# and when the feed can't be reached every place that shows it stays hidden.
# Never name a white-label partner here (text, alt, schema, comments or file names).
# Run from build.py (exec) before showcase.py and the homepage.

WL_LIVE = True
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
          " .wl-counts[hidden],.grow .g[hidden]{display:none} .wl-counts .kpi{padding:16px} .wl-counts .label{overflow-wrap:anywhere}")


def client_counts_block():
    """/clients/ block: two numbers, hidden until the Controller feed answers. No names, no domains."""
    return """        <div class="wl-counts" id="client-counts" hidden aria-live="polite">
          <div class="kpi"><div class="label">White-label client sites live</div><div class="value" data-count="white_label_live"></div></div>
          <div class="kpi"><div class="label">Client websites being built now</div><div class="value" data-count="building"></div></div>
        </div>
"""


def count_span(key, pre="", post=""):
    """Inline text with a live number, e.g. ", 9 more are being built". Hidden until the feed fills it."""
    return f'<span data-count-wrap hidden>{pre}<span data-count="{key}"></span>{post}</span>'


def build_bar(top):
    """Growth chart bar for sites being built; its height comes from the live count (top = tallest live bar)."""
    return (f'<div class="g b" data-count-bar="building" data-top="{top}" hidden>'
            '<span>+<span data-count="building"></span></span><i></i><small>Building</small></div>')


# One script for every live number: fills [data-count], then shows [data-count-wrap], the #client-counts tiles and
# the chart bar. Shows nothing unless the feed answers with two whole numbers; on any error or timeout all stay hidden.
WL_COUNTS_JS = """
  <script>(function(){if(!window.fetch||!document.querySelector("[data-count]"))return;var c=window.AbortController?new AbortController():null;var t=setTimeout(function(){c&&c.abort()},5000);
fetch(\"""" + WL_COUNTS_URL + """\",{signal:c?c.signal:undefined}).then(function(r){return r.ok?r.json():null}).then(function(d){clearTimeout(t);if(!d||d.ok!==true)return;
function n(k){var v=d[k];return typeof v==="number"&&v>=0&&Math.floor(v)===v?v:null}if(n("white_label_live")===null||n("building")===null)return;
document.querySelectorAll("[data-count]").forEach(function(e){e.textContent=String(n(e.getAttribute("data-count")))});
document.querySelectorAll("[data-count-wrap]").forEach(function(e){e.hidden=false});var b=document.getElementById("client-counts");if(b)b.hidden=false;
document.querySelectorAll("[data-count-bar]").forEach(function(e){var v=n(e.getAttribute("data-count-bar")),top=+e.getAttribute("data-top")||1;if(!v)return;e.style.setProperty("--h",Math.min(1,v/top).toFixed(3));e.parentNode.style.setProperty("--n",e.parentNode.children.length);e.hidden=false})}).catch(function(){clearTimeout(t)});})();</script>"""

#!/usr/bin/env python3
"""Builds out/pageone/clients/index.html (+ clients-v2.css) from the live chrome in ref/pageone/ and registry.json.
No network, no writes to any live site. Usage: python3 build_pageone.py [YYYY-MM-DD]"""
import html, json, os, re, shutil, sys, datetime, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stats import stats as compute_stats, SGT

REF = os.path.join(HERE, 'ref', 'pageone', 'clients')
OUT = os.path.join(HERE, 'out', 'pageone', 'clients')
SITE = 'https://pageonesingapore.com'

# registry industry_id -> block id on the live page
BLOCK_OF = {'car-workshops': 'car-workshops', 'detailing': 'detailing-wraps', 'car-parts': 'car-parts',
            'car-dealers': 'car-dealers', 'property': 'property-agents', 'home': 'home-cleaning',
            'finance': 'finance-professional', 'travel': 'travel-stays', 'other': 'others'}
AGENCY_WA_TEXT = "Hi Page One Singapore, I'd like to talk about white-label SEO websites for my agency."
AGENCY_BENEFITS = ["Your brand, not ours", "No Page One credit on the finished site", "Mobile-first, ready for phones",
                   "SEO articles after go-live", "Fast go-live on the client's own domain"]
FORBIDDEN_EXTRA = ["Dongfeng", "Battery Rescue", "Klar", "MyKar", "K Tech", "ktech.my"]


def meta_text(st):
    return (f"{st['po_live']} client websites live on their own domains across {st['po_industries']} industries. "
            f"See what Page One Singapore builds for businesses like yours, from S$100/month.")


def og_alt(st):
    return f"{st['po_live']} client websites across {st['po_industries']} industries, built by Page One Singapore"


def _e(s):
    return html.escape(s, quote=True)


def wl_stats_html(st):
    """Pure, deterministic. Inner HTML of the block between the wl-stats markers."""
    inds = ''.join(f'<li><span>{_e(l)}</span> <b>{n}</b></li>' for l, n in st['wl_industries'])
    return (
        '<section class="section cv-wl" id="white-label" aria-labelledby="wl-h">\n'
        '      <div class="wrap">\n'
        '        <p class="kicker">White-label work</p>\n'
        '        <h2 id="wl-h">Built for other agencies and dealers</h2>\n'
        '        <p class="section-lead">Websites we build for other agencies and dealers, under their brand. '
        'The work is white-label, so we show totals only: no names, domains, logos or screenshots.</p>\n'
        '        <div class="wl-tiles">\n'
        f'          <div class="wl-tile"><div class="value"><span data-reg="wl_live">{st["wl_live"]}</span></div><div class="label">White-label sites live</div></div>\n'
        f'          <div class="wl-tile"><div class="value"><span data-reg="wl_build">{st["wl_build"]}</span></div><div class="label">In build now</div></div>\n'
        f'          <div class="wl-tile"><div class="value">{st["wl_last30"]}</div><div class="label">Launched in the last 30 days</div></div>\n'
        f'          <div class="wl-tile"><div class="value">{len(st["wl_industries"])}</div><div class="label">Industries covered</div></div>\n'
        '        </div>\n'
        '        <h3 class="wl-h3">Live white-label sites by industry</h3>\n'
        f'        <ul class="wl-inds">{inds}</ul>\n'
        f'        <p class="wl-updated">Last updated <time datetime="{st["updated_iso"]}">{st["updated"]}</time> (SGT)</p>\n'
        '      </div>\n'
        '    </section>')


def agencies_html():
    wa = 'https://wa.me/6597856612?text=' + urllib.parse.quote(AGENCY_WA_TEXT, safe='')
    lis = ''.join(f'<li><svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M4 10.5l4 4 8-9"/></svg><span>{_e(b)}</span></li>' for b in AGENCY_BENEFITS)
    return ('<section class="section cv-agency" id="agencies" aria-labelledby="agency-h">\n'
            '      <div class="wrap">\n'
            '        <h2 id="agency-h">For agencies &amp; dealers: white-label SEO websites</h2>\n'
            f'        <ul class="build agency-list">{lis}</ul>\n'
            f'        <a data-cta="whatsapp_button" class="btn" href="{wa}" target="_blank" rel="noopener">Talk to us on WhatsApp</a>\n'
            '      </div>\n'
            '    </section>')


FALLBACK_JS = r"""/* Missing thumbnail -> client name on the brand colour (22 Nov 2026). Runs before the glide clones the cards. */
(function(){function nm(i){return (i.getAttribute('alt')||'').replace(/ website homepage$/,'')}
function bad(i){var p=i.parentNode;if(!p||!p.classList||!p.classList.contains('phone'))return;p.setAttribute('data-name',nm(i));p.classList.add('nothumb')}
document.addEventListener('error',function(e){var t=e.target;if(t&&t.tagName==='IMG')bad(t)},true);
function scan(){[].forEach.call(document.querySelectorAll('.phone img'),function(i){if(i.complete&&i.naturalWidth===0&&i.getAttribute('src'))bad(i)})}
document.readyState!=='loading'?scan():document.addEventListener('DOMContentLoaded',scan);addEventListener('load',scan)})();
"""
NEW_CSS = """
/* missing-thumbnail fallback (22 Nov 2026): client name on the brand colour, never a broken image */
.phone{position:relative}
.phone.nothumb img{visibility:hidden}
.phone.nothumb::after{content:attr(data-name);position:absolute;inset:6px;border-radius:15px;background:linear-gradient(160deg,#ff3d57,#8b5cf6);display:flex;align-items:center;justify-content:center;text-align:center;padding:16px;color:#fff;font:700 1.15rem/1.25 var(--display);overflow-wrap:anywhere}
.gcard .phone.nothumb::after{inset:4px;border-radius:10px;font-size:.8rem;padding:8px}

/* white-label stats + agencies (22 Nov 2026) */
.cv-wl{padding:56px 0;background:var(--bg-alt)}
.cv-wl .section-lead{margin-bottom:24px}
.wl-tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:0 0 24px}
.wl-tile{min-width:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 16px}
.wl-tile .value{font-family:var(--display);font-size:2.2rem;font-weight:700;line-height:1.1;background:var(--grad-strong);-webkit-background-clip:text;background-clip:text;color:transparent}
.wl-tile .label{color:var(--muted);font-size:.9rem;font-weight:600}
.wl-h3{font-size:1.05rem;margin:0 0 10px}
.wl-inds{list-style:none;margin:0 0 16px;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.wl-inds li{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:#fff;font-weight:600;font-size:.92rem;min-width:0}
.wl-inds li b{color:#fff;background:var(--grad-strong);border-radius:999px;padding:1px 8px;font-size:.8rem}
.wl-updated{margin:0;font-size:.85rem;color:var(--muted)}
.cv-agency{padding:56px 0}
.cv-agency h2{overflow-wrap:anywhere}
.agency-list{margin:0 0 22px;max-width:620px}
@media(min-width:768px){
  .wl-tiles{grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
  .cv-wl,.cv-agency{padding:72px 0}
}
"""


def parse_live(src):
    cards = {}  # img file -> ccard html
    for m in re.finditer(r'<a class="ccard".*?</a>', src, re.S):
        f = re.search(r'src="img/clients/([^"]+)"', m.group(0)).group(1)
        cards[f] = m.group(0)
    glide = {}
    for m in re.finditer(r'<a class="gcard".*?</a>', src, re.S):
        f = re.search(r'src="img/clients/([^"]+)"', m.group(0)).group(1)
        glide[f] = m.group(0)
    return cards, glide


def card_fields(c):
    g = lambda p: html.unescape(re.search(p, c, re.S).group(1))
    return dict(href=re.search(r'href="([^"]+)"', c).group(1), name=g(r'<h3>(.*?)</h3>'),
                desc=g(r'<p class="desc">(.*?)</p>'))


def new_ccard(rec, file, since):
    name, desc = rec['name'], rec['card']['tagline']
    host = rec['host']
    return (f'<a class="ccard" href="{rec["url"]}" target="_blank" rel="noopener"><span class="phone"><img src="img/clients/{file}" width="480" height="912" alt="{_e(name)} website homepage" loading="lazy" decoding="async"></span>'
            f'<h3>{_e(name)}</h3><p class="desc">{_e(desc)}</p><p class="since">{since}</p><p class="visit">{host} <span>Visit site &#8599;</span></p></a>')


def new_gcard(rec, file):
    n = _e(rec['name'])
    return (f'<a class="gcard" href="{rec["url"]}" target="_blank" rel="noopener" aria-label="{n} (opens in a new tab)"><span class="phone"><img src="img/clients/{file}" width="480" height="912" alt="{n} website homepage" loading="lazy" decoding="async"></span></a>')


def build(today=None, write=True):
    reg = json.load(open(os.path.join(HERE, 'registry.json')))
    today = today or datetime.datetime.now(SGT).date()
    st = compute_stats(reg, today)
    src = open(os.path.join(REF, 'index.html'), encoding='utf-8').read()
    live_cards, live_glide = parse_live(src)
    live_order = list(live_cards)

    # allowed named cards: pageone + public + live; plus own SG Garage case study (never counted)
    named = [r for r in reg['records'] if r['visibility'] == 'public' and r['agency'] == 'pageone' and r['status'] == 'live']
    case = [r for r in reg['records'] if r['id'] == 'sggarage' and (r['host'] + '.webp') in live_cards]
    shown = {}  # block id -> list of (file, ccard, gcard-or-None, rec)
    counts = {}
    for r in named:
        b = BLOCK_OF[r['industry_id']]
        counts[b] = counts.get(b, 0) + 1
    entries = {}
    for r in named + case:
        b = BLOCK_OF[r['industry_id']]
        file = (r.get('card') or {}).get('screenshot') or r['host'] + '.webp'
        if file in live_cards:
            cc, gc = live_cards[file], live_glide.get(file)
        else:
            since = datetime.date.fromisoformat(r['live_date']).strftime('Since %b %Y')
            cc, gc = new_ccard(r, file, since), new_gcard(r, file)
        entries.setdefault(b, []).append((file, cc, gc, r))
    for b in entries:  # live order first, then registry order for new cards
        entries[b].sort(key=lambda e: live_order.index(e[0]) if e[0] in live_order else 10**6)
    removed = [f for f in live_order if f not in {e[0] for v in entries.values() for e in v}]

    # block order and chips follow the live page
    block_ids = re.findall(r'<section class="ind[^"]*" id="([^"]+)"', src)
    labels = {m.group(1): m.group(2) for m in re.finditer(r'<h2 id="([^"]+)-h">(.*?) <span class="count-badge"', src)}
    out = src
    # cards per block
    for b in block_ids:
        m = re.search(r'(<section class="ind[^"]*" id="%s".*?<div class="strip"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)' % re.escape(b), out, re.S)
        ents = entries.get(b, [])
        new_strip = ''.join(e[1] for e in ents)
        head = m.group(1)
        n = counts.get(b, 0)
        head = re.sub(r'<span class="count-badge">.*?</span>', f'<span class="count-badge">{n} website{"" if n == 1 else "s"}</span>', head, count=1)
        out = out[:m.start()] + head + new_strip + m.group(3) + out[m.end():]
    # chips
    chips = ''.join(f'<a class="chip" href="#{b}">{labels[b]} <b>{counts[b]}</b></a>' for b in block_ids if counts.get(b))
    out = re.sub(r'(<nav class="chips" aria-label="Industries">).*?(</nav>)', lambda m: m.group(1) + chips + m.group(2), out, count=1, flags=re.S)
    # hero glide
    gl = []
    for b in block_ids:
        gl += [e[2] for e in entries.get(b, []) if e[2]]
    out = re.sub(r'(<div class="glide"[^>]*>).*?(</div></div>\n      </div>\n    </section>)', lambda m: m.group(1) + ''.join(gl) + m.group(2), out, count=1, flags=re.S)
    # hero kpis + lead
    out = re.sub(r'<div class="cv-kpis">.*?</div>\s*</div>\s*<p class="lead">.*?</p>',
                 '<div class="cv-kpis">\n          <div class="kpi"><div class="value"><span data-reg="po_live">%d</span></div><div class="label">client websites live on their own domain</div></div>\n'
                 '          <div class="kpi"><div class="value"><span data-reg="po_industries">%d</span></div><div class="label">industries</div></div>\n        </div>\n'
                 '        <p class="lead">Find your industry and see what we build for businesses like yours. Every named site below is live on the business\'s own domain. '
                 'Another <span data-reg="po_build">%d</span> are in build. Tap any screenshot to open it.</p>' % (st['po_live'], st['po_industries'], st['po_build']),
                 out, count=1, flags=re.S)
    # remove the dated latest-launches row
    out = re.sub(r'\n    <section class="cv-latest".*?</section>\n', '\n', out, count=1, flags=re.S)
    # wl stats + agencies right after the hero
    wl = '<!-- wl-stats:start -->' + wl_stats_html(st) + '<!-- wl-stats:end -->'
    i = out.index('    <section class="ind" id=')  # Edwin's order: stats, agencies, then the named industry blocks
    out = out[:i] + '    ' + wl + '\n\n    ' + agencies_html() + '\n\n' + out[i:]
    # disclaimer
    out = out.replace("Only live websites are counted: the business's own domain, or its own mini-site on SG Car Workshop.",
                      "Named websites are counted only when live on the business's own domain. SG Garage, our own workshop, is shown as a case study and is not counted.")
    # meta
    mt = meta_text(st)
    out = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + _e(mt), out, count=1)
    out = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + _e(mt), out, count=1)
    out = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + _e(mt), out, count=1)
    out = re.sub(r'(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*', lambda m: m.group(1) + _e(og_alt(st)), out)
    # JSON-LD: CollectionPage ItemList, WebPage
    items = []
    for i, r in enumerate(named, 1):
        file = (r.get('card') or {}).get('screenshot') or r['host'] + '.webp'
        f = card_fields(live_cards[file]) if file in live_cards else dict(href=r['url'], name=r['name'], desc=r['card']['tagline'])
        items.append({"@type": "ListItem", "position": i, "item": {"@type": "WebSite", "@id": f['href'] + '#website', "name": f['name'],
                      "url": f['href'], "description": f['desc'], "creator": {"@id": SITE + "/#business"}, "maintainer": {"@id": SITE + "/#business"}}})
    coll = {"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE + "/clients/", "name": "Websites we build, by industry",
            "about": {"@id": SITE + "/#business"}, "inLanguage": "en-SG", "dateModified": st['updated_iso'],
            "mainEntity": {"@type": "ItemList", "name": "Websites built and run by Page One Singapore", "numberOfItems": len(items), "itemListElement": items}}
    blk = '<script type="application/ld+json">\n' + json.dumps(coll, indent=2, ensure_ascii=False) + '\n  </script>'
    out, k = re.subn(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "CollectionPage".*?</script>', lambda m: blk, out, count=1, flags=re.S)
    assert k == 1
    out = re.sub(r'("@type": "WebPage".*?"description": ")[^"]*', lambda m: m.group(1) + mt, out, count=1, flags=re.S)
    out = re.sub(r'("dateModified": ")\d{4}-\d{2}-\d{2}', lambda m: m.group(1) + st['updated_iso'], out)

    out = out.replace('img/og-clients-v2.jpg', 'img/og-clients-v3.jpg')  # og_pageone.py renders v3 with the computed counts
    check(out, reg)
    if write:
        os.makedirs(OUT, exist_ok=True)
        css = open(os.path.join(REF, 'clients-v2.css'), encoding='utf-8').read()
        import hashlib  # cache-bust rule: ?v=<sha256[:8]> of the CSS actually shipped
        out = re.sub(r'clients-v2\.css(\?v=[0-9a-f]+)?"', 'clients-v2.css?v=%s"' % hashlib.sha256((css + NEW_CSS).encode()).hexdigest()[:8], out)
        js = FALLBACK_JS + open(os.path.join(REF, 'clients-v2.js'), encoding='utf-8').read()
        out = re.sub(r'clients-v2\.js(\?v=[0-9a-f]+)?"', 'clients-v2.js?v=%s"' % hashlib.sha256(js.encode()).hexdigest()[:8], out)
        open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(out)
        open(os.path.join(OUT, 'clients-v2.css'), 'w', encoding='utf-8').write(css + NEW_CSS)
        open(os.path.join(OUT, 'clients-v2.js'), 'w', encoding='utf-8').write(FALLBACK_JS + open(os.path.join(REF, 'clients-v2.js'), encoding='utf-8').read())
        os.makedirs(os.path.join(HERE, 'fixtures'), exist_ok=True)
        open(os.path.join(HERE, 'fixtures', 'wl-stats.html'), 'w', encoding='utf-8').write(wl_stats_html(st))
    return out, st, counts, removed


def forbidden_terms(reg):
    """(regex, label) pairs for every white-label record plus the fixed list."""
    terms = []
    for r in reg['records']:
        if r['visibility'] != 'white-label':
            continue
        for v in (r.get('name'), r.get('id')):
            if v:
                terms.append((r'(?<![a-z0-9])' + re.escape(v.lower()) + r'(?![a-z0-9])', v))
        for v in (r.get('host'), r.get('url'), r.get('preview_url')):
            if v:
                terms.append((re.escape(v.lower()), v))
        if r.get('host'):
            terms.append((re.escape(f"img/clients/{r['host']}.webp".lower()), 'img/clients/' + r['host']))
        terms.append((re.escape(f"img/clients/{r['id']}.webp".lower()), 'img/clients/' + r['id']))
    for v in FORBIDDEN_EXTRA:
        terms.append((r'(?<![a-z0-9])' + re.escape(v.lower()) + r'(?![a-z0-9])', v))
    return terms


def check(out, reg):
    low = out.lower()
    for rx, label in forbidden_terms(reg):
        assert not re.search(rx, low), f'white-label leak in output: {label}'
    assert 'aggregaterating' not in low, 'aggregateRating present'
    assert '+60' not in out, '+60 present'
    assert out.count('/p1-cta.js') == 1 and out.count('<script src="/p1-cta.js?v=') == 1, 'p1-cta.js tag count'


if __name__ == '__main__':
    t = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else None
    out, st, counts, removed = build(t)
    print('built', len(out), 'bytes; counts', counts, '; removed cards', removed)

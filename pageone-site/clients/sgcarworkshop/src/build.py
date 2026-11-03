#!/usr/bin/env python3
"""SG Car Workshop: static directory preview.  python3 build.py [outdir]   (default ../site)

Preview mode (LIVE = False): pages are published at https://pageonesingapore.com/preview/sgcarworkshop/ ; canonical, sitemap and
llms.txt name that address, robots.txt says Disallow: / . Internal links and assets are RELATIVE, so the same files work at the
preview address and on the real domain. LIVE = True switches every absolute URL to https://sgcarworkshop.sg/ and opens robots.txt.
Pages never carry a noindex tag: hiding the preview is done by a server header outside the pages (MASTER-RULES 4.3).
"""
import datetime
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'builder'))
import areas  # noqa: E402
from area_copy import AREA_COPY, REGION_COPY  # noqa: E402
from data import ENTRIES, CATEGORIES, PAGE_ONE_WA, PAGE_ONE_WA_SHOW, TIERS, PRICE_NOTE, FREE_EXAMPLE, REFILED  # noqa: E402
from PIL import Image  # noqa: E402

SETTINGS = json.load(open(os.path.join(HERE, 'settings.json')))   # brand, footer text, menu links, wording rules, block orders
SITE_NAME = SETTINGS['brand']
DOMAIN = SETTINGS['domain']
LIVE_BOTS = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
INDEXNOW_KEY = '4e898a9c4ad17bbc9c447eb375b62f0a'   # IndexNow key (2 Nov 2026); key file is written by every build
LIVE = os.environ.get('SGCW_LIVE') == '1'   # SGCW_LIVE=1 builds the real-domain copy (site-live/): open robots.txt, root-relative paths
# Google usage (Edwin, 2 Nov 2026): the referrer-restricted BROWSER key appears only (a) in the Maps Embed iframe URL on profile pages (free) and
# (b) as data-key on the on-click "Show opening hours" box, which assets/livephone.js uses for ONE Place Details call (businessStatus,
# regularOpeningHours; sessionStorage cache; project quota capped at 30/day). Nothing else calls Places; nothing from Google is stored except place_id.
PLACES_BROWSER_KEY = 'AIzaSyAkMQs46QK9N2fiAqc1dmZch39hPHMzsnU'
PREVIEW_BASE = 'https://pageonesingapore.com/preview/sgcarworkshop/'
BASE = 'https://%s/' % DOMAIN   # canonical, og:url, sitemap and llms.txt always name the real domain (Edwin, 2 Nov 2026), also while previewing
PATH_BASE = '/' if LIVE else '/preview/sgcarworkshop/'
UPDATED = '2026-11-01'
# sameAs for the directory's own Organization: no confirmed owned profiles exist yet (no Google Business Profile, Facebook or Instagram for the directory itself).
ORG_SAMEAS = []
import hashlib as _hl, subprocess
LM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lastmod.json')
try:
    LM = json.load(open(LM_FILE))
except Exception:
    LM = {}
LM_NEW = {}
TODAY = datetime.date.today().isoformat()


def _git_date():
    """Date of the last commit that touched the generator or data (never 'today')."""
    try:
        r = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', HERE, os.path.join(HERE, '..', 'data')], capture_output=True, text=True, cwd=HERE, timeout=20).stdout.strip()
        return r or None
    except Exception:
        return None


def seed_date(path):
    """Seed for a new or changed page (Edwin 3 Nov 2026): the workshop record's last_verified_at for a workshop page, else the last git commit date."""
    if path.startswith('workshops/'):
        slug = path.split('/')[1]
        f = os.path.join(HERE, '..', 'data', 'workshops', slug + '.json')
        if os.path.exists(f):
            v = json.load(open(f)).get('last_verified_at')
            if v:
                return v
    return _git_date() or TODAY


def main_content(html_text):
    """The page without the shared header, menu and footer: those change on every page whenever a link is added, so they are left out of the change check."""
    t = re.sub(r'<header class="top">.*?</header>', '', html_text, flags=re.S)
    t = re.sub(r'<details class="menu".*?</details>', '', t, flags=re.S)
    t = re.sub(r'<footer class="ft">.*?</footer>', '', t, flags=re.S)
    return re.sub(r'\?v=[0-9a-f]{8}', '', t)


def lastmod_of(path, html_text):
    """True lastmod: moves only when the main content changes (shared header, menu, footer and asset cache-busters ignored)."""
    h = _hl.sha1(main_content(html_text).encode()).hexdigest()[:12]
    old = LM.get(path)
    d = old['d'] if old and old.get('h2') == h else seed_date(path)
    LM_NEW[path] = {'h': h, 'h2': h, 'd': d}
    return d

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site'))
E = html.escape
import tags as _tags
REFILED = REFILED   # cards moved out of general servicing because what customers mention clearly supports a specific service (tags.refile)
CAT = {c['slug']: c for c in CATEGORIES}
ENT = {e['slug']: e for e in ENTRIES}
PAID = [e for e in ENTRIES if e['tier'] != 'free']
CAT_LIST = [c for c in CATEGORIES if any(c['slug'] in e.get('categories', [e['category']]) for e in ENTRIES)]
RN = areas.REGION_NAMES
ESTATES = areas.ESTATES
areas.annotate(ENTRIES)
PUB_REGIONS = PUB_ESTATES = PUB_PAIRS = PUB_TOWNS = None   # filled by setup_areas()
TOWNS = areas.TOWNS


def setup_areas():
    """Decide which area pages exist: a region with a listing, an estate with 1+ listings, a service x estate pair with 2+."""
    global PUB_REGIONS, PUB_ESTATES, PUB_PAIRS, PUB_TOWNS
    PUB_REGIONS, PUB_ESTATES, PUB_PAIRS = areas.published(ENTRIES)
    # Never an area x service page for general servicing, and none that repeats the whole area page (Edwin 3 Nov 2026): those are merged into the area page.
    PUB_PAIRS = {(s, c): v for (s, c), v in PUB_PAIRS.items() if c != 'general-servicing-repair' and len(v) < len(PUB_ESTATES[s])}
    PUB_TOWNS = {t: [k for k in PUB_ESTATES if ESTATES[k]['town'] == t] for t in TOWNS if any(ESTATES[k]['town'] == t for k in PUB_ESTATES)}


def free_n(es):
    return sum(1 for e in es if not is_paid(e))


setup_areas()

ICONS = {
    'spray': '<path d="M4 9h8v6H4z"/><path d="M12 11h3l2-2"/><path d="M8 15v5"/><path d="M19 5h.01M21 8h.01M21 3h.01M18 2h.01"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    'chip': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    'battery': '<rect x="2" y="8" width="18" height="10" rx="2"/><path d="M22 11v4M7 11v4M5 13h4"/>',
    'sparkle': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>',
    'film': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14M17 5v14M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    'parts': '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8z"/><path d="M3 21l6-6"/>',
    'wrench': '<path d="M14.5 6a4.5 4.5 0 0 0-5.7 5.6L3 17.5 6.5 21l5.9-5.8A4.5 4.5 0 0 0 18 9.5l-2.6 2.6-2.5-.5-.5-2.5z"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    'pin': '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'chev-l': '<path d="M15 18l-6-6 6-6"/>',
    'chev-r': '<path d="M9 18l6-6-6-6"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'out': '<path d="M7 17L17 7M8 7h9v9"/>',
    'snow': '<path d="M12 2v20M4.9 7l14.2 10M4.9 17L19.1 7"/>',
    'wheel': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/>',
    'drop': '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    'car': '<path d="M5 16V11l2-5h10l2 5v5M3 16h18v3H3z"/><circle cx="7.5" cy="19" r="1.2"/><circle cx="16.5" cy="19" r="1.2"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
}


def ic(k, cls=''):
    """Icon as a <use> of a sprite symbol; page() adds one hidden sprite with only the icons the page uses (Edwin 3 Nov 2026: smaller pages)."""
    return '<svg class="i%s" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-%s"/></svg>' % ((' ' + cls) if cls else '', k)


WA_PATH = ('M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 '
           '8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 '
           '5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z')
WA_SVG = '<svg class="i wa" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg>'


def sprite(html_):
    ids = sorted(set(re.findall(r'href="#i-([a-z0-9-]+)"', html_)))
    if not ids:
        return ''
    sym = ''.join('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (k, ('<path d="%s"/>' % WA_PATH) if k == 'wa' else ICONS[k]) for k in ids)
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">%s</svg>' % sym


# Logo mark: navy tile, gold map pin holding a hex nut ("find a workshop"). Same shape drawn in make_icons().
MARK_PATH = ('M24 41.5L14.1 27.3A12 12 0 1 1 33.9 27.3Z'
             'M24 13.2L29.9 16.6L29.9 23.4L24 26.8L18.1 23.4L18.1 16.6Z'
             'M24 17.4A2.6 2.6 0 1 0 24 22.6A2.6 2.6 0 1 0 24 17.4Z')
MARK_SVG = ('<svg width="36" height="36" viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#0f1c33"/>'
            '<path fill="#d4a64a" fill-rule="evenodd" d="%s"/></svg>' % MARK_PATH)
LOGO = MARK_SVG

_h = hashlib.sha1()
for _f in ('dir.css', 'dir.js', 'livephone.js', 'ask.js'):
    _h.update(open(os.path.join(HERE, _f), 'rb').read())
V = _h.hexdigest()[:8]

PAGES = {}   # path ('' = home, 'a/b/' ...) -> html
META = {}    # path -> title (for llms/sitemap)
FREECOUNT = {}   # path -> free workshops behind a thresholded page (check.py re-applies MIN_FREE)
HUBCARDS = {}   # town hub path -> number of workshop cards shown (a hub is indexable only if it shows every workshop in its estates)
NOINDEX = {}   # path -> reason (thin pages, Edwin 3 Nov 2026); never in sitemap.xml
INDEX_EXCEPTIONS = SETTINGS.get('index_exceptions', {})   # named pages indexable below MIN_FREE (Edwin-approved)
MIN_FREE = SETTINGS['min_free']   # an area, service or area x service page needs at least this many free workshops to be indexable
_imgsz = {}


def imgsize(rel):
    if rel not in _imgsz:
        if rel.endswith('.svg'):   # vector: take the size from the root element
            _s = open(os.path.join(HERE, 'img', rel), encoding='utf-8').read(600)
            _w, _h = re.search(r'\bwidth="(\d+)"', _s), re.search(r'\bheight="(\d+)"', _s)
            _imgsz[rel] = (int(_w.group(1)), int(_h.group(1)))
        else:
            _imgsz[rel] = Image.open(os.path.join(HERE, 'img', rel)).size
    return _imgsz[rel]


def img_tag(rel, alt, depth, lazy=True, cls=''):
    w, h = imgsize(rel)
    return '<img src="%sassets/img/%s" alt="%s" width="%d" height="%d"%s%s%s>' % (
        pre(depth), rel, E(alt, True), w, h, ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '', ' decoding="async"' if lazy else '')   # eager images decode at once so they are painted in full-page screenshots


def pre(depth):
    return '../' * depth or './'


def abs_url(path):
    return BASE + path


def wa_link(num, msg):
    return 'https://wa.me/%s?text=%s' % (num, quote(msg))


def list_wa(depth, what):
    """Page One WhatsApp link for the 'List your workshop' calls to action."""
    return wa_link(PAGE_ONE_WA, 'Hi Page One, I would like to list my workshop on %s (%s).\n\n(From %s)' % (SITE_NAME, what, BASE))


def words(s):
    return len(re.findall(r"[A-Za-z0-9$'-]+", re.sub(r'<[^>]+>', ' ', s)))


# ------------------------------------------------------------------ components
def chip_row(depth, active=None):
    li = ''.join('<li><a href="%sservices/%s/"%s>%s%s</a></li>' % (pre(depth), c['slug'], ' class="on"' if c['slug'] == active else '', ic(c['icon']), E(c['short'])) for c in CATEGORIES)
    return '<ul class="chips" aria-label="Browse by service">%s</ul>' % li


def list_card(depth, what):
    return ('<article class="card list rv"><div class="bd"><span class="ic">%s</span><h3>List your workshop</h3>'
            '<p class="tx">For business owners: is your workshop listed here? Claiming a listing is free.</p>'
            '<div class="acts"><a class="btn sm ghost" href="%slist-your-workshop/" data-cta="list_%s">How listing works</a></div></div></article>') % (
        ic('plus'), pre(depth), re.sub(r'[^a-z0-9]+', '-', what.lower()).strip('-'))


def crumbs(depth, trail):
    """trail = [(label, relpath or None)]; returns (html, jsonld)"""
    items = [('Home', '')] + trail
    parts, ld = [], []
    for i, (lab, p) in enumerate(items):
        last = i == len(items) - 1
        parts.append(E(lab) if last else '<a href="%s%s">%s</a>' % (pre(depth), p, E(lab)))
        ld.append({'@type': 'ListItem', 'position': i + 1, 'name': lab, 'item': abs_url(p if p is not None else '')} if not last else
                  {'@type': 'ListItem', 'position': i + 1, 'name': lab})
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts), {'@type': 'BreadcrumbList', 'itemListElement': ld}


def header(depth):
    p = pre(depth)
    svc = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (p, c['slug'], E(c['short'])) for c in CAT_LIST)
    reg = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(RN[k])) for k in PUB_REGIONS)
    est = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(ESTATES[k]['name'])) for k in PUB_ESTATES)
    return ('<a class="skip" href="#main">Skip to content</a><header class="top"><div class="w bar"><a class="brand" href="%s" aria-label="%s home">%s<span class="wm"><span><b>SG</b> Car Workshop</span><small>Singapore car workshop directory</small></span></a>'
            '<details class="menu"><summary aria-label="Menu">%s<span>Menu</span></summary><nav class="mpanel" aria-label="Main">'
            '<a class="mfind" href="%s#find">%s Find a workshop</a>'
            '<div class="mcols"><div class="svc-col"><h3>Services</h3><ul>%s</ul></div><div><h3>Regions</h3><ul>%s</ul></div><div><h3>Estates</h3><ul>%s</ul></div></div>'
            '<a class="mabout" href="%sabout/">About</a></nav></details></div></header>') % (p, E(SITE_NAME), LOGO, ic('menu'), p, ic('search'), svc, reg, est, p)


def footer(depth):
    p = pre(depth)
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (p, c['slug'], E(c['short'])) for c in CAT_LIST)
    reg = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(RN[k])) for k in PUB_REGIONS)
    est = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(ESTATES[k]['name'])) for k in PUB_ESTATES)
    links = ''.join('<li><a href="%s%s">%s</a></li>' % (p, m['path'], E(m['label'])) for m in SETTINGS['menu_links'])
    return ('<footer class="ft"><div class="w cols"><div><h3>%s</h3><p>%s '
            '<a href="https://pageonesingapore.com/" rel="noopener">Page One Singapore</a>.</p><p class="fine">'
            '%s</p></div>'
            '<div><h3>Services</h3><ul>%s</ul></div><div><h3>Regions</h3><ul>%s</ul><h3 class="h3b">Estates</h3><ul>%s</ul></div>'
            '<div><h3>Directory</h3><ul>%s</ul></div></div></footer>') % (E(SITE_NAME), E(SETTINGS['footer_about']), E(SETTINGS['footer_note']), cats, reg, est, links)


def wabar(items):
    return '<div class="wabar" role="region" aria-label="Contact">%s</div>' % ''.join(items)


def page(path, title, desc, body, schema=None, og=None, bar=None, h1=None, extra_js='', index=True, why=''):
    assert len(title) <= 60, (path, len(title), title)
    assert len(desc) <= 160, (path, len(desc))
    depth = path.count('/')
    url = abs_url(path)
    og_rel = og or 'og-default.jpg'
    remote = og_rel.startswith('http')
    og_url = og_rel if remote else BASE + 'assets/img/' + og_rel
    ow, oh = (1200, 630) if og_rel in ('og-default.jpg', 'wei/og.jpg') else (None, None) if remote else imgsize(og_rel)
    ld = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(s, ensure_ascii=False).replace('</', '<\\/') for s in (schema or []))
    p = pre(depth)
    gk = ''
    out = f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc, True)}">
<meta name="robots" content="{'index, follow, max-image-preview:large' if index else 'noindex, follow'}">
<link rel="canonical" href="{E(url)}">
<link rel="icon" href="{p}assets/favicon.ico" sizes="48x48">
<link rel="icon" href="{p}assets/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(SITE_NAME)}">
<meta property="og:title" content="{E(title, True)}">
<meta property="og:description" content="{E(desc, True)}">
<meta property="og:url" content="{E(url)}">
<meta property="og:image" content="{E(og_url)}">
{('<meta property="og:image:width" content="%d">' + chr(10) + '<meta property="og:image:height" content="%d">') % (ow, oh) if ow else ''}
<meta property="og:image:alt" content="{E(h1 or title, True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{E(og_url)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"></noscript>
<link rel="stylesheet" href="{p}assets/dir.css?v={V}">
<script>document.documentElement.className+=' js'</script>
{gk}{ld}</head>
<body{' class="has-bar"' if bar else ''}>
{header(depth)}
<main id="main">
{body}
</main>
{footer(depth)}
{bar or ''}
<script src="{p}assets/dir.js?v={V}" defer></script>
{('<script src="%sassets/ask.js?v=%s" defer></script>' % (p, V)) if path == '' else ''}
{('<script src="%sassets/livephone.js?v=%s" defer></script>' % (p, V)) if extra_js else ''}
</body>
</html>
'''
    out = out.replace('</body>', sprite(out) + '\n</body>', 1)
    PAGES[path] = out
    META[path] = title
    if not index:
        NOINDEX[path] = why


def area_copy(slug):
    """(paragraph, nearby MRT, landmarks). The paragraph is the industrial estate's own intro; MRT and landmarks come from its town."""
    a = ESTATES[slug]
    _p, mrt, marks = AREA_COPY[a['town']]
    return a['intro'], mrt, marks


# ------------------------------------------------------------------ pages
def home():
    depth = 0
    feats = [e for e in ENTRIES if is_paid(e)]
    slides = ''.join(slide(e) for e in feats)
    # Home list: A to Z, no tier order (Edwin 3 Nov 2026). Paid Featured clients come last in the lazy part, still searchable; the first 12 are in the HTML.
    ordered = sorted([e for e in ENTRIES if not is_paid(e)], key=lambda e: e['name'].lower()) + [e for e in ENTRIES if is_paid(e)]
    first = ''.join(card(e, 0, '') for e in ordered[:12])
    rest = ''.join(card(e, 0, '') for e in ordered[12:])
    cards = first + ('<template id="more-cards">%s</template>' % rest) if rest else first
    more_btn = ('<p id="more-btn-wrap" style="text-align:center;margin:18px 0 0;grid-column:1/-1"><button type="button" class="btn big" id="more-btn">Show all %d workshops</button></p>' % len(ordered)) if rest else ''
    faqs = [
        ('What is %s?' % SITE_NAME, 'A directory of car workshops and car services in Singapore. Each entry shows what the business does, where it is and how to contact it, using details from the business or its public listing.'),
        ('How do I contact a workshop?', 'Tap WhatsApp or Call on a card. The WhatsApp message is prefilled with the workshop name and says you found them on %s, so you only need to add your car and what you need.' % SITE_NAME),
        ('Do you rank or review workshops?', 'We do not sell rankings and we do not write reviews. Where an estate has at least 8 workshops with 20 or more Google ratings, we rank those by Google rating and number of ratings together; the formula is on the About page. Paid Featured workshops are never part of a ranking.'),
        ('How can I browse by area?', 'Pick a region (North, North-East, East, West, Central, or Mobile for services that come to you) in the search panel, or open an estate page such as Kaki Bukit or Yishun to see the workshops in that industrial area, a map and nearby areas.'),
    ]
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)
    svc_opts = '<label class="opt"><input type="radio" name="svc" value="" checked><span>All</span></label>' + ''.join(
        '<label class="opt"><input type="radio" name="svc" value="%s"><span>%s</span></label>' % (c['slug'], E(c['short'])) for c in CAT_LIST)
    reg_opts = ''.join('<label class="opt"><input type="checkbox" name="reg" value="%s"><span>%s</span></label>' % (k, E('Mobile' if k == 'mobile' else RN[k])) for k in PUB_REGIONS)
    svc_tiles = ''.join('<li><a href="services/%s/"><span class="ti">%s</span><span><b>%s</b><small>%d listing%s</small></span></a></li>' % (
        c['slug'], ic(c['icon']), E(c['short']), n, '' if n == 1 else 's') for c in CAT_LIST for n in [sum(1 for e in ENTRIES if c['slug'] in e.get('categories', [e['category']]))])
    reg_tiles = ''.join('<li><a href="areas/%s/"><span class="ti">%s</span><span><b>%s</b><small>%d listing%s</small></span></a></li>' % (
        k, ic('pin'), E(RN[k]), n, '' if n == 1 else 's') for k in PUB_REGIONS for n in [sum(1 for e in ENTRIES if e['region'] == k)])
    est_tiles = ''.join('<li><a href="areas/%s/"><span class="ti">%s</span><span><b>%s</b><small>%s &middot; %d listing%s</small></span></a></li>' % (
        k, ic('pin'), E(ESTATES[k]['name']), E(RN[ESTATES[k]['region']]), len(v), '' if len(v) == 1 else 's') for k, v in PUB_ESTATES.items())
    askdata = json.dumps({'cats': [{'slug': c['slug'], 'short': c['short'], 'blurb': c['blurb']} for c in CAT_LIST], 'areas': [{'slug': k, 'name': v['name'], 'region': v['region']} for k, v in ESTATES.items()], 'guides': [{'slug': g['slug'], 'path': _guides.gpath(g), 'h1': g['h1'], 'short': g['short'], 'kw': g['kw']} for g in _guides.GUIDES]}).replace('</', '<\\/')
    tiers = tiers_strip()
    body = f'''<section class="finder" id="find"><div class="w"><div class="hero-t"><h1>Find a car workshop in Singapore</h1>
<p>Describe the problem or type a service and area, then message the workshop on WhatsApp.</p></div>
<p class="nojs">Browse by <a href="#services">service</a> or <a href="#regions">area</a> below.</p>
<form class="panel" id="finder" role="search" aria-label="Find a workshop or describe your car problem" onsubmit="return false">
<div class="qrow"><label class="q"><span class="skip">Describe your car problem, or type a service, area or workshop name</span>{ic('search')}<textarea id="q" rows="2" maxlength="160" placeholder="Describe your car problem, e.g. knocking sound under my Mitsubishi" autocomplete="off" autocapitalize="off" enterkeyhint="search"></textarea></label><button type="submit" class="btn amber qgo">Search</button></div>
<div class="opts chiprow" role="radiogroup" aria-label="Or pick a service">{svc_opts}</div>
<p class="fine askhint">Type in your own words, in any order. We do not store your name or number, only the words you type.</p>
</form></div></section>
<section class="askres" id="askres" hidden aria-live="polite"><div class="w" id="askbody"></div></section>
<script type="application/json" id="askdata">{askdata}</script>
<section class="feat" aria-roledescription="carousel" aria-label="Featured Premium workshops"><div class="w"><div class="sec-h"><h2>Featured Premium workshops <span class="spons">Featured (paid)</span></h2>
<div class="car-nav"><button type="button" id="cprev" aria-label="Previous">{ic('chev-l')}</button><button type="button" id="cnext" aria-label="Next">{ic('chev-r')}</button></div></div>
<div class="marq" id="marq"><ul class="track" id="track" aria-label="Featured workshops">{slides}</ul></div></div></section>
<section id="workshops" class="lst"><div class="w"><div class="sec-h"><h2>All workshops</h2><a class="sec-link" href="#services">Browse by service</a></div><p class="fine adnote">Workshops are listed A to Z with no boost for any tier. Paid Featured clients are in their own labelled block above and are marked Featured (paid). Basic listings are built from the workshop's public Google Business Profile and, where available, what its customers mention in Google reviews, and link to its Google Maps listing. They are not endorsed by or arranged with the business.</p><div class="grid" id="results">{cards}{more_btn}</div>
<div class="empty" id="empty"><b>No workshops match.</b> Try fewer filters, or <a href="list-your-workshop/">list your workshop</a>.</div></div></section>
<section class="alt" id="services"><div class="w"><h2>Browse by service</h2><ul class="tiles">{svc_tiles}</ul></div></section>
<section id="regions"><div class="w"><h2>Browse by area</h2><ul class="tiles rg">{reg_tiles}</ul><h3 class="sub-h">Estates and industrial areas</h3><ul class="tiles est">{est_tiles}</ul></div></section>
<section class="alt"><div class="w"><h2>How the listings work</h2>{tiers}</div></section>
<section><div class="w nar"><h2>Questions</h2>{faq_html}</div></section>
<section class="owner-sec"><div class="w"><p class="owner-note">For business owners: Own a car workshop? Basic listings are free. <a href="list-your-workshop/" data-cta="list_home">List or manage your workshop &rarr;</a></p></div></section>'''
    ld = [
        {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'url': abs_url(''), 'inLanguage': 'en-SG'},
        dict({'@context': 'https://schema.org', '@type': 'Organization', '@id': abs_url('') + '#org', 'name': SITE_NAME, 'url': abs_url(''),
              'logo': {'@type': 'ImageObject', 'url': BASE + 'assets/icon-512.png', 'width': 512, 'height': 512}, 'parentOrganization': {'@type': 'Organization', 'name': 'Page One Singapore', 'url': 'https://pageonesingapore.com/'}}, **({'sameAs': ORG_SAMEAS} if ORG_SAMEAS else {})),
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
    ]
    page('', 'Car Workshops in Singapore | SG Car Workshop',
         'Find car workshops in Singapore by service and region: repair, gearbox, ABS and ECU, spray painting, batteries, detailing, wraps and parts.', body, ld)


def category(c):
    depth = 2
    es = [e for e in ENTRIES if c['slug'] in e.get('categories', [e['category']])]
    n = words(c['intro'])
    assert 40 <= n <= 60, (c['slug'], n)
    cr, crld = crumbs(depth, [('Services', 'services/' + c['slug'] + '/'), (c['name'], None)][1:])
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:20px"><div class="w"><h1>{E(c['name'])} in Singapore</h1><p class="lede">{E(c['intro'])}</p>{chip_row(depth, c['slug'])}</div></section>
{featured_sec(es, depth, 'services/%s/' % c['slug'], 'in ' + c['short'].lower())}
<section><div class="w"><h2 class="rv">Listings</h2><div class="grid">{''.join(card(e, depth, 'services/%s/' % c['slug']) for e in es if not is_paid(e))}{list_card(depth, c['short'].lower())}</div></div></section>'''
    itemlist = itemlist_ld(c['name'] + ' in Singapore', es)
    FREECOUNT['services/%s/' % c['slug']] = free_n(es)
    page('services/%s/' % c['slug'], '%s in Singapore | %s' % (c['name'], SITE_NAME), c['blurb'] + ' Browse Singapore listings by area.',
         body, [itemlist, dict(crld, **{'@context': 'https://schema.org'})], h1=c['name'], index=free_n(es) >= MIN_FREE, why='fewer than %d free workshops' % MIN_FREE)


def cap(t, n):
    t = ' '.join(t.split())
    if len(t) <= n:
        return t
    return t[:n - 1].rsplit(' ', 1)[0].rstrip(',;:.') + '.'


def and_list(items):
    items = list(items)
    return items[0] if len(items) == 1 else ', '.join(items[:-1]) + ' and ' + items[-1]


def fit_title(*options):
    for o in options:
        if len(o) <= 60:
            return o
    return options[-1][:60]


def itemlist_ld(name, es):
    """ItemList of the listed workshops (Basic and Verified), in the order the page shows them. Paid Featured (Premium) clients are never in it (Edwin 3 Nov 2026)."""
    es = [e for e in es if not is_paid(e)]
    return {'@context': 'https://schema.org', '@type': 'ItemList', 'name': name, 'numberOfItems': len(es),
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': abs_url('workshops/%s/' % e['slug']), 'name': e['name']} for i, e in enumerate(es)]}


def featured_sec(es, depth, page_path, where):
    """Paid Featured clients get their own clearly labelled block, away from the lists that are ranked or ordered."""
    paid = [e for e in es if is_paid(e)]
    if not paid:
        return ''
    return ('<section class="alt featblock"><div class="w"><h2>Featured (paid) %s</h2><p class="fine">Paid placements, shown on their own. They are not part of any ranking or order on this page.</p>'
            '<div class="grid">%s</div></div></section>') % (E(where), ''.join(card(e, depth, page_path) for e in paid))


def area_tile(depth, k, sub):
    return '<li><a href="%sareas/%s/"><span class="ti">%s</span><span><b>%s</b><small>%s</small></span></a></li>' % (pre(depth), k, ic('pin'), E(sub[0]), E(sub[1]))


def region(slug):
    """Level 1: /areas/<region>/"""
    depth = 2
    name = RN[slug]
    es = [e for e in ENTRIES if e['region'] == slug]
    mobile = slug == 'mobile'
    h1 = 'Mobile car services across Singapore' if mobile else 'Car workshops in the %s region' % name
    cr, crld = crumbs(depth, [(name, None)])
    est = [(k, v) for k, v in PUB_ESTATES.items() if ESTATES[k]['region'] == slug and any(e['region'] == slug for e in v)]
    tiles = ''.join(area_tile(depth, k, (ESTATES[k]['name'], '%d listing%s' % (len(v), '' if len(v) == 1 else 's'))) for k, v in est)
    est_html = '<section class="alt"><div class="w"><h2>Estates and industrial areas</h2><ul class="tiles est">%s</ul></div></section>' % tiles if tiles else ''
    mob_note = ''
    if not mobile and 'mobile' in PUB_REGIONS:
        mob_note = '<p class="fine" style="margin-top:14px">Looking for a service that comes to you? See <a href="%sareas/mobile/">mobile car services across Singapore</a>.</p>' % pre(depth)
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>{E(h1)}</h1><p class="lede">{E(areas.REGION_INTRO[slug])}</p><p>{E(REGION_COPY[slug])}</p></div></section>
{est_html}
{featured_sec(es, depth, 'areas/%s/' % slug, 'in the mobile list' if mobile else 'in the %s region' % name)}
<section><div class="w"><h2>{'Mobile listings' if mobile else 'All workshops in the %s region' % E(name)}</h2><div class="grid">{''.join(card(e, depth, 'areas/%s/' % slug) for e in es if not is_paid(e))}{list_card(depth, 'car workshop' if mobile else 'car workshop in the ' + name + ' region')}</div>{shortlist_links(es, name)}{mob_note}</div></section>'''
    other_regions = ', '.join('<a href="%sareas/%s/">%s</a>' % (pre(depth), k, E(RN[k])) for k in PUB_REGIONS if k != slug)
    rfaqs = [
        ('Which areas does the %s page cover?' % name, areas.REGION_INTRO[slug]),
        ('How do I contact a workshop in the %s?' % ('mobile list' if mobile else name + ' region'), 'Tap WhatsApp or Call on a workshop card or page. WhatsApp messages are prefilled with the workshop name and say you found them on %s, so you only need to add your car and what you need.' % SITE_NAME),
        ('Where can I look if there is nothing close to me?', ('Try another region: %s.' % other_regions) if other_regions else 'Use the search on the home page to filter by service and area.'),
    ]
    body = body.replace('</div></section>\n', '</div></section>\n', 1) + faq_block(rfaqs, 'Questions about this region')
    title = fit_title('Mobile Car Services in Singapore | %s' % SITE_NAME) if mobile else fit_title('Car Workshops in %s Singapore | %s' % (name, SITE_NAME), 'Car Workshops in %s | %s' % (name, SITE_NAME))
    desc = ('Mobile car services that come to your car anywhere in Singapore, such as onsite batteries and mobile detailing. Message them directly.' if mobile else
            'Car workshops and car services in the %s region of Singapore, with estate pages and direct WhatsApp or call contact.' % name)
    page('areas/%s/' % slug, title, cap(desc, 160), body, [itemlist_ld(h1, es), dict(crld, **{'@context': 'https://schema.org'}), faq_ld(rfaqs)], h1=h1, index=False, why='region pages are navigation only')


def faq_ld(faqs):
    """FAQPage JSON-LD that equals the visible FAQ (HTML tags stripped from answers)."""
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', t)}} for q, t in faqs]}


def faq_block(faqs, title):
    items = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), t if '<a ' in t else E(t)) for q, t in faqs)
    return '<section class="alt"><div class="w nar"><h2>%s</h2>%s</div></section>' % (E(title), items)


def town_hub(slug):
    """/areas/<town>/ : navigation page that lists the industrial estates in a town. Indexable only with 2+ estates and enough free workshops."""
    depth = 2
    t = TOWNS[slug]
    ests = PUB_TOWNS[slug]
    rname = RN[t['region']]
    para, mrt, marks = AREA_COPY[slug]
    cr, crld = crumbs(depth, [(rname, 'areas/%s/' % t['region']), (t['name'], None)])
    tiles = ''.join(area_tile(depth, k, (ESTATES[k]['name'], '%d listing%s' % (len(PUB_ESTATES[k]), '' if len(PUB_ESTATES[k]) == 1 else 's'))) for k in ests)
    total = sum(free_n(PUB_ESTATES[k]) for k in ests)
    _seen, hub_es = set(), []
    for k in ests:
        for e in PUB_ESTATES[k]:
            if e['slug'] not in _seen:
                _seen.add(e['slug']); hub_es.append(e)
    hub_es.sort(key=lambda e: e['name'].lower())
    HUBCARDS['areas/%s/' % slug] = len(hub_es)
    h1 = 'Car workshops in %s' % t['name']
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>{E(h1)}</h1><p class="lede">{E(t['intro'])}</p><p>{E(para)}</p></div></section>
<section class="alt"><div class="w"><h2>Industrial estates in {E(t['name'])}</h2><ul class="tiles est">{tiles}</ul>
<p class="fine" style="margin-top:14px">Nearby MRT stations include {E(and_list(mrt))}. Landmarks include {E(and_list(marks))}. Back to the <a href="{pre(depth)}areas/{t['region']}/">{E(rname)} region</a>.</p></div></section>
{featured_sec(hub_es, depth, 'areas/%s/' % slug, 'in ' + t['name'])}
<section><div class="w"><h2>All workshops in {E(t['name'])}</h2><div class="grid">{''.join(card(e, depth, 'areas/%s/' % slug) for e in hub_es if not is_paid(e))}</div></div></section>'''
    desc = 'Car workshop areas in %s, %s region: %s. Pick an industrial estate to compare workshops and contact them on WhatsApp.' % (t['name'], rname, and_list(ESTATES[k]['name'] for k in ests))
    page('areas/%s/' % slug, fit_title('Car Workshops in %s | %s' % (t['name'], SITE_NAME), 'Car Workshops in %s' % t['name']), cap(desc, 160), body,
         [dict(crld, **{'@context': 'https://schema.org'})], h1=h1, index=len(ests) >= 2 and total >= MIN_FREE, why='town hub with one estate or fewer than %d free workshops' % MIN_FREE)


def estate(slug, es):
    """Level 2: /areas/<estate>/  (main local SEO page)"""
    depth = 2
    paid_es = [e for e in es if is_paid(e)]
    es = rank_sorted(es) + paid_es   # free listings first in display order; paid Featured clients only feed the separate block and the counts
    ranked = [e for e in es if (FACTS.get(e['slug']) or {}).get('rank')]
    a = ESTATES[slug]
    rname = RN[a['region']]
    cr, crld = crumbs(depth, [(rname, 'areas/%s/' % a['region']), (TOWNS[a['town']]['name'], 'areas/%s/' % a['town']), (a['name'], None)])
    n = len(es)
    intro = '%s %s lists %d workshop%s here: %s.' % (a['intro'], SITE_NAME, n, '' if n == 1 else 's', and_list(e['name'] for e in es))
    svc_pairs = [(c, v) for (s_, c), v in PUB_PAIRS.items() if s_ == slug]
    chips = ''
    if svc_pairs:
        chips = '<ul class="chips" aria-label="Browse by service in %s">%s</ul>' % (E(a['name']), ''.join(
            '<li><a href="%s/">%s%s (%d)</a></li>' % (c, ic(CAT[c]['icon']), E(CAT[c]['short']), len(v)) for c, v in svc_pairs))
    lat, lon = a['lat'], a['lon']
    bbox = '%.4f,%.4f,%.4f,%.4f' % (lon - 0.011, lat - 0.007, lon + 0.011, lat + 0.007)
    map_src = 'https://www.openstreetmap.org/export/embed.html?bbox=%s&layer=mapnik&marker=%.4f%%2C%.4f' % (bbox, lat, lon)
    map_big = 'https://www.openstreetmap.org/?mlat=%.4f&mlon=%.4f#map=15/%.4f/%.4f' % (lat, lon, lat, lon)
    near = [k for k in a['nearby'] if k in PUB_ESTATES]
    near_tiles = ''.join(area_tile(depth, k, (ESTATES[k]['name'], '%s \u00b7 %d listing%s' % (RN[ESTATES[k]['region']], len(PUB_ESTATES[k]), '' if len(PUB_ESTATES[k]) == 1 else 's'))) for k in near)
    near_tiles += area_tile(depth, a['region'], ('All of the %s region' % rname, 'Region page'))
    cats = and_list(dict.fromkeys(CAT[e['category']]['name'] for e in es))
    faqs = [
        ('Which car workshops are in %s?' % a['name'], '%s currently lists %d workshop%s in %s: %s. Each has its own page with services, address and contact details.' % (SITE_NAME, n, '' if n == 1 else 's', a['name'], and_list(e['name'] for e in es))),
        ('What car services can I find in %s?' % a['name'], 'Listings here cover %s. Open a workshop page to see the services it lists.' % cats.lower()),
        ('How do I contact a workshop in %s?' % a['name'], 'Tap WhatsApp or Call on a workshop card or page. WhatsApp messages are prefilled with the workshop name and say you found them on %s, so you only need to add your car and what you need.' % SITE_NAME),
        ('Which region is %s in?' % a['name'], '%s is in the %s region of Singapore.%s Browse the <a href="%sareas/%s/">%s region page</a> for more workshops.' % (
            a['name'], rname, (' Nearby areas on %s: %s.' % (SITE_NAME, and_list(ESTATES[k]['name'] for k in near))) if near else '', pre(depth), a['region'], E(rname))),
    ]
    para, mrt, marks = area_copy(slug)
    faqs.insert(3, ('What is near %s?' % a['name'], 'Nearby MRT stations include %s. Local landmarks include %s.' % (and_list(mrt), and_list(marks))))
    near_links = ', '.join('<a href="%sareas/%s/">%s</a>' % (pre(depth), k, E(ESTATES[k]['name'])) for k in near)
    about_html = ('<section><div class="w nar"><h2>About %s</h2><p>%s</p>'
                  '<p>%s lists the workshops it has for this area on one page, so you can compare services, open each workshop page for its address and contact details, and message a workshop directly on WhatsApp or by phone. Listings show %s.%s</p></div></section>') % (
        E(a['name']), E(para), E(SITE_NAME), E(cats.lower()),
        (' If you want to compare more options nearby, see %s.' % near_links) if near_links else '')
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), t if '<a ' in t else E(t)) for q, t in faqs)
    etools = ''
    if sum(1 for e in es if e['slug'] in FACTS and e['tier'] == 'free') >= 2:
        etools = ('<div class="etools" role="group" aria-label="Filter and sort"><span class="et-l">Filter</span>'
                  '<button type="button" class="chip-b" data-f="sun" aria-pressed="false">Open Sunday</button>'
                  '<button type="button" class="chip-b" data-f="late" aria-pressed="false">Open late</button>'
                  '<label class="et-s"><span class="skip">Sort</span><select data-sort aria-label="Sort workshops"><option value="">Default order</option><option value="rating">Highest Google rating first (20+ ratings)</option></select></label>'
                  '<p class="fine et-n" hidden><b class="et-c"></b> <button type="button" class="linkb" data-clear>Clear filters</button><br>Filters use the Google Maps hours we hold. Workshops without hours are hidden while a filter is on.</p></div>')
    order_note = ('<p class="fine">Ranked by a combined score of Google rating and number of ratings, among the %d workshops here with %d or more Google ratings (the formula is on the <a href="%sabout/">About page</a>). The others follow A to Z. Ratings and hours are from Google Maps.</p>' % (len(ranked), RANK_MIN_RATINGS, pre(depth))) if ranked else '<p class="fine">Listed A to Z. Ratings and hours are from Google Maps.</p>'
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>Car workshops in {E(a['name'])}</h1><p class="lede">{E(intro)}</p>{chips}</div></section>
{about_html}
{featured_sec(paid_es, depth, 'areas/%s/' % slug, 'in ' + a['name'])}
<section class="alt"><div class="w"><h2>Workshops in {E(a['name'])}</h2>{order_note}{etools}<div class="grid" id="estate-grid">{''.join(card(e, depth, 'areas/%s/' % slug) for e in es if not is_paid(e))}{list_card(depth, 'car workshop in ' + a['name'])}</div>{shortlist_links(es, a['name'])}</div></section>
<section class="alt"><div class="w"><h2>Map of {E(a['name'])}</h2>
<div class="mapbox"><iframe src="{E(map_src)}" title="Map of {E(a['name'], True)}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
<p class="fine">Approximate area map from OpenStreetMap. <a href="{E(map_big)}" target="_blank" rel="noopener">View a larger map</a>. Use the Directions button on a workshop for its exact address.</p></div></section>
<section><div class="w"><h2>Nearby areas</h2><ul class="tiles est">{near_tiles}</ul></div></section>
<section class="alt"><div class="w nar"><h2>Questions about {E(a['name'])}</h2>{faq_html}</div></section>'''
    if ranked:
        title = fit_title('Best Car Workshops in %s: Top Rated & WhatsApp' % a['name'], 'Best Car Workshops in %s: Top Rated' % a['name'], 'Best Car Workshops in %s | WhatsApp' % a['name'], 'Car Workshops in %s: WhatsApp & Directions' % a['name'], 'Car Workshops in %s' % a['name'])
        desc = 'Compare %d car workshops in %s, ranked by Google rating and number of ratings. Open Sunday and late filters, WhatsApp and call.' % (n, a['name'])
    else:
        title = fit_title('Car Workshops in %s: WhatsApp & Directions' % a['name'], 'Car Workshops in %s | WhatsApp' % a['name'], 'Car Workshops in %s' % a['name'])
        desc = 'Find %d car workshop%s in %s, %s region, Singapore: %s. Map, nearby areas and direct WhatsApp or call.' % (n, '' if n == 1 else 's', a['name'], rname, cats.lower())
    if len(desc) > 160:
        desc = 'Compare %d car workshops in %s with Google ratings, hours and distances. WhatsApp and call.' % (n, a['name'])
    ld = [itemlist_ld('Car workshops in %s' % a['name'], es), dict(crld, **{'@context': 'https://schema.org'}), faq_ld(faqs)]
    _ix = free_n(es) >= MIN_FREE or ('areas/%s/' % slug) in INDEX_EXCEPTIONS
    FREECOUNT['areas/%s/' % slug] = free_n(es)
    page('areas/%s/' % slug, title, cap(desc, 160), body, ld, h1='Car workshops in %s' % a['name'], index=_ix, why='fewer than %d free workshops' % MIN_FREE)


def estate_service(slug, cat, es):
    """Level 3: /areas/<estate>/<service>/  (only built when 2 or more workshops match)"""
    depth = 3
    a = ESTATES[slug]
    c = CAT[cat]
    rname = RN[a['region']]
    cr, crld = crumbs(depth, [(rname, 'areas/%s/' % a['region']), (TOWNS[a['town']]['name'], 'areas/%s/' % a['town']), (a['name'], 'areas/%s/' % slug), (c['name'], None)])
    n = len(es)
    h1 = '%s in %s' % (c['name'], a['name'])
    near_s = [k for k in a['nearby'] if (k, cat) in PUB_PAIRS]
    near_a = [k for k in a['nearby'] if k in PUB_ESTATES]
    near_html = ('Nearby areas on %s: %s.' % (E(SITE_NAME), ', '.join('<a href="%sareas/%s/">%s</a>' % (pre(depth), k, E(ESTATES[k]['name'])) for k in near_a))) if near_a else ''
    if near_s:
        near_html += ' %s is also listed in %s.' % (E(c['name']), ', '.join('<a href="%sareas/%s/%s/">%s</a>' % (pre(depth), k, cat, E(ESTATES[k]['name'])) for k in near_s))
    sfaqs = [
        ('Which workshops offer %s in %s?' % (c['name'].lower(), a['name']), '%s lists %s for %s in %s.' % (SITE_NAME, and_list(e['name'] for e in es), c['name'].lower(), a['name'])),
        ('How do I contact a workshop in %s?' % a['name'], 'Tap WhatsApp or Call on a workshop card or page. WhatsApp messages are prefilled with the workshop name and say you found them on %s, so you only need to add your car and what you need.' % SITE_NAME),
        ('What is near %s?' % a['name'], 'Nearby MRT stations include %s. Local landmarks include %s.' % (and_list(area_copy(slug)[1]), and_list(area_copy(slug)[2]))),
    ]
    intro = '%d workshops in %s are listed for %s: %s. Each page shows the address, hours and how to contact the workshop.' % (n, a['name'], c['name'].lower(), and_list(e['name'] for e in es))
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>{E(h1)}</h1><p class="lede">{E(intro)}</p></div></section>
{featured_sec(es, depth, 'areas/%s/%s/' % (slug, cat), 'in ' + a['name'])}
<section><div class="w"><div class="grid">{''.join(card(e, depth, 'areas/%s/%s/' % (slug, cat)) for e in es if not is_paid(e))}</div>{shortlist_links(es, a['name'])}
<p class="fine" style="margin-top:14px">More in this area: <a href="../">all workshops in {E(a['name'])}</a>, or <a href="{pre(depth)}services/{cat}/">{E(c['name'].lower())} across Singapore</a>.</p></div></section>
<section class="alt"><div class="w nar"><h2>About {E(c['name'].lower())} in {E(a['name'])}</h2><p>{E(area_copy(slug)[0])}</p><p>{near_html}</p></div></section>
{faq_block(sfaqs, 'Questions about %s in %s' % (c['name'].lower(), a['name']))}'''
    FREECOUNT['areas/%s/%s/' % (slug, cat)] = free_n(es)
    title = fit_title('%s in %s | %s' % (c['name'], a['name'], SITE_NAME), '%s in %s' % (c['name'], a['name']))
    desc = '%s in %s, %s region: %s. Compare listings and contact a workshop directly.' % (c['name'], a['name'], rname, and_list(e['name'] for e in es))
    page('areas/%s/%s/' % (slug, cat), title, cap(desc, 160), body, [itemlist_ld(h1, es), dict(crld, **{'@context': 'https://schema.org'}), faq_ld(sfaqs)], h1=h1, index=free_n(es) >= MIN_FREE, why='fewer than %d free workshops' % MIN_FREE)


def is_paid(e):
    """Paying Featured client. Founder-owned listings are Premium-layout pages but not paid placements."""
    return e['tier'] == 'premium_leadgen' and not e.get('founder_owned')


FOUNDER_LABEL = "Owned by the site's founder"


def tier_badge(e_or_tier, cls=''):
    if not isinstance(e_or_tier, str) and e_or_tier.get('founder_owned'):
        return '<span class="tier t-founder%s">%s</span>' % ((' ' + cls) if cls else '', E(FOUNDER_LABEL))
    t = e_or_tier if isinstance(e_or_tier, str) else e_or_tier['tier']
    return '<span class="tier t-%s%s">%s</span>' % (t, (' ' + cls) if cls else '', E(TIERS[t]['badge']))



def page_label(page_path):
    return '/' + page_path


SITE_HOST = DOMAIN   # shown in the prefill so workshops see where the lead came from
WA_MSG = 'Hi, I found you on %s (%s). I would like to ask about %s for my car'
SERVICE_PHRASE = {'general-servicing-repair': 'servicing or repair', 'spray-painting-bodywork': 'spray painting or bodywork', 'gearbox-repair': 'gearbox repair',
                  'abs-ecu-module-repair': 'ABS or ECU repair', 'car-battery': 'a car battery', 'car-detailing-coating': 'detailing or coating', 'car-aircon-repair': 'car aircon repair',
                  'car-wrap-ppf': 'a wrap or PPF', 'car-parts': 'car parts'}


def wa_href(e, page_path):
    """Directory WhatsApp link for ANY tier. Prefill names the directory and its domain so the workshop can see where the lead came from."""
    return wa_link(e['whatsapp'], WA_MSG % (SITE_NAME, SITE_HOST, SERVICE_PHRASE[e['category']]))


def track_attrs(kind, e, page_path):
    return 'data-cta="%s_dir_%s" data-tier="%s" data-page="%s"' % (kind, e['slug'], e['tier'], E(page_label(page_path)))


def wa_btn(e, page_path, cls='', label='WhatsApp'):
    return '<a class="btn wa%s" href="%s" target="_blank" rel="noopener" %s>%s %s</a>' % (
        (' ' + cls) if cls else '', E(wa_href(e, page_path)), track_attrs('whatsapp', e, page_path), WA_SVG, E(label))


def tel_of(e):
    return '+' + e['whatsapp']   # Call always uses the mobile (same number as WhatsApp), never a landline (Edwin 2 Nov 2026)


def call_btn(e, page_path, cls='', label='Call'):
    return '<a class="btn%s" href="tel:%s" %s>%s %s</a>' % ((' ' + cls) if cls else '', tel_of(e), track_attrs('call', e, page_path), ic('phone'), E(label))


def contact_btns(e, page_path, cls=''):
    """WhatsApp + Call on EVERY card and profile (rule 4)."""
    return wa_btn(e, page_path, cls) + call_btn(e, page_path, cls)


def call_icon(e, page_path):
    return call_btn(e, page_path, 'sm')


def rating_line(e):
    """Edwin 3 Nov 2026: Google rating + rating count + checked month-year + See Google reviews link. Skipped (empty) when there is no rating or checked date.
    Wording is "Google ratings" (Edwin 3 Nov 2026); the link text stays "See Google reviews"."""
    g = GCACHE.get(e['slug']) or {}
    gr = e.get('google_rating') or {}   # data/workshops/<slug>.json, source Google Places (founder listing: the owner's own Google profile, with count_text)
    n, r, fa = gr.get('count') or g.get('userRatingCount'), gr.get('rating') or g.get('rating'), gr.get('checked') or g.get('fetched_at')
    if not (r and n and fa):
        return ''
    d = datetime.date.fromisoformat(fa)
    ntxt = gr.get('count_text') or format(n, ',')
    url = gr.get('url') or gm_url(e)
    return ('<p class="rtg"><b>%.1f</b> (%s Google rating%s) (checked %s) <a href="%s" target="_blank" rel="noopener" data-cta="gr_%s">See Google reviews</a></p>'
            % (float(r), ntxt, '' if n == 1 else 's', d.strftime('%B %Y'), E(url), e['slug']))


def gm_url(e):
    """Official Google Maps search URL (no API key, no billable call): name + address, pinned to the place_id."""
    return 'https://www.google.com/maps/search/?api=1&query=%s&query_place_id=%s' % (quote('%s %s Singapore' % (e['name'], e['address_public'])), e['place_id'])


def dir_url(e):
    """Official Google Maps directions URL."""
    return 'https://www.google.com/maps/dir/?api=1&destination=%s&destination_place_id=%s' % (quote('%s, %s' % (e['name'], e['address_public'])), e['place_id'])


def gm_btn(e, page_path, cls='', short=False):
    return ('<a class="btn%s" href="%s" target="_blank" rel="noopener" data-cta="maps_%s" data-tier="%s" data-page="%s">%s %s</a>'
            % ((' ' + cls) if cls else '', E(gm_url(e)), e['slug'], e['tier'], E(page_label(page_path)), ic('pin'),
               'Photos &amp; reviews' if short else 'See photos, reviews &amp; hours on Google Maps'))


def dir_btn(e, page_path, cls=''):
    return ('<a class="btn%s" href="%s" target="_blank" rel="noopener" data-cta="directions_%s" data-tier="%s" data-page="%s" data-map>%s Directions</a>'
            % ((' ' + cls) if cls else '', E(dir_url(e)), e['slug'], e['tier'], E(page_label(page_path)), ic('pin')))


def shortlist_url(es):
    """'Open these workshops in Google Maps' (map_action=shortlist, max 20 place_ids per link). Only entries with a place_id."""
    ids = [e['place_id'] for e in es if e.get('place_id')][:20]
    return 'https://www.google.com/maps/search/?api=1&query=car%%20workshop&map_action=shortlist&place_ids=%s' % ','.join(ids) if ids else None


def shortlist_links(es, label_area):
    ids = [e for e in es if e.get('place_id')]
    if not ids:
        return ''
    chunks = [ids[k:k + 20] for k in range(0, len(ids), 20)]
    return '<p class="fine gmshort">%s</p>' % ' '.join(
        '<a href="%s" target="_blank" rel="noopener" data-cta="maps_shortlist">%s Open these workshops in Google Maps%s</a>' % (
            E(shortlist_url(c)), ic('pin'), (' (%d of %d)' % (n + 1, len(chunks))) if len(chunks) > 1 else '') for n, c in enumerate(chunks))


def photo_img(p, depth, lazy=True, cls=''):
    if p.get('f'):
        return img_tag(p['f'], p['alt'], depth, lazy=lazy, cls=cls)
    return '<img src="%s" alt="%s"%s decoding="async" referrerpolicy="no-referrer"%s>' % (
        E(p['u'], True), E(p['alt'], True), ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '')


def tile(e):
    return '<div class="tile" aria-hidden="true">%s<b>%s</b><span>%s</span></div>' % (ic(CAT[e['category']]['icon']), E(e['name']), E(e.get('tile_text', CAT[e['category']]['short'])))


def region_label(e):
    if e['region'] == 'mobile':
        return 'Mobile \u00b7 island-wide'
    return '%s \u00b7 %s' % (e['area_label'], RN[e['region']])


def area_link_html(e, up):
    """' or workshops in <Estate>' / ' or mobile services' link for the foot of a workshop page."""
    if e['region'] == 'mobile':
        return ' or <a href="%sareas/mobile/">other mobile services</a>' % up
    k = e['estates'][0]
    return ' or <a href="%sareas/%s/">workshops in %s</a>' % (up, k, E(ESTATES[k]['name']))


def workshop_trail(e):
    """Home > Region > Estate > Workshop (mobile services: Home > Mobile > Workshop)."""
    t = [(RN[e['region']], 'areas/%s/' % e['region'])]
    if e['estates']:
        k = e['estates'][0]
        t.append((TOWNS[ESTATES[k]['town']]['name'], 'areas/%s/' % ESTATES[k]['town']))
        t.append((ESTATES[k]['name'], 'areas/%s/' % k))
    return t + [(e['name'], None)]


def owner_note(e, depth, page_path, cls='owner-note'):
    """Basic cards and pages: a clear claim button (Edwin 3 Nov 2026) that goes to the claim page (/list-your-workshop/?w=<slug>#claim), where the owner messages Page One.
    Customers never see Page One's WhatsApp on a listing; the button leads to the owner page. Paid tiers keep the small grey line."""
    pl_ = E(page_label(page_path))
    rm = (' <a class="rm" href="%slist-your-workshop/?w=%s#remove" data-cta="remove_%s" data-page="%s">Remove my listing</a>'
          % (pre(depth), e['slug'], e['slug'], pl_)) if e['tier'] == 'free' else ''
    if e['tier'] == 'free':
        return ('<div class="%s"><a class="claimbtn" href="%slist-your-workshop/?w=%s#claim" data-cta="claim_%s" data-page="%s">Is this your workshop? Claim this free listing</a>%s</div>'
                % (cls, pre(depth), e['slug'], e['slug'], pl_, ('<p class="fine claim-rm">%s</p>' % rm.strip()) if rm else ''))
    return ('<p class="%s">For business owners: Is this your workshop? <a href="%slist-your-workshop/?w=%s#claim" data-cta="claim_%s" data-page="%s">Manage this listing &rarr;</a></p>'
            % (cls, pre(depth), e['slug'], e['slug'], pl_))


SYN = {   # extra words people type for each service (search only, never shown)
    'spray-painting-bodywork': 'spray paint painting respray resprayed colour color bodywork body dent scratch panel',
    'gearbox-repair': 'gearbox transmission auto automatic gear shift cvt dsg',
    'abs-ecu-module-repair': 'abs ecu module ecm tcm brake engine computer control unit electronics',
    'car-battery': 'battery batteries replace replacement jump start flat alternator',
    'car-aircon-repair': 'aircon air con ac gas compressor condenser cooling coil cold leak smell odour',
    'car-detailing-coating': 'detailing detail coating ceramic polish polishing wash clean cleaning interior',
    'car-wrap-ppf': 'wrap wraps wrapping ppf film protection tint sticker',
    'car-parts': 'parts part spare accessories',
    'general-servicing-repair': 'servicing service repair maintenance aircon air con ac cooling oil brake workshop mechanic',
}


CAT_COLOR = {'general-servicing-repair': '#1d5fb8', 'spray-painting-bodywork': '#c0392b', 'gearbox-repair': '#d97706', 'abs-ecu-module-repair': '#7c3aed',
             'car-battery': '#15803d', 'car-detailing-coating': '#0e8a8a', 'car-aircon-repair': '#0369a1', 'car-wrap-ppf': '#c026a3', 'car-parts': '#5b6472'}


def initials(name):
    w = [x for x in re.split(r'[^A-Za-z0-9]+', name) if x and x.lower() not in ('the', 'pte', 'ltd', 'and', 'of')]
    return (''.join(x[0] for x in w[:2]) or name[:1]).upper()


def bt_style(e):
    return '--bc:%s' % CAT_COLOR.get(e['category'], '#1d5fb8')


def gph_tile(e):
    """Branded placeholder: workshop initials in a coloured circle + category icon (colour by category). Static, no Places call."""
    c = CAT[e['category']]
    return '<span class="bt" aria-hidden="true"><span class="ini">%s</span><span class="cic">%s</span></span>' % (E(initials(e['name'])), ic(c.get('icon', 'gear')))


def card_search(e):
    c = CAT[e['category']]
    t = ' '.join([e['name'], c['name'], SYN.get(c['slug'], ''), ' '.join(_tags.BY_ID[x]['label'] for x in e.get('tags', [])), e['area_label'], e.get('desc', ''), ' '.join(e.get('card_text', [])[:1]),
                  ' '.join(s['n'] for s in e['services']), ' '.join(e.get('services_public', [])), e.get('domain', ''), e.get('regions_note', ''), e.get('service_area', '')]).lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()


def card_profile(e):
    """Search-index text for the AI-smart homepage search (Edwin 3 Nov 2026): chips, services, customer-mentioned services/brands, themes, payment/parking words.
    Built only from the Basic profile data (pilot JSON + Google cache), so the search uses exactly what the profile page shows."""
    pl = PILOT.get(e['slug'])
    if not pl:
        return '', ''
    g = GCACHE.get(e['slug']) or {}
    ment = [x for x in (pl.get('mentioned_services') or [])]
    po = g.get('paymentOptions') or {}
    pk = g.get('parkingOptions') or {}
    words = list(pl.get('chips', [])) + list(pl.get('services', [])) + list(pl.get('good_for', [])) + ment + [pl.get('themes', ''), g.get('editorialSummary') or '']
    if any(po.get(k) for k in ('acceptsCreditCards', 'acceptsDebitCards', 'acceptsNfc')):
        words.append('card payment contactless')
    if pk.get('freeParkingLot') or pk.get('freeGarageParking'):
        words.append('free parking')
    if pk.get('paidParkingLot') or pk.get('paidGarageParking'):
        words.append('parking')
    prof = re.sub(r'[^a-z0-9]+', ' ', ' '.join(words).lower()).strip()
    return prof, '|'.join(ment)


def card(e, depth, page_path=''):
    c = CAT[e['category']]
    attrs = 'data-search="%s" data-cat="%s" data-regions="%s" data-tier="%s"' % (E(card_search(e), True), c['slug'], ' '.join(e['regions']), e['tier'])
    _prof, _ment = card_profile(e)
    _f = FACTS.get(e['slug'])
    if _f:
        attrs += ' data-rating="%s" data-sun="%d" data-late="%d"' % ((_f['rating'] or '') if _f['n'] >= RANK_MIN_RATINGS else '', 1 if _f['sunday'] else 0, 1 if _f['late'] else 0)
    if _prof:
        attrs += ' data-profile="%s" data-mention="%s"' % (E(_prof, True), E(_ment, True))
    rg = '<p class="meta rg">%s<span>%s</span></p>' % (ic('pin'), E(region_label(e)))
    if e['tier'] == 'free':
        svc = ', '.join(e.get('services_public', [])[:3])
        return ('<article class="card basic" %s><div class="ph btile" style="%s">%s%s</div><div class="bd"><span class="tag">%s</span>'
                '<h3><a href="%sworkshops/%s/">%s</a></h3>%s%s<p class="addr">%s</p><p class="tx full svcline">%s</p>%s'
                '<div class="acts">%s<a class="btn sm" href="%sworkshops/%s/" data-cta="view_%s">View details</a></div>%s</div></article>') % (
            attrs, bt_style(e), gph_tile(e), tier_badge(e, 'on-ph'), E(c['short']), pre(depth), e['slug'], E(e['name']), rg, rating_line(e), E(e['address_public']), E(svc), card_facts(e) + tap_line(e),
            contact_btns(e, page_path, 'sm'), pre(depth), e['slug'], e['slug'], owner_note(e, depth, page_path, 'claim'))
    ci = e.get('card_img')
    ph = photo_img(dict(ci, alt=ci['alt']), depth, lazy=True) if ci else tile(e)
    acts = contact_btns(e, page_path, 'sm')
    more = ('<a class="btn sm" href="%sworkshops/%s/" data-cta="view_%s">View details</a>' % (pre(depth), e['slug'], e['slug'])) if e.get('founder_owned') else ''
    return ('<article class="card" %s>'
            '<div class="ph">%s%s</div><div class="bd"><span class="tag">%s</span><h3><a href="%sworkshops/%s/">%s</a></h3>'
            '%s%s<p class="tx">%s</p><div class="acts">%s%s</div></div></article>') % (
        attrs, ph, tier_badge(e, 'on-ph'), E(c['short']), pre(depth), e['slug'], E(e['name']), rg, rating_line(e), E(e['card_text'][0]), acts, more)


def slide(e):
    c = CAT[e['category']]
    ci = e.get('card_img')
    return ('<li><article class="card fc"><div class="ph">%s%s</div><div class="bd"><span class="tag">%s</span><h3><a href="workshops/%s/">%s</a></h3>'
            '<p class="meta rg">%s<span>%s</span></p><p class="tx">%s</p><div class="acts">%s<a class="btn sm" href="workshops/%s/">View</a></div></div></article></li>') % (
        photo_img(ci, 0, lazy=True) if ci else tile(e), tier_badge(e, 'on-ph'), E(c['short']), e['slug'], E(e['name']), ic('pin'), E(region_label(e)), E(e['card_text'][0]),
        contact_btns(e, '', 'sm'), e['slug'])


def free_card(depth, ex=FREE_EXAMPLE):
    """Free-tier card: plain. No photo, no phone. Shown only as a labelled example (made-up name)."""
    c = CAT[ex['category']]
    return ('<article class="card free-card"><div class="bd"><span class="ex-flag">Example only, not a real business</span>%s<span class="tag">%s</span>'
            '<h3>%s</h3><p class="meta">%s</p><p class="tx">%s</p><div class="acts">'
            '<span class="btn sm wa ex" aria-disabled="true">%s WhatsApp</span><span class="btn sm ex" aria-disabled="true">Website: %s</span></div></div></article>') % (
        tier_badge('free'), E(c['short']), E(ex['name']), E(ex['area_label']), E(ex['text']), WA_SVG, E(ex['site_label']))


def tiers_strip():
    """Short how-it-works summary for the home page. No prices, no plan names (Edwin 3 Nov 2026: claiming is free)."""
    items = [
        ('free', 'Every workshop has a free card and short page built from its public Google Business Profile: address, WhatsApp and Call using the mobile number on that profile, Directions, and a link to its Google Maps listing.'),
        ('premium', 'Owners can claim their listing for free: correct hours and WhatsApp, add your own photos, services and brands, and see how many drivers tapped WhatsApp and Call.'),
        ('premium_leadgen', 'Featured workshops at the top of the home page are paid placements and are marked Featured (paid).'),
    ]
    li = ''.join('<li><b>%s</b>%s</li>' % (E(h), E(txt)) for h, txt in (('Free card. ', items[0][1]), ('Claim it free. ', items[1][1]), ('Featured (paid). ', items[2][1])))
    return '<ol class="steps tiers-strip">%s</ol><p class="fine" style="margin-top:10px"><a href="list-your-workshop/">Claim your free listing</a></p>' % li


def ld_business(e, url):
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', '@id': url + '#business', 'name': e['name'], 'url': url, 'mainEntityOfPage': url}
    first = next((p for p in (e.get('photos') or []) if not (p.get('f') or '').endswith('.svg')), None) or e.get('card_img')
    if first:
        ld['image'] = [BASE + 'assets/img/' + first['f'] if first.get('f') else first['u']]
    if e.get('phone'):
        ld['telephone'] = e['phone']
    adds = [a for a in e.get('addresses', []) if a.get('postal')]
    if e['slug'] == 'battery-rescue-sg':
        ld['location'] = [{'@type': 'Place', 'name': a['label'], 'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': 'Singapore', 'addressCountry': 'SG'}} for a in e['addresses']]
    elif e.get('addresses'):
        a0 = e['addresses'][0]
        ld['address'] = {'@type': 'PostalAddress', 'streetAddress': a0['street'], 'postalCode': a0['postal'], 'addressLocality': 'Singapore', 'addressCountry': 'SG'}
        if len(e['addresses']) > 1:
            ld['location'] = [{'@type': 'Place', 'name': a['label'], 'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'postalCode': a['postal'], 'addressLocality': 'Singapore', 'addressCountry': 'SG'}} for a in e['addresses'][1:]]
    ld['hasMap'] = e['map_url']
    if e.get('hours_ld'):
        ld['openingHoursSpecification'] = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': d, 'opens': o, 'closes': c} for d, o, c in e['hours_ld']]
    if e['region'] == 'mobile':
        ld['areaServed'] = {'@type': 'Country', 'name': 'Singapore'}
    else:
        ld['areaServed'] = [{'@type': 'Place', 'name': ESTATES[k]['name'] + ', Singapore'} for k in e['estates']]
    ld['makesOffer'] = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['n']}} for s in e['services']]
    same = list(e.get('social') or [])
    if e['tier'] in ('premium_leadgen', 'none'):
        same.append(e['url'])
    if same:
        ld['sameAs'] = same
    if e.get('legal'):
        ld['legalName'] = e['legal']
        ld['taxID'] = e['uen']
    return ld


def basic_texts():
    """Basic page text is built here from the record fields; the records store no display strings."""
    for e in ENTRIES:
        if e['tier'] != 'free':
            continue
        svc = and_list(s[:1].lower() + s[1:] for s in e['services_public'][:3])
        e['desc'] = 'Car workshop at %s.' % e['street']
        e['lede'] = '%s is a car workshop at %s in %s. %s %s.' % (e['name'], e['street'], e['area_label'], 'It offers' if e['services_source'] == 'google_profile' else 'Its own website lists', svc)
        e['area_ctx'] = '%s is in the %s planning area, part of the %s region of Singapore.' % (e['area_label'], e['planning_area'], RN[e['region']])


def embed_url(e):
    """Google Maps Embed API (free, key restricted to this site): name + address for Basic, place_id for Verified and Premium."""
    q = ('place_id:%s' % e['place_id']) if e['tier'] != 'free' else ('%s %s Singapore' % (e['name'], e['address_public']))
    return 'https://www.google.com/maps/embed/v1/place?key=%s&q=%s' % (PLACES_BROWSER_KEY, quote(q))


PILOT = {}
_pd = os.path.join(HERE, '..', 'data', 'pilot')
if os.path.isdir(_pd):
    for _f in sorted(os.listdir(_pd)):
        if _f.endswith('.json'):
            PILOT[_f[:-5]] = json.load(open(os.path.join(_pd, _f)))


GCACHE = {}
_gd = os.path.join(HERE, '..', 'data', 'google_cache')
if os.path.isdir(_gd):
    for _f in sorted(os.listdir(_gd)):
        if _f.endswith('.json'):
            GCACHE[_f[:-5]] = json.load(open(os.path.join(_gd, _f)))


def _hrs_facts(descs):
    """From Google weekday descriptions: (open_sunday, open_late). open_late = any Mon-Fri closing time after 7pm. None when the hours are unknown."""
    if not descs:
        return None, None
    sun = None; late = False; weekdays = 0
    for d in descs:
        day, _, rest = d.partition(':')
        day = day.strip().lower(); rest = rest.replace('\u202f', ' ').replace('\u2009', ' ').strip()
        if day == 'sunday':
            sun = bool(rest) and 'closed' not in rest.lower()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            weekdays += 1
            if 'open 24' in rest.lower():
                late = True
                continue
            for m_ in re.finditer(r'[\u2013\-]\s*(\d{1,2})(?::(\d{2}))?\s*(AM|PM)', rest):
                h, mi, ap = int(m_.group(1)) % 12, int(m_.group(2) or 0), m_.group(3)
                mins = (h + (12 if ap == 'PM' else 0)) * 60 + mi
                if ap == 'AM' and h == 0 and mi == 0:
                    mins = 24 * 60   # closes at midnight
                if mins > 19 * 60:
                    late = True
    return sun, (late if weekdays else None)


def _ord(n):
    return {1: '1st', 2: '2nd', 3: '3rd'}.get(n, '%dth' % n)


FACTS = {}   # slug -> dict(...). Recomputed on every build from data/google_cache + the records (Edwin 3 Nov 2026).
RANK_MIN_RATINGS = 20   # Edwin 3 Nov 2026 (round 2): rank by Google rating only among workshops in the same estate with at least 20 Google ratings
RANK_MIN_GROUP = 8      # Edwin 3 Nov 2026 (ranking honesty): a rank line, 'Best' title or ranked order exists only where the estate has at least 8 comparable workshops (20+ ratings)
RANK_PRIOR = 50         # Bayesian prior weight: a workshop is scored as if it had 50 extra ratings at the estate average, so few ratings are pulled toward the average
TAPS = {}               # slug -> {'whatsapp': n, 'call': n} taps, all-time and never reset (data/taps.json, written by src/taps.py from the Controller's CtaClick rows)
CLAIMED = set()          # data/claims.json: slugs whose owner has claimed the listing and been checked (owner badge only; no ranking or guide-order advantage)
TAP_SHOW_MIN = 5        # a card shows its WhatsApp tap count only from 5 taps
_tf = os.path.join(HERE, '..', 'data', 'taps.json')
TAPS_ASOF = ''
_cf = os.path.join(HERE, '..', 'data', 'claims.json')
if os.path.isfile(_cf):
    CLAIMED = set(json.load(open(_cf)))
if os.path.isfile(_tf):
    _t = json.load(open(_tf))
    TAPS = _t.get('counts', {})
    TAPS_ASOF = _t.get('as_of', '')


def _km(a, b):
    """Great-circle distance in km between two entries with lat/lon."""
    la1, lo1, la2, lo2 = [math.radians(float(x)) for x in (a['lat'], a['lon'], b['lat'], b['lon'])]
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def km_text(d):
    """Never '0.0 km': anything under 0.1 km (same building or block) reads 'under 0.1 km'."""
    return 'under 0.1 km' if d < 0.1 else '%.1f km' % d


def nearest(e, k=6, same_estate_first=False):
    """Nearest other listed workshops that have coordinates: [(entry, km)]. Entries at exactly the same point are real neighbours (same building), not errors."""
    if e.get('lat') is None:
        return []
    out = [(o, _km(e, o)) for o in ENTRIES if o['slug'] != e['slug'] and o.get('lat') is not None]
    out.sort(key=lambda t: (round(t[1], 3), t[0]['name'].lower()))
    if same_estate_first:
        same = [t for t in out if t[0]['estates'][:1] == e['estates'][:1]]
        rest = [t for t in out if t[0]['estates'][:1] != e['estates'][:1]]
        out = same + rest
    return out[:k]


def clock(m):
    """Minutes after midnight -> '6:30 PM' (1440 = 12 AM)."""
    m = m % 1440
    h, mi = divmod(m, 60)
    return '%d%s %s' % (h % 12 or 12, (':%02d' % mi) if mi else '', 'PM' if h >= 12 else 'AM')


def _clean_h(t):
    return t.replace(' ', ' ').replace(' ', ' ')


def _mins(h, mi, ap):
    h = int(h) % 12
    return (h + (12 if ap.upper() == 'PM' else 0)) * 60 + int(mi or 0)


def _ranges(rest):
    """'9:30 AM - 6:30 PM, 7 - 9 PM' -> [(open_min, close_min)]. 12:00 AM close = 1440. 'Open 24 hours' -> [(0, 1440)]."""
    rest = _clean_h(rest)
    if 'open 24' in rest.lower():
        return [(0, 1440)]
    out = []
    for m_ in re.finditer(r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?\s*[–\-]\s*(\d{1,2})(?::(\d{2}))?\s*(AM|PM)', rest):
        h1, m1, a1, h2, m2, a2 = m_.groups()
        a1 = a1 or a2
        o, c = _mins(h1, m1, a1), _mins(h2, m2, a2)
        if c == 0:
            c = 1440
        if c <= o:
            c += 1440 if c < o else 0
        out.append((o, c))
    return out


def _hrs_facts(descs):
    """From Google weekday descriptions: (open_sunday, open_late, latest weekday close in minutes or None). open_late = any Mon-Fri close after 7pm. None when hours are unknown."""
    if not descs:
        return None, None, None
    sun = None; late = False; weekdays = 0; latest = None
    for d in descs:
        day, _, rest = d.partition(':')
        day = day.strip().lower(); rest = rest.strip()
        if day == 'sunday':
            sun = bool(rest) and 'closed' not in rest.lower()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            weekdays += 1
            for o, c in _ranges(rest):
                latest = c if latest is None else max(latest, c)
                if c > 19 * 60:
                    late = True
    return sun, (late if weekdays else None), (latest if weekdays else None)


def _ord(n):
    return {1: '1st', 2: '2nd', 3: '3rd'}.get(n, '%dth' % n)


def group_hours(descs):
    """Google weekday lines -> readable groups: 'Monday to Friday 9:30 AM to 6:30 PM; Saturday 9:30 AM to 1:30 PM; closed on Sunday'. Wording only; times are Google's."""
    rows = []
    for d in descs or []:
        day, _, rest = d.partition(':')
        rows.append((day.strip(), _clean_h(rest.strip()).replace(' – ', ' to ').replace('–', ' to ')))
    out = []; i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and rows[j + 1][1] == rows[i][1]:
            j += 1
        span = rows[i][0] if i == j else '%s to %s' % (rows[i][0], rows[j][0])
        out.append(('closed on %s' % span) if 'closed' in rows[i][1].lower() else '%s %s' % (span, rows[i][1]))
        i = j + 1
    return '; '.join(out)


def hours_spec(descs):
    """schema.org openingHoursSpecification from Google weekday lines (times as Google lists them)."""
    spec = []
    for d in descs or []:
        day, _, rest = d.partition(':')
        day = day.strip()
        for o, c in _ranges(rest.strip()):
            fmt = lambda m: '%02d:%02d' % ((m // 60) % 24, m % 60)
            spec.append({'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'https://schema.org/' + day, 'opens': fmt(o), 'closes': fmt(c)})
    return spec


def compute_facts():
    FACTS.clear()
    by_estate = {}; closes = {}
    for e in ENTRIES:
        g = GCACHE.get(e['slug'])
        if e['tier'] != 'free' or not g:
            continue
        if g.get('rating') and (g.get('userRatingCount') or 0) >= RANK_MIN_RATINGS:
            by_estate.setdefault(e['estate'], []).append((e['slug'], float(g['rating']), int(g['userRatingCount'])))
        _s, _l, cl = _hrs_facts(g.get('weekdayDescriptions'))
        if cl is not None:
            closes.setdefault(e['estate'], []).append((e['slug'], cl))
    scores = {}   # estate -> {slug: score}, only for estates with RANK_MIN_GROUP+ comparable workshops
    for est, grp in by_estate.items():
        if len(grp) >= RANK_MIN_GROUP:
            avg = sum(r for _, r, _ in grp) / len(grp)
            scores[est] = {sl: (v / (v + RANK_PRIOR)) * r + (RANK_PRIOR / (v + RANK_PRIOR)) * avg for sl, r, v in grp}
    for e in ENTRIES:
        g = GCACHE.get(e['slug'])
        if e['tier'] != 'free' or not g:
            continue
        f = dict(rating=None, rank_text='', sunday=None, late=None, ment=[], n=g.get('userRatingCount') or 0, close=None, close_rank='', rank=None, rank_n=0, score=None)
        sun, late, cl = _hrs_facts(g.get('weekdayDescriptions'))
        f['sunday'], f['late'], f['close'] = sun, late, cl
        f['ment'] = list((PILOT.get(e['slug']) or {}).get('mentioned_services') or [])[:3]
        nm = ESTATES[e['estate']]['name']
        if g.get('rating'):
            f['rating'] = float(g['rating'])
        sc = scores.get(e['estate'], {})
        if e['slug'] in sc:
            f['score'] = sc[e['slug']]
            rank = 1 + sum(1 for v in sc.values() if v > f['score'] + 1e-9)
            tie = sum(1 for sl, v in sc.items() if sl != e['slug'] and abs(v - f['score']) <= 1e-9) > 0
            f['rank_n'] = len(sc); f['rank'] = rank
            f['rank_text'] = '%s%s of %d %s workshops with %d or more Google ratings, by rating and number of ratings together' % (('Joint ' if tie else ''), 'Ranked ' + _ord(rank), len(sc), nm, RANK_MIN_RATINGS)
            if tie:
                f['rank_text'] = 'Joint ' + f['rank_text'][len('Joint '):].replace('Ranked ', 'ranked ', 1)
        grp = closes.get(e['estate'], [])
        if cl is not None and len(grp) >= 3:
            others = [c for sl, c in grp if sl != e['slug']]
            x = sum(1 for c in others if cl > c)
            if x >= 1:
                f['close_rank'] = 'Closes later than %d of %d other %s workshops we list with Google Maps hours' % (x, len(others), nm)
        FACTS[e['slug']] = f


def rank_sorted(es):
    """Free (Basic) listings only, in display order. Where the estate has 8+ comparable workshops: ranked ones by combined score, best first, then the rest A to Z.
    Everywhere else: A to Z, no ranking. Paid Featured clients are never part of this list (see featured_sec)."""
    free = [e for e in es if not is_paid(e)]   # Basic and Verified, same rules, no boost for Verified (Edwin 3 Nov 2026)
    sc = lambda e: (FACTS.get(e['slug']) or {}).get('score')
    if any(e['tier'] != 'free' for e in free):   # founder-owned or Verified present: plain A to Z for the whole list (Edwin 3 Nov 2026)
        return sorted(free, key=lambda e: e['name'].lower())
    ranked = sorted([e for e in free if sc(e) is not None], key=lambda e: (-sc(e), -(FACTS[e['slug']]['n']), e['name'].lower()))
    rest = sorted([e for e in free if sc(e) is None], key=lambda e: e['name'].lower())
    return ranked + rest


def card_facts(e):
    f = FACTS.get(e['slug'])
    if not f:
        return ''
    tags = []
    if f['sunday']:
        tags.append('<li class="ct open">Open Sunday</li>')
    if f['late']:
        tags.append('<li class="ct open">Open late on weekdays</li>')
    out = ''
    if f['rank_text']:
        out += '<p class="rankline">%s</p>' % E(f['rank_text'])
    if tags:
        out += '<ul class="ctags" aria-label="Opening">%s</ul>' % ''.join(tags)
    if f['ment']:
        out += '<p class="mentline"><b>Customers mention:</b> %s</p>' % E(', '.join(f['ment']))
    return out


def compare_html(e):
    f = FACTS.get(e['slug'])
    if not f:
        return ''
    li = []
    if f['rank_text']:
        li.append('<li>%s.</li>' % E(f['rank_text']))
    if f['sunday'] is not None:
        li.append('<li>%s</li>' % ('Open on Sundays.' if f['sunday'] else 'Closed on Sundays.'))
    if f['close_rank']:
        li.append('<li>%s.</li>' % E(f['close_rank']))
    if f['late'] is not None:
        if f['close'] is not None:
            li.append('<li>%s</li>' % (('Open late on weekdays: its latest weekday closing time is %s.' if f['late'] else 'Its latest weekday closing time is %s.') % clock(f['close'])))
    near = nearest(e, 3)
    nb = ''
    if near:
        nb = '<h3>Nearest listed workshops</h3><ul class="cmp near3">%s</ul>' % ''.join('<li><a href="../%s/">%s</a>, %s away</li>' % (o['slug'], E(o['name']), km_text(d)) for o, d in near)
    return ('<h3>How it compares</h3><ul class="cmp">%s</ul>%s<p class="fine">Worked out by us from its Google Maps details and the other workshops we list. Distances are straight-line between listed addresses. It changes as we add workshops.</p>' % (''.join(li), nb)) if (li or nb) else ''


def mention_html(pl):
    m = pl.get('mentioned_services') or []
    if not m:
        return ''
    return '<h3 class="mh">Customers mention</h3><p class="fine">Taken from what customers say on Google Maps, in our own words. Not a list the workshop gave us.</p><ul class="svc-grid">%s</ul>' % ''.join('<li><span class="si">%s</span><span>%s</span></li>' % (ic(pilot_icon(x)), E(x)) for x in m)


def pilot_icon(t):
    t = t.lower()
    for keys, icon in (('aircon', 'snow'), (('ecu', 'diagnos', 'troubleshoot', 'engine'), 'chip'), (('spray', 'paint', 'panel beating'), 'spray'), (('claim', 'insurance'), 'shield'),
                       (('tyre', 'alignment', 'wheel'), 'wheel'), (('oil', 'servicing', 'service'), 'drop'), (('transmission', 'gearbox', 'suspension', 'absorber', 'drive shaft', 'lower arm', 'timing belt'), 'gear'),
                       (('towing', 'tow'), 'out'), (('van', 'private-hire', 'commercial', 'vehicle'), 'car')):
        if any(k in t for k in ([keys] if isinstance(keys, str) else keys)):
            return icon
    return 'wrench'


def tap_line(e):
    """Public WhatsApp tap count (Edwin 3 Nov 2026): only from 5 total taps (all-time, never reset), anonymous visits counted, nothing about the person. Empty until then."""
    t = (TAPS.get(e['slug']) or {}).get('whatsapp') or 0
    if t < TAP_SHOW_MIN or e['tier'] != 'free':
        return ''
    return '<p class="tapline">%d drivers have WhatsApped this workshop via %s</p>' % (t, E(SITE_NAME))


def fact_faqs(e, pl):
    """5 to 7 FAQs answered only from facts we hold: Google hours/parking/payment (with the check date), the mobile on its Google listing, the address, what customers mention.
    Plain text answers (also used for FAQPage). No rating or review words (the pilot check keeps those inside the Google section)."""
    g = GCACHE.get(e['slug']) or {}
    f = FACTS.get(e['slug']) or {}
    nm = e['name']
    d = g.get('fetched_at', '')
    qa = {}
    hrs = g.get('weekdayDescriptions') or []
    if f.get('sunday') is not None:
        qa['sun'] = ('Is %s open on Sunday?' % nm, ('Its Google Maps hours (checked %s) show it open on Sunday: %s.' % (d, group_hours([h for h in hrs if h.lower().startswith('sunday')]).replace('Sunday ', 'Sunday, ', 1))) if f['sunday']
                     else 'Its Google Maps hours (checked %s) show it closed on Sunday. Hours can change, so check by WhatsApp before you go.' % d)
    if hrs and f.get('close') is not None:
        qa['close'] = ('What time does %s close?' % nm, 'Its Google Maps hours (checked %s): %s. Hours can change, so check by WhatsApp before you go.' % (d, group_hours(hrs)))
    ment = list((pl.get('mentioned_services') or []))
    svc = list(pl.get('services') or [])
    a_ = 'We list it for %s.' % and_list(svc[:4]).lower() if svc else ''
    if ment:
        a_ += ' Customers on Google Maps mention %s, in our own words.' % and_list([(m[0].lower() + m[1:]) if len(m) > 1 and m[1].islower() else m for m in ment[:6]])
    qa['svc'] = ('What services and brands does %s handle?' % nm, (a_.strip() + ' Ask the workshop before you book, as we cannot see its full list of work.').strip())
    qa['wa'] = ('How do I WhatsApp %s?' % nm, 'Tap the WhatsApp button on this page. It opens WhatsApp to the mobile number on its Google Maps listing, with a message already written that says you found it on %s. Add your car and what you need, and send. You start the chat; we never message the workshop for you.' % SITE_NAME)
    where = '%s is at %s, in %s.' % (nm, e['address_public'], e['area_label'])
    if pl.get('mrt'):
        where += ' Getting there: %s.' % pl['mrt']
    qa['where'] = ('Where is %s?' % nm, where + ' The Directions button opens Google Maps.')
    pk = g.get('parkingOptions') or {}
    park = [n for k, n in (('freeParkingLot', 'free parking lot'), ('paidParkingLot', 'paid parking lot'), ('freeGarageParking', 'free garage parking'), ('paidGarageParking', 'paid garage parking'), ('freeStreetParking', 'free street parking'), ('paidStreetParking', 'paid street parking')) if pk.get(k)]
    if park:
        qa['park'] = ('Is there parking at %s?' % nm, 'Its Google Maps listing shows: %s (checked %s).' % (', '.join(park), d))
    po = g.get('paymentOptions') or {}
    pay = [n for k, n in (('acceptsCreditCards', 'credit cards'), ('acceptsDebitCards', 'debit cards'), ('acceptsNfc', 'contactless')) if po.get(k)]
    if pay:
        qa['pay'] = ('How can I pay at %s?' % nm, 'Its Google Maps listing shows it accepts %s (checked %s). Ask the workshop about other ways to pay.' % (', '.join(pay), d))
    qa['call'] = ('Can I call %s instead of using WhatsApp?' % nm, 'Yes. The Call button on this page dials the same mobile number as the one on its Google Maps listing. Using it costs nothing extra on %s and opens a call that you start.' % SITE_NAME)
    near = nearest(e, 3)
    if near:
        qa['near'] = ('Which other workshops are near %s?' % nm, 'The nearest listed on %s: %s. Distances are straight-line.' % (SITE_NAME, '; '.join('%s, %s away' % (o['name'], km_text(dd)) for o, dd in near)))
    order = ['sun', 'close', 'svc', 'wa', 'call', 'where', 'park', 'pay', 'near']
    return [qa[k] for k in order if k in qa][:7]


def guides_for(e):
    """Symptom and brand guides whose 'customers mention' match applies to this workshop."""
    ments = (PILOT.get(e['slug']) or {}).get('mentioned_services') or []
    out = []
    have = set(_tags.card_tags(ments))
    return [g for g in _guides.GUIDES if g['tag'] in have]


def more_in(e, depth):
    """'More in <estate>' block (Edwin 3 Nov 2026): 6 nearby workshops (same estate first) plus the matching symptom and brand guides."""
    near = nearest(e, 6, same_estate_first=True)
    if not near:
        return ''
    est = ESTATES[e['estate']]['name']
    li = ''.join('<li><a href="../%s/">%s</a><span class="fine"> %s, %s</span></li>' % (o['slug'], E(o['name']), E(o['area_label']), km_text(d)) for o, d in near)
    gl = guides_for(e)
    gh = ''
    if gl:
        gh = '<h3>Car problem and brand guides that fit</h3><ul class="tick svc-plain">%s</ul>' % ''.join('<li><a href="%s%s">%s</a></li>' % (pre(depth), _guides.gpath(g), E(g['h1'])) for g in gl[:4])
    return ('<section class="pl-sec morein"><h2>More in %s</h2><ul class="tick svc-plain nearlist">%s</ul>'
            '<p class="fine"><a href="%sareas/%s/">All workshops in %s</a></p>%s</section>') % (E(est), li, pre(depth), e['estate'], E(est), gh)


def hours_ld(e):
    g = GCACHE.get(e['slug']) or {}
    return hours_spec(g.get('weekdayDescriptions'))


def card_title(e):
    est = e['area_label']
    return fit_title('%s: Car Workshop in %s, Singapore' % (e['name'], est), '%s: Car Workshop in %s' % (e['name'], est), '%s | %s' % (e['name'], est), e['name'])


def card_desc(e):
    g = GCACHE.get(e['slug']) or {}
    est = e['area_label']
    rt = ''
    if g.get('rating') and g.get('userRatingCount'):
        n = g['userRatingCount']
        rt = ' Rated %s from %s Google rating%s.' % (g['rating'], format(n, ','), '' if n == 1 else 's')
    for tail in (' WhatsApp, call, hours and directions.', ' WhatsApp, call and directions.', ' WhatsApp or call.'):
        d = '%s: car workshop in %s, Singapore.%s%s' % (e['name'], est, rt, tail)
        if len(d) <= 160:
            return d
    return ('%s: car workshop in %s.%s WhatsApp.' % (e['name'], est, rt))[:160]


# ---------------------------------------------------------------------------------------------------------------------------------
# TEMPLATE SYSTEM (Edwin 3 Nov 2026). Base layout = page(). A workshop page is a stack of block templates defined ONCE below.
# Order comes from the workshop's own data file (`blocks`) or the tier default in settings.json. A block with no data returns '' and is skipped.
# ---------------------------------------------------------------------------------------------------------------------------------
class X:
    """Everything a block needs about one workshop page."""
    def __init__(s, e, pl=None):
        s.e, s.pl, s.depth = e, pl or {}, 2
        s.c = CAT[e['category']]
        s.path = 'workshops/%s/' % e['slug']
        s.g = GCACHE.get(e['slug']) or {}


def blk(name, html):
    """Wrap a block's markup; empty markup means the block is skipped, never shown empty."""
    return '<div class="blk" data-block="%s">%s</div>' % (name, html) if html and re.sub(r'<[^>]+>|\s', '', html) else ''


def render_blocks(x, registry):
    order = x.e.get('blocks') or SETTINGS['block_order'][x.e['tier'] if x.e['tier'] in SETTINGS['block_order'] else 'free']
    return '\n'.join(blk(n, registry[n](x)) for n in order)


def b_hero(x):
    e, pl, c = x.e, x.pl, x.c
    chips = ''.join('<li>%s</li>' % E(t) for t in pl['chips'])
    return (f'''<header class="pl-head"><div class="badges"><span class="tag">{E(c['short'])}</span>{tier_badge(e)}{('<span class="claimed-badge">Claimed by the owner</span>' if e['slug'] in CLAIMED else '')}</div>
<h1>{E(e['name'])}</h1>
<p class="meta rg">{ic('pin')}<span>{E(region_label(e))}</span></p>
{rating_line(e)}
<ul class="pl-chips" aria-label="Main work">{chips}</ul></header>
<p class="lede" style="font-size:1rem">{E(pl['lede'])}</p>''')


def b_contact(x):
    e = x.e
    return ('<div class="acts main-acts">%s</div><p class="fine">Buttons use the mobile number on its Google listing. They only open a chat or call that you start.</p>%s'
            % (contact_btns(e, x.path, 'big'), tap_line(e)))


def tag_list(e):
    """Specialties and brands for one workshop, from the shared tag list. Tags with a guide link to it."""
    out = []
    for tid in e.get('tags', []):
        t = _tags.BY_ID[tid]
        if t['kind'] not in ('service', 'brand'):
            continue
        g = next((g for g in _guides.GUIDES if g['slug'] == t['guide']), None) if t['guide'] else None
        out.append('<li><a href="../../%s">%s</a></li>' % (_guides.gpath(g), E(t['label'])) if g else '<li>%s</li>' % E(t['label']))
    return out


def b_services(x):
    pl = x.pl
    grid_ = ''.join('<li><span class="si">%s</span><span>%s</span></li>' % (ic(pilot_icon(s)), E(s)) for s in pl.get('services', []))
    tl = tag_list(x.e)
    tags = ('<h3 class="mh">Specialties and brands customers mention</h3><ul class="tick svc-plain">%s</ul>' % ''.join(tl)) if tl else ''
    return ('<section class="pl-sec"><h2>Services</h2><ul class="svc-grid">%s</ul>%s%s</section>' % (grid_, mention_html(pl), tags)) if grid_ else ''


def b_good_for(x):
    pl = x.pl
    good = ''.join('<li>%s</li>' % E(t) for t in pl.get('good_for', []))
    return ('<section class="pl-sec"><h2>Good for</h2><ul class="tick svc-plain">%s</ul>%s</section>' % (good, ('<p class="fine">%s</p>' % E(pl['good_for_note'])) if pl.get('good_for_note') else '')) if good else ''


def b_problems(x):
    gl = guides_for(x.e)
    return ('<section class="pl-sec"><h2>Problems and brands we have a guide for</h2><ul class="tick svc-plain">%s</ul></section>'
            % ''.join('<li><a href="../../%s">%s</a></li>' % (_guides.gpath(g), E(g['h1'])) for g in gl[:4])) if gl else ''


def b_pricing(x):
    e = x.e
    return ('<section class="pl-sec"><h2>Pricing</h2><p class="fine">%s</p></section>' % E(e['price_note'])) if e.get('price_note') else ''


def b_reviews(x):
    """No Google review text, no reviewer names. Our own themes, the rating is in the hero, a link to the Google Maps reviews, owner testimonials used with permission."""
    e, pl, g = x.e, x.pl, x.g
    rows = []
    if pl.get('themes'):
        rows.append('<p>%s</p>' % E(pl['themes']))
    for t in e.get('testimonials') or []:
        rows.append('<blockquote class="rv-owner"><p>%s</p></blockquote><p class="fine">Shared by the workshop with the customer\'s permission.</p>' % E(t['text']))
    if not (g.get('rating') and g.get('userRatingCount')) and not rows:
        return ''
    link = '<p><a href="%s" target="_blank" rel="noopener" data-cta="gr_%s">See Google reviews</a></p>' % (E(gm_url(e)), e['slug']) if e.get('place_id') else ''
    return '<section class="pl-sec pl-google" id="reviews"><h2>What customers say</h2>%s%s<p class="fine">Review themes are summarised in our own words from <span translate="no">Google Maps</span>. We do not copy review text.</p></section>' % (''.join(rows), link)


def b_comparison(x):
    c_ = compare_html(x.e)
    return ('<section class="pl-sec pl-google" id="compare">%s</section>' % c_) if c_ else ''


def b_hours(x):
    e, g = x.e, x.g
    clean = lambda t: t.replace('\u202f', ' ').replace('\u2009', ' ')
    rows = []
    hrs = g.get('weekdayDescriptions') or []
    if hrs:
        rows.append('<h3>Opening hours</h3><ul class="hrs-list">%s</ul>' % ''.join('<li>%s</li>' % E(clean(h)) for h in hrs))
    po = g.get('paymentOptions') or {}
    pay = [n for k, n in (('acceptsCreditCards', 'credit cards'), ('acceptsDebitCards', 'debit cards'), ('acceptsNfc', 'contactless')) if po.get(k)]
    if pay:
        rows.append('<p><b>Payment:</b> %s.</p>' % E(', '.join(pay)))
    pk = g.get('parkingOptions') or {}
    park = [n for k, n in (('freeParkingLot', 'free parking lot'), ('paidParkingLot', 'paid parking lot'), ('freeGarageParking', 'free garage parking'), ('paidGarageParking', 'paid garage parking'), ('freeStreetParking', 'free street parking'), ('paidStreetParking', 'paid street parking')) if pk.get(k)]
    if park:
        rows.append('<p><b>Parking:</b> %s.</p>' % E(', '.join(park)))
    w = g.get('websiteUri')
    if w:
        rows.append('<p><a href="%s" rel="nofollow noopener noreferrer" target="_blank" data-cta="site_%s">Workshop website</a></p>' % (E(w.split('?')[0], True), e['slug']))
    return ('<section class="pl-sec pl-google" id="hours"><h2>Hours and practical details</h2>%s<p class="gattr">From <span translate="no">Google Maps</span>, checked %s.</p></section>'
            % (''.join(rows), E(g['fetched_at']))) if rows else ''


def b_stories(x):
    stories = x.pl.get('stories') or []
    return ('<section class="pl-sec" id="jobs"><h2>Recent jobs</h2><p class="fine">Summarised in our own words from the workshop\'s own published job write-ups. Open the original for the full post.</p>' + ''.join(
        '<article class="story"><h3>%s</h3><p>%s</p><p><a href="%s" rel="noopener noreferrer" target="_blank" data-cta="story_%s">Read the original post</a></p></article>' % (E(s['title']), E(s['text']), E(s['url'], True), x.e['slug'])
        for s in stories[:2]) + '</section>') if stories else ''


def b_location(x):
    e, pl = x.e, x.pl
    embed = ('<div class="mapembed"><iframe src="%s" title="Map of %s" width="100%%" height="300" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
             % (E(embed_url(e)), E(e['name'], True)))
    mrt = ('<li>%s<span><b>Getting there:</b> %s</span></li>' % (ic('pin'), E(pl['mrt']))) if pl.get('mrt') else ''
    return (f'''<section id="find" class="pl-sec findus"><h2>Location and directions</h2>
<ul class="facts"><li data-addr>{ic('pin')}<span>{E(e['address_public'])}</span></li>{mrt}<li>{ic('pin')}<span><b>Opening hours:</b> {'listed above from Google Maps; ' if e['slug'] in GCACHE else ''}see Google Maps for current hours.</span></li></ul>
{embed}
<p class="acts" style="margin:10px 0">{dir_btn(e, x.path)} {gm_btn(e, x.path, 'big alt')}</p>
<p class="fine">{E(e['area_ctx'])}</p>
</section>
{more_in(e, x.depth)}''')


def b_tips(x):
    t = x.pl.get('tips')
    return ('<section class="pl-sec"><h2>Before you go</h2><p class="fine">General guidance, not claims about this workshop.</p><ul class="tick svc-plain">%s</ul></section>' % ''.join('<li>%s</li>' % E(i) for i in t)) if t else ''


def b_faq(x):
    faqs = x.faqs
    return ('<section class="pl-sec" id="faqs"><h2>Questions</h2>' + ''.join('<details class="pq"><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs) + '</section>') if faqs else ''


def b_claim(x):
    e, depth, path = x.e, x.depth, x.path
    if e['tier'] == 'free':
        return ('<section class="pl-sec claimbox"><h2>Is this your workshop? Claim this free listing</h2><p>Claiming is free. Keep the details right, add your own photos, services and brands, and see how many drivers tapped WhatsApp and Call. You message Page One from the claim page; we check that you run the business first. Basic listings are built from public sources and can be removed on request.</p>'
                '<p><a class="btn amber" href="%slist-your-workshop/?w=%s#claim" data-cta="claim_%s" data-page="%s">Claim this free listing</a> <a class="rm" href="%slist-your-workshop/?w=%s#remove" data-cta="remove_%s" data-page="%s">Remove my listing</a></p></section>'
                % (pre(depth), e['slug'], e['slug'], E(page_label(path)), pre(depth), e['slug'], e['slug'], E(page_label(path))))
    return ('<section class="pl-sec claimbox"><h2>Owner of this listing?</h2><p>To correct a detail or ask for this listing to be changed or removed, <a class="rm" href="%slist-your-workshop/?w=%s#remove" data-cta="remove_%s" data-page="%s">contact us</a>.</p></section>'
            % (pre(depth), e['slug'], e['slug'], E(page_label(path))))


def b_sources(x):
    e, pl, g = x.e, x.pl, x.g
    src = pl.get('sources')
    parts = []
    if src:
        parts.append('Compiled from %s%s.' % (E(src), '' if 'Google Maps listing' in src else ' and its Google Maps listing'))
    if g.get('fetched_at'):
        parts.append('Google Maps details checked %s.' % E(g['fetched_at']))
    if e.get('note') and e['tier'] != 'free':
        parts.append(E(e['note']))
    parts.append('Last updated %s. Please confirm details with the workshop before you visit.' % UPDATED)
    c = x.c
    return '<p class="fine srcs">%s</p><p class="fine">More <a href="../../services/%s/">%s</a>%s.</p>' % (' '.join(parts), c['slug'], E(c['name'].lower()), area_link_html(e, '../../'))


FREE_BLOCKS = dict(hero=b_hero, contact=b_contact, services=b_services, good_for=b_good_for, problems=b_problems, pricing=b_pricing, reviews=b_reviews,
                   comparison=b_comparison, hours=b_hours, stories=b_stories, location=b_location, tips=b_tips, faq=b_faq, claim=b_claim, sources=b_sources)


def pilot_page(e, pl):
    """Basic workshop page: block stack (see TEMPLATE SYSTEM above). Own wording from data/pilot/<slug>.json; phone = stored Google mobile only."""
    x = X(e, pl)
    path, url = x.path, abs_url(x.path)
    cr, crld = crumbs(x.depth, workshop_trail(e))
    x.faqs = fact_faqs(e, pl)
    body = '<div class="w nar basicpg pilot">%s\n%s\n</div>' % (cr, render_blocks(x, FREE_BLOCKS))
    _m = re.search(r'^(.*?)[, ]+(?:Singapore\s+)?(\d{6})\s*$', e['address_public'])
    street, postal = (_m.group(1), _m.group(2)) if _m else (e['address_public'], '')
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', 'name': e['name'], 'url': url,
          'description': pl['lede'],
          'address': {'@type': 'PostalAddress', 'streetAddress': street, 'postalCode': postal, 'addressLocality': 'Singapore', 'addressCountry': 'SG'},
          'geo': {'@type': 'GeoCoordinates', 'latitude': e['lat'], 'longitude': e['lon']}, 'telephone': tel_of(e), 'hasMap': gm_url(e),
          'areaServed': {'@type': 'Place', 'name': ESTATES[e['estate']]['name'] + ', Singapore'}}
    _hs = hours_ld(e)
    if _hs:
        ld['openingHoursSpecification'] = _hs   # times exactly as on its Google Maps listing; no aggregateRating (the rating is Google's, not collected here)
    bar = wabar([wa_btn(e, path), call_btn(e, path)])
    page(path, card_title(e), card_desc(e), body,
         [ld, faq_ld(x.faqs), dict(crld, **{'@context': 'https://schema.org'})], bar=bar, h1=e['name'])


def paid_btns(x):
    """WhatsApp, Call and secondary buttons for a Verified or Premium page."""
    e, path = x.e, x.path
    wa, call = wa_btn(e, path, 'big'), call_btn(e, path, 'big', 'Call ' + e['phone_show'])
    wa = wa.replace('WhatsApp</a>', 'WhatsApp %s</a>' % e.get('whatsapp_show', e['phone_show']))
    sec = []
    if x.lead:
        sec.append('<a class="btn amber" href="%s" target="_blank" rel="noopener" data-cta="visit_%s" data-tier="%s" data-page="%s">Visit %s for full details %s</a>' % (
            E(e['url']), e['slug'], e['tier'], E(page_label(path)), E(e['domain']), ic('out')))
    if e.get('book_url'):
        sec.append('<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="book_%s">%s</a>' % (E(e['book_url']), e['slug'], E(e['book_label'])))
    sec.append('<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="map_%s" data-map>%s %s</a>' % (E(e['map_url']), e['slug'], ic('pin'), E(e.get('map_label', 'Open in Google Maps'))))
    return wa, call, sec


def pb_hero(x):
    e = x.e
    photos = e.get('photos') or []
    hero = '<div class="hero-ph">%s</div>' % (photo_img(photos[0], x.depth, lazy=False) if photos else tile(e))
    return (f'''<div class="badges" style="margin-top:14px">{tier_badge(e)}<span class="tag">{E(x.c['short'])}</span></div>
<h1 style="margin-top:8px">{E(e['name'])}</h1>
<p class="meta">{E(e['area_label'])}</p>
{rating_line(e)}
<p class="lede" style="font-size:1rem">{E(e['lede'])}</p>''') + '\n' + hero


def pb_contact(x):
    wa, call, sec = paid_btns(x)
    return '<div class="acts main-acts">%s%s</div><div class="acts sec-acts">%s</div>' % (wa, call, ''.join(sec))


def pb_services(x):
    e = x.e
    svcs = ''.join('<li class="svc rv"><b>%s</b><span>%s</span>%s</li>' % (E(s['n']), E(s['d']), ('<em class="pr">%s</em>' % E(s['p'])) if s.get('p') else '') for s in e['services'])
    tl = tag_list(e)
    return ('<h2>Services</h2><ul class="svcs">%s</ul>' % svcs) if svcs else ''


def pb_photos(x):
    e, depth = x.e, x.depth
    photos = e.get('photos') or []
    gal = ''
    if photos and len(photos) > 1:
        gal = '<h2>Recent work</h2><div class="gal">%s</div>' % ''.join(
            '<figure class="rv job">%s<figcaption>%s</figcaption></figure>' % (photo_img(p, depth, lazy=False), E(p['cap'])) for p in photos[1:])
    if e.get('illustrations'):
        gal += '<h2>Parts range</h2><div class="gal">%s</div>' % ''.join(
            '<figure class="rv illus">%s<figcaption>%s</figcaption></figure>' % (photo_img(p, depth, lazy=False), E(p['cap'])) for p in e['illustrations'])
    return gal


def pb_details(x):
    extra = ''
    for h, kind, items in x.e.get('sections', []):
        extra += '<h2>%s</h2>' % E(h) + (('<ul class="tick">%s</ul>' % ''.join('<li>%s</li>' % E(i) for i in items)) if kind == 'ul' else ''.join('<p>%s</p>' % E(i) for i in items))
    return extra


def pb_reviews(x):
    e = x.e
    rv = e.get('reviews')
    return ('<h2>Reviews</h2><p class="reviews-line">%s <span>%s</span> <a href="%s" target="_blank" rel="noopener" data-cta="reviews_%s">%s</a></p>' % (
        ic('shield'), E(rv['text']), E(rv['url']), e['slug'], E(rv['label']))) if rv else ''


def pb_location(x):
    e = x.e
    adds = ''.join('<li data-addr>%s<span>%s%s%s</span></li>' % (
        ic('pin'), ('<b>%s</b><br>' % E(a['label'])) if a.get('label') else '', E(a['street']),
        (', Singapore ' + a['postal']) if a.get('postal') else ', Singapore') for a in e.get('addresses', []))
    if e.get('service_area') and not adds:
        adds = '<li data-addr>%s<span>%s</span></li>' % (ic('pin'), E(e['service_area']))
    elif e.get('service_area'):
        adds += '<li>%s<span>%s</span></li>' % (ic('pin'), E(e['service_area']))
    if e.get('addresses') and e['addresses'][0].get('note'):
        adds += '<li>%s<span>%s</span></li>' % (ic('shield'), E(e['addresses'][0]['note']))
    contact = '<li>%s<span>Call %s or WhatsApp %s</span></li>' % (ic('phone'), e['phone_show'], e.get('whatsapp_show', e['phone_show']))
    return '<section id="find" class="findus"><h2>%s</h2><ul class="facts">%s%s</ul></section>%s' % (E(e.get('addr_heading', 'Find us')), adds, contact, more_in(e, x.depth))


def pb_hours(x):
    e = x.e
    hours = ''
    if e.get('hours'):
        hours = '<h3>Opening hours</h3><dl class="hours">%s</dl>' % ''.join('<dt>%s</dt><dd>%s</dd>' % (E(a), E(b)) for a, b in e['hours'])
    if e.get('hours_note'):
        hours += '<p class="fine">%s</p>' % E(e['hours_note'])
    return hours


def pb_faq(x):
    return ('<h2>Questions</h2><div class="faqs">%s</div>' % ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in x.e['faqs'])) if x.e.get('faqs') else ''


def pb_ask(x):
    e = x.e
    wa, call, sec = paid_btns(x)
    return ('<div class="cta rv" style="margin-top:26px"><div><h2>Ask %s</h2><p>Message on WhatsApp or call. Say you found them on %s.</p></div><div class="acts">%s%s</div></div>%s'
            % (E(e['name']), E(SITE_NAME), wa, call, ('<div class="acts sec-acts" style="margin-top:12px">%s</div>' % sec[0]) if x.lead else ''))


PAID_BLOCKS = dict(hero=pb_hero, contact=pb_contact, services=pb_services, pricing=b_pricing, photos=pb_photos, details=pb_details, problems=b_problems,
                   reviews=pb_reviews, hours=pb_hours, location=pb_location, faq=pb_faq, ask=pb_ask, claim=b_claim, sources=b_sources)


def listing(e):
    """Verified and Premium page: the same block stack as every page (TEMPLATE SYSTEM), with the paid blocks. The lead-gen tier adds the website button."""
    x = X(e)
    x.lead = e['tier'] in ('premium_leadgen', 'none')
    path = x.path
    url = abs_url(path)
    cr, crld = crumbs(x.depth, workshop_trail(e))
    photos = e.get('photos') or []
    body = '<div class="w nar prem">%s\n%s\n</div>' % (cr, render_blocks(x, PAID_BLOCKS))
    wa, call, _sec = paid_btns(x)
    bar = wabar([wa_btn(e, path), call_btn(e, path)])
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in e['faqs']]}
    ld = [ld_business(e, url), faq_ld, dict(crld, **{'@context': 'https://schema.org'})]
    _ph = next((p for p in photos if not (p.get('f') or '').endswith('.svg')), None)   # social preview must be a raster picture
    og = e.get('og_img') or ((_ph.get('f') or _ph.get('u')) if _ph else None)
    page(path, e['title'], e['desc'], body, ld, og=og, bar=bar, h1=e['name'])


def basic_page(e):
    if e['slug'] in PILOT:
        return pilot_page(e, PILOT[e['slug']])
    """Basic (free) profile page, built entirely from the workshop record. Lazy Google Maps embed, WhatsApp + Call from the number the workshop
    publishes itself, Directions, a link to its Google Maps listing, on-click opening hours (Google, text attribution) and the owner claim/remove box.
    No gallery, FAQs, prices, ratings or reviews."""
    depth = 2
    c = CAT[e['category']]
    path = 'workshops/%s/' % e['slug']
    url = abs_url(path)
    cr, crld = crumbs(depth, workshop_trail(e))
    embed = ('<div class="mapembed"><iframe src="%s" title="Map of %s" width="100%%" height="300" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
             % (E(embed_url(e)), E(e['name'], True)))
    contact_btn = contact_btns(e, path, 'big') + gm_btn(e, path, 'big alt')
    svcs = ''.join('<li>%s</li>' % E(s) for s in e['services_public'])
    claim = owner_note(e, depth, path)
    area_links = area_link_html(e, '../../')
    own_links = ' &middot; '.join('<a href="%s" target="_blank" rel="nofollow noopener">%s</a>' % (E(u), E(t)) for u, t in
                        ((e.get('website_url'), 'Website'), (e.get('facebook_url'), 'Facebook'), (e.get('instagram_url'), 'Instagram')) if u)
    own_hours = ('<li data-hours>%s<span><b>Opening hours:</b> %s <small>(from the workshop\'s website)</small></span></li>' % (ic('pin'), E(e['hours']))) if e.get('hours') else ''
    hours_box = ('<div class="hoursbox" data-pid="%s" data-key="%s" data-slug="%s" data-page="%s"><button type="button" class="btn sm" data-cta="hours_%s" data-tier="free" data-page="%s">Show opening hours</button>'
                 '<div class="hrs" hidden aria-live="polite"></div><p class="gattr">Opening hours from <span translate="no">Google Maps</span></p></div>'
                 % (e['place_id'], PLACES_BROWSER_KEY, e['slug'], E(page_label(path)), e['slug'], E(page_label(path))))
    body = f'''<div class="w nar basicpg">{cr}
<div class="badges" style="margin-top:14px">{tier_badge(e)}<span class="tag">{E(c['short'])}</span></div>
<h1 style="margin-top:8px">{E(e['name'])}</h1>
<p class="meta rg">{ic('pin')}<span>{E(region_label(e))}</span></p>
{embed}
<p class="lede" style="font-size:1rem">{E(e['lede'])}</p>
<p>{E(e['area_ctx'])}</p>
<div class="acts main-acts">{contact_btn}</div>
<p class="fine">The WhatsApp and call buttons use the mobile number on the workshop's Google Business Profile. They only open a chat or call that you start; we never message workshops for you. Photos and reviews are on its Google Maps listing.</p>
<h2>Services</h2>
<ul class="tick svc-plain">{svcs}</ul>
<p class="fine">{'Typical services for this type of workshop; ask the workshop for details.' if e['services_source'] == 'google_profile' else "From the workshop's own website."}</p>
<section id="find" class="findus"><h2>Find us</h2>
<ul class="facts"><li data-addr>{ic('pin')}<span>{E(e['address_public'])}</span></li>{own_hours}</ul>
{hours_box}
<p style="margin:10px 0">{dir_btn(e, path)}</p>
{('<p class="fine">Workshop\'s own pages: ' + own_links + '</p>') if own_links else ''}
</section>
<p class="fine">More <a href="../../services/{c['slug']}/">{E(c['name'].lower())}</a>{area_links}.</p>
{claim}
</div>'''
    _m = re.search(r'^(.*?)[, ]+(?:Singapore\s+)?(\d{6})\s*$', e['address_public'])
    street, postal = (_m.group(1), _m.group(2)) if _m else (e['address_public'], '')
    same = [u for u in (e.get('website_url'), e.get('facebook_url'), e.get('instagram_url')) if u]
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', 'name': e['name'], 'url': url,
          'address': {'@type': 'PostalAddress', 'streetAddress': street, 'postalCode': postal, 'addressLocality': 'Singapore', 'addressCountry': 'SG'},
          'geo': {'@type': 'GeoCoordinates', 'latitude': e['lat'], 'longitude': e['lon']}, 'telephone': tel_of(e), 'hasMap': gm_url(e)}
    if same:
        ld['sameAs'] = same
    bar = wabar([wa_btn(e, path), call_btn(e, path)])
    desc = '%s: car workshop in %s, %s region. Address, WhatsApp and call, with links to its own pages and Google Maps.' % (e['name'], e['area_label'], RN[e['region']])
    desc = desc if len(desc) <= 160 else '%s, car workshop in %s. Address, WhatsApp, call and Directions.' % (e['name'], e['area_label'])
    page(path, fit_title('%s | %s Car Workshop' % (e['name'], e['area_label']), '%s | %s' % (e['name'], e['area_label']), e['name']), desc, body, [ld, dict(crld, **{'@context': 'https://schema.org'})], bar=bar, h1=e['name'], extra_js=True)


import guides as _guides


def guide_matches(g):
    """Live Basic workshops whose 'customers mention' services match this guide, grouped by estate: {estate: [(entry, [matched mentions])]}."""
    out = {}
    rx = re.compile(g['match'], re.I)
    for e in ENTRIES:
        if e['tier'] != 'free':
            continue
        ms = [m for m in ((PILOT.get(e['slug']) or {}).get('mentioned_services') or []) if rx.search(m)]
        if ms:
            out.setdefault(e['estate'], []).append((e, ms))
    return out


def guide_page(g):
    depth = 2
    path = _guides.gpath(g)
    cr, crld = crumbs(depth, [('Guides', 'guides/'), (g['short'], None)])
    causes = ''.join('<li><h3>%s</h3><p>%s</p></li>' % (E(h), E(t)) for h, t in g['causes'])
    tell = ''.join('<li>%s</li>' % E(x) for x in g['tell'])
    gm = guide_matches(g)
    if gm:
        blocks = []
        for est, items in sorted(gm.items(), key=lambda kv: ESTATES[kv[0]]['name']):
            lis = ''.join('<li class="gw"><div><a href="../../workshops/%s/"><b>%s</b></a>%s<p class="mentline"><b>Customers mention:</b> %s</p></div><div class="acts">%s</div></li>'
                          % (e['slug'], E(e['name']), ' <span class="claimed-badge">Claimed by the owner</span>' if e['slug'] in CLAIMED else '', E(', '.join(ms)), contact_btns(e, path, 'sm')) for e, ms in sorted(items, key=lambda x: x[0]['name']))
            blocks.append('<h3 class="gest"><a href="../../areas/%s/">%s</a></h3><ul class="gwl">%s</ul>' % (est, E(ESTATES[est]['name']), lis))
        wk = ('<p class="fine">Matched from what customers mention on Google Maps, in our own words. This is not an endorsement, and a workshop has to inspect the car to confirm any cause.</p>' + ''.join(blocks))
    else:
        wk = '<p>No listed workshop has a matching customer mention yet. Browse <a href="../../services/general-servicing-repair/">all servicing and repair workshops</a>.</p>'
    cat_links = ' &middot; '.join('<a href="../../services/%s/">%s</a>' % (c, E(CAT[c]['short'])) for c in g['cats'] if c in CAT)
    others = ''.join('<li><a href="../../%s">%s</a></li>' % (_guides.gpath(o), E(o['short'])) for o in _guides.GUIDES if o['slug'] != g['slug'])
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in g['faqs'])
    heading = 'Likely causes' if g['kind'] == 'problem' else 'What to know and ask'
    body = f'''<div class="w nar guidepg">{cr}
<h1 style="margin-top:14px">{E(g['h1'])}</h1>
<p class="lede" style="font-size:1rem">{E(g['lede'])}</p>
<p class="fine">General guide in plain words. It is not a diagnosis and gives no prices: only a workshop that inspects your car can say what is wrong.</p>
<h2>{E(heading)}</h2><ol class="causes">{causes}</ol>
<h2>What to tell the workshop</h2><ul class="tick svc-plain">{tell}</ul>
<div class="urgent"><b>Do not wait if:</b> {E(g['urgent'])}</div>
<h2>Workshops customers mention for this</h2>{wk}
<p class="fine">More: {cat_links}</p>
<h2>Questions</h2>{faq_html}
<h2>Other guides</h2><ul class="guide-links">{others}</ul>
</div>'''
    ld = [dict(crld, **{'@context': 'https://schema.org'}), faq_ld(g['faqs'])]
    page(path, g['title'] if len(g['title']) <= 60 else fit_title(g['title'], g['h1'], g['short']), g['desc'], body, ld, h1=g['h1'])


def guides_index():
    depth = 1
    cr, crld = crumbs(depth, [('Guides', None)])
    probs = [g for g in _guides.GUIDES if g['kind'] == 'problem']
    brands = [g for g in _guides.GUIDES if g['kind'] == 'brand']
    li = lambda gs: ''.join('<li><a href="../%s"><span><b>%s</b><small>%s</small></span></a></li>' % (_guides.gpath(g), E(g['h1']), E(g['desc'][:110].rsplit(' ', 1)[0] + '...')) for g in gs)
    body = f'''<div class="w">{cr}
<h1 style="margin-top:14px">Car problem and brand guides</h1>
<p class="lede" style="font-size:1rem;max-width:720px">Plain-word guides to common car problems and car brands, with what to tell the workshop and the workshops customers mention for each.</p>
<h2>Common problems</h2><ul class="tiles guide-tiles">{li(probs)}</ul>
<h2>By car brand</h2><ul class="tiles guide-tiles">{li(brands)}</ul>
</div>'''
    page('guides/', 'Car Problem and Brand Guides | SG Car Workshop', 'Plain-word guides to common car problems, such as knocking over humps and aircon not cold, and to car brands, with workshops customers mention.', body, [dict(crld, **{'@context': 'https://schema.org'})], h1='Car problem and brand guides')


def list_page():
    depth = 1
    cr, crld = crumbs(depth, [('Claim your free listing', None)])
    wa = E(list_wa(depth, 'general enquiry'))
    claim_generic = E(wa_link(PAGE_ONE_WA, "Hi Page One, I'm a workshop owner, about my %s listing.\n\n(From %s)" % (SITE_NAME, BASE + 'list-your-workshop/')))
    remove_generic = E(wa_link(PAGE_ONE_WA, "Hi Page One, please remove my workshop listing from %s. Business name: \n\n(From %s)" % (SITE_NAME, BASE + 'list-your-workshop/')))
    claim_names = E(json.dumps({e['slug']: e['name'] for e in ENTRIES}), True)
    claim_taps = E(json.dumps({e['slug']: (TAPS.get(e['slug']) or {}).get('whatsapp') for e in ENTRIES if e['tier'] == 'free' and ((TAPS.get(e['slug']) or {}).get('whatsapp') or 0) >= TAP_SHOW_MIN}), True)
    body = f'''<div class="w nar">{cr}
<h1 style="margin-top:14px">Claim your free workshop listing</h1>
<p class="lede" style="font-size:1rem">Claiming your listing on {E(SITE_NAME)} is <b>free</b>. Drivers already find your workshop here, with your WhatsApp and Call buttons. Claim it to run it yourself.</p>
<section class="claim-sec"><h2>What you get, free</h2>
<ul class="tick">
<li><b>A verified badge</b> once we have checked that you run the business.</li>
<li><b>Your own photos, services and brands</b> added to your page, so drivers see what you really do.</li>
<li><b>Correct hours and WhatsApp</b>, kept up to date by you.</li>
<li><b>Better matching to the right guide.</b> Your claimed details and specialties help drivers match you to the right <a href="../guides/">car problem or brand guide</a>. There is no order advantage: guides list workshops A to Z.</li>
<li><b>An open count of drivers who tapped WhatsApp and Call</b> through {E(SITE_NAME)}. We show your total WhatsApp tap count, all-time and never reset, on your card and in the estate list, like "12 drivers have WhatsApped this workshop via {E(SITE_NAME)}", once it reaches 5. Counts are anonymous and hold no personal data. We tell you your Call count too.</li>
</ul>
<p class="fine">No fee, no contract, and you can ask us to remove your listing at any time. We do not promise a number of enquiries.</p></section>
<section id="claim" class="claim-sec"><h2>Claim it on WhatsApp</h2>
<p>Message Page One and tell us which workshop is yours. We check that you run the business first, then make the changes you ask for.</p>
<p class="claim-for" id="claim-for" hidden>Listing: <b></b></p>
<p class="tapline" id="claim-taps" hidden></p>
<a class="btn amber big" id="claim-wa" href="{claim_generic}" data-names="{claim_names}" data-taps="{claim_taps}" data-wa="{PAGE_ONE_WA}" data-site="{E(SITE_NAME)}" target="_blank" rel="noopener" data-cta="claim_owner_page">{WA_SVG} Claim this free listing</a>
<p class="fine">This WhatsApp is for workshop owners only. Customers, please use the WhatsApp button on the workshop's own listing.</p></section>
<section><h2>Not listed yet?</h2><p>{E(SITE_NAME)} lists car workshops and car services in Singapore: repair, gearbox, ABS and ECU modules, spray painting and bodywork, batteries, detailing and coating, wraps and PPF, and parts. Message us and we will list yours, free.</p>
<p><a class="btn big" href="{wa}" target="_blank" rel="noopener" data-cta="whatsapp_list_page">{WA_SVG} WhatsApp Page One</a></p></section>
<section><h2>How listings are ordered</h2>
<p>We do not sell rankings. Claiming does not change any order, and paid Featured workshops are shown in their own labelled block, never in a ranking. How we rank, where we do, is explained on the <a href="../about/">About page</a>.</p></section>
<section id="remove" class="claim-sec"><h2>Remove my listing</h2>
<p>Basic listings are built from the workshop's public Google Business Profile and, where available, what its customers mention in Google reviews, and link to its Google Maps listing. They are not endorsed by or arranged with the business. If you run a workshop and want your listing taken down, send us a message and we will remove it. We check that you run the business first.</p>
<p class="claim-for" id="remove-for" hidden>Listing: <b></b></p>
<a class="btn big" id="remove-wa" href="{remove_generic}" data-names="{claim_names}" data-wa="{PAGE_ONE_WA}" data-site="{E(SITE_NAME)}" target="_blank" rel="noopener" data-cta="remove_owner_page">{WA_SVG} WhatsApp to remove my listing</a>
<p class="fine">This WhatsApp is for workshop owners only. You start the chat; we never message workshops first.</p></section>
</div>'''
    page('list-your-workshop/', 'Claim Your Free Workshop Listing | SG Car Workshop',
         'Claiming your car workshop listing is free: a verified badge, your photos, correct hours and WhatsApp, and an open count of driver taps.',
         body, [dict(crld, **{'@context': 'https://schema.org'})])


def about_page():
    depth = 1
    cr, crld = crumbs(depth, [('About', None)])
    body = f'''<div class="w nar">{cr}
<h1 style="margin-top:14px">About {E(SITE_NAME)}</h1>
<p class="lede" style="font-size:1rem">{E(SITE_NAME)} is a directory of car workshops and car services in Singapore, run by Page One Singapore, a web and SEO service for small businesses.</p>
<h2>Where the details come from</h2>
<p>Every fact on a page comes from the business itself or from public records. If a detail cannot be confirmed, such as a price or opening hours, we leave it out. We do not copy a business's website text, and we do not sell rankings. Where a Google Maps rating is shown, it is Google's, with its date.</p>\n<h2>How we rank</h2>\n<p>Only where an estate has at least 8 workshops with 20 or more Google ratings, we rank those by this score: (v / (v + 50)) x the workshop's rating + (50 / (v + 50)) x the estate's average rating, where v is its number of Google ratings. It pulls workshops with fewer ratings toward the average, so a 4.9 from 1,145 ratings can rank above a 5.0 from 59. Everywhere else we show no rank and list workshops A to Z. Paid Featured workshops are shown in their own block and are never part of a ranking.</p>
<h2>Basic listings</h2>
<p>Basic listings are built from the workshop's public Google Business Profile and, where available, what its customers mention in Google reviews, and link to its Google Maps listing. They are not endorsed by or arranged with the business. They are free and can be removed on request: use <a href="../list-your-workshop/#remove">Remove my listing</a>. Verified and Premium listings are for businesses that signed up and supplied their own details.</p>
<h2>Who we list</h2>
<p>Car workshops and car services only: repair and servicing, gearbox, ABS and ECU modules, spray painting and bodywork, batteries, detailing and coating, wraps and PPF, and parts. Car dealers and insurance are not listed.</p>
<h2>A note on one listing</h2>
<p>SG Garage (aircon repair, unit #01-309) and Edwin Garage (car repair and accident work, unit #01-295) are both owned by the founder of {E(SITE_NAME)}. They are in different units in Ang Mo Kio Industrial Park 2. They appear in the normal A to Z lists with an "Owned by the site's founder" label, are never in the Featured (paid) block, and get no boost in ordering.</p>
<h2>Contact</h2>
<p>Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W). To list a workshop or correct a page, WhatsApp {PAGE_ONE_WA_SHOW}.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn wa big" href="{E(list_wa(depth, 'general enquiry'))}" target="_blank" rel="noopener" data-cta="whatsapp_about">{WA_SVG} WhatsApp {PAGE_ONE_WA_SHOW}</a>
<a class="btn big" href="../list-your-workshop/">How listing works</a></div>
</div>'''
    page('about/', 'About SG Car Workshop | Run by Page One Singapore',
         'SG Car Workshop is a Singapore car workshop directory run by Page One Singapore. Contact us on WhatsApp.',
         body, [dict(crld, **{'@context': 'https://schema.org'}), {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About ' + SITE_NAME, 'url': abs_url('about/')}])


def legal_page(path, title, desc, h1, body_html):
    depth = 1
    cr, crld = crumbs(depth, [(h1, None)])
    body = '<div class="w nar">%s<h1 style="margin-top:14px">%s</h1>%s</div>' % (cr, E(h1), body_html)
    page(path, title, desc, body, [dict(crld, **{'@context': 'https://schema.org'})], h1=h1)


GOOGLE_TERMS = 'https://maps.google.com/help/terms_maps/'
GOOGLE_PRIVACY = 'https://policies.google.com/privacy'


def terms_page():
    legal_page('terms/', 'Terms | SG Car Workshop', 'Terms for using SG Car Workshop, a Singapore car workshop directory run by Page One Singapore.', 'Terms',
               ('<p class="lede" style="font-size:1rem">By using %s you agree to these terms.</p>'
                '<h2>What this site is</h2><p>%s lists car workshops and car services in Singapore. Basic listings are built from the workshop\'s public Google Business Profile and, where available, what its customers mention in Google reviews, and link to its Google Maps listing. They are not endorsed by or arranged with the business. Premium workshops are marked Featured (paid).</p>'
                '<h2>Using the contact buttons</h2><p>WhatsApp and Call buttons only open a chat or call that you start. We do not send messages to workshops on your behalf. Workshops are separate businesses: agree prices and work with them directly.</p>'
                '<h2>Google Maps</h2><p>Some pages show maps, opening hours or links from Google Maps. Use of Google Maps content is subject to <a href="%s" target="_blank" rel="noopener">Google Maps Terms of Service</a>.</p>'
                '<h2>Removing a listing</h2><p>If you run a workshop and want a listing removed or corrected, use <a href="../list-your-workshop/#remove">Remove my listing</a>.</p>'
                '<h2>No promises</h2><p>We take care over the details but cannot promise that a workshop is open, available or suitable. Check with the workshop before you travel.</p>')
               % (E(SITE_NAME), E(SITE_NAME), GOOGLE_TERMS))


def privacy_page():
    legal_page('privacy/', 'Privacy | SG Car Workshop', 'How SG Car Workshop handles data: what the site collects, Google Maps content, and how to ask for a listing to be removed.', 'Privacy',
               ('<p class="lede" style="font-size:1rem">This page explains what %s collects and what it shows from other sources.</p>'
                '<h2>Listing information</h2><p>Basic workshop pages show business details from the workshop\'s public Google Business Profile, such as its name, address, opening hours and mobile number. To correct or remove a listing, use <a href="../list-your-workshop/#remove">Remove my listing</a>.</p>'
                '<h2>Taps on contact buttons</h2><p>When a live visitor taps WhatsApp, Call, Directions or a Google Maps link, we record the tap with the workshop, the page, a random visit identifier and the device type, so we can report results to the business. We do not record the message you write. Do-not-track browsers are not counted. The all-time total of WhatsApp taps for each workshop may be shown on that workshop\'s card, in the estate list and on the claim page once it reaches 5; it is a count of anonymous visits and says nothing about any person.</p>'
                '<h2>Google Maps</h2><p>Some pages load a Google Maps embed, and the Show opening hours button asks Google Maps for opening hours when you press it. Google handles that data under its <a href="%s" target="_blank" rel="noopener">Privacy Policy</a> and the <a href="%s" target="_blank" rel="noopener">Google Maps Terms</a>. We do not store ratings, reviews, photos or phone numbers from Google.</p>'
                '<h2>Contact</h2><p>Page One Singapore (Snap Commercial Pte. Ltd., UEN 202209904W). WhatsApp %s.</p>')
               % (E(SITE_NAME), GOOGLE_PRIVACY, GOOGLE_TERMS, PAGE_ONE_WA_SHOW))


def not_found():
    b = PATH_BASE
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (b, c['slug'], E(c['name'])) for c in CATEGORIES)
    out = f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | {E(SITE_NAME)}</title><meta name="robots" content="noindex">
<link rel="icon" href="{b}assets/favicon.ico" sizes="48x48"><link rel="stylesheet" href="{b}assets/dir.css?v={V}"></head>
<body><main class="w nar" style="padding:60px 16px"><h1>That page is not here</h1><p>The page may have moved. Try the <a href="{b}">home page</a> or pick a service.</p>
<ul class="tick">{cats}</ul><p>Read <a href="{b}about/">about {E(SITE_NAME)}</a> or <a href="{b}list-your-workshop/">list your workshop</a>.</p><p><a class="btn amber" href="{b}">Back to {E(SITE_NAME)}</a></p></main></body></html>
'''
    return out


# ------------------------------------------------------------------ build
def build():
    compute_facts()
    basic_texts()
    home()
    for c in CAT_LIST:
        category(c)
    for k in PUB_REGIONS:
        region(k)
    for t in PUB_TOWNS:
        town_hub(t)
    for k, v in PUB_ESTATES.items():
        estate(k, v)
    for (k, cat), v in PUB_PAIRS.items():
        estate_service(k, cat, v)
    for e in PAID:
        listing(e)
    for e in ENTRIES:
        if e['tier'] == 'free':
            basic_page(e)
    guides_index()
    hub_indexes()
    for _g in _guides.GUIDES:
        guide_page(_g)
    list_page()
    about_page()
    terms_page()
    privacy_page()

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT + '/assets/img')
    for path, h in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)
    open(OUT + '/404.html', 'w', encoding='utf-8').write(not_found())
    write_redirects()
    for f in ('dir.css', 'dir.js', 'livephone.js', 'ask.js'):
        shutil.copy(os.path.join(HERE, f), OUT + '/assets/' + f)
    shutil.copytree(os.path.join(HERE, 'img'), OUT + '/assets/img', dirs_exist_ok=True)
    make_icons()
    folder_fillers()

    urls = sorted(PAGES)
    open(OUT + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                          ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (abs_url(p), lastmod_of(p, PAGES[p])) for p in urls if p not in NOINDEX) + '</urlset>\n')
    if LIVE:
        bots = LIVE_BOTS
        _unused = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
        robots = ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BASE
    else:
        robots = 'User-agent: *\nDisallow: /\n'
    open(OUT + '/robots.txt', 'w').write(robots)
    open(OUT + '/%s.txt' % INDEXNOW_KEY, 'w').write(INDEXNOW_KEY)
    json.dump(LM_NEW, open(LM_FILE, 'w'), indent=0, sort_keys=True)
    json.dump(dict(min_free=MIN_FREE, index_exceptions=sorted(INDEX_EXCEPTIONS), hub_cards=HUBCARDS, noindex=NOINDEX, free_count=FREECOUNT, redirects=REDIRECTS, sitemap=[p for p in urls if p not in NOINDEX]),
              open(os.path.join(HERE, '..', 'build-manifest.json'), 'w'), indent=1, sort_keys=True)
    # robots-live.txt always carries the crawlable live-domain rules; htaccess/.htaccess serves it as /robots.txt on sgcarworkshop.sg only
    live_robots = ''.join('User-agent: %s\nAllow: /\n\n' % b for b in LIVE_BOTS) + 'User-agent: *\nAllow: /\n\nSitemap: https://%s/sitemap.xml\n' % DOMAIN
    open(OUT + '/robots-live.txt', 'w').write(live_robots)
    lines = ['# %s' % SITE_NAME, '', '> A directory of car workshops and car services in Singapore, run by Page One Singapore. Entries use details from the business or its public listing. Estate pages rank workshops only where there are at least 8 with 20 or more Google ratings, by rating and number of ratings together; paid Featured workshops are never ranked. No rating or review markup.', '',
             'Last updated: %s' % max([d['d'] for d in LM_NEW.values()] or [UPDATED]), '', '## Services']
    lines += ['- [%s](%sservices/%s/): %s' % (c['name'], BASE, c['slug'], c['blurb']) for c in CATEGORIES]
    lines += ['', '## Areas (regions)']
    lines += ['- [%s](%sareas/%s/): %s' % (RN[k], BASE, k, areas.REGION_INTRO[k]) for k in PUB_REGIONS]
    lines += ['', '## Estates and industrial areas']
    lines += ['- [%s](%sareas/%s/): %s %d listing%s.' % (ESTATES[k]['name'], BASE, k, ESTATES[k]['intro'], len(v), '' if len(v) == 1 else 's') for k, v in PUB_ESTATES.items()]
    lines += ['', '## Car problem and brand guides', '- [All guides](%sguides/)' % BASE] + ['- [%s](%s%s): %s' % (g['h1'], BASE, _guides.gpath(g), g['desc']) for g in _guides.GUIDES]
    lines += ['', '## Listings']
    for e in ENTRIES:
        lines.append('- [%s](%sworkshops/%s/): %s, %s%s' % (e['name'], BASE, e['slug'], CAT[e['category']]['name'] + ', ' + TIERS[e['tier']]['label'], e['area_label'], (' (own website: %s)' % e['url']) if e['tier'] == 'premium_leadgen' else ''))
    lines += ['', '## More', '- [List your workshop](%slist-your-workshop/)' % BASE, '- [About](%sabout/)' % BASE, '- [Terms](%sterms/)' % BASE, '- [Privacy](%sprivacy/)' % BASE, '']
    open(OUT + '/llms.txt', 'w').write('\n'.join(lines))
    print('built %d pages + 404 into %s (LIVE=%s, v=%s)' % (len(PAGES), OUT, LIVE, V))


OLD_REGIONS = ['north', 'north-east', 'east', 'west', 'central']


def redirect_map():
    """old path -> new path, every one a single hop (Edwin 3 Nov 2026). Targets must be real pages."""
    r = {}
    for old, new in json.load(open(os.path.join(HERE, '..', 'data', 'slug_redirects.json'))).items():
        r['workshops/%s/' % old] = 'workshops/%s/' % new
    for g in _guides.GUIDES:
        if g.get('kind') == 'brand':
            r['guides/%s/' % g['slug']] = _guides.gpath(g)
    for t in TOWNS:    # old town-level pages /areas/<town>/<service>/ (only general servicing existed) -> the estate, or the town hub when it has several
        old_pair = 'areas/%s/general-servicing-repair/' % t
        if t in PUB_TOWNS:
            ests = PUB_TOWNS[t]
            r[old_pair] = 'areas/%s/' % (ests[0] if len(ests) == 1 else t)
    r['areas/kranji/'] = 'areas/carros-centre-jalan-lam-huat/'   # the old Kranji page held the Jalan Lam Huat workshops
    for reg in OLD_REGIONS:
        if reg in PUB_REGIONS:
            r['regions/%s/' % reg] = 'areas/%s/' % reg
    r['regions/'] = ''
    for old, new in r.items():
        assert old not in PAGES, ('redirect source is a live page', old)
        assert new == '' or new in PAGES, ('redirect target missing', old, new)
    return r


REDIRECTS = {}


def write_redirects():
    """Soft redirect pages (meta refresh + canonical) for every old URL, because the upload bridge cannot send .htaccess.
    proposed.htaccess holds the real one-hop 301 and 410 rules, Options -Indexes included, for the publisher to pin and upload."""
    global REDIRECTS
    REDIRECTS = redirect_map()
    for old, new in REDIRECTS.items():
        d = os.path.join(OUT, old)
        os.makedirs(d, exist_ok=True)
        rel = '../' * old.count('/') + new
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
            '<!doctype html>\n<html lang="en-SG"><head><meta charset="utf-8"><title>Moved | %s</title><meta name="robots" content="noindex">'
            '<link rel="canonical" href="%s"><meta http-equiv="refresh" content="0; url=%s"></head>'
            '<body><p>This page has moved to <a href="%s">%s</a>.</p></body></html>\n' % (E(SITE_NAME), E(abs_url(new)), rel or './', rel or './', E(abs_url(new))))
    gone = []
    try:
        import registry as _reg
        gone = sorted({x['slug'] for x in _reg.load() if x.get('status') in ('removed-on-request', 'closed') and x.get('slug')})
    except Exception:
        pass
    for g in gone:
        assert g not in {e['slug'] for e in ENTRIES}, ('removed slug reused', g)
    rules = ['# Proposed .htaccess for sgcarworkshop.sg (3 Nov 2026). NOT yet pinned or uploaded: the bridge cannot send .htaccess files.',
             '# Merge with htaccess/.htaccess (keep its RewriteEngine, Inherit and robots lines), then pin and upload through the publisher.',
             'Options -Indexes', '']
    # Exact matches only (Edwin 3 Nov 2026): "Redirect 301 /regions/ /" prefix-matched /regions/north/ and sent it to the home page. ^/old/?$ also covers the no-trailing-slash URL.
    rules += ['RedirectMatch 301 ^/%s/?$ /%s' % (re.escape(o.rstrip('/')), n) for o, n in sorted(REDIRECTS.items()) if o]
    rules += ['RedirectMatch 410 ^/workshops/%s/?$' % re.escape(g) for g in gone]
    open(os.path.join(HERE, '..', 'htaccess', 'proposed.htaccess'), 'w').write('\n'.join(rules) + '\n')
    open(os.path.join(HERE, '..', 'redirects.htaccess'), 'w').write('\n'.join(r for r in rules if r.startswith(('Redirect', 'RedirectMatch'))) + '\n')


def hub_indexes():
    """Real index pages for /areas/, /services/, /workshops/ and /brands/ so no folder shows a directory listing. Navigation only: noindex, not in the sitemap."""
    depth = 1
    def shell(path, h1, lead, inner, crumb):
        cr, crld = crumbs(depth, [(crumb, None)])
        body = '<div class="w nar">%s<h1 style="margin-top:14px">%s</h1><p class="lede" style="font-size:1rem">%s</p>%s</div>' % (cr, E(h1), E(lead), inner)
        page(path, fit_title('%s | %s' % (h1, SITE_NAME), h1), cap(lead, 160), body, [dict(crld, **{'@context': 'https://schema.org'})], h1=h1, index=False, why='folder index, navigation only')
    secs = ''
    for r in PUB_REGIONS:
        lis = ''
        for t, ests in PUB_TOWNS.items():
            if TOWNS[t]['region'] != r:
                continue
            lis += '<li><a href="../areas/%s/">%s</a><ul>%s</ul></li>' % (t, E(TOWNS[t]['name']), ''.join('<li><a href="../areas/%s/">%s</a></li>' % (k, E(ESTATES[k]['name'])) for k in ests))
        secs += '<h2><a href="../areas/%s/">%s</a></h2>%s' % (r, E(RN[r]), ('<ul class="tick">%s</ul>' % lis) if lis else '')
    shell('areas/', 'Car workshop areas in Singapore', 'Regions, towns and industrial estates that have car workshops listed on %s.' % SITE_NAME, secs, 'Areas')
    shell('services/', 'Car services in Singapore', 'The kinds of car work listed on %s.' % SITE_NAME,
          '<ul class="tick">%s</ul>' % ''.join('<li><a href="../services/%s/">%s</a></li>' % (c['slug'], E(c['name'])) for c in CAT_LIST), 'Services')
    shell('brands/', 'Car brand guides', 'Plain-word guides for owners of common car brands.',
          '<ul class="tick">%s</ul>' % ''.join('<li><a href="../%s">%s</a></li>' % (_guides.gpath(g), E(g['h1'])) for g in _guides.GUIDES if g.get('kind') == 'brand'), 'Brands')
    shell('workshops/', 'All workshops A to Z', 'Every workshop listed on %s, in alphabetical order.' % SITE_NAME,
          '<ul class="tick">%s</ul>' % ''.join('<li><a href="../workshops/%s/">%s</a> <small>%s</small></li>' % (e['slug'], E(e['name']), E(e['area_label'])) for e in sorted(ENTRIES, key=lambda e: e['name'].lower())), 'Workshops')


def folder_fillers():
    """Any other folder in the built site (assets, images, ...) gets a small noindex index page, so a server never lists its files."""
    n = 0
    for d, _dirs, files in os.walk(OUT):
        if d == OUT or 'index.html' in files:
            continue
        rel = os.path.relpath(d, OUT)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
            '<!doctype html>\n<html lang="en-SG"><head><meta charset="utf-8"><title>%s</title><meta name="robots" content="noindex"></head>'
            '<body><p>This folder is not a page. <a href="%s">Go to %s</a>.</p></body></html>\n' % (E(SITE_NAME), '../' * (rel.count(os.sep) + 1), E(SITE_NAME)))
        n += 1
    return n


def make_icons():
    """Favicon, app icons and default share image, drawn with Pillow (no external files)."""
    from PIL import ImageDraw, ImageFont

    def mark(sz, bg=True):
        """Pin + hex nut mark, drawn 8x large then scaled down for smooth edges."""
        S = 8
        k = sz * S / 48.0
        im = Image.new('RGBA', (sz * S, sz * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if bg:
            d.rounded_rectangle([0, 0, sz * S - 1, sz * S - 1], radius=int(12 * k), fill='#0f1c33')
        gold, navy = '#d4a64a', '#0f1c33'
        d.ellipse([12 * k, 8 * k, 36 * k, 32 * k], fill=gold)
        d.polygon([(14.1 * k, 27.3 * k), (33.9 * k, 27.3 * k), (24 * k, 41.5 * k)], fill=gold)
        d.polygon([(24 * k, 13.2 * k), (29.9 * k, 16.6 * k), (29.9 * k, 23.4 * k), (24 * k, 26.8 * k), (18.1 * k, 23.4 * k), (18.1 * k, 16.6 * k)], fill=navy)
        d.ellipse([21.4 * k, 17.4 * k, 26.6 * k, 22.6 * k], fill=gold)
        im = im.resize((sz, sz), Image.LANCZOS)
        if bg:
            out = Image.new('RGB', (sz, sz), '#ffffff')
            out.paste(im, mask=im.split()[3])
            return out
        return im
    mark(192).save(OUT + '/assets/icon-192.png')
    mark(512).save(OUT + '/assets/icon-512.png')
    mark(180).save(OUT + '/assets/apple-touch-icon.png')
    mark(48).save(OUT + '/assets/favicon.ico', sizes=[(48, 48)])
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), '#0f1c33')
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(15 + 10 * t), int(28 + 20 * t), int(51 + 40 * t)))
    def font(bold, size):
        for f in (('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') if bold else
                  ('/usr/share/fonts/opentype/inter/Inter-Regular.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')):
            try:
                return ImageFont.truetype(f, size)
            except OSError:
                pass
        return ImageFont.load_default()
    m = mark(150, bg=False)
    im.paste(m, (80, 150), m)
    fb, fs = font(True, 76), font(False, 34)
    d.text((260, 170), 'SG', font=fb, fill='#d4a64a')
    d.text((260 + d.textlength('SG ', font=fb), 170), 'Car Workshop', font=fb, fill='white')
    d.text((262, 270), 'Singapore car workshop directory', font=fs, fill='#cdd5e6')
    d.rounded_rectangle([80, 420, 1120, 422], radius=1, fill='#2a3c5f')
    d.text((80, 455), 'Find a workshop by service and area. WhatsApp them directly.', font=font(False, 30), fill='#d4a64a')
    im.save(OUT + '/assets/img/og-default.jpg', quality=85)


if __name__ == '__main__':
    build()

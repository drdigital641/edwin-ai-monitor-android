#!/usr/bin/env python3
"""SG Car Workshop: static directory preview.  python3 build.py [outdir]   (default ../site)

Preview mode (LIVE = False): pages are published at https://pageonesingapore.com/preview/sgcarworkshop/ ; canonical, sitemap and
llms.txt name that address, robots.txt says Disallow: / . Internal links and assets are RELATIVE, so the same files work at the
preview address and on the real domain. LIVE = True switches every absolute URL to https://sgcarworkshop.sg/ and opens robots.txt.
Pages never carry a noindex tag: hiding the preview is done by a server header outside the pages (MASTER-RULES 4.3).
"""
import hashlib
import html
import json
import os
import re
import shutil
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'builder'))
from data import ENTRIES, CATEGORIES, AREAS, PAGE_ONE_WA, PAGE_ONE_WA_SHOW, TIERS, PRICE_NOTE, FREE_EXAMPLE  # noqa: E402
from PIL import Image  # noqa: E402

SITE_NAME = 'SG Car Workshop'   # placeholder brand
DOMAIN = 'sgcarworkshop.sg'     # not bought yet
LIVE = False
PREVIEW_BASE = 'https://pageonesingapore.com/preview/sgcarworkshop/'
BASE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW_BASE
PATH_BASE = '/' if LIVE else '/preview/sgcarworkshop/'
UPDATED = '2026-11-01'
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site'))
E = html.escape
CAT = {c['slug']: c for c in CATEGORIES}
ENT = {e['slug']: e for e in ENTRIES}

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
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'out': '<path d="M7 17L17 7M8 7h9v9"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
}


def ic(k, cls=''):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (
        (' class="%s"' % cls) if cls else '', ICONS[k])


WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 '
          '8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 '
          '5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')
LOGO = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#12306b"/><path d="M8 29c3-1 4-5 8-7l8-2c5 0 9 3 12 6l4 1v4H8z" fill="#fff"/>'
        '<circle cx="16" cy="33" r="4" fill="#12306b" stroke="#fff" stroke-width="2"/><circle cx="33" cy="33" r="4" fill="#12306b" stroke="#fff" stroke-width="2"/>'
        '<path d="M6 40h36" stroke="#f5a623" stroke-width="3" stroke-dasharray="6 4" stroke-linecap="round"/></svg>')

_h = hashlib.sha1()
for _f in ('dir.css', 'dir.js'):
    _h.update(open(os.path.join(HERE, _f), 'rb').read())
V = _h.hexdigest()[:8]

PAGES = {}   # path ('' = home, 'a/b/' ...) -> html
META = {}    # path -> title (for llms/sitemap)
_imgsz = {}


def imgsize(rel):
    if rel not in _imgsz:
        _imgsz[rel] = Image.open(os.path.join(HERE, 'img', rel)).size
    return _imgsz[rel]


def img_tag(rel, alt, depth, lazy=True, cls=''):
    w, h = imgsize(rel)
    return '<img src="%sassets/img/%s" alt="%s" width="%d" height="%d"%s%s decoding="async">' % (
        pre(depth), rel, E(alt, True), w, h, ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '')


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
            '<p class="tx">Run a %s business in Singapore? Get a listing here. Message Page One on WhatsApp to ask how.</p>'
            '<div class="acts"><a class="btn sm wa" href="%s" target="_blank" rel="noopener" data-cta="whatsapp_list_%s">%s WhatsApp Page One</a>'
            '<a class="btn sm" href="%slist-your-workshop/">How it works</a></div></div></article>') % (
        ic('plus'), E(what), E(list_wa(depth, what)), re.sub(r'[^a-z0-9]+', '-', what.lower()).strip('-'), WA_SVG, pre(depth))


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
    return ('<a class="skip" href="#main">Skip to content</a><header class="top"><div class="w bar"><a class="brand" href="%s" aria-label="%s home">%s<span>%s</span></a>'
            '<nav class="main" aria-label="Main"><a href="%s#services">Services</a><a href="%s#workshops">Workshops</a><a href="%sabout/">About</a></nav>'
            '<a class="btn sm amber" href="%slist-your-workshop/">List your workshop</a></div></header>') % (p, E(SITE_NAME), LOGO, E(SITE_NAME), p, p, p, p)


def footer(depth):
    p = pre(depth)
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (p, c['slug'], E(c['name'])) for c in CATEGORIES[:5])
    return ('<footer class="ft"><div class="w cols"><div><h3>%s</h3><p>A directory of car workshops and car services in Singapore, run by '
            '<a href="https://pageonesingapore.com/" rel="noopener">Page One Singapore</a>.</p><p class="fine">Listing details are confirmed with each business. '
            'WhatsApp taps are counted and reported to the business. This is a preview and the brand name is a placeholder.</p></div>'
            '<div><h3>Services</h3><ul>%s<li><a href="%s#services">All services</a></li></ul></div>'
            '<div><h3>Directory</h3><ul><li><a href="%slist-your-workshop/">List your workshop</a></li><li><a href="%sabout/">About</a></li>'
            '<li><a href="%sllms.txt">llms.txt</a></li></ul></div></div></footer>') % (E(SITE_NAME), cats, p, p, p, p)


def wabar(items):
    return '<div class="wabar" role="region" aria-label="Contact">%s</div>' % ''.join(items)


def page(path, title, desc, body, schema=None, og=None, bar=None, h1=None):
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
    out = f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc, True)}">
<meta name="robots" content="index, follow, max-image-preview:large">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{p}assets/dir.css?v={V}">
<script>document.documentElement.className+=' js'</script>
{ld}</head>
<body{' class="has-bar"' if bar else ''}>
{header(depth)}
<main id="main">
{body}
</main>
{footer(depth)}
{bar or ''}
<script src="{p}assets/dir.js?v={V}" defer></script>
</body>
</html>
'''
    PAGES[path] = out
    META[path] = title


# ------------------------------------------------------------------ pages
def home():
    depth = 0
    featured = ''.join(card(e, 0, '') for e in ENTRIES)
    faqs = [
        ('What is %s?' % SITE_NAME, 'A small directory of car workshops and car services in Singapore. Each entry shows what the business does, where it is and how to contact it, using details confirmed by the business.'),
        ('How do I list my workshop?', 'Message Page One Singapore on WhatsApp. A Basic listing is a basic card. A Verified listing is a full page with photos, services, map, WhatsApp and Call buttons. Premium adds your own Page One website.'),
        ('How much does a listing cost?', 'A Basic listing costs nothing. The Verified listing is S$20 a month, and Premium is S$50 a month. The S$20 is not the earlier S$20 early-bird SEO plan.'),
        ('Do you rank or review workshops?', 'No. Entries are not ranked and we do not write reviews. Verified pages may show a rating line from a source people can open, with its link and the date we checked.'),
    ]
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)
    body = f'''<section class="hero"><div class="w">
<span class="eyebrow">Singapore car workshops</span>
<h1>Find a trusted car workshop in Singapore</h1>
<p class="lede">Repair, gearbox, ABS and ECU modules, spray painting, batteries, detailing, wraps and parts. Browse listings from businesses that confirmed their own details, with WhatsApp and call buttons on each card.</p>
<form class="search" role="search" action="#workshops" onsubmit="return false"><label><span class="skip">Search workshops</span>{ic('search')}<input id="q" type="search" placeholder="Search by name, service or area, e.g. gearbox, Yishun" autocomplete="off"></label></form>
{chip_row(depth)}
</div></section>
<section id="workshops"><div class="w"><h2 class="rv">Featured listings</h2>
<div class="grid">{featured}</div>
<div class="empty" id="empty"><b>No match yet.</b> Try another word, or <a href="list-your-workshop/">list your workshop</a>.</div></div></section>
<section class="alt" id="services"><div class="w"><h2 class="rv">Browse by service</h2>
<div class="grid">{''.join(f'<a class="card rv" style="text-decoration:none;color:inherit" href="services/{c["slug"]}/"><div class="bd"><span class="tag">{E(c["short"])}</span><h3>{E(c["name"])}</h3><p class="tx">{E(c["blurb"])}</p></div></a>' for c in CATEGORIES)}</div>
</div></section>
<section><div class="w"><h2 class="rv">How listings work</h2>
{tiers_strip()}</div></section>
<section class="alt"><div class="w"><div class="cta rv"><div><h2>List your workshop</h2><p>Car workshops and car services only. Ask Page One on WhatsApp how it works.</p></div>
<a class="btn amber big" href="{E(list_wa(0, 'general enquiry'))}" target="_blank" rel="noopener" data-cta="whatsapp_list_home">{WA_SVG} WhatsApp Page One</a></div></div></section>
<section><div class="w nar"><h2 class="rv">Questions</h2><div class="rv">{faq_html}</div></div></section>'''
    ld = [
        {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'url': abs_url(''), 'inLanguage': 'en-SG'},
        {'@context': 'https://schema.org', '@type': 'Organization', 'name': SITE_NAME, 'url': abs_url(''), 'parentOrganization': {'@type': 'Organization', 'name': 'Page One Singapore', 'url': 'https://pageonesingapore.com/'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
    ]
    page('', 'Car Workshops in Singapore | SG Car Workshop',
         'Browse car workshops in Singapore: repair, gearbox, ABS and ECU modules, spray painting, batteries, detailing, wraps and parts.', body, ld)


def category(c):
    depth = 2
    es = [e for e in ENTRIES if e['category'] == c['slug']]
    n = words(c['intro'])
    assert 40 <= n <= 60, (c['slug'], n)
    cr, crld = crumbs(depth, [('Services', 'services/' + c['slug'] + '/'), (c['name'], None)][1:])
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:20px"><div class="w"><h1>{E(c['name'])} in Singapore</h1><p class="lede">{E(c['intro'])}</p>{chip_row(depth, c['slug'])}</div></section>
<section><div class="w"><h2 class="rv">Listings</h2><div class="grid">{''.join(card(e, depth, 'services/%s/' % c['slug']) for e in es)}{list_card(depth, c['short'].lower())}</div></div></section>'''
    itemlist = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': c['name'] + ' in Singapore', 'numberOfItems': len(es),
                'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': abs_url('workshops/%s/' % e['slug']), 'name': e['name']} for i, e in enumerate(es)]}
    page('services/%s/' % c['slug'], '%s in Singapore | %s' % (c['name'], SITE_NAME), c['blurb'] + ' Browse Singapore listings with details confirmed by each business.',
         body, [itemlist, dict(crld, **{'@context': 'https://schema.org'})], h1=c['name'])


def area(slug, a):
    depth = 2
    es = [e for e in ENTRIES if slug in e['areas']]
    cr, crld = crumbs(depth, [(a['name'], None)])
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:20px"><div class="w"><h1>Car workshops in {E(a['name'])}</h1><p class="lede">{E(a['intro'])}</p></div></section>
<section><div class="w"><div class="grid">{''.join(card(e, depth, 'areas/%s/' % slug) for e in es)}{list_card(depth, 'car workshop in ' + a['name'])}</div></div></section>'''
    itemlist = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Car workshops in ' + a['name'], 'numberOfItems': len(es),
                'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': abs_url('workshops/%s/' % e['slug']), 'name': e['name']} for i, e in enumerate(es)]}
    page('areas/%s/' % slug, 'Car Workshops in %s | %s' % (a['name'], SITE_NAME), 'Car workshops and car services in %s, Singapore, with details confirmed by each business.' % a['name'],
         body, [itemlist, dict(crld, **{'@context': 'https://schema.org'})], h1='Car workshops in ' + a['name'])


def tier_badge(e_or_tier, cls=''):
    t = e_or_tier if isinstance(e_or_tier, str) else e_or_tier['tier']
    return '<span class="tier t-%s%s">%s</span>' % (t, (' ' + cls) if cls else '', E(TIERS[t]['badge']))


ASK = {'sg-garage': 'my car', 'cleanic-detailing': 'cleaning or fumigation for my car', 'autotex': 'a part for my car',
       'battery-rescue-sg': 'a battery for my car', 'wei-car-spray-painting': 'a spray painting job'}


def page_label(page_path):
    return '/' + page_path


def wa_href(e, page_path):
    """Directory WhatsApp link: the prefilled message names the business, the directory and the page the lead came from."""
    msg = "Hi %s, I found you on %s (%s). I'd like to ask about %s." % (e['name'], SITE_NAME, page_label(page_path), ASK.get(e['slug'], 'my car'))
    return wa_link(e['whatsapp'], msg)


def track_attrs(kind, e, page_path):
    return 'data-cta="%s_dir_%s" data-tier="%s" data-page="%s"' % (kind, e['slug'], e['tier'], E(page_label(page_path)))


def wa_btn(e, page_path, cls='', label='WhatsApp'):
    return '<a class="btn wa%s" href="%s" target="_blank" rel="noopener" %s>%s %s</a>' % (
        (' ' + cls) if cls else '', E(wa_href(e, page_path)), track_attrs('whatsapp', e, page_path), WA_SVG, E(label))


def call_btn(e, page_path, cls='', label='Call'):
    return '<a class="btn%s" href="tel:%s" %s>%s %s</a>' % ((' ' + cls) if cls else '', e['phone'], track_attrs('call', e, page_path), ic('phone'), E(label))


def photo_img(p, depth, lazy=True, cls=''):
    if p.get('f'):
        return img_tag(p['f'], p['alt'], depth, lazy=lazy, cls=cls)
    return '<img src="%s" alt="%s"%s decoding="async" referrerpolicy="no-referrer"%s>' % (
        E(p['u'], True), E(p['alt'], True), ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '')


def tile(e):
    return '<div class="tile" aria-hidden="true">%s<b>%s</b><span>%s</span></div>' % (ic(CAT[e['category']]['icon']), E(e['name']), E(e.get('tile_text', CAT[e['category']]['short'])))


def card(e, depth, page_path=''):
    c = CAT[e['category']]
    search = ' '.join([e['name'], c['name'], e['area_label'], ' '.join(s['n'] for s in e['services']), e.get('domain', ''), TIERS[e['tier']]['label'],
                       ' '.join(AREAS[a]['name'] for a in e['areas'])]).lower()
    ci = e.get('card_img')
    ph = photo_img(dict(ci, alt=ci['alt']), depth, lazy=True) if ci else tile(e)
    acts = ''
    if e.get('whatsapp'):
        acts += wa_btn(e, page_path, 'sm')
    if e.get('phone'):
        acts += call_btn(e, page_path, 'sm')
    acts += '<a class="btn sm" href="%sworkshops/%s/">Details</a>' % (pre(depth), e['slug'])
    return ('<article class="card rv" data-search="%s" data-tier="%s">'
            '<div class="ph">%s%s</div><div class="bd"><span class="tag">%s</span><h3><a href="%sworkshops/%s/">%s</a></h3>'
            '<p class="meta">%s</p><p class="tx">%s<br>%s</p><div class="acts">%s</div></div></article>') % (
        E(search, True), e['tier'], ph, tier_badge(e, 'on-ph'), E(c['short']), pre(depth), e['slug'], E(e['name']),
        E(e['area_label']), E(e['card_text'][0]), E(e['card_text'][1]), acts)


def free_card(depth, ex=FREE_EXAMPLE):
    """Free-tier card: plain. No photo, no phone. Shown only as a labelled example (made-up name)."""
    c = CAT[ex['category']]
    return ('<article class="card free-card"><div class="bd"><span class="ex-flag">Example only, not a real business</span>%s<span class="tag">%s</span>'
            '<h3>%s</h3><p class="meta">%s</p><p class="tx">%s</p><div class="acts">'
            '<span class="btn sm wa ex" aria-disabled="true">%s WhatsApp</span><span class="btn sm ex" aria-disabled="true">Website: %s</span></div></div></article>') % (
        tier_badge('free'), E(c['short']), E(ex['name']), E(ex['area_label']), E(ex['text']), WA_SVG, E(ex['site_label']))


def tiers_strip():
    """Short three-tier summary for the home page."""
    items = [
        ('free', 'A basic card: name, short description, categories, general area and a website link.'),
        ('premium', 'A full landing page: real photos, job gallery, services, address, map, WhatsApp and Call, reviews line and FAQs.'),
        ('premium_leadgen', 'Everything in Verified plus your own Page One website, local SEO and monthly tap reports.'),
    ]
    li = ''.join('<li class="rv">%s<b>%s</b><span class="pr">%s</span>%s</li>' % (tier_badge(t), E(TIERS[t]['tagline']), E(TIERS[t]['price_text']), E(txt)) for t, txt in items)
    return '<ol class="steps tiers-strip">%s</ol><p class="fine">The S$20 is the Verified listing, not the earlier S$20 early-bird SEO plan. <a href="list-your-workshop/">Compare the three tiers</a>.</p>' % li


def ld_business(e, url):
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', '@id': url + '#business', 'name': e['name'], 'url': url, 'mainEntityOfPage': url}
    first = e['photos'][0] if e.get('photos') else e.get('card_img')
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
    if e.get('areas') or e.get('service_area'):
        ld['areaServed'] = [{'@type': 'Place', 'name': AREAS[a]['name']} for a in e['areas']] or {'@type': 'Country', 'name': 'Singapore'}
    ld['makesOffer'] = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['n']}} for s in e['services']]
    same = list(e.get('social') or [])
    if e['tier'] == 'premium_leadgen':
        same.append(e['url'])
    if same:
        ld['sameAs'] = same
    if e.get('legal'):
        ld['legalName'] = e['legal']
        ld['taxID'] = e['uen']
    return ld


def listing(e):
    """Verified and Premium page. Same layout for both; the lead-gen tier adds the website button below WhatsApp and Call."""
    depth = 2
    c = CAT[e['category']]
    path = 'workshops/%s/' % e['slug']
    url = abs_url(path)
    cr, crld = crumbs(depth, [(c['name'], 'services/%s/' % c['slug']), (e['name'], None)])
    lead = e['tier'] == 'premium_leadgen'
    wa, call = wa_btn(e, path, 'big'), call_btn(e, path, 'big', 'Call ' + e['phone_show'])
    wa = wa.replace('WhatsApp</a>', 'WhatsApp %s</a>' % e.get('whatsapp_show', e['phone_show']))
    sec = []
    if lead:
        sec.append('<a class="btn amber" href="%s" target="_blank" rel="noopener" data-cta="visit_%s" data-tier="%s" data-page="%s">Visit %s for full details %s</a>' % (
            E(e['url']), e['slug'], e['tier'], E(page_label(path)), E(e['domain']), ic('out')))
    if e.get('book_url'):
        sec.append('<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="book_%s">%s</a>' % (E(e['book_url']), e['slug'], E(e['book_label'])))
    sec.append('<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="map_%s" data-map>%s %s</a>' % (E(e['map_url']), e['slug'], ic('pin'), E(e.get('map_label', 'Open in Google Maps'))))
    btns = '<div class="acts main-acts">%s%s</div><div class="acts sec-acts">%s</div>' % (wa, call, ''.join(sec))
    photos = e.get('photos') or []
    hero = '<div class="hero-ph">%s</div>' % (photo_img(photos[0], depth, lazy=False) if photos else tile(e))
    if photos and len(photos) > 1:
        gal = '<h2>Recent work</h2><div class="gal">%s</div>' % ''.join(
            '<figure class="rv job">%s<figcaption>%s</figcaption></figure>' % (photo_img(p, depth), E(p['cap'])) for p in photos[1:])
    else:
        gal = ''
    if e.get('illustrations'):
        gal += '<h2>Parts range</h2><div class="gal">%s</div>' % ''.join(
            '<figure class="rv illus">%s<figcaption>%s</figcaption></figure>' % (photo_img(p, depth), E(p['cap'])) for p in e['illustrations'])
    svcs = ''.join('<li class="svc rv"><b>%s</b><span>%s</span>%s</li>' % (E(s['n']), E(s['d']), ('<em class="pr">%s</em>' % E(s['p'])) if s.get('p') else '') for s in e['services'])
    extra = ''
    for h, kind, items in e.get('sections', []):
        extra += '<h2>%s</h2>' % E(h) + (('<ul class="tick">%s</ul>' % ''.join('<li>%s</li>' % E(i) for i in items)) if kind == 'ul' else ''.join('<p>%s</p>' % E(i) for i in items))
    adds = ''.join('<li data-addr>%s<span>%s%s%s</span></li>' % (
        ic('pin'), ('<b>%s</b><br>' % E(a['label'])) if a.get('label') else '', E(a['street']),
        (', Singapore ' + a['postal']) if a.get('postal') else ', Singapore') for a in e.get('addresses', []))
    if e.get('service_area') and not adds:
        adds = '<li data-addr>%s<span>%s</span></li>' % (ic('pin'), E(e['service_area']))
    elif e.get('service_area'):
        adds += '<li>%s<span>%s</span></li>' % (ic('pin'), E(e['service_area']))
    if e.get('addresses') and e['addresses'][0].get('note'):
        adds += '<li>%s<span>%s</span></li>' % (ic('shield'), E(e['addresses'][0]['note']))
    hours = ''
    if e.get('hours'):
        hours = '<h3>Opening hours</h3><dl class="hours">%s</dl>' % ''.join('<dt>%s</dt><dd>%s</dd>' % (E(a), E(b)) for a, b in e['hours'])
    if e.get('hours_note'):
        hours += '<p class="fine">%s</p>' % E(e['hours_note'])
    contact = '<li>%s<span>Call %s or WhatsApp %s</span></li>' % (ic('phone'), e['phone_show'], e.get('whatsapp_show', e['phone_show']))
    rv = e['reviews']
    reviews = '<p class="reviews-line">%s <span>%s</span> <a href="%s" target="_blank" rel="noopener" data-cta="reviews_%s">%s</a></p>' % (
        ic('shield'), E(rv['text']), E(rv['url']), e['slug'], E(rv['label']))
    faqs = ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in e['faqs'])
    price_note = '<p class="fine">%s</p>' % E(e['price_note']) if e.get('price_note') else ''
    note = '<p class="fine disclose">%s</p>' % E(e['note']) if e.get('note') else ''
    body = f'''<div class="w nar prem">{cr}
<div class="badges" style="margin-top:14px">{tier_badge(e)}<span class="tag">{E(c['short'])}</span></div>
<h1 style="margin-top:8px">{E(e['name'])}</h1>
<p class="meta">{E(e['area_label'])}</p>
<p class="lede" style="font-size:1.1rem">{E(e['lede'])}</p>
{btns}
{hero}
<h2>Services</h2>
<ul class="svcs">{svcs}</ul>
{price_note}
{gal}
{extra}
<section id="find" class="findus"><h2>{E(e.get('addr_heading', 'Find us'))}</h2>
<ul class="facts">{adds}{contact}</ul>
{hours}
</section>
<h2>Reviews</h2>
{reviews}
<h2>Questions</h2>
<div class="faqs">{faqs}</div>
<div class="cta rv" style="margin-top:26px"><div><h2>Ask {E(e['name'])}</h2><p>Message on WhatsApp or call. Say you found them on {E(SITE_NAME)}.</p></div><div class="acts">{wa}{call}</div></div>
{('<div class="acts sec-acts" style="margin-top:12px">%s</div>' % sec[0]) if lead else ''}
{note}
<p class="fine">Details are checked with the business before the directory goes live. Last updated {UPDATED}. Browse more <a href="../../services/{c['slug']}/">{E(c['name'].lower())}</a> listings{(' or <a href="../../areas/%s/">workshops in %s</a>' % (e['areas'][0], E(AREAS[e['areas'][0]]['name']))) if e['areas'] else ''}.</p>
</div>'''
    bar = wabar([wa_btn(e, path), call_btn(e, path)])
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in e['faqs']]}
    ld = [ld_business(e, url), faq_ld, dict(crld, **{'@context': 'https://schema.org'})]
    og = e.get('og_img') or (photos[0]['u'] if photos and photos[0].get('u') else None)
    page(path, e['title'], e['desc'], body, ld, og=og, bar=bar, h1=e['name'])


def tier_features():
    return [
        ('Basic card: name, short description, categories, general area', 'yes', 'yes', 'yes'),
        ('Link to your website', 'yes', 'yes', 'yes (shown as a secondary button)'),
        ('WhatsApp button with the source tagged', 'yes', 'yes', 'yes'),
        ('Tap counts (WhatsApp and call) reported to you', 'yes', 'yes', 'yes'),
        ('Your own full page: real photos and a completed-job gallery', 'no', 'yes', 'yes'),
        ('Detailed services with short descriptions', 'no', 'yes', 'yes'),
        ('Full address, Google Maps link and opening hours', 'no', 'yes', 'yes'),
        ('Phone, direct WhatsApp and Call buttons, sticky on phones', 'no', 'yes', 'yes'),
        ('Reviews line from a source people can check, with link and date', 'no', 'yes', 'yes'),
        ('3 to 5 local FAQs', 'no', 'yes', 'yes'),
        ('LocalBusiness structured data', 'no', 'yes', 'yes'),
        ('Your own website, local SEO, AI search optimisation, regular content', 'no', 'no', 'yes'),
        ('Lead tracking and monthly reporting', 'no', 'no', 'yes'),
    ]


def tier_table():
    def cell(v):
        if v == 'yes':
            return '<td class="y"><span aria-label="Included">%s</span></td>' % ic('shield')
        if v == 'no':
            return '<td class="n"><span aria-label="Not included">&ndash;</span></td>'
        return '<td class="y">%s</td>' % E(v)
    heads = ''.join('<th scope="col">%s<span class="pr">%s</span><small>%s</small></th>' % (tier_badge(t), E(TIERS[t]['price_text']), E(TIERS[t]['tagline'])) for t in TIERS)
    rows = ''.join('<tr><th scope="row">%s</th>%s</tr>' % (E(f), cell(a) + cell(b) + cell(c)) for f, a, b, c in tier_features())
    table = '<div class="tier-table"><table><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table></div>' % (heads, rows)
    cards = ''
    for i, t in enumerate(TIERS):
        li = ''.join('<li%s>%s</li>' % ('' if row[1 + i] != 'no' else ' class="no"', E(row[0])) for row in tier_features())
        cards += ('<article class="card tier-card rv"><div class="bd">%s<h3>%s</h3><p class="pr">%s</p><p class="meta">%s</p><ul class="tick">%s</ul>'
                  '<a class="btn amber" href="%s" target="_blank" rel="noopener" data-cta="whatsapp_list_tier_%s">%s Ask about %s</a></div></article>') % (
            tier_badge(t), E(TIERS[t]['label']), E(TIERS[t]['price_text']), E(TIERS[t]['tagline']), li, E(list_wa(1, TIERS[t]['label'])), t, WA_SVG, E(TIERS[t]['label']))
    return table + '<div class="tier-cards">%s</div>' % cards


def list_page():
    depth = 1
    cr, crld = crumbs(depth, [('List your workshop', None)])
    wa = E(list_wa(depth, 'general enquiry'))
    body = f'''<div class="w">{cr}
<h1 style="margin-top:14px">List your workshop</h1>
<p class="lede" style="font-size:1.1rem;max-width:720px">{E(SITE_NAME)} lists car workshops and car services in Singapore: repair, gearbox, ABS and ECU modules, spray painting and bodywork, batteries, detailing and coating, wraps and PPF, and parts. Pick the tier that fits your business.</p>
<h2 style="margin-top:24px">Three tiers</h2>
{tier_table()}
<p class="fine">{E(PRICE_NOTE)} Prices are per month. Every tier gets WhatsApp taps counted and reported to you, and no tier promises a number of enquiries or a ranking.</p>
<h2 style="margin-top:28px">What a free card looks like</h2>
<p>A Basic listing is a plain card. Here is a made-up example with a made-up name, so you can see the style.</p>
<div class="grid ex-grid">{free_card(depth)}</div>
<h2 style="margin-top:28px">What we need from you</h2>
<ul class="tick"><li>Your agreement in writing (WhatsApp is fine) and permission to use your photos</li><li>Business name, area, phone or WhatsApp, and the services you really offer</li><li>For Verified: your address, opening hours, a few photos of real jobs, and a review source we can link to</li></ul>
<h2>What we do not do</h2>
<p>We do not rank workshops, use rating or review markup, or list car dealers or insurers. A rating line is shown only when it comes from a source people can open, with its link and the date we checked. Anything we cannot confirm with you stays off the page.</p>
<div class="cta rv" style="margin-top:22px"><div><h2>Ask on WhatsApp</h2><p>Tell us what your workshop does and we will reply with the next step.</p></div>
<a class="btn amber big" href="{wa}" target="_blank" rel="noopener" data-cta="whatsapp_list_page">{WA_SVG} WhatsApp Page One</a></div>
</div>'''
    page('list-your-workshop/', 'List Your Car Workshop | SG Car Workshop',
         'Free, Verified S$20/month or Premium S$50/month: compare the three ways to list your car workshop in Singapore.',
         body, [dict(crld, **{'@context': 'https://schema.org'})])


def about_page():
    depth = 1
    cr, crld = crumbs(depth, [('About', None)])
    body = f'''<div class="w nar">{cr}
<h1 style="margin-top:14px">About {E(SITE_NAME)}</h1>
<p class="lede" style="font-size:1.1rem">{E(SITE_NAME)} is a directory of car workshops and car services in Singapore, run by Page One Singapore, a web and SEO service for small businesses.</p>
<h2>How entries are checked</h2>
<p>Every fact on a page comes from the business or from its public records, and the business confirms it before the directory goes live. If a detail cannot be confirmed, such as a price or opening hours, we leave it out. We never copy a business's website text. We do not rank workshops or use rating markup; a rating line appears only with a source link and the date we checked.</p>
<h2>Who we list</h2>
<p>Car workshops and car services only: repair and servicing, gearbox, ABS and ECU modules, spray painting and bodywork, batteries, detailing and coating, wraps and PPF, and parts. Car dealers and insurance are not listed.</p>
<h2>A note on one listing</h2>
<p>SG Garage, a workshop in Ang Mo Kio, belongs to the founder of Page One Singapore. We list it like any other entry and say so here.</p>
<h2>Contact</h2>
<p>Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W). To list a workshop or correct a page, WhatsApp {PAGE_ONE_WA_SHOW}.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn wa big" href="{E(list_wa(depth, 'general enquiry'))}" target="_blank" rel="noopener" data-cta="whatsapp_about">{WA_SVG} WhatsApp {PAGE_ONE_WA_SHOW}</a>
<a class="btn big" href="../list-your-workshop/">How listing works</a></div>
</div>'''
    page('about/', 'About SG Car Workshop | Run by Page One Singapore',
         'SG Car Workshop is a Singapore car workshop directory run by Page One Singapore. Details are confirmed by each business. Contact us on WhatsApp.',
         body, [dict(crld, **{'@context': 'https://schema.org'}), {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About ' + SITE_NAME, 'url': abs_url('about/')}])


def not_found():
    b = PATH_BASE
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (b, c['slug'], E(c['name'])) for c in CATEGORIES)
    out = f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | {E(SITE_NAME)}</title><meta name="robots" content="noindex">
<link rel="icon" href="{b}assets/favicon.ico" sizes="48x48"><link rel="stylesheet" href="{b}assets/dir.css?v={V}"></head>
<body><main class="w nar" style="padding:60px 16px"><h1>That page is not here</h1><p>The page may have moved. Try the <a href="{b}">home page</a> or pick a service.</p>
<ul class="tick">{cats}</ul><p><a class="btn amber" href="{b}">Back to {E(SITE_NAME)}</a></p></main></body></html>
'''
    return out


# ------------------------------------------------------------------ build
def build():
    home()
    for c in CATEGORIES:
        if any(e['category'] == c['slug'] for e in ENTRIES):
            category(c)
    for s, a in AREAS.items():
        if any(s in e['areas'] for e in ENTRIES):
            area(s, a)
    for e in ENTRIES:
        listing(e)
    list_page()
    about_page()

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT + '/assets/img')
    for path, h in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)
    open(OUT + '/404.html', 'w', encoding='utf-8').write(not_found())
    for f in ('dir.css', 'dir.js'):
        shutil.copy(os.path.join(HERE, f), OUT + '/assets/' + f)
    shutil.copytree(os.path.join(HERE, 'img'), OUT + '/assets/img', dirs_exist_ok=True)
    make_icons()

    urls = sorted(PAGES)
    open(OUT + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                          ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (abs_url(p), UPDATED) for p in urls) + '</urlset>\n')
    if LIVE:
        bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
        robots = ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BASE
    else:
        robots = 'User-agent: *\nDisallow: /\n'
    open(OUT + '/robots.txt', 'w').write(robots)
    lines = ['# %s' % SITE_NAME, '', '> A directory of car workshops and car services in Singapore, run by Page One Singapore. Entries use details confirmed by each business. No rankings and no rating or review markup.', '',
             'Last updated: %s' % UPDATED, '', '## Services']
    lines += ['- [%s](%sservices/%s/): %s' % (c['name'], BASE, c['slug'], c['blurb']) for c in CATEGORIES]
    lines += ['', '## Listings']
    for e in ENTRIES:
        lines.append('- [%s](%sworkshops/%s/): %s, %s%s' % (e['name'], BASE, e['slug'], CAT[e['category']]['name'] + ', ' + TIERS[e['tier']]['label'], e['area_label'], (' (own website: %s)' % e['url']) if e['tier'] == 'premium_leadgen' else ''))
    lines += ['', '## More', '- [List your workshop](%slist-your-workshop/)' % BASE, '- [About](%sabout/)' % BASE, '']
    open(OUT + '/llms.txt', 'w').write('\n'.join(lines))
    print('built %d pages + 404 into %s (LIVE=%s, v=%s)' % (len(PAGES), OUT, LIVE, V))


def make_icons():
    """Favicon, app icons and default share image, drawn with Pillow (no external files)."""
    from PIL import ImageDraw, ImageFont

    def mark(sz):
        im = Image.new('RGB', (sz, sz), '#12306b')
        d = ImageDraw.Draw(im)
        k = sz / 48.0
        d.rounded_rectangle([0, 0, sz - 1, sz - 1], radius=int(12 * k), fill='#12306b')
        d.polygon([(8 * k, 29 * k), (16 * k, 22 * k), (24 * k, 20 * k), (36 * k, 26 * k), (40 * k, 27 * k), (44 * k, 29 * k), (44 * k, 33 * k), (8 * k, 33 * k)], fill='white')
        for cx in (16, 33):
            d.ellipse([(cx - 4.5) * k, 28.5 * k, (cx + 4.5) * k, 37.5 * k], fill='#12306b', outline='white', width=max(1, int(2 * k)))
        d.line([(6 * k, 41 * k), (42 * k, 41 * k)], fill='#f5a623', width=max(1, int(3 * k)))
        return im
    mark(192).save(OUT + '/assets/icon-192.png')
    mark(180).save(OUT + '/assets/apple-touch-icon.png')
    mark(48).save(OUT + '/assets/favicon.ico', sizes=[(48, 48)])
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), '#12306b')
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(18 + 10 * t), int(48 + 30 * t), int(107 + 50 * t)))
    for x in range(0, W, 80):
        d.rectangle([x, 560, x + 50, 566], fill='#f5a623')
    try:
        fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 84)
        fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 38)
    except OSError:
        fb = fs = ImageFont.load_default()
    d.text((80, 190), SITE_NAME, font=fb, fill='white')
    d.text((80, 310), 'Car workshops and car services in Singapore', font=fs, fill='#f5a623')
    d.text((80, 370), 'Details confirmed by each business', font=fs, fill='#dbe6ff')
    im.save(OUT + '/assets/img/og-default.jpg', quality=85)


if __name__ == '__main__':
    build()

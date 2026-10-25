"""SG Commercial Fitout - Retail & Commercial Design & Build: builds every page into site/ (python3 build.py).

New Edwin-owned brand, started 24 Oct 2026 from the brief in drdigital641/edwin-ai-context
(handoffs/2026-10-24-rc-design-build-project.md, copied to content/PROJECT-BRIEF.md).
Facts: there are none yet beyond the brand name, tagline and service scope in the brief. No address, UEN, team,
years, prices, reviews, warranties or completed projects exist, so none are published. Every image is an
AI design concept (generated 24 Oct 2026 with Base44 GenerateImage) and is labelled as such where shown.
Pending before LIVE (shown in dashed boxes on the preview): domain, operating entity + UEN, public contact
(WhatsApp number: Edwin chose "decide later" on 24 Oct 2026), who delivers the work, service area.

Env: RC_OUT (output dir), RC_IMG (image base URL, e.g. a local folder for screenshots).
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
sys.path.insert(0, os.path.join(HERE, 'content'))
import services as C_SVC  # noqa: E402
import avl as C_AVL  # noqa: E402
import spaces as C_SPC  # noqa: E402
import guides as C_GDE  # noqa: E402

OUT = os.environ.get('RC_OUT', os.path.join(HERE, 'site'))
SLUG = 'rc-design-build'
DOMAIN = 'commercialfitout.sg'   # Edwin 24 Oct 2026 12:08 UTC (no DNS yet on 24 Oct)
LIVE = True            # True only after Edwin's go-ahead and every PENDING item is confirmed
WA_NUMBER = '6586594553'  # Edwin 24 Oct 2026
PHONE_DISPLAY = '+65 8659 4553'
ADDR_TEXT = '113 Eunos Ave 3, #04-02, Gordon Ind Building, Singapore 409838'  # Edwin 25 Oct 2026
ADDR_HTML = '113 Eunos Ave 3, #04-02<br>Gordon Ind Building<br>Singapore 409838'
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
BASE = ('https://%s/' % DOMAIN) if DOMAIN else PREVIEW
ASSET_SHA = 'c4353b1'
IMG = os.environ.get('RC_IMG') or ('https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@%s/site-assets/%s/' % (ASSET_SHA, SLUG))
TODAY = '2026-10-24'
LASTMOD_OVERRIDE = {'/guides/': '2026-10-26'}  # pages whose content changed after TODAY (night article run)
INDEXNOW_KEY = '7d4c2a9e1f6b8035c4e2a7d9b1f60c38'
BRAND = 'SG Commercial Fitout'
BRAND_FULL = 'SG Commercial Fitout - Retail & Commercial Design & Build'
TAGLINE = 'Singapore retail and commercial design & build specialists.'

if LIVE:
    assert DOMAIN and WA_NUMBER, 'LIVE needs DOMAIN and WA_NUMBER confirmed'

PENDING = [
    ('Operating company', 'Registered business name and UEN to be confirmed.'),
]

# Real work supplied by Edwin 24 Oct 2026 ("real projects" by the company). Each upload carried the caption
# "AI styling concept - proposed additions": the carpentry is real, decor items were added with AI styling.
REAL = [
    ('real-shelving', 'Built-in shelving bay', 'Full-height open shelving with adjustable shelves and a low storage counter beside it.'),
    ('real-pantry-counter', 'Pantry counter and cabinets', 'Handle-less drawers and doors under a stone-look top, with a floating shelf above.'),
    ('real-sink-counter', 'Sink counter with drawers', 'Undermount sink run with cabinets, drawers and a floating shelf with under-shelf lighting.'),
    ('real-wall-cabinet', 'Wall cabinet with adjustable shelves', 'Top-hung cabinets above the hood, fitted with concealed hinges and adjustable shelves.'),
    ('real-pantry-drawers', 'Drawer stack detail', 'Three-drawer stack and double-door cabinet with recessed finger pulls.'),
]
REAL_NOTE = 'Real SG Commercial Fitout carpentry. Decor items in these photos were added with AI styling.'
WORKSHOP = []  # filenames of real workshop photos (Edwin uploading 24 Oct 2026 evening)

# ---------- page registry ----------
SVC = {p['path']: p for p in C_SVC.PAGES}
AVLP = {p['path']: p for p in C_AVL.PAGES}
SPC = {p['path']: p for p in C_SPC.PAGES}
GDE = {p['path']: p for p in C_GDE.PAGES}
DAILY = sorted(json.load(open(os.path.join(HERE, 'content', 'daily.json'))), key=lambda d: d['date'], reverse=True)
ALL_CONTENT = {}
for d in (SVC, AVLP, SPC, GDE):
    ALL_CONTENT.update(d)

SERVICE_ORDER = ['/retail-commercial-design-build/', '/services/commercial-carpentry/', '/services/commercial-renovation/',
                 '/services/commercial-electrical-works/', '/services/commercial-tiling-flooring/',
                 '/services/commercial-painting-finishing/']
SHORT = {
    '/retail-commercial-design-build/': 'Design & Build', '/services/commercial-carpentry/': 'Carpentry',
    '/services/commercial-renovation/': 'Renovation', '/services/commercial-electrical-works/': 'Electrical works',
    '/services/commercial-tiling-flooring/': 'Tiling & flooring', '/services/commercial-painting-finishing/': 'Painting & finishing',
    '/avl/': 'AVL overview', '/avl/commercial-audio-systems/': 'Audio systems', '/avl/display-visual-systems/': 'Displays & signage',
    '/avl/architectural-feature-lighting/': 'Feature lighting', '/spaces/retail-shops-boutiques/': 'Retail shops & boutiques',
    '/spaces/offices-showrooms/': 'Offices & showrooms', '/spaces/cafes-service-counters/': 'Cafes & service counters',
    '/spaces/salons-beauty-studios/': 'Salons & beauty studios', '/services/': 'Services', '/spaces/': 'Spaces',
    '/design-concepts/': 'Design concepts', '/guides/': 'Guides', '/about/': 'About', '/contact/': 'Contact',
    '/privacy-policy/': 'Privacy policy', '/': 'Home', '/projects/': 'Projects & workshop',
    '/design-concepts/concept-of-the-day/': 'AI concept of the day',
}
for p in GDE.values():
    SHORT[p['path']] = p['h1']

NAV = [('/services/', 'Services'), ('/avl/', 'AVL'), ('/projects/', 'Projects'),
       ('/spaces/', 'Spaces'), ('/design-concepts/', 'Concepts'), ('/guides/', 'Guides'), ('/about/', 'About'),
       ('/contact/', 'Contact')]

# ---------- helpers ----------
E = html.escape


def rel(frm, to):
    """Relative link from page path frm (a folder path) to path to, so the site works in /preview/<slug>/ and on a domain."""
    if to.startswith(('http', 'mailto:', 'tel:', '#')):
        return to
    depth = len([s for s in frm.strip('/').split('/') if s])
    r = '../' * depth + to.lstrip('/')
    return r or './'


def abs_url(path):
    return BASE + path.lstrip('/')


def fix_links(h, frm):
    return re.sub(r'href="(/[^"]*)"', lambda m: 'href="%s"' % rel(frm, m.group(1)), h)


def vhash(name):
    with open(os.path.join(HERE, name), 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def img_url(key, small=False):
    return IMG + key + ('-640' if small else '') + '.webp'


def daily_url(d, small=False):
    sha = ASSET_SHA if d['asset_sha'] == 'ASSET_SHA' else d['asset_sha']
    base = os.environ.get('RC_IMG') or ('https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@%s/site-assets/%s/' % (sha, SLUG))
    return base + d['image'] + ('-640' if small else '') + '.webp'


def nice_date(iso):
    import datetime
    return datetime.date.fromisoformat(iso).strftime('%-d %b %Y')


def real_pic(key, alt, eager=False):
    return ('<img src="%s" srcset="%s 640w, %s 1100w" sizes="(max-width: 700px) 80vw, 30vw" width="640" height="480" alt="%s"%s decoding="async">'
            '<span class="tag tag-real">Real project</span>') % (img_url(key, True), img_url(key, True), img_url(key), E(alt),
                                                                ' loading="eager"' if eager else ' loading="lazy"')


def pic(key, alt, cls='', eager=False, small=False, tag=True):
    w = 640 if small else 1024
    srcset = '%s 640w, %s 1024w' % (img_url(key, True), img_url(key))
    sizes = '(max-width: 700px) 92vw, 46vw' if not small else '(max-width: 600px) 92vw, 30vw'
    t = '<img src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s"%s%s>' % (
        img_url(key, small), srcset, sizes, w, w, E(alt),
        ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"', ' decoding="async"')
    if tag:
        t += '<span class="tag">AI design concept</span>'
    return t


def wa_link(topic, frm):
    if not WA_NUMBER:
        return None
    msg = 'Hi SG Commercial Fitout, I would like to discuss %s. (Page: %s, ref: website)' % (topic, frm)
    return 'https://wa.me/%s?text=%s' % (WA_NUMBER, quote(msg))


WA_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3Z"/></svg>'


def cta(frm, topic='my space', label='Discuss Your Space', cls='btn btn-main'):
    w = wa_link(topic, frm)
    if w:
        return '<a class="%s" href="%s" rel="noopener">%s%s</a>' % (cls, E(w), WA_SVG, label)
    return '<a class="%s" href="%s">%s</a>' % (cls, rel(frm, '/contact/'), label)


def pending_box(items=None, title='Pending before launch'):
    if LIVE:
        return ''
    items = items or PENDING
    return '<div class="pending"><b>%s (preview note)</b>%s</div>' % (
        E(title), '<br>'.join('%s: %s' % (E(a), E(b)) for a, b in items))


def faq_html(faqs):
    return '<div class="faq"><h2>Frequently asked questions</h2>%s</div>' % ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)


def faq_schema(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q,
            'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}


SPECIALTY = 'Design and build specialists for retail outlets and commercial spaces in Singapore'
AUDIENCE = {'@type': 'BusinessAudience', 'name': 'Retail outlet and commercial space owners and tenants in Singapore',
            'audienceType': 'Shops, boutiques, offices, showrooms, F&B outlets, cafes and salons',
            'geographicArea': {'@type': 'Country', 'name': 'Singapore'}}
SG = {'@type': 'Country', 'name': 'Singapore', 'sameAs': 'https://en.wikipedia.org/wiki/Singapore'}


def org_schema():
    o = {'@type': ['Organization', 'GeneralContractor'], '@id': BASE + '#org', 'name': BRAND_FULL, 'alternateName': [BRAND, 'CommercialFitout.sg', 'SG Fitout'],
         'url': BASE, 'logo': BASE + 'icon-512.png', 'image': IMG + 'og-rc.jpg', 'slogan': SPECIALTY,
         'telephone': PHONE_DISPLAY, 'address': {'@type': 'PostalAddress', 'streetAddress': '113 Eunos Ave 3, #04-02, Gordon Ind Building', 'addressLocality': 'Singapore', 'postalCode': '409838', 'addressCountry': 'SG'},
         'areaServed': SG, 'audience': AUDIENCE,
         'knowsAbout': ['Retail shop fit-out', 'Commercial interior design and build', 'Shop renovation', 'Office renovation',
                        'Showroom fit-out', 'F&B counter and cafe fit-out', 'Salon fit-out', 'Commercial carpentry', 'Retail display shelving',
                        'Commercial electrical works', 'Commercial tiling and flooring', 'Audio, visual and lighting (AVL) for shops'],
         'contactPoint': {'@type': 'ContactPoint', 'telephone': PHONE_DISPLAY, 'contactType': 'sales', 'areaServed': 'SG',
                          'availableLanguage': ['English']},
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Retail and commercial design and build services in Singapore',
                             'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': SHORT[x] + ' for retail and commercial spaces',
                                                                                     'url': abs_url(x)}} for x in SERVICE_ORDER]},
         'description': 'SG Commercial Fitout specialises in design and build for retail outlets and commercial spaces in Singapore, such as shops, '
                        'offices, showrooms, F&B outlets and salons, with its own carpentry workshop: carpentry, renovation, electrical works, '
                        'tiling and flooring, painting and finishing, and audio, visual and lighting (AVL).'}
    return o


def crumbs_html(frm, crumbs):
    li = ['<li><a href="%s">Home</a></li>' % rel(frm, '/')]
    for path, name in crumbs[:-1]:
        li.append('<li><a href="%s">%s</a></li>' % (rel(frm, path), E(name)))
    li.append('<li aria-current="page">%s</li>' % E(crumbs[-1][1]))
    return '<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>%s</ol></nav>' % ''.join(li)


def crumbs_schema(crumbs):
    items = [('/', 'Home')] + list(crumbs)
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': abs_url(p)} for i, (p, n) in enumerate(items)]}


def card(frm, path, title, text, key, more='More details', small=True):
    return ('<a class="card rv" href="%s"><div class="ph">%s</div><div class="bd"><h3>%s</h3><p>%s</p>'
            '<span class="more">%s</span></div></a>') % (rel(frm, path), pic(key, title + ' (AI design concept)', small=small),
                                                        E(title), E(text), more)


def svc_tile(frm, path):
    p = ALL_CONTENT[path]
    return ('<a class="rv" href="%s"><img src="%s" width="92" height="92" alt="" loading="lazy" decoding="async">'
            '<div><h3>%s</h3><p>%s</p><span class="more">More details</span></div></a>') % (
        rel(frm, path), img_url(p['image'], True), E(SHORT.get(path, p['h1'])), E(p['card']))


# ---------- layout ----------
def brand_title(t):
    if t.endswith(' | R&C'):
        base = t[:-6]
        for suf in (' | SG Commercial Fitout', ' | SG Fitout'):
            if len(base + suf) <= 60:
                return base + suf
        return base
    return t


def head(path, title, desc, schema, og_img=None):
    title = brand_title(title)
    can = abs_url(path)
    og = og_img or (IMG + 'og-rc.jpg')
    ld = json.dumps({'@context': 'https://schema.org', '@graph': schema}, ensure_ascii=False).replace('</', '<\\/')
    r = rel(path, '/')
    return '''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2b2925">
<link rel="icon" href="%sfavicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="%sicon-192.png">
<link rel="apple-touch-icon" href="%sapple-touch-icon.png">
<link rel="manifest" href="%ssite.webmanifest">
<link rel="preload" href="%sfonts/fraunces-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%src.css?v=%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Small shop interior with oak shelving and cream walls (AI design concept)">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">%s</script>
</head>
''' % (E(title), E(desc), can, r, r, r, r, r, r, vhash('rc.css'), E(BRAND_FULL), E(title), E(desc), can, og, ld)


def header(path):
    links = ''.join('<a href="%s"%s>%s</a>' % (rel(path, p), ' aria-current="page"' if path == p or (p != '/' and path.startswith(p) and p in ('/services/', '/avl/', '/spaces/', '/guides/')) else '', E(n))
                    for p, n in NAV)
    return '''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>Retail &amp; commercial specialists</span><span>Shops · Offices · F&amp;B · Salons · Own workshop</span><a href="%s" rel="noopener">WhatsApp %s</a></div></div>
<header class="top"><div class="wrap">
<a class="brand" href="%s" aria-label="SG Commercial Fitout home"><img src="%sicons/logo-header.png" width="230" height="48" alt="SG Commercial Fitout"></a>
<nav class="nav" id="nav" aria-label="Main">%s</nav>
%s
<button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false">Menu</button>
</div></header>
<main id="main">
''' % (E(wa_link('my space', path) or rel(path, '/contact/')), PHONE_DISPLAY, rel(path, '/'), rel(path, '/'), links, cta(path, 'my space', 'WhatsApp Us'))


def footer(path):
    col = lambda paths: ''.join('<li><a href="%s">%s</a></li>' % (rel(path, p), E(SHORT[p])) for p in paths)
    return '''</main>
<footer class="foot"><div class="wrap">
<div><img class="flogo" src="%sicons/logo-sgcf-light.png" width="260" height="66" alt="SG Commercial Fitout - Retail &amp; Commercial Design &amp; Build" loading="lazy"><p>%s</p><p>%s</p><p>WhatsApp <a href="%s" rel="noopener">%s</a></p>%s</div>
<div><h3>Services</h3><ul>%s</ul></div>
<div><h3>AVL &amp; spaces</h3><ul>%s</ul></div>
<div><h3>Plan</h3><ul>%s</ul></div>
<p class="small">Photos marked "Real project" show SG Commercial Fitout carpentry (decor added with AI styling). Photos marked "AI design concept" are ideas, not completed work. &copy; 2026 %s.</p>
</div></footer>
<a class="wa-float" href="%s" rel="noopener" aria-label="WhatsApp SG Commercial Fitout">%s<span class="sr">WhatsApp %s</span></a>
<script src="%src.js?v=%s" defer></script>
<script src="%swa-tap-counter.js?v=%s" defer></script>
</body>
</html>
''' % (rel(path, '/'), E(TAGLINE), ADDR_HTML, E(wa_link('my space', path) or ''), PHONE_DISPLAY, pending_box([('Operating company', 'name and UEN to be confirmed')]),
       col(SERVICE_ORDER), col(['/avl/', '/avl/commercial-audio-systems/', '/avl/display-visual-systems/', '/avl/architectural-feature-lighting/', '/spaces/retail-shops-boutiques/', '/spaces/cafes-service-counters/']),
       col(['/projects/', '/design-concepts/', '/design-concepts/concept-of-the-day/', '/guides/', '/about/', '/contact/', '/privacy-policy/']), E(BRAND_FULL),
       E(wa_link('my space', path) or ''), WA_SVG, PHONE_DISPLAY, rel(path, '/'), vhash('rc.js'), rel(path, '/'), vhash('wa-tap-counter.js'))


def cta_band(path, topic):
    return ('<div class="wrap"><div class="cta-band rv"><div><h2>Planning a shop, office, cafe or salon space?</h2>'
            '<p>WhatsApp your floor plan, unit photos, what the space is for and your target opening date. We\'ll discuss your scope.</p></div>'
            '<div>%s</div></div></div>') % cta(path, topic, 'WhatsApp Us', 'btn btn-light')


PAGES_OUT = []  # (path, lastmod)


def write(path, doc, lastmod=TODAY):
    d = os.path.join(OUT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(doc)
    PAGES_OUT.append((path, lastmod))


# ---------- content pages ----------
def related_html(path, rels):
    out = []
    for r in rels:
        if r in SHORT:
            out.append('<li><a href="%s">%s</a></li>' % (rel(path, r), E(SHORT[r])))
    return ''.join(out)


def content_page(p, crumbs, kind='service'):
    path = p['path']
    schema = [org_schema(), crumbs_schema(crumbs), faq_schema(p['faqs'])]
    main_entity = {'@type': 'Article' if kind == 'guide' else 'Service', 'name': p['h1'], 'description': p['desc'],
                   'url': abs_url(path), 'image': img_url(p['image'])}
    if kind == 'guide':
        main_entity.update({'headline': p['h1'], 'datePublished': p['date'], 'dateModified': p['date'],
                            'author': {'@id': BASE + '#org'}, 'publisher': {'@id': BASE + '#org'}})
    else:
        main_entity.update({'provider': {'@id': BASE + '#org'}, 'serviceType': p['kicker'], 'areaServed': SG, 'audience': AUDIENCE,
                            'category': 'Retail and commercial interiors'})
    schema.append(main_entity)
    secs = ''.join('<h2>%s</h2>%s' % (E(s['h2']), fix_links(s['html'], path)) for s in p['sections'])
    meta = ''
    if kind == 'guide':
        meta = '<p class="meta">Planning guide · %s · Published 24 October 2026</p>' % E(p['reading'])
    side_rel = related_html(path, p['related'])
    owner = ''
    if kind == 'guide' and p.get('owner') in SHORT:
        owner = '<p><a class="btn btn-ghost" href="%s">%s</a></p>' % (rel(path, p['owner']), E('See ' + SHORT[p['owner']]))
    body = '''%s
<section class="phead"><div class="wrap">
<div><span class="eyebrow">%s</span><h1>%s</h1><p class="answer">%s</p>%s<div class="btns">%s</div></div>
<div class="pic">%s</div>
</div></section>
<div class="wrap layout">
<article class="prose">%s%s%s</article>
<aside class="side"><div class="panel"><h3>Related</h3><ul>%s</ul></div>
<div class="panel"><h3>Start with the basics</h3><p>A floor plan, a few unit photos, how you'll use the space and your target opening date.</p>%s</div></aside>
</div>
%s''' % (crumbs_html(path, crumbs), E(p['kicker']), E(p['h1']), E(p['answer']), meta,
         cta(path, p.get('wa_topic', 'my space')) + (' <a class="btn btn-ghost" href="%s">All services</a>' % rel(path, '/services/') if kind == 'service' else ''),
         pic(p['image'], p['image_alt'], eager=True), secs, owner, faq_html(p['faqs']), side_rel,
         cta(path, p.get('wa_topic', 'my space')), cta_band(path, p.get('wa_topic', 'my space')))
    write(path, head(path, p['title'], p['desc'], schema) + header(path) + body + footer(path), p.get('date', TODAY))


# ---------- hub pages ----------
def hub(path, title, desc, h1, kicker, intro, key, alt, inner, crumbs, extra_schema=None):
    schema = [org_schema(), crumbs_schema(crumbs), {'@type': 'CollectionPage', 'name': h1, 'url': abs_url(path), 'description': desc}]
    if extra_schema:
        schema += extra_schema
    body = '''%s
<section class="phead"><div class="wrap">
<div><span class="eyebrow">%s</span><h1>%s</h1><p class="answer">%s</p><div class="btns">%s</div></div>
<div class="pic">%s</div></div></section>
<section class="band sand"><div class="wrap">%s</div></section>
%s''' % (crumbs_html(path, crumbs), E(kicker), E(h1), E(intro), cta(path), pic(key, alt, eager=True), inner, cta_band(path, 'my space'))
    write(path, head(path, title, desc, schema) + header(path) + body + footer(path))


def build_hubs():
    # services
    inner = '<div class="head"><h2>Specialist services</h2><p>Each page explains scope, options, budget drivers and what to prepare.</p></div><div class="svc">%s</div>' % ''.join(
        svc_tile('/services/', s) for s in SERVICE_ORDER)
    inner += '<div class="head" style="margin-top:44px"><h2>Audio, visual and lighting</h2><p>Sound, screens and feature light planned with the fit-out.</p></div><div class="svc">%s</div>' % ''.join(
        svc_tile('/services/', s) for s in ['/avl/commercial-audio-systems/', '/avl/display-visual-systems/', '/avl/architectural-feature-lighting/'])
    hub('/services/', 'Retail & Commercial Renovation Services | R&C',
        'Commercial carpentry, renovation, electrical works, tiling, flooring, painting and AVL for shops, offices, cafes and salons in Singapore.',
        'Services for retail and commercial spaces', 'Services', C_SVC.SERVICES_INTRO, 'counter-joinery',
        'Custom oak shop counter with display niche (AI design concept)', inner, [('/services/', 'Services')])
    # spaces
    inner = '<div class="head"><h2>Choose your type of space</h2></div><div class="grid g4">%s</div>' % ''.join(
        card('/spaces/', p['path'], SHORT[p['path']], p['card'], p['image']) for p in C_SPC.PAGES)
    hub('/spaces/', 'Shop, Office, Cafe & Salon Interiors | R&C',
        'Plan a retail shop, office or showroom, cafe counter or salon interior: the needs, scope mix and materials for each type of business space.',
        'Interiors by type of business space', 'Spaces', C_SPC.SPACES_INTRO, 'hero-boutique',
        'Boutique shop unit with oak perimeter shelving (AI design concept)', inner, [('/spaces/', 'Spaces')])
    # guides
    inner = '<div class="head"><h2>Planning guides</h2><p>Practical reading before you speak to any contractor.</p></div><div class="grid g3">%s</div>' % ''.join(
        card('/guides/', p['path'], p['h1'], p['card'], p['image'], 'Read guide') for p in C_GDE.PAGES)
    hub('/guides/', 'Shop Fit-Out & Renovation Guides | R&C',
        'Original planning guides for Singapore shop and commercial fit-outs: briefing, shelving materials, counters, checklists, lighting and music.',
        'Planning guides for business spaces', 'Guides', C_GDE.GUIDES_INTRO, 'design-planning',
        'Shop floor plan with material samples on a table (AI design concept)', inner, [('/guides/', 'Guides')])


def build_concepts():
    path = '/design-concepts/'
    rows = []
    for c in C_SPC.CONCEPTS:
        chips = ''.join('<li><a href="%s">%s</a></li>' % (rel(path, s), E(SHORT.get(s, s))) for s in c['services'] if s in SHORT)
        rows.append('''<div class="concept rv" id="%s"><div class="pic">%s</div><div><span class="eyebrow">AI design concept · %s</span>
<h2>%s</h2><p>%s</p><ul>%s</ul><ul class="chips">%s</ul></div></div>''' % (
            E(c['slug']), pic(c['image'], c['title'] + ' (AI design concept)'), E(c['space'].title()), E(c['title']), E(c['summary']),
            ''.join('<li>%s</li>' % E(x) for x in c['elements']), chips))
    inner = '<div class="prose" style="max-width:none">%s</div>' % ''.join(rows)
    hub(path, 'Retail & Office Interior Design Concepts | R&C',
        'AI design concepts for small shops, office receptions, cafe counters, salons and showrooms: ideas to discuss, clearly labelled, not completed projects.',
        'Design concepts for retail and commercial spaces', 'Design concepts', C_SPC.CONCEPTS_INTRO, 'showroom',
        'Small showroom with oak display walls and a screen (AI design concept)', inner, [(path, 'Design concepts')],
        [{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': c['title'],
                                                     'url': abs_url(path) + '#' + c['slug']} for i, c in enumerate(C_SPC.CONCEPTS)]}])


# ---------- home ----------
HOME_FAQ = [
    ('What does SG Commercial Fitout do?', 'SG Commercial Fitout designs and builds retail and commercial spaces in Singapore: custom carpentry, renovation, '
     'electrical works, tiling and flooring, painting and finishing, and audio, visual and lighting (AVL) for shops, offices, F&B outlets and salons.'),
    ('Do you have your own carpentry workshop?', 'Yes. SG Commercial Fitout has its own carpentry workshop, so counters, cabinets and shelving can be '
     'made to your measurements. Photos of real work are on the Projects page.'),
    ('Are the photos real?', 'Photos marked "Real project" show SG Commercial Fitout carpentry; decor items in them were added with AI styling. '
     'Photos marked "AI design concept" are ideas to discuss, not completed work.'),
    ('What should I send to start?', 'WhatsApp a floor plan or unit layout, a few photos of the unit, what the space is for and your target opening date. '
     'Landlord or mall fit-out guidelines help too, if you have them.'),
]

PROCESS = [('WhatsApp us', 'Send your floor plan, unit photos, what the space is for and your target opening date.'),
           ('Site visit', 'We measure the unit and check existing services and landlord or mall rules.'),
           ('Scope & quotation', 'A written scope that shows what is included and what is not.'),
           ('Design', 'Layout, carpentry details, finishes, lighting and AVL positions agreed before work starts.'),
           ('Workshop & installation', 'Carpentry made in our workshop, then trades sequenced on site.'),
           ('Handover', 'Walk-through, defects list and the information you need to run the space.')]


def concept_line(c):
    s = [x.strip() for x in c['summary'].split('. ') if x.strip()]
    s = [x for x in s if not x.lower().startswith('an ai design concept')] or s
    return s[0].rstrip('.') + '.'


def real_fig(k, t, dsc):
    return '<figure class="real rv"><div class="ph">%s</div><figcaption><b>%s</b>%s</figcaption></figure>' % (
        real_pic(k, t + ' by SG Commercial Fitout'), E(t), E(dsc))


def workshop_block(path):
    if WORKSHOP:
        return '<div class="grid g3">%s</div>' % ''.join(
            '<figure class="real rv"><div class="ph"><img src="%s" width="640" height="480" alt="SG Commercial Fitout carpentry workshop" loading="lazy">'
            '<span class="tag tag-real">Our workshop</span></div></figure>' % (IMG + w) for w in WORKSHOP)
    if LIVE:
        return ''
    return '<div class="grid g3 ws-slots">%s</div>' % ''.join(
        '<div class="ws-slot"><span>Workshop photo %d</span><small>coming soon</small></div>' % i for i in (1, 2, 3))


HOME_TPL = '''<section class="lux lux-full">
<div class="lux-bg" aria-hidden="true">{dimg}</div><div class="lux-grad" aria-hidden="true"></div>
<div class="wrap lux-in">
<a class="lux-day" href="{dailyp}{ddate}/"><span class="lux-date">AI concept of the day &middot; {dnice}</span><span class="lux-title">{dtitle}</span><span class="lux-more">View the concept &rarr;</span></a>
<button type="button" class="lux-back" hidden>&larr; Back to today&rsquo;s concept</button>
</div><span class="tag lux-tag">AI design concept</span><span class="lux-scroll" aria-hidden="true"></span></section>

<section class="marq-band" aria-label="Past AI design concepts"><div class="wrap marq-head"><span>The archive</span><a href="{dailyp}">Browse the gallery &rarr;</a></div>
<div class="marq"><div class="marq-track">{marq}</div></div></section>

<section class="intro"><div class="wrap intro-in">
<div class="intro-l"><span class="eyebrow">Singapore retail &amp; commercial specialists</span>
<h1>Design &amp; Build for <em>Retail</em> and <em>Commercial</em> Spaces</h1></div>
<div class="intro-r"><p class="lede">We specialise in retail outlets and commercial spaces in Singapore: shops, offices, showrooms, F&amp;B outlets and salons. Carpentry, renovation, electrical, flooring and integrated audio, visual and lighting, made in our own workshop and coordinated by one contact.</p>
<div class="btns">{cta}<a class="btn btn-ghost" href="{services}">Explore Our Services</a></div></div>
</div>
<div class="wrap"><dl class="facts-line">{facts}</dl></div></section>

<section class="band sand"><div class="wrap">
<div class="head rv"><h2>Our carpentry workshop</h2><p>Counters, cabinets and shelving are made in our own workshop to your measurements, then installed on site.</p></div>
{workshop}</div></section>

<section class="band"><div class="wrap">
<div class="head rv"><h2>Our services</h2><p>One coordinated scope, or just the trade you need. Tap a service for the details.</p></div>
<div class="svc">{svcs}</div>
<p class="rv" style="margin-top:20px"><a href="{services}">All services and AVL &rarr;</a></p></div></section>

<section class="band sand"><div class="wrap">
<div class="head rv"><h2>Spaces we work on</h2><p>A boutique, an office reception, an F&amp;B counter and a salon station each need a different layout.</p></div>
<div class="grid g4">{spaces}</div></div></section>

<section class="band"><div class="wrap">
<div class="head rv"><h2>How it works</h2><p>Six simple steps, from your first WhatsApp to handover.</p></div>
<ol class="steps">{steps}</ol></div></section>

<section class="band dark"><div class="wrap avl">
<div class="pic rv">{avlpic}</div>
<div class="rv"><span class="eyebrow" style="color:var(--oak-l)">AVL: audio, visual and lighting</span>
<h2>Sound, screens and light, planned with the space</h2>
<p>Ceiling speakers, display screens and feature lighting need backing, power and cable routes. Planning them with the fit-out keeps them neat and avoids rework.</p>
<div class="trio">{trio}</div>
<div class="btns"><a class="btn btn-light" href="{avl}">Explore AVL</a></div></div>
</div></section>

<section class="band sand"><div class="wrap">
<div class="head rv"><h2>Planning guides</h2><p>Useful reading for shop owners and tenants.</p></div>
<div class="grid g3">{guides}</div>
<p class="rv" style="margin-top:20px"><a href="{guidesp}">All guides &rarr;</a></p></div></section>

<section class="band" id="enquire"><div class="wrap enq">
<div class="rv"><h2>Get a quote on WhatsApp</h2><p>Send what you already have. These four things are enough to start:</p>
<ul class="check"><li>Floor plan or unit layout</li><li>A few photos of the unit now</li><li>What the space is for</li><li>Your target opening date</li></ul></div>
<div class="panel rv"><h3>WhatsApp {phone}</h3><p>Tell us about your shop, office, F&amp;B outlet or salon and we'll discuss your scope.</p><div class="btns">{cta}</div></div>
</div></section>

<section class="band sand"><div class="wrap"><div class="faq" style="max-width:820px"><h2>Common questions</h2>{faqs}</div></div></section>
'''


def marquee(path, dp):
    items = [('%s%s/' % (dp, x['date']), daily_url(x, True), daily_url(x), x['alt'], 'AI concept of the day &middot; ' + nice_date(x['date']),
              nice_date(x['date']), x['title']) for x in DAILY[1:]]
    cp = rel(path, '/design-concepts/')
    items += [('%s#%s' % (cp, c['slug']), img_url(c['image'], True), img_url(c['image']), c['title'] + ' (AI design concept)',
               'AI design concept', 'Design concept', c['title']) for c in C_SPC.CONCEPTS]
    tpl = ('<a class="mq" href="%s" data-full="%s" data-alt="%s" data-label="%s" data-title="%s"{x}><img src="%s" width="640" height="480" '
           'alt="{alt}" loading="lazy" decoding="async"><span><small>%s</small>%s</span></a>')
    out = ['', '']
    for h, sm, full, alt, label, short, title in items:
        base = tpl % (h, full, E(alt), label, E(title), sm, E(short), E(title))
        out[0] += base.replace('{x}', '').replace('{alt}', E(alt))
        out[1] += base.replace('{x}', ' tabindex="-1" aria-hidden="true"').replace('{alt}', '')
    return out[0] + out[1]


def build_home():
    path = '/'
    d = DAILY[0]
    dp = rel(path, '/design-concepts/concept-of-the-day/')
    facts = [('What we do', 'Carpentry, renovation, electrical, flooring, painting and AVL'),
             ('Specialists in', 'Singapore retail outlets &amp; commercial spaces'),
             ('Workshop', 'Our own carpentry workshop'),
             ('Enquiries', 'WhatsApp <a href="%s" rel="noopener">%s</a>' % (E(wa_link('my space', path)), PHONE_DISPLAY))]
    body = HOME_TPL.format(
        cta=cta(path, 'my space', 'WhatsApp Us'), services=rel(path, '/services/'), dailyp=dp, ddate=d['date'],
        dimg='<img src="%s" srcset="%s 640w, %s 1024w" sizes="100vw" width="1024" height="1024" alt="%s" loading="eager" fetchpriority="high">' % (
            daily_url(d), daily_url(d, True), daily_url(d), E(d['alt'])),
        marq=marquee(path, dp),
        dnice=nice_date(d['date']), dtitle=E(d['title']),
        facts=''.join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in facts),
        real=''.join(real_fig(*r) for r in REAL), projects=rel(path, '/projects/'), workshop=workshop_block(path),
        svcs=''.join(svc_tile(path, s) for s in SERVICE_ORDER),
        spaces=''.join(card(path, p['path'], SHORT[p['path']], p['card'], p['image']) for p in C_SPC.PAGES),
        steps=''.join('<li class="rv"><strong>%s</strong><span>%s</span></li>' % (E(a), E(b)) for a, b in PROCESS),
        avlpic=pic('showroom', 'Showroom with a display screen, ceiling speakers and warm feature lighting (AI design concept)'),
        trio=''.join('<div><b>%s</b><span>%s</span></div>' % (E(t['title']), E(t['text'])) for t in C_AVL.AVL_TRIO), avl=rel(path, '/avl/'),
        guides=''.join(card(path, p['path'], p['h1'], p['card'], p['image'], 'Read guide') for p in C_GDE.PAGES[:3]),
        guidesp=rel(path, '/guides/'), phone=PHONE_DISPLAY,
        faqs=''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in HOME_FAQ))
    schema = [org_schema(), {'@type': 'WebSite', '@id': BASE + '#site', 'name': BRAND_FULL, 'url': BASE, 'publisher': {'@id': BASE + '#org'}},
              faq_schema(HOME_FAQ)]
    title = 'Singapore Retail & Commercial Design & Build | R&C'
    desc = 'Design and build specialists for Singapore retail outlets and commercial spaces: shops, offices, F&B and salons. Own carpentry workshop.'
    write(path, head(path, title, desc, schema, og_img=daily_url(d)) + header(path) + body + footer(path))


def build_projects():
    path = '/projects/'
    inner = ('<div class="head"><h2>Real projects</h2><p>%s</p></div><div class="grid g3">%s</div>'
             '<div class="head" style="margin-top:50px"><h2>Our carpentry workshop</h2><p>SG Commercial Fitout makes its carpentry in its own workshop, '
             'so counters, cabinets and shelving are built to the measurements taken on site.</p></div>%s%s') % (
        E(REAL_NOTE), ''.join(real_fig(*r) for r in REAL), workshop_block(path),
        '' if WORKSHOP else pending_box([('Workshop photos', 'real workshop photos are being added')], 'Coming soon'))
    crumbs = [(path, 'Projects & workshop')]
    schema = [org_schema(), crumbs_schema(crumbs), {'@type': 'CollectionPage', 'name': 'SG Commercial Fitout projects and workshop', 'url': abs_url(path)}]
    body = ('%s<section class="phead"><div class="wrap"><div><span class="eyebrow">Projects &amp; workshop</span>'
            '<h1>Our projects and carpentry workshop</h1><p class="answer">Built-in shelving, pantry counters, drawer units and wall cabinets made by '
            'SG Commercial Fitout in its own carpentry workshop, then installed on site.</p><div class="btns">%s</div></div>'
            '<div class="pic">%s</div></div></section><section class="band sand"><div class="wrap">%s</div></section>%s') % (
        crumbs_html(path, crumbs), cta(path, 'a carpentry project', 'WhatsApp Us'),
        real_pic('real-sink-counter', 'Sink counter with drawers by SG Commercial Fitout', eager=True), inner, cta_band(path, 'a carpentry project'))
    write(path, head(path, 'Carpentry Projects & Workshop | SG Commercial Fitout',
                     'Real carpentry by SG Commercial Fitout: built-in shelving, pantry counters, drawers and wall cabinets made in our own Singapore workshop.',
                     schema, og_img=img_url('real-sink-counter')) + header(path) + body + footer(path))


def daily_path(x):
    return '/design-concepts/concept-of-the-day/%s/' % x['date']


def build_daily():
    path = '/design-concepts/concept-of-the-day/'
    tiles = ''.join(
        ('<a class="al-tile" href="%s"><img src="%s" width="640" height="640" alt="%s" loading="%s" decoding="async">'
         '<span class="al-date">%s</span></a>') % (
            rel(path, daily_path(x)), daily_url(x, True), E(x['alt']), 'eager' if n < 9 else 'lazy', nice_date(x['date']))
        for n, x in enumerate(DAILY))
    tiles += ''.join(
        ('<a class="al-tile" href="%s#%s"><img src="%s" width="640" height="480" alt="%s (AI design concept)" loading="lazy" decoding="async">'
         '<span class="al-date">%s</span></a>') % (
            rel(path, '/design-concepts/'), c['slug'], img_url(c['image'], True), E(c['title']), E(c['space'].capitalize()))
        for c in C_SPC.CONCEPTS)
    crumbs = [('/design-concepts/', 'Design concepts'), (path, 'AI concept of the day')]
    schema = [org_schema(), crumbs_schema(crumbs),
              {'@type': 'ImageGallery', 'name': 'AI concept of the day', 'url': abs_url(path),
               'associatedMedia': [{'@type': 'ImageObject', 'contentUrl': daily_url(x), 'url': abs_url(daily_path(x)), 'name': x['title'],
                                    'uploadDate': x['date'], 'description': x['summary']} for x in DAILY]}]
    body = ('%s<section class="al-head"><div class="wrap"><span class="eyebrow">Gallery &middot; %d concepts</span>'
            '<h1>AI concept of the day</h1><p>A new AI interior idea for a Singapore shop, office, F&amp;B outlet or salon every day. '
            'Tap a picture to see the details. These are ideas to discuss, not completed projects.</p></div></section>'
            '<section class="album"><div class="wrap al-wrap"><div class="al-grid">%s</div></div></section>%s') % (
        crumbs_html(path, crumbs), len(DAILY) + len(C_SPC.CONCEPTS), tiles, cta_band(path, 'an idea from the concept of the day'))
    write(path, head(path, 'AI Interior Concept of the Day | SG Commercial Fitout',
                     'A dated daily AI interior concept for Singapore shops, offices, F&B outlets and salons. Browse every past concept as a photo album.',
                     schema, og_img=daily_url(DAILY[0])) + header(path) + body + footer(path), DAILY[0]['date'])
    for n, x in enumerate(DAILY):
        build_daily_one(x, DAILY[n - 1] if n else None, DAILY[n + 1] if n + 1 < len(DAILY) else None)


def build_daily_one(x, newer, older):
    path = daily_path(x)
    gp = '/design-concepts/concept-of-the-day/'
    crumbs = [('/design-concepts/', 'Design concepts'), (gp, 'AI concept of the day'), (path, nice_date(x['date']))]
    schema = [org_schema(), crumbs_schema(crumbs),
              {'@type': 'ImageObject', 'contentUrl': daily_url(x), 'url': abs_url(path), 'name': x['title'], 'caption': x['alt'],
               'description': x['summary'], 'uploadDate': x['date'], 'creditText': 'AI design concept by SG Commercial Fitout',
               'copyrightNotice': 'SG Commercial Fitout', 'creator': {'@type': 'Organization', 'name': BRAND}}]
    def nav(o, cls, label):
        if not o:
            return '<span class="cn-%s cn-off"></span>' % cls
        return '<a class="cn-%s" href="%s"><small>%s</small>%s</a>' % (cls, rel(path, daily_path(o)), label, E(o['title']))
    body = ('%s<section class="cdet"><div class="wrap cdet-in">'
            '<div class="cdet-pic"><img src="%s" srcset="%s 640w, %s 1024w" sizes="(max-width: 900px) 100vw, 56vw" width="1024" height="1024" '
            'alt="%s" fetchpriority="high"><span class="tag">AI design concept</span></div>'
            '<div class="cdet-txt"><a class="cdet-back" href="%s">&larr; All concepts</a>'
            '<span class="eyebrow">%s &middot; %s</span><h1>%s</h1><p class="answer">%s</p>'
            '<h2>Design ideas in this concept</h2><ul>%s</ul>'
            '<p class="cdet-note">This is an AI-generated design idea, not a completed project. We can adapt it to your unit, brand and budget.</p>'
            '<div class="btns">%s</div></div></div>'
            '<div class="wrap cnav">%s%s</div></section>%s') % (
        crumbs_html(path, crumbs), daily_url(x), daily_url(x, True), daily_url(x), E(x['alt']), rel(path, gp),
        nice_date(x['date']), E(x['space']), E(x['title']), E(x['summary']), ''.join('<li>%s</li>' % E(i) for i in x['ideas']),
        cta(path, 'this AI concept (%s)' % nice_date(x['date']), 'WhatsApp about this idea'),
        nav(newer, 'new', '&larr; Newer'), nav(older, 'old', 'Older &rarr;'), cta_band(path, 'an idea from the concept of the day'))
    title = '%s | AI Concept' % x['title']
    if len(title) > 60:
        title = x['title'][:60]
    write(path, head(path, title, ('AI interior concept for %s, %s: %s' % (x['space'].lower(), nice_date(x['date']), concept_line(x)))[:158],
                     schema, og_img=daily_url(x)) + header(path) + body + footer(path), x['date'])


# ---------- about / contact / privacy / 404 ----------
def simple(path, title, desc, h1, kicker, answer, prose, crumbs, key=None, alt='', schema_extra=None):
    schema = [org_schema(), crumbs_schema(crumbs)] + (schema_extra or [])
    picture = '<div class="pic">%s</div>' % pic(key, alt, eager=True) if key else ''
    body = '''%s
<section class="phead"><div class="wrap"%s>
<div><span class="eyebrow">%s</span><h1>%s</h1><p class="answer">%s</p></div>%s</div></section>
<div class="wrap" style="padding-bottom:30px"><article class="prose">%s</article></div>
%s''' % (crumbs_html(path, crumbs), '' if key else ' style="grid-template-columns:1fr"', E(kicker), E(h1), E(answer), picture,
         fix_links(prose, path), cta_band(path, 'my space') if path != '/contact/' else '')
    write(path, head(path, title, desc, schema) + header(path) + body + footer(path))


def build_static():
    about = '''<h2>Who we are</h2>
<p>SG Commercial Fitout is a Singapore design and build company that specialises in retail outlets and commercial spaces: shops and boutiques, offices and showrooms, F&amp;B outlets and service counters, and salons and beauty studios. We have our own carpentry workshop, so counters, cabinets and shelving are made to the measurements taken on site.</p>
<h2>What we cover</h2>
<ul><li><a href="/retail-commercial-design-build/">Design &amp; build</a>: one point of contact from brief to handover.</li>
<li><a href="/services/commercial-carpentry/">Carpentry</a>: counters, shelving, storage, display fixtures and reception joinery, made in our workshop.</li>
<li><a href="/services/commercial-renovation/">Renovation</a>, <a href="/services/commercial-electrical-works/">electrical works</a>, <a href="/services/commercial-tiling-flooring/">tiling and flooring</a>, and <a href="/services/commercial-painting-finishing/">painting and finishing</a>.</li>
<li><a href="/avl/">AVL</a>: audio, visual and lighting planned with the space.</li></ul>
<h2>Our work and our photos</h2>
<p>See <a href="/projects/">our projects and workshop</a>. Photos marked "Real project" show our own carpentry; decor items in them were added with AI styling. Photos marked "AI design concept" are ideas to discuss, not completed work. We do not publish reviews, client names or figures we cannot back up.</p>
<h2>Contact</h2>
<p>Address: %s. WhatsApp <a href="%s" rel="noopener">%s</a>. We serve businesses in Singapore.</p>
%s''' % (ADDR_TEXT, E(wa_link('my space', '/about/')), PHONE_DISPLAY, pending_box([('Operating company', 'registered name and UEN to be confirmed')]))
    simple('/about/', 'About SG Commercial Fitout | Design & Build Singapore', 'About SG Commercial Fitout: Singapore design and build for shops, offices, F&B outlets and salons, with our own carpentry workshop.',
           'About SG Commercial Fitout', 'About', 'SG Commercial Fitout is a Singapore design and build company for shops, offices, showrooms, F&B outlets and salons. It has its own carpentry workshop and covers carpentry, renovation, electrical, flooring, painting and AVL.',
           about, [('/about/', 'About')], 'design-planning', 'Floor plan and material samples on a planning table (AI design concept)',
           [{'@type': 'AboutPage', 'name': 'About SG Commercial Fitout', 'url': abs_url('/about/')}])
    w = wa_link('my space', '/contact/')
    contact = '''<h2>WhatsApp us</h2>
<p>The fastest way to start is a WhatsApp message to <strong>%s</strong> with what you already have about the unit and the business.</p>
<p><a class="btn btn-main" href="%s" rel="noopener">%sWhatsApp %s</a></p>
<h2>Address</h2>
<p>%s.</p>
<h2>What to send</h2>
<ol><li><strong>Floor plan or unit layout</strong>, from the landlord, mall or previous tenant if you have one.</li>
<li><strong>Photos of the unit</strong> as it is now: shopfront, each wall, ceiling and floor.</li>
<li><strong>What the space is for</strong>: what you sell or do there, how many staff, what customers do in the space.</li>
<li><strong>Target opening date</strong>, plus any handover or fit-out period in your lease.</li>
<li><strong>Landlord or mall fit-out guidelines</strong>, if you have them.</li>
<li><strong>Priorities</strong>: what must be right on day one, and what can wait.</li></ol>
<p class="note">Not sure where to begin? Read <a href="/guides/how-to-brief-a-shop-fit-out/">how to brief a shop fit-out</a> first.</p>''' % (PHONE_DISPLAY, E(w), WA_SVG, PHONE_DISPLAY, ADDR_TEXT)
    simple('/contact/', 'Contact SG Commercial Fitout | WhatsApp +65 8659 4553', 'WhatsApp SG Commercial Fitout at +65 8659 4553 about your shop, office, F&B or salon space. Send your floor plan, unit photos and opening date.',
           'Contact us', 'Contact', 'WhatsApp SG Commercial Fitout at +65 8659 4553. Send a floor plan, a few photos of the unit, what the space is for and your target opening date, and we will discuss your scope.',
           contact, [('/contact/', 'Contact')], 'office-reception', 'Office reception with a curved oak counter (AI design concept)',
           [{'@type': 'ContactPage', 'name': 'Contact SG Commercial Fitout', 'url': abs_url('/contact/')}])
    privacy = '''<p>Last updated 24 October 2026.</p>
<h2>What this website collects</h2>
<p>This website has no forms and sets no advertising cookies. When you tap a WhatsApp button, an anonymous count is recorded (the page you were on, whether you used a phone or computer, and the referring site) so we can see which pages help visitors. It does not record your name, number or the message you send.</p>
<h2>Messages you send</h2>
<p>If you contact SG Commercial Fitout, the details you choose to share (such as your name, number, floor plan and photos) are used only to respond to your enquiry and discuss your project, in line with Singapore's Personal Data Protection Act. They are not sold or shared for marketing.</p>
<h2>Third-party services</h2>
<p>WhatsApp messages are handled by WhatsApp under its own privacy policy. Fonts and scripts on this site are served from this website.</p>
<h2>Access, correction and questions</h2>
<p>You may ask to see, correct or delete personal data you have shared with SG Commercial Fitout.</p>
%s''' % pending_box([('Data protection contact', 'to be published with the operating company details')])
    simple('/privacy-policy/', 'Privacy Policy | SG Commercial Fitout', 'How the SG Commercial Fitout website handles personal data: no forms, an anonymous WhatsApp tap count, and how enquiry details are used.',
           'Privacy policy', 'Privacy', 'This website has no forms and no advertising cookies. It records only an anonymous count of WhatsApp button taps. Details you send when you contact SG Commercial Fitout are used only to answer your enquiry.',
           privacy, [('/privacy-policy/', 'Privacy policy')])


def build_404():
    path = '/404/'
    r = '/preview/%s/' % SLUG if not DOMAIN else '/'
    doc = head('/', 'Page not found | SG Commercial Fitout', 'This page does not exist.', [org_schema()]).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    # 404 is served at any depth, so use root-absolute links
    doc = re.sub(r'(href|src)="(?:\./|(?:\.\./)*)((?:favicon|icon-|apple-|site\.web|fonts/|rc\.css)[^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), r, m.group(2)), doc)
    hdr = header('/').replace('href="./"', 'href="%s"' % r)
    hdr = re.sub(r'(href|src)="((?!https?:|#)[^"]+)"', lambda m: '%s="%s%s"' % (m.group(1), r, m.group(2).lstrip('./')) if not m.group(2).startswith('/') else m.group(0), hdr)
    body = '''<section class="phead"><div class="wrap" style="grid-template-columns:1fr"><div><span class="eyebrow">404</span><h1>That page isn't here</h1>
<p class="answer">The link may be old or mistyped. Try one of these instead.</p>
<div class="btns"><a class="btn btn-main" href="%s">Home</a><a class="btn btn-ghost" href="%sservices/">Services</a><a class="btn btn-ghost" href="%scontact/">Contact</a></div></div></div></section>''' % (r, r, r)
    ftr = footer('/')
    ftr = re.sub(r'(href|src)="((?!https?:|#)[^"]+)"', lambda m: '%s="%s%s"' % (m.group(1), r, m.group(2).lstrip('./')) if not m.group(2).startswith('/') else m.group(0), ftr)
    with open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(doc + hdr + body + ftr)


# ---------- machine files ----------
def build_machine():
    urls = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>' % (E(abs_url(p)), LASTMOD_OVERRIDE.get(p, m)) for p, m in sorted(PAGES_OUT))
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
    bots = ['Googlebot', 'Googlebot-Image', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot',
            'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
    rb = ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots)
    rb += 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BASE
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(rb)
    lines = ['# %s' % BRAND_FULL, '', '> %s' % TAGLINE, '',
             'SG Commercial Fitout is a Singapore design and build company that specialises in retail outlets and commercial spaces, with its own carpentry workshop: shops and boutiques, offices and showrooms, '
             'cafes and service counters, salons and beauty studios. Services: integrated design and build, commercial carpentry, '
             'renovation, electrical works, tiling and flooring, painting and finishing, and audio, visual and lighting (AVL).',
             '', 'Address: %s. Contact: WhatsApp %s. Photos marked Real project show its own carpentry (decor added with AI styling); AI design concept images are ideas, not completed work.' % (ADDR_TEXT, PHONE_DISPLAY), '']
    sections = [('Services', SERVICE_ORDER), ('AVL', [p['path'] for p in C_AVL.PAGES]), ('Spaces', [p['path'] for p in C_SPC.PAGES]),
                ('Guides', [p['path'] for p in C_GDE.PAGES])]
    for name, paths in sections:
        lines.append('## %s' % name)
        for pth in paths:
            p = ALL_CONTENT[pth]
            lines.append('- [%s](%s): %s' % (p['h1'], abs_url(pth), p['card']))
        lines.append('')
    lines += ['## Other', '- [Design concepts](%s): AI design concepts, clearly labelled.' % abs_url('/design-concepts/'),
              '- [Projects & workshop](%s)' % abs_url('/projects/'), '- [AI concept of the day](%s)' % abs_url('/design-concepts/concept-of-the-day/'), '- [About](%s)' % abs_url('/about/'), '- [Contact](%s)' % abs_url('/contact/'), '']
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('\n'.join(lines))
    with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f:
        f.write(INDEXNOW_KEY)
    man = {'name': BRAND_FULL, 'short_name': 'SG Commercial Fitout', 'start_url': './', 'display': 'browser', 'background_color': '#fbf8f2',
           'theme_color': '#2b2925', 'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                               {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump(man, f)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name in ('rc.css', 'rc.js', 'wa-tap-counter.js'):
        shutil.copy(os.path.join(HERE, name), OUT)
    shutil.copytree(os.path.join(HERE, 'fonts'), os.path.join(OUT, 'fonts'))
    for name in ('favicon.ico', 'favicon-48.png', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'):
        shutil.copy(os.path.join(HERE, 'icons', name), OUT)
    os.makedirs(os.path.join(OUT, 'icons'), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'icons', 'logo-full-light.png'), os.path.join(OUT, 'icons'))
    for n in ('mark-96.png', 'logo-header.png', 'logo-sgcf-light.png'):
        shutil.copy(os.path.join(HERE, 'icons', n), os.path.join(OUT, 'icons'))
    build_home()
    build_hubs()
    build_concepts()
    build_projects()
    build_daily()
    for p in C_SVC.PAGES:
        cr = [(p['path'], SHORT[p['path']])] if p['path'] == '/retail-commercial-design-build/' else [('/services/', 'Services'), (p['path'], SHORT[p['path']])]
        content_page(p, cr)
    for p in C_AVL.PAGES:
        cr = [('/avl/', 'AVL')] if p['path'] == '/avl/' else [('/avl/', 'AVL'), (p['path'], SHORT[p['path']])]
        content_page(p, cr)
    for p in C_SPC.PAGES:
        content_page(p, [('/spaces/', 'Spaces'), (p['path'], SHORT[p['path']])])
    for p in C_GDE.PAGES:
        content_page(p, [('/guides/', 'Guides'), (p['path'], p['h1'])], kind='guide')
    build_static()
    build_404()
    build_machine()
    print('built %d pages into %s' % (len(PAGES_OUT), OUT))


if __name__ == '__main__':
    main()

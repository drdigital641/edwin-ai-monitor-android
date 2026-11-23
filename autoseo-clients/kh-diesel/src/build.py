#!/usr/bin/env python3
"""KH Diesel Fuel Pump preview build (AutoSEO.my, 23 Nov 2026).

One-time NEW-SITE build into an empty folder. After the first upload, Rule 0 applies: change live files with
read_live -> edit -> write (expected_sha256); never rerun this over the live folder without Edwin's OK.

Shared template parts used: autoseo-template/golive/golive.py (one-switch config: canonical, hreflang, OG, sitemap,
robots, llms), autoseo-template/autoseo_i18n.py (EN/BM/中文 switch, privacy path + footer link + checks),
autoseo-template/privacy/privacy_page.py (privacy text, PDPA 2010), autoseo-template/reviews.py (no-rating gate),
p1-cta.js v4 tracker (AutoSEO live copy). Site parts in this file: head(), header(), footer(), mbar(), cta_row(),
area_template(), service_template(), schema(). Every page reads facts.json; copy comes from content_<lang>.json
(EN written once; MS/ZH from the cheap translation step, Rule 6).

All internal links and assets are PAGE-RELATIVE, because the same folder is served at
https://autoseo.my/preview/kh-diesel/ and at https://khdieselfuelpump.my/ (shared docroot).
"""
import hashlib, html, json, os, re, shutil, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
T = '/mnt/project-files/autoseo-template'
sys.path[:0] = [T, T + '/golive', T + '/privacy']
import autoseo_i18n as I18N, golive, privacy_page as PV, reviews as RV

OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/site'
CFG = golive.load(os.path.join(HERE, 'site.json'))
F = json.load(open(os.path.join(HERE, 'facts.json')))
C = {L: json.load(open(os.path.join(HERE, f'content_{L}.json'))) for L in ('en', 'ms', 'zh')}
E = html.escape
UPDATED_ISO = '2026-11-23'

SERVICES = [s['id'] for s in C['en']['services']]
AREAS = [a['id'] for a in C['en']['areas']]
# page id -> English site path
PAGES = {'home': ''}
PAGES.update({s: s + '/' for s in SERVICES})
PAGES['vehicles-and-machines'] = 'vehicles-and-machines/'
PAGES.update({a: 'areas/' + a + '/' for a in AREAS})
PAGES.update({'about': 'about/', 'contact': 'contact/', 'articles': 'articles/', 'privacy': I18N.PRIVACY_PATH})

MAN = {}
for x in ['h01-cleanroom-pump-bench-16x9', 'h02-workshop-exterior-yard-16x9']:
    MAN[x] = 'hero'
GAL = ['g01-cleanroom-pump-bench', 'g02-common-rail-test-room', 'g03-pump-parts-on-bench', 'g04-turbo-rebuild-bench',
       'g05-workshop-front-canopy', 'g06-heavy-engine-workshop', 'g07-pickups-laterite-hill', 'g08-lorries-in-yard',
       'g09-coach-bus-in-bay', 'g10-hands-calibrating-pump']
MANIFEST = json.load(open(os.path.join(HERE, 'media-manifest.json')))
ALT = {m['id']: m['alt'] for m in MANIFEST['hero'] + MANIFEST['gallery']}
CAP = {m['id']: m['caption'] for m in MANIFEST['hero'] + MANIFEST['gallery']}
# Captions/alts are English in the manifest; MS/ZH captions come from content ui.ill_caps when present.

HERO_OF = {'home': 'h01', 'diesel-fuel-pump-repair-bintulu': 'h01', 'common-rail-pump-repair-bintulu': 'h01',
           'injector-repair-bintulu': 'h01', 'fuel-system-diagnosis-bintulu': 'h01', 'turbo-repair-bintulu': 'h02',
           'vehicles-and-machines': 'h02', 'about': 'h02', 'contact': 'h02', 'articles': 'h01',
           'kidurong-bintulu-port': 'h02', 'kemena-sibiyu-nyabau': 'h02', 'bintulu-town-jepak': 'h02'}
HERO_ID = {'h01': 'h01-cleanroom-pump-bench-16x9', 'h02': 'h02-workshop-exterior-yard-16x9'}
SVC_IMGS = {'diesel-fuel-pump-repair-bintulu': ['g01-cleanroom-pump-bench', 'g10-hands-calibrating-pump', 'g03-pump-parts-on-bench'],
            'common-rail-pump-repair-bintulu': ['g02-common-rail-test-room', 'g03-pump-parts-on-bench'],
            'injector-repair-bintulu': ['g02-common-rail-test-room', 'g10-hands-calibrating-pump'],
            'turbo-repair-bintulu': ['g04-turbo-rebuild-bench', 'g06-heavy-engine-workshop'],
            'fuel-system-diagnosis-bintulu': ['g10-hands-calibrating-pump', 'g01-cleanroom-pump-bench', 'g02-common-rail-test-room']}
AREA_IMG = {'kidurong-bintulu-port': ['g08-lorries-in-yard', 'g06-heavy-engine-workshop'],
            'kemena-sibiyu-nyabau': ['g05-workshop-front-canopy', 'g07-pickups-laterite-hill'],
            'bintulu-town-jepak': ['g07-pickups-laterite-hill', 'g05-workshop-front-canopy']}
SLUG_REF = {'diesel-fuel-pump-repair-bintulu': 'pump', 'common-rail-pump-repair-bintulu': 'commonrail',
            'injector-repair-bintulu': 'injector', 'turbo-repair-bintulu': 'turbo', 'fuel-system-diagnosis-bintulu': 'diagnosis',
            'kidurong-bintulu-port': 'kidurong', 'kemena-sibiyu-nyabau': 'kemena', 'bintulu-town-jepak': 'town'}

ASSET_V = {}


def vhash(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


class Page:
    def __init__(self, pid, L):
        self.pid, self.L = pid, L
        self.en_path = PAGES[pid]
        self.path = I18N.page_path(I18N.lang(L), self.en_path)
        self.depth = self.path.count('/')
        self.c = C[L]
        self.ui = C[L]['ui']
        self.p = C[L]['pages'].get(pid, {})

    def u(self, target):
        """page-relative href to a site path ('' = home)."""
        pre = '../' * self.depth
        return (pre + target) or './'

    def lp(self, pid):
        return self.u(I18N.page_path(I18N.lang(self.L), PAGES[pid]))


def wa(pg, key=None, ref='x'):
    msg = pg.c['wa_msgs'].get(key or pg.pid) or pg.c['wa_msgs']['home']
    href = f"https://wa.me/{F['whatsapp']['wa']}?text={urllib.parse.quote(msg)}"
    return f'href="{E(href)}" target="_blank" rel="noopener" data-cta="{ref}" data-ref="{ref}"'


def tel(ref, landline=False):
    n = F['landline']['e164'] if landline else F['mobile']['e164']
    return f'href="tel:{n}" data-cta="{ref}" data-ref="{ref}"'


ICON = {
    'wa': '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>',
    'call': '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 7 7L16 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
    'pin': '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    'star': '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 3l2.7 5.6 6.1.8-4.4 4.3 1 6.1L12 17l-5.4 2.8 1-6.1L3.2 9.4l6.1-.8z"/></svg>',
    'phone': '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="4" y="3" width="16" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 7h8M8 11h8M8 15h4" stroke="currentColor" stroke-width="2"/></svg>',
}


def cta_row(pg, place, cls=''):
    svc = place
    return (f'<div class="ctas {cls}"><a class="btn wa" {wa(pg, ref=f"whatsapp_{svc}")}>{ICON["wa"]}<span>{E(pg.ui["wa"])}</span></a>'
            f'<a class="btn call" {tel(f"call_{svc}")}>{ICON["call"]}<span>{E(pg.ui["call"])}</span></a></div>')


def img(pg, mid, sizes, w, h, cls='', eager=False, kind='gallery'):
    base = f'images/{kind}/{mid}'
    ws = (480, 800, 1600) if kind == 'hero' else (480, 800)
    srcset = ', '.join(f'{pg.u(base + "-" + str(x) + ".webp")} {x}w' for x in ws)
    src = pg.u(f'{base}-800.webp')
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    alt = pg.ui.get('alts', {}).get(mid) or ALT[mid]
    return f'<img class="{cls}" src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{E(alt)}" {load}>'


def cap(pg, mid):
    return pg.ui.get('caps', {}).get(mid) or CAP[mid]


def figure(pg, mid, cls='fig'):
    return (f'<figure class="{cls}">{img(pg, mid, "(min-width: 900px) 360px, 80vw", 800, 1000)}'
            f'<figcaption><span>{E(cap(pg, mid))}</span><small>{E(pg.ui["ill_credit"])}</small></figcaption></figure>')


# ---------------------------------------------------------------- schema
def schema(pg, extra):
    canon = CFG.canon
    biz = {
        '@type': 'AutoRepair', '@id': golive.jsonld_id(CFG), 'name': F['name'],
        'url': CFG.canonical_base, 'image': CFG.og_image(), 'logo': CFG.canon('images/brand/kh-badge-512.png'),
        'telephone': [F['mobile']['e164'], F['landline']['e164']],
        'address': {'@type': 'PostalAddress', 'streetAddress': F['address']['street'], 'addressLocality': F['address']['locality'],
                    'addressRegion': F['address']['region'], 'postalCode': F['address']['postcode'], 'addressCountry': 'MY'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': F['maps_url'], 'sameAs': [F['maps_url']],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                                       'opens': '08:00', 'closes': '17:30'}],
        'areaServed': [{'@type': 'City', 'name': 'Bintulu', 'containedInPlace': {'@type': 'State', 'name': 'Sarawak'}}]
        + [{'@type': 'Place', 'name': n} for n in ['Kidurong Light Industrial', 'Bintulu Port', 'Tanjung Kidurong', 'Kemena Industrial Estate',
                                                    'Sibiyu', 'Jalan Nyabau', 'Batu 10', 'Bintulu town', '2½ Mile Light Industrial', 'Assyakirin', 'Tanjung Batu', 'Jepak']],
        'knowsAbout': ['Diesel fuel pump repair', 'Common rail pump repair', 'Diesel injector testing', 'Turbocharger repair', 'Diesel fuel system diagnosis'],
        'contactPoint': {'@type': 'ContactPoint', 'telephone': F['mobile']['e164'], 'contactType': 'customer service',
                         'availableLanguage': ['en', 'ms', 'zh']},
        'founder': None,
    }
    biz.pop('founder')
    if F['flags']['show_owner_name']:
        biz['employee'] = {'@type': 'Person', 'name': F['owner'], 'jobTitle': 'Owner'}
    url = canon(pg.path)
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': pg.ui['breadcrumb_home'], 'item': canon(I18N.page_path(I18N.lang(pg.L), ''))}]
    if pg.pid != 'home':
        crumbs.append({'@type': 'ListItem', 'position': len(crumbs) + 1, 'name': pg.p.get('h1') or pg.p.get('title'), 'item': url})
    graph = [biz,
             {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': pg.p['title'], 'inLanguage': I18N.lang(pg.L)['hreflang'],
              'about': {'@id': golive.jsonld_id(CFG)}, 'dateModified': UPDATED_ISO},
             {'@type': 'BreadcrumbList', '@id': url + '#crumbs', 'itemListElement': crumbs}]
    graph += extra
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/') + '</script>'


def faq_schema(pg, faqs):
    return {'@type': 'FAQPage', '@id': CFG.canon(pg.path) + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}


def service_schema(pg):
    return {'@type': 'Service', '@id': CFG.canon(pg.path) + '#service', 'name': pg.p['h1'], 'serviceType': C['en']['pages'][pg.pid]['h1'],
            'provider': {'@id': golive.jsonld_id(CFG)}, 'areaServed': {'@type': 'City', 'name': 'Bintulu'}, 'url': CFG.canon(pg.path),
            'description': pg.p['desc']}


# ---------------------------------------------------------------- shared partials
def head(pg, ld):
    p = pg.p
    css = pg.u('assets/site.css') + '?v=' + ASSET_V['site.css']
    h01 = pg.u('images/hero/' + HERO_ID[HERO_OF.get(pg.pid, 'h01')] + '-800.webp')
    zh_font = '' if pg.L != 'zh' else ''
    return f'''<!doctype html>
<html lang="{I18N.lang(pg.L)['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(p['title'])}</title>
<meta name="description" content="{E(p['desc'])}">
{golive.head_tags(CFG, pg.en_path, pg.L)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F['name'])}">
<meta property="og:title" content="{E(p['title'])}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:image:alt" content="{E(MANIFEST['og']['alt'])}">
{I18N.og_locale_tags(I18N.lang(pg.L))}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(p['title'])}">
<meta name="twitter:description" content="{E(p['desc'])}">
<meta name="theme-color" content="#1E3A6E">
<link rel="icon" href="{pg.u('images/brand/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{pg.u('images/brand/apple-touch-icon.png')}">
<link rel="preload" href="{pg.u('assets/fonts/saira-condensed-800.woff2')}" as="font" type="font/woff2" crossorigin>
{'<link rel="preload" as="image" href="' + h01 + '" fetchpriority="high">' if pg.pid != 'privacy' else ''}
<link rel="stylesheet" href="{css}">
{ld}
</head>
<body class="lang-{pg.L} pg-{pg.pid if pg.pid in ('home','privacy','contact','about','articles','vehicles-and-machines') else ('area' if pg.pid in AREAS else 'svc')}">
<a class="skip" href="#main">{E(pg.ui['skip'])}</a>'''


def wordmark(pg):
    return (f'<a class="wm" href="{pg.lp("home")}" aria-label="{E(F["name"])}"><span class="wm-kh" aria-hidden="true"><b>K</b><i>H</i></span>'
            f'<span class="wm-t">DIESEL FUEL PUMP<small>Batu 10 · Bintulu</small></span></a>')


def nav_links(pg):
    items = [('nav_services', 'diesel-fuel-pump-repair-bintulu'), ('nav_vehicles', 'vehicles-and-machines'), ('nav_about', 'about'),
             ('nav_articles', 'articles'), ('nav_contact', 'contact')]
    return ''.join(f'<a href="{pg.lp(pid)}"{" aria-current=\"page\"" if pid == pg.pid else ""}>{E(pg.ui[k])}</a>' for k, pid in items)


def header(pg):
    sw = I18N.switcher(pg.u, pg.en_path, I18N.lang(pg.L), pg.ui['lang_label'], cls='lang')
    svc_links = ''.join(f'<a href="{pg.lp(s["id"])}">{E(s["short"])}</a>' for s in pg.c['services'])
    area_links = ''.join(f'<a href="{pg.lp(a["id"])}">{E(a["name"])}</a>' for a in pg.c['areas'])
    return f'''<header class="hd"><div class="wrap hd-in">
{wordmark(pg)}
<nav class="nav" aria-label="Main">{nav_links(pg)}</nav>
{sw}
<a class="hd-wa" {wa(pg, ref='whatsapp_header')}>{ICON['wa']}<span>{E(pg.ui['wa'])}</span></a>
<details class="sheet"><summary aria-label="{E(pg.ui['menu'])}"><span class="bars" aria-hidden="true"></span><span class="sr">{E(pg.ui['menu'])}</span></summary>
<div class="sheet-in">
<p class="sheet-h">{E(pg.ui['services_h'])}</p><div class="sheet-l">{svc_links}<a href="{pg.lp('vehicles-and-machines')}">{E(pg.ui['nav_vehicles'])}</a></div>
<p class="sheet-h">{E(pg.ui['areas_h'])}</p><div class="sheet-l">{area_links}</div>
<div class="sheet-l sheet-row"><a href="{pg.lp('home')}">{E(pg.ui['nav_home'])}</a><a href="{pg.lp('about')}">{E(pg.ui['nav_about'])}</a><a href="{pg.lp('articles')}">{E(pg.ui['nav_articles'])}</a><a href="{pg.lp('contact')}">{E(pg.ui['nav_contact'])}</a></div>
{I18N.switcher(pg.u, pg.en_path, I18N.lang(pg.L), pg.ui['lang_label'], cls='lang lang-sheet')}
<div class="ctas"><a class="btn wa" {wa(pg, ref='whatsapp_menu')}>{ICON['wa']}<span>{E(pg.ui['wa'])}</span></a><a class="btn call" {tel('call_header')}>{ICON['call']}<span>{E(pg.ui['call'])}</span></a></div>
</div></details>
</div><div class="gate" aria-hidden="true"></div></header>'''


def hours_table(pg, cls='hrs'):
    return (f'<table class="{cls}"><tbody><tr><th scope="row">{E(pg.ui["hours_week"])}</th><td>{E(pg.ui["hours_time"])}</td></tr>'
            f'<tr class="off"><th scope="row">{E(pg.ui["hours_sun"])}</th><td>{E(pg.ui["hours_closed"])}</td></tr></tbody></table>'
            f'<p class="tz">{E(pg.ui["hours_tz"])}</p>')


def footer(pg):
    svc = ''.join(f'<li><a href="{pg.lp(s["id"])}">{E(s["short"])}</a></li>' for s in pg.c['services'])
    areas = ''.join(f'<li><a href="{pg.lp(a["id"])}">{E(a["name"])}</a></li>' for a in pg.c['areas'])
    return f'''<footer class="ft"><div class="gate" aria-hidden="true"></div><div class="wrap">
<div class="ft-g">
<div class="ft-id">{wordmark(pg)}
<p class="ft-name">{E(F['name'])}</p>
<address>{E(F['address']['display'])}</address>
<p class="ft-ill">{E(pg.ui['ill_note'])}</p></div>
<div><h2>{E(pg.ui['hours_h'])}</h2>{hours_table(pg, 'hrs ft-hrs')}</div>
<div><h2>{E(pg.ui['talk_h'])}</h2><ul class="ft-l">
<li><a {wa(pg, ref='whatsapp_footer')}>{ICON['wa']}<span>{E(pg.ui['wa_long'])}</span></a></li>
<li><a {tel('call_footer')}>{ICON['call']}<span>{E(pg.ui['call_long'])}</span></a></li>
<li><a {tel('call_landline_footer', True)}>{ICON['phone']}<span>{E(pg.ui['landline'])}</span></a></li>
<li><a href="{E(F['maps_url'])}" target="_blank" rel="noopener" data-cta="map_footer" data-ref="map_footer">{ICON['pin']}<span>{E(pg.ui['open_maps'])}</span></a></li>
</ul></div>
<div><h2>{E(pg.ui['services_h'])}</h2><ul class="ft-s">{svc}</ul><h2>{E(pg.ui['areas_h'])}</h2><ul class="ft-s">{areas}</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(F['name'])}</span><a href="{pg.lp('about')}">{E(pg.ui['nav_about'])}</a><a href="{pg.lp('articles')}">{E(pg.ui['nav_articles'])}</a>{I18N.privacy_link(pg.u, I18N.lang(pg.L))}<a href="https://autoseo.my/">{E(pg.ui['credit'])}</a></div>
</div></footer>
<div class="mbar"><a class="btn wa" {wa(pg, ref='whatsapp_mobile_bar')}>{ICON['wa']}<span>{E(pg.ui['wa'])}</span></a><a class="btn call" {tel('call_mobile_bar')}>{ICON['call']}<span>{E(pg.ui['call'])}</span></a></div>
<script src="{pg.u('assets/site.js')}?v={ASSET_V['site.js']}" defer></script>
<script src="{pg.u('p1-cta.js')}?v={ASSET_V['p1-cta.js']}" defer></script>
</body>
</html>
'''


def hero(pg, h1, sub=None, place='hero'):
    hid = HERO_ID[HERO_OF.get(pg.pid, 'h01')]
    ref = 'home_hero' if pg.pid == 'home' else f'{SLUG_REF.get(pg.pid, pg.pid.split("-")[0])}_intro'
    if pg.pid in AREAS:
        ref = f'area_{SLUG_REF[pg.pid]}'
    return f'''<section class="hero">
<figure class="hero-img">{img(pg, hid, "100vw", 1600, 900, eager=True, kind='hero')}<figcaption>{E(pg.ui['ill_credit'])}</figcaption></figure>
<div class="wrap"><div class="plate-hero">
<h1>{E(h1)}</h1>
{f'<p class="sub">{E(sub)}</p>' if sub else ''}
{cta_row(pg, ref)}
</div></div>
</section>'''


def crumbs(pg, mid=None):
    parts = [f'<a href="{pg.lp("home")}">{E(pg.ui["breadcrumb_home"])}</a>']
    if mid:
        parts.append(mid)
    parts.append(f'<span aria-current="page">{E(pg.p["h1"])}</span>')
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">' + '<span class="sep" aria-hidden="true">/</span>'.join(parts) + '</nav>'


def gallery(pg, ids=GAL):
    cards = ''.join(f'<figure class="gcard">{img(pg, m, "(min-width: 900px) 300px, 68vw", 800, 1000)}'
                    f'<figcaption><span>{E(cap(pg, m))}</span><small>{E(pg.ui["ill_credit"])}</small></figcaption></figure>' for m in ids)
    return (f'<div class="rail-wrap"><div class="glide" role="group" aria-label="{E(pg.ui["carousel_label"])}" data-speed="0.035">{cards}</div>'
            f'<div class="rail-nav"><button type="button" class="rn prev" aria-label="{E(pg.ui["prev"])}"></button><button type="button" class="rn next" aria-label="{E(pg.ui["next"])}"></button></div></div>')


def faq_block(pg, faqs):
    items = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    return f'<section class="band faq"><div class="wrap narrow"><h2>{E(pg.ui["faq_h"])}</h2>{items}</div></section>'


def find_us(pg):
    return f'''<section class="band find" id="find"><div class="wrap find-g">
<div class="find-t"><h2>{E(pg.ui['find_h'])}</h2>
<address>{E(F['address']['display'])}</address>
<p class="lm">{E(pg.ui['plate_loc_v'])}</p>
{hours_table(pg)}
<div class="links"><a class="lnk" href="{E(F['maps_url'])}" target="_blank" rel="noopener" data-cta="map_findus" data-ref="map_findus">{ICON['pin']}<span>{E(pg.ui['open_maps'])}</span></a>
<a class="lnk" href="{E(F['directions_url'])}" target="_blank" rel="noopener" data-cta="directions_findus" data-ref="directions_findus">{ICON['pin']}<span>{E(pg.ui['directions'])}</span></a></div>
<div class="rev"><p><b>{E(pg.ui['review_h'])}</b> {E(pg.ui['review_p'])}</p><a class="lnk" href="{E(F['review_url'])}" target="_blank" rel="noopener" data-cta="reviews_findus" data-ref="reviews_findus">{ICON['star']}<span>{E(pg.ui['review_btn'])}</span></a></div>
</div>
<div class="map"><iframe title="{E(pg.ui['map_title'])}" src="{E(F['embed_url'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''


def plate(pg):
    rows = [('plate_loc', 'plate_loc_v'), ('plate_rooms', 'plate_rooms_v'), ('plate_hours', 'plate_hours_v'), ('plate_phones', 'plate_phones_v')]
    dl = ''.join(f'<div><dt>{E(pg.ui[a])}</dt><dd>{E(pg.ui[b])}</dd></div>' for a, b in rows)
    return f'<div class="idplate"><p class="idplate-h">{E(pg.ui["plate_h"])}</p><dl>{dl}</dl></div>'


def ticket(pg):
    steps = ''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in pg.ui['process'])
    return f'<section class="band proc"><div class="wrap narrow"><div class="ticket"><h2>{E(pg.ui["process_h"])}</h2><ol>{steps}</ol></div></div></section>'


def radius_map(pg, hi=None):
    # Approximate bearings from the Batu 10 pin; rings 5/10/20 km (scale 7px per km)
    pos = {'kemena-sibiyu-nyabau': (150 + 34, 150 - 24), 'kidurong-bintulu-port': (150 - 44, 150 - 50), 'bintulu-town-jepak': (150 - 70, 150 + 30)}
    dots = ''
    for a in pg.c['areas']:
        x, y = pos[a['id']]
        on = ' on' if a['id'] == hi else ''
        dots += f'<a href="{pg.lp(a["id"])}" class="rdot{on}"><circle cx="{x}" cy="{y}" r="9"/><text x="{x}" y="{y + 25}" text-anchor="middle">{E(a["km"])}</text></a>'
    rings = ''.join(f'<circle class="ring" cx="150" cy="150" r="{r * 7}"/><text class="rl" x="150" y="{150 - r * 7 - 4}" text-anchor="middle">{r} km</text>' for r in (5, 10))
    return (f'<figure class="radius"><svg viewBox="0 0 300 300" role="img" aria-label="{E(pg.ui["radius_caption"])}">'
            f'<rect class="rbg" x="0" y="0" width="300" height="300" rx="22"/>{rings}'
            f'<circle class="ring r20" cx="150" cy="150" r="140"/><text class="rl" x="150" y="24" text-anchor="middle">20 km</text>'
            f'{dots}<g class="pin"><circle cx="150" cy="150" r="11"/><circle cx="150" cy="150" r="4" class="pin-in"/></g>'
            f'<text class="pin-l" x="150" y="182" text-anchor="middle">{E(pg.ui["workshop_label"])}</text></svg>'
            f'<figcaption>{E(pg.ui["radius_caption"])}</figcaption></figure>')


def area_strip(pg, hi=None):
    cards = ''
    for a in pg.c['areas']:
        cur = ' aria-current="page"' if a['id'] == hi else ''
        cards += (f'<a class="acard" href="{pg.lp(a["id"])}"{cur}><span class="km">{E(a["km"])}</span><small>{E(pg.ui["km_from"])}</small>'
                  f'<b>{E(a["name"])}</b><span class="al">{E(a["line"])}</span></a>')
    return f'<div class="acards">{cards}</div>'


def svc_rows(pg, exclude=None):
    rows = ''
    for i, s in enumerate(pg.c['services']):
        if s['id'] == exclude:
            continue
        rows += (f'<a class="srow" href="{pg.lp(s["id"])}"><span class="srow-img">{img(pg, s["img"], "(min-width: 900px) 200px, 34vw", 480, 600)}</span>'
                 f'<span class="srow-t"><b>{E(s["short"])}</b><span>{E(s["line"])}</span></span></a>')
    return f'<div class="srows">{rows}</div>'


def cta_band(pg, ref):
    return (f'<section class="band ctab"><div class="wrap narrow"><h2>{E(pg.ui["cta_band_h"])}</h2><p>{E(pg.ui["cta_band_p"])}</p>'
            f'{cta_row(pg, ref)}<p class="ll"><a {tel("call_landline_" + ref, True)}>{E(pg.ui["landline"])}</a></p></div></section>')


# ---------------------------------------------------------------- page bodies
def page_home(pg):
    p = pg.p
    body = hero(pg, p['h1'], p['sub'])
    body += f'''<main id="main">
<section class="band bench"><div class="wrap"><div class="sec-h"><h2>{E(p['bench_h'])}</h2><p>{E(p['bench_p'])}</p></div></div>{gallery(pg)}</section>
<section class="band svc"><div class="wrap"><h2>{E(p['svc_h'])}</h2>{svc_rows(pg)}</div></section>
<section class="band veh"><div class="wrap veh-g"><div><h2>{E(p['veh_h'])}</h2><p>{E(p['veh_p'])}</p><a class="lnk" href="{pg.lp('vehicles-and-machines')}"><span>{E(p['veh_link'])}</span></a></div>
<div class="veh-pics">{figure(pg, 'g05-workshop-front-canopy')}{figure(pg, 'g08-lorries-in-yard')}{figure(pg, 'g09-coach-bus-in-bay')}</div></div></section>
<section class="band areas"><div class="wrap areas-g"><div><h2>{E(p['areas_h'])}</h2><p>{E(p['areas_p'])}</p>{area_strip(pg)}</div>{radius_map(pg)}</div></section>
{ticket(pg)}
<section class="band proof"><div class="wrap narrow"><p class="lead">{E(p['plate_intro'])}</p>{plate(pg)}</div></section>
{find_us(pg)}
{cta_band(pg, 'home_end')}
</main>'''
    return head(pg, schema(pg, [])) + header(pg) + body + footer(pg)


def page_service(pg):
    p = pg.p
    sid = pg.pid
    ref = SLUG_REF[sid]
    idx = SERVICES.index(sid)
    nxt = pg.c['services'][(idx + 1) % len(SERVICES)]
    imgs = SVC_IMGS[sid]
    lis = ''.join(f'<li>{E(x)}</li>' for x in p['s1_list'])
    send = ''.join(f'<li>{E(x)}</li>' for x in p['send_list'])
    body = hero(pg, p['h1'])
    body += f'''{crumbs(pg)}<main id="main">
<section class="band intro"><div class="wrap narrow"><p class="lead">{E(p['intro'])}</p><p class="upd">{E(pg.ui['updated'])}</p></div></section>
<section class="band split"><div class="wrap split-g"><div><h2>{E(p['s1_h'])}</h2><ul class="ticks">{lis}</ul><p class="note">{E(p['s1_note'])}</p></div>{figure(pg, imgs[0])}</div></section>
<section class="band alt"><div class="wrap split-g rev"><div><h2>{E(p['s2_h'])}</h2><p>{E(p['s2_p'])}</p>{cta_row(pg, ref + '_mid')}</div>{figure(pg, imgs[1])}</div></section>
<section class="band"><div class="wrap narrow"><h2>{E(p['s3_h'])}</h2><p>{E(p['s3_p'])}</p>
<div class="sendbox"><h3>{E(p['send_h'])}</h3><ul class="ticks">{send}</ul></div>
{figure(pg, imgs[2], 'fig wide') if len(imgs) > 2 else ''}</div></section>
{ticket(pg)}
{faq_block(pg, p['faqs'])}
<section class="band areas"><div class="wrap"><h2>{E(pg.ui['areas_h'])}</h2>{area_strip(pg)}</div></section>
<section class="band svc"><div class="wrap"><h2>{E(pg.ui['next_service'])}: <a href="{pg.lp(nxt['id'])}">{E(nxt['short'])}</a></h2>{svc_rows(pg, exclude=sid)}</div></section>
{find_us(pg)}
{cta_band(pg, ref + '_end')}
</main>'''
    return head(pg, schema(pg, [service_schema(pg), faq_schema(pg, p['faqs'])])) + header(pg) + body + footer(pg)


def page_area(pg):
    p = pg.p
    aid = pg.pid
    ref = SLUG_REF[aid]
    lm = ''.join(f'<li>{E(x)}</li>' for x in p['landmarks'])
    who = ''.join(f'<li>{E(x)}</li>' for x in p['who_list'])
    imgs = AREA_IMG[aid]
    others = [a for a in pg.c['areas'] if a['id'] != aid]
    area_ld = {'@type': 'Service', '@id': CFG.canon(pg.path) + '#service', 'name': p['h1'], 'provider': {'@id': golive.jsonld_id(CFG)},
               'serviceType': 'Diesel fuel pump, injector and turbo repair',
               'areaServed': [{'@type': 'Place', 'name': n} for n in C['en']['pages'][aid]['landmarks']], 'url': CFG.canon(pg.path)}
    body = hero(pg, p['h1'])
    body += f'''{crumbs(pg)}<main id="main">
<section class="band intro"><div class="wrap narrow"><p class="lead">{E(p['intro'])}</p><p class="upd">{E(pg.ui['updated'])}</p></div></section>
<section class="band split"><div class="wrap split-g"><div><h2>{E(p['local_h'])}</h2><p>{E(p['local_p'])}</p><p>{E(p['local_p2'])}</p>{cta_row(pg, 'area_' + ref + '_mid')}</div>{figure(pg, imgs[0])}</div></section>
<section class="band alt"><div class="wrap areas-g"><div><h2>{E(p['where_h'])}</h2><p>{E(p['where_p'])}</p><ul class="chips">{lm}</ul>
<h3>{E(p['who_h'])}</h3><ul class="ticks">{who}</ul></div>{radius_map(pg, aid)}</div></section>
<section class="band svc"><div class="wrap"><h2>{E(pg.ui['services_h'])}</h2>{svc_rows(pg)}</div></section>
{ticket(pg)}
<section class="band areas"><div class="wrap"><h2>{E(pg.ui['areas_h'])}</h2>{area_strip(pg, aid)}</div></section>
{find_us(pg)}
{cta_band(pg, 'area_' + ref + '_end')}
</main>'''
    return head(pg, schema(pg, [area_ld])) + header(pg) + body + footer(pg)


def page_vehicles(pg):
    p = pg.p
    groups = ''
    for i, (t, d, m) in enumerate(p['groups']):
        groups += f'<section class="band {"alt" if i % 2 else ""}"><div class="wrap split-g {"rev" if i % 2 else ""}"><div><h2>{E(t)}</h2><p>{E(d)}</p></div>{figure(pg, m)}</div></section>'
    body = hero(pg, p['h1'])
    body += f'''{crumbs(pg)}<main id="main">
<section class="band intro"><div class="wrap narrow"><p class="lead">{E(p['intro'])}</p><p class="upd">{E(pg.ui['updated'])}</p></div></section>
{groups}
<section class="band"><div class="wrap narrow"><p class="note">{E(p['note'])}</p><h2>{E(p['s_h'])}</h2><p>{E(p['s_p'])}</p></div></section>
<section class="band svc"><div class="wrap"><h2>{E(pg.ui['services_h'])}</h2>{svc_rows(pg)}</div></section>
<section class="band areas"><div class="wrap"><h2>{E(pg.ui['areas_h'])}</h2>{area_strip(pg)}</div></section>
{find_us(pg)}
{cta_band(pg, 'vehicles_end')}
</main>'''
    return head(pg, schema(pg, [])) + header(pg) + body + footer(pg)


def page_about(pg):
    p = pg.p
    body = hero(pg, p['h1'])
    body += f'''{crumbs(pg)}<main id="main">
<section class="band intro"><div class="wrap narrow"><p class="lead">{E(p['intro'])}</p></div></section>
<section class="band split"><div class="wrap split-g"><div><h2>{E(p['s1_h'])}</h2><p>{E(p['s1_p'])}</p></div>{figure(pg, 'g01-cleanroom-pump-bench')}</div></section>
<section class="band alt"><div class="wrap split-g rev"><div><h2>{E(p['s2_h'])}</h2><p>{E(p['s2_p'])}</p></div>{figure(pg, 'g06-heavy-engine-workshop')}</div></section>
<section class="band"><div class="wrap narrow"><h2>{E(p['owner_h'])}</h2><p>{E(p['owner_p'])}</p>{cta_row(pg, 'about_mid')}{plate(pg)}</div></section>
{gallery(pg)}
{ticket(pg)}
{find_us(pg)}
{cta_band(pg, 'about_end')}
</main>'''
    return head(pg, schema(pg, [])) + header(pg) + body + footer(pg)


def page_contact(pg):
    p = pg.p
    body = hero(pg, p['h1'])
    body += f'''{crumbs(pg)}<main id="main">
<section class="band intro"><div class="wrap narrow"><p class="lead">{E(p['intro'])}</p></div></section>
<section class="band"><div class="wrap narrow"><h2>{E(p['ways_h'])}</h2>
<ul class="ways">
<li><a class="btn wa" {wa(pg, ref='whatsapp_contact')}>{ICON['wa']}<span>{E(pg.ui['wa_long'])}</span></a></li>
<li><a class="btn call" {tel('call_contact')}>{ICON['call']}<span>{E(pg.ui['call_long'])}</span></a></li>
<li><a class="btn line" {tel('call_landline_contact', True)}>{ICON['phone']}<span>{E(pg.ui['landline'])}</span></a></li>
</ul>
<h2>{E(p['where_h'])}</h2><p>{E(p['where_p'])}</p><p class="note">{E(p['one_loc'])}</p>
<p>{E(pg.ui['owner_label'])}: {E(F['owner'])}</p>{plate(pg)}</div></section>
{find_us(pg)}
</main>'''
    return head(pg, schema(pg, [])) + header(pg) + body + footer(pg)


def page_articles(pg):
    p = pg.p
    links = ''.join(f'<li><a href="{pg.lp(s["id"])}">{E(s["short"])}</a></li>' for s in pg.c['services'])
    body = hero(pg, p['h1'])
    body += f'''{crumbs(pg)}<main id="main">
<section class="band intro"><div class="wrap narrow"><p class="lead">{E(p['intro'])}</p>
<div class="art-list" id="articles"><p class="note">{E(pg.ui['articles_none'])}</p><ul class="ticks">{links}</ul></div></div></section>
{cta_band(pg, 'articles_end')}
</main>'''
    ld = {'@type': 'CollectionPage', '@id': CFG.canon(pg.path) + '#hub', 'name': p['h1'], 'url': CFG.canon(pg.path)}
    return head(pg, schema(pg, [ld])) + header(pg) + body + footer(pg)


def page_privacy(pg):
    pv_facts = {'name': F['name'], 'address': F['address']['display'], 'wa_display': F['whatsapp']['display'],
                'wa_link': 'https://wa.me/' + F['whatsapp']['wa'], 'tel_display': F['mobile']['display'], 'tel_link': 'tel:' + F['mobile']['e164'],
                'extras': ['maps'], 'updated': PV.UPDATED[pg.L]}
    main = PV.render_main(pg.L, 'my', pv_facts)
    pg.p.setdefault('h1', PV.TITLES[pg.L])
    body = f'<main id="main" class="prose-page"><div class="wrap narrow prose">{main}</div></main>'
    return head(pg, schema(pg, [])) + header(pg) + body + footer(pg)


RENDER = {'home': page_home, 'vehicles-and-machines': page_vehicles, 'about': page_about, 'contact': page_contact,
          'articles': page_articles, 'privacy': page_privacy}


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    # static assets (copied from src/, versioned by content hash)
    for rel in ['assets/site.css', 'assets/site.js', 'p1-cta.js']:
        os.makedirs(os.path.dirname(os.path.join(OUT, rel)) or OUT, exist_ok=True)
        shutil.copyfile(os.path.join(HERE, rel), os.path.join(OUT, rel))
        ASSET_V[os.path.basename(rel)] = vhash(os.path.join(OUT, rel))
    for d in ['assets/fonts', 'images/brand']:
        shutil.copytree(os.path.join(HERE, d), os.path.join(OUT, d), dirs_exist_ok=True)
    built, html_by = [], {}
    for L in ('en', 'ms', 'zh'):
        for pid in PAGES:
            pg = Page(pid, L)
            fn = page_service if pid in SERVICES else page_area if pid in AREAS else RENDER[pid]
            out = fn(pg)
            write(pg.path + 'index.html', out)
            built.append(pg.path)
            html_by[pg.path] = out
    # 404 (English, never indexed)
    pg = Page('contact', 'en')
    # sitemap, robots, llms from the one-switch config
    paths = list(PAGES.values())
    write('sitemap.xml', golive.sitemap_xml(CFG, paths, UPDATED_ISO))
    write('robots.txt', golive.robots_txt(CFG))
    en = C['en']
    llms = golive.llms_header(CFG, F['name'], 'Diesel fuel pump, common rail pump, injector and turbo repair workshop at Batu 10, Jalan Bintulu–Miri, Bintulu, Sarawak, Malaysia.')
    llms += f"\n## Contact\n- WhatsApp / mobile: {F['mobile']['display']} (+60 19-854 5433)\n- Landline (Tel/Fax): {F['landline']['display']}\n- Address: {F['address']['display']}\n- Hours: Monday to Saturday 8:00am to 5:30pm, Sunday closed (Malaysia time)\n- Google Maps: {F['maps_url']}\n"
    llms += '\n## Services\n' + ''.join(f"- [{s['short']}]({CFG.canon(PAGES[s['id']])}): {s['line']}\n" for s in en['services'])
    llms += '\n## Areas (within 20 km of Batu 10)\n' + ''.join(f"- [{a['name']}]({CFG.canon(PAGES[a['id']])}): {a['km']} from Batu 10\n" for a in en['areas'])
    llms += f"\n## Other pages\n- [Vehicles and machines]({CFG.canon(PAGES['vehicles-and-machines'])})\n- [About]({CFG.canon('about/')})\n- [Contact]({CFG.canon('contact/')})\n- [Articles]({CFG.canon('articles/')})\n- [Privacy]({CFG.canon('privacy/')})\n"
    llms += '\nLanguages: English, Bahasa Melayu (/ms/), Simplified Chinese (/zh/).\nAll pictures on the site are AI-generated illustrations, not photographs of real jobs or the building.\n'
    write('llms.txt', llms)
    # gates
    probs = I18N.check_twins(set(built)) + I18N.check_privacy(set(built), html_by); RV.check_no_rating(html_by)
    print('pages', len(built), 'problems', probs)
    json.dump({'built': built, 'asset_v': ASSET_V}, open(os.path.join(OUT, '.build.json'), 'w'))


if __name__ == '__main__':
    main()

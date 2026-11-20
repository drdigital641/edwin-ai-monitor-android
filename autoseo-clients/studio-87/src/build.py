#!/usr/bin/env python3
"""Studio 87 site builder (AutoSEO.my client preview, 20 Nov 2026). English + 简体中文 only (the client asked for 中文及英文).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links and schema live here once, so one
edit updates every page in both languages. Facts: facts.json. Copy: strings_en.py / strings_zh.py (same keys, checked).
Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared template autoseo-template/autoseo_i18n.py,
limited to EN + ZH for this site.

Unified go-live: canonical, hreflang, og:url, schema, sitemap.xml and llms.txt target https://studio87.com.my/ from the start.
Asset and page links are root-relative to BASE, so the preview build (BASE=/preview/studio-87/) works on autoseo.my now, and
  python3 build.py --live   rebuilds with BASE=/ for the day studio87.com.my points at this folder.
No per-page robots meta: the preview host sends X-Robots-Tag noindex from preview/.htaccess.
Then python3 check.py (pre-upload gate) before the Bridge upload (sync_from_github, site autoseo, base_path preview/studio-87,
source autoseo-clients/studio-87/dist). Photos and logos are placed on the server from Bridge drop 6affda1dff2244c8ee44d100
(media/, see SERVER_MEDIA) and are not in the repo."""
import hashlib, html, json, os, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for p in (os.path.join(HERE, '..', '..', '..', 'autoseo-template'), '/mnt/project-files/autoseo-template'):
    if os.path.exists(os.path.join(p, 'autoseo_i18n.py')):
        sys.path.insert(0, p)
        break
import autoseo_i18n as I18N
import strings_en, strings_zh

# EN + 中文 only for this site: narrow the shared module's language list (its helpers read the module-level LANGS).
I18N.LANGS = [I18N.BY_CODE['en'], I18N.BY_CODE['zh']]
I18N.DEFAULT = I18N.LANGS[0]
STRINGS = {'en': strings_en, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
LIVE = '--live' in sys.argv
BASE = '/' if LIVE else F['preview']['base_path']
SITE = F['live']['origin'] + '/'          # canonical origin from day one
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LK = F['links']
TODAY = '2026-11-20'
NAME = F['name']

# stem -> (file, w, h, object-position). All placed on the server from the Bridge drop (sha256 in SERVER_MEDIA).
MEDIA = {
    'colour-ash-waves-back': ('colour-ash-waves-back', 1280, 1600, 'center 40%'),
    'colour-ash-waves-side': ('colour-ash-waves-side', 1280, 1600, 'center 38%'),
    'colour-ash-waves-salon': ('colour-ash-waves-salon', 1280, 1600, 'center 40%'),
    'colour-honey-waves': ('colour-honey-waves', 737, 921, 'center 45%'),
    'colour-copper-halfup': ('colour-copper-halfup', 629, 786, 'center 30%'),
    'style-braid-halfup': ('style-braid-halfup', 720, 900, 'center 35%'),
    'style-curls-portrait': ('style-curls-portrait', 711, 889, 'center 25%'),
    'upstyle-evening-waves': ('upstyle-evening-waves', 747, 934, 'center 40%'),
    'upstyle-caramel-bun': ('upstyle-caramel-bun', 740, 925, 'center 35%'),
    'upstyle-dark-chignon': ('upstyle-dark-chignon', 708, 885, 'center 30%'),
}
SERVER_MEDIA = {
    'media/colour-ash-waves-back.webp': 'd39d9380e283dfa8e6e884d376c56ff3ba9a636bb1c06822cbf0f8fc34668232',
    'media/colour-ash-waves-back.jpg': '630c9e45eb96806fe1bc290011dc3474464c75fec7f48a1d692cea155de22989',
    'media/colour-ash-waves-side.webp': '0c3994a8488bfc2e8cf33f89c4f877714ae58413da580e2f53231995a640397f',
    'media/colour-ash-waves-side.jpg': '4d2c2aa476f659864edc9b17362fe3ca94da49844f4f220a8c450cfcb39a8b5c',
    'media/colour-ash-waves-salon.webp': '6d70e81ebfecf0b924da5de40f78ab15b8d2cea74ff8efc8e2c4fcc9a20dc5be',
    'media/colour-ash-waves-salon.jpg': '2509f4d6c62ff82159195a238d85e027859a86068a378b370cf32a667d36f0f1',
    'media/colour-honey-waves.webp': '8892a1ba40125da12cdbd5d77236de25fa80552ab3f166558ccb3d6ea5cb4155',
    'media/colour-honey-waves.jpg': 'a8fe95c08e4d2cae0eb50a235c617cb77ed90b502a29950f2b7f5b02c71ad02e',
    'media/colour-copper-halfup.webp': '715a25394d467f14123aaebf5d81a10f51c5d9692a66384580499912ab3db37e',
    'media/colour-copper-halfup.jpg': 'd2fdd043ce960fc2f9b1076249d3ba4e63f857590c583b61485f9d29b11a21d4',
    'media/style-braid-halfup.webp': 'b42d21743a9254da0a90e97791896846a554b89cb9aa5af4f80f5ad0dab4326e',
    'media/style-braid-halfup.jpg': '05606b106d36eb5a9b37afbdae9690c088608f6fcd916d311e83cc907dccdc7a',
    'media/style-curls-portrait.webp': '0bd9ba92a1564b3c314e413f1caea9381c6ecd7a2fba0e61c3173096fbc66180',
    'media/style-curls-portrait.jpg': '26a3166ad8cbd776af3ebfeaa0ea91cbbbb22e24e0afe5709a232c2ecb7727cf',
    'media/upstyle-evening-waves.webp': 'eede0eebf887c2e1f6595a6c403102b93d2453731cc8862f65cdcb2b7f81f4b7',
    'media/upstyle-evening-waves.jpg': '9ef390a005c6fd19d2a2a446c544ff12e17ae882d96ff6ad2a155c095540ef68',
    'media/upstyle-caramel-bun.webp': '3c03549f6ee73534c58091a9f1b530601aa39c4424f03f763fbf3b88ee05c201',
    'media/upstyle-caramel-bun.jpg': '6cde11ba96d08d8cc53b0cb721e09c1503106d390771ee54ded484414dc7fa14',
    'media/upstyle-dark-chignon.webp': '59b6364eca1c26dee5875e65cad51137487761867f09b70752019e2a8bbd56f8',
    'media/upstyle-dark-chignon.jpg': '867b747b30edbc714d5593419fed706cb70e511395804048bde6b91ba205c538',
    'media/logo.webp': '234b39f778415e7dfebc60279ec0c1de94b8a412d881d0ab74957211958edd03',
    'media/logo.png': '734f80a429bf463fe90906034fb83b0d11ed12d0098e89bff2c5ab385791a39c',
    'media/logo-ink.webp': '81df6323158ee1fc724822df1e43d8742ba8043b7acebbb3919c4b2909865d64',
    'media/logo-ink.png': 'cfdbcf5975fd5a22a3b2ed9abc7f0ab88c7134e7873f3c3c3092a21933a714f0',
    'media/logo-on-black.webp': 'da6060f2882cfd1721e0b3e9faa697015429c835777754438590c89e154ddf0f',
    'media/logo-on-black.jpg': '06f221a04798ec0f0770bb0e4b0b17d6f2c2302716be27d36907034d6fded909',
    'media/favicon.png': '4d7e50f312c2afde03aac42912ce36693d759a92f92770c93ff4e12acc479179',
    'media/favicon.webp': '84b6a6c7072687a6446e8f21d1ac077c0d233e98d2a8f5692263735f192265b0',
    'media/og.jpg': '166ea935bae44854f051f166dfab348bf8806dd9952b4b06c1fe3e5220b3eb96',
    'media/og.webp': 'cb9595623ac1f90245bc122d9865d1a46ba5ab0d1cb99e929c72270ab2f5f4b2',
}
RAIL = ['colour-ash-waves-side', 'colour-ash-waves-salon', 'colour-honey-waves', 'colour-copper-halfup', 'style-braid-halfup',
        'style-curls-portrait', 'upstyle-evening-waves', 'upstyle-caramel-bun', 'upstyle-dark-chignon']
SVC_PATH = {'colour': 'services/hair-colouring/', 'highlights': 'services/highlights-balayage/', 'perm': 'services/perming/',
            'cut': 'services/haircuts-styling/', 'grey': 'services/grey-hair-transformation/',
            'treatment': 'services/hair-treatment-smoothing/', 'mens': 'services/mens-hair/'}
PAGES = ['', 'services/'] + [SVC_PATH[k] for k in strings_en.SERVICE_ORDER] + ['about/', 'contact/', 'articles/', 'privacy/']
NAV = [('services/', 'services'), ('about/', 'about'), ('contact/', 'contact')]


def u(p=''):
    return BASE + p


def absu(p=''):
    return SITE + p


def share_url(p=''):
    # Share images (og:image / twitter:image) must resolve NOW: preview host while on preview, live origin only after go-live (--live).
    return (SITE if LIVE else F['preview']['origin'] + F['preview']['base_path']) + p


def pu(p=''):
    return u(I18N.page_path(L, p))


def pabs(p=''):
    return absu(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


def wa_url(key='default'):
    return f"{F['whatsapp']['url']}?text={urllib.parse.quote(S.PREFILL[key])}"


ICONS = {
    'wa': '<path d="M4.6 19.4l1.1-3.5a7.9 7.9 0 1 1 2.9 2.7z"/><path d="M9.3 8.7c.3 2.5 2.3 4.7 5 5.2l.9-1.1 1.8.8-.3 1.5c-3.8.4-7.7-3.5-7.5-7.3l1.5-.3.8 1.7z"/>',
    'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z"/>',
    'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z"/><circle cx="12" cy="10.1" r="2.2"/>',
    'fb': '<path d="M14.5 8.5H17V5h-2.5A3.5 3.5 0 0 0 11 8.5V11H8.5v3.5H11V20h3.5v-5.5H17l.5-3.5h-3V9a.5.5 0 0 1 .5-.5z"/>',
    'ig': '<rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.6"/><circle cx="16.9" cy="7.1" r=".6"/>',
    'menu': '<path d="M4 9h16M8 15h12"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
    'prev': '<path d="M14.5 5.5L8 12l6.5 6.5"/>', 'next': '<path d="M9.5 5.5L16 12l-6.5 6.5"/>',
    'go': '<path d="M5 12h13M13.5 7l5 5-5 5"/>', 'star': '<path d="M12 4.2l2.3 4.8 5.2.7-3.8 3.6.9 5.2-4.6-2.5-4.6 2.5.9-5.2-3.8-3.6 5.2-.7z"/>',
}


def icon(name):
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


# ---------- CTA links (data-cta = data-ref = placement; the Controller reads the whatsapp_/call_/map_/facebook_/instagram_ prefix) ----------
def wa(place, key='default', label=None, cls='go-wa'):
    return (f'<a class="{cls}" href="{E(wa_url(key))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='go-call'):
    return (f'<a class="{cls}" href="{F["phone"]["tel"]}" data-cta="call_{place}" data-ref="call_{place}">'
            f'{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>')


def ext(kind, place, href, label, cls=None, ic=None):
    c = f' class="{cls}"' if cls else ''
    return (f'<a{c} href="{E(href)}" target="_blank" rel="noopener" data-cta="{kind}_{place}" data-ref="{kind}_{place}">'
            f'{icon(ic) if ic else ""}<span>{E(label)}</span></a>')


def pic(stem, alt, cls=None, eager=False, sizes='(min-width: 900px) 340px, 78vw'):
    f, w, h, pos = MEDIA[stem]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{u("media/" + f + ".webp")}">'
            f'<img{c} src="{u("media/" + f + ".jpg")}" width="{w}" height="{h}" alt="{E(alt)}" style="object-position:{pos}"{load} decoding="async"></picture>')


def card(stem, tag='figure'):
    return (f'<{tag} class="wk">{pic(stem, S.PHOTOS[stem])}'
            f'<figcaption>{E(S.CAP[stem])}</figcaption></{tag}>')


def rail(stems, label, cls=''):
    cards = ''.join(f'<li>{card(s)}</li>' for s in stems)
    return (f'<div class="rail {cls}"><ul class="glide" aria-label="{E(label)}" tabindex="0">{cards}</ul>'
            f'<div class="rail-nav"><button type="button" class="rn" data-dir="-1" aria-label="{E(S.UI["rail_hint"])}">{icon("prev")}</button>'
            f'<span class="rail-hint">{E(S.UI["rail_hint"])}</span>'
            f'<button type="button" class="rn" data-dir="1" aria-label="{E(S.UI["rail_hint"])}">{icon("next")}</button></div></div>')


def wordmark(cls='wm-img', ink=False, eager=False):
    f = 'logo-ink' if ink else 'logo'
    load = '' if eager else ' loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{u("media/" + f + ".webp")}">'
            f'<img class="{cls}" src="{u("media/" + f + ".png")}" width="1033" height="368" alt="{E(S.PHOTOS["logo"])}"{load} decoding="async"></picture>')


# ---------- head / header / footer ----------
def head(path, title, meta, ld, hero=None):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    pre = (f'<link rel="preload" href="{u("assets/fonts/notoserifsc-sub.woff2")}" as="font" type="font/woff2" crossorigin>' if zh else
           f'<link rel="preload" href="{u("assets/fonts/bodonimoda.woff2")}" as="font" type="font/woff2" crossorigin>')
    if hero:
        pre += f'<link rel="preload" as="image" type="image/webp" href="{u("media/" + MEDIA[hero][0] + ".webp")}" fetchpriority="high">'
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
<link rel="canonical" href="{pabs(path)}">
{I18N.hreflang_links(absu, path)}
<meta name="theme-color" content="#0A0A0A">
<link rel="icon" href="{u('media/favicon.png')}" type="image/png">
<link rel="apple-touch-icon" href="{u('media/favicon.png')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(NAME)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{pabs(path)}">
<meta property="og:image" content="{share_url('media/og.jpg')}">
<meta property="og:image:secure_url" content="{share_url('media/og.jpg')}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.PHOTOS['og'])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share_url('media/og.jpg')}">
{pre}
<link rel="stylesheet" href="{u('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def header(path):
    def cur(p):
        return ' aria-current="page"' if (path == p or (p == 'services/' and path.startswith('services/'))) else ''
    nav = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV + [('articles/', 'articles')])
    svc = ''.join(f'<a href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]["zone"])}</a>' for k in S.SERVICE_ORDER)
    return f'''<body class="lang-{L['code']}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{wordmark('wm-w', eager=True)}{wordmark('wm-k', ink=True)}</a>
<nav class="nav" aria-label="{E(S.UI['menu'])}">{nav}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='lang')}
{wa('header', label=S.UI['wa_short'], cls='go-wa sm hdr-wa')}
<button class="mb" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div></header>
<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-label="{E(S.UI['menu'])}">
<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button>
<nav class="sheet-nav" aria-label="{E(S.UI['menu'])}">{sheet}</nav>
<nav class="sheet-svc" aria-label="{E(S.UI['services'])}">{svc}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='lang')}
<div class="sheet-cta">{wa('menu')}{call('menu')}</div>
</div></div>
<main id="main">'''


def hours_table(cls='hrs'):
    rows = ''.join(f'<tr><th scope="row">{E(d)}</th><td>{E(v)}</td></tr>' for d, v in S.HOURS)
    return f'<table class="{cls}"><tbody>{rows}</tbody></table>'


def address_html():
    return '<address>' + '<br>'.join(E(x) for x in F['address']['lines']) + '</address>'


def footer():
    svc = ''.join(f'<li><a href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]["zone"])}</a></li>' for k in S.SERVICE_ORDER)
    return f'''</main>
<footer class="ft"><div class="wrap">
<div class="ft-id"><a class="ft-brand" href="{pu('')}" aria-label="{E(NAME)}">{wordmark('ft-wm')}</a>
<p class="ft-since">{E(S.UI['since'])}</p></div>
<div class="ft-g">
<div><h2>{E(S.UI['address_h'])}</h2>{address_html()}
<p>{ext('map', 'footer', LK['maps'], S.UI['maps'], cls='fl', ic='pin')}</p></div>
<div><h2>{E(S.UI['hours_h'])}</h2>{hours_table('hrs ft-hrs')}</div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul class="ft-l">
<li>{wa('footer', label='WhatsApp ' + F['whatsapp']['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{ext('facebook', 'footer', LK['facebook'], S.UI['facebook'], cls='fl', ic='fb')}</li>
<li>{ext('instagram', 'footer', LK['instagram'], S.UI['instagram'] + ' ' + LK['instagram_handle'], cls='fl', ic='ig')}</li>
</ul></div>
<div><h2>{E(S.UI['services'])}</h2><ul class="ft-s">{svc}</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(NAME)}</span><a href="{pu('about/')}">{E(S.UI['about'])}</a><a href="{pu('articles/')}">{E(S.UI['articles'])}</a><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="mbar">{wa('mobile_bar', label=S.UI['wa_short'])}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{u('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{u('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (one facts file; no aggregateRating, no Place ID) ----------
def org_ld():
    a = F['address']
    days = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']} for h in F['hours']]
    return {
        '@context': 'https://schema.org', '@type': 'HairSalon', '@id': SITE + '#salon',
        'name': NAME, 'description': S.SCHEMA['description'], 'url': pabs(''), 'inLanguage': L['hreflang'],
        'foundingDate': str(F['established_year']), 'telephone': F['phone']['e164'],
        'image': absu('media/og.jpg'), 'logo': absu('media/logo-on-black.jpg'),
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': a['city'], 'postalCode': a['postcode'],
                    'addressRegion': a['region'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['maps'],
        'openingHoursSpecification': days,
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'reservations', 'telephone': F['whatsapp']['e164'], 'url': F['whatsapp']['url'],
                          'availableLanguage': ['en', 'zh']}],
        'sameAs': [LK['facebook'], LK['instagram']],
        'areaServed': [{'@type': 'City', 'name': 'Kuantan'}, {'@type': 'State', 'name': 'Pahang'}],
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': S.SERVICES[k]['zone'], 'url': pabs(SVC_PATH[k])}} for k in S.SERVICE_ORDER],
    }


def site_ld():
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '#website', 'url': absu(''), 'name': NAME,
            'inLanguage': [x['hreflang'] for x in I18N.LANGS], 'publisher': {'@id': SITE + '#salon'}}


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (p, n) in enumerate(trail)]}


def service_ld(k):
    s = S.SERVICES[k]
    d = {'@context': 'https://schema.org', '@type': 'Service', 'name': s['h1'], 'serviceType': s['zone'], 'description': s['meta'],
         'url': pabs(SVC_PATH[k]), 'provider': {'@id': SITE + '#salon'}, 'areaServed': {'@type': 'City', 'name': 'Kuantan'}}
    if s['photos']:
        d['image'] = absu('media/' + MEDIA[s['photos'][0]][0] + '.jpg')
    return d


def faq_ld(qas):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': L['hreflang'],
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qas]}


def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


# ---------- blocks ----------
def hero():
    H = S.HOME
    return f'''<section class="hero" aria-labelledby="h1">
<div class="hero-ph">{pic('colour-ash-waves-back', S.PHOTOS['colour-ash-waves-back'], eager=True, sizes='100vw')}</div>
<div class="wrap hero-in">
<div class="hero-mark">{wordmark('hero-wm', eager=True)}</div>
<i class="hairline" aria-hidden="true"></i>
<h1 id="h1">{E(H['h1'])}</h1>
<div class="hero-cta">{wa('home_hero')}{call('home_hero', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='go-ghost')}</div>
</div></section>'''


def menu_list(full=False, place='menu'):
    rows = []
    for i, k in enumerate(S.SERVICE_ORDER):
        s = S.SERVICES[k]
        rows.append(f'<li><a class="mrow" href="{pu(SVC_PATH[k])}">'
                    f'<span class="mt"><b>{E(s["zone"])}</b><small>{E(s["line"])}</small></span>{icon("go")}</a></li>')
    return f'<ol class="menu">{"".join(rows)}</ol>'


def ritual():
    li = ''.join(f'<li><span class="rn-n">{i + 1}</span><div><h3>{E(t)}</h3><p>{E(p)}</p></div></li>' for i, (t, p) in enumerate(S.STEPS))
    return f'<ol class="ritual">{li}</ol>'


def proof_band():
    H = S.HOME
    return f'''<section class="sec cream proof"><div class="wrap">
<div class="proof-in">
<p class="proof-n" aria-hidden="true">4.9</p>
<div><h2>{E(H['proof_h'])}</h2><p>{E(H['proof_p'])}</p>
<p>{ext('map', 'reviews', LK['maps'], S.UI['reviews_link'], cls='more')}</p></div>
</div></div></section>'''


def vision_block(note=True):
    zh = S.ABOUT['vision_zh_h']
    return (f'<figure class="vision"><blockquote lang="en"><p>{E(F["vision"])}</p></blockquote>'
            + (f'<p class="vision-zh" lang="zh-Hans">{E(zh)}</p>' if zh else '')
            + f'<figcaption>Studio 87</figcaption></figure>')


def visit_block():
    H = S.HOME
    return f'''<section class="sec ivory visit"><div class="wrap visit-g">
<div><h2>{E(H['visit_h'])}</h2>{address_html()}
<p class="visit-l">{ext('map', 'home_visit', LK['maps'], S.UI['directions'], cls='more', ic='pin')}</p></div>
<div>{hours_table()}</div>
</div></section>'''


def cta_band(key='default'):
    H = S.HOME
    return f'''<section class="sec band"><div class="wrap band-in">
<h2>{E(H['band_h'])}</h2><p>{E(H['band_p'])}</p>
<div class="band-cta">{wa('band', key)}{call('band', cls='go-ghost')}</div>
<p class="offers">{E(S.UI['offers'])}</p>
</div></section>'''


def page_head(h1, lead, trail, key='default'):
    return f'''<section class="phead"><div class="wrap">
{crumb_html(trail)}
<i class="hairline" aria-hidden="true"></i>
<h1>{E(h1)}</h1>
<p class="lead">{E(lead)}</p>
<div class="hero-cta">{wa('page_head', key)}</div>
</div></section>'''


def faq_html(qas, h=None):
    items = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in qas)
    return (f'<h2>{E(h)}</h2>' if h else '') + f'<div class="faq">{items}</div>'


def social_line():
    return (f'<p class="social">{E(S.UI["more_work"])} '
            f'{ext("facebook", "work", LK["facebook"], S.UI["facebook"], cls="more", ic="fb")} '
            f'{ext("instagram", "work", LK["instagram"], S.UI["instagram"], cls="more", ic="ig")}</p>')


# ---------- pages ----------
def page_home():
    H = S.HOME
    body = (hero()
            + f'''<section class="sec ivory promise"><div class="wrap narrow">
<h2>{E(H['promise_h'])}</h2><p class="lead-dark">{E(H['promise'])}</p></div></section>
<section class="sec ivory work" aria-labelledby="work-h"><div class="wrap">
<h2 id="work-h">{E(H['rail_h'])}</h2></div>
{rail(RAIL, S.UI['rail_label'])}
<div class="wrap">{social_line()}</div></section>
<section class="sec cream"><div class="wrap menu-g">
<div class="menu-h"><h2>{E(H['menu_h'])}</h2><p>{E(H['menu_p'])}</p></div>
{menu_list()}</div></section>
<section class="sec ivory"><div class="wrap"><div class="panel">
<h2>{E(H['ritual_h'])}</h2>{ritual()}</div></div></section>'''
            + proof_band()
            + f'''<section class="sec ivory"><div class="wrap narrow"><h2 class="vis-h">{E(H['vision_h'])}</h2>{vision_block()}</div></section>'''
            + visit_block() + cta_band())
    ld = [org_ld(), site_ld()]
    return head('', H['title'], H['meta'], ld, hero='colour-ash-waves-back') + header('') + body + footer()


def page_services():
    P = S.SERVICES_PAGE
    trail = [('', S.UI['home']), ('services/', S.UI['services'])]
    qas = [S.SERVICES[k]['faq'][0] for k in S.SERVICE_ORDER]
    body = (page_head(P['h1'], P['lead'], trail)
            + f'''<section class="sec ivory"><div class="wrap">{menu_list(full=True)}</div></section>
<section class="sec cream work"><div class="wrap"><h2>{E(S.UI['gallery_h'])}</h2></div>
{rail(RAIL, S.UI['rail_label'])}<div class="wrap">{social_line()}</div></section>
<section class="sec ivory"><div class="wrap narrow">{faq_html(qas, P['faq_h'])}</div></section>'''
            + cta_band())
    ld = [org_ld(), crumb_ld(trail), faq_ld(qas)]
    return head('services/', P['title'], P['meta'], ld) + header('services/') + body + footer()


def page_service(k):
    s = S.SERVICES[k]
    path = SVC_PATH[k]
    trail = [('', S.UI['home']), ('services/', S.UI['services']), (path, s['zone'])]
    pts = ''.join(f'<li>{E(p)}</li>' for p in s['points'])
    if s['photos']:
        media = rail(s['photos'], S.UI['rail_label'], cls='short') if len(s['photos']) > 1 else card(s['photos'][0])
        work = f'<section class="sec cream work"><div class="wrap"><h2>{E(S.UI["gallery_h"])}</h2></div>{media}<div class="wrap">{social_line()}</div></section>'
    else:
        work = f'<section class="sec cream"><div class="wrap narrow">{social_line()}</div></section>'
    others = ''.join(f'<li><a href="{pu(SVC_PATH[o])}">{E(S.SERVICES[o]["zone"])}</a></li>' for o in S.SERVICE_ORDER if o != k)
    body = (page_head(s['h1'], s['lead'], trail, k)
            + f'''<section class="sec ivory"><div class="wrap svc-g">
<div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['body'])}</div>
<ul class="points">{pts}</ul>
</div></section>''' + work
            + f'''<section class="sec ivory"><div class="wrap narrow">{faq_html(s['faq'], S.SERVICES_PAGE['faq_h'])}
<h2 class="oth-h">{E(S.UI['other_services'])}</h2><ul class="others">{others}</ul></div></section>'''
            + cta_band(k))
    ld = [org_ld(), service_ld(k), crumb_ld(trail), faq_ld(s['faq'])]
    return head(path, s['title'], s['meta'], ld) + header(path) + body + footer()


def page_about():
    A = S.ABOUT
    trail = [('', S.UI['home']), ('about/', S.UI['about'])]
    body = (page_head(A['h1'], A['lead'], trail)
            + f'''<section class="sec ivory"><div class="wrap narrow prose">{''.join(f'<p>{E(p)}</p>' for p in A['body'])}</div></section>
<section class="sec cream"><div class="wrap narrow"><h2 class="vis-h">{E(S.HOME['vision_h'])}</h2>{vision_block()}</div></section>
<section class="sec ivory work"><div class="wrap"><h2>{E(A['interior_h'])}</h2></div>
{rail(['colour-ash-waves-salon', 'colour-ash-waves-side', 'colour-ash-waves-back'], S.UI['rail_label'], cls='short')}</section>'''
            + visit_block() + cta_band())
    ld = [org_ld(), crumb_ld(trail)]
    return head('about/', A['title'], A['meta'], ld) + header('about/') + body + footer()


def page_contact():
    C = S.CONTACT
    trail = [('', S.UI['home']), ('contact/', S.UI['contact'])]
    body = (page_head(C['h1'], C['lead'], trail)
            + f'''<section class="sec ivory"><div class="wrap ct-g">
<div class="ct-card"><h2>{E(S.UI['contact_h'])}</h2>
<div class="ct-cta">{wa('contact')}{call('contact', cls='go-line')}</div>
<h2>{E(S.UI['address_h'])}</h2>{address_html()}
<p>{ext('map', 'contact', LK['maps'], S.UI['directions'], cls='more', ic='pin')}</p>
<h2>{E(S.UI['hours_h'])}</h2>{hours_table()}
<h2>{E(C['social_h'])}</h2><ul class="ct-soc">
<li>{ext('facebook', 'contact', LK['facebook'], S.UI['facebook'], cls='more', ic='fb')}</li>
<li>{ext('instagram', 'contact', LK['instagram'], S.UI['instagram'] + ' ' + LK['instagram_handle'], cls='more', ic='ig')}</li></ul></div>
<div class="ct-map"><iframe title="{E(S.UI['map_title'])}" src="{E(LK['maps_embed'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</div></section>''')
    ld = [org_ld(), crumb_ld(trail)]
    return head('contact/', C['title'], C['meta'], ld) + header('contact/') + body + footer()


def page_articles():
    A = S.ARTICLES
    trail = [('', S.UI['home']), ('articles/', S.UI['articles'])]
    body = (page_head(A['h1'], A['lead'], trail)
            + f'<section class="sec ivory"><div class="wrap narrow"><p class="empty">{E(A["empty"])}</p>{social_line()}</div></section>')
    ld = [org_ld(), crumb_ld(trail)]
    return head('articles/', A['title'], A['meta'], ld) + header('articles/') + body + footer()


def page_privacy():
    P = S.PRIVACY
    trail = [('', S.UI['home']), ('privacy/', S.UI['privacy'])]
    secs = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = (f'''<section class="phead"><div class="wrap">{crumb_html(trail)}<i class="hairline" aria-hidden="true"></i><h1>{E(P['h1'])}</h1></div></section>
<section class="sec ivory"><div class="wrap narrow prose">{secs}<p class="note">{E(P['updated'])}</p></div></section>''')
    ld = [org_ld(), crumb_ld(trail)]
    return head('privacy/', P['title'], P['meta'], ld) + header('privacy/') + body + footer()


def render(path):
    if path == '':
        return page_home()
    if path == 'services/':
        return page_services()
    for k, p in SVC_PATH.items():
        if p == path:
            return page_service(k)
    return {'about/': page_about, 'contact/': page_contact, 'articles/': page_articles, 'privacy/': page_privacy}[path]()


def llms_txt():
    en = strings_en
    lines = [f'# {NAME}', '', f'> {en.LLMS["summary"]}', '',
             f'- Category: {F["category"]}', f'- Since: {F["established_year"]}',
             f'- Address: {F["address"]["one_line"]}', f'- WhatsApp / phone: {F["phone"]["intl"]} ({F["whatsapp"]["url"]})',
             f'- Hours: {en.HOURS_SHORT}', f'- Google rating: {F["reviews"]["rating"]} from {F["reviews"]["count"]} Google reviews ({F["reviews"]["as_of"]})',
             f'- Maps: {LK["maps"]}', f'- Facebook: {LK["facebook"]}', f'- Instagram: {LK["instagram"]}',
             f'- Languages: English, 简体中文 ({absu("zh/")})', f'- Vision: "{F["vision"]}"', '', '## Pages', '']
    for p in PAGES:
        lines.append(f'- [{page_title_en(p)}]({absu(p)}) / [中文]({absu("zh/" + p)})')
    lines += ['', '## Services', '']
    for k in en.SERVICE_ORDER:
        lines.append(f'- {en.SERVICES[k]["zone"]} ({strings_zh.SERVICES[k]["zone"]}): {en.SERVICES[k]["line"]} {absu(SVC_PATH[k])}')
    lines += ['', 'No prices are published; quotes are given after a consultation on WhatsApp.', '']
    return '\n'.join(lines)


def page_title_en(p):
    en = strings_en
    if p == '':
        return en.HOME['title']
    if p == 'services/':
        return en.SERVICES_PAGE['title']
    for k, sp in SVC_PATH.items():
        if sp == p:
            return en.SERVICES[k]['title']
    return {'about/': en.ABOUT, 'contact/': en.CONTACT, 'articles/': en.ARTICLES, 'privacy/': en.PRIVACY}[p]['title']


def check_keys():
    def keys(m):
        out = set()
        for n in dir(m):
            if n.isupper():
                v = getattr(m, n)
                out.add(n)
                if isinstance(v, dict):
                    out |= {f'{n}.{k}' for k in v}
                    for k, vv in v.items():
                        if isinstance(vv, dict):
                            out |= {f'{n}.{k}.{kk}' for kk in vv}
        return out
    a, b = keys(strings_en), keys(strings_zh)
    if a != b:
        sys.exit(f'string keys differ: {sorted(a ^ b)}')


def main():
    global S, L
    check_keys()
    if os.path.exists(OUT):
        import shutil
        shutil.rmtree(OUT)
    for lang in I18N.LANGS:
        L, S = lang, STRINGS[lang['code']]
        for p in PAGES:
            d = os.path.join(OUT, I18N.page_path(L, p))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(render(p))
    L, S = I18N.LANGS[0], strings_en
    import shutil
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'),
                    ignore=shutil.ignore_patterns('fonts-src', '*.txt'))
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write(I18N.sitemap_xml(absu, PAGES, TODAY))
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write(llms_txt())
    print(f'built {len(PAGES) * len(I18N.LANGS)} pages -> {os.path.relpath(OUT)} (BASE {BASE}, canonical {SITE})')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""AP Car (Ap Car Air-Cond Centre, Kuantan): build the ARTICLES section only.

The 42 preview pages were built outside this repo and are live at
https://autoseo.my/preview/apcar/. This script writes, into site/:
  articles/<slug>/index.html, ms/articles/<slug>/, zh/articles/<slug>/
  articles/index.html (+ ms/, zh/)  - the article lists
  assets/articles.css               - article-only styles (site.css is NOT touched)
Header, drawer, footer and dock come from templates/ (1:1 copies of the live
pages), so every article uses the same shared parts. Every page is noindex
while config.json preview is true, and no article goes into a sitemap.

Run:  python3 autoseo-clients/apcar/src/build.py      (stops if a check fails)
"""
import datetime, hashlib, html, json, os, re, shutil, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site')
LANGS = ['en', 'ms', 'zh']


def load(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return json.load(f) if p.endswith('.json') else f.read()


C = load('config.json')
PH = load('data/photos.json')
S = {l: load(f'strings/{l}.json') for l in LANGS}
T = {n: load(f'templates/{n}.html') for n in ('header', 'footer', 'wa_svg')}
WA_SVG = T['wa_svg'].strip()
BASE = C['base_path']
SITE = C['site_url']
PHONE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" '
             'd="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/></svg>')
TONE = {'aircond': 't1', 'adas': 't2', 'hybrid': 't3', 'ecu': 't4', 'battery': 't5', 'servicing': 't6'}
DEFAULT_PREFILL = {
    'en': 'Hi AP Car, I have a question about my car. Car model:',
    'ms': 'Hi AP Car, saya ada soalan tentang kereta saya. Model kereta:',
    'zh': '你好 AP Car，我想咨询汽车问题。车型：',
}
e = html.escape


def fill(tpl, d):
    out = re.sub(r'\{\{([a-zA-Z0-9_\-]+)\}\}', lambda m: str(d[m.group(1)]), tpl)
    return out


def wa(text):
    return f"https://wa.me/{C['whatsapp']}?text=" + urllib.parse.quote(text, safe='')


def L(lang):
    return BASE + S[lang]['prefix']


def abs_url(lang, path):
    return SITE + S[lang]['prefix'] + path


def fmt_date(lang, iso):
    y, m, d = iso.split('-')
    a = S[lang]['articles']
    return a['date_fmt'].format(d=int(d), m=a['months'][int(m) - 1], y=y)


def img(key, lang, sizes, lazy=True):
    p = PH[key]
    alt = e(p[lang])
    s4 = f"{BASE}assets/img/{key}-480.webp"
    s9 = f"{BASE}assets/img/{key}-960.webp"
    load_attr = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return (f'<img src="{s4}" srcset="{s4} 480w, {s9} 960w" sizes="{sizes}" width="{p["w"]}" height="{p["h"]}" '
            f'alt="{alt}"{load_attr} decoding="async">')


def figure(key, lang, sizes):
    return f'<figure>{img(key, lang, sizes)}<figcaption>{e(PH[key][lang])}</figcaption></figure>'


def business_node():
    days6 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return {
        '@type': 'AutoRepair', '@id': SITE + '#business', 'name': C['name'],
        'alternateName': ['AP Car', 'AP CAR AIR-COND CENTRE', '汽車維修中心'],
        'url': SITE, 'telephone': C['phone_e164'], 'email': C['email'],
        'image': SITE + 'assets/img/shopfront-960.webp',
        'address': {'@type': 'PostalAddress', 'streetAddress': C['street'], 'postalCode': C['postcode'],
                    'addressLocality': C['locality'], 'addressRegion': C['region'], 'addressCountry': 'MY'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': C['lat'], 'longitude': C['lng']},
        'hasMap': C['maps_url'],
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': days6, 'opens': '09:00', 'closes': '18:30'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Sunday', 'opens': '11:00', 'closes': '15:00'}],
        'areaServed': {'@type': 'City', 'name': 'Kuantan'},
        'knowsLanguage': ['en', 'ms', 'zh'],
        'sameAs': [C['facebook_url'], C['tiktok_url'], C['maps_url']],
    }


def head(lang, title, desc, path, graph, og_type='website', og_image=None):
    s = S[lang]
    robots = 'noindex,nofollow' if C['preview'] else 'index,follow'
    alts = ''.join(f'<link rel="alternate" hreflang="{S[x]["hreflang"]}" href="{abs_url(x, path)}">' for x in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{abs_url("en", path)}">'
    og_img = og_image or SITE + C['og_image']
    v = C['site_asset_v']
    return (
        f'<!doctype html>\n<html lang="{s["html_lang"]}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}">\n'
        f'<meta name="robots" content="{robots}">\n<link rel="canonical" href="{abs_url(lang, path)}">\n{alts}\n'
        '<meta name="theme-color" content="#15122f">\n'
        f'<meta property="og:type" content="{og_type}"><meta property="og:title" content="{e(title)}">'
        f'<meta property="og:description" content="{e(desc)}">\n'
        f'<meta property="og:url" content="{abs_url(lang, path)}"><meta property="og:image" content="{og_img}">'
        f'<meta property="og:locale" content="{s["og_locale"]}">\n'
        f'<link rel="preload" href="{BASE}assets/fonts/big-shoulders-display.woff2" as="font" type="font/woff2" crossorigin>\n'
        f'<link rel="stylesheet" href="{BASE}assets/site.css?v={v}">\n'
        f'<link rel="stylesheet" href="{BASE}assets/articles.css?v={ART_CSS_V}">\n'
        f'<link rel="icon" href="{BASE}assets/favicon.svg" type="image/svg+xml">\n'
        '<script>document.documentElement.classList.add("js")</script>\n'
        '<script type="application/ld+json">'
        + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
        + '</script>\n</head>\n')


def shared(lang, path, P, wa_url):
    s = S[lang]
    d = {'L': L(lang), 'BASE': BASE, 'path': path, 'P': P, 'WA': e(wa_url), 'WA_SVG': WA_SVG,
         'articles_nav': s['articles']['nav'], 'year': datetime.date.today().year, 'site_v': C['site_asset_v'],
         'maps': e(C['maps_url']), 'tel': C['phone_e164'], 'phone': C['phone_display'], 'email': C['email'],
         'tiktok': C['tiktok_url'], 'facebook': C['facebook_url'], 'address': e(C['address_display'])}
    for x in LANGS:
        d['cur_' + x] = 'page' if x == lang else 'false'
    for k, v in s.items():
        if isinstance(v, str):
            d[k] = v
    for k, v in s['svc'].items():
        d['svc_' + k] = v
    for k, v in s['brand'].items():
        d['brand_' + k] = v
    d['hours_rows'] = ''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in s['hours_rows'])
    return fill(T['header'], d), fill(T['footer'], d)


def btns(lang, P, ref, wa_url):
    s = S[lang]
    return (f'<div class="btn-row{" on-ink" if ref == "band" else ""}"><a class="btn btn-wa" href="{e(wa_url)}" target="_blank" rel="noopener" '
            f'data-cta="whatsapp_{P}_{ref}" data-ref="{ref}">{WA_SVG}<span>{s["wa_us"]}</span></a>'
            f'<a class="btn btn-ghost" href="tel:{C["phone_e164"]}" data-cta="call_{P}_{ref}" data-ref="{ref}">{PHONE_SVG}'
            f'<span>{s["call"]}</span></a></div>')


def crumbs(lang, items):
    parts = []
    for name, href in items:
        parts.append(f'<a href="{href}">{e(name)}</a>' if href else e(name))
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span>/</span>'.join(parts) + '</nav>'


def crumb_schema(lang, items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': html.unescape(n), 'item': u}
        for i, (n, u) in enumerate(items)]}


def read_minutes(lang, a):
    text = ' '.join([a['lead'], a['answer']] + [json.dumps(x, ensure_ascii=False) for x in a['sections']])
    n = len(text) / 450 if lang == 'zh' else len(text.split()) / 200
    return max(2, round(n + 0.5))


def section_html(lang, sec):
    out = ['<section class="sec aa-sec"><div class="wrap">', f'<div class="sec-h"><h2>{e(sec["h2"])}</h2></div>']
    for p in sec.get('p', []):
        out.append(f'<p class="aa-p">{e(p)}</p>')
    if 'list' in sec:
        out.append('<ul class="signs">' + ''.join(f'<li>{e(x)}</li>' for x in sec['list']) + '</ul>')
    if 'steps' in sec:
        out.append('<ol class="steps">' + ''.join(
            f'<li><b>{i + 1:02d}</b><div><strong>{e(a)}</strong><span>{e(b)}</span></div></li>'
            for i, (a, b) in enumerate(sec['steps'])) + '</ol>')
    if 'jobs' in sec:
        out.append('<ol class="joblist">' + ''.join(f'<li>{e(x)}</li>' for x in sec['jobs']) + '</ol>')
    if 'pair' in sec:
        out.append('<div class="aa-pair">' + ''.join(figure(k, lang, '(min-width:720px) 40vw, 92vw') for k in sec['pair']) + '</div>')
    if 'photo' in sec:
        out.append('<div class="aa-photo">' + figure(sec['photo'], lang, '(min-width:720px) 360px, 70vw') + '</div>')
    out.append('</div></section>')
    return '\n'.join(out)


def article_page(lang, art, all_arts):
    s, sa, a = S[lang], S[lang]['articles'], art[lang]
    slug = art['slug']
    path = f'articles/{slug}/'
    url = abs_url(lang, path)
    wa_url = wa(a['prefill'])
    P = 'article'
    hdr, ftr = shared(lang, path, P, wa_url)
    svc = art['service']
    svc_path = C['services'][svc]
    svc_name = s['svc'][svc]
    trail = [(s['home'], L(lang)), (sa['nav'], L(lang) + 'articles/'), (a['h1'], None)]
    trail_s = [(s['home'], abs_url(lang, '')), (sa['nav'], abs_url(lang, 'articles/')), (a['h1'], url)]
    hero = art['hero_photo']
    graph = [
        business_node(),
        {'@type': 'Article', '@id': url + '#article', 'headline': a['h1'], 'description': a['description'],
         'inLanguage': s['hreflang'], 'datePublished': art['published'], 'dateModified': art['updated'],
         'image': SITE + f'assets/img/{hero}-960.webp', 'mainEntityOfPage': url,
         'author': {'@id': SITE + '#business'}, 'publisher': {'@id': SITE + '#business'},
         'about': {'@id': SITE + '#business'}, 'keywords': a['keyword']},
        crumb_schema(lang, trail_s),
        {'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in a['faqs']]},
    ]
    others = [x for x in all_arts if x['slug'] != slug][:3]
    rel = [f'<a href="{L(lang)}{svc_path}"><i class="{TONE[svc]}"></i><span>{svc_name}</span></a>']
    for o in others:
        rel.append(f'<a href="{L(lang)}articles/{o["slug"]}/"><i class="{TONE[o["service"]]}"></i><span>{e(o[lang]["h1"])}</span></a>')
    body = [
        hdr,
        '<main id="main" class="aa">',
        '<section class="sh">',
        f'<div class="sh-media"><p class="k">{sa["k"]}</p>{img(hero, lang, "(min-width:1024px) 50vw, 100vw", lazy=False)}</div>',
        f'<div class="sh-copy wrap">{crumbs(lang, trail)}<h1>{e(a["h1"])}</h1>'
        f'<div class="tag"><time datetime="{art["published"]}">{fmt_date(lang, art["published"])}</time> · {sa["min"].format(n=read_minutes(lang, a))}</div>',
        btns(lang, P, 'hero', wa_url) + '</div>',
        '</section>',
        f'<section class="intro"><div class="wrap"><p>{e(a["lead"])}</p></div></section>',
        f'<section class="sec aa-sec"><div class="wrap"><div class="aa-ans"><p class="k">{sa["answer"]}</p><p>{e(a["answer"])}</p>'
        f'<a class="lnk" href="{L(lang)}{svc_path}">{sa["service_cta"]}: {svc_name} →</a></div></div></section>',
    ]
    body += [section_html(lang, sec) for sec in a['sections']]
    body += [
        f'<section class="sec aa-sec"><div class="wrap two"><div><p class="k">{sa["faq_h2"]}</p><h2>{sa["faq_h2"]}</h2></div><div class="faq">'
        + ''.join(f'<details><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>' for f in a['faqs'])
        + '</div></div></section>',
        f'<section class="sec aa-sec" style="padding-top:0"><div class="wrap"><div class="sec-h"><p class="k">{sa["more_k"]}</p></div>'
        f'<div class="rel">{"".join(rel)}</div></div></section>',
        f'<section class="band"><div class="wrap"><p>{sa["end_h"]} {sa["end_p"]}</p>{btns(lang, P, "band", wa_url)}</div></section>',
        '</main>',
        ftr,
    ]
    return head(lang, a['title'], a['description'], path, graph, 'article', SITE + f'assets/img/{hero}-960.webp') + '\n'.join(body)


def index_page(lang, arts):
    s, sa = S[lang], S[lang]['articles']
    path = 'articles/'
    url = abs_url(lang, path)
    wa_url = wa(DEFAULT_PREFILL[lang])
    P = 'articles'
    hdr, ftr = shared(lang, path, P, wa_url)
    trail = [(s['home'], L(lang)), (sa['nav'], None)]
    trail_s = [(s['home'], abs_url(lang, '')), (sa['nav'], url)]
    graph = [
        business_node(),
        {'@type': 'CollectionPage', '@id': url, 'url': url, 'name': sa['h1'], 'description': sa['description'],
         'inLanguage': s['hreflang'], 'about': {'@id': SITE + '#business'},
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [
             {'@type': 'ListItem', 'position': i + 1, 'url': abs_url(lang, f'articles/{x["slug"]}/'), 'name': x[lang]['h1']}
             for i, x in enumerate(arts)]}},
        crumb_schema(lang, trail_s),
    ]
    cards = []
    for x in arts:
        a = x[lang]
        cards.append(
            f'<a class="art-card aa-card" href="{L(lang)}articles/{x["slug"]}/">'
            f'{img(x["hero_photo"], lang, "(min-width:720px) 30vw, 92vw")}'
            f'<div><span class="aa-tag"><i class="{TONE[x["service"]]}"></i>{s["svc"][x["service"]]}</span>'
            f'<time datetime="{x["published"]}">{fmt_date(lang, x["published"])}</time>'
            f'<h3>{e(a["h1"])}</h3><p>{e(a["excerpt"])}</p><b>{sa["read"]} →</b></div></a>')
    body = [
        hdr,
        '<main id="main" class="aa aa-list">',
        f'<section class="sh aa-sh"><div class="sh-copy wrap">{crumbs(lang, trail)}<p class="k on-dark">{sa["k"]}</p>'
        f'<h1>{sa["h1"]}</h1><div class="tag">{sa["tag"]}</div>{btns(lang, P, "hero", wa_url)}</div></section>',
        f'<section class="sec"><div class="wrap"><div class="sec-h"><h2>{sa["list_h2"]}</h2></div>'
        f'<div class="aa-cards">{"".join(cards)}</div></div></section>',
        f'<section class="band"><div class="wrap"><p>{sa["end_h"]} {sa["end_p"]}</p>{btns(lang, P, "band", wa_url)}</div></section>',
        '</main>',
        ftr,
    ]
    return head(lang, sa['title'], sa['description'], path, graph) + '\n'.join(body)


def load_articles():
    d = os.path.join(ROOT, 'data', 'articles')
    arts = []
    for f in sorted(os.listdir(d)):
        if f.endswith('.json'):
            arts.append(load(f'data/articles/{f}'))
    arts.sort(key=lambda x: (x['published'], x['slug']), reverse=True)
    return arts


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)


css_path = os.path.join(ROOT, 'assets', 'articles.css')
ART_CSS_V = hashlib.sha1(open(css_path, 'rb').read()).hexdigest()[:8]


def main():
    arts = load_articles()
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for lang in LANGS:
        pre = S[lang]['prefix']
        write(f'{pre}articles/index.html', index_page(lang, arts))
        for art in arts:
            write(f'{pre}articles/{art["slug"]}/index.html', article_page(lang, art, arts))
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    shutil.copy(css_path, os.path.join(OUT, 'assets', 'articles.css'))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check
    errs = check.run(ROOT, OUT, C, S, arts)
    if errs:
        print('\n'.join('FAIL ' + x for x in errs))
        sys.exit(1)
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f'OK: {len(arts)} article(s) x 3 languages + 3 lists, {n} files in {OUT}')


if __name__ == '__main__':
    main()

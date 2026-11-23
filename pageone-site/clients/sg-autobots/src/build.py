#!/usr/bin/env python3
"""SgAutobots preview builder (23 Nov 2026). One facts.json + one site.json drive every page.
Shared template pieces in this file: head(), header(), footer(), bar(), cta_pair()/book_href() (CTA + Book block),
price_board() (price tables), area_page() (shared area template), schema helpers (org(), service_ld(), faq_ld(), crumbs_ld()).
Preview build only: Rule 0 forbids re-running this over live files later; later changes are read_live -> edit -> write."""
import json, os, sys, hashlib, html, re, urllib.parse as up
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/mnt/project-files/autoseo-template/golive'); import golive
sys.path.insert(0, '/mnt/project-files/autoseo-template/privacy'); import privacy_page as PV
F = json.load(open(os.path.join(HERE, 'facts.json')))
AREAS = json.load(open(os.path.join(HERE, 'areas.json')))
CFG = golive.load(os.path.join(HERE, 'site.json'))
P, BASE = golive.build_base(os.path.join(HERE, 'site.json'))   # '/preview/sg-autobots', 'https://pageonesingapore.com/preview/sg-autobots'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sga/dist'
UPDATED = '23 Nov 2026'; LASTMOD = '2026-11-23'
FL = F['flags']; SV = F['services']; SVB = {s['slug']: s for s in SV}; AB = {a['slug']: a for a in AREAS}
GAL = {g['id']: g for g in F['gallery']}; VID = {v['id']: v for v in F['videos']}
e = lambda s: html.escape(str(s), quote=True)
PAGES = []  # (path, title) for sitemap/llms

def vhash(name):
    return hashlib.sha256(open(os.path.join(HERE, name), 'rb').read()).hexdigest()[:8]
VCSS, VJS, VCTA = vhash('site.css'), vhash('site.js'), vhash('p1-cta.js')

# ---------- icons (one stroke set + brand glyphs) ----------
I_WA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2.2A9.7 9.7 0 0 0 3.7 16.9L2.3 21.8l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.5Z"/></svg>'
I_CAL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17M8.5 14.5l2.3 2.3 4.7-4.6"/></svg>'
I_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3.5h3.5l1.8 4.5-2.3 1.4a11 11 0 0 0 6.6 6.6l1.4-2.3 4.5 1.8V19a2 2 0 0 1-2 2A17 17 0 0 1 3 5.5a2 2 0 0 1 2-2Z"/></svg>'
I_CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>'
I_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M7 4.5v15l12.5-7.5z"/></svg>'
I_SWIPE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M8 8l-4 4 4 4M16 8l4 4-4 4"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
SOC_ICON = {
 'facebook': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4a21 21 0 0 0-2.3-.1c-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/></svg>',
 'instagram': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor"/></svg>',
 'tiktok': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M16.6 3c.4 2.1 1.7 3.5 3.9 3.7v3a7 7 0 0 1-3.9-1.2v6.3A5.8 5.8 0 1 1 10.8 9v3.1a2.8 2.8 0 1 0 2 2.7V3z"/></svg>',
 'carousell': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M17.5 7.2A7 7 0 1 0 17.5 16.8"/></svg>'}
SOC_LABEL = {'facebook': 'Facebook', 'instagram': 'Instagram', 'tiktok': 'TikTok', 'carousell': 'Carousell'}

# ---------- CTA + Book block (shared) ----------
def wa_href(text):
    return 'https://wa.me/%s?text=%s' % (F['wa_number'], up.quote(text, safe=''))
def wa_text(kind='quote', svc=None, area=None):
    if area and svc: return "Hi SgAutobots, can you come to %s for %s? Car model: " % (area['name'], svc['name'].lower())
    if area: return "Hi SgAutobots, can you come to my car park in %s? Car model: " % area['name']
    if svc: return "Hi SgAutobots, I'd like a quote for %s. Car model: " % svc['name'].lower()
    return "Hi SgAutobots, I'd like a quote for mobile car detailing. Car model: "
def book_href(svc=None):
    if F['booking_url']:
        u = F['booking_url'] + ('&' if '?' in F['booking_url'] else '?') + 'client=sg-autobots' + ('&service=' + svc['slug'] if svc else '')
        return u
    return wa_href(F['booking_prefill'].format(package=(svc['name'] + '.') if svc else '…'))
def a_wa(ref, text, label='WhatsApp us', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="%s">%s<span>%s</span></a>' % (cls, e(wa_href(text)), ref, I_WA, label)
def a_book(ref, svc=None, label='Book a slot', cls='btn btn-book'):
    ds = ' data-service="%s"' % svc['slug'] if svc else ''
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-cta="booking" data-ref="%s"%s>%s<span>%s</span></a>' % (cls, e(book_href(svc)), ref, ds, I_CAL, label)
def a_call(ref, label=None, cls='btn btn-ghost'):
    return '<a class="%s" href="tel:%s" data-cta="call" data-ref="%s">%s<span>%s</span></a>' % (cls, F['tel'], ref, I_TEL, label or 'Call ' + F['phone_display'])
def cta_pair(ref_wa, ref_book, text, svc=None):
    return '<div class="cta-pair">%s%s</div>' % (a_wa(ref_wa, text), a_book(ref_book, svc))

def u(path=''):  # site-relative URL
    return P + '/' + path
def img(gid, sizes='(max-width:700px) 74vw, 300px', lazy=True, cls='', alt=None):
    g = GAL[gid]
    return ('<picture><source type="image/webp" srcset="%s"><img src="%s" width="%d" height="%d" alt="%s"%s%s style="object-position:%s"></picture>'
            % (u('images/gallery/%s.webp' % g['file']), u('images/gallery/%s.jpg' % g['file']), g['w'], g['h'], e(alt or g['alt']),
               ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"', (' class="%s"' % cls) if cls else '', g['pos']))

# ---------- prices ----------
def min_price(p):
    if 'prices' in p: return min(x for x in p['prices'] if x)
    if 'range' in p: return p['range'][0]
    if 'fixed' in p: return min(x[1] for x in p['fixed'])
    if 'from' in p: return p['from']
    if 'from_text' in p: return int(re.sub(r'\D', '', p['from_text']))
def svc_from(s): return min(min_price(p) for p in s['packages'])
def money(n): return 'S$' + format(n, ',')
def price_html(p):
    if 'prices' in p:
        dp = ','.join(str(x) if x else '-' for x in p['prices'])
        return '<p class="p" data-prices="%s"><span class="v">%s</span><small>size <span class="sz">S</span></small></p>' % (dp, money(p['prices'][0]))
    if 'range' in p: return '<p class="p">%s-%s</p>' % (money(p['range'][0]), format(p['range'][1], ','))
    if 'fixed' in p: return '<p class="p">%s</p>' % ' / '.join('%s <small>%s</small>' % (money(v), e(k)) for k, v in p['fixed'])
    if 'from' in p: return '<p class="p">from %s</p>' % money(p['from'])
    return '<p class="p">%s</p>' % e(p['from_text'])
def size_table(p):
    if 'prices' not in p: return ''
    rows = ''.join('<tr data-i="%d"><th scope="row">%s</th><td>%s</td></tr>' % (i, z, money(v) if v else 'not listed') for i, (z, v) in enumerate(zip(F['sizes'], p['prices'])))
    return '<table class="tbl"><caption class="skip">%s prices by car size</caption><tbody>%s</tbody></table>' % (e(p['name']), rows)
def clock(p):
    if 'dt' not in p: return ''
    lo, hi = p['dt']; L = lambda m: m / 960 * 100
    return ('<div class="clock">%s<span>Downtime %s%s</span><div class="bar" role="img" aria-label="Car out of use for %s"><span style="left:%.1f%%;width:%.1f%%"></span></div></div>'
            % (I_CLOCK, e(p['downtime']), (' · lasts ' + e(p['lasts'])) if p.get('lasts') else '', e(p['downtime']), L(lo), max(3, L(hi) - L(lo))))
def pkg_card(p, svc, incl=True, table=False, link=False):
    li = p.get('incl') or []
    out = ['<article class="pk">', '<h3>%s</h3>' % e(p['name']), price_html(p), clock(p)]
    if p.get('lasts') and 'dt' not in p: out.append('<p class="note">Lasts %s</p>' % e(p['lasts']))
    if p.get('note'): out.append('<p class="note">%s</p>' % e(p['note']))
    if table: out.append(size_table(p))
    if incl and li: out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % e(x) for x in li))
    if p.get('addon'): out.append('<p class="note">Add-on (S$): %s</p>' % e(p['addon']))
    if link: out.append('<a class="more" href="%s">%s prices and details</a>' % (u(svc['slug'] + '/'), e(svc['name'])))
    out.append('</article>')
    return ''.join(out)
def has_sizes(pk): return any('prices' in p for p in pk)
SWITCH = ('<div class="sizes" role="group" aria-label="Car size">%s</div><p class="size-note">Prices in S$ by car size. Not sure of your size? WhatsApp your car model.</p>'
          % ''.join('<button type="button" data-i="%d" aria-pressed="%s">%s</button>' % (i, 'true' if i == 0 else 'false', z) for i, z in enumerate(F['sizes'])))
def price_board(svc, pk=None, three=False, table=True):
    pk = pk or svc['packages']
    out = (SWITCH if has_sizes(pk) else '<p class="size-note">Not sure which package fits? WhatsApp your car model.</p>')
    out += '<div class="board%s">%s</div>' % (' three' if three else '', ''.join(pkg_card(p, svc, table=table) for p in pk))
    if svc.get('shared_incl'): out += '<div class="local" style="margin-top:14px"><h3>Every coating package includes</h3><ul>%s</ul></div>' % ''.join('<li>%s</li>' % e(x) for x in svc['shared_incl'])
    if svc.get('addons'): out += '<div class="local" style="margin-top:14px"><h3>Add-ons (S$)</h3><ul>%s</ul></div>' % ''.join('<li>%s: <b class="price">%s</b></li>' % (e(a), e(b)) for a, b in svc['addons'])
    return out

# ---------- media blocks ----------
def reel(vid, ref):
    v = VID[vid]; ar = v['w'] / v['h']
    return ('<figure class="reel-fig" style="margin:0"><a class="reel" href="%s" target="_blank" rel="noopener" data-cta="tiktok" data-ref="%s" data-src="video/%s.mp4"%s data-loop="%d" style="--w:%d;--h:%d;--ar:%.4f">'
            '<div class="frame"><img src="%s" width="%d" height="%d" alt="%s" loading="lazy" decoding="async"><span class="play">%s</span></div>'
            '<figcaption>%s</figcaption></a></figure>'
            % (e(v['tiktok']), ref, vid, '' if v['loop'] else ' data-full="video/%s.mp4"' % vid, 1 if v['loop'] else 0, v['w'], v['h'], ar,
               u('images/posters/%s.jpg' % vid), v['w'], v['h'], e(v['alt']), I_PLAY, e(v['caption'])))
def photos(ids):
    return '<div class="photos">%s</div>' % ''.join('<figure>%s<figcaption>%s</figcaption></figure>' % (img(i, '(max-width:700px) 45vw, 260px'), e(GAL[i]['caption'])) for i in ids)
def quote(r):
    return ('<figure class="qc"><blockquote class="rq">%s</blockquote><figcaption>Carousell buyer %s, %s</figcaption></figure>' % (e(r['text']), e(r['user']), e(r['date'])))
def quotes_for(slug, n=2):
    q = [r for r in F['reviews'] if slug in r['svc']]
    return q[:n] if q else F['reviews'][:n]

# ---------- schema ----------
def org():
    return {"@type": "AutoWash", "@id": BASE + "/#business", "name": F['name'], "alternateName": F['google_name'], "url": BASE + "/",
            "telephone": F['tel'], "image": BASE + "/images/gallery/g04-porsche-cayenne.jpg", "logo": BASE + "/images/brand/logo-sgautobots-503.jpg",
            "priceRange": "S$65 - S$2,588", "currenciesAccepted": "SGD",
            "address": {"@type": "PostalAddress", "addressLocality": "Singapore", "addressCountry": "SG"},
            "areaServed": [{"@type": "Country", "name": "Singapore"}] + [{"@type": "Place", "name": a['name'] + ", Singapore"} for a in AREAS],
            "sameAs": [F['maps_url'], F['socials']['facebook'], F['socials']['instagram'], F['socials']['tiktok'], F['socials']['carousell']],
            "description": F['service_line']}
def offers(svc):
    out = []
    for p in svc['packages']:
        if 'prices' in p:
            v = [x for x in p['prices'] if x]
            out.append({"@type": "AggregateOffer", "name": p['name'], "priceCurrency": "SGD", "lowPrice": min(v), "highPrice": max(v), "offerCount": len(v)})
        elif 'range' in p:
            out.append({"@type": "AggregateOffer", "name": p['name'], "priceCurrency": "SGD", "lowPrice": p['range'][0], "highPrice": p['range'][1]})
        elif 'fixed' in p:
            for k, v in p['fixed']: out.append({"@type": "Offer", "name": p['name'] + ' (' + k + ')', "priceCurrency": "SGD", "price": v})
        else:
            out.append({"@type": "Offer", "name": p['name'], "priceCurrency": "SGD", "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "SGD", "minPrice": min_price(p)}})
    return out
def service_ld(svc, path, area=None):
    d = {"@type": "Service", "@id": BASE + "/" + path + "#service", "name": svc['name'] + (' in ' + area['name'] if area else ' in Singapore'),
         "serviceType": svc['name'], "provider": {"@id": BASE + "/#business"},
         "areaServed": ({"@type": "Place", "name": area['name'] + ", Singapore"} if area else {"@type": "Country", "name": "Singapore"}),
         "url": BASE + "/" + path, "offers": offers(svc)}
    return d
def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faqs]}
def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + p} for i, (n, p) in enumerate(items)]}
def webpage_ld(path, title, desc):
    return {"@type": "WebPage", "@id": BASE + "/" + path + "#page", "url": BASE + "/" + path, "name": title, "description": desc, "inLanguage": "en-SG",
            "isPartOf": {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": F['name'], "publisher": {"@id": BASE + "/#business"}}, "dateModified": LASTMOD}

# ---------- head / header / footer / bar ----------
def head(path, title, desc, ld, og_alt="SgAutobots logo with the line: mobile car detailing in Singapore, we come to you"):
    assert len(title) <= 60, (title, len(title))
    PAGES.append((path, title))
    g = golive.head_tags(CFG, path, 'en')
    ldj = json.dumps({"@context": "https://schema.org", "@graph": [org()] + ld}, ensure_ascii=False, separators=(',', ':'))
    return ('<!doctype html>\n<html lang="en-SG" data-root="%s/">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="noindex, nofollow">\n%s\n'
            '<meta name="theme-color" content="#07090d">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="SgAutobots">\n<meta property="og:locale" content="en_SG">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:image:alt" content="%s">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%s">\n<meta name="twitter:description" content="%s">\n'
            '<link rel="icon" href="%s" sizes="32x32" type="image/png">\n<link rel="icon" href="%s" sizes="192x192" type="image/png">\n<link rel="apple-touch-icon" href="%s">\n'
            '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>\n<link rel="stylesheet" href="%s?v=%s">\n<script type="application/ld+json">%s</script>\n</head>\n'
            % (P, e(title), e(desc), g, e(title), e(desc), e(og_alt), e(title), e(desc), u('images/brand/favicon-32.png'), u('images/brand/icon-192.png'), u('images/brand/icon-192.png'),
               u('fonts/bsd-800.woff2'), u('site.css'), VCSS, ldj.replace('</', '<\\/')))
NAV = [('Car spa', 'car-spa/'), ('Interior', 'interior-detailing/'), ('Fumigation', 'car-fumigation-odour-removal/'), ('Polishing', 'car-polishing-paint-correction/'),
       ('Ceramic coating', 'ceramic-coating/'), ('Glass & rims', 'glass-rim-coating/'), ('Engine bay', 'engine-bay-cleaning/'), ('Contact', 'contact/')]
def header(cur, svc=None):
    nav = ''.join('<a href="%s"%s>%s</a>' % (u(p), ' aria-current="page"' if p == cur else '', n) for n, p in NAV)
    sheet = ''.join('<a href="%s">%s</a>' % (u(p), n) for n, p in [('Home', '')] + NAV)
    return ('<body>\n<a class="skip" href="#main">Skip to content</a>\n<header class="hd"><div class="wrap">'
            '<a class="badge" href="%s"><img src="%s" width="44" height="44" alt="SgAutobots Car Detailing Specialist logo with Sonax mark"><b>SgAutobots</b></a>'
            '<nav class="nav" aria-label="Main">%s</nav>%s%s'
            '<details class="menu"><summary aria-label="Menu">%s</summary><div class="sheet">%s%s%s</div></details>'
            '</div></header>\n<main id="main">\n'
            % (u(''), u('images/brand/logo-sgautobots-503.jpg'), nav, a_book('booking_header', svc, 'Book', 'btn btn-book sm'), a_wa('whatsapp_header', wa_text(svc=svc), 'WhatsApp', 'btn btn-wa sm'),
               I_MENU, sheet, a_wa('whatsapp_menu', wa_text(svc=svc), 'WhatsApp us', 'btn btn-wa'), a_call('call_menu')))
def footer(svc=None):
    soc = ''.join('<a href="%s" target="_blank" rel="noopener" data-cta="%s" data-ref="%s_footer" aria-label="SgAutobots on %s">%s</a>' % (e(F['socials'][k]), k, k, SOC_LABEL[k], SOC_ICON[k]) for k in ['facebook', 'instagram', 'tiktok', 'carousell'])
    svcs = ''.join('<li><a href="%s">%s</a></li>' % (u(s['slug'] + '/'), e(s['name'])) for s in SV)
    ar = ''.join('<li><a href="%s">%s</a></li>' % (u('car-spa/' + a['slug'] + '/'), e(a['name'])) for a in AREAS[:7])
    return ('</main>\n<footer class="ft"><div class="wrap ft-in">'
            '<div><a class="badge" href="%s"><img src="%s" width="44" height="44" alt="" loading="lazy"><b>SgAutobots</b></a>'
            '<p style="margin-top:12px;color:var(--soft)">%s</p><p style="color:var(--soft)">%s</p>%s<div class="soc">%s</div></div>'
            '<div><h2>Services</h2><ul>%s</ul></div>'
            '<div><h2>Areas</h2><ul>%s<li><a href="%s#areas">All 13 areas</a></li></ul></div>'
            '<div><h2>Contact</h2><ul><li><a href="tel:%s" data-cta="call" data-ref="call_footer">Call %s</a></li>'
            '<li><a href="%s" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="whatsapp_footer">WhatsApp %s</a></li>'
            '<li><a href="%s" target="_blank" rel="noopener" data-cta="reviews" data-ref="reviews_footer">See our 5-star reviews</a></li>'
            '<li><a href="%s" data-cta="reviews" data-ref="review_helper_footer">Leave us a Google review</a></li>'
            '<li><a href="%s">Contact</a></li><li><a href="%s">Privacy</a></li></ul></div>'
            '<p class="legal">&copy; 2026 %s (%s). Sonax and Gtechniq are trademarks of their owners.</p>'
            '</div></footer>\n'
            % (u(''), u('images/brand/logo-sgautobots-503.jpg'), e(F['service_line']), e(F['hours_text']),
               a_wa('whatsapp_footer_btn', wa_text(svc=svc), 'WhatsApp ' + F['phone_display']), soc, svcs, ar, u(''),
               F['tel'], F['phone_display'], e(wa_href(wa_text(svc=svc))), F['phone_display'], e(F['reviews_url']), u('review/'), u('contact/'), u('privacy/'),
               F['legal_name'], F['legal_form']))
def bar(svc=None, area=None):
    return ('<div class="bar">%s%s<a class="btn call" href="tel:%s" data-cta="call" data-ref="call_mobile_bar" aria-label="Call %s">%s</a></div>\n'
            '<script src="%s?v=%s" defer></script>\n<script src="%s?v=%s" defer></script>\n</body>\n</html>\n'
            % (a_wa('whatsapp_mobile_bar', wa_text(svc=svc, area=area), 'WhatsApp'), a_book('booking_mobile_bar', svc, 'Book'), F['tel'], F['phone_display'], I_TEL,
               u('site.js'), VJS, u('p1-cta.js'), VCTA))
def crumbs(items):
    parts = []
    for i, (n, p) in enumerate(items):
        parts.append('<span aria-current="page">%s</span>' % e(n) if i == len(items) - 1 else '<a href="%s">%s</a>' % (u(p), e(n)))
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
def faq_html(faqs):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), a) for q, a in faqs)
def write(path, s):
    fp = os.path.join(OUT, path, 'index.html') if not path.endswith('.html') else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'w').write(s)

def area_strip(svc_slug='car-spa', ref='area'):
    return '<div class="areas">%s</div>' % ''.join('<a href="%s">%s <small>%s km</small></a>' % (u(svc_slug + '/' + a['slug'] + '/'), e(a['name']), a['km']) for a in AREAS)
REST = 'We also come to the rest of Singapore, WhatsApp your area.'

# ---------- service copy (only from facts.md) ----------
def dt_range(s):
    ds = [p['dt'] for p in s['packages'] if 'dt' in p]
    f = lambda m: ('%d min' % m) if m < 60 else (('%g h' % (m / 60)))
    return f(min(d[0] for d in ds)), f(max(d[1] for d in ds))
INTRO = {
 'car-spa': "A Maintenance Car Spa starts at S$65 for a size S car and takes 50 min to 1.5 h; the full Sonax Carspa is S$268-S$468 over 4-8 h. We come to your HDB or condo car park with the full mobile kit, so you never drive to a workshop.",
 'interior-detailing': "Sonax Premium Interior Detailing starts at S$148 (size S, 3-6 h), and Deep Interior Detailing & Coating with fumigation and extraction is S$388-S$688 over 4-8 h. We bring the extractor, steamer and Sonax products to your car park.",
 'car-fumigation-odour-removal': "Pest Fumigation & Interior Cleaning is S$108-S$268 and your car is out of use for 2-3 h. We do it at your own car park, with steaming, vacuum, leather seat cleaning and Sonax Air included.",
 'car-polishing-paint-correction': "Car Wash & Polish Seal starts at S$168 (size S, 2-4 h), and paint correction is S$200-S$2,000 over 4-15 h, free with Sonax CCEVO and Gtechniq coating. We machine polish at your car park, not at a workshop.",
 'ceramic-coating': "Sonax ceramic coating starts at S$368 for Ceramic Lite (size S, 4-8 h, lasts 9 months) and goes up to Gtechniq 5-9 years from S$1,488. We prep, polish and coat at your HDB or condo car park.",
 'glass-rim-coating': "Glass Water Mark Removal & Coating starts at S$188 (size S, 2-5 h, lasts 6-12 months), windscreen polish & sealant from S$80 and Gtechniq rim coating from S$200. We do it at your car park.",
 'engine-bay-cleaning': "Engine Bay Restoration is S$88-S$128 and takes 45 min to 2 h, with steaming as an add-on (listed at 50+, in S$). We clean the engine bay right where your car is parked.",
}
FAQS = {
 'car-spa': [("How much is a car spa?", "A Maintenance Car Spa (try once) is S$65 / S$75 / S$85 / S$95 for sizes S / M / L / XL. Carspa is S$168-S$268 and Sonax Carspa is S$268-S$468."),
             ("How long is my car out of use?", "The Maintenance Car Spa takes 50 min to 1.5 h. Carspa takes 2-4 h and Sonax Carspa 4-8 h."),
             ("Is there a package for regular washes?", "Yes. The Maintenance Car Spa comes as a 10-session package: S$550 / S$650 / S$750 / S$850 by car size. It is made for ceramic-coated cars and uses Sonax maintenance coating."),
             ("Do I need to bring my car anywhere?", "No. This is a mobile service: we come to your HDB or condo car park.")],
 'interior-detailing': [("What does Deep Interior Detailing include?", "Pest fumigation, steaming, plastic shampoo, leather scrub, conditioning and coating, plastic coating, fabric and carpet extraction, roof top, boot and Sonax Air. It is S$388-S$688 by car size."),
             ("How much is fabric seat extraction?", "Fabric & Alcantara Seats Brush Extraction is S$188 for a 5-seater and S$288 for a 7-seater, 2-4 h."),
             ("Can you clean a coffee or food spill?", "Yes. Accident cleaning for a coffee or food spill is an add-on from S$120."),
             ("How long does interior detailing take?", "Sonax Premium Interior takes 3-6 h. Deep Interior Detailing & Coating takes 4-8 h.")],
 'car-fumigation-odour-removal': [("How much is car fumigation?", "Pest Fumigation & Interior Cleaning is S$108-S$268."),
             ("How long does it take?", "About 2-3 h of downtime."),
             ("What is included?", "Pest fumigation, vacuum, steaming, console, steering and door panel wipe-down, leather seats cleaning and Sonax Air."),
             ("Is there a deeper option?", "Deep Interior Detailing & Coating (S$388-S$688, 4-8 h) also includes pest fumigation, plus extraction and leather and plastic coating.")],
 'car-polishing-paint-correction': [("How much is paint correction?", "Single to multi-stage paint correction is S$200-S$2,000 and takes 4-15 h. It is free with Sonax CCEVO and Gtechniq ceramic coating."),
             ("What can paint correction remove?", "Swirl marks, light scratches, oxidation, water spots, bird-dropping and sap etching, and holograms."),
             ("How long does the spray ceramic last?", "The Detail Car Wash & Polishing & Seal & Sonax Spray Ceramic Coating package lasts about 4 months. It is S$248-S$508 by car size."),
             ("Where is it done?", "At your car park. We bring the polisher and products to you.")],
 'ceramic-coating': [("How long does Sonax CCOne last?", "Sonax CCOne Ceramic Coating lasts 15 months. It is S$428 / S$558 / S$708 / S$788 by car size and takes 5-9 h."),
             ("Which coating lasts the longest?", "Gtechniq Ceramic Coating is listed at 5 years (S$888-S$1,588) and 5-9 years (S$1,488-S$2,588)."),
             ("Is paint correction included?", "Sonax CCPro includes paint correction and perfect polish. Paint correction is free with Sonax CCEVO and Gtechniq coating."),
             ("Can you coat vinyl wraps or PPF?", "Yes. Sonax Vinyl & PPF Ceramic Coating is S$428-S$788, lasts 1-2 years and takes 4-8 h."),
             ("How long will my car be out of use?", "From 4-8 h for Ceramic Lite up to 9-16 h for Gtechniq 5-9 years.")],
 'glass-rim-coating': [("How much is glass water mark removal?", "Glass Water Mark Removal & Coating is S$188 / S$288 / S$388 / S$428 by car size, takes 2-5 h and lasts 6-12 months."),
             ("Do you coat rims?", "Yes. Gtechniq (UK) Rim Ceramic Coating is from S$200, takes 1.5-3 h and lasts 1 year."),
             ("Is there a windscreen-only option?", "Yes. Windscreen polish & sealant is from S$80.")],
 'engine-bay-cleaning': [("How much is engine bay cleaning?", "Engine Bay Restoration is S$88-S$128."),
             ("How long does it take?", "45 min to 2 h."),
             ("Can you add steaming?", "Yes. Steaming is an add-on, listed at 50+ (S$)."),
             ("Is it part of any coating package?", "Gtechniq Ceramic Coating (5-9 years) adds engine bay restoration and glass polish and coating.")],
}
SHORT = {'car-spa': 'Car Spa', 'interior-detailing': 'Interior Detailing', 'car-fumigation-odour-removal': 'Car Fumigation', 'car-polishing-paint-correction': 'Car Polishing',
         'ceramic-coating': 'Ceramic Coating', 'glass-rim-coating': 'Car Glass Coating', 'engine-bay-cleaning': 'Engine Bay Cleaning'}
def hub_title(s):
    t = '%s Singapore from %s, We Come to You' % (SHORT[s['slug']], money(svc_from(s)))
    return t if len(t) <= 60 else '%s Singapore from %s' % (SHORT[s['slug']], money(svc_from(s)))

# ---------- pages ----------
def home():
    path = ''
    title = 'Mobile Car Detailing Singapore: We Come to You | SgAutobots'
    desc = 'Mobile car detailing in Singapore with Sonax and Gtechniq products, real S/M/L/XL prices and downtime, done at your HDB or condo car park.'
    feat = [('car-spa', 'maint-once'), ('car-spa', 'carspa'), ('interior-detailing', 'premium-interior'), ('interior-detailing', 'deep-interior'), ('ceramic-coating', 'ccone'), ('ceramic-coating', 'ccevo')]
    cards = ''.join(pkg_card(next(p for p in SVB[s]['packages'] if p['id'] == pid), SVB[s], incl=False, link=True) for s, pid in feat)
    bays = ''.join('<a class="bay" href="%s">%s<div><h3>%s</h3><span class="from">from %s</span><span class="dt">Downtime %s to %s</span></div></a>'
                   % (u(s['slug'] + '/'), img(s['photos'][0], '104px'), e(s['name']), money(svc_from(s)), *dt_range(s)) for s in SV)
    steps = [("WhatsApp your car model and car park", "Tell us the car, the package and where it is parked. Not sure of the size? Send the model."),
             ("We arrive with the full mobile kit", "Foam, polisher, extractor, steamer and Sonax products come to your HDB or condo car park."),
             ("Downtime, as listed", "Every package shows how long your car is out of use, from 50 min up to 16 h for the longest coating."),
             ("Done, at your parking lot", "You get the car back where you left it.")]
    tl = ''.join('<li><span class="n">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, e(a), e(b)) for i, (a, b) in enumerate(steps))
    reels = ''.join(reel(v, 'tiktok_reel_%d' % (i + 1)) for i, v in enumerate(['loop-foam-wash', 'loop-machine-polish', 'loop-seat-extraction', 'loop-rim-coating']))
    glide = ''.join('<figure><div class="fr">%s<figcaption>%s</figcaption></div></figure>' % (img(g['id']), e(g['caption'])) for g in F['gallery'])
    qs = ''.join(quote(r) for r in F['reviews'])
    ld = [webpage_ld(path, title, desc), crumbs_ld([('Home', '')])]
    hero_img = GAL['g04']
    s = head(path, title, desc, ld) + header('') + (
        '<section class="hero"><picture><source type="image/webp" srcset="%s"><img src="%s" width="720" height="900" alt="%s" fetchpriority="high"></picture>'
        '<div class="wrap"><div class="tagrow"><span class="chip red">Mobile</span><span class="chip">Sonax and Gtechniq products</span></div>'
        '<h1>Mobile Car Detailing in Singapore. We Come to You.</h1>'
        '<svg class="stroke" viewBox="0 0 320 22" fill="none" aria-hidden="true"><path d="M4 15 C 60 4, 140 4, 196 10 S 290 18, 316 6" stroke="currentColor" stroke-width="9" stroke-linecap="round"/></svg>'
        '<p class="line">The whole workshop, at your HDB or condo car park.</p>%s</div></section>\n'
        % (u('images/gallery/%s.webp' % hero_img['file']), u('images/gallery/%s.jpg' % hero_img['file']), e(hero_img['alt']),
           cta_pair('whatsapp_home_hero', 'booking_home_hero', wa_text())) +
        '<section class="proof"><div class="wrap"><div><b>%s</b><small>%s</small></div><a href="%s" target="_blank" rel="noopener" data-cta="reviews" data-ref="reviews_home">See our 5-star reviews</a>'
        '<a href="%s" target="_blank" rel="noopener" data-cta="carousell" data-ref="carousell_reviews_home">More reviews on Carousell</a></div></section>\n'
        % (e(F['claims_text_unverified']), e(F['claims_note_unverified']), e(F['reviews_url']), e(F['socials']['carousell'])) +
        '<section class="sec" id="packages"><div class="wrap"><div class="level"><i>P1</i><span>Packages and prices (2026)</span></div><h2>Pick your car size. Every price updates.</h2>%s<div class="board three">%s</div>%s</div></section>\n'
        % (SWITCH, cards, cta_pair('whatsapp_home_packages', 'booking_home_packages', "Hi SgAutobots, I'd like a quote. Package: … Car model: ")) +
        '<hr class="lane">\n<section class="sec"><div class="wrap"><div class="level"><i>P2</i><span>Seven services, one van</span></div><h2>What we do at your car park</h2><div class="bays">%s</div></div></section>\n' % bays +
        '<section class="sec alt"><div class="wrap"><div class="level"><i>P3</i><span>How it works</span></div><h2>From WhatsApp to a clean car, in your own lot</h2><ol class="steps">%s</ol></div></section>\n' % tl +
        '<section class="sec"><div class="wrap"><div class="level"><i>P4</i><span>Real jobs, filmed by us</span></div><h2>Watch the kit at work</h2><div class="reels">%s</div>'
        '<p class="lead">Tap a clip to watch the full video on our TikTok.</p></div></section>\n' % reels +
        '<section class="sec alt"><div class="wrap"><div class="level"><i>P5</i><span>Every plate under a Sonax card</span></div><h2>Detailed on site, photographed on site</h2></div>'
        '<div class="wrap"><div class="glide" data-speed="0.035">%s</div><p class="glide-hint">%s Drag to look closer. It carries on gliding after you let go.</p></div></section>\n' % (glide, I_SWIPE) +
        '<section class="sec"><div class="wrap"><div class="level"><i>P6</i><span>What Carousell buyers wrote</span></div><h2>"Will not hardsell on packages."</h2><div class="quotes">%s</div>'
        '<p><a href="%s" target="_blank" rel="noopener" data-cta="carousell" data-ref="carousell_reviews">More reviews on Carousell</a> &nbsp; <a href="%s" target="_blank" rel="noopener" data-cta="reviews" data-ref="reviews_home_quotes">See our 5-star reviews on Google</a></p></div></section>\n'
        % (qs, e(F['socials']['carousell']), e(F['reviews_url'])) +
        '<section class="sec alt" id="areas"><div class="wrap"><div class="level"><i>P7</i><span>Based in Yishun</span></div><h2>We come to these 13 towns first</h2>'
        '<p class="lead">%s Distances are straight-line from our Yishun base.</p>%s<p>%s</p>%s</div></section>\n'
        % (e(F['service_line']), area_strip(), REST, a_wa('whatsapp_home_areas', "Hi SgAutobots, can you come to my car park? Area: … Car model: ", 'WhatsApp your area')) +
        footer() + bar())
    write(path, s)

def hub(i, s):
    path = s['slug'] + '/'
    title = hub_title(s)
    desc = INTRO[s['slug']].split('. ')[0] + '. Mobile service at your car park.'
    nxt = SV[(i + 1) % len(SV)]
    faqs = FAQS[s['slug']]
    vid = VID[s['video']]
    ld = [webpage_ld(path, title, desc), service_ld(s, path), faq_ld(faqs), crumbs_ld([('Home', ''), (s['name'], path)])]
    qs = ''.join(quote(r) for r in quotes_for(s['slug'], 2))
    sv = s['slug'].replace('-', '_')
    body = (crumbs([('Home', ''), (s['name'], path)]) +
        '<section class="phead wrap"><h1>%s</h1><p class="lead">%s</p>%s</section>\n' % (e(s['h1']), e(INTRO[s['slug']]), cta_pair('whatsapp_%s_intro' % sv, 'booking_%s_intro' % sv, wa_text(svc=s), s)) +
        '<section class="sec" style="padding-top:28px"><div class="wrap"><div class="level"><i>P1</i><span>Packages and prices (2026)</span></div><h2>%s prices by car size</h2>%s</div></section>\n'
        % (e(s['name']), price_board(s, three=len(s['packages']) > 2)) +
        '<section class="sec alt"><div class="wrap split"><div><div class="level"><i>P2</i><span>On site, real jobs</span></div><h2>What it looks like at your car park</h2>%s</div>'
        '<div class="vid-one">%s</div></div></section>\n' % (photos(s['photos'][:4]), reel(s['video'], 'tiktok_%s' % sv)) +
        '<section class="sec"><div class="wrap">%s<div class="qgrid" style="margin-top:22px">%s</div></div></section>\n'
        % (cta_pair('whatsapp_%s_mid' % sv, 'booking_%s_mid' % sv, wa_text(svc=s), s), qs) +
        '<section class="sec alt"><div class="wrap"><div class="level"><i>P3</i><span>Questions</span></div><h2>%s: common questions</h2>%s</div></section>\n' % (e(s['name']), faq_html(faqs)) +
        '<section class="sec"><div class="wrap"><div class="level"><i>P4</i><span>Areas</span></div><h2>%s near you</h2><p class="lead">We come to these towns within about 10 km of our Yishun base.</p>%s<p>%s</p>'
        '<a class="next" href="%s"><span>Next service</span><b>%s</b></a></div></section>\n'
        % (e(s['name']), area_strip(s['slug']), REST, u(nxt['slug'] + '/'), e(nxt['name'])) +
        '<section class="sec"><div class="wrap"><div class="endcta"><h2>Get a %s quote on WhatsApp</h2><p class="lead">Send your car model and car park. We reply with the price for your size.</p>%s'
        '<p class="updated">Updated: %s. <a href="%s">Back to home</a></p></div></div></section>\n'
        % (e(s['name'].lower()), cta_pair('whatsapp_%s_end' % sv, 'booking_%s_end' % sv, wa_text(svc=s), s), UPDATED, u('')))
    write(path, head(path, title, desc, ld) + header(path, s) + body + footer(s) + bar(s))

def area_page(s, a):
    """Shared area template: one service x one town. Local facts come from areas.json only."""
    path = '%s/%s/' % (s['slug'], a['slug'])
    kw = '%s %s' % (SHORT[s['slug']], a['name'])
    title = '%s from %s, at Your Car Park' % (kw, money(svc_from(s)))
    if len(title) > 60: title = '%s from %s, We Come to You' % (kw, money(svc_from(s)))
    if len(title) > 60: title = '%s from %s' % (kw, money(svc_from(s)))
    lo, hi = dt_range(s)
    desc = '%s in %s from %s, downtime %s to %s, done at your car park about %s km from our Yishun base.' % (s['name'], a['name'], money(svc_from(s)), lo, hi, a['km'])
    nb = [AB[x] for x in a['neighbours'] if x in AB]
    others = [x for x in SV if x['slug'] != s['slug']][:3]
    faqs = [("Do you come to %s?" % a['name'], "Yes. %s %s is about %s km from our Yishun base. WhatsApp us your car park." % (e(F['service_line'].split(',')[0]) + '.', e(a['name']), a['km'])),
            ("How long is my car out of use?", "For %s, downtime is %s to %s depending on the package; each package above shows its own time." % (e(s['name'].lower()), lo, hi))]
    ld = [webpage_ld(path, title, desc), service_ld(s, path, a), faq_ld(faqs), crumbs_ld([('Home', ''), (s['name'], s['slug'] + '/'), (a['name'], path)])]
    sv = s['slug'].replace('-', '_'); ar = a['slug'].replace('-', '_')
    inc = ' (incl. %s)' % ', '.join(a['includes']) if a['includes'] else ''
    pk = s['packages']
    g = s['photos'][AREAS.index(a) % len(s['photos'])]
    rv = quotes_for(s['slug'], 2)[AREAS.index(a) % len(quotes_for(s['slug'], 2))]
    body = (crumbs([('Home', ''), (s['name'], s['slug'] + '/'), (a['name'], path)]) +
        '<section class="phead wrap"><h1>%s in %s, at Your Car Park</h1><p class="lead">%s from %s in %s%s, with downtime from %s. We come to you, about %s km from our Yishun base.</p>%s</section>\n'
        % (e(SHORT[s['slug']]), e(a['name']), e(s['name']), money(svc_from(s)), e(a['name']), e(inc), lo, a['km'],
           '<div class="cta-pair">%s%s</div>' % (a_wa('whatsapp_area_%s' % ar, wa_text(svc=s, area=a), 'WhatsApp us'), a_book('booking_area_%s' % ar, s))) +
        '<section class="sec" style="padding-top:24px"><div class="wrap split"><div class="local"><p class="km">%s<small>km from our Yishun base</small></p><h2 style="font-size:2rem">Car parks in %s</h2><p>%s</p><p>%s</p>'
        '<ul>%s</ul></div><div class="photos" style="grid-template-columns:1fr;max-width:340px"><figure>%s<figcaption>%s</figcaption></figure></div></div></section>\n'
        % (a['km'], e(a['name']), e(a['parking']), e(a['line']), ''.join('<li>Near %s</li>' % e(r) for r in a['roads']), img(g, '340px'), e(GAL[g]['caption'])) +
        '<section class="sec alt"><div class="wrap"><div class="level"><i>P1</i><span>Packages and prices (2026)</span></div><h2>%s prices in %s</h2>%s</div></section>\n'
        % (e(s['name']), e(a['name']), price_board(s, three=len(pk) > 2, table=False)) +
        '<section class="sec"><div class="wrap split"><div>%s<div class="faq">%s</div></div><div>%s</div></div></section>\n'
        % (cta_pair('whatsapp_area_%s_mid' % ar, 'booking_%s_%s_mid' % (sv, ar), wa_text(svc=s, area=a), s), ''.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q), x) for q, x in faqs), quote(rv)) +
        '<section class="sec alt"><div class="wrap"><h2>Nearby</h2><div class="areas">%s</div><h2 style="margin-top:22px">More services in %s</h2><div class="areas">%s</div>'
        '<p><a href="%s">All %s prices and details</a> &nbsp; <a href="%s">Home</a></p></div></section>\n'
        % (''.join('<a href="%s">%s in %s <small>%s km</small></a>' % (u(s['slug'] + '/' + n['slug'] + '/'), e(SHORT[s['slug']]), e(n['name']), n['km']) for n in nb), e(a['name']),
           ''.join('<a href="%s">%s</a>' % (u(o['slug'] + '/' + a['slug'] + '/'), e(SHORT[o['slug']])) for o in others), u(s['slug'] + '/'), e(s['name'].lower()), u('')) +
        '<section class="sec"><div class="wrap"><div class="endcta"><h2>%s in %s? WhatsApp us</h2>%s<p class="updated">Updated: %s.</p></div></div></section>\n'
        % (e(SHORT[s['slug']]), e(a['name']), cta_pair('whatsapp_area_%s_end' % ar, 'booking_%s_end' % sv, wa_text(svc=s, area=a), s), UPDATED))
    write(path, head(path, title, desc, ld) + header(s['slug'] + '/', s) + body + footer(s) + bar(s, a))

def contact():
    path = 'contact/'; title = 'Contact SgAutobots: WhatsApp +65 8366 7010'
    desc = 'WhatsApp or call SgAutobots on +65 8366 7010 to book mobile car detailing at your car park anywhere in Singapore.'
    soc = ''.join('<a href="%s" target="_blank" rel="noopener" data-cta="%s" data-ref="%s_contact">%s</a>' % (e(F['socials'][k]), k, k, SOC_LABEL[k]) for k in ['facebook', 'instagram', 'tiktok', 'carousell'])
    ld = [webpage_ld(path, title, desc), crumbs_ld([('Home', ''), ('Contact', path)])]
    body = (crumbs([('Home', ''), ('Contact', path)]) +
        '<section class="phead wrap"><h1>WhatsApp, call or book</h1><p class="lead">%s</p><p class="lead">%s</p>%s<p>%s</p></section>\n'
        % (e(F['service_line']), e(F['hours_text']), cta_pair('whatsapp_contact', 'booking_contact', wa_text()), a_call('call_contact')) +
        '<section class="sec"><div class="wrap split"><div class="local"><h2 style="font-size:2rem">Find us online</h2><div class="areas">%s</div>'
        '<p><a href="%s" target="_blank" rel="noopener" data-cta="reviews" data-ref="reviews_contact">See our 5-star reviews</a></p>'
        '<p><a href="%s" data-cta="reviews" data-ref="review_helper_contact">Leave us a Google review</a></p></div>'
        '<div><h2 style="font-size:2rem">Where we go</h2><p class="lead">These 13 towns are within about 10 km of our Yishun base. %s</p>%s</div></div></section>\n'
        % (soc, e(F['reviews_url']), u('review/'), REST, area_strip()))
    write(path, head(path, title, desc, ld) + header(path) + body + footer() + bar())

def privacy():
    path = 'privacy/'; title = 'Website Privacy Notice | SgAutobots'
    desc = 'How SgAutobots handles the details you send by WhatsApp or phone when you ask about mobile car detailing.'
    facts = {"name": F['name'], "wa_link": wa_href(wa_text()), "wa_display": F['phone_display'], "tel_link": "tel:" + F['tel'], "tel_display": F['phone_display'],
             "updated": UPDATED, "extras": ["tiktok", "facebook"]}
    main = PV.render_main('en', 'sg', facts)
    main = main.replace('data-cta="whatsapp_privacy" data-ref="privacy"', 'data-cta="whatsapp" data-ref="whatsapp_privacy"').replace('data-cta="call_privacy" data-ref="privacy"', 'data-cta="call" data-ref="call_privacy"')
    ld = [webpage_ld(path, title, desc), crumbs_ld([('Home', ''), ('Privacy', path)])]
    body = crumbs([('Home', ''), ('Privacy', path)]) + '<section class="sec" style="padding-top:20px"><div class="wrap prose">%s</div></section>\n' % main
    write(path, head(path, title, desc, ld) + header(path) + body + footer() + bar())

def review():
    path = 'review/'; title = 'Leave SgAutobots a Google Review'
    desc = 'Thank you for choosing SgAutobots. Tap once to leave a Google review.'
    ld = [webpage_ld(path, title, desc)]
    body = ('<section class="phead wrap" style="padding:48px 0"><h1>Thank you for choosing SgAutobots</h1><p class="lead">If you liked the job, a short Google review helps other car owners find us.</p>'
            '<p><a class="btn btn-book" href="%s" target="_blank" rel="noopener" data-cta="reviews" data-ref="review_helper_write">%s<span>Write a Google review</span></a></p>'
            '<p><a href="%s" target="_blank" rel="noopener" data-cta="reviews" data-ref="review_helper_read">See our 5-star reviews</a></p></section>\n' % (e(F['write_review_url']), I_CAL, e(F['reviews_url'])))
    s = head(path, title, desc, ld) + header(path) + body + footer() + bar()
    write(path, s); PAGES.remove((path, title))  # helper stays out of sitemap

def extras():
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(golive.sitemap_xml(CFG, [p for p, _ in PAGES], LASTMOD))
    open(os.path.join(OUT, 'robots.txt'), 'w').write(golive.robots_txt(CFG))
    L = [golive.llms_header(CFG, F['name'], F['service_line'] + ' Sonax (Germany) and Gtechniq (UK) products. WhatsApp +65 8366 7010.'), '', '## Services']
    for s in SV: L.append('- [%s](%s/%s/): from %s; %s' % (s['name'], BASE, s['slug'], money(svc_from(s)), s['kw']))
    L += ['', '## Areas (within about 10 km of the Yishun base)'] + ['- %s: about %s km; e.g. %s/car-spa/%s/' % (a['name'], a['km'], BASE, a['slug']) for a in AREAS]
    L += ['', '## Contact', '- WhatsApp: https://wa.me/6583667010', '- Phone: +65 8366 7010', '- Google reviews: ' + F['reviews_url'], '- [Contact](%s/contact/)' % BASE, '- [Privacy](%s/privacy/)' % BASE, '']
    open(os.path.join(OUT, 'llms.txt'), 'w').write('\n'.join(L))
    json.dump({"booking_url": F['booking_url'], "videos_live": FL['videos_live'], "_note": "booking_url: the shared booking portal URL. Empty = Book opens WhatsApp. videos_live: true once the mp4s are in video/."},
              open(os.path.join(OUT, 'site-config.json'), 'w'), indent=1)
    import shutil
    for f in ['site.css', 'site.js', 'p1-cta.js']: shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
    os.makedirs(os.path.join(OUT, 'fonts'), exist_ok=True)
    for f in ['bsd-800.woff2', 'ah-400.woff2', 'ah-700.woff2']: shutil.copy(os.path.join(HERE, f), os.path.join(OUT, 'fonts', f))
    os.makedirs(os.path.join(OUT, 'video'), exist_ok=True)
    open(os.path.join(OUT, 'video', 'README.txt'), 'w').write('Video slot: put loop-foam-wash.mp4, loop-machine-polish.mp4, loop-seat-extraction.mp4, loop-rim-coating.mp4, full-odour-removal.mp4, full-interior-cleaning.mp4 here, then set videos_live true in ../site-config.json.\n')

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    home()
    for i, s in enumerate(SV): hub(i, s)
    for s in SV:
        for a in AREAS: area_page(s, a)
    contact(); privacy(); review(); extras()
    print('pages', len(PAGES) + 1, 'out', OUT)

#!/usr/bin/env python3
"""MOON wiper blades SG preview (Page One, Edwin 17 Nov 2026).
Template-first: one head/header/footer/dock here, one CSS (static/site.css), one facts file (data.json).
Build: python3 build.py  -> site/  (photos are already live in preview/moon-wiper/img/ from the Bridge drop).
WhatsApp: set "whatsapp" in data.json and rebuild; every WhatsApp slot (header, hero, dock, footer) appears at once."""
import json, os, shutil, hashlib, html, urllib.parse
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf8'))
OUT = os.path.join(HERE, 'site')
BASE, P, S, PR = D['base'], D['path'], D['seller'], D['products']
TODAY = date.today().isoformat()
e = html.escape

def vhash(rel):
    return hashlib.sha256(open(os.path.join(HERE, 'static', rel), 'rb').read()).hexdigest()[:8]

ICON = {
 'call': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
 'wa': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21l1.7-4.6A9 9 0 1 1 8 19.6z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1.2-1.2 2 .9c-.3 1.4-1.5 2.1-2.9 1.8A8 8 0 0 1 8 9.7c-.3-1.4.4-2.6 1.8-2.9l.9 2z"/></svg>',
 'menu': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 7h18M3 12h18M3 17h18"/></svg>',
 'go': '<svg class="go" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M9 5l7 7-7 7"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14"/><path d="M3 6l9 7 9-7"/></svg>',
}

WORDMARK = '''<svg viewBox="0 0 132 30" role="img" aria-label="MOON"><defs><linearGradient id="mg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D7DCE0"/><stop offset=".48" stop-color="#9AA2A9"/><stop offset=".52" stop-color="#7E878F"/><stop offset="1" stop-color="#C3C9CE"/></linearGradient></defs>
<g fill="url(#mg)" stroke="#5B646C" stroke-width=".8"><path d="M1 29V1h7l7 16 7-16h7v28h-6V12l-6 14h-4L7 12v17z"/><path d="M34 15C34 6 39 1 47 1s13 5 13 14-5 14-13 14-13-5-13-14zm6 0c0 5.6 2.6 8.6 7 8.6s7-3 7-8.6-2.6-8.6-7-8.6-7 3-7 8.6z"/><path d="M64 15C64 6 69 1 77 1s13 5 13 14-5 14-13 14-13-5-13-14zm6 0c0 5.6 2.6 8.6 7 8.6s7-3 7-8.6-2.6-8.6-7-8.6-7 3-7 8.6z"/><path d="M95 29V1h6l12 17V1h6v28h-6L101 12v17z"/></g><path d="M121 29l10-10v10z" fill="#C8102E"/></svg>'''

NAV = [('', 'Home', ''), ('hybrid-wiper-blades/', 'Silicone Hybrid', 'Japanese cars'),
       ('conventional-wiper-blades/', 'Silicone Advance', 'Continental cars'),
       ('silicone-flat-wiper-blades/', 'Beam / flat', 'M-102, M-105'), ('rear-wiper-blades/', 'Rear blades', 'M-GRA, M-GRB, M-FR'),
       ('wiper-size-guide/', 'Size guide', ''), ('where-to-buy/', 'Where to buy', 'Kohden, Kaki Bukit'),
       ('faq/', 'FAQ', ''), ('articles/', 'Articles', '')]
DNAV = [('hybrid-wiper-blades/', 'Hybrid'), ('conventional-wiper-blades/', 'Advance'), ('silicone-flat-wiper-blades/', 'Flat'),
        ('rear-wiper-blades/', 'Rear'), ('wiper-size-guide/', 'Sizes'), ('where-to-buy/', 'Where to buy')]

def wa_url():
    n = ''.join(c for c in D['whatsapp'] if c.isdigit())
    return f'https://wa.me/{n}?text={urllib.parse.quote(D["whatsapp_text"])}' if n else ''

def call(ref, label=None, cls='btn'):
    label = label or f'Call Kohden {S["phone_short"]}'
    return f'<a class="{cls}" href="tel:{S["tel"]}" data-ref="{ref}-call">{ICON["call"]}<span>{e(label)}</span></a>'

def wa(ref, label='WhatsApp Kohden', cls='btn wa'):
    """WhatsApp slot: renders nothing until data.json has a number (Edwin 17 Nov: no live WA button yet)."""
    u = wa_url()
    return f'<a class="{cls}" href="{e(u)}" target="_blank" rel="noopener" data-ref="{ref}-whatsapp">{ICON["wa"]}<span>{e(label)}</span></a>' if u else ''

def directions(ref, cls='btn ghost'):
    return f'<a class="{cls}" href="{e(S["maps"])}" target="_blank" rel="noopener" data-cta="directions" data-ref="{ref}-directions">{ICON["pin"]}<span>Directions to Kohden</span></a>'

def email(ref):
    return f'<a href="mailto:{S["email"]}" data-ref="{ref}-email">{S["email"]}</a>'

def pic(key, eager=False, cap=True, extra=''):
    name, alt = D['images'][key]
    src = f'{P}img/{name}'
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f'<figcaption>{e(alt)}.</figcaption>' if cap else ''
    return (f'<figure class="ph-wrap"><div class="ph">{extra}<picture><source type="image/webp" srcset="{src}.webp">'
            f'<img src="{src}.jpg" width="1200" height="1600" alt="{e(alt)}" {load}></picture></div>{c}</figure>')

SWEEP = ('<svg class="sweep" viewBox="0 0 400 500" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="sv" x1="0" x2="1">'
         '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#E9ECEF"/><stop offset="1" stop-color="#A9B0B6"/></linearGradient></defs>'
         '<path d="M-20 470 Q 200 40 430 300"/></svg>')

def sizes(lst):
    return '<ul class="sizes">' + ''.join(f'<li>{e(x)}</li>' for x in lst) + '</ul>'

def org_seller():
    return {"@type": "AutoPartsStore", "@id": BASE + "where-to-buy/#kohden", "name": S['name'], "telephone": S['phone_display'], "email": S['email'],
            "address": {"@type": "PostalAddress", "streetAddress": S['street'], "postalCode": S['postcode'], "addressLocality": "Singapore", "addressCountry": "SG"},
            "openingHours": S['hours_schema'], "url": S['web']}

def product_ld(key, desc, img):
    p = PR[key]
    d = {"@type": "Product", "name": p['name'], "brand": {"@type": "Brand", "name": "MOON"},
         "manufacturer": {"@type": "Organization", "name": "Fu-Gang", "address": {"@type": "PostalAddress", "addressCountry": "TW"}},
         "description": desc, "image": f'{BASE}img/{img}.jpg' if img else f'{BASE}og.jpg'}
    if p.get('low'):
        o = {"@type": "AggregateOffer", "priceCurrency": "SGD", "lowPrice": str(p['low']), "highPrice": str(p['high']), "seller": {"@id": BASE + "where-to-buy/#kohden"}}
        if p['low'] == p['high']:
            o = {"@type": "Offer", "priceCurrency": "SGD", "price": str(p['low']), "seller": {"@id": BASE + "where-to-buy/#kohden"}}
        d["offers"] = o
    return d

def crumbs_ld(slug, name):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
    if slug: items.append({"@type": "ListItem", "position": 2, "name": name, "item": BASE + slug})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def crumb(name):
    return f'<p class="crumb"><a href="{P}">Home</a> / {e(name)}</p>'

def page(slug, title, desc, h1name, body, ld=None):
    url = BASE + slug
    graph = [crumbs_ld(slug, h1name), {"@type": "WebSite", "@id": BASE + "#site", "name": D['site_name'], "url": BASE, "inLanguage": "en-SG"}] + (ld or [])
    nav_m = ''.join(f'<li><a href="{P}{u}"{" aria-current=\"page\"" if u == slug else ""}>{e(n)}{f"<small>{e(s)}</small>" if s else ""}</a></li>' for u, n, s in NAV)
    nav_d = ''.join(f'<li><a href="{P}{u}"{" aria-current=\"page\"" if u == slug else ""}>{e(n)}</a></li>' for u, n in DNAV)
    css, cta = vhash('site.css'), vhash('p1-cta.js')
    head = f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(D['site_name'])}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og.jpg"><meta property="og:image:secure_url" content="{BASE}og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="MOON silicone wiper blades, sold in Singapore by Kohden"><meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}og.jpg">
<meta name="theme-color" content="#FFFFFF"><link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{P}fonts/archivo-narrow-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}site.css?v={css}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head><body>
<header class="hd"><div class="wrap"><a class="mark" href="{P}" aria-label="MOON wiper blades Singapore, home">{WORDMARK}<span>Wiper blades Singapore</span></a>
<ul class="dnav">{nav_d}</ul>{wa('header', 'WhatsApp', 'hd-wa')}<a class="hd-call" href="tel:{S['tel']}" data-ref="header-call">{ICON['call']}<span>Call</span></a>
<details class="nav"><summary aria-label="Menu">{ICON['menu']}</summary><ul>{nav_m}</ul></details></div></header>
<main>'''
    foot = f'''</main>
<footer class="ft"><div class="wrap">
<div><a class="mark" href="{P}" aria-label="MOON home">{WORDMARK}</a><p style="margin-top:14px">MOON silicone wiper blades, made in Taiwan by Fu-Gang. Sold in Singapore by {e(S['name'])}.</p>
<div class="btns">{call('footer')}{wa('footer')}</div></div>
<div><h2>Kohden</h2><p>{e(S['street'])}<br>Singapore {S['postcode']}<br>{e(S['hours_display'])}</p>
<ul><li><a href="tel:{S['tel']}" data-ref="footer-call-text">{S['phone_display']}</a></li><li>{email('footer')}</li><li><a href="{e(S['maps'])}" target="_blank" rel="noopener" data-cta="directions" data-ref="footer-directions">Directions on Google Maps</a></li></ul></div>
<div><h2>Blades</h2><ul>{''.join(f'<li><a href="{P}{u}">{e(n)}</a></li>' for u, n, s in NAV[1:])}</ul></div>
<p class="legal">MOON wiper blades are made in Taiwan by Fu-Gang (ISO 9001:2015, IATF 16949:2016). Prices are Kohden's published Singapore prices and can change; call to confirm.</p>
</div></footer>
<nav class="dock" data-ref="sticky-dock" aria-label="Contact Kohden">{call('dock', f'Call Kohden {S["phone_short"]}')}{wa('dock', 'WhatsApp')}</nav>
<script src="{P}p1-cta.js?v={cta}" defer></script>
</body></html>
'''
    path = os.path.join(OUT, slug, 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf8').write(head + body + foot)
    return url

def shop_block(ref):
    return f'''<div class="shop"><h2>Buy MOON from Kohden</h2><p>{e(S['name'])} is the Singapore seller. Call with your car's make, model and year and they will match the blade.</p>
<dl><dt>Address</dt><dd>{e(S['street'])}, Singapore {S['postcode']}</dd><dt>Phone</dt><dd><a href="tel:{S['tel']}" data-ref="{ref}-call-text">{S['phone_display']}</a></dd><dt>Email</dt><dd>{email(ref)}</dd><dt>Hours</dt><dd>{e(S['hours_display'])}</dd></dl>
<div class="btns">{call(ref)}{wa(ref)}{directions(ref)}</div></div>'''

def adapter_svg(code):
    """Simplified line drawings redrawn from the MOON leaflet chart (no handwriting)."""
    g = '<svg viewBox="0 0 160 80" aria-hidden="true" fill="none" stroke="#1B1F23" stroke-width="2.4" stroke-linejoin="round">'
    base = '<path d="M16 58h128" stroke="#A9B0B6" stroke-width="6"/>'
    shapes = {
     'D02': '<rect x="44" y="30" width="72" height="22"/><rect x="68" y="18" width="24" height="12" fill="#C8102E" stroke="#C8102E"/>',
     'i02': '<rect x="48" y="28" width="64" height="24"/><path d="M48 34h-10v12h10M112 34h10v12h-10" stroke="#C8102E"/>',
     'B02': '<rect x="40" y="28" width="80" height="24"/><circle cx="80" cy="40" r="7" stroke="#C8102E"/><path d="M80 40H24" stroke="#C8102E"/>',
     'L02': '<rect x="36" y="40" width="88" height="12"/><path d="M56 40v-8h48v8"/>',
     'G02': '<rect x="44" y="30" width="72" height="22"/><path d="M116 36h18v10h-10" stroke="#C8102E"/>',
     'A02': '<path d="M40 52V34a12 12 0 0 1 12-12h70" /><path d="M122 22v14H58" stroke="#C8102E"/><rect x="58" y="36" width="54" height="16"/>',
     'J02': '<rect x="44" y="30" width="72" height="22"/><path d="M70 30v-10h20v10" stroke="#C8102E"/><text x="80" y="47" font-size="14" text-anchor="middle" fill="#1B1F23" stroke="none" font-family="sans-serif" font-weight="700">C</text>',
     'K02': '<rect x="44" y="30" width="72" height="22"/><path d="M70 30v-10h20v10" stroke="#C8102E"/><text x="80" y="47" font-size="14" text-anchor="middle" fill="#1B1F23" stroke="none" font-family="sans-serif" font-weight="700">M</text>',
    }
    return g + base + shapes[code] + '</svg>'

def chart():
    li = ''.join(f'<li>{adapter_svg(c)}<b>{c}</b><span>{e(t)}{(" " + e(n)) if n else ""}</span></li>' for c, t, n in D['adapters'])
    return f'''<figure class="chart" role="group" aria-label="MOON Silicone Advance adapter chart"><ol>{li}</ol>
<figcaption>Silicone Advance adapter chart, redrawn from the MOON leaflet. Drawings are simplified. The adapters come with Silicone Advance only.</figcaption></figure>'''

def build():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ['site.css', 'p1-cta.js', 'favicon.svg']:
        shutil.copy(os.path.join(HERE, 'static', f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(HERE, 'static', 'fonts'), os.path.join(OUT, 'fonts'))
    if os.path.exists(os.path.join(HERE, 'static', 'og.jpg')): shutil.copy(os.path.join(HERE, 'static', 'og.jpg'), os.path.join(OUT, 'og.jpg'))
    h, fl, adv, rr = PR['m1001'], PR['m102'], PR['advance'], PR
    urls = []
    seller = org_seller()

    # HOME
    body = f'''<section class="hero"><div class="wrap">{pic('hybrid_boxes', eager=True, cap=False, extra=SWEEP)}
<div><h1>Moon hybrid wiper blades for Singapore</h1><p class="line">Taiwan-made silicone hybrid for Japanese cars, then Silicone Advance for Continental.</p>
<div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap"><h2>Pick your blade</h2>
<ul class="range">
<li><a href="{P}hybrid-wiper-blades/"><b>Silicone Hybrid M1001</b><span class="pr">{h['price']}</span><span class="d">For Japanese cars. Start here.</span></a></li>
<li><a href="{P}conventional-wiper-blades/"><b>Silicone Advance</b><span class="pr">Call for price</span><span class="d">The higher-end line for Continental cars, adapter included.</span></a></li>
<li><a href="{P}silicone-flat-wiper-blades/"><b>Beam / flat M-102, M-105</b><span class="pr">{fl['price']}</span><span class="d">Silicone flat blades.</span></a></li>
<li><a href="{P}rear-wiper-blades/"><b>Rear M-GRA, M-GRB, M-FR</b><span class="pr">$20 to $22</span><span class="d">Rear window blades.</span></a></li>
</ul><p class="small" style="margin-top:12px">Prices are Kohden's published Singapore prices.</p></div></section>
<section class="sec white"><div class="wrap split">{pic('pack_back')}
<div><p class="claim">2X longer lasting</p><p class="lead">That is the maker's lab-test claim: the MOON silicone blade lasted twice as long as traditional natural rubber in laboratory testing.</p>
<p>Made in Taiwan by Fu-Gang, certified ISO 9001:2015 and IATF 16949:2016.</p></div></div></section>
<section class="sec"><div class="wrap split rev">{pic('advance')}
<div><h2>Not sure of your size?</h2><p class="lead">Read the size on your old blade's box, or measure it tip to tip. Or call Kohden with your make, model and year.</p>
<div class="btns"><a class="btn ghost" href="{P}wiper-size-guide/">Open the size guide</a></div></div></div></section>
<section class="sec"><div class="wrap">{shop_block('home')}</div></section>'''
    urls.append(page('', 'MOON Hybrid Wiper Blades Singapore | Silicone, Taiwan-made',
        'MOON silicone hybrid wiper blades for Japanese cars and Silicone Advance for Continental cars. Kohden prices $20 to $80. Call +65 6966 6565.',
        'Home', body, [seller, {"@type": "Brand", "name": "MOON"}]))

    # HYBRID
    hdesc = 'MOON Silicone Hybrid M1001 wiper blade for Japanese cars: streamlined shape against wind-lift, less chatter, multi-curvature rail spline. Made in Taiwan by Fu-Gang.'
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Silicone Hybrid M1001')}<h1>MOON Silicone Hybrid wiper blades</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">M1001 for Japanese cars. {h['price']} at Kohden.</p><div class="btns">{call('hero')}{wa('hero')}</div></div>
{pic('hybrid_close', eager=True)}</div></section>
<section class="sec"><div class="wrap prose"><h2>What it is</h2>
<table class="spec"><tr><th>Model</th><td>M1001 Silicone Hybrid</td></tr><tr><th>Best for</th><td>Japanese cars</td></tr><tr><th>Fit</th><td>Exact-fit. Kohden matches the blade to your make, model and year.</td></tr>
<tr><th>Price</th><td class="num">{h['price']} (Kohden, by size)</td></tr><tr><th>Made by</th><td>Fu-Gang, Taiwan</td></tr></table>
<ul><li>Streamlined shape that cuts wind-lift.</li><li>Less chatter across the glass.</li><li>Multi-curvature rail spline to follow the windscreen.</li><li>Recyclable material.</li></ul>
<h2 style="margin-top:32px">Sizes at Kohden</h2>{sizes(h['sizes'])}
<p class="small" style="margin-top:12px">Most cars use two different front sizes. <a href="{P}wiper-size-guide/">How to find yours</a>.</p></div></section>
<section class="sec white"><div class="wrap split">{pic('leaflet')}
<div><h2>First use</h2><p class="lead">The MOON leaflet asks you to clean the glass first, then let the new blades wipe the dry glass for 5 minutes or more.</p>
<p>MOON calls it a super water-repellent silicone wiper.</p></div></div></section>
<section class="sec"><div class="wrap">{shop_block('hybrid')}</div></section>'''
    urls.append(page('hybrid-wiper-blades/', 'MOON Silicone Hybrid Wiper Blades M1001 Singapore | $30 to $80',
        'MOON Silicone Hybrid M1001 wiper blades for Japanese cars, 12 to 28 inch, $30 to $80 at Kohden Singapore. Call +65 6966 6565 to match your car.',
        'Silicone Hybrid M1001', body, [seller, product_ld('m1001', hdesc, D['images']['hybrid_close'][0])]))

    # CONVENTIONAL / SILICONE ADVANCE
    adesc = 'MOON Silicone Advance, the higher-end line for Continental cars, with water repellency and Siflon rubber technology. Adapter included.'
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Silicone Advance')}<h1>MOON Silicone Advance wiper blades</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">The higher-end line for Continental cars. Adapter included.</p><div class="btns">{call('hero', 'Call Kohden for price')}{wa('hero')}</div></div>
{pic('advance', eager=True)}</div></section>
<section class="sec"><div class="wrap"><h2>Which adapter fits your arm</h2><p class="lead">Silicone Advance comes with the adapter set below. Kohden will tell you which one your wiper arm takes.</p>{chart()}</div></section>
<section class="sec white"><div class="wrap split">{pic('pack_back')}
<div><p class="claim">2X longer lasting</p><p class="lead">The maker's lab-test claim, printed on the pack: the MOON silicone blade lasted twice as long as traditional natural rubber in laboratory testing.</p>
<table class="spec"><tr><th>Line</th><td>Silicone Advance</td></tr><tr><th>Best for</th><td>Continental cars</td></tr><tr><th>On the pack</th><td>Water repellency, Siflon rubber technology</td></tr><tr><th>Packs shown</th><td class="num">26" and 16"</td></tr><tr><th>Price</th><td>Call Kohden</td></tr></table></div></div></section>
<section class="sec"><div class="wrap">{shop_block('advance')}</div></section>'''
    urls.append(page('conventional-wiper-blades/', 'MOON Silicone Advance Wiper Blades Singapore | For Continental Cars',
        'MOON Silicone Advance wiper blades for Continental cars, with the adapter set included. Water repellent silicone. Call Kohden +65 6966 6565 for price and fit.',
        'Silicone Advance', body, [seller, product_ld('advance', adesc, D['images']['advance'][0])]))

    # FLAT
    m105 = PR['m105']
    fdesc = 'MOON silicone beam / flat wiper blades M-102 and M-105 Japan Flat, sold in Singapore by Kohden.'
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Beam / flat blades')}<h1>MOON silicone flat wiper blades</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">Beam blades with no frame. M-102 and M-105 Japan Flat.</p><div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap prose"><h2>M-102 Silicone Flat</h2>
<table class="spec"><tr><th>Type</th><td>Beam / flat</td></tr><tr><th>Price</th><td class="num">{fl['price']} (Kohden, by size)</td></tr></table>
<ul><li>Long-lasting silicone.</li><li>Less noise and chatter.</li><li>Strong corrosion resistance.</li></ul>{sizes(fl['sizes'])}</div></section>
<section class="sec white"><div class="wrap prose"><h2>M-105 Japan Flat</h2>
<table class="spec"><tr><th>Type</th><td>Beam / flat</td></tr><tr><th>Price</th><td class="num">{m105['price']} (Kohden)</td></tr></table>
<ul><li>Long-lasting silicone.</li><li>Less noise and chatter.</li><li>Strong corrosion resistance.</li></ul>{sizes(m105['sizes'])}
<p class="small" style="margin-top:14px">For most Japanese cars we suggest the <a href="{P}hybrid-wiper-blades/">Silicone Hybrid M1001</a> first.</p></div></section>
<section class="sec"><div class="wrap">{shop_block('flat')}</div></section>'''
    urls.append(page('silicone-flat-wiper-blades/', 'MOON Silicone Flat Wiper Blades Singapore | M-102, M-105',
        'MOON silicone beam / flat wiper blades: M-102 at $30 to $80 and M-105 Japan Flat at $30, Kohden Singapore. Sizes 12 to 28 inch. Call +65 6966 6565.',
        'Beam / flat blades', body, [seller, product_ld('m102', fdesc, None), product_ld('m105', fdesc, None)]))

    # REAR
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Rear blades')}<h1>MOON rear wiper blades</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">Three rear types, $20 to $22 at Kohden.</p><div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap prose">
<table class="spec"><tr><th>M-GRA Rear A-type</th><td class="num">{rr['mgra']['price']}{sizes(rr['mgra']['sizes'])}</td></tr>
<tr><th>M-GRB Rear B-type</th><td class="num">{rr['mgrb']['price']}{sizes(rr['mgrb']['sizes'])}</td></tr>
<tr><th>M-FR Rear Conti</th><td class="num">{rr['mfr']['price']}{sizes(rr['mfr']['sizes'])}</td></tr></table>
<ul><li>Resin frame like the original part.</li><li>Easy to replace yourself.</li></ul>
<p class="small">Not sure which rear type your car takes? Call Kohden with the make, model and year.</p></div></section>
<section class="sec"><div class="wrap">{shop_block('rear')}</div></section>'''
    rdesc = 'MOON rear wiper blade with a resin frame like the original part, sold in Singapore by Kohden.'
    urls.append(page('rear-wiper-blades/', 'MOON Rear Wiper Blades Singapore | M-GRA, M-GRB, M-FR from $20',
        'MOON rear wiper blades at Kohden Singapore: M-GRA $20, M-GRB $20, M-FR Conti $22. Sizes 10 to 16 inch. Call +65 6966 6565.',
        'Rear blades', body, [seller] + [product_ld(k, rdesc, None) for k in ('mgra', 'mgrb', 'mfr')]))

    # SIZE GUIDE
    pairs = ''.join(f'<div><b>{i}"</b> <span class="num">{m}mm</span></div>' for i, m in D['size_pairs'])
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Size guide')}<h1>Wiper blade size guide</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">Three ways to find your size. The fastest is a call.</p><div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap prose"><ol class="steps">
<li><div><h3>Read the box</h3><p>The old blade's box or the blade itself shows the length, often in inches.</p></div></li>
<li><div><h3>Measure tip to tip</h3><p>Measure the rubber from end to end. Driver and passenger sides are often different, so measure both, plus the rear.</p></div></li>
<li><div><h3>Call Kohden</h3><p>Give your car's make, model and year. Kohden will match the size and type.</p></div></li></ol></div></section>
<section class="sec white"><div class="wrap prose"><h2>Inches to millimetres</h2>
<p>Fu-Gang, the maker, lists sizes in inches with millimetres, for example 12" (300mm) and 28" (700mm). The pairs below use the same step of 25mm per inch.</p>
<div class="pairs">{pairs}</div></div></section>
<section class="sec"><div class="wrap">{shop_block('size')}</div></section>'''
    urls.append(page('wiper-size-guide/', 'Wiper Blade Size Guide Singapore | Inches to mm | MOON',
        'How to find your wiper blade size: read the box, measure tip to tip, or call Kohden with your make, model and year. Inch to mm pairs.',
        'Size guide', body, [seller]))

    # WHERE TO BUY
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Where to buy')}<h1>Where to buy MOON wiper blades</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">Kohden in Kaki Bukit, Monday to Friday.</p><div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap">{shop_block('buy')}</div></section>'''
    urls.append(page('where-to-buy/', 'Where to Buy MOON Wiper Blades Singapore | Kohden, Kaki Bukit',
        'Buy MOON wiper blades from KohDen International, 7 Kaki Bukit Road 1 #01-15 Eunos Technolink, Singapore 415937. +65 6966 6565, Mon to Fri 9am to 5pm.',
        'Where to buy', body, [seller]))

    # FAQ
    faqs = [
     ('Which MOON blade should I get for a Japanese car?', 'Start with the MOON Silicone Hybrid M1001. Kohden sells it from $30 to $80 depending on size.'),
     ('Which MOON blade is for Continental cars?', 'Silicone Advance, the higher-end line. It comes with the adapter set. Call Kohden for the price.'),
     ('How much are MOON wiper blades in Singapore?', "Kohden's published prices: Silicone Hybrid M1001 $30 to $80, flat M-102 $30 to $80, M-105 Japan Flat $30, rear M-GRA and M-GRB $20, rear M-FR $22."),
     ('Do MOON blades really last twice as long?', 'That is the maker\'s claim from laboratory testing: the MOON silicone blade lasted 2X longer than traditional natural rubber.'),
     ('Where are MOON wiper blades made?', 'In Taiwan, by Fu-Gang. Fu-Gang is certified ISO 9001:2015 and IATF 16949:2016.'),
     ('How do I find my wiper size?', 'Read the old blade\'s box, measure the rubber tip to tip, or call Kohden on +65 6966 6565 with your make, model and year.'),
     ('Is there anything to do before first use?', 'The MOON leaflet says to clean the glass, then let the blades wipe dry glass for 5 minutes or more.'),
     ('Where can I buy MOON blades?', f'From {S["name"]}, {S["street"]}, Singapore {S["postcode"]}. {S["hours_display"]}.'),
    ]
    q = ''.join(f'<details><summary>{e(a)}</summary><p>{e(b)}</p></details>' for a, b in faqs)
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('FAQ')}<h1>MOON wiper blade questions</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">Short answers. Call Kohden for anything else.</p><div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap faq prose">{q}</div></section>
<section class="sec"><div class="wrap">{shop_block('faq')}</div></section>'''
    fld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]}
    urls.append(page('faq/', 'MOON Wiper Blades FAQ Singapore | Sizes, Prices, Fit',
        'Answers on MOON wiper blades in Singapore: which blade for Japanese or Continental cars, Kohden prices, sizes, first use and where to buy.',
        'FAQ', body, [fld]))

    # ARTICLES (empty hub)
    body = f'''<section class="ph-hero"><div class="wrap"><div>{crumb('Articles')}<h1>Wiper blade articles</h1>
<p class="line" style="font-size:1.15rem;margin-top:12px">No articles yet. Guides will appear here.</p><div class="btns">{call('hero')}{wa('hero')}</div></div></div></section>
<section class="sec"><div class="wrap"><ul class="range" id="articles"></ul><p class="small" style="margin-top:12px">Until then, try the <a href="{P}wiper-size-guide/">size guide</a> or the <a href="{P}faq/">FAQ</a>.</p></div></section>'''
    urls.append(page('articles/', 'Wiper Blade Articles | MOON Singapore',
        'Wiper blade guides for Singapore drivers from MOON. No articles yet.', 'Articles', body, [{"@type": "CollectionPage", "name": "Wiper blade articles", "url": BASE + "articles/"}]))

    sm = ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    print('\n'.join(urls))

if __name__ == '__main__':
    build()

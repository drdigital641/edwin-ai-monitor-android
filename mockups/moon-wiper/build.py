#!/usr/bin/env python3
"""MOON wiper blades SG preview, v3 water-blue (Page One, Edwin 17 Nov 2026 4:57pm SGT).
Template-first: head/header/footer/dock/contact live here once; facts only in data.json; one CSS (static/site.css).
CTA rule: per page exactly 3 call CTAs = header icon, hero button, sticky dock. Contact details shown once per page.
Build: python3 build.py -> site/. WhatsApp: set data.json "whatsapp" (digits) and rebuild; slots appear in header, hero, dock."""
import json, os, shutil, hashlib, html, urllib.parse
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf8'))
OUT = os.path.join(HERE, 'site')
BASE, P, S, PR, IMG = D['base'], D['path'], D['seller'], D['products'], D['images']
TODAY = date.today().isoformat()
e = html.escape

def vhash(rel):
    return hashlib.sha256(open(os.path.join(HERE, 'static', rel), 'rb').read()).hexdigest()[:8]

def svg(p, sw=2):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
ICON = {
 'call': svg('<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>'),
 'wa': svg('<path d="M3 21l1.7-4.6A9 9 0 1 1 8 19.6z"/>'),
 'menu': svg('<path d="M3 7h18M3 12h18M3 17h18"/>'),
 'pin': svg('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
 'mail': svg('<rect x="3" y="5" width="18" height="14"/><path d="M3 6l9 7 9-7"/>'),
 'wind': svg('<path d="M3 9h11a3 3 0 1 0-3-3M3 15h15a3 3 0 1 1-3 3M3 12h7"/>', 1.8),
 'quiet': svg('<path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9l4 6M21 9l-4 6"/>', 1.8),
 'curve': svg('<path d="M3 17c4-8 14-8 18 0"/><path d="M3 21c4-8 14-8 18 0" opacity=".45"/>', 1.8),
 'leaf': svg('<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15z"/><path d="M5 19l7-7"/>', 1.8),
 'shield': svg('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>', 1.8),
 'ruler': svg('<rect x="2" y="8" width="20" height="8"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/>', 1.8),
 'box': svg('<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>', 1.8),
 'phone': svg('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>', 1.8),
 'drop': svg('<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>', 1.8),
 'wipe': svg('<path d="M4 20L20 6"/><path d="M4 20h4"/>', 1.8),
}

WORDMARK = '''<svg viewBox="0 0 132 30" role="img" aria-label="MOON"><defs><linearGradient id="mg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E5DA6"/><stop offset="1" stop-color="#073A6B"/></linearGradient></defs>
<g fill="url(#mg)"><path d="M1 29V1h7l7 16 7-16h7v28h-6V12l-6 14h-4L7 12v17z"/><path d="M34 15C34 6 39 1 47 1s13 5 13 14-5 14-13 14-13-5-13-14zm6 0c0 5.6 2.6 8.6 7 8.6s7-3 7-8.6-2.6-8.6-7-8.6-7 3-7 8.6z"/><path d="M64 15C64 6 69 1 77 1s13 5 13 14-5 14-13 14-13-5-13-14zm6 0c0 5.6 2.6 8.6 7 8.6s7-3 7-8.6-2.6-8.6-7-8.6-7 3-7 8.6z"/><path d="M95 29V1h6l12 17V1h6v28h-6L101 12v17z"/></g><path d="M126 13s-5 5.6-5 9a5 5 0 0 0 10 0c0-3.4-5-9-5-9z" fill="#0B8DB8"/></svg>'''

NAV = [('', 'Home', ''), ('hybrid-wiper-blades/', 'Silicone Hybrid', 'Japanese cars'),
       ('conventional-wiper-blades/', 'Silicone Advance', 'Continental cars'),
       ('silicone-flat-wiper-blades/', 'Flat blades', 'M-102, M-105'), ('rear-wiper-blades/', 'Rear blades', 'M-GRA, M-GRB, M-FR'),
       ('wiper-size-guide/', 'Size guide', 'Table and adapters'), ('where-to-buy/', 'Where to buy', 'Kohden, Kaki Bukit'),
       ('faq/', 'FAQ', ''), ('articles/', 'Articles', '')]
DNAV = [('hybrid-wiper-blades/', 'Hybrid'), ('conventional-wiper-blades/', 'Advance'), ('silicone-flat-wiper-blades/', 'Flat'),
        ('rear-wiper-blades/', 'Rear'), ('wiper-size-guide/', 'Sizes'), ('where-to-buy/', 'Where to buy')]

def wa_url():
    n = ''.join(c for c in D['whatsapp'] if c.isdigit())
    return f'https://wa.me/{n}?text={urllib.parse.quote(D["whatsapp_text"])}' if n else ''

# ---- the only 3 call CTAs a page may carry (+ WhatsApp twins, hidden until a number exists) ----
def cta_header():
    w = wa_url()
    wa = f'<a class="ic wa" href="{e(w)}" target="_blank" rel="noopener" data-ref="header-whatsapp" aria-label="WhatsApp Kohden">{ICON["wa"]}</a>' if w else ''
    return wa + f'<a class="ic" href="tel:{S["tel"]}" data-ref="header-call" aria-label="Call Kohden {S["phone_display"]}">{ICON["call"]}</a>'

def cta_hero(label=None):
    w = wa_url()
    wa = f'<a class="btn wa" href="{e(w)}" target="_blank" rel="noopener" data-ref="hero-whatsapp">{ICON["wa"]}<span>WhatsApp Kohden</span></a>' if w else ''
    return f'<div class="btns"><a class="btn" id="hero-cta" href="tel:{S["tel"]}" data-ref="hero-call">{ICON["call"]}<span>{e(label or "Call Kohden " + S["phone_short"])}</span></a>{wa}</div>'

def cta_dock():
    w = wa_url()
    wa = f'<a class="btn wa" href="{e(w)}" target="_blank" rel="noopener" data-ref="dock-whatsapp">{ICON["wa"]}<span>WhatsApp</span></a>' if w else ''
    return f'<nav class="dock" data-ref="sticky-dock" aria-label="Call Kohden"><a class="btn" href="tel:{S["tel"]}" data-ref="dock-call">{ICON["call"]}<span>Call Kohden {S["phone_short"]}</span></a>{wa}</nav>'

def contact(ref):
    """Contact details, rendered ONCE per page (footer, or the Where to buy body)."""
    return f'''<div class="kd"><dl><dt>Seller</dt><dd>{e(S['name'])}</dd><dt>Address</dt><dd>{e(S['street'])}, Singapore {S['postcode']}</dd>
<dt>Phone</dt><dd class="num">{S['phone_display']}</dd><dt>Hours</dt><dd>{e(S['hours_display'])}</dd></dl>
<div class="links"><a href="{e(S['maps'])}" target="_blank" rel="noopener" data-cta="directions" data-ref="{ref}-directions">{ICON['pin']}Directions</a><a href="mailto:{S['email']}" data-ref="{ref}-email">{ICON['mail']}{S['email']}</a></div></div>'''

def pic(name, cls='', eager=False, sizes=None, w=1080, h=1350, small=640):
    alt = IMG[name]
    src = f'{P}img/{name}'
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    sz = sizes or '(min-width:900px) 560px, 100vw'
    return (f'<picture><source type="image/webp" srcset="{src}-{small}.webp {small}w, {src}.webp {w}w" sizes="{sz}">'
            f'<img class="{cls}" src="{src}.jpg" srcset="{src}-{small}.jpg {small}w, {src}.jpg {w}w" sizes="{sz}" width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async"></picture>')

def tile(name, sizes='(min-width:900px) 280px, 50vw', eager=False):
    return pic(name, sizes=sizes, w=720, h=720, small=360, eager=eager)

def mm(i):
    return round(i * 25.4)

def hero(img, crumb, h1, line, extra='', label=None):
    c = f'<p class="crumb"><a href="{P}">Home</a> / {e(crumb)}</p>' if crumb else ''
    return f'''<section class="hero wv"><div class="grid"><figure class="art">{pic(img, eager=True)}<span class="sheen" aria-hidden="true"></span></figure>
<div class="copy wrap">{c}<h1>{h1}</h1><p class="line">{line}</p>{extra}{cta_hero(label)}</div></div></section>'''

def band(crumb, h1, line, bg='band-rain', extra=''):
    return f'''<section class="band wv" style="background-image:image-set(url('{P}img/{bg}-800.webp') type('image/webp'),url('{P}img/{bg}-800.jpg') type('image/jpeg'))"><div class="wrap">
<p class="crumb"><a href="{P}">Home</a> / {e(crumb)}</p><h1>{h1}</h1><p class="line">{line}</p>{extra}{cta_hero()}</div></section>'''

# ---- adapter chart (Silicone Advance only) ----
def adapter_svg(code):
    g = '<svg viewBox="0 0 200 110" aria-hidden="true" fill="none" stroke="#0A4D8C" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">'
    arm = '#A9BED0'; red = '#0B8DB8'
    s = {
     'D02': f'<path d="M20 70h160" stroke="{arm}" stroke-width="8"/><rect x="62" y="40" width="76" height="30"/><rect x="86" y="26" width="28" height="14" fill="{red}" stroke="{red}"/><path d="M62 92h76" stroke="{red}" stroke-width="2"/><text x="100" y="106" font-size="12" text-anchor="middle" fill="#46607A" stroke="none" font-family="sans-serif">22mm</text>',
     'i02': f'<path d="M20 70h160" stroke="{arm}" stroke-width="8"/><rect x="66" y="40" width="68" height="30"/><path d="M66 46h-14v18h14M134 46h14v18h-14" stroke="{red}"/><path d="M52 55h-10M148 55h10" stroke="{red}"/>',
     'B02': f'<path d="M20 70h160" stroke="{arm}" stroke-width="8"/><rect x="58" y="38" width="84" height="32"/><circle cx="100" cy="54" r="9" stroke="{red}"/><path d="M91 54H24" stroke="{red}"/><text x="100" y="104" font-size="12" text-anchor="middle" fill="#46607A" stroke="none" font-family="sans-serif">19 / 22mm</text>',
     'L02': f'<path d="M20 74h160" stroke="{arm}" stroke-width="8"/><rect x="50" y="56" width="100" height="14"/><path d="M72 56v-10h56v10" stroke="{red}"/><text x="100" y="104" font-size="12" text-anchor="middle" fill="#46607A" stroke="none" font-family="sans-serif">19mm</text>',
     'G02': f'<path d="M20 70h160" stroke="{arm}" stroke-width="8"/><rect x="58" y="40" width="80" height="30"/><path d="M138 48h26v14h-14v-6" stroke="{red}"/>',
     'A02': f'<path d="M20 70h120" stroke="{arm}" stroke-width="8"/><path d="M140 70V44a14 14 0 0 0-14-14H40" stroke="{arm}" stroke-width="8"/><rect x="62" y="44" width="62" height="22"/><path d="M62 36h62" stroke="{red}"/>',
     'J02': f'<path d="M20 70h160" stroke="{arm}" stroke-width="8"/><rect x="62" y="40" width="76" height="30"/><path d="M86 40V26h28v14" stroke="{red}"/><text x="100" y="62" font-size="18" text-anchor="middle" fill="#0B8DB8" stroke="none" font-family="sans-serif" font-weight="700">C</text>',
     'K02': f'<path d="M20 70h160" stroke="{arm}" stroke-width="8"/><rect x="62" y="40" width="76" height="30"/><path d="M86 40V26h28v14" stroke="{red}"/><text x="100" y="62" font-size="18" text-anchor="middle" fill="#0B8DB8" stroke="none" font-family="sans-serif" font-weight="700">M</text>',
    }
    return g + s[code] + '</svg>'

def adapter_chart(title_tag='h2'):
    li = ''.join(f'<li>{adapter_svg(c)}<span class="cd">{c}</span><span class="nm">{e(t)}</span>{f"<span class=sz>{e(n)}</span>" if n else ""}</li>' for c, t, n in D['adapters'])
    return f'''<div class="head"><{title_tag}>Adapter chart</{title_tag}><p>Redrawn from the MOON leaflet. Drawings are simplified; Kohden confirms which one your wiper arm takes.</p></div>
<p class="only">Silicone Advance only</p><ul class="ad" aria-label="Silicone Advance adapters">{li}</ul>'''

def crumbs_ld(slug, name):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE}]
    if slug: items.append({"@type": "ListItem", "position": 2, "name": name, "item": BASE + slug})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def seller_ld():
    return {"@type": "AutoPartsStore", "@id": BASE + "where-to-buy/#kohden", "name": S['name'], "telephone": S['phone_display'], "email": S['email'],
            "address": {"@type": "PostalAddress", "streetAddress": S['street'], "postalCode": S['postcode'], "addressLocality": "Singapore", "addressCountry": "SG"},
            "openingHours": S['hours_schema'], "url": S['web']}

def product_ld(key, desc, img):
    p = PR[key]
    d = {"@type": "Product", "name": p['name'], "brand": {"@type": "Brand", "name": "MOON"},
         "manufacturer": {"@type": "Organization", "name": "Fu-Gang", "address": {"@type": "PostalAddress", "addressCountry": "TW"}},
         "description": desc, "image": f'{BASE}img/{img}.jpg'}
    if p.get('low'):
        sel = {"@id": BASE + "where-to-buy/#kohden"}
        d["offers"] = ({"@type": "Offer", "priceCurrency": "SGD", "price": str(p['low']), "seller": sel} if p['low'] == p['high'] else
                       {"@type": "AggregateOffer", "priceCurrency": "SGD", "lowPrice": str(p['low']), "highPrice": str(p['high']), "seller": sel})
    return d

def page(slug, title, desc, crumbname, body, ld=None, contact_in_body=False):
    url = BASE + slug
    graph = [crumbs_ld(slug, crumbname), {"@type": "WebSite", "@id": BASE + "#site", "name": D['site_name'], "url": BASE, "inLanguage": "en-SG"}] + (ld or [])
    cur = lambda u: ' aria-current="page"' if u == slug else ''
    nav_m = ''.join(f'<li><a href="{P}{u}"{cur(u)}>{e(n)}{f"<small>{e(s)}</small>" if s else ""}</a></li>' for u, n, s in NAV)
    nav_d = ''.join(f'<li><a href="{P}{u}"{cur(u)}>{e(n)}</a></li>' for u, n in DNAV)
    css, cta, js = vhash('site.css'), vhash('p1-cta.js'), vhash('site.js')
    fcontact = '' if contact_in_body else f'<div><h2>Buy from Kohden</h2>{contact("footer")}</div>'
    out = f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(D['site_name'])}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og.jpg"><meta property="og:image:secure_url" content="{BASE}og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="MOON silicone hybrid wiper blade on water-beaded glass"><meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}og.jpg">
<meta name="theme-color" content="#0A4D8C"><link rel="icon" href="{P}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{P}fonts/saira-condensed-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}site.css?v={css}"><script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head><body>
<header class="hd"><div class="wrap"><a class="mark" href="{P}" aria-label="MOON wiper blades Singapore, home">{WORDMARK}</a>
<ul class="dnav">{nav_d}</ul>{cta_header()}
<details class="nav"><summary aria-label="Menu">{ICON['menu']}</summary><ul>{nav_m}</ul></details></div></header>
<main>{body}</main>
<footer class="ft"><div class="wrap">{fcontact}
<div><h2>Blades</h2><ul class="fl">{''.join(f'<li><a href="{P}{u}">{e(n)}</a></li>' for u, n, s in NAV[1:])}</ul></div>
<p class="legal">MOON wiper blades are made in Taiwan by Fu-Gang (ISO 9001:2015, IATF 16949:2016). Prices are Kohden's published Singapore prices and may change.</p>
</div></footer>
{cta_dock()}
<script src="{P}site.js?v={js}" defer></script><script src="{P}p1-cta.js?v={cta}" defer></script>
</body></html>
'''
    path = os.path.join(OUT, slug, 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf8').write(out)
    return url

def size_rows(pick):
    return ''.join(f'<tr><th scope="row">{s}</th><td class="num">{mm(int(s.split(chr(34))[0]))} mm</td></tr>' for s in pick)

def build():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ['site.css', 'site.js', 'p1-cta.js', 'favicon.svg', 'og.jpg']:
        shutil.copy(os.path.join(HERE, 'static', f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(HERE, 'static', 'fonts'), os.path.join(OUT, 'fonts'))
    shutil.copytree(os.path.join(HERE, 'static', 'img'), os.path.join(OUT, 'img'))
    h, fl, m105, adv = PR['m1001'], PR['m102'], PR['m105'], PR['advance']
    urls, seller = [], seller_ld()
    bg = lambda n: f"background-image:image-set(url('{P}img/{n}-800.webp') type('image/webp'),url('{P}img/{n}-800.jpg') type('image/jpeg'))"

    # HOME
    body = hero('hero-hybrid', '', 'Moon hybrid wiper blades for <span class="hl">Singapore</span>',
                'Taiwan-made silicone hybrid for Japanese cars, then Silicone Advance for Continental.', f'<span class="chip">Hybrid M1001 from $30 at Kohden</span>')
    body += f'''<section class="sec"><div class="wrap"><div class="head"><h2>Two lines. <span class="hl">Two kinds of car.</span></h2></div>
<div class="duo"><a class="pn card" href="{P}hybrid-wiper-blades/">{tile('tile-m1001', '(min-width:900px) 620px, 100vw', eager=True)}<div class="tx"><h3>Silicone Hybrid M1001</h3><p class="for">For Japanese cars</p><p class="pr">{h['price']} at Kohden</p><span class="go">See the Hybrid</span></div></a>
<a class="pn sm card" href="{P}conventional-wiper-blades/">{tile('tile-advance', '(min-width:900px) 480px, 120px', eager=True)}<div class="tx"><h3>Silicone Advance</h3><p class="for">For Continental cars</p><p class="pr">Adapter included. Price from Kohden.</p><span class="go">See Advance</span></div></a></div></div></section>
<section class="stat wv" style="{bg('band-rain')}"><div class="wrap"><span class="big">2X</span><p>longer lasting than traditional natural rubber.</p>
<p class="small">The maker's claim, from its own laboratory testing. Made in Taiwan by Fu-Gang, ISO 9001:2015 and IATF 16949:2016.</p></div></section>
<section class="sec"><div class="wrap"><div class="head"><h2>Also in the range</h2></div><ul class="rg">
<li class="card"><a href="{P}silicone-flat-wiper-blades/">{tile('tile-m102')}<div><b>Flat M-102</b><span>{fl['price']}</span></div></a></li>
<li><a href="{P}silicone-flat-wiper-blades/">{tile('tile-m105')}<div><b>Japan Flat M-105</b><span>{m105['price']}</span></div></a></li>
<li><a href="{P}rear-wiper-blades/">{tile('tile-mgr')}<div><b>Rear M-GRA / M-GRB</b><span>$20</span></div></a></li>
<li><a href="{P}rear-wiper-blades/">{tile('tile-mfr')}<div><b>Rear Conti M-FR</b><span>{PR['mfr']['price']}</span></div></a></li></ul></div></section>
<section class="sec alt"><div class="wrap"><div class="head"><h2>Know your size</h2><p>Some common front sizes, in inches and millimetres:</p></div>
<table class="tbl"><thead><tr><th>Size</th><th>Length</th><th class="c">Hybrid</th><th class="c">Flat</th></tr></thead><tbody>
{''.join(f'<tr><th scope="row">{i}"</th><td class="num">{mm(i)} mm</td><td class="y">Yes</td><td class="y">Yes</td></tr>' for i in (14, 16, 18, 24, 26))}</tbody></table>
<p style="margin-top:16px"><a href="{P}wiper-size-guide/">Full size table and adapter chart</a></p></div></section>'''
    urls.append(page('', 'MOON Hybrid Wiper Blades Singapore | Silicone, Made in Taiwan',
        'MOON silicone hybrid wiper blades for Japanese cars and Silicone Advance for Continental cars. Kohden prices $20 to $80. Call +65 6966 6565.',
        'Home', body, [seller, {"@type": "Brand", "name": "MOON"}]))

    # HYBRID
    hdesc = 'MOON Silicone Hybrid M1001 wiper blade for Japanese cars, sold in Singapore by Kohden. Made in Taiwan by Fu-Gang.'
    kd_h = ['Super streamlined shape, reduced wind-lift', 'Increasing durability, reducing chattering', 'Multi-curvature rail spline', 'Eco-product, material recyclable']
    body = hero('hero-hybrid', 'Silicone Hybrid', 'Silicone Hybrid <span class="hl">M1001</span>', 'For Japanese cars. Kohden matches it to your make, model and year.',
                f'<span class="chip">{h["price"]} at Kohden</span>')
    body += f'''<section class="sec"><div class="wrap"><div class="head"><h2>Kohden's description</h2><p>As listed on Kohden's M1001 product page; these are the seller's and maker's claims.</p></div>
<ul class="dl">{''.join(f'<li>{e(x)}</li>' for x in kd_h)}</ul><p class="src">Source: <a href="{h['url']}" target="_blank" rel="noopener">kohden.com.sg</a></p></div></section>
<section class="sec alt"><div class="wrap"><div class="head"><h2>Sizes at Kohden</h2><p>Inches as sold; millimetres are inches x 25.4.</p></div>
<table class="tbl"><thead><tr><th>Size</th><th>Length</th></tr></thead><tbody>{size_rows([s for s in h['sizes'] if '+' not in s])}
<tr><th scope="row">30" + 14"</th><td>Set of two</td></tr></tbody></table></div></section>
<section class="sec"><div class="wrap"><div class="head"><h2>First use</h2><p>From the MOON leaflet.</p></div>
<ol class="steps"><li><div><b>Clean the glass</b><span>Clean the windscreen before fitting.</span></div></li><li><div><b>Wipe dry for 5 minutes or more</b><span>Let the new blades run on dry glass.</span></div></li></ol>
<p style="margin-top:22px">Continental car? <a href="{P}conventional-wiper-blades/">See Silicone Advance</a></p></div></section>'''
    urls.append(page('hybrid-wiper-blades/', 'MOON Silicone Hybrid Wiper Blades M1001 Singapore | $30 to $80',
        'MOON Silicone Hybrid M1001 wiper blades for Japanese cars, 12 to 28 inch, $30 to $80 at Kohden Singapore. Call +65 6966 6565 to match your car.',
        'Silicone Hybrid M1001', body, [seller, product_ld('m1001', hdesc, 'hero-hybrid')]))

    # ADVANCE
    adesc = 'MOON Silicone Advance, the higher-end line for Continental cars, with water repellency and Siflon rubber technology. Adapter set included.'
    body = hero('hero-advance', 'Silicone Advance', 'Silicone <span class="hl">Advance</span>', 'The higher-end line for Continental cars. Adapter included.',
                '<p class="small" style="margin-top:12px">Pictured: Fu-Gang conventional blade.</p>', label='Call Kohden for price')
    body += f'''<section class="sec"><div class="wrap">{adapter_chart()}</div></section>
<section class="sec alt"><div class="wrap"><div class="head"><h2>On the pack</h2></div><div class="fx">
<div>{ICON['drop']}<b>Water repellency</b><span>Printed on the pack</span></div><div>{ICON['shield']}<b>Siflon rubber technology</b><span>Printed on the pack</span></div>
<div>{ICON['wipe']}<b>2X longer lasting</b><span>Maker's lab test vs natural rubber</span></div><div>{ICON['ruler']}<b>26" and 16"</b><span>Packs seen in Singapore</span></div></div>
<p style="margin-top:22px">Japanese car? <a href="{P}hybrid-wiper-blades/">See Silicone Hybrid M1001</a></p></div></section>'''
    urls.append(page('conventional-wiper-blades/', 'MOON Silicone Advance Wiper Blades Singapore | Continental Cars, Adapter Included',
        'MOON Silicone Advance wiper blades for Continental cars, adapter set included. Water repellent silicone. Call Kohden +65 6966 6565 for price and fit.',
        'Silicone Advance', body, [seller, product_ld('advance', adesc, 'tile-advance')]))

    # FLAT
    fdesc = 'MOON silicone beam / flat wiper blade, sold in Singapore by Kohden.'
    fb = f'<p class="src">Kohden\'s M-102 listing says:</p><ul class="dl"><li>Long-lasting silicone</li><li>Less noise and chatter</li><li>Strong corrosion resistance</li></ul>'
    body = hero('hero-flat', 'Flat blades', 'Silicone <span class="hl">flat</span> blades', 'Beam blades with no frame: M-102 and M-105 Japan Flat.', f'<span class="chip">From $30 at Kohden</span>')
    body += f'''<section class="sec"><div class="wrap ps">
<article class="card">{tile('tile-m102', '(min-width:900px) 560px, 100vw')}<div class="tx"><h3>M-102 Silicone Flat</h3><p class="pr num" style="margin:6px 0 0">{fl['price']}</p>{fb}<ul class="sizes">{''.join(f'<li>{e(s)}</li>' for s in fl['sizes'])}</ul></div></article>
<article class="card">{tile('tile-m105', '(min-width:900px) 560px, 100vw')}<div class="tx"><h3>M-105 Japan Flat</h3><p class="pr num" style="margin:6px 0 0">{m105['price']}</p><ul class="sizes">{''.join(f'<li>{e(s)}</li>' for s in m105['sizes'])}</ul></div></article>
</div><div class="wrap"><p style="margin-top:22px">For most Japanese cars, start with the <a href="{P}hybrid-wiper-blades/">Silicone Hybrid M1001</a>.</p></div></section>'''
    urls.append(page('silicone-flat-wiper-blades/', 'MOON Silicone Flat Wiper Blades Singapore | M-102, M-105',
        'MOON silicone beam / flat wiper blades: M-102 at $30 to $80 and M-105 Japan Flat at $30, Kohden Singapore. Sizes 12 to 28 inch.',
        'Flat blades', body, [seller, product_ld('m102', fdesc, 'tile-m102'), product_ld('m105', fdesc, 'tile-m105')]))

    # REAR
    rr = [('tile-mgr', 'M-GRA Rear A-type', PR['mgra']), ('tile-mgr', 'M-GRB Rear B-type', PR['mgrb']), ('tile-mfr', 'M-FR Rear Conti', PR['mfr'])]
    rows = ''.join(f'<li class="card">{tile(t, "116px")}<div><b>{n}</b><span class="pr">{p["price"]}</span><div class="sz">{", ".join(p["sizes"])}</div></div></li>' for t, n, p in rr)
    body = hero('hero-rear', 'Rear blades', '<span class="hl">Rear</span> wiper blades', 'Three rear types, $20 to $22 at Kohden.')
    body += f'''<section class="sec"><div class="wrap"><ul class="rr">{rows}</ul>
<div class="fx" style="margin-top:22px"><div>{ICON['box']}<b>Resin frame like the original part</b><span>Kohden product description</span></div><div>{ICON['wipe']}<b>Easy to replace yourself</b><span>Kohden product description</span></div></div></div></section>'''
    rdesc = 'MOON rear wiper blade with a resin frame like the original part, sold in Singapore by Kohden.'
    urls.append(page('rear-wiper-blades/', 'MOON Rear Wiper Blades Singapore | M-GRA, M-GRB, M-FR from $20',
        'MOON rear wiper blades at Kohden Singapore: M-GRA $20, M-GRB $20, M-FR Conti $22. Sizes 10 to 16 inch.',
        'Rear blades', body, [seller] + [product_ld(k, rdesc, t) for k, t in (('mgra', 'tile-mgr'), ('mgrb', 'tile-mgr'), ('mfr', 'tile-mfr'))]))

    # SIZE GUIDE
    def has(p, i): return any(s.startswith(f'{i}"') for s in PR[p]['sizes'])
    rows = ''
    for i in range(10, 31):
        cols = [has('m1001', i), has('m102', i), has('m105', i), has('mgra', i) or has('mgrb', i) or has('mfr', i)]
        if not any(cols): continue
        rows += f'<tr><th scope="row">{i}"</th><td class="num">{mm(i)}</td>' + ''.join('<td class="y">&#10003;</td>' if c else '<td class="n">-</td>' for c in cols) + '</tr>'
    cat = ', '.join(f'{k}" = {v}mm' for k, v in D['catalogue_mm_labels'].items())
    body = band('Size guide', 'Wiper <span class="hl">size</span> guide', 'Find your size, then check which MOON blade comes in it.')
    body += f'''<section class="sec"><div class="wrap"><div class="head"><h2>Three ways to find it</h2></div><ol class="steps">
<li><div><b>Read the old box or blade</b><span>The length is printed, usually in inches.</span></div></li>
<li><div><b>Measure tip to tip</b><span>Measure the rubber end to end, driver and passenger side separately, plus the rear.</span></div></li>
<li><div><b>Call Kohden</b><span>Give the make, model and year; they match the size and type.</span></div></li></ol></div></section>
<section class="sec alt"><div class="wrap"><div class="head"><h2>Size table</h2><p>Sizes Kohden lists for each MOON blade. Millimetres are inches x 25.4, rounded.</p></div>
<table class="tbl"><thead><tr><th>Size</th><th>mm</th><th class="c">Hybrid M1001</th><th class="c">Flat M-102</th><th class="c">Japan Flat M-105</th><th class="c">Rear</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small" style="margin-top:14px">Fu-Gang's catalogue uses rounded labels, for example {cat}. Hybrid and M-102 also come as a 30" + 14" set. Rear: M-GRA 10-14", M-GRB 12-16", M-FR 10-16".</p></div></section>
<section class="sec"><div class="wrap">{adapter_chart()}</div></section>'''
    urls.append(page('wiper-size-guide/', 'Wiper Blade Size Guide Singapore | Size Table, mm, Adapters | MOON',
        'MOON wiper size table for Singapore: every size Kohden lists for Hybrid, Flat, Japan Flat and rear blades, in inches and mm, plus the Silicone Advance adapter chart.',
        'Size guide', body, [seller]))

    # WHERE TO BUY
    body = band('Where to buy', 'Where to <span class="hl">buy</span>', 'Kohden in Kaki Bukit sells the MOON range in Singapore.')
    body += f'''<section class="sec"><div class="wrap">{contact('buy')}</div></section>'''
    urls.append(page('where-to-buy/', 'Where to Buy MOON Wiper Blades Singapore | Kohden, Kaki Bukit',
        'Buy MOON wiper blades from KohDen International, 7 Kaki Bukit Road 1 #01-15 Eunos Technolink, Singapore 415937. Mon to Fri 9am to 5pm.',
        'Where to buy', body, [seller], contact_in_body=True))

    # FAQ
    faqs = [
     ('Which MOON blade fits a Japanese car?', 'Start with the Silicone Hybrid M1001. Kohden sells it from $30 to $80 depending on size.'),
     ('Which MOON blade is for Continental cars?', 'Silicone Advance, the higher-end line. It comes with an adapter set. Kohden gives the price.'),
     ('How much are MOON wiper blades?', "Kohden's published prices: Hybrid M1001 $30 to $80, Flat M-102 $30 to $80, Japan Flat M-105 $30, rear M-GRA and M-GRB $20, rear M-FR $22."),
     ('Do they really last twice as long?', "That is the maker's claim from laboratory testing: the MOON silicone blade lasted 2X longer than traditional natural rubber."),
     ('Where are MOON blades made?', 'In Taiwan, by Fu-Gang, which holds ISO 9001:2015 and IATF 16949:2016.'),
     ('How do I find my size?', 'Read the old box or blade, measure tip to tip, or call Kohden with the make, model and year. The size guide has the full table.'),
     ('Anything to do before first use?', 'The MOON leaflet says to clean the glass, then let the blades wipe dry glass for 5 minutes or more.'),
     ('Which blades use the adapter chart?', 'Only Silicone Advance. The adapter chart does not apply to the Hybrid, flat or rear blades.'),
    ]
    q = ''.join(f'<details><summary>{e(a)}</summary><p>{e(b)}</p></details>' for a, b in faqs)
    body = band('FAQ', 'Moon wiper <span class="hl">questions</span>', 'Short answers from Kohden\'s published facts.')
    body += f'<section class="sec"><div class="wrap faq">{q}</div></section>'
    urls.append(page('faq/', 'MOON Wiper Blades FAQ Singapore | Sizes, Prices, Fit',
        'Answers on MOON wiper blades in Singapore: which blade for Japanese or Continental cars, Kohden prices, sizes, first use and the adapter chart.',
        'FAQ', body, [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": a, "acceptedAnswer": {"@type": "Answer", "text": b}} for a, b in faqs]}]))

    # ARTICLES
    body = band('Articles', 'Wiper <span class="hl">articles</span>', 'No articles yet.')
    body += f'<section class="sec"><div class="wrap"><ul class="rg" id="articles"></ul><p class="mute">Meanwhile, the <a href="{P}wiper-size-guide/">size guide</a> and <a href="{P}faq/">FAQ</a> cover the basics.</p></div></section>'
    urls.append(page('articles/', 'Wiper Blade Articles | MOON Singapore', 'Wiper blade guides for Singapore drivers from MOON. No articles yet.',
        'Articles', body, [{"@type": "CollectionPage", "name": "Wiper blade articles", "url": BASE + "articles/"}]))

    sm = ''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>' for u in urls)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    print('\n'.join(urls))

if __name__ == '__main__':
    build()

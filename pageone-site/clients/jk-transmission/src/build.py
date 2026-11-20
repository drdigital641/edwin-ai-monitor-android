#!/usr/bin/env python3
"""J & K Transmission Specialist preview build (Page One Singapore, 20 Nov 2026).
One facts file (facts.json) + this template = every page. Run: python3 build.py  -> ../site/
Photos/logos are NOT in the repo: they were placed in preview/jk-transmission/images/ from Bridge drop 6affcc237e4c96b65652cfd0.
Go-live later: set base_url/base_path in facts.json to the live domain and "/", noindex false, rebuild, sync."""
import json, os, shutil, hashlib, html, urllib.parse, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'site')
F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
BASE, ABS = F['base_path'], F['base_url']
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)
def u(p=''): return BASE + p
def absu(p=''): return ABS + p
def sha8(p): return hashlib.sha256(open(os.path.join(HERE, p), 'rb').read()).hexdigest()[:8]
V_CSS, V_JS, V_CTA = sha8('site.css'), sha8('site.js'), sha8('p1-cta.js')

def wa(extra=''):
    msg = F['prefill'] if not extra else F['prefill'].replace('My car is: ', 'Symptom: ' + extra + '. My car is: ')
    return 'https://wa.me/%s?text=%s' % (F['whatsapp'], urllib.parse.quote(msg))
TEL = 'tel:' + F['phone_e164']

# authored line icons, one stroke weight
I = {
 'wa': '<path d="M4.5 19.5l1.2-3.6A7.8 7.8 0 1 1 8.6 18.6z"/><path d="M9.2 8.6c.2-.5.7-.5 1-.4l.8 1.6c.1.3 0 .6-.2.8l-.5.5a6 6 0 0 0 2.6 2.6l.5-.5c.2-.2.5-.3.8-.2l1.6.8c.2.3.2.8-.4 1-.9.5-2 .6-3.2-.1a8.4 8.4 0 0 1-3.2-3.2c-.6-1.2-.5-2.3.2-2.9z"/>',
 'call': '<path d="M6.6 3.5h2.6l1.4 4-1.9 1.3a10.5 10.5 0 0 0 6.5 6.5l1.3-1.9 4 1.4v2.6a2 2 0 0 1-2.2 2A16.6 16.6 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/>',
 'mail': '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.8 7l8.2 6 8.2-6"/>',
 'fb': '<path d="M14.2 21v-7.3h2.6l.4-3h-3V8.9c0-.9.3-1.5 1.5-1.5h1.6V4.7a20 20 0 0 0-2.4-.1c-2.4 0-4 1.4-4 4.1v2h-2.6v3h2.6V21"/>',
 'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
 'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 'check': '<circle cx="12" cy="12" r="8.5"/><path d="M8.3 12.2l2.5 2.5 5-5.2"/>',
 'info': '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5M12 8h.01"/>',
 'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2.8v2.6M12 18.6v2.6M21.2 12h-2.6M5.4 12H2.8M18.5 5.5l-1.8 1.8M7.3 16.7l-1.8 1.8M18.5 18.5l-1.8-1.8M7.3 7.3L5.5 5.5"/><circle cx="12" cy="12" r="6.6"/>',
 'clutch': '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="5.4"/><circle cx="12" cy="12" r="1.8"/><path d="M12 3.4v2.2M12 18.4v2.2M3.4 12h2.2M18.4 12h2.2"/>',
 'solenoid': '<rect x="7" y="3" width="10" height="13" rx="2"/><path d="M7 6.5h10M7 9.5h10M7 12.5h10M12 16v5M9.5 21h5"/>',
 'chip': '<rect x="6.5" y="6.5" width="11" height="11" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 3v3.5M15 3v3.5M9 17.5V21M15 17.5V21M3 9h3.5M3 15h3.5M17.5 9H21M17.5 15H21"/>',
 'valve': '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3 10h6v4h6v-4h6M9 5v5M15 14v5"/>',
 'ring': '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="3.2"/><path d="M12 3.4c2 2 2.6 3.8 1.6 5.6M20.6 12c-2 2-3.8 2.6-5.6 1.6M12 20.6c-2-2-2.6-3.8-1.6-5.6M3.4 12c2-2 3.8-2.6 5.6-1.6"/>',
 'chain': '<rect x="2.8" y="8.5" width="9" height="7" rx="3.5"/><rect x="12.2" y="8.5" width="9" height="7" rx="3.5"/><path d="M9 12h6"/>',
 'drop': '<path d="M12 3.2s6 6.4 6 10.6a6 6 0 0 1-12 0c0-4.2 6-10.6 6-10.6z"/><path d="M9.2 14.2a2.9 2.9 0 0 0 2.8 2.6"/>',
 'jerk': '<path d="M3 15l4-6 3 8 4-11 3 8 4-4"/>',
 'delay': '<circle cx="12" cy="13" r="7.6"/><path d="M12 9v4.2l2.6 1.6M10 2.8h4M12 2.8v2.6"/>',
 'light': '<path d="M12 3.5l9 16H3z"/><path d="M12 10v4.4M12 17.2h.01"/>',
 'dct': '<circle cx="8.5" cy="12" r="5.6"/><circle cx="15.5" cy="12" r="5.6"/><path d="M8.5 9.6v4.8M15.5 9.6v4.8"/>',
 'left': '<path d="M15 5l-7 7 7 7"/>', 'right': '<path d="M9 5l7 7-7 7"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h10"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
}
def ic(n, cls='ic'): return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, I[n])

def a_wa(ref, text='WhatsApp Jason', cls='btn-wa', extra='', label=None, attrs=''):
    al = ' aria-label="%s"' % e(label) if label else ''
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="%s"%s%s>%s<span>%s</span></a>' % (cls, e(wa(extra)), ref, al, attrs, ic('wa'), e(text))
def a_call(ref, text=None, cls='btn-call'):
    return '<a class="%s" href="%s" data-cta="call" data-ref="%s">%s<span>%s</span></a>' % (cls, TEL, ref, ic('call'), e(text or 'Call ' + F['phone_display']))
def a_map(ref, text='Open in Google Maps', cls='btn-line'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-cta="map" data-ref="%s">%s<span>%s</span></a>' % (cls, e(F['maps_url']), ref, ic('pin'), e(text))

P = F['photos']
def pic(k, sizes='(min-width:900px) 40vw, 92vw', lazy=True, cls='', cap=True, pos=None, high=False, capt=None):
    p = P[k]; ld = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if high else '')
    img = ('<picture><source type="image/webp" srcset="%s"><img src="%s" width="%d" height="%d" alt="%s" style="object-position:%s"%s></picture>'
           % (u('images/%s.webp' % p['file']), u('images/%s.jpg' % p['file']), p['w'], p['h'], e(p['alt']), pos or p['pos'], ld))
    fc = '<figcaption>%s</figcaption>' % e(capt or p['cap']) if cap else ''
    return '<figure class="%s">%s%s</figure>' % (cls, img, fc)

NAV = [('', 'Home'), ('services/', 'Services'), ('about/', 'About'), ('faq/', 'FAQ'), ('contact/', 'Contact')]

def schema_org():
    o = {"@context": "https://schema.org", "@type": "AutomotiveRepair", "@id": absu('#business'), "name": F['name'],
         "legalName": F['legal_name'], "url": absu(), "image": absu('images/workshop-hero.jpg'), "logo": absu('images/logo-transparent.png'),
         "telephone": F['phone_e164'], "email": F['email'], "slogan": F['promise'],
         "description": "Gearbox and transmission repair and overhaul specialist at REVV, Jurong West. Automatic, double-clutch (DCT) and hybrid transmissions for Hybrid, Japanese, Korean and Continental cars.",
         "identifier": {"@type": "PropertyValue", "propertyID": "UEN", "value": F['uen']},
         "address": {"@type": "PostalAddress", "streetAddress": "1 Corporation Drive, #02-03, REVV", "addressLocality": "Singapore", "postalCode": F['address']['postcode'], "addressCountry": "SG"},
         "geo": {"@type": "GeoCoordinates", "latitude": F['geo']['lat'], "longitude": F['geo']['lng']},
         "hasMap": F['maps_url'],
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": h['schema'], "opens": h['opens'], "closes": h['closes']} for h in F['hours'] if 'opens' in h],
         "areaServed": [{"@type": "Place", "name": a + ", Singapore"} for a in F['areas']],
         "sameAs": [F['facebook']],
         "contactPoint": {"@type": "ContactPoint", "telephone": F['phone_e164'], "contactType": "customer service", "name": F['whatsapp_contact'], "areaServed": "SG", "availableLanguage": "en"},
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Gearbox and transmission services",
             "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s['name']}} for s in F['services']]}}
    return o

def ld(objs): return ''.join('<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False, separators=(',', ':')) for o in objs)

def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": absu(p)} for i, (p, n) in enumerate(trail)]}

def head(path, title, desc, extra_ld=(), preload_hero=False):
    can = absu(path)
    robots = '<meta name="robots" content="noindex, nofollow">' if F['noindex'] else ''
    pre = ('<link rel="preload" as="image" type="image/webp" href="%s" fetchpriority="high">' % u('images/workshop-hero.webp')) if preload_hero else ''
    return f'''<!doctype html><html lang="en-SG"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">{robots}
<link rel="canonical" href="{can}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(F['short'])}"><meta property="og:locale" content="en_SG">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{can}">
<meta property="og:image" content="{absu('images/og.jpg')}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="J &amp; K Transmission Specialist workshop at REVV, Jurong West">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{absu('images/og.jpg')}">
<meta name="theme-color" content="#1466B0">
<link rel="icon" type="image/png" sizes="512x512" href="{u('images/favicon-512.png')}"><link rel="apple-touch-icon" href="{u('images/favicon-512.png')}">
<link rel="preload" as="font" type="font/woff2" href="{u('fonts/titillium-700.woff2')}" crossorigin>{pre}
<link rel="stylesheet" href="{u('site.css')}?v={V_CSS}">
{ld([schema_org()] + list(extra_ld))}
</head>'''

def header(cur, over=False):
    nav = ''.join('<a href="%s"%s>%s</a>' % (u(p), ' aria-current="page"' if p == cur else '', n) for p, n in NAV)
    sheet = ''.join('<a href="%s">%s</a>' % (u(p), n) for p, n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr{' over' if over else ''}"><div class="wrap">
<a class="brand" href="{u()}" aria-label="J &amp; K Transmission Specialist, home"><img src="{u('images/logo-mark.webp')}" width="42" height="42" alt=""><span><b>J &amp; K Transmission</b><small>Specialist Pte Ltd</small></span></a>
<nav class="nav" aria-label="Main">{nav}</nav>
{a_wa('whatsapp_header', 'WhatsApp', label='WhatsApp Jason')}
<button class="menu" type="button" aria-controls="sheet" aria-expanded="false" aria-label="Menu">{ic('menu')}</button>
</div></header>
<div class="sheet" id="sheet" role="dialog" aria-label="Menu"><button class="sheet-x" type="button" aria-label="Close menu">{ic('x')}</button>{sheet}{a_wa('whatsapp_menu')}</div>'''

def footer():
    hrs = ''.join('<li><span>%s: %s</span></li>' % (e(h['short']), e(h['time'])) for h in F['hours'])
    return f'''<footer class="ft"><div class="wrap"><div class="ft-grid">
<div><img class="ft-logo" src="{u('images/logo-transparent.webp')}" width="991" height="1068" alt="J &amp; K Transmission Specialist Pte Ltd logo" loading="lazy">
<p>Professional gearbox repair and overhaul at REVV, Jurong West. {e(F['promise'])}</p></div>
<div><h3>Talk to Jason</h3><ul>
<li><a href="{e(wa())}" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="whatsapp_footer">{ic('wa')}WhatsApp {e(F['phone_intl'])}</a></li>
<li><a href="{TEL}" data-cta="call" data-ref="call_footer">{ic('call')}Call {e(F['phone_display'])}</a></li>
<li><a href="mailto:{F['email']}" data-cta="email" data-ref="email_footer">{ic('mail')}{e(F['email'])}</a></li>
<li><a href="{F['facebook']}" target="_blank" rel="noopener" data-cta="facebook" data-ref="facebook_footer">{ic('fb')}Facebook</a></li></ul></div>
<div><h3>Find us</h3><ul><li><a href="{e(F['maps_url'])}" target="_blank" rel="noopener" data-cta="map" data-ref="map_footer">{ic('pin')}<span>1 Corporation Drive @ REVV, #02-03, Singapore 619775</span></a></li></ul></div>
<div><h3>Opening hours</h3><ul class="muted">{hrs}</ul></div>
</div>
<div class="ft-base"><span>&copy; {datetime.date.today().year} {e(F['legal_name'])} (UEN {F['uen']})</span><a href="{u('privacy/')}">Privacy</a><a href="{F['footer_credit_url']}" rel="noopener">{e(F['footer_credit'])}</a></div>
</div></footer>
<div class="mbar">{a_wa('whatsapp_mobile_bar')}{a_call('call_mobile_bar', 'Call')}</div>
<script src="{u('site.js')}?v={V_JS}" defer></script>
<script src="{u('p1-cta.js')}?v={V_CTA}" defer></script>
</body></html>'''

def page(path, title, desc, body, cur=None, over=False, extra_ld=(), preload_hero=False):
    return head(path, title, desc, extra_ld, preload_hero) + '<body>' + header(cur if cur is not None else path, over) + '<main id="main">' + body + '</main>' + footer()

def phead(h1, lede, trail, photo=None, btns=True):
    cr = '<nav class="crumbs" aria-label="Breadcrumb">' + ' / '.join(('<a href="%s">%s</a>' % (u(p), e(n))) if i < len(trail) - 1 else e(n) for i, (p, n) in enumerate(trail)) + '</nav>'
    b = '<div class="row-btn">%s%s</div>' % (a_wa('whatsapp_page_head'), a_call('call_page_head')) if btns else ''
    txt = f'<div>{cr}<h1>{e(h1)}</h1><p class="lede">{lede}</p>{b}</div>'
    ph = pic(photo, '(min-width:900px) 45vw, 92vw', lazy=False, cls='phead-photo') if photo else ''
    return f'<section class="phead"><div class="wrap{" phead-grid" if photo else ""}">{txt}{ph}</div></section>'

# ---------- blocks ----------
def selector():
    opts = ''.join(f'<div class="opt"><input type="radio" name="sym" id="s-{s["id"]}" value="{s["id"]}"{" checked" if i == 0 else ""}><label for="s-{s["id"]}">{ic(s["id"])}{e(s["label"])}</label></div>' for i, s in enumerate(F['symptoms']))
    dx = ''.join(f'''<div class="diag{' on' if i == 0 else ''}" id="dx-{s['id']}" aria-live="polite"><h3>{e(s['label'])}</h3><p>{e(s['text'])}</p>
<p class="tip">{ic('info')}<span>{e(s['tip'])}</span></p>{a_wa('whatsapp_symptom', 'WhatsApp Jason about this', extra=s['wa'], label='WhatsApp Jason about ' + s['wa'])}</div>''' for i, s in enumerate(F['symptoms']))
    return f'''<section class="band" id="symptoms"><div class="wrap"><div class="band-h"><h2>What's your gearbox doing?</h2><p class="lede">Pick the closest one. Jason gets your answer in the WhatsApp message.</p></div>
<div class="sel-grid" data-sel><fieldset class="sel-opts"><legend class="sr">Choose a symptom</legend>{opts}</fieldset><div>{dx}</div></div></div></section>'''

def parts_list(link=True):
    li = []
    for s in F['services']:
        inner = f'{ic(s["icon"])}<span><b>{e(s["name"])}</b><span>{e(s["line"])}</span></span>'
        li.append(f'<li><a href="{u(s["page"])}">{inner}</a></li>' if link else f'<li><div>{inner}</div></li>')
    return '<ul class="parts">' + ''.join(li) + '</ul>'

def path_steps():
    li = ''.join(f'<li>{pic(s["photo"], "(min-width:1100px) 25vw, (min-width:760px) 45vw, 92vw", pos=P[s["photo"]].get("step_pos"))}<div class="card"><h3>{e(s["name"])}</h3><p>{e(s["text"])}</p></div></li>' for s in F['steps'])
    return '<ol class="path">' + li + '</ol>'

def strip(title='Real gearbox work at REVV', lede='Every photo is from the workshop at #02-03. Drag sideways, or hold to pause.'):
    shots = ''.join(pic(k, '(min-width:900px) 300px, 74vw', cls='shot') for k in F['strip'])
    return f'''<section class="band ink" id="work"><div class="wrap"><div class="band-h"><h2>{e(title)}</h2><p class="lede">{e(lede)}</p></div></div>
<div class="strip" data-strip><div class="strip-vp"><div class="strip-tr">{shots}</div></div>
<div class="wrap strip-ctl"><button type="button" data-prev aria-label="Previous photo">{ic('left')}</button><button type="button" data-next aria-label="Next photo">{ic('right')}</button><small>8 photos from the workshop</small></div></div></section>'''

def visit_block(ref='home'):
    rows = ''.join(f'<tr><th scope="row">{e(h["days"])}</th><td>{e(h["time"])}</td></tr>' for h in F['hours'])
    return f'''<div class="visit">
<div class="vcard"><h3>{ic('pin')}Workshop</h3><address>{'<br>'.join(e(x) for x in F['address']['lines'])}</address>
<p class="muted">Revv West Enterprise Hub, Jurong West. Plus code {e(F['address']['plus_code'])}.</p>{a_map('map_' + ref)}</div>
<div class="vcard"><h3>{ic('clock')}Opening hours</h3><table class="hours">{rows}</table></div>
<div class="map"><button class="map-b" type="button" data-src="{e(F['maps_embed'])}" data-title="Map: J &amp; K Transmission at REVV, 1 Corporation Drive" data-cta="map" data-ref="map_{ref}_embed"><span class="pin">{ic('pin')}</span><b>Show the map</b><span class="muted">Loads Google Maps</span></button></div>
</div>'''

def ask(ref, h2='Tell Jason what your gearbox is doing', line='Send the car model and the symptom. A short video of the problem helps too.'):
    return f'''<section class="band white dado ask"><div class="wrap"><h2>{e(h2)}</h2><p class="lede">{e(line)}</p>
<div class="row-btn">{a_wa('whatsapp_' + ref)}{a_call('call_' + ref)}</div></div></section>'''

GEARS = '''<svg class="gears" viewBox="0 0 260 260" aria-hidden="true" fill="none" stroke="#fff" stroke-width="1.4">
<g class="g1"><circle cx="100" cy="100" r="72" stroke-dasharray="6 7"/><circle cx="100" cy="100" r="58"/><circle cx="100" cy="100" r="16"/>
<path d="M100 28v20M100 152v20M28 100h20M152 100h20M49 49l14 14M137 137l14 14M151 49l-14 14M63 137l-14 14"/></g>
<g class="g2"><circle cx="196" cy="196" r="46" stroke-dasharray="5 6"/><circle cx="196" cy="196" r="34"/><circle cx="196" cy="196" r="10"/>
<path d="M196 150v12M196 230v12M150 196h12M230 196h12"/></g></svg>'''

# ---------- pages ----------
def home():
    hero = f'''<section class="hero"><div class="hero-img"><picture><source type="image/webp" srcset="{u('images/workshop-hero.webp')}"><img src="{u('images/workshop-hero.jpg')}" width="1599" height="899" alt="{e(P['hero']['alt'])}" fetchpriority="high"></picture></div>{GEARS}
<div class="wrap hero-in"><h1>Gearbox repair &amp; overhaul in West Singapore</h1><p class="hero-line">Automatic, DCT and hybrid gearboxes. REVV, Jurong West.</p>
<div data-herocta>{a_wa('whatsapp_home_hero')}<div class="row-btn">{a_call('call_home_hero', 'Call ' + F['phone_display'], 'btn-ghost')}</div></div></div></section>'''
    promise = f'''<section class="band white promise"><div class="wrap promise-grid"><div><blockquote>{e(F['promise'])}</blockquote></div>
<div><p class="lede">Honest, targeted diagnosis first. A gearbox that needs a solenoid gets a solenoid, not a whole new unit.</p>
<p>{e(F['taglines'][1])} in the west, for Hybrid, Japanese, Korean and Continental cars.</p>
<ul class="vehicles" aria-label="Vehicles we work on">{''.join('<li>%s</li>' % v for v in F['vehicles'])}</ul></div></div></section>'''
    svc = f'''<section class="band white dado" id="services"><div class="wrap"><div class="band-h"><h2>Gearbox and transmission work</h2><p class="lede">{e(F['taglines'][0])}, from a fluid service to a full overhaul.</p></div>
{parts_list()}<div class="svc-cta row-btn"><a class="btn-line" href="{u('services/')}">See all services</a>{a_wa('whatsapp_services')}</div></div></section>'''
    proc = f'''<section class="band" id="process"><div class="wrap"><div class="band-h"><h2>How an overhaul goes</h2><p class="lede">Four steps, shown with photos from our own bench.</p></div>{path_steps()}</div></section>'''
    about = f'''<section class="band white curve-top" id="about"><div class="wrap about-grid">{pic('vezel', '(min-width:900px) 40vw, 92vw', cls='about-photo')}
<div><h2>A small, humble gearbox shop in the west</h2>
<div class="fact"><b>16</b><span>years of combined experience across the team</span></div>
<p>We are new on Facebook, but not new to this trade. The workshop is at REVV, 1 Corporation Drive in Jurong West, and gearboxes are all we do.</p>
<ul class="jobs">{''.join('<li>%s<span>%s: %s</span></li>' % (ic('check'), e(j['vehicle']), e(j['work'])) for j in F['confirmed_jobs'])}</ul>
<a class="btn-line" href="{u('about/')}">About J &amp; K</a></div></div></section>'''
    visit = f'''<section class="band" id="visit"><div class="wrap"><div class="band-h"><h2>Visit the workshop at REVV</h2></div>{visit_block('home')}</div></section>'''
    body = hero + promise + selector() + svc + proc + strip() + about + visit + ask('home_ask')
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": F['short'], "url": absu()}
    return page('', 'Gearbox Repair & Overhaul in West Singapore | J & K Transmission',
                'Gearbox repair and overhaul at REVV, Jurong West: automatic, double-clutch (DCT) and hybrid transmissions. We only repair what is needed. WhatsApp Jason on 8221 5899.',
                body, cur='', over=True, extra_ld=[web], preload_hero=True)

def services():
    gal = '<div class="ph-row">' + pic('valve_dummy' if False else 'plates', '46vw', cls='ph') + pic('housing', '46vw', cls='ph') + '</div>'
    body = phead('Gearbox and transmission services in Jurong West', 'Every service on this page is work we do at REVV #02-03. We check first, then repair only what is needed.',
                 [('', 'Home'), ('services/', 'Services')], 'bench')
    body += f'<section class="band white dado"><div class="wrap split"><div><h2>What we do</h2>{parts_list(link=False)}</div><div>{gal}</div></div></section>'
    cards = [('gearbox-overhaul/', 'Gearbox overhaul & repair', 'Automatic, DCT and hybrid gearboxes opened, inspected and repaired.', 'housing'),
             ('double-clutch-dct/', 'Double-clutch (DCT) repair', 'DCT repair and replacement, hybrid double-clutch included.', 'vezel'),
             ('tcu-repair/', 'TCU / TCM repair & programming', 'Transmission Control Unit and Module repair and programming.', 'solenoids')]
    capx = {'vezel': 'A blue Honda Vezel in the workshop, bumper off'}
    lis = ''.join(f'<li>{pic(p, "(min-width:900px) 30vw, 92vw", capt=capx.get(p))}<div class="card"><h3><a href="{u(h)}">{e(t)}</a></h3><p>{e(d)}</p></div></li>' for h, t, d, p in cards)
    body += f'<section class="band"><div class="wrap"><div class="band-h"><h2>Service pages</h2></div><ol class="path svc3" style="counter-reset:none">{lis}</ol></div></section>'
    body += selector().replace('class="band"', 'class="band white dado"', 1) + ask('services_ask')
    return page('services/', 'Gearbox & Transmission Services, Jurong West | J & K Transmission',
                'Gearbox overhaul, DCT repair, mechatronics and solenoids, TCU / TCM programming, valve body, torque converter and ATF / DCTF servicing at REVV, Jurong West.',
                body, extra_ld=[crumbs_ld([('', 'Home'), ('services/', 'Services')])])

def svc_page(path, h1, title, desc, lede, sections, photos, jobs_note=None, svc_name=None):
    trail = [('', 'Home'), ('services/', 'Services'), (path, h1)]
    body = phead(h1, lede, trail, photos[0])
    side = ''.join(pic(k, '(min-width:900px) 34vw, 92vw', cls='ph') for k in photos[1:])
    prose = ''.join(f'<h2>{e(h)}</h2>' + ''.join(('<ul>' + ''.join('<li>%s</li>' % e(x) for x in p) + '</ul>') if isinstance(p, list) else '<p>%s</p>' % p for p in ps) for h, ps in sections)
    if jobs_note: prose += f'<p class="note"><b>Past job:</b> {e(jobs_note)}</p>'
    prose += '<p class="note"><b>Price and timing:</b> these depend on the car and on what the inspection finds. WhatsApp Jason to confirm for your car.</p>'
    body += f'<section class="band white dado"><div class="wrap split"><div class="prose">{prose}</div><div style="display:grid;gap:14px">{side}</div></div></section>'
    body += f'<section class="band"><div class="wrap"><div class="band-h"><h2>How the work goes</h2></div>{path_steps()}</div></section>'
    body += ask(path.strip('/').replace('-', '_') + '_ask')
    sv = {"@context": "https://schema.org", "@type": "Service", "name": svc_name or h1, "serviceType": svc_name or h1, "provider": {"@id": absu('#business')},
          "areaServed": [{"@type": "Place", "name": a + ", Singapore"} for a in F['areas']], "url": absu(path)}
    return page(path, title, desc, body, cur='services/', extra_ld=[sv, crumbs_ld(trail)])

def overhaul():
    return svc_page('gearbox-overhaul/', 'Gearbox overhaul and repair in West Singapore', 'Gearbox Overhaul & Repair, West Singapore | J & K Transmission',
        'Automatic, double-clutch (DCT) and hybrid gearbox overhaul and repair at REVV, Jurong West. Honest diagnosis first: we only repair what is needed.',
        'Automatic, double-clutch (DCT) and hybrid transmissions. The gearbox is opened, inspected on the bench and repaired where it needs it.',
        [('What an overhaul covers here', ['When a gearbox has to come apart, it is laid out on our stainless bench so the case, gears, clutch packs, valve body and solenoids can all be checked.',
           'Parts that are worn or faulty are repaired or replaced. Parts that are fine stay in. That is what we mean by &ldquo;we only repair what is needed&rdquo;.']),
         ('Related work we do', ['Reconditioned mechatronics and solenoid replacement', 'Valve body servicing', 'Torque converter repair', 'Flywheel and pulley chain replacement', 'Wear-and-tear transmission parts', 'Transmission fluid (ATF / DCTF) and engine oil servicing']),
         ('Cars we work on', ['Hybrid, Japanese, Korean and Continental cars. For a specific model, WhatsApp Jason to confirm.'])],
        ['bench', 'housing', 'gears'], svc_name='Gearbox overhaul and repair')

def dct():
    return svc_page('double-clutch-dct/', 'Double-clutch (DCT) gearbox repair, hybrids included', 'DCT Gearbox Repair & Hybrid DCT Overhaul | J & K Transmission',
        'Double-clutch (DCT) gearbox repair and replacement at REVV, Jurong West, including hybrid double-clutch gearboxes such as the Honda Vezel Hybrid.',
        'DCT repair and replacement for double-clutch gearboxes, including hybrids. Tell Jason how it shudders, slips or hesitates.',
        [('Double-clutch work we do', ['Double-clutch (DCT) repair and replacement', 'Gearbox overhaul for double-clutch and hybrid transmissions', 'Reconditioned mechatronics and solenoid replacement', 'Transmission fluid (DCTF) servicing']),
         ('Before you message', ['Send the model and year, what the car does (shudder on take-off, jerky low-speed gear changes, a warning light) and whether it happens cold, warm or both. A short video helps.'])],
        ['vezel', 'plates'], jobs_note='a Honda Vezel Hybrid double-clutch gearbox overhaul.', svc_name='Double-clutch (DCT) gearbox repair')

def tcu():
    return svc_page('tcu-repair/', 'TCU and TCM repair and programming', 'TCU / TCM Repair & Programming, Jurong West | J & K Transmission',
        'Transmission Control Unit and Module (TCU / TCM) repair and programming at REVV, Jurong West, with mechatronics and solenoid work.',
        'Transmission Control Unit and Module repair and programming, alongside mechatronics and solenoid work.',
        [('What we do', ['Transmission Control Unit / Module (TCU / TCM) repair and programming', 'Reconditioned mechatronics and solenoid replacement', 'Transmission fluid (ATF / DCTF) servicing']),
         ('Signs to mention', ['A gearbox warning light, limp mode, or shifts that feel wrong. Send Jason a photo of the dashboard and the car model.'])],
        ['solenoids', 'jack'], jobs_note='an Audi A6 with a reconditioned Transmission Control Unit, programming and fresh transmission fluid.', svc_name='TCU / TCM repair and programming')

def about():
    trail = [('', 'Home'), ('about/', 'About')]
    body = phead('About J & K Transmission', 'Trusted transmission specialists in the west, at REVV in Jurong West.', trail, 'hero')
    jobs = ''.join('<li>%s<span>%s: %s</span></li>' % (ic('check'), e(j['vehicle']), e(j['work'])) for j in F['confirmed_jobs'])
    body += f'''<section class="band white dado"><div class="wrap split"><div class="prose">
<h2>Who we are</h2><p>{e(F['name'])} is a small gearbox repair shop in the west of Singapore. In our own words: we are new on Facebook, but definitely not new to this industry.</p>
<div class="fact"><b>16</b><span>years of combined experience across the team</span></div>
<h2>How we work</h2><p><b>{e(F['promise'])}</b> Every job starts with an honest, targeted diagnosis. We fix the parts that are worn or faulty, not the whole gearbox by default.</p>
<h2>Cars we work on</h2><p>Hybrid, Japanese, Korean and Continental cars, with automatic, double-clutch (DCT) and hybrid transmissions.</p>
<h2>Work we have done</h2><ul class="jobs">{jobs}</ul>
<h2>Where we are</h2><p>{e(F['address']['one_line'])}, in the Revv West Enterprise Hub, Jurong West. WhatsApp Jason on {e(F['phone_intl'])}.</p>
</div><div style="display:grid;gap:14px">{pic('lift', '(min-width:900px) 34vw, 92vw', cls='ph')}<img src="{u('images/logo-transparent.webp')}" width="991" height="1068" alt="J &amp; K Transmission Specialist Pte Ltd logo" loading="lazy" style="max-width:220px;margin:10px auto 0"></div></div></section>'''
    body += strip('From the bench', 'Real work from the workshop at #02-03.') + ask('about_ask')
    return page('about/', 'About J & K Transmission Specialist | Gearbox Shop at REVV',
                'J & K Transmission Specialist Pte Ltd: a gearbox and transmission repair shop at REVV, Jurong West, with a combined 16 years of team experience. We only repair what is needed.',
                body, extra_ld=[crumbs_ld(trail)])

def faq():
    trail = [('', 'Home'), ('faq/', 'FAQ')]
    body = phead('Gearbox repair questions, answered', 'If your question is not here, WhatsApp Jason. Anything about price, timing or a specific model: he will confirm for your car.', trail)
    qa = ''.join(f'<details{" open" if i == 0 else ""}><summary>{e(x["q"])}</summary><div class="a"><p>{e(x["a"])}</p></div></details>' for i, x in enumerate(F['faq']))
    body += f'<section class="band white dado"><div class="wrap"><div class="faq">{qa}</div><div class="row-btn" style="margin-top:22px">{a_wa("whatsapp_faq")}</div></div></section>'
    body += ask('faq_ask')
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x['q'], "acceptedAnswer": {"@type": "Answer", "text": x['a']}} for x in F['faq']]}
    return page('faq/', 'Gearbox Repair FAQ: Hours, Location, Services | J & K Transmission',
                'Answers about J & K Transmission at REVV, Jurong West: opening hours, who to WhatsApp, the gearbox services we do and the cars we work on.',
                body, extra_ld=[fq, crumbs_ld(trail)])

def contact():
    trail = [('', 'Home'), ('contact/', 'Contact')]
    body = phead('Contact J & K Transmission at REVV, Jurong West', 'WhatsApp Jason is the fastest way: send the car model and the symptom.', trail, btns=False)
    sel = ''.join('<option>%s</option>' % e(s['label']) for s in F['symptoms']) + '<option>Something else</option>'
    body += f'''<section class="band white dado"><div class="wrap split"><div>
<h2>Message Jason</h2><form class="waform" data-wa="{F['whatsapp']}" data-prefill="{e(F['prefill'])}" data-ref="whatsapp_contact">
<div><label for="f-car">Car make and model</label><input id="f-car" name="car" autocomplete="off" placeholder="e.g. Honda Vezel Hybrid 2016" required></div>
<div><label for="f-issue">What is it doing?</label><select id="f-issue" name="issue">{sel}</select></div>
<div><label for="f-msg">Anything else (optional)</label><textarea id="f-msg" name="msg"></textarea></div>
<div><label for="f-name">Your name (optional)</label><input id="f-name" name="name" autocomplete="name"></div>
<button class="btn-wa" type="submit" data-ref="whatsapp_contact">{ic('wa')}<span>Open WhatsApp to Jason</span></button>
<p class="muted">This opens WhatsApp with your message ready. Nothing is stored on this website. See our <a href="{u('privacy/')}">privacy page</a>.</p></form></div>
<div><h2>Other ways</h2><ul class="clist">
<li><a href="{e(wa())}" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="whatsapp_contact_list">{ic('wa')}WhatsApp {e(F['phone_intl'])} (Jason)</a></li>
<li><a href="{TEL}" data-cta="call" data-ref="call_contact">{ic('call')}Call {e(F['phone_display'])}</a></li>
<li><a href="mailto:{F['email']}" data-cta="email" data-ref="email_contact">{ic('mail')}{e(F['email'])}</a></li>
<li><a href="{F['facebook']}" target="_blank" rel="noopener" data-cta="facebook" data-ref="facebook_contact">{ic('fb')}Facebook: J &amp; K Transmission Specialist</a></li></ul></div></div></section>
<section class="band"><div class="wrap"><div class="band-h"><h2>Find the workshop</h2></div>{visit_block('contact')}</div></section>'''
    cp = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact J & K Transmission", "url": absu('contact/'), "about": {"@id": absu('#business')}}
    return page('contact/', 'Contact J & K Transmission | WhatsApp Jason, REVV Jurong West',
                'WhatsApp or call Jason on 8221 5899. J & K Transmission, 1 Corporation Drive @ REVV, #02-03, Singapore 619775. Mon to Fri 9am to 6pm, Sat 9am to 3pm.',
                body, extra_ld=[cp, crumbs_ld(trail)])

def privacy():
    trail = [('', 'Home'), ('privacy/', 'Privacy')]
    body = phead('Privacy policy', 'How this website handles the details you send us.', trail, btns=False)
    body += f'''<section class="band white dado"><div class="wrap prose">
<h2>Who we are</h2><p>{e(F['legal_name'])} (UEN {F['uen']}), {e(F['address']['one_line'])}. Contact: <a href="mailto:{F['email']}" data-cta="email" data-ref="email_privacy">{F['email']}</a>.</p>
<h2>What we collect</h2><p>This website has no account or login and does not store enquiry forms. When you tap WhatsApp, call or email, you contact us through that app, and we receive what you choose to send (such as your name, number, car details and photos).</p>
<p>To understand which buttons people use, the site counts taps on its WhatsApp, call, email, map and Facebook links. That count records the page, the button, the device type and a random visit id. It does not record your name, number or message.</p>
<h2>How we use it</h2><p>We use your details only to reply to your enquiry and to arrange and carry out work on your car. We do not sell your personal data.</p>
<h2>Your choices</h2><p>You can ask us to access, correct or delete the personal data we hold about you under Singapore's Personal Data Protection Act (PDPA). Email <a href="mailto:{F['email']}" data-cta="email" data-ref="email_privacy_rights">{F['email']}</a>.</p>
<h2>Third parties</h2><p>WhatsApp, Facebook and Google Maps are run by their own companies under their own privacy policies. The map on this site loads only when you tap it.</p>
<p class="muted">Last updated {datetime.date.today().strftime('%-d %B %Y')}.</p></div></section>'''
    return page('privacy/', 'Privacy Policy | J & K Transmission Specialist', 'How the J & K Transmission Specialist website handles enquiries sent by WhatsApp, phone and email.',
                body, extra_ld=[crumbs_ld(trail)])

def notfound():
    body = phead('Page not found', 'That page is not here. Try the home page, or WhatsApp Jason about your gearbox.', [('', 'Home'), ('404', 'Not found')])
    return page('404.html', 'Page not found | J & K Transmission', 'This page could not be found.', body, cur='-')

PAGES = {'index.html': home, 'services/index.html': services, 'gearbox-overhaul/index.html': overhaul, 'double-clutch-dct/index.html': dct,
         'tcu-repair/index.html': tcu, 'about/index.html': about, 'faq/index.html': faq, 'contact/index.html': contact, 'privacy/index.html': privacy, '404.html': notfound}

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in ('site.css', 'site.js', 'p1-cta.js'): shutil.copy(os.path.join(HERE, f), OUT)
    shutil.copytree(os.path.join(HERE, 'fonts'), os.path.join(OUT, 'fonts'))
    for p, fn in PAGES.items():
        os.makedirs(os.path.dirname(os.path.join(OUT, p)) or OUT, exist_ok=True)
        open(os.path.join(OUT, p), 'w', encoding='utf8').write(fn())
    urls = [k[:-len('index.html')] for k in PAGES if k.endswith('index.html') and k != 'privacy/index.html'] + ['privacy/']
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        '  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (absu(x), TODAY) for x in urls) + '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
    print('built', len(PAGES), 'pages ->', os.path.normpath(OUT))

if __name__ == '__main__': main()

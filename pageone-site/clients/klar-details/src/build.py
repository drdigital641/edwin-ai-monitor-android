"""Klar Details revamp preview: builds every page into site/ (python3 build.py [outdir]).

Facts come from the client's own site (research/content-inventory.md, fetched 1 Nov 2026) and are limited to what Klar
already publishes. The only price on the site is the S$88 graphene bonnet trial. Images and the video are referenced from
klardetails.com.sg for the preview; at go-live they are copied to the new host. CONFIRM items live in content/pages.py.
"""
import html
import json
import os
import re
import shutil
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'content'))
import pages as C          # noqa: E402
import articles_a, articles_b  # noqa: E402
import media as M          # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'site')
SLUG = 'klar-details'
DOMAIN = 'klardetails.com.sg'
LIVE = True
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
UPDATED = '2026-11-01'
V = '15'
INDEXNOW_KEY = '3f8b2c6d9e14a7b05c2d8e6f1a4b9c73'

# Homepage promo popup. Klar switches it off by setting PROMO['on'] = False and rebuilding;
# it also hides itself after PROMO['ends'] with no rebuild. Visitors can close it; the close
# lasts for that browser session; it shows again on a new visit.
PROMO = {
    'on': True,
    'id': 'graphene-2026',
    'ends': '2026-12-31',
    'days': 7,
    'eyebrow': 'Pre-New Year sale',
    'title': 'S$300 off KlarGRAPHENE coating',
    'text': 'Why wait until 2027 to give your car the protection it deserves? Book before 31 December 2026 and save S$300 on the Graphene Coating Package.',
    'points': ['Deeper gloss and enhanced shine', 'Excellent water repellency', 'Long-lasting paint protection', 'Easier cleaning and maintenance'],
    'fine': 'Booking and coating must both be completed by 31 December 2026 to enjoy the promotion.',
    'cta': 'WhatsApp to secure a slot',
    'topic': 'the S$300 off Graphene Coating promotion.',
    'video': 'assets/promo-clip.mp4',
    'poster': 'assets/promo-poster.jpg',
}

NAME = 'Klar Details'
LEGAL = 'Klar Details'  # CONFIRM legal entity name and UEN
FOUNDED = '2014'
TEL, TEL_SHOW = '+6566356703', '6635 6703'
WA_NUM, WA_SHOW = '6589173950', '8917 3950'
WA_MSG = 'Hi Klar Details, I found your website. I would like to book a free assessment for '
EMAIL = 'klar@motoserv.sg'
ADDR = ['48 Toh Guan Road East, #02-124', 'Enterprise Hub', 'Singapore 608586']
MAPQ = quote('Klar Details, 48 Toh Guan Road East #02-124 Enterprise Hub Singapore 608586')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
FB = 'https://www.facebook.com/klardetails'
IG = 'https://www.instagram.com/klar_details/'
TT = 'https://www.tiktok.com/@klardetails'
YT = 'https://www.youtube.com/channel/UCEwDHxg8_Si8wA5gmcRvx2A'
MOTOSERV = 'https://motoserv.sg/'
HOURS = [('Monday to Friday', '9:00am to 8:00pm'), ('Saturday', '9:00am to 2:00pm'), ('Sunday and public holidays', 'Closed')]
HOURS_LINE = 'By appointment. Mon to Fri 9am to 8pm, Sat 9am to 2pm, closed Sun and PH'

E = html.escape
SERVICES = C.SERVICES
SBY = {s['slug']: s for s in SERVICES}
ARTICLES = sorted(articles_a.ARTICLES + articles_b.ARTICLES, key=lambda a: a['date'], reverse=True)
ABY = {a['slug']: a for a in ARTICLES}
AREAS = C.AREAS
IMG = {k: v for k, v in M.IMAGES.items() if not (k.endswith('_full') and k[:-5] in M.IMAGES)}  # drop same-photo duplicates
LOCAL = {  # client's branding photos (Edwin, 1 Nov 2026), served from assets/photos/
    'every_detail_counts': ('coating-every-detail-counts.jpg', 'Klar specialist applying KlarCOAT to a Mercedes bonnet under the "because every detail counts" wall', 'HERO'),
    'klarcoat_bottle': ('klarcoat-bottle.jpg', 'KlarCOAT nanotechnology coating poured onto an applicator block', 'GALLERY'),
    'specialist_wipe': ('klar-specialist-wipe.jpg', 'Klar specialist hand-finishing a white Mercedes', 'GALLERY'),
    'steam_rear_cabin': ('steam-rear-cabin.jpg', 'Steam sanitising the rear cabin of a Range Rover', 'GALLERY'),
    'fumigation_spray': ('fumigation-spray.jpg', 'Anti-bacterial fumigation treatment inside a car', 'GALLERY'),
    'steam_leather': ('steam-leather-seat.jpg', 'Controlled-pressure steam cleaning of red leather seats', 'GALLERY'),
    'vent_brush': ('vent-brush-detail.jpg', 'Detailing brush cleaning air vents and dashboard trim', 'GALLERY'),
    'graphene_apply': ('graphene-applicator-bonnet.jpg', 'KlarGRAPHENE coating applied by hand to a grey bonnet', 'GALLERY'),
    # second batch from Klar (Edwin, 1 Nov 2026) after the client said photos looked repeated
    'bentley_wall': ('bentley-studio-wall.jpg', 'Red Bentley Continental GT convertible in the Klar studio under the "because every detail counts" wall', 'BRAND'),
    'products_table': ('klar-products-vouchers.jpg', 'Klar shampoo, KlarCOAT bottles, Klar Shield, microfibre towel and Klar vouchers on a display table', 'BRAND'),
    'rupes_polish': ('rupes-machine-polish.jpg', 'Klar specialist machine polishing a red bonnet with a RUPES dual-action polisher', 'GALLERY'),
    'klarshield_spray': ('klarshield-spray.jpg', 'Klar Shield coating protector sprayed and buffed on a grey bonnet', 'GALLERY'),
    'applicator_closeup': ('coating-applicator-closeup.jpg', 'Close-up of a gloved hand laying coating with a suede applicator block', 'GALLERY'),
    'mercedes_headlight': ('mercedes-headlight-studio.jpg', 'Mercedes-Benz E-Class headlight and grille after detailing in the Klar studio', 'GALLERY'),
    'klarcoat_range': ('klarcoat-range-graphene-advance.jpg', 'KlarCOAT Clearview, Plastic, Graphene Advance and Rims bottles in front of a blue BMW in the Klar studio', 'GALLERY'),
    'rupes_white': ('rupes-polish-white-mustang.jpg', 'Machine polishing the bonnet of a white Ford Mustang with a RUPES polisher', 'GALLERY'),
}
IMG = {k: {'url': SITE + 'assets/photos/' + f, 'alt': a, 'use': u} for k, (f, a, u) in LOCAL.items()} | IMG
# Client photos copied off the old WordPress host (assets/client/<same filename>); used whenever the copy exists.
CLIENT_DIR = os.path.join(HERE, 'assets', 'client')
for _k, _v in IMG.items():
    _b = os.path.basename(_v['url'].split('?')[0])
    if 'klardetails.com.sg' in _v['url'] and os.path.exists(os.path.join(CLIENT_DIR, _b)):
        _v['url'] = SITE + 'assets/client/' + _b
# The old WordPress host went offline on 1 Nov 2026 (domain now points at Bluehost), so on the live build any client
# photo that was not recovered is dropped and its slot falls back to one of the branding photos above.
class _Img(dict):
    def __missing__(self, key):  # a dropped client photo falls back to a branding photo instead of breaking the build
        return dict.__getitem__(self, 'graphene_apply' if 'graphene' in key else 'every_detail_counts')


if LIVE:
    IMG = _Img({k: v for k, v in IMG.items() if 'klardetails.com.sg/wp-content' not in v['url']})
SUBST = {'ceramic-coating': 'klarcoat_bottle', 'graphene-coating': 'graphene_apply', 'paint-correction': 'every_detail_counts', 'interior-detailing': 'steam_rear_cabin',
         'interior-pest-control': 'fumigation_spray', 'coating-maintenance': 'specialist_wipe', 'new-car-detailing': 'specialist_wipe', 'premium-hand-wash': 'specialist_wipe'}
# one different photo per service (client: card photo must match the service, and no repeats)
SERVICE_IMG = {'ceramic-coating': 'applicator_closeup', 'graphene-coating': 'klarcoat_range', 'paint-correction': 'rupes_polish', 'interior-detailing': 'steam_rear_cabin',
               'interior-pest-control': 'fumigation_spray', 'coating-maintenance': 'klarshield_spray', 'new-car-detailing': 'mercedes_headlight', 'premium-hand-wash': 'specialist_wipe'}
HERO_KEYS = [k for k, v in IMG.items() if v['use'] == 'HERO']
GALLERY_KEYS = [k for k, v in IMG.items() if v['use'] == 'GALLERY']
BRAND_KEYS = [k for k, v in IMG.items() if v['use'] == 'BRAND']
SERVICE_IMG = {k: (v if v in IMG else SUBST[k]) for k, v in SERVICE_IMG.items()}
# first three = the homepage's latest guides, chosen to be photos the homepage shows nowhere else
ART_POOL = ['steam_leather', 'vent_brush', 'graphene_apply', 'bentley_wall', 'rupes_white', 'products_table', 'klarcoat_bottle', 'applicator_closeup', 'rupes_polish',
            'klarshield_spray', 'mercedes_headlight', 'klarcoat_range', 'steam_rear_cabin', 'every_detail_counts', 'fumigation_spray', 'specialist_wipe']
HOME_WORK = ['bentley_wall', 'rupes_white', 'products_table']  # homepage 'our work' strip: photos not used by the hero or service cards
ART_POOL = [k for k in ART_POOL if k in IMG]
VIDEO = M.VIDEOS[0] if M.VIDEOS else None

WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')
TEL_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')
ARROW = '<svg class="arr" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
    'ceramic-coating': '<path d="M3 15c0-2 1-3 3-3.5L8 8h8l2.5 3.5c2 .5 2.5 1.5 2.5 3.5v2H3z"/><circle cx="7" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/><path d="M4 6c3-2 13-2 16 0"/>',
    'graphene-coating': '<path d="M12 3l7 4v8l-7 4-7-4V7z"/><path d="M12 3v8l7 4M12 11L5 7"/>',
    'paint-correction': '<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 8 8"/><path d="M8 12l2.5 2.5L16 9"/>',
    'interior-detailing': '<path d="M5 18v-7a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v7"/><path d="M3 18h18"/><path d="M8 8V5h8v3"/>',
    'interior-pest-control': '<path d="M12 21c4 0 6-3 6-7V9H6v5c0 4 2 7 6 7z"/><path d="M12 9V5M9 6l-2-2M15 6l2-2M6 12H3M21 12h-3"/>',
    'coating-maintenance': '<path d="M12 3c3 4 6 7 6 11a6 6 0 0 1-12 0c0-4 3-7 6-11z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
    'new-car-detailing': '<path d="M3 15c0-2 1-3 3-3.5L8 8h8l2.5 3.5c2 .5 2.5 1.5 2.5 3.5v2H3z"/><circle cx="7" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/><path d="M12 2v3M9 4l1 1M15 4l-1 1"/>',
    'premium-hand-wash': '<path d="M7 20c-2 0-3-1-3-3V9l4 2 4-2 4 2 4-2v8c0 2-1 3-3 3z"/><path d="M12 3v4M8 5l1 2M16 5l-1 2"/>',
}


def icon(k):
    return '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % ICONS.get(k, ICONS['ceramic-coating'])


def wa_url(topic='my car.'):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp for a free assessment', topic='my car.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic)), WA_SVG, E(label))


def tel_btn(cls='btn btn-ghost'):
    return '<a class="%s" href="tel:%s">%s<span>Call %s</span></a>' % (cls, TEL, TEL_SVG, TEL_SHOW)


def img(key, cls='', eager=False, sizes=None):
    i = IMG[key]
    return '<img class="%s" src="%s" alt="%s"%s%s>' % (cls, E(i['url']), E(i['alt']), '' if eager else ' loading="lazy" decoding="async"', ' fetchpriority="high"' if eager else '')


def pick(keys, n, start=0):
    keys = [k for k in keys if k in IMG]
    out = []
    for i in range(n):
        if keys:
            out.append(keys[(start + i) % len(keys)])
    return out


def faq_html(items, open_first=False):
    return '<div class="faq">%s</div>' % ''.join('<details%s><summary>%s</summary><div class="fa"><p>%s</p></div></details>' % (' open' if open_first and i == 0 else '', E(q), E(a)) for i, (q, a) in enumerate(items))


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def steps_html(items):
    return '<ol class="steps">%s</ol>' % ''.join('<li><span class="n">%d</span><div><b>%s</b><p>%s</p></div></li>' % (i + 1, E(t), E(d)) for i, (t, d) in enumerate(items))


def sections_html(secs):
    return ''.join('<section class="rt"><h2>%s</h2>%s</section>' % (E(h), b) for h, b in secs)


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero='light', cta=True, kicker='', hero_img=None, og=None):
    if not title.endswith(NAME) and not title.endswith('| Klar'):
        title = '%s | %s' % (title, NAME) if len(title) + 15 <= 60 else '%s | Klar' % title
    assert len(title) <= 60, (path, len(title), title)
    assert len(desc) <= 160, (path, len(desc), desc)
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [], hero=hero, cta=cta, kicker=kicker, hero_img=hero_img, og=og)


def business_schema():
    b = {'@type': 'AutoDetailing', '@id': SITE + '#business', 'name': NAME, 'url': SITE, 'telephone': TEL, 'email': EMAIL, 'foundingDate': FOUNDED,
         'slogan': 'Because Every Detail Counts', 'parentOrganization': {'@type': 'Organization', 'name': 'MK Group', 'url': MOTOSERV},
         'logo': SITE + 'assets/logo.png', 'image': [SITE + 'assets/og.jpg'] + [IMG[k]['url'] for k in pick(HERO_KEYS, 2)],
         'address': {'@type': 'PostalAddress', 'streetAddress': '48 Toh Guan Road East, #02-124, Enterprise Hub', 'addressLocality': 'Singapore', 'postalCode': '608586', 'addressCountry': 'SG'},
         'geo': {'@type': 'GeoCoordinates', 'latitude': 1.3346, 'longitude': 103.7462},
         'hasMap': MAP, 'areaServed': [{'@type': 'Place', 'name': a['name'] + ', Singapore'} for a in AREAS] + [{'@type': 'Country', 'name': 'Singapore'}],
         'sameAs': [FB, IG, TT, YT], 'priceRange': '$$',
         'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '09:00', 'closes': '20:00'},
                                       {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Saturday', 'opens': '09:00', 'closes': '14:00'}],
         'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['name'], 'url': SITE + 'services/%s/' % s['slug']}} for s in SERVICES] +
                       [{'@type': 'Offer', 'name': 'Graphene Coating Bonnet Trial', 'price': '88', 'priceCurrency': 'SGD', 'url': SITE + 'graphene-bonnet-trial/'}]}
    return b


def svc_card(s, i):
    pic = '<div class="card-pic">%s</div>' % img(SERVICE_IMG[s['slug']])
    return ('<a class="card svc rv" href="services/%s/" style="--d:%dms">%s<div class="card-b"><span class="line">%s</span><h3>%s</h3><p>%s</p><span class="more">More details %s</span></div></a>'
            % (s['slug'], (i % 4) * 70, pic, E(s.get('line', '')), E(s['name']), E(s['card']), ARROW))


ART_IMG = {}


# each guide's photo matches its topic (Edwin, 1 Nov 2026); unlisted guides fall back to the rotation
ART_PICK = {
    'car-water-spot-removal-singapore': 'specialist_wipe', 'remove-bird-droppings-tree-sap-car-paint': 'klarshield_spray',
    'car-polishing-vs-waxing-vs-ceramic-coating': 'klarcoat_bottle', 'car-paint-oxidation-vs-clear-coat-damage': 'rupes_polish',
    'leather-car-seat-cleaning-care-guide': 'steam_leather', 'car-wheel-cleaning-remove-brake-dust': 'klarcoat_range',
    'how-to-wash-ceramic-coated-car': 'products_table', 'car-paint-swirl-marks-causes-prevention': 'rupes_white',
    'new-car-detailing-singapore-guide': 'mercedes_headlight', 'interior-car-detailing-singapore-guide': 'steam_rear_cabin',
    'how-regular-car-detailing-protects-your-vehicles-resale-value-in-singapore': 'bentley_wall',
    '5-signs-your-car-needs-paint-correction': 'rupes_polish',
    'what-really-happens-during-a-professional-car-detailing-session-and-why-it-takes-hours': 'every_detail_counts',
    'why-professional-car-detailing-matters-in-singapores-harsh-climate': 'klarshield_spray',
    'interior-car-detailing-why-its-more-than-just-a-deep-clean': 'vent_brush',
    'why-klar-details-is-the-go-to-choice-for-tesla-and-ev-owners-in-singapore': 'applicator_closeup',
    'blog-pure-water-final-rinse': 'specialist_wipe', '5-reasons-your-car-needs-ceramic-coating-in-singapore': 'klarcoat_bottle',
    'ceramic-coating-vs-graphene-coating-which-is-better-for-singapores-humid-climate': 'klarcoat_range',
    'graphene-coating-for-car-protect-in-singapore': 'graphene_apply',
}


def art_img(a):
    """Photo for an article: never the same as the article before it in date order, and spread over the whole pool."""
    if not ART_IMG:
        used = []
        for x in ARTICLES:
            pref = [k for k in ART_POOL if k not in used[-(len(ART_POOL) - 1):]]
            ART_IMG[x['slug']] = pref[0] if pref else ART_POOL[len(used) % len(ART_POOL)]
            used.append(ART_IMG[x['slug']])
    k = ART_PICK.get(a['slug'])
    return k if k in IMG else ART_IMG[a['slug']]


def acard(a, i=0, key=None):
    pic = '' if key is False else '<div class="card-pic">%s</div>' % img(key or art_img(a))
    return ('<a class="card art rv" href="articles/%s/" style="--d:%dms">%s<div class="card-b"><time datetime="%s">%s</time><h3>%s</h3><p>%s</p><span class="more">Read %s</span></div></a>'
            % (a['slug'], (i % 3) * 70, pic, a['date'], nice_date(a['date']), E(a['title']), E(a['desc']), ARROW))


def nice_date(d):
    y, m, dd = d.split('-')
    return '%d %s %s' % (int(dd), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(m) - 1], y)


def gallery_rail(keys, eager=False):
    cards = ''.join('<figure class="shot"><a href="our-work/">%s</a><figcaption>%s</figcaption></figure>' % (img(k, eager=eager and i < 2), E(IMG[k]['alt'])) for i, k in enumerate(keys))
    return '<div class="rail" data-glide><div class="rail-track">%s</div></div>' % cards


def review_cards():
    out = []
    for r in C.REVIEWS:
        body = ('<p>“%s”</p>' % E(r['text'])) if r.get('text') else ('<p class="sum">%s</p>' % E(r['summary']))
        out.append('<blockquote class="rev rv"><div class="stars" aria-label="5 star review">★★★★★</div>%s<footer>%s</footer></blockquote>' % (body, E(r['name'])))
    return '<div class="rail" data-glide="slow"><div class="rail-track revs">%s</div></div>' % ''.join(out)


def proof_strip():
    return '<ul class="proof">%s</ul>' % ''.join('<li class="rv" style="--d:%dms"><b>%s</b><span>%s</span></li>' % (i * 80, E(v), E(l)) for i, (l, v) in enumerate(C.HOME['proof']))


def band(h='Not sure what your paint needs?', p='Send a few photos on WhatsApp. We book a free assessment at Toh Guan Road East and give you a fixed quote before any work starts.'):
    return ('<section class="sec band-sec"><div class="wrap"><div class="band rv"><div><h2>%s</h2><p>%s</p></div><div class="cta-row">%s%s</div></div></div></section>'
            % (E(h), E(p), wa_btn('WhatsApp ' + WA_SHOW), tel_btn()))


def related_services(slugs):
    items = ''.join('<a class="mini" href="services/%s/">%s<span><b>%s</b><small>%s</small></span>%s</a>' % (s, icon(s), E(SBY[s]['name']), E(SBY[s].get('line', '')), ARROW) for s in slugs if s in SBY)
    return '<section class="sec alt"><div class="wrap"><h2>Related services</h2><div class="minis">%s</div></div></section>' % items if items else ''


def related_articles(slugs, heading='Guides that help you decide', avoid=()):
    # never show a photo the page already shows, and no two cards with the same photo
    used, items = set(avoid), ''
    for i, s in enumerate(x for x in slugs if x in ABY):
        k = art_img(ABY[s])
        if k in used:
            k = next((p for p in ART_POOL if p in IMG and p not in used), k)
        used.add(k)
        items += acard(ABY[s], i, k)
    return '<section class="sec"><div class="wrap"><h2>%s</h2><div class="grid3">%s</div></div></section>' % (E(heading), items) if items else ''


def promo_html():
    P = PROMO
    if not P['on']:
        return ''
    pts = ''.join('<li>%s</li>' % E(x) for x in P['points'])
    media = ('<div class="promo-media"><video autoplay muted loop playsinline preload="metadata" poster="%s"><source src="%s" type="video/mp4"></video></div>'
             % (E(P['poster']), E(P['video']))) if P.get('video') else ''
    return ('<div class="promo" id="promo" data-id="%s" data-ends="%s" data-days="%s" hidden>'
            '<div class="promo-bg" data-promo-close></div>'
            '<div class="promo-box" role="dialog" aria-modal="true" aria-labelledby="promo-t">'
            '<button class="promo-x" type="button" data-promo-close aria-label="Close">&times;</button>'
            '%s<div class="promo-body"><p class="eyebrow">%s</p><h2 id="promo-t">%s</h2><p>%s</p><ul class="ticks">%s</ul>'
            '<p class="fine">%s</p><div class="cta-row">%s<button class="btn btn-ghost" type="button" data-promo-close>No thanks</button></div>'
            '</div></div></div>'
            % (E(P['id']), E(P['ends']), P['days'], media, E(P['eyebrow']), E(P['title']), E(P['text']), pts, E(P['fine']),
               wa_btn(P['cta'], topic=P['topic'])))


def home():
    H = C.HOME
    hero_k = 'every_detail_counts'
    hero = f'''<section class="hero">
<div class="hero-media">{img(hero_k, eager=True)}</div>
<div class="wrap hero-in">
<p class="kicker rv">{E(H['hero_kicker'])}</p>
<h1 class="rv" style="--d:80ms">{E(H['hero_h1'])}</h1>
<p class="lede rv" style="--d:160ms">{E(H['hero_sub'])}</p>
<div class="cta-row rv" style="--d:240ms">{wa_btn('WhatsApp for a free assessment')}<a class="btn btn-light" href="graphene-bonnet-trial/">Try graphene on your bonnet, S$88 {ARROW}</a></div>
</div>
<div class="wrap">{proof_strip()}</div>
</section>'''
    svcs = ''.join(svc_card(s, i) for i, s in enumerate(SERVICES))
    why = ''.join('<li class="rv" style="--d:%dms"><span class="n">%02d</span><h3>%s</h3><p>%s</p></li>' % (i * 70, i + 1, E(t), E(d)) for i, (t, d) in enumerate(H['why']))
    vid = ('<section class="sec dark"><div class="wrap split"><div><p class="eyebrow">Inside the studio</p><h2>Watch a Klar premium hand wash</h2><p>Enclosed, dust-free bays, a pure-water final rinse and a hand finish. '
           'This is the same care every Signature treatment gets for at least six man-hours.</p>%s</div><div class="video portrait rv"><video controls preload="metadata" playsinline poster="assets/photos/klarcoat-bottle.jpg"><source src="assets/premium-wash.mp4" type="video/mp4"></video></div></div></section>'
           % wa_btn('Book a free assessment'))
    areas = ''.join('<a class="chip" href="areas/%s/">%s</a>' % (a['slug'], E(a['name'])) for a in AREAS)
    arts = ''.join(acard(a, i, False) for i, a in enumerate(ARTICLES[:3]))  # text cards: every photo is already on the homepage
    body = f'''
<section class="sec"><div class="wrap">
<div class="sec-h rv"><p class="eyebrow">What we do</p><h2>One page per service, so you know exactly what you are booking</h2></div>
<div class="grid4">{svcs}</div>
</div></section>
<section class="sec alt"><div class="wrap">
<div class="sec-h rv"><p class="eyebrow">Why owners choose Klar</p><h2>Particular about details? So are we.</h2></div>
<ol class="why">{why}</ol>
</div></section>
<section class="sec work-sec"><div class="wrap sec-h rv"><p class="eyebrow">Our work</p><h2>Recent cars through the bays</h2></div>{gallery_rail([k for k in HOME_WORK if k in IMG])}<div class="wrap center"><a class="btn btn-ghost" href="our-work/">See more of our work {ARROW}</a></div></section>
{vid}
<section class="sec"><div class="wrap sec-h rv"><p class="eyebrow">Reviews</p><h2>In our customers' words</h2></div>{review_cards()}<div class="wrap center"><a class="btn btn-ghost" href="reviews/">All reviews {ARROW}</a></div></section>
<section class="sec alt"><div class="wrap split">
<div class="rv"><p class="eyebrow">West Singapore</p><h2>A short drive from Jurong East, Bukit Batok and Clementi</h2><p>Klar Details sits at Enterprise Hub on Toh Guan Road East, minutes from IMM and Jurong East MRT, with covered access and enclosed bays. Owners across the west book a free assessment and leave the car with us for the day.</p><div class="chips">{areas}</div></div>
<div class="map rv"><iframe title="Map to Klar Details, 48 Toh Guan Road East" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
<section class="sec"><div class="wrap sec-h rv"><p class="eyebrow">Guides</p><h2>Decide with facts, not sales talk</h2></div><div class="wrap grid3">{arts}</div><div class="wrap center"><a class="btn btn-ghost" href="articles/">All guides {ARROW}</a></div></section>
<section class="sec alt"><div class="wrap narrow"><div class="sec-h rv"><p class="eyebrow">Questions</p><h2>Before you book</h2></div>{faq_html(C.HOME_FAQS)}<p class="center"><a href="faq/">More questions answered {ARROW}</a></p></div></section>
'''
    page('', 'Car Detailing Singapore, Toh Guan | Klar Details', 'Premium car detailing centre at Toh Guan Road East, Jurong East: ceramic and graphene coating, paint correction, interior detailing. Since 2014. Free assessment',
         H['hero_h1'], hero + body, hero=None, schema=[faq_schema(C.HOME_FAQS)], cta=True)


def services_index():
    svcs = ''.join(svc_card(s, i) for i, s in enumerate(SERVICES))
    body = ('<section class="sec"><div class="wrap"><div class="grid4">%s</div></div></section>' % svcs
            + '<section class="sec alt"><div class="wrap narrow rt"><h2>How a visit works</h2>%s</div></section>' % steps_html([
                ('WhatsApp a few photos', 'Tell us the car, how it is used and what bothers you about the paint or cabin.'),
                ('Free assessment at Toh Guan Road East', 'We inspect the paint under lights, measure what correction it needs and agree the scope.'),
                ('Fixed quote before work starts', 'You know the price and the hours before we touch the car.'),
                ('The work, in an enclosed bay', 'Preparation, correction, coating and infrared curing, or the interior programme you chose.'),
                ('Handover and aftercare', 'We walk you round the car and explain how to wash and maintain it.')]))
    page('services/', 'Car Detailing Services in Singapore', 'Every Klar Details service on its own page: ceramic and graphene coating, paint correction, interior detailing, pest control, maintenance, new car, hand wash.',
         'Car detailing services', body, crumbs=[('services/', 'Services')], lede='Each service has its own page with what is included, the process, how long it takes and the questions owners ask most.', kicker='Services')


def service_page(s, i=0):
    hk = [SERVICE_IMG[s['slug']]]
    inc = '<ul class="inc">%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in s['includes'])
    body = f'''
<section class="sec"><div class="wrap split">
<div class="rt">{s['intro']}<div class="cta-row">{wa_btn('WhatsApp for a free assessment', s['name'].lower() + '.')}{tel_btn()}</div></div>
<div class="pic rv">{img(hk[0]) if hk else ''}</div>
</div></section>
{('<section class="sec dark"><div class="wrap split"><div><p class="eyebrow">Watch</p><h2>A Klar premium hand wash, start to finish</h2><p>Filmed in the Klar bays at Toh Guan Road East.</p></div><div class="video portrait rv"><video controls preload="metadata" playsinline poster="assets/photos/klarshield-spray.jpg"><source src="assets/premium-wash.mp4" type="video/mp4"></video></div></div></section>') if s['slug'] == 'premium-hand-wash' else ''}
<section class="sec alt"><div class="wrap"><h2>What {E(s['name'].lower())} at Klar includes</h2>{inc}{extra_pics(s['slug'])}</div></section>
<section class="sec"><div class="wrap narrow"><h2>How it works</h2>{steps_html(s['steps'])}</div></section>
<section class="sec alt"><div class="wrap narrow">{sections_html(s['sections'])}</div></section>
<section class="sec"><div class="wrap narrow"><div class="price rv"><h2>Price</h2><p>{E(s['price'])}</p><div class="cta-row">{wa_btn('Ask for a quote', s['name'].lower() + '.')}<a class="btn btn-ghost" href="prices/">How we price {ARROW}</a></div></div></div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Questions about {E(s['name'].lower())}</h2>{faq_html(s['faqs'])}</div></section>
{related_services(s.get('related', []))}
{related_articles(s.get('articles', []), avoid=hk + EXTRA.get(s['slug'], []) + (['klarshield_spray'] if s['slug'] == 'premium-hand-wash' else []))}
'''
    schema = [{'@type': 'Service', 'name': s['name'], 'serviceType': s['name'], 'provider': {'@id': SITE + '#business'}, 'areaServed': {'@type': 'Country', 'name': 'Singapore'},
               'url': SITE + 'services/%s/' % s['slug'], 'description': s['desc']}, faq_schema(s['faqs'])]
    page('services/%s/' % s['slug'], s['title'], s['desc'], s['h1'], body, crumbs=[('services/', 'Services'), ('services/%s/' % s['slug'], s['name'])], kicker=s.get('line', ''), schema=schema, og=IMG[hk[0]]['url'])


EXTRA = {'interior-detailing': ['steam_leather', 'vent_brush'], 'interior-pest-control': ['steam_leather', 'vent_brush'],
         'ceramic-coating': ['klarcoat_bottle', 'bentley_wall'], 'premium-hand-wash': ['bentley_wall', 'mercedes_headlight'],
         'paint-correction': ['rupes_white', 'every_detail_counts'], 'graphene-coating': ['applicator_closeup', 'klarcoat_bottle'],
         'coating-maintenance': ['products_table', 'specialist_wipe'], 'new-car-detailing': ['klarshield_spray', 'applicator_closeup']}


def extra_pics(slug):
    ks = [k for k in EXTRA.get(slug, []) if k in IMG]
    return ('<div class="pics pics-sm">%s</div>' % ''.join('<figure class="shot"><a href="our-work/">%s</a><figcaption>%s</figcaption></figure>' % (img(k), E(IMG[k]['alt'])) for k in ks)) if ks else ''


def trial_page():
    g = SBY['graphene-coating']
    inc = ['Premium hand wash', 'Surface preparation of the bonnet', 'KlarGRAPHENE coating applied to the bonnet', 'Water-beading demonstration', 'Gloss enhancement treatment']
    faqs = [('What does the S$88 graphene bonnet trial include?', 'A premium hand wash, surface preparation, graphene coating applied to the bonnet, a water-beading demonstration and a gloss enhancement treatment. You see the finish on your own paint before deciding on a full treatment.'),
            ('How long does the bonnet trial take?', 'Allow part of a day at Toh Guan Road East. We confirm the slot and the time needed when you book on WhatsApp, because preparation depends on the condition of the bonnet.'),
            ('Can the trial be credited towards a full graphene coating?', 'Ask us when you book. We confirm the current terms in writing on WhatsApp before your visit so there is no surprise at handover.'),
            ('Is the trial suitable for a brand-new car?', 'Yes. We inspect the paint first; a new car may need little or no correction before coating. The trial is a low-cost way to compare graphene against ceramic on your own car.')]
    body = f'''
<section class="sec"><div class="wrap split">
<div class="rt"><p>The S$88 Graphene Coating Bonnet Trial is the only way in Singapore we know of to test a graphene coating on your own car before committing to a full treatment. We wash and prepare the bonnet, apply KlarGRAPHENE, show you the water beading and finish with a gloss enhancement treatment.</p>
<p>It suits new car owners deciding between ceramic and graphene, enthusiasts who want to see the gloss on their own colour, and anyone who prefers to try before they buy.</p>
<div class="cta-row">{wa_btn('Book the S$88 trial', 'the S$88 graphene bonnet trial.')}{tel_btn()}</div></div>
<div class="pic rv">{img('graphene_trial_photo' if 'graphene_trial_photo' in IMG else 'graphene_coating')}</div>
</div></section>
<section class="sec alt"><div class="wrap"><h2>What the trial includes</h2><ul class="inc">{''.join('<li>%s</li>' % E(x) for x in inc)}</ul></div></section>
<section class="sec"><div class="wrap narrow"><div class="price rv"><h2>S$88, fixed</h2><p>The price is fixed before you arrive. If the bonnet needs more preparation than the trial covers, we tell you first and you decide.</p>{wa_btn('Book the S$88 trial', 'the S$88 graphene bonnet trial.')}</div></div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Questions about the trial</h2>{faq_html(faqs)}</div></section>
{related_services(['graphene-coating', 'ceramic-coating', 'coating-maintenance'])}
{related_articles(g.get('articles', []), avoid=['graphene_trial_photo' if 'graphene_trial_photo' in IMG else 'graphene_coating', 'graphene_apply'])}
'''
    schema = [{'@type': 'Offer', 'name': 'Graphene Coating Bonnet Trial', 'price': '88', 'priceCurrency': 'SGD', 'availability': 'https://schema.org/InStock', 'url': SITE + 'graphene-bonnet-trial/',
               'offeredBy': {'@id': SITE + '#business'}, 'itemOffered': {'@type': 'Service', 'name': 'Graphene coating on the bonnet', 'provider': {'@id': SITE + '#business'}}}, faq_schema(faqs)]
    page('graphene-bonnet-trial/', 'S$88 Graphene Coating Bonnet Trial', 'Try KlarGRAPHENE on your own bonnet for S$88: hand wash, preparation, graphene coating, water-beading demo and gloss treatment at Toh Guan Road East, Singapore.',
         'Try graphene coating on your bonnet for S$88', body, crumbs=[('graphene-bonnet-trial/', 'S$88 graphene trial')], kicker='Offer', lede='See the beading and gloss on your own paint before you decide on a full KlarGRAPHENE treatment.', schema=schema)


def area_page(a, i=0):
    near = ''.join('<li>%s</li>' % E(n) for n in a.get('nearby', []))
    body = f'''
<section class="sec"><div class="wrap split">
<div class="rt">{a['intro']}<div class="cta-row">{wa_btn('WhatsApp for a free assessment')}{tel_btn()}</div></div>
<div class="map rv"><iframe title="Map to Klar Details, 48 Toh Guan Road East" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
<section class="sec alt"><div class="wrap narrow">{sections_html(a['sections'])}{('<h3>Landmarks nearby</h3><ul class="chips-ul">%s</ul>' % near) if near else ''}</div></section>
<section class="sec"><div class="wrap narrow"><h2>Questions from {E(a['name'])} owners</h2>{faq_html(a['faqs'])}</div></section>
{related_services(['ceramic-coating', 'graphene-coating', 'interior-detailing', 'paint-correction'])}
'''
    page('areas/%s/' % a['slug'], a['title'], a['desc'], a['h1'], body, crumbs=[('areas/', 'Areas'), ('areas/%s/' % a['slug'], a['name'])], kicker='West Singapore', schema=[faq_schema(a['faqs'])])


def areas_index():
    h = C.AREA_HUB
    cards = ''.join('<a class="card rv" href="areas/%s/" style="--d:%dms"><div class="card-b"><h3>%s</h3><p>%s</p><span class="more">More details %s</span></div></a>' % (a['slug'], i * 70, E(a['name']), E(a['desc']), ARROW) for i, a in enumerate(AREAS))
    body = f'''
<section class="sec"><div class="wrap narrow rt">{h['intro']}</div></section>
<section class="sec alt"><div class="wrap"><div class="grid4">{cards}</div></div></section>
<section class="sec"><div class="wrap narrow">{sections_html(h['sections'])}</div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Questions</h2>{faq_html(h['faqs'])}</div></section>
'''
    page('areas/', h['title'], h['desc'], h['h1'], body, crumbs=[('areas/', 'Areas')], kicker='West Singapore', schema=[faq_schema(h['faqs'])])


def articles_index():
    cards = ''.join(acard(a, i) for i, a in enumerate(ARTICLES))
    page('articles/', 'Car Care Guides for Singapore Owners', 'Plain guides on ceramic and graphene coating, paint correction, interior care and washing a coated car in Singapore, written by the Klar Details team.',
         'Car care guides', '<section class="sec"><div class="wrap"><div class="grid3">%s</div></div></section>' % cards, crumbs=[('articles/', 'Guides')], kicker='Guides',
         lede='Written to help you decide, not to sell. Every guide links to the service it relates to.')


def article_page(a, i=0):
    owner = SBY.get(a['owner'])
    hk = [art_img(a)]
    rel = [s for s in a.get('related', []) if s in ABY]
    body = f'''
<article class="sec"><div class="wrap narrow">
<p class="meta">Published {nice_date(a['date'])}{' · Updated ' + nice_date(UPDATED) if UPDATED > a['date'] else ''} · Klar Details team</p>
<div class="rt lead">{a['intro']}</div>
<div class="pic wide rv">{img(hk[0]) if hk else ''}</div>
<div class="rt">{sections_html(a['sections'])}</div>
{('<h2>Questions</h2>' + faq_html(a['faqs'])) if a.get('faqs') else ''}
{('<div class="owner rv"><p class="eyebrow">Related service</p><a class="mini" href="services/%s/">%s<span><b>%s</b><small>%s</small></span>%s</a></div>' % (owner['slug'], icon(owner['slug']), E(owner['name']), E(owner.get('line', '')), ARROW)) if owner else ''}
</div></article>
{related_articles(rel, 'Keep reading', avoid=hk)}
'''
    schema = [{'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': a['date'], 'dateModified': UPDATED, 'inLanguage': 'en-SG',
               'author': {'@type': 'Organization', 'name': NAME, 'url': SITE}, 'publisher': {'@id': SITE + '#business'}, 'mainEntityOfPage': SITE + 'articles/%s/' % a['slug'],
               'image': IMG[hk[0]]['url'] if hk else SITE + 'assets/og.jpg'}]
    if a.get('faqs'):
        schema.append(faq_schema(a['faqs']))
    page('articles/%s/' % a['slug'], a['title'], a['desc'], a['h1'], body, crumbs=[('articles/', 'Guides'), ('articles/%s/' % a['slug'], a['title'])], kicker='Guide', schema=schema, cta=True)


def our_work():
    shots = ''.join('<figure class="shot rv" style="--d:%dms">%s<figcaption>%s</figcaption></figure>' % ((i % 3) * 60, img(k), E(IMG[k]['alt'])) for i, k in enumerate(GALLERY_KEYS + HERO_KEYS))
    body = ('<section class="sec"><div class="wrap"><div class="masonry">%s</div></div></section>' % shots
            + '<section class="sec alt"><div class="wrap narrow rt"><h2>What you are looking at</h2><p>Coating and correction work from the Klar bays at Toh Guan Road East: EVs such as Tesla, BYD and Polestar, '
              'performance cars and daily drivers. Photos are taken under the studio lights at handover. Every car is inspected and quoted before work starts.</p></div></section>')
    page('our-work/', 'Our Work: Coating and Detailing Photos', 'Photos of ceramic and graphene coating, paint correction and interior detailing jobs from the Klar Details studio at Toh Guan Road East, Singapore.',
         'Our work', body, crumbs=[('our-work/', 'Our work')], kicker='Gallery', lede='Real cars from the bays, photographed at handover.')


def reviews_page():
    cards = ''.join('<blockquote class="rev rv" style="--d:%dms"><div class="stars" aria-label="5 star review">★★★★★</div>%s<footer>%s</footer></blockquote>'
                    % ((i % 3) * 60, ('<p>“%s”</p>' % E(r['text'])) if r.get('text') else ('<p class="sum">%s</p>' % E(r['summary'])), E(r['name'])) for i, r in enumerate(C.REVIEWS))
    body = ('<section class="sec"><div class="wrap"><div class="grid3">%s</div></div></section>' % cards
            + '<section class="sec alt"><div class="wrap narrow rt"><h2>How we handle reviews</h2><p>These are customer reviews shown in their own words. We do not edit them, pay for them or mark them up for search engines. '
              'Had your car with us? A review of your real experience helps the next owner decide.</p><p><a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">Find us on Google Maps %s</a></p></div></section>' % (MAP, ARROW))
    page('reviews/', 'Customer Reviews', 'What Klar Details customers say about the coating, workmanship and service at Toh Guan Road East, in their own words.',
         'Customer reviews', body, crumbs=[('reviews/', 'Reviews')], kicker='Reviews')


def about():
    A = C.ABOUT
    facts = '<table class="facts"><tbody>%s</tbody></table>' % ''.join('<tr><th>%s</th><td>%s</td></tr>' % (E(l), E(v)) for l, v in A['facts'])
    bk = pick(BRAND_KEYS, 1) or pick(HERO_KEYS, 1)
    body = f'''
<section class="sec"><div class="wrap split"><div class="rt">{A['intro']}</div><div class="pic rv">{img(bk[0])}</div></div></section>
<section class="sec alt"><div class="wrap narrow">{sections_html(A['sections'])}</div></section>
<section class="sec"><div class="wrap narrow"><h2>Klar Details at a glance</h2>{facts}</div></section>
'''
    page('about/', A['title'], A['desc'], A['h1'], body, crumbs=[('about/', 'About')], kicker='About')


def prices():
    P = C.PRICES
    body = f'''
<section class="sec"><div class="wrap narrow rt">{P['intro']}<div class="cta-row">{wa_btn('Ask for a quote')}<a class="btn btn-ghost" href="graphene-bonnet-trial/">S$88 graphene trial {ARROW}</a></div></div></section>
<section class="sec alt"><div class="wrap narrow">{sections_html(P['sections'])}</div></section>
<section class="sec"><div class="wrap narrow"><h2>Questions about pricing</h2>{faq_html(P['faqs'])}</div></section>
'''
    page('prices/', P['title'], P['desc'], P['h1'], body, crumbs=[('prices/', 'Prices')], kicker='Prices', schema=[faq_schema(P['faqs'])])


def faq_page():
    body = '<section class="sec"><div class="wrap narrow">%s</div></section>' % faq_html(C.FAQ_PAGE, open_first=True)
    page('faq/', 'Car Detailing and Coating FAQs', 'Answers to the questions Singapore owners ask about ceramic and graphene coating, paint correction, interior detailing and booking at Klar Details.',
         'Frequently asked questions', body, crumbs=[('faq/', 'FAQ')], kicker='FAQ', schema=[faq_schema(C.FAQ_PAGE)])


def contact():
    K = C.CONTACT
    hours = ''.join('<tr><th>%s</th><td>%s</td></tr>' % (E(d), E(h)) for d, h in HOURS)
    body = f'''
<section class="sec"><div class="wrap split">
<div class="rt">{K['intro']}
<div class="cta-row">{wa_btn('WhatsApp ' + WA_SHOW)}{tel_btn()}</div>
<h2>Visit</h2><p>{'<br>'.join(E(x) for x in ADDR)}<br><a href="{MAP}" target="_blank" rel="noopener">Open in Google Maps</a></p>
<h2>Hours</h2><p>By appointment only.</p><table class="facts"><tbody>{hours}</tbody></table>
<h2>Email</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>Follow</h2><p><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{TT}" target="_blank" rel="noopener">TikTok</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></p>
</div>
<div class="map tall rv"><iframe title="Map to Klar Details, 48 Toh Guan Road East" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>
'''
    page('contact/', K['title'], K['desc'], K['h1'], body, crumbs=[('contact/', 'Contact')], kicker='Contact', cta=False)


def privacy():
    P = C.PRIVACY
    page('privacy/', P['title'], 'How Klar Details uses the details you send by WhatsApp, phone or the contact page.', P['h1'],
         '<section class="sec"><div class="wrap narrow">%s</div></section>' % sections_html(P['sections']), crumbs=[('privacy/', 'Privacy')], cta=False)


def products_page():
    faqs = [('Can I buy Klar products for home use?', 'A retail range built on the KlarCOAT, KlarGRAPHENE and KlarSHIELD lines is being prepared. Register your interest on WhatsApp and we will message you when the first products and prices are confirmed, with the same aftercare guidance we give at handover.'),
            ('Will the products be the same ones used in the studio?', 'The retail range is drawn from the same in-house lines our detailers use. Professional coatings still need preparation, correction and curing in the studio, so retail items focus on washing, maintenance and protecting a finish between visits.'),
            ('Where will Klar products be sold?', 'At the Klar studio and through channels we confirm closer to launch. Resellers and partner workshops can ask about stocking Klar products through the franchise and partnership page.')]
    body = f'''
<section class="sec"><div class="wrap split">
<div class="rt"><p>Klar Details is preparing a retail range built on the same in-house lines our detailers use every day: KlarCOAT, KlarGRAPHENE and KlarSHIELD. The first products focus on keeping a coated car clean and protected between studio visits.</p>
<p>Product names, contents and prices are published here once confirmed. Register your interest on WhatsApp and you hear first.</p>
<div class="cta-row">{wa_btn('Register interest in Klar products', 'Klar products.')}</div></div>
<div class="pic rv">{img(pick(BRAND_KEYS, 1, 1)[0] if BRAND_KEYS else pick(HERO_KEYS, 1)[0])}</div>
</div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Questions about Klar products</h2>{faq_html(faqs)}</div></section>
{related_services(['coating-maintenance', 'premium-hand-wash', 'graphene-coating'])}
'''
    page('products/', 'Klar Products: Car Care Range', 'Klar Details is preparing a retail car care range built on its in-house KlarCOAT, KlarGRAPHENE and KlarSHIELD lines. Register your interest on WhatsApp.',
         'Klar products', body, crumbs=[('products/', 'Products')], kicker='Coming soon', lede='The lines used in our studio, prepared for home use. Details and prices published once confirmed.', schema=[faq_schema(faqs)])


def franchise_page():
    faqs = [('What does a Klar Details franchise include?', 'The Klar name and brand standards, the in-house KlarCOAT, KlarGRAPHENE, KlarINTERIOR and KlarMAINTENANCE lines, training in our preparation, application and curing process, and the backing of MK Group. Full terms are shared in conversation after a first meeting.'),
            ('Who is a Klar franchise for?', 'Workshop owners, detailers and investors in Singapore and the region who want to run a premium detailing studio to a documented standard rather than build a brand from nothing. Experience with cars helps; our training covers the Klar process.'),
            ('How do I start a conversation?', 'Send a WhatsApp message with your name, location and background, or email us. We reply with the next step, usually a visit to the Klar studio so you can see the process before any numbers are discussed.')]
    body = f'''
<section class="sec"><div class="wrap split">
<div class="rt"><p>Since 2014 Klar Details has built a detailing process around preparation, in-house coatings and controlled curing, and since November 2024 it has had MK Group behind it. We are now opening that process to partners who want to run a Klar studio of their own.</p>
<p>A Klar franchise is a premium detailing studio operated to Klar standards, with our product lines, training and brand. Tell us about yourself and we arrange a visit to the studio first.</p>
<div class="cta-row">{wa_btn('Ask about a Klar franchise', 'a Klar franchise.')}<a class="btn btn-ghost" href="mailto:{EMAIL}">Email {EMAIL}</a></div></div>
<div class="pic rv">{img(pick(BRAND_KEYS, 1, 0)[0] if BRAND_KEYS else pick(HERO_KEYS, 1)[0])}</div>
</div></section>
<section class="sec alt"><div class="wrap narrow"><h2>What partners get</h2><ul class="inc"><li>The Klar brand and studio standards</li><li>KlarCOAT, KlarGRAPHENE, KlarINTERIOR and KlarMAINTENANCE lines</li><li>Training in preparation, application and infrared curing</li><li>MK Group backing and sister brands for servicing and repairs</li><li>Marketing and website support</li><li>A studio visit before any commitment</li></ul></div></section>
<section class="sec"><div class="wrap narrow"><h2>Questions about franchising</h2>{faq_html(faqs)}</div></section>
'''
    page('franchise/', 'Klar Details Franchise and Partnerships', 'Run a premium car detailing studio to Klar standards with in-house coating lines, training and MK Group backing. Start with a visit to the Klar studio.',
         'Klar franchise and partnerships', body, crumbs=[('franchise/', 'Franchise')], kicker='Partner with Klar', lede='A Klar studio of your own, run to the standards owners already trust at Toh Guan Road East.', schema=[faq_schema(faqs)], og=None)


NAV = [('services/', 'Services'), ('graphene-bonnet-trial/', 'S$88 trial'), ('our-work/', 'Our work'), ('prices/', 'Prices'), ('articles/', 'Guides'), ('about/', 'About'), ('contact/', 'Contact')]


def shell(path, p, robots_meta=''):
    promo = promo_html() if path == '' else ''
    pre = '../' * path.count('/')
    url = SITE + path

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path == h else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' <i>/</i> '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    og = p['og'] or SITE + 'assets/og.jpg'
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'], 'inLanguage': 'en-SG',
                                 'dateModified': UPDATED, 'primaryImageOfPage': og, 'about': {'@id': SITE + '#business'}, 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = ('<section class="phero"><div class="wrap">%s%s<h1>%s</h1>%s</div></section>' % (
            crumbs_html, '<p class="kicker">%s</p>' % E(p['kicker']) if p['kicker'] else '', E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else ''))
    title = E(p['title'])
    body = fix(p['body'] + (band() if p['cta'] else ''))
    brand = ('<a class="brand" href="%s" aria-label="%s, home page"><img src="%sassets/icon-96.png" alt="" width="40" height="40"><img class="wm" src="%sassets/wordmark.png" alt="Klar Details" width="125" height="40"></a>' % (pre or './', NAME, pre, pre))
    svc_links = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, s['slug'], E(s['name'])) for s in SERVICES)
    area_links = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (pre, a['slug'], E(a['name'])) for a in AREAS)
    og_type = 'article' if path.startswith('articles/') and path != 'articles/' else 'website'
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
{robots_meta or '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#0b0d10">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, premium car detailing centre at Toh Guan Road East, Singapore">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}assets/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap">
<link rel="stylesheet" href="{pre}kd.css?v={V}">
<script src="{pre}kd.js?v={V}" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('WhatsApp', cls='btn btn-wa hdr-cta')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span><i>Menu</i></button>
</div></header>
<main id="main">
{head_hero}
{body}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}<p>Premium car detailing centre at Enterprise Hub, Toh Guan Road East, Singapore. KlarCOAT ceramic, KlarGRAPHENE, paint correction, interior detailing and coating maintenance since 2014.</p><p class="mk"><b>Complete Automotive Care.</b> Need car servicing, repairs, aircon, tyres, batteries or vehicle inspection? <a href="{MOTOSERV}" target="_blank" rel="noopener">Explore Motoserv.sg →</a></p></div>
<div><h3>Services</h3><ul>{svc_links}<li><a href="{pre}graphene-bonnet-trial/">S$88 graphene bonnet trial</a></li></ul></div>
<div><h3>Areas</h3><ul><li><a href="{pre}areas/">West Singapore</a></li>{area_links}</ul><h3>Explore</h3><ul><li><a href="{pre}our-work/">Our work</a></li><li><a href="{pre}reviews/">Reviews</a></li><li><a href="{pre}prices/">Prices</a></li><li><a href="{pre}articles/">Guides</a></li><li><a href="{pre}faq/">FAQ</a></li><li><a href="{pre}about/">About</a></li><li><a href="{pre}products/">Klar products</a></li><li><a href="{pre}franchise/">Franchise</a></li><li><a href="{pre}privacy/">Privacy</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="tel:{TEL}">{TEL_SHOW}</a></li>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{'<br>'.join(E(x) for x in ADDR)}</li>
<li>{HOURS_LINE}</li>
<li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{TT}" target="_blank" rel="noopener">TikTok</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>© 2026 {NAME} · Because Every Detail Counts</span><span>Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
{promo}<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp Klar Details on {WA_SHOW}">{WA_SVG}<span>WhatsApp</span></a><a class="dock-c" href="tel:{TEL}">{TEL_SVG}<span>Call</span></a></div>
</body>
</html>
'''


def write(rel, data, binary=False):
    fp = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'wb' if binary else 'w', **({} if binary else {'encoding': 'utf-8'})) as f:
        f.write(data)


def main():
    home(); services_index()
    for i, s in enumerate(SERVICES):
        service_page(s, i)
    trial_page(); areas_index()
    for i, a in enumerate(AREAS):
        area_page(a, i)
    articles_index()
    for i, a in enumerate(ARTICLES):
        article_page(a, i)
    our_work(); reviews_page(); about(); prices(); faq_page(); contact(); privacy(); products_page(); franchise_page()
    for path, p in PAGES.items():
        write(path + 'index.html', shell(path, p))
    nf = dict(title='Page not found | Klar Details', desc='This page does not exist.', h1='Page not found',
              body='<section class="sec"><div class="wrap"><p>That page is not here. Try our <a href="%sservices/">services</a> or <a href="%sarticles/">guides</a>.</p></div></section>' % (SITE, SITE),
              crumbs=None, lede='', schema=[], hero='light', cta=True, kicker='', hero_img=None, og=None)
    t = shell('', nf, '<meta name="robots" content="noindex">')
    t = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), SITE, '' if m.group(2) == './' else m.group(2)), t)
    t = t.replace('<link rel="canonical" href="%s">\n' % SITE, '')
    write('404.html', t)
    sm = ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, path, UPDATED) for path in PAGES)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % sm)
    bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
    write('robots.txt', 'User-agent: *\nAllow: /\n\n' + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'Sitemap: %ssitemap.xml\n' % SITE)
    write(INDEXNOW_KEY + '.txt', INDEXNOW_KEY)
    write('site.webmanifest', json.dumps({'name': NAME, 'short_name': 'Klar', 'start_url': './', 'display': 'standalone', 'background_color': '#0b0d10', 'theme_color': '#0b0d10',
                                          'icons': [{'src': 'assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}))
    llms = ['# %s' % NAME, '',
            '> Klar Details is a premium car detailing centre at 48 Toh Guan Road East, #02-124, Enterprise Hub, Singapore 608586 (Jurong East, West Singapore), operating since 2014 and part of MK Group since 1 November 2024. '
            'Services: KlarCOAT Signature Ceramic coating, KlarGRAPHENE graphene coating, paint correction, KlarINTERIOR interior detailing with NEA-approved anti-bacterial fumigation, KlarMAINTENANCE half-yearly coating maintenance, new car and EV protection, premium hand wash. '
            'Over 2,500 cars serviced. Free professional car assessment; fixed quote before work starts. Only published price: Graphene Coating Bonnet Trial S$88.', '',
            '- Address: 48 Toh Guan Road East, #02-124, Enterprise Hub, Singapore 608586', '- Phone: +65 6635 6703', '- WhatsApp: +65 8917 3950', '- Email: %s' % EMAIL,
            '- Hours: %s' % HOURS_LINE, '- Facebook: %s' % FB, '- Instagram: %s' % IG, '- TikTok: %s' % TT, '- YouTube: %s' % YT, '- Map: %s' % MAP, '- Sister brand for servicing: %s' % MOTOSERV, '', '## Pages', '']
    llms += ['- [%s](%s%s): %s' % (p['h1'], SITE, path, p['desc']) for path, p in PAGES.items()]
    write('llms.txt', '\n'.join(llms) + '\n')
    src = os.path.join(HERE, 'assets')
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(OUT, 'assets'), dirs_exist_ok=True)
    for f in ('favicon.ico', 'kd.css', 'kd.js'):
        shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
    # .htaccess for the client's own domain (preview inherits the shared preview/.htaccess; the bridge cannot write this file)
    old = {'about-us/': 'about/', 'blog/': 'articles/', 'service-klarcoat/': 'services/ceramic-coating/', 'service-klarinterior/': 'services/interior-detailing/',
           'service-klarmaintenance/': 'services/coating-maintenance/', 'service/klarcoat-2/': 'services/ceramic-coating/', 'service/klarinterior-2/': 'services/interior-detailing/',
           'service/klarmaintenance/': 'services/coating-maintenance/', 'prevent-car-water-spots-singapore/': 'articles/car-water-spot-removal-singapore/',
           'protect-car-paint-bird-droppings-tree-sap/': 'articles/remove-bird-droppings-tree-sap-car-paint/', 'top-5-automotive-workshops-in-singapore/': 'about/',
           'shopcar/': '', 'checkout/': '', 'search-page/': '', 'category/uncategorized/': 'articles/', 'author/klardetailuser/': 'articles/', 'sitemap_index.xml': 'sitemap.xml'}
    for a in ARTICLES:
        old[a['slug'] + '/'] = 'articles/%s/' % a['slug']
    ht = ['# Klar Details: upload as .htaccess in the domain root at go-live (Edwin, via cPanel).', 'Options -Indexes', 'DirectoryIndex index.html', 'ErrorDocument 404 /404.html',
          'RewriteEngine On', 'RewriteCond %{HTTPS} off [OR]', 'RewriteCond %{HTTP_HOST} ^www\\. [NC]', 'RewriteRule ^(.*)$ https://%s/$1 [L,R=301]' % DOMAIN, '']
    ht += ['RewriteRule ^%s$ /%s [L,R=301]' % (re.escape(k.rstrip('/')) + ('/?' if k.endswith('/') else ''), v) for k, v in old.items()]
    ht += ['', '<IfModule mod_headers.c>', '<FilesMatch "\\.(html)$">', 'Header set Cache-Control "max-age=3600, public"', '</FilesMatch>',
           '<FilesMatch "\\.(css|js|svg|png|ico|webp|jpg|jpeg|mp4)$">', 'Header set Cache-Control "max-age=604800, public"', '</FilesMatch>', '</IfModule>']
    with open(os.path.join(HERE, 'htaccess.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(ht) + '\n')
    if LIVE:  # tracked in the repo; the bridge cannot write it, so sync with exclude ['.htaccess'] and Edwin uploads it via cPanel
        with open(os.path.join(OUT, '.htaccess'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(ht) + '\n')
    print('pages', len(PAGES))


if __name__ == '__main__':
    main()

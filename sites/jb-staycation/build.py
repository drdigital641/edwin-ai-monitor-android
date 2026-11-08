"""JBStaycation demo preview: builds every page into site/ (python3 build.py).

Facts (client site jbstaycation.com, read 8 Nov 2026) and official travel sources are listed in README.md.
Unknowns are NOT invented; see CONFIRM below. To go live change BASE (one constant) and rebuild.
"""
import html
import json
import os
import re
import shutil
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

BASE = 'https://pageonesingapore.com/preview/jb-staycation/'   # single constant: change to the live domain at go-live
TODAY = '2026-11-08'
SITE_ID = 'jb-staycation'
NAME = 'JBStaycation'
TAGLINE = 'A quieter escape, just across the causeway.'
WA_NUM, WA_SHOW = '6590062198', '+65 9006 2198'
WA_BASE = 'https://wa.me/' + WA_NUM

CONFIRM = [
    'Legal/business name of the host (kept off the site).',
    'Prima bedrooms: client site says 3 in the header and 5 in text/gallery. Page says "multiple bedrooms" only.',
    'Prima "Minimum 2": assumed nights; page says "message us to confirm".',
    'Prima 900 sq ft (as stated by client) looks small for 20 guests; left off the page.',
    'Prima check-in/out times and house rules (none on client site).',
    'Deposit, cancellation and payment terms (client T&C is an unfilled template; no /terms/ page built).',
    'SGD equivalents: not shown until Edwin agrees.',
    'Is Lumina Glasshouse still offered? (only in one review; not listed).',
    'Google Business Profile, Airbnb, social links, email (none known; no sameAs).',
    'Brand colours/fonts: could not be read (only theme-color #f7f8f9 visible); palette is an estimate of a warm, calm look.',
    'Photo ratios and og:image size (1200 px wide, 1.91:1) not verifiable from the sandbox; self-host photos before go-live.',
    'Host drive times (Tuas 10 min / Woodlands 15 min / KSL etc.) are as stated by the host, not independently timed.',
    'Does the photo set include people/cars (privacy) and may we use them? (client own photos assumed).',
]

# ---------------------------------------------------------------- images (swap to self-hosted files later)
J = 'https://jbstaycation.com/_astro/'
IMAGES = {
    'home-hero': (J + 'img-1806-afec0c7d_4DWkh.webp', 'Exterior of a JBStaycation holiday house in Johor Bahru'),
    'prima': [
        (J + 'garden-1-f484d67f_Z1Vvjp8.webp', 'Prima house with balcony and garden, Taman Nusantara Prima'),
        (J + 'bedroom1-dc4fc514_S8DzO.webp', 'Bedroom at Prima'),
        (J + 'living-room-1-916f5d01_YKpjb.webp', 'Living room with sofa set at Prima'),
        (J + 'kitchen-1-6f876b58_2kiCvj.webp', 'Fully equipped kitchen at Prima'),
        (J + 'dining-room-1-4fb79ea0_c6d35.webp', 'Dining room with a large table at Prima'),
        (J + 'games-room-1-a94462c4_1mEGCf.webp', 'Games room at Prima'),
        (J + 'family-room-1-61218aa1_Z1KTTGy.webp', 'Family room at Prima'),
        (J + 'rooftop-terrace-769478b2_ahgCE.webp', 'Rooftop terrace at Prima'),
        (J + 'bedroom-2-3fe1fa07_2ptpN.webp', 'Second bedroom at Prima'),
        (J + 'study-corner-1-e2d6f7ba_1ibMXl.webp', 'Study corner with desk at Prima'),
    ],
    'landak': [
        (J + '01-hero-1-88ecc683_Z2ml1eU.webp', 'Bright open-plan living room at Landak Kawan Fun House'),
        (J + '02-highlights-1-41de69c7_2vHlKC.webp', 'Private games courtyard with pool table and seating'),
        (J + '03-highlights-2-4cf4369d_Z1SLno4.webp', 'Open-plan living room with foosball table'),
        (J + '04-highlights-3-c67373ad_Z1hrL0W.webp', 'Dining and living area for group gatherings'),
        (J + '05-highlights-4-4eab123b_Z1iR150.webp', 'Kitchen with breakfast counter and appliances'),
        (J + '06-highlights-5-a864f872_Z1XFtGS.webp', 'Bedroom 1 with king bed'),
        (J + '07-highlights-6-486ef2d0_18WW5R.webp', 'Bedroom 2 with two queen beds'),
        (J + '08-highlights-7-f5a62d22_Z1evoH1.webp', 'Bedroom 3 with two queen beds'),
        (J + '10-highlights-9-fe22e9ed_2p2OMA.webp', 'Front view of the private double-storey home'),
        (J + '11-highlights-10-10628baa_Z1qPf3X.webp', 'Sheltered car porch with on-site parking'),
    ],
}
IMG_W, IMG_H = 1200, 800   # assumed 3:2 box; CSS object-fit: cover keeps any real ratio tidy

# ---------------------------------------------------------------- houses
HOUSES = {
    'prima': {
        'slug': 'prima-taman-nusantara-prima', 'name': 'Prima', 'full': 'Prima, Taman Nusantara Prima',
        'short': 'Prima at Taman Nusantara Prima',
        'street': '19 Jalan Prima 3/1, Taman Nusantara Prima', 'locality': 'Iskandar Puteri', 'region': 'Johor', 'postal': '79200',
        'addr': '19 Jalan Prima 3/1, Taman Nusantara Prima, Iskandar Puteri, Johor 79200, Malaysia',
        'guests': 20, 'price': 500, 'minstay': 'Minimum stay listed as 2 (message us to confirm nights)',
        'tag': 'Big group house with karaoke, mahjong and a BBQ pit',
        'card': 'A fully furnished house for up to 20 guests, with karaoke, a mahjong table, BBQ pit, games room and rooftop terrace.',
        'stats': [('Guests', 'Up to 20'), ('Bedrooms', 'Multiple bedrooms'), ('Bathrooms', '3'), ('Rate', 'RM 500 per night')],
        'intro': ['Prima is a fully furnished house in Taman Nusantara Prima, Iskandar Puteri, made for big groups: up to 20 guests, multiple bedrooms and 3 bathrooms.',
                  'There is room to spread out. Spaces include a games room, a family room, a study corner, a rooftop terrace and a balcony, with a full kitchen for cooking together.',
                  'The host states it is about 10 minutes to Tuas and about 15 minutes to Woodlands, which makes it a natural pick if you cross by the Second Link.'],
        'amen': ['Fast Wi-Fi', 'Air conditioning', 'Full kitchen', 'Free parking', 'Smart TV', 'Washer and dryer', 'Karaoke set',
                 'Mahjong table', 'BBQ pit', 'Workspace / desk', 'Playground', 'Games room', 'Study corner', 'Family room',
                 'Rooftop terrace', 'Balcony', 'Dressing room'],
        'rules': ['Check-in and check-out times, smoking, pets and event rules are not stated on our listing yet. Message us on WhatsApp and we will confirm them before you book.'],
        'near': [('Tuas', 'about 10 minutes'), ('Woodlands', 'about 15 minutes')],
        'near_note': 'Drive times are as stated by the host.',
        'faq': [
            ('How many people can Prima sleep?', 'Prima is listed for up to 20 guests. Message us your group size and dates and we will confirm the setup.'),
            ('Is there a minimum stay at Prima?', 'The listing shows a minimum of 2. Message us on WhatsApp to confirm the minimum number of nights for your dates.'),
            ('Can we sing karaoke or play mahjong?', 'Prima has a karaoke set and a mahjong table. Please ask us about quiet hours and house rules when you enquire.'),
            ('Is there parking?', 'Yes, free parking is listed for Prima.'),
        ],
        'msg': 'Hi JBStaycation, I would like to check dates and rate for Prima (Taman Nusantara Prima).',
        'key': 'prima',
    },
    'landak': {
        'slug': 'landak-kawan-fun-house-taman-abad', 'name': 'Landak Kawan Fun House', 'full': 'Landak Kawan Fun House, Taman Abad',
        'short': 'Landak Kawan Fun House',
        'street': 'Jalan Landak Kawan 2, Taman Abad', 'locality': 'Johor Bahru', 'region': 'Johor', 'postal': '80250',
        'addr': 'Jalan Landak Kawan 2, Taman Abad, Johor Bahru, Johor 80250, Malaysia',
        'guests': 10, 'price': 500, 'minstay': 'Minimum 1 night',
        'tag': 'Games house a 5-minute walk from KSL City Mall',
        'card': 'A private double-storey house for up to 10 guests with a pool table, foosball and darts, a 5-minute walk from KSL City Mall.',
        'stats': [('Guests', 'Up to 10'), ('Bedrooms', '3'), ('Bathrooms', '3'), ('Rate', 'RM 500 per night')],
        'intro': ['Landak Kawan Fun House is a private double-storey home in Taman Abad, Johor Bahru, for up to 10 guests. It has 3 bedrooms, 3 bathrooms and 1 king bed plus 4 queen beds (bedrooms 2 and 3 each have two queens).',
                  'The fun is built in: an 8-foot pool table in the games courtyard, a foosball table, two dartboards and a 55-inch smart TV with an arcade console.',
                  'It is about a 5-minute walk to KSL City Mall, and the host states 10 minutes by car to JB City Square, KOMTAR JBCC and CIQ.'],
        'amen': ['8-ft pool table', 'Foosball table', 'Two dartboards', '55-inch smart TV with arcade console', '100 Mbps Wi-Fi',
                 'Washer and detergent', 'Hair dryer', 'Iron', 'Workspace', 'Free parking', 'Playground', 'Self check-in'],
        'rules': ['Check-in: self check-in after 3:00 pm.', 'Check-out: before 11:00 am.', 'No smoking.', 'No pets.',
                  'No BBQ or charcoal grilling.', 'Events need prior approval and may cost extra.'],
        'near': [('KSL City Mall', '5-minute walk'), ('Yu Ee hawker centre', '3 minutes'), ('JB City Square, KOMTAR JBCC, CIQ', '10 minutes'),
                 ('R&F Mall', '12 minutes'), ('Mid Valley Southkey', '12 minutes'), ('AEON Tebrau, IKEA, Toppen', '18 minutes')],
        'near_note': 'Times other than the walk are drive times as stated by the host.',
        'faq': [
            ('What time is check-in and check-out at Landak Kawan Fun House?', 'Self check-in is after 3:00 pm and check-out is before 11:00 am.'),
            ('What is the minimum stay?', 'The minimum stay is 1 night.'),
            ('Are pets, smoking or BBQ allowed?', 'No. Smoking, pets, BBQ and charcoal grilling are not allowed. Events need prior approval and may cost extra.'),
            ('What is there to do inside the house?', 'There is an 8-foot pool table, a foosball table, two dartboards and a 55-inch smart TV with an arcade console.'),
        ],
        'msg': 'Hi JBStaycation, I would like to check dates and rate for Landak Kawan Fun House (Taman Abad).',
        'key': 'landak',
    },
}
ORDER = ['prima', 'landak']

REVIEW = ('Very nice place very clean', 'P., Singapore')

# ---------------------------------------------------------------- sources for travel facts (official only)
SRC = {
    'lta_rts': ('LTA: Johor Bahru-Singapore RTS Link (project page)', 'https://www.lta.gov.sg/content/ltagov/en/upcoming_projects/rail_expansion/JB-Singapore_RTS_link.html', 'page last updated 5 May 2025; checked 8 Nov 2026'),
    'lta_feb': ('LTA news release, 2 Oct 2026: grantors informed RTS Link service targeted for February 2027', 'https://www.lta.gov.sg/content/ltagov/en/newsroom/2026/10/news-releases/grantors-informed-rts-link-service-targeted-feb-2027.html', 'released 2 Oct 2026; checked 8 Nov 2026'),
    'ica_qr': ('ICA: QR code for immigration clearance at land checkpoints (Woodlands and Tuas)', 'https://www.ica.gov.sg/enter-transit-depart/at-our-checkpoints/use-of-qr-code-for-immigration-clearance-at-woodlands-and-tuas-checkpoints', 'page last updated 27 Oct 2026; checked 8 Nov 2026'),
    'ica_traffic': ('ICA: Driving in and out of Singapore (traffic updates)', 'https://www.ica.gov.sg/enter-depart/checkpoints/trafficupdates', 'listed by search; checked 8 Nov 2026'),
}

# ---------------------------------------------------------------- articles
ARTICLES = [
    {
        'slug': 'big-group-staycation-jb-house-for-10-20-people',
        'title': 'Big group staycation in JB: a house for 10-20 people',
        'desc': 'Planning a JB staycation for 10 to 20 people? Two private houses compared: sleeping, games, karaoke, rates and route from Singapore.',
        'h1': 'Big group staycation in JB: a house for 10-20 people',
        'answer': 'For 10 people, Landak Kawan Fun House in Taman Abad sleeps up to 10 with 3 bedrooms and 5 beds. For up to 20, Prima in Taman Nusantara Prima is listed for up to 20 guests. Both are RM 500 per night, booked on WhatsApp.',
        'house': 'prima', 'img': 'prima',
        'sections': [
            ('Why a whole house suits a big group', ['One house keeps everyone together: one kitchen, one living area, one place to park. You split the nightly rate across the group, and nobody is booking six separate hotel rooms.',
                'Both JBStaycation houses are private homes in Johor Bahru, not shared buildings.']),
            ('Up to 10 guests: Landak Kawan Fun House', ['<a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad has 3 bedrooms, 3 bathrooms, 1 king bed and 4 queen beds (bedrooms 2 and 3 each have two queens). The rate is RM 500 per night with a 1-night minimum.',
                'For entertainment it has an 8-foot pool table, a foosball table, two dartboards and a 55-inch smart TV with an arcade console. Wi-Fi is 100 Mbps. House rules: no smoking, pets or BBQ, and events need prior approval.']),
            ('Up to 20 guests: Prima', ['<a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Taman Nusantara Prima, Iskandar Puteri, is listed for up to 20 guests with multiple bedrooms and 3 bathrooms. The rate is RM 500 per night; the listing shows a minimum of 2, so confirm the nights with us.',
                'It has a karaoke set, a mahjong table, a BBQ pit, a games room, a family room, a study corner, a rooftop terrace and a balcony, plus a full kitchen and free parking.']),
            ('Getting your group across', ['Many groups drive. The host states Prima is about 10 minutes from Tuas and 15 from Woodlands, and Landak is about 10 minutes from CIQ. See our <a href="{R}getting-there/">guide to getting to Johor Bahru</a> for the Causeway, Second Link and RTS Link options.']),
            ('How to ask about dates', ['Message us on WhatsApp with your group size and dates. Prices are in RM. We will reply with availability and the rate for your dates.']),
        ],
    },
    {
        'slug': 'staying-near-ksl-city-mall-what-is-within-5-15-minutes',
        'title': 'Staying near KSL City Mall: what is within 5-15 minutes',
        'desc': 'What is near KSL City Mall in Johor Bahru? Walking and driving times from Landak Kawan Fun House, as stated by the host.',
        'h1': 'Staying near KSL City Mall: what is within 5-15 minutes',
        'answer': 'Landak Kawan Fun House in Taman Abad is about a 5-minute walk to KSL City Mall and 3 minutes to Yu Ee hawker centre. The host states 10 minutes by car to JB City Square, KOMTAR JBCC and CIQ, and 12 minutes to R&F Mall and Mid Valley Southkey.',
        'house': 'landak', 'img': 'landak',
        'sections': [
            ('Walking distance', ['<a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> is about a 5-minute walk from KSL City Mall, handy for meals, shopping and anything you forgot to pack.',
                'The Yu Ee hawker centre is about 3 minutes away, as stated by the host.']),
            ('Within 10-12 minutes by car', ['JB City Square, KOMTAR JBCC and CIQ are about 10 minutes away. R&F Mall and Mid Valley Southkey are about 12 minutes away.']),
            ('Within 18 minutes by car', ['AEON Tebrau, IKEA and Toppen are about 18 minutes away.']),
            ('About these times', ['All times other than the 5-minute walk are drive times stated by the host. Traffic, especially around the checkpoints on weekends and holidays, can change them.']),
            ('Why this suits a weekend away', ['You can walk to a mall, then spend the evening at home with the pool table, foosball, darts and arcade TV. Wi-Fi is 100 Mbps. The house sleeps up to 10, with check-in after 3:00 pm and check-out before 11:00 am.',
                'Planning the trip? Read <a href="{R}articles/causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay/">which way to cross</a>, or message us on WhatsApp for dates.']),
        ],
    },
    {
        'slug': 'causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay',
        'title': 'Causeway, Second Link or RTS: which way to JB for a weekend stay',
        'ttl': 'Causeway, Second Link or RTS: Which Way to JB?',
        'desc': 'Woodlands Causeway, Tuas Second Link or the RTS Link? What official sources say, and which JBStaycation house suits each route.',
        'h1': 'Causeway, Second Link or RTS: which way to JB for a weekend stay',
        'answer': 'By road, Singapore has two land checkpoints: Woodlands and Tuas. The RTS Link train between Woodlands North and Bukit Chagar is now expected to start passenger service in February 2027, subject to safety certification (LTA, 2 Oct 2026). Prima is closer to Tuas; Landak to JB CIQ.',
        'house': 'landak', 'img': 'landak',
        'sections': [
            ('By road: Woodlands or Tuas', ['ICA operates the land checkpoints at Woodlands and Tuas and lists traffic updates on its <a href="' + SRC['ica_traffic'][1] + '" rel="noopener">driving in and out of Singapore page</a>. Check it before you leave, especially on long weekends.',
                'You must bring your passport. ICA says so on its <a href="' + SRC['ica_qr'][1] + '" rel="noopener">QR code clearance page</a> (updated 27 Oct 2026), even when you use QR clearance.']),
            ('By train: the RTS Link', ['The RTS Link connects Woodlands North in Singapore with Bukit Chagar in Johor Bahru. LTA describes a train journey of about five minutes between the stations, with Customs, Immigration and Quarantine facilities co-located so you clear both countries before boarding (<a href="' + SRC['lta_rts'][1] + '" rel="noopener">LTA project page</a>).',
                'On 2 October 2026 LTA published that passenger service is now expected to start in February 2027, subject to independent safety certification and final approvals (<a href="' + SRC['lta_feb'][1] + '" rel="noopener">LTA news release</a>). Until it opens, plan on road or other existing routes.']),
            ('Which house for which route', ['<a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Iskandar Puteri is stated by the host as about 10 minutes from Tuas and about 15 minutes from Woodlands, so it suits groups driving in via the Second Link.',
                '<a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad is stated as about 10 minutes from CIQ and a 5-minute walk from KSL City Mall, so it suits groups arriving at the Johor Bahru city side.']),
            ('Not yet confirmed', ['We have not listed RTS fares or the door-to-door time from Bukit Chagar to either house, because we have no official figure for them. Ask us on WhatsApp if you need help planning.']),
        ],
    },
]

# ---------------------------------------------------------------- helpers
def e(s):
    return html.escape(str(s), quote=True)


def wa_url(msg):
    return WA_BASE + '?text=' + quote(msg)


def wa_btn(label, msg, ref, cls='btn btn-wa'):
    return ('<a class="%s" href="%s" data-cta="whatsapp" data-cta-label="%s" rel="noopener">'
            '<svg class="ico" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.1 1.2z"/></svg>%s</a>'
            % (cls, e(wa_url(msg)), e(ref), e(label)))


def img(key_or_pair, cls='', eager=False, sizes='(min-width:900px) 560px, 100vw'):
    v = IMAGES[key_or_pair] if isinstance(key_or_pair, str) else key_or_pair
    url, alt = v[0] if isinstance(v, list) else v
    return ('<img src="%s" alt="%s" width="%d" height="%d"%s%s decoding="async"%s>'
            % (e(url), e(alt), IMG_W, IMG_H, '' if eager else ' loading="lazy"', ' fetchpriority="high"' if eager else '',
               (' class="%s"' % cls) if cls else ''))


def carousel(h):
    imgs = IMAGES[h['key']]
    slides = ''.join('<li class="slide">%s</li>' % img(p, eager=(i == 0)) for i, p in enumerate(imgs))
    return ('<section class="carousel" aria-roledescription="carousel" aria-label="Photos of %s" data-carousel>'
            '<ul class="track" tabindex="0">%s</ul>'
            '<button class="cbtn prev" type="button" aria-label="Previous photo">&#8249;</button>'
            '<button class="cbtn next" type="button" aria-label="Next photo">&#8250;</button></section>' % (e(h['name']), slides))


def faq_block(items, h2='Frequently asked questions'):
    body = ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in items)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}
    return '<section class="rv"><h2>%s</h2>%s</section>' % (e(h2), body), ld


def crumbs_ld(crumbs):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + p} for i, (n, p) in enumerate(crumbs)]}


def crumbs_html(crumbs):
    out = []
    for i, (n, p) in enumerate(crumbs):
        out.append(e(n) if i == len(crumbs) - 1 else '<a href="{R}%s">%s</a>' % (p, e(n)))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' &rsaquo; '.join(out)


def addr_ld(h):
    return {'@type': 'PostalAddress', 'streetAddress': h['street'], 'addressLocality': h['locality'],
            'addressRegion': h['region'], 'postalCode': h['postal'], 'addressCountry': 'MY'}


def org_ld():
    return {'@context': 'https://schema.org', '@type': 'LodgingBusiness', '@id': BASE + '#org', 'name': NAME,
            'url': BASE, 'telephone': WA_SHOW, 'slogan': TAGLINE, 'image': IMAGES['home-hero'][0],
            'logo': BASE + 'icon-512.png', 'priceRange': 'RM 500 per night', 'currenciesAccepted': 'MYR',
            'areaServed': 'Johor Bahru, Malaysia',
            'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'VacationRental', 'name': HOUSES[k]['full'], 'url': BASE + 'stays/%s/' % HOUSES[k]['slug']}} for k in ORDER]}


def house_ld(h):
    ld = {'@context': 'https://schema.org', '@type': 'VacationRental', '@id': BASE + 'stays/%s/#rental' % h['slug'],
          'name': h['full'], 'url': BASE + 'stays/%s/' % h['slug'], 'description': h['card'],
          'image': [u for u, _ in IMAGES[h['key']][:6]], 'telephone': WA_SHOW,
          'address': addr_ld(h), 'priceRange': 'RM %d per night' % h['price'],
          'occupancy': {'@type': 'QuantitativeValue', 'maxValue': h['guests']},
          'numberOfBathroomsTotal': 3,
          'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': a, 'value': True} for a in h['amen']],
          'containedInPlace': {'@type': 'LodgingBusiness', '@id': BASE + '#org', 'name': NAME},
          'makesOffer': {'@type': 'Offer', 'price': h['price'], 'priceCurrency': 'MYR', 'url': wa_url(h['msg']),
                         'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': h['price'], 'priceCurrency': 'MYR', 'unitText': 'night'}}}
    if h['key'] == 'landak':
        ld['numberOfBedrooms'] = 3
        ld['petsAllowed'] = False
        ld['checkinTime'] = '15:00'
        ld['checkoutTime'] = '11:00'
        ld['smokingAllowed'] = False
    return ld


# ---------------------------------------------------------------- shared shell (ONE header/footer for every page)
NAV = [('Stays', 'stays/'), ('Prices', 'prices/'), ('Getting there', 'getting-there/'), ('FAQ', 'faq/'), ('Articles', 'articles/'), ('About', 'about/')]


def header_html():
    nav = ''.join('<a href="{R}%s">%s</a>' % (p, n) for n, p in NAV)
    return ('<header class="hdr"><div class="wrap hdr-in"><a class="brand" href="{R}"><img src="{R}icon.svg" alt="" width="32" height="32"><span>JB<b>Staycation</b></span></a>'
            '<nav class="nav" aria-label="Main">%s</nav>'
            '%s</div></header>' % (nav, wa_btn('WhatsApp', 'Hi JBStaycation, I would like to ask about a stay in Johor Bahru.', 'header', 'btn btn-wa btn-sm')))


def footer_html():
    adds = ''.join('<li><b>%s</b><br>%s</li>' % (e(HOUSES[k]['name']), e(HOUSES[k]['addr'])) for k in ORDER)
    links = ''.join('<a href="{R}%s">%s</a>' % (p, n) for n, p in NAV[:5] + [('About', 'about/'), ('Contact', 'contact/'), ('Privacy', 'privacy/')])
    return ('<footer class="ftr"><div class="wrap ftr-in"><div><p class="brand-f">JB<b>Staycation</b></p><p>%s</p>'
            '<p>%s</p></div><div><p class="fh">Our houses</p><ul class="adds">%s</ul></div>'
            '<div><p class="fh">Explore</p><div class="flinks">%s</div></div></div>'
            '<div class="wrap fsmall"><span>Prices in RM. Bookings by WhatsApp only.</span> <a href="https://pageonesingapore.com/" rel="noopener">Website by Page One Singapore</a></div></footer>'
            % (e(TAGLINE), wa_btn('WhatsApp %s' % WA_SHOW, 'Hi JBStaycation, I would like to ask about a stay in Johor Bahru.', 'footer'), adds, links))


CTA_JS = r"""/* Page One CTA tap counter (copied approach from aivs.js v3, site id jb-staycation). Counts taps on WhatsApp/call/email links. ?p1test=1 = test mode. Does not run on pageonesingapore.com previews or localhost. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last={},S=null;
var T=(function(){var q=/[?&]p1test=1(&|$)/.test(location.search);try{if(q)sessionStorage.setItem('p1test','1');return sessionStorage.getItem('p1test')==='1'}catch(e){return q}})();
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=rid();sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function vid(){try{var k='p1cta_vid',v=localStorage.getItem(k);if(!v){v=rid();localStorage.setItem(k,v)}return v}catch(e){return''}}
function visit(){try{var s=JSON.parse(sessionStorage.getItem('p1cta_v')||'null');if(!s){var q=new URLSearchParams(location.search),r=document.referrer||'',rh='';try{rh=new URL(r).hostname.replace(/^www\./,'')}catch(e){}
s={t:Date.now(),l:location.pathname.slice(0,200),r:rh===h?'':r.slice(0,300),us:(q.get('utm_source')||'').slice(0,100),um:(q.get('utm_medium')||'').slice(0,100),uc:(q.get('utm_campaign')||'').slice(0,100),
ad:q.get('gclid')||q.get('gbraid')||q.get('wbraid')?'google':q.get('fbclid')?'facebook':q.get('msclkid')?'microsoft':q.get('ttclid')?'tiktok':'',n:0}}
s.n++;sessionStorage.setItem('p1cta_v',JSON.stringify(s));return s}catch(e){return null}}
S=visit();
function send(a,type){type=type||'whatsapp';var n=Date.now();if(last[type]&&n-last[type]<1500)return;last[type]=n;var s=S||{},tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var lab=a?String(a.getAttribute('data-cta-label')||a.getAttribute('aria-label')||a.textContent||'').replace(/\s+/g,' ').trim().slice(0,60):'';
try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'jb-staycation',cta_type:type,session_id:sid(),visitor_id:vid(),page_path:location.pathname.slice(0,200),
device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:s.r!=null?s.r:(document.referrer||'').slice(0,300),page_referrer:(document.referrer||'').slice(0,300),
landing_path:s.l||'',utm_source:s.us||'',utm_medium:s.um||'',utm_campaign:s.uc||'',ad_click:s.ad||'',pages_viewed:s.n||1,secs_on_site:s.t?Math.round((n-s.t)/1000):0,
cta_label:lab,tz:tz,lang:(navigator.language||'').slice(0,16),screen:(screen.width||0)+'x'+(screen.height||0),test:T?1:undefined})}).catch(function(){})}catch(e){}}
window.p1WaTap=function(a){send(a,'whatsapp')};window.p1CtaTap=function(type,a){send(a||null,type)};
function kind(el){var c=el.getAttribute&&el.getAttribute('data-cta');if(c)return c;var u=String(el.href||el.getAttribute('href')||'');
if(WA.test(u))return'whatsapp';if(/^tel:/i.test(u))return'call';if(/^mailto:/i.test(u))return'email';return''}
document.addEventListener('click',function(e){var t=e.target&&e.target.closest?e.target.closest('a[href],[data-cta]'):null;if(!t)return;var k=kind(t);if(k)send(t,k)},true)})();
"""

UI_JS = r"""/* JBStaycation UI: reveal on scroll, carousels. Content is fully visible without JS. */
(function(){
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var els=[].slice.call(document.querySelectorAll('.rv'));
if('IntersectionObserver' in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});els.forEach(function(x){io.observe(x)})}else{els.forEach(function(x){x.classList.add('in')})}
document.querySelectorAll('[data-carousel]').forEach(function(c){
var t=c.querySelector('.track'),held=false,rt=null,iv=null,drag=null;
function step(d){var w=t.clientWidth,max=t.scrollWidth-w;if(max<=0)return;var n=t.scrollLeft+d*w;if(n>max-4&&d>0)n=0;else if(n<0)n=max;t.scrollTo({left:n,behavior:rm?'auto':'smooth'})}
function hold(){held=true;clearTimeout(rt)}
function release(){clearTimeout(rt);rt=setTimeout(function(){held=false},2000)}
c.querySelector('.next').addEventListener('click',function(){step(1);hold();release()});
c.querySelector('.prev').addEventListener('click',function(){step(-1);hold();release()});
t.addEventListener('touchstart',hold,{passive:true});t.addEventListener('touchend',release,{passive:true});t.addEventListener('touchcancel',release,{passive:true});
t.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'){hold();drag={x:e.clientX,l:t.scrollLeft};t.classList.add('drag');t.style.scrollSnapType='none';try{t.setPointerCapture(e.pointerId)}catch(_){}}});
t.addEventListener('pointermove',function(e){if(drag)t.scrollLeft=drag.l-(e.clientX-drag.x)});
function up(){if(drag){drag=null;t.classList.remove('drag');t.style.scrollSnapType='';var w=t.clientWidth;t.scrollTo({left:Math.round(t.scrollLeft/w)*w,behavior:'smooth'});release()}}
t.addEventListener('pointerup',up);t.addEventListener('pointercancel',up);
t.addEventListener('focusin',hold);t.addEventListener('focusout',release);
if(!rm){iv=setInterval(function(){if(!held&&!document.hidden)step(1)},3800)}
});
})();
"""

CSS = r"""
:root{--bg:#faf6ef;--bg2:#f1eadd;--ink:#2a2622;--mute:#6b6258;--brand:#1f4a47;--brand2:#2d6a65;--gold:#b98a4b;--line:#e3d9c7;--card:#fffdf9;--wa:#1d9e55;--wa2:#157a41;--r:16px;--sh:0 8px 28px rgba(60,40,10,.10)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17130f;--bg2:#211b15;--ink:#f2ebdf;--mute:#b3a898;--brand:#8fd0c8;--brand2:#6fbab1;--gold:#d8ad6c;--line:#3a3128;--card:#1d1812;--sh:0 8px 28px rgba(0,0,0,.4)}}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}a{color:var(--brand2)}a:hover{color:var(--gold)}
h1,h2,h3,.brand span,.brand-f{font-family:Georgia,"Iowan Old Style","Times New Roman",serif;line-height:1.2;font-weight:700;color:var(--ink)}
h1{font-size:clamp(1.85rem,6.4vw,3rem);margin:.3em 0 .4em}h2{font-size:clamp(1.4rem,4.6vw,2rem);margin:0 0 .6em}h3{font-size:1.15rem;margin:.2em 0 .4em}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
section{padding:36px 0}.alt{background:var(--bg2)}
.hdr{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hdr-in{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
.brand{display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--ink);margin-right:auto}.brand span{font-size:1.25rem}.brand b{color:var(--gold)}
.nav{order:3;flex:1 1 100%;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}.nav::-webkit-scrollbar{display:none}
.nav a{white-space:nowrap;padding:6px 12px;border-radius:99px;text-decoration:none;color:var(--ink);font-size:.95rem;transition:background .25s}.nav a:hover{background:var(--bg2)}
@media(min-width:860px){.nav{order:0;flex:0 1 auto}.hdr-in{flex-wrap:nowrap}.brand{margin-right:12px}.nav{margin-right:auto}}
.btn{display:inline-flex;align-items:center;gap:8px;padding:13px 22px;border-radius:99px;font-weight:600;text-decoration:none;border:0;cursor:pointer;font-size:1rem;transition:transform .25s ease,box-shadow .25s ease,background .25s}
.btn:hover{transform:translateY(-2px)}.btn:active{transform:scale(.98)}
.btn-wa{background:var(--wa);color:#fff;box-shadow:0 6px 18px rgba(29,158,85,.3)}.btn-wa:hover{background:var(--wa2);color:#fff}
.btn-sm{padding:8px 16px;font-size:.92rem}.btn-line{background:transparent;border:1.5px solid var(--brand);color:var(--brand)}.btn-line:hover{background:var(--brand);color:var(--bg)}
.hero{padding:22px 0 40px}.hero-in{display:grid;gap:24px;align-items:center}
.hero .kick{color:var(--gold);font-weight:600;letter-spacing:.06em;text-transform:uppercase;font-size:.8rem;margin:0}
.lede{font-size:1.1rem;color:var(--mute);max-width:46ch}
.hero-img{border-radius:24px;overflow:hidden;box-shadow:var(--sh);aspect-ratio:4/3;background:var(--bg2)}.hero-img img{width:100%;height:100%;object-fit:cover}
@media(prefers-reduced-motion:no-preference){.hero-img img{animation:kb 18s ease-in-out infinite alternate}@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}}
@media(min-width:860px){.hero-in{grid-template-columns:1fr 1.1fr}}
.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}
.cards{display:grid;gap:20px}@media(min-width:760px){.cards{grid-template-columns:1fr 1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);transition:transform .35s ease,box-shadow .35s ease;display:flex;flex-direction:column}
.card:hover{transform:translateY(-4px)}.card .ph{aspect-ratio:3/2;overflow:hidden;background:var(--bg2)}.card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .6s ease}.card:hover .ph img{transform:scale(1.04)}
.card .cb{padding:16px 18px 20px;display:flex;flex-direction:column;gap:6px;flex:1}.card p{margin:0;color:var(--mute)}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}.pill{background:var(--bg2);border-radius:99px;padding:3px 12px;font-size:.88rem;color:var(--ink)}
.more{margin-top:auto;font-weight:600;text-decoration:none}
.pts{display:grid;gap:14px;padding:0;margin:0;list-style:none}@media(min-width:760px){.pts{grid-template-columns:repeat(2,1fr)}}
.pts li{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px}.pts b{display:block;font-family:Georgia,serif}
.quote{font-family:Georgia,serif;font-size:1.4rem;text-align:center;max-width:30ch;margin:0 auto}.quote cite{display:block;font:500 .95rem system-ui;color:var(--mute);margin-top:8px}
.rv{opacity:1;transform:none}
@media(prefers-reduced-motion:no-preference){.js .rv{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease}.js .rv.in{opacity:1;transform:none}}
.faq{border-bottom:1px solid var(--line);padding:4px 0}.faq summary{cursor:pointer;font-weight:600;padding:12px 0;list-style:none;display:flex;justify-content:space-between;gap:12px}.faq summary::after{content:"+";color:var(--gold);font-size:1.3rem;line-height:1}.faq[open] summary::after{content:"\2212"}.faq summary::-webkit-details-marker{display:none}.faq p{margin:0 0 12px;color:var(--mute)}
.carousel{position:relative;max-width:1080px;margin:0 auto 8px}
.track{list-style:none;margin:0;padding:0;display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;border-radius:20px;touch-action:pan-x pan-y;cursor:grab}.track::-webkit-scrollbar{display:none}.track.drag{cursor:grabbing}
.slide{flex:0 0 100%;scroll-snap-align:center;aspect-ratio:3/2;background:var(--bg2)}.slide img{width:100%;height:100%;object-fit:cover;-webkit-user-drag:none;user-select:none}
.cbtn{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.88);color:#222;font-size:1.7rem;line-height:1;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.25);display:grid;place-items:center;padding:0 0 4px}.prev{left:10px}.next{right:10px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:16px 0}@media(min-width:760px){.stats{grid-template-columns:repeat(4,1fr)}}
.stat{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px}.stat small{color:var(--mute);display:block;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}.stat b{font-size:1.05rem}
.chips{display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:0;list-style:none}.chips li{background:var(--card);border:1px solid var(--line);border-radius:99px;padding:6px 14px;font-size:.95rem}
.two{display:grid;gap:28px}@media(min-width:860px){.two{grid-template-columns:1.4fr 1fr;align-items:start}}
.side{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:18px;box-shadow:var(--sh)}.side .big{font:700 1.8rem Georgia,serif}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:var(--r);overflow:hidden;font-size:.97rem}th,td{padding:12px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}th{background:var(--bg2)}
.tw{overflow-x:auto}.crumbs{font-size:.88rem;color:var(--mute);padding:14px 0 0}.crumbs a{color:var(--mute)}
.answer{background:var(--card);border-left:4px solid var(--gold);padding:14px 18px;border-radius:0 var(--r) var(--r) 0;margin:16px 0;font-size:1.05rem}
.pphoto{border-radius:20px;overflow:hidden;aspect-ratio:21/9;margin:18px 0;background:var(--bg2)}.pphoto img{width:100%;height:100%;object-fit:cover}
.prose p,.prose li{max-width:68ch}.src li{font-size:.92rem;color:var(--mute)}
.stick{position:fixed;left:0;right:0;bottom:0;z-index:40;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:color-mix(in srgb,var(--bg) 94%,transparent);backdrop-filter:blur(8px);border-top:1px solid var(--line);display:flex;justify-content:center}
.stick .btn{width:100%;max-width:520px;justify-content:center}.has-stick{padding-bottom:78px}
.ftr{background:#173a37;color:#e9efe9;padding:34px 0 20px;margin-top:20px}.ftr a{color:#f0dcb6}.ftr .btn-wa{color:#fff}.ftr-in{display:grid;gap:24px}@media(min-width:760px){.ftr-in{grid-template-columns:1.2fr 1.4fr 1fr}}
.brand-f{font-size:1.4rem;margin:0 0 6px;color:#fff}.brand-f b{color:#f0dcb6}.fh{font-weight:700;margin:0 0 6px}.adds{list-style:none;margin:0;padding:0;font-size:.93rem}.adds li{margin-bottom:10px}
.flinks{display:flex;flex-direction:column;gap:6px}.fsmall{margin-top:22px;padding-top:14px;border-top:1px solid rgba(255,255,255,.15);font-size:.85rem;display:flex;gap:12px;justify-content:space-between;flex-wrap:wrap}
.arts{display:grid;gap:18px}@media(min-width:760px){.arts{grid-template-columns:repeat(3,1fr)}}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:99}
"""

HEAD_JS = "<script>document.documentElement.className+=' js'</script>"


def jl(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


PAGES = {}
PENDING = {}


def page(path, title, desc, h1, body, crumbs=None, ld=None, lede='', og=None, photo=None, stick=None, article=False):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, ld=ld or [], lede=lede, og=og, photo=photo, stick=stick, article=article)


def render(path, p):
    pre = '../' * path.count('/')
    url = BASE + path
    og = (p['og'] or IMAGES['home-hero'])
    crumbs = p['crumbs']
    lds = list(p['ld']) + PENDING.get(path, [])
    if crumbs and len(crumbs) > 1:
        lds.append(crumbs_ld(crumbs))
    lds.append({'@context': 'https://schema.org', '@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': p['title'],
                'description': p['desc'], 'dateModified': TODAY, 'inLanguage': 'en-SG', 'isPartOf': {'@type': 'WebSite', 'name': NAME, 'url': BASE},
                'primaryImageOfPage': {'@type': 'ImageObject', 'url': og[0]}})
    hero_h1 = '<h1>%s</h1>' % e(p['h1'])
    if path == '':
        top = ''
    else:
        top = ('<div class="wrap">%s%s%s%s</div>' % (crumbs_html(crumbs) if crumbs and len(crumbs) > 1 else '', hero_h1,
               ('<p class="lede">%s</p>' % p['lede']) if p['lede'] else '',
               ('<div class="pphoto">%s</div>' % img(p['photo'], eager=True)) if p['photo'] else ''))
    stick = ''
    if p['stick']:
        stick = '<div class="stick">%s</div>' % wa_btn(*p['stick'])
    body = ('<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            '<meta name="robots" content="index,follow,max-image-preview:large">'
            '<meta name="theme-color" content="#f7f8f9">'
            '<link rel="icon" href="{pre}favicon.ico" sizes="48x48"><link rel="icon" href="{pre}icon.svg" type="image/svg+xml"><link rel="icon" href="{pre}icon-192.png" sizes="192x192" type="image/png">'
            '<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png"><link rel="manifest" href="{pre}site.webmanifest">'
            '<meta property="og:type" content="{ogt}"><meta property="og:site_name" content="JBStaycation"><meta property="og:title" content="{title}">'
            '<meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogi}"><meta property="og:image:alt" content="{oga}">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:image" content="{ogi}">'
            '{headjs}<link rel="stylesheet" href="{pre}jb.css">{lds}</head><body class="{bc}">'
            '<a class="skip" href="#main">Skip to content</a>{hdr}<main id="main">{top}{content}</main>{ftr}{stick}'
            '<script src="{pre}jb.js" defer></script><script src="{pre}cta.js" defer></script></body></html>').format(
        title=e(p['title']), desc=e(p['desc']), url=url, pre=pre, ogt='article' if p['article'] else 'website', ogi=e(og[0]), oga=e(og[1]),
        headjs=HEAD_JS, lds=''.join(jl(x) for x in lds), bc='has-stick' if stick else '', hdr=header_html(), top=top, content=p['body'],
        ftr=footer_html(), stick=stick)
    return body.replace('{R}', pre)


# ---------------------------------------------------------------- page bodies
def house_card(k):
    h = HOUSES[k]
    return ('<article class="card rv"><a class="ph" href="{R}stays/%s/" tabindex="-1" aria-hidden="true">%s</a><div class="cb"><h3>%s</h3><div class="meta"><span class="pill">Up to %d guests</span><span class="pill">RM %d per night</span></div>'
            '<p>%s</p><a class="more" href="{R}stays/%s/" data-ref="%s">More details about %s &rarr;</a></div></article>'
            % (h['slug'], img(IMAGES[k][0] if k == 'prima' else IMAGES[k][1]), e(h['full']), h['guests'], h['price'], e(h['card']), h['slug'], k, e(h['name'])))


HOME_FAQ = [
    ('How do I book?', 'Message us on WhatsApp at %s with your dates and group size. Bookings are made through WhatsApp only.' % WA_SHOW),
    ('How much is a night?', 'Both houses are listed at RM 500 per night. Prices are in Malaysian ringgit (RM).'),
    ('How many guests can stay?', 'Prima is listed for up to 20 guests and Landak Kawan Fun House for up to 10.'),
    ('Do I need my passport?', 'Yes. ICA states that you must still bring your passport when travelling by land, even with QR code clearance.'),
]


def home_body():
    faq_html, faq_ld = faq_block(HOME_FAQ)
    PENDING.setdefault('',[]).append(faq_ld)
    return ('<section class="hero"><div class="wrap hero-in"><div><p class="kick">%s</p><h1>Johor Bahru holiday houses for Singapore families and groups</h1>'
            '<p class="lede">%s Two private houses in Johor Bahru for birthdays, reunions and long weekends, booked directly on WhatsApp.</p>'
            '<div class="cta-row">%s<a class="btn btn-line" href="{R}stays/">See the houses</a></div></div>'
            '<div class="hero-img">%s</div></div></section>'
            '<section class="alt"><div class="wrap"><h2 class="rv">Our two houses</h2><div class="cards">%s%s</div></div></section>'
            '<section><div class="wrap"><h2 class="rv">Why book with JBStaycation</h2><ul class="pts rv">'
            '<li><b>The whole house is yours</b>Private homes with kitchens, parking and space for the whole group to stay together.</li>'
            '<li><b>Made for group fun</b>Karaoke, mahjong and a BBQ pit at Prima; a pool table, foosball and darts at Landak.</li>'
            '<li><b>Close to the checkpoints</b>Host-stated drive times: Prima about 10 minutes to Tuas, Landak about 10 minutes to CIQ.</li>'
            '<li><b>Simple booking</b>Message us on WhatsApp for dates and rates. Prices are in RM.</li></ul></div></section>'
            '<section><div class="wrap rv"><h2>Plan your weekend in three steps</h2><ol><li><b>Pick a house.</b> Choose Prima for a big group of up to 20, or Landak Kawan Fun House for up to 10 with games and a short walk to KSL City Mall.</li>'
            '<li><b>Message us your dates.</b> Send your group size and dates on WhatsApp and we will confirm the rate and availability.</li>'
            '<li><b>Cross with your passport.</b> Check ICA\'s traffic updates before you leave, then drive in and settle in. Landak has self check-in after 3:00 pm.</li></ol>'
            '<p>Each house suits a different kind of trip: birthdays, reunions, family weekends or a games night with friends. Everything is under one roof, from the kitchen to the entertainment, so nobody has to split up for the evening.</p></div></section>'
            '<section class="alt"><div class="wrap rv"><h2>Getting there from Singapore</h2><p>You can cross by the Woodlands or Tuas land checkpoints (the host states Prima is about 10 minutes from Tuas and 15 from Woodlands), and the RTS Link train from Woodlands North to Bukit Chagar is expected to start passenger service in February 2027, subject to safety certification (LTA, 2 October 2026).</p>'
            '<p><a class="more" href="{R}getting-there/">Read the getting-there guide &rarr;</a></p></div></section>'
            '<section><div class="wrap rv"><blockquote class="quote">&ldquo;%s&rdquo;<cite>%s, guest review on jbstaycation.com</cite></blockquote></div></section>'
            '<div class="alt"><div class="wrap">%s<p><a class="more" href="{R}faq/">More questions and answers &rarr;</a></p></div></div>'
            '<section><div class="wrap rv" style="text-align:center"><h2>Ready to plan your stay?</h2><p>Tell us your dates and how many are coming. We will reply on WhatsApp.</p>%s</div></section>'
            % (e(TAGLINE.rstrip('.')), e(TAGLINE), wa_btn('Check dates on WhatsApp', 'Hi JBStaycation, I would like to check dates and rates for a stay in Johor Bahru.', 'home-hero'),
               img('home-hero', eager=True), house_card('prima'), house_card('landak'), e(REVIEW[0]), e(REVIEW[1]), faq_html,
               wa_btn('Message us on WhatsApp', 'Hi JBStaycation, I would like to check dates and rates for a stay in Johor Bahru.', 'home-cta')))


def stays_body():
    return ('<div class="wrap"><div class="cards" style="margin:24px 0">%s%s</div>'
            '<section class="rv"><h2>Which house is right for you?</h2><div class="tw"><table><thead><tr><th></th><th>Prima</th><th>Landak Kawan Fun House</th></tr></thead><tbody>'
            '<tr><th>Area</th><td>Taman Nusantara Prima, Iskandar Puteri</td><td>Taman Abad, Johor Bahru</td></tr>'
            '<tr><th>Guests</th><td>Up to 20</td><td>Up to 10</td></tr>'
            '<tr><th>Rate</th><td>RM 500 per night</td><td>RM 500 per night</td></tr>'
            '<tr><th>Best for</th><td>Big groups, karaoke, mahjong, BBQ</td><td>Games nights, near KSL City Mall</td></tr>'
            '<tr><th>Host-stated distance</th><td>About 10 min to Tuas, 15 min to Woodlands</td><td>5-minute walk to KSL City Mall, 10 min to CIQ</td></tr>'
            '</tbody></table></div></section></div>' % (house_card('prima'), house_card('landak')))


def house_body(k):
    h = HOUSES[k]
    faq_html, faq_ld = faq_block(h['faq'], 'Questions about %s' % h['name'])
    PENDING.setdefault('stays/%s/' % h['slug'],[]).append(faq_ld)
    stats = ''.join('<div class="stat"><small>%s</small><b>%s</b></div>' % (a, b) for a, b in h['stats'])
    amen = ''.join('<li>%s</li>' % e(a) for a in h['amen'])
    rules = ''.join('<li>%s</li>' % e(r) for r in h['rules'])
    near = ''.join('<tr><th>%s</th><td>%s</td></tr>' % (e(a), e(b)) for a, b in h['near'])
    intro = ''.join('<p>%s</p>' % e(t) for t in h['intro'])
    other = HOUSES['landak' if k == 'prima' else 'prima']
    return ('<div class="wrap">%s<div class="stats">%s</div></div>'
            '<div class="wrap two"><div class="prose">%s'
            '<section class="rv"><h2>What is included</h2><ul class="chips">%s</ul></section>'
            '<section class="rv"><h2>House rules and times</h2><ul>%s</ul></section>'
            '<section class="rv"><h2>Nearby</h2><div class="tw"><table><tbody>%s</tbody></table></div><p><small>%s</small></p></section>'
            '%s'
            '<section class="rv"><h2>Looking for another size?</h2><p>See <a href="{R}stays/%s/">%s</a> (up to %d guests), or read <a href="{R}articles/big-group-staycation-jb-house-for-10-20-people/">how to choose a house for a big group</a>.</p></section></div>'
            '<aside class="side rv"><p class="big">RM %d</p><p>per night. %s. Up to %d guests.</p><p>Prices are in RM. Message us for the rate and availability on your dates.</p>%s</aside></div>'
            % (carousel(h), stats, intro, amen, rules, near, e(h['near_note']), faq_html, other['slug'], e(other['name']), other['guests'],
               h['price'], e(h['minstay']), h['guests'], wa_btn('Check dates & rate', h['msg'], k, 'btn btn-wa')))


def prices_body():
    rows = ''.join('<tr><th><a href="{R}stays/%s/">%s</a></th><td>RM %d per night</td><td>%s</td><td>Up to %d</td></tr>'
                   % (HOUSES[k]['slug'], e(HOUSES[k]['name']), HOUSES[k]['price'], e(HOUSES[k]['minstay']), HOUSES[k]['guests']) for k in ORDER)
    return ('<div class="wrap"><div class="tw"><table><thead><tr><th>House</th><th>Rate</th><th>Minimum stay</th><th>Guests</th></tr></thead><tbody>%s</tbody></table></div>'
            '<section class="rv prose"><h2>What the listing includes</h2><p><b>Prima:</b> fast Wi-Fi, air conditioning, full kitchen, free parking, smart TV, washer and dryer, karaoke set, mahjong table, BBQ pit, workspace and a playground.</p>'
            '<p><b>Landak Kawan Fun House:</b> 100 Mbps Wi-Fi, washer and detergent, hair dryer, iron, workspace, free parking, pool table, foosball, two dartboards and a 55-inch smart TV with arcade console.</p></section>'
            '<section class="rv prose"><h2>Good to know</h2><ul><li>All prices are in Malaysian ringgit (RM).</li><li>Rates for your dates, deposits and payment details are confirmed on WhatsApp.</li>'
            '<li>Landak Kawan Fun House: events need prior approval and may cost extra.</li></ul>%s</section></div>'
            % (rows, wa_btn('Message for dates and rates', 'Hi JBStaycation, I would like to check dates and rates.', 'prices')))


def gt_body():
    srcs = ''.join('<li><a href="%s" rel="noopener">%s</a> (%s)</li>' % (e(u), e(t), e(n)) for t, u, n in [SRC[k] for k in ('lta_feb', 'lta_rts', 'ica_qr', 'ica_traffic')])
    return ('<div class="wrap prose"><div class="answer">There are two road crossings from Singapore, at Woodlands and Tuas. The RTS Link train from Woodlands North to Bukit Chagar is expected to start in February 2027. Prima is nearer Tuas; Landak Kawan Fun House is nearer CIQ and KSL City Mall.</div>'
            '<div class="tw rv"><table><thead><tr><th>Route</th><th>What we can confirm</th><th>Suits</th></tr></thead><tbody>'
            '<tr><th>Woodlands (Causeway)</th><td>ICA operates the Woodlands land checkpoint. Host-stated drive time to Prima: about 15 minutes.</td><td>Prima, or Landak via CIQ</td></tr>'
            '<tr><th>Tuas (Second Link)</th><td>ICA operates the Tuas land checkpoint. Host-stated drive time to Prima: about 10 minutes.</td><td>Prima</td></tr>'
            '<tr><th>RTS Link</th><td>Woodlands North to Bukit Chagar, about 5 minutes by train, co-located immigration. Service expected from February 2027, subject to safety certification.</td><td>Not yet running</td></tr></tbody></table></div>'
            '<section class="rv"><h2>By road: Woodlands or Tuas</h2><p>ICA runs the land checkpoints at Woodlands and Tuas. Traffic can build up on long weekends and holidays, so check ICA\'s <a href="%s" rel="noopener">driving in and out of Singapore page</a> before you leave.</p>'
            '<p>Bring your passport. ICA says you must still bring it for travel when using QR code clearance. ICA also offers QR code clearance through the MyICA app at both checkpoints (see its <a href="%s" rel="noopener">QR code page</a>).</p></section>'
            '<section class="rv"><h2>By train: the RTS Link</h2><p>LTA describes the RTS Link as connecting Woodlands North in Singapore with Bukit Chagar in Johor Bahru, a train journey of about five minutes, with Customs, Immigration and Quarantine facilities co-located so passengers clear both countries at their departure point.</p>'
            '<p>On 2 October 2026 LTA published that passenger service is now expected to start in February 2027, subject to independent safety certification and final approvals. We have not listed fares or opening hours because we have no official figure.</p></section>'
            '<section class="rv"><h2>Which house for which route</h2><ul>'
            '<li><a href="{R}stays/prima-taman-nusantara-prima/">Prima</a>: host states about 10 minutes to Tuas and about 15 minutes to Woodlands.</li>'
            '<li><a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a>: host states about 10 minutes to CIQ and a 5-minute walk to KSL City Mall.</li></ul>'
            '<p>Read more in <a href="{R}articles/causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay/">Causeway, Second Link or RTS: which way to JB</a>.</p>%s</section>'
            '<section class="rv src"><h2>Official sources</h2><ul>%s</ul></section></div>'
            % (SRC['ica_traffic'][1], SRC['ica_qr'][1], wa_btn('Ask us about your route', 'Hi JBStaycation, I would like help planning my route to your house in Johor Bahru.', 'getting-there'), srcs))


FAQ_ALL = [
    ('How do I book?', 'Message us on WhatsApp at %s with your dates, group size and the house you like. We take bookings through WhatsApp only.' % WA_SHOW),
    ('What are the check-in and check-out times?', 'At Landak Kawan Fun House, self check-in is after 3:00 pm and check-out is before 11:00 am. For Prima, message us to confirm the times.'),
    ('What is the minimum stay?', 'Landak Kawan Fun House has a minimum of 1 night. Prima shows a minimum of 2 on its listing; message us to confirm the number of nights.'),
    ('How many guests can stay?', 'Prima is listed for up to 20 guests and Landak Kawan Fun House for up to 10.'),
    ('Is there parking?', 'Yes. Free parking is listed at both houses.'),
    ('Are pets and smoking allowed?', 'At Landak Kawan Fun House, no smoking, no pets, and no BBQ or charcoal grilling. Events need prior approval and may cost extra. For Prima, ask us for the house rules.'),
    ('What currency are prices in?', 'Prices are in Malaysian ringgit (RM). Both houses are listed at RM 500 per night.'),
    ('What should I bring when crossing the border?', 'Bring your passport. ICA states that you must still bring your passport for travel by land, even if you use QR code clearance. Check official sources for current entry requirements.'),
    ('Which house is closer to Tuas?', 'The host states Prima is about 10 minutes from Tuas and about 15 minutes from Woodlands.'),
    ('Which house is near a shopping mall?', 'Landak Kawan Fun House is about a 5-minute walk to KSL City Mall, as stated by the host.'),
]


def faq_body():
    f, ld = faq_block(FAQ_ALL, 'Common questions')
    PENDING.setdefault('faq/',[]).append(ld)
    return '<div class="wrap prose">%s%s<p>Passport and border information comes from <a href="%s" rel="noopener">ICA</a> (checked 8 Nov 2026).</p></div>' % (
        f, wa_btn('Ask us on WhatsApp', 'Hi JBStaycation, I have a question about a stay.', 'faq'), SRC['ica_qr'][1])


def about_body():
    return ('<div class="wrap prose"><section class="rv"><h2>JBStaycation</h2><p>JBStaycation offers private holiday houses in Johor Bahru for families and groups, many of them travelling from Singapore. Our idea is simple: %s</p>'
            '<p>We have two houses, <a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Taman Nusantara Prima, Iskandar Puteri, and <a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad, Johor Bahru.</p>'
            '<p>Bookings are made directly with us on WhatsApp at %s. Prices are in RM.</p></section>'
            '<section class="rv"><h2>Addresses</h2><ul>%s</ul>%s</section></div>'
            % (e(TAGLINE.lower()), WA_SHOW, ''.join('<li><b>%s</b>: %s</li>' % (e(HOUSES[k]['name']), e(HOUSES[k]['addr'])) for k in ORDER),
               wa_btn('Message us', 'Hi JBStaycation, I would like to ask about a stay.', 'about')))


def contact_body():
    return ('<div class="wrap prose"><section class="rv"><h2>Message us on WhatsApp</h2><p>WhatsApp is the only way to book: <b>%s</b>. Tell us the house, your dates and how many people.</p>%s'
            '<p>Houses: %s</p></section></div>'
            % (WA_SHOW, wa_btn('Open WhatsApp', 'Hi JBStaycation, I would like to ask about a stay.', 'contact'),
               ' | '.join('<a href="{R}stays/%s/">%s</a>' % (HOUSES[k]['slug'], e(HOUSES[k]['name'])) for k in ORDER)))


def privacy_body():
    return ('<div class="wrap prose"><p>Last updated %s.</p><h2>What we collect</h2><p>When you message us on WhatsApp we receive your phone number, name shown on WhatsApp and whatever you write, such as dates and group size.</p>'
            '<h2>How we use it</h2><p>We use it to reply to your enquiry, confirm a booking and manage your stay. We do not sell your personal data.</p>'
            '<h2>Who sees it</h2><p>Messages are handled through WhatsApp, which has its own privacy policy. We share details only with people who help run your stay, or where the law requires.</p>'
            '<h2>Website analytics</h2><p>This website counts taps on contact links (for example WhatsApp) with an anonymous visitor identifier to understand which pages help visitors. It does not store your message.</p>'
            '<h2>Your choices</h2><p>You can ask us on WhatsApp to access, correct or delete your personal data, or to stop contacting you, in line with Malaysia\'s Personal Data Protection Act and Singapore\'s PDPA where they apply.</p>'
            '<p>We keep enquiry messages only as long as needed for the purposes above.</p></div>' % TODAY)


def articles_body():
    cards = ''.join('<article class="card rv"><a class="ph" href="{R}articles/%s/" tabindex="-1" aria-hidden="true">%s</a><div class="cb"><h3><a href="{R}articles/%s/">%s</a></h3><p>%s</p><a class="more" href="{R}articles/%s/">Read article &rarr;</a></div></article>'
                    % (a['slug'], img(IMAGES[a['img']][0] if a['img'] == 'prima' else IMAGES[a['img']][2]), a['slug'], e(a['title']), e(a['desc']), a['slug']) for a in ARTICLES)
    return '<div class="wrap"><div class="arts" style="margin:24px 0">%s</div></div>' % cards


def article_body(a):
    secs = ''.join('<section class="rv"><h2>%s</h2>%s</section>' % (e(h), ''.join('<p>%s</p>' % t for t in ps)) for h, ps in a['sections'])
    hh = HOUSES[a['house']]
    return ('<div class="wrap prose"><p><small>By JBStaycation, %s</small></p><div class="answer">%s</div>%s'
            '<section class="rv"><p>See the house: <a href="{R}stays/%s/">%s</a>.</p>%s</section></div>'
            % (TODAY, e(a['answer']), secs, hh['slug'], e(hh['full']), wa_btn('Ask about dates', hh['msg'], 'article-' + a['slug'][:30])))


# ---------------------------------------------------------------- assemble
def build_pages():
    page('', 'JB Holiday Houses for Singapore Groups | JBStaycation',
         'Private holiday houses in Johor Bahru for Singapore families and groups. Up to 20 guests, RM 500 per night, book on WhatsApp.',
         'Johor Bahru holiday houses for Singapore families and groups', '', ld=[org_ld(), {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NAME, 'url': BASE}])
    PAGES['']['body'] = home_body()
    page('stays/', 'Johor Bahru Holiday Houses | JBStaycation', 'Compare Prima (up to 20 guests) and Landak Kawan Fun House (up to 10 guests): private holiday houses in Johor Bahru, RM 500 per night.',
         'Our Johor Bahru holiday houses', stays_body(), [('Home', ''), ('Stays', 'stays/')],
         lede='Two private houses, one for big groups and one for games nights near KSL City Mall.', photo='home-hero',
         ld=[{'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + 'stays/%s/' % HOUSES[k]['slug'], 'name': HOUSES[k]['full']} for i, k in enumerate(ORDER)]}])
    for k in ORDER:
        h = HOUSES[k]
        path = 'stays/%s/' % h['slug']
        titles = {'prima': ('Prima: JB House for Up to 20 Guests | JBStaycation', 'Prima in Iskandar Puteri sleeps up to 20 guests, with karaoke, mahjong, BBQ pit and rooftop terrace. RM 500 per night. Book on WhatsApp.'),
                  'landak': ('Landak Kawan Fun House near KSL City Mall | JBStaycation', 'Private JB house for up to 10 guests with pool table, foosball and darts, a 5-minute walk to KSL City Mall. RM 500 per night.')}[k]
        page(path, titles[0], titles[1], h['full'], '', [('Home', ''), ('Stays', 'stays/'), (h['name'], path)], ld=[house_ld(h)],
             og=IMAGES[k][0], stick=('Check dates & rate', h['msg'], 'sticky-' + k))
        PAGES[path]['body'] = house_body(k)
        PAGES[path]['lede'] = ''
    page('prices/', 'Prices: JB Holiday Houses in RM | JBStaycation', 'JBStaycation rates: RM 500 per night at Prima and Landak Kawan Fun House, minimum stay and what is included. Message for dates.',
         'Prices (RM per night)', prices_body(), [('Home', ''), ('Prices', 'prices/')], lede='Both houses are listed at RM 500 per night. Message us for your dates.', photo='home-hero')
    page('getting-there/', 'Getting to JB from Singapore by Road or RTS | JBStaycation', 'Woodlands, Tuas or the RTS Link to Johor Bahru? Official facts with sources and which JBStaycation house suits each route.',
         'Getting to our Johor Bahru houses from Singapore', gt_body(), [('Home', ''), ('Getting there', 'getting-there/')],
         lede='Facts below come from official sources, with the date we checked them.', photo='landak')
    page('faq/', 'FAQ: Booking a JB Holiday House | JBStaycation', 'Answers on booking, check-in, minimum nights, guests, parking, pets, currency and crossing the border for JBStaycation houses.',
         'Frequently asked questions', faq_body(), [('Home', ''), ('FAQ', 'faq/')], photo='prima')
    page('about/', 'About JBStaycation | Johor Bahru Holiday Houses', 'JBStaycation offers two private holiday houses in Johor Bahru for Singapore families and groups, booked directly on WhatsApp.',
         'About JBStaycation', about_body(), [('Home', ''), ('About', 'about/')], lede=TAGLINE, photo='home-hero',
         ld=[org_ld()])
    page('contact/', 'Contact JBStaycation on WhatsApp', 'Book or ask a question on WhatsApp +65 9006 2198. Tell us the house, dates and group size.',
         'Contact us', contact_body(), [('Home', ''), ('Contact', 'contact/')], lede='WhatsApp is the fastest way to reach us.', photo='landak')
    page('privacy/', 'Privacy Notice | JBStaycation', 'How JBStaycation handles personal data from WhatsApp enquiries and website visits.', 'Privacy notice', privacy_body(), [('Home', ''), ('Privacy', 'privacy/')])
    page('articles/', 'JB Staycation Guides and Articles | JBStaycation', 'Plain-English guides for Singapore groups planning a Johor Bahru house stay: group size, KSL City Mall area and routes.',
         'Guides for staying in Johor Bahru', articles_body(), [('Home', ''), ('Articles', 'articles/')], lede='Practical answers for groups crossing from Singapore.')
    for a in ARTICLES:
        path = 'articles/%s/' % a['slug']
        ph = a['img']
        page(path, a.get('ttl') or a['title'], a['desc'], a['h1'], article_body(a),
             [('Home', ''), ('Articles', 'articles/'), (a['title'], path)], photo=(IMAGES[ph][0] if ph == 'prima' else IMAGES[ph][1]), article=True,
             og=IMAGES[ph][0] if ph == 'prima' else IMAGES[ph][1],
             ld=[{'@context': 'https://schema.org', '@type': 'Article', 'headline': a['title'], 'description': a['desc'], 'datePublished': TODAY, 'dateModified': TODAY,
                  'author': {'@type': 'Organization', 'name': NAME, 'url': BASE}, 'publisher': {'@type': 'Organization', 'name': NAME, 'logo': {'@type': 'ImageObject', 'url': BASE + 'icon-512.png'}},
                  'image': (IMAGES[ph][0] if ph == 'prima' else IMAGES[ph][1])[0], 'mainEntityOfPage': BASE + path}])


def make_icons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1f4a47"/>'
           '<path d="M12 31 32 14l20 17h-5v18H17V31z" fill="#faf6ef"/><rect x="27" y="35" width="10" height="14" rx="2" fill="#b98a4b"/></svg>')
    open(os.path.join(OUT, 'icon.svg'), 'w').write(svg)
    try:
        from PIL import Image, ImageDraw
        def draw(sz):
            im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            s = sz / 64.0
            d.rounded_rectangle([0, 0, sz - 1, sz - 1], radius=int(14 * s), fill=(31, 74, 71, 255))
            d.polygon([(12 * s, 31 * s), (32 * s, 14 * s), (52 * s, 31 * s), (47 * s, 31 * s), (47 * s, 49 * s), (17 * s, 49 * s), (17 * s, 31 * s)], fill=(250, 246, 239, 255))
            d.rounded_rectangle([27 * s, 35 * s, 37 * s, 49 * s], radius=int(2 * s), fill=(185, 138, 75, 255))
            return im
        draw(512).save(os.path.join(OUT, 'icon-512.png'))
        draw(192).save(os.path.join(OUT, 'icon-192.png'))
        draw(180).save(os.path.join(OUT, 'apple-touch-icon.png'))
        draw(256).save(os.path.join(OUT, 'favicon.ico'), sizes=[(48, 48), (32, 32), (16, 16)])
    except Exception as ex:
        print('PIL icons failed:', ex)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    build_pages()
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(render(path, p))
    # 404 (renders with site-root-relative assets via absolute BASE paths)
    nf = ('<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | JBStaycation</title>'
          '<meta name="robots" content="max-image-preview:large"><link rel="icon" href="%sicon.svg" type="image/svg+xml"><link rel="stylesheet" href="%sjb.css"></head><body>%s<main id="main"><div class="wrap" style="padding:48px 16px"><h1>Page not found</h1><p>That page does not exist. Try our <a href="%s">home page</a>, the <a href="%sstays/">stays</a> or message us on WhatsApp.</p>%s</div></main>%s<script src="%scta.js" defer></script></body></html>'
          % (BASE, BASE, header_html(), BASE, BASE, wa_btn('WhatsApp us', 'Hi JBStaycation, I would like to ask about a stay.', '404'), footer_html(), BASE))
    nf = nf.replace('{R}', BASE)
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)
    open(os.path.join(OUT, 'jb.css'), 'w').write(CSS)
    open(os.path.join(OUT, 'jb.js'), 'w').write(UI_JS)
    open(os.path.join(OUT, 'cta.js'), 'w').write(CTA_JS)
    make_icons()
    # sitemap
    urls = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>' % (BASE + p, TODAY) for p in PAGES)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
    open(os.path.join(OUT, 'robots.txt'), 'w').write(
        'User-agent: *\nUser-agent: OAI-SearchBot\nUser-agent: ChatGPT-User\nUser-agent: GPTBot\nUser-agent: Googlebot\nUser-agent: Bingbot\n'
        'User-agent: PerplexityBot\nUser-agent: ClaudeBot\nUser-agent: Claude-SearchBot\nUser-agent: Google-Extended\nUser-agent: Applebot-Extended\nUser-agent: DuckAssistBot\n'
        'Allow: /\n\nSitemap: %ssitemap.xml\n' % BASE)
    open(os.path.join(OUT, 'site.webmanifest'), 'w').write(json.dumps({'name': NAME, 'short_name': NAME, 'start_url': BASE, 'display': 'browser', 'background_color': '#faf6ef', 'theme_color': '#1f4a47',
        'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=1))
    ll = ['# JBStaycation', '', '> %s Private holiday houses in Johor Bahru, Malaysia, for Singapore families and groups. Booking by WhatsApp only: %s (%s). Prices in RM.' % (TAGLINE, WA_SHOW, WA_BASE), '', '## Houses']
    for k in ORDER:
        h = HOUSES[k]
        ll.append('- [%s](%sstays/%s/): %s. Up to %d guests, RM %d per night. %s' % (h['full'], BASE, h['slug'], h['addr'], h['guests'], h['price'], h['card']))
    ll += ['', '## Pages', '- [Prices](%sprices/)' % BASE, '- [Getting there from Singapore](%sgetting-there/)' % BASE, '- [FAQ](%sfaq/)' % BASE, '- [About](%sabout/)' % BASE, '- [Contact](%scontact/)' % BASE, '- [Articles](%sarticles/)' % BASE]
    for a in ARTICLES:
        ll.append('  - [%s](%sarticles/%s/)' % (a['title'], BASE, a['slug']))
    open(os.path.join(OUT, 'llms.txt'), 'w').write('\n'.join(ll) + '\n')
    path_prefix = '/' + BASE.split('/', 3)[3]
    open(os.path.join(OUT, 'htaccess.txt'), 'w').write(
        '# Rename to .htaccess in this folder via cPanel. Preview hiding is handled by the server outside the pages.\n'
        'RewriteEngine On\nRewriteCond %{HTTPS} !=on\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n'
        'DirectoryIndex index.html\nErrorDocument 404 ' + path_prefix + '404.html\n'
        '<IfModule mod_headers.c>\n<FilesMatch "\\.(html|xml|txt)$">\nHeader set Cache-Control "public, max-age=3600"\n</FilesMatch>\n</IfModule>\n')
    print('pages:', len(PAGES) + 1, 'built into', OUT)


if __name__ == '__main__':
    main()

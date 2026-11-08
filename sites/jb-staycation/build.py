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


def wa_msg(house=None):
    """Prefilled WhatsApp text. house = 'prima', 'landak' or None (not sure yet)."""
    label = {'prima': 'Prima', 'landak': 'Landak'}.get(house, 'not sure yet')
    return "[House: %s] Hi JBStaycation, I'd like to check dates. Group size: ___ Dates: ___" % label

CONFIRM = [
    'Legal/business name of the host (kept off the site).',
    'Prima bedrooms: client site says 3 in the header and 5 in text/gallery. Pages say "Bedrooms: ask us" (no count shown).',
    'Prima "Minimum 2": source gives no unit; page says "Minimum 2 (see WhatsApp for details)" and never "2 nights".',
    'Prima 900 sq ft (as stated by client) looks small for 20 guests; left off the page.',
    'Prima check-in/out times, quiet hours, deposit amount and house rules (none verified; pages say ask us on WhatsApp).',
    'No guest reviews are shown anywhere (Edwin, 8 Nov 2026): add only real, permitted reviews later.',
    'Deposit, cancellation and payment terms (client T&C is an unfilled template; no /terms/ page built).',
    'SGD equivalents: not shown until Edwin agrees.',
    'Google Business Profile, Airbnb, social links, email (none known; no sameAs).',
    'Brand colours/fonts: v2 uses the client site tokens (navy #0a1f38, amber #e8a33d, page #f7f8f9) and Geist from Google Fonts.',
    'Photos are self-hosted in site/img/ (client files). img-1806 (brand hero, dusk bungalow) does not visibly match either house: confirm which house it is or if it is a render.',
    'Prima: 13 photo files on the client site are exact duplicates under other names (e.g. backyard = rooftop-terrace); only one of each is used.',
    'Host drive times (Tuas 10 min / Woodlands 15 min / KSL etc.) are as stated by the host, not independently timed.',
    'Does the photo set include people/cars (privacy) and may we use them? (client own photos assumed).',
]


# ---------------------------------------------------------------- images (client's own photos, self-hosted in site/img/, 480px thumbs in site/thumb/)
SRC_IMG = os.path.join(HERE, 'photos-src')
HERO_IMG = 'img-1806-afec0c7d.webp'   # brand image the client uses on its homepage
HERO_ALT = 'JBStaycation: a holiday house at dusk with a lit car porch'

# Landak Kawan Fun House: files 01- to 43-. Captions = the client's own alt text.
_LK = {
    1: '01-hero-1-88ecc683', 2: '02-highlights-1-41de69c7', 3: '03-highlights-2-4cf4369d', 4: '04-highlights-3-c67373ad',
    5: '05-highlights-4-4eab123b', 6: '06-highlights-5-a864f872', 7: '07-highlights-6-486ef2d0', 8: '08-highlights-7-f5a62d22',
    9: '09-highlights-8-7d0593af', 10: '10-highlights-9-fe22e9ed', 11: '11-highlights-10-10628baa',
    12: '12-living-and-dining-1-bccc0015', 13: '13-living-and-dining-2-1b8bd0fd', 14: '14-living-and-dining-3-c3d37224',
    15: '15-living-and-dining-4-e06cf635', 16: '16-living-and-dining-5-63e4596c', 17: '17-games-courtyard-1-b219ad12',
    18: '18-games-courtyard-2-7cad6564', 19: '19-games-courtyard-3-4d24a278', 20: '20-games-courtyard-4-a2e2bd67',
    21: '21-kitchen-1-786943e2', 22: '22-kitchen-2-114d1833', 23: '23-kitchen-3-52b50093', 24: '24-kitchen-4-57164504',
    25: '25-bedroom-1-1-3785781e', 26: '26-bedroom-1-2-7951bd61', 27: '27-bedroom-2-1-beab14bf', 28: '28-bedroom-2-2-e34cec1d',
    29: '29-bedroom-3-1-91e8c731', 30: '30-bedroom-3-2-5c34b770', 31: '31-bathrooms-1-09c580ec', 32: '32-bathrooms-2-8c0782c3',
    33: '33-bathrooms-3-2d70288e', 34: '34-bathrooms-4-968165a8', 35: '35-bathrooms-5-b30dfb87', 36: '36-workspace-1-21bd534f',
    37: '37-workspace-2-4ad2a210', 38: '38-workspace-3-366b08b7', 39: '39-workspace-4-3bb30ebb', 40: '40-exterior-and-parking-1-aae8fe23',
    41: '41-exterior-and-parking-2-bf428544', 42: '42-exterior-and-parking-3-54084eb5', 43: '43-exterior-and-parking-4-4de451ba',
}
LK_CAP = {1: 'Bright open-plan living room', 2: 'Private games courtyard with pool table and seating', 3: 'Open-plan living room with foosball table',
          4: 'Dining and living area for group gatherings', 5: 'Kitchen with breakfast counter and appliances', 6: 'Bedroom 1 with king bed',
          7: 'Bedroom 2 with two queen beds', 8: 'Bedroom 3 with two queen beds', 9: 'Modern full bathroom with hot shower and bidet',
          10: 'Front view of the private double-storey home', 11: 'Sheltered car porch with on-site parking'}


def _lk(n, room):
    return (_LK[n] + '.webp', LK_CAP.get(n) or room, n in LK_CAP)


# Each room: (title, note, [(file, caption, caption_is_client_text)])
ROOMS = {
    'landak': [
        ('Living and dining', '', [_lk(n, 'Living and dining area') for n in (1, 3, 4, 12, 13, 14, 15, 16)]),
        ('Games courtyard', 'Pool table and dartboards', [_lk(n, 'Games courtyard') for n in (2, 17, 18, 19, 20)]),
        ('Kitchen', '', [_lk(n, 'Kitchen') for n in (5, 21, 22, 23, 24)]),
        ('Bedroom 1', '1 king bed', [_lk(n, 'Bedroom 1') for n in (6, 25, 26)]),
        ('Bedroom 2', '2 queen beds', [_lk(n, 'Bedroom 2') for n in (7, 27, 28)]),
        ('Bedroom 3', '2 queen beds', [_lk(n, 'Bedroom 3') for n in (8, 29, 30)]),
        ('Bathrooms', '3 bathrooms', [_lk(n, 'Bathroom') for n in (9, 31, 32, 33, 34, 35)]),
        ('Workspace', '', [_lk(n, 'Workspace') for n in (36, 37, 38, 39)]),
        ('Exterior and parking', '', [_lk(n, 'Exterior and parking') for n in (10, 11, 40, 41, 42, 43)]),
    ],
    # Prima: room is in the filename. 13 files on the client site are exact duplicates of these
    # (backyard, garden-1-97b7, toilet2, bedroom2, bedroom1-2, bedroom1, bedroom-5, livingroom, gatheringroom,
    # kitchen-66e7, tvconsole, studyroom-2, studyroom) and are not used.
    'prima': [
        ('Living room', '', [(f + '.webp', 'Living room', False) for f in (
            'living-room-1-916f5d01', 'living-room-2-e3f4ccd4', 'living-room-3-4de54474', 'living-room-4-09df35da', 'living-room-5-c42ada8d',
            'living-room-6-58efc964', 'living-room-7-94937415', 'living-room-8-2dad309f', 'living-room-9-6b9b736a')]),
        ('Games room', '', [(f + '.webp', 'Games room', False) for f in (
            'games-room-1-a94462c4', 'games-room-2-e0c3668e', 'games-room-3-7d4dae40', 'games-room-4-3b5fcf99', 'games-room-5-463298ed', 'games-room-6-2f421093')]),
        ('Dining room and kitchen', 'Full kitchen', [(f + '.webp', 'Dining room', False) for f in (
            'dining-room-1-4fb79ea0', 'dining-room-2-d041a842', 'dining-room-3-9e6aac83', 'dining-room-4-0f90d8aa', 'dining-room-5-424b5f73',
            'dining-room-6-8ef08b80', 'dining-room-7-a447f6c2', 'dining-room-8-bf0437ed')] +
            [(f + '.webp', 'Kitchen', False) for f in ('kitchen-1-6f876b58', 'kitchen-2-f84cf6f0', 'kitchen-3-afedb0bd')]),
        ('Family room and study corner', '', [(f + '.webp', 'Family room', False) for f in ('family-room-1-61218aa1', 'family-room-2-7f143ce7', 'family-room-3-baf58566', 'study-corner-4-cce1ac60')] +
            [(f + '.webp', 'Study corner', False) for f in ('study-corner-1-e2d6f7ba', 'study-corner-2-af2d02e4', 'study-corner-3-1f334b39')] +
            [('staircase-landing-7c95c19d.webp', 'Staircase landing', False)]),
        ('Bedrooms', '', [('bedroom-1-1-5cde8eac.webp', 'Bedroom 1', False), ('bedroom-1-2-6925f4c5.webp', 'Bedroom 1', False), ('bedroom-1-3-4168443a.webp', 'Bedroom 1', False),
                          ('bedroom-2-3fe1fa07.webp', 'Bedroom 2', False), ('bedroom-3-1-6f40c7d6.webp', 'Bedroom 3', False), ('bedroom-3-2-b88c72f7.webp', 'Bedroom 3', False),
                          ('bedroom-4-1-13bbad20.webp', 'Bedroom 4', False), ('bedroom-4-2-e813a884.webp', 'Bedroom 4', False),
                          ('bedroom-4-wardrobe-397856ab.webp', 'Bedroom 4 wardrobe', False), ('dressingroom-7fd7ee5f.webp', 'Dressing room', False)]),
        ('Bathrooms', '3 bathrooms', [('bathroom-1-14943f1d.webp', 'Bathroom', False), ('bathroom-2-1-0f06862d.webp', 'Bathroom 2', False), ('bathroom-2-2-2fc303c3.webp', 'Bathroom 2', False)]),
        ('Balcony and rooftop terrace', '', [(f + '.webp', 'Balcony', False) for f in ('balcony-1-ea2ec609', 'balcony-2-39784ce0', 'balcony-3-f340b9e8', 'balcony-4-c4870fe4', 'garden-1-f484d67f')] +
            [('rooftop-terrace-769478b2.webp', 'Rooftop terrace', False)]),
    ],
}
# hero bento (first 5 photos on each house page; mobile carousel)
BENTO = {
    'landak': ['01-hero-1-88ecc683.webp', '02-highlights-1-41de69c7.webp', '06-highlights-5-a864f872.webp', '03-highlights-2-4cf4369d.webp', '05-highlights-4-4eab123b.webp'],
    'prima': ['living-room-2-e3f4ccd4.webp', 'games-room-3-7d4dae40.webp', 'bedroom-1-1-5cde8eac.webp', 'dining-room-4-0f90d8aa.webp', 'balcony-4-c4870fe4.webp'],
}
# house cards (main photo + 3-thumb strip)
CARD_IMG = {
    'prima': ['living-room-3-4de54474.webp', 'games-room-2-e0c3668e.webp', 'bedroom-3-1-6f40c7d6.webp', 'balcony-1-ea2ec609.webp'],
    'landak': ['12-living-and-dining-1-bccc0015.webp', '17-games-courtyard-1-b219ad12.webp', '07-highlights-6-486ef2d0.webp', '04-highlights-3-c67373ad.webp'],
}
# page and article photos
PAGE_IMG = {
    'stays': HERO_IMG, 'prices': '14-living-and-dining-3-c3d37224.webp', 'getting-there': 'balcony-2-39784ce0.webp',
    'faq': 'living-room-4-09df35da.webp', 'about': HERO_IMG, 'contact': '15-living-and-dining-4-e06cf635.webp',
    'big-group-staycation-jb-house-for-10-20-people': 'games-room-5-463298ed.webp',
    'staying-near-ksl-city-mall-what-is-within-5-15-minutes': '13-living-and-dining-2-1b8bd0fd.webp',
    'causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay': 'balcony-3-f340b9e8.webp',
}
HOME_MOSAIC = ['dining-room-7-a447f6c2.webp', '19-games-courtyard-3-4d24a278.webp', 'family-room-2-7f143ce7.webp']
HOME_CTA_IMG = 'living-room-7-94937415.webp'


_ALT = {}


def _alt_for(f):
    """alt text for any photo: the client's caption (Landak) or the room from the filename (Prima), numbered when repeated."""
    if not _ALT:
        for k, rooms in ROOMS.items():
            seen = {}
            for _t, _n, ph in rooms:
                for pf, cap, is_client in ph:
                    if is_client:
                        _ALT[pf] = '%s, %s' % (cap, HOUSES[k]['name'])
                    else:
                        seen[cap] = seen.get(cap, 0) + 1
                        tot = sum(1 for _a, _b, p2 in rooms for x in p2 if x[1] == cap and not x[2])
                        _ALT[pf] = '%s at %s%s' % (cap, HOUSES[k]['name'], (', view %d' % seen[cap]) if tot > 1 else '')
    return _ALT.get(f, HERO_ALT)


def used_images():
    s = {HERO_IMG, HOME_CTA_IMG} | set(HOME_MOSAIC) | set(PAGE_IMG.values())
    for k in ROOMS:
        for _t, _n, ph in ROOMS[k]:
            s |= {p[0] for p in ph}
        s |= set(BENTO[k]) | set(CARD_IMG[k])
    return sorted(s)


DIM = {}
HAS_THUMB = False


def load_dims():
    try:
        from PIL import Image
        for f in used_images():
            with Image.open(os.path.join(SRC_IMG, f)) as im:
                DIM[f] = im.size
    except Exception as ex:
        print('PIL not available, assuming 1200x900:', ex)


def dims(f):
    return DIM.get(f, (1200, 900))


def abs_img(f):
    return BASE + 'img/' + f


# ---------------------------------------------------------------- houses
HOUSES = {
    'prima': {
        'slug': 'prima-taman-nusantara-prima', 'name': 'Prima', 'full': 'Prima, Taman Nusantara Prima',
        'short': 'Prima at Taman Nusantara Prima',
        'street': '19 Jalan Prima 3/1, Taman Nusantara Prima', 'locality': 'Iskandar Puteri', 'region': 'Johor', 'postal': '79200',
        'addr': '19 Jalan Prima 3/1, Taman Nusantara Prima, Iskandar Puteri, Johor 79200, Malaysia',
        'guests': 20, 'price': 500, 'minstay': 'Minimum 2 (see WhatsApp for details)',
        'tag': 'Big group house with karaoke, mahjong and a BBQ pit',
        'card': 'A fully furnished house for up to 20 guests, with karaoke, a mahjong table, BBQ pit, games room and rooftop terrace.',
        'stats': [('Guests', 'Up to 20'), ('Bedrooms', 'Ask us'), ('Bathrooms', '3'), ('Rate', 'RM 500 per night')],
        'intro': ['Prima is a private holiday house in Taman Nusantara Prima, Iskandar Puteri, listed for up to 20 guests at RM 500 per night. It has karaoke, a mahjong table, a BBQ pit and 3 bathrooms, with a full kitchen and free parking.',
                  'There is room to spread out. Spaces include a games room, a family room, a study corner, a rooftop terrace and a balcony, with a full kitchen for cooking together.',
                  'The host states it is about 10 minutes to Tuas and about 15 minutes to Woodlands, which makes it a natural pick if you cross by the Second Link.'],
        'amen': ['Fast Wi-Fi', 'Air conditioning', 'Full kitchen', 'Free parking', 'Smart TV', 'Washer and dryer', 'Karaoke set',
                 'Mahjong table', 'BBQ pit', 'Workspace / desk', 'Playground', 'Games room', 'Study corner', 'Family room',
                 'Rooftop terrace', 'Balcony', 'Dressing room'],
        'rules': ['Check-in and check-out times, quiet hours, smoking, pets and BBQ rules for Prima are not stated on our listing yet. Message us on WhatsApp and we will confirm them before you book.', 'Events or larger gatherings need prior approval and may cost extra. Guests must not disturb neighbours.'],
        'near': [('Tuas', 'about 10 minutes'), ('Woodlands', 'about 15 minutes')],
        'near_note': 'Drive times are as stated by the host.',
        'faq': [
            ('How many people can Prima sleep?', 'Prima is listed for up to 20 guests. Message us your group size and dates and we will confirm the setup.'),
            ('Is there a minimum stay at Prima?', 'The listing shows "Minimum 2" without a unit, so please ask us on WhatsApp for the minimum stay on your dates.'),
            ('What are the check-in and check-out times at Prima?', 'We have not listed them for Prima yet. Ask us on WhatsApp and we will confirm before you book.'),
            ('Can we sing karaoke or play mahjong?', 'Prima has a karaoke set and a mahjong table. Quiet hours are not listed, so ask us on WhatsApp, and please keep in mind the host asks guests not to disturb neighbours.'),
            ('Is there parking?', 'Yes, free parking is listed for Prima.'),
        ],
        'msg': wa_msg('prima'),
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
        'intro': ['Landak Kawan Fun House is a private house in Taman Abad, Johor Bahru, a 5-minute walk from KSL City Mall, for up to 10 guests at RM 500 per night. It has 3 bedrooms, 3 bathrooms, a pool table, foosball and darts.',
                  'The double-storey home sleeps 10 with 1 king bed plus 4 queen beds (bedrooms 2 and 3 each have two queens).',
                  'The fun is built in: an 8-foot pool table in the games courtyard, a foosball table, two dartboards and a 55-inch smart TV with an arcade console.',
                  'It is about a 5-minute walk to KSL City Mall, and the host states 10 minutes by car to JB City Square, KOMTAR JBCC and CIQ.'],
        'amen': ['8-ft pool table', 'Foosball table', 'Two dartboards', 'Kitchen for light cooking', 'Free parking', '100 Mbps Wi-Fi', 'Air conditioning',
                 '55-inch smart TV with arcade console', 'Washer and dryer', 'Workspace', 'Playground', 'Hair dryer', 'Iron', 'Self check-in'],
        'rules': ['Check-in: self check-in after 3:00 pm.', 'Check-out: before 11:00 am.', 'No smoking.', 'No pets.',
                  'No BBQ or charcoal grilling.', 'Events need prior approval and may cost extra.', 'Guests must not disturb neighbours.'],
        'near': [('KSL City Mall', '5-minute walk'), ('Yu Ee hawker centre', '3 minutes'), ('JB City Square, KOMTAR JBCC, CIQ', '10 minutes'),
                 ('R&F Mall', '12 minutes'), ('Mid Valley Southkey', '12 minutes'), ('AEON Tebrau, IKEA, Toppen', '18 minutes')],
        'near_note': 'Times other than the walk are drive times as stated by the host.',
        'faq': [
            ('What time is check-in and check-out at Landak Kawan Fun House?', 'Self check-in is after 3:00 pm and check-out is before 11:00 am.'),
            ('What is the minimum stay?', 'The minimum stay is 1 night.'),
            ('Are pets, smoking or BBQ allowed?', 'No. Smoking, pets, BBQ and charcoal grilling are not allowed. Events need prior approval and may cost extra.'),
            ('Is there parking, and can we cook?', 'Free parking is listed, and there is a kitchen for light cooking. BBQ and charcoal grilling are not allowed.'),
            ('What is there to do inside the house?', 'There is an 8-foot pool table, a foosball table, two dartboards and a 55-inch smart TV with an arcade console.'),
        ],
        'msg': wa_msg('landak'),
        'key': 'landak',
    },
}
ORDER = ['prima', 'landak']
H1S = {'prima': 'Prima: JB holiday house with karaoke for up to 20 guests', 'landak': 'Staycation near KSL City Mall: Landak Kawan Fun House'}


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
            ('Up to 20 guests: Prima', ['<a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Taman Nusantara Prima, Iskandar Puteri, is listed for up to 20 guests with 3 bathrooms; ask us about the bedrooms. The rate is RM 500 per night; the listing shows "Minimum 2" without a unit, so ask us for the minimum stay.',
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
        'house': 'landak', 'img': 'landak', 'wa': 'landak',
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
    return WA_BASE + '?text=' + quote(msg, safe='')


WA_SVG = ('<svg class="ico" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.1 1.2z"/></svg>')


def wa_btn(label, msg, ref, cls='btn btn-wa', aria=None):
    return ('<a class="%s" href="%s" data-cta="whatsapp" data-cta-label="%s" rel="noopener"%s>%s<span>%s</span></a>'
            % (cls, e(wa_url(msg)), e(ref), (' aria-label="%s"' % e(aria)) if aria else '', WA_SVG, e(label)))


# inline stroke icons (24x24, no external icon library)
ICONS = {
    'wifi': '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>',
    'snow': '<path d="M12 2v20M3.3 7l17.4 10M20.7 7 3.3 17M9 4l3 2 3-2M9 20l3-2 3 2"/>',
    'pot': '<path d="M4 10h16v7a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3zM2 10h20M9 6c0-1 1-2 1-3M14 6c0-1 1-2 1-3"/>',
    'parking': '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M9.5 17V7h3.5a3 3 0 0 1 0 6H9.5"/>',
    'tv': '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    'washer': '<rect x="4" y="2" width="16" height="20" rx="2.5"/><circle cx="12" cy="13" r="4.5"/><path d="M7.5 5.5h2"/>',
    'mic': '<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8"/>',
    'tiles': '<rect x="3" y="6" width="8" height="13" rx="1.5"/><rect x="13" y="4" width="8" height="13" rx="1.5"/><circle cx="7" cy="12.5" r="1.6"/><path d="M15.5 8.5h3M15.5 12.5h3"/>',
    'fire': '<path d="M12 2c1 4 6 6 6 12a6 6 0 0 1-12 0c0-3 2-4.5 2-7 2 1 3 3 3 5 1-2 1.5-5 1-10z"/>',
    'desk': '<path d="M2 9h20M4 9v11M20 9v11M4 14h7M14 9V5h5v4"/>',
    'slide': '<path d="M4 21V7l3-3 3 3v14M4 11h6M10 9c4 0 4 12 10 12M4 16h6"/>',
    'cue': '<circle cx="9" cy="15" r="6"/><circle cx="9" cy="15" r="2.4"/><path d="M14 10 21 3"/>',
    'book': '<path d="M3 5h6a3 3 0 0 1 3 3v12a2.5 2.5 0 0 0-2.5-2.5H3zM21 5h-6a3 3 0 0 0-3 3v12a2.5 2.5 0 0 1 2.5-2.5H21z"/>',
    'sofa': '<path d="M5 11V8a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v3M3 12a2 2 0 0 1 4 0v2h10v-2a2 2 0 0 1 4 0v5H3zM5 17v3M19 17v3"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    'rail': '<path d="M3 11h18M3 20h18M5 11v9M9.5 11v9M14.5 11v9M19 11v9M7 11V5h10v6"/>',
    'hanger': '<path d="M10 6a2 2 0 1 1 2 2v2L3 17h18l-9-7"/>',
    'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    'foos': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M12 5v14M8 9v6M16 9v6"/><circle cx="12" cy="12" r="1.6"/>',
    'wind': '<path d="M3 8h10a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7"/>',
    'iron': '<path d="M3 18h16a2 2 0 0 0 2-2v-3a5 5 0 0 0-5-5H9M3 18l2-6h15M8 8V6h5"/>',
    'key': '<circle cx="8" cy="15" r="4.5"/><path d="M11.2 11.8 20 3M16 7l3 3M14 9l2 2"/>',
    'check': '<path d="m4 12.5 5 5L20 6.5"/>',
    'users': '<circle cx="9" cy="8" r="3.6"/><path d="M2.5 20.5a6.5 6.5 0 0 1 13 0M16 4.6a3.6 3.6 0 0 1 0 6.8M21.5 20.5a6.5 6.5 0 0 0-4-6"/>',
    'bed': '<path d="M3 19V6M3 15h18v4M21 19v-6a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11.5" r="2"/>',
    'bath': '<path d="M3 12h18v2a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6zM6 12V6a2 2 0 0 1 4 0M6 20l-1 2M18 20l1 2"/>',
    'pin': '<path d="M12 21.5s7-6.2 7-11.5a7 7 0 0 0-14 0c0 5.3 7 11.5 7 11.5z"/><circle cx="12" cy="10" r="2.6"/>',
    'car': '<path d="M3 16v-4l2.2-5h13.6L21 12v4zM3 16v3h3v-3M18 16v3h3v-3M3 12h18"/><circle cx="7.5" cy="14" r=".6"/><circle cx="16.5" cy="14" r=".6"/>',
    'walk': '<circle cx="13" cy="4" r="2"/><path d="M9 21l2.5-6.5L15 17v4M7 12l2.5-3.5 4 1 3 3M11.5 14.5 13.5 9"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.2 2"/>',
    'cal': '<rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'no': '<circle cx="12" cy="12" r="9"/><path d="m5.7 5.7 12.6 12.6"/>',
    'shield': '<path d="M12 3 20 6v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    'chat': '<path d="M20.5 12a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.2-4.6A8.5 8.5 0 1 1 20.5 12z"/>',
    'home': '<path d="M3 11 12 3l9 8M5 9.5V21h5v-6h4v6h5V9.5"/>',
    'grid': '<rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'party': '<path d="M3 21 8 8l8 8zM14 3c0 2 1 3 3 3M19 9h2M17 3l1-1M12 6l1-2"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'x': '<path d="M6 6l12 12M18 6 6 18"/>',
    'left': '<path d="m15 5-7 7 7 7"/>',
    'right': '<path d="m9 5 7 7-7 7"/>',
}


def ico(name, size=22, cls='i'):
    return ('<svg class="%s" viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, size, size, ICONS[name]))


AMEN_ICON = [('wi-fi', 'wifi'), ('air con', 'snow'), ('kitchen', 'pot'), ('parking', 'parking'), ('smart tv', 'tv'), ('washer', 'washer'),
             ('karaoke', 'mic'), ('mahjong', 'tiles'), ('bbq', 'fire'), ('workspace', 'desk'), ('playground', 'slide'), ('pool table', 'cue'),
             ('games room', 'cue'), ('study', 'book'), ('family room', 'sofa'), ('rooftop', 'sun'), ('balcony', 'rail'), ('dressing', 'hanger'),
             ('dartboard', 'target'), ('foosball', 'foos'), ('hair dryer', 'wind'), ('iron', 'iron'), ('check-in', 'key'), ('tv', 'tv')]


def amen_icon(a):
    low = a.lower()
    for k, v in AMEN_ICON:
        if k in low:
            return v
    return 'check'


def pimg(f, alt=None, cls='', eager=False, sizes='(min-width:1024px) 50vw, 100vw', thumb=True, lazy=True):
    """<img> for a local photo with real width/height, alt, srcset (480px thumb + original) and lazy loading."""
    w, h = dims(f)
    alt = _alt_for(f) if alt is None else alt
    srcset = ''
    if HAS_THUMB and thumb:
        srcset = ' srcset="{R}thumb/%s 480w, {R}img/%s %dw" sizes="%s"' % (f, f, w, sizes)
    load = ' fetchpriority="high"' if eager else (' loading="lazy"' if lazy else '')
    return ('<img src="{R}img/%s"%s alt="%s" width="%d" height="%d"%s decoding="async"%s>'
            % (f, srcset, e(alt), w, h, load, (' class="%s"' % cls) if cls else ''))


def faq_block(items, h2='Frequently asked questions', intro='', cta=''):
    body = ''.join('<details class="faq"><summary><span>%s</span>%s</summary><div class="faq-a"><p>%s</p></div></details>' % (e(q), ico('x', 18, 'i pm'), e(a)) for q, a in items)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage',
          'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}
    head = ('<h2>%s</h2>' % e(h2)) if h2 else ''
    return '<div class="faqs">%s%s<div class="faq-list">%s</div>%s</div>' % (head, intro, body, cta), ld


def crumbs_ld(crumbs):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + p} for i, (n, p) in enumerate(crumbs)]}


def crumbs_html(crumbs):
    out = []
    for i, (n, p) in enumerate(crumbs):
        out.append('<span aria-current="page">%s</span>' % e(n) if i == len(crumbs) - 1 else '<a href="{R}%s">%s</a>' % (p, e(n)))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % '<span class="sep">/</span>'.join(out)


def addr_ld(h):
    return {'@type': 'PostalAddress', 'streetAddress': h['street'], 'addressLocality': h['locality'],
            'addressRegion': h['region'], 'postalCode': h['postal'], 'addressCountry': 'MY'}


def org_ld():
    return {'@context': 'https://schema.org', '@type': 'LodgingBusiness', '@id': BASE + '#org', 'name': NAME,
            'url': BASE, 'telephone': WA_SHOW, 'slogan': TAGLINE, 'image': abs_img(HERO_IMG),
            'logo': BASE + 'icon-512.png', 'priceRange': 'RM 500 per night', 'currenciesAccepted': 'MYR',
            'areaServed': 'Johor Bahru, Malaysia',
            'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'VacationRental', 'name': HOUSES[k]['full'], 'url': BASE + 'stays/%s/' % HOUSES[k]['slug']}} for k in ORDER]}


def house_ld(h):
    ld = {'@context': 'https://schema.org', '@type': 'VacationRental', '@id': BASE + 'stays/%s/#rental' % h['slug'],
          'name': h['full'], 'url': BASE + 'stays/%s/' % h['slug'], 'description': h['card'],
          'image': [abs_img(f) for f in BENTO[h['key']]] + [abs_img(CARD_IMG[h['key']][0])], 'telephone': WA_SHOW,
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
WA_HELLO = wa_msg()


def brand_mark():
    return ('<svg class="mark" viewBox="0 0 32 32" width="32" height="32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0a1f38"/>'
            '<path d="M6 15.5 16 7l10 8.5h-2.6V25H8.6v-9.5z" fill="#f7f8f9"/><rect x="13.6" y="17.5" width="4.8" height="7.5" rx="1" fill="#e8a33d"/></svg>')


def header_html(k=None):
    nav = ''.join('<a href="{R}%s">%s</a>' % (p, n) for n, p in NAV)
    return ('<header class="hdr" id="top"><div class="wrap hdr-in"><a class="brand" href="{R}" aria-label="JBStaycation home">%s<span>JB<b>Staycation</b></span></a>'
            '<nav class="nav" id="mainnav" aria-label="Main">%s</nav>'
            '<div class="hdr-act">%s<button class="mtog" type="button" aria-expanded="false" aria-controls="mainnav" aria-label="Open menu">%s%s</button></div>'
            '</div></header>' % (brand_mark(), nav, wa_btn('WhatsApp', wa_msg(k), 'header', 'btn btn-wa btn-sm hdr-wa', aria='Message us on WhatsApp'), ico('menu', 24, 'i i-open'), ico('x', 24, 'i i-close')))


def footer_html():
    adds = ''.join('<li><a href="{R}stays/%s/">%s</a><span>%s</span></li>' % (HOUSES[k]['slug'], e(HOUSES[k]['name']), e(HOUSES[k]['addr'])) for k in ORDER)
    links = ''.join('<a href="{R}%s">%s</a>' % (p, n) for n, p in NAV[:5] + [('About', 'about/'), ('Contact', 'contact/'), ('Privacy', 'privacy/')])
    return ('<footer class="ftr"><div class="wrap"><div class="ftr-top"><div class="ftr-lead"><p class="ftr-tag">%s</p>'
            '<p class="ftr-sub">Private holiday houses in Johor Bahru for Singapore families and groups.</p>%s</div>'
            '<div><p class="fh">Our houses</p><ul class="adds">%s</ul></div>'
            '<div><p class="fh">Explore</p><div class="flinks">%s</div></div></div>'
            '<p class="wordmark" aria-hidden="true">JB<span>Staycation</span></p>'
            '<div class="fsmall"><span>Prices in RM. Bookings by WhatsApp only: %s.</span> <a href="https://pageonesingapore.com/" rel="noopener">Website by Page One Singapore</a></div></div></footer>'
            % (e(TAGLINE), wa_btn('WhatsApp %s' % WA_SHOW, WA_HELLO, 'footer'), adds, links, WA_SHOW))


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


UI_JS = r"""/* JBStaycation UI: header, menu, reveal on scroll, carousels, lightbox. Content is fully visible and usable without JS. */
(function(){
var d=document,b=d.body,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var hdr=d.querySelector('.hdr'),tog=d.querySelector('.mtog');
function sc(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>24)}sc();window.addEventListener('scroll',sc,{passive:true});
if(tog)tog.addEventListener('click',function(){var o=!hdr.classList.contains('open');hdr.classList.toggle('open',o);tog.setAttribute('aria-expanded',o);tog.setAttribute('aria-label',o?'Close menu':'Open menu')});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&hdr&&hdr.classList.contains('open')){hdr.classList.remove('open');tog.setAttribute('aria-expanded','false')}});
var els=[].slice.call(d.querySelectorAll('.rv'));
setTimeout(function(){els.forEach(function(x){x.classList.add('in')})},1500);
if('IntersectionObserver' in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(x){io.observe(x)})}else{els.forEach(function(x){x.classList.add('in')})}
/* carousels: auto-slide (keeps going while the page scrolls), pause only while held or dragged, restart 2 s after release */
d.querySelectorAll('[data-carousel]').forEach(function(c){
var t=c.querySelector('.track'),held=false,rt=null,drag=null,moved=false,cnt=c.querySelector('.cnt'),sl=t.querySelectorAll('.slide'),n=sl.length,chips=[].slice.call(c.querySelectorAll('.rchips button'));
function idx(){return Math.round(t.scrollLeft/Math.max(1,t.clientWidth))}
function upd(){var i=Math.min(idx(),n-1);if(cnt)cnt.textContent=(i+1)+' / '+n;if(chips.length&&sl[i]){var r=sl[i].getAttribute('data-room');chips.forEach(function(b){var on=b.getAttribute('data-room')===r;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);if(on){var p=b.parentNode;p.scrollTo({left:b.offsetLeft-12,behavior:'auto'})}})}}
chips.forEach(function(b){b.addEventListener('click',function(){hold();var i=+b.getAttribute('data-i');t.scrollTo({left:i*t.clientWidth,behavior:rm?'auto':'smooth'});release()})});
function step(dir){var w=t.clientWidth,max=t.scrollWidth-w;if(max<=4)return;var x=t.scrollLeft+dir*w;if(x>max+4&&dir>0||t.scrollLeft>=max-4&&dir>0)x=0;else if(x<-4)x=max;t.scrollTo({left:x,behavior:rm?'auto':'smooth'})}
function hold(){held=true;clearTimeout(rt)}
function release(){clearTimeout(rt);rt=setTimeout(function(){held=false},2000)}
var nx=c.querySelector('.next'),pv=c.querySelector('.prev');
if(nx)nx.addEventListener('click',function(){hold();step(1);release()});
if(pv)pv.addEventListener('click',function(){hold();step(-1);release()});
t.addEventListener('scroll',function(){upd()},{passive:true});
t.addEventListener('touchstart',hold,{passive:true});t.addEventListener('touchend',release,{passive:true});t.addEventListener('touchcancel',release,{passive:true});
t.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&t.scrollWidth>t.clientWidth+4){hold();moved=false;drag={x:e.clientX,l:t.scrollLeft};t.classList.add('drag')}});
t.addEventListener('pointermove',function(e){if(drag){var dx=e.clientX-drag.x;if(Math.abs(dx)>5)moved=true;t.scrollLeft=drag.l-dx}});
function up(){if(drag){drag=null;t.classList.remove('drag');var w=t.clientWidth;t.scrollTo({left:Math.round(t.scrollLeft/w)*w,behavior:'smooth'});release()}}
t.addEventListener('pointerup',up);t.addEventListener('pointercancel',up);t.addEventListener('pointerleave',up);
t.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
t.addEventListener('focusin',hold);t.addEventListener('focusout',release);
if(!rm)setInterval(function(){if(!held&&!d.hidden)step(1)},4200);
upd();
});
/* lightbox: every [data-lb] link on the page, in page order */
var items=[].slice.call(d.querySelectorAll('[data-lb]'));
if(items.length){
var lb=d.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Photo viewer');lb.hidden=true;
lb.innerHTML='<div class="lb-top"><span class="lb-n"></span><button type="button" class="lb-x" aria-label="Close photo viewer"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>'+
'<figure class="lb-fig"><img alt="" decoding="async"><figcaption></figcaption></figure>'+
'<button type="button" class="lb-p" aria-label="Previous photo"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m15 5-7 7 7 7"/></svg></button>'+
'<button type="button" class="lb-nx" aria-label="Next photo"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m9 5 7 7-7 7"/></svg></button>';
b.appendChild(lb);
var im=lb.querySelector('img'),cap=lb.querySelector('figcaption'),num=lb.querySelector('.lb-n'),cur=0,last=null;
function show(i){cur=(i+items.length)%items.length;var a=items[cur],g=a.querySelector('img');im.src=a.getAttribute('href');im.alt=g?g.alt:'';cap.textContent=a.getAttribute('data-cap')||(g?g.alt:'');num.textContent=(cur+1)+' / '+items.length;
var p=new Image();p.src=items[(cur+1)%items.length].getAttribute('href')}
function open(i){last=d.activeElement;lb.hidden=false;b.classList.add('lb-on');show(i);lb.querySelector('.lb-x').focus()}
function close(){lb.hidden=true;b.classList.remove('lb-on');im.removeAttribute('src');if(last)last.focus()}
items.forEach(function(a,i){a.addEventListener('click',function(e){if(e.defaultPrevented)return;e.preventDefault();open(i)})});
d.querySelectorAll('[data-lb-open]').forEach(function(x){x.addEventListener('click',function(e){e.preventDefault();open(0)})});
lb.querySelector('.lb-x').addEventListener('click',close);lb.querySelector('.lb-p').addEventListener('click',function(){show(cur-1)});lb.querySelector('.lb-nx').addEventListener('click',function(){show(cur+1)});
lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-fig'))close()});
d.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowRight')show(cur+1);else if(e.key==='ArrowLeft')show(cur-1);else if(e.key==='Tab'){var f=[].slice.call(lb.querySelectorAll('button'));var k=f.indexOf(d.activeElement);e.preventDefault();f[(k+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)show(cur+(dx<0?1:-1));sx=null},{passive:true});
}
})();
"""

CSS = r"""
:root{--page:#f7f8f9;--surface:#fff;--ink:#0a1f38;--ink-soft:#45566b;--ink-muted:#6b7a8c;--line:#dfe4e9;--line-strong:#c3ccd6;--panel:#10304f;--panel-deep:#0a1f38;--amber:#e8a33d;--amber-deep:#a86d15;--amber-soft:#fbf1e0;--sky:#e9eff5;
--r:12px;--r-lg:18px;--ease:cubic-bezier(.23,1,.32,1);--sh:0 1px 2px rgba(10,31,56,.05),0 10px 30px -12px rgba(10,31,56,.22);--sh-lg:0 2px 4px rgba(10,31,56,.06),0 28px 60px -24px rgba(10,31,56,.38);--hh:64px;
--font:"Geist",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@media(min-width:1024px){:root{--hh:76px}}
*{box-sizing:border-box}html{overflow-x:clip;-webkit-text-size-adjust:100%;scroll-padding-top:calc(var(--hh) + 16px)}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{margin:0;background:var(--page);color:var(--ink);font:400 1.0625rem/1.65 var(--font);font-feature-settings:"ss01","ss02";overflow-x:hidden;-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:var(--ink);text-decoration-color:var(--amber);text-decoration-thickness:1.5px;text-underline-offset:3px;transition:color .2s}a:hover{color:var(--amber-deep)}
h1,h2,h3{line-height:1.12;font-weight:600;letter-spacing:-.025em;margin:0 0 .5em;color:inherit;text-wrap:balance}
h1{font-size:clamp(2rem,5.6vw,3.5rem)}h2{font-size:clamp(1.75rem,4.4vw,2.9rem)}h3{font-size:1.3rem;letter-spacing:-.015em}
p{margin:0 0 1em}p,li{text-wrap:pretty}
.wrap{max-width:1200px;margin:0 auto;padding:0 16px}@media(min-width:768px){.wrap{padding:0 clamp(24px,4vw,48px)}}
.sec{padding:36px 0}.sec-tight{padding:36px 0}@media(min-width:768px){.sec{padding:clamp(64px,10vw,120px) 0}.sec-tight{padding:clamp(48px,7vw,80px) 0}}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:.8125rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--amber-deep);margin:0 0 14px}
.eyebrow::before{content:"";width:22px;height:1.5px;background:currentColor}
.lead{font-size:clamp(1.0625rem,1.6vw,1.25rem);color:var(--ink-soft);max-width:60ch}
.muted{color:var(--ink-soft)}.note{font-size:.9375rem;color:var(--ink-muted)}
.sec-head{display:grid;gap:8px;margin-bottom:clamp(28px,4vw,48px)}@media(min-width:900px){.sec-head.split{grid-template-columns:1.1fr 1fr;align-items:end;gap:48px}.sec-head.split .lead{margin:0}}
.i{flex:none}
/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:12px 24px;border-radius:999px;font:600 1rem/1.2 var(--font);text-decoration:none;border:1.5px solid transparent;cursor:pointer;transition:transform .25s var(--ease),box-shadow .25s var(--ease),background .25s,color .25s,border-color .25s;white-space:nowrap}
.btn:hover{transform:translateY(-2px)}.btn:active{transform:translateY(0) scale(.98)}
.btn-wa{background:var(--amber);color:var(--ink);box-shadow:0 8px 24px -8px rgba(232,163,61,.7)}.btn-wa:hover{background:#f0b252;color:var(--ink)}
.btn-ghost{border-color:rgba(255,255,255,.55);color:#fff;background:rgba(255,255,255,.06);backdrop-filter:blur(6px)}.btn-ghost:hover{background:#fff;color:var(--ink)}
.btn-line{border-color:var(--line-strong);color:var(--ink);background:var(--surface)}.btn-line:hover{border-color:var(--ink);color:var(--ink)}
.btn-sm{min-height:44px;padding:8px 16px;font-size:.9375rem}
.link{display:inline-flex;align-items:center;gap:8px;font-weight:600;text-decoration:none;color:var(--ink);min-height:44px}.link .i{transition:transform .25s var(--ease)}.link:hover .i{transform:translateX(4px)}
/* header */
.hdr{position:fixed;inset:0 0 auto;z-index:50;height:var(--hh);color:var(--ink);background:rgba(247,248,249,.9);-webkit-backdrop-filter:saturate(1.4) blur(18px);backdrop-filter:saturate(1.4) blur(18px);border-bottom:1px solid var(--line);transition:background .3s,color .3s,border-color .3s}
.hdr-in{height:100%;display:flex;align-items:center;gap:16px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit;margin-right:auto;min-height:44px}.brand span{font-size:1.2rem;font-weight:500;letter-spacing:-.02em}.brand b{font-weight:700}
.nav{display:none}.nav a{color:inherit;text-decoration:none;font-weight:500;font-size:.98rem;padding:10px 12px;border-radius:8px;transition:background .2s,color .2s}.nav a:hover{background:rgba(10,31,56,.06);color:inherit}
.hdr-act{display:flex;align-items:center;gap:8px}
.mtog{width:44px;height:44px;display:grid;place-items:center;border:0;background:transparent;color:inherit;border-radius:10px;cursor:pointer;padding:0}.mtog .i-close{display:none}
.hdr.open .mtog .i-open{display:none}.hdr.open .mtog .i-close{display:block}
@media(max-width:1023px){.hdr .hdr-wa{width:44px;min-width:44px;height:44px;min-height:44px;padding:0;border-radius:50%;flex:none}.hdr .hdr-wa span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}.hdr .hdr-wa .ico{width:24px;height:24px}.hdr-in{gap:8px}.hdr-act{gap:4px;flex:none}.brand{min-width:0}.brand span{white-space:nowrap}
.js .nav{position:fixed;left:0;right:0;top:var(--hh);display:flex;flex-direction:column;padding:8px 16px 24px;background:var(--page);border-bottom:1px solid var(--line);box-shadow:0 30px 40px -30px rgba(10,31,56,.35);transform:translateY(-8px);opacity:0;visibility:hidden;transition:opacity .25s var(--ease),transform .25s var(--ease),visibility .25s}
.js .nav a{font-size:1.25rem;padding:14px 4px;border-bottom:1px solid var(--line);border-radius:0;color:var(--ink)}
.hdr.open .nav{opacity:1;transform:none;visibility:visible}
html:not(.js) .nav{display:flex;position:absolute;top:var(--hh);left:0;right:0;overflow-x:auto;gap:4px;padding:6px 16px;background:var(--page);border-bottom:1px solid var(--line)}html:not(.js) .mtog{display:none}}
@media(min-width:1024px){.nav{display:flex;gap:2px;margin-right:auto}.brand{margin-right:28px}.mtog{display:none}}
.js .home .hdr:not(.scrolled):not(.open){background:transparent;border-color:transparent;color:#fff;-webkit-backdrop-filter:none;backdrop-filter:none}
.js .home .hdr:not(.scrolled):not(.open) .nav a:hover{background:rgba(255,255,255,.12)}
.js .home .hdr:not(.scrolled):not(.open) .mark rect:first-child{fill:rgba(255,255,255,.14)}
main{display:block;position:relative;z-index:1;background:var(--page)}
.inner main{padding-top:var(--hh)}
/* home hero */
.hero{position:relative;min-height:100vh;min-height:100svh;display:flex;align-items:flex-end;color:#fff;background:var(--panel-deep);overflow:hidden;isolation:isolate}
.hero-bg{position:absolute;inset:0;z-index:-2;overflow:hidden}.hero-bg img{width:100%;height:100%;object-fit:cover;object-position:58% 50%}
@media(prefers-reduced-motion:no-preference){.hero-bg img{animation:kb 22s var(--ease) both}@keyframes kb{from{transform:scale(1.14)}to{transform:scale(1.02)}}}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(10,31,56,.62) 0,rgba(10,31,56,.12) 26%,rgba(10,31,56,.25) 48%,rgba(10,31,56,.86) 76%,rgba(10,31,56,.97) 100%)}
@media(min-width:900px){.hero::after{background:linear-gradient(180deg,rgba(10,31,56,.55) 0,rgba(10,31,56,0) 22%),linear-gradient(90deg,rgba(10,31,56,.9) 0,rgba(10,31,56,.6) 40%,rgba(10,31,56,.05) 75%),linear-gradient(0deg,rgba(10,31,56,.7) 0,rgba(10,31,56,0) 40%)}}
.hero-in{width:100%;padding-top:calc(var(--hh) + 48px);padding-bottom:28px}
.hero h1{margin:0 0 18px}
.hero .kick{display:block;font-size:.8125rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);margin-bottom:18px;max-width:none;line-height:1.5}
.hero .display{display:block;font-size:clamp(2.4rem,7.2vw,5rem);line-height:1.02;letter-spacing:-.04em;font-weight:600;max-width:11.5em;text-wrap:balance}
.hero .sub{font-size:clamp(1.0625rem,1.7vw,1.25rem);color:rgba(255,255,255,.86);max-width:44ch;margin:0 0 28px}
.cta-row{display:flex;gap:12px;flex-wrap:wrap}
.facts{list-style:none;margin:36px 0 0;padding:20px 0 0;border-top:1px solid rgba(255,255,255,.2);display:grid;grid-template-columns:1fr 1fr;gap:14px 20px;font-size:.9375rem;color:rgba(255,255,255,.9)}
.facts li{display:flex;align-items:center;gap:10px;line-height:1.35}.facts .i{color:var(--amber)}
@media(min-width:900px){.facts{display:flex;flex-wrap:wrap;gap:12px 36px}.hero-in{padding-bottom:44px}}
@media(max-width:380px){.hero .btn{flex:1 1 100%}}
/* house cards */
.cards{display:grid;gap:24px}@media(min-width:800px){.cards{grid-template-columns:1fr 1fr;gap:32px}}
.hcard{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;box-shadow:var(--sh);display:flex;flex-direction:column;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.hcard:hover{transform:translateY(-6px);box-shadow:var(--sh-lg)}
.hcard .ph{display:block;aspect-ratio:4/3;overflow:hidden;background:var(--sky);position:relative}
.ph img,.strip img,.acard .ph img,.mosaic img{width:100%;height:100%;object-fit:cover;transition:transform .7s var(--ease)}
.hcard:hover .ph img{transform:scale(1.05)}
.badge{position:absolute;left:14px;top:14px;background:rgba(255,255,255,.92);color:var(--ink);font-size:.8125rem;font-weight:600;padding:6px 12px;border-radius:999px;backdrop-filter:blur(6px)}
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px 4px 0}.strip span{aspect-ratio:4/3;overflow:hidden;border-radius:6px;background:var(--sky)}
.hcard .cb{padding:20px 20px 22px;display:flex;flex-direction:column;gap:12px;flex:1}@media(min-width:800px){.hcard .cb{padding:24px 26px 26px}}
.hcard h3{font-size:1.5rem;margin:0}.hcard h3 a{text-decoration:none;color:inherit}.hcard h3 a::after{content:"";position:absolute;inset:0;z-index:1}
.area{display:flex;align-items:center;gap:6px;color:var(--ink-soft);font-size:.9375rem;margin:0}.area .i{color:var(--amber-deep)}
.specs{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0;padding:0;list-style:none;color:var(--ink);font-size:.9375rem}.specs li{display:flex;align-items:center;gap:7px}.specs .i{color:var(--ink-soft)}
.sg{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}.sg li{display:inline-flex;align-items:center;gap:6px;background:var(--amber-soft);color:#6e4609;border-radius:999px;padding:6px 12px;font-size:.875rem;font-weight:500}
.price-row{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin-top:auto;padding-top:14px;border-top:1px solid var(--line)}
.price{margin:0;line-height:1.1}.price b{font-size:1.75rem;letter-spacing:-.03em;font-weight:700}.price small{display:block;font-size:.875rem;color:var(--ink-muted);margin-top:4px}
.go{position:relative;z-index:2;display:inline-flex;align-items:center;gap:8px;font-weight:600;color:var(--ink);text-decoration:none;min-height:44px}.hcard:hover .go .i{transform:translateX(4px)}.go .i{transition:transform .25s var(--ease)}
/* dark sections */
.dark{background:var(--panel-deep);color:#fff}.dark .eyebrow{color:var(--amber)}.dark .lead,.dark .muted{color:rgba(255,255,255,.74)}.dark a{color:#fff}
.panel{background:var(--panel)}
.pts{display:grid;gap:1px;padding:0;margin:0;list-style:none;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.12);border-radius:var(--r-lg);overflow:hidden}
@media(min-width:700px){.pts{grid-template-columns:1fr 1fr}}@media(min-width:1100px){.pts{grid-template-columns:repeat(4,1fr)}}
.pts li{background:var(--panel-deep);padding:28px 24px;display:flex;flex-direction:column;gap:10px}.pts .i{color:var(--amber);width:30px;height:30px}.pts b{font-size:1.15rem;font-weight:600;letter-spacing:-.01em}.pts span{color:rgba(255,255,255,.74);font-size:1rem}
/* steps + mosaic */
.split2{display:grid;gap:40px;align-items:center}@media(min-width:960px){.split2{grid-template-columns:1fr 1fr;gap:64px}}
.steps{list-style:none;margin:0 0 20px;padding:0;counter-reset:s;display:grid;gap:22px}
.steps li{counter-increment:s;display:grid;grid-template-columns:48px 1fr;gap:16px;align-items:start}
.steps li::before{content:counter(s,decimal-leading-zero);display:grid;place-items:center;width:48px;height:48px;border-radius:50%;border:1.5px solid var(--line-strong);font-weight:600;font-size:.95rem;color:var(--amber-deep);background:var(--surface)}
.steps b{display:block;font-size:1.1rem;margin-bottom:2px}.steps span{color:var(--ink-soft)}
.mosaic{display:grid;grid-template-columns:1.3fr 1fr;grid-template-rows:1fr 1fr;gap:10px;aspect-ratio:5/4}
.mosaic span{border-radius:var(--r);overflow:hidden;background:var(--sky)}.mosaic span:first-child{grid-row:span 2}
.mosaic span:hover img{transform:scale(1.04)}
/* quote */
.quote{margin:0 auto;max-width:900px;text-align:center}
.quote .qm{display:block;font-size:5rem;line-height:.6;color:var(--amber);font-weight:700;margin-bottom:12px}
.quote p{font-size:clamp(2rem,5.6vw,4rem);line-height:1.08;letter-spacing:-.035em;font-weight:500;margin:0 0 24px}
.quote cite{font-style:normal;color:rgba(255,255,255,.72);font-size:1rem}.quote cite b{color:#fff;font-weight:600}
/* map */
.mapcard{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:12px;box-shadow:var(--sh)}
.mapcard svg{width:100%;height:auto;display:block}.mapcard .rlist{display:none}@media(max-width:767px){.mapcard .map-w{display:none}.mapcard:not(.has-rl){display:none}.mapcard .rlist{display:grid}}.mapcard figcaption{font-size:.875rem;color:var(--ink-muted);padding:8px 8px 4px}
.routes{list-style:none;padding:0;margin:0 0 24px;display:grid;gap:12px}.routes li{display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:start}
.routes .i{width:40px;height:40px;padding:9px;border-radius:10px;background:var(--sky);color:var(--panel)}.routes b{display:block}.routes span{color:var(--ink-soft);font-size:1rem}
/* article cards */
.arts{display:grid;gap:24px}@media(min-width:760px){.arts{grid-template-columns:repeat(3,1fr)}}
.acard{position:relative;display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.acard:hover{transform:translateY(-4px);box-shadow:var(--sh-lg)}.acard:hover .ph img{transform:scale(1.05)}
.acard .ph{display:block;aspect-ratio:16/10;overflow:hidden;background:var(--sky)}
.acard .cb{padding:20px 22px 22px;display:flex;flex-direction:column;gap:10px;flex:1}.acard h3{margin:0;font-size:1.2rem}.acard h3 a{text-decoration:none;color:inherit}.acard h3 a::after{content:"";position:absolute;inset:0}
.acard p{margin:0;color:var(--ink-soft);font-size:1rem}.acard .go{margin-top:auto}
.tag{font-size:.8125rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-deep)}
/* faq */
.faqgrid{display:grid;gap:32px}.faqgrid .faqs h2{display:none}@media(min-width:960px){.faqgrid{grid-template-columns:.8fr 1.2fr;gap:64px}}
.faq{border-bottom:1px solid var(--line)}.faq:first-child{border-top:1px solid var(--line)}
.faq summary{cursor:pointer;font-weight:600;font-size:1.0625rem;padding:20px 0;min-height:44px;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px}
.faq summary::-webkit-details-marker{display:none}.faq summary:hover{color:var(--amber-deep)}
.faq .pm{transform:rotate(45deg);transition:transform .3s var(--ease);color:var(--amber-deep);width:22px;height:22px;padding:2px;border-radius:50%;border:1.5px solid currentColor}.faq[open] .pm{transform:rotate(0)}
.faq-a p{margin:0 0 20px;color:var(--ink-soft);max-width:65ch}
/* cta band */
.band{position:relative;isolation:isolate;color:#fff;text-align:center;overflow:hidden;border-radius:0}
.band .bg{position:absolute;inset:0;z-index:-2}.band .bg img{width:100%;height:100%;object-fit:cover}
.band::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(10,31,56,.78),rgba(10,31,56,.9))}
.band h2{max-width:18ch;margin:0 auto 14px}.band p{color:rgba(255,255,255,.82);max-width:46ch;margin:0 auto 28px;font-size:1.125rem}
/* inner page top */
.ptop{padding:clamp(28px,5vw,56px) 0 0}
.crumbs{font-size:.9375rem;color:var(--ink-muted);margin-bottom:18px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}.crumbs a{color:var(--ink-soft);text-decoration:none;padding:6px 0}.crumbs a:hover{color:var(--amber-deep)}.crumbs .sep{color:var(--line-strong)}
.ptop h1{max-width:22ch}.ptop .lead{margin-bottom:0}
.pphoto{margin-top:clamp(24px,4vw,40px);border-radius:var(--r-lg);overflow:hidden;aspect-ratio:16/10;background:var(--sky)}@media(min-width:800px){.pphoto{aspect-ratio:21/8}}.pphoto img{width:100%;height:100%;object-fit:cover}
.body{padding-block:clamp(36px,6vw,64px) clamp(64px,9vw,104px)}
.prose{max-width:760px}.prose h2{font-size:clamp(1.5rem,3.4vw,2rem);margin-top:1.6em}.prose p,.prose li{color:var(--ink-soft)}.prose li{margin-bottom:.4em}.prose b{color:var(--ink)}
.prose section:first-child h2{margin-top:0}
.answer{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--amber);padding:18px 22px;border-radius:var(--r);margin:0 0 28px;font-size:1.125rem;color:var(--ink);box-shadow:var(--sh)}
.byline{display:flex;align-items:center;gap:8px;color:var(--ink-muted);font-size:.9375rem;margin-bottom:20px}
table{width:100%;border-collapse:collapse;background:var(--surface);font-size:1rem}th,td{padding:14px 16px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}thead th{background:var(--sky);font-size:.875rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft)}tbody th{font-weight:600}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);margin:0 0 28px;-webkit-overflow-scrolling:touch}.tw table{min-width:540px}
.src li{font-size:.9375rem}
.prose .btn{margin-top:8px}
/* house page */
.htop{padding:clamp(20px,4vw,40px) 0 0}
.htop h1{font-size:clamp(1.65rem,4.8vw,3.25rem);margin-bottom:12px}@media(max-width:599px){.hmeta{gap:6px 16px;margin-bottom:12px;font-size:.9375rem}.htop{padding-top:12px}.gal{margin-top:14px}.subnav{display:none}}
.hmeta{display:flex;flex-wrap:wrap;gap:10px 22px;margin:0 0 18px;padding:0;list-style:none;color:var(--ink-soft);font-size:1rem}.hmeta li{display:flex;align-items:center;gap:8px}.hmeta .i{color:var(--amber-deep)}
.subnav{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -16px;padding:0 16px 4px}.subnav::-webkit-scrollbar{display:none}
.subnav a{flex:none;display:inline-flex;align-items:center;min-height:44px;padding:8px 16px;border:1px solid var(--line);border-radius:999px;background:var(--surface);text-decoration:none;font-weight:500;font-size:.9375rem;color:var(--ink);transition:border-color .2s,background .2s}.subnav a:hover{border-color:var(--ink)}
@media(min-width:768px){.subnav{margin:0;padding:0}}
.gal{position:relative;margin-top:20px}
.gal .track{list-style:none;margin:0 -16px;padding:0;display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;cursor:grab;overscroll-behavior-x:contain}.gal .track::-webkit-scrollbar{display:none}.gal .track.drag{cursor:grabbing;scroll-snap-type:none}
.gal .slide{flex:0 0 100%;scroll-snap-align:center;aspect-ratio:4/3;background:var(--sky)}
.gal .slide a{display:block;height:100%;overflow:hidden}.gal .slide img{width:100%;height:100%;object-fit:cover;-webkit-user-drag:none;user-select:none;transition:transform .6s var(--ease),filter .3s}
.cbtn{position:absolute;top:50%;transform:translateY(-50%);width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.92);color:var(--ink);cursor:pointer;box-shadow:0 4px 14px rgba(10,31,56,.25);display:grid;place-items:center;padding:0;z-index:2}.prev{left:8px}.next{right:8px}
.cnt{position:absolute;left:12px;bottom:12px;background:rgba(10,31,56,.72);color:#fff;font-size:.875rem;font-weight:500;padding:5px 11px;border-radius:999px;backdrop-filter:blur(6px)}
.gal-all{position:absolute;right:12px;bottom:12px;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 16px;border-radius:999px;background:#fff;color:var(--ink);font:600 .9375rem var(--font);text-decoration:none;box-shadow:0 6px 18px rgba(10,31,56,.25);border:0;cursor:pointer;z-index:2}
.gal-all:hover{color:var(--ink);background:var(--amber)}
@media(min-width:768px){.gal .track{margin:0;display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:8px;height:clamp(380px,44vw,560px);border-radius:var(--r-lg);overflow:hidden;cursor:default}
.gal .slide{aspect-ratio:auto;min-height:0}.gal .slide:first-child{grid-row:span 2}.gal .slide a:hover img{transform:scale(1.04);filter:brightness(1.05)}.gal .cbtn,.gal .cnt{display:none}.gal .gal-all{right:16px;bottom:16px}}
.hlay{display:grid;grid-template-columns:minmax(0,1fr);gap:40px;padding-block:clamp(32px,5vw,56px) clamp(64px,9vw,104px)}
@media(min-width:1024px){.hlay{grid-template-columns:minmax(0,1fr) 360px;gap:64px;align-items:start}}
.hmain>section{padding:clamp(32px,5vw,48px) 0;border-top:1px solid var(--line)}.hmain>section:first-child{border-top:0;padding-top:0}
.hmain h2{font-size:clamp(1.6rem,3.4vw,2.2rem)}
.hmain .intro p{color:var(--ink-soft);font-size:1.0625rem}.hmain .htag{font-size:clamp(1.35rem,2.6vw,1.75rem);margin-bottom:20px;max-width:28ch}.hmain .intro ul+p{font-size:clamp(1.15rem,1.8vw,1.3rem);color:var(--ink)}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 28px;padding:0;list-style:none}@media(min-width:700px){.stats{grid-template-columns:repeat(4,1fr)}}
.stats li{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;display:flex;flex-direction:column;gap:4px}.stats .i{color:var(--amber-deep);margin-bottom:4px}
.stats small{font-size:.8125rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-muted)}.stats b{font-size:1.0625rem;font-weight:600;line-height:1.3}
.amen{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0;padding:0;list-style:none}@media(min-width:700px){.amen{grid-template-columns:repeat(3,1fr)}}
.amen li{display:flex;align-items:center;gap:12px;padding:14px;border-radius:var(--r);background:var(--surface);border:1px solid var(--line);font-size:1rem;line-height:1.3}.amen .i{color:var(--panel);width:26px;height:26px}
.room{margin-top:36px}.room:first-of-type{margin-top:8px}
.room-h{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px}.room-h h3{margin:0;font-size:1.35rem}.room-h span{color:var(--ink-muted);font-size:.9375rem}
.rg{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0}@media(min-width:700px){.rg{grid-template-columns:repeat(3,1fr)}}
.rg figure{margin:0;display:flex;flex-direction:column;position:relative;min-width:0}.rg a{display:block;aspect-ratio:4/3;overflow:hidden;border-radius:10px;background:var(--sky)}.rg img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease)}.rg a:hover img{transform:scale(1.05)}
.rg figcaption{position:absolute;left:0;right:0;bottom:0;padding:28px 14px 12px;border-radius:0 0 10px 10px;background:linear-gradient(0deg,rgba(10,31,56,.82),rgba(10,31,56,0));color:#fff;font-size:.9375rem;font-weight:500;line-height:1.3;pointer-events:none}
.rg figure.sm2{grid-column:span 2}.rg figure.sm2 a{aspect-ratio:8/3}
@media(min-width:700px){.rg figure.sm2{grid-column:auto}.rg figure.sm2 a{aspect-ratio:4/3}.rg figure.sd2{grid-column:span 2}.rg figure.sd2 a{aspect-ratio:8/3}.rg figure.sd3{grid-column:span 3}.rg figure.sd3 a{aspect-ratio:4/1}}
.rg figure:first-child{grid-column:span 2}@media(min-width:700px){.rg figure:first-child{grid-row:span 2}.rg figure:first-child a{aspect-ratio:auto;flex:1}}
.rg.n1 figure:first-child{grid-column:1/-1;grid-row:auto}.rg.n1 figure:first-child a{aspect-ratio:16/9}
.rg.n2 figure:first-child{grid-row:auto}.rg.n2 figure:first-child a{aspect-ratio:4/3;flex:none}@media(min-width:700px){.rg.n2{grid-template-columns:2fr 1fr}.rg.n2 figure:first-child{grid-column:auto}}
.rules{list-style:none;margin:0;padding:0;display:grid;gap:10px}@media(min-width:700px){.rules{grid-template-columns:1fr 1fr}}
.rules li{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);color:var(--ink)}.rules .i{color:var(--amber-deep);margin-top:1px}.rules.one{grid-template-columns:1fr}
.near{list-style:none;margin:0 0 12px;padding:0;border:1px solid var(--line);border-radius:var(--r);background:var(--surface);overflow:hidden}
.near li{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 18px;border-top:1px solid var(--line)}.near li:first-child{border-top:0}.near li span{display:flex;align-items:center;gap:10px}.near .i{color:var(--ink-muted)}.near b{white-space:nowrap;font-weight:600}
.addr{display:flex;gap:10px;align-items:flex-start;color:var(--ink);margin-bottom:18px}.addr .i{color:var(--amber-deep);margin-top:2px}
.side{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;box-shadow:var(--sh-lg)}
@media(min-width:1024px){.side{position:sticky;top:calc(var(--hh) + 24px)}}
.side .price b{font-size:2.25rem}.side .price small{font-size:1rem;display:inline;margin-left:4px}
.side ul{list-style:none;margin:18px 0;padding:16px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);display:grid;gap:10px}.side li{display:flex;gap:10px;align-items:center;font-size:1rem}.side li .i{color:var(--ink-soft)}
.side .btn{width:100%}.side .note{margin:12px 0 0;text-align:center}
.ocard{display:grid;grid-template-columns:120px 1fr;gap:16px;align-items:center;padding:12px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);text-decoration:none;color:var(--ink);transition:transform .3s var(--ease),box-shadow .3s var(--ease)}
.ocard:hover{transform:translateY(-3px);box-shadow:var(--sh-lg);color:var(--ink)}.ocard span.ph{display:block;aspect-ratio:1;border-radius:10px;overflow:hidden}.ocard img{width:100%;height:100%;object-fit:cover}
.ocard b{display:block;font-size:1.15rem;letter-spacing:-.01em}.ocard small{display:block;color:var(--ink-soft);font-size:.9375rem}
@media(min-width:600px){.ocard{grid-template-columns:200px 1fr;padding:14px}.ocard span.ph{aspect-ratio:4/3}}
.stick{position:fixed;left:0;right:0;bottom:0;z-index:40;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.94);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:12px;box-shadow:0 -10px 30px -18px rgba(10,31,56,.35)}
.stick .price b{font-size:1.25rem}.stick .price small{font-size:.875rem;margin-top:2px}.stick .btn{min-height:48px;padding:10px 18px}
.has-stick{padding-bottom:76px}@media(min-width:1024px){.stick{display:none}.has-stick{padding-bottom:0}}
.lb-on .stick{display:none}
.after-gal,.after-faq{margin:20px 0 0}.after-faq .btn,.after-gal .btn{width:100%}@media(min-width:600px){.after-faq .btn,.after-gal .btn{width:auto}}
.hcard .card-cta{width:100%;margin-top:6px}.nf .btn{margin-top:8px}
/* lightbox */
.lb{position:fixed;inset:0;z-index:100;background:#061221;display:flex;align-items:center;justify-content:center;color:#fff}
.lb[hidden]{display:none}.lb-on{overflow:hidden}
.lb-top{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;align-items:center;padding:10px 12px 10px 20px;z-index:2}
.lb-n{font-size:.9375rem;color:rgba(255,255,255,.8)}
.lb button{width:48px;height:48px;border-radius:50%;border:0;background:rgba(255,255,255,.1);color:#fff;display:grid;place-items:center;cursor:pointer;transition:background .2s}.lb button:hover{background:rgba(255,255,255,.22)}
.lb-p,.lb-nx{position:absolute;top:50%;transform:translateY(-50%);z-index:2}.lb-p{left:12px}.lb-nx{right:12px}
.lb-fig{margin:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:64px 0 24px}
.lb-fig img{max-width:min(100%,1400px);max-height:calc(100% - 48px);width:auto;height:auto;object-fit:contain}
.lb-fig figcaption{padding:14px 20px 0;text-align:center;color:rgba(255,255,255,.85);font-size:1rem}
@media(min-width:768px){.lb-fig{padding:72px 80px 28px}}
@media(max-width:767px){.lb-p,.lb-nx{top:auto;bottom:16px;transform:none}.lb-fig{padding-bottom:80px}}
/* footer (dark curtain) */
.ftr{background:var(--panel-deep);color:rgba(255,255,255,.78);padding:clamp(56px,8vw,96px) 0 28px;position:relative;z-index:0}
.ftr a{color:#fff;text-decoration:none}.ftr a:hover{color:var(--amber)}.ftr .btn-wa{color:var(--ink)}.ftr .btn-wa:hover{color:var(--ink)}
.ftr-top{display:grid;gap:40px}@media(min-width:900px){.ftr-top{grid-template-columns:1.3fr 1.2fr .8fr;gap:56px}}
.ftr-tag{font-size:clamp(1.6rem,3vw,2.2rem);line-height:1.12;letter-spacing:-.03em;color:#fff;font-weight:600;margin:0 0 12px;max-width:16ch}
.ftr-sub{margin:0 0 24px;max-width:40ch}
.fh{font-size:.8125rem;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);font-weight:600;margin:0 0 14px}
.adds{list-style:none;margin:0;padding:0;display:grid;gap:16px}.adds li{display:flex;flex-direction:column;gap:2px;font-size:.9375rem}.adds a{font-weight:600;font-size:1.0625rem}
.flinks{display:grid;grid-template-columns:1fr 1fr;gap:2px 16px}.flinks a{padding:8px 0;min-height:44px;display:flex;align-items:center}@media(min-width:900px){.flinks{grid-template-columns:1fr}.flinks a{min-height:0;padding:5px 0}}
.wordmark{margin:clamp(40px,6vw,72px) 0 0;font-size:clamp(3rem,14.4vw,12rem);line-height:.82;letter-spacing:-.06em;font-weight:700;color:rgba(255,255,255,.1);white-space:nowrap;user-select:none}
.wordmark span{color:rgba(232,163,61,.32)}
.fsmall{margin-top:28px;padding-top:20px;border-top:1px solid rgba(255,255,255,.14);font-size:.9375rem;display:flex;gap:12px;justify-content:space-between;flex-wrap:wrap}
/* reveal */
@media(prefers-reduced-motion:no-preference) and (min-width:768px){.js .rv{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease)}.js .rv.in,.rv-all .rv{opacity:1;transform:none}}
.skip{position:absolute;left:-999px;top:8px;z-index:200}.skip:focus{left:8px;background:#fff;padding:10px 14px;border-radius:8px}
:focus-visible{outline:2.5px solid var(--amber);outline-offset:3px;border-radius:6px}
.nf{padding-block:calc(var(--hh) + 56px) 80px}

/* v4 mobile pass */
.cz{position:relative}
.hero .kick{text-transform:none;letter-spacing:0;font-size:.9375rem;font-weight:500}
.fold>summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:44px}.fold>summary::-webkit-details-marker{display:none}
.fold>summary h2{margin:0}.fold>summary .eyebrow{margin-bottom:6px}.fold .pm{transform:rotate(45deg);transition:transform .3s var(--ease);color:var(--amber-deep);width:36px;height:36px;padding:6px;border-radius:50%;border:1.5px solid currentColor;flex:none}.fold[open]>summary .pm{transform:rotate(0)}
.fold-body{padding-top:20px}.fold-body .arts{margin-bottom:12px}
.gsec{padding-top:0}
.rchips{display:none}
.rl-card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px}.rl-h{margin:0 0 8px;font-weight:700;color:var(--amber-deep)}
.rl{list-style:none;margin:0;padding:0 0 0 22px;position:relative}.rl::before{content:"";position:absolute;left:5px;top:12px;bottom:12px;width:2px;background:var(--line-strong)}
.rl li{position:relative;padding:5px 0;line-height:1.35}.rl li::before{content:"";position:absolute;left:-22px;top:12px;width:12px;height:12px;border-radius:50%;background:var(--panel);border:2px solid var(--surface)}
.rl li.t{color:var(--ink-soft);font-style:italic;padding:6px 0}.rl li.t::before{display:none}.rl li.end::before{background:var(--amber)}.rl li b,.rl li span{display:block}.rl li span{color:var(--ink-soft)}
.mapcard.has-rl{padding:12px;display:block}.mapcard .rlist{gap:10px;margin-bottom:6px}
@media(max-width:767px){
body{line-height:1.5}.steps+.after-gal{display:none}.wordmark{display:none}.pts li{padding:14px 16px}
.cz .track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;border-radius:var(--r)}.cz .track::-webkit-scrollbar{display:none}
.cz .slide{flex:0 0 100%;scroll-snap-align:center;min-width:0}
.cz .mosaic{display:flex;aspect-ratio:auto;gap:0}.cz .mosaic .slide{aspect-ratio:16/10}.hcard .cimg .ph,.hcard .cimg .strip span{aspect-ratio:3/2}
.hcard .cimg{z-index:2;border-radius:var(--r-lg) var(--r-lg) 0 0;overflow:hidden}.hcard .cimg .track{border-radius:0}.hcard .strip{display:contents}.hcard .strip span{border-radius:0}.hcard .sg{display:none}
.hcard .cb{padding:16px 16px 18px;gap:10px}.hcard h3 a{display:flex;align-items:center;min-height:44px}.cards{gap:20px}
.eyebrow,.fh{font-size:1rem;letter-spacing:.08em}
.facts li,.area,.specs li,.sg li,.note,.adds li,.src li,.hmeta,.crumbs,.near li,.stats b{font-size:1rem}
.hm{display:none}
.sec-head{margin-bottom:18px}
.hero{min-height:min(calc(100vh - 76px),680px);min-height:min(calc(100svh - 76px),680px)}
.hero-in{padding-top:calc(var(--hh) + 24px);padding-bottom:20px}
.hero h1{margin:0 0 12px}
.hero .kick{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;margin:0}
.hero .display{font-size:2.25rem;line-height:1.04}
.hero .sub{font-size:1.0625rem;line-height:1.5;margin:0 0 18px}.hero .sub .more{display:none}
.hero::after{background:linear-gradient(180deg,rgba(10,31,56,.5) 0,rgba(10,31,56,0) 22%,rgba(10,31,56,.05) 42%,rgba(10,31,56,.82) 72%,rgba(10,31,56,.96) 100%)}
.facts{margin:18px 0 0;padding-top:12px;display:flex;flex-wrap:wrap;gap:4px 22px}.facts li:nth-child(n+3){display:none}
.hero .btn{width:100%}
.pts li{padding:16px 18px;display:grid;grid-template-columns:30px 1fr;column-gap:14px;row-gap:2px}.pts .i{grid-row:span 2}
.split2{gap:28px}.steps{gap:16px;margin-bottom:16px}.steps li{grid-template-columns:40px 1fr;gap:12px}.steps li::before{width:40px;height:40px}
.after-gal{margin-top:16px}
.band p{margin-bottom:20px}
.faqgrid{gap:20px}.faq summary{padding:12px 0}.faq-a p{margin-bottom:14px}
.ftr{padding:40px 0 20px}.ftr-top{gap:28px}.wordmark{margin-top:28px}
.adds a,.fsmall a{display:inline-flex;align-items:center;min-height:44px}.adds{gap:6px}.fsmall{margin-top:20px}
.crumbs a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:0 4px}.crumbs{margin-bottom:6px;gap:0}
.note a,.prose p a,.prose li a,.muted a,.src a,.hmain p a{display:inline-block;padding:11px 10px;margin:-11px -10px}
.link{padding:0}
.subnav{display:none}.htop{padding-top:4px}.hmeta{gap:2px 16px;margin-bottom:10px}.htop h1{margin-bottom:8px}.gal{margin-top:8px}
.hlay{gap:24px;padding-top:20px}.hmain>section{padding:28px 0}.hmain>section:first-child{padding-top:0}
.rooms .room{display:contents}.rooms .room-h{display:none}.rooms .rg{display:contents}
.rooms .rg figure{flex:0 0 100%;scroll-snap-align:center;margin:0;grid-column:auto;position:relative;min-width:0}
.rooms .rg figure a{aspect-ratio:4/3!important;flex:none!important;border-radius:0}
.rooms .rg figcaption{border-radius:0}
.rooms-wrap .cnt{top:12px;bottom:auto}
.rchips{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -16px 10px;padding:0 16px 2px}.rchips::-webkit-scrollbar{display:none}
html:not(.js) .rchips{display:none}
.rchips button{flex:none;min-height:44px;padding:8px 16px;border:1px solid var(--line);border-radius:999px;background:var(--surface);font:500 1rem var(--font);color:var(--ink);cursor:pointer}.rchips button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.rooms-wrap .cz .track{border-radius:var(--r)}
}
@media(max-width:1023px){.gal+.after-gal{display:none}}
@media(min-width:768px){.cz .cbtn,.cz .cnt{display:none}}
"""


FONT_LINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..800&display=swap">')
HEAD_JS = "<script>document.documentElement.className+=' js';setTimeout(function(){document.documentElement.classList.add('rv-all')},1500)</script>"


def jl(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


PAGES = {}
PENDING = {}


def page(path, title, desc, h1, body, crumbs=None, ld=None, lede='', og=None, photo=None, stick=None, article=False, custom_top=False):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, ld=ld or [], lede=lede, og=og, photo=photo, stick=stick,
                       article=article, custom_top=custom_top)


def stick_bar(k):
    if k not in HOUSES:
        return ('<div class="stick"><p class="price"><b>RM 500</b> <small>per night &middot; both houses</small></p>%s</div>'
                % wa_btn('Check dates', wa_msg(), 'sticky-all'))
    h = HOUSES[k]
    return ('<div class="stick"><p class="price"><b>RM %d</b> <small>per night &middot; %s</small></p>%s</div>'
            % (h['price'], 'min. 1 night' if k == 'landak' else 'min. stay: ask us', wa_btn('Check dates', h['msg'], 'sticky-' + k)))


def render(path, p):
    pre = '../' * path.count('/')
    url = BASE + path
    og = p['og'] or HERO_IMG
    crumbs = p['crumbs']
    lds = list(p['ld']) + PENDING.get(path, [])
    if crumbs and len(crumbs) > 1:
        lds.append(crumbs_ld(crumbs))
    lds.append({'@context': 'https://schema.org', '@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': p['title'],
                'description': p['desc'], 'dateModified': TODAY, 'inLanguage': 'en-SG', 'isPartOf': {'@type': 'WebSite', 'name': NAME, 'url': BASE},
                'primaryImageOfPage': {'@type': 'ImageObject', 'url': abs_img(og)}})
    if path == '' or p['custom_top']:
        top = ''
    else:
        top = ('<div class="ptop"><div class="wrap">%s<h1>%s</h1>%s%s</div></div>'
               % (crumbs_html(crumbs) if crumbs and len(crumbs) > 1 else '', e(p['h1']),
                  ('<p class="lead">%s</p>' % p['lede']) if p['lede'] else '',
                  ('<div class="pphoto">%s</div>' % pimg(p['photo'], eager=True, sizes='(min-width:1248px) 1152px, 100vw')) if p['photo'] else ''))
    stick = stick_bar(p['stick'] or 'any')
    bc = ('home' if path == '' else 'inner') + (' has-stick' if stick else '')
    w, h = dims(og)
    body = ('<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            '<meta name="robots" content="index,follow,max-image-preview:large">'
            '<meta name="theme-color" content="#f7f8f9">'
            '<link rel="icon" href="{pre}favicon.ico" sizes="48x48"><link rel="icon" href="{pre}icon.svg" type="image/svg+xml"><link rel="icon" href="{pre}icon-192.png" sizes="192x192" type="image/png">'
            '<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png"><link rel="manifest" href="{pre}site.webmanifest">'
            '<meta property="og:type" content="{ogt}"><meta property="og:site_name" content="JBStaycation"><meta property="og:title" content="{title}">'
            '<meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogi}"><meta property="og:image:width" content="{ogw}"><meta property="og:image:height" content="{ogh}"><meta property="og:image:alt" content="{oga}">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:image" content="{ogi}">'
            '{headjs}{fonts}<link rel="stylesheet" href="{pre}jb.css">{lds}</head><body class="{bc}">'
            '<a class="skip" href="#main">Skip to content</a>{hdr}<main id="main">{top}{content}</main>{ftr}{stick}'
            '<script src="{pre}jb.js" defer></script><script src="{pre}cta.js" defer></script></body></html>').format(
        title=e(p['title']), desc=e(p['desc']), url=url, pre=pre, ogt='article' if p['article'] else 'website', ogi=e(abs_img(og)),
        ogw=w, ogh=h, oga=e(_alt_for(og)), headjs=HEAD_JS, fonts=FONT_LINKS, lds=''.join(jl(x) for x in lds), bc=bc, hdr=header_html(p['stick']), top=top,
        content=p['body'], ftr=footer_html(), stick=stick)
    return body.replace('{R}', pre)


# ---------------------------------------------------------------- page bodies
SG_CHIPS = {'prima': [('car', 'Tuas about 10 min'), ('car', 'Woodlands about 15 min')],
            'landak': [('walk', '5-min walk to KSL City Mall'), ('car', 'CIQ about 10 min')]}
AREA = {'prima': 'Taman Nusantara Prima, Iskandar Puteri', 'landak': 'Taman Abad, Johor Bahru'}
BADGE = {'prima': 'For big groups', 'landak': 'Games house'}


def specs(k, cls='specs'):
    h = HOUSES[k]
    items = [('users', 'Up to %d guests' % h['guests'])]
    if k == 'landak':
        items.append(('bed', '3 bedrooms'))
    items.append(('bath', '3 bathrooms'))
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s%s</li>' % (ico(i, 18), e(t)) for i, t in items))


def house_card(k, eager=False):
    h = HOUSES[k]
    imgs = CARD_IMG[k]
    strip = ''.join('<span class="slide">%s</span>' % pimg(f, sizes='(min-width:1200px) 180px, (min-width:800px) 15vw, 100vw') for f in imgs[1:])
    sg = ''.join('<li>%s%s</li>' % (ico(i, 16), e(t)) for i, t in SG_CHIPS[k])
    return ('<article class="hcard rv"><div class="cimg cz" data-carousel aria-roledescription="carousel" aria-label="Photos of %s"><div class="track"><div class="ph slide">%s<span class="badge">%s</span></div><div class="strip">%s</div></div>'
            '<button class="cbtn prev" type="button" aria-label="Previous photo">%s</button><button class="cbtn next" type="button" aria-label="Next photo">%s</button><span class="cnt" aria-hidden="true">1 / %d</span></div>'
            '<div class="cb"><p class="area">%s%s</p><h3><a href="{R}stays/%s/">%s</a></h3>%s<ul class="sg">%s</ul>'
            '<div class="price-row"><p class="price"><b>RM %d</b> <small>per night &middot; %s</small></p><span class="go">View house %s</span></div>%s</div></article>'
            % (e(h['name']), pimg(imgs[0], sizes='(min-width:1200px) 560px, (min-width:800px) 46vw, 100vw', eager=eager, lazy=not eager), BADGE[k], strip, ico('left', 22), ico('right', 22), len(imgs),
               ico('pin', 16), e(AREA[k]), h['slug'], e(h['name']), specs(k), sg, h['price'],
               'min. 1 night' if k == 'landak' else 'min. stay: ask us', ico('arrow', 18),
               wa_btn('Check dates for %s' % h['name'].replace(' Kawan Fun House', ''), h['msg'], 'card-' + k, 'btn btn-wa card-cta')))


HOME_FAQ = [
    ('How do I book?', 'Message us on WhatsApp at %s with your dates, group size and the house you like. Bookings are made through WhatsApp only.' % WA_SHOW),
    ('How much is a night?', 'Both Prima and Landak Kawan Fun House are RM 500 per night. Prices are in Malaysian ringgit (RM).'),
    ('How many guests can stay?', 'Prima is listed for up to 20 guests and Landak Kawan Fun House for up to 10.'),
    ('Is there a minimum stay?', 'Landak Kawan Fun House has a minimum stay of 1 night. For Prima, ask us on WhatsApp for the minimum stay on your dates.'),
    ('What are the check-in and check-out times?', 'At Landak Kawan Fun House, self check-in is after 3:00 pm and check-out is before 11:00 am. For Prima, ask us on WhatsApp.'),
    ('Are pets, smoking and BBQ allowed?', 'At Landak Kawan Fun House there is no smoking, no pets, and no BBQ or charcoal grilling. For Prima, ask us on WhatsApp for the house rules. At both houses, guests must not disturb neighbours.'),
    ('Is there parking, and can we cook?', 'Free parking is listed at both houses. Prima has a full kitchen; Landak Kawan Fun House has a kitchen for light cooking.'),
    ('Can we hold an event, and what is the cancellation policy?', 'Events and larger gatherings need prior approval and may cost extra, so ask us first. The host says the cancellation policy is shown before payment and in your confirmation.'),
]


def route_list():
    """Phone version of the route diagram: plain vertical lists (the SVG shows from 768 px)."""
    def chain(title, steps):
        li = ''.join('<li class="%s">%s</li>' % (c, t) for c, t in steps)
        return '<div class="rl-card"><p class="rl-h">%s</p><ol class="rl">%s</ol></div>' % (title, li)
    return ('<div class="rlist">' +
            chain('Second Link', [('', '<b>Singapore</b>'), ('', '<b>Tuas checkpoint</b>'), ('t', 'about 10 min'), ('end', '<b>Prima</b><span>Iskandar Puteri &middot; up to 20 guests</span>')]) +
            chain('Causeway', [('', '<b>Singapore</b>'), ('', '<b>Woodlands checkpoint</b>'), ('', '<b>JB CIQ</b>'), ('t', 'about 10 min'), ('end', '<b>Landak Kawan Fun House</b><span>Taman Abad &middot; up to 10 guests &middot; 5-min walk to KSL City Mall</span>')]) +
            chain('RTS Link (not running yet)', [('', '<b>Woodlands North</b>'), ('t', 'about 5 min by train'), ('end', '<b>Bukit Chagar</b><span>Expected from February 2027</span>')]) + '</div>')


def route_map(rl=False):
    """Schematic (not to scale) of Singapore -> Second Link / Causeway -> the two houses. Times are host-stated."""
    return ('<figure class="mapcard%s">' % (' has-rl' if rl else '') + (route_list() if rl else '') + '<svg class="map-w" viewBox="0 0 640 420" role="img" aria-labelledby="mapt mapd" font-family="Geist,system-ui,sans-serif">'
            '<title id="mapt">Route diagram from Singapore to the two JBStaycation houses</title>'
            '<desc id="mapd">Schematic, not to scale. From Singapore, the Second Link at Tuas leads to Prima in Iskandar Puteri, about 10 minutes as stated by the host. The Causeway at Woodlands leads to JB CIQ; Landak Kawan Fun House in Taman Abad is about 10 minutes from CIQ and a 5-minute walk from KSL City Mall. The RTS Link from Woodlands North to Bukit Chagar is expected from February 2027.</desc>'
            '<rect width="640" height="420" rx="12" fill="#f3f6f9"/>'
            '<path d="M0 215 C120 195 200 240 320 222 S520 196 640 214 V262 C520 246 430 276 320 266 S120 246 0 262 Z" fill="#cfdeec"/>'
            '<text x="24" y="40" font-size="13" font-weight="600" letter-spacing="1.6" fill="#7c8a9b">JOHOR BAHRU, MALAYSIA</text>'
            '<text x="24" y="398" font-size="13" font-weight="600" letter-spacing="1.6" fill="#7c8a9b">SINGAPORE</text>'
            '<text x="320" y="248" font-size="12" fill="#6b85a0" text-anchor="middle" font-style="italic">Strait of Johor</text>'
            # second link (west)
            '<path d="M150 360 C150 300 140 270 140 200" stroke="#10304f" stroke-width="5" fill="none" stroke-linecap="round"/>'
            '<path d="M140 200 C140 160 160 140 178 118" stroke="#e8a33d" stroke-width="3.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>'
            '<rect x="56" y="300" width="136" height="44" rx="10" fill="#fff" stroke="#dfe4e9"/>'
            '<text x="70" y="319" font-size="13" font-weight="600" fill="#0a1f38">Second Link</text><text x="70" y="335" font-size="12" fill="#45566b">Tuas checkpoint</text>'
            # causeway (east)
            '<path d="M470 360 C470 300 474 270 474 200" stroke="#10304f" stroke-width="5" fill="none" stroke-linecap="round"/>'
            '<path d="M496 360 C496 300 500 270 500 200" stroke="#7c8a9b" stroke-width="2" fill="none" stroke-dasharray="6 5"/>'
            '<path d="M474 200 C474 170 482 150 500 130" stroke="#e8a33d" stroke-width="3.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>'
            '<rect x="330" y="300" width="128" height="44" rx="10" fill="#fff" stroke="#dfe4e9"/>'
            '<text x="344" y="319" font-size="13" font-weight="600" fill="#0a1f38">Causeway</text><text x="344" y="335" font-size="12" fill="#45566b">Woodlands checkpoint</text>'
            '<text x="512" y="290" font-size="12" fill="#45566b">RTS Link</text><text x="512" y="305" font-size="12" fill="#7c8a9b">expected</text><text x="512" y="320" font-size="12" fill="#7c8a9b">Feb 2027</text>'
            '<circle cx="474" cy="196" r="6" fill="#10304f"/><text x="456" y="186" font-size="12" font-weight="600" fill="#10304f" text-anchor="end">JB CIQ</text>'
            # houses
            '<circle cx="186" cy="108" r="16" fill="#e8a33d"/><path d="M178 109 186 101l8 8h-2.5v7h-11v-7z" fill="#0a1f38"/>'
            '<text x="210" y="100" font-size="15" font-weight="700" fill="#0a1f38">Prima</text><text x="210" y="118" font-size="12" fill="#45566b">Iskandar Puteri &#183; up to 20 guests</text>'
            '<rect x="80" y="146" width="98" height="26" rx="13" fill="#0a1f38"/><text x="129" y="163" font-size="12" font-weight="600" fill="#fff" text-anchor="middle">about 10 min</text>'
            '<circle cx="508" cy="120" r="16" fill="#e8a33d"/><path d="M500 121 508 113l8 8h-2.5v7h-11v-7z" fill="#0a1f38"/>'
            '<text x="496" y="80" font-size="15" font-weight="700" fill="#0a1f38" text-anchor="end">Landak Kawan</text><text x="496" y="97" font-size="12" fill="#45566b" text-anchor="end">Taman Abad &#183; up to 10 guests</text>'
            '<rect x="518" y="146" width="106" height="26" rx="13" fill="#0a1f38"/><text x="571" y="163" font-size="12" font-weight="600" fill="#fff" text-anchor="middle">10 min to CIQ</text>'
            '<text x="532" y="64" font-size="12" fill="#a86d15" font-weight="600">KSL City Mall</text><text x="532" y="79" font-size="12" fill="#45566b">5-min walk</text>'
            '<path d="M520 110 C526 98 528 90 532 84" stroke="#a86d15" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>'
            '</svg><figcaption>Schematic, not to scale. Drive and walk times are as stated by the host.</figcaption></figure>')


def article_card(a, sizes='(min-width:760px) 33vw, 100vw'):
    return ('<article class="acard rv"><span class="ph">%s</span><div class="cb"><span class="tag">Guide</span><h3><a href="{R}articles/%s/">%s</a></h3><p>%s</p>'
            '<span class="go">Read the guide %s</span></div></article>' % (pimg(PAGE_IMG[a['slug']], sizes=sizes), a['slug'], e(a['title']), e(a['desc']), ico('arrow', 18)))


def home_body():
    faq_html, faq_ld = faq_block(HOME_FAQ, None, cta='<p class="after-faq">%s</p>' % wa_btn('Ask us on WhatsApp', wa_msg(), 'home-faq'))
    PENDING.setdefault('', []).append(faq_ld)
    msg = wa_msg()
    facts = [('home', '2 private houses'), ('users', 'Sleeps 10 to 20'), ('car', 'About 10 min from Tuas'), ('walk', '5-min walk to KSL City Mall')]
    facts_html = ''.join('<li>%s%s</li>' % (ico(i, 20), e(t)) for i, t in facts)
    why = [('home', 'The whole house is yours', 'Private homes with kitchens, parking and space for the whole group to stay together.'),
           ('party', 'Made for group fun', 'Prima has karaoke, a mahjong table and a BBQ pit. Landak Kawan Fun House has a pool table, foosball and darts.'),
           ('car', 'Close to the checkpoints', 'Host-stated drive times: Prima about 10 minutes to Tuas, Landak about 10 minutes to CIQ.'),
           ('chat', 'Simple booking', 'Message us on WhatsApp for dates and rates. Prices are in RM.')]
    why_html = ''.join('<li>%s<b>%s</b><span>%s</span></li>' % (ico(i, 30), t, d) for i, t, d in why)
    steps = [('Pick a house.', 'Choose Prima for a big group of up to 20, or Landak Kawan Fun House for up to 10 with games and a short walk to KSL City Mall.'),
             ('Message us your dates.', 'Send your group size and dates on WhatsApp and we will confirm the rate and availability.'),
             ('Cross with your passport.', 'Check ICA\'s traffic updates before you leave, then drive in and settle in. Landak has self check-in after 3:00 pm.')]
    steps_html = ''.join('<li><div><b>%s</b><span>%s</span></div></li>' % (e(a), e(b)) for a, b in steps)
    mosaic = ''.join('<span class="slide">%s</span>' % pimg(f, sizes='(min-width:960px) 30vw, 100vw') for f in HOME_MOSAIC)
    routes = [('car', 'By road: Woodlands or Tuas', 'Two land checkpoints. The host states Prima is about 10 minutes from Tuas and 15 from Woodlands.'),
              ('walk', 'Arriving on the city side', 'Landak Kawan Fun House is about 10 minutes from CIQ and a 5-minute walk from KSL City Mall.'),
              ('clock', 'By train: the RTS Link', 'Woodlands North to Bukit Chagar, expected to start passenger service in February 2027, subject to safety certification (LTA, 2 October 2026).')]
    routes_html = ''.join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (ico(i, 22), t, d) for i, t, d in routes)
    arts = ''.join(article_card(a) for a in ARTICLES)
    return (
        # hero
        '<section class="hero"><div class="hero-bg">%s</div><div class="wrap hero-in">'
        '<h1><span class="kick">JB staycation for big groups: private holiday houses in Johor Bahru</span><span class="display">%s</span></h1>'
        '<p class="sub">Two private holiday houses in Johor Bahru for groups from Singapore, both RM 500 per night.<span class="more"> Prima sleeps up to 20 and Landak Kawan Fun House up to 10. The whole house is yours, booked directly on WhatsApp.</span></p>'
        '<div class="cta-row">%s</div>'
        '<ul class="facts" aria-label="At a glance">%s</ul></div></section>'
        # houses
        '<section class="sec" id="houses"><div class="wrap"><div class="sec-head split rv"><div><p class="eyebrow">Where you could be</p><h2>Two houses, one for every kind of group</h2></div>'
        '<p class="lead hm">Choose Prima for a big group of up to 20, or Landak Kawan Fun House for up to 10 with games and a short walk to KSL City Mall.</p></div>'
        '<div class="cards">%s%s</div><p class="note" style="margin-top:20px">Drive and walk times are as stated by the host. <a href="{R}stays/">Compare both houses</a></p></div></section>'
        # why
        '<section class="sec dark"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">Why book with JBStaycation</p><h2>We keep it small on purpose.</h2></div>'
        '<ul class="pts rv">%s</ul></div></section>'
        # steps + mosaic
        '<section class="sec"><div class="wrap split2"><div class="rv"><p class="eyebrow">How it works</p><h2>Plan your weekend in three steps</h2><ol class="steps">%s</ol>'
        '<p class="after-gal">%s</p></div>'
        '<div class="rv cz" data-carousel aria-roledescription="carousel" aria-label="Photos of the houses"><div class="mosaic track">%s</div>'
        '<button class="cbtn prev" type="button" aria-label="Previous photo">%s</button><button class="cbtn next" type="button" aria-label="Next photo">%s</button><span class="cnt" aria-hidden="true">1 / %d</span></div></div></section>'
        # getting there
        '<section class="sec"><div class="wrap split2"><div class="rv"><p class="eyebrow">Getting there</p><h2>Getting there from Singapore</h2><ul class="routes">%s</ul>'
        '<a class="btn btn-line" href="{R}getting-there/">Read the getting-there guide %s</a></div>%s</div></section>'
        # articles
        '<section class="sec gsec"><div class="wrap"><details class="fold" id="guides"><summary><span class="st"><span class="eyebrow">Guides</span><h2>Plan it like a local</h2></span>%s</summary>'
        '<div class="fold-body"><p class="lead">Practical answers for groups crossing from Singapore.</p><div class="arts">%s</div><p><a class="link" href="{R}articles/">All guides %s</a></p></div></details>'
        '<script>if(innerWidth>=900)document.currentScript.previousElementSibling.open=true</script></div></section>'
        # faq
        '<section class="sec" style="background:#fff;border-top:1px solid var(--line)"><div class="wrap faqgrid"><div class="rv"><p class="eyebrow">Questions</p><h2>Frequently asked questions</h2>'
        '<p class="muted">Anything else? We reply on WhatsApp.</p><a class="link" href="{R}faq/">More questions and answers %s</a></div><div class="rv">%s</div></div></section>'
        # cta
        '<section class="sec band"><div class="bg">%s</div><div class="wrap rv"><p class="eyebrow">Book direct</p><h2>Ready to plan your stay?</h2><p>Tell us your dates and how many are coming. We will reply on WhatsApp.</p>%s</div></section>'
        % (pimg(HERO_IMG, HERO_ALT, eager=True, thumb=False), e(TAGLINE), wa_btn('Check dates on WhatsApp', msg, 'home-hero'), facts_html,
           house_card('prima'), house_card('landak'), why_html, steps_html, wa_btn('Check dates on WhatsApp', wa_msg(), 'home-gallery', 'btn btn-wa'), mosaic, ico('left', 22), ico('right', 22), len(HOME_MOSAIC), routes_html, ico('arrow', 18), route_map(),
           ico('x', 22, 'i pm'), arts, ico('arrow', 18), ico('arrow', 18), faq_html, pimg(HOME_CTA_IMG, sizes='100vw'), wa_btn('Message us on WhatsApp', msg, 'home-cta')))


def stays_body():
    return ('<div class="wrap body"><div class="cards">%s%s</div>'
            '<section class="rv" style="margin-top:clamp(48px,7vw,80px)"><p class="eyebrow">Side by side</p><h2>Which house is right for you?</h2><div class="tw"><table><thead><tr><th></th><th>Prima</th><th>Landak Kawan Fun House</th></tr></thead><tbody>'
            '<tr><th>Area</th><td>Taman Nusantara Prima, Iskandar Puteri</td><td>Taman Abad, Johor Bahru</td></tr>'
            '<tr><th>Guests</th><td>Up to 20</td><td>Up to 10</td></tr>'
            '<tr><th>Rate</th><td>RM 500 per night</td><td>RM 500 per night</td></tr>'
            '<tr><th>Best for</th><td>Big groups, karaoke, mahjong, BBQ</td><td>Games nights, near KSL City Mall</td></tr>'
            '<tr><th>Host-stated distance</th><td>About 10 min to Tuas, 15 min to Woodlands</td><td>5-minute walk to KSL City Mall, 10 min to CIQ</td></tr>'
            '</tbody></table></div></section></div>' % (house_card('prima'), house_card('landak')))


def room_gallery(k):
    out = []
    for title, note, ph in ROOMS[k]:
        ph = [p for p in ph if p[0] not in BENTO[k]]
        if not ph:
            continue
        land = [p for p in ph if dims(p[0])[0] >= dims(p[0])[1]]
        port = [p for p in ph if dims(p[0])[0] < dims(p[0])[1]]
        if port and len(land) >= 2:                      # portrait shots never take the wide feature or the spanning last tile
            ph = land[:-1] + port + land[-1:]
        n = len(ph)

        def span(i):
            cls = []
            if n > 2 and i == n - 1 and n % 2 == 0:
                cls.append('sm2')                       # phones: feature + pairs, so a lone last tile spans 2
            if n > 3 and i >= 3:
                rest = (n - 3) % 3                      # desktop: feature (2x2) + 2 beside it, then rows of 3
                if rest == 1 and i == n - 1:
                    cls.append('sd3')
                elif rest == 2 and i == n - 1:
                    cls.append('sd2')
            return ' class="slide %s"' % ' '.join(cls)
        ridx = len(out)
        figs = ''.join('<figure%s data-room="%d"><a href="{R}img/%s" data-lb data-cap="%s">%s</a>%s</figure>'
                       % (span(i), ridx, f, e(cap if is_client else '%s, %s' % (title, HOUSES[k]['name'])), pimg(f, sizes='(min-width:1024px) 300px, (min-width:768px) 33vw, 100vw'),
                          ('<figcaption>%s</figcaption>' % e(cap)) if is_client else '') for i, (f, cap, is_client) in enumerate(ph))
        out.append('<div class="room"><div class="room-h"><h3>%s</h3><span>%s%d photo%s</span></div><div class="rg%s">%s</div></div>'
                   % (e(title), (e(note) + ' &middot; ') if note else '', n, '' if n == 1 else 's', ' n1' if n == 1 else (' n2' if n == 2 else ''), figs))
    chips, first, cnt = [], 0, 0
    for i, (title, _n, ph) in enumerate(ROOMS[k]):
        m = len([p for p in ph if p[0] not in BENTO[k]])
        if m:
            chips.append('<button type="button" data-room="%d" data-i="%d" aria-pressed="false">%s</button>' % (len(chips), cnt, e(title)))
            cnt += m
    return ('<div class="rooms-wrap" data-carousel aria-roledescription="carousel" aria-label="Photos by room"><nav class="rchips" aria-label="Rooms">%s</nav>'
            '<div class="cz"><div class="rooms track" tabindex="0">%s</div>'
            '<button class="cbtn prev" type="button" aria-label="Previous photo">%s</button><button class="cbtn next" type="button" aria-label="Next photo">%s</button><span class="cnt" aria-hidden="true">1 / %d</span></div></div>'
            % (''.join(chips), ''.join(out), ico('left', 22), ico('right', 22), cnt))


def total_photos(k):
    return sum(len(ph) for _t, _n, ph in ROOMS[k])


def house_body(k):
    h = HOUSES[k]
    faq_html, faq_ld = faq_block(h['faq'], 'Questions about %s' % h['name'], cta='<p class="after-faq">%s</p>' % wa_btn('Ask us on WhatsApp', h['msg'], 'faq-' + k))
    PENDING.setdefault('stays/%s/' % h['slug'], []).append(faq_ld)
    path = 'stays/%s/' % h['slug']
    crumbs = [('Home', ''), ('Stays', 'stays/'), (h['name'], path)]
    n_all = total_photos(k)
    caps = {}
    for _t, _n, ph in ROOMS[k]:
        for f, cap, c in ph:
            caps[f] = cap if c else '%s, %s' % (_t, h['name'])
    slides = ''.join('<li class="slide"><a href="{R}img/%s" data-lb data-cap="%s">%s</a></li>'
                     % (f, e(caps[f]), pimg(f, eager=(i == 0), lazy=(i > 0), sizes=('(min-width:768px) 50vw, 100vw' if i == 0 else '(min-width:768px) 25vw, 100vw')))
                     for i, f in enumerate(BENTO[k]))
    gal = ('<section class="gal" id="photos" aria-roledescription="carousel" aria-label="Photos of %s" data-carousel><ul class="track" tabindex="0">%s</ul>'
           '<button class="cbtn prev" type="button" aria-label="Previous photo">%s</button><button class="cbtn next" type="button" aria-label="Next photo">%s</button>'
           '<span class="cnt" aria-hidden="true">1 / %d</span><a class="gal-all" href="#spaces" data-lb-open>%sView all %d photos</a></section>'
           % (e(h['name']), slides, ico('left', 22), ico('right', 22), len(BENTO[k]), ico('grid', 18), n_all))
    meta = [('pin', AREA[k]), ('users', 'Up to %d guests' % h['guests'])] + ([('bed', '3 bedrooms')] if k == 'landak' else []) + [('bath', '3 bathrooms')]
    meta_html = ''.join('<li>%s%s</li>' % (ico(i, 18), e(t)) for i, t in meta)
    sub = ''.join('<a href="#%s">%s</a>' % (a, b) for a, b in [('spaces', 'Photos'), ('amenities', 'Amenities'), ('rules', 'House rules'), ('location', 'Location'), ('faq', 'FAQ'), ('book', 'Check dates &amp; rate')])
    stat_ic = {'Guests': 'users', 'Bedrooms': 'bed', 'Bathrooms': 'bath', 'Rate': 'cal'}
    stats = ''.join('<li>%s<small>%s</small><b>%s</b></li>' % (ico(stat_ic.get(a, 'check'), 22), a, e(b)) for a, b in h['stats'])
    amen = ''.join('<li>%s<span>%s</span></li>' % (ico(amen_icon(a), 26), e(a)) for a in h['amen'])
    rule_ic = lambda r: 'no' if r.startswith('No ') else ('clock' if r.startswith('Check') else ('party' if r.startswith('Events') else 'check'))
    rules = ''.join('<li>%s<span>%s</span></li>' % (ico(rule_ic(r), 20), e(r)) for r in h['rules'])
    near = ''.join('<li><span>%s%s</span><b>%s</b></li>' % (ico('walk' if 'walk' in b else 'car', 18), e(a), e(b)) for a, b in h['near'])
    intro = '<p>%s</p>' % e(h['intro'][0])
    more = ''.join('<p>%s</p>' % e(t) for t in h['intro'][1:])
    if k == 'prima':
        more += '<p>Looking for a Johor Bahru house rental for 20 pax? Prima is listed for up to 20 guests at RM 500 per night. Ask us on WhatsApp about the bedrooms and the minimum stay.</p>'
    gal_cta = '<p class="after-gal">%s</p>' % wa_btn('Check dates on WhatsApp', h['msg'], 'gallery-' + k)
    spaces_cta = '<p class="after-gal">%s</p>' % wa_btn('Like what you see? Check dates', h['msg'], 'spaces-' + k)
    ok = 'landak' if k == 'prima' else 'prima'
    other = HOUSES[ok]
    side_items = [('users', 'Up to %d guests' % h['guests']), ('cal', h['minstay']), ('chat', 'Book directly on WhatsApp')]
    if k == 'landak':
        side_items.insert(1, ('key', 'Self check-in after 3:00 pm'))
    side = ('<aside class="side rv" id="book" aria-label="Rate and booking"><p class="price"><b>RM %d</b><small>/ night</small></p>'
            '<ul>%s</ul>%s<p class="note">Prices are in RM. Message us for the rate and availability on your dates.</p></aside>'
            % (h['price'], ''.join('<li>%s%s</li>' % (ico(i, 18), e(t)) for i, t in side_items), wa_btn('Check dates & rate', h['msg'], k, 'btn btn-wa')))
    return ('<div class="htop"><div class="wrap">%s<h1>%s</h1><ul class="hmeta">%s</ul><nav class="subnav" aria-label="On this page">%s</nav>%s%s</div></div>'
            '<div class="wrap hlay"><div class="hmain">'
            '<section class="intro rv"><h2 class="htag">%s</h2><ul class="stats">%s</ul>%s</section>'
            '<section id="amenities" class="rv"><h2>What is included</h2><ul class="amen">%s</ul></section>'
            '<section id="spaces"><h2 class="rv">Explore the spaces</h2><p class="muted rv">%d photos, room by room. Tap any photo to open it full screen.</p>%s%s</section>'
            '<section id="about" class="rv"><h2>About this house</h2>%s</section>'
            '<section id="rules" class="rv"><h2>House rules and times</h2><ul class="rules%s">%s</ul></section>'
            '<section id="location" class="rv"><h2>Location and nearby</h2><p class="addr">%s<span>%s</span></p><ul class="near">%s</ul><p class="note">%s See <a href="{R}getting-there/">getting there from Singapore</a>.</p></section>'
            '<section id="faq" class="rv">%s</section>'
            '<section class="rv"><h2>Looking for another size?</h2><a class="ocard" href="{R}stays/%s/"><span class="ph">%s</span><span><b>%s</b><small>%s &middot; up to %d guests &middot; RM %d per night</small><span class="go">View house %s</span></span></a>'
            '<p class="note" style="margin-top:16px">Or read <a href="{R}articles/big-group-staycation-jb-house-for-10-20-people/">how to choose a house for a big group</a>.</p></section></div>'
            '%s</div>'
            % (crumbs_html(crumbs), e(H1S[k]), meta_html, sub, gal, gal_cta, e(h['tag']), stats, intro, amen, n_all, room_gallery(k), spaces_cta, more,
               ' one' if len(h['rules']) == 1 else '', rules, ico('pin', 20), e(h['addr']), near, e(h['near_note']), faq_html,
               other['slug'], pimg(CARD_IMG[ok][0], sizes='200px'), e(other['name']), e(AREA[ok]), other['guests'], other['price'], ico('arrow', 18), side))


def prices_body():
    rows = ''.join('<tr><th><a href="{R}stays/%s/">%s</a></th><td>RM %d per night</td><td>%s</td><td>Up to %d</td></tr>'
                   % (HOUSES[k]['slug'], e(HOUSES[k]['name']), HOUSES[k]['price'], e(HOUSES[k]['minstay']), HOUSES[k]['guests']) for k in ORDER)
    return ('<div class="wrap body prose"><div class="tw"><table><thead><tr><th>House</th><th>Rate</th><th>Minimum stay</th><th>Guests</th></tr></thead><tbody>%s</tbody></table></div>'
            '<section class="rv"><h2>What the listing includes</h2><p><b>Prima:</b> fast Wi-Fi, air conditioning, full kitchen, free parking, smart TV, washer and dryer, karaoke set, mahjong table, BBQ pit, workspace and a playground.</p>'
            '<p><b>Landak Kawan Fun House:</b> 100 Mbps Wi-Fi, washer and detergent, hair dryer, iron, workspace, free parking, pool table, foosball, two dartboards and a 55-inch smart TV with arcade console.</p></section>'
            '<section class="rv"><h2>Good to know</h2><ul><li>All prices are in Malaysian ringgit (RM).</li><li>Rates for your dates, deposits and payment details are confirmed on WhatsApp.</li>'
            '<li>Landak Kawan Fun House: events need prior approval and may cost extra.</li></ul>%s</section></div>'
            % (rows, wa_btn('Message for dates and rates', wa_msg(), 'prices')))


def gt_body():
    srcs = ''.join('<li><a href="%s" rel="noopener">%s</a> (%s)</li>' % (e(u), e(t), e(n)) for t, u, n in [SRC[k] for k in ('lta_feb', 'lta_rts', 'ica_qr', 'ica_traffic')])
    return ('<div class="wrap body"><div class="prose"><div class="answer">There are two road crossings from Singapore, at Woodlands and Tuas. The RTS Link train from Woodlands North to Bukit Chagar is expected to start in February 2027. Prima is nearer Tuas; Landak Kawan Fun House is nearer CIQ and KSL City Mall.</div></div>'
            '<div class="gt-map" style="max-width:860px;margin:0 0 36px">%s</div><div class="prose">'
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
            '<section class="rv src"><h2>Official sources</h2><ul>%s</ul></section></div></div>'
            % (route_map(True), SRC['ica_traffic'][1], SRC['ica_qr'][1], wa_btn('Ask us about your route', wa_msg(), 'getting-there'), srcs))


FAQ_ALL = [
    ('How do I book?', 'Message us on WhatsApp at %s with your dates, group size and the house you like. We take bookings through WhatsApp only.' % WA_SHOW),
    ('What are the check-in and check-out times?', 'At Landak Kawan Fun House, self check-in is after 3:00 pm and check-out is before 11:00 am. For Prima, message us to confirm the times.'),
    ('What is the minimum stay?', 'Landak Kawan Fun House has a minimum of 1 night. Prima shows "Minimum 2" on its listing without a unit, so ask us on WhatsApp for the minimum stay.'),
    ('How many guests can stay?', 'Prima is listed for up to 20 guests and Landak Kawan Fun House for up to 10.'),
    ('Is there parking?', 'Yes. Free parking is listed at both houses.'),
    ('Are pets and smoking allowed?', 'At Landak Kawan Fun House, no smoking, no pets, and no BBQ or charcoal grilling. Events need prior approval and may cost extra. For Prima, ask us for the house rules.'),
    ('Are there quiet hours?', 'We have not listed quiet hours. Ask us on WhatsApp. The host asks guests not to disturb neighbours.'),
    ('Is a deposit needed?', 'We have not listed a deposit amount. Ask us on WhatsApp before you book.'),
    ('What is the cancellation policy?', 'The host says the cancellation policy is shown before payment and in your confirmation. You can also ask us on WhatsApp before you decide.'),
    ('Can we hold an event or a larger gathering?', 'Events and larger gatherings need prior approval and may cost extra, so please ask us first.'),
    ('Can we cook at the houses?', 'Prima has a full kitchen. Landak Kawan Fun House has a kitchen for light cooking, and no BBQ or charcoal grilling is allowed there.'),
    ('What currency are prices in?', 'Prices are in Malaysian ringgit (RM). Both houses are listed at RM 500 per night.'),
    ('What should I bring when crossing the border?', 'Bring your passport. ICA states that you must still bring your passport for travel by land, even if you use QR code clearance. Check official sources for current entry requirements.'),
    ('Which house is closer to Tuas?', 'The host states Prima is about 10 minutes from Tuas and about 15 minutes from Woodlands.'),
    ('Which house is near a shopping mall?', 'Landak Kawan Fun House is about a 5-minute walk to KSL City Mall, as stated by the host.'),
]


def faq_body():
    f, ld = faq_block(FAQ_ALL, 'Common questions')
    PENDING.setdefault('faq/', []).append(ld)
    return '<div class="wrap body prose">%s<p style="margin-top:28px">%s</p><p class="note">Passport and border information comes from <a href="%s" rel="noopener">ICA</a> (checked 8 Nov 2026).</p></div>' % (
        f, wa_btn('Ask us on WhatsApp', wa_msg(), 'faq'), SRC['ica_qr'][1])


def about_body():
    return ('<div class="wrap body prose"><section class="rv"><h2>JBStaycation</h2><p>JBStaycation offers private holiday houses in Johor Bahru for families and groups, many of them travelling from Singapore. Our idea is simple: %s</p>'
            '<p>We have two houses, <a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Taman Nusantara Prima, Iskandar Puteri, and <a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad, Johor Bahru.</p>'
            '<p>Bookings are made directly with us on WhatsApp at %s. Prices are in RM.</p></section>'
            '<section class="rv"><h2>Addresses</h2><ul>%s</ul>%s</section></div>'
            % (e(TAGLINE.lower()), WA_SHOW, ''.join('<li><b>%s</b>: %s</li>' % (e(HOUSES[k]['name']), e(HOUSES[k]['addr'])) for k in ORDER),
               wa_btn('Message us', wa_msg(), 'about')))


def contact_body():
    return ('<div class="wrap body prose"><section class="rv"><h2>Message us on WhatsApp</h2><p>WhatsApp is the only way to book: <b>%s</b>. Tell us the house, your dates and how many people.</p>%s'
            '<p style="margin-top:24px">Houses: %s</p></section></div>'
            % (WA_SHOW, wa_btn('Open WhatsApp', wa_msg(), 'contact'),
               ' | '.join('<a href="{R}stays/%s/">%s</a>' % (HOUSES[k]['slug'], e(HOUSES[k]['name'])) for k in ORDER)))


def privacy_body():
    return ('<div class="wrap body prose"><p>Last updated %s.</p><h2>What we collect</h2><p>When you message us on WhatsApp we receive your phone number, name shown on WhatsApp and whatever you write, such as dates and group size.</p>'
            '<h2>How we use it</h2><p>We use it to reply to your enquiry, confirm a booking and manage your stay. We do not sell your personal data.</p>'
            '<h2>Who sees it</h2><p>Messages are handled through WhatsApp, which has its own privacy policy. We share details only with people who help run your stay, or where the law requires.</p>'
            '<h2>Website analytics</h2><p>This website counts taps on contact links (for example WhatsApp) with an anonymous visitor identifier to understand which pages help visitors. It does not store your message.</p>'
            '<h2>Your choices</h2><p>You can ask us on WhatsApp to access, correct or delete your personal data, or to stop contacting you, in line with Malaysia\'s Personal Data Protection Act and Singapore\'s PDPA where they apply.</p>'
            '<p>We keep enquiry messages only as long as needed for the purposes above.</p></div>' % TODAY)


def articles_body():
    return '<div class="wrap body"><div class="arts">%s</div></div>' % ''.join(article_card(a) for a in ARTICLES)


def article_body(a):
    secs = ''.join('<section class="rv"><h2>%s</h2>%s</section>' % (e(h), ''.join('<p>%s</p>' % t for t in ps)) for h, ps in a['sections'])
    hh = HOUSES[a['house']]
    return ('<div class="wrap body prose"><p class="byline">%sBy JBStaycation, %s</p><div class="answer">%s</div>%s'
            '<section class="rv"><p>See the house: <a href="{R}stays/%s/">%s</a>.</p>%s</section></div>'
            % (ico('cal', 18), TODAY, e(a['answer']), secs, hh['slug'], e(hh['full']), wa_btn('Ask about dates', wa_msg(a.get('wa')), 'article-' + a['slug'][:30])))


# ---------------------------------------------------------------- assemble
def build_pages():
    page('', 'JB Staycation for Big Groups | JBStaycation',
         'Private Johor Bahru houses for groups of up to 20, RM 500 per night each. Message us on WhatsApp to check dates.',
         'JB staycation for big groups: Johor Bahru holiday houses', '', ld=[org_ld(), {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NAME, 'url': BASE}])
    PAGES['']['body'] = home_body()
    page('stays/', 'Johor Bahru Holiday Houses | JBStaycation', 'Compare Prima (up to 20 guests) and Landak Kawan Fun House (up to 10 guests): private holiday houses in Johor Bahru, RM 500 per night.',
         'Our Johor Bahru holiday houses', stays_body(), [('Home', ''), ('Stays', 'stays/')],
         lede='Two private houses, one for big groups and one for games nights near KSL City Mall.',
         ld=[{'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + 'stays/%s/' % HOUSES[k]['slug'], 'name': HOUSES[k]['full']} for i, k in enumerate(ORDER)]}])
    for k in ORDER:
        h = HOUSES[k]
        path = 'stays/%s/' % h['slug']
        titles = {'prima': ('JB Holiday House with Karaoke | JBStaycation', 'Sing karaoke, play mahjong and BBQ with up to 20 guests at RM 500 a night. Message us on WhatsApp to check dates.', H1S['prima']),
                  'landak': ('Staycation near KSL City Mall | JBStaycation', 'Walk to KSL City Mall, then play pool, foosball and darts for RM 500 a night. Message us on WhatsApp to check dates.', H1S['landak'])}[k]
        page(path, titles[0], titles[1], titles[2], '', [('Home', ''), ('Stays', 'stays/'), (h['name'], path)], ld=[house_ld(h)],
             og=BENTO[k][0], stick=k, custom_top=True)
        PAGES[path]['body'] = house_body(k)
    page('prices/', 'Prices: JB Holiday Houses in RM | JBStaycation', 'JBStaycation rates: RM 500 per night at Prima and Landak Kawan Fun House, minimum stay and what is included. Message for dates.',
         'Prices (RM per night)', prices_body(), [('Home', ''), ('Prices', 'prices/')], lede='Both houses are listed at RM 500 per night. Message us for your dates.', photo=PAGE_IMG['prices'], og=PAGE_IMG['prices'])
    page('getting-there/', 'Getting to JB from Singapore by Road or RTS | JBStaycation', 'Woodlands, Tuas or the RTS Link to Johor Bahru? Official facts with sources and which JBStaycation house suits each route.',
         'Getting to our Johor Bahru houses from Singapore', gt_body(), [('Home', ''), ('Getting there', 'getting-there/')],
         lede='Facts below come from official sources, with the date we checked them.', photo=PAGE_IMG['getting-there'], og=PAGE_IMG['getting-there'])
    page('faq/', 'FAQ: Booking a JB Holiday House | JBStaycation', 'Answers on booking, check-in, minimum stay, guests, parking, pets and crossing the border. Ask us on WhatsApp for the rest.',
         'Frequently asked questions', faq_body(), [('Home', ''), ('FAQ', 'faq/')], photo=PAGE_IMG['faq'], og=PAGE_IMG['faq'])
    page('about/', 'About JBStaycation | Johor Bahru Holiday Houses', 'JBStaycation offers two private holiday houses in Johor Bahru for Singapore families and groups, booked directly on WhatsApp.',
         'About JBStaycation', about_body(), [('Home', ''), ('About', 'about/')], lede=TAGLINE, photo=PAGE_IMG['about'],
         ld=[org_ld()])
    page('contact/', 'Contact JBStaycation on WhatsApp', 'Book or ask a question on WhatsApp +65 9006 2198. Tell us the house, dates and group size.',
         'Contact us', contact_body(), [('Home', ''), ('Contact', 'contact/')], lede='WhatsApp is the fastest way to reach us.', photo=PAGE_IMG['contact'], og=PAGE_IMG['contact'])
    page('privacy/', 'Privacy Notice | JBStaycation', 'How JBStaycation handles personal data from WhatsApp enquiries and website visits.', 'Privacy notice', privacy_body(), [('Home', ''), ('Privacy', 'privacy/')])
    page('articles/', 'JB Staycation Guides and Articles | JBStaycation', 'Plain-English guides for Singapore groups planning a Johor Bahru house stay: group size, KSL City Mall area and routes.',
         'Guides for staying in Johor Bahru', articles_body(), [('Home', ''), ('Articles', 'articles/')], lede='Practical answers for groups crossing from Singapore.')
    for a in ARTICLES:
        path = 'articles/%s/' % a['slug']
        ph = PAGE_IMG[a['slug']]
        page(path, a.get('ttl') or a['title'], a['desc'], a['h1'], article_body(a),
             [('Home', ''), ('Articles', 'articles/'), (a['title'], path)], photo=ph, article=True, og=ph,
             ld=[{'@context': 'https://schema.org', '@type': 'Article', 'headline': a['title'], 'description': a['desc'], 'datePublished': TODAY, 'dateModified': TODAY,
                  'author': {'@type': 'Organization', 'name': NAME, 'url': BASE}, 'publisher': {'@type': 'Organization', 'name': NAME, 'logo': {'@type': 'ImageObject', 'url': BASE + 'icon-512.png'}},
                  'image': abs_img(ph), 'mainEntityOfPage': BASE + path}])


def copy_images():
    """Copy the used client photos into site/img/ (same filenames) and make 480px-wide thumbs in site/img/thumb/."""
    global HAS_THUMB
    dst = os.path.join(OUT, 'img')
    tdir = os.path.join(OUT, 'thumb')
    os.makedirs(dst, exist_ok=True)
    os.makedirs(tdir, exist_ok=True)
    files = used_images()
    for f in files:
        shutil.copyfile(os.path.join(SRC_IMG, f), os.path.join(dst, f))
    try:
        from PIL import Image
        for f in files:
            with Image.open(os.path.join(SRC_IMG, f)) as im:
                w, h = im.size
                t = im.convert('RGB').resize((480, round(h * 480 / w)), Image.LANCZOS)
                t.save(os.path.join(tdir, f), 'WEBP', quality=74, method=4)
        HAS_THUMB = True
    except Exception as ex:
        print('PIL thumbs failed, using originals:', ex)
        HAS_THUMB = False
    return len(files)


def make_icons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0a1f38"/>'
           '<path d="M12 31 32 14l20 17h-5v18H17V31z" fill="#f7f8f9"/><rect x="27" y="35" width="10" height="14" rx="2" fill="#e8a33d"/></svg>')
    open(os.path.join(OUT, 'icon.svg'), 'w').write(svg)
    try:
        from PIL import Image, ImageDraw
        def draw(sz):
            im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            s = sz / 64.0
            d.rounded_rectangle([0, 0, sz - 1, sz - 1], radius=int(14 * s), fill=(10, 31, 56, 255))
            d.polygon([(12 * s, 31 * s), (32 * s, 14 * s), (52 * s, 31 * s), (47 * s, 31 * s), (47 * s, 49 * s), (17 * s, 49 * s), (17 * s, 31 * s)], fill=(247, 248, 249, 255))
            d.rounded_rectangle([27 * s, 35 * s, 37 * s, 49 * s], radius=int(2 * s), fill=(232, 163, 61, 255))
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
    load_dims()
    n_img = copy_images()
    build_pages()
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(render(path, p))
    # 404 (renders with absolute BASE paths so it works at any depth)
    nf = ('<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | JBStaycation</title>'
          '<meta name="robots" content="max-image-preview:large"><link rel="icon" href="%sicon.svg" type="image/svg+xml">%s%s<link rel="stylesheet" href="%sjb.css"></head><body class="inner has-stick">%s<main id="main"><div class="wrap nf"><p class="eyebrow">Error 404</p><h1>Page not found</h1><p class="lead">That page does not exist. Try our <a href="%s">home page</a>, the <a href="%sstays/">stays</a> or message us on WhatsApp.</p>%s</div></main>%s%s<script src="%sjb.js" defer></script><script src="%scta.js" defer></script></body></html>'
          % (BASE, HEAD_JS, FONT_LINKS, BASE, header_html(), BASE, BASE, wa_btn('WhatsApp us', wa_msg(), '404'), footer_html(), stick_bar('any'), BASE, BASE))
    nf = nf.replace('{R}', BASE).replace('<main id="main">', '<main id="main" style="padding-top:0">')
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)
    open(os.path.join(OUT, 'jb.css'), 'w').write(re.sub(r'\n+', '\n', CSS).strip() + '\n')
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
    open(os.path.join(OUT, 'site.webmanifest'), 'w').write(json.dumps({'name': NAME, 'short_name': NAME, 'start_url': BASE, 'display': 'browser', 'background_color': '#f7f8f9', 'theme_color': '#0a1f38',
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
        '<IfModule mod_headers.c>\n<FilesMatch "\\.(html|xml|txt)$">\nHeader set Cache-Control "public, max-age=3600"\n</FilesMatch>\n'
        '</IfModule>\n')
    print('pages:', len(PAGES) + 1, 'images:', n_img, 'thumbs:', HAS_THUMB, 'built into', OUT)


if __name__ == '__main__':
    main()

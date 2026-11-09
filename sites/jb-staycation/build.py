"""JB Airbnb demo preview: builds every page into site/ (python3 build.py).

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
OUT = os.environ.get('JB_OUT') or os.path.join(HERE, 'site')

BASE = 'https://jbairbnb.com/'   # live domain (Edwin 9 Nov 2026: official name JB Airbnb, domain jbairbnb.com); was pageonesingapore.com/preview/jb-staycation/
TODAY = '2026-11-09'
SITE_ID = 'jb-staycation'
NAME = 'JB Airbnb'
TAGLINE = 'A quieter escape, just across the causeway.'
WA_NUM, WA_SHOW = '6590062198', '+65 9006 2198'
WA_BASE = 'https://wa.me/' + WA_NUM


def wa_msg(house=None):
    """Prefilled WhatsApp text (strategy brief 9 Nov 2026). house = 'prima', 'landak' or None (please recommend). The enquiry form builds the same text with dates and guests."""
    label = {'prima': 'Prima', 'landak': 'Landak'}.get(house, 'Please recommend')
    return ("Hi, I'm planning a JB stay from Singapore. [House: %s]. Check-in: not decided. Check-out: not decided. Adults: not decided. Children: not decided. "
            "Please confirm availability and the final total in RM." % label)


# ---- one source for the RM price and the SGD estimate (recheck by hand before go-live; no live FX)
FX = {'myr': 500, 'rate': 0.3158, 'source_date': '6 Nov 2026', 'checked': '9 Nov 2026 SGT',
      'url': 'https://www.exchangerates.org.uk/MYR-SGD-spot-exchange-rates-history-2026.html'}
SGD_HOUSE = 'about S$%d' % round(FX['myr'] * FX['rate'])                      # about S$158
def sgd_pp(n):
    return 'about S$%.2f' % round(FX['myr'] / n * FX['rate'], 2)               # Prima 12 -> S$13.16, Landak 10 -> S$15.79 (rounded below)
SGD_PP = {'prima': 'about S$13.16', 'landak': 'about S$15.80'}                 # (old RM 500 figures, unused since 9 Nov pricing round)
# ---- nightly prices per house, cleaning included (host, confirmed by Edwin 9 Nov 2026)
PRICES = {'prima': (450, 650, 750), 'landak': (550, 750, 1000)}
TIER_NAMES = ('Weekday', 'Weekend', 'Public holiday')
def rm(n):
    return 'RM {:,}'.format(n)
def sgd_of(n):
    return 'S$%d' % round(n * FX['rate'])
def tiers_rm(k):
    a, b, c = PRICES[k]
    return '%s weekday, %s weekend, %s public holiday' % (rm(a), rm(b), rm(c))
def tiers_sgd(k):
    return 'about ' + ' / '.join(sgd_of(n) for n in PRICES[k])
def tiers_full(k):
    return '%s (%s)' % (tiers_rm(k), tiers_sgd(k))
PP_WEEKDAY = {k: 'about S$%.2f' % (PRICES[k][0] * FX['rate'] / g) for k, g in (('prima', 12), ('landak', 10))}   # Prima 11.84, Landak 17.37
def tiers_html(k, cls='tiers'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li><span>%s</span><b>%s</b><small>about %s</small></li>' % (t, rm(n), sgd_of(n)) for t, n in zip(TIER_NAMES, PRICES[k])))
DEPOSIT = 'A RM 1,000 refundable deposit applies to every booking and is refunded within 48 hours after checkout.'
PAY = ('Singapore guests pay by PayNow or PayLah to the host\'s mobile, and a receipt is issued. Malaysian guests pay in RM by bank transfer or TNG eWallet. '
       'Bank details are shared once your booking and dates are confirmed. You can also book through the Airbnb listing.')
PAY_SHORT = 'PayNow or PayLah from Singapore (receipt issued), bank transfer or TNG eWallet in RM from Malaysia, or the Airbnb listing'                 # brief figures: RM25 / RM50 per person at full occupancy
FX_TEXT = ('SGD estimate only; exchange rates vary. Based on RM1 = S$%s (%s; checked %s). The final total depends on your dates and group size.'
           % (FX['rate'], FX['source_date'], FX['checked']))


def fx_note():
    return ('<details class="fxn"><summary>About the SGD estimate</summary><p>%s Source: <a href="%s" rel="noopener">exchangerates.org.uk MYR/SGD history</a>.'
            ' RM is the price we quote; the SGD figure is not an SGD payment offer.</p></details>' % (FX_TEXT, FX['url']))

CONFIRM = [
    'Legal/business name of the host (kept off the site).',
    'Prima bedrooms: 3 (Edwin confirmed 8 Nov 2026 11:21 pm). Photos show two distinct bedrooms; the count is the host\'s.',
    'Prima minimum stay: "ask us" on every page (listing showed "Minimum 2" with no unit).',
    'Prima 900 sq ft (as stated by client); left off the page.',
    'Prima check-in/out times, quiet hours, deposit amount and house rules (none verified; pages say ask us on WhatsApp).',
    'No guest reviews are shown anywhere (Edwin, 8 Nov 2026): add only real, permitted reviews later.',
    'Deposit, cancellation and payment terms (client T&C is an unfilled template; no /terms/ page built).',
    'SGD equivalents: not shown until Edwin agrees.',
    'Google Business Profile, Airbnb, social links, email (none known; no sameAs).',
    'Brand colours/fonts: v2 uses the client site tokens (navy #0a1f38, amber #e8a33d, page #f7f8f9) and Geist from Google Fonts.',
    'Photos: Edwin\'s real photos only (jb-photos.zip, 8 Nov 2026), 14 Prima + 16 Landak, self-hosted in site/img/ (full) and site/thumb/ (800px). Each house uses only its own photos.',
    'Source conflicts kept at the site figure: Landak CIQ 10 min (Airbnb 12), Mid Valley Southkey 12 min (Airbnb 10).',
    'Host drive times (Tuas 10 min, Landak to CIQ about 12 min) are host estimates, not independently timed.',
    'Does the photo set include people/cars (privacy) and may we use them? (client own photos assumed).',
]


# ---------------------------------------------------------------- images (Edwin's real photos, self-hosted: site/img/ full size, site/thumb/ 800px)
SRC_IMG = os.path.join(HERE, 'photos-real')   # Edwin's real photos (jb-photos.zip, 8 Nov 2026): <name>.webp (max 1600) + <name>-800.webp
HERO_IMG = 'prima-hero-1600.webp'   # homepage hero ONLY: AI image Edwin chose 9 Nov 2026 (not Prima itself). Never use as a Prima photo, og:image or schema image.
HERO_ALT = 'Friends and family enjoying a JB staycation house with pool table'
HERO_V = '20261109'   # cache-buster for the hero files (same names were overwritten on the server)
OG_DEFAULT = 'prima-living-room-1.webp'   # real photo for og:image / schema
HERO_SET = {'desktop': 'prima-hero-1600.webp', 'small': 'prima-hero-800.webp', 'mobile': 'prima-hero-mobile-800.webp'}


def hero_picture():
    """<picture>: 4:5 phone crop up to 600px, otherwise 800/1600 srcset. Eager, fetchpriority=high, real width/height."""
    v = '?v=' + HERO_V
    return ('<picture><source media="(max-width:600px)" srcset="{R}img/%s%s" width="800" height="1000">'
            '<img src="{R}img/%s%s" srcset="{R}img/%s%s 800w, {R}img/%s%s 1600w" sizes="100vw" alt="%s" width="1600" height="900" fetchpriority="high" decoding="async"></picture>'
            % (HERO_SET['mobile'], v, HERO_SET['desktop'], v, HERO_SET['small'], v, HERO_SET['desktop'], v, e(HERO_ALT)))

# alt text per photo, written from the photo manifest (what is actually visible). Each house uses only its own photos.
ALT = {
    'prima-hero-1600.webp': HERO_ALT,
    'prima-living-room-1.webp': 'Wide living room at Prima with a grey sectional sofa and the pool table beyond',
    'prima-living-room-2.webp': 'Living room at Prima facing the windows',
    'prima-pool-table-1.webp': 'Indoor blue pool table at Prima',
    'prima-dining-room-1.webp': 'Dining table at Prima with the kitchen beyond',
    'prima-kitchen-1.webp': 'L-shaped kitchen at Prima with sink and countertop appliances',
    'prima-bedroom-a-1.webp': 'Bedroom at Prima with abstract prints, dark wall panels and a mirror',
    'prima-bedroom-b-1.webp': 'Bedroom at Prima with corner windows, balcony doors and a blue chair',
    'prima-dressing-area-1.webp': 'Dressing area at Prima with mirror, clothes rail and ironing board',
    'prima-blue-seating-area-1.webp': 'Blue seating area with a round table at Prima',
    'prima-study-desk-1.webp': 'Study desk and chair at Prima',
    'prima-covered-balcony-view-1.webp': 'Covered balcony at Prima with a bistro set and neighbourhood view',
    'prima-bathroom-1.webp': 'Bathroom at Prima with toilet, basin and mirror',
    'prima-shower-area-1.webp': 'Shower area at Prima with an electric shower',
    'prima-entrance-console-1.webp': 'Entrance console and plant at Prima',
    'prima-pool-table-dining-1.webp': 'Pool table in the foreground facing the dining area and kitchen at Prima',
    'prima-living-pool-table-2.webp': 'Wide living room at Prima with the pool table behind the sofa',
    'prima-pool-table-window-1.webp': 'Pool table facing the front window at Prima',
    'prima-living-pool-table-3.webp': 'Living room and TV at Prima with the pool table in the centre',
    'prima-dining-front-1.webp': 'Dining table and feature wall at Prima',
    'prima-dining-kitchen-wide-1.webp': 'Dining area and kitchen at Prima with windows and fridge',
    'prima-dining-kitchen-axis-1.webp': 'View from the dining table towards the kitchen at Prima',
    'prima-kitchen-fridge-1.webp': 'Kitchen at Prima with fridge and two windows',
    'prima-kitchen-sink-front-1.webp': 'Kitchen sink at Prima',
    'prima-bedroom-a-angle-2.webp': 'Bedroom at Prima with mirror and clothes rail',
    'prima-bedroom-a-bed-detail-1.webp': 'Bed and artwork in a bedroom at Prima',
    'prima-bedroom-b-angle-2.webp': 'Bed against a brown feature wall in a bedroom at Prima',
    'prima-bedroom-b-angle-3.webp': 'Bedroom at Prima with corner windows and balcony access',
    'prima-bedroom-b-seating-1.webp': 'Blue chair and TV corner in a bedroom at Prima',
    'prima-blue-seating-tv-1.webp': 'TV and round table in the blue seating area at Prima',
    'prima-blue-seating-wide-1.webp': 'Wide view of the blue seating and TV area at Prima',
    'prima-study-desk-angle-2.webp': 'Study desk and chair at Prima, seen from the side',
    'prima-balcony-side-1.webp': 'Covered balcony at Prima from the side, with the neighbourhood beyond',
    'prima-bathroom-wide-1.webp': 'Bathroom at Prima with basin, toilet and shower screen',
    'prima-tv-wall-1.webp': 'TV wall and coffee table at Prima',
    'prima-living-entry-angle-1.webp': 'Living room at Prima seen past the entry ledge',
    'landak-patio-bistro-pool-1.webp': 'Patio bistro table and pool table at Landak Kawan Fun House',
    'landak-pool-table-length-1.webp': 'View along the full length of the pool table at Landak Kawan Fun House',
    'landak-dartboards-detail-1.webp': '2 dart boards beside the 8ft pool table at Landak Kawan Fun House',
    'landak-living-tv-wide-1.webp': 'Living room at Landak Kawan Fun House looking towards the TV and front curtains',
    'landak-dining-room-wide-1.webp': 'Wide dining and kitchen view with the foosball table at Landak Kawan Fun House',
    'landak-living-daylight-angle-1.webp': 'Daylight living room at Landak Kawan Fun House seen from the dining side',
    'landak-living-daylight-angle-2.webp': 'Daylight living room at Landak Kawan Fun House looking towards the TV and window',
    'landak-bedroom-1-angle-3.webp': 'Bedroom with two beds at Landak Kawan Fun House, seen past the doorway',
    'landak-bathroom-portrait-1.webp': 'Bathroom at Landak Kawan Fun House with shower, toilet and basin',
    'landak-covered-counter-wide-1.webp': 'Covered counter and stools at Landak Kawan Fun House',
    'landak-staircase-1.webp': 'Staircase and covered roof at Landak Kawan Fun House',
    'landak-dining-table-detail-1.webp': 'Dining table set for a meal at Landak Kawan Fun House',
    'landak-breakfast-bar-portrait-1.webp': 'Kitchen breakfast bar at Landak Kawan Fun House',
    'landak-kitchen-appliances-1.webp': 'Microwave and countertop appliances at Landak Kawan Fun House',
    'landak-pool-table-detail-1.webp': 'Pool table felt, rack and balls at Landak Kawan Fun House',
    'landak-game-stick-detail-1.webp': 'Game stick connected behind the TV at Landak Kawan Fun House',
    'landak-tv-remote-detail-1.webp': 'TV remote at Landak Kawan Fun House',
    'landak-ironing-counter-detail-1.webp': 'Ironing counter and iron at Landak Kawan Fun House',
    'landak-kitchen-dishrack-1.webp': 'Dishes, sink and dish rack in the kitchen at Landak Kawan Fun House',
    'landak-kitchen-sink-detail-1.webp': 'Sink and washing-up area at Landak Kawan Fun House',
    'landak-electrical-controls-1.webp': 'Electrical panel and switches at Landak Kawan Fun House',
    'landak-living-room-1.webp': 'Wide living room at Landak Kawan Fun House opening to the dining area and kitchen',
    'landak-living-room-staircase-1.webp': 'Living room and staircase at Landak Kawan Fun House',
    'landak-breakfast-bar-living-room-1.webp': 'View across the breakfast counter to the living room at Landak Kawan Fun House',
    'landak-dining-foosball-1.webp': 'Dining area with foosball table and living room at Landak Kawan Fun House',
    'landak-pool-table-darts-1.webp': 'Covered patio with a blue 8ft pool table and 2 dart boards at Landak Kawan Fun House',
    'landak-patio-view-1.webp': 'Dartboards and bar stools on the covered patio at Landak Kawan Fun House',
    'landak-foosball-table-1.webp': 'Foosball table at Landak Kawan Fun House',
    'landak-tv-games-1.webp': 'TV and game controllers on the coffee table at Landak Kawan Fun House',
    'landak-kitchen-breakfast-bar-1.webp': 'Kitchen with fridge and breakfast counter at Landak Kawan Fun House',
    'landak-kitchen-sink-1.webp': 'Kitchen sink, dish rack and utensils at Landak Kawan Fun House',
    'landak-bedroom-1.webp': 'Bedroom with two double beds and a window at Landak Kawan Fun House',
    'landak-bedroom-1-angle-2.webp': 'Bedroom at Landak Kawan Fun House seen from the door, with dressing mirror',
    'landak-covered-work-counter-1.webp': 'Covered counter with iron and stools at Landak Kawan Fun House',
    'landak-bathroom-1.webp': 'Bathroom with shower, toilet and round mirror at Landak Kawan Fun House',
    'landak-bathroom-2.webp': 'Compact shower and toilet with round mirror at Landak Kawan Fun House',
    'landak-exterior-1.webp': 'Front of the double-storey Landak Kawan Fun House with its gate',
}

# Each room: (title, note, [(file, caption, caption_shown)])
def _r(k, title, note, files, caps=None):
    caps = caps or {}
    return (title, note, [(f, caps.get(f, title), f in caps) for f in files])

ROOMS = {
    'prima': [
        _r('prima', 'Living room', '', ['prima-living-room-1.webp', 'prima-living-pool-table-3.webp', 'prima-living-pool-table-2.webp', 'prima-living-room-2.webp', 'prima-tv-wall-1.webp', 'prima-blue-seating-wide-1.webp', 'prima-blue-seating-area-1.webp', 'prima-living-entry-angle-1.webp', 'prima-entrance-console-1.webp'],
           {'prima-blue-seating-wide-1.webp': 'Blue seating area', 'prima-blue-seating-area-1.webp': 'Blue seating area', 'prima-entrance-console-1.webp': 'Entrance', 'prima-tv-wall-1.webp': 'TV wall'}),
        _r('prima', 'Pool table', 'In the living room', ['prima-pool-table-dining-1.webp', 'prima-pool-table-1.webp', 'prima-pool-table-window-1.webp']),
        _r('prima', 'Dining and kitchen', '', ['prima-dining-kitchen-wide-1.webp', 'prima-dining-room-1.webp', 'prima-dining-front-1.webp', 'prima-kitchen-fridge-1.webp', 'prima-kitchen-1.webp'], {'prima-kitchen-fridge-1.webp': 'Kitchen', 'prima-kitchen-1.webp': 'Kitchen'}),
        _r('prima', 'Bedrooms', '3 bedrooms', ['prima-bedroom-b-angle-3.webp', 'prima-bedroom-b-1.webp', 'prima-bedroom-b-angle-2.webp', 'prima-bedroom-a-1.webp', 'prima-bedroom-a-angle-2.webp', 'prima-dressing-area-1.webp'],
           {'prima-bedroom-b-angle-3.webp': 'Bedroom', 'prima-bedroom-b-1.webp': 'Bedroom', 'prima-bedroom-b-angle-2.webp': 'Bedroom', 'prima-bedroom-a-1.webp': 'Bedroom', 'prima-bedroom-a-angle-2.webp': 'Bedroom', 'prima-dressing-area-1.webp': 'Dressing area'}),
        _r('prima', 'Study desk', '', ['prima-study-desk-1.webp']),
        _r('prima', 'Bathrooms', '3 bathrooms', ['prima-bathroom-wide-1.webp', 'prima-bathroom-1.webp', 'prima-shower-area-1.webp'], {'prima-shower-area-1.webp': 'Shower area'}),
        _r('prima', 'Balcony', 'Covered, with a bistro set', ['prima-covered-balcony-view-1.webp', 'prima-balcony-side-1.webp']),
    ],
    'landak': [
        _r('landak', 'Living and dining', '', ['landak-living-room-1.webp', 'landak-living-daylight-angle-1.webp', 'landak-living-daylight-angle-2.webp', 'landak-living-tv-wide-1.webp', 'landak-living-room-staircase-1.webp', 'landak-dining-room-wide-1.webp', 'landak-dining-foosball-1.webp', 'landak-breakfast-bar-living-room-1.webp', 'landak-dining-table-detail-1.webp', 'landak-staircase-1.webp']),
        _r('landak', 'Games', 'Pool table, darts, foosball, TV with arcade', ['landak-pool-table-darts-1.webp', 'landak-patio-bistro-pool-1.webp', 'landak-pool-table-length-1.webp', 'landak-dartboards-detail-1.webp', 'landak-patio-view-1.webp', 'landak-foosball-table-1.webp', 'landak-tv-games-1.webp'],
           {'landak-pool-table-darts-1.webp': '8ft pool table and 2 dart boards', 'landak-dartboards-detail-1.webp': 'Two dartboards', 'landak-foosball-table-1.webp': 'Foosball table', 'landak-tv-games-1.webp': 'TV with game controllers'}),
        _r('landak', 'Kitchen', 'For light cooking', ['landak-kitchen-breakfast-bar-1.webp', 'landak-breakfast-bar-portrait-1.webp', 'landak-kitchen-sink-1.webp', 'landak-kitchen-appliances-1.webp']),
        _r('landak', 'Bedrooms', '3 bedrooms, 1 king and 4 queen beds', ['landak-bedroom-1.webp', 'landak-bedroom-1-angle-3.webp', 'landak-bedroom-1-angle-2.webp'], {'landak-bedroom-1.webp': 'Bedroom', 'landak-bedroom-1-angle-3.webp': 'Bedroom, from the door', 'landak-bedroom-1-angle-2.webp': 'Bedroom, second angle'}),
        _r('landak', 'Bathrooms', '3 bathrooms', ['landak-bathroom-1.webp', 'landak-bathroom-portrait-1.webp', 'landak-bathroom-2.webp']),
        _r('landak', 'Laundry counter', '', ['landak-covered-counter-wide-1.webp', 'landak-covered-work-counter-1.webp']),
        _r('landak', 'Outside', 'Parking for 2 cars inside the gate', ['landak-exterior-1.webp']),
    ],
}
# hero gallery (first 5 photos on each house page; swipe carousel)
BENTO = {
    'prima': ['prima-living-room-1.webp', 'prima-dining-room-1.webp', 'prima-bedroom-b-1.webp', 'prima-covered-balcony-view-1.webp', 'prima-living-room-2.webp'],
    'landak': ['landak-living-room-1.webp', 'landak-pool-table-darts-1.webp', 'landak-bedroom-1.webp', 'landak-dining-foosball-1.webp', 'landak-exterior-1.webp'],
}
# house cards (main photo + 3-photo strip), each house only its own photos
CARD_IMG = {
    'prima': ['prima-living-room-2.webp', 'prima-pool-table-1.webp', 'prima-bedroom-a-1.webp', 'prima-covered-balcony-view-1.webp'],
    'landak': ['landak-living-room-staircase-1.webp', 'landak-foosball-table-1.webp', 'landak-bedroom-1-angle-2.webp', 'landak-patio-view-1.webp'],
}
# page and article photos
PAGE_IMG = {
    'stays': 'prima-living-room-1.webp', 'prices': 'landak-breakfast-bar-living-room-1.webp', 'getting-there': 'prima-covered-balcony-view-1.webp',
    'faq': 'landak-living-room-staircase-1.webp', 'about': 'prima-living-room-2.webp', 'contact': 'landak-dining-foosball-1.webp',
    'jb-homestay-for-big-groups-12-guests': 'prima-blue-seating-area-1.webp',
    'staying-near-ksl-city-mall-what-is-within-5-15-minutes': 'landak-pool-table-darts-1.webp',
    'causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay': 'landak-patio-view-1.webp',
}
HOME_MOSAIC = ['landak-pool-table-darts-1.webp', 'prima-dining-room-1.webp', 'landak-tv-games-1.webp']
# /stays cards: 10 photos each, real photos only
STAYS_IMG = {
    'prima': ['prima-living-room-1.webp', 'prima-living-pool-table-3.webp', 'prima-pool-table-dining-1.webp', 'prima-dining-kitchen-wide-1.webp', 'prima-bedroom-b-angle-3.webp',
              'prima-bedroom-a-1.webp', 'prima-blue-seating-wide-1.webp', 'prima-covered-balcony-view-1.webp', 'prima-kitchen-fridge-1.webp', 'prima-bathroom-wide-1.webp'],
    'landak': ['landak-living-daylight-angle-1.webp', 'landak-pool-table-darts-1.webp', 'landak-patio-bistro-pool-1.webp', 'landak-dining-room-wide-1.webp', 'landak-foosball-table-1.webp',
               'landak-tv-games-1.webp', 'landak-bedroom-1.webp', 'landak-kitchen-breakfast-bar-1.webp', 'landak-bathroom-1.webp', 'landak-exterior-1.webp'],
}
STAYS_BAND_IMG = 'landak-living-daylight-angle-2.webp'
# full albums on /stays (every real photo from jb-photos-v2 except prima-living-daylight-wide-1, the old layout), grouped by room; phones show each group as a swipe strip
ALBUM = {
    'prima': [
        ('Living, kitchen and dining', ['prima-living-room-1.webp', 'prima-living-room-2.webp', 'prima-living-pool-table-2.webp', 'prima-living-pool-table-3.webp', 'prima-tv-wall-1.webp', 'prima-living-entry-angle-1.webp', 'prima-entrance-console-1.webp', 'prima-blue-seating-wide-1.webp', 'prima-blue-seating-area-1.webp', 'prima-blue-seating-tv-1.webp', 'prima-dining-kitchen-wide-1.webp', 'prima-dining-room-1.webp', 'prima-dining-front-1.webp', 'prima-dining-kitchen-axis-1.webp', 'prima-kitchen-fridge-1.webp', 'prima-kitchen-1.webp', 'prima-kitchen-sink-front-1.webp']),
        ('Bedrooms and study', ['prima-bedroom-b-angle-3.webp', 'prima-bedroom-b-1.webp', 'prima-bedroom-b-angle-2.webp', 'prima-bedroom-b-seating-1.webp', 'prima-bedroom-a-1.webp', 'prima-bedroom-a-angle-2.webp', 'prima-bedroom-a-bed-detail-1.webp', 'prima-dressing-area-1.webp', 'prima-study-desk-1.webp', 'prima-study-desk-angle-2.webp']),
        ('Bathrooms', ['prima-bathroom-wide-1.webp', 'prima-bathroom-1.webp', 'prima-shower-area-1.webp']),
        ('Games: pool table', ['prima-pool-table-dining-1.webp', 'prima-pool-table-1.webp', 'prima-pool-table-window-1.webp']),
        ('Outside: covered balcony', ['prima-covered-balcony-view-1.webp', 'prima-balcony-side-1.webp']),
    ],
    'landak': [
        ('Living, kitchen and dining', ['landak-living-room-1.webp', 'landak-living-daylight-angle-1.webp', 'landak-living-daylight-angle-2.webp', 'landak-living-tv-wide-1.webp', 'landak-living-room-staircase-1.webp', 'landak-breakfast-bar-living-room-1.webp', 'landak-staircase-1.webp', 'landak-dining-room-wide-1.webp', 'landak-dining-table-detail-1.webp', 'landak-kitchen-breakfast-bar-1.webp', 'landak-breakfast-bar-portrait-1.webp', 'landak-kitchen-sink-1.webp', 'landak-kitchen-sink-detail-1.webp', 'landak-kitchen-dishrack-1.webp', 'landak-kitchen-appliances-1.webp']),
        ('Bedroom', ['landak-bedroom-1.webp', 'landak-bedroom-1-angle-3.webp', 'landak-bedroom-1-angle-2.webp']),
        ('Bathrooms', ['landak-bathroom-1.webp', 'landak-bathroom-2.webp', 'landak-bathroom-portrait-1.webp']),
        ('Games: pool table, darts, foosball, TV arcade', ['landak-pool-table-darts-1.webp', 'landak-patio-bistro-pool-1.webp', 'landak-pool-table-length-1.webp', 'landak-pool-table-detail-1.webp', 'landak-dartboards-detail-1.webp', 'landak-patio-view-1.webp', 'landak-foosball-table-1.webp', 'landak-dining-foosball-1.webp', 'landak-tv-games-1.webp', 'landak-game-stick-detail-1.webp', 'landak-tv-remote-detail-1.webp']),
        ('Outside, laundry and utility', ['landak-exterior-1.webp', 'landak-covered-counter-wide-1.webp', 'landak-covered-work-counter-1.webp', 'landak-ironing-counter-detail-1.webp', 'landak-electrical-controls-1.webp']),
    ],
}
HOME_CTA_IMG = 'landak-living-room-1.webp'


def _alt_for(f):
    return ALT.get(f, 'JB Airbnb holiday house in Johor Bahru')


def used_images():
    s = {HERO_IMG, HOME_CTA_IMG, STAYS_BAND_IMG} | set(HOME_MOSAIC) | set(PAGE_IMG.values()) | set(STAYS_IMG['prima']) | set(STAYS_IMG['landak']) | {f for k in ALBUM for _g, fs in ALBUM[k] for f in fs}
    for k in ROOMS:
        for _t, _n, ph in ROOMS[k]:
            s |= {p[0] for p in ph}
        s |= set(BENTO[k]) | set(CARD_IMG[k])
    return sorted(s)


DIM = {}
TDIM = {}
HAS_THUMB = False


def load_dims():
    try:
        from PIL import Image
        for f in used_images():
            with Image.open(os.path.join(SRC_IMG, f)) as im:
                DIM[f] = im.size
            if os.path.exists(os.path.join(SRC_IMG, f[:-5] + '-800.webp')):
                with Image.open(os.path.join(SRC_IMG, f[:-5] + '-800.webp')) as im:
                    TDIM[f] = im.size
    except Exception as ex:
        print('PIL not available, assuming 1200x900:', ex)


def dims(f):
    return DIM.get(f, (1200, 900))


def tdims(f):
    return TDIM.get(f, (800, 600))


def abs_img(f):
    return BASE + 'img/' + f


# ---- the 15 master FAQs (strategy brief 9 Nov 2026). Pages use subsets; FAQPage markup only lists what the page shows.
FAQ15 = {
    'cost': ('How much does a whole house cost in SGD?', 'Prices are per night for the whole house, cleaning included. Prima: ' + tiers_full('prima') + '. Landak Kawan Fun House: ' + tiers_full('landak') + '. For your group size or a gathering, WhatsApp Daniel. The SGD figures are estimates using RM1 = S$0.3158, checked on 9 November 2026 SGT against the latest displayed market observation dated 6 November. Exchange rates vary.'),
    'fit': ('Which house suits our group?', 'Prima, a landed house, takes up to 12 guests in 3 rooms, each with 1 queen bed and 2 single floor mattresses, with 3 bathrooms, a 7ft pool table and a mahjong table. Landak Kawan Fun House takes up to 10 guests in 3 bedrooms with 5 beds (1 king, 4 queens) and 3 bathrooms, with an 8ft pool table, darts, foosball, mahjong and a 5-minute walk to KSL City Mall.'),
    'safe': ('Is this a safe stay, and who will we deal with?', 'You deal directly with Daniel, our host, who is based in Singapore and JB, understands both cultures and speaks English, Malay and Chinese. Daniel is your emergency contact during the stay. Each house has a fire extinguisher under the kitchen sink and outdoor CCTV. Self check-in details are sent after a firm booking.'),
    'time': ('How long does it take from Singapore, including CIQ queues?', 'Prima is about 10 minutes from the Tuas Second Link on the Malaysian side, according to the host. Landak is in Taman Abad, a 5-minute walk from KSL City Mall. These are not door-to-door journey times from Singapore. Border queues and traffic add time; check ICA and LTA traffic updates before leaving.'),
    'car': ('What should I prepare before driving a Singapore car to JB?', 'Check JPJ’s official VEP portal for your vehicle’s registration and RFID requirements, and have valid road tax and insurance. Singapore Customs requires applicable fuel tanks to be at least three-quarters full when leaving by land. Foreign-registered petrol cars should use RON97, not subsidised RON95. Check current official rules before travel; tolls and road charges are separate from accommodation.'),
    'park': ('Where can we park?', 'Prima has parking for 2 cars inside and 6 cars outside. Landak has parking for 2 cars inside. Parking is not a guarantee against loss or damage.'),
    'pay': ('How do we pay?', PAY + ' An SGD estimate on this site is not an SGD price.'),
    'cancel': ('Is there a deposit, and what happens if we cancel?', DEPOSIT + ' There is no cancellation, but you can change your dates once.'),
    'clean': ('How clean is the house, and are linen and towels included?', 'The house is professionally cleaned after every checkout, with fresh linen, towels and toiletries provided. Cleaning is included in the nightly price.'),
    'gather': ('Can we celebrate a birthday or have a company gathering?', 'Yes, with the host\'s approval. Visitors are allowed, and quiet hours are 11pm to 7am. The RM 1,000 refundable deposit applies, as for every booking. WhatsApp Daniel with your group size and plans. These are homes with neighbours, not unrestricted venues.'),
    'checkin': ('When can we check in, and is one night possible?', 'Both houses: check-in 3pm, check-out 11am. Self check-in details are sent after a firm booking. Early check-in and late checkout cost RM 100 an hour, subject to availability, and you can ask for a waiver. The minimum stay is 1 night, or 2 nights over Christmas Eve and Christmas Day.'),
    'nocar': ('Can we come without a car, and is there food nearby?', 'Landak is a 5-minute walk from KSL City Mall. Prima is in Gelang Patah, Iskandar Puteri. See the nearby-place guides and map links to plan food and outings. Check local Grab availability, fares and your onward transport before travelling; no pickup, shuttle or cross-border ride is included.'),
    'kids': ('Are the houses suitable for children and elderly guests?', 'Prima has a ground-floor bedroom, so elderly guests do not need to use the stairs. Landak has board games and a children\'s playroom, but is a double-storey house with stairs. WhatsApp Daniel to check cots, ground-floor rooms or mobility needs for your group. Neither house is advertised as wheelchair-accessible or childproof.'),
    'pool': ('What activities and facilities are included?', 'Prima has a 7ft pool table and a mahjong table. Landak has an 8ft pool table, foosball, 2 dart boards, a mahjong table, a TV arcade, board games, a children\'s playroom, a dedicated workstation and advertised 100Mbps Wi-Fi. No BBQ at either house. No meals, transport or attraction tickets are included.'),
    'help': ('Who helps if there is a problem during our stay?', 'Daniel, the host, is your emergency contact during the stay. Message +65 9006 2198. Self check-in details are sent after a firm booking.'),
}
def faqs(*keys):
    return [FAQ15[k] for k in keys]
FAQ_GROUPS = [('Price and booking', ['cost', 'pay', 'cancel', 'checkin']), ('Choosing a house', ['fit', 'pool', 'park', 'clean', 'gather', 'kids']),
              ('Getting there', ['time', 'car', 'nocar']), ('Who you deal with', ['safe', 'help'])]

# ---------------------------------------------------------------- houses
HOUSES = {
    'prima': {
        'slug': 'prima-taman-nusantara-prima', 'name': 'Prima', 'full': 'Prima, Taman Nusantara Prima',
        'short': 'Prima at Taman Nusantara Prima',
        'street': '19 Jalan Prima 3/1, Taman Nusantara Prima', 'locality': 'Iskandar Puteri', 'region': 'Johor', 'postal': '79200',
        'addr': '19 Jalan Prima 3/1, Taman Nusantara Prima, Iskandar Puteri, Johor 79200, Malaysia',
        'guests': 12, 'price': 450, 'minstay': 'Minimum stay: 1 night (2 over Christmas Eve and Day)', 'beds': 3, 'rating': 'Rated 4.67 from 6 Airbnb reviews',
        'tag': 'Group homestay with a 7ft pool table, mahjong and parking for 8 cars',
        'card': 'A private landed house in Gelang Patah, Iskandar Puteri for up to 12 guests with a 7ft pool table in the living room, a mahjong table and parking for 8 cars, about 10 minutes from the Tuas Second Link (host estimate).',
        'bestfor': 'Best for big family and friends gatherings near LEGOLAND and Puteri Harbour, about 10 min from the Tuas Second Link',
        'top': ['7ft pool table', 'Mahjong', 'Parking for 8 cars', '3 queen beds + 6 floor mattresses', 'Ground-floor bedroom, no stairs'],
        'stats': [('Guests', 'Up to 12'), ('Bedrooms', '3'), ('Bathrooms', '3'), ('Weekday', 'RM 450 a night')],
        'intro': ['Prima is a private landed holiday house in Taman Nusantara Prima, Gelang Patah, Iskandar Puteri, for up to 12 guests. It is RM 450 a night on weekdays, RM 650 on weekends and RM 750 on public holidays, cleaning included. It has 3 rooms, each with 1 queen bed and 2 single floor mattresses, and 3 bathrooms, including a ground-floor bedroom so elderly guests do not need the stairs, with a 7ft pool table in the living room and a mahjong table for group gatherings.',
                  'There is about 2,500 sq ft to spread out in: a living room with a 7ft pool table, a dining area and kitchen, a study desk, a dressing area and a covered balcony with a bistro set. Two TVs with Netflix, Wi-Fi, a washer and air conditioning are included, and there is parking for 2 cars inside and 6 cars outside.',
                  'The host estimates about 10 minutes from the Tuas Second Link on the Malaysian side, excluding border queues, which makes it a natural pick if you cross by the Second Link. LEGOLAND Malaysia and Sunway Big Box are about a 15-minute drive.'],
        'amen': ['7ft pool table', 'Mahjong table', 'Ground-floor bedroom (no stairs needed)', 'Wi-Fi', 'Air conditioning', 'Kitchen', 'Parking: 2 cars inside, 6 outside',
                 '2 TVs with Netflix', 'Washer', 'Covered balcony', 'Study desk', 'Self check-in'],
        'rules': ['Check-in 3:00 pm, check-out 11:00 am. Self check-in details are sent after a firm booking.', 'Early check-in or late checkout: RM 100 an hour, subject to availability. You can ask for a waiver.', 'No pets.',
                  'No smoking or vaping indoors: RM 500 penalty.', 'No eating durian indoors: RM 500 penalty.', 'No BBQ.',
                  'Visitors are allowed. Quiet hours 11:00 pm to 7:00 am. Guests must not disturb neighbours.', 'Please send a copy of your ID by WhatsApp before check-in.',
                  'Gatherings need the host\'s approval.', DEPOSIT],
        'near': [('Tuas Second Link', 'about 10 min drive'), ('LEGOLAND Malaysia', 'about 15 min drive'), ('Sunway Big Box', 'about 15 min drive'), ('Puteri Harbour', 'about 15-20 min drive')],
        'near_note': 'Drive times are estimates measured from the house on the Malaysian side; they exclude border queues and depend on traffic.',
        'faq': faqs('fit', 'checkin', 'park', 'gather', 'pool') + [
            ('What are the beds at Prima?', 'Prima has 3 rooms, each with 1 queen bed and 2 single floor mattresses, for up to 12 guests.'),
        ],
        'msg': wa_msg('prima'),
        'key': 'prima',
    },
    'landak': {
        'slug': 'landak-kawan-fun-house-taman-abad', 'name': 'Landak Kawan Fun House', 'full': 'Landak Kawan Fun House, Taman Abad',
        'short': 'Landak Kawan Fun House',
        'street': 'Jalan Landak Kawan 2, Taman Abad', 'locality': 'Johor Bahru', 'region': 'Johor', 'postal': '80250',
        'addr': 'Jalan Landak Kawan 2, Taman Abad, Johor Bahru, Johor 80250, Malaysia',
        'guests': 10, 'price': 550, 'minstay': 'Minimum stay: 1 night (2 over Christmas Eve and Day)', 'beds': 3, 'rating': 'Rated 5.0 from 4 Airbnb reviews',
        'tag': 'KSL landed fun house a 5-minute walk from KSL City Mall',
        'bestfor': 'Best for groups who want to walk to KSL City Mall, food and the onsen',
        'top': ['8ft pool table', 'Foosball', '2 dart boards', 'Mahjong table', '5-min walk to KSL City Mall'],
        'card': 'A new double-storey landed fun house for up to 10 guests with an 8ft pool table, foosball, 2 dart boards, a mahjong table and a TV arcade, a 5-minute walk from KSL City Mall.',
        'stats': [('Guests', 'Up to 10'), ('Bedrooms', '3'), ('Bathrooms', '3'), ('Weekday', 'RM 550 a night')],
        'intro': ['Landak Kawan Fun House is a new double-storey house in Taman Abad, Johor Bahru, completed in September 2026, a 5-minute walk from KSL City Mall. It sleeps up to 10 guests at RM 550 a night on weekdays, RM 750 on weekends and RM 1,000 on public holidays, cleaning included, with 3 bedrooms, 3 bathrooms with water heaters, an 8ft pool table, foosball and 2 dart boards.',
                  'The 5 beds are 1 king plus 4 queens. The fun is built in: an 8ft pool table and 2 dart boards on the covered patio, a foosball table, a mahjong table, a 55-inch TV arcade, board games, a children\'s playroom and a dedicated workstation.',
                  'Wi-Fi is 100 Mbps, the kitchen is set up for light cooking, and 2 cars park inside the gate. The host estimates about 12 minutes by car to JB City Square and the Causeway CIQ, excluding border queues, and Mid Valley Southkey is about a 10-minute drive.'],
        'amen': ['8ft pool table', 'Foosball table', '2 dart boards', 'Mahjong table', '55-inch TV arcade', 'Board games', 'Children\'s playroom', 'Dedicated workstation', '3 bathrooms with water heaters', '100 Mbps Wi-Fi', 'Air conditioning',
                 'Kitchen for light cooking', 'Parking for 2 cars inside', 'Washer', 'Hair dryer', 'Iron', 'Self check-in'],
        'rules': ['Check-in 3:00 pm, check-out 11:00 am. Self check-in details are sent after a firm booking.', 'Early check-in or late checkout: RM 100 an hour, subject to availability. You can ask for a waiver.', 'No pets.',
                  'No smoking or vaping indoors: RM 500 penalty.', 'No eating durian indoors: RM 500 penalty.', 'No BBQ.',
                  'Visitors are allowed. Quiet hours 11:00 pm to 7:00 am. Guests must not disturb neighbours.',
                  'Gatherings need the host\'s approval.', DEPOSIT],
        'near': [('KSL City Mall', '5-min walk'), ('Yu Ee hawker (host tip)', 'about 3 min walk'), ('Mid Valley Southkey', 'about 10 min drive'), ('JB City Square and Causeway CIQ', 'about 12 min drive')],
        'near_note': 'Drive times are host estimates, excluding border queues and traffic.',
        'faq': faqs('checkin', 'park', 'kids', 'pool', 'nocar') + [
            ('Are pets, smoking or BBQ allowed?', 'No pets. No smoking or vaping indoors: RM 500 penalty. No eating durian indoors: RM 500 penalty. No BBQ. Quiet hours are 11:00 pm to 7:00 am.'),
        ],
        'msg': wa_msg('landak'),
        'key': 'landak',
    },
}
ORDER = ['prima', 'landak']
H1S = {'prima': 'JB homestay near Tuas Second Link: Prima', 'landak': 'JB homestay near KSL: Landak Kawan Fun House'}
ANSWER = {'prima': 'Prima is a private landed house in Gelang Patah, Iskandar Puteri for up to 12 guests, with 3 bedrooms and 3 bathrooms. It has a 7ft pool table and a mahjong table, and a ground-floor bedroom for elderly guests, plus parking for 2 cars inside and 6 outside. The host estimates about 10 minutes from Tuas Second Link, excluding border queues. WhatsApp Daniel for your dates.',
          'landak': 'Landak Kawan Fun House is a newly built September 2026 house in Taman Abad for up to 10 guests, with 3 bedrooms, 5 beds and 3 bathrooms. It is a 5-minute walk from KSL City Mall and has an 8ft pool table, darts, foosball, mahjong, 100Mbps Wi-Fi and 2 parking spaces. No BBQ.'}
SLEEP = {'prima': ['Up to 12 guests in 3 rooms with 3 bathrooms.', 'Each room has 1 queen bed and 2 single floor mattresses.', 'One bedroom is on the ground floor, so elderly guests do not need the stairs.'],
         'landak': ['Up to 10 guests in 3 bedrooms with 3 bathrooms (with water heaters).', '5 beds: 1 king and 4 queens (bedrooms 2 and 3 each have two queens).']}


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
        'slug': 'jb-homestay-for-big-groups-12-guests',
        'title': 'JB homestay for big groups: planning for 10-12 guests',
        'ttl': 'JB Homestay for Big Groups: Plan a Group Stay of 10-12',
        'desc': 'Plan a JB homestay for big groups with honest guest limits, a whole-house cost split and bedding questions. Compare the two houses before enquiring.',
        'h1': 'JB homestay for big groups: planning for 10-12 guests',
        'answer': 'For 10 people, Landak Kawan Fun House in Taman Abad sleeps up to 10 with 3 bedrooms and 5 beds. For up to 12, Prima, a landed house in Taman Nusantara Prima, has 3 bedrooms and 3 bathrooms, with a 7ft pool table and a mahjong table. Prima is RM 450 and Landak RM 550 a night on weekdays, cleaning included, booked on WhatsApp.',
        'house': 'prima', 'img': 'prima',
        'sections': [
            ('Why a whole house suits a big group', ['One house keeps everyone together: one kitchen, one living area, one place to park. You split the nightly rate across the group, and nobody is booking six separate hotel rooms.',
                'Both JB Airbnb houses are private homes in Johor Bahru, not shared buildings.']),
            ('Up to 10 guests: Landak Kawan Fun House', ['<a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad has 3 bedrooms, 3 bathrooms, 1 king bed and 4 queen beds (bedrooms 2 and 3 each have two queens), and the bathrooms have water heaters. It is ' + tiers_full('landak') + ' a night for the whole house, cleaning included, and the minimum stay is 1 night (2 over Christmas Eve and Christmas Day).',
                'For entertainment it has an 8ft pool table, a foosball table, 2 dart boards, a mahjong table, a 55-inch TV arcade and a children\'s playroom, plus a dedicated workstation. Wi-Fi is 100 Mbps.']),
            ('Up to 12 guests: Prima', ['<a href="{R}stays/prima-taman-nusantara-prima/">Prima</a>, a landed house in Taman Nusantara Prima, Iskandar Puteri, takes up to 12 guests in 3 bedrooms with 3 bathrooms, including a ground-floor bedroom for elderly guests. It is ' + tiers_full('prima') + ' a night, cleaning included, and the minimum stay is 1 night (2 over Christmas Eve and Christmas Day).',
                'Each of the 3 rooms has 1 queen bed and 2 single floor mattresses. It has a 7ft pool table, a mahjong table, a study desk and a covered balcony, plus a kitchen, 2 TVs with Netflix and parking for 2 cars inside and 6 outside, in about 2,500 sq ft.']),
            ('Getting your group across', ['Many groups drive. The host estimates Prima is about 10 minutes from the Tuas Second Link and Landak about 12 minutes from the Causeway CIQ, excluding border queues. See our <a href="{R}getting-there/">guide to getting to Johor Bahru</a> for the Causeway, Second Link and RTS Link options.']),
            ('Splitting the cost', ['Prices are per night for the whole house, cleaning included. On a weekday at full occupancy that is ' + PP_WEEKDAY['prima'] + ' per person at Prima (RM 450, 12 guests) and ' + PP_WEEKDAY['landak'] + ' at Landak (RM 550, 10 guests). Weekends and public holidays cost more; see <a href="{R}prices/">prices</a>. ' + FX_TEXT]),
            ('Bigger than 12?', ['Neither house takes more than 12 guests on its own. Booking both houses means two separate homes in different parts of JB, up to 22 guests in total, not one venue. Ask us what works for your group.']),
            ('Before you pay', [PAY + ' Cleaning is included in the nightly price.',
                'House rules at both houses: check-in 3pm, check-out 11am; quiet hours 11pm to 7am; RM 500 penalty for smoking or vaping indoors, or eating durian indoors; no BBQ; no pets; cleaning included.',
                DEPOSIT + ' There is no cancellation, but you can change your dates once. Gatherings need the host\'s approval. Visitors are allowed; quiet hours are 11pm to 7am.']),
            ('How to ask about dates', ['Message us on WhatsApp with your house choice, dates and the number of adults and children. Read the <a href="{R}articles/">JB guide for Singaporeans</a> for the crossing and first-time tips.']),
        ],
    },
    {
        'slug': 'staying-near-ksl-city-mall-what-is-within-5-15-minutes',
        'title': 'JB staycation near KSL: plan your weekend',
        'ttl': 'JB Staycation near KSL: A Walkable Weekend Guide',
        'desc': 'Plan a JB staycation near KSL with food, mall and map links from the Landak area. See the 10-guest house and ask about your weekend dates.',
        'h1': 'JB staycation near KSL: plan your weekend',
        'answer': 'Landak Kawan Fun House in Taman Abad is about a 5-minute walk to KSL City Mall and about 3 minutes on foot to the Yu Ee hawker stalls (host tip). Mid Valley Southkey is about a 10-minute drive, and JB City Square and the Causeway CIQ about 12 minutes (host estimate, excluding border queues).',
        'house': 'landak', 'img': 'landak', 'wa': 'landak',
        'sections': [
            ('Walking distance', ['<a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> is about a 5-minute walk from KSL City Mall, handy for meals, shopping and anything you forgot to pack.',
                'The Yu Ee hawker centre is about 3 minutes away, as stated by the host.']),
            ('Food and shopping on foot', ['Inside KSL City Mall (about a 5-minute walk) there is a supermarket on LG for groceries, You Kee XO for char siew and crispy siew yoke, and Tao Yuan for local snacks to bring home. On Mondays only, the KSL Monday Night Market on Jalan Seladang is about a 5-minute walk.',
                'Nearby on foot (about 5-10 minutes): Restoran Yit Foh for wanton noodles and Holiday Plaza for haircuts, nails and massage. See the <a href="{R}stays/landak-kawan-fun-house-taman-abad/#around">Around the house</a> section for map links and sample weekend plans. Opening hours change, so check Google Maps before you go.']),
            ('Within 10-12 minutes by car', ['Mid Valley Southkey is about a 10-minute drive. JB City Square and the Causeway CIQ are about 12 minutes away (host estimate).']),
            ('About these times', ['All times other than the 5-minute walk are drive times stated by the host. Traffic, especially around the checkpoints on weekends and holidays, can change them.']),
            ('Why this suits a weekend away', ['You can walk to a mall, then spend the evening at home with the pool table, foosball, darts and arcade TV. Wi-Fi is 100 Mbps. The house sleeps up to 10, with check-in after 3:00 pm and check-out before 11:00 am.',
                'The whole house is ' + tiers_full('landak') + ' a night, cleaning included (' + PP_WEEKDAY['landak'] + ' per person on a weekday at 10 guests; an estimate). Planning the trip? Read <a href="{R}articles/causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay/">which way to cross</a>, the <a href="{R}articles/">JB guide for Singaporeans</a>, or message us on WhatsApp for dates.']),
        ],
    },
    {
        'slug': 'causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay',
        'title': 'Causeway, Second Link or RTS: which way to JB for a weekend stay',
        'ttl': 'Causeway, Second Link or RTS: Which Way to JB?',
        'desc': 'Woodlands Causeway, Tuas Second Link or the RTS Link? What official sources say, and which JB Airbnb house suits each route.',
        'h1': 'Causeway, Second Link or RTS: which way to JB for a weekend stay',
        'answer': 'By road, Singapore has two land checkpoints: Woodlands and Tuas. The RTS Link train between Woodlands North and Bukit Chagar is now expected to start passenger service in February 2027, subject to safety certification (LTA, 2 Oct 2026). Prima is closer to Tuas; Landak to the Causeway CIQ.',
        'house': 'landak', 'img': 'landak',
        'sections': [
            ('By road: Woodlands or Tuas', ['ICA operates the land checkpoints at Woodlands and Tuas and lists traffic updates on its <a href="' + SRC['ica_traffic'][1] + '" rel="noopener">driving in and out of Singapore page</a>. Check it before you leave, especially on long weekends.',
                'You must bring your passport. ICA says so on its <a href="' + SRC['ica_qr'][1] + '" rel="noopener">QR code clearance page</a> (updated 27 Oct 2026), even when you use QR clearance.']),
            ('By train: the RTS Link', ['The RTS Link connects Woodlands North in Singapore with Bukit Chagar in Johor Bahru. LTA describes a train journey of about five minutes between the stations, with Customs, Immigration and Quarantine facilities co-located so you clear both countries before boarding (<a href="' + SRC['lta_rts'][1] + '" rel="noopener">LTA project page</a>).',
                'On 2 October 2026 LTA published that passenger service is now expected to start in February 2027, subject to independent safety certification and final approvals (<a href="' + SRC['lta_feb'][1] + '" rel="noopener">LTA news release</a>). Until it opens, plan on road or other existing routes.']),
            ('Which house for which route', ['<a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Gelang Patah, Iskandar Puteri is about 10 minutes from the Tuas Second Link on the Malaysian side (host estimate, excluding queues), so it suits groups driving in via the Second Link.',
                '<a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad is about 12 minutes from the Causeway CIQ (host estimate) and a 5-minute walk from KSL City Mall, so it suits groups arriving at the Johor Bahru city side.']),
            ('Not yet confirmed', ['We have not listed RTS fares or the door-to-door time from Bukit Chagar to either house, because we have no official figure for them. Ask us on WhatsApp if you need help planning.']),
        ],
    },
]


# Airbnb listings (Edwin's team, 9 Nov 2026). Ratings recorded 8 Nov 2026; no review quotes.
AIRBNB = {'prima': 'https://www.airbnb.co.uk/rooms/1712988048076930096', 'landak': 'https://www.airbnb.co.uk/rooms/1738320132895126027'}
RATING_READ = '8 Nov 2026'


def rating_link(k, text=None):
    return ('<a class="rlink" href="%s" rel="nofollow noopener" target="_blank">%s</a> <span class="rdate">(read %s)</span>'
            % (AIRBNB[k], html.escape(text or HOUSES[k]['rating']), RATING_READ))


# Guest reviews: real Airbnb review text supplied by Edwin's team 9 Nov 2026, quoted word for word (typos kept). No Review/AggregateRating schema.
REVIEWS = {
    'prima': [('Mohd', 'August 2026', ['Clean , good for friends/family gathering , affordable .']),
              ('Syed', 'July 2026', ['Water dispenser doesnt really produce cold water. Overall its good']),
              ('Shazwani', 'July 2026', ['Easy check in, clean house, responsive host and great location!']),
              ('Yeoh Ting', 'July 2026', ['everything good except the check-in had been delayed abit'])],
    'landak': [('Xu', 'October 2026', ['After a long traffic jam at SG JB Customs, we finally checked in at night. The moment we entered the house, the kids got so excited!',
                                       'Love the arcade games and soccer table, while the rest enjoyed pool and darts. Everyone had so much fun that we ended up playing until late at night! The house was spacious and comfortable, perfect for gathering. Great location too, walking distance to KSL Mall, plenty of nearby eateries (Fu Ee food stalls) for meals and supper and foot/back massage outlets to relax after a long day...',
                                       'A wonderful staycation! Will Definitely come back again!']),
               ('Johnson', 'November 2026', ['Located close to KSL so that is very convenient, the house itself looks exactly like the photos posted, modern deco and the overall it is clean and cosy!']),
               ('JI', 'October 2026', ["Booked Daniel's listing for 2 nights.", 'Place was easy to locate and surroundings was peaceful and quiet.', 'Host was very responsive throughout the stay.']),
               ('Sulung', 'October 2026', ['Had a late check-in, this one turned out to be a real gem.', 'Easy check-in, excellent location 5-6 minutes’ brisk walk to KSL.', 'Plenty of food & massage nearby, plus comfortable bed and cozy environment.', 'Will stay again definitely.'])],
}


def _rev_items(k):
    return ''.join('<li class="rev"><blockquote><p>%s</p></blockquote><p class="rev-by">%s, %s, on <a href="%s" rel="nofollow noopener" target="_blank">Airbnb</a></p></li>'
                   % ('<br>'.join(html.escape(t, quote=False) for t in lines), html.escape(n), m, AIRBNB[k]) for n, m, lines in REVIEWS[k])


def reviews_html(k):
    return ('<section id="reviews" class="rv"><h2>What guests say</h2><p class="rev-sum">%s %s</p><ul class="revs">%s</ul></section>'
            % (ico('star', 18), rating_link(k), _rev_items(k)))


def reviews_compact(k):
    return ('<details class="acc2 revacc"><summary>What guests say on Airbnb (%d reviews) %s</summary><p class="rev-sum">%s</p><ul class="revs">%s</ul></details>'
            % (len(REVIEWS[k]), ico('down', 20, 'i acc-i'), rating_link(k), _rev_items(k)))


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
    'star': '<path d="m12 3 2.7 5.6 6.1.8-4.5 4.3 1.1 6.1L12 16.9 6.6 19.8l1.1-6.1L3.2 9.4l6.1-.8z"/>',
    'party': '<path d="M3 21 8 8l8 8zM14 3c0 2 1 3 3 3M19 9h2M17 3l1-1M12 6l1-2"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'x': '<path d="M6 6l12 12M18 6 6 18"/>',
    'down': '<path d="m6 9 6 6 6-6"/>',
    'left': '<path d="m15 5-7 7 7 7"/>',
    'right': '<path d="m9 5 7 7-7 7"/>',
}


def ico(name, size=22, cls='i'):
    return ('<svg class="%s" viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, size, size, ICONS[name]))


AMEN_ICON = [('wi-fi', 'wifi'), ('air con', 'snow'), ('kitchen', 'pot'), ('parking', 'parking'), ('smart tv', 'tv'), ('washer', 'washer'),
             ('karaoke', 'mic'), ('mahjong', 'tiles'), ('bbq', 'fire'), ('workspace', 'desk'), ('desk', 'desk'), ('playroom', 'slide'), ('pool table', 'cue'), ('board games', 'tiles'),
             ('games room', 'cue'), ('study', 'book'), ('family room', 'sofa'), ('rooftop', 'sun'), ('balcony', 'rail'), ('dressing', 'hanger'), ('netflix', 'tv'),
             ('dartboard', 'target'), ('darts', 'target'), ('foosball', 'foos'), ('arcade', 'tv'), ('ksl', 'walk'), ('karaoke', 'mic'), ('mahjong', 'tiles'), ('living room', 'sofa'), ('hair dryer', 'wind'), ('iron', 'iron'), ('check-in', 'key'), ('tv', 'tv'), ('washer', 'washer')]


def amen_icon(a):
    low = a.lower()
    for k, v in AMEN_ICON:
        if k in low:
            return v
    return 'check'


def pimg800(f, alt=None):
    """Album tile: the 800px file only (thumb/), lazy, async, real width/height. The 1600px file opens in the lightbox."""
    w, h = tdims(f)
    return '<img src="{R}thumb/%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">' % (f, e(_alt_for(f) if alt is None else alt), w, h)


def pimg(f, alt=None, cls='', eager=False, sizes='(min-width:1024px) 50vw, 100vw', thumb=True, lazy=True):
    """<img> for a local photo with real width/height, alt, srcset (800px version in thumb/ + full size in img/) and lazy loading."""
    w, h = dims(f)
    alt = _alt_for(f) if alt is None else alt
    srcset = ''
    if f not in TDIM:
        thumb = False
    if HAS_THUMB and thumb:
        srcset = ' srcset="{R}thumb/%s %dw, {R}img/%s %dw" sizes="%s"' % (f, tdims(f)[0], f, w, sizes)
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
    return {'@context': 'https://schema.org', '@type': 'Organization', '@id': BASE + '#org', 'name': NAME, 'url': BASE, 'telephone': '+6590062198',
            'slogan': TAGLINE, 'logo': BASE + 'icon-512.png',
            'contactPoint': {'@type': 'ContactPoint', 'telephone': '+6590062198', 'contactType': 'reservations', 'url': 'https://wa.me/6590062198'}}


def house_ld(h):
    k = h['key']
    url = BASE + 'stays/%s/' % h['slug']
    gal = [f for _g, fs in ALBUM[k] for f in fs][:12]                        # real photos only, never the AI hero
    if k == 'prima':
        am = [('Pool table (7ft)', True), ('Mahjong', True), ('Ground-floor bedroom', True), ('wifi', True), ('outdoorGrill', False), ('Parking spaces inside', 2), ('Parking spaces outside', 6), ('Air conditioning', True), ('Kitchen', True)]
        acc = {'numberOfBedrooms': 3, 'numberOfBathroomsTotal': 3, 'occupancy': {'@type': 'QuantitativeValue', 'maxValue': 12}}
    else:
        am = [('Pool table (8ft)', True), ('Foosball', True), ('Dart boards', 2), ('Mahjong', True), ('TV arcade', True), ('Board games', True), ('Children\'s playroom', True), ('Dedicated workstation', True), ('Water heaters', True),
              ('wifi', True), ('Parking spaces', 2), ('outdoorGrill', False), ('Air conditioning', True), ('Kitchen', True)]
        acc = {'numberOfBedrooms': 3, 'numberOfBathroomsTotal': 3, 'numberOfBeds': 5, 'occupancy': {'@type': 'QuantitativeValue', 'maxValue': 10}}
    acc.update({'@type': 'Accommodation', 'additionalType': 'EntirePlace',
                'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': n, 'value': v} for n, v in am]})
    ld = {'@context': 'https://schema.org', '@type': 'VacationRental', '@id': url + '#rental', 'identifier': 'jb-' + k, 'name': h['name'], 'additionalType': 'House',
          'url': url, 'sameAs': [AIRBNB[k]], 'description': h['card'], 'image': [abs_img(f) for f in gal], 'telephone': '+6590062198',
          'address': addr_ld(h), 'priceRange': '%s to %s per night, cleaning included' % (rm(PRICES[k][0]), rm(PRICES[k][2])),
          'makesOffer': {'@type': 'Offer', 'name': 'Whole house, per night (cleaning included)', 'priceCurrency': 'MYR', 'price': PRICES[k][0], 'url': url,
                         'priceSpecification': [{'@type': 'UnitPriceSpecification', 'name': t, 'price': n, 'priceCurrency': 'MYR', 'unitText': 'night'} for t, n in zip(TIER_NAMES, PRICES[k])]}, 'containsPlace': acc, 'petsAllowed': False, 'smokingAllowed': False,
          'brand': {'@id': BASE + '#org'}}
    if True:  # both houses (host, 9 Nov 2026)
        ld['checkinTime'] = '15:00:00+08:00'
        ld['checkoutTime'] = '11:00:00+08:00'
    return ld


# ---------------------------------------------------------------- shared shell (ONE header/footer for every page)
NAV = [('Stays', 'stays/'), ('Prices', 'prices/'), ('Getting there', 'getting-there/'), ('FAQ', 'faq/'), ('JB guide', 'articles/'), ('About', 'about/')]
WA_HELLO = wa_msg()


def brand_mark():
    return ('<svg class="mark" viewBox="0 0 32 32" width="32" height="32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0a1f38"/>'
            '<path d="M6 15.5 16 7l10 8.5h-2.6V25H8.6v-9.5z" fill="#f7f8f9"/><rect x="13.6" y="17.5" width="4.8" height="7.5" rx="1" fill="#e8a33d"/></svg>')


def header_html(k=None):
    nav = ''.join('<a href="{R}%s">%s</a>' % (p, n) for n, p in NAV)
    return ('<header class="hdr" id="top"><div class="wrap hdr-in"><a class="brand" href="{R}" aria-label="JB Airbnb home">%s<span>JB <b>Airbnb</b></span></a>'
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
            '<p class="wordmark" aria-hidden="true">JB <span>Airbnb</span></p>'
            '<div class="fsmall"><span>Prices in RM. Host Daniel on WhatsApp: %s.</span> <a href="https://pageonesingapore.com/" rel="noopener">Website by Page One Singapore</a></div></div></footer>'
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


UI_JS = r"""/* JB Airbnb UI: header, menu, reveal on scroll, carousels, lightbox. Content is fully visible and usable without JS. */
(function(){
var d=document,b=d.body,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var hdr=d.querySelector('.hdr'),tog=d.querySelector('.mtog');
function sc(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>24)}sc();window.addEventListener('scroll',sc,{passive:true});
function setMenu(o){hdr.classList.toggle('open',o);d.documentElement.classList.toggle('menu-open',o);tog.setAttribute('aria-expanded',o);tog.setAttribute('aria-label',o?'Close menu':'Open menu')}
d.querySelectorAll('.mfold').forEach(function(f){var bt=f.querySelector('.mf-h');var mq=window.matchMedia('(max-width:599px)');function sync(){bt.setAttribute('aria-expanded',(!mq.matches||f.classList.contains('mopen'))?'true':'false')}sync();if(mq.addEventListener)mq.addEventListener('change',sync);bt.addEventListener('click',function(){if(!mq.matches)return;f.classList.toggle('mopen');sync()})});
function opD(){var h=location.hash;if(h.length>1){var x=d.getElementById(h.slice(1));if(x&&x.tagName==='DETAILS')x.open=true;if(x&&x.classList.contains('mfold')){x.classList.add('mopen');var hb=x.querySelector('.mf-h');if(hb)hb.setAttribute('aria-expanded','true')}}}window.addEventListener('hashchange',opD);opD();
if(tog){tog.addEventListener('click',function(){setMenu(!hdr.classList.contains('open'))});d.querySelectorAll('#mainnav a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});window.addEventListener('resize',function(){if(window.innerWidth>=1024&&hdr.classList.contains('open'))setMenu(false)})}
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&hdr&&hdr.classList.contains('open'))setMenu(false)});
var els=[].slice.call(d.querySelectorAll('.rv'));
setTimeout(function(){els.forEach(function(x){x.classList.add('in')})},1500);
if('IntersectionObserver' in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(x){io.observe(x)})}else{els.forEach(function(x){x.classList.add('in')})}
/* carousels: auto-slide (keeps going while the page scrolls), pause only while held or dragged, restart 2 s after release */
d.querySelectorAll('[data-carousel]').forEach(function(c){
var t=c.querySelector('.track'),held=false,rt=null,drag=null,moved=false,cnt=c.querySelector('.cnt'),sl=t.querySelectorAll('.slide'),n=sl.length,chips=[].slice.call(c.querySelectorAll('.rchips button'));
function idx(){return Math.round(t.scrollLeft/Math.max(1,t.clientWidth))}
function upd(){var i=Math.min(idx(),n-1);if(cnt)cnt.textContent=(i+1)+' / '+n;dots.forEach(function(b,j){b.classList.toggle('on',j===i)});if(chips.length&&sl[i]){var r=sl[i].getAttribute('data-room');chips.forEach(function(b){var on=b.getAttribute('data-room')===r;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);if(on){var p=b.parentNode;p.scrollTo({left:b.offsetLeft-12,behavior:'auto'})}})}}
chips.forEach(function(b){b.addEventListener('click',function(){hold();var i=+b.getAttribute('data-i');t.scrollTo({left:i*t.clientWidth,behavior:rm?'auto':'smooth'});release()})});
function step(dir){var w=t.clientWidth,max=t.scrollWidth-w;if(max<=4)return;var x=t.scrollLeft+dir*w;if(x>max+4&&dir>0||t.scrollLeft>=max-4&&dir>0)x=0;else if(x<-4)x=max;t.scrollTo({left:x,behavior:rm?'auto':'smooth'})}
function hold(){held=true;clearTimeout(rt)}
function release(){clearTimeout(rt);rt=setTimeout(function(){held=false},2000)}
var dots=[],dw=c.querySelector('.dots');if(dw){for(var k=0;k<n;k++){var db=d.createElement('button');db.type='button';db.setAttribute('aria-label','Photo '+(k+1));(function(i){db.addEventListener('click',function(){hold();t.scrollTo({left:i*t.clientWidth,behavior:rm?'auto':'smooth'});release()})})(k);dw.appendChild(db);dots.push(db)}}
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
'<figure class="lb-fig"><div class="lb-st"><img class="lb-lo" alt="" aria-hidden="true" width="1600" height="1200"><img class="lb-hi" alt="" decoding="async" width="1600" height="1200"></div><figcaption></figcaption></figure>'+
'<button type="button" class="lb-p" aria-label="Previous photo"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m15 5-7 7 7 7"/></svg></button>'+
'<button type="button" class="lb-nx" aria-label="Next photo"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m9 5 7 7-7 7"/></svg></button>';
b.appendChild(lb);
var im=lb.querySelector('.lb-hi'),lo=lb.querySelector('.lb-lo'),cap=lb.querySelector('figcaption'),num=lb.querySelector('.lb-n'),cur=0,last=null;
im.addEventListener('load',function(){im.classList.add('ok')});
function show(i){cur=(i+items.length)%items.length;var a=items[cur],g=a.querySelector('img'),h=a.getAttribute('href');im.classList.remove('ok');lo.src=(g&&(g.currentSrc||g.src))||h.replace('/img/','/thumb/');im.removeAttribute('src');im.src=h;if(im.complete&&im.naturalWidth)im.classList.add('ok');im.alt=g?g.alt:'';cap.textContent=a.getAttribute('data-cap')||(g?g.alt:'');num.textContent=(cur+1)+' / '+items.length;
var p=new Image();p.src=items[(cur+1)%items.length].getAttribute('href')}
function open(i){last=d.activeElement;lb.hidden=false;b.classList.add('lb-on');show(i);lb.querySelector('.lb-x').focus()}
function close(){lb.hidden=true;b.classList.remove('lb-on');im.removeAttribute('src');if(last)last.focus()}
var all=items;all.forEach(function(a){a.addEventListener('click',function(e){if(e.defaultPrevented)return;e.preventDefault();var st=a.closest('[data-lb-set]');items=st?[].slice.call(st.querySelectorAll('[data-lb]')):all;open(items.indexOf(a))})});
d.querySelectorAll('[data-lb-open]').forEach(function(x){x.addEventListener('click',function(e){e.preventDefault();items=all;open(0)})});
/* Around the house: category chips (all categories show without JS) */
d.querySelectorAll('[data-ar]').forEach(function(w){w.classList.add('ar-js');var bs=[].slice.call(w.querySelectorAll('.ar-chips button')),cs=[].slice.call(w.querySelectorAll('.ar-cat'));
bs.forEach(function(x){x.addEventListener('click',function(){var c=x.getAttribute('data-c');bs.forEach(function(y){y.setAttribute('aria-selected',y===x)});cs.forEach(function(z){z.classList.toggle('on',z.getAttribute('data-c')===c)})})})});
/* enquiry form: builds the WhatsApp message (opens WhatsApp; never sends or stores anything) */
d.querySelectorAll('form.enq').forEach(function(f){f.classList.add('enq-on');var alt=f.parentNode.querySelector('.enq-alt');if(alt)alt.classList.add('enq-hide');
var ci=f.elements['in'],co=f.elements['out'],er=f.querySelector('.enq-err');try{var t=new Date();t.setMinutes(t.getMinutes()-t.getTimezoneOffset());ci.min=t.toISOString().slice(0,10)}catch(x){}
ci.addEventListener('change',function(){co.min=ci.value||'';er.hidden=true});
function fd(v){if(!v)return'not decided';var p=v.split('-'),m=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];return (+p[2])+' '+m[+p[1]-1]+' '+p[0]}
function nv(v){v=parseInt(v,10);return isNaN(v)||v<0?'not decided':String(v)}
f.addEventListener('submit',function(ev){ev.preventDefault();if(ci.value&&co.value&&co.value<=ci.value){er.hidden=false;co.focus();return}
var msg="Hi, I'm planning a JB stay from Singapore. [House: "+f.getAttribute('data-house')+"]. Check-in: "+fd(ci.value)+". Check-out: "+fd(co.value)+". Adults: "+nv(f.elements['ad'].value)+". Children: "+nv(f.elements['ch'].value)+". Please confirm availability, sleeping arrangement, final total in RM, payment options, deposit and cancellation terms. [Source: "+f.getAttribute("data-from")+"]";
window.open('https://wa.me/6590062198?text='+encodeURIComponent(msg),'_blank','noopener')})});
/* sticky bar: hide while the footer is visible or a form field is focused */
var stk=[].slice.call(d.querySelectorAll('.stick')),ft=d.querySelector('.ftr');
function stOff(o){stk.forEach(function(x){x.classList.toggle('st-off',o)})}
if(stk.length&&ft&&'IntersectionObserver' in window){new IntersectionObserver(function(es){stOff(es[0].isIntersecting)},{rootMargin:'0px 0px -40px 0px'}).observe(ft)}
d.addEventListener('focusin',function(e){if(e.target.matches&&e.target.matches('input,select,textarea'))b.classList.add('kb-on')});
d.addEventListener('focusout',function(e){if(e.target.matches&&e.target.matches('input,select,textarea'))b.classList.remove('kb-on')});
/* /stays: Prima | Landak switcher on phones (hash selects the house) */
var hsw=d.querySelector('.hsw');if(hsw){var H=d.documentElement;
function pick(k,scroll){H.setAttribute('data-house',k);hsw.querySelectorAll('a').forEach(function(a){var on=a.getAttribute('data-h')===k;a.classList.toggle('on',on);if(on)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
if(scroll&&matchMedia('(max-width:767px)').matches){var y=hsw.getBoundingClientRect().top+window.scrollY-parseFloat(getComputedStyle(H).getPropertyValue('--hh')||64);var cur=hsw.getBoundingClientRect().top;if(window.scrollY>y)window.scrollTo(0,y)}}
pick(H.getAttribute('data-house')||'prima',false);
hsw.addEventListener('click',function(e){var a=e.target.closest('a');if(!a||!matchMedia('(max-width:767px)').matches)return;e.preventDefault();var k=a.getAttribute('data-h');history.replaceState(null,'','#'+k);pick(k,true)});
window.addEventListener('hashchange',function(){var k=location.hash==='#landak'?'landak':location.hash==='#prima'?'prima':null;if(k)pick(k,false)})}
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
--font:"Geist","Geist Fallback",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@font-face{font-family:"Geist Fallback";src:local("Arial"),local("Arimo"),local("Liberation Sans"),local("Helvetica"),local("Roboto");size-adjust:104%}
@media(min-width:1024px){:root{--hh:76px}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-padding-top:calc(var(--hh) + 16px)}
@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{margin:0;background:var(--page);color:var(--ink);font:400 1.0625rem/1.65 var(--font);font-feature-settings:"ss01","ss02";-webkit-font-smoothing:antialiased}
img{max-width:100%;height:auto;display:block}
a{color:var(--ink);text-decoration-color:var(--amber);text-decoration-thickness:1.5px;text-underline-offset:3px;transition:color .2s}a:hover{color:var(--amber-deep)}
h1,h2,h3{line-height:1.12;font-weight:600;letter-spacing:-.025em;margin:0 0 .5em;color:inherit;text-wrap:balance}
h1{font-size:clamp(2rem,5.6vw,3.5rem)}h2{font-size:clamp(1.75rem,4.4vw,2.9rem)}h3{font-size:1.3rem;letter-spacing:-.015em}
p{margin:0 0 1em}p,li{text-wrap:pretty}
.wrap{max-width:1200px;margin:0 auto;padding:0 16px}@media(min-width:768px){.wrap{padding:0 clamp(24px,4vw,48px)}}
.sec{padding:36px 0}.sec-tight{padding:36px 0}@media(min-width:768px){.sec{padding:clamp(64px,10vw,120px) 0}.sec-tight{padding:clamp(48px,7vw,80px) 0}}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:.875rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--amber-deep);margin:0 0 14px}
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
.hdr.open{background:var(--page);-webkit-backdrop-filter:none;backdrop-filter:none}.js .nav{height:calc(100vh - var(--hh));height:calc(100dvh - var(--hh));overflow-y:auto;overscroll-behavior:contain;background:#f7f8f9}html.menu-open,html.menu-open body{overflow:hidden}.menu-open .stick{display:none}
html:not(.js) .nav{display:flex;position:absolute;top:var(--hh);left:0;right:0;overflow-x:auto;gap:4px;padding:6px 16px;background:var(--page);border-bottom:1px solid var(--line)}html:not(.js) .mtog{display:none}}
@media(min-width:1024px){.nav{display:flex;gap:2px;margin-right:auto}.brand{margin-right:28px}.mtog{display:none}}
.js .home .hdr:not(.scrolled):not(.open){background:transparent;border-color:transparent;color:#fff;-webkit-backdrop-filter:none;backdrop-filter:none}
.js .home .hdr:not(.scrolled):not(.open) .nav a:hover{background:rgba(255,255,255,.12)}
.js .home .hdr:not(.scrolled):not(.open) .mark rect:first-child{fill:rgba(255,255,255,.14)}
main{display:block;position:relative;z-index:1;background:var(--page)}
.inner main{padding-top:var(--hh)}
/* home hero */
.hero{position:relative;min-height:100vh;min-height:100svh;display:flex;align-items:flex-end;color:#fff;background:var(--panel-deep);overflow:hidden;isolation:isolate}
.hero-bg{position:absolute;inset:0;z-index:-2;overflow:hidden}.hero-bg picture,.hero-bg img{display:block;width:100%;height:100%}.hero-bg img{object-fit:cover;object-position:58% 50%}
@media(prefers-reduced-motion:no-preference){.hero-bg img{animation:kb 22s var(--ease) both}@keyframes kb{from{transform:scale(1.14)}to{transform:scale(1.02)}}}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(10,31,56,.42) 0,rgba(10,31,56,0) 24%,rgba(10,31,56,0) 50%,rgba(10,31,56,.62) 78%,rgba(10,31,56,.86) 100%)}.hero h1,.hero .sub,.hero .facts{text-shadow:0 1px 2px rgba(0,0,0,.35)}.hero .kick{text-shadow:0 1px 3px rgba(0,0,0,.65)}
@media(min-width:900px){.hero::after{background:linear-gradient(180deg,rgba(10,31,56,.4) 0,rgba(10,31,56,0) 20%),linear-gradient(90deg,rgba(10,31,56,.72) 0,rgba(10,31,56,.38) 34%,rgba(10,31,56,0) 62%),linear-gradient(0deg,rgba(10,31,56,.55) 0,rgba(10,31,56,0) 34%)}}
.hero-in{width:100%;padding-top:calc(var(--hh) + 48px);padding-bottom:28px}
.hero h1{margin:0 0 18px}
.hero .kick{display:block;font-size:.875rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);margin-bottom:18px;max-width:none;line-height:1.5}
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
.badge{position:absolute;left:14px;top:14px;background:rgba(255,255,255,.92);color:var(--ink);font-size:.875rem;font-weight:600;padding:6px 12px;border-radius:999px;backdrop-filter:blur(6px)}
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
.tag{font-size:.875rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-deep)}
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
.stats small{font-size:.875rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-muted)}.stats b{font-size:1.0625rem;font-weight:600;line-height:1.3}
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
.has-stick{padding-bottom:92px}@media(min-width:1024px){.stick{display:none}.has-stick{padding-bottom:0}}
/* /stays page */
.scards{display:grid;grid-template-columns:minmax(0,1fr);gap:24px;align-items:stretch}.scards>*,.hpane,.scard,.scar,.scb,.album,.ag{min-width:0;max-width:100%;box-sizing:border-box}.scard{width:100%}.scar img{max-width:100%}@media(min-width:1024px){.scards{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px}.scards .scard{grid-row:1}.scards .album{grid-column:1/-1}}
.album{padding:4px 0 12px}.album h3{font-size:1.375rem;margin:0 0 14px}.album h3 span,.ag h4 span{color:var(--ink-soft);font-weight:500;font-size:1rem}
.ag{margin:0 0 18px}.ag h4{font-size:1.0625rem;margin:0 0 8px}
.agrid{display:grid;grid-template-columns:1fr 1fr;gap:6px}@media(min-width:700px){.agrid{grid-template-columns:repeat(3,1fr)}}@media(min-width:1024px){.agrid{grid-template-columns:repeat(4,1fr);gap:8px}}
.agrid a{display:block;aspect-ratio:4/3;overflow:hidden;border-radius:8px;background:var(--sky)}.agrid img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s var(--ease)}.agrid a:hover img{transform:scale(1.04)}
.cmp-cta{display:grid;gap:10px;margin-top:12px}@media(min-width:600px){.cmp-cta{grid-template-columns:auto auto;justify-content:start}}.cmp-cta .btn{justify-content:center}
.scard{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);overflow:hidden;box-shadow:var(--sh)}
.scar{position:relative;background:var(--sky)}.scar .track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}.scar .track::-webkit-scrollbar{display:none}
.scar .slide{flex:0 0 100%;min-width:0;aspect-ratio:3/2;scroll-snap-align:center;overflow:hidden}.scar .slide img{width:100%;height:100%;object-fit:cover;display:block}
.scar .cbtn{display:flex}.scar .prev{left:12px}.scar .next{right:12px}
.scar .dots{display:none;position:absolute;left:0;right:0;bottom:12px;justify-content:center;gap:6px}.scar .dots{gap:0}.scar .dots button{position:relative;width:44px;height:44px;border:0;background:none;padding:0;cursor:pointer}.scar .dots button::before{content:"";position:absolute;left:17px;top:17px;width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.6);box-shadow:0 1px 3px rgba(0,0,0,.3)}.scar .dots button.on::before{background:#fff;transform:scale(1.3)}
@media(max-width:767px){.scar .cbtn{display:none}}@media(min-width:768px){.scar .cbtn{display:flex}.scar .cnt{display:none}.scar .dots{display:flex}}
.scar .seeall{position:absolute;right:12px;bottom:12px;display:inline-flex;align-items:center;gap:6px;min-height:44px;padding:0 14px;border-radius:999px;background:rgba(255,255,255,.94);color:var(--ink);font-weight:600;font-size:1rem;text-decoration:none;box-shadow:0 4px 14px rgba(10,31,56,.2)}
@media(min-width:768px){.scar .seeall{bottom:52px}.scar .dots{bottom:2px}}
.scb{display:flex;flex-direction:column;gap:14px;padding:20px 20px 24px;flex:1}@media(min-width:1024px){.scb{padding:26px 28px 30px}}
.scb h2{margin:0;font-size:clamp(1.5rem,2.4vw,1.9rem)}.scb .area{margin:0;display:flex;align-items:center;gap:6px;color:var(--ink-soft);font-size:1rem}
.kf{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0;padding:0;list-style:none;font-weight:600}.kf li{display:flex;align-items:center;gap:7px;min-height:28px}
.ami{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0;padding:0;list-style:none}@media(min-width:700px){.ami{grid-template-columns:repeat(5,1fr)}}
.ami li{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;text-align:center;padding:12px 6px;border:1px solid var(--line);border-radius:var(--r);background:var(--page);font-size:1rem;font-weight:500;line-height:1.25}
.bestfor{margin:0;font-size:1.0625rem;line-height:1.5}.scb .rating{margin:0;display:flex;align-items:center;gap:6px;color:var(--ink-soft);font-size:1rem}.scb .rating .i{color:var(--amber)}
.scta{margin-top:auto;display:grid;gap:10px;padding-top:6px}@media(min-width:480px){.scta{grid-template-columns:1fr auto}}.scta .btn{width:100%;justify-content:center}
.cmp-sec{margin-top:clamp(44px,7vw,80px)}.cmp-sec+#faq{margin-top:clamp(48px,7vw,80px)}.cmp{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;margin:0 0 20px}.cmp table{table-layout:fixed;width:100%;min-width:0;border-collapse:collapse}
.cmp th,.cmp td{padding:12px 14px;vertical-align:top;border-bottom:1px solid var(--line);overflow-wrap:anywhere}.cmp tbody th{width:28%;font-weight:600;background:var(--page)}.cmp thead th{background:var(--sky);font-size:1rem;text-transform:uppercase;letter-spacing:.06em;color:var(--ink-soft)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media(max-width:599px){.cmp thead th:first-child{display:none}.cmp tr{display:grid;grid-template-columns:1fr 1fr}.cmp tbody th{grid-column:1/-1;width:auto;padding:10px 14px 4px;border-bottom:0;font-size:1rem;text-transform:uppercase;letter-spacing:.05em;color:var(--ink-soft);background:transparent}.cmp td{padding:4px 14px 12px}.cmp td:first-of-type{border-right:1px solid var(--line)}.cmp thead th{text-transform:none;letter-spacing:0;font-size:1rem;font-weight:700;color:var(--ink)}}
.stays .band{margin-top:clamp(44px,7vw,80px)}
.lb-on .stick{display:none}
.after-gal,.after-faq{margin:20px 0 0}.after-faq .btn,.after-gal .btn{width:100%}@media(min-width:600px){.after-faq .btn,.after-gal .btn{width:auto}}
.hcard .card-cta{position:relative;z-index:2;width:100%;min-height:48px;margin-top:6px}.btn-pri{background:var(--amber);color:var(--ink);box-shadow:0 8px 24px -8px rgba(232,163,61,.7)}.btn-pri:hover{background:#f0b252;color:var(--ink)}.nf .btn{margin-top:8px}
/* lightbox */
.lb{position:fixed;inset:0;z-index:100;background:#061221;display:flex;align-items:center;justify-content:center;color:#fff}
.lb[hidden]{display:none}.lb-on{overflow:hidden}
.lb-top{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;align-items:center;padding:10px 12px 10px 20px;z-index:2}
.lb-n{font-size:.9375rem;color:rgba(255,255,255,.8)}
.lb button{width:48px;height:48px;border-radius:50%;border:0;background:rgba(255,255,255,.1);color:#fff;display:grid;place-items:center;cursor:pointer;transition:background .2s}.lb button:hover{background:rgba(255,255,255,.22)}
.lb-p,.lb-nx{position:absolute;top:50%;transform:translateY(-50%);z-index:2}.lb-p{left:12px}.lb-nx{right:12px}
.lb-fig{margin:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:64px 0 24px}
.lb-st{position:relative;width:min(100%,1400px);flex:1;min-height:0;overflow:hidden}.lb-st img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}
.lb-lo{filter:blur(12px)}.lb-hi{opacity:0;transition:opacity .25s}.lb-hi.ok{opacity:1}
.lb-fig figcaption{padding:14px 20px 0;text-align:center;color:rgba(255,255,255,.85);font-size:1rem}
@media(min-width:768px){.lb-fig{padding:72px 80px 28px}}
@media(max-width:767px){.lb-p,.lb-nx{top:auto;bottom:16px;transform:none}.lb-fig{padding-bottom:80px}}
/* footer (dark curtain) */
.ftr{background:var(--panel-deep);color:rgba(255,255,255,.78);padding:clamp(56px,8vw,96px) 0 28px;position:relative;z-index:0}
.ftr a{color:#fff;text-decoration:none}.ftr a:hover{color:var(--amber)}.ftr .btn-wa{color:var(--ink)}.ftr .btn-wa:hover{color:var(--ink)}
.ftr-top{display:grid;gap:40px}@media(min-width:900px){.ftr-top{grid-template-columns:1.3fr 1.2fr .8fr;gap:56px}}
.ftr-tag{font-size:clamp(1.6rem,3vw,2.2rem);line-height:1.12;letter-spacing:-.03em;color:#fff;font-weight:600;margin:0 0 12px;max-width:16ch}
.ftr-sub{margin:0 0 24px;max-width:40ch}
.fh{font-size:.875rem;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);font-weight:600;margin:0 0 14px}
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
.facts{margin:18px 0 0;padding-top:12px;display:flex;flex-direction:column;gap:4px 22px}.facts li:nth-child(n+3){display:none}
.hero .btn{width:100%}
.pts li{padding:16px 18px;display:grid;grid-template-columns:30px 1fr;column-gap:14px;row-gap:2px}.pts .i{grid-row:span 2}
.split2{gap:28px}.steps{gap:16px;margin-bottom:16px}.steps li{grid-template-columns:40px 1fr;gap:12px}.steps li::before{width:40px;height:40px}
.after-gal{margin-top:16px}
.band p{margin-bottom:20px}
.faqgrid{gap:20px}.faq summary{padding:12px 0}.faq-a p{margin-bottom:14px}
.ftr{padding:40px 0 20px}.ftr-top{gap:28px}.wordmark{margin-top:28px}
.adds a,.fsmall a{display:inline-flex;align-items:center;min-height:44px}.adds{gap:6px}.fsmall{margin-top:20px}
.crumbs a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:0 4px}.crumbs{margin-bottom:6px;gap:0}
.note a:not(.btn),.prose p a:not(.btn),.prose li a:not(.btn),.muted a:not(.btn),.src a:not(.btn),.hmain p a:not(.btn){display:inline-block;padding:11px 10px;margin:-11px -10px}
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
/* /stays phones: one house at a time (Prima | Landak), compact card, swipe strips per room */
.sf{display:none}@media(max-width:767px){.sf{display:inline}}.hsw{display:none}.hpane{display:contents}.stick.st-h{display:none}
.acc>summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px}.acc>summary::-webkit-details-marker{display:none}.acc>summary h2{margin:0 0 16px}.acc-i{display:none}
@media(min-width:768px){.acc>summary{pointer-events:none}}
@media(max-width:767px){
.js .hsw{display:flex;position:sticky;top:var(--hh);z-index:30;margin:0 -16px 14px;padding:8px 16px;background:var(--page);border-bottom:1px solid var(--line)}
.hsw a{flex:1;display:grid;place-items:center;min-height:44px;font-weight:600;font-size:1rem;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line-strong)}
.hsw a:first-child{border-radius:999px 0 0 999px;border-right:0}.hsw a:last-child{border-radius:0 999px 999px 0}.hsw a.on{background:var(--ink);border-color:var(--ink);color:#fff}
.js .hpane{display:block}.js .hpane .scard{scroll-margin-top:calc(var(--hh) + 64px)}
html.js[data-house=prima] .hpane[data-house=landak],html.js[data-house=landak] .hpane[data-house=prima]{display:none}
.js .st-any{display:none}html.js[data-house=prima] .stick.st-h[data-house=prima],html.js[data-house=landak] .stick.st-h[data-house=landak]{display:flex}
.scb{gap:10px;padding:16px 16px 18px}
.kf{flex-wrap:nowrap;gap:0;font-size:1rem;white-space:nowrap}.kf li{min-height:24px;gap:0;flex:none}.kf .i,.kf .nm{display:none}.kf .lf{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.kf li+li::before{content:"\00b7";padding:0 6px;color:var(--ink-muted)}
.ami{grid-template-columns:1fr 1fr;gap:6px 12px}.ami li{flex-direction:row;justify-content:flex-start;text-align:left;padding:4px 0;border:0;background:none;gap:8px;min-height:32px}.ami li .i{flex:none;color:var(--amber-deep)}
.scta{padding-top:2px}
.album{padding:16px 0 4px}.album h3{font-size:1.25rem;margin:0 0 10px}.ag{margin:0 0 14px}.ag h4{margin:0 0 6px}
.agrid{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;scrollbar-width:none;margin:0 -16px;padding:0 16px;scroll-padding:0 16px}.agrid::-webkit-scrollbar{display:none}
.agrid a{flex:0 0 44%;scroll-snap-align:start}.js .stays-band,.js .hpane .after-gal{display:none}
.cmp-sec{margin-top:36px}.acc>summary{cursor:pointer;min-height:48px;padding:12px 16px;border:1px solid var(--line-strong);border-radius:var(--r);background:var(--surface)}.acc>summary h2{margin:0;font-size:1.25rem}.acc-i{display:block;flex:none;transition:transform .2s}.acc[open]>summary{margin-bottom:14px}.acc[open] .acc-i{transform:rotate(180deg)}
}
@media(max-width:374px){.kf{font-size:.9375rem}.kf li+li::before{padding:0 3px}}

/* every table: stacked label/value cards under 600px, never sideways scroll (Edwin 9 Nov 2026) */
@media(max-width:599px){.tw{overflow-x:visible}.tw table{min-width:0!important;width:100%;border:0}.tw thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.tw tr{display:block;border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:0 0 12px;background:var(--surface)}
.tw th[scope=row]{display:block;padding:4px 0 8px;border:0;font-size:1.0625rem;background:none}
.tw td{display:grid;grid-template-columns:40% 1fr;gap:10px;padding:6px 0;border:0;border-top:1px solid var(--line);overflow-wrap:anywhere}.tw td>*{grid-column:2}
.tw td::before{content:attr(data-label);font-weight:600;color:var(--ink-soft)}.tw{border:0;border-radius:0}
.cmp thead{display:none}.cmp td::before{content:attr(data-label);display:block;font-size:.875rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-muted);margin-bottom:2px}}
.tw th a{display:inline-flex;align-items:center;min-height:44px}
.tw small{font-size:.875rem}.fxn{margin:14px 0 0;font-size:1rem;color:var(--ink-soft)}.fxn summary{cursor:pointer;min-height:44px;display:flex;align-items:center;font-weight:600;color:var(--ink)}.fxn p{margin:6px 0 0}
.stick{transition:transform .25s var(--ease),opacity .25s}.stick.st-off,.kb-on .stick{transform:translateY(110%);opacity:0;pointer-events:none}

/* home: Singapore round (9 Nov 2026) */
.hero .kick{font-size:.875rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);margin:0 0 14px}
.hcap{position:absolute;right:12px;bottom:8px;margin:0;font-size:.875rem;color:rgba(255,255,255,.78);z-index:2;text-shadow:0 1px 2px rgba(0,0,0,.5)}
@media(max-width:767px){.hcap{left:16px;right:16px;bottom:8px}.hero-in{padding-bottom:68px}}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.chooser{margin:28px 0 0;padding:20px;border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface)}.chooser h3{margin:0 0 12px;font-size:1.25rem}
.ch-opts{display:flex;flex-wrap:wrap;gap:8px}.ch-opts label{display:inline-flex;align-items:center;min-height:44px;padding:0 16px;border:1.5px solid var(--line-strong);border-radius:999px;font-weight:600;cursor:pointer}
#gs1:checked~.ch-opts label[for=gs1],#gs2:checked~.ch-opts label[for=gs2],#gs3:checked~.ch-opts label[for=gs3]{background:var(--ink);border-color:var(--ink);color:#fff}
#gs1:focus-visible~.ch-opts label[for=gs1],#gs2:focus-visible~.ch-opts label[for=gs2],#gs3:focus-visible~.ch-opts label[for=gs3]{outline:3px solid var(--amber);outline-offset:2px}
.ch-res{margin-top:12px}.ch-res p{margin:0 0 8px}.ch-res .r1,.ch-res .r2,.ch-res .r3{display:none}.ch-btns{display:flex;flex-wrap:wrap;gap:8px}
#gs1:checked~.ch-res .r1,#gs2:checked~.ch-res .r2,#gs3:checked~.ch-res .r3{display:block}#gs1:checked~.ch-res .r0,#gs2:checked~.ch-res .r0,#gs3:checked~.ch-res .r0{display:none}
.trust-sec{background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.trust-sec h2{margin:0 0 20px}
.trust{list-style:none;margin:0;padding:0;display:grid;gap:16px}@media(min-width:768px){.trust{grid-template-columns:1fr 1fr}}@media(min-width:1100px){.trust{grid-template-columns:repeat(4,1fr)}}
.trust li{display:grid;grid-template-columns:28px 1fr;gap:12px}.trust .i{color:var(--amber-deep)}.trust b{display:block}.trust span{color:var(--ink-soft)}
.plans{list-style:none;margin:0 0 12px;padding:0;display:grid;gap:16px}@media(min-width:768px){.plans{grid-template-columns:1fr 1fr}}
.plans li{padding:20px;border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);display:flex;flex-direction:column;gap:8px}.plans b{font-size:1.125rem}.plans span{color:var(--ink-soft)}
.faq-h{margin:0 0 12px}
@media(max-width:767px){.trust li{grid-template-columns:24px 1fr}.chooser{padding:16px}}

/* Singapore round: /stays + house pages */
.hsw a{flex-direction:column;gap:0;line-height:1.15;padding:4px 0}.hsw a b{font-size:1rem}.hsw a small{font-size:.875rem;font-weight:500;opacity:.85}.hsw a{display:flex;align-items:center;justify-content:center}
.sgd{margin:0;font-size:1rem;color:var(--ink-soft)}.tiers{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;width:100%}.tiers li{min-width:0;display:flex;flex-direction:column;gap:2px;margin:0;padding:8px;border:1px solid var(--line);border-radius:10px;background:#fff}.tiers span{flex:1;font-size:.875rem;color:var(--ink-muted);line-height:1.25}.tiers b{font-size:1.125rem;letter-spacing:-.02em;color:var(--ink);white-space:nowrap;line-height:1.2}.tiers small{font-size:.875rem;color:var(--ink-soft);white-space:nowrap}.cinc{margin:8px 0 0;font-size:.9375rem;color:var(--ink-soft)}.side-h{margin:0 0 8px;font-weight:600}.side .tiers{margin-bottom:8px}.sgd b{color:var(--ink)}.snote{margin:0;font-size:1rem;color:var(--ink-soft)}
.jl{display:flex;gap:4px 16px;flex-wrap:wrap;font-size:1rem}.jl a{display:inline-flex;align-items:center;min-height:44px;font-weight:600;color:var(--ink)}
.near3{margin:8px 0 18px}.near3 h3{font-size:1.25rem;margin:0 0 10px}
.ar-chips{display:none;gap:8px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin:0 0 12px;padding:2px}.ar-chips::-webkit-scrollbar{display:none}
.ar-js .ar-chips{display:flex}.ar-chips button{flex:none;min-height:44px;padding:0 16px;border-radius:999px;border:1.5px solid var(--line-strong);background:var(--surface);font:600 1rem var(--font);color:var(--ink);cursor:pointer}
.ar-chips button span{color:var(--ink-muted);font-weight:500;margin-left:4px}.ar-chips button[aria-selected=true]{background:var(--ink);border-color:var(--ink);color:#fff}.ar-chips button[aria-selected=true] span{color:rgba(255,255,255,.75)}
.ar-cat h3{font-size:1.125rem;margin:16px 0 8px}.ar-js .ar-cat{display:none}.ar-js .ar-cat.on{display:block}.ar-js .ar-cat h3{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.ar-strip{position:relative;list-style:none;margin:0;padding:2px 2px 6px;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain}.ar-strip::-webkit-scrollbar{display:none}
.arc{position:relative;flex:0 0 min(78%,300px);scroll-snap-align:start;display:flex;flex-direction:column;gap:6px;padding:14px 16px 10px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface)}
.arc b{font-size:1.0625rem;line-height:1.3}.arc .why{color:var(--ink-soft);font-size:1rem;line-height:1.45;flex:1}.arc .t{display:flex;align-items:center;gap:6px;font-size:1rem;font-weight:600}.arc .t .i{color:var(--amber-deep)}
.arc .map{display:inline-flex;align-items:center;gap:6px;min-height:44px;font-weight:600;color:var(--ink)}
.acc2{border-top:1px solid var(--line);margin-top:8px}.acc2:last-child{border-bottom:1px solid var(--line)}.acc2>summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:52px;font-weight:600;font-size:1.0625rem;cursor:pointer}.acc2>summary::-webkit-details-marker{display:none}
.rulesacc>summary h2{margin:0;font-size:inherit}.rulesacc>summary{font-size:1.375rem!important;min-height:56px}.rulesacc[open]>summary{margin-bottom:12px}.hub-h{margin:40px 0 16px}.hub .tips{padding-left:22px}.rlink{color:inherit;text-decoration:underline;text-decoration-color:var(--amber);text-underline-offset:3px}.rdate{color:var(--ink-soft)}.mf-h{all:unset;display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%;font:inherit;color:inherit}.mf-i{display:none}@media(max-width:599px){.js .mf-h{cursor:pointer;min-height:48px}.js .mf-i{display:block;transition:transform .2s}.js .mfold.mopen .mf-i{transform:rotate(180deg)}.js .mfold:not(.mopen)>.mf-b{display:none}.js .mfold:not(.mopen) h2{margin-bottom:0}.js .mf-h:focus-visible{outline:2px solid var(--amber);outline-offset:2px}}.revs{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:12px}.rev{padding:14px 16px;border:1px solid var(--line);border-radius:var(--r);background:var(--surface)}.rev blockquote{margin:0}.rev blockquote p{margin:0;font-size:1rem;line-height:1.55;color:var(--ink)}.rev-by{margin:8px 0 0;font-size:.9375rem;color:var(--ink-soft);font-weight:600}.rev-by a{color:inherit;text-decoration:underline;text-decoration-color:var(--amber);display:inline-block;padding:10px 4px;margin:-10px -4px}.rev-sum{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:0}.rev-sum .i{color:var(--amber)}.revacc{margin-top:8px}@media(min-width:900px){#reviews .revs{grid-template-columns:1fr 1fr}}.acc2 .acc-i{display:block;transition:transform .2s}.acc2[open] .acc-i{transform:rotate(180deg)}.plist,.tips{margin:0 0 10px;padding-left:20px;display:grid;gap:10px}
.answer+.htag{margin-top:18px}.intro .answer{margin:0}
.sgd-s{margin:-6px 0 12px;color:var(--ink-soft)}
.enq{display:none;margin:4px 0 12px;padding:14px;border:1px solid var(--line);border-radius:var(--r);background:var(--page)}.enq.enq-on{display:block}.enq-hide{display:none!important}
.enq-h{margin:0 0 10px;font-weight:700}.enq-g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.enq label{min-width:0}.enq input{box-sizing:border-box;max-width:100%;font-size:16px!important}.enq input[type=date]{-webkit-appearance:none;appearance:none;display:block;line-height:1.3;text-align:left}.enq input[type=date]::-webkit-date-and-time-value{text-align:left}@media(max-width:599px){.enq-g{grid-template-columns:minmax(0,1fr)}.enq input{min-height:48px}}.enq label{display:flex;flex-direction:column;gap:4px;font-size:.9375rem;font-weight:600;color:var(--ink-soft)}
.enq input{min-height:44px;font:400 1rem var(--font);padding:8px 10px;border:1px solid var(--line-strong);border-radius:10px;background:#fff;color:var(--ink);width:100%;min-width:0}
.enq .btn{width:100%;margin-top:12px}.enq-err{color:#b42318;margin:8px 0 0;font-weight:600}.enq-n{margin:8px 0 0;font-size:.875rem;color:var(--ink-muted)}
/* background touch-up (Edwin 9 Nov 2026: "just plain white background need to touch up only"): warm tinted page and alternating section tints with a faint pattern instead of flat white/grey. Design, text colours and layout unchanged. */
:root{--page:#f8f5ef;--tint-b:#f4ead8;
--grid-l:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48'%3E%3Cpath d='M48 0H0V48' fill='none' stroke='%230a1f38' stroke-opacity='.04'/%3E%3Crect x='21' y='21' width='6' height='6' transform='rotate(45 24 24)' fill='%23a86d15' fill-opacity='.09'/%3E%3C/svg%3E")}
body,main{background-color:var(--page)}
.home #houses,.home .gsec,.ptop,.htop,.body{background-image:var(--grid-l)}
.home .trust-sec{background-color:var(--tint-b);background-image:var(--grid-l)}
.home .trust-sec+.sec+.sec{background:#fffdf9!important;border-top-color:var(--line)}
.trust-sec+.sec{background-color:var(--page)}
.stick{background:rgba(255,253,249,.96)}
"""


FONT_LINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..800&display=swap">')
HEAD_JS = "<script>document.documentElement.className+=' js';setTimeout(function(){document.documentElement.classList.add('rv-all')},1500)</script>"


def jl(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


PAGES = {}
PENDING = {}


import hashlib as _hl
ASSET_V = _hl.sha256((CSS + UI_JS + CTA_JS).encode()).hexdigest()[:8]  # cache-buster: changes whenever css/js change


def page(path, title, desc, h1, body, crumbs=None, ld=None, lede='', og=None, photo=None, stick=None, article=False, custom_top=False):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, ld=ld or [], lede=lede, og=og, photo=photo, stick=stick,
                       article=article, custom_top=custom_top)


def stick_bar(k):
    if k == 'stays':                                     # /stays: phones show the bar for the selected house
        return ''.join(stick_bar(x).replace('<div class="stick">', '<div class="stick%s">' % c, 1)
                       for x, c in (('any', ' st-any'), ('prima', ' st-h" data-house="prima'), ('landak', ' st-h" data-house="landak')))
    if k not in HOUSES:
        return ('<div class="stick"><p class="price"><b>From RM 450</b> <small>/ night, cleaning included</small></p>%s</div>'
                % (wa_btn('Check dates', wa_msg(), 'sticky-all')))
    h = HOUSES[k]
    return ('<div class="stick"><p class="price"><b>%s</b> <small>weekday &middot; %s weekend &middot; %s public holiday</small></p>%s</div>'
            % (rm(PRICES[k][0]), rm(PRICES[k][1]), rm(PRICES[k][2]), wa_btn('Check dates', h['msg'], 'sticky-' + k)))


def render(path, p):
    pre = '../' * path.count('/')
    url = BASE + path
    og = p['og'] or OG_DEFAULT
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
            '<meta property="og:type" content="{ogt}"><meta property="og:site_name" content="JB Airbnb"><meta property="og:title" content="{title}">'
            '<meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ogi}"><meta property="og:image:width" content="{ogw}"><meta property="og:image:height" content="{ogh}"><meta property="og:image:alt" content="{oga}">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:image" content="{ogi}">'
            '{headjs}{fonts}<link rel="stylesheet" href="{pre}jb.css?v={av}">{lds}</head><body class="{bc}">'
            '<a class="skip" href="#main">Skip to content</a>{hdr}<main id="main">{top}{content}</main>{ftr}{stick}'
            '<script src="{pre}jb.js?v={av}" defer></script><script src="{pre}cta.js?v={av}" defer></script></body></html>').format(av=ASSET_V, 
        title=e(p['title']), desc=e(p['desc']), url=url, pre=pre, ogt='article' if p['article'] else 'website', ogi=e(abs_img(og)),
        ogw=w, ogh=h, oga=e(_alt_for(og)), headjs=HEAD_JS, fonts=FONT_LINKS, lds=''.join(jl(x) for x in lds), bc=bc, hdr=header_html(p['stick']), top=top,
        content=p['body'], ftr=footer_html(), stick=stick)
    return body.replace('{R}', pre)


# ---- Around the house: places ONLY from Edwin's verified file jb-around-the-house.md (9 Nov 2026). Ratings left out; Billion Onsen kept with its 'confirm it's open' note and left out of the plans.
AROUND = {
"prima": {
"cats": [
[
"Eat",
[
[
"Pendas Floating Restaurant",
"Seafood on a kelong built over the Straits; you pick by weight, and the cooking style is free",
"about 10-15 min drive",
"https://www.google.com/maps/search/?api=1&query=Pendas+Floating+Restaurant+Gelang+Patah"
],
[
"Chua Kee Seafood Restaurant",
"Over 30 years in Gelang Patah, known for black pepper crab",
"about 5-10 min drive",
"https://www.google.com/maps/search/?api=1&query=Chua+Kee+Seafood+Restaurant+Gelang+Patah"
],
[
"Restoran Tian Lai",
"Kam heong crab and steamed ikan patin; closed Mondays, long queues at weekends",
"about 5-10 min drive",
"https://www.google.com/maps/search/?api=1&query=Restoran+Tian+Lai+Gelang+Patah"
],
[
"Wee Hoi Kopitiam",
"Old-school breakfast with handmade snow bao; opens 6am, closed Thursdays, sells out early",
"about 5-10 min drive",
"https://www.google.com/maps/search/?api=1&query=Wee+Hoi+Kopitiam+Gelang+Patah"
],
[
"Reef Seafood Restaurant",
"Family seafood dinners: kam heong crab, steamed fish",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=Reef+Seafood+Restaurant+Sunway+Puteri+Hill"
],
[
"Puteri Harbour restaurants (e.g. Les Bouchons)",
"Dinner by the marina with sunset views",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=Les+Bouchons+Puteri+Harbour"
]
]
],
[
"Shop",
[
[
"Sunway Big Box",
"GSC cinema, NSK hypermarket, Watsons and Guardian; open daily 10am-10pm",
"about 15 min drive",
"https://www.google.com/maps/search/?api=1&query=Sunway+Big+Box+Iskandar+Puteri"
],
[
"Mall of Medini",
"Next to LEGOLAND, with a BIG supermarket and Starbucks",
"about 15 min drive",
"https://www.google.com/maps/search/?api=1&query=Mall+of+Medini"
],
[
"Lotus's Bukit Indah",
"Big hypermarket for drinks and groceries",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=Lotus's+Bukit+Indah"
],
[
"AEON Mall Bukit Indah",
"Supermarket, department store, TGV cinema and chain restaurants",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=AEON+Mall+Bukit+Indah"
]
]
],
[
"Do and kids",
[
[
"LEGOLAND Malaysia",
"Theme park, water park and SEA LIFE aquarium; Miniland even has a LEGO Singapore",
"about 15 min drive",
"https://www.google.com/maps/search/?api=1&query=LEGOLAND+Malaysia+Resort"
],
[
"Puteri Harbour waterfront",
"Free marina promenade, kids' playground, sunset walks",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=Puteri+Harbour+Iskandar+Puteri"
],
[
"X Park Sunway Iskandar",
"Go-karts, ATV, archery, kayaking, paintball; open afternoons until midnight",
"about 15 min drive",
"https://www.google.com/maps/search/?api=1&query=X+Park+Sunway+Iskandar"
],
[
"Sireh Park",
"Trails, ATV rides, kayaking and an educational farm; basic entry is free",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=Sireh+Park+Iskandar+Puteri"
]
]
],
[
"Practical",
[
[
"Second Link (Tuas) / Sultan Abu Bakar CIQ",
"Usually quieter than the Causeway; Singapore cars pay S$2.10 Tuas toll each way",
"about 10 min drive",
"https://www.google.com/maps/search/?api=1&query=Sultan+Abu+Bakar+CIQ+Gelang+Patah"
],
[
"Pharmacies at Sunway Big Box",
"Watsons and Guardian",
"about 15 min drive",
"https://www.google.com/maps/search/?api=1&query=Sunway+Big+Box+Iskandar+Puteri"
]
]
]
],
"plans": [
[
"Family weekend",
"Wee Hoi Kopitiam breakfast → full day at LEGOLAND → groceries at Mall of Medini → mahjong and pool back at the house. Next day: Puteri Harbour playground → Chua Kee lunch → home via the Second Link."
],
[
"Friends' makan night",
"X Park go-karts in the late afternoon → seafood dinner at Pendas Floating Restaurant → mahjong and pool table back at the house."
],
[
"Shopping and chill day",
"AEON Bukit Indah → Lotus's grocery run → Puteri Harbour at sunset → dinner at Restoran Tian Lai."
]
]
},
"landak": {
"cats": [
[
"Eat",
[
[
"Yu Ee hawker (host tip)",
"Local hawker food right next door",
"about 3 min walk",
"https://www.google.com/maps/search/?api=1&query=Yu+Ee+Taman+Abad+Johor+Bahru"
],
[
"KSL Monday Night Market (Jalan Seladang)",
"Real pasar malam: oyster omelette, satay, muah chee; Mondays only, about 5-10pm, packed after 5:30pm",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=KSL+Monday+Night+Market+Jalan+Seladang"
],
[
"Restoran Yit Foh Wanton Noodle",
"Homemade wanton noodles and char siew, over 50 years old",
"about 5-10 min walk",
"https://www.google.com/maps/search/?api=1&query=Restoran+Yit+Foh+Wanton+Noodle+Taman+Century"
],
[
"Tian Xiang Yong Peng Fish Ball Noodle",
"Handmade fishball noodles, dry, soup or laksa",
"about 5-10 min walk",
"https://www.google.com/maps/search/?api=1&query=Tian+Xiang+Yong+Peng+Fish+Ball+Noodle+Taman+Century"
],
[
"Tasixi Hong Kong Dim Sum (Carton King)",
"Affordable push-cart dim sum",
"about 5-10 min walk",
"https://www.google.com/maps/search/?api=1&query=Tasixi+Hong+Kong+Dim+Sum+Carton+King"
],
[
"You Kee XO (KSL, LG-33)",
"Char siew and crispy siew yoke; go early",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=You+Kee+XO+KSL+City+Mall"
],
[
"Souper Tang (KSL)",
"Soups and Cantonese family meals",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=Souper+Tang+KSL+City+Mall"
],
[
"Arashi Shabu-Shabu (KSL)",
"Japanese hotpot",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=Arashi+Shabu-Shabu+KSL+City"
],
[
"Palates & Bagels by T.A.M",
"Café in a Thai-style bungalow, famous for its bagels; 8am-10pm",
"about 10-15 min walk",
"https://www.google.com/maps/search/?api=1&query=Palates+%26+Bagels+Taman+Melodies"
]
]
],
[
"Shop",
[
[
"KSL City Mall",
"500+ shops, GSC cinema, massage and a supermarket (LG) for groceries",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=KSL+City+Mall+Johor+Bahru"
],
[
"Tao Yuan (KSL, LG-10)",
"Local snacks and keropok to bring home",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=Tao+Yuan+KSL+City+Mall"
],
[
"Holiday Plaza",
"Cheap haircuts, nails and massage, with 100+ salons",
"about 5-10 min walk",
"https://www.google.com/maps/search/?api=1&query=Holiday+Plaza+Johor+Bahru"
],
[
"Mid Valley Southkey",
"JB's poshest mall; Oriental Kopi at LG",
"about 10 min drive",
"https://www.google.com/maps/search/?api=1&query=Mid+Valley+Southkey+Johor+Bahru"
],
[
"JB City Square",
"Across from JB Sentral, handy right after the border; Ming Ang bakery. Upper floors partly closed for renovation",
"about 12 min drive",
"https://www.google.com/maps/search/?api=1&query=Johor+Bahru+City+Square"
]
]
],
[
"Do and kids",
[
[
"Billion Onsen JB (104 Jalan Harimau)",
"Onsen and spa; the KL branch includes free-flow food. Opening was announced for Aug 2026, so confirm it's open",
"about 3-6 min walk",
"https://www.google.com/maps/search/?api=1&query=Billion+Onsen+Jalan+Harimau+Johor+Bahru"
],
[
"Go! Karting (KSL car park L6)",
"Quick karting session",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=Go+Karting+KSL+City+Mall"
],
[
"Dinosaurs Alive Water Theme Park (KSL Hotel)",
"Dino-themed water park for kids",
"about 5 min walk",
"https://www.google.com/maps/search/?api=1&query=Dinosaurs+Alive+Water+Theme+Park+KSL"
],
[
"Cozy Escape Reflexology (Holiday Plaza)",
"Foot reflexology with a free herbal foot bath; 9am-9pm",
"about 5-10 min walk",
"https://www.google.com/maps/search/?api=1&query=Cozy+Escape+Reflexology+Holiday+Plaza"
],
[
"Supreme Bowl (Mid Valley Southkey)",
"Cosmic bowling, darts and pool; popcorn and a drink included",
"about 10 min drive",
"https://www.google.com/maps/search/?api=1&query=Supreme+Bowl+Mid+Valley+Southkey"
],
[
"Danga Bay",
"Waterfront walk, cafés, Ferris wheel",
"about 15-20 min drive",
"https://www.google.com/maps/search/?api=1&query=Danga+Bay+Johor+Bahru"
]
]
],
[
"Practical",
[
[
"Causeway / Bangunan Sultan Iskandar CIQ",
"Avoid Friday evening heading in and Sunday evening heading home",
"about 12 min drive",
"https://www.google.com/maps/search/?api=1&query=Bangunan+Sultan+Iskandar+CIQ"
],
[
"JB Sentral (bus J100 to KSL / Holiday Plaza)",
"Option if you come without a car",
"about 12 min drive",
"https://www.google.com/maps/search/?api=1&query=JB+Sentral"
]
]
]
],
"plans": [
[
"Family weekend",
"Dinosaurs Alive water park → You Kee XO lunch → Tao Yuan snack shopping → Souper Tang dinner → games night at the house (pool table, foosball, darts)."
],
[
"Friends' makan night",
"Yit Foh wanton mee → Go! Karting → KSL Monday Night Market (Mondays) → Cozy Escape reflexology → back for darts and foosball."
],
[
"Shopping and pamper day",
"Palates & Bagels brunch → Mid Valley Southkey and Supreme Bowl → Holiday Plaza haircut/nails."
]
]
},
"tips": [
[
"Driving in needs a VEP.",
"Singapore cars need an activated VEP RFID tag linked to Touch 'n Go, applied for on the JPJ portal, plus valid road tax and insurance. There is an RM20 road charge each time you enter. Apply a week or more ahead.",
"https://vep.jpj.gov.my/",
"JPJ VEP portal"
],
[
"Fill up with RON97 only.",
"Foreign-registered petrol cars must not buy subsidised RON95. Singapore's three-quarter-tank rule also applies when you leave by land.",
"https://www.customs.gov.sg/at-customs/departing-singapore/three-quarter-tank-rule/",
"Singapore Customs"
],
[
"Top up Touch 'n Go.",
"It pays the road charge and most tolls. Top it up before you cross, and carry some ringgit cash for night markets and kopitiams.",
"",
""
],
[
"Time the border.",
"Friday evening into JB and Sunday evening back are the worst. From Prima, the Second Link is usually quicker. From Landak, the Causeway is nearer.",
"",
""
],
[
"Grab works well",
"for getting around JB if you don't drive. Install the app and add a card before you cross. No cross-border pickup is included.",
"",
""
]
]
}
AROUND_NOTE = "New to JB? Here's what's close to the house, with rough travel times and a map link for each place. Times are estimates and depend on traffic. Opening hours change, so check Google Maps before you go. Checked Nov 2026."


def _ar_time(t):
    return ico('walk' if 'walk' in t else 'car', 16) + e(t)


def around_cards(items):
    return ''.join('<li class="arc"><b>%s</b><span class="why">%s</span><span class="t">%s</span><a class="map" href="%s" rel="noopener nofollow" target="_blank">%sMap<span class="sr"> for %s (opens Google Maps)</span></a></li>'
                   % (e(n), e(w), _ar_time(t), e(u), ico('pin', 16), e(n)) for n, w, t, u in items)


def around_section(k):
    A = AROUND[k]
    chips = ''.join('<button type="button" role="tab" data-c="%d" aria-selected="%s">%s <span>%d</span></button>' % (i, 'true' if i == 0 else 'false', e(c), len(it)) for i, (c, it) in enumerate(A['cats']))
    cats = ''.join('<div class="ar-cat%s" data-c="%d" role="tabpanel"><h3>%s</h3><ul class="ar-strip">%s</ul></div>' % (' on' if i == 0 else '', i, e(c), around_cards(it)) for i, (c, it) in enumerate(A['cats']))
    plans = ''.join('<li><b>%s:</b> %s</li>' % (e(t), e(b)) for t, b in A['plans'])
    tips = ''.join('<li><b>%s</b> %s%s</li>' % (e(t), e(b), (' <a href="%s" rel="noopener">%s</a>' % (e(u), e(l))) if u else '') for t, b, u, l in AROUND['tips'])
    return ('<section id="around" class="rv"><h2>Around the house</h2><p class="muted">%s</p><div class="ar" data-ar><div class="ar-chips" role="tablist" aria-label="Nearby places">%s</div>%s</div>'
            '<details class="acc2"><summary>Sample plans %s</summary><ul class="plist">%s</ul><p class="note">Ideas, not packages. No meals, tickets or transport are included.</p></details>'
            '<details class="acc2"><summary>First time in JB? 5 tips for Singaporeans %s</summary><ol class="tips">%s</ol><p class="note">Check current official rules before you travel.</p></details></section>'
            % (e(AROUND_NOTE), chips, cats, ico('down', 20, 'i acc-i'), plans, ico('down', 20, 'i acc-i'), tips))


def around_top3(k):
    """/stays: three nearby highlights for the active house."""
    pick = {'prima': ['LEGOLAND Malaysia', 'Chua Kee Seafood Restaurant', 'Sunway Big Box'], 'landak': ['KSL City Mall', 'KSL Monday Night Market (Jalan Seladang)', 'Yu Ee hawker (host tip)']}[k]
    allp = {n: (n, w, t, u) for _c, it in AROUND[k]['cats'] for n, w, t, u in it}
    items = [allp[n] for n in pick]
    return ('<div class="near3" id="around-%s"><h3>Around %s</h3><ul class="ar-strip">%s</ul><a class="link" href="{R}stays/%s/#around">All nearby places and sample plans %s</a></div>'
            % (k, 'Prima' if k == 'prima' else 'Landak', around_cards(items), HOUSES[k]['slug'], ico('arrow', 18)))

# ---------------------------------------------------------------- page bodies
SG_CHIPS = {'prima': [('car', 'About 10 min from Tuas Second Link')],
            'landak': [('walk', '5-min walk to KSL City Mall')]}
AREA = {'prima': 'Gelang Patah, Iskandar Puteri', 'landak': 'Taman Abad, Johor Bahru'}
BADGE = {'prima': 'For big groups', 'landak': 'Games house'}


def specs(k, cls='specs'):
    h = HOUSES[k]
    items = [('users', 'Up to %d guests' % h['guests']), ('bed', '%d bedrooms' % h['beds']), ('bath', '3 bathrooms')]
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s%s</li>' % (ico(i, 18), e(t)) for i, t in items))


def house_card(k, eager=False):
    h = HOUSES[k]
    imgs = CARD_IMG[k]
    strip = ''.join('<span class="slide">%s</span>' % pimg(f, sizes='(min-width:1200px) 180px, (min-width:800px) 15vw, 100vw') for f in imgs[1:])
    sg = ''.join('<li>%s%s</li>' % (ico(i, 16), e(t)) for i, t in SG_CHIPS[k])
    return ('<article class="hcard rv"><div class="cimg cz" data-carousel aria-roledescription="carousel" aria-label="Photos of %s"><div class="track"><div class="ph slide">%s<span class="badge">%s</span></div><div class="strip">%s</div></div>'
            '<button class="cbtn prev" type="button" aria-label="Previous photo">%s</button><button class="cbtn next" type="button" aria-label="Next photo">%s</button><span class="cnt" aria-hidden="true">1 / %d</span></div>'
            '<div class="cb"><p class="area">%s%s</p><h3><a href="{R}stays/%s/">%s</a></h3>%s<ul class="sg">%s</ul>'
            '<div class="price-row">%s</div><p class="cinc">Per night, whole house, cleaning included.</p><a class="btn btn-pri card-cta" href="{R}stays/%s/">View house %s</a></div></article>'
            % (e(h['name']), pimg(imgs[0], sizes='(min-width:1200px) 560px, (min-width:800px) 46vw, 100vw', eager=eager, lazy=not eager), BADGE[k], strip, ico('left', 22), ico('right', 22), len(imgs),
               ico('pin', 16), e(AREA[k]), h['slug'], e(h['name']), specs(k), sg, tiers_html(k),
               h['slug'], ico('arrow', 18)))


HOME_FAQ = [
    ('How do I book?', 'Message Daniel on WhatsApp at %s with your dates, group size and the house you like. Pay by %s. %s' % (WA_SHOW, PAY_SHORT, DEPOSIT)),
    ('How much is a night?', 'Per night for the whole house, cleaning included. Prima: ' + tiers_rm('prima') + '. Landak Kawan Fun House: ' + tiers_rm('landak') + '. Prices are in Malaysian ringgit (RM).'),
    ('How many guests can stay?', 'Prima takes up to 12 guests in 3 bedrooms, and Landak Kawan Fun House up to 10 in 3 bedrooms.'),
    ('Is there a minimum stay?', 'The minimum stay is 1 night, or 2 nights over Christmas Eve and Christmas Day.'),
    ('What are the check-in and check-out times?', 'Both houses: check-in 3:00 pm, check-out 11:00 am, with self check-in details sent after a firm booking.'),
    ('Are pets, smoking and BBQ allowed?', 'No pets, and no smoking, vaping or durian indoors (RM 500 penalty). No BBQ at either house. Quiet hours at both houses are 11:00 pm to 7:00 am.'),
    ('Is there parking, and can we cook?', 'Prima has parking for 2 cars inside and 6 outside, and 2 cars park inside the gate at Landak Kawan Fun House. Prima has a kitchen; Landak Kawan Fun House has a kitchen for light cooking.'),
    ('Can we hold a larger gathering, and what is the cancellation policy?', 'Gatherings need the host\'s approval. ' + DEPOSIT + ' There is no cancellation, but you can change your dates once.'),
]


def route_list():
    """Phone version of the route diagram: plain vertical lists (the SVG shows from 768 px)."""
    def chain(title, steps):
        li = ''.join('<li class="%s">%s</li>' % (c, t) for c, t in steps)
        return '<div class="rl-card"><p class="rl-h">%s</p><ol class="rl">%s</ol></div>' % (title, li)
    return ('<div class="rlist">' +
            chain('Second Link', [('', '<b>Singapore</b>'), ('', '<b>Tuas checkpoint</b>'), ('t', 'about 10 min'), ('end', '<b>Prima</b><span>Iskandar Puteri &middot; up to 12 guests</span>')]) +
            chain('Causeway', [('', '<b>Singapore</b>'), ('', '<b>Woodlands checkpoint</b>'), ('', '<b>JB CIQ</b>'), ('t', 'about 12 min'), ('end', '<b>Landak Kawan Fun House</b><span>Taman Abad &middot; up to 10 guests &middot; 5-min walk to KSL City Mall</span>')]) +
            chain('RTS Link (not running yet)', [('', '<b>Woodlands North</b>'), ('t', 'about 5 min by train'), ('end', '<b>Bukit Chagar</b><span>Expected from February 2027</span>')]) + '</div>')


def route_map(rl=False):
    """Schematic (not to scale) of Singapore -> Second Link / Causeway -> the two houses. Times are host-stated."""
    return ('<figure class="mapcard%s">' % (' has-rl' if rl else '') + (route_list() if rl else '') + '<svg class="map-w" viewBox="0 0 640 420" role="img" aria-labelledby="mapt mapd" font-family="Geist,system-ui,sans-serif">'
            '<title id="mapt">Route diagram from Singapore to the two JB Airbnb houses</title>'
            '<desc id="mapd">Schematic, not to scale. From Singapore, the Second Link at Tuas leads to Prima in Iskandar Puteri, about 10 minutes as stated by the host. The Causeway at Woodlands leads to JB CIQ; Landak Kawan Fun House in Taman Abad is about 12 minutes from CIQ (host estimate) and a 5-minute walk from KSL City Mall. The RTS Link from Woodlands North to Bukit Chagar is expected from February 2027.</desc>'
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
            '<text x="210" y="100" font-size="15" font-weight="700" fill="#0a1f38">Prima</text><text x="210" y="118" font-size="12" fill="#45566b">Iskandar Puteri &#183; up to 12 guests</text>'
            '<rect x="80" y="146" width="98" height="26" rx="13" fill="#0a1f38"/><text x="129" y="163" font-size="12" font-weight="600" fill="#fff" text-anchor="middle">about 10 min</text>'
            '<circle cx="508" cy="120" r="16" fill="#e8a33d"/><path d="M500 121 508 113l8 8h-2.5v7h-11v-7z" fill="#0a1f38"/>'
            '<text x="496" y="80" font-size="15" font-weight="700" fill="#0a1f38" text-anchor="end">Landak Kawan</text><text x="496" y="97" font-size="12" fill="#45566b" text-anchor="end">Taman Abad &#183; up to 10 guests</text>'
            '<rect x="518" y="146" width="106" height="26" rx="13" fill="#0a1f38"/><text x="571" y="163" font-size="12" font-weight="600" fill="#fff" text-anchor="middle">12 min to CIQ</text>'
            '<text x="532" y="64" font-size="12" fill="#a86d15" font-weight="600">KSL City Mall</text><text x="532" y="79" font-size="12" fill="#45566b">5-min walk</text>'
            '<path d="M520 110 C526 98 528 90 532 84" stroke="#a86d15" stroke-width="1.5" fill="none" stroke-dasharray="3 3"/>'
            '</svg><figcaption>Schematic, not to scale. Drive and walk times are host estimates and exclude border queues.</figcaption></figure>')


def article_card(a, sizes='(min-width:760px) 33vw, 100vw'):
    return ('<article class="acard rv"><span class="ph">%s</span><div class="cb"><span class="tag">Guide</span><h3><a href="{R}articles/%s/">%s</a></h3><p>%s</p>'
            '<span class="go">Read the guide %s</span></div></article>' % (pimg(PAGE_IMG[a['slug']], sizes=sizes), a['slug'], e(a['title']), e(a['desc']), ico('arrow', 18)))


def home_body():
    faq_html, faq_ld = faq_block(faqs('cost', 'fit', 'cancel', 'time'), None, cta='<p class="after-faq">%s</p>' % wa_btn('Ask us on WhatsApp', wa_msg(), 'home-faq'))
    PENDING.setdefault('', []).append(faq_ld)
    facts = [('home', '2 private houses'), ('users', 'Up to 10 or 12 guests'), ('car', 'About 10 min from Tuas Second Link'), ('walk', '5-min walk to KSL City Mall')]
    facts_html = ''.join('<li>%s%s</li>' % (ico(i, 20), e(t)) for i, t in facts)
    P, L = HOUSES['prima'], HOUSES['landak']
    pv = '<a class="btn btn-line btn-sm" href="{R}stays/%s/">View %s</a>'
    chooser = ('<div class="chooser rv" aria-labelledby="ch-h"><h3 id="ch-h">Which house fits your weekend?</h3>'
               '<input type="radio" name="gs" id="gs1" class="sr"><input type="radio" name="gs" id="gs2" class="sr"><input type="radio" name="gs" id="gs3" class="sr">'
               '<div class="ch-opts" role="group" aria-label="Group size"><label for="gs1">1 to 10 guests</label><label for="gs2">11 or 12 guests</label><label for="gs3">13 or more</label></div>'
               '<div class="ch-res"><p class="r0">Tap your group size to see which house fits.</p>'
               '<div class="r1"><p>Both houses fit. Pick <b>Landak</b> for KSL City Mall on foot and a games room, or <b>Prima</b> for a 7ft pool table, mahjong and parking for 8 cars.</p><p class="ch-btns">%s%s</p></div>'
               '<div class="r2"><p><b>Prima</b> is the one: up to 12 guests in 3 rooms, each with 1 queen bed and 2 single floor mattresses.</p><p class="ch-btns">%s</p></div>'
               '<div class="r3"><p>Neither house takes more than 12 guests. Booking both means two separate homes in different parts of JB (up to 22 guests in total), not one venue. Ask us what works for your group.</p><p class="ch-btns">%s</p></div></div></div>'
               % (pv % (L['slug'], 'Landak'), pv % (P['slug'], 'Prima'), pv % (P['slug'], 'Prima'), wa_btn('Ask us on WhatsApp', wa_msg(), 'home-chooser', 'btn btn-wa btn-sm')))
    trust = [('chat', 'Daniel, your host', 'Based in Singapore and JB, speaks English, Malay and Chinese. WhatsApp %s.' % WA_SHOW),
             ('grid', 'Real photos of both houses', 'Every photo on the house pages is the actual house, room by room.'),
             ('star', 'Airbnb ratings', 'Prima: %s. Landak: %s.' % (rating_link('prima', P['rating'].replace('Rated ', 'rated ')), rating_link('landak', L['rating'].replace('Rated ', 'rated ')))),
             ('home', 'Cleaning included', 'Nightly prices include professional cleaning, fresh linen, towels and toiletries.')]
    trust_html = ''.join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (ico(i, 24), e(t), d if '<a ' in d else e(d)) for i, t, d in trust)
    plans = [('prima', 'Prima: a family weekend', 'Wee Hoi Kopitiam breakfast, a full day at LEGOLAND, groceries at Mall of Medini, then mahjong and pool back at the house.'),
             ('landak', 'Landak: a KSL weekend', 'Dinosaurs Alive water park, You Kee XO lunch at KSL, Souper Tang dinner, then pool table, foosball and darts at the house.')]
    plans_html = ''.join('<li><b>%s</b><span>%s</span><a class="link" href="{R}stays/%s/#around">What is around %s %s</a></li>'
                         % (e(t), e(d), HOUSES[k]['slug'], 'Prima' if k == 'prima' else 'Landak', ico('arrow', 18)) for k, t, d in plans)
    steps = [('Choose a house, send dates and group size.', 'Prima for up to 12 near Tuas, Landak for up to 10 near KSL. Message us on WhatsApp.'),
             ('Book and pay.', 'PayNow or PayLah from Singapore, bank transfer or TNG eWallet from Malaysia, or the Airbnb listing. RM 1,000 refundable deposit. No cancellation, but you can change your dates once.'),
             ('Plan the crossing.', 'Self check-in details are sent after a firm booking. Check-in 3pm, check-out 11am. Bring your passport and check ICA traffic updates.')]
    steps_html = ''.join('<li><div><b>%s</b><span>%s</span></div></li>' % (e(a), e(b)) for a, b in steps)
    arts = ''.join(article_card(a) for a in ARTICLES)
    return (
        '<section class="hero"><div class="hero-bg">%s</div><div class="wrap hero-in">'
        '<p class="kick">%s</p><h1><span class="display">JB staycation for Singapore groups</span></h1>'
        '<p class="sub">Your whole group, one private house in JB, from RM 450 a night with cleaning included.<span class="more"> Prima for up to 12 near Tuas, or Landak for up to 10, a 5-minute walk from KSL.</span></p>'
        '<div class="cta-row"><a class="btn btn-pri" href="#houses">View houses %s</a></div>'
        '<ul class="facts" aria-label="At a glance">%s</ul></div><p class="hcap">AI-created atmosphere image; see real house photos below.</p></section>'
        '<section class="sec" id="houses"><div class="wrap"><div class="sec-head split rv"><div><p class="eyebrow">Two private houses</p><h2>Choose Prima or Landak</h2></div>'
        '<p class="lead hm">Prima takes up to 12 near the Tuas Second Link. Landak Kawan Fun House sleeps up to 10, a 5-minute walk from KSL City Mall. Prima from RM 450 and Landak from RM 550 a night.</p></div>'
        '<div class="cards">%s%s</div>%s%s</div></section>'
        '<section class="sec trust-sec"><div class="wrap"><h2 class="rv">Why groups book direct with us</h2><ul class="trust rv">%s</ul></div></section>'
        '<section class="sec"><div class="wrap"><div class="sec-head rv"><p class="eyebrow">Around the houses</p><h2>Plan a weekend, not just a room</h2></div>'
        '<ul class="plans rv">%s</ul><p class="note">Sample plans from our guides, not packages. No meals, tickets or transport are included.</p></div></section>'
        '<section class="sec" style="background:#fff;border-top:1px solid var(--line)"><div class="wrap faqgrid"><div class="rv"><p class="eyebrow">How booking works</p><h2>Three steps</h2><ol class="steps">%s</ol></div>'
        '<div class="rv"><h2 class="faq-h">Before you ask</h2>%s<p><a class="link" href="{R}faq/">All 15 questions %s</a></p></div></div></section>'
        '<section class="sec gsec"><div class="wrap"><details class="fold" id="guides"><summary><span class="st"><span class="eyebrow">JB guide for Singaporeans</span><h2>Plan it like a local</h2></span>%s</summary>'
        '<div class="fold-body"><div class="arts">%s</div><p><a class="link" href="{R}articles/">The full JB guide for Singaporeans %s</a></p></div></details>'
        '<script>if(innerWidth>=900)document.currentScript.previousElementSibling.open=true</script></div></section>'
        % (hero_picture(), e(TAGLINE), ico('arrow', 18), facts_html,
           house_card('prima'), house_card('landak'), chooser, fx_note(), trust_html, plans_html, steps_html, faq_html, ico('arrow', 18),
           ico('x', 22, 'i pm'), arts, ico('arrow', 18)))


STAYS_FAQ = faqs('cost', 'fit', 'pool', 'cancel', 'time')
CMP_ROWS = [
    ('Area', 'Gelang Patah, Iskandar Puteri', 'Taman Abad, Johor Bahru'),
    ('Guests', 'Up to 12 (3 rooms, each 1 queen + 2 floor mattresses)', 'Up to 10'),
    ('Bedrooms', '3', '3 (5 beds: 1 king, 4 queen)'),
    ('Bathrooms', '3', '3, with water heaters'),
    ('Parking', '2 cars inside, 6 outside', '2 cars inside'),
    ('Weekday, per night', 'RM 450 (about S$142)', 'RM 550 (about S$174)'),
    ('Weekend, per night', 'RM 650 (about S$205)', 'RM 750 (about S$237)'),
    ('Public holiday, per night', 'RM 750 (about S$237)', 'RM 1,000 (about S$316)'),
    ('Per person on a weekday, full house', PP_WEEKDAY['prima'] + ' at 12 guests', PP_WEEKDAY['landak'] + ' at 10 guests'),
    ('Ground-floor bedroom', 'Yes, no stairs needed for elderly guests', 'Double-storey with stairs; WhatsApp Daniel to check'),
    ('Standout fun', '7ft pool table, mahjong', '8ft pool table, foosball, 2 dart boards, mahjong, TV arcade, children\'s playroom, dedicated workstation'),
    ('Nearby', 'LEGOLAND and Puteri Harbour about 15-20 min drive; about 10 min from Tuas Second Link', 'KSL City Mall 5-min walk; about 12 min from Causeway CIQ'),
    ('BBQ', 'No BBQ', 'No BBQ'),
    ('Check-in / out', 'Check-in 3:00 pm, check-out 11:00 am', 'Check-in 3:00 pm, check-out 11:00 am'),
    ('Minimum stay', '1 night (2 over Christmas Eve and Day)', '1 night (2 over Christmas Eve and Day)'),
    ('Cleaning', 'Included in the nightly price', 'Included in the nightly price'),
    ('Deposit', 'RM 1,000 refundable, back within 48 hours after checkout', 'RM 1,000 refundable, back within 48 hours after checkout'),
    ('Cancellation', 'No cancellation; dates can be changed once', 'No cancellation; dates can be changed once'),
]


def stays_card(k):
    h = HOUSES[k]
    imgs = STAYS_IMG[k]
    slides = ''.join('<div class="slide">%s</div>' % (
                     pimg(f, eager=True, lazy=False, sizes='(min-width:1024px) 600px, 100vw') if i == 0 else pimg800(f)) for i, f in enumerate(imgs))
    facts = [('users', '%d guests' % h['guests']), ('bed', '%d bedrooms' % h['beds'])] + ([('bed', '5 beds')] if k == 'landak' else []) + [('bath', '3 bathrooms'), ('cal', 'From %s / night' % rm(PRICES[k][0]))]
    short = {'%d guests' % h['guests']: '%d guests' % h['guests'], '%d bedrooms' % h['beds']: '%d bed' % h['beds'], '5 beds': None, '3 bathrooms': '3 bath', 'From %s / night' % rm(PRICES[k][0]): 'From %s' % rm(PRICES[k][0])}
    facts_html = ''.join('<li%s>%s<span class="lf">%s</span>%s</li>' % ('' if short[t] else ' class="nm"', ico(i, 20), e(t), ('<span class="sf" aria-hidden="true">%s</span>' % e(short[t])) if short[t] else '') for i, t in facts)
    top = ''.join('<li>%s<span>%s</span></li>' % (ico(amen_icon(a), 24), e(a)) for a in h['top'])
    return ('<article class="scard rv" id="%s"><div class="scar cz" data-carousel data-dots aria-roledescription="carousel" aria-label="Photos of %s"><div class="track" tabindex="0">%s</div>'
            '<button class="cbtn prev" type="button" aria-label="Previous photo">%s</button><button class="cbtn next" type="button" aria-label="Next photo">%s</button>'
            '<span class="cnt" aria-hidden="true">1 / %d</span><div class="dots" aria-hidden="true"></div><a class="seeall" href="#album-%s">%sSee all %d photos</a></div>'
            '<div class="scb"><p class="area">%s%s</p><h2>%s</h2><ul class="kf">%s</ul><ul class="ami">%s</ul>'
            '%s<p class="sgd">Per night, whole house, cleaning included &middot; %s per person on a weekday at %d guests</p>%s'
            '<p class="bestfor">%s.</p><p class="rating">%s%s</p>'
            '<div class="scta">%s<a class="btn btn-line" href="{R}stays/%s/">View house %s</a></div>'
            '<nav class="jl" aria-label="Jump to"><a href="#album-%s">Photos</a><a href="#cmp">Essentials</a><a href="#around-%s">Around here</a></nav></div></article>'
            % (k, e(h['name']), slides, ico('left', 22), ico('right', 22), len(imgs), k, ico('grid', 18), sum(len(fs) for _g, fs in ALBUM[k]),
               ico('pin', 16), e(AREA[k]), e(h['name']), facts_html, top, tiers_html(k), PP_WEEKDAY[k], h['guests'],
               '<p class="snote">Up to 12 guests: 3 rooms, each with 1 queen bed and 2 single floor mattresses. Ground-floor bedroom for elderly guests. No BBQ.</p>' if k == 'prima' else '<p class="snote">No BBQ. Completed September 2026 (host-stated).</p>',
               e(h['bestfor']), ico('star', 16), '<span>%s</span>' % rating_link(k),
               wa_btn('Check dates for %s' % h['name'].replace(' Kawan Fun House', ''), h['msg'], 'stays-' + k), h['slug'], ico('arrow', 18), k, k))


def album(k):
    h = HOUSES[k]
    n = sum(len(fs) for _g, fs in ALBUM[k])
    groups = ''.join('<div class="ag"><h4>%s <span>%d</span></h4><div class="agrid">%s</div></div>'
                     % (e(g), len(fs), ''.join('<a href="{R}img/%s" data-lb data-cap="%s">%s</a>' % (f, e(ALT[f]), pimg800(f))
                                             for f in fs)) for g, fs in ALBUM[k])
    return ('<section class="album" id="album-%s" aria-labelledby="alb-%s"><h3 id="alb-%s">Full photo album: %s <span>%d photos</span></h3>%s'
            '<p class="after-gal">%s</p></section>' % (k, k, k, e(h['name']), n, groups, wa_btn('Check dates for %s' % h['name'].replace(' Kawan Fun House', ''), h['msg'], 'album-' + k)))


def stays_body():
    faq_html, faq_ld = faq_block(STAYS_FAQ, '')
    faq_html = ('<details class="acc" open><summary><h2>Questions about our houses</h2>%s</summary>%s</details>'
                '<script>if(matchMedia("(max-width:767px)").matches)document.currentScript.previousElementSibling.removeAttribute("open")</script>'
                '<p class="after-faq">%s</p>' % (ico('down', 22, 'i acc-i'), faq_html, wa_btn('Ask us on WhatsApp', wa_msg(), 'stays-faq')))
    PENDING.setdefault('stays/', []).append(faq_ld)
    rows = ''.join('<tr><th scope="row">%s</th><td data-label="Prima">%s</td><td data-label="Landak">%s</td></tr>' % (e(a), e(b), e(c)) for a, b, c in CMP_ROWS)
    return ('<div class="wrap body"><nav class="hsw" aria-label="Choose a house"><a href="#prima" data-h="prima"><b>Prima</b><small>up to 12 &middot; from RM 450</small></a><a href="#landak" data-h="landak"><b>Landak</b><small>up to 10 &middot; from RM 550</small></a></nav>'
            '<script>document.documentElement.setAttribute("data-house",location.hash==="#landak"?"landak":"prima")</script>'
            '<div class="scards"><div class="hpane" data-house="prima" data-lb-set>%s%s%s</div><div class="hpane" data-house="landak" data-lb-set>%s%s%s</div></div>'
            '<section class="rv cmp-sec" id="cmp"><p class="eyebrow">Side by side</p><details class="acc" open><summary><h2>Which house is right for you?</h2>%s</summary><div class="cmp"><table><thead><tr><th scope="col"><span class="sr">Detail</span></th><th scope="col">Prima</th><th scope="col">Landak Kawan Fun House</th></tr></thead><tbody>%s</tbody></table></div>'
            '<p class="note">Drive times are host estimates, excluding border queues. Prices in RM; SGD is an estimate.</p>%s</details>'
            '<script>if(matchMedia("(max-width:767px)").matches)document.currentScript.previousElementSibling.removeAttribute("open")</script><div class="cmp-cta">%s%s</div></section>'
            '<section class="rv" id="faq">%s</section></div>'
            '<section class="sec band stays-band"><div class="bg">%s</div><div class="wrap rv"><p class="eyebrow">Book direct</p><h2>Tell us your dates and group size</h2><p>We reply on WhatsApp with the rate and availability for the house you pick.</p>%s</div></section>'
            % (stays_card('prima'), album('prima'), around_top3('prima') + reviews_compact('prima'), stays_card('landak'), album('landak'), around_top3('landak') + reviews_compact('landak'), ico('down', 22, 'i acc-i'), rows, fx_note(),
               wa_btn('WhatsApp about Prima', HOUSES['prima']['msg'], 'cmp-prima'), wa_btn('WhatsApp about Landak', HOUSES['landak']['msg'], 'cmp-landak'), faq_html, pimg(STAYS_BAND_IMG, sizes='100vw'), wa_btn('Message us on WhatsApp', wa_msg(), 'stays-band')))


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


def enquiry_form(k):
    nm = 'Prima' if k == 'prima' else 'Landak'
    return ('<form class="enq" data-house="%s" data-from="house" novalidate><p class="enq-h">Check dates on WhatsApp</p>'
            '<div class="enq-g"><label>Check-in<input type="date" name="in"></label><label>Check-out<input type="date" name="out"></label>'
            '<label>Adults<input type="number" name="ad" min="1" max="%d" inputmode="numeric"></label><label>Children<input type="number" name="ch" min="0" max="%d" inputmode="numeric"></label></div>'
            '<p class="enq-err" role="alert" hidden>Check-out must be after check-in.</p>'
            '<button type="submit" class="btn btn-wa" data-cta="whatsapp" data-cta-label="enquiry-%s">%s<span>Check dates for %s</span></button>'
            '<p class="enq-n">Optional. This opens WhatsApp with your message ready; nothing is sent until you press send.</p></form>'
            % (nm, HOUSES[k]['guests'], HOUSES[k]['guests'], k, WA_SVG, nm))

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
    meta = [('pin', AREA[k]), ('users', 'Up to %d guests' % h['guests']), ('bed', '%d bedrooms' % h['beds']), ('bath', '3 bathrooms')]
    meta_html = ''.join('<li>%s%s</li>' % (ico(i, 18), e(t)) for i, t in meta)
    sub = ''.join('<a href="#%s">%s</a>' % (a, b) for a, b in [('spaces', 'Photos'), ('amenities', 'Amenities'), ('sleep', 'Sleeping'), ('rules', 'House rules'), ('around', 'Around the house'), ('reviews', 'Reviews'), ('faq', 'FAQ'), ('book', 'Check dates &amp; rate')])
    stat_ic = {'Guests': 'users', 'Bedrooms': 'bed', 'Bathrooms': 'bath', 'Rate': 'cal'}
    stats = ''.join('<li>%s<small>%s</small><b>%s</b></li>' % (ico(stat_ic.get(a, 'check'), 22), a, e(b)) for a, b in h['stats'])
    amen = ''.join('<li>%s<span>%s</span></li>' % (ico(amen_icon(a), 26), e(a)) for a in h['amen'])
    rule_ic = lambda r: 'no' if r.startswith('No ') else ('clock' if r.startswith('Check') or r.startswith('Quiet') else ('party' if r.startswith('Larger') else ('key' if r.startswith('Self') else 'check')))
    rules = ''.join('<li>%s<span>%s</span></li>' % (ico(rule_ic(r), 20), e(r)) for r in h['rules'])
    near = ''.join('<li><span>%s%s</span><b>%s</b></li>' % (ico('walk' if 'walk' in b else 'car', 18), e(a), e(b)) for a, b in h['near'])
    intro = '<p>%s</p>' % e(h['intro'][0])
    more = ''.join('<p>%s</p>' % e(t) for t in h['intro'][1:])
    if k == 'prima':
        more += '<p>Looking for a group homestay in JB near the Second Link? Prima is a landed house with 3 rooms and 3 bathrooms for up to 12 guests at %s a night, cleaning included.</p>' % tiers_full('prima')
    gal_cta = '<p class="after-gal">%s</p>' % wa_btn('Check dates on WhatsApp', h['msg'], 'gallery-' + k)
    spaces_cta = '<p class="after-gal">%s</p>' % wa_btn('Like what you see? Check dates', h['msg'], 'spaces-' + k)
    ok = 'landak' if k == 'prima' else 'prima'
    other = HOUSES[ok]
    side_items = [('users', 'Up to %d guests' % h['guests']), ('bed', '%d bedrooms, 3 bathrooms' % h['beds']), ('cal', h['minstay']), ('cal', '%s per person on a weekday at %d guests (full house)' % (PP_WEEKDAY[k], h['guests'])),
                  ('key', 'Self check-in after 3:00 pm' if k == 'landak' else 'Self check-in'), ('star', ('RAW', rating_link(k))), ('chat', 'Book directly on WhatsApp')]
    side = ('<aside class="side rv" id="book" aria-label="Rate and booking"><p class="side-h">Per night, whole house</p>%s<p class="sgd-s">Cleaning included. %s</p>'
            '<ul>%s</ul>%s%s<p class="note">Prices are in RM. Message Daniel for availability on your dates.</p>%s</aside>'
            % (tiers_html(k), DEPOSIT, ''.join('<li>%s%s</li>' % (ico(i, 18), ('<span>%s</span>' % t[1]) if isinstance(t, tuple) else e(t)) for i, t in side_items), enquiry_form(k), wa_btn('Check dates & rate', h['msg'], k, 'btn btn-wa enq-alt'), fx_note()))
    return ('<div class="htop"><div class="wrap">%s<h1>%s</h1><ul class="hmeta">%s</ul><nav class="subnav" aria-label="On this page">%s</nav>%s%s</div></div>'
            '<div class="wrap hlay"><div class="hmain">'
            '<section class="intro rv"><p class="answer">%s</p><h2 class="htag">%s</h2><ul class="stats">%s</ul>%s</section>'
            '<section id="amenities" class="rv mfold"><h2><button type="button" class="mf-h" aria-expanded="false" aria-controls="mf-amen">What is included<svg class=\"i mf-i\" viewBox=\"0 0 24 24\" width=\"22\" height=\"22\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"m6 9 6 6 6-6\"/></svg></button></h2><div class="mf-b" id="mf-amen"><ul class="amen">%s</ul></div></section>'
            '<section id="spaces"><h2 class="rv">Explore the spaces</h2><p class="muted rv">%d photos, room by room. Tap any photo to open it full screen.</p>%s%s</section>'
            '<section id="about" class="rv mfold"><h2><button type="button" class="mf-h" aria-expanded="false" aria-controls="mf-about">About this house<svg class=\"i mf-i\" viewBox=\"0 0 24 24\" width=\"22\" height=\"22\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><path d=\"m6 9 6 6 6-6\"/></svg></button></h2><div class="mf-b" id="mf-about">%s</div></section>'
            '<section id="sleep" class="rv"><h2>Sleeping arrangements</h2><ul class="rules">%s</ul></section>'
            '<section class="rv"><details id="rules" class="acc2 rulesacc"><summary><h2>House rules and times</h2>%s</summary><ul class="rules%s">%s</ul></details></section>'
            '<section id="location" class="rv"><h2>Location</h2><p class="addr">%s<span>%s</span></p><ul class="near">%s</ul><p class="note">%s See <a href="{R}getting-there/">getting there from Singapore</a>.</p></section>'
            '%s'
            '%s<section id="faq" class="rv">%s</section>'
            '<section class="rv"><h2>The other house</h2><a class="ocard" href="{R}stays/%s/"><span class="ph">%s</span><span><b>%s</b><small>%s &middot; up to %d guests &middot; from RM %d a night</small><span class="go">View house %s</span></span></a>'
            '<p class="note" style="margin-top:16px">Or read <a href="{R}articles/jb-homestay-for-big-groups-12-guests/">how to choose a house for a big group</a>.</p></section></div>'
            '%s</div>'
            % (crumbs_html(crumbs), e(H1S[k]), meta_html, sub, gal, gal_cta, e(ANSWER[k]), e(h['tag']), stats, intro, amen, n_all, room_gallery(k), spaces_cta, more,
               ''.join('<li>%s<span>%s</span></li>' % (ico('bed', 20), e(t)) for t in SLEEP[k]),
               ico('down', 22, 'i acc-i'), ' one' if len(h['rules']) == 1 else '', rules, ico('pin', 20), e(h['addr']), near, e(h['near_note']), around_section(k), reviews_html(k), faq_html,
               other['slug'], pimg(CARD_IMG[ok][0], sizes='200px'), e(other['name']), e(AREA[ok]), other['guests'], other['price'], ico('arrow', 18), side))


def prices_body():
    rows = ''.join('<tr><th scope="row"><a href="{R}stays/%s/">%s</a></th>%s<td data-label="Per person, weekday">%s at %d guests</td><td data-label="Guests">Up to %d</td></tr>'
                   % (HOUSES[k]['slug'], e(HOUSES[k]['name']), ''.join('<td data-label="%s">%s<br><small>about %s</small></td>' % (t, rm(n), sgd_of(n)) for t, n in zip(TIER_NAMES, PRICES[k])),
                      PP_WEEKDAY[k], HOUSES[k]['guests'], HOUSES[k]['guests']) for k in ORDER)
    return ('<div class="wrap body prose"><div class="tw"><table><thead><tr><th>House</th><th>Weekday</th><th>Weekend</th><th>Public holiday</th><th>Per person (weekday, full house)</th><th>Guests</th></tr></thead><tbody>%s</tbody></table></div>%s'
            '<section class="rv"><h2>What is included</h2><p><b>Prima (landed house):</b> ground-floor bedroom (no stairs needed), 7ft pool table, mahjong table, Wi-Fi, air conditioning, kitchen, parking for 2 cars inside and 6 outside, 2 TVs with Netflix, washer, covered balcony and a study desk. 3 rooms (each 1 queen bed and 2 single floor mattresses), 3 bathrooms, up to 12 guests.</p>'
            '<p><b>Landak Kawan Fun House (KSL landed fun house):</b> 8ft pool table, foosball, 2 dart boards, mahjong table, 55-inch TV arcade, board games, children\'s playroom, dedicated workstation, 100 Mbps Wi-Fi, air conditioning, kitchen for light cooking, parking for 2 cars inside, washer, hair dryer and iron. 3 bedrooms, 3 bathrooms with water heaters, 5 beds (1 king, 4 queens), up to 10 guests.</p></section>'
            '<section class="rv"><h2>Good to know</h2><ul><li>All prices are in Malaysian ringgit (RM).</li><li>Prices are per night for the whole house, with weekday, weekend and public holiday rates. For your group size or a gathering, WhatsApp Daniel.</li><li>Cleaning is included in the nightly price.</li><li>Minimum stay: 1 night (2 over Christmas Eve and Christmas Day).</li><li>Per-person figures split the weekday whole-house rate at full occupancy; they are not bookable bed prices.</li><li>%s</li><li>%s</li><li>No cancellation, but you can change your dates once.</li><li>Gatherings need the host\'s approval.</li>'
            '<li>Early check-in or late checkout: RM 100 an hour, subject to availability (you can ask for a waiver).</li><li>No BBQ at either house.</li></ul>%s</section></div>'
            % (rows, fx_note(), PAY, DEPOSIT, wa_btn('Message for dates and rates', wa_msg(), 'prices')))


def gt_body():
    srcs = ''.join('<li><a href="%s" rel="noopener">%s</a> (%s)</li>' % (e(u), e(t), e(n)) for t, u, n in [SRC[k] for k in ('lta_feb', 'lta_rts', 'ica_qr', 'ica_traffic')])
    return ('<div class="wrap body"><div class="prose"><div class="answer">There are two road crossings from Singapore, at Woodlands and Tuas. The RTS Link train from Woodlands North to Bukit Chagar is expected to start in February 2027. Prima is nearer Tuas; Landak Kawan Fun House is nearer CIQ and KSL City Mall.</div></div>'
            '<div class="gt-map" style="max-width:860px;margin:0 0 36px">%s</div><div class="prose">'
            '<div class="tw rv"><table><thead><tr><th>Route</th><th>What we can confirm</th><th>Suits</th></tr></thead><tbody>'
            '<tr><th scope="row">Woodlands (Causeway)</th><td data-label="What we can confirm">ICA operates the Woodlands land checkpoint. Host estimate from JB CIQ to Landak: about 12 minutes, excluding queues.</td><td data-label="Suits">Landak Kawan Fun House</td></tr>'
            '<tr><th scope="row">Tuas (Second Link)</th><td data-label="What we can confirm">ICA operates the Tuas land checkpoint. Host estimate to Prima: about 10 minutes on the Malaysian side, excluding queues.</td><td data-label="Suits">Prima</td></tr>'
            '<tr><th scope="row">RTS Link</th><td data-label="What we can confirm">Woodlands North to Bukit Chagar, about 5 minutes by train, co-located immigration. Service expected from February 2027, subject to safety certification.</td><td data-label="Suits">Not yet running</td></tr></tbody></table></div>'
            '<section class="rv"><h2>By road: Woodlands or Tuas</h2><p>ICA runs the land checkpoints at Woodlands and Tuas. Traffic can build up on long weekends and holidays, so check ICA\'s <a href="%s" rel="noopener">driving in and out of Singapore page</a> before you leave.</p>'
            '<p>Bring your passport. ICA says you must still bring it for travel when using QR code clearance. ICA also offers QR code clearance through the MyICA app at both checkpoints (see its <a href="%s" rel="noopener">QR code page</a>).</p></section>'
            '<section class="rv"><h2>By train: the RTS Link</h2><p>LTA describes the RTS Link as connecting Woodlands North in Singapore with Bukit Chagar in Johor Bahru, a train journey of about five minutes, with Customs, Immigration and Quarantine facilities co-located so passengers clear both countries at their departure point.</p>'
            '<p>On 2 October 2026 LTA published that passenger service is now expected to start in February 2027, subject to independent safety certification and final approvals. We have not listed fares or opening hours because we have no official figure.</p></section>'
            '<section class="rv"><h2>Which house for which route</h2><ul>'
            '<li><a href="{R}stays/prima-taman-nusantara-prima/">Prima</a>: host estimate about 10 minutes from the Tuas Second Link, excluding queues.</li>'
            '<li><a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a>: host estimate about 12 minutes from the Causeway CIQ, excluding queues, and a 5-minute walk to KSL City Mall.</li></ul>'
            '<p>Read more in <a href="{R}articles/causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay/">Causeway, Second Link or RTS: which way to JB</a>.</p>%s</section>'
            '<section class="rv src"><h2>Official sources</h2><ul>%s</ul></section></div></div>'
            % (route_map(True), SRC['ica_traffic'][1], SRC['ica_qr'][1], wa_btn('Ask us about your route', wa_msg(), 'getting-there'), srcs))


def faq_body():
    out, items = [], []
    for g, keys in FAQ_GROUPS:
        f, _ld = faq_block(faqs(*keys), g)
        out.append('<section class="faqg">%s</section>' % f)
        items += faqs(*keys)
    _f, ld = faq_block(items, '')
    PENDING.setdefault('faq/', []).append(ld)
    return ('<div class="wrap body prose"><div class="answer">The 15 questions Singapore groups ask us most, from the SGD price to parking, payment and the crossing. For anything else, WhatsApp Daniel, the host.</div>%s'
            '<p style="margin-top:28px">%s</p><p class="note">Passport and border information comes from <a href="%s" rel="noopener">ICA</a> (checked 8 Nov 2026).</p>%s</div>') % (
        ''.join(out), wa_btn('Ask us on WhatsApp', wa_msg(), 'faq'), SRC['ica_qr'][1], fx_note())


def about_body():
    return ('<div class="wrap body prose"><section class="rv"><h2>JB Airbnb</h2><p>JB Airbnb offers private holiday houses in Johor Bahru for families and groups, many of them travelling from Singapore. Our idea is simple: %s</p>'
            '<p>We have two houses, <a href="{R}stays/prima-taman-nusantara-prima/">Prima</a> in Taman Nusantara Prima, Iskandar Puteri, and <a href="{R}stays/landak-kawan-fun-house-taman-abad/">Landak Kawan Fun House</a> in Taman Abad, Johor Bahru.</p>'
            '<p>Your host is Daniel, based in Singapore and JB. He understands both cultures and speaks English, Malay and Chinese. Ask him anything on WhatsApp at %s. %s</p></section>'
            '<section class="rv"><h2>Addresses</h2><ul>%s</ul>%s</section></div>'
            % (e(TAGLINE.lower()), WA_SHOW, PAY, ''.join('<li><b>%s</b>: %s</li>' % (e(HOUSES[k]['name']), e(HOUSES[k]['addr'])) for k in ORDER),
               wa_btn('Message us', wa_msg(), 'about')))


def contact_body():
    return ('<div class="wrap body prose"><section class="rv"><h2>Message Daniel on WhatsApp</h2><p>WhatsApp Daniel, the host, at <b>%s</b>. Tell him the house, your dates and how many people. %s %s</p>%s'
            '<p style="margin-top:24px">Houses: %s</p></section></div>'
            % (WA_SHOW, PAY, DEPOSIT, wa_btn('Open WhatsApp', wa_msg(), 'contact'),
               ' | '.join('<a href="{R}stays/%s/">%s</a>' % (HOUSES[k]['slug'], e(HOUSES[k]['name'])) for k in ORDER)))


def privacy_body():
    return ('<div class="wrap body prose"><p>Last updated %s.</p><h2>What we collect</h2><p>When you message us on WhatsApp we receive your phone number, name shown on WhatsApp and whatever you write, such as dates and group size.</p>'
            '<h2>How we use it</h2><p>We use it to reply to your enquiry, confirm a booking and manage your stay. We do not sell your personal data.</p>'
            '<h2>Who sees it</h2><p>Messages are handled through WhatsApp, which has its own privacy policy. We share details only with people who help run your stay, or where the law requires.</p>'
            '<h2>Website analytics</h2><p>This website counts taps on contact links (for example WhatsApp) with an anonymous visitor identifier to understand which pages help visitors. It does not store your message.</p>'
            '<h2>Your choices</h2><p>You can ask us on WhatsApp to access, correct or delete your personal data, or to stop contacting you, in line with Malaysia\'s Personal Data Protection Act and Singapore\'s PDPA where they apply.</p>'
            '<p>We keep enquiry messages only as long as needed for the purposes above.</p></div>' % TODAY)


HUB_ANSWER = ('Johor Bahru is in Malaysia, so every guest needs a passport, even for one night. JB Airbnb has two private houses with pool tables: Prima near the Tuas Second Link for up to 12 guests, and Landak near KSL City Mall for up to 10. Prima is ' + tiers_rm('prima') + ', and Landak ' + tiers_rm('landak') + ', per night for the whole house with cleaning included.')


def articles_body():
    P, L = HOUSES['prima'], HOUSES['landak']
    tips = ''.join('<li><b>%s</b> %s%s</li>' % (e(t), e(b), (' <a href="%s" rel="noopener">%s</a>' % (e(u), e(l))) if u else '') for t, b, u, l in AROUND['tips'])
    return ('<div class="wrap body"><div class="prose hub"><div class="answer">%s</div>'
            '<section class="rv"><h2>1. Choose a house</h2><ul>'
            '<li><a href="{R}stays/%s/">Prima</a>, Gelang Patah, Iskandar Puteri: a landed house for up to 12 guests, 3 bedrooms, a 7ft pool table, a mahjong table and parking for 8 cars. The host estimates about 10 minutes from the Tuas Second Link.</li>'
            '<li><a href="{R}stays/%s/">Landak Kawan Fun House</a>, Taman Abad: up to 10 guests, about a 5-minute walk to KSL City Mall and about 12 minutes from the Causeway CIQ (host estimate).</li></ul>'
            '<p><a href="{R}stays/">Compare both houses</a>.</p></section>'
            '<section class="rv"><h2>2. Plan the crossing</h2><p>Check ICA traffic advice before you leave and allow for border queues, especially on Friday evenings, Sunday evenings and long weekends. Read <a href="{R}articles/causeway-second-link-or-rts-which-way-to-jb-for-a-weekend-stay/">Causeway, Second Link or RTS</a> and <a href="{R}getting-there/">getting there from Singapore</a>.</p></section>'
            '<section class="rv"><h2>3. Understand the cost in SGD</h2><p>We quote in RM per night for the whole house, cleaning included. Prima: %s. Landak: %s. On a weekday at full occupancy that is %s per person at Prima (12 guests) or %s at Landak (10 guests). Pay by %s.</p>%s</section>'
            '<section class="rv"><h2>4. First time in JB? 5 tips</h2><ol class="tips">%s</ol><p class="note">Check current official rules before you travel.</p></section>'
            '<section class="rv"><h2>5. Questions Singaporeans ask</h2><p>Payment, cancellation, safety, parking, children and more: read <a href="{R}faq/">all 15 questions and answers</a>.</p></section>'
            '</div><h2 class="hub-h">Guides</h2><div class="arts">%s</div><p class="after-faq">%s</p></div>'
            % (e(HUB_ANSWER), P['slug'], L['slug'], tiers_full('prima'), tiers_full('landak'), PP_WEEKDAY['prima'], PP_WEEKDAY['landak'], PAY_SHORT, fx_note(), tips,
               ''.join(article_card(a) for a in ARTICLES), wa_btn('Ask us on WhatsApp', wa_msg(), 'hub')))


def article_body(a):
    secs = ''.join('<section class="rv"><h2>%s</h2>%s</section>' % (e(h), ''.join('<p>%s</p>' % t for t in ps)) for h, ps in a['sections'])
    hh = HOUSES[a['house']]
    return ('<div class="wrap body prose"><p class="byline">%sBy JB Airbnb, %s</p><div class="answer">%s</div>%s'
            '<section class="rv"><p>See the house: <a href="{R}stays/%s/">%s</a>.</p>%s</section></div>'
            % (ico('cal', 18), TODAY, e(a['answer']), secs, hh['slug'], e(hh['full']), wa_btn('Ask about dates', wa_msg(a.get('wa')), 'article-' + a['slug'][:30])))


# ---------------------------------------------------------------- assemble
def build_pages():
    page('', 'JB Staycation for Singapore Groups, from RM 450 a Night',
         'Plan a JB staycation for Singapore groups: two private houses from RM 450 a night (about S$142), cleaning included, real photos and practical guides.',
         'JB staycation for Singapore groups', '', ld=[org_ld(), {'@context': 'https://schema.org', '@type': 'WebSite', 'name': NAME, 'url': BASE, 'publisher': {'@id': BASE + '#org'}}])
    PAGES['']['body'] = home_body()
    page('stays/', 'JB Homestay with Pool Table: 2 Houses from RM 450', 'Compare two JB homestays with pool tables for up to 10 or 12 guests: weekday, weekend and public holiday prices from RM 450, cleaning included.',
         'JB homestay with pool table: choose your house', stays_body(), [('Home', ''), ('Stays', 'stays/')],
         lede='Two private houses with pool tables. Prima from RM 450 and Landak from RM 550 a night for the whole house, cleaning included.', og=STAYS_IMG['prima'][1], stick='stays',
         ld=[{'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'item': {'@id': BASE + 'stays/%s/#rental' % HOUSES[k]['slug'], 'name': HOUSES[k]['name'], 'url': BASE + 'stays/%s/' % HOUSES[k]['slug']}} for i, k in enumerate(ORDER)]}])
    for k in ORDER:
        h = HOUSES[k]
        path = 'stays/%s/' % h['slug']
        titles = {'prima': ('JB Homestay near Second Link: Prima, 12 Guests, RM 450+', 'Prima: landed JB group homestay near Tuas Second Link for 12 guests, 7ft pool table, parking for 8 cars. RM 450 weekday, RM 650 weekend, RM 750 public holiday.', H1S['prima']),
                  'landak': ('JB Homestay near KSL: Landak for 10 Guests, RM 550+', 'Stay at Landak, a JB homestay near KSL: a 5-minute walk to the mall, games and space for 10. RM 550 weekday, RM 750 weekend, RM 1,000 public holiday.', H1S['landak'])}[k]
        page(path, titles[0], titles[1], titles[2], '', [('Home', ''), ('Stays', 'stays/'), (h['name'], path)], ld=[house_ld(h)],
             og=BENTO[k][0], stick=k, custom_top=True)
        PAGES[path]['body'] = house_body(k)
    page('prices/', 'Prices from RM 450 a Night, Cleaning Included | JB Airbnb', 'JB Airbnb prices per night, cleaning included: Prima RM 450 to 750, Landak RM 550 to 1,000 for weekday, weekend and public holiday. Deposit and payment.',
         'Prices (RM per night)', prices_body(), [('Home', ''), ('Prices', 'prices/')], lede='Per night for the whole house, cleaning included. Prima: ' + tiers_rm('prima') + '. Landak: ' + tiers_rm('landak') + '.', photo=PAGE_IMG['prices'], og=PAGE_IMG['prices'])
    page('getting-there/', 'Getting to JB from Singapore by Road or RTS | JB Airbnb', 'Woodlands, Tuas or the RTS Link to Johor Bahru? Official facts with sources and which JB Airbnb house suits each route.',
         'Getting to our Johor Bahru houses from Singapore', gt_body(), [('Home', ''), ('Getting there', 'getting-there/')],
         lede='Facts below come from official sources, with the date we checked them.', photo=PAGE_IMG['getting-there'], og=PAGE_IMG['getting-there'])
    page('faq/', 'FAQ: Booking a JB Holiday House | JB Airbnb', 'Answers on payment, check-in times, minimum stay, cleaning, gatherings, parking and crossing the border from Singapore to our two JB houses.',
         'Frequently asked questions', faq_body(), [('Home', ''), ('FAQ', 'faq/')], photo=PAGE_IMG['faq'], og=PAGE_IMG['faq'])
    page('about/', 'About JB Airbnb | Johor Bahru Holiday Houses', 'JB Airbnb offers two private holiday houses in Johor Bahru for Singapore families and groups, booked directly on WhatsApp.',
         'About JB Airbnb', about_body(), [('Home', ''), ('About', 'about/')], lede=TAGLINE, photo=PAGE_IMG['about'],
         ld=[org_ld()])
    page('contact/', 'Contact JB Airbnb on WhatsApp', 'Book or ask a question on WhatsApp +65 9006 2198. Tell us the house, dates and group size.',
         'Contact us', contact_body(), [('Home', ''), ('Contact', 'contact/')], lede='WhatsApp is the fastest way to reach us.', photo=PAGE_IMG['contact'], og=PAGE_IMG['contact'])
    page('privacy/', 'Privacy Notice | JB Airbnb', 'How JB Airbnb handles personal data from WhatsApp enquiries and website visits.', 'Privacy notice', privacy_body(), [('Home', ''), ('Privacy', 'privacy/')])
    page('articles/', 'JB Guide for Singaporeans: Houses, Routes & Costs', 'Use this JB guide for Singaporeans to choose a house, plan the crossing and understand RM/SGD costs. Compare Prima and Landak for your group.',
         'JB guide for Singaporeans planning a short getaway', articles_body(), [('Home', ''), ('JB guide', 'articles/')], lede='Houses, the crossing, costs in SGD and first-time tips in one place.')
    for a in ARTICLES:
        path = 'articles/%s/' % a['slug']
        ph = PAGE_IMG[a['slug']]
        page(path, a.get('ttl') or a['title'], a['desc'], a['h1'], article_body(a),
             [('Home', ''), ('JB guide', 'articles/'), (a['title'], path)], photo=ph, article=True, og=ph,
             ld=[{'@context': 'https://schema.org', '@type': 'Article', 'headline': a['title'], 'description': a['desc'], 'datePublished': TODAY, 'dateModified': TODAY,
                  'author': {'@type': 'Organization', 'name': NAME, 'url': BASE}, 'publisher': {'@type': 'Organization', 'name': NAME, 'logo': {'@type': 'ImageObject', 'url': BASE + 'icon-512.png'}},
                  'image': abs_img(ph), 'mainEntityOfPage': BASE + path}])


def copy_images():
    """Copy the used photos into site/img/ (full size, max 1600) and their prepared 800px versions into site/thumb/ (same filename)."""
    global HAS_THUMB
    dst = os.path.join(OUT, 'img')
    tdir = os.path.join(OUT, 'thumb')
    os.makedirs(dst, exist_ok=True)
    os.makedirs(tdir, exist_ok=True)
    files = used_images()
    for f in files:
        shutil.copyfile(os.path.join(SRC_IMG, f), os.path.join(dst, f))
        if os.path.exists(os.path.join(SRC_IMG, f[:-5] + '-800.webp')):
            shutil.copyfile(os.path.join(SRC_IMG, f[:-5] + '-800.webp'), os.path.join(tdir, f))
    for f in HERO_SET.values():
        shutil.copyfile(os.path.join(SRC_IMG, f), os.path.join(dst, f))
    HAS_THUMB = True
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
    nf = ('<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | JB Airbnb</title>'
          '<meta name="robots" content="max-image-preview:large"><link rel="icon" href="%sicon.svg" type="image/svg+xml">%s%s<link rel="stylesheet" href="%sjb.css?v=%s"></head><body class="inner has-stick">%s<main id="main"><div class="wrap nf"><p class="eyebrow">Error 404</p><h1>Page not found</h1><p class="lead">That page does not exist. Try our <a href="%s">home page</a>, the <a href="%sstays/">stays</a> or message us on WhatsApp.</p>%s</div></main>%s%s<script src="%sjb.js?v=%s" defer></script><script src="%scta.js?v=%s" defer></script></body></html>'
          % (BASE, HEAD_JS, FONT_LINKS, BASE, ASSET_V, header_html(), BASE, BASE, wa_btn('WhatsApp us', wa_msg(), '404'), footer_html(), stick_bar('any'), BASE, ASSET_V, BASE, ASSET_V))
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
    ll = ['# JB Airbnb', '', '> %s Private holiday houses in Johor Bahru, Malaysia, for Singapore families and groups. Host: Daniel (based in Singapore and JB; English, Malay and Chinese), WhatsApp %s (%s). Pay by %s.' % (TAGLINE, WA_SHOW, WA_BASE, PAY_SHORT), '', '## Booking terms', '- Prices per night for the whole house, cleaning included. Prima: ' + tiers_full('prima') + '. Landak Kawan Fun House: ' + tiers_full('landak') + '. SGD figures are estimates at RM1 = S$0.3158.', '- ' + DEPOSIT + ' Bank details are shared once a booking and its dates are confirmed.', '- Check-in 3pm, check-out 11am; self check-in details sent after a firm booking; early check-in or late checkout RM 100 an hour, subject to availability (waiver on request).', '- Minimum stay 1 night (2 nights over Christmas Eve and Christmas Day). No cancellation; dates can be changed once.', '- Gatherings need the host\'s approval. Visitors allowed; quiet hours 11pm to 7am. No BBQ, no pets; RM 500 penalty for smoking, vaping or eating durian indoors.', '- Prima has a ground-floor bedroom, so elderly guests do not need the stairs.', '- Professionally cleaned after every checkout; fresh linen, towels and toiletries provided. Fire extinguisher under the kitchen sink; outdoor CCTV; the host is the emergency contact.', '', '## Houses']
    for k in ORDER:
        h = HOUSES[k]
        ll.append('- [%s](%sstays/%s/): %s. Up to %d guests, %s per night, cleaning included. %s' % (h['full'], BASE, h['slug'], h['addr'], h['guests'], tiers_rm(k), h['card']))
    ll += ['', '## Pages', '- [Prices](%sprices/)' % BASE, '- [Getting there from Singapore](%sgetting-there/)' % BASE, '- [FAQ](%sfaq/)' % BASE, '- [About](%sabout/)' % BASE, '- [Contact](%scontact/)' % BASE, '- [Articles](%sarticles/)' % BASE]
    for a in ARTICLES:
        ll.append('  - [%s](%sarticles/%s/)' % (a['title'], BASE, a['slug']))
    open(os.path.join(OUT, 'llms.txt'), 'w').write('\n'.join(ll) + '\n')
    path_prefix = '/' + BASE.split('/', 3)[3]
    open(os.path.join(OUT, 'htaccess.txt'), 'w').write(
        '# Rename to .htaccess in this folder via cPanel. Preview hiding is handled by the server outside the pages.\n'
        'RewriteEngine On\nRewriteCond %{HTTP_HOST} ^www\\.jbairbnb\\.com$ [NC]\nRewriteRule ^ https://jbairbnb.com%{REQUEST_URI} [L,R=301]\nRewriteCond %{HTTPS} !=on\nRewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]\n'
        'DirectoryIndex index.html\nErrorDocument 404 ' + path_prefix + '404.html\n'
        'Redirect 301 ' + path_prefix + 'articles/big-group-staycation-jb-house-for-10-20-people/ ' + BASE + 'articles/jb-homestay-for-big-groups-12-guests/\n'
        '<IfModule mod_headers.c>\n<FilesMatch "\\.(html|xml|txt)$">\nHeader set Cache-Control "public, max-age=3600"\n</FilesMatch>\n'
        '</IfModule>\n')
    # old article URL (renamed 9 Nov 2026 when Prima became 12 guests): the real 301 is in htaccess.txt; this stub covers hosts where it is not active yet
    od = os.path.join(OUT, 'articles', 'big-group-staycation-jb-house-for-10-20-people'); os.makedirs(od, exist_ok=True)
    nu = BASE + 'articles/jb-homestay-for-big-groups-12-guests/'
    open(os.path.join(od, 'index.html'), 'w', encoding='utf-8').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved: JB homestay for big groups</title><link rel="canonical" href="%s"><meta http-equiv="refresh" content="0;url=%s"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><p>This guide has moved: <a href="%s">JB homestay for big groups</a>.</p><script>location.replace(%s)</script></body></html>' % (nu, nu, nu, json.dumps(nu)))
    print('pages:', len(PAGES) + 1, 'images:', n_img, 'thumbs:', HAS_THUMB, 'built into', OUT)


if __name__ == '__main__':
    main()

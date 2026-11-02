"""CSKA Auto Enterprise: builds every page into site/ (python3 build.py).

New client from Edwin, 19 Oct 2026. B2B: CSKA supplies car workshops in Singapore with diagnostic tools and workshop equipment.
Facts used, and where they came from (all checked 19 Oct 2026):
- Name cards Edwin sent: CSKA Auto Enterprise Pte. Ltd., 101 Woodlands Ave 12, #07-03B (Polaris@Woodland) Singapore 737719,
  cskatrading20@gmail.com; Steven Chai, Business Development Manager, (65) 9822 2629; Kai Kiat (Ah Kiat), Sale Executive, (65) 8493 0068.
- Edwin: technical contact Ah Yii 9037 2820; their customers are car workshops; they are an authorised distributor of a few automotive products.
- Their own video name card: Alvis Kiew (Ah Yii), Technical Executive, (65) 9037 2820 (an older card in the same videos shows a
  previous address, 61 Woodlands Industrial Park E9 #01-20; not used).
- ACRA via data.gov.sg + opengovsg: UEN 202127592M, incorporated 7 Aug 2021, live exempt private company, registered at
  101 Woodlands Avenue 12 #07-03B S737719; SSIC 46599 wholesale of other machinery and equipment, 46563 wholesale of vehicle parts
  and accessories; activity "VEHICLES PRODUCTS/TOOLS/EQUIPMENTS".
- Facebook (read logged out in the Base44 sandbox): Steven's profile facebook.com/chai.steven.393 ("Manager at CSKA", 1.6K followers)
  and Ah Kiat's facebook.com/kiat.ah.712675, about 180 reels between them, mostly handover videos "Thanks <workshop> Trust & Support"
  naming the product. Their brand card video lists THINKCAR, AUTEL, TOPDON, SP (SP ZONE), STIRLING, ThreeBond, Ingersoll Rand and
  one more German lubricant brand (logo unclear, not used). Product facts on the site come only from those posts (which repeat the
  makers' own descriptions). Instagram @chai8552 is Steven's (80 followers, 88 posts).
- Photos: frames from their own handover videos, hosted on jsDelivr (site-assets/cska-auto, commit 2f91c78).
Not claimed anywhere: prices, opening hours, which brands they hold an authorised distributorship for (CONFIRM), the
  "Top Dealer Award" from Speed Car Auto Parts (no date), customer workshop names (CONFIRM), warranty beyond what a maker states.
"""
import html
import json
import os
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('CS_OUT', os.path.join(HERE, 'site'))

SLUG = 'cska-auto'
DOMAIN = 'cskatrading.com'  # live since 19 Oct 2026 (domain added by Edwin; Controller shows the site live)
LIVE = True  # cskatrading.com is live (19 Oct 2026); a LIVE=False build writes preview canonicals: never upload one
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
# Hidden from Google by the X-Robots-Tag header in pageonesingapore.com/preview/.htaccess, never a meta tag (Edwin, 17 Oct 2026).
IMG = os.environ.get('CS_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@2f91c78/site-assets/cska-auto/')
IMG_ABS = IMG if IMG.startswith('http') else None
UPDATED = '2026-10-19'
UPDATED_TEXT = '19 October 2026'
LLMS_UPDATED_TEXT = '2 November 2026'  # llms.txt footer only (25 Oct: authorised-distributor wording removed, Booster sections added)

NAME = 'CSKA Auto Enterprise'
LEGAL, UEN, FOUNDED = 'CSKA Auto Enterprise Pte. Ltd.', '202127592M', '2021-08-07'
WA_NUM, WA_SHOW = '6598222629', '9822 2629'
TEL = '+6598222629'
EMAIL = 'cskatrading20@gmail.com'
WA_MSG = 'Hi CSKA, I found your website. I would like to ask about '
STREET, UNIT, BUILDING, POSTAL = '101 Woodlands Avenue 12', '#07-03B', 'Polaris @ Woodlands', '737719'
ADDR = ['101 Woodlands Ave 12, #07-03B', 'Polaris @ Woodlands', 'Singapore 737719']
MAPQ = quote('101 Woodlands Avenue 12 #07-03B Singapore 737719')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
# CSKA's own Google Business Profile (Edwin, 20 Oct 2026: rated 5 stars). No review count or AggregateRating schema:
# our servers can't read Google pages, and third-party reviews are never marked up as our own (MASTER-RULES 4.5).
GBP = 'https://maps.google.com/?cid=4280054029158527073'
GBP_LINE = '<a class="grating" href="%s" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">★★★★★</span> Rated 5.0 on Google · Read our reviews</a>' % GBP
FB_STEVEN = 'https://www.facebook.com/chai.steven.393'
FB_KIAT = 'https://www.facebook.com/kiat.ah.712675'
IG_STEVEN = 'https://www.instagram.com/chai8552/'

PEOPLE = [
    ('Steven Chai', 'Business Development Manager', '6598222629', '9822 2629', 'Quotes, brands and new workshop set-ups'),
    ('Kai Kiat (Ah Kiat)', 'Sales Executive', '6584930068', '8493 0068', 'Orders and product questions (English, 中文)'),
    ('Alvis Kiew (Ah Yii)', 'Technical Executive', '6590372820', '9037 2820', 'Technical questions and help using your tool'),
]

CONFIRM = [
    'Which brands CSKA holds an authorised distributorship for in Singapore (THINKCAR? SP ZONE? others?), so each brand page can say so',
    'Opening hours, and whether workshops can visit the Polaris @ Woodlands office to see tools (showroom or office only?)',
    'Domain to use (nothing registered yet; cskaauto.com.sg is a placeholder)',
    'May we name the workshops in the handover photos (e.g. "THINKTOOL 191 at <workshop>")? Names are left out for now',
    'The Top Dealer Award from Speed Car Auto Parts (SP ZONE): which year, so it can be shown with a date',
    'The German lubricant brand on the brand card (logo reads like "ARZOIL"): exact name',
    'Do you also do TPMS sensor programming or ADAS calibration as a service, or only sell the tools? (videos show TPMS jobs)',
    'Training, delivery, installation (lifts, aircon machines) and after-sales: what is included with a purchase',
    'Warranty you give on top of the makers\' warranty, and who handles repairs',
    'Is there a CSKA Facebook business page, TikTok or Xiaohongshu? (only Steven\'s and Ah Kiat\'s profiles found)',
    'Any price list or promotions you are happy to publish',
]

NAV = [('products/', 'Products'), ('brands/', 'Brands'), ('handovers/', 'Handovers'), ('articles/', 'Guides'), ('about/', 'About'), ('contact/', 'Contact')]
E = html.escape

PHOTOS = {  # name: (width, height, alt)
    'handover-ms908s-ii': (720, 960, 'CSKA handing over an Autel MaxiSys diagnostic tablet and case at a workshop with a two-post lift'),
    'handover-ms908s-ii-b': (720, 960, 'Autel MaxiSys tablet handover in front of a workshop, Singapore'),
    'handover-ms908s-ii-c': (720, 845, 'Autel MaxiSys tablet handover at a tyre and service workshop'),
    'handover-ms908s-ii-d': (720, 845, 'Autel MaxiSys tablet and case handed over beside a customer car'),
    'handover-ms908s-ii-e': (720, 960, 'Autel MaxiSys handover at a motor works workshop'),
    'handover-ms908s-ii-f': (720, 617, 'Autel MaxiSys handover outside an autoworks workshop'),
    'handover-ms908s3': (576, 768, 'Autel MaxiSys MS908S3 handover in a busy workshop'),
    'ms908s3-screen': (540, 960, 'Autel MaxiSys MS908S3 screen showing the service functions menu'),
    'handover-thinktool-191': (720, 960, 'THINKCAR THINKTOOL 191 diagnostic tool handover at a Singapore workshop'),
    'handover-thinktool-191-b': (720, 960, 'THINKTOOL 191 handover inside an auto parts and service shop'),
    'handover-thinktool-191-c': (720, 960, 'THINKTOOL 191 handover at an automotive services workshop'),
    'handover-thinktool-191-d': (720, 960, 'THINKCAR scanner handover at a battery and tyre shop'),
    'handover-sg-garage': (540, 768, 'THINKTOOL 191 handover at Edwin Garage, Singapore'),
    'handover-expert-391': (720, 960, 'THINKTOOL Expert 391 tablet handover at a car service centre'),
    'thinktool-391-box': (540, 960, 'THINKTOOL Expert 391 tablet and its box'),
    'handover-expert-394-ev': (720, 960, 'THINKCAR Expert 394 EV diagnostic scanner handover in a workshop'),
    'handover-master-x2': (540, 960, 'THINKTOOL Master X2 handover in a workshop with two-post lifts'),
    'handover-master-2': (480, 852, 'THINKTOOL Master 2 handover at a workshop with lifts'),
    'master-2-in-use': (540, 960, 'Technician setting up a THINKTOOL Master diagnostic tablet'),
    'handover-thinktool-se': (540, 960, 'THINKTOOL SE diagnostic tool handover in a workshop'),
    'thinktool-se-tablet': (720, 960, 'THINKTOOL SE tablet in hand showing a diagnostic menu'),
    'handover-thinktool-se-trolley': (720, 960, 'THINKTOOL SE handed over with a seven-drawer tool cart'),
    'handover-lite-2': (720, 960, 'THINKTOOL Lite 2 handover outside a tyre and battery shop'),
    'handover-phoenix-elite': (720, 960, 'TOPDON Phoenix Elite diagnostic tool handover in a workshop'),
    'handover-ts508wf': (720, 960, 'Autel MaxiTPMS TS508WF TPMS tool handover at a tyre shop'),
    'handover-ts508wf-b': (640, 856, 'Autel MaxiTPMS TS508WF handover at a tyre specialist'),
    'maxitpms-screen': (720, 404, 'Autel MaxiTPMS tool screen during TPMS sensor programming'),
    'tyre-tread-examiner': (640, 856, 'Laser tyre tread and brake disc wear examiner being tried at a tyre shop'),
    'handover-v4500': (720, 960, 'TOPDON V4500 Plus jump starter handover at a transmission workshop'),
    'handover-v4500-b': (720, 960, 'TOPDON V4500 Plus jump starter handover outside a motor workshop'),
    'thinkcar-trolley-thinkpps': (540, 960, 'THINKCAR diagnostic trolley with THINKPPS 150 power supply being set up'),
    'handover-aircon-machine': (720, 960, 'SP ZONE aircon refrigerant flushing and recovery machine handed over in a workshop'),
    'handover-aircon-machine-b': (720, 960, 'SP ZONE aircon flushing and recovery machine at a workshop entrance'),
    'aircon-machine-demo': (540, 960, 'Technicians learning the SP ZONE aircon machine control panel'),
    'aircon-machine-steven': (543, 960, 'Steven Chai of CSKA with an SP ZONE aircon flushing and recovery machine'),
    'aircon-machine-team': (720, 960, 'Workshop team gathered for an SP ZONE aircon machine handover'),
    'spz6000-in-use': (720, 960, 'SP ZONE SPZ6000 aircon machine connected in a tyre workshop'),
    'spz6000-training': (720, 748, 'CSKA showing a technician how to run the SP ZONE SPZ6000'),
    'pld-212-smoke-test': (540, 960, 'THINKCAR PLD 212 smoke leak detector in use under a car bonnet'),
    'tfj-330-jack': (585, 960, 'THINKCAR TFJ 330 dual pump low-profile jack in a workshop bay'),
    'handover-tool-trolley': (720, 960, 'Seven-drawer tool trolley with a 376-piece tool set delivered to a workshop'),
    'handover-ingersoll-rand': (720, 960, 'Ingersoll Rand 3/4-inch air impact wrench handover at a workshop'),
}


def img(name, cls='', eager=False):
    w, h, alt = PHOTOS[name]
    return '<img src="%s%s.webp" alt="%s" width="%d" height="%d"%s%s>' % (
        IMG, name, E(alt), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', ' class="%s"' % cls if cls else '')


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')


def wa_url(topic='tools for my workshop.', num=WA_NUM):
    return 'https://wa.me/%s?text=%s' % (num, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp Steven', topic='tools for my workshop.', cls='btn btn-wa', num=WA_NUM):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic, num)), WA_SVG, E(label))


def brand_html(pre):
    src = '%slogo.webp' % (IMG if IMG_ABS else pre + IMG)
    return ('<a class="brand" href="%s" aria-label="%s, home page"><img class="brand-mark" src="%s" alt="CSKA logo" width="75" height="42">'
            '<span><span class="brand-name">Auto Enterprise</span><span class="brand-sub">Workshop tools &amp; equipment, Singapore</span></span></a>') % (pre or './', NAME, src)


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, photo=None):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [], hero=hero, cta=cta, photo=photo)


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def table_html(headers, rows, caption=''):
    """Comparison table (MASTER-RULES 3.3). First column is a row header so .cmp td:first-child styling does not mute it."""
    th = ''.join('<th scope="col" style="text-align:left;padding:11px 10px;border-bottom:2px solid var(--line)">%s</th>' % E(h) for h in headers)
    body = ''.join('<tr><th scope="row" style="text-align:left;padding:11px 10px;border-bottom:1px solid var(--line);vertical-align:top">%s</th>%s</tr>' % (
        E(r[0]), ''.join('<td>%s</td>' % E(c) for c in r[1:])) for r in rows)
    cap = '<caption class="small" style="text-align:left;padding:0 0 8px">%s</caption>' % E(caption) if caption else ''
    return '<div style="overflow-x:auto;margin:0 0 1em"><table class="cmp">%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cap, th, body)


def ticks(items):
    return '<ul class="ticks">%s</ul>' % ''.join('<li><b>%s</b> %s</li>' % (E(a), E(b)) for a, b in items)


def steps(items):
    return '<ol class="numbered">%s</ol>' % ''.join('<li><b>%s.</b> %s</li>' % (E(a), E(b)) for a, b in items)


def models_html(items):
    return '<div class="models">%s</div>' % ''.join('<div class="model"><span class="tag">%s</span><b>%s</b><p>%s</p></div>' % (E(t), E(n), E(d)) for t, n, d in items)


def glide(names, cls='glide', captions=None):
    out = []
    for i, n in enumerate(names):
        cap = captions[i] if captions else ''
        out.append('<figure class="gl-item">%s%s</figure>' % (img(n), '<figcaption>%s</figcaption>' % E(cap) if cap else ''))
    return '<div class="%s" role="region" aria-label="Handover photos">%s</div>' % (cls, ''.join(out))


# ----------------------------------------------------------------------------------------------
# Products (one page per product line). Model notes come only from CSKA's own posts, which quote the makers.
# ----------------------------------------------------------------------------------------------
PRODUCTS = [
    dict(slug='diagnostic-scanners', short='Diagnostic scanners', photo='handover-ms908s-ii',
         title='Car Diagnostic Scanners for Workshops | CSKA Singapore',
         desc='THINKCAR THINKTOOL, Autel MaxiSys and TOPDON Phoenix diagnostic scanners for Singapore workshops: full system scan, coding, programming.',
         h1='Car diagnostic scanners',
         gist='THINKCAR THINKTOOL, Autel MaxiSys and TOPDON scan tools, from 7-inch scanners to online-programming tablets.',
         lede='Scan tools for every kind of workshop, from a first full-system scanner to tablets that code and program modules.',
         answer='CSKA Auto Enterprise supplies car diagnostic scanners to workshops in Singapore: THINKCAR THINKTOOL models (Lite 2, T77, SE, 191, Master 2, Master X, Master X2, Expert 391), Autel MaxiSys tablets (MS908S II, MS908S3, MS909, MS909 S2) and the TOPDON Phoenix Elite. WhatsApp Steven on 9822 2629 with the cars you service and we will suggest a model.',
         gallery=['handover-ms908s-ii', 'handover-thinktool-191', 'handover-expert-391', 'handover-master-x2', 'thinktool-se-tablet', 'handover-ms908s3', 'handover-phoenix-elite', 'handover-lite-2', 'handover-sg-garage'],
         models=[('THINKCAR', 'THINKTOOL Lite 2', '7-inch full-function scanner. DoIP, CAN FD and OBDII/EOBD from 1996, with maintenance resets, special functions and coding.'),
                 ('THINKCAR', 'THINKTOOL T77', '7-inch plug-and-play full-function scanner with DoIP and CAN FD support.'),
                 ('THINKCAR', 'THINKTOOL SE', '8-inch, Android 10, 64 GB. Up to 34 service resets, bi-directional control, 220+ vehicle brands.'),
                 ('THINKCAR', 'THINKTOOL 191', 'Full system scan, advanced coding, bi-directional control and special functions. Takes THINKCAR add-on modules.'),
                 ('THINKCAR', 'THINKTOOL Master 2', 'Wireless OE-level diagnosis: full vehicle scan, live data, actuation tests and maintenance resets.'),
                 ('THINKCAR', 'THINKTOOL Master X', '220 car makes, 12V and 24V: passenger, commercial, hybrid and heavy-duty vehicles. 35 maintenance resets.'),
                 ('THINKCAR', 'THINKTOOL Master X2', '10.1-inch, 128 GB, J2534, DoIP, D-PDU and CAN FD, video remote diagnosis and a built-in TPMS module.'),
                 ('THINKCAR', 'THINKTOOL Expert 391', '10.1-inch with online programming. 120+ passenger brands, 70+ EV brands with the EV package, 150+ heavy-duty with HML.'),
                 ('Autel', 'MaxiSys MS908S II', '9.7-inch, Android 10, 128 GB, Bluetooth VCI. Codes on all systems, active tests, live data and adaptations.'),
                 ('Autel', 'MaxiSys MS908S3', '10.1-inch, Android 10, DoIP and CAN FD, Auto Scan 2.0 and 40+ service functions.'),
                 ('Autel', 'MaxiSYS MS909', '9.7-inch, 128 GB, VCI with DoIP, D-PDU and J2534, and topology module mapping.'),
                 ('Autel', 'MaxiSYS MS909 S2', '11-inch, Android 13, 256 GB, MaxiFLASH VCI2 with J2534 pass-thru, Topology 3.0, 45+ service functions.'),
                 ('TOPDON', 'Phoenix Elite', 'Wireless VCI with CAN FD, topology mapping, guided VW and Audi functions, pre-scan and post-scan reports.')],
         extra='<h2>Which car diagnostic tool does a Singapore workshop need?</h2>'
               '<p class="answer">A workshop needs a full-system diagnostic scanner, not a consumer OBD2 code reader: it must read every module, show live data, run bi-directional tests and service resets and, for newer cars, support DoIP and CAN FD. Workshops that program modules add J2534 pass-thru. CSKA stocks THINKCAR, Autel and TOPDON models at each of these levels.</p>'
               + table_html(['Model', 'Screen and storage', 'Protocols and programming', 'Best for'], [
                   ('THINKTOOL Lite 2 / T77', '7-inch', 'DoIP, CAN FD; OBDII/EOBD from 1996 (Lite 2); maintenance resets, special functions, coding', 'A first full-function scanner for a small workshop'),
                   ('THINKTOOL SE', '8-inch, Android 10, 64 GB', 'Up to 34 service resets, bi-directional control, 220+ vehicle brands', 'General servicing and repairs'),
                   ('THINKTOOL 191', 'Tablet', 'Full system scan, advanced coding, bi-directional control, special functions; takes THINKCAR add-on modules', 'Coding work, with a TPMS programmer added later'),
                   ('THINKTOOL Master X2', '10.1-inch, 128 GB', 'J2534, DoIP, D-PDU, CAN FD; 12V and 24V; built-in TPMS module; video remote diagnosis', 'Cars plus commercial vehicles and trucks'),
                   ('THINKTOOL Expert 391', '10.1-inch', 'Online programming; 120+ passenger brands, 70+ EV brands with the EV package, 150+ heavy-duty with HML', 'Programming and EV work'),
                   ('Autel MaxiSys MS908S II', '9.7-inch, Android 10, 128 GB', 'Bluetooth VCI; codes on all systems, active tests, live data, adaptations', 'Autel-level diagnostics on a budget tablet'),
                   ('Autel MaxiSys MS908S3', '10.1-inch, Android 10', 'DoIP and CAN FD; Auto Scan 2.0; 40+ service functions', 'Newer cars that need DoIP and CAN FD'),
                   ('Autel MaxiSYS MS909', '9.7-inch, 128 GB', 'VCI with DoIP, D-PDU and J2534; topology module mapping', 'J2534 programming'),
                   ('Autel MaxiSYS MS909 S2', '11-inch, Android 13, 256 GB', 'MaxiFLASH VCI2 with J2534 pass-thru; Topology 3.0; 45+ service functions; ADAS upgrade available', 'The flagship: programming, topology and ADAS'),
                   ('TOPDON Phoenix Elite', 'Tablet with wireless VCI', 'CAN FD; topology mapping; guided VW and Audi functions; pre-scan and post-scan reports', 'Workshops that want printed before/after reports'),
               ], caption='Specifications are the makers\' own, as posted by CSKA. Screen sizes and storage are listed only where the maker states them.')
               + '<p>Not sure which level you need? <a href="articles/choosing-a-diagnostic-scanner-for-your-workshop/">How to choose a diagnostic scanner for a car workshop</a> walks through coverage, bi-directional tests, coding, programming and updates.</p>',
         faqs=[('What is a car diagnostic tool?', 'A car diagnostic tool, or scan tool, is a device that plugs into the vehicle\'s OBD port to read fault codes, live data and module information, and to run tests, service resets, coding and, on higher models, ECU programming. A consumer OBD2 code reader reads and clears engine codes only; a workshop scanner covers every module.'),
               ('Which diagnostic scanner should a small workshop start with?', 'A full-system scanner such as the THINKTOOL Lite 2, T77 or SE reads and clears codes on every system, shows live data and runs common maintenance resets. Workshops that code or program modules usually move up to a THINKTOOL 191, Master X2, Expert 391 or an Autel MaxiSys tablet.'),
               ('Do you sell scanners that support J2534 programming?', 'Yes. The Autel MaxiSYS MS909 and MS909 S2 come with a J2534 pass-thru VCI, and the THINKTOOL Master X2 and Expert 391 support J2534 too. Ask us which suits the makes you program.'),
               ('Do you have scanners for 24V trucks?', 'Yes. The THINKTOOL Master X and Master X2 cover 12V and 24V vehicles, and THINKCAR\'s HML package adds heavy-duty coverage to the Expert 391.'),
               ('Can I see a scanner before I buy?', 'WhatsApp Steven on 9822 2629 or Ah Kiat on 8493 0068 to arrange a demo of the model you are looking at.')]),
    dict(slug='ev-diagnostic-tools', short='EV diagnostic tools', photo='handover-expert-394-ev',
         title='EV Diagnostic Tools and Battery Lifts | CSKA Singapore',
         desc='EV scan tools for Singapore workshops: THINKCAR Expert 394 EV, Autel MaxiSYS Ultra EV and MS909 S2 EV, plus the EVP501 EV battery lift.',
         h1='EV diagnostic tools',
         gist='Scan tools that read EV high-voltage systems and battery health, and a lift for EV battery packs.',
         lede='More electric cars are coming into Singapore workshops. These tools read their high-voltage systems and battery packs.',
         answer='For electric cars, CSKA supplies the THINKCAR Expert 394 EV, the Autel MaxiSYS Ultra EV and the Autel MS909 S2 EV, which read high-voltage systems and show battery State of Charge and State of Health on supported cars. For battery pack work we also supply the EVP501 lift, rated to 1,500 kg.',
         gallery=['handover-expert-394-ev', 'handover-ms908s-ii-d', 'thinktool-391-box', 'handover-expert-391'],
         models=[('THINKCAR', 'Expert 394 EV', '12-inch AI-assisted scanner on the TCOS system: full-system diagnostics with topology and Auto VIN, online ECU programming, 48 special resets, split screen.'),
                 ('Autel', 'MaxiSYS Ultra EV', 'EV high-voltage system analysis with diagrams and step-by-step disassembly guides, State of Charge and State of Health, battery pack testing via OBD or direct cables.'),
                 ('Autel', 'MaxiSYS MS909 S2 EV', 'The MS909 S2 tablet with EV functions; our team has used it to check Tesla battery status.'),
                 ('THINKCAR', 'Expert 391 with EV package', 'Adds 70+ EV brands to the Expert 391 tablet.'),
                 ('Lift', 'EVP501 EV battery lift', 'For battery pack removal and support. Electric raise and lower, mechanical safety lock, up to 1,500 kg and 1,785 mm lift height.')],
         extra='<h2>Which EV diagnostic tool does a Singapore workshop need?</h2>'
               '<p class="answer">A workshop that starts with electric cars needs a scan tool that reads the high-voltage system and shows the battery State of Charge and State of Health, and a lift made for battery packs only if it removes them. CSKA supplies the THINKCAR Expert 394 EV, the Autel MaxiSYS Ultra EV and the Autel MS909 S2 EV for diagnostics, and the EVP501 lift (up to 1,500 kg) for pack work. Tell us the EV brands you service and we compare the tools for you.</p>'
               + table_html(['Your workshop', 'Tool to ask about', 'Why'], [
                   ('Adds EV checks to a general repair business', 'THINKCAR Expert 394 EV', '12-inch tablet with full-system diagnostics, topology, online ECU programming and 48 special resets'),
                   ('Wants EV high-voltage analysis and pack testing', 'Autel MaxiSYS Ultra EV', 'High-voltage system analysis with diagrams and disassembly guides, State of Charge and State of Health, pack testing via OBD or direct cables'),
                   ('Already uses an Autel MS909 S2 and wants EV functions', 'Autel MaxiSYS MS909 S2 EV', 'Our team has used it to check Tesla battery status'),
                   ('Owns a THINKCAR Expert 391', 'Expert 391 with EV package', 'Adds 70+ EV brands to the tablet you already have'),
                   ('Removes or supports EV battery packs', 'EVP501 EV battery lift', 'Electric raise and lower, mechanical safety lock, up to 1,500 kg and 1,785 mm lift height'),
               ], caption='A starting list, not a quote. Ask CSKA to confirm which cars each tool supports before you buy.')
               + '<p>Want to see what a battery-health reading means? Read <a href="articles/checking-ev-battery-health/">Checking EV battery health in a workshop</a>.</p>',
         faqs=[('Can a scan tool check an EV battery\'s health?', 'On supported cars, EV-capable tools such as the Autel MaxiSYS Ultra EV show the high-voltage battery\'s State of Charge and State of Health, and the Ultra EV can also test the pack directly with its cables.'),
               ('Which EV tool is right for my workshop?', 'It depends on the EV brands you see and whether you remove battery packs. Tell us the cars you service on WhatsApp and we will compare the Expert 394 EV, Ultra EV and MS909 S2 EV for you.'),
               ('Do you supply equipment to lift EV battery packs?', 'Yes, the EVP501 lift is made for EV battery replacement and maintenance, lifting up to 1,500 kg to a height of 1,785 mm.'),
               ('Do I need a special scan tool for electric cars?', 'A normal OBD reader cannot analyse the high-voltage system. EV-capable tools such as the Expert 394 EV, Ultra EV and MS909 S2 EV are made for it. Which one fits depends on the EV brands you service.'),
               ('What should I tell CSKA before choosing an EV tool?', 'The EV brands you service, whether you remove battery packs, and the scan tool you already use. WhatsApp Steven on 9822 2629 or Ah Kiat on 8493 0068.')]),
    dict(slug='tpms-and-tyre-tools', short='TPMS and tyre tools', photo='handover-ts508wf',
         title='TPMS Tools for Tyre Shops | Autel MaxiTPMS | CSKA Singapore',
         desc='Autel MaxiTPMS TS508WF, THINKCAR scanners with TPMS modules and a laser tyre tread examiner for tyre shops and workshops in Singapore.',
         h1='TPMS and tyre shop tools',
         gist='Autel MaxiTPMS tools to activate, program and relearn sensors, and a laser tyre tread examiner.',
         lede='Tools for tyre shops: TPMS sensor work and quick tyre and brake disc checks.',
         answer='CSKA supplies the Autel MaxiTPMS TS508WF to tyre shops and workshops in Singapore. It activates TPMS sensors, reads sensor status, checks the TPMS system, programs Autel MX-sensors and runs relearns, with updates over Wi-Fi. THINKCAR scanners such as the Master X2 also include a TPMS module.',
         gallery=['handover-ts508wf', 'handover-ts508wf-b', 'maxitpms-screen', 'tyre-tread-examiner', 'handover-lite-2'],
         models=[('Autel', 'MaxiTPMS TS508WF', 'Activates TPMS sensors, reads sensor status, checks system health, programs MX-sensors and runs relearns. Quick and Advanced modes, Wi-Fi updates.'),
                 ('THINKCAR', 'THINKTOOL Master X2', 'Its built-in TPMS module activates, programs and relearns sensors.'),
                 ('THINKCAR', 'THINKTOOL 191 + TPMS programmer', 'The 191 takes THINKCAR\'s TPMS programmer as an add-on module.'),
                 ('Tyre check', 'Laser tyre tread and brake disc examiner', 'Reads tread and disc wear without removing the tyre, with a colour display, cameras to record damage and a QR report.')],
         extra='<h2>Which TPMS tool does a Singapore tyre shop need?</h2>'
               '<p class="answer">It depends on whether you only do tyres or the whole car. A tyre shop that mainly activates, programs and relearns sensors can start with the Autel MaxiTPMS TS508WF, a dedicated TPMS tool. A workshop that already scans cars can choose a THINKCAR scanner with TPMS built in (Master X2) or add the TPMS programmer to the THINKTOOL 191. For quick tread and brake disc checks at the counter, add the laser tyre tread examiner. CSKA supplies all of them in Singapore.</p>'
               + table_html(['Tool', 'What it is', 'TPMS jobs it covers', 'Best for'], [
                   ('Autel MaxiTPMS TS508WF', 'Dedicated TPMS tool', 'Activates sensors, reads sensor status, checks system health, programs Autel MX-sensors, runs relearns; Quick and Advanced modes; Wi-Fi updates', 'Tyre shops that do TPMS every day'),
                   ('THINKTOOL Master X2', 'Full diagnostic tablet', 'Built-in TPMS module to activate, program and relearn sensors, on top of full-system diagnostics', 'Workshops that want one tablet for scanning and TPMS'),
                   ('THINKTOOL 191 + TPMS programmer', 'Scanner with add-on module', 'The 191 takes THINKCAR\'s TPMS programmer as an add-on module', 'Workshops that already own, or plan to own, a 191'),
                   ('Laser tyre tread and brake disc examiner', 'Tyre check tool', 'Not a TPMS tool: reads tread and disc wear without removing the tyre and shares a QR report', 'A quick customer check at the counter'),
               ], caption='Descriptions are the makers\' own, as posted by CSKA. Ask us to confirm current versions and what comes in the box.')
               + '<p>New to TPMS work? Read <a href="articles/tpms-activate-program-relearn-explained/">TPMS sensor programming: activate, program and relearn explained</a>.</p>',
         faqs=[('What does a TPMS tool do?', 'It wakes up each tyre pressure sensor to read its ID, pressure and battery, programs replacement sensors, and runs the relearn so the car recognises the new sensor.'),
               ('Do you have a TPMS tool that programs sensors?', 'Yes. The Autel MaxiTPMS TS508WF programs Autel MX-sensors, and the THINKTOOL Master X2 has a TPMS module that programs and relearns sensors.'),
               ('Is there a quick way to check tread depth for customers?', 'The laser tyre tread and brake disc examiner reads wear without taking the wheel off and shares a report by QR code. Ask us for a demo.'),
               ('Can one tool activate, program and relearn?', 'Yes. The Autel MaxiTPMS TS508WF and the TPMS module in the THINKTOOL Master X2 both activate sensors, program them and run the relearn, so the car recognises the new sensor.'),
               ('Does CSKA deliver TPMS tools to the workshop?', 'Yes. Each tool is delivered to your workshop and handed over in person.')]),
    dict(slug='adas-calibration', short='ADAS calibration', photo='handover-ms908s-ii-c',
         title='Autel ADAS Calibration Equipment | CSKA Singapore',
         desc='Autel MaxiSys ADAS complete calibration package for Singapore workshops: calibration frame, LDW, AVM, RCW, BSD and NV kits with ADAS software.',
         h1='ADAS calibration equipment',
         gist='The Autel MaxiSys ADAS calibration package: frame, targets and software for camera and radar systems.',
         lede='After a windscreen, bumper or alignment job, driver-assistance cameras and radars often need calibrating.',
         answer='CSKA supplies the Autel MaxiSys ADAS Complete Calibration Package to Singapore workshops. It includes the standard calibration frame, the LDW calibration package, the AVM-RCW-BSD-NV calibration kit, ADAS software and the Autel MS908P complete set. The Autel MS909 S2 can also be upgraded for ADAS calibration.',
         gallery=['handover-ms908s-ii-c', 'handover-ms908s-ii-e', 'handover-ms908s-ii-f', 'ms908s3-screen'],
         models=[('Autel', 'MaxiSys ADAS Complete Calibration Package', 'Standard frame calibration package, LDW calibration package, AVM-RCW-BSD-NV calibration kit, ADAS software and the MS908P complete set.'),
                 ('Autel', 'MaxiSYS MS909 S2 ADAS upgrade', 'The MS909 S2 can be made ADAS calibration-capable with a software upgrade and the ADAS target package.')],
         extra='<h2>What does a Singapore workshop need to calibrate ADAS in-house?</h2>'
               '<p class="answer">A workshop that calibrates ADAS cameras and radars in-house needs four things: a level, well-lit bay, a calibration frame with the right targets, calibration software for the car brands it services, and the carmaker\'s procedure for each car. The Autel package CSKA supplies covers the frame, targets and software side; the bay and the procedure are yours to confirm for each job.</p>'
               + table_html(['What you need', 'Why it matters', 'In the CSKA Autel package'], [
                   ('Calibration frame', 'Holds the targets at the distances the carmaker\'s procedure sets', 'Standard calibration frame'),
                   ('Forward camera targets', 'The camera behind the windscreen is the one most often recalibrated after glass work', 'LDW calibration package'),
                   ('Other systems', 'Surround view, rear radar, blind spot and night vision each use their own targets', 'AVM-RCW-BSD-NV calibration kit'),
                   ('Software and tablet', 'Guides each calibration and must match the brands you service', 'ADAS software and the MS908P complete set; the MS909 S2 can be upgraded'),
               ], caption='A checklist, not a quote. Ask CSKA which car brands and systems you want to cover, and confirm what is in the box.')
               + '<p>Not sure what a calibration job involves? Read <a href="articles/adas-calibration-after-windscreen-replacement/">ADAS calibration after a windscreen replacement: what the workshop needs</a>.</p>',
         faqs=[('What is ADAS calibration?', 'It is re-aiming the cameras and radars behind lane departure warning, blind spot detection, surround view and similar systems so they read the road correctly, usually after windscreen, bumper or suspension work.'),
               ('What comes in the Autel ADAS package?', 'The standard calibration frame, the LDW calibration package, the AVM-RCW-BSD-NV calibration kit, ADAS software and the Autel MS908P complete set.'),
               ('Can I start with my existing Autel tablet?', 'The MS909 S2 can be upgraded for ADAS with software and the target package. WhatsApp us your tablet model and we will tell you what you need.'),
               ('What space does static ADAS calibration need?', 'A level, evenly lit area large enough to place the frame and measure the distances in the carmaker\'s procedure. Tell us your bay size and the cars you service, and check each procedure before you quote a job.'),
               ('Which car brands and systems can I calibrate with the package?', 'The package includes lane departure warning targets and an AVM-RCW-BSD-NV kit for surround view, rear radar, blind spot and night vision. Tell us the brands and systems you service and we will confirm what you need.')]),
    dict(slug='aircon-service-machines', short='Aircon service machines', photo='handover-aircon-machine',
         title='Car Aircon Flushing and Recovery Machines | SP ZONE | CSKA',
         desc='SP ZONE SPZ-FA1 and SPZ6000 all-in-one car aircon refrigerant recovery, recycling, flushing, vacuum and oil injection machines, Singapore.',
         h1='Car aircon service machines',
         gist='SP ZONE all-in-one machines: refrigerant recovery, recycling, flushing, leak test, vacuum and oil injection.',
         lede='One machine for the whole aircon service, from recovering the old refrigerant to flushing the system and recharging it.',
         answer='CSKA supplies SP ZONE car aircon service machines to Singapore workshops. The SPZ-FA1 and SPZ6000 recover, recycle and flush refrigerant, leak test, vacuum and inject oil (PAG, or POE for hybrids on the SPZ-FA1), with a refrigerant database, printed service reports and automatic purging of non-condensable gas.',
         gallery=['handover-aircon-machine', 'spz6000-in-use', 'aircon-machine-demo', 'handover-aircon-machine-b', 'spz6000-training', 'aircon-machine-team', 'aircon-machine-steven'],
         models=[('SP ZONE', 'SPZ-FA1 flushing and recovery machine', 'All in one: recovery, recycle, flushing, leak test, vacuum and oil injection, PAG or hybrid POE oil selection, 8.4-inch display, report printing, reverse pipe cleaning.'),
                 ('SP ZONE', 'SPZ6000 refrigerant flushing and recovery machine', 'Recovery, recycle, flushing, leak test, vacuum and oil injection, 9-inch display, report printing, bigger cylinder, three fans and condenser.')],
         extra='<h2>How to choose a car aircon machine for a Singapore workshop</h2>'
               '<p class="answer">Choose an all-in-one machine that recovers, recycles and flushes refrigerant, leak tests, pulls a vacuum and injects oil, so one unit covers the whole aircon service. Then check the oil options (PAG, and POE if you service hybrids), the cylinder size for busy days, the cooling fans, and whether it prints a report for the customer. CSKA supplies the SP ZONE SPZ-FA1 and SPZ6000.</p>'
               + table_html(['Feature', 'SP ZONE SPZ-FA1', 'SP ZONE SPZ6000'], [
                   ('Functions', 'Recovery, recycle, flushing, leak test, vacuum, oil injection', 'Recovery, recycle, flushing, leak test, vacuum, oil injection'),
                   ('Display', '8.4-inch', '9-inch'),
                   ('Oil', 'PAG or hybrid POE oil selection', 'Oil injection (ask us about hybrid POE oil)'),
                   ('Refrigerant cylinder', 'Standard', 'Bigger cylinder'),
                   ('Cooling', 'Not listed', 'Three fans and a condenser'),
                   ('Service report', 'Report printing', 'Report printing'),
                   ('Pipe cleaning', 'Reverse pipe cleaning', 'Not listed'),
               ], caption='Specifications are SP ZONE\'s own, as posted by CSKA. Ask us to confirm the current version before you order.')
               + '<h3>What one aircon service looks like with the machine</h3>'
               + steps([('Recover', 'The old refrigerant is pulled out of the car and weighed.'), ('Recycle', 'The machine cleans the recovered refrigerant and purges non-condensable gas automatically.'),
                        ('Flush', 'Dirt and old oil are flushed out of the system, which matters after a compressor failure.'), ('Leak test and vacuum', 'The system is checked for leaks and pulled down to a vacuum.'),
                        ('Oil injection', 'The right oil (PAG, or POE for hybrids on the SPZ-FA1) goes back in.'), ('Recharge and report', 'Refrigerant is charged by the database figure and a report is printed for the customer.')])
               + '<p>New to these machines? Read <a href="articles/car-aircon-flushing-machine-guide/">Car aircon flushing and recovery machines: a workshop guide</a>.</p>',
         faqs=[('What does an aircon flushing and recovery machine do?', 'It recovers the refrigerant from the car\'s aircon, recycles it, flushes dirt and old oil out of the system, tests for leaks, pulls a vacuum and then recharges the refrigerant and oil, all from one machine.'),
               ('Why flush a car aircon system?', 'When a compressor fails, black oil and debris spread through the system. Flushing removes them so the new compressor is not damaged. We have posted a video of how black that oil can get.'),
               ('Can the machine service hybrid cars?', 'The SPZ-FA1 lets you choose PAG oil or POE oil for hybrid compressors.'),
               ('Do you show us how to use it?', 'Our photos show the team taking workshop staff through the machine at handover. Ask Steven what is included with yours.'),
               ('Does the machine print a service report for the customer?', 'Yes. Both the SPZ-FA1 and the SPZ6000 print a service report, so the workshop can hand the customer a record of the recovery, vacuum and recharge.'),
               ('Does the machine remove air from the recovered refrigerant?', 'Yes. The SP ZONE machines purge non-condensable gas automatically during recycling, and the refrigerant database sets the charge quantity for the car.')]),
    dict(slug='battery-testers-and-jump-starters', short='Battery tools', photo='handover-v4500',
         title='Battery Testers, Chargers and Jump Starters | CSKA Singapore',
         desc='THINKCAR TBT 360 and TOPDON BT600 battery testers, TOPDON V4500 Plus jump starter, Tornado 30000 charger and THINKPPS 150 power supply.',
         h1='Battery testers, chargers and jump starters',
         gist='Battery testers that print reports, a 4500A jump starter, chargers and a programming power supply.',
         lede='Test the battery, charging and starting system in a minute, and keep voltage steady while you program.',
         answer='CSKA supplies battery tools to Singapore workshops: THINKCAR TBT 360 and TBT 360 Pro testers (3 to 360 Ah), the TOPDON BT600 tester with a built-in printer, the TOPDON V4500 Plus 12V jump starter (4500A peak), the TOPDON Tornado 30000 charger and the THINKPPS 150, which keeps a stable supply during module programming.',
         gallery=['handover-v4500', 'handover-v4500-b', 'thinkcar-trolley-thinkpps', 'handover-thinktool-191-d'],
         models=[('THINKCAR', 'TBT 360 / TBT 360 Pro', 'Tests batteries from 3 to 360 Ah plus the charging and starting system. 2.8-inch screen, Kelvin clamps, cuts off above 35V. The Pro prints reports.'),
                 ('TOPDON', 'BT600 battery tester', '12V tester with a 3.5-inch colour screen and built-in thermal printer. Measures real cold cranking amps and state of health.'),
                 ('TOPDON', 'V4500 Plus jump starter', '12V, up to 4500A peak and up to 45 jump starts per charge. PD100W fast charging, about 90 minutes to full, 3-minute boost mode.'),
                 ('TOPDON', 'Tornado 30000 battery charger', 'Workshop battery charger from TOPDON\'s Tornado range.'),
                 ('THINKCAR', 'THINKPPS 150 power supply', 'Stable power for module programming, fast charging for AGM, GEL and EFB batteries, battery activation and repair, 400A jump start and exhibition mode.'),
                 ('THINKCAR', 'Portable car battery charger', 'A compact THINKCAR charger for the workshop or the road.')],
         extra='<h2>Which battery tester does a Singapore workshop need?</h2>'
               '<p class="answer">Choose a battery tester by the battery sizes you test and whether you hand the customer a printout. The THINKCAR TBT 360 tests batteries from 3 to 360 Ah and the charging and starting system, while the TBT 360 Pro and the TOPDON BT600 print a report. Add a jump starter for flat-battery calls and a power supply when you program modules.</p>'
               + table_html(['Tool', 'Use it for', 'What the page lists'], [
                   ('THINKCAR TBT 360', 'Many battery sizes, plus the charging and starting system', 'Tests 3 to 360 Ah; 2.8-inch screen, Kelvin clamps, cuts off above 35V'),
                   ('THINKCAR TBT 360 Pro', 'The same tests with a printed report for the customer', 'Prints reports'),
                   ('TOPDON BT600', 'A printed cold cranking amps and state-of-health result', '3.5-inch colour screen, built-in thermal printer, measures real cold cranking amps'),
                   ('TOPDON V4500 Plus', 'Starting a flat battery on a call-out or in the bay', '12V, up to 4500A peak, up to 45 jump starts per charge'),
                   ('THINKPPS 150', 'Steady voltage while programming, and charging AGM, GEL and EFB batteries', 'Stable power for module programming, 400A jump start'),
               ], caption='A checklist, not a quote. Ask CSKA to confirm current versions and what comes in the box.')
               + '<p>Not sure what a test report tells your customer? Read <a href="articles/battery-tester-report-cca-state-of-health/">Battery tester reports explained: what CCA and State of Health tell your customer</a>.</p>',
         faqs=[('Why use a power supply when programming a car?', 'Programming can take a long time with the ignition on. If battery voltage drops, the update can fail. A programming power supply such as the THINKPPS 150 keeps the voltage steady.'),
               ('Which battery tester prints a report for the customer?', 'The THINKCAR TBT 360 Pro and the TOPDON BT600 both print test reports.'),
               ('Is the V4500 Plus only for big vehicles?', 'It is a 12V jump starter built for high-displacement vehicles, trucks, off-road vehicles and boats, so it also has plenty of power for cars.'),
               ('Which battery tester should a workshop buy?', 'Choose by the battery sizes you test and whether you give customers a printout. The TBT 360 covers 3 to 360 Ah, and the TBT 360 Pro and BT600 print reports. WhatsApp us the cars you service and we will suggest one.'),
               ('Does the BT600 measure cold cranking amps?', 'Yes. The TOPDON BT600 measures real cold cranking amps and state of health, and prints the result on its built-in thermal printer.')]),
    dict(slug='lifts-and-jacks', short='Lifts and jacks', photo='tfj-330-jack',
         title='Two-Post Car Lifts, Floor Jacks and Stands | CSKA Singapore',
         desc='Two-post car lifts (4 ton), THINKCAR TFJ 330 low-profile jacks, 3-ton jack stands, transmission jacks and underhoist stands for workshops.',
         h1='Lifts, jacks and stands',
         gist='Two-post lifts, low-profile floor jacks, jack stands, transmission jacks and EV battery lifts.',
         lede='The lifting equipment a workshop bay needs, from the two-post lift to the stands under the car.',
         answer='CSKA supplies lifting equipment to Singapore workshops: 4-ton two-post lifts (including top-connection models), the THINKCAR TFJ 330 dual-pump low-profile jack with an 85 mm minimum height, 3-ton floor jacks and THINKCAR TFJ103 3-ton jack stands, 500 kg double-stage transmission jacks, underhoist stands and the EVP501 EV battery lift.',
         gallery=['tfj-330-jack', 'handover-master-x2', 'handover-ms908s-ii', 'handover-master-2'],
         models=[('Lift', 'Two-post lift, 4 ton', 'Supplied and set up for new workshops; top-connection models with one-side lock also available.'),
                 ('THINKCAR', 'TFJ 330 dual pump jack', 'Dual pumps for faster lifting, 85 mm minimum pad height, magnetic tool tray, 360-degree wheels.'),
                 ('THINKCAR', 'TFJ103 jack stand (3 ton)', 'Pairs with the 3-ton THINKCAR floor jack 330.'),
                 ('Jack', 'TECH THJ-75 low-profile floor jack', '3 ton, double pump, low profile.'),
                 ('Jack', 'Double-stage transmission jack', '500 kg hydraulic jack for gearbox work.'),
                 ('Stand', '3/4 underhoist stand', 'Supports components while the car is on the lift.'),
                 ('Lift', 'EVP501 EV battery lift', 'Up to 1,500 kg and 1,785 mm, electric raise and lower with a mechanical safety lock.')],
         extra='<h2>Which two-post lift does a Singapore workshop need?</h2>'
               '<p class="answer">For most general repair workshops, a 4-ton two-post lift is the starting point: it keeps the wheels, brakes and suspension open and takes little floor space. A 4-ton lift is in the same class as the 9,000 lb (about 4.1-tonne) lifts sold from overseas. Before you buy any lift, confirm your ceiling height, floor strength, the heaviest vehicle you lift and who sets it up. CSKA supplies 4-ton two-post lifts, including top-connection models with a one-side lock, and sets them up for new workshops.</p>'
               + table_html(['Check', 'Why it matters', 'What to tell CSKA'], [
                   ('Ceiling height', 'The raised lift and the tallest car you service must clear beams, lights and roller shutters', 'The clear height of your bay and the tallest vehicle you work on'),
                   ('Floor', 'A two-post lift is normally fixed to the floor with anchor bolts, so the slab must suit the lift maker\'s requirements', 'Slab thickness and condition, if you know them'),
                   ('Capacity', 'The rated capacity must cover the heaviest vehicle you lift, including SUVs and vans', 'The heaviest vehicles you service'),
                   ('Set-up', 'Lifts are supplied and set up for new workshops, so ask what is included and who tests it', 'Your unit size, number of bays and start date'),
               ], caption='A checklist, not a quote. Ask CSKA to confirm model details, the maker\'s installation requirements and what is included.')
               + '<p>Choosing between lift types? Read <a href="articles/two-post-vs-four-post-lift-workshop/">Two-post lift or four-post lift for a Singapore workshop unit</a>.</p>',
         faqs=[('Do you supply two-post lifts for new workshops?', 'Yes. Two-post lifts are part of the new workshop set-ups we supply. WhatsApp Steven with your floor space and the vehicles you work on.'),
               ('What is a low-profile jack for?', 'Lowered cars and sports cars sit too low for a normal jack. The THINKCAR TFJ 330 goes down to 85 mm, so it fits under them.'),
               ('Do you have a jack for gearbox removal?', 'Yes, a 500 kg double-stage hydraulic transmission jack.'),
               ('Is a 4-ton two-post lift enough for SUVs and vans?', 'It depends on the vehicle. Compare the lift\'s rated capacity with the weight of the heaviest vehicle you will lift, and ask CSKA to confirm the model\'s capacity and arm reach before you order.'),
               ('What should I ask any seller before buying a car lift?', 'Ask what ceiling height and floor strength the lift needs, what power supply it uses, who installs and tests it in your workshop, and who you call for help afterwards.')]),
    dict(slug='workshop-tools', short='Workshop tools', photo='handover-tool-trolley',
         title='Workshop Tools: Tool Trolleys, Impact Wrenches, Leak Detectors',
         desc='Tool trolleys and sets, Ingersoll Rand and M7 impact wrenches, THINKCAR PLD 212 smoke leak detector, waste oil drainers and service tools.',
         h1='Workshop tools and equipment',
         gist='Tool trolleys and sets, air impact wrenches, smoke leak detectors, waste oil drainers and service kits.',
         lede='Hand tools, air tools and the service equipment that keeps a bay moving.',
         answer='CSKA supplies workshop tools to Singapore car workshops: seven- and eight-drawer tool trolleys with 360 to 376-piece sets, Ingersoll Rand and M7 air impact wrenches, the THINKCAR PLD 212 smoke leak detector, THINKCAR and HPMM waste oil drainers, Lige brake bleeders and torque wrenches, and service kits such as ATF extractors and coolant pressure testers.',
         gallery=['handover-tool-trolley', 'handover-thinktool-se-trolley', 'pld-212-smoke-test', 'handover-ingersoll-rand', 'thinkcar-trolley-thinkpps'],
         models=[('THINKCAR', 'TTK 333 general tool kit', 'Seven drawers: 61-piece 12.5 mm sockets, 131-piece 6.3 and 10 mm sockets, 26 wrenches, 20 screwdrivers, 16 pliers, 51-piece and 28-piece mechanic\'s kits.'),
                 ('Tool set', '7-drawer trolley with 376-piece set', 'Cold-rolled steel trolley with a combination tool set.'),
                 ('Ingersoll Rand', '2141 3/4-inch Ultra Duty air impact wrench', 'Heavy-duty 3/4-inch drive impact wrench.'),
                 ('M7', 'NC4650 mini air impact wrench', 'Compact 1/2-inch drive impact wrench.'),
                 ('THINKCAR', 'PLD 212 smoke leak detector', 'Finds air, vacuum and oil leaks. Built-in pump, 13 to 16 PSI output, 8 to 15 L/min flow, pressure gauge and flow meters.'),
                 ('THINKCAR / HPMM', 'Waste oil drainers', 'THINKCAR TOR 218 with adjustable height and the HPMM HC2297 80 L mobile suction drainer.'),
                 ('Lige', 'Brake bleeder, transmission oil kit, torque wrench', 'Pneumatic brake bleeder, LG14007 transmission oil kit and LG49803 1/2-inch torque wrench (40 to 220 Nm).'),
                 ('Service kits', 'ATF extractor, coolant tester, more', 'ATF oil extractor and dispenser (9.5 L), radiator coolant pressure tester kit, brake pad spreader, coil spring compressor, compression tester, creeper.')],
         extra='<h2>Which workshop tools should a Singapore car workshop buy first?</h2>'
               '<p class="answer">Start with what every bay uses daily: a tool trolley with a full set, an air impact wrench for wheels and fasteners, and a waste oil drainer for servicing. Add the specialist tools as the jobs come in, such as a smoke leak detector for air, vacuum and oil leaks, and the service kits for transmission oil, coolant and brakes. CSKA supplies all of these to Singapore workshops.</p>'
               + table_html(['Job in the bay', 'Tool', 'What the page lists'], [
                   ('Everyday hand tools', 'THINKCAR TTK 333 or a 7-drawer trolley with a 376-piece set', 'Seven drawers; 61-piece 12.5 mm sockets, 131-piece 6.3 and 10 mm sockets, 26 wrenches, 20 screwdrivers, 16 pliers'),
                   ('Wheels and fasteners', 'Ingersoll Rand 2141 or M7 NC4650 air impact wrench', '3/4-inch drive heavy duty, or compact 1/2-inch drive'),
                   ('Oil changes', 'THINKCAR TOR 218 or HPMM HC2297 waste oil drainer', 'Adjustable height, or 80 L mobile suction drainer'),
                   ('Air, vacuum and oil leaks', 'THINKCAR PLD 212 smoke leak detector', 'Built-in pump, 13 to 16 PSI output, 8 to 15 L/min flow, pressure gauge and flow meters'),
                   ('Brakes and transmission service', 'Lige brake bleeder, transmission oil kit and torque wrench; ATF extractor', 'Pneumatic bleeder, 1/2-inch torque wrench (40 to 220 Nm), 9.5 L ATF extractor and dispenser'),
               ], caption='A checklist, not a quote. Ask CSKA to confirm current versions and what comes in the box.'),
         faqs=[('What is a smoke leak detector used for?', 'It fills the intake, vacuum or EVAP system with harmless smoke at low pressure so you can see exactly where it escapes. The THINKCAR PLD 212 also works with THINKCAR scan tools on leak-related faults.'),
               ('Do you sell complete tool trolleys?', 'Yes, seven- and eight-drawer trolleys with 360 to 376-piece tool sets, including the THINKCAR TTK 333.'),
               ('Do you carry workshop chemicals?', 'Yes, including Stirling brake cleaner and ThreeBond products. Ask us for the item you need.'),
               ('Which workshop tools should a new car workshop buy first?', 'Most start with a tool trolley and a full set, an air impact wrench and a waste oil drainer, then add a smoke leak detector and service kits as the jobs come in. WhatsApp us the services you plan and we will suggest a list.'),
               ('Do the tool trolleys come with the tools?', 'Yes. The trolleys on this page are sold with their sets, for example the seven-drawer THINKCAR TTK 333 and the seven-drawer trolley with a 376-piece set.')]),
    dict(slug='new-workshop-setup', short='New workshop set-up', photo='handover-master-x2',
         title='Equipment for a New Car Workshop in Singapore | CSKA',
         desc='Opening a car workshop? CSKA supplies the lifts, scanners, aircon machine, battery tester, jacks and tools in one order. WhatsApp 9822 2629.',
         h1='Setting up a new workshop',
         gist='One supplier for the lift, scanner, aircon machine, battery tester, jacks and tool trolleys.',
         lede='Tell us how many bays and what services you will offer. We put together the equipment list.',
         answer='CSKA supplies complete equipment for new car workshops in Singapore. Recent set-ups combined two-post lifts, a THINKTOOL Master X2 scanner, a THINKCAR TBT 360 Pro battery tester, an SP ZONE SPZ-FA1 aircon machine, low-profile jacks, a waste oil drainer, impact wrenches and a tool cabinet with 374 tools. WhatsApp Steven on 9822 2629 to plan yours.',
         gallery=['handover-master-x2', 'handover-thinktool-se-trolley', 'handover-tool-trolley', 'handover-aircon-machine', 'tfj-330-jack'],
         models=[('Example set-up', 'General workshop', 'Two-post lift (4 ton), THINKTOOL Master X2 (12V and 24V), THINKCAR TBT 360 Pro battery tester, SP ZONE SPZ-FA1 aircon machine.'),
                 ('Example set-up', 'Service bay', 'Two-post lift with top connection, HPMM 80 L waste oil drainer, TECH THJ-75 3-ton low-profile jack, 1/2-inch aluminium air impact wrench, 8-drawer cabinet with 374 tools.'),
                 ('Example set-up', 'Starter kit', '360-piece tool set with seven-layer trolley, THINKCAR 3-ton floor jack and stands, underhoist stand, M7 impact wrench, 500 kg transmission jack.')],
         faqs=[('What equipment does a new car workshop need?', 'Most start with a lift per bay, a diagnostic scanner, a battery tester, a floor jack and stands, an impact wrench, a waste oil drainer and a tool trolley. An aircon machine is added if you will do aircon service.'),
               ('Can you supply everything in one order?', 'Yes. Recent new workshops took their lift, scanner, battery tester, aircon machine and tools from us together.'),
               ('How do I start?', 'WhatsApp Steven on 9822 2629 with your unit size, number of bays and the services you plan, and we will send an equipment list and quote.')]),
]
PRD = {p['slug']: p for p in PRODUCTS}

# ----------------------------------------------------------------------------------------------
# Brands
# ----------------------------------------------------------------------------------------------
BRANDS = [
    dict(slug='thinkcar', name='THINKCAR', photo='handover-thinktool-191',
         title='THINKCAR Singapore: THINKTOOL Scanners and Tools | CSKA',
         desc='THINKCAR THINKTOOL scanners (Lite 2, SE, 191, Master X2, Expert 391, 394 EV), battery testers, jacks and leak detectors for Singapore workshops.',
         gist='THINKTOOL diagnostic scanners plus THINKCAR battery testers, jacks, leak detectors and tool kits.',
         answer='CSKA Auto Enterprise supplies THINKCAR to car workshops in Singapore: THINKTOOL scanners from the Lite 2 and T77 to the SE, 191, Master 2, Master X, Master X2, Expert 391 and Expert 394 EV, plus THINKCAR TBT battery testers, the THINKPPS 150 power supply, TFJ jacks and stands, the PLD 212 smoke leak detector and TTK tool kits.',
         lines=[('THINKTOOL scanners', 'diagnostic-scanners'), ('Expert 394 EV', 'ev-diagnostic-tools'), ('TPMS module and programmer', 'tpms-and-tyre-tools'),
                ('TBT battery testers, THINKPPS 150', 'battery-testers-and-jump-starters'), ('TFJ 330 jack, TFJ103 stands', 'lifts-and-jacks'), ('PLD 212, TTK 333, TOR 218', 'workshop-tools')],
         gallery=['handover-thinktool-191', 'handover-sg-garage', 'handover-expert-391', 'handover-master-x2', 'handover-thinktool-se', 'thinktool-se-tablet', 'handover-lite-2', 'handover-master-2', 'thinkcar-trolley-thinkpps'],
         faqs=[('Where can I buy THINKCAR tools in Singapore?', 'From CSKA Auto Enterprise at 101 Woodlands Avenue 12, Polaris @ Woodlands. WhatsApp Steven on 9822 2629 or Ah Kiat on 8493 0068.'),
               ('Which THINKTOOL has online programming?', 'The THINKTOOL Expert 391 and Expert 394 EV support online ECU programming.'),
               ('Which THINKTOOL should a small workshop start with?', 'The THINKTOOL Lite 2 and T77 are 7-inch full-function scanners with DoIP and CAN FD support. The SE adds an 8-inch screen, Android 10 and up to 34 service resets. WhatsApp us the cars you service and we will suggest a model.'),
               ('Do THINKTOOL scanners work on 24V trucks?', 'Yes. The THINKTOOL Master X and Master X2 cover 12V and 24V vehicles, and THINKCAR\'s HML package adds heavy-duty coverage to the Expert 391.'),
               ('Which THINKCAR tool tests a car battery?', 'The THINKCAR TBT 360 and TBT 360 Pro testers cover 3 to 360 Ah. The THINKPPS 150 power supply keeps a stable supply during module programming.')]),
    dict(slug='autel', name='Autel', photo='handover-ms908s-ii-b',
         title='Autel MaxiSys Singapore: Scanners, TPMS, ADAS | CSKA',
         desc='Autel MaxiSys MS908S II, MS908S3, MS909, MS909 S2, MaxiSYS Ultra EV, MaxiTPMS TS508WF and ADAS calibration for Singapore workshops.',
         gist='MaxiSys diagnostic tablets, MaxiSYS Ultra EV, MaxiTPMS and the ADAS calibration package.',
         answer='CSKA Auto Enterprise supplies Autel to Singapore workshops: MaxiSys MS908S II and MS908S3 tablets, the MaxiSYS MS909 and MS909 S2 with J2534 programming, the MaxiSYS Ultra EV for electric cars, the MaxiTPMS TS508WF for tyre shops, and the MaxiSys ADAS Complete Calibration Package.',
         lines=[('MaxiSys MS908S II, MS908S3, MS909, MS909 S2', 'diagnostic-scanners'), ('MaxiSYS Ultra EV, MS909 S2 EV', 'ev-diagnostic-tools'),
                ('MaxiTPMS TS508WF', 'tpms-and-tyre-tools'), ('MaxiSys ADAS calibration package', 'adas-calibration')],
         gallery=['handover-ms908s-ii-b', 'handover-ms908s-ii', 'handover-ms908s-ii-c', 'handover-ms908s-ii-d', 'handover-ms908s-ii-e', 'handover-ms908s3', 'handover-ts508wf', 'ms908s3-screen'],
         extra='<h2>Which Autel tool suits your workshop?</h2>'
               '<p class="answer">Autel MaxiSys is Autel\'s range of workshop diagnostic tablets. In Singapore, CSKA supplies the MS908S II and MS908S3 for everyday diagnostics, the MS909 and MS909 S2 when you need J2534 programming, the MaxiSYS Ultra EV and MS909 S2 EV for electric cars, the MaxiTPMS TS508WF for tyre shops and the ADAS calibration package. Each tool is handed over at your workshop.</p>'
               + table_html(['Autel tool', 'What it is', 'Key specifications', 'Best for'], [
                   ('MaxiSys MS908S II', 'Diagnostic tablet', '9.7-inch, Android 10, 128 GB, Bluetooth VCI; codes on all systems, active tests, live data, adaptations', 'Everyday workshop diagnostics'),
                   ('MaxiSys MS908S3', 'Diagnostic tablet', '10.1-inch, Android 10, DoIP and CAN FD, Auto Scan 2.0, 40+ service functions', 'Newer cars with DoIP and CAN FD'),
                   ('MaxiSYS MS909', 'Diagnostic tablet', '9.7-inch, 128 GB, VCI with DoIP, D-PDU and J2534, topology module mapping', 'J2534 programming'),
                   ('MaxiSYS MS909 S2', 'Diagnostic tablet', '11-inch, Android 13, 256 GB, MaxiFLASH VCI2 with J2534 pass-thru, Topology 3.0, 45+ service functions; ADAS upgrade available', 'Flagship diagnostics and programming'),
                   ('MaxiSYS Ultra EV', 'EV diagnostic tablet', 'High-voltage system analysis with diagrams and disassembly guides, State of Charge and State of Health, battery pack testing via OBD or direct cables', 'Electric car specialists'),
                   ('MaxiSYS MS909 S2 EV', 'Diagnostic tablet with EV functions', 'The MS909 S2 with EV functions; used by our team to check Tesla battery status', 'Workshops adding EV work to a general bay'),
                   ('MaxiTPMS TS508WF', 'TPMS tool', 'Activates sensors, reads sensor status, checks system health, programs MX-sensors, runs relearns; Quick and Advanced modes; Wi-Fi updates', 'Tyre shops'),
                   ('MaxiSys ADAS Complete Calibration Package', 'ADAS calibration equipment', 'Standard calibration frame, LDW package, AVM-RCW-BSD-NV kit, ADAS software, MS908P complete set', 'Windscreen, bumper and alignment work'),
               ], caption='Specifications are Autel\'s own, as posted by CSKA. Ask us to confirm current versions and what comes in the box.')
               + '<p>Comparing brands? See <a href="articles/thinkcar-or-autel/">THINKCAR or Autel: which scanner suits your workshop?</a></p>',
         faqs=[('Where can I buy Autel MaxiSys in Singapore?', 'CSKA Auto Enterprise in Woodlands supplies Autel MaxiSys tablets to workshops. WhatsApp Steven on 9822 2629.'),
               ('Which Autel tablet supports J2534 programming?', 'The MaxiSYS MS909 and MS909 S2 come with a J2534 pass-thru VCI.'),
               ('Which Autel tablet supports DoIP and CAN FD?', 'The MaxiSys MS908S3 supports DoIP and CAN FD, and the MaxiSYS MS909 VCI supports DoIP, D-PDU and J2534. Newer cars increasingly need DoIP or CAN FD for a full scan.'),
               ('Which Autel tool is for electric cars?', 'The MaxiSYS Ultra EV reads high-voltage systems, shows State of Charge and State of Health and can test the battery pack directly with its cables. The MS909 S2 EV adds EV functions to the MS909 S2 tablet.'),
               ('Can my Autel MS909 S2 do ADAS calibration?', 'Yes, the MS909 S2 can be upgraded for ADAS calibration with software and the target package. WhatsApp us your tablet model and we will tell you what you need.')]),
    dict(slug='topdon', name='TOPDON', photo='handover-v4500-b',
         title='TOPDON Singapore: Phoenix Elite, BT600, V4500 Plus | CSKA',
         desc='TOPDON Phoenix Elite scanner, BT600 battery tester, V4500 Plus jump starter and Tornado 30000 charger for Singapore workshops.',
         gist='The Phoenix Elite scanner, BT600 battery tester, V4500 Plus jump starter and Tornado chargers.',
         answer='CSKA Auto Enterprise supplies TOPDON to Singapore workshops: the Phoenix Elite diagnostic tool with wireless VCI and topology mapping, the BT600 battery tester with a built-in printer, the V4500 Plus 12V jump starter with up to 4500A peak, and the Tornado 30000 battery charger.',
         lines=[('Phoenix Elite', 'diagnostic-scanners'), ('BT600, V4500 Plus, Tornado 30000', 'battery-testers-and-jump-starters')],
         gallery=['handover-v4500-b', 'handover-v4500', 'handover-phoenix-elite'],
         extra='<h2>Which TOPDON tool does a Singapore workshop need?</h2>'
               '<p class="answer">It depends on the job. For diagnostics, the Phoenix Elite scanner. For testing a battery and printing the result for the customer, the BT600. For a flat battery in the workshop, the V4500 Plus jump starter, and for charging batteries, the Tornado 30000. CSKA supplies all four in Singapore and hands each one over at your workshop.</p>'
               + table_html(['TOPDON tool', 'What it is', 'Key specifications', 'Best for'], [
                   ('Phoenix Elite', 'Diagnostic scanner', 'Tablet with wireless VCI; CAN FD; topology mapping; guided VW and Audi functions; pre-scan and post-scan reports', 'Workshops that want printed before/after reports'),
                   ('BT600', 'Battery tester', '12V; 3.5-inch colour screen; built-in thermal printer; measures real cold cranking amps and state of health', 'Testing a battery and handing the customer a report'),
                   ('V4500 Plus', 'Jump starter', '12V; up to 4500A peak; up to 45 jump starts per charge; PD100W fast charging, about 90 minutes to full; 3-minute boost mode', 'Starting flat batteries in and around the workshop'),
                   ('Tornado 30000', 'Battery charger', 'Workshop battery charger from TOPDON\'s Tornado range', 'Charging batteries in the workshop'),
               ], caption='Specifications are TOPDON\'s own, as posted by CSKA. Ask us to confirm current versions and what comes in the box.')
               + '<p>See the full range on <a href="products/diagnostic-scanners/">diagnostic scanners</a> and <a href="products/battery-testers-and-jump-starters/">battery testers and jump starters</a>.</p>',
         faqs=[('Where can I buy a TOPDON jump starter in Singapore?', 'CSKA Auto Enterprise supplies the TOPDON V4500 Plus to workshops. WhatsApp Steven on 9822 2629.'),
               ('Does TOPDON make a scanner for workshops?', 'Yes, the Phoenix Elite, with wireless VCI, CAN FD, topology mapping and pre-scan and post-scan reports.'),
               ('Which TOPDON tool prints a report for the customer?', 'The BT600 battery tester has a built-in thermal printer, and the Phoenix Elite scanner produces pre-scan and post-scan reports.'),
               ('How many jump starts does the TOPDON V4500 Plus give?', 'Up to 45 jump starts per charge, with up to 4500A peak. It charges with PD100W in about 90 minutes and has a 3-minute boost mode.'),
               ('Does CSKA deliver TOPDON tools to the workshop?', 'Yes. Each tool is delivered to your workshop and handed over in person.')]),
    dict(slug='sp-zone', name='SP ZONE', photo='spz6000-in-use',
         title='SP ZONE Aircon Machines Singapore: SPZ-FA1, SPZ6000 | CSKA',
         desc='SP ZONE SPZ-FA1 and SPZ6000 car aircon refrigerant flushing and recovery machines, supplied to Singapore workshops by CSKA Auto Enterprise.',
         gist='SPZ-FA1 and SPZ6000 all-in-one car aircon flushing and recovery machines.',
         answer='CSKA Auto Enterprise supplies SP ZONE car aircon machines in Singapore: the SPZ-FA1 and SPZ6000 refrigerant flushing and recovery machines, which recover, recycle, flush, leak test, vacuum and inject oil in one unit. SP ZONE\'s Ah Heng visited Singapore to support us, and several workshops run more than one of our SPZ6000 units.',
         lines=[('SPZ-FA1, SPZ6000', 'aircon-service-machines')],
         gallery=['spz6000-in-use', 'handover-aircon-machine', 'handover-aircon-machine-b', 'aircon-machine-demo', 'spz6000-training', 'aircon-machine-team'],
         extra='<h2>Which SP ZONE aircon machine does a Singapore workshop need?</h2>'
               '<p class="answer">Both SP ZONE machines do the whole aircon service in one unit: recover, recycle, flush, leak test, vacuum and oil injection, with a printed report for the customer. Choose the SPZ-FA1 if you service hybrids and want to pick PAG or POE oil, or want reverse pipe cleaning. Choose the SPZ6000 if you want the 9-inch screen, a bigger cylinder and three fans with a condenser for busy days. CSKA supplies both and hands them over at your workshop.</p>'
               + table_html(['SP ZONE machine', 'What it is', 'Key specifications', 'Best for'], [
                   ('SPZ-FA1', 'Flushing and recovery machine', '8.4-inch display; PAG or hybrid POE oil selection; report printing; reverse pipe cleaning', 'Workshops that service hybrid cars'),
                   ('SPZ6000', 'Flushing and recovery machine', '9-inch display; bigger cylinder; three fans and a condenser; report printing', 'Busy workshops doing many aircon jobs a day'),
               ], caption='Specifications are SP ZONE\'s own, as posted by CSKA. Ask us to confirm the current version before you order.')
               + '<p>Full comparison and the six steps of an aircon service: <a href="products/aircon-service-machines/">car aircon service machines</a>.</p>',
         faqs=[('Where can I buy an SP ZONE aircon machine in Singapore?', 'From CSKA Auto Enterprise in Woodlands. WhatsApp Steven on 9822 2629 or Alvis on 9037 2820.'),
               ('What is the difference between the SPZ-FA1 and SPZ6000?', 'Both are all-in-one recovery, flushing and recharge machines. The SPZ-FA1 has an 8.4-inch screen and PAG or hybrid POE oil selection; the SPZ6000 has a 9-inch screen, a bigger cylinder and three fans with a condenser.'),
               ('Which SP ZONE machine should a workshop that services hybrids choose?', 'The SPZ-FA1 lets you choose PAG oil or POE oil for hybrid compressors. WhatsApp Steven on 9822 2629 and we will confirm which machine fits your workshop.'),
               ('Does the SP ZONE machine print a service report?', 'Yes. Both the SPZ-FA1 and the SPZ6000 print a service report for the customer.'),
               ('Does CSKA deliver SP ZONE machines to the workshop?', 'Yes. Each machine is delivered to your workshop and handed over in person.')]),
]
BRD = {b['slug']: b for b in BRANDS}
OTHER_BRANDS = [('Ingersoll Rand', 'Air impact wrenches'), ('M7', 'Air tools'), ('Lige', 'Brake bleeders, oil kits, torque wrenches'),
                ('Stirling', 'Brake cleaner and workshop chemicals'), ('ThreeBond', 'Sealants and adhesives')]
BRAND_NAMES = ['THINKCAR', 'Autel', 'TOPDON', 'SP ZONE', 'Ingersoll Rand', 'Stirling', 'ThreeBond']

# ----------------------------------------------------------------------------------------------
# Articles (long-tail questions workshop owners search; general guidance, product facts only from CSKA's posts)
# ----------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='choosing-a-diagnostic-scanner-for-your-workshop', photo='handover-thinktool-191-c', products=['diagnostic-scanners', 'ev-diagnostic-tools'],
         title='How to Choose a Diagnostic Scanner for a Car Workshop',
         desc='What to check before buying a workshop scan tool in Singapore: coverage, full system scan, bi-directional tests, coding, programming and updates.',
         h1='How to choose a diagnostic scanner for your workshop',
         answer='Choose a workshop scanner by the cars you service and the jobs you do. Check full-system coverage for those makes, bi-directional tests, the service resets you use most, whether you need coding or online programming, support for DoIP and CAN FD on newer cars, and what software updates cost after the first year.',
         sections=[('Start from the cars in your bays', ['List the makes and model years you see every week. A tool that is strong on Japanese and Korean cars may be weaker on recent European cars, and the reverse. Ask the supplier to check coverage for your top makes, not the total number of brands on the box.']),
                   ('Match the functions to your jobs', None, [('Read and clear codes, live data', 'every scanner does this on all systems.'),
                                                              ('Bi-directional tests', 'switch components on and off to prove a fault.'),
                                                              ('Service resets', 'oil service, brake pad, throttle, steering angle, battery registration.'),
                                                              ('Coding', 'set up replacement modules and options.'),
                                                              ('Online programming', 'load new software into modules; needs a stable power supply.')]),
                   ('Check the communication protocols', ['Newer cars use DoIP and CAN FD. Make sure the tool and its VCI support them. If you plan to program with the carmakers\' own software, look for J2534 pass-thru support, as on the Autel MS909 S2 or the THINKTOOL Master X2.']),
                   ('Think about the next two years', ['Ask how long free updates last and what renewal costs. If electric cars are coming into your workshop, look at EV-capable tools such as the THINKCAR Expert 394 EV or the Autel MaxiSYS Ultra EV now rather than replacing the scanner later.']),
                   ('Try it on a real car', ['A short demo on a car from your own workshop tells you more than a spec sheet. CSKA can arrange one for the model you are considering.'])],
         faqs=[('How much should a workshop spend on a scanner?', 'It depends on the jobs you do. A full-system scanner covers diagnosis and resets; coding, programming and EV functions cost more. Ask us for quotes on two levels and compare what each adds.'),
               ('Is one scanner enough for a workshop?', 'Many small workshops start with one. Busier workshops often keep a second tool, for example a fast scanner at the service bay and a programming tablet for harder jobs.')]),
    dict(slug='thinkcar-or-autel', photo='handover-ms908s-ii-e', products=['diagnostic-scanners'],
         title='THINKCAR or Autel: Which Scanner Suits Your Workshop?',
         desc='How THINKCAR THINKTOOL and Autel MaxiSys scanners compare for Singapore workshops, model by model, and how to decide between them.',
         h1='THINKCAR or Autel: which scanner suits your workshop?',
         answer='Both THINKCAR and Autel make full-system workshop scanners with coding, bi-directional tests and service resets. THINKCAR\'s THINKTOOL range spans small 7-inch scanners to online-programming tablets and adds 24V heavy-duty coverage on some models; Autel\'s MaxiSys tablets are strong on programming with J2534 VCIs and connect to Autel\'s TPMS and ADAS equipment.',
         sections=[('Models side by side', None, [('Entry full-system scanner', 'THINKCAR THINKTOOL Lite 2 or T77 (7-inch).'),
                                                 ('Mid-range tablet', 'THINKTOOL SE or 191; Autel MaxiSys MS908S II or MS908S3.'),
                                                 ('Programming tablet', 'THINKTOOL Master X2 or Expert 391; Autel MaxiSYS MS909 or MS909 S2 with J2534.'),
                                                 ('12V and 24V', 'THINKTOOL Master X and Master X2; Expert 391 with the HML package.'),
                                                 ('Electric cars', 'THINKCAR Expert 394 EV; Autel MaxiSYS Ultra EV.')]),
                   ('When THINKCAR tends to fit', ['Workshops that also see commercial vehicles, or want one tool family from a basic scanner up to an add-on TPMS programmer, battery tester and smoke leak detector that work with the scanner.']),
                   ('When Autel tends to fit', ['Workshops that program modules often, tyre shops that want Autel MaxiTPMS, and workshops planning ADAS calibration with the Autel calibration frame and targets.']),
                   ('The honest answer', ['The right choice depends on your makes and jobs. Bring a car or a list of recent jobs and compare both on the same vehicle before you decide.'])],
         faqs=[('Can I use THINKCAR and Autel tools in the same workshop?', 'Yes. Many workshops keep tools from both makers and use whichever covers the car in front of them better.'),
               ('Which one is easier to learn?', 'Both run on Android tablets with similar menus. A short handover session on the tool you choose is usually enough to start.')]),
    dict(slug='j2534-doip-can-fd-explained', photo='ms908s3-screen', products=['diagnostic-scanners', 'battery-testers-and-jump-starters'],
         title='J2534, DoIP and CAN FD Explained for Workshops',
         desc='Plain-English guide to the J2534, DoIP and CAN FD terms on scan tool spec sheets, and why they matter for programming newer cars.',
         h1='J2534, DoIP and CAN FD explained',
         answer='J2534 is a standard that lets a workshop use the carmaker\'s own software through an aftermarket interface to reprogram modules. DoIP is diagnostics over Ethernet, used by many newer cars for fast data transfer. CAN FD is a faster version of the CAN bus. A scanner needs the right one to talk to, code or program a newer car.',
         sections=[('J2534 pass-thru', ['A J2534 device sits between a laptop or tablet and the car, so the carmaker\'s service software can flash new module software. Autel\'s MaxiSYS MS909 and MS909 S2 come with a J2534 VCI, and the THINKTOOL Master X2 and Expert 391 support J2534.']),
                   ('DoIP', ['Diagnostics over Internet Protocol uses an Ethernet connection through the OBD port. It moves large amounts of data quickly, which newer cars need for programming. Tools such as the THINKTOOL Lite 2, SE and Expert 391 and the Autel MS908S3 support it.']),
                   ('CAN FD', ['CAN with Flexible Data-rate carries more data per message than classic CAN. If a scanner does not support it, it may not connect to some modules on newer cars at all.']),
                   ('Before you program a module', None, [('Stable voltage', 'connect a programming power supply such as the THINKPPS 150.'),
                                                       ('Stable internet', 'online programming downloads files during the job.'),
                                                       ('Right software', 'confirm the tool supports that make, model and module before you start.')])],
         faqs=[('Do I need J2534 if my scanner already programs?', 'Not always. Many scanners program supported modules on their own. J2534 adds the option to use the carmaker\'s own software where the scanner does not cover a job.'),
               ('Why did my scanner not connect to a new car?', 'The car may use DoIP or CAN FD on that module. Check that your tool and its VCI support both, and that the software is up to date.')]),
    dict(slug='checking-ev-battery-health', photo='handover-expert-394-ev', products=['ev-diagnostic-tools'],
         title='Checking an EV Battery\'s Health in the Workshop',
         desc='How workshops read State of Charge and State of Health on electric cars with EV scan tools, and what to check before high-voltage work.',
         h1='Checking an EV battery\'s health in the workshop',
         answer='Workshops check an EV battery with an EV-capable scan tool that reads the high-voltage system: State of Charge shows how full the battery is, and State of Health shows how much capacity it has left compared with new. Tools such as the Autel MaxiSYS Ultra EV also show cell data and can test the pack directly.',
         sections=[('What the numbers mean', None, [('State of Charge (SoC)', 'how full the battery is now, like a fuel gauge.'),
                                                  ('State of Health (SoH)', 'remaining capacity compared with a new battery.'),
                                                  ('Cell voltages and temperatures', 'show weak cells or modules.'),
                                                  ('Fault codes', 'from the battery management system and high-voltage components.')]),
                   ('Why customers ask for it', ['Buyers of used EVs want to know the battery\'s condition, and owners want to know whether a range drop is normal. A printed or shared report from the scan tool answers both.']),
                   ('Safety first', ['High-voltage work needs trained staff, insulated tools and the maker\'s procedure. Reading data through the OBD port is low risk; opening or removing the pack is not. An EV battery lift such as the EVP501 supports the pack during removal.']),
                   ('Which tools can do it', ['The THINKCAR Expert 394 EV, the Autel MaxiSYS Ultra EV and the Autel MS909 S2 EV read EV systems on supported cars. Coverage varies by make, so check your EV brands before you buy.'])],
         faqs=[('Can any scanner read an EV battery\'s State of Health?', 'No. You need an EV-capable tool with coverage for that make. Basic OBD scanners usually cannot read high-voltage battery data.'),
               ('Is a battery health check the same on every EV?', 'The idea is the same, but what each make exposes differs. Some show SoH directly; others need a deeper test of the pack.')]),
    dict(slug='car-aircon-flushing-machine-guide', photo='spz6000-training', products=['aircon-service-machines'],
         title='Car Aircon Flushing and Recovery Machines: A Workshop Guide',
         desc='What an all-in-one car aircon recovery and flushing machine does, when to flush a system, and what to look for when buying one.',
         h1='Car aircon flushing and recovery machines: a workshop guide',
         answer='An all-in-one car aircon machine recovers and recycles the refrigerant, flushes old oil and debris out of the system, leak tests, pulls a vacuum and recharges the refrigerant and oil. Flushing matters most after a compressor failure, when contaminated black oil spreads through the condenser, pipes and evaporator.',
         sections=[('The service, step by step', None, [('Recover', 'pull the refrigerant out of the car into the machine.'),
                                                       ('Recycle', 'clean the recovered refrigerant for reuse.'),
                                                       ('Flush', 'push cleaning fluid through to carry out old oil and debris.'),
                                                       ('Leak test and vacuum', 'confirm the system holds and remove air and moisture.'),
                                                       ('Recharge', 'inject the right oil and the right amount of refrigerant.')]),
                   ('When to flush', ['After a compressor failure, or when the oil comes out dark, flush before fitting the new compressor. Debris left in the system can destroy the new part.']),
                   ('What to look for in a machine', None, [('Automatic operation', 'with on-screen prompts, so any technician can run it.'),
                                                           ('Refrigerant database', 'charge amounts by car model.'),
                                                           ('Oil selection', 'PAG for most cars, POE for hybrid electric compressors.'),
                                                           ('Printed report', 'to show the customer what was done.'),
                                                           ('Non-condensable gas purge', 'keeps recycled refrigerant clean.')]),
                   ('The machines we supply', ['CSKA supplies SP ZONE\'s SPZ-FA1 (8.4-inch display, PAG or hybrid POE oil) and SPZ6000 (9-inch display, bigger cylinder, three fans and condenser).'])],
         faqs=[('Can I use the same oil for hybrid cars?', 'No. Hybrids with electric compressors usually need POE oil, because PAG oil can affect the compressor\'s insulation. Choose a machine that lets you select the oil.'),
               ('How do I know a system needs flushing?', 'Dark or black oil, metal particles or a failed compressor are the usual signs.')]),
    dict(slug='new-car-workshop-equipment-checklist', photo='handover-thinktool-se-trolley', products=['new-workshop-setup', 'lifts-and-jacks', 'workshop-tools'],
         title='New Car Workshop Equipment Checklist (Singapore)',
         desc='A checklist of the equipment a new car workshop in Singapore needs on day one: lifts, scanner, battery tester, jacks, air tools and more.',
         h1='New car workshop equipment checklist',
         answer='A new car workshop usually needs a lift for each bay, a full-system diagnostic scanner, a battery tester, a low-profile floor jack and stands, an air impact wrench and compressor line, a waste oil drainer and a tool trolley with a full set. Add an aircon machine, TPMS tool or programming power supply for the services you plan.',
         sections=[('For every bay', None, [('Lift', 'a two-post lift suits most cars; check ceiling height and floor.'),
                                           ('Jack and stands', 'a low-profile floor jack reaches lowered cars.'),
                                           ('Tool trolley and set', 'sockets, wrenches, screwdrivers and pliers in one place.'),
                                           ('Air impact wrench', 'with a hose reel to the bay.')]),
                   ('For the workshop', None, [('Diagnostic scanner', 'full-system, with the resets you use most.'),
                                              ('Battery tester', 'ideally one that prints a report.'),
                                              ('Waste oil drainer', 'mobile suction or gravity type.'),
                                              ('Service kits', 'ATF extractor, coolant tester, brake bleeder, torque wrench.')]),
                   ('If you offer these services', None, [('Aircon', 'an all-in-one recovery and flushing machine.'),
                                                         ('Tyres', 'a TPMS tool to program and relearn sensors.'),
                                                         ('Programming', 'a stable power supply such as the THINKPPS 150.'),
                                                         ('EVs', 'an EV-capable scanner and an EV battery lift.')]),
                   ('Buy in the right order', ['Lifts and air lines go in before the opening; scanners and testers can follow. One supplier for the whole list keeps delivery and set-up on one schedule.'])],
         faqs=[('What should I buy first for a new workshop?', 'The lifts and compressed air system, because they are installed into the unit. Then the scanner, battery tester, jacks and tool trolleys.'),
               ('Can one supplier provide everything?', 'CSKA has supplied complete set-ups to new workshops: lifts, scanners, battery testers, aircon machines and tools in one order.')]),
    # Daily article 20 Oct 2026 (queue #4; first daily run after go-live). General TPMS knowledge; product facts only from the
    # TPMS product page (TS508WF, Master X2 TPMS module). No prices, no hours, no "authorised" brand claim, no customer workshops.
    dict(slug='tpms-activate-program-relearn-explained', photo='maxitpms-screen', products=['tpms-and-tyre-tools', 'diagnostic-scanners'],
         date='2026-10-20', date_text='20 October 2026',
         title='TPMS Activate, Program and Relearn Explained',
         desc='What activating, programming and relearning a TPMS sensor mean, when a tyre shop needs each step, and what to check in a TPMS tool.',
         h1='TPMS sensors: activate, program and relearn explained',
         answer='Activating a TPMS sensor wakes it up so the tool can read its ID, pressure, temperature and battery. Programming writes the right protocol and ID into a blank programmable sensor so it works on that car. Relearning teaches the car\'s TPMS module the new sensor IDs and their wheel positions, so the warning light goes off and the readings show correctly.',
         sections=[('What does activating a sensor do?', ['A direct TPMS sensor sits inside each wheel and sleeps most of the time to save its battery. The TPMS tool sends a low-frequency signal that wakes it, and the sensor replies with its ID, pressure, temperature and battery status. Activating every wheel before a tyre job shows straight away whether a sensor is dead, weak or missing, before the tyre comes off.']),
                   ('When do you need to program a sensor?', ['Only when you fit a programmable (universal) sensor. These leave the box blank, so the tool writes the protocol for that make and model into them. You can either copy the ID of the old sensor, so the car accepts it without a relearn, or create a new ID, which then has to be relearned. A sensor bought for one specific car usually comes ready and needs no programming.']),
                   ('What is a TPMS relearn?', ['The car\'s TPMS module only listens for the sensor IDs it has stored. After a new sensor with a new ID is fitted, or the wheels are rotated on cars that track wheel position, the module has to learn the new IDs and positions. Depending on the car, that happens in one of three ways:'],
                    [('Automatic relearn', 'the car learns the IDs by itself after a short drive.'),
                     ('Stationary relearn', 'the car is put into learn mode and each sensor is triggered with the tool, wheel by wheel.'),
                     ('OBD relearn', 'the tool writes the sensor IDs into the module through the OBD port.')]),
                   ('What about indirect TPMS?', ['Some cars have no pressure sensors in the wheels. Indirect systems compare wheel speeds from the ABS sensors, so there is nothing to activate or program: after inflating the tyres to the right pressure, the system is reset from the car\'s menu or a button, following the carmaker\'s steps.']),
                   ('What should a workshop TPMS tool do?', ['Check that it can activate sensors for the makes you see, read sensor status and battery, program the programmable sensors you stock, and run OBD relearns for cars that need them. CSKA supplies the Autel MaxiTPMS TS508WF, which activates sensors, checks the system, programs Autel MX-sensors and runs relearns, and the THINKCAR THINKTOOL Master X2, whose built-in TPMS module activates, programs and relearns sensors.'])],
         faqs=[('Do I need to relearn TPMS after rotating tyres?', 'On cars whose TPMS shows each wheel\'s position, yes, so the readings appear on the right wheel. On cars that only show a general warning, the IDs have not changed, so no relearn is needed. Check the carmaker\'s procedure.'),
               ('Why is the TPMS light still on after changing a sensor?', 'Usually because the car has not learned the new sensor ID yet. Run the relearn for that car, or copy the old sensor\'s ID when programming a universal sensor.'),
               ('Can one tool program sensors from any brand?', 'No. A TPMS tool programs the programmable sensors it is built for. The Autel MaxiTPMS TS508WF, for example, programs Autel MX-sensors.')]),
    # Daily article 21 Oct 2026 (catch-up for the missed odd day; queue #3). General programming knowledge; product facts only from the
    # battery page (THINKPPS 150). No prices, no hours, no "authorised" brand claim, no customer workshops.
    dict(slug='programming-power-supply-explained', photo='thinkcar-trolley-thinkpps', products=['battery-testers-and-jump-starters'],
         date='2026-10-21', date_text='21 October 2026',
         title='Programming Power Supply: What It Does and When You Need One',
         desc='Why a car needs steady voltage during ECU programming, how a programming power supply differs from a battery charger, and when a workshop needs one.',
         h1='What a programming power supply does and when you need one',
         answer='A programming power supply holds the car\'s 12V system at a steady voltage while a module is being flashed or coded. During programming the ignition is on and many modules are awake, so a battery alone can sag, and a voltage drop can interrupt the download and leave a module unusable. You need one whenever you flash or code modules, or leave a car on for a long update.',
         sections=[('Why does voltage matter during programming?', ['Programming a module can take from a few minutes to well over an hour. For that time the ignition is on, control modules are awake and the car is drawing current, but the engine is not running, so nothing is charging the battery. As the battery drains, voltage falls. Many modules and scan tools stop the job below a set voltage, and if the download is interrupted halfway, the module can be left with incomplete software and may need recovery or replacement.']),
                   ('How is it different from a battery charger?', ['A workshop charger is built to charge a battery, and its output follows the battery through charging stages. A programming power supply is built to hold a set voltage and supply current as the car\'s load changes, with or without a battery connected. For flashing, steady voltage matters more than charging speed.']),
                   ('When do you need one?', ['Use a stable supply whenever the job is long or the cost of failure is high:'],
                    [('Module programming', 'flashing new software into an ECU, TCU or body module.'),
                     ('Online programming and J2534 jobs', 'files download during the job and the car stays awake throughout.'),
                     ('Coding and module replacement', 'especially on cars that wake many modules at once.'),
                     ('Long updates and tests', 'any time the ignition must stay on for an extended period.')]),
                   ('How do you connect and use it?', ['Follow the carmaker\'s and tool maker\'s procedure for the car in front of you. In general: connect the supply to the battery or the car\'s jump-start points before you start the job, switch off lights and other loads, close the doors, keep the scan tool\'s cable and Wi-Fi connection stable, and do not disconnect anything until the tool says the programming is finished. Voltage targets differ by carmaker, so use the figure in the procedure, not a rule of thumb.']),
                   ('What should you look for in one?', ['Check the output current is enough for a modern car with many modules awake, that voltage stays steady as the load changes, and that it can also help in the bay in other ways. The THINKCAR THINKPPS 150 that CSKA supplies is described as providing stable power for module programming, with fast charging for AGM, GEL and EFB batteries, battery activation and repair, a 400A jump start and exhibition mode.'])],
         faqs=[('Can I just leave a battery charger connected while programming?', 'It is better to use a supply made for programming. A charger is designed to charge a battery, not to hold a steady voltage as the car\'s load changes, so check what the carmaker and the tool maker require.'),
               ('Do I need a power supply for a short coding job?', 'Short jobs carry less risk, but a low battery can still stop a job part-way. Many workshops connect a supply for every programming or coding job so they never have to wonder.'),
               ('What happens if voltage drops during programming?', 'The tool may stop the job, or the download may be interrupted. Depending on the module, that can leave it without working software until it is recovered or replaced, which is why a stable supply is worth connecting first.')]),
    # Night article 23 Oct 2026 (odd day; queue #7). General leak-testing knowledge; product facts only from the workshop-tools page (THINKCAR PLD 212).
    # No prices, no hours, no "authorised" brand claim, no customer workshops, no cross-link.
    dict(slug='smoke-leak-testing-vacuum-evap', photo='pld-212-smoke-test', products=['workshop-tools'],
         date='2026-10-23', date_text='23 October 2026',
         title='Smoke Leak Testing: Finding Vacuum and EVAP Leaks',
         desc='How smoke leak testing finds vacuum, intake and EVAP leaks, what to check before you start, and what a workshop should look for in a smoke leak detector.',
         h1='Smoke leak testing: finding vacuum and EVAP leaks faster',
         answer='A smoke leak test fills the intake, vacuum or EVAP system with visible, harmless smoke at low pressure, and smoke streaming out shows exactly where the leak is. It is faster than guessing at hoses, and it works on leaks too small to hear or spray-test. Use only the pressure the carmaker allows, especially on EVAP systems.',
         sections=[('What does a smoke leak test find?', ['Smoke follows air, so it comes out wherever air could get in or out. Workshops use it on the intake and vacuum side, where an unmetered air leak upsets the air-fuel mixture and can set lean codes or a rough idle, and on EVAP systems, where a small leak can set an evaporative emission code. It can also trace some oil and boost leaks, depending on the machine.']),
                   ('How is it better than spraying or listening?', ['Spraying a flammable cleaner around the engine to hear the idle change is slow, unsafe around hot parts and only finds leaks you can reach. A small EVAP leak makes no sound at all. With smoke you see the leak directly, including on hoses and seals that are hidden behind other parts, so you can go to the fault instead of replacing parts to see if it helps.']),
                   ('How is a smoke test done?', ['Follow the carmaker\'s procedure and the machine maker\'s instructions for the car in front of you. In general:'],
                    [('Read the codes first', 'a lean code, an EVAP code or a rough idle tells you which system to test.'),
                     ('Seal the system', 'block the intake or the vent as the procedure says, so smoke can only escape through the leak.'),
                     ('Connect at the right point', 'use the adapter or hose for that system, such as the intake, a vacuum line or the EVAP service port.'),
                     ('Apply smoke at low pressure', 'let the system fill, then look along hoses, joints, seals and valves for a thin stream of smoke. A torch or UV light helps in a dark engine bay.'),
                     ('Fix, then test again', 'repair the leak, clear the code and confirm that no smoke escapes.')]),
                   ('Why does pressure matter on EVAP systems?', ['Fuel vapour systems are low-pressure systems, and tanks and sensors can be damaged if they are over-pressurised. Many carmakers specify a very low test pressure for EVAP. Always use the figure in the carmaker\'s procedure and a tool that lets you control and read the pressure and flow, rather than connecting the highest output to every system.']),
                   ('What should you look for in a smoke leak detector?', ['Check that it has a built-in pump, a pressure gauge and a flow meter, that it has adapters to seal and connect to the systems you test, and that it can be used with the scan tool you already own. The THINKCAR PLD 212 that CSKA supplies is described as finding air, vacuum and oil leaks, with a built-in pump, 13 to 16 PSI output, 8 to 15 L/min flow, and a pressure gauge and flow meters. It also works with THINKCAR scan tools on leak-related faults. Ask CSKA which adapters and settings suit the systems you test.'])],
         faqs=[('Is the smoke harmful to the engine or sensors?', 'Smoke machines are designed to produce a harmless smoke for this job, but follow the maker\'s instructions and the carmaker\'s procedure. Use the right fluid for the machine, and never apply more pressure than the system allows.'),
               ('Can I smoke test a running engine?', 'Normally the test is done with the engine off, as the procedure for the car says. Test the intake and vacuum system with the engine off and the system sealed, so the smoke stays in the leak path.'),
               ('Does a lean code always mean a vacuum leak?', 'No. A lean code can also come from a weak fuel pump, a dirty injector or a faulty air flow sensor. A smoke test rules a leak in or out, so you do not replace parts you do not need to.')]),
    # Night article 25 Oct 2026 (odd day; queue #5). General lift knowledge; product facts only from the lifts-and-jacks page (4-ton two-post lifts, top-connection models).
    # No prices, no hours, no "authorised" brand claim, no customer workshops, no cross-link. Does not claim CSKA supplies four-post lifts.
    dict(slug='two-post-vs-four-post-lift-workshop', photo='tfj-330-jack', products=['lifts-and-jacks'],
         date='2026-10-25', date_text='25 October 2026',
         title='Two-Post vs Four-Post Lift for a Workshop Unit',
         desc='Two-post or four-post car lift? How access, floor space, ceiling height, floor strength and the jobs you do decide which lift suits a small workshop unit in Singapore.',
         h1='Two-post lift or four-post lift for a Singapore workshop unit?',
         answer='Choose a two-post lift if most of your jobs need the wheels, suspension, brakes or underbody free, because it gives the best access in the smallest floor area. Choose a four-post lift if you mainly do alignment, long exhaust or oil work, or want to store a car above another. Before you decide, check your ceiling height, floor strength and bay width with the lift maker.',
         sections=[('What is the main difference?', ['A two-post lift has two columns and four swing arms that lift the car by its lifting points, so the wheels hang free. A four-post lift is a drive-on platform: the car rides up on its tyres on two runways. That one difference decides most of the rest.']),
                   ('Which gives better access?', ['A two-post lift leaves the wheels, brakes, suspension and drivetrain open to the technician, which suits general repair, brake, suspension, gearbox and engine work. A four-post lift holds the car by its tyres, so wheel and suspension work needs jacks or a sliding bridge jack on top of the runways. It suits oil changes, exhaust work and wheel alignment, where the wheels must stay on the runways.']),
                   ('Which suits a small workshop unit?', ['A two-post lift takes less floor area and you can often work around the car from all sides. A four-post lift needs a longer, wider footprint for the runways and for driving on and off. Measure the bay before you choose, and leave room to open the car doors and move a tool trolley.']),
                   ('What should you check before buying either?', ['Ask the supplier to confirm each of these for your unit and for the lift model:'],
                    [('Ceiling height', 'the lift, the tallest car you service and the fully raised height must fit with room to spare. Check beams, lights and roller shutters too.'),
                     ('Floor', 'a two-post lift is usually fixed to the floor with anchor bolts, so the slab thickness and strength matter. Follow the lift maker\'s requirements.'),
                     ('Capacity', 'match the lift to the heaviest vehicle you will lift, including SUVs and vans, and read the maker\'s capacity and arm-reach limits.'),
                     ('Power and set-up', 'check the power supply the lift needs and who installs and tests it.'),
                     ('Inspection and safety', 'ask the supplier for the maker\'s inspection and servicing requirements, and follow the workplace safety rules that apply to your premises.')]),
                   ('Which should a new workshop start with?', ['Most general repair workshops start with a two-post lift, because it handles the widest range of jobs in the least space. A four-post lift is usually added later for alignment or storage if the work calls for it. CSKA supplies 4-ton two-post lifts, including top-connection models with a one-side lock, as part of new workshop set-ups. Tell CSKA your floor space and the vehicles you work on, and ask what suits your unit.'])],
         faqs=[('Can I do wheel and brake work on a four-post lift?', 'Yes, but the wheels sit on the runways, so you need a bridge jack or jacks to lift the wheels off. A two-post lift leaves the wheels free without extra equipment.'),
               ('Is a two-post lift safe for heavy cars?', 'It is safe when it is rated for the weight, the arms are placed at the carmaker\'s lifting points and the safety locks are engaged. Check the lift\'s rated capacity against the heaviest vehicle you will lift.'),
               ('What if my unit has a low ceiling?', 'Tell the supplier the clear height before you buy. Lift heights and column heights differ by model, and the answer depends on the tallest car you service.')]),
    # Night article 27 Oct 2026 (odd day; queue #6). General ADAS knowledge; product facts only from the adas-calibration page (Autel MaxiSys ADAS package, MS909 S2 upgrade).
    # No prices, no hours, no "authorised" brand claim, no customer workshops, no cross-link. Does NOT claim CSKA offers calibration as a service (README CONFIRM #7: tools only).
    dict(slug='adas-calibration-after-windscreen-replacement', photo='handover-ms908s-ii-c', products=['adas-calibration'],
         date='2026-10-27', date_text='27 October 2026',
         title='ADAS Calibration After Windscreen Replacement: Workshop Guide',
         desc='Why a windscreen replacement can need ADAS camera calibration, static versus dynamic calibration, and what a Singapore workshop needs in space, targets and software.',
         h1='What does a workshop need for ADAS calibration after a windscreen replacement?',
         answer='Many cars have a forward camera mounted on the windscreen, so replacing the glass can change what the camera sees. Carmakers usually require the camera to be calibrated afterwards, either with targets in the workshop (static), on a road drive (dynamic), or both. A workshop needs a level, well-lit bay, the right targets and frame, calibration software and the carmaker\'s procedure for each car.',
         sections=[('Why does a windscreen replacement affect ADAS?', ['The camera for lane departure warning, automatic emergency braking and similar systems often sits behind the windscreen and looks through it. A new windscreen is never fitted at exactly the same angle to the micron, so the camera\'s view shifts slightly. Calibration tells the system where "straight ahead" is again. Many carmakers ask for it after a windscreen replacement, and the workshop should follow the procedure for the car in front of it.']),
                   ('Which other jobs can need ADAS calibration?', ['Windscreen work is the best-known trigger, but the carmaker\'s procedure may also call for calibration after:'],
                    [('Bumper or grille repair', 'radars and sensors behind or in the bumper can be knocked out of position.'),
                     ('Wheel alignment or suspension work', 'a changed thrust angle changes where the car points relative to the camera.'),
                     ('Camera or radar removal or replacement', 'the unit must be taught its new position.'),
                     ('Collision repair', 'body repairs near a sensor can change its mounting angle.')]),
                   ('What is the difference between static and dynamic calibration?', ['Static calibration is done in the workshop: the car sits on a level floor and the camera is aimed at calibration targets placed on a frame at distances the carmaker specifies. Dynamic calibration is done on the road: the technician drives the car at set speeds on well-marked roads while the scan tool guides the process. Some cars need one method, some need both. The carmaker\'s procedure says which, so check it before quoting the job.']),
                   ('What does a workshop need to do it properly?', ['Ask your supplier to confirm each item for the cars you service:'],
                    [('Space and floor', 'a level, flat area large enough to place the frame and measure the distances the procedure calls for.'),
                     ('Lighting', 'even lighting without glare or strong reflections on the targets.'),
                     ('Targets and frame', 'the target set for the systems you calibrate, such as lane departure, surround view, rear radar, blind spot and night vision.'),
                     ('Software and scan tool', 'ADAS calibration software that matches the car brands you service, kept up to date.'),
                     ('The carmaker\'s procedure', 'the vehicle conditions it asks for, such as tyre pressure, fuel level and an alignment check, before you start.')]),
                   ('What does CSKA supply for ADAS calibration?', ['CSKA supplies the Autel MaxiSys ADAS Complete Calibration Package to Singapore workshops. It includes the standard calibration frame, the LDW calibration package, the AVM-RCW-BSD-NV calibration kit, ADAS software and the Autel MS908P complete set. The Autel MS909 S2 tablet can also be upgraded for ADAS calibration with software and the target package. Tell CSKA the car brands and systems you want to cover, and ask which targets and software they need.'])],
         faqs=[('Do all cars need ADAS calibration after a windscreen replacement?', 'No. It depends on the car and on whether it has a camera or sensor behind the glass. The carmaker\'s procedure for that model says whether calibration is required and which method to use.'),
               ('Can I calibrate with the car on the road instead of in the workshop?', 'Dynamic calibration is done on the road, but it needs suitable roads, speeds and lane markings, and some cars need static calibration as well. Follow the carmaker\'s procedure for the car.'),
               ('Is a wheel alignment needed before calibration?', 'Often the procedure asks for the alignment to be correct first, because the camera is aimed relative to the direction the car travels. Check the procedure for the model.'),
               ('Can I add ADAS calibration to the scan tool I already own?', 'The Autel MS909 S2 can be upgraded for ADAS calibration with software and the ADAS target package. WhatsApp CSKA your tablet model to find out what you need.')]),
    # Night article 29 Oct 2026 (odd day; queue #8). General battery-testing knowledge; product facts only from the battery-testers-and-jump-starters page (TBT 360 / 360 Pro, TOPDON BT600).
    # No prices, no hours, no "authorised" brand claim, no customer workshops, no cross-link.
    dict(slug='battery-tester-report-cca-state-of-health', photo='handover-v4500', products=['battery-testers-and-jump-starters'],
         date='2026-10-29', date_text='29 October 2026',
         title='Battery Tester Report: CCA and State of Health Explained',
         desc='How to read a car battery tester report: what CCA, state of health and state of charge mean, and how a workshop can explain the result to the customer.',
         h1='Battery tester reports explained: what CCA and State of Health tell your customer',
         answer='A battery tester report compares the battery\'s measured cold cranking amps (CCA) with its rated CCA, gives a state of health (SOH) percentage, and shows how charged it is right now. Read all three together: a battery can have good voltage and still be too weak to start the car reliably. Charge a low battery first, then test again.',
         sections=[('What does a battery tester report show?', ['Most reports list the battery type and rating you entered, the voltage, the measured CCA, a state of health (SOH) percentage, the state of charge, and a verdict such as good, recharge and retest, or replace. The exact wording differs by tester, so read the tester\'s own guide for what each verdict means.']),
                   ('What is CCA?', ['Cold cranking amps is the current a 12V battery can deliver for a short, set time at a low test temperature while holding its voltage above a minimum level. The rated CCA is printed on the battery label and is the maker\'s figure for a new battery. Different standards (SAE, EN, DIN and others) use different test methods, so the same battery can show different numbers. Always set the tester to the standard printed on the label.']),
                   ('What is the difference between state of health and state of charge?', ['State of charge says how full the battery is right now. State of health says how much of its original ability to deliver current is left, and it falls with age, heat and repeated deep discharge. A flat battery with a good SOH can be recharged and used again. A fully charged battery with a poor SOH will still struggle to start the engine. That is why a report shows both.']),
                   ('How do you read a report for the customer?', ['Walk through it in this order:'],
                    [('Check the entries', 'the battery type and CCA rating on the report must match the label, or the verdict will be wrong.'),
                     ('Look at the state of charge', 'if the battery is low, charge it and test again before judging it.'),
                     ('Compare measured CCA with rated CCA', 'a measured figure far below the rating means the battery has lost power.'),
                     ('Read the SOH', 'a low percentage means the battery is ageing even if it still starts the car today.'),
                     ('Test the starter and charging system', 'a weak battery is sometimes the symptom of a faulty alternator or a drain, so check these before selling a new battery.')]),
                   ('Why print the report?', ['A printed report gives the customer a record of the test on the day, in numbers, instead of a verbal opinion. It also helps the workshop explain why a battery needs replacing, or why it does not, and gives you something to compare against at the next service.']),
                   ('Which battery testers does CSKA supply?', ['CSKA supplies the THINKCAR TBT 360 and TBT 360 Pro, which test batteries from 3 to 360 Ah plus the charging and starting system, with the Pro printing reports. It also supplies the TOPDON BT600, a 12V tester with a 3.5-inch colour screen and a built-in thermal printer that measures real cold cranking amps and state of health. Tell CSKA the batteries you test most and ask which tester suits your workshop.'])],
         faqs=[('Can a battery with good voltage still be weak?', 'Yes. Voltage mostly shows how charged the battery is. A worn battery can read normal voltage at rest and still drop sharply when the starter pulls current, which is why CCA and SOH are measured under load.'),
               ('Should I charge a battery before testing it?', 'If the state of charge is low, charge it first and test again, as the tester\'s instructions say. A discharged battery can show a poor result that a recharge would improve.'),
               ('Do AGM and EFB batteries need different settings?', 'Testers usually ask you to choose the battery type and the rating standard. Select what is printed on the battery label, because the wrong type can give a wrong verdict.'),
               ('Is a low SOH always a reason to replace the battery?', 'Not by itself. Read it together with the state of charge, the measured CCA against the rating, and the starter and charging checks, then decide with the customer.')]),
    # Night article 31 Oct 2026 (odd day; queue #10). General scan-tool knowledge; product facts only from the support page (Autel states one year of free updates for the MS909 S2) and the scanner pages.
    # No prices, no hours, no "authorised" brand claim, no customer workshops, no cross-link. Own share image share/<slug>.jpg (JPG).
    dict(slug='scan-tool-software-subscription-ends', photo='handover-master-x2', products=['diagnostic-scanners'], share=True,
         date='2026-10-31', date_text='31 October 2026',
         title='Scan Tool Software Update Subscription Ends: What Happens?',
         desc='What a workshop scan tool can and cannot do when its free software update period ends, what to check before it runs out, and how to plan renewal.',
         h1='What happens to a scan tool when the software update subscription ends?',
         answer='In general the tool keeps working with the software already installed, so you can still read codes and run the functions you had. What stops is new software: coverage for newer cars, fixes and added functions. Each maker sets its own terms, so check your model\'s update end date and what renewal covers before it expires.',
         sections=[('Does the scan tool stop working when the subscription ends?', ['Usually no. The software on the tool at the end of the update period stays on it. The change is that the tool no longer receives new versions. Some online functions can depend on a current subscription, and the rules differ between makers and models, so read the terms for your tool rather than assume.']),
                   ('What do you lose without updates?', ['A workshop feels the gap on newer cars and newer systems rather than on the cars it already services:'],
                    [('Newer model years', 'cars released after your last update may not be listed or may have fewer systems covered.'),
                     ('Fixes', 'bugs found after your last update stay in your version.'),
                     ('New functions', 'added service resets, tests or coding options reach you only with a current update.'),
                     ('Protocol support', 'newer communication standards such as DoIP and CAN FD arrive through updates, so a tool that is not kept current falls behind as these cars become more common.')]),
                   ('What should you check before the period runs out?', ['Do these while the subscription is still active:'],
                    [('The end date', 'find it in the tool\'s settings or account page, or ask your supplier.'),
                     ('What renewal covers', 'ask whether it is all brands or only some, and whether it covers any online programming or extra modules you use.'),
                     ('Your own car mix', 'if most of your work is on older cars, you may need updates less often than a workshop that services new models every week.'),
                     ('A backup plan', 'note which jobs you could not do on an out-of-date tool, such as a model-year gap, so you can decide with facts.')]),
                   ('How do makers handle this?', ['Each maker sets its own update terms. For example, Autel states one year of free software updates and a one-year limited warranty for the MaxiSYS MS909 S2. After that, ask for the renewal for your model. THINKCAR, TOPDON and the other makers have their own terms, so confirm yours instead of using another maker\'s as a guide.']),
                   ('Who do you ask at CSKA?', ['For tools bought from CSKA, WhatsApp Steven on 9822 2629 or Ah Kiat on 8493 0068 for the renewal for your model, and Alvis on 9037 2820 for technical questions. Send the model and serial number, or a photo of the label.'])],
         faqs=[('Can I still use my scan tool after the free update period ends?', 'Generally the tool keeps the software it already has. Check the terms for your model, because online functions and some features can depend on a current subscription.'),
               ('How often should a workshop renew software updates?', 'It depends on your cars. A workshop that services recent models every week needs current coverage more than one that works mostly on older cars. Compare the jobs you turn away with what renewal covers.'),
               ('How do I renew updates for a tool I bought from CSKA?', 'Ask Steven or Ah Kiat for the renewal for your model. Update terms are set by each maker.'),
               ('Is the renewal the same for every brand?', 'No. THINKCAR, Autel, TOPDON and other makers set their own terms, so ask for the terms for your own model.')]),
    # Night article 2 Nov 2026 (even day, requested; queue #9). General hybrid-aircon knowledge with one linked source (Delphi Technologies); product fact only from the aircon page (SPZ-FA1 lets you choose PAG or POE oil).
    # No prices, no hours, no "authorised" brand claim, no customer workshops, no cross-link, no SP ZONE facts beyond the aircon page. Own share image share/<slug>.jpg (JPG).
    dict(slug='hybrid-car-aircon-service-poe-oil', photo='aircon-machine-demo', products=['aircon-service-machines'], share=True,
         source=('Delphi Technologies: Servicing air conditioning on hybrid vehicles', 'https://delphiautoparts.com/en-gb/mom/how-to/servicing-air-conditioning-on-hybrid-vehicles'),
         date='2026-11-02', date_text='2 November 2026',
         title='Hybrid Car Aircon Service: Why POE Oil Matters',
         desc='Why hybrid cars with an electric aircon compressor need POE oil, what goes wrong if PAG oil gets in, and how a workshop avoids mixing the two.',
         h1='Hybrid car aircon service: why POE oil matters and how to avoid mixing it with PAG',
         answer='Many hybrid cars use an electric aircon compressor whose motor windings sit in the oil, so the oil must not conduct electricity. POE oil is insulating; PAG oil is not. Putting PAG into a hybrid system can reduce the compressor\'s insulation and cause a fault. Always use the oil the carmaker specifies, and keep PAG out of the equipment you use on hybrids.',
         sections=[('Why does a hybrid aircon need a different oil?', ['In a conventional car the aircon compressor is turned by the engine belt. Many hybrids use an electric compressor instead, driven by a high-voltage motor, so the aircon can run with the engine off. The motor\'s windings are in contact with the compressor oil, which therefore has to be a good electrical insulator as well as a lubricant.']),
                   ('What is the difference between PAG and POE oil?', ['PAG is the common oil in belt-driven compressors. POE (polyolester) oil is the type specified for hybrid electric compressors because it insulates. Delphi Technologies states that as little as one percent of PAG oil in a hybrid system can affect its insulating properties, and that some carmakers require the parts to be replaced after cross-contamination. Never assume two oils are interchangeable: the carmaker\'s specification decides, including the viscosity.']),
                   ('What goes wrong if the wrong oil gets in?', ['Contaminated oil can lower the insulation between the compressor motor and the housing. The system can detect the leak and shut the compressor down, and the car may show an aircon fault. In the worst case a damaged compressor has to be replaced. High-voltage components should only be worked on by technicians trained for them, following the carmaker\'s procedure.']),
                   ('How does a workshop avoid mixing the oils?', ['Treat hybrid work as a separate process:'],
                    [('Check the label or manual', 'find the specified oil and refrigerant for that exact car before you start.'),
                     ('Use a machine and oil injection that suit hybrids', 'the oil you add must be POE, and nothing that has held PAG should touch a hybrid system.'),
                     ('Keep the tools separate', 'use clearly labelled hoses, injectors and containers for PAG and for POE.'),
                     ('Do not top up from memory', 'add the amount the procedure gives, and record what you used.')]),
                   ('Which CSKA aircon machine lets you choose POE oil?', ['The SP ZONE SPZ-FA1 lets you choose PAG oil or POE oil for hybrid compressors. For which machine fits your workshop, WhatsApp CSKA with the cars you service.'])],
         faqs=[('Can I use PAG oil in a hybrid car?', 'Not if the carmaker specifies POE for the electric compressor. PAG does not insulate, so it can affect the compressor motor. Follow the specification for that car.'),
               ('How do I know which oil a hybrid needs?', 'Check the compressor or under-bonnet label and the carmaker\'s service information for that model. Do not rely on another car\'s specification.'),
               ('Does every hybrid use POE oil?', 'No. It depends on whether the car has an electric compressor and on the carmaker, so always read the specification for the exact model.'),
               ('Can one machine service both normal and hybrid cars?', 'Only if it lets you choose the oil and you keep PAG out of the hybrid circuit. The SPZ-FA1 lets you select PAG or POE oil.')]),
]
# Per-page lastmod (sitemap, WebPage dateModified): daily articles carry their own date; pages they change are listed by hand.
LASTMOD = {'articles/%s/' % a['slug']: a['date'] for a in ARTICLES if a.get('date')}
# Guides lists show the newest article first (Edwin, 20 Oct 2026); same-date articles keep their list order.
ARTICLES_NEWEST = sorted(ARTICLES, key=lambda x: x.get('date', UPDATED), reverse=True)
LASTMOD.update({'': '2026-11-02', 'articles/': '2026-11-02', 'products/adas-calibration/': '2026-10-31', 'products/ev-diagnostic-tools/': '2026-10-30', 'products/lifts-and-jacks/': '2026-10-29', 'products/workshop-tools/': '2026-11-02', 'products/tpms-and-tyre-tools/': '2026-10-27', 'products/diagnostic-scanners/': '2026-10-25', 'products/battery-testers-and-jump-starters/': '2026-11-01', 'brands/thinkcar/': '2026-10-23', 'brands/topdon/': '2026-10-26', 'brands/sp-zone/': '2026-10-28',
                'products/aircon-service-machines/': '2026-10-25', 'brands/autel/': '2026-10-25', 'about/': '2026-10-25'})  # 25 Oct: Booster (scanners, aircon, Autel) + authorised wording removed (about, llms.txt)

# ----------------------------------------------------------------------------------------------
# Page bodies
# ----------------------------------------------------------------------------------------------
def prd_card(p):
    return '<a class="scard" href="products/%s/"><figure>%s</figure><span class="scard-t"><b>%s</b><span>%s</span><em>More details →</em></span></a>' % (
        p['slug'], img(p['photo']), E(p['short']), E(p['gist']))


def brand_card(b):
    return '<a class="scard" href="brands/%s/"><figure>%s</figure><span class="scard-t"><b>%s</b><span>%s</span><em>More details →</em></span></a>' % (
        b['slug'], img(b['photo']), E(b['name']), E(b['gist']))


def article_card(a):
    return '<a class="acard" href="articles/%s/"><figure>%s</figure><span><b>%s</b><em>Read the guide →</em></span></a>' % (a['slug'], img(a['photo']), E(a['h1']))


def people_html(topic='tools for my workshop.'):
    return '<div class="people">%s</div>' % ''.join(
        '<div class="person"><b>%s</b><span>%s · +65 %s</span><p class="small">%s</p>%s</div>' % (E(n), E(r), s, E(note), wa_btn('WhatsApp ' + n.split(' (')[0].split(' ')[0] if '(' not in n else 'WhatsApp ' + n.split('(')[1].rstrip(')'), topic, num=num))
        for n, r, num, s, note in PEOPLE)


def product_body(p):
    others = [x for x in PRODUCTS if x['slug'] != p['slug']]
    related = [a for a in ARTICLES if p['slug'] in a['products']]
    brands = [b for b in BRANDS if any(sl == p['slug'] for _, sl in b['lines'])]
    rel = ''
    if related:
        rel = '<h2>Guides</h2><ul class="links">%s</ul>' % ''.join('<li><a href="articles/%s/">%s</a></li>' % (a['slug'], E(a['h1'])) for a in related)
    br = ''
    if brands:
        br = '<p>Brands on this page: %s.</p>' % ', '.join('<a href="brands/%s/">%s</a>' % (b['slug'], E(b['name'])) for b in brands)
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">{E(p['answer'])}</p>
<h2>What we supply</h2>
{models_html(p['models'])}{p.get('extra', '')}
{br}
<p class="small">Model details are the makers' own descriptions as posted by CSKA. Ask us to confirm current versions and what comes in the box.</p>
</article>
<aside class="side"><div class="card sticky"><h2>Ask for a quote</h2><p>Tell us the model you want, or the cars and jobs it is for.</p>{wa_btn('WhatsApp +65 ' + WA_SHOW, p['short'].lower() + '.')}<a class="btn btn-ghost" href="handovers/">See recent handovers</a></div></aside>
</div>
<div class="wrap"><div class="sec-head row"><h2>Recent handovers</h2><a href="handovers/">All photos →</a></div></div>
{glide(p['gallery'], 'glide glide-md')}
<div class="wrap split"><article class="prose">
<h2>How buying from CSKA works</h2>
{steps(HOW)}
<h2>Questions</h2>
{faq_html(p['faqs'])}
{rel}
</article><div></div></div>
</section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><p class="eyebrow">Also from CSKA</p><h2>Other products</h2></div>
<div class="svc-grid">{''.join(prd_card(x) for x in others[:4])}</div></div></section>'''


def brand_body(b):
    lines = ''.join('<li><a href="products/%s/">%s</a> <span class="small">(%s)</span></li>' % (sl, E(t), E(PRD[sl]['short'])) for t, sl in b['lines'])
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">{E(b['answer'])}</p>
<h2>{E(b['name'])} products we supply</h2>
<ul class="links">{lines}</ul>{b.get('extra', '')}
<h2>Questions</h2>
{faq_html(b['faqs'])}
</article>
<aside class="side"><div class="card sticky"><h2>Ask about {E(b['name'])}</h2><p>Model, price and stock: one WhatsApp message.</p>{wa_btn('WhatsApp +65 ' + WA_SHOW, b['name'] + ' tools.')}<a class="btn btn-ghost" href="brands/">All brands</a></div></aside>
</div>
<div class="wrap"><div class="sec-head row"><h2>{E(b['name'])} handovers</h2><a href="handovers/">All photos →</a></div></div>
{glide(b['gallery'], 'glide glide-md')}
</section>'''


HOW = [('Tell us what you need', 'WhatsApp the model, or the cars and jobs it is for. Steven, Ah Kiat or Alvis will reply.'),
       ('Get advice and a quote', 'We suggest the right model and send a quotation.'),
       ('Delivery and handover', 'We deliver to your workshop and hand the tool over in person.'),
       ('Help after you buy', 'Technical questions go to Alvis, our Technical Executive.')]


def article_body(a):
    parts = ['<p class="answer">%s</p>' % E(a['answer'])]
    for sec in a['sections']:
        parts.append('<h2>%s</h2>' % E(sec[0]))
        if sec[1]:
            parts += ['<p>%s</p>' % E(t) for t in sec[1]]
        if len(sec) > 2:
            parts.append(ticks(sec[2]))
    links = ''.join('<li><a href="products/%s/">%s</a></li>' % (sl, E(PRD[sl]['short'])) for sl in a['products'])
    if a.get('source'):
        parts.append('<p class="small">Source: <a href="%s" rel="noopener" target="_blank">%s</a> (read %s).</p>' % (E(a['source'][1]), E(a['source'][0]), a.get('date_text', UPDATED_TEXT)))
    parts.append('<h2>Questions</h2>' + faq_html(a['faqs']))
    parts.append('<div class="card note"><h2>Talk to CSKA</h2><p>Tell us the cars you service and the jobs you do, and we will suggest the right tool.</p>%s<ul class="links">%s</ul></div>' % (wa_btn('WhatsApp +65 ' + WA_SHOW), links))
    return '''<section class="sec"><div class="wrap narrow"><article class="prose">
<figure class="lead-fig">%s</figure>
<p class="byline">By CSKA Auto Enterprise · Updated %s</p>
%s
</article></div></section>''' % (img(a['photo'], eager=True), a.get('date_text', UPDATED_TEXT), '\n'.join(parts))


def article_schema(a, path):
    return {'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'url': SITE + path, 'datePublished': a.get('date', UPDATED), 'dateModified': a.get('date', UPDATED),
            'image': (SITE + 'share/%s.jpg' % a['slug']) if a.get('share') else (IMG_ABS or SITE + IMG) + a['photo'] + '.webp', 'author': {'@type': 'Organization', 'name': NAME, 'url': SITE},
            'publisher': {'@id': SITE + '#business'}, 'mainEntityOfPage': SITE + path}


FAQ_HOME = [
    ('What does CSKA Auto Enterprise sell?', 'CSKA Auto Enterprise supplies car workshops in Singapore with diagnostic scanners, EV, TPMS and ADAS tools, aircon service machines, battery testers and jump starters, lifts and jacks, and workshop tools, from brands including THINKCAR, Autel, TOPDON and SP ZONE.'),
    ('Who do you supply?', 'Car workshops, tyre and battery shops, aircon specialists and other motor trade businesses in Singapore. We are a business-to-business supplier.'),
    ('Where are you?', 'At 101 Woodlands Avenue 12, #07-03B, Polaris @ Woodlands, Singapore 737719. We deliver to workshops across Singapore.'),
    ('How do I get a quote?', 'WhatsApp Steven on 9822 2629 or Ah Kiat on 8493 0068 with the model you want, or the cars and jobs it is for. Technical questions go to Alvis on 9037 2820.'),
]

HERO_GLIDE = ['handover-ms908s-ii', 'handover-aircon-machine', 'handover-expert-391', 'handover-v4500', 'handover-master-x2', 'handover-ts508wf', 'handover-thinktool-se-trolley',
              'spz6000-in-use', 'handover-lite-2', 'handover-phoenix-elite', 'handover-tool-trolley', 'handover-sg-garage']
HERO_CAPS = ['Autel MaxiSys', 'SP ZONE aircon machine', 'THINKTOOL Expert 391', 'TOPDON V4500 Plus', 'THINKTOOL Master X2', 'Autel MaxiTPMS TS508WF', 'THINKTOOL SE and tool cart',
             'SP ZONE SPZ6000', 'THINKTOOL Lite 2', 'TOPDON Phoenix Elite', 'Tool trolley and set', 'THINKTOOL 191']


def home_body():
    brands = ''.join('<li>%s</li>' % E(b) for b in BRAND_NAMES)
    return f'''<section class="hero"><div class="gauge" aria-hidden="true"></div><div class="wrap hero-grid">
<div class="hero-in">
<p class="kicker">Workshop tools &amp; equipment · Singapore</p>
<h1>The tools your workshop runs on, <span>handed over in person.</span></h1>
<p class="lede">CSKA Auto Enterprise supplies car workshops in Singapore with diagnostic scanners, aircon machines, battery tools, lifts and workshop equipment.</p>
<div class="cta-row">{wa_btn('WhatsApp +65 ' + WA_SHOW)}<a class="btn btn-light" href="products/">See products</a></div>
<p class="grating-row">{GBP_LINE}</p>
<ul class="brands" aria-label="Brands we supply">{brands}</ul>
</div>
<figure class="hero-fig">{img('handover-ms908s-ii', eager=True)}<figcaption>Autel MaxiSys handover at a workshop</figcaption></figure>
</div></section>
<section class="sec sec-glide"><div class="wrap sec-head"><p class="eyebrow">Recent handovers</p><h2>Delivered to workshops across Singapore</h2></div>
{glide(HERO_GLIDE, 'glide glide-lg', HERO_CAPS)}
<div class="wrap"><p class="glide-note">Hold or swipe to stop. <a href="handovers/">See all handovers →</a></p></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><p class="eyebrow">Products</p><h2>Everything a workshop bay needs</h2>
<p>Pick a product line for models, photos and questions.</p></div>
<div class="svc-grid">{''.join(prd_card(p) for p in PRODUCTS)}</div></div></section>
<section class="sec sec-dark"><div class="wrap split-2">
<div><p class="eyebrow">How we work</p><h2>From your question to a tool in your hands</h2>
{steps(HOW)}
<div class="cta-row">{wa_btn('Ask for a quote', 'a quote for my workshop.')}</div></div>
<div class="duo"><figure>{img('spz6000-training')}</figure><figure>{img('master-2-in-use')}</figure></div>
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><p class="eyebrow">Brands</p><h2>THINKCAR, Autel, TOPDON, SP ZONE and more</h2></div>
<div class="svc-grid">{''.join(brand_card(b) for b in BRANDS)}</div></div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><p class="eyebrow">Talk to us</p><h2>Three people, one WhatsApp away</h2></div>{people_html()}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><p class="eyebrow">Guides</p><h2>For workshop owners</h2></div>
<div class="rail">{''.join(article_card(a) for a in ARTICLES_NEWEST)}</div></div></section>
<section class="sec sec-alt"><div class="wrap narrow"><div class="sec-head"><h2>Questions</h2></div>{faq_html(FAQ_HOME)}</div></section>'''


HANDOVER_GROUPS = [
    ('Diagnostic scanners', 'diagnostic-scanners', ['handover-thinktool-191', 'handover-sg-garage', 'handover-thinktool-191-b', 'handover-thinktool-191-c', 'handover-thinktool-191-d', 'handover-expert-391',
                                                    'handover-master-x2', 'handover-master-2', 'handover-thinktool-se', 'handover-lite-2', 'handover-phoenix-elite']),
    ('Autel MaxiSys', 'diagnostic-scanners', ['handover-ms908s-ii', 'handover-ms908s-ii-b', 'handover-ms908s-ii-c', 'handover-ms908s-ii-d', 'handover-ms908s-ii-e', 'handover-ms908s-ii-f', 'handover-ms908s3']),
    ('EV tools', 'ev-diagnostic-tools', ['handover-expert-394-ev', 'thinktool-391-box']),
    ('Aircon service machines', 'aircon-service-machines', ['handover-aircon-machine', 'handover-aircon-machine-b', 'spz6000-in-use', 'spz6000-training', 'aircon-machine-demo', 'aircon-machine-team', 'aircon-machine-steven']),
    ('TPMS and tyre tools', 'tpms-and-tyre-tools', ['handover-ts508wf', 'handover-ts508wf-b', 'maxitpms-screen', 'tyre-tread-examiner']),
    ('Battery tools', 'battery-testers-and-jump-starters', ['handover-v4500', 'handover-v4500-b', 'thinkcar-trolley-thinkpps']),
    ('Workshop tools and jacks', 'workshop-tools', ['handover-tool-trolley', 'handover-thinktool-se-trolley', 'pld-212-smoke-test', 'handover-ingersoll-rand', 'tfj-330-jack']),
]


def handovers_body():
    out = ['<section class="sec"><div class="wrap"><p class="answer">Every tool CSKA sells is handed over at the workshop. These photos are from our handover videos, posted on <a href="%s" target="_blank" rel="noopener">Steven\'s</a> and <a href="%s" target="_blank" rel="noopener">Ah Kiat\'s</a> Facebook, where there are more than 170 videos to watch.</p></div>' % (FB_STEVEN + '/reels/', FB_KIAT + '/reels/')]
    for title, sl, names in HANDOVER_GROUPS:
        out.append('<div class="wrap"><div class="sec-head row"><h2>%s</h2><a href="products/%s/">%s →</a></div></div>%s' % (E(title), sl, E(PRD[sl]['short']), glide(names, 'glide glide-md')))
    out.append('</section>')
    return ''.join(out)


def products_index():
    return '<section class="sec"><div class="wrap"><div class="svc-grid">%s</div></div></section>' % ''.join(prd_card(p) for p in PRODUCTS)


def brands_index():
    other = ''.join('<tr><td>%s</td><td>%s</td></tr>' % (E(a), E(b)) for a, b in OTHER_BRANDS)
    return ('<section class="sec"><div class="wrap"><p class="answer">CSKA Auto Enterprise supplies Singapore workshops with THINKCAR, Autel, TOPDON and SP ZONE equipment, '
            'plus Ingersoll Rand and M7 air tools, Lige service tools and Stirling and ThreeBond workshop chemicals.</p>'
            '<div class="svc-grid">%s</div>'
            '<div class="narrow" style="margin-top:40px"><h2>Also supplied</h2><table class="cmp"><tbody>%s</tbody></table></div></div></section>') % (''.join(brand_card(b) for b in BRANDS), other)


def about_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">CSKA Auto Enterprise Pte. Ltd. is a Singapore supplier of diagnostic tools and workshop equipment for car workshops. It sells THINKCAR, Autel, TOPDON and SP ZONE equipment among other brands, delivers each tool to the workshop and hands it over in person, and works from 101 Woodlands Avenue 12, Polaris @ Woodlands.</p>
<figure class="lead-fig">{img('aircon-machine-team', eager=True)}</figure>
<h2>Who we work with</h2>
<p>Our customers are car workshops, tyre and battery shops and aircon specialists. We visit them, hand over each tool in person and show the team how to use it. Our handover videos are on <a href="{FB_STEVEN}" target="_blank" rel="noopener">Steven's Facebook</a> and <a href="{FB_KIAT}" target="_blank" rel="noopener">Ah Kiat's Facebook</a>.</p>
<h2>The team</h2>
{people_html()}
<h2>Company details</h2>
<table class="cmp"><tbody>
<tr><td>Company</td><td>{LEGAL}</td></tr>
<tr><td>UEN</td><td>{UEN}</td></tr>
<tr><td>Incorporated</td><td>7 August 2021</td></tr>
<tr><td>Business</td><td>Wholesale of workshop machinery and equipment, and vehicle parts and accessories</td></tr>
<tr><td>Address</td><td>{STREET}, {UNIT}, {BUILDING}, Singapore {POSTAL}</td></tr>
<tr><td>WhatsApp</td><td>Steven +65 9822 2629 · Ah Kiat +65 8493 0068 · Alvis +65 9037 2820</td></tr>
<tr><td>Email</td><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><td>Customers</td><td>Car workshops and motor trade businesses in Singapore</td></tr>
</tbody></table>
</article>
<aside class="side"><div class="card sticky"><h2>Talk to us</h2><p>{'<br>'.join(ADDR)}</p>{wa_btn('WhatsApp Steven')}<a class="btn btn-ghost" href="{MAP}" target="_blank" rel="noopener">Open in Google Maps</a></div></aside>
</div></section>'''


def contact_body():
    opts = ''.join('<option>%s</option>' % E(p['short'].lower()) for p in PRODUCTS)
    return f'''<section class="sec"><div class="wrap split">
<div>
<h2>WhatsApp is fastest</h2>
<p>Message Steven on +65 {WA_SHOW} with the model you want, or the cars and jobs it is for.</p>
<form class="enquiry card" id="enquiry" data-wa="{WA_NUM}" action="#">
<label>I am interested in<select name="o">{opts}</select></label>
<label>Workshop name<input name="h" autocomplete="organization"></label>
<label>Your name<input name="n" autocomplete="name"></label>
<label>Notes (model, cars you service)<textarea name="x" rows="3"></textarea></label>
<button class="btn btn-wa" type="submit">{WA_SVG}<span>Send on WhatsApp</span></button>
<p class="small">This opens WhatsApp with your message ready to send. Nothing is stored on this website.</p>
</form>
<h2 style="margin-top:40px">Or message the right person</h2>
{people_html()}
</div>
<aside><div class="card"><h2>Find us</h2><p>{LEGAL}<br>{STREET}, {UNIT}<br>{BUILDING}<br>Singapore {POSTAL}</p>
<p>{GBP_LINE}</p>
<p><a href="tel:{TEL}">Call +65 {WA_SHOW}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><a href="{FB_STEVEN}" target="_blank" rel="noopener">Facebook (Steven)</a> · <a href="{IG_STEVEN}" target="_blank" rel="noopener">Instagram</a></p>
<div class="mapbox"><iframe title="Map to CSKA Auto Enterprise" src="{MAP_EMBED}" width="100%" height="280" style="border:0;border-radius:12px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></aside>
</div></section>'''


def support_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">After you buy a tool from CSKA Auto Enterprise, technical questions go to Alvis Kiew (Ah Yii), our Technical Executive, on WhatsApp +65 9037 2820. For new orders, upgrades and add-on modules, WhatsApp Steven on 9822 2629 or Ah Kiat on 8493 0068.</p>
<figure class="lead-fig">{img('spz6000-training', eager=True)}</figure>
<h2>What to send us</h2>
{ticks([('The tool', 'model and serial number, or a photo of the label.'), ('The car', 'make, model, year and VIN if you have it.'), ('The problem', 'a photo or short video of the screen and any error message.')])}
<h2>Software updates and maker support</h2>
<p>Each maker sets its own update terms. For example, Autel states one year of free software updates and a one-year limited warranty for the MaxiSYS MS909 S2. THINKCAR's remote diagnosis lets users reach THINKCAR's cloud technicians by audio or video call on supported tools. Ask us for the terms of your model.</p>
<h2>Questions</h2>
{faq_html(SUPPORT_FAQ)}
</article>
<aside class="side"><div class="card sticky"><h2>Technical help</h2><p>Alvis Kiew (Ah Yii), Technical Executive</p>{wa_btn('WhatsApp Alvis', 'help with a tool I bought from CSKA.', num='6590372820')}<a class="btn btn-ghost" href="contact/">All contacts</a></div></aside>
</div></section>'''


SUPPORT_FAQ = [('Who do I contact if my tool shows an error?', 'WhatsApp Alvis on 9037 2820 with a photo of the screen, the tool model and the car details.'),
               ('How do I renew software updates?', 'Ask Steven or Ah Kiat for the renewal for your model. Update terms are set by each maker.')]


def privacy_body():
    return f'''<section class="sec"><div class="wrap narrow prose">
<p>{LEGAL} respects your personal data under Singapore's Personal Data Protection Act 2012 (PDPA).</p>
<h2>What we collect</h2><p>This website does not store form data. When you WhatsApp, call or email us, we receive the details you choose to send, such as your name, number, workshop name and address.</p>
<h2>How we use it</h2><p>Only to answer your enquiry, prepare a quotation, deliver your order and support the tools you buy.</p>
<h2>Sharing</h2><p>We share personal data only where needed to complete your order (for example, product registration with the maker), or where the law requires it.</p>
<h2>Your rights</h2><p>You can ask to see, correct or withdraw consent for your personal data. WhatsApp +65 {WA_SHOW} or email {EMAIL}.</p>
<p class="small">Last updated {UPDATED_TEXT}.</p></div></section>'''


def business_schema():
    return {'@type': ['Store', 'LocalBusiness'], '@id': SITE + '#business', 'name': NAME, 'legalName': LEGAL, 'foundingDate': FOUNDED,
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'UEN', 'value': UEN}, 'alternateName': ['CSKA', 'CSKA Auto'],
            'description': 'Supplier of car diagnostic scanners, EV, TPMS and ADAS tools, aircon service machines, battery tools, lifts and workshop equipment to car workshops in Singapore.',
            'url': SITE, 'telephone': TEL, 'email': EMAIL,
            'image': [(IMG_ABS or SITE + IMG) + 'handover-ms908s-ii.webp', (IMG_ABS or SITE + IMG) + 'handover-aircon-machine.webp'], 'logo': (IMG_ABS or SITE + IMG) + 'icon-512.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': '%s %s %s' % (STREET, UNIT, BUILDING), 'addressLocality': 'Singapore', 'postalCode': POSTAL, 'addressCountry': 'SG'},
            'hasMap': GBP, 'sameAs': [GBP], 'areaServed': {'@type': 'Country', 'name': 'Singapore'},
            'brand': [{'@type': 'Brand', 'name': b} for b in BRAND_NAMES],
            'employee': [{'@type': 'Person', 'name': n, 'jobTitle': r, 'telephone': '+' + num} for n, r, num, _, _ in PEOPLE],
            'knowsAbout': ['car diagnostic scanners', 'EV diagnostics', 'TPMS tools', 'ADAS calibration', 'car aircon recovery and flushing machines', 'battery testers', 'two-post car lifts', 'workshop equipment'],
            'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'Supply of ' + p['short'].lower(), 'url': SITE + 'products/%s/' % p['slug']}} for p in PRODUCTS]}  # no Product type: no public prices, and Google flags Product without offers/price (GSC, 20 Oct 2026)


page('', 'CSKA Auto Enterprise | Workshop Tools & Equipment Singapore',
     'Diagnostic scanners, aircon machines, battery tools, lifts and workshop equipment for Singapore car workshops. THINKCAR, Autel, TOPDON, SP ZONE.',
     NAME, home_body(), hero=False, schema=[faq_schema(FAQ_HOME)], photo='handover-ms908s-ii')
page('products/', 'Workshop Tools and Equipment | CSKA Auto Enterprise',
     'Diagnostic scanners, EV, TPMS and ADAS tools, aircon machines, battery tools, lifts, jacks and workshop tools for car workshops in Singapore.',
     'Products', products_index(), crumbs=[('products/', 'Products')], lede='Pick a product line for models, handover photos and questions.')
for p in PRODUCTS:
    path = 'products/%s/' % p['slug']
    page(path, p['title'], p['desc'], p['h1'], None, crumbs=[('products/', 'Products'), (path, p['short'])], lede=p['lede'], photo=p['photo'],
         schema=[{'@type': 'ItemList', 'name': p['h1'], 'url': SITE + path, 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n if n.startswith(t) else '%s %s' % (t, n), 'description': d} for i, (t, n, d) in enumerate(p['models'])]},
                 faq_schema(p['faqs'])])
page('brands/', 'Brands: THINKCAR, Autel, TOPDON, SP ZONE | CSKA Singapore',
     'Brands CSKA Auto Enterprise supplies to Singapore workshops: THINKCAR, Autel, TOPDON, SP ZONE, Ingersoll Rand, M7, Lige, Stirling and ThreeBond.',
     'Brands', brands_index(), crumbs=[('brands/', 'Brands')], lede='The makers behind the tools we hand over.')
for b in BRANDS:
    path = 'brands/%s/' % b['slug']
    page(path, b['title'], b['desc'], '%s in Singapore' % b['name'], brand_body(b), crumbs=[('brands/', 'Brands'), (path, b['name'])], photo=b['photo'],
         lede=b['gist'], schema=[{'@type': 'Brand', 'name': b['name']}, faq_schema(b['faqs'])])
page('handovers/', 'Recent Handovers to Singapore Workshops | CSKA Auto',
     'Photos of THINKCAR, Autel, TOPDON and SP ZONE tools handed over by CSKA Auto Enterprise to car workshops across Singapore.',
     'Recent handovers', handovers_body(), crumbs=[('handovers/', 'Handovers')], lede='Every tool is handed over at the workshop.', photo='handover-sg-garage')
page('support/', 'After-Sales Technical Help | CSKA Auto Enterprise',
     'Technical help for tools bought from CSKA: WhatsApp Alvis Kiew (Ah Yii), Technical Executive, on 9037 2820. Updates and maker support.',
     'After-sales technical help', support_body(), crumbs=[('support/', 'Support')], lede='Bought a tool from us and need a hand? Message Alvis.',
     schema=[faq_schema(SUPPORT_FAQ)])
page('articles/', 'Guides for Workshop Owners | CSKA Auto Enterprise',
     'Plain guides for Singapore workshop owners: choosing a scanner, THINKCAR vs Autel, J2534 and DoIP, EV battery checks, aircon machines, new workshops.',
     'Guides', '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(article_card(a) for a in ARTICLES_NEWEST),
     crumbs=[('articles/', 'Guides')], lede='Straight answers on tools and equipment for car workshops.')
# ---- 2 Nov 2026 SEO pass: hub intros + FAQs (facts from this site only; no prices/hours, none confirmed) ----
PRODUCTS_FAQ = [
    ('What does CSKA Auto Enterprise supply?', 'Tools and equipment for car workshops in Singapore: diagnostic scanners, EV diagnostic tools, TPMS and tyre tools, ADAS calibration, aircon service machines, battery testers and jump starters, lifts and jacks, workshop tools and new workshop set-up.'),
    ('Which brands do you carry?', 'THINKCAR, Autel, TOPDON and SP ZONE aircon machines, plus Ingersoll Rand, M7, Lige, Stirling and ThreeBond. See the brands page for each.'),
    ('How do I get a quote or technical advice?', 'WhatsApp +65 %s for sales or the technical contact shown on the contact page. Tell us the cars you service and the jobs you do, and we will suggest the right tool. We are at 101 Woodlands Ave 12, #07-03B, Polaris @ Woodlands, Singapore 737719.' % WA_SHOW),
]
ARTICLES_FAQ = [
    ('What do the CSKA guides cover?', 'Choosing a diagnostic scanner, THINKCAR versus Autel, J2534 and DoIP, EV battery checks, aircon flushing and service machines, TPMS, ADAS calibration, lifts, battery testers and what a new workshop needs.'),
    ('Are the guides written for workshop owners?', 'Yes. They are plain answers for Singapore workshop owners and technicians choosing tools, with the questions we hear most often when handing over equipment.'),
    ('Can I ask which tool suits my workshop?', 'Yes. WhatsApp +65 %s with the cars you service and the jobs you do, and we will suggest a tool.' % WA_SHOW),
]
PRODUCTS_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Tools and equipment for Singapore car workshops</h2>'
    '<p>CSKA Auto Enterprise Pte. Ltd. supplies car workshops from Polaris @ Woodlands. Our product lines run from diagnostic scanners and EV diagnostic tools to TPMS and tyre tools, ADAS calibration, aircon service machines, battery testers and jump starters, lifts and jacks, and general workshop tools.</p>'
    '<p>Each product line below shows the models we hand over, handover photos and the questions workshop owners ask. If you are fitting out a new workshop, start with the new workshop set-up page. Tell us the cars you service and the jobs you do on WhatsApp +65 %s, and we will suggest the right tool.</p></div></section>') % WA_SHOW
ARTICLES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Guides for workshop owners</h2>'
    '<p>These guides answer the questions Singapore workshop owners ask when choosing equipment: which diagnostic scanner to buy, how THINKCAR and Autel compare, what J2534 and DoIP mean, how to check an EV battery, and how an aircon flushing machine works.</p>'
    '<p>You will also find explanations of TPMS programming, ADAS calibration, battery tester reports, programming power supplies, lifts and what a new workshop needs. Each guide ends with questions and answers. WhatsApp us on +65 %s if yours is not covered.</p></div></section>') % WA_SHOW
def _hub(path, intro, faqs, h2):
    p = PAGES[path]
    p['body'] = intro + p['body'] + '<section class="sec"><div class="wrap narrow"><div class="sec-head"><h2>%s</h2></div>%s</div></section>' % (h2, faq_html(faqs))
    p['schema'] = list(p.get('schema') or []) + [faq_schema(faqs)]
_hub('products/', PRODUCTS_INTRO, PRODUCTS_FAQ, 'Questions about our products')
_hub('articles/', ARTICLES_INTRO, ARTICLES_FAQ, 'Questions about our guides')

for a in ARTICLES:
    path = 'articles/%s/' % a['slug']
    page(path, a['title'], a['desc'], a['h1'], article_body(a), crumbs=[('articles/', 'Guides'), (path, a['h1'])], photo=a['photo'],
         schema=[article_schema(a, path), faq_schema(a['faqs'])])
page('about/', 'About CSKA Auto Enterprise Pte. Ltd. | Woodlands, Singapore',
     'CSKA Auto Enterprise Pte. Ltd. (UEN 202127592M) supplies diagnostic tools and workshop equipment to car workshops in Singapore.',
     'About CSKA Auto Enterprise', about_body(), crumbs=[('about/', 'About')], lede='Workshop tools and equipment, handed over in person.')
page('contact/', 'Contact CSKA Auto Enterprise | WhatsApp 9822 2629',
     'WhatsApp Steven 9822 2629, Ah Kiat 8493 0068 or Alvis 9037 2820. 101 Woodlands Ave 12 #07-03B, Polaris @ Woodlands, Singapore 737719.',
     'Contact us', contact_body(), crumbs=[('contact/', 'Contact')], cta=False, lede='WhatsApp is the fastest way to reach us.')
page('privacy/', 'Privacy Policy | CSKA Auto Enterprise', 'How CSKA Auto Enterprise handles personal data under Singapore\'s PDPA.',
     'Privacy policy', privacy_body(), crumbs=[('privacy/', 'Privacy')], cta=False)
for p in PRODUCTS:
    PAGES['products/%s/' % p['slug']]['body'] = product_body(p)


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------
def render(path, p):
    pre = '../' * path.count('/')
    url = SITE + path
    share = (IMG_ABS or SITE + IMG) + 'share/home.jpg'
    for _a in ARTICLES:
        if _a.get('share') and path == 'articles/%s/' % _a['slug']:
            share = SITE + 'share/%s.jpg' % _a['slug']  # per-article JPG share image, served from the site itself

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    page_img = (IMG_ABS or SITE + IMG) + (p['photo'] or 'handover-ms908s-ii') + '.webp'
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                                 'inLanguage': 'en-SG', 'dateModified': LASTMOD.get(path, UPDATED), 'about': {'@id': SITE + '#business'}, 'primaryImageOfPage': page_img,
                                 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        bg = ''
        if p['photo'] and not path.startswith('articles/'):
            bg = '<figure class="phero-bg">%s</figure>' % img(p['photo'], eager=True)
        head_hero = '<section class="phero%s">%s<div class="wrap">%s<h1>%s</h1>%s</div></section>' % (
            ' has-bg' if bg else '', bg, crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = ('<section class="sec"><div class="wrap"><div class="band"><div><h2>Need a tool for your workshop?</h2>'
                '<p>Tell us the model, or the cars and jobs it is for. We will reply on WhatsApp.</p></div><div class="cta-row">%s</div></div></div></section>') % (
            wa_btn('WhatsApp +65 %s' % WA_SHOW))
    title = E(p['title'])
    preload = '<link rel="preload" as="image" href="%s%s.webp" fetchpriority="high">' % (IMG if IMG_ABS else pre + IMG, p['photo']) if p['photo'] else ''
    body = fix(p['body'] + band)
    brand = brand_html(pre)
    is_art = path.startswith('articles/') and path != 'articles/'
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#06070b">
<link rel="canonical" href="{url}">
{preload}
<meta property="og:type" content="{'article' if is_art else 'website'}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CSKA Auto Enterprise: diagnostic tools and workshop equipment for car workshops">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Exo+2:wght@600;700;800&display=swap">
<link rel="stylesheet" href="{pre}cska.css?v={ASSET_V}">
<script src="{pre}cska.js?v={ASSET_V}" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('WhatsApp', cls='btn btn-wa hdr-call')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<main id="main">
{head_hero}
{body}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand_html(pre)}
<p>Diagnostic tools and workshop equipment for car workshops in Singapore, handed over in person.</p></div>
<div><h3>Products</h3><ul>{''.join('<li><a href="%sproducts/%s/">%s</a></li>' % (pre, x['slug'], E(x['short'])) for x in PRODUCTS)}</ul></div>
<div><h3>Explore</h3><ul>{''.join('<li><a href="%sbrands/%s/">%s</a></li>' % (pre, b['slug'], E(b['name'])) for b in BRANDS)}<li><a href="{pre}handovers/">Handovers</a></li><li><a href="{pre}articles/">Guides</a></li><li><a href="{pre}support/">Support</a></li><li><a href="{pre}about/">About</a></li><li><a href="{pre}privacy/">Privacy</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">Steven +65 9822 2629</a></li>
<li><a href="{E(wa_url(num='6584930068'))}" target="_blank" rel="noopener">Ah Kiat +65 8493 0068</a></li>
<li><a href="{E(wa_url('help with a tool.', '6590372820'))}" target="_blank" rel="noopener">Alvis (technical) +65 9037 2820</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{'<br>'.join(ADDR)}</li>
<li><a href="{GBP}" target="_blank" rel="noopener">Google reviews ★ 5.0</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>© 2026 {LEGAL} · UEN {UEN}</span><span>Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp CSKA: sales or technical help">{WA_SVG}<span>WhatsApp us</span></a><a class="dock-alt" href="{pre}products/">Products</a></div>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', t) for h, t in [('', 'Home')] + NAV)
    p = dict(title='Page not found | CSKA Auto Enterprise', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, photo=None)
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, m.group(2) if m.group(2) != './' else ''), out)


import hashlib
# The host caches css/js for a year, so the file version comes from their content.
ASSET_V = hashlib.sha256(b''.join(open(os.path.join(HERE, f), 'rb').read() for f in ('cska.css', 'cska.js'))).hexdigest()[:8]

BOTS = ['Googlebot', 'Googlebot-Image', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot',
        'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
INDEXNOW_KEY = '208f285bfeaaa073ac0b7bb77afc1625'

HTACCESS = """# CSKA Auto Enterprise ({DOMAIN}). Document root for {DOMAIN}; also served as
# pageonesingapore.com/preview/cska-auto/ before go-live. Overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
SetEnvIfNoCase Host ^(www\\.)?pageonesingapore\\.com$ P1_PREVIEW=1
Header set X-Robots-Tag "noindex, nofollow" env=P1_PREVIEW
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600, public"
</FilesMatch>
</IfModule>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f:
        f.write(INDEXNOW_KEY)
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(path, p))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(''.join('User-agent: %s\nAllow: /\n\n' % b for b in BOTS) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path in PAGES:
            f.write('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, path, LASTMOD.get(path, UPDATED)))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# CSKA Auto Enterprise, workshop tools and equipment supplier in Singapore\n\n'
                '> CSKA Auto Enterprise Pte. Ltd. (UEN %s, incorporated 7 August 2021) supplies car workshops in Singapore with diagnostic scanners '
                '(THINKCAR THINKTOOL, Autel MaxiSys, TOPDON Phoenix), EV diagnostic tools, TPMS tools, Autel ADAS calibration equipment, SP ZONE car aircon '
                'flushing and recovery machines, battery testers, jump starters and power supplies, two-post lifts, jacks and stands, and workshop tools '
                '(Ingersoll Rand, M7, Lige, Stirling, ThreeBond). It is a business-to-business supplier that delivers each tool to the workshop and hands it over in person. '
                'Address: %s %s (%s), Singapore %s. WhatsApp: Steven Chai, Business Development Manager, +65 9822 2629; Kai Kiat (Ah Kiat), Sales Executive, '
                '+65 8493 0068; Alvis Kiew (Ah Yii), Technical Executive, +65 9037 2820. Email %s. Handover videos on facebook.com/chai.steven.393.\n\n## Pages\n'
                % (UEN, STREET, UNIT, BUILDING, POSTAL, EMAIL))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
        f.write('\nLast updated %s.\n' % LLMS_UPDATED_TEXT)
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': NAME, 'short_name': 'CSKA', 'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                               {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
                   'theme_color': '#06070b', 'background_color': '#0a0b10', 'display': 'browser'}, f)
    with open(os.path.join(HERE, 'htaccess.txt'), 'w') as f:
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN))
    import shutil
    for fn in ('cska.css', 'cska.js'):
        shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, fn))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()

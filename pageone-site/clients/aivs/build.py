"""AI Vending Solution Pte. Ltd. (AIVS): builds every page into site/ (python3 build.py).

Facts used (16 Oct 2026), and where they came from:
- ACRA (opengovsg.com, recordowl.com): AI VENDING SOLUTION PTE. LTD., UEN 202439764G, incorporated 27 Sep 2024, live,
  exempt private company, registered at 60 Jalan Lam Huat #05-55 Carros Centre Singapore 737869 (former name Foot N Tip
  Wellness Group).
- Their own website aivs.sg (WordPress/Elementor, scraped 16 Oct 2026): two machines (AI Printbox phone case printing
  vending machine, "3 mins instacase"; Topi Express automated helmet cleaning vending machine, "5 mins instafresh"),
  prices from (S$5,000 and S$1,800 for refurbished machines), warranties (1 year / 6 months, asterisked), support from
  S$99 a month, 0% royalties, cost-price stock, free training, location lists with addresses, FAQs (images deleted within
  48 hours, non-refundable purchases, "AI" = Automated Intelligence), contact details (WhatsApp +65 8878 4061,
  info@aivs.sg, Sales@topiexpress.sg), social links, two blog posts (AI Printbox locations June 2025; Topi Express at
  Hodaka Motoworld 22 Aug 2025), and the $15 price of a printed case (blog post).
- Their own photos (downloaded from aivs.sg wp-content/uploads; they belong to the client).
Not claimed anywhere: the old homepage's "Proven Monthly Revenue: $3,000+ from a single machine" (unverified), ROI
  timeframes, customer counts, Google rating, the AI Shieldbox machine seen in photos (not described on their site),
  the second phone number +65 8335 4865 (CONFIRM). Things Edwin must confirm are in CONFIRM and README.md.
"""
import html
import json
import os
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

SLUG = 'aivs'
DOMAIN = 'aivs.sg'
LIVE = True                           # live on aivs.sg since 18 Oct 2026 (Edwin OK)
NOINDEX = False                       # MASTER-RULES 4.3: previews are hidden by a server header, never a page tag
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
# Photos are served from jsDelivr (repo site-assets branch, commit 5802022) because the bridge cannot take binaries reliably.
# At go-live copy site/img/ to the client host and set AIVS_IMG=img/ .
IMG = os.environ.get('AIVS_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@5802022/site-assets/aivs/')
IMG_ABS = IMG if IMG.startswith('http') else None
# AIVS's own machine videos from aivs.sg, converted to small silent H.264 files (site-assets commit 6e4281e)
VID = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@6e4281e/site-assets/aivs/video/'
VIDEOS = {'ai-printbox': ('printbox', 'portrait', 'AI Printbox printing a custom phone case'),
          'topi-express': ('topi', 'landscape', 'Topi Express helmet cleaning machine in use')}
# Plays muted videos only while on screen, and never for visitors who ask for reduced motion.
VID_JS = ('<style>.sc-media video{width:100%;height:100%;object-fit:cover;opacity:.7;display:block;transition:opacity .6s}.sc-card:hover .sc-media video{opacity:.85}.vid{margin:20px 0 28px;border-radius:18px;overflow:hidden;background:#0f1116}.vid video{display:block;width:100%;height:auto;background:#0f1116}.vid-portrait{max-width:380px}.vid figcaption{padding:8px 14px;font-size:.85rem;color:#c9c3b3}</style><script>(function(){var v=document.querySelectorAll("video[data-auto]");if(!v.length||'
          'matchMedia("(prefers-reduced-motion: reduce)").matches)return;var io="IntersectionObserver" in window&&'
          'new IntersectionObserver(function(es){es.forEach(function(e){var x=e.target;if(e.isIntersecting){var p=x.play();'
          'p&&p.catch(function(){})}else x.pause()})},{threshold:.25});[].forEach.call(v,function(x){x.muted=true;'
          'io?io.observe(x):x.play()})})();</script>')


def video(slug, controls=False):
    name, orient, label = VIDEOS[slug]
    ctl = ' controls' if controls else ''
    return ('<video data-auto muted loop playsinline preload="metadata"%s poster="%s%s-poster.jpg" aria-label="%s">'
            '<source src="%s%s.mp4" type="video/mp4"></video>' % (ctl, VID, name, label, VID, name))
UPDATED = '2026-10-16'
# Per-page last-modified dates (sitemap + WebPage dateModified); added 28 Oct 2026. Pages not listed fall back to UPDATED.
LASTMOD = {'articles/which-phones-can-a-phone-case-printing-machine-print-for/': '2026-10-26', 'articles/can-you-run-a-vending-machine-business-part-time/': '2026-10-28'}

NAME = 'AIVS'
FULL = 'AI Vending Solution'
LEGAL = 'AI Vending Solution Pte. Ltd.'
UEN = '202439764G'
FOUNDED = '2024-09-27'
# Two WhatsApp lines (Edwin, 19 Oct 2026): sales line is the default on every button.
WA_NUM, WA_SHOW = '6583354865', '8335 4865'      # Business collaboration / machine purchase
TEL = '+6583354865'
SUP_NUM, SUP_SHOW = '6588784061', '8878 4061'    # Technical support / refund enquiries
SUP_TEL = '+6588784061'
EMAIL = 'info@aivs.sg'
WA_MSG = 'Hi AIVS, I found your website. I would like to ask about '
STREET, UNIT, BUILDING, POSTAL = '60 Jalan Lam Huat', '#05-54', 'Carros Centre', '737869'
ADDR = ['60 Jalan Lam Huat, #05-54', 'Carros Centre, Singapore 737869']
MAPQ = quote('AI Vending Solution Pte Ltd, 60 Jalan Lam Huat #05-54 Carros Centre Singapore 737869')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
GBP = 'https://maps.google.com/?cid=14142975950785926519'  # AIVS Google Business Profile (Edwin, 20 Oct 2026)
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
FB = 'https://www.facebook.com/share/1BteuRiSRK/'
IG = 'https://www.instagram.com/aivendingsolution/'
TIKTOK = 'https://www.tiktok.com/@aivendingsolution'
YT = 'https://www.youtube.com/@AIVendingSolutionPteLt'
PB_PRICE, TP_PRICE, SUPPORT, CASE_PRICE, WASH_PRICE = '5,000', '1,800', '99', '15', '5'

CONFIRM = [
    'Prices: AI Printbox from S$5,000 and Topi Express from S$1,800 (refurbished), support from S$99 a month, and what each price includes (GST, delivery, installation)',
    'Warranty asterisks: what the 1-year (AI Printbox) and 6-month (Topi Express) hardware warranties exclude',
    'Stock: the old site says both "cost price" and "attractive partner pricing" for phone casing stock; which wording is right',
    'Opening hours for the Carros Centre office (none published), and whether visitors can view a machine there',
    'AI Shieldbox (screen protector machine seen next to AI Printbox in photos): is it for sale too? It is not on the new site yet',
    'Current AI Printbox location list (14 on the old site; VivoCity and Great World from the June 2025 post are no longer listed)',
    'The old Terms & Conditions page was empty ("Please type the T&Cs here"); the new /terms/ page only repeats the customer rules from their FAQ',
    'Google Business Profile and any Google reviews to quote; the number of machines placed so far (not stated anywhere)',
]

NAV = [('machines/', 'Machines'), ('services/', 'Own a machine'), ('locations/', 'Locations'), ('prices/', 'Prices'), ('partner-with-aivs/', 'Supplier Partners'), ('articles/', 'Articles'), ('about/', 'About'), ('contact/', 'Contact')]
# mobile-menu subtitles (Edwin, 26 Oct 2026); hidden on desktop
NAV_SUB = {'services/': 'For buyers, investors and franchise prospects', 'partner-with-aivs/': 'For Singapore-based AI/smart vending machine suppliers and distributors'}
# mobile bottom bar: prefilled WhatsApp text, source = page path (Edwin, 26 Oct 2026)
DOCK_SUP_MSG = 'Hi AIVS, I need help with technical support or a refund.'
DOCK_BIZ_MSG = 'Hi AIVS, I have a business enquiry (buying a machine, investing, supplying machines or partnering).'

E = html.escape

PHOTOS = {  # name: (width, height, alt)
    'printbox-mall-dark': (675, 900, 'AI Printbox phone case printing vending machine lit up in a Singapore shopping mall at night'),
    'printbox-queue': (1039, 1400, 'Shoppers queueing at an AI Printbox machine to print custom phone cases'),
    'printbox-event': (1400, 1050, 'The AI Printbox machine at a franchise exhibition booth in Singapore with visitors around it'),
    'printbox-crowd': (675, 900, 'A crowd gathered around the AI Printbox vending machine at an exhibition'),
    'printbox-corridor': (675, 900, 'AI Printbox machine placed in a bright mall corridor in Singapore'),
    'printbox-mall': (675, 900, 'AI Printbox custom phone case vending machine in a shopping mall atrium'),
    'printbox-escalator': (675, 900, 'AI Printbox vending machine beside a mall escalator'),
    'both-machines': (675, 900, 'AI Printbox and AI Shieldbox vending machines side by side in a mall'),
    'printbox-red': (506, 900, 'Red AI Printbox machine with the "My phone, my style" wrap in a mall'),
    'printbox-shop': (675, 900, 'AI Printbox vending machine inside a shop unit'),
    'printbox-lobby': (506, 900, 'AI Printbox machine in a building lobby'),
    'printbox-front': (675, 900, 'Front view of the AI Printbox machine showing the case display and touchscreen'),
    'case-deer': (450, 800, 'A custom printed phone case with a glowing deer design, fresh out of the AI Printbox'),
    'case-dragon': (450, 800, 'A custom printed phone case with a baby dragon design from AI Printbox'),
    'case-dragon-2': (450, 800, 'A green-rimmed phone case with a dragon print made in 3 minutes at AI Printbox'),
    'topi-shop': (675, 900, 'Topi Express helmet cleaning vending machine outside a motorcycle shop in Singapore'),
    'topi-345wash': (675, 900, 'Topi Express helmet cleaning machine at 345 Wash laundromat in Telok Blangah'),
    'topi-workshop': (506, 900, 'Topi Express 5-minute helmet cleaning machine at a motorcycle workshop'),
    'topi-bw': (506, 900, 'Topi Express machine at BW Motorsports in Old Toh Tuck Road'),
    'topi-overview': (1000, 707, 'Topi Express product overview: 5-minute quick cleaning, UVC technology, eco-friendly disinfection, 3-pin plug, easy setup and mobility, cashless payment'),
    'topi-franchise': (1000, 707, 'Topi Express franchise graphic: monitor sales and inventory live, 0% royalty fee, cashless payment'),
    'topi-helmet': (454, 800, 'A rider placing a helmet into the Topi Express cleaning chamber'),
    'machines-duo': (1200, 640, 'The two AIVS machines: Topi Express helmet cleaning vending machine and AI Printbox phone case printing vending machine'),
    'dashboard': (444, 700, 'The AIVS owner dashboard on a phone showing revenue, devices and inventory'),
}


def img(name, sm=False, cls='', eager=False):
    w, h, alt = PHOTOS[name]
    return '<img src="%s%s.webp" alt="%s" width="%d" height="%d"%s%s>' % (
        IMG, name, E(alt), w, h, ' loading="lazy" decoding="async"' if not eager else ' fetchpriority="high"', ' class="%s"' % cls if cls else '')


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')
PIN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M12 22s7-7.1 7-12a7 7 0 1 0-14 0c0 4.9 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5"/></svg>')
MAIL_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>')


def wa_url(topic='owning a machine.'):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(WA_MSG + topic))


def sup_url(topic='technical support.'):
    return 'https://wa.me/%s?text=%s' % (SUP_NUM, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp us', topic='owning a machine.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic)), WA_SVG, E(label))


def mail_btn(label='Email us', cls='btn btn-ghost'):
    return '<a class="%s" href="mailto:%s">%s<span>%s</span></a>' % (cls, EMAIL, MAIL_SVG, E(label))


def enquire_btn(label='Enquire about a machine', cls='btn btn-gold'):
    return '<a class="%s" href="contact/#enquiry">%s</a>' % (cls, E(label))


MARK = '<img class="brand-mark" src="%slogo-320.png" alt="AIVS logo" width="42" height="42">' % IMG


def brand_html(pre):
    mark = MARK if IMG.startswith('http') else MARK.replace('src="', 'src="' + pre)
    return ('<a class="brand" href="%s" aria-label="%s, home page">%s<span><span class="brand-name">AIVS</span>'
            '<span class="brand-sub">AI Vending Solution · Singapore</span></span></a>') % (pre or './', FULL, mark)


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, photo=None, theme=''):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [],
                       hero=hero, cta=cta, photo=photo, theme=theme)


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}



# Question-led answer blocks (Edwin's SEO/AEO/GEO blueprint, 17 Oct 2026). Each answer opens with a
# bold one-sentence direct answer. Only facts AIVS publishes; no earnings promises.
QA = {
    'ai-printbox': [
        ('What is the AI Printbox by AIVS?',
         'The AI Printbox is a self-service kiosk that prints a customer\'s own photo or a chosen design onto a phone case in about 3 minutes.',
         'Customers pick their phone model, choose a design or upload a photo, pay cashlessly and collect the printed case. AIVS sells refurbished machines to owner-operators, who keep the sales and pay no royalties.',
         ['A custom phone case in about 3 minutes, S$%s a case' % CASE_PRICE,
          'Self-service with cashless payment, so no staff are needed at the machine',
          '13 machines live in Singapore malls and Changi Airport Terminal 3']),
        ('How much does it cost to start an AI Printbox business in Singapore?',
         'A refurbished AI Printbox machine starts from S$%s, with a 1-year hardware warranty (terms apply).' % PB_PRICE,
         'On top of the machine, budget for your location\'s rent, electricity, phone case stock (supplied by AIVS at cost price) and the optional support plan from S$%s a month. There is no franchise fee and 0%% royalties. If your budget is under S$%s, the Topi Express helmet cleaner starts from S$%s.' % (SUPPORT, PB_PRICE, TP_PRICE),
         []),
    ],
    'topi-express': [
        ('What is Topi Express by AIVS?',
         'Topi Express is a self-service machine that disinfects, deodorises and sterilises a motorcycle helmet in about 5 minutes for S$%s.' % WASH_PRICE,
         'Riders place the helmet in the chamber and pay by QR code, and UVC light with an eco-friendly disinfectant mist does the rest. AIVS sells refurbished machines to owner-operators from S$%s.' % TP_PRICE,
         ['About 5 minutes per helmet, S$%s a clean' % WASH_PRICE,
          'UVC light and an eco-friendly disinfectant mist',
          'Six machines live at motorcycle shops, workshops and a laundromat, one running 24 hours a day']),
        ('Is a helmet cleaning vending machine profitable in Singapore?',
         'It depends on the location: how many riders pass the machine and how often they stop long enough for a 5-minute clean.',
         'Each clean earns S$%s. Against that are the machine (from S$%s), rent, electricity, disinfectant and the optional support plan from S$%s a month. AIVS does not publish earnings figures, so ask AIVS for real usage numbers from comparable sites before you buy.' % (WASH_PRICE, TP_PRICE, SUPPORT),
         []),
    ],
    'own-a-vending-machine': [
        ('How does owning an AIVS vending machine work?',
         'You buy the machine outright and keep the sales, and AIVS helps you keep it running.',
         'AIVS supplies stock at cost price, trains you, and offers a support plan from S$%s a month that covers maintenance, 24/7 technical help and, for Topi Express, disinfectant top-ups. You choose and secure the location, and AIVS shares what works from its own placements at sites such as AMK Hub and Changi Airport Terminal 3 and can help with site finding. There is no franchise fee and 0%% royalties.' % SUPPORT,
         []),
        ('Can I start a vending machine business in Singapore with under S$5,000?',
         'Yes. A refurbished Topi Express helmet cleaner starts from S$%s, and the AI Printbox starts from S$%s.' % (TP_PRICE, PB_PRICE),
         'Keep money aside for the location\'s rent and electricity, the first stock and the optional support plan. A vending machine is low-effort rather than hands-off: someone still restocks it and checks it.',
         []),
        ('Is a vending machine a good side business for working professionals?',
         'It can be, because the machine sells without staff and the AIVS support plan covers repairs and technical help.',
         'Your time goes into finding the location, checking the sales dashboard on your phone and restocking. Earnings depend on the site, and AIVS does not promise a fixed income.',
         []),
    ],
}


def qa_html(slug):
    out = ''
    for q, lead, rest, bullets in QA.get(slug, []):
        out += '<h2>%s</h2><p><strong>%s</strong> %s</p>' % (E(q), E(lead), E(rest))
        if bullets:
            out += '<ul class="ticks">%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in bullets)
    return out


def qa_pairs(slug):
    return [(q, '%s %s' % (lead, rest)) for q, lead, rest, _ in QA.get(slug, [])]


def plist(items):
    return '<ul class="plist">%s</ul>' % ''.join(
        '<li><span>%s%s</span><b>%s</b></li>' % (E(n), '<small>%s</small>' % E(note) if note else '', E(p)) for n, p, note in items)


def specs(items):
    return '<div class="specs">%s</div>' % ''.join('<div class="spec"><b>%s</b><span>%s</span></div>' % (E(k), E(v)) for k, v in items)


def tile(href, photo, title, gist, more='More details →'):
    return '<a class="scard" href="%s">%s<span class="scard-t"><b>%s</b><span>%s</span><em>%s</em></span></a>' % (
        href, img(photo, sm=True), E(title), E(gist), E(more))


PRICE_NOTE = ('Prices in Singapore dollars as published by AIVS, for refurbished machines, before any options. Ask on WhatsApp for '
              'the current price, what it includes and the warranty terms.')

# ----------------------------------------------------------------------------------------------
# Locations (from aivs.sg, 16 Oct 2026)
# ----------------------------------------------------------------------------------------------
PB_LOCS = [
    ('AMK Hub', '53 Ang Mo Kio Avenue 3, Singapore 569933', 'Level 3, Lobby B'),
    ('Bukit Panjang Plaza', '1 Jelebu Road, Singapore 677743', 'Entrance of #01-56'),
    ('Changi Airport Terminal 3, Arrival Hall', '65 Airport Boulevard, Singapore 819663', '#01-VM4'),
    ('Changi Airport Terminal 3, Basement 2', '65 Airport Boulevard, Singapore 819663', 'iClaw, #B2-45'),
    ('Changi City Point', '5 Changi Business Park Central 1, Singapore 486038', 'Entrance of #02-24'),
    ('City Square Mall', '180 Kitchener Road, Singapore 208539', 'Level 4'),
    ('Eastpoint Mall', '3 Simei Street 6, Singapore 528833', 'Entrance of #01-21/22, Level 1'),
    ('Hillion Mall', '17 Petir Road, Singapore 678278', 'Basement 3, linkway to Bukit Panjang MRT'),
    ('Hougang Mall', '90 Hougang Avenue 10, Singapore 538766', 'Level 4'),
    ('Parkway Parade', '80 Marine Parade Road, Singapore 449269', 'iClaw, #B1-18B'),
    ('Sembawang Shopping Centre', '604 Sembawang Road, Singapore 758459', 'Entrance of #01-05, Level 1'),
    ('Tampines 1', '10 Tampines Central 1, Singapore 529536', 'Entrance of #02-24'),
    ('The Centrepoint', '176 Orchard Road, Singapore 238843', 'iClaw, #02-K02'),
]
TP_LOCS = [
    ('Wheels & Cycles', '39 Woodlands Close, #01-17, Singapore 737856', 'Bicycle and motorcycle shop'),
    ('345 Wash', '61 Telok Blangah Heights, #01-93, Singapore 100061', 'Laundromat'),
    ('Candy Motor', '25 Kaki Bukit Road 4, #01-69/70, Singapore 417800', 'Motorcycle accessories'),
    ('BW Motorsports', '32 Old Toh Tuck Road, iBiz Centre, #01-09, Singapore 597658', 'Motorcycle workshop'),
    ('Gusto Broz Workshop', '23 Kaki Bukit Road 4, #01-20, Singapore 417801', 'Motorcycle workshop'),
    ('Hodaka Motoworld', '10 Kaki Bukit Road 1, #01-09, KB Industrial Building, Singapore', 'Motorcycle dealer, machine running 24 hours since 22 August 2025'),
]


def loc_cards(locs, cls):
    out = []
    for name, addr, note in locs:
        q = quote('%s, %s' % (name, addr))
        out.append('<div class="loc %s"><b>%s</b><span>%s</span>%s<a href="https://www.google.com/maps/search/?api=1&amp;query=%s" target="_blank" rel="noopener">Open in Google Maps →</a></div>' % (
            cls, E(name), E(addr), '<small>%s</small>' % E(note) if note else '', q))
    return '<div class="locs">%s</div>' % ''.join(out)


# ----------------------------------------------------------------------------------------------
# Machines
# ----------------------------------------------------------------------------------------------
PB_FAQ_OWNER = [
    ('How much does an AI Printbox machine cost?', 'A refurbished AI Printbox machine is from S$%s, with a 1-year hardware warranty (terms apply) and an optional monthly support plan from S$%s. WhatsApp %s for the current price and what it includes.' % (PB_PRICE, SUPPORT, WA_SHOW)),
    ('Do I own the machine?', 'Yes. You buy and own the machine outright, and there are no royalty fees. You can run it under the AI Printbox brand or re-wrap it with your own branding. The artwork, branding and mascot designs on the AIVS wrap remain AIVS intellectual property.'),
    ('Do I need to manage it every day?', 'No. The machine is self-service and cashless. Under the monthly support plan AIVS handles maintenance and system support, and you top up phone case stock, which you buy from AIVS at partner pricing.'),
    ('Who finds the location?', 'You choose and secure your own location, which keeps the business yours. AIVS shares what it has learned from its own mall placements, such as high-footfall entrances, linkways to MRT stations and airport arrival halls, and can help with site sourcing.'),
    ('Which phones does AI Printbox support?', 'The latest iPhone and Samsung models, and the list is updated as new phones are released. The machine interface shows the models available at the time of printing.'),
    ('Why is it called "AI" when there is no artificial intelligence in the machine?', 'In the AIVS name, "AI" stands for Automated Intelligence: smart, automated vending that makes a business simple to run. It does not refer to artificial intelligence.'),
]
TP_FAQ_OWNER = [
    ('How much does a Topi Express machine cost?', 'A refurbished Topi Express helmet cleaning machine is from S$%s, with a 6-month hardware warranty (terms apply). There are no royalty fees. WhatsApp %s for the current price and what it includes.' % (TP_PRICE, WA_SHOW)),
    ('What support do I get as an owner?', 'AIVS helps with site finding and marketing, tops up the disinfectant liquid, and provides 24/7 technical support. Repairs are covered under the monthly maintenance support plan.'),
    ('Where does a helmet cleaning machine work best?', 'Where riders already stop: petrol kiosks, motorcycle repair shops, motorcycle accessory shops and detailing centres. Current Topi Express machines sit at motorcycle workshops in Kaki Bukit, Old Toh Tuck Road and Woodlands, and at a laundromat in Telok Blangah.'),
    ('How do customers pay?', 'By QR code, so no card terminal is needed. Visa and Mastercard acceptance can be arranged on request.'),
    ('Can I move the machine to a new location later?', 'Yes. Let AIVS know in advance and transport can be arranged. The machine runs off a standard 3-pin plug, so setup is simple.'),
    ('Can I put my own branding on it?', 'Yes. You can re-wrap the machine with your own branding at your own cost.'),
]
PB_FAQ_CUST = [
    ('How does AI Printbox work?', 'Select your phone model on the touchscreen, pick a design from the collection, add an AI filter, or upload your own photo, then pay. The machine prints your case in about 3 minutes.'),
    ('How much is a printed phone case?', 'A custom printed case is S$%s (price published on aivs.sg in 2025; check the machine for the current price). Each case is a durable, protective case with the design printed into it, not a sticker.' % CASE_PRICE),
    ('Is my uploaded photo kept?', 'No. Uploaded images are deleted from the system within 48 hours and are not stored, shared or used for anything else.'),
    ('Can I get a refund if I change my mind?', 'No. Purchases are non-refundable and non-exchangeable, because each case is printed to your order. You are responsible for the content you print.'),
]
TP_FAQ_CUST = [
    ('How does the Topi Express helmet cleaning machine work?', 'Place your helmet in the chamber, pay by QR code and the machine disinfects, deodorises and sterilises it with UVC and a disinfectant mist in about 5 minutes.'),
    ('How much does a helmet clean cost?', 'S$%s for a 5-minute clean, as published by AIVS. Check the machine for the current price.' % WASH_PRICE),
    ('Where can I clean my helmet?', 'At six locations: Wheels & Cycles (Woodlands), 345 Wash (Telok Blangah), Candy Motor and Gusto Broz Workshop (Kaki Bukit Road 4), BW Motorsports (Old Toh Tuck Road) and Hodaka Motoworld (Kaki Bukit Road 1, 24 hours).'),
    ('Can I clean gloves or other gear?', 'The chamber is built around a helmet. Ask at the host shop before putting other riding gear in.'),
]

MACHINES = [
    dict(slug='ai-printbox', short='AI Printbox', theme='pb', photo='printbox-mall-dark', hero_photo='printbox-front',
         tag='3-minute custom phone case printing', price=PB_PRICE,
         gist='A self-service machine that prints a customer\'s own photo or a design onto a phone case in about 3 minutes. 13 machines in Singapore malls and Changi Airport.',
         title='AI Printbox Phone Case Printing Machine from S$%s | AIVS' % PB_PRICE,
         desc='AI Printbox prints custom phone cases in 3 minutes. Own a refurbished machine from S$%s, 1-year warranty, 0%% royalties. 13 locations. WhatsApp %s.' % (PB_PRICE, WA_SHOW),
         h1='AI Printbox: the 3-minute phone case printing machine',
         lede='Customers pick a design or upload a photo, pay, and walk away with a printed case 3 minutes later. You own the machine, choose the location and keep the sales.',
         specs=[('Machine price', 'From S$%s (refurbished)' % PB_PRICE), ('Hardware warranty', '1 year*'), ('Support plan', 'From S$%s a month' % SUPPORT), ('Royalties', '0%'),
                ('Print time', 'About 3 minutes'), ('Retail price per case', 'S$%s' % CASE_PRICE), ('Payment', 'Cashless'), ('Live in Singapore', '13 locations')],
         gallery=['printbox-queue', 'printbox-event', 'case-deer', 'printbox-corridor', 'case-dragon', 'printbox-escalator'],
         sections=[
             ('What customers get', [
                 'A durable, protective phone case with their design printed into it, not a sticker or a peel-off decal. They choose a design from the collection, '
                 'add an AI filter, or upload their own photo of a pet, a group or a holiday. The machine supports the latest iPhone and Samsung models and the list grows as new phones launch.',
                 'The old site describes the typical buyer well: secondary school students and working adults who want a case nobody else has, and people looking for a last-minute personal gift.']),
             ('What you get as the owner', [
                 'A refurbished AI Printbox machine from S$%s with a 1-year hardware warranty (terms apply). You own it outright and pay no royalties. You can run it under the AI Printbox brand '
                 'that shoppers already see in 13 locations, or re-wrap it with your own branding.' % PB_PRICE,
                 'Phone case stock comes from AIVS at partner pricing. A monthly support plan from S$%s covers maintenance and system support, and training is included so you can start without any vending experience.' % SUPPORT,
                 'You choose and secure your own location. No retail shop or staff is needed: the machine is self-service and takes cashless payment around the clock.']),
             ('Where AI Printbox already runs', [
                 'AMK Hub, Bukit Panjang Plaza, Changi Airport Terminal 3 (Arrival Hall and Basement 2), Changi City Point, City Square Mall, Eastpoint Mall, Hillion Mall, Hougang Mall, '
                 'Parkway Parade, Sembawang Shopping Centre, Tampines 1 and The Centrepoint. Addresses and unit numbers are on the locations page.']),
         ],
         faqs=PB_FAQ_OWNER, cust_faqs=PB_FAQ_CUST, loc_href='locations/ai-printbox/'),
    dict(slug='topi-express', short='Topi Express', theme='tp', photo='topi-shop', hero_photo='topi-workshop',
         tag='5-minute automated helmet cleaning', price=TP_PRICE,
         gist='A plug-in machine that disinfects, deodorises and sterilises a motorcycle helmet in 5 minutes for S$%s. Built for motorcycle shops, petrol kiosks and detailing centres.' % WASH_PRICE,
         title='Topi Express Helmet Cleaning Machine from S$%s | AIVS' % TP_PRICE,
         desc='Topi Express disinfects a helmet in 5 minutes for S$%s. Own a refurbished machine from S$%s, 6-month warranty, 0%% royalties, 24/7 support. 6 locations.' % (WASH_PRICE, TP_PRICE),
         h1='Topi Express: the 5-minute helmet cleaning machine',
         lede='Riders drop a helmet in, pay by QR code and ride off fresh 5 minutes later. The lowest-cost machine in the AIVS range, built for places where riders already stop.',
         specs=[('Machine price', 'From S$%s (refurbished)' % TP_PRICE), ('Hardware warranty', '6 months*'), ('Royalties', '0%'), ('Clean time', 'About 5 minutes'),
                ('Retail price per clean', 'S$%s' % WASH_PRICE), ('Payment', 'QR code, no card terminal'), ('Power', 'Standard 3-pin plug'), ('Live in Singapore', '6 locations')],
         gallery=['topi-overview', 'topi-franchise', 'topi-helmet', 'topi-345wash', 'topi-bw', 'topi-workshop'],
         sections=[
             ('What riders get', [
                 'A helmet that is disinfected, deodorised and sterilised in about 5 minutes, using UVC and an eco-friendly disinfectant mist, for S$%s. The touchscreen walks them through it and payment is by QR code.' % WASH_PRICE,
                 'Helmets are worn daily in Singapore\'s heat, so the machine answers a real need at the places riders visit anyway: workshops, accessory shops, petrol kiosks and even a laundromat.']),
             ('What you get as the owner', [
                 'A refurbished Topi Express machine from S$%s with a 6-month hardware warranty (terms apply), no royalty fees, and a machine you can self-manage. It plugs into a standard 3-pin socket, so setup is a matter of placing it and switching it on.' % TP_PRICE,
                 'AIVS helps with site finding and marketing, tops up the disinfectant liquid, and gives 24/7 technical support. Repairs are covered under the monthly maintenance support plan. '
                 'You can track sales and inventory live from your phone, and re-wrap the machine with your own branding at your own cost.']),
             ('Where Topi Express already runs', [
                 'Wheels & Cycles in Woodlands, 345 Wash in Telok Blangah, Candy Motor and Gusto Broz Workshop on Kaki Bukit Road 4, BW Motorsports at iBiz Centre on Old Toh Tuck Road, '
                 'and Hodaka Motoworld on Kaki Bukit Road 1, where the machine has run 24 hours a day since 22 August 2025.']),
         ],
         faqs=TP_FAQ_OWNER, cust_faqs=TP_FAQ_CUST, loc_href='locations/topi-express/'),
]
MCH = {m['slug']: m for m in MACHINES}


def machine_body(m):
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % p for p in ps)) for h, ps in m['sections'])
    gal = ''.join('<figure>%s</figure>' % img(n) for n in m['gallery'])
    other = [x for x in MACHINES if x['slug'] != m['slug']][0]
    return f'''<section class="sec {m['theme']}"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(m['hero_photo'], eager=True)}</figure>
{qa_html(m['slug'])}
{specs(m['specs'])}
<p class="small">* Warranty terms apply. {E(PRICE_NOTE)}</p>
<h2>See it in action</h2>
<figure class="vid vid-{VIDEOS[m['slug']][1]}">{video(m['slug'], controls=True)}<figcaption>Video by AIVS.</figcaption></figure>
{secs}
<h2>Photos</h2>
<div class="gallery">{gal}</div>
<h2>Questions from future owners</h2>
{faq_html(m['faqs'])}
<h2>Questions from customers</h2>
{faq_html(m['cust_faqs'])}
<p class="byline">Facts on this page come from AIVS\'s published machine details and location list. Last checked {UPDATED}.</p>
</article>
<aside class="side"><div class="card sticky"><h2>Own a {E(m['short'])}</h2><p>From S${m['price']}, refurbished, 0% royalties. Tell us where you would place it and we will reply with the current price and next steps.</p>{wa_btn('WhatsApp us', topic='owning a %s machine.' % m['short'])}{enquire_btn(cls='btn btn-ghost')}
<p class="small" style="margin-top:14px"><a href="{m['loc_href']}">See all {E(m['short'])} locations →</a><br><a href="services/own-a-vending-machine/">How ownership works →</a><br><a href="machines/{other['slug']}/">Compare with {E(other['short'])} →</a></p></div></aside>
</div></section>
{VID_JS}'''


def machine_cards():
    return '<div class="mcards">%s</div>' % ''.join(
        '<a class="mcard %s" href="machines/%s/">%s<span class="mcard-t"><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="price">From S$%s <em>· More details →</em></span></span></a>' % (
            m['theme'], m['slug'], img(m['photo']), E(m['tag']), E(m['short']), E(m['gist']), m['price']) for m in MACHINES)


# ----------------------------------------------------------------------------------------------
# Services (the ownership programme, support, hosting, branding)
# ----------------------------------------------------------------------------------------------
SERVICES = [
    dict(slug='own-a-vending-machine', short='Own a vending machine', photo='printbox-crowd',
         gist='Buy a refurbished machine from S$%s, run it under the AIVS brand or your own, pay 0%% royalties and keep the sales.' % TP_PRICE,
         title='Own a Vending Machine in Singapore, 0% Royalties | AIVS',
         desc='How AIVS ownership works: buy a refurbished AI Printbox (from S$%s) or Topi Express (from S$%s), 0%% royalties, cost-price stock, training and support.' % (PB_PRICE, TP_PRICE),
         h1='Own a vending machine, not a franchise fee',
         lede='AIVS sells you the machine and stands behind it. You own the asset, choose the location, and pay no royalties on what it earns.',
         sections=[
             ('How it works', [
                 'Pick a machine: Topi Express from S$%s for riders, or AI Printbox from S$%s for shoppers. Choose and secure a location; AIVS shares what it knows about sites that work. '
                 'AIVS delivers and sets up the machine, trains you, and you start selling. Stock comes from AIVS at cost price, and a monthly support plan from S$%s covers maintenance and system support.' % (TP_PRICE, PB_PRICE, SUPPORT)]),
             ('Why ownership rather than a franchise', [
                 'A franchise usually charges an upfront fee and a cut of every sale. AIVS charges neither: you buy the machine and keep what it earns. You can use the AI Printbox or Topi Express '
                 'branding that customers already recognise from 19 live locations, or wrap the machine in your own brand. AIVS keeps the rights to its own artwork and mascots.']),
             ('What the machine earns', [
                 'That depends on the location and the product mix, and AIVS does not publish a guaranteed figure. What it does offer is a sales and inventory dashboard on your phone, so you can see '
                 'exactly what the machine took today, and the experience of its own placements in malls, the airport and motorcycle shops. Ask on WhatsApp and the team will talk you through real examples for the kind of site you have in mind.']),
             ('Who it suits', [
                 'People who want a second income without a shop or staff, business owners who want to add a self-service product to an existing site, and property or retail teams that want an attraction '
                 'at an entrance or linkway. No vending experience is needed; training and ongoing support are included.']),
         ],
         faqs=[
             ('Do I need experience to start?', 'No. AIVS provides training and supports you from setup through day-to-day operations.'),
             ('How fast can I start?', 'Typically within a few weeks of confirming your machine and location.'),
             ('How much time does it take to run?', 'The machine is self-service and cashless, so most weeks it needs only a stock check. The dashboard shows sales and inventory from your phone.'),
             ('Is there a royalty or franchise fee?', 'No. AIVS charges 0% royalties. You buy the machine and keep the sales.'),
             ('Can I use my own branding?', 'Yes. Both machines can be re-wrapped with your own branding at your own cost, or you can run them under the AI Printbox and Topi Express brands.'),
         ]),
    dict(slug='support-and-maintenance', short='Support and maintenance', photo='dashboard',
         gist='A monthly plan from S$%s that covers maintenance, system support and, for Topi Express, disinfectant top-ups, with 24/7 technical help.' % SUPPORT,
         title='Vending Machine Support Plan from S$%s/month | AIVS' % SUPPORT,
         desc='AIVS support plan for owners: maintenance and repairs, system support, 24/7 technical help, disinfectant top-ups and a live dashboard. From S$%s a month.' % SUPPORT,
         h1='Support and maintenance for owners',
         lede='You own the machine; AIVS keeps it running. One monthly plan covers the technical side so you are never the one holding a screwdriver.',
         sections=[
             ('What the plan covers', [
                 'Maintenance and repairs under the monthly maintenance support, system and software support, and 24/7 technical help by phone or WhatsApp. For Topi Express, AIVS also tops up the disinfectant liquid. '
                 'The plan starts from S$%s a month for AI Printbox; ask for the Topi Express figure.' % SUPPORT]),
             ('Hardware warranty', [
                 'Every refurbished machine comes with a hardware warranty: 1 year on AI Printbox and 6 months on Topi Express, with terms that AIVS will explain before you buy.']),
             ('See your machine from anywhere', [
                 'The owner dashboard shows revenue, device status and inventory levels for every machine you own, so you know when to restock before a customer finds an empty slot. '
                 'AIVS also monitors inventory and can prompt a restock.']),
             ('Training and business support', [
                 'Training is included with every machine, and the team is available for business questions after launch: pricing, stock choices, and what has worked at other sites.']),
         ],
         faqs=[
             ('What happens if the machine breaks down?', 'Repairs are covered under the monthly maintenance support plan. WhatsApp the technical support line, +65 %s, and the team will arrange the fix.' % SUP_SHOW),
             ('Is support available at night and on weekends?', 'AIVS lists 24/7 technical support for machine owners.'),
             ('Can I see sales without visiting the machine?', 'Yes. The owner dashboard shows real-time sales and inventory on your phone.'),
             ('Is the support plan compulsory?', 'Ask AIVS when you buy. The published plan is "low monthly support from only S$%s" and is designed for hands-off ownership.' % SUPPORT),
         ]),
    dict(slug='host-a-machine', short='Host a machine at your site', photo='printbox-corridor',
         gist='Malls, shops, petrol kiosks and workshops can host an AI Printbox or Topi Express at their site. Talk to us about placement.',
         title='Host a Vending Machine at Your Mall, Shop or Workshop | AIVS',
         desc='AIVS is looking for placement partners in Singapore: malls, linkways, airport halls, motorcycle shops, kiosks. Host an AI Printbox or Topi Express machine.',
         h1='Host a machine at your location',
         lede='AIVS places machines at sites with the right footfall and is open to new placement partners. If you manage a mall, shop, kiosk or workshop, we would like to talk.',
         sections=[
             ('Sites that work', [
                 'AI Printbox does well at mall entrances, atriums, MRT linkways and the airport arrival hall, where people have a few minutes to spare. Topi Express belongs where riders stop: '
                 'motorcycle workshops and accessory shops, petrol kiosks, detailing centres, and even a laundromat in Telok Blangah.']),
             ('What a host provides', [
                 'Floor space for a machine roughly the size of a drinks vending machine, a standard power point, and agreement on the placement. The machines are cashless, so no cash handling is involved.']),
             ('Current partners', [
                 'AI Printbox is in 13 locations including AMK Hub, Hillion Mall, Parkway Parade, Tampines 1, The Centrepoint and Changi Airport Terminal 3. Topi Express is at six motorcycle-related sites '
                 'including Hodaka Motoworld, BW Motorsports and Candy Motor.']),
             ('Next step', [
                 'Send us the address, the spot you have in mind and the kind of visitors you get. The team will arrange a meeting at your convenience to discuss how a placement could work.']),
         ],
         faqs=[
             ('Who looks after a hosted machine?', 'AIVS or the machine owner handles stock, maintenance and support. The host provides the space and power.'),
             ('How big is the machine?', 'About the footprint of a standard drinks vending machine. Ask for exact dimensions for the model you are interested in.'),
             ('Does the machine need cash collection?', 'No. Both machines are cashless.'),
             ('How do I propose my site?', 'WhatsApp %s or email %s with the address and a photo of the spot.' % (WA_SHOW, EMAIL)),
         ]),
    dict(slug='custom-branding', short='Custom branding and re-wrap', photo='printbox-red',
         gist='Run the machine under the AI Printbox or Topi Express brand, or re-wrap it with your own name, colours and mascot.',
         title='Custom Branded Vending Machine | Re-wrap Your AIVS Machine',
         desc='Own an AIVS machine and brand it your way: keep the AI Printbox or Topi Express wrap, or re-wrap the machine with your own branding at your own cost.',
         h1='Your machine, your brand',
         lede='Every AIVS machine can carry the established AI Printbox or Topi Express look, or a wrap of your own design.',
         sections=[
             ('Two ways to brand', [
                 'Keep the AIVS brand: AI Printbox\'s pink bear and Topi Express\'s blue-green helmet wrap are already seen in 19 locations, which helps a new site feel familiar on day one. '
                 'Or re-wrap the machine with your own branding at your own cost, for a corporate site, an event or a brand that wants the machine to match its shop.']),
             ('What stays with AIVS', [
                 'The artwork, branding and mascot designs on the AIVS wraps remain AIVS intellectual property, so they are licensed to you rather than sold. Your own wrap is yours.']),
             ('Events and pop-ups', [
                 'AI Printbox has drawn crowds at franchise exhibitions and roadshows. A branded machine can print event-themed cases on the spot, which makes it a popular activation.']),
         ],
         faqs=[
             ('Can I remove the AI Printbox or Topi Express branding?', 'Yes. You can re-wrap the machine with your own branding at your own cost.'),
             ('Can I use the AIVS mascots on my own marketing?', 'The AIVS artwork, branding and mascots stay AIVS intellectual property. Ask AIVS before using them outside the machine.'),
             ('Can the printed designs be branded too?', 'Ask AIVS. The AI Printbox design collection is managed centrally, and event or brand designs can be discussed.'),
         ]),
]
SVC = {s['slug']: s for s in SERVICES}


def service_body(s):
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % p for p in ps)) for h, ps in s['sections'])
    rel = ''.join(tile('machines/%s/' % m['slug'], m['photo'], m['short'], m['gist'], 'From S$%s · More details →' % m['price']) for m in MACHINES)
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(s['photo'], eager=True)}</figure>
{qa_html(s['slug'])}
{secs}
<h2>The machines</h2>
<div class="scards">{rel}</div>
<h2>Frequently asked questions</h2>
{faq_html(s['faqs'])}
<p class="byline">Facts on this page come from AIVS\'s published ownership terms. Last checked {UPDATED}.</p>
</article>
<aside class="side"><div class="card sticky"><h2>Talk to AIVS</h2><p>WhatsApp {WA_SHOW} or email {EMAIL}. Tell us which machine and where you would place it.</p>{wa_btn('WhatsApp us', topic=s['short'].lower() + '.')}{mail_btn()}
<p class="small" style="margin-top:14px"><a href="prices/">Prices →</a><br><a href="locations/">Current locations →</a></p></div></aside>
</div></section>'''


# ----------------------------------------------------------------------------------------------
# Articles
# ----------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='how-much-does-a-vending-machine-cost-in-singapore', photo='printbox-mall',
         title='How Much Does a Vending Machine Cost in Singapore?',
         desc='AIVS prices: a refurbished Topi Express helmet cleaning machine from S$%s, an AI Printbox phone case machine from S$%s, 0%% royalties.' % (TP_PRICE, PB_PRICE),
         h1='How much does a vending machine cost in Singapore?',
         answer='At AIVS, a refurbished Topi Express helmet cleaning machine is from S$%s and a refurbished AI Printbox phone case printing machine is from S$%s. Both come with a hardware warranty, 0%% royalties and an optional support plan from S$%s a month. Stock is bought from AIVS at cost price.' % (TP_PRICE, PB_PRICE, SUPPORT),
         sections=[
             ('What the machine price covers', ['The published prices are for refurbished machines: units that AIVS has reconditioned, with a 1-year hardware warranty on AI Printbox and 6 months on Topi Express (terms apply). Training is included. Ask whether delivery, installation and GST are in the figure for your order.']),
             ('The running costs', ['Three costs recur: the location (rent or a revenue share agreed with the host), stock (phone cases for AI Printbox, disinfectant for Topi Express, bought from AIVS at cost price), and the monthly support plan from S$%s that covers maintenance and system support. Power is a standard 3-pin plug.' % SUPPORT]),
             ('What AIVS does not charge', ['There is no franchise fee and no royalty on sales. You own the machine, so the asset is yours to keep, move or re-wrap.']),
             ('Which machine for which budget', ['Topi Express is the lower entry point at S$%s and suits anyone with access to a motorcycle shop, petrol kiosk or workshop. AI Printbox at S$%s is the higher-footfall machine, built for malls and the airport, where a S$%s custom case sells to shoppers and gift buyers.' % (TP_PRICE, PB_PRICE, CASE_PRICE)]),
         ],
         faqs=[('Can I pay for a machine in instalments?', 'Ask AIVS on WhatsApp %s; payment terms are discussed per order.' % WA_SHOW),
               ('Are new machines available, or only refurbished?', 'The published "from" prices are for refurbished machines. Ask AIVS about new units.'),
               ('Is the support plan compulsory?', 'Ask when you buy. It is designed so you do not have to handle maintenance yourself.')]),
    dict(slug='how-to-start-a-vending-machine-business-in-singapore', photo='printbox-event',
         title='How to Start a Vending Machine Business in Singapore',
         desc='Pick a machine, secure a location, agree terms with the host, set up payment, stock and support, then track sales. How AIVS machine owners start.',
         h1='How to start a vending machine business in Singapore',
         answer='Choose a machine that fits a location you can secure, agree the placement with the site owner, buy the machine, set up cashless payment and stock, and track sales from your phone. With AIVS you can be running within a few weeks of confirming the machine and the site, with training included.',
         sections=[
             ('Step 1: start with the location, not the machine', ['Vending lives or dies on footfall. Walk the site at the times your customers would be there. For a phone case machine that means mall entrances, linkways and the airport; for a helmet cleaning machine it means motorcycle shops, petrol kiosks and workshops.']),
             ('Step 2: agree terms with the host', ['Hosts usually want either rent or a share of sales, plus a tidy, cashless machine that does not create work. Both AIVS machines are cashless and self-service.']),
             ('Step 3: buy the machine', ['AIVS sells refurbished machines outright: Topi Express from S$%s, AI Printbox from S$%s, each with a hardware warranty and no royalties.' % (TP_PRICE, PB_PRICE)]),
             ('Step 4: set up payment, stock and support', ['Payment is by QR code (cards can be arranged). Stock comes from AIVS at cost price. The monthly support plan from S$%s covers maintenance and system support, and training is included.' % SUPPORT]),
             ('Step 5: run it from your phone', ['The owner dashboard shows revenue, device status and inventory, so you restock before a slot runs empty and see which days sell best.']),
             ('Register the business', ['Register a sole proprietorship or company with ACRA, and check with your host whether any mall or landlord approvals apply to the exact spot.']),
         ],
         faqs=[('Do I need a shop or staff?', 'No. Both AIVS machines are self-service and cashless, so no shop or staff is required.'),
               ('How long until the machine is running?', 'Typically a few weeks after you confirm the machine and the location.'),
               ('Do I need vending experience?', 'No. Training and ongoing support are included.')]),
    dict(slug='print-a-custom-phone-case-in-3-minutes', photo='case-deer',
         title='Where to Print a Custom Phone Case in 3 Minutes in Singapore',
         desc='Print your own photo on a phone case for S$%s in 3 minutes at AI Printbox. 13 locations including AMK Hub, Tampines 1, Parkway Parade and Changi Airport T3.' % CASE_PRICE,
         h1='Print a custom phone case in 3 minutes',
         answer='Find an AI Printbox machine, choose your phone model, pick a design or upload your own photo, pay cashlessly, and collect your printed case about 3 minutes later. A case is S$%s. There are 13 machines across Singapore, including AMK Hub, Hougang Mall, Tampines 1, Parkway Parade, The Centrepoint and Changi Airport Terminal 3.' % CASE_PRICE,
         sections=[
             ('How it works', ['Tap the screen and select your phone model (latest iPhone and Samsung models supported). Choose a design from the collection, add an AI filter, or upload your own photo. Pay, and the machine prints the design into a durable protective case while you wait.']),
             ('Good photos to use', ['Clear, well-lit photos with the subject in the middle work best, because the case is narrow and tall. Pets, couples, group shots and holiday skylines are the popular choices.']),
             ('Privacy and refunds', ['Uploaded photos are deleted from the system within 48 hours and are not stored or shared. Because each case is printed to order, purchases are non-refundable, and you are responsible for the content you print.']),
             ('Where to find a machine', ['See the full list with unit numbers on the AI Printbox locations page. Machines at mall entrances and the Changi Airport arrival hall are the easiest to find.']),
         ],
         faqs=[('How much is a custom phone case at AI Printbox?', 'S$%s, as published by AIVS. Check the machine for the current price.' % CASE_PRICE),
               ('Can I print a photo from my phone?', 'Yes. Upload your own image at the machine, or choose from the design collection.'),
               ('Is the design a sticker?', 'No. The print is built into the case itself.')]),
    dict(slug='how-to-clean-and-disinfect-a-motorcycle-helmet', photo='topi-helmet',
         title='How to Clean and Disinfect a Motorcycle Helmet in Singapore',
         desc='Hand washing a helmet liner takes a day to dry. A Topi Express machine disinfects, deodorises and sterilises a helmet in 5 minutes for S$%s.' % WASH_PRICE,
         h1='How to clean and disinfect a motorcycle helmet',
         answer='Remove and hand wash the liner if your helmet allows it, wipe the shell with a mild soap, and let everything dry out of direct sun, which can take a day. For a quick refresh between washes, a Topi Express machine disinfects, deodorises and sterilises the whole helmet with UVC and a disinfectant mist in about 5 minutes for S$%s.' % WASH_PRICE,
         sections=[
             ('Why helmets smell in Singapore', ['Daily riding in heat and humidity leaves sweat in the liner, and a damp liner is where bacteria and odour build up. A helmet that is never aired or cleaned also wears out faster.']),
             ('Cleaning at home', ['Check whether the liner and cheek pads come out. If they do, hand wash them in mild soap, rinse well and air dry away from direct sun. Wipe the shell and visor with a soft cloth and mild soap. Never use solvents on the shell or visor.']),
             ('Cleaning in 5 minutes', ['At a Topi Express machine, place the helmet in the chamber, pay by QR code and wait about 5 minutes while UVC light and an eco-friendly disinfectant treat the helmet. It suits riders who want a refresh on the way to or from work without a day of drying.']),
             ('Where the machines are', ['Six locations: Wheels & Cycles (Woodlands), 345 Wash (Telok Blangah), Candy Motor and Gusto Broz Workshop (Kaki Bukit Road 4), BW Motorsports (Old Toh Tuck Road) and Hodaka Motoworld (Kaki Bukit Road 1, 24 hours).']),
         ],
         faqs=[('How often should I clean my helmet?', 'Wipe the shell weekly and clean or refresh the liner regularly if you ride daily in Singapore\'s heat.'),
               ('Is UVC safe for the helmet?', 'The Topi Express cycle is designed for helmets and runs for about 5 minutes. Follow the on-screen instructions.'),
               ('How much does a helmet clean cost at Topi Express?', 'S$%s per 5-minute clean, as published by AIVS.' % WASH_PRICE)]),
    dict(slug='best-locations-for-a-vending-machine-in-singapore', photo='printbox-escalator',
         title='Best Locations for a Vending Machine in Singapore',
         desc='Where machines work in Singapore, from 19 live AIVS placements: mall entrances, MRT linkways, the airport arrival hall, motorcycle workshops and kiosks.',
         h1='Best locations for a vending machine in Singapore',
         answer='The best location is where your exact customer already waits for a few minutes. AIVS\'s 13 AI Printbox machines sit at mall entrances, MRT linkways and Changi Airport Terminal 3; its 6 Topi Express machines sit at motorcycle workshops, an accessory shop, a dealer and a laundromat. Match the product to the crowd, then check footfall at the hours that matter.',
         sections=[
             ('Malls: entrances, atriums and linkways', ['AI Printbox machines are placed at the entrances of specific shops (Bukit Panjang Plaza, Eastpoint Mall, Tampines 1, Sembawang Shopping Centre), in atriums and lobbies (AMK Hub Level 3 Lobby B), and in the Hillion Mall linkway to Bukit Panjang MRT. People slow down at these points.']),
             ('The airport', ['Changi Airport Terminal 3 has two AI Printbox machines: one in the Arrival Hall and one in Basement 2. Travellers waiting for pickups and families meeting arrivals have time and a souvenir in mind.']),
             ('Where riders stop', ['Topi Express works at the places riders already visit: Hodaka Motoworld and Candy Motor in Kaki Bukit, BW Motorsports in Old Toh Tuck Road, Wheels & Cycles in Woodlands. A laundromat (345 Wash in Telok Blangah) works too, because a wash cycle is a natural wait.']),
             ('How to judge a site', ['Count people at the hours you expect to sell. Check there is a power point and a clear line of sight. Agree who looks after the space. Both AIVS machines are cashless, which hosts prefer.']),
             ('Get help with a site', ['You choose and secure your own location, and AIVS can help with site sourcing. If you manage a site and want a machine, see the host-a-machine page.']),
         ],
         faqs=[('Does AIVS find the location for me?', 'You choose and secure your own location; AIVS shares its experience and can help with site sourcing.'),
               ('Can a machine be moved if a site does not work?', 'Yes. Tell AIVS in advance and transport can be arranged.'),
               ('Do hosts charge rent?', 'Usually rent or a share of sales, agreed between you and the host.')]),
    dict(slug='vending-machine-franchise-vs-owning-your-own-machine', photo='topi-franchise',
         title='Vending Machine Franchise vs Owning Your Own Machine',
         desc='A franchise charges a fee and a share of sales; AIVS sells you the machine outright with 0% royalties, cost-price stock and optional support. The comparison.',
         h1='Vending machine franchise vs owning your own machine',
         answer='In a franchise you pay an entry fee and a royalty on sales for the right to use a brand and system. With AIVS you buy the machine outright, pay no royalties, can use the AI Printbox or Topi Express brand or your own, and add a support plan from S$%s a month only if you want it. You own the asset either way you brand it.' % SUPPORT,
         table=[('', 'Typical franchise', 'AIVS ownership'), ('Upfront', 'Franchise fee plus equipment', 'Machine price only (from S$%s)' % TP_PRICE), ('Ongoing', 'Royalty on sales', '0%% royalties; optional support from S$%s/month' % SUPPORT),
                ('Brand', 'Franchisor brand, fixed', 'AIVS brand or your own wrap'), ('Stock', 'Franchisor pricing', 'Cost price from AIVS'), ('Location', 'Often assigned', 'You choose; AIVS helps'), ('The asset', 'Terms vary', 'Yours to keep, move or re-wrap')],
         sections=[
             ('When a franchise makes sense', ['When you want a fully prescribed system and are happy to pay for it on every sale. Some operators prefer that trade.']),
             ('When ownership makes sense', ['When you want to keep what the machine earns, control the location and the branding, and still have support on call. AIVS\'s model is built for this: you own the machine, AIVS supplies stock at cost price, trains you and maintains the machine under a monthly plan.']),
             ('What AIVS keeps', ['The AI Printbox and Topi Express artwork, branding and mascots stay AIVS intellectual property. If you re-wrap in your own brand, that wrap is yours.']),
         ],
         faqs=[('Is AIVS a franchise?', 'AIVS describes its partners as franchise partners who own their machines with 0% royalties. In practice you buy the machine and keep the sales.'),
               ('Can I leave the AIVS brand later?', 'Yes. Re-wrap the machine in your own branding at your own cost.'),
               ('Is support included or optional?', 'Support is a monthly plan from S$%s. Ask AIVS whether it is required for your machine.' % SUPPORT)]),
    dict(slug='ai-printbox-now-at-14-locations-across-singapore', photo='printbox-queue',
         title='AI Printbox Is Now at 13 Locations Across Singapore',
         desc='From four malls in June 2025 to 13 locations including Changi Airport Terminal 3, AMK Hub, Parkway Parade and The Centrepoint: where to find AI Printbox now.',
         h1='AI Printbox is now at 13 locations across Singapore',
         answer='AI Printbox, the 3-minute custom phone case machine, has grown from four mall locations announced in June 2025 to 13 machines, including two at Changi Airport Terminal 3. The full list with unit numbers is on the AI Printbox locations page.',
         sections=[
             ('How it grew', ['In June 2025 AIVS announced AI Printbox at VivoCity, Sembawang Shopping Centre, Great World and Eastpoint Mall. The current list has 13 machines: AMK Hub, Bukit Panjang Plaza, Changi Airport T3 (Arrival Hall and Basement 2), Changi City Point, City Square Mall, Eastpoint Mall, Hillion Mall, Hougang Mall, Parkway Parade, Sembawang Shopping Centre, Tampines 1 and The Centrepoint.']),
             ('Why it spreads', ['A S$%s case printed with your own photo in 3 minutes is an easy gift and an easy treat, and the machine draws a crowd wherever it stands, as it did at a franchise exhibition where visitors queued to try it.' % CASE_PRICE]),
             ('For future owners', ['Every one of these machines is the same model you can own, from S$%s refurbished, with 0%% royalties.' % PB_PRICE]),
         ],
         faqs=[('Is AI Printbox at VivoCity?', 'VivoCity and Great World were announced in June 2025 but are not on the current AIVS location list. Check the locations page for the live list.'),
               ('Which Changi Airport terminal has AI Printbox?', 'Terminal 3: the Arrival Hall (#01-VM4) and Basement 2 (iClaw, #B2-45).')]),
    dict(slug='topi-express-helmet-cleaning-at-hodaka-motoworld', photo='topi-shop',
         title='Topi Express Now Runs 24 Hours at Hodaka Motoworld',
         desc='Since 22 August 2025 a Topi Express machine has run around the clock at Hodaka Motoworld, 10 Kaki Bukit Road 1: a 5-minute helmet clean at any hour.',
         h1='Topi Express runs 24 hours at Hodaka Motoworld',
         answer='On 22 August 2025 AIVS placed a Topi Express helmet cleaning machine at Hodaka Motoworld Pte Ltd, 10 Kaki Bukit Road 1, #01-09, KB Industrial Building. The machine runs 24 hours a day, so riders can clean and disinfect a helmet in 5 minutes for S$%s even after the shop has closed.' % WASH_PRICE,
         sections=[
             ('Why Hodaka', ['Hodaka Motoworld is one of Singapore\'s best-known motorcycle names, especially among Honda riders, selling motorcycles, gear and accessories. Riders already stop there, which is exactly where a helmet cleaning machine belongs.']),
             ('What riders get', ['A 5-minute cycle that disinfects, deodorises and sterilises the helmet with UVC and an eco-friendly disinfectant mist, paid by QR code, at any hour.']),
             ('Other Topi Express machines', ['Wheels & Cycles (Woodlands), 345 Wash (Telok Blangah), Candy Motor and Gusto Broz Workshop (Kaki Bukit Road 4) and BW Motorsports (Old Toh Tuck Road).']),
         ],
         faqs=[('What are the hours at Hodaka Motoworld\'s Topi Express?', 'The machine runs 24 hours a day.'),
               ('How much is a helmet clean?', 'S$%s for about 5 minutes, as published by AIVS.' % WASH_PRICE)]),
    dict(slug='which-phones-can-a-phone-case-printing-machine-print-for', photo='case-dragon', date='2026-10-26',
         title='Which Phones Can a Case Printing Machine Print For?',
         desc='Which phones can a phone case printing machine print for? What AI Printbox supports, how to check your model first, and what to do if it is not listed.',
         h1='Which phones can a phone case printing machine print for?',
         answer='A phone case printing machine prints only for the phone models on its own list, because each case must match a phone\'s exact size, camera cut-out and buttons. AIVS says AI Printbox supports the latest iPhone and Samsung models, and the list is updated as new phones are released. The machine screen shows the models available, so you can check before you pay.',
         byline='General information; AIVS facts from its published machine pages only.',
         sections=[
             ('Which phones does AI Printbox support?', ['AIVS says the AI Printbox supports the latest iPhone and Samsung models. It does not publish a fixed list of every model, because the list changes as new phones launch. The first step on the touchscreen is to select your phone model, and the machine shows the models it can print for at that time.']),
             ('Why can\'t a machine print for every phone?', ['A printed case is a physical case made for one phone shape. The camera cut-out, button positions and edges are different on every model, so a machine can only print for the models whose cases it holds in stock. It is also why a very new or less common phone may not be listed yet.']),
             ('How do you check your phone before you go?', ['The most reliable check is the machine itself: the screen lists the available models before you pick a design or pay. If you want to be sure first, ask AIVS through the <a href="contact/">contact page</a> and name your exact model. You can find the machines in malls and at Changi Airport on the <a href="locations/ai-printbox/">AI Printbox locations page</a>.']),
             ('What if your phone is not on the list?', ['You can check again after a few weeks if your phone is new, since the list is updated as phones are released. A custom case can also be a gift: choose the recipient\'s phone model instead of your own. If your model never appears, a printing machine may not be the right way to get a custom case for that phone.']),
             ('What does the printing cost, and how long does it take?', ['A custom case takes about 3 minutes and costs S$%s, as published by AIVS. The steps are in <a href="articles/print-a-custom-phone-case-in-3-minutes/">print a custom phone case in 3 minutes</a>. Check the machine for the current price.' % CASE_PRICE]),
             ('What does the model list mean for machine owners?', ['Owners of an AI Printbox buy phone case stock from AIVS at partner pricing, and the supported-model list is kept up to date by AIVS as phones are released. Read <a href="machines/ai-printbox/">how the AI Printbox machine works</a>, or <a href="services/own-a-vending-machine/">how owning a machine works</a>.']),
         ],
         faqs=[('Does AI Printbox print for Samsung phones as well as iPhones?', 'Yes. AIVS says AI Printbox supports the latest iPhone and Samsung models, and the list is updated as new phones are released.'),
               ('Where can I see the list of supported phones?', 'On the machine itself. The interface shows the models available at the time of printing, so you can check before you pay.'),
               ('How much is a printed case and how long does it take?', 'About 3 minutes, for S$%s a case, as published by AIVS. Check the machine for the current price.' % CASE_PRICE)]),
    dict(slug='can-you-run-a-vending-machine-business-part-time', photo='dashboard', date='2026-10-28',
         title='Can You Run a Vending Machine Business Part-Time?',
         desc='Can you run a vending machine business part-time in Singapore? What a self-service machine does on its own, what still needs you, and what to ask first.',
         h1='Can you run a vending machine business part-time in Singapore?',
         answer='It can be, because AIVS machines are self-service and cashless, so no shop or staff is needed at the machine, and the owner dashboard shows revenue, device status and inventory on your phone. How much time it takes depends on how many machines you run, how far they are from you and how often they need restocking. AIVS does not publish an hours-per-week figure, so ask before you buy.',
         byline='AIVS facts from its published machine, support and ownership pages only; no earnings or time figures are claimed.',
         sections=[
             ('What does the machine do without you?', ['Both AIVS machines are self-service. A customer chooses, pays by QR code and collects, with no staff at the machine. AI Printbox prints a custom phone case in about 3 minutes; Topi Express cleans a helmet in about 5 minutes. Because payment is cashless, there is no cash to collect from the machine.']),
             ('What still needs a person?', ['A vending machine is low-effort rather than hands-off. Someone still restocks it (phone cases for AI Printbox, disinfectant for Topi Express), checks it, and keeps a good relationship with the host of the space. The owner dashboard helps by showing revenue, device status and inventory, so you can restock before a slot runs empty instead of visiting on a fixed schedule.']),
             ('Who looks after faults?', ['The optional support plan from S$%s a month covers maintenance and repairs, system support and 24/7 technical help, so a fault does not have to be fixed by you in the evening. Read what it covers on the <a href="services/support-and-maintenance/">support and maintenance page</a>.' % SUPPORT]),
             ('Why the location matters for a part-time owner', ['You choose and secure the location, and AIVS can help with site sourcing. A site close to your home or workplace makes restocking easier to fit around a job, and a site with steady footfall matters more than a convenient one that nobody walks past. See <a href="articles/best-locations-for-a-vending-machine-in-singapore/">best locations for a vending machine in Singapore</a>.']),
             ('What to ask AIVS before you buy', ['Ask how often a machine like yours is usually restocked, how stock is delivered to you, what the support plan includes and how quickly help responds. AIVS does not publish earnings figures, so ask for real usage numbers from comparable sites rather than relying on a promise. The full ownership steps are in <a href="articles/how-to-start-a-vending-machine-business-in-singapore/">how to start a vending machine business in Singapore</a>, and the model is on the <a href="services/own-a-vending-machine/">own a vending machine page</a>.']),
         ],
         faqs=[('Do I need a shop or staff to run one?', 'No. AIVS machines are self-service and cashless, so no shop or staff is needed at the machine.'),
               ('Can I see sales without visiting the machine?', 'Yes. The owner dashboard shows revenue, device status and inventory from your phone.'),
               ('Who fixes the machine if something goes wrong?', 'The optional support plan from S$%s a month covers maintenance and repairs, system support and 24/7 technical help.' % SUPPORT)]),
]
ART = {a['slug']: a for a in ARTICLES}


def article_body(a):
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % p for p in ps)) for h, ps in a['sections'])
    table = ''
    if a.get('table'):
        hdr, rows = a['table'][0], a['table'][1:]
        table = '<table class="cmp"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (
            ''.join('<th>%s</th>' % E(c) for c in hdr), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % E(c) for c in r) for r in rows))
    rel = ''.join(tile('machines/%s/' % m['slug'], m['photo'], m['short'], m['gist'], 'From S$%s · More details →' % m['price']) for m in MACHINES)
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">{E(a['answer'])}</p>
<figure class="lead-fig">{img(a['photo'], eager=True)}</figure>
{table}{secs}
<h2>Frequently asked questions</h2>
{faq_html(a['faqs'])}
<h2>The machines</h2>
<div class="scards">{rel}</div>
<p class="byline">By the AIVS team, {LEGAL}. Last updated {a.get('date', UPDATED)}. {a.get('byline', 'Facts from AIVS' + chr(39) + 's published machine details and location list.')}</p>
</article>
<aside class="side"><div class="card sticky"><h2>Ask AIVS</h2><p>Own a machine from S${TP_PRICE}, or host one at your site. WhatsApp {WA_SHOW}.</p>{wa_btn('WhatsApp us')}{enquire_btn(cls='btn btn-ghost')}
<p class="small" style="margin-top:14px"><a href="prices/">Prices →</a><br><a href="locations/">Locations →</a><br><a href="articles/">All articles →</a></p></div></aside>
</div></section>'''


def article_schema(a, path):
    return {'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': a.get('date', UPDATED), 'dateModified': a.get('date', UPDATED),
            'author': {'@type': 'Organization', 'name': LEGAL, 'url': SITE}, 'publisher': {'@id': SITE + '#business'},
            'image': (IMG_ABS or SITE + 'img/') + '%s.webp' % a['photo'], 'mainEntityOfPage': SITE + path, 'inLanguage': 'en-SG'}


def article_card(a):
    return '<a class="acard" href="articles/%s/">%s<span><b>%s</b>%s</span></a>' % (a['slug'], img(a['photo'], sm=True), E(a['h1']), E(a['desc']))


# ----------------------------------------------------------------------------------------------
# Home, hubs, about, contact, prices, terms, privacy
# ----------------------------------------------------------------------------------------------
FAQ_HOME = [
    ('What does AIVS sell?', 'Two self-service machines you can own: AI Printbox, which prints custom phone cases in 3 minutes, and Topi Express, which cleans and disinfects a helmet in 5 minutes. Both are sold refurbished with a warranty and 0% royalties.'),
    ('How much does it cost to own a machine?', 'Topi Express from S$%s and AI Printbox from S$%s, refurbished, plus an optional support plan from S$%s a month. Stock is supplied at cost price.' % (TP_PRICE, PB_PRICE, SUPPORT)),
    ('Do I need experience or staff?', 'No. The machines are self-service and cashless, training is included, and AIVS handles maintenance under the support plan.'),
    ('Where are AIVS machines today?', '19 locations in Singapore: 13 AI Printbox machines in malls and Changi Airport Terminal 3, and 6 Topi Express machines at motorcycle shops, workshops and a laundromat.'),
    ('Is there a franchise fee or royalty?', 'No. You buy the machine outright, there is no franchise fee and AIVS takes 0%% royalties on your sales. You pay for stock, which AIVS supplies at cost price, and an optional support plan from S$%s a month.' % SUPPORT),
    ('What warranty comes with a machine?', 'AI Printbox comes with a 1-year hardware warranty and Topi Express with a 6-month hardware warranty. Warranty terms apply, so ask on WhatsApp for the details before you buy.'),
    ('Who finds the location for my machine?', 'You choose and secure the location. AIVS shares what works from its own placements, such as AMK Hub and Changi Airport Terminal 3, and can help with site finding.'),
]


def home_body():
    svc = ''.join(tile('services/%s/' % s['slug'], s['photo'], s['short'], s['gist']) for s in SERVICES)
    kw = ''.join(tile(k['slug'] + '/', k['photo'], k['short'], k['lede'].split('. ')[0] + '.') for k in KEYWORD_PAGES)
    arts = ''.join(article_card(a) for a in ARTICLES[:3])
    gallery = ''.join('<figure>%s</figure>' % img(n) for n in ('printbox-event', 'printbox-queue', 'case-dragon', 'topi-345wash', 'topi-helmet'))
    return f'''<style>.hero-in{{opacity:1!important}}</style>
<section class="hero">
<div class="hero-bg" data-slides="topi-shop,printbox-crowd">{img('printbox-mall-dark', eager=True)}</div>
<div class="wrap hero-in">
<p class="eyebrow">Own the machine · 0% royalties · Singapore</p>
<h1>Own a self-service vending machine that pays you, not a franchisor.</h1>
<p class="lede">AIVS (AI Vending Solution Pte. Ltd.) sells refurbished AI Printbox phone case printers and Topi Express helmet cleaners to owner-operators, from S${TP_PRICE}. You keep the sales; we supply stock at cost, train you and maintain the machine.</p>
<div class="cta-row">{wa_btn('WhatsApp us')}<a class="btn btn-gold" href="machines/">See the machines</a></div>
<div class="hero-chips"><span>From S${TP_PRICE}</span><span>Hardware warranty</span><span>Support from S${SUPPORT}/month</span><span>19 live locations</span></div>
</div></section>
<section class="showcase" aria-label="The two machines"><div class="wrap sc-grid">
<a class="sc-card" href="machines/ai-printbox/"><div class="sc-media">{video('ai-printbox')}</div><div class="sc-body"><span class="sc-tag">AI Printbox</span><h3>Print a phone case in 3 minutes</h3><p>From S${PB_PRICE} · 13 locations</p><span class="sc-go">See the machine →</span></div></a>
<a class="sc-card" href="machines/topi-express/"><div class="sc-media">{img('topi-shop')}</div><div class="sc-body"><span class="sc-tag tp">Topi Express</span><h3>Clean a helmet in 5 minutes</h3><p>From S${TP_PRICE} · 6 locations</p><span class="sc-go">See the machine →</span></div></a>
</div></section>
{VID_JS}
<section class="stats" aria-label="AIVS at a glance"><div class="wrap">
<div class="stat"><b data-to="19">19</b><span>Machines live in Singapore</span><small>13 AI Printbox, 6 Topi Express</small></div>
<div class="stat"><b data-to="3" data-suf=" min">3 min</b><span>To print a phone case</span><small>AI Printbox</small></div>
<div class="stat"><b data-to="5" data-suf=" min">5 min</b><span>To clean a helmet</span><small>Topi Express</small></div>
<div class="stat"><b data-to="0" data-suf="%">0%</b><span>Royalties</span><small>you own the machine</small></div>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-s"><div class="wrap">
<div class="sec-head"><p class="eyebrow">How it works</p><h2 id="h-s">You own it. We help you run it.</h2></div>
<div class="scards">{svc}</div>
</div></section>
<section class="sec" aria-labelledby="h-kw"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Looking for a machine?</p><h2 id="h-kw">One contact for AI and smart vending machines in Singapore</h2><p>AIVS sells its own refurbished machines and is building a network of partner suppliers for other machine types. Tell us what you want to sell and where, and we point you to the machine that fits. Supplier or distributor of AI or smart machines? <a href="partner-with-aivs/">Partner with AIVS</a>.</p></div>
<div class="scards">{kw}</div>
</div></section>
<section class="sec sec-dark" aria-labelledby="h-why"><div class="wrap split2">
<div><p class="eyebrow">Why owners choose AIVS</p><h2 id="h-why">A proven machine, a brand shoppers know, and nobody taking a cut.</h2>
<ul class="ticks">
<li><b>Stock at cost price.</b> Phone cases and disinfectant come from AIVS at cost, so your margin stays yours.</li>
<li><b>Training and support.</b> Free training, a support plan from S${SUPPORT} a month, 24/7 technical help and a live dashboard on your phone.</li>
</ul>
<a class="btn btn-gold" href="services/own-a-vending-machine/">How ownership works</a></div>
<div class="gallery">{gallery}</div>
</div></section>
<section class="sec" aria-labelledby="h-loc"><div class="wrap">
<div class="sec-head"><p class="eyebrow">19 live locations</p><h2 id="h-loc">Where to find an AIVS machine</h2><p>Every machine below is running in Singapore today. Thinking of owning one? Visit a machine first and watch how people use it: the queue, the wait and the moment they decide to pay.</p></div>
<div class="split2">
<div><h3>AI Printbox: 13 locations</h3><p>AMK Hub, Bukit Panjang Plaza, Changi Airport Terminal 3 (Arrival Hall and Basement 2), Changi City Point, City Square Mall, Eastpoint Mall, Hillion Mall, Hougang Mall, Parkway Parade, Sembawang Shopping Centre, Tampines 1 and The Centrepoint. Shoppers print their own photo or a design on a phone case for S${CASE_PRICE} in about 3 minutes.</p></div>
<div><h3>Topi Express: 6 locations</h3><p>Wheels &amp; Cycles in Woodlands, 345 Wash in Telok Blangah, Candy Motor and Gusto Broz Workshop on Kaki Bukit Road 4, BW Motorsports on Old Toh Tuck Road and Hodaka Motoworld on Kaki Bukit Road 1, where the machine has run 24 hours a day since 22 August 2025. Riders clean and disinfect a helmet for S${WASH_PRICE} in about 5 minutes.</p></div>
</div>
<p style="margin-top:20px"><a class="btn btn-ghost" href="locations/">All locations with unit numbers</a></p>
</div></section>
<section class="sec" aria-labelledby="h-art"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Guides</p><h2 id="h-art">Thinking about a vending business?</h2></div>
<div class="acards">{arts}</div>
<p style="margin-top:20px"><a class="btn btn-ghost" href="articles/">All articles</a></p>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-faq"><div class="wrap narrow">
<div class="sec-head"><h2 id="h-faq">Quick answers</h2></div>
{faq_html(FAQ_HOME)}
</div></section>'''


def machines_index():
    return f'''<section class="sec"><div class="wrap">{machine_cards()}
<p class="small" style="margin-top:20px">{E(PRICE_NOTE)}</p></div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Compare the two machines</h2></div>
<table class="cmp"><thead><tr><th></th><th>AI Printbox</th><th>Topi Express</th></tr></thead><tbody>
<tr><td>What it does</td><td>Prints a custom phone case in about 3 minutes</td><td>Disinfects, deodorises and sterilises a helmet in about 5 minutes</td></tr>
<tr><td>Machine price</td><td>From S${PB_PRICE}, refurbished</td><td>From S${TP_PRICE}, refurbished</td></tr>
<tr><td>Hardware warranty</td><td>1 year*</td><td>6 months*</td></tr>
<tr><td>Retail price</td><td>S${CASE_PRICE} per case</td><td>S${WASH_PRICE} per clean</td></tr>
<tr><td>Best sites</td><td>Mall entrances, linkways, airport halls</td><td>Motorcycle shops, petrol kiosks, workshops</td></tr>
<tr><td>Live today</td><td>13 locations</td><td>6 locations</td></tr>
<tr><td>Royalties</td><td>0%</td><td>0%</td></tr>
</tbody></table><p class="small">* Warranty terms apply.</p></div></section>'''


def services_index():
    cards = ''.join(tile('services/%s/' % s['slug'], s['photo'], s['short'], s['gist']) for s in SERVICES)
    return f'''<section class="sec"><div class="wrap"><div class="scards">{cards}</div></div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>From enquiry to first sale</h2></div>
<div class="steps">
<div class="step"><b>Choose a machine</b><span>AI Printbox for shoppers, Topi Express for riders. We help you match the machine to the site you have in mind.</span></div>
<div class="step"><b>Secure the location</b><span>You choose and secure the spot; AIVS shares what works and can help with site sourcing.</span></div>
<div class="step"><b>Set up and train</b><span>The machine is delivered and set up, payment is configured, and you are trained to run it.</span></div>
<div class="step"><b>Sell and track</b><span>Stock at cost price, support from S${SUPPORT} a month, and a dashboard that shows sales and inventory on your phone.</span></div>
</div></div></section>'''


def locations_index():
    return f'''<section class="sec"><div class="wrap">
<div class="sec-head"><p class="eyebrow">AI Printbox · 13 locations</p><h2>Print a custom phone case</h2><p>Malls across Singapore and Changi Airport Terminal 3. <a href="locations/ai-printbox/">Full details →</a></p></div>
{loc_cards(PB_LOCS, 'pb')}
<div class="sec-head"><p class="eyebrow">Topi Express · 6 locations</p><h2>Clean a helmet in 5 minutes</h2><p>Motorcycle shops, workshops and a laundromat. <a href="locations/topi-express/">Full details →</a></p></div>
{loc_cards(TP_LOCS, 'tp')}
<p class="small">Locations as published by AIVS on {UPDATED}. Machines can move; WhatsApp AIVS if you cannot find one.</p>
</div></section>'''


def locations_machine(m, locs, intro):
    cls = m['theme']
    return f'''<section class="sec {cls}"><div class="wrap">
<div class="split2"><div><p>{E(intro)}</p>{wa_btn('WhatsApp us', topic='a %s location.' % m['short'])} <a class="btn btn-ghost" href="machines/{m['slug']}/">About the machine</a></div><figure style="margin:0">{img(m['photo'], eager=True, cls='')}</figure></div>
<h2 style="margin-top:40px">All {E(m['short'])} locations</h2>
{loc_cards(locs, cls)}
<p class="small">Locations as published by AIVS on {UPDATED}. Want one near you, or at your site? <a href="services/host-a-machine/">Host a machine →</a></p>
</div></section>'''


def prices_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">AIVS publishes its prices. A refurbished Topi Express helmet cleaning machine is from S${TP_PRICE} and a refurbished AI Printbox phone case machine is from S${PB_PRICE}. Support plans start at S${SUPPORT} a month. There are no franchise fees and no royalties, and stock is supplied at cost price.</p>
<h2>Machines</h2>
{plist([('AI Printbox, refurbished', 'From S$' + PB_PRICE, '1-year hardware warranty*, training included'), ('Topi Express, refurbished', 'From S$' + TP_PRICE, '6-month hardware warranty*, training included')])}
<h2>Running costs</h2>
{plist([('Monthly support plan', 'From S$' + SUPPORT + '/month', 'Maintenance, system support, 24/7 technical help; Topi Express disinfectant top-ups'), ('Stock', 'Cost price', 'Phone cases and disinfectant supplied by AIVS'), ('Royalties', 'S$0', 'You own the machine and keep the sales'), ('Re-wrap with your own branding', 'At your cost', 'Optional')])}
<h2>What customers pay</h2>
{plist([('Custom printed phone case (AI Printbox)', 'S$' + CASE_PRICE, 'About 3 minutes'), ('Helmet clean (Topi Express)', 'S$' + WASH_PRICE, 'About 5 minutes')])}
<p class="small">* Warranty terms apply. {E(PRICE_NOTE)} Customer prices are as published by AIVS; the machine shows the current price.</p>
<h2>Frequently asked questions</h2>
{faq_html([('Is GST included in the machine price?', 'Ask AIVS on WhatsApp %s. The published figures are "from" prices for refurbished machines.' % WA_SHOW), ('Is there a franchise fee?', 'No. AIVS charges no franchise fee and 0% royalties.'), ('What does the S$%s support plan cover?' % SUPPORT, 'Maintenance and repairs, system support and 24/7 technical help. For Topi Express it also covers disinfectant top-ups.')])}
</article>
<aside class="side"><div class="card sticky"><h2>Get the current price</h2><p>Tell us the machine and the location you have in mind.</p>{wa_btn('WhatsApp us', topic='machine prices.')}{mail_btn()}</div></aside>
</div></section>'''


def about_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img('machines-duo', eager=True)}<figcaption>The AIVS range: Topi Express (5-minute helmet cleaning) and AI Printbox (3-minute phone case printing).</figcaption></figure>
<p>{LEGAL} (AIVS) is a Singapore company that sells self-service vending machines to owner-operators and places them in malls, the airport and motorcycle shops. It was incorporated on 27 September 2024 (UEN {UEN}) and is based at Carros Centre, 60 Jalan Lam Huat, Woodlands.</p>
<h2>What we do</h2>
<p>We refurbish and sell two machines, AI Printbox and Topi Express, and support the people who buy them: training, cost-price stock, maintenance plans, 24/7 technical help and a dashboard that shows sales and inventory. Owners pay no royalties. Today 19 AIVS machines run across Singapore.</p>
<h2>Mission</h2>
<p>In AIVS\'s own words: to bring smart and convenient shopping to everyone in Singapore with our vending machines. Our franchise partners own their machines with 0% royalties, giving them full control and higher profits. We focus on a fast return on investment and a profitable business model, making vending easier and more rewarding.</p>
<h2>Vision</h2>
<p>To become Singapore\'s leading automated vending machine network, offering cashless, hassle-free, 24/7 convenience across the island, and creating more business opportunities for partners who own their machines.</p>
<h2>Why "AI"?</h2>
<p>In our name, AI stands for Automated Intelligence: smart, automated vending that makes a business simple, efficient and easy to use. It does not refer to artificial intelligence.</p>
<h2>Company details</h2>
<p>{LEGAL}<br>UEN {UEN}, incorporated 27 September 2024<br>{'<br>'.join(ADDR)}<br>Machine purchase &amp; business collaboration: WhatsApp <a data-direct href="{E(wa_url())}" target="_blank" rel="noopener">+65 {WA_SHOW}</a><br>Technical support &amp; refunds: WhatsApp <a href="{E(sup_url())}" target="_blank" rel="noopener">+65 {SUP_SHOW}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>
<a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram @aivendingsolution</a> · <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok @aivendingsolution</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></p>
</article>
<aside class="side"><div class="card sticky"><h2>Visit or call</h2><p>{'<br>'.join(ADDR)}<br>By appointment.</p>{wa_btn('WhatsApp us', topic='visiting your office.')}<a class="btn btn-ghost" href="{MAP}" target="_blank" rel="noopener">{PIN_SVG}<span>Google Maps</span></a></div></aside>
</div></section>'''


def contact_body():
    topics = ['Owning an AI Printbox machine', 'Owning a Topi Express machine', 'Hosting a machine at my site', 'Prices and support plans', 'Custom branding', 'A machine location or customer question', 'Technical support or a refund', 'Something else']
    opts = ''.join('<option>%s</option>' % E(o) for o in topics)
    return f'''<section class="sec"><div class="wrap split">
<div class="prose">
<h2>WhatsApp</h2>
<p>Tap the button and choose what your message is about. It goes straight to the right AIVS team.</p>
<p>{wa_btn('WhatsApp AIVS')}</p>
<ul class="ticks"><li><b>Machine purchase and business collaboration:</b> buying a machine, hosting one at your site or partnering with AIVS (+65 {WA_SHOW}).</li><li><b>Technical support and refund enquiries:</b> a machine problem, a customer refund or help with a machine you own (+65 {SUP_SHOW}).</li></ul>
<form class="enquiry" id="enquiry" data-sup="{SUP_NUM}" action="https://wa.me/{WA_NUM}" method="get" target="_blank">
<h2>Enquire about a machine</h2>
<p class="small">Fill this in and tap the button. It opens WhatsApp with your message ready to send.</p>
<label>I am asking about<select name="o">{opts}</select></label>
<div class="row2"><label>Machine<select name="m"><option>AI Printbox</option><option>Topi Express</option><option>Not sure yet</option></select></label><label>Location in mind<input name="l" type="text" placeholder="e.g. a mall in Jurong, my workshop"></label></div>
<label>Your name<input name="n" type="text" autocomplete="name"></label>
<label>Anything else?<textarea name="x" rows="3"></textarea></label>
<input type="hidden" name="text" value="{E(WA_MSG + 'owning a machine.')}">
<button class="btn btn-wa" type="submit">{WA_SVG}<span>Send on WhatsApp</span></button>
</form>
<h2>Email</h2>
<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>Office</h2>
<p>{LEGAL}<br>{'<br>'.join(ADDR)}<br>Carros Centre is the automotive hub on Jalan Lam Huat in Woodlands/Kranji. Visits by appointment.</p>
<h2>Social</h2>
<p><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></p>
</div>
<div class="mapbox"><iframe title="Map to AI Vending Solution at Carros Centre, 60 Jalan Lam Huat" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''


def terms_body():
    return f'''<section class="sec"><div class="wrap prose">
<p>These are the customer terms AIVS publishes for its self-service machines. Full terms and conditions for machine purchases and support plans are provided by {LEGAL} before you buy.</p>
<h2>Using an AI Printbox machine</h2>
<ul>
<li>By using the machine you agree to these terms and take full responsibility for any content you print.</li>
<li>All purchases are non-refundable and non-exchangeable, because each case is printed to your order.</li>
<li>Uploaded images are automatically deleted from the system within 48 hours and are not stored, shared or used for any other purpose.</li>
<li>Supported phone models are shown on the machine interface at the time of your order.</li>
</ul>
<h2>Using a Topi Express machine</h2>
<ul>
<li>Follow the on-screen instructions and place only a helmet in the cleaning chamber.</li>
<li>Payment is by QR code at the price shown on the machine.</li>
</ul>
<h2>Intellectual property</h2>
<p>The artwork, branding and mascot designs on AIVS machines remain the intellectual property of {LEGAL}.</p>
<h2>Contact</h2>
<p>{LEGAL}, {', '.join(ADDR)}. <a href="mailto:{EMAIL}">{EMAIL}</a>. Technical support and refund enquiries: WhatsApp +65 {SUP_SHOW}. Machine purchase and business collaboration: WhatsApp +65 {WA_SHOW}.</p>
</section>'''


def privacy_body():
    return f'''<section class="sec"><div class="wrap prose">
<p>{LEGAL} ("AIVS", "we") respects your privacy and complies with Singapore's Personal Data Protection Act 2012 (PDPA).</p>
<h2>What we collect</h2>
<p>When you contact us by WhatsApp, email or the enquiry form on this site, we receive the details you send: your name, contact number, email address and your message. The enquiry form opens WhatsApp on your device; this website does not store the form contents.</p>
<p>At an AI Printbox machine, the image you upload is used only to print your case and is automatically deleted within 48 hours. It is not stored, shared or used for any other purpose. Payments at our machines are processed by the payment provider shown on screen; we do not receive your card details.</p>
<h2>How we use it</h2>
<p>To reply to your enquiry, to arrange a machine purchase, placement or support, and to keep records required by law. We do not sell personal data.</p>
<h2>Cookies and analytics</h2>
<p>This website uses no tracking cookies. If analytics are added, this page will say so.</p>
<h2>Your rights</h2>
<p>You may ask to see or correct the personal data we hold about you, or withdraw consent, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Contact</h2>
<p>Data Protection Officer, {LEGAL}, {', '.join(ADDR)}. <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</section>'''


def business_schema():
    return {'@type': ['Organization', 'LocalBusiness'], '@id': SITE + '#business', 'name': NAME, 'legalName': LEGAL, 'alternateName': [FULL, 'AI Vending Solutions'],
            'url': SITE, 'telephone': TEL, 'email': EMAIL, 'foundingDate': FOUNDED,
            'contactPoint': [{'@type': 'ContactPoint', 'telephone': TEL, 'contactType': 'sales', 'description': 'Machine purchase and business collaboration (WhatsApp)', 'areaServed': 'SG'},
                             {'@type': 'ContactPoint', 'telephone': SUP_TEL, 'contactType': 'customer support', 'description': 'Technical support and refund enquiries (WhatsApp)', 'areaServed': 'SG'}],
            'image': [(IMG_ABS or SITE + 'img/') + n + '.webp' for n in ('machines-duo', 'printbox-mall-dark', 'topi-shop')], 'logo': (IMG_ABS or SITE) + 'icon-512.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': '%s %s %s' % (STREET, UNIT, BUILDING), 'addressLocality': 'Singapore', 'postalCode': POSTAL, 'addressCountry': 'SG'},
            'hasMap': GBP, 'sameAs': [GBP, FB, IG, TIKTOK, YT], 'areaServed': 'Singapore',
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'UEN', 'value': UEN},
            'brand': [{'@type': 'Brand', 'name': 'AI Printbox'}, {'@type': 'Brand', 'name': 'Topi Express'}],
            'knowsAbout': ['vending machines', 'phone case printing vending machine', 'helmet cleaning vending machine', 'vending machine business Singapore'],
            'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@id': SITE + 'machines/ai-printbox/#product'}, 'price': PB_PRICE.replace(',', ''), 'priceCurrency': 'SGD', 'availability': 'https://schema.org/InStock'},
                           {'@type': 'Offer', 'itemOffered': {'@id': SITE + 'machines/topi-express/#product'}, 'price': TP_PRICE.replace(',', ''), 'priceCurrency': 'SGD', 'availability': 'https://schema.org/InStock'}]}


def product_schema(m):
    return {'@type': 'Product', '@id': SITE + 'machines/%s/#product' % m['slug'], 'name': '%s vending machine (refurbished)' % m['short'], 'description': m['desc'], 'brand': {'@type': 'Brand', 'name': m['short']},
            'image': (IMG_ABS or SITE + 'img/') + '%s.webp' % m['photo'], 'url': SITE + 'machines/%s/' % m['slug'],
            'offers': {'@type': 'Offer', 'price': m['price'].replace(',', ''), 'priceCurrency': 'SGD', 'availability': 'https://schema.org/InStock', 'seller': {'@id': SITE + '#business'},
                       'priceSpecification': {'@type': 'PriceSpecification', 'price': m['price'].replace(',', ''), 'priceCurrency': 'SGD', 'description': 'From price for a refurbished machine'}}}


# ----------------------------------------------------------------------------------------------
# Register pages
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# Keyword pages (client priority, 24 Oct 2026): AI / smart / buy vending machine Singapore.
# AIVS is becoming a contact point for buyers; partner suppliers handle installation and after-sales.
# ----------------------------------------------------------------------------------------------
PARTNER_NOTE = ('AIVS started with its own phone case printing and helmet cleaning machines and still sells its remaining refurbished units. '
                'For other machine types it is building a network of partner suppliers in Singapore, so one WhatsApp reaches the right machine for your site. '
                'Partner suppliers handle installation and after-sales support; AIVS helps you choose and makes the introduction.')
KEYWORD_PAGES = [
    dict(slug='ai-vending-machine-singapore', short='AI vending machines', photo='printbox-corridor', topic='an AI vending machine for my site.',
         title='AI Vending Machine Singapore: Buy or Place One | AIVS',
         desc='AI vending machines in Singapore: self-service kiosks that print, clean or sell without staff. AIVS sells machines and connects you with partner suppliers.',
         h1='AI vending machines in Singapore',
         lede='Self-service machines that do a job for the customer, take cashless payment and report every sale to your phone. AIVS helps you choose one and put it where it earns.',
         qa=[('What is an AI vending machine?',
              'An AI vending machine is a self-service kiosk that does more than drop a product: it senses, personalises or processes something for the customer and runs unattended.',
              'In Singapore the term covers machines like the AI Printbox, which prints a photo onto a phone case in about 3 minutes, helmet cleaning machines that sterilise with UVC, and smart retail kiosks with cameras and touchscreens. All take QR or card payment and send sales and stock data to a dashboard.',
              ['Does a task for the customer, not only vends a product', 'Cashless payment, no staff at the machine', 'Live sales and inventory on your phone']),
             ('Which AI vending machines can I get in Singapore through AIVS?',
              'Today AIVS sells its own refurbished AI Printbox (from S$%s) and Topi Express (from S$%s) machines, and is adding partner suppliers for other machine types.' % (PB_PRICE, TP_PRICE),
              'Tell AIVS what you want to sell and where you would place it. If one of its own machines fits, you get a price the same day. If you need another type, such as drinks, snacks, coffee or fresh food, AIVS introduces a partner supplier who installs and supports the machine.',
              ['AI Printbox: custom phone cases, 13 live mall and airport locations', 'Topi Express: 5-minute helmet cleaning, 6 live locations', 'Partner suppliers for other machine types, with installation and after-sales handled by the supplier']),
             ('How much does an AI vending machine cost in Singapore?',
              'AIVS machines are from S$%s (Topi Express) and S$%s (AI Printbox), refurbished, with a hardware warranty and 0%% royalties.' % (TP_PRICE, PB_PRICE),
              'Partner suppliers quote their own prices, which depend on the machine type, whether it is new or refurbished, and what the support plan includes. AIVS does not publish earnings figures; ask for real usage numbers from comparable sites before you buy.',
              [])],
         sections=[
             ('What to check before you buy', [
                 'Three things decide whether an AI vending machine earns: the footfall at the exact spot, the price per transaction, and the uptime. Ask for the payment options (QR, NETS, cards), the remote dashboard, who tops up stock, '
                 'who fixes the machine and how fast, and what the warranty covers. Visit a live machine first and watch how people use it.']),
             ('Where AI vending machines work in Singapore', [
                 'Mall entrances and linkways, Changi Airport halls, HDB town centres, petrol kiosks, workshops and office lobbies. AIVS has placed 19 machines in Singapore since 2024, so it can tell you which kind of site suits which machine.']),
         ],
         faqs=[('Does AIVS install the machine?', 'For its own machines, yes: AIVS delivers, sets up and trains you. For partner suppliers\' machines, the supplier installs and provides after-sales support.'),
               ('Can I host an AI vending machine at my shop or mall instead of buying one?', 'Yes. See the host-a-machine page: AIVS or an owner places the machine and you agree a rent or revenue share.'),
               ('Is "AI" artificial intelligence?', 'In the AIVS name, AI stands for Automated Intelligence: smart, automated vending. Some machines on the market do use image recognition or personalisation features.')]),
    dict(slug='smart-vending-machine-singapore', short='Smart vending machines', photo='dashboard', topic='a smart vending machine for my site.',
         title='Smart Vending Machine Singapore: Cashless, Remote | AIVS',
         desc='Smart vending machines in Singapore: cashless payment, a live sales and stock dashboard, remote alerts. What to look for and how AIVS helps you get one.',
         h1='Smart vending machines in Singapore',
         lede='A smart vending machine takes QR and card payment, tells you what it sold and what is running low, and flags a fault before customers do. Here is what to look for and how AIVS helps you get one.',
         qa=[('What makes a vending machine "smart"?',
              'A smart vending machine is connected: it takes cashless payment, reports every sale and stock level to a dashboard, and alerts you to faults remotely.',
              'That changes the business. You restock when the data says so rather than on a fixed round, you see which products and hours sell, and you know about a jam or a power cut without visiting. AIVS machines come with this dashboard on your phone.',
              ['QR, NETS or card payment, no cash handling', 'Live sales and inventory on your phone', 'Fault alerts and 24/7 technical support']),
             ('Which smart vending machine should I get for my location?',
              'Match the machine to the people who already pass the spot: shoppers and gift buyers suit a phone case printer, riders suit a helmet cleaner, offices and dorms suit drinks and snacks.',
              'AIVS sells its own AI Printbox and Topi Express machines and is building a network of partner suppliers for other types. Tell AIVS the location and the crowd, and it will say which machine fits and introduce the supplier if it is not one of its own.',
              []),
             ('How much does a smart vending machine cost in Singapore?',
              'AIVS machines start at S$%s (Topi Express) and S$%s (AI Printbox), refurbished, with a hardware warranty, 0%% royalties and an optional support plan from S$%s a month.' % (TP_PRICE, PB_PRICE, SUPPORT),
              'Drinks, snack and combo machines from partner suppliers are priced by the supplier and depend on size, cooling, payment hardware and whether the unit is new or refurbished.',
              [])],
         sections=[
             ('Smart features worth paying for', [
                 'Cashless payment with QR and cards, a remote dashboard with per-product sales, low-stock and fault alerts, remote price changes, and a touchscreen that can show promotions. Features that rarely pay back on a small fleet: facial recognition, dynamic pricing and custom app integrations.']),
             ('Running a smart machine day to day', [
                 'Check the dashboard in the morning, restock when the alert comes, and let the support plan handle repairs. AIVS owners see revenue, devices and inventory in one app, and AIVS provides 24/7 technical support under the monthly plan.']),
         ],
         faqs=[('Does a smart vending machine need Wi-Fi?', 'It needs a data connection for payments and the dashboard. Most machines use a built-in SIM, so a power socket is usually all the site has to provide.'),
               ('Can customers pay by PayNow or GrabPay?', 'AIVS machines take QR payment and cards can be arranged on request. Ask the supplier which wallets a partner machine supports.'),
               ('Can I move a smart machine to a better location later?', 'Yes. Let AIVS or the supplier know in advance so transport and reconnection are arranged.')]),
    dict(slug='buy-vending-machine-singapore', short='Buy a vending machine', photo='both-machines', topic='buying a vending machine.',
         title='Buy a Vending Machine in Singapore from S$%s | AIVS' % TP_PRICE,
         desc='Buy a vending machine in Singapore: AIVS refurbished machines from S$%s, 0%% royalties, plus partner suppliers for drinks and snack machines.' % TP_PRICE,
         h1='Buy a vending machine in Singapore',
         lede='One contact for the machine, the location advice and the support. AIVS sells its own refurbished units and introduces partner suppliers for everything else.',
         qa=[('Where can I buy a vending machine in Singapore?',
              'You can buy directly from AIVS, which sells refurbished AI Printbox and Topi Express machines from S$%s with a hardware warranty, or through AIVS\'s partner suppliers for other machine types.' % TP_PRICE,
              'WhatsApp AIVS with what you want to sell and where. For its own machines you get a price, delivery date and training. For drinks, snacks, coffee or other products, AIVS introduces a partner supplier who quotes, installs and supports the machine.',
              ['AIVS refurbished machines: from S$%s, hardware warranty, 0%% royalties' % TP_PRICE, 'Partner suppliers for other machine types, installation and after-sales by the supplier', 'Location advice from 19 live placements in Singapore']),
             ('How much does it cost to buy a vending machine in Singapore?',
              'AIVS prices: Topi Express helmet cleaning machine from S$%s, AI Printbox phone case machine from S$%s, both refurbished.' % (TP_PRICE, PB_PRICE),
              'Add the running costs: the location (rent or revenue share), stock (from AIVS at cost price for its machines) and an optional support plan from S$%s a month. There is no franchise fee and no royalty. Partner suppliers price their own machines.' % SUPPORT,
              []),
             ('Should I buy a new or a refurbished vending machine?',
              'A refurbished machine from a seller who services it is the lower-risk way to start, because the capital at stake is smaller and the warranty tells you the seller stands behind it.',
              'Check the warranty length, what it excludes, who repairs the machine and how fast, and whether the payment system and dashboard are current. AIVS refurbishes its own units and gives a 1-year warranty on AI Printbox and 6 months on Topi Express (terms apply).',
              [])],
         sections=[
             ('How to order from AIVS', [
                 'WhatsApp the machine and the location you have in mind. AIVS confirms the current price and what it includes, agrees a delivery date, delivers and sets up the machine, trains you and connects your dashboard. Stock comes from AIVS at cost price. AIVS still sells its remaining refurbished units, so ask about availability.']),
             ('Other machine types', [PARTNER_NOTE]),
             ('What to check before paying', [
                 'The exact price and what it includes (delivery, installation, GST), the warranty terms, the support plan, the payment options, who owns the branding on the machine, and whether you can move it later. Visit one of the 19 live AIVS machines and watch customers use it before you decide.']),
         ],
         faqs=[('Can I buy a vending machine in instalments?', 'Ask AIVS on WhatsApp %s; payment terms are discussed per order.' % WA_SHOW),
               ('Do I need a licence to run a vending machine in Singapore?', 'Food and drink machines need to meet SFA requirements; non-food machines such as phone case printers and helmet cleaners do not need a food licence. See the licence guide in the articles.'),
               ('Does AIVS buy back machines?', 'Ask AIVS; terms are discussed per order.')]),
]


def kw_body(k):
    qa = ''
    for q, lead, rest, bullets in k['qa']:
        qa += '<h2>%s</h2><p><strong>%s</strong> %s</p>' % (E(q), E(lead), E(rest))
        if bullets:
            qa += '<ul class="ticks">%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in bullets)
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % E(p) for p in ps)) for h, ps in k['sections'])
    rel = ''.join(tile('machines/%s/' % m['slug'], m['photo'], m['short'], m['gist'], 'From S$%s · More details →' % m['price']) for m in MACHINES)
    others = ''.join('<li><a href="%s/">%s</a></li>' % (o['slug'], E(o['short'])) for o in KEYWORD_PAGES if o['slug'] != k['slug'])
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(k['photo'], eager=True)}</figure>
{qa}
{secs}
<h2>AIVS machines available now</h2>
<div class="scards">{rel}</div>
<h2>Frequently asked questions</h2>
{faq_html(k['faqs'])}
<p class="byline">Facts on this page come from AIVS\'s published machine details and ownership terms. Last checked {UPDATED}.</p>
</article>
<aside class="side"><div class="card sticky"><h2>Tell AIVS what you need</h2><p>What do you want to sell, and where would the machine go? AIVS replies with a machine that fits, from its own units or a partner supplier.</p>{wa_btn('WhatsApp AIVS', topic=k['topic'])}{enquire_btn(cls='btn btn-ghost')}
<p class="small" style="margin-top:14px">Also read:</p><ul class="small" style="margin:0 0 0 18px">{others}<li><a href="prices/">Prices</a></li><li><a href="services/host-a-machine/">Host a machine at your site</a></li><li><a href="partner-with-aivs/">Partner with AIVS (suppliers)</a></li></ul></div></aside>
</div></section>'''


def kw_pairs(k):
    return [(q, '%s %s' % (lead, rest)) for q, lead, rest, _ in k['qa']]



# ---- Business Collaboration page (client copy via Edwin, 26 Oct 2026) ----
COLLAB_TECH = ['AI-powered recognition or automation', 'Smart inventory management', 'IoT connectivity and remote monitoring',
               'Intelligent or robotic dispensing systems', 'Automated retail with advanced smart features']
COLLAB_WHY = ['Showcase your machines on AIVS.sg', 'Increase online visibility', 'Reach potential buyers in Singapore',
              'Generate sales enquiries', 'Explore referral or reseller partnerships']
COLLAB_RULES = ['Singapore-based suppliers and distributors only.', 'Machines must have genuine AI or smart technology features.',
                'No conventional vending machines with only basic payment or dispensing functions.', 'All machine listings are subject to AIVS approval.']
COLLAB_FAQ = [
    ('Who can partner with AIVS?', 'Singapore-based suppliers and distributors of vending machines with genuine AI or smart technology features. Traditional vending machines without meaningful AI or smart capabilities are not eligible.'),
    ('What does AIVS do, and what does the partner do?', 'AIVS focuses on digital marketing and generating enquiries. Partners handle machine supply, installation, warranty and after-sales support.'),
    ('How do I apply?', 'Email info@aivs.sg or WhatsApp +65 %s with your company name, the machines you offer and their AI or smart features. All machine listings are subject to AIVS approval.' % WA_SHOW),
]


def collab_body():
    ticks = lambda items: '<ul class="ticks">%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in items)
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img('both-machines', eager=True)}</figure>
<h2>Do you have an AI or smart vending machine? Let's collaborate!</h2>
<p>Are you a Singapore-based supplier or distributor offering innovative vending machines powered by AI or smart technology?</p>
<p>AIVS.sg is looking for local partners who want to increase their online exposure and reach more potential buyers.</p>
<p>AIVS is expanding beyond its existing AI Printbox and helmet vending machines. Our new direction is to become a multi-brand AI and smart vending machine platform in Singapore, collaborating with local suppliers and distributors offering machines equipped with AI technology or genuine smart features.</p>
<h2>We welcome machines featuring technologies such as</h2>
{ticks(COLLAB_TECH)}
<p>Traditional vending machines without meaningful AI or smart capabilities are not eligible.</p>
<h2>Why partner with AIVS?</h2>
{ticks(COLLAB_WHY)}
<p>Interested? Contact <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp +65 {WA_SHOW}.</p>
<h2>Important</h2>
{ticks(COLLAB_RULES)}
<h2>Our goal</h2>
<p>Position AIVS.sg as Singapore's dedicated platform for discovering innovative AI and smart vending solutions.</p>
<p>AIVS will focus on digital marketing and generating enquiries, while our partners handle machine supply, installation, warranty and after-sales support.</p>
<h2>Frequently asked questions</h2>
{faq_html(COLLAB_FAQ)}
</article>
<aside class="side"><div class="card sticky"><h2>Partner with AIVS</h2><p>Tell us your company, the machines you offer and their AI or smart features. Singapore-based suppliers and distributors only.</p>{mail_btn('Email info@aivs.sg')}{wa_btn('WhatsApp AIVS', topic='a business collaboration.')}
<p class="small" style="margin-top:14px">Also read:</p><ul class="small" style="margin:0 0 0 18px"><li><a href="ai-vending-machine-singapore/">AI vending machines</a></li><li><a href="smart-vending-machine-singapore/">Smart vending machines</a></li><li><a href="about/">About AIVS</a></li></ul></div></aside>
</div></section>'''


page('partner-with-aivs/', 'Business Collaboration with AIVS | Smart Vending Singapore',
     'Partner with AIVS: Singapore suppliers and distributors of AI or smart vending machines can showcase machines on AIVS.sg. Contact info@aivs.sg.',
     "Partner With AIVS: Let's Grow the Future of Smart Vending", collab_body(), crumbs=[('partner-with-aivs/', 'Business collaboration')],
     lede='A multi-brand platform for AI and smart vending machines in Singapore. AIVS markets and generates enquiries; partners supply, install and support the machines.',
     photo='both-machines', cta=False, schema=[faq_schema(COLLAB_FAQ)])


page('', 'AIVS | AI & Smart Vending Machines Singapore',
     'AIVS (AI Vending Solution Pte. Ltd.) sells AI and smart vending machines in Singapore from S$%s with 0%% royalties, or finds you one from a partner supplier.' % TP_PRICE,
     FULL, home_body(), hero=False, schema=[faq_schema(FAQ_HOME)])
for k in KEYWORD_PAGES:
    path = k['slug'] + '/'
    page(path, k['title'], k['desc'], k['h1'], kw_body(k), crumbs=[(path, k['short'])], lede=k['lede'], photo=k['photo'],
         schema=[faq_schema(kw_pairs(k) + k['faqs'])])
page('machines/', 'Vending Machines for Sale in Singapore | AIVS',
     'Two machines you can own: AI Printbox prints phone cases in 3 minutes (from S$%s), Topi Express cleans helmets in 5 minutes (from S$%s). 0%% royalties.' % (PB_PRICE, TP_PRICE),
     'The machines', machines_index(), crumbs=[('machines/', 'Machines')],
     lede='Two proven machines, both sold refurbished with a hardware warranty, training and 0% royalties. Pick the one that matches the crowd at your location.')
for m in MACHINES:
    path = 'machines/%s/' % m['slug']
    page(path, m['title'], m['desc'], m['h1'], machine_body(m), crumbs=[('machines/', 'Machines'), (path, m['short'])], lede=m['lede'], photo=m['hero_photo'], theme=m['theme'],
         schema=[product_schema(m), faq_schema(qa_pairs(m['slug']) + m['faqs'] + m['cust_faqs'])])
page('services/', 'Own a Machine: Ownership, Support, Hosting | AIVS',
     'Buy a refurbished machine, pay 0%% royalties, get stock at cost price, training and a support plan from S$%s/month. Or host a machine at your site.' % SUPPORT,
     'Own a machine', services_index(), crumbs=[('services/', 'Own a machine')],
     lede='You buy the machine and keep the sales. AIVS supplies the stock, the training, the maintenance and the know-how from 19 live placements.')
for s in SERVICES:
    path = 'services/%s/' % s['slug']
    page(path, s['title'], s['desc'], s['h1'], service_body(s), crumbs=[('services/', 'Own a machine'), (path, s['short'])], lede=s['lede'], photo=s['photo'],
         schema=[{'@type': 'Service', 'name': s['h1'], 'serviceType': s['short'], 'description': s['desc'], 'url': SITE + path, 'provider': {'@id': SITE + '#business'}, 'areaServed': 'Singapore'}, faq_schema(qa_pairs(s['slug']) + s['faqs'])])
page('locations/', 'AIVS Machine Locations in Singapore',
     'Find an AI Printbox machine (13 malls and Changi Airport T3) or a Topi Express helmet cleaner (6 motorcycle shops) in Singapore. Addresses and unit numbers.',
     'Where to find our machines', locations_index(), crumbs=[('locations/', 'Locations')],
     lede='19 machines across Singapore, with addresses and unit numbers so you can walk straight to them.')
page('locations/ai-printbox/', 'AI Printbox Locations: 13 Machines in Singapore',
     'All 13 AI Printbox locations with unit numbers: AMK Hub, Bukit Panjang Plaza, Changi Airport T3, Hillion, Hougang Mall, Parkway Parade, Tampines 1 and more.',
     'AI Printbox locations', locations_machine(MCH['ai-printbox'], PB_LOCS, 'Print a custom phone case in about 3 minutes for S$%s at any of these 13 machines. Most sit at a mall entrance, in an atrium or at an MRT linkway; two are at Changi Airport Terminal 3.' % CASE_PRICE),
     crumbs=[('locations/', 'Locations'), ('locations/ai-printbox/', 'AI Printbox')], theme='pb', photo='printbox-mall-dark',
     lede='13 machines in malls across Singapore and at Changi Airport Terminal 3.',
     schema=[{'@type': 'ItemList', 'name': 'AI Printbox locations', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': {'@type': 'Place', 'name': 'AI Printbox @ ' + n, 'address': a}} for i, (n, a, _) in enumerate(PB_LOCS)]}])
page('locations/topi-express/', 'Topi Express Locations: 6 Machines in Singapore',
     'All 6 Topi Express locations: Wheels & Cycles (Woodlands), 345 Wash (Telok Blangah), Candy Motor, Gusto Broz and Hodaka Motoworld (Kaki Bukit), BW Motorsports.',
     'Topi Express locations', locations_machine(MCH['topi-express'], TP_LOCS, 'Clean and disinfect your helmet in about 5 minutes for S$%s at these six machines. The Hodaka Motoworld machine runs 24 hours a day.' % WASH_PRICE),
     crumbs=[('locations/', 'Locations'), ('locations/topi-express/', 'Topi Express')], theme='tp', photo='topi-shop',
     lede='Six machines at motorcycle shops, workshops and a laundromat.',
     schema=[{'@type': 'ItemList', 'name': 'Topi Express locations', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': {'@type': 'Place', 'name': 'Topi Express @ ' + n, 'address': a}} for i, (n, a, _) in enumerate(TP_LOCS)]}])
page('prices/', 'Vending Machine Prices from S$%s | AIVS' % TP_PRICE,
     'AIVS prices: AI Printbox from S$%s, Topi Express from S$%s (refurbished), support from S$%s/month, 0%% royalties. Cases S$%s, helmet clean S$%s.' % (PB_PRICE, TP_PRICE, SUPPORT, CASE_PRICE, WASH_PRICE),
     'Prices', prices_body(), crumbs=[('prices/', 'Prices')],
     lede='Published "from" prices for the machines, the support plan and what customers pay. The final quote follows your order.',
     schema=[faq_schema([('Is GST included in the machine price?', 'Ask AIVS on WhatsApp %s. The published figures are "from" prices for refurbished machines.' % WA_SHOW), ('Is there a franchise fee?', 'No. AIVS charges no franchise fee and 0% royalties.'), ('What does the S$%s support plan cover?' % SUPPORT, 'Maintenance and repairs, system support and 24/7 technical help. For Topi Express it also covers disinfectant top-ups.')])])
page('articles/', 'Vending Machine Business Guides | AIVS',
     'Guides on vending machines in Singapore: costs, how to start, best locations, franchise vs ownership, where to print a phone case or clean a helmet.',
     'Articles and guides', '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(article_card(a) for a in ARTICLES),
     crumbs=[('articles/', 'Articles')], lede='Plain answers for future owners, hosts and customers.')
# ---- 2 Nov 2026 SEO pass: hub intros + FAQs (facts from this site only) ----
SERVICES_FAQ = [
    ('What does AIVS offer owners of a vending machine?', 'AIVS sells refurbished AI Printbox and Topi Express machines with 0%% royalties, supplies stock at cost price, trains you, and offers a support plan from S$%s a month with a dashboard that shows sales and inventory.' % SUPPORT),
    ('Can my shop or mall host a machine?', 'Yes. Malls, shops, petrol kiosks and workshops can host an AI Printbox or Topi Express at their site. Talk to AIVS about placement on WhatsApp %s.' % WA_SHOW),
    ('Can I put my own branding on the machine?', 'Yes. A machine can run under the AI Printbox or Topi Express brand, or be re-wrapped with your own name, colours and mascot.'),
]
ARTICLES_FAQ = [
    ('What do the AIVS guides cover?', 'Plain answers for future owners, hosts and customers: what a vending machine costs, how to start the business, good locations, licensing, franchise versus owning your own machine, and how the AI Printbox and Topi Express machines work.'),
    ('Are the figures in the guides AIVS prices?', 'Machine and support prices quoted for AIVS are the published "from" prices on the prices page. The final quote follows your order, so confirm on WhatsApp %s.' % WA_SHOW),
    ('Who can I ask about buying or hosting a machine?', 'WhatsApp the AIVS sales line on %s. For support or refunds on a machine you used, use the support line shown on the contact page.' % WA_SHOW),
]
SERVICES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Owning, supporting and hosting a machine</h2>'
    '<p>AI Vending Solution Pte. Ltd. (AIVS) sells refurbished self-service machines to owner-operators. You buy the machine and keep the sales: there is no franchise fee, AIVS takes 0%% royalties, and stock is supplied at cost price. Machines start from S$%s for Topi Express and S$%s for AI Printbox.</p>'
    '<p>Training is included, and an optional support plan from S$%s a month covers maintenance and system support, with a dashboard that shows sales and inventory on your phone. If you have a site rather than a budget, you can host a machine instead, and a machine can be re-wrapped with your own branding.</p>'
    '<p>Choose a service below, or WhatsApp AIVS on %s.</p></div></section>') % (TP_PRICE, PB_PRICE, SUPPORT, WA_SHOW)
ARTICLES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Vending machine guides for Singapore</h2>'
    '<p>These guides answer the questions we hear from people who want to own, host or use a self-service machine in Singapore. They cover what a machine costs, how to start a vending machine business, which locations work, whether you need a licence, how a franchise compares with owning your own machine, and what to check when buying refurbished.</p>'
    '<p>Other guides explain how the AI Printbox prints a phone case in about 3 minutes and how the Topi Express cleans a helmet in about 5 minutes. Each guide ends with questions and answers. For anything not covered, WhatsApp AIVS on %s.</p></div></section>') % WA_SHOW
def _hub(path, intro, faqs, h2):
    p = PAGES[path]
    p['body'] = intro + p['body'] + '<section class="sec"><div class="wrap narrow"><div class="sec-head"><h2>%s</h2></div>%s</div></section>' % (h2, faq_html(faqs))
    p['schema'] = list(p['schema']) + [faq_schema(faqs)]
_hub('services/', SERVICES_INTRO, SERVICES_FAQ, 'Questions about owning a machine')
_hub('articles/', ARTICLES_INTRO, ARTICLES_FAQ, 'Questions about our guides')

for a in ARTICLES:
    path = 'articles/%s/' % a['slug']
    page(path, a['title'], a['desc'], a['h1'], article_body(a), crumbs=[('articles/', 'Articles'), (path, a['h1'])], photo=a['photo'],
         schema=[article_schema(a, path), faq_schema(a['faqs'])])
page('about/', 'About AIVS | AI Vending Solution Pte. Ltd.',
     'AI Vending Solution Pte. Ltd. (AIVS) sells and places AI Printbox and Topi Express vending machines in Singapore. Incorporated 2024. 19 machines live.',
     'About AIVS', about_body(), crumbs=[('about/', 'About')],
     lede='A Singapore company that sells self-service machines to owner-operators and stands behind them.')
page('contact/', 'Contact AIVS | WhatsApp, Email and Office',
     'WhatsApp AIVS sales +65 %s or support +65 %s, or email %s. 60 Jalan Lam Huat #05-54 Carros Centre, Singapore 737869.' % (WA_SHOW, SUP_SHOW, EMAIL),
     'Contact AIVS', contact_body(), crumbs=[('contact/', 'Contact')], cta=False,
     lede='WhatsApp AIVS, email %s, or visit Carros Centre by appointment.' % EMAIL)
page('terms/', 'Terms & Conditions | AIVS', 'Customer terms for AI Printbox and Topi Express machines: non-refundable orders, images deleted within 48 hours, content responsibility.',
     'Terms and conditions', terms_body(), crumbs=[('terms/', 'Terms')], cta=False, lede='')
page('privacy/', 'Privacy Policy | AIVS', 'How AI Vending Solution Pte. Ltd. handles personal data under Singapore\'s PDPA, including images uploaded at AI Printbox machines.',
     'Privacy policy', privacy_body(), crumbs=[('privacy/', 'Privacy')], cta=False, lede='')


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------
def render(path, p):
    pre = '../' * path.count('/')
    url = SITE + path
    share = (IMG_ABS or SITE + 'img/') + 'share/home.jpg'

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t,
                  '<small class="nav-sub">%s</small>' % E(NAV_SUB[h]) if h in NAV_SUB else '') for h, t in NAV)
    src = 'aivs.sg/' + path if path != '404.html' else 'aivs.sg page-not-found'
    dock_sup = 'https://wa.me/%s?text=%s' % (SUP_NUM, quote(DOCK_SUP_MSG + ' [Source: %s, Support button]' % src))
    dock_biz = 'https://wa.me/%s?text=%s' % (WA_NUM, quote(DOCK_BIZ_MSG + ' [Source: %s, Business button]' % src))
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                                 'inLanguage': 'en-SG', 'dateModified': LASTMOD.get(path, UPDATED), 'about': {'@id': SITE + '#business'},
                                 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': FULL}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = '<section class="phero %s"><div class="wrap">%s<h1>%s</h1>%s</div></section>' % (
            p['theme'], crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = ('<section class="sec"><div class="wrap"><div class="band"><div><h2>Ready to own a machine?</h2>'
                '<p>WhatsApp the machine you want and the location you have in mind. From S$%s, 0%% royalties, training included.</p></div><div class="cta-row">%s%s</div></div></div></section>') % (
            TP_PRICE, wa_btn('WhatsApp us'), enquire_btn(cls='btn btn-gold'))
        band = fix(band)
    robots = 'noindex,nofollow' if NOINDEX else 'index,follow,max-image-preview:large'
    title = E(p['title'])
    lcp = p['photo'] or ('printbox-mall-dark' if path == '' else None)
    preload = '<link rel="preload" as="image" href="%s%s%s.webp" fetchpriority="high">' % ('' if IMG.startswith('http') else pre, IMG, lcp) if lcp else ''
    body = fix(p['body'])
    brand = brand_html(pre)
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="{robots}">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#111318">
<link rel="canonical" href="{url}">
{preload}
<meta property="og:type" content="{'article' if path.startswith('articles/') and path != 'articles/' else 'website'}">
<meta property="og:site_name" content="{FULL}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{IMG_ABS or pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="stylesheet" href="{pre}aivs.css?v=6">
<script src="{pre}aivs.js?v=4" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>{LEGAL} · {', '.join(ADDR)}</span><span class="strip-r"><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp AIVS</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span></div></div>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('WhatsApp', cls='btn btn-wa hdr-call')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<main id="main">
{head_hero}
{body}
{band}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}
<p>Self-service vending machines you can own: AI Printbox phone case printing and Topi Express helmet cleaning. Singapore, since 2024.</p></div>
<div><h3>Machines</h3><ul>{''.join('<li><a href="%smachines/%s/">%s</a></li>' % (pre, m['slug'], E(m['short'])) for m in MACHINES)}<li><a href="{pre}locations/">Locations</a></li><li><a href="{pre}prices/">Prices</a></li>{''.join('<li><a href="%s%s/">%s</a></li>' % (pre, k['slug'], E(k['short'])) for k in KEYWORD_PAGES)}</ul></div>
<div><h3>Own a machine</h3><ul>{''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, s['slug'], E(s['short'])) for s in SERVICES)}<li><a href="{pre}partner-with-aivs/">Partner with AIVS</a></li><li><a href="{pre}articles/">Articles</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp AIVS</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="{GBP}" target="_blank" rel="noopener">Read our Google reviews</a></li>
<li>{'<br>'.join(ADDR)}</li>
<li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a> · <a href="{YT}" target="_blank" rel="noopener">YouTube</a></li>
<li><a href="{pre}about/">About</a> · <a href="{pre}contact/">Contact</a> · <a href="{pre}terms/">Terms</a> · <a href="{pre}privacy/">Privacy</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{LEGAL} · UEN {UEN}</span><span>© 2026 {LEGAL} · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock" aria-label="WhatsApp AIVS"><a class="dock-sup" data-direct href="{E(dock_sup)}" target="_blank" rel="noopener" aria-label="WhatsApp technical support or refunds, +65 {SUP_SHOW}">{WA_SVG}<span>Support / Refunds</span></a><a class="dock-biz" data-direct href="{E(dock_biz)}" target="_blank" rel="noopener" aria-label="WhatsApp business enquiries, +65 {WA_SHOW}">{WA_SVG}<span>Business Enquiries</span></a></div>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', t) for h, t in [('', 'Home')] + NAV)
    p = dict(title='Page not found | AIVS', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, photo=None, theme='')
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, m.group(2) if m.group(2) != './' else ''), out)


# Old aivs.sg URLs -> new pages (for the go-live .htaccess)
REDIRECTS = [
    ('/ai-printbox/', '/machines/ai-printbox/'), ('/topi-express/', '/machines/topi-express/'),
    ('/blog/', '/articles/'), ('/terms-conditions/', '/terms/'),
    ('/ai-vending-solution/', '/articles/ai-printbox-now-at-14-locations-across-singapore/'),
    ('/ai-printbox-bringing-convenient-affordable-and-customised-phone-cases-to-you/', '/articles/print-a-custom-phone-case-in-3-minutes/'),
    ('/topi-express-vending-machine-now-at-hodaka-motoworld-singapore/', '/articles/topi-express-helmet-cleaning-at-hodaka-motoworld/'),
    ('/category/uncategorized/', '/articles/'), ('/author/admin/', '/about/'), ('/author/aivsbackend/', '/about/'),
]

HTACCESS = """# AI Vending Solution ({DOMAIN}). Document root for {DOMAIN}; also served as
# pageonesingapore.com/preview/aivs/ before go-live. Overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^{DQ}$ [NC]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
# Old WordPress URLs
{REDIRECTS}
RedirectMatch 301 ^/wp-sitemap.*\\.xml$ /sitemap.xml
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600, public"
</FilesMatch>
<FilesMatch "\\.(webp|png|jpg|ico|css|js)$">
Header set Cache-Control "max-age=2592000, public"
</FilesMatch>
</IfModule>
"""

BOTS = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot',
        'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']


def main():
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
        f.write('# AIVS (AI Vending Solution Pte. Ltd.), vending machines you can own, Singapore\n\n'
                '> %s (AIVS, UEN %s, incorporated 27 September 2024) sells refurbished self-service vending machines to owner-operators in Singapore '
                'and places them in malls, Changi Airport and motorcycle shops. Two machines: AI Printbox, which prints a custom phone case in about 3 minutes '
                '(customers pay S$%s; machine from S$%s with a 1-year hardware warranty), and Topi Express, which disinfects, deodorises and sterilises a motorcycle helmet in about 5 minutes '
                '(customers pay S$%s; machine from S$%s with a 6-month hardware warranty). Owners pay 0%% royalties, buy stock at cost price, get free training, 24/7 technical support, '
                'an optional support plan from S$%s a month and a live sales dashboard. 19 machines are live: 13 AI Printbox (AMK Hub, Bukit Panjang Plaza, Changi Airport T3 Arrival Hall and B2, '
                'Changi City Point, City Square Mall, Eastpoint Mall, Hillion Mall, Hougang Mall, Parkway Parade, Sembawang Shopping Centre, Tampines 1, The Centrepoint) and '
                '6 Topi Express (Wheels & Cycles Woodlands, 345 Wash Telok Blangah, Candy Motor, Gusto Broz Workshop and Hodaka Motoworld in Kaki Bukit, BW Motorsports Old Toh Tuck Road). '
                'Office: %s, Singapore %s. WhatsApp +65 %s (machine purchase and business collaboration), +65 %s (technical support and refunds), %s. "AI" in the name stands for Automated Intelligence, not artificial intelligence.\n\n## Pages\n'
                % (LEGAL, UEN, CASE_PRICE, PB_PRICE, WASH_PRICE, TP_PRICE, SUPPORT, ', '.join(ADDR[:1] + [BUILDING]), POSTAL, WA_SHOW, SUP_SHOW, EMAIL))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': LEGAL, 'short_name': NAME, 'icons': [{'src': (IMG_ABS or '') + 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': (IMG_ABS or '') + 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
                   'theme_color': '#111318', 'background_color': '#fbfaf7', 'display': 'browser'}, f)
    with open(os.path.join(OUT, 'htaccess.txt'), 'w') as f:
        dq = DOMAIN.replace('.', r'\.')
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN).replace('{DQ}', dq).replace('{REDIRECTS}', '\n'.join('Redirect 301 %s %s' % (a, b) for a, b in REDIRECTS)))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()

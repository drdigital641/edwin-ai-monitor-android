"""Star Performance Motor Pte. Ltd.: builds every page into site/ (python3 build.py).

Facts used (17 Oct 2026), and where they came from:
- ACRA via recordowl.com / opengovsg.com: STAR PERFORMANCE MOTOR PTE. LTD., UEN 202223232K, incorporated 9 Nov 2022, live,
  exempt private company. Registered address (recordowl, latest) 9 Yishun Industrial Street 1 #01-82 North Spring Bizhub
  Singapore 768163 (opengovsg still shows an older Serangoon North address). SSIC 47311 retail sale of motor vehicles.
- Facebook page facebook.com/Starperformancemotor (read 17 Oct 2026): "Sincere. Passionate. Mindful. Your trusted car dealer.
  Buy/Sell/Consign/Export and import", category Car dealership, same Yishun address, phone +65 9742 7491, sgcarmart
  dealer price list dl=3954, 5.7K followers, "100% recommend (391 reviews)". Review texts quoted verbatim (short excerpts,
  first name + initial). Four handover posts (12-15 Aug 2026): BMW 520i M Sport, VW Passat, Toyota Vellfire, VW Tiguan R-Line.
- Instagram @starperformancemotor: bio "Buy/Sell/Consign", "360+ positive reviews on Facebook"; six SOLD posts from
  March 2022 (posted as Star Performance Auto) with viewings and handover days, contacts Zach 8111 6736, Celsius, Colin.
- Their own photos from those Facebook and Instagram posts (they belong to the client).
- sgcarmart dealer page (dl=3954) blocks automated reading, so live stock is linked, not copied.
Not claimed anywhere: "price higher than trade-in guaranteed" (old IG captions), "highest trade-in value", any price,
  warranty, loan rate, opening hours, Google rating. Things to confirm are in CONFIRM and README.md.
"""
import html
import json
import os
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

SLUG = 'star-performance'
DOMAIN = 'starperformancemotor.com'
LIVE = True  # go-live approved by Edwin 17 Oct 2026 (decision card)
NOINDEX = False  # hidden-from-Google is an X-Robots-Tag header in .htaccess for the preview host, never a meta tag (Edwin, 17 Oct 2026)
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
# Photos are served from jsDelivr (repo site-assets branch, commit 1bbc69e): the bridge cannot take binaries reliably.
# At go-live copy them to the client host and set SP_IMG=img/ .
IMG = os.environ.get('SP_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@1bbc69e/site-assets/star-performance/')
IMG_ABS = IMG if IMG.startswith('http') else None
UPDATED = '2026-10-17'

NAME = 'Star Performance Motor'
LEGAL = 'Star Performance Motor Pte. Ltd.'
UEN = '202223232K'
FOUNDED = '2022-11-09'
WA_NUM, WA_SHOW = '6597427491', '9742 7491'     # CONFIRM: Facebook business line; Zach's own mobile is 8111 6736
TEL = '+6597427491'
WA_MSG = 'Hi Star Performance Motor, I found your website. I would like to ask about '
STREET, UNIT, BUILDING, POSTAL = '9 Yishun Industrial Street 1', '#01-82', 'North Spring Bizhub', '768163'
ADDR = ['9 Yishun Industrial Street 1, #01-82', 'North Spring Bizhub, Singapore 768163']
MAPQ = quote('Star Performance Motor, 9 Yishun Industrial Street 1 #01-82 North Spring Bizhub Singapore 768163')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
FB = 'https://www.facebook.com/Starperformancemotor/'
FB_REVIEWS = 'https://www.facebook.com/Starperformancemotor/reviews'
IG = 'https://www.instagram.com/starperformancemotor/'
SGCM = 'https://www.sgcarmart.com/used-cars/listing?dl=3954'
GBP = 'https://share.google/12eV3JltMSy4kgilx'  # Google Business Profile, from Edwin 19 Oct 2026
SGCM_PRICES = 'https://www.sgcarmart.com/used-cars/dealer-pricelist?dl=3954'
REC, REC_N, REC_DATE = '100%', '391', '17 October 2026'

CONFIRM = [
    'WhatsApp number for the website: the Facebook business line 9742 7491 (used now) or Zach\'s mobile 8111 6736',
    'Consignment terms: fee or commission, how long, who handles viewings, test drives and paperwork',
    'Export and import: which countries, whether you handle the LTA deregistration, and whether you import cars yourselves',
    'Car loans and insurance: do you arrange them through partners (names) or not at all',
    'Any warranty offered on cars you sell, and the after-sale help you give as standard',
    'The six SOLD cars from March 2022 were posted as "Star Performance Auto": same team? OK to show them?',
    'Current stock: send sgcarmart links or photos, or let us set up a way to keep the "Cars for sale" list in sync',
    'Team names and roles to show on the About page (reviews mention Zach, Celsius and Wei Kiat)',
]

HOURS = '10am to 8pm, every day'  # Google Business Profile as seen by Edwin 17 Oct 2026
GOOGLE_RATING = '5.0 from 110 Google reviews'  # Google Business Profile, 17 Oct 2026

NAV = [('cars-for-sale/', 'Cars for sale'), ('services/', 'Services'), ('sold-cars/', 'Sold cars'), ('reviews/', 'Reviews'),
       ('articles/', 'Guides'), ('about/', 'About'), ('contact/', 'Contact')]
E = html.escape

PHOTOS = {  # name: (width, height, alt)
    'showroom': (960, 865, 'Star Performance Motor showroom at North Spring Bizhub, Yishun, with the gold logo on the wall and cars on display'),
    'handover-bmw-520i': (526, 489, 'Customer collecting his BMW 520i M Sport from Star Performance Motor'),
    'handover-vw-passat': (526, 393, 'Volkswagen Passat handover in front of the Star Performance Motor sign'),
    'handover-toyota-vellfire': (526, 394, 'Toyota Vellfire handover to a family at Star Performance Motor'),
    'handover-vw-tiguan': (526, 687, 'Volkswagen Tiguan 2.0 R-Line handed over to a customer by Star Performance Motor'),
    'sold-mercedes-glb200': (600, 600, 'Sold: Mercedes-Benz GLB200 AMG Line Premium (2020)'),
    'sold-audi-a4-2014': (600, 600, 'Sold: Audi A4 1.8 TFSI (2014)'),
    'sold-audi-a4-2017': (600, 600, 'Sold: Audi A4 1.8 TFSI (2017)'),
    'sold-subaru-wrx': (600, 600, 'Sold: Subaru Impreza WRX 2.5M (2007)'),
    'sold-mitsubishi-lancer': (600, 600, 'Sold: Mitsubishi Lancer GLX 1.6A (2007)'),
    'sold-kia-koup': (600, 600, 'Sold: Kia Koup 1.6A (2010)'),
}


def img(name, cls='', eager=False):
    w, h, alt = PHOTOS[name]
    return '<img src="%s%s.webp" alt="%s" width="%d" height="%d"%s%s>' % (
        IMG, name, E(alt), w, h, ' loading="lazy" decoding="async"' if not eager else ' fetchpriority="high"', ' class="%s"' % cls if cls else '')


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')


def wa_url(topic='a car.'):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp us', topic='a car.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic)), WA_SVG, E(label))


def sgcm_btn(label='See our cars on sgcarmart', cls='btn btn-gold'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s</a>' % (cls, SGCM, E(label))


MARK = '<img class="brand-mark" src="%slogo-200.webp" alt="" width="42" height="42" style="border-radius:8px">'


def brand_html(pre):
    return ('<a class="brand" href="%s" aria-label="%s, home page">%s<span><span class="brand-name">STAR PERFORMANCE</span>'
            '<span class="brand-sub">Motor · Yishun, Singapore</span></span></a>') % (pre or './', NAME, (MARK % IMG) if IMG_ABS else (MARK % (pre + IMG)))


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, photo=None):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [], hero=hero, cta=cta, photo=photo)


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def tile(href, photo, title, gist, more='More details →'):
    return '<a class="scard" href="%s">%s<span class="scard-t"><b>%s</b><span>%s</span><em>%s</em></span></a>' % (href, img(photo), E(title), E(gist), E(more))


def ticks(items):
    return '<ul class="ticks">%s</ul>' % ''.join('<li><b>%s</b> %s</li>' % (E(a), E(b)) for a, b in items)


def steps(items):
    return '<ol class="numbered">%s</ol>' % ''.join('<li><b>%s.</b> %s</li>' % (E(a), E(b)) for a, b in items)


# ----------------------------------------------------------------------------------------------
# Proof: reviews (Facebook, verbatim excerpts), handover stories (Facebook, Aug 2026), sold cars (Instagram, Mar 2022)
# ----------------------------------------------------------------------------------------------
REVIEWS = [
    ('Alvin O.', 'Zach', 'September 2026', 'I highly recommend buying a car from Zach. He is sincere, transparent, and got me the best trade-in rate. When I found a minor issue two days after pickup, he immediately had his garage repair it completely free of charge.'),
    ('Samuel G.', 'Zach', 'September 2026', 'Good experience with Zach. Chill and easy to work with. No fuss, no hidden fees, and upfront with communication.'),
    ('Jaylene K.', 'Wei Kiat', 'June 2026', 'The transaction was hassle-free and the car was delivered in the exact condition promised, which gave me confidence throughout. He also went down with us for the PPI and ensured everything was clearly explained and understood.'),
    ('Toh K. H.', 'Celsius', 'September 2026', 'Thank you my bro Celsius Toh for guiding me through this journey as a first time car owner. Initially, I was really worried and had so many questions to ask, but he patiently answer all my queries and gave me very detailed explanation and guiding me step by step in making the final decision.'),
    ('Pearly T.', 'Zach', 'May 2026', 'There is definitely a reason why there are hundreds of 100% recommends. I\'m a returning customer and always pleasant to deal with Zach!'),
    ('Kelvin L.', 'Celsius', 'April 2026', 'Celsius really went the extra mile, searching high and low to find a unit that matched both my budget and what I was looking for, while still ensuring it was a good, solid car.'),
    ('Nicolas T.', 'Wei Kiat', 'June 2026', 'Dealt with Wei Kiat for the purchase of my vehicle and the entire process was seamless from start to finish. He was highly professional, efficient, and made sure everything went smoothly without any hassle.'),
    ('Tony L.', 'Celsius', 'July 2026', 'Celsius went above and beyond to assist me with my car purchase within an exceptionally short timeframe. From the outset, he was responsive, patient, and consistently professional, which made the entire process smooth and stress-free.'),
    ('Celeste N.', 'Celsius', 'April 2026', 'It was my first time buying a second-hand car, and Celcius provided top-notch service in helping me find the perfect one. He recommended several models suited to my needs, and I eventually found a car I was really happy with.'),
    ('Jobs J.', 'Zach', 'September 2026', 'Buying a used car can be stressful, especially in an industry where some dealers may not honour their promises or stop responding after collecting the vehicle. Zach is different. From the beginning, he made sure the vehicle he was selling was in tip-top condition and was transparent throughout the process.'),
    ('Yap H. H.', 'Zach', 'September 2026', 'Nice bro to deal with. Helpful throughout the purchase process. Thank you.'),
]


def rev_html(r):
    who, staff, when, text = r
    return '<figure class="rev"><blockquote>%s</blockquote><figcaption><b>%s</b> · dealt with %s · Facebook, %s</figcaption></figure>' % (E(text), E(who), E(staff), E(when))


def revs_carousel(n=8):
    return '<div class="revs" aria-label="Customer reviews from Facebook">%s</div>' % ''.join(rev_html(r) for r in REVIEWS[:n])


PROOF_LINE = '%s recommend on Facebook from %s reviews (checked %s)' % (REC, REC_N, REC_DATE)

STORIES = [
    dict(slug='bmw-520i-m-sport', photo='handover-bmw-520i', date='12 August 2026', car='BMW 520i M Sport', tag='Trade-in, then a test drive',
         gist='He came only to sell his car. While handing it over he spotted a modified BMW 520i M Sport in the showroom, test drove it and placed a deposit the same day.',
         more='The next day we drove the BMW to his preferred workshop for a full inspection: mechanically sound and in excellent condition. He collected the keys three days later.',
         services=['sell-your-car', 'buy-a-used-car']),
    dict(slug='volkswagen-passat', photo='handover-vw-passat', date='13 August 2026', car='Volkswagen Passat', tag='Buying',
         gist='He had already viewed three other Passats before ours. Asked why he chose us, he said: "I just feel you guys are easier to talk to, and we really clique."',
         more='Sincere, Passionate, Mindful: the three values on our wall are the reason we started Star Performance Motor.',
         services=['buy-a-used-car']),
    dict(slug='toyota-vellfire', photo='handover-toyota-vellfire', date='14 August 2026', car='Toyota Vellfire', tag='Export, then an upgrade',
         gist='His old car was near the end of its COE, so we found him an export offer for it. He then bought a well-priced Toyota Vellfire from us.',
         more='His pre-purchase inspection happened at the very workshop that had serviced this Vellfire for years, and it passed. We polished and detailed it before handover; his wife said it looked brand new.',
         services=['car-export', 'buy-a-used-car']),
    dict(slug='volkswagen-tiguan-r-line', photo='handover-vw-tiguan', date='15 August 2026', car='Volkswagen Tiguan 2.0 R-Line', tag='Sell, then source',
         gist='We first sold his Kia Stinger after a single viewing. Then he asked for a Tiguan 2.0 R-Line, and we searched our network for a well-maintained unit at an attractive price.',
         more='It began as a chat in a WhatsApp group and became a friendship.',
         services=['sell-your-car', 'car-sourcing']),
]

SOLD = [  # Instagram, March 2022 (posted as Star Performance Auto)
    ('sold-mercedes-glb200', 'Mercedes-Benz GLB200 AMG Line Premium (2020)', 'Sold in one viewing, handover in 8 days'),
    ('sold-audi-a4-2017', 'Audi A4 1.8 TFSI (2017)', 'Sold in two viewings, handover in 3 days'),
    ('sold-audi-a4-2014', 'Audi A4 1.8 TFSI (2014)', 'Sold in one viewing, handover in 4 days'),
    ('sold-subaru-wrx', 'Subaru Impreza WRX 2.5M (2007)', 'Sold in three viewings, handover in 6 days'),
    ('sold-mitsubishi-lancer', 'Mitsubishi Lancer GLX 1.6A (2007)', 'Sold in two viewings, handover in 5 days'),
    ('sold-kia-koup', 'Kia Koup 1.6A (2010)', 'Sold in one hour, handover in 3 days'),
]

# Current stock: filled from sgcarmart links or photos the dealer sends. Each: (photo, name, reg year, price text, sgcarmart url)
STOCK = []


def story_html(s, link=True):
    return ('<article class="story" id="%s"><figure>%s</figure><div class="story-t"><span class="tag">%s</span><h3>%s</h3><p>%s</p>%s'
            '<small>Handover %s · <a href="%s" target="_blank" rel="noopener">Facebook post</a></small></div></article>') % (
        s['slug'], img(s['photo']), E(s['tag']), E(s['car']), E(s['gist']), '<p>%s</p>' % E(s['more']) if not link else '', E(s['date']), FB)


def sold_cards(items=SOLD):
    return '<div class="cars">%s</div>' % ''.join(
        '<div class="car"><span class="badge">Sold</span><figure>%s</figure><div class="car-t"><b>%s</b><span>%s</span></div></div>' % (img(p), E(n), E(note)) for p, n, note in items)


def stock_block():
    if STOCK:
        cards = ''.join('<a class="car" href="%s" target="_blank" rel="noopener"><span class="badge">For sale</span><figure>%s</figure><div class="car-t"><b>%s</b><span>%s · %s</span></div></a>'
                        % (u, img(p), E(n), E(y), E(pr)) for p, n, y, pr, u in STOCK)
        return '<div class="cars">%s</div><p style="margin-top:18px">%s</p>' % (cards, sgcm_btn('See every car on sgcarmart'))
    return ('<div class="stock"><figure>%s</figure><div class="stock-t"><p class="eyebrow">Live stock</p><h3>Our current cars are listed on sgcarmart</h3>'
            '<p>Prices, mileage and photos for every car in our showroom are on our sgcarmart dealer page, updated as cars sell. '
            'Looking for something that is not listed? Tell us the model and budget and we will source it.</p>'
            '<div class="cta-row">%s%s</div></div></div>') % (img('showroom'), sgcm_btn(), wa_btn('Ask what is in stock', 'your current cars for sale.', 'btn btn-wa'))


# ----------------------------------------------------------------------------------------------
# Services
# ----------------------------------------------------------------------------------------------
SERVICES = [
    dict(slug='buy-a-used-car', short='Buy a used car', photo='handover-vw-passat',
         title='Buy a Used Car in Singapore | Star Performance Motor',
         desc='Quality used cars from our Yishun showroom. Test drive, pre-purchase inspection at your own workshop, clear paperwork. WhatsApp 9742 7491.',
         h1='Buy a used car from Star Performance Motor',
         gist='Quality pre-owned cars, a test drive, and an inspection at the workshop you trust.',
         lede='Pick a car from our showroom or our sgcarmart list, drive it, and have it checked at your own workshop before you commit.',
         answer='Buying a used car from Star Performance Motor means you see the car at our showroom at North Spring Bizhub in Yishun, take it for a test drive, and can have it inspected at a workshop of your choice before you pay in full. We explain the paperwork and hand the car over when the transfer is done.',
         body=[('How buying from us works', None, [
             ('Choose', 'Browse our live stock on sgcarmart or tell us on WhatsApp what you need: model, budget, how long you plan to keep it.'),
             ('View and test drive', 'Come to the showroom in Yishun. We walk you round the car and you take it for a drive.'),
             ('Inspect', 'Book a pre-purchase inspection (PPI) at any workshop you trust. Customers often ask us to come along, and we do.'),
             ('Deposit and paperwork', 'Once you are happy, a deposit holds the car while we prepare the transfer and any trade-in.'),
             ('Handover', 'You collect the car and the keys. Questions after pickup go to the same person you dealt with.')]),
             ('What customers mention most', [
                 ('Transparency.', 'Reviewers describe "no hidden fees" and a car "delivered in the exact condition promised".'),
                 ('Inspection without pressure.', 'Several buyers say our team went with them to the PPI and explained the results.'),
                 ('First-time buyers.', 'Many reviews come from first-time owners who were guided step by step.'),
                 ('Help after pickup.', 'One buyer found a minor issue two days after pickup and says it was repaired free of charge.')], None)],
         faqs=[('Can I get the car inspected before I buy?', 'Yes. You can book a pre-purchase inspection at any workshop you trust before you commit. In one August 2026 handover we drove the car to the buyer\'s workshop ourselves the day after he paid the deposit.'),
               ('Where can I see your cars?', 'At our showroom at 9 Yishun Industrial Street 1, #01-82 North Spring Bizhub, Singapore 768163. Our current cars are listed on our sgcarmart dealer page. Walk-ins are welcome, or WhatsApp 9742 7491 to book a time.'),
               ('Can I trade in my current car?', 'Yes. Tell us your car\'s model, registration year and mileage and we will make you an offer, which can go towards the car you buy.'),
               ('Do you help first-time buyers?', 'Yes. Many of our Facebook reviews are from first-time owners. We explain depreciation, COE, inspection and the transfer step by step.')]),
    dict(slug='sell-your-car', short='Sell or trade in your car', photo='handover-bmw-520i',
         title='Sell My Car in Singapore | Star Performance Motor',
         desc='Sell your car in Singapore to a Yishun dealer: send details on WhatsApp, get an offer, we inspect it and handle the transfer and loan. 9742 7491.',
         h1='Sell my car in Singapore: sell it to us or trade it in',
         gist='A fair, transparent offer for your car, outright or as a trade-in on your next one.',
         lede='Send us your car details on WhatsApp for an offer. Sell it to us outright, or trade it in against a car from our showroom.',
         answer='To sell your car to Star Performance Motor, WhatsApp us the model, registration year, mileage and a few photos. We make you an offer, inspect the car, and handle the ownership transfer. You can take the money or use it as a trade-in on a car from our showroom.',
         body=[('How selling works', None, [
             ('Send details', 'Model, registration date, mileage, COE expiry and a few photos on WhatsApp.'),
             ('Get an offer', 'We give you a figure and explain how we arrived at it.'),
             ('Inspection', 'We check the car in person to confirm its condition.'),
             ('Paperwork and payment', 'We handle the transfer and settle any outstanding loan with the bank as part of the deal.'),
             ('Handover', 'You hand over the car and keys, or drive away in your next car if you are trading in.')]),
             ('Recent examples', [
                 ('Kia Stinger.', 'Sold after a single viewing in August 2026, faster than the owner expected.'),
                 ('Trade-in to BMW 520i M Sport.', 'A customer who came only to sell his car test drove a BMW in our showroom and drove it home three days later.'),
                 ('Six cars in March 2022.', 'Each sold in one to three viewings, with handover in three to eight days.')], None)],
         faqs=[('How do I get an offer for my car?', 'WhatsApp 9742 7491 with your car\'s model, registration year, mileage, COE expiry and a few photos. We reply with an offer and arrange to see the car.'),
               ('Can you take over my outstanding car loan?', 'An outstanding loan is settled with the bank as part of the sale, and you receive the balance. Tell us your loan balance when you ask for an offer.'),
               ('Should I sell outright, trade in or consign?', 'Selling outright is fastest. Trading in saves a step if you are buying from us. Consignment can fetch more if you can wait. Our guide compares all three.'),
               ('Do you buy cars near the end of their COE?', 'Yes, and an older car may be worth more as an export. See our export service.')]),
    dict(slug='car-consignment', short='Consign your car', photo='sold-mercedes-glb200',
         title='Car Consignment in Singapore | Star Performance Motor',
         desc='Consign your car with Star Performance Motor: we market it, handle viewings and paperwork, and you get paid when it sells. WhatsApp 9742 7491.',
         h1='Car consignment in Singapore: we sell your car for you',
         gist='We market your car and handle viewings and paperwork. You get paid when it sells.',
         lede='Consignment suits owners who want a better price than a quick sale and can wait for the right buyer.',
         answer='Consignment means Star Performance Motor sells your car for you. We photograph and list it, answer enquiries, show it to buyers and handle the paperwork. You agree the selling price with us and are paid when the sale completes. Terms are agreed with you before we list the car.',
         body=[('How does car consignment work?', None, [
             ('Agree the plan', 'We look at your car and agree a target price and the terms with you.'),
             ('Listing', 'We photograph your car and list it, including on our sgcarmart dealer page and social media.'),
             ('Viewings', 'We take the calls and arrange viewings and test drives with serious buyers.'),
             ('Sale and paperwork', 'When a buyer commits we handle the deposit, the loan settlement and the ownership transfer.'),
             ('You get paid', 'You receive the agreed amount when the sale completes.')]),
             ('Why owners consign', [
                 ('Time.', 'No calls from strangers or weekend viewings for you.'),
                 ('Reach.', 'Your car is shown to our buyers and our followers.'),
                 ('Track record.', 'Our March 2022 consignment posts show cars sold in one to three viewings.')], None)],
         faqs=[('What is car consignment?', 'You keep ownership while a dealer markets your car, handles enquiries and viewings, and completes the sale. You are paid when it sells.'),
               ('How long does consignment take?', 'It depends on the car and the price. Six cars we posted in March 2022 sold in one to three viewings, with handover three to eight days after sale.'),
               ('What does consignment cost?', 'Terms are agreed before we list your car. WhatsApp 9742 7491 for the current terms.'),
               ('Can I still use my car while it is consigned?', 'Ask us when we agree the terms. It depends on how viewings will be arranged.')]),
    dict(slug='car-export', short='Export your car', photo='handover-toyota-vellfire',
         title='Car Export in Singapore Near COE Expiry | Star Performance',
         desc='Car near the end of its COE? Star Performance Motor finds export offers and can help you upgrade to your next car. WhatsApp 9742 7491.',
         h1='Car export in Singapore: export your car near the end of its COE',
         gist='Near the end of its COE? We find an export offer so you get the most from your car.',
         lede='When a car is close to COE expiry, an export buyer can pay more than a local one. We find the offer and help you move to your next car.',
         answer='When your car is near the end of its COE, Star Performance Motor can find an export buyer for it. An exported car is deregistered in Singapore, so any rebates due to you under LTA rules are paid on deregistration. We compare the export offer with a local sale and help you upgrade.',
         body=[('How it works', None, [
             ('Tell us about your car', 'Model, registration date, COE expiry and condition, on WhatsApp.'),
             ('Export offer', 'We find an export offer and compare it with what the car would fetch locally.'),
             ('Deregistration', 'The car is deregistered with LTA when it leaves Singapore. Rebates due to you are paid under LTA rules.'),
             ('Your next car', 'If you are upgrading, we line up your next car so you are not left without one.')]),
             ('A recent example', [
                 ('Toyota Vellfire, August 2026.', 'A customer whose car was near the end of its COE took an export offer we secured, then bought a Toyota Vellfire from us.')], None)],
         faqs=[('Is it better to export or renew my COE?', 'It depends on the car\'s condition, its export value and the current COE premium. Send us the details and we will compare the options for you.'),
               ('What rebates do I get when my car is exported?', 'When a car is deregistered, LTA pays the PARF rebate (for eligible cars) and the COE rebate for unused COE to the owner. Check your car\'s figures on LTA\'s OneMotoring site.'),
               ('Do you import cars too?', 'We list import on our Facebook page. WhatsApp 9742 7491 to ask about a specific car.')]),
    dict(slug='car-sourcing', short='Find a specific car', photo='handover-vw-tiguan',
         title='Car Sourcing in Singapore | Star Performance Motor',
         desc='Looking for a specific model? Star Performance Motor searches its network for a well-kept unit that fits your budget. WhatsApp 9742 7491.',
         h1='Looking for a specific car? We find it',
         gist='Tell us the model and budget. We search our network for a well-kept unit.',
         lede='From a Volkswagen Tiguan R-Line to a Honda Civic Type R FD2R, we search our network for the right unit at the right price.',
         answer='Car sourcing at Star Performance Motor starts with your model, budget and must-haves. We search our dealer network and private sellers for a well-maintained unit, check it, and bring it to you for viewing and inspection before you commit.',
         body=[('How sourcing works', None, [
             ('Brief us', 'Model, year range, budget, colour and anything you will not compromise on.'),
             ('We search', 'We look through our network and listings for units that fit.'),
             ('Shortlist', 'We share the best options with photos and history, and tell you what to look out for.'),
             ('View and inspect', 'You view and test drive the car and can have it inspected at your own workshop.'),
             ('Handover', 'We complete the purchase, the transfer and any trade-in for you.')]),
             ('Recent examples', [
                 ('Volkswagen Tiguan 2.0 R-Line, August 2026.', 'Sourced through our network after we sold the customer\'s Kia Stinger.'),
                 ('Honda Civic Type R FD2R.', 'A customer writes that Celsius searched "high and low" for a unit that matched his budget and was a good, solid car.')], None)],
         faqs=[('Can you find a car that is not in your showroom?', 'Yes. Tell us the model and budget on WhatsApp and we will search our network for it.'),
               ('Can I inspect a sourced car before buying?', 'Yes. You can view, test drive and have it inspected at a workshop of your choice before you commit.'),
               ('Do you source enthusiast cars?', 'Yes. Recent searches include a Honda Civic Type R FD2R and a modified BMW 520i M Sport.')]),
]
SVC = {s['slug']: s for s in SERVICES}


def service_body(s):
    (h_steps, _, st), (h_why, why, _) = s['body']
    rel_stories = [x for x in STORIES if s['slug'] in x['services']]
    stories = ''.join(story_html(x) for x in rel_stories)
    others = ''.join(tile('services/%s/' % o['slug'], o['photo'], o['short'], o['gist']) for o in SERVICES if o['slug'] != s['slug'])
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">{E(s['answer'])}</p>
<figure class="lead-fig">{img(s['photo'], eager=True)}</figure>
<h2>{E(h_steps)}</h2>{steps(st)}
<h2>{E(h_why)}</h2>{ticks(why)}
{'<h2>Recent handovers</h2><div class="stories">%s</div>' % stories if stories else ''}
<h2>What customers say</h2>{revs_carousel(5)}
<p class="small">{E(PROOF_LINE)}. <a href="{FB_REVIEWS}" target="_blank" rel="noopener">Read the reviews on Facebook</a>.</p>
<h2>Frequently asked questions</h2>{faq_html(s['faqs'])}
</article>
<aside class="side"><div class="card sticky"><h2>Talk to us</h2><p>WhatsApp +65 {WA_SHOW} or visit us at North Spring Bizhub, Yishun.</p>{wa_btn('WhatsApp us', s['short'].lower() + '.')}{sgcm_btn('Cars on sgcarmart', 'btn btn-ghost')}
<p class="small" style="margin-top:14px"><a href="sold-cars/">Sold cars →</a><br><a href="reviews/">Reviews →</a><br><a href="articles/">Guides →</a></p></div></aside>
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Other services</h2></div><div class="scards">{others}</div></div></section>'''


# ----------------------------------------------------------------------------------------------
# Articles
# ----------------------------------------------------------------------------------------------
LTA = 'https://onemotoring.lta.gov.sg/'
LTA_TRANSFER = 'https://onemotoring.lta.gov.sg/content/onemotoring/home/selling-deregistering/transfer-ownership.html'
MAS_LOANS = 'https://www.mas.gov.sg/regulation/explainers/motor-vehicle-loans'
MAS_USED = 'https://www.mas.gov.sg/regulation/explainers/motor-vehicle-loans/adjusting-the-value-of-used-motor-vehicles'


class Raw(str):
    """A paragraph that is already HTML (used for an editorial in-body link)."""


ARTICLES = [
    dict(slug='what-is-a-pre-purchase-inspection', modified='2026-11-02', photo='handover-bmw-520i', svc='buy-a-used-car',
         title='What Is a Pre-Purchase Inspection (PPI)? | Star Performance',
         desc='A pre-purchase inspection is an independent workshop check of a used car before you buy. What it covers, when to book it and what to ask.',
         h1='What is a pre-purchase inspection (PPI) for a used car?',
         answer='A pre-purchase inspection (PPI) is a check of a used car by a workshop you choose, done before you pay in full. The mechanic looks at the engine, gearbox, suspension, brakes, electronics and body for faults or past accident repairs, so you know the real condition of the car and can decide, or negotiate, with facts.',
         sections=[('When should you book a PPI?', ['After the test drive and before you pay the full amount. Many buyers place a refundable or conditional deposit to hold the car while the inspection is arranged. Ask the dealer how the deposit works if the PPI finds a problem.']),
                   ('What does a PPI usually cover?', ['Most workshops read fault codes with a diagnostic scanner, check fluids and leaks, inspect the underside, test the brakes and suspension, look for signs of accident repair or flooding, and road test the car. Ask your workshop for a written list of findings.']),
                   ('Which workshop should do it?', ['A workshop you trust, ideally one that knows the make. One of our August 2026 buyers chose a workshop that turned out to have serviced that very Toyota Vellfire for years, which gave him its full history.']),
                   ('What if the PPI finds something?', ['Small wear items are normal on a used car. Larger issues can be fixed before handover, reflected in the price, or be a reason to walk away. A good dealer talks you through the report rather than rushing you.']),
                   ('What to bring and what to ask', ["Bring the listing details, the registration details and the dealer's contact. Ask the workshop for its fee and how long the inspection takes, and ask for the findings in writing, with photos where possible. Tell the mechanic what worries you about the car so that it gets extra attention."]),
                   ('How to read the report', ['Separate the findings into three groups: safety items such as brakes, tyres and steering, normal wear items, and cosmetic points. Safety items should be fixed before you pay in full. Wear items and cosmetic points are good grounds to talk about the price. A pattern of serious problems is a good reason to walk away.']),
                   ('How the inspection fits with the other checks', [Raw('A PPI does not replace the test drive, and it does not show the yearly cost of owning the car. Use the <a href="articles/what-to-check-on-a-used-car-test-drive/">test drive checklist</a> first, compare cars with the <a href="articles/what-does-depreciation-mean-on-a-car-listing/">depreciation figure</a>, and then book the PPI on the car you want to buy.')]),
                   ('Is a PPI worth it on a car that looks clean?', ['Yes. A clean car can still hide worn parts, past repairs or a fault that has not shown up yet, and a few hours with a mechanic costs far less than finding out after you have paid. The inspection also gives you something concrete to base your decision on, which makes the purchase calmer for both buyer and seller. Booking one is a sign of a careful buyer, and a good dealer welcomes it.'])],
         faqs=[('Who pays for the pre-purchase inspection?', 'Usually the buyer, because the workshop works for you. Ask the workshop for its fee when you book.'),
               ('Will a dealer let me do a PPI?', 'A transparent dealer will. At Star Performance Motor buyers can book a PPI at their own workshop, and we often go along.'),
               ('Is a PPI the same as an LTA inspection?', 'No. LTA\'s periodic inspection checks roadworthiness and emissions. A PPI is a wider condition check done for the buyer.')]),
    dict(slug='trade-in-vs-consignment-vs-direct-sale', photo='sold-audi-a4-2017', svc='sell-your-car',
         title='Trade-In vs Consignment vs Direct Sale | Star Performance',
         desc='Three ways to sell your car in Singapore compared: speed, effort and price. Which suits you depends on how soon you need the money.',
         h1='Trade-in, consignment or direct sale: which way should you sell your car?',
         answer='Sell directly to a dealer if you want the fastest, simplest sale. Trade in if you are buying your next car from the same dealer and want one transaction. Consign if you can wait for the right buyer and want the dealer to handle viewings and paperwork. The right choice depends on time, effort and price.',
         table=[['', 'Direct sale to dealer', 'Trade-in', 'Consignment'], ['Speed', 'Fastest', 'Same day as your purchase', 'Depends on the buyer'],
                ['Effort for you', 'Low', 'Lowest: one deal', 'Low: dealer handles viewings'], ['Price', 'Dealer\'s offer', 'Offer set against your next car', 'Often higher, not fixed'],
                ['Best for', 'You need the money or space now', 'You are buying from the same dealer', 'You can wait for the right buyer']],
         sections=[('Direct sale', ['The dealer buys your car, settles any loan with the bank and pays you the balance. It is quick and certain, and you know the figure up front.']),
                   ('Trade-in', ['Your car\'s value goes towards the car you buy from the same dealer. You avoid a gap without a car and handle one set of paperwork. In August 2026 one of our customers came only to sell his car and drove home in a BMW 520i M Sport three days later.']),
                   ('Consignment', ['The dealer markets your car and finds the buyer while you keep ownership. It can fetch more but takes longer, and the terms (fees, duration, viewings) should be agreed in writing first.'])],
         faqs=[('Which way of selling gets the highest price?', 'Consignment often gets more because the car is sold to a private buyer, but it is not guaranteed and takes longer.'),
               ('Can I sell a car with an outstanding loan?', 'Yes. The loan is settled with the bank as part of the sale and you receive the balance.'),
               ('What details does a dealer need for an offer?', 'Model, registration date, mileage, COE expiry, service history and a few photos.')]),
    dict(slug='car-near-coe-expiry-export-or-renew', modified='2026-11-02', photo='handover-toyota-vellfire', svc='car-export',
         title='COE Expiring? Export, Scrap or Renew | Star Performance',
         desc='Your car\'s COE is ending. The three options in Singapore (renew, export or scrap) and what to compare before you decide.',
         h1='Car near the end of its COE: export, scrap or renew?',
         answer='When a car\'s COE is close to expiry you can renew the COE and keep driving, or deregister the car by exporting or scrapping it. Exporting can pay more than scrapping for a car in good condition. Compare the export offer, the rebates due on deregistration and the cost of renewing before you decide.',
         sections=[('Option 1: renew the COE', ['You pay the Prevailing Quota Premium to extend the COE for 5 or 10 years. It suits a car you know well and want to keep. Check the current premium on LTA\'s OneMotoring site.']),
                   ('Option 2: export the car', ['An export buyer pays for the car and ships it overseas, and the car is deregistered in Singapore. Popular models in good condition often fetch more this way than through a local sale near COE expiry.']),
                   ('Option 3: scrap the car', ['The car is deregistered and scrapped. This is usually the choice for cars that are not worth exporting.']),
                   ('Rebates on deregistration', ['When a car is deregistered, LTA pays any PARF rebate (for eligible cars) and a COE rebate for the unused part of the COE to the owner. Your car\'s figures are on LTA\'s OneMotoring site.']),
                   ('What to gather before you compare', ["Have your registration date, COE expiry date, mileage and a short description of the car's condition ready. With these a dealer that handles exports can give you an offer, and you can look up your rebates and the renewal cost on LTA OneMotoring. Ask for any offer in writing so you can compare the options on the same terms."]),
                   ('When renewing makes sense', ['Renewing suits a car you know well, that is in good condition and that you plan to keep for the extra years. Think about the costs of keeping an older car, such as servicing and repairs, and compare the total with the net amount you would receive from exporting. If you plan to change cars soon anyway, exporting and buying another may be simpler.']),
                   ('Timing and paperwork', [Raw('Deregistration is done with LTA, and any outstanding car loan has to be settled with the bank first, so start early rather than in the last days of the COE. Our guide on <a href="articles/what-do-you-need-to-sell-your-car-in-singapore/">what you need to sell your car in Singapore</a> lists the documents, and you can read how we handle this on our <a href="services/car-export/">car export page</a> or WhatsApp us your car details.')]),
                   ('A simple way to decide', ['Put the three options side by side on one page: the net amount from exporting, the rebates from deregistering and scrapping, and the renewal cost plus what you expect to spend keeping the car running. The option with the best result for your own plans is usually clear once the numbers are written down. If you are unsure, WhatsApp us your car details and we will explain what an export would involve before you commit to anything.'])],
         faqs=[('How do I know my car\'s export value?', 'Ask a dealer that handles exports for an offer. Send the model, registration date, COE expiry and mileage.'),
               ('Can I export my car and buy another at the same time?', 'Yes. In August 2026 one of our customers exported his old car through us and bought a Toyota Vellfire.'),
               ('Where can I check my rebates?', 'On LTA\'s OneMotoring website, using your vehicle details.')]),
    dict(slug='buying-your-first-used-car-in-singapore', modified='2026-11-02', photo='handover-vw-passat', svc='buy-a-used-car',
         title='Buying Your First Used Car in Singapore: Checklist',
         desc='First used car? A simple checklist: budget with depreciation, COE left, loan limits, insurance, test drive, inspection and the ownership transfer.',
         h1='Buying your first used car in Singapore: a checklist',
         answer='For a first used car, set a budget that includes depreciation, insurance, road tax and running costs, not only the price. Check how much COE is left, take a proper test drive, book a pre-purchase inspection at a workshop you trust, and make sure the ownership transfer is done through LTA before you drive off.',
         sections=[('1. Set the full budget', ['Look at the depreciation figure on each listing (the yearly cost of owning the car), then add insurance, road tax, parking, fuel and servicing.']),
                   ('2. Check the COE', ['How many years are left on the COE decides how long you can drive the car and how much its depreciation is.']),
                   ('3. Car loan', ['MAS sets the maximum loan amount and tenure for car loans. Check the current limits on the MAS website and ask the dealer or your bank for the rate.']),
                   ('4. Test drive and inspection', ['Drive the car on roads you know and book a pre-purchase inspection before you pay in full.']),
                   ('5. Paperwork', ['The ownership transfer is done on LTA\'s OneMotoring. Make sure insurance starts from the day you take the car.']),
                   ('Questions to ask the dealer', ['Ask for the registration date, the COE expiry date, the number of previous owners and the service records. Ask whether the car has any outstanding loan and how the deposit works if the inspection finds a problem. A dealer who answers these clearly and in writing is easier to trust than one who rushes you.']),
                   ('Mistakes first-time buyers make', ['The most common one is looking only at the monthly instalment instead of the total cost of owning the car. Others are ignoring how much COE is left, skipping the inspection because the car looks clean, and paying in full before the inspection is done. Taking your time on each step avoids most of them.']),
                   ('On the day you collect the car', [Raw('Confirm that the ownership transfer has been completed, that your insurance starts from that day, and that you have received the keys and documents. Take photos of the car at handover. Our guide on <a href="articles/what-to-do-after-buying-a-used-car/">what to do after buying a used car</a> lists the follow-up steps, and our <a href="articles/what-is-a-pre-purchase-inspection/">pre-purchase inspection guide</a> explains the check to book beforehand.')]),
                   ('Take it one step at a time', ['Buying a first car feels like many decisions at once, but they come in a clear order: decide what you can afford each year, shortlist cars with enough COE left, test drive, inspect, then agree the price and paperwork. You do not have to decide everything on the first visit. Many first-time buyers visit more than once, bring a family member or friend, and ask questions by WhatsApp in between. Our team is happy to answer them at +65 9742 7491.'])],
         faqs=[('How much should a first-time buyer budget for a used car?', 'Start from the depreciation you can afford each year, then add insurance, road tax and running costs. A dealer can show you cars that fit that number.'),
               ('Do I need a PPI for my first car?', 'It is strongly recommended. It tells you the real condition of the car before you commit.'),
               ('Can a dealer help a first-time buyer?', 'Yes. Many of our Facebook reviews are from first-time owners who were guided step by step.')]),
    dict(slug='what-does-depreciation-mean-on-a-car-listing', modified='2026-11-02', photo='sold-mercedes-glb200', svc='buy-a-used-car',
         title='What Is Depreciation on a Car Listing? | Star Performance',
         desc='Depreciation on a Singapore used car listing is the yearly cost of owning the car. How it is worked out and how to use it to compare cars.',
         h1='What does "depreciation" mean on a Singapore used car listing?',
         answer='On a Singapore used car listing, depreciation is roughly what the car costs you per year of COE remaining. It is the price minus what you would get back when the car is deregistered (such as the PARF rebate), divided by the years of COE left. A lower figure means cheaper ownership per year, which is why buyers compare it.',
         sections=[('How it is worked out', ['Take the selling price, subtract the rebate value you would expect when the COE ends, and divide by the remaining COE life in years. Listing sites show this figure for you.']),
                   ('Why it matters more than price', ['A cheaper car with little COE left can cost more per year than a dearer car with many years left. Depreciation puts them on the same footing.']),
                   ('Low depreciation does not mean a bad car', ['A low figure can simply mean a well-priced car. In August 2026 one of our buyers chose a keenly priced Toyota Vellfire, and his independent inspection found it in excellent condition. Always inspect, whatever the price.']),
                   ('A plain-language example', ['Take two cars listed at the same price. One has only a few years of COE left and the other has many. The same money is spread over fewer years on the first car, so its depreciation per year looks higher. The second car looks cheaper to own each year, even though the price on the listing is identical. That is the comparison the figure is built for.']),
                   ('What the figure leaves out', ["Depreciation covers the car's value over its remaining COE only. Insurance, road tax, parking, fuel, servicing and any loan interest are on top, so add them when you work out what a car really costs you each month. The rebate values behind the figure are set by LTA and can change, so check your own numbers on LTA OneMotoring before you rely on them."]),
                   ('How to use it when you shortlist cars', [Raw('Pick three or four cars you like and compare their depreciation side by side, then look at the things the figure cannot show: condition, mileage, service records and how the car feels on a test drive. Read our guides on <a href="articles/what-is-the-parf-rebate-and-how-is-it-calculated/">the PARF rebate</a> and on <a href="articles/should-you-buy-a-used-car-with-little-coe-left/">buying a car with little COE left</a>, then book a <a href="articles/what-is-a-pre-purchase-inspection/">pre-purchase inspection</a> on the car you choose. You can also WhatsApp us the cars you are comparing and we will give you our honest view.')]),
                   ('Where the number comes from and who sets it', ["The depreciation on a listing is an estimate worked out from the asking price, the remaining COE and the rebate you would get on deregistration. Different listing sites may present it slightly differently, so compare cars on the same site. If a figure looks unusually low or high, ask the dealer how it was calculated and check the COE expiry date and registration date against the car's own documents. A dealer who is happy to explain the number is usually a dealer who is happy to explain the car."])],
         faqs=[('Is a lower depreciation always better?', 'It means lower cost per year, but condition still matters. Pair it with a pre-purchase inspection.'),
               ('Does depreciation include insurance and road tax?', 'No. It covers the car\'s value over its remaining COE only.'),
               ('Where can I compare depreciation?', 'On listing sites such as sgcarmart, which show the figure for each car.')]),
    # EDGE daily article 18 Oct 2026 (hand-built; facts: LTA OneMotoring transfer-of-ownership page read 18 Oct 2026; sister shop = same unit, declared)
    dict(slug='what-to-do-after-buying-a-used-car', photo='showroom', svc='buy-a-used-car', date='2026-10-18',
         title='What to Do After Buying a Used Car in Singapore',
         desc='Just bought a used car? Confirm the LTA transfer within 7 days, check insurance and road tax, match the car to LTA records, then plan servicing and care.',
         h1='What should you do after buying a used car in Singapore?',
         answer='In the first week, confirm the ownership transfer on LTA\'s OneMotoring (it must be done within 7 days), make sure motor insurance in your name covers the road tax period, and check the car\'s details match LTA\'s records. Then book a first service with a workshop you trust and decide how you will look after the paint and interior.',
         sections=[('Is the ownership transfer done?', [Raw('LTA says the ownership of a second-hand car must be transferred to the new owner within 7 days of it changing hands. The seller or dealer starts the transfer online, and it takes effect once you, the new owner, confirm it with Singpass 2FA. Afterwards, check that OneMotoring shows the car in your name (<a href="%s" target="_blank" rel="noopener">LTA OneMotoring, transfer of ownership</a>, read 18 October 2026).' % LTA_TRANSFER)]),
                   ('Are your insurance and road tax in order?', ['Before you confirm the transfer, the car must have valid motor insurance under your name, covering the full period of its valid road tax. Road tax already paid and any vehicle rebates move to you with the car, so note the road tax expiry date and whether an inspection is due before the next renewal.']),
                   ('Do the car\'s details match LTA\'s records?', ['LTA advises buyers to check that the make, model, engine number and chassis number tally with LTA records. Keep the sales agreement, the pre-purchase inspection report and the service records in one place: you will want them for the first service and again when you sell the car one day.']),
                   ('When should the first service be?', [Raw('If the service records do not show a recent service, book one early, ideally with the workshop that did your <a href="articles/what-is-a-pre-purchase-inspection/">pre-purchase inspection</a> or one that knows the make. You start with fresh fluids and a clear picture of the car\'s condition.')]),
                   ('How do you look after the paint and interior?', [Raw('Expressway driving chips the bonnet and front bumper first. If you want to keep the paint as it is, one option is <a href="https://wrapstarautostyle.com/services/paint-protection-film/">paint protection film at our sister shop Wrapstar Autostyle</a>, in the same unit as our showroom. A thorough interior clean is also worth doing early, so the car feels like yours from day one.')])],
         faqs=[('How long do I have to transfer a used car into my name?', 'LTA requires the transfer within 7 days of the car changing hands. It takes effect once you, as the new owner, confirm it online with Singpass 2FA.'),
               ('Is road tax transferred to the new owner?', 'Yes. LTA says taxes already paid and vehicle rebates are transferred to the new owner with the car.'),
               ('Do I need my own insurance before the transfer?', 'Yes. The car must have valid motor insurance in your name, covering the full period of its valid road tax, before you confirm the transfer.')]),
    # Daily article 19 Oct 2026 (hand-built; facts: MAS "Motor Vehicle Loans" explainer + "Adjusting the Value of Used Motor Vehicles", read 19 Oct 2026; no loan rates, no claim that we arrange loans)
    dict(slug='how-much-car-loan-can-i-get-for-a-used-car', photo='handover-vw-tiguan', svc='buy-a-used-car', date='2026-10-19',
         title='Used Car Loan Limits in Singapore | Star Performance',
         desc='How much can you borrow for a used car? MAS caps car loans at 70% or 60% of the price, set by OMV, for up to 7 years. How the used-car OMV is worked out.',
         h1='How much can you borrow to buy a used car in Singapore?',
         answer='Under MAS rules, a bank or finance company can lend at most 70% of a car\'s purchase price if its OMV is $20,000 or less, and at most 60% if the OMV is higher, for up to 7 years. For a used car, the OMV is reduced for the car\'s age, so many older cars fall into the 70% band.',
         table=[['Open market value (OMV)', 'Maximum loan', 'Maximum tenure'], ['$20,000 or less', '70% of the purchase price', '7 years'], ['More than $20,000', '60% of the purchase price', '7 years']],
         sections=[('What are the MAS car loan limits?', [Raw('MAS sets the maximum loan amount and tenure for anyone borrowing from a financial institution to buy a new or used car, including hire purchase, where the agreement to buy is on or after 27 May 2016. The limits are in the table above. The purchase price they apply to includes the relevant taxes and the COE. Motorcycles and commercial vehicles are not covered by these limits (<a href="%s" target="_blank" rel="noopener">MAS, Motor Vehicle Loans</a>, read 19 October 2026).' % MAS_LOANS)]),
                   ('How is the OMV worked out for a used car?', [Raw('Because a used car has lost value, the lender adjusts its OMV for age before deciding which band applies: OMV minus (age in months divided by 120, times the OMV). MAS\'s own example is a car with an OMV of $25,000 bought 37 months after its first registration: $25,000 minus 37/120 of $25,000 gives $17,292, so the 70%% limit applies. A car imported as a used vehicle uses a slightly different formula (<a href="%s" target="_blank" rel="noopener">MAS, Adjusting the Value of Used Motor Vehicles</a>, read 19 October 2026).' % MAS_USED)]),
                   ('What does that mean for your down payment?', ['The rest of the price is your down payment, paid in cash. As an illustration only: on a $60,000 car in the 70% band the most you can borrow is $42,000, so you pay at least $18,000 up front; in the 60% band you can borrow up to $36,000 and pay at least $24,000. Your bank or finance company decides the actual amount and rate.']),
                   ('Can you refinance a car loan later?', ['Yes. MAS allows refinancing up to the full outstanding amount if you meet the lender\'s credit assessment. For cars bought on or after 26 February 2013, the longest refinancing tenure is 7 years minus the years since the first loan was paid out.']),
                   ('What should you ask before you commit?', [Raw('Ask the seller for the car\'s OMV and its first registration date, so you know which band applies, and ask your lender for the interest rate and the total cost over the loan. Then compare the monthly instalment with the car\'s <a href="articles/what-does-depreciation-mean-on-a-car-listing/">depreciation figure</a>, so you budget for the full cost of owning it.')])],
         faqs=[('Do the MAS loan limits apply to used cars?', 'Yes. They apply to new and used cars bought with a loan from a financial institution on or after 27 May 2016. For a used car the OMV is adjusted for age first.'),
               ('Can I get a 100% car loan in Singapore?', 'Not from a bank or finance company for a car covered by the MAS rules: the most is 70% or 60% of the purchase price, depending on the OMV.'),
               ('What is the longest car loan tenure?', 'Seven years, for both OMV bands.')]),
    # Daily article 20 Oct 2026 (queue #3; hand-built; facts: LTA OneMotoring transfer-of-ownership page read 20 Oct 2026; our own process from the sell-your-car page)
    dict(slug='what-do-you-need-to-sell-your-car-in-singapore', photo='showroom', svc='sell-your-car', date='2026-10-20',
         title='What Do You Need to Sell Your Car in Singapore?',
         desc='Selling your car? What LTA needs for the ownership transfer, why any car loan must be settled first, keeping your number plate, and when to hand over the car.',
         h1='What do you need to sell your car in Singapore?',
         answer='To transfer your car to a buyer on LTA\'s OneMotoring you need the vehicle number and the buyer\'s ID number and name, and you log in with your own Singpass. Before that, the car must have no outstanding matters such as a car loan or road tax arrears, and you should receive the money before you transfer. The buyer then confirms the transfer, which must happen within 7 days.',
         sections=[('What details does LTA ask for?', [Raw('LTA lists what the seller needs to start the transfer online: the vehicle registration number, the next owner\'s ID number (NRIC, FIN or company registration number) and name, and optionally their mobile number and email. You get an SMS once you have applied, and the buyer gets an SMS to log in and confirm (<a href="%s" target="_blank" rel="noopener">LTA OneMotoring, transfer of vehicle ownership</a>, read 20 October 2026).' % LTA_TRANSFER)]),
                   ('Does the car loan have to be paid off first?', ['Yes. LTA says the vehicle should not have any outstanding matters, such as financial loans or road tax arrears, and that vehicles being transferred should not be under financing. If you still owe the bank, the loan is settled as part of the sale before the transfer goes through. When you sell to us, we settle any outstanding loan with the bank as part of the deal.']),
                   ('Can you keep your car number?', ['Yes, if you retain it before the transfer. LTA says to retain the vehicle number first if you want to keep it; after the transfer it goes with the car.']),
                   ('What happens to road tax and rebates?', ['Road tax already paid and the car\'s rebates, such as any PARF or COE rebate it may enjoy, are transferred to the new owner with the car. Allow for that when you agree the price.']),
                   ('When should you hand over the car?', ['LTA advises sellers to transfer only after the money is received, especially when paying by cheque, and the buyer should accept the transfer before the car is handed over. Never let anyone use your Singpass to transfer the car on your behalf.']),
                   ('Is it easier to sell through a dealer?', [Raw('A dealer takes care of the paperwork for you. If you sell to Star Performance Motor, we make you an offer, inspect the car and handle the ownership transfer and any loan settlement. See <a href="services/sell-your-car/">how selling your car to us works</a>, or compare <a href="articles/trade-in-vs-consignment-vs-direct-sale/">trade-in, consignment and direct sale</a>.')])],
         faqs=[('Do I need my log card to sell my car?', 'The online transfer on OneMotoring asks for the vehicle number and the buyer\'s ID number and name, and you log in with your own Singpass. Keep your sales agreement and service records ready for the buyer.'),
               ('Can I sell a car that still has a loan?', 'Yes, but the loan must be settled before the ownership transfer, because LTA says vehicles being transferred should not be under financing.'),
               ('How long does the buyer have to confirm the transfer?', 'LTA requires the ownership to be transferred to the new owner within 7 days. The buyer confirms it online after the seller starts it.')]),
    # Night run 26 Oct 2026 (added to build.py 28 Oct 2026 so a rebuild keeps it; matches the live page)
    dict(slug='should-you-buy-a-used-car-with-little-coe-left', photo='handover-toyota-vellfire', svc='buy-a-used-car', date='2026-10-26',
         title='Buying a Used Car With Little COE Left: What to Weigh',
         desc='Thinking of a used car with little COE left? How remaining COE affects the price and cost per year, what happens when it ends, and what to ask first.',
         h1='Should you buy a used car with little COE left?',
         answer='A used car with little COE left can be good value, because the asking price usually reflects the time remaining. But you have a short window to enjoy it before you must renew the COE, export the car or scrap it. Work out the yearly cost of owning it, and decide now what you will do when the COE ends.',
         sections=[('How does the COE left affect the price?', [Raw('The COE is the right to keep the car on the road for a fixed period, so a car with less time left has less of that right to sell. That is why two otherwise similar cars can be priced very differently. Do not compare asking prices alone. Look at the listing\'s <a href="articles/what-does-depreciation-mean-on-a-car-listing/">depreciation figure</a>, which spreads the cost of the car over the time you can use it, and compare that across cars.')]),
                   ('What happens when the COE runs out?', [Raw('You have three choices: renew the COE and keep the car, export it, or scrap it. Renewing means paying the prevailing quota premium for a further 5 or 10 years, so it only makes sense for a car you are happy to keep. Exporting or scrapping deregisters the car, and you may receive rebates for the unused part of the COE and, for eligible cars, the PARF. Our guide to a <a href="articles/car-near-coe-expiry-export-or-renew/">car near the end of its COE</a> compares the three options, and you can check the current premium and your rebates on LTA OneMotoring.')]),
                   ('Who is a short-COE car suited to?', ['It can suit a buyer who needs a car for a limited time, such as a few years before moving abroad or changing plans, and who wants to pay for only the time they will use. It suits you less if you want to keep the car for many years without a large renewal cost, or if you would rather have the certainty of a long COE.']),
                   ('What should you ask before you buy?', [Raw('Ask for the exact COE expiry date, not just "a few years". Ask for the depreciation figure, the service records and the number of previous owners. Decide what you will do at expiry and whether the numbers still work if you renew. Then have the car checked: a <a href="articles/what-is-a-pre-purchase-inspection/">pre-purchase inspection</a> at a workshop you trust is worth doing whatever the COE says.')]),
                   ('How do you compare it with a longer-COE car?', [Raw('Put the two cars side by side on cost per year: price, running costs and what you expect to get back or pay at the end. A cheaper car with little COE is not automatically the better deal, and a dearer car with a long COE is not automatically wasteful. If you are still working out your budget, our <a href="articles/buying-your-first-used-car-in-singapore/">first used car checklist</a> covers the other costs to include.')])],
         faqs=[('Is a used car with little COE left cheaper?', 'Usually the asking price reflects the time left, but do not judge by price alone. Compare the yearly depreciation figure and the car\'s condition with other cars on the market.'),
               ('Can I renew the COE after I buy the car?', 'Yes. A COE can be renewed for 5 or 10 years by paying the prevailing quota premium. Check the current rules and premium on LTA\'s OneMotoring website before you decide.'),
               ('Can I get the car inspected before I commit?', 'Yes. At Star Performance Motor you can view and drive the car at our Yishun showroom and have it inspected at a workshop of your choice before you pay in full.')]),
    # Night run 28 Oct 2026 (even day; facts: our consignment page and March 2022 consignment posts; no promised timeframe; no official figures)
    dict(slug='how-long-does-car-consignment-take-in-singapore', photo='sold-mercedes-glb200', svc='car-consignment', date='2026-10-28',
         title='How Long Does Car Consignment Take in Singapore?',
         desc='How long does selling a car on consignment take in Singapore? What affects the wait, what we cannot promise, and what you can do to help it sell.',
         h1='How long does it take to sell a car through consignment?',
         answer='There is no fixed timeline for selling a car on consignment, because the car sells when a buyer agrees to your price. How fast that happens depends on the asking price, the car\'s condition and mileage, how much COE it has left, and how ready the paperwork is. Six cars we posted in March 2022 sold in one to three viewings, but that is an example, not a promise.',
         sections=[('Is there a normal timeframe for consignment?', ['No honest dealer can give one before seeing the car. Six cars we posted in March 2022 sold in one to three viewings, with handover three to eight days after the sale. Those were different cars in a different market, so treat them as an illustration of how it can go, not as a timeframe for yours.']),
                   ('What decides how fast a consigned car sells?', ['Mainly the price compared with similar cars on the market. After that come the condition, the mileage and service records, how much COE is left, and how well the car is photographed and presented. A fair price on a clean, well-documented car draws viewings sooner than a high price on a car with gaps in its history.']),
                   ('What happens once a buyer says yes?', [Raw('When a buyer commits we handle the deposit, the loan settlement if you still owe the bank, and the ownership transfer, and you receive the agreed amount when the sale completes. The paperwork side is explained in <a href="articles/what-do-you-need-to-sell-your-car-in-singapore/">what you need to sell your car in Singapore</a>.')]),
                   ('How can you help your car sell sooner?', ['Agree a realistic target price with us at the start, and ask how any later change to the price would be handled when you agree the terms. Have your service records and documents ready, keep the car clean, and tell us when you are free for viewings, because serious buyers often want to see it at short notice.']),
                   ('When is another way of selling better?', [Raw('If you need the money by a certain date, selling the car to a dealer outright is the quickest route, while consignment suits owners who can wait for a better price. Our comparison of <a href="articles/trade-in-vs-consignment-vs-direct-sale/">trade-in, consignment and direct sale</a> sets out the differences, and the full process is on our <a href="services/car-consignment/">car consignment page</a>.')])],
         faqs=[('Can you tell me how long my car will take to sell?', 'Not before we have seen it. We look at your car, then agree a target price and the terms with you, and we can discuss what to expect for your particular car.'),
               ('What does consignment cost?', 'Terms are agreed before we list your car. WhatsApp +65 9742 7491 for the current terms.'),
               ('Can I still use my car while it is consigned?', 'Ask us when we agree the terms. It depends on how viewings will be arranged.')]),
]

LASTMOD = {'articles/%s/' % a['slug']: a.get('modified', a.get('date')) for a in ARTICLES if a.get('modified') or a.get('date')}
LASTMOD['services/sell-your-car/'] = '2026-10-23'  # Booster 23 Oct 2026: title/H1/description on 'sell my car singapore'
LASTMOD['services/car-consignment/'] = '2026-10-19'  # Booster 19 Oct 2026: H1 + first H2 on the term 'car consignment singapore'


def article_body(a):
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % (p if isinstance(p, Raw) else E(p)) for p in ps)) for h, ps in a['sections'])
    table = ''
    if a.get('table'):
        hdr, rows = a['table'][0], a['table'][1:]
        table = '<table class="cmp"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (
            ''.join('<th>%s</th>' % E(c) for c in hdr), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % E(c) for c in r) for r in rows))
    s = SVC[a['svc']]
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">{E(a['answer'])}</p>
<figure class="lead-fig">{img(a['photo'], eager=True)}</figure>
{table}{secs}
<p>Related: <a href="services/{s['slug']}/">{E(s['h1'])}</a>. Official rules and figures: <a href="{LTA}" target="_blank" rel="noopener">LTA OneMotoring</a>.</p>
<h2>Frequently asked questions</h2>
{faq_html(a['faqs'])}
<p class="byline">By the team at {LEGAL}, Yishun. Last updated {a.get('modified', a.get('date', UPDATED))}. General information only; check current rules with LTA.</p>
</article>
<aside class="side"><div class="card sticky"><h2>Ask us</h2><p>Buying, selling, consigning or exporting? WhatsApp +65 {WA_SHOW}.</p>{wa_btn('WhatsApp us')}{sgcm_btn('Cars on sgcarmart', 'btn btn-ghost')}
<p class="small" style="margin-top:14px"><a href="services/">Services →</a><br><a href="reviews/">Reviews →</a><br><a href="articles/">All guides →</a></p></div></aside>
</div></section>'''


def article_schema(a, path):
    return {'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': a.get('date', UPDATED), 'dateModified': a.get('modified', a.get('date', UPDATED)),
            'author': {'@type': 'Organization', 'name': LEGAL, 'url': SITE}, 'publisher': {'@id': SITE + '#business'},
            'image': (IMG_ABS or SITE + 'img/') + '%s.webp' % a['photo'], 'mainEntityOfPage': SITE + path, 'inLanguage': 'en-SG'}


def article_card(a):
    return '<a class="acard" href="articles/%s/">%s<span><b>%s</b>%s</span></a>' % (a['slug'], img(a['photo']), E(a['h1']), E(a['desc']))


# ----------------------------------------------------------------------------------------------
# Home and hub pages
# ----------------------------------------------------------------------------------------------
FAQ_HOME = [
    ('What does Star Performance Motor do?', 'We are a used car dealer in Yishun, Singapore. We sell quality pre-owned cars, buy cars outright or as trade-ins, consign cars for owners, find specific cars on request, and arrange exports for cars near the end of their COE.'),
    ('Where is your showroom?', '9 Yishun Industrial Street 1, #01-82 North Spring Bizhub, Singapore 768163. Walk-ins are welcome, or WhatsApp +65 9742 7491 to book a time.'),
    ('What are your opening hours?', 'We are open %s at 9 Yishun Industrial Street 1, #01-82 North Spring Bizhub. Walk-ins are welcome, and you are also welcome to WhatsApp +65 9742 7491 to book a time.' % HOURS),
    ('Where can I see the cars you have for sale?', 'Our current cars, with prices and photos, are listed on our sgcarmart dealer page. You can also WhatsApp us for what is in stock today.'),
    ('Are your customers happy?', '%s recommend us on Facebook from %s reviews, as at %s.' % (REC, REC_N, REC_DATE)),
    ('Can I wrap or protect my car after I buy it?', 'Yes. Our sister business Wrapstar Autostyle shares our unit at North Spring Bizhub and does colour change wraps, colour PPF, clear paint protection film, window film and dechrome. See wrapstarautostyle.com for its colours and past works.'),
]


ARROWS = ('<div class="rail-nav"><button class="rail-btn" type="button" data-dir="-1" aria-label="Scroll left">&#8592;</button>'
          '<button class="rail-btn" type="button" data-dir="1" aria-label="Scroll right">&#8594;</button></div>')


def rail_head(eyebrow, hid, title, sub='', more=''):
    return ('<div class="rail-head"><div><p class="eyebrow">%s</p><h2 id="%s">%s</h2>%s</div><div class="rail-side">%s%s</div></div>'
            % (E(eyebrow), hid, title, '<p>%s</p>' % sub if sub else '', more, ARROWS))


def catalog_cards():
    """Cars for sale rail. Real stock first (from STOCK); until Zach sends listings, the first card opens the live
    sgcarmart list and the rest are clearly badged as cars already delivered or sold, never shown as available."""
    out = []
    for p, n, y, pr, u in STOCK:
        out.append('<a class="ccard" href="%s" target="_blank" rel="noopener"><figure>%s<span class="badge badge-sale">For sale</span></figure>'
                   '<div class="ccard-t"><b>%s</b><span>%s</span><strong>%s</strong><em>View on sgcarmart →</em></div></a>' % (u, img(p), E(n), E(y), E(pr)))
    out.append('<a class="ccard ccard-live" href="%s" target="_blank" rel="noopener"><div class="live-in"><span class="dot"></span><small>Live stock</small>'
               '<b>Every car in our showroom today</b><span>Prices, mileage, COE and photos on our sgcarmart dealer page, updated as cars sell.</span>'
               '<em>Browse all cars →</em></div></a>' % SGCM)
    for s in STORIES:
        out.append('<a class="ccard" href="sold-cars/#%s"><figure>%s<span class="badge">Delivered %s</span></figure><div class="ccard-t"><b>%s</b><span>%s</span><em>Read the story →</em></div></a>'
                   % (s['slug'], img(s['photo']), E(s['date'].split(' ', 1)[1]), E(s['car']), E(s['tag'])))
    for p, n, note in SOLD:
        out.append('<a class="ccard" href="sold-cars/"><figure>%s<span class="badge">Sold</span></figure><div class="ccard-t"><b>%s</b><span>%s</span><em>See sold cars →</em></div></a>'
                   % (img(p), E(n), E(note)))
    return '<div class="rail rail-cars">%s</div>' % ''.join(out)


def svc_cards():
    return '<div class="svc-grid">%s</div>' % ''.join(
        '<a class="svc" href="services/%s/"><figure>%s</figure><div class="svc-t"><small>0%d</small><b>%s</b><span>%s</span><em>More details →</em></div></a>'
        % (s['slug'], img(s['photo']), i + 1, E(s['short']), E(s['gist'])) for i, s in enumerate(SERVICES))


def mag_story(s):
    return ('<a class="mag" href="sold-cars/#%s"><figure>%s</figure><div class="mag-t"><small>%s · %s</small><b>%s</b><span>%s</span></div></a>'
            % (s['slug'], img(s['photo']), E(s['tag']), E(s['date']), E(s['car']), E(s['gist'])))


def mag_review(r):
    who, staff, when, text = r
    short = text if len(text) < 190 else text[:text.rfind(' ', 0, 185)] + '…'
    return ('<figure class="rev"><span class="rev-q" aria-hidden="true">&#8220;</span><blockquote>%s</blockquote>'
            '<figcaption><b>%s</b><span>Dealt with %s · Facebook, %s</span></figcaption></figure>' % (E(short), E(who), E(staff), E(when)))


def mag_article(a):
    return ('<a class="mag" href="articles/%s/"><figure>%s</figure><div class="mag-t"><small>Guide</small><b>%s</b><em>Read the guide →</em></div></a>'
            % (a['slug'], img(a['photo']), E(a['h1'])))


def home_body():
    return f'''<section class="hero"><div class="wrap hero-grid">
<div class="hero-in">
<p class="hero-kicker">Used car dealer · Yishun, Singapore</p>
<h1>Quality used cars,<br><span>honestly sold.</span></h1>
<p class="lede">Star Performance Motor is a used car dealer in Yishun: buy, sell, trade in, consign, source or export your car with one team at North Spring Bizhub. Test drive, inspect at your own workshop, then decide.</p>
<div class="cta-row"><a class="btn btn-gold" href="#cars">Browse cars for sale</a>{wa_btn('WhatsApp +65 %s' % WA_SHOW)}</div>
<ul class="hero-proof"><li><b>{REC}</b> recommend us on Facebook</li><li><b>{REC_N}</b> reviews</li><li><b>5.0</b> on Google (110)</li><li>Open <b>10am to 8pm</b> daily</li></ul>
</div>
<figure class="hero-bg">{img('showroom', eager=True)}</figure>
</div></section>
<section class="sec" id="cars" aria-labelledby="h-cars"><div class="wrap">
{rail_head('Cars for sale', 'h-cars', 'Find your next car', 'Swipe through our showroom. Live prices for every car are on sgcarmart.', sgcm_btn('All cars on sgcarmart', 'btn btn-ghost btn-sm'))}
{catalog_cards()}
</div></section>
<section class="sec sec-alt" aria-labelledby="h-s"><div class="wrap">
<div class="sec-head"><p class="eyebrow">What we do</p><h2 id="h-s">Every way to move your car</h2></div>
{svc_cards()}
</div></section>
<section class="sec" aria-labelledby="h-h"><div class="wrap">
{rail_head('Handovers', 'h-h', 'Recent handovers', 'Real customers, from our Facebook page, August 2026.', '<a class="btn btn-ghost btn-sm" href="sold-cars/">All sold cars</a>')}
<div class="rail rail-mag">{''.join(mag_story(s) for s in STORIES)}</div>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-r"><div class="wrap">
{rail_head('Reviews', 'h-r', '%s recommend us' % REC, '%s Facebook reviews, as at %s. Quoted word for word.' % (REC_N, REC_DATE), '<a class="btn btn-ghost btn-sm" href="reviews/">All reviews</a>')}
<div class="rail rail-rev revs">{''.join(mag_review(r) for r in REVIEWS[:6])}</div>
</div></section>
<section class="sec" aria-labelledby="h-art"><div class="wrap">
{rail_head('Guides', 'h-art', 'Buying or selling soon?', 'Plain-English guides for Singapore car owners.', '<a class="btn btn-ghost btn-sm" href="articles/">All guides</a>')}
<div class="rail rail-mag">{''.join(mag_article(a) for a in ARTICLES)}</div>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-faq"><div class="wrap narrow">
<div class="sec-head"><p class="eyebrow">FAQ</p><h2 id="h-faq">Quick answers</h2></div>
{faq_html(FAQ_HOME)}
</div></section>'''



def services_index():
    return '<section class="sec"><div class="wrap"><div class="scards">%s</div></div></section>' % (''.join(
        tile('services/%s/' % s['slug'], s['photo'], s['short'], s['gist']) for s in SERVICES) + tile('cars-for-sale/', 'showroom', 'Cars for sale', 'Our live showroom stock, with prices and photos on sgcarmart.', 'See the cars →'))


def cars_body():
    return f'''<section class="sec"><div class="wrap">{stock_block()}</div></section>
<section class="sec sec-alt"><div class="wrap split2">
<div><p class="eyebrow">Before you buy</p><h2>How buying from us works</h2>
{steps(SVC['buy-a-used-car']['body'][0][2])}
<a class="btn btn-gold" href="services/buy-a-used-car/">Buying in detail</a></div>
<div><p class="eyebrow">Recently sold</p><h2>Cars our customers drove home</h2><div class="stories" style="grid-template-columns:1fr">{''.join(story_html(x) for x in STORIES[:2])}</div></div>
</div></section>
<section class="sec"><div class="wrap narrow"><div class="sec-head"><h2>Questions about our cars</h2></div>{faq_html(CARS_FAQ)}</div></section>'''


CARS_FAQ = [
    ('Where are your cars listed?', 'Every car we have for sale is on our sgcarmart dealer page with price, mileage, COE and photos.'),
    ('Can I view a car before buying?', 'Yes. View and test drive it at our Yishun showroom, and book a pre-purchase inspection at your own workshop before you commit.'),
    ('Can you find a car you do not have?', 'Yes. Tell us the model and budget on WhatsApp and we will search our network.'),
]


def sold_body():
    return f'''<section class="sec"><div class="wrap">
<div class="sec-head"><p class="eyebrow">August 2026</p><h2>Recent handovers</h2></div>
<div class="stories">{''.join(story_html(x, link=False) for x in STORIES)}</div>
</div></section>
<section class="sec sec-alt"><div class="wrap">
<div class="sec-head"><p class="eyebrow">From our Instagram, March 2022</p><h2>Sold for our customers</h2><p>Six owners\' cars, with the viewings it took and the days to handover as we posted them at the time.</p></div>
{sold_cards()}
<p style="margin-top:20px"><a class="btn btn-ghost" href="{IG}" target="_blank" rel="noopener">Follow us on Instagram</a> <a class="btn btn-ghost" href="{FB}" target="_blank" rel="noopener">Facebook</a></p>
</div></section>'''


def reviews_body():
    return f'''<section class="sec"><div class="wrap">
<div class="proof" style="color:var(--ink)"><div><b>{REC}</b><span style="color:var(--muted)">recommend us on Facebook</span></div><div><b>{REC_N}</b><span style="color:var(--muted)">Facebook reviews, as at {REC_DATE}</span></div></div>
<p>On Google, our profile shows {GOOGLE_RATING} (as at {REC_DATE}). Below are excerpts from recent Facebook reviews, quoted word for word with the reviewer\'s first name and initial. <a href="{FB_REVIEWS}" target="_blank" rel="noopener">Read every review on Facebook</a>.</p>
<div class="revgrid">{''.join(rev_html(r) for r in REVIEWS)}</div>
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Recent handovers</h2></div><div class="stories">{''.join(story_html(x) for x in STORIES)}</div></div></section>'''


def about_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<p class="answer">{LEGAL} (UEN {UEN}) is a used car dealer at North Spring Bizhub in Yishun, Singapore, incorporated on 9 November 2022. We buy, sell, consign, source and export cars, and our customers recommend us {REC} on Facebook across {REC_N} reviews.</p>
<figure class="lead-fig">{img('showroom', eager=True)}</figure>
<h2>Our values</h2>
<div class="vals"><div><b>Sincere</b>Honesty builds lasting relationships.</div><div><b>Passionate</b>We love what we do, and it shows.</div><div><b>Mindful</b>We listen, care and put ourselves in your shoes.</div></div>
<h2>The people you will deal with</h2>
<p>Customers name Zach, Celsius and Wei Kiat in their reviews. You deal with the same person from first message to handover, and after it.</p>
<h2>Our sister business</h2>
<p><a href="https://wrapstarautostyle.com/" target="_blank" rel="noopener">Wrapstar Autostyle</a> shares our unit at North Spring Bizhub. It does colour change wraps, colour PPF, clear paint protection film, window film and dechrome, so you can buy a car here and give it a new look or protection next door.</p>
<h2>Company details</h2>
<table class="cmp"><tbody>
<tr><td>Legal name</td><td>{LEGAL}</td></tr><tr><td>UEN</td><td>{UEN}</td></tr><tr><td>Incorporated</td><td>9 November 2022</td></tr>
<tr><td>Showroom</td><td>{', '.join(ADDR)}</td></tr><tr><td>Opening hours</td><td>{HOURS}</td></tr><tr><td>Phone and WhatsApp</td><td>+65 {WA_SHOW}</td></tr>
<tr><td>Live stock</td><td><a href="{SGCM}" target="_blank" rel="noopener">sgcarmart dealer page</a></td></tr>
<tr><td>Social</td><td><a href="{GBP}" target="_blank" rel="noopener">Google</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></td></tr>
</tbody></table>
</article>
<aside class="side"><div class="card sticky"><h2>Visit us</h2><p>{'<br>'.join(ADDR)}</p>{wa_btn('WhatsApp us')}<a class="btn btn-ghost" href="{MAP}" target="_blank" rel="noopener">Open in Google Maps</a></div></aside>
</div></section>'''


def contact_body():
    return f'''<section class="sec"><div class="wrap split">
<div>
<h2>WhatsApp is fastest</h2>
<p>Message +65 {WA_SHOW} with what you need. For a selling, consignment or export offer, include the model, registration date, mileage, COE expiry and a few photos.</p>
<form class="enquiry card" id="enquiry" data-wa="{WA_NUM}" action="#">
<label>I would like to<select name="o"><option>buy a car</option><option>sell or trade in my car</option><option>consign my car</option><option>export my car</option><option>find a specific car</option></select></label>
<label>Car (model and year)<input name="c" autocomplete="off"></label>
<label>Your name<input name="n" autocomplete="name"></label>
<label>Notes<textarea name="x" rows="3"></textarea></label>
<button class="btn btn-wa" type="submit">{WA_SVG}<span>Send on WhatsApp</span></button>
<p class="small">This opens WhatsApp with your message ready to send. Nothing is stored on this website.</p>
</form>
</div>
<aside><div class="card"><h2>Showroom</h2><p>{LEGAL}<br>{'<br>'.join(ADDR)}</p>
<p><b>Open {HOURS}</b></p>
<p><a href="tel:{TEL}">Call +65 {WA_SHOW}</a></p>
<p><a href="{GBP}" target="_blank" rel="noopener">Google</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{SGCM}" target="_blank" rel="noopener">sgcarmart</a></p>
<div class="mapbox"><iframe title="Map to Star Performance Motor" src="{MAP_EMBED}" width="100%" height="280" style="border:0;border-radius:12px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></aside>
</div></section>'''


def privacy_body():
    return f'''<section class="sec"><div class="wrap narrow prose">
<p>{LEGAL} (UEN {UEN}) respects your personal data under Singapore\'s Personal Data Protection Act 2012 (PDPA).</p>
<h2>What we collect</h2><p>This website does not use forms that store data. When you WhatsApp, call or message us, we receive the details you choose to send, such as your name, number and car details.</p>
<h2>How we use it</h2><p>Only to answer your enquiry and to complete a purchase, sale, consignment or export you ask for, including the paperwork required by LTA, banks and insurers.</p>
<h2>Sharing</h2><p>We share personal data only with the parties needed to complete your transaction, or where the law requires it.</p>
<h2>Your rights</h2><p>You can ask to see, correct or withdraw consent for your personal data. WhatsApp +65 {WA_SHOW} or write to us at our showroom address.</p>
<p class="small">Last updated {UPDATED}.</p></div></section>'''


def business_schema():
    return {'@type': ['AutoDealer', 'LocalBusiness', 'Organization'], '@id': SITE + '#business', 'name': NAME, 'legalName': LEGAL, 'alternateName': ['Star Performance', 'Star Performance Motor', 'Star Performance Motor Pte Ltd'],
            'slogan': 'Sincere. Passionate. Mindful.', 'url': SITE, 'telephone': TEL, 'foundingDate': FOUNDED,
            'image': [(IMG_ABS or SITE + 'img/') + 'showroom.webp'], 'logo': (IMG_ABS or SITE) + 'icon-512.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': '%s %s %s' % (STREET, UNIT, BUILDING), 'addressLocality': 'Singapore', 'postalCode': POSTAL, 'addressCountry': 'SG'},
            'hasMap': MAP, 'sameAs': [GBP, FB, IG, SGCM], 'areaServed': {'@type': 'Country', 'name': 'Singapore'},
            'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '10:00', 'closes': '20:00'}],
            'currenciesAccepted': 'SGD',
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'UEN', 'value': UEN},
            'knowsAbout': ['used cars Singapore', 'car trade-in', 'car consignment', 'car export', 'car sourcing', 'pre-purchase inspection'],
            'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['short'], 'url': SITE + 'services/%s/' % s['slug']}} for s in SERVICES]}


# ----------------------------------------------------------------------------------------------
# Register pages
# ----------------------------------------------------------------------------------------------
page('', 'Star Performance Motor | Used Car Dealer in Yishun',
     'Star Performance Motor: buy, sell, trade in, consign or export your car in Yishun. 100% recommend on Facebook (391 reviews). WhatsApp 9742 7491.',
     NAME, home_body(), hero=False, schema=[faq_schema(FAQ_HOME)], photo='showroom')
page('cars-for-sale/', 'Used Cars for Sale in Yishun | Star Performance Motor',
     'See the used cars for sale at Star Performance Motor, North Spring Bizhub, Yishun. Live prices on sgcarmart. View, test drive and inspect before you buy.',
     'Cars for sale', cars_body(), crumbs=[('cars-for-sale/', 'Cars for sale')],
     lede='Our showroom stock changes every week. The live list, with prices and photos, is on our sgcarmart dealer page.', schema=[faq_schema(CARS_FAQ)])
page('services/', 'Car Services: Buy, Sell, Consign, Export | Star Performance',
     'Buy a used car, sell or trade in, consign, export near COE expiry, or have us find a specific car. Star Performance Motor, Yishun, Singapore.',
     'Our services', services_index(), crumbs=[('services/', 'Services')],
     lede='Five ways we help, all with the same transparent approach our customers write about.')
for s in SERVICES:
    path = 'services/%s/' % s['slug']
    page(path, s['title'], s['desc'], s['h1'], service_body(s), crumbs=[('services/', 'Services'), (path, s['short'])], lede=s['lede'], photo=s['photo'],
         schema=[{'@type': 'Service', 'name': s['h1'], 'serviceType': s['short'], 'description': s['desc'], 'url': SITE + path, 'provider': {'@id': SITE + '#business'}, 'areaServed': 'Singapore'}, faq_schema(s['faqs'])])
page('sold-cars/', 'Sold Cars and Happy Handovers | Star Performance Motor',
     'Recent handovers at Star Performance Motor: BMW 520i M Sport, Toyota Vellfire, VW Passat, VW Tiguan R-Line, and cars sold for owners.',
     'Sold cars and handovers', sold_body(), crumbs=[('sold-cars/', 'Sold cars')],
     lede='Real customers, real cars. Every story here comes from our own Facebook and Instagram posts.')
page('reviews/', 'Reviews: 100% Recommend on Facebook | Star Performance Motor',
     'Read what customers say about Star Performance Motor: 100% recommend on Facebook from 391 reviews. Word-for-word excerpts about Zach, Celsius and Wei Kiat.',
     'Customer reviews', reviews_body(), crumbs=[('reviews/', 'Reviews')],
     lede='%s recommend us on Facebook from %s reviews (as at %s).' % (REC, REC_N, REC_DATE))
page('articles/', 'Used Car Guides for Singapore | Star Performance',
     'Plain guides for Singapore car owners: pre-purchase inspections, trade-in vs consignment, COE expiry options, first-car checklist, depreciation.',
     'Guides', '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(article_card(a) for a in ARTICLES),
     crumbs=[('articles/', 'Guides')], lede='Straight answers for buying and selling a used car in Singapore.')
# ---- 2 Nov 2026 SEO pass: hub intros + FAQs (facts from this site only) ----
SERVICES_FAQ = [
    ('Which services does Star Performance Motor offer?', 'Five: buying a used car, selling or trading in your car, consignment, export for cars near the end of their COE, and finding a specific car. We are at 9 Yishun Industrial Street 1, #01-82 North Spring Bizhub, Singapore 768163.'),
    ('Can I trade in my car when I buy another one?', 'Yes. We make an offer for your car outright or as a trade-in on your next one. WhatsApp us the car you have and the car you want, and we reply with options and an honest view.'),
    ('How do I get started?', 'WhatsApp +65 %s or visit the showroom. We are open %s.' % (WA_SHOW, HOURS)),
]
ARTICLES_FAQ = [
    ('What do the Star Performance Motor guides cover?', 'Plain answers for buying and selling a used car in Singapore: pre-purchase inspections, trade-in versus consignment, COE expiry and export, the PARF rebate, car loans, test drives and what to do after you buy.'),
    ('Where do the rules and figures in the guides come from?', 'Where a guide quotes a rule, it links to the official LTA or MAS page. Check that page for the latest figures before you decide, because rules can change.'),
    ('Can I ask about a car or a guide?', 'Yes. WhatsApp +65 %s and we will reply. We are open %s.' % (WA_SHOW, HOURS)),
]
SERVICES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Used car services in Yishun</h2>'
    '<p>Star Performance Motor Pte. Ltd. is a used car dealer at North Spring Bizhub, Yishun. Whether you want to buy, sell, trade in or export a car, the approach is the same: we tell you what we see, in plain words, and our customers write about that on Facebook (%s recommend us, from %s reviews, as at %s).</p>'
    '<p>Buyers can see the cars in our showroom, take a test drive and book a pre-purchase inspection at their own workshop. Owners can sell outright, trade in against their next car, or consign the car and let us market it and handle viewings and paperwork. If your car is near the end of its COE we look for an export offer, and if you want a particular model, tell us the model and budget and we search our network for a well-kept unit.</p>'
    '<p>Pick a service below to see how it works, or WhatsApp us on +65 %s.</p></div></section>') % (REC, REC_N, REC_DATE, WA_SHOW)
ARTICLES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Used car guides for Singapore</h2>'
    '<p>These guides come from the questions buyers and sellers ask us at the showroom in Yishun. They cover what to check before you buy, how a pre-purchase inspection works, how trade-in, consignment and direct sale compare, and what to do when a car is near the end of its COE.</p>'
    '<p>You will also find plain explanations of the COE, the PARF rebate, car loans for used cars and what to do after you buy. Each guide ends with questions and answers, and links to the official LTA and MAS pages where a rule is quoted. If a guide does not answer your case, WhatsApp us on +65 %s.</p></div></section>') % WA_SHOW
def _hub(path, intro, faqs, h2):
    p = PAGES[path]
    p['body'] = intro + p['body'] + '<section class="sec"><div class="wrap narrow"><div class="sec-head"><h2>%s</h2></div>%s</div></section>' % (h2, faq_html(faqs))
    p['schema'] = list(p['schema']) + [faq_schema(faqs)]
_hub('services/', SERVICES_INTRO, SERVICES_FAQ, 'Questions about our services')
_hub('articles/', ARTICLES_INTRO, ARTICLES_FAQ, 'Questions about our guides')

for a in ARTICLES:
    path = 'articles/%s/' % a['slug']
    page(path, a['title'], a['desc'], a['h1'], article_body(a), crumbs=[('articles/', 'Guides'), (path, a['h1'])], photo=a['photo'],
         schema=[article_schema(a, path), faq_schema(a['faqs'])])
page('about/', 'About Star Performance Motor Pte. Ltd. | Yishun Car Dealer',
     'Star Performance Motor Pte. Ltd. (UEN 202223232K), used car dealer at North Spring Bizhub, Yishun since 2022. Sincere, passionate, mindful.',
     'About us', about_body(), crumbs=[('about/', 'About')], lede='A Yishun car dealer built on three words: sincere, passionate, mindful.')
page('contact/', 'Contact Star Performance Motor | WhatsApp 9742 7491',
     'WhatsApp +65 9742 7491 or visit 9 Yishun Industrial Street 1, #01-82 North Spring Bizhub, Singapore 768163. Buy, sell, consign or export.',
     'Contact us', contact_body(), crumbs=[('contact/', 'Contact')], cta=False, lede='WhatsApp +65 %s or visit our showroom in Yishun.' % WA_SHOW)
page('privacy/', 'Privacy Policy | Star Performance Motor', 'How Star Performance Motor Pte. Ltd. handles personal data under Singapore\'s PDPA.',
     'Privacy policy', privacy_body(), crumbs=[('privacy/', 'Privacy')], cta=False)


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------
def render(path, p):
    pre = '../' * path.count('/')
    url = SITE + path
    share = (IMG_ABS or SITE + 'img/') + 'share/home.jpg'

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                                 'inLanguage': 'en-SG', 'dateModified': LASTMOD.get(path, UPDATED), 'about': {'@id': SITE + '#business'},
                                 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = '<section class="phero"><div class="wrap">%s<h1>%s</h1>%s</div></section>' % (
            crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = fix(('<section class="sec"><div class="wrap"><div class="band"><div><h2>Buying, selling or upgrading?</h2>'
                    '<p>WhatsApp us the car you want or the car you have. We reply with options and an honest view.</p></div><div class="cta-row">%s%s</div></div></div></section>') % (
            wa_btn('WhatsApp +65 %s' % WA_SHOW), sgcm_btn('Cars for sale', 'btn btn-gold')))
    robots = 'noindex,nofollow' if NOINDEX else 'index,follow,max-image-preview:large'
    title = E(p['title'])
    preload = '<link rel="preload" as="image" href="%s%s%s.webp" fetchpriority="high">' % ('' if IMG_ABS else pre, IMG, p['photo']) if p['photo'] else ''
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
<meta name="theme-color" content="#06070a">
<link rel="canonical" href="{url}">
{preload}
<meta property="og:type" content="{'article' if path.startswith('articles/') and path != 'articles/' else 'website'}">
<meta property="og:site_name" content="{NAME}">
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
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{pre}sp.css?v=6">
<script src="{pre}sp.js?v=7" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>{LEGAL} · {', '.join(ADDR)}</span><span class="strip-r"><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp +65 {WA_SHOW}</a></span></div></div>
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
<p>Sincere. Passionate. Mindful. A used car dealer in Yishun: buy, sell, trade in, consign, source and export. Since 2022.</p></div>
<div><h3>Services</h3><ul>{''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, s['slug'], E(s['short'])) for s in SERVICES)}</ul></div>
<div><h3>Explore</h3><ul><li><a href="{pre}cars-for-sale/">Cars for sale</a></li><li><a href="{pre}sold-cars/">Sold cars</a></li><li><a href="{pre}reviews/">Reviews</a></li><li><a href="{pre}articles/">Guides</a></li><li><a href="{pre}about/">About</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp +65 {WA_SHOW}</a></li>
<li>{'<br>'.join(ADDR)}</li>
<li>Open {HOURS}</li>
<li><a href="{GBP}" target="_blank" rel="noopener">Google</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{SGCM}" target="_blank" rel="noopener">sgcarmart</a></li>
<li><a href="{pre}contact/">Contact</a> · <a href="{pre}privacy/">Privacy</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{LEGAL} · UEN {UEN}</span><span>© 2026 {LEGAL} · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp Star Performance Motor on {WA_SHOW}">{WA_SVG}<span>WhatsApp</span></a><a class="dock-call" href="{pre}cars-for-sale/">Cars for sale</a></div>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', t) for h, t in [('', 'Home')] + NAV)
    p = dict(title='Page not found | Star Performance Motor', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, photo=None)
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, m.group(2) if m.group(2) != './' else ''), out)


HTACCESS = """# Star Performance Motor ({DOMAIN}). Document root for {DOMAIN}; also served as
# pageonesingapore.com/preview/star-performance/ before go-live. Overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.starperformancemotor\\.com$ [NC]
RewriteRule ^ https://starperformancemotor.com%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
# Preview host only: pageonesingapore.com/preview/star-performance/ stays out of Google; the real domain serves the same files without this header.
SetEnvIfNoCase Host ^(www\\.)?pageonesingapore\\.com$ P1_PREVIEW=1
Header set X-Robots-Tag "noindex, nofollow" env=P1_PREVIEW
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


INDEXNOW_KEY = '99381246b278105dbbf132423ac73bbc'


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
        f.write('# Star Performance Motor, used car dealer in Yishun, Singapore\n\n'
                '> %s (UEN %s, incorporated 9 November 2022) is a used car dealer at %s, Singapore %s. '
                'Services: buy a used car, sell or trade in your car, consignment, export of cars near COE expiry, and sourcing of specific models. '
                'Values: Sincere, Passionate, Mindful. Customers recommend it %s on Facebook from %s reviews (as at %s); reviewers name Zach, Celsius and Wei Kiat. '
                'Live stock with prices is on sgcarmart (%s). Buyers can view and test drive at the showroom and book a pre-purchase inspection at their own workshop. '
                'Showroom open %s; Google rating 5.0 from 110 reviews (as at 17 October 2026). WhatsApp or call +65 %s. Facebook %s, Instagram %s. Sister business in the same unit: Wrapstar Autostyle, car wraps and PPF, https://wrapstarautostyle.com/.\n\n## Pages\n'
                % (LEGAL, UEN, ', '.join(ADDR[:1] + [BUILDING]), POSTAL, REC, REC_N, REC_DATE, SGCM, HOURS, WA_SHOW, FB, IG))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': LEGAL, 'short_name': 'Star Performance', 'icons': [{'src': (IMG_ABS or '') + 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': (IMG_ABS or '') + 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
                   'theme_color': '#06070a', 'background_color': '#06070a', 'display': 'browser'}, f)
    with open(os.path.join(HERE, 'htaccess.txt'), 'w') as f:
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()

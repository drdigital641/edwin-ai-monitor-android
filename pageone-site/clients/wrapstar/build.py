"""Wrapstar Autostyle: builds every page into site/ (python3 build.py [outdir]).

Facts used (17 Oct 2026), and where they came from:
- ACRA via companies.sg / companieshouse.sg: WRAPSTAR AUTOSTYLE, sole proprietorship, UEN 53513245W, registered 3 Nov 2025, live,
  at 9 Yishun Industrial Street 1, North Spring Bizhub, Singapore 768163 (primary activity listed as car washing and related services).
- Facebook page facebook.com/wrapstarautostyle (read logged out, 17 Oct 2026): "Our Service: Car Wrap, Car PPF / Color PPF, Dechrome,
  Window Film"; 9 Yishun Industrial Street 1, #01-82, Singapore 768163; mobile and WhatsApp +65 9754 1833; 2.7K followers;
  "100% recommend (24 reviews)". Older reviews on that page were written for Finest Detailing Express (car wash and coating);
  only the April 2026 colour PPF review is quoted.
- Their own posts: Oct 6 2026 Tesla Model 3 satin black colour PPF promo $2,788 nett (7.5mil TPU, heat self-healing, hydrophobic
  topcoat, removable); August 2026 National Day offer for hatchbacks and sedans (LTA compliant tint $388, colour wrap $1,388,
  clear PPF $2,188, colour PPF $2,588); poster "Full car color wrap from $1588 onwards"; opening promotion nano ceramic solar film
  $358 (U.P. $428), 93%-96% IR rejection, free removal of existing film, installation included, sunshade, 7-year warranty; car
  care bundle $628 nett (polish + ceramic coating, LTA compliant window film, free headlight PPF). Posters list 9754 1833 / 9742 7491.
- Photos: their own, from the Facebook page (Nov 2025 onwards), served from jsDelivr (repo site-assets branch, commit da2c02e).
  Colour names describe what the photos show; the exact film names are not known yet, so the site says "seen on our past jobs".
- Window tint rule: MOT parliamentary reply, 7 Apr 2026 (70% front windscreen and front side windows, 25% rear).
  OneMotoring vehicle modification page: tinted films need no LTA approval; tinting or masking of vehicle lamps is not allowed.
- Sister business: Star Performance Motor (same unit, https://starperformancemotor.com).
- Opening hours and Google rating: Google Business Profile screenshot from Edwin, 18 Oct 2026 (Mon-Fri 9am-6pm, Sat 9am-3pm, Sun closed; 4.9 from 123 reviews).
Not claimed anywhere: film brands, warranty on wraps or PPF, durations, "best"/"cheapest".
"""
import html
import json
import os
import re
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'site')

SLUG = 'wrapstar'
DOMAIN = 'wrapstarautostyle.com'  # live since 18 Oct 2026 (Controller switch)
LIVE = True
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
IMG = os.environ.get('WS_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@da2c02e/site-assets/wrapstar/')
UPDATED = '2026-10-18'
V = '3'

NAME = 'Wrapstar Autostyle'
TAGLINE = 'For cars that deserve more'
UEN = '53513245W'
REGISTERED = '2025-11-03'
WA_NUM, WA_SHOW, TEL = '6597541833', '9754 1833', '+6597541833'
WA_MSG = 'Hi Wrapstar Autostyle, I found your website. I would like a quote for '
STREET, UNIT, BUILDING, POSTAL = '9 Yishun Industrial Street 1', '#01-82', 'North Spring Bizhub', '768163'
ADDR = ['9 Yishun Industrial Street 1, #01-82', 'North Spring Bizhub, Singapore 768163']
MAPQ = quote('Wrapstar Autostyle, 9 Yishun Industrial Street 1 #01-82 Singapore 768163')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
FB = 'https://www.facebook.com/wrapstarautostyle'
FB_REVIEWS = 'https://www.facebook.com/wrapstarautostyle/reviews'
IG = 'https://www.instagram.com/wrapstar.autostyle/'
GBP = 'https://www.google.com/search?kgmid=/g/11f03s_v0g'  # Google Business Profile entity (from the client's Google share link)
GEO = (1.438458, 103.843362)  # OneMap, postal 768163, read 18 Oct 2026
SISTER = 'https://starperformancemotor.com/'
HOURS = 'Mon to Fri 9am to 6pm, Sat 9am to 3pm, closed Sun'  # Google Business Profile, 18 Oct 2026
HOURS_SPEC = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '09:00', 'closes': '18:00'},
              {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Saturday', 'opens': '09:00', 'closes': '15:00'}]
GRATING = '4.9 on Google from 123 reviews (checked 18 October 2026)'
REC = '100% recommend on Facebook (24 reviews, checked 17 October 2026)'
MOT = 'https://www.mot.gov.sg/news-resources/newsroom/review-of-requirements-for-window-tints-in-motor-vehicles-while-accounting-for-heat-reduction--visibility-and-road-safety/'
OM_MOD = 'https://www.onemotoring.com.sg/content/onemotoring/home/owning/modification.html'

CONFIRM = [
    'Whether customers need an appointment (hours now from Google: Mon-Fri 9-6, Sat 9-3, Sun closed)',
    'Website WhatsApp number: 9754 1833 (Facebook) is used; posters also show 9742 7491 (Star Performance Motor)',
    'Today\'s "from" prices for colour wrap, colour PPF, clear PPF, window film and dechrome (site shows posted offers with dates)',
    'Film brands you use for vinyl wrap, colour PPF, clear PPF and window film, and the warranty on each',
    'The exact film name and code for each colour on the colour catalogue (now described as "seen on our past jobs")',
    'Which jobs in the photos were vinyl wrap and which were colour PPF (Mazda CX-5 blue, BYD Seal black, white Tesla Model Y)',
    'How long a full wrap or full PPF job takes, and whether you need the car overnight',
    'The Facebook page shows older reviews for Finest Detailing Express: is that the same team? OK to mention it?',
    'Team names to show (the April 2026 review thanks Zach) and the email to publish (Facebook lists finestdetexp@gmail.com)',
    'Domain name for the site, and whether to also offer ceramic coating and motorcycle wraps as services',
]

NAV = [('colours/', 'Colours'), ('past-works/', 'Past works'), ('services/', 'Services'), ('prices/', 'Prices'),
       ('articles/', 'Guides'), ('about/', 'About'), ('contact/', 'Contact')]
E = html.escape

DIMS = json.load(open(os.path.join(HERE, 'dims.json')))
ALT = {
    'tesla-model-3-satin-black-rear': 'Tesla Model 3 in satin black colour PPF inside the Wrapstar Autostyle studio in Yishun',
    'tesla-model-3-satin-black-side': 'Side view of a Tesla Model 3 finished in satin black',
    'tesla-model-3-satin-black-front': 'Front of a satin black Tesla Model 3 under the studio hex lights',
    'tesla-model-3-satin-black-angle': 'Satin black Tesla Model 3, front three-quarter view',
    'byd-sealion-7-matte-green-front': 'BYD Sealion 7 in matte green, front view',
    'byd-sealion-7-matte-green-detail': 'Close-up of the matte green finish and door handle on a BYD Sealion 7',
    'byd-sealion-7-matte-green-side': 'BYD Sealion 7 in matte green, side view',
    'byd-sealion-7-matte-green-carpark': 'Matte green BYD Sealion 7 parked outdoors',
    'tesla-white-studio': 'White Tesla under the hexagon lights in the Wrapstar Autostyle studio',
    'tesla-model-y-ice-grey-front': 'Tesla Model Y in ice grey, front view',
    'tesla-model-y-ice-grey-angle': 'Ice grey Tesla Model Y, front three-quarter view',
    'tesla-model-y-ice-grey-side': 'Ice grey Tesla Model Y, side view',
    'tesla-model-y-ice-grey-rear': 'Ice grey Tesla Model Y, rear view',
    'mazda-cx-5-deep-blue-rear': 'Deep blue Mazda CX-5, rear view in the studio',
    'mazda-cx-5-deep-blue-front': 'Deep blue Mazda CX-5 under the hex lights',
    'mazda-cx-5-deep-blue-studio': 'Deep blue Mazda CX-5, front three-quarter view',
    'mercedes-a-class-baby-blue-rear': 'Mercedes-Benz A-Class in baby blue, rear view',
    'mercedes-a-class-baby-blue-front': 'Baby blue Mercedes-Benz A-Class, front view',
    'mercedes-a-class-baby-blue-detail': 'Close-up of the baby blue bonnet and star on a Mercedes-Benz A-Class',
    'mercedes-a-class-baby-blue-angle': 'Baby blue Mercedes-Benz A-Class, side view',
    'mercedes-c-class-baby-blue-studio': 'Mercedes-Benz C-Class coupe being wrapped baby blue in the Wrapstar Autostyle studio',
    'mercedes-a-class-pastel-pink': 'Mercedes-Benz A-Class in pastel pink',
    'tesla-model-y-yellow-front': 'Bright yellow Tesla Model Y, front three-quarter view',
    'tesla-model-y-yellow-angle': 'Bright yellow Tesla Model Y, side view',
    'tesla-model-y-yellow-rear': 'Bright yellow Tesla Model Y, rear view',
    'tesla-model-y-yellow-head-on': 'Bright yellow Tesla Model Y, head-on view',
    'bmw-m4-stealth-grey-front': 'BMW M4 in stealth matte grey with carbon parts',
    'bmw-m4-stealth-grey-studio': 'Stealth matte grey BMW M4 under the studio hex lights',
    'mercedes-cla-stealth-grey-rear': 'Mercedes-Benz CLA in stealth matte grey, rear view',
    'mercedes-cla-stealth-grey-wing': 'Stealth matte grey Mercedes-Benz CLA with rear wing',
    'byd-seal-gloss-black-front': 'BYD Seal in gloss black, front view',
    'byd-seal-gloss-black-side': 'Gloss black BYD Seal, side view',
    'byd-seal-gloss-black-angle': 'Gloss black BYD Seal, rear three-quarter view',
    'tesla-model-y-white-front': 'White Tesla Model Y, front three-quarter view',
    'tesla-model-y-white-angle': 'White Tesla Model Y, side view',
    'studio-white-tesla': 'White Tesla Model Y in the Wrapstar Autostyle studio',
    'installer-ppf-bonnet': 'Wrapstar Autostyle installer trimming film on a bonnet edge',
    'installer-window-film': 'Wrapstar Autostyle installer fitting window film on a rear windscreen',
    'installer-window-film-2': 'Installer squeegeeing window film inside the rear glass',
    'ppf-headlamp-install': 'Clear paint protection film being fitted over a headlamp',
    'window-film-mercedes': 'Window film fitted on a black Mercedes-Benz',
    'window-film-mercedes-door': 'Tinted side windows on a black car at the Star Performance Motor showroom',
    'window-film-detail': 'Close-up of tinted glass on a satin black car',
}


def img(name, cls='', eager=False, sizes=None):
    w, h = DIMS[name]
    return '<img src="%s%s.webp" alt="%s" width="%d" height="%d"%s%s>' % (
        IMG, name, E(ALT.get(name, '')), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', ' class="%s"' % cls if cls else '')


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')


def wa_url(topic='my car.'):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp for a quote', topic='my car.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic)), WA_SVG, E(label))


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def steps(items):
    return '<ol class="numbered">%s</ol>' % ''.join('<li><b>%s.</b> %s</li>' % (E(a), E(b)) for a, b in items)


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, preload=None):
    assert len(title) <= 62, (path, len(title), title)
    assert len(desc) <= 160, (path, len(desc))
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [], hero=hero, cta=cta, preload=preload)


# ------------------------------------------------------------------------------------------------
# Colour catalogue: colours seen on Wrapstar's own jobs (names describe the photos; film codes to confirm)
# ------------------------------------------------------------------------------------------------
COLOURS = [
    dict(k='satin-black', name='Satin Black', c='#202124', t='#f4f4f4', fin='satin', car='Tesla Model 3', svc='colour-ppf',
         note='Our October 2026 promo colour: satin black colour PPF on the Tesla Model 3. A low sheen that shows every body line without glare.',
         pics=['tesla-model-3-satin-black-rear', 'tesla-model-3-satin-black-front', 'tesla-model-3-satin-black-side', 'tesla-model-3-satin-black-angle', 'window-film-detail']),
    dict(k='matte-green', name='Matte Green', c='#56624f', t='#f4f4f0', fin='matte', car='BYD Sealion 7', svc='colour-change-wrap',
         note='A flat, earthy green that turns a common EV into one people stop to look at.',
         pics=['byd-sealion-7-matte-green-front', 'byd-sealion-7-matte-green-side', 'byd-sealion-7-matte-green-detail', 'byd-sealion-7-matte-green-carpark']),
    dict(k='stealth-grey', name='Stealth Grey', c='#5a5d61', t='#f5f5f5', fin='matte', car='BMW M4 and Mercedes-Benz CLA', svc='colour-change-wrap',
         note='Flat dark grey with no shine. It suits aggressive cars with carbon parts and big wings.',
         pics=['bmw-m4-stealth-grey-studio', 'bmw-m4-stealth-grey-front', 'mercedes-cla-stealth-grey-rear', 'mercedes-cla-stealth-grey-wing']),
    dict(k='ice-grey', name='Ice Grey', c='#cfd8dc', t='#121416', fin='gloss', car='Tesla Model Y', svc='colour-change-wrap',
         note='A pale grey with a cool blue hint. Clean and modern, and it hides dust better than white.',
         pics=['tesla-model-y-ice-grey-angle', 'tesla-model-y-ice-grey-front', 'tesla-model-y-ice-grey-side', 'tesla-model-y-ice-grey-rear']),
    dict(k='baby-blue', name='Baby Blue', c='#8db7dc', t='#0d1620', fin='gloss', car='Mercedes-Benz A-Class and C-Class', svc='colour-change-wrap',
         note='A soft gloss blue that looks bright in Singapore sun and calm in the shade.',
         pics=['mercedes-a-class-baby-blue-front', 'mercedes-a-class-baby-blue-angle', 'mercedes-a-class-baby-blue-rear', 'mercedes-a-class-baby-blue-detail', 'mercedes-c-class-baby-blue-studio']),
    dict(k='bright-yellow', name='Bright Yellow', c='#f4b80b', t='#111', fin='gloss', car='Tesla Model Y', svc='colour-change-wrap',
         note='Loud on purpose. Bright yellow with gloss black trim makes a family SUV look like a sports car.',
         pics=['tesla-model-y-yellow-front', 'tesla-model-y-yellow-head-on', 'tesla-model-y-yellow-angle', 'tesla-model-y-yellow-rear']),
    dict(k='pastel-pink', name='Pastel Pink', c='#ecb8c2', t='#22161a', fin='gloss', car='Mercedes-Benz A-Class', svc='colour-change-wrap',
         note='A gentle pink gloss for owners who want a car that is unmistakably theirs.',
         pics=['mercedes-a-class-pastel-pink']),
    dict(k='deep-blue', name='Deep Blue', c='#1d2c7c', t='#f2f4ff', fin='gloss', car='Mazda CX-5', svc='paint-protection-film',
         note='A rich, glossy blue that looks almost black at night.',
         pics=['mazda-cx-5-deep-blue-studio', 'mazda-cx-5-deep-blue-front', 'mazda-cx-5-deep-blue-rear']),
    dict(k='gloss-black', name='Gloss Black', c='#0d0d0f', t='#f4f4f4', fin='gloss', car='BYD Seal', svc='paint-protection-film',
         note='Deep, mirror-like black. Protection film keeps that depth free of swirls and chips.',
         pics=['byd-seal-gloss-black-front', 'byd-seal-gloss-black-angle', 'byd-seal-gloss-black-side']),
    dict(k='pure-white', name='Pure White', c='#eef0f0', t='#111', fin='gloss', car='Tesla Model Y', svc='paint-protection-film',
         note='Crisp white with gloss black accents, the cleanest look an EV can have.',
         pics=['tesla-model-y-white-front', 'tesla-model-y-white-angle', 'studio-white-tesla']),
]
CBY = {c['k']: c for c in COLOURS}


def ccard(c, pre=''):
    return ('<a class="ccard %s" href="colours/#%s" style="--c:%s;--t:%s">'
            '<span class="ph">%s</span><span class="sw"><i class="chip"></i><b>%s</b><small>%s finish · seen on our %s</small></span></a>') % (
        c['fin'], c['k'], c['c'], c['t'], img(c['pics'][0]), E(c['name']), c['fin'].capitalize(), E(c['car']))


def colour_rail():
    return '<div class="glide" data-speed="0.045" aria-label="Colour catalogue">%s</div>' % ''.join(ccard(c) for c in COLOURS)


# ------------------------------------------------------------------------------------------------
# Services
# ------------------------------------------------------------------------------------------------
REVIEW = ('Tan Shi Xian', 'April 2026', 'Very very satisfied with the quality and finishing of the ppf installed for my car. Was quoted a little cheaper than what was offered elsewhere for coloured ppf.')

SERVICES = [
    dict(slug='colour-change-wrap', short='Colour change wrap', photo='mercedes-c-class-baby-blue-studio',
         title='Car Colour Change Wrap in Singapore | Wrapstar Autostyle',
         desc='Full car colour change wraps in Yishun: gloss, satin and matte colours, removable and paint-safe. See our past jobs and WhatsApp for a quote.',
         h1='Car colour change wrap',
         gist='A whole new colour without a respray. Gloss, satin or matte vinyl that comes off when you want it to.',
         lede='A full vinyl wrap changes your car\'s colour in days, not weeks, and the factory paint stays underneath, protected and untouched.',
         answer='A colour change wrap is a thin vinyl film laid over every painted panel of your car. It gives a new colour and finish, guards the paint from light scratches and fading, and can be removed later without a respray.',
         points=[('New colour, original paint kept.', 'The factory paint stays under the film, which helps when you sell.'),
                 ('Any finish.', 'Gloss, satin and matte, from quiet greys to bright yellow.'),
                 ('Easier upkeep.', 'Wrap film shrugs off light marks and bird droppings wipe away.'),
                 ('Reversible.', 'Bored of the colour later? It can be peeled off and changed.')],
         offers=[('From $1,588', 'full car colour wrap (our posted price)'),
                 ('$1,388', 'colour wrap for hatchbacks and sedans, our National Day offer in August 2026 (SUVs and MPVs by quote)')],
         colours=['matte-green', 'stealth-grey', 'ice-grey', 'baby-blue', 'bright-yellow', 'pastel-pink'],
         faq=[('How much does a full car wrap cost in Singapore?', 'Our posted price for a full car colour wrap starts from $1,588. The final price depends on the size of the car, the film and how much of the door shuts you want covered. WhatsApp a photo of your car for an exact quote.'),
              ('Will a wrap damage my car paint?', 'A good film on healthy factory paint comes off cleanly. Panels that were badly resprayed can lift paint when film is removed, so we check the paint before we start and tell you if there is a risk.'),
              ('Do I need to tell LTA if I wrap my car?', 'Rules on colour changes are set by LTA. Check the current requirements on OneMotoring or with LTA before your job, and ask us what other owners have done.'),
              ('Can I wrap a leased or company car?', 'Yes, many owners wrap cars they plan to return or resell, because the film can be removed and the original colour is still there underneath.')]),
    dict(slug='colour-ppf', short='Colour PPF', photo='tesla-model-3-satin-black-front',
         title='Colour PPF in Singapore: Satin, Matte & Gloss | Wrapstar',
         desc='Colour PPF in Singapore changes your car colour and takes stone chips for your paint. Satin, matte and gloss, fitted at our Yishun studio. WhatsApp for a quote.',
         h1='Colour PPF: change the colour and armour the paint',
         gist='Thick TPU film in colour. You get the new look of a wrap plus real stone-chip protection.',
         lede='Colour PPF is paint protection film with the colour built in. It changes the look like a wrap, but it is thicker and tougher, so it takes stone chips, light scratches and road rash for your paint.',
         answer='Colour PPF (paint protection film) is a thermoplastic polyurethane film that is coloured. The film we posted for the Tesla Model 3 is 7.5mil TPU: it absorbs stone chips, light swirls heal under hot water or afternoon sun, and it can be removed later, leaving the factory paint underneath.',
         points=[('Real TPU armour.', '7.5mil thermoplastic polyurethane film that absorbs stone chips, scratches and road rash.'),
                 ('Heat self-healing.', 'Minor swirls and light scratches fade under hot water or Singapore\'s afternoon heat.'),
                 ('Hydrophobic topcoat.', 'Water, bird droppings, grime and tree sap slide off, so washing is quicker.'),
                 ('Resale value kept.', 'Removable later, with the original factory paint preserved underneath.')],
         offers=[('$2,788 nett', 'Tesla Model 3 satin black colour PPF, our October 2026 promo'),
                 ('$2,588', 'colour PPF for hatchbacks and sedans, our National Day offer in August 2026')],
         colours=['satin-black', 'stealth-grey', 'matte-green'],
         faq=[('What is the difference between colour PPF and a vinyl wrap?', 'Both change the colour. Colour PPF is a thicker TPU film that also absorbs stone chips and heals light swirls in heat; vinyl is thinner and costs less, but protects less. Our guide compares them side by side.'),
              ('How much is colour PPF for a Tesla Model 3?', 'Our October 2026 promo for satin black colour PPF on a Tesla Model 3 is $2,788 nett. Other cars and colours are priced by quote.'),
              ('Does colour PPF really self-heal?', 'Light swirls and fine surface scratches in the top layer fade with heat, such as hot water or a hot afternoon. Deep cuts through the film do not heal.'),
              ('Can colour PPF be removed?', 'Yes. It is designed to come off later and leave the factory paint underneath in the condition it was protected in.')]),
    dict(slug='paint-protection-film', short='Clear PPF', photo='installer-ppf-bonnet',
         title='Clear Paint Protection Film (PPF) in Yishun | Wrapstar',
         desc='Clear PPF keeps your factory colour and guards it from stone chips, swirls and stains. Full car or front only, plus headlight PPF. WhatsApp for a quote.',
         h1='Clear paint protection film (PPF)',
         gist='Invisible armour for the colour you already love. Guards against stone chips, swirls and stains.',
         lede='Love your car\'s colour as it is? Clear PPF is a transparent, tough film that keeps the factory paint looking new by taking the chips and scratches for it.',
         answer='Clear PPF is a transparent polyurethane film fitted over the paint. It keeps your original colour and finish, takes the stone chips and light scratches that would otherwise mark the paint, and makes the car easier to keep clean.',
         points=[('Keeps your colour.', 'Clear film over the factory paint, gloss stays gloss.'),
                 ('Front-end defence.', 'Bonnet, bumper and mirrors take most stone chips on expressways.'),
                 ('Headlights too.', 'Clear film on headlamps helps against chips and haze.'),
                 ('Easier washing.', 'Dirt and droppings come off the film with less effort.')],
         offers=[('$2,188', 'clear PPF for hatchbacks and sedans, our National Day offer in August 2026'),
                 ('Free headlight PPF', 'one pair, included in our $628 nett car care bundle (polish and ceramic coating plus LTA compliant window film)')],
         colours=['deep-blue', 'gloss-black', 'pure-white'],
         faq=[('Is clear PPF worth it in Singapore?', 'If your car does a lot of expressway driving or you plan to keep it for years, clear PPF saves the paint from chips that would otherwise need touch-ups or a respray.'),
              ('Can I do PPF on only the front of the car?', 'Yes. Many owners protect the bonnet, front bumper, fenders and mirrors first, as those take most of the chips. WhatsApp us for a front-only quote.'),
              ('Will clear PPF turn yellow?', 'Film quality decides how it ages. Ask us which film we fit on your car and what its warranty covers before you book.'),
              ('Can PPF go on headlights?', 'Yes, clear film can protect headlamps. LTA does not allow tinting or masking of vehicle lamps, so headlamp film should stay clear.')]),
    dict(slug='window-film', short='Window film', photo='installer-window-film',
         title='Car Window Tint & Solar Film in Singapore | Wrapstar',
         desc='LTA compliant nano ceramic solar film with 93% to 96% IR rejection to cut cabin heat. Our opening offer was $358 with a 7-year warranty. Yishun.',
         h1='Window film and solar tint',
         gist='Nano ceramic solar film that cuts the heat, LTA compliant, with a 7-year warranty on our opening offer.',
         lede='Singapore sun bakes a cabin fast, and glass roofs on EVs make it worse. Good solar film keeps the heat out without making your windows too dark to be legal.',
         answer='Car window film is a thin film fitted on the inside of the glass to reject heat and UV. The nano ceramic solar film we posted has 93% to 96% IR rejection, and we fit shades that meet Singapore\'s light rules: at least 70% visible light through the front windscreen and front side windows, and 25% at the rear.',
         points=[('Cooler cabin.', 'Nano ceramic film with 93% to 96% IR (heat) rejection, as posted for our opening offer.'),
                 ('Legal shades.', 'We match the 70% front and 25% rear light rule (MOT, 7 April 2026).'),
                 ('Old film removed.', 'Our opening offer included free removal of your existing film.'),
                 ('7-year warranty.', 'As stated on our opening offer; ask us for today\'s terms.')],
         offers=[('$358', 'nano ceramic solar film, our opening promotion (usual price $428), with free removal of old film, installation and a sunshade'),
                 ('$388', 'LTA compliant tint for hatchbacks and sedans, our National Day offer in August 2026')],
         colours=['satin-black', 'gloss-black'],
         faq=[('How dark can my car tint be in Singapore?', 'Film on the front windscreen and front side windows must let at least 70% of visible light through, and at least 25% on the rear windscreen and rear side windows. This was restated by the Ministry of Transport on 7 April 2026.'),
              ('Do I need LTA approval for window tint?', 'No. OneMotoring lists tinted films and tinted glass under modifications that do not need LTA approval, as long as the light rules are met.'),
              ('Does solar film help with a Tesla glass roof?', 'Yes. A heat-rejecting film on a panoramic glass roof cuts the heat that comes through it. See our guide on Tesla roof heat.'),
              ('How much is car window tint?', 'Our opening offer for nano ceramic solar film was $358 (usual price $428). WhatsApp your car model for today\'s price.')]),
    dict(slug='dechrome', short='Dechrome', photo='byd-seal-gloss-black-side',
         title='Chrome Delete (Dechrome) in Singapore | Wrapstar Autostyle',
         desc='Dechrome in Yishun: we turn chrome window trims, grilles and badges black with film. A sharper, sportier look that can be reversed. WhatsApp for a quote.',
         h1='Dechrome in Singapore: chrome delete for trims, grilles and badges',
         gist='Turn shiny chrome trims and badges black for a sharper, sportier look.',
         lede='Chrome window lines, grille surrounds and badges date a car fast. Dechrome covers them in gloss or satin black film, so the car looks lower, cleaner and newer.',
         answer='Dechrome, or chrome delete, means covering a car\'s chrome trims, such as window surrounds, grille bars, roof rails and badges, with black film. It gives a stealthier, sportier look, costs far less than replacing the parts, and the film can be removed later.',
         points=[('Window trims.', 'Chrome window lines in gloss or satin black.'),
                 ('Grille and badges.', 'Grille surrounds, emblems and lettering blacked out.'),
                 ('Pairs with a wrap.', 'Common with a colour change or colour PPF to finish the look.'),
                 ('Reversible.', 'The chrome is still there under the film if you want it back.')],
         offers=[('By quote', 'depends on how many chrome parts your car has; send us a photo on WhatsApp')],
         colours=['gloss-black', 'satin-black', 'bright-yellow'],
         faq=[('What is dechrome?', 'Dechrome, or chrome delete, is covering the chrome parts of a car with black film so they match a stealth or sporty look.'),
              ('How much does dechrome cost?', 'It depends on how many chrome parts your car has. Send a photo of your car on WhatsApp and we will quote you.'),
              ('Can dechrome be removed?', 'Yes. The film can be peeled off later and the chrome underneath is still there.'),
              ('Can I dechrome without wrapping the whole car?', 'Yes. Dechrome is often done on its own, as a quick way to change how a car looks.')]),
    dict(slug='ceramic-coating', short='Ceramic coating', photo='tesla-white-studio',
         title='Car Ceramic Coating in Yishun, Singapore | Wrapstar Autostyle',
         desc='Ceramic coating for paint, wraps and PPF in Yishun. Polish first, then coat, for gloss that is easier to wash. Part of our $628 nett car care bundle.',
         h1='Ceramic coating',
         gist='A hard, glossy layer over your paint that makes washing easier. Done after a polish.',
         lede='A ceramic coating is a liquid layer that bonds to your paint and cures hard. Water beads off, dirt lets go more easily, and the gloss stays deeper between washes.',
         answer='Ceramic coating is a liquid coating applied by hand to a clean, polished car. It bonds to the paint and cures into a thin, hard, glossy layer that repels water and makes dirt easier to wash off. It does not stop stone chips: that is what paint protection film is for.',
         points=[('Easier washing.', 'Water beads and runs off, and grime rinses away more easily.'),
                 ('Deeper gloss.', 'The coating goes on after a polish, so the shine you see is locked in.'),
                 ('Works with film.', 'Can go on paint, and on wraps or PPF, to keep them easier to clean.'),
                 ('Bundle price.', 'Included in our $628 nett car care bundle with polish, window film and headlight PPF.')],
         offers=[('$628 nett', 'car care bundle (usual price $950): polish and ceramic coating, LTA compliant window film and free headlight PPF (one pair); terms and limited availability apply'),
                 ('By quote', 'ceramic coating on its own; send us your car model on WhatsApp')],
         colours=['pure-white', 'gloss-black', 'deep-blue'],
         faq=[('What is car ceramic coating?', 'A liquid coating that bonds to your car paint and cures into a hard, glossy layer. It repels water and makes the car easier to keep clean.'),
              ('Does ceramic coating protect against stone chips?', 'No. A coating is very thin. For stone chips and scratches, clear PPF or colour PPF is the right choice, and a coating can go on top.'),
              ('Do I need a polish before ceramic coating?', 'Yes. The paint is cleaned and polished first, so the coating locks in a clean, glossy finish rather than old swirls.'),
              ('How much is ceramic coating at Wrapstar?', 'Our car care bundle with polish and ceramic coating, LTA compliant window film and free headlight PPF was posted at $628 nett (usual price $950). WhatsApp us for coating on its own.')]),
    dict(slug='polishing', short='Polishing', photo='studio-white-tesla',
         title='Car Polishing in Yishun, Singapore | Wrapstar Autostyle',
         desc='Car paint polishing in Yishun to lift light swirls and dullness before a coating, wrap or sale. Part of our $628 nett car care bundle. WhatsApp us.',
         h1='Car polishing',
         gist='Brings back gloss by working out light swirls and dull spots in the paint.',
         lede='Washing marks, light swirls and a dull finish build up on every daily car. A machine polish works them out of the top layer of the paint so the colour looks rich again.',
         answer='Car polishing uses a machine and a fine abrasive polish to level the top layer of clear coat. It reduces light swirls, wash marks and dullness and brings the gloss back. Deep scratches that go through the clear coat cannot be polished out. A polish is also the first step before a ceramic coating.',
         points=[('Gloss back.', 'Light swirls and wash marks are reduced, so the paint looks deeper.'),
                 ('Before a coating.', 'Polishing comes first so a ceramic coating locks in a clean finish.'),
                 ('Before you sell.', 'A polished car photographs and shows better; our sister business Star Performance Motor is in the same unit.'),
                 ('Bundle price.', 'Included in our $628 nett car care bundle with ceramic coating, window film and headlight PPF.')],
         offers=[('$628 nett', 'car care bundle (usual price $950): polish and ceramic coating, LTA compliant window film and free headlight PPF (one pair); terms and limited availability apply'),
                 ('By quote', 'polishing on its own; send us your car model and a photo of the paint on WhatsApp')],
         colours=['gloss-black', 'deep-blue', 'pure-white'],
         faq=[('What does car polishing do?', 'It levels the top layer of clear coat to reduce light swirls, wash marks and dullness, so the paint looks glossy again.'),
              ('Can polishing remove scratches?', 'Light scratches and swirls, yes. Scratches that go through the clear coat to the colour or primer need a touch-up or respray instead.'),
              ('Should I polish a wrapped or matte car?', 'No. Matte and satin wraps should never be polished, because polish adds uneven shine. Paint is polished before a wrap or coating, not the film itself.'),
              ('How much is car polishing at Wrapstar?', 'Polish and ceramic coating are part of our car care bundle, posted at $628 nett (usual price $950) with LTA compliant window film and free headlight PPF. WhatsApp us for polishing on its own.')]),
]
SBY = {s['slug']: s for s in SERVICES}

# ------------------------------------------------------------------------------------------------
# Articles
# ------------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='colour-ppf-vs-vinyl-wrap', photo='tesla-model-3-satin-black-angle', svc='colour-ppf', date='2026-10-17',
         title='Colour PPF vs Vinyl Wrap: Which One for Your Car?',
         desc='Colour PPF and vinyl wraps both change your car colour. Here is how they differ on protection, price and feel, from a Singapore wrap shop.',
         h1='Colour PPF vs vinyl wrap: which one suits your car?',
         card='Both change the colour. Only one also stops stone chips. Here is how to choose.',
         body=[('h2', 'The short answer'),
               ('ans', 'Choose a vinyl wrap if you mainly want a new colour at a lower price. Choose colour PPF if you also want real protection from stone chips and scratches, and you plan to keep the car for years. Both can be removed later.'),
               ('h2', 'How they compare'),
               ('table', [('', 'Vinyl colour wrap', 'Colour PPF'),
                          ('Material', 'Thin PVC vinyl film', 'Thick TPU (ours is 7.5mil)'),
                          ('Stone chips', 'Some protection from light marks', 'Absorbs stone chips and road rash'),
                          ('Light swirls', 'Stay until polished or replaced', 'Fade with heat (hot water or sun)'),
                          ('Finishes', 'Widest range, from gloss to matte', 'Gloss, satin and matte in a smaller range'),
                          ('Our posted price', 'From $1,588 full car', 'Tesla Model 3 satin black $2,788 nett (Oct 2026)')]),
               ('h2', 'When a vinyl wrap makes more sense'),
               ('p', 'A wrap is the quickest way to try a bold colour. If you change cars every few years, lease, or just want a fresh look for your next chapter, vinyl gives you the most colours for the least money. It still keeps the original paint underneath, which helps when you sell.'),
               ('h2', 'When colour PPF is worth the extra'),
               ('p', 'If you drive on expressways daily, the front of the car takes a stream of small stones. Colour PPF takes those hits so the paint does not. Its hydrophobic topcoat also means rain, bird droppings and tree sap slide off, so washing is faster. For a car you want to keep looking new, the extra cost buys years of protection, not just a colour.'),
               ('h2', 'What both need'),
               ('ul', ['Healthy paint underneath: chips and bad resprays show through film and can lift when it is removed.',
                       'A careful installer: edges, door shuts and seams decide whether a job looks factory or homemade.',
                       'Gentle washing: hand wash, keep pressure washers away from edges, and skip harsh polishes on matte or satin film.']),
               ('h2', 'See both on real cars'),
               ('p', 'Our colour catalogue shows the colours we have done, from satin black colour PPF on a Tesla Model 3 to a matte green BYD Sealion 7. Send us your car model and the look you want, and we will tell you which film fits.')],
         faq=[('Is colour PPF better than a wrap?', 'It protects more, because the film is thicker TPU that absorbs stone chips and heals light swirls in heat. A vinyl wrap costs less and comes in more colours. Which is better depends on whether you want protection or just a new look.'),
              ('Which lasts longer, wrap or colour PPF?', 'Film life depends on the brand, the colour, and how the car is parked and washed. Ask us which film we would fit on your car and what its warranty covers.')]),
    dict(slug='car-window-tint-rules-singapore', photo='installer-window-film-2', svc='window-film', date='2026-10-17',
         title='Car Window Tint Rules in Singapore (2026): 70% and 25%',
         desc='How dark can car tint be in Singapore? Front windows need 70% visible light, rear windows 25%, per MOT on 7 April 2026. What that means for your car.',
         h1='Car window tint rules in Singapore: the 70% and 25% light limits',
         card='How dark you can go, which windows count, and whether you need LTA approval.',
         body=[('h2', 'The rule in one line'),
               ('ans', 'In Singapore, film on the front windscreen and front side windows must let at least 70% of visible light through, and film on the rear windscreen and rear side windows must let at least 25% through. The Ministry of Transport restated this in Parliament on 7 April 2026.'),
               ('h2', 'What the numbers mean'),
               ('p', 'The percentage is visible light transmission: how much light still gets through the glass and film together. A higher number is lighter. So "70%" at the front means a light film, chosen mainly to reject heat, while "25%" at the rear allows a much darker shade for privacy.'),
               ('h2', 'Do you need LTA approval?'),
               ('p', 'No. LTA\'s OneMotoring page on vehicle modifications lists tinted films and tinted glass as modifications that do not need LTA approval. The same page lists tinting or masking of vehicle lamps as not allowed, so headlights and tail lights must not be tinted.'),
               ('h2', 'Heat rejection matters more than darkness'),
               ('p', 'Dark film is not the same as cool film. What keeps a cabin cool is infrared (IR) rejection. The nano ceramic solar film we posted for our opening offer rejects 93% to 96% of IR, so a light, legal front film can still cut a lot of heat.'),
               ('h2', 'Our checklist before you tint'),
               ('ul', ['Ask for the visible light figure of each film on each window, front and rear.',
                       'Ask for the IR rejection figure, not just the shade.',
                       'Check what the warranty covers: fading, bubbling and peeling.',
                       'If you have old film, ask whether removal is included.'])],
         faq=[('Is 50% tint legal on front windows in Singapore?', 'No. Front windscreen and front side windows need at least 70% visible light transmission, so a 50% film is too dark for the front.'),
              ('Can I tint my headlights?', 'No. OneMotoring lists tinting or masking of vehicle lamps as a modification that is not allowed. Clear protection film on headlamps is a different thing and keeps them clear.')]),
    dict(slug='tesla-glass-roof-heat', photo='tesla-white-studio', svc='window-film', date='2026-10-17',
         title='Tesla Glass Roof Too Hot? How Solar Film Helps',
         desc='Tesla Model 3 and Model Y glass roofs let a lot of heat in under Singapore sun. How heat-rejecting film works and what to ask before you fit it.',
         h1='Tesla glass roof too hot? How heat-rejecting film helps',
         card='Why the panoramic roof bakes the cabin, and what a nano ceramic film changes.',
         body=[('h2', 'Why the cabin heats up'),
               ('ans', 'A panoramic glass roof is a big window facing straight up at the midday sun. Even with the factory coating, infrared heat comes through and warms the seats, the dashboard and your head. A heat-rejecting film on the inside of the glass blocks much of that infrared before it reaches the cabin.'),
               ('h2', 'What a nano ceramic film does'),
               ('p', 'Nano ceramic films are built to reject infrared heat while staying clear enough to see through. The film we posted for our opening offer rejects 93% to 96% of IR. You keep the open, airy view of the glass roof, with less of the heat.'),
               ('h2', 'Is roof film allowed?'),
               ('p', 'The light limits in Singapore cover the front windscreen and front side windows (at least 70% visible light) and the rear windows (at least 25%). Tinted films do not need LTA approval, according to OneMotoring. Ask us which film we recommend for your roof and why.'),
               ('h2', 'What we see on Teslas'),
               ('p', 'Teslas are some of the most common cars in our studio, for satin black colour PPF on the Model 3 and colour changes on the Model Y. Owners often add window film at the same visit, so the car comes back both looking new and feeling cooler.'),
               ('h2', 'Before you book'),
               ('ul', ['Ask for the IR rejection figure of the exact film, not a range for the brand.',
                       'Ask how they handle the large curved roof glass without seams.',
                       'Check the warranty terms for bubbling and peeling.'])],
         faq=[('Does Tesla glass roof film reduce heat?', 'Yes. A heat-rejecting film on the inside of the roof glass blocks much of the infrared heat that would otherwise warm the cabin. Our posted nano ceramic film rejects 93% to 96% of IR.'),
              ('Can I fit film on both the Model 3 and Model Y roof?', 'Yes, both have large glass roofs. WhatsApp us your model and year for a quote.')]),
    dict(slug='satin-matte-or-gloss-wrap', photo='bmw-m4-stealth-grey-studio', svc='colour-change-wrap', date='2026-10-17',
         title='Satin, Matte or Gloss Wrap: Choosing Your Finish',
         desc='Gloss, satin and matte wraps look and age differently. How each finish looks in Singapore light, how to care for it, and which suits your car.',
         h1='Satin, matte or gloss: how to choose your wrap finish',
         card='The finish changes a colour more than you think. See all three on real cars.',
         body=[('h2', 'The quick guide'),
               ('ans', 'Gloss looks like fresh paint and is the easiest to care for. Satin has a soft sheen that shows body lines without glare. Matte is completely flat and the most dramatic, but needs the gentlest washing. Pick the finish first, then the colour.'),
               ('h2', 'Gloss'),
               ('p', 'Gloss film reflects light like paint, so bright colours pop. Our bright yellow Tesla Model Y and baby blue Mercedes-Benz A-Class are both gloss. It is the most forgiving finish to wash and the easiest to keep looking new.'),
               ('h2', 'Satin'),
               ('p', 'Satin sits between gloss and matte: a low sheen that follows every crease of the body. Our satin black Tesla Model 3 is the example. It looks expensive and modern, and it hides light swirls better than gloss.'),
               ('h2', 'Matte'),
               ('p', 'Matte is flat with no shine at all, which makes a car look like it was carved. Our stealth grey BMW M4 and matte green BYD Sealion 7 show how strong it looks. Matte needs care: no waxes or polishes, and spots should be wiped off soon so they do not leave marks.'),
               ('h2', 'Light matters in Singapore'),
               ('p', 'Strong midday sun washes out pale colours and makes dark gloss colours show every swirl. Look at samples outdoors, not only under shop lights, before you decide. We are happy to show you finished cars in our photos and on our Facebook page.'),
               ('h2', 'Care by finish'),
               ('ul', ['Gloss: normal hand wash, a film-safe detailer spray is fine.',
                       'Satin: hand wash, avoid polishes and wax, which can add uneven shine.',
                       'Matte: hand wash with matte-safe products only, never polish, and clean droppings quickly.'])],
         faq=[('Is matte wrap hard to maintain?', 'It needs more care than gloss: hand wash with matte-safe products, no waxing or polishing, and clean bird droppings quickly. Done right, it keeps its flat look.'),
              ('Which wrap finish hides scratches best?', 'Satin and matte hide light swirls better than gloss, because there is less reflection to show them.')]),
    dict(slug='caring-for-a-wrapped-car', photo='tesla-model-y-yellow-front', svc='colour-change-wrap', date='2026-10-17',
         title='How to Wash and Care for a Wrapped or PPF Car',
         desc='Simple rules to keep a wrapped or PPF car looking new in Singapore: hand washing, pressure washers, bird droppings, parking and what to avoid.',
         h1='How to wash and care for a wrapped or PPF car',
         card='Six simple habits that keep a wrap or PPF looking new for longer.',
         body=[('h2', 'The basics'),
               ('ans', 'Hand wash your wrapped or PPF car with a pH-neutral shampoo, keep pressure washers away from film edges, remove bird droppings and sap quickly, and avoid polishes and waxes on satin or matte film. Park in shade when you can.'),
               ('h2', 'Six habits that make film last'),
               ('ol', ['Wait a few days after the job before the first wash, so the film settles.',
                       'Hand wash with a soft mitt and a pH-neutral car shampoo.',
                       'If you use a pressure washer, stand back and never aim at seams or edges.',
                       'Clean bird droppings, sap and fuel spills the same day.',
                       'Skip abrasive polishes and cutting compounds, and on satin or matte film, skip wax.',
                       'Park in shade or a covered car park when you can: sun is the biggest ager of any film.']),
               ('h2', 'Automatic car washes'),
               ('p', 'Brush tunnels can scratch film and catch edges. A hand wash, or a touchless wash used gently, is kinder to a wrap or PPF.'),
               ('h2', 'Colour PPF self-heals, within limits'),
               ('p', 'On colour PPF, light swirls fade under hot water or a hot afternoon. Deeper cuts through the film stay, and a damaged panel can usually be re-filmed on its own.'),
               ('h2', 'Come back for a check'),
               ('p', 'One owner who had coloured PPF fitted with us wrote that they were asked to come back after a week so we could check for air bubbles or defects. If anything lifts or bubbles, WhatsApp us a photo.')],
         faq=[('When can I wash my car after a wrap?', 'Give the film a few days to settle before the first wash, then hand wash gently. Ask us for the exact timing for your film.'),
              ('Can I use a car wash after PPF?', 'Hand washing is best. Avoid brush tunnels, and keep pressure washers well back from film edges.')]),
    # EDGE daily article 18 Oct 2026 (hand-built by the 8pm run; facts from the PPF service page + OneMotoring lamp rule already on the site)
    dict(slug='which-car-panels-need-ppf-first', photo='ppf-headlamp-install', svc='paint-protection-film', date='2026-10-18',
         title='Which Car Panels Should Get Clear PPF First?',
         desc='Not doing the full car? The panels that take the most stone chips on Singapore roads, the order to cover them in, and what to ask before you book PPF.',
         h1='Which car panels should you cover with clear PPF first?',
         card='Not doing the full car? Start where the stone chips land.',
         body=[('h2', 'The short answer'),
               ('ans', 'Start with the front of the car: the front bumper, bonnet, front fenders and side mirrors take most of the stone chips on Singapore expressways. Next come the headlights, the door edges and door cups, and the top of the rear bumper where bags are loaded. A full car covers everything; a front-first job protects where most damage happens.'),
               ('h2', 'Why does the front take the hits?'),
               ('p', 'At expressway speeds, small stones flicked up by the car in front strike the leading edges of your car: the bumper, the front of the bonnet and the mirror caps. That is why a car a few years old usually shows its chips at the front, while the roof and rear doors still look fine.'),
               ('h2', 'In what order should panels be covered?'),
               ('ol', ['Front bumper: the lowest, most forward panel, and the one that takes the most chips.',
                       'Bonnet: the full bonnet if you can, or at least its leading edge.',
                       'Front fenders and side mirror caps: they catch stones thrown up from the front and the wheels.',
                       'Headlights: clear film helps against chips and haze. Keep it clear, because LTA does not allow tinting or masking of vehicle lamps.',
                       'Door edges and door cups: they guard against door knocks and fingernail scratches around the handles.',
                       'Top of the rear bumper: where bags and boxes slide in and out of the boot.']),
               ('h2', 'Front only or the full car?'),
               ('p', 'Front only suits owners who mainly want to stop stone chips at a lower price. A full car makes sense if you want every panel kept as new, often park in open car parks, or plan to keep the car for many years. Our National Day offer in August 2026 was clear PPF for hatchbacks and sedans at $2,188. WhatsApp us the panels you want for today\'s price.'),
               ('h2', 'What should you ask before you book?'),
               ('ul', ['Exactly which panels are covered, and whether the film wraps around the edges.',
                       'Which film is fitted, and what its warranty covers.',
                       'Whether chips already in the paint should be touched up first, since they show through clear film.',
                       'How long to wait before the first wash.'])],
         faq=[('Is it worth putting PPF on only the front of the car?', 'For many owners, yes. The front bumper, bonnet, fenders and mirrors take most stone chips, so covering them first protects where most damage happens, at a lower cost than a full car.'),
              ('Can PPF go on headlights in Singapore?', 'Yes, clear film can protect headlamps from chips and haze. LTA does not allow tinting or masking of vehicle lamps, so headlamp film must stay clear.'),
              ('Can I add more panels later?', 'Usually, yes. PPF is fitted panel by panel, so you can start with the front and add panels later. Ask us how the new film will meet the existing edges.')]),
    # Daily article 19 Oct 2026 (hand-built; facts from the site's own wrap/PPF/polishing pages; sister link = cross-linking opportunity #8, declared sister, same unit)
    dict(slug='should-you-remove-a-wrap-before-selling', photo='installer-ppf-bonnet', svc='colour-change-wrap', date='2026-10-19',
         title='Should You Remove a Car Wrap Before Selling Your Car?',
         desc='Selling a wrapped or PPF-covered car? When to keep the film, when to take it off, what happens to the paint underneath, and what buyers will ask.',
         h1='Should you remove your car wrap or PPF before you sell the car?',
         card='Keep the film or take it off? It depends on the film, the paint and the buyer.',
         body=[('h2', 'The short answer'),
               ('ans', 'Not always. Clear PPF in good condition is usually worth keeping, because it has protected the paint a buyer will see. A colour wrap is a personal choice, so many owners take it off and sell the car in its original colour. Either way, check the film and the paint under it before you list the car.'),
               ('h2', 'When is it worth keeping the film on?'),
               ('p', 'Clear PPF is close to invisible, so it does not change the car a buyer sees. If it is clean, with no lifting edges or yellowing, it shows that the front of the car has been kept safe from stone chips. A colour wrap or colour PPF in a neutral shade and in good condition can also stay, if the buyer likes the look.'),
               ('h2', 'When is it better to take it off?'),
               ('ul', ['The colour is bold or personal, and most buyers will want the factory colour.',
                       'The film is scratched, faded or lifting at the edges, which looks worse than bare paint.',
                       'The buyer or dealer wants to see the original paint before agreeing a price.']),
               ('h2', 'What happens to the paint when the film comes off?'),
               ('p', 'A good film on healthy factory paint comes off cleanly, and the paint underneath is in the condition it was protected in. Panels that were badly resprayed before the film went on can lift paint when the film is pulled off, so removal is a job for a wrap studio, not a quick peel at home. A polish afterwards brings the paint back to an even shine.'),
               ('h2', 'What will a buyer or dealer ask?'),
               ('raw', 'Expect questions on which film is on the car, when it was fitted, which panels it covers and what is underneath, so keep the invoice and photos from the job. If you are selling or trading in, ask <a href="https://starperformancemotor.com/services/sell-your-car/">our sister dealer Star Performance Motor</a>, in the same unit in Yishun, whether to keep the film on or take it off before they make an offer.')],
         faq=[('Does a car wrap hurt resale value?', 'A wrap keeps the factory paint underneath, which helps when you sell. A worn or very personal colour can put some buyers off, so many owners remove it before selling.'),
              ('Should I remove clear PPF before selling?', 'Usually not, if it is in good condition. Clear PPF does not change how the car looks, and it has kept the paint under it protected.'),
              ('Can I remove a car wrap myself?', 'It is safer to have a wrap studio do it. Film on resprayed panels can pull paint off, and leftover adhesive needs careful cleaning.')]),
    # Daily article 20 Oct 2026 (queue #1; hand-built; general film knowledge, no warranty or lifespan figure claimed for Wrapstar)
    dict(slug='how-long-does-a-car-wrap-last-in-singapore', photo='bmw-m4-stealth-grey-studio', svc='colour-change-wrap', date='2026-10-20',
         title='How Long Does a Car Wrap Last in Singapore?',
         desc='How long a vinyl car wrap lasts in Singapore\'s sun and rain depends on the film, the panel and how the car is kept. Signs of ageing, and how to make it last.',
         h1='How long does a car wrap last in Singapore?',
         card='Sun, rain and parking decide it as much as the film does. What to expect, and how to make a wrap last.',
         body=[('h2', 'The short answer'),
               ('ans', 'It depends on the film, the panel and how the car is kept. Film makers publish their own durability figures, usually in years, and the figure is lower for horizontal panels and for hot, sunny climates like Singapore\'s. A car that is parked under shelter and washed gently keeps its wrap looking good for much longer than one left in open-air car parks all day.'),
               ('h2', 'Why does Singapore weather age a wrap faster?'),
               ('p', 'Strong sun all year means steady UV exposure and high surface temperatures, especially on dark colours. UV fades the colour and dries out the film over time, and heat softens the adhesive at the edges. Frequent rain is less of a problem than sun, but dirt left to dry on the film after rain can stain lighter colours.'),
               ('h2', 'Which panels age first?'),
               ('p', 'The roof, bonnet and boot lid face the sun directly, so they usually fade or lose their finish before the doors and sides. Edges and deep recesses, where the film is stretched the most, are where lifting tends to start.'),
               ('h2', 'What are the signs a wrap is ageing?'),
               ('ul', ['Fading or a chalky look on the roof and bonnet.',
                       'Small cracks in the film, often on horizontal panels first.',
                       'Edges or corners starting to lift.',
                       'Stains that no longer wash out, or a gloss finish turning dull.']),
               ('h2', 'How can you make a wrap last longer?'),
               ('raw', 'Park in the shade or a sheltered car park when you can, wash the car by hand regularly and dry it, and clean off bird droppings and tree sap quickly. Avoid harsh brushes and holding a pressure washer close to the edges. Our guide on <a href="articles/caring-for-a-wrapped-car/">caring for a wrapped car</a> covers washing and products step by step.'),
               ('h2', 'Does the finish make a difference?'),
               ('raw', 'Satin and matte finishes show stains and marks differently from gloss and need gentler cleaning, so care matters more. See <a href="articles/satin-matte-or-gloss-wrap/">satin, matte or gloss</a> to compare, or our <a href="services/colour-change-wrap/">colour change wrap</a> service to talk about which film suits how your car is parked and used.')],
         faq=[('How long does a car wrap last in Singapore?', 'It depends on the film, the panel and how the car is kept. Film makers give their own durability figures, which are lower for horizontal panels and sunny climates. Sheltered parking and gentle washing make a wrap last longer.'),
              ('Which part of a wrap fades first?', 'Usually the roof, bonnet and boot lid, because they face the sun directly. Edges and deep recesses are where lifting tends to start.'),
              ('Can an old wrap be removed safely?', 'Usually, yes, by a wrap studio. The longer an old film stays on in the sun, the harder it can be to remove, so do not leave a failing wrap on for too long.')]),
    # Night article 26 Oct 2026 (new intent, not in queue; general advice only, no film brands, warranty, lifespan or price claims)
    dict(slug='what-to-ask-before-booking-a-car-wrap-in-singapore', photo='mercedes-cla-stealth-grey-rear', svc='colour-change-wrap', date='2026-10-26',
         title='What to Ask Before Booking a Car Wrap in Singapore',
         desc='Questions to ask a car wrap studio in Singapore before you book: the film, the panels covered, door edges, aftercare, removal and what is in writing.',
         h1='What should you ask before booking a car wrap in Singapore?',
         card='The questions that help you compare wrap studios fairly: film, panels, edges, aftercare, removal and what is in writing.',
         body=[('h2', 'The short answer'),
               ('ans', 'Ask which film will be used and in which finish, exactly which parts of the car are covered, how door edges and tricky areas are handled, how to look after the wrap, and how it will be removed later. Ask for the answers in writing, so you can compare studios on the same job rather than on a headline price.'),
               ('h2', 'Which film and finish will be used?'),
               ('p', 'Ask for the name of the film, its finish (gloss, satin or matte) and the exact colour code, not just a colour name. Different films behave differently on curves and age differently in the sun, so two quotes for "satin black" may not be the same product. Our guide to <a href="articles/satin-matte-or-gloss-wrap/">satin, matte or gloss</a> explains how the finishes differ.'),
               ('h2', 'Exactly which parts of the car are covered?'),
               ('ul', ['Roof, bonnet, boot, mirrors, bumpers and door handles: which are included?',
                       'Are door jambs and the areas that show when doors, bonnet or boot are open covered, or left in the original colour?',
                       'Are trims, badges and chrome parts removed, wrapped or left alone?',
                       'Does the quote cover the whole car or only the panels you listed?']),
               ('h2', 'How are edges, recesses and seams handled?'),
               ('p', 'Edges and deep recesses are where film is stretched most, so they are where lifting tends to start. Ask how the studio finishes edges and where any seams will fall. Look at finished cars in good light, not just photos, and check the corners, door edges and around the badges.'),
               ('h2', 'Is the paint checked first?'),
               ('raw', 'Film follows the surface under it, so chips, dents and past resprays can show through, and badly resprayed panels can lift paint when film is removed later. A good studio checks the paint before it starts and tells you about any risk. See <a href="articles/how-to-prepare-your-car-for-a-wrap-or-ppf/">how to prepare your car for a wrap or PPF job</a> for what to tell them.'),
               ('h2', 'What aftercare and removal should you expect?'),
               ('raw', 'Ask when you can first wash the car, how to wash it, what to avoid and who to contact if film bubbles or lifts. Ask too how the wrap will be removed and by whom, because removal is a job for a studio, not a quick peel at home. Our guide to <a href="articles/caring-for-a-wrapped-car/">caring for a wrapped car</a> covers everyday care.'),
               ('h2', 'What should be in writing?'),
               ('raw', 'Ask for the film and colour, the parts covered and not covered, the price and what it includes, the collection date and the aftercare steps in one message or document. If a studio gives a warranty, ask what it covers and for how long, and keep that in writing too. To compare a wrap with other options first, read <a href="articles/car-wrap-or-respray-which-is-better/">wrap or respray</a>, or <a href="services/colour-change-wrap/">talk to us about a colour change wrap</a> on WhatsApp.')],
         faq=[('Should I choose a wrap studio on price alone?', 'No. Two quotes can cover different films, different parts of the car and different aftercare. Ask each studio the same questions and compare the answers in writing.'),
              ('Do wrap quotes include door jambs?', 'Not always. Ask whether the areas visible when doors, bonnet or boot are open are included, because many wraps leave them in the original colour.'),
              ('How do I check the quality of a studio\'s work?', 'Look at finished cars in good light, check edges, corners and around badges, and ask to see past jobs on a similar car to yours.')]),
    dict(slug='can-dechrome-be-reversed', photo='byd-seal-gloss-black-side', svc='dechrome', date='2026-10-28',
         title='Can Dechrome Be Reversed? What to Know First',
         desc='Can dechrome (chrome delete) be reversed? What happens to the chrome under the film, what affects removal, and what to ask a studio before you book.',
         h1='Can dechrome be reversed?',
         card='Dechrome covers chrome with black film. What happens to the chrome underneath, and what to ask before you book.',
         body=[('h2', 'The short answer'),
               ('ans', 'Yes. Dechrome covers chrome trims with black film instead of removing or painting them, so the film can be peeled off later and the chrome underneath is still there. How cleanly it comes off depends on the age of the film and the condition of the surface under it, so have a studio remove it rather than peeling it yourself.'),
               ('h2', 'What happens to the chrome under the film?'),
               ('p', 'Dechrome is a covering, not a change to the part. Window surrounds, grille bars, roof rails and badges are covered in gloss or satin black film, and the chrome is still there under it if you want it back. That is the main difference from replacing or painting the parts.'),
               ('h2', 'What affects how easily the film comes off?'),
               ('ul', ['How long the film has been on the car, and how much sun and heat it has had.',
                       'The condition of the surface underneath, such as chips, scratches or earlier repairs.',
                       'Whether the part was resprayed or repaired before the film went on.',
                       'Who removes it and how: a studio that knows the film is more likely to take it off cleanly than a quick peel at home.']),
               ('h2', 'Why does it matter if you plan to sell the car?'),
               ('raw', 'Because dechrome is reversible, you can choose to keep it or return the car to its chrome look before a sale. Which is better depends on the buyer. Our guide on <a href="articles/should-you-remove-a-wrap-before-selling/">whether to remove a wrap before selling</a> covers the same question for wraps.'),
               ('h2', 'What should you ask a studio before booking dechrome?'),
               ('ul', ['Exactly which parts will be covered: window trims, grille, roof rails, badges, lettering?',
                       'Which film and finish (gloss or satin black) will be used?',
                       'How will the film be removed later, by whom, and what should you expect the surface to look like?',
                       'What is the price, and what is in writing?']),
               ('raw', 'Our <a href="articles/what-to-ask-before-booking-a-car-wrap-in-singapore/">guide to what to ask before booking a car wrap</a> has more questions that also apply to dechrome. To see what we do, read about our <a href="services/dechrome/">dechrome service</a>; the price depends on how many chrome parts your car has, so send a photo of your car on WhatsApp for a quote.')],
         faq=[('Will dechrome damage the chrome underneath?', 'The chrome is still there under the film. How the surface looks after removal depends on its condition when the film went on and how the film is taken off, so ask your studio how they remove it.'),
              ('Can I dechrome without wrapping the whole car?', 'Yes. Dechrome is often done on its own, as a quick way to change how a car looks, and it also pairs with a colour change wrap or colour PPF.'),
              ('Should I remove dechrome film myself?', 'We recommend asking a studio to do it. Removal is easier to do cleanly when the person knows the film and checks the surface as it comes off.')]),
]
ABY = {a['slug']: a for a in ARTICLES}
LASTMOD = {'articles/should-you-remove-a-wrap-before-selling/': '2026-10-19',
           'articles/how-long-does-a-car-wrap-last-in-singapore/': '2026-10-20',
           'services/dechrome/': '2026-10-19',
           'services/colour-ppf/': '2026-10-23',
           'articles/what-to-ask-before-booking-a-car-wrap-in-singapore/': '2026-10-26',
           'articles/can-dechrome-be-reversed/': '2026-10-28'}  # 23 Oct 2026 Booster: description on 'colour ppf singapore'
#  # 19 Oct 2026: new article; Booster H1/description change on 'dechrome singapore'

HOME_FAQ = [
    ('How much does a car wrap cost at Wrapstar?', 'Our posted price for a full car colour wrap starts from $1,588. Colour PPF, clear PPF, window film and dechrome are priced by car and film. See our prices page for recent offers, or WhatsApp your car model for a quote.'),
    ('Should I choose a vinyl wrap or colour PPF?', 'A vinyl wrap is the lower-cost way to change colour. Colour PPF also changes the colour, but it is thick TPU that absorbs stone chips and heals light swirls in heat. Pick colour PPF if you want protection as well as looks.'),
    ('Which colours can I choose?', 'Our colour catalogue shows colours seen on our past jobs, from satin black and matte green to baby blue and bright yellow. We can also source other colours: tell us what you have in mind.'),
    ('Where is Wrapstar Autostyle?', 'We are at 9 Yishun Industrial Street 1, #01-82, North Spring Bizhub, Singapore 768163, in the same unit as our sister business Star Performance Motor. We are open Monday to Friday 9am to 6pm and Saturday 9am to 3pm, closed on Sunday. WhatsApp 9754 1833 before you come down.'),
]


def business_schema():
    return {'@type': ['AutoBodyShop', 'LocalBusiness'], '@id': SITE + '#business', 'name': NAME, 'slogan': TAGLINE, 'url': SITE,
            'telephone': TEL, 'image': IMG + 'tesla-model-3-satin-black-rear.webp', 'logo': IMG + 'logo-wide.webp',
            'address': {'@type': 'PostalAddress', 'streetAddress': '%s %s %s' % (STREET, UNIT, BUILDING), 'addressLocality': 'Singapore',
                        'postalCode': POSTAL, 'addressCountry': 'SG'},
            'alternateName': 'Wrapstar', 'areaServed': 'Singapore', 'priceRange': '$$$', 'foundingDate': REGISTERED,
            'geo': {'@type': 'GeoCoordinates', 'latitude': GEO[0], 'longitude': GEO[1]}, 'hasMap': MAP, 'openingHoursSpecification': HOURS_SPEC,
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'UEN', 'value': UEN},
            'sameAs': [FB, IG, GBP],
            'knowsAbout': ['Car colour change wrap', 'Colour paint protection film', 'Clear paint protection film', 'Car window film', 'Dechrome', 'Ceramic coating', 'Car polishing'],
            'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Services', 'itemListElement': [
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['short'], 'url': SITE + 'services/%s/' % s['slug']}} for s in SERVICES]}}


# ------------------------------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------------------------------
def svc_card(s):
    return '<a class="svc" href="services/%s/">%s<span class="svc-t"><h3>%s</h3><p>%s</p><em>More details →</em></span></a>' % (
        s['slug'], img(s['photo']), E(s['short']), E(s['gist']))


def acard(a):
    return '<a class="acard" href="articles/%s/">%s<div><h3>%s</h3><p>%s</p></div></a>' % (a['slug'], img(a['photo']), E(a['h1']), E(a['card']))


WORKS = [('tesla-model-3-satin-black-front', 'satin-black'), ('tesla-model-y-yellow-front', 'bright-yellow'), ('byd-sealion-7-matte-green-front', 'matte-green'),
         ('mercedes-a-class-baby-blue-angle', 'baby-blue'), ('bmw-m4-stealth-grey-studio', 'stealth-grey'), ('tesla-model-y-ice-grey-angle', 'ice-grey'),
         ('mazda-cx-5-deep-blue-studio', 'deep-blue'), ('mercedes-a-class-pastel-pink', 'pastel-pink')]


def home():
    slides = [('tesla-model-3-satin-black-rear', 'Tesla Model 3 · satin black colour PPF'),
              ('mercedes-c-class-baby-blue-studio', 'Mercedes-Benz C-Class · baby blue, mid-wrap'),
              ('tesla-white-studio', 'Inside our Yishun studio')]
    sl = ''.join(img(n, 'slide', eager=(i == 0)).replace('<img ', '<img data-tag="%s" ' % E(t), 1) for i, (n, t) in enumerate(slides))
    works = ''.join('<a href="past-works/#%s">%s<span>%s</span></a>' % (k, img(n), E(CBY[k]['name'])) for n, k in WORKS)
    body = f'''<section class="hero"><div class="hero-grid">
<div class="hero-copy">
<p class="kicker">Wrapstar Autostyle · Yishun, Singapore</p>
<h1>Colour wraps &amp; PPF <span>in Singapore</span></h1>
<p class="tag">For cars that deserve more.</p>
<p class="lede">Colour change wraps, colour and clear PPF, window film and dechrome, done in our studio at North Spring Bizhub. New look, factory paint kept safe underneath.</p>
<div class="cta-row">{wa_btn()}<a class="btn btn-ghost" href="colours/">See the colours</a></div>
<ul class="hero-proof"><li><b>100%</b> recommend on Facebook</li><li><b>5</b> film services, one studio</li><li>Sister shop of <b>Star Performance Motor</b></li></ul>
</div>
<figure class="hero-media">{sl}<figcaption class="hero-tag">{E(slides[0][1])}</figcaption></figure>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Colour catalogue</p><h2>Pick your colour</h2><p>Colours seen on our past jobs, on real cars that left our studio. Tap one to see it from every angle.</p></div><a class="more" href="colours/">All colours →</a></div>
{colour_rail()}
<p class="note">Colour names describe what you see in our photos. Ask us for the exact film name, and for colours not shown here.</p>
</div></section>

<section class="sec sec-alt"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Services</p><h2>What does Wrapstar Autostyle do?</h2><p>Wrapstar Autostyle is a car wrap and film studio in Yishun, Singapore. We change your car colour with vinyl wraps or colour PPF, protect factory paint with clear PPF, cut cabin heat with LTA compliant window film, black out chrome trims, and polish and ceramic coat paint.</p></div><a class="more" href="services/">All services →</a></div>
<div class="svc-grid">{''.join(svc_card(s) for s in SERVICES)}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Past works</p><h2>What do our past works look like?</h2><p>Every photo is a real car from our studio, grouped by colour.</p></div><a class="more" href="past-works/">See all past works →</a></div>
<div class="works">{works}</div>
</div></section>

<section class="sec sec-alt"><div class="wrap"><div class="duo">
<figure class="quote"><blockquote>{E(REVIEW[2])}</blockquote><figcaption><b>{E(REVIEW[0])}</b> · colour PPF · Facebook, {E(REVIEW[1])} · <a href="{FB_REVIEWS}" target="_blank" rel="noopener">{E(REC)}</a></figcaption></figure>
<a class="sister" href="{SISTER}" target="_blank" rel="noopener">{img('window-film-mercedes-door')}<div><p class="kicker">Sister business</p><h3>Star Performance Motor</h3><p>Buying or selling a used car? Our sister business shares the same unit in Yishun. Get the car there, then give it its new look here.</p><span class="more">Visit Star Performance Motor →</span></div></a>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Questions</p><h2>Questions owners ask</h2></div><a class="more" href="articles/">All guides →</a></div>
{faq_html(HOME_FAQ)}
</div></section>'''
    page('', 'Car Wrap & Colour PPF Singapore | Wrapstar Autostyle',
         'Colour change car wraps, colour PPF, clear PPF, window film and dechrome in Yishun. See our colour catalogue and past works, then WhatsApp for a quote.',
         'Colour wraps & PPF for cars that deserve more', body, hero=False, schema=[faq_schema(HOME_FAQ)], preload='tesla-model-3-satin-black-rear')


def colours():
    rows = []
    for c in COLOURS:
        pics = ''.join(img(p) for p in c['pics'][:3])
        rows.append(f'''<article class="crow {c['fin']}" id="{c['k']}" style="--c:{c['c']};--t:{c['t']}">
<div class="sw"><h2>{E(c['name'])}</h2><p>{c['fin'].capitalize()} finish · seen on our {E(c['car'])}</p><p style="margin-top:10px">{E(c['note'])}</p>
<p style="margin-top:14px"><a href="past-works/#{c['k']}" style="color:inherit;font-weight:800;text-decoration:underline">All {E(c['name'].lower())} photos</a> · <a href="services/{c['svc']}/" style="color:inherit;text-decoration:underline">{E(SBY[c['svc']]['short'])}</a></p></div>
<div class="pics">{pics}</div></article>''')
    body = f'''<section class="sec"><div class="wrap">
{colour_rail()}
<div class="cat" style="margin-top:40px">{''.join(rows)}</div>
<p class="note" style="margin-top:22px">These are colours seen on our past jobs. Names describe what the photos show; the exact film name and code for each one is available on request, and we can source colours that are not shown here.</p>
</div></section>'''
    items = [{'@type': 'ListItem', 'position': i + 1, 'name': c['name'], 'url': SITE + 'colours/#' + c['k']} for i, c in enumerate(COLOURS)]
    page('colours/', 'Car Wrap Colour Catalogue | Wrapstar Autostyle',
         'Car wrap and colour PPF colours seen on our past jobs: satin black, matte green, stealth grey, ice grey, baby blue, bright yellow and more.',
         'Colour catalogue', body, crumbs=[('colours/', 'Colours')],
         lede='Ten colours seen on cars that left our studio, from satin black colour PPF to a bright yellow Tesla. Swipe through, then see each one up close.',
         schema=[{'@type': 'ItemList', 'name': 'Colours seen on Wrapstar Autostyle past jobs', 'itemListElement': items}])


def past_works():
    chips = '<button type="button" data-k="all" aria-pressed="true">All</button>' + ''.join(
        '<button type="button" data-k="%s" aria-pressed="false" style="--c:%s"><i></i>%s</button>' % (c['k'], c['c'], E(c['name'])) for c in COLOURS)
    groups = ''.join(f'''<section class="ggroup" id="{c['k']}" style="--c:{c['c']}"><h2><i></i>{E(c['name'])}</h2><p>{E(c['car'])} · {E(c['note'])}</p>
<div class="gal">{''.join('<button type="button" aria-label="Enlarge: %s">%s</button>' % (E(ALT[p]), img(p)) for p in c['pics'])}</div></section>''' for c in COLOURS)
    process = ''.join('<button type="button" aria-label="Enlarge: %s">%s</button>' % (E(ALT[p]), img(p)) for p in ['installer-ppf-bonnet', 'installer-window-film', 'installer-window-film-2', 'ppf-headlamp-install', 'mercedes-c-class-baby-blue-studio', 'window-film-mercedes'])
    body = f'''<section class="sec"><div class="wrap">
<div class="chips" role="group" aria-label="Filter by colour">{chips}</div>
{groups}
<section class="ggroup" id="in-the-studio"><h2>In the studio</h2><p>Film being fitted: trimming edges by hand, window film squeegeed from inside, clear film over a headlamp.</p><div class="gal">{process}</div></section>
<p class="note">More of our latest jobs are on <a href="{FB}" target="_blank" rel="noopener">Facebook</a> and <a href="{IG}" target="_blank" rel="noopener">Instagram</a>.</p>
</div></section>
<dialog class="lb" id="lb"><button class="x" type="button" aria-label="Close">✕</button><img src="" alt=""><p></p></dialog>'''
    page('past-works/', 'Car Wrap & PPF Past Works by Colour | Wrapstar Autostyle',
         'Photos of real car wraps, colour PPF and window film jobs from our Yishun studio, grouped by colour: Tesla, BYD, BMW, Mercedes-Benz and Mazda.',
         'Past works, grouped by colour', body, crumbs=[('past-works/', 'Past works')],
         lede='Real cars from our studio. Filter by colour, tap any photo to see it bigger.')


def services_index():
    body = '<section class="sec"><div class="wrap"><div class="svc-grid">%s</div></div></section>' % ''.join(svc_card(s) for s in SERVICES)
    page('services/', 'Car Wrap, PPF & Window Film Services | Wrapstar',
         'Colour change wrap, colour PPF, clear PPF, window film, dechrome, ceramic coating and polishing. One studio in Yishun, Singapore.',
         'Services', body, crumbs=[('services/', 'Services')],
         lede='Seven services, all done in our own studio at North Spring Bizhub, Yishun.')


SQ = {
    'colour-change-wrap': ('Why choose a colour change wrap?', 'How does a car wrap job work?', 'How much does a car wrap cost?',
        'A full car colour wrap at Wrapstar Autostyle starts from $1,588, our posted price. In August 2026 our National Day offer was $1,388 for hatchbacks and sedans, with SUVs and MPVs by quote. The final price depends on car size, the film and how much of the car is covered.'),
    'colour-ppf': ('Why choose colour PPF?', 'How does a colour PPF job work?', 'How much does colour PPF cost?',
        'Colour PPF costs more than a vinyl wrap because it is thick self-healing TPU. Our October 2026 promo was $2,788 nett for a Tesla Model 3 in satin black, and our August 2026 National Day offer was $2,588 for hatchbacks and sedans. Larger cars are priced by quote.'),
    'paint-protection-film': ('Why choose clear PPF?', 'How does a clear PPF job work?', 'How much does clear PPF cost?',
        'Our August 2026 National Day offer for full clear PPF was $2,188 for hatchbacks and sedans. Front-only coverage is quoted separately, and headlight PPF (one pair) comes free in our $628 nett car care bundle. The final price depends on the car, the film and the coverage you choose.'),
    'window-film': ('Why choose solar window film?', 'How does a window film job work?', 'How much does window tint cost?',
        'Our nano ceramic solar film opened at $358 (usual price $428) with a 7-year warranty, removal of old film and installation included. In August 2026 our LTA compliant tint for hatchbacks and sedans was $388. Bigger cars and extra panels such as a glass roof are priced by quote.'),
    'ceramic-coating': ('Why choose ceramic coating?', 'How does a ceramic coating job work?', 'How much does ceramic coating cost?',
        'Our car care bundle was posted at $628 nett (usual price $950). It covers a polish and ceramic coating, LTA compliant window film and free headlight PPF (one pair), with terms and limited availability. Ceramic coating on its own is priced by quote, based on your car size and paint condition.'),
    'polishing': ('Why polish your car?', 'How does a polishing job work?', 'How much does car polishing cost?',
        'Polishing is part of our car care bundle, posted at $628 nett (usual price $950), which also covers ceramic coating, LTA compliant window film and free headlight PPF (one pair). Polishing on its own is priced by quote, because it depends on your car size and how worn the paint is.'),
    'dechrome': ('Why dechrome your car?', 'How does a dechrome job work?', 'How much does dechrome cost?',
        'Dechrome is priced by quote, because the cost depends on how many chrome parts your car has: window trims, grille, badges, roof rails or exhaust tips. Send us a photo of your car on WhatsApp and we reply with a price for the parts you want blacked out.'),
}


FILM_STEPS = [('Send a photo', 'WhatsApp us your car model and a photo, with the colour or film you have in mind.'),
              ('Get a quote', 'We reply with the film options and a price for your car.'),
              ('Drop the car', 'Bring it to our studio at North Spring Bizhub, Yishun, on the agreed day.'),
              ('Collect and check', 'We walk you round the finished car, and you can come back for a check if anything bubbles or lifts.')]
CARE_STEPS = [('Send a photo', 'WhatsApp us your car model and a photo of the paint.'),
              ('Get a quote', 'We reply with a price for your car, or for the car care bundle.'),
              ('Drop the car', 'Bring it to our studio at North Spring Bizhub, Yishun, on the agreed day.'),
              ('Collect', 'We walk you round the finished car and tell you how to wash it.')]


def service_page(s):
    care = s['slug'] in ('ceramic-coating', 'polishing')
    pre_cols = ''.join(ccard(CBY[k]) for k in s['colours'])
    offers = ''.join('<div class="offer"><b>%s</b> · %s</div>' % (E(a), E(b)) for a, b in s['offers'])
    pts = '<ul>%s</ul>' % ''.join('<li><b>%s</b> %s</li>' % (E(a), E(b)) for a, b in s['points'])
    gallery = []
    for k in s['colours']:
        gallery += CBY[k]['pics'][:1]
    gal = '<div class="pgrid">%s</div>' % ''.join(img(p) for p in gallery[:3])
    rel = [a for a in ARTICLES if a['svc'] == s['slug']][:2] or ARTICLES[:2]
    others = ''.join('<li><a href="services/%s/">%s</a></li>' % (o['slug'], E(o['short'])) for o in SERVICES if o is not s)
    body = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="cols">
<div class="prose">
<figure class="pimg">{img(s['photo'], eager=True)}</figure>
<h2>What is {E(s['short'].lower())}?</h2>
<p class="ans">{E(s['answer'])}</p>
<h2>{E(SQ[s['slug']][0])}</h2>
{pts}
<h2>{E(SQ[s['slug']][1])}</h2>
<p>Four steps, all arranged on WhatsApp, at our studio in North Spring Bizhub, Yishun.</p>
{steps(CARE_STEPS if care else FILM_STEPS)}
<h2>{E(SQ[s['slug']][2])}</h2>
<p class="ans">{E(SQ[s['slug']][3])}</p>
<p>These are offers we have posted on our Facebook page, with their dates. WhatsApp us for today\'s price.</p>
{offers}
<h2>{'Gloss finishes on our past jobs' if care else 'Colours seen on our past jobs'}</h2>
{gal}
<p><a href="colours/">See the full colour catalogue</a> or <a href="past-works/">all past works</a>.</p>
<h2>{E(s['short'])} questions</h2>
{faq_html(s['faq'])}
</div>
<aside class="side">
<div class="box box-y"><h3>Get a quote</h3><p>Send your car model and the look you want. We reply on WhatsApp.</p>{wa_btn('WhatsApp ' + WA_SHOW, s['short'].lower() + '.', 'btn')}</div>
<div class="box"><h3>Other services</h3><ul>{others}</ul></div>
<div class="box"><h3>Guides</h3><ul>{''.join('<li><a href="articles/%s/">%s</a></li>' % (a['slug'], E(a['h1'])) for a in rel)}</ul></div>
</aside>
</div></div></section>
<section class="sec sec-alt" style="padding-top:56px"><div class="wrap"><div class="sec-head"><div><h2>{'Gloss colours on our past jobs' if care else 'Colours for ' + E(s['short'].lower())}</h2></div><a class="more" href="colours/">All colours →</a></div>
<div class="glide" data-speed="0.04">{pre_cols}</div></div></section>'''
    sch = [{'@type': 'Service', 'name': s['short'], 'serviceType': s['short'], 'description': s['answer'], 'provider': {'@id': SITE + '#business'},
            'areaServed': 'Singapore', 'url': SITE + 'services/%s/' % s['slug']}, faq_schema(s['faq'])]
    page('services/%s/' % s['slug'], s['title'], s['desc'], s['h1'], body, crumbs=[('services/', 'Services'), ('services/%s/' % s['slug'], s['short'])],
         lede=s['lede'], schema=sch, preload=s['photo'])


PRICE_FAQ = [
    ('Is colour PPF more expensive than a vinyl wrap?', 'Yes. Our posted wrap price starts from $1,588, while our recent colour PPF offers were $2,588 (August 2026, hatchbacks and sedans) and $2,788 nett for a Tesla Model 3 (October 2026). Colour PPF is thicker TPU film that also absorbs stone chips.'),
    ('Do SUVs cost more to wrap?', 'Usually, yes. SUVs and MPVs have more panels to cover, so they take more film and more time. Our National Day offers in August 2026 were for hatchbacks and sedans, with SUVs and MPVs priced by quote.'),
    ('How do I get an exact price?', 'WhatsApp 9754 1833 with your car model, a photo, and the colour or film you want. We reply with the film options and a price for your car.'),
]


def prices():
    rows = ''.join('<tr><td><a href="services/%s/">%s</a></td><td>%s</td></tr>' % (s['slug'], E(s['short']), '<br>'.join('<b>%s</b> %s' % (E(a), E(b)) for a, b in s['offers'])) for s in SERVICES)
    body = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="cols"><div class="prose">
<h2>How much does a car wrap cost in Singapore?</h2>
<p class="ans">A full car colour wrap at Wrapstar Autostyle starts from $1,588 (our posted price). Colour PPF, clear PPF, window film and dechrome depend on the car and the film. The offers below were posted on our Facebook page, with their dates.</p>
<table><tr><th>Service</th><th>Posted price or offer</th></tr>{rows}</table>
<h2>Car care bundle</h2>
<div class="offer"><b>$628 nett</b> (usual price $950) · polish and ceramic coating, LTA compliant window film, and free headlight PPF (one pair). Terms and limited availability apply.</div>
<h2>What changes the price of a wrap or PPF?</h2>
<ul><li><b>Car size.</b> Hatchbacks and sedans cost less than SUVs and MPVs.</li>
<li><b>Film.</b> Vinyl, colour PPF and clear PPF are different materials at different prices.</li>
<li><b>Coverage.</b> Full car, front only, door shuts, roof, trims.</li>
<li><b>Paint condition.</b> Chips or old repairs may need attention before film goes on.</li></ul>
<p>Promotions change. WhatsApp us your car model for today\'s price.</p>
<h2>Price questions</h2>
{faq_html(PRICE_FAQ)}
</div><aside class="side"><div class="box box-y"><h3>Today\'s price</h3><p>Send your car model and the service you want.</p>{wa_btn('WhatsApp ' + WA_SHOW, 'a price.', 'btn')}</div></aside></div></div></section>'''
    page('prices/', 'Car Wrap Prices Singapore | Wrapstar Autostyle',
         'Car wrap prices in Singapore: from $1,588 (our posted price). Dated offers on colour PPF, clear PPF and window film, and how to get a quote.',
         'Car wrap prices in Singapore, plus PPF', body, crumbs=[('prices/', 'Prices')], schema=[faq_schema(PRICE_FAQ)],
         lede='Posted prices and recent offers, with dates, so you know what to expect before you ask.')


def articles_index():
    body = '<section class="sec"><div class="wrap"><div class="agrid">%s</div></div></section>' % ''.join(acard(a) for a in ARTICLES)
    page('articles/', 'Car Wrap, PPF & Tint Guides | Wrapstar Autostyle',
         'Plain guides on car wraps, colour PPF, window tint rules and film care in Singapore, from the Wrapstar Autostyle studio in Yishun.',
         'Guides', body, crumbs=[('articles/', 'Guides')], lede='Straight answers to the questions owners ask us most.')


def render_blocks(blocks):
    out = []
    for kind, val in blocks:
        if kind == 'h2':
            out.append('<h2>%s</h2>' % E(val))
        elif kind == 'ans':
            out.append('<p class="ans">%s</p>' % E(val))
        elif kind == 'p':
            out.append('<p>%s</p>' % E(val))
        elif kind == 'raw':  # paragraph that is already HTML (editorial in-body link), added 19 Oct 2026
            out.append('<p>%s</p>' % val)
        elif kind == 'ul':
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in val))
        elif kind == 'ol':
            out.append('<ol>%s</ol>' % ''.join('<li>%s</li>' % E(x) for x in val))
        elif kind == 'table':
            head, rows = val[0], val[1:]
            out.append('<table><tr>%s</tr>%s</table>' % (''.join('<th>%s</th>' % E(h) for h in head),
                                                        ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % E(c) for c in r) for r in rows)))
    return ''.join(out)


def article_page(a):
    s = SBY[a['svc']]
    src = ''
    if 'tint' in a['slug'] or 'glass' in a['slug']:
        src = '<p class="note">Sources: <a href="%s" target="_blank" rel="noopener">Ministry of Transport, 7 April 2026</a>; <a href="%s" target="_blank" rel="noopener">OneMotoring, vehicle modifications</a> (both read 17 October 2026).</p>' % (MOT, OM_MOD)
    others = ''.join('<li><a href="articles/%s/">%s</a></li>' % (o['slug'], E(o['h1'])) for o in ARTICLES if o is not a)
    body = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="cols"><article class="prose">
<figure class="pimg">{img(a['photo'], eager=True)}</figure>
<p class="note">By {NAME} · {E(fmt_date(a['date']))}</p>
{render_blocks(a['body'])}
<h2>Questions</h2>
{faq_html(a['faq'])}
<p>Related service: <a href="services/{s['slug']}/">{E(s['short'])}</a>.</p>
{src}
</article>
<aside class="side"><div class="box box-y"><h3>{E(s['short'])}</h3><p>{E(s['gist'])}</p>{wa_btn('WhatsApp ' + WA_SHOW, s['short'].lower() + '.', 'btn')}</div>
<div class="box"><h3>More guides</h3><ul>{others}</ul></div></aside>
</div></div></section>'''
    sch = [{'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': a['date'], 'dateModified': a['date'],
            'image': IMG + a['photo'] + '.webp', 'author': {'@type': 'Organization', 'name': NAME, 'url': SITE},
            'publisher': {'@id': SITE + '#business'}, 'mainEntityOfPage': SITE + 'articles/%s/' % a['slug']}, faq_schema(a['faq'])]
    page('articles/%s/' % a['slug'], a['title'], a['desc'], a['h1'], body, crumbs=[('articles/', 'Guides'), ('articles/%s/' % a['slug'], a['title'].split(':')[0])],
         schema=sch, preload=a['photo'])


def fmt_date(d):
    y, m, dd = d.split('-')
    return '%d %s %s' % (int(dd), ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][int(m) - 1], y)


def about():
    body = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="cols"><div class="prose">
<figure class="pimg">{img('mercedes-c-class-baby-blue-studio', eager=True)}</figure>
<h2>Who is Wrapstar Autostyle?</h2>
<p class="ans">Wrapstar Autostyle is a car wrap and film studio in Yishun, Singapore. We do colour change wraps, colour PPF, clear paint protection film, window film, dechrome, polishing and ceramic coating, at 9 Yishun Industrial Street 1, #01-82, North Spring Bizhub, in the same unit as our sister business Star Performance Motor.</p>
<h2>What do we stand for?</h2>
<p>Our tagline is "for cars that deserve more". A wrap should look like it came from the factory: clean edges, tidy seams, no bubbles. We ask owners to come back after a job so we can check the film, because the finish is what people see every day.</p>
<h2>What is our sister business?</h2>
<p><a href="{SISTER}" target="_blank" rel="noopener">Star Performance Motor</a> is a used car dealer in the same unit. Buy, sell or trade in your car there, and give it a new colour or protection here, in one visit.</p>
<h2>Business details</h2>
<table>
<tr><th>Name</th><td>{NAME}</td></tr>
<tr><th>Registered</th><td>Sole proprietorship, UEN {UEN}, registered 3 November 2025 (ACRA)</td></tr>
<tr><th>Address</th><td>{', '.join(ADDR)}</td></tr>
<tr><th>Opening hours</th><td>{HOURS}</td></tr>
<tr><th>Google</th><td><a href="{GBP}" target="_blank" rel="noopener">{GRATING}</a></td></tr>
<tr><th>WhatsApp</th><td><a href="{E(wa_url())}" target="_blank" rel="noopener">+65 {WA_SHOW}</a></td></tr>
<tr><th>Services</th><td>Colour change wrap, colour PPF, clear PPF, window film, dechrome, polishing, ceramic coating</td></tr>
<tr><th>Social</th><td><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></td></tr>
</table>
</div><aside class="side"><div class="box box-y"><h3>Come and see</h3><p>WhatsApp before you come down so we can show you finished cars and film samples.</p>{wa_btn('WhatsApp ' + WA_SHOW, 'a visit.', 'btn')}</div></aside></div></div></section>'''
    page('about/', 'About Wrapstar Autostyle | Car Wrap Studio, Yishun',
         'Wrapstar Autostyle is a car wrap, PPF and window film studio at North Spring Bizhub, Yishun, sister business of Star Performance Motor. UEN 53513245W.',
         'About Wrapstar Autostyle', body, crumbs=[('about/', 'About')], lede='A car wrap and film studio in Yishun, for cars that deserve more.')


def contact():
    opts = ''.join('<option>%s</option>' % E(s['short']) for s in SERVICES) + '<option>Not sure yet</option>'
    cols = ''.join('<option>%s</option>' % E(c['name']) for c in COLOURS) + '<option>Something else</option>'
    body = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="duo">
<div class="box"><h2 style="font-size:1.6rem">Ask for a quote</h2><p>Fill this in and it opens WhatsApp with your message ready to send.</p>
<form class="form" id="enquiry" data-wa="{WA_NUM}">
<label>Service<select name="s">{opts}</select></label>
<label>Your car (make, model, year)<input name="c" autocomplete="off" placeholder="e.g. Tesla Model Y 2025"></label>
<label>Colour or film<select name="k"><option value="">Choose a colour</option>{cols}</select></label>
<label>Your name<input name="n" autocomplete="name"></label>
<label>Anything else<textarea name="x" placeholder="Full car, front only, trims..."></textarea></label>
<button class="btn btn-wa" type="submit">{WA_SVG}<span>Send on WhatsApp</span></button>
</form></div>
<div><div class="box" style="margin-bottom:16px"><h2 style="font-size:1.6rem">Find us</h2>
<p><b>{NAME}</b><br>{'<br>'.join(ADDR)}</p>
<p>WhatsApp or call <a href="tel:{TEL}">+65 {WA_SHOW}</a><br>Same unit as <a href="{SISTER}" target="_blank" rel="noopener">Star Performance Motor</a></p>
<p><b>Open {HOURS}</b></p>
<p><a href="{MAP}" target="_blank" rel="noopener">Open in Google Maps</a> · <a href="{GBP}" target="_blank" rel="noopener">{GRATING}</a></p></div>
<iframe class="map" src="{E(MAP_EMBED)}" loading="lazy" title="Map to Wrapstar Autostyle, North Spring Bizhub, Yishun" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></div></section>'''
    page('contact/', 'Contact Wrapstar Autostyle | WhatsApp 9754 1833',
         'WhatsApp Wrapstar Autostyle on 9754 1833 for a car wrap, PPF or window film quote. 9 Yishun Industrial Street 1 #01-82, Singapore 768163.',
         'Contact us', body, crumbs=[('contact/', 'Contact')], lede='The fastest way to a quote is WhatsApp: send your car model and the look you want.', cta=False)


def privacy():
    body = f'''<section class="sec" style="padding-top:40px"><div class="wrap"><div class="prose">
<p>This website does not use tracking cookies and does not collect personal data by itself. The quote form only prepares a WhatsApp message on your own phone; nothing is sent to us until you press send in WhatsApp.</p>
<p>When you contact us on WhatsApp or by phone, we use your name, number and car details only to reply, quote and do the job you ask for, in line with Singapore's Personal Data Protection Act (PDPA). We do not sell your data.</p>
<p>To ask about or delete the data we hold about you, WhatsApp us on +65 {WA_SHOW}.</p>
<p class="note">Updated {fmt_date('2026-10-17')}.</p></div></div></section>'''
    page('privacy/', 'Privacy | Wrapstar Autostyle', 'How Wrapstar Autostyle handles personal data under the PDPA.', 'Privacy', body, crumbs=[('privacy/', 'Privacy')], cta=False)


# ------------------------------------------------------------------------------------------------
# Render
# ------------------------------------------------------------------------------------------------
def shell(path, p, robots_meta=''):
    pre = '../' * path.count('/')
    url = SITE + path

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'], 'inLanguage': 'en-SG',
                                 'dateModified': LASTMOD.get(path, UPDATED), 'about': {'@id': SITE + '#business'}, 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = '<section class="phero"><div class="wrap">%s<h1>%s</h1>%s</div></section>' % (crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = fix('<section class="sec" style="padding-top:0"><div class="wrap"><div class="band"><div><h2>Ready for a new look?</h2><p>WhatsApp your car model and the colour you want. We reply with film options and a price.</p></div><div class="cta-row" style="margin:0">%s<a class="btn" href="colours/">Browse colours</a></div></div></div></section>' % wa_btn('WhatsApp ' + WA_SHOW))
    title = E(p['title'])
    preload = '<link rel="preload" as="image" href="%s%s.webp" fetchpriority="high">' % (IMG, p['preload']) if p['preload'] else ''
    body = fix(p['body'])
    brand = '<a class="brand" href="%s" aria-label="%s, home page"><img src="%slogo-wide.webp" alt="%s: %s" width="400" height="99"></a>' % (pre or './', NAME, IMG, NAME, TAGLINE)
    svc_links = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, s['slug'], E(s['short'])) for s in SERVICES)
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
{robots_meta or '<meta name="robots" content="index,follow,max-image-preview:large">\n'}<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#070708">
<link rel="canonical" href="{url}">
{preload}
<meta property="og:type" content="{'article' if path.startswith('articles/') and path != 'articles/' else 'website'}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{IMG}share/home.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{IMG}share/home.jpg">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{IMG}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,100..125,400..900;1,100..125,700..900&display=swap">
<link rel="stylesheet" href="{pre}ws.css?v={V}">
<script src="{pre}ws.js?v={V}" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('WhatsApp', cls='btn btn-wa hdr-cta')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<main id="main">
{head_hero}
{body}
{band}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}<p>Car colour wraps, colour and clear PPF, window film, dechrome, polishing and ceramic coating in Yishun, Singapore. Sister business of <a href="{SISTER}" target="_blank" rel="noopener">Star Performance Motor</a>.</p></div>
<div><h3>Services</h3><ul>{svc_links}</ul></div>
<div><h3>Explore</h3><ul><li><a href="{pre}colours/">Colour catalogue</a></li><li><a href="{pre}past-works/">Past works</a></li><li><a href="{pre}prices/">Prices</a></li><li><a href="{pre}articles/">Guides</a></li><li><a href="{pre}about/">About</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp +65 {WA_SHOW}</a></li>
<li>{'<br>'.join(ADDR)}</li>
<li>Open {HOURS}</li>
<li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
<li><a href="{pre}contact/">Contact</a> · <a href="{pre}privacy/">Privacy</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{NAME} · UEN {UEN}</span><span>© 2026 {NAME} · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp Wrapstar Autostyle on {WA_SHOW}">{WA_SVG}<span>WhatsApp</span></a><a class="dock-c" href="{pre}colours/">Colours</a></div>
</body>
</html>
'''


def write(rel, text):
    fp = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)


# ---- 2 Nov 2026 SEO pass: hub intros + FAQs (facts from this site only) ----
SERVICES_FAQ = [
    ('Which services does Wrapstar Autostyle offer?', 'Seven: colour change wrap, colour PPF, clear PPF, window film, dechrome, ceramic coating and polishing, all done in our own studio at 9 Yishun Industrial Street 1, #01-82 North Spring Bizhub, Singapore 768163.'),
    ('How much do your services cost?', 'Posted prices include car wraps from $1,588 and a $628 nett car care bundle (polish and ceramic coating plus LTA compliant window film and free headlight PPF). See the prices page for the dated offers; anything else is by quote on WhatsApp +65 %s.' % WA_SHOW),
    ('When is the studio open?', '%s. WhatsApp +65 %s to book a time.' % (HOURS, WA_SHOW)),
]
ARTICLES_FAQ = [
    ('What do the Wrapstar Autostyle guides cover?', 'Car wraps, colour PPF versus vinyl, how long a wrap lasts, satin, matte or gloss finishes, window film and tint rules in Singapore, ceramic window film, and how to care for a wrapped car.'),
    ('Do the guides give the Singapore window tint rules?', 'Yes. The window tint guide sets out the rules and names its source with a date. Check the official source for the latest figures, because rules can change.'),
    ('Can I ask about my own car?', 'Yes. WhatsApp +65 %s with your car model and what you want done, and we reply with options.' % WA_SHOW),
]
SERVICES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Wraps, PPF and window film in Yishun</h2>'
    '<p>Wrapstar Autostyle is a car wrap and paint protection studio at North Spring Bizhub, Yishun. We change the colour of your car with gloss, satin or matte vinyl that comes off when you want it to, add stone-chip protection with clear or colour PPF, and cut heat with LTA compliant nano ceramic window film.</p>'
    '<p>We also dechrome shiny trims and badges, polish paint to bring back gloss, and apply ceramic coating for a harder, glossier layer that is easier to wash. Pick the service below to see how it works, or check the prices page for our dated offers. WhatsApp +65 %s with your car model and we will reply with options.</p></div></section>') % WA_SHOW
ARTICLES_INTRO = ('<section class="sec"><div class="wrap narrow prose"><h2>Car wrap, PPF and tint guides for Singapore</h2>'
    '<p>These guides answer the questions car owners ask us in the studio: whether to wrap or respray, colour PPF versus vinyl, how long a wrap lasts, which finish to choose, how to prepare your car, and how to look after a wrapped car.</p>'
    '<p>You will also find window film and tint rules for Singapore, ceramic versus dyed film, dechrome, wrapping a leased or company car, and what to ask before booking. Every guide ends with questions and answers. WhatsApp us on +65 %s if yours is not covered.</p></div></section>') % WA_SHOW
def _hub(path, intro, faqs, h2):
    p = PAGES[path]
    p['body'] = intro + p['body'] + '<section class="sec"><div class="wrap narrow"><div class="sec-head"><h2>%s</h2></div>%s</div></section>' % (h2, faq_html(faqs))
    p['schema'] = list(p.get('schema') or []) + [faq_schema(faqs)]


def main():
    home(); colours(); past_works(); services_index()
    for s in SERVICES:
        service_page(s)
    prices(); articles_index()
    for a in ARTICLES:
        article_page(a)
    about(); contact(); privacy()
    _hub('services/', SERVICES_INTRO, SERVICES_FAQ, 'Questions about our services')
    _hub('articles/', ARTICLES_INTRO, ARTICLES_FAQ, 'Questions about our guides')
    for path, p in PAGES.items():
        write(path + 'index.html', shell(path, p))
    nf = dict(title='Page not found | Wrapstar Autostyle', desc='This page does not exist.', h1='Page not found',
              body='<section class="sec"><div class="wrap"><p>That page is not here. Try the <a href="colours/">colour catalogue</a>, <a href="past-works/">past works</a> or <a href="services/">services</a>.</p></div></section>',
              crumbs=None, lede='', schema=[], hero=True, cta=True, preload=None)
    # 404 is served at any depth, so it uses absolute links
    global SITE
    write('404.html', shell('', nf, '<meta name="robots" content="noindex">\n').replace('href="colours/"', 'href="%scolours/"' % SITE)
          .replace('href="past-works/"', 'href="%spast-works/"' % SITE).replace('href="services/"', 'href="%sservices/"' % SITE)
          .replace('href="ws.css', 'href="%sws.css' % SITE).replace('src="ws.js', 'src="%sws.js' % SITE).replace('href="favicon', 'href="%sfavicon' % SITE)
          .replace('href="site.webmanifest', 'href="%ssite.webmanifest' % SITE).replace('href="./"', 'href="%s"' % SITE)
          .replace('<link rel="canonical" href="%s">\n' % SITE, ''))
    # sitemap, robots, llms, manifest
    sm = ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, path, LASTMOD.get(path, UPDATED)) for path in PAGES)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % sm)
    bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
    write('robots.txt', 'User-agent: *\nAllow: /\n\n' + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'Sitemap: https://%s/sitemap.xml\n' % DOMAIN)
    write('site.webmanifest', json.dumps({'name': NAME, 'short_name': 'Wrapstar', 'start_url': './', 'display': 'standalone', 'background_color': '#070708', 'theme_color': '#070708',
                                          'icons': [{'src': IMG + 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': IMG + 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}))
    llms = ['# %s' % NAME, '', '> Car wrap and film studio in Yishun, Singapore: colour change wraps, colour PPF, clear paint protection film, window film and dechrome, plus polishing and ceramic coating. "%s".' % TAGLINE, '',
            '- Address: 9 Yishun Industrial Street 1, #01-82, North Spring Bizhub, Singapore 768163 (same unit as sister business Star Performance Motor, %s)' % SISTER,
            '- WhatsApp / phone: +65 %s' % WA_SHOW, '- Opening hours: %s (Google Business Profile, 18 October 2026)' % HOURS, '- Google rating: %s' % GRATING, '- Registered: sole proprietorship, UEN %s, 3 November 2025 (ACRA)' % UEN,
            '- Facebook: %s (%s)' % (FB, REC), '- Instagram: %s' % IG, '- Google Business Profile: %s' % GBP, '- Map: %s (latitude %s, longitude %s)' % (MAP, GEO[0], GEO[1]),
            '- Prices (posted by the business): full car colour wrap from $1,588; Tesla Model 3 satin black colour PPF $2,788 nett (October 2026 promo); nano ceramic solar film $358 opening offer (usual $428), 93%-96% IR rejection, 7-year warranty.',
            '- Window tint rule followed: at least 70% visible light front windscreen and front side windows, 25% rear (MOT, 7 April 2026).', '', '## Pages', '']
    llms += ['- [%s](%s%s): %s' % (p['h1'], SITE, path, p['desc']) for path, p in PAGES.items()]
    write('llms.txt', '\n'.join(llms) + '\n')
    print('pages', len(PAGES))


if __name__ == '__main__':
    main()

"""New Zen Werkz Pte Ltd: builds every page into site/ (python3 build.py).

Facts used (15 Oct 2026), and where they came from:
- Name "New Zen Werkz Pte Ltd" (Google Business Profile, workshop banner); formerly "Zen Werkz LLP"
  (older banner at the entrance, sgCarMart directory listing at the same address).
- Address Blk 3 Kaki Bukit Road 1 #03-04 Eunos Technolink, Singapore 415935 (ACRA record via sgpbusiness.com; Blk 3 Eunos Technolink
  is postal code 415935. sgCarMart and Car Kakis list 415395, a typo to fix in those listings).
- ACRA (sgpbusiness.com): Zen Werkz LLP T16LL1390E registered 19 Jul 2016, struck off 2022; New Zen Werkz Pte Ltd 201900125K
  incorporated 2 Jan 2019, live, SSIC 95301 repair and maintenance of motor vehicles. Both at this address.
- Car Kakis lists Mon-Sat 10:00-17:00 for Zen Werkz LLP (old listing; not shown on the site until Edwin confirms).
- Phone 6742 8117 (sgCarMart, Car Kakis).
- Services: car servicing, oil change, troubleshooting, battery (sgCarMart tags); engine and gearbox teardown,
  brake work on Mercedes-Benz, Bentley, Hummer and Mazda cars (Edwin's workshop photos). Liqui Moly banner in the workshop.
- Google Business Profile services list (Edwin, 15 Oct 2026): air & cabin filters, air conditioning, engine diagnostic, battery,
  brakes, oil change, steering & suspension, tyres, transmission. (Also lists car loan and rental cars: not on the site.)
- WhatsApp +65 8678 1878 (Edwin, 6 Nov 2026; was 8656 3133) and no social media. Hours and 5-star reviews from Google screenshots.
Not claimed anywhere: prices, years in business, warranties, review quotes, brands we have not seen, opening hours.
Things Edwin must confirm are listed in CONFIRM and in README.md.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

SLUG = 'new-zen-werkz'
DOMAIN = 'newzenwerkz.com.sg'        # Edwin confirmed 6 Nov 2026
LIVE = True
INDEXNOW_KEY = 'ea97d7cd7c1340c781fcd248d8d2c2ec'
NOINDEX = not LIVE                   # the preview is a sales demo for a prospect: keep it out of Google until go-live
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
IMG_CDN = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@75eacffeb8f9648ebe763ac148440bc67db62f68/site-assets/new-zen-werkz/'
IMG = IMG_CDN                        # at go-live copy site/img/ to the client host and set IMG = SITE + 'img/'
UPDATED = '2026-11-06'

NAME = 'New Zen Werkz'
LEGAL = 'New Zen Werkz Pte Ltd'
FORMER = 'Zen Werkz LLP'          # Edwin 6 Nov 2026: never show on the site
UEN = '201900125K'
TEL, TEL_SHOW = '+6567428117', '6742 8117'
WA_NUM, WA_SHOW = '6586781878', '+65 8678 1878'       # WhatsApp changed by Edwin, 6 Nov 2026 (was 8656 3133)
WA_MSG = 'Hi New Zen Werkz, I found your website. I would like to ask about my car.'
# Opening hours from the Google Business Profile (Edwin's screenshot, 15 Oct 2026)
HOURS = [('Monday to Friday', '9:30am to 7pm'), ('Saturday', '9:30am to 4pm'), ('Sunday', 'Closed')]
HOURS_LD = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '09:30', 'closes': '19:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Saturday', 'opens': '09:30', 'closes': '16:00'}]
# Real 5-star Google reviews (Edwin's screenshots, 15 Oct 2026). Quoted word for word, trimmed only where Google cut them off.
REVIEWS = [
    ('Robin T.', 'Local Guide', 'My go-to place to service my Merc. Ah Mun is knowledgeable and his prices are reasonable too. Highly Recommended.'),
    ('Hong Li M.', 'Local Guide', 'I have known him for 13 years. Along the way, I only trust the service he provides for my car. He is enthusiastic, serious in work, has first-class skills, is humorous, and has reasonable prices.'),
    ('Daniel G.', '', 'Boss Mun very experienced and friendly person. Workmanship also very good. Price very reasonable.'),
    ('Prinz135', '', 'The prices are reasonable, workers are knowledgeable and know what they are doing.'),
    ('Shahie J.', 'Local Guide', 'Known Ah Mun for 6 over years and no doubt that he\u2019s prices are reasonable, very helpful and importantly, he values friendship. Followed him from his previous workshop...'),
]
ADDR = ['Blk 3 Kaki Bukit Road 1', '#03-04 Eunos Technolink', 'Singapore 415935']
STREET, POSTAL = 'Blk 3 Kaki Bukit Road 1, #03-04 Eunos Technolink', '415935'
MAPQ = 'New+Zen+Werkz+Pte+Ltd+3+Kaki+Bukit+Road+1+Eunos+Technolink+Singapore+415935'
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
SGCARMART = 'https://www.sgcarmart.com/directory/'

CONFIRM = [
    'Domain name for go-live',
    'The workshop uses Liqui Moly oils and additives (seen on the banner)',
    'Findings and a quote are given before any work starts',
    'Email address (no social media for now, per Edwin)',
]

AREAS = [
    ('Right next to us', ['Kaki Bukit', 'Eunos', 'Ubi', 'Kembangan', 'Bedok North', 'Bedok Reservoir', 'Chai Chee']),
    ('East', ['Bedok', 'Tampines', 'Simei', 'Pasir Ris', 'Upper Changi', 'Siglap', 'Upper East Coast']),
    ('South', ['Paya Lebar', 'Geylang', 'Joo Chiat', 'Katong', 'Marine Parade']),
    ('West and north', ['MacPherson', 'Aljunied', 'Kallang', 'Hougang', 'Kovan', 'Serangoon', 'Sengkang']),
]
AREA_NAMES = [a for _, g in AREAS for a in g]
AREA_LD = [{'@type': 'Place', 'name': a + ', Singapore'} for a in AREA_NAMES]
NAV = [('services/', 'Services'), ('areas/', 'Areas'), ('articles/', 'Articles'), ('about/', 'About'), ('contact/', 'Contact')]
E = html.escape

PHOTOS = {  # name: (width, height, alt)
    'workshop-lineup': (1400, 933, 'A Bentley, a Mercedes-Benz E-Class and a Hummer with bonnets open inside the New Zen Werkz workshop at Eunos Technolink'),
    'engine-teardown': (1200, 800, 'A New Zen Werkz mechanic stripping down an engine beside a Mercedes-Benz with its gearbox removed'),
    'engine-gearbox': (1100, 710, 'Engine block, crankshaft and automatic gearbox laid out on the workshop floor during a rebuild'),
    'engine-closeup': (1000, 645, 'Mechanic checking the timing gears on an engine being rebuilt'),
    'workshop-entrance': (1000, 714, 'Cars waiting at the entrance to the workshop at Blk 3 #03-04, Eunos Technolink'),
    'mercedes-hummer': (1100, 720, 'Mercedes-Benz and Hummer under repair, with the New Zen Werkz Pte Ltd banner on the wall'),
    'brake-work': (822, 548, 'New Zen Werkz mechanic inspecting the brake disc and caliper on a front wheel'),
}


def img(name, sm=False, cls='', eager=False, sizes=None):
    w, h, alt = PHOTOS[name]
    src = IMG + name + ('-sm' if sm else '') + '.webp'
    if sm:
        h, w = round(h * 560 / w), 560
    return '<img%s src="%s" alt="%s" width="%d" height="%d"%s>' % (
        ' class="%s"' % cls if cls else '', src, E(alt), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"')


PHONE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')
PIN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>')


def call_btn(label='Call %s' % TEL_SHOW, cls='btn btn-red'):
    return '<a class="%s" href="tel:%s">%s<span>%s</span></a>' % (cls, TEL, PHONE_SVG, E(label))


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 '
          '11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>')


def wa_url(text=WA_MSG):
    from urllib.parse import quote
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(text))


def wa_btn(label='WhatsApp us', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url()), WA_SVG, E(label))


def hours_html():
    return '<dl class="hours">%s</dl>' % ''.join('<dt>%s</dt><dd>%s</dd>' % (E(d), E(t)) for d, t in HOURS)


def reviews_html(items):
    stars = '<span class="stars" aria-label="5 out of 5 stars">★★★★★</span>'
    return '<div class="reviews">%s</div>' % ''.join(
        '<figure class="review">%s<blockquote>%s</blockquote><figcaption><span>%s</span>%s · <a href="%s" target="_blank" rel="noopener">Google review</a></figcaption></figure>'
        % (stars, E(q), E(initials(n)), (' · <span>%s</span>' % E(t)) if t else '', MAP) for n, t, q in items)


def initials(name):
    # Rule (Edwin, 5 Nov 2026): reviewer names as initials only, linked to the source reviews.
    return ''.join(w[0].upper() + '.' for w in re.findall(r'[A-Za-z]+', name)) if ' ' in name else name[0].upper() + '.'


def map_btn(label='Get directions', cls='btn btn-ghost'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, MAP, PIN_SVG, E(label))


MARK = ('<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#14171c"/>'
        '<path d="M10 12h20L10 28h20" fill="none" stroke="#e1251b" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/></svg>')

PAGES = {}
# Home only: cover the page until the intro splash (in nzw.js) takes over; self-clears after 3.5s if the script fails.
INTRO = ('<script>try{if(!sessionStorage.getItem("nzw-intro")&&!matchMedia("(prefers-reduced-motion: reduce)").matches){var h=document.documentElement;h.classList.add("intro");'
         'setTimeout(function(){h.classList.remove("intro")},3500)}}catch(e){}</script>\n')


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, photo=None, kind='WebPage', top='', date=None):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [],
                       hero=hero, cta=cta, photo=photo, kind=kind, top=top, date=date)


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


# ----------------------------------------------------------------------------------------------
# Services
# ----------------------------------------------------------------------------------------------
SERVICES = [
    dict(slug='car-servicing', short='Car servicing & oil change', photo='engine-closeup',
         gist='Scheduled servicing, engine oil and filter changes, and fluid checks to your car maker\'s schedule.',
         title='Car Servicing & Oil Change in Kaki Bukit | New Zen Werkz',
         desc='Car servicing and engine oil change at Eunos Technolink, Kaki Bukit. New Zen Werkz services continental and Japanese cars to the maker\'s schedule. Call 6742 8117.',
         h1='Car servicing and oil change',
         lede='Regular servicing is the cheapest way to keep a car reliable. We follow your car maker\'s schedule and tell you what is due now and what can wait.',
         sections=[
             ('What a service covers', [
                 'A routine service starts with the engine oil and oil filter, then works through the items your car maker lists for that interval: air filter, cabin filter, spark plugs, brake fluid, coolant, gearbox oil where the maker specifies it, and a check of belts, hoses, tyres, brakes, suspension, lights and battery.',
                 'Many European cars run on a service indicator rather than a fixed sticker, alternating between a smaller and a larger service. We read what the car is asking for and reset the indicator once the work is done.']),
             ('The right oil for your engine', [
                 'Modern engines are built around a specific oil approval, not just a viscosity. A Mercedes-Benz may need an oil approved to MB 229.5 or 229.51, a Volkswagen group car VW 504 00 or 507 00, and so on. Using the right specification protects turbochargers, timing chains and particulate filters.',
                 'Our workshop carries Liqui Moly oils and additives. We match the oil to the approval printed in your owner\'s manual.']),
             ('Why Singapore driving counts as hard use', [
                 'Short trips, stop-start traffic and high temperatures are the conditions most owner\'s manuals describe as severe service. If most of your driving looks like that, a shorter oil change interval is usually worth it. We will tell you honestly what your car and your driving actually need.']),
         ],
         faqs=[
             ('How often should I service my car in Singapore?', 'Follow the time or distance interval in your owner\'s manual, whichever comes first. Many manuals treat short trips and stop-start traffic in hot weather as severe use, which calls for shorter oil change intervals.'),
             ('Do you service continental cars?', 'Yes. Mercedes-Benz and other continental cars are a regular part of our work, alongside Japanese and other makes.'),
             ('Which engine oil do you use?', 'We use Liqui Moly oils and match the oil to the approval your car maker specifies, such as MB 229.5 for many Mercedes-Benz engines.'),
             ('How much does a car service cost?', 'It depends on the car and which service is due. Call 6742 8117 with your car model and mileage and we will give you a quote.'),
         ]),
    dict(slug='engine-repair', short='Engine repair & overhaul', photo='engine-teardown',
         gist='From oil leaks and misfires to a full engine strip-down and rebuild, done in our own workshop.',
         title='Engine Repair & Overhaul Singapore | New Zen Werkz, Kaki Bukit',
         desc='Engine repair and engine overhaul in Singapore. New Zen Werkz strips, inspects and rebuilds engines in-house at Eunos Technolink, Kaki Bukit. Call 6742 8117.',
         h1='Engine repair and engine overhaul',
         lede='When an engine needs more than a part swap, we take it out, strip it down and rebuild it properly. The photos on this page are real jobs from our workshop floor.',
         sections=[
             ('Engine problems we fix', [
                 'Oil leaks from gaskets and seals, overheating, misfires, rough idle, loss of power, unusual knocking or rattling, smoke from the exhaust, timing chain noise, and engines that use more oil than they should.',
                 'Many of these start small. A leaking gasket or a noisy timing chain is far cheaper to fix early than after it has damaged something else.']),
             ('What an engine overhaul involves', [
                 'An overhaul means removing the engine, stripping it to the block and measuring the parts that wear: cylinder bores, pistons and rings, crankshaft journals and bearings, camshafts, valves and the timing set.',
                 'Worn parts are replaced or machined, the engine is rebuilt with new gaskets and seals, and it goes back in the car to be tested. Because every part is inspected, an overhaul tells you exactly what state the engine was in.']),
             ('Repair, overhaul or replace?', [
                 'Not every tired engine needs a full rebuild. We diagnose first, explain what we found, and lay out the options: a targeted repair, an overhaul, or a replacement engine where that makes more sense for the car\'s age and value.']),
         ],
         faqs=[
             ('What are the signs my engine needs an overhaul?', 'Heavy oil consumption, blue smoke, low compression, knocking from the bottom end and metal in the oil are common signs. A diagnosis confirms whether a repair or a full overhaul is needed.'),
             ('Do you overhaul engines in-house?', 'Yes. Engines are removed, stripped, inspected and rebuilt in our own workshop at Eunos Technolink.'),
             ('Is it worth overhauling an engine instead of replacing it?', 'Often, if the block and crankshaft are sound and the car is worth keeping. We inspect first and explain the options before any work starts.'),
         ]),
    dict(slug='gearbox-repair', short='Gearbox & transmission repair', photo='engine-gearbox',
         gist='Diagnosis and repair of automatic gearboxes: slipping, harsh shifts, leaks and limp mode.',
         title='Gearbox & Transmission Repair Singapore | New Zen Werkz',
         desc='Automatic gearbox and transmission repair in Singapore. Slipping, jerky shifts, leaks or limp mode? New Zen Werkz, Eunos Technolink, Kaki Bukit. Call 6742 8117.',
         h1='Gearbox and transmission repair',
         lede='Automatic gearboxes give warning before they fail. If yours is slipping, jerking or stuck in limp mode, get it checked before a small fault becomes a big bill.',
         sections=[
             ('Signs your gearbox needs attention', [
                 'Slipping (revs rise but the car does not pull), harsh or delayed gear changes, a jolt when selecting Drive or Reverse, whining or humming that changes with speed, a burning smell, red or brown fluid under the car, or a warning message and the car locked in one gear (limp mode).']),
             ('How we work on gearboxes', [
                 'We start with a scan of the gearbox control unit and a road test, then check the fluid level and condition. Some faults are electrical, such as a sensor or a valve body solenoid, and can be fixed without removing the gearbox.',
                 'When the fault is mechanical, the gearbox comes out of the car, as in the photos here, so the clutch packs, torque converter, seals and valve body can be inspected and repaired.']),
             ('Gearbox fluid', [
                 'Many modern automatics are sold as "filled for life", but the fluid still ages, especially in hot stop-start traffic. A fluid and filter service at a sensible interval is one of the best ways to protect an expensive gearbox. Always use the fluid your car maker specifies.']),
         ],
         faqs=[
             ('Why does my car jerk when changing gear?', 'Common causes are old or low gearbox fluid, a faulty solenoid or valve body, worn clutch packs, or software that needs adaptation. A scan and road test narrows it down.'),
             ('Can I keep driving in limp mode?', 'Only gently and only to a workshop. Limp mode protects the gearbox from further damage; driving on as normal can turn a small fault into a full rebuild.'),
             ('Do automatic gearboxes need fluid changes?', 'Yes, even many sold as "filled for life" benefit from a fluid and filter change, particularly in hot stop-start driving. Use the fluid your car maker specifies.'),
         ]),
    dict(slug='brake-repair', short='Brake repair', photo='brake-work',
         gist='Brake pads, discs, calipers and brake fluid, checked and replaced when they are due.',
         title='Brake Repair, Pads & Discs Singapore | New Zen Werkz, Kaki Bukit',
         desc='Brake pad and disc replacement, caliper repair and brake fluid change in Singapore. New Zen Werkz, Eunos Technolink, Kaki Bukit. Call 6742 8117.',
         h1='Brake repair: pads, discs and fluid',
         lede='Brakes are the one system you cannot afford to leave. We inspect the whole braking system, not just the pads.',
         sections=[
             ('Warning signs', [
                 'Squealing when you brake (many pads have a wear indicator that does this on purpose), grinding metal on metal, a vibration through the pedal or steering wheel, the car pulling to one side, a soft or sinking pedal, or a brake warning light on the dashboard.']),
             ('What we check and replace', [
                 'Pad thickness and wear pattern, disc thickness and run-out, calipers and slide pins, brake hoses and lines, the handbrake or electronic parking brake, and the condition of the brake fluid.',
                 'Pads and discs are usually replaced in axle sets so the car brakes evenly. Many cars with electronic parking brakes need a scan tool to retract the rear calipers, which we have.']),
             ('Brake fluid', [
                 'Brake fluid absorbs moisture over time, which lowers its boiling point. Many car makers specify a change every two years. Check your service booklet, or ask us to test it.']),
         ],
         faqs=[
             ('How do I know my brake pads need replacing?', 'Squealing, a pad warning light, longer stopping distances or visibly thin pads are the usual signs. We measure the pads and discs and tell you how much life is left.'),
             ('Do I need to change discs with the pads?', 'Not always. Discs are replaced when they are below the minimum thickness stamped on them, or are scored or warped.'),
             ('How often should brake fluid be changed?', 'Many car makers specify every two years because the fluid absorbs moisture. Your service booklet gives the interval for your car.'),
         ]),
    dict(slug='car-diagnostics', short='Diagnostics & troubleshooting', photo='mercedes-hummer',
         gist='Warning lights, strange noises and faults that come and go, traced to the real cause.',
         title='Car Diagnostics & Check Engine Light Singapore | New Zen Werkz',
         desc='Check engine light on? New Zen Werkz scans, troubleshoots and traces car faults to the real cause at Eunos Technolink, Kaki Bukit. Call 6742 8117.',
         h1='Car diagnostics and troubleshooting',
         lede='A fault code tells you where to start looking, not what to replace. We trace faults to their cause so you only pay for the repair you need.',
         sections=[
             ('What we diagnose', [
                 'Engine warning lights, gearbox faults, ABS and airbag lights, electrical problems, starting and charging faults, rough running, overheating, noises and vibrations, and faults that only appear now and then.']),
             ('How diagnosis works', [
                 'We read the fault codes and live data from the car\'s control units, then test the suspect parts directly: wiring, sensors, pressures and signals. A code such as "lean mixture" can come from a vacuum leak, a sensor, the fuel pump or an injector. Testing tells us which one.',
                 'Once the cause is confirmed, we explain it in plain language and give you the options before any repair starts.']),
             ('Check engine light: steady or flashing?', [
                 'A steady light means a fault has been stored; get it checked soon. A flashing light usually means the engine is misfiring badly enough to damage the catalytic converter, so reduce speed, avoid hard acceleration and have the car looked at straight away.']),
         ],
         faqs=[
             ('What should I do when the check engine light comes on?', 'If it is steady, book a check soon. If it is flashing, drive gently and get the car to a workshop as soon as possible, because a flashing light usually means a serious misfire.'),
             ('Can a scan tool tell exactly what is wrong?', 'It tells us which system logged a fault and gives us data to work with. The faulty part is confirmed by testing, which avoids replacing parts on a guess.'),
             ('Do you troubleshoot intermittent faults?', 'Yes. Faults that come and go take more testing, so tell us when it happens, how often, and what the car was doing at the time.'),
         ]),
    dict(slug='car-battery-replacement', short='Car battery replacement', photo='workshop-entrance',
         gist='Battery testing and replacement, including start-stop cars that need the new battery registered.',
         title='Car Battery Replacement in Kaki Bukit | New Zen Werkz',
         desc='Car battery testing and replacement at Eunos Technolink, Kaki Bukit, including AGM and EFB batteries for start-stop cars. New Zen Werkz. Call 6742 8117.',
         h1='Car battery testing and replacement',
         lede='Singapore\'s heat is hard on car batteries. We test the battery and the charging system so you know whether it is the battery, the alternator or something draining it.',
         sections=[
             ('Signs of a weak battery', [
                 'Slow cranking when you start the car, a battery or charging warning light, electrical gremlins such as flickering lights or warning messages, the start-stop system no longer switching the engine off, or a battery more than a few years old.']),
             ('Testing first', [
                 'A flat battery is not always a bad battery. We test the battery under load, check the alternator\'s charging output, and look for anything draining the battery while the car is parked.']),
             ('Start-stop and European cars', [
                 'Cars with start-stop need an AGM or EFB battery, not a standard one. Many European cars also need the new battery registered or coded to the car so the charging system treats it correctly. We fit the right type and do the registration where the car needs it.']),
         ],
         faqs=[
             ('How long does a car battery last in Singapore?', 'Heat shortens battery life, so batteries here often need replacing sooner than in cooler countries. A load test tells you how much life yours has left.'),
             ('Does my car need a special battery?', 'If your car has start-stop it needs an AGM or EFB battery. Your existing battery\'s label or your owner\'s manual shows the type.'),
             ('Why does a new battery need to be registered?', 'Many European cars adjust how they charge the battery based on its type and age. Registering the new battery tells the car to charge it correctly.'),
         ]),
    dict(slug='continental-car-repair', short='Continental car repair', photo='workshop-lineup',
         gist='Mercedes-Benz, Bentley and other continental cars repaired and serviced alongside Japanese and American makes.',
         title='Continental Car Repair & Servicing Singapore | New Zen Werkz',
         desc='Continental car workshop in Singapore for Mercedes-Benz, Bentley and more. Servicing, engine, gearbox and brake repair at Eunos Technolink, Kaki Bukit. Call 6742 8117.',
         h1='Continental car repair and servicing',
         lede='A Bentley, a Mercedes-Benz E-Class and a Hummer side by side on our workshop floor. Continental cars are an everyday part of our work.',
         sections=[
             ('Cars we work on', [
                 'Our workshop regularly has Mercedes-Benz and Bentley cars in for repair, alongside Japanese makes such as Mazda and American vehicles such as the Hummer. If you are not sure whether we handle your car, call 6742 8117 and ask.']),
             ('Why continental cars need a specialist approach', [
                 'European cars rely heavily on electronics and maker-specific procedures: oil approvals, gearbox fluid specifications, battery registration, electronic parking brakes and service indicator resets. Getting those details right is what keeps the car reliable.',
                 'We follow the maker\'s procedures and specifications for servicing and repairs, from routine oil changes to engine and gearbox rebuilds.']),
             ('An alternative to the dealer', [
                 'Servicing at an independent workshop is a choice many owners make once their car is out of warranty, or for repairs a dealer would only solve by replacing a whole assembly. We explain what we find and give you the options before any work starts.']),
         ],
         faqs=[
             ('Do you repair Mercedes-Benz cars?', 'Yes. Mercedes-Benz cars are a regular part of our servicing and repair work, including engine and gearbox jobs.'),
             ('Can an independent workshop service my continental car?', 'Yes, as long as the correct parts, oils and procedures for your car are used. Check your warranty terms if the car is still under the maker\'s warranty.'),
             ('Do you work on Japanese cars too?', 'Yes. Japanese makes such as Mazda are serviced and repaired here too.'),
         ]),
    dict(slug='aircon-repair', short='Car aircon repair', photo='mercedes-hummer',
         gist='Weak or warm aircon checked for leaks, gas level, compressor, fan and filter problems.',
         title='Car Aircon Repair & Servicing in Kaki Bukit | New Zen Werkz',
         desc='Car aircon not cold? New Zen Werkz checks gas, leaks, compressor, fans and cabin filters at Eunos Technolink, Kaki Bukit. WhatsApp +65 8678 1878 or call 6742 8117.',
         h1='Car aircon repair and servicing',
         lede='In Singapore the aircon works every single drive. When it stops blowing cold, we find out why instead of just topping up the gas.',
         sections=[
             ('Common aircon problems', [
                 'Air that is cool but not cold, cold only when driving, warm air at idle, a musty smell from the vents, weak airflow, a clicking or grinding noise when the aircon is switched on, or water dripping inside the car.']),
             ('How we check it', [
                 'We check the system pressures and refrigerant level, look for leaks at the hoses, joints, condenser and evaporator, and test the compressor, its clutch or control valve, and the cooling fans. Refrigerant does not get used up; if the level is low, there is a leak, and topping up without fixing it only buys time.',
                 'Weak airflow and smells are often a clogged cabin filter or a dirty evaporator, which are simple to sort out.']),
             ('Cabin and air filters', [
                 'The cabin filter cleans the air you breathe inside the car, and the engine air filter protects the engine. Both clog faster in dusty, humid conditions. We replace them at your service intervals, or sooner if they need it.']),
         ],
         faqs=[
             ('Why is my car aircon not cold?', 'The usual causes are a refrigerant leak, a failing compressor or compressor clutch, a cooling fan that is not running, or a blocked condenser. Testing the system pressures shows which.'),
             ('Does car aircon gas need topping up regularly?', 'No. The system is sealed, so a low gas level means there is a leak somewhere. The leak should be found and fixed.'),
             ('Why does my car aircon smell?', 'A musty smell usually comes from a dirty cabin filter or mould on the evaporator. Replacing the filter and cleaning the system usually cures it.'),
         ]),
    dict(slug='steering-suspension-repair', short='Steering & suspension', photo='workshop-lineup',
         gist='Knocks, clunks, pulling and a bouncy ride traced to shocks, bushes, joints or steering parts.',
         title='Steering & Suspension Repair Singapore | New Zen Werkz, Kaki Bukit',
         desc='Steering and suspension repair in Singapore: shock absorbers, bushings, ball joints, links and steering racks. New Zen Werkz, Eunos Technolink. WhatsApp +65 8678 1878.',
         h1='Steering and suspension repair',
         lede='Worn suspension makes a car noisy, tiring to drive and slower to stop. We find the worn part and replace what actually needs replacing.',
         sections=[
             ('Signs of worn suspension or steering', [
                 'Knocking or clunking over bumps, the car bouncing or floating after a hump, pulling to one side, a vibrating or off-centre steering wheel, uneven tyre wear, a heavy or vague feel to the steering, or a leaking shock absorber.']),
             ('What we check', [
                 'Shock absorbers and springs, control arm bushings, ball joints, anti-roll bar links, tie rod ends, the steering rack and its boots, and wheel bearings. On cars with air suspension we also check the air struts and compressor.',
                 'Many continental cars use a lot of rubber bushings that wear with age and heat. Replacing the right ones restores the car\'s ride without guessing.']),
             ('After the repair', [
                 'Steering and suspension work changes how the wheels sit, so a wheel alignment afterwards keeps the car driving straight and stops the tyres wearing unevenly.']),
         ],
         faqs=[
             ('What causes a clunking noise over bumps?', 'Worn anti-roll bar links, control arm bushings, ball joints or shock absorber mounts are the usual causes. Lifting the car and checking each part finds the culprit.'),
             ('How do I know my shock absorbers are worn?', 'The car keeps bouncing after a bump, dives under braking, leans more in corners, or a shock absorber is leaking oil. Uneven tyre wear can also be a sign.'),
             ('Do I need a wheel alignment after suspension repair?', 'Usually yes. Replacing steering or suspension parts can change the wheel angles, and an alignment keeps the car straight and protects the tyres.'),
         ]),
    dict(slug='tyre-replacement', short='Tyres', photo='brake-work',
         gist='Tyre checks and replacement, with a look at what caused uneven wear.',
         title='Tyre Replacement & Tyre Checks in Kaki Bukit | New Zen Werkz',
         desc='Tyre replacement and tyre checks at Eunos Technolink, Kaki Bukit: tread depth, uneven wear, punctures and tyre age. New Zen Werkz. WhatsApp +65 8678 1878.',
         h1='Tyre replacement and tyre checks',
         lede='Tyres are the only part of the car touching the road. We check them at every service and tell you honestly when they are due.',
         sections=[
             ('When tyres need replacing', [
                 'When the tread reaches the wear indicator bars moulded into the grooves, when there is a bulge or cut in the sidewall, when a puncture is too close to the shoulder to repair safely, or when the rubber is cracked with age. Check your tyres\' date code: rubber hardens over the years even if the tread looks fine.']),
             ('Uneven wear tells a story', [
                 'Wear on one edge often points to wheel alignment or worn suspension parts. Wear in the centre or on both edges points to tyre pressures. Fitting new tyres without fixing the cause means the new ones wear the same way, so we check the cause as well.']),
             ('Getting the right tyre', [
                 'Use the size, load index and speed rating your car maker specifies. Some cars use run-flat tyres or different sizes front and rear; we match what your car needs.']),
         ],
         faqs=[
             ('How do I know when my tyres need replacing?', 'Look for the tread wear indicator bars in the grooves. If the tread is level with them, or the sidewall has a bulge or cut, the tyre needs replacing.'),
             ('Why are my tyres wearing on one side?', 'One-sided wear is usually wheel alignment or worn suspension parts. It is worth fixing the cause before fitting new tyres.'),
             ('Can a punctured tyre be repaired?', 'Often, if the puncture is small and in the tread area. Punctures in the sidewall or shoulder, or tyres driven flat, should be replaced.'),
         ]),
]
SVC = {s['slug']: s for s in SERVICES}


def provider():
    return {'@id': SITE + '#business'}


def service_body(s):
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % E(p) for p in ps)) for h, ps in s['sections'])
    others = ''.join('<a class="mini" href="services/%s/">%s<span>%s</span></a>' % (o['slug'], img(o['photo'], sm=True), E(o['short']))
                     for o in SERVICES if o['slug'] != s['slug'])
    rel = [a for a in ARTICLES if s['slug'] in a['services']][:2]
    rel_html = ''
    if rel:
        rel_html = '<h2>Related articles</h2><ul class="rel">%s</ul>' % ''.join(
            '<li><a href="articles/%s/">%s</a></li>' % (a['slug'], E(a['h1'])) for a in rel)
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(s['photo'], eager=True)}</figure>
{secs}
<h2>Common questions</h2>
{faq_html(s['faqs'])}
{rel_html}
</article>
<aside class="side">
<div class="card sticky"><h2>Talk to the workshop</h2><p>Tell us your car model and what you have noticed. We will advise on the next step.</p>
{wa_btn()}{call_btn(cls='btn btn-ghost')}{map_btn()}
<p class="small">{'<br>'.join(ADDR)}</p></div>
</aside>
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Other services</h2></div><div class="minis">{others}</div></div></section>'''


# ----------------------------------------------------------------------------------------------
# Articles (general, verifiable car-care knowledge; no client claims beyond the facts above)
# ----------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='signs-your-automatic-gearbox-is-failing', photo='engine-gearbox', services=['gearbox-repair', 'continental-car-repair'],
         h1='7 signs your automatic gearbox needs attention',
         title='7 Signs Your Automatic Gearbox Is Failing (Singapore Guide) | New Zen Werkz',
         desc='Slipping, jerky shifts, limp mode or leaks? Seven warning signs of automatic gearbox trouble, what causes them and what to do next. A Singapore workshop guide.',
         answer='The most common signs of a failing automatic gearbox are slipping, harsh or delayed shifts, a jolt into Drive or Reverse, whining, a burning smell, red or brown fluid leaks and limp mode. Most start small, so a scan and fluid check early can prevent a full rebuild.',
         body=[
             ('1. Slipping', 'The engine revs rise but the car does not pick up speed to match, as if the gearbox briefly lost its grip. Slipping usually points to worn clutch packs inside the gearbox, low fluid, or a pressure problem in the valve body.'),
             ('2. Harsh or delayed gear changes', 'A thump between gears, or a pause before the next gear engages, often comes from old fluid, a sticking solenoid in the valve body, or adaptation values that need resetting. Software and fluid issues are the cheaper end of gearbox repair, which is why it pays to check early.'),
             ('3. A jolt when selecting Drive or Reverse', 'A clunk when you move the selector can be worn engine or gearbox mounts as well as an internal fault. A workshop can tell the two apart quickly.'),
             ('4. Whining, humming or buzzing', 'Noises that change with road speed can come from bearings, the torque converter or the final drive. Noises that change with engine speed point elsewhere. Note when the noise happens before you bring the car in.'),
             ('5. A burning smell', 'Overheated gearbox fluid has a sharp burnt smell. It means the fluid is breaking down and no longer protecting the gearbox properly. Stop driving hard and have it checked.'),
             ('6. Red or brown fluid under the car', 'Automatic gearbox fluid is usually red or amber when fresh and darkens with age. A leak lowers the fluid level, and a gearbox running low on fluid can slip and overheat. Seals and pan gaskets are common leak points and are usually straightforward to replace.'),
             ('7. Warning message and limp mode', 'If the gearbox detects a serious fault it may hold one gear to protect itself. Drive gently to a workshop. Carrying on as normal in limp mode can turn a sensor fault into internal damage.'),
             ('What to do next', 'Get the gearbox scanned and road tested, and have the fluid level and condition checked. Many problems turn out to be electrical or fluid-related and are fixed without removing the gearbox. When the fault is mechanical, the gearbox has to come out for inspection and repair.'),
         ]),
    dict(slug='check-engine-light-what-to-do', photo='mercedes-hummer', services=['car-diagnostics', 'engine-repair'],
         h1='Check engine light on? What it means and what to do',
         title='Check Engine Light On? What It Means & What To Do | New Zen Werkz',
         desc='What a steady or flashing check engine light means, common causes, whether you can keep driving, and why a fault code alone is not a diagnosis.',
         answer='A steady check engine light means the engine computer has stored a fault and the car should be checked soon. A flashing light usually means a severe misfire that can damage the catalytic converter, so drive gently and get the car to a workshop straight away.',
         body=[
             ('Steady light', 'The engine management system has found a fault and stored a code. The car may feel normal. It is usually safe to drive to a workshop, but do not ignore it for weeks: small faults such as a failing sensor can affect fuel use and emissions, and can hide a second fault that appears later.'),
             ('Flashing light', 'A flashing light typically means the engine is misfiring. Unburnt fuel can overheat and damage the catalytic converter, which is an expensive part. Ease off, avoid hard acceleration, and get the car checked as soon as possible.'),
             ('Common causes', 'Ignition coils and spark plugs, oxygen sensors, mass air flow sensors, vacuum or intake leaks, faulty thermostats, EGR and emissions faults, and on some cars a loose fuel cap. On turbocharged engines, boost leaks are a frequent cause too.'),
             ('Why the code is not the answer', 'A fault code says which reading was out of range, not which part failed. A "lean mixture" code, for example, can come from an air leak, a sensor, a weak fuel pump or a clogged injector. Testing the suspect parts is what separates a correct repair from replacing parts on a guess.'),
             ('What to tell your mechanic', 'When the light came on, whether it is steady or flashing, any change in how the car drives, sounds or smells, and whether it happened after refuelling or any recent work. These details save diagnosis time.'),
         ]),
    dict(slug='how-often-to-service-your-car-in-singapore', photo='engine-closeup', services=['car-servicing', 'continental-car-repair'],
         h1='How often should you service your car in Singapore?',
         title='How Often Should You Service Your Car in Singapore? | New Zen Werkz',
         desc='Service intervals explained for Singapore drivers: time vs mileage, why stop-start traffic and heat count as severe use, and choosing the right engine oil.',
         answer='Service your car at the time or distance interval in your owner\'s manual, whichever comes first. Singapore\'s short trips, stop-start traffic and heat match what many manuals call severe service, so a shorter oil change interval is often sensible.',
         body=[
             ('Time or distance, whichever comes first', 'Every owner\'s manual gives a service interval in both months and kilometres. Oil ages even when the car is not driven much, so a low-mileage car still needs servicing on time.'),
             ('Why Singapore driving is "severe"', 'Most manuals list conditions that call for a shorter schedule: frequent short trips, extended idling, stop-start traffic and high outside temperatures. Daily driving in Singapore ticks several of these boxes. If that describes your driving, follow the severe-service schedule or shorten the oil change interval.'),
             ('Service indicators on European cars', 'Many Mercedes-Benz, BMW and Volkswagen group cars calculate when the next service is due and show it on the dashboard, alternating between a smaller and a larger service. The indicator is a useful guide, but the hard-use conditions above still apply.'),
             ('Use the right oil, not just the right thickness', 'Modern engines need oil that meets the car maker\'s approval, for example MB 229.5 or 229.51 for many Mercedes-Benz engines, or VW 504 00 or 507 00 for many Volkswagen group engines. The approval is in your owner\'s manual and printed on the oil bottle.'),
             ('More than oil', 'A proper service also covers filters, brake fluid, coolant, spark plugs and a safety inspection at the intervals your maker sets. Keep the receipts: a complete service history helps when you sell the car.'),
         ]),
    dict(slug='brake-warning-signs', photo='brake-work', services=['brake-repair'],
         h1='Brake warning signs you should never ignore',
         title='Brake Warning Signs You Should Never Ignore | New Zen Werkz',
         desc='Squealing, grinding, pedal vibration, pulling or a soft pedal: what each brake warning sign means and when pads, discs or brake fluid need replacing.',
         answer='Get your brakes checked if you hear squealing or grinding, feel vibration through the pedal, the car pulls to one side, the pedal feels soft, or a brake warning light comes on. Each points to a different part of the braking system.',
         body=[
             ('Squealing', 'Many brake pads have a small metal wear indicator that squeals against the disc when the pad is getting thin. It is designed to get your attention. Some squeal also comes from glazed pads or missing anti-squeal shims.'),
             ('Grinding', 'Metal grinding usually means the pad material is gone and the backing plate is touching the disc. Stop driving if you can: braking is reduced and the discs are being damaged with every stop.'),
             ('Vibration through the pedal or steering', 'A pulsing pedal or shaking steering wheel under braking usually comes from uneven disc thickness. Discs are measured and replaced if they are below the minimum thickness stamped on them.'),
             ('Pulling to one side', 'A seized caliper or slide pin, a collapsed brake hose or contaminated pads can make one side brake harder than the other. This also wears tyres unevenly.'),
             ('Soft or sinking pedal', 'Air or moisture in the brake fluid, a leak, or a failing master cylinder can make the pedal feel spongy. Treat this as urgent.'),
             ('Brake fluid', 'Brake fluid absorbs moisture from the air, which lowers its boiling point and corrodes parts over time. Many car makers specify a change every two years; your service booklet gives the interval for your car.'),
         ]),
    dict(slug='engine-overhaul-explained', photo='engine-teardown', services=['engine-repair'],
         h1='Engine overhaul explained: what it involves and when it is worth it',
         title='Engine Overhaul Explained: What It Involves & When It Is Worth It | New Zen Werkz',
         desc='What happens during an engine overhaul, the signs an engine needs one, and how to decide between repair, overhaul and engine replacement.',
         answer='An engine overhaul means removing the engine, stripping it down, measuring the worn parts, and rebuilding it with new bearings, rings, gaskets and seals. It is worth it when the block and crankshaft are sound and the car is worth keeping.',
         body=[
             ('Signs an engine may need an overhaul', 'High oil consumption, blue smoke from the exhaust, low compression on one or more cylinders, knocking from the bottom of the engine, metal particles in the oil, or coolant and oil mixing. Each of these can have smaller causes too, which is why diagnosis comes first.'),
             ('What happens during an overhaul', 'The engine is removed and stripped to the bare block. The cylinder bores, pistons, rings, crankshaft, bearings, camshafts, valves and timing parts are cleaned, measured and checked against the maker\'s limits. Worn parts are replaced or machined, and the engine is reassembled with new gaskets and seals before going back in the car for testing.'),
             ('Overhaul or a smaller repair?', 'A leaking gasket, a stretched timing chain or a failed head gasket can often be fixed without a full rebuild. A full overhaul makes sense when wear is spread across the engine, or when the engine is already apart and the extra work costs little more.'),
             ('Overhaul or replacement engine?', 'Replacement can be quicker when a suitable engine is available, but its history is often unknown. An overhaul gives you an engine where every wearing part has been inspected. The right choice depends on the car\'s value, how long you plan to keep it, and parts availability.'),
             ('Questions to ask your workshop', 'What did the inspection find? Which parts will be replaced and which reused? How will the engine be tested afterwards? A good workshop explains this clearly before you agree to the work.'),
         ]),
    dict(slug='car-battery-signs-singapore', photo='workshop-entrance', services=['car-battery-replacement'],
         h1='Is your car battery dying? Signs, heat and start-stop batteries',
         title='Signs Your Car Battery Is Dying (Singapore) | New Zen Werkz',
         desc='Slow cranking, warning lights and start-stop that stops working: signs of a weak car battery, why heat shortens battery life, and AGM vs EFB batteries.',
         answer='Slow cranking, a battery warning light, electrical glitches and a start-stop system that no longer switches the engine off are the common signs of a weak battery. Heat shortens battery life, so batteries in Singapore often wear out sooner.',
         body=[
             ('Common signs', 'The engine turns over slowly before starting, the battery or charging light comes on, lights flicker or the car shows random warning messages, the start-stop system stops working, or the battery case looks swollen.'),
             ('Heat is the real enemy', 'High temperatures speed up the chemical reactions inside a battery and the loss of water from it. That is why batteries in hot climates tend to fail sooner than the same battery in a cool one, often with little warning.'),
             ('Battery or alternator?', 'A battery that keeps going flat may be fine and simply not being charged, or something may be draining it while the car is parked. A load test of the battery and a check of the alternator output tell you which.'),
             ('Start-stop cars need AGM or EFB batteries', 'Cars with start-stop restart the engine many times a day and need a battery built for it: AGM (absorbent glass mat) or EFB (enhanced flooded battery). Fitting a standard battery in their place shortens its life and can stop start-stop working.'),
             ('Battery registration', 'Many European cars adjust their charging to the battery\'s type and age. After a replacement, the new battery is registered or coded to the car with a scan tool so it is charged correctly.'),
         ]),
]
ART = {a['slug']: a for a in ARTICLES}


def article_body(a):
    secs = ''.join('<h2>%s</h2><p>%s</p>' % (E(h), E(p)) for h, p in a['body'])
    svc_links = ''.join('<a class="mini" href="services/%s/">%s<span>%s</span></a>' % (s, img(SVC[s]['photo'], sm=True), E(SVC[s]['short']))
                        for s in a['services'])
    more = ''.join('<li><a href="articles/%s/">%s</a></li>' % (o['slug'], E(o['h1'])) for o in ARTICLES if o['slug'] != a['slug'])[:4000]
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(a['photo'], eager=True)}</figure>
<p class="answer"><strong>Short answer:</strong> {E(a['answer'])}</p>
{secs}{('<h2>Common questions</h2>' + faq_html(a['faqs'])) if a.get('faqs') else ''}
<p class="byline">By the New Zen Werkz workshop team, Eunos Technolink, Singapore. Updated {art_mod(a)}. General guidance only: your owner's manual and a proper inspection come first.</p>
</article>
<aside class="side"><div class="card sticky"><h2>Need it checked?</h2><p>WhatsApp or call the workshop and tell us what you have noticed.</p>{wa_btn()}{call_btn(cls='btn btn-ghost')}{map_btn()}</div></aside>
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Related services</h2></div><div class="minis">{svc_links}</div>
<h2 style="margin-top:32px">More articles</h2><ul class="rel">{more}</ul></div></section>'''


# Each article keeps its own dates (Edwin 7 Nov 2026: no fake date bumps). Launch articles have no 'date' and use UPDATED.
def art_date(a):
    return a.get('date', UPDATED)


def art_mod(a):
    return a.get('updated', art_date(a))


def article_schema(a, path):
    return {'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': art_date(a), 'dateModified': art_mod(a),
            'image': IMG + a['photo'] + '.webp', 'mainEntityOfPage': SITE + path,
            'author': {'@type': 'Organization', 'name': LEGAL, '@id': SITE + '#business'}, 'publisher': {'@id': SITE + '#business'},
            'about': [SVC[s]['h1'] for s in a['services']]}


def article_card(a):
    return '<a class="acard" href="articles/%s/">%s<span><b>%s</b>%s</span></a>' % (a['slug'], img(a['photo'], sm=True), E(a['h1']), E(a['answer'][:120].rsplit(' ', 1)[0] + '...'))


# ----------------------------------------------------------------------------------------------
# Home
# ----------------------------------------------------------------------------------------------
FAQ_HOME = [
    ('Where is New Zen Werkz?', 'At Blk 3 Kaki Bukit Road 1, #03-04 Eunos Technolink, Singapore 415935, on the third floor of the Eunos Technolink building.'),
    ('What cars do you work on?', 'Continental cars such as Mercedes-Benz and Bentley are a regular part of our work, alongside Japanese makes such as Mazda and American vehicles.'),
    ('What are your opening hours?', 'Monday to Friday 9:30am to 7pm, Saturday 9:30am to 4pm, closed on Sunday. WhatsApp +65 8678 1878 or call 6742 8117 with your car model and what you have noticed.'),
]


def home_body():
    cards = ''.join(f'''<a class="scard" href="services/{s['slug']}/">{img(s['photo'], sm=True)}<span class="scard-t"><b>{E(s['short'])}</b><span>{E(s['gist'])}</span><em>More details →</em></span></a>'''
                    for s in SERVICES)
    gallery = ''.join('<figure>%s</figure>' % img(n, sm=True) for n in ('engine-teardown', 'brake-work', 'mercedes-hummer', 'engine-gearbox', 'workshop-entrance'))
    arts = ''.join(article_card(a) for a in ARTICLES[:3])
    return f'''<section class="hero">
<div class="hero-bg">{img('workshop-lineup', eager=True)}</div>
<div class="wrap hero-in">
<p class="eyebrow">Car workshop · Eunos Technolink, Kaki Bukit</p>
<h1>Car repair and servicing in Kaki Bukit, from routine oil changes to engine and gearbox rebuilds.</h1>
<p class="lede">New Zen Werkz is an independent car workshop for continental, Japanese and American cars. We diagnose properly, explain what we find, and do the work in our own workshop.</p>
{addr_line()}
<div class="cta-row">{wa_btn()}{call_btn()}{map_btn('Directions', 'btn btn-light')}</div>
</div></section>
<div class="facts"><div class="wrap">
<div><b>Workshop</b><span>Blk 3 Kaki Bukit Rd 1, #03-04</span></div>
<div><b>WhatsApp / Call</b><a href="{E(wa_url())}" target="_blank" rel="noopener">{WA_SHOW}</a> · <a href="tel:{TEL}">{TEL_SHOW}</a></div>
<div><b>Open</b><span>Mon–Fri 9:30–7 · Sat 9:30–4</span></div>
<div><b>Cars</b><span>Continental, Japanese, American</span></div>
</div></div>
<section class="sec" aria-labelledby="h-svc"><div class="wrap">
<div class="sec-head"><p class="eyebrow">What we do</p><h2 id="h-svc">Workshop services</h2><p>Pick a service for the details.</p></div>
<div class="scards">{cards}</div>
</div></section>
<section class="sec sec-dark" aria-labelledby="h-why"><div class="wrap split2">
<div><p class="eyebrow">Inside the workshop</p><h2 id="h-why">Real work, on our own floor.</h2>
<ul class="ticks">
<li><b>Engines and gearboxes rebuilt in-house.</b> We strip, inspect and rebuild, not just swap parts.</li>
<li><b>Continental cars are everyday work.</b> Mercedes-Benz and Bentley sit alongside Japanese and American makes.</li>
<li><b>Diagnosis before repair.</b> You hear what we found and your options before work starts.</li>
</ul>
<a class="btn btn-light" href="about/">About the workshop</a></div>
<div class="gallery">{gallery}</div>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-rev"><div class="wrap">
<div class="sec-head"><p class="eyebrow">From Google reviews</p><h2 id="h-rev">What customers say</h2></div>
{reviews_html(REVIEWS[:3])}
<p style="margin-top:18px"><a class="btn btn-ghost" href="{MAP}" target="_blank" rel="noopener">Read all reviews on Google</a></p>
</div></section>
<section class="sec" aria-labelledby="h-area"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Near you</p><h2 id="h-area">Your car workshop in the East, within 8 km of Kaki Bukit</h2>
<p>Drivers come to us from {', '.join(AREA_NAMES[:12])} and more.</p></div>
{local_links_html()}
<p style="margin-top:16px"><a class="btn btn-ghost" href="areas/">See all areas we serve</a></p>
</div></section>
<section class="sec" aria-labelledby="h-art"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Car care articles</p><h2 id="h-art">Know before you drive in</h2></div>
<div class="acards">{arts}</div>
<p style="margin-top:20px"><a class="btn btn-ghost" href="articles/">All articles</a></p>
</div></section>
<section class="sec" aria-labelledby="h-faq"><div class="wrap narrow">
<div class="sec-head"><h2 id="h-faq">Quick answers</h2></div>
{faq_html(FAQ_HOME)}
</div></section>'''


def services_index():
    cards = ''.join(f'''<a class="scard" href="services/{s['slug']}/">{img(s['photo'], sm=True)}<span class="scard-t"><b>{E(s['short'])}</b><span>{E(s['gist'])}</span><em>More details →</em></span></a>'''
                    for s in SERVICES)
    return '<section class="sec"><div class="wrap"><div class="scards">%s</div></div></section>' % cards


def articles_index():
    return '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(article_card(a) for a in ARTICLES)


def about_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img('mercedes-hummer', eager=True)}</figure>
<p>New Zen Werkz Pte Ltd is an independent car repair and servicing workshop at Eunos Technolink in Kaki Bukit, Singapore. New Zen Werkz Pte Ltd was incorporated in January 2019. The workshop is at Blk 3 Kaki Bukit Road 1, #03-04.</p>
<h2>What we do</h2>
<p>Routine servicing and oil changes, diagnostics, brake work and battery replacement, through to the jobs many workshops send elsewhere: taking engines and automatic gearboxes out of the car, stripping them down and rebuilding them.</p>
<p>On any given day the workshop floor might have a Bentley, a Mercedes-Benz E-Class and a Hummer side by side, with a Mazda in the next bay. The photos on this site are from our own workshop.</p>
<h2>How we work</h2>
<p>Customers know the boss as Ah Mun, and several have followed him for years. We find the cause before we fix anything. You hear what we found in plain language, with the options and a quote, before any repair starts.</p>
<h2>What customers say</h2>
{reviews_html(REVIEWS)}
<figure>{img('workshop-entrance')}<figcaption>The entrance to the workshop at Blk 3, #03-04, Eunos Technolink.</figcaption></figure>
<h2>Company details</h2>
<p>{LEGAL} (UEN {UEN}), incorporated 2 January 2019. Registered activity: repair and maintenance of motor vehicles (SSIC 95301).<br>{'<br>'.join(ADDR)}<br>Tel: <a href="tel:{TEL}">{TEL_SHOW}</a> · WhatsApp: <a href="{E(wa_url())}" target="_blank" rel="noopener">{WA_SHOW}</a></p>
</article>
<aside class="side"><div class="card sticky"><h2>Visit or call</h2><p>{'<br>'.join(ADDR)}</p>{hours_html()}{wa_btn()}{call_btn(cls='btn btn-ghost')}{map_btn()}</div></aside>
</div></section>'''


def contact_body():
    return f'''<section class="sec"><div class="wrap split">
<div class="prose">
<h2>WhatsApp or call the workshop</h2>
<p class="big"><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></p>
<p class="big2"><a href="tel:{TEL}">Call {TEL_SHOW}</a></p>
<p>Tell us your car model, the year, and what you have noticed. Photos or a short video of the problem help too. We will advise on the next step and give you a quote.</p>
<h2>Address</h2>
<p>{LEGAL}<br>{'<br>'.join(ADDR)}</p>
<p>The workshop is on the third floor of Eunos Technolink, unit #03-04. Look for the New Zen Werkz banner.</p>
<h2>Opening hours</h2>
{hours_html()}
<p class="small">Public holiday hours may differ. WhatsApp us before you come down.</p>
<div class="cta-row">{wa_btn()}{call_btn(cls='btn btn-ghost')}{map_btn()}</div>
</div>
<div class="mapbox"><iframe title="Map to New Zen Werkz at Eunos Technolink" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''


def areas_body():
    groups = ''.join('<h2>%s</h2><p>%s.</p>' % (E(t), E(', '.join(g))) for t, g in AREAS)
    svc = ''.join('<li><a href="services/%s/">%s</a></li>' % (s['slug'], E(s['short'])) for s in SERVICES)
    return f'''<section class="sec"><div class="wrap split">
<div class="prose">
<p>New Zen Werkz is at Blk 3 Kaki Bukit Road 1, #03-04 Eunos Technolink, Singapore 415935. All the areas below are within about 8 km of the workshop.</p>
<h2>Local guides: route, distance and time</h2>
<p>Real driving routes to the workshop from the main estates around us.</p>
{local_links_html()}
{groups}
<h2>Before you drive over</h2>
<p>WhatsApp {WA_SHOW} or call {TEL_SHOW} with your car model and what you have noticed, so we can tell you what to expect. The workshop is on the third floor of Eunos Technolink, unit #03-04.</p>
<div class="cta-row">{wa_btn()}{call_btn(cls='btn btn-ghost')}{map_btn()}</div>
<h2>Services at the workshop</h2>
<ul>{svc}</ul>
</div>
<div class="mapbox"><iframe title="Map to New Zen Werkz at Eunos Technolink" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''


from local_pages import LOCAL  # noqa: E402  (8 km local area pages, 6 Nov 2026)
SVC = {s['slug']: s for s in SERVICES}


def ref_btn(btn, ref):
    """Same button, with a data-ref so the Controller tap log shows which page and position was tapped."""
    return btn.replace('<a ', '<a data-ref="%s" ' % ref, 1)


def local_cta(l, pos):
    return '<div class="cta-row">%s%s</div>' % (ref_btn(call_btn(), 'area-%s-%s-call' % (l['slug'], pos)),
                                               ref_btn(wa_btn('WhatsApp %s' % WA_SHOW), 'area-%s-%s-whatsapp' % (l['slug'], pos)))


def addr_line(extra=''):
    return ('<p class="addr-line">%s<span><a href="%s" target="_blank" rel="noopener">Blk 3 Kaki Bukit Road 1, #03-04 Eunos Technolink, Singapore %s</a>%s</span></p>'
            % (PIN_SVG, MAP, POSTAL, extra))


def local_top(l):
    return addr_line('<span>%s km from %s</span>' % (l['km'], E(l['start']))) + local_cta(l, 'top')


def local_dir_url(l):
    from urllib.parse import quote
    return 'https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s' % (quote(l['start'] + ', Singapore'), MAPQ)


def local_body(l):
    steps = ''.join('<li>%s</li>' % E(x) for x in l['steps'])
    marks = ''.join('<li>%s</li>' % E(x) for x in l['landmarks'])
    focus = ''.join('<a class="mini" href="services/%s/">%s<span>%s</span></a>' % (k, img(SVC[k]['photo'], sm=True), E(SVC[k]['short'])) for k in l['focus'])
    rest = ', '.join('<a href="services/%s/">%s</a>' % (s['slug'], E(s['short'].lower() if i else s['short'])) for i, s in enumerate(x for x in SERVICES if x['slug'] not in l['focus']))
    others = ''.join('<li><a href="areas/%s/">%s</a></li>' % (o['slug'], E(o['name'])) for o in LOCAL if o['slug'] != l['slug'])
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
{''.join('<p>%s</p>' % E(x) for x in l['intro'])}
<h2>Getting here from {E(l['name'])}</h2>
<div class="route">
<div class="route-stats"><div><b>{l['km']} km</b><span>by road</span></div><div><b>about {l['mins']} min</b><span>outside peak hours</span></div></div>
<p class="small">From {E(l['start'])}. Route and time from OpenStreetMap routing (free-flowing traffic); peak-hour traffic takes longer.</p>
<ol class="steps">{steps}</ol>
<p><a class="btn btn-ghost" href="{E(local_dir_url(l))}" target="_blank" rel="noopener">{PIN_SVG}<span>Open this route in Google Maps</span></a></p>
</div>
<h2>Landmarks near the start of your drive</h2>
<ul>{marks}</ul>
<h2>Services for {E(l['name'])} drivers</h2>
<p>{E(l['focus_note'])}</p>
<div class="minis">{focus}</div>
<p>We also handle {rest}.</p>
<h2>Questions from {E(l['name'])} drivers</h2>
{faq_html(l['faqs'])}
<h2>Other areas near the workshop</h2>
<ul class="area-links">{others}</ul>
</article>
<aside class="side"><div class="card sticky"><h2>Visit or call</h2><p>{'<br>'.join(ADDR)}</p>{hours_html()}{ref_btn(wa_btn(), 'area-%s-side-whatsapp' % l['slug'])}{ref_btn(call_btn(cls='btn btn-ghost'), 'area-%s-side-call' % l['slug'])}{map_btn()}</div></aside>
</div></section>
<section class="sec"><div class="wrap"><div class="band"><div><h2>Driving over from {E(l['name'])}?</h2>
<p>Call or WhatsApp first and tell us your car model and what you have noticed.</p></div>{local_cta(l, 'end')}</div></div></section>'''


def local_links_html(cls='chips'):
    return '<ul class="%s">%s</ul>' % (cls, ''.join('<li><a href="areas/%s/">%s</a></li>' % (l['slug'], E(l['name'])) for l in LOCAL))


def business_schema():
    return {'@type': 'AutoRepair', '@id': SITE + '#business', 'name': LEGAL, 'alternateName': [NAME],
            'url': SITE, 'telephone': TEL, 'openingHoursSpecification': HOURS_LD,
            'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': '+' + WA_NUM}, 'image': [IMG + n + '.webp' for n in ('workshop-lineup', 'engine-teardown', 'brake-work')],
            'logo': SITE + 'icon-512.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': 'Singapore', 'postalCode': POSTAL, 'addressCountry': 'SG'},
            'hasMap': MAP, 'foundingDate': '2019-01-02', 'sameAs': ['https://www.sgpbusiness.com/company/New-Zen-Werkz-Pte-Ltd'], 'areaServed': AREA_LD,
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'UEN', 'value': UEN},
            'knowsAbout': [s['h1'] for s in SERVICES] + ['Mercedes-Benz', 'Bentley', 'Automatic transmission'],
            'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Workshop services', 'itemListElement': [
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['short'], 'url': SITE + 'services/%s/' % s['slug']}} for s in SERVICES]}}


# ----------------------------------------------------------------------------------------------
# Register pages
# ----------------------------------------------------------------------------------------------
page('', '%s | Car Repair & Servicing Workshop, Kaki Bukit Singapore' % LEGAL,
     'New Zen Werkz: car servicing, engine and gearbox repair, brakes and diagnostics for continental and Japanese cars at Eunos Technolink, Kaki Bukit, near Eunos, Ubi, Bedok and Tampines. Call 6742 8117.',
     'New Zen Werkz', home_body(), hero=False, schema=[faq_schema(FAQ_HOME)])
page('services/', 'Car Workshop Services in Kaki Bukit | New Zen Werkz',
     'Car servicing, engine overhaul, gearbox repair, brakes, diagnostics, batteries and continental car repair at New Zen Werkz, Eunos Technolink, Kaki Bukit.',
     'Workshop services', services_index(), crumbs=[('services/', 'Services')],
     lede='Everything from a routine service to an engine or gearbox rebuild, done at our workshop in Eunos Technolink.')
for s in SERVICES:
    path = 'services/%s/' % s['slug']
    page(path, s['title'], s['desc'], s['h1'], service_body(s), crumbs=[('services/', 'Services'), (path, s['short'])], lede=s['lede'],
         photo=s['photo'], schema=[{'@type': 'Service', 'name': s['h1'], 'serviceType': s['short'], 'description': s['desc'], 'url': SITE + path,
                                    'provider': provider(), 'areaServed': AREA_LD}, faq_schema(s['faqs'])])
page('areas/', 'Car Workshop Near Bedok, Tampines, Eunos & Ubi | New Zen Werkz',
     'Car workshop within 8 km of Kaki Bukit for drivers in Eunos, Ubi, Bedok, Tampines, Paya Lebar, Geylang, Hougang and Pasir Ris. WhatsApp +65 8678 1878.',
     'Car workshop near you in the East', areas_body(), crumbs=[('areas/', 'Areas we serve')], cta=False,
     lede='Servicing and repairs for drivers within about 8 km of Kaki Bukit.')
for l in LOCAL:
    path = 'areas/%s/' % l['slug']
    page(path, l['title'], l['desc'], 'Car workshop near %s' % l['name'], local_body(l), crumbs=[('areas/', 'Areas we serve'), (path, l['name'])],
         lede=l['lede'], cta=False, top=local_top(l),
         schema=[{'@type': 'Service', 'name': 'Car repair and servicing near %s' % l['name'], 'serviceType': 'Car repair and servicing',
                  'url': SITE + path, 'provider': provider(),
                  'areaServed': [{'@type': 'Place', 'name': x + ', Singapore'} for x in l['places']]}, faq_schema(l['faqs'])])
page('articles/', 'Car Care Articles | New Zen Werkz, Singapore',
     'Plain-English car care guides from the New Zen Werkz workshop: gearbox warning signs, check engine lights, servicing intervals, brakes, engine overhauls and batteries.',
     'Car care articles', articles_index(), crumbs=[('articles/', 'Articles')],
     lede='Straight answers to the questions drivers ask us most, written by the workshop.')
for a in ARTICLES:
    path = 'articles/%s/' % a['slug']
    page(path, a['title'], a['desc'], a['h1'], article_body(a), crumbs=[('articles/', 'Articles'), (path, a['h1'])],
         photo=a['photo'], schema=[article_schema(a, path)] + ([faq_schema(a['faqs'])] if a.get('faqs') else []), date=art_mod(a))
page('about/', 'About New Zen Werkz | Kaki Bukit Car Workshop',
     'New Zen Werkz Pte Ltd is an independent car workshop at Eunos Technolink, Kaki Bukit, servicing and rebuilding continental, Japanese and American cars.',
     'About New Zen Werkz', about_body(), crumbs=[('about/', 'About')],
     lede='An independent car workshop at Eunos Technolink, Kaki Bukit.')
page('contact/', 'Contact New Zen Werkz | Call 6742 8117, Eunos Technolink',
     'Call New Zen Werkz on 6742 8117 or visit the workshop at Blk 3 Kaki Bukit Road 1, #03-04 Eunos Technolink, Singapore 415935.',
     'Contact the workshop', contact_body(), crumbs=[('contact/', 'Contact')], cta=False,
     top=addr_line() + '<div class="cta-row">%s%s</div>' % (call_btn(), wa_btn('WhatsApp %s' % WA_SHOW)),
     lede='WhatsApp +65 8678 1878, call 6742 8117 or visit us at Eunos Technolink, Kaki Bukit.')


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------
def page_date(path):
    # Real last change per page: an article's own date; the articles hub and home move only when a newer article is added.
    p = PAGES.get(path) or {}
    if p.get('date'):
        return p['date']
    if path in ('', 'articles/'):
        return max([UPDATED] + [art_mod(a) for a in ARTICLES])
    return UPDATED


def render(path, p):
    pre = '../' * path.count('/')
    url = SITE + path
    share = IMG + 'share/home.jpg'

    def fix(s):
        return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                                 'inLanguage': 'en-SG', 'dateModified': UPDATED, 'about': {'@id': SITE + '#business'},
                                 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = '<section class="phero"><div class="wrap">%s<h1>%s</h1>%s%s</div></section>' % (
            crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '', fix(p.get('top', '')))
    band = ''
    if p['cta']:
        band = ('<section class="sec"><div class="wrap"><div class="band"><div><h2>Car not feeling right?</h2>'
                '<p>WhatsApp or call the workshop and tell us what you have noticed.</p></div><div class="cta-row">%s%s</div></div></div></section>') % (
            wa_btn(), call_btn())
    # Rule 4.3 (17 Oct 2026): no noindex meta in pages; the preview is hidden by the X-Robots-Tag header in preview/.htaccess.
    robots = 'index,follow,max-image-preview:large'
    title = E(p['title'])
    preload = '<link rel="preload" as="image" href="%s%s.webp" fetchpriority="high">' % (IMG, p['photo'] or 'workshop-lineup') if (p['photo'] or path == '') else ''
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="{robots}">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#14171c">
<link rel="canonical" href="{url}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
{preload}
<meta property="og:type" content="{'article' if path.startswith('articles/') and path != 'articles/' else 'website'}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="stylesheet" href="{pre}nzw.css?v=10">
{INTRO if path == '' and not p.get('is404') else ''}<script src="{pre}nzw.js?v=7" defer></script>
<script src="{pre}p1cta.js?v=1" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>{STREET}, Singapore {POSTAL}</span><span class="strip-r"><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a> · <a href="tel:{TEL}">Call {TEL_SHOW}</a></span></div></div>
<header class="hdr"><div class="wrap">
<a class="brand" href="{pre or './'}" aria-label="{NAME}, home page">{MARK}<span><span class="brand-name">New Zen Werkz</span><span class="brand-sub">Car repair · Kaki Bukit</span></span></a>
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('WhatsApp', 'btn btn-wa hdr-call')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<main id="main">
{head_hero}
{fix(p['body'])}
{band}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div><a class="brand" href="{pre or './'}">{MARK}<span><span class="brand-name">New Zen Werkz</span><span class="brand-sub">Car repair · Kaki Bukit</span></span></a>
<p>Independent car workshop for continental, Japanese and American cars.</p></div>
<div><h3>Services</h3><ul>{''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, s['slug'], E(s['short'])) for s in SERVICES)}</ul></div>
<div><h3>Areas</h3><ul>{''.join('<li><a href="%sareas/%s/">%s</a></li>' % (pre, l['slug'], E(l['name'])) for l in LOCAL)}<li><a href="{pre}areas/">All areas we serve</a></li></ul></div>
<div><h3>Workshop</h3><ul>
<li>{'<br>'.join(ADDR)}</li>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></li>
<li><a href="tel:{TEL}">Tel {TEL_SHOW}</a></li>
<li>Mon–Fri 9:30am–7pm · Sat 9:30am–4pm · Sun closed</li>
<li><a href="{MAP}" target="_blank" rel="noopener">Google Maps</a></li>
<li><a href="{pre}areas/">Areas we serve</a> · <a href="{pre}articles/">Articles</a> · <a href="{pre}about/">About</a> · <a href="{pre}contact/">Contact</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{LEGAL} · UEN {UEN}</span><span>© 2026 {LEGAL} · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp New Zen Werkz on {WA_SHOW}">{WA_SVG}<span>WhatsApp</span></a><a class="dock-call" href="tel:{TEL}" aria-label="Call New Zen Werkz on {TEL_SHOW}">{PHONE_SVG}<span>Call</span></a></div>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', t) for h, t in [('', 'Home')] + NAV)
    p = dict(title='Page not found | New Zen Werkz', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, photo=None)
    p['is404'] = True
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    if LIVE:
        out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="/%s"' % (m.group(1), m.group(2) if m.group(2) != './' else ''), out)
    else:
        out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="/preview/%s/%s"' % (m.group(1), SLUG, m.group(2) if m.group(2) != './' else ''), out)
    return out


HTACCESS = """# New Zen Werkz ({DOMAIN}). This folder is {DOMAIN}'s document root and also
# pageonesingapore.com/preview/new-zen-werkz/. It overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^{DQ}$ [NC]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
ErrorDocument 404 /404.html
"""


def main():
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(path, p))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write('User-agent: *\nUser-agent: OAI-SearchBot\nUser-agent: ChatGPT-User\nUser-agent: Googlebot\nUser-agent: Bingbot\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
    if LIVE:
        with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f:
            f.write(INDEXNOW_KEY)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path in PAGES:
            f.write('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, path, page_date(path)))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# %s, car workshop in Singapore\n\n'
                '> %s is an independent car repair and servicing workshop at %s, Singapore %s (UEN %s). '
                'It services and repairs continental cars such as Mercedes-Benz and Bentley as well as Japanese and American cars, '
                'including engine and automatic gearbox rebuilds, brakes, diagnostics and batteries. Tel %s, WhatsApp %s. '
                'Open Monday to Friday 9:30am-7pm, Saturday 9:30am-4pm, closed Sunday.\n\n## Pages\n'
                % (LEGAL, LEGAL, STREET, POSTAL, UEN, TEL_SHOW, WA_SHOW))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
    # CTA tap tracking -> Page One Controller (tracker v3, /mnt/project-files/tracking/wa-tap-counter.js)
    with open(os.path.join(HERE, '..', 'tracking', 'wa-tap-counter.js')) as src, open(os.path.join(OUT, 'p1cta.js'), 'w') as f:
        js = src.read()
        assert js.count("site:'SLUG'") == 1
        f.write(js.replace("site:'SLUG'", "site:'%s'" % SLUG))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': LEGAL, 'short_name': NAME, 'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
            'theme_color': '#14171c', 'background_color': '#ffffff', 'display': 'browser'}, f)
    with open(os.path.join(OUT, 'favicon.svg'), 'w') as f:
        f.write(MARK.replace(' class="brand-mark"', ' xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true"', ''))
    with open(os.path.join(OUT, '.htaccess'), 'w') as f:
        dom = DOMAIN or 'CLIENT-DOMAIN'
        f.write(HTACCESS.replace('{DOMAIN}', dom).replace('{DQ}', dom.replace('.', r'\.')))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()

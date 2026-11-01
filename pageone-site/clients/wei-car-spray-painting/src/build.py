"""Wei Car Spray Painting: builds every page into site/ (python3 build.py [outdir]).

Facts used (1 Nov 2026) and where they came from:
- ACRA (via acrawatch.sg and recordowl.com, data.gov.sg dataset): WEI CAR SPRAY PAINTING PTE. LTD., UEN 201215981N,
  incorporated 28 June 2012, live exempt private company, registered at 1017 Yishun Industrial Park A #01-242 S768759,
  primary SSIC 95301 repair and maintenance of motor vehicles (changed 10 Aug 2024 from car washing).
- Facebook page (screenshot from Edwin, 1 Nov 2026): "100% recommend (238 reviews)"; BLK 1017 UNIT#01-242/246/252, Yishun,
  Singapore 768759; phone 9638 3306; email weileng619@yahoo.com; has a Book Now button.
- Instagram @weicarspraypainting (screenshot, 1 Nov 2026): 25 posts; bio "Blk 1017 #01-242 & 246 Yishun Industrial Park A".
  Logo: gold car outline with "Wei Car Spray Painting Pte Ltd" on black.
- sgCarmart listing (photo shared on their Facebook, 8 Sep 2022): Blk 1017 Yishun Industrial Park A #01-242 S768759;
  opening hours 9am-7pm Mon-Fri, 9am-5pm Sat; phone 67593229 and 96383306; categories Repair & Servicing, Spray Painting.
  The shopfront photo shows the signboard with the Spies Hecker logo and an ICI Autocolor spray booth.
- Facebook posts (screenshots from Edwin, 1 Nov 2026): Porsche Macan full body colour change to Fountain Blue Metallic (29 May 2025);
  MG exterior respray British racing green (HGY), "4 day downtime" (10 Nov 2023); Honda Civic full in/out respray Aiika CS46, rooftop gloss
  black, new spoiler (24 Nov 2023); Mini Cooper new colour, orange before / pink after (7 May 2022); Honda Spada respray new colour Aiika paint
  (11 Feb 2026); Porsche Cayenne new-model bodykit installation imported from overseas (4 Feb 2026); Kia Cerato Forte "4th time customer"
  (31 Mar 2023); team photo (26 Sep 2024); claims post (21 Sep 2024): "We provide insurance claim third party, personal injury claim,
  replacement car, towing service, loss of income/use PHV, repair all damaged car accident/panel beating, 96383306 Wei"; poster (8 Apr 2026):
  "Full respray $888 this month only", "9638 3306 (WhatsApp Now)" (expired offer, not shown).
Not claimed anywhere: prices, durations, warranties, insurance or claims work, "best"/"cheapest", review text, rating schema.
"""
import html
import json
import os
import re
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'site')

SLUG = 'wei-car-spray-painting'
DOMAIN = ''  # CONFIRM: no domain yet
LIVE = False
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
UPDATED = '2026-11-01'
V = '5'
INDEXNOW_KEY = '7c41e9a0d2b85f36a1e4c07b9d5f2e18'

NAME = 'Wei Car Spray Painting'
LEGAL = 'Wei Car Spray Painting Pte. Ltd.'
UEN = '201215981N'
FOUNDED = '2012-06-28'
TEL1, TEL1_SHOW = '+6567593229', '6759 3229'
TEL2, TEL2_SHOW = '+6596383306', '9638 3306'
WA_NUM, WA_SHOW = '6596383306', '9638 3306'  # their own poster (8 Apr 2026): "9638 3306 (WhatsApp Now)"; insurance post: "96383306 Wei"
WA_MSG = 'Hi Wei Car Spray Painting, I found your website. I would like a quote for '
EMAIL = 'weileng619@yahoo.com'
STREET, UNITS, POSTAL = 'Blk 1017 Yishun Industrial Park A', '#01-242/246/252', '768759'
ADDR = ['Blk 1017 Yishun Industrial Park A', '#01-242, #01-246 and #01-252', 'Singapore 768759']
MAPQ = quote('Wei Car Spray Painting, 1017 Yishun Industrial Park A #01-242 Singapore 768759')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
FB = 'https://www.facebook.com/share/19YgRcqvBh/'
IG = 'https://www.instagram.com/weicarspraypainting/'
REC = '100% recommend on Facebook from 238 reviews'
REC_DATE = 'checked 1 November 2026'
HOURS_SRC = 'Mon to Fri 9am to 7pm, Sat 9am to 5pm'  # CONFIRM: from the 2022 sgCarmart listing
HOURS_OK = False  # True once Wei confirms; adds hours to schema and drops the "call first" note

CONFIRM = [
    'Current opening hours (sgCarmart 2022 listing says Mon-Fri 9am-7pm, Sat 9am-5pm; Sunday?)',
    'Services list: panel spray, full respray, scratch, dent, bumper repair, servicing and repairs: all done in-house?',
    'Insurance claims post is from 21 Sep 2024: still offering third-party claims, personal injury claims, replacement car, towing, loss of use for PHV?',
    'Full respray $888 was an April 2026 "this month only" offer: any current from-price we can show?',
    'Prices "from" for panel spray and full respray (none shown until confirmed)',
    'Founder / boss name and how long they have been spraying (company registered 28 Jun 2012)',
    'Job photos are cropped from Facebook screenshots (1 Nov 2026): send originals for sharper images; permission to quote 3-4 Facebook reviews',
    'Paint brands: posts mention Aiika paint (2023, 2026); signboard shows Spies Hecker (2022). Which do they use now?',
    'Domain name for go-live',
]

E = html.escape
CAR_OUTER = 'M4 44C30 30 60 24 92 14C120 6 150 8 172 20C182 21 190 21 193 24C196 28 197 35 195 42'
CAR_INNER = 'M10 44C60 34 120 30 186 25'


def car_svg(cls='car', draw=False):
    return ('<svg class="%s" viewBox="0 0 200 50" aria-hidden="true" fill="none" stroke="currentColor" stroke-linecap="round">'
            '<path class="o%s" d="%s" stroke-width="3.2"/><path class="i%s" d="%s" stroke-width="1.6"/></svg>') % (
        cls, ' draw' if draw else '', CAR_OUTER, ' draw' if draw else '', CAR_INNER)


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')
TEL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>'

# simple line icons (24x24) per service
ICONS = {
    'spray': '<path d="M4 9h8v6H4z"/><path d="M12 11h3l2-2"/><path d="M8 15v5"/><path d="M19 5h.01M21 8h.01M21 3h.01M18 2h.01"/>',
    'full': '<path d="M3 15c0-2 1-3 3-3.5L8 8h8l2.5 3.5c2 .5 2.5 1.5 2.5 3.5v2H3z"/><circle cx="7" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/><path d="M9 5l1-2M15 5l-1-2M12 5V2"/>',
    'scratch': '<path d="M3 17 9 7"/><path d="M8 19l7-12"/><path d="M14 19l6-10"/>',
    'dent': '<path d="M3 7c4 0 5 2 9 2s5-2 9-2"/><path d="M3 15c4 0 4-4 9-4s5 4 9 4"/><path d="M3 20h18"/>',
    'bumper': '<path d="M3 10c2-2 16-2 18 0v5c-2 2-16 2-18 0z"/><path d="M7 12.5h10"/><path d="M5 6l2 2M19 6l-2 2"/>',
    'claim': '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5"/><path d="M10 13h6M10 17h4"/>',
    'kit': '<path d="M3 16c1-3 3-5 7-5h6c2 0 4 1 5 3v2z"/><path d="M14 8l6-2"/><path d="M3 19h18"/>',
    'wrench': '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8z" transform="rotate(0)"/><path d="M3 21l6-6"/><path d="M14.7 6.3 17 4l3 3-2.3 2.3"/>',
}


def icon(k):
    return '<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % ICONS[k]


def wa_url(topic='my car.'):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp photos for a quote', topic='my car.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic)), WA_SVG, E(label))


def tel_btn(cls='btn btn-ghost'):
    return '<a class="%s" href="tel:%s">%s<span>Call %s</span></a>' % (cls, TEL1, TEL_SVG, TEL1_SHOW)


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def steps(items):
    return '<ol class="steps">%s</ol>' % ''.join('<li><b>%s</b><span>%s</span></li>' % (E(a), E(b)) for a, b in items)


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, kicker=''):
    assert len(title) <= 60, (path, len(title), title)
    assert len(desc) <= 160, (path, len(desc))
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [], hero=hero, cta=cta, kicker=kicker)


def hours_line():
    return HOURS_SRC if HOURS_OK else '%s (please call to confirm before coming)' % HOURS_SRC


# ------------------------------------------------------------------------------------------------
# Services: one owner page per search intent
# ------------------------------------------------------------------------------------------------
SERVICES = [
    dict(slug='car-spray-painting', short='Panel spray painting', icon='spray', kw='car spray painting',
         photo='porsche-macan-fountain-blue', cap='Porsche Macan after its respray in Fountain Blue Metallic, May 2025.',
         title='Car Spray Painting in Yishun | Wei Car Spray Painting',
         desc='Panel spray painting in Yishun: colour-matched paint for scratched, faded or repaired panels, done in a spray booth. WhatsApp photos for a quote.',
         h1='Car spray painting in Yishun',
         card='Respray one panel or a few: doors, bumpers, bonnet, fenders. Colour-matched to the rest of your car.',
         lede='When one or two panels are scratched, faded or repaired, a panel respray brings them back to the same colour and shine as the rest of the car.',
         answer=('Car spray painting at Wei is panel work: the damaged panel is cleaned, sanded, filled where needed, primed, then sprayed with paint mixed '
                 'to your car\'s colour code and finished with clear coat in a spray booth. You only pay for the panels that need it, not the whole car.'),
         when=['Scratches through the clear coat that polishing cannot remove', 'Faded or peeling clear coat on the roof, bonnet or boot', 'A panel that was repaired after a knock and now needs paint',
               'Mismatched colour from an earlier repair done elsewhere', 'Chips and rust spots along door edges and wheel arches'],
         process=[('Inspect', 'We look at the panel in daylight, check the colour code and tell you what the job needs.'),
                  ('Prepare', 'Old paint is sanded down, dents and chips are filled, and the area around is masked off.'),
                  ('Prime', 'Primer seals the bare metal or filler so the colour sits evenly.'),
                  ('Spray', 'Colour is mixed to your paint code and sprayed in the booth, then clear coat goes on top.'),
                  ('Finish', 'Once cured, the panel is polished and checked against the panels next to it.')],
         faq=[('Will the new paint match the rest of my car?', 'Paint is mixed from your car\'s paint code, then checked against the panel next to it. Older paint fades, so for metallic and pearl colours the new colour is often blended slightly into the next panel so the change cannot be seen.'),
              ('Do I need to respray the whole car?', 'Usually not. If only a few panels are damaged, a panel respray is enough. A full respray makes sense when the paint is faded or peeling all over, or you want a new colour.'),
              ('How do I get a price?', 'WhatsApp clear photos of the damage in daylight, plus your car model. We reply with what the job needs. The final price is confirmed after we see the car.'),
              ('Can I wash my car after a respray?', 'Yes, gentle washing is fine. Ask us before waxing, polishing or coating the new paint, as fresh paint needs time to harden fully.')]),
    dict(slug='full-car-respray', short='Full respray & colour change', icon='full', kw='full car respray',
         photo='mg-british-racing-green', cap='MG exterior respray in British Racing Green (HGY), November 2023. Their post: "4 day downtime".',
         title='Full Car Respray & Colour Change | Wei Car Spray Painting',
         desc='Full car respray and colour change in Yishun, Singapore: the whole car repainted in its original colour or a new one, like our Macan and MG jobs.',
         h1='Full car respray and colour change',
         card='Whole-car repaint in the same colour or a new one: Porsche Macan, MG, Honda Civic and more.',
         lede='A full respray repaints the whole body so the colour and shine are even from front to back. It suits older cars with faded or peeling paint, or owners who want a new colour.',
         answer=('A full car respray repaints every exterior panel of the car. Old paint is sanded, dents and rust spots are fixed, the body is primed and then sprayed '
                 'in colour and clear coat. It costs more than panel work, so we only recommend it when most panels need paint anyway.'),
         when=['Clear coat peeling on the roof, bonnet and boot at the same time', 'Paint faded all over from years under the Singapore sun', 'Many small dents, chips and scratches around the car',
               'You want a new colour (check the LTA rules first, see below)', 'Preparing an older car you plan to keep for years'],
         process=[('Inspect', 'We go round the whole car with you and agree which panels, trims and areas are included.'),
                  ('Strip and prepare', 'Trims and lights are removed where needed, the body is sanded, and dents and rust spots are repaired.'),
                  ('Prime', 'The bare and repaired areas are primed and sanded smooth.'),
                  ('Spray', 'Colour and clear coat are sprayed in the booth, panel by panel.'),
                  ('Refit and polish', 'Trims go back on, the paint is polished and checked in daylight before you collect.')],
         faq=[('Is a full respray better than panel spray?', 'Not always. If the damage is on a few panels, panel spray costs less and matches well. A full respray is worth it when the paint is tired all over.'),
              ('Can I change my car colour?', 'Yes. We have changed cars to new colours, such as a Porsche Macan to Fountain Blue Metallic and a Mini Cooper from orange to pink. A colour change is a vehicle modification, so check the current LTA rules on OneMotoring and tell us when you book.'),
              ('Will you remove my lights and trims?', 'Where needed for a clean finish, yes. We agree what is removed and refitted when we inspect the car.'),
              ('How do I get a price?', 'WhatsApp photos of all four sides of the car in daylight plus the model and year. The final price is confirmed after inspection.')]),
    dict(slug='scratch-repair', short='Scratch repair', icon='scratch', kw='car scratch repair',
         photo='honda-spada-white-side', cap='Honda Spada after a respray with Aiika paint, February 2026.',
         title='Car Scratch Repair in Yishun | Wei Car Spray Painting',
         desc='Car scratch repair in Yishun: light scratches polished out, deep scratches filled and spray painted to match. Send photos on WhatsApp.',
         h1='Car scratch repair',
         card='Key marks, scuffs and scrapes: polished out if shallow, repainted if they go through the paint.',
         lede='Not every scratch needs paint. We check how deep it goes first, then choose the smallest fix that makes it disappear.',
         answer=('Car scratch repair depends on depth. Scratches only in the clear coat can often be polished out. Scratches that show primer or metal need the panel '
                 'sanded, filled, primed and spray painted to your colour code. Send a photo and we will tell you which one yours is.'),
         when=['Key scratches along doors', 'Scuffs from car park pillars and kerbs', 'Scratches from bicycles, trolleys or bags', 'Scratches that show white primer or bare metal', 'Swirls or scratches around door handles'],
         process=[('Check the depth', 'If your fingernail catches in the scratch, it is usually through the clear coat and needs paint.'),
                  ('Shallow scratch', 'Machine polishing levels the clear coat so the scratch no longer shows.'),
                  ('Deep scratch', 'The area is sanded, filled if needed and primed.'),
                  ('Paint', 'Colour is mixed to your paint code and sprayed, then clear coat.'),
                  ('Blend and polish', 'The new paint is blended and polished so the repair cannot be seen.')],
         faq=[('Can a scratch be fixed without spray painting?', 'If it is only in the clear coat, often yes, by polishing. If you can see primer or metal, the panel needs paint to stop rust and to look right.'),
              ('Do touch-up pens work?', 'For tiny stone chips they can stop rust, but on longer scratches they usually leave a visible line. Panel paint gives an even finish.'),
              ('Should I fix a scratch quickly?', 'Yes if it shows bare metal. Exposed metal can start to rust in our wet weather, and rust spreads under the paint.'),
              ('How do I get a price?', 'WhatsApp a close photo and a wider photo of the scratch in daylight. We reply with what it needs.')]),
    dict(slug='dent-repair', short='Dent repair', icon='dent', kw='car dent repair',
         photo='porsche-macan-primer', cap='Bodywork prepared and primed in the workshop before paint (Porsche Macan, May 2025).',
         title='Car Dent Repair in Yishun | Wei Car Spray Painting',
         desc='Car dent repair in Yishun: dents in doors, fenders and panels knocked out, filled and repainted to match. WhatsApp photos to Wei Car Spray Painting.',
         h1='Car dent repair',
         card='Door dings, fender dents and car park knocks: panel beaten, smoothed and repainted.',
         lede='Dents from car park knocks, poles and minor bumps are pushed back into shape, smoothed and painted so the panel looks like it was never hit.',
         answer=('Car dent repair at Wei means the metal is worked back into shape, any low spots are filled and sanded smooth, and the panel is primed and spray painted '
                 'to match. If the paint is cracked, painting is needed anyway; if the dent is small and the paint is unbroken, tell us and we will advise.'),
         when=['Door dings from car park neighbours', 'Dents on fenders and quarter panels from poles or bollards', 'Creases along a door or panel line', 'Dents with cracked or chipped paint', 'Dents left after a minor bump'],
         process=[('Inspect', 'We check the size of the dent, whether the paint is cracked and what is behind the panel.'),
                  ('Shape', 'The panel is worked back into shape as closely as possible.'),
                  ('Fill and smooth', 'Small low spots are filled and sanded flat.'),
                  ('Prime and paint', 'The area is primed, then sprayed in your colour and clear coat.'),
                  ('Polish', 'The repair is polished and checked against the rest of the car.')],
         faq=[('Does every dent need repainting?', 'No. If the paint is cracked or the dent needs filling, it needs paint. A small, shallow dent with unbroken paint may not. We tell you after we see it.'),
              ('Can you fix dents on plastic bumpers?', 'Bumpers are plastic and are repaired differently. See our bumper repair page.'),
              ('Will the repaired panel look different?', 'Paint is mixed to your colour code and blended where needed so the repair matches the panels around it.'),
              ('How do I get a price?', 'WhatsApp photos of the dent from straight on and from an angle, in daylight. The final price is confirmed after inspection.')]),
    dict(slug='bumper-repair', short='Bumper repair', icon='bumper', kw='car bumper repair',
         photo='kia-cerato-four-colours', cap='One customer\'s Kia Cerato Forte front end over four visits, March 2023.',
         title='Car Bumper Repair & Respray | Wei Car Spray Painting',
         desc='Car bumper repair in Yishun: scuffed, scratched, cracked or dented bumpers repaired and spray painted to match. WhatsApp photos for a quote.',
         h1='Car bumper repair and respray',
         card='Scuffed corners, cracks and scrapes on front and rear bumpers, repaired and repainted.',
         lede='Bumper corners take the most knocks in tight car parks. Most scuffs, scrapes and small cracks can be repaired and repainted instead of buying a new bumper.',
         answer=('Bumper repair fixes the plastic first, then the paint. Scuffs are sanded smooth, small cracks and splits are repaired, and the bumper is primed with a '
                 'primer made for plastic and spray painted to your colour. If the bumper is badly broken or its clips are torn off, we will tell you if replacing it makes more sense.'),
         when=['Scuffed bumper corners from car park pillars', 'Scrapes from kerbs and ramps under the front bumper', 'Small cracks or splits in the bumper', 'Paint peeling off the bumper', 'Mismatched bumper colour from an earlier repair'],
         process=[('Inspect', 'We check the damage, the clips and the sensors (if your car has parking sensors).'),
                  ('Repair the plastic', 'Scuffs are sanded smooth; small cracks are repaired and reinforced.'),
                  ('Prime', 'A primer made for plastic is used so the paint stays on.'),
                  ('Paint', 'Colour and clear coat are sprayed to match the body.'),
                  ('Refit', 'The bumper is refitted and checked for gaps and alignment.')],
         faq=[('Repair or replace a bumper?', 'Scuffs, scratches and small cracks are usually repaired. A bumper that is badly split, warped or has broken mounting points may be better replaced. We tell you which after we see it.'),
              ('Will my parking sensors still work?', 'We check them before and after the job. Tell us if a sensor was already faulty before the repair.'),
              ('Why does bumper paint sometimes look different?', 'Plastic bumpers can take colour slightly differently from metal panels. Paint is mixed to your code and checked against the panel next to it.'),
              ('How do I get a price?', 'WhatsApp photos of the bumper damage in daylight plus your car model. The final price is confirmed after inspection.')]),
    dict(slug='car-servicing-repair', short='Servicing & repairs', icon='wrench', kw='car servicing yishun',
         photo='team', cap='The Wei Car Spray Painting team at the workshop, September 2024.',
         title='Car Servicing & Repairs in Yishun | Wei Car Spray Painting',
         desc='Car servicing and repairs at Wei Car Spray Painting, Blk 1017 Yishun Industrial Park A. Call or WhatsApp to book a slot.',
         h1='Car servicing and repairs',
         card='Repair and servicing work at the same workshop, so bodywork and mechanical jobs can be done together.',
         lede='Besides spray painting, Wei Car Spray Painting is listed for car repair and servicing. Tell us what your car needs and we will advise.',
         answer=('Wei Car Spray Painting is registered for repair and maintenance of motor vehicles and is listed for repair and servicing as well as spray painting. '
                 'Call or WhatsApp with your car model and what you need, and we will tell you if we can do it and when.'),
         when=['Routine servicing', 'Repairs found during a bodywork job', 'Combining a paint job with other work on the car', 'Checks before or after a long trip'],
         process=[('Tell us the job', 'WhatsApp or call with your car model, mileage and what you need.'),
                  ('Book a slot', 'We agree a day to bring the car in.'),
                  ('Inspect and quote', 'We check the car and confirm the work and price before starting.'),
                  ('Collect', 'We let you know when the car is ready.')],
         faq=[('Can I do servicing and a paint job at the same time?', 'Ask us when you book. Doing both in one visit can save you a second trip.'),
              ('Do you service all makes?', 'Call or WhatsApp with your car model and we will confirm.'),
              ('How do I book?', 'Call %s or WhatsApp %s with your car model and the job.' % (TEL1_SHOW, WA_SHOW))]),
    dict(slug='accident-repair-insurance-claims', short='Accident repair & claims', icon='claim', kw='accident repair insurance claim',
         photo='porsche-macan-stripped', cap='Panels removed and bodywork under repair in the workshop (May 2025).',
         title='Accident Repair & Insurance Claims Yishun | Wei Car',
         desc='Accident repair and panel beating in Yishun, with help on third-party insurance claims, personal injury claims, towing and a replacement car.',
         h1='Accident repair and insurance claims',
         card='Panel beating after an accident, plus help with third-party claims, towing and a replacement car.',
         lede='After an accident you need the car fixed and the claim sorted. We repair accident damage and help you with the claim paperwork.',
         answer=('Wei Car Spray Painting repairs accident damage and panel beating, and has offered help with third-party insurance claims, personal injury claims, '
                 'a replacement car, towing, and loss of income or loss of use claims for private-hire drivers (their post, September 2024). Call or WhatsApp Wei on 9638 3306 after an accident.'),
         when=['Your car was hit and the other driver is at fault (third-party claim)', 'You need towing to the workshop', 'You need a replacement car while yours is repaired',
               'You drive for a private-hire platform and lose income while the car is off the road', 'Panel beating and respray after any accident'],
         process=[('Call or WhatsApp', 'Tell Wei what happened and send photos of the damage and the scene.'),
                  ('Towing if needed', 'Ask about towing if the car cannot be driven.'),
                  ('Report and claim', 'We help you with the report and the claim paperwork.'),
                  ('Repair', 'Panel beating, parts and respray in the workshop.'),
                  ('Collect', 'We let you know when the car is ready.')],
         faq=[('Do you help with third-party insurance claims?', 'Yes. Wei Car Spray Painting has offered help with third-party claims, personal injury claims, replacement cars, towing and loss of use for private-hire drivers. Call 9638 3306 to check your case.'),
              ('What should I do right after an accident?', 'Make sure everyone is safe, take photos of the cars, plates and scene, exchange details with the other driver, then call us. Report the accident to your insurer as your policy requires.'),
              ('Can I get a replacement car?', 'Ask Wei when you call. A replacement car is one of the services listed for claims.'),
              ('I drive private hire. Can I claim lost income?', 'Loss of income or loss of use claims for private-hire drivers are listed in our claims services. Call to check what applies to your case.')]),
    dict(slug='body-kit-installation', short='Body kit installation', icon='kit', kw='body kit installation singapore',
         photo='porsche-cayenne-bodykit-side', cap='Porsche Cayenne with a new-model body kit, imported from overseas and installed by us, February 2026.',
         title='Body Kit Installation in Singapore | Wei Car Spray Painting',
         desc='Body kit installation and spray painting in Yishun: bumpers, skirts and spoilers fitted and painted to match, like our Porsche Cayenne and Honda Civic jobs.',
         h1='Body kit installation',
         card='Bumpers, skirts, lips and spoilers fitted and painted to match the car.',
         lede='A body kit only looks right when it fits well and the paint matches. We fit and spray kits in the same workshop.',
         answer=('Wei Car Spray Painting fits body kits and spoilers and paints them to match. Recent jobs include a new-model body kit imported from overseas for a Porsche Cayenne '
                 '(February 2026) and a new spoiler with a full respray and gloss black roof on a Honda Civic (November 2023).'),
         when=['Fitting a facelift or new-model look kit', 'Adding a spoiler, lip or side skirts', 'Painting a kit you bought to match your car', 'Combining a kit with a full respray or colour change'],
         process=[('Plan', 'Tell us the car and the kit. We check fit and what paint the kit needs.'),
                  ('Test fit', 'Parts are offered up to the car and adjusted for gaps.'),
                  ('Prepare and paint', 'Parts are sanded, primed and sprayed to match.'),
                  ('Install', 'The kit is fitted and checked for gaps and alignment.')],
         faq=[('Can you install a kit I bought myself?', 'Ask us with the kit details and photos. Fit quality differs between kits, so we check it first.'),
              ('Will the kit match my car colour?', 'Kit parts are sprayed in your car colour, or a contrast colour if you want, like the gloss black roof on our Civic job.'),
              ('Is a body kit legal in Singapore?', 'Body kits are a vehicle modification. Check the current LTA rules on OneMotoring before you buy, and tell us when you book.')]),
]
SBY = {s['slug']: s for s in SERVICES}

# ------------------------------------------------------------------------------------------------
# Articles: long-tail questions buyers type; each links to its owner service page
# ------------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='panel-spray-vs-full-respray', svc='full-car-respray', icon='full',
         title='Panel Spray or Full Respray: Which Does Your Car Need?',
         desc='Panel spray painting or a full car respray? How to tell which one your car needs, what each involves and when a full respray is worth it.',
         h1='Panel spray or full respray: which does your car need?',
         lede='Most cars only need a few panels painted. Here is how to tell when that is enough and when a full respray makes more sense.',
         sections=[
             ('What is the difference?', ['A panel spray repaints only the damaged panels, such as one door or a bumper. A full respray repaints every exterior panel of the car. Panel work costs less and keeps the original factory paint on the rest of the car; a full respray gives one even colour and finish everywhere.']),
             ('When panel spray is enough', ['Choose panel spray when the damage is local: a scratched door, a scuffed bumper corner, a dented fender. Paint is mixed from your car\'s paint code and blended into the next panel where needed, so the repair matches.',
                                             '<ul><li>One to a few damaged panels</li><li>The rest of the paint is still glossy</li><li>You want to keep as much original paint as possible</li></ul>']),
             ('When a full respray makes sense', ['A full respray is worth it when the problem is everywhere, not in one spot.',
                                                  '<ul><li>Clear coat peeling on the roof, bonnet and boot</li><li>Paint faded all over after years in the sun</li><li>Many chips, dents and scratches all around the car</li><li>You want a new colour (check LTA rules on OneMotoring first)</li></ul>']),
             ('A quick test you can do', ['Wash the car and look at it in daylight from a few metres away. If the damage is in two or three places and the other panels still shine, panel spray is usually the answer. If the whole car looks dull or patchy, ask about a full respray.']),
             ('Not sure? Send photos', ['WhatsApp photos of all four sides in daylight. We will tell you honestly which option fits, and why. See <a href="services/car-spray-painting/">panel spray painting</a> and <a href="services/full-car-respray/">full car respray</a> for how each job is done.'])]),
    dict(slug='can-car-scratches-be-fixed-without-respray', svc='scratch-repair', icon='scratch',
         title='Can a Car Scratch Be Fixed Without Spray Painting?',
         desc='Some car scratches polish out, others need paint. The fingernail test, the three paint layers and when a scratch needs spray painting.',
         h1='Can a car scratch be fixed without spray painting?',
         lede='Often, yes. It depends on how deep the scratch goes. The fingernail test tells you in a few seconds.',
         sections=[
             ('The short answer', ['A scratch that is only in the clear coat can usually be polished out without paint. A scratch that shows white primer or grey metal needs the panel painted, both to look right and to stop rust.']),
             ('The three layers of car paint', ['<ol><li><b>Clear coat:</b> the glossy top layer that protects the colour.</li><li><b>Base coat:</b> the colour layer.</li><li><b>Primer:</b> the layer that bonds paint to the metal or plastic underneath.</li></ol>',
                                                'The deeper the scratch, the more layers need to be rebuilt.']),
             ('The fingernail test', ['Run your fingernail gently across the scratch. If it does not catch, the scratch is probably in the clear coat and may polish out. If it catches, the scratch has likely gone through the clear coat. If you can see white or grey at the bottom, it has reached primer or metal.']),
             ('What about touch-up pens?', ['Touch-up paint is fine for tiny stone chips to keep rust away. On a longer key scratch it usually leaves a raised, uneven line that is easy to see. For those, a proper panel repair gives an invisible result.']),
             ('Get it checked', ['Send one close photo and one wider photo of the scratch on WhatsApp. We will tell you if it can be polished or needs paint. Read more on our <a href="services/scratch-repair/">car scratch repair</a> page.'])]),
    dict(slug='how-car-paint-colour-matching-works', svc='car-spray-painting', icon='spray',
         title='How Car Paint Colour Matching Works',
         desc='How a workshop matches new paint to your car: the paint code, mixing, spray-out checks and blending into the next panel so repairs cannot be seen.',
         h1='How car paint colour matching works',
         lede='A good repair is one you cannot spot. That comes down to the paint code, careful mixing and blending.',
         sections=[
             ('It starts with the paint code', ['Every car has a paint code from the factory, usually on a sticker or plate in the door jamb, under the bonnet or in the boot. The code tells the painter which formula to mix. The same colour name can have several formulas, so the code matters more than the name.']),
             ('Why the code alone is not enough', ['Paint changes with age. Years of sun can make the original colour slightly lighter or duller than the factory formula. Metallic and pearl paints also look different depending on how they are sprayed. So the mixed colour is checked against your actual car, not only the code.']),
             ('Spray-out and adjust', ['Painters spray a small test card and compare it with the car in good light. If it is off, the mix is adjusted until it matches.']),
             ('Blending into the next panel', ['For metallic and pearl colours, the new colour is often faded slightly into the panel next to the repair, then the clear coat covers both. This hides the edge so your eye cannot find where the new paint starts.']),
             ('What you can do', ['Bring the car in clean and in daylight hours so the colour can be checked properly. See how panel work is done on our <a href="services/car-spray-painting/">car spray painting</a> page.'])]),
    dict(slug='repair-or-replace-car-bumper', svc='bumper-repair', icon='bumper',
         title='Should You Repair or Replace a Damaged Car Bumper?',
         desc='Scuffed, cracked or dented bumper? When a bumper can be repaired and repainted, and when replacing it is the better choice.',
         h1='Should you repair or replace a damaged car bumper?',
         lede='Most bumper damage in Singapore comes from tight car parks and kerbs, and most of it can be repaired. Here is how to tell.',
         sections=[
             ('Usually repairable', ['<ul><li>Scuffed or scraped corners</li><li>Scratches through the paint</li><li>Small cracks or short splits</li><li>Paint peeling off the plastic</li><li>Shallow dents that pop back</li></ul>',
                                     'These are sanded, repaired, primed with a primer made for plastic and repainted to match.']),
             ('Often better replaced', ['<ul><li>Large splits or missing pieces</li><li>Torn mounting tabs or clips so the bumper will not sit straight</li><li>Bumpers warped out of shape</li><li>Damage around sensor or camera mounts that cannot be made secure</li></ul>']),
             ('Check the hidden parts', ['A knock hard enough to crack the bumper can also bend the bracket or the reinforcement bar behind it. Ask the workshop to look behind the bumper, not just at the surface.']),
             ('Parking sensors', ['If your car has parking sensors, mention it. They are checked before and after the job, and the paint around them must stay thin enough for them to work.']),
             ('Get advice first', ['WhatsApp photos of the damage in daylight and we will say whether a repair will do. More on our <a href="services/bumper-repair/">bumper repair</a> page.'])]),
    dict(slug='choosing-a-car-spray-painting-workshop', svc='car-spray-painting', icon='spray',
         title='How to Choose a Car Spray Painting Workshop',
         desc='What to check before choosing a car spray painting workshop in Singapore: spray booth, paint system, colour matching, quotes and reviews.',
         h1='How to choose a car spray painting workshop',
         lede='Paint jobs look similar on the first day. The difference shows months later. Here is what to ask before you book.',
         sections=[
             ('1. Do they spray in a booth?', ['A spray booth keeps dust and insects out of wet paint and controls how it dries. Paint sprayed in the open is more likely to show specks and uneven gloss.']),
             ('2. What paint do they use?', ['Ask which paint brand and system the workshop uses. Established refinish brands have tested colour formulas for most car models, which helps the match.']),
             ('3. How do they match colour?', ['A good painter will ask for or find your paint code, check the colour against your car and blend into the next panel where needed. Be wary of a quote that skips this.']),
             ('4. Is the quote clear?', ['The quote should say which panels are included, whether dents or rust are repaired first and whether trims or lights are removed. Final prices often depend on what is found once sanding starts, so ask how changes are handled.']),
             ('5. What do other customers say?', ['Read recent reviews and look at photos of finished jobs, ideally of cars in colours like yours. Wei Car Spray Painting is %s (%s): see our <a href="%s" target="_blank" rel="noopener">Facebook page</a>.' % (REC, REC_DATE, FB)]),
             ('Visit the workshop', ['Wei Car Spray Painting is at %s, %s, Singapore %s. WhatsApp photos first, then bring the car in for a look. See <a href="services/car-spray-painting/">car spray painting</a>.' % (STREET, UNITS, POSTAL)])]),
]
ABY = {a['slug']: a for a in ARTICLES}

HOME_FAQ = [
    ('Where is Wei Car Spray Painting?', 'At Blk 1017 Yishun Industrial Park A, units #01-242, #01-246 and #01-252, Singapore 768759, in the Yishun industrial estate.'),
    ('How do I get a quote for spray painting?', 'WhatsApp clear photos of the damage in daylight plus your car model to %s. We reply with what the job needs; the final price is confirmed after we see the car.' % WA_SHOW),
    ('Can you change my car to a new colour?', 'Yes. Recent colour changes include a Porsche Macan in Fountain Blue Metallic and a Mini Cooper from orange to pink. For only a few damaged panels, a panel respray in your current colour is enough.'),
    ('Can you help with an accident insurance claim?', 'Yes. We repair accident damage and help with third-party claims, towing and a replacement car. Call or WhatsApp Wei on %s.' % WA_SHOW),
]


def business_schema():
    b = {'@type': 'AutoBodyShop', '@id': SITE + '#business', 'name': NAME, 'legalName': LEGAL, 'url': SITE,
         'telephone': [TEL1, TEL2], 'email': EMAIL, 'foundingDate': FOUNDED, 'taxID': UEN,
         'logo': SITE + 'assets/logo.png', 'image': [SITE + 'assets/og.jpg', SITE + 'assets/jobs-porsche-macan-fountain-blue.webp', SITE + 'assets/shopfront.jpg'], 'employee': {'@type': 'Person', 'name': 'Wei', 'telephone': TEL2},
         'address': {'@type': 'PostalAddress', 'streetAddress': '1017 Yishun Industrial Park A, #01-242', 'addressLocality': 'Singapore', 'postalCode': POSTAL, 'addressCountry': 'SG'},
         'hasMap': MAP, 'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'sameAs': [FB, IG],
         'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['short'], 'url': SITE + 'services/%s/' % s['slug']}} for s in SERVICES]}
    if HOURS_OK:
        b['openingHoursSpecification'] = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '09:00', 'closes': '19:00'},
                                          {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Saturday', 'opens': '09:00', 'closes': '17:00'}]
    return b


DIMS = json.load(open(os.path.join(HERE, 'dims.json')))


def jimg(k, alt, cls='', eager=False):
    w, h = DIMS[k]
    return '<img src="assets/jobs-%s.webp" alt="%s" width="%d" height="%d"%s%s>' % (
        k, E(alt), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', ' class="%s"' % cls if cls else '')


# Real jobs from their Facebook page (screenshots from Edwin, 1 Nov 2026). Dates are the post dates.
JOBS = [
    dict(k='porsche-macan-fountain-blue', car='Porsche Macan', work='Full body colour change to Fountain Blue Metallic', date='May 2025', tag='Colour change',
         more=['porsche-macan-stripped', 'porsche-macan-primer', 'porsche-macan-fountain-blue-2']),
    dict(k='mg-british-racing-green', car='MG', work='Exterior respray in British Racing Green (HGY), 4 days downtime', date='November 2023', tag='Full respray',
         more=['mg-british-racing-green-side']),
    dict(k='honda-civic-grey-blue', car='Honda Civic', work='Full respray inside and out in Aiika CS46, gloss black roof, new spoiler', date='November 2023', tag='Respray + spoiler', more=[]),
    dict(k='mini-cooper-pink', car='Mini Cooper', work='New colour: from orange to pink', date='May 2022', tag='Colour change', more=['mini-cooper-orange-before']),
    dict(k='honda-spada-white', car='Honda Spada', work='Respray in a new colour with Aiika paint', date='February 2026', tag='Colour change',
         more=['honda-spada-white-rear', 'honda-spada-white-side']),
    dict(k='porsche-cayenne-bodykit-side', car='Porsche Cayenne', work='New-model body kit, imported from overseas, installed', date='February 2026', tag='Body kit', more=[]),
    dict(k='kia-cerato-four-colours', car='Kia Cerato Forte', work='The same customer back for the 4th time: four looks over the years', date='March 2023', tag='Repeat customer', more=[]),
]

# Demo car colours: each one seen on a real Wei job. Hex values are on-screen approximations.
PAINTS = [
    ('Fountain Blue Metallic', '#8ea2c0', 'Porsche Macan, May 2025', 'porsche-macan-fountain-blue'),
    ('British Racing Green', '#1f3b30', 'MG, November 2023', 'mg-british-racing-green'),
    ('Aiika CS46 grey-blue', '#aab4c6', 'Honda Civic, November 2023', 'honda-civic-grey-blue'),
    ('Pearl white', '#f2f0ea', 'Honda Spada, February 2026', 'honda-spada-white'),
    ('Pink', '#f1a3c6', 'Mini Cooper, May 2022', 'mini-cooper-pink'),
    ('Orange (before)', '#ee8f1e', 'Mini Cooper, May 2022', 'mini-cooper-pink'),
    ('Silver grey', '#a3a9b0', 'Porsche Cayenne, February 2026', 'porsche-cayenne-bodykit-side'),
]

CAR_BODY = ('M38 172 L38 146 Q40 122 72 115 L150 104 C188 72 232 58 300 56 C358 56 396 66 432 96 L500 108 C546 115 566 128 569 152 '
            'L571 170 Q569 184 552 186 L506 186 A44 44 0 0 0 418 186 L192 186 A44 44 0 0 0 104 186 L58 186 Q40 184 38 172 Z')


def demo_car():
    """Side-view demo car: body fill comes from CSS var --paint; JS sprays a new colour across it."""
    def car(cls):
        gid = 'g' + cls.replace(' ', '-')
        return f'''<svg class="{cls}" viewBox="0 0 610 240" aria-hidden="true">
<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".38" stop-color="#fff" stop-opacity=".06"/><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient></defs>
<path class="body" d="{CAR_BODY}"/>
<path d="{CAR_BODY}" fill="url(#{gid})"/>
<path d="M60 130 C200 118 420 118 556 134" stroke="#fff" stroke-opacity=".35" stroke-width="2" fill="none"/>
<path d="M168 104 C202 78 238 69 292 67 L298 67 L298 104 Z M310 67 C352 67 382 75 414 100 L310 104 Z" fill="#1c2128"/>
<path d="M175 101 C205 80 236 72 288 70" stroke="#fff" stroke-opacity=".25" stroke-width="3" fill="none"/>
<path d="M300 106 L302 180 M196 108 L192 176" stroke="#000" stroke-opacity=".18" stroke-width="1.5" fill="none"/>
<path d="M548 128 Q562 132 566 146 L548 144 Z" fill="#fff6d8"/><path d="M40 136 L56 134 L56 150 L40 152 Z" fill="#c4262e"/>
<rect x="250" y="118" width="22" height="4" rx="2" fill="#000" opacity=".25"/><rect x="360" y="118" width="22" height="4" rx="2" fill="#000" opacity=".25"/>
</svg>'''
    wheels = ''.join(f'<g transform="translate({x} 186)"><circle r="41" fill="#15171b"/><circle r="25" fill="#c9cdd3"/><circle r="25" fill="none" stroke="#8b9097" stroke-width="2"/>'
                     + ''.join(f'<path d="M0 -6 L-4 -22 L4 -22 Z" fill="#8b9097" transform="rotate({a})"/>' for a in range(0, 360, 72)) + '<circle r="6" fill="#4b5058"/></g>'
                     for x in (148, 462))
    sw = ''.join('<button type="button" class="sw" style="--c:%s" data-c="%s" data-n="%s" data-j="%s" data-img="assets/jobs-%s.webp" aria-label="%s, seen on %s"%s></button>'
                 % (c, c, E(n), E(j), k, E(n), E(j), ' aria-pressed="true"' if i == 0 else ' aria-pressed="false"') for i, (n, c, j, k) in enumerate(PAINTS))
    n0, c0, j0, k0 = PAINTS[0]
    return f'''<div class="studio" style="--paint:{c0}">
<div class="stage">
<div class="car-wrap">{car('car base')}<div class="coat">{car('car top')}</div><div class="mist" aria-hidden="true"></div>
<svg class="wheels" viewBox="0 0 610 240" aria-hidden="true">{wheels}</svg></div>
<div class="floor" aria-hidden="true"></div>
</div>
<div class="picker">
<p class="pk-label">Tap a colour from our real jobs</p>
<div class="sws" role="group" aria-label="Paint colours">{sw}</div>
<a class="pk-job" href="our-work/"><img src="assets/jobs-{k0}.webp" alt="" width="56" height="40" loading="lazy"><span><b class="pk-n">{E(n0)}</b><small class="pk-j">Seen on our job: {E(j0)}</small></span></a>
</div>
</div>'''


def colour_picker():
    sw = ''.join('<a class="sw" style="--c:%s" href="our-work/#%s" aria-label="%s: see the %s job" title="%s, %s"></a>' % (c, k, E(n), E(j), E(n), E(j)) for n, c, j, k in PAINTS)
    return '<div class="wrap picker"><p class="pk-label">Tap a colour to see the real job</p><div class="sws" role="group" aria-label="Colours from our jobs">%s</div></div>' % sw


def job_card(j, eager=False):
    return ('<a class="job" data-k="%s" href="our-work/#%s">%s<span class="job-tag">%s</span><span class="job-txt"><b>%s</b><span>%s</span><small>%s</small></span></a>'
            % (j['k'], j['k'], jimg(j['k'], '%s: %s (%s)' % (j['car'], j['work'], j['date']), eager=eager), E(j['tag']), E(j['car']), E(j['work']), E(j['date'])))


def jobs_rail(eager=False):
    return '<div class="rail" data-glide tabindex="0" aria-label="Recent jobs"><div class="rail-track">%s</div></div>' % ''.join(job_card(j, eager and i < 3) for i, j in enumerate(JOBS))


def before_after():
    return f'''<div class="ba" style="--x:50%">
<div class="ba-img ba-after">{jimg('mini-cooper-pink', 'Mini Cooper after: resprayed pink')}</div>
<div class="ba-img ba-before">{jimg('mini-cooper-orange-before', 'Mini Cooper before: orange')}</div>
<span class="ba-l">Before</span><span class="ba-r">After</span>
<input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
<span class="ba-handle" aria-hidden="true"></span>
</div>'''


def svc_card(s):
    return ('<a class="svc" href="services/%s/"><span class="svc-ic">%s</span><h3>%s</h3><p>%s</p><span class="more">More details <i aria-hidden="true">→</i></span></a>'
            % (s['slug'], icon(s['icon']), E(s['short']), E(s['card'])))


def acard(a):
    return ('<a class="acard" href="articles/%s/"><span class="acard-art" aria-hidden="true">%s%s</span><span class="acard-body"><span class="tagline">Guide</span><h3>%s</h3><p>%s</p></span></a>'
            % (a['slug'], car_svg('acar'), icon(a['icon']), E(a['h1']), E(a['lede'])))


def proof_items():
    return ('<ul class="proof"><li><b>100%%</b><span>recommend on <a href="%s" target="_blank" rel="noopener">Facebook</a></span></li>'
            '<li><b>238</b><span>Facebook reviews</span></li><li><b>2012</b><span>registered as a Pte Ltd</span></li><li><b>3</b><span>units at Blk 1017 Yishun</span></li></ul>' % FB)


def home():
    body = f'''
<section class="hero">
<div class="wrap hero-top">
<div class="hero-copy">
<p class="kicker">Yishun Industrial Park A · Since 2012</p>
<h1>Car spray painting in Yishun, <span>see our real work.</span></h1>
<p class="lede">Resprays, colour changes, scratch, dent and bumper repair, body kits and accident claims at Blk 1017 Yishun Industrial Park A. WhatsApp photos and Wei tells you what your car needs.</p>
</div>
<div class="hero-side">
<div class="cta-row">{wa_btn()}{tel_btn()}</div>
<p class="rec">★ {REC} <small>({REC_DATE})</small></p>
<a class="link" href="our-work/">See all jobs <i aria-hidden="true">→</i></a>
</div>
</div>
{colour_picker()}
{jobs_rail(eager=True)}
</section>

<section class="sec">
<div class="wrap">
<div class="sec-head"><p class="kicker">What needs fixing?</p><h2>Pick the job, see how we do it</h2></div>
<div class="svc-grid">{''.join(svc_card(s) for s in SERVICES)}</div>
</div>
</section>

<section class="sec sec-tint">
<div class="wrap split">
{before_after()}
<div>
<p class="kicker">Before and after</p>
<h2>Orange Mini, now pink</h2>
<p>Drag the slider. This Mini Cooper came in orange and left in a new colour (May 2022). A colour change means the whole body is prepared, primed and sprayed, not just the panels you see first.</p>
<a class="link" href="services/full-car-respray/">Full respray and colour change <i aria-hidden="true">→</i></a>
</div>
</div>
</section>

<section class="sec">
<div class="wrap split">
<figure class="photo">{jimg('team', 'The Wei Car Spray Painting team in the workshop at Blk 1017 Yishun Industrial Park A')}<figcaption>The team at the workshop, September 2024.</figcaption></figure>
<div>
<p class="kicker">The workshop</p>
<h2>Three units, one team, one job done properly</h2>
<p>We work from units #01-242, #01-246 and #01-252 at Blk 1017 Yishun Industrial Park A. Panels are prepared in the workshop and painted in the spray booth, so dust stays out of the wet paint.</p>
{steps([('Send photos', 'WhatsApp the damage in daylight with your car model.'), ('We advise', 'Polish, panel paint, full respray or repair.'), ('Bring the car in', 'We inspect it and confirm the work and price.'), ('Collect', 'Colour-matched, polished and checked.')])}
</div>
</div>
</section>

<section class="sec sec-tint">
<div class="wrap trust">
<div><p class="kicker">Proof</p><h2>Trusted by drivers, again and again</h2><p>One Kia Cerato owner has come back four times for a new look. Read our Facebook reviews and see new jobs on Instagram.</p>
<div class="cta-row"><a class="btn btn-ghost" href="{FB}" target="_blank" rel="noopener">Read Facebook reviews</a><a class="btn btn-ghost" href="{IG}" target="_blank" rel="noopener">Instagram</a></div></div>
{proof_items()}
</div>
</section>

<section class="sec">
<div class="wrap">
<div class="sec-head row"><div><p class="kicker">Guides</p><h2>Before you book a paint job</h2></div><a class="link" href="articles/">All guides <i aria-hidden="true">→</i></a></div>
<div class="glide" tabindex="0" aria-label="Guides">{''.join(acard(a) for a in ARTICLES)}</div>
</div>
</section>

<section class="sec sec-tint">
<div class="wrap narrow">
<div class="sec-head"><p class="kicker">Questions</p><h2>Quick answers</h2></div>
{faq_html(HOME_FAQ)}
</div>
</section>

<section class="sec">
<div class="wrap split visit">
<div>
<p class="kicker">Visit</p>
<h2>Find us in Yishun</h2>
<p class="addr">{'<br>'.join(ADDR)}</p>
<p>Opening hours: {hours_line()}.</p>
<p>Phone <a href="tel:{TEL1}">{TEL1_SHOW}</a> · WhatsApp <a href="tel:{TEL2}">{TEL2_SHOW}</a> (Wei)<br>Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<div class="cta-row"><a class="btn btn-ghost" href="{E(MAP)}" target="_blank" rel="noopener">Open in Google Maps</a></div>
</div>
<div class="map"><iframe title="Map to Wei Car Spray Painting" src="{E(MAP_EMBED)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</section>
'''
    page('', 'Car Spray Painting Yishun | Wei Car Spray Painting',
         'Car spray painting, full resprays, colour changes, scratch, dent and bumper repair in Yishun. 100% recommend on Facebook (238 reviews).',
         'Car spray painting in Yishun', body, hero=False, schema=[faq_schema(HOME_FAQ)])


def our_work():
    items = []
    for j in JOBS:
        gal = ''.join('<figure>%s</figure>' % jimg(k, '%s, %s' % (j['car'], k.replace('-', ' '))) for k in [j['k']] + j['more'])
        items.append('<article class="work" id="%s"><div class="work-gal">%s</div><div class="work-txt"><span class="job-tag">%s</span><h2>%s</h2><p>%s.</p><p class="muted">Posted on our Facebook page, %s.</p></div></article>'
                     % (j['k'], gal, E(j['tag']), E(j['car']), E(j['work']), E(j['date'])))
    body = '<section class="sec"><div class="wrap works">%s</div></section>' % ''.join(items)
    page('our-work/', 'Car Respray Before & After | Wei Car Spray Painting',
         'Real resprays, colour changes and body kits from our Yishun workshop: Porsche Macan, MG, Honda Civic, Mini Cooper, Honda Spada and more.',
         'Our work', body, crumbs=[('our-work/', 'Our work')], lede='Real cars from our workshop, with the dates we posted them. More on our Facebook and Instagram.', kicker='Gallery',
         schema=[{'@type': 'ImageGallery', 'name': 'Wei Car Spray Painting jobs', 'image': [SITE + 'assets/jobs-%s.webp' % j['k'] for j in JOBS]}])


def services_index():
    body = '<section class="sec"><div class="wrap"><div class="svc-grid">%s</div></div></section>' % ''.join(svc_card(s) for s in SERVICES)
    page('services/', 'Spray Painting & Body Repair Services | Wei Car', 'Panel spray painting, full respray, scratch, dent and bumper repair, plus servicing and repairs at Blk 1017 Yishun Industrial Park A.',
         'Our services', body, crumbs=[('services/', 'Services')], lede='Paint and body repair for every kind of everyday damage, plus servicing and repairs at the same workshop.', kicker='Services')


def service_page(s):
    rel = [a for a in ARTICLES if a['svc'] == s['slug']]
    others = [x for x in SERVICES if x['slug'] != s['slug']][:3]
    body = f'''
<section class="sec"><div class="wrap svc-layout">
<article class="prose">
<figure class="photo">{jimg(s['photo'], s['cap'], eager=True)}<figcaption>{E(s['cap'])}</figcaption></figure>
<p class="answer">{E(s['answer'])}</p>
<h2>When you need {E(s['short'].lower())}</h2>
<ul class="ticks">{''.join('<li>%s</li>' % E(w) for w in s['when'])}</ul>
<h2>How we do it</h2>
{steps(s['process'])}
{'<h2>Guides on this</h2><ul>%s</ul>' % ''.join('<li><a href="articles/%s/">%s</a></li>' % (a['slug'], E(a['h1'])) for a in rel) if rel else ''}
<h2>Questions</h2>
{faq_html(s['faq'])}
</article>
<aside class="side">
<div class="side-card"><span class="side-ic">{icon(s['icon'])}</span><h3>Get a quote</h3><p>WhatsApp photos of the damage in daylight with your car model. The final price is confirmed after we see the car.</p>{wa_btn('WhatsApp ' + WA_SHOW, s['kw'] + '.')}{tel_btn()}</div>
<div class="side-card"><h3>Workshop</h3><p>{'<br>'.join(ADDR)}</p><p class="muted">{REC} ({REC_DATE}).</p></div>
</aside>
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Other services</h2></div><div class="svc-grid three">{''.join(svc_card(x) for x in others)}</div></div></section>
'''
    page('services/%s/' % s['slug'], s['title'], s['desc'], s['h1'], body, crumbs=[('services/', 'Services'), ('services/%s/' % s['slug'], s['short'])],
         lede=s['lede'], kicker='Wei Car Spray Painting · Yishun',
         schema=[{'@type': 'Service', 'name': s['short'], 'serviceType': s['kw'], 'description': s['answer'], 'provider': {'@id': SITE + '#business'},
                  'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'url': SITE + 'services/%s/' % s['slug']}, faq_schema(s['faq'])])


def articles_index():
    body = '<section class="sec"><div class="wrap"><div class="agrid">%s</div></div></section>' % ''.join(acard(a) for a in ARTICLES)
    page('articles/', 'Car Paint & Body Repair Guides | Wei Car Spray Painting', 'Plain guides on car scratches, dents, bumpers, colour matching and resprays from a Yishun spray painting workshop.',
         'Car paint and body repair guides', body, crumbs=[('articles/', 'Guides')], lede='Short, practical answers to the questions drivers ask us most.', kicker='Guides')


def article_page(a):
    s = SBY[a['svc']]
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join(p if p.startswith('<') else '<p>%s</p>' % p for p in ps)) for h, ps in a['sections'])
    body = f'''
<section class="sec"><div class="wrap svc-layout">
<article class="prose">
<p class="byline">By {NAME} · Updated <time datetime="{UPDATED}">1 November 2026</time></p>
{secs}
</article>
<aside class="side"><div class="side-card"><span class="side-ic">{icon(s['icon'])}</span><h3>{E(s['short'])}</h3><p>{E(s['card'])}</p><a class="link" href="services/{s['slug']}/">See how we do it <i aria-hidden="true">→</i></a>{wa_btn('WhatsApp photos', s['kw'] + '.')}</div></aside>
</div></section>
'''
    page('articles/%s/' % a['slug'], a['title'] if len(a['title']) <= 60 else a['title'][:60], a['desc'], a['h1'], body,
         crumbs=[('articles/', 'Guides'), ('articles/%s/' % a['slug'], a['h1'])], lede=a['lede'], kicker='Guide',
         schema=[{'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': UPDATED, 'dateModified': UPDATED, 'image': SITE + 'assets/og.jpg',
                  'author': {'@type': 'Organization', 'name': NAME, 'url': SITE}, 'publisher': {'@id': SITE + '#business'}, 'mainEntityOfPage': SITE + 'articles/%s/' % a['slug']}])


def about():
    body = f'''
<section class="sec"><div class="wrap split">
<div class="prose">
<p class="answer">{LEGAL} is a car spray painting and repair workshop at Blk 1017 Yishun Industrial Park A, Singapore. The company was registered on 28 June 2012 (UEN {UEN}) and works from units #01-242, #01-246 and #01-252.</p>
<h2>What we do</h2>
<p>Panel spray painting, full resprays, scratch repair, dent repair and bumper repair, plus car servicing and repairs. Paint is mixed to your car's colour code and sprayed in a spray booth.</p>
<h2>Company details</h2>
<table class="facts"><tbody>
<tr><th>Legal name</th><td>{LEGAL}</td></tr>
<tr><th>UEN</th><td>{UEN}</td></tr>
<tr><th>Registered</th><td>28 June 2012</td></tr>
<tr><th>Address</th><td>{', '.join(ADDR)}</td></tr>
<tr><th>Phone</th><td><a href="tel:{TEL1}">{TEL1_SHOW}</a> · <a href="tel:{TEL2}">{TEL2_SHOW}</a></td></tr>
<tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>Opening hours</th><td>{hours_line()}</td></tr>
<tr><th>Reviews</th><td>{REC} ({REC_DATE})</td></tr>
<tr><th>Social</th><td><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram @weicarspraypainting</a></td></tr>
</tbody></table>
</div>
<figure class="shop"><img src="assets/shopfront.webp" alt="Wei Car Spray Painting signboard and spray booth at Blk 1017 Yishun Industrial Park A" width="673" height="370" loading="lazy" decoding="async"><figcaption>The workshop and spray booth.</figcaption></figure>
</div></section>
'''
    page('about/', 'About Wei Car Spray Painting Pte Ltd | Yishun', 'Wei Car Spray Painting Pte Ltd (UEN 201215981N), registered 2012: spray painting and repair workshop at Blk 1017 Yishun Industrial Park A.',
         'About Wei Car Spray Painting', body, crumbs=[('about/', 'About')], lede='A Yishun spray painting and repair workshop, registered since 2012.', kicker='About')


def contact():
    body = f'''
<section class="sec"><div class="wrap split">
<div>
<h2>Send photos for a quote</h2>
<form id="enquiry" class="form" data-wa="{WA_NUM}">
<label>What needs fixing?<select name="s"><option>Panel spray painting</option><option>Full car respray</option><option>Scratch repair</option><option>Dent repair</option><option>Bumper repair</option><option>Servicing or repairs</option></select></label>
<label>Car model<input name="c" placeholder="e.g. Toyota Corolla Altis 2018" autocomplete="off"></label>
<label>Your name<input name="n" autocomplete="name"></label>
<label>Notes<textarea name="x" rows="3" placeholder="Where is the damage? Any deadline?"></textarea></label>
<button class="btn btn-wa" type="submit">{WA_SVG}<span>Continue on WhatsApp</span></button>
<p class="muted">This opens WhatsApp with your message. Attach your photos there. Nothing is stored on this website.</p>
</form>
</div>
<div class="prose">
<h2>Contact details</h2>
<p class="addr">{'<br>'.join(ADDR)}</p>
<p>Phone <a href="tel:{TEL1}">{TEL1_SHOW}</a><br>Mobile <a href="tel:{TEL2}">{TEL2_SHOW}</a><br>Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Opening hours: {hours_line()}.</p>
<div class="map"><iframe title="Map to Wei Car Spray Painting" src="{E(MAP_EMBED)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</div></section>
'''
    page('contact/', 'Contact Wei Car Spray Painting | Yishun', 'Call 6759 3229 or WhatsApp photos for a spray painting quote. Blk 1017 Yishun Industrial Park A #01-242, Singapore 768759.',
         'Contact us', body, crumbs=[('contact/', 'Contact')], lede='WhatsApp photos of the damage for the fastest answer, or call the workshop.', kicker='Contact', cta=False)


def privacy():
    body = f'''<section class="sec"><div class="wrap narrow prose">
<p>This website does not use cookies for advertising and has no login. The enquiry form does not send anything to us through this website: it only opens WhatsApp with your message, and you choose whether to send it.</p>
<p>We count taps on WhatsApp buttons (page, time, device type and how you reached the site) to understand which pages help customers. No names, phone numbers or IP addresses are kept for this.</p>
<p>Personal data you send us by WhatsApp, phone or email is used only to reply to you and do the job, following Singapore's Personal Data Protection Act (PDPA). To ask about your data, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>{LEGAL}, UEN {UEN}.</p>
</div></section>'''
    page('privacy/', 'Privacy Policy | Wei Car Spray Painting', 'How Wei Car Spray Painting handles personal data under the PDPA.', 'Privacy policy', body, crumbs=[('privacy/', 'Privacy')], cta=False)


NAV = [('services/', 'Services'), ('our-work/', 'Our work'), ('services/accident-repair-insurance-claims/', 'Insurance claims'), ('articles/', 'Guides'), ('about/', 'About'), ('contact/', 'Contact')]


def shell(path, p, robots_meta=''):
    pre = '../' * path.count('/')
    url = SITE + path

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path == h else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'], 'inLanguage': 'en-SG',
                                 'dateModified': UPDATED, 'primaryImageOfPage': SITE + 'assets/og.jpg', 'about': {'@id': SITE + '#business'}, 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = ('<section class="phero"><div class="wrap">%s%s<h1>%s</h1>%s</div>%s</section>' % (
            crumbs_html, '<p class="kicker">%s</p>' % E(p['kicker']) if p['kicker'] else '', E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '', car_svg('pcar', draw=True)))
    band = ''
    if p['cta']:
        band = ('<section class="sec band-sec"><div class="wrap"><div class="band"><div><h2>Got a scratch, dent or scuff?</h2>'
                '<p>WhatsApp photos in daylight with your car model. We tell you what it needs.</p></div><div class="cta-row">%s%s</div></div></div></section>' % (wa_btn('WhatsApp ' + WA_SHOW), tel_btn()))
    title = E(p['title'])
    body = fix(p['body'] + band)
    brand = ('<a class="brand" href="%s" aria-label="%s, home page"><img src="%sassets/logo.webp" alt="" width="44" height="44"><span><b>Wei Car</b><small>Spray Painting</small></span></a>' % (pre or './', NAME, pre))
    svc_links = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (pre, s['slug'], E(s['short'])) for s in SERVICES)
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
<meta name="theme-color" content="#f7f5f0">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}, Blk 1017 Yishun Industrial Park A">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}assets/og.jpg">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}assets/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{pre}wc.css?v={V}">
<script src="{pre}wc.js?v={V}" defer></script>
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
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}<p>Car spray painting, scratch, dent and bumper repair, full resprays, servicing and repairs at Blk 1017 Yishun Industrial Park A, Singapore.</p></div>
<div><h3>Services</h3><ul>{svc_links}</ul></div>
<div><h3>Explore</h3><ul><li><a href="{pre}articles/">Guides</a></li><li><a href="{pre}about/">About</a></li><li><a href="{pre}contact/">Contact</a></li><li><a href="{pre}privacy/">Privacy</a></li></ul></div>
<div><h3>Contact</h3><ul>
<li><a href="tel:{TEL1}">{TEL1_SHOW}</a> · <a href="tel:{TEL2}">{TEL2_SHOW}</a></li>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{'<br>'.join(ADDR)}</li>
<li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{LEGAL} · UEN {UEN}</span><span>© 2026 {NAME} · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp Wei Car Spray Painting on {WA_SHOW}">{WA_SVG}<span>WhatsApp</span></a><a class="dock-c" href="tel:{TEL1}">{TEL_SVG}<span>Call</span></a></div>
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
    for s in SERVICES:
        service_page(s)
    articles_index()
    for a in ARTICLES:
        article_page(a)
    our_work(); about(); contact(); privacy()
    for path, p in PAGES.items():
        write(path + 'index.html', shell(path, p))
    nf = dict(title='Page not found | Wei Car Spray Painting', desc='This page does not exist.', h1='Page not found',
              body='<section class="sec"><div class="wrap"><p>That page is not here. Try our <a href="%sservices/">services</a> or <a href="%sarticles/">guides</a>.</p></div></section>' % (SITE, SITE),
              crumbs=None, lede='', schema=[], hero=True, cta=True, kicker='')
    t = shell('', nf, '<meta name="robots" content="noindex">')
    # 404 is served at any depth: make relative links absolute
    t = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), SITE, '' if m.group(2) == './' else m.group(2)), t)
    t = t.replace('<link rel="canonical" href="%s">\n' % SITE, '')
    write('404.html', t)
    sm = ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, path, UPDATED) for path in PAGES)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % sm)
    bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
    write('robots.txt', 'User-agent: *\nAllow: /\n\n' + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'Sitemap: %ssitemap.xml\n' % SITE)
    write(INDEXNOW_KEY + '.txt', INDEXNOW_KEY)
    write('site.webmanifest', json.dumps({'name': NAME, 'short_name': 'Wei Car', 'start_url': './', 'display': 'standalone', 'background_color': '#f7f5f0', 'theme_color': '#f7f5f0',
                                          'icons': [{'src': 'assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}))
    llms = ['# %s' % NAME, '',
            '> %s is a car spray painting and repair workshop at Blk 1017 Yishun Industrial Park A, Singapore 768759: panel spray painting, full resprays, scratch, dent and bumper repair, plus car servicing and repairs. Registered 28 June 2012 (UEN %s).' % (LEGAL, UEN), '',
            '- Address: %s, units %s, Singapore %s' % (STREET, UNITS, POSTAL), '- Phone: %s, mobile %s' % (TEL1_SHOW, TEL2_SHOW), '- Email: %s' % EMAIL,
            '- Opening hours: %s' % hours_line(), '- Reviews: %s (%s)' % (REC, REC_DATE), '- Facebook: %s' % FB, '- Instagram: %s' % IG, '- Map: %s' % MAP,
            '- Quotes: send photos of the damage on WhatsApp; the final price is confirmed after inspection.', '', '## Pages', '']
    llms += ['- [%s](%s%s): %s' % (p['h1'], SITE, path, p['desc']) for path, p in PAGES.items()]
    write('llms.txt', '\n'.join(llms) + '\n')
    # static files
    import shutil
    for d in ('assets',):
        src = os.path.join(HERE, d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(OUT, d), dirs_exist_ok=True)
    for f in ('favicon.ico', 'wc.css', 'wc.js'):
        shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
    print('pages', len(PAGES))


if __name__ == '__main__':
    main()

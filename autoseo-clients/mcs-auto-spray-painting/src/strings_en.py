"""English copy for the MCS Auto Spray Painting preview. Same keys in strings_ms.py and strings_zh.py (build.py checks).
Facts (address, numbers, hours, links, rating) live in facts.json; this file holds words only."""

UI = {
    'skip': 'Skip to content', 'menu': 'Menu', 'close': 'Close menu', 'lang': 'Language', 'breadcrumb': 'Breadcrumb',
    'home': 'Home', 'services': 'Services', 'about': 'About', 'contact': 'Contact', 'articles': 'Articles', 'privacy': 'Privacy',
    'wa_btn': 'WhatsApp us a photo', 'wa_short': 'WhatsApp', 'call_btn': 'Call 016-556 2998', 'call_short': 'Call',
    'facebook': 'Facebook', 'tiktok': 'TikTok', 'youtube': 'YouTube', 'maps': 'Open in Google Maps', 'directions': 'Get directions',
    'reviews': 'Read our Google reviews', 'email_h': 'Email',
    'hours_h': 'Opening hours', 'address_h': 'Workshop', 'contact_h': 'Talk to us', 'find_h': 'Find us',
    'closed': 'Closed', 'today': 'Today',
    'prev': 'Previous photo', 'next': 'Next photo', 'gallery_label': 'Finished cars and booth photos',
    'zones_label': 'Choose a service', 'see_service': 'More about this service', 'all_services': 'All services',
    'other_services': 'Other services', 'tagline': 'Pusat Kecantikan Kereta',
    'map_title': 'Map of MCS Auto Spray Painting, Taman Bukit Indah',
}

# Opening hours rows (facts.json hours, Google Business Profile 20 Nov 2026). Tuesday closed.
HOURS = [('Monday', '9:00am to 7:00pm'), ('Tuesday', 'Closed'), ('Wednesday to Friday', '9:00am to 5:00pm'), ('Saturday and Sunday', '9:00am to 7:00pm')]
HOURS_SHORT = 'Mon, Sat, Sun 9am to 7pm. Wed to Fri 9am to 5pm. Tuesday closed.'

PREFILL = {
    'default': "Hi MCS Auto Spray Painting, I'd like to ask about spray painting / body repair. Model and year: ",
    'spray-painting': "Hi MCS Auto Spray Painting, I'd like a quote for spray painting. Model and year: ",
    'custom-colour': "Hi MCS Auto Spray Painting, I'd like to ask about a custom colour. Model and year: ",
    'body-repair': "Hi MCS Auto Spray Painting, I need accident body repair. Model and year: ",
    'paint-protection': "Hi MCS Auto Spray Painting, I'd like to ask about Nippon AI-PPS paint protection. Model and year: ",
    'rims-calipers-engine': "Hi MCS Auto Spray Painting, I'd like to paint my rims / calipers / engine bay. Model and year: ",
    'interior-repair': "Hi MCS Auto Spray Painting, I'd like to ask about seat / interior repair. Model and year: ",
    'carbon-bodykits': "Hi MCS Auto Spray Painting, I'd like to ask about carbon-fibre repair / a body kit. Model and year: ",
    'insurance-windscreen': "Hi MCS Auto Spray Painting, I'd like help with an insurance / windscreen claim. Model and year: ",
    'motorbike': "Hi MCS Auto Spray Painting, I'd like to ask about motorbike spray work. Bike model: ",
}

CHIPS = {'cyan': 'Candy cyan', 'green': 'Racing green', 'black': 'Gloss black'}

HOME = {
    'title': 'Spray Painting & Body Repair in Bukit Indah, Johor | MCS Auto Spray Painting',
    'meta': 'MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri: full and panel spray painting, custom candy and pearl colours, accident body repair and insurance claims. WhatsApp 016-556 2998.',
    'h1': 'Spray painting and body repair in Bukit Indah, Johor.',
    'chips_label': 'Finishes from real jobs',
    'promise_h': 'One workshop for paint, body and interior',
    'promise': [
        'MCS Auto Spray Painting is a bengkel cat kereta and body shop on Jalan Indah 16/11, Taman Bukit Indah, Iskandar Puteri. Full-car and panel spray painting, custom candy and pearl colours, accident body repair and insurance claims all happen under one fascia: Pusat Kecantikan Kereta.',
        'Send a photo of your car on WhatsApp and tell us what you have in mind. We reply with what the job needs.',
    ],
    'zones_h': 'What do you want done?',
    'zones_p': 'Tap a service to see a real job from our workshop.',
    'process_h': 'From colour chat to collection',
    'process_p': 'Four steps, the same for a scuffed bumper or a full colour change.',
    'proof_h': 'Finished cars, fresh from the booth',
    'proof_line': '4.5 on Google from 65 reviews',
    'proof_themes': 'Drivers mention quick WhatsApp updates, patient colour advice, candy-blue paint jobs, accident repairs and motorbike spray work.',
    'hours_h': 'Visit the workshop',
    'hours_p': 'Closed on Tuesday. Wednesday to Friday we close at 5:00pm.',
    'band_h': 'Got a scratch, a dent or a colour in mind?',
    'band_p': 'WhatsApp a photo to 016-556 2998 with your car model and year.',
}

STEPS = [
    ('WhatsApp colour consult', 'Send photos of the car and the colour or damage. We talk through the finish and what the job needs.'),
    ('Body prep and repair', 'Dents and damaged panels are repaired, sanded and masked so only the right surfaces get paint.'),
    ('Spray booth and clear coat', 'Colour goes on inside the spray booth, then a clear coat for depth and gloss.'),
    ('Collect your car', 'Pick up your car at Jalan Indah 16/11 and look over the finish with us.'),
]

SERVICE_ORDER = ['spray-painting', 'custom-colour', 'body-repair', 'paint-protection', 'polish-coating', 'rims-calipers-engine',
                 'interior-repair', 'carbon-bodykits', 'insurance-windscreen', 'motorbike']

SERVICES = {
    'spray-painting': {
        'zone': 'Spray painting', 'short': 'Full-car and panel respray in our own spray booth.',
        'title': 'Car Spray Painting in Bukit Indah, Iskandar Puteri | MCS Auto Spray Painting',
        'meta': 'Full-car and panel spray painting at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. Spray booth work, WhatsApp a photo for a quote.',
        'h1': 'Car spray painting in Bukit Indah',
        'lead': 'Full-car resprays and single-panel touch-ups, painted inside our spray booth on Jalan Indah 16/11.',
        'paras': ['Faded roof, a scraped door or a whole new colour: we prep the surface, mask what should stay untouched and spray inside the booth, then finish with clear coat.',
                  'Send us photos on WhatsApp with the model and year so we can tell you what the job involves.'],
        'points': ['Full-car respray', 'Single panels, bumpers and doors', 'Colour matched to your car', 'Booth spray and clear coat'],
    },
    'custom-colour': {
        'zone': 'Custom colour', 'short': 'Candy, pearl and colour-flip finishes, and colour matching.',
        'title': 'Custom Car Colour, Candy & Pearl Paint in Johor Bahru | MCS Auto Spray Painting',
        'meta': 'Custom colour matching with candy and pearl finishes at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri. See our candy-cyan Toyota Vellfire.',
        'h1': 'Custom colour, candy and pearl finishes',
        'lead': 'The candy-cyan Toyota Vellfire on this site was painted in our booth. Bring us your colour idea.',
        'paras': ['Custom colour starts with a conversation. Share a photo, a colour you like or a sample, and we talk through how it will look in daylight, in shade and at night.',
                  'We also colour-match existing paint, so a repaired panel sits right next to the original.'],
        'points': ['Candy, pearl and colour-flip finishes', 'Colour matching for repairs', 'Full colour changes', 'Advice before any paint is mixed'],
        'posted': 'Posted on our Facebook page:',
        'posted_aikka': 'Aikka two-tone crystal colour job',
    },
    'body-repair': {
        'zone': 'Body repair', 'short': 'Knocking, dent and accident repair, then a matched respray.',
        'title': 'Accident Body Repair in Bukit Indah, Johor | MCS Auto Spray Painting',
        'meta': 'Accident body repair at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri: dents, damaged panels and bumpers repaired and resprayed in our booth.',
        'h1': 'Accident body repair in Bukit Indah',
        'lead': 'Knocking and dent work, cracked bumpers and damaged panels repaired, then painted to match.',
        'paras': ['After a knock, send us photos of the damage from a few angles. We look at what can be repaired and what needs replacing, then prep and respray in the booth.',
                  'If the repair goes through your insurer, we can help with the claim too.'],
        'points': ['Knocking and dent repair', 'Accident panel and bumper repair', 'Paint matched to the rest of the car', 'Insurance claim help'],
    },
    'paint-protection': {
        'zone': 'Nippon AI-PPS', 'short': 'Spray-on paint protection film, clear or coloured, no seams or glue.',
        'title': 'Nippon AI-PPS Paint Protection in Iskandar Puteri | MCS Auto Spray Painting',
        'meta': 'Nippon AI-PPS spray-on paint protection film, clear or coloured, at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. WhatsApp 016-556 2998.',
        'h1': 'Nippon AI-PPS paint protection',
        'lead': 'Nippon AI-PPS is sprayed on as a clear or coloured protective film, with no seams and no glue.',
        'paras': ['Because it is sprayed on, AI-PPS covers the panel without the joins or glue lines of a stuck-on film. It helps the paint resist stone chips and light scratches, and light marks can be polished out.', 'It suits a car fresh from a respray or a car whose paint you want to keep looking good. WhatsApp us your model and year and we will explain how it is applied.'],
        'points': ['Clear or coloured finish', 'Sprayed on: no seams, no glue', 'Helps resist stone chips and light scratches', 'Light marks can be polished out'],
    },
    'rims-calipers-engine': {
        'zone': 'Rims and calipers', 'short': 'Rim, brake caliper and engine-bay painting.',
        'title': 'Rim, Brake Caliper & Engine Bay Painting in Johor | MCS Auto Spray Painting',
        'meta': 'Rim, brake caliper and engine-bay painting at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. WhatsApp a photo for a quote.',
        'h1': 'Rim, caliper and engine-bay painting',
        'lead': 'Colour on the details: rims, brake calipers and the engine bay.',
        'paras': ['A new colour on the rims or calipers changes how the whole car looks. We also paint engine-bay parts.',
                  'Tell us the colour you want and send a photo of the rims or calipers as they are now.'],
        'points': ['Rim painting', 'Brake caliper painting', 'Engine-bay painting', 'Colours to match or contrast your car'],
    },
    'interior-repair': {
        'zone': 'Interior and seats', 'short': 'Leather seat repair and reupholstery, diamond-quilt and custom colours, steering wheel and roof lining.',
        'title': 'Car Seat & Interior Repair, Reupholstery in Bukit Indah | MCS Auto Spray Painting',
        'meta': 'Seat, steering-wheel and roof-lining repair, reupholstery and door-card retrims at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri.',
        'h1': 'Seat and interior repair, reupholstery',
        'lead': 'Torn seats, a worn steering wheel or a sagging roof lining, fixed in our upholstery bay.',
        'paras': ['Our interior bay handles leather seat repair and reupholstery, including diamond-quilt stitching and custom colours, plus steering-wheel and roof-lining repair and door-card retrims. The two-tone beige and black seats and door card on this page are one of our retrims.',
                  'Send photos of the interior and tell us the look you want.'],
        'points': ['Leather seat repair and reupholstery', 'Diamond-quilt stitching and custom colours', 'Steering-wheel and roof-lining repair', 'Door-card retrims'],
    },
    'carbon-bodykits': {
        'zone': 'Carbon and body kits', 'short': 'Carbon-fibre repair and custom body kits.',
        'title': 'Carbon Fibre Repair & Custom Body Kits in Johor Bahru | MCS Auto Spray Painting',
        'meta': 'Carbon-fibre repair and custom body kits at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. WhatsApp 016-556 2998.',
        'h1': 'Carbon-fibre repair and custom body kits',
        'lead': 'Carbon-fibre parts repaired and custom body kits fitted and painted.',
        'paras': ['Cracked or scuffed carbon-fibre parts can often be repaired. We also fit custom body kits and paint them to suit the car.',
                  'WhatsApp us photos of the part or the kit you are planning, with your model and year.'],
        'points': ['Carbon-fibre repair', 'Custom body kits', 'Kits painted to match', 'Photos first, then advice'],
    },
    'insurance-windscreen': {
        'zone': 'Insurance and windscreen', 'short': 'Help with insurance and windscreen claims.',
        'title': 'Insurance Claim Spray & Windscreen Claims in Johor | MCS Auto Spray Painting',
        'meta': 'Insurance claims and windscreen claims at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. WhatsApp us your claim details.',
        'h1': 'Insurance and windscreen claims',
        'lead': 'Accident repair through your insurer, and windscreen claims, handled at our workshop.',
        'paras': ['After an accident, WhatsApp us photos of the damage and tell us who your insurer is. We will tell you what we need from you to start the claim.',
                  'Windscreen claims are handled the same way: send a photo of the crack or chip.'],
        'points': ['Accident insurance claims', 'Windscreen claims', 'Repair and respray after approval', 'Tell us your insurer on WhatsApp'],
    },
    'motorbike': {
        'zone': 'Motorbike spray', 'short': 'Spray work and colour changes for motorbikes.',
        'title': 'Motorbike Spray Painting in Bukit Indah, Johor | MCS Auto Spray Painting',
        'meta': 'Motorbike spray painting at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. WhatsApp a photo of your bike.',
        'h1': 'Motorbike spray painting',
        'lead': 'Bikes come through our workshop too, for spray work and colour changes.',
        'paras': ['Motorbike spray work is something riders mention in our Google reviews. Send a photo of the bike and the parts you want painted.',
                  'The green bike in these photos was on our workshop floor, beside the upholstery bay.'],
        'points': ['Motorbike spray work', 'Colour changes and repaints', 'Send a photo of the bike first', 'Same workshop as our car jobs'],
    },
}

SERVICES_PAGE = {
    'title': 'Spray Painting, Body Repair & Interior Services in Bukit Indah | MCS Auto Spray Painting',
    'meta': 'All services at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri: spray painting, custom colour, body repair, Nippon AI-PPS, rims, interior, carbon, claims and motorbikes.',
    'h1': 'Our services',
    'lead': 'Paint, body, interior and claims, all at one workshop on Jalan Indah 16/11.',
    'one_stop_h': 'One-stop auto service',
    'one_stop': 'The MCS AUTO DETAILER fascia sits on the bay next door on the same shopfront, part of the same workshop.',
}

ABOUT = {
    'title': 'About MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri',
    'meta': 'MCS Auto Spray Painting is a multi-bay paint and body workshop on Jalan Indah 16/11, Taman Bukit Indah, Iskandar Puteri, Johor. Pusat Kecantikan Kereta.',
    'h1': 'About MCS Auto Spray Painting',
    'lead': 'Pusat Kecantikan Kereta: a car beauty centre on Jalan Indah 16/11.',
    'sign_h': 'Look for the dark fascia',
    'sign_p': 'Our signboard reads Pusat Kecantikan Kereta, with the MCS BODY & PAINT shield and red-and-white MCS AUTO SPRAY PAINTING lettering. The workshop runs across several bays of the same shopfront, with the MCS AUTO DETAILER fascia on the bay next door.',
    'unit_h': 'Unit 57 and the spray booth',
    'unit_p': 'The gold 57 on the beam marks our main unit. Inside are the spray booth, the paint bench and the upholstery bay. You will see 3M, HyperTint and HyperFilm signage around the workshop.',
    'contact_h': 'Who to ask for',
    'contact_p': 'When you WhatsApp or call 016-556 2998, ask for Ah Long (小龙).',
    'area_p': 'We serve drivers in Taman Bukit Indah, Iskandar Puteri and the wider Johor Bahru area.',
}

CONTACT = {
    'title': 'Contact MCS Auto Spray Painting, Bukit Indah | WhatsApp 016-556 2998',
    'meta': 'MCS Auto Spray Painting, No. 57, Jalan Indah 16/11, Taman Bukit Indah, 79000 Iskandar Puteri, Johor. WhatsApp or call 016-556 2998. Closed Tuesday.',
    'h1': 'Contact and directions',
    'lead': 'WhatsApp is the fastest way to reach us. Send a photo of the car with your model and year.',
    'map_h': 'On the map',
    'ask_for': 'Ask for Ah Long (小龙).',
}

PRIVACY = {
    'title': 'Privacy | MCS Auto Spray Painting',
    'meta': 'How MCS Auto Spray Painting handles the details you send when you contact us.',
    'h1': 'Privacy',
    'body': [
        ('What we receive', 'When you WhatsApp, call or email us, we receive the details you choose to send, such as your name, number, car model and photos of the car.'),
        ('How we use it', 'We use these details only to reply to you, quote and carry out work on your car. We do not sell your details.'),
        ('Website taps', 'This website counts taps on its contact buttons (WhatsApp, call, email, map) to see which buttons are used. It does not record your name or number.'),
        ('Your choices', 'To ask what we hold about you or to have it removed, email mcs01092020@gmail.com or WhatsApp 016-556 2998.'),
    ],
}

ARTICLES = {
    'title': 'Spray Painting & Body Repair Articles | MCS Auto Spray Painting',
    'meta': 'Articles on car spray painting, colour and body repair from MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri.',
    'h1': 'Articles',
    'empty': 'Articles from the workshop will appear here soon. Until then, WhatsApp us your question.',
}

# alt text / captions for the real photos (facts.json captions, shortened; no names for people in handover)
PHOTOS = {
    'cover': 'Candy-cyan Toyota Vellfire in front of the MCS Auto Spray Painting shopfront on Jalan Indah 16/11, Taman Bukit Indah',
    'vellfire-front': 'Front of the candy-cyan Vellfire after its colour job, on a Bukit Indah street',
    'vellfire-rear': 'Rear of the same Vellfire, showing the pearl finish in daylight',
    'vellfire-unit-57': 'The Vellfire inside unit 57, under the MCS AUTO SPRAY PAINTING sign',
    'vellfire-booth': 'The Vellfire mid-job in the spray booth, windows masked with paper and tape',
    'handover': 'Thumbs up with the finished candy-cyan Vellfire',
    'mclaren-shopfront': 'A gloss-black McLaren under the MCS AUTO SPRAY PAINTING fascia',
    'lotus-booth': 'A racing-green Lotus in the MCS spray booth during a lion-dance visit',
    'panels-booth': 'Freshly painted red and black panels on stands in the spray booth',
    'shopfront-booth': 'Spray booth doors and technicians under the MCS fascia',
    'signboard': 'MCS fascia: Pusat Kecantikan Kereta, the MCS BODY & PAINT shield and MCS AUTO SPRAY PAINTING lettering',
    'motorbike': 'A green adventure motorcycle on the MCS workshop floor',
    'upholstery-bay': 'The upholstery bay with seats and rolls of material',
    'door-panel': 'Door card retrimmed in two-tone beige and black with white stitching',
    'seats': 'Front seats retrimmed in two-tone beige and black',
}

SCHEMA = {
    'description': 'Auto spray painting and body repair workshop in Taman Bukit Indah, Iskandar Puteri, Johor: full and panel spray painting, custom candy and pearl colours, accident body repair, Nippon AI-PPS paint protection, polishing, ceramic coating and PPF, interior repair, insurance and windscreen claims, motorbike spray.',
}

LLMS = {
    'intro': 'Auto spray painting, body repair and interior workshop in Taman Bukit Indah, Iskandar Puteri, Johor Bahru, Malaysia. Signboard: Pusat Kecantikan Kereta.',
}

# ---------- Facebook enrichment (Edwin, 20 Nov 2026): new service, home bands, new photos ----------
PREFILL.update({
    'polish-coating': "Hi MCS Auto Spray Painting, I'd like to ask about polishing / ceramic coating / PPF. Model and year: ",
    'photo': "Hi MCS Auto Spray Painting, here is a photo of my car. Model and year: ",
    'colour-consult': "Hi MCS Auto Spray Painting, I'd like to book a colour consultation at your colour lounge. Model and year: ",
})
SERVICES['polish-coating'] = {
    'zone': 'Polish, coating and PPF', 'short': 'Polishing, ceramic coating and PPF or wrapping.',
    'title': 'Car Polishing, Ceramic Coating & PPF in Bukit Indah | MCS Auto Spray Painting',
    'meta': 'Polishing, ceramic coating and PPF / wrapping at MCS Auto Spray Painting, Taman Bukit Indah, Iskandar Puteri, Johor. WhatsApp 016-556 2998.',
    'h1': 'Polishing, ceramic coating and PPF',
    'lead': 'Finishing work for new or existing paint: polishing, ceramic coating, and PPF or wrapping.',
    'paras': ['After a respray, or on paint that has lost its shine, polishing brings the gloss back. Ceramic coating and PPF or wrapping add a layer on top of the paint.',
              'Tell us on WhatsApp which one you have in mind, with your model and year, and send a photo of the paint as it is now.'],
    'points': ['Polishing', 'Ceramic coating', 'PPF and wrapping', 'Photo first, then advice'],
}
SERVICES_PAGE.update({
    'paint_h': 'Paint systems',
    'paint_p': 'We work with an AkzoNobel paint system alongside Nippon AI-PPS; you will see the signage in the shop.',
})
UI.update({'alt_suffix': ', MCS Auto Spray Painting, Iskandar Puteri'})
HOME.update({
    'ba_h': 'Before and after', 'ba_p': 'Real MCS jobs, straight from our workshop.', 'ba_wa': 'Send us a photo of your car',
    'ba_label': 'Before and after photos',
    'show_h': 'See the colour before you choose it',
    'show_p': 'Come into our colour lounge and look at real painted sample panels: solids, candy, pearl, chameleon colour-shift, holographic and carbon-weave.',
    'show_wa': 'Book a colour consultation', 'show_label': 'Colour sample walls',
    'reels_h': 'Watch real jobs on Facebook Reels', 'reels_p': 'Short clips from the workshop, posted on our Facebook page.',
    'reel_tag': 'Facebook Reel', 'reel_views': '22K+ views on Facebook', 'reels_label': 'Facebook Reels',
    'reels': ['Nippon AI-PPS spray-on protection demo', 'Blue pearl paint that shifts colour in the light', 'See all MCS Reels on Facebook'],
})
# alt text (what is visible; the page adds UI['alt_suffix']) for the photos from the MCS Facebook page (drop 6affdd2345c3eab90d6f61ce)
PHOTOS.update({
    'bmw-candy-red-hero': 'Glossy candy-red BMW 3-Series after a full respray, three-quarter front view, MCS AUTO SPRAY PAINTING plate frame',
    'bmw-candy-red-front': 'The same candy-red BMW 3-Series head-on, LED headlights on and trees reflected in the bonnet',
    'bmw-gloss-detail': 'Close-up of the candy-red BMW front wing, headlight and alloy wheel, showing the depth of the gloss',
    'bmw-before-after-front': 'Before and after: BMW 3-Series front in white, then in glossy candy red',
    'bmw-before-after-rear': 'Before and after: BMW 318i rear in white, then in glossy candy red',
    'bmw-seats-before-after': 'Before and after: worn black leather BMW front seats, then re-trimmed in red leather with black side panels',
    'bmw-red-black-front-seat': 'Red-and-black leather front seat in the BMW, seen through the open door',
    'colour-showroom': 'MCS colour lounge with walls of painted colour samples, a table and velvet chairs',
    'swatch-wall-candy': 'Swatch wall of carbon-look, flake, chameleon, blue, yellow, green and red samples',
    'swatch-wall-chameleon': 'Purple-blue chameleon colour-shift samples above yellow, blue, silver and holographic samples',
    'swatch-panels-carbon-pearl': 'Wood-pattern and carbon-weave sample panels above pearl and holographic samples',
    'honda-accord-two-tone-4x5': 'Green Honda Accord with a black carbon-look bonnet, LED headlight and gold wheel',
    'burgundy-diamond-seat': 'Burgundy leather bench seat with diamond-quilt stitching',
    'tan-diamond-seat': 'Tan leather seat with diamond-quilted centre panels inside the MCS shop',
})
CAPS = {  # short captions for the new photos
    'bmw-candy-red-hero': 'Candy-red BMW 3-Series respray',
    'bmw-candy-red-front': 'Same BMW, head-on',
    'bmw-gloss-detail': 'Gloss depth on the candy-red BMW',
    'bmw-before-after-front': 'BMW 3-Series: white to candy red, front',
    'bmw-before-after-rear': 'Same BMW, rear',
    'bmw-seats-before-after': 'BMW seats: worn black leather to red-and-black re-trim',
    'bmw-red-black-front-seat': 'Red-and-black BMW front seat',
    'colour-showroom': 'Our colour lounge',
    'swatch-wall-candy': 'Solids, candy and flake samples',
    'swatch-wall-chameleon': 'Chameleon colour-shift and holographic samples',
    'swatch-panels-carbon-pearl': 'Carbon-weave and pearl samples',
    'honda-accord-two-tone-4x5': 'Green and black two-tone Honda Accord with carbon-look bonnet',
    'burgundy-diamond-seat': 'Burgundy diamond-stitch leather seat',
    'tan-diamond-seat': 'Tan diamond-quilted seat rebuild',
}

# JT Autoworks, English copy. Every key here must exist in strings_ms.py and strings_zh.py (build fails otherwise).
# Facts (numbers, address, prices, hours) come from facts.json; {placeholders} are filled by build.py.
# Rules: no em dashes, no invented facts, owner name only through {tech} (build fills "our technician" while the flag is off).

UI = {
    'skip': 'Skip to content',
    'menu': 'Menu', 'close': 'Close menu', 'lang': 'Language',
    'wa_btn': 'WhatsApp us', 'wa_short': 'WhatsApp', 'call_btn': 'Call 6222 3102', 'call_short': 'Call',
    'home': 'Home', 'packages': 'Packages', 'services': 'Services', 'find_us': 'How to find us', 'about': 'About',
    'areas': 'Areas we serve', 'articles': 'Articles', 'privacy': 'Privacy',
    'breadcrumb': 'Breadcrumb',
    'prev': 'Previous photo', 'next': 'Next photo',
    'play': 'Play video', 'tap_sound': 'Tap for sound', 'load_fb': 'Plays from Facebook after you tap',
    'watch_more': 'Watch more on Facebook',
    'hours_h': 'Opening hours', 'mon_fri': 'Monday to Friday', 'sat': 'Saturday', 'sun': 'Sunday', 'closed': 'Closed',
    'hours_mf': '9:00am to 5:00pm', 'hours_sat': '9:00am to 3:00pm', 'hours_short': 'Mon to Fri 9am to 5pm, Sat 9am to 3pm, Sun closed',
    'address_h': 'Workshop address', 'contact_h': 'Talk to us',
    'maps': 'Open in Google Maps', 'directions': 'Get directions', 'reviews': 'Read our Google reviews', 'write_review': 'Write a Google review',
    'facebook': 'Facebook', 'instagram': 'Instagram', 'email': 'Email',
    'credit': 'Website by AutoSEO.my',
    'per_litre': 'per extra litre', 'litres': 'litres', 'for3': 'for 3 services',
    'pkg_wa': 'WhatsApp about Package {L}',
    'see_packages': 'See the three packages', 'see_services': 'All services', 'see_find': 'How to find us',
    'faq_h': 'Questions people ask',
    'map_title': 'Map of JT Autoworks at Premier @ Kaki Bukit',
    'all_makes': 'All makes welcome.',
    'reel_more': 'More clips from the workshop',
    'legal': 'JT AUTOWORKS PTE. LTD.',
}

TECH = 'our technician'          # used while facts.flags.show_owner_name is false
TECH_CAP = 'Our technician'

# ---------- WhatsApp prefills (per page / per button) ----------
PREFILL = {
    'default': "Hi JT Autoworks, I'd like to ask about my car. Car model and year: ",
    'home': "Hi JT Autoworks, I'd like to ask about my car. Car model and year: ",
    'pkg_a': "Hi JT Autoworks, I'd like to ask about Package A (Liqui Moly Top Tec, 6L, $628).",
    'pkg_b': "Hi JT Autoworks, I'd like to ask about Package B (Castrol Edge, 6L, $528).",
    'pkg_c': "Hi JT Autoworks, I'd like to ask about Package C (Castrol Edge, 4L, $428).",
    'packages': "Hi JT Autoworks, I'd like to ask which service package suits my car. Car model and year: ",
    'services': "Hi JT Autoworks, I'd like to ask about a repair. Car model and year: ",
    'diagnostics': "Hi JT Autoworks, I'd like a diagnosis. What the car is doing: ",
    'aircon': "Hi JT Autoworks, my aircon is not cold. Car model and year: ",
    'battery': "Hi JT Autoworks, I'd like my battery tested. Car model and year: ",
    'ev': "Hi JT Autoworks, I'd like to ask about my EV. Model and year: ",
    'ppi': "Hi JT Autoworks, I'd like a pre-purchase inspection. Car model and year: ",
    'towing': "Hi JT Autoworks, I need a tow. My location: ",
    'german': "Hi JT Autoworks, I'd like to ask about my car. Make, model and year: ",
    'find_us': "Hi JT Autoworks, I need directions to #02-52, Gate 1.",
    'about': "Hi JT Autoworks, I'd like to ask about my car. Car model and year: ",
    'areas': "Hi JT Autoworks, I'd like to bring my car in. Car model and year: ",
    'articles': "Hi JT Autoworks, I'd like to ask about my car. Car model and year: ",
    'privacy': "Hi JT Autoworks, I have a question.",
    'reel_aircon': "Hi JT Autoworks, my aircon is not cold. Car model and year: ",
    'reel_battery': "Hi JT Autoworks, I'd like my battery tested. Car model and year: ",
    'reel_ev_light': "Hi JT Autoworks, my EV has a warning light on. Model and year: ",
    'reel_dash_lights': "Hi JT Autoworks, I have a warning light on my dashboard. Car model and year: ",
    'reel_ev_owners': "Hi JT Autoworks, I'd like to ask about servicing my EV. Model and year: ",
    'reel_diagnostics': "Hi JT Autoworks, I'd like a diagnosis. What the car is doing: ",
    'reel_used_car': "Hi JT Autoworks, I'd like a pre-purchase inspection. Car model and year: ",
    'reel_oil_leak': "Hi JT Autoworks, I think my car has an oil leak. Car model and year: ",
    'reel_bmw5': "Hi JT Autoworks, my car is jerking. Car model and year: ",
    'reel_new_chapter': "Hi JT Autoworks, I'd like to ask about my car. Car model and year: ",
}

# ---------- Reel captions (plain language, not the promo text) ----------
REELS = {
    'aircon': 'Aircon not cold? Find the leak first.',
    'battery': 'Battery test before any replacement.',
    'ev_light': 'An EV warning light, checked properly.',
    'dash_lights': 'What your dashboard lights are telling you.',
    'ev_owners': 'Servicing for EV owners after warranty.',
    'diagnostics': 'Root cause first, then the repair.',
    'used_car': 'Check a used car before you pay.',
    'oil_leak': 'Tracing an oil leak to the source.',
    'bmw5': 'A BMW 5 Series jerking fault, found.',
    'new_chapter': 'Our new workshop at Premier @ Kaki Bukit.',
}

# ---------- Shared blocks ----------
PKG = {
    'h2': 'Service packages',
    'lead': 'Three packages, each covering 3 services. Prices are shown in full.',
    'name': 'Package {L}',
    'oil_line': '{oil}, {litres}L engine oil',
    'extra': 'Extra oil ${x} per litre',
    'inc_h': 'Included in every package',
    'common': {
        'oil_filter': 'Oil filter x{n}',
        'check_50': '50-point check x{n}',
        'aircon_flush_gas': 'Aircon flushing and gas top-up x{n}',
        'tyre_rotation': 'Tyre rotation x{n}',
        'tyre_patch': 'Tyre patching x{n}',
        'coolant': 'Coolant top-up, up to 10L, x{n}',
    },
    'flush': 'Liqui Moly engine flush, oil additive and injection cleaner',
    'windshield': 'Liqui Moly windshield cleaner 50ml',
    'no_flush': 'No flush bundle or windshield cleaner',
    'brake_fluid': 'Brake fluid flushing is done only when brake pads are changed.',
    'lifetime': 'Package customers get lifetime free checking.',
    'visc': 'Oil grades on the posters: {v}.',
    'poster_alt': 'JT Autoworks Package {L} price poster',
    'combined_alt': 'JT Autoworks service packages A, B and C side by side',
}

PROCESS = {
    'h2': 'How a job runs here',
    'lead': 'Diagnosis comes before parts.',
    'steps': [
        ('WhatsApp us', 'Tell us the car and what it is doing. A short video helps.'),
        ('Inspect and diagnose', 'We find the root cause before we talk about parts.'),
        ('Quote, no charge', 'You get a quote with no obligation and no charge.'),
        ('Repair only what is needed', 'Parts are replaced only when they really need replacing.'),
        ('Collect your car', 'Your car is in good hands.'),
    ],
}

PROOF = {
    'h2': 'Why drivers come back',
    'items': [
        ('$50 labour', 'A turbo problem quoted near $2,000 elsewhere was fixed here for $50 labour, with no components charged.'),
        ('The fault another workshop missed', 'A BMW 5 Series that kept jerking had been seen elsewhere. We traced the real cause.'),
        ('Since 2018. One mechanic.', 'One relationship built on trust.'),
    ],
    'note': 'JT Autoworks opened at Premier @ Kaki Bukit in May 2026.',
    'reviews_line': 'Read what customers wrote on Google.',
}

PHOTOS = {
    'h2': 'Inside the workshop',
    'shopfront-corridor-tighter-4x5': 'The JT Autoworks signboard at unit #02-52',
    'mercedes-c-class-on-lift-4x5': 'A Mercedes-Benz on the lift at JT Autoworks',
    'volkswagen-golf-cabriolet-on-lift-4x5': 'A Volkswagen Golf Cabriolet on the lift at JT Autoworks',
    'shopfront-corridor-4x5': 'The JT Autoworks shopfront at Premier @ Kaki Bukit',
    'hero': 'The JT Autoworks shopfront at unit #02-52, Premier @ Kaki Bukit',
}

GATE = {
    'h2': 'Find us: Gate 1, unit #02-52',
    'lead': 'Premier @ Kaki Bukit has more than 100 workshops. Come in through Gate 1 and look for our signboard at #02-52.',
    'landmarks_h': 'Landmarks near the block',
    'landmarks': {
        'Gate 1': 'Use Gate 1 of Premier @ Kaki Bukit.',
        'VICOM Inspection Centre': 'VICOM Inspection Centre is a nearby landmark.',
        'Kaki Bukit Camp': 'Kaki Bukit Camp is a nearby landmark.',
        'Bartley Rd East': 'Bartley Rd East runs nearby.',
        'POSB': 'There is a POSB nearby.',
    },
    'poster_alt': 'JT Autoworks location poster showing Gate 1 and unit #02-52',
    'poster_labels': 'The poster also marks Bike Labz, Sri Udhayan Coffee Bar, Atlas Vending Solutions and KB-1 in the block.',
    'lost': 'Lost in the block? WhatsApp us and we will guide you to #02-52.',
}

SERVICES = {
    'diagnostics': {
        'name': 'Diagnostics', 'card': 'Root cause first. No guesswork and no unnecessary parts.',
        'title': 'Car diagnostics in Kaki Bukit | JT Autoworks',
        'meta': 'Honest car diagnosis at Premier @ Kaki Bukit, Gate 1. We find the root cause first and replace only what is needed. WhatsApp 8358 4927.',
        'h1': 'Car diagnostics in Kaki Bukit, root cause first',
        'lead': 'Warning light, jerking, a noise you cannot place? We diagnose before we replace.',
        'body': [
            'Many repairs cost more than they should because parts are changed until the problem goes away. We work the other way round: proper diagnosis first, no guesswork and no unnecessary parts replacement.',
            'One turbo job quoted near $2,000 elsewhere was fixed here for $50 labour with no components charged. A BMW 5 Series jerking fault that another workshop missed was traced and fixed.',
        ],
        'list_h': 'What we look at',
        'list': ['Warning lights on the dashboard', 'Jerking, hesitation and rough running', 'Engine faults and leaks', 'Electrical faults', 'EV warning lights'],
    },
    'aircon': {
        'name': 'Aircon', 'card': 'Not cold? We find the leak first, then fix it.',
        'title': 'Car aircon repair in Kaki Bukit | JT Autoworks',
        'meta': 'Car aircon not cold? JT Autoworks at Premier @ Kaki Bukit finds the leak first, then repairs. Aircon flushing and gas top-up. WhatsApp 8358 4927.',
        'h1': 'Car aircon repair in Kaki Bukit',
        'lead': 'Topping up gas without finding the leak only buys time. We find the leak first.',
        'body': [
            'A gas top-up alone does not stop a leak. We find why the aircon is leaking before anything is replaced, then quote with no obligation and no charge.',
            'Aircon flushing and gas top-up is also part of every service package.',
        ],
        'list_h': 'Aircon work',
        'list': ['Leak finding', 'Aircon flushing', 'Gas top-up', 'Repair of the leaking part'],
    },
    'battery': {
        'name': 'Battery', 'card': 'Tested first, replaced only if needed, with registration and coding.',
        'title': 'Car battery test and replacement in Kaki Bukit | JT Autoworks',
        'meta': 'Car battery tested first at JT Autoworks, Premier @ Kaki Bukit. Replaced only if needed, with battery registration and coding. WhatsApp 8358 4927.',
        'h1': 'Car battery test and replacement in Kaki Bukit',
        'lead': 'We test the battery first. You replace it only if it needs replacing.',
        'body': [
            'A slow start is not always a dead battery. We test the battery and charging first so you do not pay for a battery you did not need.',
            'Many modern cars need the new battery registered and coded to the car. We do that as part of the job.',
        ],
        'list_h': 'Battery work',
        'list': ['Battery and charging test', 'Replacement only when needed', 'Battery registration and coding'],
    },
    'ev': {
        'name': 'EV diagnostics and servicing', 'card': 'EV-trained technicians. An affordable choice after warranty.',
        'title': 'EV workshop in Kaki Bukit | JT Autoworks',
        'meta': 'EV diagnostics and servicing at Premier @ Kaki Bukit by EV-trained technicians. An affordable alternative after manufacturer warranty. WhatsApp 8358 4927.',
        'h1': 'EV workshop in Kaki Bukit for diagnostics and servicing',
        'lead': 'EV-trained technicians, diagnose-first, after your manufacturer warranty ends.',
        'body': [
            'Once the manufacturer warranty is over, many EV owners look for an affordable alternative. Our EV-trained technicians handle EV diagnostics and servicing at Premier @ Kaki Bukit.',
            'EV warning lights get the same treatment as any other fault: we find the cause before anything is replaced. Towing can be arranged for EVs too.',
        ],
        'list_h': 'EV work',
        'list': ['EV warning light diagnosis', 'EV servicing', 'Towing arranged for EVs'],
        'tags': 'Owners of these EVs ask us often:',
    },
    'ppi': {
        'name': 'Pre-purchase inspection', 'card': 'Check a used car properly before you pay for it.',
        'title': 'Pre-purchase car inspection in Kaki Bukit | JT Autoworks',
        'meta': 'Used-car pre-purchase inspection at JT Autoworks, Premier @ Kaki Bukit. Know what you are buying before you pay. WhatsApp 8358 4927.',
        'h1': 'Pre-purchase car inspection in Kaki Bukit',
        'lead': 'Know what you are buying before you pay for it.',
        'body': [
            'A used car can look clean and still hide an expensive problem. Bring it to us before you commit and we will inspect it and tell you plainly what we find.',
        ],
        'list_h': 'What we check',
        'list': ['Engine and gearbox', 'Brakes and suspension', 'Aircon and electronics', 'Leaks, wear and accident signs'],
    },
    'towing': {
        'name': '24/7 towing', 'card': 'Towing arranged around the clock, for cars and EVs.',
        'title': '24/7 car and EV towing arranged | JT Autoworks Kaki Bukit',
        'meta': 'Broken down? JT Autoworks arranges 24/7 towing for cars and EVs to our workshop at Premier @ Kaki Bukit, Gate 1. WhatsApp 8358 4927.',
        'h1': '24/7 towing arranged for cars and EVs',
        'lead': 'Broken down? WhatsApp us your location and we arrange the tow.',
        'body': [
            'We arrange 24/7 towing for cars and EVs to our workshop at Premier @ Kaki Bukit. Send your location and the car model on WhatsApp so we can arrange the right tow.',
            'Once the car is with us, it gets the same diagnose-first approach: root cause first, then a quote with no obligation and no charge.',
        ],
        'list_h': 'Send us on WhatsApp',
        'list': ['Your location', 'Car make and model, or EV model', 'What happened'],
    },
    'german': {
        'name': 'German and luxury cars', 'card': 'BMW, Mercedes-Benz, Audi, Porsche and more. All makes welcome.',
        'title': 'BMW, Mercedes and Audi workshop in Kaki Bukit | JT Autoworks',
        'meta': 'European and luxury car workshop at Premier @ Kaki Bukit: BMW, Mercedes-Benz, Audi, Volkswagen, Porsche, Lexus, Land Rover, Volvo. All makes welcome.',
        'h1': 'BMW, Mercedes and Audi workshop in Kaki Bukit',
        'lead': 'A European and luxury focus, with every make welcome.',
        'body': [
            'German and luxury cars are our focus: BMW, Mercedes-Benz, Audi, Volkswagen and Porsche, plus Lexus, Land Rover and Volvo. These cars reward a careful diagnosis, and punish guesswork.',
            'A BMW 5 Series that kept jerking had already been to another workshop. We traced the real fault. Whatever you drive, the approach is the same.',
        ],
        'list_h': 'Makes we focus on',
    },
}
SERVICE_ORDER = ['diagnostics', 'aircon', 'battery', 'ev', 'ppi', 'towing', 'german']
OTHER_SERVICES = {
    'h2': 'Also at the workshop',
    'items': [('Engine repairs', 'Diagnosed first, repaired properly.'), ('Brakes', 'Brake checks and repairs.'),
              ('Oil service', 'Or save with one of the three packages.'), ('50-point check', 'Included with every package service.')],
}
CHECK_50 = {
    'engine': 'Engine', 'brakes': 'Brakes', 'suspension_steering': 'Suspension and steering', 'tyres': 'Tyres',
    'electrical': 'Electrical', 'lights': 'Lights', 'fluids': 'Fluids', 'aircon': 'Aircon',
    'battery_charging': 'Battery and charging', 'exhaust': 'Exhaust', 'safety': 'Safety features', 'body_interior': 'Body and interior',
}

# ---------- Pages ----------
HOME = {
    'title': 'Diagnose-first car workshop in Kaki Bukit | JT Autoworks',
    'meta': 'JT Autoworks, car workshop at Premier @ Kaki Bukit, Gate 1, #02-52. Diagnose-first European and EV specialist, clear package prices, all makes welcome.',
    'h1': 'Diagnose-first car workshop in Kaki Bukit',
    'line': 'European and EV specialist. We fix only what is needed.',
    'chips': [('Diagnose first', 'Root cause before parts'), ('Free quote', 'No obligation, no charge'), ('#02-52, Gate 1', 'Premier @ Kaki Bukit')],
    'intro_h': 'A car workshop at Premier @ Kaki Bukit that explains before it charges',
    'intro': 'JT Autoworks is a diagnose-first car workshop in Kaki Bukit, at unit #02-52 of Premier @ Kaki Bukit. We focus on BMW, Mercedes-Benz, Audi and other European cars and on EVs, and every make is welcome. Quotes come with no obligation and no charge, and parts are replaced only when necessary.',
    'svc_h': 'What we do',
    'lounge': 'Waiting? There is a lounge with complimentary drinks.',
    'final_h': 'Tell us what your car is doing',
    'final_line': 'WhatsApp 8358 4927. A short video of the problem helps.',
    'faq': [
        ('What are your opening hours?', 'Monday to Friday 9:00am to 5:00pm, Saturday 9:00am to 3:00pm. Closed on Sunday.'),
        ('Where exactly is the workshop?', 'Unit #02-52, Premier @ Kaki Bukit, 8 Kaki Bukit Ave 4, Singapore 415875. Come in through Gate 1.'),
        ('Do you charge for a quote?', 'No. Quotes come with no obligation and no charge.'),
        ('What do the service packages include?', 'Each package covers 3 services with engine oil, an oil filter, a 50-point check and a coolant top-up every time, plus aircon flushing and gas top-up, tyre rotation and tyre patching once.'),
        ('Do you work on EVs?', 'Yes. EV-trained technicians handle EV diagnostics and servicing, and towing can be arranged for EVs.'),
        ('Which car makes do you service?', 'Our focus is BMW, Mercedes-Benz, Audi, Volkswagen, Porsche, Lexus, Land Rover and Volvo. All makes are welcome.'),
    ],
}

PACKAGES = {
    'title': 'Engine oil service packages in Kaki Bukit | JT Autoworks',
    'meta': 'Three engine oil service packages at JT Autoworks, Kaki Bukit: A $628 Liqui Moly Top Tec 6L, B $528 Castrol Edge 6L, C $428 Castrol Edge 4L. 3 services each.',
    'h1': 'Engine oil service packages in Kaki Bukit',
    'lead': 'Three packages, 3 services each, with the price shown in full.',
    'compare_h': 'All three packages on one poster',
    'faq': [
        ('How many services does a package cover?', 'Each package covers 3 services.'),
        ('What is the difference between the packages?', 'Package A uses 6L of Liqui Moly Top Tec ($628). Package B uses 6L of Castrol Edge ($528). Both include a Liqui Moly engine flush, oil additive and injection cleaner, and a 50ml Liqui Moly windshield cleaner. Package C uses 4L of Castrol Edge ($428) without the flush bundle or windshield cleaner.'),
        ('What if my car needs more oil?', 'Extra oil is $29 per litre on Package A and $20 per litre on Packages B and C.'),
        ('Which oil grades do the packages list?', 'The package posters list 5W-40, 5W-30 and 0W20.'),
        ('Is brake fluid included?', 'Brake fluid flushing is done only when brake pads are changed.'),
        ('Is there anything after the 3 services?', 'Package customers get lifetime free checking.'),
    ],
}

SERVICES_PAGE = {
    'title': 'Car repair and servicing in Kaki Bukit | JT Autoworks',
    'meta': 'Diagnostics, aircon, battery, EV servicing, pre-purchase inspection, towing and European car repair at JT Autoworks, Premier @ Kaki Bukit, Gate 1.',
    'h1': 'Car repair and servicing in Kaki Bukit',
    'lead': 'Every job starts with a diagnosis. Every make is welcome.',
}

FIND = {
    'title': 'How to find JT Autoworks at Premier @ Kaki Bukit, Gate 1',
    'meta': 'JT Autoworks is at 8 Kaki Bukit Ave 4, #02-52, Premier @ Kaki Bukit, Singapore 415875. Enter through Gate 1. Map, directions and opening hours.',
    'h1': 'How to find us at Premier @ Kaki Bukit',
    'lead': 'Come in through Gate 1, then look for unit #02-52.',
}

ABOUT = {
    'title': 'About JT Autoworks, a new workshop in Kaki Bukit',
    'meta': 'JT Autoworks opened at Premier @ Kaki Bukit in May 2026: a diagnose-first workshop for European cars and EVs, with clear prices and no-charge quotes.',
    'h1': 'About JT Autoworks',
    'lead': 'A new workshop in Kaki Bukit, built on an old habit: diagnose first.',
    'body': [
        'JT Autoworks opened at unit #02-52, Premier @ Kaki Bukit, in May 2026. The workshop is new. The approach is not.',
        'Since 2018. One mechanic. One relationship built on trust. The approach stays the same: find the real cause, fix the real problem, and replace parts only when necessary.',
        'We focus on European cars and EVs and welcome every make. Quotes come with no obligation and no charge, and the three service packages are priced in full.',
    ],
    'values_h': 'What you can expect',
    'values': [('Quick to reply', 'WhatsApp us your question and we reply quickly.'),
               ('Honest diagnosis', 'Root cause first. No guesswork and no unnecessary parts.'),
               ('Clear prices', 'Package prices in full, and quotes with no charge.'),
               ('Reliable work', 'Expert workmanship, done right the first time.')],
    'lounge': 'While you wait, there is a lounge with complimentary drinks.',
}

AREAS = {
    'title': 'Car workshop near Ubi, Eunos, Bedok and Tampines | JT Autoworks',
    'meta': 'JT Autoworks serves drivers from Kaki Bukit, Ubi, Eunos, Bedok, Tampines, Paya Lebar, MacPherson and Hougang at Premier @ Kaki Bukit, Gate 1.',
    'h1': 'Car workshop for Kaki Bukit and nearby areas',
    'lead': 'One workshop, one address: Premier @ Kaki Bukit, Gate 1, #02-52.',
    'area_h': 'Car workshop for {area} drivers',
    'area_p': 'Driving in from {area}? JT Autoworks is at Premier @ Kaki Bukit. Enter through Gate 1 and find unit #02-52. Diagnosis comes first, quotes have no charge, and the three service packages are priced in full.',
    'here_p': 'We are in Kaki Bukit itself, at Premier @ Kaki Bukit, 8 Kaki Bukit Ave 4. Enter through Gate 1 and find unit #02-52.',
}

PRIVACY = {
    'title': 'Privacy | JT Autoworks',
    'meta': 'How JT Autoworks handles the details you send when you contact us.',
    'h1': 'Privacy',
    'body': [
        ('What we collect', 'When you WhatsApp, call or email us, we receive the details you choose to send, such as your name, number, car model and photos or videos of the problem.'),
        ('How we use it', 'We use these details only to reply to you, quote and carry out work on your car. We do not sell your details.'),
        ('Website taps', 'This website counts taps on its contact buttons (WhatsApp, call, email, map) to see which buttons are used. It does not record your name or number.'),
        ('Your choices', 'To ask what we hold about you or to have it removed, email hao@jtautoworks.com.sg or WhatsApp 8358 4927.'),
    ],
}

ARTICLES = {
    'title': 'Car care articles | JT Autoworks Kaki Bukit',
    'meta': 'Car care articles from JT Autoworks, a diagnose-first workshop at Premier @ Kaki Bukit.',
    'h1': 'Car care articles',
    'empty': 'Articles from the workshop will appear here soon. Until then, WhatsApp us your question.',
}

SCHEMA = {
    'description': 'Diagnose-first car workshop at Premier @ Kaki Bukit, Gate 1, #02-52. European and EV specialist, all makes welcome.',
}
LLMS = {
    'intro': 'JT Autoworks (JT AUTOWORKS PTE. LTD.) is a diagnose-first car workshop at Premier @ Kaki Bukit, Singapore, focused on European cars and EVs, all makes welcome.',
}

# ---------- redesign blocks (20 Nov) ----------
LOOK = {
    'poster_alt': 'JT Autoworks poster: {name}',
    'kicker': 'Premier @ Kaki Bukit, Gate 1, #02-52',
    'reels_h': 'Video highlights',
    'reels_lead': 'Short clips from the workshop. Tap a video to play it.',
    'pkg_kicker': 'Clear prices',
    'quotes_h': 'In customers\' words',
    'quotes': ['His knowledge of car and repair skills is top notch.',
               'I never have any worries at all to let them handle my servicing and repairs!',
               'I believe integrity and honesty is the most important trait in car repair business.'],
    'quote_src': 'From a Google review',
    'about_more': 'About the workshop',
    'gallery_lead': 'Real photos from unit #02-52.',
}

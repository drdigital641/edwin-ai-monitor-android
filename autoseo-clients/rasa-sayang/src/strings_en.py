# English copy for the Rasa Sayang Automotive preview. Every fact comes from facts.json (Bridge drop, 19 Nov 2026).
# All visible words live here. strings_ms.py and strings_zh.py have exactly the same keys and structure (shared AutoSEO template rule).
# Never: hours, prices, reviews, ratings, staff names, founding year, opening dates, emails, warranties, awards. No em dashes in copy.

PREFILL = "Hi Rasa Sayang Automotive, I'd like to ask about my car. Model and year: "

UI = {
    "skip": "Skip to content",
    "menu": "Menu",
    "close": "Close",
    "nav_home": "Home",
    "nav_services": "Services",
    "nav_about": "About",
    "nav_articles": "Articles",
    "nav_contact": "Contact",
    "wa_btn": "WhatsApp us",
    "wa_btn_long": "WhatsApp 016-664 1686",
    "call_btn": "Call",
    "call_btn_long": "Call 016-664 1686",
    "fb_btn": "Facebook page",
    "waze_btn": "Waze",
    "map_btn": "Google Maps",
    "prev": "Previous photo",
    "next": "Next photo",
    "lang_label": "Language",
    "aria_main": "Main",
    "aria_menu": "Menu",
    "aria_pages": "Pages",
    "aria_contact": "Contact",
    "aria_breadcrumb": "Breadcrumb",
    "aria_photo": "Photo",
    "home_aria": "Rasa Sayang Automotive home",
    "logo_alt": "Rasa Sayang Automotive Group Sdn Bhd logo",
    "photo_open": "Open photo",
    "footer_hq": "Shah Alam HQ",
    "footer_subang": "Subang Jaya branch",
    "footer_talk": "Talk to us",
    "footer_pages": "Pages",
    "credit": "Website by AutoSEO.my",
    "brands_note": "Car brand names only describe the cars we work on. We are an independent workshop.",
    "reg_no": "Company no.",
    "privacy": "Privacy",
    "related": "Other services",
    "ask_title": "Tell us what the car is doing",
    "ask_line": "Send the model, year and the warning on the dash. A photo or short video helps.",
    "faq_h2": "Questions",
    "jobs_h2": "Jobs we have posted",
    "watch_fb": "Watch on Facebook",
    "reel_other": "Reel",
    "last_updated": "Last updated 19 November 2026",
    "hq_tag": "HQ",
    "branch_tag": "Branch",
    "areas_label": "We see cars from",
    "service_area_note": "Drivers come to us from across the Klang Valley.",
}

CAPTIONS = {
    "cover": "Yellow Lamborghini, white Ferrari and an orange Lamborghini in the Shah Alam bay",
    "og": "Supercars in the Rasa Sayang Automotive bay, Shah Alam",
    "porsche-taycan-ev-battery-lift": "Porsche Taycan EV on the lift for high-voltage battery work",
    "porsche-taycan-ev-diagnostics": "Diagnostic tablet connected to a Porsche Taycan",
    "volvo-xc90-t8-hybrid-battery-work": "Volvo XC90 T8 hybrid battery pack out on the floor",
    "volvo-xc90-t8-hybrid-battery-modules": "Close-up of Volvo XC90 T8 battery modules",
    "volvo-xc90-t8-coolant-pump-hoses": "Volvo XC90 T8 coolant pump and hoses on a fender cover",
    "volvo-xc90-t8-erad-parts": "Volvo XC90 T8 ERAD parts laid out",
    "volvo-xc90-t8-erad-bay": "Volvo XC90 T8 in the bay for ERAD motor work",
    "volvo-xc90-t8-hybrid-bdu": "Volvo XC90 T8 hybrid battery disconnect unit",
    "volvo-xc60-t8-coolant-pumps": "Volvo XC60 T8 coolant pumps on a fender cover",
    "volvo-xc60-t8-obc-control-units": "Volvo XC60 T8 onboard charger and control units",
    "volvo-xc60-t8-fuel-pump-module": "Volvo XC60 T8 fuel pump module",
    "ferrari-488-gear-knob-internals": "Ferrari 488 gear knob opened up",
    "ferrari-488-gear-knob-panel": "Ferrari 488 gear knob panel on the bench",
    "bmw-x5-f15-gearbox-flywheel": "BMW X5 F15 gearbox and flywheel work on the lift",
    "lamborghini-aventador-svj-service-lift": "Lamborghini Aventador SVJ on a two-post lift",
    "lamborghini-aventador-svj-rear": "Rear of a Lamborghini Aventador SVJ in the bay",
    "supercar-service-bay-shah-alam": "Three supercars in the Shah Alam bay",
    "lamborghini-aventador-svj-front-service": "Lamborghini Aventador SVJ front service, oils ready",
    "ev-hybrid-fender-cover-coolant-pumps": "Hybrid coolant pumps on a fender cover",
    "rolls-royce-front-engine-service": "Rolls-Royce on the lift for front engine work",
    "rolls-royce-engine-overhaul-lift": "Rolls-Royce on a two-post lift, two engines on the floor",
    "rolls-royce-engines-on-floor": "Engines out on the workshop floor",
    "volvo-xc90-t8-erad-motor": "Volvo XC90 T8 ERAD motor",
    "rolls-royce-air-suspension": "Rolls-Royce air suspension work",
    "volvo-xc90-t8-brake-fluid": "Volvo XC90 T8 brake fluid service",
}

REELS = {
    "reel_purosangue": "Ferrari Purosangue car service and software reset",
    "reel_intro": "Company introduction",
}

# Jobs seen in their Facebook posts (facts.json jobs_seen_in_posts). Shown as work done, not a price menu.
JOBS = [
    "Hybrid high-voltage battery replacement: Volvo XC90 / XC60 T8, BMW X5 F15 / 45e / G05, Mercedes S400 hybrid",
    "Electric rear-axle (ERAD) motor replacement",
    "IGM, IEM, EME and DCDC module repair and programming",
    "Air suspension, air balloon and electric absorber",
    "Suspension arms and steering rack",
    "Brake pads and discs",
    "Major service and timing belt",
    "Gearbox repair and ATF",
    "Engine repair and engine mounting",
    "Aircond compressor, condenser and cooling coil",
    "Wireless Android Auto / Apple CarPlay update",
    "Software reset (Ferrari Purosangue)",
    "Turbo repair (Ferrari 488 GTB)",
]

CARS_LABEL = "Models from our posts"
CARS = ["Porsche Taycan", "Porsche Macan", "Porsche GT3", "Volvo XC90 T8", "Volvo XC60 T8", "BMW X5 F15", "BMW X5 45e", "BMW X5 G05",
        "BMW i8", "BMW M4", "BMW X6M", "Mercedes-Benz S400 Hybrid", "Mercedes-Benz C350e", "Mercedes-Benz GT", "Mercedes-Benz GTS", "Mercedes-Benz GLC", "Mercedes-Benz S-Class W223",
        "Ferrari 488 GTB", "Ferrari Purosangue", "Lamborghini Aventador SVJ", "Lamborghini Urus", "Lamborghini Huracan",
        "Rolls-Royce Cullinan", "Rolls-Royce Ghost", "Range Rover L460 PHEV", "Bentley Continental GT"]

HOME = {
    "title": "Hybrid, EV and Supercar Workshop in Shah Alam | Rasa Sayang Automotive",
    "desc": "Hybrid EV workshop in Shah Alam and Subang Jaya: high-voltage battery, ERAD, module, engine overhaul, aircond and supercar repair. WhatsApp 016-664 1686.",
    "h1": "Hybrid, EV and supercar workshop in Shah Alam",
    "hero_line": "High-voltage diagnostics and precise repair for new energy cars and supercars.",
    "intro_h2": "One bay for batteries, modules and big engines",
    "intro_p": [
        "Rasa Sayang Automotive is a new energy vehicle workshop in Selangor, with our HQ in Seksyen 26, Shah Alam and a branch in SS14, Subang Jaya.",
        "We work on high-voltage electrical systems, battery systems, electric drive systems and electronic control modules, and we take on the complex faults other shops send away.",
    ],
    "brands_label": "Makes we service",
    "spec_h2": "What we fix",
    "process_h2": "How a job runs",
    "process_steps": [
        ("WhatsApp us", "Send the model, year and the warning or fault. Photos help."),
        ("Diagnose", "We scan the high-voltage system and control modules to find the cause."),
        ("Repair", "Battery, motor, module, engine or aircond work, done in our bay."),
        ("Collect", "We tell you what was done, then you drive home."),
    ],
    "work_h2": "Cars we have worked on",
    "work_line": "Real jobs from our Shah Alam bay. Swipe or tap a photo.",
    "reels_h2": "Recent work on Facebook",
    "visit_h2": "Two workshops in Selangor",
    "visit_line": "Shah Alam HQ and Subang Jaya branch. WhatsApp before you come in.",
}

FAQ_HOME = [
    ("Do you repair hybrid and EV high-voltage batteries?",
     "Yes. We have replaced hybrid high-voltage batteries on the Volvo XC90 and XC60 T8, BMW X5 F15, 45e and G05, and the Mercedes S400 hybrid. WhatsApp us your model and year."),
    ("Where are your workshops?",
     "Our HQ is at 21, Jalan Serendah 26/40, Seksyen 26, 40400 Shah Alam. Our branch is at 10, Jalan SS14/2, SS14, 47500 Subang Jaya. Both are in Selangor."),
    ("Which makes do you work on?",
     "BMW, Mercedes-Benz, Porsche, Lamborghini, Ferrari, McLaren, Volvo, Rolls-Royce, Audi and Land Rover."),
    ("Do you help other workshops?",
     "Yes. We give technical support to other workshops on complex faults, electronic systems and new energy vehicle repairs."),
    ("What are your opening hours?",
     "Please WhatsApp 016-664 1686 before you come in and we will arrange a time."),
]

SERVICES = [
    {
        "id": "hybrid-ev", "slug": "hybrid-ev-repair",
        "name": "Hybrid and EV repair",
        "card_line": "High-voltage battery, ERAD motor, onboard charger and module work.",
        "photo": "volvo-xc90-t8-hybrid-battery-modules",
        "photos": ["volvo-xc90-t8-hybrid-battery-work", "volvo-xc90-t8-erad-motor", "volvo-xc60-t8-obc-control-units", "porsche-taycan-ev-diagnostics"],
        "title": "Hybrid and EV Repair in Shah Alam | Rasa Sayang Automotive",
        "desc": "New energy vehicle workshop in Selangor: hybrid high-voltage battery, ERAD motor, IGM, EME and DCDC module repair in Shah Alam and Subang Jaya.",
        "h1": "Hybrid and EV repair in Shah Alam",
        "lead": "Hybrid EV workshop in Shah Alam for high-voltage batteries, electric drive and control modules.",
        "body": [
            ("High-voltage battery work", "We have replaced hybrid high-voltage batteries on the Volvo XC90 and XC60 T8, the BMW X5 F15, 45e and G05, and the Mercedes S400 hybrid. Volvo hybrid battery jobs in Shah Alam are some of our most common posts."),
            ("Electric drive and modules", "We replace electric rear-axle (ERAD) motors and repair and program IGM, IEM, EME and DCDC modules, plus onboard chargers and coolant pumps."),
            ("Diagnostics first", "Every new energy vehicle job starts with a scan of the high-voltage system and the control modules, so we fix the cause and not only the warning."),
        ],
        "faq": [
            ("Do you replace Volvo T8 hybrid batteries?", "Yes. We have done high-voltage battery work on the Volvo XC90 T8 and XC60 T8 in our Shah Alam bay."),
            ("Can you repair an EME or DCDC module?", "Yes. We repair and program IGM, IEM, EME and DCDC modules. WhatsApp us the model, year and the fault message."),
        ],
    },
    {
        "id": "engine", "slug": "engine-repair-overhaul",
        "name": "Engine repair and overhaul",
        "card_line": "Engine repair, mounting, timing belt, gearbox and full overhaul.",
        "photo": "rolls-royce-engine-overhaul-lift",
        "photos": ["rolls-royce-engines-on-floor", "rolls-royce-front-engine-service", "bmw-x5-f15-gearbox-flywheel"],
        "title": "Engine Repair and Overhaul, Shah Alam and Subang Jaya | Rasa Sayang Automotive",
        "desc": "Engine overhaul in Subang Jaya and Shah Alam: engine repair, engine mounting, timing belt, gearbox repair and ATF for continental cars and supercars.",
        "h1": "Engine repair and engine overhaul",
        "lead": "Engine overhaul in Subang Jaya and Shah Alam, from mountings to a full rebuild.",
        "body": [
            ("Engine repair and overhaul", "We take engines out, rebuild them and put them back. Our photos show Rolls-Royce engines on the floor during an overhaul, and a Porsche GT3 engine repair."),
            ("Gearbox and drivetrain", "Gearbox repair and ATF service, flywheel work and engine mounting, on cars like the BMW X5 F15, Porsche Macan and Mercedes-Benz GTS."),
            ("Major service", "Major car service and timing belt jobs, done in the same bay as our heavier engine work."),
        ],
        "faq": [
            ("Do you do full engine overhauls?", "Yes. Engine overhaul is one of our main services at the Shah Alam HQ and the Subang Jaya branch."),
            ("Do you repair gearboxes?", "Yes. We have done gearbox repair and ATF service on BMW, Porsche and Mercedes-Benz cars."),
        ],
    },
    {
        "id": "supercar", "slug": "supercar-repair",
        "name": "Supercar repair",
        "card_line": "Lamborghini, Ferrari, McLaren, Porsche and Rolls-Royce.",
        "photo": "lamborghini-aventador-svj-service-lift",
        "photos": ["lamborghini-aventador-svj-front-service", "lamborghini-aventador-svj-rear", "ferrari-488-gear-knob-internals", "rolls-royce-air-suspension"],
        "title": "Supercar Repair in Shah Alam, Klang Valley | Rasa Sayang Automotive",
        "desc": "Supercar repair in Shah Alam and supercar workshop for the Klang Valley: Lamborghini, Ferrari, McLaren, Porsche and Rolls-Royce service, software and suspension.",
        "h1": "Supercar repair in Shah Alam",
        "lead": "A supercar workshop for the Klang Valley, with the cars on our own lifts.",
        "body": [
            ("Service and software", "We have serviced a Lamborghini Aventador SVJ, done a car service and software reset on a Ferrari Purosangue, and repaired the turbo on a Ferrari 488 GTB."),
            ("Suspension and interior parts", "Air suspension, air balloon and electric absorber work on Rolls-Royce cars, and gear knob panel repairs on the Ferrari 488 and BMW M4."),
            ("Makes", "Lamborghini, Ferrari, McLaren, Porsche and Rolls-Royce, alongside BMW, Mercedes-Benz, Audi, Volvo and Land Rover."),
        ],
        "faq": [
            ("Which supercars do you work on?", "Lamborghini, Ferrari, McLaren, Porsche and Rolls-Royce. Our posts include the Aventador SVJ, Urus, Ferrari 488 GTB, Purosangue and Rolls-Royce Cullinan and Ghost."),
            ("Can you reset supercar software?", "Yes. We did a car service and software reset on a Ferrari Purosangue. WhatsApp us your model and what you need."),
        ],
    },
    {
        "id": "aircond", "slug": "aircond-repair",
        "name": "Aircond repair",
        "card_line": "Compressor, condenser and cooling coil, hybrid systems included.",
        "photo": "ev-hybrid-fender-cover-coolant-pumps",
        "photos": ["volvo-xc60-t8-coolant-pumps", "volvo-xc90-t8-coolant-pump-hoses"],
        "title": "Car Aircond Repair in Shah Alam | Rasa Sayang Automotive",
        "desc": "Aircond repair in Shah Alam and Subang Jaya: compressor, condenser and cooling coil, including hybrid electric compressors on BMW and Mercedes-Benz.",
        "h1": "Car aircond repair in Shah Alam",
        "lead": "Aircond repair in Shah Alam for petrol, hybrid and EV systems.",
        "body": [
            ("Compressor, condenser, cooling coil", "We replace aircond compressors, condensers and cooling coils. Recent jobs include the BMW X5 G05 hybrid compressor and condenser, and the Mercedes-Benz C350e cooling coil."),
            ("Hybrid and EV aircond", "On hybrids and EVs the aircond compressor runs on the high-voltage system. Our posts show compressor jobs on the Mercedes-Benz S400 hybrid, BMW X5 45e and Porsche Taycan."),
        ],
        "faq": [
            ("Do you repair hybrid aircond compressors?", "Yes. Recent jobs include the hybrid aircond compressor and condenser on a BMW X5 G05."),
            ("My aircond is not cold. What should I send?", "WhatsApp us the model, year and what changed. A short video of the vents and the dash helps."),
        ],
    },
    {
        "id": "workshop-support", "slug": "workshop-technical-support",
        "name": "Support for other workshops",
        "card_line": "Complex faults, electronics and new energy vehicle repairs.",
        "photo": "volvo-xc90-t8-hybrid-bdu",
        "photos": ["volvo-xc90-t8-erad-parts", "porsche-taycan-ev-battery-lift"],
        "title": "Technical Support for Workshops, Selangor | Rasa Sayang Automotive",
        "desc": "Technical support for other workshops in the Klang Valley: high-voltage, battery, electric drive and control module faults, and complex diagnostics.",
        "h1": "Technical support for other workshops",
        "lead": "Stuck on a new energy vehicle or an electronic fault? Bring it to us.",
        "body": [
            ("What we support", "High-voltage electrical systems, battery systems, electric drive systems, electronic control modules and complex fault diagnostics."),
            ("How it works", "WhatsApp us the car, the fault codes and what has been tried. We tell you how we can help, in our bay or with the diagnosis."),
        ],
        "faq": [
            ("Do you work with other workshops?", "Yes. We give technical support to other workshops on complex faults, electronic systems and new energy vehicle repairs."),
        ],
    },
]

SERVICES_INDEX = {
    "title": "Services: Hybrid, EV, Engine, Supercar and Aircond | Rasa Sayang Automotive",
    "desc": "Hybrid and EV repair, engine repair and overhaul, supercar repair, aircond repair and technical support for workshops in Shah Alam and Subang Jaya.",
    "h1": "Our services",
    "lead": "Five areas of work, from high-voltage batteries to full engine rebuilds.",
}

ABOUT = {
    "title": "About Rasa Sayang Automotive Group Sdn Bhd | Shah Alam",
    "desc": "Rasa Sayang Automotive Group Sdn Bhd: a hybrid, EV and supercar repair workshop with an HQ in Shah Alam and a branch in Subang Jaya, Selangor.",
    "h1": "About Rasa Sayang Automotive",
    "lead": "A hybrid, EV and supercar repair workshop in Selangor.",
    "tag_h2": "In our own words",
    "tag_main": "Specialized Repair Center for New Energy Vehicles and Supercars",
    "tag_points": ["Expert Diagnostics", "Precision Repair", "Technical Excellence"],
    "body": [
        ("What we do", "Hybrid and EV / new energy vehicle maintenance, engine repair, supercar repair, engine overhaul and aircond repair, plus technical support for other workshops."),
        ("Where we are", "Our HQ is in Seksyen 26, Shah Alam, and our branch is in SS14, Subang Jaya. We see cars from Klang, Damansara, Cheras, Petaling Jaya, Puchong, USJ and Kuala Lumpur."),
    ],
}

CONTACT = {
    "title": "Contact and Locations, Shah Alam and Subang Jaya | Rasa Sayang Automotive",
    "desc": "WhatsApp or call 016-664 1686. Rasa Sayang Automotive HQ in Seksyen 26, Shah Alam and branch in SS14, Subang Jaya, with Waze and Google Maps links.",
    "h1": "Contact and locations",
    "lead": "WhatsApp is the fastest way to reach us.",
    "wa_h": "WhatsApp or call",
    "wa_p": "Send the model, year and the fault. We reply on WhatsApp.",
    "hours_h": "Opening hours",
    "hours_p": "Please WhatsApp before you come in and we will arrange a time.",
}

PRIVACY = {
    "title": "Privacy | Rasa Sayang Automotive",
    "desc": "How Rasa Sayang Automotive Group Sdn Bhd handles the information you send us on WhatsApp, by phone or through this website.",
    "h1": "Privacy",
    "body": [
        ("What we collect", "When you WhatsApp or call us, we see your name, number and the details you send about your car. We use them only to reply and to work on your car."),
        ("This website", "This site counts taps on its WhatsApp, call, Facebook and map buttons so we know which buttons are used. It does not use advertising cookies."),
        ("Your choices", "You can ask us to delete your messages and details at any time. WhatsApp 016-664 1686."),
    ],
}

ARTICLES = {
    "title": "Articles | Rasa Sayang Automotive",
    "desc": "Articles from Rasa Sayang Automotive on hybrid, EV and supercar care in the Klang Valley.",
    "h1": "Articles",
    "lead": "Notes from our bay on hybrid, EV and supercar care. New articles are on the way.",
}

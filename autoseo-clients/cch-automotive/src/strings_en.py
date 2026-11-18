# English copy for the CCH Automotive site. Every fact here comes from facts.json (Bridge drop, 18 Nov 2026).
# Keep all visible words in this file. strings_ms.py and strings_zh.py have exactly the same keys (shared AutoSEO template rule).
# No hours, prices, reviews, ratings, staff names, company number or dealer claims. No em dashes in copy.

UI = {
    "skip": "Skip to content",
    "menu": "Menu",
    "close": "Close",
    "nav_services": "Services",
    "nav_about": "About",
    "nav_contact": "Contact",
    "nav_articles": "Articles",
    "nav_home": "Home",
    "wa_btn": "WhatsApp us",
    "wa_btn_long": "WhatsApp 010-935 9391",
    "call_btn": "Call",
    "call_btn_long": "Call 010-935 9391",
    "email_btn": "Email us",
    "fb_btn": "Facebook page",
    "map_btn": "Open in Google Maps",
    "prev": "Previous",
    "next": "Next",
    "footer_find": "Find the workshop",
    "footer_talk": "Talk to us",
    "footer_pages": "Pages",
    "credit": "Website by AutoSEO.my",
    "brands_note": "Brand names on this site only describe the cars and products we work with.",
    "privacy": "Privacy",
    "photo_open": "Open photo",
    "related": "Other services",
    "ask_title": "Ask about your car",
    "ask_line": "Send the model, year and what the car is doing. Photos or a short video help.",
    "lang_label": "Language",
    "aria_main": "Main",
    "aria_menu": "Menu",
    "aria_pages": "Pages",
    "aria_contact": "Contact",
    "aria_photo": "Photo",
    "aria_breadcrumb": "Breadcrumb",
    "home_aria": "CCH Automotive home",
    "logo_alt": "CCH Automotive logo",
    "faq_about": "Questions about {name}",
    "last_updated": "Last updated 18 November 2026.",
    "contact_wa_h": "WhatsApp or call",
    "contact_mail_h": "Email and Facebook",
    "contact_hours_h": "Opening hours",
    "contact_addr_h": "Address",
}

# WhatsApp prefill for this language (the number itself lives in facts.json).
PREFILL = "Hi CCH Automotive, I'd like to ask about my car. Model and year: "

# Alt text and captions: say only what the photo shows. Keys are image stems in build.py.
CAPTIONS = {
    "alpine-fender-engine": "Black BMW on a two-post lift, Alpine Germany fender cover on",
    "bmw-x-lift": "BMW X3 (F25) on the lift, new mounts on the floor",
    "engine-bay-mini": "MINI John Cooper Works on the lift, Motul oil ready",
    "engine-bay-open-hood": "Open engine bay, two bottles of Motul Multipower Plus",
    "fj-cruiser-lift": "Toyota FJ Cruiser on the scissor lift, Toyota AT fluid on the floor",
    "fj-cruiser-yellow": "Toyota FJ Cruiser in the bay",
    "merc-engine-bay-2": "White Mercedes-Benz on the lift with Alpine RS 0W-40",
    "mercedes-c-white": "Mercedes-Benz C-Class in the workshop",
    "mercedes-ml-engine": "Mercedes-Benz ML / GLE with Alpine RS 5W-40 C3",
    "mercedes-white-engine-bay": "Mercedes-Benz A-Class or CLA, Alpine Longlife III 5W-30 and DSG Fluid",
    "mustang-lift": "Ford Mustang transmission service, Motorcraft Mercon LV fluid",
    "pickup-lift": "Toyota Hilux GR Sport service with Alpine TSN 10W-40",
    "subaru-engine-bay": "Subaru WRX STI on the lift, new front control arms",
    "oil-alpine-red": "Alpine TSN 10W-40 and a Toyota oil filter",
    "oil-jugs-red": "Motorcraft Mercon LV, transmission pan, filter and gasket",
    "alpine-yellow-oil": "Alpine Longlife 12 FE 0W-30 and a Perodua oil filter",
    "parts-engine-mounts": "Gearbox mounting for a BMW X3 F25",
    "turbo-piping-parts": "Old and new hoses on an Alpine fender cover",
    "poster-conti": "CCH Automotive services poster: Professional in Conti Car",
    "flyer-service-repair": "CCH Automotive Car Service and Repair flyer",
    "oil-kit": "Parts laid out for a service: Alpine RSL 5W-40, filters, fluids, suspension and steering parts",
    "cover": "CCH Automotive workshop bay with a black Ford Mustang, a yellow Porsche and a black Porsche on a two-post lift",
    "og": "CCH Automotive workshop bay in Likas, Kota Kinabalu",
}

# Facebook-post car list on the home page (facts.json cars_worked_on.from_posts, in this language).
CARS_FROM_POSTS = ["BMW F30 M Sport (steering and paddle shifter activation)", "Audi R8 V8 (oil change)", "Mercedes C200 Kompressor",
                   "Porsche Carrera Turbo S", "Range Rover Sport", "Mustang GT 5.0 (cooling coil)", "Toyota Hilux (brake upgrade)", "Mini",
                   "Toyota Alphard / Vellfire", "Honda Accord", "Toyota FJ Cruiser", "Subaru"]

HOME = {
    "title": "Continental car workshop in Kota Kinabalu | CCH Automotive, Likas",
    "desc": "CCH Automotive is a Continental car workshop in Likas, Kota Kinabalu: Mercedes, BMW, Audi and VW troubleshooting, diagnostics, module coding, engine, gearbox and aircond.",
    "h1": "Continental car workshop in Kota Kinabalu",
    "hero_line": "Mercedes, BMW, Audi and VW repairs on Jalan Tuaran, Likas.",
    "hero_tag": "Professional in Conti Car",
    "services_h2": "What we fix in the Likas bay",
    "services_line": "Swipe through the work we take on. Tap a card for the details.",
    "intro_h2": "More than 10 years on Continental cars",
    "intro_p": [
        "CCH Automotive Sdn Bhd is a car workshop in Likas Baharu on Jalan Tuaran, Kota Kinabalu, in the Jalan Tuaran Bypass area. "
        "We work on Continental cars: Mercedes-Benz, BMW, Audi and Volkswagen, along with the other makes Sabah drivers bring in.",
        "The workshop has more than 10 years of experience. Bring us a warning light, a gearbox that feels wrong, an aircond that has stopped "
        "blowing cold or a car that is simply due for its service. We start with troubleshooting and computer diagnostics, then repair.",
    ],
    "brands_label": "Continental makes we look after",
    "process_h2": "From your WhatsApp to the lift and back",
    "process_steps": [
        ("WhatsApp us", "Send the model, year and what the car is doing to 010-935 9391."),
        ("Diagnose and code", "Troubleshooting and computer diagnostics find the fault. Modules are programmed or coded when the job needs it."),
        ("Repair", "Engine, gearbox, aircond, electrical or service work is done in our Likas workshop."),
        ("Collect", "Drive your car home from Jalan Tuaran."),
    ],
    "work_h2": "Cars we have worked on",
    "work_line": "Real jobs from our workshop. Hold or swipe to stop the strip, tap a photo to see it whole.",
    "posts_h3": "Also from our Facebook posts",
    "oil_h2": "Alpine Germany engine oil",
    "oil_p": "We use Alpine Germany engine oil. Our posts mention Alpine RS 10W-60, and the grades in our workshop photos include "
             "Alpine RS 0W-40, RS 5W-40 C3, Longlife 12 FE 0W-30, Longlife III 5W-30, TSN 10W-40, RSL 5W-40 and Alpine DSG Fluid.",
    "visit_h2": "Find us on Jalan Tuaran",
    "visit_p": "Lot 5, Batu 5½, Jalan Tuaran, Likas Baharu, 88450 Kota Kinabalu, Sabah. Opening hours are not listed online yet, "
               "so WhatsApp us to arrange a time before you drive over.",
    "faq_h2": "Questions drivers ask us",
}

FAQ_HOME = [
    ("Which cars do you work on?",
     "We are a Continental car workshop for Mercedes-Benz, BMW, Audi and Volkswagen. Our posts also show jobs on a BMW F30 M Sport, an Audi R8 V8, "
     "a Mercedes C200 Kompressor, a Porsche Carrera Turbo S, a Range Rover Sport, a Mustang GT 5.0, a Toyota Hilux, a Mini, a Toyota Alphard / Vellfire, "
     "a Honda Accord, a Toyota FJ Cruiser and a Subaru."),
    ("Where is CCH Automotive?",
     "Lot 5, Batu 5½, Jalan Tuaran, Likas Baharu, 88450 Kota Kinabalu, Sabah, in the Jalan Tuaran Bypass area. The Google Maps link on this page searches that address."),
    ("What are your opening hours?",
     "Our opening hours are not listed online yet. WhatsApp 010-935 9391 to arrange a time before you come."),
    ("Can you program or code modules?",
     "Yes. Module programming and coding is one of our services. One example from our posts is a BMW F30 M Sport where we activated the M Sport steering and paddle shifters."),
    ("Which engine oil do you use?",
     "We use Alpine Germany engine oil, for example Alpine RS 10W-60, Alpine RS 5W-40 C3 and Alpine Longlife III 5W-30."),
    ("How do I get a price for a repair?",
     "Send the model, year and what the car is doing on WhatsApp. Photos or a short video of the problem help us reply properly."),
]

# Service pages. 'photos' are stems from PHOTOS in build.py; 'card' is the photo on the home scroller card.
SERVICES = [
    {
        "id": "troubleshooting", "slug": "car-troubleshooting",
        "name": "Car troubleshooting",
        "card_line": "Warning lights, odd noises and faults that come and go.",
        "card": "engine-bay-open-hood",
        "title": "Car troubleshooting in Kota Kinabalu | CCH Automotive, Likas",
        "desc": "Car troubleshooting at CCH Automotive, a Continental car workshop on Jalan Tuaran, Likas, Kota Kinabalu. WhatsApp 010-935 9391.",
        "h1": "Car troubleshooting in Kota Kinabalu",
        "lead": "A car workshop in Likas that finds the fault first. Bring us the warning light, the noise or the problem that only shows up some days.",
        "body": [
            ("Finding the cause, not guessing",
             "Troubleshooting is where most of our jobs start. We listen to what the car is doing, check it in the workshop and use computer diagnostics "
             "to read what the car's systems have recorded. Once the cause is found, we can move on to the repair."),
            ("Continental cars and more",
             "We are a Continental car specialist for Mercedes-Benz, BMW, Audi and Volkswagen, and our workshop photos also show Toyota, Subaru, Ford and MINI jobs."),
        ],
        "photos": ["engine-bay-open-hood", "alpine-fender-engine", "turbo-piping-parts"],
        "faq": [
            ("What should I send before I bring the car?", "The model, year and what the car is doing. A photo of the warning light or a short video of the noise helps."),
        ],
    },
    {
        "id": "engine-gearbox", "slug": "engine-gearbox-repair",
        "name": "Engine and gearbox repair",
        "card_line": "Engine faults, gearbox and transmission work, mountings.",
        "card": "parts-engine-mounts",
        "title": "Engine and gearbox repair in Sabah | CCH Automotive, Kota Kinabalu",
        "desc": "Engine and gearbox repair for Continental cars at CCH Automotive, Jalan Tuaran, Likas, Kota Kinabalu, Sabah. Transmission work too. WhatsApp 010-935 9391.",
        "h1": "Engine and gearbox repair in Sabah",
        "lead": "Engine and gearbox repair for Mercedes, BMW, Audi and VW at our Likas workshop in Kota Kinabalu, plus transmission work.",
        "body": [
            ("Engine and gearbox jobs",
             "Engine and gearbox repair is one of our main services, and transmission work is on our service flyer. Our photos show a BMW X3 (F25) on the lift "
             "with a new gearbox mounting, and a Ford Mustang on the lift for a transmission service with Motorcraft Mercon LV fluid and a new pan, filter and gasket."),
            ("Diagnose first",
             "Engine and gearbox complaints start with troubleshooting and computer diagnostics, so the repair is aimed at the real cause."),
        ],
        "photos": ["bmw-x-lift", "parts-engine-mounts", "mustang-lift", "oil-jugs-red"],
        "faq": [
            ("Do you do transmission work?", "Yes. Transmission is listed on our service flyer, alongside engine and gearbox repair."),
        ],
    },
    {
        "id": "diagnostics", "slug": "computer-diagnostics",
        "name": "Computer diagnostics",
        "card_line": "Reading the car's systems to find what is really wrong.",
        "card": "mercedes-ml-engine",
        "title": "Car computer diagnostics in Kota Kinabalu | Mercedes, BMW, Audi workshop",
        "desc": "Computer diagnostics for Mercedes, BMW, Audi and VW at CCH Automotive, Likas, Kota Kinabalu. WhatsApp 010-935 9391.",
        "h1": "Computer diagnostics for Mercedes, BMW and Audi in Kota Kinabalu",
        "lead": "Modern Continental cars report their faults electronically. Computer diagnostics at our Likas workshop reads them before any parts are changed.",
        "body": [
            ("Why diagnostics comes first",
             "A warning light can have more than one cause. Computer diagnostics reads the fault records in the car's systems and points the troubleshooting "
             "in the right direction on Mercedes-Benz, BMW, Audi, Volkswagen and other models."),
            ("Diagnostics, then coding or repair",
             "When a fault is traced to a module, the next step can be module programming and coding. When it is mechanical, we move on to the repair."),
        ],
        "photos": ["mercedes-ml-engine", "merc-engine-bay-2", "mercedes-white-engine-bay"],
        "faq": [
            ("Can you read the warning light on my Mercedes or BMW?", "Yes. Computer diagnostics is one of our services for Mercedes-Benz, BMW, Audi and Volkswagen."),
        ],
    },
    {
        "id": "module-programming", "slug": "module-programming-coding",
        "name": "Module programming and coding",
        "card_line": "Programming modules and coding features on European cars.",
        "card": "alpine-fender-engine",
        "title": "Module programming and coding in Kota Kinabalu | CCH Automotive",
        "desc": "Module programming and coding for BMW, Mercedes, Audi and VW at CCH Automotive, Likas, Kota Kinabalu. WhatsApp 010-935 9391.",
        "h1": "Module programming and coding in Kota Kinabalu",
        "lead": "Programming and coding for Continental cars at our Likas workshop, from a replaced module to features you want switched on.",
        "body": [
            ("What programming and coding covers",
             "Many parts on a modern European car are run by modules. Module programming and coding is one of our listed services. "
             "One job from our posts: a BMW F30 M Sport where we activated the M Sport steering and paddle shifters."),
            ("Ask about your model",
             "What can be coded depends on the car. WhatsApp us the model, year and what you want done so we can check it for you."),
        ],
        "photos": ["alpine-fender-engine", "bmw-x-lift"],
        "faq": [
            ("Can you activate features on my BMW?", "Coding is one of our services. Our posts show a BMW F30 M Sport with M Sport steering and paddle shifter activation. Send us your model and year to check yours."),
        ],
    },
    {
        "id": "service", "slug": "car-service-maintenance",
        "name": "Car service and maintenance",
        "card_line": "Oil changes with Alpine Germany oil, filters and fluids.",
        "card": "oil-alpine-red",
        "title": "Car service and oil change in Kota Kinabalu | Alpine oil | CCH Automotive",
        "desc": "Car service, maintenance and oil change with Alpine Germany engine oil at CCH Automotive, Jalan Tuaran, Likas, Kota Kinabalu. WhatsApp 010-935 9391.",
        "h1": "Car service and maintenance in Kota Kinabalu",
        "lead": "Servicing and oil changes at our Jalan Tuaran workshop in Likas, with Alpine Germany engine oil.",
        "body": [
            ("Service and oil change",
             "Car service and maintenance is part of our everyday work, and oil change is on our flyer. We use Alpine Germany engine oil. "
             "Our posts mention Alpine RS 10W-60 and an Audi R8 V8 oil change, and our photos show Alpine RS 0W-40, RS 5W-40 C3, Longlife 12 FE 0W-30, "
             "Longlife III 5W-30, TSN 10W-40, RSL 5W-40 and Alpine DSG Fluid."),
            ("Cars in for service",
             "Our photos show a Toyota Hilux GR Sport serviced with Alpine TSN 10W-40, a MINI John Cooper Works, a Toyota FJ Cruiser and a Subaru WRX STI with new "
             "front control arms. Our posts also mention a brake upgrade on a Toyota Hilux."),
        ],
        "photos": ["pickup-lift", "oil-alpine-red", "alpine-yellow-oil", "engine-bay-mini", "subaru-engine-bay"],
        "wide": "oil-kit",
        "faq": [
            ("Which oil goes into my car?", "We use Alpine Germany engine oil. Send your model and year on WhatsApp and ask which grade suits it."),
        ],
    },
    {
        "id": "aircond", "slug": "aircond-service-repair",
        "name": "Aircond service and repair",
        "card_line": "Aircond not cold? Service, repair and cooling coil work.",
        "card": "poster-conti",
        "title": "Car aircond service in Kota Kinabalu | CCH Automotive, Likas",
        "desc": "Car aircond service and repair at CCH Automotive, a Continental car workshop on Jalan Tuaran, Likas, Kota Kinabalu. WhatsApp 010-935 9391.",
        "h1": "Car aircond service in Kota Kinabalu",
        "lead": "Aircond service and repair at our Likas workshop. Our logo says it plainly: car engine and aircon.",
        "body": [
            ("Aircond work we do",
             "Aircond service and repair is one of our core services and is on both our poster and our flyer. One job from our posts is a cooling coil on a Mustang GT 5.0."),
            ("Tell us what the aircond is doing",
             "Blowing warm, cold only when driving, a smell or a noise: send the model, year and what you notice on WhatsApp before you come in."),
        ],
        "photos": [],
        "poster": "poster-conti",
        "faq": [
            ("My car aircond is not cold. Can you check it?", "Yes. Aircond service and repair is one of our services. WhatsApp us the model, year and what the aircond is doing."),
        ],
    },
    {
        "id": "electrical-hybrid", "slug": "electrical-hybrid",
        "name": "Electrical and hybrid",
        "card_line": "Electrical faults and hybrid cars, as listed on our flyer.",
        "card": "flyer-service-repair",
        "title": "Car electrical and hybrid repair in Kota Kinabalu | CCH Automotive",
        "desc": "Electrical and hybrid car work at CCH Automotive, Jalan Tuaran, Likas, Kota Kinabalu. Diagnostics first. WhatsApp 010-935 9391.",
        "h1": "Car electrical and hybrid work in Kota Kinabalu",
        "lead": "Electrical and hybrid is one of the services on our Car Service and Repair flyer.",
        "body": [
            ("Electrical faults",
             "Electrical problems on a modern car often show up as warning lights or systems that stop working. We start with troubleshooting and computer diagnostics "
             "to trace the fault, and module programming and coding when a module is involved."),
            ("Hybrid cars",
             "Electrical and hybrid sits on our service flyer next to engine, aircond, transmission and oil change. WhatsApp us your hybrid's model, year and the problem first."),
        ],
        "photos": [],
        "poster": "flyer-service-repair",
        "faq": [
            ("Do you work on hybrid cars?", "Electrical and hybrid is listed on our service flyer. Send your model, year and the problem on WhatsApp so we can tell you if we can help."),
        ],
    },
]

SERVICES_INDEX = {
    "title": "Car repair services in Kota Kinabalu | CCH Automotive, Likas",
    "desc": "Troubleshooting, diagnostics, module coding, engine and gearbox, service, aircond, electrical and hybrid at CCH Automotive, Jalan Tuaran, Likas, Kota Kinabalu.",
    "h1": "Car repair services at our Likas workshop",
    "lead": "Everything we take on at CCH Automotive, a Continental car workshop on Jalan Tuaran, Kota Kinabalu.",
}

ABOUT = {
    "title": "About CCH Automotive | Continental car workshop, Likas, Kota Kinabalu",
    "desc": "CCH Automotive Sdn Bhd: a Continental car workshop on Jalan Tuaran, Likas, Kota Kinabalu with more than 10 years of experience.",
    "h1": "About CCH Automotive, a Jalan Tuaran workshop",
    "lead": "Professional in Conti Car, with more than 10 years of experience.",
    "body": [
        ("Who we are",
         "CCH Automotive Sdn Bhd, also known as CCH Auto, is an automotive repair shop and Continental car specialist in Likas Baharu, Kota Kinabalu, "
         "on Jalan Tuaran in the Jalan Tuaran Bypass area. Our own line is \"Professional in Conti Car\", and the workshop has more than 10 years of experience."),
        ("What we do",
         "Car troubleshooting, engine and gearbox repair, computer diagnostics, module programming and coding, car service and maintenance, aircond service and repair, "
         "and electrical and hybrid work. Our flyer also lists transmission and oil change."),
        ("Our oil",
         "We use Alpine Germany engine oil on the cars we service."),
    ],
    "media_h2": "Our poster and flyer",
}

CONTACT = {
    "title": "Contact CCH Automotive | Car workshop, Jalan Tuaran, Likas, Kota Kinabalu",
    "desc": "WhatsApp or call CCH Automotive on 010-935 9391. Lot 5, Batu 5½, Jalan Tuaran, Likas Baharu, 88450 Kota Kinabalu, Sabah.",
    "h1": "Contact our car workshop in Likas",
    "lead": "WhatsApp is the quickest way to reach us. Send the model, year and what the car is doing.",
    "hours_note": "Opening hours are not listed online yet. Please WhatsApp us to arrange a time before you come.",
    "area_note": "The Jalan Tuaran Bypass area.",
}

PRIVACY = {
    "title": "Privacy | CCH Automotive",
    "desc": "How the CCH Automotive website handles your information.",
    "h1": "Privacy",
    "body": [
        ("What this website collects",
         "This website has no forms and no accounts. A small script counts taps on the WhatsApp, call, email, Facebook and map buttons so we can see which buttons help visitors. "
         "It records the button, the page, the device type, the time zone set on your device and a random visit code. It does not record your name or phone number."),
        ("When you contact us",
         "When you WhatsApp, call or email us, we see what you send, such as your number and your message, and use it only to reply about your car."),
        ("Other services",
         "Links to WhatsApp, Facebook and Google Maps open those services, which have their own privacy policies."),
        ("Questions",
         "Email cchautomotive6@gmail.com about anything on this page."),
    ],
}

ARTICLES = {
    "title": "Car care articles for Kota Kinabalu drivers | CCH Automotive",
    "desc": "Articles from CCH Automotive, a Continental car workshop in Likas, Kota Kinabalu.",
    "h1": "Car care articles from our Likas workshop",
    "lead": "Articles from CCH Automotive will appear here. Until then, WhatsApp us your question.",
}

# English strings for the S & P Precision Parts (Monaer) site. strings_ms.py and strings_zh.py have the SAME keys.
# Facts (phone, address, company no., maker claims) live in facts.json. No prices, warranty, stock counts, origin
# country, workshop names or fitment years here: none are confirmed yet.

UI = {
    'skip': 'Skip to content', 'menu': 'Menu', 'close': 'Close menu', 'lang': 'Language',
    'home': 'Home', 'products': 'Products', 'finder': 'Part finder', 'locator': 'Find a workshop',
    'join': 'For workshops', 'faq': 'FAQ', 'contact': 'Contact', 'articles': 'Articles', 'privacy': 'Privacy',
    'breadcrumb': 'Breadcrumb',
    'wa_btn': 'Check my car on WhatsApp', 'wa_short': 'WhatsApp', 'call_btn': 'Call 016-855 6611', 'call_short': 'Call',
    'join_btn': 'Apply to become authorised', 'locator_btn': 'Find a workshop',
    'finder_btn': 'Open the part finder', 'see_more': 'See details', 'all_products': 'All products',
    'tagline': 'Authorised Monaer brake parts distributor in Skudai, Johor.',
    'contact_h': 'Talk to us', 'follow_h': 'Follow', 'facebook': 'Facebook page', 'maps': 'Google Maps', 'waze': 'Waze',
    'email': 'Email us', 'address_h': 'Address', 'company': 'Company no.',
    'faq_h': 'Questions drivers and workshops ask',
    'maker_note': 'Product details on this site are as published by Monaer Brake System Malaysia. Ask us for the details of your exact part.',
    'safety': 'Brakes are a safety part. Always confirm the exact part for your car with us or your workshop before fitting.',
    'sample': 'Catalogue example',
    'steps_h': 'How to get Monaer pads for your car',
    'steps': [
        ('Send your car details', 'Make, model, year and engine on WhatsApp. A photo of your road tax or the old pad helps.'),
        ('We match the part', 'We check the Monaer catalogue number against your car\'s original part number.'),
        ('Fit at a workshop', 'Collect from us in Skudai or have it fitted at a Monaer workshop near you.'),
    ],
    'privacy_line': 'By sending, you agree we use these details only to reply to you (PDPA).',
    'opens_wa': 'This opens WhatsApp with your details filled in. Nothing is stored on this website.',
}

PREFILL = {
    'default': 'Hi S & P Precision Parts, I want to check Monaer brake pads for my car. Car model and year: ',
    'contact': 'Hi S & P Precision Parts, I have a question about Monaer brake parts: ',
    'pads': 'Hi, please check Monaer brake pads for my car. Make / model / year: ',
    'discs': 'Hi, please check Monaer brake discs for my car. Make / model / year: ',
    'care': 'Hi, I want to ask about Monaer brake cleaner and workshop items: ',
    'locator': 'Hi, which workshop near me can fit Monaer brake parts? My area: ',
    'join': 'Hi, my workshop wants to become an authorised Monaer workshop. Workshop name and town: ',
    # finder / join forms build these with the filled fields
    'f_intro': 'Hi, please check Monaer brake pads for my car.',
    'f_make': 'Make', 'f_model': 'Model', 'f_year': 'Year', 'f_axle': 'Front / rear', 'f_part': 'Part or OE number',
    'j_intro': 'Hi, my workshop wants to become an authorised Monaer workshop.',
    'j_name': 'Workshop', 'j_person': 'Contact person', 'j_town': 'Town', 'j_state': 'State', 'j_phone': 'Phone', 'j_bays': 'Service bays', 'j_note': 'Note',
}

HOME = {
    'title': 'Monaer Brake Pads & Discs Malaysia | S & P Precision Parts, Skudai',
    'meta': 'Monaer nano ceramic brake pads, coated discs and brake fluid from the authorised distributor in Skudai, Johor. Check your car on WhatsApp or find a workshop near you.',
    'h1': 'Monaer brake pads and discs in Malaysia',
    'line': 'Nano ceramic pads, matched to your car. Check yours in a minute.',
    'stop_label': 'Monaer brake disc',
    'two_h': 'Two ways to get Monaer on your car',
    'two': [
        ('Drivers', 'Tell us your car. We match the Monaer part and point you to a workshop that fits it.', 'finder'),
        ('Workshops', 'Stock Monaer direct from the distributor and get listed on our workshop finder.', 'join'),
    ],
    'why_h': 'What makes Monaer pads different',
    'why_p': 'As published by Monaer Brake System Malaysia.',
    'why': [
        ('Nano ceramic pads', 'Monaer pads use a nano ceramic friction material, made for quiet stops and clean rims in daily traffic.'),
        ('Built for heat', 'Monaer lists heat fade resistance from 600°C, and 800°C on its performance pads, so the bite stays when the brakes get hot.'),
        ('A full kit in every box', 'Each pad set comes with brake cleaner spray, gloves and high-temperature anti-noise grease. No extra shopping for the job.'),
        ('Pads, discs and fluid from one brand', 'Coated high-carbon discs, DOT 4 and DOT 5.1 brake fluid, and a pad range made for EVs too.'),
    ],
    'feel_h': 'What you notice on the road',
    'feel': ['Strong, steady bite', 'Quieter braking', 'Less black dust on your rims', 'Holds up when the brakes are hot', 'Longer disc life'],
    'feel_note': 'These are the points Monaer lists for its nano ceramic pads.',
    'range_h': 'The Monaer range',
    'finder_h': 'Does Monaer have a pad for my car?',
    'finder_p': 'Monaer covers daily cars to premium models and EVs. Send us your car and we check the exact part.',
    'locator_h': 'Find a Monaer workshop',
    'locator_p': 'Ask us for the nearest place to get Monaer fitted, or join as an authorised workshop.',
    'compare_h': 'Ceramic or semi-metallic?',
    'compare_p': 'Most pads sold in Malaysia are one of these two types. Here is the plain difference.',
    'compare_rows': [
        ('Noise', 'Quieter', 'Can squeal more'),
        ('Wheel dust', 'Light, pale dust', 'More dark dust'),
        ('Disc wear', 'Gentle on discs', 'Wears discs faster'),
        ('Best for', 'Daily driving, city and highway', 'Heavy loads, hard use'),
    ],
    'compare_cols': ('', 'Nano ceramic (Monaer)', 'Semi-metallic'),
    'faq': [
        ('Is S & P Precision Parts an authorised Monaer distributor?', 'Yes. S & P Precision Parts Sdn Bhd in Skudai, Johor is an authorised distributor of Monaer brake parts.'),
        ('How do I know which Monaer pad fits my car?', 'WhatsApp us your car make, model, year and engine. We match the Monaer catalogue number to your car\'s original part number before you buy.'),
        ('Can I buy direct or do I need a workshop?', 'Ask us on WhatsApp. We can tell you where to collect and which workshop near you can fit them.'),
    ],
}

PRODUCTS = {
    'title': 'Monaer Brake Products: Pads, Discs, Brake Care | S & P Precision Parts',
    'meta': 'The Monaer brake range in Malaysia: ceramic brake pads, brake discs, brake parts cleaner and workshop items. Ask S & P Precision Parts in Skudai.',
    'h1': 'Monaer brake products',
    'lead': 'Pads, discs and brake care from one brand, supplied from Skudai, Johor.',
}

# one entry per product group page (build.py GROUPS drives menus, hub, pages, sitemap)
PG = {
    'pads': {
        'name': 'Brake pads', 'chip': 'Pads',
        'title': 'Monaer Nano Ceramic Brake Pads Malaysia | S & P Precision Parts',
        'meta': 'Monaer nano ceramic brake pads: quiet, low dust, heat resistant, with a fitting kit in every box. Matched to your car by the authorised distributor in Skudai, Johor.',
        'h1': 'Monaer nano ceramic brake pads',
        'lead': 'Quiet, low dust pads with a fitting kit in every box.',
        'line': 'Nano ceramic pads for daily cars, premium models and EVs.',
        'points': ['Nano ceramic friction material', 'Heat fade resistance from 600°C, 800°C on performance pads (as listed by Monaer)',
                   'Low dust, so rims stay cleaner', 'Quieter braking and longer disc life',
                   'Kit in the box: brake cleaner spray, gloves and high-temperature anti-noise grease', 'One set is 4 pieces, enough for one axle',
                   'A pad range made for EVs'],
        'body_h': 'When to change your brake pads',
        'body': ['Squealing or grinding when you brake', 'The pedal feels softer or goes lower than before', 'The car pulls to one side when braking',
                 'Your workshop measures less than about 3 mm of pad left', 'The brake warning light comes on'],
        'faqs': [
            ('What is in a Monaer brake pad box?', 'One set of 4 pads for one axle, plus the fitting kit Monaer lists: brake cleaner spray, gloves and high-temperature anti-noise grease.'),
            ('Do I change pads in pairs?', 'Pads are always changed per axle: both front wheels together, or both rear wheels together. A Monaer set covers one axle.'),
            ('Does Monaer have pads for EVs?', 'Yes. Monaer has an EV brake pad range made for the weight of electric cars. Send us your EV model to check.'),
        ],
    },
    'discs': {
        'name': 'Brake discs', 'chip': 'Discs',
        'title': 'Monaer Brake Discs Malaysia | Coated High-Carbon Discs | S & P Precision Parts',
        'meta': 'Monaer high-carbon brake discs with anti-rust coating, drilled and slotted. WhatsApp your car model to check the size with the authorised distributor in Johor.',
        'h1': 'Monaer brake discs',
        'lead': 'Coated high-carbon discs, sold as a left and right pair.',
        'line': 'High-carbon discs with a silver anti-rust coating.',
        'points': ['High-carbon disc material', 'Silver protective coating that helps stop rust and corrosion in wet weather',
                   'Drilled and slotted design', 'One box holds the left and right pair',
                   'Steel brush and microfibre cloth included in the box', 'Sized to your car: confirm model, size and spec before buying'],
        'body_h': 'Signs your discs need changing',
        'body': ['Steering wheel or pedal shakes when braking', 'Deep grooves or a lip on the disc edge', 'Blue heat marks on the disc face',
                 'The disc is thinner than the minimum stamped on it'],
        'faqs': [
            ('Why are Monaer discs silver?', 'The silver layer is a protective coating that helps prevent rust and corrosion, useful in Malaysian rain and humidity.'),
            ('Do I need new discs every time I change pads?', 'Not always. Your workshop measures the disc. If it is above the minimum thickness and smooth, new pads alone are fine.'),
        ],
    },
    'care': {
        'name': 'Brake fluid and brake care', 'chip': 'Fluid and care',
        'title': 'Monaer Brake Fluid DOT 4 & DOT 5.1, Brake Cleaner | S & P Precision Parts',
        'meta': 'Monaer DOT 4 and DOT 5.1 brake fluid, brake parts cleaner and fitting items. Supplied to workshops and drivers by S & P Precision Parts, Skudai, Johor.',
        'h1': 'Monaer brake fluid and brake care',
        'lead': 'DOT 4 and DOT 5.1 fluid, plus the items that finish a clean brake job.',
        'line': 'DOT 4 and DOT 5.1 brake fluid, cleaner spray, grease and gloves.',
        'points': ['Monaer brake fluid in DOT 4 and DOT 5.1', 'Monaer brake parts cleaner spray', 'High-temperature anti-noise grease', 'Monaer work gloves'],
        'body_h': 'Signs your brake fluid needs changing',
        'body': ['The brake light stays on after the handbrake is down', 'The pedal feels soft or needs a deeper press', 'The fluid in the reservoir looks dark',
                 'Your service book says it is due'],
        'faqs': [
            ('DOT 4 or DOT 5.1: which one for my car?', 'Use the grade your car maker specifies, shown on the reservoir cap or in the owner manual. Send us your model if you are not sure.'),
            ('Do you supply brake care items to workshops?', 'Yes. WhatsApp us with what you need and how many.'),
        ],
    },
}

FINDER = {
    'title': 'Monaer Brake Pad Finder: Check Your Car | S & P Precision Parts',
    'meta': 'Check if Monaer brake pads fit your car. Search by car make, model or Monaer part number, or send your car to us on WhatsApp for an exact match.',
    'h1': 'Find Monaer brake pads for your car',
    'lead': 'Search the catalogue, or send us your car and we match it for you.',
    'search_h': 'Search the catalogue',
    'search_label': 'Car make, model or Monaer number',
    'search_ph': 'e.g. Audi, Touareg or M0307',
    'none': 'Not in the online list yet. Send it to us on WhatsApp and we check the full catalogue.',
    'list_note': 'The full Monaer catalogue is being loaded here. For now the list shows published examples only, so we check every car on WhatsApp before you buy.',
    'cols': ('Monaer no.', 'Type', 'Fits', 'Pack'),
    'type_pad': 'Nano ceramic brake pads', 'pack_4': '1 set / 4 pcs',
    'form_h': 'Send your car to us',
    'form_p': 'Fill in what you know. We reply with the matching Monaer part.',
    'f_make': 'Car make', 'f_model': 'Model', 'f_model_ph': 'e.g. Myvi, X70, City', 'f_year': 'Year', 'f_year_ph': 'e.g. 2019',
    'f_axle': 'Front or rear', 'f_axle_opts': ['Front', 'Rear', 'Both', 'Not sure'], 'f_part': 'Part or OE number (if you have it)',
    'f_send': 'Send to WhatsApp', 'choose': 'Choose',
    'read_h': 'How to read a Monaer pad box',
    'read': [
        ('Monaer number', 'Monaer\'s own part code, for example M0307. One number can fit several car models.'),
        ('Car model and chassis code', 'The cars the pad fits, with the chassis code in brackets, for example Audi A8L (D5/4N).'),
        ('Set size', 'One set is 4 pieces, enough for the two wheels on one axle.'),
    ],
    'faqs': [
        ('What if my car is not in the list?', 'Most cars are not online yet. Send us your car on WhatsApp and we check the full catalogue.'),
        ('Where do I find my original part number?', 'On the old pad backing plate, your service invoice, or ask your workshop. A photo of the old pad on WhatsApp also works.'),
    ],
}

LOCATOR = {
    'title': 'Find a Monaer Brake Workshop in Malaysia | S & P Precision Parts',
    'meta': 'Find an authorised workshop in Malaysia that fits Monaer brake pads and discs. Search by state, or WhatsApp us for the nearest one to you.',
    'h1': 'Find a Monaer workshop in Malaysia',
    'lead': 'Authorised workshops that stock and fit Monaer brake parts.',
    'state_h': 'Choose your state',
    'all': 'All states',
    'empty_h': 'More authorised workshops are being added',
    'empty_p': 'We only list workshops that have joined the Monaer network. Ask us on WhatsApp and we tell you where to get Monaer fitted in your area.',
    'ask_btn': 'Ask for a workshop near me',
    'card_call': 'Call', 'card_map': 'Directions', 'card_wa': 'WhatsApp', 'dist_tag': 'Authorised distributor', 'dist_line': 'Supply, part matching and collection.',
    'own_h': 'Run a workshop?',
    'own_p': 'Get listed here when you become an authorised Monaer workshop.',
    'faqs': [
        ('How are workshops listed?', 'Only workshops that have joined as authorised Monaer workshops are shown. We do not list a workshop without its agreement.'),
        ('My area has no workshop yet. What now?', 'WhatsApp us your town. We tell you the nearest place to get Monaer brake parts fitted.'),
    ],
}

JOIN = {
    'title': 'Become an Authorised Monaer Workshop | S & P Precision Parts',
    'meta': 'Workshops in Malaysia: stock Monaer nano ceramic brake pads, discs and fluid from the authorised distributor in Johor and get listed on our workshop finder.',
    'h1': 'Become an authorised Monaer workshop',
    'lead': 'Stock Monaer brake parts direct and get found by drivers near you.',
    'get_h': 'What your workshop gets',
    'get': [
        ('Direct supply', 'Order from the authorised distributor in Skudai, Johor.'),
        ('Listed on the workshop finder', 'Drivers who search for Monaer see your workshop, phone and map link.'),
        ('Part matching help', 'Send us a car or an OE number and we find the Monaer part.'),
        ('One brand for the whole job', 'Pads, discs, brake fluid and brake cleaner in one order.'),
    ],
    'form_h': 'Apply in one minute',
    'form_p': 'Your details go to us on WhatsApp. We reply with the next steps and the terms.',
    'f_name': 'Workshop name', 'f_person': 'Your name', 'f_town': 'Town', 'f_state': 'State', 'f_phone': 'Phone',
    'f_bays': 'Service bays', 'f_bays_opts': ['1 to 2', '3 to 5', '6 or more'], 'f_note': 'Anything else (optional)',
    'f_send': 'Send application on WhatsApp', 'choose': 'Choose',
    'faqs': [
        ('Is there a fee to join?', 'Ask us on WhatsApp. We explain the terms for your workshop directly.'),
        ('Which areas are you looking for?', 'Workshops in Johor and across Malaysia can apply. Tell us your town and we reply with what is possible in your area.'),
    ],
}

FAQ_PAGE = {
    'title': 'Monaer Brake Pads FAQ | S & P Precision Parts, Malaysia',
    'meta': 'Answers about Monaer nano ceramic brake pads in Malaysia: what is special, heat and dust, fitment, discs, fluid, workshops and how to join.',
    'h1': 'Monaer brake parts: questions and answers',
    'lead': 'Short answers for drivers and workshops.',
    'items': [
        ('What is special about Monaer brake pads?', 'They use a nano ceramic material: quieter, low dust and stable when hot. Every set also comes with a fitting kit of cleaner spray, gloves and anti-noise grease.'),
        ('How are they different from the pads my car came with?', 'Factory pads cover basic use. Monaer says its nano ceramic pads give more consistent braking, less noise and less dust in city traffic and daily driving.'),
        ('Nano ceramic or semi-metallic?', 'Semi-metallic pads make more dark dust. Nano ceramic pads are cleaner and quieter, which suits daily driving.'),
        ('How much heat can they take?', 'Monaer lists heat fade resistance from 600°C, and 800°C on its performance pads. Ask us for the figure for your part.'),
        ('How do I check if Monaer fits my car?', 'Use the part finder or send us your car on WhatsApp. We confirm model, size and spec before you buy.'),
        ('Do you have brake discs and brake fluid too?', 'Yes. Monaer has coated high-carbon discs and DOT 4 and DOT 5.1 brake fluid.'),
        ('Do you deliver outside Johor?', 'Ask us on WhatsApp with your town and we tell you the options.'),
        ('How can my workshop stock Monaer?', 'Apply on the For workshops page. We reply on WhatsApp with the next steps.'),
    ],
}

CONTACT = {
    'title': 'Contact S & P Precision Parts | Monaer Distributor, Skudai Johor',
    'meta': 'Contact S & P Precision Parts Sdn Bhd, authorised Monaer brake parts distributor: 016-855 6611, No. 15 Jalan Selesa Indah 9, 81300 Skudai, Johor.',
    'h1': 'Contact S & P Precision Parts',
    'lead': 'WhatsApp is the fastest way to reach us.',
    'about_h': 'About us',
    'about_p': 'S & P Precision Parts Sdn Bhd is an authorised distributor of Monaer brake parts, based in Taman Selesa Indah, Skudai. We supply drivers and workshops with Monaer pads, discs and brake fluid, and we match every part to the car before it goes out.',
}

ARTICLES = {
    'title': 'Brake Tips and News | S & P Precision Parts (Monaer)',
    'meta': 'Brake pad and disc tips for Malaysian drivers and workshops from S & P Precision Parts, the authorised Monaer distributor in Skudai, Johor.',
    'h1': 'Brake tips and news',
    'empty': 'New articles on brake care for Malaysian roads are coming soon.',
}

PRIVACY = {
    'title': 'Privacy Policy | S & P Precision Parts',
    'meta': 'How S & P Precision Parts Sdn Bhd handles your personal data under the Malaysian PDPA.',
    'h1': 'Privacy policy',
    'lead': 'How we handle your details.',
    'body': [
        ('What we collect', 'Only what you send us on WhatsApp, phone or email, such as your name, number, car details and area.'),
        ('Why', 'To reply to you, match brake parts to your car and arrange supply or fitting.'),
        ('This website', 'The forms on this site do not store your details. They open WhatsApp with your message filled in. We count taps on our contact buttons without collecting names or numbers.'),
        ('Your rights', 'You can ask us to see, correct or delete your details at any time by WhatsApp or email.'),
    ],
}

LLMS = {
    'intro': 'S & P Precision Parts Sdn Bhd (Skudai, Johor) is an authorised distributor of Monaer brake parts: nano ceramic brake pads, coated high-carbon brake discs, DOT 4 and DOT 5.1 brake fluid and brake care items. Drivers can check fitment on WhatsApp; workshops can apply to become authorised Monaer workshops.',
}

ALT = {
    'monaer-kit': 'Monaer brake pads, blue Monaer box, brake parts cleaner, grease tubes and gloves',
    'monaer-pads': 'Two Monaer brake pad sets showing the friction surface and backing plates',
    'monaer-box': 'Blue Monaer brake disc box',
    'monaer-care': 'Monaer brake parts cleaner spray, grease tubes and work gloves',
    'sp-banner': 'S & P Precision Parts banner with the Monaer brake range',
    'sp-name-card': 'S & P Precision Parts name card with Skudai address',
}

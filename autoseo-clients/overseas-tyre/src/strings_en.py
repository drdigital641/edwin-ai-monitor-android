# English copy for the Overseas Tyre preview. Same keys in strings_ms.py and strings_zh.py (build.py fails on a mismatch).
# Facts (numbers, address, hours, links) live in facts.json, never here.

SVC_ORDER = ['tyres', 'alignment', 'servicing', 'brakes', 'battery', 'diagnostics']

UI = {
    'skip': 'Skip to content', 'menu': 'Menu', 'close': 'Close menu', 'lang': 'Language',
    'home': 'Home', 'services': 'Services', 'about': 'About us', 'contact': 'Contact', 'articles': 'Articles', 'privacy': 'Privacy',
    'wa_btn': 'WhatsApp us', 'wa_hero': 'WhatsApp us now', 'call_btn': 'Call us', 'call_short': 'Call',
    'wa_label': 'WhatsApp', 'manager': 'In-Charge Manager', 'landline': 'Workshop line', 'email': 'Email', 'facebook': 'Facebook',
    'maps': 'Google Maps', 'waze': 'Waze', 'reviews_link': 'Read our Google reviews', 'michelin_link': 'Michelin dealer locator',
    'hours_h': 'Opening hours', 'closed': 'Closed', 'wed_closed': 'Closed on Wednesdays',
    'open_days': 'Mon–Tue, Thu–Sun', 'wed': 'Wednesday', 'hours_time': '9:30am to 7:30pm',
    'hours_line': 'Open 9:30am to 7:30pm, closed on Wednesdays',
    'address_h': 'Workshop address', 'find_h': 'Find the workshop', 'contact_h': 'Talk to us',
    'see_service': 'More about this service', 'all_services': 'All services', 'see_about': 'About the workshop', 'see_contact': 'Address and hours',
    'breadcrumb': 'Breadcrumb', 'prev': 'Previous photo', 'next': 'Next photo', 'map_title': 'Map to Overseas Tyre in Taman Bukit Indah',
    'rating_of': 'from', 'rating_reviews': 'Google reviews', 'faq_h': 'Questions drivers ask',
    'legal': 'Overseas Tyre And Services Sdn Bhd', 'credit': 'Website by AutoSEO.my', 'sep': '. ', 'also_h': 'Also in the workshop',
}

PREFILL = {
    'default': "Hi Overseas Tyre, I'd like to ask about tyres or servicing. Model and year: ",
    'tyres': "Hi Overseas Tyre, I'd like to ask about new tyres. Tyre size or model and year: ",
    'alignment': "Hi Overseas Tyre, I'd like to ask about wheel alignment and balancing. Model and year: ",
    'servicing': "Hi Overseas Tyre, I'd like to book a car service. Model and year: ",
    'brakes': "Hi Overseas Tyre, I'd like to ask about brakes or suspension. Model and year: ",
    'battery': "Hi Overseas Tyre, I'd like to ask about a car battery or aircon service. Model and year: ",
    'diagnostics': "Hi Overseas Tyre, I'd like to ask about a problem with my car. Model and year: ",
}

HOME = {
    'title': 'Michelin Tyre Shop in Bukit Indah, Johor Bahru | Overseas Tyre',
    'meta': 'Michelin dealer and car workshop in Taman Bukit Indah, Johor Bahru: tyres, wheel alignment, balancing, servicing, brakes and suspension. WhatsApp 018-234 1322.',
    'h1': 'Michelin tyres and car service in Bukit Indah',
    'line': 'Tyres, alignment and servicing in one open bay. Closed Wednesdays.',
    'promise_h': 'One stop for tyres and the car on top of them',
    'promise': 'Overseas Tyre is a Michelin dealer and car workshop on Jalan Indah 16/11 in Taman Bukit Indah, Johor Bahru. Drive in for new tyres, wheel alignment and balancing, a regular service, brakes or suspension, and wait in the air-conditioned room while the bay does the work.',
    'promise_pts': [
        ('Michelin dealer', 'Listed on the Michelin Malaysia dealer locator. Continental tyres and sport rims too.'),
        ('Hunter tyre changer', 'Wheels are fitted on a Hunter machine in our own bay.'),
        ('Clear explanations', 'Our technicians show you what is wrong, with video when it helps.'),
    ],
    'bands_h': 'What we do in the bay',
    'michelin_h': 'Real Michelin jobs from our bay',
    'michelin_p': 'New Michelin Pilot Sport 5 in 225/40ZR18 and Primacy 5 in 225/60R17, straight from the stack to the car. Tell us your size on WhatsApp and we will check stock.',
    'id_h': 'Look for the yellow and blue sign',
    'id_p': 'Our signboard reads Pusat Servis Kereta Dan Tayar, Overseas Tyre And Services Sdn. Bhd. The workshop sits at 2, Jalan Indah 16/11 in Taman Bukit Indah, with open bays and stacks of new tyres out front.',
    'final_h': 'Need tyres or a service this week?',
    'final_line': 'Send your car model and year on WhatsApp. We reply with what it needs.',
    'faq': [
        ('Where is Overseas Tyre?', 'At 2, Jalan Indah 16/11, Taman Bukit Indah, 81200 Johor Bahru, Johor. Open Google Maps or Waze from this page for directions.'),
        ('What are your opening hours?', 'Monday, Tuesday and Thursday to Sunday, 9:30am to 7:30pm. We are closed on Wednesdays.'),
        ('Which tyre brands do you fit?', 'We are a Michelin dealer and also supply Continental tyres. Ask us on WhatsApp for your size.'),
        ('How do I get a quote?', 'WhatsApp 018-234 1322 with your car model, year and tyre size if you know it.'),
    ],
}

BANDS = {
    'tyres': ('Michelin and Continental tyres', 'New tyres supplied and fitted, punctures repaired, worn sets replaced. Bring the size on your sidewall or just your car model.'),
    'fitting': ('Fitted on a Hunter machine', 'Every wheel goes on the Hunter tyre changer in our bay, then gets balanced before it goes back on your car.'),
    'alignment': ('Wheel alignment and balancing', 'Pulling to one side or a shaking wheel? We set the alignment on the rack and balance each wheel.'),
    'servicing': ('Regular car servicing', 'Engine oil, lubricants and general maintenance, done on the lift in the same visit as your tyres.'),
    'brakes': ('Brakes, shock absorbers and suspension', 'Brakes, shock absorbers and suspension parts checked under the car and replaced when they are worn.'),
}

PROCESS = {
    'h2': 'How a tyre job goes',
    'lead': 'Four steps, one visit.',
    'steps': [
        ('WhatsApp us', 'Send your car model and year, and your tyre size if you have it.'),
        ('We inspect and recommend', 'We check your tyres and wheels, then tell you what you need and why.'),
        ('Fit, balance and align', 'New tyres go on the Hunter changer, each wheel is balanced, then the alignment is set.'),
        ('Collect your car', 'We show you what was done, you pay and drive off.'),
    ],
}

PROOF = {
    'h2': 'What Google reviewers rate us',
    'lead': 'Rated by drivers on our Google Business Profile.',
    'rail_h': 'Recent work in our bay',
    'rail_lead': 'Swipe through real jobs from the workshop.',
}

CAPS = {
    'cover': 'Overseas Tyre shopfront in Taman Bukit Indah: blue Michelin fascia, yellow name panel and open service bays',
    'signboard': 'Overseas Tyre signboard: Pusat Servis Kereta Dan Tayar, Overseas Tyre And Services Sdn. Bhd.',
    'bay-alignment': 'Our alignment and service bay with the in-ground alignment rack',
    'hunter-fitting': 'Technician fitting an alloy wheel on our Hunter tyre changer',
    'brakes-suspension': 'Brake disc, hub and shock absorber work under the car',
    'harrier-tyres': 'Toyota Harrier on the lift with a set of new tyres',
    'hrv-tyres': 'Honda HR-V on the two-post lift with four new tyres',
    'vellfire-bay': 'Toyota Vellfire in the open bay',
    'bmw-x5-wheel-off': 'BMW X5 on the lift with the front wheel off',
    'mercedes-wheel': 'Mercedes on the alignment turntable, alloy with an Otani tyre',
    'sport-rim': 'Black multi-spoke sport rim with an Atlander tyre',
    'michelin-ps5-job': 'New Michelin Pilot Sport 5, 225/40ZR18, ready for a Toyota MPV',
    'michelin-ps5-fitted': 'Michelin Pilot Sport 5 fitted on the same Toyota',
    'michelin-primacy-job': 'New Michelin Primacy 5, 225/60R17, for a Toyota Vellfire',
    'branded-voxy': 'The Toyota MPV after its tyre job, with our workshop bumper plate',
    'michelin-ps5-close': 'Michelin Pilot Sport 5 225/40ZR18 sidewall, close up',
    'michelin-primacy-close': 'Michelin Primacy 5 225/60R17 sidewall, close up',
}

SERVICES_PAGE = {
    'title': 'Car Services in Bukit Indah, Johor Bahru | Overseas Tyre',
    'meta': 'Tyres, wheel alignment, balancing, servicing, brakes, suspension, battery, aircon and diagnostics at our Taman Bukit Indah workshop in Johor Bahru.',
    'h1': 'Car workshop services in Bukit Indah',
    'lead': 'Everything we do at our Taman Bukit Indah bay, from Michelin tyres to brakes and aircon.',
}

SERVICES = {
    'tyres': {
        'name': 'Tyres', 'card': 'Michelin dealer. Supply, fitting, repair and replacement.',
        'title': 'Michelin Tyre Dealer in Johor Bahru, Bukit Indah | Overseas Tyre',
        'meta': 'Michelin dealer in Taman Bukit Indah, Johor Bahru. New tyres supplied and fitted on a Hunter changer, puncture repair, Continental tyres and sport rims.',
        'h1': 'Michelin tyre dealer in Bukit Indah, Johor Bahru',
        'lead': 'New tyres, puncture repair and replacement sets, fitted in our own bay.',
        'body': [
            'Overseas Tyre is listed on the Michelin Malaysia dealer locator for Johor Bahru. We supply and fit Michelin tyres, and we also supply Continental tyres and sport rims.',
            'Not sure of your size? Send a photo of the tyre sidewall or just your car model and year on WhatsApp. We will tell you what fits and check stock before you drive in.',
            'Every tyre is fitted on our Hunter tyre changer and each wheel is balanced before it goes back on the car. If your car pulls or the new set wears unevenly, ask us to set the alignment in the same visit.',
        ],
        'list_h': 'Tyre work we do',
        'list': ['New tyre supply and fitting', 'Tyre repair and puncture checks', 'Worn or damaged tyre replacement', 'Michelin and Continental tyres', 'Sport rims', 'Wheel balancing after fitting'],
        'faq': [
            ('Are you a Michelin dealer?', 'Yes. Overseas Tyre And Services is listed on the Michelin Malaysia dealer locator for Johor Bahru.'),
            ('Do you have my tyre size?', 'Send the size on your sidewall or your car model and year on WhatsApp and we will check.'),
        ],
    },
    'alignment': {
        'name': 'Wheel alignment and balancing', 'card': 'Straight steering and smooth wheels.',
        'title': 'Wheel Alignment and Balancing in Bukit Indah, JB | Overseas Tyre',
        'meta': 'Wheel alignment and wheel balancing at Overseas Tyre, Taman Bukit Indah, Johor Bahru. Fix a car that pulls or a shaking steering wheel.',
        'h1': 'Wheel alignment and balancing in Bukit Indah',
        'lead': 'For a car that pulls to one side, a crooked steering wheel or a wheel that shakes.',
        'body': [
            'Our alignment bay has an in-ground alignment rack and turntables. We set the wheel angles so the car tracks straight and the tyres wear evenly.',
            'Balancing is done wheel by wheel. It is the usual fix for a steering wheel that shakes at speed, and we do it every time we fit new tyres.',
            'Ask for an alignment after new tyres, after hitting a kerb or pothole, or when your tyres wear more on one edge.',
        ],
        'list_h': 'Signs you need it',
        'list': ['Car pulls to the left or right', 'Steering wheel not straight', 'Steering wheel shakes at speed', 'Tyres worn on one edge', 'After new tyres or suspension work'],
        'faq': [
            ('Do I need an alignment with new tyres?', 'It is a good idea, especially if the old tyres wore unevenly. Ask us when you book the tyres.'),
            ('Can you balance my wheels without new tyres?', 'Yes. WhatsApp us your car model and we will fit you in.'),
        ],
    },
    'servicing': {
        'name': 'Car servicing', 'card': 'Engine oil, lubricants and regular maintenance.',
        'title': 'Car Servicing and Engine Oil in Bukit Indah, JB | Overseas Tyre',
        'meta': 'Regular car servicing, engine oil, lubricants and general maintenance at Overseas Tyre, Taman Bukit Indah, Johor Bahru.',
        'h1': 'Car servicing and engine oil in Bukit Indah',
        'lead': 'Regular servicing and general maintenance, on the lift next to your tyres.',
        'body': [
            'We do regular car servicing at our Taman Bukit Indah workshop: engine oil and lubricants, and general maintenance checks.',
            'While the car is on the lift we look at the tyres, brakes and suspension too, and tell you what is fine and what needs attention.',
            'WhatsApp your car model and year to ask what your service includes and to book a time.',
        ],
        'list_h': 'Included in our servicing work',
        'list': ['Engine oil and lubricants', 'General maintenance', 'Tyre, brake and suspension check on the lift'],
        'faq': [
            ('Which cars do you service?', 'Our bay sees Toyota, Honda, BMW, Mercedes and more. Send your model and year to check.'),
            ('Can I wait for my car?', 'Yes. We have a clean, air-conditioned waiting room.'),
        ],
    },
    'brakes': {
        'name': 'Brakes and suspension', 'card': 'Brakes, shock absorbers, suspension and spare parts.',
        'title': 'Brakes, Shock Absorbers and Suspension in Bukit Indah | Overseas Tyre',
        'meta': 'Brake, shock absorber and suspension repair with spare parts at Overseas Tyre, Taman Bukit Indah, Johor Bahru.',
        'h1': 'Brakes, shock absorbers and suspension in Bukit Indah',
        'lead': 'Brake and suspension work under the car, with spare parts supplied.',
        'body': [
            'Our technicians work on brakes, discs and hubs, shock absorbers and suspension parts with the car up on the lift.',
            'We supply the spare parts and explain what is worn before we replace anything. Ask us to show you, with video when it helps.',
            'If you hear knocking over bumps, feel the car bounce, or your brakes squeal or pull, WhatsApp us your car model and year.',
        ],
        'list_h': 'What we check and replace',
        'list': ['Brakes', 'Shock absorbers', 'Suspension parts', 'Spare parts supply'],
        'faq': [
            ('Will you explain what is wrong first?', 'Yes. Our technicians show you the worn part, with video when it helps, before replacing it.'),
            ('Do you supply the parts?', 'Yes. Spare parts are supplied by the workshop.'),
        ],
    },
    'battery': {
        'name': 'Battery and aircon', 'card': 'Car battery replacement and air-conditioning service.',
        'title': 'Car Battery and Aircon Service in Bukit Indah, JB | Overseas Tyre',
        'meta': 'Car battery replacement and car air-conditioning service at Overseas Tyre, Taman Bukit Indah, Johor Bahru.',
        'h1': 'Car battery and aircon service in Bukit Indah',
        'lead': 'A new battery or a car aircon that blows cold again.',
        'body': [
            'We replace car batteries and service car air-conditioning at our Taman Bukit Indah workshop.',
            'If your car is slow to start or the aircon is not as cold as it was, WhatsApp us your car model and year and tell us what you notice.',
            'Battery and aircon work can be done in the same visit as your tyres or a regular service.',
        ],
        'list_h': 'Battery and aircon work',
        'list': ['Car battery replacement', 'Car air-conditioning service'],
        'faq': [
            ('Can you check my aircon on the same day as my tyres?', 'Ask us on WhatsApp when you book and we will plan both.'),
        ],
    },
    'diagnostics': {
        'name': 'Diagnostics', 'card': 'Troubleshooting with clear explanations.',
        'title': 'Car Diagnostics and Troubleshooting in Bukit Indah | Overseas Tyre',
        'meta': 'Car diagnostics and troubleshooting at Overseas Tyre, Taman Bukit Indah, Johor Bahru. Technicians explain the problem clearly, with video.',
        'h1': 'Car diagnostics and troubleshooting in Bukit Indah',
        'lead': 'We find the problem first, then explain it clearly before any repair.',
        'body': [
            'Warning light, strange noise or a car that just does not feel right? Our technicians troubleshoot the problem at our Taman Bukit Indah workshop.',
            'We explain what we find in plain words and show you the defect, with video when it helps, so you can decide on the repair.',
            'WhatsApp us your car model and year and describe what you notice. A short video of the noise or warning light helps.',
        ],
        'list_h': 'Bring the car in for',
        'list': ['Warning lights', 'Strange noises or vibration', 'Starting or running problems', 'A second look before a big repair'],
        'faq': [
            ('Will you tell me what is wrong before fixing it?', 'Yes. We explain the defect clearly, with video when it helps, before any repair.'),
        ],
    },
}

ABOUT = {
    'title': 'About Overseas Tyre, Taman Bukit Indah, Johor Bahru',
    'meta': 'Overseas Tyre And Services Sdn Bhd: Pusat Servis Kereta Dan Tayar and Michelin dealer at 2, Jalan Indah 16/11, Taman Bukit Indah, Johor Bahru.',
    'h1': 'Pusat Servis Kereta Dan Tayar in Taman Bukit Indah',
    'lead': 'A Michelin dealer and car workshop on Jalan Indah 16/11.',
    'body': [
        'Overseas Tyre And Services Sdn Bhd runs a tyre and car service centre at 2, Jalan Indah 16/11, Taman Bukit Indah, Johor Bahru. Our signboard reads Pusat Servis Kereta Dan Tayar.',
        'We are a Michelin dealer, listed on the Michelin Malaysia dealer locator, and we also supply Continental tyres and sport rims. Tyres are fitted on a Hunter tyre changer in our own bay.',
        'Beyond tyres, we do wheel alignment and balancing, regular servicing with engine oil and lubricants, brakes, shock absorbers and suspension, car batteries, aircon and diagnostics.',
        'Our technicians explain defects clearly, with video when it helps. While you wait, there is a clean, air-conditioned waiting room.',
    ],
    'vals_h': 'What drivers get here',
    'vals': [
        ('Michelin dealer', 'Listed on the Michelin Malaysia dealer locator.'),
        ('Own fitting bay', 'Hunter tyre changer, alignment rack and lifts.'),
        ('Straight answers', 'Defects explained clearly, with video.'),
        ('Cool waiting room', 'Clean and air-conditioned.'),
    ],
}

CONTACT = {
    'title': 'Contact Overseas Tyre, Bukit Indah, Johor Bahru',
    'meta': 'WhatsApp 018-234 1322. 2, Jalan Indah 16/11, Taman Bukit Indah, 81200 Johor Bahru. Open 9:30am to 7:30pm, closed on Wednesdays.',
    'h1': 'Contact Overseas Tyre in Bukit Indah',
    'lead': 'WhatsApp is fastest. Send your car model and year.',
    'wa_note': 'Main line, WhatsApp and calls',
    'manager_note': 'Calls',
    'landline_note': 'As listed on Google',
    'dir_h': 'Getting here',
    'dir_p': 'We are at 2, Jalan Indah 16/11 in Taman Bukit Indah. Look for the blue Michelin fascia and the yellow name panel.',
}

ARTICLES = {
    'title': 'Tyre and Car Care Articles | Overseas Tyre, Bukit Indah',
    'meta': 'Tyre and car care articles from Overseas Tyre, a Michelin dealer and car workshop in Taman Bukit Indah, Johor Bahru.',
    'h1': 'Tyre and car care articles',
    'lead': 'Notes from our Bukit Indah bay on tyres, alignment and servicing will appear here soon.',
}

PRIVACY = {
    'title': 'Privacy | Overseas Tyre',
    'meta': 'How the Overseas Tyre website handles your information.',
    'h1': 'Privacy',
    'body': [
        ('Who we are', 'This website belongs to Overseas Tyre And Services Sdn Bhd, 2, Jalan Indah 16/11, Taman Bukit Indah, 81200 Johor Bahru, Johor, Malaysia.'),
        ('What we collect', 'The site has no forms. When you tap WhatsApp, call or email, you contact us directly through that app, and we only see what you send us.'),
        ('Button taps', 'We count taps on our WhatsApp, call, email, map and Facebook buttons to see which parts of the site help drivers. This count uses a random visit code, the page and the button, and does not identify you.'),
        ('Maps', 'The contact page shows a Google Maps map. Google may set its own cookies when the map loads.'),
        ('Your requests', 'To ask about your information, email overseastyrebi@gmail.com or WhatsApp 018-234 1322.'),
    ],
}

SCHEMA = {
    'description': 'Michelin dealer and car workshop in Taman Bukit Indah, Johor Bahru: tyres, wheel alignment and balancing, servicing, brakes, suspension, battery, aircon and diagnostics.',
    'knows': ['Tyre supply and fitting', 'Tyre repair', 'Wheel alignment', 'Wheel balancing', 'Car servicing', 'Engine oil', 'Brakes', 'Shock absorbers', 'Suspension', 'Car battery replacement', 'Car air-conditioning service', 'Car diagnostics'],
}

LLMS = {
    'intro': 'Overseas Tyre And Services Sdn Bhd (Pusat Servis Kereta Dan Tayar) is a Michelin dealer and car workshop in Taman Bukit Indah, Johor Bahru, Malaysia.',
}

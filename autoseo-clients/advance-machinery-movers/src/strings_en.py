# English copy for the Advance Machinery Movers preview. Same keys in strings_ms.py and strings_zh.py (build.py fails on a mismatch).
# Facts (numbers, address, hours, links, names) live in facts.json. Wording below only restates the 2026 business card and
# www.advance-movers.com as recorded in the drop facts; nothing is invented (no rates, tonnage beyond 10-ton, licences or projects).

SVC_ORDER = ['rigging', 'relocation', 'stuffing', 'crating', 'alignment', 'rental']

UI = {
    'skip': 'Skip to content', 'menu': 'Menu', 'close': 'Close menu', 'lang': 'Language',
    'home': 'Home', 'services': 'Services', 'about': 'About us', 'contact': 'Contact', 'articles': 'Articles', 'privacy': 'Privacy',
    'wa_btn': 'WhatsApp us', 'wa_hero': 'WhatsApp Mei Wan', 'call_btn': 'Call the office', 'call_short': 'Call',
    'wa_label': 'WhatsApp', 'wa_who': 'Wong Mei Wan, Assistant Manager', 'landline': 'Office', 'fax': 'Fax',
    'email': 'Email', 'email_general': 'General enquiries', 'email_meiwan': 'Wong Mei Wan',
    'maps': 'Google Maps', 'waze': 'Waze', 'listing': 'Our Google listing',
    'hours_h': 'Opening hours', 'closed': 'Closed', 'open_days': 'Monday to Saturday', 'sun': 'Sunday', 'hours_time': '8:00am to 5:00pm',
    'hours_line': 'Monday to Saturday 8:00am to 5:00pm. Sunday closed.',
    'address_h': 'Office and workshop', 'find_h': 'Find us', 'contact_h': 'Talk to us',
    'see_service': 'See this service', 'all_services': 'All services', 'see_about': 'About the company',
    'breadcrumb': 'Breadcrumb', 'prev': 'Previous photo', 'next': 'Next photo', 'map_title': 'Map to Advance Machinery Movers in Taman Perindustrian Tampoi Jaya',
    'faq_h': 'Questions factories ask', 'company_no': 'Company no.', 'credit': 'Website by AutoSEO.my',
    'authority': '29 Years in Operation · Approaching 30 Years in 2027', 'where': 'Tampoi Jaya, Johor Bahru',
    'stop': 'Stop', 'step': 'Step', 'served_h': 'Companies we have served',
}

PREFILL = {
    'default': "Hi Advance Machinery Movers, I'd like to ask about machinery moving or plant relocation.",
    'rigging': "Hi Advance Machinery Movers, I'd like to ask about moving, dismantling or installing a machine.",
    'relocation': "Hi Advance Machinery Movers, I'd like to ask about a plant relocation.",
    'stuffing': "Hi Advance Machinery Movers, I'd like to ask about stuffing or unstuffing machines from a container.",
    'crating': "Hi Advance Machinery Movers, I'd like to ask about wooden crates or vacuum packing for a machine.",
    'alignment': "Hi Advance Machinery Movers, I'd like to ask about precision alignment after a machine move.",
    'rental': "Hi Advance Machinery Movers, I'd like to ask about renting the heavy forklift or side loader.",
}

HOME = {
    'title': 'Machinery Movers & Plant Relocation in Johor Bahru | Advance Machinery Movers',
    'meta': 'Machinery moving, rigging and millwright work, plant relocation, container stuffing, wooden crates and heavy forklift rental from Tampoi Jaya, Johor Bahru. Since 1997. WhatsApp 016-722 6779.',
    'h1': 'Machinery movers and plant relocation in Johor Bahru',
    'promise_h': 'Heavy machines, moved and set down right',
    'promise': 'Advance Machinery Movers Sdn. Bhd. has handled heavy machinery for factories since 1997. One crew takes a machine from dismantling, lifting and transport through to installation and precision alignment, for MNCs and SMEs in Malaysia and Singapore.',
    'promise_pts': [
        ('Since 1997', 'Incorporated in Johor Bahru. 29 years in operation, our 30th year comes in 2027.'),
        ('Malaysia and Singapore', 'Moving and packing work on both sides of the Causeway.'),
        ('Insured and trained', 'Goods-in-transit insurance, and crews trained in forklift operation and safety by UMW and CIDB.'),
    ],
    'journey_h': 'One machine, from its old floor to its new one',
    'journey_lead': 'Most jobs follow the same path. We can take every stop, or only the ones you need.',
    'journey': [
        ('rigging', 'crane-lift', 'Lift and shift', 'Cranes, forklifts, dollies and our own custom equipment take the machine off its base and onto the trailer.'),
        ('crating', 'wooden-crates', 'Crate and pack', 'Custom wooden crates built to the machine, normal pack or vacuum pack, with certified fumigation when the shipment needs it.'),
        ('stuffing', 'container-stuffing', 'Into the container', 'Machines stuffed and unstuffed using ramps, forklifts, dollies and special-made equipment, without damage.'),
        ('alignment', 'precision-install', 'Install and align', 'At the new floor we install the machine and finish with precision alignment.'),
    ],
    'more_h': 'Also on our card',
    'timeline_h': 'How a plant relocation runs',
    'timeline_lead': 'For a full line or a whole plant, the job is planned stop by stop.',
    'rail_h': 'Real jobs by our crew',
    'rail_lead': 'Photos from moves, lifts and installs in factories and yards.',
    'fleet_h': 'Our own forklifts and crew',
    'fleet_p': 'Toyota and TCM forklifts line up outside our Tampoi Jaya workshop. A 10-ton forklift and the side loader are also available for rent.',
    'team_p': 'The same crew in brown and green, celebrating Chinese New Year at our premises.',
    'final_h': 'Planning a machine move or a relocation?',
    'final_line': 'Send Mei Wan the machine, the address and your date on WhatsApp.',
    'faq': [
        ('What are your opening hours?', 'Monday to Saturday, 8:00am to 5:00pm. We are closed on Sunday.'),
        ('Do you work in Singapore as well as Malaysia?', 'Yes. We provide moving and packing services in Malaysia and Singapore, from our office in Taman Perindustrian Tampoi Jaya, Johor Bahru.'),
        ('Can I rent a heavy forklift?', 'Yes. A 10-ton forklift and a side loader are available for rent at competitive prices. WhatsApp us with your dates and site.'),
        ('How long have you been in business?', 'Advance Machinery Movers Sdn. Bhd. was incorporated in 1997 in Johor Bahru. 2026 is our 29th year in operation, and 2027 is our 30th anniversary.'),
        ('Are machines insured while you move them?', 'We have goods-in-transit insurance coverage, and our personnel are covered by Personal Accident (PA) insurance.'),
    ],
}

SERVICES = {
    'rigging': {
        'name': 'Rigging & Millwright Services',
        'card': 'Moving, dismantling and installation of all types of machines.',
        'title': 'Rigging & Millwright Services in Johor Bahru | Advance Machinery Movers',
        'meta': 'Rigging and millwright services in Johor Bahru: moving, lifting, shifting, dismantling and installation of all types of machines, through to precision alignment. Malaysia and Singapore.',
        'h1': 'Rigging and millwright services',
        'lead': 'Moving, dismantling and installation of all types of machines, from one crew.',
        'body': [
            'We have specialised in handling all kinds of heavy machinery since 1997. The full service covers dismantling, moving, shifting, transporting, unloading and installation, right up to precision alignment.',
            'Every factory floor is different, so we use custom-made equipment such as hoists, dollies, trucks and forklifts to suit the space, the access and the machine.',
            'Tell us what the machine is, where it stands now and where it needs to go. We will plan the lift and the move with you.',
        ],
        'list_h': 'What the job covers',
        'list': ['Dismantling machines', 'Lifting and shifting', 'Transporting and unloading', 'Installation at the new site', 'Precision alignment to finish'],
        'faq': [
            ('Which machines do you move?', 'All types of machines, from single units to full production equipment, in factories in Malaysia and Singapore.'),
            ('Do you install the machine as well?', 'Yes. Our full service runs from dismantling and moving through to installation and precision alignment.'),
        ],
    },
    'relocation': {
        'name': 'Plant Relocation',
        'card': 'A whole line or plant, dismantled, moved and set up again.',
        'title': 'Plant Relocation in Johor Bahru, Malaysia & Singapore | Advance Machinery Movers',
        'meta': 'Plant relocation from Johor Bahru: dismantling, packing, moving, installation and precision alignment of production machinery, in Malaysia and Singapore. WhatsApp Wong Mei Wan.',
        'h1': 'Plant relocation',
        'lead': 'Dismantle, pack, move, install and align, planned as one job.',
        'body': [
            'When a whole line or plant has to move, the risk sits in the handovers. We keep the job with one crew, from taking the machines down to setting them up and aligning them on the new floor.',
            'Our relocation work uses the same services we offer one by one: rigging and millwright work, wooden crates and vacuum packing, container stuffing and unstuffing, and precision alignment.',
            'We work in Malaysia and Singapore. Send us the machine list and both addresses to start.',
        ],
        'list_h': 'What a relocation includes',
        'list': ['Planning with your team', 'Dismantling the machines', 'Crating or packing for the trip', 'Lifting, loading and transport', 'Installation and precision alignment'],
        'faq': [
            ('Where do you relocate plants?', 'In Malaysia and Singapore, from our base in Taman Perindustrian Tampoi Jaya, Johor Bahru.'),
            ('How do we start?', 'WhatsApp Wong Mei Wan on 016-722 6779 with your machine list, the current and new addresses, and your target dates.'),
        ],
    },
    'stuffing': {
        'name': 'Stuffing & Unstuffing Machines of the Container',
        'card': 'Machines into and out of containers, safely and without damage.',
        'title': 'Container Stuffing & Unstuffing of Machines, Johor Bahru | Advance Machinery Movers',
        'meta': 'Stuffing and unstuffing machines from shipping containers in Johor Bahru, using ramps, forklifts, dollies and special-made equipment. Malaysia and Singapore.',
        'h1': 'Stuffing and unstuffing machines of the container',
        'lead': 'Machines into and out of containers, swiftly, safely and without damage.',
        'body': [
            'Machines shipped in containers need care at both ends. We stuff and unstuff them professionally, swiftly and safely, so they arrive without damage.',
            'Depending on the machine and the container, we use ramps, forklifts, dollies and special-made equipment to move the load in and out.',
            'If the machine also needs crating or vacuum packing before it goes into the container, we can do that too.',
        ],
        'list_h': 'Equipment we use',
        'list': ['Ramps', 'Forklifts', 'Dollies', 'Special-made equipment'],
        'faq': [
            ('Can you pack the machine before stuffing?', 'Yes. We build custom wooden crates and offer normal pack or vacuum pack, with certified fumigation if required.'),
            ('Do you also unstuff incoming containers?', 'Yes. We handle both stuffing and unstuffing of machines.'),
        ],
    },
    'crating': {
        'name': "Wooden Crates' Packing & Vacuum Packing",
        'card': 'Custom wooden crates, normal pack or vacuum pack, for local and overseas shipments.',
        'title': 'Wooden Crates & Vacuum Packing for Machines, Johor Bahru | Advance Machinery Movers',
        'meta': 'Custom wooden crates and vacuum packing for machines in Johor Bahru, for local and overseas shipments, with certified fumigation if required.',
        'h1': "Wooden crates' packing and vacuum packing",
        'lead': 'Custom crates for local and overseas shipments. No size too large or too small.',
        'body': [
            'We build wooden crates to fit each machine, for local deliveries and overseas shipments. No size is too large or too small.',
            'Choose normal pack or vacuum pack, depending on the machine and the journey. Certified fumigation is available if your shipment requires it.',
            'Crating can be booked on its own, or as one stop in a full move or plant relocation.',
        ],
        'list_h': 'Packing options',
        'list': ['Custom-made wooden crates', 'Normal pack', 'Vacuum pack', 'Certified fumigation if required', 'Local and overseas shipments'],
        'faq': [
            ('Do you make crates for export?', 'Yes. Our custom crates are made for local and overseas shipments, with certified fumigation if required.'),
            ('Is there a size limit?', 'No size is too large or too small. Send us the machine details on WhatsApp.'),
        ],
    },
    'alignment': {
        'name': 'Precision Alignment',
        'card': 'The last step of an install: machines set and aligned on the new floor.',
        'title': 'Precision Alignment of Machines in Johor Bahru | Advance Machinery Movers',
        'meta': 'Precision alignment after machine installation in Johor Bahru, as the final step of our dismantling and installation service. Malaysia and Singapore.',
        'h1': 'Precision alignment',
        'lead': 'The final step of our dismantling and installation service.',
        'body': [
            'A machine that has been moved is only finished when it is set down and aligned. Our dismantling and installation service runs right up to precision alignment.',
            'Precision alignment is listed as its own service on our card, so you can book it as part of a move or plant relocation with us.',
            'Tell us about the machine and the site on WhatsApp and we will advise on the job.',
        ],
        'list_h': 'Where it fits',
        'list': ['After installation at a new site', 'As the last stop of a plant relocation', 'Part of our rigging and millwright work'],
        'faq': [
            ('Is alignment included when you install a machine?', 'Our full dismantling and installation service runs right up to precision alignment.'),
            ('Can I book alignment with a relocation?', 'Yes. Precision alignment is one of the six services on our card. WhatsApp us with the machine details.'),
        ],
    },
    'rental': {
        'name': 'Rental of Heavy Forklift & Side Loader',
        'card': 'A 10-ton forklift and a side loader for rent at competitive prices.',
        'title': 'Heavy Forklift & Side Loader Rental in Johor Bahru | Advance Machinery Movers',
        'meta': 'Rent a 10-ton forklift or a side loader in Johor Bahru at competitive prices from Advance Machinery Movers, Taman Perindustrian Tampoi Jaya. WhatsApp 016-722 6779.',
        'h1': 'Rental of heavy forklift and side loader',
        'lead': 'A 10-ton forklift and a side loader, available for rent at competitive prices.',
        'body': [
            'Need lifting power for a few days? Our 10-ton forklift and our side loader (also called a side lorry) are available for rent at competitive prices.',
            'WhatsApp Wong Mei Wan with your dates, your site address and what needs moving, and we will reply with availability and a quote.',
        ],
        'list_h': 'Available for rent',
        'list': ['10-ton forklift', 'Side loader (side lorry)'],
        'faq': [
            ('What can I rent?', 'A 10-ton forklift and a side loader, at competitive prices.'),
            ('How do I get a rental quote?', 'WhatsApp 016-722 6779 or call the office on 07-236 9348 with your dates and site.'),
        ],
    },
}

TIMELINE = [
    ('Survey', 'We look at the machines, the access and the route with your team.'),
    ('Dismantle', 'Machines are taken down and prepared for lifting.'),
    ('Pack', 'Wooden crates, normal pack or vacuum pack where the trip needs it.'),
    ('Move', 'Lifting, loading, container stuffing and transport.'),
    ('Install', 'Machines unloaded and installed at the new site.'),
    ('Precision alignment', 'The last step, so the line is ready to run.'),
]

CAPS = {
    'cover': 'Our crew in brown-and-green uniforms with forklifts at the Tampoi Jaya workshop, under the trilingual company signboard.',
    'og': 'Forklifts lined up at the Advance Machinery Movers workshop in Taman Perindustrian Tampoi Jaya, under the company signboard.',
    'unit-14': 'Unit 14, Jalan Bayu 2/1: our two-storey unit with a green roof, signboard showing 14 and 441099-U, pallet trucks and timber below.',
    'fleet': 'Toyota and TCM forklifts lined up at our workshop entrance under the trilingual signboard.',
    'team-cny': 'Our team in brown and green uniforms celebrating Chinese New Year with a lion dance at the premises.',
    'training': 'In-house safety training in our meeting room: crew with gloves and helmets, a trainer at the whiteboard and screen.',
    'crane-lift': 'A mobile crane lifts a large machine onto a long trailer while our crew guides the load.',
    'container-lift': 'A crane lifts an open-top container holding a machine at a works yard.',
    'container-stuffing': 'A forklift stuffs a wrapped machine into a shipping container at a factory loading bay.',
    'wooden-crates': 'Crew in high-visibility vests load large custom wooden crates onto a trailer.',
    'protective-packing': 'A large machine sealed in protective foil wrap on timber skids, ready for shipment.',
    'heavy-forklift': 'A heavy forklift moves a blue industrial press inside a factory bay.',
    'dismantling': 'Our crew works on a large green machine in a factory bay, with an overhead crane and forklift in use.',
    'precision-install': 'Technicians in protective suits and yellow helmets working inside a machine frame during installation.',
    'plant-relocation': 'A crane lifts a large industrial press onto a green truck during a machinery move.',
    'logo': 'Advance Machinery Movers logo',
}

SERVICES_PAGE = {
    'title': 'Machinery Moving Services in Johor Bahru | Advance Machinery Movers',
    'meta': 'Six services from Advance Machinery Movers, Johor Bahru: rigging and millwright, plant relocation, container stuffing, wooden crates and vacuum packing, precision alignment, heavy forklift rental.',
    'h1': 'Our services',
    'lead': 'Six services on our card, from one crew in Tampoi Jaya, Johor Bahru.',
}

ABOUT = {
    'title': 'About Advance Machinery Movers Sdn. Bhd. | Since 1997, Johor Bahru',
    'meta': 'Advance Machinery Movers Sdn. Bhd. (441099-U) was incorporated in 1997 in Johor Bahru: 29 years moving machinery for factories in Malaysia and Singapore, 30th anniversary in 2027.',
    'h1': 'About Advance Machinery Movers',
    'lead': 'Incorporated in 1997 in Johor Bahru. 29 years in operation, and our 30th anniversary in 2027.',
    'story_h': 'A Johor Bahru company since 1997',
    'story': [
        'Advance Machinery Movers Sdn. Bhd. (441099-U) was incorporated in 1997 in Johor Bahru, Malaysia. We are a service provider in the moving and packing industry in Malaysia and Singapore.',
        'Our customer base includes MNCs and SMEs. 2026 is our 29th year in operation, and we reach our 30th anniversary in 2027.',
    ],
    'sign_h': 'Our signboard, in three languages',
    'sign_p': 'Our office and workshop are at 14 & 20, Jalan Bayu 2/1, Taman Perindustrian Tampoi Jaya. The signboard reads:',
    'safety_h': 'Trained crews, insured moves',
    'safety': [
        ('Training', 'Our personnel are fully trained in forklift operations and safety issues by UMW and CIDB. Regular in-house and on-site training is carried out.'),
        ('Licences', 'Our staff have the required licences.'),
        ('Goods-in-transit insurance', 'We have insurance coverage for goods in transit.'),
        ('Personal Accident insurance', 'Our personnel are covered by Personal Accident (PA) insurance.'),
    ],
    'vm_h': 'How we work',
    'vision': ['To provide a comprehensive service', 'We move it differently'],
    'mission': ['Safety and reliability, always', 'Your machines reach their final destination in good condition and on time', 'Our word is our honour'],
    'vision_h': 'Vision', 'mission_h': 'Mission',
    'served_p': 'A selection of the companies named on our customer page and in our past customer logos. Listed for reference only.',
    'team_h': 'The people behind the moves',
}

CONTACT = {
    'title': 'Contact Advance Machinery Movers | Tampoi Jaya, Johor Bahru',
    'meta': 'Contact Advance Machinery Movers: WhatsApp Wong Mei Wan 016-722 6779, office 07-236 9348, 14 & 20 Jalan Bayu 2/1, Taman Perindustrian Tampoi Jaya, 81200 Johor Bahru. Mon to Sat 8am to 5pm.',
    'h1': 'Contact us',
    'lead': 'WhatsApp is the fastest way to reach Wong Mei Wan, our Assistant Manager.',
    'wa_note': 'Machine type, both addresses and your dates help us reply faster.',
    'office_note': 'Office line, Monday to Saturday 8:00am to 5:00pm.',
    'fax_note': 'Fax',
    'dir_h': 'Getting here',
    'dir_p': 'We are on Jalan Bayu 2/1 in Taman Perindustrian Tampoi Jaya, Johor Bahru. Open Google Maps or Waze for directions.',
}

ARTICLES = {
    'title': 'Articles | Advance Machinery Movers, Johor Bahru',
    'meta': 'Articles from Advance Machinery Movers on machinery moving, plant relocation, crating and container stuffing in Johor Bahru, Malaysia and Singapore.',
    'h1': 'Articles',
    'lead': 'Guides on machinery moving and plant relocation are on the way. Until then, our services are below.',
}

PRIVACY = {
    'title': 'Privacy | Advance Machinery Movers',
    'meta': 'How Advance Machinery Movers Sdn. Bhd. handles the details you send by WhatsApp, phone or email.',
    'h1': 'Privacy',
    'body': [
        ('What we collect', 'When you contact us by WhatsApp, phone, fax or email, we receive the details you choose to send, such as your name, company, number and job details.'),
        ('How we use it', 'We use these details only to reply to you, quote and carry out the job. We do not sell your details.'),
        ('Button taps', 'This website counts taps on its WhatsApp, call, email and map buttons to see which buttons help visitors. It does not record your IP address or fingerprint your device.'),
        ('Contact', 'To ask about or remove your details, email advance.movers@yahoo.com or call 07-236 9348.'),
    ],
}

SCHEMA = {
    'description': 'Machinery movers in Johor Bahru since 1997: rigging and millwright services, plant relocation, container stuffing and unstuffing, wooden crates and vacuum packing, precision alignment, and heavy forklift and side loader rental, in Malaysia and Singapore.',
    'knows': ['Machinery moving', 'Rigging', 'Millwright services', 'Plant relocation', 'Container stuffing', 'Wooden crate packing', 'Vacuum packing', 'Precision alignment', 'Forklift rental'],
}

LLMS = {
    'intro': 'Advance Machinery Movers Sdn. Bhd. (441099-U, 先進機械搬運私人有限公司) is a machinery moving company in Taman Perindustrian Tampoi Jaya, Johor Bahru, incorporated in 1997, serving factories in Malaysia and Singapore.',
}

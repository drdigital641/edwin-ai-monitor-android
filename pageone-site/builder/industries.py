# Industry pages (/industries/<slug>/), the industries hub and the free website check page.
# Run from build.py (exec), so it uses build.py's helpers: page, hero, cta, service, SITE, WA_LINK, HERE.
# Content rules: only real results (Search Console numbers already published on /results/), example searches are
# labelled as examples, no invented statistics, no ranking guarantees.

PROOF_GARAGE = """<div class="kpis reveal">
          <div class="kpi"><div class="label">Edwin Garage: clicks from Google</div><div class="value">""" + EG["clicks"] + """</div><div class="delta">28 days to """ + THROUGH_SHORT + """</div></div>
          <div class="kpi"><div class="label">Average position</div><div class="value">""" + EG["pos"] + """</div><div class="delta">Page one is 1 to 10</div></div>
          <div class="kpi"><div class="label">Searches on page one</div><div class="value">""" + EG["page_one"] + """</div><div class="delta">Google Search Console</div></div>
        </div>
        <p class="note reveal">Edwin Garage is Edwin's own car workshop in Ang Mo Kio, where this system was first built and tested. <a class="link" href="/results/">See the full case study →</a></p>"""

PROOF_CLEANIC = """<div class="kpis reveal">
          <div class="kpi"><div class="label">Cleanic Detailing: clicks from Google</div><div class="value">""" + CL["clicks"] + """</div><div class="delta">28 days to """ + THROUGH_SHORT + """</div></div>
          <div class="kpi"><div class="label">Average position</div><div class="value">""" + CL["pos"] + """</div><div class="delta">From """ + CL["prev_pos"] + """ the 28 days before</div></div>
          <div class="kpi"><div class="label">Searches on page one</div><div class="value">""" + CL["page_one"] + """</div><div class="delta">Google Search Console</div></div>
        </div>
        <p class="note reveal">Cleanic Detailing is a Singapore car grooming business we run the website and SEO for. <a class="link" href="/results/">See the full case study →</a></p>"""


def site_proof(url, label, what):
    return f"""<p class="section-lead reveal">We built and run the website for <a class="link" href="{url}" target="_blank" rel="noopener">{label}</a>, {what}. Visit it and judge for yourself: it's the same system you get. <a class="link" href="/results/">See our Google results →</a></p>"""


INDUSTRIES = [
    {
        "slug": "car-workshop", "name": "Car workshops", "short": "car workshop",
        "title": "SEO &amp; Website for Car Workshops in Singapore | Page One",
        "desc": "Get your car workshop found on Google, Google Maps and ChatGPT. Built and proven on Edwin Garage in Ang Mo Kio. S$20/month, no setup fee, no contract.",
        "h1": "Get your car workshop found on Google",
        "lead": "Drivers search for a workshop when something goes wrong: a warning light, a strange noise, a servicing that's due. Page One makes sure your workshop shows up on Google, Google Maps and ChatGPT at that moment. Built and proven on Edwin's own workshop.",
        "searches": ["car servicing Ang Mo Kio", "car aircon not cold repair", "workshop near me open Sunday", "accident claim workshop Singapore", "brake pad replacement price"],
        "needs": [("A page for each service", "Servicing, aircon, brakes, accident claims, tyres: each gets its own page, so Google can match it to what drivers type."),
                  ("Your location, made obvious", "Your address, opening hours and area in the right places, so you appear for \"near me\" searches and on Google Maps."),
                  ("Trust before they call", "Photos of your workshop and work, what brands you handle, and a one-tap WhatsApp button for quotes.")],
        "proof": PROOF_GARAGE,
        "faqs": [("Can SEO really bring customers to a car workshop?", "It's how Edwin Garage gets found: in the 28 days to " + THROUGH + " it got " + EG["clicks"] + " clicks from Google with an average position of " + EG["pos"] + ", according to Google Search Console. Results vary by workshop and area, so we don't guarantee them."),
                 ("Do I need to do anything technical?", "No. Tell us your services, brands and area and send some photos on WhatsApp. We do the website, Google Maps, Google and Bing setup."),
                 ("I already have a website. Do I need a new one?", "No. We can add an SEO landing page next to it on a subdomain, or take over looking after your existing site.")],
    },
    {
        "slug": "car-detailing", "name": "Car detailing &amp; grooming", "short": "car detailing business",
        "title": "SEO &amp; Website for Car Detailing in Singapore | Page One",
        "desc": "Car grooming, coating and interior cleaning businesses: get found on Google, Maps and ChatGPT. Proven on Cleanic Detailing. S$20/month, no contract.",
        "h1": "Get your car detailing business found on Google",
        "lead": "Car owners compare detailers online before they book: coating, polishing, interior cleaning, odour removal. Page One puts your services in front of them on Google, Google Maps and ChatGPT, with the same system that runs Cleanic Detailing.",
        "searches": ["car interior cleaning Singapore", "ceramic coating price", "car polish near me", "car odour removal", "mobile car wash at home"],
        "needs": [("Pages for each service", "Coating, polishing, interior steam cleaning, odour removal: separate pages so each can show up for its own searches."),
                  ("Before-and-after photos", "Real photos of your work, labelled so Google Images and AI assistants understand them."),
                  ("Easy booking", "A WhatsApp button and clear service areas, so customers can ask for a slot in one tap.")],
        "proof": PROOF_CLEANIC,
        "faqs": [("Does this work for mobile detailers without a shop?", "Yes. Google lets service-area businesses hide their address and list the areas they cover. We set that up for you."),
                 ("What results have you had in this industry?", "Cleanic Detailing got " + CL["clicks"] + " clicks from Google in the 28 days to " + THROUGH + " and appeared on page one for " + CL["page_one"] + " different searches, according to Google Search Console. Results vary, so we don't guarantee them."),
                 ("How long does it take?", "Your site is usually live within 7 days. Search results build over weeks to months; Cleanic Detailing took about three months to reach these numbers.")],
    },
    {
        "slug": "cleaning-services", "name": "Cleaning services", "short": "cleaning business",
        "title": "SEO &amp; Website for Cleaning Services in Singapore | Page One",
        "desc": "Home, office, sofa and mattress cleaning businesses: get found on Google, Google Maps and ChatGPT. S$20/month, website included, no setup fee.",
        "h1": "Get your cleaning business found on Google",
        "lead": "People search for cleaners when they need one now: after a renovation, before moving in, when the sofa needs a deep clean. Page One gets your cleaning business into those searches on Google, Google Maps and ChatGPT.",
        "searches": ["sofa cleaning Singapore", "post renovation cleaning HDB", "mattress cleaning near me", "part time cleaner Tampines", "carpet cleaning price"],
        "needs": [("A page per service", "Sofa, mattress, carpet, post-renovation, move-in: each service on its own page with clear prices or how you quote."),
                  ("Areas you cover", "The estates and areas you serve, so you show up for local searches across Singapore."),
                  ("Proof you're reliable", "Photos, what's included, and a WhatsApp button so customers can send a photo and get a quote.")],
        "proof": site_proof("https://sofacaresg.com/", "SofaCare SG", "a sofa, mattress and upholstery cleaning business"),
        "faqs": [("I clean islandwide. Can I still show up in local searches?", "Yes. We list the areas you cover and set up your Google Business Profile as a service-area business."),
                 ("Do I need a website, or is Carousell enough?", "Marketplace listings help, but Google and ChatGPT can't rank them like your own website. A website is yours and shows up when people search."),
                 ("What does it cost?", "S$20 a month on the Get Found plan (introductory price), with no setup fee and no contract.")],
    },
    {
        "slug": "aircon-servicing", "name": "Aircon servicing", "short": "aircon servicing company",
        "title": "SEO &amp; Website for Aircon Servicing in Singapore | Page One",
        "desc": "Aircon servicing, chemical wash and repair companies: get found on Google, Google Maps and ChatGPT when customers search. S$20/month, no contract.",
        "h1": "Get your aircon servicing company found on Google",
        "lead": "When an aircon stops cooling or starts leaking, people search and call the first company that looks trustworthy. Page One gets your aircon business into those searches on Google, Google Maps and ChatGPT.",
        "searches": ["aircon chemical wash Tampines", "aircon leaking water repair", "aircon servicing package HDB", "aircon not cold", "aircon gas top up price"],
        "needs": [("Pages for each job", "General servicing, chemical wash, chemical overhaul, gas top-up, repairs and installation: separate pages for separate searches."),
                  ("Your service areas", "The towns you cover named clearly, so you appear for searches like \"aircon servicing Bedok\"."),
                  ("Prices and trust", "Clear package prices or how you quote, photos of your team at work, and one-tap WhatsApp.")],
        "proof": "",
        "faqs": [("There are many aircon companies on Google. Can a small one still show up?", "Big companies compete for broad searches. Small companies can do well on specific ones, like a service plus a town, which also come from customers ready to book. That's what SEO Boosts focus on."),
                 ("Do you guarantee page one?", "No honest provider can guarantee rankings, because Google decides. We document the work in before/after reports."),
                 ("Can you handle Google Maps too?", "Yes. Setting up and improving your Google Business Profile is part of the Get Found plan.")],
    },
    {
        "slug": "renovation-contractor", "name": "Renovation contractors", "short": "renovation business",
        "title": "SEO &amp; Website for Renovation Contractors in Singapore",
        "desc": "Renovation, carpentry and home repair contractors: get found on Google, Maps and ChatGPT with a website that shows your work. S$20/month, no contract.",
        "h1": "Get your renovation business found on Google",
        "lead": "Homeowners spend weeks researching before they choose a contractor. They look at past projects, check reviews and compare. Page One gives your renovation business a website that shows your work and gets it found on Google, Google Maps and ChatGPT.",
        "searches": ["HDB bathroom renovation", "kitchen cabinet carpentry Singapore", "BTO renovation contractor", "toilet waterproofing repair", "small renovation works near me"],
        "needs": [("A portfolio that sells", "Project photos grouped by type (kitchen, bathroom, whole-home), each with a short description Google can read."),
                  ("Services and specialities", "What you do and don't do, the housing types you handle, and the areas you cover."),
                  ("Easy enquiries", "A WhatsApp button so homeowners can send floor plans and photos for a quote.")],
        "proof": "",
        "faqs": [("Can my project photos help with Google?", "Yes. Well-labelled photos can show up in Google Images and help Google and AI assistants understand the work you do."),
                 ("I get most jobs through referrals. Why do I need SEO?", "Referrals often check you online before calling. A clear website and Google Maps listing help them trust you, and SEO brings in people who don't know you yet."),
                 ("How much does it cost?", "S$20 a month on the Get Found plan (introductory price), including the website. No setup fee, no contract.")],
    },
    {
        "slug": "tuition-centre", "name": "Tuition centres", "short": "tuition centre",
        "title": "SEO &amp; Website for Tuition Centres in Singapore | Page One",
        "desc": "Tuition centres and private tutors: get found on Google, Google Maps and ChatGPT when parents search by subject, level and area. S$20/month.",
        "h1": "Get your tuition centre found by parents on Google",
        "lead": "Parents search by subject, level and area, and increasingly ask ChatGPT for recommendations. Page One gets your tuition centre into those searches with a website that answers parents' questions clearly.",
        "searches": ["PSLE maths tuition Bishan", "O level chemistry tuition", "small group tuition near me", "secondary English tuition Tampines", "JC economics tutor"],
        "needs": [("Pages by subject and level", "PSLE, O level, A level and IP: each subject and level gets a page that matches how parents search."),
                  ("Your location and timetable", "Address, nearby MRT, class times and class sizes: the details parents compare."),
                  ("Answers parents look for", "Teaching approach, tutor qualifications and fees, written clearly so AI assistants can quote them.")],
        "proof": "",
        "faqs": [("Can a small centre compete with big tuition brands online?", "Yes, on specific searches: a subject, a level and your area. Those searches come from parents nearby who are ready to sign up."),
                 ("Do you set up Google Maps for my centre?", "Yes. Your Google Business Profile is part of the Get Found plan."),
                 ("Can you help us show up in ChatGPT answers?", "We connect your site to Bing (which ChatGPT search uses), label your details with structured data and write content that answers parents' questions. No one can guarantee an AI will recommend you, but these steps make it possible.")],
    },
    {
        "slug": "plumber", "name": "Plumbers", "short": "plumbing business",
        "title": "SEO &amp; Website for Plumbers in Singapore | Page One",
        "desc": "Plumbers and plumbing contractors: get found on Google, Google Maps and ChatGPT when customers need help fast. S$20/month, website included.",
        "h1": "Get your plumbing business found when customers need you",
        "lead": "A leaking pipe or choked toilet can't wait, so people search and call fast. Page One makes sure your plumbing business shows up on Google, Google Maps and ChatGPT, with a phone and WhatsApp button one tap away.",
        "searches": ["plumber near me", "choked toilet Singapore", "water heater installation HDB", "kitchen sink leaking repair", "24 hour plumber Jurong"],
        "needs": [("Pages for urgent jobs", "Choked toilets, leaks, water heaters and pipe replacement: each gets a page that matches what people type in a hurry."),
                  ("Fast contact", "Call and WhatsApp buttons at the top of every page, working well on phones."),
                  ("Licences and areas", "Your licences, the areas you cover and your hours, so customers trust you before they call.")],
        "proof": "",
        "faqs": [("Most of my customers call in an emergency. Does SEO help?", "Yes. Emergency searches happen on phones, and people call the first trustworthy result. A fast mobile site and Google Maps listing put you there."),
                 ("Do you list my PUB licence?", "If you're a licensed plumber, we show your licence details clearly. It's a strong trust signal for customers."),
                 ("What does it cost?", "S$20 a month (introductory price), no setup fee and no contract.")],
    },
    {
        "slug": "pest-control", "name": "Pest control", "short": "pest control company",
        "title": "SEO &amp; Website for Pest Control in Singapore | Page One",
        "desc": "Pest control companies: get found on Google, Google Maps and ChatGPT when homes and businesses search for help. S$20/month, no contract.",
        "h1": "Get your pest control company found on Google",
        "lead": "Nobody plans to need pest control. When they do, they search for the specific pest and their area. Page One gets your company into those searches on Google, Google Maps and ChatGPT.",
        "searches": ["termite treatment HDB", "bed bug treatment Singapore", "cockroach control near me", "rat problem in house", "mosquito fogging service"],
        "needs": [("A page per pest", "Termites, bed bugs, cockroaches, rodents, mosquitoes: each has its own searches, so each gets its own page."),
                  ("Homes and businesses", "Clear pages for residential and commercial work, with how you inspect and treat."),
                  ("Trust signals", "Your NEA licence details, treatment guarantees you actually offer, and a WhatsApp button for photos.")],
        "proof": "",
        "faqs": [("Do I need a page for every type of pest?", "It helps. People search for the specific pest, so a page for each one gives Google a clear match."),
                 ("Can you help with commercial clients too?", "Yes. We can add pages aimed at businesses, such as F&B outlets and offices."),
                 ("How long until I see results?", "Your site is usually live within 7 days. Google results build over weeks to months, depending on competition.")],
    },
    {
        "slug": "beauty-salon", "name": "Beauty salons &amp; spas", "short": "beauty salon",
        "title": "SEO &amp; Website for Beauty Salons in Singapore | Page One",
        "desc": "Beauty salons, spas, nail and lash studios: get found on Google, Google Maps and ChatGPT by customers nearby. S$20/month, website included.",
        "h1": "Get your salon found by customers nearby",
        "lead": "Customers search by treatment and area, then check photos and reviews before they book. Page One gets your salon onto Google, Google Maps and ChatGPT, with a website that shows your work and makes booking easy.",
        "searches": ["facial near me", "eyelash extension Tampines", "gel manicure Bugis", "hair salon Bishan", "home based lash studio"],
        "needs": [("Treatments with prices", "Each treatment on its own page with prices and what's included, so customers can compare and book."),
                  ("Photos and reviews", "Your best work and your Google reviews, front and centre."),
                  ("One-tap booking", "A WhatsApp button or your booking link on every page.")],
        "proof": "",
        "faqs": [("I'm a home-based studio. Can I still show up on Google Maps?", "Yes. You can list the area you serve without showing your full address publicly. We set it up for you."),
                 ("Instagram works for me. Why a website?", "Instagram is great for showing your work, but Google and ChatGPT can't rank it like a website. A website catches the customers who search instead of scroll."),
                 ("What does it cost?", "S$20 a month (introductory price), website included, no setup fee and no contract.")],
    },
    {
        "slug": "property-agent", "name": "Property agents", "short": "property agent",
        "title": "Website &amp; SEO for Property Agents in Singapore | Page One",
        "desc": "Property agents: a personal website that gets found on Google and ChatGPT, built and managed for you. S$20/month. We run aliciaongproperty.com.",
        "h1": "A personal website for property agents, found on Google",
        "lead": "Sellers, buyers and landlords search for an agent who knows their estate and property type. A personal website helps you get found and remembered, beyond the portals. Page One builds and manages it for you.",
        "searches": ["property agent Punggol", "sell HDB 4 room", "condo rental agent", "HDB resale process", "how to choose a property agent"],
        "needs": [("Your speciality, clearly", "The estates, property types and services you focus on, written so Google and AI assistants can match you to them."),
                  ("Helpful guides", "Answers to common questions in your market, which build trust and bring in searches."),
                  ("Required details shown", "Your name, CEA registration number and agency details shown clearly, as agents' advertising in Singapore should.")],
        "proof": site_proof("https://aliciaongproperty.com/", "Alicia Ong Property", "a Singapore property agent"),
        "faqs": [("Do I still need my own website if I list on property portals?", "Portals bring listings to buyers. Your own website brings people to you: sellers looking for an agent, and anyone who searches your name."),
                 ("Will you include my CEA details?", "Yes. We show your name, registration number and agency details on the site, and keep the content factual."),
                 ("What does it cost?", "S$20 a month (introductory price), website included, no setup fee and no contract.")],
    },
]

# New-business pages: for someone opening one of these businesses. Extra keys: "new" (listed under "Opening a new
# business?" on the hub), "eyebrow", "opening" (what to set up before day one) and "cta". No proof section: we don't
# run a site in these industries yet, so none is claimed.
NEW_INDUSTRIES = [
    {
        "slug": "home-bakery", "name": "Home bakeries", "short": "home bakery", "new": True,
        "eyebrow": "Starting a home bakery?",
        "title": "Starting a Home Bakery? Website + Google SEO | Page One",
        "desc": "Starting a home bakery in Singapore? Get a website on your own domain, Google Maps and WhatsApp orders set up before your first bake. S$20/month, no setup fee.",
        "h1": "Starting a home bakery? Get found from your first bake",
        "lead": "Instagram gets you started, but people also search Google and ask ChatGPT for cakes, bakes and tarts near them. Page One sets up a simple website with your menu, how to order and a WhatsApp button, plus your Google listing, so new customers can find you from day one.",
        "searches": ["custom birthday cake Punggol", "home baker near me", "pineapple tarts order Singapore", "halal home bakery", "bento cake delivery"],
        "needs": [("Your menu, clearly", "What you bake, sizes, flavours and prices or how you quote, with photos. Each popular item can have its own page so Google can match it to searches."),
                  ("How to order", "Lead time, pickup area or delivery, payment and how far ahead to order, written once so you stop answering the same questions on chat."),
                  ("Orders by WhatsApp", "A one-tap WhatsApp button on every page, so a customer looking at a cake photo can message you straight away.")],
        "opening": [("Check the home-based business rules", "Read the current HDB or URA home-based business rules and SFA's guidance on home-based food businesses, and follow them. We don't give legal advice, but we can show the details customers should know, such as halal status, on your site."),
                    ("Pick your name and domain", "Choose a name you can keep, then register the matching domain in your name (usually S$15–30 a year). Use the same name on Instagram, Google and your website."),
                    ("Decide what you'll list first", "Start with your best-selling bakes and your order process. You can add more items as you go."),
                    ("Get on Google Maps", "A Google Business Profile can show your service area without showing your home address. We set it up with you.")],
        "faqs": [("I bake from home. Can I be on Google Maps without showing my address?", "Yes. Google lets you list the area you serve and hide your full address. We set it up that way for home-based businesses."),
                 ("Is Instagram not enough for a home bakery?", "Instagram is great for showing your bakes, but Google and ChatGPT can't rank it like a website. A website catches the customers who search instead of scroll, and it's yours."),
                 ("I haven't started selling yet. Is it too early?", "No. Setting up your website and Google listing before you launch means you're findable from your first order. It's usually live within 7 days."),
                 ("What does it cost?", "S$20 a month on the Get Found plan (introductory price), website included, no setup fee and no contract. Your domain is paid by you directly, usually S$15–30 a year.")],
        "cta": ("Starting a home bakery? Let's get you found.", "Tell Edwin on WhatsApp what you bake and where you deliver. No obligation."),
    },
    {
        "slug": "cafe", "name": "Cafes", "short": "cafe", "new": True,
        "eyebrow": "Opening a cafe?",
        "title": "Opening a Cafe in Singapore? Website + Google | Page One",
        "desc": "Opening a cafe in Singapore? Get your website, menu, opening hours and Google Maps listing ready before day one, so people nearby can find you. S$20/month.",
        "h1": "Opening a cafe? Be on Google before your first customer",
        "lead": "When a new cafe opens, people nearby search Google Maps and ask ChatGPT where to go for coffee, brunch or a quiet place to work. Page One gets your cafe onto Google, Google Maps and AI search with a simple website showing your menu, hours and location.",
        "searches": ["cafe near me", "brunch Tiong Bahru", "work friendly cafe Singapore", "new cafes Singapore", "halal cafe Bugis"],
        "needs": [("Menu and prices", "Your menu as real text, not just a photo, so Google and AI assistants can read it and match it to what people search for."),
                  ("Hours, location and how to get there", "Opening hours, nearest MRT, parking and whether you take reservations, the same on your website and your Google listing."),
                  ("Photos that make people come in", "Your space, your food and your coffee, labelled so Google Images and AI assistants understand them.")],
        "opening": [("Get your licence sorted first", "Food shops in Singapore need the right SFA licence before they open. Once that's in progress, you can get your website and Google listing ready in parallel."),
                    ("Claim your Google listing early", "Set up your Google Business Profile with your opening date, so people can find you from day one. We set it up with you."),
                    ("Register your domain", "Register your cafe's domain in your name (usually S$15–30 a year), and use the exact same name everywhere."),
                    ("Put your menu online", "Even a short opening menu helps. We can add seasonal items and new dishes later.")],
        "faqs": [("We open in a few weeks. When should we set up the website?", "Before you open. Your website is usually live within 7 days, and having your Google listing and website ready means people can find you as soon as you open your doors."),
                 ("Can you put our menu on the website?", "Yes. We put it on as real text with prices, so Google and AI assistants can read it, and we update it when you send changes on WhatsApp."),
                 ("Do we still need a website if we're on food delivery apps?", "Delivery apps list you alongside many competitors. Your own website and Google listing bring people to you directly, for dine-in, takeaway and events."),
                 ("What does it cost?", "S$20 a month on the Get Found plan (introductory price), website included, no setup fee and no contract.")],
        "cta": ("Opening a cafe? Let's get you on the map.", "Tell Edwin on WhatsApp where you're opening and when. No obligation."),
    },
    {
        "slug": "nail-lash-studio", "name": "Nail &amp; lash studios", "short": "nail or lash studio", "new": True,
        "eyebrow": "Opening a nail or lash studio?",
        "title": "Opening a Nail or Lash Studio? Website + SEO | Page One",
        "desc": "Opening a nail or lash studio in Singapore? Get a website with services, prices and WhatsApp booking, plus Google Maps, from day one. S$20/month, no contract.",
        "h1": "Opening a nail or lash studio? Get booked from Google",
        "lead": "New customers search by treatment and area, then look at photos and prices before they book. Page One gives your new studio a website with your services, prices and a booking button, and puts you on Google, Google Maps and ChatGPT from day one.",
        "searches": ["gel manicure Tampines", "eyelash extension near me", "lash lift price Singapore", "nail salon Jurong East", "home based lash studio"],
        "needs": [("Services with prices", "Each treatment, such as gel manicure, nail art, lash extensions or lash lift, with prices and how long it takes, so customers can choose before they message."),
                  ("Your work, front and centre", "Photos of your sets and designs, labelled so Google Images and AI assistants understand them."),
                  ("Easy booking", "A WhatsApp button or your booking link on every page, plus your hours and location or service area.")],
        "opening": [("Settle your name and domain", "Pick a studio name you can keep and register the matching domain in your name (usually S$15–30 a year)."),
                    ("Write your price list", "Start with your main treatments and prices. You can add promotions and new services later."),
                    ("Get on Google Maps", "A Google Business Profile with your hours and photos. Home-based? You can show your area without your full address."),
                    ("Collect your first reviews", "Ask your first customers to leave a Google review. It's one of the first things new customers look at.")],
        "faqs": [("I'm opening a home-based lash studio. Can I still show up on Google Maps?", "Yes. You can list the area you serve without showing your full address publicly. We set it up for you."),
                 ("Instagram works for me. Why a website?", "Instagram is great for showing your work, but Google and ChatGPT can't rank it like a website. A website catches the customers who search instead of scroll."),
                 ("Can I link my booking app?", "Yes. We can put your booking link next to the WhatsApp button on every page."),
                 ("What does it cost?", "S$20 a month (introductory price), website included, no setup fee and no contract.")],
        "cta": ("Opening a studio? Let's get you booked.", "Tell Edwin on WhatsApp what you offer and where. No obligation."),
    },
    {
        "slug": "fitness-studio", "name": "Fitness studios &amp; personal trainers", "short": "fitness studio or personal training business", "new": True,
        "eyebrow": "Opening a gym, studio or PT business?",
        "title": "New Fitness Studio or PT Business? Website + SEO | Page One",
        "desc": "Opening a fitness studio or starting as a personal trainer in Singapore? Get a website, Google Maps and WhatsApp enquiries set up from day one. S$20/month.",
        "h1": "Starting a fitness studio or PT business? Get found first",
        "lead": "People search for a trainer, a class or a studio near home or work, then compare what's offered and what it costs. Page One gives your new studio or personal training business a website that explains your classes and prices, and gets you onto Google, Google Maps and ChatGPT.",
        "searches": ["personal trainer Bishan", "pilates studio near me", "HIIT class Singapore", "personal trainer for beginners", "boxing class Tanjong Pagar"],
        "needs": [("Classes and sessions explained", "Each class type or training package on its own page, with who it's for, how long it is and the price or how you quote."),
                  ("Your trainers and qualifications", "Who teaches, their experience and certifications, written clearly so customers and AI assistants can trust them."),
                  ("Easy trial booking", "A WhatsApp button for trial sessions and questions, plus your timetable, location or the areas you train in.")],
        "opening": [("Decide what you'll offer first", "Your main classes or packages and prices. Keep it simple at launch and add more as you grow."),
                    ("Register your domain", "Register your studio or trainer name as a domain in your name (usually S$15–30 a year)."),
                    ("Get on Google Maps", "A Google Business Profile for your studio. Mobile personal trainer? You can list the areas you cover instead of an address."),
                    ("Have your certifications ready", "List the qualifications you actually hold. Customers check, and it helps them choose you.")],
        "faqs": [("I'm a freelance personal trainer without a studio. Do I need a website?", "It helps. People search for a trainer by area and goal, and a website with your approach, packages and qualifications gives them a reason to message you. Google lets you list the areas you cover without a fixed address."),
                 ("Can you show our class timetable?", "Yes. We can add your timetable and update it when you send changes on WhatsApp."),
                 ("We're opening soon. Is it too early?", "No. Your website is usually live within 7 days, and being on Google before you open means people can find you from day one."),
                 ("What does it cost?", "S$20 a month (introductory price), website included, no setup fee and no contract.")],
        "cta": ("Starting out in fitness? Let's get you found.", "Tell Edwin on WhatsApp what you offer and where. No obligation."),
    },
]
INDUSTRIES = INDUSTRIES + NEW_INDUSTRIES

_checker_src = open(os.path.join(HERE, "home_body.html"), encoding="utf-8").read()
CHECKER_SECTION = _checker_src[_checker_src.index("<!-- WEBSITE CHECKER -->"):_checker_src.index("<!-- CLIENT STORIES -->")]


def industry_page(ind):
    url = f"/industries/{ind['slug']}/"
    searches = "".join(f"<li>{s}</li>" for s in ind["searches"])
    needs = "".join(f'<div class="card reveal"><h3>{h}</h3><p>{p}</p></div>' for h, p in ind["needs"])
    faq_html = "".join(f"        <details><summary>{q}</summary><p>{a}</p></details>\n" for q, a in ind["faqs"])
    others = " · ".join(f'<a class="link" href="/industries/{o["slug"]}/">{o["name"]}</a>' for o in INDUSTRIES if o["slug"] != ind["slug"])
    proof = f"""
    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Proof</p>
        <h2 class="reveal">The same system, running on a real {ind['short']}</h2>
        {ind.get("proof", "")}
      </div>
    </section>
""" if ind.get("proof") else ""
    opening = "".join(f'<li><b>{h}.</b> {p}</li>' for h, p in ind.get("opening", []))
    opening = f"""
    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Before you open</p>
        <h2 class="reveal">Opening a {ind['short']}: what to set up first</h2>
        <ul class="ticks reveal">{opening}</ul>
        <p class="note reveal">We do the website, Google Maps, Google and Bing setup for you. <a class="link" href="/new-business-website/">See the full new business launch checklist →</a></p>
      </div>
    </section>
""" if opening else ""
    cta_title, cta_text = ind.get("cta", (f"Get your {ind['short']} found", "Check your website free, or chat with Edwin on WhatsApp. No obligation."))
    body = hero(f'<a href="/industries/">Industries</a> / {ind["name"]}', ind.get("eyebrow", ind["name"] + " in Singapore"), ind["h1"], ind["lead"],
                '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · website + SEO · no setup fee</p>') + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">How customers find a {ind['short']}</p>
        <h2 class="reveal">They search for the job, and the area</h2>
        <p class="section-lead reveal">Example searches people type into Google or ask ChatGPT (examples only):</p>
        <ul class="ticks reveal">{searches}</ul>
        <p class="section-lead reveal">If your website doesn't use the words customers use, Google and AI assistants can't match you to them. That's what we fix.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">What we set up</p>
        <h2 class="reveal">What a {ind['short']} website needs to get found</h2>
        <div class="cards three" style="margin-top:32px">{needs}</div>
        <p class="note reveal">Plus everything in the Get Found plan: Google Business Profile, Google and Bing connected, structured data for AI search, hosting, security and a monthly technical audit. <a class="link" href="/get-found/">See what's included →</a></p>
      </div>
    </section>
{proof}{opening}
    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">{ind['name']}: your questions, answered</h2>
        <div style="margin-top:24px">
{faq_html}        </div>
        <p class="note reveal">Other industries: {others}</p>
      </div>
    </section>

""" + cta(cta_title, cta_text)
    page(f"industries/{ind['slug']}/index.html", ind["title"], ind["desc"],
         [service(f"Website and SEO for {ind['name'].replace('&amp;', '&').lower()} in Singapore", url, ind["desc"], "20"),
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in ind["faqs"]]}],
         body, crumb=ind["name"], crumb_parent=("Industries", "/industries/"), updated="2026-10-13" if ind.get("new") else None)


for _ind in INDUSTRIES:
    industry_page(_ind)

def _ind_card(i):
    return f'<div class="card reveal"><h3><a href="/industries/{i["slug"]}/">{i["name"]}</a></h3><p>{i["desc"]}</p><a class="card-link" href="/industries/{i["slug"]}/">See how it works →</a></div>'


_new_cards = "".join(_ind_card(i) for i in INDUSTRIES if i.get("new"))
_ind_cards = "".join(_ind_card(i) for i in INDUSTRIES if not i.get("new"))
page("industries/index.html",
     "SEO &amp; Websites by Industry in Singapore | Page One",
     "How Page One gets Singapore small businesses found on Google, Maps and ChatGPT, by industry: new bakeries, cafes and studios, workshops, cleaning and more.",
     [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
         {"@type": "ListItem", "position": n + 1, "url": f"{SITE}/industries/{i['slug']}/", "name": i["name"].replace("&amp;", "&")}
         for n, i in enumerate(INDUSTRIES)]}],
     hero("Industries", "Who we help", "Get found on Google, whatever you do",
          "Page One builds and looks after websites that get Singapore small businesses found on Google, Google Maps and ChatGPT, whatever the trade, for S$20 a month. Customers search differently for a plumber than for a tuition centre, so pick your industry to see what people search for, what your website needs, and the results we've had where we have them.") + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Opening a new business?</p>
        <h2 class="reveal">Get found from day one</h2>
        <p class="section-lead reveal">What to set up before you open, and what your first website needs. <a class="link" href="/new-business-website/">See the new business launch checklist →</a></p>
        <div class="cards three" style="margin-top:32px">{_new_cards}</div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Established trades</p>
        <h2 class="reveal">Industries we help</h2>
        <div class="cards three" style="margin-top:32px">{_ind_cards}</div>
        <p class="note reveal">Don't see your industry? The same system works for most local businesses. <a class="link" href="{WA_LINK}" target="_blank" rel="noopener">Ask Edwin on WhatsApp →</a></p>
      </div>
    </section>

""" + cta(),
     crumb="Industries", updated=AIV_UPDATED)

# ---------- Free website check (landing page for the checker) ----------
FREE_CHECK_FAQ = [
    ("Is the website check really free?", "Yes. No sign-up, no email needed. Enter your website address and you get your score and the list of fixes on screen in under a minute."),
    ("What does the check look at?", "Google basics (title, description, headings, indexing, sitemap), mobile setup, security (HTTPS), your business details for Google Maps, structured data, whether AI assistants like ChatGPT can read your site, and page speed."),
    ("What should I do with the results?", "Each item is explained in plain English with why it matters. You can fix them yourself, or ask Edwin on WhatsApp and he'll tell you honestly what's worth fixing first."),
    ("Can I check a competitor's website?", "Yes. The check only reads what's publicly visible, so you can compare your site with anyone's."),
]
_fc_faq = "".join(f"        <details><summary>{q}</summary><p>{a}</p></details>\n" for q, a in FREE_CHECK_FAQ)
page("free-website-check/index.html",
     "Free Website &amp; SEO Check for Singapore Businesses | Page One",
     "Free SEO check for your website: Google basics, mobile, speed and ChatGPT readiness, with a score out of 100 and plain-English fixes. No sign-up, under a minute.",
     [{"@context": "https://schema.org", "@type": "WebApplication", "name": "Page One free website check", "url": SITE + "/free-website-check/",
       "applicationCategory": "BusinessApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SGD"},
       "provider": PROVIDER, "description": "Checks a website's Google basics, mobile setup, speed and AI-search readiness and explains each fix in plain English."},
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FREE_CHECK_FAQ]}],
     hero("Free website check", "Free · no sign-up · under a minute", "Free website and SEO check",
          "Type your website address below. It's the same check we run before we work on any client's website.", buttons=False) + "\n" + CHECKER_SECTION + f"""
    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">About the free check</h2>
        <div style="margin-top:24px">
{_fc_faq}        </div>
        <p class="note reveal">Want to see what a full report looks like? <a class="link" href="/report.html">Open the sample report →</a></p>
      </div>
    </section>

""" + cta("Want it fixed for you?", "Get Found takes care of it for S$20 a month: website or landing page, Google, Maps and AI search, managed every month."),
     crumb="Free website check")

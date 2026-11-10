"""Page content for the AutoSEO.my site.

Text marked COPY is the client's own wording and is kept word for word.
Everything else is plain, general guidance: no client names, no figures,
no prices. Brand facts (name, WhatsApp, prefills) live in brand.json.
"""

# ---------------------------------------------------------------- COPY
ABOUT_PARAS = [  # COPY
    "AutoSEO.my is a specialised digital marketing agency dedicated exclusively to helping automotive businesses across Malaysia build stronger brands, improve online visibility and generate more customer enquiries.",
    "Unlike general digital marketing agencies, we focus entirely on the automotive industry.",
    "We combine Search Engine Optimisation (SEO), Answer Engine Optimisation (AEO) and Generative Engine Optimisation (GEO) to help automotive businesses get discovered through Google Search, Google Maps and AI-powered search platforms such as ChatGPT, Gemini and Perplexity.",
]
GOAL = "Our goal is simple: Make your automotive business easier to find, easier to trust and easier to choose."  # COPY
MISSION = "To become Malaysia's most trusted automotive digital marketing specialist by helping automotive businesses strengthen their online presence, build lasting brand authority and attract more customers."  # COPY

HERO_H1 = "Is Your Automotive Business Visible on Google and AI Search?"  # COPY
HERO_LINES = [  # COPY
    "Your next customer could already be searching for your services.",
    "Let AutoSEO.my help them find you.",
]
BTN_AUDIT = "Get a Free Automotive SEO Audit"  # COPY
BTN_SPECIALIST = "WhatsApp Our SEO Specialists"  # COPY

WHY = [  # COPY
    ("100% Automotive Industry Specialisation", "We understand how motorists search for workshops, dealerships, tyres, repairs and automotive services.", "🔧"),
    ("Built for the Malaysian Market", "Our strategies target local customer demand across Kuala Lumpur, Selangor, Johor Bahru, Penang and other Malaysian locations.", "📍"),
    ("SEO + AEO + GEO Expertise", "We help automotive businesses compete in traditional Google search and prepare for the growing importance of AI-powered discovery.", "🔍"),
    ("Focused on Real Business Growth", "Our priority is not just traffic and keyword rankings. We focus on qualified enquiries, WhatsApp leads, calls and customer conversions.", "📈"),
]

# ---------------------------------------------------------------- SERVICES
# number, slug, card title (COPY), short name, card text (COPY), emoji, page details
SERVICES = [
    {
        "n": 1, "slug": "automotive-seo", "emoji": "🔍",
        "title": "Automotive SEO — Rank Higher on Google",
        "short": "Automotive SEO",
        "text": "Improve organic search visibility for relevant automotive services and location-based keywords that potential customers are searching for.",
        "h1": "Automotive SEO in Malaysia: rank higher on Google",
        "meta": "Automotive SEO for Malaysian workshops, dealers, tyre shops and parts suppliers: service and location pages that match what motorists search on Google.",
        "why": "Most motorists start with a search like “car service near me” or “tyre shop Shah Alam”. If your website doesn’t have a clear page for that service in that area, Google has nothing of yours to show. Automotive SEO gives each service and each area you cover a page that answers the search properly.",
        "covers": [
            "Keyword research on the services and areas your customers actually search for, in English and Bahasa Malaysia",
            "One clear page for each main service, with the details a motorist needs before they call",
            "Location pages for the areas you really serve, such as Petaling Jaya, Shah Alam, Johor Bahru or George Town",
            "Technical checks: page speed, mobile layout, titles, headings, broken links and indexing",
            "Structured data (schema) so Google understands your business, services and FAQs",
            "Regular review of what is working in Google Search Console, and changes based on it",
        ],
        "searches": ["car service near me", "bengkel kereta Shah Alam", "gearbox repair Kuala Lumpur", "brake pad replacement Johor Bahru", "car workshop Penang"],
        "faqs": [
            ("How long does automotive SEO take to work?", "SEO builds over months, not days. Technical fixes and new service pages can be picked up by Google within weeks, while stronger rankings for competitive searches usually take longer. We don’t promise specific rankings or dates, because Google decides those."),
            ("Do you target Bahasa Malaysia searches too?", "Yes, where your customers use them. Many motorists search in a mix of English and Bahasa Malaysia, such as “bengkel kereta” or “kedai tayar”, so we check both when we plan your pages."),
            ("Do I need a new website for SEO?", "Not always. If your current website is sound, we improve it. If it is slow, hard to use on a phone or hard to edit, we may suggest a rebuild. We’ll explain which after the free audit."),
        ],
    },
    {
        "n": 2, "slug": "aeo-answer-engine-optimisation", "emoji": "💬",
        "title": "AEO — Get Discovered Through Answer Engines",
        "short": "AEO (Answer Engine Optimisation)",
        "text": "Structure automotive content to improve its eligibility for Google featured snippets, AI-generated answers and conversational search.",
        "h1": "AEO for automotive businesses: be the answer people see",
        "meta": "Answer Engine Optimisation for Malaysian automotive businesses: clear answers to motorists’ questions, structured for featured snippets and AI answers.",
        "why": "More searches now end with an answer rather than a list of links: a featured snippet, an AI overview or a voice reply. Motorists ask things like “how often should I change my gearbox oil?” or “why is my car aircon not cold?”. AEO makes sure your business has a clear, accurate answer ready, so you can be the source those answers draw on.",
        "covers": [
            "A list of the real questions your customers ask, before and after they visit",
            "Short, direct answers at the top of each page, followed by the detail",
            "FAQ sections on service pages, marked up with FAQ schema",
            "Plain headings that match how people phrase their questions",
            "Facts kept consistent across your website and Google Business Profile",
        ],
        "searches": ["how often to service a car in Malaysia", "why is my car aircon not cold", "when to change tyres", "what does a car battery cost", "is my gearbox slipping"],
        "faqs": [
            ("What is the difference between SEO and AEO?", "SEO helps your pages rank in the list of search results. AEO shapes your content so search engines and AI tools can lift a clear answer from it, for featured snippets, AI overviews and voice search. They work best together."),
            ("Will AEO get my business into Google’s AI answers?", "Nobody can guarantee that, because Google and AI tools choose their own sources. AEO improves your eligibility by giving them clear, well-structured and accurate answers to use."),
            ("Do I have to write the answers myself?", "No. We draft them from what you tell us about your services and how you work, and you check them for accuracy before they go live."),
        ],
    },
    {
        "n": 3, "slug": "geo-ai-search-visibility", "emoji": "🤖",
        "title": "GEO — Build Visibility in AI Search",
        "short": "GEO (Generative Engine Optimisation)",
        "text": "Strengthen your brand's discoverability and authority across AI-powered search experiences, including ChatGPT, Google Gemini and Perplexity.",
        "h1": "GEO in Malaysia: get your automotive business into AI search",
        "meta": "Generative Engine Optimisation for automotive businesses in Malaysia: help ChatGPT, Google Gemini and Perplexity find, understand and mention your brand.",
        "why": "Some motorists now ask ChatGPT, Gemini or Perplexity to recommend a workshop or explain a repair before they ever open Google. These tools build their answers from what they can read and trust about you online. GEO makes your business facts clear, consistent and easy for AI tools to find.",
        "covers": [
            "Clear business facts on your website: what you do, where, and for which vehicles",
            "The same name, contact link and areas everywhere your business appears online",
            "An llms.txt file and clean structured data that AI tools can read",
            "Search engine setup on Google and Bing, which several AI tools draw on",
            "Helpful guides and FAQs that give AI tools something accurate to quote",
            "Checks on how AI tools currently describe your business",
        ],
        "searches": ["best tyre shop in Johor Bahru", "recommend a car aircon specialist in Penang", "EV service centre Kuala Lumpur", "where to buy car parts in Selangor"],
        "faqs": [
            ("What is GEO?", "Generative Engine Optimisation is the work of making your business easy for AI tools such as ChatGPT, Google Gemini and Perplexity to find, understand and mention when people ask them for recommendations or advice."),
            ("Can you guarantee ChatGPT will recommend my business?", "No. AI tools decide their own answers and they change over time. What we can do is make sure accurate, consistent information about your business is out there for them to use."),
            ("Does GEO replace SEO?", "No. AI tools often rely on the same pages and signals that search engines use, so good SEO is the base that GEO builds on."),
        ],
    },
    {
        "n": 4, "slug": "automotive-website-design", "emoji": "🖥️",
        "title": "Automotive Website Design & Development",
        "short": "Automotive Website Design & Development",
        "text": "Create professional, mobile-friendly, SEO-ready websites designed to turn visitors into WhatsApp enquiries, phone calls and confirmed bookings.",
        "h1": "Automotive website design in Malaysia, built to bring enquiries",
        "meta": "Mobile-friendly, SEO-ready websites for Malaysian workshops, dealers and automotive suppliers, designed to turn visitors into WhatsApp enquiries and bookings.",
        "why": "Most of your visitors will be on a phone, often standing next to a car that needs attention. They want to see quickly what you fix, where you are and how to reach you. A good automotive website loads fast, answers those questions on the first screen and puts a WhatsApp button within thumb’s reach.",
        "covers": [
            "Mobile-first design that loads quickly on Malaysian mobile networks",
            "A page for each service, with the questions customers usually ask",
            "WhatsApp buttons with a ready-written message, so enquiries arrive with context",
            "SEO built in from the start: titles, headings, schema and a clean sitemap",
            "Real photos of your premises and work, where you can provide them",
            "A site you own, on your own domain",
        ],
        "searches": ["car workshop website", "website for car dealer Malaysia", "tyre shop website design"],
        "faqs": [
            ("How much does a website cost?", "It depends on the number of pages and what you need. WhatsApp us for a quote after we understand your business."),
            ("Can you improve my existing website instead?", "Yes. If your current site is in good shape, we can fix its speed, layout and SEO rather than rebuild it."),
            ("Will the website be mine?", "Yes. The website is built for your business on your own domain."),
        ],
    },
    {
        "n": 5, "slug": "google-maps-local-seo", "emoji": "📍",
        "title": "Google Maps & Local SEO",
        "short": "Google Maps & Local SEO",
        "text": "Optimise Google Business Profiles to improve local discoverability, strengthen customer trust and attract nearby motorists.",
        "h1": "Google Maps and local SEO for automotive businesses in Malaysia",
        "meta": "Google Business Profile and local SEO for Malaysian workshops, tyre shops, detailers and dealers: be easier to find on Google Maps when nearby motorists search.",
        "why": "When a motorist searches “tyre shop near me”, Google usually shows a map with a handful of businesses before any website. Your Google Business Profile decides whether you appear there and whether people trust you enough to tap. Local SEO keeps that profile complete, accurate and active.",
        "covers": [
            "A complete Google Business Profile: the right categories, services, hours and service areas",
            "Your business name and details kept the same on your profile, website and directories",
            "Regular profile posts and photos that show your real work",
            "A simple routine for asking happy customers for Google reviews, and replying to reviews",
            "Location pages on your website that support your Maps listing",
        ],
        "searches": ["tyre shop near me", "car wash near me", "workshop open Sunday Petaling Jaya", "car battery replacement near me"],
        "faqs": [
            ("Why doesn’t my business show on Google Maps?", "Common reasons are an unverified or incomplete profile, the wrong main category, or details that don’t match your website. The free audit checks these first."),
            ("Can you get us more Google reviews?", "We set up an easy, honest way to ask your real customers for reviews. We never buy reviews or write fake ones, as that breaks Google’s rules and can get a profile suspended."),
            ("Do I need a shop address to appear on Maps?", "No. Mobile services can use a service-area profile that lists the areas they cover instead of a public address."),
        ],
    },
    {
        "n": 6, "slug": "automotive-content-marketing", "emoji": "📝",
        "title": "Automotive Content & Brand Awareness",
        "short": "Automotive Content & Brand Awareness",
        "text": "Develop industry-specific articles, service guides, FAQs and digital content that build brand credibility and attract relevant search traffic.",
        "h1": "Automotive content that builds trust and brings search traffic",
        "meta": "Articles, service guides and FAQs for Malaysian automotive businesses, written for motorists, to build brand credibility and attract relevant search traffic.",
        "why": "Motorists research before they spend money on their car. Helpful articles and service guides answer their questions, show that you know your trade and bring in people searching for specific problems. Over time they also give search engines and AI tools more reasons to trust your brand.",
        "covers": [
            "Articles on the questions your customers ask, in plain Malaysian English",
            "Service guides that explain a repair or product, what affects the job and what to expect",
            "FAQs for each service page",
            "Content planned around searches in the areas you serve",
            "Facts checked with you before anything is published",
        ],
        "searches": ["signs your car battery is dying", "how long do tyres last in Malaysia", "car coating vs wax", "hybrid battery replacement"],
        "faqs": [
            ("Who writes the content?", "We draft it based on your services and expertise, and you approve anything that states facts about your business before it goes live."),
            ("How often should we publish?", "Regular, useful content does better than bursts. We agree a pace that suits your business when we plan the work."),
            ("Will you copy content from other websites?", "No. Copied content doesn’t help with Google or AI search. Everything is written for your business."),
        ],
    },
]

# ---------------------------------------------------------------- INDUSTRIES
# label (COPY), slug, "a ..." phrase for prefills, page details
INDUSTRIES = [
    {
        "label": "Car workshops and automotive service centres", "slug": "car-workshops", "short": "Car workshops", "emoji": "🔧",
        "who": "a car workshop",
        "h1": "SEO for car workshops and service centres in Malaysia",
        "meta": "SEO, Google Maps and AI search visibility for car workshops and automotive service centres in Kuala Lumpur, Selangor, Johor Bahru and Penang.",
        "intro": "Motorists usually look for a workshop when something has already gone wrong, so they search fast and choose fast. They want a workshop that is close, open and clearly fixes their problem. The workshops that show up with clear service pages and a strong Google Maps listing are the ones that get the call.",
        "focus": [
            "A page for each main job you do, such as servicing, brakes, gearbox, suspension or engine repair",
            "Car makes you specialise in, if you do, so the right owners find you",
            "A strong Google Business Profile with your real hours and services",
            "Area pages for the neighbourhoods you actually serve",
            "A WhatsApp button so customers can send photos or describe the problem straight away",
        ],
        "searches": ["car workshop near me", "bengkel kereta Klang", "car service Subang Jaya", "gearbox specialist Johor Bahru"],
    },
    {
        "label": "New and used car dealerships", "slug": "car-dealerships", "short": "Car dealerships", "emoji": "🚗",
        "who": "a car dealership",
        "h1": "SEO for new and used car dealerships in Malaysia",
        "meta": "Help car buyers find your new or used car dealership on Google, Google Maps and AI search, with clear pages and WhatsApp enquiries.",
        "intro": "Car buyers compare a lot before they visit a showroom. They search by brand, model, budget and location, and many ask AI tools for advice too. A dealership that answers those questions clearly online is easier to shortlist.",
        "focus": [
            "Pages for the brands and models you sell, with the information buyers look for",
            "Location pages for each showroom or branch",
            "Helpful guides on buying, trading in and owning a car",
            "Google Business Profiles kept accurate for every outlet",
            "WhatsApp enquiry buttons with the model already named in the message",
        ],
        "searches": ["used car dealer Kuala Lumpur", "recond car Shah Alam", "car showroom Johor Bahru", "trade in my car Penang"],
    },
    {
        "label": "Tyre shops and tyre distributors", "slug": "tyre-shops", "short": "Tyre shops", "emoji": "🛞",
        "who": "a tyre shop",
        "h1": "SEO for tyre shops and tyre distributors in Malaysia",
        "meta": "Help motorists and trade buyers find your tyre shop or tyre distribution business on Google, Google Maps and AI search across Malaysia.",
        "intro": "Tyre searches are often very local and very specific: a tyre size, a brand, or a puncture that needs fixing now. Distributors also need to be found by workshops and fleets looking for supply. Clear pages and a well-kept Maps listing help both kinds of customer.",
        "focus": [
            "Pages for the tyre brands and services you offer, such as alignment, balancing and puncture repair",
            "Google Maps visibility for “tyre shop near me” searches",
            "Trade pages for workshops and fleets if you distribute",
            "Answers to common tyre questions: sizes, wear, age and pressure",
            "WhatsApp enquiries that include the customer’s tyre size",
        ],
        "searches": ["tyre shop near me", "kedai tayar Johor Bahru", "wheel alignment Petaling Jaya", "tyre distributor Malaysia"],
    },
    {
        "label": "Car accessories and aftermarket retailers", "slug": "car-accessories", "short": "Car accessories", "emoji": "🎛️",
        "who": "a car accessories business",
        "h1": "SEO for car accessories and aftermarket retailers in Malaysia",
        "meta": "Help motorists find your car accessories or aftermarket shop on Google and AI search, with clear product and fitting pages for Malaysian buyers.",
        "intro": "Accessory buyers search by product and by car model, such as dashcams, head units, body kits or tint for a specific car. Pages that match those searches, and show what you fit and where, turn browsing into enquiries.",
        "focus": [
            "Category pages for the products you sell and fit",
            "Car model pages where you have popular fitments",
            "Guides that help buyers choose between options",
            "Google Maps visibility for your fitting outlets",
            "WhatsApp enquiries with the product and car model filled in",
        ],
        "searches": ["dashcam installation Kuala Lumpur", "android player car Selangor", "car tint Johor Bahru", "bodykit shop Penang"],
    },
    {
        "label": "Car air-conditioning specialists", "slug": "car-aircon-specialists", "short": "Car aircon specialists", "emoji": "❄️",
        "who": "a car air-conditioning business",
        "h1": "SEO for car air-conditioning specialists in Malaysia",
        "meta": "Help motorists with a warm car aircon find your specialist workshop on Google, Google Maps and AI search in Kuala Lumpur, Selangor, Johor Bahru and Penang.",
        "intro": "In Malaysian heat, a car aircon that stops blowing cold is urgent. Owners search for the symptom as often as the service. A specialist that explains common aircon problems and shows up on Maps nearby is well placed to get the job.",
        "focus": [
            "Pages for gas top-ups, compressor, cooling coil, blower and servicing work",
            "Symptom guides, such as “aircon not cold” or “aircon smells”",
            "Google Business Profile with aircon services listed",
            "Area pages for the places you serve",
            "WhatsApp enquiries so customers can describe the problem first",
        ],
        "searches": ["car aircon not cold", "car aircon service Shah Alam", "aircon kereta Johor Bahru", "compressor replacement Penang"],
    },
    {
        "label": "Car detailing, polishing and coating centres", "slug": "car-detailing", "short": "Car detailing and coating", "emoji": "✨",
        "who": "a car detailing centre",
        "h1": "SEO for car detailing, polishing and coating centres in Malaysia",
        "meta": "Help car owners find your detailing, polishing or coating centre on Google, Google Maps and AI search, with clear service pages and WhatsApp bookings.",
        "intro": "Detailing customers compare options and want to see the result before they book. They search for a service and an area, then look at photos and reviews. Clear service pages, real photos and a strong Maps profile make it easier to choose you.",
        "focus": [
            "Pages for each service, such as interior cleaning, polishing, ceramic coating and paint protection film",
            "Guides that explain the differences between treatments",
            "Photos of your own work on your website and Google profile",
            "A steady flow of genuine Google reviews",
            "WhatsApp booking messages with the car model included",
        ],
        "searches": ["ceramic coating Kuala Lumpur", "car polish near me", "interior cleaning Petaling Jaya", "PPF Johor Bahru"],
    },
    {
        "label": "EV and hybrid vehicle specialists", "slug": "ev-hybrid-specialists", "short": "EV and hybrid specialists", "emoji": "🔋",
        "who": "an EV and hybrid specialist",
        "h1": "SEO for EV and hybrid vehicle specialists in Malaysia",
        "meta": "Help EV and hybrid owners in Malaysia find your specialist service on Google and AI search, with clear pages on the systems you work on.",
        "intro": "EV and hybrid owners often can’t use any workshop, so they search hard for someone who knows their car. Many also ask AI tools for advice first. Clear pages about the systems and models you handle help these owners find and trust you.",
        "focus": [
            "Pages for hybrid battery, EV servicing and diagnostic work you offer",
            "Model and brand pages where you have real experience",
            "Plain guides that answer common EV and hybrid questions",
            "Clear business facts that AI tools can read and repeat",
            "WhatsApp enquiries with the model and symptom included",
        ],
        "searches": ["hybrid battery replacement Kuala Lumpur", "EV service centre Selangor", "hybrid specialist Penang", "EV workshop Johor Bahru"],
    },
    {
        "label": "Car battery and spare parts suppliers", "slug": "battery-spare-parts", "short": "Batteries and spare parts", "emoji": "⚙️",
        "who": "a car battery and spare parts business",
        "h1": "SEO for car battery and spare parts suppliers in Malaysia",
        "meta": "Help motorists and workshops find your car battery or spare parts business on Google, Google Maps and AI search across Malaysia.",
        "intro": "Battery and parts searches are often urgent or very specific: a car that won’t start, or a part number for a particular model. Pages organised by car model and part, plus a reliable Maps listing, help buyers find you when they need you.",
        "focus": [
            "Pages for battery types and the car models they fit",
            "Parts categories organised the way buyers search",
            "Trade pages for workshops if you supply them",
            "Google Maps visibility for “car battery near me” searches",
            "WhatsApp enquiries that include the car model and part needed",
        ],
        "searches": ["car battery near me", "bateri kereta Johor Bahru", "spare parts Kuala Lumpur", "car battery delivery Selangor"],
    },
    {
        "label": "Automotive equipment and diagnostic tool distributors", "slug": "equipment-diagnostic-tools", "short": "Equipment and diagnostic tools", "emoji": "🧰",
        "who": "an automotive equipment distributor",
        "h1": "SEO for automotive equipment and diagnostic tool distributors in Malaysia",
        "meta": "Help workshops and trade buyers find your automotive equipment or diagnostic tool business on Google and AI search across Malaysia.",
        "intro": "Your customers are workshop owners and technicians who research carefully before buying equipment. They search by tool type, brand and function, and often ask AI tools to compare options. Clear product and category pages help you get on their shortlist.",
        "focus": [
            "Category and product pages written for workshop buyers",
            "Comparison guides between tool types and uses",
            "Support and training information that builds trust",
            "Clear company facts for AI tools and B2B searches",
            "WhatsApp enquiries that name the product the buyer is looking at",
        ],
        "searches": ["car diagnostic tool Malaysia", "car lift supplier Selangor", "workshop equipment Kuala Lumpur", "scan tool distributor Malaysia"],
    },
]
OTHER_INDUSTRY = "Other automotive-related businesses"  # COPY

# ---------------------------------------------------------------- FAQ (site-wide)
FAQS = [
    ("What does AutoSEO.my do?", "AutoSEO.my helps automotive businesses in Malaysia get found online. We combine SEO, AEO and GEO so workshops, dealers, tyre shops and other automotive businesses are easier to find on Google Search, Google Maps and AI tools such as ChatGPT, Gemini and Perplexity, and easier to contact on WhatsApp."),
    ("Who do you work with?", "Only automotive businesses: car workshops and service centres, dealerships, tyre shops, accessory retailers, car aircon specialists, detailing centres, EV and hybrid specialists, battery and parts suppliers, equipment distributors and other automotive-related businesses."),
    ("Which areas do you cover?", "We work with businesses across Malaysia, including Kuala Lumpur, Selangor, Johor Bahru and Penang. Strategies are built around the areas where your customers are."),
    ("How much does it cost?", "It depends on your business and what you need. WhatsApp us for a quote after a free automotive SEO audit."),
    ("What is the free automotive SEO audit?", "We look at how your business appears today on Google Search, Google Maps and AI search, and at your website if you have one, then tell you in plain language what to fix first. Ask for it on WhatsApp."),
    ("What are SEO, AEO and GEO?", "SEO helps your pages rank on Google. AEO shapes your content into clear answers for featured snippets and AI answers. GEO helps AI tools such as ChatGPT, Gemini and Perplexity find and mention your business. Together they cover how motorists search today."),
    ("Can you guarantee first place on Google?", "No. Nobody can honestly guarantee rankings, because Google and AI tools decide their own results. We focus on the work that improves your chances, and on what matters most: qualified enquiries, WhatsApp leads and calls."),
    ("How do I get started?", "Send us a WhatsApp message. Tell us your business name, what you do and where, and we’ll arrange your free automotive SEO audit."),
]
HOME_FAQ_COUNT = 4

# ---------------------------------------------------------------- HOW IT WORKS
STEPS = [
    ("Step 1", "Free automotive SEO audit", "Send us a WhatsApp message with your business name and location. We check how you appear on Google Search, Google Maps and AI search today, and what is holding you back.", [
        "Your Google Business Profile and Maps listing",
        "Your website, if you have one: speed, mobile layout and pages",
        "How you show up for the searches your customers use",
        "What AI tools can find about your business",
    ]),
    ("Step 2", "A plan for your business", "We explain what we found in plain language and suggest what to fix first. The plan is built around your services, your areas and the customers you want more of.", [
        "Priorities, most important first",
        "Which services and areas to focus on",
        "A quote on WhatsApp, with no obligation",
    ]),
    ("Step 3", "We do the work", "We carry out the agreed work across SEO, AEO and GEO, from your website and Google profile to content that answers your customers’ questions.", [
        "Website and page improvements",
        "Google Maps and local SEO",
        "Content, FAQs and structured data",
    ]),
    ("Step 4", "Review and improve", "We look at what is bringing in enquiries and keep improving it. The focus stays on qualified enquiries, WhatsApp leads, calls and customers, not just traffic.", [
        "What people search to find you",
        "Which pages bring enquiries",
        "Next improvements, agreed with you",
    ]),
]

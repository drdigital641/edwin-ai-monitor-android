# R&C content brief for writers (read fully before writing)

Project: R&C - Retail & Commercial Design & Build, a NEW Singapore brand owned by Edwin (Page One Singapore).
Full client brief: PROJECT-BRIEF.md in this folder (read sections 3, 5, 7, 8, 10).
Audience: Singapore owners and tenants of shops, offices/showrooms, cafes/service counters, salons/beauty studios.

## Hard rules (a page that breaks one is rejected)
1. NO invented facts: no years of experience, project counts, clients, team size, in-house team, factory/workshop,
   accreditations, licences held, insurance, warranties, awards, reviews, brand partnerships, office address.
2. NO prices, price ranges, minimum budgets or turnaround times/deadlines. Talk about what DRIVES cost and time instead.
3. NO regulatory specifics stated as fact (no named authorities, permit names, licence types, fees, rules).
   Allowed wording: "Check with your landlord or mall management about approvals, permitted working hours and
   contractor rules." / "Some works may need submissions by qualified professionals; these should be identified
   at the site assessment stage." Nothing more specific.
4. Voice: the business does not yet have a proven delivery team, so do NOT write "our team", "our craftsmen",
   "we have completed", "we guarantee". Explain the service neutrally ("A commercial carpentry scope usually covers...")
   and describe R&C's INTENDED process ("An R&C project is planned to follow these steps"). "We" may appear only
   for planning/enquiry help: "Send us your floor plan", "we'll discuss your scope".
5. Never claim kitchen exhaust, structural, fire-safety submissions, specialist certification, full F&B compliance.
   Cafe content: counters, seating, display, finishes only; food licensing/kitchen compliance is the operator's own matter
   (say so softly, without naming agencies).
6. No superlatives (best, leading, No.1, premium-quality guaranteed), no "cheapest", no guaranteed results.
7. Every page is DISTINCT. Respect scope boundaries (PROJECT-BRIEF section 5): Design & Build = integrated planning +
   coordination; Renovation = fit-out/refurbishment execution; Carpentry = counters, cabinets, shelving, storage, display
   fixtures, reception joinery; Electrical = power points, wiring, general lighting installation; AVL = sound, screens,
   feature lighting and controls. Link across rather than repeat.
8. Plain, practical, concise British/Singapore English ("colour", "metre"). Short paragraphs. Answer-first: under each
   H2 that is a question, the first paragraph answers it in 40-60 words.
9. Generic dimensions/design norms are OK only if phrased as typical starting points to confirm on site
   (e.g. "many service counters sit around 900-1,050 mm high; confirm with your staff and equipment"). No statistics.
10. Concept imagery is "AI design concept", never "our project". Don't mention photos unless asked.

## Output format: a Python module (UTF-8), valid syntax, defining a list PAGES = [ {...}, ... ]
Each page dict:
{
  'path': '/services/commercial-carpentry/',      # exactly the path you were given
  'title': 'Commercial Carpentry Singapore | R&C',  # <= 60 chars incl. " | R&C"
  'desc': '...',                                  # 120-155 chars, no "guaranteed"
  'h1': '...',
  'kicker': 'Commercial carpentry',               # 1-3 word label above H1
  'answer': '...',                                # 40-60 words: what it is + who it suits (plain text)
  'card': '...',                                  # 1-2 sentences (<= 30 words) for cards on other pages
  'image': 'counter-joinery',                     # key from the image list below
  'image_alt': '...',                             # describe the scene; end with "(AI design concept)"
  'sections': [                                   # 6-9 sections, total 900-1,400 words per page
     {'h2': 'Who commercial carpentry suits', 'html': '<p>...</p><ul><li>...</li></ul>'},
     ...
  ],
  'faqs': [('Question?', 'Answer, 30-70 words, plain text.'), ...],   # 4-6, specific to this page
  'related': ['/services/commercial-renovation/', '/guides/...'],    # 3-5 internal paths from the site map
  'wa_topic': 'custom carpentry for my shop',     # phrase used in a WhatsApp prefill
}
Allowed HTML in 'html': <p> <ul> <ol> <li> <strong> <em> <h3> <table><thead><tbody><tr><th><td> and
<a href="/path/">anchor</a> to internal paths ONLY from the site map below (descriptive anchors, max ~4 per page).
Use <p class="note">...</p> for a short caution/tip. No inline styles, no images, no external links.
Tables: max 3 columns, short cells (they must read on a phone).

Service-page sections to cover (adapt headings to the topic; brief section 7):
who it suits + problems solved; scope: typically included / usually separate (exclusions); options and trade-offs
(materials, finishes, equipment, layout); what drives the budget (no figures); planning and lead-time factors (no promises);
coordination and site access (landlord/mall, working hours, other trades); the intended process + what the customer
should prepare (floor plan, unit photos, intended use, target opening date); related services.

## Site map (only link to these)
/ , /retail-commercial-design-build/ , /services/ , /services/commercial-carpentry/ , /services/commercial-renovation/ ,
/services/commercial-electrical-works/ , /services/commercial-tiling-flooring/ , /services/commercial-painting-finishing/ ,
/avl/ , /avl/commercial-audio-systems/ , /avl/display-visual-systems/ , /avl/architectural-feature-lighting/ ,
/spaces/ , /spaces/retail-shops-boutiques/ , /spaces/offices-showrooms/ , /spaces/cafes-service-counters/ ,
/spaces/salons-beauty-studios/ , /design-concepts/ , /guides/ , /about/ , /contact/ ,
/guides/how-to-brief-a-shop-fit-out/ , /guides/retail-display-shelving-materials/ , /guides/planning-a-custom-shop-counter/ ,
/guides/small-shop-renovation-checklist/ , /guides/lighting-a-retail-display/ , /guides/background-music-for-shops/

## Image keys (AI design concepts)
hero-boutique (small shop unit, oak shelving, cream walls), office-reception (oak reception counter), cafe-counter,
salon-stations, display-shelving, counter-joinery (custom counter close-up), fitout-site (unit mid fit-out),
electrical-lighting-track (ceiling track lights + neat power points), floor-tiling, paint-finish, avl-display (screen /
digital signage in a showroom), avl-audio (discreet ceiling speakers in a cafe), feature-lighting (accent lighting on
display), design-planning (floor plan + material samples on a table), showroom.

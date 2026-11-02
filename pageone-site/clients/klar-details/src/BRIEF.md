# Klar Details rebuild: writer brief (1 Nov 2026)

Read fully before writing any content module. Sources of truth: research/content-inventory.md (the client's own site, fetched 1 Nov 2026) and research/competitors.md (SERP teardown). Rules: /mnt/project-files/seo-method/MASTER-RULES.md (sections 1-6 are binding).

## Who
Klar Details, premium car detailing centre, 48 Toh Guan Road East, #02-124, Enterprise Hub, Singapore 608586 (Jurong East, West Singapore; a few minutes from IMM and Jurong East MRT; Toh Guan is the estate shared with Enterprise Hub). Phone +65 6635 6703. WhatsApp +65 8917 3950 (wa.me/6589173950). Email klar@motoserv.sg. By appointment: Mon-Fri 9am-8pm, Sat 9am-2pm, Sun and PH closed (homepage version; a blog post said otherwise, flagged for confirmation, so never state hours in article bodies). Operating since 2014. "Over 2,500 cars serviced". An MK Group brand since 1 Nov 2024 (sister brands Motoserv, Mr Kool, Mr Gearbox, K-Tech). Klar Consultant: Eric Wong. Staff named in reviews: Zhi Wei. Tagline: "Because Every Detail Counts".

In-house product lines (never name third-party coating brands as Klar's): KlarCOAT Signature Ceramic Treatment ("about 1 to 2 years with minimal upkeep", typically two layers where suitable), KlarGRAPHENE (graphene coating, "up to 3 to 5 years with proper maintenance"), KlarINTERIOR (interior detailing, controlled-pressure steam, NEA-approved aviation-grade anti-bacterial fumigation, suggested every 6-12 months, quarterly for PHV), KlarMAINTENANCE (half-yearly coating maintenance, KlarSHIELD top layer each visit, pure-water final rinse at ~0 ppm TDS vs Singapore tap water 80-120 ppm), KlarCOAT Titanium (offered through authorised car agents; mention only on About). Signature exterior treatment takes "at least 6 man-hours". Infrared curing lamps are used. Enclosed, dust-free bays; in-house EV charging; EV/hybrid-safe processes (Tesla, BYD, Polestar jobs shown). Free professional car assessment. "No hard sell, transparent pricing" (customer's words).

The ONLY published price: Graphene Coating Bonnet Trial S$88 (premium hand wash, surface preparation, graphene coating on the bonnet, water-beading demonstration, gloss enhancement). Every other price is "fixed quote after the free assessment". NEVER invent a price, duration, warranty term, rating, review count, award or statistic. Where competitors publish prices we only say that the quote is fixed before work starts.

## Writing rules
- Answer first: 40-60 plain words under every question heading, then detail. Short paragraphs. Numbered steps as lists. Comparisons as tables (HTML <table>).
- Premium, calm, precise tone. Perfectionist audience: fewer words, exact words. No hype, no "best", "No.1", "guaranteed", "cheapest". Singapore English, S$ prices.
- "30+ years" is COMBINED team experience; write it that way or leave it out. Never "30 years in business".
- Local detail where true: Toh Guan Road East, Enterprise Hub, Jurong East, IMM, Jurong East MRT, Bukit Batok, Clementi, Boon Lay, Jurong West, Teban, Pandan, Tuas, Pioneer. Covered drive-in, enclosed bays. Do not invent parking fees, travel times beyond "a few minutes' drive", or MRT walking times.
- Each article links to its owner service page with descriptive anchor text and to one related article. Each service page links to 2 related services and 2 articles.
- Titles under 60 characters, descriptions under 160, brand at the end ("| Klar Details"). One H1 per page (the builder adds it from `h1`).
- FAQ answers 40-70 words. Only questions a real buyer types.
- Dates: keep each article's original published date from the inventory; `updated` = "2026-11-01".
- HTML in content strings: only <p>, <h3>, <ul>/<ol>/<li>, <table>, <strong>, <em>, <a href="…">. Internal links are site-relative with a leading slash and trailing slash, e.g. /services/graphene-coating/ or /articles/how-to-wash-ceramic-coated-car/. No <h2> inside section bodies (the section heading becomes the h2). No inline styles, no images (the builder places images).

## URL map (use exactly these)
Services: /services/ceramic-coating/ (KlarCOAT Signature Ceramic), /services/graphene-coating/ (KlarGRAPHENE + S$88 trial), /services/paint-correction/, /services/interior-detailing/ (KlarINTERIOR), /services/interior-pest-control/ (NEA-approved fumigation, odour, bacteria), /services/coating-maintenance/ (KlarMAINTENANCE, KlarSHIELD, pure water), /services/new-car-detailing/ (new car and EV protection packages), /services/premium-hand-wash/ (hand wash and exterior decontamination).
Offer: /graphene-bonnet-trial/ (S$88).
Areas: /areas/ (West Singapore hub), /areas/jurong-east/, /areas/bukit-batok/, /areas/clementi/, /areas/jurong-west-boon-lay/.
Other: /about/, /prices/, /reviews/, /our-work/, /faq/, /contact/, /articles/, /articles/<slug>/ (same slugs as the old blog posts).

## Module format (Python, UTF-8, importable, no code besides the data)
```python
SERVICES = [{
  'slug': 'graphene-coating', 'name': 'Graphene Coating', 'line': 'KlarGRAPHENE',
  'card': 'One or two sentences for the homepage card.',
  'title': '…', 'desc': '…', 'h1': '…',
  'intro': '<p>40-60 word answer-first paragraph.</p>',
  'includes': ['…', '…'],            # what the service includes (from the inventory)
  'steps': [('Step name', 'one sentence'), …],
  'sections': [('Heading as a real question or statement', '<p>…</p>'), …],  # 3-5 sections
  'price': 'Plain sentence on price: S$88 trial where relevant, otherwise fixed quote after the free assessment.',
  'faqs': [('Question?', 'Answer 40-70 words.'), …],   # 4-6
  'related': ['ceramic-coating', 'coating-maintenance'],
  'articles': ['how-to-wash-ceramic-coated-car', '…'],
}]
AREAS = [{'slug': 'jurong-east', 'name': 'Jurong East', 'title': '…', 'desc': '…', 'h1': '…', 'intro': '<p>…</p>',
  'sections': [...], 'faqs': [...], 'nearby': ['IMM', 'Jurong East MRT', …]}]
ARTICLES = [{'slug': '…', 'title': '…', 'date': 'YYYY-MM-DD', 'desc': '…', 'h1': '…', 'owner': 'graphene-coating',
  'intro': '<p>…</p>', 'sections': [('H2 text', '<p>…</p>'), …], 'faqs': [(q, a), …], 'related': ['other-article-slug']}]
```
Articles: 500-900 words, rewritten in our own words from the inventory summary of each post (the inventory text is paraphrased, so never present it as a quote). Merge the duplicate pairs: #12 + #21 water spots -> slug car-water-spot-removal-singapore (keep prevent-car-water-spots-singapore in the 301 list); #15 + #22 bird droppings -> slug remove-bird-droppings-tree-sap-car-paint. Skip #11 "Top 5 Automotive Workshops" (self-promotional, contradicts facts). Facts only from the inventory and general, uncontroversial car-care knowledge (no statistics unless already on Klar's site, e.g. TDS 80-120 ppm, 25-30 hours a month inside cars; humidity "80 to 90 percent").

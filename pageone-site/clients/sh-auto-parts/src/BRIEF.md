# SH Auto Parts website preview - build brief (29 Oct 2026)

Client: SH AUTO PARTS PTE. LTD. (see FACTS.md - the ONLY facts allowed). Edwin's ask: a site like the Mega Power mockup
(/mnt/project-files/mega-power/: build.py, mp.js, staff.js, data.js, wa.js - reuse code/approach), but for a China / EV
car parts supplier, mainly BODY parts, selling in Singapore to WORKSHOPS and CAR OWNERS. No export, no supplier funnel.
Premium / luxury look with luxury photos. Homepage = main business + searchable catalogue right on the homepage.
Search in owner language: brand + model + part, e.g. "Tesla Model Y tail lamp", "Tesla Y bumper", "Denza D9 rear reflector"
(people also type "Denza 09", "model y taillight", "atto3 headlight"). NOT chassis/OEM numbers. Staff login to update catalogue.

Output: /mnt/project-files/sh-auto-parts/ (build.py, sh.css, sh.js, staff.js, staff.css, wa.js, assets/) and built site in
site/ via `python3 build.py site`. Preview URL will be https://pageonesingapore.com/preview/sh-auto-parts/ (BASE in canonical
= https://pageonesingapore.com/preview/sh-auto-parts until a domain exists; keep it a single BASE constant). All internal links
relative (like Mega Power's {{R}} root prefix). No `noindex` meta in pages (preview is hidden by a server header).

## Rules (Page One master rules)
- Never invent: no prices, stock claims, warranty, delivery, "genuine/OEM/original", "authorised", "best/cheapest", reviews,
  years in business beyond "registered 2024", people, phone, hours. Contact = WhatsApp/phone "to confirm" in preview:
  set WA = "" and PHONE = "" constants; while empty, every WhatsApp/enquire button opens the on-site enquiry form
  (/enquiry/?q=...) prefilled with the part, and a small gold "preview note" says the number is pending. When WA is set, buttons
  become https://wa.me/65XXXXXXXX?text=<prefilled "Hi SH Auto Parts, I'm looking for: <part> for <brand model>. (from website)">.
- Brand names are used descriptively only ("parts for Tesla Model Y"). No car-maker logos, use styled text chips.
- Catalogue entries are SAMPLE/DEMO data (no real list yet): each has status "Ask for availability", no price, flag
  sample:true, and the UI shows a subtle "Sample listing - staff to confirm" tag. Staff edits replace them.
- One page per service: /parts/<category>/ pages (bumpers, lamps & lights [headlamps, tail lamps, reflectors, fog lamps],
  mirrors, body panels [bonnet, fender, doors, tailgate], grilles & trims, other parts), plus /brands/<brand>/ (16 brands,
  each lists its models and parts; short honest intro), /for-workshops/, /for-car-owners/, /catalogue/ (full search page with
  brand/model/part filters, URL params ?q= &brand= &model= &part=), /about/ (only FACTS.md facts), /contact/, /enquiry/,
  /privacy/ (PDPA), /articles/ with 3 useful, careful guides (no invented stats; e.g. "Tesla Model Y tail lamp: what to send
  us to get the right part", "Body parts for China EVs in Singapore: what to check before you buy", "Which part is it?
  Bumper, fender, reflector and trim names explained"), /staff/ (demo dashboard), 404.html.
- Lean homepage (~500-900 visible words): hero with big search box + "Try:" chips, brand chip strip, part category cards
  (photo or icon, 1 line + "More details"), featured listings, "For workshops / For car owners" two cards, how it works
  (search -> send car & part -> we confirm fitment and reply), 4 FAQs max (FAQPage JSON-LD == visible), CTA.
- Each page: unique <title> <60 chars, description <160, canonical, og:* + twitter summary_large_image, og:image =
  BASE/og.jpg (1200x630, make with PIL: dark graphite gradient, red accent, the SH wordmark/emblem, "China & EV car parts
  in Singapore"), meta robots "index,follow,max-image-preview:large", favicon.ico (48) + icon-192.png + apple-touch-icon 180
  + site.webmanifest, JSON-LD (AutoPartsStore with legalName, identifier UEN, address = registered address, logo, image;
  BreadcrumbList; FAQPage only where visible; ItemList on catalogue, NO Product/Offer schema since no prices).
- sitemap.xml (lastmod), robots.txt (Allow all incl. OAI-SearchBot, ChatGPT-User, GPTBot, Googlebot, Bingbot, PerplexityBot,
  ClaudeBot, Google-Extended; sitemap line), llms.txt (plain facts), IndexNow key file (32 hex, random), htaccess.txt (go-live
  notes; do NOT ship a real .htaccess).
- wa.js = copy of /mnt/project-files/mega-power/wa.js with site id 'sh-auto-parts' (WA tap counter). Load on every page.
- css/js URLs versioned by content hash (?v=), like Mega Power's asset().
- Motion: reveal-on-scroll (transform/opacity), hover lifts, slow Ken Burns on hero photo, brand-chip marquee; respects
  prefers-reduced-motion; content readable with JS off. No count-up numbers.
- Plain static HTML, fast. Images: width/height + alt + loading=lazy (except hero). Phone-first (Edwin reviews on a phone):
  sticky bottom bar on mobile (Search / Enquire / WhatsApp). No horizontal scroll at 360px.

## Look
Luxury automotive: near-black #0A0A0C / graphite #141418 / #1C1C22 surfaces, white text, logo red #D7262E accent (thin red
lines, buttons), a little warm silver #C9C9CF. Headings: "Saira" (Google Fonts, 600-800, slight italic for hero like the logo);
body "Inter". Generous spacing, large photography, subtle glass header. Light sections may alternate (#F4F3F0) for catalogue
readability - your call, keep contrast AA.

Logo: recreate as inline SVG (placeholder until client sends the file): a red (#D7262E) circular emblem - a thick ring open at
upper right with a sharp swoosh tail, containing a bold stylised italic "S" - next to italic heavy wordmark "SH AUTO" / "PARTS"
in black (white on dark), tagline "China Car Parts Supplier". Make favicon PNGs from the emblem (render the SVG with Playwright
chromium screenshot: require('playwright') works, chromium.launch() no options; or draw with PIL).

Photos (free Unsplash License, hotlinked; the sandbox cannot download them, browsers can). Use
`https://images.unsplash.com/photo-<id>?auto=format&fit=crop&w=<w>&q=70` with srcset (800/1400/2000) and a dark CSS
gradient behind each so a failed load still looks good. Credit line on /about/ ("Stock photos: Unsplash"). Label these as
"mood" imagery only - never as SH's products. IDs + what they show:
- 1642268565002-729f4e3dad5b  tail light of a car in the dark  (HERO)
- 1620891549027-942fdc95d3f5  matte black electric car parked under warm sky
- 1560958089-b8a1929cea89     white saloon parked beside mountains (Tesla-style EV)
- 1725745096249-f6e7c160c4be  close-up of a car tail light
- 1518438223361-dde09dbeed6a  vehicle taillight turned on
- 1531843256863-af93f4edfcfb  red vehicle headlights
- 1593941707874-ef25b8b4a92b  EV charging cable plugged into car
- 1666919643134-d97687c1826c  white sports car in a showroom
- 1572191267783-5618f992aff5  black Tesla steering wheel / interior
- 1615903214534-582a77a2a85e  red and black car door (body panel)
- 1648866892162-9336ef9182e2  white Tesla Model 3 in a car park (Singapore photographer)
Product cards without a staff photo use a refined SVG line icon of the part type (bumper, headlamp, tail lamp, reflector,
mirror, bonnet, fender, door, tailgate, grille, trim, other) on a dark card - not stock photos.

## Catalogue data (data.js, SAMPLE)
Brands -> models sold in Singapore (keep to these; don't add years or variants):
Tesla: Model 3, Model Y | BYD: Atto 3, Dolphin, Seal, Sealion 7, M6 | Denza: D9 | MG: MG4, ZS EV, MG5, HS |
Maxus: MIFA 9, eDeliver 3 | Chery: (no model - "ask us") | Omoda: Omoda E5 | Jaecoo: J7 | GAC: Aion Y, Aion V | XPeng: G6, X9 |
Foton: (no model - "ask us") | Geely: (no model - "ask us") | Zeekr: 001, X, 009 | Deepal: S07, L07 | Avatr: 11, 12 | Ora: Good Cat.
Part types (slug, name, synonyms owners type):
front-bumper (front bumper, bumper front, fbumper) | rear-bumper (rear bumper, back bumper) | bumper-trim (bumper lip, bumper
strip, bumper garnish, "sticker bumper", bumper moulding) | headlamp (headlight, head lamp, front light) | tail-lamp (taillight,
tail light, rear lamp, back light, brake light) | rear-reflector (reflector, rear reflector, bumper reflector) | fog-lamp (fog
light) | side-mirror (wing mirror, side mirror, mirror cover, mirror glass) | bonnet (hood) | fender (front fender, wing) |
door-panel (door, door shell) | tailgate (boot, trunk lid, liftgate) | grille (front grille, grill) | wheel-arch (arch
lining, fender liner) | other (wiper, cabin filter, etc.).
Generate ~90-120 sample entries: for each model, a sensible subset (all get headlamp, tail-lamp, front-bumper, rear-bumper,
side-mirror; plus a few others). Entry: id, brand, model, part slug, title like "Tesla Model Y Tail Lamp", position where
natural (Left / Right / Pair - make 'side: "Left or right - tell us"' generic, don't invent part numbers), status "ask",
sample:true, photo "" (staff can set URL), note "".

## Search (sh.js) - the most important feature
Normalise: lowercase, strip punctuation, collapse spaces. Model aliases: "y"/"model y"/"my" -> Model Y, "3"/"model 3"/"m3"
-> Model 3 (only when brand Tesla present or with "model"), "09"/"d 9"/"d9" -> D9, "atto3"/"atto 3", "seal u" etc.; brand
aliases: "byd", "denza", "mg", "aion"->GAC Aion, "omoda", "jaecoo", "zeekr", "xpeng"/"xpeng"/"xiaopeng". Part synonyms as
above (multi-word first). Score = brand match + model match + part match; show best results first with matched words
highlighted, live as you type (debounced), on homepage (top 6 + "See all N results" -> /catalogue/?q=) and on /catalogue/.
Zero/weak match: friendly card "We may still have it - send us your car and part" -> enquiry prefilled. Each result card:
part icon/photo, title, brand-model chip, part type, status pill ("Ask for availability" / staff-set "In stock" / "Can
order"), buttons: "Enquire" (WA or form) + "Details" (modal or anchor). Test these queries must return the right top result:
"Tesla Model Y tail lamp", "tesla y taillight", "model y bumper", "Denza D9 rear reflector", "denza 09 reflector",
"atto3 headlight", "MG4 side mirror", "zeekr 001 bonnet", "sticker bumper model y" (-> bumper trim). Write a tiny node test
(tools/search_test.mjs) that loads data.js + search fn and asserts these.

## Staff dashboard (/staff/) - demo, like Mega Power's staff.js
Login screen (demo: any name + PIN shown on screen "demo PIN 2468"; clearly says "Demo - real login added at go-live").
After login: list/search all entries, add/edit/delete (brand, model, part type, title, side, status, optional price text
field "staff choice, shown only if filled", photo URL, note, published toggle), bulk "mark sample entries as confirmed",
enquiries inbox (from the enquiry form, stored in localStorage), export/import JSON. Public pages merge localStorage staff
changes over data.js (same as Mega Power: mp_*_v1 keys -> sh_*_v1). A top preview bar on public pages: "Preview for SH Auto
Parts - not live. Staff demo: /staff/".

## Done = 
build runs clean; search tests pass; every JSON-LD parses; FAQ schema count == visible; no broken internal links (write a
small checker); screenshots with Playwright (phone 390x844 and desktop 1440x900) of home (top + scrolled), catalogue with
query "Tesla Model Y tail lamp", a brand page, a parts page, staff dashboard after login -> save to
/mnt/project-files/sh-auto-parts/screens/*.jpg. Note: the sandbox cannot load Unsplash/Google Fonts (network blocked), so
screenshots will show the fallback gradients - that's expected; make sure fallbacks look premium anyway.

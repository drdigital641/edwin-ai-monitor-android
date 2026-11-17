# Maison new-launch page template (LOCKED, Edwin 16 Nov 2026 3:49pm SGT)

Source of truth: the 7 live full-concept pages, read through the Bridge on 16 Nov 2026 ~08:00 UTC
(pageone:preview/maison-interior-design/new-launches/<slug>/index.html). All 7 live files are byte-identical
to the generator output below, so the generator IS the template.

| Page | live sha256 (16 Nov) | FAQ | type-card CTAs |
|---|---|---|---|
| chencharu-acres | ec98acb2... | 13 | 2room 3room 4room 5room |
| toa-payoh-hillside | 0351bdb8... | 14 | cca 2room 4room |
| bayshore-sails | f3f46bb6... | 14 | 2room-t1 2room-t2 3room 4room |
| plantation-dew | c906052b... | 14 | 2room 3room 4room 5room 3gen |
| sembawang-anchor | d4ba3b93... | 13 | 2room 3room 4room 5room |
| brickland-weave | 945cd5b6... | 9 | 2room 3room 4room 5room |
| keat-hong-grange | ec12740f... | 10 | 2room 3room 4room 5room |

## 1. Where the template lives (ONE place for shared parts)
Repo drdigital641/edwin-ai-monitor-android, branch `claude/project-thread-6s51oo` (commit cf7fa7f), folder `maison-expand/gen2/`:
- `gen2.py` = page builder. Shared blocks are functions/strings here: `btn()` (tracked WhatsApp button), `band()` (CTA band),
  JSON-LD graph, FAQ block, trust block, related-articles list, sources, nearby cards, end CTA. Change once, rebuild all.
- `head.html` (header + nav), `foot.html` (footer), `fab.html` (sticky WhatsApp dock), `plan.html` (floor-plan figure),
  `nv.css` + `../gen/nlp-expand.css` -> shipped as `/nlp-expand.css` (live ?v=f0b6baaf; file sha 95660c5f).
- `data.py` = ONE dict per project (`P["<slug>"] = dict(...)`): name, town, region, cls, units, dir (v4 folder), types
  (label, key, official count/area), official URL, glance rows, plans (img, w, h, alt, title, caption), plan_gaps,
  rooms4 (living/kitchen/main/common/other), feat, renders (4 x R(room, style, stem, pos, text, alt)), near, extra_src,
  faq_new, intro. Optional: faqs, ans, near_cards, near_h, kw, cite, pub, checked.
- Build: `python3 maison-expand/gen2/gen2.py <outdir> <slug>`; deploy with Bridge `sync_from_github` (base_sha256 per replaced file).
- A new project = a new `data.py` entry only. Never hand-edit a built page; never copy header/footer/CTA HTML into data.
- Variants still to add to gen2 before their first build: CONDO/EC/LANDED (developer brochure plans, "Private condominium"
  wording, no HDB MOP/Prime lines; title/desc say "<town> condo/EC" not "BTO") and COMMERCIAL (Shaw Tower set: reception,
  open office, meeting room, pantry; H1 "<Name> Fit-Out & Interior Design"). gen2 today is BTO/HDB-only (desc hard-codes "BTO").

## 2. Head / meta pattern
- title: `<Name> Renovation & Interior Design | Floor Plan, Ideas, Quote — Maison`
- meta description: `<Name> <Town> BTO: flat types, floor plan guide, renovation ideas and a free layout plan for your unit type. WhatsApp Maison.`
- H1: `<Name> Renovation & Interior Design` (commercial: `Fit-Out & Interior Design`)
- canonical + og:url `https://maisoninteriordesign.sg/new-launches/<slug>/`; og/twitter title+desc = title/desc.
- Assets: `/mid.css?v=27d05deb`, `/nlp-expand.css?v=f0b6baaf`, `/mid.js?v=10d9e567`, `/p1-cta.js?v=b54fbe0c` (tap tracker; required).
- JSON-LD @graph: HomeAndConstructionBusiness, BreadcrumbList, Article (datePublished = page's first publish, `pub`;
  dateModified = build date), FAQPage (one Question per visible FAQ).
- LIVE GUARD: a title/meta/JSON-LD/FAQ-question change on an existing page needs a one-time GUARD_OVERRIDES entry
  (see DAILY-LAUNCH-PAGE.md step 6). Keep every old FAQ question verbatim; only add.

## 3. Section order (top to bottom, all 7 pages identical)
1. Header + nav, breadcrumb (`nav.nlp-crumbs`)
2. HERO `section.nv-hero`: H1, short intro, swipeable gallery of the 4 v4 renders (`figure.nv-slide s0..s3`):
   s0 Living room (hero), s1 Kitchen, s2 Main bedroom, s3 Common bedroom. Caption = "<Room>: <Style name>" +
   "Concept design by Maison, not the actual unit". Files `/images/new-launches/<slug>-v4/<slug>-v4-<room>-<style>-1920.webp`
   (+ -900 srcset). CTA data-ref `<slug>-hero`.
3. FLAT TYPES `#flat-types`: one card per official flat type (count + approx. area from HDB), each with a
   "Free layout plan for <type>" CTA, data-ref `<slug>-type-<key>`.
4. AT A GLANCE `.nlp-facts-s`: official facts table (type/classification, location/bounds, units, blocks/storeys, dates as HDB estimates).
5. SPACE PLANNING `#space-planning`: official HDB Layout Ideas plan (`figure.nv-plan`, credited, "typical plan, not a specific
   stack"), then room by room for the full plan: living/dining (shelter), kitchen + service yard, main bedroom, common
   bedrooms, baths: zoning, storage spots, traffic flow, keep/hack. Real areas only.
6. CTA BAND 1 (`.nx-band`): "Get a free layout plan for your 4-room at <Name>", data-ref `<slug>-plan`.
7. CONCEPTS `#concepts`: "The design thinking behind the four concepts": per render the palette, materials, lighting and why it
   suits this flat/estate, plus practical theory (light, flow, storage ratio, small-space tricks).
8. RECOMMENDATIONS `#recommendations`: per flat type must-dos, nice-to-haves, common mistakes, phase timeline from key
   collection, checklist. No invented prices.
9. CTA BAND 2: "Want this scoped for your <Name> flat?", data-ref `<slug>-recs`.
10. TRUST `.nv-trust`: "HDB homes Maison has designed" (3 real Maison project photos from /wp-content/uploads/).
11. PLANNING `.nlp-plan-s`: "Planning your <Name> renovation" (permit, defects, timeline).
12. ABOUT `.nv-about`: "About <Name>" (official intro).
13. RELATED ARTICLES `.nv-rel`: 3 Maison links (today: /articles/itemised-renovation-quotation/,
    /articles/prepare-for-interior-design-consultation/, /services/bto-renovation/). Pick 3-5 that fit; if none fit, list topics for the writer roster.
14. FAQ `.nlp-faq`: 9-14 `<details class="qa">` + "Ask Maison on WhatsApp" CTA, data-ref `<slug>-faq`.
15. SOURCES AND LINKS `.nlp-src`: HDB project page, Layout Ideas image, brochure, HDB BTO portal (4-6 links).
16. NEARBY `.nlp-near`: 4-5 related launch cards on the site ("More November 2026 BTO launches" or "Nearby new launches").
17. END CTA `section.cta.dark`: "Planning your <Name> renovation? WhatsApp Maison", data-ref `<slug>-end`.
18. Footer, sticky dock (`fab.html`) data-ref `<slug>-dock`.

## 4. CTAs (all tracked on the Controller)
WhatsApp 6593391185, prefilled with project + flat type, every link has `data-ref` and the page loads `/p1-cta.js`.
Live set: hero, type-<key> (one per flat type), plan, recs, faq, end, dock (9-11 refs per page).
Prefills: hero "Hi Maison, I'm planning my <Name> renovation. Can I see design ideas and a quote?";
type "Hi Maison, I'm collecting keys at <Name> (<type>). Can I get a free layout plan for my <type>?".
One ?p1test=1 tap per new page must show as a CtaClick test row before the page is DONE (Controller sandbox can reach the domain).

## 5. 390px rules
Mobile first at 390px: no horizontal scroll (scrollWidth = 390), gallery swipeable with dots, one-column cards, CTA buttons
full width and >= 44px tall, plan image scales to width, long text below the pictures. Check 390 and 1280 before DONE.

## 6. Minimum quality bar (a page below this is FLAGGED and does not go live)
- 4 v4 renders present, from Base44 (no OpenAI, no stock), all 4 slots filled, captions with the concept disclaimer.
- Official floor plan shown and credited (HDB Layout Ideas or developer brochure). No plan on file = condo/EC variant waits, or flag.
- 15 H2 sections in the order above; >= 3,100 words in the rendered page; >= 9 FAQ with matching FAQPage JSON-LD.
- Facts (developer, units, flat types, areas, dates) only from official sources, each linked in Sources; HDB dates called estimates;
  never claim balcony/park-view stacks, key dates or prices that are not published.
- >= 9 tracked CTAs incl. hero, plan, recs, end, dock; p1-cta.js loaded; one ?p1test=1 tap recorded.
- dateModified = build date; canonical/og correct; no noindex, no /preview/ links, no Page One credit (white-label).
- sitemap.xml updated (Bridge auto step) and IndexNow sent (retry later on 429).

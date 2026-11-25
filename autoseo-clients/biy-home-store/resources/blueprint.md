# BIY Home Store — Phase 1 website blueprint (draft v1)

AutoSEO (Malaysia). Drafted 25 Nov 2026, SGT. Phase 1 only: SEO + product catalogue + WhatsApp enquiry. No cart, login or payment (Phase 2/3 not started).
Client match is likely but **not confirmed**: BIY Home Store (Kota Tinggi) Sdn Bhd, Johor, 4 branches (see README.md). Nothing below invents products, prices, stock or contact details. Every product, price and photo comes from AutoCount (or a CSV export) later; demo data is flagged and can never publish live.

Fixed rules applied: client-site-fixed-rules group A (A0 gate open), mobile-first-wow, template-first, senior SEO workflow.

---

## 0. Key decisions at a glance
| Decision | Choice | Helps |
|---|---|---|
| Render | Server-rendered HTML from one product database + shared templates (no hard-coded product HTML, no client-only rendering) | SEO: Google sees full H1, text, price, schema in source. Maintenance: one template edit updates every page |
| Data | AutoCount → sync job → website DB → templates. Pages never call AutoCount live | Speed (Core Web Vitals), uptime if AutoCount is offline |
| Product URL | `/product/<slug>/`, slug stored once, never auto-changed; 301 table on any change | Keeps rankings; no broken links when AutoCount names change |
| Variants | One page per product family (e.g. one paint range), sizes/colours as variants with own SKU | Matches real searches like "harga cat jotun majestic 5 liter" without 5 thin duplicate pages |
| Index rule | A product is indexable only if active + real photo + enough real description/specs; else it is listed but `noindex` | Avoids thousands of thin pages (brief rule 10.5) |
| Filters | Filter/sort/search URLs = canonical to clean page + `noindex,follow`; only curated brand×category combos get clean URLs | No duplicate-URL bloat, crawl budget goes to real pages |
| Search | Big search bar first; searches name, SKU/item code, brand, category, model; Malay/English synonyms (cat=paint, gerudi=drill, simen=cement) | Discovery for walk-in style queries; search terms logged → content gaps |
| Price display | Real AutoCount price, or "WhatsApp for latest price" if Edwin/client prefers; never invented | Conversion: price visibility is goal 3; trust |
| Stock | Labels only (In stock / Limited / Check availability), per branch, thresholds in config | Sets expectation without exposing exact quantities |
| Language | Write English once; cheap translation to real `/ms/` and `/zh/` pages + hreflang (rule A6) | Malay queries dominate autocomplete ("kedai hardware", "harga cat") |
| Look | BIY's own orange #ED5623 + charcoal, the tilted-square logo as shape motif; must NOT look like Shopee (Shopee is also orange) | Client recognises it; avoids "Shopee clone" look |
| CTA | WhatsApp prefill with product, SKU, URL and branch; tracked on Controller + GA4 | Goal 4 (WhatsApp) measurable per product |

---

## 1. Complete sitemap
```
/                                   Home
/search/?q=                         Search results (noindex,follow)
/category/                          All categories
/category/<cat>/                    e.g. /category/paint-painting-supplies/
/category/<cat>/<subcat>/           e.g. /category/power-tools/cordless-drills/
/category/<cat>/page/2/             Crawlable pagination
/brand/                             All brands (5 only)
/brand/jotun/  /brand/nippon-paint/  /brand/ici/  /brand/bosch/  /brand/dong-cheng/
/brand/<brand>/<cat>/               Curated combos only when ≥ 8 real products (e.g. /brand/bosch/power-tools/)
/product/<slug>/                    Product detail (one per product family)
/contractors/                       Trade supply + quotation via WhatsApp
/stores/                            All branches + map
/stores/<branch>/                   One per confirmed branch (Kota Tinggi HQ, Kota Tinggi JTH, Kota Masai, Pontian — to confirm)
/hardware-shop/<area>/              Area pages from one area template, towns within 20 km of a branch (rule A4), after branches confirmed
/articles/                          Guides hub (nightly runner later, rule 23/29b)
/articles/<slug>/                   e.g. "How much paint for a 3-room house"
/about/  /contact/  /privacy/       (privacy linked in footer, rule 13)
/ms/...  /zh/...                    Full mirrors of every indexable page
/sitemap.xml                        Index → pages, categories, brands, products-1..n, articles, ms, zh
/robots.txt   /llms.txt             Generated, never hand-edited
```
Why: a shallow, predictable tree (home → category → product within 3 clicks) lets Google crawl everything from links, not from the search box.

---

## 2. Homepage wireframe (desktop 1280)
```
[Top bar: 4 branches · open today hours · WhatsApp]               (from data file)
[Logo BIY] [=========== Search {product_count} products, SKU, brand ===========][WhatsApp][Stores]
[Nav: Paint | Power Tools | Hand Tools | Electrical | Plumbing | Building Materials | Safety | Adhesives | Brands | Contractors]
[Hero band: 1 real store photo / promo banner (only real promos) + H1 + 1 line + WhatsApp]
[Shop by category: 9–12 tiles with real product photos]
[Popular brands: Jotun · Nippon Paint · ICI · Bosch · Dong Cheng (logo tiles → brand pages)]
[Best sellers: product card rail (from AutoCount sales data, else hidden)]
[Featured products: grid 5×2]
[Special offers: only if real offer data exists, else section not rendered]
[Contractor supply band: bulk enquiry → WhatsApp quote]
[Why shop with us: 4 icons — wide range, recognised brands, reasonable prices, 4 branches]  (no unverified claims)
[Store locator: map + 4 branch cards (address, hours, call, directions, WhatsApp)]
[Reviews: "See our 5-star reviews" + real review quotes (no overall rating)]
[Footer: category links · brand links · branches · privacy · language switch]
```
Why: search first (goal 2), brands and categories as crawlable links (SEO), stores + WhatsApp on every screen (goals 4–5).

## 3. Mobile homepage wireframe (390px, designed first)
```
┌ Sticky header: [BIY logo] ........ [EN|BM|中] [WhatsApp]
├ Search bar (full width, sticky on scroll)  "Cari produk / Search paint, drill, SKU"
├ Category icon grid: 2 rows × 4, swipe for more
├ Hero card: real store photo, H1 (≤12 words), WhatsApp button      ← all in first screen
├ Brand chips rail (5 brands)
├ Best sellers rail (2-up cards, finger-drag carousel per rule A9)
├ Featured grid 2 columns
├ Contractor band (one line + "Get trade quote" WhatsApp)
├ Nearest branch card (4 branches, tap to call / directions)
├ Reviews strip
└ Footer accordion (categories, brands, branches)
Bottom bar (fixed): Home · Categories · Search · WhatsApp · Stores
```
Why: ~70% mobile traffic; search + category + WhatsApp all reachable with a thumb, no scrolling.

## 4. Product listing (category) page layout
```
Breadcrumb: Home › Power Tools › Cordless Drills
H1: Cordless Drills            (1–2 line intro, real)
[Filter chips: Brand · Sub-type · Voltage/Size · Price range · Availability]   (mobile: bottom sheet)
[Sort: Popular | Price ↑ | Price ↓ | Newest]          ← changes view, URL canonical stays clean
Grid: 2 cols (390) / 5 cols (1280)
  Card: 1:1 photo · brand · name (2 lines) · size chips · price or "Check price" · stock label · [WhatsApp]
Crawlable pagination 1 2 3 … (real <a> links)
Below grid: short buying guide + 3–5 real FAQs + links to related categories and brands
```
Why: Shopee-style scanning for conversion; real paginated links and text below the grid for SEO.

## 5. Individual product page layout
```
Breadcrumb: Home › Paint › Interior Paint › Jotun …
[Gallery 1:1, swipe, zoom]        | Brand (link) · H1 product name
                                  | SKU / item code · Model
                                  | Variant picker (size / colour) → price + SKU update
                                  | Price (real) or "WhatsApp for latest price"
                                  | Availability by branch (labels)
                                  | [WhatsApp enquiry — primary]  [Call]  [Directions]
Key specs (4–6 bullets from AutoCount specs)
Description (indexable text from data)
Full spec table
Related products (same category + same brand), more from brand
FAQ (only from real data / client answers)
Sticky mobile bar: price + WhatsApp
```
WhatsApp prefill template (one shared template):
`Hi BIY, I am interested in {brand} {name} {variant}, SKU {sku}. {url} May I check the latest price and stock availability at {branch}?`
Why: everything a buyer needs above the fold; the prefilled message tells staff exactly which SKU, so replies are faster (conversion).
Schema: `Product` + `Offer` only when a real price exists (Google product rich results need price, review or rating); `BreadcrumbList` always.

## 6. Category and brand page layout
Category: as section 4, plus sub-category tiles at top, "Shop by brand" chips (only brands with products in that category).
Brand page (`/brand/jotun/`):
```
H1: Jotun paint at BIY Home Store     (brand intro, 2–3 lines, factual)
Product ranges (tiles from data: e.g. interior / exterior / waterproofing — only ranges stocked)
Categories this brand appears in (links)
Product grid (filterable, paginated)
Brand FAQs (e.g. "Which branch stocks Jotun?" — from client answers)
Links: other paint brands, paint guides, nearest branch
```
Why: brand pages target "kedai cat jotun near me", "nippon paint shop", "dong cheng near me" — clear brand + local intent.

## 7. SEO URL architecture
- Lowercase, hyphens, trailing slash, English slugs; `/ms/` and `/zh/` reuse the same slug after the prefix (simple hreflang pairing).
- Product slug = brand + product family (+ key size only if the family has one size). SKU kept out of URL so item-code changes don't break URLs.
- Slugs stored in DB (`slug_locked=1`); renames go to `redirects` table → 301.
- Parameters (`?sort=`, `?brand=`, `?price=`, `?q=`, `?page=` on filters) → `rel=canonical` to clean URL, `noindex,follow`, not linked with crawlable <a>.
- Curated combos (`/brand/<b>/<cat>/`) only when ≥ 8 real products, else not generated.
- One URL per thing: no `/product/<id>` aliases, no category path inside product URL (product can sit in 2 categories without duplicates).

## 8. Product database structure (proposed, MySQL)
| Table | Key fields |
|---|---|
| products | id, autocount_item_code (UNIQUE), family_id, name, slug (UNIQUE, locked), brand_id, short_desc, description, status (active/inactive), is_indexable (computed), is_demo, source_updated_at, synced_at |
| product_families | id, name, slug, brand_id, primary_category_id, description, seo_title, seo_description (manual, sync never overwrites) |
| variants | id, family_id, item_code (UNIQUE), label (e.g. 5L / White), uom, barcode, price, member_price (if shown), price_updated_at |
| brands | id, name, slug, allowed (only the 5), intro, logo_path |
| categories | id, parent_id, name, slug, sort, intro, faq_json |
| category_map | autocount_item_group / item_type → category_id (manual mapping) |
| product_categories | product_id, category_id, is_primary |
| images | id, family_id/variant_id, path, alt, width, height, sort, source (autocount/manual) |
| specs | family_id/variant_id, key, value, unit, sort |
| stock | variant_id, branch_id, qty (private), label (computed), updated_at |
| branches | id, name, slug, address, lat, lng, phone, whatsapp, hours_json, gbp_url |
| redirects | from_path, to_path, created_at |
| sync_runs / sync_errors | run id, type (full/delta/stock/price), started/ended, counts, error rows |
| search_log | term, results_count, ts (for content gaps) |
| site_config (one file) | name, WhatsApp numbers, stock thresholds, price display mode, CTA templates, language list |

## 9. AutoCount API integration plan
Flow: AutoCount → sync job (cron on server) → staging tables → validation → website DB → page cache cleared for changed URLs → sitemap lastmod + IndexNow ping.
1. Confirm product: AutoCount Accounting (on-prem) uses AOTG API (AOTG Client installed on their AutoCount server) — https://wiki.autocountsoft.com/wiki/Introduction_to_AOTG_API ; AutoCount Cloud Accounting uses the Integration API with API-Key + Key-ID headers and per-key permissions — https://accounting-api.autocountcloud.com/documentation/ . Ask for a key limited to read-only stock item / price / stock methods.
2. Jobs: nightly full item sync; delta every 30–60 min using modified-date filters (AOTG StockItem GetList supports ModifiedFromDate/ModifiedToDate); stock/price sync on its own schedule.
3. Validation: reject rows without item code; UNIQUE item_code (duplicate SKU prevention); price > 0 or treated as "Check price"; brand must map to one of the 5 or row is held; category must be mapped or row held in review queue.
4. Errors: retries with backoff (1, 5, 15 min), then mark run failed + alert to Controller; last good data keeps serving.
5. Images: AutoCount usually has few photos → images managed on our side keyed by item code; AutoCount image URLs used if provided.
6. Inactive items: page stays 200 with "No longer available" + related items for 90 days, then 301 to category (no mass 404s).
7. Demo data: `is_demo=1`, shown only on preview with a "Demo data" ribbon; pre-upload check fails the build if any demo row or placeholder price reaches the live host.
8. Before AutoCount access: import from a CSV export (AutoCount or SiteGiant) using the same staging + validation path, so the API later just replaces the source.
Secrets: API keys stored only on the server (env/config outside web root), never in briefs or chat.

## 10. Technical SEO checklist
- [ ] One H1 per page; title ≤ 60 chars starting with the keyword; unique meta description
- [ ] Server-rendered HTML, crawlable nav + footer links to all categories and brands
- [ ] Canonical on every page; filter/sort/search noindex,follow
- [ ] Dynamic sitemap.xml index (split ≤ 10,000 URLs per file), lastmod from data; robots.txt points to it
- [ ] Breadcrumbs + BreadcrumbList schema; Product/Offer only with real price; Organization + LocalBusiness (HardwareStore) per branch with real NAP; FAQPage only with real FAQs
- [ ] hreflang en / ms / zh / x-default; language switch goes to the same page (rule A6)
- [ ] Images: WebP/AVIF, width/height set, lazy below fold, alt text from product name + brand
- [ ] Core Web Vitals: LCP < 2.5s on 4G at 390px, CLS < 0.1; no heavy JS framework on product pages
- [ ] OG tags with 1200×630 JPG/PNG < 300KB (rule 12)
- [ ] Security headers + /privacy/ (rule 13); caching rules (rule 30)
- [ ] 301 redirects table; inactive product handling; no soft 404s
- [ ] GA4 + Search Console + Bing + IndexNow ready (submission at go-live, rule 29)
- [ ] CTA tracking on every WhatsApp/call/directions button (rule 11): events whatsapp_click (sku), call_click, directions_click, view_item, search (term), select_category
- [ ] Preview noindex, one-switch go-live config (rule 15); base-switch + apex/www SSL gates (29a, 29e)
- [ ] If replacing biyhomestore.com: full 301 map from every old SiteGiant URL (products, categories, pages) before switching

## 11. Phase 1 development roadmap
| Step | What | Done when |
|---|---|---|
| 0 | Gate: confirm client, Controller record, billing (rule A0); domain decision; WhatsApp number | Edwin confirms |
| 1 | Data: CSV export + real category tree + brand mapping; photo source | Category map approved |
| 2 | Design sample: ONE 390px homepage sample to Edwin (standing rule) | Edwin happy |
| 3 | Templates: header/footer/CTA/schema/card/listing/product/brand/store/area as shared templates + site_config | Grep check passes |
| 4 | Catalogue: import (demo → real), index rule, search + synonyms | Real products render |
| 5 | Content: 5 brand pages, category intros, 4 store pages, contractors page, area pages (20 km) | All written in English once |
| 6 | Translations: /ms/ and /zh/ via cheap translation, hreflang | Switch never 404s |
| 7 | Tracking: GA4 + Controller CTA test taps | Test tap recorded |
| 8 | QA gate: 390px + 1280px shots vs best previous site; CWV; schema test | Passes rule 16 |
| 9 | Go-live: base switch, SSL, GSC/Bing/IndexNow, Controller Live, article runner row | Rules 28–29e ticked |
| 10 | AutoCount: switch source from CSV to API when key arrives | Delta sync running |

---

## Keyword research (brief, Malaysia) — Google autocomplete, gl=my, checked 25 Nov 2026
No search volumes yet (needs Keyword Planner / GSC). These are real phrasings Google suggests. Raw: `research/autocomplete-2026-11-25.json`.
| Cluster | Real queries seen | Intent | Target page |
|---|---|---|---|
| Local "near me" | kedai hardware near me; kedai hardware near me open now; hardware shop near me open sunday; kedai hardware cat near me; kedai hardware elektrik near me | Find/visit | Home + /stores/ + GBP (Map Pack) |
| Local town | kedai hardware kota tinggi (johor); hardware shop kota tinggi; hardware shop pasir gudang; kedai hardware pasir gudang; hardware shop pontian; kedai hardware pontian | Find/visit | /stores/<branch>/ |
| Paint brand + shop | kedai cat jotun near me; kedai cat nippon near me; jotun kota tinggi; kedai cat jotun kota tinggi; paint shop near me jotun; ici paint shop near me | Buy/visit | /brand/jotun/, /brand/nippon-paint/, /brand/ici/ |
| Paint price (Malay) | harga cat jotun 5 liter / 18 liter / 20 liter; harga cat jotun majestic 5 liter; harga cat nippon paint 5 liter / 18 liter; harga cat nippon paint weatherbond 18 liter; harga cat dulux 18 liter; harga cat dulux weathershield | Buy (price) | Product family pages with size variants |
| Paint price (English) | jotun paint price malaysia; jotun majestic price malaysia; nippon paint price malaysia; nippon weatherbond price malaysia; ici paint malaysia price list | Buy (price) | Same product pages (/ms/ vs English titles) |
| Power tools brand | bosch power tools malaysia dealer; bosch cordless drill malaysia; harga bosch drill; harga bosch gws 700; dong cheng drill; dong cheng cordless drill price; dong cheng grinder; dong cheng near me | Buy | /brand/bosch/, /brand/dong-cheng/, product pages |
| Building materials | harga simen 1 bag (terkini); harga simen semasa; harga simen 1 pallet | Price check | /category/building-materials/ (only if prices published) |
| Brand navigational | biy home store; biy home store kota tinggi; biy home store jth | Navigational | Home, store pages |
Notes: ICI Paints Malaysia became Akzo Nobel Paints (Malaysia) and sells as Dulux (https://www.dulux.com.my/en/about-us), so the ICI brand page should say "ICI (Dulux)" and target both names — once the client confirms what is stocked. Malay price queries are the strongest pattern → `/ms/` product pages matter.

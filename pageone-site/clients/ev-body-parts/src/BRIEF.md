# EV Body Parts (evbodyparts.sg) - build brief (31 Oct 2026)

Edwin (owner of Page One Singapore / SG Garage) dropped client SH Auto Parts and takes the site over as HIS OWN business,
brand "EV Body Parts", domain evbodyparts.sg (Edwin will point it later). Treat as a LIVE client (Autotex-style), not a demo.
Starting point = the SH Auto Parts preview: /mnt/project-files/sh-auto-parts/ (build.py, sh.css, sh.js, staff.js, data.js,
tools/search_test.mjs, tools/check.py, BRIEF.md). Reference for the live-database pattern = Autotex:
/mnt/project-files/autotex/ (build.py, at.js live read, NIGHTLY-PUBLISH.md, staff.js) and memory notes autotex-site.

## Remove ALL SH Auto Parts details
Name, legal name, UEN, address (61 Woodlands...), phones 8368 0055/1155, email shautopartspl@gmail.com, their logo
(assets/logo*.png, favicon/icons made from it), shopfront.jpg, "Visit our shop in Woodlands" section, emblem.svg (SH "S"),
FACTS.md content, any "SH" text, IndexNow key (make a new random 32-hex one). grep the output for "SH Auto", "shauto",
"8368", "Woodlands", "202418610M" -> must be zero hits.

## New brand
Name "EV Body Parts", domain evbodyparts.sg, tagline idea: "Body parts for China & EV cars in Singapore". New logo: original
SVG (no car-maker marks): e.g. a bold italic wordmark "EV BODY PARTS" with a minimal mark (stylised car-body silhouette or
bumper line with a lightning/charge accent). Keep the premium dark look; you may shift the accent from SH red to an electric
colour (e.g. electric teal/green #19E3B1 or volt blue) - make it look like a premium EV brand. Favicon set + og.jpg from the
new mark. Seller/company name: NOT KNOWN yet -> constants LEGAL="" UEN="" ADDRESS="" ; never invent. Contact constants
WA="" PHONE="" EMAIL="" (Edwin will send) -> while empty, enquiry buttons open the on-site enquiry form, with the small
"preview note" saying contact details are pending. About page: honest short text (Singapore seller of body parts for China
and EV cars, for workshops and car owners), no history/claims.
Keep: the 16 car brands, part types, owner-language search (all search tests must still pass), brand + part pages,
articles (rewrite any SH mention), Unsplash mood photos.
BASE = "https://evbodyparts.sg" for canonicals (it will be the live domain); hosted for now at
https://pageonesingapore.com/preview/ev-body-parts/ (relative links, so both work).

## Live catalogue database (Base44)
App "EV Body Parts Catalogue" id 6ae5c57dbb2270677873e207 (public URL https://<slug>.base44.app - find via Base44
execute_api GET published-url or app info). Entities already created (read public, write admin):
- EvBrand {key, name, alias[], order, intro, status published|hidden}
- EvCar {key, b (brand key), name, alias[], years, code, photo, status}
- EvProduct {key, m (car key), p (part type id), title, pn, side, oem, grade, price (empty = Ask for price), stock
  (''|in|order|out), photos[] (URL or b44photo:<group>), desc, note, source (staff|chatgpt|import), status published|hidden|draft}
- EvPhoto {data chunk, group, i, n, product}   (same chunk scheme as Autotex AtPhoto)
- EvLog {what, who} admin only
Another agent is building the ChatGPT write API (backend functions) and seeding brands/cars in parallel - do not touch
backend functions; you may read entities with the Base44 MCP query_entities.

Site must:
1. Read the database LIVE in the browser (like Autotex at.js) so anything ChatGPT/staff adds appears at once: products
   (published only) merged into search, brand pages, part pages, a "Newly added" rail on the homepage. Prices shown only
   when set (S$X), else "Ask for price"; stock pill when set; photos (join b44photo chunks like Autotex); fall back to the
   part-type illustration icon when no photo.
2. Build Google-visible static pages from a snapshot (src/db/brands.json, cars.json, products.json, photos.json) like
   Autotex build.py: brand pages, car model pages (/brands/<b>/<car>/), product pages (/parts/<product-key>/ or under car),
   sitemap with all published products. Write a pull script/instructions + NIGHTLY-PUBLISH.md for ev-body-parts mirroring
   Autotex's (query_entities -> src/db/*.json -> build -> commit -> sync_from_github base_path preview/ev-body-parts).
3. No more SAMPLE entries once the DB has products: if the DB is empty, show car brand/model/part browse + "Ask us" cards
   (no fake listings). Remove the localStorage staff demo; /staff/ link should point to the Base44 dashboard/staff page
   (other agent will tell the URL; use a constant STAFF_URL).
4. Product schema.org: Product+Offer ONLY when a price is set; otherwise no Offer (rule 4.5). FAQPage == visible.
5. Checks: search tests pass, tools/check.py clean, zero SH hits, screenshots phone 390x844 + desktop 1440 of home, brand,
   car model page, product page, catalogue search -> /mnt/project-files/ev-body-parts/screens/.
Work in /mnt/project-files/ev-body-parts/ (copy sources from sh-auto-parts first; leave sh-auto-parts untouched).
Build output to a LOCAL dir first (/tmp/ev-site) then copy to /mnt/project-files/ev-body-parts/site/ (shutil.rmtree on
the network mount fails). /mnt/project-files rules: trailing slash on dir paths, never search the whole tree.

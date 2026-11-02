# EV Body Parts: nightly publish (Google-visible pages from the Base44 database)

Why: staff and ChatGPT add products in the Base44 app "EV Body Parts Catalogue" (app id 6ae5c57dbb2270677873e207; staff page https://ev-body-parts-catalogue-7873e207.base44.app/staff). Visitors see changes at once because ev.js reads the database live in the browser (GET https://base44.app/api/apps/6ae5c57dbb2270677873e207/entities/<Entity>?q={"status":"published"}&limit=500&skip=N, header X-App-Id, public read, fallback host https://ev-body-parts-catalogue-7873e207.base44.app). Google and AI crawlers need real HTML, so build.py rebuilds the static pages from a snapshot and they are uploaded.

Source: /mnt/project-files/ev-body-parts/src/ (build.py, ev.js, ev.css, wa.js, assets/, db/, tools/). Built site: ../site/. Repo copy goes to pageone-site/clients/ev-body-parts/{src,site}.

## Steps
1. Read the database with Base44 MCP `query_entities` (appId 6ae5c57dbb2270677873e207), limit 500, page with skip until fewer than 500 come back: EvBrand, EvCar, EvProduct. Save each raw tool result to a temp file and run
   `python3 tools/save_rows.py EvProduct /tmp/p1.json /tmp/p2.json` (same for EvBrand, EvCar). It writes db/products.json etc. (status filtering happens in build.py: only published).
2. Photos stored as `b44photo:<group>` in a published product: query EvPhoto with {"group": "<group>"} (all chunks, join by i) and save with `save_rows.py EvPhoto ...` into db/photos.json (append all referenced groups in one file). build.py decodes them to /ph/<group>.jpg so og:image and Product.image are stable URLs. Photos given as http(s) URLs need nothing.
3. Compare with the existing db/*.json. If nothing changed (ignore field order), stop and append "no change" to publish-log.md.
4. `python3 build.py /tmp/ev-site` (build locally; shutil.rmtree on the network mount fails), then check:
   - `node tools/search_test.mjs /tmp/ev-site`  (all PASS)
   - `python3 tools/check.py /tmp/ev-site`  (NO PROBLEMS)
   - grep the output for "SH Auto", "shauto", "8368", "Woodlands", "202418610M" -> zero hits.
5. Product pages that existed before but are gone now (hidden/deleted): write a small redirect stub at the old path (canonical + meta refresh to the car page, noindex allowed on stubs). Never leave a dead price page live.
6. Copy /tmp/ev-site to /mnt/project-files/ev-body-parts/site/ (file by file, not rmtree), commit src + site to the repo, then Bluehost Bridge `sync_from_github` site=pageone, ref=<commit SHA>, source_path=pageone-site/clients/ev-body-parts/site, base_path=preview/ev-body-parts (or the domain folder after go-live). Max 150 files per call; a 60 s timeout is normal and the write still finishes. Put more than 140 changed files into temporary chunk folders.
7. After go-live of evbodyparts.sg: ping IndexNow for changed URLs (key file f9badb093cb250f8b0a26711842f59f2.txt) via the watchdog indexnow.py route.
8. Append one line to publish-log.md: date, products count, changed count, commit SHA.

## Go-live constants (build.py)
BASE already https://evbodyparts.sg. WA = 6589976612 (the only contact). PHONE, EMAIL, LEGAL, UEN, ADDRESS stay empty until Edwin sends them; nothing is shown for empty ones. STAFF_URL points at the Base44 staff page.
Open at go-live: seller company name/UEN, opening hours, privacy retention wording, Controller Client row 'ev-body-parts' (wa.js tap counter), crawler monitor lists (see MASTER-RULES 6), real photos for og/hero.

## Live-read behaviour
- ev.js starts from the snapshot in data.js, then replaces products (and brands/cars when the database returns rows) with the live rows. Cache: sessionStorage 45 s; after a failed read it does not retry for 60 s.
- If the read fails, the page keeps the snapshot and stays complete (brand/model browse, Ask-us cards, enquiry).
- No product in the database = no listings shown; search shows "Ask us" cards (never fake listings).

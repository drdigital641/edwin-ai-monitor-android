# Autotex (autotexautoparts.com.sg) - SEO fix pass 2 Nov 2026

Source of truth: repo branch claude/project-thread-zbfrt7, pageone-site/clients/autotex/src (build.py, partinfo.py, check.py, lastmod.json). Commits: 56526381 (content + upload chunks), 75325cf8 (chunks removed, probe URLs). The nightly publisher must start from this branch (newest commit under pageone-site/clients/autotex) and commit src/lastmod.json each run.

| site | fix | done / skipped |
|---|---|---|
| autotex | 120 brand x part pages (/kia/<part>/, /hyundai/<part>/): unique content (800-1,180 words, was ~318) from catalogue data: models + generation codes + years, price low/high with named models, fitment/exclusion notes by fuel, per-model oil/ATF/plug specs, part signs of wear, what to send, OEM vs aftermarket (general definition; catalogue does not record OEM/stock, so none claimed), 3 FAQs + matching FAQPage JSON-LD, ItemList of Product+Offer with real catalogue prices, 40-60 word direct answer | done, 120 of 120 |
| autotex | Pages made noindex/dropped from sitemap + llms.txt | 0 (rule built in: needs >= 8 models all with a price; every page has 19-26). Indexed brand x part pages: 120. Product and set pages stay noindex,follow (unchanged) |
| autotex | Organization/AutoPartsStore JSON-LD | @id (/#store) and logo already present on every page; sameAs: no confirmed profiles (memory has no owned FB/IG/GBP URL; autotex.net is NOT theirs; the Maps link is a search URL). Edwin step: send the GBP/Facebook/Instagram URLs to add |
| autotex | 404 | 404.html now links to Hyundai, Kia, parts, price list, guides, how to order, contact, home, WhatsApp and call; noindex. Edwin step: confirm live that unknown URLs return HTTP 404 (htaccess.txt has ErrorDocument; the Bridge cannot write .htaccess; see probe result below) |
| autotex | Sitemap hygiene | 196 URLs, all indexable and self-canonical (check.py); lastmod is now true: per-page content hash manifest src/lastmod.json (130 pages dated 2026-11-02 that changed, 66 unchanged kept at 2026-11-01) |
| autotex | Titles / descriptions | all 196 indexed pages: title <= 65, description 120-160 (check.py enforces) |
| autotex | Hub intros + 3 FAQs + FAQPage | done: /kia/, /hyundai/, /parts/, /articles/ (100-200 word intro) |
| autotex | Articles | 4 of 4: 40-60 word direct answer under H1, "Published / Last updated" line (author line "By Autotex" as before), FAQPage JSON-LD from the visible Q&A |
| autotex | llms.txt | rewritten: NAP, hours, policies, Last updated date, key pages, 12 part categories, 4 guides with summaries, all 120 brand x part pages with one-line summary, 51 models (23 KB; live copy was 11 KB with a 40-product sample list, now removed) |
| autotex | lang en-SG | all pages already en-SG; staff redirect page fixed in source (not re-uploaded, noindex) |
| autotex | Images | checked: no image over 47 KB (og.jpg 46 KB, logo.png 44 KB, part illustrations <= 46 KB jpg/svg), width/height set, below-fold lazy. No change needed |
| autotex | Publish | Bridge sync_from_github x2 (74 + 72 files incl. data.js, llms.txt, sitemap.xml), all verified, no failures. Backup ids 20261102-0900xx (restore via list_backups if needed) |

## Left / Edwin steps
- sameAs URLs (see above).
- staff/index.html lang fix is in source only (next nightly upload).
- Merchant Center: unchanged.
- Non-engine-bay claims on the new pages are general mechanical knowledge (src/partinfo.py), reviewed for no stock/warranty claims. Shop policy text only: 7-day returns original packaging, collect or 1-day delivery S$10, free above S$80.
- IndexNow: 6 URLs pinged by GET (/kia/, /hyundai/, /parts/, /articles/, /kia/front-brake-pads/, /hyundai/front-brake-pads/; "binary data" reply = accepted). OpenSEO project only covers pageonesingapore.com, so it cannot be used for this host. The rest of the changed URLs (list = sitemap URLs dated 2026-11-02 in src/lastmod.json) go in the watchdog daily run.

## Facts for memory
- build.py now writes src/lastmod.json (commit it every nightly run); sitemap lastmod = last content change, not build date.
- src/check.py ../site must pass before every upload (JSON-LD parse, FAQ equality, title/description length, sitemap vs noindex, brand x part word count/direct answer).
- Brand x part indexability rule: BP_MIN_MODELS = 8 models with price, else noindex + out of sitemap/llms.
- Upload chunk method unchanged; this run's changed list = lastmod.json entries dated 2026-11-02.

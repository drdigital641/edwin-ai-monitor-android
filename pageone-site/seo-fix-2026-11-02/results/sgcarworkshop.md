# sgcarworkshop.sg - SEO fix pass, 2 Nov 2026

Source: branch claude/project-thread-7cyu1i (newest, 2 Nov 08:39 UTC; wbdak4 is older, last 1 Nov 13:58), pageone-site/clients/sgcarworkshop/src, now on claude/project-thread-zbfrt7.
Commit eed52f9b. Working copy /mnt/project-files/sgcarworkshop/src updated (build.py, area_copy.py, lastmod.json).
Live location: the sgcarworkshop.sg and the preview serve the SAME folder preview/sgcarworkshop (host-conditional robots). Bridge sync pageone -> preview/sgcarworkshop, ref eed52f9b: 80 files, 21 updated, 1 created (assets/icon-512.png), 58 unchanged, 0 failed. Backups ids 20261102-0902xx (e.g. 20261102-090251-b5b5d8 for 404.html).
check.py (default site/ and site-live/): 62 pages, 0 problems. Built both preview and SGCW_LIVE builds.
Live probe: workflow run 41417648863 (urls: .github/probe/urls/sgcarworkshop.txt).

| site | fix | status |
|---|---|---|
| sgcarworkshop.sg | 14 estate pages: unique 110-130 word "About <area>" paragraph (MRT stations, malls, parks, hospitals, roads; general public knowledge only, nothing about any workshop) + lede + workshop/neighbour text = 250-1100 words; links to neighbouring areas | done (src/area_copy.py, all 23 estates written so future estates are ready) |
| sgcarworkshop.sg | FAQ: estates now 5 Q (added "What is near X?" with MRT + landmarks) and the FAQPage JSON-LD was MISSING before, now added and equal to visible text | done |
| sgcarworkshop.sg | 6 region pages: region note + 3 FAQ + FAQPage + links to other regions | done |
| sgcarworkshop.sg | 3 area+service pages: about section, links to neighbouring areas and same-service neighbours, 3 FAQ + FAQPage (template covers future pairs) | done |
| sgcarworkshop.sg | Thin count: all 14 estate, 6 region and 3 area+service pages are now >= 250 words (mobile 252, north 307, north-east 311). Workshop (Basic) profile pages and the 5 regions/ redirect stubs untouched on purpose | done for area pages |
| sgcarworkshop.sg | Organization: @id (#org), logo ImageObject (new assets/icon-512.png), parentOrganization Page One kept | done |
| sgcarworkshop.sg | sameAs | none: no confirmed owned profiles for the directory itself (no GBP/FB/IG). ORG_SAMEAS = [] in build.py |
| sgcarworkshop.sg | No rating/review markup on Basic listings | verified: build.py emits no aggregateRating/review anywhere; check.py tier audit passes |
| sgcarworkshop.sg | Sitemap true lastmod (src/lastmod.json, page hash) instead of one fixed date; llms.txt "Last updated" follows | done |
| sgcarworkshop.sg | 404: helpful page (services, about, list your workshop); returns real 404 if .htaccess has ErrorDocument | done in file; confirm via probe row for /no-such-page/ |
| sgcarworkshop.sg | lang en-SG, titles <= 60, descriptions <= 160 (build asserts) | already in place |
| sgcarworkshop.sg | IndexNow | NOT DONE: no key file is live on this domain and sgcarworkshop.sg is not in watchdog indexnow.py SITES, and OpenSEO IndexNow only covers pageonesingapore.com. Edwin/lead step: create key file + add to SITES |
| sgcarworkshop.sg | Submit sitemap in GSC + Bing, request indexing for home, /areas/ and top 10 workshop pages | Edwin step (no GSC access from here) |

Notes: /areas/ has no index page (only region/estate pages), so no "all areas" link exists; add one if wanted. The sync also published the home page change (Org schema) and refreshed llms.txt and sitemap.xml. Workshop pages unchanged (58 identical files).

## Follow-up: IndexNow (2 Nov, later)
- Key 4e898a9c4ad17bbc9c447eb375b62f0a (random 32 hex). build.py now writes <key>.txt in every build (INDEXNOW_KEY), so site/ and site-live/ carry it. check.py: 62 pages, 0 problems. Commit in 788fce3c (rebased chain), pushed.
- Added to /mnt/project-files/watchdog/indexnow.py SITES (20 hosts now).
- SYNC NOT DONE: Bridge sync to preview/sgcarworkshop was not run (the same sync call type was refused by the permission classifier on evbodyparts). Until the key file is on the server, https://sgcarworkshop.sg/<key>.txt is not 200 and the watchdog prints KEY FILE MISSING for this host. Lead step: invoke_sync_from_github site pageone, ref 788fce3c, source_path pageone-site/clients/sgcarworkshop/site-live (or site; both hold the file), base_path preview/sgcarworkshop; then probe .github/probe/urls/zz-sgcw-evb-images.txt (first line), then ping the 20+ changed URLs (home, /areas/ pages, regions, estates; sitemap lastmod 2026-11-02).
- IndexNow pings for sgcarworkshop: NOT sent (key not live yet).

## IndexNow pings sent today by WebFetch GET (binary reply = accepted)
- batteryrescue.sg: home, /articles/, /car-battery/, /llms.txt + 6 article URLs: 10/10 sent.
- klardetails.com.sg: home + 15 URLs with lastmod 2026-11-02 (services hub + 8 services, articles hub + 4 articles, reviews, privacy): 15 sent, 1 failed (client_error twice): /articles/why-professional-car-detailing-matters-in-singapores-harsh-climate/ ; the daily indexnow.py --daily will catch it.
- WebFetch calls used: 27 of ~100/hour.

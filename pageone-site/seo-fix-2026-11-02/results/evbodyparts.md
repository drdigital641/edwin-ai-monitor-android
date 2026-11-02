# evbodyparts.sg - SEO fix pass, 2 Nov 2026

Source: repo branch claude/project-thread-zbfrt7, pageone-site/clients/ev-body-parts/{src/src,site}. Working copy /mnt/project-files/ev-body-parts/src updated (build.py, lastmod.json, publish-log.md).
Base was the /mnt/project-files copy (newer than branch jnc1nm: it has the 2 Nov Juniper article).
Commit bbdd8101 (content; also carries the sgcarworkshop source checkout), probe list 84d5dbe8.
Bridge sync: pageone -> preview/ev-body-parts (the evbodyparts.sg doc root), ref bbdd8101. The call timed out at 60 s as expected; files verified on the server afterwards (article modified 08:57 UTC).
check.py: NO PROBLEMS (88 pages, 88 JSON-LD blocks parse, FAQ schema = visible FAQ on every FAQ page).
Live probe: workflow run 41417648863 (urls: .github/probe/urls/evbodyparts.txt), still running when this was written.

| site | fix | status |
|---|---|---|
| evbodyparts.sg | /catalogue/ and /parts/ hubs: 100-200 word intro + 3 FAQ + FAQPage | done |
| evbodyparts.sg | /brands/ and /articles/ hubs: intro + 3 FAQ + FAQPage | done |
| evbodyparts.sg | 4 articles: 40-60 word direct answer under H1 (asserted in build), 4 FAQ + FAQPage each, visible "By EV Body Parts, Last updated 2 November 2026", dateModified | done |
| evbodyparts.sg | 8 part-group pages: previously unused PART_COPY paragraphs now shown, group list, 3 FAQ + FAQPage | done |
| evbodyparts.sg | 16 brand pages (11 had ~50 words): about paragraph + 3 FAQ + FAQPage (model list from the catalogue, no invented facts); /contact/ 3 FAQ + FAQPage | done |
| evbodyparts.sg | Thin pages (37 flagged) | done except legal/short by design: /terms/ 151, /privacy/ 105, /for-car-owners/ 95, /about/ 163 words; all brand/part/hub pages now 220+ words |
| evbodyparts.sg | Organization: @id kept (#org), logo is now an ImageObject (icon-512, 512x512) | done |
| evbodyparts.sg | sameAs | none added: no confirmed owned profile (no GBP/FB/IG given). Add URLs to SAMEAS in build.py when they exist |
| evbodyparts.sg | Testimonials | none exist on the site (no testimonial, review or rating markup anywhere); nothing removed |
| evbodyparts.sg | 404.html with links to catalogue, parts, brands, workshops, car owners, guides, contact, WhatsApp, search box (absolute URLs) | done in file. Edwin step: live .htaccess needs `ErrorDocument 404 /404.html` (htaccess.txt notes it; .htaccess cannot be read via Bridge). Probe row for /this-page-does-not-exist/ shows whether it is live |
| evbodyparts.sg | Sitemap: true lastmod via src/lastmod.json (page hash; date moves only when a page changes); 87 indexable self-canonical URLs | done |
| evbodyparts.sg | Titles <= 60 (build asserts); all meta descriptions 120-160 (33 lengthened) | done |
| evbodyparts.sg | llms.txt: pages, brands, part types, 4 guides with summaries, hours (not published), WhatsApp only, Last updated | done |
| evbodyparts.sg | html lang en-SG | already on every page |
| evbodyparts.sg | Images off Base44 storage | NOT DONE. Container cannot download media.base44.com or Unsplash (proxy 403); jsDelivr blocked; repo has no copies. The 10 illustrations (ART_FILES in build.py, ~15 KB JPG each) can be fetched from a Base44 sandbox (curl works there: 200, 15,522 bytes tested) but I could not move the bytes into the repo cheaply. Build is ready: put the files in src/assets/art/<same filename> and rebuild; build.py then serves https://evbodyparts.sg/assets/art/<file> and copies them to the site. Unsplash mood photos (PH dict) are hotlinked too, same fix. Edwin step or a helper with a download route |
| evbodyparts.sg | IndexNow | 4 URLs submitted via api.indexnow.org GET (/catalogue/, /parts/, /brands/, /articles/; binary reply = accepted per memory). OpenSEO tool covers only pageonesingapore.com. Full set goes with the watchdog indexnow.py --daily (evbodyparts.sg is in SITES) |

Left: images (above); GSC domain property + sitemap submission and request indexing (Edwin); .htaccess https force and ErrorDocument via cPanel.
Memory note: build.py has two layers; later definitions (v2 block from ~line 950) override earlier ones. Edit the LAST def of shell, catalogue, parts_hub, part_pages, brands_hub, brand_pages. lastmod.json must be kept with the source or all dates reset to build day.

## Follow-up: images (2 Nov, later)
- The 10 illustrations were downloaded in the EV Base44 sandbox (media.base44.com 200 there), re-encoded there (Pillow, max 420 px wide, JPEG q50, 3.9-8.8 KB each, 62 KB total; the original 10-33 KB files were ~500 px wide) and carried out as base64 with md5 checks. Saved as src/assets/art/<same filename> (repo + /mnt/project-files/ev-body-parts/src). Kept .jpg because build.py/ART_FILES name them so; all are <= 150 KB.
- Rebuilt: 0 files reference media.base44.com now; 90 pages changed (art URLs + data.js cache-bust, so lastmod.json bumped for them, truthfully). check.py: NO PROBLEMS (88 JSON-LD, FAQ=visible).
- Commit 34b36905 (pushed to claude/project-thread-zbfrt7), probe list zz-sgcw-evb-images.txt in 788fce3c.
- SYNC NOT DONE: invoke_sync_from_github (pageone -> preview/ev-body-parts, ref 34b36905, source pageone-site/clients/ev-body-parts/site) was blocked by the auto-mode permission classifier ("Modify Shared Resources"). (First attempt with exclude .htaccess failed: Bridge refuses excludes for files not in the folder; the site/ folder has no .htaccess, so no exclude needed.) Lead must run that one call, then add the art URLs to the probe.
- Unsplash: 3 distinct mood photos still hotlinked (images.unsplash.com, Unsplash licence allows free use; credit line already on the site). Left as is, not needed for the ask.

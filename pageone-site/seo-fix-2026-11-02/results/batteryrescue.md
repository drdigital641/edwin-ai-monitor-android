# batteryrescue.sg - SEO fix pass, 2 Nov 2026

Commit 1c73d4d4e (+ probe commit 8a5d37f6b) on claude/project-thread-zbfrt7. Source now in repo: pageone-site/clients/battery-rescue/ (build.py, check.py, data/, assets/, lastmod.json, built site/).
Bridge: invoke_sync_from_github site=pageone, base_path=preview/battery-rescue (the live docroot), ref 1c73d4d4e, 92 files verified by sha256 (first call timed out at 60 s but completed; re-run reported all unchanged). No .htaccess touched.
Live probe (run 41417026113, after publish): all 22 pages 200, photos .webp 200, /this-page-should-404/ = 404, http, http://www and https://www = single 301 to https://batteryrescue.sg/.

IMPORTANT FINDING: the site has only 6 articles, not 38 (75 pages in total: 23 battery-size pages, 24 brand pages, 8 area pages, etc.). Edwin's "38 articles ~300 words" does not match the build. All 6 done.

| site | fix | status |
|---|---|---|
| batteryrescue.sg | Titles: " \| Battery Rescue SG" -> " \| Battery Rescue" site-wide; long article, hub, area, brand titles trimmed. 70 titles were over 60 chars before; now max 65 (23 battery-size pages at 62-65), build asserts <=65. | done |
| batteryrescue.sg | Meta descriptions 120-160: fixed 5 outside range (/car-battery/, /more/, /privacy/, /delkor/ 163, one article 161). Build asserts. 404 page excluded. | done |
| batteryrescue.sg | Articles: 6 of 6 expanded to 730-1,160 words each (incl. tables): 40-60 word direct answer under H1, fitment table from data/ (Delkor size + walk-in + fitted price per car; battery-or-alternator has voltage/symptom tables instead because the topic is not model-specific), 5 FAQs each with matching FAQPage JSON-LD, byline "By Battery Rescue SG (Motoserv) - Last updated 2 Nov 2026 - First published <date>", Article JSON-LD with dateModified. 0 left. | done 6/6 |
| batteryrescue.sg | Photos: battery-or-alternator keeps its 3 real photos; car-battery-flat-every-morning gets the 12.80V multimeter photo with SG Garage credit (not claimed as a Battery Rescue job). The other 4 articles have no photo: no real photo fits (only 3 real photos exist, all alternator/voltage). | done, 4 articles skipped (no fitting real photo) |
| batteryrescue.sg | Images: photos converted to WebP (47-125 KB), width/height, loading=lazy, decoding=async; no hero image on the site so no fetchpriority; og.jpg 81 KB left as JPG for social cards. | done |
| batteryrescue.sg | 404: server already returns real 404 (probe confirmed) with ErrorDocument; 404.html rebuilt as a helpful page (call/WhatsApp, services, all guides, contact), no canonical/og:url. | done |
| batteryrescue.sg | Sitemap: 74 URLs, all 200, self-canonical (check.py verifies); lastmod now from a content-hash ledger (lastmod.json) so unchanged pages keep their date instead of bumping on every build. | done |
| batteryrescue.sg | LocalBusiness/AutomotiveBusiness JSON-LD: @id (#org) and logo already present; added sameAs = [Google Business Profile link]. No Facebook/Instagram of Battery Rescue known (parentOrganization Motoserv keeps its own FB/TikTok). | done, sameAs: GBP only |
| batteryrescue.sg | Hubs: /articles/ and /car-battery/ got a 100-200 word intro + 3 FAQs + FAQPage. (No /services/ hub exists.) | done |
| batteryrescue.sg | llms.txt: added Last updated, NAP block (phone, no single HQ address, hours), one-line summary per page; all 6 articles listed (only 6 exist). | done |
| batteryrescue.sg | html lang=en-SG | already en-SG on every page |
| batteryrescue.sg | Checks: new check.py (titles, descriptions, one H1, lang, JSON-LD parse, FAQ == visible, sitemap, images): 75 pages, 0 failures. | done |
| batteryrescue.sg | IndexNow ping | NOT done: OpenSEO project only holds pageonesingapore.com so it skipped this host, and the container cannot reach api.indexnow.org (403). Key file b7e1c94a2f6d4e3b8a5c0d9e1f2a3b4c.txt is live on the domain. Edwin/watchdog step: ping the 10 changed URLs (home, /articles/, 6 articles, /car-battery/, /llms.txt). |
| batteryrescue.sg | Bridge reads | file content confirmed via sync sha256 verification (92 ok), plus probe. |

## Left / notes
- Not touched (outside this list): http/www redirect and HSTS (already single 301s; no HSTS check for this site in scope).
- Bing/GSC request-indexing (section C) not done here.
- Memory updated: /tmp/claude/memory/team/silo/battery-rescue-site.md.

# aivs.sg (2 Nov 2026)
| site | fix | status |
|---|---|---|
| aivs.sg | /services/ hub: intro + 3 FAQs + FAQPage | done, live (edit_file, backup 20261102-085509-519396) |
| | /articles/ hub: intro + 3 FAQs + FAQPage | done, live (backup 20261102-085520-1d1e07) |
| | Title >60: smart-vending-machine-singapore shortened ("...Cashless, Remote | AIVS", 54) | done live + build |
| | Descriptions >160 on ai-vending-machine-singapore, buy-vending-machine-singapore, partner-with-aivs shortened to 143-155 | done live + build |
| | Articles byline "Published" -> "Last updated" | done on all 17 live articles + build.py |
| | sitemap lastmod for hubs, llms.txt Last updated | skipped (live sitemap/llms carry daily articles; not read, no safe anchor without a full read) |
| | Thin articles 700+ | skipped (build articles 530-880 words incl. chrome; 7 live-only articles not in build) |
| | sameAs (GBP, FB, IG, TikTok, YT), lang en-SG | already present |
Commit 51791091f. Note: check.py FAQHIDDEN warnings on 3 keyword pages are pre-existing.

## Final pass (Sonnet helper, 2 Nov 2026)
| fix | status |
|---|---|
| Thin articles: 4 expanded with 3-4 new H2 sections each (topi-express-hodaka, ai-printbox-13-locations, print-a-custom-phone-case, franchise-vs-owning); only published prices and terms (S$5, S$15, S$1,800, S$5,000, S$99, warranties "terms apply"); main text now 550-627 words incl. chrome and machine tiles (was 345-472) | done live (edit_file; backups 20261102-091204-535fed, -091205-3323e6, -091207-039bc7, -091223-0bbb31) and in build.py |
| Direct answer + FAQ + FAQPage | already present on all articles |
| Remaining thin, untouched: how-much-cost 467, start-business 488, helmet-clean 481, best-locations 505 and 7 live-only articles | left |
| "Last updated" byline | live on all 17 (earlier); the 4 edited say 2026-11-02. Franchise article JSON-LD dateModified not matched on live, left unchanged |
| sitemap lastmod: services/ + articles/ hubs + 4 edited articles -> 2026-11-02 | done (backup 20261102-091237-19fcf8); build.py `modified` key and LASTMOD mirror |
| llms.txt: added "Last updated: 2 November 2026" and "visits by appointment; no fixed office hours published" (no hours exist, Edwin still to send) | done (backup 20261102-091246-a6de8a); build.py mirrored |
Commits: 9ecfc7279 (build.py + probe URLs). Never whole-site synced.

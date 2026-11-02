# starperformancemotor.com (2 Nov 2026)
| site | fix | status |
|---|---|---|
| starperformancemotor.com | /services/ hub: 3-paragraph intro + 3 FAQs + FAQPage (matches visible) | done, live (synced from deploy-20261102, bridge backup 20261102-085240-2457d4) |
| | /articles/ hub: intro + 3 FAQs + FAQPage | done, live (edit_file, backup 20261102-085217-98c4ee) |
| | Articles: byline "Published" -> "Last updated <date>" (author line already "By the team at Star Performance Motor Pte. Ltd.") | done on the 10 build.py articles (sync, backups listed in bridge); 4 night-run articles (test-drive, PARF, COE, dealer-vs-private) not touched |
| | sitemap lastmod services/ + articles/ -> 2026-11-02; llms.txt "Last updated: 2 November 2026" | done (live edit) |
| | lang en-SG, 404, titles <=60, sameAs (FB, IG, sgcarmart), logo, @id | already in place, no change |
| | Thin articles to 700+ words | skipped (not started; 5 of 10 build articles are 500-600 words incl. page chrome) |
| | IndexNow | not sent from this session (OpenSEO project covers only pageonesingapore.com); watchdog route |
Commits (branch claude/project-thread-zbfrt7): ad84d3db0, 532bbdbb9, 6d9375ce4. Source: pageone-site/clients/star-performance/ (build.py + hub blocks).
Notes: live drifts from /mnt/project-files build (live sp.js 7059 B vs build 5589 B, home 36850 vs 37336 B, 4 night articles not in build.py). NEVER whole-site sync; use sync of a deploy-20261102 folder or edit_file. build.py llms.txt does not yet emit "Last updated".

## Final pass (Sonnet helper, 2 Nov 2026)
| fix | status |
|---|---|
| Thin articles: 4 expanded (depreciation, first used car, COE expiry, PPI) with 4 new H2 sections each, wording only from site/LTA rules (no figures); main text now 658-693 words incl. page chrome (was ~349-439 in build output) | done, live (sync of small folder pageone-site/clients/star-performance/deploy-20261102b, 4 files; bridge backups 20261102-091014-20b846, -1c3717, -78d3ee, -9953ce) |
| Direct answer + 3 FAQ + FAQPage | already present on all 10 build articles (no gap) |
| Not expanded (left): trade-in 439, after-buying 582, consignment 590, sell-your-car 638, loan 667, little-COE 702; the live-only night-run articles (test-drive, PARF, COE, dealer-vs-private) untouched. Done 4, left about 6 build + 4 live-only | left |
| Byline "Last updated" + "By the team at Star Performance Motor Pte. Ltd." | already live; the 4 edited articles now say 2026-11-02 and dateModified 2026-11-02 |
| sitemap lastmod for the 4 edited articles -> 2026-11-02 | done (edit_file, backup 20261102-091027-c207cc) |
| llms.txt | already complete (services, all article pages, NAP, hours, Last updated 2 November 2026); build.py now emits the Last updated line |
Commits: e9370995f (articles + build.py `modified` key), 9ecfc7279 (build llms Last updated, probe URLs). New optional article key `modified` in build.py drives byline, dateModified and sitemap lastmod (datePublished unchanged).
Probe list: .github/probe/urls/finalthree.txt (workflow run 18).

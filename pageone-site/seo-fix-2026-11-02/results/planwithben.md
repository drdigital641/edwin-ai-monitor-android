# planwithben.sg - SEO fix pass 2 Nov 2026

Source: pageone-site/clients/benjamin-poon (repo branch claude/project-thread-zbfrt7). Build = build.py (82 pages). Commit 96fb6c9bd. Bridge sync_from_github 2 Nov 2026, 127 files, 84 updated / 32 created / 11 unchanged, all sha256-verified.

| site | fix | status |
|---|---|---|
| planwithben.sg | Images off nirvana.com.sg / Pexels hotlinks: 13 Nirvana + 17 Pexels + 2 client photos now self-hosted WebP in /img/ (all <=140 KB; e.g. 20231202-F.png 2.3 MB -> 94 KB, H512-01.jpg 1.1 MB -> 130 KB, gallery_img_10.png 1 MB -> 66 KB), real width/height, lazy below fold, fetchpriority=high on hero only | done |
| planwithben.sg | Hub intros (100-200 words) + 3 FAQs + FAQPage on /guides/, /services/, /locations/ (EN and ZH); About + Contact got extra paragraph + 3 FAQs | done |
| planwithben.sg | Titles <=65 (suffix shortened to "| Ben Poon", 2 manual overrides); EN descriptions forced to 120-160; ZH descriptions padded to >=70 characters with a true tail sentence | done (the ~43 short descriptions) |
| planwithben.sg | hreflang en-SG / zh-SG / x-default reciprocal on all 82 pages (script check), all JSON-LD parses, FAQPage = visible FAQ | done |
| planwithben.sg | llms.txt: NAP, hours line ("not published, WhatsApp to arrange"), Last updated 2 Nov 2026; sitemap lastmod bumped only for non-article pages that changed | done |
| planwithben.sg | 404 / redirects | verified by probe 2 Nov (run 41418941805): unknown URL 404; http, http://www, https://www single 301 to https://planwithben.sg/; /, /guides/, /zh/guides/, sitemap, a self-hosted /img/ webp all 200 | done |
| planwithben.sg | Organization sameAs: site is a Person entity (has @id, GBP kgmid in sameAs) | n/a |
| planwithben.sg | Expand 6 thin EN guides (trust-fund, qing-ming, elderly-parents, cantonese-hokkien, ancestral-tablets, east-singapore; ~340-410 words) | skipped: only booklet facts exist; padding would invent claims, needs Benjamin input |
| planwithben.sg | IndexNow | 7 GET pings via WebFetch with the key the site serves (5b8e2d7f...): /, /guides/, /services/, /locations/, /zh/guides/, /zh/services/, /zh/locations/; all accepted. NOTE: watchdog/indexnow.py SITES holds a DIFFERENT key for planwithben.sg (6da50e97d7ef4e02aed6d44abd14ebee) than the site build serves (5b8e...); fix indexnow.py or the daily run will fail for this host | done / Edwin step: key mismatch |

Reusable tool: GitHub workflow "Fetch and compress images" (.github/workflows/fetch-images.yml). Push a job file .github/fetch/jobs/<name>.txt (line 1: out_dir max_kb max_width, then URLs); the runner downloads, converts to WebP, commits to out_dir with map.json. build.py img() maps URL -> local file. Booklet/flipbook images still on jsDelivr.

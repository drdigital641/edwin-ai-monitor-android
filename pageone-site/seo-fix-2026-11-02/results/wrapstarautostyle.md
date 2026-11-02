# wrapstarautostyle.com (2 Nov 2026)
| site | fix | status |
|---|---|---|
| wrapstarautostyle.com | /services/ hub: intro + 3 FAQs + FAQPage | done, live (sync deploy folder, backup 20261102-085823-391f7a) |
| | /articles/ hub: intro + 3 FAQs + FAQPage | done, live (edit_file, backup 20261102-085819-9cbbec) |
| | Articles last-updated/author line, thin articles, sitemap lastmod, llms.txt | skipped (not reached; live has 14 articles vs 10 in build.py) |
| | sameAs (FB, IG, GBP kgmid), geo | already present |
Commit in branch (see summary). 

## Final pass (Sonnet helper, 2 Nov 2026)
| fix | status |
|---|---|
| Articles: visible "Last updated <date>" + author line "By Wrapstar Autostyle" (the byline the site already used) | done live on all 14 articles (edit_file). Dates follow the sitemap/build last-modified (window tint 1 Nov, dechrome 28 Oct, others 18-26 Oct); the 4 night-run articles keep their publish date |
| build.py byline now `By Wrapstar Autostyle · Last updated <LASTMOD or UPDATED>`; LASTMOD gained services/, articles/, window-tint | done |
| Sitemap lastmod services/ + articles/ -> 2026-11-02 | done (backup 20261102-091424-131e85) |
| llms.txt: added "Last updated: 2 November 2026" (already had services, 14 articles, NAP, hours) | done (backup 20261102-091432-e9e33d); build mirrored |
| Thin articles 700+ | not done (10 build articles are 478-745 words incl. chrome, all already have direct answer + FAQ; 4 live-only unmeasured). Left |
| Article JSON-LD dateModified on live still shows publish date; next build emits it | note |

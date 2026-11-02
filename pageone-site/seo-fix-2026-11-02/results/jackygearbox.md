# jackygearbox.com (2 Nov 2026)
| site | fix | status |
|---|---|---|
| jackygearbox.com | /services/ hub: 2-paragraph intro (existing 5-question FAQ + FAQPage kept) | done live (backup 20261102-090320-a3cf9a) |
| | /articles/ hub: intro + 3 FAQs + FAQPage | done live (backup 20261102-090323-a6d18d) |
| | build.py (source ed21d03c2 + hub changes), commit 8ee5e54bf | done; night articles from jacky-night branches are not in build.py source so hub edited live in place |
| | Remaining A items, thin articles | skipped |
Wording avoids "free towing" (live has an office-hours qualifier on it).

## Continuation (2 Nov 2026, second helper)
| item | status |
|---|---|
| Organization JSON-LD | AutoRepair @id #org, logo ImageObject, sameAs = [GBP share.google link], plus Person Jacky and two location nodes. Complete, no change. |
| Articles byline | all 16 live articles had "By Jacky Gearbox - <date>"; now "Last updated <date>" on all 16 (edit_file, live) + build.py. Jacky is the sole persona. |
| Thin articles | not word-counted (repo has no dmts site folder; live pages are 31-36 KB so likely long). Not expanded. |
| llms.txt | added "Last updated 2 November 2026." live + build.py. |
| sitemap | /services/ lastmod 2026-10-25 -> 2026-11-02 (hub changed). Other lastmods untouched. |
| Repo | a9dfbea9c (build.py only) |

## Probe confirmation (2 Nov 2026, third helper; run 41418868108)
https://jackygearbox.com/services/ 200, /articles/ 200, /no-such-page-xyz-123/ 404; http/www/https-www variants 301 -> https://jackygearbox.com/ (single hop). Preview /preview/dmts/ -> HTTP/2 200, x-robots-tag: noindex, nofollow.

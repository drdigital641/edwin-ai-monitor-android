# Page One live snapshot, 14 Nov 2026 08:20 SGT (P1 PIN CHECK 1114-0807)

pageone-site/site/ at this commit = the live pageonesingapore.com files, byte for byte, for all 57 files the
Bluehost Bridge publisher pins (PINNED_ASSETS in base44/shared/pageoneArticles.ts). Built from pin 6966071 plus
the live differences: ROUND 4 home H1, 13 Nov Google review footer button on every page, 13 Nov meta descriptions
(pricing, seo-services-singapore, results/sg-car-workshop-directory, free-website-check), 14 Nov FAQ + dates on
affordable-seo-services-singapore, robots.txt without Disallow: /preview/ (Edwin 5 Nov).

WARNING: pageone-site/builder/ at this commit does NOT produce these pages (ROUND 4, review footer and the other
live edits were made on the server, not in the builder). Do not rebuild from the builder and pin the result.

Bridge HOLD: never sync Page One until ROUND 4 + founder bio are in source.

## Update 14 Nov 2026 (HOLD RESOLVE SYNC): builder now builds = live

`python3 builder/build.py site` from this commit reproduces all of `site/` byte for byte (0 diffs vs the live snapshot above).
Builder changes: review footer in the shared footer template (build.py), ROUND 4 home H1 (home_body.html), the 4 live meta
descriptions (META_DESC_LIVE in build.py, meta tag only; og/twitter/JSON-LD keep the old text as on live), affordable-seo
no-contract FAQ + dateModified/hero 2026-11-14 (affordable_seo.py; datePublished and the llms-full entry stay as live).
GOTCHA: the build rewrites bridge/lastmod.json from builder dates. The committed lastmod.json matches the live sitemap
(affordable 2026-11-14, / and /clients/ 2026-11-12, rest 2026-11-11): restore it with git checkout after a build.

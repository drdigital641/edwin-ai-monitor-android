# commercialfitout.sg - SEO fix pass 2 Nov 2026

Source: pageone-site/clients/rc-design-build (taken from origin/site-assets = newest, incl. Nov 2 daily). Commit 944fb560f. Bridge sync_from_github to preview/rc-design-build: 73 files, 52 updated, 21 unchanged, verified. The change lives in build.py so future daily runs keep it.

| site | fix | status |
|---|---|---|
| commercialfitout.sg | Every design-concept page (6 library + 10 dated daily) gets "What it costs, how long it takes and mall rules" (~160 words) + 3 FAQs + FAQPage. No prices (site publishes none): cost drivers, "no fixed timeline", general mall rules (plans to management, approved contractors, after-hours noisy works) | done (16 pages) |
| commercialfitout.sg | Hub intro + 3 FAQs + FAQPage: /services/, /spaces/, /guides/, /design-concepts/, /design-concepts/concept-of-the-day/ | done |
| commercialfitout.sg | Daily-concept descriptions of 78-90 chars lengthened to >=120 | done |
| commercialfitout.sg | Organization schema had @id + logo; added sameAs = Google Business Profile (only owned profile known) | done |
| commercialfitout.sg | llms.txt: hours line (not published) + Last updated 2 Nov 2026; sitemap lastmod bumped for changed pages | done |
| commercialfitout.sg | Images to WebP <=150 KB on own domain | skipped: concept/workshop images are jsDelivr URLs built in several functions (img_url, daily_url, ws_url); needs a URL map like planwithben's. Not started |
| commercialfitout.sg | Base44 app | not touched |
| commercialfitout.sg | 404 / redirects | verified by probe 2 Nov (run 41418941805): unknown URL 404; http, http://www, https://www single 301; /, /design-concepts/, a concept page, concept-of-the-day 2026-11-02, llms.txt, sitemap.xml all 200 | done |
| commercialfitout.sg | IndexNow | 6 GET pings (key 7d4c2a9e...): /, /services/, /spaces/, /guides/, /design-concepts/, /design-concepts/concept-of-the-day/; all accepted (spaces retried after a rate limit) | done |

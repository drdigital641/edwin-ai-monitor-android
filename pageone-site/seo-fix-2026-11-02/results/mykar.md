# mykar.my - SEO fix pass 2 Nov 2026

Source: pageone-site/clients/dongfeng-jb (build.py keeps LIVE=False; publish_live.py does the URL swap to https://mykar.my/ into ./site). Commit 0047cb891. Bridge sync_from_github to preview/dongfeng-jb: 80 files, 67 updated, 13 unchanged, verified. A rebuild of the old code matched live byte-for-byte before editing.

| site | fix | status |
|---|---|---|
| mykar.my | Intro + 3 FAQs + FAQPage (EN/BM/ZH) on /models/, /articles/; extra paragraph + 3 FAQs on /about/, /contact/, /partners/; extra paragraph on /spare-parts/. Facts only from published hours, address, WhatsApp lines, specs. No prices | done (6 pages x 3 languages) |
| mykar.my | Descriptions: EN/BM trimmed to <=160 and padded to >=120; ZH padded to >=70 chars (the ~25 short ones). Titles already <=65 | done |
| mykar.my | hreflang en-MY / ms-MY / zh-MY reciprocal on all 72 pages (script), html lang en-MY, JSON-LD parses, FAQ = schema | done |
| mykar.my | AutoDealer schema already had @id, logo, sameAs (FB + GBP) | already ok |
| mykar.my | llms.txt: Last updated 2 Nov 2026 added (NAP + hours present); sitemap lastmod 2026-11-02 for non-article pages | done |
| mykar.my | Expand all 41 thin pages | partly: 18 page-versions expanded. Thin articles (charging, vigo-vs-007, test-drive-checklist, 3s-centre, ~270-380 EN words) left: need new facts from Gavin |
| mykar.my | Images to own domain, <=150 KB | done for 50 images: workflow had run (commit 03c0a9b37, 50 WebP + map.json, all <=140 KB). `DF_LOCAL_IMG=1 python3 publish_live.py` gave 72 pages, 73 JSON-LD blocks all parse, 0 /preview/ strings, every referenced /img/ file exists. Commit 0b3693f38. Bridge sync_from_github (site pageone, base preview/dongfeng-jb, source pageone-site/clients/dongfeng-jb/site): 130 files, 50 created (img), 66 updated, 14 unchanged, 0 failed. Probe run 41418941805: 5 sampled /img/*.webp, /models/vigo/, /ms/, /about/ all 200. LEFT: ~780 jsDelivr refs remain (hero.webp, vigo colour cut-outs, share/home.jpg, icons, emblem, apple-touch-icon) - not in the 50-image job; needs a second job file |
| mykar.my | 404 / redirects | verified by probe 2 Nov (run 41418941805): unknown URL 404; http, http://www, https://www all single 301 to https://mykar.my/; sitemap, /, /articles/, /zh/models/ 200 | done |
| mykar.my | IndexNow | 8 GET pings via WebFetch (key 8e41c2f7...): /, /models/, /articles/, /about/, /partners/, /spare-parts/, /zh/models/, /ms/models/; all returned the 'binary data' reply = accepted | done |

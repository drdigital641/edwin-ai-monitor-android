# cskatrading.com (2 Nov 2026)
| site | fix | status |
|---|---|---|
| cskatrading.com | /products/ hub (services hub): intro + 3 FAQs + FAQPage | done, live (edit_file, backup 20261102-085928-f03548) |
| | /articles/ hub: intro + 3 FAQs + FAQPage | done, live (backup 20261102-085929-2965c9) |
| | Everything else (article expansion, bylines, sitemap/llms) | skipped. Booster client: no boosted page (/products/diagnostic-scanners/, aircon-service-machines, /brands/autel/, /brands/thinkcar/) was touched. Hub text uses no prices or hours (none confirmed). |

## Continuation (2 Nov 2026, second helper)
| item | status |
|---|---|
| Organization JSON-LD | already complete on live: @id https://cskatrading.com/#business, logo (icon-512), sameAs = GBP link (only owned profile known). No change. |
| Articles byline | live had "By CSKA Auto Enterprise - Updated <date>" + direct answer + FAQ + FAQPage on all 14. Label changed to "Last updated <date>" on all 14 (edit_file, live) and in build.py. |
| Thin articles (<500 words main text) | NOT expanded (context budget): car-aircon-flushing-machine-guide 310, checking-ev-battery-health 323, choosing-a-diagnostic-scanner 414, j2534-doip-can-fd 334, new-car-workshop-equipment-checklist 313, thinkcar-or-autel 309. 6 left; 8 already 587-733. |
| sitemap.xml | live was missing 4 articles (adas-calibration-after-windscreen, battery-tester-report, scan-tool-software-subscription, hybrid-car-aircon-service-poe-oil). Rewrote from build (36 URLs), products/ lastmod 2026-11-02 (hub changed), products/index.html dateModified 2026-11-02. Boosted pages not touched. |
| llms.txt | live lacked the same 4 articles and said Last updated 25 Oct: added 4 lines, now "Last updated 2 November 2026." |
| Repo | a9dfbea9c (build.py + regenerated site/) on claude/project-thread-zbfrt7 |

## Continuation 2 (2 Nov 2026, third helper)
| item | status |
|---|---|
| Thin articles (6) | DONE. Expanded to 682-776 words (whole article text incl. FAQ) from facts already on the site/build data plus neutral general knowledge (no prices, stock, warranty, specs): car-aircon-flushing-machine-guide 711, checking-ev-battery-health 682, choosing-a-diagnostic-scanner 776, j2534-doip-can-fd 721, new-car-workshop-equipment-checklist 718, thinkcar-or-autel 700. Each now has 4 FAQs; visible FAQ = FAQPage (checked, JSON-LD parses). Byline "Last updated 2 November 2026", Article dateModified 2026-11-02 (build.py: new `mod`/`mod_text` fields; datePublished and guide-list order unchanged). |
| Live | per-folder sync_from_github (commit 533d84627), backups 20261102-092048-0bffd9, -092054-3aea6c, -092058-1b12bd, -092102-36ba71, -092106-e01eff, -092111-92f8cc; sitemap.xml 6 lastmods -> 2026-11-02 (backup 20261102-092119-c0b5ef). No boosted page touched; no whole-site sync. |
| Revert found | commit 9ecfc7279 (AIVS/Wrapstar thread, stale tree) had reverted this site's "Last updated" byline, products/ lastmod and the probe.sh header edits in the repo. CSKA + probe.sh/headers.txt restored in 77eb2094f (live was never affected). |
| Live probe (run 41418868108) | https://cskatrading.com/products/ 200, /articles/ 200, /no-such-page-xyz-123/ 404; http and www variants 301 -> https://cskatrading.com/ (single hop). |
| Pushed | 77eb2094f (restore), 533d84627 (articles) |

# Star Performance Motor (star-performance) — preview build

New client (17 Oct 2026, dealer contact Zach). Used car dealer, 9 Yishun Industrial Street 1 #01-82 North Spring Bizhub S768163.
Target domain www.starperformancemotor.com.sg (not resolving yet on 17 Oct 2026). Preview: https://pageonesingapore.com/preview/star-performance/ (bridge site "pageone", folder preview/star-performance). Noindex until go-live.

- `build.py` writes 19 pages into `site/` (facts, sources and CONFIRM list at the top; LIVE/DOMAIN flags; STOCK list for current cars).
- Pages: home (stock block, 5 service cards + cars-for-sale card, 4 handover stories, review carousel, 3 guides, 4 FAQs), /cars-for-sale/, /services/ + 5 (buy-a-used-car, sell-your-car, car-consignment, car-export, car-sourcing), /sold-cars/, /reviews/, /articles/ + 5, /about/, /contact/ (form opens WhatsApp), /privacy/, 404. Schema AutoDealer+Organization, Service, FAQPage, Article, Breadcrumb. No review/rating schema (third-party Facebook reviews). llms.txt, sitemap, robots (AI bots allowed), htaccess.txt for go-live.
- Theme: black + brand yellow-gold (their logo). sp.css / sp.js adapted from AIVS (reveal, hero slideshow, count-up, tilt) + review carousel autoplay.
- Photos: their own, from Facebook (showroom cover, 4 handover photos Aug 2026, logo) and Instagram (6 SOLD posts Mar 2022). Served from jsDelivr, repo site-assets branch commit 1bbc69e (site-assets/star-performance/).

## Sources and scraping notes (17 Oct 2026)
- Container proxy blocks FB/IG/sgcarmart. The Bluehost Bridge Base44 sandbox (app 6ac6d47b4ec84148578914c7) can reach them: Playwright (npm i playwright@1.47.2 in /tmp/pw) loads the FB page logged out (only ~4 newest posts + the reviews tab), IG /<user>/embed/ gives 6 posts with captions. Run long scripts with `setsid nohup ... &` (MCP times out at 60s). FB /photo/ pages need login (all return the same splash image).
- sgcarmart (dealer dl=3954) is behind Cloudflare: blocked even with headless Chromium and r.jina.ai. Live stock is linked, not copied.
- ACRA: UEN 202223232K, inc. 9 Nov 2022 (recordowl: Yishun address; opengovsg: older Serangoon North address).
- FB: phone +65 9742 7491, "100% recommend (391 reviews)" on 17 Oct 2026, 5.7K followers. IG captions (2022): Zach 8111 6736, Celsius 9139 6825, Colin 9108 6931.
- Not claimed: "price higher than trade-in guaranteed", "highest trade-in", "cheapest depreciation", prices, warranty, hours.

## To confirm with the client: see CONFIRM in build.py.

## Go-live
Addon domain www.starperformancemotor.com.sg -> preview/star-performance folder, DNS, AutoSSL, LIVE=True, rebuild, re-upload, htaccess.txt -> .htaccess via cPanel, Search Console + Bing, EDGE daily articles + backlinks tracker, GBP website link.

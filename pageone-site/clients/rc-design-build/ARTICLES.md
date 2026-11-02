# SG Commercial Fitout (commercialfitout.sg) - night article rules

LIVE since 25 Oct 2026. Night run writes one guide on EVEN SGT dates (seo-method/daily/articles.md).

How to add a guide
1. Read content/guides.py and keep the same dict shape (path /guides/<slug>/, title <=60 chars ending " | R&C"
   (build.py rewrites it to the brand), desc, h1, kicker, answer (40-60 word direct answer), card, image (an
   existing image key from content/guides.py or services), image_alt ending "(AI design concept)", date (SGT
   YYYY-MM-DD), owner (one service/space page it supports), reading, sections (question H2s), faqs, related, wa_topic).
2. Append it as G7, G8 ... and add it to PAGES. Pick a long-tail query a Singapore shop/office/F&B tenant types
   (e.g. "kiosk counter design singapore", "shop signage lighting", "salon station carpentry"). Check the
   existing guides first so two articles never target the same keyword.
3. Facts: general practical guidance only. No prices, timelines, warranties, licences, UEN, team, years, reviews,
   no named authority rules or figures unless linked to the official page with an "as of" date.
   Address/phone only as in build.py. Images: only existing AI concept images or Edwin's own photos; no logos.
4. Build: `python3 build.py` (no RC_IMG). Copy build.py, content, site to the repo copy
   pageone-site/clients/rc-design-build/ on site-assets, commit, push, then bridge sync_from_github
   {site: pageone, ref: SHA, source_path: pageone-site/clients/rc-design-build/site, base_path: preview/rc-design-build}.
5. Verify https://commercialfitout.sg/guides/<slug>/ returns 200, then IndexNow the new URL + /guides/ + /sitemap.xml
   (key 7d4c2a9e1f6b8035c4e2a7d9b1f60c38).
Coordinate: the 00:00 SGT concept-of-the-day run also commits this folder; git pull before building.

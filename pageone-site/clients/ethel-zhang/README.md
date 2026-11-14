# Ethel Zhang (ethel-zhang) — preview build

Client: Ethel Zhang, Associate Division Director, Huttons Asia Pte Ltd (L3008899K), CEA R059986J, WhatsApp +65 9183 6325. Built 16 Oct 2026.
Domain will be ethelzhang.com (currently a GoHighLevel "10-Year Property Fit Scorecard" opt-in page; the new site rebuilds that scorecard as an on-page quiz at /scorecard/).
Preview: https://pageonesingapore.com/preview/ethel-zhang/ (bridge site "pageone", folder preview/ethel-zhang). Noindex until go-live.

- `build.py` writes every page into `site/` (facts, DOMAIN/LIVE flags and CONFIRM list at the top). Build from a scratchpad copy, not from this folder (files under /mnt/project-files gain C2PA bloat); `site/` here holds only ethel.css and ethel.js (edited by hand, not generated).
- Pages: home, /dream-method/, /scorecard/ (5-question quiz, result sent to WhatsApp), /services/ hub + 6 service pages (buying, upgrading, selling, investment, renting, retirement/legacy), /about/ (timeline from her notes, EC Coffee Bar link confirmed by Edwin), /articles/ + 6 articles, /contact/ (form opens WhatsApp), /privacy/, 404, robots (AI bots allowed), sitemap, llms.txt, IndexNow key e7a1c3f95b2d4e6a8c0f1b3d5e7a9c2f.
- Photos: PropertyGuru headshot (src/pg.jpg) and 5 of her Instagram posts (src/ig/, screenshots from Edwin), cropped to site/img/*.webp.
- `manual-upload/htaccess.txt` and `manual-upload/img/share/home.jpg` need cPanel upload at go-live (bridge can't write them).
- Positioning (from her coach's notes): relationship-based residential adviser for every stage of life; ICA = financially capable SC/PR aged 30-50; D.R.E.A.M. Alignment Method; big promise = right property for present life stage + 10-year plan.
- Left out on purpose (CEA): "$400k+ profit", "don't wait" urgency, any transaction promises. 47 transactions / 5.0 from 2 reviews are PropertyGuru figures (linked, dated Oct 2026).
- Open items: see CONFIRM.txt.

## Update 16 Oct 2026 (late)
- Theme: pinkish-white "dreamy princess" (ethel.css v10): aurora hero, falling petals and feed marquee (added by ethel.js), glass cards, rose-gold type.
- Bilingual: English at /, Simplified Chinese at /zh/ (zh/<key>.json holds the translations; build.py load_zh() renders them). EN | 中文 switch in header, hreflang, sitemap alternates.
- New pages: services/offices-and-shophouses/, services/business-premises/, 2 commercial articles.
- Upload tip: base64 writes over ~30 KB get stopped by the safety classifier; keep images under ~25 KB. Version bumps on pages were done with invoke_edit_file.

## Daily articles (17 Oct 2026)
- Writer: Base44 Controller app, function `ethelArticle`, workflow "Ethel Article Writer" (07:30 SGT daily). Each run picks a new owner/buyer question, writes EN + 中文 (official .gov.sg sources only, CEA-safe), makes an AI image and stores an `EthelArticle` record (status `ready`).
- Images: Core.GenerateImage, resized to 800px JPEG and hosted on media.base44.com (UploadFile). All 8 older articles have AI images too (status `legacy` records).
- Publish to the site (not automatic yet): export EthelArticle records to records.json, run `python3 ethel_publish.py` (writes auto/*.json), then `python3 build.py`, then upload the new article pages, both articles indexes, home cards, sitemap.xml and llms.txt via the Bluehost Bridge.
- Lessons: jsquash/jimp codecs fail in Base44 functions (use jpeg-js + fast-png); FTP safeWrite can't verify image uploads, so images stay on Base44 hosting.

# Carzy World Sdn Bhd (AutoSEO.my client preview)

Static site in English, Malay and Simplified Chinese, rendered at build time from one set of shared templates.
Preview: https://autoseo.my/preview/carzy-world/ (BM at `ms/`, 中文 at `zh/`), noindex while previewing.

- `data/business.json`: every business fact (name, company no., address, phone/WhatsApp, email, hours, Google rating, links). Change a fact once here.
- `data/site.json`: languages, service pages (slug, icon, photo), photos, recent work, the five Google reviews (kept in original English).
- `strings/en.json`, `ms.json`, `zh.json`: every visible string, meta, FAQ, photo alt text and WhatsApp prefills (same keys in each).
- `templates/`: head, header (with EN | BM | 中文 switch), page hero, trust strip, service card, review card, FAQ, CTA band, photo, footer + mobile WhatsApp/Call bar.
- Video-led layout (11 Nov 2026): homepage hero is the self-hosted signature clip (muted autoplay loop, poster only when reduced motion), a reel strip of click-to-load Facebook clips (no Facebook request before a tap), and a click-to-play 190E clip. Clip data: `data/site.json` `self_videos` + `embeds` (platform + url + thumb; youtube/tiktok builders ready in build.py). Files in `media/` are uploaded to the server by hand and are not in this repo; pages link to them page-relatively.
- `photos/`: the business's own photos from its Google Maps listing. The build adds 640px copies, the header logo and icons.
- `src/build.py` builds `site/` and runs `src/check.py`; a failed check stops the build.
- `site/sitemap.xml` and `site/llms.txt` are written for the planned domain https://www.carzyworld.com/ and are not linked from autoseo.my.

Build: `python3 autoseo-clients/carzy-world/src/build.py` (needs Pillow).

Move to carzyworld.com: in `data/business.json` set `site_url` to `https://www.carzyworld.com/`, `base_path` to `/`, `preview` to false; rebuild; add a robots.txt with the sitemap line.

# Hybrid World Specialist preview site (AutoSEO.my client)

HYBRID WORLD (M) SDN BHD (202301037226), brand Hybrid World Specialist (HWS). Hybrid and EV car workshop in Taman Bukit Indah, Iskandar Puteri, Johor Bahru.

- Preview: https://autoseo.my/preview/hybrid-world/ (+ ms/, zh/). Upload the contents of `site/` to `public_html/autoseo.my/preview/hybrid-world/`. No .htaccess and no media/ are shipped (the 12 reel MP4s + posters are already in media/ on the server). Every page has a noindex meta tag; autoseo.my/preview/.htaccess sends the header.
- Planned domain: https://hybridworld.my/ (not registered yet). sitemap.xml and llms.txt in site/ are written for it.

## Build

    python3 autoseo-clients/hybrid-world/src/build.py

Writes fully rendered HTML into `site/` and runs `src/check.py` (one H1, shared parts on every page, noindex, hreflang, schema facts = config, FAQ schema = visible FAQ, review quotes verbatim, no iframe before a tap, blocklist of white-label words and claims we cannot make, no English left on BM/中文 pages). A failed check stops the build.

## Where things live

- `config.json`: every business fact (name, company no., address, phone/WhatsApp, email, hours, map, Facebook, rating).
- `strings/en.json`, `ms.json`, `zh.json`: every visible word, incl. WhatsApp prefills.
- `data/site.json`: page order, photo-to-service mapping, carousel, reels (id, shape, seconds), review quotes (verbatim, first names).
- `templates/`: head, header, footer, WhatsApp + call buttons, sticky bar, service tile, step, carousel, reel, review, map facade, FAQ, CTA, breadcrumb.
- `assets/site.css` (palette vars at top), `assets/site.js` (menu, off-screen pause, reels, map tap-to-load, carousel).
- `photos/`: the client's real photos (Google Maps + Facebook). fb-01..03 are a Toyota Voxy; never caption any as Lexus/CT200h.

## Move day

config.json: `site_url` = `https://hybridworld.my/`, `base_path` = `/`, `preview` = false, rebuild, add a robots.txt.

# AutoSEO.my site (preview)

Static site, rendered at build time. Preview address: `/preview/autoseo-my/` on the agency preview host (noindex).

- `data/brand.json` — the one file for brand facts: name, tagline, company, WhatsApp number, prefills, areas, base path, `preview` switch, `site_url`.
- `data/content.py` — page text (client copy kept word for word, marked COPY).
- `templates/` — shared parts used by every page: `head.html` (meta, robots, schema slot), `header.html` (logo + nav), `page_hero.html`, `faq_block.html`, `cta_band.html`, `footer.html` (footer + floating WhatsApp button).
- `assets/base.css` + `assets/brand.css` → `site/assets/site.css`; `assets/site.js`. Links carry `?v=<hash>`.
- `src/build.py` — builds `site/` and then runs `src/check.py`; the build stops if the check fails.
- `src/check.py` — pre-upload grep against `data/blocklist.txt`, plus one H1, robots noindex,nofollow, schema parses with no phone/address/email, no sitemap.

Build: `python3 autoseo-my/src/build.py`

Going live later: set `preview` to false and `site_url` to the live domain in `brand.json`, set `base_path` to `/`, rebuild, and add a sitemap.

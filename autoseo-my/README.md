# AutoSEO.my site (preview)

Static site in three languages, rendered at build time from one set of templates.
English at `/preview/autoseo-my/`, Malay at `/preview/autoseo-my/ms/`, Chinese at `/preview/autoseo-my/zh/` (all noindex while previewing).

- `data/brand.json`: brand facts shared by every language (name, tagline, company, WhatsApp number, base path, `preview` switch, `site_url`).
- `data/site.json`: languages, page order, slugs and icons.
- `strings/en.json`, `strings/ms.json`, `strings/zh.json`: all visible text, meta, FAQ, schema text and WhatsApp prefills per language (same keys in each).
- `data/clients.json`: the client websites on `/clients/` (EN/BM/中文), only sites live on their own domain, with screenshots in `assets/clients/` and the page's own `assets/clients.css`. Client names there are allowed by `check.py` on the /clients/ pages only.
- `data/site.json` `partners_live`: false keeps `/partners/` unbuilt and unlinked until that page is live.
- Footer tagline: English on EN pages; on ms/zh inner pages the English line plus `<span class="tagline-tr">` with the translation; ms/zh home pages show the translation only (matches live, 13 Nov 2026).
- `templates/`: the shared header (with the EN | BM | 中文 switcher), page hero, FAQ block, CTA band and footer with the WhatsApp button. One edit changes all three languages.
- `assets/base.css` + `assets/brand.css` → `site/assets/site.css`; `assets/site.js`. Links carry `?v=<hash>`.
- `src/build.py`: builds `site/`, then runs `src/check.py`; the build stops if the check fails.
- `src/check.py`: blocklist grep (`data/blocklist.txt`) over all output, plus checks for one H1, noindex, lang tags, canonical, hreflang, valid schema without phone/address/email, no sitemap, and no leftover English or placeholders on ms/zh pages.

Build: `python3 autoseo-my/src/build.py`

To go live: set `preview` to false, set `site_url` to the domain (canonical and hreflang then become absolute) and `base_path` to `/`, rebuild, and add a sitemap.

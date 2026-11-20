# AutoSEO shared site template

## Standing rule (Edwin, 18 Nov 2026, 11:37pm SGT)

Every AutoSEO site must ship in English, Simplified Chinese and Malay from the first preview: a header language switcher, /zh/ and /ms/ pages for every English page, hreflang plus x-default, and all three languages in sitemap.xml, all generated from the shared template and one facts/strings file.

## What the template owns

`autoseo_i18n.py` is imported by every AutoSEO site build. One edit here changes every page of every site on its next build.

| Part | Function | Where it goes |
|---|---|---|
| Languages | `LANGS` | English at the site root, Malay at `/ms/`, Simplified Chinese at `/zh/` (never `/my/`, `/cn/`, `/bm/`) |
| html lang + hreflang codes | `LANGS[i]['hreflang']` | `en`, `ms`, `zh-Hans` (K Tech keeps its existing `en-MY`, `ms-MY`, `zh-MY`) |
| hreflang block | `hreflang_links(absu, path)` | the shared head partial: three alternates plus `x-default` pointing at the English URL |
| og:locale | `og_locale_tags(L)` | the shared head partial |
| Language switcher | `switcher(u, path, L, aria_label)` | the shared header (and the mobile menu). Labels are fixed: **EN, BM, 中文** |
| sitemap.xml | `sitemap_xml(absu, paths, lastmod)` | generated from the page list: every page in all three languages, each with `xhtml:link` alternates and `x-default` |
| Twin gate | `check_twins(files)` | the site's check.py: fails if any English page has no `/ms/` or `/zh/` twin |

## How a site uses it

1. **One facts file** (`facts.json`): name, phone, WhatsApp, address, prices, anything that is a fact. Never repeated in copy files.
2. **One strings file per language** (`strings_en.py`, `strings_ms.py`, `strings_zh.py`) with the SAME keys: titles, meta descriptions, H1s, body copy, schema slogans, alt text and captions, WhatsApp prefill messages, UI labels and aria labels. The build fails if a key is missing in any language.
3. **One build** (`build.py`) loops over `I18N.LANGS` and renders every page from the same shared head, header, footer and blocks. No hand-edited page, header, footer or switcher.
4. **sitemap.xml and llms.txt** are generated from the page list, never edited by hand.
5. **Fully rendered HTML**: H1, body text and JSON-LD are in the page source in every language. No client-side includes.
6. **Same CTA tracking on every language**: the WhatsApp/call/email/map links come from one helper, so `data-cta` placements are identical in EN, BM and 中文 (only the prefill text changes).

## Translation rules

- Simplified Chinese (`zh-Hans`) and Bahasa Melayu (`ms`). Localised wording, not literal machine copy.
- Translate title tags, meta descriptions, H1s, body copy, schema slogans, alt text and WhatsApp prefills.
- No invented facts: nothing that is not already on the English page or in facts.json (no hours, reviews, ratings, staff names, map pins, company numbers, prices or claims).
- Brand names, model names, oil grades and phone numbers stay as written.

## Previews and go-live

- Previews: `noindex, nofollow` on every page in every language; the preview is never added to autoseo.my's sitemap.xml or llms.txt and never pinged to IndexNow. The site's own sitemap.xml is built for its future domain.
- Uploads only through the Bluehost Bridge (`sync_from_github` with a commit SHA), backup first, Publish only, never Activate, no new `.htaccess`.
- After a change: grep the built output and the live pages (home, an inner page and an article, in EN, BM and 中文), shots at 390px and 1280px, pre-upload grep (old prices, removed credits, placeholders, invented facts).

## Sites built on this template

- CCH Automotive (`autoseo-clients/cch-automotive/`), first site on the shared module, 18 Nov 2026.
- Older AutoSEO sites (AutoSEO.my, Carzy World, Hybrid World, EMATS, AP Car, K Tech) have the same pattern inside their own build.py; move them onto this module the next time each is rebuilt. Benz World has no generator in the repo yet (see the migration note in /mnt/project-files/autoseo-my/site-template/).

## Look v2 blocks (Edwin, 20 Nov 2026: "too boxy and square")

New AutoSEO sites start from `blocks/`, not from plain bordered boxes. Reference build: `autoseo-clients/jt-autoworks/` (preview https://autoseo.my/preview/jt-autoworks/).

| Block | Files | What it is |
|---|---|---|
| Photo hero | `blocks.py` `photo_hero()`, `blocks.css` "photo hero" + "header" | Full-bleed real shopfront or bay photo behind a transparent header (white glass after 24px of scroll), white H1 and the WhatsApp CTA on the photo, bottom fading into the next band. Phone uses a 4:5 or taller crop, desktop a wide photo. Real photos only. |
| Video facade | `video_tile()`, `reel_strip()`, `blocks.css` "video facade" + "swipe strip", `blocks.js` | 9:16 tile that shows the real poster frame and a clear play icon from first paint. Self-hosted MP4: `<video poster>`. Otherwise an `<img>` facade that swaps to the official Facebook embed on tap (no Facebook script before the tap). No poster frame means no tile: never an empty or black box. Strip: ~64vw on phones, 4 across on desktop. |
| Soft cards | `soft_card()`, `soft_cards()`, `lap_block()`, `blocks.css` "package strip" + "overlapping" + "FAQ" | Rounded (18 to 24px) cards with soft shadows and no hard borders: package strip with the real poster (contain), big price and a WhatsApp button on every card; overlapping photo-and-text block; soft FAQ rows. |
| Colour bands | `blocks.css` "colour bands" | Full-width bands that alternate navy and light, each rising over the last with rounded top corners. |
| Floating bar | `blocks.css` "floating mobile bar", `blocks.js` | Pill WhatsApp + Call bar on phones, hidden while the hero buttons are on screen. |

How to use: copy the `:root` tokens from `blocks.css` and recolour them from the client's logo (keep radii, shadows, spacing), paste the block CSS into the site stylesheet, include `blocks.js` (or the same code in site.js), and render with the `blocks.py` functions, passing CTA HTML from the site's own `wa()`/`call()` helpers so `data-cta`/`data-ref` stay per site. Mix layouts on the home page: one swipe strip (videos), one overlap block, one package strip; do not repeat one square tile everywhere. Designed posters always `object-fit: contain`; real photos `cover`. Check at 390px, then 360px and desktop.

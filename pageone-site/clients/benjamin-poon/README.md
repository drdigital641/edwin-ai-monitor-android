# Benjamin Poon (潘国雄) website (preview)

New Page One client, 22 Oct 2026 (Edwin). Personal consultant site: Nirvana Singapore niches, ancestral tablets, funeral services, will planning. English (/) + Simplified Chinese (/zh/), no Malay.
Spec: `HANDOVER-from-client.md`. Edwin's rule: never show his award/sales dollar amounts (the $68,776.58 figure and the "$50K Elite Club" box/badge are cropped out).

Preview target: https://pageonesingapore.com/preview/benjamin-poon/ (hidden by the preview/.htaccess X-Robots-Tag header; no noindex in pages).

## Files
- `build.py`: builds `site/` (44 pages = 22 x 2 languages, plus 404, sitemap with hreflang en-SG / zh-SG / x-default, robots with AI bots, llms.txt, manifest, IndexNow key). Facts + sources in the docstring; `CONFIRM` list. `LIVE = False` shows dashed "PENDING CLIENT APPROVAL" boxes; set True at go-live to hide them.
- `content/`: `services.py`, `locations.py`, `guides_a.py`, `guides_b.py` (bilingual content modules, each with SOURCES and per-page `pending`), `BRIEF.md` (rules the writers followed).
- `bp.css`, `bp.js`: ivory / deep green / muted gold theme, reveal-on-scroll (below-fold only, text never changed by script), mobile WhatsApp + Call dock.
- Images: `assets/` (portrait crop, 3 award images, og image), `icons/` (BP monogram favicon set). Served from jsDelivr: site-assets branch commit c012476, folder site-assets/benjamin-poon/.
- Built site committed to GitHub: branch site-assets, folder `pageone-site/clients/benjamin-poon/site`, commit 0deab34009c57bcb65e2684003fe9ea19c7df5e1.
- `CONTENT_SOURCES.md`, `CLIENT_APPROVAL_CHECKLIST.md`, `SEO_KEYWORD_MAP.md` (handover deliverables 6-8).

## Upload (preview)
Bridge `sync_from_github` {site: pageone, ref: <commit SHA>, source_path: pageone-site/clients/benjamin-poon/site, base_path: preview/benjamin-poon}. Done 22 Oct 2026 00:28 UTC: 55/55 files verified by sha256 (another thread ran the sync after Edwin reconnected + re-approved the bridge connector; sessions started before that only saw the old 10 tools).

## QA run 22 Oct 2026 (local build)
- Dollar-amount sweep (68,776 / 50K / $50 / Elite Club) over all files: none.
- Every JSON-LD block parses; every internal link resolves; one H1 per page; titles within limits.
- Playwright (Chromium) at 390x844 and 1366x900: no horizontal scroll; hero, Chinese pages, service, location and guide pages render; body text present unscrolled.
- Live (from the Base44 sandbox, browser UA): EN + /zh/ home, a service, a location, a guide, bp.css, favicon, sitemap, robots all 200; X-Robots-Tag: noindex, nofollow present; portrait loads from jsDelivr; no dollar amounts in the live home page.

## Go-live (only on Edwin's word)
1. Benjamin answers CLIENT_APPROVAL_CHECKLIST.md; update content + `CONFIRM`; set `LIVE = True`, `DOMAIN`.
2. Buy domain, addon domain -> preview/benjamin-poon, `htaccess.txt` in as `.htaccess` via cPanel.
3. Rebuild, commit, sync_from_github; Search Console + Bing sitemap submit; IndexNow (key 5b8e2d7f1c9a4e06a3d2f8b7c6e1a940).
4. Join the loops: articles every 2 days, backlinks tracker, Controller Client row live. No GBP at a venue he doesn't run.

## Redesign 22 Oct 2026 (Edwin: mykar.my structure + nirvana.com.sg look)
- Theme: charcoal #1d1c1a, ivory, champagne gold #ddcc97 / #a88c52, Playfair Display headings (Didot-like, as Nirvana), Jost body.
- Photos: `content/photos_nirvana.py` (15 official nirvana.com.sg photos, hotlinked, use PENDING Benjamin/Nirvana OK) + `content/photos.py` (Pexels + Commons, hotlinked). Credits on /disclaimer/.
- Benjamin's Facebook (facebook.com/benpoon82) needs login; Edwin to send photos.
- 22 Oct 01:03 UTC: light editorial redesign benchmarked on nirvana.com.sg, live ref 5ed7b917768aff9ec7f0e19a4cbabdaf52ec7225. Comparison screenshots compare-*.jpg, preview-home-full.jpg.
- Visual QA of hotlinked photos: Playwright in the Base44 sandbox (/tmp/pw), routing the preview URL to raw.githubusercontent at the commit, jimp-resized, base64 via saved tool output.

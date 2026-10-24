# R&C - Retail & Commercial Design & Build (preview)

Preview: https://pageonesingapore.com/preview/rc-design-build/ (hidden from Google by the parent preview/.htaccess
X-Robots-Tag header; pages carry index,follow, no noindex tag). Built 24 Oct 2026. Edwin-owned brand, not a client company.
Brief: content/PROJECT-BRIEF.md (from drdigital641/edwin-ai-context handoffs/2026-10-24-rc-design-build-project.md).

## Files
- build.py: builds 28 pages into site/ (`python3 build.py`; RC_OUT / RC_IMG env for local screenshots). Settings at top:
  DOMAIN, LIVE, WA_NUMBER, ASSET_SHA. PENDING list drives the dashed "preview note" boxes (hidden when LIVE).
- content/: services.py, avl.py, spaces.py (incl. 6 CONCEPTS), guides.py (6 guides), BRIEF.md (writer rules).
- rc.css / rc.js (motion: reveal-on-scroll, hero drift; no script changes text), fonts/ (Fraunces + Manrope, self-hosted),
  icons/ (R&C mark), assets/ (15 AI concept images + og-rc.jpg; served from jsDelivr site-assets @6958e99),
  wa-tap-counter.js (Controller slug rc-design-build), screens/ (screenshots).
- Repo: drdigital641/edwin-ai-monitor-android, branch site-assets: pageone-site/clients/rc-design-build (source + site/),
  site-assets/rc-design-build (images). Preview upload = Bridge sync_from_github {site: pageone, ref: <sha>,
  source_path: pageone-site/clients/rc-design-build/site, base_path: preview/rc-design-build}. First sync: d33791c.

## Pages (28)
Home, /retail-commercial-design-build/, /services/ + 5 service pages, /avl/ + 3 AVL pages, /spaces/ + 4 space pages,
/design-concepts/ (6 labelled concepts), /guides/ + 6 guides, /about/, /contact/, /privacy-policy/, 404.

## Rules kept
No invented facts: no address, UEN, team, years, prices, timelines, reviews, warranties, licences, completed work.
Every image is labelled "AI design concept". No regulatory specifics. CTAs go to /contact/ until WA_NUMBER is set
(then wa.me with prefill: project type, page, ref=website).

## Pending (Edwin) before go-live
1. Domain (none chosen; do not buy without Edwin). 2. Operating company + UEN. 3. WhatsApp number (Edwin 24 Oct: decide later).
4. Who delivers the work. 5. Service area. 6. Real photos of actual work, when they exist (separate "Actual work" section).

## Go-live steps (only on Edwin's word)
1. Set DOMAIN, WA_NUMBER, LIVE = True, rebuild, commit, sync.
2. Write htaccess.txt (https, no-www, index.html 301, ErrorDocument 404 /404.html, 1 h HTML cache; copy new-age-polish/htaccess.txt
   pattern) and have it placed as .htaccess via cPanel; addon domain doc root = preview/rc-design-build.
3. Search Console + Bing, IndexNow (key file 7d4c2a9e1f6b8035c4e2a7d9b1f60c38.txt already in site), Controller row -> live.

## Temporary image tool
Base44 app "R&C Image Studio (temp)" (6adc39a33be36ae8a3ed0782) has a key-guarded genImage function (secret IMG_KEY) used to
make the concept images. Delete the app when no more images are needed.

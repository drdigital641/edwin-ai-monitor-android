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

## Status: LIVE on https://commercialfitout.sg since 25 Oct 2026 (Edwin: "verified in gsc and live")
Addon domain doc root = preview/rc-design-build (same files as the preview URL; the preview host still sends noindex).
Checked 25 Oct 01:15 UTC: http and www 301 to https://commercialfitout.sg/, /about -> /about/, real 404, no X-Robots
on the domain, robots allows OAI-SearchBot, sitemap 30 URLs, IndexNow 202. No own .htaccess was needed for that.
Controller Client row status live. Night run writes a guide on EVEN SGT dates (ARTICLES.md); IndexNow daily via
watchdog/indexnow.py. Still open: operating company + UEN (no box shown on LIVE; add to footer/schema once Edwin
gives it), workshop photos (WORKSHOP list in build.py; section hidden until filled).

## Temporary image tool
Base44 app "R&C Image Studio (temp)" (6adc39a33be36ae8a3ed0782) has a key-guarded genImage function (secret IMG_KEY) used to
make the concept images. Delete the app when no more images are needed.

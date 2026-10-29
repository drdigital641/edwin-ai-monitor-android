# Autotex Kia & Hyundai parts shop (preview)

Client: Autotex Aircon Enterprise (UEN 52353300D, registered 24 Feb 1995), 1 Kaki Bukit Ave 6 #01-42 AutoBay@Kaki Bukit S417883, tel 6747 9618, WhatsApp +65 9731 9547, Google 5.0 (4 reviews).
Built 29 Oct 2026. Preview: https://pageonesingapore.com/preview/autotex/ (hidden by the parent preview/.htaccess header; pages carry no noindex).
WARNING: autotex.net (linked from their Google profile) is NOT theirs: it is Autotex Private Limited, a textile company in Coimbatore, India. Never link it; fix the GBP website field at go-live.

## Build
`python3 build.py ../site` from src/. Sources: catalog.py (brands, 20 models, 9 categories, 18 part types, sample price formula), build.py, at.js (search, finder, cart -> WhatsApp), at.css, staff.js/staff.css (dashboard), wa.js (tap counter, site 'autotex'), assets/.
Upload = Bridge `sync_from_github` site=pageone, base_path=preview/autotex, source_path=pageone-site/clients/autotex/site.

## Facts vs samples
- Facts: ACRA + Google profile + Edwin's message (stockist, direct from Korea, sells direct to drivers at distribution price).
- SAMPLE (not real): all 346 products and prices. Each product has sample=1 and shows a "Sample price" badge. `LIVE = True` in build.py hides sample prices (shown as "Ask for price") and drops them from Product schema.
- Part numbers, stock and photos: none yet. Product art is an icon with "Photo coming".

## Staff dashboard (/staff/, demo PIN 1995)
Edits are saved in the viewer's browser (localStorage at_catalog_v1) and the shop pages in that browser show them. Export JSON -> save as src/catalogue.json and rebuild to publish. Real go-live needs a backend (Base44/Controller) so Save publishes for everyone.

## Open (ask Autotex)
1. Real catalogue: which models and parts they stock, prices, part numbers, stock status, photos.
2. Opening hours (Google shows 9:30am Fri only).
3. Domain for the shop; logo; delivery offered? payment methods (PayNow?).
4. Confirm wording "at distribution price" and "direct from Korea" (genuine/OEM?).
5. Add a Controller Client row 'autotex' for the WhatsApp tap counter.

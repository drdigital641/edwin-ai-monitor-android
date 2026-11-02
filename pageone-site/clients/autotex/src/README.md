# Autotex Kia & Hyundai parts shop (live: https://autotexautoparts.com.sg)

Client: Autotex Aircon Enterprise (UEN 52353300D, registered 24 Feb 1995), 1 Kaki Bukit Ave 6 #01-42 AutoBay@Kaki Bukit S417883, tel 6747 9618, WhatsApp +65 9731 9547, Google 5.0 (4 reviews).
Hours: Mon-Fri 9:30am-5:30pm, Sat 9:30am-3:30pm, Sunday closed.
WARNING: autotex.net (linked from their Google profile) is NOT theirs: it is Autotex Private Limited, a textile company in Coimbatore, India. Never link it; fix the GBP website field at go-live.

## Flow: database -> db/*.json -> build -> upload
1. Staff add cars, products and photos in the Base44 dashboard (https://autotex-catalogue-05dbf5ec.base44.app/, app id 6ae3683191b1a44205dbf5ec). /staff/ on the site only redirects there.
2. Export the raw API arrays (public read, page with `skip`, limit 500) into `src/db/`:
   - `cars.json`   = /entities/AtCar
   - `products.json` = /entities/AtProduct
   - `photos.json` = /entities/AtPhoto (optional; only needed for `b44photo:<id>` photos). `python3 pull_photos.py --fetch` downloads it.
   Base URL: https://autotex-catalogue-05dbf5ec.base44.app/api/apps/6ae3683191b1a44205dbf5ec
3. `python3 build.py ../site` from src/. Only rows with status "published" are used. build.py then calls pull_photos.py, which writes `assets/p/<id>.jpg` into the site.
4. Upload `site/` to the domain root (Bridge `sync_from_github`, source_path `pageone-site/clients/autotex/site`), paste `htaccess.txt` as `.htaccess` via cPanel.

With an empty `products.json` the site lists the part TYPES Autotex supplies for each car with an "Ask on WhatsApp" button and no price. No stock or prices are invented.

## Live data in the browser
at.js loads AtCar and AtProduct from the public API on every page (cached 5 minutes in sessionStorage) and the database wins over the built pages: changed price/stock/photos update, hidden products disappear, new products and new cars show in search, the finder and model pages (new products open at `search/?id=<key>`). If the fetch fails the static build stays. Between rebuilds the built pages are only the baseline, so rebuild after big catalogue changes (new product pages, SEO).

## URLs
Product page: `{brand}/{car key}/{part id}/` for the first product of a car + part type, otherwise `{brand}/{car key}/{product key}/` (also for part "other").
Photos: http(s) URLs are used directly (img, og:image, Product.image); `b44photo:<id>` is resolved from photos.json to `assets/p/<id>.jpg`, or lazily from /entities/AtPhoto/<id> in the browser.

## Files
catalog.py (BRANDS, CATS, 18 PARTS: no prices), build.py, pull_photos.py, at.js (search, finder, cart -> WhatsApp, live data), at.css, wa.js (tap counter, site 'autotex'), data.js (generated), assets/ (logo.svg, logo-dark.svg, icons, og.jpg), db/.
staff.js/staff.css are the retired local dashboard and are no longer copied into the site.

## Go-live checklist
Search Console + Bing verification, GBP website link to the new domain, IndexNow, Controller Client row 'autotex' for the WhatsApp tap counter, confirm wording "at distribution price" and "direct from Korea", delivery and payment methods. Public holiday opening is not stated on the site (unknown).

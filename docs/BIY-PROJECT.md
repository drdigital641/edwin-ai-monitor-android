# BIY Home Store: PROJECT FILE (single source of truth)

Client: BIY Home Store (Kota Tinggi) Sdn Bhd, Johor, Malaysia (AutoSEO.my client, slug `biy-home-store`).
Owner: Edwin (Dr Digital). Created 26 Nov 2026, 7:09am SGT, by Website Manager (Grok).
Everything here comes from real files, briefs or Edwin's messages. Anything not confirmed is marked **OPEN**.
All times are SGT (Asia/Singapore).

> **READ THIS FILE BEFORE ANY BIY JOB. UPDATE IT AFTER.** See section 10.
> This file must contain NO secrets: no keys, tokens, passwords, hashes or phone numbers other than the public business WhatsApp. Use names only (for example `BIY_FEED_READ_KEY`).

---

## 1. Goal and stages

**Goal:** a fast, mobile-first, Google-SEO hardware shop for BIY (paint, power tools, hardware, building materials) that turns searches into WhatsApp enquiries and shop visits, and later reads live stock and products from BIY's AutoCount through an API. Edwin: "BIY is going to be a big project", so Grok and Claude must stay in sync (26 Nov 2026, 7:06am).

Edwin's stage numbering (26 Nov 2026) replaces the three "Phases" in his 25 Nov master brief. The master brief is kept for reference only (section 9).

| Stage | What | Done when |
|---|---|---|
| **1** | Preview with add-to-cart (enquiry basket, browser memory) and sample data that switches off by itself. Then go-live on biyhomestore.com (replacing the unfinished SiteGiant shop). | Preview passes the quality gate; Edwin OKs; domain switched; live gates ticked (SSL apex + www, GSC/Bing/IndexNow, Controller Live, SITE-NOTES, article roster row) |
| **2** | Live AutoCount vendor feed: the AutoCount vendor pushes products and stock to the BIY Catalogue API; the site reads `/feed/products` and replaces the sample data. | Vendor's first live push published; site rebuilt; sample label gone (no code change); before/after screenshot |
| **3** | **OPEN, Edwin to define.** The plan doc does not define Stage 3. Candidate items from the 25 Nov master brief (not assigned, not confirmed): preorder submission, guest checkout, customer contact details, order confirmation, customer accounts, membership, loyalty, online payment, order history and tracking, contractor pricing, repeat purchases. | Edwin defines |

Rule for the architecture: Stage 2 and 3 must not need a front-end rebuild (master brief rule 11: API integration must not require rebuilding the whole front end).

---

## 2. Decisions log (dated, who decided)

| Date and time (SGT) | Decision | Who |
|---|---|---|
| 25 Nov 2026 | Client is BIY Home Store (Kota Tinggi) Sdn Bhd, 4 branches. Existing SiteGiant shop at biyhomestore.com is "not done up", safe to overwrite. | Edwin (client match was Grok's best match, used as default) |
| 25 Nov 2026, 10:31pm | "Let's do the website first." Phase 1 preview only. Rule A0 (billing entry before build) overridden for the preview only. Billing stays "awaiting Edwin's fee". | Edwin |
| 25 Nov 2026, ~10:40pm | Bridge drop unusable (BRIDGE_DROP_KEY not set), so files go to Drive folder `Client Photo Banks / biy-home-store`, anyone-with-link reader. | Grok (workaround) |
| 25 Nov 2026, 10:50pm | Phase 1 defaults until Edwin answers: all 4 branches; WhatsApp 012-568 8961 (wa.me/60125688961); "WhatsApp for price", no prices anywhere; brands Jotun, Nippon Paint, Dong Cheng, Bosch only; ICI held (published:false); own orange/charcoal identity, not a Shopee look; preview noindex. | Grok defaults from Edwin's brief, **not yet confirmed by Edwin** |
| 25 to 26 Nov 2026 (time not recorded) | "Go live" on biyhomestore.com. Add-to-cart with browser memory. Dummy data for the preview that switches off automatically when the API is linked. | Edwin |
| 26 Nov 2026, 6:44am | Verbatim: "biystore - implement add to cart button with browser memory. -prefill site with dummy data for client preview - which will automatically switch off with api is linked up." This relaxes the old "no cart" default. The cart is an enquiry basket: no prices, no payment, no login. | Edwin |
| 26 Nov 2026, 6:51am | Brief v3 (cart + sample fallback) sent to Claude. | Grok |
| 26 Nov 2026, 6:53am | Approved the backend as a separate Base44 app (not the Bridge, not AutoSEO Admin, not the Controller). | Edwin |
| 26 Nov 2026, ~7:00am | Grok built and published the Base44 app "BIY Catalogue API" (id 6b076707c2f2e4cff2aa4988), checkpoint 6b076854de695654e871e546. Smoke test passed with the test key. | Grok |
| 26 Nov 2026, ~7:01am | Feed addendum written for Claude (feed URL, read key via environment variable `BIY_FEED_READ_KEY`, resolver states). Written, not yet confirmed as relayed. | Grok (relay status OPEN) |
| 26 Nov 2026, 7:06am | This project file is the shared source of truth, read before and updated after every BIY job by both Grok and Claude. | Edwin |
| Reported by Edwin, date not recorded | AutoCount edition and support contact: Edwin "will check". | Edwin |

Standing rules that apply to BIY: Base44 Publish only, never Activate. Never publish a client's overall Google or Facebook rating. Payment, deletions and contacting outsiders need Edwin's direct yes.

---

## 3. Architecture

### 3.1 The site (Stage 1)
- Preview (all noindex, host-level `X-Robots-Tag` from `preview/.htaccess`; no per-page robots meta except data-flagged sample and cart pages):
  - English: https://autoseo.my/preview/biy-home-store/
  - Malay: https://autoseo.my/preview/biy-home-store/ms/
  - Chinese: https://autoseo.my/preview/biy-home-store/zh/
- Server folder (through the Bridge only): `public_html/autoseo.my/preview/biy-home-store/`. A future live domain points at this same folder (one-switch go-live, rule 15).
- The site is built from the **shared AutoSEO trilingual template** (header, nav, language switch, footer, CTA, schema). Shop-specific parts (search-first header, category, brand, product and range templates, data loader, cart) are shared template pieces the next e-commerce client inherits. Repeated blocks live in one template; facts live in one data file (`facts.json`).
- Server-rendered HTML stays complete without JavaScript. Adding or removing a product means the data changes and the site rebuilds; no hard-coded product HTML.
- Identity: BIY's orange (#ED5623, sampled from the logo) with charcoal (#2B2B2B). Not a Shopee look.
- Brand allow-list on the site: Jotun, Nippon Paint, Dong Cheng, Bosch. Never shown: ICI (held), Makita, Hiltem, Stanley, Anchor, Riland, Atlas Copco, Daihuu.
- Branch codes (use exactly): `kota-tinggi-hq`, `kota-tinggi-jth`, `kota-masai`, `pontian`. Pontian shows no postcode (the source typo "8200" is not published).

### 3.2 Cart and WhatsApp checkout (Stage 1, being built by Claude)
- Add to cart on every card and product page; header cart icon with count; cart drawer; `/cart/`, `/ms/cart/`, `/zh/cart/` (noindex, not in sitemap).
- Storage: browser `localStorage` only (`biy_cart_v1`, `biy_branch_v1`, `biy_name_v1`). No cookies, no server calls, no phone field.
- Checkout = WhatsApp: the button opens `https://wa.me/60125688961?text=<encoded message>` with the cart lines, chosen pickup branch, optional name and note. No price in the message while `price_mode` is `whatsapp_only`. SAMPLE- SKUs are never shown or sent.
- Tracking: `data-ref` values `cart_open`, `whatsapp_cart_checkout`, `whatsapp_cart_page`; existing `p1-cta.js` unchanged; test taps with `?p1test=1` only.

### 3.3 `price_mode`
- Current value everywhere: `whatsapp_only` (in `facts.json` and in the feed envelope). Meaning: no price text, no Offer schema, no price in JSON-LD, "WhatsApp for price" on every card.
- Prices are **stored** by the API (so we can turn them on later) but **never published** while the mode is `whatsapp_only`.
- Other modes and the switch to show prices: **OPEN** (needs Edwin and BIY to confirm prices; not defined yet).

### 3.4 Sample data and the switch to live (Stage 1 to 2)
- Sample file: `products.sample.json` (48 SKUs, all prefixed `SAMPLE-`, no prices, no stock, no photos). Two Bosch items seen on biyhomestore.com have `is_sample=false`.
- One resolver `resolve_products()` in the generator reads `data/shop-config.json`:
  `live_feed = {"url":"https://biy-catalogue-api-f2aa4988.base44.app/api/feed/products","key_env":"BIY_FEED_READ_KEY","key_file":"<server path outside public_html, or null>","timeout_s":10,"min_active":1}`.
- Three states: (a) not configured: sample + label; (b) configured but empty or failing: sample + label; (c) **live** = HTTP 200, valid JSON, schema-valid records, at least 1 active product, none with `is_sample`. In (c) only live products are used (never mixed with sample), the label disappears, a snapshot is saved and `live_seen = true` is recorded.
- After `live_seen`, a failing feed keeps the last good snapshot; the site never falls back to sample again.
- Today the live feed is empty (`count 0`, vendor has not pushed), so the expected state is (b) or (a): sample + label "Sample products for preview" plus footer line "Sample data only. Not BIY's real stock or items."
- Rebuild trigger: on each Bridge publish, plus a `feed_version` check (`?meta=1` or ETag) in an existing scheduled batch. A rebuild every 30 to 60 minutes is enough. No new per-site cron without Edwin's OK. Claude must report which mechanism exists: **OPEN**.
- Read key delivery: environment variable `BIY_FEED_READ_KEY` first, then the `key_file` path. Never in chat, git, `public_html`, JSON, SITE-NOTES or reports. Built folder must not contain `biy_feed_` or Authorization text.

### 3.5 The backend: Base44 app "BIY Catalogue API" (Stage 2)
- Base44 app id: `6b076707c2f2e4cff2aa4988`. Published. Checkpoint `6b076854de695654e871e546`.
- **Base URL:** `https://biy-catalogue-api-f2aa4988.base44.app/api`
- Vendor routes: `/v1/...` under that base (for example `https://biy-catalogue-api-f2aa4988.base44.app/api/v1/ping`).
- Site feed (read only, separate key): `GET https://biy-catalogue-api-f2aa4988.base44.app/api/feed/products`. `?meta=1` returns `{ok, mode, feed_version, count}`; the full response carries an ETag (send `If-None-Match`, get 304 when unchanged).
- Why a separate app: the Bluehost Bridge holds the keys that publish to Bluehost, and a third-party vendor key must never sit in that blast radius. The AutoSEO Admin and Controller hold client and billing data. **Never mix with AutoKnowledge AI (6aa6abdb78ddeca50382b49e) or Quotation Master.** Claude must not edit this app; it only reads the feed.
- Built as: one TanStack server route `/api/v1/*` (all vendor endpoints) plus `/api/feed/products`. Entities: `BiyProduct` (prices, stock, images, specs embedded), `BiyRequestLog`, `BiyIdempotency`, `BiyRateWindow`, all admin-only. Local source copy: `/workspace/clients/biy-store/base44-app/`.
- Not built yet: photo download and copy (image URLs are stored as links), `BiyMapping` and an admin view for held products, key rotation UI. Fallback if Base44 proves too limited (raw body for HMAC, rate limiting): a PHP endpoint on Bluehost through the Bridge.
- Feed rules: only active, not deleted, brand-allow-listed products (or no brand); never prices or exact stock quantities; stock label `in_stock` or `ask`; `deleted[]` lists slugs for "no longer available" (noindex) or 410, kept out of the sitemap. Category in the feed is the raw AutoCount value, mapped by the site through `data/category-map.json` (unknown category: skip and list in the build report).
- Key names (values live only in `/workspace/clients/biy-store/secrets/biy-api-keys.env`, never printed): `BIY_VENDOR_LIVE_KEY`, `BIY_VENDOR_TEST_KEY`, `BIY_VENDOR_HMAC_SECRET`, `BIY_SITE_FEED_READ_KEY`, plus `*_SHA256` hashes in the Base44 app secrets (`BIY_VENDOR_LIVE_KEY_SHA256`, `BIY_VENDOR_TEST_KEY_SHA256`, `BIY_SITE_FEED_READ_KEY_SHA256`, `BIY_HMAC_REQUIRED=false`). **Name note:** the site-side environment variable is `BIY_FEED_READ_KEY`; it carries the same value as `BIY_SITE_FEED_READ_KEY` in the keys file. Keep this mapping.
- Key delivery to the vendor: separate private channel, never plain email. Not sent. Channel is Edwin's decision.
- Rotation: new key row, 7 days overlap, disable the old one. Kill switch: set the key row `status = disabled`.

### 3.6 Data flow
`AutoCount (BIY)` -> `vendor connector (their server)` -> **push** to `/v1/...` -> Base44 validates and stores -> read-only `/feed/products` -> site resolver at build time -> fully rendered EN/BM/ZH pages published through the Bridge. We never log in to AutoCount; "the vendor" is whoever writes the connector.

---

## 4. API contract summary (full text: `biy-autocount-push-api.md`, v1.0, 26 Nov 2026)

- Auth: `Authorization: Bearer <key>` plus `Content-Type: application/json`. Test key starts `biy_test_`, live key starts `biy_live_`; the key decides the mode. HTTPS only. Optional HMAC-SHA256 request signing (`X-BIY-Timestamp`, `X-BIY-Signature`), currently not required.
- Endpoints:

| Endpoint | Use | Limit |
|---|---|---|
| `GET /v1/ping` | check key, mode, limits | |
| `POST /v1/products/upsert` | create or update full products (omitted fields cleared, except `images`) | 100 per request |
| `POST /v1/stock/update` | stock only, every 5 to 15 minutes | 500 rows |
| `POST /v1/prices/update` | price only (stored, not shown) | 500 rows |
| `POST /v1/products/deactivate` | hide (reversible) | 100 SKUs |
| `POST /v1/products/delete` | remove (marker kept 90 days) | 100 SKUs |
| `POST /v1/products/{sku}/images` | base64 upload, only if no public URL | 3 MB, 8 per product |
| `GET /v1/products/{sku}` | what we hold, incl. `published` and image status | |
| `GET /feed/products` | site only, read-only feed key | |

- Product fields: `sku` (AutoCount ItemCode, never changes), `title`, `description`, `short_description`, `category`, `brand`, `model`, `barcode`, `unit`, `group{code,name,variant_label}` (same `group.code` = sizes of one product page), `prices[]` (money as strings), `stock[]` (`branch`, `qty`), `images[]` (https URL, `alt`, `primary`), `specs[]`, `active`, `updated_at` (UTC).
- Envelope: `ok`, `mode`, `request_id`, `summary`, `results[]` (per item: created, updated, unchanged, skipped_stale, rejected with `code`). HTTP 200 with `ok:true` can still contain rejected items.
- Behaviour: `Idempotency-Key` header on every POST (24 h); newer `updated_at` wins (`skipped_stale`); 60 requests per minute per key; test mode is stored separately and never reaches the feed; `?dry_run=true` on the live key validates and saves nothing; body max 1 MB.
- Held products: unknown category or branch is stored with `held_reason` and `published=false`.
- Support contact and AutoCount edition in the vendor doc are still placeholders (section 8).
- Smoke test: `/workspace/clients/biy-store/api/tests/smoke.py` (reads keys from the keys file, never prints them).

---

## 5. File map

### 5.1 Box (`/workspace/clients/biy-store/`)
| Path | What |
|---|---|
| `BIY-PROJECT.md` | this file (box master) |
| `README.md` | client facts and evidence, open questions from 25 Nov |
| `master-brief-2026-11-25.txt` | Edwin's original master prompt (3 phases) |
| `blueprint.md` | Phase 1 blueprint (sitemap, wireframes, URL rules, DB shape, SEO checklist, roadmap) |
| `drop/` | Stage 1 data drop: `facts.json` (single source of truth), `brands.json`, `categories.json`, `products.json`, logos, favicon, `og.jpg`, `manifest.json` |
| `drop2/` | `products.sample.json`, `product-feed.schema.json`, `autocount-push-api.md` |
| `api/` | `biy-autocount-push-api.md` and `.pdf` (vendor doc), `integration-design-and-backend-plan.md` (internal), `tests/smoke.py` |
| `base44-app/` | local source copy of the BIY Catalogue API |
| `verify/` | phone screenshots of the preview |
| `secrets/biy-api-keys.env` | key values (folder 700, file 600). **Never read aloud, printed or uploaded.** |
| `/workspace/claude-msgs/2026-11-25-biy-store-build.txt` | Stage 1 build brief (preview v1/v2) |
| `/workspace/claude-msgs/2026-11-26-biy-cart-sample.txt` | v3 brief: cart + sample fallback |
| `/workspace/claude-msgs/2026-11-26-biy-feed-addendum.txt` | feed addendum to v3 |
| `/workspace/claude-msgs/2026-11-26-biy-sync-protocol.txt` | brief to add this file to Claude's repo (not sent until Edwin relays it) |

### 5.2 Drive
| Item | ID |
|---|---|
| Folder `Client Photo Banks / biy-home-store` (view-only link) | `1cZwatA8R7hyUHR03RBSngvVG2szccszK` |
| Parent folder `Client Photo Banks` | `1JGsa5NGX845NEGT6GnYg8kLlO9WmaCWp` |
| `BIY-PROJECT.md` (this file, mirror; update this file, never add a duplicate) | `1RIV8N-XrxFeCmCXHA8VVr_1DWR_sw1Fx` |
| `facts.json` | `1iABxn00y-hNp6a5HFm3C5yTFa0AWh69x` |
| `brands.json` | `1KsWZ2nSMBjc8wUa0KZbNWMBexgW-WUft` |
| `categories.json` | `1344H3Ug1JiHbA-UgNkFWJlG_i8-ftJoX` |
| `products.json` | `1WksmqG1Mg5UKBAPGCEpLMTFFL8KEvbs_` |
| `products.sample.json` | `1PBmLHgqqUv_UlPGqD3c18UtQ0C0rzsPX` |
| `product-feed.schema.json` | `1sM3kNh6tjE-7yHsT6qZ8WnspNg20dGJ4` |
| `autocount-push-api.md` | `1M6LusLycAbO5kEdPXHO96lj9_kfFGBEi` (**Drive copy is older: 16,596 bytes vs 16,939 bytes on the box, made before the base URL was added. Refresh before the vendor or Claude relies on it.**) |
| `blueprint.md`, `README.md`, `keyword-patterns.md`, `manifest.json` | `1bcyig1xt5sWDc7DluGUPZ5qhj7_5YOxw`, `1X3_x3kX9FmMr2fpJJ2kk4K-2_brQLaJ6`, `1iQKA7R7_odYRQ_pLEwPFL73HWp90Z5Ev`, `1QkyFW1FWIoZ9LgEu49ES5SjkVRpjzolx` |
| `logo-mark.png`, `logo-mark.webp`, `favicon-512.png`, `og.jpg` | `19JaSxBe0_Gm2mDN20aLn-O0yBVOg0BPR`, `1rzyvUFmFcQvAB0XDG-8BYhDhdXTO821y`, `1sRJldM0cQbuvZEWJ4bOxLIuugwJhGyVg`, `17XI9D7UZN14NwfXfuGBLwwF8whW4WZyX` |

### 5.3 Other systems
- Claude's repo: this file is committed at `docs/BIY-PROJECT.md`. Repo name or URL: **OPEN** (not recorded in any source Grok holds; Claude to state it in its first report).
- Controller client slug: `biy-home-store` (Controller app 6ac7f2548a9c3877449e2772). Live domain, status and billing entry: see section 7.
- Bluehost Bridge (Base44 app 6ac6d47b4ec84148578914c7): all reads and writes to Bluehost go through it, with fingerprints (`expected_sha256`), SITE-NOTES log lines and Publish only.
- Site notes: the site's `SITE-NOTES` file on the server (read it through the Bridge before any edit, rule 0).

---

## 6. Fixed rules for BIY

1. **Rule 0:** the server is the source of truth. Before any site edit: check MASTER-RULES version, read SITE-NOTES, pull the fresh live file through the Bridge, write back with `expected_sha256`. Never rebuild from an old local or repo copy.
2. **Base44: Publish only, NEVER Activate.** Never mix BIY with AutoKnowledge AI or Quotation Master.
3. **No secrets in this file, in git, in `public_html`, in chat or in reports.** Use names only (for example `BIY_FEED_READ_KEY`). No phone number in this file except the public business WhatsApp (wa.me/60125688961).
4. **noindex only on the preview** (host-level header). Go-live switches canonical, hreflang, schema, sitemap and robots from one config; do not hard-code per-page noindex that would have to be stripped later (exception: data-flagged sample and cart pages).
5. **Visual changes: show ONE sample first** (390 px) before rolling out.
6. No prices, no payment, no accounts, no ICI, no new brands until Edwin says so. Never invent product data, claims or photos. Never publish an overall Google or Facebook rating.
7. Templates and one data file (template-first); media sizing rules; phone check at 360 and 390 before reporting.
8. Money, DNS, deletions and contacting outsiders (including the AutoCount vendor) need Edwin's direct yes.
9. Do not edit the BIY Catalogue API app from the site job.

---

## 7. Current status per stage (updated 26 Nov 2026, 7:09am SGT)

**Stage 1: IN PROGRESS.**
- Preview v2 (marketplace layout) is live: `/`, `/ms/`, `/zh/` return 200 (checked 26 Nov, 7:07am).
- Cart: **not built yet.** `/cart/` returns 404 on the preview (checked 7:07am). Claude has had the v3 brief since 6:51am and the cart job is running in the thread "Add enquiry basket to BIY Home Store". Feed addendum follows in the same thread (relay status OPEN).
- Sample data resolver and label: not live yet (part of the same job).
- Go-live on biyhomestore.com: **not done.** Started on 25 Nov through the SiteGiant account (credentials are in the vault, not here); domain control is OPEN (section 8). Controller client record: live domain and status Live not set; billing-list entry: **OPEN** (awaiting Edwin's fee).

**Stage 2: BACKEND BUILT, VENDOR NOT STARTED.**
- BIY Catalogue API published and smoke-tested with the test key (26 Nov, ~7:00am). Live feed is empty (`count 0`).
- Vendor doc (`.md` and `.pdf`) written with live base URL; not sent. Support contact and AutoCount edition still placeholders. No keys delivered.
- Site resolver for the feed: in the Stage 1 cart job (config and tests only; no real live state until the vendor pushes).

**Stage 3: NOT DEFINED (OPEN, Edwin).**

---

## 8. Open items

| # | Item | Owner |
|---|---|---|
| 1 | AutoCount edition: Accounting (on-prem, AOTG API) or Cloud Accounting, and the vendor's name | Edwin ("will check") |
| 2 | Support contact for the vendor doc (section 10 placeholder) | Edwin |
| 3 | How the vendor gets its keys (private channel; test key first) and when the vendor doc is sent | Edwin |
| 4 | Domain login for biyhomestore.com: Cloudflare, registrar or SiteGiant admin; who controls DNS; whether SiteGiant checkout stays running; full 301 map from old SiteGiant URLs | Edwin |
| 5 | Confirm the WhatsApp number used for enquiries (default wa.me/60125688961; the old site shows another main number) and whether any branch has its own | Edwin |
| 6 | Prices: publish selling prices online or keep "WhatsApp for price"; member and trade price display; when and how to leave `whatsapp_only` | Edwin and BIY |
| 7 | Branch details: opening hours per branch, Pontian postcode (source prints a 4-digit typo), Google Business Profile access, Facebook admin and logo files | Edwin |
| 8 | Whether ICI (Dulux) is carried and may be shown; any other brand outside the four | Edwin |
| 9 | Stage 3 scope and order | Edwin |
| 10 | Billing-list amount for the Controller (rule A0 gate for go-live); the project is larger than a normal AutoSEO site | Edwin |
| 11 | Product photos: who owns them (vendor may have none; Drive photo bank still works for hero images); stored copy of vendor photos is not built | Edwin and Grok |
| 12 | Category mapping AutoCount item groups to site categories, and branch location codes in AutoCount (mapped when the first push arrives) | Grok with the vendor |
| 13 | Cart build (v3 + feed addendum): finish, publish, report the three resolver results, decoded WhatsApp texts, screenshots, rebuild-trigger answer | Claude |
| 14 | State the name of Claude's repo, then commit this file as `docs/BIY-PROJECT.md` (see sync brief) | Claude |
| 15 | Add `BIY_FEED_READ_KEY` to Claude's environment, or confirm the key-file route | Edwin or Grok (approved route) |
| 16 | Verify the finished cart: phone screenshots at 360 and 390 (EN, MS, ZH), WhatsApp link decode, resolver states, grep for secrets and prices, live fetch of all pages | Website Manager (Grok) |
| 17 | Refresh the Drive copy of `autocount-push-api.md` (older than the box copy) | Website Manager (Grok) |
| 18 | Build still missing in the backend: photo copy, `BiyMapping` admin view, key rotation UI | Grok (after vendor starts) |
| 19 | Confirm Claude received the feed addendum in the cart thread | Grok |

---

## 9. Reference: Edwin's original 3 phases (25 Nov master brief)

- Phase 1: SEO and product catalogue, WhatsApp enquiry, AutoCount-ready data, local SEO. No login or payment.
- Phase 2: shopping cart, add to cart, guest checkout, preorder submission, customer contact details, order confirmation, WhatsApp order communication. No account registration.
- Phase 3: customer accounts, membership, loyalty, online payment gateway, order history, order tracking, contractor pricing, repeat purchases.
The 26 Nov stages (section 1) now govern. The enquiry cart from Phase 2 moved into Stage 1; the remaining Phase 2 and Phase 3 items are not yet assigned to a stage (Stage 3 is OPEN).

---

## 10. Sync protocol (Grok, Website Manager, and Claude Code)

1. **Before any BIY job** (a brief, a fix, a check, a build): read this whole file. Master copy on the box: `/workspace/clients/biy-store/BIY-PROJECT.md`. Claude's committed copy: `docs/BIY-PROJECT.md` in its repo. Drive mirror: file `1RIV8N-XrxFeCmCXHA8VVr_1DWR_sw1Fx` in folder `1cZwatA8R7hyUHR03RBSngvVG2szccszK`. If the copies differ, the one with the newest change-log entry wins; say so and reconcile.
2. **After the job:** add one line to the change log (section 11), update the status (section 7) and the open items (section 8), and update the decisions log (section 2) if Edwin decided something. Do not write secrets.
3. **Claude** includes the diff of its change-log entry in its done report. **Website Manager** copies the newest version to the box master and re-uploads the Drive mirror (update the existing file, never a duplicate), then tells Claude the new Drive file content when a brief goes out.
4. Edwin's new decisions are written to the decisions log by whoever hears them first, with date and time in SGT and "Edwin" as the decider.
5. If a brief and this file disagree, stop, report the conflict, and let Edwin decide. Never resolve it by guessing.
6. Anything unknown is marked **OPEN**. Never invent facts, keys, URLs or numbers.

---

## 11. Change log

| Date and time (SGT) | Who | What |
|---|---|---|
| 26 Nov 2026, 7:09am | Website Manager (Grok) | Created this file from the plan doc, vendor doc, three Claude briefs, memory and Edwin's messages. Drive mirror created (file ID `1RIV8N-XrxFeCmCXHA8VVr_1DWR_sw1Fx`). Sections 1 to 11 filled; Stage 3 OPEN; found Drive copy of `autocount-push-api.md` is older than the box copy; noted the key-name mapping `BIY_FEED_READ_KEY` = `BIY_SITE_FEED_READ_KEY`. |

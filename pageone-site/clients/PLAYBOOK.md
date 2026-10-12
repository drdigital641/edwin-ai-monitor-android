# Client website playbook (Claude builds every client site by hand)

The controller app's Clients page queues jobs on the `Client` record (`design_job`). The hourly
"Page One Claude worker" routine picks them up. DMTS (`clients/dmts/`) is the reference standard.

## Jobs
- `mockup_queued`: after Edwin imports the client's old site. Build ONE page: a home-page mock-up.
- `site_queued`: after Edwin presses Activate (the Client has `domain`). Build the full website.
- `design_notes` holds Edwin's requested changes; apply them, then keep them (don't clear).
- While working set `design_job` to `mockup_working` / `site_working` and keep `design_step` (plain
  words) and `design_progress` (0-100) current. Finish with `mockup_done` / `site_done`,
  `design_progress: 100`, `design_done_at`, `custom: true`. If something only Edwin can give is
  missing (no phone/WhatsApp anywhere, unreadable old site), set `needs_you` and say exactly what.

## Where things live
- Source: `pageone-site/clients/<slug>/` with `build.py` (copy, FAQ, business details at the top),
  `source/` (captured old pages, photos) and `site/` (output). Commit and push to the working branch.
- Published to the `pageone` site at `preview/<slug>/` via the Bluehost Bridge (claim a BridgeLock
  first, release after, leave a BridgeNote). Never move files on activation: the client's domain is
  pointed at `public_html/website_b1ec45f5/preview/<slug>/`.
- Add a blank `index.html` to every image folder (no folder listings).

## Standard (match DMTS)
- Real photos and logo from the old site (resize to max 2000 px, webp, sensible names). Brand colour
  from their logo/site. Clean system font stack, sticky header, top bar with phone/WhatsApp,
  icon cards, trust strip from TRUE facts only, how-it-works steps, gallery, FAQ, contact cards with
  map link, strong WhatsApp CTAs plus a floating WhatsApp button. Mobile-first: no horizontal scroll
  at 390 px; check 390 and 1280 px in headless Chromium before publishing.
- All internal links relative (same files work at both addresses).
- `<meta name="p1-site" content="<slug>">` on every page (the go-live check looks for it).
- Footer credit: "Website & SEO by Page One Singapore" linking to https://pageonesingapore.com/.
- WhatsApp tracker (same CtaClick snippet as dmts.js, `site: '<slug>'`), skipped on
  pageonesingapore.com.

## Robots and duplicates (standard)
- pageonesingapore.com/robots.txt disallows `/preview/` in every group, so preview copies are never
  crawled under pageonesingapore.com. Each client domain serves its own folder's `robots.txt`
  (Allow all + its sitemap). Never remove that Disallow; never add client folders anywhere else.

## Go-live (the same for every client)
1. Edwin presses Activate with the client's domain (Claude builds or finishes the full site).
2. cPanel → Domains → Create a new domain (addon domain): the client's domain, untick "Share
   document root", document root `public_html/website_b1ec45f5/preview/<slug>`.
3. The client only changes DNS: A record @ → 173.254.31.20, CNAME www → their domain.
4. AutoSSL issues https; the Clients page checklist confirms DNS, site, https and Search Console.

## Mock-up specifics
- One page only (index.html + css/js + img). `noindex, nofollow`. Canonical = the preview URL.
  Yellow strip: "Preview by Page One Singapore. This is a draft of your new website."
- Set `preview_url` = https://pageonesingapore.com/preview/<slug>/ and `status` = `preview`.

## Full site specifics
- Home, Services (or one page per main service when there are several), About, Contact, plus any
  page the business clearly needs (gallery, locations). Indexable. Canonical, Open Graph and
  structured data (LocalBusiness + FAQPage + BreadcrumbList) name `https://<domain>/`.
- `robots.txt` and `sitemap.xml` for the domain, `llms.txt`, and the IndexNow key file
  `<indexnow_key>.txt` (key from the Client record).
- Remove the preview strip. The page must answer the go-live check on the domain.

## Before/after reports (every client, every SEO run or Boost)
- Before touching anything, capture the old site while it is still live: run the public checker
  (`siteCheck` basics) on the old home page, run Lighthouse mobile locally
  (`npx lighthouse@12.2.1 <url> --form-factor=mobile` with CHROME_PATH=/opt/pw-browsers/chromium),
  take 390 px and 1280 px screenshots (puppeteer-core with a real viewport; Chromium's
  `--screenshot --window-size` crops wide layouts and misleads), and save them in
  `clients/<slug>/before/` with a README table. Attach the share code and speed to the Client's
  onboarding ScoreRecord (share_id, speed_json, speed_score) and to the SiteCheck row (speed_json).
- The new site must beat the old one on every measure. Aim for 100 on the checker for every page.
- Every ScoreRecord now saves its own shareable report (share_id → https://pageonesingapore.com/?report=<id>#check):
  go-live (with a speed test), fixes, routine score changes. After an SEO run or Boost, record a
  ScoreRecord with kind `boost` the same way, so the client's history shows the measured result.
- The Controller's score history shows a Report link per entry, and "Copy progress summary" includes
  the before and latest report links.

## Content rules
- Only facts from the old site and Edwin. Never invent prices, reviews, ratings, years, awards,
  guarantees or response times. No "best", "No. 1", "cheapest".
- Plain, friendly Singapore English. No exclamation marks.
- The only phone numbers are the client's own.

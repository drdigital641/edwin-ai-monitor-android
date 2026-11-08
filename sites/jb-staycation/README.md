# JBStaycation demo preview (built 8 Nov 2026)

Existing site: https://jbstaycation.com/. Target preview: https://pageonesingapore.com/preview/jb-staycation/. `python3 build.py` writes 15 pages + assets into `site/`; `python3 check.py` validates JSON-LD, links, sitemap. Go live = change BASE in build.py and rebuild. Rename `site/htaccess.txt` to `.htaccess` via cPanel (no X-Robots-Tag; preview hiding is server-side).

## Facts and sources
Client site facts (8 Nov 2026): see build.py HOUSES. Photos hot-linked from jbstaycation.com via the IMAGES dict (swap to self-hosted before go-live).
Official travel sources (checked 8 Nov 2026): LTA RTS project page; LTA news release 2 Oct 2026 (RTS service now expected Feb 2027, subject to safety certification); ICA QR code clearance page (updated 27 Oct 2026; passport still required); ICA driving in and out of Singapore (link only).
Left out: 89 happy stayers, Lumina Glasshouse, Prima bedroom count and 900 sq ft, SGD prices, ratings schema, RTS fares, /terms/.
CTA tap script (cta.js) copied from aivs.js v3 with site id jb-staycation; it does not run on pageonesingapore.com or localhost.

## CONFIRM
- Legal/business name of the host (kept off the site).
- Prima bedrooms: client site says 3 in the header and 5 in text/gallery. Page says "multiple bedrooms" only.
- Prima "Minimum 2": assumed nights; page says "message us to confirm".
- Prima 900 sq ft (as stated by client) looks small for 20 guests; left off the page.
- Prima check-in/out times and house rules (none on client site).
- Deposit, cancellation and payment terms (client T&C is an unfilled template; no /terms/ page built).
- SGD equivalents: not shown until Edwin agrees.
- Is Lumina Glasshouse still offered? (only in one review; not listed).
- Google Business Profile, Airbnb, social links, email (none known; no sameAs).
- Brand colours/fonts: could not be read (only theme-color #f7f8f9 visible); palette is an estimate of a warm, calm look.
- Photo ratios and og:image size (1200 px wide, 1.91:1) not verifiable from the sandbox; self-host photos before go-live.
- Host drive times (Tuas 10 min / Woodlands 15 min / KSL etc.) are as stated by the host, not independently timed.
- Does the photo set include people/cars (privacy) and may we use them? (client own photos assumed).

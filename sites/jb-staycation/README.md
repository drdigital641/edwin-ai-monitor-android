# JBStaycation demo preview (built 8 Nov 2026)

Existing site: https://jbstaycation.com/. Target preview: https://pageonesingapore.com/preview/jb-staycation/. `python3 build.py` writes 15 pages + assets into `site/`; `python3 check.py` validates JSON-LD, links, sitemap. Go live = change BASE in build.py and rebuild. Rename `site/htaccess.txt` to `.htaccess` via cPanel (no X-Robots-Tag; preview hiding is server-side).

## Facts and sources
Client site facts (8 Nov 2026): see build.py HOUSES. Photos: the client's own files from photos-src/, copied by build.py into site/img/ (same filenames) with 480px thumbs in site/img/thumb/ (needs Pillow; falls back to originals). Room groups, captions and picks are in ROOMS/BENTO/CARD_IMG in build.py. No hot-linking.
Official travel sources (checked 8 Nov 2026): LTA RTS project page; LTA news release 2 Oct 2026 (RTS service now expected Feb 2027, subject to safety certification); ICA QR code clearance page (updated 27 Oct 2026; passport still required); ICA driving in and out of Singapore (link only).
Left out: 89 happy stayers, Lumina Glasshouse, Prima bedroom count and 900 sq ft, SGD prices, ratings schema, RTS fares, /terms/.
CTA tap script (cta.js) copied from aivs.js v3 with site id jb-staycation; it does not run on pageonesingapore.com or localhost.

## v3 changes (8 Nov 2026)
One FAQ per page (home: 8 host-stated questions, one visible H2, matching FAQPage); WhatsApp prefills "[House: Prima|Landak|not sure yet] Hi JBStaycation, I'd like to check dates. Group size: ___ Dates: ___" everywhere; sticky mobile WhatsApp bar on every page; CTA after each house card, gallery, FAQ; house pages: photo gallery then CTA first, long text in "About this house"; Prima bedrooms shown as "ask us", minimum "Minimum 2 (see WhatsApp for details)"; Landak amenity list per brief; review labelled as Lumina Glasshouse; keyword-led titles/H1/descriptions. `python3 wa_check.py` decodes every wa.me link and prints distinct prefills.

## CONFIRM
- Legal/business name of the host (kept off the site).
- Prima bedrooms: client site says 3 in the header and 5 in text/gallery. Pages say "Bedrooms: ask us" (no count shown).
- Prima "Minimum 2": source gives no unit; page says "Minimum 2 (see WhatsApp for details)" and never "2 nights".
- Prima 900 sq ft (as stated by client) looks small for 20 guests; left off the page.
- Prima check-in/out times, quiet hours, deposit amount and house rules (none verified; pages say ask us on WhatsApp).
- Review: only "Very nice place very clean" (Philip, Singapore) exists, from a stay at Lumina Glasshouse; shown with that label. Remove if Lumina is no longer offered.
- Deposit, cancellation and payment terms (client T&C is an unfilled template; no /terms/ page built).
- SGD equivalents: not shown until Edwin agrees.
- Is Lumina Glasshouse still offered? (only in one review; not listed).
- Google Business Profile, Airbnb, social links, email (none known; no sameAs).
- Brand colours/fonts: v2 uses the client site tokens (navy #0a1f38, amber #e8a33d, page #f7f8f9) and Geist from Google Fonts.
- Photos are self-hosted in site/img/ (client files). img-1806 (brand hero, dusk bungalow) does not visibly match either house: confirm which house it is or if it is a render.
- Prima: 13 photo files on the client site are exact duplicates under other names (e.g. backyard = rooftop-terrace); only one of each is used.
- Host drive times (Tuas 10 min / Woodlands 15 min / KSL etc.) are as stated by the host, not independently timed.
- Does the photo set include people/cars (privacy) and may we use them? (client own photos assumed).

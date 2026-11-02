# cleanicdetailing.com - SEO fix pass 2 Nov 2026

Edits made live via Bridge invoke_edit_file (each backed up, byte-verified). Static copies in front of WordPress; Endurance cache may hold old copies.

| site | fix | status |
|---|---|---|
| cleanic | Remove AggregateRating 5.0/405 from LocalBusiness JSON-LD on article pages | DONE on 31 static copies: mitsubishi, mazda, kia, hyundai, subaru, volvo, audi, lexus, car-fumigation-safe-during-pregnancy, grab-driver, allergy-friendly, asthma, car-flooded-inside, bed-bugs, car-fumigation-jb-vs-singapore, car-fumigation-cost-2026, car-interior-cleaning-singapore-full-guide, pet-urine, car-dashboard, car-disinfection-service, car-aircon-smells-bad, car-carpet, insects-in-my-car, bees, spider, lizard, ants, car-odour-removal-3, car-mould-removal-3, cockroach-in-car-2, car-cockroach-fumigation, mirakn-dry-gas. Home untouched. `review` array nodes left in place (not in list). |
| cleanic | Same, WordPress-only pages (no static copy; 29 pages still serve 5.0/405) | SKIPPED: not in Bridge folders (WP database/plugin). Edwin step E1 |
| cleanic | Broken JSON-LD on /mitsubishi-interior-cleaning-fumigation-singapore/ | DONE: FAQPage block had literal "n" instead of newlines inside a `<p>`; rewritten as valid JSON matching the visible FAQ text. Not fixed (not listed): 35 visible stray "n" paragraphs (`<p>n</p>`) from the same import bug; probably on other pages too |
| cleanic | Remove /car-steam-cleaning-singapore-2/ and /emergency-car-detailing-singapore/ from sitemap | DONE (sitemap.xml). Pages still return 200, no 301/canonical change made |
| cleanic | One H1: /car-fumigation-singapore/, /mirakn-dry-gas-fumigation-singapore/ | DONE: banner h1.section-title demoted to h2 (same class) |
| cleanic | One H1: /car-grooming-singapore/, /home-glowup/ | SKIPPED: WordPress-only pages. Edwin step E1 |
| cleanic | Schema + OG on /articles/ | DONE: og:*, twitter:*, CollectionPage + BreadcrumbList JSON-LD added (lang already en-SG) |
| cleanic | Shorten 78 long titles | NOT DONE: 76 titles >65 chars. Needs per-page rewrite, out of budget. Suffix swap `&#8211; Cleanic Detailing` -> `| Cleanic` alone fixes only 9 of the 44 static ones |
| cleanic | lang en-SG on WP templates | NOT DONE: all pages except home and /articles/ are en-US. Edwin step E1 |
| cleanic | WebP | SKIPPED: Bridge cannot write large binaries. Edwin step E2 |

## Edwin steps (Cleanic)
E1. WordPress admin: Settings > General > Site Language "English (Singapore)" (fixes lang). For the WP-only pages remove AggregateRating from the LocalBusiness schema (SEO/schema plugin or theme) and demote the duplicate H1 on /car-grooming-singapore/ and /home-glowup/. WP-only pages with rating: sand-dirt-car-interior, pet-hair-removal-car, why-is-my-car-interior-always-damp, water-leaking-into-car, wet-carpet-in-car, sewage-smell-in-car, mosquito-in-car, preventing-cockroach-infestations-in-cars, centipede-in-car, car-grooming-singapore, durian-smell, snake-in-car, dead-animal-smell, rotten-smell, food-spill-smell, milk-spilled-in-car-smell, car-interior-stain-removal, car-interior-hygiene, sanitise-car-for-baby, leather-car-seat-cleaning, car-seat-cleaning, pet-smell-in-car, cigarette-smell-in-car, rat-in-my-car-engine, porsche-panamera-total-refresh, mobile-car-detailing-singapore-the-convenient-way..., home-glowup.
E2. cPanel: convert large wp-content/uploads JPGs to WebP; the Newfold "WebP Existing Image Redirect" rule in .htaccess serves a .webp sibling automatically.
E3. .htaccess (cPanel, back up first). Currently http://www.cleanicdetailing.com/ returns 200 on plain http. Replace the block between "# BEGIN Cleanic www Redirect" and "# END Cleanic www Redirect" with:
```
# BEGIN Cleanic www Redirect
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} !^www\.cleanicdetailing\.com$ [NC]
RewriteRule ^(.*)$ https://www.cleanicdetailing.com/$1 [R=301,L]
</IfModule>
<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=31536000"
</IfModule>
# END Cleanic www Redirect
```
Test: curl -I http://www.cleanicdetailing.com/ and http://cleanicdetailing.com/ give one 301 to https://www.; https responses carry strict-transport-security. The 404 test also chains via 301 today; this single rule removes the extra hop.
E4. Purge Endurance cache after the edits so the static copies show the new schema.

Probe commit d35fc8989 adds .github/probe/audit.sh (per-page title length, h1 count, AggregateRating, lang for sitemap URLs of the 3 sites).

## Pass 2 (continuation helper, 2 Nov 2026)
- Titles: NOT DONE (this helper ran out of budget after the SG Garage edits); 79 of 88 sitemap pages still >65 chars (probe 09:06 UTC). Next: per-page rewrite on the 44 static copies via invoke_edit_file (title + og:title). Skip /car-interior-cleaning-singapore-full-guide/ and /car-cockroach-fumigation-singapore/ (1 Nov near-miss pages, judge 15 and 29 Nov). Homepage not touched, so no cache purge needed (if edited later: cleanic-force-purge-home-20261004.php).
- Live probe 09:06 UTC: 88 pages; AggregateRating on 29 pages (was 59 before; the remaining ones are WordPress-only, Edwin step E1); lang en-US on the non-static pages (E1); 2 pages with h1 != 1 (WP-only /car-grooming-singapore/, /home-glowup/); http://www.cleanicdetailing.com/ still 200 on plain http (E3); 404 test still goes through a 301.

## Pass 3 - title shortening on static copies (2 Nov 2026, continuation helper)
Done via Bridge invoke_edit_file (each edit backed up, byte-verified by the bridge): **53 static pages** got a shorter `<title>` (brand suffix `| Cleanic`, filler trimmed, main term kept first; no prices/facts changed). og:title and twitter:title were set to the same short text where they had matched the title (51 pages; /vomit-cleaning-service-singapore/ has no twitter:title; /car-fumigation-singapore/ and /mirakn-dry-gas-fumigation-singapore/ keep their own already-short og/twitter titles, 62 and 56 chars).
Skipped on purpose: homepage (no cache purge needed), /car-interior-cleaning-singapore-full-guide/, /car-cockroach-fumigation-singapore/ (near-miss, judge 15 + 29 Nov). Already <=65, untouched: how-cleanic-detailing-gets-found-on-google (52), how-to-prepare-car-for-fumigation (54), /articles/ (56), /about/, /contact/, /home-glowup/.
Known gap: /kia-interior-cleaning-fumigation-singapore/ - `<title>` done (55 chars) but the og:title and twitter:title edits failed the bridge byte-verification 3 times (original restored each time), so they still read "Kia Car Interior Cleaning and Fumigation Singapore | Cleanic Detailing" (73). Retry later or edit by hand.
Not re-probed live yet (Endurance cache may serve old titles for a while). Re-run .github/probe/audit.sh to confirm; expected remaining >65: only the WordPress-only pages below, plus kia og/twitter.

Static titles now (base | Cleanic): Mitsubishi/Kia/Hyundai/Subaru/Mazda Interior Cleaning and Fumigation Singapore; Volvo/Lexus Interior Fumigation and Steam Cleaning Singapore; Audi Interior Fumigation and Detailing in Singapore; and 41 more articles (see live probe).

### WordPress-only pages left (no static copy; Edwin edits in WordPress/Yoast "SEO title"). Paste the short title; Yoast adds no suffix if you use the whole field, so the brand is included.
| URL slug | now (chars) | proposed title |
|---|---|---|
| /why-is-my-car-interior-always-damp-singapore/ | 68 | Why Is My Car Interior Always Damp? \| Cleanic |
| /water-leaking-into-car-singapore/ | 83 | Water Leaking Into Your Car? Causes and Fixes \| Cleanic |
| /wet-carpet-in-car-singapore/ | 83 | Why Is My Car Carpet Wet? What to Do \| Cleanic |
| /sewage-smell-in-car-singapore/ | 88 | Why Does My Car Smell Like Sewage? \| Cleanic |
| /mosquito-in-car-singapore/ | 94 | Mosquitoes in Your Car: Why and How to Stop Them \| Cleanic |
| /preventing-cockroach-infestations-in-cars/ | 94 | How to Prevent Car Pest Infestations in Singapore \| Cleanic |
| /centipede-in-car-singapore/ | 99 | Centipede in Car Singapore: How to Remove It \| Cleanic |
| /car-grooming-singapore/ | 78 | Car Grooming Singapore \| Mobile On-Site Service 24/7 \| Cleanic |
| /durian-smell-in-car-singapore/ | 77 | How to Remove Durian Smell From Your Car \| Cleanic |
| /snake-in-car-singapore/ | 70 | Snake in Car Singapore: What to Do Right Now \| Cleanic |
| /dead-animal-smell-in-car-singapore/ | 82 | Dead Animal Smell in Your Car? How to Remove It \| Cleanic |
| /rotten-smell-in-car-singapore/ | 79 | Why Does My Car Smell Rotten? Causes and Fixes \| Cleanic |
| /food-spill-smell-in-car-singapore/ | 71 | How to Remove Food Spill Smells From Your Car \| Cleanic |
| /milk-spilled-in-car-smell-singapore/ | 105 | Spilled Milk in Your Car? Remove the Smell \| Cleanic |
| /car-interior-stain-removal-singapore/ | 105 | Car Interior Stain Removal Singapore: Old Stains \| Cleanic |
| /car-interior-hygiene-singapore/ | 90 | Car Interior Hygiene Singapore: Is Your Cabin Dirty? \| Cleanic |
| /sanitise-car-for-baby-singapore/ | 95 | How to Sanitise a Car for a Baby in Singapore \| Cleanic |
| /leather-car-seat-cleaning-singapore/ | 115 | Leather Car Seat Cleaning Singapore: Clean and Protect \| Cleanic |
| /car-seat-cleaning-singapore/ | 102 | Car Seat Cleaning Singapore: Fabric and Leather Seats \| Cleanic |
| /pet-smell-in-car-singapore/ | 72 | How to Remove Pet Odour From Your Car Interior \| Cleanic |
| /cigarette-smell-in-car-singapore/ | 77 | How to Get Cigarette Smell Out of a Car \| Cleanic |
| /rat-in-my-car-engine-singapore/ | 94 | Rat in Your Car Engine or Interior? How to Fix It \| Cleanic |
| /porsche-panamera-total-refresh-singapore/ | 124 | Porsche Panamera Total Refresh Singapore \| Cleanic |
| /mobile-car-detailing-singapore-the-convenient-way-to-keep-your-car-immaculate/ | 104 | Mobile Car Detailing Singapore: On-Site Convenience \| Cleanic |

25 WordPress-only pages >65 chars. Each proposal is <=65 chars (most <=60). /home-glowup/ (37), /about/ (34), /contact/ (36) are already short. Note these pages are en-US/AggregateRating issues per E1 above; the same WordPress session can fix those.

# sggarage.com - SEO fix pass 2 Nov 2026

| site | fix | status |
|---|---|---|
| sggarage | Remove noindex URL from articles/sitemap.xml | DONE (car-aircon-not-cold-in-singapore-12-common-causes... removed from articles/sitemap.xml; root sitemap did not list it per probe) |
| sggarage | /llms-full.txt | DONE: created (same facts as llms.txt, Last updated 2026-11-02); llms.txt did not link it |
| sggarage | 404 returns real 404 | Edwin step S1. Cause: unknown non-.html URLs hit the WordPress-style `RewriteRule . /index.php`, and index.php serves index.html with 200 |
| sggarage | HSTS | Edwin step S1 |
| sggarage | One-hop http bare -> https www redirect | Edwin step S1 (currently http bare -> https bare -> https www) |
| sggarage | Shorten 135 titles | NOT DONE: 134 titles >65; 129 end "| Edwin Garage Singapore". Generator not found in the Base44 apps I could search (SgGarage Controller, Bluehost Bridge, Controller: no match), likely server PHP (site-renderer.php / site-data.php, not writable via Bridge) or Make. Suffix cut alone is not enough (titles are 70-100 chars). Needs the generator template |
| sggarage | Compress tesla-lca-1.jpg (359 KB) | SKIPPED: Bridge cannot write binaries. Route: WebP <=150 KB on jsDelivr site-assets branch (site-assets/sggarage/) or cPanel, then swap img src in the Tesla article |
| sggarage | lang en-SG | already en-SG on all 158 sitemap pages (probe) |

## Edwin step S1: .htaccess (cPanel, copy to .htaccess.bak-20261102 first)
1. Replace the "Force canonical www" block with:
```
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{HTTPS} !=on [OR]
  RewriteCond %{HTTP_HOST} !^www\. [NC]
  RewriteRule ^ https://www.sggarage.com%{REQUEST_URI} [R=301,L]
</IfModule>
```
2. Add HSTS:
```
<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000"
</IfModule>
```
3. In "# BEGIN WordPress" change the last rewrite line `RewriteRule . /index.php [L]` to `RewriteRule . - [R=404,L]` (ErrorDocument 404 /404.html is already at the top and 404.html exists).
Test: curl -I https://www.sggarage.com/no-such-page-xyz/ -> 404; curl -I http://sggarage.com/ -> one 301 to https://www.sggarage.com/; https carries strict-transport-security. On a 500, restore the backup.

## S1 safety check (Bridge, live files, 2 Nov 2026) - VERDICT: step 3 is SAFE
- Live .htaccess (sha 98da5fda..., 3541 bytes): the WordPress block only fires when REQUEST_FILENAME is not a file and not a directory. A rule above it already returns a real 404 for any missing `*.html`. DirectoryIndex is `index.html index.htm index.php`.
- Live index.php (741 bytes) is not a router: it returns 410 for one removed article path, otherwise readfile(index.html) (or redirects to /). It looks up no slug, page or article. site-renderer.php / site-data.php (Aug 2026) are only render functions for a rebuild script; index.php does not include them. wp-admin is a 643-byte stub, no WordPress routing exists.
- Sitemap pages: the root sitemap lists / , /car-aircon-repair/, /car-servicing-repair/, /accident-claim-repair/, /prices/, /about/, /articles/ (all real folders on disk) plus article .html URLs. I compared the article URLs with `invoke_list_files articles/`: each has a static file (checked against the listing by eye). No page is served only through index.php. Extra files not in the sitemap: articles/test.html, the noindex aircon stub, index.html.bak-*.
- So the only requests reaching index.php today are unknown non-.html paths, which wrongly get the homepage with 200. `RewriteRule . - [R=404,L]` turns exactly those into 404 (rendered with ErrorDocument /404.html). `/about` without slash is caught by !-d (mod_dir slash redirect); `/` is served by DirectoryIndex. Keep `RewriteRule ^index\.php$ / [R=301,L]` as is.
- NOT verified: executing the rule (container cannot reach the site). After Edwin's change run the curl tests above.

## Title shortening (Bridge, 2 Nov 2026)
- Titles live in static articles/*.html (title, og:title, twitter:title), written by the article publisher, not by site-renderer.php (that only renders home + 3 service pages). Publisher template is not reachable from Bridge (submit-article.php is only a .bak), so new articles still come out with "| Edwin Garage Singapore". Lasting fix (Edwin/publisher owner): suffix "| Edwin Garage", cap titles at 60 chars.
- DONE: 36 articles via invoke_edit_file, suffix "| Edwin Garage Singapore" -> "| Edwin Garage" (backups from 20261102-0903 to 090613). 32 pages also had og:title/twitter:title changed; on 4 only the title tag changed (og differs): third-party-insurance-claim-singapore-workshop, toyota-harrier-suspension-problems-singapore, what-happens-skip-engine-oil-change-singapore, when-to-change-transmission-fluid-singapore. All 36 now <=65 chars: bmw-battery-registration, tyre-puncture-repair-or-replace, car-fuel-smell, car-diagnostic-fee, soft-brake-pedal, car-wiper-streaks, intermittent-car-fault-diagnosis, car-wont-go-into-gear, car-coolant-flush-or-top-up, car-vibrates-at-idle, car-sliding-door-wont-close, wheel-bearing-noise, starter-motor-repair-replacement, car-repair-second-opinion, engine-oil-pressure-warning-light, car-radiator-fan-not-working, car-repair-cost-how-to-know-overcharged, car-wont-start-morning-..., coe-car-maintenance-10-year-guide, edwin-garage-promise-honest-car-workshop, first-visit-edwin-garage-what-to-expect, head-gasket-failure-warning-signs, honda-vezel-aircon-problems, how-long-accident-repair-takes, how-to-find-an-honest-car-workshop-ang-mo-kio, tesla-repair-vs-authorised-service-centre, third-party-insurance-claim, toyota-harrier-suspension-problems, toyota-wish-aircon-not-cold-causes-fixes, toyota-wish-shock-absorber-life, what-happens-skip-engine-oil-change, wheel-alignment-signs-what-checked, when-to-change-transmission-fluid, why-car-aircon-smells-and-how-to-fix-it, why-edwin-garage-is-appointment-only, tyre-sidewall-bulge-safe-driving.
- LEFT: 98 titles still >65 (needs word trimming, 66-136 chars even after the suffix swap). Deliberately skipped: the 1 Nov near-miss pages (car-aircon-blowing-warm-air, car-aircon-compressor-failure..., car-aircon-diagnostic..., hyundai-avante-aircon-not-cold, battery-service-walk-in, car-accident-first-24-hours, car-aircon-pressure-test..., pre-purchase-inspection, car-aircon-servicing-cost, car-aircon-not-cold-...-causes-repair-options, /car-aircon-repair/); judge 15 and 29 Nov.

## Live probe 2 Nov 2026 09:06 UTC (run 41417965035, audit.sh)
158 sitemap pages: lang en-SG on all, h1 = 1 on all, AggregateRating 0. Titles >65: still 134, because the probe was served the OLD HTML minutes after the edits (server files are changed and byte-verified; .htaccess caches text/html for 1 week and there may be a page cache). Re-run the probe later; expect about 98 left. Redirects: http bare -> https bare -> https www (2 hops), unknown URL /no-such-page-xyz-123/ still 301 then page (needs step S1), HSTS still missing.

## Title pass 3 (continuation helper, 2 Nov 2026 ~09:15-09:21 UTC)
- DONE: 94 more article <title> tags shortened via Bridge invoke_edit_file (each edit byte-verified by the tool, backups 20261102-091437 to 092117). All new titles are <=65 chars (most 45-60), main term first, suffix "| Edwin Garage" (brand dropped on 14 where it would not fit or was already redundant). No facts, prices or claims changed (only trailing filler removed; "600+ Reviews (2026)" and "11 Years" kept).
- og:title + twitter:title changed together with the title on 83 pages. On 11 pages only the <title> changed (og/twitter differ by entity escaping of an apostrophe or &): abs-warning-light-on-..., brake-wear-replace-brake-pads, car-absorber-replacement-signs, car-servicing-singapore-complete-guide, first-car-servicing-singapore-new-owner-guide, how-to-choose-...-a-mechanic-s-guide, hybrid-car-battery-warning-signs, minor-vs-major-car-service, timing-belt-replacement-when-to-change, toyota-vios-brake-vibration, tesla-radiator-cleaning. Their og/twitter titles are still the long old text (harmless for the Page One title audit).
- Near-miss pages skipped as ordered (10 articles + /car-aircon-repair/). Not touched: articles/index.html (59 chars already), test.html, the noindex stub.
- Total now: 36 + 94 = 130 article titles shortened; 4 near-miss articles carry over from the list above and stay long until the judge dates (15 and 29 Nov). Expect the audit to show about 5-8 titles >65 (near-miss pages only).
- Titles with a possible duplicate: toyota-wish-aircon-not-cold-singapore ("Toyota Wish Aircon Not Cold Singapore | Edwin Garage") vs toyota-wish-aircon-not-cold-causes-fixes-singapore (shortened earlier); different words but similar. Not changed.
- NOT verified live: re-run the probe (audit.sh) after the .htaccess 1-week HTML cache or a cache purge; the earlier probe was served old HTML.
- Lasting fix still open: the article publisher template (not reachable via Bridge) must use "| Edwin Garage" and cap titles at 60.

# sofacaresg.com - SEO fix pass 2 Nov 2026

Source: Alicia Base44 app 6abfbd745673cb07e77e909c, file base44/shared/sofaStaticRenderer.ts (hourly cron at minute 17 publishes it). No live-file edits (they would be overwritten). Edits auto-committed in Base44; no checkpoint created.

| site | fix | status |
|---|---|---|
| sofacare | html lang en-SG | DONE in renderer baseHtml; live at the next hourly publish, not yet verified live. sofaNotFound.ts and sofaLeadPortal.ts still lang="en" |
| sofacare | Shorten 51 long titles | DONE in renderer: article titles <=60 (brand "| SofaCare SG" -> "| SofaCare" -> brand dropped -> trimmed at word boundary); contact, sofa, mattress, upholstery page titles shortened. Verify with probe audit after next publish |
| sofacare | Compress hero JPG (1.1 MB) and 220 KB PNGs | SKIPPED: needs binary replacement in /media/. Edwin step F1 |
| sofacare | HSTS | Edwin step F2 |

## Edwin steps
F1. cPanel sofacaresg.com/media/: convert the hero JPG and the ~220 KB PNGs to WebP <=150 KB, then point the source (hero_image URL in the SofaCare app content) at the .webp, otherwise the next publish re-mirrors the original.
F2. .htaccess (back up first): in the existing `<IfModule mod_headers.c>` block add `Header always set Strict-Transport-Security "max-age=31536000"`. (http -> https is already a single 301.)
F3. After minute 17 of the next hour run the SEO live probe on sofacaresg.com (expect lang="en-SG", titles <=60).

## Pass 2 (continuation helper, 2 Nov 2026)
- Base44 checkpoint on app 6abfbd745673cb07e77e909c: id 6ae85299eac8479f82add66c (commit 860cb7d9, auto-named "Sanitize Danny AI Links"; includes the renderer edit).
- Probe 09:06 UTC (before the next :17 publish): 59 pages, lang still "en", 54 titles >65 (renderer change not yet published). NOT yet verified: after the next :17 publish, re-run the probe and Bridge-read one article to confirm the short title and lang="en-SG".
- Redirects seen: http://www and https://www both 301 to https://sofacaresg.com/ (non-www is canonical).

## Pass 3: live check after the 09:17 UTC publish (2 Nov 2026 09:21 UTC) - NOT APPLIED LIVE
- Bridge read of sofa-cleaning-tampines.html: still `<html lang="en">` and old 66-char title "Sofa & Mattress Cleaning Tampines | Within 3 Hours | SofaCare SG"; file mtime 2026-10-19 (unchanged). Directory listing: index.html mtime 2026-10-19, no site file changed since 2026-11-01 23:17 UTC.
- Base44 SofaCarePublishRun: the 06:17, 07:17, 08:17 and 09:17 UTC runs all completed (status completed, 59 pages, 48 articles) with changedFiles = 0. So the publisher ran and rendered identical HTML to what is live: the deployed backend function is still using the OLD sofaStaticRenderer. The source file base44/shared/sofaStaticRenderer.ts does contain lang="en-SG" and the app version is 860cb7d9 (checkpoint 6ae85299eac8479f82add66c), but the cron's deployed bundle has not picked it up (Base44 backend functions need a deploy/publish of the app, a checkpoint alone does not redeploy them).
- Not a validation failure: no error in any run. Note the pipeline aborts on duplicate titles (sofaProductionPipeline.ts `titles.has`) and unknown links, so after deploy check the first run's status; if it fails with "Invalid title", two shortened titles collided.
- Did not force-publish (per brief). Edwin step F4: publish/deploy the Alicia app (6abfbd745673cb07e77e909c) from Base44 so functions redeploy, then check SofaCarePublishRun at the next :17 for changedFiles ~59 and re-read index.html + one article via Bridge for lang="en-SG" and short titles.

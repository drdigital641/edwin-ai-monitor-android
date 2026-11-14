# Generated-file override: sitemap.xml, sitemap.txt, llms.txt (DIFF ONLY, NOT SAVED)

Task "SITEMAP OVERRIDE AND INNER OG 1114-2210", Part A. Edwin 10:09pm SGT 14 Nov 2026:
"Yes, allow sitemap.xml, sitemap.txt and llms.txt to update automatically".
Live backups: ~/backups-private/<site>-sitemap-llms-pre-override-20261114-0709.tgz (taken by the requester).

Nothing here is saved in any Base44 app. Base44 functions go live on save (SPO rule), so this waits for the
Security and Privacy Officer review and then Edwin's "save".

## Files
- `generated-override.diff`: against Bluehost Bridge app 6ac6d47b4ec84148578914c7, /app at git caa0c6f
  (apply in /app with `patch -p1` after stripping the `pa0/` / `pa/` prefixes, or by hand; 3 source files + 1 new test).
- `generatedOverride.test.ts`: the new test file (also inside the diff).
- `test-run.txt`: full suite result on the patched copy, 40 passed / 0 failed.
- `MD5SUMS`.

## What changes
1. `base44/shared/liveGuard.ts`: new `publisher?: boolean` argument. Only when it is exactly `true`, the site key is
   `pageone`, and the path is exactly one of
   `sitemap.xml | sitemap.txt | llms.txt` at the Page One root or directly inside
   `preview/star-performance/`, `preview/klar-details/`, `preview/cska-auto/`, `preview/dmts/` (Jacky), `preview/benjamin-poon/`,
   the "replacing this file type needs an override" refusal is replaced by content checks:
   - sitemap.xml: valid UTF-8, well-formed XML (balanced tags, quoted attributes, no raw `&`, no DOCTYPE/DTD,
     one root), root `<urlset>` or `<sitemapindex>`, at least one `<loc>` holding an http(s) URL. Else refused.
   - sitemap.txt: at least one line, every non-empty line an https URL. Else refused.
   - llms.txt: not empty after trimming. Else refused.
2. `base44/shared/bridgeOps.ts` `writeFile`: new opt `publisher?: boolean`, forwarded as `publisher: opts.publisher === true`.
3. `base44/shared/pageoneArticles.ts` `put()` (the hourly publisher's only write helper) passes `{ publisher: true }`.
   No other caller passes it (a test walks every .ts/.js file under base44/ and fails if any other line does).

## What does NOT change
- Every check before it still runs first and unchanged: path rules, delete/move block, never-write list
  (.htaccess, php, etc.), unknown live state refusal, HTML checks for .html, the reviewed GUARD_OVERRIDES path.
- sggarage: no entry, no override; SG Garage HOLD and the SgGarage Controller never-write lock are untouched
  (sggarage writes are in a different app and never reach this code path with site `pageone`).
- Bulk write_files, MCP write_file/edit_file, sync_from_github and restore never pass the flag, so they still need a
  reviewed override for these files.
- Other client folders (ECU Clinic, Wrapstar, Cleanic, ContiExpert...), robots.txt, llms-full.txt, any other .txt/.xml: unchanged.
- A brand-new (absent) file was already allowed before this change and still is; the content checks only apply to replacements.

## For the reviewer: what the publisher will do once saved
- Page One root: on the first :25 run after save, the publisher writes its generated sitemap.xml, sitemap.txt and
  llms.txt (from the Controller article list + templates in pageoneArticles.ts). The last dry-run compare showed the
  LIVE copies of these three are newer than source, so any line added by hand on live and not produced by the
  generator will be replaced. Backups from 22:09 exist (above).
- Client folders: the publisher only writes a client file that is pinned in clientAssets.ts and whose recorded state sha
  differs from the pin sha. Today only Jacky (`preview/dmts/sitemap.xml`, `preview/dmts/llms.txt`) has these files pinned;
  Star, Klar, CSKA and Ben sitemap/llms are not pinned, so for them the override only matters once a pin is added.

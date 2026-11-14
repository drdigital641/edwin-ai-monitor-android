# Bridge auto-sitemap: draft diff for Edwin

Status: DRAFT. Nothing is saved in the Bridge app. Nothing was written to any website. No real IndexNow request was sent.
Base: Bridge commit 5012f3e. Built and tested in a separate copy, never in the app folder.

## What changes

After every publish through the Bridge, the Bridge now does three extra things for that site:

- It adds the new page to `sitemap.xml`, or bumps the `<lastmod>` of a page it already lists.
- It adds the same URL to `sitemap.txt`, and adds a one-line entry to `llms.txt` (only for pages not yet in the file).
- It sends one IndexNow request for the pages that were actually written, and only those.

It runs for `sync_from_github`, `write_files`, `write_file` and `edit_file`. A dry run shows the plan and writes nothing.

## Files in the diff

- New: `base44/shared/autoSitemap.ts` (pure functions: page URL, "is this page indexable", sitemap merge, llms merge).
- New: `base44/shared/autoSitemapRun.ts` (the step that runs after a publish, reads the live files, writes through the guard, sends IndexNow).
- Changed: `base44/shared/liveGuard.ts` (new narrow write rule, see below).
- Changed: `base44/shared/bridgeOps.ts` (one new option, `autoSitemap`, passed to the guard).
- Changed: `base44/shared/bulkWrite.ts` (hook for sync_from_github and write_files, real run and dry run).
- Changed: `base44/functions/bridgeWrite/entry.ts` and `bridgeEdit/entry.ts` (hook for the single-file tools).
- Changed: `autoSitemapRun.ts` also reads the publisher pin list `clientAssets.ts` (see Pinned files).
- New: `base44/tests/autoSitemap.test.ts` (19 tests).
- Not touched: `bridgeConfig.ts`, the Page One hourly publisher, the existing overrides.

## The exact guard rule

Only the auto step (option `autoSitemap`, set nowhere else) may REPLACE these files, and only these:

- `sitemap.xml`, `sitemap.txt`, `llms.txt` in the root of the site being published.
- For Page One, only the client folders already named in the existing override (for example `preview/star-performance/`). Page One's own root is NOT allowed here.
- The live file must already exist. A sitemap is never created from nothing.
- The site's HOLD flag must be OFF. `writeFile` checks HOLD first, so a held site is refused before the guard runs.
- Never-write list and path rules still run first. Sub-folder paths are refused.
- The new content must pass the existing checks, which keep the SPO fix: no `script`, `iframe`, `object`, `embed`, no `on*` attributes, no `javascript:`.
- `sitemap.xml`: every live `<loc>` must still be there. New URLs must be https on a host the live file already uses.
- `sitemap.txt`: every live line must still be there. New lines must be https on a host the live file already uses.
- `llms.txt`: every non-empty live line must still be there, unchanged. New lines may not contain `<`, `>`, control characters or `javascript:`.

## How the merge behaves

- Existing entries are never dropped, reordered or rewritten. `xhtml:link` and image tags stay byte for byte.
- A page already in the sitemap gets only its `<lastmod>` bumped, and never backwards.
- Running the same publish twice changes nothing and sends nothing the second time.
- Titles and descriptions for `llms.txt` are cleaned (no `<`, `>`, `[`, `]`, control characters, `javascript:`).
- Not indexed: review helper pages (any `*review*.html`), `404.html`, pages with noindex, meta-refresh redirect stubs, Search Console verification files, fragments, anything under `preview/` of Page One that is not a client folder.

## Pinned files (update 15 Nov)

The hourly publisher rewrites a pinned file when its live sha differs from the pin, at the next :25 run. So the auto step does NOT write a pinned file.

- Before each write, the exact path is checked against `CLIENT_PINNED_ASSETS` in `clientAssets.ts`.
- A pinned file is skipped and reported as `{file, skipped: 'pinned: re-pin to new sha needed', newSha}`. Dry run reports the same.
- Other files in the same run are still written, and IndexNow is still sent for the pages written (the pages are live).
- Current sites with pinned sitemap.xml AND llms.txt: Jacky Gearbox (`preview/dmts/`), CSKA Auto (`preview/cska-auto/`), ECU Clinic (`preview/ecu-clinic/`), Wrapstar (`preview/wrapstar/`). No pinned `sitemap.txt` anywhere.
- Of these, only Jacky Gearbox and CSKA are covered by the auto step today. ECU Clinic and Wrapstar are not in the Bridge hold list, so they are not touched at all.
- The pins in `pageoneArticles.ts` (PINNED_ASSETS, robots.txt, llms-full.txt and Page One's root pages) are for Page One's own root, which this step never writes. Star Performance, Klar Details, Benjamin Poon, SG Garage and all other Bridge sites have no pinned sitemap or llms files.
- To get a pinned file updated: commit the new file to git and re-pin it (new URL and the `newSha` shown in the result).

## IndexNow

- Key: a root file named `<32 hex>.txt` whose content equals its name. No key file means IndexNow is skipped, with the reason shown.
- Sent: one POST to `api.indexnow.org/indexnow` with host, key, keyLocation and the URL list (max 1000), only for pages written in this publish on the site host.
- Never sent: review pages, noindex pages, the Page One preview host.

## Safety switches

- `AUTO_SITEMAP_ENABLED = true` in `autoSitemap.ts` is the kill switch. Set it to false and the whole step does nothing.
- `AUTO_SITEMAP_EXCLUDE = ['pageone']` skips Page One's own root. Its hourly publisher keeps rebuilding those files.
- A failure in the auto step never fails or undoes the page writes. It is reported in the tool result under `autoSitemap` (status, added, bumped, files, indexnow).

## Choices to check

- Page One client folders (Star Performance, Klar Details, CSKA, Jacky Gearbox, Benjamin Poon) ARE covered, each as its own site with its own domain. If the hourly publisher already rebuilds those sitemaps, add them to `AUTO_SITEMAP_EXCLUDE`, for example `pageone:preview/star-performance/`.
- IndexNow is sent for every indexable page actually written (new or edited), not only when the sitemap changed. A same-day second edit still notifies Bing.
- `sitemap.txt` keeps its live lines and only appends missing URLs, instead of being rebuilt from the XML. This keeps any extra live lines.
- If `llms.txt` has no Articles or Pages heading, a new `## Recent pages` section is added at the end.
- The site host comes from the live sitemap (www or not), so IndexNow uses the same host the sitemap uses.

## What is NOT covered

- Pages written by other routes (the hourly Page One publisher, restore_backup). restore_backup does not trigger it.
- Deletes: removed pages stay in the sitemap, because the rule is "never drop".
- Sitemap index files (`<sitemapindex>`): reported and skipped, not merged.
- Sites with no sitemap.xml, or whose root is a sub-folder not handled by the Bridge: skipped with a reason.
- Base44's article writer and the Wrapstar carousel are separate items.
- A UTF-8 BOM at the start of a live file is not kept when the file is rewritten (harmless to crawlers).

## Risks

- Every publish now adds a few cPanel reads (sitemap.xml, sitemap.txt, llms.txt, the folder listing) and up to three writes. Each write is backed up and read back by the normal write path.
- A big sync (up to 150 files) adds about 8 more cPanel calls, not 150, because only the sitemap files are touched.
- If two publishes run at the same moment, the second sitemap write is refused (the file changed) and is reported. The next publish fixes it.
- The change goes live the moment it is saved in the Bridge app. Review the diff, then say "save" before anything is saved.

## Test results

- Baseline at 5012f3e: 50 passed, 0 failed in `tests/` (60 passed, 0 failed with `base44/tests/siteFeed.test.ts`).
- With the change: 79 passed, 0 failed (60 existing + 19 new). Command: `deno test --no-check -A --import-map tests/importmap.json tests/ base44/tests/`.
- New tests cover: pure functions (XSS titles, javascript: locs refused, never-drop, idempotence), the guard flag (allowed for unlocked sites, refused with HOLD ON, sub-folders, dropped locs, script/on*/javascript:), and the hook with a fake cPanel and fake fetch (pinned sitemap skipped and unpinned written, 3 files plus one IndexNow POST with only the changed URLs, dry run writes nothing, an auto failure does not fail the batch).
- HOLD ON is tested by switching the sggarage flag on inside the test and back off. `bridgeConfig.ts` is not edited.
- Type check passes for the new and changed files. `deno check` of `pageoneArticles.ts` fails here only because `npm:marked` is not installed in the test copy (same as baseline).

## Files here

- `bridge-auto-sitemap.diff` (diff -ruN against 5012f3e, deno.lock excluded)
- `test-baseline.txt` (full deno output at 5012f3e)
- `test-auto-sitemap.txt` (full deno output with the change)

## Rebased onto ddd665c (15 Nov 2026, after the "move 3 sites" Bridge save)
- The 5012f3e diff applies cleanly onto Bridge git ddd665c (line offsets only, no conflicts). The changed lines are identical.
- Rebased tree: Base44 sandbox /tmp/qul5nf-rb. Rebased diff: sandbox /tmp/qul5nf-rebased-ddd665c.diff (1017 lines, md5 c65eb50669efe9c841685554d15a7141).
- Full suite on the rebased tree: 86 passed, 0 failed (67 at ddd665c plus 19 new).
- K Tech, Benz World and Li Lian are covered automatically (they are in SITES / SITE_HOLDS with HOLD off).
- One thing for SPO: the move thread's own override for those 3 sites (MOVED_GENERATED_SITES) already lets any Bridge tool write replace their sitemap/llms files with only the generatedFileProblem check, and it runs before the auto-sitemap rule. So for those 3 sites the extra "never drop a live URL/line" rule is not enforced by the guard (the merge code itself still never drops anything). Easy fix if wanted: add the never-drop check to that override too.

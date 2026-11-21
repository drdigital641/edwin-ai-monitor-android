# Bridge change "article-autoindex" (21 Nov 2026) - REVIEW BEFORE SAVE

Thread: "Automate article sitemap and indexing". Built on Bluehost Bridge git a5af44b. NOT saved to Base44: per the
16 Nov review-before-save rule this waits for SPO review, then save + Edwin Publishes (Publish only, never Activate).

## Why
1. HX Auto (hxautoservice.com.my, roster row 43, on the API runner from 21 Nov) lives in autoseo.my `preview/hx-auto/`.
   The Bridge auto-sitemap step maps every autoseo write to autoseo.my's ROOT sitemap and drops `preview/` pages, so an
   HX article today gets NO sitemap.xml entry, NO llms.txt line and NO IndexNow. `bridgeRunnerIndexNow` also refuses
   hxautoservice.com.my URLs (403, not a domain of site autoseo).
2. Edwin 21 Nov: IndexNow must carry the new article URL AND the sitemap URL. The Bridge sent page URLs only.
3. IndexNow 429 came back as a plain `error`; the runner had to guess. Now it carries `retry_later: true` and the URL list.

## What changes (3 files + tests)
- `shared/liveGuard.ts`: new `AUTO_SITEMAP_SITE_FOLDERS` = `{ autoseo: { 'hx-auto': 'hxautoservice.com.my' } }`.
  `autoSitemapPathOk()` lets the auto step replace exactly `preview/hx-auto/sitemap.xml` and `preview/hx-auto/llms.txt` on
  site autoseo (same checks as the Page One client folders: file must exist, every live URL/line kept, new URLs https on
  a host the live file uses). Unlisted folders (Carku, 911 Garage, Rasa Sayang...) stay hidden previews.
- `shared/autoSitemapRun.ts`: `subsiteFor()` maps autoseo `preview/hx-auto/...` to that folder + domain. IndexNow list
  gets `https://<host>/sitemap.xml` appended whenever sitemap.xml was written (and in the dry-run plan). 429 result adds
  `retry_later: true, urlList`. Status stays `error` for 429 so existing callers behave as before.
- `shared/runner.ts`: `indexNowGroups()` adds the site's folder domains, so `bridgeRunnerIndexNow` accepts
  hxautoservice.com.my URLs (key file found in `preview/hx-auto/`).
- `tests/autoSitemap.test.ts`: 4 new tests (HX mapping and guard paths, HX hook end to end with page + sitemap ping,
  hidden autoseo preview never listed or pinged, 429 retry_later); 6 existing assertions now expect the sitemap URL.

## Tests
`deno test --no-check -A --import-map tests/importmap.json tests/ base44/tests/`: 152 passed / 0 failed
(baseline a5af44b: 148 / 0). `apply_bridge_patch.py` applied to a clean a5af44b copy gives byte-identical files.

## Live checks done (read-only)
- hxautoservice.com.my/sitemap.xml 200 urlset 42 URLs; key file + llms.txt present in autoseo `preview/hx-auto/`.
- Bridge write_files dry run on sgcarworkshop (Hon Win test page, nothing written): autoSitemap would add the URL,
  sitemap.xml + llms.txt "would update", IndexNow "would send" (page only = the gap fixed here).

## After Publish
- Set `hx-auto` to `active` in night-writers/templates/article-autoindex/sites.json.
- Every future AutoSEO go-live served from an autoseo.my folder: add one line to `AUTO_SITEMAP_SITE_FOLDERS`
  (autoseo-template/golive README step 7).

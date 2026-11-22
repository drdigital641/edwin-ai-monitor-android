# Dynamic sitemap template (Edwin, 23 Nov 2026 SGT, every live client site)

`sitemap_dynamic.py` rebuilds a live site's `sitemap.xml` from the pages that are really public on the Bluehost server,
with an accurate `lastmod` per URL, and hands changed URLs to the existing IndexNow daily batch. It builds on
`../article-autoindex/` (same `sites.json` rows, same Bridge runner client, same `state/indexnow-queue.json` + 429 backoff).

Why (gaps found 22-23 Nov 2026): Danny ILP article live but not in the sitemap, Danny `/areas/` and one insight listed
with a trailing slash that 301s, 10 Danny core pages without lastmod, SofaCare dog-urine article dropped when the
22 Nov area-page upload rewrote the sitemap, Page One managed-website article never added (the Bridge auto-sitemap
skips Page One's root by design and the article template was not wired into the runner yet).

## What a run does (per active site row)
1. `bridgeListLive` the site folder (recursive), collect `.html` pages, skip assets/admin/login/preview/404/verification files.
2. Read only new or changed pages (mtime), at most 150 per run (`SITEMAP_MAX_READS`), cached in `state/sitemap-cache-<site>.json`.
3. Keep a page only if indexable: no `robots noindex`, not a redirect stub, canonical on the site's own host. `<loc>` = canonical.
4. `lastmod` = SGT day the page's visible content last changed (body hash, scripts and `?v=` ignored). First sight:
   JSON-LD `dateModified`/`datePublished`, else the current sitemap's lastmod, else file mtime.
5. Rule 6: `/ms/` and `/zh/` pages get `xhtml:link` hreflang (en, ms, zh, x-default) only when the counterpart page exists.
6. Never drops a live indexable URL. More than max(5, 10%) drops = nothing written, status `drop_guard`.
7. Keeps `<image:image>` blocks, writes `sitemap.xml` only (never sitemap.txt), only when changed, with `expected_sha256`.
8. IndexNow: added + lastmod-moved URLs + the sitemap URL are queued for the daily batch (`resend_queue`); `--ping-now`
   sends at once and queues on 429.

## Keys and secrets
The Bridge submits IndexNow with the key file the host already publishes at its root (`bridgeRunnerIndexNow`, own
domain only, key never returned). The template never reads, prints, stores or hard-codes a key; nothing goes into
front-end JS. Runner auth = `BRIDGE_RUNNER_KEY` from the environment.

## Wiring (Grok Bot / Website Manager, one-time, no Bridge or Controller change needed)
```
python3 sitemap_dynamic.py --all             # nightly, after the midnight article run (queues IndexNow)
python3 ../article-autoindex/article_autoindex.py --resend-indexnow   # the existing daily batch sends the queue
python3 sitemap_dynamic.py --site danny --dry-run                     # check one site, writes nothing
```
First run per site reads every page over a few nights (150 reads/run cap, Bluehost load cut 22 Nov).
Run it after any bulk upload (area pages, rebuilds) so a rewrite that loses URLs is repaired the same night.

## Known limits
- Rows with status other than `active` are skipped (hx-auto, overseas-tyre, sp-precision-parts, rasa-sayang, cchauto wait
  on Bridge cp 6b01e564 Publish; autotex NXDOMAIN). Set them active after Publish.
- Pinned client sitemaps (Jacky, CSKA, ECU Clinic, Wrapstar: clientAssets CLIENT_PINNED_ASSETS) are reverted by the :25
  publisher; the run reports the write but the pin wins until the repo copy is updated.
- sgcarworkshop.sg: its build.py already writes the sitemap from the same rule (noindex thin pages excluded); the template
  agrees with it. Never run a full sgcarworkshop rebuild+publish over Website Manager's hub edits.
- Page One root: add `SITE_EXTRA_EXCLUDE['pageone']` for any new private top-level folder.

Tests: `python3 test_sitemap_dynamic.py` (12 tests, fake Bridge, no network).

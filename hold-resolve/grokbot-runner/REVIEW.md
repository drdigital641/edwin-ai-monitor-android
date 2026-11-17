# Grokbot runner key + generateArticleImage: diffs for review BEFORE the Base44 save (Security & Privacy Officer)

Brief (Website Manager for Edwin, 18 Nov 2026): move routine jobs to an API runner on the Grok Bot box; every Bluehost
read and write still goes through the Bluehost Bridge; Base44 still makes every image.

**Status: NOT saved.** Built and tested in sandbox copies only (Bridge `/tmp/runner` on Bridge git 3592dca, Controller
`/tmp/ctl` on Controller git 12ca0c2). Base44 backend code goes live on save, so nothing is saved until this review passes.

| App | Diff | Tests on the patched copy |
|---|---|---|
| Bluehost Bridge 6ac6d47b4ec84148578914c7 | `bridge-runner.diff` | new tests/runnerKey.test.ts 8/8; tests/ 95/0, base44/tests 37/0; eslint clean; vite build OK |
| Page One Controller 6ac7f2548a9c3877449e2772 | `controller-runner.diff` | new base44/tests/runnerFeed.test.ts 4/4; all 134/0; eslint clean |

`src/` holds the exact new files and `apply.py` / `controller/apply_controller.py` (each edit must match exactly once),
so the save can be re-applied on top of whatever the apps' HEAD is at save time.

## What the Bridge change does
- **New key scope `runner`** (keys.ts). Made only by a signed-in admin on the Connect page (new button "Generate Grok Bot
  runner key"); shown once, only its SHA-256 is stored; revocable on the same page. Label `grokbot-runner`.
- **Allowed actions** (handler.ts + runner.ts `RUNNER_KEY_ACTIONS`): `list`, `read` (live files), `write`, `write_many`,
  `runner_sitemap`, `runner_indexnow`, `runner_controller`, `runner_image`. Everything else answers 403. Session-only tools
  (htaccess, hero_image, image_gate, drop_publish) are refused before the scope check, as today.
- **Named sites only** (`RUNNER_SITES`, 17 keys). A site added to SITES later does not join the runner until named.
- **Writes** go through the unchanged `writeFile`: replacing a live file needs the base `expected_sha256` (missing or stale =
  409), verified backup before every replace, live guard, BRIDGE HOLD, image gate, CTA gate, secret-content check, and the
  frozen-site rule (Cleanic and pageone `preview/contiexpert/`: articles only). No delete path exists for the key.
- **`bridgeRunnerSitemap`**: reruns the existing auto-sitemap step (merge-only sitemap.xml + llms.txt, then IndexNow) for 1-20
  `.html` pages already on the site.
- **`bridgeRunnerIndexNow`**: URLs must be plain https on the site's own domain (pageone: its client-folder domains). The
  key file is found on the server; the key is never returned or logged (test asserts both).
- **`bridgeRunnerController`**: relays `copy_fix` / `taps` (read only) and `article_last` to the Controller's new
  `runnerFeed`, signed with the Bridge's existing pinned P-256 key (same as articleFeed). Inputs validated on both sides.
- **`generateArticleImage`**: Base44 GenerateImage -> three NEW files in the site's article image folder:
  `<slug>.webp` 1536x1024, `<slug>-card.webp` 768x512, `<slug>-og.jpg` 1200x630. Never replaces a file; same site+folder+slug
  returns the saved result. Shares hero_image's daily caps (3 per site, 40 total per SGT day). Prompt ban list and an
  "Illustrative" alt rule as in hero_image. Uses `npm:imagescript@1.3.0` (MIT, pure JS/wasm) for the resize; if it cannot
  load, the original file is used for all three URLs (warning returned).
- **Logging**: every runner call (allowed or refused) writes a BridgeLog row with `label: grokbot-runner`, actor
  `grokbot-runner (runner key)` and a `detail` of counts only (op, slug, number of paths/urls/files). BridgeLog gets a new
  `label` field; enums widened (Base44 does not enforce them today).

## What the Controller change does
- **New `runnerFeed`**: accepts only a Bridge-signed payload with purpose `grokbot_runner` (or a signed-in admin / CRON_KEY).
  - `copy_fix`: urgent/warn dashboard rows with the exact "Copy fix" instruction text, check list and FixRequest status.
  - `taps`: CTA counts per site (unique and raw, today/7 days, per-day WhatsApp) and enquiry counts. No visitor ids, client
    WhatsApp numbers, message texts, plans or contacts (test asserts).
  - `article_last`: writes only `article_last_built`, `article_last_title`, `article_last_url` on one non-partner Client found
    by slug; URL must be https on that client's domain or a preview host (pageonesingapore.com, autoseo.my).
- **`portfolio`**: one new cron-only action `runner_status` = the same read-only status branch (4 one-line edits), so
  runnerFeed can trim it. Admin behaviour unchanged.

## Points for the reviewer
1. Breadth: the runner key can write any file type writeFile allows (HTML, CSS, JS, images) on 17 sites. The jobs in the
   brief (Copy fix sweep, carousel, area pages) need more than articles/. If the key leaked, the damage is the same as a
   site key on every named site (no deletes, no .htaccess, base hash + backup on every replace, all logged). Revoke on Connect.
2. Signed Controller payloads are valid for 20 minutes (no nonce, as articleFeed). A replayed `article_last` only re-sets the
   same three values.
3. Image spend is capped by the shared daily counters; a key can not raise them.
4. `bridgeSelfTest` (pre-existing, unchanged) is a public read-only health check with no key; noted, not part of this change.
5. write_many writes one call-level row with the label plus the existing per-file rows (actor = runner, no label).

## After the save
Edwin Publishes the Bridge checkpoint (frontend button + MCP) and the Controller checkpoint (Publish only, never Activate).
Backend functions are live on save; the Connect button appears after the Bridge Publish.

## Saved 18 Nov 2026 ~7:10am SGT (Edwin OK 6:53am SGT)
- Bridge checkpoint 6afcdddaeed39d3e0091a0c8 (git 36ce09c), Controller checkpoint 6afcdddb3aaf67e56cbc4403 (git 72e15c6). Both need Publish.
- Change after review (deploy blocker): the npm imagescript build ships native .node files the function bundler cannot pack,
  so runnerImage.ts imports the Deno build (https://deno.land/x/imagescript@1.3.0/mod.ts). It has no WebP encoder, so all
  three files are JPEG (<slug>.jpg, <slug>-card.jpg, <slug>-og.jpg). Tests 132/0 after the change.
- Every Bridge entry file got a one-line comment so all functions redeploy with the runner-aware handler.
- IMPORTANT: until the Bridge checkpoint is Published, the published bundles of the existing functions still read scope
  'runner' as 'full' (old scopeOf). Do NOT create the runner key before the Publish. Claude's test key is switched off.

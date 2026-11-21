# SPO review: runner article records (22 Nov 2026)

Reviewer: Security & Privacy Officer. Scope: three unsaved backend changes. Read-only review; nothing was saved or deployed.

## Verdicts

| Change | Verdict |
|---|---|
| 1. Bridge (imageGate, bridgeRunnerArticle, runner key action) | PASS with fixes |
| 2. SofaCare runnerArticleIngest + runnerArticleChecks | PASS with fixes (one must-fix) |
| 3. Controller runnerFeed article_last | PASS |

## Auth, replay, SSRF, secrets (all three)

- Unsigned callers cannot create records or reach files. `runnerArticleIngest/entry.ts` calls `verify()` before anything else:
  pinned kid, ECDSA P-256 verify over the exact payload string, `sent_at` within 20 minutes, then `purpose === 'runner_article'` and
  `site === 'sofacare'`. Service role is used only after that. Failure is a generic 401. Only the public JWK is in code (fine in a public repo).
- Replay: no nonce, 20 minute window both directions. A replayed request is harmless while the record exists (same slug and title returns
  `created:false`) and dry_run is read-only. Residual: if an article is deleted inside the window, a captured request could recreate it. Low.
- Signing oracle: `signedAppCall` (crawlerLogs.ts) is exported and signs any payload with the key the Controller also trusts. The only caller
  fixes `purpose`, and each receiver checks purpose, so no cross-app replay today. See nice-to-have N1.
- SSRF: none. `signedAppCall` takes only a 24-hex app id and an identifier-only function name and posts to the fixed host `base44.app`.
  Nothing is fetched from a caller URL. `hero_image` URLs are only stored, never fetched, by this path.
- Path traversal: `hero_path` must match `^images/articles/<slug>.(jpg|jpeg|png|webp)$` where slug is already `^[a-z0-9]+(-[a-z0-9]+)*$`, so no `..`,
  no slashes, no other folders. `readLiveFile` also applies the Bridge's existing blocked-path and secret-content checks. The site is a whitelist
  (`ARTICLE_RECORD_SITES`).
- Secrets: none in code, logs or the OpenAPI doc (only the env var name BRIDGE_RUNNER_KEY, as before). `handler.ts` logs slug, op and counts only, never
  content or `hero_b64`.
- Runner key gain: only `runner_article`, which can (a) create SofaCare Article records that go LIVE at the next :17 publish with no human gate, and
  (b) read `images/articles/<slug>.*` of the sofacare Bridge site. It cannot reach any other app, entity, site, or file. This is new "publish live"
  power, bounded by the checks (see F2, N2).

## Change 1: Bridge

Image gate. `heroImg` now: fetchpriority=high image outside header/nav/footer/aside, then "hero" class, then old rule after cutting related cards.
Empty result still fails closed (`checkUrl` reports "hero image is missing"). The reused-photo check against the hub, the og:image and twitter:image
stem checks and the third-party host block are unchanged, so a reused or foreign image still fails for NEW article pages.

Must-fix: none blocking security. One availability regression to fix before relying on it (F3).

## Change 2: SofaCare

Must-fix list:
- F1. `functions/runnerArticleIngest/entry.ts` line 61: after `UploadFile`, the returned URL is only checked for the prefix
  `https://media.base44.com/`. `runnerArticleChecks.ts` line 26 requires the stricter `.../images/public/<24hex>/<file>.(png|jpe?g|webp)` for supplied URLs
  but SKIPS it when a hero was uploaded (`heroUploaded`). If the upload URL has another shape the stored hero could be one the hourly publisher
  or the image gate rejects. Apply the same strict regex to the uploaded URL before `Article.create` (line 63), and return 502 without creating.
- F2. Raw HTML is not checked. `checkArticle` validates markdown links only (line 57) and `wa.me`; `content`, `title`, `hero_image_alt`, `faqs` may carry
  `<script>`, `<iframe>`, `<a href="javascript:...">`, or inline `<a>`/`<img>` that bypass the 3-5 internal links and external-link rules, and the page goes live
  unattended. Unless the publisher is confirmed to escape all of these, fail on `/<\s*[a-z!\/]/i` and `javascript:|data:` in all text fields
  (the Controller clip already strips `<>`; the Bridge clip does not).

Should-fix:
- F4. `entry.ts` line 39: duplicates are detected via `Article.list('-published_date', 500)`. Once there are more than 500 articles, older slugs/titles
  are invisible, so the slug/title uniqueness and "live slug" link checks silently weaken. Use `filter({slug})` for the slug check and a title filter, or page through.
  Concurrent calls can also both pass the check (no lock); the runner is serial, so low.
- F5. No daily cap. The runner key can create many valid articles per night. Add a cap (for example 3 created per SGT day) in the ingest function.

## Change 1 fix list (Bridge)

- F3. `shared/imageGate.ts` `stripChrome`: it deletes everything inside any `<header>...</header>`. Templates that wrap the article's own H1 and hero in
  `<header class="article-header">` lose their hero, rule 1 and 2 find nothing and the gate answers "hero image is missing" (a false block, same symptom as
  21 Nov). Add a fallback: if the stripped body yields no hero, retry the old rule on `cutRelated(html)` without stripping header. Fails closed today, so
  not a security hole.

## Nice-to-have

- N1. Add an audience field (`aud: <target app id>`) to the signed payload and check it in the ingest function; stop exporting a generic signer, or whitelist purposes in `signedAppCall`.
- N2. In `checkArticle`, require the hero to be unique: reject if `hero_image` equals any other Article's hero_image, and pin the URL path to `SOFA_APP_ID`
  (exported but unused). This closes reused/foreign media for SofaCare itself.
- N3. `entry.ts` line 33: `req.json()` parses the whole body before the 3.5 MB check. Check `content-length` first. Unsigned callers can burn CPU only.
- N4. `imageGate.ts` rule 2 (hero class) runs before `cutRelated`, so a related card inside a container whose class contains "hero" could still be read
  as the hero. Apply `cutRelated` to rule 2 as well. Rule 1 trusts the `fetchpriority` marker, so a page with a decoy marked image would pass; acceptable
  because the gate targets accidents, not an adversarial author, and og:image/twitter:image still must match the slug.
- N5. Orphan upload if `Article.create` fails after `UploadFile` (entry.ts lines 59-63); harmless, log it.
- N6. Controller: `article_last` for built-in slugs returns `ok:true, stored:false`, which can mask a runner that thinks it recorded a date. The `builtin:true` flag
  is returned, so the runner should log it. Also confirm no Client row exists with slug cleanic/sofacare/pageone, since the built-in branch now shadows it.

## Change 3: Controller (PASS)

`BUILTIN_SITES` branch is a no-op with no writes, requires an https URL on the exact expected host (no user, password or port), and sits behind the
existing auth path, so it grants nothing. `SLUG_ALIASES` only renames lilian to lilian-properties before the existing slug regex. No fix needed.

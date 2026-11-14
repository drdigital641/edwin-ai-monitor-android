# SG Garage OPTION C (DRAFT DIFFS, NOT SAVED)

This is task "SG GARAGE OPTION C 1114-2335". Edwin's words, relayed at 11:30pm SGT on 14 Nov 2026: "Unlock SG Garage, allow sitemap and article cards to update, and close the side door so everything goes through the Bridge".

The unlock save 3e01a2c81 (flags OFF) still stands:
- Bluehost Bridge: git 33343ea, checkpoint 6af880138a6c7cf41e0e2566.
- SgGarage Controller: git ac87bd6, checkpoint 6af8803f403adb49f721da4b.

The guard-off and never-write-removal diffs (`../sggarage-unlock/v2/` and `../sggarage-unlock/separate-after-save/`) are **DROPPED**. The live guard and the never-write lock stay.

Nothing in this folder is saved, synced or published. Base44 functions go live on save, so each diff waits for SPO's review and Edwin's "save". Both diffs were built and tested in /tmp copies of each app's /app. Neither /app was changed.

## 1. Bluehost Bridge: narrow sggarage override

**Diff:** `bridge-sggarage-override.diff`, on top of the saved git 33343ea.

**Pattern:** the same as Page One's f4a3b8e4a.

**Where it applies:**
- Site key `sggarage` only (docroot public_html/carbonfibre, Bridge prefix '').
- The exact root paths `sitemap.xml`, `sitemap.txt`, `llms.txt` and `article-cards.json`. Nothing in a sub-folder matches, and no other name matches.
- Only writes that carry the publisher flag (`SGG_OVERRIDE_WRITERS = ['publisher']`).
- The other checks still run first, and still refuse:
  - the path rules;
  - the never-write list, unchanged for all sites;
  - an unknown live state.

**Content checks:**
- **sitemap.xml:** must pass the existing `generatedFileProblem` / `xmlProblem`, including the d1f0dbf3d hardening:
  - well-formed XML;
  - a `<urlset>` or `<sitemapindex>` root;
  - at least one `<loc>`;
  - no script, iframe, object or embed element in any namespace;
  - no `on*` attribute;
  - no `javascript:` (also when hidden with references or whitespace);
  - `xhtml:link` alternates are allowed.
- **sitemap.txt:** at least one line, and every line an https URL.
- **llms.txt:** not empty.
- **article-cards.json:** new strict shape check, `articleCardsProblem`:
  - a JSON array of 1 to 5000 cards;
  - each card is a plain object with exactly `href`, `cat` and `title`, all strings;
  - `href` matches `/articles/<lower-case-slug>.html` and is unique;
  - `title` is 1–300 characters and `cat` is 1–60, with no `<`, `>` or control characters;
  - no `javascript:` anywhere, in the raw text or after JSON unescaping;
  - **when the live file is a readable card list, every live href must still be there.** Cards may be added or edited, never dropped. SPO: say if you want this rule removed.

**Unchanged:**
- The Page One override (`GENERATED_OVERRIDE_SITES = ['pageone']`, same paths).
- All 7 flags.
- `bridgeConfig.ts` (not touched).
- Every other site's guard.

**Tests:** `tests/sggGeneratedOverride.test.ts` (new) and `tests/generatedOverride.test.ts` (the sggarage case updated).
- Override: **50 passed, 0 failed** (`test-bridge-override.txt`).
- Saved 33343ea unchanged: 45 passed, 0 failed.

### IMPORTANT: as specified, this override does nothing yet
- **The hourly publisher never writes sggarage.com.** In `pageoneArticles.ts`, SITE_KEY is 'pageone', and the publisher flag is set only by its put().
- **The SG Garage night run uses Bridge tool calls** (runbook /mnt/project-files/sggarage/DAILY-ARTICLE.md, step 5: `invoke_edit_file` on sitemap.xml and llms.txt). Those calls carry no publisher flag.
- **So with `['publisher']` the sggarage files are still refused** when the night run updates them.

### Optional delta for that: `bridge-sggarage-override-tools-delta.diff`
- **Applies on top of** `bridge-sggarage-override.diff`.
- **The change:** one line, `SGG_OVERRIDE_WRITERS = ['publisher', 'tools']`, plus test updates.
- **Effect:** Bridge tool writes (edit_file, write_file, write_files, sync_from_github) may also replace the same four sggarage files, with the same content checks.
- **Unchanged by the delta:** Page One stays publisher-only. Everything else is the same.
- **Tests:** 50 passed, 0 failed (`test-bridge-override-plus-tools-delta.txt`).
- **When it works:** the MCP tools run the PUBLISHED Bridge code, so this delta only takes effect for tool calls after it is saved **and** Published.

## 2. SgGarage Controller: side door closed

**Diff:** `sggarage-controller-side-door.diff`, on top of the saved git ac87bd6.

**Option chosen: the fallback (refuse and check), not routing via the Bridge. Why:**
- **Routing would add a stored credential.** The Controller would need a Bridge write credential stored as a new secret, plus a cross-app call that the Bridge accepts. That is a new credential and a new trust path, which needs Edwin to create the secret and Publish the Bridge.
- **Routing would change how the Controller behaves.** Its callers (ftpWriteFile, the website command worker, the health check) expect FTP semantics: sha-checked overwrite, backup and rollback.
- **The fallback is self-contained.** It reuses the Bridge's own check code, byte for byte, and adds no secret.

**Scope:** permanent, like the never-write lock. It applies whatever the HOLD flag says. It covers only the SG Garage docroot, found exactly as the HOLD finds it:
- a `carbonfibre` path segment, or
- a folder whose FTP listing has an SG Garage marker file.

If that check cannot run, the change is refused (fail closed).

**What it refuses inside SG Garage:**
1. **Deletes, renames, folder removal and SITE commands:**
   - delete: `remove`, DELE;
   - rename: `rename`, RNFR, RNTO;
   - folder removal: `removeDir`, `removeEmptyDir`, `clearWorkingDir`, RMD, XRMD;
   - every SITE command (SITE CHMOD and the rest), MFMT, MFCT, and any FTP method or verb it does not know.
2. **An HTML overwrite** that would change or lose:
   - a title, meta description, H1 or JSON-LD value;
   - a FAQ question;
   - the "Leave us a Google review" footer;
   - or is older than live.

   This is the Bridge's own `htmlProblems()`, in `base44/shared/liveGuard.ts`, copied byte for byte from the saved Bridge 33343ea (MD5 b41399f37b38dae6d5f044d30d0df453, also in this folder). The check runs before the backup and before any byte is sent.
3. **An HTML upload or append that does not come from `safeWriteRemoteText`,** so check 2 cannot be skipped. That covers raw `uploadFrom`, STOR, `appendFrom` and APPE on `.html`/`.htm`.

**What it still allows:**
- **The health probe:** removal of `/_cleanic_control/validation/chatgpt-health-<id>.txt`.
- **Rollback:** `safeWriteRemoteText` may remove a NEW file it just created when its own write fails verification.
- **Normal writes:** new files, HTML body edits that keep the protected parts, non-HTML overwrites (sitemap.xml, article-cards.json, robots.txt, CSS, JS, images) and mkdir.
- **Everything outside SG Garage:** unchanged. The test checks that a Cleanic path can still be deleted, renamed and SITE CHMODed.

**Refusal response:**
- 403 with `side_door: true`.
- A ConnectionAudit row `side-door-refused`.
- Never retried.
- The never-write check and the HOLD still run first.

**Tests:** new `tests/sggSideDoor.test.ts` (43 refusals, server bytes unchanged). These existing tests were adjusted where they relied on rename, SITE CHMOD or a raw HTML upload inside SG Garage: `tests/neverWrite.test.ts`, `tests/sggHold.test.ts`, `tests/sggUnlocked.test.ts`. `tests/fakeFtp.ts` gains `removeEmptyDir`.

| Run | Result | Log |
|---|---|---|
| Flag OFF (as saved) | **18 passed, 0 failed** | `test-controller-side-door-flag-off.txt` |
| Flag set ON (test copy only) | **18 passed, 0 failed** | `test-controller-side-door-flag-on.txt` |
| Saved ac87bd6 unchanged | 14 passed, 0 failed | `test-controller-ac87bd6-unchanged.txt` |

**Not covered by this diff (SPO: say if you want it):**
- **Non-HTML overwrites through the Controller** (robots.txt, sitemap.xml, article-cards.json) are not content-checked. The ask covered HTML only.
- **The Controller's own ensureDir/mkdir** is still allowed.

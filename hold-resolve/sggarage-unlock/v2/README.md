# SG Garage unlock v2 (DIFF ONLY, NOT SAVED)

Task "SG GARAGE UNLOCK DIFF UPDATE 1114-2325". This **replaces** the v1 diffs in the folder above (commit 3e01a2c81).
Edwin's words, relayed: 10:42pm "go through Claude and remove the lock"; 11:07pm "Unlock sggarage as well", "Unlock everyone";
11:11pm "We'll do all the checking and upload the latest, never-overwritten website to the server. Then you unlock everything."

Nothing here has been saved, synced or published. Base44 functions go live on save, so this waits for SPO's review and Edwin's "save".
Both diffs were built and tested in /tmp copies of each app's /app. Neither app's /app was changed.

## Bluehost Bridge 6ac6d47b4ec84148578914c7: `bridge-unlock-v2.diff` (on top of saved git e1d39cf)

| File | Change |
|---|---|
| `base44/shared/bridgeConfig.ts` | `sggarage` HOLD `on: true` -> `on: false` (+ comment). The other 6 flags and every file-type block (SECRET_NAMES, EXECUTABLE, `.htaccess`, cgi-bin/.well-known) are unchanged. |
| `base44/shared/liveGuard.ts` | New `NO_LIVE_GUARD_SITES = ['sggarage']`. For that site only, `liveGuard()` returns "allowed" right after the path check and the config/code rule (NEVER). No live-state compare, no HTML/JSON-LD/FAQ/footer checks, no file-type override, no override list. Not a narrow override: the whole light guard is off for sggarage. |
| `tests/generatedOverride.test.ts` | The old "refused for sggarage" sitemap/llms test now expects "allowed". |
| `tests/sggNoLiveGuard.test.ts` (new) | sggarage FAQ/JSON-LD/title change, footer removal, sitemap.xml, article-cards.json, robots.txt, llms.txt, live-unknown and new page all allowed; `.htaccess`, `.user.ini`, `php.ini`, `.php`, `.cgi`, `.pl`, `.py`, `.sh`, `../` and absolute paths still refused; Page One, Star, Cleanic, ContiExpert still refused exactly as before; `SGGARAGE` (wrong case) is not exempt. |

Tests (`deno test --no-check -A --import-map tests/importmap.json tests/`):
- v2: **49 passed, 0 failed** (`test-bridge-v2.txt`)
- unchanged e1d39cf: 45 passed, 0 failed (`test-bridge-e1d39cf-unchanged.txt`)

Kept for sggarage: the hourly publisher still never writes sggarage.com, and every Bridge write still makes its own per-file backup first.

## SgGarage Controller 6a9404b277a56a67dfd98681: `sggarage-controller-unlock-v2.diff` (on top of saved git 4f87f50)

The never-write lock (786127ad3 + 41c0fc4e8) is removed: every file it touched is back to the 91bbee9 (HOLD-only) version, then the v1 unlock edits are applied on top.

| File | Change |
|---|---|
| `base44/shared/neverWrite.ts` | deleted |
| `tests/neverWrite.test.ts` | deleted |
| `base44/shared/ftpClient.ts` | never-write checks removed (raw targets, resolved paths, folder-upload refusal, SITE verb words, NeverWriteError rethrow); neutral messages for the raw-FTP and unsafe-path refusals (from v1) |
| `base44/shared/ftpFileOps.ts` | never-write checks and rethrow removed |
| `base44/functions/ftpWriteFile/entry.ts`, `ftpHealthCheck/entry.ts`, `websiteCommandWorker/entry.ts` | NeverWriteError -> 403 handling and never-write audit logging removed |
| `tests/fakeFtp.ts` | the 3 test helpers added for never-write removed |
| `base44/shared/siteHold.ts` | `sggarage` `on: true` -> `on: false` (+ comment) |
| `tests/sggHold.test.ts` | HOLD refusal tests run only while the flag is ON (from v1) |
| `tests/sggUnlocked.test.ts` (new) | flag OFF: normal writes on every path go through; `.htaccess`, `.user.ini`, `.php`, `.cgi`, `.sh`, `.shtml` are now written (200) with no never-write refusal; raw `ftp.request` / `ftp.send` still refused |

Tests (`deno test --no-check --allow-env --import-map tests/importmap.json tests/`):
- v2 flag OFF: **10 passed, 0 failed** (`test-controller-v2-flag-off.txt`)
- v2 with the flag set back ON (test copy only): **10 passed, 0 failed** (`test-controller-v2-flag-on.txt`; HOLD refusals all work, unlocked tests skip with EXPECTED)
- unchanged 4f87f50: 10 passed, 0 failed (`test-controller-4f87f50-unchanged.txt`)

## What changes for SG Garage once this is saved (SPO please check)
1. **Through the SgGarage Controller, `.htaccess`, PHP and other server config/code files on sggarage.com can be written** (FTP). That is what removing the never-write means.
2. **The unsafe-path check (control character, backslash, `~`) no longer runs on this Controller while the flag is OFF.** It lives inside the HOLD check (91bbee9 design), and the never-write also enforced it. The raw FTP command block stays on always.
3. Through the Bridge, sggarage edits are no longer compared with live. **The pre-write step is a Claude procedure, not code:** before any sggarage write, Claude compares the live files with source and pulls any newer live file into source first (exactly as in 8dd497c4e), so nothing written by hand on the server is overwritten. See docs/EMERGENCY-LOCK.md.
4. The Bridge still refuses `.htaccess` and server code for every site, sggarage included.
5. All other sites: guard and flags unchanged (Page One Controller untouched).

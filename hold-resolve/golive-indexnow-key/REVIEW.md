# Go live switch: IndexNow key file (21 Nov 2026)

Why: overseastyre.my went live at 10:39pm SGT through the Controller Go live switch with every check green, but the docroot had no IndexNow key file, so IndexNow answered 422. The key file is now on that site by hand (200, key matches) and the 37 sitemap URLs were resubmitted (202).

Permanent fix (Edwin's ask: the switch and the preview template always place the key file in the site root, and a key-file check among the go-live checks):

## Bridge (bridge-goLive.diff), base = checkpoint 6b018b76 (published)
- Switch On plans the key BEFORE anything is written: a valid `<32 hex>.txt` already in the site folder wins; else the client key the Controller sends (`indexnow_key`); else the parent's standard key, read at run time from `autoseo: preview/hx-auto/`. No key at all = refused with 409 and nothing changed.
- After the page retarget succeeds and before the host rules, a missing key file is written (new file, Bridge writeFile with backup/guards, `publisher: true`). Like robots.txt, a rollback leaves it (no delete; harmless).
- New go-live check: `IndexNow key file at site root (200, key matches)`. A failure reverts the switch like every other check.
- The key is never returned, logged or put in an alert: the check info is only the HTTP status, write errors pass through `hideKey`, the result says only `added (client|standard|site key)` / `already there`. The audit row logs only site/path of the call (not the body).
- Switch Off: unchanged (no key work).
- Test: `pickIndexNowKey` order and bad-input refusal; 14 of 14 pass.

## Controller (controller.diff), base = checkpoint 6b018b7c (published)
- Both flip callers (AutoSEO panel `goLive`, Activate `clientSites` runGoLive) also send the client's `indexnow_key` when the record has one. Page One clients have no standard key, so this keeps them working when their folder has no key file.

## Template (project files, not the repo)
- `/mnt/project-files/autoseo-template/golive/golive.py`: `Cfg.indexnow_key` (site.json `indexnow_key` or env `INDEXNOW_KEY`), `files` command writes `<key>.txt` into the build root, `check` has the same key check. Tests 9 of 9 pass. README section added.

## Order to Publish
Bridge first, then Controller. Either order is safe: an older Controller just sends no key, and the Bridge then uses the folder key or the AutoSEO standard key.

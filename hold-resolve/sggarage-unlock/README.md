# SG Garage unlock (DIFF ONLY, NOT SAVED)

> **Superseded by `v2/`** ("SG GARAGE UNLOCK DIFF UPDATE 1114-2325"): use the v2 diffs. v1 below is kept for the record.

This is task "SG GARAGE UNLOCK 1114-2245". Edwin's words, relayed at 10:42pm SGT on 14 Nov 2026: "go through Claude and remove the lock".

Nothing here has been saved, published or synced. Base44 functions go live on save, so this waits for SPO's review and then Edwin's "save".

## Step 1: live compare and pull (done, read-only)
- **What was compared:** all 202 source files (commit 9ce0077) against www.sggarage.com, using GET requests from the Bridge sandbox.
  - 198 files were the same.
  - services/index.html redirects (301) over HTTP, so it was checked with a Bridge read instead. It is the same.
- **3 files had been edited on the server today**, by work done outside Claude:
  - articles/car-engine-knocking-noise-singapore.html (13:02 SGT)
  - car-servicing-repair/index.html (13:04 SGT)
  - index.html (homepage card list)
- **The pull:** the exact server bytes were taken with Bridge read_file and the sha256 of each was checked. They were committed as source in 8dd497c4e, and hold-resolve/sggarage-live-source-shas.txt was updated.
- **Pins:** SG Garage has no Bridge pins, so nothing needed re-pinning.
- **New live-only pages:** none were found. The live sitemap has no URL that is missing from the source.

## Step 2: the unlock diffs
- **`bridge-unlock.diff`** (Bluehost Bridge 6ac6d47b4ec84148578914c7, on top of git 38e9ed2):
  - Changes one line: `sggarage` goes from `on: true` to `on: false` in `base44/shared/bridgeConfig.ts` SITE_HOLDS. There is also a comment.
  - Full suite with the flag off: **40 passed, 0 failed** (`test-bridge-flag-off.txt`). The two "EXPECTED while SG Garage HOLD is ON" skips now run their isolation checks, and both pass.
- **`sggarage-controller-unlock.diff`** (SgGarage Controller 6a9404b277a56a67dfd98681, on top of git 4f87f50):
  - `base44/shared/siteHold.ts`: `sggarage` `on: true` becomes `on: false`.
  - `base44/shared/ftpClient.ts`: two refusals that are always on now give a neutral message instead of "SG GARAGE HOLD is ON". Nothing else changes in that file. The two refusals are:
    - raw `client.ftp.request/send/handle`;
    - an unsafe path containing a control character, a backslash or `~`.
  - `tests/sggHold.test.ts`:
    - The HOLD refusal tests run only while the flag is ON. With the flag OFF they print EXPECTED and skip.
    - The fail-closed flag rules are still tested.
  - New `tests/sggUnlocked.test.ts`, which checks two things with the flag OFF:
    - Normal SG Garage writes go through. This covers new file, overwrite with sha, upload, rename, mkdir, SITE CHMOD, ftpWriteFile 200, worker 200 and the health probe.
    - Server config and code are still refused (12 names, 403, audit rows), and so are folder uploads, raw FTP and unsafe paths.
  - Results:

    | Run | Passed | Failed | Log |
    |---|---|---|---|
    | Flag OFF | 14 | 0 | `test-controller-flag-off.txt` |
    | Flag ON | 14 | 0 | `test-controller-flag-on.txt` (the unlocked tests skip with EXPECTED) |
    | Unchanged 4f87f50 | 10 | 0 | |

## Never-write lock (786127ad3 + 41c0fc4e8): kept as the every-site rule
- **What it blocks:** `.htaccess`, `.htpasswd`, `.user.ini`, `php.ini`, PHP, `.cgi`, `.pl`, `.py`, `.sh`, `.shtml`, a code extension in the middle of a name, and folder uploads.
- **Why it stays:** these are the same file types the Bluehost Bridge refuses for every site (`bridgeConfig.ts` SECRET_NAMES/EXECUTABLE, liveGuard NEVER). It blocks nothing that a normal SG Garage page, article, CSS, JS, image, JSON or sitemap write needs. None of it has to be removed for SG Garage to work like the other sites.
- **Where it is stricter than the Bridge:** `.shtml`, `.php3`–`.php8`/`.pht`/`.phps`, a code extension in the middle of a name, and folder uploads. No code in the app uses folder uploads.

## Live guard (Bridge) and Edwin's own Claude edits
- **It does not block:** normal publishes, new pages, CSS/JS/images, or body edits.
- **It does block, through the Bridge:**
  - an edit that changes a title, meta description, H1, JSON-LD value, FAQ question or the review footer;
  - replacing sitemap.xml, llms.txt, robots.txt, or any .json/.txt/.xml file;
  - any delete, move or rename.
- **Today's own edits:** 2 of today's 3 server-side SG Garage edits would have been REFUSED through the Bridge (`live-guard-check.txt`).
- **The nightly SG Garage article:** its new page would go through, but its sitemap.xml and article-cards.json updates would be refused. The sitemap override saved tonight covers Page One only.
- **The SgGarage Controller FTP path has no live guard,** so writes through it are not affected.

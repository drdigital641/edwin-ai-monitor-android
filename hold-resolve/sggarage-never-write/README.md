# SG Garage Controller: permanent never-write block (DIFF ONLY, NOT SAVED)

Security review "SGG NEVER-WRITE 1114-1110", 14 Nov 2026. App: SgGarage Controller (Base44 6a9404b277a56a67dfd98681).
Nothing was saved in any Base44 app, no checkpoint, nothing published, every HOLD flag stays ON.

## What it blocks
Every FTP write path in the app refuses a target whose basename is `.htaccess`, `.user.ini` or `php.ini`, or that is
PHP code: `.php`, `.php3-8`, `.phtml`, `.pht`, `.phps`, `.phar` anywhere as an extension (so `shell.php.jpg` is refused too),
case-insensitive, after removing trailing dots and spaces, with backslashes read as slashes.

Paths covered: ftpWriteFile / safeWriteRemoteText, websiteCommandWorker, ftpHealthCheck probe write and remove,
restoreSnapshot, uploadFrom / upload / appendFrom / append, remove, rename (old AND new name), ensureDir / MKD,
raw STOR / APPE / DELE / RNFR / RNTO / SITE, and the /_chatgpt_backups backup writes. Folder uploads
(uploadFromDir / uploadDir) are always refused because they cannot be checked file by file.

- Runs before any byte is sent: in safeWriteRemoteText before a connection opens, and in the withFtp guard before every
  client call. It runs BEFORE the HOLD check and does not depend on the HOLD flag.
- No bypass flag, no override list. Change these files by hand in cPanel.
- Clear error: `NEVER-WRITE: <what> <path> refused ... Nothing was sent to the server.` HTTP 403 with `never_write: true`,
  command marked failed, ConnectionAudit row `stage: never-write-refused`. Never retried.

## Files
- `sggarage-never-write.diff` applies ON TOP of the HOLD diff `hold-resolve/sggarage-controller-hold/sggarage-controller-hold.diff` (commit 5113c84). Kept separate from the guard set.
- `neverWrite.ts` (new shared/neverWrite.ts), `neverWrite.test.ts` (fake-FTP tests).
- The 5113c84 HOLD test got two widened assertions (`refusedAny`: HoldError OR NeverWriteError) for the `/.htaccess` and `uploadFromDir` cases, because the never-write block now refuses them first. All other HOLD assertions unchanged.

## Test results (deno, fake FTP, no network)
| Run | Passed | Failed |
|---|---|---|
| HOLD on, full suite (4 never-write + 6 HOLD) | 10 | 0 |
| HOLD off (scratch copy, SG Garage docroot), never-write tests | 4 | 0 |
| Unchanged 5113c84 code + its own tests | 6 | 0 |

498 write attempts across 29 blocked name variants were refused with server bytes unchanged after each and no backup written.
With HOLD off, 13 normal .html/.css/.js/image/txt writes, a png upload, a rename, SITE CHMOD on .html and the ftpHealthCheck
probe write + remove all succeed. Entry functions: ftpWriteFile x4 and the worker x4 return 403 with 8 audit rows.
deno check: 17 errors, all pre-existing (same count as before the change).

## Limits
Covers this app only. Other writers (Alicia app cPanel token, Edwin's 13:05 job, site-rebuild.php, cPanel cron, Zen Cart,
humans) are listed in `../sggarage-controller-hold/WRITERS.md`. Saving waits for Edwin's own yes.

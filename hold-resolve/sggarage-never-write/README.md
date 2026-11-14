# SG Garage Controller: permanent never-write block (DIFF ONLY, NOT SAVED)

Security review "SGG NEVER-WRITE 1114-1110", 14 Nov 2026. App: SgGarage Controller (Base44 6a9404b277a56a67dfd98681).
Nothing was saved in any Base44 app, no checkpoint, nothing published, every HOLD flag stays ON.

## What it blocks
Every FTP write path in the app refuses a target whose basename is `.htaccess`, `.htpasswd`, `.user.ini` or `php.ini`, or that is
server code: `.php`, `.php3-8`, `.phtml`, `.pht`, `.phps`, `.phar`, `.cgi`, `.pl`, `.py`, `.sh`, `.shtml` anywhere as an extension
(so `shell.php.jpg` and `run.cgi.txt` are refused too). `.htpasswd` and `.cgi/.pl/.py/.sh/.shtml` were added in
"SGG NEVER-WRITE ADD 1114-1125" to match the Bluehost Bridge NEVER list (`.shtml` because server-side includes can run commands),
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
- `never-write-add-delta.diff` (1114-1125) adds `.htpasswd` and `.cgi/.pl/.py/.sh/.shtml` on top of `sggarage-never-write.diff`.
  Apply order: 5113c84 HOLD diff, then `sggarage-never-write.diff`, then `never-write-add-delta.diff`.
  `neverWrite.ts` and `neverWrite.test.ts` in this folder are the final versions (after the delta).
- `sggarage-never-write.diff` applies ON TOP of the HOLD diff `hold-resolve/sggarage-controller-hold/sggarage-controller-hold.diff` (commit 5113c84). Kept separate from the guard set.
- `neverWrite.ts` (new shared/neverWrite.ts), `neverWrite.test.ts` (fake-FTP tests).
- The 5113c84 HOLD test got two widened assertions (`refusedAny`: HoldError OR NeverWriteError) for the `/.htaccess` and `uploadFromDir` cases, because the never-write block now refuses them first. All other HOLD assertions unchanged.

## Test results after the 1114-1125 addition (runs-add-1114-1125/)
| Run | Passed | Failed |
|---|---|---|
| HOLD on, full suite (4 never-write + 6 HOLD) | 10 | 0 |
| HOLD off (scratch copy, SG Garage docroot), never-write tests | 4 | 0 |
| Unchanged 5113c84 code + its own tests | 6 | 0 |

1045 write attempts across 61 blocked variants (29 earlier + 32 new: .htpasswd x5, .cgi x6, .pl x5, .py x5, .sh x5, .shtml x6,
each with case, trailing dot/space and mid-name forms) refused on every write path, server bytes unchanged after each, no
backup written. Also: existing /.htpasswd and /page.shtml overwrite with the right sha refused, page.shtml.<stamp>.bak refused.
Entry functions: ftpWriteFile x10 and the worker x10 return 403, 20 audit rows. 23 normal names (incl. .htpasswd-help.txt,
cgi-guide.html, perl.html, python.html, shop.html, x.pyc, x.plist, push.js, flash.sharp.css) still write with HOLD off.

## Test results 1114-1110 (first version, deno, fake FTP, no network)
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

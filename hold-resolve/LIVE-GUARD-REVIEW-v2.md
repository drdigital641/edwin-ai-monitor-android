# Live guard v2: revised after security review (GUARD SPO CHANGES 1114-0945), DIFF ONLY

Nothing below is saved in either Base44 app. Base44 backend code goes live as soon as it is saved, so it waits for
security review + Edwin's "save the guard".
- Guard file: `hold-resolve/liveGuard.ts` on branch claude/project-thread-xc39oz, commit b647840 (copy: /mnt/project-files/hold-resolve/liveGuard.ts)
- Full unified diffs (made against the current app code, type-checked, NOT applied):
  Bridge sandbox `/tmp/g2/bridge.diff` (164 lines), Controller sandbox `/tmp/g3/controller.diff` (132 lines).
  The hunks are reproduced below.

## The 6 required changes
1. **Fail closed, three states.** The caller passes `live` = `absent` | `present{bytes}` | `unknown{error}`.
   `absent` only when the SERVER's own folder listing (cPanel `Fileman::list_files` / FTP `MLSD`) of the parent folder was
   read and has no such name, or the parent folder is itself confirmed absent the same way (never above the site root).
   An HTTP 404 is never used. `unknown` (any read/listing error, symlink, folder, other type) is REFUSED.
   The old `if (!liveBytes) return null` is gone.
2. **Live bytes from the server, exact path.** Bridge: cPanel `get_file_content` of the exact path (`readBytes`), after
   the listing shows `type=file`. Controller: FTP `RETR` of the exact path after `MLSD` shows `type=file`.
3. **Coverage.** Replacing a live file is allowed only for identical bytes, HTML that passes the SEO checks, or an
   allowlisted static type (css, js, mjs, png, jpg/jpeg, webp, avif, gif, svg, ico, woff/woff2, ttf, otf, eot). Every
   other replace (robots.txt, sitemap*.xml, llms*.txt, json, txt, xml, pdf, webmanifest, unknown) is refused unless an
   override matches. `.htaccess, .htpasswd, .user.ini, php.ini, *.php, *.phtml, *.phar, *.cgi, *.pl, *.py, *.sh` are
   refused even as new files, and no override applies to them. **The Bridge publisher no longer writes any .htaccess**
   (server rules + pinned server files removed from the hourly run; reported as `blocked`).
4. **Deletes, moves, renames.** `liveGuard` refuses op `delete`/`move`/`rename` always. Bridge: no tool deletes, moves or
   renames a live file (cPanel API2 is allow-listed to `copy`/`chmod` for backups and `compress` into ~/backups-private).
   Controller: `ftpClient.rename()` / `remove()` now throw unless the file is a fresh `tmp-upload-xxxxxxxx-*` made by
   safeWrite, so nothing can move or delete a live file (tested in a sandbox copy: both blocked).
5. **Path normalising before the guard.** `relProblem()` runs on the RAW path from the caller: refuses NUL, backslash,
   control characters, absolute paths (`/`, `C:`, `~`), URLs, and empty / `.` / `..` segments. Symlink targets are
   refused because the listing type must be exactly `file` (cPanel listing asks for all types incl. `link`; MLSD keeps
   the raw type such as `OS.unix=slink`).
6. **Comments fixed.** Both in liveGuard.ts and next to each `GUARD_OVERRIDES`: an override is live as soon as it is
   SAVED (not on Publish); any GUARD_OVERRIDES edit needs security review AND Edwin's own written yes before saving.
   An override matches only exact site + path + sha256 of the new bytes, with `by: 'Edwin'` and a `review` reference.
Optional race narrowing: done. The live state is re-read from the server just before the upload (Bridge) / just before
the rename into place (Controller); any change refuses with nothing written.

## Which write paths call it, and what happens on refusal
| App | Path | How live is read | On refusal |
|---|---|---|---|
| Bridge | `writeFile` (bridgeOps.ts): write_file, edit_file, restore_backup, and every publisher write (pinned pages, articles, sitemap/llms/articles index) | `probeLive()`: cPanel list_files of the parent + get_file_content | BridgeError 409 before any backup/upload; tool calls logged in BridgeLog by the handler audit; publisher item `status: error` with the text in PageOnePublishRun |
| Bridge | `runBulk` (write_files, sync_from_github) | `probeLive()` for every file first | dry run: `compare {same, update, create, unknown, refused}`, `would_change[]`, `guard_refusals[]`; real run: WHOLE batch refused before any write, one BridgeLog row per file (`action: live-guard-refused`) |
| Bridge | publisher .htaccess | n/a | never written (`status: blocked`) |
| Controller | `safeWrite` (bluehostFiles.ts): Upload, Restore, clientSites put + golive | `probeLiveFtp()`: MLSD of the parent + RETR | HttpError 409 before backup/upload; BluehostFileLog row ok:false with the text (existing catch) |
| Controller | `ftpClient.rename/remove` | n/a | throws unless temp upload file |
Every HOLD check still runs first (423) and stays ON.

## Side effects to know before saving
- After a HOLD lifts, the Page One publisher can no longer replace sitemap.xml, sitemap.txt or llms.txt (not HTML,
  not allowlisted) without an override, so a new article would publish but those files would be refused. Needs a
  decision (override per change, or a later reviewed rule such as "sitemap may only gain URLs").
- CSKA Booster title/meta edits and price changes need an override.
- restore_backup of an older page that changes title/meta/H1 is refused unless overridden.

## Guard tests (sandbox copy, node): all as expected
old 6966071 page over live: refused (older, lost FAQ, footer) · live over live: allowed · unknown live: refused ·
confirmed new file: allowed · robots.txt / sitemap.xml / json replace: refused · css replace: allowed ·
new .htaccess / new .php: refused · `a/../b.html`, `/etc/x`, backslash: refused · delete: refused.

## Key hunks (Bridge)
```ts
// bridgeOps.ts writeFile, after hold/blocked/size checks:
const live = await probeLive(site, rel);
const guard = await liveGuard({ site, rel: relInput, op: 'write', live, newBytes: bytes, overrides: GUARD_OVERRIDES, sha256 });
if (guard) throw new BridgeError(guard, 409);
const liveSha = live.state === 'present' ? await sha256(live.bytes) : null;
const current = opts.current ?? await readBytes(abs);
if ((current ? current.sha256 : null) !== liveSha) throw new BridgeError('LIVE GUARD: the live file changed while it was being checked; ...', 409);
// ... after backupFile, before upload:
const again = await probeLive(site, rel);
const againSha = again.state === 'present' ? await sha256(again.bytes) : again.state === 'absent' ? null : 'unknown';
if (againSha !== liveSha) throw new BridgeError('LIVE GUARD: the live file changed just before the write; ...', 409);

// bridgeOps.ts new:
export async function probeLive(site, rel): Promise<LiveState>   // listing type must be 'file', then readBytes(abs)
async function listedType(abs, root)                             // list_files types file|dir|link|char|block|fifo|socket;
                                                                 // on listing error: absent only if parent confirmed absent
// pageoneArticles.ts: publishServerRules / publishPinnedServerFiles no longer called; result { status: 'blocked' }.
// bridgeConfig.ts: export const GUARD_OVERRIDES = Object.freeze([]) (+ the save-is-live comment).
```
## Key hunks (Controller)
```js
// bluehostFiles.ts safeWrite, after writePolicy + FTP connect:
const live = await probeLiveFtp(ftp, rel);
const guard = await liveGuard({ site: 'pageone', rel, op: 'write', live, newBytes: bytes, overrides: GUARD_OVERRIDES, sha256 });
if (guard) throw new HttpError(guard, 409);
// current must equal the probed live sha, else 409; re-probe before ftp.rename(temp, rel), else remove temp + 409.
// ftpClient.ts: listAll(dir) keeps raw MLSD type; rename()/remove() only for /tmp-upload-[0-9a-f]{8}-/ files.
```

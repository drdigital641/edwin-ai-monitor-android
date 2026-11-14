# Bridge cPanel call sites: proof (14 Nov 2026, "GUARD CHOKEPOINT 1114-1010")

Taken on the v3 sandbox copy (v2 wiring + choke point), base44/ of the Bluehost Bridge app. Nothing saved in the app.
Line numbers are v3 lines.

## A. Raw cPanel transport outside shared/cpanel.ts
`grep -rnE "2083|json-api|/execute/|CPANEL\.host" base44 --include=*.ts | grep -v shared/cpanel.ts`
-> only `bridgeConfig.ts:5  host: 'https://sggarage.com:2083'` (the constant). No other file builds a cPanel request:
every call goes through uapi / api2 / api2Read / downloadFile in cpanel.ts, so the choke point sees all of them.

## B. Every call that CHANGES something on the server (uapi upload_files/save_file_content, api2 fileop/mkdir)
All are in bridgeOps.ts; none anywhere else (crawlerLogs.ts and siteFeed.ts only call domains_data, list_files,
get_file_content, LogManager/Stats reads and downloadFile of ~/logs/*.gz).

| line | call | where | target | choke point result |
|---|---|---|---|---|
| 155 | api2 mkdir | makeDir (backupFile only) | ~/bluehost-bridge-private/backups/<site>/<id> | mkdir allowed |
| 167 | uapi upload_files | putBytes | writeFile 309 + 322 (granted exact abs) and selfTest 551 (~/bluehost-bridge-private/selftest) | site path only with writeFile grant |
| 182 | api2 mkdir | ensureDirTree | site folders (writeFile 302, prepareFolders 579) or private floors | mkdir allowed, creates no file |
| 185 | api2 fileop chmod 0700 | ensureDirTree, only when permissions = 0700 | private floors only (365, 371, 393, 436, 549, 571) | private only |
| 376 | api2 fileop copy | backupFile | dest ~/bluehost-bridge-private/backups/... | private dest only |
| 378 | api2 fileop chmod 0600 | backupFile | the private backup copy | private only |
| 396, 399 | fileop compress + chmod | backupTgz (publisher deploy backup) | ~/backups-private/*.tgz | private dest only |
| 441, 446 | fileop compress + chmod | packTgz (sync backups before/added/full) | ~/backups-private/*.tgz | private dest only |

## C. The grant exists only inside writeFile
`grep -rn withSiteWriteGrant base44`
- cpanel.ts:41 definition
- bridgeOps.ts:6 import
- bridgeOps.ts:309 writeFile upload step
- bridgeOps.ts:322 writeFile restore-on-mismatch step

## D. Every tool reaches the server through writeFile
`grep -rn "writeFile(" base44` (callers):
- functions/bridgeWrite/entry.ts:4: write_file -> writeFile
- bridgeOps.ts:348: editFile (edit_file) -> `writeFile(site, rel, new TextEncoder().encode(text), file.sha256, { current: file })`
- bridgeOps.ts:523: restoreBackup (restore_backup) -> reads the private backup (`readBytes(BACKUP_ROOT/...)`), then
  `writeFile(site, rel, saved.bytes, current?.sha256 || null, ...)`; it never copies the backup into the site.
- bulkWrite.ts:124: runBulk -> writeFile per file (write_files via writeMany; sync_from_github via runBulk)
- githubSync.ts:150: syncFromGithub -> `runBulk(site, {...planned}, ctx, ...)`; its only other server steps are
  syncBackupBefore (146) and syncBackupAdded (153) = packTgz into ~/backups-private.
- pageoneArticles.ts:784, 786, 816, 829, 844: publisher -> writeFile (site 'pageone' only; .htaccess blocked in v2)

Bodies (v3 sandbox):
- editFile (bridgeOps.ts 331-350): loadFile (normalizeRel, readBlockedReason, resolvePath, readBytes) -> text edits -> line 348 writeFile.
- restoreBackup (bridgeOps.ts 515-525): backup_id regex, normalizeRel, readBytes from BACKUP_ROOT, resolvePath, readBytes(abs), line 523 writeFile.
- syncFromGithub (githubSync.ts 109-160): validate request, download from GitHub at a commit sha, holdReason pre-check (141),
  syncBackupBefore (146), line 150 runBulk -> writeFile, syncBackupAdded (153).

So even if a future caller skips writeFile, the choke point refuses any upload/copy/chmod into a site folder and every
move/rename/unlink/trash/extract, because only writeFile holds a grant.

## E. Percent-encoded paths
normalizeRel (bridgeOps.ts 55-70) never decodes anything: no decodeURIComponent/unescape in the Bridge path code, and
every segment must match `^[A-Za-z0-9._\-~@+() ]+$`, so "%" is refused before resolvePath. The choke point refuses "%"
in any absolute destination too, and fileop must pass doubledecode=0 so cPanel does not decode either.
Test: tests/cpanelChokepoint.test.ts ("percent-encoded paths can never decode into a path walk").

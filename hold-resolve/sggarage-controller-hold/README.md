# SG Garage HOLD for the SgGarage Controller app (diff only)

14 Nov 2026, "SGG CONTROLLER HOLD 1114-1040". App: **SG Garage — FTP Code Bridge**, Base44 6a9404b277a56a67dfd98681 (sandbox /app at c579ccc).

**Nothing was saved in any Base44 app, nothing was published, and no checkpoint was made** (create_checkpoint would save the functions, and Base44 backend code is live on save). The app's /app tree is unchanged (`git status` clean at c579ccc). The diff was built and tested in a throwaway copy, /tmp/h1/b in that app's sandbox.

## What the diff does (`sggarage-controller-hold.diff`, 239 lines, 5 files changed + 1 new)

- **New `base44/shared/siteHold.ts`**
  - `SITE_HOLDS = [{ key:'sggarage', on:true, docroot:'/home3/sgmodde1/public_html/carbonfibre' }]`, the same pattern as the Bridge and the Page One Controller.
  - `holdOn()` **fails closed**. The hold counts as ON when the entry is missing or malformed, when `on` is anything but the boolean `false` (`'false'` and `0` both still count as ON), and when reading the flag throws.
  - `HoldError` is the refusal error (status 423). `logHoldRefusal()` writes a ConnectionAudit row `{stage:'hold-refused', status:'fail', detail}`.
- **`shared/ftpClient.ts` `withFtp()`** is the only place this app opens an FTP connection. Every caller now gets a guarded client.
  - **Read-only methods pass:** list, cd, pwd, size, lastMod, downloadTo and the like.
  - **These are checked before anything is sent:** uploadFrom/upload, appendFrom/append, remove, removeDir, removeEmptyDir, clearWorkingDir, rename (both ends), ensureDir (mkdir), uploadFromDir/uploadDir. So are `send()` and `sendIgnoringError()` with STOR, STOU, APPE, DELE, RNFR, RNTO, MKD, RMD, SITE, MFMT or MFCT.
  - **Raw access is blocked:** `client.ftp.request`, `send` and `handle` are refused.
  - **Unknown methods are treated as writes,** so they are refused too.
  - **How a path is judged to be SG Garage:**
    - It is resolved against the current folder, with `.` and `..` worked out. Backslash, control characters and `~` are refused.
    - It is SG Garage if any of its segments is `carbonfibre`. That covers /carbonfibre, /public_html/carbonfibre and /home3/sgmodde1/public_html/carbonfibre.
    - It is SG Garage if the FTP root, or the folder the login lands in, lists an SG Garage-only marker file (`site-renderer.php` or the IndexNow key `adba3d20…txt`). In that case the whole tree under that folder is held.
    - If that listing fails, the write is refused (fail closed) and the check is not cached.
  - Hold refusals are never retried.
- **`shared/ftpFileOps.ts` `safeWriteRemoteText()`**
  - A HoldError from the upload step is rethrown as it is. It used to be swallowed as an "upload error" and then sent through a rollback.
  - The backup into `/_chatgpt_backups/...` is a write as well, so it is refused inside SG Garage.
  - CONTROLLER_VERSION is now `sggarage-ftp-2026-11-14.hold`.
- **Entry functions:**
  - `ftpWriteFile` returns 423 and logs the refusal.
  - `websiteCommandWorker` marks the WebsiteCommand `failed` with the hold message, returns 423 and logs the refusal.
  - `ftpHealthCheck` returns 423 and logs the refusal (its probe write and delete). `write_test:false` still passes, because it only lists and reads.
- **Not changed:** ftpReadFile, ftpListFiles, entities, the workflow, the agent and the frontend.

## Tests (`tests/`, results in `test-output.txt`): 6 of 6 pass

The tests use a fake in-memory FTP server, a fake Base44 SDK and a fake runtime. There is no network and nothing is saved. Every refusal also asserts that the server state is byte-identical and that no write call was made. To run them:

`deno test --no-check --allow-env --import-map tests/importmap.json tests/sggHold.test.ts`

What the six tests cover:

1. **The flag fails closed.** Eight malformed or missing variants all count as ON. Only `on:false` counts as OFF.
2. **The FTP root is the SG Garage docroot.**
   - Refused: overwrite, new file, .htaccess, the backup folder, remove, rename, removeDir, clearWorkingDir, ensureDir, uploadFromDir, an unknown method, `send DELE`, `SITE CHMOD`, and raw `ftp.request`.
   - Still allowed: reads, NOOP and SIZE.
3. **The FTP root is the account home.**
   - Refused: carbonfibre paths, a relative path after `cd`, a `..` walk, rename out of carbonfibre, rename into carbonfibre, backslash paths and `~` paths.
   - Still allowed: a write elsewhere, `/_cleanic_control/validation/probe.txt`.
4. **The check cannot be completed.** A login folder carrying the marker is refused, and so is any write when the root listing fails.
5. **Hold explicitly off.** The same write goes through, which shows the guard is the only thing blocking it.
6. **Entry functions.** ftpWriteFile, ftpHealthCheck and websiteCommandWorker each return 423, the command is marked failed, three `hold-refused` ConnectionAudit rows are written, and the server is unchanged.

Type check: `deno check` gives 17 errors before and 17 after. All of them already existed (implicit `any`, and the fake `access()` signature). The diff adds no new type errors.

## Limits (say plainly)

- A symlink with some other name that points into carbonfibre, from an FTP root that is neither the docroot nor shows `carbonfibre` in the path, would not be caught by the name or marker checks. **The real fix is in cPanel:** restrict this app's FTP account to the folder it is meant for (FTP Accounts, then Directory).
- We could not confirm the FTP root, because the FTP secrets are not readable from the sandbox and we did not connect. The health probe uses `/_cleanic_control`, which suggests the root is Cleanic's folder or the account home.
- **If the root is a public docroot, `/_chatgpt_backups/` holds web-public .bak copies.** Edwin should check this in cPanel File Manager.
- This guards this app only. Other writers are in `WRITERS.md`.

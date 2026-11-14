# Emergency lock: how to stop or allow changes to a live website

Written 14 Nov 2026 for Edwin ("SG GARAGE UNLOCK 1114-2245"), updated for "SG GARAGE OPTION C 1114-2335".
Standing rule: **all coding on every client site goes through Claude, so the repo copy always matches live.**

## 1. The fast way: just tell Claude

Send one of these messages in the Page One project:

```
LOCK sggarage now
```

```
UNLOCK sggarage
```

You can use any site key from the table in section 2, or say `LOCK everything`.

Here is what happens after you send it:

1. **Claude prepares the change.** Claude sets that site's flag to `on: true` (lock) or `on: false` (unlock) in every app listed for the site. It runs the tests and gives you the checkpoint ids.
2. **Claude saves it.**
   - A **lock** is saved straight away. Locking only stops writes, so it is always safe.
   - An **unlock** waits for SPO's review and your "save".
3. **You press Publish** on each checkpoint. Press **Publish only, never Activate**.

The lock is fully on only after step 3. Saving alone does not cover everything:

| App | What the flag stops as soon as it is **saved** | What it stops only after you **Publish** |
|---|---|---|
| Bluehost Bridge | The hourly :25 publisher. | The Bridge tools Claude and ChatGPT call: write_file, edit_file, write_files, sync_from_github, restore_backup. |
| Page One Controller | Its FTP writes. | Same as on save. |
| SgGarage Controller | Its FTP writes (ftpWriteFile, the website command worker, the health check probe). | Same as on save. |

Base44 backend code is live when it is saved, so treat every save as live.

## 2. Flag names per site and app

Each flag sits in a `SITE_HOLDS` list. `on: true` means locked: nothing in that app may write the site's live files. `on: false` means unlocked.

| Site | Flag key | Bluehost Bridge (`6ac6d47b4ec84148578914c7`), file `base44/shared/bridgeConfig.ts` | Page One Controller (`6ac7f2548a9c3877449e2772`), file `base44/shared/bluehostFiles.ts` | SgGarage Controller (`6a9404b277a56a67dfd98681`), file `base44/shared/siteHold.ts` |
|---|---|---|---|---|
| Page One (pageonesingapore.com, not the client folders) | `pageone` | yes | yes | no |
| SG Garage / Edwin Garage (sggarage.com) | `sggarage` | yes | no (this app cannot reach sggarage.com) | yes |
| Star Performance (preview/star-performance) | `star` | yes | yes | no |
| Klar Details (preview/klar-details) | `klar` | yes | yes | no |
| CSKA (preview/cska-auto) | `cska` | yes | yes | no |
| Jacky Gearbox (preview/dmts) | `jacky` | yes | yes | no |
| Benjamin Poon (preview/benjamin-poon) | `ben` | yes | yes | no |

**Fail-safe:** if a flag is missing, misspelled or cannot be read, the site counts as **locked**.

**Not covered by any flag:** these can still change a live site:
- writes outside these apps, such as cPanel File Manager, Edwin's own outside jobs, site-rebuild.php, cPanel cron and Zen Cart;
- the Alicia app's cPanel token;
- the Cleanic and ContiExpert tools.

The list of writers is in `hold-resolve/sggarage-controller-hold/WRITERS.md`. To stop everything at once, change the cPanel password, then ask Claude to update the stored secrets. Claude only ever sees secret names, never their values.

## 3. Rules that apply to every site, locked or not

Updated for "SG GARAGE OPTION C 1114-2335". The v2 plan (no live guard for SG Garage, never-write lock removed) is **DROPPED**: the live guard and the never-write lock stay. Points marked **(Option C, once saved)** are draft diffs in `hold-resolve/sggarage-option-c/`; they run only after SPO's review and your "save".

**Flags now:** all 7 Bridge flags OFF (Bridge git 33343ea). SgGarage Controller `sggarage` flag OFF (git ac87bd6). Page One Controller flags OFF.

- **Server config and server code are never written by the Bluehost Bridge**, for any site (sggarage included). This covers `.htaccess`, `.htpasswd`, `.user.ini`, `php.ini`, PHP files, `.cgi`, `.pl`, `.py` and `.sh`. The Page One Controller has the same rule.
  - The one exception: the publisher may write a reviewed, pinned `.htaccess`.
  - To change these files, edit them in cPanel File Manager or ask Claude for a reviewed exception.
- **SgGarage Controller never-write lock stays** (786127ad3 + 41c0fc4e8). It refuses `.htaccess`, PHP and other config/code files on sggarage.com over FTP, and refuses raw FTP commands, whatever the flag says.
- **Live guard (Bluehost Bridge), every site including SG Garage:** an overwrite of a live file is refused if any of these is true:
  - It is an HTML page that would change or lose a title, meta description, H1, JSON-LD value, FAQ question or the "Leave us a Google review" footer.
  - It is a robots.txt, sitemap, llms.txt, .json or other data file. Exceptions:
    - the hourly publisher may update sitemap.xml, sitemap.txt and llms.txt for Page One and its 5 client folders (saved);
    - **(Option C, once saved)** SG Garage only: sitemap.xml, sitemap.txt, llms.txt and article-cards.json at the sggarage root, with content checks (safe well-formed sitemap, https-only sitemap.txt, non-empty llms.txt, strict article-cards.json shape that never drops a live card). As drafted this is for the publisher only, which does not write sggarage today; the optional "tools delta" also lets Claude's Bridge tool calls (the night article run) use it.
  - It is a delete, move or rename.

  New pages, CSS, JavaScript, images and normal body text edits go through. Anything else needs a reviewed override, which Claude prepares and you approve.
- **(Option C, once saved) SgGarage Controller side door closed.** Inside the SG Garage folder, the SgGarage Controller refuses (403, logged as `side-door-refused`):
  - delete, rename, folder removal and every SITE command (DELE, RNFR/RNTO, RMD, SITE CHMOD and the rest). The one exception is the health check's own probe file `_cleanic_control/validation/chatgpt-health-<id>.txt`, and a rollback removing a new file it just created;
  - an HTML overwrite that would change or lose a title, meta description, H1, JSON-LD value, FAQ question or the footer (the Bridge's own check, copied byte for byte);
  - a raw HTML upload or append that skips that check.

  Other sites reached by this Controller are not affected.
- **Before any sggarage write, Claude still follows the pre-write step:**
  1. Compare the live files with the repo source (GET from www.sggarage.com, or Bridge read_file).
  2. If a live file is newer (someone edited it on the server), take the exact server bytes, check the sha256, commit them as source, and only then make the change on top.
  3. Make the tgz backup in `~/backups-private/` and tell you its path, then write.
- `LOCK sggarage now` (section 1) stops all writes at once.

## 4. What the hourly :25 publisher does

- **When:** every hour at :25 (cron `25 * * * *`), the Bluehost Bridge "Page One Article Publisher" runs.
- **Code it runs:** the Bridge's **saved** (sandbox) code, so no Publish is needed.
- **Where it writes:** **Page One only** (pageonesingapore.com and its preview/ client folders). It never writes sggarage.com.
- **What it writes:**
  - new and changed Page One articles;
  - the Page One sitemap.xml, sitemap.txt and llms.txt (regenerated);
  - every "pinned" file whose recorded copy differs from its pin (in `pageoneArticles.ts` SITE_SRC and `clientAssets.ts`).
- **Before any pinned file:** it makes a tgz in `~/backups-private/pageone-deploy-<time>Z.tgz`. If that backup cannot be verified, it writes nothing.
- **When it skips a site:** if that site's flag is ON, the publisher skips it and logs 'held'.
- **Gotcha:** if someone edits a pinned file on the server, the next :25 run puts the pinned version back. Ask Claude to pull the server copy into the repo and re-pin it first.

## 5. Restoring from ~/backups-private

Backups are on the Bluehost server in `~/backups-private/`. That folder is private and is not on any website.

| File name | What it holds |
|---|---|
| `<site>-pre-<task>-<date>-<time>.tgz` | Your own backups before a job, e.g. `sggarage-pre-unlock-20261114-2245.tgz` |
| `pageone-full-<folder>-<time>Z.tgz` | The whole target folder, taken by sync_from_github before it replaced files |
| `<site>-sync-before-...tgz` / `<site>-sync-added-...tgz` | The files a sync replaced / the new files it added |
| `pageone-deploy-<time>Z.tgz` | The pinned files the :25 publisher was about to replace |

There are also per-file Bridge backups (`~/bluehost-bridge-private/backups/`), taken before every Bridge write.

**Easiest:** tell Claude which file and roughly when, for example:

```
Restore sggarage index.html to how it was before 10pm tonight
```

Claude finds the backup with `list_backups`, restores only that file with `restore_backup` (which backs up the current version first, so it can be undone), and then checks the live page.

**By hand in cPanel (when Claude is not available):**

1. Open cPanel, then **File Manager**, then go to `backups-private`.
2. Right-click the .tgz and choose **Extract**. **Extract into a NEW empty folder** such as `restore-tmp`. Never extract into `public_html` or a site folder, because that overwrites everything at once.
3. Open `restore-tmp`, find the file you need, and **Copy** it to the same place in the site folder. Say yes to overwrite only for that file.
4. Check the page in a private browser window, then delete `restore-tmp`.

After a restore by hand, tell Claude. The repo copy must be updated to match live, or the next sync or :25 run could undo your restore.

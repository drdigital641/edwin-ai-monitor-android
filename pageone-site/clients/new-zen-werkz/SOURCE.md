# New Zen Werkz source of truth (7 Nov 2026)
- Builder: THIS folder (/mnt/project-files/new-zen-werkz): build.py, build_zh.py, local_pages.py, zh_lib.py, zh/, local/.
  Build here (it needs ../tracking/wa-tap-counter.js): `python3 build.py && python3 build_zh.py`.
- Articles: add a dict at the TOP of ARTICLES with date='YYYY-MM-DD' (SGT) and faqs=[(q, a), ...]. Launch articles have no date and use UPDATED (2026-11-06).
  Sitemap lastmod is per page: an article's own date; home and /articles/ move only when a newer article is added. Never bump UPDATED to "refresh".
- Repo copy: pageone-site/clients/new-zen-werkz. Latest: branch claude/project-thread-inxk53, commit ae382988b (8 Nov 2026 SGT: added car-aircon-not-cold-singapore EN+ZH; synced, icons excluded).
- 10 Nov 2026 SGCW push 3: brake-warning-signs got an ABS section + one disclosed link to sgcarworkshop.sg/areas/kaki-bukit-industrial-estate/ (EN+ZH, updated 2026-11-10). Repo copy now on claude/project-thread-sbl84y with everything above. Never re-sync favicon.svg from this folder (the mount adds C2PA metadata); when syncing, exclude favicon.svg, apple-touch-icon.png, icon-192.png, icon-512.png (repo copies are older than live; restored from backup 10 Nov).
- 10 Nov 2026 night (even-c2): added car-pulling-to-one-side-steering-wheel-shaking EN+ZH; builder/strings in this folder are current. Changed files only (diff vs live) synced from commit 85ca5dc01 on branch night-2026-11-10-even-c2 (client-builds/2026-11-10/new-zen-werkz, source in new-zen-werkz-src); the repo copy on claude/project-thread-inxk53 does not yet have this article, so copy from this folder next time.
  After a change: copy build.py, build_zh.py, local_pages.py, zh/, local/ and site/ (no site/img) into the repo folder on your branch, commit, push,
  then Bridge sync_from_github {site: pageone, ref: <sha>, source_path: pageone-site/clients/new-zen-werkz/site, base_path: preview/new-zen-werkz}, and update this file.
- IndexNow key ea97d7cd7c1340c781fcd248d8d2c2ec (watchdog/indexnow.py).

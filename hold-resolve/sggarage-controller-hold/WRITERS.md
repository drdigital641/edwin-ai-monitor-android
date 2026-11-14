# Every known job that can write to SG Garage's docroot (/home3/sgmodde1/public_html/carbonfibre)

14 Nov 2026, "SGG CONTROLLER HOLD 1114-1040". Source checked against the snapshot at commit 9ce0077 (pageone-site/clients/sggarage/site, 202 files, equal to live).

"Blocked by Bridge HOLD" means the Bluehost Bridge (Base44 app 6ac6d47b) currently refuses the write with 423 because `SITE_HOLDS` has sggarage set to on (check at bridgeOps.ts:267). Nothing else is guarded by that flag.

| # | Writer | How it writes | Schedule | Blocked by Bridge HOLD? | Source it writes from |
|---|---|---|---|---|---|
| 1 | **Bluehost Bridge** tools: bridgeWrite, bridgeEdit, bridgeWriteMany, bridgeSyncGithub, bridgeRestore | cPanel UAPI through writeFile (bridgeOps.ts:263) | on call | **YES** (and the v3 choke point is drafted, not saved) | whatever the caller sends (see 2 to 5) |
| 2 | **Night run** scheduled task trig_01BTQ8xw…, "Page One night run (1:05am)" | Bridge sync_from_github of sites/sggarage/articles-drop, plus edit_file of sitemap.xml, articles/index.html and llms.txt | daily 01:05 SGT | **YES**: its prompt skips SG Garage ("skipped: Bridge HOLD"), and the Bridge refuses anyway | **OLDER**: builders on night-2026-11-14-even-g-sggarage (545a341b footer.html + build_*.py) predate 9ce0077 and must be rebased on it before the hold lifts |
| 3 | **Watchdog** scheduled task trig_01Csk8…, "Page One watchdog" | Bridge edits ("fix through the site's normal path") | daily 05:30 SGT | **YES** | edits the live file in place (reads live first); no repo source |
| 4 | **Weekly near-miss check** scheduled task trig_01SKyAJ… | Bridge edits to titles, meta and H1 on all live clients, SG Garage included | Sundays 08:37 SGT (next 15 Nov) | **YES** | live file plus "mirror in /mnt/project-files/<site>/build.py", which is **OLDER** than 9ce0077 for SG Garage |
| 5 | ChatGPT Custom GPT / BridgeNote pickup / Bridge site keys | Bridge tools | on call / nightly pickup | **YES** | whatever is sent |
| 6 | **Bridge hourly publisher** (pageoneArticles.ts) | Bridge, SITE_KEY='pageone' (line 23) | hourly at :25 | n/a: **cannot reach SG Garage** | Page One only |
| 7 | **Page One Controller** (6ac7f254) FTP | its FTP root is the Page One docroot | on call | n/a: **cannot reach SG Garage** (it has its own SITE_HOLDS) | Page One only |
| 8 | **SgGarage Controller** (6a9404b2, "SG Garage — FTP Code Bridge"): ftpWriteFile (safeWriteRemoteText, entry line 17), websiteCommandWorker (line 65), ftpHealthCheck (probe write line 41, `client.remove` line 52), restoreSnapshot (`remove` ftpFileOps.ts:125) | direct FTP (basic-ftp) with its own FTP_* secrets, plus backups to /_chatgpt_backups | **no schedule**. The "Process Website Command" workflow is effectively off (its condition is `status == "__disabled_use_explicit_process_tool__"`). Called by the admin FtpBrowser page, the cleanic_manager agent, admin calls, or CRON_KEY calls | **NO**. Blocked once **this diff** is saved | no repo source: writes whatever content the caller sends. No file-type block, so php and .htaccess are writable today |
| 9 | **Alicia app** (AliciaOngProperty 6abfbd74): httpsPublisher, sofaHttpsPublisher, sofaProductionPublisher, dannyHttpsPublisher, plus the sofaSchedule and dannySchedule schedules | cPanel save_file_content/upload_files with a token for the **whole sgmodde1 account** | its own schedules (SofaCare / Danny / Alicia) | **NO**. Its code only targets website_cf18616c / 4f2228cb / 661a0adc and private folders (SITE_CHANGE_ALLOWLIST + assertPublicationPath), never carbonfibre, but nothing outside its own code stops it | its own sites' sources; never SG Garage files |
| 10 | **Edwin's outside 13:05 job** | writes straight to the server, never through the Bridge | daily ~13:05 SGT (stopped publishing new SG Garage articles after 6 Nov) | **NO** | **unknown**; not in this repo |
| 11 | **site-rebuild.php / site-renderer.php** (PHP in the docroot, modified 13 Nov 01:53Z) | server-side PHP. A mass article rewrite on 13 Nov 01:28 to 02:02Z is not in BridgeLog | unknown trigger (web hit or cron) | **NO** (the Bridge never runs it) | renders from its own templates and data on the server: **unknown vs 9ce0077** |
| 12 | **cPanel cron jobs** | anything | unknown | **NO** | unknown. The Bridge cannot list cron (no Cron UAPI in its allow-list): **Edwin to check cPanel > Cron Jobs** |
| 13 | **Zen Cart shop / zc_admin** (PHP shop in the same docroot) | writes cache, logs, uploads and images | on use | **NO** | not source-tracked (left out of the snapshot on purpose) |
| 14 | **Cleanic AI Controller** (6a8f0a27) | not inspected (rule: don't touch Cleanic) | its own writer workflows | unknown | unknown. If its FTP or cPanel account reaches carbonfibre it is a writer |
| 15 | Humans with cPanel File Manager / FTP | manual | n/a | **NO** | n/a |

Other scheduled tasks on the account were checked and **do not write SG Garage**:
- Autotex nightly 02:13 (Autotex only)
- SG Commercial Fitout 00:00 (preview/rc-design-build)
- Cleanic Express safety check (one-shot, Cleanic Base44 only)
- Daily Claude cost check
- AutoKnowledge correction review
- Page One monthly security reminder (read-only)
- Disabled: SGCW screening, R&C concept, Page One Claude worker, Cleanic visitor alerts, AutoKnowledge hourly

Other Base44 apps grepped with no cPanel or FTP writer: SearchInsight Bridge, Edwin AI Monitor, SofaCare SG, Danny, AutoKnowledge.

**Gaps that this diff does not close:** #9, #10, #11, #12, #13, #14 and #15. Two account-level fixes cover most of them:
- (a) Restrict each FTP account and API token in cPanel to its own folder, or give the Alicia app its own scoped cPanel user.
- (b) Review the cPanel Cron Jobs list and how site-rebuild.php gets triggered.

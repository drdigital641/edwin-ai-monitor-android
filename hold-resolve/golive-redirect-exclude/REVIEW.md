# Go Live redirect exclusions + base-switch gate (23 Nov 2026)

Why: the sgautobots.com Go Live block 301'd every /preview/sg-autobots/* path, including /preview/sg-autobots/booking/.
The hand fix (one negative RewriteCond for booking) is live; this makes it permanent in the generator.

## Bridge app (checkpoint 6b04580fa6eea27963e8b2ed, commits 112b4f9..4592fce)
- shared/goLivePure.ts: cleanExcludes (validated, lower-cased, sorted), detectApps (subfolder with index.php, admin/ or api/),
  notesApps (SITE-NOTES "separate app" lines), excludeConds before the folder 301 in parentBlock + htaccess, previewLeft, lineDiff.
- shared/goLive.ts: redirectExcludes (Controller list + x-site-map + auto), excluded folders skipped by retarget,
  op plan (dry run: diff, exclusions, preview refs left), sslDirect (TCP to 173.254.31.20 + startTls SNI, apex + www) in domainStatus,
  goLiveCheck adds: 0 preview refs (files + served home/inner/sitemap/robots/llms), CSS/JS/images 200 on home + 3 inner,
  excluded app not redirected, preview inner page 301 same path. Failed gate = switch-on reverted, refused, never live.
- shared/runnerOpenapi.ts: x-site-map golive_redirect_exclude {"pageone preview/sg-autobots/": ["booking"]}.
- tests/goLive.test.ts: 6 new tests, incl. byte-identical sg-autobots block. 26/26 pass.

## Controller app (checkpoint 6b0458112b0ce1620da01e53, commit 23e8354)
- entities/Client.jsonc: redirect_exclude (array of strings). Client sg-autobots set to ["booking"].
- functions/goLive + clientSites runGoLive: send redirect_exclude on every flip; goLive action plan (dry run).

## Template
- autoseo-template/golive/golive.py + test_golive.py (copies here): clean_excludes, detect_apps, exclusion lines in parent_block + htaccess. 14 pass.

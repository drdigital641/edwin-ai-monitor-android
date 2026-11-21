# Go-live Activate fix (21 Nov 2026, thread "Fix SGCarAccident go-live permanently")

## What broke
Edwin pressed Activate for sgcaraccident.sg at 7:33pm SGT. The Bridge domain gate (bridgeGoLive flip) refused because DNS had
no A record yet, so nothing was changed. Controller clientSites golive_run then set the client back to "preview" and never retried.
Edwin set the status to Live by hand; the domain then served the untouched preview pages, whose CSS/JS links are
/preview/sgcaraccident/assets/... (404 on the domain, docroot = the folder), so the site rendered unstyled.
Second gap found while fixing: even a passing flip only rewrites .html + sitemap/robots/llms. Data files (assets/centres/*.json)
and data-base="/preview/<slug>/" attributes keep preview paths.

Fixed by hand on live already (repo build switched to live, sync_from_github 28f433b, root .htaccess golive block, backup 20261121-120531-73816d).

## Change 1: Bridge (app 6ac6d47b...) shared/goLivePure.ts + shared/goLive.ts  (bridge-goLive.diff)
- stripPreviewPaths(): live only, after the attribute pass, any remaining root-relative /preview/<slug>/ (after quote, ( = , or space) -> /.
- retargetAsset(): CSS/JS/JSON/webmanifest = retargetText + stripPreviewPaths.
- retargetFiles also visits text assets (.css .js .mjs .json .webmanifest, not *.min.js, <600 KB); unchanged files are not written.
- Post-check "no preview URL left on home" now really checks previewPath (old check looked for "//" and never failed).
- New unit test; 13/13 pass. Real preview home + aig.en.json from commit 92f14ba -> 0 preview paths left.
- Same write path as before (writeFile publisher:true, base sha, backup, rollback list). No new endpoints, keys or scopes.

## Change 2: Controller (app 6ac7f254...) functions/clientSites/entry.ts  (controller-clientSites.diff)
- runGoLive() extracted from golive_run. Domain-gate refusal (DNS/https not ready, nothing written) -> status activating,
  design_job golive_waiting, plain message; no longer drops back to preview.
- Retries by itself: check_all (runs on every Clients page open; max 1 switch per call), Check now, and set_status live.
- set_status live on a hand-built site that has not switched runs the switch; refuses with the reason if it cannot.
- runCheck: hand-built sites have no p1-site tag -> site check = same <title> as the preview; status live only when golive is true.
- golive_working counts as pending only when older than 10 min (no double switch beside a running Activate).
- deno check: 140 errors before and after (all pre-existing, none in the new code).

## Review asks
Security/privacy: no secret values printed; BRIDGE_GOLIVE_KEY read as before; no new public surface.
Correctness: regex in stripPreviewPaths; retry loop cannot run twice at once; nothing marks a site live without a passed switch.

## Round 2 (after SPO review 1 = FAIL, 2 blockers)
- Auto-retry (check_all) only for design_job golive_waiting, status activating/live, and not while golive_lock_at < 5 min. Failed switches retry only on Check now / Activate / set Live.
- goLiveFlow requires design_job golive_* (went through Activate) and status activating/live, so old failed previews are never switched by themselves.
- runGoLive takes a lock (golive_lock_at) before the Bridge call and clears it on every outcome; a held lock returns busy.
- runCheck uses custom !== false consistently; a hand-built site in the Activate flow only goes Live with golive true.
- set_status live: any hand-built site in the Activate flow runs the switch (not only waiting/failed).
- golive_run: waiting = 200 with client (row shows the waiting message); failure = 409 with an error field.
- Bridge refusal is HTTP 200 (confirmed: the 7:33pm refusal reached the refused branch under the old !resp.ok check).
- Known nit kept: switching Live OFF does not re-add /preview/<slug>/ inside JSON/data-base (rare path; HTML attributes still restored).
- Schema: Client gets golive_lock_at (date-time string).

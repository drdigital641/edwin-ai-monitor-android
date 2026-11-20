# Review: Controller site-checker load limits (20 Nov 2026)

Why: Bluehost ticket I-27487071 flagged ~8,400 requests from the Controller's "PageOneSiteChecker/1.0" (/ 2,900, /sitemap.xml 1,090, /llms.txt 578, /articles/ 539, /robots.txt 257 in 110 minutes). Edwin approved cutting it. Publish only, never Activate.

Cause found in base44/functions/portfolio/entry.ts action "refresh":
- The 30-minute gate only applied to the scheduled run (no user). The dashboard calls refresh itself whenever status says `stale`, and polls every 2 minutes, so every open dashboard (and the Re-check button) bypassed the gate.
- A run that timed out saved nothing, so `stale` stayed true and the next poll started another full run: a retry loop when Bluehost is slow.
- Every run did a heavy check on every site: timeHome (up to 2 GETs), basics (/, robots, sitemap, llms, plain/www variants), checkArticles (sitemap, hub, article pages), and a second GET of /.

Change (portfolio-checker-limits.diff, plus 3 fields in PortfolioSite, see PortfolioSite.addition.txt):
- One refresh per 30 min in total for ALL callers (idle:'recent' otherwise).
- Light check per site every 30 min: one plain GET of the homepage only, no retry, body cancelled.
- Heavy check (basics + sitemap/robots/llms + article hub/pages) at most once per 24 h per site, max 4 sites per run (oldest first), so it is spread over the day; a site waiting on a fresh article check may repeat after 6 h, never sooner.
- Back-off on failure or timeout: 1 h, 2 h, 4 h, 6 h cap; the failed site is skipped until then; the heavy check never runs on a site whose light check failed. Two fails in a row show "Homepage did not answer" on the dashboard; one good check clears it.
- Spread: 2 workers (was 3), 0.8-1.6 s random pause after each site; the claim (light_at) is written before the fetch so overlapping runs skip it.
- status: `stale` is now "no light check for 2 h" (or an article check pending), not "heavy check older than 6 h".
- timeHome (2 GETs per site) is no longer called; the light GET time is reused as responseMs.

Expected load: about 1 homepage GET per site per 30 min (was ~10-20 requests per site per run, run unbounded) plus at most 4 heavy checks per 30 min.

For the reviewer: no new secret, no new outbound host, same safeFetch against our own client domains; entity fields are plain strings/number; RLS unchanged (admin only). Other callers left as is: crawlerMonitor (every 6 h, 4 GETs/site, labelled synthetic), siteMonitor (hourly, pageonesingapore.com only), autoseoLink/autoseoAdmin/prospectEngine (on demand).

Not saved in Base44 yet (code goes live on save). After PASS: apply diff + entity fields, create checkpoint (call twice, see memory gotcha), Edwin Publishes (never Activate).

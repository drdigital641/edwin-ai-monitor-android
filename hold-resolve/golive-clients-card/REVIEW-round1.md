# clients_card review, round 1 (independent, read-only, 21 Nov 2026)

Scope: bridge/goLiveClientsPure.ts, bridge/goLiveClients.ts, tests/goLiveClientsPure.test.mts, the two controller/*.edit.json, against Bridge HEAD (bridgeOps.ts, goLive.ts, goLivePure.ts, handler.ts, liveGuard.ts, imageGate.ts, bridgeConfig.ts) and Controller goLive/clientSites entry.ts.
The test passes locally (node 22, `--experimental-strip-types`): ALL PASS, all 3 pages byte-for-byte.

## Checked and OK
- Imports: `BridgeError, probeLive, readLiveFile, writeFile` are all exported by bridgeOps.ts; `cleanDomain` by goLivePure.ts; `registryFor` by goLive.ts. Signatures match (`writeFile(site, rel, bytes, expectedSha, opts)`, `readLiveFile(site, rel)` returns `content` + `base_sha256`, `probeLive(site, rel)` returns `{state: present|absent|unknown}`).
- No circular import: goLive.ts imports bridgeOps, htaccess, goLivePure, autoSitemapRun. None of them import goLiveClients.ts. The entry imports both, which is fine.
- writeFile: a new file with `expectedSha` undefined is allowed (it is refused only when the file exists and the bytes differ). An existing page with `r.base_sha256` is a compare-and-swap with a verified backup. The pages are not hub pages (imageGate HUB_PAGE = articles|guides|insights|blog), so the image gate skips them. The CTA gate runs, but the pages already carry the tracker (the hand edit passed it). liveGuard only refuses `unknown` or frozen sites, so the `publisher` flag changes nothing for a .jpg.
- handler.bridgeTool always returns `{ ok: true, ...result }`. So "no ok key on purpose" makes no difference: the Controller always receives ok:true and stores `complete`. This is harmless.
- base64: the Lighthouse final-screenshot is roughly 50 to 200 KB. `atob` plus `Uint8Array.from` handles that size without trouble. The regex has no newline issue.
- addClientCard on the real EN, MS and ZH layouts: block, chips, badge, lead, KPIs and ItemList all match. A layout that is not recognised throws before any write, and launches.json is only touched when all 3 pages are fine. A re-run after a partial failure finishes the remaining pages.

## Findings (most important first)

### 1. goLiveClients.ts L51 + Controller edits: `industry: c.niche` is free text, not an industry id. A non-automotive client gets labelled "Car workshop" on a public page
Live Client rows show niche values like "Car workshop (auto repair shop)" and "Hybrid & EV car repair and hybrid battery specialist", and most are null. `pickIndustry(given)` only matches an id or an exact English name, so it falls through to the home <title>/<h1> rules every time. If nothing matches, it defaults to `car-workshops`. Some AutoSEO clients are not workshops: `advance-machinery-movers`, `studio-87`, `sp-precision-parts`. When one of them goes live, it is published as "Car workshop, <town>" in 3 languages and in the launches popup.
Fix: run the keyword rules on `given` (niche) text before the title. When `ind.from === 'default'`, do not publish: return `{ skipped: true, detail: 'industry unknown, send industry=<id>' }`, or publish only when body.industry is an exact id.

### 2. goLiveClients.ts L17-37 (captureHome): retry on 429 is useless, and the time budget is tight
Without PAGESPEED_API_KEY, the keyless quota is "Queries per day". scratchpad psi.json from tonight shows exactly that 429 RESOURCE_EXHAUSTED, so the immediate second call fails the same way. A 45 s timeout also gets a second 45 s try. Worst case for the op: home 10 s + 2 probes + PSI 90 s + og 10 s + jpg write + 3 page read/backup/write/verify + launches write. That is about 140 to 170 s, close to the Controller's 170 s AbortSignal, and the Bridge function may have its own wall limit. If the request is cut, the Controller stores an error, and the Bridge may stop after EN is written but before MS/ZH. Nothing retries it automatically (see 4).
Fix: make one attempt only. Do not retry on 4xx/429, and retry on 5xx only if elapsed < 30 s. Add `&fields=lighthouseResult/audits/final-screenshot/details/data`, which shrinks the multi-MB JSON. Add an overall deadline in clientsCardOp (for example, do not start the og fetch after 70 s). Confirm that PAGESPEED_API_KEY is set on the Bridge, otherwise the share-image fallback becomes the normal path.

### 3. goLiveClients.ts L46-47, L68-69: uncaught fetch errors abort the whole op
- L46: a TLS error or timeout on the home fetch throws, instead of returning `skipped`.
- L68: the og:image fetch is outside any try. A timeout there throws after up to 90 s of PSI.
- Also L61: if probeLive returns `unknown` (a cPanel listing error), the code treats the file as missing and goes on to capture. Then writeFile (L75) is refused by liveGuard (`unknown`) and the op throws.
The Controller catches all of these, so the go-live result is not changed. But the op fails noisily instead of reporting cleanly.
Fix: wrap L46 and L68-70 in try/catch and turn errors into `skipped`/fallback. For L61, return skipped when `state === 'unknown'`.

### 4. Controller edits: a skipped or failed clients_card is never retried, and concurrent go-lives collide
`pages[l] = 'FAILED'` covers several cases. A STALE write from two clients going live in the same minute, a 429, or a skipped result from "domain not 200 yet" right after the flip are all stored in golive_status.clients_card, and nothing runs the op again. The /clients/ card then silently never appears.
Fix: in clientsCardOp, on a 409 "STALE WRITE" for a page, re-read and re-apply once. In the Controller, re-run clients_card from check/check_all while `golive && clients_card.complete !== true` and the last attempt was more than 1 h ago. The op is idempotent, so this is safe.

### 5. goLiveClientsPure.ts L143 (addLaunch): slug-prefix idempotency gives a false "already there"
`String(x.id).startsWith(c.slug + '-')`: slug `rasa` matches id `rasa-sayang-2026-11-20`. I reproduced this: with an `overseas-tyre-...` entry present, a new site with slug `overseas` returns null, and launches is never added.
Fix: `new RegExp('^' + reEsc(c.slug) + '-\\d{4}-\\d{2}-\\d{2}$').test(x.id)`.

### 6. goLiveClientsPure.ts L119-120: `navEnd` is not checked
If `</nav>` is missing after the industry-nav, `indexOf` returns -1 and `out.slice(0, -1)` splices the chip in before the last character of the document. That writes a broken page.
Fix: `need(navEnd > navStart, 'the end of the industry chips')`. In the same spirit, bound `cardsAt` (L99) and the badge search (L102) to before the next `<div class="industry-block`. Otherwise a block with a different cards class or no badge silently edits the next block. The chip bump at L106 is silent when there is no match: use `need`.

### 7. White-label: L46-48 only proves the domain answers 200, not that this slug's switch is On
The op does not tie `domain` to `slug`. Any 200 domain the caller passes is named, and a re-run after a switch Off still names the site if the domain keeps answering 200.
Fix (cheap): read `join(e.base,'index.html')` with readLiveFile and require its `<link rel="canonical">` to start with `https://<domain>/`. That is exactly what the flip writes when On. Also reject `PREVIEW_HOST_RE` domains (autoseo.my / pageonesingapore.com) as goLiveOp does.

### 8. Minor (public text, not blocking)
- Pure L72: the zh default line puts the English town in front of Chinese: "Skudai, Johor Bahru汽车维修厂". Use `${s.zh}（${town}）`, or have the Controller send line.zh.
- Pure L146: `s.en.toLowerCase()` gives "ev and hybrid specialist" in the popup trade. Lowercase only the first letter.
- Pure L42: "(M)" is never stripped, because `\b` before "(" fails. "Enterprise" is stripped, which may be intended.
- Pure L91: idempotency only matches `href="https://<apex>/"`. A hand-made card with www or without the trailing slash gets a duplicate.
- goLiveClients L75: `publisher: true` is documented as "only the hourly Page One publisher". It has no effect on a .jpg, so drop it to keep the flag's meaning.
- REVIEW.md says "Bridge auto-sitemap bumps lastmod". writeFile does not do that: only the tool wrappers call autoSitemapAfter. The /clients/ lastmod is not bumped (call autoSitemapAfter or drop the claim).
- launches.json is rewritten with JSON.stringify(…, 2), so the one-line `trade`/`line` objects get expanded. The JSON stays valid; this is cosmetic only.

## Verdict
No signature, import or cycle problems, and the page edit is right for today's layouts. Before saving, fix 1 (wrong public industry label for non-workshop clients), 3 (exceptions) and 5 (false idempotency), and add the navEnd check from 6. 2, 4 and 7 are reliability and white-label hardening and are strongly recommended.

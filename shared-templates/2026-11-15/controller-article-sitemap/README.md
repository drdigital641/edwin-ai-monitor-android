# Controller: sitemap, llms.txt, cards and IndexNow for each new client article (DRAFT, not saved)

Working copy: /tmp/qul5nf-ctl in the Base44 sandbox (from Controller HEAD 21ffaabc7759effbd15c2f010bd94b6cf3298ce6). Nothing was saved to the Controller, no test touched /app, no website was written, no IndexNow was sent.

**What changes**
After the Client Article Writer publishes a client article, one shared helper now: adds the articles index and the article to `sitemap.xml` (new `<url><loc><lastmod>` lines only; existing entries untouched and in order); rebuilds `sitemap.txt` from the locs; adds ONE line for the article to `llms.txt` at the end of its Articles section, only if the URL is missing; adds one card to `article-cards.json` only if the site has one (same keys, none dropped); sends IndexNow for the article URL and /articles/ only, with that client's `indexnow_key`, only when the site is live. Each step reports its own result in the run output (`follow_up`). One failed step never blocks the others.
It also fixes a real gap: today the guard refuses to replace `sitemap.xml`, so the run stops after the article page and IndexNow never goes out (see FINDINGS.md, problem 1). `publishLive` no longer regenerates sitemap.xml, llms.txt or robots.txt for a new article; the helper adds to them instead.

**Files**
- NEW `base44/shared/articleSeo.ts`: the helper, plus verbatim copies of the Bridge's `xmlProblem`, `generatedFileProblem`, `articleCardsProblem` (no script/iframe/object/embed element, no on* attribute, no javascript:, urlset/sitemapindex root, at least one loc).
- `base44/shared/liveGuard.ts`: a `FOLLOWUP_PATH` allowlist and an optional `generatedOk` argument (+10 lines, one `return null`).
- `base44/shared/bluehostFiles.ts`: `safeWrite(..., opts)`; with `{ articleFollowUp: true }` it sets `generatedOk` only after `articleFollowUpProblem()` passes.
- `base44/functions/clientSites/entry.ts`: `write_articles` calls the helper after `publishLive(..., incremental)`.
- NEW `tests/articleSeo.test.ts`: 12 tests with fakes.

**Guard rule (the narrow override)**
Only a write carrying `articleFollowUp: true` may REPLACE `preview/<client-slug>/sitemap.xml`, `sitemap.txt`, `llms.txt` or `article-cards.json`, and only if the new bytes pass the content checks against the live bytes: well-formed urlset, no active content, no live URL/line/card dropped or reordered, at most 2 new sitemap URLs, 2 new llms lines, 1 new card, 20 new sitemap.txt lines. All other guard checks still run first (unknown live state, never-write list, path rules, byte-exact backup and readback) and HOLD flags are applied before the guard. robots.txt, HTML and every other file are unchanged. Like the Bridge's override, this is live the moment it is saved: needs security review and Edwin's written yes first.

**Not covered**
- generateArticle (Page One): handled entirely by the Bridge hourly publisher, which already does all three. Bridge-published sites for any other client are for the Bridge thread's auto-sitemap step.
- Ethel and AutoSEO: no Controller site write; their publisher sits outside the Controller.
- Custom (hand-built) sites are excluded from `write_articles`.
- If a client site has no `sitemap.xml`, `sitemap.txt` or `llms.txt` yet, the helper skips it (never creates); the full build still creates them.
- A sitemapindex file is left alone.

**Risks**
- Saving changes `clientSites`, `bluehostFiles` and `liveGuard`, which several other functions share (bluehostUpload, bluehostRestore). `safeWrite` default behaviour is unchanged; the new argument is optional.
- New articles are inserted at the end of the llms Articles section, new cards at the front (newest first): check the order Edwin wants.
- `renderLive` still rewrites index/about/contact HTML on each article (unchanged behaviour); a guard refusal there still stops the run before the follow-up.
- Type checking: the repo has about 140 existing implicit-any errors under `deno check`; the new module and tests are clean and run under `deno test`.

**Counts** (HEAD 21ffaab, tests/ and base44/tests/, via an import map pointing npm:@base44/sdk@0.8.44 at the installed 0.8.61)
Before: 122 passed, 0 failed. After: 134 passed, 0 failed (12 new). The 97/0 figure from earlier is out of date: HEAD has more tests now.

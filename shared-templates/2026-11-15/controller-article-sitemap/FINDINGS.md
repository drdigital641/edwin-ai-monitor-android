# Controller article writers: how a new article reaches a live site (15 Nov 2026)

Controller app 6ac7f2548a9c3877449e2772, code at HEAD 21ffaabc7759effbd15c2f010bd94b6cf3298ce6 (read only; nothing saved live).
Bridge app 6ac6d47b4ec84148578914c7 read only (shared/pageoneArticles.ts, shared/liveGuard.ts).

## Step 1 table

| Writer (workflow -> function) | What it writes | How it reaches the live site | sitemap.xml | sitemap.txt | llms.txt | article cards | IndexNow |
|---|---|---|---|---|---|---|---|
| Daily Article Writer -> generateArticle (Page One Singapore, pageonesingapore.com) | `Article` entity only (status published) | Bridge hourly publisher. The Controller serves them through `articleFeed`; the Bridge builds the pages. Not FTP, not GitHub. | Yes, rebuilt every run by the Bridge (`sitemapXml`) | Yes (`sitemapTxt`) | Yes (`llmsTxt`) | The site has no JSON card list: the Bridge rebuilds `articles/index.html` (`indexPage`) | Yes, changed URLs only, the Page One key (INDEXNOW_KEY in pageoneArticles.ts) |
| Client Article Writer -> clientSites `write_articles` (Controller-generated client sites: custom=false, status activating/live) | `ClientArticle` entity, then the pages themselves | DIRECT FTP from the Controller: `publishLive` -> `put` -> `safeWrite` (bluehostFiles.ts) into `preview/<slug>/`, with live guard v2 and HOLD flags | Rebuilt whole by `renderLive`, but see problem 1 | Never written | Rebuilt whole by `renderLive`, but see problem 1 | No JSON file; `articles/index.html` is regenerated from all `ClientArticle` rows (no card is dropped as long as the rows exist) | Sent for the article URL + /articles/ with `Client.indexnow_key`, only if `live_at` is set and only if every earlier write succeeded |
| Ethel Article Writer -> ethelArticle | `EthelArticle` entity (status ready) | Neither the Controller nor the Bridge publishes it (no code in either app reads EthelArticle). The comment says "the site publisher"; that lives outside both apps. | not here | not here | not here | not here | not here |
| AutoSEO night run -> autoseoArticles `built` | Only records `article_last_*` fields on the Client | No site write. The run builds a zip; Edwin uploads it (Carzy World, EMATS, AP Car). Read only towards the websites. | n/a | n/a | n/a | n/a | n/a |

Hand-built (custom) sites are excluded from `write_articles` (`!c.custom`), and other writes to client folders (goLiveCustom, Activate) are not article writers.

## Problems found in the one direct writer (clientSites write_articles)

1. **Live guard v2 refuses the sitemap and llms.txt replace.** `renderLive` regenerates `robots.txt`, `sitemap.xml`, `llms.txt` and the key file on every article. In `liveGuard()` any replace of a non-HTML, non-asset file is refused ("replacing this file type needs an override") and `GUARD_OVERRIDES` is empty. A byte-identical robots.txt passes ("no change"), but a changed `sitemap.xml` throws. `publishLive` has no per-file catch, so the run stops there: the article page and `articles/index.html` are already live, but the sitemap and llms.txt are not updated, the key file is not written and IndexNow is never sent (the `catch` records an error only). If the guard is live as it appears in HEAD, new client articles are published without sitemap or IndexNow.
2. `sitemap.txt` is never produced for client sites.
3. There is no `article-cards.json` for these sites (the card list is HTML), so nothing to add; the helper handles a card file if one exists.
4. The workflow description promises "sitemap and llms.txt, and tells Bing (IndexNow)", so the code and the promise disagree.

## Controller live guard (controller-guard-v2) rules that matter

- Every write goes `safeWrite` -> `writePolicy` (HOLD flags in `SITE_HOLDS`, all `on:false` today; Page One root managed files and `articles/` are read-only for the Controller) -> `liveGuard`.
- delete/move/rename always refused; `.htaccess`, `.user.ini`, `php.ini` and code extensions never written, even as new files.
- New file (server listing says absent): allowed. Identical bytes: allowed.
- Replace of HTML only if title, meta description, H1, JSON-LD values, FAQ questions and the Google review footer are kept and the source is not older than live. Replace of css/js/images/fonts allowed.
- Replace of `robots.txt`, `sitemap*.xml`, `llms*.txt`, `*.json`, `*.txt`, `*.xml`, anything else: REFUSED unless a `GUARD_OVERRIDES` entry (exact site, path, sha256 of the new bytes, Edwin + security review) matches. There is no generated-file override in the Controller (the Bridge has one, `GENERATED_OVERRIDE`, for its hourly publisher only).
- The Bridge's `xmlProblem`, `generatedFileProblem` and `articleCardsProblem` do not exist in the Controller's copy of liveGuard.ts (151 lines vs the Bridge's longer file).

## What the diff does

Only the Client Article Writer path needs code. generateArticle already gets all of it from the Bridge, so nothing is duplicated there. The Bridge thread's auto-sitemap step for every Bridge publish covers any Bridge-published article; this diff does not touch it. Ethel and AutoSEO write no site from the Controller, so there is nothing to attach to (see README for what is not covered).

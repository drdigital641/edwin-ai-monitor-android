# SgGarage Controller: content-check for non-HTML overwrites (DRAFT, NOT SAVED)

For Edwin. Base44 app "SgGarage Controller" (6a9404b277a56a67dfd98681), on top of saved Option C (git b2a568f).
Nothing here is saved, published or run against sggarage.com. /app was not touched; all work and tests were in /tmp copies.
Base44 functions go live when /app is saved, so this waits for the security reviewer and your "save".

## What it does
Inside the SG Garage docroot only, whatever the HOLD flag says (no bypass flag), the Controller now refuses a bad overwrite
of these files. The check runs inside safeWriteRemoteText, after the sha check, before the backup and before any byte is sent.
If the live file cannot be read, the write fails (fail closed). A refusal is 403 with `content_check: true`, a
ConnectionAudit row `content-check-refused`, and is never retried.

1. robots.txt (first). Refused if the new file:
   - is empty, over 64 KB, contains `<`, a NUL or another control character;
   - has a line that is not blank, a `#` comment, or one of User-agent, Allow, Disallow, Sitemap, Crawl-delay, Host (any case) with a value;
   - adds a Disallow that the live file does not already have, for `*`, Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, GPTBot, PerplexityBot, ClaudeBot or Applebot, that covers `/`, `/articles/` or `/index.html` (prefix, `*` and `$` rules understood, so `/`, `/*`, `/a`, `/*.html$` are all caught);
   - drops a `Sitemap:` line the live file has, or adds a Sitemap that is not https on sggarage.com or www.sggarage.com.
   Fine: adding Allow lines, comments, Disallow for /zc_admin/ /cache/ and similar, blocking other bots.
2. sitemap.xml: the Bridge's xmlProblem (well-formed, urlset/sitemapindex root, no script/iframe/object/embed, no on* attribute, no javascript:, no DOCTYPE), at least one `<loc>`, and every live `<loc>` still present.
3. sitemap.txt: at least 1 line, every line an https URL on sggarage.com or www.sggarage.com, every live line kept.
4. llms.txt: not empty, no `<script`, no NUL, every non-empty live line kept.
5. article-cards.json: the Bridge's articleCardsProblem (strict card shape, no javascript:, never drop a live card).
6. Any other `*.json`: must parse as JSON.
A new file with no live copy gets the same checks without the "keep live" parts.

## Not covered
CSS, JS, images, and every other file type. Raw `uploadFrom` on the guarded client is not content-checked for non-HTML (nothing in this app calls it except safeWriteRemoteText and its own rollback, which restores the original bytes). `robots.txt`, sitemap and llms.txt in other folders of the SG Garage zone are matched by file name. The date/age rule of the HTML check is not applied to these files.

## Files changed
- NEW base44/shared/nonHtmlGuard.ts (ContentCheckError, robots/sitemap/llms/json checks, Bridge copy)
- base44/shared/ftpFileOps.ts (calls the check; CONTROLLER_VERSION now `sggarage-ftp-2026-11-15.hold-neverwrite-sidedoor-nonhtml`)
- base44/shared/ftpClient.ts (a content-check refusal is final, never retried)
- base44/functions/ftpWriteFile, ftpHealthCheck, websiteCommandWorker entry.ts (403 + `content_check` + audit row)
- NEW tests/sggNonHtmlCheck.test.ts; tests/neverWrite.test.ts and tests/sggSideDoor.test.ts adjusted: they wrote placeholder text to robots.txt/sitemap.xml/data.json inside SG Garage, which is now correctly refused.

## Bridge copy (read-only source, byte for byte)
Bridge app 6ac6d47b4ec84148578914c7, base44/shared/liveGuard.ts at git 5012f3e (the Bridge HEAD read; it already holds the tools delta).
- Whole file MD5: dfbaec0a46dd030c71bde8c0464226e0
- Copied block (lines 155-243: articleCardsProblem, XML_ACTIVE_ELEMENTS, decodeRefs, xmlProblem) MD5: 65f48ac0d48bc6f539819a8b789838cd (verified identical in the Controller file)
- Saved Controller liveGuard.ts (htmlProblems, from Bridge 33343ea) MD5 b41399f37b38dae6d5f044d30d0df453, unchanged.
- New nonHtmlGuard.ts MD5 85c7d5e50e9facbc2c9a21f1971846c5; tests/sggNonHtmlCheck.test.ts MD5 4082eade1eb08ec5f548dde7b091ffcf.
The Bridge may change its guard later; this copy then needs the same update.

## Test counts (fake FTP, no network)
- Baseline b2a568f: 18 passed, 0 failed (HOLD flag OFF as saved, and ON in a test copy).
- Working copy: HOLD OFF 27 passed, 0 failed; HOLD ON (test copy only) 27 passed, 0 failed (18 old + 9 new).
- New tests cover about 70 refusal cases (server bytes and write-op count unchanged after each), good edits, new files, fail-closed on unreadable live file, Cleanic robots.txt `Disallow: /` still passing, 403 shape + audit rows, no retry.

## Risks and choices to check
- Over-strictness: a live robots.txt with an unusual line is read leniently, but the NEW file must be fully clean, so an edit that keeps a vendor-specific directive (e.g. `Noindex:`) is refused.
- `Disallow:` with an empty value is allowed (standard "allow all"); your rule said "with a value", say if you want it refused.
- Any existing live Disallow that already covers `/articles/` is kept as is; only NEW ones are refused.
- While the HOLD is ON, a bad file gets the 403 content-check message instead of the 423 hold message; good writes still get 423.
- "Keep live" rules mean a deliberate removal of a sitemap URL or llms.txt line must go through the Bridge.
- Diff file headers have no timestamps; it was built from the /tmp copies (diff -ruN, deno.lock excluded).

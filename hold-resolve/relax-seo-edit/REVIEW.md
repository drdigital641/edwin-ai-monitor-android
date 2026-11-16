# Relax Bridge live guard for approved SEO edits: SPO review request (16 Nov 2026)

Edwin's instruction (16 Nov 2026, 2:10pm SGT): "Let Claude's approved jobs edit titles, meta, H1 and content without
asking me, keep auto-backups." Deletions, .htaccess, credential/config/secret files, DNS/hosting changes and frozen-site
rules stay blocked exactly as before. No broader edit types, no existing override removed, no client site changed.

Base: Bluehost Bridge sandbox main git 5bae2e2 (includes the unpublished MyKar fb-posts, SG Car Workshop directory and
GUARD_OVERRIDES changes of checkpoints 6afa9e88, 6afa93c8, 6afa9a6a). NOT saved in Base44 until this review passes.

## Revision 2 (after SPO review 1 FAIL / PASS WITH CHANGES)
- HIGH fixed: articles-only sites. `SEO_EDIT_ARTICLES_ONLY` = cleanic, contiexpert (future own key) and pageone
  preview/contiexpert/. On those the relaxation applies only under articles/; every other page keeps the old refusal.
  Note: Cleanic's existing posts at the site root (e.g. car-steam-cleaning-singapore-2/) are therefore still refused,
  as before; new article files are unaffected (new files were always allowed).
- Title/H1/meta counts ignore comments and script/style/template/noscript/textarea blocks; closing tags allow spaces.
- Number of meta description tags must equal live (or go 0 -> 1); the 1-400 limit applies whenever the new page has one.
- New title / meta text may not contain < or > (entity-encoded too); a new H1 may not contain script, iframe, on*= or javascript:.
- Comment states that the seoEdit scope is ANY signed-in Base44 admin of the Bridge with no key, Edwin's login included,
  and that restore_backup can put back an older title/H1/meta (intended rollback; the older-date check still applies).
- One test per relaxed refusal message (htmlProblems wording must match SEO_EDIT_RELAXED).
- guardOverrides1115 test made green by recognising the 16 Nov one-time Maison and Urban Eco entries (test file only).
  NO override entry was added or removed (Edwin's brief: do not remove existing overrides; other threads' pending
  Publishes use that list). Removing stale one-time entries is offered as a separate job.
- Diff now includes the tests (tests/seoEditRelax.test.ts, tests/guardOverrides1115.test.ts).

## What changes (relax-seo-edit.diff)
- `liveGuard.ts`: new APPROVED SEO EDIT RULE. When `seoEdit` is true (and not the publisher), for an HTML page outside
  `preview/sgcarworkshop/`, the three refusals "title would change", "meta description would change" and "H1 would change"
  are dropped. Sanity checks are added instead: same number of `<title>` and `<h1>` elements as live, title 1-200 chars,
  H1 1-250 chars, meta description not removed and 1-400 chars when live has one. Kill switch `SEO_EDIT_ON`.
- `seoEdit` is set ONLY by the write_file, edit_file, write_files and restore_backup tool entries, and only when
  `ctx.agent === 'claude' && !ctx.viaKey` (Claude's signed-in Bridge session). ChatGPT key, site keys, drop keys never.
- sync_from_github (runBulk without seoEdit), drop_publish, the hourly publisher, auto-sitemap and hero-image writes never pass it.

## Retained safeguards (unchanged code paths)
- BRIDGE HOLD (frozen sites) checked first in writeFile for every route.
- writeBlockedReason / secret-name checks (.htaccess, PHP/CGI/shell, .env, wp-config, keys) before the guard.
- Never-write list in liveGuard (.htaccess, .htpasswd, .user.ini, php.ini, PHP/CGI/pl/py/sh) for new and replaced files.
- Deletes (only sitemap.txt with exact sha), moves and renames: blocked.
- Unknown live state, path rules (.., absolute, URL, backslash, control chars): refused.
- HTML: older-than-live date, JSON-LD loss/change, FAQ question loss, review-footer removal: still refused.
- Non-HTML replacements (robots.txt, sitemap, llms.txt, json, txt, xml, pdf, manifest...) still need an override.
- MyKar fb-posts.json rule, SG Car Workshop directory rule, generated-file overrides: unchanged.
- GUARD_OVERRIDES: untouched (no entry added or removed).
- Base sha256 compare-and-swap, verified private backup before every replace, byte-exact readback + auto-restore: unchanged.
- Rollback: restore_backup (one step), itself backed up first.

## Tests
`tests/seoEditRelax.test.ts`: 10 tests, all pass (output in test-output.txt). Full Bridge suite in a /tmp copy of 5bae2e2
+ this diff: 168 passed, 0 failed, 1 ignored.

## Questions for SPO
1. Is "Claude's signed-in session" (agent claude, no API key) the right scope for "Claude's approved jobs"?
2. Is excluding sync_from_github / drop_publish right (sync is the stale-source route the guard was built for)?
3. Any bypass of the retained checks via the new path?

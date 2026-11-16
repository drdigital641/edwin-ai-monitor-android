# Relax Bridge live guard for approved SEO edits: SPO review request (16 Nov 2026)

Edwin's instruction (16 Nov 2026, 2:15pm SGT): "Let Claude's approved jobs edit titles, meta, H1 and content without
asking me, keep auto-backups." Deletions, .htaccess, credential/config/secret files, DNS/hosting changes and frozen-site
rules stay blocked exactly as before. No broader edit types, no existing override removed, no client site changed.

Base: Bluehost Bridge sandbox main git 5bae2e2 (includes the unpublished MyKar fb-posts, SG Car Workshop directory and
GUARD_OVERRIDES changes of checkpoints 6afa9e88, 6afa93c8, 6afa9a6a). NOT saved in Base44 until this review passes.

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
`seoEditRelax.test.ts`: 8 tests, all pass (output in test-output.txt). Full Bridge suite in a /tmp copy: 165 passed,
1 failed: guardOverrides1115 "unexpected extra override entry", which fails identically on the untouched base 5bae2e2
(pre-existing, caused by other threads' new GUARD_OVERRIDES entries; not touched here).

## Questions for SPO
1. Is "Claude's signed-in session" (agent claude, no API key) the right scope for "Claude's approved jobs"?
2. Is excluding sync_from_github / drop_publish right (sync is the stale-source route the guard was built for)?
3. Any bypass of the retained checks via the new path?

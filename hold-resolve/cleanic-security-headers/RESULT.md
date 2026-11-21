# Result (22 Nov 2026)

SPO review: PASS with one must-fix (no backslash in BEGIN/comment lines, which Apache joins as line continuation; no control characters in values). Applied. Re-review PASS after adding the exact-constant TASKLET_DENY stanza (cleanup brief item 6: deny /tasklet-api.php and /tasklet_publish.php).

Tests: tests/frozenHeaders.test.ts 11/11, full Bridge suite 110 passed, 0 failed.

Saved: Bridge git cc1ec9f, checkpoint 6b022f538922522b5c5bd6e7 (Edwin: Publish only, never Activate).

Final liveGuard.ts additions:

```ts
const SEC_BLOCK = /^# BEGIN Page One security headers v\d+[^\n\\]*\n(?:#[^\n\\]*\n)*<IfModule mod_headers\.c>\n((?:[^\n]*\n)+?)<\/IfModule>\n# END Page One security headers v\d+\n\n?/;
const SEC_HEADER_LINE = /^Header always set (Strict-Transport-Security|X-Content-Type-Options|X-Frame-Options|Referrer-Policy|Permissions-Policy|Content-Security-Policy|Content-Security-Policy-Report-Only) "[^"\\%\x00-\x1f\x7f]*"$/;
export const TASKLET_DENY = '# BEGIN Page One deny old tasklet files (22 Nov 2026)\n<FilesMatch "^(tasklet-api|tasklet_publish)\\.php$">\nRequire all denied\n</FilesMatch>\n# END Page One deny old tasklet files\n\n';
// stripSecurityBlock: remove a valid header block at the top, then an exact TASKLET_DENY prefix (startsWith); live and new remainders must be identical.
// liveGuard: if (frozen && args.htaccess === true && rel === '.htaccess' && live.state === 'present' && frozenHeadersOnlyChange(live.bytes, newBytes)) return null;
```

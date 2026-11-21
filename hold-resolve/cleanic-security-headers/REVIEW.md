# Cleanic security headers: frozen-site guard exception (review before save)

Job: thread "Add security headers to 11 sites", Edwin's batch brief 22 Nov 2026 7:38am SGT ("On Cleanic, change only the headers, nothing else in WP").

The Bridge htaccess tool refused cleanic:.htaccess (frozen site, articles only). This diff adds a narrow exception in base44/shared/liveGuard.ts: inside a frozen site, only via the safe .htaccess tool, only for the root .htaccess, the write is allowed when the only difference is the 'Page One security headers' block at the very top, and that block holds only `Header always set <7 named security headers> "value"` lines (no %, backslash, env=, other directives). Add / update / remove allowed (remove keeps auto-restore working). Everything else on frozen sites stays refused.

Tests: new tests/frozenHeaders.test.ts 9/9; full Bridge suite 108 passed, 0 failed. Diff: cleanic-headers.diff.

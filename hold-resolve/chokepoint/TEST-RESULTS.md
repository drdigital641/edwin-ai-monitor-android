# Test results (14 Nov 2026, Bridge sandbox copy /tmp/g4/v3, deno test --no-check, fetch mocked, no network)

## New: tests/cpanelChokepoint.test.ts  -> ok | 2 passed | 0 failed
- refused: upload_files into site root (no grant), .htaccess upload, upload after grant ended, grant for a different file,
  save_file_content, fileop copy into site, fileop move / rename / unlink / trash / extract / link / killdir,
  chmod on a site file, fileop without doubledecode=0, copy dest with "..", "%2e%2e", "%2f", upload dir with "..",
  two destinations in one copy, mkdir name with ".."  (each: no request reached cPanel)
- allowed: upload into ~/bluehost-bridge-private (selftest), upload into site WITH writeFile grant, copy into private
  backups, compress into ~/backups-private, chmod on a private backup, mkdir inside a site
- percent paths refused by normalizeRel AND by writeFile before any cPanel call: %2e%2e/index.html, %2E%2E/%2E%2E/etc/passwd,
  articles/%2e%2e/%2e%2e/x.html, ..%2findex.html, %2e%2e%2f%2e%2e%2fx, a%2fb.html, %252e%252e/x.html, %c0%ae%c0%ae/x,
  a/%00.html, articles\..\x.html, ../x.html, a/../../x.html; "/etc/passwd" stays site-relative "etc/passwd".

## Existing mock tests on v3 (mocks given the server listing the live guard needs)
- bulkWriteMock: "bulk create, then overwrite rules, backups and per-file results" ok (every write went through the
  writeFile grant). "cannot reach into another site folder" FAILED with "BRIDGE HOLD is ON for SG Garage": same failure on
  the unchanged Bridge code (the test writes to sggarage while its HOLD is on).
- githubSyncMock: 4 ok. Same SG Garage HOLD failure as above. "sync ~40 files" FAILED because the live guard v2
  (already PASSED review) refuses the fixture's change of H1 "" -> "page 0" on an existing live page: the guard working as
  designed, not the choke point.

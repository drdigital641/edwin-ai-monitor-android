# Bridge drop folder (15 Nov 2026), NOT yet saved to the Bridge

Patch: `bridge-drop-folder-onto-c83fbe2.diff` (md5 56304967cead3abe3e115e98538f6554), made against Bridge f2ae522, applies cleanly on Bridge head c83fbe2 (that head only changed bridgeConfig.ts + guardOverrides1115.test.ts).

Apply: in a /tmp copy of /app: `patch -p1 < bridge-drop-folder-onto-c83fbe2.diff` (paths are pnew/...; use -p1).
Tests: `deno test --no-check -A --import-map tests/importmap.json tests/ base44/tests/` -> 104 passed / 0 failed on c83fbe2 (98 existing + 6 new in tests/dropFolder.test.ts). deno check clean on the changed files; vite build + eslint clean for Connect.jsx.

Files: shared/drops.ts (new), shared/handler.ts (drop scope + sessionOnly), shared/keys.ts (scope 'drop'), shared/bridgeOps.ts (putDropBytes/readDropBytes, private folder only),
functions bridgeDropPut, bridgeDropStatus (bot), bridgeDropList, bridgeDropRead, bridgeDropPublish, bridgeDropClear (Claude, session only),
entities BridgeDrop, BridgeDropFile (admin rls), BridgeKey enum + "drop", mcp/config.json (4 Claude tools), src/pages/Connect.jsx ("Bot drop folder" key option), tests.
No change to the cPanel choke point, liveGuard, HOLD flags, .htaccess or PHP handling. See BOT-DROP-GUIDE.md.

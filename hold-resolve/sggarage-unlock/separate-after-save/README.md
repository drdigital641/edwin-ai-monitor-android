# SG Garage: the two SEPARATE diffs left after "SG GARAGE UNLOCK SAVE 1114-2330" (NOT saved)

> **DROPPED** (Edwin 11:30pm SGT 14 Nov, "SG GARAGE OPTION C 1114-2335"): do not save these two diffs. The live guard and the never-write lock stay. Replaced by `../../sggarage-option-c/`.

3e01a2c81 (flags OFF only) was saved at 11:40pm SGT 14 Nov 2026:
- Bluehost Bridge git 33343ea (on e1d39cf), checkpoint 6af880138a6c7cf41e0e2566. Tests on saved code 45/0.
- SgGarage Controller git ac87bd6 (on 4f87f50), checkpoint 6af8803f403adb49f721da4b. Tests on saved code 14/0 (never-write still refuses: 1045 attempts / 61 names; 12 config/code names 403).

These are the v2 changes (../v2/, commit 9eb8cadd2) re-cut so they apply ON TOP OF the saved code. Each waits for SPO and Edwin.

| Diff | App, base | Touches | Tests of the resulting tree |
|---|---|---|---|
| `bridge-guard-off-sggarage.diff` | Bridge, on 33343ea | `liveGuard.ts` (NO_LIVE_GUARD_SITES = ['sggarage'] only), `tests/generatedOverride.test.ts`, new `tests/sggNoLiveGuard.test.ts`. bridgeConfig.ts (flags, file-type blocks) untouched; NEVER list unchanged for all sites. | 49/0 (`../v2/test-bridge-v2.txt`: same tree) |
| `sggarage-controller-never-write-removal.diff` | SgGarage Controller, on ac87bd6 | removes never-write (786127ad3 + 41c0fc4e8); siteHold.ts comment only; sggUnlocked.test.ts updated. App only serves sggarage. | flag off 10/0, flag on 10/0 (`../v2/test-controller-v2-flag-*.txt`: same tree) |

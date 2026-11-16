# Move 3 sites: Bridge diffs for after-the-fact review (Security & Privacy Officer)

Bluehost Bridge (Base44 app 6ac6d47b4ec84148578914c7). Edwin's brief, 15 Nov 2026 12:36am SGT: "Move K Tech, Benz World, Li Lian to Bridge".

## Status
Both steps are **already saved and Published**:
- Step 1, 15 Nov ~12:58am SGT.
- Step 2, 15 Nov ~1:20am SGT.

A review gate before the save was not in place then. These diffs are for review after the fact.

| Step | Bridge git | Checkpoint | Diff file | Tests |
|---|---|---|---|---|
| 1. Add ktech, benzworld, lilian with HOLD ON | 5252c21 (vs parent) | 6af8908597be4786e4a6ecbb | step1-5252c21-hold-on.diff | 67/0 |
| 2. HOLD off: ktech, then benzworld, then lilian | 5252c21..ddd665c | 6af894a168e459d4e5162f31 | step2-ddd665c-hold-off.diff | 67/0 |

## What step 1 does (5252c21)
- **New site keys.** `SITES` adds ktech = ktech.my, benzworld = benzworld.my and lilian = lilianproperties.com. Their document roots are looked up live from cPanel, like the other sites.
- **HOLD ON.** The 3 new `SITE_HOLDS` entries are `on: true` with `prefix: ''`, which blocks every write to those sites. The existing 7 flags are unchanged.
- **Own-folder rule.** This was added after a security review finding. `dropSharedRoots()` in loadRoots drops any of the 3 sites whose root equals or contains another site's root. Every call for that site then fails closed.
- **Generated-file override in liveGuard.ts.** Edwin's brief asked for "the same guard ... including the sitemap.xml/sitemap.txt/llms.txt override".
  - `MOVED_GENERATED_SITES` and `MOVED_GENERATED_PATH` let only these 3 sites replace exactly root sitemap.xml, sitemap.txt and llms.txt.
  - Those files still go through the `generatedFileProblem` content checks: no script or on* attributes, no javascript:, and not 0 URLs.
- **Other files.** The site enums and descriptions are updated in mcp/config.json, openapi.ts and Connect.jsx. Tests are in tests/move3Sites.test.ts. The tests/sggGeneratedOverride.test.ts flag filter now excludes the 3 new keys.

## What step 1 does NOT change
- **NEVER list.** `writeBlockedReason` and `readBlockedReason` are untouched: .htaccess, PHP, CGI, .sh and secret names stay blocked for every site.
- **Page One and SG Garage paths are unchanged:**
  - `GENERATED_OVERRIDE_SITES` = ["pageone"]
  - the `GENERATED_OVERRIDE_PATH` regex
  - the SG Garage override
  - the publisher pins
  - the Page One prefix and SG Garage flags
  The tests assert each of these.
- **liveGuard.ts is not fully untouched.** Its only change is the narrow 3-file override above, with all existing rules kept.
- **No writes.** No write reached any of the 3 sites while HOLD was ON. The only operations were dry-run compares: K Tech 105 same, Benz World 189 same, Li Lian 267 same, with 0 updates and 0 creates.

## What step 2 does (ddd665c)
- **Flags.** It changes only the 3 `on: true` flags to `on: false`, plus the test that asserts them.
- **When.** It was saved after the dry-run compares above showed 0 differences.
- **Saves.** It went in as three separate saves: ktech, then benzworld, then lilian.

## Later Bridge changes in the same job (for completeness)
- **0b08c1b, cp 6af906277.** Live-edit tools read_live_file and list_live_files, and compare-and-swap with a base sha256 on every write. Saved and Published 15 Nov.
- **04a4a4c, cp 6af90819.** Carzy World HOLD off, after a 107/107 compare.
- **f78fcb6, cp 6af90a0b.** 7 more sites added HOLD ON: hybridworld, autoseo, ecumats, apcar, jayven, urbaneco and snapsg.
- **16de882, cp 6af90d23.** HOLD off for those 7, after 0-difference compares.

All of these are already Published. Diffs can be added here on request.

## Gate from now on (Edwin, 16 Nov 2026)
- Any Bridge HOLD-off, or other backend change, is pushed as a diff to this folder and reviewed **before** it is saved in Base44.
- Base44 backend code goes live on save, so a review only before Publish is too late.

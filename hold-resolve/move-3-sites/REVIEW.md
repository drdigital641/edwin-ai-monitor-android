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

---

# SPO round 1 result (16 Nov 2026): PASS. Fixes below are NOT saved in Base44 and wait for review

## Live docroots (Bridge list_sites, read-only, 16 Nov 2026 9:20am SGT)

| Site key | Domain | Docroot | Nested in another site's folder? |
|---|---|---|---|
| ktech | ktech.my | public_html/ktech.my | no, own folder |
| benzworld | benzworld.my | public_html/benzworld.my | no, own folder |
| lilian | lilianproperties.com | public_html/lilianproperties.com | no, own folder |

- benzworld's folder also serves the cPanel sub-domain website-76a0b1a9.sgmodder.com. That domain is the same folder, not a different site.
- No Bridge site root is nested inside another one. The other 8 moved sites are also in their own `public_html/<domain>` folders, and snapsg is in `public_html/snapsg`.
- **Because none is nested, item 1 is hardening only.**

## fix1-spo-2026-11-16.diff: items 1 to 3

This was prepared in a /tmp copy of Bridge git 7563686, not in /app, so nothing is live.

1. **HIGH, hardening.** `dropSharedRoots` now also drops a key whose root sits **inside** another site's root (`mine.startsWith(r + '/')`). New test cases:
   - carbonfibre/ktech is dropped.
   - website_02a02bac/x/y is dropped.
   - The look-alike sibling carbonfibre-ktech is kept.
   - The existing "nested is kept" assertion is flipped to "dropped".
2. **LOW.** The move3Sites config test pins every moved key's HOLD flag `=== false`. This covers the 3 original keys and the 8 later ones.
3. **LOW.** New `MOVED_OVERRIDE_WRITERS = Object.freeze(['publisher','tools'])`.
   - The moved-sites generated-file override in liveGuard now checks it the same way the SG Garage override checks `SGG_OVERRIDE_WRITERS`.
   - A test asserts the value and that it is frozen.

**Tests on the patched copy:** 153 passed, 1 failed, 1 ignored. The unpatched copy gives 152 passed and the same 1 failure. That failure is `tests/guardOverrides1115.test.ts` ("unexpected extra override entry"), from another thread's one-time override fixture, and it has nothing to do with this change. This patch adds 1 test and breaks none.

## Later steps, already saved and Published, for review after the fact (item 4)

| Diff file | Bridge git range | What |
|---|---|---|
| step3-0b08c1b-live-edit-cas.diff | ddd665c..0b08c1b | **Most important.** read_live_file / list_live_files, compare-and-swap (base sha256) on write_file, edit_file, write_files and sync_from_github, and the account domain list in list_sites |
| step4-04a4a4c-carzy-hold-off.diff | 0b08c1b..04a4a4c | Carzy World HOLD off after a 107/107 compare |
| step5-f78fcb6-7-sites-hold-on.diff | 04a4a4c..f78fcb6 | 7 sites added HOLD ON: hybridworld, autoseo, ecumats, apcar, jayven, urbaneco, snapsg |
| step6-16de882-7-sites-hold-off.diff | f78fcb6..16de882 | HOLD off for those 7 after 0-difference compares |

The secret-like strings in step3 are the detection regexes, not real values.

## Save plan once SPO passes fix1
1. Apply fix1 in Base44 /app as one save.
2. Run the full suite on the saved code.
3. Create a checkpoint for Edwin to Publish.

MCP tool calls run the published code, so items 1 and 3 reach the live tools only after Publish.

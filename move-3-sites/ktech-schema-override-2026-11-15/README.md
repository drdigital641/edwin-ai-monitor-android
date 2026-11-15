# K Tech schema override (prepared, NOT saved to the Bridge)

51 HTML pages on ktech.my still carry the old JSON-LD (Andrew, Hooi, Masai). The LIVE GUARD refuses JSON-LD value changes
without a GUARD_OVERRIDES entry for the exact new bytes. Edwin approved the override on 15 Nov 2026 (decision card).

- plan.json: per file `expected_sha256` (= live now, matches the Bridge after-sha of the visible edit) + 4 edits + `new_sha256`.
- GUARD_OVERRIDES-entries.ts: 51 entries to paste into base44/shared/bridgeConfig.ts GUARD_OVERRIDES.
- Check: contact/index.html new_sha256 cea45275... equals the sha the guard itself printed when it refused the same bytes.

Order once the Bridge queue is clear: checkpoint, paste entries, save, apply the 51 edit_file calls (expected_sha256 = plan base),
then remove the entries, save, checkpoint. Edits change only the 4 JSON-LD strings; no visible text.

# Bridge NEEDS YOU list + Grok Bot notice (15 Nov 2026)

Edwin's ask (15 Nov 2026 10:33am SGT): a real-time "needs you" alert from the Bluehost Bridge to Grok Bot (Website Manager).
NOT saved in Base44 yet: only one Bridge code change may be in flight; save when the coordinator says the queue is clear.

## What it adds
- Entity `BridgeNeedsYou` (admin-only; hidden from the MCP entity tools): id, type publish|server, target (site/app), ref
  (checkpoint id or file/setting), summary, why, status open|done, opened_at/done_at, live_check, site_recheck, notice outcome.
- `bridgeNeedsYou` (MCP tool `needs_you`, signed-in admin or full key): add / done / resend.
  - add sends exactly ONE notice. Same open step (type+target+ref, case/spacing ignored) = duplicate, no notice.
    Two adds at the same moment: oldest row wins, the other is deleted before any notice.
  - done needs live_check + site_recheck; sends nothing. list sends nothing.
  - resend only for not_configured / rate_limited / failed (HTTP status); "unknown" (timeout) needs confirm_resend.
  - No automatic retries (routine fires have no idempotency key). Max 20 notices per hour.
- `bridgeNeedsList` (MCP tool `list_needs_you`, read only): open items or one by id. Grok Bot calls it over HTTP:
  POST https://blue-bridge-pilot.base44.app/functions/bridgeNeedsList, header X-Bridge-Key = a "needs" key, body {} or {"id": "..."}.
  A needs key can do nothing else. Make it on the Connect page: "Generate Grok Bot key (read needs-you list only)".
- Text is short plain text only: markup/PHP/.htaccess lines/code fences/many lines, credential patterns, long tokens and the
  webhook values themselves are refused.

## Notice
Secrets (Edwin adds in Base44): GROKBOT_WEBHOOK_URL, GROKBOT_WEBHOOK_KEY. Never logged, stored or returned; errors keep only the HTTP status.
- Routine URL (api.anthropic.com/v1/claude_code/routines/<trig_id>/fire, as the routine panel shows): headers
  Authorization: Bearer <key>, anthropic-version: 2023-06-01, anthropic-beta: experimental-cc-routine-2026-04-01;
  body {"text": "Bluehost Bridge NEEDS YOU notice (JSON): {...}"}.
- Any other https URL: body = the notice JSON, Authorization: Bearer <key>.
- Notice JSON: {event:"needs_you", source:"bluehost-bridge", id, type, target, ref, summary}.

## Files
New: base44/shared/needsYou.ts, base44/entities/BridgeNeedsYou.jsonc, base44/functions/bridgeNeedsYou/entry.ts,
base44/functions/bridgeNeedsList/entry.ts, tests/needsYou.test.ts, tests/stubs/runtime.ts (replaces the stub; test hooks only).
Changed by apply.py: base44/shared/handler.ts (needs key scope), base44/shared/keys.ts, src/pages/Connect.jsx, base44/mcp/config.json (+ mcp-tools.json).

## Save steps (when the queue is clear)
1. Copy /app to /tmp/nyb-<date> in the Bridge sandbox, curl these files in at the commit, `python3 apply.py mcp-tools.json`.
2. deno test (tests/), deno check entries, eslint Connect.jsx, vite build, in the /tmp copy.
3. Copy the same files into /app (auto-commit), create_checkpoint, give Edwin the checkpoint to Publish.

Self-test 15 Nov 2026 (head 6c1e80b/c83fbe2 copy): needsYou 9/9; full suite 76/1, the 1 is the pre-existing
guardOverrides1115 "exactly 2 entries" check (fixed at head c83fbe2); deno check OK; eslint clean; vite build OK.

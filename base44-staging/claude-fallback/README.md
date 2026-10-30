# Claude API fallback for Base44 (staged 30 Oct 2026)

Edwin added a Claude API key as the Base44 secret `pageone-api-key` (Controller app 6ac7f2548a9c3877449e2772).
Goal: when Base44 refuses an LLM call for credit limits, the run carries on with Claude and Edwin is told afterwards.

**Not applied yet.** Base44 pauses every code edit (sandbox 402) while the workspace is out of integration credits,
so this file waits here until Edwin tops up. The key is never in this repo (repo is public).

## Apply steps (when credits are back)
1. Copy `claudeFallback.ts` to `base44/shared/claudeFallback.ts` in the Controller.
2. In `base44/shared/llmFallback.ts` `invokeLLM(Core, params, source)`, on a credit-limit error (current test:
   credit-limit text or HTTP 402) try in this order:
   1. `claudeInvokeLLM(params)` then `logFallback(base44, source, true)`; return its result.
   2. on Claude error: `logFallback(base44, source, false, err)`, then the existing llmGateway (OpenAI) call.
   Claude handles `add_context_from_internet` via its web search tool, so those calls may now fall back too
   (the OpenAI gateway still must not take them). `file_urls` calls still do not fall back.
3. Create entity `ClaudeFallbackLog` (source, model, input_tokens, output_tokens, ok, error, run_date), admin-only rls.
4. Checkpoint, then Edwin taps **Publish** on the Controller.
5. Other apps (Danny, Alicia, SofaCare, Cleanic, R&C): copy the same two files and add the same secret to each app
   (only Edwin can paste the value; Claude can't read secrets). Or add Claude to the llmGateway in API Flow Manager
   once, which covers every app at once (needs the key pasted there as `pageone-api-key`).
6. Bundle the checker fix from /mnt/project-files/handovers/2026-10-30-checker-false-down-fix.md in the same Publish.

## Limits
- Workflows that Base44 cancels before they start (status `insufficient_credits`) never reach this code. For those,
  the 01:05 SGT Claude night run writes the missed articles itself (seo-method/daily/articles.md "CREDITS OUT").
  To make writers survive fully, trigger them from the Bluehost cron (like Danny and SofaCare publishing) instead
  of Base44 workflows.
- Images still fall back to the OpenAI gateway (Claude does not make images).
- Models: Haiku 5.5 for short calls, Sonnet 5.5 for articles, JSON and web search.

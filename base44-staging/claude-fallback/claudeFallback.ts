// Claude API fallback for Base44 InvokeLLM (Page One Singapore).
// Used by shared/llmFallback.ts when Base44 refuses an LLM call for credit limits.
// The key is read from a Base44 secret at run time. It is never stored in code or in this repo.
import Anthropic from "npm:@anthropic-ai/sdk";

// Cheap models for routine runs (Edwin's token rules, 21 Oct 2026).
export const CLAUDE_FAST = "claude-haiku-5-5";    // short tasks: tags, summaries, checks
export const CLAUDE_WRITER = "claude-sonnet-5-5"; // articles, long JSON, web-search calls

// Edwin saved the key as "pageone-api-key" (Base44 shows "Pageone-api-key"). Env names are case-sensitive, so try each.
const KEY_NAMES = ["Pageone-api-key", "pageone-api-key", "PAGEONE_API_KEY", "ANTHROPIC_API_KEY"];

export function claudeKey(): string | null {
  for (const n of KEY_NAMES) {
    const v = Deno.env.get(n);
    if (v && v.trim()) return v.trim();
  }
  return null;
}

// Same params shape as Core.InvokeLLM: { prompt, response_json_schema?, add_context_from_internet?, file_urls?, model? }.
// Returns what InvokeLLM returns: a string, or the parsed object when response_json_schema is set.
export async function claudeInvokeLLM(params: any, opts: { long?: boolean } = {}): Promise<any> {
  const apiKey = claudeKey();
  if (!apiKey) throw new Error("Claude fallback: no pageone-api-key secret in this app");
  if (params?.file_urls?.length) throw new Error("Claude fallback: file_urls not supported");

  const client = new Anthropic({ apiKey, timeout: 170_000, maxRetries: 2 });
  const web = !!params?.add_context_from_internet;
  const schema = params?.response_json_schema;
  const promptLen = String(params?.prompt ?? "").length;
  const model = web || schema || opts.long || promptLen > 6000 ? CLAUDE_WRITER : CLAUDE_FAST;

  let prompt = String(params?.prompt ?? "");
  if (schema) {
    prompt += "\n\nReply with ONLY one JSON object that matches this JSON Schema. No markdown, no commentary.\n" +
      JSON.stringify(schema);
  }

  const req: any = {
    model,
    max_tokens: 16000,
    output_config: { effort: model === CLAUDE_FAST ? "low" : "medium" },
    messages: [{ role: "user", content: prompt }],
  };
  // Live web search keeps prospect / AI-visibility answers grounded instead of invented.
  if (web) req.tools = [{ type: "web_search_20260209", name: "web_search", max_uses: 5 }];

  let res: any;
  if (model === CLAUDE_WRITER) {
    // Server-side refusal fallback (Claude API only), as recommended for Sonnet 5.5.
    res = await client.beta.messages.create({ ...req, betas: ["server-side-fallback-2026-07-01"], fallbacks: "default" } as any);
  } else {
    res = await client.messages.create(req);
  }
  if (res.stop_reason === "refusal") throw new Error("Claude fallback: request declined");

  const text = (res.content ?? []).filter((b: any) => b.type === "text").map((b: any) => b.text).join("").trim();
  lastUsage = { model: res.model ?? model, input: res.usage?.input_tokens ?? 0, output: res.usage?.output_tokens ?? 0 };
  if (!schema) return text;
  return parseJson(text);
}

export let lastUsage: { model: string; input: number; output: number } | null = null;

function parseJson(text: string): any {
  const t = text.replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "").trim();
  try { return JSON.parse(t); } catch { /* fall through */ }
  const a = t.indexOf("{"), b = t.lastIndexOf("}");
  if (a >= 0 && b > a) return JSON.parse(t.slice(a, b + 1));
  throw new Error("Claude fallback: reply was not JSON");
}

// One row per fallback call, so the 05:30 SGT watchdog can tell Edwin what ran on Claude.
// Entity ClaudeFallbackLog: source, model, input_tokens, output_tokens, ok, error, run_date (SGT).
export async function logFallback(base44: any, source: string, ok: boolean, error?: string) {
  try {
    const sgt = new Date(Date.now() + 8 * 3600_000).toISOString().slice(0, 10);
    await base44.asServiceRole.entities.ClaudeFallbackLog.create({
      source, ok, error: error ? String(error).slice(0, 500) : "",
      model: lastUsage?.model ?? "", input_tokens: lastUsage?.input ?? 0, output_tokens: lastUsage?.output ?? 0,
      run_date: sgt,
    });
  } catch (_) { /* logging must never break a run */ }
}

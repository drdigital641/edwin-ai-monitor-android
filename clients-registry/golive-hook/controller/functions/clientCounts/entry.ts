// Public, read-only: the two client counts shown on pageonesingapore.com /clients/ (Edwin, 12 Nov 2026).
// No secret needed. Returns ONLY { ok, white_label_live, building } - never names, slugs or domains.
// Cached in memory for 5 minutes so page views don't each read the Client table.
// Counting rule (real client builds only, optional Client.count_as_building) lives in shared/clientCounts.ts.
// 22 Nov 2026: both numbers come from shared/clientsRegistry.ts, the same totals as pageonesingapore.com/clients/ (response shape unchanged).
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { cors, preflight } from '../../shared/publicApi.ts';
import { clientCounts } from '../../shared/clientCounts.ts';

const TTL_MS = 5 * 60 * 1000;
let cache: { at: number; body: { ok: true; white_label_live: number; building: number } } | null = null;

export default async function (req: Request) {
  const pre = preflight(req);
  if (pre) return pre;
  const headers = { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=300', ...cors(req),
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS' };
  if (req.method !== 'GET' && req.method !== 'POST') return new Response(JSON.stringify({ ok: false }), { status: 405, headers });
  try {
    if (!cache || Date.now() - cache.at > TTL_MS) {
      const base44 = createClientFromRequest(req);
      // every row (22 Nov 2026): registry status overrides apply to some rows the Controller marks dormant (SofaCare, billing only)
      const rows: any[] = await base44.asServiceRole.entities.Client.filter({}, '-created_date', 1000);
      cache = { at: Date.now(), body: { ok: true, ...clientCounts(rows || []) } };
    }
    return new Response(JSON.stringify(cache.body), { status: 200, headers });
  } catch (_e) {
    return new Response(JSON.stringify({ ok: false }), { status: 503, headers: { ...headers, 'Cache-Control': 'no-store' } });
  }
}

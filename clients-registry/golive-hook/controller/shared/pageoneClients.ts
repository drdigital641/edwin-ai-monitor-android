// After EVERY passed go-live (Edwin 22 Nov 2026, PERMANENT; both brands; goLive flip and clientSites Activate/runGoLive):
// refresh pageonesingapore.com /clients/ through the Bridge op pageone_clients. Numbers from shared/clientsRegistry.ts
// (same rules as clients-registry/registry.json + stats.py); a Page One public client also sends its card fields.
// Never throws: the result (or the error) is returned for golive_status.pageone_clients, and the go-live result is never changed.
import { pageoneClientsBody } from './clientsRegistry.ts';

export async function pageoneClientsAfterGoLive(E: any, c: any, bridge: (op: Record<string, unknown>) => Promise<any>): Promise<any> {
  try {
    const all: any[] = await E.Client.filter({}, '-created_date', 1000);   // every row: billing-only rows with a status override are dormant in the Controller
    const body = pageoneClientsBody(all || [], c);
    const r = await bridge(body);
    const { ok: _ok, ...rest } = r || {};
    return { ...rest, sent: { client: body.client, card: body.card ? (body.card as any).host : null }, at: new Date().toISOString() };
  } catch (e) {
    return { complete: false, error: (e instanceof Error ? e.message : String(e)).slice(0, 300), at: new Date().toISOString() };
  }
}

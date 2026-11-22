import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { cleanDomain } from '../../shared/goLiveGate.ts';
import { pageoneClientsAfterGoLive } from '../../shared/pageoneClients.ts';

// ONE-SWITCH GO-LIVE (Edwin 20 Nov 2026, 7:03pm SGT). Admin only. The Controller holds the domain + Live switch; the Bridge does the work
// (function bridgeGoLive, key scope golive in the secret BRIDGE_GOLIVE_KEY). The Bridge picks the site and folder from the client SLUG.
//   status { id, domain? } -> DNS (only 173.254.31.20) + https check, saved on the client
//   save   { id, domain }  -> keep the domain (refused while live)
//   flip   { id, live }    -> switch On (refused unless the domain gate passes) or Off (back to preview with noindex); report saved
const BRIDGE = 'https://blue-bridge-pilot.base44.app/functions/bridgeGoLive';
const RUN_LOCK_MS = 3 * 60_000;

async function bridge(op: Record<string, unknown>) {
  const key = Deno.env.get('BRIDGE_GOLIVE_KEY');
  if (!key) throw new Error('BRIDGE_GOLIVE_KEY is not set in this app. Make a go-live key on the Bridge Connect page and add it as a secret.');
  const r = await fetch(BRIDGE, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Bridge-Key': key }, body: JSON.stringify(op), signal: AbortSignal.timeout(170_000) });
  const j: any = await r.json().catch(() => ({}));
  if (!r.ok || j?.ok === false) throw new Error(String(j?.error || 'Bridge answered ' + r.status).slice(0, 1500));
  return j;
}

export default async function (req: Request) {
  const base44 = createClientFromRequest(req);
  const user = await base44.auth.me().catch(() => null);
  if (!user || user.role !== 'admin') return Response.json({ error: 'Forbidden' }, { status: 403 });
  const body = await req.json().catch(() => ({}));
  const action = String(body?.action || '');
  const E = base44.asServiceRole.entities;
  const c: any = await E.Client.get(String(body?.id || '')).catch(() => null);
  if (!c) return Response.json({ error: 'Client not found' }, { status: 404 });
  if (!/^[a-z0-9][a-z0-9-]{1,60}$/.test(String(c.slug || ''))) return Response.json({ error: 'This client has no usable slug' }, { status: 400 });
  const prev: any = c.golive_status || {};
  const save = (patch: any) => E.Client.update(c.id, patch);

  try {
    if (action === 'save') {
      if (c.golive) return Response.json({ error: 'Switch Live off before changing the domain.' }, { status: 400 });
      const d = cleanDomain(body.domain);
      if (body.domain && !d) return Response.json({ error: 'That is not a valid domain name.' }, { status: 400 });
      return Response.json({ ok: true, client: await save({ golive_domain: d, golive_status: { ...prev, status: null } }) });
    }
    if (action === 'status') {
      const d = cleanDomain(body.domain || c.golive_domain);
      if (!d) return Response.json({ error: 'Enter the client domain first.' }, { status: 400 });
      const r = await bridge({ op: 'status', domain: d });
      const gl = { ...prev, status: { ...r.status, at: new Date().toISOString() } };
      return Response.json({ ok: true, status: gl.status, client: await save({ golive_domain: c.golive ? c.golive_domain : d, golive_status: gl }) });
    }
    if (action === 'flip') {
      const live = body.live === true;
      const d = cleanDomain(c.golive_domain);
      if (!d) return Response.json({ error: 'Save the client domain first.' }, { status: 400 });
      if (live === !!c.golive && !prev.partial) return Response.json({ ok: true, unchanged: true, client: c });
      const started = Date.parse(prev.running_at || '') || 0;
      if (Date.now() - started < RUN_LOCK_MS) return Response.json({ error: 'A go-live run is already in progress. Wait a few minutes.' }, { status: 409 });
      await save({ golive_status: { ...prev, running_at: new Date().toISOString() } });
      let r: any;
      try { r = await bridge({ op: 'flip', slug: c.slug, site: String(c.brand || '').toLowerCase() === 'autoseo' ? 'autoseo' : 'pageone', domain: d, live, indexnow_key: c.indexnow_key || undefined }); }   // key: Bridge places <key>.txt if the folder has none
      catch (e) {
        const err = e instanceof Error ? e.message : String(e);
        await save({ golive_status: { ...prev, running_at: null, error: err, at: new Date().toISOString() } });
        return Response.json({ error: err }, { status: 502 });
      }
      const switched = !r.refused && !r.partial;
      const report = { status: r.status || prev.status || null, live: !!r.live, refused: !!r.refused, partial: !!r.partial, ok: r.ok ?? null, detail: r.detail || '', checks: r.checks || [],
        rules: r.rules || null, content: r.content ? { total: r.content.total, changed: r.content.changed, remaining: r.content.remaining } : null, running_at: null, error: null, at: new Date().toISOString() };
      const patch: any = { golive_status: report };
      if (switched) { patch.golive = live; patch.golive_at = report.at; }
      const saved = await save(patch);                                   // the switch result is saved first, whatever happens below
      // 21 Nov 2026 (Edwin, PERMANENT): every AutoSEO switch-on also adds the site to autoseo.my /clients/ (EN/BM/中文) + launches.json.
      // Industry override = Client.niche (an /industries/ id, e.g. tyre-shops). A failure here never changes the switch result.
      // 22 Nov 2026 (Edwin, PERMANENT): every switch-on, BOTH brands, also refreshes pageonesingapore.com /clients/ (white-label totals,
      // Page One counts, last-updated date; named card for a Page One public client), op pageone_clients. Runs next to clients_card
      // (different sites), result saved in golive_status.pageone_clients; a failure never changes the switch result either.
      if (switched && live && r.ok) {
        const isAutoseo = String(c.brand || '').toLowerCase() === 'autoseo';
        const [card, po] = await Promise.all([
          isAutoseo ? bridge({ op: 'clients_card', slug: c.slug, site: 'autoseo', domain: d, name: c.name || '', area: c.area || '', industry: c.niche || undefined })
            .catch((e) => ({ complete: false, error: (e instanceof Error ? e.message : String(e)).slice(0, 300) })) : Promise.resolve(undefined),
          pageoneClientsAfterGoLive(E, { ...c, golive: true, golive_domain: d }, bridge),
        ]);
        const report2: any = { ...report, pageone_clients: po };
        if (isAutoseo) report2.clients_card = card;
        return Response.json({ ok: true, report: report2, client: await save({ golive_status: report2 }).catch(() => saved) });
      }
      return Response.json({ ok: true, report, client: saved });
    }
    return Response.json({ error: 'Unknown action' }, { status: 400 });
  } catch (e) {
    return Response.json({ error: e instanceof Error ? e.message : String(e) }, { status: 500 });
  }
}

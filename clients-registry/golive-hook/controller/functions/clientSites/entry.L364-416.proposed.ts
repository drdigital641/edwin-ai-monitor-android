// ONE-SWITCH go-live for hand-built sites (Edwin 20 Nov): the Bridge does the full switch (pages, data files, asset paths,
// canonical/og/schema/sitemap/robots, noindex off, host-aware .htaccess, post-check with automatic rollback).
// 21 Nov 2026 (sgcaraccident.sg): Activate pressed before DNS/https were ready was refused and never tried again, so the
// domain served the preview pages with /preview/<slug>/ asset paths (no CSS). Now a refusal by the domain gate keeps the
// client in "Going live" with design_job golive_waiting, and check / check_all (every Clients page open) / set_status live
// run the switch again by themselves as soon as the domain is ready. Never marks a client live without a passed switch.
async function runGoLive(E: any, c: any): Promise<any> {
  const back = c.status === 'live' && c.golive ? 'live' : 'activating';
  if (lockedNow(c)) return { ok: false, busy: true, detail: 'A go-live switch for this site is already running. Try again in a few minutes.', error: 'A go-live switch for this site is already running.' };
  await E.Client.update(c.id, { golive_lock_at: new Date().toISOString() });
  try {
    const key = Deno.env.get('BRIDGE_GOLIVE_KEY');
    if (!key) throw new Error('BRIDGE_GOLIVE_KEY is not set in this app.');
    const site = String(c.brand || '').toLowerCase() === 'autoseo' ? 'autoseo' : 'pageone';
    const resp = await fetch('https://blue-bridge-pilot.base44.app/functions/bridgeGoLive', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Bridge-Key': key },
      body: JSON.stringify({ op: 'flip', slug: c.slug, site, domain: c.domain, live: true, indexnow_key: c.indexnow_key || undefined }), signal: AbortSignal.timeout(170_000) });
    const r: any = await resp.json().catch(() => ({}));
    if (!resp.ok || r?.ok === false && !r.checks && !r.refused) throw new Error(String(r?.error || 'Bridge answered ' + resp.status).slice(0, 400));
    if (r.refused && r.status && !r.status.can_go_live && !(r.checks || []).length) {
      // Domain not ready yet (DNS or https). Nothing was changed; wait and retry by itself.
      await E.Client.update(c.id, { golive_lock_at: null, status: back, design_job: 'golive_waiting', design_progress: 20,
        golive_status: { ...(c.golive_status || {}), live: false, refused: true, waiting: true, detail: r.detail || '', checks: [], at: new Date().toISOString() },
        design_step: 'Waiting for the domain (' + String(r.status.detail || r.detail || 'DNS or https not ready').slice(0, 200) + '). The switch runs by itself as soon as DNS points here and https works: each time the Clients page opens, or tap Check now.' });
      return { ok: false, waiting: true, detail: r.detail, client: await E.Client.get(c.id) };
    }
    if (r.refused || r.partial || !r.ok) {
      const bad = (r.checks || []).filter((x: any) => !x.ok).map((x: any) => x.name).join('; ');
      await E.Client.update(c.id, { golive_lock_at: null, status: back, design_job: r.partial ? 'golive_waiting' : 'golive_failed', golive_status: { ...(c.golive_status || {}), live: false, refused: !!r.refused, partial: !!r.partial, detail: r.detail || '', checks: r.checks || [], at: new Date().toISOString() },
        design_step: (r.partial ? 'Part done, continues by itself: ' : 'NOT live (nothing half-switched): ') + String(r.detail || bad || 'check failed').slice(0, 300) + (r.partial ? '' : ' Fix it, then press Check now.') });
      return { ok: false, refused: true, detail: r.detail, error: 'Not live: ' + String(r.detail || 'checks failed').slice(0, 300), checks: r.checks || [] };
    }
    const client = await E.Client.update(c.id, { golive_lock_at: null, status: 'live', golive: true, golive_domain: c.domain, golive_at: new Date().toISOString(), live_at: c.live_at || new Date().toISOString(), design_job: 'site_live', design_progress: 100,
      golive_status: { live: true, ok: true, detail: r.detail || '', checks: r.checks || [], content: r.content ? { total: r.content.total, changed: r.content.changed } : null, at: new Date().toISOString() },
      design_step: `Switched to ${c.domain}: ${r.content?.changed ?? 0} files updated, host rules on, all ${(r.checks || []).length} checks passed.` });
    // 21 Nov 2026 (Edwin, PERMANENT): an AutoSEO switch-on also adds the site to autoseo.my /clients/ (EN/BM/中文) + launches.json.
    // Industry override = Client.niche (an /industries/ id). Runs after the live state is saved; a failure never changes it.
    // 22 Nov 2026 (Edwin, PERMANENT): every passed switch-on, BOTH brands, also refreshes pageonesingapore.com /clients/ (white-label
    // totals, Page One counts, last-updated date; named card for a Page One public client), op pageone_clients, saved in
    // golive_status.pageone_clients. Runs next to clients_card (different sites); a failure never changes the live state.
    const bridgeOp = async (op: Record<string, unknown>) => {
      const cr = await fetch('https://blue-bridge-pilot.base44.app/functions/bridgeGoLive', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Bridge-Key': key },
        body: JSON.stringify(op), signal: AbortSignal.timeout(170_000) });
      const j: any = await cr.json().catch(() => ({}));
      if (!cr.ok || j?.ok === false) throw new Error(String(j?.error || 'Bridge answered ' + cr.status).slice(0, 300));
      return j;
    };
    const [card, po] = await Promise.all([
      site === 'autoseo' ? bridgeOp({ op: 'clients_card', slug: c.slug, site, domain: c.domain, name: c.name || '', area: c.area || '', industry: c.niche || undefined })
        .catch((e: any) => ({ complete: false, error: String(e?.message || e).slice(0, 300) })) : Promise.resolve(undefined),
      pageoneClientsAfterGoLive(E, client || { ...c, status: 'live', golive: true, golive_domain: c.domain }, bridgeOp),
    ]);
    const extra: any = { pageone_clients: po };
    if (site === 'autoseo') extra.clients_card = card;
    const out = await E.Client.update(c.id, { golive_status: { ...(client?.golive_status || {}), ...extra } }).catch(() => client);
    return { ok: true, golive: r, client: out };
  } catch (e: any) {
    await E.Client.update(c.id, { golive_lock_at: null, status: back, design_job: 'golive_failed', design_step: 'Go-live switch failed: ' + String(e?.message || e).slice(0, 200) + ' (tap Check now to retry).' }).catch(() => null);
    return { ok: false, error: String(e?.message || e).slice(0, 300), detail: String(e?.message || e).slice(0, 300) };
  }
}

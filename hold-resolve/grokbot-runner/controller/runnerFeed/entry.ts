// GROKBOT RUNNER (Edwin 18 Nov 2026): what the Grok Bot API runner may see and change here, always through the Bluehost
// Bridge (bridgeRunnerController), never directly. Accepted only from a request signed with the Bridge's private key
// (same pinned key as articleFeed / crawlerIngest, less than 20 minutes old, purpose 'grokbot_runner'), or a signed-in
// admin / CRON_KEY for testing. The apps share no secret.
//   { op: 'copy_fix', site? }  -> sites whose dashboard row needs a fix (urgent/warn): the issue text and the exact
//                                 "Copy fix" instruction the dashboard copies, plus the current FixRequest status. Read only.
//   { op: 'taps', site? }      -> CTA tap counts per site (unique visitors today / 7 days, raw taps, per-day WhatsApp)
//                                 and enquiry counts. Counts only: no visitor ids, numbers, messages or client contacts.
//   { op: 'article_last', slug, date, title, url } -> sets ONLY article_last_built / article_last_title / article_last_url
//                                 on that Client record. Nothing else is written.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { guard } from '../../shared/guard.ts';
import { verifyBridgeBatch } from '../../shared/crawlerEval.ts';

const PURPOSE = 'grokbot_runner';
const clip = (v: unknown, n: number) => String(v ?? '').replace(/[\u0000-\u001f\u007f<>]/g, ' ').trim().slice(0, n);
const bare = (h: string) => String(h || '').toLowerCase().replace(/^https?:\/\//, '').replace(/\/.*$/, '').replace(/^www\./, '');
const PREVIEW_HOSTS = ['pageonesingapore.com', 'autoseo.my'];

export default async function (req: Request) {
  if (req.method !== 'POST') return Response.json({ ok: false, error: 'method' }, { status: 405 });
  const base44 = createClientFromRequest(req);
  const body = await req.clone().json().catch(() => null);
  const verified = await verifyBridgeBatch(body);
  let p: any;
  if (verified.ok && verified.payload?.purpose === PURPOSE) p = verified.payload;
  else {
    const denied = await guard(req, base44);
    if (denied) return denied;
    p = body || {};
  }
  const op = String(p?.op || '');
  const E = base44.asServiceRole.entities;

  if (op === 'copy_fix' || op === 'taps') {
    const r: any = await base44.asServiceRole.functions.invoke('portfolio', { action: 'runner_status', cron_key: Deno.env.get('CRON_KEY') || '' }).catch(() => null);
    const d = r?.data ?? r;
    if (!d || !Array.isArray(d.sites)) return Response.json({ ok: false, error: 'Dashboard status not available' }, { status: 502 });
    const only = p?.site ? clip(p.site, 80) : '';
    const sites = d.sites.filter((s: any) => !only || s.key === only);
    const meta = { refreshed_at: d.refreshed_at || null, stale: !!d.stale };
    if (op === 'copy_fix') {
      const issues = sites.filter((s: any) => ['urgent', 'warn'].includes(s.action?.level)).map((s: any) => ({
        site: s.key, name: s.name, url: s.url, level: s.action.level, issue: s.action.text,
        // Same text as the dashboard's Copy fix button (PortfolioOverview.jsx copyFix).
        copy_fix: `Fix this issue on ${s.name} (${s.url}):\n\n"${s.action?.text}"\n\nDiagnose from primary evidence, apply the smallest safe fix, and verify on the live site.`,
        checks: Array.isArray(s.issues) ? s.issues.slice(0, 20) : [], health_score: s.health_score ?? null,
        fix: s.fix ? { status: s.fix.status, issue: s.fix.issue, result: s.fix.result, requested_at: s.fix.requested_at, finished_at: s.fix.finished_at } : null,
      }));
      return Response.json({ ok: true, ...meta, count: issues.length, issues }, { headers: { 'Cache-Control': 'no-store' } });
    }
    const taps = sites.map((s: any) => ({ site: s.key, name: s.name, url: s.url, cta: s.cta || {}, wa_days: s.wa_days || [],
      ...(s.enq_today !== undefined ? { enq_today: s.enq_today, enq_7d: s.enq_7d } : {}) }));
    return Response.json({ ok: true, ...meta, count: taps.length, taps }, { headers: { 'Cache-Control': 'no-store' } });
  }

  if (op === 'article_last') {
    const slug = clip(p?.slug, 80);
    if (!/^[a-z0-9][a-z0-9-]{1,79}$/.test(slug)) return Response.json({ ok: false, error: 'slug must be the Controller client slug' }, { status: 400 });
    const date = clip(p?.date, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return Response.json({ ok: false, error: 'date must be YYYY-MM-DD (SGT)' }, { status: 400 });
    const title = clip(p?.title, 200);
    if (!title) return Response.json({ ok: false, error: 'title is required' }, { status: 400 });
    const url = clip(p?.url, 400);
    let host = '';
    try { const u = new URL(url); if (u.protocol === 'https:' && !u.username && !u.password && !u.port) host = bare(u.hostname); } catch { /* bad */ }
    const rows: any[] = (await E.Client.filter({ slug }, '-created_date', 3).catch(() => [])).filter((c: any) => !c.is_partner);
    if (rows.length !== 1) return Response.json({ ok: false, error: rows.length ? 'More than one client has this slug' : 'Unknown client slug' }, { status: 404 });
    const c = rows[0];
    if (!host || (host !== bare(c.domain || '') && !PREVIEW_HOSTS.includes(host))) return Response.json({ ok: false, error: 'url must be https on the client domain or its preview host' }, { status: 400 });
    await E.Client.update(c.id, { article_last_built: date, article_last_title: title, article_last_url: url });
    return Response.json({ ok: true, slug, date }, { headers: { 'Cache-Control': 'no-store' } });
  }

  return Response.json({ ok: false, error: 'op must be copy_fix, taps or article_last' }, { status: 400 });
}

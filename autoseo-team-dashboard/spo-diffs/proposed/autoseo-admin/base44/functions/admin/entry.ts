// AutoSEO team dashboard (Edwin 21 Nov 2026): the ONLY server function the page calls.
// 1) The caller must be signed in to THIS app (Base44 email + password login; the app is private_with_login,
//    invite-only). A non-invited account gets no user from auth.me() and is refused here with 401 and no data.
// 2) Client data: forwarded to the Controller's autoseoLink function, signed with this app's P-256 private key
//    (shared/linkAuth.ts, audience 'autoseo-controller'). The Controller re-checks the signed email against its
//    AutoSEO allowlist and returns only AutoSEO-brand rows through teamRow(). Read only.
// 3) Billing: AutoSEO's OWN records for billing its clients in RM (entity AutoseoBillingPlan in this app, server-only
//    RLS). No Stripe call of any kind until a key is added and reviewed. Page One billing is never read here.
// 4) Sales network (Edwin 21 Nov 9:11am SGT: ONE app): SalesNode + SalesSettings live in THIS app now (copied from the
//    old AutoSEO Sales Web app, legacyId kept). Same rules as the old /sales page. Server-only RLS.
// 5) The private key is made here on first use and stored in LinkKey (no user can read it). Only an admin of this app
//    can read the PUBLIC key (action link_public_key) to give to the Controller and Sales Web in a reviewed checkpoint.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { generateLinkKey, signLink, LINK_MAX_BODY } from '../../shared/linkAuth.ts';

const CONTROLLER = 'https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/autoseoLink';
const CONTROLLER_ACTIONS = ['me', 'team_clients'];                       // v1: read only (no memo, no new client)
const SALES_ACTIONS: Record<string, string> = { sales_data: 'data', sales_add: 'add', sales_remove: 'remove', sales_settings: 'settings' };
const MAX_NODES = 500;
const DEFAULT_SPLIT = { customer: 300, direct: 60, referral: 40 };
const cleanName = (v: unknown) => String(v ?? '').replace(/[\u0000-\u001f\u007f<>]/g, '').replace(/\s+/g, ' ').trim().slice(0, 60);
const nodeOut = (n: any) => ({ id: String(n.id), name: String(n.name || ''), role: String(n.role || ''), parentId: String(n.parentId || '') });
async function readSplit(E: any) {
  const r: any = (await E.SalesSettings.filter({ key: 'main' }).catch(() => []))[0];
  return r ? { customer: Number(r.customer ?? 300), direct: Number(r.direct ?? 60), referral: Number(r.referral ?? 40) } : { ...DEFAULT_SPLIT };
}
// Same checks as the old Sales Web: numbers 0..1,000,000 with 2 decimals, customer > 0, direct + referral <= customer.
function checkSplit(v: any) {
  const out: any = {};
  for (const k of ['customer', 'direct', 'referral']) {
    const n = Number(v?.[k]);
    if (!Number.isFinite(n) || n < 0 || n > 1_000_000 || Math.round(n * 100) !== n * 100) return { error: 'number' };
    out[k] = n;
  }
  if (out.customer <= 0) return { error: 'number' };
  if (out.direct + out.referral > out.customer) return { error: 'too_much' };
  return { split: out };
}
async function sales(E: any, action: string, b: any) {
  const all: any[] = (await E.SalesNode.list('createdAt', MAX_NODES + 50).catch(() => [])) || [];
  const byId = new Map(all.map((n) => [n.id, n]));
  if (action === 'data') return reply({ ok: true, nodes: all.map(nodeOut), settings: await readSplit(E) });
  if (action === 'settings') {
    const r: any = checkSplit(b?.settings);
    if (r.error) return reply({ ok: false, code: r.error }, 400);
    const row: any = (await E.SalesSettings.filter({ key: 'main' }).catch(() => []))[0];
    if (row) await E.SalesSettings.update(row.id, r.split); else await E.SalesSettings.create({ key: 'main', ...r.split });
    return reply({ ok: true, settings: r.split });
  }
  if (action === 'add') {
    const name = cleanName(b?.name);
    const parent = byId.get(String(b?.parentId || ''));
    if (!name) return reply({ ok: false, code: 'name' }, 400);
    if (!parent) return reply({ ok: false, code: 'parent' }, 400);
    if (all.length >= MAX_NODES) return reply({ ok: false, code: 'full' }, 400);
    const created = await E.SalesNode.create({ name, role: 'salesperson', parentId: parent.id, createdAt: new Date().toISOString() });
    return reply({ ok: true, node: nodeOut(created) });
  }
  if (action === 'remove') {
    const node = byId.get(String(b?.id || ''));
    if (!node) return reply({ ok: false, code: 'parent' }, 404);
    if (node.role === 'centre') return reply({ ok: false, code: 'invalid' }, 400);
    // Referrals move up one level to the removed person's parent (same as the old /sales page).
    const kids = all.filter((n) => n.parentId === node.id);
    const parentIsCentre = byId.get(node.parentId)?.role === 'centre';
    for (const k of kids) await E.SalesNode.update(k.id, { parentId: node.parentId, role: parentIsCentre ? k.role : 'salesperson' });
    await E.SalesNode.delete(node.id);
    return reply({ ok: true, moved: kids.length });
  }
  return reply({ ok: false, code: 'invalid' }, 400);
}
const BILL_STATUS = ['', 'paid', 'due', 'failed', 'not_billed'];
const ID_RE = /^[a-f0-9]{24}$/;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const reply = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow' } });
const s = (v: unknown, n: number) => String(v ?? '').replace(/[\u0000-\u001f\u007f]/g, '').trim().slice(0, n);

async function linkKey(E: any) {
  let rows: any[] = await E.LinkKey.list('created_date', 1).catch(() => []);
  if (!rows.length) {
    const k = await generateLinkKey();
    await E.LinkKey.create({ ...k, created_at: new Date().toISOString() });
    rows = await E.LinkKey.list('created_date', 1);   // two first calls at once: both use the oldest row
  }
  return rows[0];
}

// One signed call. Only the fields each action needs leave this app.
async function signed(E: any, url: string, aud: string, actor: string, action: string, args: Record<string, unknown>) {
  const payload = JSON.stringify({ v: 1, aud, actor, action, args });
  if (new TextEncoder().encode(payload).length > LINK_MAX_BODY) return reply({ ok: false, code: 'invalid' }, 400);
  try {
    const k = await linkKey(E);
    const headers = await signLink(k.private_jwk, payload);
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', ...headers }, body: payload, signal: AbortSignal.timeout(28_000) });
    const j: any = await r.json().catch(() => null);
    if (!j || typeof j !== 'object') return reply({ ok: false, code: 'server' }, 502);
    if (r.status === 503) return reply({ ok: false, code: 'not_set' }, 503);
    if (j.ok === false && !j.code) j.code = String(j.error || 'server');   // Sales Web answers { error }
    return reply(j, 200);
  } catch {
    return reply({ ok: false, code: 'network' }, 502);
  }
}


const planOut = (p: any) => ({
  client_id: String(p.client_id), plan: String(p.plan || ''), amount: typeof p.amount === 'number' ? p.amount : null, currency: 'MYR',
  status: String(p.status || ''), period_start: String(p.period_start || ''), period_end: String(p.period_end || ''),
  handled_at: String(p.handled_at || ''), handled_for: String(p.handled_for || ''),
});

export default async function (req: Request) {
  if (req.method !== 'POST') return reply({ ok: false, code: 'invalid' }, 405);
  const base44 = createClientFromRequest(req);
  const user: any = await base44.auth.me().catch(() => null);
  const email = String(user?.email || '').trim().toLowerCase();
  if (!email || !['admin', 'user'].includes(String(user?.role || ''))) return reply({ ok: false, code: 'bad_token' }, 401);
  const b: any = await req.json().catch(() => ({}));
  const action = String(b?.action || '');
  const E = base44.asServiceRole.entities;

  if (action === 'link_public_key') {
    if (user.role !== 'admin') return reply({ ok: false, code: 'not_allowed' }, 403);
    const k = await linkKey(E);
    return reply({ ok: true, public_jwk: JSON.parse(k.public_jwk) });
  }

  if (CONTROLLER_ACTIONS.includes(action)) return signed(E, CONTROLLER, 'autoseo-controller', email, action, {});

  // Security review 21 Nov 2026: billing and sales also need the Controller's AutoSEO allowlist (defence in depth on top
  // of this app's invite list). One signed 'me' call; anything but ok:true stops here with the Controller's code.
  if (SALES_ACTIONS[action] || action.startsWith('billing_')) {
    const gate: any = await (await signed(E, CONTROLLER, 'autoseo-controller', email, 'me', {})).json().catch(() => null);
    if (!gate?.ok) return reply({ ok: false, code: String(gate?.code || 'not_allowed') }, gate?.code === 'not_set' ? 503 : 403);
  }
  if (SALES_ACTIONS[action]) return sales(E, SALES_ACTIONS[action], b);

  // ---------- billing: AutoSEO's own records (RM). No Stripe. ----------
  const P = E.AutoseoBillingPlan;
  if (action === 'billing_list') {
    const rows: any[] = await P.list('-updated_date', 500).catch(() => []);
    const seen = new Set<string>(), plans: any[] = [];
    for (const r of rows) if (r?.client_id && !seen.has(r.client_id)) { seen.add(r.client_id); plans.push(planOut(r)); }
    return reply({ ok: true, plans });
  }
  if (action === 'billing_save' || action === 'billing_handle') {
    const client_id = s(b?.client_id, 24);
    if (!ID_RE.test(client_id)) return reply({ ok: false, code: 'invalid' }, 400);
    const old: any = (await P.filter({ client_id }, '-updated_date', 1).catch(() => []))[0] || null;
    const at = new Date().toISOString();
    let patch: any;
    if (action === 'billing_handle') {
      if (!old) return reply({ ok: false, code: 'invalid' }, 400);
      patch = { handled_at: at, handled_for: String(old.period_end || ''), updated_by: email, updated_at: at };
    } else {
      const amount = b?.amount === null || b?.amount === '' || b?.amount === undefined ? null : Number(b.amount);
      if (amount !== null && (!Number.isFinite(amount) || amount < 0 || amount > 1_000_000 || Math.round(amount * 100) !== amount * 100)) return reply({ ok: false, code: 'number' }, 400);
      const status = String(b?.status || '');
      const ps = s(b?.period_start, 10), pe = s(b?.period_end, 10);
      if (!BILL_STATUS.includes(status) || (ps && !DATE_RE.test(ps)) || (pe && !DATE_RE.test(pe)) || (ps && pe && pe < ps)) return reply({ ok: false, code: 'invalid' }, 400);
      patch = { client_id, plan: s(b?.plan, 60), amount, currency: 'MYR', status, period_start: ps, period_end: pe, updated_by: email, updated_at: at };
    }
    const saved = old ? await P.update(old.id, patch) : await P.create(patch);
    return reply({ ok: true, plan: planOut(saved) });
  }

  return reply({ ok: false, code: 'invalid' }, 400);
}

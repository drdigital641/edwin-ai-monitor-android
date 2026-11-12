// AutoSEO Admin app: the ONLY server function the page calls (13 Nov 2026).
// 1) The caller must be signed in to THIS app (Base44 built-in Google login; the app is private_with_login, invite-only,
//    Google is the only login method). No Controller session or token ever reaches the browser.
// 2) It forwards one of four actions to the Controller's autoseoLink function, signed with this app's P-256 private key
//    (shared/linkAuth.ts). The Controller re-checks the signed email against its AutoSEO allowlist and owner scoping,
//    so this app holds no client data at all and cannot widen what a user sees.
// 3) The private key is made here on first use and stored in LinkKey (no user can read it: rls matches no role). Only an
//    admin of this app can read the PUBLIC key (action link_public_key) to give to the Controller.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { generateLinkKey, signLink, LINK_MAX_BODY } from '../../shared/linkAuth.ts';

const CONTROLLER = 'https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/autoseoLink';
const ACTIONS = ['me', 'clients', 'save_memo', 'create_client'];
const reply = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow' } });

// Only the fields each action needs leave this app.
function argsFor(action: string, b: any) {
  const s = (v: unknown, n: number) => String(v ?? '').slice(0, n);
  if (action === 'save_memo') return { client_id: s(b?.client_id, 64), memo: s(b?.memo, 5000) };
  if (action === 'create_client') return { company: s(b?.company, 120), url: s(b?.url, 200), url_type: s(b?.url_type, 10), notes: s(b?.notes, 5000) };
  return {};
}

async function linkKey(E: any) {
  let rows: any[] = await E.LinkKey.list('created_date', 1).catch(() => []);
  if (!rows.length) {
    const k = await generateLinkKey();
    await E.LinkKey.create({ ...k, created_at: new Date().toISOString() });
    rows = await E.LinkKey.list('created_date', 1);   // two first calls at once: both use the oldest row
  }
  return rows[0];
}

export default async function (req: Request) {
  if (req.method !== 'POST') return reply({ ok: false, code: 'invalid' }, 405);
  const base44 = createClientFromRequest(req);
  const user: any = await base44.auth.me().catch(() => null);
  const email = String(user?.email || '').trim().toLowerCase();
  if (!email) return reply({ ok: false, code: 'bad_token' }, 401);
  const b: any = await req.json().catch(() => ({}));
  const action = String(b?.action || '');
  const E = base44.asServiceRole.entities;

  if (action === 'link_public_key') {
    if (user.role !== 'admin') return reply({ ok: false, code: 'not_allowed' }, 403);
    const k = await linkKey(E);
    return reply({ ok: true, public_jwk: JSON.parse(k.public_jwk) });
  }
  if (!ACTIONS.includes(action)) return reply({ ok: false, code: 'invalid' }, 400);

  const payload = JSON.stringify({ v: 1, aud: 'autoseo-controller', actor: email, action, args: argsFor(action, b) });
  if (new TextEncoder().encode(payload).length > LINK_MAX_BODY) return reply({ ok: false, code: 'invalid' }, 400);
  try {
    const k = await linkKey(E);
    const headers = await signLink(k.private_jwk, payload);
    const r = await fetch(CONTROLLER, { method: 'POST', headers: { 'Content-Type': 'application/json', ...headers }, body: payload, signal: AbortSignal.timeout(28_000) });
    const j: any = await r.json().catch(() => null);
    if (!j || typeof j !== 'object') return reply({ ok: false, code: 'server' }, 502);
    return reply(j, r.status === 503 ? 503 : 200);
  } catch {
    return reply({ ok: false, code: 'network' }, 502);
  }
}

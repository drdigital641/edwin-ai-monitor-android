// AutoSEO Admin app -> Controller signed link (Edwin 13 Nov 2026 12:10am SGT: separate AutoSEO Admin Base44 app,
// no Controller session for AutoSEO staff, ever). Only the AutoSEO Admin app's server calls this, signed with its
// P-256 private key (shared/linkAuth.ts). Order on every call:
//   1) signature headers + 2-minute window checked BEFORE the body is read; body capped; signature; nonce used once
//   2) payload shape: { v: 1, aud: 'autoseo-controller', actor: <email the AutoSEO Admin app signed in with Google>,
//      action, args } - anything else is refused
//   3) actor must be an ACTIVE AutoseoAdminUser row (the same allowlist Edwin runs on the AutoSEO tab)
//   4) only that row's account's clients are read or written (shared/autoseoAdmin.ts accountClients / publicRow)
// Same four actions and the same rules as autoseoAdmin (the Google Client ID route, now OFF by default):
//   me | clients | save_memo { client_id, memo } | create_client { company, url, url_type, notes }
// No preAuth / Controller session is involved, and nothing outside publicRow() ever leaves the Controller.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { AUTOSEO, byBrand, partnerOf } from '../../shared/brand.ts';
import { safeFetch, readText } from '../../shared/siteAudit.ts';
import { parseArticleIndex } from '../../shared/articleRuns.ts';
import { slugify } from '../../shared/clientSite.ts';
import { verifyLink } from '../../shared/linkAuth.ts';
import { AUTOSEO_ADMIN_LINK_PUBLIC_JWK } from '../../shared/autoseoLinkKey.ts';
import { normEmail, accountClients, defaultAccountOf, publicRow, openUrlOf, stepOf, countTaps, cleanNewClient, cleanMemo } from '../../shared/autoseoAdmin.ts';

const ACTIONS = ['me', 'clients', 'save_memo', 'create_client'];
const NONCE_KEEP_MS = 10 * 60_000;
const out = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
const deny = (status: number) => out({ ok: false, code: status === 503 ? 'not_set' : status === 413 ? 'too_large' : 'bad_link' }, status);

// The signed payload, strictly: any extra or missing field is refused.
export function cleanPayload(raw: string): { actor: string; action: string; args: any } | null {
  let p: any; try { p = JSON.parse(raw); } catch { return null; }
  if (!p || typeof p !== 'object' || Array.isArray(p)) return null;
  if (p.v !== 1 || p.aud !== 'autoseo-controller') return null;
  const actor = normEmail(p.actor);
  if (!/^[^@\s]{1,64}@[^@\s]{1,190}$/.test(actor)) return null;
  if (!ACTIONS.includes(String(p.action))) return null;
  const args = p.args && typeof p.args === 'object' && !Array.isArray(p.args) ? p.args : {};
  return { actor, action: String(p.action), args };
}

const UA = 'AutoSEOSiteChecker/1.0';
const CACHE_MS = 10 * 60 * 1000;
const cache = new Map<string, { at: number; v: any }>();
async function cached<T>(key: string, fn: () => Promise<T>): Promise<T> {
  const hit = cache.get(key);
  if (hit && Date.now() - hit.at < CACHE_MS) return hit.v;
  const v = await fn();
  cache.set(key, { at: Date.now(), v });
  return v;
}
async function healthOf(url: string) {
  if (!url) return 'none';
  let u: URL; try { u = new URL(url); } catch { return 'none'; }
  const r = await safeFetch(u, 9000, UA).catch(() => null);
  try { r?.res?.body?.cancel(); } catch { /* ignore */ }
  if (!r || !r.res) return 'down';
  if (r.res.status >= 500) return 'down';
  if (!r.res.ok) return 'warn';
  return r.ms > 5000 ? 'warn' : 'ok';
}
async function articlesOf(url: string) {
  if (!url) return 0;
  let idx: URL; try { idx = new URL('articles/', url); } catch { return 0; }
  const r = await safeFetch(idx, 9000, UA).catch(() => null);
  if (!r?.res?.ok) { try { r?.res?.body?.cancel(); } catch { /* ignore */ } return 0; }
  return parseArticleIndex((await readText(r.res)).text, r.url.toString()).length;
}

export default async function (req: Request) {
  if (req.method !== 'POST') return deny(401);
  const base44 = createClientFromRequest(req);
  const E = base44.asServiceRole.entities;
  const N = E.AutoseoLinkNonce;
  const check = await verifyLink(req.headers, () => req.text(), {
    publicJwk: AUTOSEO_ADMIN_LINK_PUBLIC_JWK,
    useNonce: async (nonce) => {
      const seen: any[] = await N.filter({ nonce }, '-created_date', 1).catch(() => [{}]);
      if (seen.length) return false;
      return await N.create({ nonce, at: new Date().toISOString() }).then(() => true).catch(() => false);
    },
  });
  if (!check.ok) return deny(check.status);
  // Nonces older than 10 minutes can never pass the 2-minute window again.
  N.filter({ at: { $lt: new Date(Date.now() - NONCE_KEEP_MS).toISOString() } }, 'at', 50)
    .then((old: any[]) => Promise.all(old.map((r) => N.delete(r.id).catch(() => null)))).catch(() => null);
  const p = cleanPayload(check.body);
  if (!p) return out({ ok: false, code: 'invalid' }, 400);
  const body = p.args, action = p.action;

  try {
    // allowlist (Edwin controls it on the AutoSEO tab)
    const users: any[] = await E.AutoseoAdminUser.filter({ email: p.actor }, '-created_date', 5).catch(() => []);
    const me = users.find((u) => u && u.active === true && normEmail(u.email) === p.actor && u.account_id);
    if (!me) return out({ ok: false, code: 'not_allowed' }, 403);

    const all: any[] = byBrand(await E.Client.filter({ brand: AUTOSEO }, '-created_date', 1000).catch(() => []), AUTOSEO);
    const account = all.find((c) => c.id === me.account_id && c.is_partner && !c.duplicate_of);
    if (!account) return out({ ok: false, code: 'not_allowed' }, 403);
    const partner = partnerOf(all, AUTOSEO);
    const mine = accountClients(all, account.id, defaultAccountOf(all));

    if (!me.last_seen_at || Date.now() - Date.parse(me.last_seen_at) > 3600e3) {
      E.AutoseoAdminUser.update(me.id, { last_seen_at: new Date().toISOString() }).catch(() => null);
    }

    if (action === 'me') {
      return out({ ok: true, user: { email: p.actor, name: String(me.name || '') }, group_link: String(account.autoseo_group_link || '') });
    }

    if (action === 'clients') {
      const since = new Date(Date.now() - 30 * 864e5).toISOString();
      const rows = await Promise.all(mine.map(async (c) => {
        const open = openUrlOf(c, partner);
        const [health, articles, taps] = await Promise.all([
          stepOf(c.status) === 'pending' ? 'none' : cached('h:' + open, () => healthOf(open)),
          stepOf(c.status) === 'pending' ? 0 : cached('a:' + open, () => articlesOf(open)),
          c.slug ? cached('t:' + c.slug, async () => countTaps(await E.CtaClick.filter({ site: c.slug, created_date: { $gte: since } }, '-created_date', 3000).catch(() => []))) : { wa: 0, call: 0 },
        ]);
        return publicRow(c, partner, { health, articles, taps });
      }));
      const order = { pending: 0, preview: 1, live: 2 } as Record<string, number>;
      rows.sort((a, b) => (order[a.step] - order[b.step]) || a.name.localeCompare(b.name));
      return out({ ok: true, clients: rows });
    }

    if (action === 'save_memo') {
      const c = mine.find((x) => x.id === String(body?.client_id || ''));
      if (!c) return out({ ok: false, code: 'not_found' }, 404);
      const at = new Date().toISOString();
      await E.Client.update(c.id, { autoseo_memo: cleanMemo(body?.memo), autoseo_memo_at: at, autoseo_memo_by: p.actor });
      return out({ ok: true, memo_updated_at: at });
    }

    // create_client: the one record the dashboard adds
    const x = cleanNewClient(body);
    if (x.errors.length) return out({ ok: false, code: 'invalid', fields: x.errors }, 400);
    const dayAgo = Date.now() - 864e5;
    const recent = all.filter((c) => c.autoseo_owner_id === account.id && c.autoseo_submitted_at && Date.parse(c.autoseo_submitted_at) > dayAgo);
    if (recent.length >= 20) return out({ ok: false, code: 'rate' }, 429);
    const taken = new Set(((await E.Client.list('-created_date', 2000).catch(() => [])) as any[]).map((c) => c.slug));
    const base = slugify(x.company);
    let slug = base, n = 2;
    while (taken.has(slug) || ['pageone', 'sggarage', 'cleanic', 'sofacare', 'alicia', 'danny', 'autoseo-my', 'admin'].includes(slug)) slug = `${base}-${n++}`;
    const at = new Date().toISOString();
    const created: any = await E.Client.create({
      name: x.company, slug, status: 'draft', brand: AUTOSEO,
      autoseo_owner_id: account.id, autoseo_followup: true,
      autoseo_preferred_url: x.url, autoseo_url_type: x.url_type, autoseo_notes: x.notes,
      autoseo_submitted_by: p.actor, autoseo_submitted_at: at,
    });
    return out({ ok: true, client_id: created?.id || '' });
  } catch (_e) {
    return out({ ok: false, code: 'server' }, 500);
  }
}

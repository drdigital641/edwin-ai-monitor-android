// K Tech (ktech.my) Autel MS906 MAX year-end promotion: checkout order endpoint (22 Nov 2026, Edwin's brief).
// Public endpoint called by the ktech.my checkout pages (EN, /ms/, /zh/). Only the browser Origin ktech.my is accepted.
//   action "order":  validate -> store KtechOrder FIRST (status awaiting_payment) -> payment switch:
//       secret KTECH_STRIPE_SECRET_KEY set  -> Stripe Checkout Session (K Tech's own account), answer { ref, pay_url }
//       else secret KTECH_STRIPE_PAYMENT_URL -> Stripe Payment Link + prefilled_email + client_reference_id
//       else (today)                          -> { ref, pay_url: null }: page shows "Payment link opening soon"
//   action "status": success page check. Re-reads the Checkout Session from Stripe with the secret key; the order is
//       marked paid only when Stripe says payment_status = paid for this order's ref. The browser is never trusted.
// Price, product and end date are fixed here (server side), never taken from the browser.
// Never answers with stored data beyond the customer's own ref and status. No emails are sent (notifications OFF, TBC).
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';

const PRODUCT = 'Autel MaxiSys MS906 MAX';
const UNIT = 5800;                       // RM per unit, postage within Malaysia included
const CURRENCY = 'MYR';
const ENDS_AT = Date.parse('2026-12-31T16:00:00Z'); // 1 Jan 2027 00:00 MYT = after 31 Dec 2026 23:59:59 MYT
const MAX_QTY = 10;
const ORIGINS = ['https://ktech.my', 'https://www.ktech.my'];
const SITE = 'https://ktech.my';
const LANGS: Record<string, string> = { en: '', ms: 'ms/', zh: 'zh/' };
const STATES = ['Johor', 'Kedah', 'Kelantan', 'Melaka', 'Negeri Sembilan', 'Pahang', 'Perak', 'Perlis', 'Pulau Pinang',
  'Sabah', 'Sarawak', 'Selangor', 'Terengganu', 'Kuala Lumpur', 'Putrajaya', 'Labuan'];
const MAX_BODY = 4096;
const PER_IP_10MIN = 5, PER_DAY_ALL = 300;

const clip = (v: unknown, n: number) => String(v ?? '').replace(/[\u0000-\u001f\u007f]+/g, ' ').replace(/\s+/g, ' ').trim().slice(0, n);

function cors(origin: string) {
  return { 'Access-Control-Allow-Origin': ORIGINS.includes(origin) ? origin : ORIGINS[0], 'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type', 'Access-Control-Max-Age': '86400', 'Vary': 'Origin', 'Cache-Control': 'no-store',
    'Content-Type': 'application/json' };
}
const out = (origin: string, status: number, body: unknown) => new Response(JSON.stringify(body), { status, headers: cors(origin) });

// Malaysian mobile: +60 / 60 / 0 then 1x and 7-8 more digits (01x-xxx xxxx). Normalised to +601xxxxxxxx.
export function normPhone(v: string): string | null {
  let d = String(v || '').replace(/[\s\-().]/g, '');
  if (d.startsWith('+')) d = d.slice(1);
  if (d.startsWith('60')) d = d.slice(2); else if (d.startsWith('0')) d = d.slice(1); else return null;
  if (d.startsWith('0')) d = d.slice(1);
  return /^1\d{8,9}$/.test(d) ? '+60' + d : null;
}

export function validate(b: any) {
  const errs: string[] = [];
  const name = clip(b.name, 80), email = clip(b.email, 120).toLowerCase();
  const phone = normPhone(clip(b.phone, 24));
  const a1 = clip(b.address_line1, 120), a2 = clip(b.address_line2, 120), city = clip(b.city, 60), state = clip(b.state, 40);
  const postcode = clip(b.postcode, 8);
  const qty = Number(b.qty);
  if (name.length < 2) errs.push('name');
  if (!phone) errs.push('phone');
  if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email)) errs.push('email');
  if (a1.length < 3) errs.push('address_line1');
  if (!/^\d{5}$/.test(postcode)) errs.push('postcode');
  if (city.length < 2) errs.push('city');
  if (!STATES.includes(state)) errs.push('state');
  if (!Number.isInteger(qty) || qty < 1 || qty > MAX_QTY) errs.push('qty');
  if (b.consent !== true) errs.push('consent');
  return { errs, rec: { name, email, phone: phone || '', address_line1: a1, address_line2: a2, postcode, city, state, qty } };
}

// IP is never stored. Only HMAC-SHA256(KTECH_IP_SALT, ip) is kept, for the rate limit. Without the secret a random
// per-instance salt is used (hashes then can't be linked across instances or reversed). Only the platform's real-IP
// header is trusted; no IP = no per-IP limit (the day cap still applies).
const RUN_SALT = Array.from(crypto.getRandomValues(new Uint8Array(32)), (x) => x.toString(16).padStart(2, '0')).join('');
async function ipHash(req: Request): Promise<string> {
  const ip = (req.headers.get('cf-connecting-ip') || '').trim();
  if (!ip) return '';
  const salt = (Deno.env.get('KTECH_IP_SALT') || '').trim() || RUN_SALT;
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(salt), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode('ktech-order-rl:' + ip));
  return Array.from(new Uint8Array(sig)).map((x) => x.toString(16).padStart(2, '0')).join('').slice(0, 32);
}

function newRef(now: Date) {
  const ymd = new Date(now.getTime() + 8 * 3600_000).toISOString().slice(2, 10).replace(/-/g, '');  // Malaysia date
  const abc = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  const r = crypto.getRandomValues(new Uint8Array(5));
  return `KT-MAX-${ymd}-` + Array.from(r, (x) => abc[x % abc.length]).join('');
}

const hits = new Map<string, number[]>();
function limited(key: string, max: number, win: number) {
  const now = Date.now(); const a = (hits.get(key) || []).filter((t) => now - t < win);
  if (a.length >= max) { hits.set(key, a); return true; }
  a.push(now); hits.set(key, a); if (hits.size > 5000) hits.clear(); return false;
}

function form(obj: Record<string, string | number>) {
  return Object.entries(obj).map(([k, v]) => encodeURIComponent(k) + '=' + encodeURIComponent(String(v))).join('&');
}
async function stripe(key: string, method: string, path: string, body?: Record<string, string | number>) {
  const r = await fetch('https://api.stripe.com/v1/' + path, { method, headers: { Authorization: 'Bearer ' + key,
    'Content-Type': 'application/x-www-form-urlencoded' }, body: body ? form(body) : undefined, signal: AbortSignal.timeout(8000) });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error('stripe ' + r.status + ' ' + clip(j?.error?.code || j?.error?.type || '', 60));
  return j;
}

function pageUrl(lang: string, q: string) { return `${SITE}/${LANGS[lang]}autel-ms906-max-promo/checkout/${q}`; }

async function payFor(order: any): Promise<{ mode: string; url: string | null; session?: string }> {
  const key = (Deno.env.get('KTECH_STRIPE_SECRET_KEY') || '').trim();
  const link = (Deno.env.get('KTECH_STRIPE_PAYMENT_URL') || '').trim();
  if (/^(sk|rk)_(live|test)_/.test(key)) {
    const meta: Record<string, string | number> = {
      'metadata[order_ref]': order.ref, 'metadata[product]': PRODUCT, 'metadata[qty]': order.qty, 'metadata[lang]': order.lang,
    };  // personal details stay in KtechOrder only (PDPA: Stripe Checkout collects its own shipping + phone)
    const s = await stripe(key, 'POST', 'checkout/sessions', {
      mode: 'payment', client_reference_id: order.ref, customer_email: order.email,
      'line_items[0][quantity]': order.qty, 'line_items[0][price_data][currency]': 'myr',
      'line_items[0][price_data][unit_amount]': UNIT * 100,
      'line_items[0][price_data][product_data][name]': PRODUCT + ' (year-end promotion, postage within Malaysia included)',
      'shipping_address_collection[allowed_countries][0]': 'MY', 'phone_number_collection[enabled]': 'true',
      'payment_intent_data[metadata][order_ref]': order.ref, ...meta,
      expires_at: Math.floor(Date.now() / 1000) + 23 * 3600,
      success_url: pageUrl(order.lang, `?ref=${order.ref}&session_id={CHECKOUT_SESSION_ID}`),
      cancel_url: pageUrl(order.lang, `?ref=${order.ref}&cancelled=1`),
    });
    return { mode: 'checkout', url: String(s.url || ''), session: String(s.id || '') };
  }
  if (/^https:\/\/(buy\.stripe\.com|checkout\.stripe\.com)\//.test(link)) {
    const u = new URL(link);
    u.searchParams.set('prefilled_email', order.email); u.searchParams.set('client_reference_id', order.ref);
    return { mode: 'payment_link', url: u.toString() };
  }
  return { mode: 'none', url: null };
}

export default async function (req: Request) {
  const origin = req.headers.get('origin') || '';
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(origin) });
  if (req.method !== 'POST') return out(origin, 405, { ok: false, error: 'method' });
  if (!ORIGINS.includes(origin)) return out(origin, 403, { ok: false, error: 'origin' });
  try {
    const raw = await req.text();
    if (raw.length > MAX_BODY) return out(origin, 413, { ok: false, error: 'size' });
    let b: any; try { b = JSON.parse(raw); } catch { return out(origin, 400, { ok: false, error: 'json' }); }
    if (!b || typeof b !== 'object' || Array.isArray(b)) return out(origin, 400, { ok: false, error: 'json' });
    const lang = ['en', 'ms', 'zh'].includes(b.lang) ? String(b.lang) : 'en';
    const svc = createClientFromRequest(req).asServiceRole;

    if (b.action === 'status') {
      const ref = clip(b.ref, 32), sid = clip(b.session_id, 200);
      const sip = await ipHash(req);
      if (limited('st:' + (sip || 'noip'), sip ? 20 : 200, 600_000)) return out(origin, 429, { ok: false, error: 'rate' });
      if (!/^KT-MAX-\d{6}-[A-Z0-9]{5}$/.test(ref)) return out(origin, 200, { ok: true, ref, status: 'unknown' });
      const rows = await svc.entities.KtechOrder.filter({ ref }, '-created_date', 1);
      const o = rows?.[0];
      if (!o) return out(origin, 200, { ok: true, ref, status: 'unknown' });  // same answer as a wrong ref: no probing
      const key = (Deno.env.get('KTECH_STRIPE_SECRET_KEY') || '').trim();
      if (o.status !== 'paid' && /^cs_(live|test)_/.test(sid) && o.stripe_session_id === sid && /^(sk|rk)_(live|test)_/.test(key)) {
        const s = await stripe(key, 'GET', 'checkout/sessions/' + encodeURIComponent(sid));
        if (s.client_reference_id === ref && s.payment_status === 'paid' && s.currency === 'myr' && Number(s.amount_total) === o.total * 100) {
          await svc.entities.KtechOrder.update(o.id, { status: 'paid', paid_at: new Date().toISOString(), paid_by: 'success_check',
            stripe_session_id: s.id, stripe_payment_intent: String(s.payment_intent || ''), amount_paid: Number(s.amount_total) / 100 });
          o.status = 'paid';
        }
      }
      return out(origin, 200, { ok: true, ref, status: o.status });
    }

    if (b.action !== 'order') return out(origin, 400, { ok: false, error: 'action' });
    const now = new Date();
    if (now.getTime() >= ENDS_AT) return out(origin, 410, { ok: false, error: 'ended' });
    const ip = await ipHash(req);
    // Honeypot / too-fast form: answer like a success with a made-up ref and store NOTHING.
    const fill = Number(b.fill_ms);
    const spam = clip(b.company_website, 100) !== '' || (Number.isFinite(fill) && fill >= 0 && fill < 2500);
    if (spam) return out(origin, 200, { ok: true, ref: newRef(now), pay_url: null });
    if (ip) {
      if (limited('ip:' + ip, PER_IP_10MIN, 600_000)) return out(origin, 429, { ok: false, error: 'rate' });
      const since = new Date(now.getTime() - 600_000).toISOString();
      const recent = await svc.entities.KtechOrder.filter({ ip_hash: ip, ordered_at: { $gte: since } }, '-created_date', PER_IP_10MIN + 1);
      if ((recent || []).length >= PER_IP_10MIN) return out(origin, 429, { ok: false, error: 'rate' });
    } else if (limited('noip', 60, 600_000)) return out(origin, 429, { ok: false, error: 'rate' });
    const today = new Date(now.getTime() - 86400_000).toISOString();
    const day = await svc.entities.KtechOrder.filter({ ordered_at: { $gte: today } }, '-created_date', PER_DAY_ALL + 1);
    if ((day || []).length >= PER_DAY_ALL) return out(origin, 429, { ok: false, error: 'rate' });

    const { errs, rec } = validate(b);
    if (errs.length) return out(origin, 422, { ok: false, error: 'invalid', fields: errs });
    const test = /^qa-test/i.test(rec.name);  // hand-made checks only; a browser flag is never trusted
    const order: any = { ...rec, ref: newRef(now), status: 'awaiting_payment', lang, product: PRODUCT, unit_price: UNIT,
      total: UNIT * rec.qty, currency: CURRENCY, pdpa_consent: true, ordered_at: now.toISOString(),
      page_path: clip(b.page_path, 120).split(/[?#]/)[0], ip_hash: ip, payment_mode: 'none' };
    if (test) order.flag = 'test';
    if (!order.ip_hash) delete order.ip_hash;
    if (!order.address_line2) delete order.address_line2;
    const saved = await svc.entities.KtechOrder.create(order);

    let pay: { mode: string; url: string | null; session?: string } = { mode: 'none', url: null };
    try { pay = await payFor(order); } catch (_e) {
      await svc.entities.KtechOrder.update(saved.id, { notes: 'payment start failed: ' + clip(String(_e), 120) });
      return out(origin, 200, { ok: true, ref: order.ref, pay_url: null, pay_error: true });
    }
    if (pay.mode !== 'none') await svc.entities.KtechOrder.update(saved.id, { payment_mode: pay.mode, ...(pay.session ? { stripe_session_id: pay.session } : {}) });
    return out(origin, 200, { ok: true, ref: order.ref, pay_url: pay.url });
  } catch (_e) {
    return out(origin, 500, { ok: false, error: 'server' });
  }
}

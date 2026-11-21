// K Tech promo orders: Stripe webhook (K Tech's OWN Stripe account; never a Page One key). Optional but recommended:
// it marks orders paid even when the customer closes the tab before the success page, and it is the only way
// Payment Link orders get marked paid. Needs secret KTECH_STRIPE_WEBHOOK_SECRET (whsec_...). Subscribe to:
//   checkout.session.completed, checkout.session.async_payment_succeeded
// Signature verified with HMAC-SHA256 (Stripe-Signature t=..,v1=..), 5-minute tolerance. Unsigned = refused.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';

async function hmac(secret: string, msg: string) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const s = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(msg));
  return Array.from(new Uint8Array(s)).map((x) => x.toString(16).padStart(2, '0')).join('');
}
function same(a: string, b: string) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }

export default async function (req: Request) {
  if (req.method !== 'POST') return new Response('method', { status: 405 });
  const secret = (Deno.env.get('KTECH_STRIPE_WEBHOOK_SECRET') || '').trim();
  const sig = req.headers.get('stripe-signature') || '';
  if (Number(req.headers.get('content-length') || 0) > 65536) return new Response('size', { status: 413 });
  const raw = await req.text();
  if (raw.length > 65536) return new Response('size', { status: 413 });
  if (!secret.startsWith('whsec_') || !sig) return new Response('not configured', { status: 400 });
  const parts = Object.fromEntries(sig.split(',').map((p) => p.split('=')).filter((p) => p.length === 2 && p[0] !== 'v1'));
  const v1s = sig.split(',').filter((p) => p.startsWith('v1=')).map((p) => p.slice(3));
  const t = Number(parts.t);
  if (!Number.isFinite(t) || Math.abs(Date.now() / 1000 - t) > 300) return new Response('stale', { status: 400 });
  const want = await hmac(secret, `${t}.${raw}`);
  if (!v1s.some((v) => same(v, want))) return new Response('signature', { status: 400 });
  let ev: any; try { ev = JSON.parse(raw); } catch { return new Response('json', { status: 400 }); }
  if (!['checkout.session.completed', 'checkout.session.async_payment_succeeded'].includes(ev?.type)) return new Response('ignored', { status: 200 });
  const s = ev.data?.object || {};
  const ref = String(s.client_reference_id || s.metadata?.order_ref || '');
  if (!/^KT-MAX-\d{6}-[A-Z0-9]{5}$/.test(ref) || s.payment_status !== 'paid') return new Response('ok', { status: 200 });
  const svc = createClientFromRequest(req).asServiceRole;
  const rows = await svc.entities.KtechOrder.filter({ ref }, '-created_date', 1);
  const o = rows?.[0];
  if (!o) return new Response('unknown ref', { status: 200 });
  const amount = Number(s.amount_total) / 100;
  const patch: Record<string, unknown> = { stripe_session_id: String(s.id || ''), stripe_payment_intent: String(s.payment_intent || ''), amount_paid: amount };
  if (s.currency === 'myr' && amount === o.total) { patch.status = 'paid'; patch.paid_at = new Date().toISOString(); patch.paid_by = 'webhook'; }
  else patch.notes = `paid amount ${amount} ${String(s.currency || '').toUpperCase()} does not match total ${o.total} MYR: check by hand`;
  if (o.status !== 'paid') await svc.entities.KtechOrder.update(o.id, patch);
  return new Response('ok', { status: 200 });
}

// Site feed request signing (11 Nov 2026, Security & Privacy review). Identical copy in the Bluehost Bridge and the
// Page One Controller. HMAC-SHA256 with its own secret SITE_FEED_HMAC_KEY (base64 of at least 32 random bytes),
// read from the app's environment only. It is not BRIDGE_API_KEY and not a BridgeKey row.
// Signed string: "site-feed-v1\n<unix seconds>\n<nonce: 32 hex>\n<sha256 hex of the exact body>".
// Headers: X-Feed-Ts, X-Feed-Nonce, X-Feed-Sig (64 hex).

export const FEED_MAX_AGE_S = 300;          // older (or further in the future) than 5 minutes: rejected
export const FEED_MAX_BODY = 3_000_000;     // bytes
const enc = new TextEncoder();

// The secret as bytes, or null when missing/short (callers then fail closed).
export function feedKeyBytes(raw: string | null | undefined): Uint8Array | null {
  if (!raw) return null;
  try {
    const b = atob(raw.trim().replace(/-/g, '+').replace(/_/g, '/'));
    const out = Uint8Array.from(b, (c) => c.charCodeAt(0));
    return out.length >= 32 ? out : null;
  } catch { return null; }
}

const hex = (buf: ArrayBuffer) => [...new Uint8Array(buf)].map((x) => x.toString(16).padStart(2, '0')).join('');
export async function sha256Hex(s: string): Promise<string> { return hex(await crypto.subtle.digest('SHA-256', enc.encode(s))); }
export const canonical = (ts: string, nonce: string, bodyHash: string) => `site-feed-v1\n${ts}\n${nonce}\n${bodyHash}`;

async function hmacHex(key: Uint8Array, msg: string): Promise<string> {
  const k = await crypto.subtle.importKey('raw', key as BufferSource, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return hex(await crypto.subtle.sign('HMAC', k, enc.encode(msg)));
}

// Constant-time compare of two hex strings (time does not depend on where they differ).
export function timingSafeEqualHex(a: string, b: string): boolean {
  const x = enc.encode(a), y = enc.encode(b);
  let diff = x.length ^ y.length;
  for (let i = 0; i < Math.max(x.length, y.length); i++) diff |= (x[i] ?? 0) ^ (y[i] ?? 0);
  return diff === 0;
}

// Bridge side: headers for one request.
export async function signFeed(key: Uint8Array, body: string, nowMs = Date.now()): Promise<Record<string, string>> {
  const ts = String(Math.floor(nowMs / 1000));
  const nonce = hex(crypto.getRandomValues(new Uint8Array(16)).buffer);
  const sig = await hmacHex(key, canonical(ts, nonce, await sha256Hex(body)));
  return { 'X-Feed-Ts': ts, 'X-Feed-Nonce': nonce, 'X-Feed-Sig': sig };
}

export type FeedCheck = { ok: true; body: string; nonce: string } | { ok: false; status: 401 | 413 | 503; reason: string };

// Controller side. Order matters:
//  1. no secret configured -> 503 (fail closed)
//  2. missing or malformed headers, or timestamp outside 5 minutes -> 401, before the body is read
//  3. declared body too large -> 413, before the body is read
//  4. body read (capped), HMAC checked in constant time -> 401 on mismatch
//  5. nonce already used -> 401 (checked only after a valid signature, so unsigned calls cannot fill the store)
// `reason` is for our own counters only; never send it, or any input, back to the caller.
export async function verifyFeed(
  headers: Headers, readBody: () => Promise<string>,
  opts: { key: Uint8Array | null; nowMs?: number; useNonce: (nonce: string) => Promise<boolean> },
): Promise<FeedCheck> {
  if (!opts.key) return { ok: false, status: 503, reason: 'no_key' };
  const ts = headers.get('x-feed-ts') || '', nonce = headers.get('x-feed-nonce') || '', sig = headers.get('x-feed-sig') || '';
  if (!/^\d{9,11}$/.test(ts) || !/^[0-9a-f]{32}$/.test(nonce) || !/^[0-9a-f]{64}$/.test(sig)) return { ok: false, status: 401, reason: 'unsigned' };
  const age = Math.abs((opts.nowMs ?? Date.now()) / 1000 - Number(ts));
  if (!(age <= FEED_MAX_AGE_S)) return { ok: false, status: 401, reason: 'stale' };
  if (Number(headers.get('content-length') || 0) > FEED_MAX_BODY) return { ok: false, status: 413, reason: 'too_large' };
  const body = await readBody();
  if (enc.encode(body).length > FEED_MAX_BODY) return { ok: false, status: 413, reason: 'too_large' };
  const want = await hmacHex(opts.key, canonical(ts, nonce, await sha256Hex(body)));
  if (!timingSafeEqualHex(want, sig)) return { ok: false, status: 401, reason: 'bad_sig' };
  if (!(await opts.useNonce(nonce))) return { ok: false, status: 401, reason: 'replay' };
  return { ok: true, body, nonce };
}

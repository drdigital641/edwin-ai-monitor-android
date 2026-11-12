// AutoSEO Admin app <-> Page One Controller signed link (13 Nov 2026). IDENTICAL copy in both apps
// (AutoSEO Admin base44/shared/linkAuth.ts and Controller base44/shared/linkAuth.ts).
//
// ECDSA P-256 / SHA-256. The AutoSEO Admin app holds the private key (made on its server on first use, never shown to
// anyone); the Controller holds only the public key, written in its code (shared/autoseoLinkKey.ts), so the
// Controller has no shared secret that could sign requests.
// Signed string: "autoseo-link-v1\n<unix seconds>\n<nonce: 32 hex>\n<sha256 hex of the exact body>".
// Headers: X-Link-Ts, X-Link-Nonce, X-Link-Sig (base64url of the 64-byte r||s signature).

export const LINK_MAX_AGE_S = 120;        // older (or further in the future) than 2 minutes: rejected
export const LINK_MAX_BODY = 20_000;      // bytes; the largest call (new client with 5,000-char notes) is far below
const enc = new TextEncoder();
const ALG = { name: 'ECDSA', namedCurve: 'P-256' } as const;
const SIG = { name: 'ECDSA', hash: 'SHA-256' } as const;

const hex = (buf: ArrayBuffer) => [...new Uint8Array(buf)].map((x) => x.toString(16).padStart(2, '0')).join('');
export const b64u = (buf: ArrayBuffer) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
export const unb64u = (s: string) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)), (c) => c.charCodeAt(0));
export async function sha256Hex(s: string): Promise<string> { return hex(await crypto.subtle.digest('SHA-256', enc.encode(s))); }
export const canonical = (ts: string, nonce: string, bodyHash: string) => `autoseo-link-v1\n${ts}\n${nonce}\n${bodyHash}`;

// Public part only (kty, crv, x, y): anything else in a stored or pasted key is ignored.
export function publicPart(jwk: any) {
  if (!jwk || jwk.kty !== 'EC' || jwk.crv !== 'P-256' || typeof jwk.x !== 'string' || typeof jwk.y !== 'string') return null;
  return { kty: 'EC', crv: 'P-256', x: jwk.x, y: jwk.y };
}

// AutoSEO Admin app side: a new key pair, as JSON strings.
export async function generateLinkKey(): Promise<{ private_jwk: string; public_jwk: string }> {
  const kp = await crypto.subtle.generateKey(ALG, true, ['sign', 'verify']) as CryptoKeyPair;
  const priv = await crypto.subtle.exportKey('jwk', kp.privateKey);
  const pub = publicPart(await crypto.subtle.exportKey('jwk', kp.publicKey));
  return { private_jwk: JSON.stringify(priv), public_jwk: JSON.stringify(pub) };
}

// AutoSEO Admin app side: headers for one request.
export async function signLink(privateJwk: string, body: string, nowMs = Date.now()): Promise<Record<string, string>> {
  const key = await crypto.subtle.importKey('jwk', JSON.parse(privateJwk), ALG, false, ['sign']);
  const ts = String(Math.floor(nowMs / 1000));
  const nonce = hex(crypto.getRandomValues(new Uint8Array(16)).buffer);
  const sig = await crypto.subtle.sign(SIG, key, enc.encode(canonical(ts, nonce, await sha256Hex(body))));
  return { 'X-Link-Ts': ts, 'X-Link-Nonce': nonce, 'X-Link-Sig': b64u(sig) };
}

export type LinkCheck = { ok: true; body: string; nonce: string } | { ok: false; status: 401 | 413 | 503; reason: string };

// Controller side. Order matters (same order as the reviewed site feed check, shared/feedAuth.ts):
//  1. no public key configured -> 503 (fail closed)
//  2. missing or malformed headers, or timestamp outside 2 minutes -> 401, before the body is read
//  3. declared body too large -> 413, before the body is read
//  4. body read (capped), ECDSA signature checked -> 401 on mismatch
//  5. nonce already used -> 401 (checked only after a valid signature, so unsigned calls cannot fill the store)
// `reason` is for our own counters only; never send it, or any input, back to the caller.
export async function verifyLink(
  headers: Headers, readBody: () => Promise<string>,
  opts: { publicJwk: any; nowMs?: number; useNonce: (nonce: string) => Promise<boolean> },
): Promise<LinkCheck> {
  const pub = publicPart(opts.publicJwk);
  if (!pub) return { ok: false, status: 503, reason: 'no_key' };
  const ts = headers.get('x-link-ts') || '', nonce = headers.get('x-link-nonce') || '', sig = headers.get('x-link-sig') || '';
  if (!/^\d{9,11}$/.test(ts) || !/^[0-9a-f]{32}$/.test(nonce) || !/^[A-Za-z0-9_-]{86}$/.test(sig)) return { ok: false, status: 401, reason: 'unsigned' };
  const age = Math.abs((opts.nowMs ?? Date.now()) / 1000 - Number(ts));
  if (!(age <= LINK_MAX_AGE_S)) return { ok: false, status: 401, reason: 'stale' };
  if (Number(headers.get('content-length') || 0) > LINK_MAX_BODY) return { ok: false, status: 413, reason: 'too_large' };
  const body = await readBody();
  if (enc.encode(body).length > LINK_MAX_BODY) return { ok: false, status: 413, reason: 'too_large' };
  let good = false;
  try {
    const key = await crypto.subtle.importKey('jwk', pub, ALG, false, ['verify']);
    good = await crypto.subtle.verify(SIG, key, unb64u(sig), enc.encode(canonical(ts, nonce, await sha256Hex(body))));
  } catch { good = false; }
  if (!good) return { ok: false, status: 401, reason: 'bad_sig' };
  if (!(await opts.useNonce(nonce))) return { ok: false, status: 401, reason: 'replay' };
  return { ok: true, body, nonce };
}

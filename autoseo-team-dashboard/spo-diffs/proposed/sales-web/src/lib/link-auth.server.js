// Signed server-to-server link from the AutoSEO team dashboard (Base44 app "AutoSEO Admin") to this app (21 Nov 2026).
// Same scheme as the reviewed Controller link (AutoSEO Admin base44/shared/linkAuth.ts): ECDSA P-256 / SHA-256.
// The dashboard holds the private key on its server; this app holds only the PUBLIC key (autoseo-link-key.server.js).
// Signed string: "autoseo-link-v1\n<unix seconds>\n<nonce: 32 hex>\n<sha256 hex of the exact body>".
// Order: no key -> 503 (fail closed); bad/missing headers or >2 min old -> 401 before the body is read; too large -> 413;
// signature -> 401; nonce used before -> 401. The reason is never sent back.
export const LINK_MAX_AGE_S = 120;
export const LINK_MAX_BODY = 20000;
const enc = new TextEncoder();
const ALG = { name: "ECDSA", namedCurve: "P-256" };
const SIG = { name: "ECDSA", hash: "SHA-256" };
const hex = (buf) => [...new Uint8Array(buf)].map((x) => x.toString(16).padStart(2, "0")).join("");
const unb64u = (s) => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/") + "===".slice((s.length + 3) % 4)), (c) => c.charCodeAt(0));
const sha256Hex = async (s) => hex(await crypto.subtle.digest("SHA-256", enc.encode(s)));
const canonical = (ts, nonce, h) => `autoseo-link-v1\n${ts}\n${nonce}\n${h}`;

export function publicPart(jwk) {
  if (!jwk || jwk.kty !== "EC" || jwk.crv !== "P-256" || typeof jwk.x !== "string" || typeof jwk.y !== "string") return null;
  return { kty: "EC", crv: "P-256", x: jwk.x, y: jwk.y };
}

export async function verifyLink(headers, readBody, { publicJwk, useNonce, nowMs }) {
  const pub = publicPart(publicJwk);
  if (!pub) return { ok: false, status: 503 };
  const ts = headers.get("x-link-ts") || "", nonce = headers.get("x-link-nonce") || "", sig = headers.get("x-link-sig") || "";
  if (!/^\d{9,11}$/.test(ts) || !/^[0-9a-f]{32}$/.test(nonce) || !/^[A-Za-z0-9_-]{86}$/.test(sig)) return { ok: false, status: 401 };
  const age = Math.abs((nowMs ?? Date.now()) / 1000 - Number(ts));
  if (!(age <= LINK_MAX_AGE_S)) return { ok: false, status: 401 };
  if (Number(headers.get("content-length") || 0) > LINK_MAX_BODY) return { ok: false, status: 413 };
  const body = await readBody();
  if (enc.encode(body).length > LINK_MAX_BODY) return { ok: false, status: 413 };
  let good = false;
  try {
    const key = await crypto.subtle.importKey("jwk", pub, ALG, false, ["verify"]);
    good = await crypto.subtle.verify(SIG, key, unb64u(sig), enc.encode(canonical(ts, nonce, await sha256Hex(body))));
  } catch { good = false; }
  if (!good) return { ok: false, status: 401 };
  if (!(await useNonce(nonce))) return { ok: false, status: 401 };
  return { ok: true, body };
}

// The signed payload, strictly. Audience must be this app; login is never possible over the link.
export const LINK_ACTIONS = ["data", "add", "remove", "settings"];
export function cleanLinkPayload(raw) {
  let p; try { p = JSON.parse(raw); } catch { return null; }
  if (!p || typeof p !== "object" || Array.isArray(p)) return null;
  if (p.v !== 1 || p.aud !== "autoseo-sales") return null;
  const actor = String(p.actor || "").trim().toLowerCase();
  if (!/^[^@\s]{1,64}@[^@\s]{1,190}$/.test(actor)) return null;
  if (!LINK_ACTIONS.includes(String(p.action))) return null;
  const args = p.args && typeof p.args === "object" && !Array.isArray(p.args) ? p.args : {};
  return { actor, action: String(p.action), args };
}

// Data endpoint for the internal page https://autoseo.my/sales/
// Nothing is returned without a session token. POST {action:"login", password} gives a token
// (password = Base44 secret SALES_EDIT_PIN). Every other action needs {token}.
// 21 Nov 2026: the AutoSEO team dashboard (Base44 app "AutoSEO Admin") reaches the SAME data server-to-server with a
// signed link (X-Link-* headers, link-auth.server.js). No PIN or token is involved on that path, and the /sales page
// path below is unchanged.
import { createFileRoute } from "@tanstack/react-router";
import { MAX_NODES, ROLES, cleanName, listAll } from "@/lib/sales-web.server";
import { authorised, checkSettings, login, readSettings, saveSettings } from "@/lib/sales-auth.server";
import { verifyLink, cleanLinkPayload } from "@/lib/link-auth.server";
import { AUTOSEO_ADMIN_LINK_PUBLIC_JWK } from "@/lib/autoseo-link-key.server";

const ALLOWED_ORIGINS = ["https://autoseo.my", "https://www.autoseo.my"];
const NONCE_KEEP_MS = 10 * 60 * 1000;

function cors(request) {
  const origin = request.headers.get("origin") || "";
  const h = {
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "600",
    "Cache-Control": "no-store",
    "X-Robots-Tag": "noindex, nofollow",
    Vary: "Origin",
  };
  if (ALLOWED_ORIGINS.includes(origin)) h["Access-Control-Allow-Origin"] = origin;
  return h;
}

const json = (request, body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors(request), "Content-Type": "application/json" } });

const clean = (n) => ({ id: n.id, name: n.name, role: n.role, parentId: n.parentId || "" });

// The four data actions, shared by both paths. Returns [body, status].
async function act(svc, action, body) {
  const all = await listAll(svc.entities);
  const byId = new Map(all.map((n) => [n.id, n]));

  if (action === "data") {
    return [{ ok: true, nodes: all.map(clean), settings: await readSettings(svc) }, 200];
  }

  if (action === "settings") {
    const r = checkSettings(body.settings);
    if (r.error) return [{ ok: false, error: r.error }, 400];
    await saveSettings(svc, r.settings);
    return [{ ok: true, settings: r.settings }, 200];
  }

  if (action === "add") {
    const name = cleanName(body.name);
    const role = ROLES.includes(String(body.role)) ? String(body.role) : "salesperson";
    const parent = byId.get(String(body.parentId || ""));
    if (!name) return [{ ok: false, error: "name" }, 400];
    if (!parent) return [{ ok: false, error: "parent" }, 400];
    if (all.length >= MAX_NODES) return [{ ok: false, error: "full" }, 400];
    const created = await svc.entities.SalesNode.create({
      name,
      role: parent.role === "centre" ? role : "salesperson",
      parentId: parent.id,
      createdAt: new Date().toISOString(),
    });
    return [{ ok: true, node: clean(created) }, 200];
  }

  if (action === "remove") {
    const node = byId.get(String(body.id || ""));
    if (!node) return [{ ok: false, error: "missing" }, 404];
    if (node.role === "centre") return [{ ok: false, error: "centre" }, 400];
    // Referrals move up one level to the removed node's parent.
    const kids = all.filter((n) => n.parentId === node.id);
    const parentIsCentre = byId.get(node.parentId)?.role === "centre";
    for (const k of kids) {
      await svc.entities.SalesNode.update(k.id, { parentId: node.parentId, role: parentIsCentre ? k.role : "salesperson" });
    }
    await svc.entities.SalesNode.delete(node.id);
    return [{ ok: true, moved: kids.length }, 200];
  }

  return [{ ok: false, error: "action" }, 400];
}

// Signed path (AutoSEO team dashboard server only). Fails closed while no public key is set.
async function linked(request, svc) {
  const out = (body, status) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
  const N = svc.entities.LinkNonce;
  const check = await verifyLink(request.headers, () => request.text(), {
    publicJwk: AUTOSEO_ADMIN_LINK_PUBLIC_JWK,
    useNonce: async (nonce) => {
      const seen = await N.filter({ nonce }).catch(() => [{}]);
      if (seen && seen.length) return false;
      return N.create({ nonce, at: new Date().toISOString() }).then(() => true, () => false);
    },
  });
  if (!check.ok) return out({ ok: false, error: check.status === 503 ? "off" : "auth" }, check.status);
  N.filter({ at: { $lt: new Date(Date.now() - NONCE_KEEP_MS).toISOString() } })
    .then((old) => Promise.all((old || []).slice(0, 50).map((r) => N.delete(r.id).catch(() => null)))).catch(() => null);
  const p = cleanLinkPayload(check.body);
  if (!p) return out({ ok: false, error: "action" }, 400);
  const [body, status] = await act(svc, p.action, p.args);
  return out(body, status);
}

export const Route = createFileRoute("/api/sales-web")({
  server: {
    handlers: {
      OPTIONS: async ({ request }) => new Response(null, { status: 204, headers: cors(request) }),

      GET: async ({ request }) => json(request, { ok: false, error: "auth" }, 401),

      POST: async ({ request, context }) => {
        if (request.headers.get("x-link-sig")) return linked(request, context.getBase44().asServiceRole);

        const origin = request.headers.get("origin") || "";
        if (!ALLOWED_ORIGINS.includes(origin)) return json(request, { ok: false, error: "origin" }, 403);

        let body;
        try {
          body = await request.json();
        } catch {
          return json(request, { ok: false, error: "bad_json" }, 400);
        }
        const svc = context.getBase44().asServiceRole;
        const action = String(body.action || "");

        if (action === "login") {
          const r = await login(svc, body.password);
          if (r.error === "off") return json(request, { ok: false, error: "off" }, 503);
          if (r.error === "locked") return json(request, { ok: false, error: "locked" }, 429);
          if (r.error) return json(request, { ok: false, error: "wrong" }, 401);
          return json(request, { ok: true, token: r.token, hours: r.hours });
        }

        if (!(await authorised(body.token))) return json(request, { ok: false, error: "auth" }, 401);

        const [res, status] = await act(svc, action, body);
        return json(request, res, status);
      },
    },
  },
});

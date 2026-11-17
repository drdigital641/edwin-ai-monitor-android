// Public data endpoint for the internal page https://autoseo.my/sales/
// GET  -> the commission network (anyone with the link may view)
// POST -> add / remove nodes, only with the edit PIN (Base44 secret SALES_EDIT_PIN, never in page source)
import { createFileRoute } from "@tanstack/react-router";
import { secrets } from "base44:runtime";

const ALLOWED_ORIGINS = ["https://autoseo.my", "https://www.autoseo.my"];
const MAX_NODES = 500;
const MAX_FAILS = 10; // wrong PINs allowed per window, across everyone
const WINDOW_MS = 15 * 60 * 1000;
const ROLES = ["dealer", "salesperson"];

function cors(request) {
  const origin = request.headers.get("origin") || "";
  const h = {
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
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

const clean = (n) => ({
  id: n.id,
  name: n.name,
  role: n.role,
  parentId: n.parentId || "",
  createdAt: n.createdAt || n.created_date || "",
});

async function sha256(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return new Uint8Array(buf);
}

async function pinMatches(given, expected) {
  const a = await sha256(String(given || ""));
  const b = await sha256(String(expected || ""));
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

function cleanName(v) {
  return String(v || "")
    // eslint-disable-next-line no-control-regex
    .replace(/[\u0000-\u001f\u007f<>]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 60);
}

async function listAll(entities) {
  return (await entities.SalesNode.list("createdAt", MAX_NODES + 50)) || [];
}

async function guardRow(svc) {
  const rows = await svc.entities.EditGuard.filter({ key: "global" });
  if (rows && rows[0]) return rows[0];
  return svc.entities.EditGuard.create({ key: "global", fails: 0, windowStart: new Date().toISOString() });
}

export const Route = createFileRoute("/api/sales-web")({
  server: {
    handlers: {
      OPTIONS: async ({ request }) => new Response(null, { status: 204, headers: cors(request) }),

      GET: async ({ request, context }) => {
        const rows = await listAll(context.getBase44().entities);
        return json(request, { ok: true, nodes: rows.map(clean) });
      },

      POST: async ({ request, context }) => {
        const origin = request.headers.get("origin") || "";
        if (!ALLOWED_ORIGINS.includes(origin)) return json(request, { ok: false, error: "origin" }, 403);

        let body;
        try {
          body = await request.json();
        } catch {
          return json(request, { ok: false, error: "bad_json" }, 400);
        }
        const svc = context.getBase44().asServiceRole;

        const expected = secrets.get("SALES_EDIT_PIN");
        if (!expected || String(expected).length < 6) return json(request, { ok: false, error: "edit_off" }, 503);

        // Lock-out: too many wrong PINs in the window refuses every edit until the window ends.
        const guard = await guardRow(svc);
        const now = Date.now();
        let fails = Number(guard.fails || 0);
        let windowStart = Date.parse(guard.windowStart || "") || now;
        if (now - windowStart > WINDOW_MS) {
          fails = 0;
          windowStart = now;
        }
        if (fails >= MAX_FAILS) return json(request, { ok: false, error: "locked" }, 429);

        if (!(await pinMatches(body.pin, expected))) {
          await svc.entities.EditGuard.update(guard.id, { fails: fails + 1, windowStart: new Date(windowStart).toISOString() });
          return json(request, { ok: false, error: "wrong_pin" }, 401);
        }

        const action = String(body.action || "");
        if (action === "check") return json(request, { ok: true });

        const all = await listAll(svc.entities);
        const byId = new Map(all.map((n) => [n.id, n]));

        if (action === "add") {
          const name = cleanName(body.name);
          const role = String(body.role || "");
          const parent = byId.get(String(body.parentId || ""));
          if (!name) return json(request, { ok: false, error: "name" }, 400);
          if (!ROLES.includes(role)) return json(request, { ok: false, error: "role" }, 400);
          if (!parent) return json(request, { ok: false, error: "parent" }, 400);
          // From a person node, the +1 is always a referral (a salesperson they brought in).
          if (parent.role !== "centre" && role !== "salesperson") return json(request, { ok: false, error: "role" }, 400);
          if (all.length >= MAX_NODES) return json(request, { ok: false, error: "full" }, 400);
          const created = await svc.entities.SalesNode.create({
            name,
            role,
            parentId: parent.id,
            createdAt: new Date().toISOString(),
          });
          return json(request, { ok: true, node: clean(created) });
        }

        if (action === "remove") {
          const node = byId.get(String(body.id || ""));
          if (!node) return json(request, { ok: false, error: "missing" }, 404);
          if (node.role === "centre") return json(request, { ok: false, error: "centre" }, 400);
          const mode = body.children === "branch" ? "branch" : "lift";
          const kids = all.filter((n) => n.parentId === node.id);
          if (mode === "lift") {
            // Referrals move up one level to the removed node's parent.
            for (const k of kids) {
              const newRole = node.parentId && byId.get(node.parentId)?.role === "centre" ? k.role : "salesperson";
              await svc.entities.SalesNode.update(k.id, { parentId: node.parentId, role: newRole });
            }
            await svc.entities.SalesNode.delete(node.id);
            return json(request, { ok: true, removed: 1, moved: kids.length });
          }
          const doomed = [];
          const walk = (id) => {
            doomed.push(id);
            all.filter((n) => n.parentId === id).forEach((c) => walk(c.id));
          };
          walk(node.id);
          for (const id of doomed) await svc.entities.SalesNode.delete(id);
          return json(request, { ok: true, removed: doomed.length, moved: 0 });
        }

        return json(request, { ok: false, error: "action" }, 400);
      },
    },
  },
});

# Applies the GROKBOT RUNNER edits to existing Bridge files; every edit must match exactly once.
import sys, os
root = sys.argv[1]
def edit(path, pairs):
    f = os.path.join(root, path); t = open(f).read()
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, (path, n, old[:80])
        t = t.replace(old, new)
    open(f, 'w').write(t); print('edited', path)

edit('base44/shared/keys.ts', [
("// 'needs': Grok Bot, read the needs-you list only (15 Nov 2026).\nexport type KeyScope = 'full' | 'overview' | 'drop' | 'needs' | `site:${string}`;",
 "// 'needs': Grok Bot, read the needs-you list only (15 Nov 2026).\n// 'runner': the Grok Bot API runner (18 Nov 2026), named client sites only, see runner.ts.\nexport type KeyScope = 'full' | 'overview' | 'drop' | 'needs' | 'runner' | `site:${string}`;"),
("  if (raw === 'drop') return 'drop';\n", "  if (raw === 'drop') return 'drop';\n  if (raw === 'runner') return 'runner';\n"),
("scope === 'needs' ? 'Grok Bot (needs list, read only)' : scope.slice(5) + ' automation';",
 "scope === 'needs' ? 'Grok Bot (needs list, read only)' : scope === 'runner' ? 'grokbot-runner' : scope.slice(5) + ' automation';"),
])

edit('base44/shared/handler.ts', [
("import { addNeedsYou } from './needsYou.ts';\n",
 "import { addNeedsYou } from './needsYou.ts';\nimport { RUNNER_KEY_ACTIONS, RUNNER_SITES, RUNNER_LABEL, RUNNER_ACTOR_EMAIL } from './runner.ts';\n"),
("const NEEDS_KEY_ACTIONS = new Set(['needs_read']);\n",
 "const NEEDS_KEY_ACTIONS = new Set(['needs_read']);\n// GROKBOT RUNNER (18 Nov 2026): the runner key (scope 'runner') may run RUNNER_KEY_ACTIONS on RUNNER_SITES only (runner.ts).\nconst RUNNER_ACTOR = { email: RUNNER_ACTOR_EMAIL, role: 'admin' };\n"),
("          await authLog(base44, { endpoint: action, allowed: false, reason, source, ...extra });\n",
 "          await authLog(base44, { endpoint: action, allowed: false, reason, source, ...extra });\n          if (info?.scope === 'runner') await runnerLog(base44, action, false, reason, started);\n"),
("        if (scope === 'needs' && !NEEDS_KEY_ACTIONS.has(action)) {\n          return await deny('This key can only read the needs-you list', 403, authMeta);\n        }\n",
 "        if (scope === 'needs' && !NEEDS_KEY_ACTIONS.has(action)) {\n          return await deny('This key can only read the needs-you list', 403, authMeta);\n        }\n        if (scope === 'runner' && !RUNNER_KEY_ACTIONS.has(action)) {\n          return await deny('The runner key cannot use this tool (allowed: list, read, write, write_many, sitemap, IndexNow, Controller reads, article image)', 403, authMeta);\n        }\n"),
("        } else {\n          user = scope === 'overview' ? OVERVIEW_ACTOR",
 "        } else if (scope === 'runner') {\n          user = RUNNER_ACTOR;\n        } else {\n          user = scope === 'overview' ? OVERVIEW_ACTOR"),
("      if (siteOnly && body.site !== siteOnly) throw new BridgeError('This key only works for the ' + siteOnly + ' site', 403);\n",
 "      if (siteOnly && body.site !== siteOnly) throw new BridgeError('This key only works for the ' + siteOnly + ' site', 403);\n      if (user === RUNNER_ACTOR && opts.needsSite !== false && !RUNNER_SITES.includes(body.site)) throw new BridgeError('The runner key does not work for site ' + body.site, 403);\n"),
("const agent = (user === KEY_ACTOR ? 'chatgpt' : siteOnly || dropKey ? 'automation' : 'claude') as Agent;",
 "const agent = (user === KEY_ACTOR ? 'chatgpt' : siteOnly || dropKey || user === RUNNER_ACTOR ? 'automation' : 'claude') as Agent;"),
("const viaKey = user === KEY_ACTOR || user === OVERVIEW_ACTOR || user === NEEDS_ACTOR || Boolean(siteOnly) || Boolean(dropKey);",
 "const viaKey = user === KEY_ACTOR || user === OVERVIEW_ACTOR || user === NEEDS_ACTOR || user === RUNNER_ACTOR || Boolean(siteOnly) || Boolean(dropKey);"),
("      if (opts.logs) await audit(base44, user, action, body, true, result, null, started);",
 "      if (opts.logs || user === RUNNER_ACTOR) await audit(base44, user, action, body, true, result, null, started);"),
("      if (opts.logs && base44 && user) await audit(base44, user, action, body, false, null, message, started);",
 "      if ((opts.logs || user === RUNNER_ACTOR) && base44 && user) await audit(base44, user, action, body, false, null, message, started);"),
("      error, actor: user?.email || null, duration_ms: Date.now() - started,\n    });\n  } catch { /* logging must never block a verified write result */ }\n}",
 "      error, actor: user?.email || null, duration_ms: Date.now() - started,\n      ...(user?.email === RUNNER_ACTOR_EMAIL ? { label: RUNNER_LABEL, detail: runnerDetail(body) } : {}),\n    });\n  } catch { /* logging must never block a verified write result */ }\n}\n\n// What a runner call asked for, without file contents, prompts or keys (counts and short ids only).\nfunction runnerDetail(body: any): string {\n  const d: Record<string, unknown> = {};\n  if (typeof body?.op === 'string') d.op = body.op.slice(0, 20);\n  if (typeof body?.slug === 'string') d.slug = body.slug.slice(0, 80);\n  for (const k of ['paths', 'urls', 'files']) if (Array.isArray(body?.[k])) d[k] = body[k].length;\n  if (body?.dry_run === true) d.dry_run = true;\n  return JSON.stringify(d);\n}\n\n// BridgeLog row for a runner call refused before it ran (wrong tool or session-only tool).\nasync function runnerLog(base44: any, action: string, ok: boolean, error: string, started: number) {\n  try {\n    await base44.asServiceRole.entities.BridgeLog.create({ action, ok, error: error.slice(0, 300), actor: RUNNER_ACTOR_EMAIL, label: RUNNER_LABEL, duration_ms: Date.now() - started });\n  } catch { /* never block a refusal */ }\n}"),
])

edit('base44/shared/heroImage.ts', [
("const NO_TEXT = 'No text,", "export const NO_TEXT = 'No text,"),
("function sgtNow() {", "export function sgtNow() {"),
("async function base44Image(", "export async function base44Image("),
("async function fetchImage(", "export async function fetchImage("),
("async function readState(", "export async function readState("),
("async function writeState(", "export async function writeState("),
])

edit('base44/shared/autoSitemapRun.ts', [
("async function findIndexNowKey(", "export async function findIndexNowKey("),
("async function sendIndexNow(", "export async function sendIndexNow("),
])

edit('base44/entities/BridgeKey.jsonc', [
('drop = a bot may only put files in the private drop folder and read drop status."',
 'drop = a bot may only put files in the private drop folder and read drop status. needs = Grok Bot reads the needs-you list only. runner = grokbot-runner (18 Nov 2026): list/read/write live files of the named client sites (base sha256 required to replace), sitemap.xml + llms.txt rebuild, IndexNow, Controller Copy fix + tap reads, article_last update, article images; no deletes, .htaccess, credentials, DB, Bridge config or Publish."'),
('        "drop",\n', '        "drop",\n        "needs",\n        "runner",\n'),
])

edit('base44/entities/BridgeLog.jsonc', [
('        "restore"\n      ],', '        "restore",\n        "list",\n        "read",\n        "write_many",\n        "runner_sitemap",\n        "runner_indexnow",\n        "runner_controller",\n        "runner_image"\n      ],'),
('    "detail": {\n', '    "label": {\n      "type": "string",\n      "description": "Who made the call when it was a named runner, e.g. grokbot-runner (every runner call is logged, allowed or refused)"\n    },\n    "detail": {\n'),
])

edit('src/pages/Connect.jsx', [
('''      const res = await base44.functions.invoke("bridgeKey", scope === "needs"
        ? { action: "create", scope: "needs", label: "Grok Bot (needs list, read only)" }
        : { action: "create", label: "ChatGPT" });''',
'''      const res = await base44.functions.invoke("bridgeKey", scope === "needs"
        ? { action: "create", scope: "needs", label: "Grok Bot (needs list, read only)" }
        : scope === "runner"
          ? { action: "create", scope: "runner", label: "grokbot-runner" }
          : { action: "create", label: "ChatGPT" });'''),
('setFresh(body.key); setFreshScope(scope === "needs" ? "needs" : "full");',
 'setFresh(body.key); setFreshScope(scope === "needs" || scope === "runner" ? scope : "full");'),
('''          <KeyRound className="mr-1.5 h-4 w-4" />Generate Grok Bot key (read needs-you list only)
        </Button>
''',
'''          <KeyRound className="mr-1.5 h-4 w-4" />Generate Grok Bot key (read needs-you list only)
        </Button>
        <Button size="sm" variant="outline" onClick={() => create("runner")} disabled={busy}>
          <KeyRound className="mr-1.5 h-4 w-4" />Generate Grok Bot runner key (client sites, no deletes)
        </Button>
'''),
('''            ? "Copy this key now. It is shown only once. It can only read the needs-you list (send it as X-Bridge-Key to bridgeNeedsList)."
            : "Copy this key now.''',
'''            ? "Copy this key now. It is shown only once. It can only read the needs-you list (send it as X-Bridge-Key to bridgeNeedsList)."
            : freshScope === "runner"
              ? "Copy this key now. It is shown only once. Paste it into Website Manager's secure box as BRIDGE_RUNNER_KEY. It reads and writes the named client sites only (no deletes, no .htaccess, no keys); every call is logged as grokbot-runner."
              : "Copy this key now.'''),
])

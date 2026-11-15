#!/usr/bin/env python3
# Applies the NEEDS YOU change to a Bridge tree (run with cwd = tree root, after copying the new files from this folder).
# Every replacement asserts its old text exists exactly once, so a moved Bridge head fails loudly instead of half-applying.
import json, sys

def rep(path, old, new):
    s = open(path).read()
    if s.count(old) != 1: sys.exit('APPLY FAILED: %s: expected 1 match, got %d for %r' % (path, s.count(old), old[:60]))
    open(path, 'w').write(s.replace(old, new, 1))

rep('base44/shared/handler.ts', """const OVERVIEW_ACTOR = { email: 'pageone-controller (overview key)', role: 'admin' };""", """const OVERVIEW_ACTOR = { email: 'pageone-controller (overview key)', role: 'admin' };
// NEEDS YOU (15 Nov 2026): a "needs" key (Grok Bot) may only read the needs-you list.
const NEEDS_ACTOR = { email: 'grokbot (needs key)', role: 'admin' };
const NEEDS_KEY_ACTIONS = new Set(['needs_read']);""")
rep('base44/shared/handler.ts', """        if (scope.startsWith('site:')) {""", """        if (scope === 'needs' && !NEEDS_KEY_ACTIONS.has(action)) {
          return await deny('This key can only read the needs-you list', 403, authMeta);
        }
        if (scope.startsWith('site:')) {""")
rep('base44/shared/handler.ts', """          user = scope === 'overview' ? OVERVIEW_ACTOR : KEY_ACTOR;""", """          user = scope === 'overview' ? OVERVIEW_ACTOR : scope === 'needs' ? NEEDS_ACTOR : KEY_ACTOR;""")
rep('base44/shared/handler.ts', """const viaKey = user === KEY_ACTOR || user === OVERVIEW_ACTOR || Boolean(siteOnly) || Boolean(dropKey);""", """const viaKey = user === KEY_ACTOR || user === OVERVIEW_ACTOR || user === NEEDS_ACTOR || Boolean(siteOnly) || Boolean(dropKey);""")

rep('base44/shared/keys.ts', """export type KeyScope = 'full' | 'overview' | 'drop' | `site:${string}`;""", """// 'needs': Grok Bot, read the needs-you list only (15 Nov 2026).
export type KeyScope = 'full' | 'overview' | 'drop' | 'needs' | `site:${string}`;""")
rep('base44/shared/keys.ts', """  if (raw === 'overview') return 'overview';""", """  if (raw === 'overview') return 'overview';
  if (raw === 'needs') return 'needs';""")
rep('base44/shared/keys.ts', """const fallback = scope === 'overview' ? 'Page One Controller' : scope === 'full' ? 'ChatGPT' : scope === 'drop' ? 'Bot drop key' : scope.slice(5) + ' automation';""", """const fallback = scope === 'overview' ? 'Page One Controller' : scope === 'full' ? 'ChatGPT' : scope === 'drop' ? 'Bot drop key' : scope === 'needs' ? 'Grok Bot (needs list, read only)' : scope.slice(5) + ' automation';""")

rep('src/pages/Connect.jsx', '''  const [fresh, setFresh] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    try {
      const res = await base44.functions.invoke("bridgeKey", { action: "list" });''', '''  const [fresh, setFresh] = useState(null);
  const [freshScope, setFreshScope] = useState("full");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    try {
      const res = await base44.functions.invoke("bridgeKey", { action: "list" });''')
rep('src/pages/Connect.jsx', '''  const create = async () => {
    setBusy(true); setError(null);
    try {
      const res = await base44.functions.invoke("bridgeKey", { action: "create", label: "ChatGPT" });
      const body = bodyOf(res);
      if (!body.key) throw new Error(body.error || "The key was not returned. Try again.");
      setFresh(body.key);''', '''  // scope "needs" = Grok Bot: reads the needs-you list only (15 Nov 2026).
  const create = async (scope) => {
    setBusy(true); setError(null);
    try {
      const res = await base44.functions.invoke("bridgeKey", scope === "needs"
        ? { action: "create", scope: "needs", label: "Grok Bot (needs list, read only)" }
        : { action: "create", label: "ChatGPT" });
      const body = bodyOf(res);
      if (!body.key) throw new Error(body.error || "The key was not returned. Try again.");
      setFresh(body.key); setFreshScope(scope === "needs" ? "needs" : "full");''')
rep('src/pages/Connect.jsx', '''      <Button size="sm" onClick={create} disabled={busy}>
        <KeyRound className="mr-1.5 h-4 w-4" />Generate ChatGPT key
      </Button>''', '''      <div className="flex flex-wrap gap-2">
        <Button size="sm" onClick={() => create("full")} disabled={busy}>
          <KeyRound className="mr-1.5 h-4 w-4" />Generate ChatGPT key
        </Button>
        <Button size="sm" variant="outline" onClick={() => create("needs")} disabled={busy}>
          <KeyRound className="mr-1.5 h-4 w-4" />Generate Grok Bot key (read needs-you list only)
        </Button>
      </div>''')
rep('src/pages/Connect.jsx', '''<p className="text-xs font-medium text-amber-900">Copy this key now. It is shown only once. Keep it private: it can change your live websites.</p>''', '''<p className="text-xs font-medium text-amber-900">{freshScope === "needs"
            ? "Copy this key now. It is shown only once. It can only read the needs-you list (send it as X-Bridge-Key to bridgeNeedsList)."
            : "Copy this key now. It is shown only once. Keep it private: it can change your live websites."}</p>''')

p = 'base44/mcp/config.json'; d = json.load(open(p)); fns = d['tools']['functions']
if any(f['name'] in ('needs_you', 'list_needs_you') for f in fns): sys.exit('APPLY FAILED: tools already present')
fns.extend(json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'mcp-tools.json')))
d['tools']['entity_overrides']['BridgeNeedsYou'] = {"operations": [], "description": None}
json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False); open(p, 'a').write('\n')
print('applied')

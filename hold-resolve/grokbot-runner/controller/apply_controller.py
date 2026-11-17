# Lets the Controller's own runnerFeed (CRON_KEY) read the dashboard status; every edit must match exactly once.
import sys, os
root = sys.argv[1]
f = os.path.join(root, 'base44/functions/portfolio/entry.ts'); t = open(f).read()
pairs = [
("  const pre = await preAuth(req, body, ['refresh', 'feed']);",
 "  // GROKBOT RUNNER (18 Nov 2026): 'runner_status' = the same read-only status, only for runnerFeed (CRON_KEY), which trims it.\n  const pre = await preAuth(req, body, ['refresh', 'feed', 'runner_status']);"),
("  const isStatus = action === 'status';", "  const isStatus = action === 'status' || action === 'runner_status';"),
("  if (!user && (!['refresh', 'feed'].includes(action) || !(await isCron(req, body)))) return Response.json({ error: 'Forbidden' }, { status: 403 });",
 "  if (!user && (!['refresh', 'feed', 'runner_status'].includes(action) || !(await isCron(req, body)))) return Response.json({ error: 'Forbidden' }, { status: 403 });"),
("  if (action === 'status') {\n    const newest", "  if (isStatus) {\n    const newest"),
]
for old, new in pairs:
    n = t.count(old); assert n == 1, (n, old[:70]); t = t.replace(old, new)
open(f, 'w').write(t); print('edited portfolio')

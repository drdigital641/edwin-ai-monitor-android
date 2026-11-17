// GROKBOT RUNNER runnerFeed tests (18 Nov 2026). Run: deno test -A --no-check base44/tests/runnerFeed.test.ts
// Fake SDK client (no network, no real key): unsigned outsiders refused, Copy fix + taps trimmed, article_last writes 3 fields only.
import { assertEquals } from 'jsr:@std/assert@1';

let me: any = null;
const updates: any[] = [];
const clients = [
  { id: 'c1', slug: 'carzy', domain: 'carzyworld.com.my', is_partner: false, whatsapp: '+60123456789' },
  { id: 'c2', slug: 'ktech', domain: 'ktech.my', is_partner: true },
];
const status = { refreshed_at: '2026-11-17T20:00:00Z', stale: false, sites: [
  { key: 'carzy', name: 'Carzy World', url: 'https://carzyworld.com.my/', action: { level: 'urgent', text: 'Home page down' }, issues: ['http 500'], health_score: 20,
    fix: { id: 'f', status: 'queued', issue: 'x', result: '', requested_at: 'r', finished_at: null, progress: 0 }, cta: { whatsapp: { today: 1, d7: 3 } }, wa_days: [{ day: '2026-11-17', n: 1 }],
    update: { number: '+60123456789', text: 'private message' }, wa_report: { text: 'private', link: 'https://wa.me/x' }, plan: { amount: 100 } },
  { key: 'sggarage', name: 'SG Garage', url: 'https://sggarage.com/', action: { level: 'ok', text: 'All good' }, cta: { whatsapp: { today: 0, d7: 9 } }, wa_days: [], enq_today: 0, enq_7d: 2 },
] };
(globalThis as any).__fake = {
  auth: { me: async () => me },
  asServiceRole: {
    entities: { Client: { filter: async (q: any) => clients.filter((c) => c.slug === q.slug), update: async (id: string, d: any) => { updates.push({ id, d }); return d; } } },
    functions: { invoke: async (_n: string, body: any) => ({ data: body.action === 'runner_status' ? status : null }) },
  },
};
const { default: fn } = await import('./runnerFeedUnderTest.ts');
const call = async (body: any) => { const r = await fn(new Request('https://x.test/f', { method: 'POST', body: JSON.stringify(body) })); return { status: r.status, body: await r.json() }; };

Deno.test('unsigned outsider refused; bad signature refused', async () => {
  me = null;
  assertEquals((await call({ op: 'taps' })).status, 403);
  assertEquals((await call({ payload: JSON.stringify({ purpose: 'grokbot_runner', op: 'taps', sent_at: new Date().toISOString() }), sig: 'AAAA', kid: 'nope' })).status, 403);
  me = { role: 'user' };
  assertEquals((await call({ op: 'taps' })).status, 403);
});

Deno.test('copy_fix: urgent/warn only, dashboard Copy fix text, no contacts', async () => {
  me = { role: 'admin' };
  const r = await call({ op: 'copy_fix' });
  assertEquals(r.status, 200); assertEquals(r.body.count, 1);
  assertEquals(r.body.issues[0].copy_fix.startsWith('Fix this issue on Carzy World (https://carzyworld.com.my/):'), true);
  const s = JSON.stringify(r.body);
  assertEquals(/private|wa\.me|\+6012|amount/.test(s), false);
});

Deno.test('taps: counts only, site filter', async () => {
  me = { role: 'admin' };
  const r = await call({ op: 'taps', site: 'sggarage' });
  assertEquals(r.body.count, 1); assertEquals(r.body.taps[0].enq_7d, 2);
  assertEquals(/private|wa\.me|\+6012/.test(JSON.stringify((await call({ op: 'taps' })).body)), false);
});

Deno.test('article_last: 3 fields only, own domain or preview host, partner/unknown refused', async () => {
  me = { role: 'admin' };
  assertEquals((await call({ op: 'article_last', slug: 'carzy', date: '2026-11-18', title: 'T', url: 'https://evil.example/a/' })).status, 400);
  assertEquals((await call({ op: 'article_last', slug: 'ktech', date: '2026-11-18', title: 'T', url: 'https://ktech.my/a/' })).status, 404);
  assertEquals((await call({ op: 'article_last', slug: 'nobody', date: '2026-11-18', title: 'T', url: 'https://x.my/a/' })).status, 404);
  assertEquals((await call({ op: 'article_last', slug: 'carzy', date: '18-11-2026', title: 'T', url: 'https://carzyworld.com.my/a/' })).status, 400);
  const r = await call({ op: 'article_last', slug: 'carzy', date: '2026-11-18', title: 'New article', url: 'https://www.carzyworld.com.my/articles/a/' });
  assertEquals(r.status, 200);
  assertEquals(Object.keys(updates.at(-1).d).sort(), ['article_last_built', 'article_last_title', 'article_last_url']);
  assertEquals((await call({ op: 'drop_table' })).status, 400);
});

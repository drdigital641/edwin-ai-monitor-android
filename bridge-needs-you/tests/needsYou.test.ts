// NEEDS YOU self-test (Edwin 15 Nov 2026 10:33am SGT): a test item fires exactly one webhook call, duplicates send nothing,
// done/list/resend send nothing, and the read tool hides secrets and file contents. In-memory base44 + fake webhook (no network).
// Run: deno test --no-check -A --import-map tests/importmap.json tests/needsYou.test.ts
import { addNeedsYou, listNeedsYou, markNeedsYouDone, resendNeedsYou, noticeRequest, cleanText } from '../base44/shared/needsYou.ts';
import { keyHash } from '../base44/shared/keys.ts';
import needsListEntry from '../base44/functions/bridgeNeedsList/entry.ts';
import needsEntry from '../base44/functions/bridgeNeedsYou/entry.ts';

const FAKE_URL = 'https://api.anthropic.com/v1/claude_code/routines/trig_TESTONLY000/fire';
const FAKE_KEY = 'sk-ant-oat01-FAKEKEYFORTESTSONLY1234567890abcdef';
(globalThis as any).__testSecrets = { GROKBOT_WEBHOOK_URL: FAKE_URL, GROKBOT_WEBHOOK_KEY: FAKE_KEY };

function fail(msg: string): never { throw new Error(msg); }
function eq(a: unknown, b: unknown, msg: string) { if (JSON.stringify(a) !== JSON.stringify(b)) fail(msg + ': got ' + JSON.stringify(a) + ', want ' + JSON.stringify(b)); }
function noSecret(text: string, msg: string) {
  for (const v of [FAKE_URL, FAKE_KEY, 'trig_TESTONLY000', 'FAKEKEYFORTESTSONLY']) if (text.includes(v)) fail(msg + ': leaked ' + v.slice(0, 6) + '...');
}

// In-memory entities with the SDK calls the bridge uses.
function makeDb() {
  const tables: Record<string, any[]> = {};
  let n = 0;
  const match = (r: any, q: any) => Object.entries(q || {}).every(([k, v]) => r[k] === v);
  const sortRows = (rows: any[], sort?: string) => {
    if (!sort) return rows;
    const desc = sort.startsWith('-'); const k = sort.replace(/^-/, '');
    return [...rows].sort((a, b) => (String(a[k]) < String(b[k]) ? -1 : String(a[k]) > String(b[k]) ? 1 : 0) * (desc ? -1 : 1));
  };
  const entity = (name: string) => {
    tables[name] ??= [];
    const t = tables[name];
    return {
      async create(data: any) { n++; const row = { id: 'row' + String(n).padStart(8, '0'), created_date: new Date(Date.now() + n).toISOString(), ...data }; t.push(row); return { ...row }; },
      async update(id: string, data: any) { const r = t.find((x) => x.id === id); if (!r) throw new Error('missing'); Object.assign(r, data); return { ...r }; },
      async delete(id: string) { const i = t.findIndex((x) => x.id === id); if (i >= 0) t.splice(i, 1); },
      async filter(q: any, sort?: string, limit = 50) { return sortRows(t.filter((r) => match(r, q)), sort).slice(0, limit).map((r) => ({ ...r })); },
      async list(sort?: string, limit = 50) { return sortRows(t, sort).slice(0, limit).map((r) => ({ ...r })); },
    };
  };
  const entities = new Proxy({}, { get: (_t, name: string) => entity(name) });
  const client = { asServiceRole: { entities }, auth: { me: async () => ({ email: 'claude-test@example.invalid', role: 'admin' }) } };
  return { client, tables };
}

// Fake webhook: counts calls, can answer slowly or with an error.
type Call = { url: string; headers: Record<string, string>; body: string };
let calls: Call[] = [];
let answer: 'ok' | 'http500' | 'hang' = 'ok';
const consoleLines: string[] = [];
for (const m of ['log', 'info', 'warn', 'error', 'debug'] as const) {
  const orig = console[m].bind(console);
  (console as any)[m] = (...a: unknown[]) => { consoleLines.push(a.map(String).join(' ')); orig(...a); };
}
globalThis.fetch = (async (input: any, init: any = {}) => {
  const headers: Record<string, string> = {};
  for (const [k, v] of Object.entries(init.headers || {})) headers[k.toLowerCase()] = String(v);
  calls.push({ url: String(input), headers, body: String(init.body || '') });
  if (answer === 'hang') {
    return await new Promise((_r, rej) => init.signal?.addEventListener('abort', () => rej(new DOMException('timeout', 'TimeoutError'))));
  }
  if (answer === 'http500') return new Response('{"type":"error"}', { status: 500 });
  return Response.json({ type: 'routine_fire', claude_code_session_id: 'session_test', claude_code_session_url: 'https://claude.ai/code/session_test' });
}) as any;

const ITEM = { type: 'publish', target: 'Bluehost Bridge', ref: '6af918157d3d4a734af8b2da', summary: 'Publish the weekly guard override checkpoint', why: 'Guard refuses the weekly sitemap refresh until published' };

Deno.test('a test item fires exactly one webhook call, routine format, key only in the header', async () => {
  const { client } = makeDb(); calls = []; answer = 'ok';
  const res = await addNeedsYou(client, ITEM, 'claude');
  eq(res.added, true, 'added'); eq(res.notice, 'sent', 'notice'); eq(calls.length, 1, 'webhook calls');
  const c = calls[0];
  eq(c.url, FAKE_URL, 'url'); eq(c.headers['authorization'], 'Bearer ' + FAKE_KEY, 'bearer');
  eq(c.headers['anthropic-version'], '2023-06-01', 'version'); eq(c.headers['anthropic-beta'], 'experimental-cc-routine-2026-04-01', 'beta');
  const body = JSON.parse(c.body); if (typeof body.text !== 'string') fail('routine body must be {text}');
  const notice = JSON.parse(body.text.slice(body.text.indexOf('{')));
  eq(Object.keys(notice).sort(), ['event', 'id', 'ref', 'source', 'summary', 'target', 'type'], 'notice fields');
  eq(notice.id, res.item.id, 'notice id'); eq(notice.type, 'publish', 'notice type');
  noSecret(c.body, 'notice body'); noSecret(JSON.stringify(res), 'add result');
});

Deno.test('the same open step again sends nothing (no duplicates), also with different case/spacing', async () => {
  const { client, tables } = makeDb(); calls = []; answer = 'ok';
  const a = await addNeedsYou(client, ITEM, 'claude');
  const b = await addNeedsYou(client, { ...ITEM, target: ' bluehost  BRIDGE ', ref: ITEM.ref.toUpperCase(), summary: 'Publish it again please' }, 'claude');
  eq(b.added, false, 'second add'); eq(b.duplicate, true, 'duplicate'); eq(b.item.id, a.item.id, 'same item');
  eq(calls.length, 1, 'still one webhook call'); eq(tables.BridgeNeedsYou.length, 1, 'one row');
});

Deno.test('two adds at the same moment: one row, one notice', async () => {
  const { client, tables } = makeDb(); calls = []; answer = 'ok';
  const [a, b] = await Promise.all([addNeedsYou(client, ITEM, 'claude'), addNeedsYou(client, ITEM, 'claude')]);
  eq([a.added, b.added].filter(Boolean).length, 1, 'one added');
  eq(tables.BridgeNeedsYou.filter((r) => r.status === 'open').length, 1, 'one open row');
  eq(calls.length, 1, 'one webhook call');
});

Deno.test('done and list send no notice; done needs live check + site re-check; a reopened step notifies once more', async () => {
  const { client } = makeDb(); calls = []; answer = 'ok';
  const a = await addNeedsYou(client, { type: 'server', target: 'commercialfitout.sg', ref: 'SGNIC VerifiedID@SG', summary: 'Complete VerifiedID@SG so the serverHold lifts', why: 'Domain is on serverHold, site is down' }, 'claude');
  eq(calls.length, 1, 'one call after add');
  let refused = false; try { await markNeedsYouDone(client, { id: a.item.id }, 'claude'); } catch { refused = true; }
  eq(refused, true, 'done without live check refused');
  const d = await markNeedsYouDone(client, { id: a.item.id, live_check: 'whois shows ok, NXDOMAIN gone', site_recheck: 'https://commercialfitout.sg/ 200, wa.me buttons present' }, 'claude');
  eq(d.item.status, 'done', 'done');
  await listNeedsYou(client, {}); await listNeedsYou(client, { id: a.item.id }); await listNeedsYou(client, { status: 'all' });
  eq(calls.length, 1, 'done/list sent nothing');
  const open = await listNeedsYou(client, {}); eq(open.count, 0, 'nothing open');
  const again = await addNeedsYou(client, { type: 'server', target: 'commercialfitout.sg', ref: 'SGNIC VerifiedID@SG', summary: 'Hold is back' }, 'claude');
  eq(again.added, true, 'new item after done'); eq(calls.length, 2, 'a real new need notifies');
});

Deno.test('failed / not configured / timeout: recorded without secrets; resend only when it never arrived', async () => {
  const { client } = makeDb(); calls = []; answer = 'http500';
  const a = await addNeedsYou(client, ITEM, 'claude');
  eq(a.notice, 'failed', 'failed'); eq(calls.length, 1, 'one attempt, no auto retry'); noSecret(JSON.stringify(a), 'failed result');
  answer = 'ok';
  const r = await resendNeedsYou(client, { id: a.item.id }); eq(r.notice, 'sent', 'resent'); eq(calls.length, 2, 'resend = one call');
  let refused = false; try { await resendNeedsYou(client, { id: a.item.id }); } catch { refused = true; }
  eq(refused, true, 'no resend after sent'); eq(calls.length, 2, 'no duplicate');

  const saved = (globalThis as any).__testSecrets; (globalThis as any).__testSecrets = {};
  const b = await addNeedsYou(client, { ...ITEM, ref: 'aaaaaaaaaaaaaaaaaaaaaaaa' }, 'claude');
  eq(b.notice, 'not_configured', 'not configured'); eq(calls.length, 2, 'no call without secrets');
  (globalThis as any).__testSecrets = saved;

  answer = 'hang';
  const c = await addNeedsYou(client, { ...ITEM, ref: 'bbbbbbbbbbbbbbbbbbbbbbbb' }, 'claude');
  eq(c.notice, 'unknown', 'timeout = unknown'); eq(calls.length, 3, 'one attempt');
  answer = 'ok'; refused = false;
  try { await resendNeedsYou(client, { id: c.item.id }); } catch { refused = true; }
  eq(refused, true, 'unknown needs confirm_resend'); eq(calls.length, 3, 'nothing sent');
  noSecret(JSON.stringify(await listNeedsYou(client, { status: 'all' })), 'list after failures');
});

Deno.test('items refuse file contents and secrets', async () => {
  const bad = [
    '<?php echo 1; ?>', '<html><body>x</body></html>', 'RewriteRule ^ /x [R=301]', '```\ncode\n```', 'a\nb\nc\nd\ne',
    'token ' + FAKE_KEY, 'see ' + FAKE_URL, 'ghp_' + 'A'.repeat(36), 'CPANEL_TOKEN=abc', 'x'.repeat(700),
  ];
  for (const t of bad) { let threw = false; try { cleanText('why', t, 600); } catch { threw = true; } if (!threw) fail('accepted: ' + t.slice(0, 20)); }
  for (const ok of ['Publish checkpoint 6af918157d3d4a734af8b2da (git b57e3cd)', 'live sha 2367b292f0e1d2c3b4a5968778695a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7 matches', 'public_html/pageone/preview/rc-design-build/.htaccess']) cleanText('why', ok, 600);
  const { client } = makeDb(); calls = [];
  let threw = false; try { await addNeedsYou(client, { ...ITEM, why: '<script>alert(1)</script>' }, 'claude'); } catch { threw = true; }
  eq(threw, true, 'add refuses markup'); eq(calls.length, 0, 'refused add sends nothing');
  threw = false; try { await addNeedsYou(client, { ...ITEM, ref: 'not-a-checkpoint' }, 'claude'); } catch { threw = true; }
  eq(threw, true, 'publish needs a checkpoint id');
});

Deno.test('non-routine https webhook: notice JSON body + Bearer; http refused', () => {
  const r = noticeRequest('https://hooks.example.invalid/grok', 'k'.repeat(20), { id: 'x' });
  eq(JSON.parse(String(r.init.body)), { id: 'x' }, 'plain body');
  eq((r.init.headers as any)['anthropic-beta'], undefined, 'no beta header');
  let threw = false; try { noticeRequest('http://hooks.example.invalid/grok', 'k', {}); } catch (e) { threw = true; noSecret(String(e), 'url error'); }
  eq(threw, true, 'http refused');
});

Deno.test('read tool over HTTP: needs key reads only; overview / site keys refused; no secrets in any response', async () => {
  const { client } = makeDb(); calls = []; answer = 'ok';
  (globalThis as any).__testClient = client;
  const keys: Record<string, string> = { needs: 'bb_needs' + 'n'.repeat(40), overview: 'bb_over' + 'o'.repeat(40), site: 'bb_site' + 's'.repeat(40) };
  for (const [scope, key] of Object.entries(keys)) {
    await client.asServiceRole.entities.BridgeKey.create({ label: scope, scope: scope === 'site' ? 'site:cleanic' : scope, key_hash: await keyHash(key), active: true });
  }
  const a = await addNeedsYou(client, ITEM, 'claude');
  const call = async (entry: any, key: string | null, body: any) => {
    const headers: Record<string, string> = { 'content-type': 'application/json' };
    if (key) headers['X-Bridge-Key'] = key;
    const res = await entry(new Request('https://bridge.invalid/fn', { method: 'POST', headers, body: JSON.stringify(body) }));
    const text = await res.text(); noSecret(text, 'http response'); return { status: res.status, json: JSON.parse(text) };
  };
  const list = await call(needsListEntry, keys.needs, {});
  eq(list.status, 200, 'needs key lists'); eq(list.json.count, 1, 'one open');
  const one = await call(needsListEntry, keys.needs, { id: a.item.id });
  eq(one.json.item.status, 'open', 'item open'); eq(one.json.item.summary, ITEM.summary, 'summary');
  const fields = Object.keys(one.json.item).sort();
  for (const f of fields) if (/key|url|token|secret|content|dedupe|error/i.test(f)) fail('read view field ' + f);
  eq((await call(needsEntry, keys.needs, { action: 'add', ...ITEM, ref: 'cccccccccccccccccccccccc' })).status, 403, 'needs key cannot add');
  eq((await call(needsEntry, keys.needs, { action: 'done', id: a.item.id, live_check: 'x', site_recheck: 'y' })).status, 403, 'needs key cannot close');
  eq((await call(needsListEntry, keys.overview, {})).status, 403, 'overview key refused');
  eq((await call(needsListEntry, keys.site, {})).status, 403, 'site key refused');
  eq((await call(needsListEntry, 'bb_wrong' + 'w'.repeat(40), {})).status, 401, 'unknown key refused');
  const viaSession = await call(needsEntry, null, { action: 'add', ...ITEM, ref: 'dddddddddddddddddddddddd' });
  eq(viaSession.status, 200, 'signed-in admin adds'); eq(viaSession.json.notice, 'sent', 'sent');
  eq(calls.length, 2, 'exactly one call per real new item');
  (globalThis as any).__testClient = undefined;
});

Deno.test('nothing logged the webhook URL or key', () => {
  for (const line of consoleLines) noSecret(line, 'console');
});

// APPROVED SEO EDIT RULE self-test (Edwin 16 Nov 2026: "Let Claude's approved jobs edit titles, meta, H1 and content
// without asking me, keep auto-backups"). Pure guard calls with fake live states, then the real write path
// (write_file / edit_file / write_files / restore_backup) against the same in-memory fake cPanel as liveEdit.test.ts.
// Run: deno test --no-check -A --import-map tests/importmap.json tests/seoEditRelax.test.ts
import { liveGuard, SEO_EDIT_ON, MYKAR_FB_PATH } from '../base44/shared/liveGuard.ts';
import { writeFile, editFile, restoreBackup, listBackups, deleteSitemapTxt } from '../base44/shared/bridgeOps.ts';
import { writeMany, runBulk } from '../base44/shared/bulkWrite.ts';
import { GUARD_OVERRIDES, SITE_HOLDS, holdReason } from '../base44/shared/bridgeConfig.ts';

const HOME = '/home3/sgmodde1', ROOT = HOME + '/public_html', PAGEONE = ROOT + '/pageone';
const files = new Map<string, Uint8Array>();
const dirs = new Set<string>([HOME, ROOT, PAGEONE, ROOT + '/cleanic', HOME + '/bluehost-bridge-private', HOME + '/bluehost-bridge-private/backups']);
const calls: string[] = [];
let failUploadFor = '';
let inflight = 0, maxInflight = 0;
const latin1 = (b: Uint8Array) => Array.from(b, (c) => String.fromCharCode(c)).join('');
const ok = (data: any) => Response.json({ result: { status: 1, errors: null, data } });
const parentOf = (p: string) => p.slice(0, p.lastIndexOf('/'));

globalThis.fetch = (async (input: any, init: any = {}) => {
  inflight++; maxInflight = Math.max(maxInflight, inflight);
  await new Promise((r) => setTimeout(r, 2));
  try {
    const url = new URL(String(input));
    if (url.pathname.startsWith('/execute/')) {
      const fn = url.pathname.slice(9); calls.push(fn);
      const q = url.searchParams;
      if (fn === 'DomainInfo/domains_data') return ok({ main_domain: { domain: 'sggarage.com', documentroot: ROOT },
        addon_domains: [{ domain: 'pageonesingapore.com', documentroot: PAGEONE }, { domain: 'cleanicdetailing.com', documentroot: ROOT + '/cleanic' }], sub_domains: [], parked_domains: [] });
      if (fn === 'Fileman/get_file_information') {
        const p = q.get('path')!;
        if (files.has(p)) return ok({ exists: 1, mode: 0o100644, size: files.get(p)!.length, mtime: 1 });
        if (dirs.has(p)) return ok({ exists: 1, mode: 0o040755, size: 4096, mtime: 1 });
        return Response.json({ result: { status: 0, errors: ['The file is not available'] } });
      }
      if (fn === 'Fileman/list_files') { // server listing for the live guard probe (14 Nov 2026)
        const d = q.get('dir')!; if (!dirs.has(d)) return Response.json({ result: { status: 0, errors: ['No such directory'] } });
        const rows: any[] = [];
        for (const f of files.keys()) if (parentOf(f) === d) rows.push({ file: f.slice(d.length + 1), type: 'file' });
        for (const x of dirs) if (x !== d && parentOf(x) === d) rows.push({ file: x.slice(d.length + 1), type: 'dir' });
        return ok(rows);
      }
      if (fn === 'Fileman/get_file_content') {
        const b = files.get(q.get('dir') + '/' + q.get('file'));
        return b ? ok({ content: latin1(b) }) : Response.json({ result: { status: 0, errors: ['No such file'] } });
      }
      if (fn === 'Fileman/upload_files') {
        const form = init.body as FormData; const dir = String(form.get('dir')); const f = form.get('file-1') as File;
        if (!dirs.has(dir)) return Response.json({ result: { status: 0, errors: ['no dir'] } });
        const bytes = new Uint8Array(await f.arrayBuffer());
        if (f.name === failUploadFor && latin1(bytes) === 'will fail') bytes[0] ^= 1; // corrupt the new content only, to exercise verify + restore
        files.set(dir + '/' + f.name, bytes);
        return ok({ succeeded: 1 });
      }
    }
    if (url.pathname === '/json-api/cpanel') {
      const p = new URLSearchParams(String(init.body)); const fn = p.get('cpanel_jsonapi_func')!; calls.push('api2/' + fn + '/' + (p.get('op') || ''));
      const res = (data: any[]) => Response.json({ cpanelresult: { event: { result: 1 }, data } });
      if (fn === 'mkdir') {
        const d = p.get('path') + '/' + p.get('name');
        if (dirs.has(d) || !dirs.has(p.get('path')!)) return Response.json({ cpanelresult: { event: { result: 1 }, data: [{ result: 0, reason: 'exists or no parent' }] } });
        dirs.add(d); return res([{ result: 1 }]);
      }
      if (fn === 'fileop' && p.get('op') === 'copy') { files.set(p.get('destfiles')!, files.get(p.get('sourcefiles')!)!.slice()); return res([{ result: 1 }]); }
      if (fn === 'fileop' && p.get('op') === 'chmod') return res([{ result: 1 }]);
    }
    return new Response('unexpected ' + url, { status: 500 });
  } finally { inflight--; }
}) as typeof fetch;

const logs: any[] = [];
const ctx: any = { agent: 'claude', viaKey: false, email: 'admin@test', base44: { asServiceRole: { entities: {
  BridgeLock: { filter: async () => [] }, BridgeLog: { create: async (r: any) => { logs.push(r); return r; } } } } } };

function eq(a: unknown, b: unknown, m: string) { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error(m + ': expected ' + JSON.stringify(b) + ' got ' + JSON.stringify(a)); }

const enc = (s: string) => new TextEncoder().encode(s);
const shaHex = async (t: string) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', enc(t))), (b) => b.toString(16).padStart(2, '0')).join('');
const P = PAGEONE + '/preview/_live';
dirs.add(PAGEONE + '/preview'); dirs.add(P); dirs.add(P + '/assets'); dirs.add(P + '/cgi-bin');
dirs.add(P + '/svc'); dirs.add(PAGEONE + '/preview/sgcarworkshop');

const dec = (b: Uint8Array) => new TextDecoder().decode(b);
const sha = async (b: Uint8Array) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', b)), (x) => x.toString(16).padStart(2, '0')).join('');
const PG = (o: { title?: string; meta?: string | null; h1?: string; body?: string; ld?: string; faq?: string; footer?: boolean; date?: string } = {}) =>
  '<!doctype html><html><head><title>' + (o.title ?? 'Brake Repair Singapore') + '</title>'
  + (o.meta === null ? '' : '<meta name="description" content="' + (o.meta ?? 'Brake pads and discs replaced same day.') + '">')
  + '<script type="application/ld+json">' + (o.ld ?? '{"@type":"AutoRepair","name":"X Garage","telephone":"+65 6000 0000"}') + '</script>'
  + '</head><body><h1>' + (o.h1 ?? 'Brake repair') + '</h1><p>' + (o.body ?? 'We fix brakes.') + '</p>'
  + '<time datetime="' + (o.date ?? '2026-11-10') + '">10 Nov</time>'
  + '<details><summary>' + (o.faq ?? 'How long does it take?') + '</summary>About an hour.</details>'
  + (o.footer === false ? '' : '<a class="p1-foot-review" href="/review.html">Leave us a Google review</a>') + '</body></html>';
const LIVE = PG();
const present = (t: string) => ({ state: 'present' as const, bytes: enc(t) });
const guard = (rel: string, live: any, next: string, extra: Record<string, unknown> = {}, site = 'pageone', op: any = 'write') =>
  liveGuard({ site, rel, op, live, newBytes: enc(next), overrides: GUARD_OVERRIDES, sha256: sha, ...extra });
const R = 'preview/_live/svc/brakes.html';
const out: string[] = [];
async function allowed(name: string, p: Promise<string | null>) { const r = await p; if (r !== null) throw new Error(name + ' should pass: ' + r); out.push('allowed  ' + name); }
async function refused(name: string, p: Promise<string | null>, why: RegExp) { const r = await p; if (r === null || !why.test(r)) throw new Error(name + ' should be refused (' + why + '): ' + r); out.push('refused  ' + name + '  -> ' + r.replace(/^LIVE GUARD refused \w+ of [^ ]+ \(nothing was changed\): /, '').slice(0, 90)); }

Deno.test('rule is on, and approved tool edits of title / meta / H1 / body pass without an override', async () => {
  if (SEO_EDIT_ON !== true) throw new Error('SEO_EDIT_ON');
  const L = present(LIVE), s = { seoEdit: true };
  await allowed('title change', guard(R, L, PG({ title: 'Brake Repair Singapore | Same-Day Pads' }), s));
  await allowed('meta description change', guard(R, L, PG({ meta: 'Same-day brake pad and disc replacement in Ubi.' }), s));
  await allowed('H1 change', guard(R, L, PG({ h1: 'Same-day brake repair in Singapore' }), s));
  await allowed('body content change', guard(R, L, PG({ body: 'We fix brakes. New paragraph about disc skimming.' }), s));
  await allowed('title + meta + H1 + body together', guard(R, L, PG({ title: 'T2', meta: 'M2', h1: 'H2', body: 'B2' }), s));
  await allowed('newer date with retitle', guard(R, L, PG({ title: 'T3', date: '2026-11-16' }), s));
  await allowed('JSON-LD gains a value', guard(R, L, PG({ h1: 'H4', ld: '{"@type":"AutoRepair","name":"X Garage","telephone":"+65 6000 0000","url":"https://x.sg/"}' }), s));
  await allowed('.htm page title change', guard('preview/_live/svc/a.htm', L, PG({ title: 'T5' }), s));
  console.log(out.splice(0).join('\n'));
});

Deno.test('the same edits are still refused on every route that is not an approved tool edit', async () => {
  const L = present(LIVE), next = PG({ title: 'Retitled', h1: 'New H1', meta: 'New meta' });
  await refused('no seoEdit (sync_from_github / drop_publish route)', guard(R, L, next), /title would change.*meta description would change.*H1 would change/);
  await refused('publisher with seoEdit', guard(R, L, next, { seoEdit: true, publisher: true }), /title would change/);
  await refused('auto-sitemap with seoEdit (html)', guard(R, L, next, { seoEdit: true, autoSitemap: true }), /auto-sitemap may only replace/);
  await refused('SG Car Workshop page title (own rule kept)', guard('preview/sgcarworkshop/index.html', L, next, { seoEdit: true }), /title would change.*H1 would change/);
  await allowed('SG Car Workshop meta-only change (its existing rule, unchanged)', guard('preview/sgcarworkshop/index.html', L, PG({ meta: 'Now 812 workshops' }), { seoEdit: true }));
  console.log(out.splice(0).join('\n'));
});

Deno.test('retained HTML safeguards still refuse approved edits', async () => {
  const L = present(LIVE), s = { seoEdit: true };
  await refused('older-than-live source', guard(R, L, PG({ title: 'T', date: '2026-10-01' }), s), /source is older than live/);
  await refused('JSON-LD value changed', guard(R, L, PG({ ld: '{"@type":"AutoRepair","name":"X Garage","telephone":"+65 9999 9999"}' }), s), /JSON-LD would lose or change/);
  await refused('JSON-LD removed', guard(R, L, PG({ title: 'T', ld: '{}' }), s), /JSON-LD would lose or change/);
  await refused('FAQ question lost', guard(R, L, PG({ faq: 'Different question?' }), s), /FAQ would lose 1 question/);
  await refused('review footer removed', guard(R, L, PG({ footer: false }), s), /Google review" footer would be removed/);
  await refused('title removed', guard(R, L, PG().replace(/<title>.*?<\/title>/, ''), s), /must keep 1 <title>/);
  await refused('second title added', guard(R, L, PG().replace('</head>', '<title>x</title></head>'), s), /must keep 1 <title>/);
  await refused('empty title', guard(R, L, PG({ title: '  ' }), s), /title must be 1-200/);
  await refused('title over 200 chars', guard(R, L, PG({ title: 'x'.repeat(201) }), s), /title must be 1-200/);
  await refused('H1 removed', guard(R, L, PG().replace(/<h1>.*?<\/h1>/, ''), s), /must keep 1 <h1>/);
  await refused('extra H1 added', guard(R, L, PG({ body: '<h1>Two</h1>' }), s), /must keep 1 <h1>/);
  await refused('empty H1', guard(R, L, PG({ h1: '<span></span>' }), s), /H1 must be 1-250/);
  await refused('meta description removed', guard(R, L, PG({ meta: null }), s), /meta description would be removed/);
  await refused('meta description emptied', guard(R, L, PG({ meta: '' }), s), /meta description must be 1-400/);
  await refused('meta description over 400', guard(R, L, PG({ meta: 'm'.repeat(401) }), s), /meta description must be 1-400/);
  console.log(out.splice(0).join('\n'));
});

Deno.test('retained non-HTML, server-config, delete and unknown-state blocks are unchanged', async () => {
  const s = { seoEdit: true }, L = present('x');
  for (const f of ['robots.txt', 'sitemap.xml', 'llms.txt', 'data/x.json', 'feed.xml', 'doc.pdf', 'site.webmanifest', 'notes.txt'])
    await refused('replace ' + f, guard('preview/_live/' + f, L, 'y', s), /needs an override/);
  await refused('mykar fb-posts.json bad shape', guard(MYKAR_FB_PATH, L, '{"x":1}', s), /mykar fb-posts\.json rule/);
  for (const f of ['.htaccess', 'svc/.htaccess', '.htpasswd', '.user.ini', 'php.ini', 'contact.php', 'x.phtml', 'a.phar', 'form.cgi', 'run.py', 'a.pl', 'deploy.sh']) {
    await refused('replace ' + f, guard('preview/_live/' + f, L, 'y', s), /never written by a tool/);
    await refused('create ' + f, guard('preview/_live/' + f, { state: 'absent' }, 'y', s), /never written by a tool/);
  }
  await refused('delete index.html', guard(R, present(LIVE), '', s, 'pageone', 'delete'), /delete of a live file is blocked/);
  await refused('delete .htaccess', guard('.htaccess', present('x'), '', s, 'pageone', 'delete'), /delete of a live file is blocked/);
  await refused('move', guard(R, present(LIVE), PG({ title: 'T' }), s, 'pageone', 'move'), /move of a live file is blocked/);
  await refused('rename', guard(R, present(LIVE), PG({ title: 'T' }), s, 'pageone', 'rename'), /rename of a live file is blocked/);
  await refused('unknown live state', guard(R, { state: 'unknown', error: 'read error' }, PG({ title: 'T' }), s), /could not be confirmed/);
  for (const bad of ['../x.html', '/etc/x.html', 'a//b.html', 'a\\b.html', 'https://x.sg/a.html'])
    await refused('path ' + bad, guard(bad, present(LIVE), PG({ title: 'T' }), s), /path|absolute|URLs/);
  console.log(out.splice(0).join('\n'));
});

Deno.test('frozen-site HOLD flags and the write-path blocks are unchanged', async () => {
  console.log('ok       ' + SITE_HOLDS.length + ' HOLD flags, on: ' + JSON.stringify(SITE_HOLDS.filter((h: any) => h.on).map((h: any) => h.site)));
  // writeFile checks holdReason first for every route, before the guard; the rule never reaches a held site.
  for (const h of SITE_HOLDS.filter((x: any) => x.on)) if (!holdReason((h as any).site, 'index.html')) throw new Error('hold ' + (h as any).site);
  for (const f of ['.htaccess', 'contact.php', '.env', 'wp-config.php']) {
    let m = ''; try { await writeFile('pageone', 'preview/_live/' + f, enc('x'), null, { seoEdit: true }); } catch (e) { m = (e as Error).message; }
    if (!m) throw new Error(f + ' was written'); out.push('refused  writeFile seoEdit ' + f + '  -> ' + m.slice(0, 70));
  }
  files.set(P + '/index.html', enc(LIVE));
  let d = ''; try { await deleteSitemapTxt('pageone', 'preview/_live/index.html', await sha(files.get(P + '/index.html')!)); } catch (e) { d = (e as Error).message; }
  if (!/Only a file named exactly sitemap.txt/.test(d) || !files.has(P + '/index.html')) throw new Error('delete: ' + d);
  out.push('refused  delete_file index.html -> ' + d.slice(0, 70));
  console.log(out.splice(0).join('\n'));
});

Deno.test('write_file retitle: written, verified, backed up; restore_backup rolls it back in one step', async () => {
  files.set(P + '/svc/brakes.html', enc(LIVE));
  const base = await sha(enc(LIVE));
  const next = PG({ title: 'Brake Repair Singapore | Same-Day', h1: 'Same-day brake repair', meta: 'New meta.' });
  let stale = ''; try { await writeFile('pageone', R, enc(next), 'a'.repeat(64), { seoEdit: true }); } catch (e) { stale = (e as Error).message; }
  if (!/STALE WRITE refused/.test(stale)) throw new Error('stale base: ' + stale);
  let noBase = ''; try { await writeFile('pageone', R, enc(next), null, { seoEdit: true }); } catch (e) { noBase = (e as Error).message; }
  if (!/expected_sha256 is required/.test(noBase)) throw new Error('no base: ' + noBase);
  let plain = ''; try { await writeFile('pageone', R, enc(next), base); } catch (e) { plain = (e as Error).message; }
  if (!/title would change/.test(plain)) throw new Error('route without seoEdit should still refuse: ' + plain);
  if (dec(files.get(P + '/svc/brakes.html')!) !== LIVE) throw new Error('refused writes changed live');
  const w: any = await writeFile('pageone', R, enc(next), base, { seoEdit: true });
  if (!w.saved || !w.verified || !w.backupId || dec(files.get(P + '/svc/brakes.html')!) !== next) throw new Error('write: ' + JSON.stringify(w));
  const bk = [...files.keys()].find((k) => k.includes('/backups/pageone/' + w.backupId + '/'))!;
  if (!bk || dec(files.get(bk)!) !== LIVE) throw new Error('backup copy is not the old live page');
  console.log('allowed  write_file title+H1+meta with base; verified; backup ' + w.backupId + ' holds the old page byte-exact');
  console.log('refused  same write with stale base / no base / without seoEdit; live unchanged');
  const list: any = await listBackups('pageone', R);
  if (!list.backups.some((b: any) => b.backupId === w.backupId)) throw new Error('list_backups: ' + JSON.stringify(list));
  const r: any = await restoreBackup('pageone', w.backupId, R, { seoEdit: true });
  if (!r.saved || !r.verified || r.restoredFrom !== w.backupId || dec(files.get(P + '/svc/brakes.html')!) !== LIVE) throw new Error('restore: ' + JSON.stringify(r));
  const bk2 = [...files.keys()].find((k) => k.includes('/backups/pageone/' + r.backupId + '/'))!;
  if (!r.backupId || dec(files.get(bk2)!) !== next) throw new Error('restore did not back up the edited page first');
  console.log('allowed  restore_backup ' + w.backupId + ' -> old title back, verified; the edited page was backed up first (' + r.backupId + ')');
});

Deno.test('edit_file and write_files retitle; runBulk without seoEdit (sync_from_github route) still refuses', async () => {
  files.set(P + '/svc/brakes.html', enc(LIVE));
  let noFlag = ''; try { await editFile('pageone', R, [{ old_text: '<title>Brake Repair Singapore</title>', new_text: '<title>X</title>' }], await sha(enc(LIVE))); } catch (x) { noFlag = (x as Error).message; }
  if (!/title would change/.test(noFlag)) throw new Error('edit_file without seoEdit: ' + noFlag);
  console.log('refused  edit_file title change without seoEdit (API key callers) -> title would change');
  const e: any = await editFile('pageone', R, [{ old_text: '<title>Brake Repair Singapore</title>', new_text: '<title>Brake Repair SG | Ubi</title>' }], await sha(enc(LIVE)), { seoEdit: true });
  if (!e.saved || !e.backupId || !dec(files.get(P + '/svc/brakes.html')!).includes('<title>Brake Repair SG | Ubi</title>')) throw new Error('edit_file: ' + JSON.stringify(e));
  console.log('allowed  edit_file title change; backup ' + e.backupId);
  const cur = dec(files.get(P + '/svc/brakes.html')!);
  const next = cur.replace('<h1>Brake repair</h1>', '<h1>Brake repair in Ubi</h1>');
  const plan = { base: '', overwrite: true, files: [{ path: R, bytes: enc(next), expected: await sha(enc(cur)) }], totalBytes: next.length };
  let m = ''; try { await runBulk('pageone', plan as any, ctx, { dryRun: false, started: Date.now() }); } catch (x) { m = (x as Error).message; }
  if (!/LIVE GUARD refused.*H1 would change/.test(m) || dec(files.get(P + '/svc/brakes.html')!) !== cur) throw new Error('runBulk without seoEdit: ' + m);
  console.log('refused  runBulk without seoEdit (sync_from_github route) -> ' + m.slice(0, 80));
  for (const [who, c] of [['ChatGPT key', { ...ctx, agent: 'chatgpt', viaKey: true }], ['site key', { ...ctx, agent: 'automation', viaKey: true }], ['claude via key', { ...ctx, viaKey: true }]] as const) {
    let k = ''; try { await writeMany({ site: 'pageone', files: [{ path: R, content: next, expected_sha256: await sha(enc(cur)) }] }, c); } catch (x) { k = (x as Error).message; }
    if (!/H1 would change/.test(k) || dec(files.get(P + '/svc/brakes.html')!) !== cur) throw new Error('write_files via ' + who + ': ' + k);
    console.log('refused  write_files H1 change via ' + who + ' -> H1 would change');
  }
  const b: any = await writeMany({ site: 'pageone', files: [{ path: R, content: next, expected_sha256: await sha(enc(cur)) }] }, ctx);
  const row = (b.results || b.files || []).find((x: any) => x.path === R);
  if (!row || row.status !== 'updated' || !row.backupId || dec(files.get(P + '/svc/brakes.html')!) !== next) throw new Error('write_files: ' + JSON.stringify(b).slice(0, 400));
  console.log('allowed  write_files H1 change; backup ' + row.backupId);
});

Deno.test('tool entry points pass seoEdit only for Claude\'s signed-in session; sync, drops, publisher never pass it', async () => {
  const src = (p: string) => Deno.readTextFileSync(new URL('../base44/' + p, import.meta.url));
  const FLAG = "seoEdit: ctx.agent === 'claude' && !ctx.viaKey";
  for (const f of ['functions/bridgeWrite/entry.ts', 'functions/bridgeEdit/entry.ts', 'functions/bridgeRestore/entry.ts', 'shared/bulkWrite.ts'])
    if (!src(f).includes(FLAG)) throw new Error(f + ' does not gate seoEdit on the Claude session');
  for (const f of ['shared/githubSync.ts', 'shared/drops.ts', 'shared/pageoneArticles.ts', 'shared/autoSitemapRun.ts', 'shared/heroImage.ts'])
    if (/seoEdit/.test(src(f))) throw new Error(f + ' must not pass seoEdit');
  const all = [...src('shared/bridgeOps.ts').matchAll(/seoEdit: (true|[^,})]+)/g)].map((m) => m[1]);
  if (all.includes('true')) throw new Error('bridgeOps sets seoEdit: true unconditionally');
  console.log('ok       write_file / edit_file / restore_backup / write_files gate on the Claude session; sync, drops, publisher, auto-sitemap, hero image never pass seoEdit');
});


// ---- runner additions: a real PNG behind a fake Base44 image URL, and a fake IndexNow API ----
const harnessFetch = globalThis.fetch;
const indexNowSent: any[] = [];
let photo: Uint8Array = new Uint8Array();
globalThis.fetch = (async (input: any, init: any = {}) => {
  const url = new URL(String(input));
  if (url.hostname === 'img.test') return new Response(photo, { status: 200, headers: { 'content-type': 'image/png' } });
  if (url.hostname === 'api.indexnow.org') { indexNowSent.push(JSON.parse(String(init.body))); return new Response('', { status: 202 }); }
  return harnessFetch(input, init);
}) as typeof fetch;
let genCalls = 0;
(globalThis as any).__bridgeTestClient.asServiceRole.integrations = { Core: { GenerateImage: async (_a: any) => { genCalls++; return { url: 'https://img.test/gen-' + genCalls + '.png' }; } } };
for (const d of ['/images', '/images/articles', '/preview/aivs', '/preview/aivs/images', '/preview/aivs/images/articles', '/articles']) dirs.add(PAGEONE + d);

const RUNNER_KEY = 'bb_' + 'r'.repeat(43);
table('BridgeKey').push({ id: 'k4', label: 'grokbot-runner', scope: 'runner', key_hash: await keyHash(RUNNER_KEY), active: true, last_used_at: new Date().toISOString() });
const runnerRows = () => table('BridgeLog').filter((r) => r.label === 'grokbot-runner');
const assert = (c: unknown, m: string) => { if (!c) throw new Error(m); };

Deno.test('R1. runner sites are named, all real Bridge sites; allowed actions are exactly the brief', () => {
  for (const s of RUNNER_SITES) assert(Object.hasOwn(SITES, s), 'unknown site ' + s);
  assert([...RUNNER_KEY_ACTIONS].sort().join(',') === 'list,read,runner_controller,runner_image,runner_indexnow,runner_sitemap,write,write_many', 'action list changed');
});

Deno.test('R2. runner key: list, read, write (new), replace needs the base sha256, backup kept; each call logged as grokbot-runner', async () => {
  files.set(PAGEONE + '/articles/old-page.html', enc('<html><head><title>Old</title></head><body><h1>Old</h1></body></html>'));
  const before = runnerRows().length;
  let r = await call(listLiveFn, { site: 'pageone', path: 'articles' }, RUNNER_KEY); assert(r.status === 200, 'list ' + JSON.stringify(r.body));
  r = await call(listFn, { site: 'pageone', path: 'articles' }, RUNNER_KEY); assert(r.status === 200, 'list old ' + JSON.stringify(r.body));
  r = await call(readFn, { site: 'pageone', path: 'articles/old-page.html' }, RUNNER_KEY); assert(r.status === 200 && r.body.sha256, 'read');
  const base = r.body.sha256;
  r = await call(readOldFn, { site: 'pageone', path: 'articles/old-page.html' }, RUNNER_KEY); assert(r.status === 200, 'read old');
  r = await call(writeFn, { site: 'pageone', path: 'images/articles/new-note.txt', content: 'hello runner' }, RUNNER_KEY);
  assert(r.status === 200 && r.body.saved, 'new write ' + JSON.stringify(r.body));
  r = await call(writeFn, { site: 'pageone', path: 'articles/old-page.html', content: '<html><head><title>New</title></head><body><h1>New</h1></body></html>' }, RUNNER_KEY);
  assert(r.status === 409 && /expected_sha256 is required/.test(r.body.error), 'replace without base must be refused: ' + JSON.stringify(r.body));
  r = await call(writeFn, { site: 'pageone', path: 'articles/old-page.html', expected_sha256: 'a'.repeat(64), content: '<html><head><title>New</title></head><body><h1>New</h1></body></html>' }, RUNNER_KEY);
  assert(r.status === 409 && /STALE/.test(r.body.error), 'stale base must be refused');
  r = await call(writeFn, { site: 'pageone', path: 'articles/old-page.html', expected_sha256: base, content: '<html><head><title>New</title></head><body><h1>New</h1></body></html>' }, RUNNER_KEY);
  assert(r.status === 200 && r.body.saved && r.body.backupId, 'replace with base ' + JSON.stringify(r.body));
  r = await call(writeManyFn, { site: 'pageone', base: 'images/articles', files: [{ path: 'a-note.txt', content: 'a' }, { path: 'b-note.txt', content: 'b' }] }, RUNNER_KEY);
  assert(r.status === 200, 'write_many ' + JSON.stringify(r.body).slice(0, 300));
  const rows = runnerRows().slice(before);
  assert(rows.length === 9, 'expected 9 grokbot-runner rows, got ' + rows.length);
  assert(rows.every((x) => x.actor === 'grokbot-runner (runner key)'), 'actor');
  assert(rows.filter((x) => !x.ok).length === 2, 'two refused writes logged ok:false');
  log('runner rows: ' + rows.map((x) => x.action + (x.ok ? '' : '(refused)')).join(', '));
});

Deno.test('R3. runner key refused: edit, restore, sync, keys, overview, sites, guide, note, claim, backups, htaccess, hero_image, image_gate, needs, drops, self-test, crawler', async () => {
  const before = runnerRows().length;
  const cases: [string, any, any][] = [
    ['edit', editFn, { site: 'pageone', path: 'articles/old-page.html', edits: [] }], ['restore', restoreFn, { site: 'pageone', backup_id: 'x', path: 'a' }],
    ['sync_github', syncGhFn, { site: 'pageone' }], ['keys', keyFn, { action: 'create', scope: 'full' }], ['overview', overviewFn, {}],
    ['sites', sitesFn, {}], ['guide', guideFn, {}], ['note', noteFn, {}], ['claim', claimFn, {}], ['sync', syncFn, {}],
    ['backups', backupsFn, { site: 'pageone', path: 'a' }], ['htaccess', htaccessFn, { site: 'pageone', op: 'read', path: '.htaccess' }],
    ['hero_image', heroFn, { site: 'pageone' }], ['image_gate', gateFn, { site: 'pageone' }], ['needs', needsFn, {}], ['needs_read', needsListFn, {}],
    ['drop_put', dropPutFn, {}], ['drop_publish', dropPublishFn, {}], ['self_test', selfTestFn, {}], ['crawler', crawlerFn, {}],
  ];
  for (const [name, fn, body] of cases) {
    const r = await call(fn, body, RUNNER_KEY);
    assert(r.status === 403, name + ' was not refused: ' + r.status + ' ' + JSON.stringify(r.body).slice(0, 200));
    log('refused  ' + name.padEnd(12) + ' -> ' + String(r.body.error).slice(0, 80));
  }
  const rows = runnerRows().slice(before);
  assert(rows.length === cases.length && rows.every((x) => x.ok === false), 'every refusal logged: ' + rows.length);
});

Deno.test('R4. writes the live guard refuses for every caller: .htaccess, secrets, frozen Cleanic page, delete-like empty paths', async () => {
  files.set(ROOT + '/cleanic/index.html', enc('<html><head><title>Cleanic</title></head><body><h1>Cleanic</h1></body></html>'));
  const r0 = await call(readFn, { site: 'cleanic', path: 'index.html' }, RUNNER_KEY);
  const cases: [string, any, RegExp][] = [
    ['.htaccess', { site: 'pageone', path: '.htaccess', content: 'Deny from all' }, /htaccess/i],
    ['wp-config', { site: 'cleanic', path: 'wp-config.php', content: 'x' }, /./],
    ['secret content', { site: 'pageone', path: 'images/articles/k.txt', content: 'api_key = "sk_live_' + 'x'.repeat(30) + '"' }, /password, key or token/],
    ['frozen cleanic home', { site: 'cleanic', path: 'index.html', expected_sha256: r0.body.sha256, content: '<html><body>changed</body></html>' }, /frozen|articles/i],
  ];
  for (const [name, body, why] of cases) {
    const r = await call(writeFn, body, RUNNER_KEY);
    assert(r.status >= 400 && why.test(String(r.body.error)), name + ' not refused: ' + r.status + ' ' + JSON.stringify(r.body).slice(0, 200));
    log('refused  ' + name.padEnd(20) + ' -> ' + String(r.body.error).slice(0, 80));
  }
});

Deno.test('R5. IndexNow: own domain only, key found on the server and never returned; sitemap rebuild runs', async () => {
  const KEY = 'c'.repeat(32);
  let r = await call(indexNowFn, { site: 'pageone', urls: ['https://evil.example/x/'] }, RUNNER_KEY);
  assert(r.status === 403, 'foreign domain must be refused');
  r = await call(indexNowFn, { site: 'pageone', urls: ['http://pageonesingapore.com/a/'] }, RUNNER_KEY);
  assert(r.status === 400, 'http must be refused');
  r = await call(indexNowFn, { site: 'pageone', urls: ['https://aivs.sg/articles/x/'] }, RUNNER_KEY);
  assert(r.status === 200 && r.body.status === 'skipped', 'no key file -> skipped ' + JSON.stringify(r.body));
  files.set(PAGEONE + '/preview/aivs/' + KEY + '.txt', enc(KEY));
  r = await call(indexNowFn, { site: 'pageone', urls: ['https://aivs.sg/articles/x/', 'https://www.aivs.sg/articles/y/'] }, RUNNER_KEY);
  assert(r.status === 200 && r.body.status === 'sent', 'sent ' + JSON.stringify(r.body));
  assert(!JSON.stringify(r.body).includes(KEY), 'IndexNow key leaked in the response');
  assert(!JSON.stringify(table('BridgeLog')).includes(KEY), 'IndexNow key leaked in BridgeLog');
  assert(indexNowSent.length === 2 && indexNowSent.every((b) => b.key === KEY), 'one send per host');
  r = await call(sitemapFn, { site: 'pageone', paths: ['articles/old-page.html'] }, RUNNER_KEY);
  assert(r.status === 200 && r.body.autoSitemap, 'sitemap ' + JSON.stringify(r.body).slice(0, 200));
  r = await call(sitemapFn, { site: 'pageone', paths: ['.htaccess'] }, RUNNER_KEY);
  assert(r.status === 400, 'sitemap takes .html pages only');
});

Deno.test('R6. Controller relay: op and article_last fields checked before any call', async () => {
  let r = await call(controllerFn, { op: 'delete_client' }, RUNNER_KEY); assert(r.status === 400, 'bad op');
  r = await call(controllerFn, { op: 'article_last', slug: 'carzy', date: '18/11/2026', title: 't', url: 'https://x' }, RUNNER_KEY); assert(r.status === 400, 'bad date');
  r = await call(controllerFn, { op: 'article_last', slug: 'carzy', date: '2026-11-18', title: 't', url: 'http://x' }, RUNNER_KEY); assert(r.status === 400, 'http url');
});

Deno.test('R7. generateArticleImage: hero 1536x1024 webp, card 768x512 webp, og 1200x630 jpg as NEW files; cached; prompt rules', async () => {
  const im = new Image(1536, 1024);
  for (let i = 0; i < im.bitmap.length; i += 4) { const x = (i / 4) % 1536, y = Math.floor(i / 4 / 1536); im.bitmap[i] = (x * 7 + y * 3) & 255; im.bitmap[i + 1] = (x ^ y) & 255; im.bitmap[i + 2] = (y / 4) & 255; im.bitmap[i + 3] = 255; }
  photo = await im.encode(1);
  let r = await call(imageFn, { site: 'pageone', slug: 'runner-test-article', prompt: 'our client testimonial at the workshop counter' }, RUNNER_KEY);
  assert(r.status === 400, 'banned prompt');
  r = await call(imageFn, { site: 'pageone', slug: 'runner-test-article', prompt: 'A quiet Singapore shophouse office desk with a laptop and a coffee cup in morning light', folder: 'preview/aivs/images/articles' }, RUNNER_KEY);
  assert(r.status === 200, 'image ' + JSON.stringify(r.body).slice(0, 300));
  const b = r.body;
  assert(b.hero_url === 'https://aivs.sg/images/articles/runner-test-article.webp', 'hero url ' + b.hero_url);
  assert(b.card_url.endsWith('/runner-test-article-card.webp') && b.og_image_url.endsWith('/runner-test-article-og.jpg'), 'card/og');
  assert(b.files.hero.width === 1536 && b.files.card.width === 768 && b.files.og.height === 630, 'sizes');
  assert(b.alt.startsWith('Illustrative'), 'alt');
  for (const f of ['runner-test-article.webp', 'runner-test-article-card.webp', 'runner-test-article-og.jpg']) assert(files.has(PAGEONE + '/preview/aivs/images/articles/' + f), 'missing ' + f);
  const g = genCalls;
  r = await call(imageFn, { site: 'pageone', slug: 'runner-test-article', prompt: 'A quiet Singapore shophouse office desk with a laptop and a coffee cup in morning light', folder: 'preview/aivs/images/articles' }, RUNNER_KEY);
  assert(r.status === 200 && r.body.cached === true && genCalls === g, 'second call cached, no new image');
  r = await call(imageFn, { site: 'pageone', slug: 'x2-article', prompt: 'A quiet Singapore shophouse office desk with a laptop', folder: '../etc' }, RUNNER_KEY);
  assert(r.status === 400, 'bad folder');
  log('image files: ' + Object.entries(b.files).map(([k, v]: any) => k + ' ' + v.width + 'x' + v.height + ' ' + v.bytes + 'B').join(', '));
});

Deno.test('R8. summary', () => { console.log(lines.join('\n')); });

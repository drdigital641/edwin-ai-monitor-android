// LIVE GUARD choke point in shared/cpanel.ts + percent-encoded path test (14 Nov 2026, "GUARD CHOKEPOINT 1114-1010").
// fetch is replaced: no network. Run: deno test --import-map tests/importmap.json tests/cpanelChokepoint.test.ts
import { uapi, api2, withSiteWriteGrant, ChokepointError } from '../base44/shared/cpanel.ts';
import { normalizeRel, writeFile } from '../base44/shared/bridgeOps.ts';

const HOME = '/home3/sgmodde1', SITE = HOME + '/public_html/carbonfibre', PRIV = HOME + '/bluehost-bridge-private', BK = HOME + '/backups-private';
let sent = 0;
globalThis.fetch = (async (input: any) => {
  sent++;
  const url = new URL(String(input));
  if (url.pathname === '/json-api/cpanel') return Response.json({ cpanelresult: { event: { result: 1 }, data: [{ result: 1 }] } });
  return Response.json({ result: { status: 1, errors: null, data: {} } });
}) as typeof fetch;

const form = (dir: string, name: string) => { const f = new FormData(); f.append('dir', dir); f.append('overwrite', '1'); f.append('file-1', new File([new Uint8Array([1])], name), name); return f; };
async function refused(label: string, fn: () => Promise<unknown>) {
  const before = sent;
  let err: unknown = null;
  try { await fn(); } catch (e) { err = e; }
  if (!err) throw new Error(label + ': was NOT refused');
  if (sent !== before) throw new Error(label + ': a request reached cPanel');
  console.log('refused  ', label, '->', String((err as Error).message).slice(0, 110));
}
async function allowed(label: string, fn: () => Promise<unknown>) {
  const before = sent; await fn();
  if (sent === before) throw new Error(label + ': no request was sent');
  console.log('allowed  ', label);
}

Deno.test('cPanel choke point refuses every change into a site folder unless writeFile granted it', async () => {
  await refused('upload_files into site root, no grant', () => uapi('Fileman', 'upload_files', form(SITE, 'index.html'), 'POST'));
  await refused('upload_files .htaccess into site root', () => uapi('Fileman', 'upload_files', form(SITE, '.htaccess'), 'POST'));
  await allowed('upload_files into ~/bluehost-bridge-private (selftest probe)', () => uapi('Fileman', 'upload_files', form(PRIV + '/selftest', 'probe.txt'), 'POST'));
  await allowed('upload_files into site root WITH writeFile grant', () => withSiteWriteGrant(SITE + '/index.html', () => uapi('Fileman', 'upload_files', form(SITE, 'index.html'), 'POST')));
  await refused('same upload after the grant ended', () => uapi('Fileman', 'upload_files', form(SITE, 'index.html'), 'POST'));
  await refused('grant for one file does not cover another', () => withSiteWriteGrant(SITE + '/a.html', () => uapi('Fileman', 'upload_files', form(SITE, 'b.html'), 'POST')));
  await refused('save_file_content into site (not allow-listed either)', () => uapi('Fileman', 'save_file_content', { dir: SITE, file: 'x.html', content: 'x' }, 'POST'));
  await refused('fileop copy into site root', () => api2('fileop', { op: 'copy', sourcefiles: PRIV + '/backups/x', destfiles: SITE + '/index.html', doubledecode: '0' }));
  await allowed('fileop copy site file into ~/bluehost-bridge-private/backups (writeFile backup step)', () => api2('fileop', { op: 'copy', sourcefiles: SITE + '/index.html', destfiles: PRIV + '/backups/sggarage/20261114-000000-abcdef/index.html', doubledecode: '0' }));
  await allowed('fileop compress into ~/backups-private (deploy tgz)', () => api2('fileop', { op: 'compress', sourcefiles: SITE + '/index.html,' + SITE + '/about', destfiles: BK + '/sggarage-deploy-20261114-000000Z.tgz', metadata: 'tar.gz', doubledecode: '0' }));
  for (const op of ['move', 'rename', 'unlink', 'trash', 'extract', 'link', 'killdir'])
    await refused('fileop ' + op, () => api2('fileop', { op, sourcefiles: SITE + '/index.html', destfiles: SITE + '/old.html', doubledecode: '0' }));
  await refused('fileop chmod on a site file', () => api2('fileop', { op: 'chmod', sourcefiles: SITE + '/index.html', metadata: '0777', doubledecode: '0' }));
  await allowed('fileop chmod on a private backup', () => api2('fileop', { op: 'chmod', sourcefiles: PRIV + '/backups/x', metadata: '0600', doubledecode: '0' }, 2));
  await refused('fileop copy without doubledecode=0', () => api2('fileop', { op: 'copy', sourcefiles: SITE + '/index.html', destfiles: PRIV + '/backups/y' }));
  await refused('copy dest walks out of private with ..', () => api2('fileop', { op: 'copy', sourcefiles: SITE + '/index.html', destfiles: PRIV + '/../public_html/carbonfibre/index.html', doubledecode: '0' }));
  await refused('copy dest with %2e%2e', () => api2('fileop', { op: 'copy', sourcefiles: SITE + '/index.html', destfiles: PRIV + '/%2e%2e/public_html/carbonfibre/index.html', doubledecode: '0' }));
  await refused('copy dest with %2f', () => api2('fileop', { op: 'copy', sourcefiles: SITE + '/index.html', destfiles: PRIV + '%2f..%2fpublic_html/x.html', doubledecode: '0' }));
  await refused('upload dir with .. into site', () => uapi('Fileman', 'upload_files', form(PRIV + '/../public_html/carbonfibre', 'index.html'), 'POST'));
  await refused('two destinations in one copy', () => api2('fileop', { op: 'copy', sourcefiles: SITE + '/a', destfiles: PRIV + '/a,' + SITE + '/b', doubledecode: '0' }));
  await allowed('mkdir inside a site (changes no file)', () => api2('mkdir', { path: SITE + '/articles', name: 'new', permissions: '0755' }));
  await refused('mkdir with .. in the name', () => api2('mkdir', { path: SITE, name: '../x', permissions: '0755' }));
});

Deno.test('percent-encoded paths can never decode into a path walk', async () => {
  const bad = ['%2e%2e/index.html', '%2E%2E/%2E%2E/etc/passwd', 'articles/%2e%2e/%2e%2e/x.html', '..%2findex.html', '%2e%2e%2f%2e%2e%2fx', 'a%2fb.html',
    '%252e%252e/x.html', '%c0%ae%c0%ae/x', 'a/%00.html', 'articles\\..\\x.html', '../x.html', 'a/../../x.html'];
  for (const p of bad) {
    let ok = false;
    try { normalizeRel(p); } catch { ok = true; }
    if (!ok) throw new Error('normalizeRel accepted ' + p);
    const before = sent; let threw = false;
    try { await writeFile('sggarage', p, new TextEncoder().encode('x'), null); } catch { threw = true; }
    if (!threw || sent !== before) throw new Error('writeFile did not refuse ' + p + ' before any cPanel call');
    console.log('refused   path', JSON.stringify(p));
  }
  // A leading slash is read as site-relative, never as a server path: '/etc/passwd' -> 'etc/passwd' inside the site root.
  if (normalizeRel('/etc/passwd') !== 'etc/passwd') throw new Error('leading slash not kept inside the site');
  console.log('inside    path "/etc/passwd" -> site-relative "etc/passwd" (and the live guard refuses absolute input)');
  if (normalizeRel('articles/car-engine-knocking-noise-singapore.html') !== 'articles/car-engine-knocking-noise-singapore.html') throw new Error('normal path broken');
});

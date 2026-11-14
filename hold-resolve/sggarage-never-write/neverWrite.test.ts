// SG GARAGE NEVER-WRITE tests (14 Nov 2026, "SGG NEVER-WRITE 1114-1110"). Fake in-memory FTP + fake Base44 SDK,
// no network, nothing saved. Run in TWO copies: the normal one (HOLD on) and a scratch copy with the sggarage HOLD
// flag set to on:false. With the HOLD on, the fake server is a non-SG Garage folder (the HOLD does not apply there);
// with the HOLD off it is the SG Garage docroot itself. Either way only the never-write block can refuse.
// Run: deno test --no-check --allow-env --import-map tests/importmap.json tests/neverWrite.test.ts
import { reset, state } from './fakeFtp.ts';
import { audit, cmds } from './fakeSdk.ts';
import { withFtp } from '../base44/shared/ftpClient.ts';
import { safeWriteRemoteText, readRemoteText, sha256 } from '../base44/shared/ftpFileOps.ts';
import { holdOn } from '../base44/shared/siteHold.ts';
import { NeverWriteError, neverWriteReason } from '../base44/shared/neverWrite.ts';
import ftpWriteFile from '../base44/functions/ftpWriteFile/entry.ts';
import ftpHealthCheck from '../base44/functions/ftpHealthCheck/entry.ts';
import websiteCommandWorker from '../base44/functions/websiteCommandWorker/entry.ts';

const HOLD = holdOn();
console.log('SG Garage HOLD flag in this copy:', HOLD ? 'ON (fake server = a non-SG Garage folder)' : 'OFF (fake server = the SG Garage docroot)');
const BAD = ['.htaccess', '.HTACCESS', '.htaccess.', '.htaccess ', '.HtAccess . ', '.user.ini', '.USER.INI', '.user.ini.', 'php.ini', 'PHP.INI', 'php.ini ',
  'index.php', 'INDEX.PHP', 'x.Php', 'x.php3', 'x.php5', 'x.php7', 'x.phtml', 'x.PHTML', 'x.pht', 'x.phps', 'x.phar', 'x.PHAR',
  'x.php.', 'x.php ', 'x.php...', 'x.php . ', 'shell.php.jpg', 'a/b/c.php',
  // SGG NEVER-WRITE ADD 1114-1125: Bridge NEVER list
  '.htpasswd', '.HTPASSWD', '.htpasswd.', '.htpasswd ', '.HtPasswd . ',
  'run.cgi', 'RUN.CGI', 'run.cgi.', 'run.cgi ', 'run.cgi.txt', 'cgi-bin/run.cgi',
  'x.pl', 'X.PL', 'x.pl...', 'x.pl . ', 'x.pl.jpg',
  'x.py', 'X.Py', 'x.py.', 'x.py ', 'x.py.png',
  'x.sh', 'X.SH', 'x.sh.', 'x.sh ', 'x.sh.html',
  'x.shtml', 'X.SHTML', 'x.shtml.', 'x.shtml ', 'x.shtml.bak', 'a/b/page.shtml'];
const GOOD = ['index.html', 'about/index.html', 'assets/style.css', 'assets/app.js', 'img/logo.png', 'img/photo.webp', 'robots.txt', 'sitemap.xml',
  'data.json', 'php-guide.html', '.htaccess-notes.txt', 'phpinfo.html', 'x.phpx',
  '.htpasswd-help.txt', 'cgi-guide.html', 'perl.html', 'python.html', 'shop.html', 'x.pyc', 'x.plist', 'x.shtm.txt.html', 'push.js', 'flash.sharp.css'];

function server() {
  const files: Record<string, string> = { '/index.html': '<h1>Home</h1>', '/robots.txt': 'User-agent: *', '/.htaccess': 'RewriteEngine On', '/index.php': '<?php echo 1;', '/.htpasswd': 'u:hash', '/page.shtml': '<!--#echo var="x" -->', '/old.html': 'old' };
  if (!HOLD) files['/adba3d204db0f9cd2fb386bf0cc497ce.txt'] = 'key';      // the SG Garage docroot marker
  reset(files, { dirs: ['/_cleanic_control/validation', '/a/b', '/about', '/assets', '/img'] });
}
const snap = () => JSON.stringify([...state.files.entries()].map(([k, v]) => [k, sha256(Buffer.from(v))]).sort()) + '|' + [...state.dirs].sort().join(',');
const stream = (t = 'x') => new Blob([t]).stream();
let refusals = 0;
async function refused(label: string, fn: () => Promise<unknown>) {
  const before = snap(), w = state.writes; let err: any = null;
  try { await fn(); } catch (e) { err = e; }
  if (!(err instanceof NeverWriteError)) throw new Error(label + ': expected a NEVER-WRITE refusal, got ' + (err ? err.name + ' ' + err.message : 'success'));
  if (snap() !== before || state.writes !== w) throw new Error(label + ': server changed');
  refusals++;
}
const req = (body: any) => new Request('http://x/', { method: 'POST', body: JSON.stringify(body) });

Deno.test('name rule: every blocked variant is caught, normal names are not', () => {
  for (const n of BAD) if (!neverWriteReason(n)) throw new Error('not blocked: ' + JSON.stringify(n));
  for (const n of GOOD) if (neverWriteReason(n)) throw new Error('wrongly blocked: ' + n);
  console.log('ok       ' + BAD.length + ' blocked variants, ' + GOOD.length + ' normal names allowed');
});

Deno.test('every FTP write path refuses blocked names before any byte is sent', async () => {
  server(); refusals = 0;
  for (const n of BAD) {
    const p = '/' + n;
    await refused('safeWriteRemoteText new ' + n, () => safeWriteRemoteText(p, 'x'));
    await refused('uploadFrom ' + n, () => withFtp((c: any) => c.uploadFrom(stream(), p)));
    await refused('upload ' + n, () => withFtp((c: any) => c.upload(stream(), p)));
    await refused('appendFrom ' + n, () => withFtp((c: any) => c.appendFrom(stream(), p)));
    await refused('remove ' + n, () => withFtp((c: any) => c.remove(p)));
    await refused('rename good -> ' + n, () => withFtp((c: any) => c.rename('/old.html', p)));
    await refused('rename ' + n + ' -> good', () => withFtp((c: any) => c.rename(p, '/new.html')));
    await refused('relative upload after cd ' + n, () => withFtp(async (c: any) => { await c.cd('/a/b'); await c.uploadFrom(stream(), n.split('/').pop()); }));
    await refused('ensureDir named ' + n, () => withFtp((c: any) => c.ensureDir(p)));
    for (const verb of ['STOR', 'APPE', 'DELE', 'RNFR', 'RNTO', 'MKD'])
      await refused('send ' + verb + ' ' + n, () => withFtp((c: any) => c.send(verb + ' ' + p)));
    await refused('send SITE CHMOD 777 ' + n, () => withFtp((c: any) => c.send('SITE CHMOD 777 ' + p)));
    await refused('write into the backup folder /_chatgpt_backups/' + n, () => withFtp(async (c: any) => { await c.uploadFrom(stream(), '/_chatgpt_backups/' + n); }));
  }
  await refused('overwrite existing /.htaccess with the right sha', () => safeWriteRemoteText('/.htaccess', 'x', { expectedSha256: sha256(Buffer.from('RewriteEngine On')) }));
  await refused('overwrite existing /index.php with the right sha', () => safeWriteRemoteText('/index.php', 'x', { expectedSha256: sha256(Buffer.from('<?php echo 1;')) }));
  await refused('overwrite existing /.htpasswd with the right sha', () => safeWriteRemoteText('/.htpasswd', 'x', { expectedSha256: sha256(Buffer.from('u:hash')) }));
  await refused('overwrite existing /page.shtml with the right sha', () => safeWriteRemoteText('/page.shtml', 'x', { expectedSha256: sha256(Buffer.from('<!--#echo var="x" -->')) }));
  await refused('backup name page.shtml.2026-11-14T00-00-00-000Z.bak', () => withFtp((c: any) => c.uploadFrom(stream(), '/_chatgpt_backups/page.shtml.2026-11-14T00-00-00-000Z.bak')));
  // A PHP file's backup name (x.php.<stamp>.bak) is refused as well; a config file never reaches the backup step.
  await refused('backup name x.php.2026-11-14T00-00-00-000Z.bak', () => withFtp((c: any) => c.uploadFrom(stream(), '/_chatgpt_backups/x.php.2026-11-14T00-00-00-000Z.bak')));
  if ([...state.files.keys()].some((k) => k.startsWith('/_chatgpt_backups/'))) throw new Error('a backup was written for a refused file');
  await refused('uploadFromDir (cannot be name-checked)', () => withFtp((c: any) => c.uploadFromDir('/tmp', '/')));
  await refused('backslash path a\\b.php', () => withFtp((c: any) => c.uploadFrom(stream(), 'a\\b.php')));
  console.log('refused  ' + refusals + ' write attempts across ' + BAD.length + ' names; server bytes unchanged after each');
});

Deno.test('entry functions refuse with 403, mark the command failed and log never-write-refused', async () => {
  server(); audit.length = 0; const before = snap();
  for (const n of ['.htaccess', 'x.PHP ', 'php.ini', '.user.ini.', '.htpasswd', 'run.CGI', 'x.pl', 'x.py.', 'x.sh ', 'x.shtml']) {
    const r1 = await ftpWriteFile(req({ path: '/' + n, content: 'x' }));
    if (r1.status !== 403) throw new Error('ftpWriteFile ' + n + ' -> ' + r1.status);
    const id = 'nw-' + n; cmds[id] = { id, action: 'write', path: '/' + n, content: 'x', status: 'pending', attempts: 0 };
    const r2 = await websiteCommandWorker(req({ id }));
    if (r2.status !== 403 || cmds[id].status !== 'failed' || !/NEVER-WRITE/.test(cmds[id].error)) throw new Error('worker ' + n + ' -> ' + r2.status + ' ' + cmds[id].status);
  }
  if (snap() !== before) throw new Error('server changed');
  const rows = audit.filter((a) => a.stage === 'never-write-refused');
  if (rows.length !== 20) throw new Error('expected 20 never-write-refused rows, got ' + rows.length);
  console.log('refused  ftpWriteFile x10 (403) + websiteCommandWorker x10 (403, command failed); 20 audit rows, e.g. ' + rows[0].detail.slice(0, 110));
});

Deno.test('normal .html/.css/.js/image writes still work (only the never-write block can refuse here)', async () => {
  server();
  for (const n of GOOD) {
    const r = await safeWriteRemoteText('/' + n, 'content of ' + n, state.files.has('/' + n) ? { expectedSha256: sha256(Buffer.from(state.files.get('/' + n)!)) } : {});
    if (!r.verified) throw new Error('not verified ' + n);
  }
  await withFtp((c: any) => c.uploadFrom(new Blob([new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0, 255])]).stream(), '/img/binary.png'));
  await withFtp((c: any) => c.rename('/old.html', '/renamed.html'));
  await withFtp((c: any) => c.send('SITE CHMOD 644 /index.html'));
  const back = await readRemoteText('/assets/style.css');
  if (back.content !== 'content of assets/style.css') throw new Error('readback');
  if (!state.files.has('/img/binary.png') || !state.files.has('/renamed.html')) throw new Error('upload/rename missing');
  const h = await ftpHealthCheck(req({}));
  if (h.status !== 200) throw new Error('health check with probe write + remove -> ' + h.status + ' ' + JSON.stringify(await h.json()));
  console.log('allowed  ' + GOOD.length + ' safe writes (overwrites with backups) + png upload + rename + SITE CHMOD on .html + ftpHealthCheck probe write/remove');
});

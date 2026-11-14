// SG GARAGE HOLD tests for the SgGarage Controller (14 Nov 2026, "SGG CONTROLLER HOLD 1114-1040").
// Fake in-memory FTP server, fake Base44 SDK: no network, nothing saved anywhere.
// Run: deno test --no-check=remote --import-map tests/importmap.json tests/sggHold.test.ts
import { reset, state, Client } from './fakeFtp.ts';
import { audit, cmds } from './fakeSdk.ts';
import { guardClient, withFtp } from '../base44/shared/ftpClient.ts';
import { safeWriteRemoteText, readRemoteText, sha256 } from '../base44/shared/ftpFileOps.ts';
import { holdOn, HoldError } from '../base44/shared/siteHold.ts';
import ftpWriteFile from '../base44/functions/ftpWriteFile/entry.ts';
import ftpHealthCheck from '../base44/functions/ftpHealthCheck/entry.ts';
import websiteCommandWorker from '../base44/functions/websiteCommandWorker/entry.ts';

const MARK = 'adba3d204db0f9cd2fb386bf0cc497ce.txt';
const snap = () => JSON.stringify([...state.files.entries()].map(([k, v]) => [k, sha256(Buffer.from(v))]).sort());
async function refused(label: string, fn: () => Promise<unknown>) {
  const before = snap(), w = state.writes; let err: any = null;
  try { await fn(); } catch (e) { err = e; }
  if (!(err instanceof HoldError)) throw new Error(label + ': expected a HOLD refusal, got ' + (err ? err.message : 'success'));
  if (snap() !== before || state.writes !== w) throw new Error(label + ': something changed on the server');
  console.log('refused ', label);
}
async function allowed(label: string, fn: () => Promise<unknown>) { await fn(); console.log('allowed ', label); }
const req = (body: any) => new Request('http://x/', { method: 'POST', body: JSON.stringify(body) });

Deno.test('hold flag fails closed', () => {
  if (!holdOn()) throw new Error('default must be ON');
  for (const bad of [[], null, undefined, 'x', [{ key: 'sggarage' }], [{ key: 'sggarage', on: 'false' }], [{ key: 'sggarage', on: 0 }], [{ key: 'other', on: false }]])
    if (!holdOn('sggarage', bad)) throw new Error('should be ON for ' + JSON.stringify(bad));
  if (holdOn('sggarage', [{ key: 'sggarage', on: false }])) throw new Error('explicit false should be OFF');
  console.log('ok      flag missing/malformed/unreadable = ON; only on:false = OFF');
});

Deno.test('FTP root IS the SG Garage docroot: every write, rename and delete refused', async () => {
  reset({ ['/' + MARK]: 'k', '/index.html': '<h1>SGG</h1>', '/robots.txt': 'User-agent: *', '/articles/a.html': 'a' });
  const sha = sha256(Buffer.from('<h1>SGG</h1>'));
  await refused('safeWriteRemoteText overwrite /index.html', () => safeWriteRemoteText('/index.html', 'X', { expectedSha256: sha }));
  await refused('safeWriteRemoteText new /new.html', () => safeWriteRemoteText('/new.html', 'X'));
  await refused('safeWriteRemoteText /.htaccess', () => safeWriteRemoteText('/.htaccess', 'Deny from all'));
  await refused('backup folder /_chatgpt_backups is inside the docroot too', () => withFtp((c: any) => c.uploadFrom(new Blob(['x']).stream(), '/_chatgpt_backups/x.bak')));
  await refused('remove', () => withFtp((c: any) => c.remove('/articles/a.html')));
  await refused('rename', () => withFtp((c: any) => c.rename('/index.html', '/old.html')));
  await refused('removeDir', () => withFtp((c: any) => c.removeDir('/articles')));
  await refused('clearWorkingDir', () => withFtp((c: any) => c.clearWorkingDir()));
  await refused('ensureDir (mkdir)', () => withFtp((c: any) => c.ensureDir('/newdir')));
  await refused('send DELE', () => withFtp((c: any) => c.send('DELE /index.html')));
  await refused('send SITE CHMOD', () => withFtp((c: any) => c.send('SITE CHMOD 777 index.html')));
  await refused('client.ftp.request raw STOR', () => withFtp(async (c: any) => c.ftp.request('STOR /index.html')));
  await refused('uploadFromDir', () => withFtp((c: any) => c.uploadFromDir('/tmp', '/')));
  await refused('a method the guard does not know is treated as a write', () => withFtp((c: any) => c.someFutureWriteMethod()));
  await allowed('read /robots.txt', async () => { const r = await readRemoteText('/robots.txt'); if (r.content !== 'User-agent: *') throw new Error('bad read'); });
  await allowed('send NOOP / SIZE', () => withFtp(async (c: any) => { await c.send('NOOP'); await c.send('SIZE /index.html'); }));
});

Deno.test('FTP root is the account home: carbonfibre refused at any depth, other sites still work', async () => {
  reset({ '/public_html/carbonfibre/index.html': 'sgg', ['/public_html/carbonfibre/' + MARK]: 'k', '/public_html/cleanic/index.html': 'c' }, { dirs: ['/_cleanic_control/validation'] });
  await refused('/public_html/carbonfibre/index.html', () => safeWriteRemoteText('/public_html/carbonfibre/x.html', 'X'));
  await refused('relative path after cd', () => withFtp(async (c: any) => { await c.cd('/public_html/carbonfibre'); await c.uploadFrom(new Blob(['x']).stream(), 'x.html'); }));
  await refused('.. walk into carbonfibre', () => withFtp((c: any) => c.uploadFrom(new Blob(['x']).stream(), '/public_html/cleanic/../carbonfibre/x.html')));
  await refused('rename OUT of carbonfibre', () => withFtp((c: any) => c.rename('/public_html/carbonfibre/index.html', '/public_html/cleanic/stolen.html')));
  await refused('rename INTO carbonfibre', () => withFtp((c: any) => c.rename('/public_html/cleanic/index.html', '/public_html/carbonfibre/index.html')));
  await refused('backslash path', () => withFtp((c: any) => c.remove('\\public_html\\carbonfibre\\index.html')));
  await refused('~ path', () => withFtp((c: any) => c.remove('~/public_html/carbonfibre/index.html')));
  await allowed('write outside SG Garage (/_cleanic_control/validation/probe.txt) still works', async () => {
    const r = await safeWriteRemoteText('/_cleanic_control/validation/probe.txt', 'ok'); if (!r.verified) throw new Error('not verified');
  });
});

Deno.test('login folder is the docroot, or the check cannot run: refused (fail closed)', async () => {
  reset({ ['/sgg/' + MARK]: 'k', '/sgg/index.html': 'sgg' }, { loginPwd: '/sgg' });
  await refused('relative write in a login folder that has the SG Garage marker', () => withFtp((c: any) => c.uploadFrom(new Blob(['x']).stream(), 'index.html')));
  reset({ '/index.html': 'x' }, { listFails: true });
  await refused('root listing fails -> cannot prove it is not SG Garage', () => withFtp((c: any) => c.uploadFrom(new Blob(['x']).stream(), '/index.html')));
});

Deno.test('hold OFF (explicit on:false) lets the same write through, so the guard is the only thing blocking', async () => {
  reset({ ['/' + MARK]: 'k' });
  const c = guardClient(new Client(), '/', [{ key: 'sggarage', on: false }]);
  await c.uploadFrom(new Blob(['x']).stream(), '/new.html');
  if (!state.files.has('/new.html')) throw new Error('write did not happen with hold off');
  console.log('allowed  write with hold explicitly off (guardClient test hook only)');
});

Deno.test('entry functions: 423, failed command, and a hold-refused ConnectionAudit row for each refusal', async () => {
  reset({ ['/' + MARK]: 'k', '/robots.txt': 'r', '/index.html': 'i' }, { dirs: ['/_cleanic_control/validation'] });
  audit.length = 0;
  const before = snap();
  const r1 = await ftpWriteFile(req({ path: '/index.html', content: 'X', expected_sha256: sha256(Buffer.from('i')) }));
  if (r1.status !== 423) throw new Error('ftpWriteFile status ' + r1.status);
  const r2 = await ftpHealthCheck(req({}));
  if (r2.status !== 423) throw new Error('ftpHealthCheck status ' + r2.status);
  cmds['c1'] = { id: 'c1', action: 'write', path: '/index.html', content: 'X', expected_sha256: sha256(Buffer.from('i')), status: 'pending', attempts: 0 };
  const r3 = await websiteCommandWorker(req({ id: 'c1' }));
  if (r3.status !== 423 || cmds['c1'].status !== 'failed') throw new Error('worker status ' + r3.status + ' / ' + cmds['c1'].status);
  if (snap() !== before) throw new Error('server changed');
  const held = audit.filter((a) => a.stage === 'hold-refused' && a.status === 'fail');
  if (held.length !== 3) throw new Error('expected 3 hold-refused audit rows, got ' + held.length);
  for (const h of held) console.log('logged  ', h.detail.slice(0, 120));
  const r4 = await ftpHealthCheck(req({ write_test: false }));
  if (r4.status !== 200) throw new Error('read-only health check should pass, got ' + r4.status);
  console.log('allowed  ftpHealthCheck write_test:false (list + read only)');
});

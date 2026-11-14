// In-memory FTP server for the SG Garage HOLD tests (stands in for npm:basic-ftp). No network.
export const state: any = { files: new Map<string, Uint8Array>(), dirs: new Set<string>(['/']), loginPwd: '/', listFails: false, sent: [] as string[], writes: 0 };
export function reset(files: Record<string, string>, opts: any = {}) {
  state.files = new Map(); state.dirs = new Set(['/']); state.sent = []; state.writes = 0;
  state.loginPwd = opts.loginPwd || '/'; state.listFails = !!opts.listFails;
  for (const d of opts.dirs || []) addDir(d);
  for (const [p, c] of Object.entries(files)) { addDir(p.slice(0, p.lastIndexOf('/')) || '/'); state.files.set(p, new TextEncoder().encode(c)); }
}
function addDir(d: string) { const parts = d.split('/').filter(Boolean); let cur = ''; for (const x of parts) { cur += '/' + x; state.dirs.add(cur); } }
const abs = (cwd: string, p: string) => { const out: string[] = []; for (const s of ((p.startsWith('/') ? '' : cwd + '/') + p).split('/')) { if (!s || s === '.') continue; if (s === '..') out.pop(); else out.push(s); } return '/' + out.join('/'); };
export class Client {
  cwd = '/'; ftp: any = { verbose: false, request: async (c: string) => { state.sent.push(c); state.writes++; return { code: 250 }; }, send: (c: string) => { state.sent.push(c); state.writes++; } };
  constructor(_t?: number) {}
  async access() { this.cwd = state.loginPwd; }
  async pwd() { return this.cwd; }
  async cd(p: string) { const a = abs(this.cwd, p); if (!state.dirs.has(a)) throw new Error('550 No such file or directory'); this.cwd = a; }
  async list(p = '') {
    const d = abs(this.cwd, p || '.');
    if (state.listFails) throw new Error('550 Permission denied');
    if (!state.dirs.has(d)) throw new Error('550 No such file or directory');
    const rows: any[] = [];
    for (const f of state.files.keys()) if ((f.slice(0, f.lastIndexOf('/')) || '/') === d) rows.push({ name: f.slice(f.lastIndexOf('/') + 1), size: 1, isDirectory: false });
    for (const x of state.dirs) if (x !== d && (x.slice(0, x.lastIndexOf('/')) || '/') === d) rows.push({ name: x.slice(x.lastIndexOf('/') + 1), isDirectory: true });
    return rows;
  }
  async downloadTo(sink: any, p: string) { const b = state.files.get(abs(this.cwd, p)); if (!b) throw new Error('550 No such file'); await new Promise((r, j) => sink.write(Buffer.from(b), (e: any) => e ? j(e) : r(null))); }
  async uploadFrom(src: any, p: string) { const chunks: any[] = []; for await (const c of src) chunks.push(Buffer.from(c)); state.files.set(abs(this.cwd, p), new Uint8Array(Buffer.concat(chunks))); state.writes++; }
  async ensureDir(p: string) { const a = abs(this.cwd, p); addDir(a); this.cwd = a; state.writes++; }
  async remove(p: string) { state.files.delete(abs(this.cwd, p)); state.writes++; }
  async rename(a: string, b: string) { const x = state.files.get(abs(this.cwd, a)); if (x) { state.files.delete(abs(this.cwd, a)); state.files.set(abs(this.cwd, b), x); } state.writes++; }
  async removeDir(p: string) { state.writes++; }
  async clearWorkingDir() { state.writes++; }
  async uploadFromDir(_l: string, _r?: string) { state.writes++; }
  async someFutureWriteMethod() { state.writes++; }
  async send(c: string) { state.sent.push(c); if (!/^(NOOP|PWD|SIZE|MDTM|FEAT|TYPE)/i.test(c)) state.writes++; return { code: 200 }; }
  async sendIgnoringError(c: string) { return this.send(c); }
  close() {}
}

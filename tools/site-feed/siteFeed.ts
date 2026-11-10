// Site feed for the Page One Controller (11 Nov 2026; hardened after the Security & Privacy review the same day).
// The host firewall refuses the Controller's cloud checker on a few sites (Klar Details, Battery Rescue,
// planwithben.sg, sgcarworkshop.sg, mykar.my), so their article runs looked "Running"/"Failed" although the
// articles were live. The Controller asks for the files it needs (sitemap.xml, the article hub, a few article pages);
// this app reads them from the server's disk through cPanel and sends them back, HMAC-signed.
// cPanel calls used here, all read-only: DomainInfo/domains_data, Fileman/list_files, Fileman/get_file_content.
// Nothing is written, uploaded, moved, renamed, chmod-ed or deleted on any website.
import { secrets } from 'base44:runtime';
import { uapi, checkResult } from './cpanel.ts';
import { CPANEL } from './bridgeConfig.ts';
import { feedKeyBytes, signFeed } from './feedAuth.ts';
import { feedPathFor } from './feedPath.ts';

type FileOut = { status: number; text: string };
const CONTROLLER_FEED = 'https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/siteFeedIngest';
const MAX_ROUNDS = 4;
const MAX_FILES = 160;            // files per run
const MAX_FILE_BYTES = 1_000_000; // per file (checked from the directory listing before reading)
const MAX_TOTAL_BYTES = 2_500_000;
const MAX_TEXT = 400_000;         // kept per file after trimming

async function docroots(): Promise<Record<string, string>> {
  const d = checkResult(await uapi('DomainInfo', 'domains_data', {}), 'domains_data');
  const roots: Record<string, string> = {};
  for (const x of [d?.main_domain, ...(d?.addon_domains || [])].filter(Boolean)) {
    const dom = String(x.domain || '').toLowerCase();
    const root = String(x.documentroot || '').replace(/\/+$/, '');
    if (dom && /^[a-z0-9.-]+$/.test(dom) && root) roots[dom] = root;
  }
  return roots;
}

// One directory listing per folder per run (read-only). Used to refuse symlinks and oversize files before reading.
async function listDir(cache: Map<string, Map<string, { type: string; size: number }>>, dir: string) {
  if (cache.has(dir)) return cache.get(dir)!;
  const m = new Map<string, { type: string; size: number }>();
  try {
    const rows = checkResult(await uapi('Fileman', 'list_files', { dir, show_hidden: '0', include_mime: '0', include_permissions: '0' }), 'list_files');
    for (const r of Array.isArray(rows) ? rows : []) m.set(String(r.file), { type: String(r.type || ''), size: Number(r.size) || 0 });
  } catch { /* unreadable folder: treated as missing */ }
  cache.set(dir, m);
  return m;
}

// Every folder from the document root down must be a real folder and the file a real file (no symlinks).
async function plainFile(cache: Map<string, Map<string, { type: string; size: number }>>, root: string, abs: string): Promise<number | null> {
  const parts = abs.slice(root.length + 1).split('/');
  let dir = root;
  for (let i = 0; i < parts.length; i++) {
    const e = (await listDir(cache, dir)).get(parts[i]);
    const last = i === parts.length - 1;
    if (!e || e.type !== (last ? 'file' : 'dir')) return null;
    if (last) return e.size;
    dir += '/' + parts[i];
  }
  return null;
}

async function readText(abs: string): Promise<string | null> {
  const i = abs.lastIndexOf('/');
  try {
    const data = checkResult(await uapi('Fileman', 'get_file_content', {
      dir: abs.slice(0, i), file: abs.slice(i + 1), from_charset: 'ISO-8859-1', to_charset: 'UTF-8', update_html_document_encoding: '0',
    }), 'get_file_content');
    const s = typeof data === 'string' ? data : data?.content;
    if (typeof s !== 'string') return null;
    const bytes = new Uint8Array(s.length);
    for (let k = 0; k < s.length; k++) bytes[k] = s.charCodeAt(k) & 255;
    return new TextDecoder('utf-8').decode(bytes);
  } catch { return null; }
}

// Only what the Controller reads from a page: the <head>, JSON-LD blocks and link tags.
function trimHtml(t: string): string {
  const head = (t.match(/<head[\s\S]*?<\/head>/i) || [''])[0];
  const ld = t.match(/<script[^>]+application\/ld\+json[^>]*>[\s\S]*?<\/script>/gi) || [];
  const links = t.match(/<a\s[^>]*>/gi) || [];
  return [head, ...ld, ...links].join('\n').slice(0, MAX_TEXT);
}

export async function readPublicUrl(roots: Record<string, string>, url: string, cache = new Map(), budget = { bytes: MAX_TOTAL_BYTES }): Promise<FileOut> {
  const fp = feedPathFor(url, roots, CPANEL.home);
  if (!fp.ok) return { status: fp.status, text: '' };
  for (const abs of fp.candidates) {
    const size = await plainFile(cache, fp.root, abs);
    if (size == null) continue;
    if (size > MAX_FILE_BYTES || size > budget.bytes) return { status: 413, text: '' };
    const text = await readText(abs);
    if (text == null) continue;
    budget.bytes -= size;
    return { status: 200, text: abs.endsWith('.xml') ? text.slice(0, MAX_TEXT) : trimHtml(text) };
  }
  return { status: 404, text: '' };
}

// Logged summary holds counts, sizes, a body hash and status only: no secret, signature, header or file content.
export async function siteFeed(_base44: unknown) {
  const key = feedKeyBytes(secrets.get('SITE_FEED_HMAC_KEY'));
  if (!key) return { ok: false, error: 'SITE_FEED_HMAC_KEY not set (feed skipped)' };
  const roots = await docroots();
  const files: Record<string, FileOut> = {};
  const cache = new Map(), budget = { bytes: MAX_TOTAL_BYTES };
  let res: any = null, refused = 0, lastStatus = 0;
  for (let round = 1; round <= MAX_ROUNDS; round++) {
    const body = JSON.stringify({ round, files });
    const r = await fetch(CONTROLLER_FEED, {
      method: 'POST', headers: { 'Content-Type': 'application/json', ...(await signFeed(key, body)) }, body, signal: AbortSignal.timeout(120_000),
    }).catch(() => null);
    lastStatus = r?.status || 0;
    if (!r || !r.ok) { await r?.body?.cancel().catch(() => {}); return { ok: false, status: lastStatus, round, files: Object.keys(files).length }; }
    res = await r.json().catch(() => null);
    const need: string[] = Array.isArray(res?.need) ? res.need.filter((x: unknown) => typeof x === 'string') : [];
    const fresh = need.filter((u) => !files[u]);
    if (!fresh.length || Object.keys(files).length >= MAX_FILES) break;
    for (const u of fresh.slice(0, MAX_FILES - Object.keys(files).length)) {
      files[u] = await readPublicUrl(roots, u, cache, budget);
      if (files[u].status !== 200) refused++;
    }
  }
  return { ok: !!res?.ok, status: lastStatus, saved: Number(res?.saved) || 0, files: Object.keys(files).length, not_read: refused, bytes_read: MAX_TOTAL_BYTES - budget.bytes };
}

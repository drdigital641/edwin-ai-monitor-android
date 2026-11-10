// Which files the site feed may read (11 Nov 2026, Security & Privacy review). Pure function, unit-tested.
// Only article folders plus the one sitemap file, only .html/.md/.json (and exactly /sitemap.xml), inside a domain's
// document root. Everything else is refused before any cPanel call.

export const ARTICLE_DIRS = ['/articles/', '/article/', '/guides/', '/insights/'];
export const ALLOWED_EXT = /\.(html|md|json)$/i;
export const MAX_PATH = 300;

export type FeedPath = { ok: true; domain: string; root: string; candidates: string[] } | { ok: false; status: 400 | 403 | 404 };

// candidates: absolute file paths to try in order (inside root). The caller must still refuse symlinks and oversize files.
export function feedPathFor(url: string, roots: Record<string, string>, home: string): FeedPath {
  let u: URL;
  try { u = new URL(url); } catch { return { ok: false, status: 400 }; }
  if (u.protocol !== 'https:' || u.username || u.password || u.port || u.search || u.hash) return { ok: false, status: 400 };
  const domain = u.hostname.toLowerCase().replace(/^www\./, '');
  const root = roots[domain];
  // Document roots come from cPanel; they must sit inside the account's home folder.
  if (!root || !root.startsWith(home + '/') || root.includes('..')) return { ok: false, status: 404 };
  const raw = u.pathname;   // already normalised by URL(): "/a/../b" becomes "/b", so test the raw text too
  if (raw.length > MAX_PATH || /%2e|%2f|%5c|%00/i.test(url) || url.includes('..') || raw.includes('//') || raw.includes('\\')) return { ok: false, status: 403 };
  let p: string;
  try { p = decodeURIComponent(raw); } catch { return { ok: false, status: 400 }; }
  if (p.includes('%') || p.includes('\0') || p.includes('\\') || !p.startsWith('/')) return { ok: false, status: 403 };
  const segs = p.split('/').slice(1);
  if (segs.some((s, i) => (s === '' && i !== segs.length - 1) || s === '.' || s === '..' || s.startsWith('.') || !/^[\p{L}\p{N}._~@()+,-]*$/u.test(s))) return { ok: false, status: 403 };
  let candidates: string[];
  if (p === '/sitemap.xml') candidates = [p];
  else {
    if (!ARTICLE_DIRS.some((d) => p.startsWith(d) || p + '/' === d)) return { ok: false, status: 403 };
    if (p.endsWith('/')) candidates = [p + 'index.html'];
    else if (/\.[A-Za-z0-9]{1,6}$/.test(p)) candidates = [p];
    else candidates = ARTICLE_DIRS.includes(p + '/') ? [p + '/index.html'] : [p + '/index.html', p + '.html'];
    candidates = candidates.filter((c) => ALLOWED_EXT.test(c));
    if (!candidates.length) return { ok: false, status: 403 };
  }
  return { ok: true, domain, root, candidates: candidates.map((c) => root + c) };
}

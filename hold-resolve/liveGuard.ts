// LIVE GUARD v2 (14 Nov 2026; Edwin "HOLD RESOLVE SYNC 1114-0850", security review "GUARD SPO CHANGES 1114-0945").
// DRAFT FOR REVIEW: not saved in any Base44 app. Base44 backend functions go live as soon as they are SAVED, so this
// file and its wiring must not be saved until security review and Edwin say "save the guard".
//
// Every write, replace, delete, move or rename of a live file asks liveGuard() first. Fail closed:
//   - The caller passes the live state read from the SERVER (cPanel/FTP file listing + exact-path read), never HTTP:
//       absent  = the parent folder's server listing was read and has no entry with that name (a new file)
//       present = the listing shows a regular file and its bytes were read from that exact path
//       unknown = anything else (read error, listing error, symlink, folder, device): REFUSED
//   - delete / move / rename of a live file: always REFUSED (no tool may do it; there is no override).
//   - Replacing a live file is allowed only for:
//       identical bytes (no change), or
//       HTML (.html/.htm) that keeps every live title, meta description, H1, JSON-LD value, FAQ question and the
//         "Leave us a Google review" footer, and is not older than live, or
//       an allowlisted static asset type (css, js, images, fonts).
//     Everything else (robots.txt, sitemap*.xml, llms*.txt, .htaccess, .user.ini, php.ini, *.php, json, txt, xml, pdf,
//     webmanifest, any unknown type) is REFUSED unless an override entry matches.
//   - Server config / code names (.htaccess, .user.ini, php.ini, *.php, *.phtml, *.phar, *.cgi, *.pl, *.py, *.sh)
//     are refused even as NEW files, and an override never applies to them.
// Override: an entry in GUARD_OVERRIDES for the exact site, path and sha256 of the new bytes. IMPORTANT: Base44
// backend code is live as soon as it is saved (not on Publish), so an override is live the moment it is saved.
// Any GUARD_OVERRIDES edit needs security review AND Edwin's own written yes BEFORE it is saved.
// Pure TypeScript, no imports, so the Bridge and the Controller share the same file.

export type LiveState =
  | { state: 'absent' }
  | { state: 'present'; bytes: Uint8Array }
  | { state: 'unknown'; error: string };

export type GuardOp = 'write' | 'delete' | 'move' | 'rename';

export type GuardOverride = {
  site: string; path: string; sha256: string;   // exact new bytes this override allows
  by: 'Edwin'; review: string; note: string;     // review: security review reference
};

const NEVER = /(^|\/)(\.htaccess|\.htpasswd|\.user\.ini|php\.ini)$|\.(php\d?|phtml|phar|cgi|pl|py|sh)$/i;
const HTML = /\.html?$/i;
const ASSET_OK = /\.(css|js|mjs|png|jpe?g|webp|avif|gif|svg|ico|woff2?|ttf|otf|eot)$/i;

// Path rules, applied to the raw path given by the caller BEFORE any normalising: no NUL, backslash, absolute path,
// "..", "." or empty segment, URL, or control character. Returns the problem, or null when the path is clean.
export function relProblem(raw: unknown): string | null {
  if (typeof raw !== 'string' || raw === '') return 'path is missing';
  if (/[\0\\]/.test(raw)) return 'path contains NUL or backslash';
  if (/[\x00-\x1f\x7f]/.test(raw)) return 'path contains control characters';
  if (raw.startsWith('/') || /^[A-Za-z]:/.test(raw) || raw.startsWith('~')) return 'absolute paths are not allowed';
  if (/^[a-z][a-z0-9+.-]*:/i.test(raw)) return 'URLs are not allowed';
  const parts = raw.split('/');
  if (parts.some((p) => p === '' || p === '.' || p === '..')) return 'path has an empty, "." or ".." segment';
  return null;
}

const dec = (b: Uint8Array) => new TextDecoder('utf-8').decode(b);
const norm = (s: string) => s.replace(/\s+/g, ' ').trim();
const unent = (s: string) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const strip = (s: string) => norm(unent(s.replace(/<[^>]*>/g, ' ')));
const all = (re: RegExp, s: string, g = 1) => [...s.matchAll(re)].map((m) => m[g]);

function metaDescription(html: string): string | null {
  for (const tag of all(/<meta\b([^>]*)>/gi, html)) {
    if (/\bname\s*=\s*["']description["']/i.test(tag)) {
      const c = /\bcontent\s*=\s*"([^"]*)"|\bcontent\s*=\s*'([^']*)'/i.exec(tag);
      return c ? norm(unent(c[1] ?? c[2] ?? '')) : '';
    }
  }
  return null;
}

function jsonLd(html: string): unknown[] {
  return all(/<script\b[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi, html).map((raw) => {
    try { return JSON.parse(raw); } catch { return { __unparsed: norm(raw) }; }
  });
}

// "path = value" facts; arrays compare as sets, so lists may gain items but never lose or change one.
function facts(v: unknown, path: string, out: Set<string>) {
  if (Array.isArray(v)) { for (const item of v) facts(item, path + '[]', out); return; }
  if (v && typeof v === 'object') {
    for (const [k, x] of Object.entries(v as Record<string, unknown>)) {
      if (k === 'dateModified' || k === 'datePublished' || k === 'uploadDate') continue; // checked as "older source"
      facts(x, path + '.' + k, out);
    }
    return;
  }
  out.add(path + ' = ' + JSON.stringify(v));
}

function newestDate(html: string): string | undefined {
  return [
    ...all(/"(?:dateModified|datePublished)"\s*:\s*"(\d{4}-\d{2}-\d{2})/g, html),
    ...all(/<time\b[^>]*datetime\s*=\s*["'](\d{4}-\d{2}-\d{2})/gi, html),
    ...all(/article:modified_time["'][^>]*content\s*=\s*["'](\d{4}-\d{2}-\d{2})/gi, html),
  ].sort().pop();
}

const REVIEW_FOOTER = /p1-foot-review|href\s*=\s*["'][^"']*review\.html/i;

// SEO problems when the new HTML replaces the live HTML (empty = keeps everything live has).
export function htmlProblems(liveBytes: Uint8Array, newBytes: Uint8Array): string[] {
  const live = dec(liveBytes), next = dec(newBytes);
  const out: string[] = [];
  const ld = newestDate(live), nd = newestDate(next);
  if (ld && (!nd || nd < ld)) out.push('source is older than live (newest date ' + (nd || 'none') + ' < live ' + ld + ')');
  const t = (h: string) => all(/<title\b[^>]*>([\s\S]*?)<\/title>/gi, h).map(strip);
  if (JSON.stringify(t(live)) !== JSON.stringify(t(next))) out.push('title would change: ' + JSON.stringify(t(live)[0] ?? '') + ' -> ' + JSON.stringify(t(next)[0] ?? ''));
  const md = metaDescription(live);
  if (md !== null && md !== metaDescription(next)) out.push('meta description would change');
  const h1 = (h: string) => all(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi, h).map(strip);
  if (JSON.stringify(h1(live)) !== JSON.stringify(h1(next))) out.push('H1 would change: ' + JSON.stringify(h1(live)[0] ?? '') + ' -> ' + JSON.stringify(h1(next)[0] ?? ''));
  const lf = new Set<string>(), nf = new Set<string>();
  jsonLd(live).forEach((b) => facts(b, '', lf));
  jsonLd(next).forEach((b) => facts(b, '', nf));
  const lost = [...lf].filter((f) => !nf.has(f));
  if (lost.length) out.push('JSON-LD would lose or change ' + lost.length + ' value(s), e.g. ' + lost[0].slice(0, 160));
  const q = (h: string) => new Set(all(/<summary\b[^>]*>([\s\S]*?)<\/summary>/gi, h).map(strip));
  const nq = q(next);
  const lostQ = [...q(live)].filter((x) => !nq.has(x));
  if (lostQ.length) out.push('FAQ would lose ' + lostQ.length + ' question(s), e.g. ' + JSON.stringify(lostQ[0].slice(0, 120)));
  if (REVIEW_FOOTER.test(live) && !REVIEW_FOOTER.test(next)) out.push('"Leave us a Google review" footer would be removed');
  return out;
}

const eq = (a: Uint8Array, b: Uint8Array) => a.length === b.length && a.every((x, i) => x === b[i]);

// Returns null when the operation may go ahead, or the refusal text (the caller must not touch the file, and logs it).
export async function liveGuard(args: {
  site: string; rel: unknown; op: GuardOp; live: LiveState; newBytes?: Uint8Array;
  overrides: readonly GuardOverride[]; sha256: (b: Uint8Array) => Promise<string>;
}): Promise<string | null> {
  const { site, op, live, newBytes, overrides, sha256 } = args;
  const refuse = (why: string) => 'LIVE GUARD refused ' + op + ' of ' + site + ':' + String(args.rel) + ' (nothing was changed): ' + why;
  const bad = relProblem(args.rel);
  if (bad) return refuse(bad);
  const rel = args.rel as string;
  if (op !== 'write') return refuse(op + ' of a live file is blocked');
  if (!newBytes) return refuse('no new content given');
  if (NEVER.test(rel)) return refuse('server configuration and code files are never written by a tool');
  if (live.state === 'unknown') return refuse('the live file could not be confirmed from the server (' + live.error + ')');
  if (live.state === 'absent') return null;                       // confirmed new file
  if (eq(live.bytes, newBytes)) return null;                      // no change
  let problems: string[];
  if (HTML.test(rel)) problems = htmlProblems(live.bytes, newBytes);
  else if (ASSET_OK.test(rel)) problems = [];
  else problems = ['replacing this file type (' + (rel.split('/').pop() || rel) + ') needs an override'];
  if (!problems.length) return null;
  const sha = await sha256(newBytes);
  if (overrides.some((o) => o.site === site && o.path === rel && o.sha256 === sha && o.by === 'Edwin' && o.review)) return null;
  return refuse(problems.join('; ') + '. Bring the source up to date with live first. Only an override reviewed by'
    + ' security and approved by Edwin can allow it (GUARD_OVERRIDES entry for sha256 ' + sha + ').');
}

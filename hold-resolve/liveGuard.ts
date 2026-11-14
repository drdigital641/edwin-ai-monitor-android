// LIVE GUARD (Edwin, 14 Nov 2026, "HOLD RESOLVE SYNC 1114-0850"): before any write that REPLACES a live file,
// compare the new bytes with the live bytes and refuse when the new file would take away live SEO content:
//   - an older source (its newest date is before the live file's newest date)
//   - a changed or removed <title>, meta description or <h1>
//   - a removed or changed JSON-LD block (blocks may only grow: every live FAQ question / list item must stay)
//   - a removed FAQ question (<details><summary>)
//   - a removed "Leave us a Google review" footer (p1-foot-review / review.html link)
//   - any change to robots.txt
// New files (nothing live yet) and identical bytes always pass. The only override is an entry in
// GUARD_OVERRIDES for the exact new bytes (sha256), which needs a code change that Edwin Publishes.
// Pure TypeScript, no imports, so the Bridge and the Controller share the same file.

export type GuardOverride = { site: string; path: string; sha256: string; by: string; note: string };

const dec = (b: Uint8Array) => new TextDecoder('utf-8').decode(b);
const norm = (s: string) => s.replace(/\s+/g, ' ').trim();
const unent = (s: string) => s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const strip = (s: string) => norm(unent(s.replace(/<[^>]*>/g, ' ')));

function all(re: RegExp, s: string, g = 1): string[] {
  const out: string[] = [];
  for (const m of s.matchAll(re)) out.push(m[g]);
  return out;
}

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
  const out: unknown[] = [];
  for (const raw of all(/<script\b[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi, html)) {
    try { out.push(JSON.parse(raw)); } catch { out.push({ __unparsed: norm(raw) }); }
  }
  return out;
}

// Flatten JSON-LD into "path = value" facts. Arrays are compared as sets of their items, so a list
// may gain items (a new article in an ItemList) but never lose or change one.
function facts(v: unknown, path: string, out: Set<string>) {
  if (Array.isArray(v)) { for (const item of v) facts(item, path + '[]', out); return; }
  if (v && typeof v === 'object') {
    for (const [k, x] of Object.entries(v as Record<string, unknown>)) {
      if (k === 'dateModified' || k === 'datePublished' || k === 'uploadDate') continue; // dates: checked as "older source"
      facts(x, path + '.' + k, out);
    }
    return;
  }
  out.add(path + ' = ' + JSON.stringify(v));
}

function dates(html: string): string[] {
  const d = [
    ...all(/"(?:dateModified|datePublished)"\s*:\s*"(\d{4}-\d{2}-\d{2})/g, html),
    ...all(/<time\b[^>]*datetime\s*=\s*["'](\d{4}-\d{2}-\d{2})/gi, html),
    ...all(/article:modified_time["'][^>]*content\s*=\s*["'](\d{4}-\d{2}-\d{2})/gi, html),
  ];
  return d.sort();
}

const REVIEW_FOOTER = /p1-foot-review|href\s*=\s*["'][^"']*review\.html/i;

export function liveGuardProblems(rel: string, liveBytes: Uint8Array, newBytes: Uint8Array): string[] {
  const file = rel.split('/').pop() || rel;
  if (file === 'robots.txt') {
    return dec(liveBytes) === dec(newBytes) ? [] : ['robots.txt would change'];
  }
  if (!/\.html?$/i.test(rel)) return [];
  const live = dec(liveBytes), next = dec(newBytes);
  const problems: string[] = [];

  const ld = dates(live), nd = dates(next);
  const liveNewest = ld[ld.length - 1], newNewest = nd[nd.length - 1];
  if (liveNewest && (!newNewest || newNewest < liveNewest)) problems.push('source is older than live (newest date ' + (newNewest || 'none') + ' < live ' + liveNewest + ')');

  const t = (h: string) => all(/<title\b[^>]*>([\s\S]*?)<\/title>/gi, h).map(strip);
  if (JSON.stringify(t(live)) !== JSON.stringify(t(next))) problems.push('title would change: ' + JSON.stringify(t(live)[0] ?? '') + ' -> ' + JSON.stringify(t(next)[0] ?? ''));

  const md = metaDescription(live), nmd = metaDescription(next);
  if (md !== null && md !== nmd) problems.push('meta description would change');

  const h1 = (h: string) => all(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi, h).map(strip);
  if (JSON.stringify(h1(live)) !== JSON.stringify(h1(next))) problems.push('H1 would change: ' + JSON.stringify(h1(live)[0] ?? '') + ' -> ' + JSON.stringify(h1(next)[0] ?? ''));

  const lf = new Set<string>(), nf = new Set<string>();
  jsonLd(live).forEach((b, i) => facts(b, '', lf));
  jsonLd(next).forEach((b, i) => facts(b, '', nf));
  const lost = [...lf].filter((f) => !nf.has(f));
  if (lost.length) problems.push('JSON-LD would lose or change ' + lost.length + ' value(s), e.g. ' + lost[0].slice(0, 160));

  const q = (h: string) => new Set(all(/<summary\b[^>]*>([\s\S]*?)<\/summary>/gi, h).map(strip));
  const nq = q(next);
  const lostQ = [...q(live)].filter((x) => !nq.has(x));
  if (lostQ.length) problems.push('FAQ would lose ' + lostQ.length + ' question(s), e.g. ' + JSON.stringify(lostQ[0].slice(0, 120)));

  if (REVIEW_FOOTER.test(live) && !REVIEW_FOOTER.test(next)) problems.push('"Leave us a Google review" footer would be removed');
  return problems;
}

// Returns null when the write may go ahead, or the refusal text.
export async function liveGuard(site: string, rel: string, liveBytes: Uint8Array | null, newBytes: Uint8Array,
  overrides: readonly GuardOverride[], sha256: (b: Uint8Array) => Promise<string>): Promise<string | null> {
  if (!liveBytes) return null;
  const problems = liveGuardProblems(rel, liveBytes, newBytes);
  if (!problems.length) return null;
  const sha = await sha256(newBytes);
  if (overrides.some((o) => o.site === site && o.path === rel && o.sha256 === sha)) return null;
  return 'LIVE GUARD refused ' + site + ':' + rel + ' (nothing was changed): ' + problems.join('; ') +
    '. Bring the source up to date with live first. Only Edwin can override (GUARD_OVERRIDES entry for sha256 ' + sha + ').';
}

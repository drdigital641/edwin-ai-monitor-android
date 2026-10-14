// Bump the Page One pins in the Bluehost Bridge app (6ac6d47b4ec84148578914c7) to a merged commit.
// Run inside the Bridge sandbox (Base44 run_command), from the app root:
//   C=<full merge sha>; curl -s https://raw.githubusercontent.com/drdigital641/edwin-ai-monitor-android/$C/pageone-site/bridge/update_pins.mjs > /tmp/u.mjs && node /tmp/u.mjs $C
// It points SITE_SRC at the commit and recomputes the sha256 of every SITE_SRC pin from the raw file at
// that commit (so a pin can never point at bytes that were not reviewed). It also replaces the "## Results" and
// "## Websites we run" sections of LLMS_BASE with pageone-site/bridge/llms-results.md and llms-websites.md
// (written by builder/build.py from showcase.json), and PAGE_LASTMOD (per-page sitemap dates) from bridge/lastmod.json.
// New pages still need a PINNED_ASSETS and STATIC_PAGES entry by hand.
// Afterwards: create a checkpoint, run the "Page One Article Publisher" workflow and check the live sha256 values.
import fs from 'fs';
import crypto from 'crypto';

const C = process.argv[2];
if (!/^[0-9a-f]{40}$/.test(C || '')) { console.error('usage: node update_pins.mjs <40-char commit sha>'); process.exit(1); }
const RAW = `https://raw.githubusercontent.com/drdigital641/edwin-ai-monitor-android/${C}/pageone-site/`;
const F = 'base44/shared/pageoneArticles.ts';
let s = fs.readFileSync(F, 'utf8');

s = s.replace(/const SITE_SRC = 'https:\/\/raw\.githubusercontent\.com\/drdigital641\/edwin-ai-monitor-android\/[0-9a-f]{40}\/pageone-site\/site\/';/,
  `const SITE_SRC = '${RAW}site/';`);

const get = async (path) => {
  const r = await fetch(RAW + path);
  if (!r.ok) throw new Error(`${path}: HTTP ${r.status}`);
  return Buffer.from(await r.arrayBuffer());
};

const changed = [];
for (const m of [...s.matchAll(/\{ rel: '([^']+)', url: SITE_SRC \+ '([^']+)', sha256: '([0-9a-fx]+)' \}/g)]) {
  const h = crypto.createHash('sha256').update(await get('site/' + m[2])).digest('hex');
  if (h !== m[3]) changed.push(`${m[1]}  ${m[3].slice(0, 8)} -> ${h.slice(0, 8)}`);
  s = s.replace(m[0], `{ rel: '${m[1]}', url: SITE_SRC + '${m[2]}', sha256: '${h}' }`);
}

const swap = (start, end, text) => {
  const i = s.indexOf(start), j = s.indexOf(end, i);
  if (i < 0 || j < 0) throw new Error(`LLMS_BASE section not found: ${start}`);
  s = s.slice(0, i) + text.trimEnd() + '\n' + s.slice(j);
};
swap('## Results (', '\n## Services', (await get('bridge/llms-results.md')).toString('utf8'));
swap('## Websites we run\n', '\n## Area served', (await get('bridge/llms-websites.md')).toString('utf8'));

// Per-page sitemap dates (pageone-site/bridge/lastmod.json, written by builder/build.py), once the Bridge has PAGE_LASTMOD.
const lm = /const PAGE_LASTMOD: Record<string, string> = \{[^}]*\};/;
if (lm.test(s)) s = s.replace(lm, `const PAGE_LASTMOD: Record<string, string> = ${(await get('bridge/lastmod.json')).toString('utf8').trim()};`);

// Business JSON-LD for article pages (pageone-site/bridge/org-graph.json), between the ORG_GRAPH markers.
const og0 = s.indexOf('// ORG_GRAPH:start\n'), og1 = s.indexOf('// ORG_GRAPH:end');
if (og0 >= 0 && og1 > og0) s = s.slice(0, og0) + '// ORG_GRAPH:start\nconst ORG_GRAPH = ' + (await get('bridge/org-graph.json')).toString('utf8').trim() + ';\n' + s.slice(og1);

fs.writeFileSync(F, s);
console.log(changed.length ? changed.join('\n') : 'no page changed');
console.log(`pins: ${changed.length} changed; SITE_SRC -> ${C.slice(0, 7)}; llms.txt Results and Websites sections refreshed`);

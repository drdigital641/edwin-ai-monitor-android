// Generated-file override (sitemap.xml / sitemap.txt / llms.txt). Run:
// deno test --no-check -A --import-map tests/importmap.json tests/generatedOverride.test.ts
// Pure guard calls with fake live states: never touches a live site.
import { liveGuard, xmlProblem, generatedFileProblem } from '../base44/shared/liveGuard.ts';

const enc = (s: string) => new TextEncoder().encode(s);
const sha256 = async (b: Uint8Array) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', b))).map((x) => x.toString(16).padStart(2, '0')).join('');
const OLD_XML = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>https://example.sg/</loc></url>\n</urlset>\n';
const NEW_XML = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>https://example.sg/</loc><lastmod>2026-11-14</lastmod></url>\n<url><loc>https://example.sg/a/?x=1&amp;y=2</loc></url>\n</urlset>\n';
const live = (s: string) => ({ state: 'present' as const, bytes: enc(s) });
const g = (site: string, rel: string, liveText: string, newText: string, publisher = true) =>
  liveGuard({ site, rel, op: 'write', live: live(liveText), newBytes: enc(newText), overrides: [], sha256, publisher });
const ok = async (p: Promise<string | null>) => { const r = await p; if (r !== null) throw new Error('expected allowed, got: ' + r); };
const no = async (p: Promise<string | null>, m: RegExp) => { const r = await p; if (r === null || !m.test(r)) throw new Error('expected refusal ' + m + ', got: ' + r); };

const FOLDERS = { pageone: '', star: 'preview/star-performance/', klar: 'preview/klar-details/', cska: 'preview/cska-auto/', jacky: 'preview/dmts/', ben: 'preview/benjamin-poon/' };

for (const [name, pre] of Object.entries(FOLDERS)) {
  Deno.test(`allowed for ${name}: sitemap.xml, sitemap.txt, llms.txt`, async () => {
    await ok(g('pageone', pre + 'sitemap.xml', OLD_XML, NEW_XML));
    await ok(g('pageone', pre + 'sitemap.txt', 'https://example.sg/\n', 'https://example.sg/\nhttps://example.sg/a/\n'));
    await ok(g('pageone', pre + 'llms.txt', '# Old\n', '# New\n- [Home](https://example.sg/)\n'));
  });
}

Deno.test('refused for sggarage (no override at all), same three files', async () => {
  for (const rel of ['sitemap.xml', 'sitemap.txt', 'llms.txt']) {
    await no(g('sggarage', rel, rel === 'sitemap.xml' ? OLD_XML : 'a\n', rel === 'sitemap.xml' ? NEW_XML : 'https://x.sg/\n'), /needs an override/);
  }
});

Deno.test('refused for other sites and other client folders', async () => {
  await no(g('cleanic', 'sitemap.xml', OLD_XML, NEW_XML), /needs an override/);
  await no(g('contiexpert', 'llms.txt', 'a', 'b'), /needs an override/);
  await no(g('pageone', 'preview/ecu-clinic/sitemap.xml', OLD_XML, NEW_XML), /needs an override/);
  await no(g('pageone', 'preview/wrapstar/llms.txt', 'a', 'b'), /needs an override/);
  await no(g('pageone', 'preview/star-performance/sub/sitemap.xml', OLD_XML, NEW_XML), /needs an override/);
  await no(g('pageone', 'articles/sitemap.xml', OLD_XML, NEW_XML), /needs an override/);
});

Deno.test('refused for any other file, even from the publisher', async () => {
  for (const rel of ['robots.txt', 'llms-full.txt', 'data.json', 'sitemap.xml.bak', 'sitemap-index.xml', 'preview/dmts/robots.txt', 'feed.xml', 'sitemap.xml.gz']) {
    await no(g('pageone', rel, 'a', 'b'), /needs an override|refused/);
  }
});

Deno.test('server config and code stay never-write even from the publisher', async () => {
  await no(g('pageone', '.htaccess', 'a', 'b'), /never written/);
  await no(g('pageone', 'preview/dmts/index.php', 'a', 'b'), /never written/);
});

Deno.test('refused when the write is not from the publisher (bulk write, MCP write_file, sync)', async () => {
  await no(g('pageone', 'sitemap.xml', OLD_XML, NEW_XML, false), /needs an override/);
  await no(liveGuard({ site: 'pageone', rel: 'llms.txt', op: 'write', live: live('a'), newBytes: enc('b'), overrides: [], sha256 }), /needs an override/);
  // a truthy non-boolean is not accepted
  await no(liveGuard({ site: 'pageone', rel: 'llms.txt', op: 'write', live: live('a'), newBytes: enc('b'), overrides: [], sha256, publisher: 'yes' as any }), /needs an override/);
});

Deno.test('bad XML refused', async () => {
  const bad = [
    '<urlset><url><loc>https://x.sg/</loc></url>',                       // root not closed
    '<urlset><url><loc>https://x.sg/</url></loc></urlset>',             // wrong nesting
    '<urlset><url><loc>https://x.sg/?a=1&b=2</loc></url></urlset>',     // raw &
    '<urlset><url><loc>https://x.sg/</loc></url></urlset><urlset></urlset>', // two roots
    'junk<urlset><url><loc>https://x.sg/</loc></url></urlset>',         // text outside root
    '<html><body><loc>https://x.sg/</loc></body></html>',               // wrong root
    '<!DOCTYPE x [<!ENTITY a "b">]><urlset><url><loc>https://x.sg/</loc></url></urlset>', // DTD
    '<urlset><url foo=bar><loc>https://x.sg/</loc></url></urlset>',     // unquoted attribute
    '',                                                                  // empty
  ];
  for (const b of bad) await no(g('pageone', 'sitemap.xml', OLD_XML, b), /generated-file override: sitemap\.xml is not well-formed XML/);
  await no(liveGuard({ site: 'pageone', rel: 'sitemap.xml', op: 'write', live: live(OLD_XML), newBytes: new Uint8Array([0x3c, 0xff, 0xfe]), overrides: [], sha256, publisher: true }), /not valid UTF-8/);
});

Deno.test('sitemap.xml with 0 URLs refused', async () => {
  await no(g('pageone', 'sitemap.xml', OLD_XML, '<?xml version="1.0"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'), /0 URLs/);
  await no(g('pageone', 'preview/klar-details/sitemap.xml', OLD_XML, '<urlset><url><loc></loc></url></urlset>'), /0 URLs/);
  await no(g('pageone', 'preview/klar-details/sitemap.xml', OLD_XML, '<urlset><url><loc>not a url</loc></url></urlset>'), /0 URLs/);
});

Deno.test('empty llms.txt refused, bad sitemap.txt refused', async () => {
  for (const e of ['', '   \n\n\t']) await no(g('pageone', 'llms.txt', '# a', e), /llms\.txt is empty/);
  await no(g('pageone', 'preview/benjamin-poon/llms.txt', '# a', ''), /llms\.txt is empty/);
  await no(g('pageone', 'sitemap.txt', 'https://x.sg/\n', '\n\n'), /0 URLs/);
  await no(g('pageone', 'sitemap.txt', 'https://x.sg/\n', 'https://x.sg/\n<script>\n'), /not an https URL/);
  await no(g('pageone', 'sitemap.txt', 'https://x.sg/\n', 'http://x.sg/\n'), /not an https URL/);
});

Deno.test('unknown live state and path tricks still refused first', async () => {
  const r = await liveGuard({ site: 'pageone', rel: 'sitemap.xml', op: 'write', live: { state: 'unknown', error: 'timeout' }, newBytes: enc(NEW_XML), overrides: [], sha256, publisher: true });
  if (!r || !/could not be confirmed/.test(r)) throw new Error('got ' + r);
  await no(g('pageone', '../sitemap.xml', OLD_XML, NEW_XML), /refused/);
  await no(g('pageone', 'preview/star-performance/../../sitemap.xml', OLD_XML, NEW_XML), /refused/);
  const d = await liveGuard({ site: 'pageone', rel: 'sitemap.xml', op: 'delete', live: live(OLD_XML), overrides: [], sha256, publisher: true });
  if (!d || !/blocked/.test(d)) throw new Error('delete got ' + d);
});

Deno.test('real-shape sitemaps pass the XML check (sitemapindex, image namespace, comments, CDATA)', () => {
  const ok2 = [
    NEW_XML,
    '﻿<?xml version="1.0"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://x.sg/s1.xml</loc></sitemap></sitemapindex>',
    '<?xml version="1.0"?>\n<!-- generated -->\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n<url><loc>https://x.sg/</loc><image:image><image:loc>https://x.sg/a.jpg</image:loc></image:image></url>\n</urlset>',
    "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'><url><loc>https://x.sg/</loc><x><![CDATA[a & <b>]]></x><y/></url></urlset>",
  ];
  for (const x of ok2) { const p = generatedFileProblem('sitemap.xml', enc(x)); if (p) throw new Error(p + ' for ' + x.slice(0, 60)); }
  if (xmlProblem('<urlset><a></b></urlset>') === null) throw new Error('mismatch passed');
});

Deno.test('wiring: only the publisher put() passes publisher: true, and writeFile forwards it strictly', async () => {
  const ops = await Deno.readTextFile(new URL('../base44/shared/bridgeOps.ts', import.meta.url));
  if (!ops.includes("publisher: opts.publisher === true")) throw new Error('writeFile does not forward publisher strictly');
  const hits: string[] = [];
  for await (const f of walk(new URL('../base44/', import.meta.url))) {
    const t = await Deno.readTextFile(f);
    for (const m of t.matchAll(/publisher:\s*true/g)) hits.push(f.pathname.replace(/.*base44\//, '') + '@' + t.slice(0, m.index).split('\n').length);
  }
  if (hits.length !== 1 || !hits[0].startsWith('shared/pageoneArticles.ts@')) throw new Error('publisher: true found at ' + JSON.stringify(hits));
});
async function* walk(dir: URL): AsyncGenerator<URL> {
  for await (const e of Deno.readDir(dir)) {
    const u = new URL(e.name + (e.isDirectory ? '/' : ''), dir);
    if (e.isDirectory) yield* walk(u); else if (/\.(ts|js)$/.test(e.name)) yield u;
  }
}

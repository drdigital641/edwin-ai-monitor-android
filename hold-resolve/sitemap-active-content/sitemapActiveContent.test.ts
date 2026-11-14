// SPO LOW follow-up (14 Nov 2026): the sitemap.xml check refuses active content. Run:
// deno test --no-check -A --import-map tests/importmap.json tests/sitemapActiveContent.test.ts
// Pure function and guard calls with fake live states: never touches a live site.
import { liveGuard, xmlProblem, generatedFileProblem } from '../base44/shared/liveGuard.ts';

const enc = (s: string) => new TextEncoder().encode(s);
const sha256 = async (b: Uint8Array) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', b))).map((x) => x.toString(16).padStart(2, '0')).join('');
const NS = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"';
const XHTML = 'xmlns:xhtml="http://www.w3.org/1999/xhtml"';
const OLD_XML = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset ${NS}>\n<url><loc>https://example.sg/</loc></url>\n</urlset>\n`;
const wrap = (inner: string, attrs = '') => `<?xml version="1.0" encoding="UTF-8"?>\n<urlset ${NS} ${XHTML}${attrs}>\n<url><loc>https://example.sg/</loc>${inner}</url>\n</urlset>\n`;
const refused = (x: string, m: RegExp) => {
  const p = generatedFileProblem('sitemap.xml', enc(x));
  if (p === null || !m.test(p)) throw new Error('expected refusal ' + m + ', got: ' + p + ' for ' + x.slice(0, 160));
};
const allowed = (x: string) => {
  const p = generatedFileProblem('sitemap.xml', enc(x));
  if (p !== null) throw new Error('expected allowed, got: ' + p + ' for ' + x.slice(0, 160));
};

Deno.test('script / iframe / object / embed refused in any namespace and any case', () => {
  for (const el of ['script', 'iframe', 'object', 'embed']) {
    for (const name of [el, el.toUpperCase(), 'xhtml:' + el, 'html:' + el, 'x:' + el[0].toUpperCase() + el.slice(1)]) {
      refused(wrap(`<${name}>a</${name}>`), /element <.+> is not allowed/);
      refused(wrap(`<${name} src="https://x.sg/a"/>`), /element <.+> is not allowed/);
    }
  }
  refused(`<script ${NS}><url><loc>https://x.sg/</loc></url></script>`, /element <script> is not allowed/);
});

Deno.test('on* attributes refused in any namespace and any case', () => {
  for (const a of ['onload', 'onerror', 'ONCLICK', 'onMouseOver', 'xhtml:onload', 'x:onfocus', 'on']) {
    refused(wrap(`<xhtml:link rel="alternate" hreflang="en" href="https://example.sg/" ${a}="x"/>`), /attribute .+ is not allowed/);
    refused(wrap(`<lastmod ${a}='1'>2026-11-14</lastmod>`), /attribute .+ is not allowed/);
  }
  refused(wrap('', ' onload="x"'), /attribute onload is not allowed/);
});

Deno.test('javascript: refused anywhere, also hidden with case, whitespace or character references', () => {
  for (const js of [
    'javascript:alert(1)', 'JavaScript:alert(1)', 'java\tscript:x', 'java&#x09;script:x', '&#106;avascript:x',
    'javascript&#58;x', 'javascript&#x3A;x', 'javascript&colon;x',
    '&#x6A;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3a;x',
  ]) {
    refused(wrap(`<xhtml:link rel="alternate" hreflang="en" href="${js}"/>`), /javascript: is not allowed/);
  }
  refused(`<urlset ${NS}><url><loc>javascript:alert(1)</loc></url></urlset>`, /javascript: is not allowed/);
  refused(wrap('<x><![CDATA[javascript:alert(1)]]></x>'), /javascript: is not allowed/);
  refused(wrap('<!-- javascript:x -->'), /javascript: is not allowed/);
});

Deno.test('xhtml:link hreflang alternates stay allowed, and look-alike words are not refused', () => {
  allowed(wrap('<xhtml:link rel="alternate" hreflang="en" href="https://example.sg/"/><xhtml:link rel="alternate" hreflang="zh" href="https://example.sg/zh/"/><xhtml:link rel="alternate" hreflang="x-default" href="https://example.sg/"/>'));
  allowed(wrap('<xhtml:link rel="alternate" hreflang="en" href="https://example.sg/"></xhtml:link>'));
  allowed(`<urlset ${NS}><url><loc>https://example.sg/javascript-basics/?online=1&amp;onload=2</loc></url><url><loc>https://example.sg/objects/embedded-scripts/</loc></url></urlset>`);
  allowed(wrap('<xhtml:link rel="alternate" hreflang="en" href="https://example.sg/?x=onload"/>'));
  allowed(wrap('<image:image xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"><image:loc>https://example.sg/a.jpg</image:loc></image:image>'));
  allowed(wrap('<scripture>a</scripture><objects/><embedded/><iframes/>'));
  allowed(wrap('', ' xmlns:ont="https://example.sg/ns"'));
});

Deno.test('through the guard: publisher write with active content refused, clean hreflang sitemap allowed', async () => {
  const live = { state: 'present' as const, bytes: enc(OLD_XML) };
  const run = (x: string, rel: string) => liveGuard({ site: 'pageone', rel, op: 'write', live, newBytes: enc(x), overrides: [], sha256, publisher: true });
  for (const rel of ['sitemap.xml', 'preview/dmts/sitemap.xml', 'preview/benjamin-poon/sitemap.xml']) {
    const bad = await run(wrap('<xhtml:script>x</xhtml:script>'), rel);
    if (bad === null || !/element <xhtml:script> is not allowed/.test(bad)) throw new Error('expected refusal, got ' + bad);
    const bad2 = await run(wrap('<xhtml:link rel="alternate" hreflang="en" href="javascript:alert(1)"/>'), rel);
    if (bad2 === null || !/javascript: is not allowed/.test(bad2)) throw new Error('expected refusal, got ' + bad2);
    const bad3 = await run(wrap('<lastmod onclick="x">2026-11-14</lastmod>'), rel);
    if (bad3 === null || !/attribute onclick is not allowed/.test(bad3)) throw new Error('expected refusal, got ' + bad3);
    const good = await run(wrap('<xhtml:link rel="alternate" hreflang="zh" href="https://example.sg/zh/"/>'), rel);
    if (good !== null) throw new Error('expected allowed, got ' + good);
  }
  if (xmlProblem(wrap('<embed/>')) === null) throw new Error('embed passed');
});

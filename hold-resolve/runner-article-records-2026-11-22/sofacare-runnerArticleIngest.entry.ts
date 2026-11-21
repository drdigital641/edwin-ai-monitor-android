// RUNNER ARTICLE RECORDS (Edwin 22 Nov 2026, PERMANENT): the Grok Bot API runner creates SofaCare articles as Article
// records (the hourly :17 publisher renders the site from these records and drops hand-written files). The runner never
// calls this directly: it calls the Bluehost Bridge (bridgeRunnerArticle, runner key), and the Bridge signs the request
// with its pinned P-256 key. Only the PUBLIC key is here (same pinned key the Controller trusts); the apps share no secret.
// Signed payload: { purpose:'runner_article', site:'sofacare', request_id, dry_run, article:{...}, hero_b64?, hero_name?, sent_at }
// Creates ONE Article (status published, origin auto) only when every check passes; otherwise 422 with the problems.
// Same slug again with the same title = the existing record is returned (created:false), so a retry never doubles up.
import { createClientFromRequest } from 'npm:@base44/sdk@0.8.44';
import { checkArticle, SOFA_APP_ID } from '../../shared/runnerArticleChecks.ts';

const BRIDGE_PUBLIC_JWK = Object.freeze({
  kty: 'EC', crv: 'P-256', kid: '2ca976d1567c69b2',
  x: 'hnj0W8ifjVEsIexqGbz92bAGHNux-H9JoZnygmGYEho', y: 'txxOl663_Xxt0TJLZrwjh5Z8kacsNp8gdO5x7YxUd8c',
});
const unb64u = (s: string) => { const b = atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)); return Uint8Array.from(b, (c) => c.charCodeAt(0)); };
async function verify(body: any): Promise<any | null> {
  try {
    if (typeof body?.payload !== 'string' || typeof body?.sig !== 'string' || body.payload.length > 3_500_000 || body.kid !== BRIDGE_PUBLIC_JWK.kid) return null;
    const key = await crypto.subtle.importKey('jwk', { kty: 'EC', crv: 'P-256', x: BRIDGE_PUBLIC_JWK.x, y: BRIDGE_PUBLIC_JWK.y }, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['verify']);
    if (!(await crypto.subtle.verify({ name: 'ECDSA', hash: 'SHA-256' }, key, unb64u(body.sig), new TextEncoder().encode(body.payload)))) return null;
    const p = JSON.parse(body.payload);
    const sent = Date.parse(p?.sent_at || '');
    if (!sent || Math.abs(Date.now() - sent) > 20 * 60_000) return null;
    return p;
  } catch { return null; }
}
const json = (o: unknown, status = 200) => Response.json(o, { status, headers: { 'Cache-Control': 'no-store' } });
const magic = (b: Uint8Array) => (b[0] === 0xff && b[1] === 0xd8) ? 'jpg' : (b[0] === 0x89 && b[1] === 0x50) ? 'png' : (b[0] === 0x52 && b[1] === 0x49 && b[8] === 0x57) ? 'webp' : '';
const sgtDate = () => new Date(Date.now() + 8 * 3600_000).toISOString().slice(0, 10);

export default async function (req: Request) {
  if (req.method !== 'POST') return json({ ok: false, error: 'method' }, 405);
  const body = await req.json().catch(() => null);
  const p = await verify(body);
  if (!p || p.purpose !== 'runner_article' || p.site !== 'sofacare') return json({ ok: false, error: 'Only signed Bridge requests are accepted' }, 401);
  const base44 = createClientFromRequest(req);
  const E = base44.asServiceRole.entities;
  const a = p.article || {};
  const all: any[] = await E.Article.list('-published_date', 500);
  const existing = all.find((x) => x.slug === a.slug);
  if (existing && String(existing.title || '').trim() === String(a.title || '').trim() && existing.status === 'published') {
    return json({ ok: true, created: false, id: existing.id, slug: existing.slug, hero_image: existing.hero_image, note: 'already exists (retry)' });
  }
  const liveSlugs = new Set(all.filter((x) => x.status === 'published').map((x) => String(x.slug || '')));
  const titles = new Set(all.map((x) => String(x.title || '').trim().toLowerCase()));
  if (existing) liveSlugs.add(String(existing.slug));
  let bytes: Uint8Array | null = null, ext = '';
  if (typeof p.hero_b64 === 'string' && p.hero_b64) {
    try { bytes = Uint8Array.from(atob(p.hero_b64), (c) => c.charCodeAt(0)); } catch { return json({ ok: false, error: 'hero_b64 not base64' }, 400); }
    ext = magic(bytes);
    if (!ext || bytes.length < 15_000 || bytes.length > 2_000_000) return json({ ok: false, error: 'hero image must be a real JPEG/PNG/WebP between 15 KB and 2 MB' }, 422);
  }
  const { fails, warns, faqs } = checkArticle(a, { liveSlugs, titles, heroUploaded: !!bytes, sgtToday: sgtDate() });
  if (fails.length) return json({ ok: false, error: 'Article checks failed', problems: fails, warnings: warns }, 422);
  if (p.dry_run === true) return json({ ok: true, dry_run: true, created: false, slug: a.slug, warnings: warns });
  let hero = String(a.hero_image || '');
  if (bytes) {
    const file = new File([bytes as unknown as BlobPart], `${a.slug}.${ext}`, { type: ext === 'jpg' ? 'image/jpeg' : 'image/' + ext });
    const up: any = await base44.asServiceRole.integrations.Core.UploadFile({ file });
    hero = String(up?.file_url || '');
    if (!/^https:\/\/media\.base44\.com\//.test(hero)) return json({ ok: false, error: 'hero upload did not return a media.base44.com URL', got_host: (() => { try { return new URL(hero).host; } catch { return ''; } })() }, 502);
  }
  const rec = await E.Article.create({
    title: a.title.trim(), slug: a.slug, keyword: a.keyword.trim(), h1: a.h1.trim(), meta_description: a.meta_description.trim(),
    excerpt: a.excerpt.trim(), content: a.content, faqs: JSON.stringify(faqs), hero_image: hero, hero_image_alt: a.hero_image_alt.trim(),
    related_service: a.related_service, status: 'published', published_date: a.published_date, origin: 'auto',
  });
  return json({ ok: true, created: true, id: rec.id, slug: rec.slug, hero_image: hero, warnings: warns,
    live_after: 'next hourly publish at :17 (page, hub card, sitemap.xml, llms.txt, IndexNow)', request_id: String(p.request_id || '').slice(0, 80) });
}

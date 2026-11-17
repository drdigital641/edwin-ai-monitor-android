// generateArticleImage (Edwin 18 Nov 2026, Grok Bot runner brief): one Base44 image per article (Base44 makes every image),
// placed on Bluehost through the Bridge as three files next to each other in the site's article image folder:
//   <slug>.webp      hero  1536x1024 (3:2)
//   <slug>-card.webp card  768x512   (3:2)
//   <slug>-og.jpg    og:image / twitter:image 1200x630 (JPEG for the widest link-preview support)
// Each file is NEW and written by writeFile (HOLD, live guard, frozen-site rule, verify). An existing file is never
// replaced: a second call for the same site+folder+slug returns the saved result (cached) and makes no new image.
// Same daily limits as hero_image (shared counters): 3 per site and 40 in total per Singapore day.
// If the resize library cannot load, the original image is written once as <slug>.<ext> and all three URLs point to it
// (warning returned), so an article is never blocked by the resizer.
import { BridgeError, liveUrl, writeFile } from './bridgeOps.ts';
import { base44Image, fetchImage, readState, writeState, sgtNow, NO_TEXT } from './heroImage.ts';

const STATE_ENTITY = 'PageOnePublishState';
const LIMIT_PER_SITE_PER_DAY = 3;
const LIMIT_TOTAL_PER_DAY = 40;
const FOLDER_RE = /^[a-z0-9][a-z0-9_-]*(\/[a-z0-9][a-z0-9_-]*){0,5}$/;
const FOLDER_END = /(^|\/)(images|img|assets|uploads|articles|media|hero)$/;
const STYLE = 'Photorealistic editorial photo for a Singapore or Malaysia local-business article, realistic everyday setting that matches the scene.';
const PROMPT_BAN = /\b(our (client|customer|team|technician|shop|workshop)|testimonial|before and after|logo|certified|licensed|guarantee|award)\b|\$\s?\d|RM\s?\d/i;
const CLAIM_ALT = /\b(our (client|customer|team|technician|job|work)|real (job|photo|customer)|actual (job|customer)|before and after|testimonial)\b/i;

// Default article image folder per site when the caller sends none. Cleanic is WordPress: dated uploads folder.
function defaultFolder(site: string, y: string, m: string): string {
  if (site === 'cleanic') return `wp-content/uploads/${y}/${m}`;
  if (site === 'alicia') return 'assets/articles';
  return 'images/articles';
}

// The public URL: a pageone client folder is served on the client's own domain (preview/<folder>/ -> https://<domain>/).
async function publicUrl(site: string, rel: string): Promise<string> {
  if (site === 'pageone') {
    const m = /^preview\/([a-z0-9-]+)\/(.+)$/.exec(rel);
    if (m) {
      const { AUTO_SITEMAP_CLIENT_FOLDERS } = await import('./liveGuard.ts');
      const d = (AUTO_SITEMAP_CLIENT_FOLDERS as Record<string, string>)[m[1]];
      if (d) return 'https://' + d + '/' + m[2];
    }
  }
  return liveUrl(site, rel);
}

async function counts(base44: any, date: string, site: string) {
  const rows = await base44.asServiceRole.entities[STATE_ENTITY].list('-created_date', 400).catch(() => []);
  let total = 0, perSite = 0;
  for (const r of rows || []) {
    const k = String(r.key || '');
    if (!k.startsWith('hero:')) continue;
    let v: any = {}; try { v = JSON.parse(r.value || '{}'); } catch { /* ignore */ }
    if (v.generated_on !== date) continue;
    total++; if (k.startsWith('hero:' + site + ':')) perSite++;
  }
  return { total, perSite };
}

type Out = { kind: 'hero' | 'card' | 'og'; rel: string; bytes: Uint8Array; w: number; h: number; format: string };

async function variants(src: Uint8Array, base: string, ext: string): Promise<{ files: Out[]; warning?: string }> {
  try {
    const { Image } = await import('npm:imagescript@1.3.0');
    const img: any = await Image.decode(src);
    const make = async (w: number, h: number, as: 'webp' | 'jpg', q: number) => {
      const c = img.clone().cover(w, h);
      return as === 'webp' ? await c.encodeWEBP(q) : await c.encodeJPEG(q);
    };
    return { files: [
      { kind: 'hero', rel: base + '.webp', bytes: await make(1536, 1024, 'webp', 80), w: 1536, h: 1024, format: 'webp' },
      { kind: 'card', rel: base + '-card.webp', bytes: await make(768, 512, 'webp', 78), w: 768, h: 512, format: 'webp' },
      { kind: 'og', rel: base + '-og.jpg', bytes: await make(1200, 630, 'jpg', 84), w: 1200, h: 630, format: 'jpg' },
    ] };
  } catch (e) {
    const msg = (e instanceof Error ? e.message : String(e)).slice(0, 120);
    return { files: [{ kind: 'hero', rel: base + '.' + ext, bytes: src, w: 0, h: 0, format: ext }], warning: 'resize unavailable (' + msg + '): one original file is used for hero, card and og:image' };
  }
}

// body: { site, slug, prompt, alt?, folder?, landscape? }
export async function generateArticleImage(body: any, ctx: { base44: any }) {
  const { base44 } = ctx;
  const site = String(body?.site || '');
  const now = sgtNow();
  const slug = String(body?.slug || '');
  if (!/^[a-z0-9][a-z0-9-]{2,79}$/.test(slug)) throw new BridgeError('slug must be lowercase-hyphen, 3-80 chars', 400);
  const sent = typeof body?.folder === 'string' ? body.folder.trim().replace(/^\/+|\/+$/g, '') : '';
  if (sent && (sent.includes('..') || !FOLDER_RE.test(sent) || !FOLDER_END.test(sent))) throw new BridgeError('folder must be a lowercase site folder ending in images, img, assets, uploads, articles, media or hero (e.g. images/articles or preview/aivs/images/articles)', 400);
  if (site === 'pageone' && sent && sent.startsWith('preview/') && !/^preview\/[a-z0-9-]+\//.test(sent)) throw new BridgeError('folder under preview/ must name the client folder', 400);
  const folder = sent || defaultFolder(site, now.y, now.m);
  const prompt = String(body?.prompt || '').replace(/\s+/g, ' ').trim();
  if (prompt.length < 20 || prompt.length > 400) throw new BridgeError('prompt must be 20-400 characters: describe the picture, not the article', 400);
  if (PROMPT_BAN.test(prompt)) throw new BridgeError(`prompt contains something not allowed (${String(prompt.match(PROMPT_BAN)?.[0])}). Describe a plain scene.`, 400);
  let alt = String(body?.alt || '').replace(/\s+/g, ' ').trim();
  if (!alt) { alt = 'Illustrative photo: ' + prompt; if (alt.length > 125) alt = alt.slice(0, 125).replace(/\s+\S*$/, ''); }
  if (alt.length < 20 || alt.length > 125) throw new BridgeError('alt must be 20-125 characters', 400);
  if (!alt.toLowerCase().startsWith('illustrative')) throw new BridgeError('alt must start with "Illustrative" (AI picture on a real business site)', 400);
  if (CLAIM_ALT.test(alt)) throw new BridgeError('alt must not claim a real job, client or team', 400);

  const key = `hero:${site}:runner:${folder}:${slug}`;
  const prev = await readState(base44, key);
  if (prev?.stage === 'done') return { ...prev.result, cached: true };

  let gatewayUrl = prev?.stage === 'generated' ? String(prev.gateway_url || '') : '';
  if (!gatewayUrl) {
    const c = await counts(base44, now.date, site);
    if (c.total >= LIMIT_TOTAL_PER_DAY || c.perSite >= LIMIT_PER_SITE_PER_DAY) throw new BridgeError(`daily article image limit reached (${c.perSite} for ${site}, ${c.total} in total today)`, 429);
    gatewayUrl = await base44Image(base44, `${STYLE} Scene: ${prompt}. Photorealistic, natural light, high detail. ${NO_TEXT}`, body?.landscape !== false);
    // Saved at once so a retry after a hosting failure does not pay for a second image.
    await writeState(base44, key, prev, { stage: 'generated', gateway_url: gatewayUrl, generated_on: now.date, scene: prompt });
  }
  const img = await fetchImage(gatewayUrl);
  const { files, warning } = await variants(img.bytes, folder + '/' + slug, img.ext);
  const placed: Record<string, any> = {};
  for (const f of files) {
    const r: any = await writeFile(site, f.rel, f.bytes, undefined);
    if (!r?.saved && !r?.unchanged) throw new BridgeError('could not write ' + f.rel, 502);
    placed[f.kind] = { url: await publicUrl(site, f.rel), path: '/' + f.rel, width: f.w || img.w || null, height: f.h || img.h || null, format: f.format, bytes: f.bytes.length };
  }
  if (!placed.card) placed.card = placed.hero;
  if (!placed.og) placed.og = placed.hero;
  const result = { site, folder, slug, alt, hero_url: placed.hero.url, card_url: placed.card.url, og_image_url: placed.og.url,
    files: placed, generated_on: now.date, model: 'Base44 GenerateImage', warnings: warning ? [warning] : [] };
  await writeState(base44, key, await readState(base44, key), { stage: 'done', gateway_url: gatewayUrl, generated_on: now.date, scene: prompt, result });
  return { ...result, cached: false };
}

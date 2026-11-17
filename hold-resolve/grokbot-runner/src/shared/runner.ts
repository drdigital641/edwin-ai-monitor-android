// GROKBOT RUNNER KEY (Edwin 18 Nov 2026, brief "Bridge runner key + image function"): routine jobs (midnight articles,
// 5am Copy fix sweep, sgcarworkshop sweep, daily builds, IndexNow resends, area pages) move to an API runner on the
// Grok Bot box. Every Bluehost read and write still goes through the Bridge, with key scope 'runner':
//   - list / read live files, write_file / write_files (the base sha256 compare-and-swap, verified backup and live
//     guard of writeFile apply as for every caller), sitemap.xml + llms.txt rebuild, IndexNow submit (the key file is
//     found on the server and never returned), Controller Copy fix issues + tap counts (read only), the Controller
//     article_last_* fields, and generateArticleImage (Base44 image -> hero, card and og:image files on Bluehost).
//   - NOT: deletes, .htaccess (the htaccess tool is session-only), credentials (secret names/content are refused by
//     writeFile), the database, Bridge config, keys, restore, sync, drops, needs-you, Base44 Publish.
//   - Only the sites named in RUNNER_SITES. Cleanic and ContiExpert stay frozen (articles only) through the live guard.
//   - Every runner call (allowed or refused) gets a BridgeLog row with label 'grokbot-runner'.
import { SITES } from './bridgeConfig.ts';
import { AUTO_SITEMAP_CLIENT_FOLDERS } from './liveGuard.ts';
import { BridgeError, normalizeRel } from './bridgeOps.ts';
import { autoSitemapAfter, findIndexNowKey, sendIndexNow } from './autoSitemapRun.ts';
import { INDEXNOW_MAX_URLS } from './autoSitemap.ts';
import { signedControllerCall } from './crawlerLogs.ts';

export const RUNNER_LABEL = 'grokbot-runner';
export const RUNNER_ACTOR_EMAIL = 'grokbot-runner (runner key)';

// Named client sites (Edwin 18 Nov 2026). A site added to SITES later does NOT join the runner until it is named here.
// 'pageone' covers pageonesingapore.com and the client folders under preview/ (ContiExpert = preview/contiexpert/,
// frozen: articles only, enforced by the live guard for every caller).
export const RUNNER_SITES: readonly string[] = Object.freeze([
  'sggarage', 'cleanic', 'alicia', 'danny', 'sofacare', 'pageone', 'ktech', 'benzworld', 'lilian', 'carzy',
  'hybridworld', 'autoseo', 'ecumats', 'apcar', 'jayven', 'urbaneco', 'snapsg',
]);

// Bridge actions the runner key may run. 'list'/'read' = bridgeListLive/bridgeList and bridgeReadLive/bridgeRead,
// 'write' = bridgeWrite, 'write_many' = bridgeWriteMany. bridgeHtaccess also says 'write' but is session-only, which is
// checked before the scope, so a key can never reach it.
export const RUNNER_KEY_ACTIONS: ReadonlySet<string> = new Set([
  'list', 'read', 'write', 'write_many', 'runner_sitemap', 'runner_indexnow', 'runner_controller', 'runner_image',
]);

const bare = (h: string) => h.toLowerCase().replace(/^www\./, '');

// sitemap.xml + llms.txt rebuild for pages already on the server (e.g. after a write whose autoSitemap step failed,
// or a resend). Same code as the step that runs after every write: merges only, never drops a URL, writes through
// writeFile (base sha, backup, live guard, HOLD), then sends IndexNow for those pages.
export async function runnerSitemap(body: any, ctx: { base44: any }) {
  const list = Array.isArray(body?.paths) ? body.paths : [];
  if (!list.length || list.length > 20) throw new BridgeError('paths must list 1-20 .html pages already on the site', 400);
  const paths = list.map((p: unknown) => normalizeRel(p));
  const bad = paths.find((p: string) => !/\.html?$/i.test(p));
  if (bad) throw new BridgeError('only .html pages: ' + bad, 400);
  return { site: body.site, paths, autoSitemap: await autoSitemapAfter({ site: body.site, written: paths.map((path: string) => ({ path })), dryRun: body?.dry_run === true, base44: ctx.base44 }) };
}

// Where a site's IndexNow key file lives: the site root, or (pageone) the client folder whose domain the URL is on.
export function indexNowGroups(site: string): { prefix: string; domain: string }[] {
  if (!(site in SITES)) return [];
  if (site !== 'pageone') return [{ prefix: '', domain: SITES[site as keyof typeof SITES].domain }];
  return [{ prefix: '', domain: SITES.pageone.domain },
    ...Object.entries(AUTO_SITEMAP_CLIENT_FOLDERS).map(([f, d]) => ({ prefix: 'preview/' + f + '/', domain: d }))];
}

// IndexNow submit. The Bridge finds the site's key file on the server (a 32-hex .txt whose content is its own name)
// and sends it to api.indexnow.org; the key is never returned or logged. URLs must be https on that site's own domain.
export async function runnerIndexNow(body: any) {
  const site = String(body?.site || '');
  const urls = Array.isArray(body?.urls) ? body.urls.map((u: unknown) => String(u || '').trim()) : [];
  if (!urls.length || urls.length > INDEXNOW_MAX_URLS) throw new BridgeError('urls must list 1-' + INDEXNOW_MAX_URLS + ' https URLs', 400);
  const groups = indexNowGroups(site);
  const byGroup = new Map<string, { prefix: string; host: string; urls: string[] }>();
  for (const u of urls) {
    let url: URL;
    try { url = new URL(u); } catch { throw new BridgeError('not a URL: ' + u.slice(0, 120), 400); }
    if (url.protocol !== 'https:' || url.username || url.password || url.port) throw new BridgeError('URL must be plain https: ' + u.slice(0, 120), 400);
    const g = groups.find((x) => bare(x.domain) === bare(url.hostname));
    if (!g) throw new BridgeError('URL is not on a domain of site ' + site + ': ' + u.slice(0, 120), 403);
    const k = g.prefix + '|' + url.hostname.toLowerCase();
    const cur = byGroup.get(k) || { prefix: g.prefix, host: url.hostname.toLowerCase(), urls: [] };
    if (!cur.urls.includes(url.href)) cur.urls.push(url.href);
    byGroup.set(k, cur);
  }
  const results: any[] = [];
  for (const g of byGroup.values()) {
    const key = await findIndexNowKey(site, g.prefix);
    if (!key) { results.push({ host: g.host, status: 'skipped', reason: 'no IndexNow key file in the site folder', urls: g.urls.length }); continue; }
    results.push({ host: g.host, ...(await sendIndexNow(g.host, key, g.urls)) });
  }
  const st = (s: string) => results.some((r) => r.status === s);
  return { site, status: st('error') ? 'error' : st('sent') ? (st('skipped') ? 'partial' : 'sent') : 'skipped', results };
}

// Controller reads and the article_last_* update, through the Controller's runnerFeed function (signed with the
// Bridge's pinned key, like articleFeed; the Controller app is private and the apps share no secret).
export async function runnerController(body: any, ctx: { base44: any }) {
  const op = String(body?.op || '');
  if (!['copy_fix', 'taps', 'article_last'].includes(op)) throw new BridgeError('op must be copy_fix, taps or article_last', 400);
  const clip = (v: unknown, n: number) => String(v ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, n);
  const payload: Record<string, unknown> = { purpose: 'grokbot_runner', op };
  if (op === 'article_last') {
    payload.slug = clip(body?.slug, 80); payload.date = clip(body?.date, 10); payload.title = clip(body?.title, 200); payload.url = clip(body?.url, 400);
    if (!/^[a-z0-9][a-z0-9-]{1,79}$/.test(String(payload.slug))) throw new BridgeError('slug must be the Controller client slug', 400);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(payload.date))) throw new BridgeError('date must be YYYY-MM-DD (SGT)', 400);
    if (!payload.title) throw new BridgeError('title is required', 400);
    if (!/^https:\/\//.test(String(payload.url))) throw new BridgeError('url must be https', 400);
  } else if (body?.site !== undefined && body?.site !== null && body?.site !== '') {
    payload.site = clip(body.site, 80);
  }
  let out: any;
  try { out = await signedControllerCall(ctx.base44, 'runnerFeed', payload, 90_000); }
  catch (e) { throw new BridgeError(String(e instanceof Error ? e.message : e).slice(0, 300), 502); }
  if (!out || out.ok !== true) throw new BridgeError('Controller: ' + String(out?.error || 'no answer').slice(0, 200), 502);
  const { ok: _ok, ...rest } = out;
  return { op, ...rest };
}

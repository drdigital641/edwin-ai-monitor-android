// op clients_card of bridgeGoLive (Edwin 21 Nov 2026, PERMANENT): after an AutoSEO site is switched live, put it on
// autoseo.my /clients/ (EN, /ms/, /zh/) with a real capture of the live home page, then add it to assets/launches.json.
// Called by the Controller right after a passed switch-on (goLive flip, clientSites runGoLive), or by Claude's session.
// Never runs for a site that is not live (the live home page must answer 200 on the client domain) and never for Page One.
// Every write: read live -> change -> writeFile with the base sha256 (verified backup); a page that already links the
// domain is left alone, so running it twice changes nothing.
import { BridgeError, probeLive, readLiveFile, writeFile } from './bridgeOps.ts';
import * as P from './goLivePure.ts';
import * as C from './goLiveClientsPure.ts';
import { registryFor } from './goLive.ts';
import * as Q from './pageoneClientsPure.ts';
import { findIndexNowKey, sendIndexNow } from './autoSitemapRun.ts';

const msg = (e: unknown) => (e instanceof Error ? e.message : String(e));
const sgtDate = () => new Date(Date.now() + 8 * 3600_000).toISOString().slice(0, 10);
const b64 = (s: string) => Uint8Array.from(atob(s), (ch) => ch.charCodeAt(0));
const isJpeg = (b: Uint8Array) => b.length > 1000 && b[0] === 0xff && b[1] === 0xd8;

// Real capture of the live home page: Google PageSpeed Insights desktop run, Lighthouse "final-screenshot" (JPEG).
// Optional secret PAGESPEED_API_KEY raises the quota. The page CSS crops any size to 16:10 (object-fit: cover).
// One attempt, 50 s max (the keyless quota is per day, a retry of a 429 does not help).
async function captureHome(url: string): Promise<Uint8Array | null> {
  const key = Deno.env.get('PAGESPEED_API_KEY');
  const api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?strategy=desktop&category=performance'
    + '&fields=' + encodeURIComponent('lighthouseResult/audits/final-screenshot/details/data') + '&url=' + encodeURIComponent(url) + (key ? '&key=' + encodeURIComponent(key) : '');
  try {
    const r = await fetch(api, { signal: AbortSignal.timeout(50_000) });
    if (!r.ok) { try { await r.body?.cancel(); } catch { /* ignore */ } return null; }
    const j: any = await r.json();
    const m = /^data:image\/jpeg;base64,(.+)$/.exec(String(j?.lighthouseResult?.audits?.['final-screenshot']?.details?.data || ''));
    if (m) { const b = b64(m[1]); if (isJpeg(b)) return b; }
  } catch { /* timeout or bad answer */ }
  return null;
}
// Read -> change -> write with the base sha; a stale-write refusal (another run wrote meanwhile) is retried once on a fresh read.
async function editLive(rel: string, change: (t: string) => string | null, site = 'autoseo'): Promise<'added' | 'already'> {
  for (let i = 0; ; i++) {
    const r: any = await readLiveFile(site, rel);
    const next = change(String(r.content));
    if (next === null) return 'already';
    try { await writeFile(site, rel, new TextEncoder().encode(next), r.base_sha256); return 'added'; }
    catch (err) { if (i === 0 && (err as any)?.status === 409) continue; throw err; }
  }
}

export async function clientsCardOp(body: any) {
  const e = registryFor(body.slug, body.site);
  if (e.parent !== 'autoseo') return { skipped: true, detail: 'Not an AutoSEO site: the autoseo.my /clients/ page is only for AutoSEO clients.' };
  const domain = P.cleanDomain(body.domain);
  if (!domain) throw new BridgeError('A valid domain is required', 400);
  if (/(^|\.)(autoseo\.my|pageonesingapore\.com)$/.test(domain)) throw new BridgeError('That is a preview host, not a client domain', 400);
  const url = `https://${domain}/`;
  // White-label rule: only a site that is already switched live AND public on its own domain is named.
  // The slug's own folder must carry canonical https://<domain>/ (ties the domain to this slug), and the domain must answer 200.
  const own: any = await readLiveFile(e.site, (e.base ? e.base + '/' : '') + 'index.html');
  const canonTag = (/<link\b[^>]*\brel=["']canonical["'][^>]*>/i.exec(String(own.content)) || [])[0] || '';
  const canon = (/\bhref=["']([^"']+)["']/i.exec(canonTag) || [])[1] || '';
  if (canon !== url) return { skipped: true, detail: `The ${body.slug} folder is not switched to ${domain} (canonical ${canon || 'missing'}), so it is not added to /clients/.` };
  let home = '';
  try {
    const hr = await fetch(url, { headers: { 'User-Agent': 'BridgeGoLiveCheck' }, redirect: 'manual', signal: AbortSignal.timeout(10_000) });
    if (hr.status !== 200) { try { await hr.body?.cancel(); } catch { /* ignore */ } return { skipped: true, detail: `${url} answered ${hr.status}, so it is not added to /clients/ yet.` }; }
    home = await hr.text();
  } catch (err) { return { skipped: true, detail: `${url} could not be opened (${msg(err).slice(0, 120)}), so it is not added to /clients/ yet.` }; }
  const title = (/<title[^>]*>([^<]*)<\/title>/i.exec(home) || [])[1] || '';
  const h1 = ((/<h1[^>]*>([\s\S]*?)<\/h1>/i.exec(home) || [])[1] || '').replace(/<[^>]+>/g, ' ');
  const ind = C.pickIndustry(body.industry, title + ' ' + h1);
  if (!ind) return { skipped: true, detail: 'Industry unknown: set the Controller client niche to one of ' + Object.keys(C.INDUSTRIES).join(', ') + ' and run clients_card again. Nothing was changed.' };
  const name = C.cleanName(body.name) || C.cleanName(title.split(/[|–-]/).pop());
  if (!name) throw new BridgeError('No business name: send name (the Controller client name).', 400);
  const line = C.defaultLine(ind.id, C.cleanTown(body.area));
  for (const l of C.LANGS) if (body.line && typeof body.line[l] === 'string' && body.line[l].trim()) line[l] = String(body.line[l]).trim().slice(0, 120);

  // Thumbnail: keep one that is already there (hand-made webp or an earlier run), else capture, else the site's share image.
  let image = '', thumb = '';
  for (const ext of ['webp', 'jpg']) {
    const rel = `assets/clients/${body.slug}.${ext}`;
    const st = (await probeLive('autoseo', rel)).state;
    if (st === 'present') { image = '/' + rel; thumb = 'already there'; break; }
    if (st !== 'absent') return { skipped: true, detail: `Could not tell whether ${rel} exists (${st}). Nothing was changed; run clients_card again.` };
  }
  if (!image) {
    let bytes = await captureHome(url); thumb = 'live home page capture (PageSpeed desktop)';
    if (!bytes) {
      const og = (/<meta\b[^>]*property=["']og:image["'][^>]*content=["']([^"']+)["']/i.exec(home) || /<meta\b[^>]*content=["']([^"']+)["'][^>]*property=["']og:image["']/i.exec(home) || [])[1];
      if (og && og.startsWith(url)) {
        try {
          const r = await fetch(og, { signal: AbortSignal.timeout(10_000) });
          const b = new Uint8Array(await r.arrayBuffer());
          if (r.ok && isJpeg(b)) { bytes = b; thumb = 'SHARE IMAGE (capture failed): replace with a home page capture'; }
        } catch { /* no share image either */ }
      }
    }
    if (!bytes) return { skipped: true, detail: 'No thumbnail: the home page capture and the share image both failed. Nothing was changed; run clients_card again later.' };
    const rel = `assets/clients/${body.slug}.jpg`;
    await writeFile('autoseo', rel, bytes, undefined, { publisher: true });
    image = '/' + rel;
  }
  const card: C.Card = { slug: body.slug, name, url, host: domain, image, industry: ind.id, line, alt: C.defaultAlt(name, domain) };

  const pages: Record<string, string> = {};
  for (const l of C.LANGS) {
    try {
      pages[l] = (await editLive(C.PAGES[l], (t) => C.addClientCard(t, l, card))) === 'added' ? 'added' : 'already listed';
    } catch (err) { pages[l] = 'FAILED: ' + msg(err).slice(0, 200); }
  }
  let launches = 'not changed (a page failed)';
  if (Object.values(pages).every((v) => !v.startsWith('FAILED'))) {
    try {
      launches = (await editLive('assets/launches.json', (t) => C.addLaunch(t, card, sgtDate()))) === 'added' ? 'added (newest)' : 'already there';
    } catch (err) { launches = 'FAILED: ' + msg(err).slice(0, 200); }
  }
  const complete = Object.values(pages).every((v) => !v.startsWith("FAILED")) && !launches.startsWith("FAILED");
  return { complete, industry: ind.id, industry_from: ind.from, name, line: line.en, thumbnail: { path: image, source: thumb }, pages, launches,
    urls: ['https://autoseo.my/clients/#' + ind.id] };
}

// op pageone_clients of bridgeGoLive (Edwin 22 Nov 2026, PERMANENT): after EVERY passed go-live (AutoSEO or Page One, Controller
// Go live switch or Activate) refresh pageonesingapore.com/clients/: the white-label totals block, the data-reg counts, dateModified
// and the meta descriptions, all from body.stats (computed by the Controller, shared/clientsRegistry.ts = registry.json rules).
// For a Page One public client that is live on its own domain it also adds the named card (+ badge, chip, hero glide, ItemList).
// White-label rule: the input for an AutoSEO / white-label / own client must carry totals only (pageoneClientsPure.cardInput throws
// otherwise) and never gets a card. Read live -> change -> write with the base sha (verified backup); running it twice changes nothing.
export async function pageoneClientsOp(body: any) {
  let st: Q.Stats, kind: Q.ClientKind, cardIn: any;
  try { st = Q.checkStats(body.stats); ({ kind, card: cardIn } = Q.cardInput(body)); }
  catch (err) { throw new BridgeError(msg(err), 400); }
  let card: Q.PoCard | null = null;
  let cardRes: any = kind.agency === 'pageone' && kind.visibility === 'public' ? { status: 'none', detail: 'no card sent (stats only)' } : { status: 'not named', detail: 'white-label / own: counted only' };
  if (cardIn) {
    try {
      // the card's own checks: host/url shape, the slug's folder switched to this domain, the domain answers 200, a thumbnail exists
      const pre = Q.checkCard({ ...cardIn, image: cardIn.image || 'x.jpg' });
      const url = `https://${pre.host}/`;
      const e = registryFor(pre.slug, 'pageone');
      if (e.parent !== 'pageone') throw new Error('not a Page One site');
      const own: any = await readLiveFile(e.site, (e.base ? e.base + '/' : '') + 'index.html');
      const canonTag = (/<link\b[^>]*\brel=["']canonical["'][^>]*>/i.exec(String(own.content)) || [])[0] || '';
      const canon = (/\bhref=["']([^"']+)["']/i.exec(canonTag) || [])[1] || '';
      if (canon !== url && canon !== `https://www.${pre.host}/`) throw new Error(`the ${pre.slug} folder is not switched to ${pre.host} (canonical ${canon || 'missing'})`);
      const hr = await fetch(url, { headers: { 'User-Agent': 'BridgeGoLiveCheck' }, redirect: 'manual', signal: AbortSignal.timeout(10_000) });
      try { await hr.body?.cancel(); } catch { /* ignore */ }
      if (hr.status !== 200) throw new Error(`${url} answered ${hr.status}`);
      // Thumbnail: clients/img/clients/<host>.webp|.jpg kept when there; else the same PageSpeed capture as clients_card, saved as .jpg
      let image = '';
      for (const ext of ['webp', 'jpg']) {
        const st2 = (await probeLive('pageone', Q.IMG_DIR + pre.host + '.' + ext)).state;
        if (st2 === 'present') { image = pre.host + '.' + ext; break; }
        if (st2 !== 'absent') throw new Error(`could not tell whether ${Q.IMG_DIR}${pre.host}.${ext} exists (${st2})`);
      }
      let thumb = 'already there';
      if (!image && !Q.hasCard(String((await readLiveFile('pageone', Q.PAGE)).content), pre.host)) {
        const bytes = await captureHome(url);
        if (!bytes) throw new Error('no thumbnail: the PageSpeed capture failed (run again later, or add ' + Q.IMG_DIR + pre.host + '.webp by hand)');
        await writeFile('pageone', Q.IMG_DIR + pre.host + '.jpg', bytes, undefined);
        image = pre.host + '.jpg'; thumb = 'live home page capture (PageSpeed desktop)';
      }
      card = Q.checkCard({ ...pre, image: image || pre.host + '.webp' });
      cardRes = { status: 'pending', thumbnail: thumb };
    } catch (err) { cardRes = { status: 'needs_card', detail: msg(err).slice(0, 300) }; }
  }
  let page: string;
  try {
    const hold: { cr: Q.CardResult | null } = { cr: null };
    page = (await editLive(Q.PAGE, (t) => { const r = Q.applyPageOne(t, st, card); hold.cr = r.card; return r.html; }, 'pageone')) === 'added' ? 'updated' : 'unchanged';
    if (hold.cr) cardRes = { ...cardRes, ...hold.cr };
  } catch (err) {
    return { complete: false, page: 'FAILED: ' + msg(err).slice(0, 300), card: card ? { status: 'not added (page failed)' } : cardRes, urls: [Q.PAGE_URL] };
  }
  // IndexNow for https://pageonesingapore.com/clients/ only. The key is found on the server and never returned or logged.
  let indexnow: any = { status: 'skipped', reason: 'page unchanged' };
  if (page === 'updated') {
    try {
      const key = await findIndexNowKey('pageone', '');
      const r: any = key ? await sendIndexNow('pageonesingapore.com', key, [Q.PAGE_URL]) : { status: 'skipped', reason: 'no IndexNow key file in the site root' };
      indexnow = { status: r.status, http: r.http, reason: r.reason, retry_later: r.retry_later };
    } catch (err) { indexnow = { status: 'error', error: msg(err).slice(0, 100) }; }
  }
  return { complete: !['needs_card'].includes(cardRes.status), page, card: cardRes,
    stats: { po_live: st.po_live, po_industries: st.po_industries, po_build: st.po_build, wl_live: st.wl_live, wl_build: st.wl_build, wl_last30: st.wl_last30, updated_iso: st.updated_iso },
    indexnow, urls: [Q.PAGE_URL] };
}

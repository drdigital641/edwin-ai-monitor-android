// pageonesingapore.com /clients/ on go-live (Edwin 22 Nov 2026, PERMANENT: "every go-live must also update pageonesingapore.com/clients/
// automatically"). Pure text helpers for op pageone_clients of bridgeGoLive, no I/O. Markers and render functions follow
// clients-registry/CONTRACT.md and build_pageone.py (wl_stats_html, meta_text, og_alt, new_ccard, new_gcard): for the same numbers the
// output is byte-identical to the Python builder (tests/pageoneClientsPure.test.mts checks it against fixtures/wl-stats.html and the
// built page). White-label rule: totals only. Nothing here ever names, links or pictures a white-label (AutoSEO) client.

export const PAGE = 'clients/index.html';
export const PAGE_URL = 'https://pageonesingapore.com/clients/';
export const IMG_DIR = 'clients/img/clients/';
const BIZ = 'https://pageonesingapore.com/#business';

// registry industry_id -> block id on the live page (build_pageone.py BLOCK_OF). A block id itself is accepted too.
export const BLOCK_OF: Record<string, string> = {
  'car-workshops': 'car-workshops', 'detailing': 'detailing-wraps', 'car-parts': 'car-parts', 'car-dealers': 'car-dealers',
  'property': 'property-agents', 'home': 'home-cleaning', 'finance': 'finance-professional', 'travel': 'travel-stays', 'other': 'others',
};

export type Stats = {
  wl_live: number; wl_build: number; wl_industries: [string, number][]; wl_last30: number;
  po_live: number; po_industries: number; po_build: number; updated: string; updated_iso: string;
};
// One named Page One card. image = file name inside clients/img/clients/ (e.g. "newclient.sg.jpg").
export type PoCard = { slug: string; name: string; host: string; url: string; industry_id: string; desc: string; since: string; image: string };
export type ClientKind = { agency: 'pageone' | 'autoseo'; visibility: 'public' | 'white-label' | 'own' };

export class InputError extends Error { status = 400; }
const need = (c: unknown, what: string): void => { if (!c) throw new InputError('Page layout not recognised: ' + what + ' not found. Nothing was changed.'); };

// Python html.escape(s, quote=True)
export const esc = (s: string) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
const reEsc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const jsonStr = (s: string) => JSON.stringify(s).slice(1, -1);

// ---------- input checks ----------
const int = (v: unknown, k: string) => { if (!Number.isInteger(v) || (v as number) < 0 || (v as number) > 100000) throw new InputError('stats.' + k + ' must be a whole number'); return v as number; };
export function checkStats(s: any): Stats {
  if (!s || typeof s !== 'object') throw new InputError('stats is required (computed by the Controller, shared/clientsRegistry.ts)');
  const inds = s.wl_industries;
  if (!Array.isArray(inds) || inds.length > 60) throw new InputError('stats.wl_industries must be a list of [label, count]');
  const wl_industries = inds.map((p: any) => {
    if (!Array.isArray(p) || p.length !== 2 || typeof p[0] !== 'string' || !p[0].trim() || p[0].length > 80) throw new InputError('stats.wl_industries rows must be [label, count]');
    return [p[0], int(p[1], 'wl_industries count')] as [string, number];
  });
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(s.updated_iso))) throw new InputError('stats.updated_iso must be YYYY-MM-DD');
  if (!/^\d{1,2} [A-Z][a-z]{2} \d{4}$/.test(String(s.updated))) throw new InputError('stats.updated must look like "22 Nov 2026"');
  return { wl_live: int(s.wl_live, 'wl_live'), wl_build: int(s.wl_build, 'wl_build'), wl_industries, wl_last30: int(s.wl_last30, 'wl_last30'),
    po_live: int(s.po_live, 'po_live'), po_industries: int(s.po_industries, 'po_industries'), po_build: int(s.po_build, 'po_build'),
    updated: String(s.updated), updated_iso: String(s.updated_iso) };
}

// WHITE-LABEL SAFETY (Edwin 22 Nov 2026): the input for a white-label or own client may carry only the totals. Any name, host, url,
// domain or card in it is refused (throws), and a card is never inserted for agency autoseo. Returns the card input or null.
const IDENTIFYING = ['name', 'host', 'url', 'domain', 'card', 'image', 'desc'];
export function cardInput(body: any): { kind: ClientKind; card: any | null } {
  const k = body?.client || {};
  if (!['pageone', 'autoseo'].includes(k.agency) || !['public', 'white-label', 'own'].includes(k.visibility))
    throw new InputError('client.agency (pageone|autoseo) and client.visibility (public|white-label|own) are required');
  const kind = { agency: k.agency, visibility: k.visibility } as ClientKind;
  const named = kind.agency === 'pageone' && kind.visibility === 'public';
  if (!named) {
    const carried = IDENTIFYING.filter((f) => body?.[f] !== undefined && body?.[f] !== null && body?.[f] !== '')
      .concat(IDENTIFYING.filter((f) => k[f] !== undefined && k[f] !== null && k[f] !== '').map((f) => 'client.' + f));
    if (carried.length) throw new InputError('White-label rule: a ' + kind.agency + ' ' + kind.visibility + ' client is counted only. The input must not carry ' + carried.join(', ') + '. Nothing was changed.');
    return { kind, card: null };
  }
  return { kind, card: body.card ?? null };
}

// ---------- renderers (byte-identical to build_pageone.py) ----------
export function metaText(st: Stats) {
  return `${st.po_live} client websites live on their own domains across ${st.po_industries} industries. See what Page One Singapore builds for businesses like yours, from S$100/month.`;
}
export function ogAlt(st: Stats) {
  return `${st.po_live} client websites across ${st.po_industries} industries, built by Page One Singapore`;
}
export function wlStatsHtml(st: Stats) {
  const inds = st.wl_industries.map(([l, n]) => `<li><span>${esc(l)}</span> <b>${n}</b></li>`).join('');
  return '<section class="section cv-wl" id="white-label" aria-labelledby="wl-h">\n'
    + '      <div class="wrap">\n'
    + '        <p class="kicker">White-label work</p>\n'
    + '        <h2 id="wl-h">Built for other agencies and dealers</h2>\n'
    + '        <p class="section-lead">Websites we build for other agencies and dealers, under their brand. '
    + 'The work is white-label, so we show totals only: no names, domains, logos or screenshots.</p>\n'
    + '        <div class="wl-tiles">\n'
    + `          <div class="wl-tile"><div class="value"><span data-reg="wl_live">${st.wl_live}</span></div><div class="label">White-label sites live</div></div>\n`
    + `          <div class="wl-tile"><div class="value"><span data-reg="wl_build">${st.wl_build}</span></div><div class="label">In build now</div></div>\n`
    + `          <div class="wl-tile"><div class="value">${st.wl_last30}</div><div class="label">Launched in the last 30 days</div></div>\n`
    + `          <div class="wl-tile"><div class="value">${st.wl_industries.length}</div><div class="label">Industries covered</div></div>\n`
    + '        </div>\n'
    + '        <h3 class="wl-h3">Live white-label sites by industry</h3>\n'
    + `        <ul class="wl-inds">${inds}</ul>\n`
    + `        <p class="wl-updated">Last updated <time datetime="${st.updated_iso}">${st.updated}</time> (SGT)</p>\n`
    + '      </div>\n'
    + '    </section>';
}
export function ccardHtml(c: PoCard) {
  return `<a class="ccard" href="${c.url}" target="_blank" rel="noopener"><span class="phone"><img src="img/clients/${c.image}" width="480" height="912" alt="${esc(c.name)} website homepage" loading="lazy" decoding="async"></span>`
    + `<h3>${esc(c.name)}</h3><p class="desc">${esc(c.desc)}</p><p class="since">${c.since}</p><p class="visit">${c.host} <span>Visit site &#8599;</span></p></a>`;
}
export function gcardHtml(c: PoCard) {
  const n = esc(c.name);
  return `<a class="gcard" href="${c.url}" target="_blank" rel="noopener" aria-label="${n} (opens in a new tab)"><span class="phone"><img src="img/clients/${c.image}" width="480" height="912" alt="${n} website homepage" loading="lazy" decoding="async"></span></a>`;
}
// "2026-11-22" -> "Since Nov 2026" (Python strftime('Since %b %Y'))
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
export const sinceOf = (iso: string) => { const m = /^(\d{4})-(\d{2})-\d{2}$/.exec(iso); return m ? `Since ${MON[Number(m[2]) - 1]} ${m[1]}` : ''; };

// ---------- 1-3: stats block, data-reg spans, dateModified, meta descriptions ----------
const START = '<!-- wl-stats:start -->', END = '<!-- wl-stats:end -->';
const REG_KEYS = ['po_live', 'po_industries', 'po_build', 'wl_live', 'wl_build'] as const;
export function refreshStats(html: string, st: Stats): string {
  const a = html.indexOf(START), b = html.indexOf(END);
  need(a >= 0 && b > a && html.indexOf(START, a + 1) < 0 && html.indexOf(END, b + 1) < 0, 'exactly one wl-stats:start/end marker pair');
  let out = html.slice(0, a + START.length) + wlStatsHtml(st) + html.slice(b);
  out = out.replace(new RegExp('(<span data-reg="(' + REG_KEYS.join('|') + ')">)\\d+(</span>)', 'g'), (_m, open, k, close) => open + (st as any)[k] + close);
  out = out.replace(/("dateModified": ")\d{4}-\d{2}-\d{2}/g, (_m, p) => p + st.updated_iso);
  const mt = esc(metaText(st)), alt = esc(ogAlt(st));
  for (const tag of ['<meta name="description" content="', '<meta property="og:description" content="', '<meta name="twitter:description" content="']) {
    need(out.includes(tag), tag + '...');
    out = out.replace(new RegExp('(' + reEsc(tag) + ')[^"]*'), (_m, p) => p + mt);
  }
  out = out.replace(/(<meta (?:property="og:image:alt"|name="twitter:image:alt") content=")[^"]*/g, (_m, p) => p + alt);
  out = out.replace(/("@type": "WebPage"[\s\S]*?"description": ")[^"]*/, (_m, p) => p + jsonStr(metaText(st)));
  return out;
}

// ---------- 4: one named card (pageone + public + live) ----------
export type CardResult = { status: 'added' | 'already' | 'needs_card'; block?: string; detail: string };
const BLOCK_RE = (id: string) => new RegExp('<(?:section class="ind[^"]*"|div class="industry-block[^"]*") id="' + reEsc(id) + '"');
const ANY_BLOCK_RE = /<(?:section class="ind[^"]*"|div class="industry-block[^"]*") id="([^"]+)"/g;

export function hasCard(html: string, host: string) {
  const h = reEsc(host.replace(/^www\./, ''));
  return new RegExp('<a class="ccard" href="https?://(www\\.)?' + h + '/?"').test(html);
}
export function blockFor(html: string, industry: string): string | null {
  for (const id of [industry, BLOCK_OF[industry]]) if (id && BLOCK_RE(id).test(html)) return id;
  return null;
}
export function checkCard(c: any): PoCard {
  const s = (v: unknown, k: string, max: number) => { const t = String(v ?? '').trim(); if (!t || t.length > max || /[<>]/.test(t)) throw new InputError('card.' + k + ' is missing or not plain text'); return t; };
  const host = s(c?.host, 'host', 120).toLowerCase();
  if (!/^[a-z0-9.-]+\.[a-z]{2,}$/.test(host)) throw new InputError('card.host must be a bare host name');
  if (/(^|\.)(autoseo\.my|pageonesingapore\.com)$/.test(host)) throw new InputError('card.host is a preview host, not a client domain');
  const url = s(c?.url, 'url', 200);
  if (!new RegExp('^https://(www\\.)?' + reEsc(host) + '/$').test(url)) throw new InputError('card.url must be https://<host>/');
  const image = s(c?.image, 'image', 140);
  if (!/^[a-z0-9.-]+\.(webp|jpg)$/.test(image)) throw new InputError('card.image must be <host>.webp or <host>.jpg');
  const since = s(c?.since, 'since', 20);
  if (!/^Since [A-Z][a-z]{2} \d{4}$/.test(since)) throw new InputError('card.since must look like "Since Nov 2026"');
  return { slug: s(c?.slug, 'slug', 80), name: s(c?.name, 'name', 80), host, url, industry_id: s(c?.industry_id, 'industry_id', 60), desc: s(c?.desc, 'desc', 160), since, image };
}

// Returns the new page, or null when the card is already there or cannot be placed (result says which).
export function addPoCard(html: string, c: PoCard): { html: string | null; result: CardResult } {
  if (hasCard(html, c.host)) return { html: null, result: { status: 'already', detail: c.host + ' already has a card' } };
  const id = blockFor(html, c.industry_id);
  if (!id) return { html: null, result: { status: 'needs_card', detail: `Industry "${c.industry_id}" has no block on /clients/ (ids on the page: ${[...html.matchAll(ANY_BLOCK_RE)].map((m) => m[1]).join(', ')}). Add the card by hand or set the industry; nothing guessed.` } };
  let out = html;
  // block range: this block's opening tag up to the next block (or </main>)
  const bs = out.search(BLOCK_RE(id));
  ANY_BLOCK_RE.lastIndex = bs + 1;
  const nx = ANY_BLOCK_RE.exec(out);
  const be = nx ? nx.index : out.indexOf('</main>', bs);
  need(be > bs, 'the end of block ' + id);
  const blk = out.slice(bs, be);
  // cards strip: the first </div> after <div class="strip" ...> closes it (cards hold no div)
  const so = blk.search(/<div class="strip"[^>]*>/);
  need(so >= 0, 'the cards strip of ' + id);
  const sc = blk.indexOf('</div>', so);
  need(sc > so, 'the end of the cards strip of ' + id);
  const prevImgs = [...blk.slice(so, sc).matchAll(/<a class="ccard"[^>]*>\s*<span class="phone"><img src="img\/clients\/([^"]+)"/g)].map((m) => m[1]);
  // badge
  const bm = /<span class="count-badge">(\d+) websites?<\/span>/.exec(blk);
  need(bm, 'the count badge of ' + id);
  const n = Number(bm![1]) + 1;
  const label = (new RegExp('<h2 id="' + reEsc(id) + '-h">([\\s\\S]*?) <span class="count-badge"').exec(blk) || [])[1];
  need(label, 'the heading of ' + id);
  let nb = blk.slice(0, sc) + ccardHtml(c) + blk.slice(sc);
  nb = nb.replace(bm![0], `<span class="count-badge">${n} website${n === 1 ? '' : 's'}</span>`);
  out = out.slice(0, bs) + nb + out.slice(be);
  // chip
  const nav = /<nav class="chips" aria-label="Industries">([\s\S]*?)<\/nav>/.exec(out);
  need(nav, 'the industry chips');
  const chipRe = new RegExp('<a class="chip" href="#' + reEsc(id) + '">([\\s\\S]*?) <b>(\\d+)</b></a>');
  let chips = nav![1];
  if (chipRe.test(chips)) chips = chips.replace(chipRe, (_m, l) => `<a class="chip" href="#${id}">${l} <b>${n}</b></a>`);
  else {
    const order = [...out.matchAll(ANY_BLOCK_RE)].map((m) => m[1]);
    const after = order.slice(order.indexOf(id) + 1);
    const chip = `<a class="chip" href="#${id}">${label} <b>${n}</b></a>`;
    const at = after.map((b) => chips.indexOf(`<a class="chip" href="#${b}">`)).filter((i) => i >= 0).sort((x, y) => x - y)[0];
    chips = at === undefined ? chips + chip : chips.slice(0, at) + chip + chips.slice(at);
  }
  out = out.slice(0, nav!.index) + '<nav class="chips" aria-label="Industries">' + chips + '</nav>' + out.slice(nav!.index + nav![0].length);
  // hero glide: after the gcard of this block's last card, else at the end
  const go = out.search(/<div class="glide"[^>]*>/);
  need(go >= 0, 'the hero glide');
  const gc = out.indexOf('</div>', go);
  let at = gc;
  for (const f of prevImgs.reverse()) {
    const i = out.indexOf(`<img src="img/clients/${f}"`, go);
    if (i > go && i < gc) { at = out.indexOf('</a>', i) + 4; break; }
  }
  out = out.slice(0, at) + gcardHtml(c) + out.slice(at);
  // JSON-LD ItemList of the CollectionPage: numberOfItems + 1, item appended
  const cp = /<script type="application\/ld\+json">\s*\{\s*"@context": "https:\/\/schema\.org",\s*"@type": "CollectionPage"[\s\S]*?<\/script>/.exec(out);
  need(cp, 'the CollectionPage JSON-LD');
  let js = cp![0];
  const nm = /"numberOfItems": (\d+)/.exec(js);
  need(nm, 'numberOfItems');
  const pos = Number(nm![1]) + 1;
  const tail = js.lastIndexOf('\n      }\n    ]');
  need(tail > 0, 'the end of itemListElement');
  const item = { '@type': 'ListItem', position: pos, item: { '@type': 'WebSite', '@id': c.url + '#website', name: c.name, url: c.url, description: c.desc, creator: { '@id': BIZ }, maintainer: { '@id': BIZ } } };
  const itemTxt = JSON.stringify(item, null, 2).split('\n').map((l) => '      ' + l).join('\n');
  js = js.slice(0, tail) + '\n      },\n' + itemTxt + js.slice(tail + '\n      }'.length);
  js = js.replace(nm![0], `"numberOfItems": ${pos}`);
  JSON.parse(js.replace(/^<script[^>]*>/, '').replace(/<\/script>$/, ''));
  out = out.slice(0, cp!.index) + js + out.slice(cp!.index + cp![0].length);
  return { html: out, result: { status: 'added', block: id, detail: `${c.host} added to #${id} (${n}), ItemList ${pos}` } };
}

// Whole page step: card (if any) then the totals. Returns null when nothing changes (running it twice = no change).
export function applyPageOne(html: string, st: Stats, card: PoCard | null): { html: string | null; card: CardResult | null } {
  let out = html, cr: CardResult | null = null;
  if (card) { const r = addPoCard(out, card); cr = r.result; if (r.html) out = r.html; }
  out = refreshStats(out, st);
  return { html: out === html ? null : out, card: cr };
}

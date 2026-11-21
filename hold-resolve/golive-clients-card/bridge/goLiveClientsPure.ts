// AutoSEO /clients/ card on go-live (Edwin 21 Nov 2026, PERMANENT: "make the go-live switch do this step automatically for every
// future AutoSEO go-live"). Pure text helpers, no I/O, tested in tests/goLiveClients.test.ts. Port of autoseo-template/golive/clients_card.py.

export type Lang = 'en' | 'ms' | 'zh';
export const LANGS: Lang[] = ['en', 'ms', 'zh'];
export const PAGES: Record<Lang, string> = { en: 'clients/index.html', ms: 'ms/clients/index.html', zh: 'zh/clients/index.html' };

// Industry ids = the autoseo.my /industries/<id>/ pages. Singular names make the default card line.
export const INDUSTRIES: Record<string, Record<Lang, string>> = {
  'car-workshops': { en: 'Car workshop', ms: 'Bengkel kereta', zh: '汽车维修厂' },
  'car-dealerships': { en: 'Car dealership', ms: 'Pusat jualan kereta', zh: '汽车经销店' },
  'tyre-shops': { en: 'Tyre shop', ms: 'Kedai tayar', zh: '轮胎店' },
  'car-accessories': { en: 'Car accessories shop', ms: 'Kedai aksesori kereta', zh: '汽车配件店' },
  'car-aircon-specialists': { en: 'Car aircon specialist', ms: 'Pakar aircond kereta', zh: '汽车冷气专家' },
  'car-detailing': { en: 'Car detailing and coating', ms: 'Detailing dan coating kereta', zh: '汽车美容与镀膜' },
  'ev-hybrid-specialists': { en: 'EV and hybrid specialist', ms: 'Pakar EV dan hibrid', zh: '电动车与混合动力专家' },
  'battery-spare-parts': { en: 'Batteries and spare parts', ms: 'Bateri dan alat ganti', zh: '电池与零配件' },
  'equipment-diagnostic-tools': { en: 'Equipment and diagnostic tools', ms: 'Peralatan dan alat diagnostik', zh: '设备与诊断工具' },
};
// Plural block titles, used only when the page has no footer link to read the name from.
const PLURAL: Record<string, Record<Lang, string>> = {
  'tyre-shops': { en: 'Tyre shops', ms: 'Kedai tayar', zh: '轮胎店' },
  'car-accessories': { en: 'Car accessories', ms: 'Aksesori kereta', zh: '汽车配件' },
};

const T: Record<Lang, { live: string; visit: string; one: string; many: (n: number) => string; lead: RegExp; leadFmt: (c: number, i: number) => string }> = {
  en: { live: 'Live', visit: 'Visit', one: '1 website', many: (n) => n + ' websites',
    lead: /(\d+) client websites are live on their own domains, across (\d+) industries/, leadFmt: (c, i) => `${c} client websites are live on their own domains, across ${i} industries` },
  ms: { live: 'Hidup', visit: 'Lawati', one: '1 laman web', many: (n) => n + ' laman web',
    lead: /(\d+) laman web pelanggan sudah hidup di domain sendiri, merentas (\d+) industri/, leadFmt: (c, i) => `${c} laman web pelanggan sudah hidup di domain sendiri, merentas ${i} industri` },
  zh: { live: '已上线', visit: '访问', one: '1 个网站', many: (n) => n + ' 个网站',
    lead: /已有 (\d+) 个客户网站在其自有域名上线，涵盖 (\d+) 个行业/, leadFmt: (c, i) => `已有 ${c} 个客户网站在其自有域名上线，涵盖 ${i} 个行业` },
};

export type Card = { slug: string; name: string; url: string; host: string; image: string; industry: string; line: Record<Lang, string>; alt: Record<Lang, string> };

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const reEsc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

// "Overseas Tyre And Services Sdn Bhd" -> "Overseas Tyre And Services" (company suffixes are not shown on the card).
export function cleanName(n: unknown): string {
  return String(n ?? '').replace(/\s+/g, ' ').trim().replace(/[,\s]*\b(sdn\.?\s*bhd\.?|bhd\.?|pte\.?\s*ltd\.?|enterprise|\(m\))\s*$/i, '').trim().slice(0, 80);
}
// "Taman Bukit Indah, Johor Bahru, Malaysia" -> "Taman Bukit Indah, Johor Bahru"
export function cleanTown(a: unknown): string {
  return String(a ?? '').replace(/\s+/g, ' ').replace(/,?\s*Malaysia\s*$/i, '').trim().slice(0, 80);
}
// Industry from the Controller (an id, its English name, or free niche text), else from the live home page <title>/<h1>.
// No match = null: the caller skips (never lists a business under a guessed industry).
export function pickIndustry(given: unknown, homeText: string): { id: string; from: string } | null {
  const g = String(given ?? '').trim().toLowerCase();
  if (g) {
    if (Object.hasOwn(INDUSTRIES, g)) return { id: g, from: 'controller' };
    for (const [id, n] of Object.entries(INDUSTRIES)) if (n.en.toLowerCase() === g || (PLURAL[id]?.en || '').toLowerCase() === g) return { id, from: 'controller' };
  }
  const t = homeText.toLowerCase();
  const rules: [RegExp, string][] = [
    [/\btyres?\b|\btires?\b|\btayar\b|wheel alignment/, 'tyre-shops'],
    [/\baircon(d)?\b|air-cond|air cond/, 'car-aircon-specialists'],
    [/detailing|ceramic coating|paint protection/, 'car-detailing'],
    [/\bhybrid\b|\bev\b|electric vehicle/, 'ev-hybrid-specialists'],
    [/\bdealer(ship)?\b|showroom|used cars? for sale/, 'car-dealerships'],
    [/diagnostic tools?|scan tools?|\bautel\b|equipment/, 'equipment-diagnostic-tools'],
    [/\bbatter(y|ies)\b|spare parts/, 'battery-spare-parts'],
    [/accessor(y|ies)|bodykit|body kit/, 'car-accessories'],
    [/workshop|bengkel|car service|car repair|servis kereta|pusat servis/, 'car-workshops'],
  ];
  for (const [re, id] of rules) if (g && re.test(g)) return { id, from: 'controller niche text' };
  for (const [re, id] of rules) if (re.test(t)) return { id, from: 'home page title' };
  return null;
}
export function defaultLine(industry: string, town: string): Record<Lang, string> {
  const s = INDUSTRIES[industry];
  if (!town) return { en: s.en, ms: s.ms, zh: s.zh };
  return { en: `${s.en}, ${town}`, ms: `${s.ms}, ${town}`, zh: `${town}${s.zh}` };
}
export function defaultAlt(name: string, host: string): Record<Lang, string> {
  return { en: `${name} website homepage (${host})`, ms: `Laman utama laman web ${name} (${host})`, zh: `${name} 网站首页（${host}）` };
}

function cardHtml(lang: Lang, c: Card): string {
  const t = T[lang];
  return `          <a class="card site-card reveal" href="${esc(c.url)}" target="_blank" rel="noopener">\n`
    + `            <span class="browser"><span class="browser-bar"><i></i><i></i><i></i><span>${esc(c.host)}</span></span><img src="${esc(c.image)}" width="640" height="400" alt="${esc(c.alt[lang])}" decoding="async" loading="lazy"></span>\n`
    + `            <p class="pill live-pill"><span class="live-dot" aria-hidden="true"></span>${t.live}</p>\n`
    + `            <h3>${esc(c.name)}</h3>\n            <p>${esc(c.line[lang])}</p>\n`
    + `            <span class="card-link">${t.visit} ${esc(c.host)} ↗</span>\n          </a>\n`;
}

// Adds the card (first in its industry block, or a new block at the end), bumps the counts and the JSON-LD ItemList.
// Returns null when the page already links to the site (idempotent) and throws when the page layout is not the expected one.
export function addClientCard(html: string, lang: Lang, c: Card): string | null {
  const t = T[lang];
  if (html.includes(`href="${c.url}"`)) return null;
  const need = (cond: unknown, what: string) => { if (!cond) throw new Error(`clients page (${lang}): ${what} not found`); };
  const lm = t.lead.exec(html); need(lm, 'the count sentence');
  const nm = /"numberOfItems": (\d+),/.exec(html); need(nm, 'ItemList numberOfItems');
  const blockRe = new RegExp(`<div class="industry-block( alt)?" id="${reEsc(c.industry)}">`);
  const bm = blockRe.exec(html);
  let out = html, newInd = false;
  if (bm) {
    const cardsAt = out.indexOf('<div class="cards two site-cards">\n', bm.index); need(cardsAt > 0, 'the cards list');
    const at = cardsAt + '<div class="cards two site-cards">\n'.length;
    out = out.slice(0, at) + cardHtml(lang, c) + out.slice(at);
    const badge = /<span class="count-badge">([^<]*)<\/span>/g; badge.lastIndex = bm.index;
    const bb = badge.exec(out); need(bb, 'the count badge');
    const n = parseInt((bb![1].match(/\d+/) || ['0'])[0], 10) + 1;
    out = out.slice(0, bb!.index) + `<span class="count-badge">${t.many(n)}</span>` + out.slice(bb!.index + bb![0].length);
    out = out.replace(new RegExp(`(<a href="#${reEsc(c.industry)}">[^<]*<span class="chip-count">)(\\d+)(</span>)`), (_m, a, d, b) => a + (parseInt(d, 10) + 1) + b);
  } else {
    newInd = true;
    const all = [...out.matchAll(/<div class="industry-block( alt)?" id="[^"]+">/g)]; need(all.length, 'an industry block');
    const last = all[all.length - 1];
    const alt = last[1] ? '' : ' alt';
    const foot = new RegExp(`href="(?:/(?:ms|zh))?/industries/${reEsc(c.industry)}/">([^<]+)</a>`).exec(out);
    const title = foot ? foot[1] : esc((PLURAL[c.industry] || INDUSTRIES[c.industry])[lang]);
    const block = `      <div class="industry-block${alt}" id="${c.industry}">\n        <div class="industry-head reveal">\n          <h2>${title}</h2>\n`
      + `          <span class="count-badge">${t.one}</span>\n        </div>\n        <div class="cards two site-cards">\n${cardHtml(lang, c)}        </div>\n      </div>\n`;
    const end = out.indexOf('      </div>\n    </section>', last.index!); need(end > 0, 'the end of the industry list');
    out = out.slice(0, end) + block + out.slice(end);
    const navStart = out.indexOf('<nav class="industry-nav"'); need(navStart > 0, 'the industry chips');
    const navEnd = out.indexOf('</nav>', navStart); need(navEnd > navStart, 'the end of the industry chips');
    out = out.slice(0, navEnd) + `  <a href="#${c.industry}">${title}<span class="chip-count">1</span></a>\n        ` + out.slice(navEnd);
  }
  const lm2 = t.lead.exec(out)!;
  const cnt = parseInt(lm2[1], 10) + 1, inds = parseInt(lm2[2], 10) + (newInd ? 1 : 0);
  out = out.slice(0, lm2.index) + t.leadFmt(cnt, inds) + out.slice(lm2.index + lm2[0].length);
  const kpi = [...out.matchAll(/(<div class="kpi"><div class="label">[^<]*<\/div><div class="value">)(\d+)(<\/div><\/div>)/g)].slice(0, 2);
  need(kpi.length === 2, 'the two counters');
  for (const [k, v] of [[kpi[1], inds], [kpi[0], cnt]] as [RegExpMatchArray, number][]) {
    const s = k.index! + k[1].length; out = out.slice(0, s) + v + out.slice(s + k[2].length);
  }
  const nm2 = /"numberOfItems": (\d+),/.exec(out)!;
  const pos = parseInt(nm2[1], 10) + 1;
  out = out.slice(0, nm2.index) + `"numberOfItems": ${pos},` + out.slice(nm2.index + nm2[0].length);
  const close = out.indexOf('\n   }\n  ]', nm2.index); need(close > 0, 'the end of the ItemList');
  const item = `,\n   {\n    "@type": "ListItem",\n    "position": ${pos},\n    "url": ${JSON.stringify(c.url)},\n    "name": ${JSON.stringify(c.name)}\n   }`;
  out = out.slice(0, close + 5) + item + out.slice(close + 5);
  return out;
}

// launches.json: newest first (the homepage "Just launched" popup shows the first entry for 30 days). Idempotent per site.
export function addLaunch(text: string, c: Card, dateSgt: string): string | null {
  const d = JSON.parse(text);
  const list: any[] = Array.isArray(d.launches) ? d.launches : [];
  const idRe = new RegExp('^' + reEsc(c.slug) + '-\\d{4}-\\d{2}-\\d{2}$');
  if (list.some((x) => x && (x.url === c.url || idRe.test(String(x.id || ''))))) return null;
  const s = INDUSTRIES[c.industry];
  const entry = { id: `${c.slug}-${dateSgt}`, name: c.name, url: c.url, host: c.host, image: c.image, launched: dateSgt,
    trade: { en: s.en.toLowerCase(), ms: s.ms.toLowerCase(), zh: s.zh }, line: c.line };
  d.launches = [entry, ...list];
  return JSON.stringify(d, null, 2) + '\n';
}

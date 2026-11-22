// Clients registry in the Controller (Edwin 22 Nov 2026, PERMANENT). Pure: Client records in, registry rows + the public numbers out.
// Mirrors clients-registry/registry.json + sync_controller.py + stats.py (Python reference, same numbers):
//   agency    pageone | autoseo        visibility  public (named card on pageonesingapore.com/clients) | white-label (counts only) | own (never counted)
//   status    Client.status live -> live, preview/activating -> in_build, anything else -> dormant
// Default: brand AutoSEO -> autoseo white-label; brand Page One -> pageone public. OVERRIDES below hold the exceptions (registry wins).
// Skipped: duplicate_of rows, partner rows (is_partner), mini-sites (domain contains "/", e.g. Hon Win Motor on sgcarworkshop.sg),
// and in-build rows that are not real builds (same rule as the old shared/clientCounts.ts: count_as_building, NOT_BUILDING, mock-up words).
// Used by clientCounts (homepage numbers) and by every go-live (Bridge op pageone_clients). Only numbers leave the Controller for
// white-label rows: rows() keeps a name/host only for pageone public rows.
import { AUTOSEO, brandOf, hostOfDomain } from './brand.ts';

export type Agency = 'pageone' | 'autoseo';
export type Visibility = 'public' | 'white-label' | 'own';
export type Status = 'live' | 'in_build' | 'dormant';
export type Row = { slug: string; agency: Agency; visibility: Visibility; status: Status; live_date: string | null;
  industry_id: string; industry_label: string; industry_from: 'registry' | 'niche' | 'default'; name?: string; host?: string };
export type Stats = { wl_live: number; wl_build: number; wl_industries: [string, number][]; wl_last30: number;
  po_live: number; po_industries: number; po_build: number; updated: string; updated_iso: string };

// Industry labels (registry.json seed.py IND_PO / IND_AS).
export const IND_PO: Record<string, string> = { 'car-workshops': 'Car workshops', 'detailing': 'Detailing, wraps and grooming', 'car-parts': 'Car parts and products',
  'car-dealers': 'Car dealers', 'property': 'Property agents', 'home': 'Home, renovation and cleaning',
  'finance': 'Finance and professional services', 'travel': 'Travel and stays', 'other': 'Other local businesses' };
export const IND_AS: Record<string, string> = { 'car-workshops': 'Car workshops', 'car-dealerships': 'Car dealerships', 'car-aircon-specialists': 'Car aircon specialists',
  'car-detailing': 'Car detailing and coating', 'ev-hybrid-specialists': 'EV and hybrid specialists', 'battery-spare-parts': 'Batteries and spare parts',
  'equipment-diagnostic-tools': 'Equipment and diagnostic tools', 'tyre-shops': 'Tyre shops', 'machinery-movers': 'Machinery movers',
  'hair-salons': 'Hair salons', 'food': 'Food', 'other': 'Other industries' };

// Exceptions by Controller slug (registry.json, Edwin 22 Nov 2026). The Controller brand says Page One for these four AutoSEO clients.
export const OVERRIDES: Record<string, { agency?: Agency; visibility?: Visibility; status_override?: Status }> = {
  'ktech': { agency: 'autoseo', visibility: 'white-label' },
  'klar-details': { agency: 'autoseo', visibility: 'white-label' },
  'battery-rescue': { agency: 'autoseo', visibility: 'white-label' },
  'dongfeng-jb': { agency: 'autoseo', visibility: 'white-label' },
  'autoseo-site': { agency: 'autoseo', visibility: 'own' },
  'autoseo-my': { agency: 'autoseo', visibility: 'own' },
  'sgcarworkshop': { agency: 'pageone', visibility: 'own' },
  'clients-v2': { agency: 'pageone', visibility: 'own' },
  'sofacare': { status_override: 'live' },     // billing_only row: its Controller status is not trusted
};
// Registry rows with no Controller record (controller_slug "-"), live by override.
export const EXTRAS: Row[] = [
  { slug: 'alicia', agency: 'pageone', visibility: 'public', status: 'live', live_date: null, industry_id: 'property', industry_label: 'Property agents', industry_from: 'registry', name: 'Alicia Ong Property', host: 'aliciaongproperty.com' },
  { slug: 'danny', agency: 'pageone', visibility: 'public', status: 'live', live_date: null, industry_id: 'finance', industry_label: 'Finance and professional services', industry_from: 'registry', name: 'Danny Chua Financial', host: 'dannychuafinancial.com' },
];
export const EXCLUDE = new Set(['hon-win-motor']);   // mini-site on sgcarworkshop.sg, not a client website (also caught by the "/" rule)

// Industry ids of the current rows (registry.json industry_id, by Controller slug). New clients: Client.niche (an id, or text rules).
export const INDUSTRY: Record<string, string> = {
  // white-label (AutoSEO ids)
  'hx-auto': 'car-workshops', 'cch-automotive': 'car-workshops', 'benz-world': 'car-workshops', 'emats': 'car-workshops', 'carzy-world': 'car-workshops',
  'dongfeng-jb': 'car-dealerships', 'apcar': 'car-aircon-specialists', 'klar-details': 'car-detailing', 'rasa-sayang': 'ev-hybrid-specialists',
  'hybrid-world': 'ev-hybrid-specialists', 'sp-precision-parts': 'battery-spare-parts', 'battery-rescue': 'battery-spare-parts',
  'ktech': 'equipment-diagnostic-tools', 'overseas-tyre': 'tyre-shops', 'jt-autoworks': 'car-workshops', 'mcs-auto-spray-painting': 'car-workshops',
  'lt-automart': 'car-dealerships', 'advance-machinery-movers': 'machinery-movers', 'studio-87': 'hair-salons', 'hock-chuan-hiong': 'food', '911garage': 'car-workshops',
  // Page One public
  'ecu-clinic': 'car-workshops', 'dmts': 'car-workshops', 'contiexpert': 'car-workshops', 'new-zen-werkz': 'car-workshops', 'jk-transmission': 'car-workshops',
  'loo-san-choon': 'detailing', 'wrapstar': 'detailing', 'ev-body-parts': 'car-parts', 'autotex': 'car-parts', 'cska-auto': 'car-parts', 'xado': 'car-parts',
  'star-performance': 'car-dealers', 'lilian-properties': 'property', 'jayven-ang': 'property', 'sofacare': 'home', 'maison-interior-design': 'home',
  'rc-design-build': 'home', 'urban-eco': 'home', 'benjamin-poon': 'finance', 'jb-staycation': 'travel', 'aivs': 'other', 'sgcaraccident': 'other',
  'hyper-power': 'other', 'moon-wiper': 'other', 'exn-lube': 'other', 'ape-champs-swim': 'other', 'carku': 'other',
  // own (never counted)
  'sgcarworkshop': 'other', 'autoseo-site': 'other',
};
// Card names of the current Page One public rows (registry.json name). New clients: Client.name without company suffixes.
export const CARD_NAME: Record<string, string> = {
  'ecu-clinic': 'The ECU Clinic', 'dmts': 'Jacky Gearbox', 'contiexpert': 'ContiExpert by Volt Autocare', 'new-zen-werkz': 'New Zen Werkz',
  'jk-transmission': 'J & K Transmission Specialist', 'loo-san-choon': 'Cleanic Detailing', 'wrapstar': 'Wrapstar Autostyle', 'ev-body-parts': 'EV Body Parts',
  'autotex': 'Autotex', 'cska-auto': 'CSKA Auto Enterprise', 'xado': 'XADO Singapore', 'star-performance': 'Star Performance Motor',
  'lilian-properties': 'Ng Li Lian', 'jayven-ang': 'Jayven Ang', 'sofacare': 'SofaCare SG', 'maison-interior-design': 'Maison Interior Design',
  'rc-design-build': 'SG Commercial Fitout', 'urban-eco': 'Urban Eco Solutions', 'benjamin-poon': 'Benjamin Poon', 'jb-staycation': 'JB Staycations',
  'aivs': 'AI Vending Solution', 'sgcaraccident': 'SGCarAccident', 'hyper-power': 'Hyper Power', 'moon-wiper': 'Moon Wiper', 'exn-lube': 'EXN Lube',
  'ape-champs-swim': 'Ape Champs Swim', 'carku': 'Carku',
};

// Not real builds (from the old clientCounts rule): never counted as in build.
export const NOT_BUILDING = new Set(['mega-power', 'kohden', 'alicia-vvip', 'jb-video']);
const NOT_BUILDING_WORDS = /\b(mock-?ups?|demos?|videos?)\b/i;
const STATUS: Record<string, Status> = { live: 'live', preview: 'in_build', activating: 'in_build' };

const RULES_AS: [RegExp, string][] = [
  [/\btyres?\b|\btires?\b|\btayar\b|wheel alignment/i, 'tyre-shops'], [/\baircon(d)?\b|air-cond|air cond/i, 'car-aircon-specialists'],
  [/detailing|ceramic coating|paint protection|\bppf\b/i, 'car-detailing'], [/\bhybrid\b|\bev\b|electric vehicle/i, 'ev-hybrid-specialists'],
  [/batter(y|ies)|spare parts?|alat ganti/i, 'battery-spare-parts'], [/diagnostic|equipment|scanner/i, 'equipment-diagnostic-tools'],
  [/dealer|showroom|used car|3s cent/i, 'car-dealerships'], [/machinery|movers?\b/i, 'machinery-movers'], [/\bsalon\b|\bhair\b/i, 'hair-salons'],
  [/\bfood\b|bak ?kwa|restaurant|cafe|café/i, 'food'], [/workshop|bengkel|repair|servic|spray paint|gearbox|\becu\b/i, 'car-workshops'],
];
const RULES_PO: [RegExp, string][] = [
  [/detailing|\bwraps?\b|\bppf\b|grooming|coating|tint/i, 'detailing'], [/used car|car dealer|dealership/i, 'car-dealers'],
  [/workshop|gearbox|transmission|\becu\b|\babs\b|car repair|car servic|spray paint/i, 'car-workshops'],
  [/\bparts?\b|batter(y|ies)|\btyres?\b|engine oil|lubricant|wiper|additive/i, 'car-parts'],
  [/property|realty|propnex|\bera\b|huttons|new launch/i, 'property'],
  [/interior|renovation|carpentry|cleaning|\bsofa\b|mattress|fitout|fit-out|hydroponic/i, 'home'],
  [/financ|insurance|\bwills?\b|accounting|memorial|niches?\b/i, 'finance'], [/travel|staycation|hotel|holiday|homestay/i, 'travel'],
];
function industryOf(c: any, visibility: Visibility): { id: string; label: string; from: Row['industry_from'] } {
  const table = visibility === 'white-label' ? IND_AS : IND_PO;      // seed.py: white-label rows use the AutoSEO industry names
  const reg = INDUSTRY[c.slug];
  if (reg && table[reg]) return { id: reg, label: table[reg], from: 'registry' };
  const n = String(c.niche || '').trim();
  if (Object.hasOwn(table, n.toLowerCase())) return { id: n.toLowerCase(), label: table[n.toLowerCase()], from: 'niche' };
  for (const [re, id] of visibility === 'white-label' ? RULES_AS : RULES_PO) if (re.test(n)) return { id, label: table[id], from: 'niche' };
  return { id: 'other', label: table.other, from: 'default' };
}

export const sgtDate = (iso: unknown): string | null => {
  const t = Date.parse(String(iso || ''));
  return Number.isFinite(t) ? new Date(t + 8 * 3600_000).toISOString().slice(0, 10) : null;
};
export const cleanName = (n: unknown) => String(n ?? '').replace(/\s+/g, ' ').trim()
  .replace(/[,\s]*\b(sdn\.?\s*bhd\.?|bhd\.?|pte\.?\s*ltd\.?|pte\.?)\s*$/i, '').trim().slice(0, 80);

function notABuild(c: any) {
  if (c.count_as_building === false) return true;
  if (c.count_as_building === true) return false;
  if (NOT_BUILDING.has(c.slug)) return true;
  return NOT_BUILDING_WORDS.test(`${c.slug || ''} ${c.name || ''}`.replace(/-/g, ' ')) || /\bpreview\b/i.test(c.name || '');
}

// One Client record -> one registry row, or null when it is not a client website.
export function classify(c: any): Row | null {
  if (!c || c.duplicate_of || c.is_partner || EXCLUDE.has(c.slug)) return null;
  if (String(c.domain || '').includes('/')) return null;                       // mini-site, not its own domain
  const o = OVERRIDES[c.slug] || {};
  const agency: Agency = o.agency || (brandOf(c) === AUTOSEO ? 'autoseo' : 'pageone');
  const visibility: Visibility = o.visibility || (agency === 'autoseo' ? 'white-label' : 'public');
  let status: Status = STATUS[c.status] || 'dormant';
  if (o.status_override && (c.billing_only || !c.status)) status = o.status_override;
  if (status === 'in_build' && notABuild(c)) status = 'dormant';
  if (c.count_as_building === true && status === 'dormant' && c.status !== 'dormant') status = 'in_build';
  const ind = industryOf(c, visibility);
  const live_date = status === 'live' ? sgtDate(c.live_at) || sgtDate(c.golive_at) || sgtDate(c.activated_at) : null;
  const row: Row = { slug: String(c.slug || ''), agency, visibility, status, live_date, industry_id: ind.id, industry_label: ind.label, industry_from: ind.from };
  if (agency === 'pageone' && visibility === 'public') {                       // only named rows ever carry a name/host
    row.name = CARD_NAME[c.slug] || cleanName(c.name);
    const h = hostOfDomain(c.golive_domain || c.domain);
    if (h) row.host = h;
  }
  return row;
}

// All rows: Controller records (classified) + registry extras. `liveNow` = slug just switched live by a passed go-live
// (its Client.status may still say preview/activating), counted as live from `today`.
export function rows(clients: any[], opts: { liveNow?: string; today?: string } = {}): Row[] {
  const out: Row[] = [];
  const seen = new Set<string>();
  for (const c of clients || []) {
    const r = classify(c);
    if (!r || (r.slug && seen.has(r.slug))) continue;
    if (opts.liveNow && r.slug === opts.liveNow && r.status !== 'live') { r.status = 'live'; r.live_date = opts.today || sgtDate(new Date().toISOString()); }
    seen.add(r.slug); out.push(r);
  }
  for (const x of EXTRAS) if (!seen.has(x.slug)) out.push({ ...x });
  return out;
}

const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const cmp = (a: string, b: string) => (a < b ? -1 : a > b ? 1 : 0);
const addDays = (iso: string, d: number) => new Date(Date.parse(iso + 'T00:00:00Z') + d * 86400_000).toISOString().slice(0, 10);

// stats.py, line for line. today = YYYY-MM-DD in SGT (default: now).
export function stats(rs: Row[], today?: string): Stats {
  const t = today || sgtDate(new Date().toISOString())!;
  const recs = rs.filter((r) => r.visibility !== 'own' && (r.status === 'live' || r.status === 'in_build'));
  const wl = recs.filter((r) => r.visibility === 'white-label');
  const wlLive = wl.filter((r) => r.status === 'live');
  const inds = new Map<string, number>();
  for (const r of wlLive) inds.set(r.industry_label, (inds.get(r.industry_label) || 0) + 1);
  const cut = addDays(t, -30);
  const recent = wlLive.filter((r) => r.live_date && r.live_date > cut);
  const poLive = recs.filter((r) => r.visibility === 'public' && r.status === 'live' && r.agency === 'pageone');
  const poBuild = recs.filter((r) => r.visibility === 'public' && r.status === 'in_build');
  const [y, m, d] = t.split('-').map(Number);
  return {
    wl_live: wlLive.length, wl_build: wl.filter((r) => r.status === 'in_build').length,
    wl_industries: [...inds.entries()].sort((a, b) => b[1] - a[1] || cmp(a[0], b[0])), wl_last30: recent.length,
    po_live: poLive.length, po_industries: new Set(poLive.map((r) => r.industry_id)).size, po_build: poBuild.length,
    updated: `${d} ${MON[m - 1]} ${y}`, updated_iso: t,
  };
}

// The Bridge op pageone_clients body for one passed go-live. White-label / own: totals only (no name, host, url, card).
// Page One public + live + own domain: plus the card fields the Bridge needs (it checks the domain and makes the thumbnail).
export function pageoneClientsBody(clients: any[], c: any, today?: string): Record<string, unknown> {
  const t = today || sgtDate(new Date().toISOString())!;
  const rs = rows(clients, { liveNow: c?.slug, today: t });
  const st = stats(rs, t);
  const me = rs.find((r) => r.slug === c?.slug) || null;
  const client = me ? { agency: me.agency, visibility: me.visibility } : { agency: brandOf(c) === AUTOSEO ? 'autoseo' : 'pageone', visibility: 'own' };
  const body: Record<string, unknown> = { op: 'pageone_clients', stats: st, client };
  if (me && me.agency === 'pageone' && me.visibility === 'public' && me.status === 'live' && me.host && me.name) {
    const niche = String(c.niche || '').trim(), area = String(c.area || '').trim();
    const desc = (niche && area && !niche.toLowerCase().includes(area.toLowerCase()) ? `${niche}, ${area}` : niche || IND_PO[me.industry_id]).slice(0, 150);
    const [y, m] = (me.live_date || t).split('-').map(Number);
    body.card = { slug: me.slug, name: me.name, host: me.host, url: `https://${me.host}/`, industry_id: me.industry_id, desc, since: `Since ${MON[m - 1]} ${y}` };
    body.industry_from = me.industry_from;
  }
  return body;
}

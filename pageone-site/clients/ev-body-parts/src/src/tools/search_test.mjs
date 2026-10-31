// node tools/search_test.mjs [site-dir]  - loads data.js + ev.js and asserts owner-language queries.
// Run A: the empty database (as built): every query must resolve to the right "Ask us" card or product title.
// Run B: with fixture products added (as if ChatGPT/staff had added them): products must rank first.
import fs from 'node:fs'; import vm from 'node:vm'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url)), root = path.join(here, '..');
const siteDir = process.argv[2] || '/tmp/ev-site';
function load() {
  const ctx = { console }; ctx.window = ctx; ctx.globalThis = ctx; vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(siteDir, 'data.js'), 'utf8'), ctx);
  vm.runInContext(fs.readFileSync(path.join(root, 'ev.js'), 'utf8'), ctx);
  return ctx.EV;
}
const T = [
  ['Tesla Model Y tail lamp', 'Tesla Model Y Tail Lamp'],
  ['tesla y taillight', 'Tesla Model Y Tail Lamp'],
  ['model y bumper', /^Tesla Model Y( — [^ ]+)? (Front|Rear) Bumper$/],
  ['Tesla Y bumper', /^Tesla Model Y( — [^ ]+)? (Front|Rear) Bumper$/],
  ['Denza D9 rear reflector', 'Denza D9 Rear Reflector'],
  ['denza 09 reflector', 'Denza D9 Rear Reflector'],
  ['Denza 09', /^Denza D9 /],
  ['model y taillight', 'Tesla Model Y Tail Lamp'],
  ['atto3 headlight', 'BYD Atto 3 Headlamp'],
  ['MG4 side mirror', 'MG MG4 Side Mirror'],
  ['zeekr 001 bonnet', 'Zeekr 001 Bonnet'],
  ['sticker bumper model y', 'Tesla Model Y Bumper Trim'],
  ['model 3 front bumper', 'Tesla Model 3 Front Bumper'],
  ['byd seal u tail light', 'BYD Seal Tail Lamp'],
  ['aion y headlight', 'GAC Aion Y Headlamp'],
  ['xpeng g6 wing mirror', 'XPeng G6 Side Mirror'],
  ['sealion 7 rear bumper', 'BYD Sealion 7 Rear Bumper'],
  ['tesla my fender', 'Tesla Model Y Fender'],
  ['headligt atto 3', 'BYD Atto 3 Headlamp'],
  ['hood model y', 'Tesla Model Y Bonnet'],
  ['model y juniper tail lamp', /Model Y — Juniper Tail Lamp/],
  ['model 3 highland bumper', /Model 3 — Highland/],
  ['zs ev facelift headlamp', /ZS EV — 2023 facelift Headlamp/],
];
let fail = 0;
function run(label, EV) {
  console.log('== ' + label + ' (entries in memory: ' + EV.entries().length + ')');
  for (const [q, exp] of T) {
    const r = EV.search(q); const top = r.results[0] && r.results[0].e.title;
    const ok = top && (exp instanceof RegExp ? exp.test(top) : (top === exp || top.replace(/ — [^]*? (?=(Tail Lamp|Front Bumper|Rear Bumper|Side Mirror|Bonnet|Bumper Trim|Fender|Headlamp)$)/, ' ') === exp));
    if (!ok) fail++;
    console.log((ok ? 'PASS' : 'FAIL') + '  ' + q.padEnd(28) + ' -> ' + (top || '(none)') + (r.results[0] && r.results[0].e.ask ? ' [ask card]' : ''));
  }
  for (const q of ['asdfgh', 'ferrari bumper', 'tesla model y wiper blade', '', 'zeekr 009 grille']) {
    const r = EV.search(q);
    console.log('INFO  ' + JSON.stringify(q).padEnd(30) + ' -> ' + r.results.length + ' results, weak=' + r.weak + (r.results[0] ? ', top=' + r.results[0].e.title : ''));
  }
}
const A = load(); run('A: empty database, Ask-us cards', A);
// no fake listings: with an empty DB no result may be a product
if (A.entries().length === 0 && T.some(([q]) => A.search(q).results.some(x => !x.e.ask))) { fail++; console.log('FAIL  non-ask result with empty DB'); }
const B = load();
const mk = (m, p, title, extra = {}) => ({ key: m + '-' + p, m, p, title, price: null, stock: '', photos: [], created: '2026-10-31', ...extra });
const fx = [['tesla-model-y', 'tail-lamp', 'Tesla Model Y Tail Lamp', { price: 450, stock: 'in' }], ['tesla-model-y', 'front-bumper', 'Tesla Model Y Front Bumper'], ['tesla-model-y', 'bumper-trim', 'Tesla Model Y Bumper Trim'],
  ['denza-d9', 'rear-reflector', 'Denza D9 Rear Reflector'], ['byd-atto-3', 'headlamp', 'BYD Atto 3 Headlamp'], ['mg-mg4', 'side-mirror', 'MG MG4 Side Mirror'], ['zeekr-001', 'bonnet', 'Zeekr 001 Bonnet'],
  ['tesla-model-3', 'front-bumper', 'Tesla Model 3 Front Bumper'], ['byd-seal', 'tail-lamp', 'BYD Seal Tail Lamp'], ['gac-aion-y', 'headlamp', 'GAC Aion Y Headlamp'], ['xpeng-g6', 'side-mirror', 'XPeng G6 Side Mirror'],
  ['byd-sealion-7', 'rear-bumper', 'BYD Sealion 7 Rear Bumper'], ['tesla-model-y', 'fender', 'Tesla Model Y Fender'], ['tesla-model-y', 'bonnet', 'Tesla Model Y Bonnet']].map(a => mk(...a));
B.applyLive({ brands: B.state.brands, cars: B.state.cars, products: fx });
run('B: fixture products', B);
const r = B.search('Tesla Model Y tail lamp'); if (r.results[0].e.price !== 450 || r.results[0].e.ask) { fail++; console.log('FAIL price/product rank'); }
console.log(fail ? `\n${fail} FAILED` : `\nALL PASSED (${T.length} x 2 runs)`);
process.exit(fail ? 1 : 0);

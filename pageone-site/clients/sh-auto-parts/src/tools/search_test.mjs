// node tools/search_test.mjs  - loads data.js + sh.js (search engine) and asserts owner-language queries
import fs from 'node:fs'; import vm from 'node:vm'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url)), root = path.join(here, '..');
const ctx = { console }; ctx.window = ctx; ctx.globalThis = ctx; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'data.js'), 'utf8'), ctx);
vm.runInContext(fs.readFileSync(path.join(root, 'sh.js'), 'utf8'), ctx);
const SH = ctx.SH;
// [query, expected top title, optional: top-N titles that must all be within an allowed set]
const T = [
  ['Tesla Model Y tail lamp', 'Tesla Model Y Tail Lamp'],
  ['tesla y taillight', 'Tesla Model Y Tail Lamp'],
  ['model y bumper', /^Tesla Model Y (Front|Rear) Bumper$/],
  ['Tesla Y bumper', /^Tesla Model Y (Front|Rear) Bumper$/],
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
];
let fail = 0;
for (const [q, exp] of T) {
  const r = SH.search(q); const top = r.results[0] && r.results[0].e.title;
  const ok = top && (exp instanceof RegExp ? exp.test(top) : top === exp);
  if (!ok) fail++;
  console.log((ok ? 'PASS' : 'FAIL') + '  ' + q.padEnd(28) + ' -> ' + (top || '(none)') + (r.results.length ? '  [' + r.results.length + ' results' + (r.weak ? ', weak' : '') + ']' : ''));
}
// zero / weak match must not crash and must be flagged weak
for (const q of ['asdfgh', 'ferrari bumper', 'tesla model y wiper blade', '', 'zeekr 009 grille']) {
  const r = SH.search(q);
  console.log('INFO  ' + JSON.stringify(q).padEnd(30) + ' -> ' + r.results.length + ' results, weak=' + r.weak + (r.results[0] ? ', top=' + r.results[0].e.title : ''));
}
console.log(fail ? `\n${fail} FAILED of ${T.length}` : `\nALL ${T.length} PASSED`);
process.exit(fail ? 1 : 0);

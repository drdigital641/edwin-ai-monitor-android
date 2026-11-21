import * as C from './pure.mts';
import { readFileSync } from 'node:fs';
const card: C.Card = { slug: 'overseas-tyre', name: 'Overseas Tyre And Services', url: 'https://overseastyre.my/', host: 'overseastyre.my', image: '/assets/clients/overseas-tyre.webp', industry: 'tyre-shops',
 line: { en: 'Michelin tyre shop and car service, Bukit Indah, Johor Bahru', ms: 'Kedai tayar Michelin dan servis kereta, Bukit Indah, Johor Bahru', zh: '新山武吉英达米其林轮胎店与汽车保养' },
 alt: C.defaultAlt('Overseas Tyre And Services', 'overseastyre.my') };
let fail = 0; const ok = (c: boolean, n: string) => { console.log((c ? 'PASS ' : 'FAIL ') + n); if (!c) fail++; };
for (const [l, f] of [['en', 'clients_'], ['ms', 'ms_clients_'], ['zh', 'zh_clients_']] as const) {
  const src = readFileSync(f, 'utf8'), want = readFileSync('new_' + f, 'utf8');
  const got = C.addClientCard(src, l, card)!;
  ok(got === want, l + ' new industry block = live result');
  ok(C.addClientCard(got, l, card) === null, l + ' second run changes nothing');
  // existing industry: a second workshop goes first in car-workshops, counts 14/8, workshops 6
  const ws = { ...card, slug: 'x-auto', name: 'X Auto', url: 'https://xauto.my/', host: 'xauto.my', industry: 'car-workshops', line: C.defaultLine('car-workshops', 'Skudai'), alt: C.defaultAlt('X Auto', 'xauto.my') };
  const g2 = C.addClientCard(got, l, ws)!;
  const blk = g2.slice(g2.indexOf('id="car-workshops"'), g2.indexOf('id="car-workshops"') + 900);
  ok(blk.indexOf('xauto.my') > 0 && blk.indexOf('xauto.my') < blk.indexOf('hxautoservice.com.my'), l + ' card first in its block');
  ok(/<span class="count-badge">6[^<]*<\/span>/.test(blk), l + ' block badge 6');
  ok(g2.includes('href="#car-workshops">') && /#car-workshops">[^<]*<span class="chip-count">6</.test(g2), l + ' chip 6');
  ok(/"numberOfItems": 14,/.test(g2) && g2.includes('"position": 14'), l + ' ItemList 14');
  ok(/<div class="value">14<\/div>/.test(g2) && /<div class="value">8<\/div>/.test(g2), l + ' counters 14/8');
  for (const m of g2.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) JSON.parse(m[1]);
  // third: brand-new industry with footer name
  const acc = { ...ws, slug: 'y-acc', url: 'https://yacc.my/', host: 'yacc.my', industry: 'car-accessories' };
  const g3 = C.addClientCard(g2, l, acc)!;
  ok(/id="car-accessories"/.test(g3) && /<div class="value">9<\/div>/.test(g3), l + ' new industry 9, title ' + (/id="car-accessories">\s*<div class="industry-head reveal">\s*<h2>([^<]*)/.exec(g3) || [])[1]);
  ok(/industry-block" id="car-accessories"/.test(g3), l + ' alternates alt (after alt block = plain)');
}
const lj = readFileSync('assets_launches.json', 'utf8');
const n1 = C.addLaunch(lj, card, '2026-11-21')!; ok(JSON.parse(n1).launches[0].id === 'overseas-tyre-2026-11-21', 'launch prepended');
ok(C.addLaunch(n1, card, '2026-11-22') === null, 'launch idempotent');
ok(C.pickIndustry('', 'Michelin Tyre Shop in Bukit Indah, Johor Bahru | Overseas Tyre')!.id === 'tyre-shops', 'industry from title');
ok(C.pickIndustry('Tyre shops', '')!.id === 'tyre-shops' && C.pickIndustry('car-detailing', 'tyre')!.id === 'car-detailing', 'industry from controller');
ok(C.pickIndustry('nonsense', 'Car Workshop Bukit Indah | HX Auto Service')!.id === 'car-workshops', 'workshop from title'); ok(C.pickIndustry('Machinery movers', 'Heavy machinery moving Johor')=== null, 'unknown industry = skip'); ok(C.pickIndustry('Car tyre and rim shop', '')!.id === 'tyre-shops', 'niche text'); ok(C.addLaunch(JSON.stringify({launches:[{id:'overseas-tyre-2026-11-21',url:'https://overseastyre.my/'}]}), {...card, slug:'overseas', url:'https://overseas.my/'}, '2026-11-22') !== null, 'slug prefix not a false duplicate');
ok(C.cleanName('Overseas Tyre And Services Sdn Bhd') === 'Overseas Tyre And Services', 'clean name');
ok(C.cleanTown('Taman Bukit Indah, Johor Bahru, Malaysia') === 'Taman Bukit Indah, Johor Bahru', 'clean town');
ok(!C.addClientCard.toString().includes('eval'), 'no eval');
let threw = false; try { C.addClientCard('<html></html>', 'en', card); } catch { threw = true; } ok(threw, 'unknown layout throws, nothing written');
console.log(fail ? 'FAILED ' + fail : 'ALL PASS'); process.exit(fail ? 1 : 0);

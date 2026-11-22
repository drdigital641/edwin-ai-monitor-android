// Public client counts for pageonesingapore.com (12 Nov 2026; registry classifier 22 Nov 2026). Run: deno test tests/clientCounts.test.ts
import { clientCounts, countsAsBuilding } from '../base44/shared/clientCounts.ts';

function eq(a: unknown, b: unknown) { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error('expected ' + JSON.stringify(b) + ' got ' + JSON.stringify(a)); }

Deno.test('white label = live AutoSEO sites only', () => {
  eq(clientCounts([
    { status: 'live', brand: 'AutoSEO' },
    { status: 'preview', brand: 'AutoSEO' },
    { status: 'live', brand: 'Page One' },
    { status: 'live' },
  ]).white_label_live, 1);
});
Deno.test('building = preview or activating, any brand; drafts, live and dormant do not count', () => {
  eq(clientCounts([
    { slug: 'a', status: 'preview' }, { slug: 'b', status: 'preview', brand: 'AutoSEO' }, { slug: 'c', status: 'activating' },
    { slug: 'd', status: 'draft' }, { slug: 'e' }, { slug: 'f', status: 'live' }, { slug: 'g', status: 'dormant' },
  ]).building, 3);
});
Deno.test('mock-ups, demos, video jobs and extra previews do not count', () => {
  for (const c of [
    { slug: 'mega-power', name: 'Mega Power', status: 'preview' },
    { slug: 'alicia-vvip', name: 'Alicia Ong new-launch preview', status: 'preview' },
    { slug: 'jb-video', name: 'JB Staycations', status: 'preview' },
    { slug: 'abc-mockup', name: 'ABC', status: 'preview' },
    { slug: 'abc', name: 'ABC demo', status: 'preview' },
  ]) eq(countsAsBuilding(c), false);
});
Deno.test('count_as_building overrides the default rule', () => {
  eq(countsAsBuilding({ slug: 'mega-power', status: 'preview', count_as_building: true }), true);
  eq(countsAsBuilding({ slug: 'x', status: 'draft', count_as_building: true }), true);
  eq(countsAsBuilding({ slug: 'x', status: 'live', count_as_building: true }), false);
  eq(countsAsBuilding({ slug: 'x', status: 'preview', count_as_building: false }), false);
});
Deno.test('partner and duplicate records are not sites; billing-only rows are (registry rule, 22 Nov 2026: Cleanic)', () => {
  eq(clientCounts([
    { status: 'live', brand: 'AutoSEO', is_partner: true, billing_only: true },
    { status: 'preview', duplicate_of: 'x' },
  ]), { white_label_live: 0, building: 0 });
  eq(clientCounts([{ slug: 'b', status: 'live', brand: 'AutoSEO', billing_only: true }]).white_label_live, 1);
});
Deno.test('registry exceptions (22 Nov 2026): Page One-branded AutoSEO clients are white-label; mini-sites and own sites never count', () => {
  eq(clientCounts([
    { slug: 'ktech', status: 'live', brand: 'Page One' }, { slug: 'klar-details', status: 'live', brand: 'Page One' },
    { slug: 'hon-win-motor', status: 'live', domain: 'sgcarworkshop.sg/workshops/hon-win-motor' },
    { slug: 'x-mini', status: 'live', brand: 'AutoSEO', domain: 'sgcarworkshop.sg/workshops/x' },
    { slug: 'autoseo-site', status: 'live' }, { slug: 'sgcarworkshop', status: 'live' },
  ]), { white_label_live: 2, building: 0 });
});
Deno.test('only the two numbers come back', () => {
  eq(Object.keys(clientCounts([{ status: 'live', brand: 'AutoSEO', name: 'Secret Co', domain: 'secret.example' }])).sort(), ['building', 'white_label_live']);
});

// Two public numbers for pageonesingapore.com (Edwin, 12 Nov 2026):
//  - white_label_live: live white-label client sites. 22 Nov 2026 (Edwin): counted by shared/clientsRegistry.ts (registry.json rules),
//    so K Tech, Klar Details, Battery Rescue and MyKar (Controller brand Page One) count as white-label, and the homepage number
//    equals the wl_live total on pageonesingapore.com/clients/.
//  - building: REAL client sites in build (Edwin 12 Nov 9:37pm SGT). Mock-ups and demos, extra preview pages of
//    clients who are already live, and video jobs do not count.
// Only these two numbers ever leave the Controller: no names, slugs or domains.
// Partner/billing-only accounts and likely duplicates are not sites, so they are skipped.
//
// Building rule:
//  1. Client.count_as_building (optional field) wins when set: true counts, false never counts.
//  2. Otherwise a site counts only when status is preview or activating (drafts don't count),
//     it is not in NOT_BUILDING, and its name/slug doesn't mark it as a mock-up, demo, video job or extra preview.
import { rows, stats } from './clientsRegistry.ts';

export const BUILDING_STATUSES = ['preview', 'activating'];

// Known records that are not client builds (no record is changed; the rule just skips them).
export const NOT_BUILDING = new Set([
  'mega-power',   // mock-up
  'kohden',       // prospect mock-up
  'alicia-vvip',  // extra preview page of a client who is already live
  'jb-video',     // video job for a client who is already live
]);
const NOT_BUILDING_WORDS = /\b(mock-?ups?|demos?|videos?)\b/i;

const isSite = (c: any) => !!c && !c.is_partner && !c.billing_only && !c.duplicate_of;

export function countsAsBuilding(c: any): boolean {
  if (!isSite(c)) return false;
  if (c.count_as_building === true) return c.status !== 'live' && c.status !== 'dormant';
  if (c.count_as_building === false) return false;
  if (!BUILDING_STATUSES.includes(c.status)) return false;
  if (NOT_BUILDING.has(c.slug)) return false;
  const words = `${c.slug || ''} ${c.name || ''}`.replace(/-/g, ' ');
  if (NOT_BUILDING_WORDS.test(words) || /\bpreview\b/i.test(c.name || '')) return false;
  return true;
}

// 22 Nov 2026: both numbers come from the registry classifier (same totals as /clients/): white_label_live = wl_live,
// building = wl_build + po_build (real builds of both brands, the same rule as countsAsBuilding above plus the registry exceptions).
// Response shape unchanged: only these two numbers.
export function clientCounts(clients: any[]): { white_label_live: number; building: number } {
  const st = stats(rows(clients || []));
  return { white_label_live: st.wl_live, building: st.wl_build + st.po_build };
}

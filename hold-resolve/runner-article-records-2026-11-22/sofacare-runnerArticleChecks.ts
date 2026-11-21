// SofaCare Article checks for runner-made records (22 Nov 2026). Port of night-writers/sofacare/check_article.py:
// every FAIL there is a FAIL here (the hourly :17 publisher stops the WHOLE site on most of them), WARNs are returned.
export const SOFA_APP_ID = '6a9c4351b2a32e6fb4dc814c';
export const RETIRED_SLUGS = new Set(['cat-pee-sofa-cleaning-singapore', 'dining-chair-cleaning-price-singapore', 'dining-chair-cleaning-service-singapore',
  'mattress-cleaning-for-dust-mites-and-allergies-singapore', 'mattress-dust-mite-allergy-cleaning-singapore', 'how-to-remove-blood-stains-from-mattress-singapore',
  'remove-urine-stains-smell-mattress-singapore', 'coffee-spill-sofa-cleaning-singapore', 'how-to-clean-fabric-sofa-mould-singapore', 'wash-fabric-sofa-singapore',
  'couch-deep-cleaning-singapore', 'yacht-upholstery-cleaning-singapore', 'yacht-mattress-cleaning-singapore', 'private-jet-mattress-cleaning-singapore',
  'fb-upholstery-cleaning-singapore', 'office-chair-upholstery-cleaning-singapore', 'dining-chair-upholstery-stain-removal-singapore',
  'upholstery-cleaning-dining-chairs-singapore', 'leather-upholstery-cleaning-singapore', 'upholstery-cleaning-singapore']);
const PAGES = new Set(['/sofa-cleaning-singapore.html', '/mattress-cleaning-singapore.html', '/pricing.html', '/faq.html', '/contact.html', '/leather-sofa-cleaning-singapore.html']);
const COVER = ['3-hour call-out response within about 8 km of Punggol, Sengkang and Tampines.', 'Same-day service for addresses beyond 8 km (the rest of Singapore).'];
export type Faq = { q: string; a: string };

export function checkArticle(p: any, ctx: { liveSlugs: Set<string>; titles: Set<string>; heroUploaded: boolean; sgtToday: string }): { fails: string[]; warns: string[]; faqs: Faq[] } {
  const fails: string[] = [], warns: string[] = [];
  const F = (m: string) => fails.push(m), W = (m: string) => warns.push(m);
  const s = (k: string) => (typeof p?.[k] === 'string' ? p[k] : '');
  const content = s('content'), title = s('title'), h1 = s('h1'), slug = s('slug');
  let faqs: Faq[] = [];
  try { const raw = typeof p?.faqs === 'string' ? JSON.parse(p.faqs) : p?.faqs; if (Array.isArray(raw)) faqs = raw.map((f: any) => ({ q: String(f?.q || '').trim(), a: String(f?.a || '').trim() })); } catch { /* checked below */ }
  const all = [content, title, h1, s('meta_description'), s('excerpt'), s('hero_image_alt'), faqs.map((f) => f.q + ' ' + f.a).join(' ')].join(' ');
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug) || slug.length > 60) F('slug must be lowercase-hyphen, <=60 chars');
  if (RETIRED_SLUGS.has(slug)) F('slug is a retired SofaCare slug');
  if (ctx.liveSlugs.has(slug)) F('slug already exists');
  for (const k of ['title', 'h1', 'meta_description', 'excerpt', 'content', 'keyword', 'hero_image_alt', 'published_date']) if (!s(k).trim()) F('missing field ' + k);
  if (!ctx.heroUploaded && !/^https:\/\/media\.base44\.com\/images\/public\/[a-f0-9]{24}\/[A-Za-z0-9_.-]+\.(png|jpe?g|webp)$/.test(s('hero_image'))) F('hero_image must be a media.base44.com/images/public/... URL (Bridge hero_image or generateArticleImage) (or send hero_path to the Bridge)');
  if (!['sofa', 'mattress'].includes(s('related_service'))) F('related_service must be sofa or mattress');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s('published_date'))) F('published_date must be YYYY-MM-DD (SGT)');
  else { const d = Date.parse(s('published_date') + 'T00:00:00Z') - Date.parse(ctx.sgtToday + 'T00:00:00Z'); if (d > 86400_000 || d < -3 * 86400_000) F('published_date must be within the last 3 SGT days (today ' + ctx.sgtToday + ')'); }
  if (s('meta_description').length > 155) F('meta_description > 155 chars');
  if (s('excerpt').length > 200) F('excerpt > 200 chars');
  if (title.length > 65) F(`title ${title.length} chars > 65`);
  if (ctx.titles.has(title.trim().toLowerCase())) F('title is already used by another page');
  if (!(faqs.length >= 6 && faqs.length <= 8 && faqs.every((f) => f.q && f.a))) F('faqs must be 6-8 {q,a}');
  if (/wa\.me|whatsapp\.com\/send|api\.whatsapp/i.test(all)) F('wa.me/WhatsApp URL in article: number as plain text only (the template adds tracked buttons)');
  if (!content.includes('+65 9025 9771')) F('plain-text +65 9025 9771 CTA missing');
  const lines = content.trimEnd().split('\n');
  if (!(lines[lines.length - 1] || '').startsWith('WhatsApp Sofa Care Singapore')) W('last line should be the single soft WhatsApp CTA');
  const forb = all.match(/gjourney|g-journey|202128581E|NEA ?2609|8581E\/C2|NEA[- ]?(?:Class|licen[cs]ed)|nea-list|list of licensed cleaning|carousell|admiralty link|750482|bizsafe/i);
  if (forb) F(`forbidden identity term "${forb[0]}"`);
  for (const [re, why] of [[/\bNEA\b/i, 'NEA'], [/\blicen[cs]ed\b/i, 'licensed'], [/\bcertified\b/i, 'certified'], [/\bGforce\b/i, 'Gforce'], [/\bSofaCare( SG)?\b/i, 'brand must be "Sofa Care Singapore"'], [/\bguarantee[ds]?\b/i, 'guarantee wording'], [/award|#1|best in singapore|most reviewed|\d\.\d\s*(?:star|\/5)|\d+ reviews/i, 'award/rating/review claim']] as [RegExp, string][]) {
    const m = all.match(re); if (m) F(`banned: ${why} -> "${m[0]}"`);
  }
  if (/\b(upholster\w*|chairs?|carpets?|rugs?|curtains?|yachts?|boats?|jets?|cars?|vehicles?|restaurants?|cafes?|hotels?)\b/i.test(all)) W('off-scope word present: check it is not a service offer');
  if (/"aggregateRating"|"@type":\s*"Review"/.test(all)) F('review markup');
  const okPrices = new Set([60, 80, 87, 107, 127, 150, 97, 20]);
  for (const m of all.matchAll(/\$\s?(\d[\d,]*)/g)) {
    const v = parseInt(m[1].replace(/,/g, ''), 10), i = m.index || 0;
    if (!okPrices.has(v) && !/(?:DIY|product|cloth|conditioner)/i.test(all.slice(Math.max(0, i - 60), i + m[0].length + 40))) F(`price $${v} is not in the published table`);
  }
  if (/(from|starts? at|starting)\s+\$20|steam[^.|]{0,40}from \$20|\$\d+\s*(?:-|–|to)\s*\$\d+/i.test(all)) F('steam must be "+$20", no price ranges');
  if (/no (?:hidden )?(?:transport|location|weekend)?\s*surcharge|nothing extra to pay/i.test(all)) F('no "no surcharge" claims');
  if (/\b\d+\s*(?:[-–to]+\s*\d+)?\s*hours?\b[^.]{0,30}dr(?:y|ies|ying)|dr(?:y|ies|ying)[^.]{0,40}\b\d+\s*(?:[-–to]+\s*\d+)?\s*hours?/i.test(all)) F('invented drying-time hours');
  if (/(?:from|starting)\s+\$\d+[^.]{0,30}leather|leather[^.]{0,40}\$\d+/i.test(all)) F('leather has no price (photo quote only)');
  for (const c of COVER) if (/3-hour|same-day/i.test(all) && all.includes('about 8 km') && !content.includes(c)) F('coverage wording must be exactly: ' + c);
  if (/within 3 hours|in as little as 3 hours|24-hour|24 hour|guarantee/i.test(all)) F('coverage drift (use only the two exact sentences)');
  const links = [...content.matchAll(/\]\(([^)\s]+)\)/g)].map((m) => m[1]);
  const internal = links.filter((l) => l.startsWith('/') || l.includes('sofacaresg.com'));
  const owner = s('related_service') === 'mattress' ? '/mattress-cleaning-singapore.html' : '/sofa-cleaning-singapore.html';
  if (internal.length < 3 || internal.length > 5) F(`${internal.length} internal links (need 3-5)`);
  if (!content.slice(0, Math.floor(content.length / 2)).includes(owner)) F('owner page link ' + owner + ' must appear before the midpoint');
  for (const l of internal) {
    const path = l.replace(/^https:\/\/(www\.)?sofacaresg\.com/, '');
    const m = path.match(/^\/articles\/([a-z0-9-]+)\.html$/);
    if (m) { if (!ctx.liveSlugs.has(m[1]) || RETIRED_SLUGS.has(m[1])) F('link to unpublished/retired slug ' + m[1]); }
    else if (!PAGES.has(path)) F('unknown internal link ' + l + ' (would stop the hourly publish)');
  }
  for (const l of links) if (!(l.startsWith('/') || l.includes('sofacaresg.com')) && !/^https:\/\/(?:www\.)?(?:cleanicdetailing|sggarage)\.com/.test(l)) F('external link not allowed: ' + l.slice(0, 80));
  if (/^# /m.test(content)) F('no H1 inside content');
  if ((content.match(/^## /gm) || []).length < 6) F('need 6-9 H2');
  for (const need of ['## Key takeaways', '**Direct answer:**', '## Cost and pricing', '## Singapore service areas']) if (!content.includes(need)) F('missing ' + need);
  const wc = content.split(/\s+/).filter(Boolean).length;
  if (wc < 1800 || wc > 2500) W(`word count ${wc} (target 1800-2500)`);
  if (/\b20[0-9]{2}\b/.test(title + h1 + s('meta_description')) && !/2026/.test(title + h1 + s('meta_description'))) F('stale year in headline fields');
  return { fails, warns, faqs };
}

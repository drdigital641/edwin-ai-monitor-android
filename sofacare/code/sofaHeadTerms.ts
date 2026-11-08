// Head-term pass (Edwin, 8 Nov 2026): one page per head term, mattress page with its own process,
// content and FAQ, a leather sofa cleaning page, real job before/after sliders, same prices everywhere.
// Facts only from the published price table and Edwin's rules: open 24/7, 3-hour call-out within about
// 8 km of Punggol, Sengkang and Tampines, same-day elsewhere, drying about 4-8 hours, leather by photo quote.
import { cloneSofaShell } from './sofaAreaPages.ts';
import { SOFA_REAL_PAIRS, SOFA_REAL_PHOTO_BASE } from './sofaRealResults.ts';
import { syncFaqSchema } from './sofaSeoPush.ts';

const SITE = 'https://sofacaresg.com';
const WA = '6590259771';
const esc = (s: string) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
export const LEATHER_PAGE = 'leather-sofa-cleaning-singapore.html';

// ---------- Real job photos (self-hosted under /images/jobs/) ----------
export const SOFA_JOBS_BASE = 'https://raw.githubusercontent.com/drdigital641/edwin-ai-monitor-android/c99cb7219e5d16f60b3024019ff81a96827b216c/sofacare/jobs/';
type Job = { id: string; kind: 'sofa' | 'mattress' | 'velvet'; w: number; h: number; s: [number, number]; before: string; after: string; caption: string };
const JOBS: Job[] = [
  { id: 'grey-2seater-fabric-sofa', kind: 'sofa', w: 1200, h: 900, s: [640, 480], before: 'Grey fabric two-seater sofa with ring-shaped marks and dark patches on the seat cushions, arms and backrest, before cleaning', after: 'The same grey fabric two-seater sofa after cleaning, with an even colour across the cushions, arms and backrest', caption: 'Grey fabric two-seater sofa.' },
  { id: 'grey-3seater-recliner-sofa', kind: 'sofa', w: 1200, h: 1000, s: [640, 533], before: 'Grey fabric three-seater recliner sofa with darker soiled patches on the seats and armrests, before cleaning', after: 'The same grey fabric three-seater recliner sofa after cleaning, seats and armrests even in colour', caption: 'Grey fabric three-seater recliner sofa.' },
  { id: 'cream-velvet-tufted-armchair', kind: 'velvet', w: 900, h: 1200, s: [480, 640], before: 'Cream velvet tufted armchair with small brown spots on the backrest and seat, before cleaning', after: 'The same cream velvet tufted armchair after cleaning, backrest and seat free of the brown spots', caption: 'Cream velvet tufted armchair.' },
  { id: 'mattress-urine-stain', kind: 'mattress', w: 1200, h: 900, s: [640, 480], before: 'White mattress with large yellow-brown stains and a ring mark on the top surface, before cleaning', after: 'White mattress after cleaning, with the yellow-brown stains no longer visible', caption: 'Mattress with a urine stain.' },
  { id: 'mattress-scallop-yellow-stain', kind: 'mattress', w: 900, h: 1080, s: [480, 576], before: 'Mattress with a scallop-pattern cover and yellow marks across the middle, before cleaning', after: 'The same scallop-pattern mattress after cleaning, cover an even white', caption: 'Scallop-pattern mattress with yellow staining.' },
  { id: 'mattress-pillowtop-stain', kind: 'mattress', w: 1200, h: 953, s: [640, 508], before: 'Pillow-top mattress with a large brown ring stain near the centre, before cleaning', after: 'The same pillow-top mattress after cleaning, the brown ring stain gone from the centre', caption: 'Pillow-top mattress with a ring stain.' },
  { id: 'mattress-heart-pattern', kind: 'mattress', w: 1200, h: 810, s: [640, 432], before: 'Quilted mattress with a heart pattern and a long yellow-brown stain down the middle, before cleaning', after: 'The same heart-pattern quilted mattress after cleaning, the yellow-brown stain gone', caption: 'Heart-pattern quilted mattress.' },
];
export const SOFA_JOB_FILES: string[] = JOBS.flatMap((j) => ['before', 'after'].flatMap((k) => [`${j.id}-${k}-1200.webp`, `${j.id}-${k}-640.webp`]));

const img = (j: Job, k: 'before' | 'after') => {
  const big = `/images/jobs/${j.id}-${k}-1200.webp`, small = `/images/jobs/${j.id}-${k}-640.webp`;
  return `<img class="sc-ba-${k}" src="${big}" srcset="${small} ${j.s[0]}w, ${big} ${j.w}w" sizes="(min-width: 760px) 720px, 100vw" alt="${esc(k === 'before' ? j.before : j.after)}" width="${j.w}" height="${j.h}" loading="lazy" decoding="async"${k === 'after' ? ' data-real-photo' : ''}>`;
};
const slider = (j: Job) =>
  `<figure class="sc-ba" data-sc-ba><div class="sc-ba-frame" style="aspect-ratio:${j.w}/${j.h};--pos:50%">${img(j, 'after')}${img(j, 'before')}<span class="sc-ba-line" aria-hidden="true"></span><span class="sc-ba-tag sc-ba-tag-b">Before</span><span class="sc-ba-tag sc-ba-tag-a">After</span><input class="sc-ba-range" type="range" min="0" max="100" value="50" aria-label="${esc('Slide to compare before and after: ' + j.caption.replace(/\.$/, ''))}"></div><figcaption><strong>Real Sofa Care Singapore job.</strong> ${esc(j.caption)} Drag the slider to compare. Results depend on the material and how old the stain is.</figcaption></figure>`;
// The two 7 Nov sofa pairs and the 7 Nov mattress pair, as sliders (pinned GitHub source, mirrored to /media/).
const oldSlider = (i: number) => {
  const p = SOFA_REAL_PAIRS[i];
  const one = (s: typeof p.before, k: string) => `<img class="sc-ba-${k}" src="${SOFA_REAL_PHOTO_BASE}${s.file}" alt="${esc(s.alt)}" width="${s.w}" height="${s.h}" loading="lazy" decoding="async"${k === 'after' ? ' data-real-photo' : ''}>`;
  return `<figure class="sc-ba" data-sc-ba><div class="sc-ba-frame" style="aspect-ratio:${p.after.w}/${p.after.h};--pos:50%">${one(p.after, 'after')}${one(p.before, 'before')}<span class="sc-ba-line" aria-hidden="true"></span><span class="sc-ba-tag sc-ba-tag-b">Before</span><span class="sc-ba-tag sc-ba-tag-a">After</span><input class="sc-ba-range" type="range" min="0" max="100" value="50" aria-label="${esc('Slide to compare before and after: ' + p.caption.replace(/, before and after cleaning\.$/, ''))}"></div><figcaption><strong>Real Sofa Care Singapore job.</strong> ${esc(p.caption)} Drag the slider to compare.</figcaption></figure>`;
};
const SLIDER_JS = `<script>document.addEventListener('input',function(e){var t=e.target;if(t&&t.classList&&t.classList.contains('sc-ba-range'))t.parentNode.style.setProperty('--pos',t.value+'%')});</script>`;

export const sofaHeadTermStyles = `
.sc-ba-list{display:grid;gap:28px}
@media (min-width:900px){.sc-ba-list{grid-template-columns:1fr 1fr;align-items:start}}
.sc-ba{margin:0}
.sc-ba-frame{position:relative;width:100%;max-width:720px;overflow:hidden;border-radius:14px;background:#f1f5f9;touch-action:pan-y}
.sc-ba-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.sc-ba-before{clip-path:inset(0 calc(100% - var(--pos)) 0 0)}
.sc-ba-line{position:absolute;top:0;bottom:0;left:var(--pos);width:3px;margin-left:-1px;background:#fff;box-shadow:0 0 0 1px rgba(15,35,50,.25);pointer-events:none}
.sc-ba-line::after{content:'';position:absolute;top:50%;left:50%;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:999px;background:#fff;box-shadow:0 2px 8px rgba(15,35,50,.3)}
.sc-ba-tag{position:absolute;top:10px;z-index:1;padding:4px 10px;border-radius:999px;color:#fff;font-size:.8rem;font-weight:700;pointer-events:none}
.sc-ba-tag-b{left:10px;background:rgba(15,35,50,.85)}
.sc-ba-tag-a{right:10px;background:#0e7c66}
.sc-ba-range{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:ew-resize;-webkit-appearance:none;appearance:none}
.sc-ba figcaption{margin-top:8px;font-size:.9rem;color:#475569}
.sc-ht-table{width:100%;border-collapse:collapse;font-size:.95rem}
.sc-ht-table th,.sc-ht-table td{border:1px solid rgba(15,35,50,.12);padding:10px;text-align:left;vertical-align:top}
.sc-ht-table th{background:#f1f5f9}
.sc-ht-links{margin-top:16px;line-height:1.8}
`;

// ---------- Shared HTML helpers ----------
const sec = (h: string, inner: string, id = '') => `<section class="sc-home-sec"${id ? ` id="${id}"` : ''}><div class="sc-in"><h2>${esc(h)}</h2>${inner}</div></section>`;
const P = (t: string) => `<p>${t}</p>`;
const ul = (items: string[]) => `<ul class="sc-list">${items.map((i) => `<li>${i}</li>`).join('')}</ul>`;
const table = (head: string[], rows: string[][]) => `<div class="sc-table-scroll" style="overflow-x:auto;-webkit-overflow-scrolling:touch"><table class="sc-ht-table"><thead><tr>${head.map((h) => `<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
const faqItems = (faqs: [string, string][]) => faqs.map(([q, a]) => `<details class="group rounded-xl border border-brand-slate/10 bg-white p-5 shadow-sm"><summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-semibold text-brand-slate"><span>${esc(q)}</span><span class="text-brand-ochre transition-transform group-open:rotate-45" aria-hidden="true">+</span></summary><p class="mt-3 text-sm leading-relaxed text-brand-slate/80">${esc(a)}</p></details>`).join('');
function waHref(path: string, cta: string, msg: string): string {
  const text = `${msg}\n\n[Source:SofaCareSG]\n[CTA:${cta}]\n[Page:/${path === 'index.html' ? '' : path}]`;
  return `https://wa.me/${WA}?text=${encodeURIComponent(text).replace(/%20/g, '+')}`;
}
const waBtn = (path: string, cta: string, label: string, msg: string) => `<div class="sc-inline-cta" data-sc-inline-cta><p>Open 24/7. Send photos and your postal code for a quote.</p><a href="${waHref(path, cta, msg)}" class="sc-wa-btn" data-cta="whatsapp" rel="noopener noreferrer" target="_blank" aria-label="${esc('WhatsApp Sofa Care Singapore: ' + label)}"><span>${esc(label)}</span></a></div>`;

function replaceSection(html: string, heading: string, replacement: string): string {
  const i = html.indexOf(heading);
  if (i === -1) return html;
  const s = html.lastIndexOf('<section', i), e = html.indexOf('</section>', i);
  if (s === -1 || e === -1) throw Error('Head terms: section not found: ' + heading);
  return html.slice(0, s) + replacement + html.slice(e + 10);
}
function replaceRealResults(html: string, replacement: string): string {
  const i = html.indexOf('data-sofacare-real-results');
  if (i === -1) throw Error('Head terms: real results section missing');
  const s = html.lastIndexOf('<section', i);
  // The real-results section has no nested <section>.
  const e = html.indexOf('</section>', i);
  return html.slice(0, s) + replacement + html.slice(e + 10);
}
function setHead(html: string, title: string, desc: string, h1?: string): string {
  let h = html.replace(/<title\b[^>]*>[\s\S]*?<\/title>/i, `<title>${esc(title)}</title>`)
    .replace(/(<meta name="description" content=")[^"]*(")/, `$1${esc(desc)}$2`)
    .replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${esc(title)}$2`)
    .replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${esc(desc)}$2`)
    .replace(/(<meta name="twitter:title" content=")[^"]*(")/, `$1${esc(title)}$2`)
    .replace(/(<meta name="twitter:description" content=")[^"]*(")/, `$1${esc(desc)}$2`);
  if (!/<meta name="twitter:title"/.test(h)) h = h.replace('</title>', `</title><meta name="twitter:title" content="${esc(title)}"/>`);
  if (h1) h = h.replace(/(<h1\b[^>]*>)[\s\S]*?(<\/h1>)/, `$1${esc(h1)}$2`);
  return h;
}

// ---------- Mattress page ----------
const MATTRESS_STEPS: [string, string][] = [
  ['Check the mattress and its label', 'We look at the size, the cover fabric and how the mattress is built (pocket spring, foam, latex, hybrid or pillow-top), and read any care label. We note stains, odour and old water marks, and tell you what is likely to improve before we start.'],
  ['Vacuum the surface, seams and sides', 'A thorough vacuum lifts dust, skin flakes, hair and dust mite debris from the top, the quilting, the piping and the sides. This is done before anything wet touches the cover.'],
  ['Pre-treat stains and odour areas', 'Sweat marks, urine, blood, food and drink stains get a pre-treatment chosen for the stain type and left to work. Protein stains such as blood and urine are never treated with heat first, because heat can set them.'],
  ['Controlled clean and extraction', 'On covers that suit it, cleaning solution is applied in controlled amounts and pulled back out with an extraction machine, so dirt leaves the mattress instead of being pushed deeper. Foam and latex get less moisture, not more.'],
  ['Hot steam, only where suitable (+$20)', 'The hot steam add-on is used only when the cover and filling suit it. It is not used on every foam or latex mattress, and we tell you on WhatsApp if it is not suitable for yours.'],
  ['Final check and drying advice', 'We look over the result with you, point out anything that did not fully lift, and explain how to dry the mattress: good airflow, a fan if you have one, and no bedding until it is dry. Drying usually takes about 4–8 hours.'],
];
const MATTRESS_FAQ: [string, string][] = [
  ['How much does mattress cleaning cost in Singapore?', 'Mattress cleaning starts from $80. A Queen is $87 and a King is $97. The hot steam add-on is +$20 where the mattress suits it. Your price is confirmed on WhatsApp before we come.'],
  ['Can you remove urine smell from a mattress?', 'Fresh urine usually improves well. If urine has soaked deep into the foam, or the same spot has been wet many times, the stain can lighten while some smell comes back on humid days. We tell you from your photos what is likely to improve.'],
  ['Will old yellow sweat stains come out?', 'Yellow sweat marks are body oils and sweat that have aged in the cover. They usually lighten a lot, but very old marks may not disappear completely. We say so before we start.'],
  ['Is it safe to clean a memory foam or latex mattress?', 'Yes, with less moisture. Foam and latex hold water, so we use controlled amounts and extraction, and we do not use steam unless the cover and filling suit it. Follow any care label from the maker.'],
  ['Does mattress cleaning get rid of bed bugs?', 'No. Cleaning removes dust, dust mite debris, stains and odour. Bed bugs need a pest control company. If you see bed bugs, call pest control first and book cleaning after.'],
  ['Does cleaning remove dust mites?', 'Vacuuming and cleaning remove dust and dust mite debris from the surface and seams, which many people with allergies find helps. No cleaning removes every mite for good, so a mattress protector and regular vacuuming still matter.'],
  ['How long does the mattress take to dry?', 'Usually about 4–8 hours. Thick pillow-top and foam mattresses, and closed air-conditioned rooms, take longer. Keep the room airy, use a fan if you have one, and do not put bedding back until the mattress is dry.'],
  ['What should I send on WhatsApp for a quote?', 'A photo of the whole mattress, close-ups of the stains, the mattress size, the label if there is one, and your postal code.'],
  ['Do I need to do anything before you arrive?', 'Strip the sheets, protector and any topper, and clear space around the bed so we can reach all sides. Let us know about anyone at home with allergies or sensitivities.'],
  ['When can you come?', 'We are open 24/7. Within about 8 km of Punggol, Sengkang and Tampines we offer a 3-hour call-out; the rest of Singapore is same-day. We confirm the time on WhatsApp.'],
];
function mattressProcess(): string {
  return `<section class="section-ozone py-16" id="mattress-process"><div class="container-prose"><div class="mx-auto max-w-2xl text-center"><p class="text-xs font-semibold uppercase tracking-widest text-brand-ochre-dark">The Process</p><h2 class="mt-2 text-3xl font-bold text-brand-slate sm:text-4xl">Our Mattress Cleaning Process</h2><p class="mt-4 text-lg text-brand-slate/70">Every mattress is checked first, then cleaned with as little moisture as the filling needs.</p></div><ol class="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">${MATTRESS_STEPS.map(([t, d], i) => `<li class="relative rounded-2xl border border-brand-slate/10 bg-white p-6 shadow-sm"><span class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-brand-slate text-sm font-bold text-white">${i + 1}</span><h3 class="mt-4 text-lg font-semibold text-brand-slate">${esc(t)}</h3><p class="mt-2 text-sm leading-relaxed text-brand-slate/70">${esc(d)}</p></li>`).join('')}</ol></div></section>`;
}
function mattressDepth(): string {
  const types = table(['Mattress type', 'How we clean it', 'What to know'], [
    ['Pocket spring or coil, with a fabric cover', 'Vacuum, pre-treat, then controlled cleaning and extraction. Hot steam add-on if the cover suits it.', 'Usually the most forgiving. Drying about 4–8 hours.'],
    ['Memory foam', 'Vacuum, pre-treat, low-moisture cleaning and extraction. Steam only if the cover and foam suit it.', 'Foam holds water, so we keep moisture low. Follow the maker\'s care label.'],
    ['Latex', 'Vacuum, gentle low-moisture cleaning and extraction. No heavy steam.', 'Latex should not be soaked or heated. Allow full airflow while it dries.'],
    ['Hybrid and pillow-top', 'Vacuum the quilting and seams well, pre-treat, then controlled cleaning and extraction.', 'Thick tops take longer to dry. Do not put bedding back while damp.'],
    ['Baby and children\'s mattresses', 'Same steps, with low moisture. Tell us about allergies or sensitivities when you ask for a quote.', 'Keep children off the mattress until it is fully dry.'],
  ]);
  const stains = table(['Problem', 'What to do now', 'What cleaning can do'], [
    ['Urine or bedwetting', 'Blot with paper towels. Do not use hot water or a steamer.', 'Fresh accidents usually improve well. Repeated or deep urine can leave some smell on humid days.'],
    ['Yellow sweat marks', 'Use a protector and wash it every 2–4 weeks.', 'Usually lighten a lot. Very old marks may not fully disappear.'],
    ['Blood', 'Blot with cold water only. Heat sets blood.', 'Fresh blood often lifts well. Old blood may leave a faint mark.'],
    ['Food and drink', 'Blot, do not rub. Lift any solids first.', 'Most spills improve. Coloured drinks can leave a shadow.'],
    ['Musty smell or mould spots', 'Air the room and dry the mattress fully.', 'Surface marks and smell can improve. Mould deep inside the filling may mean the mattress should be replaced, and we will tell you.'],
    ['Bed bugs', 'Call a pest control company.', 'Cleaning does not get rid of bed bugs.'],
  ]);
  return sec('Mattress types we clean', P('How a mattress is built decides how much water and heat it can take. We check the type and any care label before choosing the method.') + types, 'mattress-types')
    + sec('Mattress stains and what to expect', P('Results depend on the stain and how long it has been there. We tell you from your photos what is likely to improve, and we do not promise that every stain will come out.') + stains, 'mattress-stains')
    + sec('Before and after your appointment', '<h3>Before we arrive</h3>' + ul(['Strip the sheets, mattress protector and any topper.', 'Clear space around the bed so we can reach every side.', 'Tell us about stains you want us to focus on, and about anyone at home with allergies.']) + '<h3>After cleaning</h3>' + ul(['Keep the room airy and run a fan if you have one. Drying usually takes about 4–8 hours.', 'Do not put sheets back on a damp mattress.', 'Use a mattress protector and wash it every 2–4 weeks to keep sweat out of the mattress.', 'Vacuum the mattress every few weeks and rotate it if the maker allows.']), 'mattress-care');
}
function mattressPage(h: string): string {
  h = setHead(h, 'Mattress Cleaning Singapore from $80 | Sofa Care Singapore', 'Mattress cleaning services in Singapore from $80 for a single or super single. WhatsApp photos for urine, stain and odour assessment and an available slot.', 'Mattress Cleaning Singapore');
  h = replaceRealResults(h, `<section class="sc-real" aria-labelledby="sc-real-h" data-sofacare-real-results data-sofacare-service-photo><div class="sc-real-in"><h2 id="sc-real-h">Real mattress cleaning results</h2><p class="sc-real-sub">Photos from real Sofa Care Singapore mattress jobs. Drag each slider to compare before and after.</p><div class="sc-ba-list">${JOBS.filter((j) => j.kind === 'mattress').map(slider).join('')}${oldSlider(2)}</div></div></section>`);
  h = replaceSection(h, 'Our Sofa Cleaning Process', mattressProcess() + mattressDepth());
  const f = h.indexOf('Mattress Cleaning FAQ');
  if (f === -1) throw Error('Head terms: mattress FAQ missing');
  const s = h.lastIndexOf('<section', f), e = h.indexOf('</section>', f);
  const faqSec = h.slice(s, e + 10).replace(/(<div class="mx-auto mt-10 max-w-3xl space-y-3">)[\s\S]*(<\/div><\/div><\/section>)$/, (_m, a, b) => a + faqItems(MATTRESS_FAQ) + b);
  if (!faqSec.includes(MATTRESS_FAQ[1][0].slice(0, 20))) throw Error('Head terms: mattress FAQ layout changed');
  h = h.slice(0, s) + faqSec + h.slice(e + 10);
  return syncFaqSchema(h);
}

// ---------- Sofa page ----------
function sofaDepth(): string {
  const fabrics = table(['Material', 'How to recognise it', 'How we clean it'], [
    ['Cotton and linen', 'Matte woven fabric; you can see the threads. Labels are often W or WS.', 'Vacuum, pre-treat, then injection and extraction if a hidden-spot test is fine. Natural fibres can shrink or brown if over-wetted, so moisture is kept controlled.'],
    ['Polyester and microfibre', 'Smooth, tightly woven or suede-like. Labels are often W, WS or S.', 'W and WS: injection and extraction. S-coded microfibre: low-moisture cleaning only, because water can leave rings.'],
    ['Velvet and chenille', 'A soft pile that changes shade when brushed the other way.', 'Low-moisture cleaning worked with the pile, then the pile is brushed back. Steam only if the label and a test allow it.'],
    ['Mixed or unknown fabric', 'No label, or a blend you are not sure about.', 'We test a hidden spot first and choose the gentlest method that works.'],
    ['Leather', 'A smooth or grained hide.', `Leather is a different job, quoted from photos. See <a href="/${LEATHER_PAGE}">leather sofa cleaning</a>.`],
  ]);
  const labels = table(['Care code', 'What it means'], [['W', 'Water-based cleaning is fine.'], ['S', 'Solvent or low-moisture cleaning only, no water.'], ['WS', 'Either method is fine.'], ['X', 'Vacuum or brush only. No wet cleaning.']]);
  const stains = table(['Stain', 'What to do now', 'What cleaning can do'], [
    ['Coffee and tea', 'Blot with a dry cloth. Do not rub.', 'Fresh spills usually lift well. Old ones may leave a light shadow.'],
    ['Food and oil', 'Lift solids, then blot. Avoid soap, which spreads oil.', 'Usually improves well with pre-treatment.'],
    ['Sweat and body oil (arms, headrests)', 'Wipe gently; do not scrub the pile.', 'Darkened areas usually lighten a lot.'],
    ['Pet or child urine', 'Blot with paper towels. No hot water.', 'Fresh urine improves well. Urine that soaked into the foam can leave some smell on humid days.'],
    ['Milk and vomit', 'Remove solids, blot with cold water only.', 'Usually improves; the smell can need a second treatment.'],
    ['Ink and dye transfer', 'Do not use alcohol or wipes on the fabric.', 'May only partly lift, depending on the ink and fabric.'],
    ['Musty smell or mould spots', 'Air the room and keep the sofa dry.', 'Surface mould spots and smell can improve; deep mould inside cushions may not.'],
  ]);
  const velvet = JOBS.find((j) => j.kind === 'velvet')!;
  return sec('Fabric types and how we clean them', P('Start with the care label under a seat cushion or on the base. It tells us which methods are safe. Fabric sofa cleaning starts from $60 for a 1-seater.') + labels + fabrics + '<h3>Velvet example</h3>' + P('A real velvet job: small brown spots on a cream tufted armchair, cleaned with a low-moisture method and the pile brushed back.') + slider(velvet), 'sofa-fabrics')
    + sec('Sofa stains and what to expect', P('Results depend on the stain, the fabric and how long the stain has been there. We tell you from your photos what is likely to improve, and we do not promise that every stain will come out.') + stains, 'sofa-stains');
}
function sofaPage(h: string): string {
  h = setHead(h, 'Sofa Cleaning Singapore from $60 | Sofa Care Singapore', 'On-site sofa cleaning in Singapore from $60 for a 1-seater fabric sofa. Send photos on WhatsApp for stain assessment, a confirmed quote and available slots.', 'Sofa Cleaning Singapore');
  h = replaceRealResults(h, `<section class="sc-real" aria-labelledby="sc-real-h" data-sofacare-real-results data-sofacare-service-photo><div class="sc-real-in"><h2 id="sc-real-h">Real sofa cleaning results</h2><p class="sc-real-sub">Photos from real Sofa Care Singapore sofa jobs. Drag each slider to compare before and after.</p><div class="sc-ba-list">${JOBS.filter((j) => j.kind === 'sofa').map(slider).join('')}${oldSlider(0)}${oldSlider(1)}</div></div></section>`);
  const i = h.indexOf('Our Sofa Cleaning Process');
  if (i === -1) throw Error('Head terms: sofa process missing');
  const s = h.lastIndexOf('<section', i);
  h = h.slice(0, s) + sofaDepth() + h.slice(s);
  // Leather summary on the sofa page points to the leather page instead of competing with it.
  h = h.replace(/(<h3>Leather sofa cleaning<\/h3>[\s\S]*?)(<h3>)/, (_m, a, b) => a + P(`Leather is quoted from photos. Read how we assess and clean it on our <a href="/${LEATHER_PAGE}">leather sofa cleaning page</a>.`) + b);
  return h;
}

// ---------- Leather page ----------
const LEATHER_FAQ: [string, string][] = [
  ['How much does leather sofa cleaning cost?', 'Leather is quoted from photos, because the price depends on the leather type, the size of the sofa and its condition. The fabric sofa prices on our pricing page are not leather prices.'],
  ['Is my sofa real leather or PU?', 'Real leather has small, uneven grain and creases and smells like leather. PU (faux leather) and bonded leather have a very even pattern and can peel or flake. A photo of the label or a peeling corner helps us tell.'],
  ['Do you steam clean leather?', 'Not as a rule. Steam can damage many leathers. Aniline, nubuck and suede are never steamed. Protected leather is cleaned with a gentle leather cleaner that is wiped off, not soaked in.'],
  ['Will cleaning remove ink or dye transfer?', 'Sometimes partly. Fresh ink and jeans dye on protected leather can improve; ink that has soaked into aniline leather usually cannot be fully removed. We tell you from a close-up photo.'],
  ['Can you fix cracks, peeling or scratches?', 'No. Cracks, peeling and scratches are damage, not dirt. Cleaning can make the surface look more even, but it cannot repair the hide or the coating.'],
  ['Do you condition the leather?', 'Only where it suits the leather and you want it. Some finishes should not be conditioned. We tell you on WhatsApp what we recommend for your sofa.'],
  ['How long until I can use the sofa?', 'Leather is cleaned with little moisture, so the surface is usually dry to the touch soon after. If it was conditioned, allow time before heavy use. We give you the timing for your sofa.'],
  ['When can you come?', 'We are open 24/7. Within about 8 km of Punggol, Sengkang and Tampines we offer a 3-hour call-out; the rest of Singapore is same-day. We confirm the time on WhatsApp.'],
];
function leatherHead(): string {
  const url = `${SITE}/${LEATHER_PAGE}`;
  const title = 'Leather Sofa Cleaning Singapore | Sofa Care Singapore';
  const desc = 'Leather sofa cleaning in Singapore with a material-specific assessment. WhatsApp photos of your sofa and care label for suitable treatment advice and a quote.';
  const ld = [
    { '@context': 'https://schema.org', '@type': 'WebPage', '@id': url + '#webpage', name: 'Leather Sofa Cleaning Singapore', description: desc, url },
    { '@context': 'https://schema.org', '@type': 'Service', '@id': url + '#service', name: 'Leather Sofa Cleaning Singapore', serviceType: 'Leather sofa cleaning', url, description: desc, provider: { '@id': `${SITE}/#business` }, areaServed: [{ '@type': 'Country', name: 'Singapore' }, ...['Punggol', 'Sengkang', 'Tampines', 'Pasir Ris', 'Hougang'].map((n) => ({ '@type': 'Place', name: n }))] },
    { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE}/` }, { '@type': 'ListItem', position: 2, name: 'Sofa cleaning', item: `${SITE}/sofa-cleaning-singapore.html` }, { '@type': 'ListItem', position: 3, name: 'Leather sofa cleaning', item: url }] },
    { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: LEATHER_FAQ.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
  ];
  return `<title>${esc(title)}</title><meta name="description" content="${esc(desc)}"/><link rel="canonical" href="${url}"/><meta property="og:title" content="${esc(title)}"/><meta property="og:description" content="${esc(desc)}"/><meta property="og:url" content="${url}"/><meta name="twitter:title" content="${esc(title)}"/><meta name="twitter:description" content="${esc(desc)}"/>`
    + ld.map((d) => `<script type="application/ld+json">${JSON.stringify(d).replace(/</g, '\\u003c')}</script>`).join('');
}
function leatherMain(): string {
  const path = LEATHER_PAGE;
  const msg = 'Hi Sofa Care Singapore, I\'d like a quote for leather sofa cleaning.\nPostal code: ___\nSofa size: ___\nI will send photos and the care label.';
  const types = table(['Leather type', 'How to recognise it', 'How it is cleaned'], [
    ['Protected (pigmented) leather', 'Even colour, a light coating on top. A drop of water sits on the surface. Most family sofas are this type.', 'Gentle leather cleaner worked in with a soft brush or cloth and wiped off. Conditioning only if it suits the finish.'],
    ['Aniline and semi-aniline', 'Natural look with visible pores; a drop of water darkens it quickly.', 'Very gentle, low-moisture cleaning only. No steam. Some marks cannot be removed without risk, and we will say so.'],
    ['Nubuck and suede', 'Soft, velvety surface that marks when you brush it.', 'Dry methods and specialist care only. No water-based or steam cleaning. We may suggest a specialist.'],
    ['Bonded leather and PU (faux leather)', 'Very even pattern; may peel or flake at seams and seat edges.', 'Gentle surface clean. Peeling and flaking are coating damage and cannot be repaired by cleaning.'],
  ]);
  const problems = table(['Problem', 'What cleaning can do'], [
    ['Darkened headrests and arms (body oil)', 'Usually improves well on protected leather.'],
    ['Food and drink spills', 'Usually wipe clean if they have not soaked in.'],
    ['Ink and jeans dye transfer', 'May partly improve on protected leather; often permanent on aniline.'],
    ['Cracks, peeling, scratches, fading', 'Damage, not dirt. Cleaning cannot repair it.'],
    ['Smell', 'Surface odour can improve. Smell that has soaked into the foam may remain.'],
  ]);
  const body =
    sec('How we handle leather sofas', P('Leather is not cleaned like fabric. Fabric sofas get injection and extraction; leather does not. Every leather sofa is checked first: the type of leather, the finish, any coating damage and the marks you want treated. We test the cleaner on a hidden spot before working on the whole sofa.') + P('Because the right method depends on the leather, we quote leather sofas from your photos, not from the fabric price list.') + waBtn(path, 'LEATHER_TOP', 'WhatsApp photos of your leather sofa', msg), 'leather-how')
    + sec('Leather types', P('The type of leather decides what is safe. If you are not sure, send a close-up photo and the care label or brand.') + types, 'leather-types')
    + sec('What we do on the day', '<ol class="sc-list">' + [
      'Check the leather type, finish and condition with you, and point out existing cracks, peeling or fading.',
      'Test the cleaner on a hidden spot.',
      'Vacuum seams, crevices and under the cushions.',
      'Clean the surface gently with a leather-safe cleaner, worked in and wiped off. No soaking, no fabric extraction.',
      'Condition only if it suits the leather and you want it.',
      'Look over the result with you and explain aftercare.',
    ].map((s) => `<li>${esc(s)}</li>`).join('') + '</ol>', 'leather-steps')
    + sec('Stains and damage: what to expect', P('We tell you from your photos what is likely to improve. Cleaning removes dirt; it does not repair damage.') + problems, 'leather-limits')
    + sec('What to send for a quote', ul(['A photo of the whole sofa and one of each seat.', 'Close-ups of the marks, cracks or peeling.', 'The care label or brand, if you have it.', 'Your postal code.']) + waBtn(path, 'LEATHER_MID', 'Send photos for a leather quote', msg), 'leather-quote')
    + sec('Looking after leather', ul(['Dust with a soft dry cloth every week.', 'Wipe spills straight away with a soft damp cloth, then dry it.', 'Keep leather out of direct afternoon sun and away from air-con vents blowing straight onto it.', 'Do not use baby wipes, alcohol, bleach, household detergents or a home steamer.', 'Follow the maker\'s care instructions if you have them.']), 'leather-care')
    + sec('Related services', `<p class="sc-ht-links">Fabric sofas: <a href="/sofa-cleaning-singapore.html">sofa cleaning Singapore</a> (from $60) · Mattresses: <a href="/mattress-cleaning-singapore.html">mattress cleaning services</a> (from $80) · Guides: <a href="/articles/leather-sofa-cleaning-cost-singapore.html">leather sofa cleaning cost</a>, <a href="/articles/can-you-steam-clean-a-leather-sofa-singapore.html">can you steam clean a leather sofa?</a>, <a href="/articles/leather-vs-fabric-sofa-cleaning-singapore.html">leather vs fabric sofa cleaning</a>, <a href="/articles/recommend-sofa-cleaning-singapore-leather-couches.html">choosing a leather couch cleaner</a> · <a href="/pricing.html">Full price table</a></p>`, 'leather-related');
  return `<main class="flex-1 pb-20 md:pb-0"><nav aria-label="Breadcrumb" class="container-prose pt-6"><ol class="flex flex-wrap items-center gap-1.5 text-sm text-muted-foreground"><li class="flex items-center gap-1.5"><a class="hover:text-brand-slate" href="/">Home</a></li><li class="flex items-center gap-1.5" aria-hidden="true">/</li><li class="flex items-center gap-1.5"><a class="hover:text-brand-slate" href="/sofa-cleaning-singapore.html">Sofa cleaning</a></li><li class="flex items-center gap-1.5" aria-hidden="true">/</li><li class="flex items-center gap-1.5" aria-current="page">Leather sofa cleaning</li></ol></nav>`
    + `<section class="border-b border-brand-slate/10 bg-brand-ozone"><div class="container-prose py-12 md:py-16"><div class="max-w-3xl"><p class="text-xs font-semibold uppercase tracking-widest text-brand-ochre-dark">Leather · Open 24/7</p><h1 class="mt-2 text-4xl font-bold text-brand-slate sm:text-5xl">Leather Sofa Cleaning Singapore</h1><p class="mt-4 text-lg text-brand-slate/80">On-site leather sofa cleaning, matched to your leather type. Send photos of your sofa and its care label on WhatsApp and we will tell you what is safe, what is likely to improve, and your quote.</p><p class="mt-3 text-brand-slate/80">Open 24/7. 3-hour call-out within about 8 km of Punggol, Sengkang and Tampines; same-day for the rest of Singapore.</p></div>${waBtn(path, 'LEATHER_HERO', 'WhatsApp photos for a leather quote', msg)}</div></section>`
    + body
    + `<section class="py-16"><div class="container-prose"><div class="mx-auto max-w-2xl text-center"><p class="text-xs font-semibold uppercase tracking-widest text-brand-ochre-dark">FAQ</p><h2 class="mt-2 text-3xl font-bold text-brand-slate sm:text-4xl">Leather Sofa Cleaning FAQ</h2></div><div class="mx-auto mt-10 max-w-3xl space-y-3">${faqItems(LEATHER_FAQ)}</div></div></section>`
    + `<section class="bg-brand-slate py-16"><div class="container-prose text-center"><h2 class="text-3xl font-bold text-white sm:text-4xl">Send us a photo of your leather sofa</h2><p class="mx-auto mt-4 max-w-2xl text-white/70">Open 24/7. WhatsApp +65 9025 9771 with photos, the care label and your postal code.</p>${waBtn(path, 'LEATHER_END', 'WhatsApp Sofa Care Singapore', msg)}</div></section></main>`;
}

// ---------- Prices: same table everywhere, steam +$20 ----------
function prices(h: string, p: string): string {
  const steamRow = (row: string, label: string, price: string) => row.replace(label, 'Hot steam add-on (where the material suits it)').replace(price, '+$20');
  // Service page and pricing sofa tables: add a steam row after the L-shape row.
  h = h.replace(/<tr\b(?:(?!<\/tr>)[\s\S])*L-shaped \/ sectional sofa(?:(?!<\/tr>)[\s\S])*<\/tr>/, (row) => h.includes('Hot steam add-on (where the material suits it)') || p === 'pricing.html' ? row : row + steamRow(row, 'L-shaped / sectional sofa', '+$20 add-on'));
  if (p === 'mattress-cleaning-singapore.html') h = h.replace(/<tr\b(?:(?!<\/tr>)[\s\S])*King mattress(?:(?!<\/tr>)[\s\S])*<\/tr>/, (row) => row + steamRow(row, 'King mattress', '$97'));
  if (p === 'index.html') h = h.replace('<tr><td>Mattress cleaning (single / super single)</td><td>from $80</td></tr>', (r) => r + '<tr><td>Queen / King mattress</td><td>$87 / $97</td></tr><tr><td>Hot steam add-on (where the material suits it)</td><td>+$20</td></tr><tr><td>Leather sofa</td><td>Photo quote</td></tr>');
  // "from $20" for steam becomes "+$20" in visible text (Edwin 8 Nov: steam is +$20).
  return h.replace(/(<td>[^<]*[Ss]team[^<]*<\/td>\s*<td>)from \$20/g, '$1+$20')
    .replace(/(steam[^<.]{0,60}?)(?:starts |is available )?from \$20/gi, '$1+$20')
    .replace(/add-on \+\$20 where/g, 'add-on (+$20) where');
}

// ---------- Internal links ----------
const AREA_ANCHORS: [string, string][] = [['sofa cleaning Singapore', 'mattress cleaning Singapore'], ['professional sofa cleaning', 'mattress cleaning services'], ['sofa cleaning', 'mattress cleaning'], ['fabric sofa cleaning', 'mattress deep cleaning'], ['sofa cleaning Singapore', 'mattress cleaning services']];
export type LinkRow = [string, string, string];
function hubLine(p: string, leather: boolean, log: LinkRow[]): string {
  const links: [string, string][] = leather
    ? [[LEATHER_PAGE, 'leather sofa cleaning'], ['sofa-cleaning-singapore.html', 'fabric sofa cleaning'], ['mattress-cleaning-singapore.html', 'mattress cleaning']]
    : [['sofa-cleaning-singapore.html', 'sofa cleaning in Singapore'], ['mattress-cleaning-singapore.html', 'mattress cleaning in Singapore']];
  links.forEach(([d, a]) => log.push(['/' + p, '/' + d, a]));
  return `<p class="sc-ht-links" data-sc-hub-links><strong>Our services:</strong> ${links.map(([d, a]) => `<a href="/${d}">${esc(a)}</a>`).join(' · ')}</p>`;
}

export function applySofaHeadTerms(files: Record<string, string>, areaSlugs: string[]): LinkRow[] {
  const log: LinkRow[] = [];
  const base = files['sofa-cleaning-singapore.html'];
  if (!base) throw Error('Head terms: sofa page missing');
  // New leather page, cloned from the sofa page shell before the sofa page itself changes.
  files[LEATHER_PAGE] = cloneSofaShell(base, leatherHead(), leatherMain(), 'sofa-cleaning-singapore.html', LEATHER_PAGE);
  if (!files['sitemap.xml'].includes(`${SITE}/${LEATHER_PAGE}<`)) files['sitemap.xml'] = files['sitemap.xml'].replace('</urlset>', `<url><loc>${SITE}/${LEATHER_PAGE}</loc></url></urlset>`);
  files['mattress-cleaning-singapore.html'] = mattressPage(files['mattress-cleaning-singapore.html']);
  files['sofa-cleaning-singapore.html'] = sofaPage(files['sofa-cleaning-singapore.html']);
  files['index.html'] = setHead(files['index.html'], 'Sofa Care Singapore | Sofa & Mattress Cleaning, Open 24/7', 'Sofa Care Singapore offers on-site sofa and mattress cleaning. Open 24/7. WhatsApp photos and your postal code for a quote and available appointment.', 'Sofa Care Singapore: Sofa & Mattress Cleaning');
  // Home service chooser: add leather next to sofa and mattress.
  files['index.html'] = files['index.html'].replace('<p class="sc-more-guides"', `<p class="sc-ht-links" data-sc-chooser><strong>Choose a service:</strong> <a href="/sofa-cleaning-singapore.html">Sofa cleaning (fabric, from $60)</a> · <a href="/mattress-cleaning-singapore.html">Mattress cleaning (from $80)</a> · <a href="/${LEATHER_PAGE}">Leather sofa cleaning (photo quote)</a></p><p class="sc-more-guides"`);
  log.push(['/', '/sofa-cleaning-singapore.html', 'Sofa cleaning (fabric, from $60)'], ['/', '/mattress-cleaning-singapore.html', 'Mattress cleaning (from $80)'], ['/', '/' + LEATHER_PAGE, 'Leather sofa cleaning (photo quote)']);
  // Hubs link each other.
  for (const [p, links] of [
    ['sofa-cleaning-singapore.html', [['mattress-cleaning-singapore.html', 'mattress cleaning services'], [LEATHER_PAGE, 'leather sofa cleaning'], ['pricing.html', 'full price table']]],
    ['mattress-cleaning-singapore.html', [['sofa-cleaning-singapore.html', 'professional sofa cleaning'], [LEATHER_PAGE, 'leather sofa cleaning'], ['pricing.html', 'full price table']]],
  ] as [string, [string, string][]][]) {
    const line = `<p class="sc-ht-links" data-sc-hub-links><strong>Also from Sofa Care Singapore:</strong> ${links.map(([d, a]) => `<a href="/${d}">${esc(a)}</a>`).join(' · ')}</p>`;
    files[p] = files[p].replace('</main>', `<section class="sc-home-sec"><div class="sc-in">${line}</div></section></main>`);
    links.forEach(([d, a]) => log.push(['/' + p, '/' + d, a]));
  }
  ['sofa-cleaning-singapore.html', 'mattress-cleaning-singapore.html', 'pricing.html'].forEach((d) => log.push(['/' + LEATHER_PAGE, '/' + d, d.replace('.html', '').replace(/-/g, ' ')]));
  // Area pages: one sofa and one mattress link each, anchors varied across pages.
  areaSlugs.forEach((p, i) => {
    if (!files[p] || files[p].includes('data-sc-area-hubs')) return;
    const [a1, a2] = AREA_ANCHORS[i % AREA_ANCHORS.length];
    files[p] = files[p].replace('</main>', `<section class="sc-home-sec"><div class="sc-in"><p class="sc-ht-links" data-sc-area-hubs>Prices and the full process: <a href="/sofa-cleaning-singapore.html">${esc(a1)}</a> and <a href="/mattress-cleaning-singapore.html">${esc(a2)}</a>. Leather sofas are on our <a href="/${LEATHER_PAGE}">leather sofa cleaning</a> page.</p></div></section></main>`);
    log.push(['/' + p, '/sofa-cleaning-singapore.html', a1], ['/' + p, '/mattress-cleaning-singapore.html', a2], ['/' + p, '/' + LEATHER_PAGE, 'leather sofa cleaning']);
  });
  // Articles: both hubs (leather articles: leather page first), and a twitter:title where missing.
  for (const p of Object.keys(files).filter((k) => /^articles\/[^/]+\.html$/.test(k))) {
    let h = files[p];
    const leather = /leather/.test(p);
    if (!h.includes('data-sc-hub-links')) h = h.replace('</article>', hubLine(p, leather, log) + '</article>');
    if (!/<meta name="twitter:title"/.test(h)) {
      const og = (h.match(/<meta property="og:title" content="([^"]*)"/) || [])[1];
      if (og) h = h.replace(/(<meta property="og:title" content="[^"]*"\/?>)/, `$1<meta name="twitter:title" content="${og}"/>`);
    }
    files[p] = h;
  }
  for (const p of Object.keys(files)) if (p.endsWith('.html') && !['lead-log.html', '404.html'].includes(p)) files[p] = prices(files[p], p);
  // Slider script and styles on pages that have sliders.
  for (const p of Object.keys(files)) if (p.endsWith('.html') && files[p].includes('data-sc-ba') && !files[p].includes('sc-ba-range\')')) files[p] = files[p].replace('</body>', SLIDER_JS + '</body>');
  files['sofacare-design-v2.css'] += '\n' + sofaHeadTermStyles;
  return log;
}

export const SOFA_LEATHER_LLMS = `- [Leather sofa cleaning Singapore](${SITE}/${LEATHER_PAGE}): leather sofas, quoted from photos`;

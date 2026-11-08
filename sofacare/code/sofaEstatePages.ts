// Estate pages (Edwin, 8 Nov 2026): 9 estates under the Punggol, Sengkang and Tampines area pages.
// Landmarks are kept to places we are sure are in or next to each estate. Photos are real Sofa Care
// jobs with unknown locations, so the pages never say a photo was taken in the estate.
// Prices only from the published table. Coverage wording as on the area pages.
import { cloneSofaShell } from './sofaAreaPages.ts';
import { JOBS, slider, SLIDER_JS } from './sofaHeadTerms.ts';

const SITE = 'https://sofacaresg.com';
const WA = '6590259771';
const esc = (s: string) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

type Estate = {
  slug: string; name: string; area: string; parent: string; title: string; desc: string;
  lede: string; around: string[]; homes: string[]; photos: [string, string]; faqs: [string, string][];
};

const CALLOUT = '3-hour call-out response within about 8 km of Punggol, Sengkang and Tampines. Same-day service for addresses beyond 8 km (the rest of Singapore).';

export const SOFA_ESTATES: Estate[] = [
  {
    slug: 'sofa-cleaning-punggol-sumang.html', name: 'Sumang', area: 'Punggol', parent: 'sofa-cleaning-punggol.html',
    title: 'Sofa & Mattress Cleaning Sumang, Punggol | Sofa Care Singapore',
    desc: 'On-site sofa and mattress cleaning in Sumang, Punggol. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Sumang, on the west side of Punggol. Send a photo and your postal code on WhatsApp and we will confirm the price and the earliest slot. We are open 24/7.',
    around: [
      'Sumang is on the Punggol West LRT loop. Sumang LRT station is in the estate, with Soo Teck and Nibong LRT stations either side of it, and Punggol Waterway Park is a short walk away.',
      'Punggol MRT station and Waterway Point are a few LRT stops away, so most Sumang blocks are a quick trip for us from anywhere in Punggol.',
    ],
    homes: [
      'Homes in Sumang are mostly HDB flats, many of them recent BTOs, so a lot of the sofas we are asked about are fabric L-shapes and 3-seaters bought for a new flat, and the mattresses are often still fairly new.',
      'New sofas pick up stains fast in the first few years: drinks, food on the arms, and body oil on the headrest. Cleaning early, before a stain has sat for months, usually gives the best result.',
    ],
    photos: ['grey-2seater-fabric-sofa', 'mattress-urine-stain'],
    faqs: [
      ['Do you clean sofas and mattresses in Sumang?', 'Yes. We clean on-site at your home in Sumang and across Punggol. We are open 24/7, and the time is confirmed on WhatsApp before we come.'],
      ['How fast can you come to Sumang?', 'Sumang is in Punggol, inside our 3-hour call-out area. Send your postal code and a photo on WhatsApp and we will confirm the earliest slot.'],
      ['My sofa is quite new. Is it worth cleaning already?', 'Often, yes. Fresh stains and early body-oil marks usually lift much better than ones left for a long time. Send a photo and we will tell you what to expect.'],
      ['How much does it cost?', 'Sofa cleaning starts from $60 and mattress cleaning from $80. The full price table is on this page, and your final price is confirmed on WhatsApp.'],
    ],
  },
  {
    slug: 'sofa-cleaning-punggol-waterway-point.html', name: 'Waterway Point', area: 'Punggol', parent: 'sofa-cleaning-punggol.html',
    title: 'Sofa Cleaning Waterway Point, Punggol | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning around Waterway Point and Punggol Point. Open 24/7, 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp for a quote.',
    lede: 'We clean sofas and mattresses on-site in the homes around Waterway Point in Punggol Central and up towards Punggol Point. WhatsApp a photo and your postal code for a quote and the earliest slot. Open 24/7.',
    around: [
      'Waterway Point is the mall next to Punggol MRT station and the bus interchange in Punggol Central, with the Punggol Waterway running beside it.',
      'Further north, Punggol Point Park and Punggol Point LRT station are near the coast, along the Punggol Promenade.',
    ],
    homes: [
      'This part of Punggol has HDB flats and condos close to the Waterway and the coast. Homes near the water can feel humid, and humidity slows drying after a clean.',
      'After we clean, keep air moving: a fan, or a window open for a while, helps more than leaving the air-con on in a closed room. Drying usually takes about 4 to 8 hours.',
    ],
    photos: ['cream-velvet-tufted-armchair', 'mattress-heart-pattern'],
    faqs: [
      ['Do you come to homes near Waterway Point?', 'Yes. We clean on-site across Punggol Central, the Waterway and up to Punggol Point. We are open 24/7.'],
      ['How fast can you get here?', 'Punggol is inside our 3-hour call-out area. Send your postal code and a photo on WhatsApp and we confirm the earliest slot.'],
      ['My flat is near the water and feels damp. Will the sofa dry?', 'Yes, it just needs airflow. Run a fan or open a window, and allow about 4 to 8 hours before heavy use.'],
      ['Can you clean a velvet armchair?', 'Yes, where the care label allows it. Velvet is cleaned with low moisture and brushed with the pile. Send a photo of the chair and its label.'],
    ],
  },
  {
    slug: 'sofa-cleaning-punggol-northshore.html', name: 'Northshore', area: 'Punggol', parent: 'sofa-cleaning-punggol.html',
    title: 'Sofa & Mattress Cleaning Northshore | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Punggol Northshore. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Northshore, the newer estate along Punggol\'s northern shore. WhatsApp a photo and your postal code for a quote and the earliest slot. Open 24/7.',
    around: [
      'Northshore sits along Northshore Drive on Punggol\'s northern coast. Samudera and Punggol Point LRT stations serve the estate, and Northshore Plaza has shops and food.',
      'Punggol Coast MRT station and the Punggol Digital District are close by.',
    ],
    homes: [
      'Northshore is mostly newer HDB flats facing the sea. Many households are young families, so we often see milk and food spills on fabric seats and toilet-training accidents on children\'s mattresses.',
      'Sea air is humid. After cleaning, give the room airflow with a fan or an open window so the sofa or mattress dries well, usually in about 4 to 8 hours.',
    ],
    photos: ['grey-3seater-recliner-sofa', 'mattress-scallop-yellow-stain'],
    faqs: [
      ['Do you clean in Northshore?', 'Yes. We clean on-site in Northshore and across Punggol, 24/7.'],
      ['How fast can you come to Northshore?', 'Northshore is in Punggol, inside our 3-hour call-out area. Send your postal code and a photo and we confirm the earliest slot.'],
      ['Can you clean a child\'s mattress after accidents?', 'Yes. We treat the area and extract as much as the mattress allows. Old or repeated accidents may only partly improve, and we tell you that from your photos first.'],
      ['Can you clean a fabric recliner?', 'Yes. Fabric recliners are cleaned like other fabric sofas, with care around the moving parts. Leather recliners are quoted from photos.'],
    ],
  },
  {
    slug: 'sofa-cleaning-sengkang-rivervale.html', name: 'Rivervale', area: 'Sengkang', parent: 'sofa-cleaning-sengkang.html',
    title: 'Sofa & Mattress Cleaning Rivervale | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Rivervale, Sengkang. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Rivervale, on the east side of Sengkang. Send a photo and your postal code on WhatsApp and we confirm the price and the earliest slot. Open 24/7.',
    around: [
      'Rivervale is on the Sengkang East LRT loop, served by stations such as Rumbia, Bakau and Kangkar. Rivervale Mall and Rivervale Plaza are the neighbourhood shopping centres.',
      'Sengkang MRT station and Compass One are a short LRT ride away.',
    ],
    homes: [
      'Rivervale has many HDB flats that have been lived in for a good number of years, so sofas and mattresses here have often had years of daily use.',
      'Older fabric sofas usually have built-up body oil on the arms and headrests and general dulling across the seats. That usually improves well. Wear, fading and very old stains may not, and we tell you before we start.',
    ],
    photos: ['grey-2seater-fabric-sofa', 'mattress-pillowtop-stain'],
    faqs: [
      ['Do you clean in Rivervale?', 'Yes. We clean on-site in Rivervale and across Sengkang, 24/7.'],
      ['How fast can you come to Rivervale?', 'Sengkang is inside our 3-hour call-out area. Send your postal code and a photo on WhatsApp and we confirm the earliest slot.'],
      ['My sofa is many years old. Is it worth cleaning?', 'Often, yes. Built-up dirt and body oil usually improve a lot. Fabric wear and fading do not, so we tell you what to expect from your photos.'],
      ['How much does a queen mattress cost?', 'A queen mattress is $87. Single and super single start from $80, and a king is $97.'],
    ],
  },
  {
    slug: 'sofa-cleaning-sengkang-anchorvale.html', name: 'Anchorvale', area: 'Sengkang', parent: 'sofa-cleaning-sengkang.html',
    title: 'Sofa & Mattress Cleaning Anchorvale | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Anchorvale, Sengkang. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Anchorvale, Sengkang. WhatsApp a photo and your postal code for a quote and the earliest slot. We are open 24/7.',
    around: [
      'Anchorvale Community Club and Sengkang Sports Centre stand together on Anchorvale Road, and Sengkang Riverside Park is nearby.',
      'Sengkang MRT station and Compass One are a short trip away.',
    ],
    homes: [
      'Anchorvale is mostly HDB flats, with many families. Active households mean sweat and body oil on sofa seats and headrests, and sweat marks on mattresses.',
      'Yellow sweat marks on a mattress usually lighten a lot with cleaning. A washable mattress protector afterwards keeps it cleaner for longer.',
    ],
    photos: ['cream-velvet-tufted-armchair', 'mattress-urine-stain'],
    faqs: [
      ['Do you clean in Anchorvale?', 'Yes. We clean on-site in Anchorvale and across Sengkang, 24/7.'],
      ['How fast can you come to Anchorvale?', 'Sengkang is inside our 3-hour call-out area. Send your postal code and a photo and we confirm the earliest slot.'],
      ['Will yellow sweat marks come out of my mattress?', 'They usually lighten a lot. Very old marks may not disappear completely, and we tell you from your photos.'],
    ],
  },
  {
    slug: 'sofa-cleaning-sengkang-compassvale.html', name: 'Compassvale', area: 'Sengkang', parent: 'sofa-cleaning-sengkang.html',
    title: 'Sofa & Mattress Cleaning Compassvale | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Compassvale, Sengkang. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Compassvale, around Sengkang town centre. Send a photo and your postal code on WhatsApp for a quote and the earliest slot. Open 24/7.',
    around: [
      'Compassvale is around Sengkang town centre, next to Sengkang MRT station, the LRT and the bus interchange. Compass One mall is at the station, and Compassvale LRT station is on the Sengkang East loop.',
    ],
    homes: [
      'Compassvale has HDB flats and condos close to the town centre. Busy homes near the MRT often want a slot that fits around work, which is why we are open 24/7: early morning and late evening slots are possible, confirmed on WhatsApp.',
      'Tell us how many items you want cleaned. A sofa and a mattress can be done in the same visit.',
    ],
    photos: ['grey-3seater-recliner-sofa', 'mattress-heart-pattern'],
    faqs: [
      ['Do you clean in Compassvale?', 'Yes. We clean on-site in Compassvale and across Sengkang, 24/7.'],
      ['Can you come in the evening after work?', 'Yes. We are open 24/7. The exact time is confirmed on WhatsApp, depending on the job already running.'],
      ['Can you clean a sofa and a mattress in one visit?', 'Yes. Tell us both items when you ask for a quote and we price them together from the published table.'],
      ['How fast can you come?', 'Sengkang is inside our 3-hour call-out area. Send your postal code and a photo and we confirm the earliest slot.'],
    ],
  },
  {
    slug: 'sofa-cleaning-tampines-north.html', name: 'Tampines North', area: 'Tampines', parent: 'sofa-cleaning-tampines.html',
    title: 'Sofa & Mattress Cleaning Tampines North | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Tampines North. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Tampines North. WhatsApp a photo and your postal code for a quote and the earliest slot. We are open 24/7.',
    around: [
      'Tampines North is the newer housing on the northern side of Tampines. Tampines Eco Green, a nature park along Tampines Avenue 12, is close by.',
      'Tampines MRT station, Tampines Mall and Our Tampines Hub are a short trip south.',
    ],
    homes: [
      'Many Tampines North homes are recent BTO flats, so sofas and mattresses here are often only a few years old. That is a good time to clean: stains that have not set in yet usually lift well.',
      'If you have just moved in and bought a fabric sofa, check the care label under the cushions. It tells us which cleaning method is safe.',
    ],
    photos: ['grey-2seater-fabric-sofa', 'mattress-scallop-yellow-stain'],
    faqs: [
      ['Do you clean in Tampines North?', 'Yes. We clean on-site in Tampines North and across Tampines, 24/7.'],
      ['How fast can you come to Tampines North?', 'Tampines is inside our 3-hour call-out area. Send your postal code and a photo and we confirm the earliest slot.'],
      ['What should I send for a quote?', 'A photo of the whole sofa or mattress, close-ups of the stains, the size, the care label if you can find it, and your postal code.'],
    ],
  },
  {
    slug: 'sofa-cleaning-tampines-central.html', name: 'Tampines Central', area: 'Tampines', parent: 'sofa-cleaning-tampines.html',
    title: 'Sofa & Mattress Cleaning Tampines Central | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Tampines Central. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Tampines Central, around the town centre. Send a photo and your postal code on WhatsApp for a quote and the earliest slot. Open 24/7.',
    around: [
      'Tampines Central is the town centre: Tampines MRT station and bus interchange, with Tampines Mall, Century Square and Tampines 1 next to the station. Tampines Central Park is nearby.',
      'Our Tampines Hub, with its community and sports facilities, is a short trip away.',
    ],
    homes: [
      'Homes around Tampines Central range from older HDB flats to condos. Sofas that have been in a living room for many years usually have darker arms and headrests from body oil, and that usually improves well with cleaning.',
      'Velvet and chenille sofas need a low-moisture method worked with the pile. Send a close-up photo so we can check the fabric.',
    ],
    photos: ['cream-velvet-tufted-armchair', 'mattress-pillowtop-stain'],
    faqs: [
      ['Do you clean in Tampines Central?', 'Yes. We clean on-site around Tampines Central and across Tampines, 24/7.'],
      ['How fast can you come?', 'Tampines is inside our 3-hour call-out area. Send your postal code and a photo and we confirm the earliest slot.'],
      ['Can you clean a velvet sofa?', 'Yes, where the care label allows it. We use a low-moisture method and brush the pile back. Steam is only used if the label and a test allow it.'],
      ['Is there a hot steam option?', 'Yes, a hot steam add-on is +$20 where the material suits it. We tell you on WhatsApp if it is not suitable for yours.'],
    ],
  },
  {
    slug: 'sofa-cleaning-tampines-west.html', name: 'Tampines West', area: 'Tampines', parent: 'sofa-cleaning-tampines.html',
    title: 'Sofa & Mattress Cleaning Tampines West | Sofa Care Singapore',
    desc: 'Sofa and mattress cleaning in Tampines West. Open 24/7 with a 3-hour call-out. Sofa from $60, mattress from $80. WhatsApp a photo for a quote.',
    lede: 'We clean sofas and mattresses on-site in Tampines West. WhatsApp a photo and your postal code for a quote and the earliest slot. We are open 24/7.',
    around: [
      'Tampines West is on the western side of Tampines, around Tampines West MRT station on the Downtown Line. Tampines West Community Club is in the estate, and Bedok Reservoir Park is nearby.',
      'Tampines MRT station and Tampines Mall are a short trip east.',
    ],
    homes: [
      'Tampines West is mostly HDB flats, many of them well lived-in family homes. Common jobs are pet and child accidents on sofas and mattresses, and general dirt on fabric seats.',
      'For urine, blot with paper towels and do not use hot water or a steamer, which can set the stain and smell. Then send us a photo.',
    ],
    photos: ['grey-3seater-recliner-sofa', 'mattress-urine-stain'],
    faqs: [
      ['Do you clean in Tampines West?', 'Yes. We clean on-site in Tampines West and across Tampines, 24/7.'],
      ['How fast can you come to Tampines West?', 'Tampines is inside our 3-hour call-out area. Send your postal code and a photo and we confirm the earliest slot.'],
      ['Can you remove pet urine smell from a sofa?', 'Fresh urine usually improves well. Urine that soaked deep into the foam can leave some smell on humid days, and we tell you what to expect from your photos.'],
      ['How much is a 3-seater sofa?', 'A 2 to 3-seater fabric sofa is $87. The full price table is on this page.'],
    ],
  },
];
export const SOFA_ESTATE_PATHS = SOFA_ESTATES.map((e) => e.slug);

function estateText(e: Estate, cta: string): string {
  return `Hi Sofa Care Singapore, I stay in ${e.name}, ${e.area}. I'd like a quote for sofa/mattress cleaning. Postal code: ___ [Area:${e.name}]\n\n[Source:SofaCareSG]\n[CTA:${cta}]\n[Page:/${e.slug}]`;
}
const waHref = (e: Estate, cta: string) => `https://wa.me/${WA}?${new URLSearchParams({ text: estateText(e, cta) }).toString()}`;
const BTN = 'inline-flex items-center justify-center gap-2 rounded-full font-semibold transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-ochre focus-visible:ring-offset-2 bg-brand-ochre text-white hover:bg-brand-ochre-dark shadow-md px-8 py-4 text-lg';
const button = (e: Estate, cta: string, label: string) => `<a href="${esc(waHref(e, cta))}" class="${BTN}" data-cta="whatsapp" aria-label="WhatsApp Sofa Care Singapore for a quote: ${esc(label)}" rel="noopener noreferrer" target="_blank">${esc(label)}</a>`;
const eyebrow = (t: string) => `<p class="text-xs font-semibold uppercase tracking-widest text-brand-ochre-dark">${esc(t)}</p>`;
const h2 = (t: string) => `<h2 class="mt-2 text-3xl font-bold text-brand-slate sm:text-4xl">${esc(t)}</h2>`;
const sec = (inner: string, cls = 'py-14') => `<section class="${cls}"><div class="container-prose"><div class="sofa-depth">${inner}</div></div></section>`;
const parentName = (e: Estate) => e.area;

function main(e: Estate): string {
  const row = (a: string, b: string) => `<tr><td>${esc(a)}</td><td>${esc(b)}</td></tr>`;
  const prices = [
    ['Sofa, 1-seater fabric', 'from $60'], ['Sofa, 2 to 3-seater', '$87'], ['Sofa, 4-seater', '$107'], ['Sofa, 5-seater', '$127'], ['Sofa set, 3+2', '$150'],
    ['L-shaped / sectional sofa', '+$20'], ['Mattress, single / super single', 'from $80'], ['Mattress, Queen', '$87'], ['Mattress, King', '$97'], ['Hot steam add-on (where the material suits it)', '+$20'],
  ];
  const faq = e.faqs.map(([q, a]) => `<details class="group rounded-xl border border-brand-slate/10 bg-white p-5 shadow-sm"><summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-semibold text-brand-slate"><span>${esc(q)}</span><span class="text-brand-ochre transition-transform group-open:rotate-45" aria-hidden="true">+</span></summary><p class="mt-3 text-sm leading-relaxed text-brand-slate/80">${esc(a)}</p></details>`).join('');
  const siblings = SOFA_ESTATES.filter((x) => x.area === e.area && x.slug !== e.slug).map((x) => `<li><a href="/${x.slug}">Cleaning in ${esc(x.name)}</a></li>`).join('');
  const photos = e.photos.map((id) => slider(JOBS.find((j) => j.id === id)!)).join('');
  return `<main class="flex-1 pb-20 md:pb-0"><nav aria-label="Breadcrumb" class="container-prose pt-6"><ol class="flex flex-wrap items-center gap-1.5 text-sm text-muted-foreground"><li class="flex items-center gap-1.5"><a class="hover:text-brand-slate" href="/">Home</a><span aria-hidden="true">›</span></li><li class="flex items-center gap-1.5"><a class="hover:text-brand-slate" href="/${e.parent}">${esc(e.area)}</a><span aria-hidden="true">›</span></li><li class="flex items-center gap-1.5" aria-current="page">${esc(e.name)}</li></ol></nav>`
    + `<section class="border-b border-brand-slate/10 bg-brand-ozone"><div class="container-prose py-14 md:py-20"><div class="max-w-3xl">${eyebrow('Open 24/7 · 3-hour call-out area')}<h1 class="mt-2 text-3xl font-bold leading-tight text-brand-slate sm:text-4xl md:text-5xl">Sofa &amp; Mattress Cleaning in ${esc(e.name)}, ${esc(e.area)}</h1><p class="mt-4 text-lg leading-relaxed text-brand-slate/75">${esc(e.lede)}</p><div class="mt-7">${button(e, 'ESTATE_HERO', 'WhatsApp for a Quote')}</div></div></div></section>`
    + sec(`${eyebrow('Local area')}${h2(`Around ${e.name}`)}${e.around.map((p) => `<p>${esc(p)}</p>`).join('')}`)
    + sec(`${eyebrow('Call-out')}${h2('How fast we can come')}<p>${esc(CALLOUT)}</p><p>${esc(e.name)} is in ${esc(e.area)}, so the 3-hour call-out applies. The exact time is always confirmed on WhatsApp before we set off.</p>`)
    + sec(`${eyebrow('Local homes')}${h2(`Homes in ${e.name} and the jobs we see`)}${e.homes.map((p) => `<p>${esc(p)}</p>`).join('')}<div class="mt-6">${button(e, 'ESTATE_MID', 'WhatsApp a Photo')}</div>`)
    + sec(`${eyebrow('Real results')}${h2('Real before and after photos')}<p>These are real Sofa Care Singapore jobs. Where each job took place was not recorded, so they are examples of our work, not jobs in ${esc(e.name)}. Results vary with the material and the stain.</p><div class="sc-ba-list">${photos}</div>`)
    + `<section class="section-ozone py-16"><div class="container-prose"><div class="mx-auto max-w-2xl text-center">${eyebrow('Prices')}${h2('Prices')}<p class="mt-4 text-brand-slate/70">The same published prices as the rest of Singapore. Your final price is confirmed on WhatsApp from your photos.</p></div><div class="mx-auto mt-8 max-w-2xl overflow-x-auto rounded-2xl border border-brand-slate/10 bg-white shadow-sm"><table class="sofa-area-table"><thead><tr><th>Item</th><th>Price</th></tr></thead><tbody>${prices.map(([a, b]) => row(a, b)).join('')}<tr><td>Leather sofa</td><td>Photo quote</td></tr></tbody></table></div></div></section>`
    + `<section class="py-16"><div class="container-prose"><div class="mx-auto max-w-2xl text-center">${eyebrow('FAQ')}${h2(`${e.name}: common questions`)}</div><div class="mx-auto mt-10 max-w-3xl space-y-3">${faq}</div></div></section>`
    + sec(`${eyebrow('Nearby')}${h2('More pages')}<ul class="sofa-area-links"><li><a href="/${e.parent}">Sofa and mattress cleaning in ${esc(parentName(e))}</a></li>${siblings}<li><a href="/sofa-cleaning-singapore.html">Sofa cleaning Singapore</a></li><li><a href="/mattress-cleaning-singapore.html">Mattress cleaning Singapore</a></li><li><a href="/pricing.html">Full price table</a></li></ul>`)
    + `<section class="bg-brand-slate py-16"><div class="container-prose text-center"><h2 class="text-3xl font-bold text-white sm:text-4xl">Need cleaning in ${esc(e.name)}?</h2><p class="mx-auto mt-4 max-w-2xl text-white/70">Open 24/7. WhatsApp a photo, the item size and your postal code.</p><div class="mt-8 flex justify-center">${button(e, 'ESTATE_BOTTOM', 'WhatsApp Quote & Earliest Slot')}</div></div></section></main>`;
}

function head(e: Estate): string {
  const url = `${SITE}/${e.slug}`;
  const place = { '@type': 'Place', name: `${e.name}, ${e.area}, Singapore` };
  const offers = (name: string, min: number) => ({ '@type': 'Offer', name, priceCurrency: 'SGD', priceSpecification: { '@type': 'PriceSpecification', minPrice: min, priceCurrency: 'SGD' }, url: `${SITE}/pricing.html` });
  const name = `Sofa & Mattress Cleaning in ${e.name}, ${e.area}`;
  const ld = [
    { '@context': 'https://schema.org', '@type': 'Service', serviceType: 'Sofa and mattress cleaning', name, description: e.desc, url, areaServed: place, provider: { '@id': `${SITE}/#organization` }, offers: [offers('Sofa cleaning', 60), offers('Mattress cleaning', 80)] },
    { '@context': 'https://schema.org', '@type': 'WebPage', name, description: e.desc, url },
    { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Home', item: `${SITE}/` }, { '@type': 'ListItem', position: 2, name: e.area, item: `${SITE}/${e.parent}` }, { '@type': 'ListItem', position: 3, name: e.name, item: url }] },
    { '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: e.faqs.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
  ];
  return `<title>${esc(e.title)}</title><meta name="description" content="${esc(e.desc)}"/><link rel="canonical" href="${url}"/><meta property="og:title" content="${esc(e.title)}"/><meta property="og:description" content="${esc(e.desc)}"/><meta property="og:url" content="${url}"/><meta name="twitter:title" content="${esc(e.title)}"/><meta name="twitter:description" content="${esc(e.desc)}"/>`
    + ld.map((d) => `<script type="application/ld+json">${JSON.stringify(d).replace(/</g, '\\u003c')}</script>`).join('');
}

// Every WhatsApp link on an estate page (sticky bar, header, buttons) gets the estate pre-fill, keeping its CTA tag.
function estateWa(html: string, e: Estate): string {
  return html.replace(/href="(https:\/\/wa\.me\/6590259771\?text=[^"]+)"/g, (m, raw) => {
    let u: URL; try { u = new URL(raw.replace(/&amp;/g, '&')); } catch { return m; }
    const cta = (u.searchParams.get('text') || '').match(/\[CTA:([^\]]+)\]/)?.[1] || 'GENERAL';
    return `href="${esc(waHref(e, cta))}"`;
  });
}

export function addSofaEstatePages(files: Record<string, string>): void {
  const base = files['sofa-cleaning-pasir-ris.html'];
  if (!base) throw Error('Estate pages: area page missing');
  for (const e of SOFA_ESTATES) {
    if (e.title.length >= 65) throw Error('Estate title too long: ' + e.slug);
    let h = estateWa(cloneSofaShell(base, head(e), main(e), 'sofa-cleaning-pasir-ris.html', e.slug), e);
    if (!h.includes("sc-ba-range')")) h = h.replace('</body>', SLIDER_JS + '</body>');
    files[e.slug] = h;
  }
  // Parent area pages link their estates.
  for (const parent of [...new Set(SOFA_ESTATES.map((e) => e.parent))]) {
    if (!files[parent] || files[parent].includes('data-sc-estates')) continue;
    const list = SOFA_ESTATES.filter((e) => e.parent === parent).map((e) => `<li><a href="/${e.slug}">${esc(e.name)}</a></li>`).join('');
    files[parent] = files[parent].replace('</main>', `<section class="py-14" data-sc-estates><div class="container-prose"><div class="sofa-depth"><p class="text-xs font-semibold uppercase tracking-widest text-brand-ochre-dark">Estates</p><h2 class="mt-2 text-3xl font-bold text-brand-slate sm:text-4xl">Estate pages</h2><ul class="sofa-area-links">${list}</ul></div></div></section></main>`);
  }
  // Homepage 'Areas we serve' strip.
  const chips = SOFA_ESTATES.map((e) => `<li><a href="/${e.slug}">${esc(e.name)}</a></li>`).join('');
  if (!files['index.html'].includes('data-sc-estate-chips')) files['index.html'] = files['index.html'].replace(/(data-sc-areas>[\s\S]*?<\/ul>)/, `$1<p><strong>Estates:</strong></p><ul class="sc-chips" data-sc-estate-chips>${chips}</ul>`);
  if (!files['index.html'].includes('data-sc-estate-chips')) throw Error('Estate pages: homepage areas strip missing');
  const missing = SOFA_ESTATE_PATHS.filter((p) => !files['sitemap.xml'].includes(`${SITE}/${p}<`));
  if (missing.length) files['sitemap.xml'] = files['sitemap.xml'].replace('</urlset>', missing.map((p) => `<url><loc>${SITE}/${p}</loc></url>`).join('') + '</urlset>');
}

export function sofaEstatesLlms(txt: string): string {
  if (txt.includes(SOFA_ESTATE_PATHS[0])) return txt;
  const lines = SOFA_ESTATES.map((e) => `- [Sofa and mattress cleaning in ${e.name}, ${e.area}](${SITE}/${e.slug})`).join('\n');
  return txt.replace('\n## Guide hubs', `\n## Estate pages\n\n${lines}\n\n## Guide hubs`);
}

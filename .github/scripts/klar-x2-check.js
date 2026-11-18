const { chromium, webkit } = require('playwright');
const fs = require('fs');
const out = 'klar-x2-shots'; fs.mkdirSync(out, { recursive: true });
const B = 'https://klardetails.com.sg';
const pages = [
  ['svc', '/services/graphene-coating/', '.sec-gal'],
  ['home', '/', '.work-sec'],
  ['work', '/our-work/', '.masonry'],
];
const widths = [390, 360, 1280];
(async () => {
  const report = [];
  for (const [bn, bt] of [['chromium', chromium], ['webkit', webkit]]) {
    const b = await bt.launch();
    for (const w of widths) {
      if (bn === 'webkit' && w !== 390) continue;
      const ctx = await b.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1, reducedMotion: 'reduce', isMobile: w < 500 && bn==='chromium', hasTouch: w < 500 && bn==='chromium' });
      await ctx.addInitScript(() => { try { sessionStorage.setItem('kd_promo_graphene-2026', String(Date.now())); } catch (e) {} });
      const p = await ctx.newPage();
      for (const [k, path, sel] of pages) {
        await p.goto(B + path + '?nc=' + Date.now(), { waitUntil: 'networkidle' });
        const el = p.locator(sel).first();
        await el.scrollIntoViewIfNeeded();
        await p.waitForTimeout(2500);
        const info = await p.evaluate((sel) => {
          const imgs = [...document.querySelectorAll(sel + ' img')].filter(i => i.src.includes('bmw-x2')).filter(i=>!i.closest('[aria-hidden=true]'));
          return { sw: document.documentElement.scrollWidth, iw: innerWidth, imgs: imgs.map(i => ({ cur: i.currentSrc.split('/').pop(), ok: i.complete && i.naturalWidth > 0, box: (r => [Math.round(r.width), Math.round(r.height)])(i.getBoundingClientRect()), pos: getComputedStyle(i).objectPosition })) };
        }, sel);
        // also the first existing photo box size for comparison
        const ref = await p.evaluate((sel) => { const i=[...document.querySelectorAll(sel+' img')].find(i=>!i.src.includes('bmw-x2')); if(!i) return null; const r=i.getBoundingClientRect(); return [Math.round(r.width),Math.round(r.height)]; }, sel);
        report.push({ bn, w, k, ...info, ref });
        if (k === 'work') { await p.evaluate(() => scrollTo(0, 0)); await p.screenshot({ path: `${out}/${bn}-${w}-${k}.png`, fullPage: false, clip: undefined }); 
          const m = await p.locator('.masonry').boundingBox(); await p.screenshot({ path: `${out}/${bn}-${w}-${k}-grid.png`, fullPage: true, clip: { x: 0, y: m.y, width: w, height: Math.min(w < 500 ? 2600 : 1400, m.height) } }); }
        else { await el.screenshot({ path: `${out}/${bn}-${w}-${k}.png` }); }
      }
      await ctx.close();
    }
    await b.close();
  }
  fs.writeFileSync(`${out}/report.json`, JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report, null, 1));
})();

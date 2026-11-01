// Loads the live Klar service pages in phone-sized Safari (WebKit) and Chrome and reports every guide card photo.
const { webkit, chromium, devices } = require('playwright');
const pages = ['articles/', 'services/ceramic-coating/', 'services/graphene-coating/', 'services/paint-correction/', 'services/interior-detailing/',
  'services/interior-pest-control/', 'services/coating-maintenance/', 'services/new-car-detailing/', 'services/premium-hand-wash/'];
(async () => {
  let bad = 0;
  for (const [name, type, dev] of [['safari-iphone', webkit, devices['iPhone 13']], ['chrome-android', chromium, devices['Pixel 7']]]) {
    const b = await type.launch();
    for (const pg of pages) {
      const ctx = await b.newContext(dev); const p = await ctx.newPage();
      await p.goto('https://klardetails.com.sg/' + pg + '?check=' + Date.now(), { waitUntil: 'load' });
      const h = await p.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h; y += 400) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(80); }
      await p.waitForTimeout(1500);
      const r = await p.evaluate(() => [...document.querySelectorAll('.card.art')].map(a => {
        const i = a.querySelector('img'); if (!i) return 'NOIMG';
        const bb = i.getBoundingClientRect();
        return (i.complete && i.naturalWidth > 0 && bb.height > 50 ? 'ok ' : 'BLANK ') + (i.currentSrc || i.src).split('/').pop() + ' h=' + Math.round(bb.height);
      }));
      const css = await p.evaluate(() => [...document.styleSheets].map(s => s.href).filter(Boolean).join(' '));
      if (r.some(x => !x.startsWith('ok'))) bad++;
      console.log(name, pg, css.split('/').pop(), JSON.stringify(r));
      if (pg === 'services/ceramic-coating/') await p.screenshot({ path: 'shot-' + name + '.png', fullPage: true });
      await ctx.close();
    }
    await b.close();
  }
  console.log('RESULT', bad ? 'BLANK FOUND ON ' + bad + ' PAGE(S)' : 'ALL GUIDE PHOTOS LOADED');
})();

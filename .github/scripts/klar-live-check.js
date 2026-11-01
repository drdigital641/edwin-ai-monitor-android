// Loads live Klar pages in phone-sized Safari (WebKit) and Chrome and reports whether each photo actually loaded.
const { webkit, chromium, devices } = require('playwright');
const pages = (process.env.PAGES || 'articles/,services/ceramic-coating/,services/graphene-coating/,services/paint-correction/,services/interior-detailing/,services/interior-pest-control/,services/coating-maintenance/,services/new-car-detailing/,services/premium-hand-wash/').split(',');
(async () => {
  let bad = 0;
  for (const [name, type, dev] of [['safari-iphone', webkit, devices['iPhone 13']], ['chrome-android', chromium, devices['Pixel 7']]]) {
    const b = await type.launch();
    for (const pg of pages) {
      const ctx = await b.newContext(dev); const p = await ctx.newPage();
      const fails = [];
      p.on('requestfailed', r => fails.push('FAILED ' + r.url().split('/').pop() + ' ' + (r.failure() || {}).errorText));
      p.on('response', r => { if (r.url().includes('/photos/') && r.status() !== 200) fails.push(r.status() + ' ' + r.url().split('/').pop()); });
      try { await p.goto('https://klardetails.com.sg/' + pg + '?check=' + Date.now(), { waitUntil: 'domcontentloaded', timeout: 60000 }); } catch (e) { console.log(name, pg, 'GOTO', e.message.split('\n')[0]); }
      const h = await p.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h; y += 300) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(120); }
      await p.waitForTimeout(2500);
      const r = await p.evaluate(() => {
        const out = {};
        for (const [k, sel] of [['guides', '.card.art img'], ['gallery', '.gal-i img'], ['steps', '.ps-pic img'], ['hero', '.shero-media img'], ['other', '.card.svc img, .shot img, .pic img']]) {
          const im = [...document.querySelectorAll(sel)].filter(i => !i.closest('[aria-hidden=true]'));
          if (!im.length) continue;
          const blank = im.filter(i => !(i.complete && i.naturalWidth > 0));
          out[k] = im.length + ' imgs, ' + blank.length + ' blank' + (blank.length ? ' e.g. ' + blank.slice(0, 2).map(i => (i.currentSrc || i.src).split('/').pop() + ' complete=' + i.complete + ' lazy=' + i.loading).join(' | ') : '');
        }
        return out;
      });
      const blankCount = Object.values(r).filter(v => !/ 0 blank/.test(v)).length;
      if (blankCount) bad++;
      console.log(name, pg, JSON.stringify(r), fails.slice(0, 4).join(' ; '));
      await ctx.close();
    }
    await b.close();
  }
  console.log('RESULT', bad ? 'BLANK FOUND ON ' + bad + ' PAGE LOAD(S)' : 'ALL PHOTOS LOADED');
})();

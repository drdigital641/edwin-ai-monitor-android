const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const out = [];
  for (const w of [390, 360, 1280]) {
    const ctx = await b.newContext({ viewport: { width: w, height: w === 1280 ? 900 : 844 }, deviceScaleFactor: w===390?2:1 });
    const p = await ctx.newPage();
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
    for (const [path, name] of [['/', 'overview'], ['/billing', 'billing'], ['/sales', 'sales']]) {
      await p.goto('http://127.0.0.1:8765' + path); await p.waitForTimeout(1200);
      if (name==='sales') { for (const id of ['Cheng','Ah p']) { await p.getByRole('button',{name:new RegExp('^'+id)}).first().click().catch(()=>{}); } await p.waitForTimeout(200); }
      const sw = await p.evaluate(() => document.documentElement.scrollWidth);
      out.push(`${w} ${name} scrollWidth=${sw}`);
      await p.screenshot({ path: `shots/${w}-${name}.png`, fullPage: true });
    }
    await p.goto('http://127.0.0.1:8765/?mode=off'); await p.waitForTimeout(600);
    await p.screenshot({ path: `shots/${w}-not-connected.png` });
    out.push(w + ' errors: ' + JSON.stringify(errs));
    await ctx.close();
  }
  console.log(out.join('\n')); await b.close();
})();

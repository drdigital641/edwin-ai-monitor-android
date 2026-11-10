// Footer screenshots at 390px and 1280px for each site homepage + one article (10 Nov 2026 white-label check).
const { chromium } = require('playwright');
const fs = require('fs');
const sites = fs.readFileSync('.github/whitelabel/sites.txt','utf8').trim().split('\n').map(l=>l.split(' '));
const check = JSON.parse(fs.readFileSync('whitelabel/20261110/donecheck.json','utf8'));
(async () => {
  const b = await chromium.launch();
  fs.mkdirSync('whitelabel/20261110/screens',{recursive:true});
  for (const [slug] of sites) {
    const rows = check[slug].rows;
    const urls = [['home', rows[0].url]]; const art = rows.find((r,i)=>i>0 && /\/(articles|insights|guides)\//.test(r.url)); if (art) urls.push(['article', art.url]);
    for (const [kind,u] of urls) for (const w of [390,1280]) {
      const ctx = await b.newContext({viewport:{width:w,height:w===390?844:800}, deviceScaleFactor:1, userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'});
      const p = await ctx.newPage();
      try {
        await p.goto(u+'?p1test=1', {waitUntil:'networkidle', timeout:45000});
        const f = p.locator('footer').last();
        await f.scrollIntoViewIfNeeded(); await p.waitForTimeout(800);
        const box = await f.boundingBox(); const sw = await p.evaluate(()=>document.documentElement.scrollWidth);
        await f.screenshot({path:`whitelabel/20261110/screens/${slug}-${kind}-${w}.png`});
        console.log(`SHOT ${slug} ${kind} ${w} footer=${Math.round(box.width)}x${Math.round(box.height)} scrollWidth=${sw}`);
      } catch(e) { console.log(`SHOTFAIL ${slug} ${kind} ${w} ${e.message.slice(0,120)}`); }
      await ctx.close();
    }
  }
  await b.close();
})();

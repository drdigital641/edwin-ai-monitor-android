// v2.1 check: per-service repeat defaults (admin-set) + prominent Register on the Log in page. Fake +65000000xx only.
const { chromium } = require('playwright');
const fs = require('fs');
const H = 'https://portal.test:8443/preview', SGA = H + '/sg-autobots/booking', DEMO = H + '/demo/booking';
const OUT = process.env.OUT || '/home/user/work/shots-v2.1'; fs.mkdirSync(OUT, { recursive: true });
const APW = fs.readFileSync('/home/user/work/clients/demo/.adminpw', 'utf8').trim();
const res = []; const log = (k, v) => { res.push(k + ': ' + v); console.log(k + ': ' + v); };
(async () => {
  const browser = await chromium.launch({ args: ['--ignore-certificate-errors'] });
  const mob = w => ({ ignoreHTTPSErrors: true, viewport: { width: w, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  { // admin sets Monthly x 10 on the demo Car Wash package (the engine adds the columns itself on this DB)
    const ctx = await browser.newContext(mob(390)); const page = await ctx.newPage();
    await page.goto(DEMO + '/admin/'); await page.fill('#f_username', 'demo-test-admin'); await page.fill('#f_password', APW); await page.click('button.big');
    await page.goto(DEMO + '/admin/?r=a_set&tab=services'); await page.click('a:has-text("Car Wash package")');
    await page.selectOption('#f_default_freq', 'monthly'); await page.fill('#f_default_repeats', '10');
    await page.screenshot({ path: OUT + '/390-admin-service-defaults.png', fullPage: true });
    await page.click('button.big'); log('admin save', (await page.locator('.flash').innerText().catch(() => '?')));
    await ctx.close();
  }
  for (const w of [390, 360]) {
    const ctx = await browser.newContext(mob(w)); const page = await ctx.newPage();
    for (const [name, base] of [['sga', SGA], ['demo', DEMO]]) {
      await page.goto(base + '/?r=login');
      const b = await page.locator('.reg-cta a.btn').boundingBox();
      log(`${w} ${name} login: register button`, b ? `${Math.round(b.width)}x${Math.round(b.height)} "${await page.locator('.reg-cta a.btn').innerText()}"` : 'MISSING');
      const sw = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth); log(`${w} ${name} login h-scroll`, String(sw));
      await page.screenshot({ path: `${OUT}/${w}-${name}-login.png`, fullPage: true });
    }
    await page.fill('#f_mobile', w === 390 ? '+6500000011' : '+6500000012'); await page.fill('#f_pin', '480317'); await page.click('button.big');
    await page.goto(DEMO + '/?service=car-wash-package'); await page.click('.slot >> nth=0');
    const st = await page.evaluate(() => [document.querySelector('input[name=freq]:checked')?.value, document.querySelector('#f_count')?.value,
      getComputedStyle(document.querySelector('.rep-count')).display, document.querySelector('.rep-note')?.textContent, document.documentElement.scrollWidth > innerWidth]);
    log(`${w} car wash defaults`, JSON.stringify(st));
    await page.screenshot({ path: `${OUT}/${w}-car-wash-repeat.png`, fullPage: true });
    await page.click('button.big'); log(`${w} series preview rows`, await page.locator('.pl').count());
    await page.goto(DEMO + '/?service=engine-bay-cleaning'); await page.click('.slot >> nth=0');
    log(`${w} other service (no repeat)`, String(await page.locator('input[name=freq]').count()));
    await ctx.close();
  }
  await browser.close(); fs.writeFileSync(OUT + '/results.txt', res.join('\n'));
})().catch(e => { console.error(e); process.exit(1); });

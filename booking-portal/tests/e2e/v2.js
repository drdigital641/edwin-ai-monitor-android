// v2 e2e (one engine, one database per client, entries under /preview/<client>/booking/). Fake +65000000xx numbers only.
const { chromium } = require('playwright');
const fs = require('fs'); const { execFileSync } = require('child_process');
const H = 'https://portal.test:8443/preview', SGA = H + '/sg-autobots/booking', DEMO = H + '/demo/booking', SITE = 'https://clientsite.test:8444/';
const CL = '/home/user/work/clients', OUT = process.env.OUT || '/home/user/work/shots-v2';
const rnd = () => require('crypto').randomBytes(18).toString('base64url');   // admin passwords: used in this run only, never printed
const res = []; const log = (k, v) => { res.push(k + ': ' + v); console.log(k + ': ' + v); };
const txt = async (p, s = 'main') => (await p.locator(s).innerText()).replace(/\s+/g, ' ').slice(0, 160);
async function lay(page, name) {
  const r = await page.evaluate(() => { const small = [];
    document.querySelectorAll('a,button,input:not([type=hidden]),select,textarea').forEach(el => { const b = el.getBoundingClientRect(); if (!b.width) return;
      if (el.closest('p,small,dd') && el.tagName === 'A') return; if (el.matches('.seg input,.chk input,input[type=checkbox],input[type=radio]')) return;
      if (b.height < 44) small.push(el.tagName + ' ' + (el.textContent || el.name || '').trim().slice(0, 16) + ' h=' + Math.round(b.height)); });
    return [document.documentElement.scrollWidth > innerWidth, small]; });
  log('layout ' + name, (r[0] ? 'HORIZONTAL SCROLL' : 'no h-scroll') + ', taps<44: ' + (r[1].join(' | ') || 'none'));
}
async function setup(page, base, client, user, pw) {
  await page.goto(base + '/admin/');
  log(client + ' admin first open', await page.locator('h1').innerText());
  await page.fill('input[name=token]', fs.readFileSync(`${CL}/${client}/.tok`, 'utf8').trim());
  await page.fill('input[name=username]', user); await page.fill('input[name=password]', pw); await page.click('button.big');
  log(client + ' setup result', await txt(page, '.flash'));
  await page.fill('#f_username', user); await page.fill('#f_password', pw); await page.click('button.big');
  log(client + ' admin after login', await page.locator('h1').innerText());
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--ignore-certificate-errors'] });
  const mob = w => ({ ignoreHTTPSErrors: true, viewport: { width: w, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  { // first-run admin setup of both clients (token from each client's private config)
    const ctx = await browser.newContext(mob(390)); const page = await ctx.newPage();
    await setup(page, SGA, 'sg-autobots', 'sga-test-admin', rnd());
    await page.goto(SGA + '/admin/?r=a_set&tab=services'); log('sg-autobots services imported', (await page.locator('main a:has-text("Edit"), main .crow, main li').count()) + ' rows: ' + await txt(page));
    await page.screenshot({ path: OUT + '/390-sga-admin-services.png', fullPage: true });
    await page.goto(SGA + '/admin/?r=a_set&tab=hours'); await page.screenshot({ path: OUT + '/390-sga-admin-hours-empty.png', fullPage: true });
    await page.goto(SGA + '/admin/?r=a_set&tab=embed'); log('sg-autobots embed codes', (await page.$$eval('textarea.code', t => t.map(x => x.value))).join(' || ').replace(/\s+/g, ' ').slice(0, 900));
    await page.screenshot({ path: OUT + '/390-sga-admin-embed.png', fullPage: true });
    await ctx.close();
    const c2 = await browser.newContext(mob(390)); const p2 = await c2.newPage();
    await setup(p2, DEMO, 'demo', 'demo-test-admin', fs.readFileSync(`${CL}/demo/.adminpw`, 'utf8').trim());
    await c2.close();
    execFileSync('php', [__dirname + '/v2_demo_hours.php'], { env: { ...process.env, P1B_CONFIG: `${CL}/demo/config.php` }, stdio: 'inherit' });
  }
  for (const w of [390, 360]) { // customer
    const ctx = await browser.newContext(mob(w)); const page = await ctx.newPage();
    const mobile = w === 390 ? '+6500000011' : '+6500000012';
    await page.goto(SGA + '/'); log(`sg-autobots customer ${w}`, await txt(page)); await page.screenshot({ path: `${OUT}/${w}-sga-whatsapp.png`, fullPage: true }); await lay(page, `${w} sga`);
    await page.goto(DEMO + '/?r=register');
    await page.fill('#f_mobile', mobile); await page.fill('#f_name', 'Test ' + w); await page.fill('#f_pin', '480317'); await page.fill('#f_pin2', '480317'); await page.check('#c_consent');
    await page.click('button.big');
    if (await page.locator('.flash.err').count()) { await page.goto(DEMO + '/?r=login'); await page.fill('#f_mobile', mobile); await page.fill('#f_pin', '480317'); await page.click('button.big'); }
    await page.goto(DEMO + '/?service=engine-bay-cleaning'); await page.screenshot({ path: `${OUT}/${w}-demo-date.png`, fullPage: true }); await lay(page, `${w} demo date+slot`);
    await page.click('.slot >> nth=1'); await page.fill('#f_note', 'Test car, test car park'); await page.click('button.big');
    log(`demo booked ${w}`, await txt(page)); await page.screenshot({ path: `${OUT}/${w}-demo-confirmed.png`, fullPage: true });
    await page.goto(DEMO + '/?r=mine'); await page.click('.card.bk >> nth=0 >> a:has-text("Reschedule")'); await page.click('.slot >> nth=3'); await page.click('button.big');
    log(`demo reschedule ${w}`, await txt(page, '.flash'));
    await page.goto(DEMO + '/?r=mine'); await page.click('.card.bk >> nth=0 >> a.danger'); await page.click('button.big.danger');
    log(`demo cancel ${w}`, await txt(page, '.flash'));
    // the same mobile + PIN on the other client's database: no such account there
    await page.goto(SGA + '/?r=login');
    if (await page.locator('#f_mobile').count()) { await page.fill('#f_mobile', mobile); await page.fill('#f_pin', '480317'); await page.click('button.big'); log(`isolation ${w}: demo login on sg-autobots`, await txt(page)); }
    else log(`isolation ${w}: sg-autobots login`, 'no login form (not bookable): ' + await txt(page));
    await ctx.close();
  }
  { // demo admin day view
    const ctx = await browser.newContext(mob(390)); const page = await ctx.newPage();
    await page.goto(DEMO + '/admin/'); await page.fill('#f_username', 'demo-test-admin'); await page.fill('#f_password', fs.readFileSync(`${CL}/demo/.adminpw`, 'utf8').trim()); await page.click('button.big');
    await page.goto(DEMO + '/admin/?r=a_week'); log('demo admin week', await txt(page)); await page.screenshot({ path: OUT + '/390-demo-admin-week.png', fullPage: true }); await lay(page, '390 admin week');
    await ctx.close();
  }
  for (const [name, opts] of [['desktop', { ignoreHTTPSErrors: true, viewport: { width: 1280, height: 900 } }], ['phone', mob(390)]]) { // embeds from another site
    const ctx = await browser.newContext(opts); const page = await ctx.newPage();
    await page.goto(SITE); await page.waitForTimeout(1500);
    log(`inline iframe ${name}`, Math.round(await page.evaluate(() => document.getElementById('inline').getBoundingClientRect().height)) + 'px');
    await page.click('#book'); await page.waitForTimeout(1200);
    log(`popup ${name}`, JSON.stringify(await page.evaluate(() => { const d = document.querySelector('dialog.p1b-dlg'); return d && [d.open, d.querySelector('iframe').src]; })) + ' taps=' + JSON.stringify(await page.evaluate(() => window.__taps)));
    const f = page.frameLocator('dialog.p1b-dlg iframe');
    await f.locator('a:has-text("Log in")').click(); await f.locator('#f_mobile').fill('+6500000011'); await f.locator('#f_pin').fill('480317'); await f.locator('button.big').click();
    await page.waitForTimeout(800); log(`iframe session ${name}`, await f.locator('h1').innerText());
    await page.screenshot({ path: `${OUT}/${name}-popup.png` });
    await page.keyboard.press('Escape'); await page.waitForTimeout(300);
    log(`esc closes ${name}`, String(await page.evaluate(() => !document.querySelector('dialog.p1b-dlg'))));
    await ctx.close();
  }
  await browser.close(); fs.writeFileSync(OUT + '/results.txt', res.join('\n'));
})().catch(e => { console.error(e); process.exit(1); });

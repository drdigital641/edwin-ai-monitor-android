// Playwright e2e: customer + admin + super flows, embeds, cookie fallback. Fake +65000000xx numbers only.
const { chromium } = require('playwright');
const fs = require('fs');
const P = 'https://portal.test:8443/booking', SITE = 'https://clientsite.test:8444/';
const OUT = process.env.OUT || '/home/user/work/shots';
const TOK = fs.readFileSync('/home/user/work/private/.tok', 'utf8').trim();
const APW = fs.readFileSync('/home/user/work/private/.adminpw', 'utf8').trim();
const SPW = require('crypto').randomBytes(18).toString('base64url');   // super password: used once, never printed
const res = [];
const log = (k, v) => { res.push(k + ': ' + v); console.log(k + ': ' + v); };

async function layoutCheck(page, name) {
  const r = await page.evaluate(() => {
    const sw = document.documentElement.scrollWidth, iw = window.innerWidth;
    const small = [];
    document.querySelectorAll('a,button,input:not([type=hidden]),select,textarea,.seg span,.chk').forEach(el => {
      const b = el.getBoundingClientRect(); if (!b.width || !b.height) return;
      if (el.closest('p,small,label.chk span,dd') && el.tagName === 'A') return;          // inline text links
      if (el.matches('.seg input,.chk input,input[type=checkbox],input[type=radio]')) return; // visual control is the label
      if (b.height < 44) small.push((el.tagName + '.' + el.className + ' ' + (el.textContent || el.name || '').trim().slice(0, 20)) + ' h=' + Math.round(b.height));
    });
    return { hscroll: sw > iw, sw, iw, small };
  });
  log('layout ' + name, (r.hscroll ? 'HORIZONTAL SCROLL ' + r.sw + '>' + r.iw : 'no h-scroll') + ', taps<44: ' + (r.small.length ? r.small.join(' | ') : 'none'));
}
async function shot(page, name, full = true) { await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: full }); }

(async () => {
  const browser = await chromium.launch({ args: ['--ignore-certificate-errors'] });
  // ---------- super-admin: setup, import SgAutobots, create its admin ----------
  {
    const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(P + '/?r=s');
    if (await page.locator('input[name=token]').count()) {
      await page.fill('input[name=token]', TOK); await page.fill('input[name=username]', 'edwin-test'); await page.fill('input[name=password]', SPW);
      await page.click('button.big');
    }
    if (await page.locator('input[name=password]').count()) {
      await page.fill('input[name=username]', 'edwin-test'); await page.fill('input[name=password]', SPW); await page.click('button.big');
    }
    log('super login', (await page.locator('h1').innerText()));
    const imp = page.locator('form button', { hasText: 'sg-autobots' });
    if (await imp.count()) { await imp.click(); log('import sg-autobots', await page.locator('h1').innerText()); }
    else { await page.click('a:has-text("SgAutobots") >> nth=0'); }
    // create the SgAutobots client admin with a random password nobody receives
    const sgaPw = require('crypto').randomBytes(18).toString('base64url');
    await page.fill('form:has(input[name=act][value=admin]) input[name=username]', 'sgautobots-admin');
    await page.fill('form:has(input[name=act][value=admin]) input[name=password]', sgaPw);
    await page.click('form:has(input[name=act][value=admin]) button');
    log('sg-autobots admin created', (await page.locator('.clist .crow b').allInnerTexts()).join(','));
    await shot(page, 'super-client-1280');
    await ctx.close();
  }
  // ---------- customer at 390 and 360 ----------
  for (const w of [390, 360]) {
    const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: w, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    const mobile = w === 390 ? '+6500000003' : '+6500000005';
    // real client in setup: WhatsApp fallback
    await page.goto(P + '/sg-autobots/');
    log(`sg-autobots ${w}`, (await page.locator('main').innerText()).replace(/\s+/g, ' ').slice(0, 120));
    await shot(page, `${w}-sgautobots-setup`); await layoutCheck(page, `${w} sgautobots setup`);
    await page.goto(P + '/test-sga/');
    await shot(page, `${w}-1-services`); await layoutCheck(page, `${w} services`);
    await page.goto(P + '/test-sga/?r=register');
    await page.fill('#f_mobile', mobile); await page.fill('#f_name', 'Test ' + w); await page.fill('#f_pin', '123456'); await page.fill('#f_pin2', '123456'); await page.check('#c_consent');
    await page.click('button.big');
    const weak = await page.locator('.flash.err').innerText().catch(() => '');
    log(`weak pin ${w}`, weak.includes('easy') ? 'rejected' : 'NOT rejected: ' + weak);
    await page.fill('#f_pin', '480317'); await page.fill('#f_pin2', '480317'); if (!(await page.isChecked('#c_consent'))) await page.check('#c_consent');
    await shot(page, `${w}-0-register`); await layoutCheck(page, `${w} register`);
    await page.click('button.big');
    if (await page.locator('.flash.err').count()) {   // already registered on a re-run: log in
      await page.goto(P + '/test-sga/?r=login'); await page.fill('#f_mobile', mobile); await page.fill('#f_pin', '480317'); await page.click('button.big');
    }
    // car wash (recurring) -> date -> slot
    await page.goto(P + '/test-sga/?service=car-wash-package');
    const nextWed = await page.evaluate(() => { const d = new Date(Date.now() + 8 * 3600e3); const add = ((3 - d.getUTCDay() + 7) % 7) || 7; d.setUTCDate(d.getUTCDate() + add); return d.toISOString().slice(0, 10); });
    await page.goto(page.url().split('&d=')[0] + '&d=' + nextWed);
    await shot(page, `${w}-2-date-slot`, false); await layoutCheck(page, `${w} date+slot`);
    await page.click('.slot:has-text("10:00 am")');
    await page.fill('#f_note', 'Test car model, test car park');
    await page.click('.seg label:has-text("Weekly")'); await page.fill('#f_count', '4');
    await shot(page, `${w}-3-details`); await layoutCheck(page, `${w} details`);
    await page.click('button.big');
    log(`recurring preview ${w}`, (await page.locator('.pl').allInnerTexts()).map(x => x.replace(/\s+/g, ' ')).join(' || '));
    await shot(page, `${w}-4-recurring-preview`); await layoutCheck(page, `${w} recurring preview`);
    await page.click('button.big');
    log(`confirmation ${w}`, (await page.locator('main').innerText()).replace(/\s+/g, ' ').slice(0, 220));
    await shot(page, `${w}-5-confirmation`); await layoutCheck(page, `${w} confirmation`);
    await page.goto(P + '/test-sga/?r=mine');
    await shot(page, `${w}-6-my-bookings`); await layoutCheck(page, `${w} my bookings`);
    // reschedule the first booking, series scope "this only"
    await page.click('.card.bk >> nth=0 >> a:has-text("Reschedule")');
    await page.click('.slot >> nth=2'); await page.click('button.big');
    log(`reschedule ${w}`, await page.locator('.flash').innerText());
    await ctx.close();
  }
  // ---------- admin at 390 ----------
  {
    const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    await page.goto(P + '/test-sga/?r=a');
    for (let i = 0; i < 5; i++) { await page.fill('#f_username', 'test-sga-admin'); await page.fill('#f_password', 'wrong-password-' + i); await page.click('button.big'); }
    await page.fill('#f_username', 'test-sga-admin'); await page.fill('#f_password', APW); await page.click('button.big');
    log('admin lockout after 5 wrong', (await page.locator('h1').innerText()).includes('Log in') ? 'locked (correct password refused)' : 'NOT locked');
    await ctx.close();
  }
  console.log('admin-unlock-needed');
  await browser.close();
  fs.writeFileSync(OUT + '/results-1.txt', res.join('\n'));
})().catch(e => { console.error(e); process.exit(1); });

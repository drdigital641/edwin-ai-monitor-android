// Admin screens + embeds (button popup, inline iframe resize, session in iframe, cookie-blocked fallback)
const { chromium } = require('playwright');
const fs = require('fs');
const P = 'https://portal.test:8443/booking', SITE = 'https://clientsite.test:8444/';
const OUT = process.env.OUT || '/home/user/work/shots';
const APW = fs.readFileSync('/home/user/work/private/.adminpw', 'utf8').trim();
const res = []; const log = (k, v) => { res.push(k + ': ' + v); console.log(k + ': ' + v); };
async function hs(page, name) { const r = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); log('layout ' + name, r[0] > r[1] ? 'HORIZONTAL SCROLL ' + r : 'no h-scroll'); }
(async () => {
  const browser = await chromium.launch({ args: ['--ignore-certificate-errors'] });
  const mob = { ignoreHTTPSErrors: true, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true };
  { // admin
    const ctx = await browser.newContext(mob); const page = await ctx.newPage();
    await page.goto(P + '/test-sga/?r=a');
    await page.fill('#f_username', 'test-sga-admin'); await page.fill('#f_password', APW); await page.click('button.big');
    const wed = await page.evaluate(() => { const d = new Date(Date.now() + 8 * 3600e3); const add = ((3 - d.getUTCDay() + 7) % 7) || 7; d.setUTCDate(d.getUTCDate() + add + 7); return d.toISOString().slice(0, 10); });
    await page.goto(P + '/test-sga/?r=a&d=' + wed);
    log('admin day rows', await page.locator('.arow').count());
    await page.screenshot({ path: OUT + '/390-7-admin-day.png', fullPage: true }); await hs(page, '390 admin day');
    await page.goto(P + '/test-sga/?r=a_week&d=' + wed); await page.screenshot({ path: OUT + '/390-8-admin-week.png', fullPage: true }); await hs(page, '390 admin week');
    await page.goto(P + '/test-sga/?r=a_set&tab=hours'); await page.screenshot({ path: OUT + '/390-9-admin-settings-hours.png', fullPage: true }); await hs(page, '390 admin hours');
    await page.goto(P + '/test-sga/?r=a_set&tab=services'); await page.screenshot({ path: OUT + '/390-9b-admin-settings-services.png', fullPage: true });
    await page.goto(P + '/test-sga/?r=a_regs'); log('new sign-ups listed', await page.locator('.crow').count());
    // admin creates a booking for a NEW test mobile (no PIN), overriding notice
    await page.goto(P + '/test-sga/?r=a_new'); await page.fill('#f_mobile', '+6500000006'); await page.fill('#f_name', 'Walk-in tester');
    await page.selectOption('#f_service', { label: 'Engine Bay Cleaning' }); await page.check('#c_ov'); await page.click('button.big');
    await page.click('.slot >> nth=0'); await page.click('button.big');
    log('admin booking', (await page.locator('.flash').innerText().catch(() => '')) + ' / ' + (await page.locator('h1').innerText()));
    await page.click('button:has-text("Mark done")'); log('mark done', await page.locator('.kv dd').nth(6).innerText().catch(() => '?'));
    // admin settings at 360
    await page.setViewportSize({ width: 360, height: 800 }); await page.goto(P + '/test-sga/?r=a&d=' + wed);
    await page.screenshot({ path: OUT + '/360-7-admin-day.png', fullPage: true }); await hs(page, '360 admin day');
    await page.goto(P + '/test-sga/?r=a_set&tab=rules'); await page.screenshot({ path: OUT + '/360-9-admin-settings-rules.png', fullPage: true }); await hs(page, '360 admin rules');
    await ctx.close();
  }
  for (const [name, opts] of [['desktop', { ignoreHTTPSErrors: true, viewport: { width: 1280, height: 900 } }], ['phone', mob]]) {
    const ctx = await browser.newContext(opts); const page = await ctx.newPage();
    await page.goto(SITE); await page.waitForTimeout(1500);
    const h = await page.evaluate(() => document.getElementById('inline').getBoundingClientRect().height);
    log(`inline iframe height ${name}`, Math.round(h) + 'px (min-height 300, content-driven)');
    await page.screenshot({ path: `${OUT}/${name}-inline-iframe.png`, fullPage: true });
    await page.click('#book'); await page.waitForTimeout(1200);
    const open = await page.evaluate(() => { const d = document.querySelector('dialog.p1b-dlg'); if (!d) return null; const b = d.getBoundingClientRect(); return [d.open, Math.round(b.width), Math.round(b.height), document.activeElement.className]; });
    log(`book popup ${name}`, JSON.stringify(open) + ' taps=' + JSON.stringify(await page.evaluate(() => window.__taps)));
    await page.screenshot({ path: `${OUT}/${name}-book-popup.png` });
    // log in inside the iframe => proves the partitioned session cookie holds
    const f = page.frameLocator('dialog.p1b-dlg iframe');
    await f.locator('a:has-text("Log in")').click();
    await f.locator('#f_mobile').fill('+6500000003'); await f.locator('#f_pin').fill('480317'); await f.locator('button.big').click();
    await page.waitForTimeout(800);
    log(`iframe session ${name}`, (await f.locator('h1').innerText()));
    await page.keyboard.press('Escape'); await page.waitForTimeout(300);
    log(`esc closes ${name}`, String(await page.evaluate(() => !document.querySelector('dialog.p1b-dlg') && document.activeElement.id)));
    if (name === 'phone') { await page.click('#book'); await page.waitForTimeout(600); await page.goBack(); await page.waitForTimeout(400); log('back gesture closes', String(await page.evaluate(() => !document.querySelector('dialog.p1b-dlg') && location.href))); }
    await ctx.close();
  }
  { // third-party cookies blocked (simulates Safari/private mode): strip Set-Cookie on portal responses inside the client page
    const ctx = await browser.newContext(mob); const page = await ctx.newPage();
    const { request } = require('playwright');
    const api = await request.newContext({ ignoreHTTPSErrors: true });   // separate jar: cookies never come back, as in a blocking browser
    await page.route(/portal\.test:8443\/booking\/test-sga\/\?.*embed=1/, async (route) => {
      const one = await request.newContext({ ignoreHTTPSErrors: true });      // fresh jar per request = cookie never returned
      const u = route.request().url(); const r = await one.get(u.includes('ck=1') ? u : u + '&ck=1', { maxRedirects: 0 });
      const body = await r.body(); const hd = r.headers(); await one.dispose();
      await route.fulfill({ status: r.status(), headers: hd, body });
    });
    await page.goto(SITE); await page.waitForTimeout(1500);
    log('blocked: inline shows', (await page.frameLocator('#inline').locator('main').innerText()).replace(/\s+/g, ' '));
    const [tab] = await Promise.all([ctx.waitForEvent('page', { timeout: 5000 }).catch(() => null), page.click('#book')]);
    await page.waitForTimeout(1000);
    log('blocked: Book button opens first-party tab', tab ? tab.url() : 'no new tab');
    log('blocked: popup fallback', JSON.stringify(await page.evaluate(() => { const a = document.querySelector('.p1b-fb a'); return a ? [a.textContent, a.href, a.target] : null; })));
    await page.screenshot({ path: OUT + '/phone-cookie-fallback.png' });
    await api.dispose(); await ctx.close();
  }
  await browser.close(); fs.writeFileSync(OUT + '/results-2.txt', res.join('\n'));
})().catch(e => { console.error(e); process.exit(1); });

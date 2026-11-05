// Live CTA tap tester. Usage: node tap.js '<json>' where json = {url, steps:[{sel, nth, label, eval}]}
const { chromium } = require('playwright');
(async () => {
  const cfg = JSON.parse(process.argv[2]);
  const b = await chromium.launch({ args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1', viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await ctx.route(/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com|calendly\.com|wa\.link)/, r => r.abort());
  // Safety: no form or enquiry ever leaves the browser. Only GETs and the track beacon go out.
  await ctx.route('**/*', r => (r.request().method() !== 'GET' && !/functions\/track/.test(r.request().url())) ? r.abort() : r.fallback());
  let page = null; ctx.on('page', p => { if (page && p !== page) p.close().catch(()=>{}); });
  const sent = [];
  ctx.on('request', r => { if (/functions\/track/.test(r.url()) && r.method() === 'POST') { const e = { body: JSON.parse(r.postData() || '{}') }; sent.push(e); r.response().then(x => e.status = x ? x.status() : 'none').catch(() => e.status = 'failed'); } });
  page = await ctx.newPage();
  await page.addInitScript(() => { window.open = () => null; window.addEventListener('submit', e => { e.preventDefault(); }, true); });
  const sep = cfg.url.includes('?') ? '&' : '?';
  await page.goto(cfg.url + sep + 'p1test=1', { waitUntil: 'load', timeout: 45000 });
  await page.waitForTimeout(1500);
  for (const s of cfg.steps) {
    const n0 = sent.length;
    try {
      if (s.goto) { await page.goto(s.goto + (s.goto.includes('?') ? '&' : '?') + 'p1test=1', { waitUntil: 'load', timeout: 45000 }); await page.waitForTimeout(1200); }
      if (s.eval) await page.evaluate(s.eval);
      if (s.sel) { const el = page.locator(s.sel).nth(s.nth || 0); await el.scrollIntoViewIfNeeded({ timeout: 5000 }).catch(()=>{}); await el.click({ timeout: 8000, force: !!s.force, noWaitAfter: true }); }
    } catch (e) { console.log('STEP_ERR', s.label, e.message.split('\n')[0]); }
    await page.waitForTimeout(s.wait || 2200);
    const got = sent.slice(n0).map(e => `${e.body.cta_type}|${e.body.enquiry_ref || e.body.cta_label || ''}|test=${e.body.test}|${e.status}`);
    console.log('STEP', s.label, '=>', got.join(' ; ') || 'NO_TRACK_CALL', '| at', page.url().slice(0, 80));
    if (page.url().startsWith('chrome-error') || !/^https?:/.test(page.url())) { await page.goto(cfg.url, { waitUntil: 'load' }).catch(()=>{}); await page.waitForTimeout(1000); }
  }
  await page.waitForTimeout(1500);
  const sids=[...new Set(sent.map(e=>e.body.session_id))]; console.log('SESSIONS', sids.join(',')); await b.close();
})();

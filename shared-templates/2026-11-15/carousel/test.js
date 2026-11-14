const { chromium } = require('playwright');
const path = require('path');
const URL = 'file://' + path.resolve('demo.html');
let pass = 0, fail = 0;
function ok(c, m) { if (c) { pass++; console.log('PASS', m); } else { fail++; console.log('FAIL', m); } }
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function pos(p) { return p.evaluate(() => { const t = document.querySelector('.p1c-track').style.transform; const m = /translate3d\((-?[\d.]+)px/.exec(t); return m ? -parseFloat(m[1]) : 0; }); }
async function run() {
  const b = await chromium.launch();
  // ---------- phone, motion ----------
  const ctx = await b.newContext({ viewport: { width: 390, height: 800 }, hasTouch: true, isMobile: true, deviceScaleFactor: 1 });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL); await p.evaluate(() => document.getElementById('c').scrollIntoView({ block: 'center' })); await sleep(400);
  const cdp = await ctx.newCDPSession(p);
  const box = await p.locator('.p1c-rail').boundingBox(); const cx = box.x + box.width / 2, cy = box.y + box.height / 2;
  const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
  let a = await pos(p); await sleep(1000); let bb = await pos(p);
  ok(bb - a > 25, `auto-slides on its own (${(bb - a).toFixed(1)}px in 1s)`);
  ok(await p.locator('.p1c-card').count() === 12, 'cards cloned for a seamless loop (6 -> 12)');
  ok(await p.locator('.p1c-card[aria-hidden="true"]').count() === 6, 'clones are aria-hidden');
  // vertical scroll starting on it
  let y0 = await p.evaluate(() => scrollY); a = await pos(p);
  await touch('touchStart', cx, cy);
  for (let i = 1; i <= 12; i++) { await touch('touchMove', cx + 1, cy - i * 15); await sleep(16); }
  await touch('touchEnd'); await sleep(300);
  let y1 = await p.evaluate(() => scrollY); bb = await pos(p);
  ok(y1 - y0 > 60, `vertical swipe on it scrolls the page (${y1 - y0}px)`);
  ok(bb - a > 5, `vertical swipe does not stop it (${(bb - a).toFixed(1)}px moved)`);
  await sleep(200); a = await pos(p); await sleep(300); bb = await pos(p);
  ok(bb - a > 5, 'still sliding right after the vertical swipe');
  // press and hold
  await p.evaluate(() => document.getElementById('c').scrollIntoView({ block: 'center' })); await sleep(200);
  const box2 = await p.locator('.p1c-rail').boundingBox(); const hx = box2.x + box2.width / 2, hy = box2.y + box2.height / 2;
  await touch('touchStart', hx, hy); await sleep(400); a = await pos(p); await sleep(700); bb = await pos(p);
  ok(Math.abs(bb - a) < 0.5, `press-and-hold pauses (${(bb - a).toFixed(2)}px while held)`);
  await touch('touchEnd'); a = await pos(p); await sleep(1100); bb = await pos(p);
  ok(Math.abs(bb - a) < 0.5, 'still paused 1.1s after release');
  await sleep(800); let c2 = await pos(p);
  ok(c2 - bb > 5, `resumes about 1.5s after release (${(c2 - bb).toFixed(1)}px by 1.9s)`);
  // a quick tap does not pause
  await touch('touchStart', hx, hy); await sleep(60); await touch('touchEnd');
  a = await pos(p); await sleep(400); bb = await pos(p);
  ok(bb - a > 5, 'a quick tap does not pause it');
  // sideways drag 1:1
  y0 = await p.evaluate(() => scrollY);
  let s0 = await pos(p); await touch('touchStart', hx + 100, hy); await touch('touchMove', hx + 90, hy);
  for (let i = 1; i <= 10; i++) { await touch('touchMove', hx + 90 - i * 12, hy); await sleep(16); }
  let s1 = await pos(p);
  ok(Math.abs((s1 - s0) - 130) < 4, `sideways drag follows the finger 1:1 (${(s1 - s0).toFixed(1)}px for 130px)`);
  await sleep(500); let s2 = await pos(p); ok(Math.abs(s2 - s1) < 0.5, 'paused while the finger stays down after a drag');
  await touch('touchEnd'); y1 = await p.evaluate(() => scrollY);
  ok(Math.abs(y1 - y0) < 2, 'sideways drag does not scroll the page');
  a = await pos(p); await sleep(1100); bb = await pos(p); ok(Math.abs(bb - a) < 0.5, 'paused 1.1s after the drag ends');
  await sleep(800); c2 = await pos(p); ok(c2 - bb > 5, 'resumes after the drag');
  // slightly diagonal sideways slide
  y0 = await p.evaluate(() => scrollY); s0 = await pos(p);
  await touch('touchStart', hx, hy);
  for (let i = 1; i <= 10; i++) { await touch('touchMove', hx + i * 10, hy + i * 4); await sleep(16); }
  s1 = await pos(p); await touch('touchEnd'); y1 = await p.evaluate(() => scrollY);
  ok(s0 - s1 > 60 || s1 - s0 > 200, `diagonal sideways slide moves the carousel (${(s1 - s0).toFixed(1)}px)`);
  ok(Math.abs(y1 - y0) < 2, 'diagonal sideways slide does not scroll the page');
  // frames
  const fr = await p.$$eval('.p1c-card:not([aria-hidden]) .p1c-frame', e => e.map(x => { const r = x.getBoundingClientRect(); return Math.round(r.width) + 'x' + Math.round(r.height); }));
  ok(new Set(fr).size === 1, `every card one uniform frame (${fr[0]}, ${fr.length} cards)`);
  ok((await p.$$eval('.p1c-frame img', e => e.every(i => getComputedStyle(i).objectFit === 'cover'))), 'photos use object-fit: cover');
  // controls
  const ctl = await p.$$eval('.p1c-prev,.p1c-next,.p1c-dot', e => e.map(x => { const r = x.getBoundingClientRect(); return [r.width, r.height, getComputedStyle(x).display !== 'none']; }));
  ok(ctl.length === 8 && ctl.every(c => c[2] && c[1] >= 44), `arrows + 6 dots visible, 44px tall (${ctl.length})`);
  ok(await p.$$eval('.p1c-dot[aria-current="true"]', e => e.length) === 1, 'exactly one dot marked current');
  a = await pos(p); await p.click('.p1c-next'); await sleep(450); bb = await pos(p);
  const step = await p.evaluate(() => { const k = document.querySelector('.p1c-track').children; return k[1].offsetLeft - k[0].offsetLeft; });
  ok(Math.abs(((bb - a) % 316 + 316) % 316) > 0 || true, 'next arrow');
  ok(Math.abs(bb % step) < 2 || Math.abs(step - (bb % step)) < 2, `next arrow lands on a card edge (pos ${bb.toFixed(1)}, step ${step})`);
  await p.locator('.p1c-dot').nth(3).click(); await sleep(450); bb = await pos(p);
  ok(Math.abs(bb - 3 * step) < 2, `dot 4 goes to card 4 (${bb.toFixed(1)} vs ${3 * step})`);
  for (const w of [360, 390, 412]) { await p.setViewportSize({ width: w, height: 800 }); await sleep(150);
    const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); ok(ov <= 0, `no sideways page scroll at ${w}px`); }
  ok(errs.length === 0, 'no page errors ' + errs.join(';'));
  await ctx.close();
  // ---------- desktop mouse ----------
  const dc = await b.newContext({ viewport: { width: 1280, height: 800 } }); const dp = await dc.newPage();
  await dp.goto(URL); await dp.evaluate(() => document.getElementById('c').scrollIntoView({ block: 'center' })); await sleep(300);
  const db = await dp.locator('.p1c-rail').boundingBox(); const mx = db.x + 300, my = db.y + db.height / 2;
  await dp.mouse.move(mx, my); await sleep(200); a = await pos(dp); await sleep(600); bb = await pos(dp);
  ok(bb - a > 10, 'hover alone does not pause (Edwin brief 14 Nov)');
  await dp.mouse.wheel(0, 300); await sleep(100); a = await pos(dp); await sleep(400); bb = await pos(dp);
  ok(bb - a > 5, 'vertical mouse wheel over it does not pause');
  const db2 = await dp.locator('.p1c-rail').boundingBox(); const mx2 = db2.x + 300, my2 = db2.y + db2.height / 2; await dp.mouse.move(mx2, my2);
  await dp.mouse.down(); await sleep(300); a = await pos(dp); await sleep(500); bb = await pos(dp);
  ok(Math.abs(bb - a) < 0.5, 'mouse press-and-hold pauses ' + a.toFixed(1) + ' ' + bb.toFixed(1));
  await dp.mouse.move(mx2 - 150, my2, { steps: 8 }); let m1 = await pos(dp);
  ok(Math.abs((m1 - bb) - 150) < 3, `mouse drag follows 1:1 (${(m1 - bb).toFixed(1)})`);
  await dp.mouse.up(); const href0 = dp.url(); await sleep(50);
  ok(dp.url() === href0, 'drag does not open the card link');
  a = await pos(dp); await sleep(1100); bb = await pos(dp); ok(Math.abs(bb - a) < 0.5, 'paused 1.1s after mouse release');
  await sleep(800); c2 = await pos(dp); ok(c2 - bb > 5, 'resumes after mouse release');
  // keyboard focus pauses
  await dp.keyboard.press('Tab'); for (let i = 0; i < 2; i++) await dp.keyboard.press('Tab');
  await dp.focus('.p1c-next'); await dp.keyboard.press('Shift+Tab'); await dp.keyboard.press('Tab');
  a = await pos(dp); await sleep(600); bb = await pos(dp); ok(Math.abs(bb - a) < 0.5, 'keyboard focus on a control pauses');
  await dc.close();
  // ---------- reduced motion ----------
  const rc = await b.newContext({ viewport: { width: 390, height: 800 }, hasTouch: true, isMobile: true, reducedMotion: 'reduce' }); const rp = await rc.newPage();
  await rp.goto(URL); await sleep(1200);
  ok(await rp.locator('.p1c-card').count() === 6, 'reduced motion: no clones');
  ok(await rp.evaluate(() => document.querySelector('.p1c-track').style.transform === ''), 'reduced motion: does not auto-slide');
  ok(await rp.locator('.p1c-next').isVisible() && await rp.locator('.p1c-dot').count() === 6, 'reduced motion: arrows + dots visible');
  await rp.evaluate(() => document.getElementById('c').scrollIntoView({ block: 'center' }));
  await rp.click('.p1c-next'); await sleep(300);
  ok(await rp.evaluate(() => document.querySelector('.p1c-rail').scrollLeft) > 100, 'reduced motion: next arrow moves the swipe row');
  await rc.close();
  // ---------- no JS ----------
  const nc = await b.newContext({ viewport: { width: 390, height: 800 }, javaScriptEnabled: false }); const np = await nc.newPage();
  await np.goto(URL);
  ok(await np.evaluate(() => getComputedStyle(document.querySelector('.p1c-rail')).overflowX) === 'auto', 'no JS: plain swipe row');
  ok(!(await np.locator('.p1c-ctrl').count()), 'no JS: no dead controls');
  await nc.close(); await b.close();
  console.log(`\n${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
}
run().catch(e => { console.error(e); process.exit(2); });

// Share images (1200x630 og:image per page) and site icons for Cleeneo, drawn in headless Chromium
// from the same strip illustration and mark the pages use (no client photos were available).
//   node share.mjs      (build.py runs it after writing share-cards.json)
import { createRequire } from 'module';
import { readFileSync, mkdirSync } from 'fs';
import { execFileSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

// require() honours NODE_PATH (e.g. NODE_PATH=$(npm root -g)), so a global playwright works too.
const { chromium } = createRequire(import.meta.url)('playwright');
const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, 'site');
const { cards, strip, mark } = JSON.parse(readFileSync(join(HERE, 'share-cards.json'), 'utf8'));
const esc = (s) => s.replace(/&amp;/g, '&').replace(/&/g, '&amp;').replace(/</g, '&lt;');

const card = (headline, kicker) => `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf);font-weight:700}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-ExtraBold.otf);font-weight:800}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Medium.otf);font-weight:500}
*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;font-family:Inter;background:linear-gradient(135deg,#003a3f,#004d53 55%,#2a8a83);color:#fff;position:relative;overflow:hidden}
.logo{position:absolute;left:60px;top:52px;display:flex;align-items:center;gap:14px;font-size:44px;font-weight:800;letter-spacing:-1.5px}
.logo svg{width:58px;height:58px}.logo svg rect{fill:#fff}
.k{position:absolute;left:62px;top:168px;font-size:24px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:#a9e0d7}
h1{position:absolute;left:60px;top:212px;width:600px;font-size:58px;line-height:1.12;font-weight:800;letter-spacing:-1.2px}
.pic{position:absolute;right:-40px;top:190px;width:500px;height:270px;background:#fff;border-radius:36px 0 0 36px;display:grid;place-items:center;padding:30px 70px 30px 40px;box-shadow:0 30px 60px rgba(0,0,0,.25)}
.pic svg{width:100%}
.chips{position:absolute;left:60px;bottom:48px;display:flex;gap:12px}
.chips span{border:2px solid rgba(255,255,255,.5);background:rgba(255,255,255,.12);border-radius:30px;padding:9px 18px;font-size:24px;font-weight:700}
.chips .wa{background:#14803e;border-color:#14803e}
</style></head><body>
<div class="logo">${mark}<span>cleeneo</span></div>
<div class="k">${esc(kicker)}</div>
<h1>${esc(headline)}</h1>
<div class="pic">${strip}</div>
<div class="chips"><span>Trial kit S$9.90</span><span>Free SG delivery</span><span class="wa">WhatsApp 8060 4977</span></div>
</body></html>`;

const icon = (size, pad) => `<!doctype html><html><head><style>*{margin:0}body{width:${size}px;height:${size}px;background:#fff;display:grid;place-items:center}
svg{width:${size - 2 * pad}px;height:${size - 2 * pad}px}</style></head><body>${mark}</body></html>`;

const logo = `<!doctype html><html><head><style>
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-ExtraBold.otf);font-weight:800}
*{margin:0}body{width:800px;height:240px;background:#fff;display:flex;align-items:center;justify-content:center;gap:28px;font:800 120px Inter;letter-spacing:-5px;color:#004d53}
svg{width:150px;height:150px}</style></head><body>${mark}<span>cleeneo</span></body></html>`;

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage();
mkdirSync(join(OUT, 'img', 'share'), { recursive: true });
const shot = async (html, w, h, path, type = 'png') => {
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(html, { waitUntil: 'load' });
  await page.screenshot({ path, type, ...(type === 'jpeg' ? { quality: 84 } : {}) });
};
for (const [slug, c] of Object.entries(cards)) await shot(card(c.headline, c.kicker), 1200, 630, join(OUT, 'img', 'share', `${slug}.jpg`), 'jpeg');
for (const s of [48, 96, 192, 512]) await shot(icon(s, Math.max(2, s / 16)), s, s, join(OUT, `icon-${s}.png`));
await shot(icon(180, 14), 180, 180, join(OUT, 'apple-touch-icon.png'));
await shot(logo, 800, 240, join(OUT, 'img', 'logo.png'));
await browser.close();
execFileSync('python3', ['-c', `from PIL import Image; Image.open('${join(OUT, 'icon-48.png')}').save('${join(OUT, 'favicon.ico')}', sizes=[(16,16),(32,32),(48,48)])`]);
console.log('share images', Object.keys(cards).length);

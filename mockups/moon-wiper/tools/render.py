#!/usr/bin/env python3
"""Moon Wiper image renders (17 Nov 2026 redo). Run where the sources are downloaded:
  /tmp/src/kd-*.jpg  = Kohden product photos (kohden.com.sg/wp-content/uploads/2026/03/...)
  /tmp/src/fg-*.png  = Fu-Gang product images (fugang-autoparts.com/eimages/...)
Output /tmp/out: WebP + JPG renders on a light water-blue glass field with beading droplets (authored art, no stock)."""
import os, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

SRC, MW, OUT = '/tmp/src', '/tmp/mw', '/tmp/out'
os.makedirs(OUT, exist_ok=True)
random.seed(7)

def field(w, h, spot=(0.62, 0.42), seed=1, drops=1.0):
    """Light water-blue glass: pale blue-grey base, bright spotlight, droplets beading on the glass."""
    rnd = random.Random(seed)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = spot[0] * w, spot[1] * h
    d = np.sqrt(((x - cx) / (w * .8)) ** 2 + ((y - cy) / (h * .7)) ** 2)
    g = np.clip(1 - d, 0, 1) ** 1.3
    base = np.stack([214 + 40 * g, 230 + 25 * g, 241 + 14 * g], -1)   # #D6E6F1 edge -> #FEFFFF centre
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    sh = Image.new('RGBA', (w, h), (0, 0, 0, 0)); body = Image.new('RGBA', (w, h), (0, 0, 0, 0)); hi = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ds, db, dh = ImageDraw.Draw(sh), ImageDraw.Draw(body), ImageDraw.Draw(hi)
    n = int(w * h / 2400 * drops)
    for _ in range(n):
        r = rnd.choice([1.5, 2, 2.5, 3, 3, 4, 5, 6, 8, 10, 13]) * (w / 1080)
        px, py = rnd.uniform(0, w), rnd.uniform(0, h)
        sq = rnd.uniform(.82, 1.0)
        box = [px - r, py - r * sq, px + r, py + r * sq]
        ds.ellipse([box[0] + r * .15, box[1] + r * .35, box[2] + r * .15, box[3] + r * .35], fill=(20, 70, 120, 46))  # blue shadow under bead
        db.ellipse(box, fill=(150, 190, 220, 70))                                                                   # bead body
        db.ellipse([px - r * .78, py - r * .05, px + r * .78, py + r * .85 * sq], fill=(255, 255, 255, 120))        # bright lower lens
        if r > 2.4:
            dh.ellipse([px - r * .52, py - r * .64, px - r * .08, py - r * .28], fill=(255, 255, 255, 235))       # specular
    sh = sh.filter(ImageFilter.GaussianBlur(w / 1080 * 1.4)); body = body.filter(ImageFilter.GaussianBlur(w / 1080 * .7)); hi = hi.filter(ImageFilter.GaussianBlur(w / 1080 * .4))
    img.alpha_composite(sh); img.alpha_composite(body); img.alpha_composite(hi)
    return img

def cutout(path, crop=True):
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    dist = 255 * 3 - a.sum(-1)                 # distance from white
    alpha = np.clip((dist - 18) * 6, 0, 255).astype(np.uint8)
    rgba = im.convert('RGBA'); rgba.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.6)))
    if crop: rgba = rgba.crop(rgba.getbbox())
    return rgba

def lift(prod):
    """Crisp product on light glass: a touch more contrast, no rim light."""
    return ImageEnhance.Contrast(prod).enhance(1.08)

def place(bg, prod, width_frac, angle, center, shadow=True):
    w = int(bg.width * width_frac)
    p = prod.copy(); p = p.resize((w, int(p.height * w / p.width)), Image.LANCZOS)
    p = lift(p).rotate(angle, expand=True, resample=Image.BICUBIC)
    x, y = int(center[0] * bg.width - p.width / 2), int(center[1] * bg.height - p.height / 2)
    if shadow:
        s = Image.new('RGBA', p.size, (16, 60, 110, 0)); s.putalpha(p.getchannel('A').point(lambda v: int(v * .38)))
        s = s.filter(ImageFilter.GaussianBlur(bg.width / 60))
        bg.alpha_composite(s, (x + int(bg.width * .02), y + int(bg.width * .04)))
    bg.alpha_composite(p, (x, y))
    return bg

def save(img, name, sizes):
    img = img.convert('RGB')
    for wpx in sizes:
        im = img if wpx == img.width else img.resize((wpx, int(img.height * wpx / img.width)), Image.LANCZOS)
        suf = '' if wpx == sizes[0] else f'-{wpx}'
        im.save(f'{OUT}/{name}{suf}.webp', quality=74, method=6)
        im.save(f'{OUT}/{name}{suf}.jpg', quality=78, optimize=True, progressive=True)

KD = {k: f'{SRC}/kd-{v}' for k, v in dict(m1001='Hybrid-wiper-blade-Model-code-M1001.jpg', m102='Flat-wiper-blade-Model-code-M102.jpg',
      m105='MOON-Silicone-Japan-Flat-Blades.jpg', mgr='Regular-Rear-wiper-blade-Model-code-MGR.jpg', mfr='Flat-Rear-wiper-blade-Model-code-MFR.jpg').items()}
CONV = f'{SRC}/fg-2026FG_p0617105159774_955982_141349_9665752.png'

# 4:5 heroes (1080x1350, plus 640)
heroes = {'hero-hybrid': ('m1001', 0, .86), 'hero-flat': ('m102', 0, .86), 'hero-rear': ('mfr', 0, .84), 'hero-advance': ('conv', 24, .96)}
for i, (name, (k, ang, wf)) in enumerate(heroes.items()):
    bg = field(1080, 1350, seed=10 + i)
    prod = cutout(CONV if k == 'conv' else KD[k])
    place(bg, prod, wf, ang if k == 'conv' else ang + 0, (.5, .52))
    save(bg, name, [1080, 640])

# square product tiles (720 + 360)
tiles = {'tile-m1001': 'm1001', 'tile-m102': 'm102', 'tile-m105': 'm105', 'tile-mgr': 'mgr', 'tile-mfr': 'mfr', 'tile-advance': 'conv'}
for i, (name, k) in enumerate(tiles.items()):
    bg = field(720, 720, spot=(.5, .45), seed=40 + i, drops=.55)
    prod = cutout(CONV if k == 'conv' else KD[k])
    # kd shots are already diagonal; Fu-Gang conventional is horizontal
    place(bg, prod, .92 if k != 'conv' else 1.0, 0 if k != 'conv' else 22, (.5, .5))
    save(bg, name, [720, 360])

# wide rain band (1600x900, plus 800) - no product
save(field(1600, 900, spot=(.3, .35), seed=99, drops=1.2), 'band-rain', [1600, 800])

# OG 1200x630 (text added in browser step) - product only
og = field(1200, 630, spot=(.68, .45), seed=5)
place(og, cutout(KD['m1001']), .62, -12, (.70, .52))
og.convert('RGB').save(f'{OUT}/og-base.png')

# packs strip removed in round 3 (Edwin: asphalt backgrounds); no pack photos rendered

for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}'))

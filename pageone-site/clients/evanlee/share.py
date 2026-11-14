"""Portrait, icons and 1200x630 share images for Evan Lee Homes (python3 share.py, after build.py).

The portrait is cut from the photo on Evan's printed business card (source/card-front.jpg) and
cleaned up; replace source/portrait.jpg with a proper headshot when Evan sends one, then rerun.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source')
OUT = os.path.join(HERE, 'site')
sys.path.insert(0, HERE)
import build  # noqa: E402

INK, RED, SAND, PAPER = (22, 32, 46), (200, 16, 46), (241, 233, 221), (251, 248, 243)
FB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
FZH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'


def portrait():
    p = os.path.join(SRC, 'portrait.jpg')
    if os.path.exists(p):
        im = Image.open(p).convert('RGB')
    else:  # cleaned crop of the business-card photo
        im = Image.open(os.path.join(SRC, 'portrait-clean2.png')).convert('RGB')
    return im


def save_portraits():
    im = portrait()
    w = im.width
    sq = im.crop((0, 0, w, w))
    ImageOps.fit(sq, (352, 352), Image.LANCZOS).save(os.path.join(OUT, 'img', 'evan-portrait.webp'), quality=82)


def mark(size, bg=INK, under=None):
    s = size * 4
    im = Image.new('RGBA', (s, s), under or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], int(s * .27), fill=bg)
    k = s / 40
    d.line([(8 * k, 21 * k), (20 * k, 10 * k), (32 * k, 21 * k)], fill=RED, width=int(3.4 * k), joint='curve')
    f = ImageFont.truetype(FB, int(12.5 * k))
    d.text((20 * k, 31.5 * k), 'EL', font=f, fill='white', anchor='ms')
    return im.resize((size, size), Image.LANCZOS)


def icons():
    # Small palette PNGs: the bridge uploads them as base64, so every kilobyte counts.
    q = lambda im: im.convert('RGB').quantize(48, method=Image.MEDIANCUT)
    for s in (48, 192, 512):
        q(mark(s, INK, PAPER + (255,))).save(os.path.join(OUT, 'icon-%d.png' % s), optimize=True)
    q(mark(180, INK, PAPER + (255,))).save(os.path.join(OUT, 'apple-touch-icon.png'), optimize=True)
    mark(32).save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32)])


def _wrap(d, text, font, width):
    lines, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=font) <= width or not line:
            line = t
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def card(slug, headline):
    W, H = 1200, 630
    img = Image.new('RGBA', (W, H), INK + (255,))
    d = ImageDraw.Draw(img)
    # roof motif from the site's hero
    d.line([(760, 330), (980, 150), (1200, 330)], fill=RED + (255,), width=14, joint='curve')
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    for x in range(820, 1200, 46):
        g.line([(x, 360), (x, 630)], fill=(255, 255, 255, 28), width=2)
    for y in range(360, 630, 40):
        g.line([(820, y), (1200, y)], fill=(255, 255, 255, 28), width=2)
    img.alpha_composite(grid)
    # portrait disc
    pr = ImageOps.fit(portrait(), (230, 230), Image.LANCZOS, centering=(.5, .25))
    m = Image.new('L', (230, 230), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 229, 229], fill=255)
    ring = Image.new('RGBA', (250, 250), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([0, 0, 249, 249], fill=PAPER + (255,))
    img.alpha_composite(ring, (865, 225))
    img.paste(pr, (875, 235), m)
    img.alpha_composite(mark(72), (60, 52))
    fb = ImageFont.truetype(FB, 30)
    fz = ImageFont.truetype(FZH, 30)
    d = ImageDraw.Draw(img)
    d.text((150, 62), 'Evan Lee', font=fb, fill='white')
    d.text((150 + d.textlength('Evan Lee ', font=fb), 62), '李敏彦', font=fz, fill=(185, 194, 207))
    d.text((150, 100), 'ERA PROPERTY AGENT · CEA R074252A', font=ImageFont.truetype(FM, 19), fill=(255, 138, 156))
    size = 60
    while True:
        fh = ImageFont.truetype(FB, size)
        lines = _wrap(d, headline, fh, 740)
        if len(lines) <= 3 or size <= 40:
            break
        size -= 4
    y = 200
    for ln in lines[:3]:
        d.text((60, y), ln, font=fh, fill='white')
        y += int(size * 1.2)
    fs = ImageFont.truetype(FB, 26)
    wa = 'WhatsApp +65 8824 2798'
    tw = d.textlength(wa, font=fs)
    d.rounded_rectangle([60, H - 110, 60 + tw + 40, H - 58], 26, fill=(18, 140, 74))
    d.text((80, H - 101), wa, font=fs, fill='white')
    d.text((60, H - 150), 'ERA Realty Network Pte Ltd · Licence L3002382K', font=ImageFont.truetype(FM, 22), fill=(185, 194, 207))
    p = os.path.join(OUT, 'img', 'share', slug + '.jpg')
    img.convert('RGB').save(p, 'JPEG', quality=62, optimize=True, progressive=True)


def main():
    os.makedirs(os.path.join(OUT, 'img', 'share'), exist_ok=True)
    save_portraits()
    icons()
    # One share image for every page until Evan sends a proper headshot (see build.SHARE).
    card('home', build.PAGES['']['h1'])
    print('share images:', len(build.PAGES))


if __name__ == '__main__':
    main()

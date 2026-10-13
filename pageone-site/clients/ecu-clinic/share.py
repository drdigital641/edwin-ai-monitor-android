"""Share images (WhatsApp, Facebook, Google) for The ECU Clinic, made from the client's own photos.

    card(slug, photo, headline) -> site/img/share/<slug>.jpg (1200x630, used as og:image)

photo is a full-size original in source/photos. Icons and logo files are made by prep.py.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source')
OUT = os.path.join(HERE, 'site')
FONT_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FONT_M = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
CHARCOAL = (24, 30, 34)
LOGO = os.path.join(SRC, 'logo-horizontal.png')
CHIPS = ['6-month warranty', 'Pick-up & delivery', 'Mon–Sat 10am–6pm']
WA = 'WhatsApp 9893 1923'


def _wrap(draw, text, font, width):
    lines, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def _logo_plate(height):
    logo = Image.open(LOGO).convert('RGBA')
    w = round(logo.width * height / logo.height)
    logo = logo.resize((w, height), Image.LANCZOS)
    pad = 14
    plate = Image.new('RGBA', (w + 2 * pad, height + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, plate.width - 1, plate.height - 1], 16, fill=(255, 255, 255, 245))
    plate.alpha_composite(logo, (pad, pad))
    return plate


def card(slug, photo, headline, kicker='Brake system specialist · Kaki Bukit'):
    W, H = 1200, 630
    img = ImageOps.fit(ImageOps.exif_transpose(Image.open(os.path.join(SRC, 'photos', photo))).convert('RGB'), (W, H), Image.LANCZOS)
    shade = Image.new('L', (W, 1))
    for x in range(W):
        shade.putpixel((x, 0), int(240 - 140 * min(1, x / (W * 0.85))))
    img = Image.composite(Image.new('RGB', (W, H), CHARCOAL), img, shade.resize((W, H)))
    canvas = img.convert('RGBA')
    canvas.alpha_composite(_logo_plate(72), (56, 46))
    d = ImageDraw.Draw(canvas)
    d.text((60, 196), kicker.upper(), font=ImageFont.truetype(FONT_M, 26), fill=(134, 220, 198))
    size = 64
    while True:
        fh = ImageFont.truetype(FONT_B, size)
        lines = _wrap(d, headline, fh, 800)
        if len(lines) <= 3 or size <= 44:
            break
        size -= 4
    y = 240
    for ln in lines[:3]:
        d.text((58, y), ln, font=fh, fill='white')
        y += int(size * 1.18)
    fs = ImageFont.truetype(FONT_B, 24)
    x, y = 60, H - 92
    glass = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glass)
    chips = []
    for chip in CHIPS:
        tw = d.textlength(chip, font=fs)
        g.rounded_rectangle([x, y, x + tw + 30, y + 46], 23, fill=(255, 255, 255, 38), outline=(255, 255, 255, 120), width=2)
        chips.append((x + 15, chip))
        x += tw + 40
    canvas.alpha_composite(glass)
    d = ImageDraw.Draw(canvas)
    for cx, chip in chips:
        d.text((cx, y + 10), chip, font=fs, fill='white')
    tw = d.textlength(WA, font=fs)
    d.rounded_rectangle([W - 56 - tw - 34, y, W - 56, y + 46], 23, fill=(20, 128, 62))
    d.text((W - 56 - tw - 17, y + 10), WA, font=fs, fill='white')
    path = os.path.join(OUT, 'img', 'share', slug + '.jpg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(os.path.join(os.path.dirname(path), 'index.html'), 'a').close()
    canvas.convert('RGB').save(path, 'JPEG', quality=64, optimize=True, progressive=True)
    return path

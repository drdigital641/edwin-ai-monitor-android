"""Share images (WhatsApp, Facebook, Google) and site icons for DMTS, made from the client's own photos.

    card(slug, photo, headline)   -> site/img/share/<slug>.jpg (1200x630, used as og:image)
    icons()                       -> favicon.ico, icon-48/96/192/512.png, apple-touch-icon.png, logo.png

Photos come from the full-size originals in source/photos (the web .webp files are 800px copies).
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source', 'photos')
OUT = os.path.join(HERE, 'site')
FONT_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FONT_M = '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
NAVY = (11, 30, 51)
LOGO = os.path.join(SRC, 'Dynamic-Motoring-Logo_transparent.png')

# web image name -> full-size original
ORIGINAL = {
    'atf-fluids': 'IMG_0399e.jpg', 'customer-lounge': 'IMG_0420e.jpg', 'diagnostics': 'IMG_0311e.jpg',
    'engine-bay-check': 'IMG_0304e.jpg', 'gearbox-parts': 'IMG_0321e.jpg', 'gearbox-removal': 'IMG_0329e.jpg',
    'gearbox-teardown': 'IMG_0318e.jpg', 'hero-workshop': 'IMG_0301e.jpg', 'mechanics-under-car': 'IMG_0298e.jpg',
    'shopfront': 'Shopfront-02.jpg', 'transmission-cutaway': 'WhatsApp-Image-2017-12-14-at-4.04.40-PM-1.jpg',
    'workshop-lifts': 'WhatsApp-Image-2017-12-15-at-11.47.32-AM.jpg',
}


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
    logo = logo.crop(logo.getbbox())
    w = round(logo.width * height / logo.height)
    logo = logo.resize((w, height), Image.LANCZOS)
    pad = 16
    plate = Image.new('RGBA', (w + 2 * pad, height + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, plate.width - 1, plate.height - 1], 18, fill=(255, 255, 255, 245))
    plate.alpha_composite(logo, (pad, pad))
    return plate


def card(slug, photo, headline, kicker='Gearbox & auto transmission specialist · Singapore'):
    W, H = 1200, 630
    img = ImageOps.fit(Image.open(os.path.join(SRC, ORIGINAL[photo])).convert('RGB'), (W, H), Image.LANCZOS)
    # Dark navy wash, strongest on the left where the text sits.
    shade = Image.new('L', (W, 1))
    for x in range(W):
        shade.putpixel((x, 0), int(235 - 150 * min(1, x / (W * 0.85))))
    shade = shade.resize((W, H))
    img = Image.composite(Image.new('RGB', (W, H), NAVY), img, shade)
    d = ImageDraw.Draw(img)
    canvas = img.convert('RGBA')
    canvas.alpha_composite(_logo_plate(70), (56, 48))
    d = ImageDraw.Draw(canvas)
    fk = ImageFont.truetype(FONT_M, 26)
    d.text((60, 196), kicker.upper(), font=fk, fill=(156, 199, 255))
    size = 64
    while True:
        fh = ImageFont.truetype(FONT_B, size)
        lines = _wrap(d, headline, fh, 780)
        if len(lines) <= 3 or size <= 44:
            break
        size -= 4
    y = 240
    for ln in lines[:3]:
        d.text((58, y), ln, font=fh, fill='white')
        y += int(size * 1.18)
    # Bottom strip: the three offers and the WhatsApp number.
    fs = ImageFont.truetype(FONT_B, 25)
    x, y = 60, H - 92
    glass = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glass)
    chips = []
    for chip in ['Diagnostic from S$30', 'Free towing', '6-month warranty']:
        tw = d.textlength(chip, font=fs)
        g.rounded_rectangle([x, y, x + tw + 32, y + 46], 23, fill=(255, 255, 255, 38), outline=(255, 255, 255, 120), width=2)
        chips.append((x + 16, chip))
        x += tw + 44
    canvas.alpha_composite(glass)
    d = ImageDraw.Draw(canvas)
    for cx, chip in chips:
        d.text((cx, y + 9), chip, font=fs, fill='white')
    wa = 'WhatsApp 8430 9665'
    tw = d.textlength(wa, font=fs)
    d.rounded_rectangle([W - 60 - tw - 36, y, W - 60, y + 46], 23, fill=(20, 128, 62))
    d.text((W - 60 - tw - 18, y + 9), wa, font=fs, fill='white')
    path = os.path.join(OUT, 'img', 'share', slug + '.jpg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    canvas.convert('RGB').save(path, 'JPEG', quality=84, optimize=True, progressive=True)
    return path


def icons():
    """Square gear icon from the logo, for browser tabs, Google results and phone home screens."""
    logo = Image.open(LOGO).convert('RGBA')
    logo = logo.crop(logo.getbbox())
    # The gears sit at the left of the logo: cut at the first empty column after them.
    alpha = logo.getchannel('A')
    top = int(logo.height * 0.7)  # "Transmission Specialist" runs along the bottom, under the grey gear
    cut = next(x for x in range(logo.height // 4, logo.width) if alpha.crop((x, 0, x + 1, top)).getbbox() is None)
    gear = logo.crop((0, 0, cut, logo.height))
    gear = gear.crop(gear.getbbox())
    def square(size, pad, bg):
        im = Image.new('RGBA', (size, size), bg)
        g = ImageOps.contain(gear, (size - 2 * pad, size - 2 * pad), Image.LANCZOS)
        im.alpha_composite(g, ((size - g.width) // 2, (size - g.height) // 2))
        return im
    out = {}
    for s in (48, 96, 192, 512):
        p = os.path.join(OUT, f'icon-{s}.png')
        square(s, max(2, s // 16), (255, 255, 255, 255)).save(p, optimize=True)
        out[s] = p
    square(180, 18, (255, 255, 255, 255)).convert('RGB').save(os.path.join(OUT, 'apple-touch-icon.png'), optimize=True)
    square(48, 2, (255, 255, 255, 255)).save(os.path.join(OUT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    wide = ImageOps.contain(logo, (1200, 450), Image.LANCZOS)
    plate = Image.new('RGBA', (wide.width + 60, wide.height + 60), (255, 255, 255, 255))
    plate.alpha_composite(wide, (30, 30))
    plate.convert('RGB').save(os.path.join(OUT, 'img', 'logo.png'), optimize=True)
    return out


if __name__ == '__main__':
    print(card('sample', 'hero-workshop', 'Gearbox Repair & Auto Transmission Specialist in Singapore'))
    print(icons())

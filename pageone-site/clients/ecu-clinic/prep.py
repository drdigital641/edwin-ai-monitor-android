"""Web images, logo and icons for The ECU Clinic, made from the client's own files in source/.

    python3 prep.py   -> site/img/*.webp (4:3, 800 px), site/img/logo.webp/.png, favicon + icons

CROP keeps each photo's subject in a 4:3 frame (top, bottom as fractions of the photo height, or
None to centre-crop). The BMW scan screen is cropped above the customer's VIN.
"""
import os
from PIL import Image, ImageChops, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source')
OUT = os.path.join(HERE, 'site')
IMG = os.path.join(OUT, 'img')

HERO = 'mercedes-esp-pumps'  # home hero background (also gets a 1200 px -lg version)

# web name -> (source photo, (top, bottom) as fractions of height, or None)
PHOTOS = {
    'ecu-circuit-board': ('module-circuit-board.jpg', None),
    'ecu-board-repair': ('ecu-board-pad-repair.jpg', (0.16, 0.58)),
    'ecu-chip-damage': ('ecu-board-damaged-chip.jpg', (0.10, 0.52)),
    'abs-pump-in-car': ('abs-unit-engine-bay-1.jpg', (0.25, 0.81)),
    'abs-module-in-car': ('abs-unit-engine-bay-2.jpg', (0.26, 0.68)),
    'esp-control-unit-scan': ('diagnostic-mercedes-esp-version.jpg', (0.37, 0.80)),
    'bmw-fault-code-scan': ('diagnostic-bmw-fault-codes.jpg', (0.225, 0.645)),  # stops above the VIN
    'mercedes-module-wiring': ('mercedes-module-wiring.jpg', (0.30, 0.72)),
    'ecu-units-on-bench': ('ecu-units-on-bench.jpg', None),
    'bmw-body-module': ('bmw-fem-body-module.jpg', (0.19, 0.75)),
    'vw-gateway-module': ('vw-gateway-module.jpg', (0.30, 0.86)),
    # Job photos from the client, 13 Oct 2026 (ABS / TCU / ELV / hybrid battery refocus)
    'abs-esc-units-bench': ('abs-esc-units-on-bench.jpg', (0.04, 0.60)),
    'mercedes-esp-pumps': ('mercedes-esp-pumps.jpg', (0.20, 0.60)),
    'hyundai-kia-esc': ('hyundai-kia-esc-units.jpg', (0.30, 0.70)),
    'mercedes-7g-conductor-plate': ('mercedes-722-9-conductor-plate-kit.jpg', (0.28, 0.70)),
    'active-brake-assist-warning': ('mercedes-active-brake-assist-warning.jpg', None),
    'control-board-bench': ('control-board-repair-bench.jpg', None),
    'mini-fuse-box': ('mini-fuse-box.jpg', (0.12, 0.68)),
    'mercedes-elv': ('mercedes-elv-steering-lock.jpg', (0.42, 0.82)),
    'elv-units': ('elv-steering-lock-units.jpg', (0.30, 0.70)),
    'hybrid-battery-pack': ('hybrid-battery-pack-1.jpg', (0.18, 0.58)),
    'hybrid-battery-side': ('hybrid-battery-pack-2.jpg', (0.22, 0.62)),
    'hybrid-battery-modules': ('hybrid-battery-new-modules.jpg', (0.10, 0.50)),
    # Honda scan screens from Edwin, 14 Oct 2026 (VIN / frame and serial numbers blurred in the source copy).
    # A 4-value crop is (left, top, right, bottom) as fractions.
    'honda-radar-fault-codes': ('honda-vezel-radar-fault-codes.jpg', (0.10, 0.21, 0.86, 0.97)),
    'mercedes-esp-fault-code': ('mercedes-esp-n30-4-fault-code.jpg', (0.33, 0.75)),
    'bmw-cas-fault-codes': ('bmw-cas-fault-codes.jpg', (0.04, 0.10, 0.70, 0.98)),
    'honda-yaw-rate-codes': ('honda-yaw-rate-sensor-codes.jpg', (0.0, 0.0, 0.73, 1.0)),
    'honda-abs-radar-codes': ('honda-vezel-abs-and-radar-codes.jpg', (0.12, 0.44, 0.86, 0.85)),
    'honda-vsa-fault-codes': ('honda-vezel-vsa-fault-codes.jpg', (0.13, 0.33, 1.0, 0.82)),
    # Job photos from Edwin, 27 Oct 2026 (VIN and scanner serial blurred in the source copies).
    # A 5th value 'pad' keeps the whole crop and pads it to 4:3 on a dark background (wide scan screens).
    'bmw-cas3-modules': ('bmw-cas3-modules-e90.jpg', (0.0, 0.33, 1.0, 0.80)),
    'mercedes-c180-esp-unit': ('mercedes-c180-cgi-esp-unit.jpg', None),
    'mercedes-c180-esp-codes': ('mercedes-c180-cgi-esp-codes.jpg', (0.17, 0.19, 0.92, 0.80, 'pad')),
    'mercedes-me17-ecus': ('mercedes-me17-ecus-c205.jpg', (0.08, 0.0, 0.92, 1.0)),
    'mercedes-camtronic-codes': ('mercedes-me-camtronic-codes.jpg', (0.0, 0.34, 1.0, 0.80, 'pad')),
    'audi-abs-fault-codes': ('audi-a3-abs-codes.jpg', (0.19, 0.0, 0.97, 0.77)),
    # Toyota Alphard / Vellfire Hybrid job from Edwin, 30 Oct 2026. The source copies already have the scanner
    # serial and VIN painted out and the licence plate cut off; the crops below stay clear of both areas.
    'toyota-alphard-abs-codes': ('toyota-alphard-hybrid-abs-codes.jpg', (0.10, 0.02, 0.94, 0.68, 'pad')),
    'toyota-alphard-new-actuator': ('toyota-alphard-new-brake-actuator.jpg', (0.15, 0.59)),
    'toyota-alphard-old-vs-new-actuator': ('toyota-alphard-old-vs-new-brake-actuator.jpg', (0.0, 0.0, 1.0, 0.68, 'pad')),
}


def photo(name):
    src, band = PHOTOS[name]
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, 'photos', src))).convert('RGB')
    if band and len(band) >= 4:
        im = im.crop((int(im.width * band[0]), int(im.height * band[1]), int(im.width * band[2]), int(im.height * band[3])))
        if len(band) == 5 and band[4] == 'pad':
            w = max(im.width, im.height * 4 // 3)
            canvas = Image.new('RGB', (w, w * 3 // 4), (24, 28, 34))
            canvas.paste(im, ((w - im.width) // 2, (w * 3 // 4 - im.height) // 2))
            im = canvas
    elif band:
        im = im.crop((0, int(im.height * band[0]), im.width, int(im.height * band[1])))
    return ImageOps.fit(im, (1600, 1200) if im.width >= 1600 else (im.width, im.width * 3 // 4), Image.LANCZOS)


def web_photos():
    for name in PHOTOS:
        im = photo(name)
        q = 50 if name.startswith('ecu-') else 62  # dense circuit-board detail compresses poorly
        im.resize((640, 480), Image.LANCZOS).save(os.path.join(IMG, name + '.webp'), 'WEBP', quality=q, method=6)
        im.resize((1200, 900), Image.LANCZOS).save(os.path.join(IMG, name + '-lg.webp'), 'WEBP', quality=40, method=6) if name == HERO else None


def _cutout(box):
    """Part of the logo with the white background made transparent."""
    im = Image.open(os.path.join(SRC, 'logo-original.jpg')).convert('RGB').crop(box)
    # Distance from white: the darkest channel of each pixel (keeps coloured parts as well as grey text).
    r, g, b = im.split()
    dist = ImageChops.invert(ImageChops.darker(ImageChops.darker(r, g), b))
    alpha = dist.point(lambda v: 0 if v < 12 else min(255, int((v - 12) * 255 / 60)))
    out = im.convert('RGBA')
    out.putalpha(alpha)
    return out.crop(out.getbbox())


BOARD = (110, 70, 390, 240)
WORDS = (30, 250, 470, 296)
TAG = (100, 308, 400, 332)


def logos():
    board, words, tag = _cutout(BOARD), _cutout(WORDS), _cutout(TAG)
    # Horizontal lockup for the header: board on the left, name and tagline on the right.
    bh = 150
    board_s = board.resize((round(board.width * bh / board.height), bh), Image.LANCZOS)
    tw = 520
    words_s = words.resize((tw, round(words.height * tw / words.width)), Image.LANCZOS)
    tag_s = tag.resize((round(tag.width * tw / words.width * 1.05), round(tag.height * tw / words.width * 1.05)), Image.LANCZOS)
    gap = 26
    W = board_s.width + gap + tw
    lock = Image.new('RGBA', (W, bh), (0, 0, 0, 0))
    lock.alpha_composite(board_s, (0, 0))
    ty = (bh - words_s.height - 16 - tag_s.height) // 2
    lock.alpha_composite(words_s, (board_s.width + gap, ty))
    lock.alpha_composite(tag_s, (board_s.width + gap + 2, ty + words_s.height + 16))
    lock.resize((538, 100), Image.LANCZOS).save(os.path.join(IMG, 'logo.webp'), 'WEBP', quality=82, alpha_quality=70, method=6)
    flat = Image.new('RGBA', lock.size, (255, 255, 255, 255))
    flat.alpha_composite(lock)
    flat.convert('RGB').quantize(64).save(os.path.join(IMG, 'logo.png'), optimize=True)
    lock.save(os.path.join(SRC, 'logo-horizontal.png'))
    board.save(os.path.join(SRC, 'logo-board.png'))
    print('logo', lock.size)
    # Favicon and app icons: the watchdog's redesign (14 Oct 2026, Edwin's request) lives in source/favicon/
    # and is copied as is, so re-running prep.py keeps it.
    import shutil
    for f in ('favicon.ico', 'icon-48.png', 'icon-96.png', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'):
        shutil.copy(os.path.join(SRC, 'favicon', f), os.path.join(OUT, f))

if __name__ == '__main__':
    os.makedirs(IMG, exist_ok=True)
    web_photos()
    logos()
    for d in (IMG,):
        open(os.path.join(d, 'index.html'), 'w').close()

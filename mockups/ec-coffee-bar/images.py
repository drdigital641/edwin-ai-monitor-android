"""Makes the site's webp photos from source/ (python3 images.py).
Sources: EC Coffee Bar's own menu PDF (July 2025, published on her Grab Dine Out listing) and the photos
she uploaded to Grab Dine Out. Each crop is (source file, box in source pixels)."""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source')
OUT = os.path.join(HERE, 'site', 'img')
M = lambda n: os.path.join(SRC, 'menu-pages', 'p-%03d.jpg' % n)
G = lambda n: os.path.join(SRC, 'grab', 'g%d.webp' % n)

CROPS = {
    'signature-spread': (M(20), (742, 100, 1232, 700)),       # Signature Spread wine set for 4-6 pax
    'afternoon-tea': (M(12), (47, 152, 538, 455)),             # EC afternoon Glow Tea Set
    'lunch-spread': (M(10), (742, 88, 1232, 488)),            # EC mixed lunch set
    'sunrise-sharing': (M(2), (742, 418, 1232, 690)),          # EC Sunrise sharing, 4 drinks
    'croissant-set': (M(2), (742, 98, 1232, 340)),             # Sunrise croissants, 4 drinks
    'cake-slices': (M(11), (4, 124, 568, 322)),
    'cocktails': (M(26), (742, 470, 1235, 712)),               # EC 6 signature cocktails set
    'wine-dinner': (M(15), (47, 91, 538, 418)),                # Mango Salsa chicken with wine
    'lamb-wine': (M(15), (880, 91, 1232, 418)),
    'cheese-wine': (M(17), (90, 205, 640, 520)),
    'beer-snacks': (M(18), (712, 108, 1278, 342)),
    'dinner-for-two': (M(19), (0, 84, 372, 308)),
    'iced-drinks': (M(24), (642, 232, 1026, 672)),
    'carbonara': (M(7), (0, 140, 640, 560)),
    'breakfast-platter': (G(1), (0, 120, 1080, 1340)),
    'breakfast-studio': (G(4), None),
    'prawn-bowl': (G(3), None),
    'chocolate-cake': (G(5), None),
    'lamb-rack': (G(6), None),
    'bar-counter': (G(7), None),
    'melon-salad': (G(8), (0, 120, 1080, 960)),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    sizes = {}
    for name, (src, box) in CROPS.items():
        im = Image.open(src).convert('RGB')
        if box:
            im = im.crop(box)
        if im.width > 560:
            im = im.resize((560, round(im.height * 560 / im.width)), Image.LANCZOS)
        q = 42 if name in ('breakfast-platter', 'chocolate-cake', 'lamb-rack', 'bar-counter') else 56
        im.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=q, method=6)  # one size only: the bridge takes text-encoded uploads
        sizes[name] = im.size
    # logo: circular badge from her Grab logo
    logo = Image.open(G(10)).convert('RGBA')
    mask = Image.new('L', logo.size, 0)
    ImageDraw.Draw(mask).ellipse((4, 4, logo.width - 5, logo.height - 5), fill=255)
    logo.putalpha(mask)
    logo.save(os.path.join(OUT, 'logo.png'))
    logo.resize((160, 160), Image.LANCZOS).save(os.path.join(OUT, 'logo-160.webp'), 'WEBP', quality=90)
    site = os.path.dirname(OUT)
    for s in (192, 512):
        bg = Image.new('RGBA', (s, s), (255, 255, 255, 255)); l = logo.resize((s, s), Image.LANCZOS); bg.alpha_composite(l)
        bg.convert('RGB').quantize(32).save(os.path.join(site, 'icon-%d.png' % s), optimize=True)
    bg = Image.new('RGBA', (180, 180), (255, 255, 255, 255)); bg.alpha_composite(logo.resize((180, 180), Image.LANCZOS))
    bg.convert('RGB').quantize(32).save(os.path.join(site, 'apple-touch-icon.png'), optimize=True)
    logo.resize((48, 48), Image.LANCZOS).save(os.path.join(site, 'favicon.ico'), sizes=[(48, 48), (32, 32), (16, 16)])
    # share image 1200x630
    sp = Image.open(os.path.join(OUT, 'signature-spread.webp')).convert('RGB')
    w = 1200; sp = sp.resize((w, round(sp.height * w / sp.width)), Image.LANCZOS)
    top = max(0, (sp.height - 630) // 2); share = sp.crop((0, top, w, top + 630))
    os.makedirs(os.path.join(OUT, 'share'), exist_ok=True)
    share.save(os.path.join(OUT, 'share', 'home.jpg'), quality=70)
    for k, v in sizes.items():
        print(k, v)


if __name__ == '__main__':
    main()

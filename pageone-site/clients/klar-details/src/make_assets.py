"""Brand assets for the preview: K mark (SVG + PNG favicons) and a 1200x630 og.jpg. Replace with the client's logo files at go-live."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'assets')
os.makedirs(A, exist_ok=True)
RED = (215, 38, 45)
INK = (11, 13, 16)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0b0d10"/>'
       '<path d="M18 14h9v15.2L40.6 14H52L35.2 32.4 52.8 50H41.2L27 34.6V50h-9z" fill="#d7262d"/></svg>')
open(os.path.join(A, 'logo.svg'), 'w').write(SVG)


def mark(size):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    r = size * 14 // 64
    dr.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=INK)
    f = ImageFont.truetype(FONT, int(size * 0.72))
    bb = dr.textbbox((0, 0), 'K', font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    dr.text(((size - w) / 2 - bb[0], (size - h) / 2 - bb[1]), 'K', font=f, fill=RED)
    return im


for s, name in ((192, 'icon-192.png'), (512, 'icon-512.png'), (180, 'apple-touch-icon.png'), (512, 'logo.png')):
    mark(s).save(os.path.join(A, name))
mark(48).convert('RGB').save(os.path.join(HERE, 'favicon.ico'), sizes=[(48, 48)])

og = Image.new('RGB', (1200, 630), INK)
dr = ImageDraw.Draw(og)
for i in range(630):
    c = int(11 + i * 0.03)
    dr.line((0, i, 1200, i), fill=(c, c + 2, c + 4))
dr.rounded_rectangle((80, 150, 300, 370), radius=48, fill=(20, 23, 28), outline=(60, 64, 70), width=2)
f = ImageFont.truetype(FONT, 160)
bb = dr.textbbox((0, 0), 'K', font=f)
dr.text((190 - (bb[2] - bb[0]) / 2 - bb[0], 260 - (bb[3] - bb[1]) / 2 - bb[1]), 'K', font=f, fill=RED)
f1 = ImageFont.truetype(FONT, 84)
dr.text((350, 170), 'Klar Details', font=f1, fill=(255, 255, 255))
f2 = ImageFont.truetype(FONT, 34)
dr.text((352, 280), 'Premium car detailing centre', font=f2, fill=(205, 208, 214))
dr.text((352, 330), 'Toh Guan Road East, Singapore', font=f2, fill=(205, 208, 214))
f3 = ImageFont.truetype(FONT, 26)
dr.text((352, 420), 'Because Every Detail Counts', font=f3, fill=RED)
dr.line((80, 540, 1120, 540), fill=(50, 54, 60), width=2)
dr.text((80, 560), 'Ceramic & graphene coating  ·  Paint correction  ·  Interior detailing  ·  Since 2014', font=ImageFont.truetype(FONT, 24), fill=(170, 174, 181))
og.save(os.path.join(A, 'og.jpg'), quality=86, optimize=True)
print('assets ok')

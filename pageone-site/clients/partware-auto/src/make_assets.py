#!/usr/bin/env python3
"""Generate Partware Auto favicon set, og.jpg and text logo with Pillow (no Honda logo). Run: python3 make_assets.py"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = HERE / "assets"; L = HERE / "logo"; A.mkdir(exist_ok=True); L.mkdir(exist_ok=True)
F = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INK = (18, 22, 28); RED = (212, 42, 30); WHITE = (255, 255, 255); GREY = (201, 207, 216)
font = lambda p, s: ImageFont.truetype(p, s)

def slanted(draw, box, color, skew=0.18):
    x0, y0, x1, y1 = box; d = (y1 - y0) * skew
    draw.polygon([(x0 + d, y0), (x1 + d, y0), (x1, y1), (x0, y1)], fill=color)

def icon(size):
    im = Image.new("RGB", (size, size), INK); d = ImageDraw.Draw(im)
    pad = int(size * .1); slanted(d, (pad, pad, size - pad - int(size * .18), size - pad), RED)
    f = font(F, int(size * .42)); t = "PW"
    w = d.textlength(t, font=f); d.text(((size - w) / 2 - size * .02, size * .5), t, font=f, fill=WHITE, anchor="lm")
    return im

for s, n in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (48, "favicon-48.png")):
    icon(s).save(A / n)
icon(256).save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

# og.jpg 1200x630
im = Image.new("RGB", (1200, 630), INK); d = ImageDraw.Draw(im)
d.polygon([(0, 0), (300, 0), (240, 630), (0, 630)], fill=RED)
d.polygon([(300, 0), (350, 0), (290, 630), (240, 630)], fill=(168, 30, 20))
d.text((60, 315), "PW", font=font(F, 150), fill=WHITE, anchor="lm")
d.text((400, 235), "PARTWARE AUTO", font=font(F, 76), fill=WHITE, anchor="lm")
d.text((404, 330), "Your Honda Parts Specialist", font=font(FB, 44), fill=GREY, anchor="lm")
d.rectangle((404, 395, 570, 401), fill=RED)
d.text((404, 450), "Retail  |  Wholesale  |  Export  |  Kaki Bukit", font=font(FB, 30), fill=GREY, anchor="lm")
im.save(A / "og.jpg", quality=88, optimize=True)

# text logos (png on transparent for light + dark backgrounds, plus svg)
def logo(fg, name):
    im = Image.new("RGBA", (900, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    slanted(d, (8, 20, 100, 140), RED); d.text((54, 80), "PW", font=font(F, 50), fill=WHITE, anchor="mm")
    d.text((140, 80), "PARTWARE AUTO", font=font(F, 76), fill=fg, anchor="lm"); im.save(L / name)
logo(INK, "logo.png"); logo(WHITE, "logo-dark.png")
for fg, n in (("#12161C", "logo.svg"), ("#FFFFFF", "logo-dark.svg")):
    (L / n).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 160" width="900" height="160" role="img" aria-label="Partware Auto"><polygon points="26,20 118,20 100,140 8,140" fill="#D42A1E"/><text x="54" y="96" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="50" fill="#fff" text-anchor="middle">PW</text><text x="140" y="104" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="72" fill="{fg}">PARTWARE AUTO</text></svg>')
print("assets ok")

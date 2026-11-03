"""Favicons + share image for the ContiExpert / Volt Autocare preview. Run: python3 make_assets.py <out_assets_dir>"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
NAVY=(11,27,43); VOLT=(200,240,49); WHITE=(255,255,255); MUTED=(160,176,194)
F='/usr/share/fonts/opentype/inter/'
def font(w,s): return ImageFont.truetype(F+('Inter-%s.otf'%w), s)
def bolt(d, x, y, s, fill):
    pts=[(0.58,0.04),(0.18,0.56),(0.46,0.56),(0.38,0.96),(0.82,0.40),(0.54,0.40),(0.66,0.04)]
    d.polygon([(x+px*s,y+py*s) for px,py in pts], fill=fill)
def mark(n):
    im=Image.new('RGBA',(n*4,n*4),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,n*4-1,n*4-1], radius=int(n*4*0.22), fill=NAVY)
    bolt(d, n*4*0.14, n*4*0.12, n*4*0.76, VOLT)
    return im.resize((n,n), Image.LANCZOS)
mark(512).save(os.path.join(out,'icon-512.png'))
mark(192).save(os.path.join(out,'icon-192.png'))
mark(180).convert('RGB').save(os.path.join(out,'apple-touch-icon.png'))
mark(96).save(os.path.join(out,'favicon-96.png'))
mark(48).save(os.path.join(out,'favicon.ico'), sizes=[(48,48),(32,32),(16,16)])
# share image 1200x630: 10 km rings around the Newton Circus pin
W,H=1200,630; im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
cx,cy=870,315
for r,c in ((290,(22,44,66)),(190,(28,54,80)),(95,(36,66,96))):
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=c, outline=(60,92,124), width=2)
for r,l in ((95,'3 km'),(190,'6 km'),(290,'10 km')):
    d.text((cx+6, cy-r+8), l, font=font('Medium',22), fill=MUTED)
d.ellipse([cx-16,cy-16,cx+16,cy+16], fill=VOLT)
d.ellipse([cx-6,cy-6,cx+6,cy+6], fill=NAVY)
m=mark(88); im.paste(m,(70,70),m)
d.text((176,78),'ContiExpert', font=font('Bold',44), fill=WHITE)
d.text((178,130),'by Volt Autocare', font=font('Medium',24), fill=VOLT)
y=230
for line in ('European car servicing','and repairs at','Newton Circus'):
    d.text((70,y), line, font=font('Bold',56), fill=WHITE); y+=68
d.text((70,470),'143 Bukit Timah Road, inside Shell', font=font('Medium',28), fill=MUTED)
d.text((70,512),'WhatsApp +65 8221 5502', font=font('SemiBold',28), fill=VOLT)
im.save(os.path.join(out,'og.jpg'), quality=86, optimize=True, progressive=True)
print('assets ok')

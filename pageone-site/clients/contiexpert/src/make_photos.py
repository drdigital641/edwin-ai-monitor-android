"""Copy the client's public images (fetched 3 Nov 2026 with Edwin's OK) into assets/photos as WebP. Run: python3 make_photos.py <research-fetch dir> <out assets dir>"""
import sys, os, json
from PIL import Image
R, OUT = sys.argv[1], os.path.join(sys.argv[2], 'photos'); os.makedirs(OUT, exist_ok=True)
wp = {x['n']: x['file'] for x in json.load(open(os.path.join(R, 'wp-manifest.json')))}
def save(im, name, w, crop=None):
    im = im.convert('RGB')
    if crop:  # crop box as fractions (l,t,r,b)
        W, H = im.size; im = im.crop((int(crop[0]*W), int(crop[1]*H), int(crop[2]*W), int(crop[3]*H)))
    if im.size[0] > w: im = im.resize((w, int(im.size[1]*w/im.size[0])), Image.LANCZOS)
    im.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=78); return im.size
dims = {}
S = lambda n: Image.open(os.path.join(R, 'social', n + '.webp'))
# real Volt staff/workshop stills (TikTok/Instagram covers)
dims['team-coilwash'] = save(S('tt-coilwash'), 'team-coilwash', 540, (0, 0.04, 1, 0.80))
dims['team-atf'] = save(S('tt-atf'), 'team-atf', 540, (0, 0.04, 1, 0.80))
dims['team-outdoor'] = save(S('ig-2025-11-21-video'), 'team-outdoor', 360, (0, 0.08, 1, 0.66))
dims['cataclean-hybrid'] = save(S('fb-2026-04'), 'cataclean-hybrid', 526)
for n in ['ig-2025-12-15b', 'ig-2025-12-23b', 'ig-2025-12-23a', 'ig-2025-11-19', 'ig-2025-12-15a', 'ig-2025-11-26', 'ig-2025-11-25', 'ig-2025-12-03']:
    dims[n] = save(S(n), n, 512)
# topic photos from the client's current website media library
for key, n in {'svc-servicing': 38, 'svc-diagnostics': 47, 'svc-aircon': 72, 'svc-brakes': 9, 'svc-ppi': 37, 'svc-hybrid': 177,
               'brand-bmw': 57, 'brand-mercedes': 94, 'brand-audi': 31, 'consult': 48, 'mechanic-under': 186}.items():
    dims[key] = save(Image.open(os.path.join(R, 'wp', wp[n])), key, 1000)
for key, n in {'logo-bmw': 105, 'logo-mercedes': 106, 'logo-audi': 100, 'logo-vw': 98, 'logo-porsche': 101, 'logo-mini': 99}.items():
    dims[key] = save(Image.open(os.path.join(R, 'wp', wp[n])), key, 160)
json.dump(dims, open(os.path.join(OUT, 'dims.json'), 'w'))
print(len(dims), 'photos', sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) // 1024, 'KB')

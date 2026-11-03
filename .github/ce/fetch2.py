"""Round 2 (Edwin, 3 Nov 2026): find REAL Volt Autocare workshop photos.
Downloads the business's own public TikTok/Instagram videos with yt-dlp, pulls frames every 1.5 s,
and collects Google listing photo URLs exposed on the public AutoKaki and Google Maps pages.
Output: pageone-site/clients/contiexpert/src/research-fetch/real/"""
import os, re, subprocess, json, urllib.request, glob
from PIL import Image

OUT = 'pageone-site/clients/contiexpert/src/research-fetch/real'
os.makedirs(OUT + '/video', exist_ok=True); os.makedirs(OUT + '/frames', exist_ok=True); os.makedirs(OUT + '/google', exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36', 'Accept-Language': 'en-SG,en;q=0.9'}
log = []

VIDEOS = [
    'https://www.tiktok.com/@volt.autocare/video/7590338366718119176',
    'https://www.tiktok.com/@volt.autocare/video/7589786815586979090',
    'https://www.tiktok.com/@volt.autocare/video/7521640813332352274',
    'https://www.tiktok.com/@volt.autocare/video/7521639730732092679',
    'https://www.tiktok.com/@volt.autocare/video/7520132820224724232',
    'https://www.instagram.com/voltautocare/reel/DSUYy3gCVnf/',
]
# also try the whole TikTok profile (may list more videos)
try:
    r = subprocess.run(['yt-dlp', '--flat-playlist', '-J', 'https://www.tiktok.com/@volt.autocare'], capture_output=True, text=True, timeout=120)
    j = json.loads(r.stdout or '{}')
    for e in j.get('entries', []) or []:
        u = e.get('url') or e.get('webpage_url')
        if u and u not in VIDEOS: VIDEOS.append(u)
    log.append('profile entries: %d' % len(j.get('entries', []) or []))
except Exception as ex:
    log.append('profile list failed: %s' % ex)

for i, v in enumerate(VIDEOS[:25]):
    vid = re.sub(r'\W+', '-', v.rstrip('/').split('/')[-1])
    fn = '%s/video/%02d-%s.mp4' % (OUT, i, vid)
    r = subprocess.run(['yt-dlp', '-f', 'mp4/best', '-o', fn, v], capture_output=True, text=True, timeout=300)
    if not os.path.exists(fn):
        log.append('FAIL %s %s' % (v, r.stderr[-300:])); continue
    log.append('ok %s %d bytes' % (v, os.path.getsize(fn)))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', fn, '-vf', 'fps=1/1.5,scale=720:-2', '-q:v', '3', '%s/frames/%02d-%%03d.jpg' % (OUT, i)])
    os.remove(fn)  # keep frames only

# Google listing photos exposed on public pages
for name, url in [('autokaki', 'https://www.autokaki.com/locations/a89adf30-5c25-4de5-b30d-37b9d7b9d09b'),
                  ('gmaps', 'https://www.google.com/maps/place/?q=place_id:ChIJo3RG_6EZ2jERe6mk_x7K0Sw')]:
    try:
        h = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode('utf-8', 'ignore')
        urls = sorted(set(re.findall(r'https://lh[0-9]\.googleusercontent\.com/(?:p|gps-cs-s|geougc-cs)/[A-Za-z0-9_\-]+', h)))
        log.append('%s: %d google photo urls' % (name, len(urls)))
        for k, u in enumerate(urls[:30]):
            try:
                b = urllib.request.urlopen(urllib.request.Request(u + '=s1600', headers=UA), timeout=40).read()
                if len(b) > 8000:
                    open('%s/google/%s-%02d.jpg' % (OUT, name, k), 'wb').write(b)
            except Exception as ex:
                log.append('  img fail %s' % ex)
    except Exception as ex:
        log.append('%s page fail %s' % (name, ex))

# contact sheets (numbered) so the frames can be reviewed quickly
def sheet(files, outname, cols=8, w=200):
    if not files: return
    ims = []
    for f in files:
        try:
            im = Image.open(f).convert('RGB'); im.thumbnail((w, int(w * 1.8))); ims.append((os.path.basename(f), im))
        except Exception: pass
    from PIL import ImageDraw
    hmax = max(im.size[1] for _, im in ims) + 16
    rows = (len(ims) + cols - 1) // cols
    S = Image.new('RGB', (cols * w, rows * hmax), 'white'); d = ImageDraw.Draw(S)
    for k, (n, im) in enumerate(ims):
        x, y = (k % cols) * w, (k // cols) * hmax
        S.paste(im, (x, y)); d.text((x + 2, y + im.size[1] + 2), n, fill='black')
    S.save(OUT + '/' + outname, quality=80)
fr = sorted(glob.glob(OUT + '/frames/*.jpg'))
for k in range(0, len(fr), 48):
    sheet(fr[k:k + 48], 'sheet-frames-%d.jpg' % (k // 48 + 1))
sheet(sorted(glob.glob(OUT + '/google/*.jpg')), 'sheet-google.jpg', cols=5, w=300)
open(OUT + '/log.txt', 'w').write('\n'.join(log))
print('\n'.join(log)); print(len(fr), 'frames')

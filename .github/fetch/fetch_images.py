import sys, os, io, json, hashlib, urllib.request
from PIL import Image

urls_file, out_dir, max_kb, max_w = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
os.makedirs(out_dir, exist_ok=True)
mp_path = os.path.join(out_dir, "map.json")
mp = json.load(open(mp_path)) if os.path.exists(mp_path) else {}
for u in [l.strip() for l in open(urls_file) if l.strip()]:
    if u in mp:
        print("skip (done)", u)
        continue
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA, "Referer": "https://" + u.split("/")[2] + "/"})
        data = urllib.request.urlopen(req, timeout=40).read()
        im = Image.open(io.BytesIO(data))
        if getattr(im, "is_animated", False):
            print("animated, skip", u)
            continue
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        im = im.convert("RGBA" if has_alpha else "RGB")
        w = min(max_w, im.width)
        while True:
            h = round(im.height * w / im.width)
            r = im.resize((w, h), Image.LANCZOS) if w != im.width else im
            ok = False
            for q in (82, 76, 70, 64, 58, 52, 46):
                b = io.BytesIO()
                r.save(b, "WEBP", quality=q, method=6)
                if b.tell() <= max_kb * 1024:
                    ok = True
                    break
            if ok or w <= 480:
                break
            w = int(w * 0.85)
        f = hashlib.sha1(u.encode()).hexdigest()[:12] + ".webp"
        open(os.path.join(out_dir, f), "wb").write(b.getvalue())
        mp[u] = {"f": f, "w": r.width, "h": r.height}
        print("OK %6d KB %dx%d <- %d KB %s" % (len(b.getvalue()) // 1024, r.width, r.height, len(data) // 1024, u))
    except Exception as e:
        print("FAIL", u, e)
json.dump(mp, open(mp_path, "w"), indent=0)

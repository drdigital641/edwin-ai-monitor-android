#!/usr/bin/env python3
"""Write AtPhoto rows (src/db/photos.json) into the built site as assets/p/<id>.jpg.

Usage: python3 pull_photos.py [OUT_DIR] [--fetch]
  --fetch  first download all AtPhoto rows from the public API into db/photos.json
build.py calls run() automatically after building. Missing photos.json = nothing to do.
"""
import base64, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
API = "https://autotex-catalogue-05dbf5ec.base44.app/api/apps/6ae3683191b1a44205dbf5ec/entities/AtPhoto"

def fetch():
    import urllib.request
    rows, skip = [], 0
    while True:
        with urllib.request.urlopen(f"{API}?limit=100&skip={skip}", timeout=60) as r:
            page = json.load(r)
        rows += page
        if len(page) < 100: break
        skip += 100
    (HERE / "db").mkdir(exist_ok=True)
    (HERE / "db" / "photos.json").write_text(json.dumps(rows))
    return rows

def run(out):
    f = HERE / "db" / "photos.json"
    if not f.exists(): return 0
    n = 0
    d = Path(out) / "assets" / "p"
    for row in json.loads(f.read_text()):
        m = re.match(r"data:[^;,]+;base64,(.+)$", row.get("data") or "", re.S)
        if not (row.get("id") and m and re.fullmatch(r"[A-Za-z0-9_-]+", row["id"])): continue
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{row['id']}.jpg").write_bytes(base64.b64decode(m.group(1)))
        n += 1
    print(f"pull_photos: wrote {n} photos")
    return n

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--fetch" in sys.argv: fetch()
    run(args[0] if args else HERE.parent / "site")

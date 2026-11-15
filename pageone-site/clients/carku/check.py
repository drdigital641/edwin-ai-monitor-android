"""Checks the built site: JSON-LD parses, one H1, internal links and assets exist, no banned glyphs."""
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, "site"); bad = 0
# official images live only on the server (placed from the Bridge drop folder), listed here
DROP = set(open(os.path.join(HERE, "data", "drop_images.txt")).read().split())
for dp, _, fs in os.walk(S):
    for f in fs:
        if not f.endswith(".html"): continue
        fp = os.path.join(dp, f); h = open(fp).read(); rel = os.path.relpath(fp, S)
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try: json.loads(m)
            except Exception as ex: print("JSON-LD", rel, ex); bad += 1
        if h.count("<h1") != 1: print("H1 count", rel, h.count("<h1")); bad += 1
        if "—" in h or "→" in h: print("banned glyph", rel); bad += 1
        if f == "404.html": continue
        for u in re.findall(r'(?:href|src)="([^"#]+)', h):
            if u.startswith(("http", "mailto:", "tel:", "data:")): continue
            t = os.path.normpath(os.path.join(dp, u.split("?")[0]))
            if os.path.isdir(t): t = os.path.join(t, "index.html")
            if "/assets/img/carku/" in t and os.path.basename(t) in DROP: continue
            if not os.path.exists(t): print("missing", rel, u); bad += 1
print("problems:", bad); sys.exit(1 if bad else 0)

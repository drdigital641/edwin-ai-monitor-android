# Usage: promo_check.py <build.py dir> <file or dir>...  Checks before-10pm promo price consistency.
import sys, re, pathlib, importlib.util
src = pathlib.Path(sys.argv[1]) / "build.py"
txt = src.read_text()
P = {}
for k, aka, ah, lp, t in re.findall(r'\("([A-Z0-9-]+)","([^"]*)",(\d+),([\d.]+),"([^"]+)"\)', txt):
    P[k] = float(lp)
f = lambda x: f"${x:,.2f}"
roles = {}
for k, L in P.items():
    for role, v in (("list", L), ("walk", L-20), ("promo", L+30), ("was", L+50), ("night", L+80)):
        roles.setdefault(f(v), set()).add(role)
was_only = {v for v, r in roles.items() if r == {"was"}}
coll = {v: r for v, r in roles.items() if "was" in r and len(r) > 1}
files = []
for a in sys.argv[2:]:
    p = pathlib.Path(a)
    files += [x for x in p.rglob("*") if x.suffix in (".html", ".txt", ".js")] if p.is_dir() else [p]
bad = []
for fp in files:
    s = fp.read_text(errors="ignore")
    if "⟪" in s: bad.append((fp, "unrendered token"))
    for mm in re.finditer(r"\$[\d,]+\.\d\d", s):
        v = mm.group(); ctx = s[max(0, mm.start()-40):mm.end()+15]
        if v in was_only or v in coll:
            ok = ("<s>" in s[max(0, mm.start()-4):mm.start()]) or re.search(r"(usually|normally) $", s[max(0, mm.start()-12):mm.start()])
            if not ok and v in coll: continue  # same figure is also a valid other price
            if not ok: bad.append((fp, "unstruck old day price " + v + " :: " + ctx.replace("\n", " ")))
    for mm in re.finditer(r"\+ ?\$50\b", s):
        if not re.search(r"(normally|usually) $", s[max(0, mm.start()-10):mm.start()]):
            bad.append((fp, "formula +$50 :: " + s[max(0, mm.start()-60):mm.end()+20].replace("\n", " ")))
print("sizes", len(P), "collisions (was price equal to another valid price):", coll)
print("files", len(files), "issues", len(bad))
for b in bad[:60]: print(b[0], "|", b[1])

#!/usr/bin/env python3
"""Hand-off zip for ONE new article on a LIVE AutoSEO client domain (Edwin, 13 Nov 2026).

    python3 autoseo-clients/live_article_zip.py <site> <slug> [--date YYYY-MM-DD]

Sites: emats (ecumats.my), hybrid-world (hybridworld.com.my), carzy-world (carzyworld.com.my),
autoseo-my (autoseo.my itself: source autoseo-my/ at the repo root, which always builds live).
The live sites are built and deployed by Dev Desk (build_live.py / build.py --live). This script never deploys.
It runs the repo build in live mode (site-live/) and zips:
  source/data/articles/<slug>.json      the article data file (what build_live.py reads)
  overlay/...                           ready-built files, ONLY: the new article in EN/MS/ZH, the three /articles/
                                        index pages, sitemap.xml, llms.txt
  FILES.txt                             what is in the zip and the deploy rules
Deploy rules (Edwin): add-only. Never overwrite or delete .htaccess, the IndexNow key .txt, BingSiteAuth.xml,
robots.txt, .well-known/, cgi-bin/. Never re-sync existing pages or assets. Keep the live light CSS/JS
(66cb46470 zips); never the dark 741f9d1 / 3159841 files.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITES = {"emats": "config.json", "hybrid-world": "config.json", "carzy-world": "data/business.json", "autoseo-my": "data/brand.json"}
LANG_PREFIX = ["", "ms/", "zh/"]
PROTECTED = re.compile(r"(^|/)(\.htaccess|robots\.txt|BingSiteAuth\.xml|\.well-known/|cgi-bin/)|^[0-9a-f]{8,}\.txt$", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site", choices=sorted(SITES))
    ap.add_argument("slug")
    ap.add_argument("--date", default=(datetime.now(timezone.utc) + timedelta(hours=8)).date().isoformat())
    a = ap.parse_args()
    own = a.site == "autoseo-my"  # autoseo.my builds live already (brand.json preview false): no --live, output site/
    root = HERE.parent / "autoseo-my" if own else HERE / a.site
    cfg = json.loads((root / SITES[a.site]).read_text(encoding="utf-8"))
    live = cfg["site_url"].rstrip("/") + "/" if own else cfg["live_site_url"]
    if own and cfg.get("preview"):
        sys.exit("autoseo-my brand.json preview is true: not a live build")
    src = root / "data" / "articles" / f"{a.slug}.json"
    if not src.exists():
        sys.exit(f"no article data file {src}")
    r = subprocess.run([sys.executable, str(root / "src" / "build.py")] + ([] if own else ["--live"]))
    if r.returncode:
        sys.exit("live build failed: nothing zipped")
    out = root / ("site" if own else "site-live")
    files = []
    for p in LANG_PREFIX:
        files.append(f"{p}articles/index.html")
        art = out / p / "articles" / a.slug
        if not (art / "index.html").exists():
            sys.exit(f"missing {p}articles/{a.slug}/index.html")
        files += [str(f.relative_to(out)) for f in sorted(art.rglob("*")) if f.is_file()]
    files += ["sitemap.xml", "llms.txt"]

    problems = []
    for rel in files:
        if PROTECTED.search(rel):
            problems.append(f"protected file in overlay: {rel}")
        t = (out / rel).read_text(encoding="utf-8")
        if "/preview/" in t or "autoseo.my/preview" in t:
            problems.append(f"{rel}: preview URL")
        if rel.endswith(".html"):
            if 'content="index,follow' not in t or "noindex" in t:
                problems.append(f"{rel}: robots must be index,follow")
            m = re.search(r'<link rel="canonical" href="([^"]+)"', t)
            if not m or not m.group(1).startswith(live):
                problems.append(f"{rel}: canonical not on {live}")
    sm = (out / "sitemap.xml").read_text(encoding="utf-8")
    if f"{live}articles/{a.slug}/" not in sm:
        problems.append("sitemap.xml: new article missing")
    if f"{live}articles/{a.slug}/" not in (out / "llms.txt").read_text(encoding="utf-8"):
        problems.append("llms.txt: new article missing")
    if problems:
        sys.exit("STOP, nothing zipped:\n- " + "\n- ".join(problems))

    dest = Path("/mnt/project-files/autoseo-my/live-articles") / a.date
    dest.mkdir(parents=True, exist_ok=True)
    zp = dest / f"{a.site}-live-article-{a.slug}.zip"
    lines = [f"{a.site} live article {a.slug} ({a.date} SGT) for {live}", "",
             "Build with Dev Desk's live builder from source/ (or upload overlay/ as is). ADD-ONLY deploy:",
             "never overwrite or delete .htaccess, IndexNow key .txt, BingSiteAuth.xml, robots.txt, .well-known/, cgi-bin/;",
             "never re-sync existing pages or assets; keep the live light CSS/JS. Then IndexNow the new URLs.", "",
             "source/data/articles/" + src.name + "  sha256 " + hashlib.sha256(src.read_bytes()).hexdigest()[:16]]
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(src, f"source/data/articles/{src.name}")
        for rel in files:
            z.write(out / rel, f"overlay/{rel}")
            lines.append(f"overlay/{rel}  sha256 " + hashlib.sha256((out / rel).read_bytes()).hexdigest()[:16])
        z.writestr("FILES.txt", "\n".join(lines) + "\n")
    print(zp)
    print("new URLs:", " ".join(f"{live}{p}articles/{a.slug}/" for p in LANG_PREFIX))


if __name__ == "__main__":
    main()

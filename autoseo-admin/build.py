"""Build the upload folder for autoseo.my/preview/admin/ (or /admin/ later).
python3 autoseo-admin/build.py  ->  autoseo-admin/dist/ + zip. Demo data is left out; assets get ?v=<hash>."""
import hashlib, json, pathlib, re, shutil, sys, zipfile
here = pathlib.Path(__file__).parent
cfg = json.loads((here / "build-config.json").read_text())
dist = here / "dist"
shutil.rmtree(dist, ignore_errors=True); (dist / "assets").mkdir(parents=True)
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:8]
for f in ["admin.css", "admin.js", "strings.js"]:
    shutil.copy(here / "assets" / f, dist / "assets" / f)
(dist / "config.js").write_text("window.AUTOSEO_ADMIN_CONFIG = " + json.dumps({"google_client_id": cfg["google_client_id"], "api_url": cfg["api_url"]}, indent=2) + ";\n")
html = (here / "index.html").read_text()
html = re.sub(r"<!--DEMO-->.*?<!--/DEMO-->\n", "", html, flags=re.S)
for name, path in [("assets/admin.css", dist / "assets/admin.css"), ("assets/admin.js", dist / "assets/admin.js"), ("assets/strings.js", dist / "assets/strings.js"), ("config.js", dist / "config.js")]:
    html = re.sub(re.escape(name) + r"\?v=[^\"]*", f"{name}?v={h(path)}", html)
(dist / "index.html").write_text(html)
shutil.copy(here / "htaccess.txt", dist / ".htaccess")
# checks
assert 'name="robots" content="noindex' in html, "noindex meta missing"
assert "demo" not in html.lower(), "demo left in"
assert "X-Robots-Tag" in (dist / ".htaccess").read_text()
for p in dist.rglob("*"):
    if p.is_file() and re.search(r"page\s*one|pageonesingapore|edwin", p.read_text(errors="ignore"), re.I):
        sys.exit(f"Page One / Edwin wording found in {p}")
out = here / f"autoseo-admin-preview-{cfg.get('label','build')}.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(dist.rglob("*")):
        if p.is_file(): z.write(p, p.relative_to(dist))
print("built", out, [str(p.relative_to(dist)) for p in sorted(dist.rglob('*')) if p.is_file()])

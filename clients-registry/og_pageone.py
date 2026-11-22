"""Render the /clients share image (1200x630 JPEG < 300 KB) with the computed counts. Usage: python3 og_pageone.py out.jpg"""
import json, sys, os, subprocess, tempfile
from stats import stats
s = stats(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'registry.json'))))
HTML = f"""<html><head><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;800&family=Space+Grotesk:wght@700&display=block" rel="stylesheet">
<style>body{{margin:0;width:1200px;height:630px;background:radial-gradient(circle at 85% 15%,#2a1a5e 0,#0b1f3a 45%,#060b18 100%);color:#fff;font-family:'Plus Jakarta Sans',sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 80px;box-sizing:border-box}}
.b{{font:700 30px 'Space Grotesk';color:#ff8a3d;margin-bottom:26px}} h1{{font:700 74px/1.05 'Space Grotesk';margin:0 0 34px;letter-spacing:-1px}}
.row{{display:flex;gap:22px}} .t{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:22px 28px}}
.n{{font:800 58px 'Plus Jakarta Sans';background:linear-gradient(90deg,#ff3d57,#ff8a3d);-webkit-background-clip:text;color:transparent}} .l{{font-size:24px;color:#c9d2e3}}</style></head>
<body><div class="b">Page One Singapore</div><h1>Websites we build,<br>by industry</h1><div class="row">
<div class="t"><div class="n">{s['po_live']}</div><div class="l">client websites live</div></div>
<div class="t"><div class="n">{s['po_industries']}</div><div class="l">industries</div></div>
<div class="t"><div class="n">+{s['wl_live']}</div><div class="l">white-label sites live</div></div></div></body></html>"""
JS = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
await p.setContent(require('fs').readFileSync(process.argv[2],'utf8'),{waitUntil:'networkidle'});await p.waitForTimeout(500);
await p.screenshot({path:process.argv[3],type:'jpeg',quality:85});await b.close();})();"""
d = tempfile.mkdtemp(); h = os.path.join(d, 'og.html'); j = os.path.join(d, 'og.js')
open(h, 'w').write(HTML); open(j, 'w').write(JS)
subprocess.run(['node', j, h, os.path.abspath(sys.argv[1])], check=True, env=dict(os.environ, NODE_PATH=subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()))

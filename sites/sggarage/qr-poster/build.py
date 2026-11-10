"""Build the Edwin Garage counter QR poster (A4 PDF + PNG preview).

Usage: python3 build.py OUT_DIR
Needs: qrcode[pil], playwright (Chromium pre-installed).
"""
import base64, io, sys, subprocess, pathlib, json
import qrcode
from qrcode.constants import ERROR_CORRECT_M

QR_URL = "https://sgcarworkshop.sg/?utm_source=edwin-garage&utm_medium=qr-poster&utm_campaign=counter"
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out.mkdir(parents=True, exist_ok=True)

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=20, border=4)
qr.add_data(QR_URL)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
buf = io.BytesIO(); img.save(buf, format="PNG")
(out / "qr-sgcarworkshop.png").write_bytes(buf.getvalue())
qr_b64 = base64.b64encode(buf.getvalue()).decode()

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Edwin Garage counter poster</title>
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: #fff; }}
body {{ font-family: Arial, Helvetica, sans-serif; color: #1d1d1b; }}
.page {{ width: 210mm; height: 297mm; padding: 16mm 18mm; display: flex; flex-direction: column;
  border: 6mm solid #f4e9d8; }}
.brand {{ font-size: 13pt; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: #8a5a1c; }}
h1 {{ font-size: 34pt; line-height: 1.12; margin: 6mm 0 5mm; }}
.lead {{ font-size: 16pt; line-height: 1.4; margin: 0 0 4mm; }}
.qrbox {{ margin: 6mm auto 4mm; text-align: center; }}
.qrbox img {{ width: 92mm; height: 92mm; display: block; margin: 0 auto; image-rendering: pixelated; }}
.scan {{ font-size: 18pt; font-weight: 700; margin-top: 3mm; }}
.url {{ font-size: 14pt; color: #444; margin-top: 1mm; }}
.note {{ font-size: 10.5pt; line-height: 1.4; color: #555; margin-top: auto; border-top: 0.4mm solid #e2d3bb; padding-top: 4mm; }}
.nap {{ font-size: 11pt; margin-top: 2mm; color: #333; }}
</style></head><body><div class="page">
<div class="brand">Edwin Garage</div>
<h1>Need a different kind of workshop?</h1>
<p class="lead">We can help with car servicing, repairs, car aircon and accident claim repair here at #01-295.</p>
<p class="lead">If your car needs a specialist for a job we don't do, scan the code to find a nearby workshop or another workshop type.</p>
<div class="qrbox">
  <img src="data:image/png;base64,{qr_b64}" alt="QR code to sgcarworkshop.sg">
  <div class="scan">Scan to search SG Car Workshop</div>
  <div class="url">sgcarworkshop.sg</div>
</div>
<div class="note">SG Car Workshop was founded by Edwin, who owns Edwin Garage, and our listing there is labelled
"Owned by the site's founder". Check every workshop you find there, including us, the same way.
<div class="nap"><b>Edwin Garage Aircon &amp; Car Repair</b> · Blk 5032 Ang Mo Kio Industrial Park 2 #01-295, Singapore 569535</div></div>
</div></body></html>"""
(out / "poster.html").write_text(html, encoding="utf-8")

js = """
const { chromium } = require('playwright');
(async () => {
  const [html, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + html);
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await p.screenshot({ path: png, fullPage: false });
  await b.close();
})();
"""
jsf = out / "_render.js"; jsf.write_text(js)
import os
env = dict(os.environ, NODE_PATH=subprocess.check_output(["npm", "root", "-g"]).decode().strip())
subprocess.run(["node", str(jsf), str((out / "poster.html").resolve()), str(out / "poster.pdf"), str(out / "poster-preview.png")], check=True, env=env, cwd="/tmp")
jsf.unlink()
print(json.dumps({"qr_url": QR_URL, "out": str(out)}))

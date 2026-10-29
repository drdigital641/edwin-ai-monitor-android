// Generates favicon / icons / og.jpg from assets/emblem.svg (run once; outputs are committed in assets/)
const {chromium}=require('playwright');const fs=require('fs');
const A='/mnt/project-files/sh-auto-parts/assets/';
const svg=fs.readFileSync(A+'emblem.svg','utf8');
(async()=>{const b=await chromium.launch();
async function shot(html,w,h,out,opts={}){const p=await b.newPage({viewport:{width:w,height:h}});await p.setContent(html);await p.screenshot({path:out,omitBackground:!!opts.t});await p.close()}
const wrap=(bg,pad,size)=>`<body style="margin:0;background:${bg};width:${size}px;height:${size}px;display:grid;place-items:center"><div style="width:${size-2*pad}px;height:${size-2*pad}px">${svg.replace('<svg ','<svg width="100%" height="100%" ')}</div></body>`;
await shot(wrap('transparent',2,48),48,48,A+'favicon-48.png',{t:1});
await shot(wrap('#0A0A0C',34,192),192,192,A+'icon-192.png');
await shot(wrap('#0A0A0C',90,512),512,512,A+'icon-512.png');
await shot(wrap('#0A0A0C',26,180),180,180,A+'apple-touch-icon.png');
const og=`<body style="margin:0;width:1200px;height:630px;background:radial-gradient(900px 500px at 85% 0%,rgba(215,38,46,.28),transparent 60%),linear-gradient(135deg,#0A0A0C 0%,#16161b 55%,#0A0A0C 100%);font-family:Arial,Helvetica,sans-serif;color:#fff;position:relative;overflow:hidden">
<div style="position:absolute;left:0;top:0;width:12px;height:630px;background:#D7262E"></div>
<div style="position:absolute;left:90px;top:150px;width:220px;height:220px">${svg.replace('<svg ','<svg width="100%" height="100%" ')}</div>
<div style="position:absolute;left:350px;top:150px;font-weight:900;font-style:italic;font-size:112px;line-height:.95;letter-spacing:-2px">SH AUTO<br>PARTS</div>
<div style="position:absolute;left:354px;top:372px;width:120px;height:4px;background:#D7262E"></div>
<div style="position:absolute;left:354px;top:400px;font-size:30px;letter-spacing:6px;color:#C9C9CF;text-transform:uppercase">China Car Parts Supplier</div>
<div style="position:absolute;left:90px;top:528px;font-size:38px;font-weight:700">China &amp; EV car parts in Singapore</div>
<div style="position:absolute;right:60px;bottom:44px;font-size:22px;color:#8d8d97">Workshops &amp; car owners</div></body>`;
await shot(og,1200,630,'/tmp/sh-scratch/og.png');
await b.close()})();

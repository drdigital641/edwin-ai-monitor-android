// Generates logo/favicon/icons/og.jpg from assets/mark.svg (outputs are committed in assets/)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const A=path.join(__dirname,'..','assets')+'/';
const svg=fs.readFileSync(A+'mark.svg','utf8').replace('<svg ','<svg width="100%" height="100%" ');
(async()=>{const b=await chromium.launch();
async function shot(html,w,h,out,t){const p=await b.newPage({viewport:{width:w,height:h}});await p.setContent(html);await p.screenshot({path:out,omitBackground:!!t});await p.close()}
const tile=(size,pad,bg)=>`<body style="margin:0;background:${bg};width:${size}px;height:${size}px;display:grid;place-items:center"><div style="width:${size-2*pad}px;height:${size-2*pad}px">${svg}</div></body>`;
await shot(tile(48,0,'transparent'),48,48,A+'favicon-48.png',1);
await shot(tile(192,0,'transparent'),192,192,A+'icon-192.png',1);
await shot(tile(512,0,'transparent'),512,512,A+'icon-512.png',1);
await shot(tile(180,0,'#07090B'),180,180,A+'apple-touch-icon.png');
await shot(tile(96,0,'transparent'),96,96,A+'logo-96.png',1);
const F="'Arial Black','Helvetica Neue',Arial,sans-serif";
const og=`<body style="margin:0;width:1200px;height:630px;background:radial-gradient(900px 520px at 88% -5%,rgba(25,227,177,.30),transparent 60%),radial-gradient(700px 420px at 0% 100%,rgba(18,184,230,.16),transparent 60%),linear-gradient(135deg,#07090B 0%,#0F1518 55%,#07090B 100%);font-family:${F};color:#fff;position:relative;overflow:hidden">
<div style="position:absolute;left:0;top:0;width:12px;height:630px;background:linear-gradient(#3DF2C4,#12B8E6)"></div>
<div style="position:absolute;left:92px;top:130px;width:230px;height:230px">${svg}</div>
<div style="position:absolute;left:364px;top:128px;font-weight:900;font-style:italic;font-size:104px;line-height:.98;letter-spacing:-2px">EV BODY<br>PARTS</div>
<div style="position:absolute;left:368px;top:350px;width:120px;height:4px;background:#19E3B1"></div>
<div style="position:absolute;left:368px;top:378px;font-family:Arial,sans-serif;font-size:27px;letter-spacing:5px;color:#B8C6C3;text-transform:uppercase">evbodyparts.sg</div>
<div style="position:absolute;left:92px;top:500px;font-family:Arial,sans-serif;font-size:40px;font-weight:700">Body parts for China &amp; EV cars in Singapore</div>
<div style="position:absolute;left:92px;top:556px;font-family:Arial,sans-serif;font-size:24px;color:#8FA19D">For workshops &amp; car owners</div></body>`;
await shot(og,1200,630,'/tmp/ev-og.png');
await b.close();
})();

const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const lines=fs.readFileSync('seo-check-2026-11-27/urls.txt','utf8').trim().split('\n');
fs.mkdirSync('seo-check-2026-11-27/shots',{recursive:true});const out=[];
const b=await chromium.launch();
for(const l of lines){const [label,url]=l.trim().split(/\s+/);
for(const w of [390,1280]){const p=await b.newPage({viewport:{width:w,height:w===390?844:900}});
let st='';try{const r=await p.goto(url,{waitUntil:'networkidle',timeout:45000});st=r?r.status():'none';}catch(e){st='ERR '+e.message.slice(0,80);}
await p.waitForTimeout(800);
const info=await p.evaluate(()=>({hs:document.documentElement.scrollWidth>innerWidth+1,sw:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight,robots:(document.querySelector('meta[name=robots]')||{}).content||'',canon:(document.querySelector('link[rel=canonical]')||{}).href||'',ld:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>{try{JSON.parse(s.textContent);return 'ok'}catch(e){return 'BAD'}}).join(',')})).catch(e=>({err:String(e)}));
await p.screenshot({path:`seo-check-2026-11-27/shots/${label}-${w}.jpg`,type:'jpeg',quality:55,fullPage:true,clip:undefined}).catch(()=>{});
out.push({label,url,w,status:st,...info});await p.close();}}
await b.close();fs.writeFileSync('seo-check-2026-11-27/shots/report.json',JSON.stringify(out,null,1));})();

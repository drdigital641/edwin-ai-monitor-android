// Live check of batteryrescue.sg launch promo (7 Nov 2026). Runs on a GitHub runner.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const out=[];const log=s=>{console.log(s);out.push(s)};
fs.mkdirSync('shots',{recursive:true});fs.mkdirSync('live',{recursive:true});
const sm=await (await fetch('https://batteryrescue.sg/sitemap.xml?x='+Date.now())).text();
const urls=[...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map(x=>x[1]);log('sitemap urls '+urls.length);
let bad=0;
for(const u of urls.concat(['https://batteryrescue.sg/llms.txt'])){const r=await fetch(u+'?x='+Date.now());const t=await r.text();if(r.status!==200){bad++;log('STATUS '+r.status+' '+u)}
 fs.writeFileSync('live/'+(u.replace('https://batteryrescue.sg/','').replace(/\//g,'_')||'home')+(u.endsWith('.txt')?'':'.html'),t)}
log('non-200: '+bad);
const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route(/functions\/track/,r=>r.fulfill({status:200,body:'{}'}));
await p.goto('https://batteryrescue.sg/?p1test=1&v='+Date.now(),{waitUntil:'networkidle'});await p.waitForTimeout(1000);
await p.screenshot({path:'shots/promo-home.png'});
log('hero line: '+(await p.textContent('.where')).replace(/\s+/g,' '));
await p.fill('#s-in','Honda Vezel');await p.waitForTimeout(700);const li=await p.$('#s-car .sug li');if(li){await li.click();await p.waitForTimeout(700)}
await (await p.$('#s-res')).scrollIntoViewIfNeeded();await p.evaluate(()=>scrollBy(0,120));await p.waitForTimeout(400);await p.screenshot({path:'shots/promo-calculator.png'});
log('calculator: '+(await p.textContent('#s-res')).replace(/\s+/g,' ').slice(0,300));
const line=async(u,sel)=>{await p.goto(u+'?v='+Date.now(),{waitUntil:'networkidle'});return (await p.textContent(sel)).replace(/\s+/g,' ').trim()};
log('NS40ZL tier: '+await line('https://batteryrescue.sg/battery/ns40zl/','.tier.day'));await p.screenshot({path:'shots/promo-battery-ns40zl.png'});
log('NS60L tier: '+await line('https://batteryrescue.sg/battery/ns60l/','.tier.day'));
log('AGM LN5 tier: '+await line('https://batteryrescue.sg/battery/agm-ln5/','.tier.day'));
log('NS40ZL night: '+await line('https://batteryrescue.sg/battery/ns40zl/','.tier.night'));
await p.goto('https://batteryrescue.sg/prices/',{waitUntil:'networkidle'});const t=await p.$('.tbl');await t.scrollIntoViewIfNeeded();await p.waitForTimeout(300);await p.screenshot({path:'shots/promo-prices.png'});
log('prices page scrollWidth '+await p.evaluate(()=>document.documentElement.scrollWidth));
await p.goto('https://batteryrescue.sg/rescue/yishun/',{waitUntil:'networkidle'});await p.waitForTimeout(300);await p.screenshot({path:'shots/promo-area-yishun.png'});
const raw=fs.readFileSync('live/battery_ns40zl_.html','utf8');
const ld=[...raw.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map(x=>x[1]).join('');
log('ns40zl schema offers: '+JSON.stringify([...ld.matchAll(/"name": "([^"]*)", "price": "([^"]*)"/g)].map(x=>x[1]+'='+x[2])));
log('schema has <s> or was-price fields: '+(/<s>|priceSpecification|"was|169\.90/.test(ld)));
log('page errors: '+JSON.stringify(errs));
fs.writeFileSync('shots/result.txt',out.join('\n'));await b.close()})();

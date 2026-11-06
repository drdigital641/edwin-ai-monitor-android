// Live check of batteryrescue.sg homepage hero (6 Nov 2026): 390px screenshots + checks. Runs on a GitHub runner.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const out=[];const log=s=>{console.log(s);out.push(s)};
fs.mkdirSync('shots',{recursive:true});
try{
const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
let beacons=0;await p.route(/functions\/track/,r=>{beacons++;r.fulfill({status:200,body:'{}'})});
await p.route(/wa\.me|api\.whatsapp/,r=>r.abort());
const r=await p.goto('https://batteryrescue.sg/?p1test=1&v='+Date.now(),{waitUntil:'networkidle'});log('home status '+r.status());
await p.waitForTimeout(1200);
await p.screenshot({path:'shots/live-390-1.png'});
log('h1: '+(await p.textContent('h1')).trim());
log('phone pill: '+(await p.$$('.top .hot')).length+', sticky bar: '+(await p.$$('.act')).length+', bottom nav links: '+(await p.$$('.tabs a')).length);
log('cards: '+(await p.$$eval('.pk',x=>x.map(e=>e.innerText.replace(/\s+/g,' ')).join(' | '))));
log('help buttons: '+(await p.$$eval('#help a',x=>x.map(e=>e.className+' '+e.getAttribute('href')).join(' , '))));
log('animations: '+await p.evaluate(()=>{const g=s=>{const e=document.querySelector(s);return e?getComputedStyle(e).animationName:'missing'};return g('.siren .beam')+'/'+g('.pk.red')+'/'+g('.tick')}));
await p.evaluate(()=>scrollBy(0,760));await p.waitForTimeout(700);await p.screenshot({path:'shots/live-390-2.png'});
await p.evaluate(()=>scrollTo(0,0));
await p.evaluate(()=>{document.querySelector('#help a[href^="tel:"]').addEventListener('click',e=>e.preventDefault())});
await p.click('#help a[href^="tel:"]');await p.waitForTimeout(900);log('track beacons after Call tap (test mode): '+beacons);
await p.click('.pk.red');await p.waitForTimeout(1000);log('after red tap, help in view: '+await p.evaluate(()=>{const r=document.querySelector('#help').getBoundingClientRect();return r.top>=0&&r.top<innerHeight}));
await p.click('.pk.grn');await p.waitForTimeout(800);log('after green tap, compare visible: '+await p.evaluate(()=>{const c=document.querySelector('[data-panel=compare]');return c&&!c.hidden})+' hash '+await p.evaluate(()=>location.hash));
await p.screenshot({path:'shots/live-390-compare.png'});
await p.goto('https://batteryrescue.sg/?p1test=1&v=2'+Date.now(),{waitUntil:'networkidle'});await p.waitForTimeout(800);
log('price link href: '+await p.getAttribute('.where a','href'));
await p.click('.where a');await p.waitForTimeout(1300);
log('after price link tap: box in view '+await p.evaluate(()=>{const r=document.querySelector('#car-price').getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight})+', input focused '+await p.evaluate(()=>document.activeElement&&document.activeElement.id)+', compare hidden '+await p.evaluate(()=>document.querySelector('[data-panel=compare]').hidden));
await p.screenshot({path:'shots/live-390-price-link.png'});
const raw=await (await fetch('https://batteryrescue.sg/?raw='+Date.now())).text();
log('raw HTML has H1 text: '+/<h1[^>]*>[\s\S]*What.s happening with your car\?<\/h1>/.test(raw)+', robots noindex: '+/noindex/i.test(raw)+', canonical: '+(raw.match(/rel="canonical" href="([^"]+)"/)||[])[1]);
const types=[...raw.matchAll(/"@type":\s*"([A-Za-z]+)"/g)].map(x=>x[1]);log('schema types on home: '+[...new Set(types)].join(','));
log('NAP on home: name '+raw.includes('Battery Rescue SG')+', tel +6581259169 '+raw.includes('+6581259169')+', 8125 9169 '+raw.includes('8125 9169'));
for(const u of ['rescue/','articles/','llms.txt']){const t=await (await fetch('https://batteryrescue.sg/'+u+'?r='+Date.now())).text();log(u+' islandwide wording: '+/all of Singapore|anywhere in Singapore|All of Singapore/.test(t)+', old 2027 line gone: '+!/More areas coming in 2027/.test(t))}
const hdr=await fetch('https://batteryrescue.sg/');log('X-Robots-Tag header: '+hdr.headers.get('x-robots-tag'));
log('page errors: '+JSON.stringify(errs));
const rm=await b.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});await rm.goto('https://batteryrescue.sg/');log('reduced-motion red card animation: '+await rm.evaluate(()=>getComputedStyle(document.querySelector('.pk.red')).animationName));
const d=await b.newPage({viewport:{width:1280,height:800}});await d.goto('https://batteryrescue.sg/');await d.waitForTimeout(800);await d.screenshot({path:'shots/live-desktop.png'});
}catch(e){log('ERROR '+e.message)}
const q=await b.newPage();
for(const a of ['woodlands','sembawang','yishun','ang-mo-kio','yio-chu-kang','hougang','sengkang','punggol']){try{const x=await q.goto('https://batteryrescue.sg/rescue/'+a+'/');log('area '+a+' '+x.status())}catch(e){log('area '+a+' ERR '+e.message)}}
for(const u of ['rescue/','prices/','outlets/','sitemap.xml']){try{const x=await q.goto('https://batteryrescue.sg/'+u);log(u+' '+x.status())}catch(e){log(u+' ERR')}}
fs.writeFileSync('shots/result.txt',out.join('\n'));await b.close()})();

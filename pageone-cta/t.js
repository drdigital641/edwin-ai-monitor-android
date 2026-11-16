const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const R='/home/user/edwin-ai-monitor-android/pageone-cta/';
const map={};for(const b of ['b1','b2','b3'])(function walk(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f);if(fs.statSync(p).isDirectory())walk(p);else map[path.relative(R+'sync/'+b,p)]=p}})(R+'sync/'+b);
(async()=>{const br=await chromium.launch();let bad=0,clicks=0,pagesN=0;
for(const rel of Object.keys(map)){const ctx=await br.newContext();await ctx.addInitScript(()=>{Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false});window.open=function(){return {}}});
 const posts=[];await ctx.route('**/*',async r=>{const u=new URL(r.request().url());
  if(u.hostname==='base44.app'){if(r.request().method()==='POST'){const b=JSON.parse(r.request().postData()||'{}');if(b.entity==='CtaClick')posts.push(b)}return r.fulfill({status:204,body:''})}
  if(u.hostname!=='pageonesingapore.com')return r.abort();
  let p=u.pathname.slice(1);if(p===''||p.endsWith('/'))p+='index.html';
  let f=map[p]||(p==='p1-cta.js'?R+'p1-cta.js':R+'live/'+p);if(!fs.existsSync(f))f=R+'live/'+p;
  if(!fs.existsSync(f))return r.fulfill({status:404,body:''});
  const ct=p.endsWith('.js')?'application/javascript':p.endsWith('.css')?'text/css':'text/html';return r.fulfill({status:200,contentType:ct,body:fs.readFileSync(f)})});
 const pg=await ctx.newPage();let url='https://pageonesingapore.com/'+rel.replace(/index\.html$/,'');await pg.goto(url,{waitUntil:'load'});await pg.waitForTimeout(300);pagesN++;
 const ok=await pg.evaluate(()=>[!!window.__p1cta,typeof window.p1Track]);if(!ok[0]||ok[1]!=='function'){console.log('NOTRACK',rel,ok);bad++}
 const n=await pg.$$eval('a[href*="wa.me/"],a[href^="tel:"],a[href^="mailto:"]',as=>as.length);
 for(let i=0;i<n;i++){const before=posts.length;const exp=await pg.$$eval('a[href*="wa.me/"],a[href^="tel:"],a[href^="mailto:"]',(as,i)=>{const a=as[i];a.addEventListener('click',e=>e.preventDefault(),{once:true});const d=a.getAttribute('data-cta');a.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));return d},i);
  await pg.waitForTimeout(1600);clicks++;const got=posts.slice(before);
  if(got.length!==1||got[0].cta_type!==exp){bad++;if(bad<15)console.log('MISMATCH',rel,i,exp,JSON.stringify(got.map(g=>g.cta_type)))}}
 await ctx.close()}
console.log('pages',pagesN,'clicks',clicks,'bad',bad);await br.close()})();

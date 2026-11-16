const {chromium}=require('playwright');const fs=require('fs');const R='/home/user/edwin-ai-monitor-android/pageone-cta/';
(async()=>{const br=await chromium.launch();
async function run(rel,fn,nowd){const ctx=await br.newContext();if(!nowd)await ctx.addInitScript(()=>{Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false})});await ctx.addInitScript(()=>{window.open=function(){return {}}});
const posts=[];await ctx.route('**/*',async r=>{const u=new URL(r.request().url());if(u.hostname==='base44.app'){if(r.request().method()==='POST'){const b=JSON.parse(r.request().postData()||'{}');if(b.entity==='CtaClick')posts.push(b.cta_type+(b.bot?'(bot)':'')+(b.test?'(test)':''))}return r.fulfill({status:204,body:''})}
if(u.hostname!=='pageonesingapore.com')return r.abort();let p=u.pathname.slice(1);if(p===''||p.endsWith('/'))p+='index.html';
let f=['b1','b2','b3'].map(b=>R+'sync/'+b+'/'+p).find(x=>fs.existsSync(x))||(p==='p1-cta.js'?R+'p1-cta.js':R+'live/'+p);if(!fs.existsSync(f))return r.fulfill({status:404,body:''});
return r.fulfill({status:200,contentType:p.endsWith('.js')?'application/javascript':p.endsWith('.css')?'text/css':'text/html',body:fs.readFileSync(f)})});
const pg=await ctx.newPage();await pg.goto('https://pageonesingapore.com/'+rel,{waitUntil:'load'});await pg.waitForTimeout(300);await fn(pg);await pg.waitForTimeout(1800);console.log(rel,'->',JSON.stringify(posts));await ctx.close()}
const addClick=(html)=>async pg=>{await pg.evaluate(h=>{const d=document.createElement('div');d.innerHTML=h;document.querySelector('main,body').appendChild(d);const a=d.querySelector('a');a.addEventListener('click',e=>e.preventDefault());a.click()},html)};
await run('',addClick('<a href="tel:+6597856612" data-cta="call">Call</a>'));
await run('',addClick('<a href="mailto:x@example.com" data-cta="email">Mail</a>'));
await run('signup/',async pg=>{await pg.fill('#signup-form [name=name]','T');await pg.fill('#signup-form [name=business]','B');await pg.click('#signup-form [type=submit]')});
await run('signup/',async pg=>{await pg.click('#signup-form [type=submit]')});
await run('contact/',async pg=>{await pg.fill('#lead-form [name=name]','T');await pg.click('#lead-form [type=submit]')});
await run('',async pg=>{await pg.click('#chat-launcher');await pg.waitForTimeout(200);await pg.evaluate(()=>{const a=document.querySelector('.chat-reply');a.addEventListener('click',e=>e.preventDefault());a.click()})});
await run('?p1test=1',addClick('<a href="tel:+6597856612" data-cta="call">Call</a>'));
await run('',addClick('<a href="tel:+6597856612" data-cta="call">Call</a>'),true);
await br.close()})();

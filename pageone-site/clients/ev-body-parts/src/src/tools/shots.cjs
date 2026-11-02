// node tools/shots.cjs <site-dir> <out-dir> <mode: live|fail|snapshot>
// Serves the built site locally, mocks the Base44 REST read with Playwright route interception (the sandbox has no internet),
// checks the live-read code path, and takes phone (390x844) + desktop (1440x900) screenshots.
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const SITE=process.argv[2]||'/tmp/ev-site',OUT=process.argv[3]||'/tmp/ev-shots',MODE=process.argv[4]||'live';const PORT=8792+(MODE==='live'?0:MODE==='fail'?1:2);
fs.mkdirSync(OUT,{recursive:true});
const db=n=>JSON.parse(fs.readFileSync(__dirname+'/../db/'+n+'.json','utf8'));
const P=(k,m,p,title,x)=>Object.assign({key:k,m,p,title,status:'published',created_date:'2026-10-31T11:00:00',photos:[]},x||{});
const LIVE=[P('tesla-model-y-tail-lamp-left','tesla-model-y','tail-lamp','Tesla Model Y Tail Lamp (Left)',{side:'L',price:380,stock:'in'}),
 P('tesla-model-y-side-mirror-right','tesla-model-y','side-mirror','Tesla Model Y Side Mirror (Right)',{side:'R',price:120.5,photos:['b44photo:live1']}),
 P('byd-atto-3-headlamp','byd-atto-3','headlamp','BYD Atto 3 Headlamp',{stock:'order'}),
 P('zeekr-001-bonnet','zeekr-001','bonnet','Zeekr 001 Bonnet',{})];
const px='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==';
const seen=[];
(async()=>{
 const srv=spawn('python3',['-m','http.server',String(PORT),'-d',SITE],{stdio:'ignore'});
 await new Promise(r=>setTimeout(r,1200));
 const b=await chromium.launch();
 const VP={phone:{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true},desktop:{viewport:{width:1440,height:900}}};
 let fails=0; const ok=(c,m)=>{console.log((c?'OK   ':'FAIL ')+m);if(!c)fails++};
 for(const [name,opt] of Object.entries(VP)){
  const ctx=await b.newContext(opt);
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1|localhost)/,r=>{
   const u=r.request().url();
   if(/base44\.app\/api\/apps\/6ae5c57dbb2270677873e207\/entities\//.test(u)){
    seen.push(r.request().method()+' '+u+' hdr X-App-Id='+r.request().headers()['x-app-id']);
    if(MODE==='fail')return r.abort();
    const ent=u.split('/entities/')[1].split('?')[0];
    const body=ent==='EvBrand'?db('brands'):ent==='EvCar'?db('cars'):ent==='EvProduct'?LIVE:ent==='EvPhoto'?[{group:'live1',i:0,n:1,data:px}]:[];
    return r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify(body)});
   }
   r.abort();
  });
  const p=await ctx.newPage();const U='http://127.0.0.1:'+PORT+'/';
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.addInitScript(()=>{window.__opened=[];window.open=(u)=>{window.__opened.push(u);return {}}});
  const shot=async(n,full)=>{await p.waitForTimeout(600);await p.screenshot({path:`${OUT}/v2-${name}-${n}.jpg`,type:'jpeg',quality:80,fullPage:!!full})};
  const reveal=()=>p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));
  await p.goto(U);await p.waitForTimeout(900);await reveal();await shot('home-top');
  await p.goto(U);await reveal();await p.waitForTimeout(500);await shot('home-full',true);
  ok(await p.evaluate(()=>!document.querySelector('.mbar')),'no bottom 3-button bar');
  ok(await p.evaluate(()=>getComputedStyle(document.querySelector('.fab')).position==='fixed'&&document.querySelectorAll('.fab').length===1),'one floating WhatsApp button');
  await p.click('.burger');await p.waitForTimeout(500);await shot('menu');
  ok(await p.evaluate(()=>getComputedStyle(document.querySelector('.fab')).opacity==='0'),'fab hidden while menu open');
  ok(await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.textContent.trim()).join('|')),'menu items listed');
  await p.keyboard.press('Escape');
  await p.goto(U+'catalogue/');await p.fill('#cq-q','tesla model y side mirror');await p.waitForTimeout(900);await shot('catalogue-search',true);
  const t=await p.evaluate(()=>[...document.querySelectorAll('#cat-res .rc h3')].map(h=>h.textContent));
  ok(/Side Mirror/.test(t[0]||''),'search top result: '+t[0]);
  await p.goto(U+'brands/tesla/model-y/');await reveal();await p.waitForTimeout(900);await shot('car-model-y');
  // cart: one listed product (if any) + one Ask-us chip
  const hasProd=await p.evaluate(()=>!!document.querySelector('.rc [data-add]'));
  if(hasProd)await p.click('.rc [data-add]');
  await p.click('.chipbtn');await p.waitForTimeout(300);
  await p.click('.chipbtn:nth-of-type(3)');await p.waitForTimeout(300);
  const bd=await p.evaluate(()=>document.querySelector('[data-cart-count]').textContent);ok(+bd>=2,'cart badge count '+bd);
  await p.goto(U);await p.waitForTimeout(500);
  ok((await p.evaluate(()=>document.querySelector('[data-cart-count]').textContent))===bd,'badge persists across pages: '+bd);
  await p.click('.cartbtn');await p.waitForTimeout(600);await shot('cart');
  const rows=await p.evaluate(()=>document.querySelectorAll('.cdr .cl li').length);ok(rows>=2,'cart drawer rows '+rows);
  await p.fill('.cdr input[name=name]','Test Workshop');await p.fill('.cdr textarea','2022 car, photo to follow');
  await p.click('[data-send]');await p.waitForTimeout(300);
  const wa=await p.evaluate(()=>decodeURIComponent((window.__opened[0]||'')));
  ok(/^https:\/\/wa\.me\/6589976612\?text=Hi EV Body Parts/.test(wa),'WhatsApp order link');console.log(wa.split('\n').map(l=>'     | '+l).join('\n'));
  ok(await p.evaluate(()=>!!document.querySelector('[data-clear]')),'Clear cart offered after sending');
  await p.click('[data-clear]');ok((await p.evaluate(()=>document.querySelector('[data-cart-count]').hidden)),'cart cleared, badge hidden');
  const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);ok(!ov,name+': no horizontal overflow');
  ok(errs.length===0,name+' js errors: '+(errs.join(' | ')||'none'));
  await ctx.close();
 }
 console.log('REST requests seen ('+MODE+'): '+seen.length);[...new Set(seen)].slice(0,5).forEach(s=>console.log('  '+s.slice(0,230)));
 await b.close();srv.kill();process.exit(fails?1:0);
})();

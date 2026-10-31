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
  const shot=async(n,full)=>{await p.waitForTimeout(600);await p.screenshot({path:`${OUT}/${name}-${n}.jpg`,type:'jpeg',quality:80,fullPage:!!full})};
  const reveal=()=>p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));
  await p.goto(U);await p.waitForTimeout(900);await reveal();await shot('home-top');
  const rail=await p.evaluate(()=>{const s=document.querySelector('[data-new-sec]');return {hidden:s.hidden,cards:s.querySelectorAll('.rc').length}});
  if(MODE==='live')ok(!rail.hidden&&rail.cards===4,`home "Newly added" rail shows live products (${rail.cards} cards)`);else ok(true,`home rail hidden=${rail.hidden} cards=${rail.cards}`);
  await p.evaluate(()=>window.scrollTo(0,document.querySelector('[data-new-sec]').getBoundingClientRect().top+scrollY-70));await shot('home-new');
  await p.goto(U);await reveal();await p.waitForTimeout(500);await shot('home-full',true);
  await p.goto(U+'catalogue/');await p.fill('#cq-q','tesla model y side mirror');await p.waitForTimeout(900);await shot('catalogue-search',true);
  const t=await p.evaluate(()=>[...document.querySelectorAll('#cat-res .rc h3')].map(h=>h.textContent));
  if(MODE==='live'){ok(/Side Mirror/.test(t[0]||'')&&!/Tail/.test(t[0]),'live-only product is top search result: '+t[0]);
   const price=await p.evaluate(()=>document.querySelector('#cat-res .rc .price')?.textContent);ok(price==='S$120.50','price shown S$120.50: '+price);
   const im=await p.evaluate(()=>{const i=document.querySelector('#cat-res .rc img');return i&&i.src.slice(0,22)});ok(im==='data:image/png;base64,','b44photo chunks joined and shown: '+im);}
  else ok(/Side Mirror/.test(t[0]||''),'fallback Ask-us card on search: '+t[0]);
  await p.goto(U+'catalogue/?q='+encodeURIComponent('Tesla Model Y tail lamp'));await p.waitForTimeout(800);await shot('catalogue-query');
  await p.goto(U+'brands/tesla/');await reveal();await p.waitForTimeout(800);await shot('brand-tesla');
  await p.goto(U+'brands/tesla/model-y/');await reveal();await p.waitForTimeout(800);await shot('car-model-y');
  if(fs.existsSync(SITE+'/brands/tesla/model-y/tail-lamp-left/index.html')){await p.goto(U+'brands/tesla/model-y/tail-lamp-left/');await reveal();await shot('product');}
  await p.goto(U+'enquiry/?q='+encodeURIComponent('Tesla Model Y Tail Lamp'));await shot('enquiry');
  if(name==='phone'){await p.goto(U);await p.click('.burger');await shot('menu')}
  const ov=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);ok(!ov,name+': no horizontal overflow');
  ok(errs.length===0,name+' js errors: '+(errs.join(' | ')||'none'));
  await ctx.close();
 }
 console.log('REST requests seen ('+MODE+'): '+seen.length);[...new Set(seen)].slice(0,5).forEach(s=>console.log('  '+s.slice(0,230)));
 await b.close();srv.kill();process.exit(fails?1:0);
})();

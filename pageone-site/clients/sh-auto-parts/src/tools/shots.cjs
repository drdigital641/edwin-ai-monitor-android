// node tools/shots.cjs [outdir]  - serves site/ locally and takes phone (390x844) + desktop (1440x900) screenshots
const {chromium}=require('playwright');const {spawn}=require('child_process');
const OUT=process.argv[2]||'/mnt/project-files/sh-auto-parts/screens';const PORT=8791;
(async()=>{
 const srv=spawn('python3',['-m','http.server',String(PORT),'-d','/mnt/project-files/sh-auto-parts/site'],{stdio:'ignore'});
 await new Promise(r=>setTimeout(r,1200));
 const b=await chromium.launch();
 const VP={phone:{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true},desktop:{viewport:{width:1440,height:900}}};
 for(const [name,opt] of Object.entries(VP)){
  const ctx=await b.newContext(opt);
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1|localhost)/,r=>r.abort());
  const p=await ctx.newPage();const U='http://127.0.0.1:'+PORT+'/';
  const shot=async(n,full)=>{await p.waitForTimeout(500);await p.screenshot({path:`${OUT}/${name}-${n}.jpg`,type:'jpeg',quality:80,fullPage:!!full})};
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto(U);await shot('home-top');
  await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));
  await p.evaluate(()=>window.scrollTo(0,document.querySelector('#hq-res').getBoundingClientRect().top+scrollY-20));
  await p.fill('#hq-q','Tesla Model Y tail lamp');await p.waitForTimeout(400);await shot('home-search');
  await p.evaluate(()=>window.scrollTo(0,document.querySelector('.cgrid').getBoundingClientRect().top+scrollY-80));await shot('home-scrolled');
  await p.evaluate(()=>window.scrollTo(0,document.querySelector('.two').getBoundingClientRect().top+scrollY-80));await shot('home-scrolled2');
  await p.goto(U);await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));await p.waitForTimeout(300);await shot('home-full',true);
  await p.goto(U+'catalogue/?q='+encodeURIComponent('Tesla Model Y tail lamp'));await shot('catalogue-query');
  await p.goto(U+'catalogue/');await shot('catalogue-all');
  await p.goto(U+'brands/tesla/');await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));await shot('brand-tesla');
  await p.goto(U+'parts/lamps-lights/');await shot('parts-lamps');
  await p.goto(U+'articles/tesla-model-y-tail-lamp-what-to-send/');await shot('article');
  await p.goto(U+'enquiry/?q='+encodeURIComponent('Tail Lamp for Tesla Model Y'));await shot('enquiry');
  if(name==='phone'){await p.goto(U);await p.click('.burger');await shot('menu')}
  await p.goto(U+'staff/');await shot('staff-login');
  await p.fill('input[name=n]','Demo Staff');await p.fill('input[name=p]','2468');await p.click('button[type=submit]');await shot('staff-overview');
  await p.click('[data-tab=catalogue]');await p.fill('#sq','tesla model y');await p.waitForTimeout(300);await shot('staff-catalogue');
  console.log(name,'js errors:',errs.length?errs:'none');
  await ctx.close();
 }
 await b.close();srv.kill();
})();

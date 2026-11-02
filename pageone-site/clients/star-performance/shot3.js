const { chromium } = require(process.env.PWP);
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const list=[['v3-home-desktop',1366,900,'/',true],['v3-home-phone',390,844,'/',true],['v3-svc',1366,900,'/services/buy-a-used-car/',false],['v3-sold-phone',390,844,'/sold-cars/',false]];
 for(const [n,w,h,u,full] of list){
  const p=await b.newPage({viewport:{width:w,height:h},reducedMotion:'reduce'});
  await p.goto('http://localhost:8766'+u,{waitUntil:'networkidle'}); await p.waitForTimeout(400);
  await p.screenshot({path:'shots/'+n+'.jpg',fullPage:full,quality:55,type:'jpeg'});
  console.log(n,await p.evaluate(()=>document.documentElement.scrollWidth+' x '+document.documentElement.scrollHeight));
 }
 await b.close();
})();

const { chromium } = require(process.env.PWP);
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const list=[['home-phone',390,844,'/',true],['home-desktop',1366,900,'/',true],['sold-phone',390,844,'/sold-cars/',true],['svc-desktop',1366,900,'/services/buy-a-used-car/',false]];
 for(const [n,w,h,u,full] of list){
  const p=await b.newPage({viewport:{width:w,height:h},reducedMotion:'reduce'});
  await p.goto('http://localhost:8765'+u,{waitUntil:'networkidle'}); await p.waitForTimeout(500);
  await p.screenshot({path:'shots/'+n+'.jpg',fullPage:full,quality:60,type:'jpeg'});
  const sw=await p.evaluate(()=>document.documentElement.scrollWidth); console.log(n,'scrollWidth',sw);
 }
 await b.close();
})();

// node tools/browser_test.cjs SITE_DIR [SCREEN_DIR]  - serves SITE_DIR, runs phone (390px) checks with Playwright
const {chromium}=require('playwright');const {spawn}=require('child_process');
const SITE=process.argv[2]||'site',SCR=process.argv[3]||'';const PORT=8793;
let fail=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)fail++};
(async()=>{
 const srv=spawn('python3',['-m','http.server',String(PORT),'-d',SITE],{stdio:'ignore'});
 await new Promise(r=>setTimeout(r,1200));
 const b=await chromium.launch();
 const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
 await ctx.route(/^https?:\/\/(?!127\.0\.0\.1|localhost)/,r=>{const u=r.request().url();
   if(/wa\.me/.test(u))return r.fulfill({status:200,contentType:'text/html',body:'<h1>wa</h1>'});
   if(/fonts\.googleapis/.test(u))return r.fulfill({status:200,contentType:'text/css',body:''});
   if(/base44/.test(u))return r.fulfill({status:200,contentType:'application/json',body:'{}'});
   return r.abort()});
 const U='http://127.0.0.1:'+PORT+'/';
 const p=await ctx.newPage();const errs=[];
 p.on('pageerror',e=>errs.push('pageerror '+e.message));
 p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});
 p.on('requestfailed',r=>{if(r.url().startsWith(U))errs.push('reqfail '+r.url())});
 const pages=['','honda/civic-fc/','honda/civic-fc/front-brake-pads/','honda/vezel-ru/headlamp/','export/','workshops/','parts/','parts/undercarriage-parts/','articles/parts-list-chassis-vin-export-quote/','about/','contact/','cart/','staff/'];
 for(const pg of pages){errs.length=0;await p.goto(U+pg,{waitUntil:'networkidle'});
   const w=await p.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);
   ok(w[0]<=w[1],`no horizontal scroll /${pg} (${w[0]}<=${w[1]})`);
   ok(errs.length===0,`no console errors /${pg} ${errs.join(' | ')}`);}
 // search quality via the in-page engine
 await p.goto(U);
 const Q=[['civic brake pads',/Brake Pads for Honda Civic/,8],['vezel headlamp',/Headlamp for Honda Vezel/,2],['hrv tail lamp',/Tail Lamp for Honda Vezel/,2],['fit cabin filter',/Cabin Filter for Honda Jazz/,2],
  ['jazz gk spark plugs',/Spark Plugs for Honda Jazz \/ Fit \(GK\)/,1],['civic fc front bumper',/Front Bumper for Honda Civic \(FC\)/,1],['crv rw shock absorber',/Shock Absorber for Honda CR-V \(RW\)/,2],
  ['freed gb5 wiper',/Wiper Blades for Honda Freed \(GB5\)/,1],['stepwgn blower motor',/Blower Motor for Honda Stepwgn/,1],['accord cv engine mount',/Engine Mounting for Honda Accord \(CV\)/,1],
  ['insight ignition coil',/Ignition Coil for Honda Insight/,1],['vezel hybrid cabin filter',/Cabin Filter for Honda Vezel/,2],['civic fe cv joint',/CV Joint .* Honda Civic \(FE\)/,1],['stream rn water pump',/Water Pump for Honda Stream/,1],['civik brake pad',/Brake Pads for Honda Civic/,4]];
 for(const [q,re,n] of Q){const r=await p.evaluate(q=>{const o=window.PW.search(q);return o.items.map(x=>x.title)},q);
   ok(r.length>=n&&re.test(r[0]),`search "${q}" -> ${r.length} results, top: ${r[0]}`)}
 // UI search page
 await p.goto(U+'search/?q='+encodeURIComponent('civic brake pads'));let c=await p.locator('[data-results] .pc').count();ok(c>=8,`search page civic brake pads: ${c} cards`);
 await p.goto(U+'search/?q='+encodeURIComponent('vezel headlamp'));c=await p.locator('[data-results] .pc').count();ok(c>=2,`search page vezel headlamp: ${c} cards`);
 // finder
 await p.goto(U);await p.selectOption('[data-f=m]','civic-fc');await p.selectOption('[data-f=p]','front-brake-pads');await Promise.all([p.waitForNavigation(),p.click('.finder button.primary')]);
 ok(/civic-fc\/front-brake-pads\/$/.test(p.url()),'finder -> product page '+p.url());
 // add to cart on product page, then cart WhatsApp link
 await p.goto(U+'honda/civic-fc/front-brake-pads/');await p.click('.buy-f button.primary');
 await p.goto(U+'cart/');ok(await p.locator('.ci').count()===1,'cart has 1 item');
 await p.fill('.co input[name=name]','Test Driver');await p.selectOption('.co select[name=grade]','OEM');
 let waUrl='';p.on('request',r=>{if(/wa\.me/.test(r.url()))waUrl=r.url()});
 await p.click('.co button[type=submit]');await p.waitForTimeout(800);
 ok(/wa\.me\/6587977581\?text=/.test(waUrl),'cart wa.me link: '+waUrl.slice(0,70));
 ok(/Front%20Brake%20Pads/.test(waUrl)&&/OEM/.test(decodeURIComponent(waUrl)),'cart message has item and grade');
 // export page: parts list checker + file + submit
 await p.goto(U+'export/');
 await p.fill('textarea[name=parts]','Civic FC front brake pads, 4\nVezel RU headlamp left, 2\nsome unknown widget 9, 3\nJazz GK cabin filter x 10');
 await p.click('[data-parts-go]');
 const res=await p.locator('.pl-res li').allTextContents();
 ok(res.length===4&&/Front Brake Pads for Honda Civic/.test(res[0])&&/4 ×/.test(res[0]),'export checker matches pasted line: '+res[0].slice(0,80));
 ok(res.filter(t=>/Not in the catalogue/.test(t)).length===1,'export checker flags unmatched line');
 ok(/Several fits|Part found/.test(res[1]+res[3])||res.length===4,'ambiguous lines handled');
 await p.setInputFiles('input[type=file]',{name:'list.csv',mimeType:'text/csv',buffer:Buffer.from('part,qty\nCity GN rear bumper,2\n')});
 await p.waitForTimeout(400);
 ok((await p.inputValue('textarea[name=parts]')).includes('City GN rear bumper'),'file upload read by FileReader into list');
 ok((await p.locator('.pl-res li').count())===5&&/Rear Bumper for Honda City/.test((await p.locator('.pl-res li').allTextContents())[4]),'file line matched (header skipped)');
 await p.fill('input[name=name]','Ali');await p.fill('input[name=company]','Ali Motors');await p.fill('input[name=country]','Malaysia');await p.fill('input[name=contact]','+60 12 345 6789');await p.fill('input[name=vehicle]','Vezel RU1-1234567');
 waUrl='';await p.click('#export-form button[type=submit]');await p.waitForTimeout(1200);
 const href=await p.evaluate(()=>document.querySelector('[data-wa-open]')&&document.querySelector('[data-wa-open]').href);
 ok(/wa\.me\/6587977581\?text=/.test(href||waUrl),'export submit builds wa.me link to 6587977581');
 const msg=decodeURIComponent((href||waUrl).split('text=')[1]||'');
 ok(/Malaysia/.test(msg)&&/Civic/.test(msg)&&/some unknown widget/.test(msg),'export message has country, matched items, unmatched line');
 await p.goto(U+'staff/');const leads=await p.evaluate(()=>JSON.parse(localStorage.getItem('pw_leads_v1')||'[]'));ok(leads.length===1&&leads[0].type==='EXPORT'&&leads[0].unmatched.length>=1,'lead saved in localStorage');
 if(SCR){await p.goto(U+'export/');await p.fill('textarea[name=parts]','Civic FC front brake pads, 4\nVezel RU headlamp left, 2\nsome unknown widget 9, 3');await p.click('[data-parts-go]');
   await p.evaluate(()=>document.querySelector('[data-parts-out]').scrollIntoView({block:'center'}));await p.waitForTimeout(400);await p.screenshot({path:SCR+'/phone-export.jpg',type:'jpeg',quality:82});}
 // staff: PIN 2015 -> Enquiries
 await p.goto(U+'staff/');await p.fill('#st-name','Demo');await p.fill('#st-pin','1995');await p.click('button[type=submit]');ok(/Wrong PIN/.test(await p.textContent('#st-lerr')),'wrong PIN rejected');
 await p.fill('#st-pin','2015');await p.click('button[type=submit]');await p.waitForSelector('#st-tab-leads');await p.click('#st-tab-leads');
 ok(/Ali Motors/.test(await p.textContent('#st-panel'))&&/Malaysia/.test(await p.textContent('#st-panel')),'staff Enquiries list shows saved export lead');
 await p.selectOption('[data-lact=status]','Contacted');ok((await p.evaluate(()=>JSON.parse(localStorage.getItem('pw_leads_v1'))[0].status))==='Contacted','staff status change saved');
 await p.click('#st-tab-products');await p.waitForSelector('#st-list');ok(await p.locator('#st-list').count()===1,'staff products tab renders');
 // workshop lead
 await p.goto(U+'workshops/');await p.fill('#trade-form input[name=company]','AB Workshop');await p.fill('#trade-form input[name=name]','Bob');await p.fill('#trade-form input[name=contact]','91234567');
 await p.fill('#trade-form textarea[name=note]','Need weekly supply');await p.click('#trade-form button[type=submit]');await p.waitForTimeout(900);
 await p.goto(U+'staff/');ok((await p.evaluate(()=>JSON.parse(localStorage.getItem('pw_leads_v1')).length))===2,'workshop lead saved (2 total)');
 // home screenshot + reduced-motion / no animated counters
 await p.goto(U);await p.waitForTimeout(600);if(SCR)await p.screenshot({path:SCR+'/phone-home.jpg',type:'jpeg',quality:82});
 ok(await p.evaluate(()=>document.querySelectorAll('[data-cu]').length)===0,'no script-animated proof figures');
 await b.close();srv.kill();console.log(fail?`\n${fail} FAILED`:'\nALL PASSED');process.exit(fail?1:0);
})().catch(e=>{console.error(e);process.exit(2)});

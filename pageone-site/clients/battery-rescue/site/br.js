/* Battery Rescue SG app logic. Data comes from data.js (window.BR). Never rewrites price text in the served HTML. */
(function(){
var D=window.BR||{},$=function(s,r){return(r||document).querySelector(s)},$$=function(s,r){return[].slice.call((r||document).querySelectorAll(s))};
var WA=D.wa||'6581259169',SITE='battery-rescue',HOST=location.hostname.replace(/^www\./,'');
/* ---------- tap counter (Page One Controller "track"; live domain only) ---------- */
var last={};
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function trk(type,ref){var n=Date.now();if(last[type]&&n-last[type]<1500)return;last[type]=n;
 if(HOST!==D.domain)return;
 try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},
 body:JSON.stringify({entity:'CtaClick',site:SITE,cta_type:type,enquiry_ref:String(ref||'').slice(0,40),session_id:sid(),page_path:location.pathname.slice(0,200),
 device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200)})}).catch(function(){})}catch(e){}}
window.brTrk=trk;
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';
 if(/^tel:/i.test(h))trk('call',a.getAttribute('data-ref')||'');else if(/wa\.me|whatsapp/i.test(h))trk('whatsapp',a.getAttribute('data-ref')||'')},true);
/* ---------- helpers ---------- */
function money(x){return'$'+x.toFixed(2)}
function sgHour(){var d=new Date(Date.now()+(8*60+new Date().getTimezoneOffset())*60000);return d.getHours()}
function isNight(){var h=sgHour();return h>=22||h<9}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function waLink(msg){return'https://wa.me/'+WA+'?text='+encodeURIComponent(msg)}
/* ---------- reveal on scroll (opacity/transform only) ---------- */
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -40px'});
 $$('.rv').forEach(function(el){var r=el.getBoundingClientRect();if(r.top<innerHeight)el.classList.add('in');else io.observe(el)})}else $$('.rv').forEach(function(el){el.classList.add('in')});
/* ---------- mode switch ---------- */
var app=$('#app');if(!app)return;
function setMode(m){$$('.seg button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.mode===m?'true':'false')});
 $$('[data-panel]').forEach(function(p){p.hidden=p.dataset.panel!==m});
 try{history.replaceState(null,'',m==='compare'?'#compare':location.pathname)}catch(e){}}
$$('.seg button').forEach(function(b){b.addEventListener('click',function(){setMode(b.dataset.mode)})});
setMode(location.hash==='#compare'?'compare':'stuck');
window.addEventListener('hashchange',function(){setMode(location.hash==='#compare'?'compare':'stuck');scrollTo(0,0)});
$$('.tabs a').forEach(function(a){a.addEventListener('click',function(){if(a.pathname===location.pathname&&!a.hash){setMode('stuck')}})});
/* ---------- car search ---------- */
var FIT=D.fit||[],P=D.price||{};
function label(r){return r[0]+' '+r[1]}
function yrs(y){var n=(y.match(/(19|20)\d\d/g)||[]).map(Number);var a=n[0]||1900,b=/now/i.test(y)?2100:(n[1]||n[0]||2100);return[a,b]}
function search(q){q=q.toLowerCase().replace(/[^a-z0-9 \-]/g,' ').trim();if(q.length<2)return[];var t=q.split(/\s+/),yr=null,out=[];
 t=t.filter(function(w){if(/^(19|20)\d\d$/.test(w)){yr=+w;return false}return true});
 for(var i=0;i<FIT.length&&out.length<40;i++){var r=FIT[i],s=(r[0]+' '+r[1]).toLowerCase(),s2=s.replace(/-/g,'');
  if(!t.every(function(w){return s.indexOf(w)>-1||s2.indexOf(w.replace(/-/g,''))>-1}))continue;
  if(yr){var g=yrs(r[2]);if(yr<g[0]||yr>g[1])continue}out.push(i)}return out}
function bindSearch(box){var inp=$('input',box),ul=$('.sug',box),x=$('.x',box),k=-1,hits=[];
 function draw(){ul.innerHTML=hits.map(function(i,j){var r=FIT[i];return'<li data-i="'+i+'"'+(j===k?' class="k"':'')+'>'+esc(label(r))+'<small>'+esc(r[2])+'</small></li>'}).join('')+(inp.value.length>1&&!hits.length?'<li data-none="1">Car not listed? <b>Tap to ask us on WhatsApp</b></li>':'');ul.style.display=ul.innerHTML?'block':'none'}
 inp.addEventListener('input',function(){x.style.display=inp.value?'block':'none';hits=search(inp.value);k=-1;draw()});
 inp.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){k=Math.min(k+1,hits.length-1);draw();e.preventDefault()}else if(e.key==='ArrowUp'){k=Math.max(k-1,0);draw();e.preventDefault()}else if(e.key==='Enter'&&hits.length){pick(hits[Math.max(k,0)]);e.preventDefault()}});
 ul.addEventListener('click',function(e){var li=e.target.closest('li');if(!li)return;if(li.dataset.none){trk('whatsapp','not_listed');location.href=waLink('Hi Battery Rescue, my car is not in your list: '+inp.value+'. Which Delkor battery fits and what is the price?');return}pick(+li.dataset.i)});
 x.addEventListener('click',function(){inp.value='';x.style.display='none';hits=[];draw();inp.focus()});
 function pick(i){var r=FIT[i];inp.value=label(r)+' ('+r[2]+')';hits=[];ul.innerHTML='';ul.style.display='none';inp.blur();box.dispatchEvent(new CustomEvent('car',{detail:r}))}}
$$('.carbox').forEach(bindSearch);
/* ---------- stuck mode ---------- */
var cur=null;
function batLine(r){var k=r[4];return k?{k:k,name:'Delkor '+((D.name||{})[k]||k),ah:P[k][0],list:P[k][1]}:{k:null,name:r[3]}}
var sBox=$('#s-car'),sRes=$('#s-res');
if(sBox)sBox.addEventListener('car',function(e){var r=e.detail,b=batLine(r);cur={r:r,b:b};var n=isNight();
 var h='<div class="bat"><div class="ic">'+D.bolt+'</div><div><span>'+esc(label(r))+' ('+esc(r[2])+') uses</span><b>'+esc(b.name)+'</b></div></div>';
 if(b.k){h+='<div class="tiers"><div class="tier day'+(n?'':' hl')+'"><div><div class="n">Fitted where you are'+(n?'':' · now')+'</div><div class="d">Before 10pm, incl. Sunday</div></div><div class="p">'+money(b.list+50)+'</div></div>'+
 '<div class="tier night'+(n?' hl':'')+'"><div><div class="n">Night & public holiday'+(n?' · now':'')+'</div><div class="d">10pm to 9am, and PH</div></div><div class="p">'+money(b.list+80)+'</div></div></div>'+
 '<p class="note">Battery + fitting at your location. GST included. 1-year warranty.</p>'}
 else h+='<div class="enq">We need to check stock for this size. Tap WhatsApp or Call and we will confirm the battery and price.</div>';
 sRes.innerHTML=h;sRes.classList.add('on');updWa()});
function waMsg(loc){var m='Hi Battery Rescue, my car battery is flat. Please help.';if(cur){m+='\nCar: '+label(cur.r)+' ('+cur.r[2]+')\nBattery: '+cur.b.name}if(loc)m+='\nMy location: '+loc;m+='\n(Website source: '+location.href.split('#')[0]+')';return m}
function updWa(){$$('.wa-dyn').forEach(function(a){a.href=waLink(waMsg(''))})}
updWa();
$$('.wa-loc').forEach(function(a){a.addEventListener('click',function(e){if(!navigator.geolocation)return;e.preventDefault();var done=false,lbl=$('.t',a),old=lbl?lbl.innerHTML:'';
 if(lbl)lbl.innerHTML='Getting your location…';
 function go(loc){if(done)return;done=true;if(lbl)lbl.innerHTML=old;trk('whatsapp',(cur&&cur.b.k||'rescue')+(loc?'|gps':''));location.href=waLink(waMsg(loc))}
 navigator.geolocation.getCurrentPosition(function(p){go('https://maps.google.com/?q='+p.coords.latitude.toFixed(5)+','+p.coords.longitude.toFixed(5))},function(){go('')},{enableHighAccuracy:true,timeout:7000,maximumAge:60000});
 setTimeout(function(){go('')},9000)})});
/* ---------- compare mode ---------- */
var O=D.out||[],cBox=$('#c-car'),cRes=$('#c-res'),oUl=$('#c-out'),ccur=null,me=null;
function km(a,b){var R=6371,dl=(b[0]-a[0])*Math.PI/180,dn=(b[1]-a[1])*Math.PI/180,x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*Math.PI/180)*Math.cos(b[0]*Math.PI/180)*Math.sin(dn/2)*Math.sin(dn/2);return 2*R*Math.asin(Math.sqrt(x))}
function drawOut(){if(!oUl)return;var list=O.slice();if(me)list.sort(function(a,b){return km(me,[a.lat,a.lng])-km(me,[b.lat,b.lng])});
 var w=ccur&&ccur.b.k?money(ccur.b.list-20):'';
 oUl.innerHTML=list.map(function(o){return'<li><div class="on"><div><b>'+esc(o.name)+'</b><div class="ad">'+esc(o.addr)+'</div><div class="ad">'+esc(D.hours)+'</div></div>'+(me?'<span class="km">~'+km(me,[o.lat,o.lng]).toFixed(1)+' km</span>':'')+'</div>'+
 (w?'<div class="ad" style="margin-top:6px">'+esc(ccur.b.name)+' fitted here: <b style="color:var(--ok)">'+w+'</b> with web code</div>':'')+
 '<div class="row"><button class="btn g" data-code="'+esc(o.slug)+'">Get $20 code</button><a class="btn o" href="https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(o.map)+'" target="_blank" rel="noopener">Map</a></div></li>'}).join('')}
if(cBox)cBox.addEventListener('car',function(e){var r=e.detail,b=batLine(r);ccur={r:r,b:b};
 var h='<div class="bat"><div class="ic">'+D.bolt+'</div><div><span>'+esc(label(r))+' ('+esc(r[2])+') uses</span><b>'+esc(b.name)+(b.k?' · '+b.ah+'Ah':'')+'</b></div></div>';
 if(b.k)h+='<div class="tiers"><div class="tier walk hl"><div><div class="n">Walk-in at a Motoserv outlet</div><div class="d">With $20 web code · Mon-Sat 9am-6pm</div></div><div class="p">'+money(b.list-20)+'<s>'+money(b.list)+'</s></div></div>'+
 '<div class="tier day"><div><div class="n">Fitted at your location</div><div class="d">Before 10pm, incl. Sunday</div></div><div class="p">'+money(b.list+50)+'</div></div>'+
 '<div class="tier night"><div><div class="n">Night & public holiday</div><div class="d">10pm to 9am, and PH</div></div><div class="p">'+money(b.list+80)+'</div></div></div><p class="note">Delkor battery, fitting and GST included. 1-year warranty. Old battery taken away.</p>';
 else h+='<div class="enq">This size needs a stock check. <a href="'+waLink('Hi Battery Rescue, price check please. Car: '+label(r)+' ('+r[2]+'), battery size '+r[3]+'.')+'">Ask on WhatsApp</a> and we will reply with the Delkor price.</div>';
 cRes.innerHTML=h;cRes.classList.add('on');drawOut()});
drawOut();
var gb=$('#c-gps');if(gb)gb.addEventListener('click',function(){if(!navigator.geolocation)return;gb.textContent='Finding you…';navigator.geolocation.getCurrentPosition(function(p){me=[p.coords.latitude,p.coords.longitude];gb.textContent='Sorted nearest first';drawOut()},function(){gb.textContent='Location blocked: try postal code'},{timeout:8000,maximumAge:300000})});
var pf=$('#c-pc');if(pf)pf.addEventListener('submit',function(e){e.preventDefault();var v=$('input',pf).value.replace(/\D/g,'');if(v.length!==6)return;
 fetch('https://www.onemap.gov.sg/api/common/elastic/search?searchVal='+v+'&returnGeom=Y&getAddrDetails=N&pageNum=1').then(function(r){return r.json()}).then(function(j){var x=j.results&&j.results[0];if(x){me=[+x.LATITUDE,+x.LONGITUDE];drawOut()}}).catch(function(){})});
/* ---------- $20 walk-in code ---------- */
var sh=$('#sheet');
function code(){var c;try{c=localStorage.getItem('br_code')}catch(e){}if(!c){var a='ABCDEFGHJKMNPQRSTUVWXYZ23456789';c='BR-';for(var i=0;i<4;i++)c+=a[Math.floor(Math.random()*a.length)];try{localStorage.setItem('br_code',c)}catch(e){}}return c}
document.addEventListener('click',function(e){var b=e.target.closest('[data-code]');if(b&&sh){var o=O.filter(function(x){return x.slug===b.dataset.code})[0]||{name:'any Motoserv outlet'},c=code();
 $('.code',sh).textContent=c;$('#sh-o',sh).textContent=o.name;$('#sh-b',sh).textContent=ccur&&ccur.b.k?ccur.b.name+': '+money(ccur.b.list-20)+' (was '+money(ccur.b.list)+')':'$20 off any Delkor battery';
 trk('promo_code',c+'|'+(ccur&&ccur.b.k||'-')+'|'+(o.slug||'-'));sh.classList.add('on')}
 if(e.target.closest('[data-close]')||e.target===sh)sh&&sh.classList.remove('on')});
})();

/* Driver lead to XADO (Edwin, 7 Nov 2026): the driver sends XADO Singapore (WhatsApp) their workshop's details,
   and XADO Singapore contacts the workshop. Tap: driver_workshop_lead_to_xado. The no-workshop button is a plain link with
   data-cta="driver_no_workshop_lead", counted by site.js. */
(function(){
var NUM='6593391185';
function norm(v){var d=String(v||'').replace(/[\s().-]/g,'');if(d.charAt(0)==='+')d=d.slice(1);if(/^0065/.test(d))d=d.slice(2);
  if(/^[89]\d{7}$/.test(d))return'65'+d;if(/^65[89]\d{7}$/.test(d))return d;return null}
function clean(v){return String(v||'').replace(/\s+/g,' ').trim().slice(0,80)}
window.xadoLeadText=function(ws,num,name,car){var t='Hi XADO Singapore, please contact my workshop about XADO oil: '+ws+', WhatsApp '+num+'.';
  if(name&&car)t+=' Driver: '+name+', car: '+car+'.';else if(name)t+=' Driver: '+name+'.';else if(car)t+=' Car: '+car+'.';
  return t+' No min order, no obligation.'};
window.xadoLeadLink=function(ws,raw,name,car){var n=norm(raw);ws=clean(ws);if(!n||!ws)return null;
  return 'https://wa.me/'+NUM+'?text='+encodeURIComponent(window.xadoLeadText(ws,n,clean(name),clean(car)))};
[].forEach.call(document.querySelectorAll('.xlead'),function(f){
  var q=function(n){return f.querySelector('[name='+n+']')},ws=q('ws'),num=q('wsnum'),nm=q('driver'),car=q('car'),err=f.querySelector('.ref-err'),go=f.querySelector('button');
  if(!ws||!num||!go)return;
  function fail(el,m){err.textContent=m;el.setAttribute('aria-invalid','true');el.focus()}
  [ws,num,nm,car].forEach(function(el){if(!el)return;el.addEventListener('input',function(){if(err.textContent){err.textContent='';ws.removeAttribute('aria-invalid');num.removeAttribute('aria-invalid')}});
    el.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();go.click()}})});
  go.addEventListener('click',function(){
    if(!clean(ws.value))return fail(ws,"Please type your workshop's name.");
    if(!num.value.trim())return fail(num,"Please type your workshop's WhatsApp number.");
    if(!norm(num.value))return fail(num,"That doesn't look like a Singapore mobile number. Please check it: 8 digits starting with 8 or 9, for example 9123 4567.");
    err.textContent='';ws.removeAttribute('aria-invalid');num.removeAttribute('aria-invalid');
    var link=window.xadoLeadLink(ws.value,num.value,nm&&nm.value,car&&car.value);
    if(window.p1CtaTap)window.p1CtaTap('driver_workshop_lead_to_xado',go);
    var w=window.open(link,'_blank');if(w){try{w.opener=null}catch(e){}}else location.href=link});
});
/* Keep the floating WhatsApp bubble off the form: hide it while the form, its button/note or the
   no-workshop box sits under it (7 Nov 2026). */
var bub=document.querySelector('.wa-float'),zones=document.querySelectorAll('.xlead,.xref-after');
if(bub&&zones.length){var tick=0;function chk(){tick=0;var cs=getComputedStyle(bub),vw=document.documentElement.clientWidth,vh=innerHeight,
    bR=vw-parseFloat(cs.right),bB=vh-parseFloat(cs.bottom),b={right:bR,bottom:bB,left:bR-bub.offsetWidth,top:bB-bub.offsetHeight},hit=false;
  [].forEach.call(zones,function(z){var r=z.getBoundingClientRect();if(r.top<b.bottom+12&&r.bottom>b.top-12&&r.left<b.right+12&&r.right>b.left-12)hit=true});
  bub.classList.toggle('wa-off',hit)}
  function req(){if(!tick){tick=1;requestAnimationFrame(chk)}}
  addEventListener('scroll',req,{passive:true});addEventListener('resize',req);chk()}
})();

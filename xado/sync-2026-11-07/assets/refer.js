/* Driver lead to XADO (Edwin, 7 Nov 2026): the driver sends Roland (XADO Singapore WhatsApp) their workshop's details,
   and Roland contacts the workshop. Tap: driver_workshop_lead_to_roland. The no-workshop button is a plain link with
   data-cta="driver_no_workshop_lead", counted by site.js. */
(function(){
var NUM='6593391185';
function norm(v){var d=String(v||'').replace(/[\s().-]/g,'');if(d.charAt(0)==='+')d=d.slice(1);if(/^0065/.test(d))d=d.slice(2);
  if(/^[89]\d{7}$/.test(d))return'65'+d;if(/^65[89]\d{7}$/.test(d))return d;return null}
function clean(v){return String(v||'').replace(/\s+/g,' ').trim().slice(0,80)}
window.xadoLeadText=function(ws,num,name,car){var t='Hi Roland, please contact my workshop about XADO oil: '+ws+', WhatsApp '+num+'.';
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
    if(window.p1CtaTap)window.p1CtaTap('driver_workshop_lead_to_roland',go);
    var w=window.open(link,'_blank');if(w){try{w.opener=null}catch(e){}}else location.href=link});
});
})();

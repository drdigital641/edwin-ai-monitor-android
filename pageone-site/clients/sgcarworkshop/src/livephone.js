/* Basic PROFILE pages only. On-click "Show opening hours": ONE Place Details call (fields businessStatus,regularOpeningHours), result kept in this
   visitor's sessionStorage for the tab; nothing is stored on our side. The project quota is capped (30/day): on any error we say hours are not
   available right now. A permanently closed workshop is flagged (tap counter) so it can be hidden at the next build. */
(function(){
var b=document.querySelector('.hoursbox');if(!b)return;
var btn=b.querySelector('button'),out=b.querySelector('.hrs'),pid=b.getAttribute('data-pid'),key=b.getAttribute('data-key'),slug=b.getAttribute('data-slug'),ck='hrs_'+pid;
function say(lines){out.textContent='';lines.forEach(function(t){var p=document.createElement('p');p.textContent=t;out.appendChild(p)});out.hidden=false;btn.hidden=true}
function show(j){
 if(j.s==='CLOSED_PERMANENTLY'){say(['This workshop may be permanently closed. Check Google Maps before you go.']);
  try{var a=document.createElement('a');a.setAttribute('data-cta','closed_flag_'+slug);a.setAttribute('data-tier','free');a.style.display='none';document.body.appendChild(a);a.click()}catch(e){}return}
 if(j.h&&j.h.length){say(j.h);return}
 say(['Opening hours are not listed on Google Maps.']);
}
function fail(){say(['Opening hours are not available right now. Open the Google Maps listing to check.'])}
btn.addEventListener('click',function(){
 try{var c=sessionStorage.getItem(ck);if(c){show(JSON.parse(c));return}}catch(e){}
 if(!window.fetch||!key||!pid){fail();return}
 btn.disabled=true;
 var ctl=window.AbortController?new AbortController():null,t=setTimeout(function(){if(ctl)ctl.abort()},6000);
 fetch('https://places.googleapis.com/v1/places/'+encodeURIComponent(pid)+'?fields=businessStatus,regularOpeningHours&key='+encodeURIComponent(key),{signal:ctl?ctl.signal:undefined})
 .then(function(r){clearTimeout(t);return r.ok?r.json():null}).then(function(j){
  if(!j){fail();return}
  var r={s:j.businessStatus||'',h:(j.regularOpeningHours&&j.regularOpeningHours.weekdayDescriptions)||[]};
  try{sessionStorage.setItem(ck,JSON.stringify(r))}catch(e){}show(r)}).catch(fail);
});
})();

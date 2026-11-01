/* Basic PROFILE pages only, and only when no phone number is stored for the workshop.
   One Place Details call for the number the workshop publishes itself (field mask: nationalPhoneNumber,internationalPhoneNumber).
   Nothing is stored: the result lives in this visitor's sessionStorage for the tab. If the call fails or the project quota is used up, the button stays hidden. */
(function(){
var s=document.querySelector('.livephone');if(!s)return;
var pid=s.getAttribute('data-pid'),key=s.getAttribute('data-key'),ck='lp_'+pid;
function show(intl){
 var dg=String(intl||'').replace(/\D/g,'');if(dg.length<10||dg.slice(0,2)!=='65')return;
 var loc=dg.slice(2),mob=/^[89]\d{7}$/.test(loc),slug=s.getAttribute('data-slug'),pg=s.getAttribute('data-page'),a=document.createElement('a');
 a.className='btn big'+(mob?' wa':'');a.target=mob?'_blank':'';a.rel='noopener';a.setAttribute('data-tier','free');a.setAttribute('data-page',pg);
 if(mob){var m='Hi, I found you on '+s.getAttribute('data-site')+' ('+s.getAttribute('data-host')+'). I would like to ask about '+s.getAttribute('data-ask');
  a.href='https://wa.me/'+dg+'?text='+encodeURIComponent(m);a.setAttribute('data-cta','whatsapp_dir_'+slug);a.textContent='WhatsApp'}
 else{a.href='tel:+'+dg;a.setAttribute('data-cta','call_dir_'+slug);a.textContent='Call'}
 s.parentNode.insertBefore(a,s);
}
try{var c=sessionStorage.getItem(ck);if(c!==null){c=JSON.parse(c);if(c&&c.n)show(c.n);return}}catch(e){}
if(!window.fetch||!key||!pid)return;
var ctl=window.AbortController?new AbortController():null,t=setTimeout(function(){if(ctl)ctl.abort()},6000);
fetch('https://places.googleapis.com/v1/places/'+encodeURIComponent(pid)+'?fields=nationalPhoneNumber,internationalPhoneNumber&key='+encodeURIComponent(key),{signal:ctl?ctl.signal:undefined})
.then(function(r){clearTimeout(t);return r.ok?r.json():null}).then(function(j){
 var n=j&&(j.internationalPhoneNumber||'');try{sessionStorage.setItem(ck,JSON.stringify({n:n||null}))}catch(e){}
 if(n)show(n)}).catch(function(){try{sessionStorage.setItem(ck,JSON.stringify({n:null}))}catch(e){}});
})();

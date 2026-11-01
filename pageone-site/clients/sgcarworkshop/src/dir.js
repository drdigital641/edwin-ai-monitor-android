(function(){
var d=document,els=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(el){io.observe(el)})}
else{els.forEach(function(el){el.classList.add('in')})}
var q=d.getElementById('q');
if(q){var cards=d.querySelectorAll('[data-search]'),em=d.getElementById('empty');
function f(){var v=q.value.trim().toLowerCase(),n=0;cards.forEach(function(c){var ok=!v||c.getAttribute('data-search').indexOf(v)>-1;c.hidden=!ok;if(ok)n++});if(em)em.classList.toggle('show',!!v&&!n)}
q.addEventListener('input',f);var fm=q.form;if(fm)fm.addEventListener('submit',function(e){e.preventDefault();f()})}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-cta]');if(!a)return;var c=a.getAttribute('data-cta');try{if(window.dataLayer)window.dataLayer.push({event:'cta_click',cta:c})}catch(x){}track(a,c)});
/* Lead counter: Page One Controller public write-only "track" function (same endpoint and payload as pageonesingapore.com main.js).
   Fires ONLY on the live directory domain, so preview clicks are not counted. WhatsApp and call taps on business listings only. */
var LIVE_HOST='sgcarworkshop.sg',APP='6ac7f2548a9c3877449e2772';
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function keep(st,k){try{var v=st.getItem(k);if(!v){v=rid();st.setItem(k,v)}return v}catch(x){return rid()}}
function track(a,c){try{
if(location.hostname!==LIVE_HOST&&location.hostname!=='www.'+LIVE_HOST)return;
if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.webdriver)return;
var tier=a.getAttribute('data-tier');if(!tier||!/^(whatsapp|call)_dir_/.test(c))return;
var slug=c.replace(/^(whatsapp|call)_dir_/,''),page=a.getAttribute('data-page')||location.pathname,ua=navigator.userAgent;
var body=JSON.stringify({entity:'CtaClick',site:'sgcarworkshop',session_id:keep(sessionStorage,'sgcw-sid'),visitor_id:keep(localStorage,'sgcw-vid'),page_path:location.pathname,
referrer:(document.referrer||'').slice(0,300),device_type:/Mobi|Android|iPhone/i.test(ua)?'mobile':/iPad|Tablet/i.test(ua)?'tablet':'desktop',
cta_type:c,enquiry_ref:slug+'|'+tier+'|'+page});
var url='https://base44.app/api/apps/'+APP+'/functions/track',sent=false;
if(navigator.sendBeacon){try{sent=navigator.sendBeacon(url,new Blob([body],{type:'application/json'}))}catch(x){}}
if(!sent&&window.fetch){fetch(url,{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:body}).catch(function(){})}
}catch(x){}}
})();

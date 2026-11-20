/* CTA tap counter v4 for Overseas Tyre (site key overseas-tyre), 20 Nov 2026.
   Counts WhatsApp, call (tel:), email (mailto:) and other data-cta taps; data-cta / data-ref name the placement.
   Preview (/preview/...): taps are sent ONLY when the page was opened with ?p1test=1, and are stored as test taps.
   Live domain: every tap counts; ?p1test=1 marks that tab's taps as tests. No IP or fingerprinting. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,''),pv=/^\/preview\//.test(location.pathname);
if(h==='localhost')return;window.__p1cta=4;var SITE='overseas-tyre';
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,BOOK=/calendly\.com|setmore\.com|simplybook|fresha\.com|square\.site\/book|book\.squareup|youcanbook\.me|\/book(ing)?(-now)?\/?(\?|#|$)|appointment/i,last={},S=null,waOpen=0;
var TQ=(function(){var q=/[?&]p1test=1(&|$)/.test(location.search);try{if(q)sessionStorage.setItem('p1test','1');return sessionStorage.getItem('p1test')==='1'}catch(e){return q}})();var T=pv||TQ;
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=rid();sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function vid(){try{var k='p1cta_vid',v=localStorage.getItem(k);if(!v){v=rid();localStorage.setItem(k,v)}return v}catch(e){return''}}
function visit(){try{var s=JSON.parse(sessionStorage.getItem('p1cta_v')||'null');if(!s){var q=new URLSearchParams(location.search),r=document.referrer||'',rh='';try{rh=new URL(r).hostname.replace(/^www\./,'')}catch(e){}
s={t:Date.now(),l:location.pathname.slice(0,200),r:rh===h?'':r.slice(0,300),us:(q.get('utm_source')||'').slice(0,100),um:(q.get('utm_medium')||'').slice(0,100),uc:(q.get('utm_campaign')||'').slice(0,100),
ad:q.get('gclid')||q.get('gbraid')||q.get('wbraid')?'google':q.get('fbclid')?'facebook':q.get('msclkid')?'microsoft':q.get('ttclid')?'tiktok':'',n:0}}
s.n++;sessionStorage.setItem('p1cta_v',JSON.stringify(s));return s}catch(e){return null}}
S=visit();
function place(a){if(!a||!a.closest)return'';var r=a.closest('[data-ref]');if(r)return r.getAttribute('data-ref');
try{for(var e=a;e&&e!==document.body;e=e.parentElement){var p=getComputedStyle(e).position;if(p==='fixed')return'float';if(p==='sticky')return'sticky'}}catch(x){}
if(a.closest('header,.hd,.header,.site-header'))return a.closest('nav')?'nav':'header';if(a.closest('nav'))return'nav';if(a.closest('footer,.ft,.footer,.site-footer'))return'footer';
if(a.closest('form'))return'form';if(a.closest('.hero,[class*="hero"]'))return'hero';var s=a.closest('section[id],article,section[class]');
if(s){if(s.tagName==='ARTICLE')return'article';return'section:'+(s.id||String(s.className).split(' ')[0]).slice(0,30)}return'body'}
function send(a,type,lab0){if(pv&&!TQ)return;type=String(type||'whatsapp').toLowerCase().replace(/[^a-z0-9_]+/g,'_').slice(0,40);var n=Date.now();if(last[type]&&n-last[type]<1500)return;last[type]=n;var s=S||{},tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var txt=lab0||(a?String(a.getAttribute('aria-label')||a.textContent||a.getAttribute('name')||a.id||''):''),pl=place(a);
var lab=((pl?pl+' | ':'')+txt).replace(/\s+/g,' ').trim().slice(0,60);
try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:SITE,cta_type:type,session_id:sid(),visitor_id:vid(),page_path:location.pathname.slice(0,200),
device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:s.r!=null?s.r:(document.referrer||'').slice(0,300),page_referrer:(document.referrer||'').slice(0,300),
landing_path:s.l||'',utm_source:s.us||'',utm_medium:s.um||'',utm_campaign:s.uc||'',ad_click:s.ad||'',pages_viewed:s.n||1,secs_on_site:s.t?Math.round((n-s.t)/1000):0,
cta_label:lab,tz:tz,lang:(navigator.language||'').slice(0,16),screen:(screen.width||0)+'x'+(screen.height||0),test:T?1:undefined})}).catch(function(){})}catch(e){}}
window.p1WaTap=function(a){send(a,'whatsapp')};window.p1CtaTap=function(type,a){send(a||null,type)};
function kind(el){var c=el.getAttribute&&el.getAttribute('data-cta');if(c)return c;var u=String(el.href||el.getAttribute('href')||'');
if(WA.test(u))return'whatsapp';if(/^tel:/i.test(u))return'call';if(/^mailto:/i.test(u))return'email';if(BOOK.test(u)&&!/^#/.test(el.getAttribute('href')||''))return'booking';return''}
document.addEventListener('click',function(e){var t=e.target&&e.target.closest?e.target.closest('a[href],[data-cta]'):null;if(!t||t.tagName==='FORM')return;var k=kind(t);if(k&&k!=='form_submit')send(t,k)},true);
try{var wo=window.open;window.open=function(u){try{if(WA.test(String(u||''))){waOpen=Date.now();var f=document.activeElement&&document.activeElement.closest?document.activeElement.closest('form'):null;send(f||document.activeElement,'whatsapp',f?'WhatsApp form':'')}}catch(x){}return wo.apply(window,arguments)}}catch(e){}
document.addEventListener('submit',function(e){var f=e.target;if(!f||!f.getAttribute)return;
if(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||''))return send(f,'whatsapp');
var c=f.getAttribute('data-cta');if(c)return send(f,c);if(f.getAttribute('role')==='search'||f.querySelector('input[type=search]'))return;
if(f.querySelector('input[type=email],input[type=tel],textarea,input[name*=phone i],input[name*=email i],input[name*=mobile i]'))setTimeout(function(){if(Date.now()-waOpen>1500)send(f,'form_submit')},60)},true)})();

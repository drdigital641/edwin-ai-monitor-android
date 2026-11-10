/* CTA tap counter -> Page One Controller (public write-only "track" fn). Replace SLUG with the Controller Client slug.
   v1 22 Oct 2026; v2 27 Oct 2026: per-tap details; v3 5 Nov 2026: every CTA, not just WhatsApp:
   whatsapp (wa.me / WhatsApp links and data-wa forms), call (tel:), email (mailto:), booking (booking links or data-cta="booking"),
   form_submit (a real lead form: has a phone/email/message field, or data-cta="form_submit"; search forms never count).
   Test mode: open any page with ?p1test=1 and every tap in that tab is stored as a test, outside Edwin's numbers.
   Sends only what a browser tells any website: page, first referrer + UTM of the visit, button text, screen size, time zone, language,
   pages viewed and seconds on site, plus random visit/visitor ids. No IP, no fingerprinting, no ad click ids (only "came from an ad"). */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,BOOK=/calendly\.com|setmore\.com|simplybook|fresha\.com|square\.site\/book|book\.squareup|youcanbook\.me|\/book(ing)?(-now)?\/?(\?|#|$)|appointment/i,last={},S=null;
var T=(function(){var q=/[?&]p1test=1(&|$)/.test(location.search);try{if(q)sessionStorage.setItem('p1test','1');return sessionStorage.getItem('p1test')==='1'}catch(e){return q}})();
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=rid();sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function vid(){try{var k='p1cta_vid',v=localStorage.getItem(k);if(!v){v=rid();localStorage.setItem(k,v)}return v}catch(e){return''}}
function visit(){try{var s=JSON.parse(sessionStorage.getItem('p1cta_v')||'null');if(!s){var q=new URLSearchParams(location.search),r=document.referrer||'',rh='';try{rh=new URL(r).hostname.replace(/^www\./,'')}catch(e){}
s={t:Date.now(),l:location.pathname.slice(0,200),r:rh===h?'':r.slice(0,300),us:(q.get('utm_source')||'').slice(0,100),um:(q.get('utm_medium')||'').slice(0,100),uc:(q.get('utm_campaign')||'').slice(0,100),
ad:q.get('gclid')||q.get('gbraid')||q.get('wbraid')?'google':q.get('fbclid')?'facebook':q.get('msclkid')?'microsoft':q.get('ttclid')?'tiktok':'',n:0}}
s.n++;sessionStorage.setItem('p1cta_v',JSON.stringify(s));return s}catch(e){return null}}
S=visit();
function send(a,type){type=type||'whatsapp';var n=Date.now();if(last[type]&&n-last[type]<1500)return;last[type]=n;var s=S||{},tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var lab=a?String(a.getAttribute('aria-label')||a.getAttribute('data-ref')||a.textContent||a.getAttribute('name')||a.id||'').replace(/\s+/g,' ').trim().slice(0,60):'';
try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'contiexpert',cta_type:type,session_id:sid(),visitor_id:vid(),page_path:location.pathname.slice(0,200),
device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:s.r!=null?s.r:(document.referrer||'').slice(0,300),page_referrer:(document.referrer||'').slice(0,300),
landing_path:s.l||'',utm_source:s.us||'',utm_medium:s.um||'',utm_campaign:s.uc||'',ad_click:s.ad||'',pages_viewed:s.n||1,secs_on_site:s.t?Math.round((n-s.t)/1000):0,
cta_label:lab,tz:tz,lang:(navigator.language||'').slice(0,16),screen:(screen.width||0)+'x'+(screen.height||0),test:T?1:undefined})}).catch(function(){})}catch(e){}}
window.p1WaTap=function(a){send(a,'whatsapp')};window.p1CtaTap=function(type,a){send(a||null,type)};
function kind(el){var c=el.getAttribute&&el.getAttribute('data-cta');if(c)return c;var u=String(el.href||el.getAttribute('href')||'');
if(WA.test(u))return'whatsapp';if(/^tel:/i.test(u))return'call';if(/^mailto:/i.test(u))return'email';if(BOOK.test(u)&&!/^#/.test(el.getAttribute('href')||''))return'booking';return''}
document.addEventListener('click',function(e){var t=e.target&&e.target.closest?e.target.closest('a[href],[data-cta]'):null;if(!t||t.tagName==='FORM')return;var k=kind(t);if(k&&k!=='form_submit')send(t,k)},true);
document.addEventListener('submit',function(e){var f=e.target;if(!f||!f.getAttribute)return;
if(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||''))return send(f,'whatsapp');
var c=f.getAttribute('data-cta');if(c)return send(f,c);if(f.getAttribute('role')==='search'||f.querySelector('input[type=search]'))return;
if(f.querySelector('input[type=email],input[type=tel],textarea,input[name*=phone i],input[name*=email i],input[name*=mobile i]'))send(f,'form_submit')},true)})();

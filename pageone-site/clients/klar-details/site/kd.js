(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  /* reveal on scroll: decorates only, text is always in the HTML */
  var els=d.querySelectorAll('.rv');
  if(!('IntersectionObserver' in window)||rm){[].forEach.call(els,function(e){e.classList.add('in')})}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    [].forEach.call(els,function(e){var r=e.getBoundingClientRect();if(r.top<innerHeight*1.2&&r.bottom>0){e.classList.add('in')}else io.observe(e)});
    /* safety net: nothing stays hidden for a reader that never scrolls */
    setTimeout(function(){[].forEach.call(els,function(e){e.classList.add('in')})},2500)}
  /* homepage promo: hides after its end date, a close lasts for the browser session only; it comes back in a new visit */
  var pr=d.getElementById('promo');
  if(pr){var key='kd_promo_'+pr.getAttribute('data-id'),ends=new Date(pr.getAttribute('data-ends')+'T23:59:59+08:00'),days=+pr.getAttribute('data-days')||7,seen=0;
    try{seen=+sessionStorage.getItem(key)||0}catch(e){}
    function close(){pr.hidden=true;d.body.style.overflow='';try{sessionStorage.setItem(key,String(Date.now()))}catch(e){}var v=pr.querySelector('video');if(v)v.pause()}
    if(Date.now()<=ends.getTime()&&Date.now()-seen>days*864e5){
      setTimeout(function(){pr.hidden=false;d.body.style.overflow='hidden';var v=pr.querySelector('video');if(v&&v.play){var k=v.play();if(k&&k.catch)k.catch(function(){})}var x=pr.querySelector('.promo-x');if(x)x.focus()},1400);
      pr.addEventListener('click',function(e){if(e.target.closest('[data-promo-close]'))close()});
      d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!pr.hidden)close()});
      [].forEach.call(pr.querySelectorAll('a.btn-wa'),function(a){a.addEventListener('click',function(){try{sessionStorage.setItem(key,String(Date.now()))}catch(e){}})});
    }
  }
  /* lazy photos: some Safari versions never start a native lazy image (blank tiles). Load each one as it comes near,
     and load any that are still waiting shortly after the page has loaded. The src stays in the HTML for search engines. */
  var lz=[].slice.call(d.querySelectorAll('img[loading="lazy"]'));
  function go(i){if(i.getAttribute('loading')==='lazy'){i.setAttribute('loading','eager');if(!i.complete){var s=i.getAttribute('srcset');if(s)i.srcset=s;i.src=i.getAttribute('src')}}}
  if('IntersectionObserver' in window){var lo=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){go(x.target);lo.unobserve(x.target)}})},{rootMargin:'800px 800px'});lz.forEach(function(i){lo.observe(i)})}
  function late(){setTimeout(function(){lz.forEach(go)},1800)}
  if(d.readyState==='complete')late();else window.addEventListener('load',late);
  /* service galleries: arrow buttons move one photo; swipe works natively */
  [].forEach.call(d.querySelectorAll('[data-swipe]'),function(g){var nav=g.nextElementSibling;if(!nav||!nav.classList.contains('gal-nav'))return;
    nav.removeAttribute('aria-hidden');[].forEach.call(nav.querySelectorAll('.gal-b'),function(b){b.setAttribute('aria-label',b.getAttribute('data-dir')>0?'Next photo':'Previous photo');
      b.addEventListener('click',function(){var it=g.querySelector('.gal-i');var w=it?it.getBoundingClientRect().width+14:300;g.scrollBy({left:w*+b.getAttribute('data-dir'),behavior:rm?'auto':'smooth'})})})});
  /* rails glide slowly; pause on touch, hover or sideways swipe */
  [].forEach.call(d.querySelectorAll('[data-glide]'),function(r){
    var t=r.querySelector('.rail-track');if(!t||rm)return;
    if(t.scrollWidth<r.clientWidth*1.2)return;
    [].slice.call(t.children).forEach(function(c){var k=c.cloneNode(true);k.setAttribute('aria-hidden','true');k.classList.add('in');[].forEach.call(k.querySelectorAll('a'),function(a){a.tabIndex=-1});t.appendChild(k)});
    var speed=r.getAttribute('data-glide')==='slow'?0.018:0.03,hold=0,last=0,acc=0,tm;
    function half(){return t.scrollWidth/2}
    function step(ts){if(last&&!hold&&!d.hidden){acc+=(ts-last)*speed;if(acc>=1){r.scrollLeft+=Math.floor(acc);acc-=Math.floor(acc)}}if(r.scrollLeft>=half())r.scrollLeft-=half();last=ts;requestAnimationFrame(step)}
    requestAnimationFrame(step);
    function pause(ms){hold=1;clearTimeout(tm);tm=setTimeout(function(){hold=0},ms)}
    r.addEventListener('mouseenter',function(){hold=1});r.addEventListener('mouseleave',function(){hold=0});
    r.addEventListener('touchstart',function(){pause(4000)},{passive:true});r.addEventListener('touchmove',function(){pause(4000)},{passive:true});
    r.addEventListener('focusin',function(){hold=1});r.addEventListener('focusout',function(){hold=0});
  });
});
})();
/* Page One CTA tap counter v3 (5 Nov 2026), same as /tracking/wa-tap-counter.js: WhatsApp, call, email, booking, form_submit; ?p1test=1 test mode. */
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
try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'klar-details',cta_type:type,session_id:sid(),visitor_id:vid(),page_path:location.pathname.slice(0,200),
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

(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){

  /* demo car: tap a swatch, new paint sprays across the body */
  var st=d.querySelector('.studio');
  if(st){var busy=0,n=st.querySelector('.pk-n'),j=st.querySelector('.pk-j'),ji=st.querySelector('.pk-job img'),sws=[].slice.call(st.querySelectorAll('.sw')),cur=0,auto=null,touched=0;
    function paint(b){if(busy||b.getAttribute('aria-pressed')==='true')return;busy=1;var c=b.getAttribute('data-c');
      sws.forEach(function(x){x.setAttribute('aria-pressed',x===b)});cur=sws.indexOf(b);
      n.textContent=b.getAttribute('data-n');j.textContent='Seen on our job: '+b.getAttribute('data-j');ji.src=b.getAttribute('data-img');
      st.style.setProperty('--next',c);
      if(rm){st.style.setProperty('--paint',c);busy=0;return}
      st.classList.remove('spraying');void st.offsetWidth;st.classList.add('spraying');
      setTimeout(function(){st.style.setProperty('--paint',c);st.classList.remove('spraying');busy=0},1200)}
    sws.forEach(function(b){b.addEventListener('click',function(){touched=1;paint(b)})});
    /* gentle demo: change colour every 4.5 s until the visitor taps */
    if(!rm&&!navigator.webdriver)auto=setInterval(function(){if(touched||d.hidden)return;var r=st.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return;paint(sws[(cur+1)%sws.length])},4500);
  }
  /* job carousel: glides slowly, pauses while touched or hovered */
  [].forEach.call(d.querySelectorAll('[data-glide]'),function(r){
    var t=r.querySelector('.rail-track');if(!t||rm)return;
    t.innerHTML+=t.innerHTML;[].forEach.call(t.children,function(c,i){if(i>=t.children.length/2){c.setAttribute('aria-hidden','true');c.tabIndex=-1}});
    var hold=0,last=0,acc=0,down=0,sx=0,sl=0;
    function half(){return t.scrollWidth/2}
    function step(ts){if(last&&!hold&&!d.hidden){acc+=(ts-last)*0.03;if(acc>=1){r.scrollLeft+=Math.floor(acc);acc-=Math.floor(acc)}}if(r.scrollLeft>=half())r.scrollLeft-=half();last=ts;requestAnimationFrame(step)}
    requestAnimationFrame(step);
    r.addEventListener('mouseenter',function(){hold=1});r.addEventListener('mouseleave',function(){hold=0;down=0});
    r.addEventListener('touchstart',function(){hold=1},{passive:true});r.addEventListener('touchend',function(){setTimeout(function(){hold=0},1500)});
    r.addEventListener('mousedown',function(e){down=1;sx=e.pageX;sl=r.scrollLeft;e.preventDefault()});
    d.addEventListener('mouseup',function(){down=0});
    r.addEventListener('mousemove',function(e){if(down)r.scrollLeft=sl-(e.pageX-sx)});
    r.addEventListener('click',function(e){if(Math.abs(r.scrollLeft-sl)>6&&sl)e.preventDefault()},true);
  });
  /* before / after slider */
  [].forEach.call(d.querySelectorAll('.ba'),function(b){var i=b.querySelector('.ba-range');i.addEventListener('input',function(){b.style.setProperty('--x',i.value+'%')})});
  /* reveal on scroll: only opacity/transform, text is in the HTML */
  var els=[].slice.call(d.querySelectorAll('.sec-head,.svc,.steps li,.proof li,.acard,.faq details,.band,.photo,.ba,.work,.side-card,.answer'));
  if(!rm&&'IntersectionObserver' in window&&!navigator.webdriver){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
    els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<innerHeight)return;e.classList.add('rv');var i=[].indexOf.call(e.parentNode.children,e);e.style.transitionDelay=Math.min(i,5)*70+'ms';io.observe(e)});
  }
});
})();
/* enquiry form -> WhatsApp */
(function(){var f=document.getElementById('enquiry');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
var L=['Hi Wei Car Spray Painting, I found your website. I would like a quote for: '+g('s')];
if(g('c'))L.push('Car: '+g('c'));if(g('n'))L.push('Name: '+g('n'));if(g('x'))L.push('Notes: '+g('x'));L.push('(I will send photos here.)');
if(window.p1WaTap)window.p1WaTap(null);
window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(L.join('\n')),'_blank','noopener')});})();
/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Replace wei-car-spray-painting with the Controller Client slug. v1 22 Oct 2026; v2 27 Oct 2026: per-tap details.
   Sends only what a browser tells any website: page, first referrer + UTM of the visit, button text, screen size, time zone, language,
   pages viewed and seconds on site, plus random visit/visitor ids. No IP, no fingerprinting, no ad click ids (only "came from an ad"). */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0,S=null;
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=rid();sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function vid(){try{var k='p1cta_vid',v=localStorage.getItem(k);if(!v){v=rid();localStorage.setItem(k,v)}return v}catch(e){return''}}
function visit(){try{var s=JSON.parse(sessionStorage.getItem('p1cta_v')||'null');if(!s){var q=new URLSearchParams(location.search),r=document.referrer||'',rh='';try{rh=new URL(r).hostname.replace(/^www\./,'')}catch(e){}
s={t:Date.now(),l:location.pathname.slice(0,200),r:rh===h?'':r.slice(0,300),us:(q.get('utm_source')||'').slice(0,100),um:(q.get('utm_medium')||'').slice(0,100),uc:(q.get('utm_campaign')||'').slice(0,100),
ad:q.get('gclid')||q.get('gbraid')||q.get('wbraid')?'google':q.get('fbclid')?'facebook':q.get('msclkid')?'microsoft':q.get('ttclid')?'tiktok':'',n:0}}
s.n++;sessionStorage.setItem('p1cta_v',JSON.stringify(s));return s}catch(e){return null}}
S=visit();
function send(a){var n=Date.now();if(n-last<1500)return;last=n;var s=S||{},tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var lab=a?String(a.getAttribute('aria-label')||a.textContent||'').replace(/\s+/g,' ').trim().slice(0,60):'';
try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'wei-car-spray-painting',cta_type:'whatsapp',session_id:sid(),visitor_id:vid(),page_path:location.pathname.slice(0,200),
device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:s.r!=null?s.r:(document.referrer||'').slice(0,300),page_referrer:(document.referrer||'').slice(0,300),
landing_path:s.l||'',utm_source:s.us||'',utm_medium:s.um||'',utm_campaign:s.uc||'',ad_click:s.ad||'',pages_viewed:s.n||1,secs_on_site:s.t?Math.round((n-s.t)/1000):0,
cta_label:lab,tz:tz,lang:(navigator.language||'').slice(0,16),screen:(screen.width||0)+'x'+(screen.height||0)})}).catch(function(){})}catch(e){}}
window.p1WaTap=send;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send(a)},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.getAttribute&&(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||'')))send(null)},true)})();

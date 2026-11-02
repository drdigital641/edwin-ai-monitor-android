(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  /* hero crossfade */
  var sl=[].slice.call(d.querySelectorAll('.hero-media .slide')),si=0,tag=d.querySelector('.hero-tag');
  if(sl.length){sl[0].classList.add('on');
    if(sl.length>1&&!rm)setInterval(function(){if(d.hidden)return;sl[si].classList.remove('on');si=(si+1)%sl.length;sl[si].classList.add('on');if(tag)tag.textContent=sl[si].getAttribute('data-tag')||''},5500)}
  /* reveal on scroll */
  var els=[].slice.call(d.querySelectorAll('.sec-head,.svc,.works a,.quote,.sister,.faq details,.band,.acard,.crow,.ggroup,.prose>h2,.numbered li,.offer'));
  if(!rm&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
    els.forEach(function(e){e.classList.add('rv');var i=[].indexOf.call(e.parentNode.children,e);e.style.transitionDelay=Math.min(i,5)*60+'ms';io.observe(e)});
  }
  /* past works: colour filter */
  var chips=d.querySelectorAll('.chips button');
  [].forEach.call(chips,function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-k');
    [].forEach.call(chips,function(x){x.setAttribute('aria-pressed',x===b)});
    [].forEach.call(d.querySelectorAll('.ggroup'),function(g){g.hidden=!(k==='all'||g.id===k)})})});
  if(location.hash&&chips.length){var t=d.querySelector('.chips button[data-k="'+location.hash.slice(1)+'"]');if(t)t.click()}
  /* lightbox */
  var lb=d.getElementById('lb');
  if(lb&&lb.showModal){var li=lb.querySelector('img'),lp=lb.querySelector('p');
    d.addEventListener('click',function(e){var b=e.target.closest('.gal button');if(!b)return;var im=b.querySelector('img');li.src=im.src;li.alt=im.alt;lp.textContent=im.alt;lb.showModal()});
    lb.addEventListener('click',function(e){if(e.target===lb||e.target.closest('.x'))lb.close()})}
});
})();
/* enquiry form -> WhatsApp */
(function(){var f=document.getElementById('enquiry');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
var L=['Hi Wrapstar Autostyle, I found your website. I would like a quote for: '+g('s')];
if(g('c'))L.push('Car: '+g('c'));if(g('k'))L.push('Colour or film: '+g('k'));if(g('n'))L.push('Name: '+g('n'));if(g('x'))L.push('Notes: '+g('x'));
window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(L.join('\n')),'_blank','noopener')});})();
/* continuous glide on carousels: loops, pauses only when held or swiped sideways; page scrolling never pauses it */
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.glide'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');c.removeAttribute('id');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});r.appendChild(c)});
  r.classList.add('auto');
  var o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.04)};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var hold=function(){o.hold=Date.now()+3000},sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;hold()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mousedown',function(){o.hold=Infinity});addEventListener('mouseup',function(){if(o.hold===Infinity&&!touching)hold()});
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))hold()},{passive:true});
  r.addEventListener('focusin',hold);
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);else o.vis=true;
  rails.push(o)});
if(!rails.length)return;
var last=0;
function tick(t){var dt=last?Math.min(64,t-last):16;last=t;
  rails.forEach(function(o){var r=o.r;
    if(!o.vis||d.hidden||Date.now()<o.hold){o.pos=r.scrollLeft;return}
    o.pos+=dt*o.speed;
    if(o.half&&o.pos>=o.half)o.pos-=o.half;
    r.scrollLeft=o.pos});
  requestAnimationFrame(tick)}
requestAnimationFrame(tick)})})();
/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Site: wrapstar. Added 22 Oct 2026. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0;
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function send(){var n=Date.now();if(n-last<1500)return;last=n;try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'wrapstar',cta_type:'whatsapp',session_id:sid(),page_path:location.pathname.slice(0,200),device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200)})}).catch(function(){})}catch(e){}}
window.p1WaTap=send;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send()},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.getAttribute&&(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||'')))send()},true)})();

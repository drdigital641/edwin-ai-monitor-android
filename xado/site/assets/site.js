document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));
  const f=b.dataset.f;
  document.querySelectorAll('.dealer').forEach(d=>d.classList.toggle('hide',f!=='All'&&d.dataset.region!==f));
}));
if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){document.querySelectorAll('.hero-bg').forEach(v=>v.pause());}

/* reveal on scroll: cards fade up as they enter; text is never changed */
(function(){var d=document;if(!('IntersectionObserver' in window))return;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var els=d.querySelectorAll('.card,.steps>div,.prod,.dealer,.pg,.rel,.split>*,.tbl,.takeaways');var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
[].forEach.call(els,function(e){if(e.getBoundingClientRect().top>innerHeight){e.classList.add('rv');io.observe(e)}})})();
/* continuous glide on carousels (Wrapstar standard): loops, pauses only when held or swiped sideways; page scrolling never pauses it */
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var rails=[];[].forEach.call(d.querySelectorAll('.glide'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.removeAttribute('id');[].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});r.appendChild(c)});
  r.classList.add('auto');var o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.04)};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var hold=function(){o.hold=Date.now()+3000},sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;hold()}};r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mousedown',function(){o.hold=Infinity});addEventListener('mouseup',function(){if(o.hold===Infinity&&!touching)hold()});
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))hold()},{passive:true});r.addEventListener('focusin',hold);
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);else o.vis=true;rails.push(o)});
if(!rails.length)return;var last=0;
function tick(t){var dt=last?Math.min(64,t-last):16;last=t;rails.forEach(function(o){var r=o.r;if(!o.vis||d.hidden||Date.now()<o.hold){o.pos=r.scrollLeft;return}
  o.pos+=dt*o.speed;if(o.half&&o.pos>=o.half)o.pos-=o.half;r.scrollLeft=o.pos});requestAnimationFrame(tick)}requestAnimationFrame(tick)})();
/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Site: xado. Skips the preview host. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0;
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function send(){var n=Date.now();if(n-last<1500)return;last=n;try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'xado',cta_type:'whatsapp',session_id:sid(),page_path:location.pathname.slice(0,200),device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200)})}).catch(function(){})}catch(e){}}
window.p1WaTap=send;d=document;d.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send()},true)})();

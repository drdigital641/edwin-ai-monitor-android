/* MCS Auto Spray Painting site script: menu sheet, header on scroll, floating bar, service-zone selector, booth tape peel,
   Wrapstar glide gallery. No libraries; every page reads fully without it. */
(function(){var d=document;d.documentElement.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
/* menu sheet */
var mb=d.querySelector('.mb'),sh=d.getElementById('sheet');
if(mb&&sh){var close=function(){sh.hidden=true;mb.setAttribute('aria-expanded','false');d.body.style.overflow='';mb.focus()};
  mb.addEventListener('click',function(){sh.hidden=false;mb.setAttribute('aria-expanded','true');d.body.style.overflow='hidden';var x=sh.querySelector('.sheet-x');x&&x.focus()});
  sh.addEventListener('click',function(e){if(e.target===sh||e.target.closest('.sheet-x')||e.target.closest('a'))close()});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!sh.hidden)close()})}
/* header: transparent over the hero, solid dark metallic after 24px */
var top=d.querySelector('.top');
if(top){var sol=function(){top.classList.toggle('solid',(window.scrollY||0)>24)};sol();addEventListener('scroll',sol,{passive:true})}
/* floating WhatsApp bar waits until the hero buttons scroll away */
var hc=d.querySelector('.hero-cta,.ph .btns'),mbar=d.querySelector('.mbar');
if(hc&&mbar&&'IntersectionObserver' in window){new IntersectionObserver(function(es){mbar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc)}
/* service-zone selector (tabs; without JS every zone is listed) */
[].forEach.call(d.querySelectorAll('.zones'),function(z){var tabs=[].slice.call(z.querySelectorAll('[role=tab]'));
  function pick(t,focus){tabs.forEach(function(b){var on=b===t;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;
    var p=d.getElementById(b.getAttribute('aria-controls'));p&&p.classList.toggle('on',on)});
    if(focus)t.focus();var r=t.parentNode;if(r.scrollWidth>r.clientWidth){r.scrollTo({left:t.offsetLeft-16,behavior:reduce?'auto':'smooth'})}}
  tabs.forEach(function(b,i){b.addEventListener('click',function(){pick(b)});
    b.addEventListener('keydown',function(e){var k=e.key,n=null;if(k==='ArrowRight'||k==='ArrowDown')n=tabs[(i+1)%tabs.length];
      if(k==='ArrowLeft'||k==='ArrowUp')n=tabs[(i-1+tabs.length)%tabs.length];if(n){e.preventDefault();pick(n,true)}})})});
/* booth doors: the masking tape peels once the steps come into view */
var bo=d.querySelectorAll('.booth');
if(reduce||!('IntersectionObserver' in window)){[].forEach.call(bo,function(e){e.classList.add('in')})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -15% 0px',threshold:.2});
  [].forEach.call(bo,function(e){io.observe(e)})}
});
})();
/* Wrapstar glide: native finger drag (overflow-x auto, no touch-action:pan-y), rAF autoplay with clones; vertical page scroll never
   pauses it; a ~350ms hold or a sideways drag pauses it, resuming 1.5s after release; hover pauses on desktop; arrows step one photo.
   prefers-reduced-motion: no autoplay (arrows and swipe still work). */
(function(){var d=document,reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,RESUME=1500;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.gl'),function(g){var r=g.querySelector('.glide');if(!r)return;
  var kids=[].slice.call(r.children),o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.04)};
  var hold=function(){o.hold=Date.now()+RESUME};
  [].forEach.call(g.querySelectorAll('.arr'),function(b){b.addEventListener('click',function(){var w=kids[0].getBoundingClientRect().width+14;
    o.hold=Date.now()+RESUME+600;r.scrollBy({left:w*(+b.getAttribute('data-dir')),behavior:reduce?'auto':'smooth'})})});
  if(reduce||r.scrollWidth<=r.clientWidth+4)return;
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});
    [].forEach.call(c.querySelectorAll('img'),function(i){i.setAttribute('alt','')});r.appendChild(c)});
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;hold()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mousedown',function(){o.hold=Infinity});addEventListener('mouseup',function(){if(o.hold===Infinity&&!touching)hold()});
  g.addEventListener('pointerenter',function(e){if(e.pointerType==='mouse')o.hold=Infinity});g.addEventListener('pointerleave',function(e){if(e.pointerType==='mouse')hold()});
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))hold()},{passive:true});
  r.addEventListener('focusin',function(){o.hold=Infinity});r.addEventListener('focusout',hold);
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

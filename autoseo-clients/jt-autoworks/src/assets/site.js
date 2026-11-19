/* JT Autoworks site script: menu sheet, scroll reveal, tap-to-load Facebook reels, self-hosted video sound toggle,
   Wrapstar-style 4:5 photo rail. No libraries; the page reads fully without it. */
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

/* reveal once (shown at once with reduced motion or no IntersectionObserver) */
var rvs=d.querySelectorAll('.rv');
if(reduce||!('IntersectionObserver' in window)){[].forEach.call(rvs,function(e){e.classList.add('in')})}
else{var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}})},{rootMargin:'0px 0px -10% 0px',threshold:.1});
  [].forEach.call(rvs,function(e){ro.observe(e)})}

/* Facebook reel facades: no Facebook script or frame until a tap */
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.vf-b');if(!b)return;
  var f=d.createElement('iframe');f.src=b.getAttribute('data-src');f.title=b.getAttribute('aria-label');
  f.setAttribute('allow','autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share');f.setAttribute('allowfullscreen','');
  b.parentNode.replaceChild(f,b)});

/* self-hosted hero video: muted autoplay unless reduced motion (then poster only); "Tap for sound" */
[].forEach.call(d.querySelectorAll('.vf-own'),function(w){var v=w.querySelector('video'),s=w.querySelector('.vf-snd');
  if(!reduce){v.preload='auto';var p=v.play();p&&p.catch&&p.catch(function(){})}
  s&&s.addEventListener('click',function(){v.muted=!v.muted;if(!v.muted&&v.paused)v.play();s.setAttribute('aria-pressed',v.muted?'false':'true')})});

/* photo rail: native finger drag (overflow-x auto, no touch-action), rAF glide with clones. Vertical page scroll never
   pauses it; a ~350ms hold or a sideways drag pauses it; it resumes 1.5s after release. Reduced motion: no glide. */
[].forEach.call(d.querySelectorAll('.rail'),function(w){var r=w.querySelector('.rail-t'),dots=[].slice.call(w.querySelectorAll('.dots i'));
  var kids=[].slice.call(r.children),n=kids.length,gap=12;if(!n)return;
  var step=function(){return kids[0].offsetWidth+gap};
  var mark=function(){if(!dots.length)return;var i=Math.round(r.scrollLeft/step())%n;dots.forEach(function(x,k){x.classList.toggle('on',k===i)})};
  r.addEventListener('scroll',mark,{passive:true});mark();
  var o={pos:r.scrollLeft,hold:0,vis:true,half:0,speed:.04};
  var later=function(){o.hold=Date.now()+1500};
  [].forEach.call(w.querySelectorAll('.arr'),function(b){b.addEventListener('click',function(){o.hold=Date.now()+4000;
    r.scrollBy({left:(+b.getAttribute('data-dir'))*step(),behavior:reduce?'auto':'smooth'})})});
  if(reduce)return;
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');r.appendChild(c)});
  var measure=function(){o.half=r.children[n].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  if(r.scrollWidth<=r.clientWidth+4)return;
  var sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;later()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mouseenter',function(){o.hold=Infinity});r.addEventListener('mouseleave',later);
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))later()},{passive:true});
  r.addEventListener('focusin',function(){o.hold=Date.now()+4000});
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);
  var last=0;
  function tick(t){var dt=last?Math.min(64,t-last):16;last=t;
    if(!o.vis||d.hidden||Date.now()<o.hold){o.pos=r.scrollLeft}
    else{o.pos+=dt*o.speed;if(o.half&&o.pos>=o.half)o.pos-=o.half;r.scrollLeft=o.pos}
    requestAnimationFrame(tick)}
  requestAnimationFrame(tick)});
})})();

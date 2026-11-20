/* Advance Machinery Movers site JS (20 Nov 2026). No libraries. Content is fully visible without JS.
   1. menu sheet  2. header turns white with charcoal type after 24px on the photo hero (autoseo-template/blocks.js)
   3. sticky WhatsApp + Call bar hidden while the hero buttons are on screen (blocks.js)
   4. work carousel = Wrapstar glide (ws.js): native finger drag, rAF autoplay writing scrollLeft over cloned children for a
      seamless loop; vertical page scroll never pauses it (passive listeners, no preventDefault); a ~350ms still hold or a
      sideways drag (dx > 8 and dx > dy) pauses; autoplay resumes from the finger's position 1.5 s after release; hover and
      focus pause only on devices with a real hover pointer; prefers-reduced-motion = no autoplay (arrows still work). */
(function(){var d=document,w=window;d.documentElement.classList.add('js');
var reduce=w.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var hover=w.matchMedia&&matchMedia('(hover: hover) and (pointer: fine)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
/* 1 menu */
var mb=d.querySelector('.mb'),sh=d.getElementById('sheet');
function close(){if(!sh||sh.hidden)return;sh.hidden=true;mb.setAttribute('aria-expanded','false');d.body.style.overflow='';mb.focus()}
if(mb&&sh){mb.addEventListener('click',function(){sh.hidden=false;mb.setAttribute('aria-expanded','true');d.body.style.overflow='hidden';var x=sh.querySelector('.sheet-x');x&&x.focus()});
  sh.addEventListener('click',function(e){if(e.target===sh||e.target.closest('.sheet-x'))close()});
  d.addEventListener('keydown',function(e){if(e.key==='Escape')close()})}
/* 2 header */
var top=d.querySelector('.over .top');
if(top){var sol=function(){top.classList.toggle('solid',(w.scrollY||0)>24)};sol();w.addEventListener('scroll',sol,{passive:true})}
/* 3 sticky bar */
var hc=d.querySelector('.hero-cta'),mbar=d.querySelector('.mbar');
if(hc&&mbar&&'IntersectionObserver' in w){new IntersectionObserver(function(es){mbar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc)}
/* 4 glide */
var rails=[];
[].forEach.call(d.querySelectorAll('.glide'),function(r){
  var o={r:r,pos:0,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.035),auto:false};
  var kids=[].slice.call(r.children);
  var arrows=r.parentNode.querySelectorAll('.arr');
  var step=function(){var c=r.children[0];return c?c.getBoundingClientRect().width+14:300};
  [].forEach.call(arrows,function(a){a.addEventListener('click',function(){var dir=+a.getAttribute('data-dir');o.hold=Date.now()+2500;
    var t=r.scrollLeft+dir*step();if(o.half&&t<0)t+=o.half,r.scrollLeft+=o.half;r.scrollTo({left:t,behavior:reduce?'auto':'smooth'})})});
  if(reduce||r.scrollWidth<=r.clientWidth+4)return;
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});
    [].forEach.call(c.querySelectorAll('img'),function(i){i.setAttribute('alt','')});r.appendChild(c)});
  r.classList.add('auto');o.auto=true;o.pos=r.scrollLeft;
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();w.addEventListener('resize',measure);
  var hold=function(){o.hold=Date.now()+1500},sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;hold()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mousedown',function(){o.hold=Infinity});w.addEventListener('mouseup',function(){if(o.hold===Infinity&&!touching)hold()});
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))hold()},{passive:true});
  if(hover){r.addEventListener('mouseenter',function(){o.hover=true});r.addEventListener('mouseleave',function(){o.hover=false});
    r.addEventListener('focusin',function(){o.hold=Infinity});r.addEventListener('focusout',hold)}
  if('IntersectionObserver' in w)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);else o.vis=true;
  rails.push(o)});
if(!rails.length)return;
var last=0;
function tick(t){var dt=last?Math.min(64,t-last):16;last=t;
  rails.forEach(function(o){var r=o.r;
    if(!o.vis||d.hidden||o.hover||Date.now()<o.hold){o.pos=r.scrollLeft;if(o.half&&o.pos>=o.half){o.pos-=o.half;r.scrollLeft=o.pos}return}
    o.pos+=dt*o.speed;
    if(o.half&&o.pos>=o.half)o.pos-=o.half;
    r.scrollLeft=o.pos});
  requestAnimationFrame(tick)}
requestAnimationFrame(tick);
})})();

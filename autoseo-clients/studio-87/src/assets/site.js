/* Studio 87 site JS (AutoSEO template blocks, 20 Nov 2026). No libraries.
   Header solid after 24px (shared blocks.js), menu sheet, mobile bar hidden while the hero buttons show,
   Wrapstar-style work rail: native finger drag, rAF autoplay on scrollLeft with cloned children for a seamless loop.
   Vertical page scroll never pauses it (passive touch listeners, no preventDefault). A ~350ms still hold or a sideways
   drag (dx > 8 and dx > dy) pauses; autoplay resumes from the finger's position 1.5s after release.
   No focus or hover pause on touch devices. prefers-reduced-motion: no autoplay. */
(function(){var d=document,h=d.documentElement;h.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var touchDev=window.matchMedia&&matchMedia('(hover: none)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
/* header */
var top=d.querySelector('.top');
if(top){var sol=function(){top.classList.toggle('solid',(window.scrollY||0)>24)};sol();addEventListener('scroll',sol,{passive:true})}
/* menu sheet */
var sh=d.getElementById('sheet'),mb=d.querySelector('.mb');
function setSheet(o){if(!sh)return;sh.hidden=!o;mb&&mb.setAttribute('aria-expanded',o);h.classList.toggle('noscroll',o);if(o){var x=sh.querySelector('.sheet-x');x&&x.focus()}else mb&&mb.focus()}
mb&&mb.addEventListener('click',function(){setSheet(sh.hidden)});
sh&&sh.addEventListener('click',function(e){if(e.target===sh||e.target.closest('.sheet-x'))setSheet(false)});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sh&&!sh.hidden)setSheet(false)});
/* mobile bar off while the hero / page-head buttons are on screen */
var hc=d.querySelector('.hero-cta'),mbar=d.querySelector('.mbar');
if(hc&&mbar&&'IntersectionObserver' in window){new IntersectionObserver(function(es){mbar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc)}
/* rails */
var rails=[];
[].forEach.call(d.querySelectorAll('.rail'),function(wrap){
  var r=wrap.querySelector('.glide');if(!r)return;
  var o={r:r,pos:0,hold:0,vis:false,half:0,auto:false,speed:+(r.getAttribute('data-speed')||0.035)};
  var step=function(){var c=r.children[0];return c?c.getBoundingClientRect().width+parseFloat(getComputedStyle(r).columnGap||16):300};
  [].forEach.call(wrap.querySelectorAll('.rn'),function(b){b.addEventListener('click',function(){
    o.hold=Date.now()+4000;r.scrollBy({left:step()*(+b.getAttribute('data-dir')),behavior:reduce?'auto':'smooth'})})});
  if(reduce||r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');
    [].forEach.call(c.querySelectorAll('a,button,img'),function(a){a.setAttribute('tabindex','-1');if(a.tagName==='IMG')a.setAttribute('alt','')});r.appendChild(c)});
  r.classList.add('auto');o.auto=true;o.pos=r.scrollLeft;
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var resume=function(){o.hold=Date.now()+1500},sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;resume()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  if(!touchDev){r.addEventListener('mouseenter',function(){o.hold=Infinity});r.addEventListener('mouseleave',resume);
    r.addEventListener('focusin',function(){o.hold=Infinity});r.addEventListener('focusout',resume)}
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))resume()},{passive:true});
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
requestAnimationFrame(tick);
})})();

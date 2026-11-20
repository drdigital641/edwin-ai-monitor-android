/* Hock Chuan Hiong site JS (no libraries). Menu sheet, floating WhatsApp bar (hidden while the first-screen buttons show),
   and the Wrapstar glide carousel (ws.js behaviour: continuous loop, never stops for page scroll; pauses while held or slid
   sideways, plus hover and arrow taps per house rule 0.11; reduced motion = still swipe row with arrows). */
(function(){var d=document;d.documentElement.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
var sh=d.getElementById('sheet'),mb=d.querySelector('.mb');
function open(o){if(!sh)return;sh.hidden=!o;mb&&mb.setAttribute('aria-expanded',o?'true':'false');d.documentElement.style.overflow=o?'hidden':'';if(o){var x=sh.querySelector('.sheet-x');x&&x.focus()}else{mb&&mb.focus()}}
mb&&mb.addEventListener('click',function(){open(true)});
sh&&sh.addEventListener('click',function(e){if(e.target===sh||e.target.closest('.sheet-x'))open(false)});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sh&&!sh.hidden)open(false)});
var hc=d.querySelector('.hero-cta, .ph .btns'),mbar=d.querySelector('.mbar');
if(hc&&mbar&&'IntersectionObserver' in window){new IntersectionObserver(function(es){mbar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc)}
/* arrows: scroll one card and hold the glide for 3s */
[].forEach.call(d.querySelectorAll('.gl'),function(g){var r=g.querySelector('.glide');
  [].forEach.call(g.querySelectorAll('.arr'),function(b){b.addEventListener('click',function(){var c=r.querySelector('li');var w=c?c.getBoundingClientRect().width+16:300;
    r.__hold&&r.__hold();r.scrollBy({left:w*(+b.getAttribute('data-dir')),behavior:reduce?'auto':'smooth'})})})});
});
})();
/* continuous glide on carousels: loops, pauses only when held, hovered or swiped sideways; page scrolling never pauses it */
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.glide'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');c.removeAttribute('id');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});
    [].forEach.call(c.querySelectorAll('img'),function(i){i.setAttribute('alt','')});r.appendChild(c)});
  r.classList.add('auto');
  var o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.04)};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var hold=function(){o.hold=Date.now()+3000},sx=0,sy=0,touching=false,grab=false,tm=0;r.__hold=hold;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;hold()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mousedown',function(){o.hold=Infinity});addEventListener('mouseup',function(){if(o.hold===Infinity&&!touching)hold()});
  r.addEventListener('mouseenter',function(){if(!touching)o.hold=Infinity});r.addEventListener('mouseleave',function(){if(!touching)hold()});
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

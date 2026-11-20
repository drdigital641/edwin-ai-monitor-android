/* LT Automart site JS (no libraries): menu sheet, upgrade-menu tabs, floating WhatsApp bar (hidden while the first-screen
   buttons show), and the Wrapstar glide carousel (ws.js behaviour: continuous rAF loop with clones, never stops for page
   scroll; 350ms hold or a sideways drag pauses it, resumes 1.5s after release; hover and arrow taps pause per house rule
   0.11; reduced motion = still swipe row with arrows). Content is fully visible with JS off. */
(function(){var d=document;d.documentElement.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
var sh=d.getElementById('sheet'),mb=d.querySelector('.burger');
function open(o){if(!sh)return;sh.hidden=!o;mb&&mb.setAttribute('aria-expanded',o?'true':'false');d.documentElement.style.overflow=o?'hidden':'';if(o){var x=sh.querySelector('.sheet-x');x&&x.focus()}else{mb&&mb.focus()}}
mb&&mb.addEventListener('click',function(){open(true)});
sh&&sh.addEventListener('click',function(e){if(e.target===sh||e.target.closest('.sheet-x'))open(false)});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sh&&!sh.hidden)open(false)});
/* upgrade menu tabs */
[].forEach.call(d.querySelectorAll('.upg'),function(m){var tabs=[].slice.call(m.querySelectorAll('.upg-chip'));
  function show(t,focus){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;
    var p=d.getElementById(x.getAttribute('aria-controls'));p&&p.classList.toggle('on',on)});if(focus)t.focus();
    t.scrollIntoView&&t.parentNode.scrollTo&&t.parentNode.scrollTo({left:t.offsetLeft-24,behavior:reduce?'auto':'smooth'})}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){show(t)});
    t.addEventListener('keydown',function(e){var k=e.key==='ArrowRight'?1:e.key==='ArrowLeft'?-1:0;if(k){e.preventDefault();show(tabs[(i+k+tabs.length)%tabs.length],true)}})});
  tabs[0]&&show(tabs[0])});
/* floating bar off while hero / page-head buttons are on screen */
var hc=d.querySelector('.nh-cta, .page-head .btns'),bar=d.querySelector('.float-bar');
if(hc&&bar&&'IntersectionObserver' in window){new IntersectionObserver(function(es){bar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc)}
/* carousel arrows: scroll one card and hold the glide */
[].forEach.call(d.querySelectorAll('.bay-rail'),function(g){var r=g.querySelector('.rail');
  [].forEach.call(g.querySelectorAll('.rail-btn'),function(b){b.addEventListener('click',function(){var c=r.querySelector('li');var w=c?c.getBoundingClientRect().width+16:300;
    r.__hold&&r.__hold(3000);r.scrollBy({left:w*(+b.getAttribute('data-dir')),behavior:reduce?'auto':'smooth'})})})});
});
})();
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.rail'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.removeAttribute('id');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});
    [].forEach.call(c.querySelectorAll('img'),function(i){i.setAttribute('alt','')});r.appendChild(c)});
  r.classList.add('auto');
  var o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.035)};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var hold=function(ms){o.hold=Date.now()+(ms||1500)},sx=0,sy=0,touching=false,grab=false,tm=0;r.__hold=hold;
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
  r.addEventListener('focusin',function(){hold(3000)});
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

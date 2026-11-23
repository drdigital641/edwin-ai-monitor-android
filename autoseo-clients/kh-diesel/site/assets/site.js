/* KH Diesel site.js v2 (precision lab): menu sheet, sticky bar, carousel arrows, HUD counter, timeline glow. Carousel glide copied from the Wrapstar reference. */
(function(){var d=document;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  /* close the menu sheet after a link tap or Escape */
  var sh=d.querySelector('.sheet');
  if(sh){sh.addEventListener('click',function(e){if(e.target.closest('.sheet-in a'))sh.open=false});
    d.addEventListener('keydown',function(e){if(e.key==='Escape')sh.open=false})}
  /* sticky bar hides while the hero buttons are on screen */
  var bar=d.querySelector('.mbar'),hc=d.querySelector('.hx-ctas');
  if(bar&&hc&&'IntersectionObserver' in window)new IntersectionObserver(function(es){bar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc);
  /* arrows: move one card, then the glide resumes 1.5 s later (hold set by the scroll listener below) */
  [].forEach.call(d.querySelectorAll('.rail-wrap'),function(w){var r=w.querySelector('.glide');if(!r)return;
    [].forEach.call(w.querySelectorAll('.rn'),function(b){b.addEventListener('click',function(){var c=r.querySelector('.gcard');var step=c?c.getBoundingClientRect().width+14:280;
      r.dispatchEvent(new Event('focusin'));r.scrollBy({left:b.classList.contains('prev')?-step:step,behavior:'smooth'})})})});
});
})();
/* continuous glide on carousels: loops, pauses only when held or swiped sideways; page scrolling never pauses it (Wrapstar reference) */
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
  var hold=function(){o.hold=Date.now()+1500},sx=0,sy=0,touching=false,grab=false,tm=0;
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
/* lab motion: HUD pressure count-up, fuel-flow line length, timeline glow. Light: one rAF per scroll, only while a section is on screen. */
(function(){var d=document,w=window,rm=w.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.documentElement.classList.add('js');
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  /* HUD counter 0 -> data-to (visual effect only) */
  [].forEach.call(d.querySelectorAll('.cnt'),function(el){var to=+el.getAttribute('data-to')||0,bar=el.closest('.rd')&&el.closest('.rd').querySelector('.rd-bar i');
    var fmt=function(n){return Math.round(n).toLocaleString('en-US')};if(rm){el.textContent=fmt(to);return}
    var t0=0,dur=2600;el.textContent='0';function step(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-k,3);
      el.textContent=fmt(to*e+(k<1?Math.random()*6:0));if(bar)bar.style.setProperty('--p',(e*100).toFixed(1)+'%');if(k<1)requestAnimationFrame(step)}
    setTimeout(function(){requestAnimationFrame(step)},350)});
  /* fuel-flow line: set travel distance for the glowing pulse */
  var fl=d.querySelector('.flow-line');function flow(){if(!fl)return;fl.style.setProperty('--h',fl.offsetHeight+'px');fl.style.setProperty('--w',fl.offsetWidth+'px')}
  flow();w.addEventListener('resize',flow);
  /* light each diagram node as the pulse passes on phones (cheap: on scroll position) */
  var nodes=[].slice.call(d.querySelectorAll('.node'));
  /* scroll-driven sections */
  var tl=d.querySelector('.tline'),items=tl?[].slice.call(tl.children):[],live={},q=false;
  function upd(){q=false;var vh=w.innerHeight;
    if(tl&&live.tl){var r2=tl.getBoundingClientRect(),p2=Math.min(1,Math.max(0,(vh*.62-r2.top)/r2.height));tl.style.setProperty('--tp',p2.toFixed(3));
      items.forEach(function(li){li.classList.toggle('on',li.getBoundingClientRect().top+20<vh*.62)})}
    if(nodes.length&&live.diag){nodes.forEach(function(n){var b=n.getBoundingClientRect();n.classList.toggle('lit',b.top<vh*.6&&b.bottom>vh*.25)})}}
  function onScroll(){if(!q){q=true;requestAnimationFrame(upd)}}
  if('IntersectionObserver' in w){var io=new IntersectionObserver(function(es){es.forEach(function(e){live[e.target.getAttribute('data-k')]=e.isIntersecting});onScroll()},{rootMargin:'10% 0px'});
    if(tl){tl.setAttribute('data-k','tl');io.observe(tl)}
    var dg=d.querySelector('.diag');if(dg){dg.setAttribute('data-k','diag');io.observe(dg)}}
  else{live={tl:1,diag:1}}
  if(rm)items.forEach(function(li){li.classList.add('on')}),tl&&tl.style.setProperty('--tp','1');
  w.addEventListener('scroll',onScroll,{passive:true});w.addEventListener('resize',onScroll);upd();
  /* gentle reveal for panels below the fold */
  if(!rm&&'IntersectionObserver' in w){var rv=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');rv.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    [].forEach.call(d.querySelectorAll('main .band .wrap>*:not(.flow-wrap),.idplate,.map-card,.cr-copy'),function(el){if(el.getBoundingClientRect().top>w.innerHeight){el.classList.add('rv');rv.observe(el)}})}
});
})();

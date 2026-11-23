/* SgAutobots preview site.js (23 Nov 2026). Content works with JS off; this only adds the size switcher, glide, video swap and the Book switch. */
(function(){var d=document,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
var ROOT=(d.documentElement.getAttribute('data-root')||'/');
ready(function(){
 /* S/M/L/XL switcher: one tap updates every price card on the page */
 var sw=[].slice.call(d.querySelectorAll('.sizes button'));
 function setSize(i){sw.forEach(function(b){b.setAttribute('aria-pressed',String(+b.getAttribute('data-i')===i))});
  [].forEach.call(d.querySelectorAll('[data-prices]'),function(el){var p=el.getAttribute('data-prices').split(','),v=p[i];
   var o=el.querySelector('.v');if(!o)return;if(v&&v!=='-'){o.textContent='S$'+Number(v).toLocaleString('en-SG');el.classList.remove('na')}else{o.textContent='Ask us';el.classList.add('na')}
   var s=el.querySelector('.sz');if(s)s.textContent=['S','M','L','XL'][i]});
  [].forEach.call(d.querySelectorAll('.tbl tr[data-i]'),function(tr){tr.classList.toggle('on',+tr.getAttribute('data-i')===i)});
  try{sessionStorage.setItem('sga_size',i)}catch(e){}}
 sw.forEach(function(b){b.addEventListener('click',function(){setSize(+b.getAttribute('data-i'))})});
 if(sw.length){var s0=0;try{s0=+(sessionStorage.getItem('sga_size')||0)}catch(e){}setSize(s0)}
 /* Book button: one config value (site-config.json booking_url). Empty = WhatsApp booking prefill already in the HTML */
 try{fetch(ROOT+'site-config.json',{cache:'no-cache'}).then(function(r){return r.ok?r.json():null}).then(function(c){if(!c)return;
  if(c.booking_url){[].forEach.call(d.querySelectorAll('a[data-cta="booking"]'),function(a){var u;try{u=new URL(c.booking_url)}catch(e){return}
   u.searchParams.set('client','sg-autobots');var sv=a.getAttribute('data-service');if(sv)u.searchParams.set('service',sv);a.href=u.toString()})}
  if(c.videos_live)liveVideos()}).catch(function(){})}catch(e){}
 function liveVideos(){[].forEach.call(d.querySelectorAll('.reel[data-src]'),function(a){var f=a.querySelector('.frame'),im=f.querySelector('img');
   var v=d.createElement('video');v.muted=true;v.setAttribute('muted','');v.setAttribute('playsinline','');v.loop=a.getAttribute('data-loop')==='1';v.preload='none';v.poster=im.currentSrc||im.src;v.setAttribute('aria-label',im.alt);
   v.src=ROOT+a.getAttribute('data-src');f.insertBefore(v,f.firstChild);im.style.visibility='hidden';
   if(!rm&&'IntersectionObserver' in window&&v.loop){new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){v.play().then(function(){a.classList.add('playing')}).catch(function(){})}else v.pause()})},{threshold:.5}).observe(a)}
   a.addEventListener('click',function(ev){var full=a.getAttribute('data-full');if(!full)return;ev.preventDefault();openFull(ROOT+full,v.poster)})})}
 function openFull(src,poster){var dl=d.createElement('dialog');dl.className='vd';dl.innerHTML='<video controls playsinline autoplay></video><button type="button" aria-label="Close">&times;</button>';
   var v=dl.querySelector('video');v.src=src;v.poster=poster;d.body.appendChild(dl);dl.showModal();
   dl.addEventListener('close',function(){v.pause();dl.remove()});dl.querySelector('button').onclick=function(){dl.close()};dl.addEventListener('click',function(e){if(e.target===dl)dl.close()})}
});
/* continuous glide (copied from the Wrapstar reference): loops, pauses only when held or swiped sideways; page scrolling never pauses it; resumes 1.5 s after release */
if(rm)return;
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.glide'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.removeAttribute('id');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});[].forEach.call(c.querySelectorAll('img'),function(i){i.setAttribute('loading','lazy')});r.appendChild(c)});
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
  r.addEventListener('mouseenter',function(){o.hold=Infinity});r.addEventListener('mouseleave',hold);
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

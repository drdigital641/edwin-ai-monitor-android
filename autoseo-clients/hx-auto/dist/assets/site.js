/* HX Auto Service site script: menu sheet, car diagram tabs, scan bar fill, lightbox for the -full photos, Wrapstar-style work carousel. No libraries. */
(function(){var d=document,R=d.documentElement;R.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
/* menu sheet */
var mb=d.querySelector('.hb-menu'),sh=d.getElementById('sheet');
if(mb&&sh){var close=function(){sh.hidden=true;mb.setAttribute('aria-expanded','false');d.body.style.overflow=''};
  mb.addEventListener('click',function(){sh.hidden=false;mb.setAttribute('aria-expanded','true');d.body.style.overflow='hidden';var x=sh.querySelector('.sheet-x');x&&x.focus()});
  sh.addEventListener('click',function(e){if(e.target===sh||e.target.closest('.sheet-x')||e.target.closest('a'))close()});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!sh.hidden)close()})}


/* car diagram: tabs are the controls; the SVG marker follows. Markers also take a mouse click. */
[].forEach.call(d.querySelectorAll('.dg'),function(g){var tabs=[].slice.call(g.querySelectorAll('.zt')),ps=g.querySelectorAll('.zp'),ms=g.querySelectorAll('.zm');
  function pick(z,focus){tabs.forEach(function(t){var on=t.getAttribute('data-z')===z;t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;if(on&&focus)t.focus()});
    [].forEach.call(ps,function(p){p.classList.toggle('on',p.getAttribute('data-z')===z)});[].forEach.call(ms,function(m){m.classList.toggle('on',m.getAttribute('data-z')===z)})}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){pick(t.getAttribute('data-z'))});
    t.addEventListener('keydown',function(e){var k=e.key==='ArrowRight'||e.key==='ArrowDown'?1:e.key==='ArrowLeft'||e.key==='ArrowUp'?-1:0;if(k){e.preventDefault();pick(tabs[(i+k+tabs.length)%tabs.length].getAttribute('data-z'),true)}})});
  [].forEach.call(ms,function(m){m.addEventListener('click',function(){pick(m.getAttribute('data-z'))})});
  pick(g.getAttribute('data-zone'))});

/* scan bar fills once it scrolls into view (end state shown with no JS or reduced motion) */
[].forEach.call(d.querySelectorAll('.sb'),function(b){if(reduce||!('IntersectionObserver' in window)){b.classList.add('go');return}
  var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){b.classList.add('go');io.disconnect()}},{threshold:.35});io.observe(b)});

/* lightbox for the -full photos; a drag on the rail never opens it */
var lb=d.getElementById('lb'),moved=false;
if(lb&&lb.showModal){var li=lb.querySelector('img'),lc=lb.querySelector('.lb-c');
  d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.ph-b');if(!b||moved)return;
    li.src=b.getAttribute('data-full');li.alt=b.getAttribute('data-cap');lc.textContent=b.getAttribute('data-cap');lb.showModal()});
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.closest('.lb-x'))lb.close()})}

/* work rail: native finger drag (overflow-x auto), rAF glide with clones. Vertical page scroll never pauses it;
   a ~350ms hold, a sideways drag or hover pauses it; it resumes 1.5s after release. Reduced motion: no glide. */
[].forEach.call(d.querySelectorAll('.wr'),function(w){var r=w.querySelector('.wr-t'),dots=[].slice.call(w.querySelectorAll('.dots i'));
  var kids=[].slice.call(r.children),n=kids.length,gap=12;
  var step=function(){return kids[0].offsetWidth+gap};
  var mark=function(){if(!dots.length)return;var i=Math.round(r.scrollLeft/step())%n;dots.forEach(function(x,k){x.classList.toggle('on',k===i)})};
  r.addEventListener('scroll',mark,{passive:true});mark();
  var o={pos:r.scrollLeft,hold:0,vis:true,half:0,speed:.045};
  var later=function(){o.hold=Date.now()+1500};
  [].forEach.call(w.querySelectorAll('.arr'),function(b){b.addEventListener('click',function(){o.hold=Date.now()+4000;
    r.scrollBy({left:(+b.getAttribute('data-dir'))*step(),behavior:reduce?'auto':'smooth'})})});
  if(reduce||r.scrollWidth<=r.clientWidth+4)return;
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});r.appendChild(c)});
  var measure=function(){o.half=r.children[n].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;moved=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(dx>8||dy>8)moved=true;
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;later()}setTimeout(function(){moved=false},60)};
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

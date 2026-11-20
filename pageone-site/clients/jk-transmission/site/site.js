/* J & K Transmission site JS (20 Nov 2026). No libraries. Content is visible without JS. */
(function(){var d=document,R=d.documentElement;R.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
/* header: transparent over the hero, white after 24px */
var h=d.querySelector('.hdr');if(h){var s=function(){h.classList.toggle('solid',(window.scrollY||0)>24)};s();addEventListener('scroll',s,{passive:true})}
/* phone bar hides while the hero WhatsApp button is on screen */
var hc=d.querySelector('[data-herocta]'),mb=d.querySelector('.mbar');
if(hc&&mb&&'IntersectionObserver' in window){new IntersectionObserver(function(e){mb.classList.toggle('off',e[0].isIntersecting)}).observe(hc)}
/* menu sheet */
var sh=d.getElementById('sheet'),mo=d.querySelector('.menu');
function shut(){sh.classList.remove('open');mo.setAttribute('aria-expanded','false');R.style.overflow=''}
if(sh&&mo){mo.addEventListener('click',function(){sh.classList.add('open');mo.setAttribute('aria-expanded','true');R.style.overflow='hidden';var f=sh.querySelector('a');f&&f.focus()});
 sh.querySelector('.sheet-x').addEventListener('click',shut);d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sh.classList.contains('open'))shut()})}
/* symptom selector: one diagnosis pointer + WhatsApp with that symptom in the prefill */
[].forEach.call(d.querySelectorAll('[data-sel]'),function(w){var ins=w.querySelectorAll('input[type=radio]');
 function show(){[].forEach.call(ins,function(i){var p=d.getElementById('dx-'+i.value);if(p)p.classList.toggle('on',i.checked)})}
 [].forEach.call(ins,function(i){i.addEventListener('change',show)});show()});
/* map facade: no Google request until tapped */
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.map-b');if(!b)return;var f=d.createElement('iframe');
 f.src=b.getAttribute('data-src');f.title=b.getAttribute('data-title');f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.setAttribute('allowfullscreen','');b.parentNode.replaceChild(f,b)});
/* contact form: builds the WhatsApp message to Jason (nothing is stored on this site) */
var wf=d.querySelector('form[data-wa]');if(wf)wf.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=wf.elements[n];return x?String(x.value||'').trim():''};
 var m=wf.getAttribute('data-prefill')+(g('car')||'')+(g('issue')?'\nIssue: '+g('issue'):'')+(g('msg')?'\n'+g('msg'):'')+(g('name')?'\nName: '+g('name'):'');
 location.href='https://wa.me/'+wf.getAttribute('data-wa')+'?text='+encodeURIComponent(m)});
/* photo strip: Wrapstar carousel behaviour. Native horizontal finger swipe (overflow-x:auto, scroll-snap proximity),
   continuous rAF autoplay over clones (snap off only while autoplaying), vertical page scroll never pauses it,
   a horizontal swipe, a ~350ms hold or mouse hover pauses, resume 1.5s after release, reduced motion = no autoplay. */
[].forEach.call(d.querySelectorAll('[data-strip]'),function(st){var vp=st.querySelector('.strip-vp'),tr=st.querySelector('.strip-tr');if(!vp||!tr)return;
 var orig=[].slice.call(tr.children);orig.forEach(function(c){var k=c.cloneNode(true);k.setAttribute('aria-hidden','true');[].forEach.call(k.querySelectorAll('img'),function(i){i.loading='lazy';i.alt=''});tr.appendChild(k)});
 var W=0,pos=0,v=reduce?0:32,user=false,hover=false,rt=0,last=0,vis=true,mine=0;
 function measure(){W=tr.children[orig.length].offsetLeft-tr.children[0].offsetLeft}
 function auto(on){vp.classList.toggle('auto',on)}
 function hold(){user=true;clearTimeout(rt);auto(false)}
 function release(){clearTimeout(rt);rt=setTimeout(function(){user=false;pos=vp.scrollLeft},1500)}
 function step(t){var dt=last?Math.min(64,t-last):16;last=t;
  if(!user&&!hover&&vis&&v&&W){auto(true);if(Math.abs(vp.scrollLeft-Math.round(pos))>2)pos=vp.scrollLeft;pos+=v*dt/1000;if(pos>=W)pos-=W;mine=t;vp.scrollLeft=Math.round(pos)}
  requestAnimationFrame(step)}
 measure();addEventListener('resize',measure);
 if('IntersectionObserver' in window)new IntersectionObserver(function(e){vis=e[0].isIntersecting}).observe(vp);
 requestAnimationFrame(step);
 /* touch: decide direction; vertical drags are left to the page and never pause */
 var sx=0,sy=0,dir='',ht=0;
 vp.addEventListener('touchstart',function(e){var p=e.touches[0];sx=p.clientX;sy=p.clientY;dir='';clearTimeout(ht);ht=setTimeout(function(){if(!dir){dir='hold';hold()}},350)},{passive:true});
 vp.addEventListener('touchmove',function(e){if(dir)return;var p=e.touches[0],dx=Math.abs(p.clientX-sx),dy=Math.abs(p.clientY-sy);
  if(dx>8&&dx>dy){dir='x';clearTimeout(ht);hold()}else if(dy>8){dir='y';clearTimeout(ht)}},{passive:true});
 vp.addEventListener('touchend',function(){clearTimeout(ht);if(dir==='x'||dir==='hold')release();dir=''},{passive:true});
 vp.addEventListener('touchcancel',function(){clearTimeout(ht);if(dir==='x'||dir==='hold')release();dir=''},{passive:true});
 /* trackpad / wheel / momentum scrolls that are not ours count as the user; loop the clones both ways */
 vp.addEventListener('scroll',function(){if(performance.now()-mine<60)return;/* our own autoplay step */
  if(W&&user){if(vp.scrollLeft>=W)vp.scrollLeft-=W;else if(vp.scrollLeft<=0)vp.scrollLeft+=W}
  if(user&&dir!=='x'&&dir!=='hold')release()},{passive:true});
 vp.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY)){hold();release()}},{passive:true});
 vp.addEventListener('mouseenter',function(){hover=true;auto(false)});vp.addEventListener('mouseleave',function(){hover=false;pos=vp.scrollLeft});
 function nudge(k){var c=tr.children[1].offsetLeft-tr.children[0].offsetLeft;hold();if(k<0&&vp.scrollLeft<c)vp.scrollLeft+=W;vp.scrollBy({left:k*c,behavior:reduce?'auto':'smooth'});release()}
 var pv=st.querySelector('[data-prev]'),nx=st.querySelector('[data-next]');pv&&pv.addEventListener('click',function(){nudge(-1)});nx&&nx.addEventListener('click',function(){nudge(1)});
});
})})();

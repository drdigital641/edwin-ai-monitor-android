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
/* photo strip: Wrapstar behaviour. Native finger drag, continuous rAF autoplay over clones, vertical scroll never pauses,
   only a ~350ms hold or a horizontal drag pauses, resume 1.5s after release, hover pauses (mouse), reduced motion = no autoplay. */
[].forEach.call(d.querySelectorAll('[data-strip]'),function(st){var vp=st.querySelector('.strip-vp'),tr=st.querySelector('.strip-tr');if(!vp||!tr)return;
 var orig=[].slice.call(tr.children);orig.forEach(function(c){var k=c.cloneNode(true);k.setAttribute('aria-hidden','true');[].forEach.call(k.querySelectorAll('img'),function(i){i.loading='lazy';i.alt=''});tr.appendChild(k)});
 var W=0,x=0,v=reduce?0:-32,paused=false,hover=false,rt=0,tw=null,last=0,vis=true;
 function measure(){W=tr.children[orig.length].offsetLeft-tr.children[0].offsetLeft}
 function wrap(){if(!W)return;while(x<=-W)x+=W;while(x>0)x-=W}
 function paint(){tr.style.transform='translate3d('+x.toFixed(2)+'px,0,0)'}
 function step(t){var dt=last?Math.min(64,t-last):16;last=t;
  if(tw){var p=Math.min(1,(t-tw.t0)/320),e=1-Math.pow(1-p,3);x=tw.a+(tw.b-tw.a)*e;if(p>=1)tw=null}
  else if(!paused&&!hover&&vis&&v)x+=v*dt/1000;
  wrap();paint();requestAnimationFrame(step)}
 function pause(){paused=true;clearTimeout(rt)}
 function resume(){clearTimeout(rt);rt=setTimeout(function(){paused=false},1500)}
 measure();addEventListener('resize',measure);
 if('IntersectionObserver' in window)new IntersectionObserver(function(e){vis=e[0].isIntersecting}).observe(vp);
 requestAnimationFrame(step);
 var sx=0,sy=0,bx=0,mode='',ht=0,pid=null;
 vp.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&e.button)return;sx=e.clientX;sy=e.clientY;bx=x;mode='';pid=e.pointerId;tw=null;
  clearTimeout(ht);ht=setTimeout(function(){if(!mode){mode='hold';pause()}},350);if(e.pointerType==='mouse'){mode='drag';pause();vp.setPointerCapture(pid);vp.classList.add('drag')}});
 vp.addEventListener('pointermove',function(e){if(e.pointerId!==pid)return;var dx=e.clientX-sx,dy=e.clientY-sy;
  if(!mode||mode==='hold'){if(Math.abs(dx)>8&&Math.abs(dx)>Math.abs(dy)){mode='drag';clearTimeout(ht);pause();try{vp.setPointerCapture(pid)}catch(_){}vp.classList.add('drag')}
   else if(mode!=='hold'&&Math.abs(dy)>8){mode='scroll';clearTimeout(ht)}}
  if(mode==='drag'){x=bx+dx;wrap();e.preventDefault()}});
 function up(e){if(e.pointerId!==pid)return;clearTimeout(ht);if(mode==='drag'||mode==='hold')resume();mode='';pid=null;vp.classList.remove('drag')}
 vp.addEventListener('pointerup',up);vp.addEventListener('pointercancel',up);
 vp.addEventListener('click',function(e){if(Math.abs(x-bx)>6)e.preventDefault()},true);
 vp.addEventListener('mouseenter',function(){hover=true});vp.addEventListener('mouseleave',function(){hover=false});
 function nudge(dir){var c=tr.children[1].offsetLeft-tr.children[0].offsetLeft;pause();tw={a:x,b:x-dir*c,t0:performance.now()};resume()}
 var pv=st.querySelector('[data-prev]'),nx=st.querySelector('[data-next]');pv&&pv.addEventListener('click',function(){nudge(-1)});nx&&nx.addEventListener('click',function(){nudge(1)});
});
})})();

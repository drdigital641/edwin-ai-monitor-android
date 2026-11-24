/* Sheng Heng Auto Service Centre: menu sheet, before/after sliders, warning-lamp process, photo rail, video facade. */
(function(){var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.documentElement.classList.add('js');
/* menu sheet */
var sh=d.getElementById('sheet'),ob=d.getElementById('mopen'),cb=d.getElementById('mclose');
function setSheet(o){if(!sh)return;sh.classList.toggle('open',o);sh.setAttribute('aria-hidden',o?'false':'true');if(ob)ob.setAttribute('aria-expanded',o?'true':'false');d.body.style.overflow=o?'hidden':'';if(o&&cb)cb.focus();else if(ob)ob.focus()}
if(ob)ob.addEventListener('click',function(){setSheet(true)});if(cb)cb.addEventListener('click',function(){setSheet(false)});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sh&&sh.classList.contains('open'))setSheet(false)});
/* before/after sliders: range input drives --x (finger, mouse and keyboard) */
[].forEach.call(d.querySelectorAll('.ba'),function(b){var r=b.querySelector('input');if(!r)return;function s(){b.style.setProperty('--x',r.value+'%')}r.addEventListener('input',s);s()});
/* warning lights off: lamps turn green when the list scrolls into view */
var lp=d.querySelector('.lamps');if(lp){if(RM||!('IntersectionObserver' in window))lp.classList.add('on');else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){lp.classList.add('on');io.disconnect()}})},{threshold:.35});io.observe(lp)}}
/* photo rail (Wrapstar reference): native finger drag on a scroll box; continuous rAF autoplay over cloned children.
   Vertical page scroll never pauses it; only a ~350ms hold or a horizontal drag pauses it; resumes 1.5s after release. Reduced motion: no autoplay. */
[].forEach.call(d.querySelectorAll('.rail[data-auto]'),function(rl){if(RM)return;var kids=[].slice.call(rl.children),n=kids.length;if(n<2)return;
 kids.forEach(function(li){var c=li.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(x){x.tabIndex=-1});[].forEach.call(c.querySelectorAll('img'),function(i){i.loading='lazy'});rl.appendChild(c)});
 rl.classList.add('auto');var paused=false,until=0,last=0,SP=32,pos=rl.scrollLeft,hold=null,sx=0,sy=0,dir='';
 function setW(){return rl.children[n].offsetLeft-rl.children[0].offsetLeft}var W=setW();addEventListener('resize',function(){W=setW()});
 function loop(t){var dt=last?Math.min(t-last,64):0;last=t;
  if(!paused&&t>until&&W>0){if(Math.abs(rl.scrollLeft-pos)>2)pos=rl.scrollLeft;pos+=SP*dt/1000;if(pos>=W)pos-=W;rl.scrollLeft=pos}
  else{pos=rl.scrollLeft;if(W>0&&pos>=W){pos-=W;rl.scrollLeft=pos}}
  requestAnimationFrame(loop)}
 requestAnimationFrame(loop);
 function release(){clearTimeout(hold);hold=null;if(paused){paused=false;until=performance.now()+1500}dir=''}
 rl.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;dir='';hold=setTimeout(function(){paused=true},350)},{passive:true});
 rl.addEventListener('touchmove',function(e){if(dir)return;var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);if(dx<6&&dy<6)return;clearTimeout(hold);dir=dx>dy?'h':'v';if(dir==='h')paused=true},{passive:true});
 rl.addEventListener('touchend',release,{passive:true});rl.addEventListener('touchcancel',release,{passive:true});
 rl.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;hold=setTimeout(function(){paused=true},350)});
 rl.addEventListener('pointerup',function(e){if(e.pointerType==='mouse')release()});
 rl.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY)){paused=true;clearTimeout(hold);hold=setTimeout(release,200)}},{passive:true});
});
/* video facade: poster + play icon; the self-hosted mp4 loads only on tap */
[].forEach.call(d.querySelectorAll('button.vf[data-src]'),function(b){b.addEventListener('click',function(){var v=d.createElement('video');v.src=b.getAttribute('data-src');v.muted=true;v.loop=true;v.playsInline=true;v.setAttribute('playsinline','');v.controls=true;v.poster=b.querySelector('img').src;v.setAttribute('aria-label',b.getAttribute('aria-label')||'');var w=d.createElement('div');w.className='vf';w.appendChild(v);b.replaceWith(w);var p=v.play();if(p&&p.catch)p.catch(function(){})})});
})();

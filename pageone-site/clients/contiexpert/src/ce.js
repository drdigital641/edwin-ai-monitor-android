(function(){var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.documentElement.classList.remove('no-js');
/* menu */
var b=d.querySelector('.burger'),n=d.getElementById('nav');if(b&&n)b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false')});
/* reveal on scroll: only elements below the first screen are hidden, and only once the observer exists */
if(!RM&&'IntersectionObserver'in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
[].forEach.call(d.querySelectorAll('[data-rv]'),function(el){if(el.closest('.marq'))return;if(el.getBoundingClientRect().top>innerHeight){el.classList.add('rv');io.observe(el)}})}
/* Marquee carousel, Page One standard (3 Nov 2026): slides on its own, never pauses for page scroll or hover;
   pauses only while held or slid sideways, resumes ~2s after release; manual slide 1:1 with the finger.
   Touch: decide on the first 6px, sideways = slide (preventDefault), vertical = page scroll. Reduced motion: static swipe row + arrows. */
[].forEach.call(d.querySelectorAll('.marq'),function(mq){var tr=mq.querySelector('.track');if(!tr)return;
if(RM){mq.parentNode.classList.add('rm');var pv=mq.parentNode.querySelector('.cprev'),nx=mq.parentNode.querySelector('.cnext');
function step(k){var li=tr.querySelector('li');if(li)tr.scrollBy({left:k*(li.getBoundingClientRect().width+14)})}
if(pv)pv.addEventListener('click',function(){step(-1)});if(nx)nx.addEventListener('click',function(){step(1)});return}
var kids=[].slice.call(tr.children),cnt=kids.length;if(!cnt)return;
var off=0,held=false,drag=false,resumeAt=0,last=0,SP=34,sw=0,sx=0,sy=0,so=0,mode='',moved=false;mq.classList.add('on');
function addSet(){kids.forEach(function(li){var c=li.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(x){x.tabIndex=-1});tr.appendChild(c)})}
addSet();function measure(){var o=tr.children[cnt].offsetLeft-tr.children[0].offsetLeft;if(o>0)sw=o}measure();
while(sw>0&&tr.children.length/cnt*sw<mq.clientWidth+2*sw)addSet();
function wrap(){if(sw>0)off=((off%sw)+sw)%sw}function draw(){tr.style.transform='translate3d('+(-off).toFixed(2)+'px,0,0)'}
function loop(t){var dt=last?Math.min(t-last,100):0;last=t;if(!held&&!drag&&t>=resumeAt){off+=SP*dt/1000;wrap();draw()}requestAnimationFrame(loop)}requestAnimationFrame(loop);
addEventListener('resize',function(){measure();wrap();draw()});
function release(){held=false;if(drag){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}resumeAt=performance.now()+2000}
/* touch */
mq.addEventListener('touchstart',function(e){var t=e.touches[0];held=true;mode='';moved=false;sx=t.clientX;sy=t.clientY;so=off},{passive:true});
mq.addEventListener('touchmove',function(e){if(!held)return;var t=e.touches[0],dx=t.clientX-sx,dy=t.clientY-sy;
if(!mode){if(Math.abs(dx)<6&&Math.abs(dy)<6)return;mode=Math.abs(dx)>=Math.abs(dy)?'x':'y';if(mode==='x'){drag=true;moved=true;mq.classList.add('drag')}else{held=false;resumeAt=0}}
if(mode==='x'){e.preventDefault();off=so-dx;wrap();draw()}},{passive:false});
['touchend','touchcancel'].forEach(function(ev){mq.addEventListener(ev,function(){if(mode!=='y')release();mode=''},{passive:true})});
/* mouse */
var md=false;mq.addEventListener('mousedown',function(e){if(e.button!==0)return;md=true;held=true;moved=false;sx=e.clientX;so=off});
addEventListener('mousemove',function(e){if(!md)return;var dx=e.clientX-sx;if(!drag&&Math.abs(dx)>6){drag=true;moved=true;mq.classList.add('drag')}if(drag){off=so-dx;wrap();draw()}});
addEventListener('mouseup',function(){if(md){md=false;release()}});
mq.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation()}},true);
mq.addEventListener('dragstart',function(e){e.preventDefault()});
});
})();

(function(){var v=document.querySelector('.pipv'),b=document.querySelector('.vsnd');if(!v)return;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){v.removeAttribute('autoplay');v.pause()}
if(b)b.addEventListener('click',function(){if(v.muted){v.muted=false;v.currentTime=0;v.controls=true;v.play();b.style.display='none'}});})();

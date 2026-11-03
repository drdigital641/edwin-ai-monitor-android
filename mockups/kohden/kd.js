(function(){'use strict';
var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
/* mobile menu */
var bg=d.getElementById('burger'),nav=d.getElementById('nav');
if(bg&&nav){bg.addEventListener('click',function(){var o=!nav.classList.contains('open');nav.classList.toggle('open',o);d.body.classList.toggle('menu',o);bg.setAttribute('aria-expanded',o?'true':'false');d.body.style.overflow=o?'hidden':''})}
/* reveal: content stays visible for bots and if the observer never fires */
var rv=[].slice.call(d.querySelectorAll('.rv'));
if('IntersectionObserver' in window&&!RM&&!/bot|crawl|spider|headless/i.test(navigator.userAgent)){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.05});rv.forEach(function(el){io.observe(el)});setTimeout(function(){rv.forEach(function(el){el.classList.add('in')})},4000)}else rv.forEach(function(el){el.classList.add('in')});
/* workshop filter */
var fb=[].slice.call(d.querySelectorAll('.filters button')),dl=[].slice.call(d.querySelectorAll('.dealer[data-region]'));
fb.forEach(function(b){b.addEventListener('click',function(){var f=b.getAttribute('data-f');fb.forEach(function(x){x.classList.toggle('on',x===b)});dl.forEach(function(k){k.hidden=!(f==='All'||k.getAttribute('data-region')===f)})})});
/* Carousel (Wrapstar standard): seamless marquee via rAF translateX. Never pauses on hover, page scroll or visibility;
   stops only while held or slid sideways, resumes 2s after release. Reduced motion: plain swipe row. */
[].forEach.call(d.querySelectorAll('.marq'),function(mq){var tr=mq.querySelector('.track');if(!tr||RM)return;
var kids=[].slice.call(tr.children),n=kids.length;if(!n)return;
var off=0,tt=false,until=0,held=false,drag=false,sx=0,so=0,pid=null,moved=false,last=0,SP=38,sw=0;
mq.classList.add('on');
function addSet(){kids.forEach(function(li){var c=li.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(x){x.tabIndex=-1});tr.appendChild(c)})}
addSet();var one=tr.children[n].offsetLeft-tr.children[0].offsetLeft;sw=one;
while(one>0&&tr.children.length/n*one<mq.clientWidth+2*one){addSet()}
function draw(){tr.style.transform='translate3d('+(-off).toFixed(2)+'px,0,0)'}
function wrap(){if(sw>0){off=((off%sw)+sw)%sw}}
function loop(t){var dt=last?Math.min(t-last,100):0;last=t;if(!held&&!drag&&!tt&&t>until){off+=SP*dt/1000;wrap();draw()}requestAnimationFrame(loop)}
requestAnimationFrame(loop);
window.addEventListener('resize',function(){var o=tr.children[n].offsetLeft-tr.children[0].offsetLeft;if(o>0)sw=o;wrap();draw()});
function release(){held=false;until=performance.now()+2000;if(drag){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}if(pid!==null){try{mq.releasePointerCapture(pid)}catch(x){}pid=null}}
mq.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'||e.button!==0)return;held=true;drag=false;moved=false;sx=e.clientX;so=off;pid=e.pointerId});
mq.addEventListener('pointermove',function(e){if(!held)return;var dx=e.clientX-sx;
if(!drag&&Math.abs(dx)>6){drag=true;moved=true;mq.classList.add('drag');try{mq.setPointerCapture(e.pointerId)}catch(x){}}
if(drag){off=so-dx;wrap();draw()}});
['pointerup','pointercancel','lostpointercapture'].forEach(function(ev){mq.addEventListener(ev,function(){if(held)release()})});
var tx=0,ty=0,tso=0,mode='';
mq.addEventListener('touchstart',function(e){var t=e.touches[0];tx=t.clientX;ty=t.clientY;tso=off;mode='';tt=true;moved=false},{passive:true});
mq.addEventListener('touchmove',function(e){if(!tt)return;var t=e.touches[0],dx=t.clientX-tx,dy=t.clientY-ty;
if(!mode){if(Math.abs(dx)<6&&Math.abs(dy)<6)return;mode=Math.abs(dx)>=Math.abs(dy)?'h':'v';if(mode==='v'){tt=false;return}drag=true;moved=true;mq.classList.add('drag')}
if(mode==='h'){if(e.cancelable)e.preventDefault();off=tso-dx;wrap();draw()}},{passive:false});
['touchend','touchcancel'].forEach(function(ev){mq.addEventListener(ev,function(){if(mode==='h'){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}if(tt)until=performance.now()+2000;tt=false;mode=''},{passive:true})});
mq.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation()}},true);
mq.addEventListener('dragstart',function(e){e.preventDefault()});
});
})();

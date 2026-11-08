/* JBStaycation UI: reveal on scroll, carousels. Content is fully visible without JS. */
(function(){
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var els=[].slice.call(document.querySelectorAll('.rv'));
if('IntersectionObserver' in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});els.forEach(function(x){io.observe(x)})}else{els.forEach(function(x){x.classList.add('in')})}
document.querySelectorAll('[data-carousel]').forEach(function(c){
var t=c.querySelector('.track'),held=false,rt=null,iv=null,drag=null;
function step(d){var w=t.clientWidth,max=t.scrollWidth-w;if(max<=0)return;var n=t.scrollLeft+d*w;if(n>max-4&&d>0)n=0;else if(n<0)n=max;t.scrollTo({left:n,behavior:rm?'auto':'smooth'})}
function hold(){held=true;clearTimeout(rt)}
function release(){clearTimeout(rt);rt=setTimeout(function(){held=false},2000)}
c.querySelector('.next').addEventListener('click',function(){step(1);hold();release()});
c.querySelector('.prev').addEventListener('click',function(){step(-1);hold();release()});
t.addEventListener('touchstart',hold,{passive:true});t.addEventListener('touchend',release,{passive:true});t.addEventListener('touchcancel',release,{passive:true});
t.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'){hold();drag={x:e.clientX,l:t.scrollLeft};t.classList.add('drag');t.style.scrollSnapType='none';try{t.setPointerCapture(e.pointerId)}catch(_){}}});
t.addEventListener('pointermove',function(e){if(drag)t.scrollLeft=drag.l-(e.clientX-drag.x)});
function up(){if(drag){drag=null;t.classList.remove('drag');t.style.scrollSnapType='';var w=t.clientWidth;t.scrollTo({left:Math.round(t.scrollLeft/w)*w,behavior:'smooth'});release()}}
t.addEventListener('pointerup',up);t.addEventListener('pointercancel',up);
t.addEventListener('focusin',hold);t.addEventListener('focusout',release);
if(!rm){iv=setInterval(function(){if(!held&&!document.hidden)step(1)},3800)}
});
})();

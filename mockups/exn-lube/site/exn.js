(function(){var d=document.documentElement;
if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){d.classList.add('js');
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});setTimeout(function(){document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')})},2500)}
var m=document.querySelector('.menu'),n=document.querySelector('.nav');if(m&&n)m.addEventListener('click',function(){var o=n.classList.toggle('open');m.setAttribute('aria-expanded',o)});
/* carousel standard: auto-slides, keeps sliding on scroll, pauses only while held/dragged, restarts ~2s after release */
document.querySelectorAll('.carousel[data-auto]').forEach(function(c){var held=false,t=null;
function step(){if(held)return;var w=c.firstElementChild?c.firstElementChild.getBoundingClientRect().width+12:300;
if(c.scrollLeft+c.clientWidth>=c.scrollWidth-4)c.scrollTo({left:0,behavior:'smooth'});else c.scrollBy({left:w,behavior:'smooth'})}
var iv=setInterval(step,3200);function down(){held=true;clearTimeout(t)}function up(){clearTimeout(t);t=setTimeout(function(){held=false},2000)}
c.addEventListener('pointerdown',down);c.addEventListener('touchstart',down,{passive:true});c.addEventListener('pointerup',up);c.addEventListener('touchend',up);c.addEventListener('pointercancel',up)})})();

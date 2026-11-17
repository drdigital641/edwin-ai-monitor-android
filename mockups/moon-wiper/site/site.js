/* MOON preview call dock. Shows only after the hero call button has scrolled away, and steps aside (slides down)
   whenever product cards, a table or the adapter chart reach the bottom strip it covers, so it never hides them. */
(function(){var d=document.querySelector('.dock'),h=document.getElementById('hero-cta');if(!d)return;
if(!('IntersectionObserver' in window)){d.classList.add('on');return}
var past=!h,under=new Set();function upd(){d.classList.toggle('on',past&&under.size===0)}
if(h)new IntersectionObserver(function(es){es.forEach(function(x){past=!x.isIntersecting&&x.boundingClientRect.top<0});upd()}).observe(h);
var zone=Math.ceil(d.getBoundingClientRect().height)||80;
var io=new IntersectionObserver(function(es){es.forEach(function(x){x.isIntersecting?under.add(x.target):under.delete(x.target)});upd()},{rootMargin:'-'+Math.max(0,window.innerHeight-zone-12)+'px 0px 0px 0px'});
document.querySelectorAll('[data-nodock]').forEach(function(el){io.observe(el)});upd()})();

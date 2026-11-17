/* MOON preview: sticky call dock appears only after the hero call button scrolls out of view */
(function(){var d=document.querySelector('.dock'),h=document.getElementById('hero-cta');if(!d)return;
if(!h||!('IntersectionObserver' in window)){d.classList.add('on');return}
new IntersectionObserver(function(es){es.forEach(function(x){d.classList.toggle('on',!x.isIntersecting&&x.boundingClientRect.top<0)})}).observe(h)})();

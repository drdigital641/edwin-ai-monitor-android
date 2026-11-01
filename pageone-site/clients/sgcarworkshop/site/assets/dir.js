(function(){
var d=document,els=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(el){io.observe(el)})}
else{els.forEach(function(el){el.classList.add('in')})}
var q=d.getElementById('q');
if(q){var cards=d.querySelectorAll('[data-search]'),em=d.getElementById('empty');
function f(){var v=q.value.trim().toLowerCase(),n=0;cards.forEach(function(c){var ok=!v||c.getAttribute('data-search').indexOf(v)>-1;c.hidden=!ok;if(ok)n++});if(em)em.classList.toggle('show',!!v&&!n)}
q.addEventListener('input',f);var fm=q.form;if(fm)fm.addEventListener('submit',function(e){e.preventDefault();f()})}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-cta]');if(!a)return;try{if(window.dataLayer)window.dataLayer.push({event:'cta_click',cta:a.getAttribute('data-cta')})}catch(x){}});
})();

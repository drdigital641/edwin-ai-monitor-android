/* R&C site script: mobile menu, reveal-on-scroll, phone-friendly tables. Text is never changed by script. */
(function(){
  var d=document,root=d.documentElement;
  var btn=d.querySelector('.menu-btn'),nav=d.getElementById('nav');
  if(btn&&nav){btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o?'true':'false')});}
  d.querySelectorAll('.prose table').forEach(function(t){
    var hs=[].map.call(t.querySelectorAll('thead th'),function(h){return h.textContent.trim()});
    if(!hs.length)return;
    t.querySelectorAll('tbody tr').forEach(function(r){[].forEach.call(r.children,function(c,i){if(hs[i])c.setAttribute('data-l',hs[i])})});
  });
  if(!('IntersectionObserver' in window)||navigator.webdriver)return;
  if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var els=d.querySelectorAll('.rv');
  var vh=window.innerHeight||800;
  root.classList.add('js');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el,i){
    if(el.getBoundingClientRect().top<vh){el.classList.add('in')}else{el.style.transitionDelay=((i%4)*70)+'ms';io.observe(el)}
  });
})();

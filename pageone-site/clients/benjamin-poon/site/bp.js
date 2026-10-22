(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('mnav');
  if (btn && nav) btn.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  // Reveal-on-scroll: only items below the first screen are hidden, and only once JS runs (text stays in the HTML).
  var items = [].slice.call(document.querySelectorAll('.card,.awards figure,.steps li,.band,.faq details'));
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var vh = window.innerHeight;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) {
    if (el.getBoundingClientRect().top > vh) { el.classList.add('rv'); io.observe(el); }
  });
})();

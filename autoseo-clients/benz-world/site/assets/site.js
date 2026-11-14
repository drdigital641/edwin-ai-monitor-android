/* Benz World preview: menu, sticky bar, hero slideshow, scroll reveal.
   No layout depends on JS; all text is in the HTML. Under prefers-reduced-motion
   the hero stays on its first (static) photo, later slides are never fetched,
   and reveals are skipped. */
(function(){var d=document,w=window;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
var reduce=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;
ready(function(){
  var menu=d.querySelector('details.menu');
  if(menu){d.addEventListener('click',function(e){if(menu.open&&!menu.contains(e.target))menu.open=false});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu.open){menu.open=false;menu.querySelector('summary').focus()}})}

  /* Glass header: shadow once scrolled (passive listener). */
  var head=d.querySelector('.site-head');
  if(head){var st=false,tk=false;
    var upd=function(){tk=false;var on=(w.pageYOffset||d.documentElement.scrollTop)>40;if(on!==st){st=on;head.classList.toggle('is-scrolled',on)}};
    w.addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd()}

  /* Sticky WhatsApp + Call bar: hidden until the hero CTA row has scrolled out of view. */
  var bar=d.querySelector('.mbar');
  var cta=d.querySelector('.hero .btn-row, .phero .btn-row');
  if(bar&&cta){
    if(!('IntersectionObserver' in w)){bar.classList.add('is-visible')}
    else{
      var io=new IntersectionObserver(function(es){
        es.forEach(function(e){bar.classList.toggle('is-visible', !e.isIntersecting)});
      },{threshold:0,rootMargin:'0px 0px -8px 0px'});
      io.observe(cta);
    }
  }else if(bar){bar.classList.add('is-visible')}

  /* Scroll reveal (subtle). Content is visible without JS and with reduced motion. */
  var rv=[].slice.call(d.querySelectorAll('[data-rv]'));
  if(reduce||!('IntersectionObserver' in w)){rv.forEach(function(e){e.classList.add('in')})}
  else if(rv.length){
    var ro=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}});
    },{threshold:0.12,rootMargin:'0px 0px -6% 0px'});
    rv.forEach(function(e){ro.observe(e)});
  }

  /* Hero: slow Ken Burns crossfade. */
  var hero=d.querySelector('.hero-cine');
  if(!hero||reduce)return;
  var slides=[].slice.call(hero.querySelectorAll('.slide'));
  if(slides.length<2)return;
  var bars=[].slice.call(hero.querySelectorAll('.slide-bars i'));
  var no=hero.querySelector('.sc-no'),txt=hero.querySelector('.sc-t');
  var DUR=7000,FADE=1900,cur=0,timer=null,visible=true;
  hero.style.setProperty('--dur',DUR+'ms');

  function load(s){
    return new Promise(function(res){
      if(s.getAttribute('data-ready'))return res();
      [].forEach.call(s.querySelectorAll('[data-srcset]'),function(e){e.srcset=e.getAttribute('data-srcset');e.removeAttribute('data-srcset')});
      var im=s.querySelector('img');
      if(im.getAttribute('data-src')){im.src=im.getAttribute('data-src');im.removeAttribute('data-src')}
      function ok(){s.setAttribute('data-ready','1');res()}
      if(im.complete&&im.naturalWidth)ok();else{im.addEventListener('load',ok,{once:true});im.addEventListener('error',function(){res()},{once:true})}
    });
  }
  function setBars(i){
    bars.forEach(function(b,k){b.classList.remove('on');b.classList.toggle('done',k<i)});
    if(bars[i]){void bars[i].offsetWidth;bars[i].classList.add('on')}
  }
  function show(i){
    var prev=slides[cur],next=slides[i];
    prev.classList.remove('is-on');prev.classList.add('is-out');
    next.classList.add('is-on');
    setTimeout(function(){prev.classList.remove('is-out')},FADE);
    cur=i;
    if(no)no.textContent=(i<9?'0':'')+(i+1);
    if(txt)txt.textContent=next.getAttribute('data-cap')||'';
    setBars(i);
    load(slides[(i+1)%slides.length]);
  }
  function tick(){
    var i=(cur+1)%slides.length;
    load(slides[i]).then(function(){if(slides[i].getAttribute('data-ready'))show(i);schedule()});
  }
  function schedule(){clearTimeout(timer);if(visible&&!d.hidden)timer=setTimeout(tick,DUR)}
  function start(){
    hero.classList.add('cine-on');setBars(0);
    load(slides[1]);schedule();
    if('IntersectionObserver' in w){
      new IntersectionObserver(function(es){visible=es[0].isIntersecting;
        if(visible){setBars(cur);schedule()}else clearTimeout(timer)}).observe(hero);
    }
    d.addEventListener('visibilitychange',function(){if(d.hidden)clearTimeout(timer);else{setBars(cur);schedule()}});
  }
  if(d.readyState==='complete')start();else w.addEventListener('load',start,{once:true});
});})();

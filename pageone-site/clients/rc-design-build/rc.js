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
  /* archive strip: auto-slides; touch/click pauses, customer can swipe or drag; resumes 1s after release */
  var mq=d.querySelector('.marq');
  if(mq){
    root.classList.add('marq-js');
    var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var speed=0.45,held=false,resumeAt=0,last=0,pos=mq.scrollLeft,drag=null,moved=false;
    function half(){return mq.scrollWidth/2}
    function hold(){held=true}
    function release(){held=false;resumeAt=performance.now()+1000;pos=mq.scrollLeft}
    function step(t){
      var dt=last?Math.min(t-last,50):16;last=t;
      if(!held&&!reduce&&t>=resumeAt&&!d.hidden){
        pos+=speed*dt/16;
        if(pos>=half())pos-=half();
        mq.scrollLeft=pos;
      }else if(held){pos=mq.scrollLeft}
      if(!drag){if(mq.scrollLeft>=half()){mq.scrollLeft-=half();pos=mq.scrollLeft}else if(!held&&mq.scrollLeft<1){mq.scrollLeft+=half();pos=mq.scrollLeft}}
      requestAnimationFrame(step);
    }
    mq.addEventListener('touchstart',hold,{passive:true});
    mq.addEventListener('touchend',release,{passive:true});
    mq.addEventListener('touchcancel',release,{passive:true});
    mq.addEventListener('mouseenter',hold);
    mq.addEventListener('mouseleave',function(){if(drag){drag=null;mq.classList.remove('dragging')}release()});
    mq.addEventListener('wheel',function(){hold();clearTimeout(mq._w);mq._w=setTimeout(release,200)},{passive:true});
    var lastTouch=0;mq.addEventListener('touchstart',function(){lastTouch=Date.now()},{passive:true});
    mq.addEventListener('mousedown',function(e){if(e.button!==0||Date.now()-lastTouch<800)return;drag={x:e.clientX,s:mq.scrollLeft};moved=false;e.preventDefault()});
    window.addEventListener('mousemove',function(e){if(!drag)return;var dx=e.clientX-drag.x;if(Math.abs(dx)>5&&!moved){moved=true;mq.classList.add('dragging')}var v=drag.s-dx,h=half();if(v<0){v+=h;drag.s+=h}else if(v>=h){v-=h;drag.s-=h}mq.scrollLeft=v});
    window.addEventListener('mouseup',function(){if(!drag)return;drag=null;mq.classList.remove('dragging');pos=mq.scrollLeft});
    mq.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
    mq.addEventListener('focusin',hold);mq.addEventListener('focusout',release);
    requestAnimationFrame(step);
    /* tap an archive picture: show it in the hero */
    var hero=d.querySelector('.lux'),himg=hero&&hero.querySelector('.lux-bg img'),hday=hero&&hero.querySelector('.lux-day'),back=hero&&hero.querySelector('.lux-back');
    if(himg&&hday){
      var today={src:himg.currentSrc||himg.src,alt:himg.alt,label:hday.querySelector('.lux-date').innerHTML,title:hday.querySelector('.lux-title').textContent,href:hday.getAttribute('href')};
      var show=function(o,isToday){
        var pre=new Image();pre.onload=pre.onerror=function(){
          himg.style.opacity='0';
          setTimeout(function(){himg.removeAttribute('srcset');himg.src=o.src;himg.alt=o.alt;hday.querySelector('.lux-date').innerHTML=o.label;
            hday.querySelector('.lux-title').textContent=o.title;hday.setAttribute('href',o.href);himg.style.opacity='1';if(back)back.hidden=!!isToday},250);
        };pre.src=o.src;
        window.scrollTo({top:0,behavior:'smooth'});
      };
      mq.addEventListener('click',function(e){
        var a=e.target.closest&&e.target.closest('.mq');if(!a||e.defaultPrevented)return;e.preventDefault();
        show({src:a.getAttribute('data-full'),alt:a.getAttribute('data-alt'),label:a.getAttribute('data-label'),title:a.getAttribute('data-title'),href:a.getAttribute('href')});
      });
      if(back)back.addEventListener('click',function(){show(today,true)});
    }
  }
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

/* Carku Singapore: menu, sticky WhatsApp bar, model rail, image fallback, CTA tracking */
(function(){
  var d=document,w=window;
  function ready(f){d.readyState!=="loading"?f():d.addEventListener("DOMContentLoaded",f)}
  var reduce=w.matchMedia&&w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  ready(function(){
    /* image fallback: hide a broken image so the frame shows the model code */
    [].forEach.call(d.querySelectorAll(".frame img"),function(im){
      var off=function(){im.style.visibility="hidden"};
      if(im.complete&&im.naturalWidth===0&&im.currentSrc)off();
      im.addEventListener("error",off);
    });

    /* menu */
    var menu=d.querySelector("[data-menu]");
    if(menu){
      menu.addEventListener("click",function(e){if(e.target.closest("a"))menu.open=false});
      d.addEventListener("keydown",function(e){if(e.key==="Escape"&&menu.open){menu.open=false;menu.querySelector("summary").focus()}});
      d.addEventListener("click",function(e){if(menu.open&&!menu.contains(e.target))menu.open=false});
    }

    /* sticky bar: appears once the page's own WhatsApp button has scrolled away */
    var bar=d.querySelector("[data-sticky]"),anchor=d.querySelector("[data-sticky-anchor]");
    function setBar(on){if(!bar)return;bar.classList.toggle("on",on);bar.setAttribute("aria-hidden",on?"false":"true");
      [].forEach.call(bar.querySelectorAll("a"),function(a){on?a.removeAttribute("tabindex"):a.setAttribute("tabindex","-1")})}
    setBar(false);
    if(bar&&anchor&&"IntersectionObserver" in w){
      new IntersectionObserver(function(es){var e=es[0];setBar(!e.isIntersecting&&e.boundingClientRect.top<0)}).observe(anchor);
    }else if(bar){w.addEventListener("scroll",function(){setBar(w.scrollY>w.innerHeight*.7)},{passive:true})}

    /* model rail: auto-advances, pauses on hover, touch and focus, dots + arrows, native swipe, still under reduced motion */
    [].forEach.call(d.querySelectorAll("[data-rail]"),function(box){
      var rail=box.querySelector(".rail"),items=rail.children,dots=box.querySelector(".dots"),prev=box.querySelector("[data-prev]"),next=box.querySelector("[data-next]");
      var paused=false,timer=null,resume=null,n=items.length;
      function step(){return items.length>1?items[1].offsetLeft-items[0].offsetLeft:rail.clientWidth}
      function idx(){return Math.round(rail.scrollLeft/step())}
      function maxIdx(){return Math.max(0,Math.round((rail.scrollWidth-rail.clientWidth)/step()))}
      function go(i){var m=maxIdx();if(i>m)i=0;if(i<0)i=m;rail.scrollTo({left:i*step(),behavior:reduce?"auto":"smooth"})}
      var btns=[];
      for(var i=0;i<n;i++){(function(i){var b=d.createElement("button");b.type="button";b.setAttribute("aria-label","Show model "+(i+1)+" of "+n);
        b.addEventListener("click",function(){go(i);hold(6000)});dots.appendChild(b);btns.push(b)})(i)}
      function mark(){var k=Math.min(idx(),n-1);btns.forEach(function(b,j){b.setAttribute("aria-current",j===k?"true":"false")})}
      rail.addEventListener("scroll",function(){w.requestAnimationFrame(mark)},{passive:true});mark();
      prev.addEventListener("click",function(){go(idx()-1);hold(6000)});
      next.addEventListener("click",function(){go(idx()+1);hold(6000)});
      function hold(ms){paused=true;clearTimeout(resume);resume=setTimeout(function(){paused=false},ms)}
      box.addEventListener("mouseenter",function(){paused=true;clearTimeout(resume)});
      box.addEventListener("mouseleave",function(){hold(1500)});
      rail.addEventListener("touchstart",function(){paused=true;clearTimeout(resume)},{passive:true});
      rail.addEventListener("touchend",function(){hold(2500)},{passive:true});
      box.addEventListener("focusin",function(){paused=true;clearTimeout(resume)});
      box.addEventListener("focusout",function(){hold(2000)});
      if(!reduce){timer=setInterval(function(){if(!paused&&!d.hidden)go(idx()+1)},3800)}
    });

    /* CTA tracking hook */
    d.addEventListener("click",function(e){
      var a=e.target.closest("[data-cta]");if(!a)return;
      (w.dataLayer=w.dataLayer||[]).push({event:"cta_click",cta:a.getAttribute("data-cta"),
        channel:/wa\.me/.test(a.href)?"whatsapp":/^tel:/.test(a.href)?"call":"link",page:location.pathname});
    });
  });
})();

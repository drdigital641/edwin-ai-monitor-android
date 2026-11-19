/* AutoSEO shared blocks JS (look v2, 20 Nov 2026). No libraries. Include once, deferred.
   header glass after scroll, floating WhatsApp bar hidden while the hero buttons show, Facebook facade swap on tap
   (no Facebook script before a tap), self-hosted hero video (muted autoplay unless reduced motion, "Tap for sound"). */
(function(){var d=document;d.documentElement.classList.add('js');
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
var top=d.querySelector('.top');
if(top){var sol=function(){top.classList.toggle('solid',(window.scrollY||0)>24)};sol();addEventListener('scroll',sol,{passive:true})}
var hc=d.querySelector('.hero-cta'),mbar=d.querySelector('.mbar');
if(hc&&mbar&&'IntersectionObserver' in window){new IntersectionObserver(function(es){mbar.classList.toggle('off',es[0].isIntersecting)},{threshold:0}).observe(hc)}
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.vf-b');if(!b)return;
  var f=d.createElement('iframe');f.setAttribute('loading','eager');f.src=b.getAttribute('data-src');f.title=b.getAttribute('aria-label');
  f.setAttribute('allow','autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share');f.setAttribute('allowfullscreen','');
  b.parentNode.replaceChild(f,b)});
[].forEach.call(d.querySelectorAll('.vf-own'),function(w){var v=w.querySelector('video'),s=w.querySelector('.vf-snd');
  if(!reduce){v.preload='auto';var p=v.play();p&&p.catch&&p.catch(function(){})}
  s&&s.addEventListener('click',function(){v.muted=!v.muted;if(!v.muted&&v.paused)v.play();s.setAttribute('aria-pressed',v.muted?'false':'true')})});
})})();

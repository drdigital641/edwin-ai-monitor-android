/* Star Performance home reels: lazy muted autoplay loop, tap for sound, tabs on phone. */
(function(){var d=document,root=d.getElementById('watch');if(!root)return;
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var save=navigator.connection&&navigator.connection.saveData;
var items=[].slice.call(root.querySelectorAll('.rl-item')),tabs=[].slice.call(root.querySelectorAll('.rl-tab'));
var mq=matchMedia('(min-width:900px)'),sound=false,visible=false;
function vid(i){return i.querySelector('video')}
function load(i){var v=vid(i);if(!v.getAttribute('src')){v.src=v.getAttribute('data-src');v.load()}return v}
function mute(i,m){var v=vid(i);v.muted=m;i.classList.toggle('snd',!m)}
function play(i){var v=load(i);var p=v.play();if(p&&p.catch)p.catch(function(){})}
function isActive(i){return mq.matches||i.classList.contains('on')}
function sync(){items.forEach(function(i){var v=vid(i);
  if(visible&&isActive(i)&&!rm&&!save){play(i)}else{if(v.getAttribute('src'))v.pause()}})}
items.forEach(function(i){var v=vid(i);
  v.addEventListener('playing',function(){i.classList.add('playing')});
  v.addEventListener('pause',function(){i.classList.remove('playing')});
  i.querySelector('.rl-tap').addEventListener('click',function(){
    var v2=load(i);
    if(v2.muted||v2.paused){ /* first tap: restart with sound, silence the other reel */
      items.forEach(function(o){if(o!==i)mute(o,true)});
      v2.currentTime=0;mute(i,false);sound=true;play(i)
    }else{mute(i,true);sound=false}
  });
});
function pick(n){items.forEach(function(i,k){var on=k===n;i.classList.toggle('on',on);if(!on){mute(i,true);vid(i).pause()}else if(sound)mute(i,false)});
  tabs.forEach(function(t,k){t.setAttribute('aria-pressed',k===n)});sync()}
tabs.forEach(function(t,k){t.addEventListener('click',function(){pick(k)})});
/* swipe the reel sideways to switch language (phone) */
var sx=0,sy=0;root.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;sy=e.touches[0].clientY},{passive:true});
root.addEventListener('touchend',function(e){if(mq.matches)return;var dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
  if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5){var cur=items.findIndex(function(i){return i.classList.contains('on')});pick(Math.max(0,Math.min(items.length-1,cur+(dx<0?1:-1))))}},{passive:true});
/* chip on hero: jump to the reels and start the chosen one */
[].forEach.call(d.querySelectorAll('[data-reel]'),function(a){a.addEventListener('click',function(){var n=+a.getAttribute('data-reel');if(!mq.matches)pick(n)})});
if('IntersectionObserver' in window){new IntersectionObserver(function(es){visible=es[es.length-1].isIntersecting;sync()},{rootMargin:'120px 0px',threshold:.25}).observe(root)}
else{visible=true;sync()}
mq.addEventListener&&mq.addEventListener('change',sync);
d.addEventListener('visibilitychange',function(){if(d.hidden)items.forEach(function(i){vid(i).pause()});else sync()});
})();

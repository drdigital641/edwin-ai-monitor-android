/* AutoSEO shared SHOP script (first site: BIY Home Store, 25 Nov 2026). No framework; every page is fully rendered HTML
   and works with JS off. This adds: rails (Wrapstar carousel rules), branch picker for WhatsApp prefills, the static
   search page, header search reveal on the home page, menu sheet, dataLayer events (view_item, search, select_category)
   and an optional GA4 switch (data-ga4 on <body>, blank = off). */
(function(){
var d=document,w=window,RM=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;
w.dataLayer=w.dataLayer||[];function dl(o){try{w.dataLayer.push(o)}catch(e){}}
w.shopDL=dl; /* shared helper: cart.js pushes add_to_cart / remove_from_cart / view_cart / begin_checkout through it */
function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))}
/* ---------- GA4 switch ---------- */
var ga=d.body.getAttribute('data-ga4');if(ga){var s=d.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(ga);d.head.appendChild(s);w.gtag=function(){w.dataLayer.push(arguments)};w.gtag('js',new Date());w.gtag('config',ga)}
/* ---------- menu sheet ---------- */
var sh=d.getElementById('sheet'),mo=d.getElementById('mopen'),mc=d.getElementById('mclose');
function sheet(o){if(!sh)return;sh.classList.toggle('open',o);sh.setAttribute('aria-hidden',o?'false':'true');if(mo)mo.setAttribute('aria-expanded',o?'true':'false');d.documentElement.classList.toggle('noscroll',o)}
if(mo)mo.addEventListener('click',function(){sheet(true)});if(mc)mc.addEventListener('click',function(){sheet(false)});
if(sh)sh.addEventListener('click',function(e){if(e.target===sh)sheet(false)});
d.addEventListener('keydown',function(e){if(e.key==='Escape')sheet(false)});
/* ---------- header search reveal (home: the hero holds the big search) ---------- */
var hd=d.querySelector('.hd'),hs=d.getElementById('hero-search');
if(hd&&hs&&'IntersectionObserver'in w){new IntersectionObserver(function(en){hd.classList.toggle('hd-show',!en[0].isIntersecting)},{rootMargin:'-60px 0px 0px 0px'}).observe(hs)}
/* ---------- rails: Wrapstar behaviour ---------- */
$$('[data-rail]').forEach(function(el){
  var tr=el.firstElementChild;if(!tr)return;
  if(el.scrollWidth<=el.clientWidth+4||RM)return; /* only autoplay a rail that overflows; never under reduced motion */
  var kids=Array.prototype.slice.call(tr.children),half;
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');var f=$$('a,button',c);if(c.matches('a,button'))f.push(c);f.forEach(function(a){a.setAttribute('tabindex','-1')});tr.appendChild(c)});
  half=tr.scrollWidth/2;el.classList.add('rail-auto');
  var pos=el.scrollLeft,run=true,last=0,sp=0.035,hold=null,rt=null,x0=0,y0=0;
  function tick(t){if(run){var dt=last?Math.min(t-last,50):16;pos+=sp*dt;if(pos>=half)pos-=half;el.scrollLeft=pos}last=t;requestAnimationFrame(tick)}
  function pause(){run=false;clearTimeout(rt)}
  function resume(ms){clearTimeout(rt);rt=setTimeout(function(){pos=el.scrollLeft;if(pos>=half)pos-=half;run=true},ms)}
  el.addEventListener('touchstart',function(e){var p=e.touches[0];x0=p.clientX;y0=p.clientY;clearTimeout(hold);hold=setTimeout(pause,350)},{passive:true});
  el.addEventListener('touchmove',function(e){var p=e.touches[0],dx=Math.abs(p.clientX-x0),dy=Math.abs(p.clientY-y0);if(dy>8&&dy>dx){clearTimeout(hold);return}if(dx>8&&dx>dy){clearTimeout(hold);pause()}},{passive:true});
  el.addEventListener('touchend',function(){clearTimeout(hold);if(!run)resume(1500)},{passive:true});
  el.addEventListener('touchcancel',function(){clearTimeout(hold);if(!run)resume(1500)},{passive:true});
  if(w.matchMedia&&w.matchMedia('(hover: hover) and (pointer: fine)').matches){el.addEventListener('mouseenter',pause);el.addEventListener('mouseleave',function(){resume(400)})}
  el.addEventListener('scroll',function(){if(!run){pos=el.scrollLeft}},{passive:true});
  requestAnimationFrame(tick);
});
/* ---------- branch picker: rewrites every WhatsApp prefill that has {branch} ---------- */
var bj=d.getElementById('branches-data'),BR=null;try{BR=bj?JSON.parse(bj.textContent):null}catch(e){}
function waHref(a,name){var t=a.getAttribute('data-wa-tpl'),n=a.getAttribute('data-wa-num');if(!t||!n)return;a.href='https://wa.me/'+n+'?text='+encodeURIComponent(t.split('{branch}').join(name))}
function pick(slug,save){if(!BR||!BR[slug])return;$$('a[data-wa-tpl]').forEach(function(a){waHref(a,BR[slug])});$$('[data-branch-pick]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-branch-pick')===slug?'true':'false')});$$('[data-branch-name]').forEach(function(s){s.textContent=BR[slug]});if(save){try{localStorage.setItem('biy_branch',slug)}catch(e){}}}
if(BR){var fixed=d.body.getAttribute('data-branch'),saved=null;try{saved=localStorage.getItem('biy_branch')}catch(e){}
  if(fixed)pick(fixed,false);else if(saved)pick(saved,false);
  $$('[data-branch-pick]').forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-branch-pick'),true)})})}
/* ---------- dataLayer events ---------- */
var vi=d.getElementById('view-item');if(vi){try{dl({event:'view_item',ecommerce:{items:[JSON.parse(vi.textContent)]}})}catch(e){}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-select-category]');if(a)dl({event:'select_category',category:a.getAttribute('data-select-category')})},true);
$$('[data-search-form]').forEach(function(f){f.addEventListener('submit',function(){var q=f.querySelector('input[name=q]');if(q&&q.value.trim())dl({event:'search_submit',search_term:q.value.trim().slice(0,80)})})});
/* ---------- search page ---------- */
var app=d.getElementById('search-app');if(!app)return;
var q='';try{q=(new URLSearchParams(location.search).get('q')||'').trim().slice(0,80)}catch(e){}
$$('input[name=q]').forEach(function(i){if(q)i.value=q});if(!q)return;
var lang=app.getAttribute('data-lang'),pre=app.getAttribute('data-prefix'),out=d.getElementById('search-results'),lab={};try{lab=JSON.parse(app.getAttribute('data-labels')||'{}')}catch(e){}
function esc(s){return String(s).replace(/[<>&"']/g,function(c){return{'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]})}
function norm(s){return String(s||'').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g,'').replace(/[^\p{L}\p{N}]+/gu,' ').trim()}
fetch(app.getAttribute('data-index'),{credentials:'omit'}).then(function(r){return r.json()}).then(function(ix){
  var toks=norm(q).split(' ').filter(Boolean),res=[];
  ix.items.forEach(function(it){var hay=norm([it.n[lang],it.n.en,it.b,it.k].join(' ')),cjk=hay.replace(/ /g,'');
    var sc=0;for(var i=0;i<toks.length;i++){var t=toks[i];if(hay.indexOf(t)>-1||cjk.indexOf(t)>-1)sc++;else return}
    if(norm(it.n[lang]||it.n.en).indexOf(norm(q))===0)sc+=2;res.push([sc+(it.t==='product'?0.5:0),it])});
  res.sort(function(a,b){return b[0]-a[0]});
  var h='<h2>'+esc((lab.results||'{q}').replace('{q}',q))+'</h2>';
  if(res.length){h+='<ul class="sr-list">'+res.slice(0,40).map(function(r){var it=r[1];return'<li><a href="'+pre+it.p+'"><span class="sr-t">'+esc(lab[it.t]||it.t)+'</span><b>'+esc(it.n[lang]||it.n.en)+'</b>'+(it.b?'<small>'+esc(it.b)+'</small>':'')+'</a></li>'}).join('')+'</ul>'}
  out.innerHTML=h;out.hidden=false;var nf=d.getElementById('search-none');if(nf)nf.hidden=!!res.length;
  dl({event:'search',search_term:q,results:res.length});
}).catch(function(){});
})();

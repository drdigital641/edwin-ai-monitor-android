/* SG Car Workshop quick wins (22 Nov 2026).
   1) Opening status on cards ("Open now, closes 6pm"), from the Google Maps hours on each workshop page (assets/hours.json), computed in Singapore time. No hours = no status.
   2) "Open now" filter on listing pages.
   3) Sticky WhatsApp / Call bar on listing pages (and home search results) for the workshop card in view. It copies that card's own links, so taps are tracked as usual. */
(function(){
'use strict';
var d=document,main=d.getElementById('main');if(!main)return;
var me=d.currentScript||d.querySelector('script[src*="assets/qw.js"]'),base=me?me.src.replace(/assets\/qw\.js.*$/,''):'/';
var path=location.pathname.replace(/^\/preview\/sgcarworkshop/,'')||'/';
var isHome=path==='/'||path==='/index.html',isList=/^\/(services|areas)\/[^\/]+/.test(path)&&!/^\/areas\/?$/.test(path);
var HRS=null,DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function units(scope){return [].slice.call((scope||main).querySelectorAll('article.card,li.gw')).filter(function(u){return u.querySelector('a[href*="wa.me"]')})}
function slugOf(u){var a=u.querySelectorAll('a[href*="workshops/"]');for(var i=0;i<a.length;i++){var m=/workshops\/([a-z0-9-]+)\/?(?:[#?].*)?$/.exec(a[i].getAttribute('href'));if(m)return m[1]}return ''}
function sgNow(){var t=new Date(Date.now()+288e5);return t.getUTCDay()*1440+t.getUTCHours()*60+t.getUTCMinutes()}
function fmt(m){m=((m%1440)+1440)%1440;var h=Math.floor(m/60),mi=m%60;if(!h&&!mi)return 'midnight';if(h===12&&!mi)return 'noon';var ap=h<12?'am':'pm',hh=h%12||12;return hh+(mi?':'+(mi<10?'0':'')+mi:'')+ap}
function status(rows){var W=10080,iv=[],tot=0;rows.forEach(function(r){var s=r[0]*1440+r[1],e=r[0]*1440+r[2];if(r[2]<=r[1])e+=1440;iv.push([s,e]);tot+=e-s});
 if(!iv.length)return null;if(tot>=W-10)return{c:'open',t:'Open 24 hours'};
 iv.sort(function(a,b){return a[0]-b[0]});var now=sgNow();
 for(var i=0;i<iv.length;i++){var s=iv[i][0],e=iv[i][1],n=now<s&&now+W<e?now+W:now;
  if(n>=s&&n<e){var end=e,k=0,g=true;while(g&&k<8){g=false;k++;for(var j=0;j<iv.length;j++){if(iv[j][0]%W===end%W&&iv[j][1]>iv[j][0]&&j!==i){end+=iv[j][1]-iv[j][0];g=true;break}}}
   var left=end-n;if(left>=1440)return{c:'open',t:'Open now, 24 hours'};return{c:left<=60?'soon':'open',t:(left<=60?'Closing soon, ':'Open now, ')+'closes '+fmt(end)}}}
 var best=null;iv.forEach(function(x){var s=x[0]>now?x[0]:x[0]+W;if(best===null||s<best)best=s});
 var dd=Math.floor(best/1440)-Math.floor(now/1440),when=dd===0?'':dd===1?' tomorrow':' '+DN[Math.floor(best/1440)%7];
 return{c:'closed',t:'Closed, opens '+fmt(best)+when}}
function stOf(u){if(!HRS)return null;var s=u.__slug;if(s===undefined)s=u.__slug=slugOf(u);var r=s&&HRS[s];return r?status(r):null}
function paint(u){var st=stOf(u),p=u.querySelector('.qw-st');if(!st){if(p)p.parentNode.removeChild(p);u.removeAttribute('data-open');return}
 if(!p){p=d.createElement('p');p.className='qw-st';p.appendChild(d.createElement('i'));p.appendChild(d.createElement('span'));
  var anchor=u.querySelector('.meta.rg')||u.querySelector('h3')||u.querySelector('div');if(anchor&&anchor.parentNode)anchor.parentNode.insertBefore(p,anchor.nextSibling);else u.insertBefore(p,u.firstChild)}
 p.className='qw-st '+st.c;p.lastChild.textContent=st.t;p.setAttribute('title','Opening hours from Google Maps, Singapore time');u.setAttribute('data-open',st.c==='closed'?'0':'1')}
function paintAll(){units(d).forEach(paint);filt();barUpd()}
/* Open now filter */
var ob=null,note=null,fon=false;
function filt(){if(!ob)return;var us=units(main),n=0,tot=0;us.forEach(function(u){var ok=u.getAttribute('data-open')==='1';tot++;if(ok)n++;u.classList.toggle('qw-hide',fon&&!ok)});
 if(note){note.hidden=!fon;note.textContent=n?('Showing '+n+' open now. Hours from Google Maps; workshops without hours are hidden.'):'None open right now by Google Maps hours. Tap Open now again to see all.'}}
function tools(){if(!isList||ob)return;var any=units(main).some(function(u){return u.hasAttribute('data-open')});if(!any)return;
 var w=d.createElement('div');w.className='w qw-tools';ob=d.createElement('button');ob.type='button';ob.className='qw-ob';ob.setAttribute('aria-pressed','false');ob.setAttribute('data-cta','filter_open_now');
 ob.appendChild(d.createElement('i'));ob.appendChild(d.createTextNode('Open now'));note=d.createElement('p');note.className='qw-on';note.hidden=true;note.setAttribute('aria-live','polite');w.appendChild(ob);w.appendChild(note);
 var hero=main.querySelector('section.hero'),h1=main.querySelector('h1');
 if(hero&&hero.parentNode)hero.parentNode.insertBefore(w,hero.nextSibling);else if(h1&&h1.parentNode){w.className='qw-tools';h1.parentNode.insertBefore(w,h1.nextSibling)}else return;
 ob.addEventListener('click',function(){fon=!fon;ob.setAttribute('aria-pressed',fon?'true':'false');filt();barUpd()})}
/* Sticky bar */
var bar=null,cur=null,raf=0;
function scope(){if(isList)return main;if(isHome){var r=d.getElementById('askres');return r&&!r.hidden?r:null}return null}
function visible(u){return u.offsetParent!==null&&!u.hidden}
function pickU(){var sc=scope();if(!sc)return null;var us=units(sc).filter(visible);if(!us.length)return null;
 for(var i=0;i<us.length;i++){var r=us[i].getBoundingClientRect();if(r.bottom>90)return us[i]}return us[us.length-1]}
function cp(src,dst){['href','data-cta','data-tier','data-page','target','rel'].forEach(function(k){var v=src.getAttribute(k);if(v!==null)dst.setAttribute(k,v);else dst.removeAttribute(k)});dst.setAttribute('data-ref','sticky_bar')}
function mk(){bar=d.createElement('div');bar.className='qw-bar';bar.setAttribute('role','region');bar.setAttribute('aria-label','Contact this workshop');bar.hidden=true;
 bar.innerHTML='<span class="qw-bn"><b></b><small></small></span><a class="btn wa" data-cta=""><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg> WhatsApp</a><a class="btn" data-cta=""><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-phone"/></svg> Call</a>';
 if(!d.getElementById('i-wa')){var u=bar.querySelector('.wa use');if(u)u.parentNode.parentNode.removeChild(u.parentNode)}
 d.body.appendChild(bar)}
function barUpd(){if(!isList&&!isHome)return;if(!bar)mk();var u=pickU();if(!u){bar.hidden=true;d.body.classList.remove('qw-hasbar');return}
 var wa=u.querySelector('a[href*="wa.me"]'),tel=u.querySelector('a[href^="tel:"]'),bw=bar.querySelector('.btn.wa'),bc=bar.querySelector('.btn:not(.wa)');
 if(u!==cur||bw.getAttribute('href')!==wa.getAttribute('href')){cur=u;cp(wa,bw);if(tel){cp(tel,bc);bc.hidden=false}else bc.hidden=true;
  var nm=u.querySelector('h3')||u.querySelector('b');bar.querySelector('.qw-bn b').textContent=nm?nm.textContent.trim():'This workshop'}
 var st=u.querySelector('.qw-st'),sm=bar.querySelector('.qw-bn small'),tier=u.querySelector('.tier');
 sm.className=st?st.className.replace('qw-st','').trim():'';sm.textContent=st?st.textContent:(tier?tier.textContent.trim():'');
 bar.hidden=false;d.body.classList.add('qw-hasbar')}
function onScroll(){if(raf)return;raf=requestAnimationFrame(function(){raf=0;barUpd()})}
if(isList||isHome){window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll)}
/* Search results and late-loaded cards: paint new cards as they appear */
if(window.MutationObserver){var mt=0;new MutationObserver(function(){clearTimeout(mt);mt=setTimeout(function(){units(d).forEach(function(u){if(!u.__p){u.__p=1;paint(u)}});filt();barUpd()},60)}).observe(main,{childList:true,subtree:true,attributes:true,attributeFilter:['hidden']})}
if(isList)barUpd();
var need=units(d).length||isHome;
if(need&&window.fetch){fetch(base+'assets/hours.json?v=20261122',{credentials:'omit'}).then(function(r){if(!r.ok)throw r.status;return r.json()}).then(function(j){HRS=(j&&j.h)||{};units(d).forEach(function(u){u.__p=1});paintAll();tools();filt();setInterval(paintAll,60000)}).catch(function(){})}
})();

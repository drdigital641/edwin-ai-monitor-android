/* AutoSEO shared SHOP enquiry basket (first site: BIY Home Store v3, 26 Nov 2026). No prices, no payment, no login.
   Browser memory only: localStorage <pfx>_cart_v1 = {v:1, items:[{sku,group,name,brand,model,variant,unit,qty,sample,added_at}],
   updated_at}; <pfx>_branch_v1 (pickup branch id), <pfx>_name_v1 (optional name). No cookies, no server calls: the cart
   leaves the browser only when the visitor taps "Send enquiry on WhatsApp" (wa.me link with the list as text).
   Config = ONE inline JSON block per page (#shop-cfg: mode, price_mode, ids, branches, strings), no extra request.
   Storage blocked (private mode): the cart lives in memory for this page and a note says it will not be remembered.
   Markup it reads (rendered by the build, works as plain links with JS off):
     [data-cart-open]  header cart link (href = cart page) + [data-cart-count] badge
     [data-cart-item]  card / product block holding  button[data-add data-sku data-group data-name data-brand data-model
                       data-variant data-unit data-sample]  + optional select[data-variant-select] or input[data-vopt] radios
     [data-cart-ui]    drawer body and the cart page (data-ref-checkout = tracking ref of the send button)
     #cart-drawer      the drawer dialog ([data-cart-close] closes it) */
(function(){
var d=document,w=window,ce=d.getElementById('shop-cfg');if(!ce)return;
var C;try{C=JSON.parse(ce.textContent)}catch(e){return}
var S=C.s||{},P=C.pfx||'shop',K=P+'_cart_v1',KB=P+'_branch_v1',KN=P+'_name_v1',MAXL=C.max_lines||40,MAXQ=C.max_qty||99;
var IDS={};(C.ids||[]).forEach(function(i){IDS[i]=1});
var ok=true,mem=null,memB='',memN='',note='',full=false;
function dl(o){try{if(w.shopDL)w.shopDL(o);else(w.dataLayer=w.dataLayer||[]).push(o)}catch(e){}}
function t(k,n){var s=S[k]!=null?S[k]:k;return n==null?s:String(s).split('{n}').join(n)}
function esc(s){return String(s==null?'':s).replace(/[<>&"']/g,function(c){return{'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;',"'":'&#39;'}[c]})}
function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))}
function sget(k){try{var v=localStorage.getItem(k);ok=true;return v}catch(e){ok=false;return null}}
function sset(k,v){try{if(v==null)localStorage.removeItem(k);else localStorage.setItem(k,v);ok=true}catch(e){ok=false}}
function blank(){return{v:1,items:[],updated_at:null}}
function clean(c){if(!c||c.v!==1||!Array.isArray(c.items))return blank();var seen={},out=[];
  c.items.forEach(function(it){if(!it||typeof it.sku!=='string'||!it.sku||seen[it.sku]||out.length>=MAXL)return;seen[it.sku]=1;
    var q=Math.max(1,Math.min(MAXQ,parseInt(it.qty,10)||1));
    out.push({sku:it.sku.slice(0,64),group:String(it.group||'').slice(0,64),name:String(it.name||'').slice(0,200),brand:String(it.brand||'').slice(0,60),
      model:String(it.model||'').slice(0,80),variant:String(it.variant||'').slice(0,40),unit:String(it.unit||'').slice(0,12),qty:q,sample:!!it.sample,added_at:it.added_at||null})});
  return{v:1,items:out,updated_at:c.updated_at||null}}
function load(){var r=sget(K);if(!ok)return mem||blank();var c=null;try{c=r?JSON.parse(r):null}catch(e){c=null}c=clean(c);
  if(C.mode==='live'){var n=c.items.length;c.items=c.items.filter(function(it){return!it.sample});if(c.items.length!==n)save(c,true)} /* sample lines go silently once the live feed is on */
  mem=c;return c}
function save(c,quiet){c.updated_at=new Date().toISOString();mem=c;sset(K,JSON.stringify(c));if(!quiet)render()}
function find(c,sku){for(var i=0;i<c.items.length;i++)if(c.items[i].sku===sku)return i;return-1}
function total(c){return c.items.reduce(function(a,b){return a+b.qty},0)}
function isReal(it){return!it.sample&&!/^SAMPL[E]-/i.test(it.sku)}
function price(sku){var p=C.price_mode==='show'&&C.prices?C.prices[sku]:null;return p?parseFloat(p):null}
function money(n){return(C.cur||'RM')+' '+n.toFixed(2)}
function ev(name,items){dl({event:name,ecommerce:{items:items.map(function(it){return{item_id:it.sku,quantity:it.qty}})},cart_lines:cartNow().items.length,cart_qty:total(cartNow())})}
function cartNow(){return mem||load()}
/* ---------- actions ---------- */
function add(it){var c=load(),i=find(c,it.sku);full=false;
  if(i>-1)c.items[i].qty=Math.min(MAXQ,c.items[i].qty+1);
  else{if(c.items.length>=MAXL){full=true;render();return false}c.items.push({sku:it.sku,group:it.group,name:it.name,brand:it.brand,model:it.model,variant:it.variant,unit:it.unit,qty:1,sample:it.sample,added_at:new Date().toISOString()})}
  save(c);ev('add_to_cart',[{sku:it.sku,qty:1}]);return true}
function setQ(sku,q,allowZero){var c=load(),i=find(c,sku);if(i<0)return;full=false;
  if(q<1){if(!allowZero)return;var it=c.items.splice(i,1)[0];save(c);ev('remove_from_cart',[it]);return}
  var old=c.items[i].qty;c.items[i].qty=Math.min(MAXQ,q);save(c);if(q<old)ev('remove_from_cart',[{sku:sku,qty:old-q}]);else if(q>old)ev('add_to_cart',[{sku:sku,qty:q-old}])}
function rm(sku){var c=load(),i=find(c,sku);if(i<0)return;var it=c.items.splice(i,1)[0];full=false;save(c);ev('remove_from_cart',[it])}
function clearAll(){var c=load();if(!c.items.length)return;var old=c.items.slice();c.items=[];full=false;save(c);ev('remove_from_cart',old)}
/* ---------- WhatsApp message ---------- */
function bname(it){var n=it.name||'',b=it.brand||'';return b&&n.toLowerCase().indexOf(b.toLowerCase()+' ')===0?n.slice(b.length+1):n}
function brId(){var v=sget(KB);return ok?(v||''):memB}
function brName(id){for(var i=0;i<(C.branches||[]).length;i++)if(C.branches[i].id===id)return C.branches[i].name;return''}
function custName(){var v=sget(KN);return(ok?(v||''):memN).slice(0,60)}
function waUrl(c){var br=brName(brId())||t('no_preference'),nm=custName().trim(),nt=note.trim().slice(0,200),it=c.items;
  function line(x,i,fullInfo){var n=bname(x),parts=[];
    if(fullInfo&&x.model&&n.toLowerCase().indexOf(x.model.toLowerCase())<0)parts.push(x.model);
    if(x.variant)parts.push(x.variant);if(fullInfo&&isReal(x))parts.push('SKU '+x.sku);
    var s=(i+1)+'. '+(x.brand?x.brand+' ':'')+n+(parts.length?' ('+parts.join(', ')+')':'')+' x '+x.qty,p=price(x.sku);
    if(p!=null)s+=' · '+money(p*x.qty);return s}
  function make(fullInfo,max){var L=[t('wa_intro'),t('wa_branch')+t('wa_sep')+br],n=Math.min(it.length,max);
    for(var i=0;i<n;i++)L.push(line(it[i],i,fullInfo));if(it.length>n)L.push(t('wa_more',it.length-n));
    if(nm)L.push(t('wa_name')+t('wa_sep')+nm);if(nt)L.push(t('wa_note')+t('wa_sep')+nt);L.push(t('wa_thanks'));
    return'https://wa.me/'+C.wa+'?text='+encodeURIComponent(L.join('\n'))}
  var u=make(true,it.length);if(u.length>1800)u=make(false,it.length);
  if(u.length>1800){var m=Math.min(15,it.length);u=make(false,m);while(u.length>1800&&m>1){m--;u=make(false,m)}}
  return u}
w.shopCartWaUrl=function(){return waUrl(cartNow())}; /* QA hook: the exact link the send button uses */
/* ---------- render: header badge ---------- */
function badge(c){var n=total(c),lab=n===1?t('cart_items_one',n):t('cart_items',n);
  $$('[data-cart-count]').forEach(function(b){b.textContent=n>99?'99+':String(n);b.hidden=n===0});
  $$('[data-cart-open]').forEach(function(a){a.setAttribute('aria-label',lab)})}
/* ---------- render: card and product page controls ---------- */
function chosen(box){var sel=box.querySelector('[data-variant-select]'),btn=box.querySelector('[data-add]');if(!btn)return null;
  var o={sku:btn.getAttribute('data-sku'),group:btn.getAttribute('data-group')||'',name:btn.getAttribute('data-name')||'',brand:btn.getAttribute('data-brand')||'',
    model:btn.getAttribute('data-model')||'',variant:btn.getAttribute('data-variant')||'',unit:btn.getAttribute('data-unit')||'',sample:btn.getAttribute('data-sample')==='1'};
  var src=null;if(sel)src=sel.options[sel.selectedIndex];else{var r=box.querySelector('input[data-vopt]:checked');if(r)src=r;else if(box.querySelector('input[data-vopt]'))return null}
  if(src){if(!src.getAttribute('data-sku'))return null;o.sku=src.getAttribute('data-sku');o.variant=src.getAttribute('data-variant')||'';o.unit=src.getAttribute('data-unit')||o.unit;if(src.getAttribute('data-model'))o.model=src.getAttribute('data-model')}
  return o}
function stepper(box){var s=box.querySelector('.qty-c');if(s)return s;s=d.createElement('div');s.className='qty qty-c';s.hidden=true;
  s.innerHTML='<button type="button" class="q-dec" aria-label="'+esc(t('qty_dec'))+'">−</button><span class="q-n" aria-live="polite"></span><button type="button" class="q-inc" aria-label="'+esc(t('qty_inc'))+'">+</button>';
  var b=box.querySelector('[data-add]');b.parentNode.insertBefore(s,b.nextSibling);return s}
function syncBox(box,c){var btn=box.querySelector('[data-add]');if(!btn)return;var o=chosen(box),i=o?find(c,o.sku):-1,s=stepper(box);
  btn.disabled=!o;btn.setAttribute('aria-disabled',o?'false':'true');
  if(i>-1){btn.hidden=true;s.hidden=false;s.querySelector('.q-n').textContent=c.items[i].qty;s.querySelector('.q-n').setAttribute('aria-label',t('qty')+' '+c.items[i].qty);
    s.querySelector('.q-inc').disabled=c.items[i].qty>=MAXQ}else{btn.hidden=false;s.hidden=true}
  var pe=box.querySelector('[data-price]');if(pe){var p=o?price(o.sku):null;pe.textContent=p!=null?money(p):'';pe.hidden=p==null}}
function flash(box,txt){var a=box.querySelector('[data-added]');if(!a)return;a.textContent=txt;box.classList.add('just-added');clearTimeout(box._ft);box._ft=setTimeout(function(){box.classList.remove('just-added');a.textContent=''},1800)}
/* ---------- render: cart UI (drawer + cart page) ---------- */
function opts(){var id=brId(),h='<option value="">'+esc(t('no_preference'))+'</option>';(C.branches||[]).forEach(function(b){h+='<option value="'+esc(b.id)+'"'+(b.id===id?' selected':'')+'>'+esc(b.name)+'</option>'});return h}
function skeleton(ui){if(ui._b)return;ui._b=1;var u=ui.getAttribute('data-uid')||('cu'+Math.random().toString(36).slice(2,7));
  ui.innerHTML='<p class="cu-note" hidden>'+esc(t('not_saved'))+'</p><p class="cu-full" hidden role="status">'+esc(t('cart_full',MAXL))+'</p>'+
  '<div class="cu-empty" hidden><p>'+esc(t('cart_empty'))+'</p><a class="btn btn-line btn-sm" href="'+esc(C.cats_url)+'">'+esc(t('browse_categories'))+'</a></div>'+
  '<ul class="cu-lines" aria-label="'+esc(t('cart'))+'"></ul>'+
  '<div class="cu-foot"><div class="cu-tools"><button type="button" class="cu-clear">'+esc(t('clear_cart'))+'</button></div>'+
  '<label class="cu-f" for="'+u+'-br"><span>'+esc(t('pickup_branch'))+'</span><select id="'+u+'-br" class="cu-br">'+opts()+'</select></label>'+
  '<label class="cu-f" for="'+u+'-nm"><span>'+esc(t('your_name'))+'</span><input id="'+u+'-nm" class="cu-nm" type="text" maxlength="60" autocomplete="name"></label>'+
  '<label class="cu-f" for="'+u+'-nt"><span>'+esc(t('note'))+'</span><textarea id="'+u+'-nt" class="cu-nt" maxlength="200" rows="2"></textarea><small class="cu-cnt">0/200</small></label>'+
  '<a class="btn btn-wa btn-lg cu-send" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="'+esc(ui.getAttribute('data-ref-checkout')||'whatsapp_cart')+'">'+(C.wa_icon||'')+'<span>'+esc(t('send_enquiry'))+'</span></a>'+
  '<p class="cu-fine">'+esc(t('cart_fine'))+'</p></div>';
  ui.querySelector('.cu-nm').value=custName();
  ui.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var li=b.closest('[data-sku]');
    if(b.classList.contains('cu-clear')){clearAll();var f=ui.querySelector('.cu-empty a');if(f)f.focus();return}
    if(!li)return;var sku=li.getAttribute('data-sku'),c=load(),i=find(c,sku);if(i<0)return;
    if(b.classList.contains('q-dec'))setQ(sku,c.items[i].qty-1,false);else if(b.classList.contains('q-inc'))setQ(sku,c.items[i].qty+1,false);
    else if(b.classList.contains('cl-rm')){var nx=li.nextElementSibling||li.previousElementSibling;rm(sku);var tg=nx&&ui.querySelector('[data-sku="'+(nx.getAttribute('data-sku')||'').replace(/"/g,'')+'"] .cl-rm');(tg||ui.querySelector('.cu-empty a')||ui.querySelector('.cu-clear')).focus()}});
  ui.querySelector('.cu-br').addEventListener('change',function(){memB=this.value;sset(KB,this.value||null);syncAll()});
  ui.querySelector('.cu-nm').addEventListener('input',function(){memN=this.value.slice(0,60);sset(KN,memN||null);syncAll(ui)});
  ui.querySelector('.cu-nt').addEventListener('input',function(){note=this.value.slice(0,200);syncAll(ui)});
  ui.querySelector('.cu-send').addEventListener('click',function(e){var c=load();if(!c.items.length){e.preventDefault();return}this.href=waUrl(c);ev('begin_checkout',c.items)})}
function syncAll(except){$$('[data-cart-ui]').forEach(function(ui){if(!ui._b)return;var nt=ui.querySelector('.cu-nt'),nm=ui.querySelector('.cu-nm'),br=ui.querySelector('.cu-br');
  if(ui!==except){if(nt.value!==note)nt.value=note;if(nm.value!==custName())nm.value=custName()}if(br.value!==brId())br.value=brId();
  ui.querySelector('.cu-cnt').textContent=note.length+'/200';var c=cartNow(),s=ui.querySelector('.cu-send');
  if(c.items.length){s.href=waUrl(c);s.removeAttribute('aria-disabled')}else{s.removeAttribute('href');s.setAttribute('aria-disabled','true')}})}
function lineHtml(x){var meta=[x.brand,x.model&&bname(x).toLowerCase().indexOf(x.model.toLowerCase())<0?x.model:'',x.variant].filter(Boolean).join(' · '),p=price(x.sku),miss=!IDS[x.sku];
  return'<li class="cl" data-sku="'+esc(x.sku)+'"><div class="cl-t"><b>'+esc(x.name)+'</b><small>'+esc(meta)+'</small>'+
  (p!=null?'<span class="cl-p">'+esc(money(p))+' × '+x.qty+' = '+esc(money(p*x.qty))+'</span>':'<span class="cl-p">'+esc(t('whatsapp_for_price'))+'</span>')+
  (miss?'<span class="cl-x">'+esc(t('no_longer_listed'))+'</span>':'')+'</div>'+
  '<div class="cl-c"><div class="qty" role="group" aria-label="'+esc(t('qty'))+'"><button type="button" class="q-dec" aria-label="'+esc(t('qty_dec'))+'"'+(x.qty<=1?' disabled':'')+'>−</button>'+
  '<span class="q-n" aria-live="polite" aria-label="'+esc(t('qty')+' '+x.qty)+'">'+x.qty+'</span><button type="button" class="q-inc" aria-label="'+esc(t('qty_inc'))+'"'+(x.qty>=MAXQ?' disabled':'')+'>+</button></div>'+
  '<button type="button" class="cl-rm" aria-label="'+esc(t('remove')+': '+x.name+(x.variant?' '+x.variant:''))+'">'+esc(t('remove'))+'</button></div></li>'}
function render(){var c=cartNow();badge(c);$$('[data-cart-item]').forEach(function(b){syncBox(b,c)});
  $$('[data-cart-ui]').forEach(function(ui){skeleton(ui);var has=c.items.length>0;
    ui.querySelector('.cu-note').hidden=ok;ui.querySelector('.cu-full').hidden=!full;ui.querySelector('.cu-empty').hidden=has;ui.querySelector('.cu-foot').hidden=!has;
    var ul=ui.querySelector('.cu-lines'),html=c.items.map(lineHtml).join(''),ae=d.activeElement,li=ae&&ul.contains(ae)&&ae.closest('[data-sku]'),foc=li?[li.getAttribute('data-sku'),ae.className||'cl-rm']:null;
    if(ul._h!==html){ul.innerHTML=html;ul._h=html;if(foc){var f=ul.querySelector('[data-sku="'+foc[0].replace(/"/g,'')+'"] .'+foc[1].split(' ')[0]);if(f&&!f.disabled)f.focus();else{f=ul.querySelector('[data-sku="'+foc[0].replace(/"/g,'')+'"] .cl-rm');if(f)f.focus()}}}
    ul.hidden=!has});
  syncAll()}
/* ---------- card / product page events ---------- */
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-add]');if(b){var box=b.closest('[data-cart-item]'),o=box&&chosen(box);if(!o)return;
    if(add(o)){var s=box.querySelector('.qty-c .q-inc');if(s)s.focus();flash(box,t('added'))}else flash(box,t('cart_full',MAXL));return}
  var q=e.target.closest&&e.target.closest('.qty-c button');if(q){var bx=q.closest('[data-cart-item]'),oo=chosen(bx);if(!oo)return;var c=load(),i=find(c,oo.sku);if(i<0)return;
    var nq=c.items[i].qty+(q.classList.contains('q-inc')?1:-1);setQ(oo.sku,nq,true);if(nq<1){var ab=bx.querySelector('[data-add]');if(ab)ab.focus()}}});
d.addEventListener('change',function(e){var bx=e.target.closest&&e.target.closest('[data-cart-item]');if(bx&&(e.target.matches('[data-variant-select]')||e.target.matches('input[data-vopt]')))syncBox(bx,cartNow())});
/* ---------- drawer ---------- */
var dr=d.getElementById('cart-drawer'),last=null,onPage=!!d.querySelector('[data-cart-page]');
function focusables(){return $$('a[href],button:not([disabled]),select,input,textarea,[tabindex]:not([tabindex="-1"])',dr).filter(function(x){return x.offsetParent!==null})}
function open(){if(!dr)return;last=d.activeElement;dr.hidden=false;dr.setAttribute('aria-hidden','false');d.documentElement.classList.add('noscroll');render();
  requestAnimationFrame(function(){dr.classList.add('open');var cb=dr.querySelector('.cd-x');if(cb)cb.focus()});ev('view_cart',cartNow().items)}
function close(){if(!dr||dr.hidden)return;dr.classList.remove('open');dr.setAttribute('aria-hidden','true');d.documentElement.classList.remove('noscroll');
  setTimeout(function(){dr.hidden=true},200);if(last&&last.focus)last.focus()}
w.shopCartOpen=open;
$$('[data-cart-open]').forEach(function(a){a.addEventListener('click',function(e){if(onPage){e.preventDefault();var u=d.querySelector('[data-cart-page]');if(u)u.scrollIntoView({block:'start'});return}if(dr){e.preventDefault();open()}})});
if(dr){$$('[data-cart-close]',dr).forEach(function(x){x.addEventListener('click',close)});
  dr.addEventListener('keydown',function(e){if(e.key==='Escape'){e.stopPropagation();close();return}
    if(e.key==='Tab'){var f=focusables();if(!f.length)return;var a=f[0],z=f[f.length-1];if(e.shiftKey&&d.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&d.activeElement===z){e.preventDefault();a.focus()}}})}
/* ---------- other tabs ---------- */
w.addEventListener('storage',function(e){if(e.key===K||e.key===KB||e.key===KN||e.key===null){mem=null;load();render()}});
load();render();if(onPage)ev('view_cart',cartNow().items);
})();

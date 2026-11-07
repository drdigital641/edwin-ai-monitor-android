# Towner picker v3 (7 Nov 2026): one carousel of style-specific room concepts, driven by flat type + style.
# A room becomes a slide (and gets a room chip + plan hotspot) only when its img is "style", meaning
# images/new-launches/<slug>/<slug>-<prefix><style>-<room id>.webp exists for all four styles.
# When Maison sends the remaining images, set that room's img to "style" and rebuild.
import json as _json

PICKER2 = {
 "4": dict(label="4-room", units="226 units · HDB p.14", plan="maison-plan", ph=1640,
           plan_alt="Maison redrawn floor plan of a Towner Residences 4-room flat (first p.12 arrangement), for illustration",
           src="https://btohq.sgp1.cdn.digitaloceanspaces.com/bto/aug-2021-bto/towner-residences.pdf#page=8",
           note="4-room first arrangement (the first of two on HDB brochure p.12): 90 sqm / approx. 93 sqm.",
           prefix="", rooms=[("living", "Living/Dining", .30, .54, "style"), ("kitchen", "Kitchen", .438, .74, "style"),
                             ("bedroom", "Main bedroom", .778, .39, "style"), ("bedroom-2", "Bedroom 2", .421, .31, "style"),
                             ("bedroom-3", "Bedroom 3", .602, .31, "style")]),
 "3": dict(label="3-room", units="90 units · HDB p.14", plan="maison-plan-3room", ph=1640,
           plan_alt="Maison redrawn floor plan of a Towner Residences 3-room flat, for illustration",
           src="https://btohq.sgp1.cdn.digitaloceanspaces.com/bto/aug-2021-bto/towner-residences.pdf#page=7",
           note="3-room, HDB brochure p.10: 65 sqm / approx. 68 sqm.",
           prefix="3room-", rooms=[("living", "Living/Dining", .684, .52, "style"), ("kitchen", "Kitchen", .484, .825, "style"),
                                   ("bedroom", "Main bedroom", .284, .37, "style"), ("bedroom-2", "Bedroom 2", .478, .31, "style")]),
}

PICKER2_V = "p3"
PICKER2_CSS = """
.vp2 [hidden]{display:none!important}
.vp2 .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.vp2.vsec{padding-top:20px}
.vp2-car{position:relative;margin:0 -20px}
.vp2-track{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain;outline-offset:-3px}
.vp2-track::-webkit-scrollbar{display:none}
.vp2-slide{flex:0 0 100%;scroll-snap-align:start;scroll-snap-stop:always;margin:0}
.vp2-ph{position:relative;aspect-ratio:16/9;background:var(--bg2);overflow:hidden}
.vp2-ph img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover}
.vp2-ph img.n{opacity:0;transition:opacity .2s ease;pointer-events:none}.vp2-ph img.n.on{opacity:1}
.vp2-slide figcaption{padding:8px 20px 0;font-size:15px;color:var(--ink)}
.vp2-slide figcaption span{display:block;font-size:12px;color:var(--mute)}
.vp2-arw{position:absolute;left:0;right:0;top:0;aspect-ratio:16/9;display:none;align-items:center;justify-content:space-between;padding:0 12px;pointer-events:none}
.vp2-arw button{pointer-events:auto;width:46px;height:46px;border-radius:50%;border:0;background:rgba(244,239,232,.92);color:var(--ink);font-size:22px;line-height:1;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.vp2-nav{display:flex;align-items:center;gap:6px;padding:6px 20px 0}
.vp2-dots{display:flex;gap:2px}
.vp2-dots button{width:28px;height:28px;border:0;background:none;padding:0;cursor:pointer;display:flex;align-items:center;justify-content:center}
.vp2-dots button i{width:8px;height:8px;border-radius:50%;background:var(--line);border:1px solid var(--mute)}
.vp2-dots button[aria-pressed="true"] i{background:var(--ink);border-color:var(--ink)}
.vp2-count{font-size:13px;color:var(--ink2);margin-left:auto}
.vp2-chips{margin-top:4px}
.vp2-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:8px}
.vp2 button.pill{min-height:40px;padding:0 12px;border:1px solid var(--ink);background:transparent;color:var(--ink);font:500 12px/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;cursor:pointer}
.vp2 button.pill[aria-pressed="true"]{background:var(--ink);color:#fff}
.vp2-sty button.pill{flex:1 1 0;padding:0 4px}
.vp2-units{font-size:13px;color:var(--ink2);margin-left:4px}
.vp2-rooms button{min-height:40px;padding:0 10px;border:1px solid var(--line);background:rgba(255,255,255,.55);color:var(--ink);font:400 14px/1.1 var(--sans);cursor:pointer;flex:1 1 auto}
.vp2-rooms button[aria-pressed="true"]{border-color:var(--ink);background:var(--brass);color:#fff}
.vp2-src{font-size:12px;color:var(--mute);margin-top:8px}.vp2-src a,.vp2-off a{color:var(--brass);text-decoration:underline}
.vp2-navh{font:400 22px/1.2 var(--serif);margin:28px 0 4px}
.vp2-tap{margin:0 0 10px;font-size:14px;color:var(--ink2)}
.vp2-plan{position:relative;border:1px solid var(--line);background:#f5f2ec}
.vp2-plan a{display:block}.vp2-plan img{display:block;width:100%;height:auto;aspect-ratio:1920/1640}
.vp2-hs{position:absolute;transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;border:2px solid #fff;background:#3f4a3c;color:#fff;font:600 15px/1 var(--sans);cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.3);padding:0}
.vp2-hs[aria-pressed="true"]{background:var(--brass);transform:translate(-50%,-50%) scale(1.15)}
.vp2-off{font-size:15px;margin-top:10px}
@media(min-width:900px){.vp2-ph,.vp2-arw{width:100%;max-height:max(300px,calc(100vh - 320px))}.vp2-ph img{object-position:50% 100%}.vp2.vsec{padding-top:32px}.vp2-car,.vp2-chips{max-width:960px;margin-left:auto;margin-right:auto}.vp2-arw{display:flex}
.vp2-slide figcaption,.vp2-nav{padding-left:0;padding-right:0}.vp2-sty button.pill{flex:0 0 auto;padding:0 14px}
.vp2-navw{display:grid;grid-template-columns:3fr 2fr;gap:32px;align-items:end}}
"""

def _p2_slides(k):
    return [r for r in PICKER2[k]["rooms"] if r[4] == "style"]

def picker2(slug, h1, wa):
    V = PICKER2_V
    b = f"{BASE}images/new-launches/{slug}/{slug}"
    t = PICKER2["4"]
    data = {k: dict(label=v["label"], units=v["units"], plan=v["plan"], alt=v["plan_alt"], src=v["src"], note=v["note"], prefix=v["prefix"],
                    rooms=[dict(id=r[0], label=r[1], x=r[2], y=r[3]) for r in _p2_slides(k)]) for k, v in PICKER2.items()}
    sl = _p2_slides("4")
    types = "".join(f'<button type="button" class="pill" data-t="{k}" aria-pressed="{"true" if k == "4" else "false"}">{v["label"]}</button>' for k, v in sorted(PICKER2.items()))
    styles = "".join(f'<button type="button" class="pill" data-s="{x.lower()}" aria-pressed="{"true" if i == 0 else "false"}">{x}</button>' for i, x in enumerate(STYLES))
    hs = "".join(f'<button type="button" class="vp2-hs" data-i="{i}" style="left:{r[2]*100:.1f}%;top:{r[3]*100:.1f}%" aria-label="{i+1}. {r[1]}" aria-pressed="{"true" if i == 0 else "false"}">{i+1}</button>' for i, r in enumerate(sl))
    rooms = "".join(f'<button type="button" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">{i+1}. {r[1]}</button>' for i, r in enumerate(sl))
    def slide(i, r):
        f = f"{b}-modern-{r[0]}"
        alt = f"AI concept: Modern style {r[1].lower().replace('/', ' and ')} for a Towner Residences 4-room flat"
        return (f'<figure class="vp2-slide" aria-roledescription="slide" aria-label="{i+1} of {len(sl)}">'
                f'<div class="vp2-ph"><img class="b" src="{f}.webp?v={V}" srcset="{f}-960.webp?v={V} 960w, {f}.webp?v={V} 1920w" sizes="(min-width:900px) 960px, 100vw" '
                f'width="1920" height="1080" alt="{e(alt)}"{"" if i == 0 else " loading=\"lazy\""} decoding="async"><img class="n" alt="" aria-hidden="true" width="1920" height="1080"></div>'
                f'<figcaption><b>Modern · {r[1]}</b><span>AI concept, for illustration only</span></figcaption></figure>')
    slides = "".join(slide(i, r) for i, r in enumerate(sl))
    dots = "".join(f'<button type="button" data-i="{i}" aria-label="Slide {i+1}" aria-pressed="{"true" if i == 0 else "false"}"><i></i></button>' for i in range(len(sl)))
    pl = f"{b}-{t['plan']}"
    return (f'<style>{PICKER2_CSS}</style><section class="vsec vp2" id="choose"><div class="wrap"><h2 class="sr">Choose your flat, style and room</h2>'
            f'<div class="vp2-car" aria-roledescription="carousel" aria-label="Room concepts">'
            f'<div class="vp2-track" tabindex="0">{slides}</div>'
            f'<div class="vp2-arw"><button type="button" class="vp2-prev" aria-label="Previous slide">&#8249;</button><button type="button" class="vp2-next" aria-label="Next slide">&#8250;</button></div>'
            f'<div class="vp2-nav"><div class="vp2-dots">{dots}</div><span class="vp2-count">1 / {len(sl)}</span></div></div>'
            f'<div class="vp2-chips"><div class="vp2-row vp2-type" role="group" aria-label="Flat type">{types}<span class="vp2-units">{t["units"]}</span></div>'
            f'<div class="vp2-row vp2-sty" role="group" aria-label="Style">{styles}</div>'
            f'<div class="vp2-row vp2-rooms" role="group" aria-label="Room">{rooms}</div>'
            f'<p class="vp2-src">AI concepts, for illustration only; all cabinetry, furnishings and finishes are proposed. {e(t["note"])} Source: <a href="{t["src"]}" target="_blank" rel="noopener">HDB brochure (archive copy)</a></p></div>'
            f'<h3 class="vp2-navh">Tap a room on the plan</h3><p class="vp2-tap">Or use the room buttons above.</p>'
            f'<div class="vp2-navw"><div class="vp2-plan"><a href="{pl}.webp?v={V}" target="_blank" rel="noopener"><img src="{pl}.webp?v={V}" srcset="{pl}-960.webp?v={V} 960w, {pl}.webp?v={V} 1920w" '
            f'sizes="(min-width:900px) 58vw, 100vw" width="1920" height="1640" alt="{e(t["plan_alt"])}" loading="lazy" decoding="async"></a>{hs}</div>'
            f'<p class="vp2-off"><a href="https://assets.hdb.gov.sg/community/towner_residences/index.html" target="_blank" rel="noopener">View official floor plan</a></p></div></div></section>'
            f'<script>window.VP2={_json.dumps(data)};window.VP2B="{b}";window.VP2Q="?v={V}";</script>'
            + JS2)

JS2 = r"""<script>(function(){var D=VP2,B=VP2B,Q=VP2Q,w=document.getElementById('choose'),st={t:'4',s:'modern',i:0},tok=0,
q=function(x){return w.querySelector(x)},qa=function(x){return [].slice.call(w.querySelectorAll(x))},tr=q('.vp2-track'),
RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function cap(x){return x.charAt(0).toUpperCase()+x.slice(1)}
function big(){return innerWidth>960||devicePixelRatio>1.5&&innerWidth>480}
function file(t,s,r){return B+'-'+D[t].prefix+s+'-'+r.id}
function sz(f){return f+(big()?'.webp':'-960.webp')+Q}
var C={};function pre(u){if(!C[u]){C[u]=new Promise(function(res){var i=new Image();i.onload=function(){i.decode?i.decode().then(res,res):res()};i.onerror=function(){res()};i.src=u})}return C[u]}
function idle(fn){(window.requestIdleCallback||function(c){setTimeout(c,600)})(fn)}
function rooms(){return D[st.t].rooms}
function warm(){var R=rooms(),r=R[st.i],n=R[(st.i+1)%R.length];pre(sz(file(st.t,st.s,n)));
idle(function(){['modern','luxury','scandi','japandi'].forEach(function(x){pre(sz(file(st.t,x,r)))})})}
function press(sel,v){qa(sel).forEach(function(b){b.setAttribute('aria-pressed',+b.dataset[v.k]===v.v||b.dataset[v.k]===v.v?'true':'false')})}
function mark(){press('.vp2-dots button',{k:'i',v:st.i});press('.vp2-rooms button',{k:'i',v:st.i});press('.vp2-hs',{k:'i',v:st.i});
q('.vp2-count').textContent=(st.i+1)+' / '+rooms().length}
function go(i,inst){var n=rooms().length;st.i=(i+n)%n;tr.scrollTo({left:st.i*tr.clientWidth,behavior:inst||RM?'auto':'smooth'});mark();warm()}
/* swap one slide's photo: old one stays until the new one is loaded and decoded, then a short fade */
function swap(fig,r,my){var T=D[st.t],S=cap(st.s),u=sz(file(st.t,st.s,r)),b=fig.querySelector('img.b'),n=fig.querySelector('img.n'),
alt='AI concept: '+S+' style '+r.label.toLowerCase().replace('/',' and ')+' for a Towner Residences '+T.label+' flat',txt=S+' · '+r.label;
return pre(u).then(function(){if(my!==tok)return;n.src=u;return n.decode?n.decode().catch(function(){}):0}).then(function(){if(my!==tok)return;
n.classList.add('on');fig.querySelector('figcaption b').textContent=txt;
setTimeout(function(){if(my!==tok)return;b.removeAttribute('srcset');b.removeAttribute('loading');b.src=u;b.alt=alt;
(b.decode?b.decode().catch(function(){}):Promise.resolve()).then(function(){if(my!==tok)return;n.style.transition='none';n.classList.remove('on');void n.offsetWidth;n.style.transition=''})},230)})}
function slideHTML(r,i,len){return '<figure class="vp2-slide" aria-roledescription="slide" aria-label="'+(i+1)+' of '+len+'"><div class="vp2-ph"><img class="b" alt="" width="1920" height="1080"><img class="n" alt="" aria-hidden="true" width="1920" height="1080"></div><figcaption><b></b><span>AI concept, for illustration only</span></figcaption></figure>'}
/* rebuild for the current type + style; keeps the same room when it exists */
function build(keepId){var T=D[st.t],R=T.rooms,figs=qa('.vp2-slide'),same=figs.length===R.length&&figs.every(function(f,i){return f.dataset.r===R[i].id}),my=++tok;
if(!same){tr.innerHTML=R.map(function(r,i){return slideHTML(r,i,R.length)}).join('');figs=qa('.vp2-slide');
figs.forEach(function(f,i){f.dataset.r=R[i].id;var u=sz(file(st.t,st.s,R[i])),b=f.querySelector('img.b');if(i!==st.i)b.loading='lazy';b.src=u});
q('.vp2-dots').innerHTML=R.map(function(r,i){return '<button type="button" data-i="'+i+'" aria-label="Slide '+(i+1)+'"><i></i></button>'}).join('');bindDots()}
var k=R.map(function(r){return r.id}).indexOf(keepId);st.i=k<0?0:k;
/* current slide first, then the rest */
swap(figs[st.i],R[st.i],my).then(function(){figs.forEach(function(f,i){if(i!==st.i)swap(f,R[i],my)})});
go(st.i,true)}
function buildType(){var T=D[st.t],p=q('.vp2-plan'),rb='',pl=B+'-'+T.plan,im=p.querySelector('img');
im.src=pl+'.webp'+Q;im.srcset=pl+'-960.webp'+Q+' 960w, '+pl+'.webp'+Q+' 1920w';im.alt=T.alt;p.querySelector('a').href=pl+'.webp'+Q;
p.querySelectorAll('.vp2-hs').forEach(function(x){x.remove()});
T.rooms.forEach(function(r,i){var b=document.createElement('button');b.type='button';b.className='vp2-hs';b.dataset.i=i;b.style.left=(r.x*100)+'%';b.style.top=(r.y*100)+'%';b.setAttribute('aria-label',(i+1)+'. '+r.label);b.textContent=i+1;p.appendChild(b);
rb+='<button type="button" data-i="'+i+'">'+(i+1)+'. '+r.label+'</button>'});
q('.vp2-rooms').innerHTML=rb;q('.vp2-units').textContent=T.units;
var s=q('.vp2-src'),a=s.querySelector('a');s.firstChild.textContent='AI concepts, for illustration only; all cabinetry, furnishings and finishes are proposed. '+T.note+' Source: ';a.href=T.src;bindRooms()}
/* after a tap, bring the photo fully into view just under the fixed header; no scroll if already fully visible */
function toCar(){var h=document.getElementById('hd'),hb=h?Math.max(0,h.getBoundingClientRect().bottom):0,c=q('.vp2-ph').getBoundingClientRect();
if(c.top<hb||c.bottom>innerHeight){scrollTo({top:Math.max(0,c.top+scrollY-hb-8),behavior:RM?'auto':'smooth'})}}
function bindRooms(){qa('.vp2-rooms button,.vp2-hs').forEach(function(b){b.onclick=function(){hold(4000);go(+b.dataset.i);toCar()}})}
function bindDots(){qa('.vp2-dots button').forEach(function(b){b.onclick=function(){hold(4000);go(+b.dataset.i)}})}
qa('.vp2-slide').forEach(function(f,i){f.dataset.r=rooms()[i].id});
qa('.vp2-type button').forEach(function(b){b.onclick=function(){if(st.t===b.dataset.t)return;var id=rooms()[st.i].id;st.t=b.dataset.t;press('.vp2-type button',{k:'t',v:st.t});buildType();build(id);hold(4000);toCar()}});
qa('.vp2-sty button').forEach(function(b){b.onclick=function(){if(st.s===b.dataset.s)return;st.s=b.dataset.s;press('.vp2-sty button',{k:'s',v:st.s});build(rooms()[st.i].id);hold(4000);toCar()}});
q('.vp2-prev').onclick=function(){hold(4000);go(st.i-1)};q('.vp2-next').onclick=function(){hold(4000);go(st.i+1)};
tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();hold(4000);go(st.i+1)}else if(e.key==='ArrowLeft'){e.preventDefault();hold(4000);go(st.i-1)}});
/* follow manual swipes */
var raf=0;tr.addEventListener('scroll',function(){if(raf)return;raf=requestAnimationFrame(function(){raf=0;var i=Math.round(tr.scrollLeft/Math.max(1,tr.clientWidth));if(i!==st.i&&i<rooms().length){st.i=i;mark();warm()}})},{passive:true});
addEventListener('resize',function(){tr.scrollTo({left:st.i*tr.clientWidth})});
/* Edwin's carousel standard: slides on its own, keeps going while the page scrolls,
   pauses only while a finger or mouse holds or drags it, restarts about 2s after release */
var held=false,until=0,DUR=5000;
function hold(ms){until=Date.now()+ms}
['touchstart','pointerdown'].forEach(function(ev){tr.addEventListener(ev,function(){held=true},{passive:true})});
['touchend','touchcancel','pointerup','pointercancel'].forEach(function(ev){addEventListener(ev,function(){if(held){held=false;hold(2000)}},{passive:true})});
if(!RM)setInterval(function(){if(held||Date.now()<until||rooms().length<2)return;go(st.i+1)},DUR);
bindRooms();bindDots();mark();idle(warm)})()</script>"""

# Towner style picker v2: flat type -> style -> room (config from Edwin's team, 7 Nov 2026).
import json as _json

PICKER2 = {
 "4": dict(label="4-room", units="226 units · HDB p.14", plan="maison-plan", ph=1640,
           plan_alt="Maison redrawn floor plan of a Towner Residences 4-room flat (first p.12 arrangement), for illustration",
           src="https://btohq.sgp1.cdn.digitaloceanspaces.com/bto/aug-2021-bto/towner-residences.pdf#page=8",
           note="4-room first arrangement (the first of two on HDB brochure p.12): 90 sqm / approx. 93 sqm.",
           prefix="", rooms=[("living", "Living/Dining", .365, .48, "style"), ("kitchen", "Kitchen", .44, .73, "kitchen"),
                             ("bedroom", "Main bedroom", .777, .33, "style"), ("bedroom-2", "Bedroom 2", .419, .29, None),
                             ("bedroom-3", "Bedroom 3", .594, .29, "study")]),
 "3": dict(label="3-room", units="90 units · HDB p.14", plan="maison-plan-3room", ph=1640,
           plan_alt="Maison redrawn floor plan of a Towner Residences 3-room flat, for illustration",
           src="https://btohq.sgp1.cdn.digitaloceanspaces.com/bto/aug-2021-bto/towner-residences.pdf#page=7",
           note="3-room, HDB brochure p.10: 65 sqm / approx. 68 sqm.",
           prefix="3room-", rooms=[("living", "Living/Dining", .697, .44, "style"), ("kitchen", "Kitchen", .447, .747, None),
                                   ("bedroom", "Main bedroom", .251, .308, "style"), ("bedroom-2", "Bedroom 2", .478, .278, None)]),
}
FIXED_CAP = {"kitchen": "Kitchen concept (same for all styles)", "study": "Bedroom 3 as a study (same for all styles)"}
EMPTY_TXT = "No verified concept for this room yet. Share your approved plan with Maison."

PICKER2_CSS = """
.vp2 [hidden]{display:none!important}
.vp2-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:14px 0 0}
.vp2 button.pill{min-height:44px;padding:0 18px;border:1px solid var(--ink);background:transparent;color:var(--ink);font:500 13px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;cursor:pointer}
.vp2 button.pill[aria-pressed="true"]{background:var(--ink);color:#fff}
.vp2 .vp2-sty button.pill{flex:1 1 calc(50% - 8px)}
@media(min-width:560px){.vp2 .vp2-sty button.pill{flex:0 0 auto}}
.vp2-units{font-size:14px;color:var(--ink2);margin-left:6px}
.vp2-plan{position:relative;margin-top:16px;border:1px solid var(--line);background:#f5f2ec}
.vp2-plan a{display:block}.vp2-plan img{display:block;width:100%;height:auto;aspect-ratio:1920/1640}
.vp2-hs{position:absolute;transform:translate(-50%,-50%);width:34px;height:34px;border-radius:50%;border:2px solid #fff;background:#3f4a3c;color:#fff;font:600 15px/1 var(--sans);cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.3);padding:0}
.vp2-hs[aria-pressed="true"]{background:var(--brass);transform:translate(-50%,-50%) scale(1.15)}
.vp2-off{font-size:15px;margin-top:10px}.vp2-off a,.vp2-src a{color:var(--brass);text-decoration:underline}
.vp2-tap{margin:18px 0 0;font-size:15px;color:var(--ink2)}
.vp2-rooms{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
@media(min-width:700px){.vp2-rooms{grid-template-columns:repeat(3,1fr)}}
.vp2-rooms button{min-height:44px;border:1px solid var(--line);background:rgba(255,255,255,.5);color:var(--ink);font:400 15px/1.2 var(--sans);cursor:pointer;padding:6px 10px}
.vp2-rooms button[aria-pressed="true"]{border-color:var(--ink);background:var(--ink);color:#fff}
.vp2-view{margin-top:18px}.vp2-view figure{margin:0}
.vp2-view img{display:block;width:100%;height:auto;aspect-ratio:16/9;background:var(--bg2)}
.vp2-cap{font-size:15px;color:var(--ink);margin-top:8px}
.vp2-empty{aspect-ratio:16/9;border:1px dashed var(--mute);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:20px;text-align:center;color:var(--ink2);background:rgba(255,255,255,.4)}
.vp2-src{font-size:13px;color:var(--mute);margin-top:8px}
@media(min-width:900px){.vp2-grid{display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:start}.vp2-view{margin-top:16px}}
"""

def picker2(slug, h1, wa):
    b = f"{BASE}images/new-launches/{slug}/{slug}"
    t = PICKER2["4"]
    data = {k: dict(label=v["label"], units=v["units"], plan=v["plan"], ph=v["ph"], alt=v["plan_alt"], src=v["src"], note=v["note"],
                    prefix=v["prefix"], rooms=[dict(id=r[0], label=r[1], x=r[2], y=r[3], img=r[4]) for r in v["rooms"]]) for k, v in PICKER2.items()}
    types = "".join(f'<button type="button" class="pill" data-t="{k}" aria-pressed="{"true" if k == "4" else "false"}">{v["label"]}</button>' for k, v in sorted(PICKER2.items()))
    styles = "".join(f'<button type="button" class="pill" data-s="{x.lower()}" aria-pressed="{"true" if i == 0 else "false"}">{x}</button>' for i, x in enumerate(STYLES))
    hs = "".join(f'<button type="button" class="vp2-hs" data-r="{r[0]}" style="left:{r[2]*100:.1f}%;top:{r[3]*100:.1f}%" aria-label="{i+1}. {r[1]}" aria-pressed="{"true" if i == 0 else "false"}">{i+1}</button>' for i, r in enumerate(t["rooms"]))
    rooms = "".join(f'<button type="button" data-r="{r[0]}" aria-pressed="{"true" if i == 0 else "false"}">{i+1}. {r[1]}</button>' for i, r in enumerate(t["rooms"]))
    pl = f"{b}-{t['plan']}"
    img = (f'<img src="{b}-modern-living.webp" srcset="{b}-modern-living-960.webp 960w, {b}-modern-living.webp 1920w" sizes="(min-width:900px) 45vw, 100vw" '
           f'width="1920" height="1080" alt="AI concept: Modern style living and dining for a Towner Residences 4-room flat" decoding="async">')
    empty = f'<div class="vp2-empty" hidden><p>{EMPTY_TXT}</p>{wa}</div>'
    return (f'<style>{PICKER2_CSS}</style><section class="vsec vp2"><div class="wrap"><h2 class="vh2">Choose your flat, style and room</h2>'
            f'<p class="vsub">AI concepts, for illustration only; all cabinetry, furnishings and finishes are proposed.</p>'
            f'<div class="vp2-row vp2-type" role="group" aria-label="Flat type">{types}<span class="vp2-units">{t["units"]}</span></div>'
            f'<div class="vp2-row vp2-sty" role="group" aria-label="Style">{styles}</div>'
            f'<div class="vp2-grid"><div><div class="vp2-plan"><a href="{pl}.webp" target="_blank" rel="noopener"><img src="{pl}.webp" srcset="{pl}-960.webp 960w, {pl}.webp 1920w" '
            f'sizes="(min-width:900px) 45vw, 100vw" width="1920" height="1640" alt="{e(t["plan_alt"])}" loading="lazy" decoding="async"></a>{hs}</div>'
            f'<p class="vp2-off"><a href="https://assets.hdb.gov.sg/community/towner_residences/index.html" target="_blank" rel="noopener">View official floor plan</a></p>'
            f'<p class="vp2-tap">Tap a room on the plan, or choose a room below.</p><div class="vp2-rooms" role="group" aria-label="Room">{rooms}</div></div>'
            f'<div class="vp2-view"><figure>{img}{empty}<figcaption class="vp2-cap">Modern · Living/Dining</figcaption></figure>'
            f'<p class="vp2-src">{e(t["note"])} Source: <a href="{t["src"]}" target="_blank" rel="noopener">HDB brochure (archive copy)</a></p></div></div></div></section>'
            f'<script>window.VP2={_json.dumps(data)};window.VP2B="{b}";window.VP2FIX={_json.dumps(FIXED_CAP)};</script>'
            + """<script>(function(){var D=VP2,B=VP2B,F=VP2FIX,w=document.currentScript.previousElementSibling.previousElementSibling,st={t:'4',s:'modern',r:'living'};
function q(s){return w.querySelector(s)}function qa(s){return w.querySelectorAll(s)}
function cap(x){return x.charAt(0).toUpperCase()+x.slice(1)}
function press(sel,attr,v){qa(sel).forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute(attr)===v?'true':'false')})}
function bind(){qa('.vp2-hs,.vp2-rooms button').forEach(function(b){b.onclick=function(){st.r=b.dataset.r;render()}})}
function buildType(){var T=D[st.t],p=q('.vp2-plan'),hs='',rb='';
var pl=B+'-'+T.plan,im=p.querySelector('img');im.src=pl+'.webp';im.srcset=pl+'-960.webp 960w, '+pl+'.webp 1920w';im.alt=T.alt;p.querySelector('a').href=pl+'.webp';
p.querySelectorAll('.vp2-hs').forEach(function(x){x.remove()});
T.rooms.forEach(function(r,i){var b=document.createElement('button');b.type='button';b.className='vp2-hs';b.dataset.r=r.id;b.style.left=(r.x*100)+'%';b.style.top=(r.y*100)+'%';b.setAttribute('aria-label',(i+1)+'. '+r.label);b.textContent=i+1;p.appendChild(b);
rb+='<button type="button" data-r="'+r.id+'">'+(i+1)+'. '+r.label+'</button>'});
q('.vp2-rooms').innerHTML=rb;q('.vp2-units').textContent=T.units;
var s=q('.vp2-src');s.firstChild.textContent=T.note+' Source: ';s.querySelector('a').href=T.src;bind()}
function render(){var T=D[st.t],r=T.rooms.filter(function(x){return x.id===st.r})[0],img=q('.vp2-view img'),em=q('.vp2-empty'),c=q('.vp2-cap'),S=cap(st.s),f;
press('.vp2-type button','data-t',st.t);press('.vp2-sty button','data-s',st.s);press('.vp2-hs','data-r',st.r);press('.vp2-rooms button','data-r',st.r);
if(r.img==='style'){f=B+'-'+T.prefix+st.s+'-'+r.id;c.textContent=S+' · '+r.label;img.alt='AI concept: '+S+' style '+r.label.toLowerCase().replace('/',' and ')+' for a Towner Residences '+T.label+' flat'}
else if(r.img){f=B+'-'+r.img;c.textContent=F[r.img];img.alt='AI concept: '+F[r.img]+', Towner Residences '+T.label}
if(f){img.srcset=f+'-960.webp 960w, '+f+'.webp 1920w';img.src=f+'.webp';img.hidden=false;em.hidden=true}
else{img.hidden=true;em.hidden=false;c.textContent=r.label+' · no concept yet'}}
qa('.vp2-type button').forEach(function(b){b.onclick=function(){if(st.t===b.dataset.t)return;st.t=b.dataset.t;st.r='living';buildType();render()}});
qa('.vp2-sty button').forEach(function(b){b.onclick=function(){st.s=b.dataset.s;render()}});bind()})()</script>""")

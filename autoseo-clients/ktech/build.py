#!/usr/bin/env python3
"""ktec.my builder (template-first). facts.json + src/content.py + templates here -> static crawlable HTML.
python3 build.py              -> dist-preview/       (autoseo.my/preview/ktec/, noindex)
python3 build.py --live       -> dist-live/          (https://ktec.my/, index,follow)
python3 build.py --live-ktech -> dist-live-ktech/    (https://ktech.my/, index,follow)
Header, footer, dock, WhatsApp CTA, schema, hreflang, sitemap, robots, llms.txt rendered once here."""
import json, os, sys, shutil, html
from urllib.parse import quote
B=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(B,'src'))
from content import *
import articles as ART  # K Tech articles (13 Nov 2026): src/articles.py + data/articles/*.json
from products import PRODUCTS
F=json.load(open(os.path.join(B,'facts.json'),encoding='utf-8'))
LIVE_KTECH='--live-ktech' in sys.argv
LIVE='--live' in sys.argv or LIVE_KTECH
if LIVE_KTECH:
    M=F.get('live_ktech') or {'base_url':'https://ktech.my/','base_path':'/','noindex':False}
    OUT=os.path.join(B,'dist-live-ktech')
    # In-memory only: WhatsApp / enquiry copy should name the live domain.
    WA.update({k: v.replace('ktec.my','ktech.my') for k,v in WA.items()})
    for lang, block in CONTACT.items():
        block['lines']=[line.replace('ktec.my','ktech.my') for line in block['lines']]
else:
    M=F['live'] if LIVE else F['preview']
    OUT=os.path.join(B,'dist-live' if LIVE else 'dist-preview')
BASE_URL=M['base_url']; BASE=M['base_path']; NOINDEX=M['noindex']
CANON=BASE_URL if LIVE else 'https://ktec.my/'
A=BASE+'assets/'; V='?v=20261113p'
ARTS=ART.load(B); ART_KEYS=ART.register(globals(),ARTS)
E_=html.escape
WA_SVG='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z"/></svg>'
ICON={'ev':'<svg viewBox="0 0 48 48"><rect x="6" y="14" width="32" height="20"/><path d="M38 20h4v8h-4M20 17l-5 8h8l-5 8"/></svg>',
      'ac':'<svg viewBox="0 0 48 48"><path d="M24 4v40M7 14l34 20M7 34l34-20M19 6l5 5 5-5M19 42l5-5 5 5"/></svg>'}
def url(p,l): return BASE+LANG_META[l]['prefix']+SLUG[p]
def aurl(p,l): return BASE_URL+LANG_META[l]['prefix']+SLUG[p]
def curl_(p,l): return CANON+LANG_META[l]['prefix']+SLUG[p]
def wa(l,extra=''): return 'https://wa.me/'+F['whatsapp']+'?text='+quote(WA[l]+extra)
def wabtn(l,label=None,cls='btn btn-wa',ref='cta'):
    return f'<a class="{cls}" href="{wa(l)}" target="_blank" rel="noopener" data-ref="{ref}">{WA_SVG}<span>{E_(label or UI[l]["wa_quote"])}</span></a>'
def wa_num(num,l,extra=''):
    return 'https://wa.me/'+num+'?text='+quote(WA[l]+extra)
def purl(slug,l):
    return BASE+LANG_META[l]['prefix']+SLUG['tools']+slug+'/'
def pcurl(slug,l):
    return CANON+LANG_META[l]['prefix']+SLUG['tools']+slug+'/'
def prod_ctas(l, model, ref='product'):
    return f'<div class="pctas"><a class="btn btn-wa" href="{wa(l,model)}" target="_blank" rel="noopener" data-ref="{ref}">{WA_SVG}<span>{E_(UI[l]["wa_quote"])}</span></a></div>'
RELATED={
  'maxisys-ultra-s2':['maxisys-ms919-s2','maxisys-ms909-s2'],
  'maxisys-ms919-s2':['maxisys-ultra-s2','maxisys-ms909-s2'],
  'maxisys-ms909-s2':['maxisys-ultra-s2','maxisys-ms919-s2'],
  'maxisys-ms909ev':['ev-diagnostics-upgrade-kit'],
  'ev-diagnostics-upgrade-kit':['maxisys-ms909ev'],
  'maxisys-ms908s3':['maxicheck-mx900'],
  'maxisys-ms906pro':['maxicheck-mx900'],
  'maxicheck-mx900':['maxisys-ms906pro'],
}
BY_SLUG={pr['slug']:pr for pr in PRODUCTS}


def schema_org(l):
    offers=[{'@type':'Offer','itemOffered':{'@type':'Product','name':'Autel '+f[l][0],'brand':{'@type':'Brand','name':'Autel'},'category':f[l][0]}} for f in FAMILIES]
    return {'@context':'https://schema.org','@type':['Store','AutomotiveBusiness'],'@id':CANON+'#org','name':F['name'],'legalName':F['name'],
      'alternateName':'K Tech','identifier':F['company_no'],'url':CANON,'logo':CANON+'assets/ktech-logo.png','image':CANON+'assets/og.jpg',
      'telephone':'+'+F['call'],'email':F['email'],'slogan':F['bio'],'hasMap':F['maps'],'address':{'@type':'PostalAddress','streetAddress':F['street'],'postalCode':F['postcode'],'addressLocality':F['locality'],'addressRegion':F['region'],'addressCountry':F['country']},
      'contactPoint':[{'@type':'ContactPoint','contactType':'sales','telephone':'+'+F['whatsapp'],'contactOption':'WhatsApp','areaServed':['Johor Bahru','Masai','MY']},{'@type':'ContactPoint','contactType':'customer service','telephone':'+'+F['call'],'name':F['call_name'],'email':F['email'],'areaServed':'MY'},{'@type':'ContactPoint','contactType':'customer service','name':F['call2_name'],'telephone':'+'+F['call2'],'email':F['email'],'areaServed':'MY'}],
      'areaServed':[{'@type':'City','name':'Johor Bahru'},{'@type':'City','name':'Masai'},{'@type':'Country','name':'Malaysia'}],'brand':{'@type':'Brand','name':'Autel'},
      'sameAs':[F['facebook'],F['facebook2']],'knowsAbout':['Autel diagnostic tools','ADAS calibration','TPMS','key programming','EV diagnostics'],
      'subOrganization':{'@type':'Organization','name':'AutoSEO.my','url':F['autoseo']},
      'hasOfferCatalog':{'@type':'OfferCatalog','name':'Autel tools','itemListElement':offers}}
def faq_schema(l,items):
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}
def crumbs(p,l):
    it=[{'@type':'ListItem','position':1,'name':UI[l]['nav']['home'],'item':curl_('home',l)}]
    if p!='home': it.append({'@type':'ListItem','position':2,'name':UI[l]['nav'][p],'item':curl_(p,l)})
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':it}

def head(p,l,schemas, title=None, desc=None, canon=None, og_image=None, alternates=None):
    t=title if title is not None else TITLE[p][l]; d=desc if desc is not None else DESC[p][l]
    can=canon if canon is not None else curl_(p,l)
    ogimg=og_image or (CANON+'assets/og.jpg')
    if alternates is None:
        alternates={x: curl_(p,x) for x in LANGS}
    alt=''.join(f'<link rel="alternate" hreflang="{LANG_META[x]["html"]}" href="{alternates[x]}">' for x in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{alternates["en"]}">'
    zh='&family=Noto+Sans+SC:wght@400;600;700' if l=='zh' else ''
    js=''.join('<script type="application/ld+json">'+json.dumps(s,ensure_ascii=False)+'</script>' for s in schemas)
    return f'''<!doctype html><html lang="{LANG_META[l]['html']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E_(t)}</title><meta name="description" content="{E_(d)}"><meta name="robots" content="{'noindex,nofollow' if NOINDEX else 'index,follow,max-image-preview:large'}">
<link rel="canonical" href="{can}">{alt}
<meta property="og:type" content="website"><meta property="og:title" content="{E_(t)}"><meta property="og:description" content="{E_(d)}"><meta property="og:url" content="{can}"><meta property="og:image" content="{ogimg}"><meta property="og:locale" content="{LANG_META[l]['og']}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f3f4f0"><link rel="icon" type="image/png" href="{A}favicon.png"><link rel="apple-touch-icon" href="{A}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=Public+Sans:wght@400;600{zh}&display=swap">
<link rel="stylesheet" href="{A}k.css{V}">{js}</head><body>'''

def header(p,l, lang_href=None):
    nav=''.join(f'<a href="{url(x,l)}"{" aria-current=page" if x==p else ""}>{E_(UI[l]["nav"][x])}</a>' for x in PAGES[1:])
    mnav=''.join(f'<a href="{url(x,l)}">{E_(UI[l]["nav"][x])}</a>' for x in PAGES)
    href=lang_href or (lambda x: url(p,x))
    lang=''.join(f'<a href="{href(x)}" hreflang="{LANG_META[x]["html"]}" lang="{LANG_META[x]["html"]}"{" aria-current=true" if x==l else ""}>{LANG_META[x]["label"]}</a>' for x in LANGS)
    return f'''<header class="top"><div class="wrap"><a class="brand" href="{url('home',l)}" aria-label="K Tech Auto Solution"><img src="{A}ktech-logo.webp{V}" alt="K Tech Auto Solution logo" width="110" height="56" decoding="async"></a>
<nav class="tnav" aria-label="Main">{nav}</nav><div class="lang" aria-label="Language">{lang}</div>
<button class="menu-btn" aria-expanded="false" aria-controls="mnav" aria-label="{UI[l]['menu']}"><i></i><i></i><i></i></button></div><nav id="mnav" aria-label="Mobile">{mnav}</nav></header><main>'''

def footer(l):
    u=UI[l]; nav=''.join(f'<a href="{url(x,l)}">{E_(u["nav"][x])}</a>' for x in PAGES+['articles'])
    return f'''</main><footer class="foot"><div class="wrap"><div class="fg">
<div><img src="{A}ktech-logo-white.webp{V}" alt="K Tech Auto Solution" width="110" height="56" loading="lazy" decoding="async"><p>{E_(F['name'])}<br>{u['co']} {F['company_no']}<br><a href="{F['maps']}" target="_blank" rel="noopener">{E_(F['address_full'])}</a></p>
<p><a href="{wa(l)}" target="_blank" rel="noopener" data-ref="footer">WhatsApp {F['whatsapp_display']}</a><br><a href="tel:+{F['call']}" data-ref="footer-call">{E_(u['calln'].format(n=F['call_name']))} {F['call_display']}</a><br><a href="tel:+{F['call2']}" data-ref="footer-call2">{E_(u['calln'].format(n=F['call2_name']))} {F['call2_display']}</a><br>{u['email']}: <a href="mailto:{F['email']}">{F['email']}</a><br><a href="{F['facebook']}" target="_blank" rel="noopener">Facebook: {E_(F['facebook_label'])} →</a><br><a href="{F['facebook2']}" target="_blank" rel="noopener">Facebook: {E_(F['facebook2_label'])} →</a></p></div>
<nav aria-label="Footer">{nav}</nav>
<div><p>{E_(u['autoseo_foot'])}</p><a class="seo-l" href="{F['autoseo']}">AutoSEO.my — SEO websites for automotive workshops</a></div></div>
<p class="tm">{E_(u['tm'])}</p><p class="tm" style="border:0;margin:0;padding:0">© 2026 {E_(F['name'])}</p></div></footer>
<div class="dock">{wabtn(l,u['wa'],ref='dock')}</div><script src="{A}k.js{V}" defer></script></body></html>'''

def fam_card(f,l,tag='div'):
    n,s=f[l]
    pic=f'<img src="{A}{f["img"]}" alt="Autel {E_(n)} tool" width="560" height="420" loading="lazy" draggable="false">' if f['img'] else ICON[f['k']]
    md=f'<span class="md">{E_(f["models"])}</span>' if f['models'] else ''
    return f'<{tag} class="fam" id="{f["k"]}"><span class="code">{f["code"]}</span><div class="pic">{pic}</div><div class="tx"><h3>{E_(n)}</h3><p>{E_(s)}</p>{md}</div></{tag}>'

EVIMG=['ev-showroom-opening','ev-service-counter','ev-autel-kit','ev-car-boot-kit','ev-booth-demo','ev-expo-team','ev-display-counter','ev-training-audience']
def events(l,cls='sec alt',num='02'):
    u=UI[l]; it=''.join(f'<figure class="tshot"><img src="{A}{f}.webp" alt="{E_(c)}, K Tech" width="720" height="900" loading="lazy" draggable="false"><figcaption>{E_(c)}</figcaption></figure>' for f,c in zip(EVIMG,u['ev']))
    it+=f'<figure class="tshot"><img src="{A}ktec-team-workshop.webp" alt="{E_(u["team"])}" width="900" height="1125" loading="lazy" draggable="false"><figcaption>{E_(u["team"])}</figcaption></figure>'
    fb=f'<a href="{F["facebook"]}" target="_blank" rel="noopener">Facebook: {E_(F["facebook_label"])} →</a><br><a href="{F["facebook2"]}" target="_blank" rel="noopener">Facebook: {E_(F["facebook2_label"])} →</a>'
    return f'<section class="{cls}" id="events"><div class="wrap"><div class="sh"><div><span class="mono">{num}</span><h2>{E_(u["ev_h"])}</h2><p>{E_(u["ev_s"])}</p></div></div><div class="glide" data-speed="0.04">{it}</div><p class="fbl">{fb}</p></div></section>'
def faq_html(l,items):
    return '<div class="faq">'+''.join(f'<details><summary>{E_(q)}</summary><p>{E_(a)}</p></details>' for q,a in items)+'</div>'
def end_cta(l,h,p):
    return f'<section class="sec dark end"><div class="wrap"><h2>{E_(h)}</h2><p>{E_(p)}</p>{wabtn(l,ref="end")}</div></section>'

def page_home(l):
    h=HOME[l]; u=UI[l]
    sys_=''.join(f'<li><span>{E_(s)}</span><i>{E_(h["scan_ok"])}</i></li>' for s in h['scan_sys'])
    wave1='<svg viewBox="0 0 400 84" preserveAspectRatio="none"><polyline fill="none" stroke="#0f9fb3" stroke-width="2" points="'+' '.join(f'{x},{42+ (18 if (x//10)%4==1 else -14 if (x//10)%4==2 else 4)*(1 if x<200 else 1)}' for x in range(0,401,10))+'"/></svg>'
    wave2='<svg class="b" viewBox="0 0 400 84" preserveAspectRatio="none"><path fill="none" stroke="#f2a516" stroke-width="2" d="M0 60 Q25 22 50 60 T100 60 T150 60 T200 60 T250 60 T300 60 T350 60 T400 60"/></svg>'
    rail=''.join(f'<a class="fam" href="{url("tools",l)}#{f["k"]}"><span class="code">{f["code"]}</span><div class="pic">'+(f'<img src="{A}{f["img"]}" alt="Autel {E_(f[l][0])}" width="560" height="420" loading="lazy" draggable="false">' if f['img'] else ICON[f['k']])+f'</div><div class="tx"><h3>{E_(f[l][0])}</h3><p>{E_(f[l][1])}</p></div></a>' for f in FAMILIES)
    pic=['<svg viewBox="0 0 24 24"><path d="M4 12l5 5L20 6"/></svg>','<svg viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>','<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/></svg>']
    proof=f'<a href="{F["autel_wtb"]}" target="_blank" rel="noopener">{pic[0]}<span>{E_(h["proof"][0])} <u>{E_(u["listed"])}</u></span></a><div>{pic[1]}<span>{E_(h["proof"][1])}</span></div><div>{pic[2]}<span>{E_(h["proof"][2])}</span></div>'
    steps=''.join(f'<li><span class="n">0{i+1}</span><div><h3>{E_(a)}</h3><p>{E_(b)}</p></div></li>' for i,(a,b) in enumerate(h['steps']))
    body=f'''<section class="hero"><div class="wrap hgrid"><div>
<span class="badge mono"><b></b>{E_(u['badge'])}</span><h1>{h['h1']}</h1><p class="line">{E_(h['line'])}</p>
<div class="ctas">{wabtn(l,ref='hero')}<a class="lnk" href="{url('tools',l)}">{E_(u['see_range'])} →</a></div></div>
<div class="tabwrap"><div class="tab" aria-hidden="true"><div class="th"><span>{E_(h['scan_t'])}</span><span>● LIVE</span></div>
<div class="wave">{wave1}{wave2}<span class="rpm"><b>812</b><small>RPM</small></span></div><ul class="sys">{sys_}</ul><div class="bar"><b></b></div>
<div class="st" data-run="{E_(h['vin'])}" data-done="{E_(h['done'])}">{E_(h['vin'])}</div>
<div class="prod"><img src="{A}autel-diag.webp" alt="" width="560" height="420"><small>AUTEL® MAXISYS</small></div></div></div></div></section>
<section class="sec"><div class="wrap"><div class="sh"><div><span class="mono">01 · Autel®</span><h2>{E_(h['range_h'])}</h2><p>{E_(h['range_s'])}</p></div></div>
<div class="glide" data-speed="0.04">{rail}</div></div></section>
{events(l)}
<section class="sec"><div class="wrap"><div class="sh"><div><span class="mono">03</span><h2>{E_(h['proof_h'])}</h2></div></div><div class="proof">{proof}</div></div></section>
<section class="sec alt"><div class="wrap"><div class="sh"><div><span class="mono">04</span><h2>{E_(h['steps_h'])}</h2></div></div><ol class="steps">{steps}</ol></div></section>
<section class="sec"><div class="wrap"><div class="seo"><div><span class="mono" style="color:#7fdbe8">AutoSEO.my</span><h2>{E_(h['seo_h'])}</h2><p>{E_(h['seo_p'])}</p></div><a class="btn" href="{F['autoseo']}">{E_(h['seo_b'])} →</a></div></div></section>
<section class="sec"><div class="wrap"><div class="sh"><div><span class="mono">05</span><h2>{E_(u['faq'])}</h2></div></div>{faq_html(l,FAQ[l])}</div></section>
{end_cta(l,h['cta_h'],h['cta_p'])}'''
    return head('home',l,[schema_org(l),faq_schema(l,FAQ[l])])+header('home',l)+body+footer(l)

def ph(p,l,h1,intro):
    u=UI[l]; return f'<section class="ph"><div class="wrap"><div class="crumb"><a href="{url("home",l)}">{E_(u["nav"]["home"])}</a> / {E_(u["nav"][p])}</div><h1>{E_(h1)}</h1><p>{E_(intro)}</p>{wabtn(l,ref="top")}</div></section>'

def product_schema(pr,l):
    c=pr[l]
    return {'@context':'https://schema.org','@type':'Product','name':c['name'],'description':c['intro'],
            'brand':{'@type':'Brand','name':'Autel'},'image':CANON+'assets/'+pr['img'],'url':pcurl(pr['slug'],l),
            'category':'Automotive diagnostic tool','manufacturer':{'@type':'Organization','name':'Autel'}}

def product_crumbs(pr,l):
    c=pr[l]
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':UI[l]['nav']['home'],'item':curl_('home',l)},
        {'@type':'ListItem','position':2,'name':UI[l]['nav']['tools'],'item':curl_('tools',l)},
        {'@type':'ListItem','position':3,'name':c['name'],'item':pcurl(pr['slug'],l)}]}

def product_block(pr,l, link=True, heading='h2'):
    c=pr[l]; u=UI[l]
    w,h=pr.get('wh',(1200,700))
    feats=''.join(f'<li>{E_(x)}</li>' for x in (c['features'] if not link else c['features'][:5]))
    specs=''
    if not link and c.get('specs'):
        specs=f'<h3>{E_(u["prod_spec"])}</h3><dl class="pspec">'+''.join(f'<div><dt>{E_(k)}</dt><dd>{E_(v)}</dd></div>' for k,v in c['specs'])+'</dl>'
    note=f'<p class="pnote">{E_(c["note"])}</p>' if c.get('note') and not link else ''
    cov=f'<p class="pcov"><b>{E_(u["prod_cov"])}.</b> {E_(c["coverage"])}</p>' if c.get('coverage') and not link else ''
    more=f'<p class="pmore"><a href="{purl(pr["slug"],l)}">{E_(u["prod_more"])} →</a></p>' if link else ''
    rel=''
    if not link:
        slugs=RELATED.get(pr['slug'],[])
        if slugs:
            rel='<div class="prel">'+''.join(f'<a href="{purl(s,l)}">{E_(BY_SLUG[s][l]["name"])}</a>' for s in slugs if s in BY_SLUG)+'</div>'
    hid=pr['slug']
    img=pr['img']
    sku=pr['sku']
    parts=[]
    parts.append(f'<article class="psec" id="{hid}">')
    parts.append(f'<div class="phero"><img src="{A}{img}" alt="{E_(c["alt"])}" width="{w}" height="{h}" loading="lazy"></div>')
    parts.append('<div class="ptx"><span class="mono">'+E_(sku)+'</span>')
    parts.append(f'<{heading}>{E_(c["name"])}</{heading}>')
    parts.append(f'<p class="ptag">{E_(c["tag"])}</p>')
    parts.append(f'<p>{E_(c["intro"])}</p>')
    parts.append(f'<h3>{E_(u["prod_feat"])}</h3><ul class="pfeats">{feats}</ul>')
    parts.append(f'<h3>{E_(u["prod_use"])}</h3><p>{E_(c["use"])}</p>')
    parts.append(specs+cov+note)
    parts.append(prod_ctas(l, c['name'], ref=hid))
    parts.append(more+rel+'</div></article>')
    return ''.join(parts)

def page_product(pr,l):
    c=pr[l]; u=UI[l]
    crumb=f'<div class="pcrumb"><a href="{url("home",l)}">{E_(u["nav"]["home"])}</a> / <a href="{url("tools",l)}">{E_(u["nav"]["tools"])}</a> / {E_(c["name"])}</div>'
    body=(f'<section class="ph"><div class="wrap">{crumb}<p class="mono" style="margin:0 0 8px">{E_(u["badge"])}</p></div></section>'
          f'<section class="sec"><div class="wrap">{product_block(pr,l,link=False,heading="h1")}'
          f'<p class="pmore" style="margin-top:18px"><a href="{url("tools",l)}">← {E_(u["prod_back"])}</a></p>'
          f'<p class="pnote">{E_(u["prod_src"])}</p></div></section>'
          +end_cta(l,HOME[l]['cta_h'],HOME[l]['cta_p']))
    alts={x: pcurl(pr['slug'],x) for x in LANGS}
    return head('tools',l,[schema_org(l),product_schema(pr,l),product_crumbs(pr,l)],
                title=c['title'], desc=c['desc'], canon=pcurl(pr['slug'],l),
                og_image=CANON+'assets/'+pr['img'], alternates=alts)+header('tools',l, lang_href=lambda x, slug=pr['slug']: purl(slug,x))+body+footer(l)


def page_tools(l):
    t=TOOLS[l]; fq=FAQ[l][:4]; u=UI[l]
    items={'@context':'https://schema.org','@type':'ItemList','name':t['h1'],'itemListElement':[{'@type':'ListItem','position':i+1,'item':product_schema(pr,l)} for i,pr in enumerate(PRODUCTS)]}
    newbox=f'<div class="newbox"><span class="mono">MS909S2</span><h2>{E_(u["new_t"])}</h2><p>{E_(u["new_p"])}</p><p class="pmore" style="margin-top:10px"><a href="{purl("maxisys-ms909-s2",l)}">{E_(u["prod_more"])} →</a></p></div>'
    fams='<div class="flist">'+''.join(fam_card(f,l,'article') for f in FAMILIES)+'</div>'
    models=('<section class="sec alt" id="models"><div class="wrap"><div class="sh"><div><span class="mono">Autel</span><h2>'
            +E_(u['prod_all'])+'</h2><p>'+E_(u['prod_src'])+'</p></div></div>'
            +''.join(product_block(pr,l,link=True) for pr in PRODUCTS)+'</div></section>')
    body=ph('tools',l,t['h1'],t['intro'])+f'<section class="sec"><div class="wrap">{newbox}{fams}</div></section>'+models+f'<section class="sec"><div class="wrap"><div class="sh"><div><h2>{E_(u["faq"])}</h2></div></div>{faq_html(l,fq)}</div></section>'+end_cta(l,HOME[l]['cta_h'],HOME[l]['cta_p'])
    return head('tools',l,[schema_org(l),items,faq_schema(l,fq),crumbs('tools',l)])+header('tools',l)+body+footer(l)

def page_services(l):
    s=SERVICES[l]; arts=''
    for code,n,p,link,lt in s['items']:
        a=f' <a href="{F[link]}"{" target=_blank rel=noopener" if link!="autoseo" else ""}>{lt} →</a>' if link else ''
        arts+=f'<article{" class=hl" if link=="autoseo" else ""}><span class="n">{code}</span><div><h2>{E_(n)}</h2><p>{E_(p)}{a}</p></div></article>'
    svc=[{'@context':'https://schema.org','@type':'Service','name':n,'description':p,'provider':{'@id':CANON+'#org'},'areaServed':'Malaysia',**({'url':F['autoseo']} if link=='autoseo' else {})} for _,n,p,link,_ in s['items']]
    u=UI[l]; tr=''.join(f'<figure class="tshot"><img src="{A}ktec-training-{i}.webp" alt="{E_(u['train'])} {i}, K Tech Johor Bahru" width="720" height="900" loading="lazy" draggable="false"><figcaption>{E_(u['train'])}</figcaption></figure>' for i in range(1,6))
    train=f'<section class="sec alt" id="training"><div class="wrap"><div class="sh"><div><span class="mono">S5</span><h2>{E_(u["train_h"])}</h2><p>{E_(u["train_s"])}</p></div></div><div class="glide" data-speed="0.04">{tr}</div><p class="fbl"><a href="{F["facebook"]}" target="_blank" rel="noopener">Facebook: {E_(F["facebook_label"])} →</a><br><a href="{F["facebook2"]}" target="_blank" rel="noopener">Facebook: {E_(F["facebook2_label"])} →</a></p></div></section>'
    body=ph('services',l,s['h1'],s['intro'])+f'<section class="sec"><div class="wrap"><div class="svc">{arts}</div><p class="recent"><b>{E_(u["recent"])}</b> {E_(u["recent_t"])}</p></div></section>'+train+end_cta(l,HOME[l]['cta_h'],HOME[l]['cta_p'])
    return head('services',l,[schema_org(l),*svc,crumbs('services',l)])+header('services',l)+body+footer(l)

def page_about(l):
    a=ABOUT[l]; rows=''.join(f'<tr><th>{E_(k)}</th><td>{E_(v)}</td></tr>' for k,v in a['rows'])+f'<tr><th>{E_(UI[l]["call"])}</th><td><a href="tel:+{F["call"]}">{E_(UI[l]["calln"].format(n=F["call_name"]))} {F["call_display"]}</a><br><a href="tel:+{F["call2"]}">{E_(UI[l]["calln"].format(n=F["call2_name"]))} {F["call2_display"]}</a></td></tr><tr><th>{E_(UI[l]["email"])}</th><td><a href="mailto:{F["email"]}">{F["email"]}</a></td></tr>'
    rows=rows.replace('AutoSEO.my</td>',f'<a href="{F["autoseo"]}">AutoSEO.my</a></td>',1).replace('81100 Johor Bahru, Johor</td>','81100 Johor Bahru, Johor · <a href="'+F['maps']+'" target="_blank" rel="noopener">Google Maps →</a></td>')
    body=ph('about',l,a['h1'],a['p'])+f'<section class="sec"><div class="wrap"><div class="about-g"><figure class="real1"><img src="{A}ktec-team-workshop.webp" alt="{E_(UI[l]['team'])}" width="900" height="1125" loading="lazy"><figcaption>{E_(UI[l]['team'])}</figcaption></figure><table class="spec">{rows}</table></div><p style="margin-top:16px"><a href="{F["autel_wtb"]}" target="_blank" rel="noopener">{E_(UI[l]["listed"])} →</a> <br><a href="{F["facebook"]}" target="_blank" rel="noopener">Facebook: {E_(F["facebook_label"])} →</a><br><a href="{F["facebook2"]}" target="_blank" rel="noopener">Facebook: {E_(F["facebook2_label"])} →</a></p></div></section>'+events(l,num='K')+end_cta(l,HOME[l]['cta_h'],HOME[l]['cta_p'])
    return head('about',l,[schema_org(l),crumbs('about',l)])+header('about',l)+body+footer(l)

def page_contact(l):
    c=CONTACT[l]
    body=ph('contact',l,c['h1'],c['p'])+f'''<section class="sec"><div class="wrap cgrid"><div class="cbox"><span class="mono">WhatsApp</span><a class="big" href="{wa(l)}" target="_blank" rel="noopener" data-ref="contact-number">{F['whatsapp_display']}</a>{wabtn(l,ref='contact')}<p class="mono" style="margin:12px 0 0">{E_(UI[l]['areas'])}</p>
<div class="cact"><a class="btn btn-ghost" href="tel:+{F['call']}" data-ref="contact-call">{E_(UI[l]['calln'].format(n=F['call_name']))} {F['call_display']}</a><a class="btn btn-ghost" href="tel:+{F['call2']}" data-ref="contact-call2">{E_(UI[l]['calln'].format(n=F['call2_name']))} {F['call2_display']}</a><a class="btn btn-ghost" href="mailto:{F['email']}">{F['email']}</a></div>
<p style="margin-top:16px"><span class="mono">{UI[l]['addr']}</span><br>{E_(F['address_full'])}<br><a href="{F['maps']}" target="_blank" rel="noopener">{UI[l]['map']} →</a><br><a href="{F['facebook']}" target="_blank" rel="noopener">Facebook: {E_(F['facebook_label'])} →</a><br><a href="{F['facebook2']}" target="_blank" rel="noopener">Facebook: {E_(F['facebook2_label'])} →</a></p></div>
<form class="cbox" id="enquiry" data-wa="{F['whatsapp']}" data-lines='{E_(json.dumps(c["lines"],ensure_ascii=False))}'><span class="mono">{E_(c['form_h'])}</span>
<label for="need">{E_(c['f_need'])}</label><input id="need" name="need" autocomplete="off"><label for="name">{E_(c['f_name'])}</label><input id="name" name="name" autocomplete="name"><label for="shop">{E_(c['f_shop'])}</label><input id="shop" name="shop" autocomplete="organization">
<button class="btn btn-wa" type="submit">{WA_SVG}<span>{E_(c['f_send'])}</span></button></form></div></section>'''
    return head('contact',l,[schema_org(l),crumbs('contact',l)])+header('contact',l)+body+footer(l)

R={'home':page_home,'tools':page_tools,'services':page_services,'about':page_about,'contact':page_contact}
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT+'/assets')
for f in os.listdir(B+'/src/img'): shutil.copy(B+'/src/img/'+f,OUT+'/assets/'+f)
shutil.copy(B+'/src/k.css',OUT+'/assets/'); shutil.copy(B+'/src/k.js',OUT+'/assets/')
if LIVE_KTECH:
    _css=os.path.join(OUT,'assets','k.css')
    open(_css,'w',encoding='utf-8').write(open(B+'/src/k.css',encoding='utf-8').read().replace('ktec.my','ktech.my'))
for l in LANGS:
    for p in PAGES:
        d=os.path.join(OUT,LANG_META[l]['prefix']+SLUG[p]); os.makedirs(d,exist_ok=True)
        open(d+'index.html','w',encoding='utf-8').write(R[p](l))
    for pr in PRODUCTS:
        d=os.path.join(OUT,LANG_META[l]['prefix']+SLUG['tools']+pr['slug']); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(page_product(pr,l))
ART.build(globals(),ARTS)
# sitemap/robots/llms
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for p in PAGES+ART_KEYS:
    for l in LANGS:
        alts=''.join(f'<xhtml:link rel="alternate" hreflang="{LANG_META[x]["html"]}" href="{curl_(p,x)}"/>' for x in LANGS)
        lm=next((x['updated'] for x in ARTS if 'art:'+x['slug']==p),F['updated'])
        sm+=f'<url><loc>{curl_(p,l)}</loc><lastmod>{lm}</lastmod>{alts}</url>\n'
for pr in PRODUCTS:
    for l in LANGS:
        alts=''.join(f'<xhtml:link rel="alternate" hreflang="{LANG_META[x]["html"]}" href="{pcurl(pr["slug"],x)}"/>' for x in LANGS)
        sm+=f'<url><loc>{pcurl(pr["slug"],l)}</loc><lastmod>{F["updated"]}</lastmod>{alts}</url>\n'
open(OUT+'/sitemap.xml','w').write(sm+'</urlset>\n')
open(OUT+'/robots.txt','w').write(('User-agent: *\nDisallow: /\n' if NOINDEX else 'User-agent: *\nAllow: /\n\nSitemap: '+CANON+'sitemap.xml\n'))
open(OUT+'/llms.txt','w',encoding='utf-8').write(f"# {F['name']}\n> Authorised Autel dealer in Johor Bahru, Malaysia (listed on autel.com Where to Buy, Malaysia). Company No. {F['company_no']}. WhatsApp +{F['whatsapp']}. Call {F['call_name']} +{F['call']} or {F['call2_name']} +{F['call2']}. Facebook: {F['facebook']} and {F['facebook2']}. Email {F['email']}. Address: {F['address_full']}. Runs technical training sessions for workshop technicians.\n\n## Pages\n"+''.join(f"- [{UI['en']['nav'][p]}]({curl_(p,'en')})\n" for p in PAGES)+''.join(f"- [{pr['en']['name']}]({pcurl(pr['slug'],'en')})\n" for pr in PRODUCTS)+("\n## Articles\n"+''.join(f"- [{a['en']['h1']}]({curl_('art:'+a['slug'],'en')}): {a['en']['description']}\n" for a in ARTS) if ARTS else '')+f"\n## Related\n- [AutoSEO.my]({F['autoseo']}): SEO websites for automotive businesses, a brand of K Tech Auto Solution Sdn Bhd\n")
open(OUT+'/404.html','w',encoding='utf-8').write(head('home','en',[]).replace(TITLE['home']['en'],'Page not found | K Tech')+header('home','en')+f'<section class="ph"><div class="wrap"><h1>Page not found</h1><p><a href="{url("home","en")}">Home →</a></p></div></section>'+footer('en'))
# pre-upload ban check
bad=['Page One','pageonesingapore','TODO','lorem','XXXX','★','rating']
for root,_,fs in os.walk(OUT):
    for fn in fs:
        if fn.endswith(('.html','.txt','.xml')):
            t=open(os.path.join(root,fn),encoding='utf-8').read()
            for b in bad:
                if b in t: sys.exit(f'BANNED "{b}" in {root}/{fn}')
print('built',OUT)

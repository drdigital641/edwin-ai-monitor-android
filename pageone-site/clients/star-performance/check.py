import os,re,json,glob,html
root='site'; bad=0; pages=glob.glob(root+'/**/index.html',recursive=True)
for f in sorted(pages):
    s=open(f).read(); d=os.path.dirname(f)
    for m in re.finditer(r'(?:href|src)="([^"]+)"',s):
        u=m.group(1)
        if u.startswith(('http','mailto:','#','data:')): continue
        u=u.split('#')[0].split('?')[0]
        p=os.path.normpath(os.path.join(d,u))
        if os.path.isdir(p): p=os.path.join(p,'index.html')
        if not os.path.exists(p): print('BROKEN',f,u); bad+=1
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: j=json.loads(b.replace('<\\/','</'))
        except Exception as e: print('BADJSON',f,e); bad+=1
        else:
            vis=len(re.findall(r'<details><summary>',s)); faq=sum(len(x['mainEntity']) for x in j['@graph'] if x.get('@type')=='FAQPage')
            if vis!=faq: print('FAQMISMATCH',f,vis,faq); bad+=1
    t=re.search(r'<title>(.*?)</title>',s).group(1); dsc=re.search(r'name="description" content="(.*?)"',s).group(1)
    words=len(re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',s)).split())
    flag=('TITLE>60 ' if len(html.unescape(t))>60 else '')+('DESC>160 ' if len(html.unescape(dsc))>160 else '')
    if s.count('<h1')!=1: flag+='H1x%d '%s.count('<h1')
    if '%%' in s or '%s' in s: flag+='FMT '
    print('%5d words %3d/%3d %s %s'%(words,len(html.unescape(t)),len(html.unescape(dsc)),flag,f))
print('pages',len(pages),'problems',bad); print(open('site/sitemap.xml').read().count('<url>'),'sitemap urls')

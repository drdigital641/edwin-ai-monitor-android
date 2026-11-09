import os,re,json,glob,xml.dom.minidom as md
from html.parser import HTMLParser
import os
S=os.environ.get('JB_OUT') or 'site'
BASE='https://pageonesingapore.com/preview/jb-staycation/'
bad=0
files=[f for f in glob.glob(S+'/**/*.html',recursive=True)]
for f in files:
    h=open(f).read()
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try: json.loads(m)
        except Exception as ex: print('BAD JSON',f,ex);bad+=1
    t=re.search(r'<title>(.*?)</title>',h).group(1); d=re.search(r'name="description" content="(.*?)"',h)
    if len(t)>60 or (d and len(d.group(1))>160): print('LEN',f,len(t),len(d.group(1)) if d else 0)
    if f!=S+'/404.html':
        if h.count('<h1')!=1: print('H1',f)
    for tag in re.findall(r'<img [^>]*>',h):
        if not all(a in tag for a in (' width="',' height="',' alt="')): print('IMG ATTR',f,tag[:120]);bad+=1
    for ss in re.findall(r'srcset="([^"]+)"',h):
        for part in ss.split(','):
            u=part.strip().split(' ')[0]
            if u.startswith('http'): continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f),u.split("?")[0]))): print('MISSING srcset',f,u);bad+=1
    if 'jbstaycation.com/_astro' in h: print('HOTLINK',f);bad+=1
    for href in re.findall(r'(?:href|src)="([^"#]+)"',h):
        href=href.split('?')[0]  # ignore cache-buster query strings
        if href.startswith(('http','mailto','tel','data')): 
            if href.startswith(BASE):
                p=href[len(BASE):]
                tgt=os.path.join(S,p); 
                if p.endswith('/') or p=='': tgt=os.path.join(tgt,'index.html')
                if not os.path.exists(tgt): print('MISSING abs',f,href);bad+=1
            continue
        tgt=os.path.normpath(os.path.join(S,href.lstrip('/')) if href.startswith('/') else os.path.join(os.path.dirname(f),href))
        if os.path.isdir(tgt): tgt=os.path.join(tgt,'index.html')
        if not os.path.exists(tgt): print('MISSING',f,href);bad+=1
md.parse(S+'/sitemap.xml')
print('files',len(files),'bad',bad)

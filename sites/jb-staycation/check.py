import os,re,json,glob,xml.dom.minidom as md
from html.parser import HTMLParser
S='site'
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
    for href in re.findall(r'(?:href|src)="([^"#]+)"',h):
        if href.startswith(('http','mailto','tel','data')): 
            if href.startswith(BASE):
                p=href[len(BASE):]
                tgt=os.path.join(S,p); 
                if p.endswith('/') or p=='': tgt=os.path.join(tgt,'index.html')
                if not os.path.exists(tgt): print('MISSING abs',f,href);bad+=1
            continue
        tgt=os.path.normpath(os.path.join(os.path.dirname(f),href))
        if os.path.isdir(tgt): tgt=os.path.join(tgt,'index.html')
        if not os.path.exists(tgt): print('MISSING',f,href);bad+=1
md.parse(S+'/sitemap.xml')
print('files',len(files),'bad',bad)

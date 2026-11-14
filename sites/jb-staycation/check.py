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
# Link preview tags (14 Nov 2026): og:image + secure_url + type + 1200x630 + twitter card/image, JPG on this site, 1200x630 under 300KB, inside the first 32KB
from urllib.parse import urlparse
for f in files:
    h=open(f,encoding='utf-8').read()
    if 'og:title' not in h: continue   # 404 and the review helper carry no preview tags
    m=re.search(r'<meta property="og:image" content="([^"]+)"><meta property="og:image:secure_url" content="([^"]+)"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',h)
    if not m or m.group(1)!=m.group(2) or not m.group(1).endswith('.jpg'): print('OG TAGS',f);bad+=1;continue
    if not re.search(r'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%s">'%re.escape(m.group(1)),h): print('TWITTER TAGS',f);bad+=1
    if h.find('name="twitter:image"')>32000: print('OG BEYOND 32KB',f);bad+=1
    ip=os.path.join(S,urlparse(m.group(1)).path.lstrip('/').replace('preview/jb-staycation/',''))
    try:
        from PIL import Image
        if Image.open(ip).size!=(1200,630) or os.path.getsize(ip)>=300*1024: print('OG IMAGE SIZE',f,ip);bad+=1
    except Exception as ex: print('OG IMAGE MISSING',f,ip);bad+=1
md.parse(S+'/sitemap.xml')
print('files',len(files),'bad',bad)

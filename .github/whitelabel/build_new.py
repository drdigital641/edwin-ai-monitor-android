# White-label footer round (Edwin 10 Nov 2026): crawl each live site (sitemap + internal links),
# keep the original bytes of every page carrying the Page One footer credit, and write a copy with
# only the credit (and its separator) removed. Output: whitelabel/20261110/<slug>/{orig,new}/<path>.
import re, sys, os, hashlib, urllib.request, urllib.parse, concurrent.futures as cf, collections, random, json
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
OUT='whitelabel/20261110'
A='<a href="https://pageonesingapore.com/">Page One Singapore</a>'
AQ=re.escape(A)
RULES=[ # (name, regex, replacement), applied in order
 ('span-credit', r'<span>(?:Website &amp; SEO by|Website by|Laman web &amp; SEO oleh|网站与 SEO：|网站制作) ?'+AQ+r'</span>', ''),
 ('dot-credit', r' · (?:Website &amp; SEO by|网站与 SEO 由) ?'+AQ, ''),
 ('autotex-home', r'Website &amp; SEO by '+AQ+r' · ', ''),
 ('p-credit', r'\s*<p>Website &amp; SEO by '+AQ+r'</p>', ''),
 ('rc-credit', r' Website &amp; SEO by '+AQ+r'\.(?=</p>)', ''),
 ('xado-mid', r'Website &amp; SEO by '+AQ+r'\. ', ''),
 ('xado-end', r' Website &amp; SEO by '+AQ+r'(?=</div>)', ''),
 ('anchor-credit', r'<a href="https://pageonesingapore.com/">Website &amp; SEO by Page One Singapore</a>', ''),
 ('jb-credit', r' <a href="https://pageonesingapore.com/" rel="noopener">Website by Page One Singapore</a>', ''),
]
def get(u, t=30):
    for i in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=t)
            return r.status, r.read(), r.geturl(), r.headers.get('Content-Type','')
        except urllib.error.HTTPError as e: return e.code,b'',u,''
        except Exception: pass
    return 0,b'',u,''
def path_of(base,u):
    p=urllib.parse.urlparse(u).path
    p=urllib.parse.unquote(p).lstrip('/')
    if p=='' or p.endswith('/'): p+='index.html'
    return p
def crawl(base, only_home=False):
    seen=set(); pages={}
    todo=[base+'/', base+'/404.html']
    if not only_home:
        sm=[base+'/sitemap.xml']; sms=set()
        while sm:
            s=sm.pop()
            if s in sms: continue
            sms.add(s); c,b,_,_=get(s); b=b.decode('utf-8','replace')
            locs=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',b)
            if '<sitemapindex' in b: sm+=locs
            else: todo+=locs
    host=urllib.parse.urlparse(base).netloc
    def fetch(u):
        c,b,final,ct=get(u+'?nc=%d'%random.randint(1,10**9))
        return u,c,b,final,ct
    while todo:
        batch=[]
        for u in todo:
            u=u.split('#')[0].split('?')[0]
            pu=urllib.parse.urlparse(u)
            if pu.netloc.replace('www.','')!=host.replace('www.',''): continue
            u=base+pu.path
            if u in seen: continue
            if re.search(r'\.(css|js|png|jpe?g|webp|gif|svg|ico|pdf|xml|txt|json|webmanifest|woff2?|mp4|avif)$',pu.path,re.I): continue
            seen.add(u); batch.append(u)
        todo=[]
        with cf.ThreadPoolExecutor(10) as ex:
            for u,c,b,final,ct in ex.map(fetch,batch):
                if c!=200 or 'html' not in ct: continue
                if final.split('?')[0].rstrip('/')!=u.rstrip('/') and not u.endswith('404.html'): continue
                pages[u]=b
                if only_home: continue
                for h in re.findall(rb'href="([^"#]+)"',b):
                    h=h.decode('utf-8','replace')
                    if h.startswith(('mailto:','tel:','javascript:','https://wa.me')): continue
                    todo.append(urllib.parse.urljoin(u,h))
    return pages
summary={}
for line in open('.github/whitelabel/sites.txt'):
    slug,dom=line.split()
    if slug=='danny': continue   # rendered by the Base44 publisher; fixed at its source
    c,b,final,_=get('https://'+dom+'/')
    base=re.match(r'https?://[^/]+',final).group(0)
    pages=crawl(base, only_home=False)
    st=collections.Counter(); left=[]
    for u,b in pages.items():
        txt=b.decode('utf-8')
        if 'pageonesingapore.com/"' not in txt: continue
        new=txt; used=[]
        for name,rx,rep in RULES:
            new2,n=re.subn(rx,rep,new)
            if n: used.append(f'{name}x{n}'); new=new2
        if new==txt: left.append(u); continue
        rest=[m for m in re.findall(r'.{0,80}href="https://pageonesingapore\.com/?".{0,60}',new)]
        if rest: left.append(u+' STILL '+rest[0][:160])
        p=path_of(base,u)
        for kind,data in (('orig',b),('new',new.encode('utf-8'))):
            fp=os.path.join(OUT,slug,kind,p); os.makedirs(os.path.dirname(fp),exist_ok=True)
            open(fp,'wb').write(data)
        st['changed']+=1; st[' '.join(used)]+=1
    st['crawled']=len(pages)
    summary[slug]=dict(st)
    print(f'=== {slug} {base} crawled={len(pages)} changed={st["changed"]}')
    for k,v in st.items():
        if k not in ('changed','crawled'): print(f'   rules {k}: {v}')
    for x in left[:8]: print('   LEFT',x)
json.dump(summary,open(OUT+'/summary.json','w'),indent=1)

# White-label footer inventory (10 Nov 2026). Crawls each site's sitemap + home, finds the Page One credit.
import re, sys, json, urllib.request, concurrent.futures as cf, collections, random
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def get(u, t=25):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=t)
        return r.status, r.read().decode('utf-8','replace'), r.geturl()
    except urllib.error.HTTPError as e: return e.code,'',u
    except Exception as e: return 0,str(e)[:80],u
def sitemap_urls(base):
    out=[]; seen=set(); todo=[base+'/sitemap.xml']
    while todo:
        s=todo.pop()
        if s in seen: continue
        seen.add(s); c,b,_=get(s)
        locs=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',b)
        if '<sitemapindex' in b: todo+=locs
        else: out+=locs
    return out
CRE=re.compile(r'.{0,160}(?:pageonesingapore|Page One Singapore|Page One).{0,120}',re.S|re.I)
res={}
for line in open('.github/whitelabel/sites.txt'):
    slug,dom=line.split()
    c,b,final=get('https://'+dom+'/')
    base=re.match(r'https?://[^/]+',final).group(0) if final else 'https://'+dom
    urls=sitemap_urls(base); urls=list(dict.fromkeys([base+'/']+urls))
    def chk(u):
        c,b,_=get(u+('&' if '?' in u else '?')+'nc=%d'%random.randint(1,10**9))
        snips=[re.sub(r'\s+',' ',m.group(0)) for m in CRE.finditer(b)]
        foot=[s for s in snips if re.search(r'by\s*<a[^>]*pageonesingapore|by Page One|Website',s,re.I)]
        ld=[s for s in snips if re.search(r'"(creator|author|publisher|provider)"',s)]
        return u,c,len(b),foot,ld,snips
    stats=collections.Counter(); variants=collections.Counter(); ldv=collections.Counter(); other=collections.Counter(); bad=[]
    with cf.ThreadPoolExecutor(8) as ex:
        for u,c,n,foot,ld,snips in ex.map(chk,urls):
            stats['pages']+=1
            if c!=200: bad.append((u,c)); continue
            if foot: stats['with_credit']+=1
            for s in foot: variants[s]+=1
            for s in ld: ldv[s]+=1
            for s in snips:
                if s not in foot and s not in ld: other[s]+=1
    print(f'=== {slug} {base} home={c} pages={stats["pages"]} credit_pages={stats["with_credit"]} non200={len(bad)}')
    for u,cc in bad[:5]: print('  NON200',cc,u)
    for s,n in variants.most_common(6): print(f'  CREDIT x{n}: {s}')
    for s,n in ldv.most_common(4): print(f'  SCHEMA x{n}: {s[:260]}')
    for s,n in other.most_common(4): print(f'  OTHER x{n}: {s[:260]}')
    for f in ('llms.txt','llms-full.txt'):
        cc,bb,_=get(base+'/'+f)
        for m in CRE.finditer(bb): print(f'  {f}: {re.sub(r"\s+"," ",m.group(0))[:220]}')

import os,re,sys,json,glob
D=sys.argv[1]; bad=[]
F=json.load(open('/tmp/sga/src/facts.json'))
pages=sorted(glob.glob(D+'/**/index.html',recursive=True))
titles={};descs={}
for p in pages:
    s=open(p).read(); rel=p[len(D)+1:]
    vis=re.sub(r'<script type="application/ld\+json">.*?</script>','',s,flags=re.S)
    noq=re.sub(r'<blockquote class="rq">.*?</blockquote>','',vis,flags=re.S)
    text=re.sub(r'<[^>]+>',' ',noq)
    for pat in [r'lorem',r'TODO',r'placeholder',r'S\$50\b',r'from \$50',r'thousands',r'No\.1',r'best detailer',r'guarantee',r'Colin',r'5 Yishun',r'#04-09',r'Criterion',r'767998',r'990 reviews']:
        if re.search(pat,s if pat in('lorem','TODO','placeholder','Colin','aggregateRating') else text,re.I): bad.append((rel,pat))
    if 'aggregateRating' in s: bad.append((rel,'aggregateRating'))
    if not F['flags']['claims_verified'] and re.search(r'Official Sonax Partner|Authori[sz]ed',s,re.I): bad.append((rel,'claim'))
    if not F['flags']['show_owner_name'] and re.search(r'\bZac\b',text): bad.append((rel,'Zac outside quote'))
    for n in re.findall(r'wa\.me/(\d+)',s):
        if n!='6583667010': bad.append((rel,'wa '+n))
    if s.count('<h1')!=1: bad.append((rel,'h1=%d'%s.count('<h1')))
    for need in ['name="robots" content="noindex, nofollow"','p1-cta.js?v=','rel="canonical"','og:image:width','data-cta="booking"']:
        if need not in s: bad.append((rel,'missing '+need))
    t=re.search(r'<title>(.*?)</title>',s).group(1); d=re.search(r'name="description" content="(.*?)"',s).group(1)
    if len(t)>60: bad.append((rel,'title>60'))
    titles.setdefault(t,[]).append(rel); descs.setdefault(d,[]).append(rel)
    if 'openingHours' in s or 'streetAddress' in s or 'postalCode' in s: bad.append((rel,'schema field'))
    for a in re.findall(r'<a [^>]*>',s):
        if re.search(r'wa\.me|tel:|facebook\.com|instagram\.com|tiktok\.com|carousell|search\.google',a) and ('data-cta' not in a or 'data-ref' not in a): bad.append((rel,'untracked '+a[:80]))
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S): json.loads(m.replace('<\\/','</'))
dup=[k for k,v in titles.items() if len(v)>1]+[k for k,v in descs.items() if len(v)>1]
print('pages',len(pages),'problems',len(bad),'dup titles/desc',len(dup))
for b in bad[:30]: print(b)
for k in dup[:5]: print('DUP',k)

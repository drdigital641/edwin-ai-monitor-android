import os,re,json,glob,html
B="site";bad=0
for f in sorted(glob.glob(B+"/**/*.html",recursive=True)):
    t=open(f).read();p=f[len(B):]
    title=re.search(r"<title>(.*?)</title>",t).group(1);desc=re.search(r'name="description" content="(.*?)"',t).group(1)
    h1=len(re.findall(r"<h1",t))
    lds=re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)
    faqs=0
    for l in lds:
        g=json.loads(l)["@graph"]
        for n in g:
            if n["@type"]=="FAQPage": faqs+=len(n["mainEntity"])
    vis=len(re.findall(r"<details>",t))
    body=re.sub(r"<script.*?</script>|<style.*?</style>","",t,flags=re.S);words=len(re.sub(r"<[^>]+>"," ",body.split("<main>")[1].split("</main>")[0]).split())
    probs=[]
    if len(html.unescape(title))>60: probs.append(f"title {len(html.unescape(title))}")
    if len(html.unescape(desc))>160: probs.append(f"desc {len(html.unescape(desc))}")
    if h1!=1: probs.append(f"h1 {h1}")
    if faqs!=vis: probs.append(f"faq {faqs}!={vis}")
    if "noindex" in t: probs.append("noindex")
    # internal links
    d=os.path.dirname(f)
    for h in re.findall(r'href="([^"#?]+)',t):
        if h.startswith(("http","tel:","mailto:","/")): continue
        tgt=os.path.normpath(os.path.join(d,h))
        if not (os.path.isfile(tgt) or os.path.isfile(os.path.join(tgt,"index.html"))): probs.append("broken "+h)
    if probs: bad+=1
    print(f"{p:60} w={words:4} faq={vis} {' '.join(probs)}")
print("problem pages:",bad)

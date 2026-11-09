# Submit changed sitemap URLs to IndexNow. Run from a Base44 sandbox:  python3 indexnow.py [--since 2026-10-15] [--daily] [host ...]
# --daily (Edwin 19 Oct 2026: IndexNow at least once a day for every website): every site is submitted every day, with its
# changed URLs (lastmod >= --since, default yesterday) plus its homepage, so no site goes a day without a submission.
import json,re,sys,urllib.request,urllib.error
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
SITES=[('pageonesingapore.com','88afa8ab82937e3ff1848834ee3965d4',['/sitemap.xml']),
('www.sggarage.com','adba3d204db0f9cd2fb386bf0cc497ce',['/sitemap.xml','/articles/sitemap.xml']),
('www.cleanicdetailing.com','02659208fb1f5b18fe19111d95aec5ed',['/sitemap.xml']),
('aliciaongproperty.com','fd109038030b62a78adde288147a4516',['/sitemap.xml']),
('dannychuafinancial.com','8f806152a130fff2777ef45e6a79909c',['/sitemap.xml']),
('sofacaresg.com','7bc6243944e7d831c8e83f4303869914',['/sitemap.xml']),
('jackygearbox.com','bae8ecc2b65d5772f8be703cd544d1bc',['/sitemap.xml']),
('theecuclinicsg.com','a297274b0e018294438558b379efa82a',['/sitemap.xml']),
('starperformancemotor.com','99381246b278105dbbf132423ac73bbc',['/sitemap.xml']),
('wrapstarautostyle.com','dcf0dd5907cd49c0ba4cdeee3318b569',['/sitemap.xml']),
('aivs.sg','ca7b1686ff644a43b29a08f26a0764eb',['/sitemap.xml']),
('cskatrading.com','208f285bfeaaa073ac0b7bb77afc1625',['/sitemap.xml']),
('mykar.my','8e41c2f7a9d34b6e90b1c5f2d7a3e816',['/sitemap.xml']),
('planwithben.sg','6da50e97d7ef4e02aed6d44abd14ebee',['/sitemap.xml']),
('commercialfitout.sg','7d4c2a9e1f6b8035c4e2a7d9b1f60c38',['/sitemap.xml','/design-concepts/concept-of-the-day/']),
('batteryrescue.sg','b7e1c94a2f6d4e3b8a5c0d9e1f2a3b4c',['/sitemap.xml']),
('autotexautoparts.com.sg','7d3e9a51c4b84f2e9a0c6b1d58e2f437',['/sitemap.xml']),
('evbodyparts.sg','f9badb093cb250f8b0a26711842f59f2',['/sitemap.xml']),
('klardetails.com.sg','3f8b2c6d9e14a7b05c2d8e6f1a4b9c73',['/sitemap.xml']),
('sgcarworkshop.sg','4e898a9c4ad17bbc9c447eb375b62f0a',['/sitemap.xml']),
('contiexpert.sg','6f1c2e9a4b7d48c3a05e9d21b8f3c7e4',['/sitemap.xml']),
('newzenwerkz.com.sg','ea97d7cd7c1340c781fcd248d8d2c2ec',['/sitemap.xml']),
('xado-shop.sg','879bbba824426e5ff0c647ecf4805b25',['/sitemap.xml']),
('jbstaycations.com','8902a563f0e8890158ac4cf1b41cd50d',['/sitemap.xml'])]
args=sys.argv[1:]; since=''
if '--since' in args: i=args.index('--since'); since=args[i+1]; del args[i:i+2]
daily='--daily' in args
if daily:
  args.remove('--daily')
  if not since:
    import datetime; since=(datetime.datetime.utcnow()+datetime.timedelta(hours=8)-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
def get(u):
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=20); return r.read().decode('utf-8','replace')
def entries(x): return re.findall(r'<loc>\s*([^<\s]+)\s*</loc>(?:\s*<lastmod>\s*([^<\s]+))?',x)
for host,key,sms in SITES:
  if args and host not in args: continue
  try:
    if get(f'https://{host}/{key}.txt').strip()!=key: print(host,'KEY FILE WRONG'); continue
  except Exception as e: print(host,'KEY FILE MISSING',e); continue
  urls=[]
  for sm in sms:
    try:
      x=get(f'https://{host}{sm}')
      es=entries(x)
      if '<sitemapindex' in x:
        es=[e for c,_ in es for e in entries(get(c))]
      urls+=[u for u,lm in es if not since or (lm and lm>=since)]
    except Exception as e: print(host,sm,'ERR',e)
  if daily: urls=[f'https://{host}/']+urls
  urls=[u for u in dict.fromkeys(urls) if host.replace('www.','') in u]
  if not urls: print(host,'nothing changed'); continue
  body=json.dumps({'host':host,'key':key,'keyLocation':f'https://{host}/{key}.txt','urlList':urls[:10000]}).encode()
  try: st=urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow',data=body,headers={'Content-Type':'application/json; charset=utf-8'}),timeout=30).status
  except urllib.error.HTTPError as e: st=f'{e.code} {e.read()[:100]}'
  except Exception as e: st=str(e)
  print(host,len(urls),'urls',st)

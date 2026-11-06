import json, urllib.request, urllib.error
key = 'b7e1c94a2f6d4e3b8a5c0d9e1f2a3b4c'; host = 'batteryrescue.sg'
urls = ['https://batteryrescue.sg/'] + ['https://batteryrescue.sg/' + p for p in ['rescue/', 'services/jump-start/', 'services/towing/', 'articles/', 'articles/car-wont-start-what-to-do/', 'articles/efb-vs-agm-vs-standard-battery/', 'articles/car-battery-flat-every-morning/', 'llms.txt']]
data = json.dumps({'host': host, 'key': key, 'keyLocation': f'https://{host}/{key}.txt', 'urlList': urls}).encode()
try:
    st = urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow', data=data, headers={'Content-Type': 'application/json; charset=utf-8'}), timeout=40).status
except urllib.error.HTTPError as e:
    st = f'{e.code} {e.read()[:120]}'
except Exception as e:
    st = str(e)
print('INDEXNOW', st)
open('shots/result.txt', 'a').write(f'\nIndexNow {urls}: {st}\n')

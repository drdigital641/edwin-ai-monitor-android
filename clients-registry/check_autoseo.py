"""Check an autoseo.my /clients page (en/ms/zh HTML files given as args) against registry.json: the named live hosts
must equal registry rows agency=autoseo, status=live (incl. own=never), and no in-build/preview row may be named."""
import json, re, sys, os
reg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'registry.json')))
want = {r['host'] for r in reg['records'] if r['agency'] == 'autoseo' and r['visibility'] == 'white-label' and r['status'] == 'live'}
hidden = [r for r in reg['records'] if r['agency'] == 'autoseo' and r['status'] != 'live' and r['visibility'] != 'own']
bad = 0
for f in sys.argv[1:]:
    h = open(f, encoding='utf-8').read()
    got = set(re.findall(r'class="card site-card[^"]*" href="https://([^/"]+)/"', h))
    leak = [r['name'] for r in hidden if r['name'].lower() in h.lower() or '/preview/%s/' % r['id'] in h]
    ok = got == want and not leak
    bad += not ok
    print(f, 'OK' if ok else 'MISMATCH', len(got), 'missing', sorted(want - got), 'extra', sorted(got - want), 'leak', leak)
sys.exit(bad)

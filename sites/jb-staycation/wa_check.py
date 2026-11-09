"""Decode every wa.me link in the built site and check it equals Edwin's exact prefill (9 Nov 2026 5:09pm):
general text everywhere, house text on the two house pages and on house-named /stays/ buttons. Also checks the raw ?text= value matches his encoded strings. Sends nothing."""
import glob, html, os, re, sys
from urllib.parse import urlparse, unquote
S = os.environ.get('JB_OUT') or 'site'
ENC = {
 'general': 'Hi%20Daniel%2C%0A%0AI%27m%20planning%20a%20JB%20stay%20from%20Singapore.%0A%5BHouse%3A%20Please%20recommend%5D.%0ACheck-in%3A%20%20am%2Fpm%0ACheck-out%3A%20am%2Fpm.%0AAdults%3A%20%20%20%20%20pax%20.%0AChildren%3A%20%20%20pax.%0A%0APlease%20confirm%20availability%20and%20the%20final%20price%20total%20in%20RM%20.',
 'prima': 'Hi%20Daniel%2C%0A%0AI%27m%20planning%20a%20JB%20stay%20from%20Singapore.%0A%5BHouse%3A%20Prima%5D.%0ACheck-in%3A%20%20am%2Fpm%0ACheck-out%3A%20am%2Fpm.%0AAdults%3A%20%20%20%20%20pax%20.%0AChildren%3A%20%20%20pax.%0A%0APlease%20confirm%20availability%20and%20the%20final%20price%20total%20in%20RM%20.',
 'landak': 'Hi%20Daniel%2C%0A%0AI%27m%20planning%20a%20JB%20stay%20from%20Singapore.%0A%5BHouse%3A%20Landak%20Kawan%20Fun%20House%5D.%0ACheck-in%3A%20%20am%2Fpm%0ACheck-out%3A%20am%2Fpm.%0AAdults%3A%20%20%20%20%20pax%20.%0AChildren%3A%20%20%20pax.%0A%0APlease%20confirm%20availability%20and%20the%20final%20price%20total%20in%20RM%20.',
}
TXT = {k: unquote(v) for k, v in ENC.items()}
bad = links = 0; per = {}
for f in sorted(glob.glob(S + '/**/*.html', recursive=True)):
    rel = f[len(S):].lstrip('/')
    want = 'prima' if rel.startswith('stays/prima-') else 'landak' if rel.startswith('stays/landak-') else 'general'
    t = open(f, encoding='utf-8').read()
    for href, lab in re.findall(r'href="(https://wa\.me/[^"]*)"[^>]*?data-cta-label="([^"]*)"', t):
        links += 1
        if rel == 'stays/index.html':   # /stays/: house-named buttons carry their house (Edwin 9 Nov 5:27pm)
            want = 'prima' if 'prima' in lab else 'landak' if 'landak' in lab else 'general'
        u = urlparse(html.unescape(href)); raw = u.query[5:] if u.query.startswith('text=') else None
        ok = u.path == '/6590062198' and raw == ENC[want] and unquote(raw) == TXT[want]
        if not ok: bad += 1; print('BAD', rel, href[:120])
        per[want] = per.get(want, 0) + 1
    if 'data-cta="whatsapp"' not in t and 'wa.me' in t: print('NO TRACK ATTR', rel); bad += 1
print('wa links', links, per, 'bad', bad)
sys.exit(1 if bad else 0)

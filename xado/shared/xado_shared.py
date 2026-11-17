#!/usr/bin/env python3
"""XADO shared parts (xado-shop.sg). ONE place for the repeated blocks; pages stay plain server-rendered HTML.

- keep_reading(slug)        -> the "Keep reading" section for an article, from related-articles.json
- fix_home_links(html)      -> Home/logo links and BreadcrumbList Home item point at the root "/" (never index.html)
- apply(html, slug=None)    -> both, on a whole page

Night run: render the new article from a current live article, then run
    python3 xado_shared.py check            # every article listed by >= 2 others, 3-4 related each
    python3 xado_shared.py render <slug>    # prints the Keep reading block
    python3 xado_shared.py apply <file> [slug]  # rewrites a local page in place
"""
import html as H, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, 'related-articles.json')))
ART = DATA['articles']

def card(slug):
    a = ART[slug]
    return ('<a class="rel" href="%s.html"><img src="../assets/img/%s" alt="" loading="lazy"><span>%s</span><b>%s</b></a>'
            % (slug, a['img'], a['cat'], a['title']))

def keep_reading(slug):
    return ('<section class="wrap"><h2>Keep reading</h2><div class="rels">'
            + ''.join(card(s) for s in ART[slug]['related']) + '</div></section>')

KR = re.compile(r'<section class="wrap"><h2>Keep reading</h2><div class="rels">.*?</div></section>', re.S)

def fix_home_links(h):
    h = re.sub(r'href="(?:\.\./)*index\.html"', 'href="/"', h)
    h = h.replace('href="https://xado-shop.sg/index.html"', 'href="https://xado-shop.sg/"')
    h = h.replace('"item": "https://xado-shop.sg/index.html"', '"item": "https://xado-shop.sg/"')
    return h

def apply(h, slug=None):
    h = fix_home_links(h)
    if slug:
        new = keep_reading(slug)
        h, n = KR.subn(lambda m: new, h)
        if n != 1:
            raise SystemExit('Keep reading block not found exactly once (%d)' % n)
    return h

def check():
    inbound = {s: 0 for s in ART}
    bad = []
    for s, a in ART.items():
        if not 3 <= len(a['related']) <= 4: bad.append('%s has %d related' % (s, len(a['related'])))
        for r in a['related']:
            if r not in ART: bad.append('%s -> unknown %s' % (s, r))
            elif r == s: bad.append('%s lists itself' % s)
            else: inbound[r] += 1
    bad += ['%s is listed by only %d articles' % (s, n) for s, n in inbound.items() if n < 2]
    print('\n'.join(bad) or 'OK: %d articles, inbound %s' % (len(ART), inbound))
    return not bad

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'check': sys.exit(0 if check() else 1)
    if cmd == 'render': print(keep_reading(sys.argv[2]))
    if cmd == 'apply':
        p = sys.argv[2]; slug = sys.argv[3] if len(sys.argv) > 3 else None
        open(p, 'w').write(apply(open(p).read(), slug))

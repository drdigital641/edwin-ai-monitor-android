"""Maison WhatsApp link rules (Edwin 16 Nov 2026): every wa.me anchor opens in a new tab
(target="_blank" rel="noopener"), carries data-cta="whatsapp", and the layout-plan prefill is short.
Never changes the number. Idempotent: running it twice changes nothing."""
import re
from urllib.parse import quote, unquote

TAG = re.compile(r'<a\s[^>]*?href="https://(?:wa\.me|api\.whatsapp\.com)/[^"]*"[^>]*>', re.I)
HREF = re.compile(r'href="(https://wa\.me/\d+\?text=)([^"]*)"')
OLD_PLAN = re.compile(r"Hi Maison, I['’]m collecting keys at (.+?) \((.+)\)\. Can I get a free layout plan for my \2\?$")

def short_text(t):
    m = OLD_PLAN.match(t)
    return f"Hi Maison, I'd like a free layout plan for my {m.group(2)} at {m.group(1)}." if m else t

def fix_tag(tag):
    def href(m):
        raw = m.group(2).replace('&amp;', '&')
        t = unquote(raw); n = short_text(t)
        return m.group(0) if n == t else f'href="{m.group(1)}{quote(n, safe="")}"'
    tag = HREF.sub(href, tag)
    add = []
    if not re.search(r'\starget=', tag): add.append('target="_blank"')
    rm = re.search(r'\srel="([^"]*)"', tag)
    if not rm: add.append('rel="noopener"')
    elif 'noopener' not in rm.group(1).split():
        tag = tag[:rm.start(1)] + (rm.group(1) + ' noopener').strip() + tag[rm.end(1):]
    if not re.search(r'\sdata-cta=', tag): add.append('data-cta="whatsapp"')
    if add: tag = tag[:-1].rstrip() + ' ' + ' '.join(add) + '>'
    return tag

def fix_html(html):
    return TAG.sub(lambda m: fix_tag(m.group(0)), html)

if __name__ == '__main__':
    import sys
    for p in sys.argv[1:]:
        s = open(p, encoding='utf-8').read(); o = fix_html(s)
        if o != s: open(p, 'w', encoding='utf-8').write(o); print('fixed', p)

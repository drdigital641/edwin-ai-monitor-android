"""Website Manager "For workshops" header (live 22 Nov 2026, qw.css / qw.js), brought into the build so a rebuild keeps it.
qwify() adds exactly what Website Manager added on live to a page that uses the shared header: the qw.css link after dir.css,
the "For workshops" button beside the menu, the "For workshops: get Featured" menu link before About, and qw.js after dir.js."""
import re

QW_V = '20261122'


def qwify(h):
    if '<details class="menu">' not in h or 'assets/qw.css' in h:
        return h
    m = re.search(r'<link rel="stylesheet" href="([^"]*)assets/dir\.css\?v=[0-9a-f]+">', h)
    if not m:
        return h
    p = m.group(1)
    h = h.replace(m.group(0), m.group(0) + '\n<link rel="stylesheet" href="%sassets/qw.css?v=%s">' % (p, QW_V), 1)
    h = h.replace('<details class="menu">', '<div class="qw-r"><a class="qw-fw" href="%slist-your-workshop/" data-cta="nav_for_workshops">For workshops</a><details class="menu">' % p, 1)
    about = '<a class="mabout" href="%sabout/">About</a></nav></details>' % p
    h = h.replace(about, '<a class="mabout qw-mfw" href="%slist-your-workshop/" data-cta="nav_for_workshops_menu">For workshops: get Featured</a>%s</div>' % (p, about), 1)
    h = re.sub(r'(<script src="%sassets/dir\.js\?v=[0-9a-f]+" defer></script>\n)' % re.escape(p),
               lambda x: x.group(1) + '<script src="%sassets/qw.js?v=%s" defer></script>\n' % (p, QW_V), h, count=1)
    return h


def qw_intro(h):
    """Website Manager 22 Nov 2026 on listing pages (areas, services): the "In short" answer and lede leave the hero and go into a
    <section class="qw-intro"> placed right after the first workshop grid section, which moves up to sit right under the hero."""
    if 'class="qw-intro"' in h:
        return h
    m = re.search(r'(<section class="hero"[^>]*><div class="w">(?:(?!</section>).)*?</h1>)((?:(?!</section>).)*?)(</div></section>\n)', h, re.S)
    if not m or not re.search(r'<p class="(answer|lede)"', m.group(2)):
        return h
    intro = m.group(2)
    g = None
    for s in re.finditer(r'<section[^>]*>.*?</section>', h[m.end():], re.S):
        if 'class="grid"' in s.group(0):
            g = s; break
    if not g:
        return h
    gs, ge = m.end() + g.start(), m.end() + g.end()
    G = h[gs:ge]
    before, after = h[m.end():gs], h[ge:]
    rest = (before[:-1] if before.endswith('\n') else before) + after
    fm = re.match(r'(<section class="alt featblock"><div class="w"><h2>.*?</h2>)(<p class="fine">Paid placements[^<]*</p>)(.*)(</div></section>)$', G, re.S)
    if fm:   # Featured block: the "Paid placements" note moves under the cards
        G = fm.group(1) + fm.group(3) + fm.group(2) + fm.group(4)
    return h[:m.start()] + m.group(1) + m.group(3) + G + '\n<section class="qw-intro"><div class="w">' + intro + '</div></section>\n' + rest

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

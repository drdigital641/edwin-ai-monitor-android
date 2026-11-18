"""Shared AutoSEO three-language template parts (Edwin's standing rule, 18 Nov 2026).

Every AutoSEO site build imports this file, so one edit here changes the language switcher, the hreflang head
block and the sitemap language entries on every page of every site that is rebuilt. Sites keep their own look;
this file only owns the language plumbing.

  import autoseo_i18n as I18N
  for L in I18N.LANGS: ...                       # en at the root, ms at /ms/, zh at /zh/
  I18N.page_path(L, 'services/')                 # 'ms/services/'
  I18N.hreflang_links(absu, 'services/')         # <link rel="alternate"> x3 + x-default (in the shared head)
  I18N.switcher(u, 'services/', L, label)        # header switcher EN / BM / 中文 (in the shared header)
  I18N.sitemap_xml(absu, ['', 'services/'], lastmod)  # every page x 3 languages with xhtml:link + x-default

absu(p) must return the absolute URL of site path p (no leading slash); u(p) the root-relative href.
"""
from html import escape as _e

# code, folder prefix, html lang + hreflang code, switcher label, og:locale
LANGS = [
    {'code': 'en', 'prefix': '', 'hreflang': 'en', 'label': 'EN', 'og_locale': 'en_MY', 'name': 'English'},
    {'code': 'ms', 'prefix': 'ms/', 'hreflang': 'ms', 'label': 'BM', 'og_locale': 'ms_MY', 'name': 'Bahasa Melayu'},
    {'code': 'zh', 'prefix': 'zh/', 'hreflang': 'zh-Hans', 'label': '中文', 'og_locale': 'zh_CN', 'name': '简体中文'},
]
BY_CODE = {L['code']: L for L in LANGS}
DEFAULT = LANGS[0]  # x-default always points at the English URL


def lang(code):
    return BY_CODE[code]


def page_path(L, path=''):
    """Site path of `path` (the English path, no leading slash) in language L."""
    return L['prefix'] + path


def hreflang_links(absu, path=''):
    """The hreflang block for the shared head partial: one link per language plus x-default (English)."""
    out = [f'<link rel="alternate" hreflang="{L["hreflang"]}" href="{absu(page_path(L, path))}">' for L in LANGS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{absu(page_path(DEFAULT, path))}">')
    return '\n'.join(out)


def og_locale_tags(L):
    alts = ''.join(f'\n<meta property="og:locale:alternate" content="{o["og_locale"]}">' for o in LANGS if o is not L)
    return f'<meta property="og:locale" content="{L["og_locale"]}">' + alts


def switcher(u, path, L, aria_label='Language', cls='lang-sw'):
    """Header language switcher. Labels are fixed house-wide: EN, BM, 中文. Links go to the same page in each language."""
    links = []
    for o in LANGS:
        cur = ' aria-current="true"' if o is L else ''
        links.append(f'<a href="{u(page_path(o, path))}" hreflang="{o["hreflang"]}" lang="{o["hreflang"]}"{cur}>{o["label"]}</a>')
    sep = '<span class="sl" aria-hidden="true">/</span>'
    return f'<nav class="{cls}" aria-label="{_e(aria_label)}">{sep.join(links)}</nav>'


def sitemap_xml(absu, paths, lastmod):
    """sitemap.xml generated from the page list: every English path and its /ms/ and /zh/ twins, each with the
    full xhtml:link set and x-default. `lastmod` is a date string or a function(path) -> date string."""
    lm = lastmod if callable(lastmod) else (lambda p: lastmod)
    rows = []
    for L in LANGS:
        for p in paths:
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{o["hreflang"]}" href="{absu(page_path(o, p))}"/>' for o in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{absu(page_path(DEFAULT, p))}"/>'
            rows.append(f'<url><loc>{absu(page_path(L, p))}</loc><lastmod>{lm(p)}</lastmod>{alts}</url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(rows) + '\n</urlset>\n')


def check_twins(page_files):
    """Gate: every English page must have its /ms/ and /zh/ twin. page_files = set of built site paths.
    Returns a list of problems (empty = pass)."""
    bad = []
    en = [p for p in page_files if not p.startswith(('ms/', 'zh/'))]
    for p in en:
        for L in LANGS[1:]:
            if page_path(L, p) not in page_files:
                bad.append(f'missing {L["code"]} twin of /{p}')
    return bad

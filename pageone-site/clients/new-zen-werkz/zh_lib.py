"""Shared helpers for the Chinese (/zh/) version: find translatable strings in the built English pages."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(HERE, 'site')
LD_KEYS = {'name', 'description', 'text', 'headline', 'serviceType', 'alternativeHeadline', 'abstract', 'caption', 'contactType', 'dayOfWeek_label'}
ATTR_RE = re.compile(r'\b(alt|aria-label|title)="([^"]*)"')
META_RE = re.compile(r'(<meta (?:name|property)="(?:description|og:title|og:description)" content=")([^"]*)(")')
SKIP = re.compile(r'^[\s\d+·•|/:,.\-–—()#&;]*$')


def english_pages():
    out = []
    for root, _, files in os.walk(SITE_DIR):
        if os.sep + 'zh' in root[len(SITE_DIR):] or root.endswith('/img'):
            continue
        for f in files:
            if f.endswith('.html'):
                full = os.path.join(root, f)
                out.append(os.path.relpath(full, SITE_DIR))
    return sorted(out)


def split_parts(html):
    """Yield (kind, text) for every piece: 'raw' (tags, scripts) or 'text' (a text node)."""
    pos = 0
    for m in re.finditer(r'<script\b.*?</script>|<style\b.*?</style>|<[^>]+>', html, re.S):
        if m.start() > pos:
            yield 'text', html[pos:m.start()]
        yield 'raw', m.group(0)
        pos = m.end()
    if pos < len(html):
        yield 'text', html[pos:]


def wanted(s):
    s = s.strip()
    return bool(s) and not SKIP.match(s) and re.search('[A-Za-z]', s)


def ld_strings(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in LD_KEYS and isinstance(v, str) and wanted(v):
                acc.add(v)
            elif k == 'knowsAbout' and isinstance(v, list):
                acc.update(x for x in v if isinstance(x, str))
            else:
                ld_strings(v, acc)
    elif isinstance(obj, list):
        for x in obj:
            ld_strings(x, acc)

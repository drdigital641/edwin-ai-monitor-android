#!/usr/bin/env python3
"""One-switch go-live module (Edwin, 20 Nov 2026). Shared by AutoSEO and Page One site builds.

A site has ONE config (site.json). Everything host-dependent is generated from it:
canonical, og:url, og:image/twitter:image, hreflang, JSON-LD url/@id, sitemap.xml,
robots.txt Sitemap line, llms.txt header, the host-aware .htaccess, and the go-live check.
Flipping "live" re-renders all of it. Never hard-code a domain in a page.

CLI:
  golive.py htaccess site.json           -> prints the folder .htaccess
  golive.py parent  site.json            -> prints the host-limited block for a parent .htaccess
  golive.py retarget site.json DIST      -> rewrites share/canonical tags in a built tree (idempotent)
  golive.py files   site.json DIST       -> writes sitemap.xml, robots.txt into DIST
  golive.py check   site.json [--acme]   -> go-live check, exit 1 on any failure
"""
import json, re, sys, os, ssl, http.client, struct
from urllib.parse import urlsplit

LANG_PREFIX = {"en": "", "ms": "ms/", "zh": "zh/"}
HREFLANG = {"en": "en", "ms": "ms", "zh": "zh-Hans"}
PREVIEW_HOSTS = ("autoseo.my", "pageonesingapore.com")


class Cfg:
    def __init__(self, d):
        self.d = d
        self.slug = d["slug"]
        pu = urlsplit(d["preview_url"])
        self.preview_host = pu.netloc.lower()
        self.preview_path = pu.path if pu.path.endswith("/") else pu.path + "/"
        self.live_domain = (d.get("live_domain") or "").lower().strip("/")   # empty until Edwin enters it
        self.live = bool(d.get("live", False)) and bool(self.live_domain)    # never live without a domain
        self.languages = d.get("languages", ["en", "ms", "zh"])
        self.og_path = d.get("og_image", "images/og.jpg").lstrip("/")
        self.og_version = str(d.get("og_version", ""))
        self.hreflang = {**HREFLANG, **d.get("hreflang", {})}
        self.preview_base = "https://%s%s" % (self.preview_host, self.preview_path)
        # No domain yet: pages carry the preview URL only. Once a domain is set, canonical is the live domain.
        self.canonical_base = ("https://%s/" % self.live_domain) if self.live_domain else self.preview_base

    @property
    def share_base(self):
        """Where og:image / twitter:image must resolve RIGHT NOW."""
        return self.canonical_base if self.live else self.preview_base

    def canon(self, path=""):
        return self.canonical_base + path.lstrip("/")

    def og_image(self):
        q = ("?v=" + self.og_version) if self.og_version else ""
        return self.share_base + self.og_path + q

    def lang_path(self, lang, path):
        return LANG_PREFIX[lang] + path.lstrip("/")


def load(path):
    with open(path) as f:
        return Cfg(json.load(f))


# ---------------------------------------------------------------- tags
def head_tags(c, path, lang, img=None):
    """Share/canonical tags for one page. path = English-relative path ('' = home, 'services/').
    img = optional page-own share image path relative to the site (article pages: the image gate needs their own image)."""
    url = c.canon(c.lang_path(lang, path))
    img = (c.share_base + img.lstrip("/")) if img else c.og_image()
    out = ['<link rel="canonical" href="%s">' % url]
    for l in c.languages:
        out.append('<link rel="alternate" hreflang="%s" href="%s">' % (c.hreflang[l], c.canon(c.lang_path(l, path))))
    out.append('<link rel="alternate" hreflang="x-default" href="%s">' % c.canon(path))
    out += ['<meta property="og:url" content="%s">' % url,
            '<meta property="og:image" content="%s">' % img,
            '<meta property="og:image:secure_url" content="%s">' % img,
            '<meta property="og:image:type" content="image/jpeg">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta name="twitter:image" content="%s">' % img]
    return "\n".join(out)


def jsonld_id(c, fragment="business"):
    return c.canon("#" + fragment)


def sitemap_xml(c, paths, lastmod):
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in paths:
        for l in c.languages:
            rows.append("<url><loc>%s</loc><lastmod>%s</lastmod>" % (c.canon(c.lang_path(l, p)), lastmod))
            for m in c.languages:
                rows.append('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (c.hreflang[m], c.canon(c.lang_path(m, p))))
            rows.append('<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % c.canon(p))
            rows.append("</url>")
    rows.append("</urlset>")
    return "\n".join(rows) + "\n"


def robots_txt(c):
    return "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % c.canonical_base


def llms_header(c, name, summary):
    return "# %s\n\n> %s\n\nSite: %s\nSitemap: %ssitemap.xml\n" % (name, summary, c.canonical_base, c.canonical_base)


# ---------------------------------------------------------------- retarget a built tree
def _swap_base(val, c):
    """Map any preview-base or live-base URL onto the canonical live base."""
    for b in (c.preview_base, "http://" + c.live_domain + "/", "https://www." + c.live_domain + "/"):
        if val.startswith(b):
            return c.canonical_base + val[len(b):]
    return val


def retarget_html(html, c):
    img = c.og_image()
    def meta(prop_attr, prop):
        return re.compile(r'(<meta\s+%s="%s"\s+content=")([^"]*)(")' % (prop_attr, re.escape(prop)), re.I)
    def share(m):
        v = m.group(2)
        # a page's own image (article) keeps its file, only its host moves; the generic share image is reset
        own = _swap_base(v, c) if (c.og_path not in v) else img
        return m.group(1) + own + m.group(3)
    for attr, prop in (("property", "og:image"), ("property", "og:image:secure_url"), ("name", "twitter:image")):
        html = meta(attr, prop).sub(share, html)
    html = meta("property", "og:image:type").sub(lambda m: m.group(1) + "image/jpeg" + m.group(3), html)
    html = meta("property", "og:url").sub(lambda m: m.group(1) + _swap_base(m.group(2), c) + m.group(3), html)
    html = re.sub(r'(<link\s+rel="(?:canonical|alternate)"[^>]*?href=")([^"]*)(")',
                  lambda m: m.group(1) + _swap_base(m.group(2), c) + m.group(3), html, flags=re.I)
    def ld(m):
        body = re.sub(r'("(?:url|@id)"\s*:\s*")([^"]*)(")', lambda k: k.group(1) + _swap_base(k.group(2), c) + k.group(3), m.group(2))
        return m.group(1) + body + m.group(3)
    html = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, html, flags=re.S)
    return html


def retarget_tree(dist, c):
    n = 0
    for root, _, fs in os.walk(dist):
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(root, f)
                s = open(p, encoding="utf-8").read()
                t = retarget_html(s, c)
                if t != s:
                    open(p, "w", encoding="utf-8").write(t); n += 1
    return n


# ---------------------------------------------------------------- .htaccess
def _host_re(hosts):
    return "^(www\\.)?(%s)(:[0-9]+)?$" % "|".join(re.escape(h) for h in hosts)


def htaccess(c):
    """Folder .htaccess for the site's docroot folder (e.g. preview/<slug>/). Host-aware."""
    L, ph, live = c.live_domain, c.preview_host, c.live
    o = ["# Generated by autoseo-template/golive (do not hand edit). slug=%s live=%s" % (c.slug, live),
         "# Rules are limited to the named hosts. ACME is excluded from every redirect.",
         "Options -Indexes", "RewriteEngine On", "",
         "# ACME http-01: always reachable over http, never redirected, never behind auth",
         "RewriteCond %{REQUEST_URI} ^/\\.well-known/acme-challenge/ [NC]", "RewriteRule ^ - [L]", "",
         "# Noindex ONLY on the preview host (never on the live host)",
         "<IfModule mod_setenvif.c>", 'SetEnvIfNoCase Host "%s" SITE_PREVIEW_HOST=1' % _host_re([ph]), "</IfModule>",
         "<IfModule mod_headers.c>", 'Header always set X-Robots-Tag "noindex, nofollow" env=SITE_PREVIEW_HOST', "</IfModule>", ""]
    if live:
        o += ["# LIVE host: www -> https apex, one hop, same path and query",
              "RewriteCond %%{HTTP_HOST} ^www\\.%s(:[0-9]+)?$ [NC]" % re.escape(L),
              "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % L, "",
              "# LIVE host: http -> https apex",
              "RewriteCond %%{HTTP_HOST} ^%s(:[0-9]+)?$ [NC]" % re.escape(L),
              "RewriteCond %{HTTPS} !=on",
              "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % L, "",
              "# PREVIEW host only: /preview/<slug>/... -> live domain, same path. Never fires on the live host.",
              "RewriteCond %%{HTTP_HOST} %s [NC]" % _host_re([ph]),
              "RewriteCond %%{REQUEST_URI} ^%s(?:/(.*))?$ [NC]" % re.escape(c.preview_path.rstrip("/")),
              "RewriteRule ^ https://%s/%%1 [L,R=301]" % L]
    else:
        o += ["# NOT LIVE: preview host only, http -> https and www -> apex, same path",
              "RewriteCond %%{HTTP_HOST} ^www\\.%s(:[0-9]+)?$ [NC]" % re.escape(ph),
              "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % ph,
              "RewriteCond %%{HTTP_HOST} ^%s(:[0-9]+)?$ [NC]" % re.escape(ph),
              "RewriteCond %{HTTPS} !=on",
              "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % ph]
    return "\n".join(o) + "\n"


def parent_block(c):
    """Block to add to a PARENT .htaccess (autoseo.my root) when the folder file cannot be created.
    Every rule is limited to the live host or the preview host, so it never catches another addon domain."""
    L, ph = c.live_domain, c.preview_host
    return "\n".join([
        "# --- golive:%s (generated) ---" % c.slug,
        "RewriteCond %{REQUEST_URI} ^/\\.well-known/acme-challenge/ [NC]", "RewriteRule ^ - [L]",
        "RewriteCond %%{HTTP_HOST} ^www\\.%s$ [NC]" % re.escape(L), "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % L,
        "RewriteCond %%{HTTP_HOST} ^%s$ [NC]" % re.escape(L), "RewriteCond %{HTTPS} !=on",
        "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % L,
        "RewriteCond %%{HTTP_HOST} %s [NC]" % _host_re([ph]),
        "RewriteCond %%{REQUEST_URI} ^%s(?:/(.*))?$ [NC]" % re.escape(c.preview_path.rstrip("/")),
        "RewriteRule ^ https://%s/%%1 [L,R=301]" % L,
        "# --- end golive:%s ---" % c.slug]) + "\n"


def parent_htaccess(own_hosts, extra_blocks=""):
    """Safe parent rules: http->https and www->apex ONLY for the parent's own hosts (never an addon domain)."""
    h0 = own_hosts[0]
    return "\n".join([
        "RewriteEngine On",
        "RewriteCond %{REQUEST_URI} ^/\\.well-known/acme-challenge/ [NC]", "RewriteRule ^ - [L]",
        extra_blocks.rstrip(),
        "RewriteCond %%{HTTP_HOST} %s [NC]" % _host_re(own_hosts),
        "RewriteCond %{HTTPS} !=on",
        "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % h0,
        "RewriteCond %%{HTTP_HOST} ^www\\.%s(:[0-9]+)?$ [NC]" % re.escape(h0),
        "RewriteRule ^ https://%s%%{REQUEST_URI} [L,R=301]" % h0]) + "\n"


# ---------------------------------------------------------------- domain gate
SERVER_IP = "173.254.31.20"


def domain_status(domain):
    """Gate for the Live switch: domain must resolve to the Bluehost IP and https must be valid."""
    import socket
    out = {"domain": domain, "dns_ok": False, "https_ok": False, "ips": [], "detail": ""}
    try:
        out["ips"] = sorted({i[4][0] for i in socket.getaddrinfo(domain, 443, socket.AF_INET)})
        out["dns_ok"] = out["ips"] == [SERVER_IP]
        if not out["dns_ok"]: out["detail"] = "resolves to %s, need %s" % (",".join(out["ips"]), SERVER_IP)
    except Exception as e:
        out["detail"] = "DNS: %s" % e; return out
    try:
        _req(domain, "/", True, "HEAD")      # default context verifies cert chain and hostname
        out["https_ok"] = True
    except Exception as e:
        out["detail"] = (out["detail"] + " HTTPS: %s" % e).strip()
    out["can_go_live"] = out["dns_ok"] and out["https_ok"]
    return out


# ---------------------------------------------------------------- go-live check
def _req(host, path, https=True, method="GET", timeout=20, body=False):
    cls = http.client.HTTPSConnection if https else http.client.HTTPConnection
    kw = {"context": ssl.create_default_context()} if https else {}
    cn = cls(host, timeout=timeout, **kw)
    cn.request(method, path, headers={"User-Agent": "golive-check/1.0", "Accept": "*/*"})
    r = cn.getresponse(); data = r.read() if body else b""
    h = {k.lower(): v for k, v in r.getheaders()}
    cn.close(); return r.status, h, data


def jpeg_size(b):
    i = 2
    while i < len(b):
        if b[i] != 0xFF: i += 1; continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", b[i + 5:i + 9]); return w, h
        i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None


def go_live_check(c, acme_file=".well-known/acme-challenge/golive-test.txt", probe_paths=None):
    L, res = c.live_domain, []
    def add(name, ok, info): res.append((name, bool(ok), info))
    def one301(label, host, https, path="/"):
        try:
            s, h, _ = _req(host, path, https)
            add(label, s == 301 and h.get("location", "").rstrip("/") == ("https://%s%s" % (L, path)).rstrip("/"), "%s %s" % (s, h.get("location")))
        except Exception as e: add(label, False, "unreachable: %s" % e)
    one301("http apex -> https apex (single 301)", L, False)
    one301("http www -> https apex (single 301)", "www." + L, False)
    one301("https www -> https apex (single 301)", "www." + L, True)
    home_html = b""
    paths = ["/"] + ["/%s" % LANG_PREFIX[l] for l in c.languages if l != "en"] + ["/sitemap.xml"]
    for p in (probe_paths or paths):
        try:
            s, h, d = _req(L, p, True, body=(p == "/"))
            if p == "/": home_html = d
            add("live %s 200, no X-Robots-Tag" % p, s == 200 and "x-robots-tag" not in h, "%s xrt=%s" % (s, h.get("x-robots-tag")))
        except Exception as e: add("live %s" % p, False, "unreachable: %s" % e)
    try:
        s, h, _ = _req(c.preview_host, c.preview_path)
        add("preview host -> 301 to live", s == 301 and h.get("location", "").startswith("https://" + L), "%s %s" % (s, h.get("location")))
    except Exception as e: add("preview host -> 301 to live", False, "unreachable: %s" % e)
    imgs = set(re.findall(r'(?:og:image|twitter:image)"\s+content="([^"]+)"', home_html.decode("utf8", "ignore")))
    for u in sorted(imgs) or []:
        try:
            su = urlsplit(u); s, h, d = _req(su.netloc, su.path + ("?" + su.query if su.query else ""), body=True)
            sz = jpeg_size(d)
            add("og/twitter image %s" % u, s == 200 and h.get("content-type", "").startswith("image/jpeg") and sz == (1200, 630), "%s %s %s" % (s, h.get("content-type"), sz))
        except Exception as e: add("og/twitter image %s" % u, False, str(e))
    if not imgs: add("og/twitter image present", False, "none found on live home")
    if acme_file:
        try:
            s, h, _ = _req(L, "/" + acme_file, False)
            add("http ACME test file 200, no redirect", s == 200, "%s %s" % (s, h.get("location")))
        except Exception as e: add("http ACME test file", False, "unreachable: %s" % e)
    return res


# ---------------------------------------------------------------- "Just launched" popup (Edwin 20 Nov 2026: "Yes, auto update")
def launch_entry(c, name, line, trade, launched):
    """Entry for autoseo.my/assets/launches.json (newest first = the popup card). line/trade = {en, ms, zh}.
    White-label rule: the site must already be live AND have its card + /assets/clients/<slug>.webp on autoseo.my/clients/."""
    return {"id": "%s-%s" % (c.slug, launched), "name": name, "url": c.canonical_base, "host": c.live_domain,
            "image": "/assets/clients/%s.webp" % c.slug, "launched": launched, "trade": trade, "line": line}


def add_launch(launches_json_text, entry):
    """Prepend entry to launches.json text (idempotent on id). Returns the new text."""
    d = json.loads(launches_json_text)
    d["launches"] = [entry] + [x for x in d.get("launches", []) if x.get("id") != entry["id"]]
    return json.dumps(d, ensure_ascii=False, indent=2) + "\n"


def main(a):
    if len(a) < 2: print(__doc__); return 2
    cmd, c = a[0], load(a[1])
    if cmd == "htaccess": print(htaccess(c), end="")
    elif cmd == "parent": print(parent_block(c), end="")
    elif cmd == "retarget": print("files changed:", retarget_tree(a[2], c))
    elif cmd == "files":
        open(os.path.join(a[2], "robots.txt"), "w").write(robots_txt(c)); print("robots.txt written")
    elif cmd == "domain": print(json.dumps(domain_status(c.live_domain)))
    elif cmd == "check":
        r = go_live_check(c, acme_file=".well-known/acme-challenge/golive-test.txt" if "--acme" in a else None)
        for n, ok, i in r: print("%s  %s  [%s]" % ("PASS" if ok else "FAIL", n, i))
        return 0 if all(x[1] for x in r) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

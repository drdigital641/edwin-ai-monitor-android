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
        # ONE SETTING (Edwin 23 Nov 2026, after the MCS hand edit): go_live_domain. Empty = preview mode
        # (P = '/preview/<slug>', BASE = preview URL). Set = live: P = '', BASE = 'https://<domain>'. It sets
        # live_domain + live together, so a build never needs a hand edit of hardcoded paths again.
        gld = (d.get("go_live_domain") or "").lower().strip().strip("/")
        gld = re.sub(r"^https?://", "", gld).strip("/")
        if gld.startswith("www."): gld = gld[4:]
        if gld:
            self.live_domain, self.live = gld, True
        self.languages = d.get("languages", ["en"])  # Rule 6 default English only; MY-address sites set ["en","ms","zh"] in site.json
        self.og_path = d.get("og_image", "images/og.jpg").lstrip("/")
        self.og_version = str(d.get("og_version", ""))
        # IndexNow key (21 Nov 2026, Overseas Tyre 422): <key>.txt must sit in the site root. From site.json "indexnow_key"
        # or the env INDEXNOW_KEY (AutoSEO standard key); never printed. The Bridge Go live switch also places it if missing.
        k = str(d.get("indexnow_key") or os.environ.get("INDEXNOW_KEY") or "").strip().lower()
        self.indexnow_key = k if re.fullmatch(r"[0-9a-f]{32}", k) else ""
        # REDIRECT EXCLUSIONS (Edwin 23 Nov 2026, after sgautobots.com 301'd /preview/sg-autobots/booking/): paths inside the
        # preview folder that hold their own app and must never be caught by the folder-wide 301. site.json "redirect_exclude".
        self.redirect_exclude = clean_excludes(d.get("redirect_exclude", []))
        self.hreflang = {**HREFLANG, **d.get("hreflang", {})}
        self.preview_base = "https://%s%s" % (self.preview_host, self.preview_path)
        # No domain yet: pages carry the preview URL only. Once a domain is set, canonical is the live domain.
        self.canonical_base = ("https://%s/" % self.live_domain) if self.live_domain else self.preview_base

    @property
    def base_path(self):
        """P for builders: '' when live, '/preview/<slug>' (no trailing slash) on the preview host."""
        return "" if self.live else self.preview_path.rstrip("/")

    @property
    def site_base(self):
        """BASE for builders (no trailing slash): 'https://<domain>' when live, else the preview URL."""
        return ("https://%s" % self.live_domain) if self.live else self.preview_base.rstrip("/")

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
def head_tags(c, path, lang):
    """Share/canonical tags for one page. path = English-relative path ('' = home, 'services/')."""
    url = c.canon(c.lang_path(lang, path))
    img = c.og_image()
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
    for attr, prop in (("property", "og:image"), ("property", "og:image:secure_url"), ("name", "twitter:image")):
        html = meta(attr, prop).sub(lambda m: m.group(1) + img + m.group(3), html)
    html = meta("property", "og:image:type").sub(lambda m: m.group(1) + "image/jpeg" + m.group(3), html)
    html = meta("property", "og:url").sub(lambda m: m.group(1) + _swap_base(m.group(2), c) + m.group(3), html)
    html = re.sub(r'(<link\s+rel="(?:canonical|alternate)"[^>]*?href=")([^"]*)(")',
                  lambda m: m.group(1) + _swap_base(m.group(2), c) + m.group(3), html, flags=re.I)
    def ld(m):
        body = re.sub(r'("(?:url|@id)"\s*:\s*")([^"]*)(")', lambda k: k.group(1) + _swap_base(k.group(2), c) + k.group(3), m.group(2))
        return m.group(1) + body + m.group(3)
    html = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, html, flags=re.S)
    return html


def build_base(site):
    """For build.py: P, BASE = golive.build_base('site.json') (path or dict). Reads go_live_domain (or live_domain+live)."""
    c = load(site) if isinstance(site, str) else Cfg(site)
    return c.base_path, c.site_base


TEXT_EXT = (".html", ".xml", ".txt", ".js", ".css", ".json", ".webmanifest")


def retarget_paths(text, c):
    """Already-built files: swap every preview URL and root-relative /preview/<slug>/ path to the live site when live,
    and back when not live (idempotent). Covers links, src, srcset, CSS url(), sitemap, llms.txt, JSON-LD."""
    pv_abs, pv_path = c.preview_base, c.preview_path                      # https://autoseo.my/preview/x/ , /preview/x/
    if c.live:
        live_abs = "https://%s/" % c.live_domain
        text = text.replace(pv_abs, live_abs)
        return re.sub(r'(?<![\w.:/-])' + re.escape(pv_path), "/", text)
    return text      # flip back: canonical/og handled by retarget_html; root paths only exist after a live build


def retarget_tree(dist, c, paths=False):
    """paths=True also runs retarget_paths on every text file (use when the build hardcoded P)."""
    n = 0
    if paths:
        for root, _, fs in os.walk(dist):
            for f in fs:
                if f.endswith(TEXT_EXT) and f != ".htaccess":
                    p = os.path.join(root, f)
                    s = open(p, encoding="utf-8").read()
                    t = retarget_paths(s, c)
                    if t != s:
                        open(p, "w", encoding="utf-8").write(t)
    return n + _retarget_html_tree(dist, c)


def _retarget_html_tree(dist, c):
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


def _security_block():
    """Page One security headers v2 (Edwin 22 Nov 2026, PERMANENT): every generated .htaccess carries the shared block.
    Source of truth: /mnt/project-files/security/headers-template/security-headers-block.conf. Folders shown in the
    Base44 Controller/client panel may be framed by it."""
    here = os.path.dirname(os.path.abspath(__file__))
    tdir = os.path.normpath(os.path.join(here, "..", "..", "security", "headers-template"))
    if tdir not in sys.path:
        sys.path.insert(0, tdir)
    import security_headers
    return security_headers.block(frame_ancestors_extra="https://autoseo.my https://*.base44.app https://app.base44.com https://pageonesingapore.com")


_EXCLUDE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,60}(/[a-z0-9][a-z0-9._-]{0,60}){0,3}$")


def clean_excludes(items):
    """Lower-case, strip slashes, de-duplicate and SORT (same set = same bytes, so a re-run changes nothing). Bad entries raise."""
    if isinstance(items, str):
        items = [x for x in re.split(r"[\s,]+", items) if x]
    out = set()
    for x in items or []:
        s = str(x).strip().lower().strip("/")
        if not s:
            continue
        if not _EXCLUDE_RE.match(s) or ".." in s.split("/"):
            raise ValueError("redirect_exclude entry is not valid: %r" % x)
        out.add(s)
    return sorted(out)


def detect_apps(folder):
    """Safety default: direct subfolders of the built/live site folder that hold their own app (index.php, admin/ or api/).
    Returns [(name, why)]. Dot folders (.well-known) are skipped; ACME has its own rule."""
    hits = []
    for name in sorted(os.listdir(folder)):
        p = os.path.join(folder, name)
        if name.startswith(".") or not os.path.isdir(p) or not _EXCLUDE_RE.match(name.lower()):
            continue
        why = [w for w, ok in (("index.php", os.path.isfile(os.path.join(p, "index.php"))),
                                ("admin/", os.path.isdir(os.path.join(p, "admin"))),
                                ("api/", os.path.isdir(os.path.join(p, "api")))) if ok]
        if why:
            hits.append((name.lower(), " + ".join(why)))
    return hits


def _exclude_conds(c):
    pre = re.escape(c.preview_path)
    return ["RewriteCond %%{REQUEST_URI} !^%s%s(/|$) [NC]" % (pre, re.escape(p)) for p in c.redirect_exclude]


def htaccess(c):
    """Folder .htaccess for the site's docroot folder (e.g. preview/<slug>/). Host-aware."""
    L, ph, live = c.live_domain, c.preview_host, c.live
    o = ["# Generated by autoseo-template/golive (do not hand edit). slug=%s live=%s" % (c.slug, live),
         "# Rules are limited to the named hosts. ACME is excluded from every redirect.",
         _security_block().rstrip("\n"),
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
              "RewriteCond %%{HTTP_HOST} %s [NC]" % _host_re([ph]), *_exclude_conds(c),
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
        "RewriteCond %%{HTTP_HOST} %s [NC]" % _host_re([ph]), *_exclude_conds(c),
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
    if c.indexnow_key:
        try:
            s, h, d = _req(L, "/%s.txt" % c.indexnow_key, True, body=True)
            ok = s == 200 and d.decode("utf8", "ignore").strip() == c.indexnow_key
            add("IndexNow key file at site root (200, key matches)", ok, "%s%s" % (s, "" if ok or s != 200 else " wrong content"))
        except Exception as e: add("IndexNow key file at site root", False, "unreachable: %s" % str(e).replace(c.indexnow_key, "<key>"))
    else: add("IndexNow key file at site root", False, "no indexnow_key in site.json and no INDEXNOW_KEY set")
    if acme_file:
        try:
            s, h, _ = _req(L, "/" + acme_file, False)
            add("http ACME test file 200, no redirect", s == 200, "%s %s" % (s, h.get("location")))
        except Exception as e: add("http ACME test file", False, "unreachable: %s" % e)
    return res


def write_indexnow_key(c, dist):
    """Writes <key>.txt (content = key) in the site root of a built tree. Preview builds ship it too, so the live domain serves it from the first minute."""
    if c.indexnow_key:
        with open(os.path.join(dist, c.indexnow_key + ".txt"), "w") as f: f.write(c.indexnow_key)
    return bool(c.indexnow_key)


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
    elif cmd == "retarget": print("files changed:", retarget_tree(a[2], c, paths="--paths" in a))
    elif cmd == "base": print(json.dumps({"P": c.base_path, "BASE": c.site_base, "live": c.live}))
    elif cmd == "files":
        open(os.path.join(a[2], "robots.txt"), "w").write(robots_txt(c)); print("robots.txt written")
        if c.indexnow_key:
            write_indexnow_key(c, a[2]); print("IndexNow key file written (site root)")
        else: print("WARNING: no indexnow_key in site.json / INDEXNOW_KEY: no IndexNow key file written (the Go live switch adds the standard one)")
    elif cmd == "domain": print(json.dumps(domain_status(c.live_domain)))
    elif cmd == "check":
        r = go_live_check(c, acme_file=".well-known/acme-challenge/golive-test.txt" if "--acme" in a else None)
        for n, ok, i in r: print("%s  %s  [%s]" % ("PASS" if ok else "FAIL", n, i))
        return 0 if all(x[1] for x in r) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

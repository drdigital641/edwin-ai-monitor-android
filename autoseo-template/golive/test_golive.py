import json, golive as g
def cfg(live): 
    return g.Cfg({"slug":"x","preview_url":"https://autoseo.my/preview/x/","live_domain":"x.com.my","live":live,"og_version":"2"})
def test_share_base():
    assert cfg(False).og_image()=="https://autoseo.my/preview/x/images/og.jpg?v=2"
    assert cfg(True).og_image()=="https://x.com.my/images/og.jpg?v=2"
def test_canon_always_live():
    for l in (0,1): assert 'href="https://x.com.my/ms/a/"' in g.head_tags(cfg(l),"a/","ms")
def test_htaccess_live():
    h=g.htaccess(cfg(True))
    assert "acme-challenge" in h and "https://x.com.my/%1" in h and "^/preview/x(?:/(.*))?$" in h
    i=h.index("PREVIEW host only"); assert "HTTP_HOST} ^(www" in h[i:]  # preview redirect host-limited
    assert "https://autoseo.my/preview" not in h   # never redirects to preview host
def test_htaccess_off_no_live_rules():
    h=g.htaccess(cfg(False)); assert "https://x.com.my" not in h and "SITE_PREVIEW_HOST" in h
def test_retarget_flip():
    html='<link rel="canonical" href="https://autoseo.my/preview/x/a/"><meta property="og:image" content="https://autoseo.my/preview/x/images/og.jpg?v=2"><meta name="twitter:image" content="https://autoseo.my/preview/x/images/og.jpg?v=2"><script type="application/ld+json">{"url":"https://autoseo.my/preview/x/a/","@id":"https://x.com.my/#b"}</script>'
    o=g.retarget_html(html,cfg(True))
    assert o.count("https://x.com.my/images/og.jpg?v=2")==2 and 'href="https://x.com.my/a/"' in o and '"url":"https://x.com.my/a/"' in o
    assert g.retarget_html(o,cfg(False)).count("autoseo.my/preview/x/images/og.jpg")==2   # flip back
def test_sitemap_robots():
    c=cfg(True); assert "preview" not in g.sitemap_xml(c,["","a/"],"2026-11-20") and "Sitemap: https://x.com.my/sitemap.xml" in g.robots_txt(c)
def test_parent_safe():
    p=g.parent_htaccess(["autoseo.my"]); assert "^(www\\.)?(autoseo\\.my)" in p and p.index("acme")<p.index("HTTPS")
def test_no_domain_preview_only():
    c=g.Cfg({"slug":"x","preview_url":"https://autoseo.my/preview/x/","live_domain":"","live":True})
    assert not c.live and "x.com.my" not in g.head_tags(c,"","en") and c.canon("a/")=="https://autoseo.my/preview/x/a/"


def test_indexnow_key_file(tmp_path=None):
    import tempfile, os as _os
    d = tempfile.mkdtemp()
    c = g.Cfg({"slug": "x", "preview_url": "https://autoseo.my/preview/x/", "indexnow_key": "A" * 32})
    assert c.indexnow_key == "a" * 32 and g.write_indexnow_key(c, d)
    assert open(_os.path.join(d, "a" * 32 + ".txt")).read() == "a" * 32
    assert g.Cfg({"slug": "x", "preview_url": "https://autoseo.my/preview/x/", "indexnow_key": "../bad"}).indexnow_key in ("", _os.environ.get("INDEXNOW_KEY", "").lower())


def test_htaccess_has_security_headers():
    for live in (True, False):
        h = g.htaccess(cfg(live))
        assert h.count("# BEGIN Page One security headers v2") == 1
        for n in ("Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy",
                  "Permissions-Policy", "Content-Security-Policy ", "Content-Security-Policy-Report-Only"):
            assert "Header always set " + n in h, n
        assert h.index("security headers") < h.index("RewriteEngine On")
def test_go_live_domain_one_setting():
    pv = g.Cfg({"slug":"x","preview_url":"https://autoseo.my/preview/x/","go_live_domain":""})
    assert (pv.base_path, pv.site_base, pv.live) == ("/preview/x", "https://autoseo.my/preview/x", False)
    lv = g.Cfg({"slug":"x","preview_url":"https://autoseo.my/preview/x/","go_live_domain":"https://www.x.com.my/"})
    assert (lv.base_path, lv.site_base, lv.live, lv.live_domain) == ("", "https://x.com.my", True, "x.com.my")
    assert g.build_base({"slug":"x","preview_url":"https://autoseo.my/preview/x/","go_live_domain":"x.com.my"}) == ("", "https://x.com.my")
def test_retarget_paths_live():
    lv = g.Cfg({"slug":"x","preview_url":"https://autoseo.my/preview/x/","go_live_domain":"x.com.my"})
    t = '<a href="/preview/x/ms/">BM</a><img src="/preview/x/m.webp" srcset="/preview/x/a.webp 1x"><link rel="canonical" href="https://autoseo.my/preview/x/a/"><a href="https://autoseo.my/">AutoSEO</a><a href="/preview/xy/">other</a>'
    o = g.retarget_paths(t, lv)
    assert "preview/x/" not in o and 'href="/ms/"' in o and 'src="/m.webp"' in o and 'href="https://x.com.my/a/"' in o
    assert 'href="https://autoseo.my/"' in o and "/preview/xy/" in o
    assert g.retarget_paths(o, lv) == o   # idempotent

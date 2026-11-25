import os, sys, json, tempfile
from urllib.parse import urlsplit, parse_qs
sys.path.insert(0, os.path.dirname(__file__))
import shop

def test_wa_roundtrip():
    t = "Hi BIY Home Store, I am interested in Bosch Angle Grinder GWS 7-100ET. https://x.y/p/?a=1&b=2 May I check?"
    u = shop.wa_url("+60125688961", t)
    assert u.startswith("https://wa.me/60125688961?text=")
    assert parse_qs(urlsplit(u).query)["text"][0] == t

def test_index_rule():
    assert not shop.product_indexable({"indexable": True, "status": "active", "images": [], "description": "x"})
    assert shop.product_indexable({"indexable": True, "status": "active", "images": [{"src": "a"}], "specs": [1]})
    assert not shop.product_indexable({"indexable": False, "status": "active", "images": [{"src": "a"}], "specs": [1]})

def test_price_refused():
    d = tempfile.mkdtemp()
    json.dump({"brands_published": ["b"]}, open(os.path.join(d, "facts.json"), "w"))
    json.dump([{"slug": "b", "published": True, "ranges": []}], open(os.path.join(d, "brands.json"), "w"))
    json.dump([{"slug": "c"}], open(os.path.join(d, "categories.json"), "w"))
    json.dump({"products": [{"id": "x", "slug": "x", "status": "active", "brand": "b", "category": "c", "price": 10}]},
              open(os.path.join(d, "products.json"), "w"))
    try:
        shop.load_catalog(d); assert False
    except shop.CatalogError as e:
        assert "price" in str(e)

def test_fill_keeps_unknown():
    assert shop.fill("{a} {b}", a=1) == "1 {b}"

def _feed_dir(url):
    d = tempfile.mkdtemp()
    json.dump({"price_mode": "whatsapp_only", "live_feed": {"url": url, "key_file": os.path.join(d, "k"), "timeout_s": 5, "min_active": 1}},
              open(os.path.join(d, "shop-config.json"), "w"))
    open(os.path.join(d, "k"), "w").write("test")
    json.dump({"type": "object", "required": ["sku", "title", "active", "updated_at"],
               "properties": {"sku": {"type": "string"}, "active": {"type": "boolean"}}}, open(os.path.join(d, "product-feed.schema.json"), "w"))
    json.dump({"feed_version": "s", "products": [{"sku": "SAMPLE-1", "title": "x", "active": True, "is_sample": True, "updated_at": "t"}]},
              open(os.path.join(d, "products.sample.json"), "w"))
    return d

def test_resolver_three_states():
    live = {"feed_version": "v1", "products": [{"sku": "A1", "title": "A", "active": True, "updated_at": "t"}]}
    d = _feed_dir(None)
    assert shop.resolve_products(d)["mode"] == "sample"                                   # not configured
    d = _feed_dir("https://feed.invalid/x")
    assert shop.resolve_products(d, fetch=lambda u, k, t: (404, b""))["mode"] == "sample"  # configured, failing
    assert shop.resolve_products(d, fetch=lambda u, k, t: (200, b'{"products":[]}'))["mode"] == "sample"
    bad = {"products": [{"sku": "A1", "title": "A", "active": True, "updated_at": "t", "is_sample": True}]}
    assert shop.resolve_products(d, fetch=lambda u, k, t: (200, json.dumps(bad).encode()))["mode"] == "sample"
    r = shop.resolve_products(d, fetch=lambda u, k, t: (200, json.dumps(live).encode()))  # live
    assert r["mode"] == "live" and [x["sku"] for x in r["records"]] == ["A1"]
    r = shop.resolve_products(d, fetch=lambda u, k, t: (500, b""))                         # once live, never back to sample
    assert r["mode"] == "live" and r["records"][0]["sku"] == "A1"

def test_real_sku():
    assert shop.real_sku("SAMPLE-X", False) is None and shop.real_sku("A1", True) is None and shop.real_sku("A1", False) == "A1"

if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"): f(); print("ok", k)

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

if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"): f(); print("ok", k)

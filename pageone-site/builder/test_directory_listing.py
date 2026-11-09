"""Unit check for directory_listing.py with a fictional sample. Writes only to a temp dir; never into site/.
Run: python3 builder/test_directory_listing.py"""
import json, os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from directory_listing import listing_page, write_listing

SAMPLE = {
    "name": "Sample Auto Workshop", "trade": "Car workshop", "slug": "sample-auto-workshop", "area": "Yishun",
    "services": ["Servicing", "Brake repair"],
    "hours": [{"label": "Mon to Fri", "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
    "phone": "+65 6000 0000", "whatsapp": "6560000000",
    "photos": [{"src": "https://example.com/p1.jpg", "alt": "Workshop bay", "width": 800, "height": 600}],
    "gbp_url": "https://maps.google.com/?cid=1", "about": "Sample text <b>escaped</b>.",
}
BASE = "https://example-directory.sg"
html = listing_page(SAMPLE, BASE)
blocks = re.findall(r'<script type="application/ld\+json">\n(.*?)\n</script>', html, re.S)
assert len(blocks) == 1
ld = json.loads(blocks[0])
assert ld["@type"] == "LocalBusiness" and ld["url"] == BASE + "/car-workshop/sample-auto-workshop/"
assert not {"aggregateRating", "review"} & set(ld)
assert 'rel="canonical" href="' + ld["url"] + '"' in html
assert 'data-cta="whatsapp_directory_sample-auto-workshop"' in html and "wa.me/6560000000" in html
assert 'href="tel:+6560000000"' in html and "&lt;b&gt;" in html and "<b>escaped" not in html.replace(blocks[0], "")
with tempfile.TemporaryDirectory() as t:
    assert os.path.isfile(write_listing(SAMPLE, BASE, t))
print("directory_listing ok")

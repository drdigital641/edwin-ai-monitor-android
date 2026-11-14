"""Page One shared blocks (15 Nov 2026). One place for the Google review button so a change here
updates every site build. Builders: `from p1_blocks import review_button` (add this folder to sys.path).
Hand-made / Bridge sites: use review-button.html as an Apache SSI include (/inc/review-button.html).

The default output is byte-for-byte the markup that is live today on the SG Garage / Carzy / Fitout /
MyKar footers (13 Nov 2026), so switching a builder to this helper changes no live page.
"""
from html import escape

REVIEW_CSS = """<style>
/* Google review footer button (2026-11-13) */
.p1-foot-review{margin:16px 0 0}
.p1-foot-review a{
  display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;
  min-height:44px;min-width:44px;padding:10px 18px;
  border:1.5px solid currentColor;border-radius:999px;
  text-decoration:none!important;font-weight:700;line-height:1.25;color:inherit
}
.p1-foot-review a:hover{opacity:.88}
footer.foot .p1-foot-review{margin:12px 0 8px}
</style>"""

LABELS = {
    "en": "Leave us a Google review",
    "ms": "Tinggalkan ulasan Google kami",
    "zh": "给我们 Google 评价",
}


def review_button(key, lang="en", label=None, data_ref=None, nofollow=False, with_css=True, href=None):
    """The footer "Leave us a Google review" button.

    key      business key for /review.html?business=KEY (e.g. "edwingarage", "carzyworld")
    href     optional full link instead (e.g. the Google writereview?placeid= URL on sites without a helper page)
    nofollow True adds rel="nofollow" (the review-helper rule asks for it); False = today's live bytes
    """
    if href and not (href.startswith("https://search.google.com/") or href.startswith("https://g.page/") or href.startswith("/review.html")):
        raise ValueError("review href must be a Google review link or /review.html")
    if not href:
        if not key or not str(key).replace("-", "").replace("_", "").isalnum():
            raise ValueError("review key must be letters, digits, - or _")
        href = "/review.html?business=" + key
    rel = "nofollow noopener" if nofollow else "noopener"
    text = escape(label or LABELS.get(lang, LABELS["en"]), quote=False)
    ref = ' data-ref="%s"' % escape(data_ref) if data_ref else ""
    a = '<p class="p1-foot-review"><a href="%s" target="_blank" rel="%s"%s>%s</a></p>' % (escape(href), rel, ref, text)
    return (REVIEW_CSS + "\n" + a) if with_css else a


if __name__ == "__main__":
    # self-test: must equal the live SG Garage article footer block (branch q0c6xt footer.html lines 6-18)
    live = REVIEW_CSS + '\n<p class="p1-foot-review"><a href="/review.html?business=edwingarage" target="_blank" rel="noopener" data-ref="google_review_footer">Leave us a Google review</a></p>'
    assert review_button("edwingarage", data_ref="google_review_footer") == live
    assert 'rel="nofollow noopener"' in review_button("carzyworld", nofollow=True)
    assert "Tinggalkan" in review_button("carzyworld", lang="ms")
    for bad in ['x" onclick="y', "a b", "", "javascript:alert(1)"]:
        try:
            review_button(bad); raise SystemExit("FAIL accepted " + bad)
        except ValueError:
            pass
    try:
        review_button(None, href="javascript:alert(1)"); raise SystemExit("FAIL accepted js href")
    except ValueError:
        pass
    assert "placeid=ChIJ" in review_button(None, href="https://search.google.com/local/writereview?placeid=ChIJx")
    print("p1_blocks self-test: 6 checks passed")

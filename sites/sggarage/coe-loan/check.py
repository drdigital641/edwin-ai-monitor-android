"""Checks for /coe-renewal-loan/: banned wording, schema, FAQ match, CTA. Exit 1 on any problem."""
import json, re, sys, html
from urllib.parse import unquote
p = sys.argv[1] if len(sys.argv) > 1 else "site/coe-renewal-loan/index.html"
h = open(p).read()
bad = []
visible = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", " ", visible))
low = (h).lower()
for w in ["%", "p.a.", "interest", "approval in", "guarantee", "instant", "easy approval", "no rejection", "tenure",
          "instalment", "installment", "dbs", "ocbc", "uob", "maybank", "hsbc", "standard chartered", "citibank", "hong leong",
          "<!--", "placeholder", " hidden", "lender name"]:
    hay = text.lower() if w == "%" else low.replace("%20", "").replace("%2c", "").replace("%22", "").replace("%3a", "").replace("%28", "").replace("%29", "").replace("%2f", "") if w == "%" else low
    if w == "%":
        if "%" in text: bad.append("visible %")
        continue
    if w in low: bad.append("found: " + w)
if re.search(r'style="[^"]*display:\s*none', h): bad.append("hidden inline block")
lds = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]
g = lds[0]["@graph"]
types = [n["@type"] if isinstance(n["@type"], str) else "+".join(n["@type"]) for n in g]
if any(t in ("Offer", "LoanOrCredit", "FinancialProduct") for t in types): bad.append("forbidden schema type")
faq = [n for n in g if n["@type"] == "FAQPage"][0]["mainEntity"]
vis_q = [html.unescape(q) for q in re.findall(r"<summary>(.*?)</summary>", h)]
vis_a = [html.unescape(a) for a in re.findall(r"</summary><p>(.*?)</p></details>", h)]
if [q["name"] for q in faq] != vis_q: bad.append("FAQ questions differ")
if [q["acceptedAnswer"]["text"] for q in faq] != vis_a: bad.append("FAQ answers differ")
if h.count("<h1") != 1: bad.append("h1 count")
t = re.search(r"<title>(.*?)</title>", h).group(1); d = html.unescape(re.search(r'name="description" content="(.*?)"', h).group(1))
if len(d) > 155: bad.append(f"meta {len(d)}")
was = set(re.findall(r'href="(https://wa\.me/[^"]+)"', h))
pre = [unquote(html.unescape(u).split("text=", 1)[1]) for u in was if "text=" in u]
ctas = len(re.findall(r">WhatsApp us for a quote<", h))
print("title", len(t), t); print("meta", len(d)); print("schema", types); print("faq", len(faq)); print("wa ctas", ctas)
print("prefill", sorted(set(pre)))
print("PROBLEMS:", bad or "none"); sys.exit(1 if bad else 0)

"""Page One prices: the ONE place to change the Get Found price.

Builder sources write tokens such as %%PLAN%% instead of a hard-coded price; fill() swaps them
for the real figures when each file is written (pages, llms-full.txt, org-graph.json, llms-results.md).
build.py also copies PLAN into site/main.js (const PLAN_PRICE) and checks that the share image
images/og-<PLAN>.png exists. Boost packs (6 = S$60, 10 = S$100) are not plan-derived and stay as text.
"""

PLAN = 100          # Get Found, S$ per month (Edwin, 11 Nov 2026)
BOOST = 10          # one SEO Boost run, S$
MAX_BOOSTS = 5      # priceRange in schema = plan .. plan + 5 Boosts
DOMAIN_MIN, DOMAIN_MAX = 15, 30   # typical domain cost per year, paid by the client


def _s(n):
    return f"S${n:,}"


TOKENS = {
    "%%PLAN_YEAR_DOMAIN%%": f"{_s(PLAN * 12 + DOMAIN_MIN)}–{PLAN * 12 + DOMAIN_MAX:,}",
    "%%PLAN_YEAR%%": _s(PLAN * 12),
    "%%PLAN_MAX%%": _s(PLAN + MAX_BOOSTS * BOOST),
    "%%PLAN_B1%%": _s(PLAN + 1 * BOOST),
    "%%PLAN_B2%%": _s(PLAN + 2 * BOOST),
    "%%PLAN_B3%%": _s(PLAN + 3 * BOOST),
    "%%PLAN_NUM%%": str(PLAN),
    "%%PLAN%%": _s(PLAN),
}


def fill(text):
    for k, v in TOKENS.items():
        text = text.replace(k, v)
    if "%%PLAN" in text:
        raise SystemExit("price.py: unknown %%PLAN token left in output")
    return text

"""Service page guide copy (audit feedback Edwin shared 4 Nov 2026: service pages were listing-only).

General mechanical knowledge only, the same rule as src/guides.py: no prices, no promises, no claims about any workshop,
no endorsement words (check.py enforces). Each entry: what the job involves, warning signs, what to ask, FAQs, related guides."""

import json as _cj, os as _co
def _content(name):
    """Site content lives in data/content/*.json (Edwin 10 Nov 2026: data-driven site); code only renders it."""
    return _cj.load(open(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "content", name)))
COPY = _content("service_copy.json")

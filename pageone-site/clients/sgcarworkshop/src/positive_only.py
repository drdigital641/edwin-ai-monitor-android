"""Positive-only rule (Edwin 5 Nov 2026): never publish complaints or negative review summaries about any workshop.
Used by finish_batch (strips them on build) and check.py (fails the build if one gets through)."""
import re

# A sentence that reports a complaint, a bad outcome or a single unhappy review.
NEG = re.compile(
    r"\b(one|some|a few|several|other) (review|reviews|customer|customers|reviewer|reviewers|driver|drivers|people)\b[^.]*\b("
    r"report\w*|complain\w*|question\w*|unhappy|disappoint\w*|poor|bad|issue\w*|problem\w*|overcharg\w*|wait\w*|left|criticis\w*|warn\w*|negative)"
    r"|\b(complain\w*|complaint\w*|unhappy|disappoint\w*|dissatisf\w*|overcharg\w*|poor (repair|repairs|workmanship|experience|service|attitude)|"
    r"bad (experience|service|attitude)|rude|dishonest|scam\w*|ripped off|negative review\w*|mixed review\w*|problems? after|"
    r"left (scratches|damage)|scratches left|not (fixed|resolved)|worse than before)\b", re.I)


# Positive phrasings that contain a negative word ("honest prices without overcharging").
OK = re.compile(r"\b(without|no|never|not|instead of) (any )?(overcharg\w*|upsell\w*|hidden costs?|pressure|complaints?)\b|\bproblems? (other shops|a dealer|the dealer)\b", re.I)


def is_neg(s):
    return bool(NEG.search(OK.sub('', s)))


def sentences(t):
    return [s for s in re.split(r'(?<=[.!?])\s+', (t or '').strip()) if s]


def clean(t):
    """Drop every negative sentence; keep the rest word for word."""
    return ' '.join(s for s in sentences(t) if not is_neg(s))


def bad(t):
    return [s for s in sentences(t) if is_neg(s)]


def page_hits(raw):
    """Negative sentences in a built page: visible text plus every attribute value (search index, data-* fields)."""
    import html as _h
    out = []
    parts = [_h.unescape(v) for v in re.findall(r'="([^"]{20,})"', raw)] + [_h.unescape(re.sub(r'<[^>]+>', ' . ', raw))]
    for p in parts:
        for s in re.split(r'(?<=[.!?])\s+|\s{2,}| \. |(?=\bcustomers on google maps mention\b)', p):
            if s and is_neg(s):
                out.append(s.strip()[:160])
    return out

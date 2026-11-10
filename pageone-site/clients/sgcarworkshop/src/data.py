"""Entries for the SG Car Workshop directory (preview). Every fact has a source note in `source`.

Rules (MASTER-RULES 1-4, PLAN.md): verified facts only; if a fact is not in the client's own build files it is left out;
card wording is fresh (never copied from the client's site); no ratings or review schema; no bypass work; no prices
unless confirmed.

tier (PLAN.md "Tiers", Edwin 1 Nov 2026, permanent rule: a premium listing never has less than a free one):
  "free"             Basic: card plus a SHORT profile page (/workshops/<slug>/): one Google photo slot, short text, plain service names,
                     address + Directions, hours, Google rating line (text only), WhatsApp or Call. No gallery, FAQs, service
                     descriptions, prices or carousel placement (those are Verified/Premium)
  "premium"          full page: real photos, job gallery, services, full address, phone, WhatsApp + Call, map, reviews line with
                     source link and date (no rating schema), FAQs, LocalBusiness data
  "premium_leadgen"  everything in premium, plus the business's own website (Page One own-domain clients): badge
                     "Premium", website link as a SECONDARY button below WhatsApp/Call
"""

PAGE_ONE_WA = "6589976612"  # Page One / admin WhatsApp (Edwin, 1 Nov 2026: +65 8997 6612). Not SG Garage's own number.
PAGE_ONE_WA_SHOW = "8997 6612"

import json as _cj, os as _co
def _content(name):
    """Site content lives in data/content/*.json (Edwin 10 Nov 2026: data-driven site); code only renders it."""
    return _cj.load(open(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "content", name)))

CATEGORIES = _content("categories.json")

# Singapore's five URA planning regions (North, North-East, East, West, Central). A region page is built only if a listing covers it.
REGIONS = _content("regions.json")


# Tier names, badges and monthly prices (S$). Edwin set these on 1 Nov 2026. The Verified S$20 is the DIRECTORY Verified listing;
# it is not Page One's older S$20 early-bird SEO plan. Prices live here so they change in one place.
TIERS = _content("tiers.json")
PRICE_NOTE = "Prices are not published: ask us on WhatsApp. Basic is free."  # Edwin 1 Nov 2026: Verified S$20/mo, Premium S$50/mo, internal only

# One clearly labelled example of the free tier, shown only on /list-your-workshop/ (made-up name, not a real business).
FREE_EXAMPLE = _content("free_example.json")

WD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SAT = ["Saturday"]

# Photos: "f" = file in src/img (copied to site/assets/img); "u" = absolute URL hotlinked from the client's own live pages (preview only).
# Prose is written fresh (never copied from the client's site). Prices only where the client's own live page publishes them.

ENTRIES = [{k: v for k, v in _e.items() if k != "_order"} for _e in sorted((_cj.load(open(_f)) for _f in __import__("glob").glob(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "listings", "*.json"))), key=lambda r: r["_order"])]   # paid, Verified and founder listings: one record per listing in data/listings/<slug>.json


# ---- Basic (tier "free") listings: card + short profile page. Source: basic-run/2026-11-01.json (public Google business listings, checked 1 Nov 2026).
# Fields shown on the card: name, desc, category, area + region, WhatsApp (only if a mobile number) or Call, Directions (Google Maps cid).
# ---------------------------------------------------------------------------------------------------------------------
# Basic listings come from data/workshops/<slug>.json (schema: data/schema.json). Only place_id is kept from Google.
# A record is LIVE only when: status == "active", google_screen.passed is true, it has a stored SG mobile (+65 8/9 + 7 digits) with whatsapp true from the
# Google Business Profile (source google_profile + checked_at, Option B, Edwin 2 Nov 2026) or the workshop's own pages (own_site + evidence + source_url), and its place_id
# is not in data/removed.json. Everything shown on a page is built from these fields by build.py templates.
# ---------------------------------------------------------------------------------------------------------------------
import json as _json, os as _os, re as _re

DATA_DIR = _os.environ.get("SGCW_DATA_DIR") or _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data")
MOBILE_RE = _re.compile(r"^\+65[89]\d{7}$")
FORBIDDEN_KEYS = {"rating", "user_rating_count", "reviews", "phone_google", "hours_google", "business_status", "display_name", "formatted_address",
                  "types", "primary_type", "website_uri", "google_maps_uri", "cid", "google_photos", "businessStatus", "displayName",
                  "formattedAddress", "websiteUri", "googleMapsUri", "nationalPhoneNumber"}
_CODES = _json.load(open(_os.path.join(DATA_DIR, "categories.json")))["codes"]


def _jload(name, default):
    p = _os.path.join(DATA_DIR, name)
    return _json.load(open(p)) if _os.path.exists(p) else default


REMOVED = {r["place_id"] if isinstance(r, dict) else r for r in _jload("removed.json", [])}


def workshop_files():
    d = _os.path.join(DATA_DIR, "workshops")
    return sorted(_os.path.join(d, f) for f in _os.listdir(d) if f.endswith(".json")) if _os.path.isdir(d) else []


def record_problems(r):
    """Schema + live-rule problems for one workshop record (check.py prints these; the loader refuses a bad ACTIVE record)."""
    out = []
    for k in ("slug", "place_id", "name", "name_source_url", "address", "postal_code", "address_source_url", "lat", "lng", "geo_source",
              "planning_area", "region", "estate", "categories", "services", "services_source_url", "phones", "google_screen", "status", "tier",
              "first_seen_at", "last_verified_at", "collector_version", "place_id_checked_at"):
        if r.get(k) in (None, "", []) and k not in ("lat", "lng") and not (k == "geo_source" and r.get("status") != "active"):  # coordinates are filled when a passed record is promoted
            out.append("missing " + k)
    if r.get("schema_version") != 1:
        out.append("schema_version must be 1")
    bad = FORBIDDEN_KEYS & set(r)
    if bad:
        out.append("stores Google-only field(s) %s" % sorted(bad))
    if r.get("geo_source") != "onemap" and r.get("status") == "active":
        out.append("geo_source must be onemap")
    if r.get("status") not in ("active", "pending", "closed", "removed"):
        out.append("bad status")
    if r.get("tier") not in ("basic", "verified", "premium"):
        out.append("bad tier")
    for c in r.get("categories", []):
        if c not in _CODES:
            out.append("unknown category " + c)
    mobiles = [p for p in r.get("phones", []) if p.get("kind") == "mobile"]
    for p in r.get("phones", []):
        if p.get("kind") == "mobile" and not MOBILE_RE.match(p.get("e164", "")):
            out.append("mobile not +65 8/9 + 7 digits: %s" % p.get("e164"))
        if p.get("source") not in ("google_profile", "own_site"):
            out.append("phone %s needs source google_profile or own_site" % p.get("e164"))
        if not p.get("checked_at"):
            out.append("phone %s missing checked_at" % p.get("e164"))
        if p.get("source") == "own_site":
            for k in ("evidence", "source_url"):
                if not p.get(k):
                    out.append("own_site phone %s missing %s" % (p.get("e164"), k))
            if not str(p.get("source_url", "")).startswith("http"):
                out.append("own_site phone source_url must be a URL")
    if r.get("status") == "active":
        if not mobiles or not any(p.get("whatsapp") is True for p in mobiles):
            out.append("ACTIVE record needs a mobile with whatsapp true")
        if (r.get("google_screen") or {}).get("passed") is not True:
            out.append("ACTIVE record has not passed the Google screen")
        if r.get("place_id") in REMOVED:
            out.append("place_id is in removed.json")
    return out


def _from_record(r):
    m = [p for p in r["phones"] if p["kind"] == "mobile" and p.get("whatsapp")][0]
    a = r["address"]
    street = ", ".join(x for x in [(" ".join(x for x in [a.get("block"), a.get("street")] if x)), a.get("building")] if x)
    addr_public = "%s%s, Singapore %s" % (street, (", " + a["unit"]) if a.get("unit") else "", r["postal_code"])
    import areas as _ar
    cat = _CODES[r["categories"][0]]
    est = r["estate"]
    return dict(
        slug=r["slug"], place_id=r["place_id"], name=r["name"], tier="free", category=cat, categories=[_CODES[c] for c in r["categories"]],
        blocks=r.get("blocks") or None, google_rating=r.get("google_rating"),
        estate=est, locality=r.get("locality"), area_label=r.get("locality") or _ar.TOWNS[_ar.ESTATES[est]["town"]]["name"], regions=[r["region"]], region=r["region"], planning_area=r["planning_area"],
        address_public=addr_public, street=street, postal=r["postal_code"], addresses=[dict(label=None, street=street, postal=r["postal_code"])],
        lat=r["lat"], lon=r["lng"], services_public=list(r["services"]), services=[], services_source=r["services_source_url"],
        phone=m["e164"], phone_show="%s %s" % (m["e164"][3:7], m["e164"][7:]), whatsapp=m["e164"].lstrip("+"), contact_source=m.get("source_url") or "google_profile",
        contact_evidence=m.get("evidence") or "Google Business Profile", contact_checked=m["checked_at"],
        website_url=r.get("website_url"), facebook_url=r.get("facebook_url"), instagram_url=r.get("instagram_url"), email=r.get("email"),
        hours=(r.get("hours") or {}).get("text"), hours_source=r.get("hours_source_url"), name_source=r["name_source_url"], address_source=r["address_source_url"],
        uen=r.get("uen"), last_verified=r["last_verified_at"], regions_note="Region from the planning area (URA).")


BASIC = []
PENDING_RECORDS = []
for _f in workshop_files():
    _r = _json.load(open(_f))
    if _r.get("status") != "active":
        PENDING_RECORDS.append(_r)
        continue
    _p = record_problems(_r)
    if _p:
        raise SystemExit("data/workshops/%s: %s" % (_os.path.basename(_f), "; ".join(_p)))
    BASIC.append(_from_record(_r))
ENTRIES.extend(BASIC)


_paid = lambda e: e["tier"] == "premium_leadgen"
ENTRIES.sort(key=lambda e: (0 if _paid(e) else 1, "" if _paid(e) else e["name"].lower()))  # Premium, Verified, then Basic A to Z (paid keep their set order)


# One shared tag list: tag every card and refile out of general servicing where customer mentions clearly support a specific service (tags.py).
import tags as _tg
REFILED = _tg.apply(ENTRIES, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data", "pilot"))
# Tyre shops (Edwin 7 Nov 2026): filed under car-tyres only where the Google listing or the shop's own website clearly shows tyre work (data/tyre_shops.json).
TYRE_SHOPS = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "data", "tyre_shops.json")))["shops"]
for _e in ENTRIES:
    if _e["slug"] in TYRE_SHOPS and "car-tyres" not in _e.get("categories", [_e["category"]]):
        _e["categories"] = list(_e.get("categories", [_e["category"]])) + ["car-tyres"]

#!/usr/bin/env python3
"""Permanent registry of every workshop ever built or rejected (Edwin, 3 Nov 2026). data/registry.json holds ONLY:
place_id, slug, name_norm, postal_code, mobile, status, date. Never delete entries: a rejected or removed workshop must never be looked up again.
Statuses: built | rejected-no-mobile | rejected-not-car-repair | closed | removed-on-request.
Candidate check (before ANY Places call or build): match by place_id, by mobile, or by normalised name + postal code. A match = skip and log."""
import json, os, re, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get('SGCW_DATA_DIR') or os.path.join(HERE, '..', 'data')
STATUSES = ('built', 'rejected-no-mobile', 'rejected-not-car-repair', 'closed', 'removed-on-request')
MOBILE_RE = re.compile(r'^\+65[89]\d{7}$')
STOP = {'pte', 'ltd', 'private', 'limited', 'singapore', 'sg', 'the', 'and', 'co', 'company', 'enterprise', 'enterprises'}


def norm_name(n):
    t = re.sub(r'[^a-z0-9]+', ' ', (n or '').lower().replace('&', ' and ')).split()
    return ' '.join(w for w in t if w not in STOP)


def path():
    return os.path.join(DATA, 'registry.json')


def load():
    return json.load(open(path())) if os.path.exists(path()) else []


def save(reg):
    json.dump(reg, open(path(), 'w'), indent=1, ensure_ascii=False)


def match(reg, place_id=None, mobile=None, name=None, postal=None):
    """Return (entry, why) for the first registry entry the candidate matches, else (None, None)."""
    nn = norm_name(name) if name else None
    for e in reg:
        if place_id and e.get('place_id') == place_id: return e, 'place_id'
        if nn and postal and e.get('name_norm') == nn and e.get('postal_code') == str(postal): return e, 'name+postal'
    return None, None


def add(reg, place_id, slug, name, postal, mobile, status, date=None):
    assert status in STATUSES, status
    for e in reg:   # one entry per place_id: update its status, never duplicate
        if place_id and e.get('place_id') == place_id:
            e.update(slug=slug or e['slug'], status=status, date=date or e['date'])
            if mobile: e['mobile'] = mobile
            return e
    e = dict(place_id=place_id, slug=slug, name_norm=norm_name(name), postal_code=str(postal or ''), mobile=mobile, status=status, date=date or dt.date.today().isoformat())
    reg.append(e); return e


def sync_built(entries, date=None):
    """Mark every live directory entry as built (adds the missing ones). Run after each build."""
    reg = load(); n = 0
    for e in entries:
        if any(x['slug'] == e['slug'] and x['status'] == 'built' for x in reg): continue
        postal = e.get('postal') or ((e.get('addresses') or [{}])[0].get('postal'))
        add_by_slug(reg, e['slug'], e.get('place_id'), e['name'], postal, e.get('phone'), date); n += 1
    save(reg); return n


def add_by_slug(reg, slug, place_id, name, postal, mobile, date):
    for x in reg:
        if x['slug'] == slug:
            x.update(status='built', mobile=mobile or x.get('mobile'), place_id=place_id or x.get('place_id')); return
    if place_id:
        add(reg, place_id, slug, name, postal, mobile, 'built', date)
    else:
        reg.append(dict(place_id=None, slug=slug, name_norm=norm_name(name), postal_code=str(postal or ''), mobile=mobile, status='built', date=date or dt.date.today().isoformat()))

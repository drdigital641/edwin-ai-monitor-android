# Workshop fact files (Edwin, 2 Nov 2026, 11:12pm)

One file per workshop: data/facts/<slug>.json, mirrored to /mnt/project-files/sgcarworkshop/facts/<slug>.json for Site Ops.
Sources allowed: the workshop's own website, public logged-out Facebook/Instagram views, SGCarMart, Carousell, the Singapore Motor Workshop Association directory, the company register (ACRA/BizFile public data), our stored Google data.
Never log in, message, follow, like, comment or contact a workshop. No photos (Basic has none). Invent nothing.

Schema:
{
 "slug": "...", "researched_at": "YYYY-MM-DD", "researcher": "Claude (Sonnet)",
 "facts": [ {"field": "services|specialties|makes|established|payment|booking|address|other", "value": "...", "source_url": "https://...", "retrieved": "YYYY-MM-DD"} ],
 "conflicts": [ {"field": "...", "values": [{"value": "...", "source_url": "..."}], "note": "not used on the page"} ],
 "not_found": ["website", "warranty", "payment methods", ...],
 "phone_rule": "Phone = the stored Google mobile only; other numbers are never published."
}
Rules: every fact has a source_url; conflicting or unconfirmable facts go in conflicts/not_found and are not used; no ratings, review quotes, staff names or second numbers.
Pilot design is NOT approved: researching and queuing only, nothing published from these files until Edwin approves.

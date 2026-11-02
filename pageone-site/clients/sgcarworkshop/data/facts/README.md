# Workshop fact files (Edwin, 2 Nov 2026, 11:12pm)

One file per workshop: data/facts/<slug>.json, mirrored to /mnt/project-files/sgcarworkshop/facts/<slug>.json for Site Ops.
Sources allowed: the workshop's own website, public logged-out Facebook/Instagram views, SGCarMart, Carousell, the Singapore Motor Workshop Association directory, the company register (ACRA/BizFile public data), our stored Google data.
Never log in, message, follow, like, comment or contact a workshop. No photos (Basic has none). Invent nothing.

Schema:
{
 "slug": "...", "researched_at": "YYYY-MM-DD", "researcher": "Claude (Sonnet)",
 "facts": [ {"field": "services|specialties|makes|established|payment|booking|address|other", "value": "...", "source_url": "https://...", "retrieved": "YYYY-MM-DD"} ],
 "conflicts": [ {"field": "...", "values": [{"value": "...", "source_url": "..."}], "note": "not used on the page"} ],
"stories": [ {"title": "...", "car": "...", "problem": "...", "action": "...", "job_date": "YYYY-MM-DD or null", "source_url": "https://... (the workshop's own public post)", "retrieved": "YYYY-MM-DD", "notes": "..."} ],
 "not_found": ["website", "warranty", "payment methods", ...],
 "phone_rule": "Phone = the stored Google mobile only; other numbers are never published."
}
Rules: every fact has a source_url; conflicting or unconfirmable facts go in conflicts/not_found and are not used; no ratings, review quotes, staff names or second numbers.
Pilot design is NOT approved: researching and queuing only, nothing published from these files until Edwin approves.

STORIES (Edwin, 2 Nov 2026, "Do not invent stories"): collect up to 2 REAL job stories per workshop, only from the workshop's own public posts (its website, logged-out Facebook or Instagram, SGCarMart). Save each under "stories" with its source_url and date. On the page: our own words in 2 or 3 short sentences (car, problem, what they did) with a link to the original post. No photos, no customer names, no car plates. Never invent, embellish or combine stories. General advice articles are not stories. If no real story exists, "stories" is empty and the page leaves the section out entirely.

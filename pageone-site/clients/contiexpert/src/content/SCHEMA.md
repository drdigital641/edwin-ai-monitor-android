# Content module schema (for helper writers)

Write plain Python 3 files that define lists of dicts. No imports. Use double-quoted or triple-quoted strings.
HTML allowed inside "html"/"a" strings: <p> <ul> <ol> <li> <strong> <em> <h3> <table><thead><tbody><tr><th><td> <a href="..."> only.
Internal links are root-relative and MUST be one of the URLs below (the build rewrites them for preview).

## Site URLs (only link to these)
/                                   home
/services/                          services hub
/services/european-car-servicing/
/services/car-diagnostics-warning-lights/
/services/car-aircon-repair/
/services/brake-suspension-repair/
/services/gearbox-transmission-service/
/services/hybrid-ev-servicing/
/services/pre-purchase-inspection/
/brands/mercedes-benz/
/brands/bmw/
/brands/audi-volkswagen/
/areas-we-serve/                    drivers within 10 km of Newton Circus
/contact-us/                        address, map, WhatsApp
/faqs/
/article/                           guides hub
/bmw-check-engine-light-singapore/
/mercedes-engine-overheating-singapore/
/audi-aircon-not-cold-repair-singapore/
/european-car-service-schedule-singapore/
/dealer-vs-independent-workshop-singapore/
/pre-purchase-car-inspection-singapore-your-ultimate-guide-to-buying-with-confidence/

## Page dict
{
  "slug": "european-car-servicing",          # last path segment
  "name": "European Car Servicing",          # short name for cards/nav
  "card": "1-2 sentence card text, under 30 words.",
  "title": "<= 58 chars, main term first, ends with ' | Volt Autocare'",
  "desc": "meta description 120-155 chars",
  "h1": "page H1",
  "answer": "40-60 word direct answer paragraph that opens the page (plain text, no HTML)",
  "sections": [ {"h2": "Question-style heading", "html": "<p>...</p>"} ],   # 4-7 sections
  "faqs": [ {"q": "...?", "a": "plain text 30-70 words"} ],               # exactly 4
  "related": ["/url/", "/url/"],          # 2-4 internal URLs from the list
  "confirm": ["things the client must confirm before this page goes live"]
}
Articles add: "date": "2026-11-03", "service": "/services/<owner>/" (owner page URL), "minutes": int read time, "brand" optional.

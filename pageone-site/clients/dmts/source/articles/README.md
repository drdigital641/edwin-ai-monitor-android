# Jacky Gearbox articles (jackygearbox.com/articles/)

One file per article: `<slug>.md`. The slug becomes the URL. build.py turns every file here into a page,
adds it to the Articles hub, footer, sitemap and llms.txt, and makes its share image.

Who writes them: the daily 8pm EDGE run (one article per run, Edwin's permanent rule, 14 Oct 2026),
using the EDGE Loop: pick a long-tail query no existing page owns, tear down the current top 10, then
write the page that covers what they cover plus what they miss, with Singapore detail.

Header (key: value lines, then a line with only ---):
- title (under 65 chars), desc (under 160), h1, short (2-5 words, footer link), date (YYYY-MM-DD)
- img: photo-name|alt text (a photo in site/img/, e.g. gearbox-teardown, atf-fluids, diagnostics)
- services, problems: comma-separated slugs that exist in build.py

Body: "## " / "### " headings, "- " lists, paragraphs, **bold**, [text](/path/) links to our own pages.
End with "## Questions" then Q: / A: lines (one line each) for the FAQ block and schema.

Fact rules (client):
- Jacky is the sole persona: he diagnoses, tests, inspects and road-tests; the workshop team does the repair.
- No new prices, durations, review counts, years or results. Only S$30 diagnostic, 6-month warranty,
  free towing in office hours, one number 8430 9665.
- No DMTS / Dynamic Motoring name, no email, no other workshops named.
- General gearbox facts only, hedged where makers differ ("follow your car maker's schedule").

Publish: rebuild (python3 build.py), commit to claude/dmts-launch-check, then list the changed files in the
Bluehost Bridge app's base44/shared/clientAssets.ts (pinned commit + sha256), redeploy
publishPageOneArticles and run its workflow.

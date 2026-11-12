# Maison articles: data format (12 Nov 2026)

One file per article: `data/articles/<slug>.json`. `python3 build.py` renders it with the shared template
(articles.py: site head/header/footer/CTA, Article + BreadcrumbList + FAQPage schema), adds it to the
/articles/ hub, sitemap.xml and llms.txt. The build stops and lists every problem; nothing is built on a failure.

Fields (all required unless marked optional):
- slug: lower-case words joined by - (also the file name)
- date_published: YYYY-MM-DD (SGT); date_modified optional, only when the content really changed
- title: max 70 characters, contains `keyword`; ends " | Maison"
- description: 110 to 160 characters
- keyword: one search phrase; must appear in title, h1 and lead
- eyebrow: short topic label
- h1: ["plain part", "italic part"]
- lead: first paragraph, plain text
- hero: {src, alt, w, h, caption?}; src = an image the site already uses (a wp-content name from build.py, or /img/... /images/... path)
- sections: [{h2, p?: [..], list?: [..], steps?: [[title, text], ..], p_after?: [..]}]
- related: [["services/bto-renovation/", "label"], ..] at least 2 internal links to real pages
- faq: [[question, answer], ..] at least 3
- wa_text: WhatsApp prefill
- sources: optional [[name, url], ..] for any outside fact (official pages only)

Content rules (Edwin 12 Nov 2026): topics only from Maison's real services, reviews and new-launch pages; real facts
only. Never: prices or money amounts, guarantees or promises, invented results, property selling, prices, yields or
investment advice for any project (CEA), appointed-designer claims. The build blocks these words. Plain text only.

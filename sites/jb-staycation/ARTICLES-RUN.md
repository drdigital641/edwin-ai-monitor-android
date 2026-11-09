# JB Staycations night article run (Edwin, 9 Nov 2026)

Site: https://jbstaycations.com (docroot = Bluehost folder preview/jb-staycation of site "pageone").
Cadence: 1 article every 2 days, EVEN SGT nights, in the 01:05 SGT night run (scheduled task "Page One night run").
ContiExpert runs on odd nights, so there is no clash. Run JB after the other even-night sites; it needs no Base44 credits.

## 0. Gate: the content plan (HARD RULE)
- Topics come ONLY from the content plan, strictly in order: /mnt/project-files/jb-staycation/content-plan.md
  (Website Manager's copy is /workspace/clients/jb-staycation/seo/content-plan.md; Edwin pastes it into the
  "Launch JB Staycations site" thread and it is saved to the path above).
- If the plan file is missing, or every row is done: SKIP. Write "skipped: no content plan" (or "plan finished")
  in the run summary and append one line to /mnt/project-files/jb-staycation/article-log.md. Never invent a topic.
- Take the first plan row not yet in article-log.md. One article per even night. Edwin (9 Nov): use the plan's topics strictly
  in order on the EVEN-night run; the plan's own dates (13, 15, 17 Nov...) are indicative only, the even-night slot wins.
- Slot 0: no article until the tech SEO brief (9 Nov) is live (check memory jb-staycation-site / thread "Launch JB Staycations site").
- Follow the plan's keyword OWNERSHIP MAP: never target a keyword owned by /, /stays/, a house page, /prices/, /getting-there/ or an existing article.
- Proof gate: fewer than 2 real proof items = skip the slot and log it. Re-check Google SG page 1 for the keyword (web search) before writing.
- Conditional rows: #7 only after the MOM + Johor 2027 holiday lists are published; #8 only if LTA has an official RTS opening date and fares (else skip, move #9 up).
- HOLD (Edwin 9 Nov): never state a 24/25 Dec nightly rate (PH or not) until Edwin confirms with Daniel; say "WhatsApp Daniel for Christmas Eve and Christmas Day rates". The 2-night minimum over Christmas Eve and Christmas Day is a confirmed fact.
- Author stays the Organization "JB Staycations" (no Person author unless Edwin approves).
- Dict keys for plan rows: also set 'next': (anchor, path) to the next spoke once it exists (the build adds the link), and the build adds a WhatsApp CTA after the intro and at the end.

## 1. Facts (only these; anything else = leave it out)
- Prima: Taman Nusantara Prima, Gelang Patah, Iskandar Puteri; up to 12 guests (never more); 3 rooms, each 1 queen + 2 single floor mattresses; ground-floor bedroom for elderly guests; 7ft pool table; mahjong; parking 2 inside + 6 outside; about 10 min from Tuas Second Link (host estimate).
- Landak Kawan Fun House: Taman Abad; up to 10 guests; 3 bedrooms, 5 beds; 8ft pool table, foosball, 2 dart boards, mahjong, TV arcade, kids playroom, workstation; about 5-min walk to KSL City Mall; about 12 min from Causeway CIQ (host estimate).
- Prices per night, whole house, cleaning included: Prima RM 450 weekday / RM 650 weekend / RM 750 public holiday; Landak RM 550 / RM 750 / RM 1,000. Use the build.py helpers (tiers_full, PP_WEEKDAY, DEPOSIT, PAY) instead of typing figures.
- RM 1,000 refundable deposit, returned within 48 hours after checkout. Check-in 3pm, check-out 11am. Quiet hours 11pm-7am. RM 500 only as the indoor smoking/vaping/durian penalty.
- Host: Daniel only (never any other name). WhatsApp +65 9006 2198.
- Drive/walk times: ONLY from AROUND in build.py / the house pages' "Around the house" notes, always "about" + "host estimate".
- BANNED: karaoke, BBQ, swimming pool, party/parties, event/events, Woon, "20 guests", HitPay, smoke alarm, invented reviews/prices/times/opening hours. Say "gatherings".
- Every article carries at least 2 PROOF ITEMS: a real house photo already on the site (STAYS_IMG / PAGE_IMG filename), a real price, a real host drive time, or a real FAQ answer from FAQS.

## 2. Write it (source only, never hand-edit HTML)
1. git fetch; check out branch claude/project-thread-ids6hl (or the newest JB branch named in memory jb-staycation-site) and copy sites/jb-staycation/build.py + review_helper.py over /mnt/project-files/jb-staycation/ only if the repo copy is newer.
2. Append one dict to ARTICLES in /mnt/project-files/jb-staycation/build.py:
   slug, date (SGT YYYY-MM-DD of the run), title, ttl (<=60 chars, unique), desc (<=155 chars, keyword first), h1 (contains the keyword),
   answer (40-60 words, plain text), house ('prima' or 'landak'), photo (an existing real photo filename), optional wa,
   sections [(h2, [paragraphs])] with links to {R}stays/<house slug>/ and {R}prices/, and faqs [(q, a)] x 3-5.
   The build adds: Article schema with that date, FAQPage schema, hub + /stays/ links, WhatsApp CTA, hub card (newest first), sitemap lastmod = date, llms.txt line.
3. Do NOT change TODAY for other pages, the CSS, the hero images or any other copy.
4. Build: JB_OUT=<scratch> python3 build.py; JB_OUT=<scratch> python3 check.py (0 bad); JB_OUT=<scratch> python3 wa_check.py; text-scan the new page for the banned words; overflow check 360/390/412/1280.
5. Copy into the repo: for each top-level item of <scratch> except img/ and thumb/: replace sites/jb-staycation/site/<item>; mirror the same into sites/jb-staycation/deploy/pages (no img/thumb). Never copy img/ (keeps the AI hero byte-identical: sha 456406d0/afb7cb55/0ee2f9ed).
6. Commit (source, then pages) with the Claude trailers, push, Bluehost Bridge invoke_sync_from_github site pageone, source_path sites/jb-staycation/deploy/pages, base_path preview/jb-staycation, ref = full SHA, exclude ["htaccess.txt"].
7. Verify live from the Base44 sandbox (app 6ac6d47b4ec84148578914c7): new URL 200, one H1, jb.css?v= matches the build, hero sha unchanged.
8. IndexNow from the same sandbox: host jbstaycations.com, key 8902a563f0e8890158ac4cf1b41cd50d, keyLocation https://jbstaycations.com/8902a563f0e8890158ac4cf1b41cd50d.txt, URLs = new article + /articles/ + /sitemap.xml pages changed.
9. Append to article-log.md: date | plan row | slug | commit | IndexNow status. Write the JB EdgeDailyLog (Controller) with the article title on article nights only.

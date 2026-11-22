# XADO image gate fix (23 Nov 2026)

Job: Bluehost Bridge IMAGE GATE refused preview/xado/articles/what-is-xado-brand-meaning-origin.html (422, BridgeLog 6b031841, 22 Nov 16:28Z) naming the "Keep reading" card sg-traffic.jpg as the hero.

## Root cause
The 22 Nov hero-detection change (stripChrome) removed every `<header>` block. XADO's article template keeps the H1 and the real hero `<img fetchpriority="high">` inside `<header class="art-hero">`, so the hero was deleted before detection and the gate fell through to the first image after the H1 that was left: the "Keep reading" card (class `rels`/`rel`, heading "Keep reading"), which cutRelated did not recognise. The slug-name and reused-photo rules then ran against the card photo.

The slug-name and reused-photo rules were already applied only to hero/og:image/twitter:image; the bug was hero mis-detection. Live-domain URLs (https://xado-shop.sg/...) already resolve to preview/xado/ files (checkUrl tries prefix + path), and a page-relative hero resolves too: no change needed there, both tested.

## Change (imageGate.ts only)
1. A `<header>` that contains the H1 is the article header and is kept; site header/nav/footer/aside are still stripped.
2. Related-card blocks also match whole-token class `rel`/`rels` and headings "Keep reading", "Read more", "Further reading".
3. Related cards are cut before every hero step (fetchpriority, hero class, fallback), so a card photo can never be read as the hero.

## Tests (Bridge sandbox, deno)
- Synthetic XADO draft (live 20 Nov template, slug swapped): absolute live-domain hero PASS; page-relative ../images/articles/<slug>.jpg PASS; hero swapped to sg-traffic.jpg FAIL (not own image + reused on hub); hero removed FAIL (hero missing).
- Regression: old vs new heroImg on 51 live article pages across 14 sites (sggarage, planwithben, pageone, xado, ktech, urbaneco, danny, alicia, maison, hx, benzworld, sgcarworkshop, cchauto, jayven): 47 identical; 4 differ, all XADO, now reading the real hero instead of sg-traffic.jpg / a card.

## Security / privacy
No new I/O, hosts, secrets or permissions. Gate cannot be loosened by this: hero must still be slug-named (or media.base44.com), a real image file on this site, and not used on the hub. Worst case of a false "article header" keep is that logo-like images are considered, which SKIP_IMG already filters.

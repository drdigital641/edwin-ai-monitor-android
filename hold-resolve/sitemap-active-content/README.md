# Sitemap active-content check (SPO LOW follow-up): DIFF ONLY, NOT SAVED

Task "SITEMAP OVERRIDE SAVE 1114-2240", second part. This is a follow-up to the generated-file override, which was
saved 14 Nov 2026 ~10:58pm SGT as Bridge git 38e9ed2 (checkpoint 6af87609cb12153a1c0fbd0e).
Nothing here is saved in any Base44 app. It waits for the SPO review and then Edwin's "save".

## Files
- `active-content.diff`: against Bluehost Bridge app 6ac6d47b4ec84148578914c7, /app at git 38e9ed2
  (`git apply` in /app; changes 1 file and adds 1 test file).
- `sitemapActiveContent.test.ts`: the new test file (also inside the diff).
- `test-run.txt`, `MD5SUMS`.

## What changes (base44/shared/liveGuard.ts, xmlProblem only)
xmlProblem now also refuses the following in sitemap.xml:
- **Blocked elements:** any element whose local name (after any `prefix:`), in any letter case, is `script`, `iframe`,
  `object` or `embed`. This includes the root element.
- **Event-handler attributes:** any attribute whose local name starts with `on`, in any case and any namespace,
  for example `onload` or `xhtml:onload`.
  - Attribute names are read from complete `name="value"` pairs, so a URL such as `?online=1` inside a value is not
    read as an attribute.
  - `xmlns` and `xmlns:prefix` declarations are exempt, because they only declare a prefix.
- **`javascript:` anywhere in the file:** in any case, and with whitespace or control characters between the letters.
  It is checked both in the raw text and after decoding numeric (`&#106;`, `&#x3A;`) and named
  (`&colon;`, `&tab;`, `&newline;`) character references. This covers values, text, CDATA and comments.

`xhtml:link` (hreflang alternates) stays allowed. Look-alike names also stay allowed, for example `scripture`,
`objects`, `embedded`, `iframes`, and URLs such as `/javascript-basics/` or `?onload=2`.

## What does NOT change
- sitemap.txt, llms.txt and the paths the override covers stay as they are.
- The `publisher` flag wiring stays as it is.
- All the other guard checks stay as they are.

## Checks run (Bridge sandbox COPY /tmp/pc of /app at 38e9ed2; /app untouched and clean)
- Full suite: 45 passed, 0 failed (40 existing + 5 new tests).
- The 6 repo source sitemaps (Page One root, Star, Klar, CSKA, Jacky, Ben) all pass the new check.
  Ben's sitemap has 94 `xhtml:link` hreflang lines.

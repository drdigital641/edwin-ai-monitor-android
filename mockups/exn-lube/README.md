# EXN Lube - new exnlube.com (Page One preview)

Preview: https://pageonesingapore.com/preview/exn-lube/ (hidden from Google by the parent preview X-Robots-Tag header; canonicals/sitemap name exnlube.com so go-live edits nothing).
Source: repo mockups/exn-lube on branch claude/project-thread-fhaasi. Rebuild: `python3 build.py` then `python3 check.py`, commit, Bridge `sync_from_github` site=pageone source_path=mockups/exn-lube/site base_path=preview/exn-lube.
Header/footer/nav live only in build.py shell(). Tap tracker site slug: exn-lube.

## Why the old site loses
exnlube.com is a Create React App shell: every URL (even /sitemap.xml) returns the same 267-char page titled "Exnlube"; no text, no links, no schema, no sitemap, content loaded by JavaScript only. Meta says "industries in Malaysia".

## Fact sources (nothing invented)
- EXN corporate deck (Messe Frankfurt download 2025), Automechanika Dubai exhibitor page, YouTube @exnlube.official about.
- Product grades/specs/pack sizes and bottle photos: KohDen (EXN Singapore distributor) store, read 3 Nov 2026; images hotlinked from kohden.com.sg; other images hotlinked from exnlube.com/static/media.

## Open questions for Edwin / EXN
1. Who is the client: EXN Malaysia (brand site, built) or a Singapore seller.
2. WhatsApp number (WA in build.py; empty = call/email only).
3. Google Business Profile of EXN (name/address/phone must match; Place ID for the Google Review Helper page, not built yet).
4. Carios Molytech base oil: exhibitor page says "Synthetic Esters", KohDen lists "semi-synthetic". Site currently says neither.
5. Grades/specs for Motios, HDDEO, industrial, marine, grease, Garios (not in any source).
6. Store locator data (700+ outlets) for a real Where to buy list; Facebook URL; founding year check (reg. no. 2012 vs "established 2015").
7. Real favicon from EXN logo (current favicon is a placeholder "EXN" mark); own-hosted product photos at go-live.
8. Domain/DNS and plan/price.

# Shared sliding carousel (15 Nov 2026)

Wrapstar-style glide, as one shared file pair for every site: `p1-carousel.js` (10.8 KB, about 6 KB minified) and `p1-carousel.css` (3 KB). Markup to copy: `carousel.html`.

## How it behaves
- Slides on its own, nonstop, as a seamless loop (cards are cloned once, clones hidden from screen readers).
- Vertical page scrolling never stops it, even when the finger starts on the carousel.
- Only press-and-hold (about 0.25 s) or a sideways drag pauses it. It starts again 1.5 s after release.
- A quick tap does not pause it, and hovering does not pause it.
- Fingers and mouse slide it 1:1, left and right, and the page does not move sideways. A drag never opens the card link under it.
- Arrows and dots are always visible (44 px touch targets). Keyboard focus pauses it until focus leaves.
- Every card is one uniform frame (set by `--p1c-ratio`), photos fill it with object-fit: cover.
- prefers-reduced-motion: no auto-slide, a plain swipe row with the same arrows and dots.
- No JavaScript: a plain swipe row, no dead buttons.

## Changes from Wrapstar's ws.js
- Resume time 3 s -> 1.5 s (Edwin's brief).
- Moves the track with transform instead of scrollLeft, so the slide is smoother and 1:1 drag is exact.
- Touch decided on the first 6 px (sideways = slide, vertical = page), per the 3 Nov rule.
- Adds arrows, dots and keyboard pause (design guide 0.11 and 7).

## Conflict with the design guide
House rule 0.11 (12 Nov) says carousels pause on hover too. Edwin's 14 Nov brief says only hold or sideways drag pauses. The template follows the 14 Nov brief. `data-hover-pause="1"` on a carousel turns hover pause on if Edwin wants rule 0.11 back.

## Per site
The look comes from each site's own CSS variables (`--p1c-card`, `--p1c-gap`, `--p1c-ratio`, `--p1c-radius`, `--p1c-accent`), so the visible design stays different per site. Add `?v=<hash>` to both files (Bluehost caches CSS/JS for a year).

## Tests
`node test.js` (Playwright, real touch events through Chrome DevTools): 42 passed, 0 failed, run 3 times. Output in `test-output.txt`. Covers auto-slide, vertical swipe, hold, tap, 1:1 drag, diagonal drag, resume timing, mouse hold/drag/hover/wheel, keyboard, uniform frames, arrows/dots, 360/390/412 px no sideways scroll, reduced motion and no-JS.

Not rolled out to any site.

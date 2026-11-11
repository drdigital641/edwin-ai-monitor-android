# New-launch page data format

Every project page at `/new-launches/<slug>/` is built from **one JSON file**:
`data/new-launches/<slug>.json`. The page layout lives in one place (`newlaunch.py`, styles in `mid.css`),
and the header, footer, breadcrumb, WhatsApp button and schema come from the shared helpers in `build.py`.
Change the template once and every project page changes on the next build.

The build writes fully rendered HTML (no JavaScript is needed to see any content), and adds every project to
the `/new-launches/` hub, `sitemap.xml` and `llms.txt`.

A complete real example: [`new-launch-example.json`](new-launch-example.json) (Norwood Grand, with concept
renders, floor plans and unit tips).

## Commands

```
python3 build.py                        # build the whole site into ./site
python3 build.py --check  FOLDER        # check a folder of packs or JSON files, build nothing
python3 build.py --add-batch FOLDER     # convert + check, save to data/new-launches/, then build the site
```

`FOLDER` can hold JSON files (`<slug>.json`), light project packs (`<slug>/page.md` or `<slug>.md`), or both.
`INDEX.md` and `README.md` are skipped. Packs are converted to JSON first (see "Light packs" below).
If any file has a problem, the build **stops and lists every problem**, and nothing is built or copied.
A slug that already exists is replaced, and the command says which ones it replaced.

After a build, upload the **contents of `site/`** to the site folder. Never upload a `.htaccess`.

## Required fields

| Field | What it is |
|---|---|
| `name` | Project name as people search it, e.g. `"Norwood Grand"` |
| `slug` | URL part, lower case with hyphens. Must match the file name: `norwood-grand.json` |
| `type` | One of `Condo`, `EC`, `BTO`, `HDB`, `Landed`, `Commercial` (drives the hub filter) |
| `area` | Town or neighbourhood shown on the page, e.g. `"Woodlands"` |
| `region` | One of `Central`, `East`, `North`, `North-East`, `West` (used for nearby projects) |
| `developer` | Developer or agency. Use `""` if not confirmed |
| `tenure` | e.g. `"99-year lease from 18 December 2023"`. `""` if not confirmed |
| `top` | TOP, completion or launch date wording. Keep "expected", "indicative", "unconfirmed" as written. `""` if none |
| `unit_mix` | Unit types / sizes. `""` if not confirmed |
| `official_site` | Full URL of the official project page, or `""` |
| `sources` | List of `{"label", "url"}` (optional `"nofollow": true` for third-party or PDF links) |
| `nearby_hints` | List of slugs to show first under "Nearby projects" (can be `[]`) |
| `intro` | First paragraph(s), markdown. Must contain `keywords[0]` |
| `faq` | List of `{"q", "a"}`; answers are markdown |
| `keywords` | List. `keywords[0]` must appear in the title, the H1 and the first intro paragraph |

A blank fact (`""`, or the older `"Not confirmed"`) is kept in the data but **never shown**, so no empty rows
or headings appear. Never fill a blank with a guess.

## Optional fields

| Field | What it does |
|---|---|
| `label` | Type wording shown on the page, e.g. `"Private condominium"`, `"HDB BTO"` |
| `district` | Postal district (`"D11"`) or HDB town (`"Kallang/Whampoa"`); first choice for nearby cards |
| `top_label` | Label for the `top` row (default `TOP`), e.g. `"Launch / TOP / key date"` |
| `facts` | Extra fact rows: `{"label", "value"}` (optional `link_label`, `link_url`) |
| `facts_note` | Short markdown note under the facts (e.g. "not officially confirmed" wording) |
| `title` | SEO title. Default: `<Name> Renovation & Interior Design \| <area> \| Maison` |
| `description` | Meta description, **155 characters or fewer** (checked) |
| `whatsapp_text` / `hero_whatsapp_text` | WhatsApp prefill text. Default names the project |
| `hero` | Image object for the top of the page (default: first render, then first gallery image) |
| `hub_image` | Image object for the hub card (default: the hero image) |
| `renders`, `renders_heading`, `renders_intro`, `renders_note` | Concept renders (see below) |
| `floor_plans`, `plans_heading`, `plans_intro`, `plans_note` | Official floor plans (see below) |
| `unit_tips`, `unit_tips_heading`, `unit_tips_note` | Cards: `{"unit", "tip"}` + optional `size`, `bedrooms` |
| `sections` | Free sections: `{"heading", "text"}` (markdown) + optional `bullets` list |
| `gallery`, `gallery_heading` | Extra images: image object + optional `caption` |
| `steps`, `steps_heading` | Timeline: `{"title", "text"}` + optional `duration`. Default: the standard timeline for the type |
| `timeline_note` | One line under the timeline |
| `guide` | Which service guide to link: `bto`, `condo`, `ec`, `landed`, `office`, `retail` (default from `type`) |
| `cta_text` | Line in the dark WhatsApp band at the end |
| `reviewed` | "Facts checked …" line under the sources |
| `date_published`, `date_modified` | `YYYY-MM-DD`; `date_modified` is the sitemap lastmod |

Any optional block that is missing or empty is simply not rendered.

### Image objects

```json
{"image": "/images/new-launches/<slug>/<file>-1600.webp", "image_small": "/images/new-launches/<slug>/<file>-900.webp",
 "width": 1600, "height": 900, "alt": "What the picture shows"}
```

Images must be `.webp` files under `/images/` or `/img/` in the repo, with whole-number `width` and `height`.
`image_small` is optional; its width is read from the `-NNN.webp` ending. All images below the top one lazy-load.

### Concept renders

Each render is an image object plus optional `style`, `room`, `title` (H3), `text` and `whatsapp_text`.
Every render is captioned **"Concept design by Maison, not the actual unit"** automatically.

### Floor plans

Each plan is an image object plus `caption` and `credit` (e.g. `"Floor plan: Norwood Grand brochure, CDL"`),
optional `title`, `credit_url` and `credit_link_text` (the part of the credit that becomes a nofollow link).
Copy official plans as they are (crop and scale only) and always credit the source.

## Checks the build makes

- unknown field names (catches typos), missing required fields, wrong types
- slug format and slug = file name; `type`, `region` and `guide` values
- every image exists, is `.webp`, and has width and height
- `keywords[0]` in the title, H1 and first paragraph; description of 155 characters or fewer
- nearby hints that point to a page that does not exist yet are skipped with a note
- after the build: no `/preview/` paths, no Page One credit, no noindex (except the parc-point-tengah stub), no dotfiles

## What every page gets

One H1 `<Name> Renovation & Interior Design`; breadcrumb; facts as cards (no tables, so nothing scrolls sideways
on a phone); the optional blocks; planning notes (defects, rules, timeline for the type); FAQ; sources; three nearby
projects (hints, then same district, same area, same region and type, then same type); a WhatsApp CTA to
`wa.me/6593391185` with a project prefill; Article + FAQPage + BreadcrumbList JSON-LD; canonical, Open Graph and
Twitter tags with absolute `https://maisoninteriordesign.sg/` URLs.

## Light packs (markdown)

`newlaunch_pack.py` converts packs written in this layout:

```
# <Name> Interior Design & Renovation | <place> <Condo|EC|BTO|HDB> — Maison
SEO title: …
Meta description: …
Keywords: <name> renovation, …
## Project facts
- Type: condominium | executive condominium | HDB BTO project | HDB project
- Developer: … Source: https://…
- District / town: D11 | Bedok
- Address / Units / Tenure / Unit types / Launch / TOP / key date: … (blank = not shown)
- Note: … (shown under the facts)
- Recorded source (not used as official confirmation): https://… (listed as a nofollow source)
- File note: … (internal, not published)
## <Name> interior design and renovation
paragraphs (first one becomes the intro, the rest a "Planning your <Name> interior" section)
## Floor plan            (not published when there is no plan)
## Target keywords       (not published)
## Frequently asked questions
**Question?** Answer
## Nearby projects       (links become nearby_hints)
## Talk to Maison        (first line becomes the CTA text)
## Sources               (- https://… lines)
```

What the converter changes, and why:
- The title is reordered to `<Name> Renovation & Interior Design | …` so the main keyword is in the title.
- If the first paragraph lacks `keywords[0]`, one sentence is added: "This page sets out what is on file and how to plan your `<keyword>`."
- A meta description over 155 characters is shortened by dropping stock phrases first ("Unconfirmed figures are left blank.").
- Dates like `2027-Q4` become `Q4 2027`; `2026-06-16` becomes `16 June 2026`. The words around them are kept.
- Internal words are swapped for reader words: "this light pack" → "this page", "this row" → "this project".
- Region comes from the HDB town or the postal district (URA planning regions).

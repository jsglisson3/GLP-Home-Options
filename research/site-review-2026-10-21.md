# Site review: Oct 21, 2026 (planning session, no live page changed)

**What this is:** a tough, honest review of the whole site as it is live today (Checkpoint 10), written to aim the next sessions. **Method:** full-page screenshots of Home, Options, Our story, New homes and Contact at 1440 px wide, Home and Options at 390 px (phone), every Home section read at close range, plus timing and weight numbers from a local run. Findings are my judgment; nothing here is a study. Privacy and Terms were not visually reviewed.

## Verdict

The foundation is strong: one clear promise, an honest comparison, one coherent look, clean accessibility and a very light page. It is **not yet "best ever"** because of four gaps:

1. **Photos**: two key photos have unconfirmed origins, several are soft, and one shows third parties.
2. **Proof is thin** (one closing story, one build; correctly no invented reviews).
3. **Home is too long** (about 13,000 px on a laptop, about 20,000 px on a phone) and repeats the Options page.
4. **One design device repeats** until it feels templated.

## What is working (protect these)

- **The hero** (people-led, gable frame, cream): clear promise, real faces, two obvious actions, a calm numbers strip. The header now matches it on every page.
- **Honest numbers.** The compare table says "Trades some price for speed and certainty", and the default net-sheet example shows listing netting about $7,000 more. That candor is the strongest trust move on the site; keep it.
- **One system**: navy leads, green accents, cream and white alternate, one navy "pause" section, one green contact finale. Typography and spacing feel the same on every page.
- **Real build photos** on New homes and in the Home teaser.
- **Phones**: faces in the first screen, a sticky call, text and consult bar, tap targets of 44 px or more, no sideways scrolling.
- **Weight and accessibility**: see the numbers below; automated accessibility scans are clean.

## Findings, ranked

Size: S under 20 min, M one session, L more. "Approval" means it changes direction, scope or architecture, so it waits for Jeremy.

| # | Priority | Finding | Fix | Size | Approval |
|---|---|---|---|---|---|
| F1 | **P0 trust** | The origins of the **bridge hero photo** and the **kitchen-table photo** are unconfirmed (`PROJECT_STATUS.md` risk table). The alt text states them as real events ("Ethan and Joey going over options with homeowners at a kitchen table"). No file carries camera data (web exports strip it), so nothing proves either way. Sessions 6c and 6d also sharpened and warmed the bridge photo and added 6% of mirrored, blurred background above their heads (faces untouched; the unedited original is in `research/photos/from-old-build/`). | Ask Joey for the original files and whether both are real photographs of them (`questions-for-joey.md`, Q1). If either is not, replace it and fix the alt text. The site stays `noindex` until answered. | S to ask, M to replace | No |
| F2 | **P0 trust** | The **riverfront banner** is 900 x 225 px stretched to about 1440 px on laptops (visibly soft) and its origin is unknown. | Replace with a photo Joey took or a licensed one, or show it smaller in a frame. | S | No |
| F3 | **P0 trust** | The **closing-day photo** shows the sellers' faces and a title company's sign (`CONTENT_CLAIMS.md` row 32). | Consent from the sellers and the title company, or crop or replace (Q2). | S | No |
| F4 | P1 | **Home repeats Options.** Four back-to-back explainers (three option cards, how it works, compare table, net sheet) cover ground the Options page covers again in more depth. | Give "The numbers" (compare table and net sheet, 2,372 px of the page) its own page; Home keeps a one-screen teaser. That alone brings Home to about 11,200 px on a laptop and 16,600 px on a phone. Also trimming the FAQ to the five most-asked (with a link to the rest) and folding "how it works" into the options section brings it to about 9,500 px and 14,500 px. | M | **Yes (D7)** |
| F5 | P1 | **The green-italic second headline line repeats**: 11 headlines on Home use it (hero included), and it is on every page. A signature used everywhere stops being one. | Keep it for the hero and three or four key moments; plain bold for the rest. | S | **Yes (D8)** |
| F6 | P1 | **Card grids repeat**: three path cards, four value cards, three "is GLP legit" cards, three "who it is for" cards, "good fit / maybe not" pairs three times on Options. | Vary the forms (one list, one split layout, one timeline). Already planned as P7. | M | No |
| F7 | P1 | **Proof is thin.** One closing story and one build. | Gather real proof: Google reviews once they exist, the gallery (Session 10), a recent-closings line from Joey's own numbers if he wants to share them. Never invent. | M | No |
| F8 | P1 | **The contact form's consent text still has placeholders** (`[BUSINESS NAME]`, example.com links) and the form cannot be tested from here. Launch blocker. | Session 11 with GoHighLevel access. | M | No |
| F9 | P2 | **Column balance**: on Home "About GLP" the button sits about 10 px under the last list item and the right column is empty below the quote; the story photo has empty space under it; the FAQ intro column is sparse. | Align and space the columns. | S | No |
| F10 | P2 | **Glass**: five uses today (header, phone bar, contact cards on the dark section, name plates on the portraits, the Options "jump to" panel). The last two are almost opaque, so the blur adds cost and no look. | Keep three, make the other two solid. This is the Session 4 list. | S | **Yes (D10)** |
| F11 | P2 | **22 different width breakpoints** in the CSS (19 `max-width` values and 3 `min-width` values; 27 media queries in 57 blocks). `research/css-inventory-2026-10-21.md` has the counts and a proposed mapping. | Consolidate to four (Session 5, P1). | M | No (planned) |
| F12 | P2 | **Photos are about 800 px.** The 2x hero file is made from the same 800 px source, so it is smoother, not truly sharper. | Joey's originals (1600 px or more on the long side). | | No |
| F13 | P2 | **Unused code**: the numbers count-up in `js/site.js` (about 25 lines). | Remove in Session 5. | S | No |
| F14 | P2 | **Launch plumbing missing**: `noindex`, no sitemap, robots or canonical; analytics and conversion tracking not set. | Session 13. | S | No |
| F15 | P2 | **Accessibility beyond automation**: no manual keyboard or screen-reader pass; the desktop menu links are 36 to 37 px tall (above the 24 px WCAG 2.2 minimum, below our 44 px goal). | Session 12. | M | No |

## Measurements (local server, so no network time; not a Lighthouse score)

| | Home | Options | Our story | New homes | Contact |
|---|---|---|---|---|---|
| Page height, 1440 px wide | 13,050 | 9,039 | 6,541 | 5,883 | 3,905 |
| Page height, 390 px wide | 20,295 | 13,841 | not measured | not measured | not measured |
| HTML (KB, raw) | 51 | 37 | 25 | 23 | 22 |
| Images, whole page (KB) | 797 | 29 | 412 | 465 | 29 |
| Layout shift | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

Home section heights, laptop / phone (px): hero 787 / 1,153; strip under the hero 332 / 607; options 1,642 / 2,699; story 1,126 / 1,561; how it works 890 / 1,243; **numbers (table and net sheet) 2,372 / 4,377**; riverfront banner 560 / 520; about 1,178 / 1,646; new-home teaser 943 / 1,296; FAQ 1,314 / 1,761; contact 1,320 / 2,123; footer 505 / 1,165.

Shared on every page: CSS 59 KB raw (about 13 KB compressed), JavaScript 13 KB raw (about 4 KB compressed), fonts 71 KB on the main pages. Home first screen: 236 KB of images, 10 requests; whole page 17 requests. Everything is light. A real score needs Lighthouse on the live site (Session 12).

## Not verified

A real phone or tablet; keyboard-only and screen-reader use; Lighthouse and real network speed; the GoHighLevel form; copy accuracy beyond `CONTENT_CLAIMS.md`; Contact, Privacy and Terms at close range; the picker and net sheet beyond looking at them.

## Ideas that would raise the ceiling (scope additions; none started, all need approval)

- **Save or print "your numbers"** from the net sheet (done in the browser, nothing sent), so families deciding together (inheritance, divorce) can share it.
- **A short intro video** of Joey and Ethan (poster image, no autoplay, captions), only if Joey wants it.
- **"Our work" gallery** (Session 10, blocked on Joey).
- **A short guided "which path fits?"** (three questions, a one-paragraph answer, then a prefilled consultation request). The picker already does a one-tap version.
- **Real reviews strip** once real reviews exist.
- **Situation pages** (inherited home, divorce, relocation, repairs) written from Joey's real experience, which also help search later.

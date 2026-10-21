# GLP Home Options: design system

**Source of truth for visual decisions.** The code (`css/site.css`) is the truth for what exists today; this file records the values, the rules, and **which decisions Jeremy has actually approved**. If this file and the code disagree, believe the code, then fix this file.

Last verified against the code: Oct 21, 2026 (Session 1, Checkpoint 1).

## 0. Approval status (read this first)

Nothing below has been signed off as a complete package yet. The system was built across earlier sessions from Jeremy's directions; the master plan (Oct 21) now asks for formal approval in Phase 1.

| Level | Meaning |
|---|---|
| **APPROVED** | Jeremy approved this explicitly (date given). Locked: changing it needs his approval. |
| **DIRECTED** | Jeremy asked for this explicitly in conversation. Treat as approved; don't undo without asking. |
| **BUILT** | In the code today. Not yet formally approved. Keep, but it can still change through the approval process. |
| **PROPOSAL** | Our suggestion. Not built. Needs approval. |

**DIRECTED by Jeremy (from the conversation):**
1. Light, bright, "not so black": use the **logo's colors** (navy and green) on light surfaces. *"Use those colors... make this something you would sell to a million dollar investor."* No dark mode.
2. **Back off the green.** Navy leads; green is the supporting accent.
3. Classy, enterprise-level, "feels alive and proper": restrained, purposeful motion.
4. Best-in-class standards (Baymard form guidance, CXL credibility checklist), **mobile ready**.
5. Remove the watermark from the Chattanooga riverfront photo (done).
6. A **Facebook logo that links to Joey's page** in several places (header, phone menu, footer, About, Contact, home contact, New homes).
7. Never invent reviews, licenses, years in business, or awards.
8. (Oct 21) A separate construction site may follow; this site stays about **home buying/selling options**, and New homes remains a light teaser.

**APPROVED by Jeremy on Oct 21, 2026:**
9. **D1: navy leads, green is the accent.** The color tokens in section 2 are locked.
10. **D4: the homepage hero is A, people-led** (approved Oct 21, Session 3). B (numbers-led) was prototyped and not chosen.
11. **D2: cream is the site's one tint** (hero approved Oct 21, Session 3; extended by Jeremy on Oct 21, Session 6b, to every hero, the alternate sections and the footer; see P3).
11. **D5: a restrained set of glass and motion.** Keep header glass, small overlays on photos and the ridge and contour touches; drop the floating blobs and photo parallax (exact glass list set in Session 4, applied in Session 5). **Built at Checkpoint 5 (Session 3b):** the floating blobs, the photo drift, the hero photo's slow zoom and the tags' bobbing are gone from `css/site.css` and `js/site.js`; only the glass reduction to the 7 listed uses is left for Session 5.
12. **Claims:** copy says only what Joey's own materials support, or what Jeremy has confirmed and `CONTENT_CLAIMS.md` tags **J** until Joey confirms it.

**Proceeding by default (Jeremy told, no objection):** D3 keep Plus Jakarta Sans and the Fraunces italic accent; D6 keep the five-page structure (the gallery's placement is decided later).

All decisions (D1 to D6) and their status are in `PROJECT_STATUS.md`, section C.

**Built into the live site at Checkpoint 5 (Session 3b):** D2's warm cream is the Home hero surface (`--cream`, `.hero .hero-bg` in `css/site.css`; page heroes stay cool), and D5's removal of the floating blobs, photo drift, hero photo zoom and tag bobbing. The hero A/B choice is still not applied (Session 6).

**Checkpoints 6 and 7 (Session 6a):** hero A (people-led, chosen by Joey) is the live Home hero. The header has a constant 80px height with a 50px logo and, on Home only, takes the hero's cream at the top of the page (white glass once you scroll). On phones a "Joey & Ethan" chip with two small portraits shows their faces in the first screen. Headlines use `text-wrap:balance` and intros `text-wrap:pretty`. From 981 to 1100px the photo tags and caption are slightly smaller so they never overlap.

**Checkpoint 8 (Session 6b):** Jeremy approved cream beyond the hero, so cream is the site's one tint: every hero, the alternate sections (white and cream alternate), the footer and the small tinted controls; mist and mint are retired (`--cream-100 #f8f3e7` for bands). The header takes the hero's cream at the top of every page. For a more professional look, the floating hero tags, the pulsing location pill, the path chips and the button shine sweep were removed, and the primary-button shadow is softer. Cream contrast (computed): on `#f8f3e7` and `#f6f0e3`, `--text` 7.1 and 6.9, `--muted` 5.8 and 5.7, `--navy-800` 10.8 and 10.6, `--green-700` 6.0 and 5.9; on the darkest hero end `#efe8d8`, `--muted` 5.3 and `--green-700` 5.5. `--green-600` (4.4 on `#f6f0e3`) is used only for large headline text, icons, the header wordmark and the numbers strip on white, where it measures above 4.5. The numbers strip on Home no longer counts up; it shows the final numbers at once.

**Checkpoint 9 (Session 6c):** the Home hero photo was re-processed, not re-shot: the source is 800 x 600, so it was resampled with Lanczos, lightly sharpened and warmed (`images/joey-ethan-bridge.jpg` for normal screens and `images/joey-ethan-bridge-2x.jpg`, 1600 x 1200, for sharp screens, chosen by `srcset`); the original is kept in `research/photos/from-old-build/`. The gable frame is slimmer on every page (7px line, 7px white mat; was 9 and 8) and the photo has a soft shade at the bottom behind the name plate. The header's phone number is plain text with a small green phone glyph and the Facebook logo has no circle; the scroll-progress line was removed. **The photo is the limit: ask Joey for the original file or a new portrait (at least 1600px tall).**

## 1. Brand personality (from the master plan)

Premium and sophisticated; trustworthy and transparent; warm, local, human; modern, clear, easy to use. The message: **You have options. We will help you understand them. The decision is yours.** No pressure-driven design, no stock real-estate look, no decoration without a job.

## 2. Color (BUILT; hierarchy and hex values APPROVED Oct 21; all tokens are CSS variables in `:root`)

| Token | Hex | Use |
|---|---|---|
| `--navy-900` | `#1a323d` | Deepest navy: shadows, dark surfaces |
| `--navy-800` | `#233948` | Headings (`--ink`), dark buttons |
| `--navy-700` | `#2d4855` | **Primary brand navy** (logo roof), wordmark, focus ring, ghost button text |
| `--navy-600` / `-500` | `#3b5b69` / `#527785` | Secondary navy, supporting text on dark |
| `--navy-300` / `-200` / `-100` | `#a3b8c0` / `#c7d5da` / `#e3ebee` | Borders, dividers, soft fills |
| `--green-800` / `-700` | `#2e5649` / `#366554` | Green text and eyebrows on light (`-700` is the AA-safe green for small text) |
| `--green-600` | `#3c7a66` | **Primary brand green** (logo roof): italic accent, links, icons |
| `--green-500` / `-400` | `#4e9279` / `#6faa93` | Hover states, decorative |
| `--green-300` / `-200` / `-100` / `-50` | `#9fc8b8` / `#c9e0d6` / `#e4f0eb` / `#f2f8f5` | Tints, active nav pill, soft backgrounds |
| `--cream-100` | `#f8f3e7` | Section bands (`.sec-cream`), the strip under the Home hero, the footer and small tinted controls. The cool `--mist` and the mint gradient were retired on Oct 21 (Session 6b). |
| `--text` | `#3d5560` | Body text |
| `--muted` | `#4a626d` | Secondary text (still passes AA) |
| `--line` / `--line-2` | `#dce6e6` / `#cbd8d8` | Hairlines and card borders |
| `--grad` | `135deg, #2d4855 → #37625c (52%) → #3c7a66` | Signature gradient: eyebrow bar, icon tiles, dark bands, progress bar |
| Page background | `#fff` | Default. White and cream (`.sec-cream`) sections alternate, and no section sits on the same surface as its neighbor. |
| Facebook blue | `#0866FF` | **Only** inside the Facebook logo symbol. Never a theme color. |

Primary button: `linear-gradient(135deg, #3a7a66, #316656)` with white text (measured 5.3:1).

**Measured contrast (axe + scan, Oct 21):** text on white or mist ≥ 5.5:1 for `--text`, `--muted`, `--green-700`; white on the primary button 5.3:1; white on the dark contact band 5.8 to 10.4:1 depending on where it sits on the gradient; large display text ≥ 7:1 on the new pages. Goal stays WCAG 2.2 AA everywhere.

## 3. Typography (BUILT)

Self-hosted variable fonts (no Google requests), `font-display: swap`:
- **Plus Jakarta Sans** (variable, weights 200–800): headings, body, UI, numbers.
- **Fraunces italic** (variable, weights 100–900): *accent phrase only*, never body text.

| Role | Size | Line height | Tracking | Weight |
|---|---|---|---|---|
| Body | `clamp(1rem, .96rem + .2vw, 1.0625rem)` | 1.65 | normal | 450 |
| `.lede` | `clamp(1.06rem, 1.4vw, 1.2rem)`, max 62ch | 1.65 | normal | 450 |
| H1 | `clamp(2.35rem, 4.7vw, 4.2rem)` (`.contact h1`: `clamp(2.2rem, 4.5vw, 3.7rem)`) | 1.02 | −.04em | 800 |
| H2 | `clamp(2.05rem, 4.5vw, 3.5rem)` | 1.04 | −.035em | 800 |
| H3 / `.h3` | `1.3rem` | 1.2 | −.02em | 700 |
| Eyebrow | `.78rem`, uppercase | 1 | +.16em | 800, `--green-700`, with a 30×3 px gradient bar |
| Buttons | `1rem` (lg `1.06rem`, sm `.95rem`) | 1 | normal | 700 |

**The italic accent (`.ital`):** Fraunces italic 500, `--green-600`, `1.04em`, set on its own line (`display:block`) inside H1/H2. One accent phrase per heading. It is the main "warm, human" typographic gesture.

Headings use `text-wrap: balance`. Do not add a third font.

## 4. Layout and spacing (BUILT)

- Content width `--maxw: 1240px` via `.wrap`, side padding `clamp(20px, 4vw, 48px)` plus device safe areas.
- Sections (`.sec`): vertical padding `clamp(76px, 10vw, 136px)`. Section heads (`.head`): max 780px (`.center` max 980px), 18px gap, bottom margin `clamp(40px, 6vw, 72px)`.
- `--pull: clamp(64px, 8vw, 112px)` pulls the stats strip up over the hero.
- Sticky header: 82px tall, 68px after scrolling. `scroll-padding-top: 92px` so anchors clear it.
- **There is no spacing scale.** Gaps and paddings are individual values. (PROPOSAL P2.)

### Breakpoints (BUILT, and inconsistent)

19 distinct width conditions across 47 width-based `@media` rules (51 `@media` rules in all; the rest are print, reduced-motion and coarse-pointer): max-width **380, 420, 440, 480, 520, 560, 620, 700, 720, 760, 860, 900, 960, 980, 1080, 1160** and min-width **981, 1161, 1360**. Most used: 900 (12 rules), 980 (6), 520 (5). The ones that carry real decisions: **≤1160** (nav collapses to the phone menu), **≥1360** (header phone pill appears), **≤900** and **≤520** (layouts stack, phone sizing).

**PROPOSAL P1 (Phase 2, no visual change intended):** consolidate to four: 520 (phone), 900 (tablet), 1160 (nav), 1360 (wide), and map every other value onto them.

## 5. Surfaces: radii, shadows, glass (BUILT)

- Radii: `--r-s 12px`, `--r-m 20px`, `--r-l 28px`; buttons, nav pills and chips are fully round (`999px`).
- Shadows: `--sh-1` (hairline lift), `--sh-2` (cards, open FAQ), `--sh-3` (floating UI), all tinted navy.
- Borders: 1px `--line`; cards often `--line` plus `--sh-1`.
- **Glass (translucent white + blur)** is used in 7 places: the sticky header (`.74` white, blur 16, saturate 1.8, `.95` once scrolled), photo caption chip (`.gable-cap`), floating cards (`.fc`), founder captions, contact reach tiles (on the dark band), the phone action bar, and the "Jump to an option" panel on the Options page (`.jump`). Text on every glass surface passes AA. **D5 (approved Oct 21)** keeps the header glass and small overlays on photos; Session 4 decides, for each of the seven, whether it stays (the contact reach tiles, the "Jump to" panel and the phone action bar are the ones to review).

## 6. Motion (BUILT)

Principles: motion explains or rewards, never decorates; everything is off for `prefers-reduced-motion`; the page is fully readable with JavaScript off.

| Motion | Spec |
|---|---|
| Scroll reveal (`.rv`) | `reveal` keyframes, `.85s cubic-bezier(.2,.7,.2,1)`, 28px rise, stagger `--d × 90ms`. Content stays visible without JS or IntersectionObserver. |
| Hero ridge parallax | Scroll position drives one CSS variable (`--p`) via `requestAnimationFrame`; a few px only. The riverfront photo parallax (`--py`) was removed at Checkpoint 5 (D5). |
| Background blobs | Removed at Checkpoint 5 (D5). |
| Topographic contours | Canvas, drawn once per size (static lines; 16 rings around two peaks). |
| Header | Height and background ease in `.3s`; scroll-progress bar fills with scroll. |
| Count-up (stats strip) | 1.2s ease-out cubic; 8s failsafe shows final numbers. |
| Buttons | Lift 2px on hover, sheen sweep `.8s`; arrow nudges 3px. |
| Page changes | `@view-transition` soft fade where supported. |

Reduced motion: all animations and transitions are removed; reveals show immediately; parallax and count-up are skipped. **Approved Oct 21 (D5):** drop the background blobs (`drift`) and the photo parallax; keep scroll reveal, the ridge and contour touches, count-up, button hover and the page fade. **PROPOSAL P4:** define motion tokens (durations, easings) in Phase 2.

## 7. Components (BUILT; class names in `css/site.css`)

| Component | Classes | Rules worth keeping |
|---|---|---|
| Header + nav | `.hdr .nav .hdr-phone .hdr-cta .hdr-fb .menu-btn .mnav` | Contact is last in the nav. Facebook logo button in the header at ≥1161px; phone menu has a "Follow us on Facebook" row. |
| Phone action bar | `.mobile-bar` | Appears after the hero buttons scroll away; steps aside at the form. |
| Hero (home) | `.hero .hero-grid .gable .eyebrow .micro` | One H1, one primary action, one human photo with a single name plate. No floating tags (removed Oct 21, Session 6b). |
| Page hero (inner pages) | `.phero .crumbs` | Breadcrumb, H1, lede, one primary action. |
| Photo frame | `.gable` (`.g1 .g2 .g3`, `clipPath#gable`) | The roofline of the logo as a photo mask. Use for people and homes. |
| Section heading | `.head .eyebrow .ital` | Eyebrow + H2 with italic accent + optional lede. |
| Icon tiles / beliefs | `.tile .belief .beliefs .beats .num .checks` | Line icons from the SVG sprite (`i-*` symbols), 2px stroke. |
| Stats strip | `.stats` (`data-count`) | Only numbers Joey's site supports. |
| Compare table | `.cmp .table-card .table-scroll` | Scrolls sideways on phones; focusable. |
| Net sheet | `.net .sheet .verdict` | Symmetric verdict; "Example figures" labeled; disclaimer shown. |
| Fit picker | `.picker .picker-opts .path .opt-sec` | Appears only with JavaScript. |
| "Jump to" panel | `.jump` (Options page) | In-page links to each option; glass surface. |
| Option sections | `.opt-card` | "A good fit if" and an honest "Maybe not if". |
| FAQ | `.faq` (`<details>`) | The same data drives the visible list and the FAQPage structured data (builder). |
| Contact block | `.contact .reach-item .next .form-card .ghl` | Labels above fields; form is the GoHighLevel iframe. |
| Gallery | `.gallery` (New homes) | Captions are honest status labels. |
| CTA band, footer | `.cta-band .ftr` | Every page ends with a next step. |
| Buttons | `.btn .btn-primary .btn-ghost .btn-lg .btn-sm` | Pill shape; min-height 52 (lg 60, sm 46). |
| Facebook | `.fb-btn .fb-logo` | The logo is a white disc with the `#0866FF` mark. Don't use the line-icon class on it. |

### Hero tag system (RETIRED Oct 21, Session 6b; kept as history)

**Retired:** Jeremy said the floating tags on the photo "look tacky". They are removed from the Home and New homes heroes and the CSS is deleted. The photo carries one solid white name plate; the numbers live in the strip below it. Do not bring floating tags back without Jeremy's approval. The five rules below are kept only so the reasoning is not lost.

Jeremy's feedback: the floating tags on the photo "look random". The old tags sat at three different overhangs and heights; on phones the speed tag covered Ethan's eyes and the caption ran under the call tag. They now follow five rules:

1. **One overhang.** Every tag hangs the same distance past the photo frame: 40px (14px on phones; on single-column tablet widths `min(40px, (100vw - 470px) / 2 - 12px)`, so nothing is clipped).
2. **One size.** The three tags share a width and height: 224 x 62px (phones 202 x 54), with a 12px gap where they stack.
3. **Two groups.** The speed tag ("Selling directly / Close in 7-14 days") hangs off the right side with its top on the roof peak. The price and call tags form a left stack with one left edge.
4. **One bottom line.** The bottom of the call tag and the bottom of the Joey & Ethan caption sit on the same line, 28px above the frame's bottom (the caption is 20px from the right edge). On phones the caption becomes a nameplate centred on the bottom edge, so it never meets the call tag; the price tag is hidden there, as before.
5. **Faces stay clear.** Nothing sits above the chins. Check any change by looking at the photo at 1440, 820 and 390.

No bobbing and no slow photo zoom (D5). Verified: no tag overlaps or clips at 1440, 1100, 820, 560, 390 and 320, and every label stays on one line.

## 8. Accessibility and responsive requirements

- **WCAG 2.2 AA is the target.** Baseline: axe-core 0 violations on all 7 pages at 1440, 820, 390 (touch) and 390 with reduced motion, plus the phone menu open and the picker pressed.
- Visible focus: 3px `--navy-700` outline, 3px offset (white on dark bands). Skip link on every page. Landmarks and one H1 per page.
- Tap targets (measured Oct 21, non-inline links, buttons, inputs and FAQ rows on all 7 pages): nothing is under WCAG 2.2 AA's 24px minimum. Buttons, inputs and FAQ rows are 46px or taller. Footer links are 36px tall on desktop (44px on phones), header and breadcrumb links are 32px, and the phone-number text link on Our story is 40px. That meets AA but not the 44px best practice (**PROPOSAL P5:** 44px on touch).
- Forms: permanent labels above fields (Baymard). The embedded GHL form's own styling is controlled inside GoHighLevel.
- No horizontal scrolling at any tested width; test at 320px in Phase 6.
- Respect `prefers-reduced-motion`; no autoplay media; no dark mode (deliberate).

## 9. Image treatment

Photos are real project/people photos in the gable frame, with descriptive alt text and explicit width/height. Current sources are ~800px wide (soft above ~1000px display width): **replace with Joey's originals** (see `PROJECT_STATUS.md`). The logo is a 240×132 raster (`images/glp-mark.png`): **a vector logo is needed**. Don't use the old site's illustrated option images (they look AI-generated). Saved copies of images get an invisible provenance tag (a few KB), which is harmless.

## 10. Gaps and proposals (none approved)

| # | Proposal | Phase |
|---|---|---|
| P1 | Consolidate 19 breakpoints into 4 | 2 |
| P2 | Add a spacing scale (`--space-1..8`) and a type scale as tokens | 2 |
| P3 | Warm neutral (cream) surface. **APPROVED for the hero (Oct 21, Session 3) and extended to the whole site (Oct 21, Session 6b):** `--cream: #f6f0e3`; hero background `linear-gradient(180deg,#fdfbf6 0%,var(--cream) 55%,#efe8d8 100%)`; the ridge's front layer stays `--mist`. Contrast on the darkest stop `#efe8d8`: body text 6.45:1, `--muted` 5.28:1, navy-800 9.83:1, green-700 5.47:1; the green-600 italic accent is 4.13:1, so on cream it is for large type only. Any other section: not decided. Built in `css/proto.css`; applied in Session 6. | done (1); apply in 6 |
| P4 | Motion tokens (durations, easings) | 2 |
| P5 | 44px touch targets for footer/inline links on touch devices | 6 |
| P6 | Responsive images (`srcset`, WebP/AVIF) once originals exist | 6 |
| P7 | Reduce repeated tile-card grids on the home page (the plan asks for varied layouts) | 4 |

## 11. Research basis

CXL website-credibility checklist (real staff photos with names and roles, address and phone visible, Contact last in nav, plain language, no fake proof); Baymard form guidance (labels above fields, minimal fields); Google people-first content guidance (first-hand experience, original value); Opendoor/Offerpad patterns (one headline and one action, human photo, proof under the hero, side-by-side comparison, "is this legit?" answered head-on). We copy patterns, never wording.

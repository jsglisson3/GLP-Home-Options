# GLP Home Options website: PROJECT STATUS

**Start here every session.** This file is the map. The code is the truth. If they disagree, believe the code, then fix this file.

_Last updated: Oct 21, 2026, Session 1 (Phase 0), Checkpoint 1._

## Which documents are authoritative

| File | Authoritative for |
|---|---|
| `PROJECT_STATUS.md` (this file) | Current state, approved decisions, implementation record, session log |
| `SESSION_HANDOFF.md` | **The latest handoff:** exactly what the next session does |
| `ROADMAP.md` | Phases, session-by-session plan, dependencies, acceptance criteria |
| `DESIGN_SYSTEM.md` | Design values and rules, with each marked DIRECTED / BUILT / PROPOSAL |
| `CONTENT_CLAIMS.md` | Every factual claim on the site, its source, and what Joey must confirm |
| `README.md` | How to run, build and publish |
| `CHECKPOINT.json` | Fingerprints of the files at the last verified checkpoint (written by `tools/checkpoint.py`) |
| `PICKUP.md` | **Superseded.** A pointer only. Its content moved into the files above. |

## The three working rules (Jeremy's, non-negotiable)

1. **The code is the truth; the status file is the map.** At the start of every session check both: read this file and `SESSION_HANDOFF.md`, run `python tools/checkpoint.py`, look at the live site. Never assume a feature exists because an earlier chat said it was finished.
2. **Every session ends at a checkpoint.** No unfinished, sprawling rewrite. Leave the project stable, record unfinished work, define the next task, run `python tools/checkpoint.py --write "label"`.
3. **Preserve the plan and approved design decisions.** They live here, in `DESIGN_SYSTEM.md` and in `ROADMAP.md`, in version control, not in anyone's memory of a chat.

Workflow: one focused session, one verified checkpoint, updated documentation, one clearly defined next session. Sessions are **30 to 45 minutes**; plan for 30 to 40. Never claim something was saved, deployed or tested unless it actually was.

**Other standing rules from Jeremy:** this site is Joey's livelihood and his family's, so accuracy and trust beat flash: never invent reviews, licenses, years in business, awards or numbers; if we don't have it, leave it out or ask Joey. Keep messages short and plain, and send a one-line status when he nudges. He approves creative direction, scope and architecture changes. He publishes in VS Code: Source Control, stage all (the **+**), type a message, **Commit**, then **Sync Changes**.

---

## A. Project identity

- **Project:** the website for **GLP Home Options** (Chattanooga, TN area): home options for homeowners (sell directly, list with an agent, keep the home, creative solutions), plus a light teaser for new homes they are building. Operated by **GL Partners LLC**; co-founders **Joey** and **Ethan**; mailing address PO Box 55, Hixson, TN. Directed and published by Joey's brother **Jeremy Glisson** (times in these notes are Central); built in sessions with Claude.
- **New website (this project):** https://jsglisson3.github.io/GLP-Home-Options/ (GitHub Pages; draft; `noindex, nofollow`).
- **Existing website (reference, not a template):** https://glphomeoptions.com/ (appears to be built on GoHighLevel: its images come from a HighLevel file host and its form from HighLevel; who controls the account and domain is not yet confirmed). Pages: Home, About, Options, Calculator, Contact Us, Terms of Service, Privacy Policy.
- **Facebook:** https://www.facebook.com/profile.php?id=61588492362641
- **Repository (verified Oct 21 from `.git/config`):** https://github.com/jsglisson3/GLP-Home-Options.git, branch `main`, GitHub Pages deploys `main` / root. **The repository is public.**
- **Working directory and source of truth:** `C:\Users\jsgli\Documents\GLP-Home-Options` on Jeremy's computer. An AI session works on a temporary copy in a cloud workspace (which may also hold its own stale `.git`; ignore it).
- **Deployed state (checked Oct 21, after the 8:34 AM publish):** GitHub Pages serves the site from commit **`b6cc372` "Full refresh"** (committed 8:34 AM CDT; it is the last commit in the saved git log). Fetching `/` and `/contact.html` returned the new multi-page site: nav, H1s ("Real home options. Clear next steps." and "Let's talk about your home. No pressure, no scripts."), the Facebook links and `noindex, nofollow`; the Contact page shows the corrected heading order. This is a page-level check by reading the fetched text. A byte-for-byte comparison is not possible from the workspace (its shell can't reach github.io).
- **Stack:** plain HTML, CSS and vanilla JavaScript; no framework; no server. A small Python script (`tools/build-pages.py`) generates the 7 pages from shared parts, and the output is plain files. Fonts are self-hosted. The contact form and booking are GoHighLevel embeds (form `c36UOOc2pkosxfvRfjZJ`, booking `cM59fR3vJlAVRy08Depz`, host `links.voiseai.com`).

**Technical constraints that shape how sessions work**
- The AI workspace has **no GitHub access (no GitHub account is linked to it; checked Oct 21) and no shell on Jeremy's computer**. It can read and write files there through a bridge, but it **cannot commit, push, or delete**. Jeremy commits and syncs. At each checkpoint the AI gives him a ready-made commit message.
- **Save protocol:** stage files in the workspace in one step; commit them to the device in a **later, separate** step; verify with a directory listing. (Doing both in one step once wrote stale files.)
- Saving to the device adds an invisible provenance tag to images and to the SVG sprite `tools/pages/_sprite.html`. The builder's `clean_sprite()` removes it from page output; the checkpoint tool ignores it.
- The GoHighLevel form cannot load in the workspace, so **the AI cannot verify the form**. A person must test it on a phone after any change.
- Facebook shows only the newest post when logged out. The AI never signs in.
- Only Chromium has been tested. No real-device, Safari or Firefox testing yet.

## B. Vision and success criteria

- **Personality:** premium and sophisticated; trustworthy and transparent; warm, local, human; modern, clear, easy to use. Message: **You have options. We will help you understand them. The decision is yours.** No aggressive sales language, no pressure design, no misleading promises.
- **Audiences:** homeowners facing inheritance, divorce, relocation, repairs, financial stress or downsizing (primary); first-time buyers and families (new homes, secondary).
- **Design goals:** a distinctive, calm, light design in the logo's navy and green; story first; one clear next step per page; honest numbers.
- **A successful finished site (proposed criteria; Jeremy to confirm):** (1) every claim traces to Joey's own materials or is removed; (2) real photos of real people and projects; (3) the form works end to end and its text-message consent is correct; (4) legal pages lawyer-reviewed; (5) WCAG 2.2 AA with 0 axe violations and a clean manual keyboard pass; (6) Lighthouse scores in the 90s on mobile; (7) live on glphomeoptions.com, indexed, with a sitemap and analytics; (8) Joey has signed off on every page.

## C. Approved design system

Full detail and the DIRECTED / BUILT / PROPOSAL labels are in **`DESIGN_SYSTEM.md`**. Summary: navy `#2d4855` leads and green `#3c7a66` supports (both from the logo) on white and mist surfaces; Plus Jakarta Sans with a Fraunces italic accent; a gable-shaped photo frame; restrained scroll, ridge and contour motion that switches off for reduced motion; no dark mode.

**Approval status:** Jeremy has *directed* the direction (light, logo colors, back off the green, classy and alive, mobile first, Facebook logo, no invented claims). He has **not yet formally approved the system as a package.** Everything in code is BUILT, pending the decisions below.

### Decisions needing Jeremy's approval (Phase 1)

| # | Decision | Recommendation |
|---|---|---|
| **D1** | **Color hierarchy.** Keep navy-led with green as the accent (as built; matches "back off the green"), or move to a deep-green-led palette (the master plan lists deep greens first). | Keep navy-led. Lock the hex values in `DESIGN_SYSTEM.md` as tokens. |
| **D2** | **Warmth.** The palette is cool and clean; "warm, local, human" comes mostly from photos and the italic accent. Test one warm neutral (sand/cream) on a few surfaces? | Yes, but only inside the hero prototypes (Session 3), not site-wide. |
| **D3** | **Typography.** Keep Plus Jakarta Sans + Fraunces italic accent, or evaluate an editorial serif for headlines? | Keep. Try a serif headline only in one hero prototype. |
| **D4** | **Hero.** Approve building two prototypes to compare: **A, people-led** (Joey and Ethan in the gable frame, as built) and **B, numbers-led** (net sheet or compare table in the hero, smaller photo). | Approve. Pick after seeing both (Session 3). |
| **D5** | **Glass and motion.** Glass blur is used in 7 places; motion includes ridge and photo parallax, blobs, count-up and view transitions. Keep all, or trim to header, small overlays and the ridge/contour signature? | Trim to the restrained set, then define motion tokens. |
| **D6** | **Architecture and gallery.** Confirm the 5-page structure built this morning (Home, Your options, Our story, New homes, Contact) with New homes staying a light teaser. Where should the homes gallery go: inside New homes, its own "Our work" page, or the future construction site? | Confirm the structure. Decide gallery placement after Joey sends photos and answers. |

## D. Roadmap summary, open questions and risks

Roadmap: see **`ROADMAP.md`** (13 sessions to launch). Phase status: 0 done; 1 re-opened as review and approval; 2 to 6 built but need review, consolidation or validation; 7 not started. **Next: Session 2** (see `SESSION_HANDOFF.md`).

### Open questions (ask Joey; claim-related ones are in `CONTENT_CLAIMS.md`)

1. The six "fix first" claims: seller financing and lease options; counties served; "doing business as"; "free" and "no obligation, ever"; "anytime"; the example $255,000 offer.
2. Which phone number is primary? (Earlier notes mention a second number on older Facebook posts.)
3. Are `joey-ethan-bridge.jpg` and `kitchen-table.jpg` original photographs of Joey and Ethan, and do we have the rights? (They look heavily retouched; an original is the biggest trust upgrade.)
4. May we use the September closing story, the closing photo (it shows a title company's branded prop), and quotes from his Facebook posts?
5. His own words for the About page: why they started, how long they have been doing this, what each of them handles. Today it is built only from public material. Also anything he wants said, or not said, in "what happens next."
6. Original, full-resolution photos (builds, closings, the team, neighborhoods). Everything we have is about 800px, saved from Facebook or the old site. Rights to the 900px riverfront photo.
7. Tennessee real estate license or brokerage? Which advertising disclosures apply? Ask a lawyer.
8. Who controls the glphomeoptions.com domain and the GoHighLevel account? We need both to launch and to fix the form.
9. New build: still unsold? Price still mid $200s? What does "down payment assistance" mean here? Is a separate construction site coming, and when?
10. **The homes gallery (Jeremy, Oct 21):** which houses, their status, whether addresses/prices/interiors may be shown, photo ownership, originals.
11. Real reviews: once there are 3+ happy sellers, ask for Google reviews. We add real ones only.

### Risks

| Risk | Detail | Mitigation |
|---|---|---|
| Unverified claims live on the draft | See `CONTENT_CLAIMS.md` "Fix first" | Session 2; site is `noindex` meanwhile |
| **Public repository** | The repo is public and the preview serves every file in the repo root, so these notes, `research/` (source photos) and `tools/` are visible to anyone with the link. A keyword scan of the text files on Oct 21 found no passwords, keys or private data (only the public phone, email, form and booking ids that are already on the live pages). The claims register is candid. | Jeremy's call: keep as is, or move the notes to a separate private repo, or deploy only a site subfolder before launch (needs approval; changes the Pages setting). Not urgent. |
| GoHighLevel form | Consent text has `[BUSINESS NAME]`, `[USE_CASE_FROM_CAMPAIGN_DESCRIPTION]` and example.com links; styling set only inside GHL; unverifiable by AI | Session 11, with Joey |
| Photo quality and provenance | ~800px sources; raster logo (240×132); provenance of two photos unconfirmed | Joey's originals; vector logo |
| No social proof | Facebook shows 0 reviews; we never invent them | Ask for real reviews |
| Legal pages | Plain-words drafts, not lawyer-reviewed | Lawyer review before launch |
| Build status goes stale | "Driveway in, finishing underway" will age | Update regularly or use neutral wording |
| Design-system drift | 19 breakpoints, no spacing scale | Session 5 |
| Single-browser testing | Chromium only | Session 12 |

## E. Implementation record

### E1. Architecture decisions

| Decision | Alternatives considered | Why |
|---|---|---|
| Static site on GitHub Pages | A framework (Next, Astro); a site builder | Free, fast, simple, same pattern Jeremy already runs for another site (FOTCL) |
| Pages generated by `tools/build-pages.py` from shared parts; output committed as plain HTML | Copy the header and footer into 7 files (they drift); JavaScript includes (flash of missing content, weaker SEO) | One copy of the header, footer, FAQ and contact block; FAQ data feeds both the visible list and the FAQPage structured data |
| Progressive enhancement | JS-only components | Pages are fully readable without JavaScript; the fit picker appears only with JS |
| Self-hosted variable fonts | Google Fonts | Privacy, speed, no third-party requests |
| GoHighLevel form embed | A custom form | Joey's CRM and text-message campaign already live there |
| `noindex, nofollow` while draft | Indexing the preview | Don't compete with or confuse the live business site |
| `NEW_HOMES` constant | Hard-coded links | The construction business may get its own site: one line switches every link |
| Light theme only | Dark mode | Deliberate: the brand is bright, clear and calm |

### E2. File map

| Path | What it is |
|---|---|
| `index.html`, `options.html`, `about.html`, `new-homes.html`, `contact.html`, `privacy-policy.html`, `terms-of-service.html` | **Generated.** Never edit by hand. |
| `tools/pages/*.html` | The `<main>` content of index, options, about, new-homes, contact. **Edit these.** |
| `tools/pages/_sprite.html` | SVG icon sprite and the gable clip-path |
| `tools/build-pages.py` | Header, footer, mobile bar, head and meta, FAQ text, structured data, site facts (phone, email, Facebook, booking/form IDs, `CSS_V`/`JS_V`, `NEW_HOMES`) |
| `tools/legal_text.py` | Privacy and Terms wording (marked as a draft) |
| `tools/check-links.py` | Every link, anchor, image and script resolves; no duplicate ids |
| `tools/a11y-check.py` | axe-core accessibility and layout scan at 4 viewports (needs Playwright and axe-core) |
| `tools/checkpoint.py` | Session start/end check against `CHECKPOINT.json` |
| `tools/make-legal.py`, `make-og.py`, `og-card.html` | Legacy shim; share-card generator |
| `css/site.css`, `js/site.js` | All styling and behavior (bump `CSS_V`/`JS_V` in the builder after editing) |
| `images/`, `fonts/` | Site photos, logo, favicons, share card; self-hosted fonts |
| `research/` | Source photos and early notes. **Not loaded by the site.** |

### E2b. What each page is for

| Page | Job | Story arc | The one action |
|---|---|---|---|
| Home (`index.html`) | Landing page; links out to the deeper pages | Problem, options, proof, numbers, people, action | Talk to Joey or Ethan |
| Your options (`options.html`) | Sell direct, list, keep the home, creative solutions; each with how it works, what it costs, "a good fit if" and an honest "maybe not if"; fit picker, example net sheet, FAQ | What are my choices? What does each cost me? Which fits? | Get my options |
| Our story (`about.html`) | Real headshots first, why they do this, what they stand for, the September closing as a 4-step case, "Is GLP legit? Check us out" | Who are these guys, and can I trust them? | Talk to Joey or Ethan |
| New homes (`new-homes.html`) | Light teaser: spec card, job-site gallery, who it is for, FAQ | What are they building? Is it for me? | Ask about this home |
| Contact (`contact.html`) | Call, text, email, book and Facebook tiles; "what happens next"; the form; find us | Easiest possible way to reach a human | Send details or call |
| Privacy, Terms | Plain-words legal pages (draft) | | |

Every inner page ends with a call-to-action band, so there is always a next step. Header order: Your options, The numbers, Our story, New homes, Contact (last, per the credibility research).

### E3. Existing functionality that must be preserved

- Seller **net sheet** (`#calc`): inputs, formulas and symmetric verdict in `js/site.js`; labeled "Example figures"; disclaimer shown.
- **Compare table**, **FAQ** (one data set drives the list and the FAQPage JSON-LD), **fit picker** (JS only), **mobile menu**, **phone action bar**, **scroll-spy**, **count-up** with failsafe, reveal-on-scroll that never hides content without JS.
- **Facebook placements** (Jeremy asked for these twice): header logo button (≥1161px), phone menu row, footer button on every page, About "See our work" card, Contact reach tile and card, home contact tile, a link on New homes, FAQ text, and `sameAs` in structured data. URL is the `FB` constant in the builder.
- The three home path cards (sell direct, list, keep) and the "Situation doesn't fit a box?" strip link to the matching section on the Options page.
- **GHL form and booking IDs**; `tel:`/`sms:`/`mailto:` links.
- Legal page URLs `/privacy-policy` and `/terms-of-service` (same as the old site).
- `noindex, nofollow` until launch (Session 13).
- Accessibility baseline (0 axe violations) and reduced-motion behavior.

### E4. Features and status

| Feature | Status | Verified how |
|---|---|---|
| 7 pages generated from shared parts | Working, published | Fresh rebuild reproduces all 7 pages byte for byte (`checkpoint.py`) |
| Net sheet | Working | Formulas read from `js/site.js` on Oct 21; **not yet validated against test cases** (Session 11) |
| Compare table, FAQ, picker, menu, action bar | Working | axe scans and visual checks at 4 viewports |
| GHL form + booking | Embedded | **Unverified** (cannot load in the workspace); live fetch shows the iframe link only |
| Structured data | LocalBusiness with the two founders (home, contact), FAQPage (home, options, new homes), BreadcrumbList (options, our story, new homes, contact) | Every block parsed as valid JSON on Oct 21; no reviews, ratings, price range, hours or awards (none invented). `areaServed` needs real places (claim 2). |
| Facebook integration | Working | Live fetch of Home, Options and Contact reports the header, footer and in-page links. The phone-menu row (`mnav-fb`) is in the page source, but the fetch summary did not list it, so it is not confirmed live; check it on a phone |
| Legal pages | Draft | Not lawyer-reviewed |
| Homes gallery | **Not built** (Jeremy's idea Oct 21) | See Session 10 |
| Analytics, sitemap, robots, canonical | Not built | Session 13 |

### E5. Phase 0 audit: new site vs. Joey's live site

| | Joey's site (glphomeoptions.com) | New site (this project) |
|---|---|---|
| Pages | Home, About, Options, Calculator, Contact Us, Terms, Privacy | Home, Your options, Our story, New homes, Contact, Terms, Privacy |
| Home | Hero, 3 values, 4 path cards ("Learn more" jumps to the form), 3 steps, local blurb, closing CTA. No numbers, no stories. | Hero with photo, proof strip, 3 paths and a fit picker, September story, how it works, compare table, net sheet, riverfront band, about, new homes teaser, FAQ, contact |
| Calculator | Separate page: inputs address, price, payoff, commission %, closing $; sample result $127,000; disclaimer "Estimates are for informational purposes only." | Net sheet on the home page: listing vs. direct side by side, with repairs, carrying costs and months to sell; symmetric verdict; disclaimer |
| Contact | Phone, email, "Chattanooga, TN"; 8-field form with unfilled text-consent placeholders and example.com links | Same GHL form embedded, plus call, text, email, book and Facebook tiles; real on-site policy links |
| Legal | Privacy (9 sections), Terms (10), "Legal entity: GL Partners LLC" | Plain-words rewrites (draft), same URLs |
| Social proof | None | None, by rule (Facebook: 0 reviews) |
| Facebook | Not linked | Linked on every page (3 to 7 links per page; the logo button is in the header) |
| Accessibility | Not audited by us | axe: 0 violations on all pages and viewports |

**Strongest elements today:** a clear story and one action per page; an honest compare table and net sheet that never claim one path is always better; real project photos (a closing, a build in progress); light pages (a first view is roughly 80 to 400 KB; New homes is the heaviest at about 560 KB because of its four build photos); a clean accessibility baseline; a one-source builder that prevents drift; Facebook integrated; structured data with nothing invented.

**Weaknesses:** claims not in Joey's materials (`CONTENT_CLAIMS.md`); no social proof to show; ~800px photos, a 240×132 raster logo, and a 900×225 riverfront panorama that is soft when shown full width; GHL form consent placeholders, and its look is set inside GoHighLevel so we could not check it; 19 breakpoints, no spacing scale, no motion tokens; only one hero composition explored; a long home page that repeats tile-card grids; cool palette with little explicit warmth; no analytics, sitemap or canonical; no manual keyboard or screen-reader pass; Chromium only.

**Opportunities:** the homes gallery; real photos and a short video of Joey and Ethan; Google Business Profile and real reviews; situation and city pages for local search; GHL follow-up automation; the custom domain; responsive images and a Lighthouse pass; a downloadable seller checklist.

### E6. Testing performed (Oct 21) and what is unverified

| Check | Result |
|---|---|
| `python tools/check-links.py` | 7 pages, 339 links, all resolve, no duplicate ids |
| `python tools/checkpoint.py` | Fresh build reproduces all 7 saved pages exactly |
| axe-core (`tools/a11y-check.py`) | 0 violations on all 7 pages at 1440, 820, 390 (touch) and 390 reduced motion; phone menu open and picker pressed also 0 |
| Contrast scan, 4 new pages, desktop and phone | All text meets 4.5:1 (3:1 large) |
| Page weight (measured in Chromium against a local copy: gzip-compressed text + fonts + the images that load without scrolling) | Files: HTML 14 to 52 KB each; CSS 61 KB (13 KB gzip); JS 13 KB (4.5 KB gzip); two fonts 73 KB. **First view, desktop / phone:** Home 298 / 196 KB; Options 126; Our story 403 / 326; New homes 560; Contact 123; Privacy and Terms about 78. Photos are the main cost (JPEG, ~800px); Session 12 adds responsive images and a modern format. |
| Tap-target sizes (non-inline links, buttons, inputs, FAQ rows; all 7 pages) | Nothing is under WCAG 2.2 AA's 24px minimum. Buttons, inputs and FAQ rows are 46px or taller. Desktop footer links are 36px tall and header/breadcrumb links 32px; on phones, breadcrumb links are 32px and the phone-number text link on Our story is 40px. The 44px best-practice target is not fully met (P5, Session 12). |
| Live site | Home, Options and Contact fetched Oct 21: robots tag, H1s, nav, Facebook links and the corrected Contact headings match the repo. (Page-level read of the fetched text, not a byte comparison.) |
| Joey's live site, re-read Oct 21 | Home sections, four path cards that jump to the form, no statistics or reviews; Calculator inputs and the $127,000 sample with its one-line disclaimer; Terms and Privacy naming "GLP Home Options (Legal entity: GL Partners LLC)"; legal URLs `/privacy-policy` and `/terms-of-service`. |
| Contact details vs. Joey's site and Facebook | Phone, email, entity and PO Box verified (the PO Box is on Facebook only; see `CONTENT_CLAIMS.md`) |

**Not verified:** the GHL form and booking; real phones; Safari/Firefox; keyboard-only and screen-reader walkthrough; Lighthouse; 320px width; print; net sheet against test cases.

### E7. Known defects and cautions

See the risk table above and `CONTENT_CLAIMS.md`. No known broken links, console errors from our code, or accessibility violations. Some links are smaller than the 44px best-practice size (footer 36px and breadcrumbs 32px on desktop; breadcrumbs 32px on phones); all meet WCAG 2.2 AA's 24px minimum. See the tap-target row in E6.

## F. Session log

### Session 0: before the plan (reconstructed Oct 21, from chat summaries and `.git/logs/HEAD`)

- **Oct 20 evening to Oct 21 about 1:30 AM.** Read Joey's live site and Facebook; built a single-file page, then a light redesign in the logo's colors with shared CSS/JS, Privacy and Terms pages, share card, favicons and the accessibility test tool. Commits (CDT): `669bec7` "first commit" (12:22 AM), `524b3cb` "first big edit" (12:44), `9001c17` "Big facelift" (1:32).
- **Oct 21, 7:54 to 8:34 AM.** After Jeremy's morning request, benchmarked best-in-class sites; built the shared page builder and four new pages (Your options, Our story, New homes, Contact); added the Facebook logo placements; moved the nav collapse to 1160px; fixed layout bugs found in screenshots; ran link, accessibility and contrast checks; rewrote the notes. Jeremy committed `b6cc372` "Full refresh" at 8:34 AM and synced; the site is live.

### Session 1: Oct 21, 2026, Phase 0 audit and safe foundation

- **Objective:** establish the baseline and the persistent plan; no site changes.
- **Work completed:** verified the live site, repository and Joey's live pages; audited code, tokens, features, page weights and claims; verified the contact details; wrote this file, `ROADMAP.md`, `DESIGN_SYSTEM.md`, `CONTENT_CLAIMS.md` and `SESSION_HANDOFF.md`; added `tools/checkpoint.py` and recorded Checkpoint 1; turned `PICKUP.md` into a pointer; updated `README.md`; logged Jeremy's gallery idea.
- **Files changed:** created `PROJECT_STATUS.md`, `ROADMAP.md`, `DESIGN_SYSTEM.md`, `CONTENT_CLAIMS.md`, `SESSION_HANDOFF.md`, `CHECKPOINT.json`, `tools/checkpoint.py`; modified `README.md` and `PICKUP.md`. **No HTML, CSS or JavaScript changed.**
- **Tests:** see E6.
- **Decisions made:** treat the existing build as the baseline rather than start over; `PROJECT_STATUS.md` is authoritative and `PICKUP.md` is retired; leave the unverified claims on the draft for Session 2 rather than editing during an audit session (the site is `noindex`).
- **Outstanding:** D1 to D6 await approval; six "fix first" claims; Joey's answers; GHL form fix; the gallery.
- **Exact next task:** Session 2, see `SESSION_HANDOFF.md`.

## G. Immediate handoff

- **Current phase and status:** Phase 0 complete at Checkpoint 1. Phase 1 is re-opened as review and approval.
- **Next task:** Session 2, decisions intake and accuracy patch. Full instructions, where to start in the code, what not to change, and how to verify completion are in **`SESSION_HANDOFF.md`**.

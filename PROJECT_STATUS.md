# GLP Home Options website: PROJECT STATUS

**Start here every session.** This file is the map. The code is the truth. If they disagree, believe the code, then fix this file.

_Last updated: Oct 21, 2026, Session 2 (decisions intake and accuracy patch), Checkpoint 2._

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
- **Deployed state (checked Oct 21):** GitHub Pages serves the site from commit **`b6cc372` "Full refresh"** (8:34 AM CDT, the last commit that changed a page). Commit **`5091df7` "Checkpoint 1: Phase 0 audit and project record"** (9:08 AM CDT) added only the notes and the checkpoint tool. After the 8:34 AM publish, fetching `/` and `/contact.html` returned the new multi-page site: nav, H1s ("Real home options. Clear next steps." and "Let's talk about your home. No pressure, no scripts."), the Facebook links and `noindex, nofollow`. That is a page-level check by reading the fetched text; a byte-for-byte comparison is not possible from the workspace (its shell can't reach github.io). **Checkpoint 2 (the Session 2 accuracy patch) is the next commit.** At the start of Session 3, check whether it is live: once it is, the footer reads "Serving Chattanooga, TN" (it used to say "Serving Chattanooga and the surrounding counties").
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

**Approval status (updated Oct 21, Session 2):** Jeremy has *directed* the overall direction (light, logo colors, back off the green, classy and alive, mobile first, Facebook logo, no invented claims) and, on Oct 21, **explicitly approved D1, D4, D5 and the claims approach** below. D2, D3 and D6 proceed by default: he was told the plan on Oct 21 and did not object, and he sees the result in the Session 3 prototypes. Everything else in the code is BUILT, pending Session 4's formal lock.

### Decisions (Phase 1)

| # | Decision | Status |
|---|---|---|
| **D1** | **Color hierarchy.** Navy leads, green is the accent (as built), versus a deep-green-led palette. | **APPROVED Oct 21: navy leads, green accent.** The hex values in `DESIGN_SYSTEM.md` section 2 are now locked tokens; changing one needs Jeremy's approval. |
| **D2** | **Warmth.** Test one warm neutral (sand/cream) surface beside the cool palette. | Proceeding by default: test it **only inside the hero prototypes** (Session 3), not site-wide. Jeremy confirms when he sees them. |
| **D3** | **Typography.** Plus Jakarta Sans plus the Fraunces italic accent. | Proceeding by default: keep. A serif headline may appear in at most one hero prototype. |
| **D4** | **Hero.** Build two prototypes to compare: **A, people-led** (Joey and Ethan in the gable frame, as built) and **B, numbers-led** (net sheet or compare table in the hero, smaller photo). | **APPROVED Oct 21: build both.** Jeremy picks after seeing them (Session 3). |
| **D5** | **Glass and motion.** Glass blur is used in 7 places; motion includes ridge and photo parallax, blobs, count-up and view transitions. | **APPROVED Oct 21 as a direction: restrained set.** Keep header glass, small overlays on photos, and the ridge and contour touches; drop the floating blobs and photo parallax. Session 4 sets the exact list of the 7 glass uses that stay; Session 5 applies it. |
| **D6** | **Architecture and gallery.** Five pages (Home, Your options, Our story, New homes, Contact), New homes a light teaser; where the homes gallery goes. | Structure: proceeding by default (Jeremy published it on Oct 21). Gallery placement (inside New homes, its own "Our work" page, or the future construction site) is decided after Joey sends photos and answers (Session 10). |
| **Claims** | How to treat the six unverified claims (`CONTENT_CLAIMS.md`, "Fixed in Session 2"). | **APPROVED Oct 21: "Joey's own words now."** Replace with his wording and pull what isn't verified; restore a claim only when Joey confirms it. Done in Session 2 (see the session log). |

## D. Roadmap summary, open questions and risks

Roadmap: see **`ROADMAP.md`** (13 sessions to launch). Phase status: 0 done; 1 partly approved (D1, D4, D5 approved; the hero choice is pending); 2 to 6 built but need review, consolidation or validation; 7 not started. **Next: Session 3, hero prototypes A and B** (see `SESSION_HANDOFF.md`).

### Open questions (ask Joey; claim-related ones are in `CONTENT_CLAIMS.md`)

1. **The six claims patched in Session 2 need Joey's real answers before any of them can come back** (`CONTENT_CLAIMS.md`, rows 1 to 6 and 41): does GLP actually offer seller financing or lease options; which counties and towns; is the consultation free; is he reachable at all hours, and does (423) 451-5707 take texts; is there a registered trade name (DBA); is he comfortable with the example $255,000 (85%) offer.
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
| Unconfirmed claims on the draft | The six "fix first" claims were pulled or reworded to Joey's own words in Session 2. What is left (marked OURS or FB in `CONTENT_CLAIMS.md`) still needs Joey's OK | Joey's answers; site is `noindex` meanwhile |
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
| Structured data | LocalBusiness with the two founders (home, contact), FAQPage (home, options, new homes), BreadcrumbList (options, our story, new homes, contact) | Every block parsed as valid JSON on Oct 21; no reviews, ratings, price range, hours or awards (none invented). `areaServed` is the single city "Chattanooga, TN" until Joey lists real counties and towns (claim 2). |
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

**Weaknesses:** some claims still need Joey's OK (`CONTENT_CLAIMS.md`; the six worst were fixed in Session 2); no social proof to show; ~800px photos, a 240×132 raster logo, and a 900×225 riverfront panorama that is soft when shown full width; GHL form consent placeholders, and its look is set inside GoHighLevel so we could not check it; 19 breakpoints, no spacing scale, no motion tokens; only one hero composition explored; a long home page that repeats tile-card grids; cool palette with little explicit warmth; no analytics, sitemap or canonical; no manual keyboard or screen-reader pass; Chromium only.

**Opportunities:** the homes gallery; real photos and a short video of Joey and Ethan; Google Business Profile and real reviews; situation and city pages for local search; GHL follow-up automation; the custom domain; responsive images and a Lighthouse pass; a downloadable seller checklist.

### E6. Testing performed (Oct 21) and what is unverified

| Check | Result |
|---|---|
| `python tools/check-links.py` | 7 pages, 340 links, all resolve, no duplicate ids (re-run after the Session 2 patch) |
| `python tools/checkpoint.py` | Fresh build reproduces all 7 saved pages exactly |
| axe-core (`tools/a11y-check.py`) | 0 violations on all 7 pages at 1440, 820, 390 (touch) and 390 reduced motion; phone menu open and picker pressed also 0. **Re-run after the Session 2 patch: "all clear", same result.** |
| Contrast scan, 4 new pages, desktop and phone | All text meets 4.5:1 (3:1 large) |
| Page weight (measured in Chromium against a local copy: gzip-compressed text + fonts + the images that load without scrolling) | Files: HTML 14 to 52 KB each; CSS 61 KB (13 KB gzip); JS 13 KB (4.5 KB gzip); two fonts 73 KB. **First view, desktop / phone:** Home 298 / 196 KB; Options 126; Our story 403 / 326; New homes 560; Contact 123; Privacy and Terms about 78. Photos are the main cost (JPEG, ~800px); Session 12 adds responsive images and a modern format. |
| Tap-target sizes (non-inline links, buttons, inputs, FAQ rows; all 7 pages) | Nothing is under WCAG 2.2 AA's 24px minimum. Buttons, inputs and FAQ rows are 46px or taller. Desktop footer links are 36px tall and header/breadcrumb links 32px; on phones, breadcrumb links are 32px and the phone-number text link on Our story is 40px. The 44px best-practice target is not fully met (P5, Session 12). |
| Live site | Home, Options and Contact fetched Oct 21: robots tag, H1s, nav, Facebook links and the corrected Contact headings match the repo. (Page-level read of the fetched text, not a byte comparison.) |
| Joey's live site, re-read Oct 21 | Home sections, four path cards that jump to the form, no statistics or reviews; Calculator inputs and the $127,000 sample with its one-line disclaimer; Terms and Privacy naming "GLP Home Options (Legal entity: GL Partners LLC)"; legal URLs `/privacy-policy` and `/terms-of-service`. |
| Contact details vs. Joey's site and Facebook | Phone, email, entity and PO Box verified (the PO Box is on Facebook only; see `CONTENT_CLAIMS.md`) |
| **Session 2 patch checks** | A search of all pages, the builder, the legal text and the scripts finds none of the removed wording (seller financing, lease options, surrounding counties, doing business as, free consultation, "no obligation, ever", anytime). A text diff of the rebuilt pages shows only the planned changes. Every JSON-LD block parses, and the FAQ items in the structured data match the visible FAQ lists. 24 screenshots of every changed area at 1440 and 390 (touch) show no wrapping or layout problems. At the net sheet's defaults, read in a browser, listing nets $112,000 and the $255,000 example offer nets $105,000 (verdict: "Listing nets about $7,000 more."). |

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

### Session 2: Oct 21, 2026, decisions intake and accuracy patch

- **Objective:** record Jeremy's decisions and take the six unverified claims off the draft. No visual change.
- **Decisions Jeremy made (about 9:10 AM):** claims, **"Joey's own words now"**; D1, navy leads with green as the accent (approved, hex values locked); D4, build both hero prototypes (A people-led, B numbers-led) and he picks; D5, a restrained set of glass and motion (approved as a direction). D2, D3 and D6 proceed by default. Recorded in section C, `DESIGN_SYSTEM.md` and `ROADMAP.md`.
- **Work completed:** the six claims were replaced with Joey's own wording or pulled, in the page copy, FAQs, structured data, footer, page descriptions and the legal pages' mailing address. In plain words:
  - Seller financing and lease options are no longer mentioned anywhere (the "Yes" FAQ and both explainers are gone). Joey's sentence, "For unique situations where the standard paths don't feel like a fit, we explore structured options together," is used instead, and the Options page shows a plain three-step "How it works".
  - "Chattanooga and the surrounding counties" is now "Chattanooga, TN"; the structured data lists the city only.
  - "Doing business as" is now Joey's own "GLP Home Options (Legal entity: GL Partners LLC)".
  - "Free consultation" and "no obligation, ever" are now "Request a consultation" and "No obligation, no spam. Your information is kept confidential."
  - "Call or text anytime" is now "Call or text."
  - The $255,000 example offer stays, with a clearer label. "Takes about a minute" came off the contact-form pitch (it stays for our own net sheet).
- **Files changed:** `tools/build-pages.py`, `tools/legal_text.py`, `tools/pages/index.html`, `options.html`, `about.html`, `contact.html`; all 7 generated pages (rebuilt, not hand-edited); `CONTENT_CLAIMS.md`, `PROJECT_STATUS.md`, `DESIGN_SYSTEM.md`, `ROADMAP.md`, `SESSION_HANDOFF.md`, `CHECKPOINT.json`. No CSS or JavaScript changed (`CSS_V` and `JS_V` stay at 18 and 7).
- **Tests:** see E6 (rebuild reproduces the pages, 340 links, axe all clear at 4 viewports, no old wording left, JSON-LD parses, 24 screenshots reviewed).
- **Outstanding:** Joey's answers (see open question 1 and the rest of that list); the GHL form; the hero choice (Session 3).
- **Exact next task:** Session 3, hero prototypes A and B, see `SESSION_HANDOFF.md`.

## G. Immediate handoff

- **Current phase and status:** Phase 0 complete. Phase 1 is partly approved (D1, D4, D5); the accuracy patch is done and recorded at Checkpoint 2. The hero choice (D4) is pending.
- **Next task:** Session 3, two hero prototypes (A people-led, B numbers-led) built in isolation, plus the one warm-surface test (D2). Full instructions, where to start in the code, what not to change, and how to verify completion are in **`SESSION_HANDOFF.md`**.

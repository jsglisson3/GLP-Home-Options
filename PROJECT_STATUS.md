# GLP Home Options website: PROJECT STATUS

**Start here every session.** This file is the map. The code is the truth. If they disagree, believe the code, then fix this file.

_Last updated: Oct 21, 2026, Session 6c (the top half and the header: sharper, warmer hero photo, slimmer frame, simpler header; the dead prototype files are gone), Checkpoint 9._

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
- **Deployed state (checked Oct 21):** GitHub Pages serves the site from commit **`b6cc372` "Full refresh"** (8:34 AM CDT, the last commit that changed a page). Commit **`5091df7` "Checkpoint 1: Phase 0 audit and project record"** (9:08 AM CDT) added only the notes and the checkpoint tool. After the 8:34 AM publish, fetching `/` and `/contact.html` returned the new multi-page site: nav, H1s ("Real home options. Clear next steps." and "Let's talk about your home. No pressure, no scripts."), the Facebook links and `noindex, nofollow`. That is a page-level check by reading the fetched text; a byte-for-byte comparison is not possible from the workspace (its shell can't reach github.io). **Checkpoint 2 (`8124c77` "Text changes", 9:28 AM) and Checkpoint 3 (`73b0b53` "Updated wording and countys", 9:46 AM) are live** (confirmed Oct 21 by fetching the Contact page with a cache-busting query: the address block reads "GLP Home Options (Legal entity: GL Partners LLC)"). **Checkpoint 4 (Session 3: `proto-hero-a.html`, `proto-hero-b.html`, `css/proto.css`, `js/proto.js`, `tools/build-prototypes.py`, two small avatar images, and the docs) is saved on Jeremy's computer and goes live with his next commit.** It is additive and `noindex`; no real page changed. **Checkpoint 5 (Session 3b polish) is saved on Jeremy's computer and goes live with his next commit, together with Checkpoint 4 if that is not yet pushed. Unlike Checkpoint 4 it changes real pages:** the Home hero is warm cream, the floating blobs and photo drift are gone, and the 320px header fits. **Checkpoints 6 and 7 (Session 6a, the landing page's top half) are saved on Jeremy's computer and go live with his next commit, together with any earlier checkpoint not yet pushed.** **Checkpoints 6 to 9 (Sessions 6a to 6c: hero A live, seamless header, phone faces, cream across the whole site, floating hero tags removed, sharper hero photo, simpler header) are saved on Jeremy's computer and go live with his next commit. The picture he sent at 4:39 PM CT was a stale browser tab (he said at 4:55 PM he had not refreshed, and the new version "looks better"). At 4:55 PM he also confirmed he had deleted the five dead prototype files (`proto-hero-a.html`, `proto-hero-b.html`, `css/proto.css`, `js/proto.js`, `tools/build-prototypes.py`); the workspace copy was removed to match.**
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

**Approval status (updated Oct 21, Session 3):** Jeremy has *directed* the overall direction (light, logo colors, back off the green, classy and alive, mobile first, Facebook logo, no invented claims) and, on Oct 21, **explicitly approved D1, D4, D5 and the claims approach** below. **On Oct 21 in Session 3 (about 10:20 AM) he also chose hero A (people-led) and the warm cream surface behind the hero only (D4, D2).** D3 and D6 proceed by default: he was told the plan on Oct 21 and did not object. Everything else in the code is BUILT, pending Session 4's formal lock.

### Decisions (Phase 1)

| # | Decision | Status |
|---|---|---|
| **D1** | **Color hierarchy.** Navy leads, green is the accent (as built), versus a deep-green-led palette. | **APPROVED Oct 21: navy leads, green accent.** The hex values in `DESIGN_SYSTEM.md` section 2 are now locked tokens; changing one needs Jeremy's approval. |
| **D2** | **Warmth.** Test one warm neutral (sand/cream) surface beside the cool palette. | **APPROVED Oct 21 (Session 3), for the hero surface only:** `--cream: #f6f0e3`, used as the hero background gradient `#fdfbf6 → #f6f0e3 → #efe8d8`; the ridge's two back layers stay cool. **EXTENDED Oct 21, 4:35 PM (Session 6b): Jeremy said "yes on the cream", so cream is the site's one tint:** every hero (all pages), the alternate sections (white and cream alternate), the strip under the Home hero, the footer and the small tinted controls; the cool mist and mint tints are retired. Live in `css/site.css`: `--cream #f6f0e3` (hero), `--cream-100 #f8f3e7` (section bands, footer), class `.sec-cream`. |
| **D3** | **Typography.** Plus Jakarta Sans plus the Fraunces italic accent. | Proceeding by default: keep. A serif headline may appear in at most one hero prototype. |
| **D4** | **Hero.** Build two prototypes to compare: **A, people-led** (Joey and Ethan in the gable frame, as built) and **B, numbers-led** (net sheet or compare table in the hero, smaller photo). | **APPROVED Oct 21 (Session 3): A, people-led.** Both were built and shown (desktop and phone, cool and warm). B (numbers-led) was not chosen; it stays in the repo until Session 6 for reference, then is deleted. Jeremy's note on A: the floating tags looked random, so they were rebuilt on five rules (`DESIGN_SYSTEM.md`, "Hero tag system"). |
| **D5** | **Glass and motion.** Glass blur is used in 7 places; motion includes ridge and photo parallax, blobs, count-up and view transitions. | **APPROVED Oct 21 as a direction: restrained set.** Keep header glass, small overlays on photos, and the ridge and contour touches; drop the floating blobs and photo parallax. Session 4 sets the exact list of the 7 glass uses that stay; Session 5 applies it. |
| **D6** | **Architecture and gallery.** Five pages (Home, Your options, Our story, New homes, Contact), New homes a light teaser; where the homes gallery goes. | Structure: proceeding by default (Jeremy published it on Oct 21). Gallery placement (inside New homes, its own "Our work" page, or the future construction site) is decided after Joey sends photos and answers (Session 10). |
| **Claims** | How to treat the six unverified claims (`CONTENT_CLAIMS.md`). | **APPROVED Oct 21: "Joey's own words now."** Done in Session 2. About 9:30 AM Jeremy then answered the open questions himself (yes to all) and asked for five claims to go back; they are on the draft tagged **J** (Jeremy's word, not yet Joey's) until Joey confirms. |

## D. Roadmap summary, open questions and risks

Roadmap: see **`ROADMAP.md`** (13 sessions to launch). Phase status: 0 done; 1 partly approved (D1, D2, D4, D5 approved; hero A chosen; the formal lock is Session 4); 2 to 6 built but need review, consolidation or validation; 7 not started. **Next: Session 4, direction lock** (see `SESSION_HANDOFF.md`).

### Open questions (ask Joey; claim-related ones are in `CONTENT_CLAIMS.md`)

1. **Joey must confirm what Jeremy said for him on Oct 21** (`CONTENT_CLAIMS.md`, tag **J**, rows 1, 2, 4, 5, 6 and 41): that GLP offers seller financing and lease options (and that a lawyer reviews how it is described); the real list of counties and towns (Jeremy: Chattanooga and the surrounding counties within about an hour, including parts of Georgia and Sequatchie); that the first consultation is free; that he is reachable at all hours and (423) 451-5707 takes texts; and that he is comfortable with the example $255,000 (85%) offer. Also: is there a registered trade name (DBA)?
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
| Claims on the draft that rest on Jeremy's word, not Joey's | Seller financing and lease options, the wider service area, the free consultation, "anytime", texting and the example offer went back on the site on Jeremy's word (Oct 21). The first two carry legal weight. What is left (OURS or FB in `CONTENT_CLAIMS.md`) also needs Joey's OK | Joey confirms each (tag J) and a lawyer reviews the seller financing and lease option wording before launch; site is `noindex` meanwhile |
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
| Structured data | LocalBusiness with the two founders (home, contact), FAQPage (home, options, new homes), BreadcrumbList (options, our story, new homes, contact) | Every block parsed as valid JSON on Oct 21; no reviews, ratings, price range, hours or awards (none invented). `areaServed` is the city "Chattanooga, TN" plus one text line, "Counties within about an hour of Chattanooga, in Tennessee and Georgia" (Jeremy's words, claim 2); it should name real counties once Joey lists them. |
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

**Weaknesses:** some claims still need Joey's OK (`CONTENT_CLAIMS.md`; five of them rest on Jeremy's word until Joey confirms); no social proof to show; ~800px photos, a 240×132 raster logo, and a 900×225 riverfront panorama that is soft when shown full width; GHL form consent placeholders, and its look is set inside GoHighLevel so we could not check it; 19 breakpoints, no spacing scale, no motion tokens; only one hero composition explored; a long home page that repeats tile-card grids; cool palette with little explicit warmth; no analytics, sitemap or canonical; no manual keyboard or screen-reader pass; Chromium only.

**Opportunities:** the homes gallery; real photos and a short video of Joey and Ethan; Google Business Profile and real reviews; situation and city pages for local search; GHL follow-up automation; the custom domain; responsive images and a Lighthouse pass; a downloadable seller checklist.

### E6. Testing performed (Oct 21) and what is unverified

| Check | Result |
|---|---|
| `python tools/check-links.py` | 7 pages, 340 links, all resolve, no duplicate ids (re-run after the Session 2 patch) |
| `python tools/checkpoint.py` | Fresh build reproduces all 7 saved pages exactly |
| axe-core (`tools/a11y-check.py`) | 0 violations on all 7 pages at 1440, 820, 390 (touch) and 390 reduced motion; phone menu open and picker pressed also 0. **Re-run after the Session 2 patch and again after Jeremy's answers were applied: "all clear" both times.** |
| Contrast scan, 4 new pages, desktop and phone | All text meets 4.5:1 (3:1 large) |
| Page weight (measured in Chromium against a local copy: gzip-compressed text + fonts + the images that load without scrolling) | Files: HTML 14 to 52 KB each; CSS 61 KB (13 KB gzip); JS 13 KB (4.5 KB gzip); two fonts 73 KB. **First view, desktop / phone:** Home 298 / 196 KB; Options 126; Our story 403 / 326; New homes 560; Contact 123; Privacy and Terms about 78. Photos are the main cost (JPEG, ~800px); Session 12 adds responsive images and a modern format. |
| Tap-target sizes (non-inline links, buttons, inputs, FAQ rows; all 7 pages) | Nothing is under WCAG 2.2 AA's 24px minimum. Buttons, inputs and FAQ rows are 46px or taller. Desktop footer links are 36px tall and header/breadcrumb links 32px; on phones, breadcrumb links are 32px and the phone-number text link on Our story is 40px. The 44px best-practice target is not fully met (P5, Session 12). |
| Live site | Home, Options and Contact fetched Oct 21: robots tag, H1s, nav, Facebook links and the corrected Contact headings match the repo. (Page-level read of the fetched text, not a byte comparison.) |
| Joey's live site, re-read Oct 21 | Home sections, four path cards that jump to the form, no statistics or reviews; Calculator inputs and the $127,000 sample with its one-line disclaimer; Terms and Privacy naming "GLP Home Options (Legal entity: GL Partners LLC)"; legal URLs `/privacy-policy` and `/terms-of-service`. |
| Contact details vs. Joey's site and Facebook | Phone, email, entity and PO Box verified (the PO Box is on Facebook only; see `CONTENT_CLAIMS.md`) |
| **Session 2 checks** | After Jeremy's answers were applied (Checkpoint 3): pages rebuild; 340 links resolve; every JSON-LD block parses and the FAQ data matches the visible FAQ lists (11, 6 and 6 items); axe all clear; no page scrolls sideways at 1440, 390 or 320; screenshots of every changed area at 1440, 390 and 320 were reviewed. Wording kept out of the site: "doing business as", "no obligation, ever", and "takes about a minute" for the form (it stays only for our own net sheet). At the net sheet's defaults, read in a browser, listing nets $112,000 and the $255,000 example offer nets $105,000 (verdict: "Listing nets about $7,000 more."). |
| **Session 3 checks** | Prototypes A and B, cool and warm: axe 0 violations in all 24 scans (16, then 8 more after the tag change) at 1440, 820, 390 touch and 390 reduced motion; 476 links resolve (9 pages); no broken images; no sideways scroll at 1440 and 390; the toggle, its URL state (`?surface=warm`), the A/B links, keyboard use and the phone call bar were tested; A's tags were checked for overlaps and clipping at 1440, 1100, 820, 560, 390 and 320 (none) and every tag label stays on one line. First-view weight (gzipped text, fonts, images): live Home 298 KB desktop / 196 KB phone; A 301 / 200 (the prototype files add about 3 KB); B 243 / 141 (no big photo, two small portraits). The only console errors are the contact-form script, which the workspace cannot reach (same on the live pages). |
| **Session 3b checks (Checkpoint 5)** | Pages rebuilt clean; 476 links, anchors, images and scripts resolve (9 pages including the 2 prototypes); axe 0 violations in all 28 page scans (7 pages at 1440, 820, 390 touch and 390 reduced motion) and in the phone menu and the picker; no sideways scroll and no header overflow at 320, 340 or 360 on all 7 pages; the 320px Menu button is 46 by 46 and keeps its name "Menu"; the email link stays on one line at 320 on Contact and Our story; screenshots reviewed at 1440, 390 and 320 (cream hero, band backgrounds without blobs, the photo band, the narrow header). **Not verified:** a real phone; Joey's own look at the cream. |
| **Session 6a checks (Checkpoints 6 and 7)** | Pages rebuilt clean; 345 links, anchors, images and scripts resolve (9 pages including the 2 redirect pages); axe 0 violations in all 28 page scans (7 pages at 1440, 820, 390 touch and 390 reduced motion) and in the phone menu and the picker (Home scanned again after round two); speed on Home (local; the phone run has the CPU slowed 4 times): largest paint 204 ms on desktop and on phone, layout shift 0 on load and while scrolling (0.0003 on desktop before the constant-height header); screenshots reviewed at 1920, 1440, 1366, 1280, 1160, 1100, 1024, 990, 820, 600, 390 and 320; no tag or caption overlaps at 981, 1024, 1060, 1100, 1160, 1280 or 1440. **Not verified:** a real phone; Joey's own look at the final page. |
| **Session 6b checks (Checkpoint 8)** | Pages rebuilt clean (CSS v26); 341 links, anchors, images and scripts resolve (9 pages including the 2 redirect pages; 4 fewer links than at Checkpoint 7 because the three path chips and the call tag were removed); axe 0 violations in all 28 page scans (7 pages at 1440, 820, 390 touch and 390 reduced motion) and in the phone menu and the picker; no sideways scrolling, broken images or script errors (the small-target notes are the same 28 informational ones as before); text contrast on cream computed for every text color in use (numbers in `DESIGN_SYSTEM.md`); the numbers strip shows its final numbers at 0.3 s after load; screenshots reviewed: the Home top at 1440, 1193 (the width of Jeremy's picture), 1024 and 390, full-page views of Home, About, Options, New homes and Contact at 1440, and the New homes top. **Not verified:** a real phone; Joey's own look; Home and the other pages between 520 and 980px wide below the first screen (only colors changed there); the 320px hero. |
| **Session 6c checks (Checkpoint 9)** | Pages rebuilt clean (CSS v27, JS v9); 339 links, anchors, images and scripts resolve (7 pages; 2 fewer than at Checkpoint 8 because the two old redirect pages were deleted); axe 0 violations in all 28 page scans (7 pages at 1440, 820, 390 touch and 390 reduced motion) and in the phone menu and the picker; the small-target notes are the same informational ones as before (desktop menu links at 36 to 37px; the phone and tablet targets are 44px or more); the build reproduces all 7 saved pages exactly; the hero photo, frame and header were reviewed at 1440 (full view, a 2x close-up of the right side, and the scrolled header). **Not verified:** a real phone; the new photo on a high-resolution screen other than by the 2x close-up; Joey's look at the result. |

**Not verified:** the GHL form and booking; real phones; Safari/Firefox; keyboard-only and screen-reader walkthrough; Lighthouse; 320px width; print; net sheet against test cases.

### E7. Known defects and cautions

See the risk table above and `CONTENT_CLAIMS.md`. No known broken links, console errors from our code, or accessibility violations. Some links are smaller than the 44px best-practice size (footer 36px and breadcrumbs 32px on desktop; breadcrumbs 32px on phones); all meet WCAG 2.2 AA's 24px minimum. See the tap-target row in E6. **At 320px wide** (first looked at in Session 2) no page scrolls sideways, but the email link in the Contact and Our story tiles wraps with a lone "m" on its second line, and the Home hero button wraps to two lines. Cosmetic; fix in Session 12. **Found in Session 3, also at 320px:** the header's logo and Menu button need about 343px, so at 320px the Menu button is clipped by about 23px (fine from about 343px up: checked at 340, 360, 375 and 390). Fix in Session 12 (shrink the wordmark or the button below about 360px). (**Fixed in Session 3b, Checkpoint 5:** the Menu button is icon-only at 350px and narrower; no sideways scroll or header overflow at 320, 340 or 360 on any page.)

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

### Session 2: Oct 21, 2026, decisions intake and accuracy patch (with a second pass, 2b)

- **Objective:** record Jeremy's decisions and take the six unverified claims off the draft. No visual change.
- **Decisions Jeremy made (about 9:10 AM):** claims, **"Joey's own words now"**; D1, navy leads with green as the accent (approved, hex values locked); D4, build both hero prototypes (A people-led, B numbers-led) and he picks; D5, a restrained set of glass and motion (approved as a direction). D2, D3 and D6 proceed by default. Recorded in section C, `DESIGN_SYSTEM.md` and `ROADMAP.md`.
- **Pass 1 (Checkpoint 2):** the six claims were replaced with Joey's own wording or pulled, in the page copy, FAQs, structured data, footer, page descriptions and the legal pages' mailing address.
- **Pass 2b (Checkpoint 3, from about 9:30 AM):** Jeremy answered the questions for Joey himself ("yes" to all five; service area Chattanooga and the surrounding counties, about an hour out, including Georgia and Sequatchie). Restored, in the page sources only: seller financing and lease options (Joey's sentence leads, then the plain-English definitions and the two explainer FAQs); the wider service area (footer, hero pill, FAQ, structured data text); "free" consultation (hero button, and the FAQs that say the first conversation is free); "anytime". The $255,000 example stays. Kept from pass 1: Joey's own "No obligation, no spam. Your information is kept confidential."; his "Legal entity" wording instead of "doing business as"; no "ever"; no "takes about a minute" in the form pitch; the clearer example-offer label. Every restored claim is tagged **J** (Jeremy's word, not yet Joey's) in `CONTENT_CLAIMS.md`.
- **Files changed:** `tools/build-pages.py`, `tools/legal_text.py`, `tools/pages/index.html`, `options.html`, `about.html`, `contact.html`; all 7 generated pages (rebuilt, not hand-edited); `CONTENT_CLAIMS.md`, `PROJECT_STATUS.md`, `DESIGN_SYSTEM.md`, `ROADMAP.md`, `SESSION_HANDOFF.md`, `CHECKPOINT.json`. No CSS or JavaScript changed (`CSS_V` and `JS_V` stay at 18 and 7).
- **Tests:** see E6.
- **Outstanding:** Joey's confirmation of every J claim; a lawyer's review of the seller financing and lease option wording; the GHL form; the 320px wraps (Session 12); the hero choice (Session 3).
- **Exact next task:** Session 3, hero prototypes A and B, see `SESSION_HANDOFF.md`.

### Session 3: Oct 21, 2026, hero prototypes and the hero choice

- **Built (additive, `noindex`):** `tools/build-prototypes.py` reads the built `index.html` and writes `proto-hero-a.html` and `proto-hero-b.html` (only the hero differs), with `css/proto.css`, `js/proto.js` (Cool/Warm toggle, `?surface=warm`) and two avatar crops (`images/joey-avatar.jpg`, `images/ethan-avatar.jpg`, from the Our story portraits). Nothing in `css/site.css`, `js/site.js`, `tools/build-pages.py` or `tools/pages/` changed.
- **A (people-led):** the live hero without the three blobs; photo and tags held still (D5). **B (numbers-led):** a side-by-side card of Joey's own numbers (Timeline, Commission and fees, Closing costs, Repairs, and "Usually nets the most", the row that favors listing, kept on purpose), Joey and Ethan as two small portraits, no big photo; the stats strip is hidden in B because the card carries the same numbers. The build stops if the live table wording changes.
- **Jeremy's feedback (10:07 AM):** the tags on the people version \"look random\". Rebuilt on five rules (see `DESIGN_SYSTEM.md`). This also fixed two phone defects in the live hero: the speed tag covered Ethan's eyes, and the caption ran under the call tag.
- **Decision (about 10:20 AM):** A, people-led, with the warm cream surface behind the hero only.
- **Findings:** the 320px header (E7). The warm cream passes contrast for all small text (numbers in `DESIGN_SYSTEM.md`, P3).
- **Not done (by design):** applying A and the warm hero to the real Home page (Session 6); any warm neutral outside the hero (needs a decision in Session 4); deleting the prototypes (Session 6).
- **Checkpoint 4 written.** **Exact next task:** Session 4, direction lock, see `SESSION_HANDOFF.md`.

### Session 3b: Oct 21, 2026, polish pass while Joey picks the hero (Checkpoint 5)
- **Why:** Jeremy asked for polished improvements everywhere (10:29 AM) and said he really likes the cream: "it looks classy". The hero choice (A or B) is NOT applied to the live Home page, because Joey is picking; only changes that hold either way were made.
- **Changed on the live pages:** (1) The warm cream (D2, approved) is now the Home hero surface: `--cream:#f6f0e3` and `.hero .hero-bg` in `css/site.css`; page heroes keep the cool surface. (2) The D5 trims: the floating blobs are removed everywhere (Home hero, page heroes, call-to-action bands, contact band; markup in `tools/pages/index.html` and `tools/build-pages.py`, rules and the `drift` keyframes in the CSS); the photo-band drift (`.pano` parallax, `--py`) is removed from `js/site.js` and the CSS; the hero photo's slow zoom (`breathe`) and the tags' bobbing (`bob`) are removed. The ridge parallax (`--p`) and the contour lines stay. (3) At 350px and narrower the Menu button shows only its icon and keeps "Menu" as its accessible name, which fixes the 320px header overflow. (4) The email link is slightly smaller at 380px and narrower, so it stays on one line at 320. (5) Breadcrumb links are 44px tall on touch screens. Cache versions are now `CSS_V, JS_V = 19, 8`.
- **Prototypes:** they look the same as before. The Cool button now restores the cool surface through a rule in `css/proto.css` (v=2), because cream is now the live default. `tools/build-prototypes.py` no longer requires blobs in the live hero.
- **Checks:** see E6, "Session 3b checks".
- **Outstanding:** the hero choice (Joey); whether Jeremy wants cream beyond the hero (a question for Session 4); the earlier open items.
- **Exact next task:** Session 4, see `SESSION_HANDOFF.md`.

### Session 6a: Oct 21, 2026 (afternoon), the landing page's top half (Checkpoints 6 and 7)
- **Decision:** Joey picked hero A (people-led) after seeing both prototypes; Jeremy told me at about 4:07 PM CT: "go with the first non numbers option ... you can throw the other out". Hero B is retired. Jeremy also asked for about 25 minutes on the landing page, the header and the top half.
- **Starting point:** at the start of this session the workspace already held hero A applied to the live Home page (the tag system and the three path chips in `css/site.css`, a calm staggered entrance, phone tweaks), edited between 4:04 and 4:05 PM before Jeremy's message and not recorded in any checkpoint. It was reviewed in full, kept and verified here.
- **Done (live pages):** (1) The header no longer shrinks on scroll (constant 80px height, 50px logo), because the old shrink pulled the whole page up by 14px as you began to scroll. On Home the header takes the hero's cream at the top of the page, so there is no seam, and turns to white glass after scrolling (`body:has(.hero) .hdr:not(.scrolled)`). (2) On phones (767px and narrower) a "Joey & Ethan" chip with two small portraits replaces the plain location pill, so their faces are in the first screen (the big photo sits below the fold); markup `.hero-people` in `tools/pages/index.html`, images `images/joey-avatar.jpg` and `images/ethan-avatar.jpg`. (3) Balanced headline line breaks and no one-word last lines in the intro (`text-wrap`). (4) Hero B retired: `proto-hero-a.html` and `proto-hero-b.html` are small redirect pages to the home page (old links still work). `css/proto.css`, `js/proto.js` and `tools/build-prototypes.py` are removed from the build and used by no page; Jeremy can delete those three files and the two redirect pages in VS Code whenever convenient (the AI cannot delete files on his computer). (5) Round two: at 981 to 1100px wide the photo tags and the caption overlapped, so the tags are a little smaller in that range, their labels stay on one line, and on the narrowest laptops (981 to 1010px) the caption keeps the names only. `CSS_V` is 23.
- **Checks:** see E6, "Session 6a checks".
- **Outstanding:** Session 4's direction lock (the exact list of 7 glass uses; a yes or no on cream beyond the hero); Sessions 5 and 7 to 9; Joey's confirmation of the J claims; the earlier open items.
- **Exact next task:** see `SESSION_HANDOFF.md`.

### Session 6b: Oct 21, 2026 (late afternoon), cream across the site and a more professional hero (Checkpoint 8)
- **Decisions from Jeremy:** 4:35 PM: "yes on the cream" (cream beyond the hero). 4:37 PM: a 20-minute timer while he drove, "really do your best to knock out the next phase of the landing page". 4:39 PM, with a picture of the hero: the floating tags on the photo "look tacky" and "some other header options look a little gimmicky, I need to look professional". I read "header options" as the decorative items at the top of the page and removed them; **what else he meant is a question for him (see `SESSION_HANDOFF.md`).**
- **Done (live pages):** (1) **Cream is the site's one tint (D2 extended):** `.sec-mint` and `.sec-mist` became `.sec-cream` (`#f8f3e7`) on all pages; white and cream alternate (About's story section went white so two cream sections do not touch); every hero (`.hero-bg`, the legal-page hero) is the cream gradient; the strip under the Home hero, the footer, the picker, the FAQ side cards (now white), the comparison-table header and the phone-menu Facebook card follow. The header takes the hero's cream at the top of every page (`body:has(.hero,.phero,.doc-hero)`). `--mist` is removed. (2) **Floating tags removed** from the Home and New homes hero photos (they covered the picture and repeated the numbers strip); the photo keeps one solid white name plate. The tag system CSS is deleted. (3) The pulsing "live" dot pill became the standard small-caps eyebrow; the three path chips under the intro are gone (the intro sentence keeps the three paths); on phones the Joey & Ethan chip is now a plain byline (no pill). (4) Buttons: softer shadow and no shine sweep; the "Coming soon" dot no longer pulses. (5) The numbers strip no longer counts up: for a moment it showed "3–3 days" and "0 paths", which is not true; the final numbers now show at once (the count-up code in `js/site.js` is unused; remove it in Session 5).
- **Not changed:** copy, claims, links (the 4 removed links were the three path chips and the call tag), the stats strip, the ridge and contour lines, the glass on the header and the dark bands.
- **Checks:** see E6, "Session 6b checks".
- **Outstanding:** Jeremy's answer on what else looked gimmicky; Session 4's glass list; Sessions 5 and 7 to 9; Joey's confirmation of the J claims; the earlier open items. At 1024px wide the two hero buttons stack (as before); worth a look in Session 5.
- **Exact next task:** see `SESSION_HANDOFF.md`.

### Session 6c: Oct 21, 2026 (late afternoon), the top half and the header, "absolutely perfect" (Checkpoint 9)
- **Decisions from Jeremy:** 4:54 PM, "whats the next section to focus on another 10 minute chunk?"; 4:55 PM, about the hero picture on the right, "i need this whole right part of this top section to be incredible"; 4:56 PM, "spend all your energy on this top 50% ... and the header as well, everything needs to be flawless" (so the next section was not started; the chunk went to the hero and the header). He deleted the five dead prototype files at about 4:55 PM.
- **Finding:** the hero photo is the limit. The only file is 800 x 600 (`research/photos/from-old-build/joey-ethan-walnut-street-bridge-800x600.jpg`); at 2x it was being stretched, so it looked soft, and the faces take up only the top third of the frame. A better result needs a larger original or a new portrait from Joey.
- **Done (live pages):** (1) The hero photo is resampled with Lanczos, lightly sharpened and warmed: `images/joey-ethan-bridge.jpg` (800 x 600, normal screens) and new `images/joey-ethan-bridge-2x.jpg` (1600 x 1200, sharp screens), picked by `srcset`; the preload link carries the same set. The original stays in `research/`. (2) The gable frame is slimmer on every page (7px line and 7px white mat; was 9 and 8) and the photo has a soft shade at the bottom behind the name plate. (3) The header is simpler: the phone number is plain text with a small green phone glyph (no pill, no dark circle), the Facebook logo has no circle, and the scroll-progress line under the header is removed (markup, CSS and the two JS lines). Tap targets are still 46px.
- **Not changed:** copy, claims, layout of the hero, the numbers strip, the other sections.
- **Checks:** see E6, "Session 6c checks".
- **Outstanding:** ask Joey for the original photo file or a new portrait shot (at least 1600px tall, ideally the two of them from the waist up with space above their heads); Jeremy's answer on what else looked gimmicky; Session 4's glass list; the earlier open items.
- **Exact next task:** see `SESSION_HANDOFF.md`.

## G. Immediate handoff

- **Current phase and status:** Phase 0 complete. Phase 1 is partly approved (D1, D2, D4, D5); the hero is chosen (A, people-led, warm cream) and recorded at Checkpoint 4 (Session 3). The accuracy work was recorded at Checkpoint 3. Session 3b (Checkpoint 5) then put the cream and the D5 trims on the live site; the hero A/B choice is still not applied there (Joey is picking; Session 6). Session 6a (Checkpoints 6 and 7): Joey chose hero A, it is applied to the live Home page with a refined header; hero B is retired. Session 6b (Checkpoint 8): Jeremy approved cream beyond the hero, so cream is the site's one tint (heroes, alternate sections, footer); the floating hero tags, the pulsing pill, the path chips and the button shine were removed for a more professional look. Session 6c (Checkpoint 9): the hero photo was sharpened and warmed, the frame slimmed, the header simplified; the photo's 800 px source is now the limit (ask Joey for a bigger original).
- **Next task:** Session 4, lock the direction: label every design-system item DIRECTED or APPROVED, and set the exact list of the 7 glass uses (D5). Full instructions are in **`SESSION_HANDOFF.md`**.

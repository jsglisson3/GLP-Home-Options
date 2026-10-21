# GLP Home Options: roadmap

**The plan for the whole project, session by session.** Authoritative for sequencing and acceptance criteria. Status lives in `PROJECT_STATUS.md`; the next session's exact task lives in `SESSION_HANDOFF.md`.

Rules this plan follows (from the master plan): sessions are **30 to 45 minutes**; one primary objective per session; every session ends at a verified checkpoint with updated documents; never start a new phase just because time is left; changes to creative direction, scope or major architecture need Jeremy's approval.

## Where we really are

The master plan assumes a clean start. This project did not start clean: earlier sessions (before the plan existed) already built a working draft with a design system, five content pages, a calculator and a deployment. So the phases below are marked with what **exists** versus what is **approved**. We do not redo built work; we review it, approve or adjust it, then refine it.

| Phase | What exists today | Status |
|---|---|---|
| 0 Audit and safe foundation | Audit done, project record created, checkpoint tool added | **Done in Session 1** |
| 1 Creative direction and visual design | A complete direction is *built* (light, navy and green from the logo, Plus Jakarta Sans + Fraunces italic accent, gable photo frame). One hero composition only. No formal approval. | **Partly approved Oct 21** (D1, D2, D4, D5); D3, D6 proceed by default; hero A (people-led) chosen with a warm cream hero surface (Session 3); the formal lock is Session 4 |
| 2 Design system and foundation | Tokens and components exist in `css/site.css` (19 breakpoints, no spacing scale, no motion tokens) | Built, needs consolidation |
| 3 Homepage structure | Five pages built and published (Home, Your options, Our story, New homes, Contact) | Built, needs approval |
| 4 Section refinement | Sections exist; several need a review for repetition. The accuracy patch is done (Session 2). | Partly done |
| 5 Function and integration | Net sheet works but is not validated against test cases. GHL form embedded but unverified and its consent text has placeholders. | Partly done |
| 6 Accessibility, responsive, performance | Accessibility baseline is clean (axe: 0 violations). Performance never measured with Lighthouse. No manual keyboard or screen-reader pass. | Partly done |
| 7 Final QA and deployment | Draft is live on GitHub Pages as `noindex`. Not launch-ready. | Not started |

## Session plan

Each session is sized for 30 to 40 minutes. "Postponing" lists what we deliberately do not touch.

### Session 1: Phase 0 audit (done, Oct 21)
Verified the live site and repo, audited code, design tokens, claims and weights, wrote the project record, added `tools/checkpoint.py`. No site changes.

### Session 2: Decisions intake and accuracy patch (Phase 4, content accuracy) (done, Oct 21)
- **Goal:** record Jeremy's answers to D1 to D6 (see `PROJECT_STATUS.md` section C; recorded Oct 21), then make the site match what Joey has actually confirmed. Jeremy chose "Joey's own words now": use his wording and pull what isn't verified.
- **Do:** fix the six "Fix first" rows in `CONTENT_CLAIMS.md`. Where Joey hasn't answered, use Joey's own wording or the conservative option: seller financing/lease options (remove or neutralize; affects the FAQ list in `tools/build-pages.py`, `tools/pages/options.html`, `index.html`, `about.html`, page descriptions, JSON-LD), "surrounding counties" (use "Chattanooga, TN"), "doing business as", "free"/"ever", "anytime", example offer.
- **Success:** every "??" row resolved or softened; pages rebuilt; `python tools/checkpoint.py --write` passes; Jeremy publishes.
- **Postponing:** any visual change.
- **Result:** all six rows reworked to Joey's own wording or pulled, then (Jeremy's answers, about 9:30 AM) five restored and tagged J; 7 pages rebuilt; links, axe and screenshots checked; Checkpoints 2 and 3 written. Joey still has to confirm every J claim.

### Session 3: Phase 1, hero exploration
- **Goal:** compare two meaningfully different hero compositions as isolated prototypes (not touching the live hero): **A, people-led** (Joey and Ethan in the gable frame, as built) and **B, numbers-led** (net sheet or compare table in the hero, smaller photo). Also test one warm neutral surface (P3).
- **Success:** both prototypes viewable at desktop and phone; Jeremy picks one (D4).
- **Postponing:** applying the choice to the live pages.
- **Result (Oct 21, done):** both prototypes built and checked (`PROJECT_STATUS.md`, E6 and the Session 3 log). Jeremy chose **A, people-led** and the **warm cream hero surface**. His feedback turned the floating tags into a five-rule system (`DESIGN_SYSTEM.md`). B is deleted in Session 6.

### Session 4: Phase 1, direction lock
- **Goal:** turn D1 to D6 plus the hero choice into the approved design system (`DESIGN_SYSTEM.md` marks items APPROVED). Also set the exact list of the 7 glass uses that stay (D5).
- **Success:** every token and rule is labeled DIRECTED or APPROVED; open items listed.
- **Inputs from Session 3:** hero A, the warm cream hero surface and the tag system are decided. Session 4 also asks whether any other section gets a warm neutral, and counts the hero tags and caption among the glass uses.

### Session 5: Phase 2, design system consolidation
- **Goal:** tokens and conventions: 4 breakpoints (P1), spacing and type scales (P2), motion tokens (P4). **No intended visual change except the approved D5 trims** (the floating blobs, photo parallax, hero photo zoom and tag bobbing were already removed in Session 3b, Checkpoint 5; what remains is to reduce glass to the list set in Session 4), shown as before and after screenshots.
- **Success:** screenshots before and after match; axe still 0; checkpoint.

### Sessions 6 to 9: Phase 3/4, section-by-section refinement (one session each)
- 6: header, navigation, hero (applies the chosen hero: **A, people-led**, with the tag system and the warm cream hero surface moved from `css/proto.css` into `css/site.css` and `tools/pages/index.html`; then delete `proto-hero-a.html`, `proto-hero-b.html`, `css/proto.css`, `js/proto.js`, `tools/build-prototypes.py` and the two avatar images). (Update, Session 3b: the warm cream hero surface is already in `css/site.css`; only the tag system and the chosen hero markup remain to move.)
- 7: problem, options, trust sections (vary the repeated card grids, P7).
- 8: September story, compare table, net sheet (copy and layout, not formulas).
- 9: About, New homes, FAQ, contact section, footer.
- **Success per session:** that section meets its design, content, usability and accessibility criteria; consistent with the approved system.

### Session 10: the homes gallery (Jeremy's idea, Oct 21)
- **Goal:** a gallery of Joey's homes from his Facebook page ("our work").
- **Needs first (blocking):** Joey's answers (which homes; status; address/price/interior photos allowed; photo ownership; originals; licensing and advertising rules, see `CONTENT_CLAIMS.md` question 8) and decision D6 on placement: (1) inside New homes, (2) its own "Our work" page, or (3) the future construction site.
- **Success:** accessible gallery (keyboard, alt text, honest captions like "Closed September 2026" or "Now building"), no invented stats, consent recorded.
- **Why not sooner:** we can't build it from the logged-out Facebook view (it exposes only the newest post), and it may belong on the construction site.

### Session 11: Phase 5, function and integration
- Validate the net sheet with test cases (known inputs and outputs, edge cases: zero, negative, blank).
- Fix the GHL form with Joey (its look can only be changed inside GoHighLevel: Form Builder, then Style). Form `links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ`, booking `.../widget/booking/cM59fR3vJlAVRy08Depz`; it appears on the home page and the Contact page.
  - **Consent text:** still contains `[BUSINESS NAME]` and `[USE_CASE_FROM_CAMPAIGN_DESCRIPTION]`, and its Privacy and Terms links point to example.com. Replace with GLP Home Options / GL Partners LLC wording that matches the registered text-message campaign, linking to `/privacy-policy` and `/terms-of-service`. Carriers usually also want message-frequency and HELP/STOP wording.
  - **Styling:** primary `#3c7a66`, font Plus Jakarta Sans, radius about 12px, button text "Get my options", labels above fields (Baymard), optional fields marked "(optional)", one column on phones.
  - **Fields:** keep to name, phone and property address; the rest optional.
  - **Behavior:** confirm the thank-you behavior and where leads go.
- Walk every journey end to end: call, text, email, book, form, Facebook.

### Session 12: Phase 6, accessibility, responsive, performance
- Lighthouse baseline and fixes; responsive images (`srcset`, WebP/AVIF) once originals exist (P6); font loading; 320px width (known wraps: the email link in the Contact and Our story tiles, the Home hero button; and the header, whose logo and Menu button need about 343px, so the Menu button is clipped by about 23px at 320px); keyboard-only and screen-reader walkthrough; 44px touch targets (P5); console errors; print. (**Fixed in Session 3b, Checkpoint 5:** the Menu button is icon-only at 350px and narrower; no sideways scroll or header overflow at 320, 340 or 360 on any page.)

### Session 13: Phase 7, launch QA and deployment
- Remove `noindex` (one line in `head()` of `tools/build-pages.py`); un-comment the canonical line there and set the real domain (`SITE`, which also drives og:url and og:image); `sitemap.xml`, `robots.txt`; analytics and form-conversion tracking (and confirm the Privacy page's "we respect Do Not Track" stays true once analytics is added); point glphomeoptions.com at the site (GitHub Pages custom domain + DNS, with Joey) keeping `/privacy-policy` and `/terms-of-service`; lawyer-reviewed Privacy and Terms (remove the "Draft for review" note in `tools/legal_text.py`); share-card check; final live verification of every page and link.

### After launch (backlog, not scheduled)
Situation pages (inherited home, divorce, relocation, needs repairs, financial stress, downsizing), each with unique copy from Joey's real experience; city pages (only towns Joey confirms; candidates to ask about: Hixson, Signal Mountain, Ooltewah, East Ridge, Red Bank, Soddy-Daisy, Collegedale); a real-reviews strip once real reviews exist; a market snapshot only with sourced numbers; a real SVG logo; video of Joey and Ethan; Google Business Profile; connect the construction site.

## Dependencies

| Task | Waits on |
|---|---|
| Launch with the J-tagged claims | Joey's confirmation of each (`CONTENT_CLAIMS.md`, rows 1, 2, 4, 5, 6, 41) and a lawyer's look at seller financing and lease options |
| Session 4 | Jeremy's decisions D1 to D6 and the Session 3 hero choice (made: A, people-led, warm cream hero) |
| Session 5 | Session 4 (we consolidate the approved system) |
| Session 10 gallery | Joey's photos and answers; D6 |
| Session 11 form fix | GoHighLevel access (Joey or Jeremy); registered text-message campaign wording |
| Session 13 launch | Lawyer review, real reviews (if any), domain control, Joey's sign-off on every claim |

## Risks

- Joey's answers arrive slowly: mitigated by the J tags in `CONTENT_CLAIMS.md` (we always know whose word a claim rests on) and by keeping the site `noindex` until he confirms.
- Source photos are ~800px and one may be AI-generated (the bridge photo): real originals are the biggest trust upgrade.
- The GHL form can't be exercised from our workspace: needs a human test on a phone after every change.
- The construction business may split off: `NEW_HOMES` in `tools/build-pages.py` is the one-line switch.
- Legal pages are plain-words drafts, not legal advice.
- Sessions end abruptly: the checkpoint rule exists to make that harmless.

# GLP Home Options: roadmap

**The plan for the whole project, session by session.** Authoritative for sequencing and acceptance criteria. Status lives in `PROJECT_STATUS.md`; the next session's exact task lives in `SESSION_HANDOFF.md`.

Rules this plan follows (from the master plan): sessions are **30 to 45 minutes**; one primary objective per session; every session ends at a verified checkpoint with updated documents; never start a new phase just because time is left; changes to creative direction, scope or major architecture need Jeremy's approval.

## Where we really are

The master plan assumes a clean start. This project did not start clean: earlier sessions (before the plan existed) already built a working draft with a design system, five content pages, a calculator and a deployment. So the phases below are marked with what **exists** versus what is **approved**. We do not redo built work; we review it, approve or adjust it, then refine it.

| Phase | What exists today | Status |
|---|---|---|
| 0 Audit and safe foundation | Audit done, project record created, checkpoint tool added | **Done in Session 1** |
| 1 Creative direction and visual design | A complete direction is *built* (light, navy and green from the logo, Plus Jakarta Sans + Fraunces italic accent, gable photo frame). One hero composition only. No formal approval. | **Partly approved Oct 21** (D1, D2, D4, D5); D3 proceeds by default; D6 was settled on Oct 21 (night): the gallery is its own "Our work" page; hero A (people-led) chosen with a warm cream hero surface (Session 3); the formal lock is Session 4 |
| 2 Design system and foundation | Tokens and components exist in `css/site.css` (73 media-query blocks at 30 different widths on Oct 22, up from 19 breakpoints at the start; no spacing scale, no motion tokens) | Built, needs consolidation (Session 5) |
| 3 Homepage structure | Eight pages built (Home, Your options, Our story, Our work, New homes, Contact, Privacy, Terms). Home (18,278 px on a phone) and Your options (12,157) are long. | Built, needs approval (D7) |
| 4 Section refinement | Sections exist; several need a review for repetition. The accuracy patch is done (Session 2) and a plain-words pass is done (Session 6g). A full review was written Oct 22 (`research/site-review-2026-10-22.md`). | Partly done |
| 5 Function and integration | The net sheet is tested to the dollar (`tools/netsheet-test.py`, extended at Checkpoint 36 to 150 random cases, the break-even proof and a real printed PDF); its break-even line and Print button are built (Checkpoint 36); a fairness pass is still proposed (D16 (a)). The GHL form can be seen in the built-in browser pane on Jeremy's computer (not from the cloud workspace). It **never loaded below the fold** until Checkpoint 35 (a lazy frame the embed script parks off-screen; see `PROJECT_STATUS.md`); an attorney has not reviewed its consent text (no placeholders remain). | Partly done |
| 6 Accessibility, responsive, performance | Accessibility is clean (axe: 0 violations; Lighthouse 100 on all 8 pages, Oct 22). Lighthouse on a local copy: performance 94 to 100, layout shift 0. No manual keyboard or screen-reader pass and no real-phone pass yet. | Partly done |
| 7 Final QA and deployment | Draft is live on GitHub Pages as `noindex` (the live site is Checkpoint 30; later checkpoints wait for Jeremy's commit). Not launch-ready. | Not started |

**Update, Oct 22, 3:08 PM (Checkpoint 37, notes only): the contact form area is the next big job.** Jeremy, 3:03 PM, on the live Contact page: "on desktop veiew still lots of white space and this whole form still sticks out .. this is one of the main thigns so has tob e incredible this whole area  just note that down". 3:08 PM: "this is the form from his existing site.. we will need to make a new one in the future lets leave this alone.. thatts fine its tacky im following now" and "ill talk to him on this one". So the current form stays as it is, and **a new contact form (D17)** comes first after he talks to Joey. Checkpoint 36 is live (committed at 2:58 PM, commit `0a2cad1`) and was checked on the live site. **3:17 PM: Jeremy asked for calculator defaults that make GLP "the easy win" (D18). Nothing changed; the plan is one real recent deal from Joey as the default, plus a guard for silly numbers.**

**Update, Oct 22, afternoon (Checkpoint 36): the last push before Jeremy leaves town.** Jeremy, 1:09 PM: he is out of town from today, so there is **one final deployment** and about three and a half hours to prepare it. Checkpoint 35 was live and he said it looked solid (1:08 PM), with "a little extra space on the form." He chose the job at about 11:24 AM ("Easy to call, hard to doubt"): the D14 polish bundle. Checkpoint 36 is D14 plus the form's extra space trimmed, a friendly 404 page, and net sheet round two (a break-even line and "Print my numbers"). **What the site is for (Joey's goal, relayed 1:10 PM):** get it onto Google, earn high ratings for soft leads, and hook it up to his CRM. The form already feeds Joey's GoHighLevel CRM; the Google Business Profile, the domain and indexing are the next phase and stay parked until Jeremy talks to Joey this weekend (1:12 PM). The site stays `noindex` meanwhile. **Whatever is wrong on the live site after this push cannot be fixed until Jeremy can commit again,** so Checkpoint 36 was held to changes that could be proven in the test browser, and the form trim is CSS-only and can be removed in one step (`research/ghl-form-style.md`, "FORM-TRIM").

**Update, Oct 22, 11:30 AM (Checkpoint 35): the contact form is the main call to action and it must work perfectly.** Jeremy, 11:28 and 11:29 AM: "this form never seems to load.. it needs to be flawless and not like a bolt on scammy thing" and "that is the main call to action button so its gotta work perfect." **Standing rule from here on: the form is never allowed to be a blank box, and it must look like part of the site.** The loading half is fixed in code at Checkpoint 35 (found: the frame was `loading="lazy"` and the form company's script parks it 10,000 px off-screen, so the browser never loaded it unless it was on the first screen); it still needs a look on the live site after his push. The look half needs someone with GoHighLevel access (`research/ghl-form-style.md`: the button still says "Button"). Longer term: a form built into our own page (see "Other options" in that file) is the way to remove the last third-party piece; that is a decision for Jeremy, Joey and a lawyer, because the text-message consent record lives in GoHighLevel.

**Update, Oct 22 (Checkpoint 34):** a full review and the "what works" research are written. They found that the biggest gap is facts only Joey has and proof that takes time, not design. See "Proposed plan v3" below (new decisions D12 to D16; nothing is approved).

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
- **Update (Oct 21, Session 6b):** Jeremy answered **yes to cream beyond the hero** and it is built (Checkpoint 8). He also asked for a more professional look, so the floating hero tags, the pulsing pill, the path chips, the button shine and the numbers count-up were removed. What remains for Session 4: the exact glass list (the hero tags are gone, so the caption no longer uses glass), and asking Jeremy what else looked gimmicky. Session 6c then sharpened and warmed the hero photo, slimmed the frame and simplified the header; the 800px photo is now the limit, so **ask Joey for the original or a new portrait** before the final launch pass.

### Session 5: Phase 2, design system consolidation
- **Goal:** tokens and conventions: 4 breakpoints (P1), spacing and type scales (P2), motion tokens (P4). **No intended visual change except the approved D5 trims** (the floating blobs, photo parallax, hero photo zoom and tag bobbing were already removed in Session 3b, Checkpoint 5; what remains is to reduce glass to the list set in Session 4), shown as before and after screenshots.
- **Success:** screenshots before and after match (use `tools/shots.py` and `tools/shots-diff.py`); axe still 0; `tools/claims-check.py` clear; checkpoint.

### Sessions 6 to 9: Phase 3/4, section-by-section refinement (one session each)
- 6: header, navigation, hero (applies the chosen hero: **A, people-led**, with the tag system and the warm cream hero surface moved from `css/proto.css` into `css/site.css` and `tools/pages/index.html`; then delete `proto-hero-a.html`, `proto-hero-b.html`, `css/proto.css`, `js/proto.js`, `tools/build-prototypes.py` and the two avatar images). (Update, Session 3b: the warm cream hero surface is already in `css/site.css`; only the tag system and the chosen hero markup remain to move.) (Update, Session 6a, Oct 21: hero A is applied to the live Home page, the header is refined and the prototypes are retired at Checkpoint 6; navigation wording and the other pages' headers remain.)
- 7: problem, options, trust sections (vary the repeated card grids, P7).
- 8: September story, compare table, net sheet (copy and layout, not formulas).
- 9: About, New homes, FAQ, contact section, footer.
- **Success per session:** that section meets its design, content, usability and accessibility criteria; consistent with the approved system.

### Session 10: the homes gallery (Jeremy's idea, Oct 21), built early in Session 6e
- **Built Oct 21 (night, Session 6e, Checkpoint 12):** Jeremy approved decision D6 at 8:40 PM: the gallery is **its own "Our work" page** (`work.html`), closings and builds together, with a new menu link; New homes keeps its small strip. It has three groups (Renovating, Building, Recently closed), a keyboard-friendly photo viewer, and a photo list in `tools/gallery_data.py`. A second Recently closed photo (a SOLD sign) was added at Checkpoint 14 on Jeremy's word; Joey has not confirmed it (`CONTENT_CLAIMS.md` row 47). The eight renovation photos came from Joey's personal Facebook via Jeremy; the building and closing photos are the ones already on the site plus two lot photos.
- **What this session still has to do (blocking launch):** Joey's answers (which homes are his; status; whether a city or neighborhood, prices or interiors may be shown; **who owns each photo**; originals; licensing and advertising rules, see `CONTENT_CLAIMS.md` question 8 and rows 42 to 46). Then add more photos with `tools/process-photos.py` and `tools/gallery_data.py`, swap in originals, and record consent. The six properties Jeremy named are in a private log outside the repo (never put street addresses in the repo; it is public).
- **Success:** accessible gallery (keyboard, alt text, honest captions like "Closed September 2026" or "Now building"), no invented stats, consent recorded.
- **A video:** Jeremy asked about a Facebook video of Joey's (Oct 21, night). Our tools cannot fetch Facebook, so it needs a saved file. An intro video is in decision D11 ("not now"); putting any video on the site is its own approval.

### Session 11: Phase 5, function and integration
- Validate the net sheet with test cases (known inputs and outputs, edge cases: zero, negative, blank).
- Fix the GHL form with Joey (its look can only be changed inside GoHighLevel: Form Builder, then Style). Form `links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ`, booking `.../widget/booking/cM59fR3vJlAVRy08Depz`; it appears on the home page and the Contact page.
  - **Its look (Jeremy, Oct 21, 11:09 PM: "a third-party bolt-on ... like an ad on top of the website"):** diagnosed, and a fix prepared and tested on a copy of the form page at Checkpoint 13: `research/ghl-form-style.md` (steps and what to check) and `research/ghl-form-custom.css` (paste-ready). It needs someone with GoHighLevel access, about 5 minutes, then a phone test and one test lead. The button still says "Button": change it in the form's settings (suggested "Send my details"). Not tested: the form inside our page, error messages, a phone width.
  - **Consent text (checked Oct 21, about 11:15 PM):** no placeholders are left; it names "GL Partners LLC DBA GLP Home Options". Its Privacy and Terms links point to `glphomeoptions.com/privacy-policy` and `/terms-of-service` (the old site; after launch those addresses must open our Privacy and Terms pages). The first checkbox repeats "Message frequency varies." (delete one). A lawyer should still read the wording; carriers usually also want message-frequency and HELP/STOP wording.
  - **Styling:** done by the prepared CSS: our green, Plus Jakarta Sans, 12px corners, labels above fields (Baymard), 54px fields at 16px text, one column.
  - **Fields:** the goal is name, phone and property address, the rest optional. Today phone and email are both required; ask Joey whether email must stay required.
  - **Behavior:** confirm the thank-you behavior and where leads go.
- Walk every journey end to end: call, text, email, book, form, Facebook.

### Session 12: Phase 6, accessibility, responsive, performance
- Lighthouse baseline and fixes; responsive images (`srcset`, WebP/AVIF) once originals exist (P6); font loading; 320px width (known wraps: the email link in the Contact and Our story tiles, the Home hero button; and the header, whose logo and Menu button need about 343px, so the Menu button is clipped by about 23px at 320px); keyboard-only and screen-reader walkthrough; 44px touch targets (P5); console errors; print. (**Fixed in Session 3b, Checkpoint 5:** the Menu button is icon-only at 350px and narrower; no sideways scroll or header overflow at 320, 340 or 360 on any page.)

### Session 13: Phase 7, launch QA and deployment
- Remove `noindex` (one line in `head()` of `tools/build-pages.py`); un-comment the canonical line there and set the real domain (`SITE`, which also drives og:url and og:image); `sitemap.xml`, `robots.txt`; analytics and form-conversion tracking (and confirm the Privacy page's "we respect Do Not Track" stays true once analytics is added); point glphomeoptions.com at the site (GitHub Pages custom domain + DNS, with Joey) keeping `/privacy-policy` and `/terms-of-service`; lawyer-reviewed Privacy and Terms (remove the "Draft for review" note in `tools/legal_text.py`); share-card check; final live verification of every page and link.

### After launch (backlog, not scheduled)
Situation pages (inherited home, divorce, relocation, needs repairs, financial stress, downsizing), each with unique copy from Joey's real experience; city pages (only towns Joey confirms; candidates to ask about: Hixson, Signal Mountain, Ooltewah, East Ridge, Red Bank, Soddy-Daisy, Collegedale); a real-reviews strip once real reviews exist; a market snapshot only with sourced numbers; a real SVG logo; video of Joey and Ethan; Google Business Profile; connect the construction site.

## The next 10 big things (PROPOSED by Claude for Jeremy on Oct 22 at about 8:30 AM; nothing here is approved or started until Jeremy says so)

Asked for by Jeremy at 8:20 AM. Grouped by what has to happen first. Nothing is invented: every number, review, license or result below waits for Joey. The search listing, launch plan, Google listing, domain and analytics work stays parked until Jeremy says the site is pristine (his 1:02 AM message); items 7 and 8 are that bundle, written down so it is ready.

**Before launch: make it pristine and make it convert**

1. **Real-phone pass and Joey's read-through (the gate for everything else).** Jeremy and Joey go through every page on real phones (iPhone and Android, with the text size turned up) and run the start-at-top test; Joey confirms every claim, photo and number in `CONTENT_CLAIMS.md` (rows 42 to 47 first), the license and brokerage details, the county list and the main phone number. Needs: Jeremy, Joey.
2. **Make the contact form ours and fast.** Restyle the GoHighLevel form to match the site (`research/ghl-form-style.md`; the consent wording stays exactly as it is), and set up what happens after a form is sent: a text and email alert to Joey and Ethan within a minute, a friendly automatic reply, and a "we will call you today" line only if Joey can keep it. Speed of reply wins these leads. Needs: GoHighLevel access, Joey.
3. **Real proof: reviews, stories and results.** Collect the first real reviews and permission to quote them (Google, Facebook, past sellers), turn two or three of Joey's real projects into short before-and-after stories on Our work, and add "The numbers" (D7) only with numbers Joey confirms. Needs: Joey. Never invented.
4. **Make the net sheet the star (Jeremy: "crucial").** Joey's real cost ranges, closing costs checked with a title company for the counties he serves, a "send me my numbers" button that texts or emails the result to the homeowner and to Joey, and a one-page printable version for the kitchen table. The math is tested to the dollar after every change, as now. Needs: Joey, a title company's numbers.
5. **Shorten Home (needs Jeremy's yes).** Home is long because of its structure, not its words: fold "How it works" into the option cards, move the photo band, shorten the FAQ (the proposals are in `SESSION_HANDOFF.md`). Goal: a worried homeowner reaches the options and the phone number in about half the scrolling.
6. **Joey and Ethan on video.** A 60-second "who we are and how this works" on Home and Our story, plus short clips of finished homes: real faces and voices are the strongest answer to the "we buy houses" noise. Captions, no sound on its own, light files. Needs: Joey, Ethan, a phone.

**Launch (parked until the site is pristine)**

7. **The launch bundle.** Google Business Profile, the site map (`research/site-map-proposal.md`), search titles and descriptions, business data for search engines, a sitemap file, the custom domain with redirects from Joey's old pages, and `noindex` removed only on launch day, with a one-page launch checklist and a way back. Needs: Jeremy's go and the domain decision.
8. **Know what works.** Simple privacy-friendly analytics, counts of call, text and form taps, tracking links for Facebook posts and mailers, and a one-page monthly report Joey can read in two minutes. Needs: item 7's domain.

**After launch**

9. **Local pages and plain answers.** One short page per place and situation Joey really serves (his cities and counties; inherited homes, behind on payments, a tenant in the house, repairs needed), each with the phone number, for the person searching in the middle of a bad week. Only places and situations Joey confirms.
10. **Keep it easy and sound.** A simple way for Joey or Ethan to add a "now building" card or a finished project without code (the photo tool exists), a monthly health check (links, speed, accessibility, and the big-text and bottom-bar tests), backups, a short "how to edit the site" guide and, if Joey wants that channel, a page for referral partners (realtors, attorneys, estate and probate professionals).

## Launch-blockers scorecard (written Oct 22, about 9:20 AM, Session 6g; a checklist, not new scope)

What stands between "pristine" and "ready to show the public", who can move it, and where the work is. The search, domain, Google listing and analytics work stays parked until Jeremy says the site is pristine, so it is not on this list. **Nothing on this list can be finished by Claude alone**; what Claude could do without anyone has been done (Checkpoints 13 to 32).

| # | Blocker | Why it blocks | Owner | Where the work is |
|---|---|---|---|---|
| 1 | Joey confirms the facts: photo origins, the closing-day story, "free first conversation", "call or text anytime", seller financing and lease options, counties, the main phone number | Every claim is "Joey's own words, not yet confirmed" until he says so | Joey (through Jeremy) | `research/questions-for-joey.md`, `CONTENT_CLAIMS.md` rows 42 to 47 |
| 2 | Is either founder a licensed Tennessee agent, and does GLP ever assign contracts? | Decides the advertising rules and whether the 2025 wholesaling law applies | Joey, then a Tennessee attorney or TREC | `research/compliance-questions-for-joey.md` sections 1 and 2 |
| 3 | Texting: is a campaign already registered, does the form's consent wording match it, and should the Terms and Privacy Policy gain HELP, frequency and "not a condition" lines | Unregistered or mismatched business texts get blocked; wording is the form's legal footing | Jeremy and Joey (GoHighLevel), an attorney for the words | `research/compliance-questions-for-joey.md` section 6 (the legal pages are not changed without Jeremy's decision) |
| 4 | Business name filed (GLP Home Options for GL Partners LLC), county and city licenses, contractor license for the new homes | The site and the registered texting brand use the name | Joey | `research/compliance-questions-for-joey.md` sections 4 and 5 |
| 5 | A real-phone pass: start-at-top, bottom bar, menu, net sheet, the photo viewer, with text enlarged, on an iPhone, an Android and, if one can be borrowed, an older iPhone or iPad | The cloud has only Chrome's engine; no real Safari has seen the site | Jeremy | `research/browser-support-audit.md` ("Next steps") |
| 6 | **The contact form, the main call to action:** (a) it loads every time (code fixed at Checkpoint 35; check it on the live site after the push, on a real phone too), (b) its look (the button says "Button"), (c) one real test lead end to end (arrives in GoHighLevel, alert to Joey and Ethan within a minute, a friendly reply, consent recorded) | Speed of reply wins these leads; a blank or unfinished-looking form loses them; it is the one thing on the site that is not ours yet | (a) Claude and Jeremy; (b) and (c) Jeremy or Joey (GoHighLevel access) | `research/ghl-form-style.md`, `research/lead-response-playbook.md`, `tools/form-test.py` |
| 7 | Real proof: first honest reviews, permission to use a seller's story or photo | The site shows no reviews rather than invent any | Joey | `research/joey-kit.md` |
| 8 | Jeremy's decisions: the clean-photo zip and the 16 raw photos in the public repo (`research/photos/incoming`), D7 to D11, the proposed shorter Home | Housekeeping and scope that only he can approve | Jeremy | `SESSION_HANDOFF.md` morning section |

## Proposed plan v3 (from the Oct 22 full review; PROPOSED, nothing here is approved until Jeremy says so)

**Why a v3.** Jeremy asked (Oct 22, 9:49 AM) for a full website review, a roadmap update and research on what works for this kind of site. The review (`research/site-review-2026-10-22.md`), the research (`research/what-works-2026-10-22.md`) and four independent reads (three research helpers, and one who read the site cold as four made-up first-time visitors) changed the picture in five ways:

1. **The biggest gap is not design.** Design, speed, accessibility and plain words are strong (Lighthouse on a local copy: Performance 94 to 100 and Accessibility 100 on every page). The gap is the facts only Joey has (how an offer is set, how GLP earns, what a seller pays, what happens after "yes," full names and bios, a service-area list) and the proof that takes time (reviews).
2. **Our honest net sheet is rare in what we read, so it is worth protecting** with Joey's real numbers: the example's 85% cash offer and the "no fees" and "we pay the closing costs" wording are his to confirm (`CONTENT_CLAIMS.md` rows 6 and 38). **It also leans a little toward a cash sale** (a 6% commission that is probably at the high end, the whole house payment counted as a cost of waiting, and $0 of waiting on the cash-sale side: roughly $2,000 to $3,000 of the example's $7,000 gap), so it needs a fairness pass before launch (review N27).
3. **Length is the second gap.** Home is 18,278 px tall on a phone (12,138 on a laptop); Your options is 12,157 (7,498).
4. **Small, safe conversion fixes exist** (one main button label, the phone number as plain text in the laptop header and under the phone hero buttons, a friendly 404 page, and the phone number no longer splitting across two lines on phones, which it does at 5 of the 6 widths tested), each needing Jeremy's yes.
5. **The site does not answer the situations its own chips promise.** "Inherited homes" is the first chip, but probate, heirs, signing from another state and belongings appear nowhere; "Financial stress" is a chip, but being behind on payments appears nowhere; tenants do not appear. And the "neutral guide" voice sits beside a buyer's offer, which a wary reader can see (review N22, N23).

**What stays the same.** Everything approved above stays in force, and nothing was removed from the plan. Search, the launch plan, the Google listing (except D15 below), the domain, analytics, situation and city pages, ads and mail stay **parked** until Jeremy says the site is pristine.

### New decisions for Jeremy (recommendation first; D7 to D11 are in plan v2 below)

| # | Decision | Recommend | Why |
|---|---|---|---|
| D12 | **Internal notes in a public repository.** Free GitHub Pages needs a public repository, and ours holds notes that name weak spots in our own claims and wording. | **Yes, before `noindex` comes off:** move the internal notes to a private repository or folder (or keep this repository private on a paid GitHub plan, which publishes Pages from private repositories). Until then the rules research and the raw research stay out through `.gitignore` (done at Checkpoints 33 and 34). | Anyone can read a public repository, and the site becomes easier to find at launch. |
| D13 | **Add the "trust pack" to the plan:** (a) how we set an offer and how we earn; (b) what happens after "yes," and the promises GLP keeps on every deal; (c) a "What to ask any buyer, including us" checklist; (d) full names, short bios, a real service-area list, independent checks (a HUD-approved counselor, your own attorney, an independent title company); (e) short plain answers, on the pages we already have, for the situations the Home chips promise: an inherited house or an owner in another state, an owner behind on payments, a rental with a tenant; and one line owning that GLP is a buyer too. | **Yes to the scope.** Each piece ships only with Joey's confirmed facts and, for promises, the contract summary and the situation answers, an attorney's glance. | These are the questions wary sellers ask and the site cannot yet answer (review N1 to N8, N22, N23). With no reviews yet, they are the strongest honest proof available. |
| D14 | **A small "conversion polish" bundle:** one main button label ("Get my options") wherever a button opens the form; the phone number as plain text in the laptop header and under the phone hero buttons, kept on one line; the Home "Common situations" chips either linked or plain text; a friendly 404 page; "Last reviewed" dates on Options and the net sheet; the two honesty lines on Options at body size; a person on the Options page; softer New homes wording; and the small polish in review N31 (button spacing, a hyphen break, the cropped photo, the empty form box). | **Yes** | Each is a few lines. Before-and-after screenshots and the full test set prove nothing else moved (N10, N11, N15, N17, N18, N25, N26, N29, N31). About one session. **BUILT at Checkpoint 36 (Oct 22, afternoon; Jeremy chose it at about 11:24 AM: "Easy to call, hard to doubt"). Nothing in it needs Joey. What exactly shipped, and what was left out, is in the Checkpoint 36 entry in `PROJECT_STATUS.md`.** |
| D15 | **Un-park only the Google Business Profile**, so honest reviews have a place to land and the clock starts before launch. The review requests follow the safe wording in `research/lead-response-playbook.md`. | **Yes** (the profile and the review requests only; the rest of the parked list stays parked) | Reviews take months to build, and 47% of people skip a business with fewer than 20 (BrightLocal 2026, a vendor). Google's rules do not accept a PO box as the business address, so the address choice (review N5) comes first. **ON HOLD (Jeremy, Oct 22, 1:12 PM): "we will have to hold off on Joey's Google profile stuff, I'll talk to him this weekend." Joey's goal (told by Jeremy at 1:10 PM): get the site onto Google, earn high ratings for soft leads, and hook it up to his CRM. The site is the destination for that traffic; the profile, the domain and indexing are the next phase and stay parked until Jeremy has talked to Joey.** |
| D16 | **Net sheet, round two.** (a) A fairness pass: count waiting the same way on both sides, relabel the monthly cost ("interest, taxes, insurance, utilities"), and use a commission Joey and a local agent agree on (review N27). (b) A break-even line ("In this example, a cash offer above about $262,000 beats listing") so a seller can test any offer. (c) A plainer name than "net sheet" ("What you'd keep"). (d) "Print my numbers": a printable layout, moved from D11's "not now" into the plan, before launch. | **Yes** | The sheet is the page's main trust tool, and a skeptical reader re-did the math by hand. Families decide on paper, and about 1 in 5 adults 65 and over has no smartphone (Pew, 2026). The math stays tested to the dollar (`tools/netsheet-test.py`). About one to two sessions. **(b) and (d) BUILT at Checkpoint 36:** the green answer box gains "On these numbers, a cash offer above $X keeps more in your pocket than listing" (X is price minus commission, closing costs, repairs and the cost of waiting; it does not depend on the offer or the mortgage; hidden when it means nothing), and a "Print my numbers" button prints one clean page (the typed numbers, the two sheets, the answer, how to reach us; nothing else from the page). No default numbers and no method changed. **(a) fairness and (c) the plainer name are NOT built:** (a) changes the numbers a seller sees and Joey should see it first; (c) is a naming decision. |
| D17 | **A new contact form.** The form on the Contact and Home pages is GoHighLevel's plain default and, Jeremy says, the same form that serves Joey's existing site. It looks like a bolt-on, and the site cannot restyle what is inside the frame. Jeremy, 3:03 PM: the form area is "one of the main thigns so has tob e incredible"; 3:08 PM: "we will need to make a new one in the future lets leave this alone." | **Decided Oct 22, 3:08 PM: leave the current form exactly as it is and build a new one after Jeremy talks to Joey.** Proposed route: **(A)** first, a copy of the form made for the new site in GoHighLevel, with the ready-made `research/ghl-form-custom.css` and the button text changed (about an hour with one real test lead); **(B)** later, only if Joey's GoHighLevel allows it and he wants it, a form built into our own page that sends the details in (best look, most work, needs a legal look at the consent record). | It is the main call to action. Editing the existing form in place would also change Joey's current site, which nobody has asked for. The details, the measurements and four questions for Joey are in `research/ghl-form-style.md`. |
| D18 | **The calculator's default example.** The net sheet opens on our own invented example (a $300,000 sale price, a $255,000 cash offer, 6% commission, 2.5% closing costs, $8,000 of repairs, 2.5 months of waiting), where listing nets $112,000, the offer $105,000, and the headline says "You'd keep about $7,000 more by listing." Jeremy, Oct 22, 3:17 PM: "i cannot stand right now is the default numbers for this calculator .. make them somthing that makes GLP Home make like the easy win". The sheet also has no guard: $2,000,000 in the offer box gives "You'd keep about $1,738,000 more by selling direct." | **Do not make up a flattering example. Make a true one:** one real recent deal from Joey with rounded numbers (ideally the September closing, if the sellers are comfortable), used as the default, plus a guard for silly numbers. Until then the current example stays (it was labeled "an example only, not a quote"). Nothing changed on Oct 22. | The defaults are claims about what Joey pays. A default that makes selling to GLP look better than a real offer would be sets the wrong expectation, and that is where 1-star reviews come from (the opposite of D15). The honest win is speed and certainty, which the green box already leads with. Question 24 in `research/questions-for-joey.md`; the places to change are listed in `PROJECT_STATUS.md`, Checkpoint 38. |

### Re-ordered plan (this sharpens "The next 10 big things" above; it does not replace them)

**Needs Joey (one call of 30 to 45 minutes, then Jeremy's yes)**

1. **The Round 2 questions plus the five already queued** (`research/questions-for-joey.md`, items 13 to 23 and the short text, which now has seven questions). They unlock the trust pack (D13) and the net sheet's real numbers (D16).
2. **Photo originals and the three confirmations** (review F1 to F3, F12): the single biggest upgrade, and the gate for launch (D9).
3. **The honest review path** (D15, `research/lead-response-playbook.md`).

**Needs Jeremy's yes; Claude can build it**

4. **The conversion polish bundle** (D14), then **the trust pack copy** as Joey's answers arrive (D13, review N1 to N8, N17, N22 to N24).
5. **Home and Options diet** (D7) and the heading trim (D8). Target: Home about 14,500 px on a phone and about 9,500 on a laptop.
6. **Net sheet, round two** (D16): fairness, break-even line, plainer name, print layout.
7. **Session 5:** one set of widths (30 today), proven by `tools/computed-diff.py`, plus an archive for old checkpoint notes (`PROJECT_STATUS.md` is 135 KB).

**Needs people and devices**

8. **The real-phone pass** (launch blocker 5) **and a reading test** with 3 to 5 people aged 60 and over who say each page's point back in their own words. No tool can do either.
9. **The contact form and a real test lead** (launch blocker 6; GoHighLevel access): require only name and phone, accept any phone format, set the alerts, state the reply time Joey can keep.
10. **The attorney:** the legal pages (including the "Do Not Track" sentence and the "Draft for review" note, review N16), the texting and consent wording, and any promises the site makes (launch blockers 2 to 4).

**Later (parked, unchanged, with the research now written down)**

11. **The launch bundle** (item 7 of "The next 10"). New from the research: Google wants one profile, a business name that matches the site, no PO box as the address (a service-area business can hide its address), and a service area within about two hours of the base. National ranking sites, not local buyers, fill most searches, so build for the visitor who has heard of GLP and is checking it is real (`research/private/C-local-visibility.md`).
12. **Analytics, local and situation pages, video, ads and mail.** Situation pages look under-served locally but need legal accuracy and Joey's real experience; no benchmark exists for a new site, so judge on about 90 days of our own numbers.

### Updated measures of success (these add to "Success measures" in plan v2)

- **Lighthouse baseline today (local copy, phone settings):** Performance 94 (Home), 97 to 100 (the rest); Accessibility 100 everywhere; Best practices 100 (96 where the form script cannot load here); SEO 63 only because of `noindex`. **Targets on the live site:** Performance 95 or more on every page, Accessibility 100, Best practices 95 or more, SEO 95 or more once `noindex` is off. Home's largest paint is 2.4 s against a 2.5 s limit, so Home must not get heavier, and it must be re-measured with the real form script.
- **Length:** Home about 14,500 px on a phone (18,278 today) and about 9,500 on a laptop (12,138 today); Your options about 10,500 on a phone (12,157).
- **Trust:** each of the six worries (a low offer, pressure, a contract that is hard to leave, hidden fees, who is really buying, "can I check you out") is answered in plain words on the site, and every "J" claim is confirmed by Joey. Zero unexplained "fair" or "no fees" wording at launch.
- **Reading:** 3 to 5 readers aged 60 and over can say each page's point and how to reach a person.
- **Phone number:** visible as plain text in the first screen (or the Menu) on a phone and in the laptop header; never split across two lines at 320 to 430 px wide (5 of 6 widths split it today).
- **Net sheet:** both sides counted the same way; defaults Joey and a local agent agree on; a break-even line; the example still computed to the dollar by `tools/netsheet-test.py`.
- **Situations:** an inherited house or an owner in another state, an owner behind on payments, and a rental with a tenant each get a short, true, attorney-glanced answer (or an honest "we don't handle this").
- **After launch (parked with analytics):** call taps, text taps, form sends and net-sheet starts counted separately; judge after about 90 days.

### Recommended order (30 to 40 minutes each; supplements the table in plan v2)

| Step | Objective | Waits on |
|---|---|---|
| 1 | Joey call (Round 2 and the queued five); Jeremy's answers to D7 to D18 | Jeremy, Joey |
| 1c | **The calculator's default example (D18):** one real recent deal from Joey (question 24) as the default, a guard for silly numbers, and every place the example is written updated in one pass | Joey's real deal, Jeremy's yes |
| 1b | **A new contact form (D17):** one that looks like the site on every screen and replaces the form from Joey's existing site; first the talk with Joey (who can sign in to GoHighLevel; a copy of the form for the new site; or a form built into our own page), then a design Jeremy and Joey approve, then one real test lead | Jeremy's talk with Joey, GoHighLevel access |
| 2 | Conversion polish bundle (D14), including the phone number on one line | D14. **Done at Checkpoint 36** |
| 3 | Trust pack, part 1: how we set an offer, what happens after "yes," the net-sheet example and "no fees" wording, "bring your own expert" additions, one line owning that GLP is a buyer too | D13, Joey's answers, an attorney's glance at the promises |
| 4 | Home and Options diet (D7), heading trim (D8) | D7, D8 |
| 5 | Trust pack, part 2: names and bios, address wording, service-area list, extra FAQ answers, the situation answers (inherited, behind on payments, rentals), the buyer checklist | Joey, an attorney's glance |
| 6 | Net sheet, round two (D16): fairness pass, break-even line, plainer name, print layout | D16, Joey (commission and closing-cost defaults). **Break-even line and print layout done at Checkpoint 36; the fairness pass and the plainer name wait for Joey** |
| 7 | Session 5 (widths) and the notes archive | Jeremy's go |
| 8 | Form, real-phone pass, reading test, attorney | GoHighLevel access, Jeremy, Joey, an attorney |
| 9 | Session 12 (Lighthouse on the live site, keyboard, screen reader) and Session 13 (launch) | Everything above, Joey's sign-off, the domain |

## Proposed plan v2 (PROPOSED on Oct 21, planning session; nothing here is approved until Jeremy says so)

The approved plan above stays in force. This section proposes what to add or reorder, based on `research/site-review-2026-10-21.md`. Jeremy can answer every decision in one message: "go with your recommendations", or "D7 no, the rest yes".

### Decisions for Jeremy (recommendation first)

| # | Decision | Recommend | Why |
|---|---|---|---|
| D7 | Give "The numbers" (compare table and net sheet) its own page; Home keeps a one-screen teaser. The "The numbers" menu item stays. | **Yes** | Home is about 13,000 px on a laptop and repeats the Options page. This alone brings it to about 11,200 px (laptop) and 16,600 px (phone); trimming the FAQ to the five most-asked and folding "how it works" into the options section (Session 7, same approval) brings it to about 9,500 and 14,500. A focused page is also easy to share in a text or on Facebook. About one session. |
| D8 | Use the green-italic second headline line only for the hero and three or four key moments; plain bold elsewhere. | **Yes** | 11 headlines on Home use it; a signature used everywhere stops being one. About 20 minutes. |
| D9 | Do not launch until every unconfirmed photo is confirmed by Joey or replaced. | **Yes** | The site presents the people photos as real moments (review F1 to F3). The site is already `noindex`. |
| D10 | Glass: keep three uses (header, phone bottom bar, contact cards on the dark section); make the About name plates and the Options "jump to" panel solid. | **Yes** | Those two are almost opaque, so the blur adds cost and no look. Today's code has 5 uses, not 7. This is Session 4's list. |
| D11 | Allow the scope additions in the review (save or print the numbers, a guided "which path fits", a real-reviews strip, situation pages, an intro video) as later sessions, each approved on its own. | **Not now** | Keep launch focused; revisit after Session 11. |

### Jeremy's direction, Oct 21, 11:09 to 11:11 PM (recorded at Checkpoint 13; applies to every session below)

- **Tone:** professional but not too corporate; follow the best guidelines but not cookie-cutter; authentic, not a sellout.
- **Audience:** ordinary homeowners, many short on money and time, many wary of "we buy houses" ads. Plain words, no pressure, no luxury gloss, short forms, phone first.
- **Contact form:** it must not look like a third-party bolt-on. The form's own look is Session 11's job (GoHighLevel access; the fix is ready). **Our side of the frame** is proposed for Session 9: a calmer card with no heavy shadow, Joey and Ethan's faces beside the form, a short "what happens next" line, and the phone number as the first choice. Proposed until built and seen.
- **Tonight's last push (Jeremy, 11:24 PM):** he chose options 1 (trim the Options page), 2 (a plain-talk pass for the audience) and 3 (the contact section on our side). Option 4 (the new "The numbers" page, D7) is parked: "we will come back to that, but keep this in mind." **11:30 PM: trim words first, then the plain-talk pass.** **11:33 PM: the net sheet must be simplified ("crucial").**
- **Status at Checkpoint 30 (about 8:30 AM, Oct 22):** the Options page is trimmed (7,450 px, was 8,829); the net sheet is simplified (three boxes up front, same math, tested); a SOLD-sign photo is on Our work (not confirmed by Joey); Home and About have had their repeated words cut (Home 1,382 down to 1,328 words, its fast-close, fix-and-clean and fees questions merged into one); **Checkpoint 22 trims New homes (372 down to 336 words) and Contact (326 down to 298)**. Checkpoints 13 to 30 are committed and live (his pushes at 8:02, 8:08 and 8:31 AM; Checkpoint 30 is the fix that stops the phone's bottom bar flashing while a page loads). Checkpoint 31 (notes), Checkpoint 32 (the older-phone fix, the rules research, Joey's kit and the launch-blockers scorecard, built while his computer was off) and Checkpoint 33 (notes: the rules research's last corrections) wait for his next commit. **Checkpoint 17 is the start-at-top fix:** a link from a text, or a reload, always opens at the top (the cause was a `#numbers` on the end of the link); a link from another page of the site still jumps to its section. **Checkpoint 19 is the first mobile batch** (44 px touch targets, a text-size floor on phones, a lighter hero photo) **Checkpoint 20 adds safety nets** (no page stays half blank if its script fails) **and a faster Contact page**, and **Checkpoint 21 adds a swipe in the photo viewer and more room in the bottom bar on the narrowest phones**; 19 to 29 are saved in his folder, not yet committed. **Checkpoint 23 is the first part of the plain-talk pass** (industry words and pitch phrases swapped for everyday ones on every page; the words changed, not the claims; "seller financing" and "lease option" explained in a few words on Home), and **Checkpoint 24 finishes it with the net sheet words** ("You'd keep about $7,000 more by listing", "Mortgage owed", "Cost of waiting"; the math is unchanged and tested), and **Checkpoint 25 is the contact section on our side** (Joey's and Ethan's faces at the top of the form card on Home and Contact, a softer card shadow; the form and the consent wording are untouched), and **Checkpoint 26 improves phones held sideways** (a slimmer header and a bigger photo viewer) and adds a tablet and landscape check; every page held up at every tablet and landscape size. **Checkpoint 27 is typography polish:** curly apostrophes everywhere (set automatically when the pages are built), no paragraph ending on one lonely word (on Chrome, Edge and Safari), and one repeated word fixed in a heading; the words and facts did not change. **Checkpoint 28 makes every page hold up when a reader makes the text bigger** (a phone's text size or a laptop browser's font size; new `tools/bigtext-test.py`) and fixes three slips found on the way: the footer's email ran into the next column at about 900 to 930 px, the net sheet's numbers crowded the edge of their cards at about 960 to 1070 px, and on short phones the open Menu's Call and Text hid behind the bottom bar. **Checkpoint 29 extends that to phones that enlarge the letters themselves** (the Menu button, the bottom bar, the footer and the cards; the new "letters" part of `tools/bigtext-test.py`, a simulation in Chromium) and fixes Home's "now building" card, which ran under the photos at about 920 to 1110 px wide. He went to bed at 12:36 AM and chose the folder way (no GitHub pushes). **Jeremy's top priority (11:54 PM): a long mobile pass, step 0 of the overnight plan; at 12:09 AM he added: do the mobile pass, the words and the contact section, and think about the whole site map as a UX designer and a marketer to get ready for a live business website.** Not started: the rest of the mobile pass (the other oversized thumbnails, the logo file) and the final proofreading pass (both are in the overnight plan in `SESSION_HANDOFF.md`). **Parked by Jeremy at 1:02 AM until the site is pristine:** SEO, the launch plan, the Google listing, the domain switch and analytics (`research/site-map-proposal.md` holds the research and the questions).

### Success measures (proposed launch targets)

- Lighthouse on the live site, phone: Performance 95 or more, Accessibility 100, Best practices 95 or more, SEO 95 or more (after `noindex` is removed). Core Web Vitals: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less (CLS is 0.000 locally today).
- axe: 0 violations on all 7 pages at 4 views; a keyboard-only and a screen-reader pass done; touch targets 44 px or more.
- After D7 and the Session 7 trims: Home about 9,500 px on a laptop and 14,500 px on a phone (13,050 and 20,295 today). Page weight 1 MB or less per page (Home is about 0.8 MB).
- Zero unconfirmed claims or photos at launch (every **J** claim confirmed by Joey).
- Tracked actions at launch: call tap, text tap, form submit, calculator start (Session 13).

### Recommended order (30 to 40 minutes each)

| Session | Objective | Waits on |
|---|---|---|
| 4 | Direction lock: label the design system; set the glass list (D10) and the headline rule (D8). No page changes. | D8, D10 |
| 5 | Consolidation: 4 breakpoints (22 at Checkpoint 11, 24 at Checkpoint 12; the starting inventory and a proposed mapping are in `research/css-inventory-2026-10-21.md`), spacing, type and motion tokens (motion today is 5 keyframes, all behind `no-preference`; proposed 160, 280 and 480 ms plus one easing curve), fix the column-balance spots (review F9), make the two glass uses solid. Before and after screenshots match except those. | Session 4 |
| 7 | Home diet: the new "The numbers" page (D7), a Home teaser, menu and links; trim the FAQ to the five most-asked and fold "how it works" into the options section; vary the repeated card grids (F6). | D7 |
| 8 | Options page: shorten it (9,039 px) without losing depth; Our story rhythm. | |
| 9 | New homes, Contact (including our side of the form's frame, see above), footer polish. | |
| 10 | Homes gallery: the Our work page is built (Session 6e); this session adds Joey's confirmations, originals and more photos. | Joey's photos and answers |
| 11 | Form (its look: the fix is ready), consent text, every journey end to end. | GoHighLevel access |
| 12 | Lighthouse, keyboard and screen-reader pass, 320 px, print. | |
| 13 | Launch QA and deployment. | Joey's confirmations, a lawyer, the domain |

**Joey track, in parallel:** Jeremy sends `research/questions-for-joey.md` (short text first). Photo originals are the biggest single upgrade and they gate D9.

## Dependencies

| Task | Waits on |
|---|---|
| Launch with the J-tagged claims | Joey's confirmation of each (`CONTENT_CLAIMS.md`, rows 1, 2, 4, 5, 6, 41) and a lawyer's look at seller financing and lease options |
| Session 4 | Jeremy's decisions D1 to D6 and the Session 3 hero choice (made: A, people-led, warm cream hero) |
| Session 5 | Session 4 (we consolidate the approved system) |
| Session 10 gallery (page built) | Joey's confirmation of the photos, who owns them, and what may be shown |
| Session 11 form fix | GoHighLevel access (Joey or Jeremy); registered text-message campaign wording |
| Session 13 launch | Lawyer review, real reviews (if any), domain control, Joey's sign-off on every claim |

## Risks

- Joey's answers arrive slowly: mitigated by the J tags in `CONTENT_CLAIMS.md` (we always know whose word a claim rests on) and by keeping the site `noindex` until he confirms.
- Source photos are ~800px and the origins of two (the bridge hero and the kitchen table) are unconfirmed: real originals are the biggest trust upgrade (review findings F1 to F3).
- The GHL form can't be exercised from our workspace: needs a human test on a phone after every change.
- The construction business may split off: `NEW_HOMES` in `tools/build-pages.py` is the one-line switch.
- Legal pages are plain-words drafts, not legal advice.
- Sessions end abruptly: the checkpoint rule exists to make that harmless.

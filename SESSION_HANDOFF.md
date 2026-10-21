# Session handoff

**Written:** Oct 21, 2026, at the end of Session 2 (accuracy patch), Checkpoint 2.
**Replace this file at the end of every session.** It always describes exactly one next session. The long-term plan is in `ROADMAP.md`; the full state is in `PROJECT_STATUS.md`.

## Where the project is

- **Session 2 is done.** The six unverified claims were replaced with Joey's own wording or pulled (`CONTENT_CLAIMS.md` shows each one, before and after). **No visual change.** `python tools/checkpoint.py` is clean at Checkpoint 2: a fresh build reproduces all 7 pages, 340 links resolve, axe is all clear at 4 viewports.
- **Is Checkpoint 2 live yet?** It goes live when Jeremy commits and syncs. Check by fetching the Home page: if the footer says "Serving Chattanooga, TN", it is live (the old text said "Serving Chattanooga and the surrounding counties"). Update the "Deployed state" line in `PROJECT_STATUS.md` either way.
- **Jeremy approved on Oct 21:** D1 (navy leads, green is the accent; hex values locked), D4 (build both hero prototypes and he picks), D5 (a restrained set of glass and motion, as a direction), and "Joey's own words now" for claims. D2 (one warm surface, tested only in the prototypes), D3 (keep the fonts) and D6 (keep the five pages) proceed by default.
- **Waiting on Joey** (list in `PROJECT_STATUS.md`, open question 1): seller financing and lease options, counties and towns, free consultation, hours and texts, a registered trade name, the example offer. None of these blocks Session 3.

## Next session: Session 3, hero prototypes (30 to 45 minutes)

**One objective:** build **two isolated hero prototypes** so Jeremy can compare and pick (D4), and test **one warm surface** (D2). **The live hero does not change.** Applying the chosen hero to the real Home page is Session 6.

### Needed from Jeremy (ask in the first message)

1. **Did you commit and sync Checkpoint 2?** (If not, do that first; message below.)
2. **Anything Joey has answered** since Oct 21. If not, nothing is needed to start.
3. At the end: **pick A or B**, and **cool or warm** (use AskUserQuestion, with the screenshots sent first).

### Start protocol (5 minutes, in this order)

1. Read `PROJECT_STATUS.md`, this file, `ROADMAP.md` (Session 3) and `DESIGN_SYSTEM.md` (color, motion, glass, and the P3 note).
2. Get the project from Jeremy's folder, not from memory: `C:\Users\jsgli\Documents\GLP-Home-Options` (list it, then stage the files into a working folder; about 70 files, at most 50 per staging call, so two calls; stage everything, including `images/`, `fonts/` and `research/photos/`, or the link check and checkpoint report missing files).
3. Run `python tools/checkpoint.py`. **Expected: clean.** If it reports differences, stop and find out why before editing (the folder was edited elsewhere, or a sync is pending), and tell Jeremy.
4. Read the newest line of `.git/logs/HEAD` in his folder, and fetch the live Home page (see "Is Checkpoint 2 live yet?" above).

### The two prototypes

| | **A: people-led** | **B: numbers-led** |
|---|---|---|
| Idea | Joey and Ethan are the first trust signal | The honest numbers are the first trust signal |
| Composition | The hero as built: copy left, gable photo right, three small floating facts (call, 7-14 days, $0 commission) | Headline, one line of lede and the one action on the left. On the right, a compact side-by-side of the paths (sell direct, list with an agent, keep it). A small photo of Joey and Ethan beside the headline or under it. |
| Numbers allowed | None new | Only Joey's, from `CONTENT_CLAIMS.md` rows 14, 15, 20, 21: 7-14 days, $0 commission and we pay closing costs, 45-90+ days, about 6% commission, "usually nets the most", keep the home. **No net-sheet figures in the hero** (those are our examples). |
| Photo | `images/joey-ethan-bridge.jpg`, as live. Its provenance is unconfirmed (open question 3). If it comes out, test `images/joey.jpg` and `images/ethan.jpg` (the Our story headshots). | Same files, smaller |

**Rules for both**

- **Same words and facts as the live hero** wherever possible (H1 "Real home options. Clear next steps."; button "Request a consultation"; the phone number; "No obligation, no spam. Your information is kept confidential."). Any new wording must come from rows marked **V** in `CONTENT_CLAIMS.md`, or be a plain label that makes no claim. Never invent a review, license, award, number or photo. Use only the photos already in `images/`.
- **Same tokens:** navy `#2d4855` leads, green `#3c7a66` is the accent; same fonts; one primary action per hero.
- **D5 trims already applied inside the prototypes:** no floating blobs and no photo parallax. Keep the ridge and contour touches, header glass and small overlays on photos. Respect `prefers-reduced-motion`.
- **D2, the warm surface:** add **one** warm neutral (sand or cream) as a single, clearly named token in the prototype stylesheet, with a small "cool / warm" toggle on the prototype pages, so each hero can be seen both ways. Pick the value, record it in `DESIGN_SYSTEM.md` as a PROPOSAL, and check that every text color on it keeps 4.5:1 (3:1 for large text).
- **Light first view:** no new image heavier than the existing hero photo. Report each prototype's first-view weight next to the live Home hero (the whole Home first view is 298 KB desktop, 196 KB phone).
- Both must work at **1440, 820, 390 (touch)** and be checked at **320**, and with reduced motion.

**Recommended technique** (it keeps the live pages and the real CSS and JavaScript untouched):

- Create `tools/build-prototypes.py`. It reads the generated `index.html`, replaces only the `<section class="hero">...</section>` block with the prototype's markup, adds `<link rel="stylesheet" href="css/proto.css">` after `css/site.css`, marks the title "PROTOTYPE", adds the cool/warm toggle, and writes `proto-hero-a.html` and `proto-hero-b.html` **at the site root**. The existing header, footer and icons then stay identical.
- Put prototype-only styles in a new `css/proto.css`. **Do not edit `css/site.css`, `js/site.js`, `tools/build-pages.py` or `tools/pages/*.html`.**
- Use the root, not a subfolder, and **do not use a `<base>` tag**: the page's inline icon sprite is referenced as `<use href="#i-...">`, which a `<base>` tag can break in some browsers.
- The checkpoint tool already tracks root `*.html`, `css/*.css` and `tools/*.py`; `tools/check-links.py` already checks every root `*.html`, so the prototypes are covered. The rebuild check only compares the 7 real pages, so the prototypes do not disturb it. The prototypes stay `noindex` like the rest of the draft; delete them after the chosen hero is applied (Session 6).

### Do not change

The live hero and every other part of the real pages; `css/site.css`; `js/site.js`; `tools/build-pages.py`; the phone, email, Facebook URL, form id and booking id; the net sheet; the `noindex` tag; the Facebook placements; page structure and URLs; the claims (the wording from Session 2 stays).

### Done means

- Both prototypes load with no console errors and no broken images; `python tools/check-links.py` passes.
- `python /path/to/tools/a11y-check.py proto-hero-a.html proto-hero-b.html` (run from the folder that has `node_modules`) shows **0 violations at all 4 viewports**, in the cool state and the warm state.
- Screenshots of **A and B, cool and warm, at 1440 and 390** (8 images) are looked at, and any wrap or layout problem is fixed. Send Jeremy the key ones.
- Jeremy has picked A or B and cool or warm. Record it: `PROJECT_STATUS.md` section C (D4 and D2 as APPROVED with the date), `DESIGN_SYSTEM.md` (the hero decision; P3 resolved), `ROADMAP.md` (Session 3 done; Session 6 applies the chosen hero). **If Jeremy is not there to pick,** leave both prototypes in place and record "pick pending": Session 4 can lock everything else but not the hero.
- `PROJECT_STATUS.md` updated (session log, section G, E6 results, "Last updated"); this file replaced with the Session 4 handoff; `python tools/checkpoint.py --write "Session 3: hero prototypes"` run last.

### End-of-session protocol (every session)

1. Verify (above). 2. Update the docs. 3. Write the checkpoint. 4. In **one** step stage every changed file (new and changed pages, sources, docs, `CHECKPOINT.json`) into the outputs folder; in a **separate, later** step copy them to Jeremy's folder; list the folder to confirm sizes. 5. Give Jeremy the commit message. He stages (+), commits and syncs in VS Code Source Control. 6. Fetch the live site after he syncs, if he says he has.

## Commands

```
python tools/checkpoint.py                      # start of session: does the code match the last checkpoint?
python tools/build-pages.py                     # rebuild the 7 pages from tools/pages/*.html and the builder
python tools/build-prototypes.py                # (created in Session 3) rebuild the two hero prototypes from index.html
python tools/check-links.py                     # every link, anchor, image and script on every root page
python tools/a11y-check.py [page.html ...]      # accessibility scan (needs Playwright and axe-core); no names = the 7 real pages
python tools/checkpoint.py --write "label"      # end of session, after everything passes
python -m http.server 8000                      # preview at http://localhost:8000
```

## Suggested commit message for Checkpoint 2 (Jeremy)

```
Session 2: accuracy patch and decisions recorded

Replace six unverified claims with Joey's own wording or remove them: seller financing and lease options, surrounding counties, "doing business as", "free" and "no obligation, ever", "anytime", and the example-offer label. Record decisions D1, D4, D5 and the claims approach. No visual change.
```

## If something looks wrong

- **The "Git" lines of the checkpoint tool look stale in the cloud workspace** (an old commit, many "changed" files): that copy has its own old `.git`. Ignore it there; the real history is `.git/logs/HEAD` in Jeremy's folder.
- **Checkpoint reports "CHANGED":** a tracked file differs from the last checkpoint. Look at which. If Jeremy edited it on purpose, accept it and record it in the session log. If not, find out before building on it.
- **Checkpoint reports the sprite or an image:** saving through the bridge adds an invisible provenance tag to images and to `tools/pages/_sprite.html`. The tool and the builder already ignore it.
- **The Contact page's FAQ is chosen by exact question text** (`FAQ["contact"]` in `tools/build-pages.py`): "Do I have to sell to you if I reach out?", "How do I know GLP is legit?" and "What areas do you serve?". If a later session rewords one of those three questions, it silently drops off the Contact page. Change the filter at the same time.
- **The GoHighLevel form looks wrong live:** it cannot be tested from the workspace. Record what Jeremy sees and defer to Session 11.
- **Facebook shows only one post:** expected when logged out. Never sign in; ask Joey for photos instead.

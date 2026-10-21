# Session handoff

**Written:** Oct 21, 2026, at the end of Session 6a (the landing page's top half), Checkpoint 7.
**Replace this file at the end of every session.** It always describes exactly one next session. The long-term plan is in `ROADMAP.md`; the full state is in `PROJECT_STATUS.md`.

## Where the project is

- **Session 3 is done.** Two hero prototypes were built and checked (A people-led, B numbers-led). Jeremy chose **A, people-led** and the **warm cream surface behind the hero only** (about 10:20 AM, Oct 21). His note on A, that the floating tags looked random, produced a five-rule tag system (`DESIGN_SYSTEM.md`, "Hero tag system"); it also fixed two phone defects in the live hero.
- **Live site = commit `73b0b53`** (Checkpoints 2 and 3). **Checkpoint 4 goes live with Jeremy's next commit.** It is additive: `proto-hero-a.html`, `proto-hero-b.html`, `css/proto.css`, `js/proto.js`, `tools/build-prototypes.py`, two avatar images and the docs. No real page changed. After he syncs, the prototypes are at `https://jsglisson3.github.io/GLP-Home-Options/proto-hero-a.html` and `proto-hero-b.html` (add `?surface=warm` for the warm state), so he can show Joey. Check with a cache-busting query (`?cb=...`); the fetch tool caches 15 minutes.
- **Session 3b polish (Checkpoint 5) changed real pages:** the Home hero is now warm cream; the floating blobs, photo drift, hero photo zoom and tag bobbing are gone; the 320px header is fixed (icon-only Menu at 350px and narrower). Checkpoints 4 and 5 go live together with Jeremy's next commit if 4 is not yet pushed. The hero A/B choice is still NOT applied to the live Home page (Joey is picking; Session 6).
- **Jeremy said he really likes the cream ("classy").** D2 approved it for the hero only; in Session 4 ask whether to try it on one or two more sections.
- **Session 6a (Checkpoints 6 and 7):** Joey chose hero A (people-led). It is live on the Home page (in the next commit) with a refined header; on phones a Joey & Ethan chip puts their faces in the first screen. Hero B is retired: `proto-hero-a.html` and `proto-hero-b.html` are redirect pages. **Jeremy can delete these in VS Code whenever convenient:** `proto-hero-a.html`, `proto-hero-b.html`, `css/proto.css`, `js/proto.js`, `tools/build-prototypes.py` (nothing uses them).
- **Approved by Jeremy:** D1 (navy leads, green accent), D2 (warm cream, hero only), D4 (hero A), D5 (restrained glass and motion, as a direction), and "Joey's own words now" for claims. D3 and D6 proceed by default.
- **Waiting on Joey:** his confirmation of every claim tagged **J** (seller financing and lease options, the service area, free consultation, "anytime", texting, the example offer); a lawyer's look at how seller financing and lease options are described; where the bridge photo came from (open question 3).
- **Fixed in Session 3b:** the 320px header overflow (icon-only Menu at 350px and narrower; no overflow at 320, 340 or 360 on any page). The 320px hero button wrap is still to be re-checked in Session 12.

## Next session: Session 4, direction lock (30 to 45 minutes)

**Objective:** turn the approved decisions into the formal design system, and set the exact list of the 7 glass uses (D5). **No change to any real page.**

### Needed from Jeremy (ask in the first message, at most two questions)

1. Should any other section use the warm cream, or stay cool (D2 was approved for the hero only)?
2. Approve the glass list you propose (below). Send a short list, not a document.

### Start protocol (5 minutes)

1. Read `PROJECT_STATUS.md`, this file, `ROADMAP.md` (Sessions 4 and 5) and `DESIGN_SYSTEM.md`.
2. Get the project from Jeremy's folder, not from memory: `C:\Users\jsgli\Documents\GLP-Home-Options` (stage everything, including `images/`, `fonts/` and `research/photos/`; at most 50 files per staging call). Run `python tools/checkpoint.py`. **Expected: clean at Checkpoint 4.** If it is not, stop and find out why.
3. Read the newest line of `.git/logs/HEAD` in his folder; if he has pushed, fetch the live Home page with a cache-busting query.

### What to do

1. **Inventory the glass:** `grep -n "backdrop-filter" css/site.css`. List every use with what it sits on. Propose the 7 to keep (the header glass is one; the hero tags and the caption count) and which to drop. Remember D5: header glass, small overlays on photos, and the ridge and contour touches stay; floating blobs and photo parallax go (Session 5 removes them).
2. **Label `DESIGN_SYSTEM.md`:** every token and rule is DIRECTED, APPROVED or PROPOSED. Items already approved: color hierarchy and hex values (D1), the hero (A), the warm cream hero surface (P3), the hero tag system, D5 as a direction. Leave P1, P2, P4, P5, P6 as proposals for Session 5 unless Jeremy decides now.
3. **Check the docs agree** with each other (decisions, dates, next session).

### Do not change

Every real page, `css/site.css`, `js/site.js`, `tools/build-pages.py`, `tools/pages/*`; the claims; the phone, email, Facebook URL, form id and booking id; the `noindex` tag. Leave the prototypes alone until Session 6 deletes them.

### Done means

- `DESIGN_SYSTEM.md` has no unlabeled token or rule; the glass list is written down and Jeremy has approved it (or "pending" is recorded).
- `PROJECT_STATUS.md` (session log, section G, "Last updated") and `ROADMAP.md` updated; this file replaced with the Session 5 handoff; `python tools/checkpoint.py --write "Session 4: direction lock"` run last.

### End-of-session protocol (every session)

1. Verify. 2. Update the docs. 3. Write the checkpoint. 4. In **one** step stage every changed file into the outputs folder; in a **separate, later** step copy them to Jeremy's folder; read them back and compare hashes (images gain an invisible provenance tag when saved, so compare their pixels). 5. Give Jeremy the commit message. He stages (+), commits and syncs in VS Code Source Control. 6. Fetch the live site after he syncs, if he says he has.

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

## Suggested commit message for Checkpoint 4 (Jeremy)

```
Session 3: hero prototypes (A, people-led, chosen) and project record

Add two isolated hero prototypes, proto-hero-a.html and proto-hero-b.html, with a cool/warm surface toggle, built from the live Home page by tools/build-prototypes.py. Jeremy chose A with a warm cream hero surface. Record the decisions, the five-rule tag system and the findings. No real page changed.
```

## If something looks wrong

- **The "Git" lines of the checkpoint tool look stale in the cloud workspace** (an old commit, many "changed" files): that copy has its own old `.git`. Ignore it there; the real history is `.git/logs/HEAD` in Jeremy's folder.
- **Checkpoint reports "CHANGED":** a tracked file differs from the last checkpoint. Look at which. If Jeremy edited it on purpose, accept it and record it in the session log. If not, find out before building on it.
- **Checkpoint reports the sprite or an image:** saving through the bridge adds an invisible provenance tag to images and to `tools/pages/_sprite.html`. The tool and the builder already ignore it.
- **The Contact page's FAQ is chosen by exact question text** (`FAQ["contact"]` in `tools/build-pages.py`): "Do I have to sell to you if I reach out?", "How do I know GLP is legit?" and "What areas do you serve?". If a later session rewords one of those three questions, it silently drops off the Contact page. Change the filter at the same time.
- **The GoHighLevel form looks wrong live:** it cannot be tested from the workspace. Record what Jeremy sees and defer to Session 11.
- **Facebook shows only one post:** expected when logged out. Never sign in; ask Joey for photos instead.
- **The prototypes look stale or wrong after a Home change:** re-run `python tools/build-prototypes.py` (it reads the built `index.html`, and stops with a message if the live comparison-table wording changed). They are deleted in Session 6.

## Suggested commit message for Checkpoint 5 (Session 3b)

Subject: Polish: warm cream home hero, calmer motion, 320px header fix

Body:
- Warm cream behind the Home hero (page heroes stay cool)
- Remove floating blobs, photo drift, hero photo zoom and tag bobbing
- Menu button is icon-only at 350px and narrower, so the header fits at 320px
- Breadcrumb links are 44px on touch screens; the email link fits on one line at 320px
- Hero prototypes A and B (not linked from the site) and the project notes updated

## Suggested commit message for Checkpoints 6 and 7 (Session 6a)

Subject: Landing page: hero A (people-led) live, seamless header, phone faces

Body:
- Joey picked hero A: it is now the live Home hero (retire the numbers version)
- Header keeps one height (no jump when you scroll) and blends into the cream hero
- Phones: a Joey & Ethan chip with portraits in the first screen
- Balanced headline and intro line breaks
- Tags and caption no longer overlap on 981 to 1100px wide screens
- Old prototype pages now redirect to the home page; project notes updated

# Session handoff

**Written:** Oct 21, 2026, about 11 PM CT, at the end of Session 6e, Checkpoint 12.
**Replace this file at the end of every session.** It describes exactly one next session and what is true right now. The long-term plan is in `ROADMAP.md`; the full state is in `PROJECT_STATUS.md`.

## Where the project is

- **Live site = Jeremy's commit "fixes" (9:08 PM CT)** at https://jsglisson3.github.io/GLP-Home-Options/ (`noindex`). A live fetch at about 10:55 PM showed the plain-talk pass (no quiz, no numbers strip) and a header **without** "Our work". **Checkpoint 12 is saved in his folder and waits for him to commit and sync:** the new Our work page, the simpler header, the menu-highlight fix and the start-at-top fix. After he syncs, fetch the live Home page and `work.html` with a cache-busting query to confirm.
- **Approved by Jeremy:** D1 (navy leads, green accent); D2 (warm cream, the whole site's one tint); D4 (hero A, people-led, in the gable frame); D5 (restrained glass and motion, as a direction; the exact list is Session 4); D6 (the gallery is its own "Our work" page, approved Oct 21, 8:40 PM); "Joey's own words now" for claims. D3 proceeds by default.
- **What Session 6e did (Checkpoint 12):** a plainer, more human site (Jeremy: "authentic, like real people are behind it, not a corporate sellout"): the "What matters most?" quiz and the Home numbers strip are gone, "Joey or Ethan" replaces "our team"; the **Our work** page with 16 photos (Renovating 8, Building 7, Recently closed 1) and a keyboard-friendly viewer; the header lost its phone number (six links did not fit) and the full header starts at 1241px; pages open at the very top on phones; the Home menu highlight clears at the top. Tools: `tools/process-photos.py`, `tools/gallery_data.py`, `js/gallery.js`; `.gitignore` for the photo inbox. All checks passed (E6, "Session 6e checks").
- **The photos on Our work rest on Jeremy's word.** The eight renovation photos came from Joey's personal Facebook via Jeremy; Joey has not confirmed they are his projects, that he wants them shown, or who took them (`CONTENT_CLAIMS.md` rows 42 to 46). The site is `noindex` meanwhile.
- **No street address is in any repo file, on purpose.** The six properties Jeremy named are in a private log **outside the repo**: `C:\Users\jsgli\Documents\GLP-private\flips-log.md` (with his words, links, the questions for Joey, the photo rules, and notes on two videos). Read it at the start of a session that touches the gallery; keep adding to it.
- **Videos (Oct 21, about 10:55 PM):** Jeremy saved two screen recordings of Joey's Facebook videos into `research/photos/incoming/` (`Home walkthrough 1.mp4`, `Home walkthrough 2 .mp4`). They are about 470 px wide, have Facebook's buttons on top, and the first has an address in its text and a John Denver song. **Not used on the site.** Best path: ask Joey for the original files. A video on the site is a scope decision (D11 lists an intro video as "not now"). `Facebook.mhtml` in the same folder was not opened and should be deleted by Jeremy.
- **`research/photos/incoming/` is the photo and video inbox.** New files there are ignored by git (`.gitignore`) and by the checkpoint tool. The 16 photos that were dropped there earlier tonight were **already committed**, so they are public (the repo is public); that cannot be undone from here.
- **Biggest risks:** the origins of two people photos on the live pages (the bridge hero and the kitchen table; review F1 to F3); the riverfront banner is soft; the closing photo shows third parties and a title company's branding; the GoHighLevel consent text still has placeholders.
- **Waiting on Jeremy:** commit and sync Checkpoint 12; try the start-at-top fix on his phone (open a page, scroll, reload, and open it from a bookmark and from a link in a message; tell me if any still starts in the middle, and how he got there); answers to D7 to D11 (`ROADMAP.md`, "Proposed plan v2"); what else at the top of the page looked gimmicky; sending the Joey text (`research/questions-for-joey.md`); whether to delete `Facebook.mhtml`.
- **Waiting on Joey:** the photo confirmations (rows 42 to 46), photo and video originals, every claim tagged **J**, license or brokerage (his videos say "New Listing coming soon"), the county list, the main phone number, reviews, GoHighLevel access, the domain. A lawyer should look at how seller financing and lease options are described.

## Next session: Session 4, direction lock (30 to 45 minutes)

**Objective:** turn the approved decisions into the formal design system and set the exact glass list. **No change to any real page.**

### Needed from Jeremy (first message, short)

1. That Checkpoint 12 is committed and synced, and whether the start-at-top fix works on his phone.
2. His answers to **D7 to D11** in `ROADMAP.md` ("go with your recommendations" is a valid answer). D8 (headline rule) and D10 (glass list) feed this session directly.
3. What else at the top of the page looked gimmicky, if anything. One question.

### Start protocol (5 minutes)

1. Read `PROJECT_STATUS.md`, this file, `ROADMAP.md` (Sessions 4 and 5 and "Proposed plan v2") and `DESIGN_SYSTEM.md`.
2. Get the project from Jeremy's folder, not from memory: `C:\Users\jsgli\Documents\GLP-Home-Options` (stage everything except `research/photos/incoming/`, which can hold big videos; include `images/`, `fonts/` and the rest of `research/photos/`; at most 50 files per staging call). Run `python3 tools/checkpoint.py`. **Expected: clean at Checkpoint 12** (ignore the workspace's stale "Git" lines). If not, stop and find out why.
3. Read the newest line of `.git/logs/HEAD` in his folder (stage it, then read it); if he has pushed, fetch the live Home page, Our work page or stylesheet with a cache-busting query.

### What to do

1. **Inventory the glass** with `grep -n "backdrop-filter" css/site.css`. Recommendation (D10): keep `.hdr`, `.mobile-bar` and `.reach-item`; make `.founder figcaption` and `.jump` solid. Record the final list; the CSS change itself is Session 5.
2. **Label `DESIGN_SYSTEM.md`:** every token and rule is DIRECTED, APPROVED or PROPOSED. Already approved: color hierarchy and hex values (D1), the cream tint (D2), hero A (D4), D5 as a direction, the Our work page (D6). Leave P1, P2, P4, P5, P6 as proposals for Session 5 unless Jeremy decides now. Record the headline rule (D8) once he answers.
3. **Check the docs agree** with each other and with the code (decisions, dates, next session).

### Do not change

Every real page, `css/site.css`, `js/site.js`, `js/gallery.js`, `tools/build-pages.py`, `tools/pages/*`; the claims; the phone, email, Facebook URL, form id and booking id; the `noindex` tag.

### Done means

- `DESIGN_SYSTEM.md` has no unlabeled token or rule; the glass list is written down and Jeremy has approved it (or "pending" is recorded).
- `PROJECT_STATUS.md` (session log, section G, "Last updated") and `ROADMAP.md` updated; this file replaced with the Session 5 handoff; `python3 tools/checkpoint.py --write "Session 4: direction lock"` run last.

### End-of-session protocol (every session)

1. Verify (rebuild, `check-links.py`, `claims-check.py`, accessibility scan; for Session 5, `shots.py` before and after). 2. Update the docs. 3. Write the checkpoint (`--write` raises the number every time it runs). 4. In **one** step stage every changed file into the outputs folder (use `|| exit 1` after each copy: lines after a failed heredoc still run); in a **separate, later** step commit them to Jeremy's folder (a new folder may need creating first; test with one file); read them back and compare hashes (images gain an invisible tag when saved, so compare their pixels; if a read-back is stale, commit again with `force`). 5. Give Jeremy the commit message (no attribution lines). He stages (+), commits and syncs in VS Code Source Control; the AI cannot commit or push. 6. Fetch the live site after he syncs, if he says he has.

## Commands

```
python3 tools/checkpoint.py                     # start of session: does the code match the last checkpoint?
python3 tools/build-pages.py                    # rebuild the 8 pages from tools/pages/*.html and the builder
python3 tools/check-links.py                    # every link, anchor, image, script and linked file on every root page
python3 tools/claims-check.py                   # the "never invent" rule: no credentials, ratings, awards, results or founding years unless allowlisted
python3 tools/process-photos.py --slug NAME photo.jpg   # prepare a photo for Our work (upright, metadata removed, 1600px and 800px); prints the gallery_data.py line
python3 tools/shots.py ../shots-before          # full-page screenshots (1440 and 390 px, or --widths=320,768,1024); keep the folder outside the project
python3 tools/shots-diff.py ../shots-before ../shots-after   # which pictures changed and by how much
python3 tools/a11y-check.py index.html ...      # accessibility scan (Playwright and axe-core, run from the folder that has node_modules); give .html names; also tests the Our work photo viewer
python3 tools/checkpoint.py --write "label"     # end of session, after everything passes
python3 -m http.server 8000                     # preview at http://localhost:8000
```

## If something looks wrong

- **The "Git" lines of the checkpoint tool look stale in the cloud workspace** (an old commit, many "changed" files): that copy has its own old `.git`. Ignore it there; the real history is `.git/logs/HEAD` in Jeremy's folder.
- **Checkpoint reports "CHANGED":** a tracked file differs from the last checkpoint. If Jeremy edited it on purpose, accept it and record it in the session log; if not, find out before building on it.
- **Checkpoint reports the sprite or an image:** saving through the bridge adds an invisible tag to images and to `tools/pages/_sprite.html`. The tool and the builder already ignore it.
- **A script's scrolling is undone, or full-page screenshots show blank photo frames:** the pages hold themselves at the top until a visitor touches, scrolls or presses a key (or 8 seconds pass), and the photos use native lazy loading. A script must press a key first, then scroll in steps and wait (`tools/shots.py` does).
- **The Contact page's FAQ is chosen by exact question text** (`FAQ["contact"]` in `tools/build-pages.py`): "Do I have to sell to you if I reach out?", "How do I know GLP is legit?" and "What areas do you serve?". If a later session rewords one of those three, it silently drops off the Contact page; change the filter at the same time.
- **The GoHighLevel form looks wrong live:** it cannot be tested from the workspace. Record what Jeremy sees and defer to Session 11.
- **Facebook:** our tools cannot fetch it (it refuses them) and we never sign in. Ask Joey or Jeremy for saved photos or video files.
- **Our work photo groups:** photos of mixed shapes flow into columns; a group whose photos are all the same shape sits in rows (the builder decides). Seven same-shape Building photos leave one photo alone in the last row; a "More on Facebook" tile could fill it.

## Suggested commit message for this session (Jeremy)

Subject: Our work page, plainer wording, simpler header, pages open at the top on phones

Body:
- New Our work page: 16 photos in three groups with a keyboard-friendly photo viewer
- Plain-talk pass: quiz and numbers strip removed, "Joey or Ethan" instead of "our team"
- Header: no phone number, full menu from 1241px; the menu highlight clears at the top
- Pages open at the very top on phones
- Photo tools, a git ignore for the photo inbox, notes and checkpoint 12

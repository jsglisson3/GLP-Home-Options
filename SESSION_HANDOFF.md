# Session handoff

> **IN PROGRESS (Oct 21, about 9 PM CT):** Jeremy asked for the site to feel like two real people, not a company, and for the gallery. Saved so far, not yet checkpointed: a wording pass (no more "we're real" announcements, "Joey or Ethan" instead of "our team"), and the removal of the "What matters most?" quiz and the hero stats strip. The "Our work" gallery page is being built next. The notes below still describe Checkpoint 11 until the final notes replace this file.

**Written:** Oct 21, 2026, at the end of the planning session after Session 6d, Checkpoint 11.
**Replace this file at the end of every session.** It describes exactly one next session and what is true right now. The long-term plan is in `ROADMAP.md`; the full state is in `PROJECT_STATUS.md`.

## Where the project is

- **Live site = Jeremy's commit "more changes" (5:13 PM CT) = Checkpoint 10**, at https://jsglisson3.github.io/GLP-Home-Options/ (`noindex`). All 7 pages are live. Checked by fetching the live stylesheet with a cache-busting query (`?cb=...`; the fetch tool caches 15 minutes).
- **Approved by Jeremy:** D1 (navy leads, green accent); D2 (warm cream, now the whole site's one tint); D4 (hero A, people-led, in the gable frame); D5 (restrained glass and motion, as a direction; the exact list is Session 4); "Joey's own words now" for claims. D3 and D6 proceed by default.
- **Built today (Sessions 3 to 6d):** hero A is live; the header is simple and blends into the cream hero on every page, and "Get my options" shows beside Menu on tablets; floating hero tags, the pulsing pill, path chips, button shine and the numbers count-up are gone; the hero photo is sharper, warmer and has headroom (the unedited original is in `research/photos/from-old-build/`); the prototype files were deleted.
- **The planning session (this one) changed no live page.** It produced `research/site-review-2026-10-21.md` (15 ranked findings), **Proposed plan v2 with decisions D7 to D11** in `ROADMAP.md`, a send-ready question list for Joey, `research/questions-for-joey.md`, a photo brief for him, `research/photo-brief-for-joey.md`, and a counted CSS inventory for Session 5, `research/css-inventory-2026-10-21.md`. It also added `tools/claims-check.py` and `tools/shots.py` with `tools/shots-diff.py`.
- **Biggest risk found:** the origins of two people photos (the bridge hero and the kitchen table) are unconfirmed, and their alt text states them as real events. Also the riverfront banner is soft and the closing photo shows third parties. Ask Joey (review F1 to F3).
- **Waiting on Jeremy:** his answers to D7 to D11; what else at the top of the page looked gimmicky (I only changed the phone number, Facebook logo, scroll line and the tablet button); sending the Joey text.
- **Waiting on Joey:** photo originals and origins; every claim tagged **J** in `CONTENT_CLAIMS.md`; license or brokerage; the county list; the main phone number; reviews; GoHighLevel access; the domain. A lawyer should look at how seller financing and lease options are described.

## Next session: Session 4, direction lock (30 to 45 minutes)

**Objective:** turn the approved decisions into the formal design system and set the exact glass list. **No change to any real page.**

### Needed from Jeremy (first message, short)

1. His answers to **D7 to D11** in `ROADMAP.md` ("go with your recommendations" is a valid answer). D8 (headline rule) and D10 (glass list) feed this session directly.
2. What else at the top of the page looked gimmicky, if anything. One question.

### Start protocol (5 minutes)

1. Read `PROJECT_STATUS.md`, this file, `ROADMAP.md` (Sessions 4 and 5 and "Proposed plan v2") and `DESIGN_SYSTEM.md`.
2. Get the project from Jeremy's folder, not from memory: `C:\Users\jsgli\Documents\GLP-Home-Options` (stage everything, including `images/`, `fonts/` and `research/photos/`; at most 50 files per staging call). Run `python3 tools/checkpoint.py`. **Expected: clean at Checkpoint 11** (ignore the workspace's stale "Git" lines). If not, stop and find out why.
3. Read the newest line of `.git/logs/HEAD` in his folder (stage it, then read it); if he has pushed, fetch the live Home page or stylesheet with a cache-busting query.

### What to do

1. **Inventory the glass** with `grep -n "backdrop-filter" css/site.css`. At Checkpoint 10 there are 5 uses: `.hdr` (header), `.founder figcaption` (name plates on the portraits), `.reach-item` (contact cards on the dark section), `.mobile-bar` (phone bottom bar) and `.jump` (Options "jump to" panel). Recommendation (D10): keep `.hdr`, `.mobile-bar` and `.reach-item`; make `.founder figcaption` and `.jump` solid. Record the final list; the CSS change itself is Session 5.
2. **Label `DESIGN_SYSTEM.md`:** every token and rule is DIRECTED, APPROVED or PROPOSED. Already approved: color hierarchy and hex values (D1), the cream tint (D2), hero A (D4), the hero tag system rules (now mostly retired), D5 as a direction. Leave P1, P2, P4, P5, P6 as proposals for Session 5 unless Jeremy decides now. Record the headline rule (D8) once he answers.
3. **Check the docs agree** with each other and with the code (decisions, dates, next session).

### Do not change

Every real page, `css/site.css`, `js/site.js`, `tools/build-pages.py`, `tools/pages/*`; the claims; the phone, email, Facebook URL, form id and booking id; the `noindex` tag.

### Done means

- `DESIGN_SYSTEM.md` has no unlabeled token or rule; the glass list is written down and Jeremy has approved it (or "pending" is recorded).
- `PROJECT_STATUS.md` (session log, section G, "Last updated") and `ROADMAP.md` updated; this file replaced with the Session 5 handoff; `python3 tools/checkpoint.py --write "Session 4: direction lock"` run last.

### End-of-session protocol (every session)

1. Verify (rebuild, `check-links.py`, `claims-check.py`, accessibility scan; for Session 5, `shots.py` before and after). 2. Update the docs. 3. Write the checkpoint (`--write` raises the number every time it runs). 4. In **one** step stage every changed file into the outputs folder (use `|| exit 1` after each copy: lines after a failed heredoc still run); in a **separate, later** step commit them to Jeremy's folder; read them back and compare hashes (images gain an invisible tag when saved, so compare their pixels; if a read-back is stale, commit again with `force`). 5. Give Jeremy the commit message. He stages (+), commits and syncs in VS Code Source Control. 6. Fetch the live site after he syncs, if he says he has.

## Commands

```
python3 tools/checkpoint.py                     # start of session: does the code match the last checkpoint?
python3 tools/build-pages.py                    # rebuild the 7 pages from tools/pages/*.html and the builder
python3 tools/check-links.py                    # every link, anchor, image and script on every root page
python3 tools/claims-check.py                   # the "never invent" rule: no credentials, ratings, awards, results or founding years unless allowlisted
python3 tools/shots.py ../shots-before          # full-page screenshots (1440 and 390 px, or --widths=320,768,1024); keep the folder outside the project
python3 tools/shots-diff.py ../shots-before ../shots-after   # which pictures changed and by how much
python3 tools/a11y-check.py index.html ...      # accessibility scan (Playwright and axe-core); give .html names
python3 tools/checkpoint.py --write "label"     # end of session, after everything passes
python3 -m http.server 8000                     # preview at http://localhost:8000
```

## If something looks wrong

- **The "Git" lines of the checkpoint tool look stale in the cloud workspace** (an old commit, many "changed" files): that copy has its own old `.git`. Ignore it there; the real history is `.git/logs/HEAD` in Jeremy's folder.
- **Checkpoint reports "CHANGED":** a tracked file differs from the last checkpoint. If Jeremy edited it on purpose, accept it and record it in the session log; if not, find out before building on it.
- **Checkpoint reports the sprite or an image:** saving through the bridge adds an invisible tag to images and to `tools/pages/_sprite.html`. The tool and the builder already ignore it.
- **Full-page screenshots show blank photo frames:** the photos use native lazy loading, so a script must scroll down the page in steps (and wait) before it takes the shot.
- **The Contact page's FAQ is chosen by exact question text** (`FAQ["contact"]` in `tools/build-pages.py`): "Do I have to sell to you if I reach out?", "How do I know GLP is legit?" and "What areas do you serve?". If a later session rewords one of those three, it silently drops off the Contact page; change the filter at the same time.
- **The GoHighLevel form looks wrong live:** it cannot be tested from the workspace. Record what Jeremy sees and defer to Session 11.
- **Facebook shows only one post:** expected when logged out. Never sign in; ask Joey for photos instead.

## Suggested commit message for this session (Jeremy)

Docs and research only; no live page changed.

Subject: Planning: site review, proposed plan v2 and decisions, questions for Joey

Body:
- Full-site review with ranked findings (research/site-review-2026-10-21.md)
- Proposed plan v2 with decisions D7 to D11 for Jeremy to answer (ROADMAP.md)
- Send-ready question list for Joey (research/questions-for-joey.md)
- Photo brief for Joey; CSS inventory for the consolidation session
- New tools: a claims check and a before/after screenshot comparison
- Session handoff rewritten; project notes updated

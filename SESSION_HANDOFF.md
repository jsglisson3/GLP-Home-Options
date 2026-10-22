# Session handoff

**Written:** Oct 21, 2026, about 11:55 PM CT, at the wind-down of Session 6g, Checkpoint 15. Checkpoints 13 and 14 came just before it and are already live.
**Replace this file at the end of every session.** It describes exactly one next session and what is true right now. The long-term plan is in `ROADMAP.md`; the full state is in `PROJECT_STATUS.md`.

## Where the project is

- **Live site = Jeremy's commit "trim and simple" (11:45 PM CT, Checkpoint 14), pushed 11:45:53 PM** (his repo log shows three pushes tonight: 11:05, 11:30 and 11:45) at https://jsglisson3.github.io/GLP-Home-Options/ (`noindex`). It has the Our work page, the six-link header, the menu-highlight and start-at-top fixes, the trimmed Options page, the simplified net sheet and the SOLD-sign photo. Checkpoint 12 was "big push" (`9d79ab4`, 11:05 PM); Checkpoint 13 was "form changes" (11:30 PM).
- **Checkpoint 15 is saved in his folder and waits for him to commit and sync.** It changes only Home and About (words cut, below). Earlier: Checkpoint 13 (Session 6f) changed no page: notes and three research files about the contact form (below), updated Joey questions, Jeremy's tone and audience direction. **Checkpoint 14 (Session 6g, committed) changed live pages:** the **Options page is trimmed** by cutting words (1,263 down to 1,113 words; 8,829 down to 7,450 px on a laptop), the **net sheet on Home is simplified** (three boxes up front, the five assumed costs under "Change the costs we assumed", no bars; same math, tested), and a **SOLD-sign photo is added to Our work** under the September closing as "Another closing day" (not confirmed by Joey; `CONTENT_CLAIMS.md` row 47). CSS v32, JS v14. Two new tools: `tools/netsheet-test.py` (run it after any net sheet change) and `tools/page-size.py` (page height and words).
- **Approved by Jeremy:** D1 (navy leads, green accent); D2 (warm cream, the whole site's one tint); D4 (hero A, people-led, in the gable frame); D5 (restrained glass and motion, as a direction; the exact list is Session 4); D6 (the gallery is its own "Our work" page, approved Oct 21, 8:40 PM); "Joey's own words now" for claims. D3 proceeds by default.
- **Jeremy's direction, Oct 21, 11:09 to 11:11 PM** (`DESIGN_SYSTEM.md`, section 0, items 8a to 8c): professional but not too corporate; best guidelines but not cookie-cutter; authentic, not a sellout. The people selling are ordinary homeowners, many short on money and time, many wary of "we buy houses" ads, so: plain words, no pressure, no luxury gloss, short forms, phone first.
- **The contact form looks like a bolt-on** (Jeremy: "scammy, like an ad on top of the website"). It is GoHighLevel's default in an iframe from `links.voiseai.com`; only someone with GoHighLevel access can restyle it. **A tested fix is ready:** `research/ghl-form-style.md` (what is wrong, steps, what to check), `research/ghl-form-custom.css` (paste-ready) and `research/ghl-form-before-after.jpg`. The button still says "Button". The consent text now names "GL Partners LLC DBA GLP Home Options" with no placeholders left. Not tested: the form inside our page (the AI's browser tab shows the frame blank), error messages, a phone width.
- **The photos on Our work rest on Jeremy's word.** The eight renovation photos came from Joey's personal Facebook via Jeremy; Joey has not confirmed they are his projects, that he wants them shown, or who took them (`CONTENT_CLAIMS.md` rows 42 to 46). The site is `noindex` meanwhile.
- **No street address is in any repo file, on purpose.** The six properties Jeremy named are in a private log **outside the repo**: `C:\Users\jsgli\Documents\GLP-private\flips-log.md` (his words, links, the questions for Joey, the photo rules, notes on three videos and a photo with a SOLD sign). Read it at the start of a session that touches the gallery; keep adding to it.
- **Videos and the SOLD photo (Oct 21, about 10:55 to 11:01 PM):** Jeremy saved three screen recordings of Joey's Facebook videos and one photo of three people holding a SOLD sign into `research/photos/incoming/`. **None is used on the site** (reasons are in the private log). Best path: ask Joey for the originals. A video on the site is a scope decision (D11 lists an intro video as "not now"). `Facebook.mhtml` in the same folder was not opened and should be deleted by Jeremy.
- **`research/photos/incoming/` is the photo and video inbox.** New files there are ignored by git (`.gitignore`) and by the checkpoint tool. The 16 photos that were dropped there earlier tonight were **already committed**, so they are public (the repo is public); that cannot be undone from here.
- **Biggest risks:** the origins of two people photos on the live pages (the bridge hero and the kitchen table; review F1 to F3); the riverfront banner is soft; the closing photo shows third parties and a title company's branding; the contact form's look and the consent wording (a fix is ready; it needs GoHighLevel access and a lawyer's read).
- **Waiting on Jeremy:** try the start-at-top fix on his phone (open a page, scroll, reload, and open it from a bookmark and from a link in a message; tell me if any still starts in the middle, and how he got there); get Joey to add him to GoHighLevel or paste the CSS himself; answers to D7 to D11 (`ROADMAP.md`, "Proposed plan v2"); sending the Joey text (`research/questions-for-joey.md`); whether to delete `Facebook.mhtml`.
- **Waiting on Joey:** the photo confirmations (rows 42 to 46), photo and video originals, the SOLD-photo people and title company, every claim tagged **J**, license or brokerage (his videos say "New Listing coming soon"), the county list, the main phone number, reviews, GoHighLevel access, the domain. A lawyer should look at how seller financing and lease options are described.

## Next: the overnight run (Jeremy is going to sleep; nothing goes live until he commits in the morning)

**His rules for it:** trim words first, then plain talk (11:30 PM). Tone: professional but not too corporate, not cookie-cutter, authentic (11:10 PM). Audience: ordinary homeowners short on money and time, wary of "we buy houses" ads (11:11 PM). **The net sheet is crucial** (11:33 PM; done once, keep it simple). The new "The numbers" page (D7) is parked: leave the compare table and net sheet where they are.

Do these in order. **One checkpoint and one save per step**, so he can accept or reject each by commit. If a check fails and cannot be fixed in a few minutes, undo that step (the files saved before it are the safe state) and write what happened at the top of this file.

1. **Trim words on New homes and Contact, then take a second look at Home.** (**Done:** the Options page (Checkpoint 14) and, at Checkpoint 15, About (662 words) and Home (1,382 down to 1,328 words; its three FAQ questions on speed, fixing and fees became one). Session 6g in `PROJECT_STATUS.md` shows the method. New homes is 372 words and Contact 326, both already short, so aim for about 10% there. **Home is still about 12,100 px tall because of structure, not words;** see the proposals below, which need Jeremy's approval.) Cut sentences that repeat another, list items that say the same thing twice, and cards that repeat each other. Keep every "Maybe not if", every confirmed claim (`CONTENT_CLAIMS.md`), and the phone, email, Facebook link, form id and booking id. Targets: Home toward about 1,000 words only if he approves the structure changes below; the others by about 10%. Measure with `python3 tools/page-size.py PAGE` before and after.
2. **Plain-talk pass on every page, after step 1.** Short sentences, everyday words, no pitch language. Explain or drop jargon (MLS, carrying costs, as-is, equity, title company, off-market): say what it means in the same sentence. Talk about money the way a neighbor would. Phone first. Add no claims; keep `python3 tools/claims-check.py` clear. Read the net sheet labels last.
3. **The contact section, our side of the frame** (Home and Contact): a calmer card (softer shadow), Joey and Ethan's faces beside the form, three short lines on what happens next, the phone number as the first choice. Do not replace the form or touch the consent wording; its own look stays a GoHighLevel job (`research/ghl-form-style.md`).
4. **Final QA and a morning handoff:** before and after pictures (`tools/shots.py`) for every changed page; axe (see Commands); links; claims; `python3 tools/netsheet-test.py` (must print `FAILS 0`); 320 to 390 px widths. Replace this file with a short morning summary at the top: what changed, what to look at first, what to reject if he does not like it, and the commit messages.

**Do not:** build the numbers page; change the glass; add claims or photos; change the phone, email, Facebook link, form id, booking id or the `noindex` tag; sign in anywhere; put a street address in any repo file.

**Proposals that need Jeremy's approval (list them in the morning notes; do not do them overnight):** Home is long because it repeats what other pages say, not because of wordy sentences. (a) Fold the "How it works" steps into the option cards, since Home already has a 3-step "What happens next" block by the form. (b) Move the panoramic photo band into About, which says the same thing. (c) Cut the Home FAQ to about 5 to 7 questions (it has 9 after tonight's merge; the full set stays on the Options page). (d) About repeats Home's "Why we do this" panel, "Beyond buying" band and "Is GLP legit?" tiles; keep each idea on one page. (e) The numbers on their own page (D7) stays parked.

## After the overnight run: Session 4, direction lock (30 to 45 minutes)

**Objective:** turn the approved decisions into the formal design system and set the exact glass list. **No change to any real page.** The glass inventory is already done (5 uses; `DESIGN_SYSTEM.md` section 5) and Checkpoint 13 recorded the D10 recommendation; what is left is Jeremy's answers.

### Needed from Jeremy (first message, short)

1. That Checkpoints 13 and 14 and the overnight checkpoints are committed and synced, and whether the start-at-top fix works on his phone.
2. His answers to **D7 to D11** in `ROADMAP.md` ("go with your recommendations" is a valid answer). D8 (headline rule) and D10 (glass list) feed this session directly.
3. What else at the top of the page looked gimmicky, if anything. One question.

### Start protocol (5 minutes)

1. Read `PROJECT_STATUS.md`, this file, `ROADMAP.md` (Sessions 4 and 5 and "Proposed plan v2") and `DESIGN_SYSTEM.md`.
2. Get the project from Jeremy's folder, not from memory: `C:\Users\jsgli\Documents\GLP-Home-Options` (stage everything except `research/photos/incoming/`, which can hold big videos; include `images/`, `fonts/` and the rest of `research/photos/`; at most 50 files per staging call). Run `python3 tools/checkpoint.py`. **Expected: clean at the newest checkpoint** (ignore the workspace's stale "Git" lines). If not, stop and find out why.
3. Read the newest line of `.git/logs/HEAD` in his folder (stage it, then read it); if he has pushed, fetch the live Home page, Our work page or stylesheet with a cache-busting query.

### What to do

1. **Inventory the glass** with `grep -n "backdrop-filter" css/site.css` (done once: 5 uses). Recommendation (D10): keep `.hdr`, `.mobile-bar` and `.reach-item`; make `.founder figcaption` and `.jump` solid. Record the final list; the CSS change itself is Session 5.
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
python3 tools/page-size.py options              # a page's height and word count, section by section, at 1440 and 390 px
python3 tools/netsheet-test.py                  # the net sheet math against an independent calculation (must print FAILS 0)
python3 tools/a11y-check.py index.html ...      # accessibility scan (Playwright and axe-core, run from the folder that has node_modules; `npm i axe-core` first in a new session); give .html names; also tests the Our work photo viewer
python3 tools/checkpoint.py --write "label"     # end of session, after everything passes
python3 -m http.server 8000                     # preview at http://localhost:8000
```

## If something looks wrong

- **The "Git" lines of the checkpoint tool look stale in the cloud workspace** (an old commit, many "changed" files): that copy has its own old `.git`. Ignore it there; the real history is `.git/logs/HEAD` in Jeremy's folder.
- **Checkpoint reports "CHANGED":** a tracked file differs from the last checkpoint. If Jeremy edited it on purpose, accept it and record it in the session log; if not, find out before building on it.
- **Checkpoint reports the sprite or an image:** saving through the bridge adds an invisible tag to images and to `tools/pages/_sprite.html`. The tool and the builder already ignore it.
- **A script's scrolling is undone, or full-page screenshots show blank photo frames:** the pages hold themselves at the top until a visitor touches, scrolls or presses a key (or 8 seconds pass), and the photos use native lazy loading. A script must press a key first, then scroll in steps and wait (`tools/shots.py` does).
- **The Contact page's FAQ is chosen by exact question text** (`FAQ["contact"]` in `tools/build-pages.py`): "Do I have to sell to you if I reach out?", "How do I know GLP is legit?" and "What areas do you serve?". If a later session rewords one of those three, it silently drops off the Contact page; change the filter at the same time.
- **The GoHighLevel form looks wrong live:** the AI cannot test it inside our page (its browser tab shows the frame blank) and must never sign in or fill the form. It can be looked at on its own address, `https://links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ`, with nothing typed. Use `research/ghl-form-style.md`; record what Jeremy sees.
- **The AI's browser tab is hidden:** `requestAnimationFrame` never fires and computed styles can be stale mid-transition, so check with screenshots and synchronous scripts, not timers.
- **Facebook:** our tools cannot fetch it (it refuses them) and we never sign in. Ask Joey or Jeremy for saved photos or video files.
- **Our work photo groups:** photos of mixed shapes flow into columns; a group whose photos are all the same shape sits in rows (the builder decides). Seven same-shape Building photos leave one photo alone in the last row; a "More on Facebook" tile could fill it.

## Suggested commit messages (Jeremy)

Checkpoints 12, 13 and 14 are already committed and pushed ("big push", "form changes", "trim and simple"). **Checkpoint 15:**

Trim repeated words on Home and About

- Home: cut repeated phrases in the option cards, the strip under them and the About band; three FAQ questions (how fast, fix and clean, fees) merged into one with every fact kept
- About: four sentences shortened
- No claim, number, photo, style or script changed; checkpoint 15

(If the overnight run adds more checkpoints, each has its own message at the top of this file.)

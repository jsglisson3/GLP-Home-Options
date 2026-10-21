# Session handoff

**Written:** Oct 21, 2026, at the end of Session 1 (Phase 0), Checkpoint 1.
**Replace this file at the end of every session.** It always describes exactly one next session. The long-term plan is in `ROADMAP.md`; the full state is in `PROJECT_STATUS.md`.

## Where the project is

- A complete draft is **live** on GitHub Pages (commit `b6cc372`, `noindex`). Session 1 changed **no site files**; it created the project record and a checkpoint tool.
- `python tools/checkpoint.py` is clean at Checkpoint 1 (a fresh build reproduces all 7 pages; 339 links resolve).
- Six claims on the draft are not in Joey's own materials. They are the first thing to fix.

## Next session: Session 2, decisions intake and accuracy patch (30 to 40 minutes)

**One objective:** make the site say only what Joey's own materials support, and record Jeremy's answers to the design decisions. **No visual changes.**

### Needed from Jeremy (ask in the first message)

1. **Did you commit and sync Checkpoint 1?** (If not, do that first; message below.)
2. **D1 to D6** from `PROJECT_STATUS.md` section C. "Go with your recommendations" is a valid answer. Record the answers there as APPROVED, with the date.
3. **Anything Joey has answered** (counties, seller financing and lease options, free consultation, hours, second phone number). If Joey has not answered, use the conservative wording below.
4. Whether the repository should stay public (see the risk in `PROJECT_STATUS.md`). No change is needed now.

### Start protocol (5 minutes, in this order)

1. Read `PROJECT_STATUS.md`, this file, `CONTENT_CLAIMS.md` ("Fix first") and `ROADMAP.md` (Session 2).
2. Get the project from Jeremy's folder, not from memory: `C:\Users\jsgli\Documents\GLP-Home-Options` (list it, then stage the files into a working folder; about 70 files, at most 50 per staging call, so two calls; stage everything, including `images/`, `fonts/` and `research/photos/`, or the link check and checkpoint will report missing files).
3. Run `python tools/checkpoint.py`. **Expected: clean.** If it reports differences, stop and find out why before editing (the folder was edited elsewhere, or a sync is pending), and tell Jeremy.
4. Read the newest line of `.git/logs/HEAD` in his folder to see the latest commit. Fetch the live Home and Contact pages and confirm they match.

### The work: the six "Fix first" claims

Line numbers are as of Checkpoint 1; search the quoted text if they have moved. Edit the **sources** (`tools/build-pages.py`, `tools/legal_text.py`, `tools/pages/*.html`), never the generated root pages. If Joey has confirmed a claim, keep it, mark it **V** in `CONTENT_CLAIMS.md` with the date and his words, and skip its change.

| # | Claim | Where | Conservative replacement (Joey's own wording where it exists) |
|---|---|---|---|
| 1 | Seller financing and lease options | `build-pages.py` 55, 61, 257 (meta and structured-data descriptions); FAQ data 114-115, 131-135; `pages/index.html` 141; `pages/options.html` 23, 212, 221-222; `pages/about.html` 58 | Use Joey's sentence: "For unique situations where standard paths do not feel like a fit, we explore structured options together." Remove the "Do you offer seller financing or lease options?" FAQ and the two explainer FAQs (the FAQ list also feeds the FAQPage data, so they disappear from both). Remove the definitions list on Options. Rewrite the three descriptions without the phrase. |
| 2 | "surrounding counties" | `build-pages.py` 119 (FAQ), 261 (`areaServed` "Surrounding counties"), 350 (footer pill); `pages/index.html` 14, 347; `pages/about.html` 15; `pages/contact.html` 12 | "Chattanooga, TN" (Joey's site) and "Based in Hixson" (Facebook). Drop the `Place` "Surrounding counties" from structured data. Ask Joey for a real list. |
| 3 | "doing business as" | `legal_text.py` 58; `pages/contact.html` 12 | His exact words: "GLP Home Options (Legal entity: GL Partners LLC)". |
| 4 | "free" consultation, "No obligation, ever" | `build-pages.py` 100, 138 (FAQ), 406 (CTA note); `pages/index.html` 18 ("Request a free consultation"), 21; `pages/options.html` 15 | His labels: "Request a Consultation"; "No obligation. Your information is kept confidential." Drop "free" and "ever". (The "$0 commission" card on the hero is verified; leave it.) |
| 5 | "anytime" | `build-pages.py` 102, 454; `pages/index.html` 33; `pages/about.html` 149; `pages/contact.html` 13 | "Call or text", "Reach us by phone, text or email". **Leave** "opt out at any time" in `legal_text.py` 45 and 91 (that is a consumer right, not an availability claim). |
| 6 | Example offer of $255,000 | `pages/index.html` 271 (default value); `pages/options.html` 271 (sentence) | Needs a decision. Default plan: keep the example, and add a one-line label next to the field: "An example, not a GLP quote. Real offers depend on the home." Ask Joey if he would rather use a different number or leave it blank. |
| (29) | "Takes about a minute" | `build-pages.py` 469; `pages/index.html` 21; `pages/options.html` 254 | "Share a few details." (The form has about 8 fields.) |

Everything else in the register that says **OURS** (for example "You'll talk to Joey or Ethan") stays for now; it is a question for Joey, not a change for this session.

### Do not change

Visual design, layout, CSS or JavaScript; the phone, email, Facebook URL, form id, booking id; the net sheet formulas; the `noindex` tag; the Facebook placements; page structure and URLs; anything on the Options page that is marked **V** in the claims register (7-14 days, no commission, 6%, 2-3%, 45-90+ days).

### Done means

- `grep -il -E "seller financ|lease option|surrounding count|doing business|anytime|free consult|ever\." *.html` returns only claims Joey confirmed (and nothing from the two "at any time" lines).
- `python tools/build-pages.py`, then `python tools/check-links.py` pass; `python tools/a11y-check.py` shows 0 violations if it can be run (setup is at the top of the file); look at Home, Options and Contact at phone width in screenshots (text-only changes should not shift the layout; watch for wrapping in the hero and the footer pill).
- `CONTENT_CLAIMS.md` statuses updated; `PROJECT_STATUS.md` updated (section C decisions, E4 features, F session log, G handoff); this file replaced with the Session 3 handoff.
- `python tools/checkpoint.py --write "Session 2: accuracy patch"` run last.

### End-of-session protocol (every session)

1. Verify (above). 2. Update the docs. 3. Write the checkpoint. 4. In **one** step stage every changed file (generated pages, sources, docs, `CHECKPOINT.json`) into the outputs folder; in a **separate, later** step copy them to Jeremy's folder; list the folder to confirm sizes. 5. Give Jeremy the commit message. He stages (+), commits and syncs in VS Code Source Control. 6. Fetch the live site after he syncs, if he says he has.

## Commands

```
python tools/checkpoint.py                      # start of session: does the code match the last checkpoint?
python tools/build-pages.py                     # rebuild the 7 pages from tools/pages/*.html and the builder
python tools/check-links.py                     # every link, anchor, image and script
python tools/a11y-check.py                      # accessibility scan (needs Playwright and axe-core)
python tools/checkpoint.py --write "label"      # end of session, after everything passes
python -m http.server 8000                      # preview at http://localhost:8000
```

## Suggested commit message for Checkpoint 1 (Jeremy)

```
Checkpoint 1: Phase 0 audit and project record

Add PROJECT_STATUS, ROADMAP, DESIGN_SYSTEM, CONTENT_CLAIMS, SESSION_HANDOFF, CHECKPOINT.json and tools/checkpoint.py. Rewrite README and turn PICKUP into a pointer. No site files changed.
```

## If something looks wrong

- **The "Git" lines of the checkpoint tool look stale in the cloud workspace** (an old commit, many "changed" files): that copy has its own old `.git`. Ignore it there; the real history is `.git/logs/HEAD` in Jeremy's folder.
- **Checkpoint reports "CHANGED":** a tracked file differs from the last checkpoint. Look at which. If Jeremy edited it on purpose, accept it and record it in the session log. If not, find out before building on it.
- **Checkpoint reports the sprite or an image:** saving through the bridge adds an invisible provenance tag to images and to `tools/pages/_sprite.html`. The tool and the builder already ignore it.
- **The GoHighLevel form looks wrong live:** it cannot be tested from the workspace. Record what Jeremy sees and defer to Session 11.
- **Facebook shows only one post:** expected when logged out. Never sign in; ask Joey for photos instead.

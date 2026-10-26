# GLP Home Options: website

Website for **GLP Home Options** (Joey & Ethan), Chattanooga / Hixson, TN. Plain HTML, CSS and JavaScript. Nothing to install to host it.

> Status: **working draft** for Joey's review. Set to `noindex` so search engines skip this preview copy. Not ready to replace glphomeoptions.com yet. **Start with `PROJECT_STATUS.md`**: it is the map (where things stand, decisions, open questions, session log). The code is the truth; if the two disagree, believe the code and fix the notes.

## Project documents

| File | What it holds |
|---|---|
| `PROJECT_STATUS.md` | Current state, approved decisions, implementation record, session log. Names the other documents. |
| `SESSION_HANDOFF.md` | Exactly what the next working session does. Replaced at the end of every session. |
| `ROADMAP.md` | The phases and the session-by-session plan |
| `DESIGN_SYSTEM.md` | Colors, type, spacing, motion, components; each marked directed, built or proposed |
| `CONTENT_CLAIMS.md` | Every factual claim on the site, its source, and what Joey still needs to confirm |
| `CHECKPOINT.json` | Fingerprints of the files at the last verified checkpoint (written by `tools/checkpoint.py`) |
| `PICKUP.md` | Retired. Points to the files above. |

## The pages

| File | What it is |
|---|---|
| `index.html` | Landing page: the story, three paths, the numbers, FAQ, contact form |
| `options.html` | Your options: sell direct, list, keep the home, creative solutions |
| `about.html` | Our story: Joey and Ethan, what they stand for, the September closing |
| `work.html` | Our work: photos from the job sites and a recent closing, with a photo viewer |
| `new-homes.html` | New homes: the home they're building now (kept deliberately light) |
| `contact.html` | Contact: call, text, email, book, Facebook, and the form |
| `privacy-policy.html`, `terms-of-service.html` | Plain-words legal pages (draft, not lawyer-reviewed) |

## How the site is built (read before editing)

The header, footer, icon sprite, FAQ and contact block repeat on every page, so they are generated from one place. The output is still plain files; GitHub Pages serves them as-is.

```
python3 tools/build-pages.py     # rewrites all 8 pages from the shared pieces
python3 tools/check-links.py     # every link, anchor, image and script resolves; no duplicate ids
```

- **Edit** `tools/pages/<page>.html` (the middle of each page), `tools/build-pages.py` (header, footer, FAQ text, page titles, phone/email/Facebook, structured data), `tools/legal_text.py` (Privacy and Terms wording), `css/site.css`, `js/site.js`, `js/gallery.js` (the photo viewer).
- **Don't edit** the root `.html` files by hand. They get overwritten the next time the builder runs.
- After changing `css/site.css` or `js/site.js`, bump `CSS_V` / `JS_V` at the top of `tools/build-pages.py` and rebuild (this makes browsers fetch the new file).
- Commit the generated root `.html` files too, since that is what GitHub Pages serves.
- The link to the "New homes" page is one constant, `NEW_HOMES`, in `tools/build-pages.py`. If the construction business gets its own site, point that one line at it.

## What's here

- `css/site.css`, `js/site.js`: all styling and behavior
- `images/`, `fonts/`: photos, logo, favicons, share picture, self-hosted fonts (`images/work/` holds the Our work photos)
- `tools/`: page builder, link checker, accessibility test, checkpoint check, legal text, share-picture generator
- `research/`: source photos, reviews and research notes (not loaded by the site, but this repository is public, so everything in it can be seen, except the folder `research/private/` and the rules notes, which `.gitignore` keeps out and which stay in the family's folder only)

## Adding photos to Our work

1. Drop the originals into `research/photos/incoming/` (this folder is ignored by git, so new files in it are not published; photos and videos Joey has not OK'd should stay there or outside the folder).
2. Prepare each one: `python3 tools/process-photos.py --slug some-name "research/photos/incoming/photo.jpg"` (it straightens the photo, removes camera and location data, and writes `images/work/some-name.jpg`, plus a small version for big photos). It prints the line to paste next.
3. Paste that line into `tools/gallery_data.py`, choose the group and write the caption and the alt text from what the photo shows. Never put a street address, price or house count in either.
4. Add a row for it in `CONTENT_CLAIMS.md`, rebuild (`python3 tools/build-pages.py`), and run the checks.

Street addresses of homes Joey flipped or sold are kept in a private log outside this folder, never in the repository.

## Preview on your computer

Open a terminal in this folder and run `python -m http.server 8765`, then visit http://127.0.0.1:8765/. (Double-clicking `index.html` also works, but the browser console shows harmless font warnings.)

## Hosting on GitHub Pages

Same setup as FOTCL (`github.com/jsglisson3/FOTCL`). `.nojekyll` is included.

1. Repo: `github.com/jsglisson3/GLP-Home-Options`, branch `main`.
2. On GitHub: **Settings, Pages, Deploy from a branch, `main` / `(root)`, Save**. (Only needed once.)
3. About a minute after each push it's live at **https://jsglisson3.github.io/GLP-Home-Options/**

**The 404 page and the real domain.** `404.html` (generated from `tools/pages/404.html`) is what GitHub Pages shows for any address that does not exist. Its links and files are written as `/GLP-Home-Options/...` (root-absolute, so it works at any depth); the prefix comes from `SITE` in `tools/build-pages.py`. When the site moves to glphomeoptions.com, change `SITE` to `https://glphomeoptions.com/`, rebuild, and the prefix becomes `/` by itself (`tools/check-links.py`, `tools/notfound-test.py` and `tools/_site.py` all read it from there).

To publish a change in VS Code: **Source Control** (left bar), stage all changes (the **+** next to "Changes"), type a short message, **Commit**, then **Sync Changes**.

## Checking your work

- `python tools/checkpoint.py` compares the project with the last saved checkpoint (`CHECKPOINT.json`), confirms a fresh build reproduces the saved pages, and runs the link check. Run it at the **start** of a session (it should say "clean"). At the **end**, once everything passes, run `python tools/checkpoint.py --write "short label"`.
- `python tools/form-test.py` checks that the contact form always shows up, or falls back to a call or text card (Checkpoint 35). The real form lives on GoHighLevel's server and this test cannot reach it, so it stands in for the form in a test browser and plays what a visitor can meet: fine, blocked, never loads, no JavaScript. It must print `FAILS 0`. Run it after any change to the "Contact form" part of `js/site.js` or the `.ghl` rules in `css/site.css`; the form frame is added by the script, not by the page, on purpose (see `PROJECT_STATUS.md`, Checkpoint 35).
- `python tools/netsheet-test.py` (extended at Checkpoints 36 and 42) checks the seller net sheet in a real browser against an independent calculation, to the dollar: four fixed cases and 150 random ones for the two "You keep" totals and the break-even line; the proof that typing the break-even in as the cash offer makes the two totals equal (and $600 either side flips the answer by $600); the "Print my numbers" button; and a real PDF of the printed page on Letter and A4 (one page, the right content, nothing else from the page, dark text on white); the "Worth a second look" note for numbers that look like typos (it shows for the right cases, stays quiet for ordinary ones, waits while typing, never changes a number, and prints with the sheet); and the order of the answer, buttons and sheets on phones, tablets and wide screens. It needs Playwright with Chromium and `pdftotext` (poppler). Run it after any change to `calc()` in `js/site.js`, the net sheet markup or the print rules.
- `python tools/notfound-test.py` (Checkpoint 36) serves the folder the way GitHub Pages does (a missing address anywhere under the site folder gets status 404 and the body of `404.html`) and checks the friendly page at shallow and deep addresses: status, title, `noindex`, styles, fonts, logo and icons load, every link works, no sideways scroll at 320 to 1440 px, "Go to the home page" really goes home.
- `python tools/nobreak-test.py` (Checkpoint 36) keeps the phone number and "short-term" in one piece on every page, at nine widths and three text sizes, and fails if one of them ever sits next to loose text in a flex or grid parent (where it would turn into a separate cell).
- `tools/_site.py` is imported by the audit tools for one reason: the 404 page's links start with the site folder (`/GLP-Home-Options/css/site.css`), and this makes their small local servers understand that. Nothing to run.
- `python tools/check-links.py` finds broken links, missing images and duplicate ids across all pages. It's instant and needs nothing installed.
- `python tools/a11y-check.py` scans every page at desktop, tablet and phone sizes and reports accessibility problems, broken images, sideways scrolling and small tap targets. Setup is at the top of that file (it needs `axe-core` installed next to where you run it). The goal is 0 problems.

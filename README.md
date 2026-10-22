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
- `research/`: source photos and older notes (not loaded by the site, but this repository is public, so everything in it can be seen)

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

To publish a change in VS Code: **Source Control** (left bar), stage all changes (the **+** next to "Changes"), type a short message, **Commit**, then **Sync Changes**.

## Checking your work

- `python tools/checkpoint.py` compares the project with the last saved checkpoint (`CHECKPOINT.json`), confirms a fresh build reproduces the saved pages, and runs the link check. Run it at the **start** of a session (it should say "clean"). At the **end**, once everything passes, run `python tools/checkpoint.py --write "short label"`.
- `python tools/check-links.py` finds broken links, missing images and duplicate ids across all pages. It's instant and needs nothing installed.
- `python tools/a11y-check.py` scans every page at desktop, tablet and phone sizes and reports accessibility problems, broken images, sideways scrolling and small tap targets. Setup is at the top of that file (it needs `axe-core` installed next to where you run it). The goal is 0 problems.

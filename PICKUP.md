# Pick-up notes: GLP Home Options site

_Updated Oct 21, 2026, about 1:30 AM Central. End of the big redesign session. Read this first when you come back._

**Why this site matters:** it's Joey's livelihood and his family's. Jeremy wants it classy, enterprise-level, and good enough to "sell to a million-dollar investor." Accuracy and trust beat flash. **Never invent** reviews, licenses, years in business, awards, or numbers. If we don't have it, we leave it out or ask Joey.

**Working with Jeremy:** he checks in now and then; send a one-line status when nudged. He publishes through VS Code (Source Control: stage all, write a message, Commit, then **Sync Changes**), not the terminal. Keep final messages short and plain.

---

## Tomorrow's plan (in order)

1. **Look at the live site together.** Jeremy syncs from VS Code, opens https://jsglisson3.github.io/GLP-Home-Options/ on his phone and desktop, and tells us what feels off. Fix that first.
2. **Get answers and real photos from Joey** (see "Ask Joey"). The two biggest trust upgrades: original photos from his phone, and a real photo of the two of them. Swap them in (hero, About, galleries). Replace `images/kitchen-table.jpg`, which looks AI-generated.
3. **Fix the contact form inside GoHighLevel** (see "GHL form checklist"): placeholder consent text, example.com links, styling.
4. **Build the next pages** (see "Roadmap"). Suggested order: Options (selling directly, listing, seller financing / lease options, keeping the home), About (Joey & Ethan), New construction, Contact, then situation pages and city pages. Re-read the old site's Options and About pages for Joey's own wording first: https://glphomeoptions.com/options and /about.
5. **Launch checklist** when Joey approves (see "Before launch").

**Source of truth:** the git folder on Jeremy's computer, `C:\Users\jsgli\Documents\GLP-Home-Options\`, synced to GitHub. The cloud workspace copy may be gone next session. At the start, list that folder with `device_list_dir` and stage what you need with `device_stage_files` (max 50 files per call; start with `index.html`, `css/site.css`, `js/site.js`, the two legal pages, `tools/*`, `PICKUP.md`; pull images only as needed). To write back: stage into `/mnt/user-data/outputs/...` in one call, then `device_commit_files` in a **later separate** call, then verify with `device_list_dir`. (Batching the stage and the commit in one step wrote stale files once.)

---

## Where it stands

- **Status:** working draft, redesigned tonight. Still `noindex` (search engines skip it). Not ready to replace glphomeoptions.com yet.
- **Pages:** `index.html` (the landing page), `privacy-policy.html`, `terms-of-service.html`.
- **Hosting:** GitHub Pages from `github.com/jsglisson3/GLP-Home-Options`, branch `main`, root. Same setup as the FOTCL site. `.nojekyll` is included. GitHub Pages also serves `privacy-policy.html` at `/privacy-policy` and `terms-of-service.html` at `/terms-of-service`, the same paths as the old site. That matters for the text-message carrier registration, which likely points at those URLs.
- **Tests (last run tonight):** axe-core, WCAG 2.2 AA + best-practice rules, **0 violations** on all 3 pages at desktop 1440, tablet 820, phone 390, and phone with reduced motion; also with the phone menu open and a picker option pressed. No broken images, no sideways scrolling. Text on gradients and photos (which axe can't judge) was measured separately: every item meets 4.5:1 (3:1 for large text).

## Why it was black, and what changed

The first version used my own near-black "night navy" bands plus gold. **None of that came from the logo.** The logo is a mid navy (#2d4855) with a green (#3c7a66) house and white. Tonight's redesign:

- Light, airy surfaces (white and a faint mint) with the logo's navy and green as accents; a navy→green gradient for key moments. `color-scheme: light` (dark mode removed on purpose; revisit later if wanted).
- Type: Plus Jakarta Sans (body and headings) and Fraunces italic for the green emphasis phrases ("Clear next steps."). Both self-hosted in `fonts/`, preloaded, no third-party requests.
- A **gable frame** (the roofline from the logo) around the hero and "how it works" photos. It's an inline SVG `clipPath` named `gable`, layered as `.g1` gradient ring, `.g2` white, `.g3` photo.
- Chattanooga homage: faint topographic contour lines, a ridge silhouette in the hero, and a full-width riverfront band ("We live and work in Chattanooga").
- It "feels alive" through motion, all switched off under `prefers-reduced-motion`: scroll reveals, headline word-rise, drifting color blobs, a pulsing "live" dot, gently bobbing floating cards, a slow photo "breathe," parallax on the ridge and riverfront band, count-up numbers, a scroll progress bar in the header, and a nav that highlights the current section. With JavaScript off, everything is still visible and usable.
- Mobile: sticky header, full-screen menu, and a Call / Text / Get my options bar that slides in only after the hero buttons scroll away and steps aside while the form is on screen.

## Layout verdict

For now a **single strong landing page is the right layout**: one story, one main action (talk to Joey and Ethan), proof early, every real path laid out. Long term the site should grow into a small multi-page site for trust and search: **Sell / Options / Build / About / Contact**, plus **situation pages** (inherited home, divorce, relocation, needs repairs, financial stress, downsizing) and **city pages** (only towns Joey confirms; ideas: Hixson, Signal Mountain, Ooltewah, East Ridge, Red Bank, Soddy-Daisy, Collegedale). Each page: unique copy from Joey's real experience, one primary action, FAQ, internal links. Add `sitemap.xml` and `robots.txt` at launch.

## File map

| Path | What it is |
|---|---|
| `index.html` | The landing page. Header, footer, mobile bar, icon sprite, two JSON-LD blocks (LocalBusiness, FAQPage). |
| `privacy-policy.html`, `terms-of-service.html` | **Generated** by `tools/make-legal.py` from the header/footer in `index.html`. Edit the wording inside the script and re-run it. |
| `css/site.css` | All styles. Design tokens (colors, radii, shadows) are at the top. |
| `js/site.js` | All behavior (reveals, count-up, menu, scroll-spy, picker, net-sheet math, topo canvas, mobile bar, form-loading note). |
| `images/`, `fonts/` | Photos, logo, favicons, `og-card.jpg` (share picture), self-hosted fonts. `build-lot.jpg` is currently unused. |
| `tools/` | `a11y-check.py` (accessibility + layout test), `make-legal.py`, `make-og.py` + `og-card.html` (builds the 1200x630 share picture). |
| `research/` | Source photos from Facebook and the old site, plus older handoff notes. Not loaded by the site. |

**Technical notes**
- No build step. Every page carries its own header/footer copy. If you change the header/footer in `index.html`, run `python3 tools/make-legal.py` so the legal pages match. When we add more pages, extend that script (or adopt a tiny static generator) rather than copy-pasting.
- **Cache busting:** `css/site.css?v=11` and `js/site.js?v=6` in `index.html`. Bump the number whenever you change those files, then re-run `make-legal.py` (it copies the numbers).
- The FAQ JSON-LD is hand-maintained. It must match the visible FAQ text word for word.
- The net sheet math: list net = price - payoff - commission - closing - repairs - (monthly carry x months); direct net = offer - payoff. Defaults are illustrative. The Terms page says figures are estimates, not offers.
- Local preview: `python3 -m http.server 8765` in the project folder, then http://127.0.0.1:8765/. (Opening the file directly shows harmless font CORS errors in the console.)
- Run the test: from a folder where you ran `npm i axe-core`, `python /path/to/tools/a11y-check.py`. Needs `pip install playwright pillow` and `playwright install chromium`.
- Known quirk: Plus Jakarta Sans at weight 800 leaves a loose period after "options"; fixed in the hero with `.h1 .dot`. Other headings looked fine.

## What we learned about the business (Facebook + the whole old site)

- **GLP Home Options** is operated by **GL Partners LLC** (shown in the footer and JSON-LD `legalName`). Co-founders **Joey and Ethan**. Based in Hixson, TN (PO Box 55). Serves "Chattanooga and the surrounding counties."
- Real paths they offer: buy directly (as-is, they cover closing costs, no commissions, close in about 7-14 days), list with an agent, keep the home (refinance, rent it out), and creative options (seller financing, lease options, and similar). They also **build new homes**.
- Recent story: a September closing, 35 years of deferred maintenance, bought off-market, and they helped the seller find a rental for the next step. Now building: 3 bed / 2 bath on 0.6+ acres, mid-$200s (from his Oct 13 post; update when it sells).
- Voice: "No pressure. Just solutions." Plain English, local, family business.
- The old site has no testimonials, license numbers, awards, or years in business, so the new one shows none.
- The old site's option illustrations looked AI-generated; we did not reuse them (they're in `research/photos/`).
- The old site's Privacy and Terms had 9 and 10 sections; the new pages follow the same structure in plain words (see Before launch about lawyer review).
- His weekly Facebook market posts are labeled "AI content," so we don't copy those stats.

## Benchmark: what the best peers do, and what we took

We looked at Opendoor, Offerpad, and Baymard's published form research. We copy patterns, never wording or visuals: one headline + one main action + a human photo + "takes a minute / info stays private" beside the button; proof stats right under the hero; side-by-side comparison vs the traditional route; answering "is this legit?" head-on; the main action repeated down the page; city pages in the footer; mark optional vs required fields, labels above fields, few fields, mobile-friendly inputs. Still to copy once real: reviews/ratings, licensing and Equal Housing notices.

## Ask Joey

1. **Phone number:** (423) 451-5707 (site and Facebook header) or 423-401-6779 (older Facebook posts)? The site uses the first everywhere. A search-and-replace on `4234515707` and `451-5707` handles a change (also in JSON-LD and the OG card text if it ever gets a number).
2. **Is the bridge photo a real photo of the two of them?** It looks very polished. A genuine photo is the biggest trust upgrade; if it's AI-generated, replace it.
3. OK to use the closing-day photo and the September story? (Seller privacy and consent.)
4. OK to use words from his Facebook posts ("No pressure. Just solutions." etc.)?
5. Which towns and counties do they actually serve? (For city pages.)
6. Does he hold a TN real estate license or work with a broker? (Needed for any license line and Equal Housing notice.)
7. Is the new build still unsold? Update or remove "Now building" when it sells.
8. **Send the original photos from his phone** (builds, closings, the team, neighborhoods). Everything we have is about 800px, saved from Facebook or the old site.
9. Rights to the Chattanooga riverfront photo (only 900px wide, so it looks soft when wide).
10. Anything he wants said or not said in the "what happens next" steps.

## GHL (GoHighLevel) form checklist

The form is an iframe from `links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ`; booking is `.../widget/booking/cM59fR3vJlAVRy08Depz`. Its look can only be changed inside GoHighLevel (Form Builder, then Style). Recommended: primary color **#3c7a66**, font **Plus Jakarta Sans**, corner radius about 12px, button text **"Get my options"**, labels above fields, mark optional fields "(optional)", one column on phones, keep it to name, phone, property address (the rest optional). **Fix before launch:** the consent text still contains `[BUSINESS NAME]` and `[USE_CASE_FROM_CAMPAIGN_DESCRIPTION]`, and its Privacy/Terms links point to example.com. Replace with GLP Home Options / GL Partners LLC wording that matches the registered text-message campaign, linking to `/privacy-policy` and `/terms-of-service`.

## Before launch (don't skip)

- Remove `<meta name="robots" content="noindex, nofollow">` from all three pages; un-comment the canonical link in `index.html` and set the real domain; switch the `og:url`/`og:image` addresses from the github.io address to the real domain.
- Fix the GHL consent text and links (above).
- **Have a lawyer review the Privacy Policy and Terms.** They're a plain-words rewrite of Joey's old pages, not legal advice. Remove the "Draft for review" note from both (it's marked `REMOVE THIS NOTE AT LAUNCH` in `tools/make-legal.py`). Confirm the "we respect Do Not Track" line is still true if analytics gets added. Carriers usually also want message frequency and HELP wording; confirm with GHL what the registered campaign says.
- Get 3+ real reviews (Google Business Profile, Facebook) after closings and add them (first name + neighborhood + quote). Never invent.
- Point glphomeoptions.com at the new site (GitHub Pages custom domain + DNS) once Joey approves; keep `/privacy-policy` and `/terms-of-service` working.
- Add `sitemap.xml`, `robots.txt`, analytics, and form-conversion tracking.
- Replace placeholder-quality photos (see Ask Joey).

## Roadmap after the landing page

1. Real founders photo + a short "why we started" in Joey's voice.
2. Options, About, New construction, Contact pages; then situation pages and city pages.
3. Sharper hero image once we have originals (srcset, WebP/AVIF), and a real SVG logo (we only have a ~200px original; `images/glp-mark.png` is a cleaned copy).
4. Reviews strip once real; "market snapshot" only with sourced numbers.
5. A short first step on the form (name, phone, address), inside GHL.
6. Performance pass (Lighthouse) after real photos are in.

## Session log

- **Oct 21, ~00:00-01:30 (redesign):** read his Facebook and every old-site page; rebuilt `index.html` with shared `css/site.css` and `js/site.js`; light logo-colored design system; motion and mobile pass; subgrid-aligned cards; fixed an 8px sideways overflow on phones (the rotated photo "plate"); added `main{overflow-x:clip}` as a safety net; mobile action bar now appears after the hero buttons; contrast fixes (`--muted` darkened to #4a626d, stronger overlays on the riverfront band and contact band); added Privacy/Terms pages, `og-card.jpg`, favicons, new test tool; removed an unused font. Not done tonight: tablet and reduced-motion screenshots were checked by the automated scan only, not by eye; the real GHL iframe was not loaded in a browser (blocked offline), so check the form card on the live site.
- Earlier sessions: navy+gold single-file version, Facebook/old-site research, benchmark notes, first publish to GitHub Pages.

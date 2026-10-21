# Pick-up notes: GLP Home Options site

_Updated Oct 21, 2026, about 8:35 AM Central. Read this first when you come back._

**Why this site matters:** it's Joey's livelihood and his family's. Jeremy wants it classy, enterprise-level, and good enough to "sell to a million-dollar investor." Accuracy and trust beat flash. **Never invent** reviews, licenses, years in business, awards, or numbers. If we don't have it, we leave it out or ask Joey.

**Working with Jeremy:** he checks in now and then; send a one-line status when nudged. He publishes through VS Code (Source Control: stage all, write a message, Commit, then **Sync Changes**), not the terminal. Keep final messages short and plain.

**Heads-up from Jeremy (Oct 21, 8:11 AM):** he will probably build a **separate site for Joey's construction business**. This site stays about **home buying / selling options**. So the New homes page is deliberately one light teaser page, and the link to it lives in a single constant (`NEW_HOMES` at the top of `tools/build-pages.py`). When the construction site exists, point that constant at it (header, footer, menu and every "Now building" link follow), or keep our page as a short bridge.

---

## Where things stand (read this part twice)

- **Live on GitHub Pages right now:** the overnight single-landing-page version (git commit `ad04d66`).
- **Saved in Jeremy's folder but NOT published yet:** the multi-page version built this morning. To publish: VS Code, Source Control, stage all (+), message, Commit, **Sync Changes**. About a minute later it's live at https://jsglisson3.github.io/GLP-Home-Options/.
- **First thing next session:** have Jeremy publish, then open the live site on his phone and desktop and tell us what feels off. Fix that before anything new. Things that can only be checked live: the GoHighLevel form (home page and Contact page), the Facebook links, the phone menu on a real phone.
- Still `noindex` (search engines skip it). Not ready to replace glphomeoptions.com until Joey answers the list below.

## Pages (all generated; see "How the site is built")

| Page | Job | Story arc | One action |
|---|---|---|---|
| `index.html` | The landing page. Hero, proof stats, three paths, the September closing story, how it works, compare table + net sheet, riverfront band, about, now building, FAQ, contact form. Now links out to the deeper pages. | Problem, options, proof, numbers, people, action | Talk to Joey or Ethan |
| `options.html` | **Your options.** Sell direct, list, keep the home, creative solutions. Each has how it works, what it costs, "a good fit if" and an honest "maybe not if." Fit picker, example net sheet, 6-question FAQ. | What are my choices? What does each cost me? Which fits? | Get my options |
| `about.html` | **Our story.** Real headshots first, why we do this (2 answers vs 4), what we stand for, the September closing as a 4-step case, riverfront band, we build too, "Is GLP legit? Check us out" (call, Facebook, bring your own attorney). | Who are these guys, and can I trust them? | Talk to Joey or Ethan |
| `new-homes.html` | **New homes.** Light teaser: gable-framed photo, spec card (3 bed, 2 bath, 0.6+ acres, mid $200s), job-site gallery, who it's for, 6-question FAQ. | What are they building? Is it for me? | Ask about this home |
| `contact.html` | **Contact.** H1 hero with call/text/email/book/Facebook tiles, "what happens next," the form, find us, 3 quick answers, "not ready to talk? explore." | Easiest possible way to reach a human | Send details / call |
| `privacy-policy.html`, `terms-of-service.html` | Plain-words legal pages (draft, not lawyer-reviewed). Same URLs as the old site (`/privacy-policy`, `/terms-of-service`). | | |

Every inner page ends with a call-to-action band (Send us a few details, Call or text) so there is always a next step. Header: Your options, The numbers, Our story, New homes, Contact (last, per the credibility research), plus the Facebook logo, phone number and a "Get my options" button.

## Facebook logo (Jeremy asked twice, so don't lose these)

URL: `https://www.facebook.com/profile.php?id=61588492362641` (one constant, `FB`, in `tools/build-pages.py`). The logo is a real blue-circle "f" drawn as the `i-fb-logo` symbol in `tools/pages/_sprite.html`, so it reads as Facebook on any background. Placements: **header** (round logo button, desktop 1161px and up), **phone menu** ("Follow us on Facebook" row), **footer** (button on every page), **About** ("See our work" card), **Contact page** (reach tile and "See our work" card), **home contact section** (reach tile), **New homes** (text link under the gallery), the FAQ answer to "How do I know GLP is legit?", and the `sameAs` in the structured data.

## How the site is built

GitHub Pages serves plain files, but the header, footer, icon sprite, FAQ and contact block repeat on every page. So there is one small builder and the output is still plain HTML:

```
python3 tools/build-pages.py     # rewrites all 7 pages
python3 tools/check-links.py     # every link, anchor, image, script resolves; no duplicate ids
```

- `tools/pages/<page>.html`: the `<main>` content of index, options, about, new-homes, contact. **Edit these, not the root `.html` files** (those are overwritten). Tokens inside them: `[[herobg]] [[crumbs]] [[fb-button]] [[contact-href]] [[home]] [[new-homes-href]] [[fb]] [[faq <set>]] [[cta <set>]] [[contact home]] [[contact page]]`.
- `tools/pages/_sprite.html`: icons and the gable clip-path.
- `tools/legal_text.py`: wording of Privacy and Terms (the "Draft for review" note is marked `REMOVE THIS NOTE AT LAUNCH`).
- `tools/build-pages.py`: header, footer, mobile bar, FAQ text, page titles and descriptions, structured data, site facts (phone, email, Facebook, booking and form IDs). **The FAQ lives here once and feeds both the visible list and the FAQPage structured data**, so they can't drift.
- `tools/make-legal.py` is now just a shim that runs the builder.
- Bump `CSS_V` / `JS_V` in the builder whenever you change `css/site.css` or `js/site.js` (cache busting), then rebuild. Currently `?v=18` and `?v=7`.
- Commit the generated root `.html` files; that is what GitHub Pages serves.
- **Harmless quirk:** when Claude saves a file to your computer, the transfer stamps an invisible "Content Credentials" (provenance) tag on images (about 6 KB each, ignored by browsers) and on the SVG sprite. For the sprite it shows up as a `<metadata>` block, so `clean_sprite()` in the builder strips it out when building pages. Don't be surprised if image files on the device are a few KB bigger than the ones in the cloud workspace.

Design system, accessibility testing, local preview and the net-sheet math are unchanged from the overnight notes: light only; navy `#2d4855` + green `#3c7a66` from the logo; Plus Jakarta Sans + Fraunces italic (self-hosted); gable photo frame; everything animated switches off under reduced motion and the site works with JavaScript off (the fit picker only shows when JavaScript is on). Local preview: `python3 -m http.server 8765` in the project folder. Accessibility run: from a folder where `npm i axe-core` was done, `python /path/to/tools/a11y-check.py` (now covers all 7 pages by default).

Changes this morning worth knowing: the desktop nav now collapses to the phone menu at 1160px and below (it needed the room for the Facebook logo); the phone number pill in the header shows from 1360px up; `@view-transition` gives a soft fade between pages in browsers that support it; the home path cards now link to the matching spot on the Options page.

## Benchmarks applied (compare to the best, copy patterns not wording)

- **CXL credibility checklist:** real staff photos with names and roles (About hero), address and phone in header and footer, Contact link last in the nav, no dead links (checker), plain language, specific facts over superlatives, show the numbers (compare table, net sheet, "what it costs you" on every option), transparent policies (legal pages linked everywhere), testimonials **only if real** (none exist, none shown), fast pages, don't overload credibility badges.
- **Baymard:** permanent labels above fields, not placeholder-as-label (applies to the GHL form; see below).
- **Google people-first content:** first-hand experience (the September closing, the job-site photos), original value (net sheet), clear titles, About linked from every page.
- **Opendoor / Offerpad patterns:** one headline and one main action, human photo, proof under the hero, side-by-side comparison, "is this legit?" answered head-on, main action repeated down the page. We added the honest "maybe not if" lists, which the big players avoid and which build trust.

## Ask Joey (one list, send it to him)

1. **Phone number:** (423) 451-5707 (site and Facebook header) or 423-401-6779 (older Facebook posts)? The site uses the first. One change in `tools/build-pages.py` plus the legal text handles it.
2. **Is the bridge photo a real photo of the two of them?** It looks very polished. A genuine photo is the biggest trust upgrade; if it's AI-generated, replace it. Same for `kitchen-table.jpg`.
3. **OK to use the closing-day photo and the September story?** (Seller privacy and consent.) Also: the "Just Closed" key in that photo shows a title company's branding (Key Title & Escrow, 423-206-2226) and a second small logo. Fine to show?
4. **OK to use words from his Facebook posts** ("No pressure. Just solutions." etc.)?
5. **His own words for the About page:** why they started, how long they've been doing this, what each of them handles, a line each. Today the story is built only from what's public. (No invented backgrounds.)
6. **Which towns and counties** do they actually serve? (City pages, and the "surrounding counties" line.)
7. **Does he hold a TN real estate license or work with a broker?** (Needed for any license line and the Equal Housing notice. Also decides how we describe "list with an agent.")
8. **The new build:** still unsold? Price still mid $200s? Is down payment assistance real and what should we say? Update or remove when it sells. (And whether the construction site is coming; see the heads-up above.)
9. **Original photos from his phone** (builds, closings, the team, neighborhoods). Everything we have is about 800px, saved from Facebook or the old site.
10. Rights to the Chattanooga riverfront photo (only 900px wide, soft when wide).
11. Anything he wants said or not said in "what happens next."
12. Real reviews: after a closing, ask the seller for a Google review. We add 3+ with first name and neighborhood. Never invent.

## GHL (GoHighLevel) form checklist

The form is an iframe from `links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ`; booking is `.../widget/booking/cM59fR3vJlAVRy08Depz`. It's on the home page and the Contact page. Its look can only be changed inside GoHighLevel (Form Builder, then Style). Recommended: primary color **#3c7a66**, font **Plus Jakarta Sans**, corner radius about 12px, button text **"Get my options"**, labels above fields, mark optional fields "(optional)", one column on phones, keep it to name, phone, property address (the rest optional). **Fix before launch:** the consent text still contains `[BUSINESS NAME]` and `[USE_CASE_FROM_CAMPAIGN_DESCRIPTION]`, and its Privacy/Terms links point to example.com. Replace with GLP Home Options / GL Partners LLC wording that matches the registered text-message campaign, linking to `/privacy-policy` and `/terms-of-service`. Also confirm the form's thank-you behavior and where leads go.

## Before launch (don't skip)

- Remove `<meta name="robots" content="noindex, nofollow">` (it's in `head()` in the builder, one place); un-comment the canonical line there and set the real domain; switch `SITE` (og:url / og:image) from the github.io address to the real domain.
- Fix the GHL consent text and links (above).
- **Have a lawyer review the Privacy Policy and Terms.** They're a plain-words rewrite of Joey's old pages, not legal advice. Remove the "Draft for review" note. Confirm "we respect Do Not Track" stays true if analytics gets added. Carriers usually also want message frequency and HELP wording.
- Get 3+ real reviews and add them. Never invent.
- Point glphomeoptions.com at the new site (GitHub Pages custom domain + DNS) once Joey approves; keep `/privacy-policy` and `/terms-of-service` working.
- Add `sitemap.xml`, `robots.txt`, analytics, and form-conversion tracking.
- Replace placeholder-quality photos (see Ask Joey).

## Roadmap (suggested order)

1. Publish this version and look at it live together; fix what feels off.
2. Get Joey's answers and original photos; swap them in (hero, About, galleries); write the About page in his voice.
3. Fix the GHL form and consent text.
4. **Situation pages** (inherited home, divorce, relocation, needs repairs, financial stress, downsizing), each with unique copy from Joey's real experience, one action, FAQ and links back to Options. Then **city pages** (only towns Joey confirms; ideas: Hixson, Signal Mountain, Ooltewah, East Ridge, Red Bank, Soddy-Daisy, Collegedale).
5. Real reviews strip; a market snapshot only with sourced numbers; a real SVG logo (we only have a ~200px original); sharper hero image (srcset, WebP/AVIF) once we have originals; a performance pass (Lighthouse).
6. Decide with Jeremy how the construction site and this one link to each other.

## What we learned about the business (Facebook + the whole old site)

- **GLP Home Options** is operated by **GL Partners LLC** (footer and structured data). Co-founders **Joey and Ethan**. Based in Hixson, TN (PO Box 55). Serves "Chattanooga and the surrounding counties."
- Real paths: buy directly (as-is, they cover closing costs, no commissions, close in about 7-14 days), list with an agent, keep the home (refinance, rent it out), creative options (seller financing, lease options). They also **build new homes**.
- Recent story: a September closing, 35 years of deferred maintenance, bought off-market, and they helped the seller find a rental. Now building: 3 bed / 2 bath on 0.6+ acres, mid-$200s (his Oct 13 post).
- Voice: "No pressure. Just solutions." Plain English, local, family business.
- The old site has no testimonials, license numbers, awards, or years in business, so the new one shows none.
- The old site's option illustrations looked AI-generated; we did not reuse them (they're in `research/photos/`). His weekly Facebook market posts are labeled "AI content," so we don't copy those stats.
- Old Privacy and Terms had 9 and 10 sections; the new pages follow the same structure in plain words.

## Source of truth and how to save

The git folder on Jeremy's computer, `C:\Users\jsgli\Documents\GLP-Home-Options\`, synced to GitHub. The cloud workspace copy may be gone next session. At the start, list that folder with `device_list_dir` and stage what you need with `device_stage_files` (max 50 files per call; start with `index.html`, `css/site.css`, `js/site.js`, `tools/*`, `tools/pages/*`, `PICKUP.md`; pull images only as needed). To write back: stage into `/mnt/user-data/outputs/...` in one call, then `device_commit_files` in a **later separate** call, then verify with `device_list_dir`. (Batching the stage and the commit in one step wrote stale files once.)

## Session log

- **Oct 21, ~7:54-8:35 AM (multi-page):** read the live state; researched the best peers (CXL credibility checklist, Baymard, people-first SEO); built the one-source page builder and the Options, Our story, New homes and Contact pages; added the Facebook logo in the header, phone menu, footer, About, Contact and home contact; widened the header breakpoint; fixed a few layout bugs found in screenshots (step-number circles, spec card overflow, caption collision on phones); link check clean (7 pages, 339 links, no duplicate ids); accessibility scan (axe) shows **0 problems on all 7 pages** at desktop, tablet, phone and phone with reduced motion, plus the phone menu open and the fit picker pressed; every text color on the four new pages passes contrast (4.5:1 body, 3:1 large). Last-minute catches: a heading-order flag on Contact (fixed) and a heading that went invisible in the Contact form card because of that fix (also fixed, and re-checked). Not done: the GHL form can't load offline, so it has not been seen working; real photos and Joey's answers still pending.
- **Oct 21, ~00:00-01:30 (redesign):** rebuilt `index.html` with shared CSS/JS; light logo-colored design system; motion and mobile pass; Privacy/Terms pages; share picture; favicons; test tool.
- Earlier sessions: navy+gold single-file version, Facebook/old-site research, first publish to GitHub Pages.

# Pick-up notes — GLP Home Options site

_Updated Oct 21, 2026. Goal from Jeremy: a classy, enterprise-level site that blows Joey away. It's his family's livelihood, so accuracy and trust come first._

## Where it stands
`index.html` is the working draft: single page, no build step, images in `images/`. It no longer has the "Preview draft" banner or "To add" boxes. It is **not ready to replace glphomeoptions.com yet** (see "Before launch").

**This session built:**
- Hero v2: Joey & Ethan photo above the fold, tap-to-call card, one primary action, reassurance microcopy, proof strip (7–14 days / $0 commission / every option / local team), two "latest from the team" links.
- **Recent story** section (Sept closing: 35 years of deferred maintenance, bought off-market, rental found for the next move) with the real closing-day photo.
- **Now building** section (3 bed / 2 bath, 0.6+ acres, mid-$200s; driveway pour, kitchen cabinets, exterior).
- Trail map moved into the "Three paths" section; comparison table stacks into cards on phones.
- Palette backed off the green: night navy + gold, green only on check marks and the logo.
- Real contact block: call, text, email, booking link, GoHighLevel form embedded, plus a "form not loading?" fallback.
- Mobile: sticky Call / Text / Get my options bar, full-screen menu, 44px+ tap targets, safe-area aware.
- Accessibility: skip link, real table semantics, keyboard-focusable regions, dark mode, reduced motion. Automated axe-core scan = **0 violations** on phone + desktop, light + dark.
- SEO: title/description, Open Graph, LocalBusiness + FAQ JSON-LD, icons. **`noindex` is ON** (see Before launch).
- Riverfront photo: removed the corner caption that read like a watermark. The image file itself has no text baked in.

## Benchmark: what the best peers do, and what we took
Looked at Opendoor and Offerpad (the category leaders) and Baymard's form research. We copy *patterns*, never their wording or visuals.

| Pattern from the best | Where we are |
|---|---|
| Opendoor: one headline, one main action, a human photo, and "takes 5 minutes / info stays private" next to the button | Done in the hero (faces + microcopy) |
| Opendoor: proof stats directly under the hero | Done, using only claims Joey's own site already makes |
| Opendoor/Offerpad: side-by-side vs the traditional route (timeline, fees) | Done (comparison table + net sheet) |
| Offerpad: answers "Is X legit?" head-on | Added FAQ "How do I know GLP is legit?" |
| Offerpad: repeats the main CTA through the page; city pages in the footer | CTA repeated; city pages are a next step |
| Offerpad/Opendoor: real licensing + Equal Housing notices in the footer | **Ask Joey** whether/where that applies before adding |
| Both: reviews/press/ratings | None exist yet. We don't fake it. See next steps |
| Baymard: mark required vs optional clearly, labels above fields, few fields, mobile-friendly inputs | The form lives inside GoHighLevel, so these changes happen there (see next steps) |

Sources: offerpad.com, opendoor.com, baymard.com (guideline 686 "indicating required and optional fields"; free articles on mobile form usability). Baymard's detailed guideline text is paywalled; we applied its published principles, not its premium content.

## Confirmed facts
Phone (423) 451-5707 · info@glphomeoptions.com · PO Box 55, Hixson, TN · "Chattanooga and the surrounding counties" · Facebook page ID 61588492362641 · GHL form `links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ` · GHL booking `links.voiseai.com/widget/booking/cM59fR3vJlAVRy08Depz`. The existing site has **no** testimonials, license numbers, awards, or years in business, so we show none.

## Ask Joey
1. Which phone number: (423) 451-5707 (site + FB header) or 423-401-6779 (older FB posts)?
2. Is the bridge photo a real photo of the two of them? It has a very polished look. A genuine photo is the biggest single trust upgrade; if it's AI-generated we should replace it.
3. OK to use the closing-day photo and the Sept story on the site? Seller privacy/consent.
4. OK to use words from his Facebook posts ("No pressure. Just solutions." etc.)?
5. Towns/counties served, for local SEO pages.
6. Does he hold a TN real estate license / work with a broker? (Equal Housing notice, license line.)
7. Is the new build still unsold? Update/remove "Now building" when it sells. Price/specs are from his Oct 13 post.
8. Rights to the Chattanooga riverfront photo (only 900px wide, so it also looks soft when wide).

## Before launch (don't skip)
- Remove the `noindex` meta tag in `index.html` (it's marked DRAFT) and add a canonical URL.
- Fix the GoHighLevel consent text that still says `[BUSINESS NAME]` / example.com. Needed for text-message compliance.
- Add real Privacy Policy + Terms pages (the old site had them). A lawyer should review.
- Get 3+ real reviews (Google Business Profile + Facebook) after closings; add them to the page. Template idea: first name + neighborhood + quote. Never invent.
- Point glphomeoptions.com at the new site (or paste the page into GHL hosting) once Joey approves.

## Next steps (priority order)
1. Real founders photo + a short "why we started" in Joey's voice (the old About page has none).
2. Hero upgrade with a higher-res Chattanooga skyline/riverfront image and a real SVG logo (only a 200px logo exists).
3. Separate pages for SEO and trust: Sell an inherited house, Sell a house that needs repairs, Divorce, Relocation, Seller financing & lease options, New construction, Hixson / Signal Mountain / Ooltewah / East Chattanooga.
4. Move the contact form to a short first step (name, phone, address) inside GHL; mark optional fields as optional; labels above fields; one column on mobile.
5. Reviews strip + Google rating once real.
6. "Market snapshot" only with sourced numbers (his FB weekly posts are flagged "AI content", so we don't copy those stats).
7. Analytics + form-conversion tracking.

## Technical notes
- Palette tokens live at the top of `index.html` (`--river` navy, `--blaze` gold, `--band` dark band). Dark bands stay dark in dark mode via a scoped override near the end of the CSS.
- Accessibility/phone check: `tools/a11y-check.py` (Playwright + axe-core; setup steps are at the top of the file). Re-run after big changes. Last result: 0 violations, phone + desktop, light + dark.
- Source photos are in `research/photos/` (not loaded by the page).

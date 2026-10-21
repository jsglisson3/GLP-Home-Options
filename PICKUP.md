# Pick-up notes — GLP Home Options site

_Last session: Oct 21, 2026. Goal from Jeremy: make a site that blows Joey away — this is his family's livelihood._

## Where it stands

- `index.html` = the previous session's build (trail-map design: pine/river green + blaze gold, contour background, three-path chooser, net-sheet calculator, FAQ, contact form). Still a **preview draft**: ribbon on, "To add" markers, form shows a preview message instead of sending.
- Live preview from last session: https://claude.ai/artifact/N2xbnPH846e9WDubVH3FCp
- This session was research + photo collection (below). The big upgrade build has **not** been done yet.

## Confirmed business facts

| Item | Value | Source |
|---|---|---|
| Phone | (423) 451-5707 | current site + Facebook page header |
| Email | info@glphomeoptions.com | current site (contact page) |
| Mailing address | PO Box 55, Hixson, TN | Facebook page |
| Facebook | https://www.facebook.com/profile.php?id=61588492362641 (50 followers, 0 reviews) | |
| Lead form (GoHighLevel) | https://links.voiseai.com/widget/form/c36UOOc2pkosxfvRfjZJ | current site |
| Booking calendar | https://links.voiseai.com/widget/booking/cM59fR3vJlAVRy08Depz | current site |
| Service area (their words) | "Chattanooga and the surrounding counties" | Facebook, May 18 post |

**Ask Joey:** older Facebook posts (May–June) list **423-401-6779**; the site and page header list 423-451-5707. Confirm which one goes on the site.

## What Facebook added (their own posts)

- **Intro:** "house buying specialists focused on solutions — not pressure… on-market listing, off-market solutions, or a quick as-is sale."
- **Real story, Sept 18:** helped homeowners with a house that had 35 years of deferred maintenance; bought it completely off-market, worked around their timeline, and helped them find a rental for their next move — "just walk away and that's what they did." Closed with a local title company. Closing-day photo saved (`research/photos/facebook/closing-day-…`). → Use as a "recent story" section. **Confirm the seller is OK with the photo on the website** (it's already on Facebook).
- **They build, too:** new construction in Chattanooga — 3 bed / 2 bath on 0.6+ acres, mid-$200s (Oct 13 post); driveway concrete going in Oct 20 ("finals getting done"). May 15 post says several affordable new builds are coming, priced for the City of Chattanooga down-payment assistance program. → Add a "Now building" section with the construction photos. **Update or remove when that house sells.**
- **Also offer:** seller financing, lease options, creative deal structures, free property value consultations (May 18 / June 25 posts).
- Facebook cover photo (staged white living room) is unknown provenance — not used.

## Photos collected (`research/photos/`)

- `from-old-build/` — Joey & Ethan on the Walnut Street Bridge, both headshots, kitchen-table photo, house mark.
- `current-site/` — the three option images from glphomeoptions.com (sell direct, list with agent, keep the home). These look like stock/AI images — use lightly.
- `facebook/` — new-build exterior, lot + excavator, driveway pour, concrete truck, kitchen in progress, closing day (all real, 800px).
- `chattanooga-riverfront-pano-900x225.jpg` — Jeremy's aquarium/riverfront shot (only 900px wide; needs upscaling or a smaller placement for a hero). **Confirm we have rights to use it** if it isn't Jeremy's own photo.
- `glp-logo-original-200px.jpg` — only 200px exists anywhere; plan is to redraw the house mark as SVG.

## Next steps (in order)

1. **Upgrade build:** cinematic Chattanooga hero with Joey & Ethan + call/text CTAs; path cards with photos; "Recent story" (Sept 18 deal + closing photo); "Now building" section with the new-construction photos; keep net-sheet calculator, comparison table, how-it-works, about, FAQ (+ FAQ schema); contact with call / text / email / booking link; sticky mobile call bar.
2. **Remove the preview ribbon + "To add" markers** — replace review placeholders with their promises (no invented reviews, licenses, years, or awards).
3. **Wire the form for the hosted site:** embed the GoHighLevel form (iframe works on a real domain) so leads land in Joey's CRM. Fix "[BUSINESS NAME]" / example.com text in the GHL form's consent settings.
4. SEO: meta/Open Graph, LocalBusiness JSON-LD, SVG logo + favicon.
5. Test on phone + desktop, light + dark, then push → GitHub Pages updates.
6. Later: point glphomeoptions.com at the new site (or keep GHL hosting and paste the page in) once Joey approves.

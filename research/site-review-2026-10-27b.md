# Checkpoint 48 review: tighter desktop, the net sheet and a premium pass (Oct 27, 2026)

Jeremy asked on Oct 26 at about 11:20 PM Chattanooga time. He wanted three things. First, cut the extra white space and "shrink it up a little bit" on desktop. Second, use the new skills harder ("i dont feel like you did a ton with your new skills"). Third, make the numbers section "more attractive i want to wow people". The standard is his brief, "Transform This Website Into an Exceptional, Premium Digital Experience". Its full text is in the project chat; it is not in this repo. I built this overnight in the cloud while his computer was off.

Where the brief and the project rules disagree, the project rules win:
- no new claims;
- the net sheet keeps its numbers, method and name;
- no form is typed into or sent;
- `noindex` stays.

**How to read this report.** Each fact is labelled:
- **measured:** taken from a real browser (Chromium, through Playwright);
- **tested:** an automated check passed;
- **calculated:** worked out from hex values or file sizes;
- **judgement:** my opinion, not measured.

## How the skills were used

- **design-taste-frontend** (Jeremy installed it for this).
  - **Its inspector.** It checks a page in a browser at 1440, 768 and 390 px. I ran it on six pages: before, then four rounds, fixing after each round (the last after the phone headlines went in).
  - **Its house rules** drove most of the changes:
    - no small labels above headings;
    - no shadows on things at rest;
    - no 1 px outlines or hairline dividers;
    - no decorative gradients;
    - headlines in two lines or fewer;
    - nothing meant to be read under 13 px.
  - **Its "direction" draw** (a new palette, typefaces and layout) was not used to restyle the site. The colours, the two typefaces and the people-led hero are approved and locked (D1 to D4), so I applied its rules inside them.
- **frontend-design** (Anthropic): spend boldness in one place and keep the rest quiet. Here that place is the net sheet.
- **ui-ux-pro-max** (used in Checkpoint 47). The spacing audit searched it for section spacing and vertical rhythm and found no guidance that fit, so nothing in this pass rests on it.
- **Three independent audits.** Fresh reviewers, who had not seen my reasoning, measured the pages in a browser and proposed exact values:
  - spacing on Home;
  - spacing on the other pages;
  - typography on all nine pages.

  Their 21 main findings (10 High, 9 Medium, 2 Polish) were to be re-checked by a skeptic each, but those checks recorded no verdict. So I applied the proposals and measured the results myself.
- **What stopped at the usage limit and was not rerun:**
  - three more audits: components, art direction, and responsive layout with accessibility;
  - a planned panel of three competing net sheet designs, each to be scored by judges.

  I designed and built the net sheet directly from one idea (section 2) and checked it with the inspector and the tests. The inspector and the test suite cover much of the missing audits' ground, but no independent reader did.

## 1. Overall assessment

### Before: Checkpoint 47, live

The site was already simple, accessible and honest. On a computer, though, it still read as a template. The inspector counted these on Home alone (**measured**):

| What it found | How many |
|---|---|
| Shadows on things at rest | 29 |
| Gradient fills | 8 |
| Boxes drawn with a 1 px outline | 12 |
| Hairline dividers | 7 |
| Small labels above headings | 8 |
| Headlines of three lines at 1440 px | 4 |
| Text blocks smaller than 13 px | 12 |

The buttons also had a gradient fill and a glow.

There was a lot of empty space. Every section had 112 px above and below it, and every heading had 72 px under it. A laptop screen often showed one heading and a field of cream.

The net sheet's answer is the most important thing on the site, and it was hard to find. It sat in a narrow column beside the form, and the two "You keep" totals were barely bigger than the text around them.

### After: Checkpoint 48

The site is flat and tighter:
- **A card is now a change of tone** (cream on white, or white on cream), not a box with a line and a shadow.
- **Every main page is shorter on a computer** (**measured** at 1440 px):
  - Home: 734 px shorter;
  - Our work: 1,239 px;
  - Our story: 720 px.
- **Headings hold to two lines** from 901 to 2560 px wide on every page (**measured** at 17 widths; before, 15 headings on five pages ran to three or four lines).
- **The net sheet reads top to bottom as one sheet:**
  1. your numbers;
  2. the two results side by side, with "You keep" set large;
  3. the answer in one deep green band.

Phones keep their approved layout and spacing. On phones, the changes are the flatter look, the removed labels and lines, and shorter headlines (Jeremy said yes on the morning of Oct 27): seven are reworded and phone titles are about 17% smaller, so no title runs past two lines from 375 to 520 px (section 3).

### Inspector counts, before → after (measured)

The inspector checks each page at 1440, 768 and 390 px. A FAIL is a must-fix in the skill's rules; a WARN is fix or defend.

| Page | Checkpoint 47 (live) | Checkpoint 48 (final build) |
|---|---|---|
| Home | 12 FAIL, 10 WARN | 3 FAIL, 8 WARN |
| Your options | 11 FAIL, 7 WARN | 4 FAIL, 5 WARN |
| Our story | 11 FAIL, 11 WARN | 1 FAIL, 7 WARN |
| Our work | 8 FAIL, 6 WARN | 2 FAIL, 4 WARN |
| New homes | 10 FAIL, 6 WARN | 1 FAIL, 4 WARN |
| Contact | 12 FAIL, 8 WARN | 4 FAIL, 6 WARN |
| **All six** | **64 FAIL, 48 WARN** | **15 FAIL, 34 WARN** |

### An honest score (judgement)

The skill scores a page like a juror: design 40, usability 30, creativity 20, content 10. On that scale I would put the desktop site at about 7.5 out of 10 now, against about 6 before.

The skill also has hard caps:
- any FAIL left on a page caps it at 6.0;
- a headline of three or more lines at any width caps it at 6.5.

Every page still has at least one FAIL. The 15 that are left:

| How many | What | Why it stays |
|---|---|---|
| 5 | "Still page" | The skill wants every section to move and a moving picture. This project rules out autoplay and keeps motion restrained (D5). |
| 4 | False alarms: "labels above headings" (3) and "icon cards" (1) | See section 7. |
| 2 | Text under the phone call bar while scrolling | That is what a fixed bar does. |
| 2 | Too few pictures (Your options, Contact) | Needs Joey's photos. |
| 1 | The carousel's photos at the screen edge | On purpose, so it looks swipeable. |
| 1 | Small text on Contact | Joey's consent wording. |

Section 7 goes through each one. So by the letter of the skill this is not "done", and I am not claiming it is.

## Findings by priority

| # | Priority | Finding (before) | Status |
|---|---|---|---|
| none | Critical | **None found.** All of these passed before and after (**tested**): links, claims, accessibility (axe, 0 violations), overflow at 11 widths, 200% text, the net sheet's sums and the contact form's behaviour. | |
| H1 | High | **Too much white space on desktop** (Jeremy). Sections had up to 112 px padding, headings up to 72 px under them, and the ridge under the hero was up to 270 px. | **Done.** Now 88, 48 and 200 px at most. Phones are unchanged. |
| H2 | High | **The net sheet had no focal point** (Jeremy: "wow"). The answer sat in a narrow column, the totals were small, and the answer box had a gradient. | **Done.** It is now one sheet with one big result (section 2). No number, default, method or word changed. |
| H3 | High | **Template surfaces:** shadows on things at rest, gradients, glowing buttons, 1 px outlines, hairlines and frosted glass in five places. | **Done.** Surfaces are flat. Shadows stay only on things that float, and frosted glass only on the header. |
| H4 | High | **Headlines of three or four lines on desktop.** 15 headings on five pages ran past two lines somewhere from 901 to 2560 px; at 1440 there were 4 on Home. | **Done.** None runs past two lines on any of the nine pages at 17 widths from 901 to 2560 px (**measured**). |
| H5 | High | **Small labels above headings** (8 on Home). | **Done.** None left. Each was worked into the text, or dropped where the photo badge or the heading already said it (`CONTENT_CLAIMS.md` row 66). |
| M1 | Medium | **Text smaller than 13 px** (12 blocks on Home). | **Done.** Nothing meant to be read is smaller than .82rem (about 13 px). |
| M2 | Medium | **Long lines.** Intro paragraphs ran about 97 characters a line on desktop. | **Done.** About 68 characters now. |
| M3 | Medium | **Home's three paths hid their most useful fact,** how long each takes, in a small pill. | **Done.** On computers the time leads each card, set large. |
| M4 | Medium | **The carousel's heading, sentence and arrows** were stacked in three rows. | **Done.** They share one row on computers, and the arrows are filled circles. |
| M5 | Medium | **Our work left one photo alone** in the last row. | **Done.** No photo sits alone at any width (**measured** at 390 to 1920). |
| M6 | Medium | **Contact page on a computer:** the left column ended halfway down and left a hole beside the form. | **Done.** The Home hero's photo of Joey and Ethan fills it. Computers only; phones and tablets never download it. |
| M7 | Medium | **About's panorama headline** ran to three lines on tablets (701 to 980 px). | **Done.** Two lines (**measured**). |
| M8 | Medium | **The net sheet's number boxes had a pale edge,** about 1.4:1 against their fill (**calculated**). WCAG 2.2 asks for 3:1 on the edge of a control. | **Done.** They use the contact form's edge colour, 3.4:1 (**calculated**). |
| M9 | Medium | **Long headlines on phones,** three or four lines at 390 px: Home 7, Your options 4, Our story 4, Contact 2, New homes 2, Our work 1. | **Done** (Jeremy said yes on the morning of Oct 27). Seven headlines are shorter and phone titles about 17% smaller up to 520 px wide: no title runs past two lines from 375 to 520 px; at 320 and 360 px a few still take three (**measured**). |
| M10 | Medium | **Few photos:** Your options has none, and Contact had none. | **Half done.** Contact now has one on computers. Your options needs a photo from Joey, or a decision. |
| P1 | Polish | **The comparison table** had a "GLP" badge, a gradient header and a shadow. | **Done.** Flat header, the direct column in deep green, striped rows on computers, no badge. |
| P2 | Polish | **Too many font sizes:** 22 on Home. The inspector suggests about five. | **Open.** Cutting them down risks the approved phone layout, so it needs a careful pass of its own. |
| P3 | Polish | **Old CSS** for pieces that no longer exist. | **Done.** Rules for the labels, the "Coming soon" tag and the old "live" dot removed. |
| P4 | Polish | **The phone call bar** was frosted glass over moving text. | **Done.** Solid white with a soft shadow. |

## 2. Major improvements

### 1. The net sheet

This is the section on Home that opens "What would you actually walk away with?".

**The idea:** the closing statement a title company hands a seller. It is one sheet, read top to bottom:
- the numbers at its head;
- the two paths side by side, each ending in what you keep;
- then the answer.

That paper is the thing a homeowner will eventually hold, and the net sheet now looks like an honest early copy of it.

On screens 1017 px and wider it now reads as one white sheet, top to bottom:
- **Your numbers** (the three boxes) sit in a row across the top. "A real offer depends on the home" sits beside them.
- **The costs we assumed** open five across on wide screens.
- **The two results** sit side by side: listing on cream on the left, direct on pale green on the right. Each ends in a firm rule and **"You keep"**, now up to 48 px; before, it was barely bigger than the text around it. The direct total is green.
- **The answer** is one flat deep green band across the sheet. From about 1150 px wide, the break-even line sits in its own box beside it.
- **The two buttons and the fine print** come last.

The comparison table above it is flat to match. Phones and tablets keep the answer-first order from Checkpoint 42; there the change is the flatter look.

What did not change:
- every number, default and sum (**tested**);
- every word;
- every id the script uses;
- the print layout, which still prints the two sheets and the answer (**tested**).

### 2. Shorter, tighter pages on desktop

Full page heights in pixels, Checkpoint 47 → Checkpoint 48 (**measured** in Chromium, the same way for both):

| Page | Phone, 390 px | 1024 px | 1440 px | 1920 px |
|---|---|---|---|---|
| Home | 16,719 → 16,588 (−131) | 10,561 → 10,169 (−392) | 11,260 → 10,526 (**−734**) | 11,289 → 10,561 (−728) |
| Your options | 11,801 → 11,584 (−217) | 7,264 → 7,137 (−127) | 7,471 → 7,111 (−360) | 7,494 → 7,118 (−376) |
| Our story | 8,903 → 8,835 (−68) | 5,618 → 5,203 (−415) | 6,082 → 5,362 (**−720**) | 6,076 → 5,378 (−698) |
| Our work | 9,038 → 8,998 (−40) | 4,749 → 3,898 (−851) | 5,648 → 4,409 (**−1,239**) | 5,642 → 4,417 (−1,225) |
| New homes | 6,200 → 6,125 (−75) | 4,756 → 4,354 (−402) | 5,346 → 4,761 (−585) | 5,346 → 4,774 (−572) |
| Contact | 6,064 → 5,990 (−74) | 3,708 → 3,781 (+73) | 3,884 → 3,796 (−88) | 3,884 → 3,806 (−78) |
| Privacy Policy | 4,406 → 4,400 (−6) | 2,779 → 2,782 (+3) | 2,917 → 2,839 (−78) | 2,917 → 2,839 (−78) |
| Terms of Service | 4,036 → 4,030 (−6) | 2,731 → 2,733 (+2) | 2,871 → 2,792 (−79) | 2,871 → 2,792 (−79) |

What the table shows:
- **At 1440 and 1920:** every page is shorter.
- **At 1024:** every page but three is shorter. Contact is 73 px taller because of its new photo, and the two legal pages are 2 to 3 px taller.
- **On phones:** every page is 6 to 217 px shorter. That comes only from the removed labels and lines; phone spacing is unchanged.

### 3. Flat, calmer surfaces everywhere

**What changed:**
- Cards are defined by tone: cream on white sections, white on cream ones.
- Shadows stay only on things that float: the header once you scroll, the phone menu, the call bar and the photo viewer.
- Lines stay only where they do a job: boxes you type in, real tables and the phone menu.
- Buttons are flat: green for the main one, pale navy for the other.

**Three details of approved choices changed with this.** Each is easy to undo if Jeremy preferred the old look:
- **The hero's background** is flat cream. D2 approved a soft cream gradient there.
- **The name plates on photos,** and the phone call bar, are solid white instead of frosted glass. D5 kept small frosted overlays on photos; the header keeps its glass.
- **The three dark bands** use one flat deep teal, `#2b5155`, taken from the middle of the old navy-to-green gradient. Those bands are the photo carousel, the call-to-action band and the contact band. This is the only new colour value.

## 3. Design refinements

### Spacing, desktop only

The smallest values are the phone values, so phones keep their spacing.

| Where | Before (at most) | After (at most) |
|---|---|---|
| Section padding (`.sec`) | 112 px | 88 px |
| Under each heading (`.head`) | 72 px | 48 px |
| The ridge under the hero | 270 px | 200 px |
| Slim sections | 88 px | 68 px |
| The call-to-action band | 104 px | 84 px |
| The contact section | 132 px | 96 px |
| The footer (top) | 84 px | 64 px |

The hero's bottom padding tapers from 36 px at 1024 px wide to 16 px from 1280 px.

### Type

- **Headings, 901 to 2560 px wide:** two lines at most on every page (**measured**). From 901 to 980 px the story, about, building and "we build too" sections already sit in two columns (Contact from 961 px), so their titles take the half-column size there as well; they ran to three or four lines in that band.
  - Section headings are at most 3rem.
  - Headings beside a photo, list or form are at most 2.6rem.
  - Page titles are at most 3.25rem.
  - The FAQ side heading sits on one line.
- **Intro paragraphs:** about 68 characters a line, down from about 97.
- **Small text:** nothing meant to be read is under about 13 px, at any width.
- **Card titles:** one size from 701 px wide.

### Home

- **Three paths:** each card leads with the time it takes ("7–14 days", "45–90+ days", "Your timeline"), set large on computers.
- **Carousel:** the heading, the sentence and the Previous/Next arrows share one row on computers. The arrows are filled circles instead of outlines.
- **Photo frame:** the gable frame's outer line is flat green instead of a gradient.

### Other pages

- **Our work:** no photo sits alone on the last row. With two across, an odd one out spans the row. With three across, a leftover one makes the last row four photos, and a leftover two share it.
- **Contact, computers:** the page title runs across both columns, so it fits in two lines; beside the form it took four. The form starts under it, level with the Call and Text tiles. Home keeps the form level with its heading.
- **Contact, computers:** the photo of Joey and Ethan from the Home hero sits under "What happens next?", with their names and "Co-founders, Hixson, TN". The image file and its alt text are the ones on Home, and the caption carries the same words as the Home name plate.
- **Our story, tablets:** the panorama's headline uses the full width over a darker lower half of the photo, so it fits in two lines.

### Phone headlines (Jeremy said yes on the morning of Oct 27)

Up to 520 px wide, phone titles are about 17% smaller: section titles 27 px instead of 33 px, page titles 31 px instead of 35 px. Tablets and computers keep their sizes. Seven headlines are shorter, with the same meaning and no new claim (`CONTENT_CLAIMS.md` row 67):
- **Home:** "Most push one answer. We show you all of them." (was "Most companies push one answer.")
- **Home and Our story:** "Chattanooga is home, same as yours." (was "We live and work in Chattanooga, same as you.")
- **Your options:** "Every path, side by side." (was "Every path for your home, side by side."); "List with an agent. Best price, if you can wait." (was "The best price, when you can wait."); "Creative solutions. When the usual won't fit." (was "When the usual paths don't fit.")
- **Our story:** "You hear two answers. There are more." (was "Homeowners hear two answers.")
- **Contact:** "Let's talk. No pressure, no scripts." (was "Let's talk about your home.")

Titles past two lines on the nine pages (**measured**):

| Width (px) | 320 | 360 | 375 | 390 | 412 | 430 | 480 | 520 | 540 | 600 | 700 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Before | 32 | 25 | 23 | 20 | 17 | 10 | 5 | 5 | 3 | 1 | 1 |
| After | 22 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 4. UX and accessibility

**Kept** (**tested**):
- one H1 per page and the skip link;
- the 3 px focus ring;
- 44 px tap targets and labels above fields;
- reduced motion respected;
- 0 axe violations.

No motion was added.

**Improved:**
- **Number boxes:** the net sheet's number boxes now have a 3.4:1 edge, up from about 1.4:1 (**calculated**; axe does not check this).
- **Small text:** raised to about 13 px.
- **Line length:** intro paragraphs are about 68 characters a line, the comfortable range for reading (**judgement**).
- **The phone call bar** is solid, so text no longer shows blurred through it.
- **Easier first read (judgement):** fewer labels and lines mean less to read before the heading. The net sheet's answer is now the largest thing in its section, so a wary visitor sees what they keep before the detail.

**Not verified:**
- no screen reader pass (VoiceOver, NVDA);
- no keyboard-only walk by a person (the automated focus and tab checks passed);
- no check on real phones.

I am not claiming full WCAG 2.2 AA compliance; the automated checks are a floor.

## 5. Performance and technical quality

- **Stylesheet:** 92,947 to 98,468 bytes, or 23,309 to 25,097 compressed: about 1.8 KB more over the wire (**calculated**). The new net sheet and layout rules outweigh the old rules removed.
- **No new scripts, fonts or outside requests.**
- **The Contact photo** is the Home hero's existing image, served at 800 px wide (**measured**):
  - phones and tablets never download it (checked at 390 and 768 px);
  - computers fetch it with the page (checked at 1024 and 1440 px). It is marked lazy, but it sits close enough to the first screen that the browser loads it at once.
- **Frosted glass** went from five kinds of surface to one (the header). Blur is costly to draw on low-end phones, so scrolling should be smoother (**judgement**; not measured on a device).
- **Pages are still built from `tools/pages/*.html` by `tools/build-pages.py`.** The one change to the builder is the Contact photo (`contact_section()`). CSS is v52, JS is v26.
- **One test was updated, not weakened.** `tools/netsheet-test.py` used to check that "the sheet sits beside the form" on wide screens. That layout was deliberately replaced, so the test now checks the new one at 1017, 1100, 1440 and 1920 px:
  - the three boxes in one row;
  - all of them above the two results;
  - the two results side by side, listing on the left.

  The checks for the answer-first order on phones and tablets are unchanged.
- **A second test was updated, not weakened.** `tools/form-test.py` checked that on the Contact page the form sits "level with the heading". The Contact page's heading now runs across the top, so that check failed in the final run, as it should have. Here is how it was changed:
  - The Contact check now asks for the new layout: the heading across the top, the form right under it level with the Call and Text tiles, and the left column in order, with the photo last.
  - Home, which keeps the old layout, got its own copy of the old check.
  - A new check makes sure the photo stays hidden on a phone.

  It now runs 289 checks, all passing.

## 6. Testing

### The full suite

All 19 tools were run on the finished build, phone headlines included (**tested**).

| Tool | What it checks | Result |
|---|---|---|
| check-links | every link, anchor, image and script on 9 pages (478) | pass, no duplicate ids |
| claims-check | words that need Joey's confirmation | clear |
| orphan-check | a single word alone on a heading's or label's last line | 4, under the limit of 6 |
| seo-check | `noindex` and the preview build | FAILS 0 |
| reviews-check | the dormant review path | FAILS 0 |
| notfound-test | the 404 page and its 45 links | FAILS 0 |
| nobreak-test | 46 phrases never split, at 9 widths and 3 text sizes | FAILS 0 |
| safety-test | no page stays blank when a script fails | FAILS 0 |
| netsheet-test | the sums, every state, the layout and order at 8 widths, print | FAILS 0 |
| viewer-test | the photo viewer | FAILS 0 |
| scrolltop-test | pages open at the top | FAILS 0 |
| bar-test | the phone call bar | FAILS 0 |
| mobile-audit | phone layout, tap targets and load speed (a report) | no sideways scroll. Its other notes were there before: the logo's small lockup text, the logo file's size, and one link at the end of a sentence on Home (the same before and after) |
| wide-audit | 9 pages at 11 sizes, 320 to 2560 px | FAILS 0 |
| bigtext-test | 369 page and size combinations with bigger text, plus 40 with the menu or photo viewer open | FAILS 0 |
| readability | reading ease and school grade | grade 3.4 to 5.0 on the main pages |
| page-size | heights and word counts (a report) | see section 2 |
| a11y-check | axe on every page and every open state | 0 violations |
| form-test | the contact form, 289 checks | FAILS 0, after the layout update in section 5 |

axe also lists, for each page, between 2 and 36 places it cannot judge on its own and leaves for a person to look at. Most are text over photos or coloured bands. I did not check each of these by hand.

### Inspector

Run on six pages at 1440, 768 and 390 px (**measured**):
- on Checkpoint 47 (before);
- in rounds 2 and 3, with fixes after each;
- on the build before the phone headlines (round 4);
- on the final build, with the phone headlines.

The before and final counts are in section 1.

### Widths and text sizes checked

- wide-audit: 9 pages at 11 widths, 320 to 2560 px;
- nobreak-test: 9 widths at 3 text sizes;
- mobile-audit: phone widths;
- bigtext-test: 200% text;
- headings: two lines or fewer on nine pages at 17 widths from 901 to 2560 px, and from 375 to 900 px (**measured** at 12 widths);
- About's panorama: from 701 to 980 px (**measured**).

### Screenshots

Before and after at 1440 px for each main page, and the net sheet at 1440, 1280 and 390 px. They are in the thread, and in `/mnt/project-files/ck48-shots/`, which is not in the repo.

### Not tested

- real phones: swiping, the call bar while scrolling, iPhone Safari;
- Safari and Firefox on a computer. Only Chromium is installed here. By reading the stylesheet, Checkpoint 48 adds two CSS features the live site did not use: `display:contents` on the plain wrapper in the carousel heading (computers only; Safari has supported it since 2018 and Firefox since 2015, and the wrapper means nothing to a screen reader, so nothing is lost), and one more `text-wrap` line, which browsers without it ignore;
- screen readers;
- printing on paper (the print layout is checked in the browser only);
- the live site, which is blocked from the cloud;
- anything that sends, because no form was typed into or submitted.

The three audits that stopped at the usage limit (components, art direction, responsive) were not rerun.

## 7. Remaining opportunities

### What the inspector still flags

| Flag | What it is | What to do |
|---|---|---|
| Text under the call bar while scrolling (phones) | Real, but built in | The fixed Call and Text bar covers whatever scrolls behind it, headings included. That is what a fixed bar does; moving it is a bigger decision than this pass. |
| "Edge text" at 768 and 390 px; "side-scroll"; "empty middle" | By design | The carousel's photos run off the edge so it looks swipeable. Jeremy asked for carousels. |
| "Still page" | By design | No autoplay and restrained motion (D5). |
| "No footage" | No honest clip exists | A short clip from Joey of a job site would answer it, but under the no-autoplay rule it would have to be click to play. |
| Few pictures (Your options 0, Contact 1) | Real | Needs Joey's photos (`research/photo-brief-for-joey.md`). |
| Two rows of identical cards (Our story) | Real, minor | Could become a list set in large type. Worth trying in a later pass. |
| 22 font sizes on Home | Real, minor | A careful consolidation pass, checked against the phone layouts. |
| "Labels above headings" | False alarm | "Cost of waiting" above the net sheet totals is the last row of the list. "Direct" is a column name in the Options mini sheet. "Another closing day" is a photo badge. |
| "Icon cards" on Home | False alarm | The check marks belong to a list, not decorative icons. |
| "Off centre" at 1440 px (Your options, Contact) | False alarm | The page is centred; the right-hand text column simply ends before the edge of the layout. |
| "Lopsided" (Our story panorama) | False alarm | The headline sits over the photo, which fills the width. |
| Mixed-font headline, cream background | Approved | The Fraunces italic accent (D3) and cream (D2) are locked. |
| Contact "body size 13.8 px", "grey body text" | Mostly Joey's legal text | The small text is Joey's text-message consent wording, which only Joey and an attorney should change. Its contrast still passes (5.8:1). |

### Still open from Checkpoint 47

1. Drop the comparison table on Home, since the net sheet covers it? My recommendation was to keep it.
2. Fold New homes into Our work? My recommendation was to keep it.

## 8. Next steps

**Jeremy:**
1. Look at the before/after screenshots and the live preview once Checkpoint 48 is committed. The commit message is in `SESSION_HANDOFF.md`.
2. Try it on your phone.
3. Say yes or no to the three detail changes in section 2: flat hero cream, solid photo name plates, one dark teal.
4. Decide the two Checkpoint 47 questions.

**Joey:** photos for Your options and Contact; one real deal for the net sheet's example (D18); his consent wording, with an attorney.

**Next session:**
- real-device checks: iPhone Safari, Android Chrome, Firefox;
- the font-size consolidation;
- the three audits that did not run, if Jeremy wants an independent read.

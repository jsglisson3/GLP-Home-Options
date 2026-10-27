# Whole-site UI/UX review, Oct 27, 2026

Asked by Jeremy (Oct 27, about 8:24 PM Oct 26 Chattanooga time): review the whole site with the new UI/UX skills, then simplify everything as much as possible so the site feels better. Later (about 9:36 PM): "don't be afraid to add a carousel feature i always love that". The work is Checkpoint 47.

## How the two skills were used

- **ui-ux-pro-max** (github.com/nextlevelbuilder/ui-ux-pro-max-skill). I read it but did not install it in this folder. Used for:
  - its priority order: accessibility, touch, performance, style, layout, type and colour, motion, forms, navigation;
  - its design-system search for "local real estate home buyer trust service", set to calm, low motion and spacious;
  - its rule list, mainly `primary-action` (one main button per screen), `excessive-motion` (animate one or two things per view), `content-priority`, `whitespace-balance`, `consistency` and `icon-style-consistent`;
  - its carousel guidance: no movement the visitor did not start, Previous/Next buttons as the keyboard route, and still images under reduced motion;
  - its pre-delivery checklist.

  **Not used:** the palette and fonts it suggested (royal blue with an "urgent" orange, Cinzel and Josefin Sans). They read as luxury and pressure, which is wrong for this audience, and the navy, green and two fonts are already approved. It agreed with what we already do: navy for trust, the accent colour only on the main button, contact details never hidden, and a short form.
- **frontend-design** (Anthropic). Used as the taste filter: spend boldness in one place and cut decoration that has no job. In particular it says to avoid the common "generated page" tells:
  - a small capital label above every heading;
  - an accent phrase in every heading;
  - a fade-and-slide on every section;
  - the same rounded card with an icon square everywhere;
  - an arrow on every button.
- **Inspiration sites:** this session's network blocks dribbble.com and awwwards.com, so I could not browse them. Nothing here is copied from them.
- **Independent check:** three fresh reviewers who had not seen my reasoning checked the change, one each for code, visuals and the project rules. A fourth reader then tried to disprove each of their findings: 17 of the 19 held and are fixed below, and the other two were disproved and needed no change. A second round checked those fixes and the carousel. It found one real carousel problem (at 200% text on phones the last caption was cut off and Next stopped short) and a handful of small ones, all fixed.

## What is already strong (kept)

- The people-led hero: Joey and Ethan's faces in the first screen, the phone number as text, and "no obligation" said once.
- The net sheet: honest, explained, printable, and on phones the answer comes first.
- Plain words almost everywhere, with no fake urgency and no invented numbers.
- Accessibility and phone work well above average: tested at many widths and text sizes, 0 axe violations, 44 px tap targets, and the Call and Text tiles above the form.
- The contact form: only name and phone are required, and everything else is folded away.

## Findings and what was done

| # | Finding | Skill rule | What changed |
|---|---|---|---|
| 1 | **Every section opened with a small capital label** ("YOUR OPTIONS", "HOW IT WORKS"...): 37 on the six main pages (10 on Home), plus "Legal" on the two legal pages. They repeated the heading and are the most common template tell. | frontend-design: no labels above content | 31 removed from the main pages, plus the two "Legal" labels. **Six stay because each carries a fact**, now as a plain sentence-case line: "Chattanooga & surrounding counties" (Home first screen, wide screens), "A recent closing" (Home and About), "Seller net sheet", "Recently closed" (Our work), "Coming soon · Chattanooga" (New homes). The 404 page keeps "Page not found". |
| 2 | **41 headings had a green italic second line**, so none stood out. | frontend-design: boldness in one place | The italic accent stays in each page's main title only. In section headings the second sentence still starts its own line, in the same type as the rest. |
| 3 | **48 blocks on Home faded and slid in as you scrolled** (174 across the six main pages). That is motion without meaning, and content appeared late on slow phones. | ui-ux: excessive-motion, motion-meaning | Removed. Content is simply there. The hero headline's one entrance stays. |
| 4 | **Arrows on almost every button and link** (40 in all). | frontend-design: arrow on every button | Removed from buttons and text links. Text links are now underlined so they still look like links. Arrows stay where they mean "go": the photo viewer, the "Jump to" and "Explore" lists, the contact tiles, the diagram on Our story, and the new carousel buttons. |
| 5 | **27 decorative icon squares** on option, value, proof and "who it's for" cards. They carried no information and made every card look alike. | frontend-design: the card kit; ui-ux: icon discipline | The 20 decorative ones are gone. The 7 in the "Jump to" and "Explore" lists stay, because each marks a link. |
| 6 | **Mixed small-label styles**: capital, letter-spaced micro-labels ("THE SITUATION", "CO-FOUNDERS", "EXPLORE", "BEDROOMS", "CALL") next to plain ones. | ui-ux: consistency | All small labels are now one plain sentence-case style, slightly larger and easier to read. The only capitals left are the "HOME OPTIONS" lockup inside the logo and the "GLP" badge. |
| 7 | **Home repeated itself near the end.** The FAQ had its own Call and Email box right above the contact section, which has them again. On phones the contact section ended with "What happens next?", the same three steps as "How it works". | ui-ux: content-priority | The FAQ box is gone on Home, Options and New homes. Each FAQ intro now carries the phone number as a link ("Call or text (423) 451-5707 and ask us directly"). On Options and New homes the email address is now only in the footer. "What happens next?" is hidden on Home below about 960 px wide (phones and upright tablets, where the form sits in one column). Wide screens keep it beside the form, where it stops the left column ending halfway down, and the Contact page keeps it everywhere. |
| 8 | **Too many big buttons per screen on Home.** Under the option cards sat a card with its own button plus two large buttons, and the closing story ended with two more. | ui-ux: primary-action | One sentence with a link and one button under the cards. The story ends with "Read our story" only. |
| 9 | **Very generous section spacing on wide screens** (up to 136 px above and below every section). | ui-ux: whitespace-balance | Up to 112 px. Phones are unchanged. |
| 10 | **Home showed only one closing and the new build**, and never the renovation work, which is the strongest proof for a wary seller. | Jeremy's carousel request; ui-ux carousel rules | **New photo carousel on Home**, after "How it works": "Before, during and after." It holds the 8 renovation photos with the same captions and descriptions as Our work, so nothing new is claimed, and ends with "See all our work". It never moves by itself. Visitors swipe it on a phone, or use the Previous/Next buttons or the arrow keys on a computer. Photos keep their own shape, with no cropping. Without JavaScript it still scrolls sideways. It is placed after "How it works", not right after the closing story, so the photos never read as that same house. |

## Left for you to decide (nothing changed)

1. **The comparison table on Home.** The net sheet right below it makes the same point with real numbers. Removing the table would save about one phone screen. The Options page and the footer link to it, so those links would point at the net sheet instead. My recommendation is to keep it, because a table is quicker to scan than typing numbers.
2. **New homes and Our work.** Folding New homes into Our work would cut the menu from six items to five. You had said New homes stays a light teaser and may move to a separate construction site, so I left it alone.
3. **The default net sheet numbers** stay as they are. D18 waits on one real deal from Joey.
4. **Joey's two text-message consent sentences** take about 545 px of the form on a phone. They are his legal wording, so any shortening is for Joey and an attorney.

## What did not change

- Colours and fonts.
- The hero photo, headline, wording and phone number. Only the small label's style and the button arrow changed.
- The net sheet's numbers, method and name.
- The form's fields and wording, Joey's sentences, and the phone, email and address. Only the send button's arrow and the message label's capitals went.
- The legal pages' policy text. Only the "Legal" label above the title went.
- Every claim. The new or reworded text is: the carousel heading "Before, during and after.", its line "Photos from our job sites, from first demo to the finished kitchen." and "See all our work" (all from the Our work page); the Home line "Situation doesn't fit a box? We also look at options like seller financing... See how those work", made from the card it replaced, and the FAQ intros now naming the phone number.
- `noindex`, so the site stays out of search.

## Page heights (full page, before → after)

| Page | Phone (390 px) | Laptop (1440 px) |
|---|---|---|
| Home | 17,037 → 16,786 (16,073 without the 713 px carousel) | 10,914 → 11,257 (10,457 without the 800 px carousel) |
| Our story | 9,676 → 8,999 | 6,602 → 6,079 |
| Your options | 12,306 → 11,898 | 7,637 → 7,468 |
| Our work | 9,274 → 9,135 | 5,931 → 5,645 |
| New homes | 6,810 → 6,297 | 5,734 → 5,343 |
| Contact | 6,426 → 6,162 | 4,156 → 3,881 |
| Privacy, Terms | about 33 px shorter | about 41 px shorter |

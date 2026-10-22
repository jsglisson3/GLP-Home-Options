# Older phones and browsers: what the site needs, and what it does without

_Written Oct 22, 2026 (Session 6g, Checkpoint 32). A code check plus a simulated old phone. No real iPhone, iPad or Safari was available in the cloud (only Chrome's engine), so read "simulated" as "very likely", not "proven"._

## The short answer

- **The scripts are safe on old phones.** Both site scripts and the small head script parse as plain old-style JavaScript (the 2009 standard, ES5), and every newer browser feature they touch has a fallback: the scroll-reveal and bottom bar fall back to "show everything / show the bar" when `IntersectionObserver` is missing (iOS before 12.2), and the Our work photo viewer only starts when the browser knows `<dialog>` (iOS 15.4 and later); otherwise each photo is simply a link to the full picture.
- **The stylesheet was the weak spot, and Checkpoint 32 fixes it.** Before the fix, a phone from the iPhone 6 era (iOS 12) would have shown every page in a plain serif font with most spacing gone, no side padding, and the four photo frames (Home hero and "how it works", About, New homes) collapsed. After the fix the same simulated phone shows the right font, spacing and frames; what is left is cosmetic (below).
- **Newer phones and computers are not affected.** Every line added is overridden by the line right after it. Proof: `tools/computed-diff.py` compared Checkpoint 31 and 32 on all 8 pages at 7 screen widths (320 to 1920 px): 56 page-and-width pairs, 22,771 elements, every size, position and style value identical (0 differences).

## What was wrong, and the fix

Browsers throw away a CSS line they do not understand, and some newer features sit in lines that mattered:

| Newer feature | First iPhone / Chrome that has it | What an older phone did before the fix | Fix |
|---|---|---|---|
| `clamp()` (sizes that grow with the screen) | iOS 13.4 / Chrome 79 | The whole `body{font:…}` line was dropped, so all text became the browser's default serif. About 90 other sizes and spacings (section padding, headline sizes) vanished and pages ran together. | 92 plain lines in front of them, using each rule's smallest size. |
| `inset` and `margin-inline`, `padding-block` | about iOS 14.5 to 15 / Chrome 87 to 89 (the compatibility table says 15 for the whole family) | Photo frames, tinted overlays and centered containers lost their edges and side padding. | 14 `inset` rules and 16 margin/padding rules get left/right/top/bottom twins. |
| `aspect-ratio` | iOS 15 / Chrome 88 (from memory; the table I used did not list it) | The four photo frames had no height and disappeared. | A short `@supports not (aspect-ratio:1/1)` block gives them the same height the old way. |
| `--pull:clamp(…)` (a variable) | as `clamp()` | The hero's bottom padding became zero. | A one-line `@supports not` override. |

Everything else was already safe: `100svh/100dvh` sit behind a plain `100vh`; `:has()` and `:focus-visible` rules are optional extras (old phones keep their normal focus ring and header color); the subgrid layout is inside `@supports`; `backdrop-filter` has the `-webkit-` form; the hero gable's `clip-path:url(#gable)` on inline SVG works on iOS 13 and later; `<details>` FAQs, `loading="lazy"` and `fetchpriority` are ignored harmlessly when unknown.

## What each phone gets now (support floor)

| Phone or browser | What to expect |
|---|---|
| iOS 15.4 and later, Chrome and Samsung Internet from about 2022 | As designed. |
| iOS 14.5 to 15.3 | As designed, except: no custom focus rings (the normal ring shows), no smooth scrolling on in-page links, and the hero header keeps a white tint instead of cream. |
| iOS 13.4 to 14.4 (and Chrome 79 to 83) | Same as above, plus rows of buttons and icon-to-label gaps sit tighter, because flex `gap` arrives in iOS 14.5 and Chrome 84. Everything is readable and tappable. |
| iOS 12 and early 13 (iPhone 5s to 6 Plus, old iPads) | Plainer but complete: correct font, spacing at the small end of each range (including on tablets), photo frames present. Buttons that sit side by side or stacked touch each other. |
| Older than iOS 12, Internet Explorer, old Edge | Not tested. Text, links and the call and text buttons should still work (the script has a fallback), but the icons (the sprite uses `<use href>`) and some layout may not show. |

Compatibility figures come from the open caniuse data (checked Oct 22, 2026): `clamp()` iOS 13.4 / Chrome 79; flex `gap` iOS 14.5 / Chrome 84; `:focus-visible` iOS 15.4 / Chrome 86; `:has()` iOS 15.4 / Chrome 105; `svh/dvh` iOS 15.4 / Chrome 108; `scroll-behavior` iOS 15.4 / Chrome 61; `overflow:clip` iOS 16 / Chrome 90; subgrid iOS 16 / Chrome 117; `<dialog>` iOS 15.4 / Chrome 37; `loading="lazy"` iOS 15.4 (partial) to 16.4 / Chrome 77; `IntersectionObserver` iOS 12.2 / Chrome 58.

## What is still plainer on old phones (by choice)

- **Flex `gap`** (iOS before 14.5): 36 rules. There is no clean "feature query" for flex gap, so I did not patch them; a script check could add margins if a real old phone shows crowding.
- **`overflow-x:clip`** (iOS before 16): a page could scroll sideways if something is wider than the screen. The big-text and phone tests found nothing wider.
- **Smooth scroll, focus rings, `:has()` header tint, `100svh` hero height** on iOS before 15.4: cosmetic.
- **`text-wrap:balance/pretty`** (line-break polish): ignored by browsers that do not know it.

## How this was checked (so it can be repeated)

1. Read every CSS feature flagged by a compatibility scanner (`doiuse` with caniuse data): 17 features, 358 notices; looked at each flagged line.
2. Parsed both scripts and the inline head scripts with the `acorn` JavaScript parser in ES5 mode: all parse.
3. Scanned the 8 pages' HTML for newer elements and attributes (`<dialog>` is created by script only; no `<picture>`, no modules).
4. **Simulated an old browser:** made a copy of the stylesheet with every declaration an iOS 12 or iOS 14.5 Safari cannot parse removed (as that browser would), loaded all 8 pages at 375 px wide in Chrome and compared heights and screenshots. Before the fix the simulated iOS 12 Home page was 12,533 px tall against 18,515 px normally (spacing gone); after the fix it is 18,466 px and looks right. This simulates the missing CSS, not WebKit's own quirks.
5. Proved the fix changes nothing for modern browsers with `tools/computed-diff.py` (above). The full big-text, bottom-bar, safety, start-at-top, link, claims and accessibility checks were run on the fixed version as well; results are in `PROJECT_STATUS.md`.

## Next steps (your call)

- **Borrow one old iPhone or iPad** (an iPhone 6 to 8 or an iPad Air 2, if a relative has one) and look at Home, Options with the net sheet, Contact and the menu once the site is live. Fifteen minutes would show whether the flex-gap crowding needs a patch.
- **When analytics is switched on (parked),** look at the visitors' iOS and Android versions before deciding how far back to polish.
- The scripts used for the simulation live in the cloud workspace for now; `tools/computed-diff.py` is in the repo.

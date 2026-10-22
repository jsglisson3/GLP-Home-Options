# CSS inventory: what Session 5 (consolidation) starts from

**Generated Oct 21, 2026 from `css/site.css` at Checkpoint 11 (the live Checkpoint 10 code); the numbers are counted, the target buckets are proposals.** Nothing here changes a page. Session 5's rule still applies: before and after screenshots must match (`tools/shots.py` with `--widths` set to the widths in the "band" column, then `tools/shots-diff.py`).

File size: 60,347 bytes, 750 lines.

## Breakpoints (media queries)

Proposed target breakpoints (P1): **640** (phones), **980** (stacking to one column), **1160** (full desktop header), **1360** (the header phone number), plus **420** for narrow-phone tweaks if the bands below prove too wide (without it, drop 420 and move those rules to 640). Each query is mapped to its nearest target. A rule moved to a target changes how the page looks in the "band" of widths between the old edge and the new one, so that band must be screenshotted (`tools/shots.py --widths=...`). Risk: low is 40 px or less, check is up to 100 px, LARGE is more. The `max-width:350px` rule is the 320 px icon-only Menu and should stay as it is.

| Query | Blocks | Rules inside | Bytes | First lines | Target | Band that would change |
|---|---|---|---|---|---|---|
| `(max-width:1080px)` | 1 | 2 | 116 | 676 | 1160 | 1081 to 1160 px (check) |
| `(max-width:1160px)` | 1 | 3 | 88 | 115 | 1160 | none (none) |
| `(max-width:350px)` | 1 | 2 | 183 | 120 | 420 | 351 to 420 px (check) |
| `(max-width:380px)` | 2 | 2 | 92 | 500,675 | 420 | 381 to 420 px (low) |
| `(max-width:420px)` | 2 | 6 | 170 | 118,391 | 420 | none (none) |
| `(max-width:440px)` | 1 | 5 | 457 | 492 | 420 | 421 to 440 px (low) |
| `(max-width:480px)` | 1 | 1 | 46 | 533 | 420 | 421 to 480 px (check) |
| `(max-width:520px)` | 6 | 15 | 653 | 182,188,234,397,445,693 | 420 | 421 to 520 px (check) |
| `(max-width:560px)` | 2 | 4 | 363 | 252,678 | 640 | 561 to 640 px (check) |
| `(max-width:620px)` | 3 | 7 | 353 | 644,666,698 | 640 | 621 to 640 px (low) |
| `(max-width:640px)` | 1 | 2 | 49 | 116 | 640 | none (none) |
| `(max-width:700px)` | 2 | 14 | 998 | 336,407 | 640 | 641 to 700 px (check) |
| `(max-width:720px)` | 1 | 1 | 62 | 287 | 640 | 641 to 720 px (check) |
| `(max-width:760px)` | 2 | 11 | 1478 | 537,705 | 640 | 641 to 760 px (LARGE) |
| `(max-width:767px)` | 1 | 2 | 204 | 211 | 640 | 641 to 767 px (LARGE) |
| `(max-width:860px)` | 1 | 1 | 46 | 735 | 980 | 861 to 980 px (LARGE) |
| `(max-width:900px)` | 12 | 21 | 954 | 229,294,307,321,432,453... | 980 | 901 to 980 px (check) |
| `(max-width:960px)` | 2 | 2 | 91 | 396,516 | 980 | 961 to 980 px (low) |
| `(max-width:980px)` | 5 | 11 | 492 | 178,282,600,643,665 | 980 | none (none) |
| `(min-width:1161px)` | 2 | 2 | 50 | 117,572 | 1160 | none (none) |
| `(min-width:1360px)` | 1 | 1 | 31 | 114 | 1360 | 1360 to 1360 px (low) |
| `(min-width:981px)` | 1 | 1 | 64 | 187 | 980 | none (none) |
| `(min-width:981px) and (max-width:1100px)` | 1 | 3 | 151 | 198 | 980 | none (none) |
| `(pointer:coarse)` | 2 | 2 | 53 | 530,589 | keep | n/a |
| `(prefers-reduced-motion:no-preference)` | 1 | 1 | 33 | 738 | keep | n/a |
| `(prefers-reduced-motion:reduce)` | 1 | 4 | 175 | 742 | keep | n/a |
| `print` | 1 | 2 | 77 | 749 | keep | n/a |

Distinct queries: 27 (22 width edges: 19 `max-width` values and 3 `min-width` values); media blocks: 57.

## Type sizes

44 distinct `font-size` values. Most used:

| Value | Uses |
|---|---|
| `.95rem` | 7 |
| `.88rem` | 6 |
| `.9rem` | 5 |
| `.86rem` | 4 |
| `.92rem` | 3 |
| `.97rem` | 3 |
| `.96rem` | 3 |
| `1.06rem` | 2 |
| `.58rem` | 2 |
| `1rem` | 2 |
| `1.02rem` | 2 |
| `1.04rem` | 2 |
| `1.15rem` | 2 |
| `clamp(2.35rem,4.7vw,4.2rem)` | 1 |
| `clamp(2.05rem,4.5vw,3.5rem)` | 1 |
| `1.3rem` | 1 |
| `1.04em` | 1 |
| `clamp(1.06rem,1.4vw,1.2rem)` | 1 |
| `1.6rem` | 1 |
| `1.02em` | 1 |
| `clamp(1.08rem,1.55vw,1.26rem)` | 1 |
| `.93rem` | 1 |

## Spacing (padding, margin, gap)

55 distinct lengths across padding, margin and gap. Most used:

| Length | Uses |
|---|---|
| `12px` | 37 |
| `18px` | 37 |
| `14px` | 30 |
| `10px` | 26 |
| `22px` | 26 |
| `16px` | 26 |
| `8px` | 21 |
| `28px` | 18 |
| `20px` | 17 |
| `24px` | 16 |
| `6px` | 15 |
| `26px` | 12 |
| `32px` | 12 |
| `34px` | 11 |
| `9px` | 11 |
| `36px` | 11 |
| `40px` | 9 |
| `0px` | 8 |
| `4px` | 8 |
| `2px` | 8 |
| `64px` | 7 |
| `48px` | 6 |
| `11px` | 6 |
| `30px` | 6 |
| `76px` | 5 |
| `72px` | 5 |
| `44px` | 5 |
| `80px` | 4 |

## Corner radii

20 distinct values. Most used:

| Value | Uses |
|---|---|
| `var(--r-l)` | 18 |
| `999px` | 13 |
| `50%` | 8 |
| `var(--r-m)` | 8 |
| `18px` | 5 |
| `12px` | 4 |
| `14px` | 3 |
| `2px` | 2 |
| `7px` | 2 |
| `8px` | 2 |
| `16px` | 2 |
| `10px` | 2 |
| `15px` | 2 |
| `6px` | 1 |

## Stacking (z-index)

6 distinct values: `-1` (5), `200` (1), `60` (1), `3` (1), `-2` (1), `70` (1).

## Motion

Durations used: `.2s` (18), `.25s` (17), `.3s` (4), `.4s` (4), `.35s` (4), `.8s` (3), `.9s` (3), `.38s` (3), `.7s` (2), `.5s` (2), `1s` (2), `0s` (2), `.85s` (1), `.95s` (1), `.74s` (1), `.86s` (1), `.08s` (1). Easings used: `cubic-bezier(.2,.7,.2,1)` (15), `ease` (10), `cubic-bezier(.2,.75,.2,1)` (1), `linear` (1).

Keyframes: `reveal`, `rise`, `enter`, `enter-photo`, `draw` (all behind `prefers-reduced-motion: no-preference`). Proposed tokens (P4): 160, 280 and 480 ms plus `cubic-bezier(.2,.7,.2,1)` (already the most used curve on the phone bar).

## Colors outside the token block

After `:root`, the file uses 376 `var(--...)` references and 56 `rgb()` or `rgba()` literals, plus these hard-coded hex colors:

| Hex | Uses |
|---|---|
| `#fff` | 71 |
| `#c4ecda` | 4 |
| `#3a7a66` | 3 |
| `#fdfbf6` | 3 |
| `#e8f6ef` | 2 |
| `#316656` | 2 |
| `#fbfdfc` | 2 |
| `#25404d` | 2 |
| `#2b5155` | 2 |
| `#336b59` | 2 |
| `#9fc8b8` | 1 |
| `#34705d` | 1 |
| `#2a5a4c` | 1 |
| `#efe8d8` | 1 |

Each hard-coded color is either a token waiting to happen (Session 5) or a one-off (the Facebook blue, the white page background).


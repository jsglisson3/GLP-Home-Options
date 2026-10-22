# Site review: Oct 22, 2026 (full review of all 8 pages; no live page changed)

**What this is:** a whole-site review for Jeremy, Joey and Ethan, written at Checkpoint 34 (the site itself last changed at Checkpoint 32) and aimed at the next sessions. It follows `site-review-2026-10-21.md` (written at Checkpoint 10) and reports what happened to each of its 15 findings. **Companions:** `what-works-2026-10-22.md` (the research) and "Proposed plan v3" in `ROADMAP.md` (what to do about it). Nothing here is approved until Jeremy says so, and nothing here is on the site.

**Method.**

- I read the full text of every page (Home, Your options, Our story, Our work, New homes, Contact, Privacy, Terms), including every FAQ answer.
- I looked at each page on a phone (390 px wide) and a laptop (1440 px wide), scrolling the way a visitor does.
- I ran Lighthouse 12 on all 8 pages (phone settings) on a local copy that mimics GitHub Pages (compressed files, 10-minute caching). The contact form's script cannot load in our workspace, so the "Best practices" score of 96 on Home and Contact is that missing script, not a site error. These are local numbers, not the live site's.
- I re-ran our own checks (links, claims, readability, checkpoint, single-word lines).
- Four independent research helpers worked in parallel: three on research (`what-works-2026-10-22.md`) and one who read the site cold, as four different first-time visitors, without seeing any of our notes.
- Findings are my judgment, backed by the numbers shown. Nothing here is a study of GLP's own visitors; there are none yet.

## Verdict

The site is strong where sites like this are usually weak: one clear promise, honest numbers (the net sheet can say that listing wins, and the example does), plain words (about grade 4 on our yardstick), real faces, a call and text option on every page, very light pages, and a clean accessibility record. In the research we read, no other seller-facing page showed a net sheet that can come out in favor of listing.

What stands between "good" and "ready to show the public" is mostly **not design.** It is three things:

1. **Facts only Joey has**, which wary sellers ask about and the site does not yet answer: how an offer is set, how GLP earns money, what a seller pays at closing, what happens if a seller changes their mind, who closes, full names and bios, a service-area list.
2. **Real proof**, which takes time: no reviews, one closing story, first names only, a PO box only.
3. **Length**: Home is 18,278 px tall on a phone (about 22 screens) and Your options is 12,157 px.

Plus the things only people and real devices can test: a real-phone pass, the contact form, the legal pages, and a reading test with older visitors.

A fresh reader agrees. A helper who read the site cold, as four made-up visitors (a 71-year-old with an inherited house, a night-shift worker behind on the mortgage, a daughter settling an estate from another state, and a skeptical landlord), found the tone warm and the arithmetic checkable (they re-did the net sheet by hand and it adds up). Their trust stopped where checking would start: nothing on the site can be verified outside the company. I checked their claims against the pages and by measurement; the ones that held up, and what my own checks added, are N22 to N31 and the section "What four first-time visitors made of it."

## Scorecard (my judgment)

| Area | Rating | Why |
|---|---|---|
| Clear promise, first screen | Good | Faces, a headline, one sentence on what GLP does, two actions. The headline itself is a brand line ("Real home options. Clear next steps."); the sentence below it does the explaining. A cold reader got who, where, what the two buttons do and "no pressure" within five seconds, but not that GLP buys houses for cash, how fast, or the phone number (the first digits on Home are 13,652 px down a phone page). |
| Honesty and candor | **Strong** | The compare table, the net sheet, "Trades some price for speed and certainty," "Honest about fit," "bring your own attorney or title company." |
| Proof and credibility | **Gap** | No reviews, one closing story, one build, photos from Joey's own phone (good) but first names only, no bios, no license or affiliation details, a PO box only. |
| Explaining the deal | **Gap** | "A fair cash offer" is never explained; nothing on how GLP earns, what the seller pays, who closes, or what happens after "yes." |
| Contact paths | Good | Call, text, email, book a call, Facebook, a form, a "what happens next" line, a fallback if the form does not load. The form is the one thing that is not ours yet and cannot be tested from here. |
| Phone experience | **Strong** | Bottom bar, 44 px targets, text-size floor, safety nets, tested with enlarged text. Real phones still to do. |
| Speed | **Strong** | See Lighthouse below. |
| Accessibility | **Strong** (automated) | axe 0 violations; Lighthouse 100 on every page. Manual keyboard and screen-reader pass not done. |
| Answers to common questions | Good | 9 questions on Home, 5 on Options, 3 on Contact. Missing the classic seller questions listed in N6. |
| Page length and structure | **Gap** | Home 12,138 px (laptop) and 18,278 px (phone); Options 7,498 and 12,157. |
| Legal and rules footing | **Gap** (waiting on others) | Legal pages are plain-words drafts with a visible "Draft for review" note; texting wording and the form's consent are for an attorney and GoHighLevel; see `compliance-questions-for-joey.md`. |
| Search and launch readiness | Parked | `noindex` on; no sitemap, robots file or custom 404 page. Parked by Jeremy until the site is pristine. |
| Upkeep | Good, one warning | Strong checks and tools. CSS has 73 media-query blocks at 30 different widths (it was 57 at 22); `PROJECT_STATUS.md` is 135 KB. |

## Measured today (local, Oct 22)

| Page | Performance | Accessibility | Best practices | SEO | Largest paint | Blocking time |
|---|---|---|---|---|---|---|
| Home | 94 | 100 | 96* | 63** | 2.4 s | 220 ms |
| Your options | 99 | 100 | 100 | 63** | 1.7 s | 70 ms |
| Our story | 99 | 100 | 100 | 63** | 2.3 s | 30 ms |
| Our work | 100 | 100 | 100 | 63** | 1.8 s | 30 ms |
| New homes | 97 | 100 | 100 | 63** | 2.4 s | 110 ms |
| Contact | 99 | 100 | 96* | 63** | 2.0 s | 40 ms |
| Privacy | 100 | 100 | 100 | 63** | 1.2 s | 0 ms |
| Terms | 100 | 100 | 100 | 63** | 1.4 s | 0 ms |
| Home, laptop settings | 100 | 100 | 96* | 63** | 0.6 s | 0 ms |

\* The form's third-party script cannot load in our workspace. \** The only SEO failure is the deliberate `noindex`; it will pass when `noindex` is removed. Layout shift is 0 on every page. Phone settings, simulated slow connection. Home's first load is 243 KB; the whole page after scrolling is about 0.8 MB; Our work is about 2 MB (19 photos, loaded as you scroll). Home's largest paint (2.4 s) is close to the 2.5 s "good" limit, so Home should not get heavier, and it must be re-measured on the live site with the real form script. GitHub Pages caches files for 10 minutes and we cannot change that.

## What happened to the Oct 21 findings

| # | Finding | Status today |
|---|---|---|
| F1 | Bridge hero and kitchen-table photo origins unconfirmed | **Open, waiting on Joey** (`questions-for-joey.md` item 1; `CONTENT_CLAIMS.md`) |
| F2 | Riverfront banner is 900 x 225 px stretched wide; origin unknown | **Open.** Still 900 x 225; visibly soft on a laptop; origin and license unknown |
| F3 | Closing-day photo shows sellers' faces and a title company's sign | **Open, waiting on Joey** (consent), and a second closing photo with a title company's logo was added on Oct 21 on the same terms |
| F4 | Home repeats the Options page | **Open (D7).** Home is 7% shorter on a laptop (13,050 to 12,138 px) and 10% on a phone (20,295 to 18,278) from word trims, and Options is 17% shorter on a laptop (9,039 to 7,498) and 12% on a phone (13,841 to 12,157), but the structure is the same |
| F5 | The green italic second headline line is on every headline | **Open (D8).** 10 of the 10 content headings on Home use it |
| F6 | Card grids repeat | **Open** (Session 7) |
| F7 | Proof is thin | **Partly.** The Our work page exists (8 renovation photos, 7 build photos, 2 closing photos); still no reviews, no Joey-confirmed gallery (the cold read also noted no dates, scope or whose projects they are); the safe way to ask for reviews is written (`lead-response-playbook.md`) |
| F8 | Form consent text had placeholders | **Partly.** No placeholders remain (checked Oct 21, 11:15 PM); the wording still needs an attorney, and the form is untested from here |
| F9 | Column balance (button 10 px under a list; sparse columns) | Not re-measured; the new screenshots show a sparse left column under the FAQ intro on a laptop, nothing broken |
| F10 | Glass effect used five times; two nearly opaque | **Open (D10)** |
| F11 | 22 different widths in the CSS | **Worse:** 30 widths in 73 blocks (the older-phone and large-text fixes added more). Session 5, with `tools/computed-diff.py` to prove nothing changes |
| F12 | Photos are about 800 px | **Open, waiting on Joey's originals.** The hero now has a 1200 px and a 1600 px version, made from the same 800 px source, so it is smoother, not sharper |
| F13 | Unused count-up code | **Done** (removed) |
| F14 | Launch plumbing missing | **Parked** by Jeremy (and still true: `noindex`, no sitemap, robots file, canonical or custom 404 page) |
| F15 | Manual accessibility pass; menu links 36 to 37 px | **Partly.** 44 px targets on phones, text-size and large-letter tests added; the manual keyboard and screen-reader pass is still not done |

## New findings

Priority: **P0** = the site should not go public without it; **P1** = a clear gain in trust or sign-ups; **P2** = polish or upkeep. "Needs" says who has to move first. Anything that changes copy, layout or scope waits for Jeremy.

### Trust and proof (the biggest gap)

| # | Pri | Finding | Fix | Size | Needs |
|---|---|---|---|---|---|
| N1 | P0 | **Nothing says how GLP sets an offer or how it earns money.** "A fair cash offer" (Home, Options) has no explanation, which is one of the phrases wary sellers already distrust, and "what's the catch?" goes unanswered. | A plain box on Options ("How we figure our offer, and how we make money") with a one-line version in the FAQs. Only what is true on every deal. | S once answered | Joey (Round 2, items 13 and 14), then Jeremy's yes |
| N2 | P0 | **Nothing says what happens after "yes."** No line on who buys (GLP's own money?), who closes, what you sign, what a seller can still change and until when. Our "no obligation" is correctly about the first conversation; a seller will ask about the contract. | A "What happens after you say yes" section (steps, who closes, how long an offer stays open, what you can still change) and a short list of promises GLP keeps on every deal. | S to M | Joey (items 15, 16), compliance answers 1 and 2, an attorney's glance |
| N3 | P1 | **The two numbers the site's trust rests on are Joey's to confirm:** the net sheet's example offer (85% of the sale price) and the wording "no fees," "we pay the closing costs" and "Commission and fees $0." Sources we read say cash offers often land well below market value (one agent's blog says 70 to 95%; HomeLight says investors typically offer about 70% of after-repair value minus repairs; both are vendors). If GLP's real offers are lower than the example, the "about $7,000 more by listing" gap would look smaller than a seller will meet. | Confirm Joey's real range and what the seller still pays at closing; adjust the example or show a range, and word "no fees" to match every closing statement. | S | Joey (items 13, 14); `CONTENT_CLAIMS.md` rows 6 and 38 |
| N4 | P1 | **Joey and Ethan are first names only,** with photos and values but no biography: no last names, how long in Chattanooga, what each does, how long in real estate or building. Only 22% of people read About pages in full or mostly (2002 survey), so names also belong in every footer. | Full names (their choice) and two or three true sentences each; repeat names with the phone number in the footer. | S | Joey, Ethan (item 17) |
| N5 | P1 | **The only address is a PO box,** and no place is named where sellers meet. Wary sellers look for a real address; Google's rules do not accept a PO box as a business address. | Label the PO box "Mailing address," say what is true ("we come to you" or a real meeting place), and decide the address once before any Google listing. | S | Joey (item 18) |
| N6 | P1 | **The service area is vague** ("surrounding counties," "generally within about an hour, in Tennessee and Georgia"), and a seller in a border county cannot tell. **Several classic seller questions are not answered:** can you buy with a mortgage, liens, back taxes or a tenant; what if the house is in probate or has several heirs; what do I need to do or sign; what if I say no. | The real list of counties and towns; four or five more FAQ answers written from Joey's real experience. | S to M | Joey (item 4 and a short call) |
| N7 | P1 | **No "What to ask any buyer, including us" checklist.** The consumer advice we read says to ask exactly these questions; with no reviews, it is the strongest honest proof we can give, and it is easy to share in a text. | A short page or section with ten questions (draft in the private B report), after N1 and N2 are answered. | M | Joey's answers to N1 to N3 |
| N8 | P1 | **"Bring your own expert" names an attorney or title company** but not a free HUD-approved housing counselor, an agent's opinion or "bring someone you trust to every call." | Add those lines. Re-check any counselor phone number or link before publishing (the Tennessee Attorney General page we found dates from 2019). | S | Jeremy's yes |
| N9 | P1 | **No reviews anywhere, and the clock has not started.** 97% of people read local reviews and 47% skip a business with fewer than 20 (BrightLocal 2026, a vendor); reviews take months. | Start the safe review request in `lead-response-playbook.md` with the first real past sellers; decide with Jeremy whether to un-park only the Google Business Profile so reviews have a home. Show no stars or counts until they are real. | S to start | Jeremy (D15), Joey |

### Getting from "interested" to "calling"

| # | Pri | Finding | Fix | Size | Needs |
|---|---|---|---|---|---|
| N10 | P1 | **Nine different button labels open the same contact form** (Get my options, Request a free consultation, Talk through your situation, Go over these numbers, Ask for an offer, Talk it through, Tell us about it, Send us a few details, Talk to Joey or Ethan). Home's main button says "Request a free consultation": the one corporate phrase on a plain-spoken site, and it leans on the unconfirmed word "free." The cold read also found that "consultation" can sound like paying a professional. | One main label ("Get my options") wherever the button opens the form; keep a different label only where it adds meaning ("Go over these numbers" after the net sheet, "Ask about this home"). Test it against "Send details" in the reading test with older readers instead of guessing. | S | Jeremy (copy) |
| N11 | P1 | **The phone number is not visible text in the laptop header.** The header shows "Get my options" and a Facebook icon; the number sits behind "Call or text us." About 1 in 5 adults 65 and over has no smartphone (Pew, 2026), and independent buyer pages put the number up front. **On a phone it is no closer:** the first time the digits appear in text on Home is 13,652 px down an 18,278 px page (75%), on Options 9,500 of 12,157, on Our work 7,850 of 9,302 (measured; before that, only the "Call or text us" buttons). | Add "(423) 451-5707" as plain text next to the header button on laptop and tablet widths, and just under the hero buttons (or at the top of the Menu) on a phone. | S | Jeremy (design) |
| N12 | P1 | **The contact form** is third-party, requires phone and email, makes no promise about reply time and is untested (from `ROADMAP.md`, item 2, and `research/ghl-form-style.md`). The research says to ask for name and phone first, accept any phone format, and promise only a reply time that can be kept. | Restyle with the prepared CSS; require only name and phone; set the alerts; state the reply time Joey can keep. | M | GoHighLevel access, Joey (item 19) |
| N13 | P1 | **The pages are long, and the longest is the one most visitors see first.** Home is 18,278 px on a phone. Research points the same way: one job per first screen, question headings, an "On this page" list on long pages (Options has one; Home does not). | D7 ("The numbers" on its own page), trim the Home FAQ, fold "How it works" into the option cards. Target for Home about 14,500 px on a phone. | M | Jeremy (D7) |
| N14 | P2 | **The net sheet cannot be printed or saved,** and families deciding together (an inheritance, a divorce, an adult child helping a parent) often do it on paper. A phone or browser print of the page today includes the whole page. | A "Print my numbers" button and a print layout for the net sheet. The math stays tested. | M | Jeremy (moves D11 item up) |
| N15 | P2 | **The "Common situations" chips under the Home hero look tappable but are not.** | Make them links (to Options or Contact), or show them as plain text. | S | Jeremy |

### Accuracy, rules and housekeeping

| # | Pri | Finding | Fix | Size | Needs |
|---|---|---|---|---|---|
| N16 | P1 | **The Privacy Policy says "We respect 'Do Not Track' signals,"** and says cookies are used "to understand how visitors use the site." Nothing in our code reads that signal, the third-party form script is outside our control, and there is no analytics today. A visible "Draft for review" note also sits on both legal pages. | Remove or verify the Do Not Track sentence and fix the cookie wording with the attorney's review; remove the draft note only after that review. | S | Jeremy (legal pages are not changed without him), attorney |
| N17 | P2 | **Dated wording will go stale:** "A closing from this fall" (Home, About, Our work, 3 places) and "Closed · September 2026." Winter starts Dec 21. There is no "last reviewed" date on Options or the net sheet. | Swap to "Closed in September 2026" wording before Dec 21; add "Last reviewed October 2026" to Options and the net sheet. | S | Jeremy |
| N18 | P2 | **No custom 404 page, robots file or sitemap.** A mistyped link shows GitHub's plain page. | A friendly 404 page now (safe); robots and sitemap with the launch bundle. | S | Jeremy (small) |
| N19 | P2 | **The Facebook link is a numbered address** (`profile.php?id=...`). | Joey can claim a short Facebook name in the page's settings; then the link is easier to say and to trust. | S | Joey |
| N20 | P2 | **The notes are in a public repository.** The notes and research name weak spots in our own claims and wording. Rules research is already kept out (`.gitignore`), and so is the raw research in `research/private/`; `PROJECT_STATUS.md`, `SESSION_HANDOFF.md` and the earlier reviews are public. | Before `noindex` is removed: move internal notes to a private repository or folder, or keep this repository private (GitHub Pages from a private repository needs a paid GitHub plan; checked Oct 22). | S to M | Jeremy (D12) |
| N21 | P2 | **CSS has grown to 73 media-query blocks at 30 widths,** and `PROJECT_STATUS.md` to 135 KB. Both slow every future change. | Session 5 (four widths, proven by `tools/computed-diff.py`); move old checkpoint notes to an archive file and keep a one-page status. | M | Jeremy (go) |

### Added after the cold read (each one checked by me against the pages)

| # | Pri | Finding | Fix | Size | Needs |
|---|---|---|---|---|---|
| N22 | P1 | **The situations the "Common situations" chips promise are not answered.** The first chip is "Inherited homes," but probate, estate, executor, heir, deed, documents, paperwork, remote, notary and "out of state" appear on no page (I searched all 8). "Financial stress" is a chip, but foreclosure, "behind on payments" and "late notice" appear nowhere, and "Keep the home" suggests refinancing or renting it out. Tenant, landlord, lien and back taxes are missing too. A cold reader in each situation could not tell whether GLP could help or what to do first. | Short, plain answers on the pages we already have (not new pages): who can sign for an inherited house, whether a seller can sell before probate ends, whether an owner in another state can sign remotely, what happens to belongings ("no cleaning" is ambiguous), what to do about a late-payment letter, what happens to a tenant. Write only what Joey really does; have an attorney glance at it; point to an estate attorney and a HUD-approved housing counselor. | M | Joey (new item 21), an attorney's glance, Jeremy's yes (D13) |
| N23 | P1 | **The site presents itself as a neutral guide, but it is also the buyer.** "Our goal isn't to buy your house" (Home, Our story), "Most companies push one answer. We show you all of them," and "Homeowners usually hear two choices: list with an agent, or sell to an investor for less than the house is worth," while "Sell directly to us" comes first in the option lists on Home and Your options and the site's own table says a direct sale "usually brings in less than a perfect listing." A wary reader can see that GLP is the investor. The honesty is there; the framing can look like a dodge. | Say it once, in plain words ("We're a buyer too, so we have a stake. Here is how we earn, and how to check any offer, ours included"); soften "our goal isn't to buy your house" to what is true; keep the compare table exactly as it is. Pairs with N1. | S | Jeremy (copy), Joey (N1 answers) |
| N24 | P1 | **One closing carries the whole site.** The September closing is the only story. The FAQ answer "Can you help me figure out where to go next? Often, yes" rests on that single sale ("In a recent sale…"). The story's headline, "35 years of put-off repairs," can read as judging the sellers if they see it. The photo caption does not say who is pictured. | Ask the sellers and Joey to approve the headline and photo; reword "Often, yes" to what one sale supports until there are more; add a seller quote only with permission; say who is in the photo. | S | Joey and the sellers (item 2), Jeremy |
| N25 | P1 | **Your options has no person on it.** Joey and Ethan are not named on that page (0 times) and no photo of them appears, on the page that holds the biggest money claims. The two most honest sentences are also set small: "The trade: a direct sale usually brings in less than a perfect listing" and "A real offer depends on the home. We make it after we see the house." are 14 px; body text is 16 to 17 px. | A face and "Questions? Joey or Ethan will answer" near the top; set both honesty lines at body size (their contrast is fine, about 6.5 to 1). | S | Jeremy (design) |
| N26 | P1 | **The phone number splits across two lines on phones.** "(423) 451-" ends one line and "5707" starts the next, in the "Form not loading? Call or text…" line on Home and Contact, at phone widths of 360, 375, 390 and 430 px (not at 412). At 320 px the "Call or text (423) 451-5707" button splits it on Options, Our story, New homes and Our work. A broken number is easy to misread, on the one thing a nervous visitor needs. | Keep the number on one line (non-breaking hyphen and space, `white-space: nowrap`) and let the words around it wrap. Re-test at 320 to 430 px. | S | Jeremy (D14) |
| N27 | P1 | **The net sheet leans a little toward a cash sale.** Three small things, each defensible alone. (1) A 6% commission is probably at the high end: Redfin's national figure for the buyer's agent alone was about 2.4 to 2.5% in 2025, and the seller's own agent is paid separately, so the total depends on that agent's rate; a local agent's quote should settle it. (2) "Monthly cost while listed" counts the whole house payment, but the part that pays down the loan comes back at closing. (3) The cash-sale side counts $0 for the 7 to 14 days it takes to close, though the same bills continue (about a third of a month, $630 at the default $1,800). Together they favor a cash sale by roughly $2,000 to $3,000 of the example's $7,000 gap (commission at 5.5% alone is $1,500). The example still favors listing, but a seller who prices it with a local quote may notice, and this is the page's main trust tool. | Count waiting the same way on both sides; relabel the hint ("interest, taxes, insurance, utilities"); ask Joey and a local agent what to use for commission; add a break-even line ("In this example, a cash offer above about $262,000 beats listing"), so a seller can test any offer, ours or anyone's. Re-run `netsheet-test.py` to the dollar. | M | Jeremy (D16), Joey (item 22) |
| N28 | P2 | **More for the attorney on the legal pages.** The Privacy Policy (section 5) says "If you opt in, we use your phone number to text you," while the Terms (section 6) say "When you give us your phone number, you agree to receive text messages…, possible offers." Both should match the form's consent box and the registered text campaign. "PO Box 55, Hixson, TN" has no ZIP anywhere, including the Privacy Policy's contact line. Terms section 5 says "We do not promise that any of the materials are accurate, complete, or current," which sits oddly beside our promise of honest numbers, and section 9 ("exclusive jurisdiction of the courts") is heavy for homeowners. This is standard-form wording; the attorney decides. | Give the attorney this list with N16; make the three texts agree; add the ZIP once Joey confirms the box. | S | Attorney, Joey (item 18), Jeremy |
| N29 | P2 | **New homes copy pushes while the rest of the site says "no pressure."** "Ask about getting in before it's listed" appears 4 times (Home once, New homes three times) and "Tired of crazy prices?" 3 times, and the page says both "Coming soon" and "Now building." No address or neighborhood, completion month, plan or rendering, builder license or warranty is given. | Soften to "Want to see it before it's listed? Ask us"; use one status label once Joey confirms it; add the facts that are true (completion month; license and warranty, if any); name the down payment assistance program Joey means, or drop "Ask us how down payment assistance could help"; ask whether "crazy prices" is Joey's own phrase to keep. | S | Joey (item 23), Jeremy (tone) |
| N30 | P2 | **A few terms are used without a definition:** "net sheet" (the nav says "The numbers," the footer "Compare & net sheet," the button "Run the net sheet"), "closing," "title company," "refinancing" and "A cash offer to compare." The site already defines "as-is" and "seller financing" well. "Guides, not gurus" may not land with older readers. | One plain line at first use for each (for example, "closing: the day the sale is final and you get paid"); a plainer name than "net sheet" in visitor-facing words (such as "What you'd keep"); try it in the reading test. | S | Jeremy (copy) |
| N31 | P2 | **Small polish a visitor can see.** (1) "Meet Joey & Ethan" sits almost touching its paragraph on Home (about 3 px below the last line of text; every other button on the page has 20 to 67 px on a phone). (2) "short-term" breaks across lines at its hyphen in two places on Home. (3) On Our work, the "Before and after" tile has a squared white edge while the others are rounded. (4) In the kitchen-table photo the person at the right edge is cut off by the frame (seen on a phone; the helper saw it on a laptop too). (5) By design the hero buttons start to fade in at 0.74 s and finish at about 1.5 s, so on a slow phone there is an empty gap where the main action will be. (6) If the form script cannot load (an ad blocker, a weak signal), a visitor sees a blank white box about 760 px tall, with the "Form not loading?" line just under it. (7) About 10 to 12% of Home's text on a phone is about 14 px or smaller (labels at 12.5 px, chips at 13 px, fine print at 14 px; the "HOME OPTIONS" line in the logo is 9.3 px); body text is 16 to 17 px. | One short polish session with the bundle: fix the spacing and the hyphen; check the tile edge and the crop against Joey's originals; start the button row earlier; if no form has appeared after a few seconds, show the fallback line (and the call and text buttons) inside the empty box; leave the small sizes for the reading test to judge. | S | Jeremy (D14) |

## What I would protect

- The compare table and the net sheet, including "Trades some price for speed and certainty," and the default example in which listing nets more.
- "Honest about fit," "bring your own attorney or title company," and the stance "sometimes the right answer isn't us."
- The people-first hero, the named founders, and the call or text option on every page.
- Plain words (about grade 4 on our yardstick; the legal pages about 7.6) and the question-style FAQ.
- The light pages and the safety nets (no page stays blank if a script fails).
- Not inventing proof: no counts, stars, badges, awards or press logos. We use none of the "spam signals" the research lists, with one exception: "a fair cash offer" is not yet explained (N1).
- The Contact page's big Call, Text and Email tiles, the "Form not loading?" fallback line, and one phone number used everywhere (the same on all 8 pages).
- "A conversation, not a contract" and "Do I have to decide on the first call? No."; the "A good fit if / Maybe not if" boxes; no urgency banners, countdown timers or address-first forms.
- Real, unpolished job-site photos (they read as genuine; a cold reader said so too).

## What four first-time visitors made of it

*Made-up people, played by one helper who had not seen our notes. Their guesses about what they would do are guesses, not data. I checked every factual claim below against the pages.*

**The five-second test (Home).** A stranger can say the name and the place, that two named, smiling men run it, that it compares ways to sell (to GLP, with an agent, or keep the house), "plain English, no pressure," and what the two buttons are. A stranger cannot say whether GLP buys houses for cash, how fast or at what cost (the first card that says so is about 1,500 px down on a phone), the phone number, who Joey and Ethan are beyond first names, or anything that proves GLP is real.

| Visitor | What helped | What the site did not answer | Likely first move (a guess) |
|---|---|---|---|
| **Ruth, 71,** Hixson, an inherited house in Red Bank, iPhone, nervous | Faces and "Hixson" under them; "No pressure"; "We live and work in Chattanooga, same as you"; "The first conversation is free"; "have your own attorney or title company review anything" | Who they are (no last names, years or license); what to do first with an inherited house; what makes an offer "fair"; what "net sheet" and "title company" mean; the number is far down the page | Call, not the form |
| **Marcus, 44,** night-shift aide, behind on the mortgage, Android, a 20-minute break | "7–14 days"; Text in the bottom bar; "No pressure, no scripts"; "There's no judgment here" (deep in Options) | Nothing about being behind, a foreclosure letter, how fast an offer follows a first contact, or what he would keep; "Call or text anytime" promises no reply time | Text from the bar |
| **Dana, 38,** settling her mother's estate, brother out of state, laptop, evening | The three steps; "You pick the closing date"; "no repairs, no cleaning, and no showings"; Book a call; Options is good enough to send her brother | Documents, probate, who must sign, signing from another state, what happens to belongings, who runs the closing and who pays them | Email or book a call; send her brother the Options link |
| **Tom, 52,** rental with tenant damage, laptop, skeptical | The arithmetic checks ($112,000 by listing against $105,000 selling to GLP); the example where listing wins; "Maybe not if" | How an offer is figured (the sheet takes an offer as an input, it never derives one); what "we pay the closing costs" covers; tenants and damaged units are not mentioned; how many homes GLP has bought | Bookmark the sheet, then ask one pointed question |

**What all four ran into:** who these people are, provably; how an offer is figured and how GLP earns; a very long Home page; and legal pages that still say "Draft for review," which a wary visitor can read as "not finished."

**Where I checked, or disagreed with the helper.**

- **Confirmed.** Probate, estate, executor, heir, deed, document(s), paperwork, remote, notary, "out of state," foreclosure, tenant, landlord and lien appear on no page. Joey and Ethan are not named on Options. The first digits of the number are 13,652 px down Home on a phone. The number splits across lines (N26). The two legal pages word the text-message consent differently, and no ZIP is given. New homes has urgency lines and two status labels. "Sell directly to us" is first in the option lists on Home and Your options. "Often, yes" rests on one sale. The net sheet's arithmetic adds up. About 10 to 12% of Home's text on a phone is about 14 px or smaller (10.5% at 14.0 px or less, 12.5% counting the 14.1 px fine print).
- **Corrected.** "Lender" does appear twice (a line on Options that says to talk with "a lender or advisor," and a down-payment line on New homes), though not in a way that helps someone who is behind on payments. The form box is about 760 px tall, not over 850.
- **Already on our list.** The share-card address (github.io) differs from the canonical address (glphomeoptions.com); both are switched at launch (`ROADMAP.md`, Session 13).
- **Not seen by the helper.** The contact form, the booking calendar, Facebook, the opened phone menu, the enlarged-photo view on Our work, an enlarged-text view and page speed.

## Not verified

- A real phone or tablet, and real Safari on an iPhone (our cloud has only Chrome's engine).
- Keyboard-only and screen-reader use.
- The contact form: how it looks inside our page, what happens after "Send," where leads go, and its real speed.
- Speed on the live site with the real form script, and on a slow connection.
- How actual visitors, and older visitors in particular, read and react (the research has no test for this audience; the four made-up visitors are an informed guess, not a test).
- Whether the net sheet's default numbers match what a Chattanooga agent quotes today (N27): the research gives national figures only.
- Google's own ranking, ads and map results for Chattanooga searches. Our search tool is not Google.
- Joey's confirmation of every claim and photo (`CONTENT_CLAIMS.md`).

## What I would do first

1. **A short call with Joey** on the Round 2 questions (items 13 to 23 in `questions-for-joey.md`), plus the five already queued. These unlock N1 to N7 and N22 to N24, and they are the gap that matters most.
2. **Jeremy's decisions** D7 to D16 in `ROADMAP.md` (one message: "go with your recommendations," or name the exceptions).
3. **The small, safe bundle** once Jeremy says yes (D14): one main button label, the phone number in the laptop header and under the phone hero buttons, the number kept on one line (N26), links or plain text for the situation chips, a custom 404 page, "last reviewed" dates, the honesty lines at body size, and the small polish in N31.
4. **Net sheet round two** (D16): count both sides the same way, add the break-even line, a plainer name, and a print layout. The math stays tested to the dollar.
5. **Home and Options diet** (D7), then the heading-signature trim (D8).
6. **The trust pack's copy** (D13, N1 to N8 and N22 to N24) as Joey's answers arrive, each part checked by an attorney where it makes a promise.
7. **The real-phone pass and a reading test** with 3 to 5 people aged 60 and over, who say what each page means in their own words (and try "Get my options" against "Send details").
8. **Session 5,** the CSS consolidation, with before-and-after proof that nothing changed.
9. **The contact form** (GoHighLevel access) and a real test lead.

## Sources for numbers quoted here that are not in `what-works-2026-10-22.md`

- Redfin, buyer's agent commission, Q2 2025 average 2.43% (up from 2.38% a year earlier): [Business Wire release, Aug 2025](https://www.businesswire.com/news/home/20250812345440/en/Buyers-Agent-%20Commissions-Tick-Up-to-Pre-NAR-Settlement-Levels).
- Redfin, buyer's agent commission, Q3 2025 average 2.42% (2.52% on homes under $500,000): [Inman, Dec 2025](https://www.inman.com/2025/12/08/buyers-agent-commissions-see-rebound-in-wake-of-settlement/). Neither source gives the listing agent's share or a total.
- GitHub Pages "is available in public repositories with GitHub Free … and in public and private repositories with GitHub Pro, GitHub Team, GitHub Enterprise Cloud, and GitHub Enterprise Server": [GitHub Docs, Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
- Everything else (Pew, BrightLocal, HomeLight and the rest) is listed with its link in `what-works-2026-10-22.md`.
- Page measurements (phone number positions and line breaks, type sizes, spacing, form box height) are mine, from a headless Chromium on a local copy of the site.

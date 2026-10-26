# GLP Home Options: site map and launch plan (a proposal)

**For:** Jeremy first, then Joey once Jeremy is happy with it. **Written:** Oct 22, 2026, overnight (Session 6g).
**Status: PARKED for later.** Jeremy, 1:02 AM Oct 22: "let's not go too crazy for SEO and launch plan stuff ... keep it focused on making this website pristine before we do that, that's later on." This file is a reference so the thinking is not lost. Nothing in it is built, nothing here changes a live page, and no one should work on the search or launch parts until the site itself is pristine and Jeremy says go. The page-structure ideas (S2 to S4, section 7) are proposals that need his yes.
**Not legal advice.** Anything about laws, licenses or rules below is a *question to ask a Tennessee attorney*, with the source I found. I am not a lawyer, and most sources are summaries by other people.

You asked me to think about the whole site as a UX designer and as a marketer, so it can become a live business website soon. This is that thinking, in one place.

> **Parked part (Jeremy, 1:01 AM Oct 22):** "lets not go too crazy for SEO and launch plan stuff ... keep it focused on making this the best website possible before we do that, that's later on." So **sections 1 to 9 (the pages, the menu, Home, the ways in, trust and proof) are the working part: they are about the site itself.** **Sections 10 to 13 (search, the Google listing, switching the domain, the attorney questions, the launch checklist) are written down for later and are not being worked on.** No Docs page was published and nothing was built from this file.

---

## 1. The short version

1. **The site is close.** It is fast, clean on phones, honest about the numbers, and it shows real faces. That is the right kind of site for people who are nervous about "we buy houses" ads.
2. **Four things stand between it and live, and none is a design problem:**
   - **Things only Joey can confirm:** whether the photos are his and may be shown, whether either of them holds a real estate license, the claims tagged "J", which counties they cover.
   - **The contact form and texting set-up inside GoHighLevel:** the form's look, its consent wording (it still has placeholder text), and the text-message registration.
   - **Switching glphomeoptions.com over.** The domain still shows the *old* GoHighLevel site today (section 10).
   - **A short list of questions for a Tennessee attorney** (section 11).
3. **Keep the launch small.** The 8 pages we have, plus three small "plumbing" pages (a thank-you page, a "page not found" page, and a redirect so the old `/calculator` link keeps working). Add more pages only when Joey can fill them with true things.
4. **The best structural change is giving the net sheet its own page** (decision D7, parked) and slimming Home. The old site already had a `/calculator` page, so people already look for it there.
5. **The cheapest trust gains are not design:** a short guide called "How to check any cash buyer, including us"; a "check us out" box that points to the state's business record; real Google reviews; one 60-second video of Joey and Ethan.
6. **Be realistic about traffic.** For the first months most visitors will come from Joey's own network (Facebook, texts, word of mouth) and from a Google Business listing, not from search rankings. So the site's first job is to *turn someone who half-trusts you into a phone call*.

## 2. Decisions I need from you

"Go with your recommendations" is a fine answer. Each one is a separate step, so you can approve or reject it by commit.

| # | Decision | My recommendation | Effort |
|---|---|---|---|
| S1 | Launch scope: the 8 pages plus a thank-you page, a "page not found" page and a `/calculator` redirect | Yes | Small |
| S2 | Rename "Our story" to "About" in the menu, breadcrumb and page title (the headline stays) | Yes. It is what people look for, and the old site used `/about` | Tiny |
| S3 | **D7:** the compare table and net sheet on their own page ("The numbers") | Yes, before launch. If not, at least the `/calculator` redirect to the net sheet on Home | Medium |
| S4 | Home diet: (a) fold "How it works" into the option cards, (b) move the panoramic photo band into About, (c) cut the Home FAQ to 6 or 7 questions, (d) stop About and Home repeating each other | Yes to all four, as four small steps | Medium |
| S5 | Put a click-to-call back in the desktop header (it was removed at Checkpoint 12 for room) | Yes, on wide screens only, if it fits | Small |
| S6 | Keep "New homes" in the main menu | Yes for now. It is real, and it shows they build. Revisit with data | None |
| S7 | Situation pages after launch (inherited home, divorce, needs repairs, behind on payments, moving, landlords): which two or three first | Joey picks the ones he has really handled | Content from Joey |
| S8 | Add simple, privacy-friendly analytics (calls, texts, form, booking) | Yes at launch | Small |
| S9 | Who controls the domain registrar and the GoHighLevel account, and who picks the switch-over day | Joey and Jeremy together | Decision |
| S10 | A 60-second intro video from Joey and Ethan | Ask Joey. Only if he wants to | Joey's time |

## 3. Who it is for, and the one job it has

**Who** (your words, Oct 21): ordinary homeowners who are short on money and time and wary of "we buy houses" ads. Many arrive stressed, on a phone, often late in the day. Some are dealing with an inheritance, a divorce, a move, a house that needs more repair than they can pay for, or payments they can't keep up.

**The one job:** get them to talk to Joey or Ethan with as little fear as possible. In order of preference: **call, text, a short form, a booked time.**

**What a worried seller needs to learn in about ten seconds** (every page should answer these):
1. Who are you? (names, faces, local)
2. Is this a scam? (proof, no pressure, ways to check)
3. What happens if I reach out? (three plain steps, no obligation)

## 4. What we have today

| Page | File | Job | Words in the main part | Notes |
|---|---|---|---|---|
| Home | `index.html` | Introduce, build trust, point to a path or a call | about 1,600 | Too long (about 12,100 px on a laptop, 18,100 px on a phone). It repeats Options. |
| Your options | `options.html` | Each way to sell or keep, with costs, fit and no-fit, FAQ | about 1,270 | Trimmed Oct 21 |
| Our story | `about.html` | Who they are and why to trust them | about 650 | Repeats some of Home |
| Our work | `work.html` | Photos: renovating, building, recently closed | about 240 | Photos not yet confirmed by Joey |
| New homes | `new-homes.html` | A second audience: buyers of the home they are building | about 460 | |
| Contact | `contact.html` | Call, text, book, form (GoHighLevel) | about 430 | The form still looks like a bolt-on |
| Privacy Policy, Terms of Service | `privacy-policy.html`, `terms-of-service.html` | Legal | about 510 and 430 | Need an attorney's read |

**The old site, live at glphomeoptions.com today** (I looked at it, nothing typed): Home, `/about`, `/options`, **`/calculator`** (a seller net sheet), `/contact`, `/terms-of-service`, `/privacy-policy`. Its page title is "GLP Home Options – Clarity & Choice for Homeowners", it is built on GoHighLevel, and I found no "do not index" tag, so search engines can see it. The new site covers every one of those pages except `/calculator`.

## 5. Proposed site map

```
Home
├─ Your options
│    └─ (later) Situation pages: inherited home · divorce · needs repairs · behind on payments · moving · landlords
├─ The numbers  (compare table + net sheet)           ← S3 / D7: its own page, recommended
├─ About  (today "Our story")                         ← S2
├─ Our work
├─ New homes
├─ Contact
│    └─ Thank you  (after the form; hidden from search)
├─ (later) Where we buy
├─ (later) Guides:  "How to check any cash buyer, including us"
├─ (later) Reviews  (real ones only)
├─ Privacy Policy · Terms of Service   (footer)
└─ plumbing: "page not found" page · /calculator redirect · sitemap.xml · robots.txt
```

| Page | When | Job | Needs from someone |
|---|---|---|---|
| The 8 pages we have | Launch | See section 6 | Joey's confirmations (photos, claims, license) |
| Thank-you page | Launch | Confirms the message went through, says what happens next, shows the phone number again, lets us count form sends. Hidden from search | **Changed at Checkpoint 46:** the new form shows its own "Thank you" panel in place and does not redirect, so this page is only needed if a separate page is wanted for counting sends. (It was written when the GoHighLevel form had to send people to it.) |
| "Page not found" page | Launch | A friendly dead end: "We can't find that page. Call or text, or go Home." | Nothing |
| `/calculator` redirect | Launch | The old net sheet link lands on the new net sheet | Nothing |
| The numbers (own page) | Launch if S3 is yes | The most useful and most shareable thing on the site | Your yes |
| Situation pages (2 or 3 first) | Within about 60 days | Answer one worried question each, in plain words, from real experience, with one clear call or text button | **Joey's real stories and answers** (I will not invent them) |
| Where we buy | After Joey lists his counties | A short list of counties and towns | Joey |
| Guide: how to check any cash buyer | Within about 60 days | Honest consumer help. Builds trust with exactly the people who are wary | Joey's OK and an attorney's read |
| Reviews | Only when real reviews exist | Real, unedited, with permission | Real customers |

**Deliberately left out:** a page for every small town (thin copies hurt more than they help), a weekly blog (nobody can keep it up), pop-ups and chat widgets (they cheapen trust), countdown timers and "only 3 spots left" (not the tone you chose), stock photos of happy families, "as seen on" badges, counters of houses bought.

## 6. Menu and page jobs

**Menu today:** Your options · The numbers · Our story · Our work · New homes · Contact, a Facebook icon, and a green "Get my options" button. On a phone there is a Menu button and a bar at the bottom (Call, Text, Get my options).

**Suggested:** same menu, with "Our story" renamed "About" (S2) and, if S3 is yes, "The numbers" opening its own page. In the footer, add "Where we buy", "Guides" and "Reviews" as they appear.

| Page | Its one job | One action at the end | Keep / change |
|---|---|---|---|
| Home | Make a stranger feel safe in 10 seconds, then show the four ways | Call or text | Slim it (section 7) |
| Your options | Let someone compare honestly and see themselves in "A good fit if" | "Run the net sheet" or call | Keep. Later, each option could get its own page if search data asks for it |
| The numbers | Show what a seller keeps, in their own numbers | "Want us to check these numbers with you?" (call, text) | Move off Home (S3). Never ask for contact info before showing the result |
| About | Put two real people in front of the reader | Call or text | Absorb the panoramic band from Home; end the repeats with Home |
| Our work | Proof | "See what we'd do with your house" | Add a line on what was done for each project once Joey confirms the details |
| New homes | Serve buyers | "Ask about the home" | Keep short. Fair-housing wording check (section 11) |
| Contact | The easy way in | Call first, then text, then the form | Calmer card, faces beside the form, three lines on what happens next (the planned "contact section on our side") |

## 7. Home: a shorter path

The earlier review found that Home repeats Options, so it is long because of its *structure*, not its sentences. A suggested order, built around the questions a visitor asks in turn:

1. **Hero:** the promise, Joey and Ethan, Call / Text / Get my options. (Keep as it is.)
2. **A strip of three plain facts** in Joey's words.
3. **The four ways,** as cards. "How it works" folds in here as one line per card (S4a).
4. **"What it might look like in numbers":** one example and a button to The numbers (S3).
5. **Proof:** three photos from Our work, the Facebook link, and real reviews when they exist.
6. **The people:** a short "meet Joey and Ethan" with a link to About (the panoramic band moves to About, S4b).
7. **FAQ:** six or seven questions (S4c). The full set stays on Options.
8. **Contact:** phone first, then the form.

The earlier review estimated this takes Home from about 13,000 px to about 9,500 px on a laptop and from about 20,000 px to about 14,500 px on a phone (before this week's trims). Each step is a separate checkpoint.

## 8. How people reach Joey and Ethan

| Path | What the visitor does | What must work | What to measure |
|---|---|---|---|
| **Call** | Taps the phone number | Someone answers or the voicemail is friendly. Who covers evenings? | Taps on the phone number |
| **Text** | Taps "Text" | The number can receive texts and someone replies the same day | Taps on Text |
| **Form** | Sends name and phone (and the address if they want to) | The form is short; it reaches *both* of them within minutes; the visitor lands on the thank-you page; consent wording is final; texting is registered (section 11) | Thank-you page views |
| **Book a time** | Picks a slot (calendar ID `cM59fR3vJlAVRy08Depz`) | The calendar sends a confirmation and a reminder | Bookings |
| **Net sheet, then call** | Runs their numbers, then calls | No contact info is asked before the result. No numbers are sent anywhere | Net sheet opens (a count only) |
| **Facebook** | Messages the page | Someone watches it | Not on the site |

**Speed matters more than design here.** A seller who fills in a form and hears nothing for a day has usually called someone else. That is common wisdom in this line of work; I did not verify it, but it fits how people behave when they are worried. So decide who watches the form notifications, and only promise a reply time on the site that Joey and Ethan can keep ("we reply the same day" only if it is true).

## 9. Trust and proof

**What is real today:** two named people with faces, a local base, a phone and email, a legal entity (GL Partners LLC), a Facebook page, builds in progress, one closing story, and honest numbers (the example shows listing netting more than a direct sale, which is the strongest trust move on the site).

**What to add, only when true:**
- **A "check us out" box:** "GL Partners LLC is registered with the Tennessee Secretary of State. You can look us up there." Inviting a check is a strong signal to a nervous reader. Needs Joey's OK and the exact registered name.
- **License or brokerage line,** if either of them has a license (section 11).
- **Real Google reviews.** After each closing, send the customer a direct link to leave a review. Never pay for one, never ask only the happy ones (section 11).
- **A short "what we won't do" list in Joey's own words** (no pressure, no surprise fees, whatever he really stands behind).
- **The guide "How to check any cash buyer, including us"** (below).
- **A 60-second video** from Joey and Ethan, phone-shot is fine, with captions. For this audience, hearing two real people say it plainly may do more than any redesign.

**The guide, in outline (all general consumer advice; Joey and an attorney should read it):** ask who is actually buying (the company, or someone who will pass your contract to another buyer); ask how they pay; get the offer in writing with every cost and who pays it; have your own attorney or title company read it before you sign; never be rushed; be careful with anyone who wants money from you up front; look up the business on the state's record; compare with a listing using a net sheet. It ends with "we will answer all of these for you, too."

## 10. Search, the Google listing, and switching the domain

### Search (realistic)
Big national "we buy houses" companies dominate the main search terms in a town like Chattanooga, and a new site takes months to be noticed. So do the groundwork once, correctly, and do not count on search early.

**Already good:** one H1 per page, descriptive image text, fast pages, mobile-friendly, structured data for the business, a share card.

**To fix or add at launch (technical):**
- The "do not index" tag (`noindex, nofollow`) comes off every page on launch day. Not before: Joey has not confirmed the photos or claims yet.
- Each page already names `glphomeoptions.com` as its preferred address (canonical), but the share-card tags and the structured data still point at the temporary `jsglisson3.github.io` address. Switch them to the domain on launch day.
- Add `sitemap.xml` and `robots.txt`, and register the site with Google Search Console.
- The Home page description is 259 characters; Google shows about 155. Suggested (same facts, nothing new): *"Joey and Ethan help Chattanooga homeowners compare every option: sell as-is, list, or keep the home. Local, no pressure. Call or text (423) 451-5707."*
- Add the thank-you page, the "page not found" page and the `/calculator` redirect.

**Words people actually use:** "sell my house fast", "sell house as-is", "cash offer", "inherited house", "behind on mortgage", "divorce and the house", "can't afford repairs". The plain-talk pass already moves the page text toward these words, and the situation pages use them in their headlines.

### The Google listing (Google Business Profile)
This is probably the most useful free tool for the first months. GLP visits the homeowner (one visit), so it fits Google's "service area business" type: you hide the street address and list the area you cover.
- **Google does not accept a PO box or a rented mailbox as the address** (their guidelines say so). The site shows "PO Box 55, Hixson, TN". A listing needs a real, private address to verify; it stays hidden from the public. Does Joey or Ethan have one (an office or a home office)?
- Keep the business name, phone and area wording the same on the site, Google, Facebook and anywhere else (consistency matters for local search).
- Pick the closest official category in Google's list when setting it up (the list changes, so choose in the dashboard).
- Service areas should stay within about two hours' drive of the base (Google's guideline), which fits "about an hour from Chattanooga".

### Measuring
Add one simple, privacy-friendly analytics tool at launch (a tool that does not use cookies is simplest; the Privacy Policy must mention whatever is used). Count: taps on the phone number, taps on Text, thank-you page views, bookings, net sheet opens (a count only, never the numbers). Look once a week: how many calls, texts and forms came in, and from where (use a simple tag on the Facebook link).

### Switching the domain (technical, but you should know the plan)
**Today:** `glphomeoptions.com` shows the old GoHighLevel site. The new site is only at `jsglisson3.github.io/GLP-Home-Options/` (hidden from search).

1. **Before the switch:** the whole new site is tested on the temporary address, including the form on a real iPhone and a real Android phone. Joey has approved. The attorney questions are answered. Texting is registered, or text consent is left out for now.
2. **A day before:** lower the domain's "time to live" setting (so a mistake can be undone quickly). Check that email records are not touched.
3. **Switch day:** in the repository's Pages settings add the custom domain (GitHub adds a `CNAME` file). At the domain registrar: four `A` records for the main address pointing to GitHub's addresses, and a `www` record pointing to `jsglisson3.github.io` (GitHub's guide lists the exact values; keep the email records). Then turn on "Enforce HTTPS" once GitHub offers it (it can take up to a day).
4. **Same day in the site:** remove `noindex`, switch the share-card and structured-data addresses to the domain, add the sitemap and robots files, and add the redirect for `/calculator`.
5. **After:** check HTTPS, the `www` address, every link, the form, call and text links, the share card (Facebook's sharing debugger), and Search Console. Old addresses `/about`, `/options`, `/contact`, `/terms-of-service`, `/privacy-policy` should open the new pages (I believe GitHub Pages serves `about.html` at `/about`; **test it** after the switch).
6. **Undo plan:** point the records back to the old setup. This is why step 2 matters.
7. **Ask Joey first:** does anything in GoHighLevel (email links, review links, the calendar, trigger links) rely on the pages at `glphomeoptions.com`? Once the domain points to GitHub, those GoHighLevel *website* pages stop showing. The form and calendar addresses at `links.voiseai.com` keep working.

**Ownership:** the site's code lives in Jeremy's personal GitHub account. That is fine to start. Later, consider moving it to a GitHub organization for the business, or at least giving Joey access, so the business does not depend on one person's account.

## 11. Questions for an attorney, and wording to double-check

These are flags, not conclusions. Sources are in section 14.

| # | Topic | What I found | Why it matters here | Question |
|---|---|---|---|---|
| C1 | **Tennessee wholesaling law (2025)** | The Tennessee Real Estate Commission's Spring 2025 newsletter says wholesaling is allowed if the buyer (1) tells the possible assignee about their equitable interest in writing and (2) tells the seller at least three days before assigning the contract that they intend to wholesale. It says the governor signed it March 25, 2025, effective on signature. The bill's record shows it as Public Chapter 72. **I have not read the enacted text, and the newsletter does not mention penalties.** | If GLP ever sells its right to buy a house to someone else, or advertises a house it has under contract but does not own, this applies. If it always buys in its own name and closes, it probably does not, but that is for an attorney to say. | Does GLP always buy in its own name? Ever assign a contract? Does the site's wording match what GLP really does? |
| C2 | **Real estate license** | The site says "List with an agent". The Tennessee rule on personal interest says all licensees must identify themselves as licensees when buying or selling property for themselves. A local Realtor association's summary says ads by licensees must show the firm name and phone number, and that a website must show the firm name and phone number prominently on every page. Joey's videos say "New Listing coming soon". | If either person is licensed, the footer, About page and the "List with an agent" wording may need a license and brokerage line. If neither is licensed, "List with an agent" must be clear that GLP refers people to an agent (and who). | Is either of them a licensee? Who is "the agent"? |
| C3 | **Reviews and testimonials** | The FTC's rule on fake and misleading reviews took effect Oct 21, 2024. Summaries say it covers fake or misattributed reviews, paying for reviews, undisclosed insiders' reviews, hiding negative reviews, and showing only favorable ones as if typical. Penalties are over $50,000 per violation (adjusted each year). | We show no reviews today, which is right. When reviews exist, they must be real, from real customers, not paid for, with any relationship disclosed. | How should we collect and show reviews? |
| C4 | **Business name** | "GLP Home Options" is not the legal name (GL Partners LLC). FindLaw says a Tennessee LLC using another name registers an "assumed name" with the Secretary of State ($20; renew every 5 years). | The name appears on the site, Google, Facebook and the phone. | Is "GLP Home Options" registered? |
| C5 | **Texting** | To text people from GoHighLevel, carriers require a brand and campaign registration (called A2P 10DLC). Rejection reasons include: no visible text opt-in or privacy policy on the website, a business name that does not match, and sample messages with no "Reply STOP". Brand approval can take a day; campaigns a few days to a week; costs are small. | Our site has a Terms page that covers texts and a form whose consent text still has placeholders. | Who registers? Is the consent wording final? |
| C6 | **Consent to be texted** | The form's consent wording still has `[BUSINESS NAME]` placeholder text and example links (a known launch blocker; needs GoHighLevel access). | Text-message rules (TCPA) are strict about consent. | What wording should the form use? |
| C7 | **Fair housing wording** | The New homes page says the home is "for first-time buyers and families". Fair-housing guidance for housing ads generally steers away from saying who a home is "for" by family status. I did not research this deeply. | New homes is a housing ad. | Is the wording fine, or should it describe the house, not the buyer? |
| C8 | **Helping people behind on payments** | Our "keep the home" text mentions refinancing and says to talk to a lender or advisor too, which is good. I did not research rules on marketing to homeowners in foreclosure or on helping with lenders. | If GLP ever talks to a lender on a homeowner's behalf, extra rules may apply. | Do we ever do that? What must the site say or avoid? |
| C9 | **Privacy Policy and Terms** | Both exist and mention texts. | Must match what really happens (GoHighLevel, analytics, email). | Please read both. |
| C10 | **"No obligation", "no fees", "we pay closing costs"** | These are Joey's words (tagged J in `CONTENT_CLAIMS.md`). | They are promises. | Are they always true, and in writing in the contract? |

## 12. Launch checklist (who does what)

**A. Only Joey can answer** (the second text, after Jeremy approves): photo confirmations and originals; license or brokerage; whether GLP ever assigns contracts; counties and towns; the main phone number and whether it receives texts; hours and who answers; whether a Google listing already exists and who owns it; Facebook page admins; domain registrar and GoHighLevel logins; whether anything in GoHighLevel depends on the old website pages; which situations he has really handled.
**B. Attorney:** C1 to C10 above, plus a read of Privacy and Terms.
**C. GoHighLevel** (someone with access): restyle the form (`research/ghl-form-style.md` has a tested plan), final consent wording, redirect to the thank-you page, owner notifications to both phones, texting registration, optional missed-call text-back.
**D. Domain:** switch-over steps in section 10.
**E. Site (me):** thank-you page, 404, `/calculator` redirect, sitemap and robots, switch-day script that flips addresses and removes `noindex` (tested on a copy, with an undo), shorter Home description, analytics hook (off until approved), situation-page template (empty), the D7 and Home steps if approved.
**F. Local:** create and verify the Google listing; ask the first real customers for reviews; keep name, phone and area wording the same everywhere.
**G. Quality gates before the switch:** links 0 broken; claims check clear; accessibility scan 0 problems; slow-phone speed inside 2.5 s; the form tested on a real iPhone and a real Android phone; Safari and Firefox looked at; a person walks the page with a keyboard only; one pass with a screen reader.

## 13. What I would build next if you approve (in order)

1. The plumbing: thank-you page, "page not found", `/calculator` redirect, sitemap and robots (kept out of the live pages until launch day), shorter Home description.
2. A switch-day script (`tools/launch.py`) that makes the launch changes in a *copy*, runs every check on it, and can undo itself. You would run it on launch day, not before.
3. S2 (rename to About).
4. S4 (Home diet) as four small checkpoints, then S3 (The numbers page) if approved.
5. The contact section on our side (calmer card, faces, three lines on what happens next).
6. Empty templates for situation pages and the guide, so content from Joey drops in quickly.

## 14. Sources, and how far to trust them

Mostly secondary (summaries by other people). Confirm with an attorney or the agency before relying on any of it.

- Tennessee wholesaling bill: [Tennessee Real Estate Commission, Spring 2025 newsletter](https://www.tn.gov/content/dam/tn/commerce/documents/regboards/trec/newsletters/Spring-2025.pdf) (official, but a short summary); bill records for [HB 781](https://open.pluralpolicy.com/tn/bills/114/HB781) and [SB 909 on FastDemocracy](https://fastdemocracy.com/bill/tn/114/bills/TNB00055352) (Public Chapter 72).
- Tennessee real estate rules: [Rule 1260-02-.11, Personal Interest](https://regulations.justia.com/states/tennessee/title-1260/chapter-1260-02/section-1260-02-11/); [Greater Chattanooga Association of Realtors, "Is your advertising in compliance?"](https://gcar.net/news/entry/is-your-advertising-in-compliance) (a trade association's summary of Rule 1260-02-.12).
- FTC reviews rule: [Morgan Lewis summary](https://www.morganlewis.com/pubs/2024/08/ftc-issues-final-rule-on-consumer-reviews-and-testimonials); also [Olshan](https://olshanlaw.com/Advertising-Law-Blog/FTC-Publishes-New-Rule-Covering-Fake-Reviews-and-Testimonials).
- Assumed names in Tennessee: [FindLaw](https://www.findlaw.com/smallbusiness/starting-a-business/how-to-file-a-dba-in-tennessee-in-3-steps.html).
- Google listing rules: [Google Business Profile guidelines](https://support.google.com/business/answer/3038177?hl=en) (official).
- Texting registration: [Ecosire guide to GoHighLevel A2P 10DLC](https://ecosire.com/blog/gohighlevel-a2p-10dlc-compliance-guide) (a vendor's guide; GoHighLevel's own help pages should be checked).
- GitHub Pages: [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) and [a custom 404 page](https://docs.github.com/en/enterprise-server@3.17/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site) (official).
- The old site: I opened `glphomeoptions.com` and `/calculator` in a browser on Oct 22 and only read them.

**What I did not verify:** the enacted text of Public Chapter 72; Tennessee rules on advertising by unlicensed investors; fair-housing rules in detail; rules on helping homeowners facing foreclosure; GoHighLevel's current registration steps; whether `/about` works without `.html` on GitHub Pages; anything about how well the site will rank. The advice on layout, wording and trust is my professional judgment, not a study.

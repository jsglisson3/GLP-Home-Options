# Content claims register

**Purpose:** every factual or promise-like statement on the site, where it came from, and what is still unconfirmed. This is how we keep the standing rule: **never invent reviews, licenses, years in business, awards, results, or business claims we can't verify.**

**Last audited:** Oct 21, 2026 (Session 1), against Joey's live site (glphomeoptions.com: Home, About, Options, Calculator, Contact, Privacy, Terms) and the GLP Home Options Facebook page. **Session 2 (Oct 21) patched the six "fix first" claims**; the section below says what the site says now. Authoritative for claims; `PROJECT_STATUS.md` links here.

**Status key**

| Tag | Meaning |
|---|---|
| **V** | Verified today against Joey's own live site or Facebook page info. |
| **FB** | Taken from Joey's Facebook posts in earlier sessions. Not re-checkable today (logged out, Facebook shows only the newest post). Needs Joey's OK to reuse his words. |
| **OURS** | Wording or a promise we added. Plausible, but it speaks for Joey, so he must OK it. |
| **??** | Not found in Joey's materials. Needs his answer. **Fix or soften before launch.** |

---

## Fixed in Session 2 (Oct 21): the six "fix first" claims

Jeremy chose **"Joey's own words now."** Each claim below was replaced with Joey's wording from his live site, or pulled. A claim comes back only when Joey confirms it. A search of every page, the page builder and the scripts finds none of the old wording.

| # | Claim before Session 2 | What Joey's site says | What the draft site says now | Bring it back only when |
|---|---|---|---|---|
| 1 | "Do you offer seller financing or lease options? **Yes.**" plus two explainer FAQs ("What is seller financing?", "What is a lease option?") | "Creative Solutions: For unique situations where standard paths do not feel like a fit, we explore structured options together." Neither term appears anywhere in his materials. | His sentence (we only added "the" and a contraction): "For unique situations where the standard paths don't feel like a fit, we explore structured options together." Home FAQ: "What if my situation doesn't fit a standard path?" Options: a plain three-step "How it works" card (tell us, we review, you choose). Page descriptions say "explore creative solutions". Seller financing and lease options are not named anywhere. | Joey confirms he offers them **and** a lawyer has looked at the rules. Then add plain-English explainers back. |
| 2 | "Serving **Chattanooga and the surrounding counties**" | "Chattanooga, TN" only. Facebook intro lists no counties. | "Serving Chattanooga, TN" (home pill, footer). "Based in Hixson, serving Chattanooga, TN." (About, Contact). Service-area FAQ: "We work in Chattanooga, TN, and we're based in Hixson. Not sure whether your address is in our area? Call or text us and we'll tell you." Structured data `areaServed` is the city "Chattanooga, TN". | Joey gives the real list of counties and towns. |
| 3 | "GL Partners LLC, **doing business as** GLP Home Options" | Terms and Privacy pages: "GLP Home Options (Legal entity: GL Partners LLC)". | His exact phrase, "GLP Home Options (Legal entity: GL Partners LLC)", with "PO Box 55, Hixson, TN" on the Contact page and in the Privacy policy mailing address. | Joey confirms a registered trade name (a real DBA). |
| 4 | "Request a **free** consultation", "The first conversation is free", "Free and confidential. **No obligation, ever.**" | "Request a Consultation" and "No obligation, no spam. Your information is kept confidential." Nothing says "free" or "ever". | Button "Request a consultation". "No obligation, no spam. Your information is kept confidential." (home hero, and the call-to-action band on Options, About and New homes). FAQs: "No. There's no obligation." | Joey confirms consultations cost nothing (then "free" may return; "ever" stays out). |
| 5 | "Call or text **anytime**" | No hours on his site. Facebook shows "Always open", which is a page setting. | "Call or text". See row 41: whether the number takes texts is still unconfirmed. | Joey states his real availability. |
| 6 | Example cash offer of **$255,000** on a $300,000 home (85%) in the net sheet | Not on his site (our invented example). | **Kept** as the default, with a clearer label: "An example only, not a quote. A real offer depends on the home, and we make it after we see it." At the net sheet defaults, listing nets about **$7,000 more** ($112,000 vs. $105,000), so the example does not flatter GLP. | Still ask Joey if he is comfortable with 85%, or whether to use a neutral figure. |

## Identity and contact

| # | Claim | Where | Source | Status | Notes |
|---|---|---|---|---|---|
| 7 | Phone **(423) 451-5707** | Everywhere (header, footer, tiles, `tel:`/`sms:` links, structured data) | Joey's Contact page; Facebook page info | **V** | Earlier notes mention a second number seen on older Facebook posts (423-401-6779). Ask which is primary. |
| 8 | Email **info@glphomeoptions.com** | Contact, footer, structured data | Joey's Contact, Terms and Privacy pages (decoded in a real browser; the page source hides it) | **V** | |
| 9 | **PO Box 55, Hixson, TN**; "based in Hixson" | Footer (all pages), Contact, structured data | Facebook page info and page title. Not on Joey's website (it shows only "Chattanooga, TN"). | **V** (Facebook only) | It's a mailbox, not an office. Never imply visitors can walk in. |
| 10 | **GL Partners LLC** operates GLP Home Options | Footer, About, legal pages | Re-checked Oct 21: Joey's Terms and Privacy pages say "GLP Home Options (Legal entity: GL Partners LLC)", including their footers. His home page footer says only "GLP Home Options". | **V** | His wording is "Legal entity", not "operates"; our pages say it plainly, which is consistent. |
| 11 | Co-founders **Joey and Ethan** | About, hero caption | Joey's About page ("Co-Founder" x2) | **V** | |
| 12 | "You'll talk to **Joey or Ethan**" | Home, About, New homes, Contact | Joey's site: "you talk to a real person on our team" | **OURS** | Confirm the founders personally answer and follow up, or say "a real person on our team". |
| 13 | "A real person answers when you call" / "not a call center" | Home stats, About | Joey's About: "talk to a real person on our team" | **V** (first part); "not a call center" **OURS** | |
| 41 | "Call or text" (a number that takes texts) | Every page: hero, header, footer, About, Contact, Options, New homes | Joey's Terms and Privacy pages cover text messages he sends after opt-in. Nothing says visitors can text (423) 451-5707. | **OURS** | Confirm the number receives texts and who answers. If not, say "Call". Added in Session 2 when "anytime" came out. Numbered 41 to keep earlier row references stable. |

## How the business works (all from Joey's Options page, checked today)

| # | Claim | Source | Status |
|---|---|---|---|
| 14 | Direct sale closes in **7–14 days** ("as little as 7"), you pick the date | Options table "7–14 Days (Your Choice)"; card "as little as 7 days" | **V** |
| 15 | **No commissions or fees**, "$0 commission", on a direct sale | "Zero commissions or fees"; table "None (0%)" | **V** |
| 16 | GLP **pays closing costs** on a direct sale | Table: "We Pay Them" | **V** |
| 17 | Sold **as-is**: no repairs, no cleaning | "No repairs or cleaning needed" | **V** |
| 18 | **No showings**, just one visit | Table: "None (Just one visit)" | **V** |
| 19 | A **fair cash offer** | "We make a fair cash offer" | **V** |
| 20 | Listing: **45–90+ days**, about **6%** commission, about **2–3%** seller closing costs, repairs usually needed for top dollar, **usually nets the most** | Options table and card | **V** |
| 21 | Keep the home: refinancing, renting it out, getting past a rough patch | Options card "Keep the Home" | **V** |
| 22 | Situations: inheritance, divorce, job relocation, repairs, financial stress, downsizing | About: inheritance, divorce, job relocation, "simplify"; Options: "homes needing repairs", "financial or situational stress" | **V** (downsizing ~ "simplify") |
| 23 | "**Guides, not gurus**" | About H1 | **V** |
| 24 | "We'll share what we'd do in your shoes" | Home: "share what we would do in your shoes" | **V** |
| 25 | Your information is **private / confidential** | Contact: "kept confidential" | **V** |
| 26 | "This site is for informational purposes only and is not legal, tax, or financial advice." | Joey's footer; on every page here | **V** |
| 27 | "You're always free to have your own attorney or title company review anything before you sign" | Home, Options, About, Contact FAQs | **OURS** (protective) |
| 28 | "The numbers go on the table, **including the ones that don't favor us**" | About | **OURS** (a promise on his behalf) |
| 29 | "Takes about a minute" | **Resolved Session 2.** Removed from the contact-form pitch (now "a few details", no time claim). It stays once, on the Options page, for our own net sheet (8 fields, all pre-filled). | **OURS** (net sheet only) |
| 30 | Quotes: "No pressure. Just solutions." and "Real estate isn't always cut and dry. Sometimes you just need options." | Home, About | **FB** (needs Joey's OK) |

## Stories and projects

| # | Claim | Where | Source | Status |
|---|---|---|---|---|
| 31 | September 2026 closing: **35 years of deferred maintenance**, bought off-market, no listing/showings/repairs, closing date to fit their move, helped them find a rental | Home story, About case study | Facebook post (Sept 2026), read in an earlier session | **FB** |
| 32 | Closing-day photo (shows a third party's branded prop: "KEY Title & Escrow" and a second logo) | Home, About | Facebook photo | **FB**. Needs consent (seller privacy, title company branding). |
| 33 | New build: **3 bed, 2 bath, 0.6+ acres, mid $200s**, Chattanooga, "coming soon" | New homes, Home teaser | Facebook post (Oct 13) | **FB** |
| 34 | Build status: "driveway concrete is in, finishing work underway", "decks on, siding going up", "kitchen cabinets in" | New homes, captions | Facebook photos/posts. Newest public post (Oct 20): "Concrete's going in! Finals getting done." | **FB**, consistent. **Will go stale**: update regularly or use neutral wording. |
| 35 | "Ask about getting in **before it's listed**" | New homes, Home | Facebook (earlier session) | **FB** |
| 36 | **Down payment assistance** ("ask us how it could help") | New homes (hero, audience card, FAQ), Home | Facebook (earlier session). The FAQ answer is generic ("exists for many first-time buyers; depends on your lender"). | **FB**. Confirm what GLP actually offers or partners on. |
| 37 | "We build affordable new homes in Chattanooga for first-time buyers and families" | Home, About, New homes | Facebook post wording ("Tired of crazy prices?...") | **FB** |

## Numbers and tools

| # | Claim | Source | Status |
|---|---|---|---|
| 38 | Net sheet defaults: $300,000 price, $150,000 payoff, 6% commission, 2.5% closing, $8,000 repairs, $1,800/month carrying cost, 2.5 months to sell | 6%, 2–3% and 45–90+ days are Joey's. The repairs, carrying cost and payoff are our examples, labeled "Example figures". | **V** (rates), **OURS** (examples) |
| 39 | Verdict logic is symmetric (listing vs. direct; "about the same" within $500); the sheet ignores taxes, prorations, concessions and capital gains | Read from `js/site.js` | **V**. Disclaimer shown: "Estimates for information only. Not legal, tax, or financial advice." |
| 40 | "Neither one is always better." | Our editorial line; consistent with Joey's "usually nets the most" for listing | **OURS** |

## Things the site deliberately does NOT claim (keep it that way)

- No reviews, testimonials, star ratings (Facebook shows "Not yet rated (0 reviews)"), awards, licenses, certifications, years in business, number of homes bought, or dollar results.
- No `aggregateRating`, `priceRange`, or opening hours in the structured data.
- No market statistics. Joey's weekly Facebook market posts are labeled "AI content", so we do not copy those numbers. A market snapshot would need sourced data.
- No claim that GLP "lists homes on the MLS" (Joey's Options page says "We list your home on the MLS"; that implies a license or a partner brokerage, so we say "list with an agent").
- No seller financing or lease options, no "free" consultation, no "anytime", no "surrounding counties", no "doing business as". These came out in Session 2. Do not bring any back without Joey's yes.

## Questions that block launch (ask Joey)

1. Do you (or Ethan) hold a Tennessee real estate license, or work with a brokerage? Which licensing and advertising disclosures apply to your buying and listing (and to the home gallery below)? Ask a lawyer.
2. Seller financing and lease options: do you actually offer them? (Row 1.) Until you say yes, the site does not mention them.
3. Which counties and towns do you really serve? (Row 2.)
4. Is the consultation free? Are you available at all hours? Does (423) 451-5707 take texts? (Rows 4, 5, 41.)
5. Which phone number is primary? (Row 7.)
6. May we use the closing story, the closing photo (and the title-company branding in it), and quotes from your Facebook posts? (Rows 30-32.)
7. Down payment assistance: what is real? Is the new home still unsold and still in the mid $200s? (Rows 33-36.)
8. **Gallery (Jeremy's idea, Oct 21):** which houses from your Facebook page should be shown, what is each one's status (sold, available, under construction), may we show addresses, prices and interior photos, who owns the photos, and can you send the originals? (Facebook only exposes the newest post when logged out, so we can't list them ourselves.)
9. Real reviews: once you have 3+ happy sellers, ask them for Google reviews. We add real ones with first name and neighborhood. Never invent.
10. Are you comfortable with the $255,000 (85%) example offer in the net sheet, or should it be a neutral number? (Row 6.)

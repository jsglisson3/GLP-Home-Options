# Fixing the contact form's look (GoHighLevel)

**Why:** Jeremy, Oct 21, 11:09 PM: the questionnaire "looks like a third-party bolt-on, scammy, like an ad on top of the website." He is right. The form on the Home and Contact pages is GoHighLevel's plain default, in a frame (an iframe) from `links.voiseai.com`. Our site's CSS cannot reach inside it. Only someone who can open the form in GoHighLevel can change it.

**Decision, Oct 22, 3:08 PM (Jeremy): leave the current form alone; build a new one later.** Jeremy, 3:03 PM, looking at the live Contact page on a wide screen: "on desktop veiew still lots of white space and this whole form still sticks out .. this is one of the main thigns so has tob e incredible this whole area  just note that down". After I explained that GoHighLevel draws everything inside the frame, 3:08 PM: "ahhh so this is the form from his existing site.. we will need to make a new one in the future lets leave this alone.. thatts fine its tacky im following now" and "ill talk to him on this one" (Joey). **What that means:** (1) Do not paste anything into the existing form and do not change its button or its text: it is, Jeremy says, the form from Joey's existing site, so an edit would change that site too. (2) The steps further down ("The fix: steps for whoever has GoHighLevel access") now apply to **a copy** of the form made for the new site, not to this one; the copy needs its own place in the leads workflow and a new `FORM_ID` in `tools/build-pages.py`. (3) Our side of the frame stays as it is (FORM-TRIM, Checkpoint 36); when the form is replaced by a restyled copy, delete FORM-TRIM in the same push (see the first update below).

**Why it feels like "lots of white space"** (measured Oct 22, 3:09 PM, on the form's own page at 456 px wide, the width of the card in Jeremy's screenshot; nothing typed, nothing sent): the form draws 41 px of its own padding at each side; its first field starts 61 px below the top of the page (30 px of padding plus 31 px that may belong only to the standalone page); each field row is 87 px (a 71 px label-and-box, the box itself 36 px, plus a 16 px gap), so four small boxes take about 350 px; the two consent paragraphs are 176 and 128 px tall; the button is 45 px tall. Small boxes in big gaps read as empty space, and the site's fonts and colors stop at the frame's edge, so the form looks pasted in. A form that "has to be incredible" fixes both: the same font, field style and button as the site, and an even, tight rhythm.

**What "incredible" would mean for this area** (from Jeremy's words and the site's rules; proposed, Jeremy and Joey decide): one font, one field style and one button label ("Get my options") from the card's heading to its last line; no seam between our heading and the first field; the fewest fields Joey needs to call someone back (name and phone first); the consent text in one font and size, the wording unchanged, the doubled sentence gone; a success message in Joey and Ethan's voice; 16 px field text so phones do not zoom in; works with a keyboard and a screen reader; on a wide screen the form and the call, text and email tiles feel like one block, not a form beside a list.

**The two routes (proposed):** **A. A copy of today's form, styled** (about an hour with whoever has the login, plus one real test lead): copy it in GoHighLevel, change "Button" to "Get my options", paste `research/ghl-form-custom.css`, remove the doubled sentence, point the copy at the same leads workflow, send one test lead from a real phone, then change `FORM_ID`, delete FORM-TRIM and rebuild. It keeps the consent record, the spam check and the CRM hookup that GoHighLevel gives for free. **B. A form built into our own page** that sends the details to GoHighLevel (a workflow with a webhook, or its API; someone with access sets that up): the best look and full control, but we rebuild the consent record and the spam protection, test with real leads, and get a legal look at the wording. Recommendation: A first; B only if Joey's GoHighLevel allows it and he wants it.

**For Jeremy's talk with Joey:** "Added Oct 22, 3:08 PM: the contact form" at the end of `research/questions-for-joey.md` has four questions (who can sign in to GoHighLevel, since the form is served from `links.voiseai.com`; whether we can have a second copy of the form; where leads go and who answers; whether the consent wording is the registered wording).

**Update, Oct 22, afternoon (Checkpoint 36): FORM-TRIM, one CSS rule that removes the extra space around the form.** Jeremy, 1:08 PM, looking at the live form: "a little extra space on the form." The company's form draws its own padding (about 42 px a side, about 20 px blank above its first label) inside our card's own padding, so on a 375 px phone the fields were about half the screen wide (203 px). The rule in `css/site.css` (search for `FORM-TRIM`) makes the form's frame as wide as the card (`width:calc(100% + 2*clamp(24px,3vw,38px))` with matching negative side margins, which is the card's padding) and starts it 14 px higher (`margin-top:-14px`). Result on a 375 px phone: fields about 24% wider, the form about 120 px shorter. **It is tuned to how the form looks today.** Two ways it can go wrong, and what to do:
1. **If someone restyles the form in GoHighLevel and removes the form's own padding (the paste-ready `research/ghl-form-custom.css` does),** the fields would touch the card's edge. **Delete the whole `.ghl iframe{...}` rule** (the comment above it explains why; both `margin` and `width` lines go) and rebuild.
2. **If the form ever looks clipped or off-centre on the live site,** the same rule is the first suspect. Deleting it brings back exactly the Checkpoint 35 look (the extra space returns; nothing else changes). It is CSS only: no script or markup depends on it, and the form-loading code and its tests do not care whether it is there.
The test browser stands in for the form (it cannot reach GoHighLevel), so the real result is judged on the live site, in the browser pane, after the push.

**Update, Oct 22, 11:30 AM (Checkpoint 35): the form also never loaded below the first screen.** Cause and fix are in `PROJECT_STATUS.md` (Checkpoint 35): our frame was `loading="lazy"` and GoHighLevel's embed script parks every form frame 10,000 px off-screen until the form reports its height, so the browser never fetched it. That is fixed on our side; nothing in GoHighLevel needs to change for it. The look problems below still need someone with GoHighLevel access. Measured again today on the real form: the button is `button.btn.btn-dark.button-element` with the label "Button" (`#18bd5b`); the consent paragraphs have inline fonts; fields are 12 px; the two consent links point at `glphomeoptions.com`; Cloudflare's bot check inside the form logged "Error: 600010" when the form was opened by itself in the pane (may be the pane itself; one test lead from a real phone settles it). On a phone the form is about 1,150 px tall at 390 px wide because of the two long consent paragraphs, so a smaller consent font and the card's side padding matter more there.

**Who it is for:** ordinary homeowners, many short on money and time, who have seen a lot of "we buy houses" ads (Jeremy, Oct 21, 11:11 PM). The form has to look like it belongs to two local guys, not to an ad network. See `DESIGN_SYSTEM.md`, section 0.

![Before and after](ghl-form-before-after.jpg)

## What is wrong (measured on the live form, Oct 21, about 11:15 PM)

| What | Today | Why it hurts |
|---|---|---|
| Button label | The word **"Button"** (the builder's placeholder), bright green `#18bd5b`, 5px corners | Looks unfinished and off-brand. This is the worst one. |
| A card inside our card | The form draws its own white card, with a shadow, 44px side margins and 40px padding | Our card already frames it, so it reads as a pasted-in box. |
| Fonts | Labels Inter 14px; fields Inter 12px; first consent in Segoe UI bold, second in Georgia serif with the company name in another color (inline styles) | Three fonts in one form. 12px fields also make iPhones zoom in when tapped. |
| Links | Default blue `#0d6efd` | Not our color. |
| Field borders | `#acacac`, about 2.3:1 against white | Below the 3:1 that WCAG asks of a field's outline. |
| First consent | "Message frequency varies." appears twice | Looks careless in a legal line. |
| Required fields | Phone and Email both marked required | A question for Joey: many people would rather give a phone number only. |

Good news seen at the same time: the consent text now names "GL Partners LLC DBA GLP Home Options" (no `[BUSINESS NAME]` placeholders left), and the Privacy and Terms links point to `glphomeoptions.com/privacy-policy` and `/terms-of-service` (the old site's pages; see "After launch" below).

## The fix: steps for whoever has GoHighLevel access (about 5 minutes)

Menu names in GoHighLevel move around a little. Look for the form builder and its Style panel.

1. Open the form (id `c36UOOc2pkosxfvRfjZJ`, "GLP Home Options lead form") in the form builder.
2. **Button text:** change "Button" to **Send my details** (or "Get my options", Joey's call). This is a setting, not CSS, and it matters most.
3. **Custom CSS:** paste all of `research/ghl-form-custom.css` into the form's Custom CSS box.
4. **First consent:** delete the repeated "Message frequency varies." Change nothing else in the consent wording. The text must keep matching the registered text-message campaign.
5. Save. Then, on a real phone, open the live Contact page and:
   - look at the form (one font, green button, no box inside the box);
   - tap a field (the page should not zoom in);
   - send **one test lead with a phone number you control**, and check it arrives where leads go and that the consent is recorded.
6. Tell Claude what you see. (Update, Oct 22: when Jeremy's computer is on, Claude can open the real form in the built-in browser pane, so it can check the form by itself and inside our page; it still cannot submit a real lead without a go from Jeremy.)

## What the CSS does and does not do

- **Does:** removes the form's own card and margins, uses the site's font (loaded from our site, falling back to Inter), makes fields 54px tall with 12px corners and a visible border, makes the consent text one font, size and color, makes the button a green pill in our gradient, colors the links.
- **Does not:** change any wording, required flags, field order, the consent checkboxes, where leads go, or the form's behavior.
- **Tested:** on a throwaway copy of the live form page in a browser tab, at 500px wide (the form's width on a laptop screen), by adding the CSS to the page in the browser. Nothing was saved in GoHighLevel and nothing was submitted. Not tested: the error messages after a failed send, a phone width inside our page, and the form inside our page at all.
- **Why every rule repeats the id (`#_builder-form#_builder-form`):** the builder's own rules carry `!important` and are specific, and a normal rule loses to them. Repeating the id makes ours win.
- **If it ever looks off:** remove the pasted CSS and the form goes back to the default look. Nothing else depends on it.

## Check before pasting

- **Is this form also on the old site?** If `glphomeoptions.com` embeds the same form, the new look shows there too. If that matters, duplicate the form, paste the CSS into the copy, re-point the leads workflow, and change `FORM_ID` in `tools/build-pages.py`. If not, edit it in place.
- The font line points at `jsglisson3.github.io/GLP-Home-Options/fonts/...`. When the site moves to `glphomeoptions.com`, change that address. If the font fails to load, the form falls back to Inter and still looks fine.

## After launch

The consent text's links use `glphomeoptions.com/privacy-policy` and `/terms-of-service`. When the new site replaces the old one on that domain, those two addresses must still open the new Privacy and Terms pages (GitHub Pages serves `privacy-policy.html` at `/privacy-policy`, so they should). Check them then.

## Other options, not now

- **A form built into our own page** that sends the details to GoHighLevel. It would look perfect, but it needs a GoHighLevel workflow set up by someone with access, and we would have to rebuild the consent record and spam protection that the GoHighLevel form gives for free. A Session 11 decision, with Joey and a lawyer, not tonight.
- **Our side of the frame** (Session 6e+): a softer card shadow, Joey and Ethan's faces on the card, a calmer band. Listed in `ROADMAP.md`.

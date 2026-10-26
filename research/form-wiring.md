# Connecting the contact form to a place that receives it

**Written:** Oct 26, 2026 (Checkpoint 46). **For:** Jeremy, and whoever sets up the receiving end. **Nothing is connected.** Today the form builds a ready-made text and email from what the visitor typed, and the visitor's own phone or mail app sends it (the text button comes first on a phone; the email button comes first on a computer or tablet, which cannot send a text by themselves). The main button says "Get my message ready", and the page says plainly, in those words, that nothing has been sent until the visitor presses Send in their own app. No lead is lost, but nothing lands in a CRM or an inbox by itself yet.
**Not legal advice.** Anything about text-message rules is in `compliance-questions-for-joey.md` (kept private, for an attorney). Facts about outside services below were read on their own pages on Oct 26, 2026; check them again before relying on them.

## The change itself is one line

In `tools/build-pages.py`:

```
FORM_ENDPOINT = ""            ->  FORM_ENDPOINT = "https://the-address-that-receives-it"
FORM_FORMAT   = "json"        ->  "json" or "form" (see "What the receiving end gets")
```

Then rebuild (`python3 tools/build-pages.py`) and run `python3 tools/form-test.py`, `python3 tools/safety-test.py` and `python3 tools/seo-check.py`. `form-test.py` already plays both modes against a made-up address (`https://leads.example.test/hook`), so it proves the **page** behaves; it cannot prove the **real receiver** works. That needs the live test below. `seo-check.py --launch` prints a reminder (not a failure) while `FORM_ENDPOINT` is empty, and it fails if the value is anything but empty or an `https` address. To go back, set it to `""` and rebuild; the form returns to the hand-off. **The main button's words follow by themselves:** "Get my message ready" while the address is empty (it sends nothing, and says so), "Send to Joey & Ethan" once it is set. `form-test.py` swaps in both the address and that label when it plays the connected mode.

## What the receiving end gets

One `POST` from the visitor's browser, sent as a "simple" cross-origin request (no permission check first, no custom headers, no cookies). The body is either **JSON text** (`Content-Type: text/plain;charset=UTF-8`, so the receiver must parse the body as JSON itself) or an ordinary **web form** (`application/x-www-form-urlencoded`, where `true`/`false` become `yes`/`no`). `FORM_FORMAT` picks one. A form-style catch hook is the safer first try; a small relay (option B) can take either.

| Field | Example | Notes |
|---|---|---|
| `name` | `Maria Lopez` | required |
| `phone` | `(423) 555-0123` | required. A US number is ten digits, formatted this way (area code and exchange never start with 0 or 1). A number that starts with `+` and a country other than 1 (`+44 20 7946 0958`) is sent exactly as the visitor typed it (8 to 15 digits, nothing reformatted). An extension goes in the note |
| `email` | `maria@example.com` | optional, may be empty |
| `topic`, `topic_label` | `sell`, `Selling my home` | `sell` / `keep` / `new` / `unsure`, or empty. A button on the site may have chosen it (`?for=`) |
| `channel` | `text` | `call` / `text` / `email`, or empty |
| `address` | `123 Main St` | optional, free text |
| `message` | `Got a call from an agent...` | optional, up to 600 characters |
| `consent_service`, `consent_marketing` | `true` / `false` (form: `yes` / `no`) | the two optional, unchecked text-message boxes, exactly as the visitor left them |
| `consent_version` | `8b99d710` | a short fingerprint of the two consent sentences on screen. It changes by itself if the wording ever does (`tools/form_text.py: consent_version()`) |
| `page` | `https://glphomeoptions.com/contact` | the page the form was on |
| `sent_at` | `2026-10-26T14:03:09.000Z` | the visitor's own clock, so **do not trust it**; use the time the receiver got it |
| `seconds_on_form` | `47` | whole seconds from when the form's script ran (about when the page opened) to Send. The page never acts on it; it is there for the receiver. A robot that posts at once shows `0` or `1`, but a person with autofill can also be quick, so **treat it as a hint, never as a reason to drop a request on its own** |
| `website` | `https://spam.example` | **Only present when the hidden trap field has something in it.** Real requests do not have it. See the next paragraph. |

**The hidden trap field.** People never see the box called `website`. A robot that fills in every box fills it in too. **The page never judges it:** a person's password manager can fill that box by mistake, and a person must never be shown a thank-you for a request that went nowhere. So whenever the box has something in it, the request is sent as usual **with `website` in it** (and `seconds_on_form`), and the receiving end decides. The sensible rule: **flag it, do not throw it away**: keep those requests in a separate place for a person to glance at, because the occasional real person will be in there. If the receiver answers with success the visitor sees the thank-you, as for any request; if it does not, the visitor gets the ready-made text and email like any other failure. A spam bot that posts straight to the address and never opens the page is not caught by this at all; only the receiver (option B below) can stop that. While nothing is connected the trap is ignored, since nothing is sent anyway.

## What the receiving end must do

1. **Answer with a success code (200 to 299) within about 15 seconds.** Anything else, or silence, makes the page show "We couldn't confirm that was sent" and fall back to the ready-made text or email (so a lead is never lost to a dead end). The post is sent with `keepalive`, so it can finish even if the visitor leaves the page at once.
2. **Allow this site's address through the browser's cross-origin rule (CORS)**: send `Access-Control-Allow-Origin: *` (or the exact site address) on the answer. Both addresses matter: `https://jsglisson3.github.io` while it is a preview, and the real domain at launch. **Why this matters beyond "it doesn't work":** if the receiver *gets* the post but leaves out that header, the browser hides the answer, the page reports a failure, the visitor is shown the fallback and may text as well, and the lead arrives twice. Check the browser console during the live test (a red "blocked by CORS policy" line is the sign). **Two copies of one lead can also happen when a visitor presses Send again after a timeout.** If that turns out to matter, the page could send a random reference with each send so the receiver can recognise a repeat; it does not today, and adding it is a small change.
3. **Treat everything as untrusted text.** Names, notes and addresses come straight from strangers. Do not paste them into a page, a script or a formula without escaping them.
4. **Keep the consent record**: `consent_version`, both consent values, the receiver's own time, the page, and (on the receiver, not the page) the visitor's IP address. Keep the exact wording for each version, too. `tools/form_text.py` holds today's; an old version's wording can be recovered from the repository's history by its fingerprint. Today's version is `8b99d710`.
5. **Do not tell the visitor anything the site does not promise.** The page says "Joey or Ethan will get back to you" with no time. An automatic reply, if Joey wants one, should say the same.

## Three ways to build the receiving end (for Jeremy and Joey to choose)

**A. Straight into GoHighLevel** (Joey's CRM; he already uses it for the old form and the booking page).
A workflow with an *Inbound Webhook* trigger gives a URL that creates a contact from a test request (read Oct 26 from a third party's setup guide; confirm on GoHighLevel's own pages). Fewest moving parts, one place for Joey to look. **Unknowns:** whether that URL answers with the CORS header above (if it does not, the browser will report a failure even though the contact arrives, which is the duplicate case in item 2); whether it reads a form-style body (try `"form"` first) or a JSON one; and whether the plan charges extra for that trigger. Someone with the login must test all three. Do not guess.

**B. A small relay between the page and GoHighLevel** (a Cloudflare Worker is the usual choice).
The page posts to the relay; the relay adds the CORS header, flags robots (a request with the trap field filled goes to a separate place for a person to glance at rather than being thrown away; `seconds_on_form` is only a hint; it can also rate-limit by IP), forwards the lead to GoHighLevel (webhook or API) and also emails a copy to Joey as a backup, so a CRM problem never loses a lead. Cloudflare's pages read Oct 26: the Workers free plan allows 100,000 requests a day and 10 ms of processor time per request, which is far more than this form needs; Turnstile (Cloudflare's robot check, if spam ever becomes a problem) is free with no limit on checks, up to 20 widgets. Cost: one more thing for someone to look after, and the secret key for GoHighLevel lives in the relay, never in the page. **This is what I would build** if option A's three unknowns do not all come back "yes".

**C. A hosted "form to email" service.**
Quickest, but the leads' personal details sit with one more company, Joey's CRM does not see them unless it is connected, and the consent record is only as good as that service's export. Fine as a stop-gap; not what a business that texts its leads should end up on.

## What Joey has to decide first

These are already on `research/questions-for-joey.md` (Oct 26 additions): where leads should go and who gets the alert; who answers, and by when (a reply time must be something he can keep every time, and is never put on the site until he says so); whether the visitor gets an automatic reply and what it says; and whether GoHighLevel may text the visitor afterwards, which depends on his registered text campaign and on an attorney's reading of the consent wording. The form is built so that none of these answers changes the page: only the one line above, and the receiver.

## The live test (before the real site points at it)

Do these with a test contact name such as `TEST - do not call`, from a real phone on mobile data, with Joey (or Jeremy) watching where the lead should appear. Delete the test contacts afterwards. Nothing here should touch Joey's real pipeline until the receiver is proven.

1. Fill the form with everything, tick **neither** consent box, send. It should appear within a minute, every field spelled right, both consent values `false`/`no`, one copy only. The page should say "Thank you".
2. Do it again with **both** boxes ticked. Both values should arrive as `true`/`yes`.
3. Fill it with awkward text: an apostrophe and an ampersand in the name, an emoji and a line break in the note, a very long note. All of it should arrive unchanged and not break anything downstream.
4. Open the browser's console during one send. No red CORS line.
5. Turn on airplane mode and send. The page should show the ready-made text and email ("We couldn't confirm that was sent") within a few seconds, and nothing should arrive.
6. Turn the receiver off (or point a test build at a dead address) and send. The page should show the same fallback within 15 seconds.
7. In the console, put text in the hidden trap field (`document.getElementById('lf-web').value='x'`) and send. The request **arrives, with a `website` value**, and the page says thank you because the receiver answered. The receiving end should flag it, not drop it silently. Then switch the receiver off and do it again: the page shows the fallback, never a thank-you.
8. Send twice quickly (double-tap the button). One lead only.
9. Check the same on a desktop browser and one other phone (iPhone and Android if both are around).

## What this form does *not* do (on purpose)

No analytics or tracking scripts, no cookies, nothing stored in the browser, no third-party code on the page, no autofill of the visitor's details from the address bar, no countdowns or "limited slots" language, and no promise about how fast anyone replies. Keep it that way when wiring it up: any pixel or script added to the form needs Joey's agreement, and a line in the privacy policy.

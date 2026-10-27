#!/usr/bin/env python3
"""The contact form: does it work, in every way a visitor can meet it? (lead_form() in tools/build-pages.py, js/form.js, the .lf rules in css/site.css.)

Run:   python3 tools/form-test.py        It must print  FAILS 0.   (add --long for one more case that waits 16 seconds: a receiving end that never answers)
Nothing leaves this machine: the site is served on a throwaway local port, and every address outside it is refused (the test stands in for the
receiving end where it needs one). Nothing is ever typed into the real company form: there is no frame on the page any more.

What it plays:
  the built pages ......... one form on Home and on Contact, no frame from another company, no script from another company; Joey's two text-message
                            boxes are word for word what tools/form_text.py holds, unticked and optional; every field has a label and the right keyboard
                            and autofill hints; the trap field is hidden from people and takes no room; the other pages carry none of it
  the buttons ............. every button that leads to the form says what the visitor wants (data-topic) and, from another page, carries ?for=...
                            so the form opens with that choice made; a topic in the address works; one that is not a real choice is ignored
  checking ................ an empty Send names both missing things, in one box (focused) and next to each field, with aria-invalid and a
                            link per line; fixing a field clears its message at once; phone and email mistakes are explained in plain words
  the phone number ........ formats while typed, lets backspace work, leaves a leading 1 or + alone until the field is left, then tidies it
  nothing connected yet ... the Send button says "Get my message ready" (it sends nothing); it makes a ready-made text and email (nothing leaves the page), shows
                            exactly what they say, puts the text button first on a phone and the email button first on a computer or tablet (the words of both buttons
                            follow), names any text-message box they ticked, copies it (and gives the keyboard back when the browser has no clipboard), goes back to
                            the form with everything still typed in; the line under the heading names the main button by its words and says what to do if nothing
                            opens; a click anywhere in the first moments of the panel is ignored (a double-click), unless the phone's clock was set back; half-emoji
                            in a note are swapped, a whole emoji is kept; a filled trap field changes nothing here
  before the script has run . pressing Send or Enter cannot put the details in the address bar (the form cannot submit by itself)
  keyboard (phone) ........ the "next" key in the name, email and address boxes moves on instead of sending the form; Done in a wrong phone box keeps the
                            error box's alert role; Enter on a choice or a text-message box, and a held Enter key, send nothing; every box shows a clear focus ring
  connected (FORM_ENDPOINT) the details are posted once (never twice), "Thank you" shows; a filled trap field never turns a request into a false thank-you:
                            it is posted along with a note of it, for the receiving end to judge; a refusal, a blocked answer or silence gives the text and email
                            hand-off ("We couldn't confirm that was sent") instead of a dead end
  no JavaScript ........... the form is replaced by a call, text and email card that works
  fit ..................... phone widths 320 to 430, tablet, laptop, desktop and text at 150% and 200%: nothing runs off the screen or out of the card,
                            targets are big enough, typing never makes the phone zoom in, the form sits right under the heading on a phone and
                            beside the other parts on a computer
  keyboard ................ the tab order, Space and Enter on the choices, the extras and the boxes
  axe (when it is installed) the form in four states: as it opens, with errors, the ready-made message, the thank-you
"""
import functools, html as H, http.server, json, pathlib, re, socketserver, sys, threading, time, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import _site  # noqa: E402,F401  (lets the base-folder addresses work on the local server)
import form_text as FT  # noqa: E402

LONG = "--long" in sys.argv
SRC = (ROOT / "tools" / "build-pages.py").read_text(encoding="utf-8")
PHONE = re.search(r'PHONE_TEL, PHONE_SMS, PHONE = "tel:\+1(\d+)", "sms:\+1(\d+)", "([^"]+)"', SRC)
SMS_BASE, PHONE_TXT = "sms:+1" + PHONE.group(2), PHONE.group(3)
EMAIL = re.search(r'^EMAIL = "([^"]+)"', SRC, re.M).group(1)
HOOK = "https://leads.example.test/hook"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k):
        pass

    def handle(self):
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError):   # the browser walked away from a download half way (a page change): not a problem
            pass


srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()
fails = []


def check(name, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + name + (("  " + str(detail)) if detail != "" else ""))
    if not ok:
        fails.append(name)


# ================================================================= 0. the built pages, read as text
pages = {f.name: f.read_text(encoding="utf-8") for f in sorted(ROOT.glob("*.html"))}
for name, t in pages.items():
    check(f"{name}: no frame and no script from another company on the page", "<iframe" not in t and "form_embed.js" not in t and "widget/form" not in t)
    has = name in ("index.html", "contact.html")
    check(f"{name}: {'one form (id lf) and js/form.js' if has else 'no form and no form script'}",
          (t.count('id="lf"') == 1 and "js/form.js?v=" in t) if has else ('id="lf"' not in t and "form.js" not in t))
check("js/site.js no longer builds a frame or names another company", "voiseai" not in (ROOT / "js" / "site.js").read_text(encoding="utf-8"))
ENDPOINT = re.search(r'^FORM_ENDPOINT = "([^"]*)"', SRC, re.M).group(1)
ENDPOINT_BUILT = ENDPOINT   # what the built pages were made with (the connected-mode cases below pretend an address, and the label that goes with it)
check("the form cannot submit by itself before js/form.js has run (method post, and onsubmit returns false), so a stray Send never writes the details into the address", 'method="post" onsubmit="return false"' in pages["contact.html"] and 'method="post" onsubmit="return false"' in pages["index.html"])
check("the Send button says what it does: 'Get my message ready' while nothing is connected, 'Send to Joey & Ethan' once something is", re.search(r'<span class="lf-send-t">([^<]*)</span>', pages["contact.html"]).group(1) == ("Get my message ready" if not ENDPOINT_BUILT else "Send to Joey &amp; Ethan"), ENDPOINT_BUILT)
check("the box of problems carries no alert role itself (the one inside it does: the box takes focus, and some screen readers skip the text when both are the same element)", re.search(r'<div class="lf-sum" id="lf-sum" tabindex="-1" hidden>', pages["contact.html"]) is not None)
check("the form's data-endpoint is the builder's FORM_ENDPOINT (empty until the receiving end exists, else https)", f'data-endpoint="{ENDPOINT}"' in pages["contact.html"] and (ENDPOINT == "" or ENDPOINT.startswith("https://")), ENDPOINT)

FORMAT = re.search(r'^FORM_FORMAT = "([^"]*)"', SRC, re.M).group(1)
check("the form's data-format is the builder's FORM_FORMAT, json or form", f'data-format="{FORMAT}"' in pages["contact.html"] and FORMAT in ("json", "form"), FORMAT)
check("the form carries a fingerprint of the two text-message sentences (it changes by itself if the wording does)", f'data-consent-version="{FT.consent_version()}"' in pages["contact.html"] and re.fullmatch(r"[0-9a-f]{8}", FT.consent_version()) is not None, FT.consent_version())
for fid, hint in (("lf-name", "next"), ("lf-phone", "done"), ("lf-email", "next"), ("lf-address", "next")):
    check(f"{fid}: the phone's Return key says '{hint}'", f'id="{fid}"' in pages["contact.html"] and re.search(r'id="%s"[^>]*enterkeyhint="%s"' % (fid, hint), pages["contact.html"]) is not None)

# ================================================================= the buttons that lead to the form
for name, t in pages.items():
    for m in re.finditer(r'<a [^>]*href="([^"]*)"[^>]*>', t):
        tag, href = m.group(0), m.group(1)
        topic = re.search(r'data-topic="([^"]*)"', tag)
        q = re.search(r"[?&]for=([^&#]*)", href)
        if topic:
            check(f"{name}: data-topic=\"{topic.group(1)}\" is a real choice", topic.group(1) in dict(FT.TOPICS))
            if name not in ("index.html", "contact.html"):
                check(f"{name}: a button with data-topic={topic.group(1)} also carries ?for={topic.group(1)} ({href})", bool(q) and q.group(1) == topic.group(1) and href.endswith("#contact"))
        if q:
            check(f"{name}: ?for={q.group(1)} names a real choice", q.group(1) in dict(FT.TOPICS))
topic_links = sum(len(re.findall(r'data-topic="', t)) for t in pages.values())
check("the buttons that say what the visitor wants are there (Options, New homes, Home, the bands)", topic_links >= 9, topic_links)

# ================================================================= everything below needs a browser
SHOW = """() => { const f = document.getElementById('lf'); const v = e => { if (!e) return false; const s = getComputedStyle(e), r = e.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
  return { form: v(f), hand: v(document.getElementById('lf-hand')), done: v(document.getElementById('lf-done')), sum: v(document.getElementById('lf-sum')), nojs: v(document.querySelector('.lf-nojs')) }; }"""
ACTIVE = "(() => { const a = document.activeElement; return a ? (a.id || a.tagName.toLowerCase() + (a.name ? ':' + a.name : '')) : ''; })()"
ERRS = "[...document.querySelectorAll('.lf-err:not([hidden])')].map(e => e.lastChild.textContent.trim())"
INVALID = "[...document.querySelectorAll('#lf [aria-invalid=true]')].map(e => e.id)"


def ctx_page(b, w=1280, h=900, mobile=False, js=True, reduced=True, grant=False, record=None, hook=None, endpoint=False, blank_js=False, slow=0):
    ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, java_script_enabled=js,
                        reduced_motion="reduce" if reduced else "no-preference", device_scale_factor=1)
    if grant:
        ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=BASE.rstrip("/"))

    def handler(route):
        url = route.request.url
        if url.startswith(BASE):
            path = urllib.parse.urlparse(url).path
            if endpoint and path.endswith(".html") and (ROOT / path.lstrip("/")).exists():   # the page, as it will be once FORM_ENDPOINT is set (endpoint="form": and FORM_FORMAT too)
                body = (ROOT / path.lstrip("/")).read_text(encoding="utf-8").replace('data-endpoint=""', 'data-endpoint="%s"' % HOOK).replace('<span class="lf-send-t">Get my message ready</span>', '<span class="lf-send-t">Send to Joey &amp; Ethan</span>')
                if endpoint == "form":
                    body = body.replace('data-format="json"', 'data-format="form"')
                return route.fulfill(status=200, content_type="text/html; charset=utf-8", body=body)
            if slow and path.endswith("/js/form.js"):   # a very slow connection: everything waits (the test's own thread sleeps, so every script arrives together, late)
                time.sleep(slow)
            if blank_js and path.endswith("/js/form.js"):   # the form's script, empty: what a visitor has in the first moments of a slow connection, when the form is already on screen
                return route.fulfill(status=200, content_type="application/javascript", body="")
            return route.continue_()
        if hook is not None and url.startswith(HOOK):
            if record is not None:
                record.append({"method": route.request.method, "body": route.request.post_data, "type": route.request.headers.get("content-type", "")})
            return hook(route)
        if record is not None:
            record.append({"blocked": url})
        return route.abort()
    ctx.route("**/*", handler)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    return ctx, pg, errs


def open_form(pg, page="contact.html", query=""):
    pg.goto(BASE + page + query, wait_until="load")
    pg.keyboard.press("Shift")   # the pages keep themselves at the top until a visitor does something
    pg.add_style_tag(content=".mobile-bar{display:none!important}")
    pg.evaluate("document.querySelectorAll('.rv').forEach(e => e.classList.add('in'))")
    pg.locator("#lf").scroll_into_view_if_needed()


def fill_valid(pg, name="Jane Smith", phone="4234515707", extras=True):
    pg.fill("#lf-name", name)
    pg.click("#lf-phone")
    pg.keyboard.type(phone, delay=8)
    if extras:
        pg.click("#lf-more summary")
        pg.fill("#lf-email", "jane@example.com")
        pg.fill("#lf-address", "123 Main St, Hixson 37343")
        pg.fill("#lf-message", "My mom's house.\nEvenings are best.")


def hrefs(pg):
    sms = urllib.parse.unquote(pg.get_attribute("#lf-sms", "href"))
    mail = urllib.parse.unquote(pg.get_attribute("#lf-mail", "href"))
    return sms, mail


with sync_playwright() as p:
    b = p.chromium.launch()

    # ============================================================= 1. as it opens (desktop, Contact)
    ctx, pg, errs = ctx_page(b)
    seen = []
    pg.on("request", lambda r: seen.append(r.url))
    open_form(pg)
    s = pg.evaluate(SHOW)
    check("Contact, desktop: the form shows; the no-JavaScript card and the old frame do not", s["form"] and not s["nojs"] and not s["hand"] and not s["done"] and not s["sum"], s)
    check("  four choices, none ticked; the two text boxes unticked", pg.evaluate("document.querySelectorAll('input[name=topic]').length") == 4 and
          pg.evaluate("document.querySelectorAll('input[name=topic]:checked').length") == 0 and
          pg.evaluate("document.querySelectorAll('input[name^=consent]:checked').length") == 0)
    check("  the choices are the ones in tools/form_text.py, in that order", pg.evaluate("[...document.querySelectorAll('input[name=topic]')].map(e => e.value + '|' + e.parentNode.textContent.trim())") == [f"{v}|{l}" for v, l in FT.TOPICS])
    svc, mkt = pg.evaluate("[...document.querySelectorAll('.check span')].map(e => e.textContent)")
    check("  the non-marketing text box says exactly what Joey's form says", svc == FT.CONSENT_SERVICE, svc)
    check("  the marketing text box says exactly what Joey's form says", mkt == FT.CONSENT_MARKETING, mkt)
    check("  both text boxes are optional, each its own checkbox with its own label", pg.evaluate("[...document.querySelectorAll('input[name^=consent]')].map(e => [e.type, e.required, !!e.closest('label')])") == [["checkbox", False, True]] * 2)
    check("  the first box says 'Message frequency varies' twice, exactly as his form does (kept; Joey is asked about it)", svc.count("Message frequency varies") == 2)
    fields = pg.evaluate("""[...document.querySelectorAll('#lf input:not([type=radio]):not([type=checkbox]), #lf textarea')].map(e => ({ id: e.id, type: e.type, ac: e.getAttribute('autocomplete'), im: e.getAttribute('inputmode'),
      req: e.required, label: (document.querySelector('label[for=' + e.id + ']') || {}).textContent, hidden: !!e.closest('[aria-hidden=true]') }))""")
    by = {f["id"]: f for f in fields}
    check("  Your name: text, autofill 'name', required, labelled", by["lf-name"]["type"] == "text" and by["lf-name"]["ac"] == "name" and by["lf-name"]["req"] and by["lf-name"]["label"] == "Your name", by["lf-name"])
    check("  Phone number: tel keypad, autofill 'tel', required, labelled", by["lf-phone"]["type"] == "tel" and by["lf-phone"]["ac"] == "tel" and by["lf-phone"]["im"] == "tel" and by["lf-phone"]["req"] and by["lf-phone"]["label"] == "Phone number", by["lf-phone"])
    check("  Email: email keyboard, autofill 'email', optional", by["lf-email"]["type"] == "email" and by["lf-email"]["ac"] == "email" and not by["lf-email"]["req"], by["lf-email"])
    check("  Address: autofill 'address-line1', optional; note: a real text area, optional", by["lf-address"]["ac"] == "address-line1" and not by["lf-address"]["req"] and by["lf-message"]["type"] == "textarea" and not by["lf-message"]["req"])
    check("  every visible field has its own label (no placeholders doing a label's job)", all(f["label"] for f in fields if not f["hidden"]) and pg.evaluate("document.querySelectorAll('#lf [placeholder]').length") == 0)
    check("  the trap field is hidden from people and from screen readers, and is not in the tab order", by["lf-web"]["hidden"] and pg.evaluate("document.getElementById('lf-web').tabIndex") == -1)
    check("  and it takes no room and cannot be seen: a tiny clipped box in place, not a box parked far off to the side", pg.evaluate("""(() => { const w = document.getElementById('lf-web').closest('.lf-hp'), r = w.getBoundingClientRect(), s = getComputedStyle(w);
      return r.width <= 1.5 && r.height <= 1.5 && r.left >= 0 && r.right <= document.documentElement.clientWidth + 1 && w.classList.contains('vh') && s.clipPath !== 'none'; })()"""))
    check("  the Privacy Policy and Terms links open in a new tab (so a half-filled form is not lost)", pg.evaluate("[...document.querySelectorAll('.lf-legal a')].map(a => a.target + '|' + a.rel + '|' + a.getAttribute('href'))") == ["_blank|noopener|privacy-policy.html", "_blank|noopener|terms-of-service.html"])
    check("  the button says what it does (nothing is connected yet, so it only prepares the message)", pg.inner_text(".lf-send").strip() == "Get my message ready", pg.inner_text(".lf-send"))
    check("  nothing was requested from outside the site (no analytics, no frame, no fonts from elsewhere)", all(u.startswith(BASE) or u.startswith("data:") for u in seen), [u for u in seen if not (u.startswith(BASE) or u.startswith("data:"))])
    check("  the details block is closed, so the form starts short", pg.evaluate("document.getElementById('lf-more').open") is False)

    # ============================================================= 2. checking
    pg.click(".lf-send")
    pg.wait_for_timeout(150)
    s = pg.evaluate(SHOW)
    check("empty Send: the box at the top shows, the form stays, nothing is handed off", s["sum"] and s["form"] and not s["hand"], s)
    check("  focus moved to the box (a keyboard or screen-reader user lands on it)", pg.evaluate(ACTIVE) == "lf-sum", pg.evaluate(ACTIVE))
    check("  both missing things are named, in plain words, next to the fields and in the box", pg.evaluate(ERRS) == ["Please tell us your name.", "Please add a phone number so we can reach you."] and
          pg.evaluate("[...document.querySelectorAll('#lf-sum li')].map(e => e.textContent)") == ["Please tell us your name.", "Please add a phone number so we can reach you."], pg.evaluate(ERRS))
    check("  both fields are marked invalid, and each is tied to its message", pg.evaluate(INVALID) == ["lf-name", "lf-phone"] and
          pg.evaluate("[...document.querySelectorAll('#lf-name,#lf-phone')].every(e => e.getAttribute('aria-describedby').split(' ').some(id => document.getElementById(id) && !document.getElementById(id).hidden))"))
    check("  the box is an alert (announced, by the box inside it) and says how many things", pg.get_attribute("#lf-sum", "role") is None and pg.evaluate("document.querySelectorAll('#lf-sum > [role=alert]').length") == 1 and "A few things" in pg.inner_text("#lf-sum"))
    check("  each message starts with a hidden 'Error:' for screen readers, and its icon is silent", pg.evaluate("[...document.querySelectorAll('.lf-err:not([hidden])')].every(e => e.querySelector('.vh') && e.querySelector('.vh').textContent === 'Error: ' && e.querySelector('svg').getAttribute('aria-hidden') === 'true')"))
    check("  the phone box also says why we ask (it stays in view next to the field)", pg.evaluate("document.getElementById('lf-phone-hint').textContent") == "So Joey or Ethan can reach you about your request." and
          pg.evaluate("document.getElementById('lf-phone').getAttribute('aria-describedby')") == "lf-phone-err lf-phone-hint")
    pg.click("#lf-sum a[data-for=phone]")
    check("  a line in the box takes the visitor to its field", pg.evaluate(ACTIVE) == "lf-phone", pg.evaluate(ACTIVE))
    pg.keyboard.type("423", delay=8)
    check("  while typing a fix, the message updates and then goes the moment the number is whole",
          "too short" in (pg.inner_text("#lf-phone-err") or "") and pg.evaluate(INVALID) == ["lf-name", "lf-phone"], pg.inner_text("#lf-phone-err"))
    check("  the box at the top follows (its phone line says the same), and what changes while someone types is not announced again", pg.evaluate("[...document.querySelectorAll('#lf-sum li')].map(e => e.textContent)") == pg.evaluate(ERRS) and pg.evaluate("document.querySelectorAll('#lf-sum [role=alert]').length") == 0, pg.evaluate("[...document.querySelectorAll('#lf-sum li')].map(e => e.textContent)"))
    pg.keyboard.type("4515707", delay=8)
    check("  ...and it goes the moment the number is whole", pg.evaluate(INVALID) == ["lf-name"] and pg.evaluate(ERRS) == ["Please tell us your name."], pg.evaluate(INVALID))
    check("  the box at the top is down to the one thing left, and its heading says so", pg.evaluate("[...document.querySelectorAll('#lf-sum li')].map(e => e.textContent)") == ["Please tell us your name."] and "One thing to check" in pg.inner_text("#lf-sum") and pg.evaluate(SHOW)["sum"], pg.inner_text("#lf-sum"))
    pg.fill("#lf-name", "J")
    pg.evaluate("document.getElementById('lf-name').dispatchEvent(new Event('input', {bubbles: true}))")
    check("  a one-letter name is not accepted, and the message stays until it is fixed", pg.evaluate(INVALID) == ["lf-name"])
    pg.fill("#lf-name", "Jane")
    pg.evaluate("document.getElementById('lf-name').dispatchEvent(new Event('input', {bubbles: true}))")
    check("  a name clears its message at once", pg.evaluate(INVALID) == [] and pg.evaluate(ERRS) == [])
    check("  and when the last thing is fixed the box at the top goes too (nothing left to check)", not pg.evaluate(SHOW)["sum"], pg.evaluate(SHOW))
    # leaving a field alone is not scolded; leaving a wrong one is told
    pg.reload(); open_form(pg)
    pg.click("#lf-name"); pg.keyboard.press("Tab")
    check("  tabbing through an empty field does not scold", pg.evaluate(INVALID) == [])
    pg.keyboard.type("42345", delay=8); pg.keyboard.press("Tab")
    check("  leaving a half-typed phone number does explain it (with the area-code example)", "(423) 555-0123" in pg.inner_text("#lf-phone-err") and pg.evaluate(INVALID) == ["lf-phone"], pg.inner_text("#lf-phone-err"))
    pg.fill("#lf-phone", "")
    pg.fill("#lf-phone", "42345157071")
    pg.evaluate("document.getElementById('lf-phone').dispatchEvent(new Event('blur'))")
    check("  eleven digits that do not start with 1: 'too many digits', and where an extension goes", "too many digits" in pg.inner_text("#lf-phone-err") and "extension can go in the note" in pg.inner_text("#lf-phone-err"), pg.inner_text("#lf-phone-err"))
    for bad_no in ("0000000000", "1111111111", "4230000000", "0234515707"):
        pg.fill("#lf-phone", bad_no); pg.evaluate("document.getElementById('lf-phone').dispatchEvent(new Event('blur'))")
        check(f"  {bad_no} cannot be a US number (an area code or exchange never starts with 0 or 1): explained, not accepted", "doesn\u2019t look right" in pg.inner_text("#lf-phone-err") and pg.evaluate(INVALID) == ["lf-phone"], pg.inner_text("#lf-phone-err"))
    pg.fill("#lf-phone", "")
    pg.click("#lf-phone"); pg.keyboard.type("1 423 451 5707", delay=8)
    check("  a leading 1 is left alone while typing", pg.input_value("#lf-phone") == "1 423 451 5707", pg.input_value("#lf-phone"))
    pg.keyboard.press("Tab")
    check("  ...and is tidied when the field is left (the 1 is not part of the number)", pg.input_value("#lf-phone") == "(423) 451-5707" and pg.evaluate(INVALID) == [], pg.input_value("#lf-phone"))
    pg.fill("#lf-phone", "+1 (423) 451-5707"); pg.evaluate("document.getElementById('lf-phone').dispatchEvent(new Event('change', {bubbles: true}))")
    pg.click("#lf-name")
    check("  +1 (423) 451-5707 is accepted and tidied", pg.input_value("#lf-phone") == "(423) 451-5707", pg.input_value("#lf-phone"))
    pg.fill("#lf-phone", "+44 20 7946 0958"); pg.evaluate("document.getElementById('lf-phone').dispatchEvent(new Event('change', {bubbles: true}))")
    pg.click("#lf-name")
    check("  a number from another country (+44 20 7946 0958) is accepted and left exactly as typed", pg.input_value("#lf-phone") == "+44 20 7946 0958" and pg.evaluate(INVALID) == [], (pg.input_value("#lf-phone"), pg.evaluate(INVALID)))
    pg.fill("#lf-phone", "+44 20 79"); pg.evaluate("document.getElementById('lf-phone').dispatchEvent(new Event('blur'))")
    check("  ...but a short one is explained, in words that mention the country code", "country code" in pg.inner_text("#lf-phone-err") and pg.evaluate(INVALID) == ["lf-phone"], pg.inner_text("#lf-phone-err"))
    pg.fill("#lf-phone", ""); pg.click("#lf-phone"); pg.keyboard.type("4234515707", delay=8)
    check("  typing ten digits gives (423) 451-5707", pg.input_value("#lf-phone") == "(423) 451-5707", pg.input_value("#lf-phone"))
    for _ in range(4):
        pg.keyboard.press("Backspace")
    check("  backspace takes one character at a time, through the dash and brackets (it never puts them back under the finger)", pg.input_value("#lf-phone") == "(423) 451-", pg.input_value("#lf-phone"))
    pg.keyboard.type("5707", delay=8)
    check("  ...and typing on afterwards continues the format", pg.input_value("#lf-phone") == "(423) 451-5707", pg.input_value("#lf-phone"))
    pg.keyboard.type("9", delay=8)
    check("  an eleventh digit is not hidden: the number is left as typed and Send says 'too many digits'", pg.input_value("#lf-phone") == "(423) 451-57079", pg.input_value("#lf-phone"))
    pg.fill("#lf-phone", ""); pg.evaluate("navigator.clipboard && 0")
    pg.evaluate("(() => { const e = document.getElementById('lf-phone'); e.focus(); e.value = '423-451-5707'; e.dispatchEvent(new InputEvent('input', {bubbles: true, inputType: 'insertFromPaste'})); })()")
    check("  a pasted 423-451-5707 is formatted", pg.input_value("#lf-phone") == "(423) 451-5707", pg.input_value("#lf-phone"))
    # an edit in the middle must not jump the cursor
    pg.fill("#lf-phone", "(423) 451-5707"); pg.click("#lf-phone")
    pg.evaluate("document.getElementById('lf-phone').setSelectionRange(4, 4)")
    pg.keyboard.type("9", delay=8)
    check("  typing in the middle of the number leaves the cursor where it was", pg.evaluate("document.getElementById('lf-phone').selectionStart") == 5, pg.evaluate("document.getElementById('lf-phone').selectionStart"))
    # email
    pg.fill("#lf-phone", "(423) 451-5707"); pg.fill("#lf-name", "Jane Smith")
    pg.click("#lf-more summary"); pg.fill("#lf-email", "jane@@example")
    pg.click(".lf-send")
    pg.wait_for_timeout(150)
    check("a wrong email is explained and nothing is handed off", "should look like name@example.com" in pg.inner_text("#lf-email-err") and pg.evaluate(INVALID) == ["lf-email"] and pg.evaluate(SHOW)["form"], pg.inner_text("#lf-email-err"))
    pg.click("#lf-more summary"); pg.click(".lf-send"); pg.wait_for_timeout(150)
    check("  with the extras closed, a wrong email opens them so the problem is in sight", pg.evaluate("document.getElementById('lf-more').open") is True)
    pg.click("#lf-more summary")   # shut them again
    pg.click("#lf-sum a[data-for=email]")
    check("  the line in the box about the email opens the extras again if they were shut, and lands on the field", pg.evaluate("document.getElementById('lf-more').open") is True and pg.evaluate(ACTIVE) == "lf-email", pg.evaluate(ACTIVE))
    pg.fill("#lf-email", "")
    pg.click(".lf-send"); pg.wait_for_timeout(200)
    check("an empty email is fine (it is optional): Send goes through", pg.evaluate(SHOW)["hand"], pg.evaluate(SHOW))
    check("  the box with the problems is gone", not pg.evaluate(SHOW)["sum"])
    ctx.close()

    # where the box with the problems lands after Send: in sight, just under the sticky header (a phone, a phone on its side, a small old phone)
    for who, w, h in (("phone", 390, 844), ("phone on its side", 844, 390), ("small phone", 320, 568)):
        ctx, pg, errs = ctx_page(b, w, h, True)
        open_form(pg)
        pg.click(".lf-send"); pg.wait_for_timeout(900)
        r = pg.evaluate("""() => { const b = document.getElementById('lf-sum').getBoundingClientRect(), hd = document.querySelector('.hdr').getBoundingClientRect(); return { top: Math.round(b.top), bottom: Math.round(b.bottom), hdr: Math.round(hd.bottom), H: innerHeight }; }""")
        check(f"{who} ({w}x{h}): after Send the box with the problems is in sight, right under the header", r["top"] >= r["hdr"] - 1 and r["top"] <= r["hdr"] + 60 and r["bottom"] <= r["H"], r)
        ctx.close()

    # before the form's script has run (a slow connection: the form is on screen a moment before it is ready): Enter and Send must not put the details in the address bar
    ctx, pg, errs = ctx_page(b, blank_js=True)
    pg.goto(BASE + "contact.html", wait_until="load")
    pg.keyboard.press("Shift")
    pg.add_style_tag(content=".mobile-bar{display:none!important}")
    pg.locator("#lf").scroll_into_view_if_needed()
    before = pg.url
    check("script not run yet: the form is showing (so this test means something)", pg.evaluate(SHOW)["form"] and not pg.evaluate(SHOW)["nojs"], pg.evaluate(SHOW))
    pg.fill("#lf-name", "Jane Smith"); pg.fill("#lf-phone", "4234515707")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(300)
    pg.click(".lf-send"); pg.wait_for_timeout(300)
    check("  pressing Enter or Send then does nothing, and puts nothing in the address bar (the details never travel in a web address)", pg.url == before and "Jane" not in pg.url and "4234515707" not in pg.url and "?" not in pg.url.split("#")[0], pg.url)
    ctx.close()

    # ============================================================= 3. the choices, and a button that says what the visitor wants
    ctx, pg, errs = ctx_page(b)
    open_form(pg, "contact.html", "?for=new")
    check("?for=new in the address ticks 'A new home'", pg.evaluate("document.querySelector('input[name=topic]:checked').value") == "new")
    open_form(pg, "contact.html", "?for=bogus")
    check("?for=bogus is ignored (nothing ticked, no error)", pg.evaluate("document.querySelectorAll('input[name=topic]:checked').length") == 0 and not errs, errs)
    open_form(pg, "contact.html", "?for=%22%3E%3Cscript%3E")
    check("a hostile ?for= is ignored", pg.evaluate("document.querySelectorAll('input[name=topic]:checked').length") == 0 and not errs, errs)
    pg.goto(BASE + "index.html"); pg.keyboard.press("Shift")
    pg.add_style_tag(content=".mobile-bar{display:none!important}")
    pg.evaluate("document.querySelectorAll('.rv').forEach(e => e.classList.add('in'))")
    pg.evaluate("document.querySelector('a[data-topic=new]').click()")
    check("Home: the 'Ask about this home' button ticks 'A new home' as it scrolls to the form", pg.evaluate("document.querySelector('input[name=topic]:checked').value") == "new" and pg.evaluate("location.hash") == "#contact", pg.evaluate("location.hash"))
    pg.evaluate("document.querySelector('a[data-topic=sell]').click()")
    check("  the net sheet's 'Go over these numbers' button ticks 'Selling my home'", pg.evaluate("document.querySelector('input[name=topic]:checked').value") == "sell")
    pg.goto(BASE + "options.html"); pg.keyboard.press("Shift")
    hr = pg.evaluate("[...document.querySelectorAll('a[data-topic]')].map(a => a.getAttribute('data-topic') + ' ' + a.getAttribute('href'))")
    check("Options: each path's button (and the closing band) carries its own choice to the Contact page", hr == ["sell contact.html?for=sell#contact", "sell contact.html?for=sell#contact", "keep contact.html?for=keep#contact", "unsure contact.html?for=unsure#contact", "unsure contact.html?for=unsure#contact"], hr)
    pg.click("a[data-topic=keep]"); pg.wait_for_load_state("load")
    check("  following the 'keep' button lands on the form with 'Keeping my home' ticked", pg.evaluate("location.pathname.endsWith('contact.html')") and pg.evaluate("document.querySelector('input[name=topic]:checked') && document.querySelector('input[name=topic]:checked').value") == "keep" and pg.evaluate("location.hash") == "#contact", pg.url)
    pg.goto(BASE + "new-homes.html"); pg.keyboard.press("Shift")
    hr = pg.evaluate("[...document.querySelectorAll('a[data-topic]')].map(a => a.getAttribute('href'))")
    check("New homes: both 'Ask about this home' buttons and the closing band carry 'A new home'", hr.count("contact.html?for=new#contact") == 3, hr)
    # the choices are a real radio group: arrow keys move the tick, one at a time
    pg.goto(BASE + "contact.html"); pg.keyboard.press("Shift")
    pg.focus("input[name=topic][value=sell]"); pg.keyboard.press("Space")
    pg.keyboard.press("ArrowRight")
    check("keyboard: Space ticks a choice and an arrow moves to the next (only one is ever ticked)", pg.evaluate("document.querySelector('input[name=topic]:checked').value") == "keep" and pg.evaluate("document.querySelectorAll('input[name=topic]:checked').length") == 1)
    pg.click("label.pill:nth-child(3)")
    check("  tapping a choice ticks it", pg.evaluate("document.querySelector('input[name=topic]:checked').value") == "new")
    ctx.close()

    # ============================================================= 4. nothing connected yet: the ready-made message (a computer, then a phone)
    for who, w, mobile in (("desktop", 1280, False), ("phone", 390, True)):
        rec = []
        ctx, pg, errs = ctx_page(b, w, 900 if not mobile else 844, mobile, grant=True, record=rec)
        open_form(pg)
        pg.click("label.pill:nth-child(1)")
        fill_valid(pg, "jane   smith")
        pg.check("input[name=consent_service]", force=True)
        pg.click(".lf-send"); pg.wait_for_timeout(250)
        s = pg.evaluate(SHOW)
        check(f"{who}: Send shows the ready-made message and hides the form", s["hand"] and not s["form"] and not s["done"], s)
        check(f"  focus is on the message panel (announced), whose heading says nothing has been sent", pg.evaluate(ACTIVE) == "lf-hand" and "ready to send" in pg.inner_text("#lf-hand-h") and "Nothing has been sent yet" in pg.inner_text("#lf-hand"), pg.evaluate(ACTIVE))
        msg = pg.inner_text("#lf-msg")
        check("  the message names the visitor, what they want, how to reach them, and carries their note (spaces tidied)",
              msg.startswith("Hi Joey and Ethan, this is jane smith. I'm reaching out from your website.") and "Interested in: Selling my home" in msg and "Best number: (423) 451-5707" in msg and
              "Email: jane@example.com" in msg and "Home address or ZIP: 123 Main St, Hixson 37343" in msg and msg.endswith("My mom's house.\nEvenings are best."), msg)
        check("  the box they ticked is named in one plain line (the other is not), and none of the box wording is copied in", "Text messages OK (non-marketing): yes" in msg and "Text messages OK (marketing): yes" not in msg and "consent" not in msg.lower() and "STOP" not in msg, msg)
        sms, mail = hrefs(pg)
        check("  the text link is sms:<number>?&body=<the message>, which iPhone and Android both read", sms == SMS_BASE + "?&body=" + msg, sms[:80])
        check("  the email link goes to the company address, with who and what in the subject, and the message (line breaks as CRLF)", mail.startswith(f"mailto:{EMAIL}?subject=Website request from jane smith - Selling my home&body=") and mail.split("&body=", 1)[1] == msg.replace("\n", "\r\n"), mail[:90])
        check("  no curly quotes in what is sent (a text with one costs double)", not re.search("[‘’“”]", sms + mail))
        first = pg.evaluate("document.querySelector('.lf-actions a').id")
        check(f"  {'the text button comes first and is the green one (a phone)' if mobile else 'the email button comes first on a computer'}", first == ("lf-sms" if mobile else "lf-mail") and "btn-primary" in pg.get_attribute(f"#{first}", "class"), first)
        check("  the other way is still there, as the quiet button", "btn-ghost" in pg.get_attribute("#lf-mail" if mobile else "#lf-sms", "class"))
        check("  the phone number is offered too", PHONE_TXT in pg.inner_text(".lf-mini"))
        sw, mw = pg.inner_text("#lf-sms-t").strip(), pg.inner_text("#lf-mail-t").strip()
        check(f"  the words of the two buttons follow the order ({'text' if mobile else 'email'} is the main one; the other says 'or')",
              (sw, mw) == (("Text it to Joey & Ethan", "Or email it instead") if mobile else ("Or text it instead", "Email it to Joey & Ethan")), (sw, mw))
        lede_id = pg.get_attribute("#lf-hand", "aria-describedby")
        check("  the panel is described by the line that is showing (and says nothing about tapping, which a computer does not do)", lede_id == ("lf-lede-sms" if mobile else "lf-lede-mail") and pg.evaluate("id => { const e = document.getElementById(id); return !!e && !e.hidden; }", lede_id) and "Tap" not in pg.inner_text("#lf-hand"), (lede_id, pg.inner_text("#lf-hand")[:160]))
        lede = pg.inner_text("#" + lede_id)
        main_label = pg.inner_text("#lf-sms-t" if mobile else "#lf-mail-t").strip()
        check("  the line under the heading names the main button by its words (not its colour) and says what to do if nothing opens", f"\u201c{main_label}\u201d" in lede and "\u201cCopy my message\u201d" in lede and "call us" in lede and "green" not in lede.lower(), lede)
        check("  the message is marked 'do not translate' (a browser's translator would otherwise change what is about to be sent)", pg.get_attribute("#lf-msg", "translate") == "no")
        pg.wait_for_timeout(520)   # a panel ignores clicks for its first moments (a double-click on Send)
        pg.click("#lf-copy"); pg.wait_for_timeout(250)
        check("  Copy puts exactly the message on the clipboard and says so", pg.evaluate("navigator.clipboard.readText()") == msg and "Copied" in pg.inner_text("#lf-live"), pg.inner_text("#lf-live"))
        pg.click("#lf-edit"); pg.wait_for_timeout(200)
        check("  Change my details: the form is back, with everything still typed in, and the name field has focus",
              pg.evaluate(SHOW)["form"] and pg.input_value("#lf-name") == "jane   smith" and pg.input_value("#lf-phone") == "(423) 451-5707" and pg.input_value("#lf-email") == "jane@example.com" and
              pg.evaluate("document.querySelector('input[name=topic]:checked').value") == "sell" and pg.evaluate("document.querySelector('input[name=consent_service]').checked") and pg.evaluate(ACTIVE) == "lf-name", pg.evaluate(ACTIVE))
        check("  nothing went anywhere: no request left the page during all of it", [r for r in rec if r] == [], rec)
        check("  no script errors", errs == [], errs)
        ctx.close()

    # what they said they prefer wins
    for chan, want in (("email", "lf-mail"), ("text", "lf-sms")):
        ctx, pg, errs = ctx_page(b, 390, 844, True)
        open_form(pg)
        fill_valid(pg, extras=False)
        pg.click("#lf-more summary"); pg.click(f"label.pill:has(input[value={chan}])")
        pg.click(".lf-send"); pg.wait_for_timeout(200)
        check(f"a visitor who prefers {chan}: that button comes first, even on a phone", pg.evaluate("document.querySelector('.lf-actions a').id") == want and "Best way to reach me: " + chan.capitalize() in pg.inner_text("#lf-msg"), pg.evaluate("document.querySelector('.lf-actions a').id"))
        if chan == "email":
            check("  and the line under the heading talks about email", "email app" in pg.inner_text("#lf-hand"))
        ctx.close()

    # a computer, or a tablet, cannot send a text on its own: the email button comes first there, even for someone who prefers a text for the reply
    for who, w, h, mobile in (("computer", 1280, 900, False), ("tablet", 820, 1180, True)):
        ctx, pg, errs = ctx_page(b, w, h, mobile)
        open_form(pg)
        fill_valid(pg, extras=False)
        pg.click("#lf-more summary"); pg.click("label.pill:has(input[value=text])")
        pg.click(".lf-send"); pg.wait_for_timeout(200)
        first = pg.evaluate("document.querySelector('.lf-actions a').id")
        check(f"a {who}, and the visitor prefers a text for the reply: the email button still comes first (this device cannot send a text), and the message says what they prefer",
              first == "lf-mail" and "Best way to reach me: Text" in pg.inner_text("#lf-msg") and "email app" in pg.inner_text("#lf-hand"), first)
        ctx.close()

    # a double-click on Send (people do it): its second click must not land on a button of the panel that has just appeared
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, extras=False)
    pg.click(".lf-send"); pg.click("#lf-edit"); pg.wait_for_timeout(100)
    st = pg.evaluate(SHOW)
    check("a click on a button of the message panel in its first moments is ignored (a double-click on Send must not take the visitor back to the form)", st["hand"] and not st["form"], st)
    pg.wait_for_timeout(520); pg.click("#lf-edit"); pg.wait_for_timeout(150)
    check("  a moment later the same button works", pg.evaluate(SHOW)["form"] and not pg.evaluate(SHOW)["hand"], pg.evaluate(SHOW))
    ctx.close()

    # the same guard, two more ways: a click beside the card (on a phone the panel is shorter than the form, so the second click of a double-click can land on the tiles below it),
    # and a phone whose clock is set back just then (the guard must never count a negative time, or every button of the panel would be dead)
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, extras=False)
    pg.click(".lf-send")
    pg.evaluate("window.__beside = 0; window.__count = e => { window.__beside++; e.preventDefault(); }; window.addEventListener('click', window.__count); document.querySelector('.reach-main a').click()")   # the listener sees only clicks that nothing stopped on the way (and keeps the Call link from dialling)
    first = pg.evaluate("window.__beside")
    pg.wait_for_timeout(520)
    pg.evaluate("document.querySelector('.reach-main a').click()")
    later = pg.evaluate("window.__beside"); pg.evaluate("window.removeEventListener('click', window.__count)")
    check("a click on the Call tile (outside the card) in the first moments of the message panel is ignored; a moment later it goes through", first == 0 and later == 1, (first, later))
    pg.click("#lf-edit"); pg.wait_for_timeout(150)
    pg.click(".lf-send")
    pg.evaluate("(() => { const r = Date.now; Date.now = function () { return r.call(Date) - 60000; }; })()")
    pg.click("#lf-edit"); pg.wait_for_timeout(150)
    check("  with the phone's clock set back a minute just then, the panel's buttons still work", pg.evaluate(SHOW)["form"] and not pg.evaluate(SHOW)["hand"], pg.evaluate(SHOW))
    ctx.close()

    # Copy in a browser with no clipboard (the older way of copying takes the keyboard's place for a moment: it must be given back)
    ctx, pg, errs = ctx_page(b)
    pg.add_init_script("Object.defineProperty(navigator, 'clipboard', { value: undefined, configurable: true })")
    open_form(pg)
    fill_valid(pg, extras=False)
    pg.click(".lf-send"); pg.wait_for_timeout(520)
    pg.focus("#lf-copy"); pg.keyboard.press("Enter"); pg.wait_for_timeout(250)
    check("Copy in a browser with no clipboard: the keyboard stays on the Copy button, and the page says what happened", pg.evaluate(ACTIVE) == "lf-copy" and pg.inner_text("#lf-live").strip() != "", (pg.evaluate(ACTIVE), pg.inner_text("#lf-live")))
    ctx.close()

    # a minimal message: only what was given
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, "Sam Lee", "4235550100", extras=False)
    pg.click(".lf-send"); pg.wait_for_timeout(200)
    check("a name and a number alone make a short, tidy message (no empty lines of 'Email:' or 'Address:')", pg.inner_text("#lf-msg") == "Hi Joey and Ethan, this is Sam Lee. I'm reaching out from your website.\n\nBest number: (423) 555-0100", pg.inner_text("#lf-msg"))
    check("  and the email subject is just who, when no choice was made", urllib.parse.unquote(pg.get_attribute("#lf-mail", "href")).startswith(f"mailto:{EMAIL}?subject=Website request from Sam Lee&body="), urllib.parse.unquote(pg.get_attribute("#lf-mail", "href"))[:90])
    ctx.close()

    # both text-message boxes ticked
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, "Sam Lee", "4235550100", extras=False)
    pg.check("input[name=consent_service]", force=True); pg.check("input[name=consent_marketing]", force=True)
    pg.click(".lf-send"); pg.wait_for_timeout(200)
    m = pg.inner_text("#lf-msg")
    check("both text-message boxes ticked: both are named, in the order they appear on the form, after the contact lines",
          m == "Hi Joey and Ethan, this is Sam Lee. I'm reaching out from your website.\n\nBest number: (423) 555-0100\nText messages OK (non-marketing): yes\nText messages OK (marketing): yes", m)
    ctx.close()

    # a number from another country, and an ellipsis, curly quotes and a long dash in the note
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    pg.fill("#lf-name", "Ann Bell"); pg.click("#lf-phone"); pg.keyboard.type("+44 20 7946 0958", delay=8)
    pg.click("#lf-more summary"); pg.fill("#lf-message", "It\u2019s \u201cold\u201d\u2026 call me \u2013 any time")
    pg.click(".lf-send"); pg.wait_for_timeout(200)
    m = pg.inner_text("#lf-msg")
    check("a number from another country goes into the message as typed; an ellipsis, curly quotes and a long dash become plain characters",
          "Best number: +44 20 7946 0958" in m and m.endswith("It's \"old\"... call me - any time"), m)
    ctx.close()

    # half of an emoji (a broken paste): swapped for the usual replacement mark, and the form still works
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, "Lee Wong", extras=False)
    pg.click("#lf-more summary")
    pg.evaluate(r"document.getElementById('lf-message').value = 'Call me \uD83D please \uDE00'")
    pg.click(".lf-send"); pg.wait_for_timeout(250)
    m = pg.inner_text("#lf-msg")
    check("half of an emoji in the note (a broken paste) becomes the usual replacement mark, and the ready-made message still appears", pg.evaluate(SHOW)["hand"] and m.endswith("Call me � please �") and errs == [], (m[-40:], errs))
    ctx.close()

    # several halves of emoji in a row (a worse broken paste): each is swapped, a whole emoji stays
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, "Lee Wong", extras=False)
    pg.click("#lf-more summary")
    pg.evaluate(r"document.getElementById('lf-message').value = 'Hi \uDE00\uDE00\uDE00 there \uD83D\uDE0A ok \uD83D\uD83D'")
    pg.click(".lf-send"); pg.wait_for_timeout(250)
    m = pg.inner_text("#lf-msg")
    check("several halves of emoji in a row are each swapped for the replacement mark, a whole emoji is kept, and the ready-made message still appears", pg.evaluate(SHOW)["hand"] and m.endswith("Hi \ufffd\ufffd\ufffd there \U0001F60A ok \ufffd\ufffd") and errs == [], (m[-40:], errs))
    ctx.close()

    # the trap field filled while nothing is connected (a password manager can do that): the person must still get their message, never a false thank-you
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, "Pat Real", extras=False)
    pg.evaluate("document.getElementById('lf-web').value = 'https://example.com'")
    pg.click(".lf-send"); pg.wait_for_timeout(250)
    s = pg.evaluate(SHOW)
    check("nothing connected, trap field filled: the ready-made message shows (not a thank-you that would be untrue)", s["hand"] and not s["done"] and "Nothing has been sent yet" in pg.inner_text("#lf-hand") and "Pat Real" in pg.inner_text("#lf-msg"), s)
    check("  and the trap field's content is not in what is sent", "example.com" not in pg.inner_text("#lf-msg") and "example.com" not in urllib.parse.unquote(pg.get_attribute("#lf-sms", "href") + pg.get_attribute("#lf-mail", "href")))
    ctx.close()

    # ============================================================= 5. connected: posts to FORM_ENDPOINT
    def answer(code, ok_headers=True):
        def h(route):
            hd = {"Access-Control-Allow-Origin": "*"} if ok_headers else {}
            route.fulfill(status=code, headers=hd, body="ok")
        return h
    rec = []
    ctx, pg, errs = ctx_page(b, record=rec, hook=answer(200), endpoint=True)
    open_form(pg)
    pg.click("label.pill:nth-child(2)")
    fill_valid(pg, "pat jones")
    pg.check("input[name=consent_marketing]", force=True)
    pg.dblclick(".lf-send"); pg.wait_for_timeout(500)
    posts = [r for r in rec if r.get("method") == "POST"]
    check("connected: pressing Send twice fast posts once", len(posts) == 1, len(posts))
    data = json.loads(posts[0]["body"]) if posts else {}
    check("  the post is plain text/JSON (no pre-flight needed), and carries every field except the trap", posts and posts[0]["type"].startswith("text/plain") and
          set(data) == set(FT.FIELDS) - {"website"}, sorted(data))
    check("  the values are right (tidy name, formatted number, the choice, both boxes as true/false, the page)", data.get("name") == "pat jones" and data.get("phone") == "(423) 451-5707" and data.get("topic") == "keep" and data.get("topic_label") == "Keeping my home" and
          data.get("consent_service") is False and data.get("consent_marketing") is True and data.get("email") == "jane@example.com" and data.get("page", "").endswith("/contact.html") and re.match(r"\d{4}-\d\d-\d\dT", data.get("sent_at", "")), data)
    check("  it says which wording of the text-message boxes was on screen, and how many seconds the visitor took", data.get("consent_version") == FT.consent_version() and isinstance(data.get("seconds_on_form"), int) and 0 <= data["seconds_on_form"] < 120, (data.get("consent_version"), data.get("seconds_on_form")))
    s = pg.evaluate(SHOW)
    check("  'Thank you' shows, with the first name, and the form and the ready-made message do not", s["done"] and not s["form"] and not s["hand"] and "Thank you, Pat." in pg.inner_text("#lf-done-h"), pg.inner_text("#lf-done-h"))
    check("  it makes no promise about time, and the phone number is there", s["done"] and not re.search(r"\b(hour|minute|day|soon|quickly|today|24|48)", pg.inner_text("#lf-done").lower()) and PHONE_TXT in pg.inner_text("#lf-done"), pg.inner_text("#lf-done"))
    check("  focus is on the thank-you (announced)", pg.evaluate(ACTIVE) == "lf-done")
    pg.wait_for_timeout(520); pg.click("#lf-again"); pg.wait_for_timeout(200)
    check("  'Send another message' gives a fresh form (everything cleared, the extras closed again)", pg.evaluate(SHOW)["form"] and pg.input_value("#lf-name") == "" and pg.input_value("#lf-phone") == "" and pg.evaluate("document.querySelectorAll('input:checked').length") == 0 and pg.evaluate(ACTIVE) == "lf-name" and pg.evaluate("document.getElementById('lf-more').open") is False)
    # the trap field: the page never judges it. It is posted (with how long the form had been open) and the receiving end decides; the visitor sees
    # a thank-you only because the receiving end answered, never because the page made one up
    rec.clear()
    fill_valid(pg, "Robot Rob", extras=False)
    pg.evaluate("document.getElementById('lf-web').value = 'http://spam.example'")
    pg.click(".lf-send"); pg.wait_for_timeout(400)
    posts = [r for r in rec if r.get("method") == "POST"]
    d2 = json.loads(posts[0]["body"]) if posts else {}
    check("  a trap field filled (fast, as a robot would): the request is still posted, with the trap field and the seconds in it, for the receiving end to judge",
          len(posts) == 1 and d2.get("website") == "http://spam.example" and d2.get("name") == "Robot Rob" and isinstance(d2.get("seconds_on_form"), int) and d2["seconds_on_form"] < 60, (len(posts), d2.get("website"), d2.get("seconds_on_form")))
    check("  and the thank-you shows because the receiving end answered", pg.evaluate(SHOW)["done"])
    # a name that is a title and a surname: the thank-you must not read 'Thank you, Mrs..'
    pg.wait_for_timeout(520); pg.click("#lf-again"); pg.wait_for_timeout(150)
    fill_valid(pg, "Mrs. Smith", extras=False)
    pg.click(".lf-send"); pg.wait_for_timeout(400)
    check("  a name like 'Mrs. Smith' gets a plain 'Thank you.' (no title in the greeting)", pg.inner_text("#lf-done-h").strip() == "Thank you.", pg.inner_text("#lf-done-h"))
    check("  no script errors", errs == [], errs)
    ctx.close()

    # connected, posting as an ordinary web form (FORM_FORMAT = "form")
    rec = []
    ctx, pg, errs = ctx_page(b, record=rec, hook=answer(200), endpoint="form")
    open_form(pg)
    pg.click("label.pill:nth-child(3)")
    fill_valid(pg, "pat o'neil & sons")
    pg.check("input[name=consent_service]", force=True)
    pg.click(".lf-send"); pg.wait_for_timeout(500)
    posts = [r for r in rec if r.get("method") == "POST"]
    parsed = dict(urllib.parse.parse_qsl(posts[0]["body"], keep_blank_values=True)) if posts else {}
    check("posting as a web form: one post, as name=value&name=value, with the usual form content type", len(posts) == 1 and posts[0]["type"].startswith("application/x-www-form-urlencoded"), [(r.get("type"), (r.get("body") or "")[:60]) for r in posts])
    check("  every field is there (the trap field is not), booleans are yes/no, awkward characters survive", set(parsed) == set(FT.FIELDS) - {"website"} and parsed.get("consent_service") == "yes" and parsed.get("consent_marketing") == "no" and
          parsed.get("name") == "pat o'neil & sons" and parsed.get("phone") == "(423) 451-5707" and parsed.get("topic") == "new" and parsed.get("message") == "My mom's house.\nEvenings are best.", parsed)
    check("  'Thank you' shows", pg.evaluate(SHOW)["done"])
    ctx.close()

    def unreachable(route):
        route.abort("failed")   # what the page sees when the receiving end is down, offline, or its answer is blocked by the browser
    for label, hook, ok_headers in (("a refusal (500)", answer(500), True), ("a connection that fails (down, offline, or an answer the browser blocks)", unreachable, False)):
        rec = []
        ctx, pg, errs = ctx_page(b, 390, 844, True, record=rec, hook=hook, endpoint=True)
        open_form(pg)
        fill_valid(pg, extras=False)
        label0 = pg.inner_text(".lf-send").strip()
        pg.click(".lf-send"); pg.wait_for_timeout(700)
        s = pg.evaluate(SHOW)
        check(f"connected, but {label}: the visitor gets the text and email hand-off, not a dead end", s["hand"] and not s["done"] and "couldn\u2019t confirm that was sent" in pg.inner_text("#lf-hand-h"), pg.inner_text("#lf-hand-h"))
        check("  it says the details are still there and offers the phone number", "still here" in pg.inner_text("#lf-hand") and PHONE_TXT in pg.inner_text("#lf-hand"), pg.inner_text("#lf-hand"))
        check("  the Send button is back to normal (not stuck on 'Sending')", pg.get_attribute(".lf-send", "aria-busy") is None and pg.inner_text(".lf-send").strip() == label0 == "Send to Joey & Ethan" and pg.evaluate("document.querySelectorAll('.lf-send .spin').length") == 0, (label0, pg.inner_text(".lf-send")))
        pg.wait_for_timeout(520); pg.click("#lf-edit"); pg.wait_for_timeout(150)
        check("  Change my details still works, and Send can be tried again", pg.evaluate(SHOW)["form"] and pg.input_value("#lf-name") == "Jane Smith")
        ctx.close()

    rec = []
    ctx, pg, errs = ctx_page(b, 390, 844, True, record=rec, hook=answer(500), endpoint=True)
    open_form(pg)
    fill_valid(pg, "Pat Real", extras=False)
    pg.evaluate("document.getElementById('lf-web').value = 'https://example.com'")
    pg.click(".lf-send"); pg.wait_for_timeout(700)
    s = pg.evaluate(SHOW)
    check("connected, a trap field filled, and the receiving end refuses: the visitor gets the hand-off, never a made-up thank-you", s["hand"] and not s["done"] and "couldn\u2019t confirm" in pg.inner_text("#lf-hand-h"), s)
    ctx.close()

    held = []
    ctx, pg, errs = ctx_page(b, 390, 844, True, hook=lambda route: held.append(route), endpoint=True)   # the answer is held back until the test lets it go
    open_form(pg)
    fill_valid(pg, "Pat Real", extras=False)
    pg.click(".lf-send"); pg.wait_for_timeout(300)
    pg.fill("#lf-name", "")   # the visitor empties a box while it waits
    held[0].fulfill(status=500, headers={"Access-Control-Allow-Origin": "*"}, body="no")
    pg.wait_for_timeout(500)
    m = pg.inner_text("#lf-msg")
    check("connected, the receiving end refuses, and the visitor had emptied the name box while it waited: the hand-off uses the details that were sent (never 'this is .')", pg.evaluate(SHOW)["hand"] and m.startswith("Hi Joey and Ethan, this is Pat Real.") and "Best number: (423) 451-5707" in m, m[:90])
    ctx.close()

    if LONG:
        def silent(route):
            pass   # never answers
        rec = []
        ctx, pg, errs = ctx_page(b, 390, 844, True, record=rec, hook=silent, endpoint=True)
        open_form(pg)
        fill_valid(pg, extras=False)
        pg.click(".lf-send"); pg.wait_for_timeout(1000)
        check("connected, but silent: while it waits the button says Sending, cannot be pressed again, and a screen reader is told", pg.get_attribute(".lf-send", "aria-busy") == "true" and "Sending" in pg.inner_text(".lf-send") and "Sending your details" in pg.inner_text("#lf-status"))
        pg.wait_for_timeout(15500)
        check("  after 15 seconds the visitor gets the hand-off", pg.evaluate(SHOW)["hand"] and "couldn\u2019t confirm" in pg.inner_text("#lf-hand-h"))
        ctx.close()

    # ============================================================= 6. no JavaScript
    ctx, pg, errs = ctx_page(b, js=False)
    pg.goto(BASE + "contact.html")
    s = pg.evaluate(SHOW)
    check("no JavaScript: the form is hidden and the call/text/email card shows", s["nojs"] and not s["form"] and not s["hand"] and not s["done"], s)
    links = pg.evaluate("[...document.querySelectorAll('.lf-nojs a')].map(a => a.getAttribute('href') + '|' + a.textContent.trim())")
    check("  the card's Call, Text and Email links are real", links == [f"tel:+1{PHONE.group(1)}|Call {PHONE_TXT}", f"{SMS_BASE}|Text us", f"mailto:{EMAIL}|Email us"], links)
    check("  the 'prefer to talk' line is not repeated under the card", pg.evaluate("getComputedStyle(document.querySelector('.form-alt')).display") == "none")
    ctx.close()

    # ============================================================= 6b. a very slow connection
    # the 6-second timer in the head swaps the form for the call-and-text card when the scripts have not run; when they do arrive after all, the form must come back, working
    ctx, pg, errs = ctx_page(b, slow=7)
    pg.add_init_script("window.__jsLog = []; new MutationObserver(function (ms) { for (var i = 0; i < ms.length; i++) if (ms[i].target === document.documentElement) __jsLog.push(document.documentElement.classList.contains('js')); }).observe(document, { attributes: true, subtree: true, attributeFilter: ['class'] });")   # (the document exists when this runs; the <html> element may not yet)
    pg.goto(BASE + "contact.html", wait_until="load")
    pg.keyboard.press("Shift")
    pg.add_style_tag(content=".mobile-bar{display:none!important}")
    pg.evaluate("document.querySelectorAll('.rv').forEach(e => e.classList.add('in'))")
    log = pg.evaluate("window.__jsLog")
    check("scripts that arrive after the 6-second timer: the page had swapped the form for the card, and when they arrived the form came back (js class on, off, on)", len(log) >= 3 and log[0] is True and False in log and log[-1] is True and log.index(False) < len(log) - 1, log)
    s = pg.evaluate(SHOW)
    check("  the form shows again (not the card), and it works", s["form"] and not s["nojs"], s)
    pg.locator("#lf").scroll_into_view_if_needed()
    fill_valid(pg, extras=False)
    pg.click(".lf-send"); pg.wait_for_timeout(300)
    check("  Send gives the ready-made message", pg.evaluate(SHOW)["hand"], pg.evaluate(SHOW))
    ctx.close()

    # ============================================================= 7. fit
    def fit_report(pg):
        return pg.evaluate("""() => {
          const card = document.querySelector('.form-card'), cr = card.getBoundingClientRect(), W = window.innerWidth, out = { sideways: document.documentElement.scrollWidth > W, over: [], small: [], zoom: [] };
          const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !e.closest('[aria-hidden=true]'); };
          card.querySelectorAll('input:not([type=radio]):not([type=checkbox]),textarea,button,a,summary,.pill span,.check,.lf-checks,.lf-sum,.lf-msg,legend').forEach(e => {
            if (!vis(e)) return; const r = e.getBoundingClientRect();
            if (r.left < cr.left - 1 || r.right > cr.right + 1) out.over.push((e.id || e.className || e.tagName) + ' ' + Math.round(r.left - cr.left) + '/' + Math.round(cr.right - r.right));
            if (e.scrollWidth > e.clientWidth + 1 && !e.matches('a,input,textarea')) out.over.push('clipped: ' + (e.id || e.className || e.tagName));
          });
          card.querySelectorAll('input:not([type=radio]):not([type=checkbox]),textarea,button,summary,.pill,.check,.lf-mini a,.lf-mini button,.lf-sum a').forEach(e => {
            if (!vis(e)) return; const r = e.getBoundingClientRect();
            if (r.height < 43.5) out.small.push((e.id || e.className || e.tagName) + ' h=' + Math.round(r.height));
          });
          card.querySelectorAll('input:not([type=radio]):not([type=checkbox]),textarea').forEach(e => { if (vis(e) && parseFloat(getComputedStyle(e).fontSize) < 16) out.zoom.push(e.id + ' ' + getComputedStyle(e).fontSize); });
          return out; }""")

    for w, mobile in ((320, True), (360, True), (390, True), (430, True), (768, False), (1024, False), (1280, False), (1440, False)):
        for page in ("contact.html", "index.html"):
            ctx, pg, errs = ctx_page(b, w, 900 if not mobile else 844, mobile)
            open_form(pg, page)
            r = fit_report(pg)
            check(f"{page} at {w}px: nothing sideways, nothing out of the card, targets 44px+, typing will not zoom a phone", not r["sideways"] and not r["over"] and not r["small"] and not r["zoom"], r)
            if page == "contact.html":
                pg.click("#lf-more summary")
                pg.click(".lf-send"); pg.wait_for_timeout(150)
                r = fit_report(pg)
                check(f"  {w}px with the extras open and the errors showing", not r["sideways"] and not r["over"] and not r["small"] and not r["zoom"], r)
                fill_valid(pg, "A Very Long Name Indeed Mr Bartholomew Featherstonehaugh-Worthington", extras=False)
                pg.fill("#lf-message", "x" * 200)
                pg.click(".lf-send"); pg.wait_for_timeout(200)
                r = fit_report(pg)
                check(f"  {w}px, the ready-made message with a long name and a long unbroken note", not r["sideways"] and not r["over"] and not r["small"], r)
            ctx.close()
    for pct in (150, 200):
        for w, mobile in ((390, True), (1280, False)):
            ctx, pg, errs = ctx_page(b, w, 844, mobile)
            open_form(pg)
            pg.add_style_tag(content=f"html{{font-size:{pct}%!important}}")
            pg.wait_for_timeout(100)
            r = fit_report(pg)
            check(f"text at {pct}% on a {w}px screen: nothing sideways, nothing out of the card", not r["sideways"] and not r["over"], r)
            pg.click(".lf-send"); pg.wait_for_timeout(150)
            r = fit_report(pg)
            check(f"  ...with the errors showing", not r["sideways"] and not r["over"], r)
            ctx.close()

    # where the form sits
    POS = """() => { const t = id => document.querySelector(id).getBoundingClientRect();
      return { top: t('.contact-top'), main: t('.reach-main'), card: t('.form-card'), more: t('.reach-more'), next: t('.next') }; }"""
    ctx, pg, errs = ctx_page(b, 390, 844, True)
    open_form(pg)
    pos = pg.evaluate(POS)
    short = {k: (round(v["top"]), round(v["bottom"])) for k, v in pos.items()}
    check("phone: heading, then Call and Text, then the form, then Email / Book / Facebook, then the three steps (one column)",
          pos["top"]["bottom"] <= pos["main"]["top"] + 1 and pos["main"]["bottom"] <= pos["card"]["top"] + 1 and pos["card"]["bottom"] <= pos["more"]["top"] + 1 and pos["more"]["bottom"] <= pos["next"]["top"] + 1, short)
    top_card, top_name = pg.evaluate("window.scrollTo(0, 0); [document.querySelector('.form-card').getBoundingClientRect().top, document.getElementById('lf-name').getBoundingClientRect().top]")
    check("  on Contact the Call and Text tiles and the start of the form are on the first screen of a phone, and the first box is under two screens down", pos["main"]["bottom"] < 844 and top_card < 844 and top_name < 844 * 1.6, (round(top_card), round(top_name)))
    check("  the photo of Joey and Ethan under the steps stays hidden on a phone (Checkpoint 48: computers only)",
          pg.evaluate("(() => { const e = document.querySelector('.contact-photo'); return !!e && getComputedStyle(e).display === 'none'; })()"))
    ctx.close()
    # Checkpoint 48: on the Contact page the heading runs across both columns (beside the form it took four lines), so there the form
    # starts right under the heading, level with the Call and Text tiles, and the photo of Joey and Ethan sits under the steps.
    # Home keeps the form level with the heading. Both keep the left column's order.
    def left_column(pos):
        return (pos["main"]["right"] <= pos["card"]["left"] and pos["more"]["right"] <= pos["card"]["left"] and pos["next"]["right"] <= pos["card"]["left"] and
                pos["main"]["top"] >= pos["top"]["bottom"] and pos["more"]["top"] >= pos["main"]["bottom"] and pos["next"]["top"] >= pos["more"]["bottom"])
    ctx, pg, errs = ctx_page(b, 1440, 900)
    open_form(pg)
    pos = pg.evaluate(POS)
    photo = pg.evaluate("(() => { const e = document.querySelector('.contact-photo'); if (!e || getComputedStyle(e).display === 'none') return null; const r = e.getBoundingClientRect(); return {left: r.left, right: r.right, top: r.top, bottom: r.bottom}; })()")
    short = {k: (round(v["left"]), round(v["top"])) for k, v in pos.items()}
    check("computer, Contact: the heading runs across the top; under it the form is in the right-hand column, level with the Call and Text tiles; Call/Text, Email/Book/Facebook, the steps and the photo are in the left column, in that order",
          pos["top"]["right"] >= pos["card"]["right"] - 1 and pos["card"]["top"] >= pos["top"]["bottom"] and pos["card"]["top"] - pos["top"]["bottom"] < 60 and abs(pos["card"]["top"] - pos["main"]["top"]) < 90 and left_column(pos) and
          photo is not None and photo["right"] <= pos["card"]["left"] and photo["top"] >= pos["next"]["bottom"], (short, photo and (round(photo["left"]), round(photo["top"]))))
    ctx.close()
    ctx, pg, errs = ctx_page(b, 1440, 900)
    open_form(pg, "index.html")
    pos = pg.evaluate(POS)
    short = {k: (round(v["left"]), round(v["top"])) for k, v in pos.items()}
    check("computer, Home: the form is in the right-hand column, level with the heading; Call/Text, Email/Book/Facebook and the steps are in the left column, in that order; no photo there",
          pos["card"]["left"] >= pos["top"]["right"] and abs(pos["card"]["top"] - pos["top"]["top"]) < 90 and left_column(pos) and
          pg.evaluate("!document.querySelector('.contact-photo')"), short)
    ctx.close()

    # ============================================================= 8. keyboard
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    pg.focus("#lf-name"); pg.keyboard.press("Shift+Tab")
    check("keyboard: from the name, Shift+Tab goes back to the choices", pg.evaluate(ACTIVE).startswith("input:topic"), pg.evaluate(ACTIVE))
    order = []
    pg.focus("#lf-name")
    for _ in range(6):
        pg.keyboard.press("Tab"); order.append(pg.evaluate(ACTIVE))
    check("  Tab order: name, phone, the extras, the two text boxes, Send", order == ["lf-phone", "summary", "input:consent_service", "input:consent_marketing", "button", "a"][:0] + ["lf-phone", "summary", "input:consent_service", "input:consent_marketing", "button", "a"] or order[:5] == ["lf-phone", "summary", "input:consent_service", "input:consent_marketing", "button"], order)
    pg.focus("#lf-more summary"); pg.keyboard.press("Enter")
    check("  Enter on the extras opens them, and the next Tab is the email field", pg.evaluate("document.getElementById('lf-more').open") and (pg.keyboard.press("Tab") or True) and pg.evaluate(ACTIVE) == "lf-email")
    pg.focus("input[name=consent_service]"); pg.keyboard.press("Space")
    check("  Space ticks a text box", pg.evaluate("document.querySelector('input[name=consent_service]').checked"))
    pg.keyboard.press("Space")
    check("  ...and unticks it", not pg.evaluate("document.querySelector('input[name=consent_service]').checked"))
    pg.click(".check:nth-child(2) span")
    check("  tapping the words of a text box ticks it (the whole line is the target)", pg.evaluate("document.querySelector('input[name=consent_marketing]').checked"))
    pg.fill("#lf-name", "Kim Park"); pg.click("#lf-phone"); pg.keyboard.type("4235550123", delay=5); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    check("  Enter inside a field sends the form", pg.evaluate(SHOW)["hand"])
    ctx.close()

    # a phone's keyboard has a "next" key that sends Enter: in the boxes that are followed by another box, it moves on instead of sending the form
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    pg.click("#lf-more summary")
    for here, there in (("lf-name", "lf-phone"), ("lf-email", "lf-address"), ("lf-address", "lf-message")):
        pg.focus("#" + here); pg.keyboard.press("Enter"); pg.wait_for_timeout(60)
        st = pg.evaluate(SHOW)
        check(f"keyboard: Enter in {here} moves on to {there} and sends nothing", pg.evaluate(ACTIVE) == there and st["form"] and not st["sum"] and not st["hand"], (pg.evaluate(ACTIVE), st))
    pg.fill("#lf-message", "a"); pg.keyboard.press("Enter")
    check("  Enter in the note adds a line (it is a note, not a button)", pg.input_value("#lf-message") == "a\n" and pg.evaluate(SHOW)["form"], repr(pg.input_value("#lf-message")))
    pg.focus("#lf-phone"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    check("  Enter in the phone box (the last box that has to be filled in) sends the form", pg.evaluate(SHOW)["sum"], pg.evaluate(SHOW))
    ctx.close()

    # Done / Enter in a wrong phone number, Enter on a choice or a text box, and a key held a moment too long
    ALERTS = "document.querySelectorAll('#lf-sum [role=alert]').length"
    ctx, pg, errs = ctx_page(b, 390, 844, True)
    open_form(pg)
    pg.fill("#lf-name", "Kim Park"); pg.focus("#lf-phone"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    check("Enter (the phone keyboard's Done) in an empty phone box: the error box shows with its alert role still on it, so a screen reader announces it, and it has the focus", pg.evaluate(SHOW)["sum"] and pg.evaluate(ALERTS) == 1 and pg.evaluate(ACTIVE) == "lf-sum", (pg.evaluate(SHOW), pg.evaluate(ALERTS), pg.evaluate(ACTIVE)))
    open_form(pg)
    pg.fill("#lf-name", "Kim Park"); pg.click("#lf-phone"); pg.keyboard.type("423", delay=5); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
    check("  and in a phone box that is too short", pg.evaluate(SHOW)["sum"] and pg.evaluate(ALERTS) == 1 and pg.evaluate(ACTIVE) == "lf-sum", (pg.evaluate(SHOW), pg.evaluate(ALERTS), pg.evaluate(ACTIVE)))
    pg.click("#lf-phone"); pg.keyboard.type("4515707", delay=5); pg.wait_for_timeout(100)
    check("  fixing the box still takes its line (and the whole box) away, and the alert role is gone with it", not pg.evaluate(SHOW)["sum"] and pg.evaluate(ALERTS) == 0, (pg.evaluate(SHOW), pg.evaluate(ALERTS)))
    ctx.close()

    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    fill_valid(pg, extras=False)
    pg.focus("input[name=topic][value=sell]"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    st = pg.evaluate(SHOW)
    check("Enter on one of the choices does not send the form (Space ticks it)", st["form"] and not st["hand"] and not st["sum"] and not st["done"], st)
    pg.focus("input[name=consent_service]"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
    st = pg.evaluate(SHOW)
    check("  nor does Enter on a text-message box, which stays as it was (unticked)", st["form"] and not st["hand"] and not st["sum"] and not pg.evaluate("document.querySelector('input[name=consent_service]').checked"), st)
    pg.focus("input[name=consent_service]"); pg.keyboard.press("Space")
    check("  and Space still ticks it", pg.evaluate("document.querySelector('input[name=consent_service]').checked"))
    ctx.close()

    ctx, pg, errs = ctx_page(b, 390, 844, True)
    open_form(pg)
    pg.fill("#lf-name", "Kim Park"); pg.focus("#lf-name")
    pg.keyboard.down("Enter"); pg.keyboard.down("Enter"); pg.keyboard.down("Enter"); pg.keyboard.up("Enter"); pg.wait_for_timeout(200)   # a key held down: the second and third are repeats
    st = pg.evaluate(SHOW)
    check("a held Enter key: the first press moves from the name to the phone box, the repeats send nothing and scold nothing", pg.evaluate(ACTIVE) == "lf-phone" and st["form"] and not st["sum"] and not st["hand"], (pg.evaluate(ACTIVE), st))
    ctx.close()

    # the ring around a box that has the keyboard is easy to see, in every box
    ctx, pg, errs = ctx_page(b)
    open_form(pg)
    pg.click("#lf-more summary")
    for sel in ("#lf-name", "#lf-phone", "#lf-email", "#lf-address", "#lf-message"):
        pg.focus(sel); pg.keyboard.press("Shift"); pg.focus(sel)
        ring = pg.evaluate("sel => { const s = getComputedStyle(document.querySelector(sel)); return [s.outlineStyle, parseFloat(s.outlineWidth), s.outlineColor]; }", sel)
        check(f"keyboard focus is easy to see on {sel} (a solid outline of 3px or more, not removed)", ring[0] != "none" and ring[1] >= 3 and ring[2] not in ("transparent", "rgba(0, 0, 0, 0)"), ring)
    ctx.close()

    # ============================================================= 9. axe, when it is installed
    axe_path = next((q for q in (pathlib.Path("node_modules/axe-core/axe.min.js"), ROOT / "node_modules/axe-core/axe.min.js", ROOT.parent / "node_modules/axe-core/axe.min.js") if q.exists()), None)
    if axe_path is None:
        print("skip  axe: not installed here (npm i axe-core, then run from that folder)")
    else:
        AXE = axe_path.read_text()
        TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]

        def axe_run(pg, label):
            pg.add_script_tag(content=AXE)
            res = pg.evaluate("(tags) => axe.run(document.querySelector('.form-card'), { runOnly: { type: 'tag', values: tags } }).then(r => ({ v: r.violations.map(v => v.id + ': ' + v.nodes.map(n => n.target.join(' ')).join(' ; ')), inc: r.incomplete.map(v => v.id + ': ' + v.nodes.map(n => n.target.join(' ')).join(' ; ')) }))", TAGS)
            check(f"axe, {label}: no violations", res["v"] == [], res["v"])
            if res["inc"]:
                print("      needs a look (axe 'incomplete'):", res["inc"])

        for who, w, mobile in (("computer", 1280, False), ("phone", 390, True)):
            ctx, pg, errs = ctx_page(b, w, 900 if not mobile else 844, mobile)   # reduced motion: nothing is mid-fade while axe measures
            open_form(pg)
            pg.wait_for_timeout(300)
            axe_run(pg, f"{who}, as it opens")
            pg.click("#lf-more summary"); pg.click(".lf-send"); pg.wait_for_timeout(300)
            axe_run(pg, f"{who}, with errors and the extras open")
            fill_valid(pg, extras=False); pg.click(".lf-send"); pg.wait_for_timeout(300)
            axe_run(pg, f"{who}, the ready-made message")
            pg.evaluate("document.getElementById('lf-hand').hidden = true; document.getElementById('lf-done').hidden = false"); pg.wait_for_timeout(300)
            axe_run(pg, f"{who}, the thank-you")
            ctx.close()
    b.close()

print("\nFAILS", len(fails))
if fails:
    print("\n".join("  - " + f for f in fails))
sys.exit(1 if fails else 0)

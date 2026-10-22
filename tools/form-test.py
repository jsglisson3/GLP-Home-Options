#!/usr/bin/env python3
"""Does the contact form always show up, or fall back to a call/text card? (js/site.js "Contact form", the .ghl rules in css/site.css.)

Run:   python3 tools/form-test.py        It must print  FAILS 0.   (add --long for one more case that takes a minute: a form that comes up after 65 s)
The real form is a third-party frame (links.voiseai.com) that this machine cannot reach, so the test stands in for it: it serves a
pretend form page and a pretend embed script on that address (browser-level, nothing leaves the machine) and plays the situations a
visitor can meet:
  happy path ......... embed script and form both fine: the box shows the form, no blank box, no leftover placeholder
  lazy bug ........... the Checkpoint 34 bug: a frame marked loading="lazy" that the embed script parks off-screen never loads.
                       The page must never carry a lazy frame, and the frame must be added when the box is near
  embed script blocked  (an ad blocker, a company network): the form still shows
  embed script never shows the frame: the page shows it itself after 6 s
  form never loads ... (blocked, offline, dead): after 12 s the box becomes the call/text card with working links;
                       "Try the form again" builds a fresh frame and, when the form is back, shows it
  form comes up late . the call/text card is up (12 s), then the form says hello at 14 s: the card gives way to the form
                       (with the embed script working, and with it parking the frame for good)
  no JavaScript ...... the call/text card shows, without the retry button
It also checks the page at phone and desktop sizes: the box never overflows the screen sideways, and the card's buttons fit; and with bigger
text (the page's text size at 125 to 200%, and letters-only enlargement the way a phone's text size does it) the waiting outline and the call/text
card stay inside their box and inside the screen (the state is forced, so the check does not wait 12 s).
"""
import functools, http.server, pathlib, re, socketserver, sys, threading
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FORM_ID = "c36UOOc2pkosxfvRfjZJ"
HOST = "https://links.voiseai.com"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k):
        pass


srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()
fails = []


def check(name, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + name + (("  " + str(detail)) if detail != "" else ""))
    if not ok:
        fails.append(name)


# ---- the pretend form page: it says hello to the page, and answers the embed script's hello with its height (as the real one does)
CHILD = """<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;font:16px serif}.f{height:864px;background:#fff}</style></head>
<body><div class="f"><label>First Name</label> <input></div><script>
window.addEventListener('message', function (e) {
  if (typeof e.data === 'string' && e.data.indexOf('[iFrameSizer]') === 0) {
    var id = e.data.slice(13).split(':')[0];
    parent.postMessage('[iFrameSizer]' + id + ':864:483:init', '*');
  }
});
parent.postMessage('[iFrameResizerChild]Ready', '*');
parent.postMessage('["iframeLoaded"]', '*');
</script></body></html>"""
DEAD_CHILD = "<!doctype html><html><head><meta charset='utf-8'></head><body></body></html>"   # loads, but never says a word (its scripts are blocked)
# loads at once but says hello only after __MS__ ms (a slow connection, a busy server): the page has already given up by then
LATE_CHILD = (CHILD.replace("window.addEventListener('message', function (e) {\n  if (typeof", "var up = false;\nwindow.addEventListener('message', function (e) {\n  if (!up) return;\n  if (typeof")
              .replace("parent.postMessage('[iFrameResizerChild]Ready', '*');\nparent.postMessage('[\"iframeLoaded\"]', '*');",
                       "setTimeout(function () { up = true; parent.postMessage('[iFrameResizerChild]Ready', '*'); parent.postMessage('[\"iframeLoaded\"]', '*'); }, __MS__);"))
assert "__MS__" in LATE_CHILD and "if (!up) return;" in LATE_CHILD

# ---- the pretend embed script: parks every form frame off-screen and invisible, and shows it (after an animation frame, as the
# real one does) when the form has reported its height. REVEAL=false makes one that parks and never shows.
def vendor(reveal=True):
    return """(function () {
  function park(f) { f.setAttribute('data-parked', '1'); var s = f.style; s.opacity = '0'; s.visibility = 'hidden'; s.pointerEvents = 'none'; s.left = '-9999px'; s.position = 'absolute'; }
  function show(f) { var s = f.style; s.opacity = '1'; s.pointerEvents = 'auto'; s.visibility = 'visible'; s.display = 'block'; s.left = ''; s.position = 'relative'; }
  function frames() { return [].slice.call(document.querySelectorAll('iframe')).filter(function (f) { return (f.src || '').indexOf('/widget/form/') > -1; }); }
  function scan() { frames().forEach(function (f) { if (!f.getAttribute('data-parked')) park(f); try { f.contentWindow.postMessage('[iFrameSizer]' + f.id + ':8:false:true:32:true:true:::auto:true', '*'); } catch (e) {} }); }
  window.addEventListener('message', function (e) {
    var d = e.data; if (typeof d !== 'string') return;
    if (d.indexOf('["iframeLoaded"]') === 0 || d.indexOf('[iFrameResizerChild]Ready') === 0) scan();
    var m = /^\\[iFrameSizer\\]([^:]+):(\\d+):(\\d+):(\\w+)/.exec(d);
    if (m && %s) { var f = document.getElementById(m[1]); if (f) requestAnimationFrame(function () { f.style.height = (+m[2] + 5) + 'px'; show(f); }); }
  });
  scan();
})();""" % ("true" if reveal else "false")


def install(ctx, mode):
    """mode = {"child": ok|dead|down|late, "vendor": ok|parks|blocked}; change it while a page is open to change what the next request meets."""
    def handler(route):
        url = route.request.url
        if url.startswith(BASE):
            return route.continue_()
        if url.startswith(HOST + "/widget/form/"):
            if mode["child"] == "ok":
                return route.fulfill(status=200, content_type="text/html", body=CHILD)
            if mode["child"] == "dead":
                return route.fulfill(status=200, content_type="text/html", body=DEAD_CHILD)
            if mode["child"] == "late":
                return route.fulfill(status=200, content_type="text/html", body=LATE_CHILD.replace("__MS__", str(mode.get("ms", 14000))))
            return route.abort()
        if url == HOST + "/js/form_embed.js":
            if mode["vendor"] == "ok":
                return route.fulfill(status=200, content_type="application/javascript", body=vendor(True))
            if mode["vendor"] == "parks":
                return route.fulfill(status=200, content_type="application/javascript", body=vendor(False))
            return route.abort()
        return route.abort()
    ctx.route("**/*", handler)


STATE = "document.querySelector('.ghl').getAttribute('data-state')"
FRAME = """(() => { const f = document.querySelector('.ghl iframe'); if (!f) return null; const s = getComputedStyle(f), r = f.getBoundingClientRect();
  return { id: f.id, lazy: f.getAttribute('loading'), vis: s.visibility, op: s.opacity, pos: s.position, h: Math.round(r.height), w: Math.round(r.width), x: Math.round(r.left) }; })()"""
SHOWN = lambda fr: bool(fr) and fr["vis"] == "visible" and fr["op"] == "1" and fr["pos"] != "absolute" and fr["x"] > -100
BOXES = """(() => { const b = document.querySelector('.ghl'); const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return s.display !== 'none' && r.width > 0 && r.height > 0; };
  return { wait: vis(b.querySelector('.ghl-wait')), slow: vis(b.querySelector('.ghl-slow')), h: Math.round(b.getBoundingClientRect().height) }; })()"""


def wait_state(pg, want, ms):
    try:
        pg.wait_for_function(f"{STATE} === {want!r}", timeout=ms)
        return True
    except Exception:
        return False


# ---- 0. the page itself: no lazy frame in any built page, and no embed script on the page (site.js adds it with the frame)
for f in sorted(ROOT.glob("*.html")):
    t = f.read_text(encoding="utf-8")
    check(f"{f.name}: no <iframe loading=lazy> (the embed script parks frames off-screen, so a lazy one never loads)", not re.search(r"<iframe[^>]*loading=", t))
    check(f"{f.name}: the embed script is not on the page (site.js adds it with the frame)", "form_embed.js" not in t)

with sync_playwright() as p:
    b = p.chromium.launch()

    def page(mode, w=1280, h=900, mobile=False, js=True):
        ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, java_script_enabled=js)
        install(ctx, mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        return ctx, pg, errs

    # 1. happy path, Contact page, desktop
    mode = {"child": "ok", "vendor": "ok"}
    ctx, pg, errs = page(mode)
    pg.goto(BASE + "contact.html")
    check("happy path (desktop, Contact): the form shows", wait_state(pg, "ready", 6000), pg.evaluate(STATE))
    fr, bx = pg.evaluate(FRAME), pg.evaluate(BOXES)
    check("  the frame is on screen, not parked", SHOWN(fr), fr)
    check("  the frame took the height the form reported (864 + 5)", fr and fr["h"] == 869, fr and fr["h"])
    check("  no placeholder and no call card left showing", not bx["wait"] and not bx["slow"], bx)
    check("  the frame has no lazy attribute and the right title", fr and fr["lazy"] is None and pg.evaluate("document.querySelector('.ghl iframe').title").startswith("Contact form"))
    check("  one frame only", pg.evaluate("document.querySelectorAll('.ghl iframe').length") == 1)
    check("  the page has no script errors", not errs, errs)
    ctx.close()

    # 2. happy path, Home page: far down, so nothing is added until the visitor is near; then it loads
    ctx, pg, errs = page(mode, 390, 844, mobile=True)
    pg.goto(BASE + "index.html"); pg.wait_for_timeout(1500)
    check("Home: the form is not fetched while the visitor is far from it", pg.evaluate("document.querySelectorAll('.ghl iframe').length") == 0 and pg.evaluate(STATE) == "idle", pg.evaluate(STATE))
    pg.evaluate("window.dispatchEvent(new Event('touchmove'))")   # a real visitor drags first; until then the start-at-top guard undoes any jump
    pg.evaluate("document.querySelector('.ghl').scrollIntoView({block: 'center', behavior: 'instant'})")
    check("Home (phone): near the box, the form loads and shows", wait_state(pg, "ready", 6000), pg.evaluate(STATE))
    fr = pg.evaluate(FRAME)
    check("  the frame is on screen and not wider than the box", SHOWN(fr) and fr["w"] <= 390, fr)
    check("  the page does not scroll sideways", pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), pg.evaluate("document.documentElement.scrollWidth"))
    check("  the page has no script errors", not errs, errs)
    ctx.close()

    # 3. the embed script is blocked
    ctx, pg, errs = page({"child": "ok", "vendor": "blocked"})
    pg.goto(BASE + "contact.html")
    check("embed script blocked: the form still shows (about a second after the form speaks)", wait_state(pg, "ready", 6000), pg.evaluate(STATE))
    fr = pg.evaluate(FRAME)
    check("  the frame is on screen with a sensible height (it cannot be measured, so the measured one is used)", SHOWN(fr) and 800 <= fr["h"] <= 1000, fr)
    ctx.close()

    # 4. the embed script parks the frame and never shows it
    ctx, pg, errs = page({"child": "ok", "vendor": "parks"})
    pg.goto(BASE + "contact.html")
    pg.wait_for_timeout(3000)
    check("embed script never shows the frame: still waiting at 3 s (not shown too early)", pg.evaluate(STATE) == "loading", pg.evaluate(STATE))
    check("  after 6 s the page shows the frame itself", wait_state(pg, "ready", 6500), pg.evaluate(STATE))
    fr = pg.evaluate(FRAME)
    check("  the frame is on screen at the height the form reported", SHOWN(fr) and fr["h"] == 869, fr)
    ctx.close()

    # 5. the form never loads (host unreachable): call card after 12 s, then retry when the host is back
    mode = {"child": "down", "vendor": "ok"}
    ctx, pg, errs = page(mode)
    pg.goto(BASE + "contact.html")
    pg.wait_for_timeout(9000)
    check("form unreachable: placeholder still showing at 9 s", pg.evaluate(STATE) == "loading", pg.evaluate(STATE))
    check("  after 12 s the box turns into the call/text card", wait_state(pg, "slow", 6000), pg.evaluate(STATE))
    bx = pg.evaluate(BOXES)
    check("  the call card shows and the placeholder is gone", bx["slow"] and not bx["wait"], bx)
    links = pg.evaluate("[...document.querySelectorAll('.ghl-slow a')].map(a => [a.getAttribute('href'), a.textContent.trim()])")
    check("  Call and Text point at the real number, Email at the real address",
          links[0][0] == "tel:+14234515707" and links[1][0] == "sms:+14234515707" and links[2][0] == "mailto:info@glphomeoptions.com", links)
    check("  the card has no blank frame above it", not SHOWN(pg.evaluate(FRAME)))
    mode["child"] = "ok"                      # the network comes back
    pg.click("[data-ghl-retry]")
    check("  'Try the form again' builds a fresh frame and the form shows", wait_state(pg, "ready", 6000), pg.evaluate(STATE))
    fr = pg.evaluate(FRAME)
    check("  exactly one frame is left, and it is the new one", pg.evaluate("document.querySelectorAll('.ghl iframe').length") == 1 and fr["id"].endswith("-1"), fr)
    check("  the form shows at its height", SHOWN(fr) and fr["h"] == 869, fr)
    ctx.close()

    # 5b. the form comes up late (after the call card is already showing): the card gives way to the form by itself
    late = []
    for vend in ("ok", "parks"):
        c, g, e = page({"child": "late", "vendor": vend, "ms": 14000})
        g.goto(BASE + "contact.html")
        late.append((vend, c, g, e))
    seen = [False] * len(late)
    for _ in range(70):                       # up to 14 s, watching both pages (the card is up for only about two seconds on each)
        for i, (vend, c, g, e) in enumerate(late):
            if not seen[i] and g.evaluate(STATE) == "slow":
                seen[i] = True
        if all(seen):
            break
        late[0][2].wait_for_timeout(200)
    for i, (vend, c, g, e) in enumerate(late):
        check(f"late form (embed script {'works' if vend == 'ok' else 'parks and never shows it'}): the call card is up before the form speaks", seen[i], g.evaluate(STATE))
    for vend, c, g, e in late:
        check(f"  then the form says hello (14 s): the card gives way and the form shows (embed script {vend})", wait_state(g, "ready", 12000), g.evaluate(STATE))
        fr, bx = g.evaluate(FRAME), g.evaluate(BOXES)
        check("  the frame is on screen at the height the form reported, no card or placeholder left", SHOWN(fr) and fr["h"] == 869 and not bx["wait"] and not bx["slow"], [fr, bx])
        check("  no script errors", not e, e)
        c.close()

    if "--long" in sys.argv:   # the page stops watching after a minute of nothing; a form that comes up after that must still be shown
        c, g, e = page({"child": "late", "vendor": "parks", "ms": 65000})
        g.goto(BASE + "contact.html")
        check("very late form (65 s, embed script parks it): the call card is up", wait_state(g, "slow", 14000), g.evaluate(STATE))
        check("  at 65 s the form says hello and, 6 s later at the latest, shows", wait_state(g, "ready", 60000), g.evaluate(STATE))
        fr = g.evaluate(FRAME)
        check("  the frame is on screen at the height the form reported", SHOWN(fr) and fr["h"] == 869, fr)
        c.close()

    # 6. the form loads but its scripts are blocked (it never speaks): call card, not a blank box
    ctx, pg, errs = page({"child": "dead", "vendor": "ok"})
    pg.goto(BASE + "contact.html")
    check("blank form (loads, never speaks): the call card shows after 12 s", wait_state(pg, "slow", 14000), pg.evaluate(STATE))
    ctx.close()

    # 7. phone, the call card: buttons fit and the page does not scroll sideways
    ctx, pg, errs = page({"child": "down", "vendor": "ok"}, 320, 700, mobile=True)
    pg.goto(BASE + "contact.html")
    check("320 px: the call card shows", wait_state(pg, "slow", 15000), pg.evaluate(STATE))
    pg.evaluate("document.querySelector('.ghl-slow').scrollIntoView({block: 'center', behavior: 'instant'})")
    fit = pg.evaluate("""(() => { const card = document.querySelector('.ghl-slow').getBoundingClientRect();
      return { sideways: document.documentElement.scrollWidth > window.innerWidth, btns: [...document.querySelectorAll('.ghl-slow-btns .btn')].map(b => { const r = b.getBoundingClientRect(); return [Math.round(r.left - card.left), Math.round(card.right - r.right), Math.round(r.height), b.scrollWidth <= b.clientWidth + 1]; }) }; })()""")
    check("  no sideways scroll; both buttons inside the card, 44 px or taller, text not cut", not fit["sideways"] and all(b[0] >= 0 and b[1] >= 0 and b[2] >= 44 and b[3] for b in fit["btns"]), fit)
    ctx.close()

    # 8. no JavaScript: the call card shows, the retry button does not
    ctx, pg, errs = page({"child": "ok", "vendor": "ok"}, js=False)
    pg.goto(BASE + "contact.html")
    bx = pg.evaluate("""(() => { const b = document.querySelector('.ghl'); const vis = e => e && getComputedStyle(e).display !== 'none';
      return { wait: vis(b.querySelector('.ghl-wait')), slow: vis(b.querySelector('.ghl-slow')), retry: vis(b.querySelector('[data-ghl-retry]')) }; })()""")
    check("no JavaScript: the call card shows, no placeholder, no retry button", bx["slow"] and not bx["wait"] and not bx["retry"], bx)
    ctx.close()

    # 9. bigger text: the waiting outline and the call/text card stay inside their box and the screen
    LETTERS = """(n) => { const els = [...document.querySelectorAll('body *')]; const sizes = els.map(e => parseFloat(getComputedStyle(e).fontSize));
      els.forEach((e, i) => e.style.setProperty('font-size', (sizes[i] * n) + 'px', 'important')); }"""
    FITS = """(which) => { const box = document.querySelector('.ghl'), part = box.querySelector(which), card = part.getBoundingClientRect(), out = { sideways: document.documentElement.scrollWidth > window.innerWidth, over: [], cut: [] };
      part.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && (r.left < card.left - 1 || r.right > card.right + 1)) out.over.push(e.tagName + '.' + e.className);
        if (e.matches('a.btn, button') && e.scrollWidth > e.clientWidth + 1) out.cut.push(e.textContent.trim()); });
      const bx = box.getBoundingClientRect(); if (card.left < bx.left - 1 || card.right > bx.right + 1 || bx.right > window.innerWidth + 1) out.over.push('card or box past the edge');
      return out; }"""
    for kind, n, w in [("text size", 1.25, 390), ("text size", 1.5, 360), ("text size", 2.0, 390), ("text size", 1.5, 320), ("letters", 1.5, 390), ("letters", 2.0, 360), ("letters", 1.5, 320)]:
        ctx, pg, errs = page({"child": "down", "vendor": "ok"}, w, 800, mobile=True)
        pg.goto(BASE + "contact.html"); pg.wait_for_timeout(600)
        if kind == "text size":
            pg.evaluate(f"document.documentElement.style.fontSize = '{int(n * 100)}%'")
        else:
            pg.evaluate(LETTERS, n)
        pg.wait_for_timeout(200)
        for state, part in (("loading", ".ghl-wait"), ("slow", ".ghl-slow")):
            pg.evaluate(f"document.querySelector('.ghl').setAttribute('data-state', '{state}')")   # forced: the real states are tested above
            pg.evaluate(f"document.querySelector('{part}').scrollIntoView({{block: 'center', behavior: 'instant'}})")
            fit = pg.evaluate(FITS, part)
            check(f"{w} px, {kind} {int(n * 100)}%, {state}: inside the box and the screen, no button text cut", not fit["sideways"] and not fit["over"] and not fit["cut"], fit)
        ctx.close()

    b.close()

print("\nFAILS", len(fails))
sys.exit(1 if fails else 0)

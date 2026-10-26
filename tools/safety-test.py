#!/usr/bin/env python3
"""If the page's script fails, does the page still show everything?  (js/site.js hides sections until they scroll into view.)

Run:   python3 tools/safety-test.py        It must print  FAILS 0.
It serves this folder on a throwaway port and opens every page in a phone-sized Chromium (touch on, outside requests blocked):
  1. normal:            the script runs, the page keeps its "js" class, window.__glpReady is true, sections below the screen start hidden;
  2. script missing:    js/site.js fails to load  -> the "js" class is dropped at once and every section is visible;
  3. script crashes:    js/site.js throws on its first line -> after the 6 s safety timer in the head every section is visible;
  4. guard crashes:     history.scrollRestoration throws (the start-at-top guard fails) -> the rest of the script still runs
                        (menu button works, __glpReady is true);
  5. Contact page:      its heading block is plain; the Call and Text tiles and the form card fade in from the stylesheet alone.
"""
import functools, http.server, pathlib, socketserver, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()
PAGES = _site.page_files()   # every page in the folder, found by tools/_site.py
fails = []
def check(name, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + name + (("  " + str(detail)) if detail != "" else ""))
    if not ok: fails.append(name)

# how many "rv" sections are still invisible (opacity 0) right now
HIDDEN = "[...document.querySelectorAll('.rv')].filter(e => parseFloat(getComputedStyle(e).opacity) < 0.05).length"
JS_CLASS = "document.documentElement.classList.contains('js')"

with sync_playwright() as p:
    b = p.chromium.launch()
    def fresh(block_script=False, crash_script=False, init=None):
        ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        def handler(r):
            u = r.request.url
            if not u.startswith(BASE): return r.abort()
            if "js/site.js" in u and block_script: return r.abort()
            if "js/site.js" in u and crash_script: return r.fulfill(status=200, content_type="application/javascript", body="throw new Error('test: script crashed');")
            return r.continue_()
        ctx.route("**/*", handler)
        if init: ctx.add_init_script(init)
        return ctx, ctx.new_page()

    for page in PAGES:
        # 1. normal
        ctx, pg = fresh(); pg.goto(BASE + page); pg.wait_for_timeout(900)
        ready = pg.evaluate("window.__glpReady === true")
        hidden = pg.evaluate(HIDDEN)
        check(f"{page}: normal load keeps the script's features (ready flag set, js class kept)", ready and pg.evaluate(JS_CLASS), (ready, pg.evaluate(JS_CLASS)))
        if page not in ("privacy-policy.html", "terms-of-service.html", "404.html"):
            check(f"{page}: sections below the screen still wait to scroll into view", hidden > 0, hidden)
        ctx.close()

        # 2. script missing: the js class goes at once, everything shows
        ctx, pg = fresh(block_script=True); pg.goto(BASE + page); pg.wait_for_timeout(500)
        check(f"{page}: script missing -> everything visible at once", (not pg.evaluate(JS_CLASS)) and pg.evaluate(HIDDEN) == 0, (pg.evaluate(JS_CLASS), pg.evaluate(HIDDEN)))
        ctx.close()

    # 3. script crashes (two pages are enough; the timer is the same on all of them): visible after the 6 s timer
    for page in ("index.html", "contact.html"):
        ctx, pg = fresh(crash_script=True); pg.goto(BASE + page); pg.wait_for_timeout(1500)
        early = pg.evaluate(JS_CLASS)
        pg.wait_for_timeout(5500)
        check(f"{page}: script crashes -> everything visible after the 6 s timer", (not pg.evaluate(JS_CLASS)) and pg.evaluate(HIDDEN) == 0 and early, (early, pg.evaluate(JS_CLASS), pg.evaluate(HIDDEN)))
        ctx.close()

    # 4. the start-at-top guard crashes: the rest of the script must still run
    boom = "try { Object.defineProperty(history, 'scrollRestoration', { get() { return 'auto'; }, set(v) { throw new Error('test: guard crashed'); } }); } catch (e) {}"
    for page in ("index.html", "contact.html"):
        ctx, pg = fresh(init=boom); pg.goto(BASE + page); pg.wait_for_timeout(900)
        ready = pg.evaluate("window.__glpReady === true")
        pg.click(".menu-btn"); pg.wait_for_timeout(500)
        opened = pg.evaluate("document.querySelector('.menu-btn').getAttribute('aria-expanded') === 'true' && !document.querySelector('#mnav').hidden")
        check(f"{page}: if the start-at-top guard crashes, the rest of the script still runs (ready flag, menu opens)", ready and opened, (ready, opened))
        ctx.close()

    # 5. Contact page: nothing on the first screen waits for the script
    ctx, pg = fresh(block_script=True); pg.goto(BASE + "contact.html"); pg.wait_for_timeout(300)
    pg.evaluate("document.documentElement.classList.add('js')")   # pretend the script were still loading
    top = pg.evaluate("(() => { const e = document.querySelector('.contact-copy > div'); return [e.className, getComputedStyle(e).opacity]; })()")
    check("Contact: the heading block is plain (no fade), so it paints with the page", top[0] == "" and top[1] == "1", top)
    vis = pg.evaluate("""() => ['.reach-item.rv:nth-child(1)', '.reach-item.rv:nth-child(2)', '.form-card'].map(s => {
        const e = document.querySelector(s); return [s, e.classList.contains('in'), getComputedStyle(e).animationName]; })""")
    check("Contact: Call tile, Text tile and form card fade in from the stylesheet alone", all(v[1] and v[2] == "reveal" for v in vis), vis)
    ctx.close()
    b.close()

print("\nFAILS", len(fails))
raise SystemExit(1 if fails else 0)

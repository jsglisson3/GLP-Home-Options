#!/usr/bin/env python3
"""Does every page open at the top? (The start-at-top rules in js/site.js, "Open at the very top".)

Run:   python3 tools/scrolltop-test.py        It must print  FAILS 0.
It serves this folder on a throwaway port, opens the Home page in a phone-sized Chromium (touch on, outside requests blocked),
and checks: a plain open; an open with #numbers from a text (no referrer); the same link from another page of the site
(that one should jump); a reload after scrolling; Back (the browser's own memory is kept); that a late jump while loading is
undone; that a drag or a tap on a link ends the guard but a tap on bare page does not.
"""
import functools, http.server, pathlib, socketserver, sys, threading, time
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()
fails = []
def check(name, ok, detail=""):
    print(("ok    " if ok else "FAIL  ") + name + (("  " + str(detail)) if detail != "" else ""))
    if not ok: fails.append(name)
Y = "Math.round(window.pageYOffset)"

with sync_playwright() as p:
    b = p.chromium.launch()
    def fresh():
        ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        return ctx, ctx.new_page()

    # 1. a plain open, then a jump while the page is still loading
    ctx, pg = fresh(); pg.goto(BASE + "index.html"); pg.wait_for_timeout(600)
    check("plain open is at the top", pg.evaluate(Y) == 0, pg.evaluate(Y))
    pg.evaluate("window.scrollTo({top: 5000, behavior: 'instant'})"); pg.wait_for_timeout(500)
    check("a late jump (a form loading) is undone", pg.evaluate(Y) == 0, pg.evaluate(Y))
    # a tap on bare page does not end the guard
    pg.evaluate("document.querySelector('main').dispatchEvent(new Event('touchstart', {bubbles:true}))")
    pg.evaluate("window.scrollTo({top: 4000, behavior: 'instant'})"); pg.wait_for_timeout(400)
    check("a tap on bare page keeps the guard", pg.evaluate(Y) == 0, pg.evaluate(Y))
    # a drag ends it
    pg.evaluate("window.dispatchEvent(new Event('touchmove'))")
    pg.evaluate("window.scrollTo({top: 3000, behavior: 'instant'})"); pg.wait_for_timeout(400)
    check("a drag ends the guard (the visitor can scroll)", pg.evaluate(Y) == 3000, pg.evaluate(Y))
    ctx.close()

    # 1a. the guard gives up after four corrections (someone is scrolling by a way we do not see, e.g. a screen reader)
    ctx, pg = fresh(); pg.goto(BASE + "index.html"); pg.wait_for_timeout(500)
    for i in range(4):
        pg.evaluate("window.scrollTo({top: 2000, behavior: 'instant'})"); pg.wait_for_timeout(250)
    pg.evaluate("window.scrollTo({top: 2000, behavior: 'instant'})"); pg.wait_for_timeout(300)
    check("after four corrections the guard lets go", pg.evaluate(Y) == 2000, pg.evaluate(Y))
    ctx.close()

    # 1b. a tap on a link ends it
    ctx, pg = fresh(); pg.goto(BASE + "index.html"); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('a[href=\"#contact\"]').dispatchEvent(new Event('touchstart', {bubbles:true}))")
    pg.evaluate("window.scrollTo({top: 2500, behavior: 'instant'})"); pg.wait_for_timeout(400)
    check("a tap on a link ends the guard", pg.evaluate(Y) == 2500, pg.evaluate(Y))
    ctx.close()

    # 2. a link from a text: #numbers, no referrer
    ctx, pg = fresh(); pg.goto(BASE + "index.html#numbers"); pg.wait_for_timeout(800)
    check("a texted link with #numbers opens at the top", pg.evaluate(Y) == 0, pg.evaluate(Y))
    check("... and the #numbers is dropped from the address", pg.evaluate("location.hash") == "", pg.evaluate("location.hash"))
    ctx.close()

    # 3. the same link from another page of this site (should jump)
    ctx, pg = fresh(); pg.goto(BASE + "index.html#numbers", referer=BASE + "options.html"); pg.wait_for_timeout(800)
    ref = pg.evaluate("document.referrer")
    check("a link from another page of the site still jumps to its section", pg.evaluate(Y) > 500, (pg.evaluate(Y), ref))
    ctx.close()

    # 3b. a real click from another page
    ctx, pg = fresh(); pg.goto(BASE + "options.html"); pg.wait_for_timeout(400)
    pg.evaluate("document.querySelector('a[href=\"index.html#numbers\"]').click()"); pg.wait_for_timeout(1200)
    check("clicking index.html#numbers on Options lands on the numbers", pg.evaluate(Y) > 500 and "index.html" in pg.url, (pg.evaluate(Y), pg.url))
    ctx.close()

    # 4. a reload after the visitor scrolled
    ctx, pg = fresh(); pg.goto(BASE + "index.html"); pg.wait_for_timeout(500)
    pg.mouse.move(100, 300); pg.mouse.wheel(0, 3000); pg.wait_for_timeout(500)
    scrolled = pg.evaluate(Y)
    pg.reload(); pg.wait_for_timeout(900)
    check("a reload opens at the top", scrolled > 1000 and pg.evaluate(Y) == 0, (scrolled, pg.evaluate(Y)))
    ctx.close()

    # 5. Back keeps the browser's own memory
    ctx, pg = fresh(); pg.goto(BASE + "index.html"); pg.wait_for_timeout(500)
    pg.mouse.move(100, 300); pg.mouse.wheel(0, 3000); pg.wait_for_timeout(500)
    before = pg.evaluate(Y)
    pg.goto(BASE + "options.html"); pg.wait_for_timeout(500)
    pg.go_back(); pg.wait_for_timeout(1200)
    check("Back returns to where the visitor was", before > 1000 and abs(pg.evaluate(Y) - before) < 80, (before, pg.evaluate(Y)))
    ctx.close()

    # 6. every page opens at the top with a stray #section from a text
    for page, h in [("options.html", "#direct"), ("about.html", "#story"), ("contact.html", "#contact"), ("work.html", "#closed"), ("new-homes.html", "#faq")]:
        ctx, pg = fresh(); pg.goto(BASE + page + h); pg.wait_for_timeout(700)
        check(f"{page}{h} from a text opens at the top", pg.evaluate(Y) == 0, pg.evaluate(Y))
        ctx.close()
    b.close()
print("FAILS", len(fails))
sys.exit(1 if fails else 0)

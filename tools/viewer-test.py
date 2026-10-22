#!/usr/bin/env python3
"""Does the Our work photo viewer work on a phone?  (js/gallery.js)

Run:   python3 tools/viewer-test.py        It must print  FAILS 0.
It serves this folder on a throwaway port and opens the Our work page in a phone-sized Chromium (touch on, outside requests blocked):
a tap on a photo opens the viewer at "1 of N"; a swipe left shows 2, a swipe right shows 1 again; a mostly-vertical drag and a
short drag change nothing; the arrow keys and the Next/Previous buttons still work; the Close button and Esc close it and give
focus back to the photo; the buttons are 44 px or larger.
Then, on phones held sideways (five landscape sizes), every photo with its caption, counter and buttons stays on the screen, with no
overlaps, and the photo is at least 190 px tall (Checkpoint 26).
"""
import functools, http.server, pathlib, socketserver, threading
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

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)
    ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(BASE + "work.html"); pg.wait_for_timeout(800)
    COUNT = "document.querySelector('.lb-count') && document.querySelector('.lb-count').textContent"

    def swipe(x0, y0, x1, y1, steps=6):
        cdp.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": x0, "y": y0}]})
        for i in range(1, steps + 1):
            cdp.send("Input.dispatchTouchEvent", {"type": "touchMove", "touchPoints": [{"x": x0 + (x1 - x0) * i / steps, "y": y0 + (y1 - y0) * i / steps}]})
        cdp.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
        pg.wait_for_timeout(250)

    # open the first photo with a tap
    first = pg.query_selector(".work-grid a")
    first.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
    first.tap(); pg.wait_for_timeout(500)
    opened = pg.evaluate("!!document.querySelector('dialog.lb[open]')")
    check("a tap on a photo opens the viewer", opened)
    c0 = pg.evaluate(COUNT); check("it opens at photo 1", (c0 or "").startswith("1 of "), c0)
    total = int((c0 or "1 of 0").split(" of ")[1])

    swipe(300, 400, 80, 410); c1 = pg.evaluate(COUNT)
    check("a swipe left shows photo 2", (c1 or "").startswith("2 of "), c1)
    swipe(80, 400, 300, 395); c2 = pg.evaluate(COUNT)
    check("a swipe right goes back to photo 1", (c2 or "").startswith("1 of "), c2)
    swipe(200, 300, 205, 600); c3 = pg.evaluate(COUNT)
    check("a mostly vertical drag changes nothing", c3 == c2, c3)
    swipe(200, 400, 170, 402); c4 = pg.evaluate(COUNT)
    check("a short drag changes nothing", c4 == c2, c4)
    swipe(80, 400, 300, 395); c5 = pg.evaluate(COUNT)
    check(f"a swipe right on photo 1 wraps to the last photo ({total} of {total})", (c5 or "").startswith(f"{total} of "), c5)
    swipe(300, 400, 80, 410); c6 = pg.evaluate(COUNT)
    check("and a swipe left wraps back to photo 1", (c6 or "").startswith("1 of "), c6)

    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(150)
    check("the arrow key still moves to photo 2", (pg.evaluate(COUNT) or "").startswith("2 of "), pg.evaluate(COUNT))
    pg.tap(".lb-next"); pg.wait_for_timeout(150)
    check("the Next button still works", (pg.evaluate(COUNT) or "").startswith("3 of "), pg.evaluate(COUNT))
    pg.tap(".lb-prev"); pg.wait_for_timeout(150)
    check("the Previous button still works", (pg.evaluate(COUNT) or "").startswith("2 of "), pg.evaluate(COUNT))
    sizes = pg.evaluate("[...document.querySelectorAll('.lb-close,.lb-prev,.lb-next')].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; })")
    check("Close, Previous and Next are 44 px or larger", all(w >= 44 and h >= 44 for w, h in sizes), sizes)
    inside = pg.evaluate("(() => { const i = document.querySelector('.lb-img').getBoundingClientRect(); return i.left >= 0 && i.right <= innerWidth && i.top >= 0 && i.bottom <= innerHeight; })()")
    check("the photo fits on the screen", inside)

    pg.tap(".lb-close"); pg.wait_for_timeout(300)
    check("the Close button closes the viewer", not pg.evaluate("!!document.querySelector('dialog.lb[open]')"))
    check("focus goes back to the photo that was opened", pg.evaluate("document.activeElement && document.activeElement.matches('.work-grid a')"))
    first.tap(); pg.wait_for_timeout(400); pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    check("Esc closes it too", not pg.evaluate("!!document.querySelector('dialog.lb[open]')"))
    ctx.close()

    # phones held sideways: every photo, its caption and the buttons stay on the screen (Checkpoint 26)
    RECTS = """() => { const R = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return {t: r.top, b: r.bottom, l: r.left, r: r.right}; };
      return {vw: innerWidth, vh: innerHeight, img: R('.lb-img'), cap: R('.lb-cap'), close: R('.lb-close'), prev: R('.lb-prev'), next: R('.lb-next'), count: R('.lb-count')}; }"""
    for (w, h) in ((844, 390), (667, 375), (932, 430), (568, 320), (640, 360)):
        lc = b.new_context(viewport={"width": w, "height": h}, is_mobile=True, has_touch=True, device_scale_factor=1, reduced_motion="reduce")
        lc.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        lp = lc.new_page(); lp.goto(BASE + "work.html"); lp.wait_for_timeout(700)
        f = lp.query_selector(".work-grid a"); f.scroll_into_view_if_needed(); lp.wait_for_timeout(300); f.tap(); lp.wait_for_timeout(600)
        n = int((lp.evaluate(COUNT) or "1 of 0").split(" of ")[1]); bad = []; smallest = 9999
        for i in range(n):
            lp.wait_for_timeout(200)
            m = lp.evaluate(RECTS); img = m["img"]; smallest = min(smallest, img["b"] - img["t"])
            if img["t"] < 0 or img["b"] > m["vh"] or img["l"] < 0 or img["r"] > m["vw"]: bad.append(f"photo {i+1} is off the screen")
            if m["cap"] and (m["cap"]["b"] > m["vh"] or m["cap"]["t"] < img["b"] - 1): bad.append(f"photo {i+1}: caption off the screen or on the photo")
            for k in ("close", "prev", "next", "count"):
                e = m[k]
                if e and (e["t"] < 0 or e["b"] > m["vh"] or e["l"] < 0 or e["r"] > m["vw"]): bad.append(f"photo {i+1}: {k} is off the screen")
            if m["prev"] and img["l"] < m["prev"]["r"] - 1: bad.append(f"photo {i+1}: the photo touches Previous")
            if m["next"] and img["r"] > m["next"]["l"] + 1: bad.append(f"photo {i+1}: the photo touches Next")
            lp.keyboard.press("ArrowRight")
        check(f"sideways {w}x{h}: all {n} photos, captions and buttons stay on the screen; photo at least 190 px tall", n > 0 and not bad and smallest >= 190, f"smallest photo {round(smallest)} px" + (" | " + "; ".join(bad[:3]) if bad else ""))
        lc.close()
    b.close()

print("\nFAILS", len(fails))
raise SystemExit(1 if fails else 0)

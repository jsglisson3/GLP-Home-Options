#!/usr/bin/env python3
"""Does the Home photo carousel work? (Checkpoint 49; js/site.js, "Photo strip", and css/site.css, "Photo strip on Home".)

Run:   python3 tools/carousel-test.py        It must print  FAILS 0.
It serves this folder on a throwaway port and opens Home in Chromium at 320, 390, 1024, 1440 and 2560 px wide (outside requests blocked).
At each width: the count starts at "1" with Previous dimmed; Next walks the count up one photo at a time to the last photo and then dims;
Previous walks back to the start; an arrow key moves the strip once it has focus; every photo frame is the same size; the buttons are
at least 44 px; the page never scrolls sideways; no script errors. Then with JavaScript off: the count and buttons stay hidden, the strip
keeps its own scrollbar and "See all our work" still shows.
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

STATE = """() => ({now: document.querySelector('.car-now').textContent,
  prev: document.querySelector('.car-prev').getAttribute('aria-disabled'),
  next: document.querySelector('.car-next').getAttribute('aria-disabled'),
  x: document.querySelector('.car-track').scrollLeft,
  over: document.documentElement.scrollWidth - window.innerWidth})"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(320, 640), (390, 844), (1024, 768), (1440, 900), (2560, 1440)]:
        ctx = b.new_context(viewport={"width": w, "height": h})
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        pg = ctx.new_page(); errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(BASE + "index.html", wait_until="networkidle")
        pg.locator("#work-strip").scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        total = len(pg.query_selector_all(".car-slide"))
        s = pg.evaluate(STATE)
        check(f"{w}px: starts at 1 with Previous dimmed, no sideways page scroll", s["now"] == "1" and s["prev"] == "true" and s["next"] == "false" and s["over"] <= 0, s)
        seen = [s["now"]]
        for _ in range(total + 2):
            pg.eval_on_selector(".car-next", "e => e.click()"); pg.wait_for_timeout(700); seen.append(pg.evaluate(STATE)["now"])
        s = pg.evaluate(STATE)
        check(f"{w}px: Next reaches {total} and dims", s["now"] == str(total) and s["next"] == "true", ",".join(seen))
        check(f"{w}px: the count climbs one photo at a time", all(int(b_) - int(a_) in (0, 1) for a_, b_ in zip(seen, seen[1:])), ",".join(seen))
        for _ in range(total + 2):
            pg.eval_on_selector(".car-prev", "e => e.click()"); pg.wait_for_timeout(700)
        s = pg.evaluate(STATE)
        check(f"{w}px: Previous returns to 1", s["now"] == "1" and s["x"] <= 2 and s["prev"] == "true", s)
        pg.focus(".car-track"); pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(800)
        check(f"{w}px: an arrow key moves the strip", pg.evaluate(STATE)["x"] > 0)
        sizes = pg.eval_on_selector_all(".car-slide img", "a => a.map(i => { const r = i.getBoundingClientRect(); return Math.round(r.width) + 'x' + Math.round(r.height); })")
        check(f"{w}px: every photo frame is the same size", len(set(sizes)) == 1, sizes[0])
        bw = pg.eval_on_selector(".car-btn", "e => e.getBoundingClientRect().width")
        check(f"{w}px: buttons at least 44 px", bw >= 44, bw)
        check(f"{w}px: no script errors", not errors, errors)
        ctx.close()

    ctx = b.new_context(java_script_enabled=False, viewport={"width": 1440, "height": 900})
    ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
    pg = ctx.new_page(); pg.goto(BASE + "index.html")
    r = pg.evaluate("""() => ({ctrl: getComputedStyle(document.querySelector('.car-ctrl')).display,
      bar: getComputedStyle(document.querySelector('.car-track')).scrollbarWidth,
      more: !!document.querySelector('.car-more').offsetParent})""")
    check("no JavaScript: count and buttons hidden, the strip keeps its scrollbar, the link shows", r["ctrl"] == "none" and r["bar"] != "none" and r["more"], r)
    ctx.close(); b.close()

print(f"\nFAILS {len(fails)}")
raise SystemExit(1 if fails else 0)

#!/usr/bin/env python3
"""Does the phone's bottom bar (Call, Text, Get my options) behave?   (added at Checkpoint 30)

Run:   python3 tools/bar-test.py [folder]        It must print  FAILS 0.   (needs: pip install playwright; playwright install chromium)

Before Checkpoint 30 the bar sat on screen for a moment while every phone page loaded, then slid away once the page's script ran.
This test holds the script back (the local server sleeps before sending js/site.js) and watches the bar:
  1) all 8 pages on a 390 x 844 phone: the bar is never on screen before the script has run;
  2) Home: tucked away at the top, slides in after the hero buttons scroll away, steps aside at the contact form, away again at the top;
  3) the script is missing (404): the page drops its "js" flag at once and the bar stays visible;
  4) the script is stuck for 9 seconds: the bar shows when the page's 6-second safety timer fires;
  5) a laptop (1280 x 800): no bar at all.
"""
import sys, pathlib, threading, http.server, socketserver, functools, time
from playwright.sync_api import sync_playwright

folder = str(pathlib.Path(sys.argv[1]).resolve()) if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent)
MODE = {"delay": 0, "fail": False}
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        try:
            if self.path.startswith("/js/site.js"):
                if MODE["fail"]: self.send_error(404); return
                time.sleep(MODE["delay"] / 1000)
            return super().do_GET()
        except (BrokenPipeError, ConnectionResetError):
            pass
class T(socketserver.ThreadingTCPServer):
    daemon_threads = True; allow_reuse_address = True
srv = T(("127.0.0.1", 0), functools.partial(H, directory=folder)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}/"
PAGES = ["index.html", "options.html", "new-homes.html", "work.html", "about.html", "contact.html", "privacy-policy.html", "terms-of-service.html"]
STATE = """() => { const b = document.querySelector('.mobile-bar'); if (!b) return null; const r = b.getBoundingClientRect(), cs = getComputedStyle(b);
  return {auto: b.classList.contains('auto'), on: b.classList.contains('on'), shown: cs.display !== 'none' && cs.visibility === 'visible' && r.top < innerHeight - 1 && r.bottom > 1,
          js: document.documentElement.classList.contains('js'), ready: !!window.__glpReady}; }"""
fails = []
def check(ok, msg):
    print(("  ok    " if ok else "  FAIL  ") + msg)
    if not ok: fails.append(msg)
def sample(pg, ms, every=60):
    out = []; t0 = time.time()
    while (time.time() - t0) * 1000 < ms:
        try:
            s = pg.evaluate(STATE)
            if s: out.append((round((time.time() - t0) * 1000), s))
        except Exception: pass
        pg.wait_for_timeout(every)
    return out
def phone(b, w=390, h=844):
    return b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, is_mobile=True, has_touch=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    print("1. every page, script held back 700 ms (390x844 phone): the bar must not be on screen before the script runs")
    MODE.update(delay=700, fail=False)
    for name in PAGES:
        ctx = phone(b); pg = ctx.new_page(); pg.goto(base + name, wait_until="commit")
        s = sample(pg, 1700)
        before = [t for t, x in s if not x["auto"] and x["shown"]]
        after_auto = [x for t, x in s if x["auto"]]
        first_auto = next((t for t, x in s if x["auto"]), None)
        check(first_auto is not None and not before, f"{name}: samples before the script {len([1 for t,x in s if not x['auto']])}, shown before script {len(before)}; script ran at ~{first_auto} ms")
        ctx.close()
    print("2. home page behavior after the script (390x844)")
    MODE.update(delay=0, fail=False)
    ctx = phone(b); pg = ctx.new_page(); pg.goto(base + "index.html"); pg.wait_for_function("window.__glpReady === true"); pg.wait_for_timeout(500)
    s = pg.evaluate(STATE); check(s["auto"] and not s["shown"], f"at the top the bar is tucked away ({s})")
    pg.mouse.move(200, 400); pg.mouse.wheel(0, 1400); pg.wait_for_timeout(1800); s = pg.evaluate(STATE); check(s["shown"], f"after scrolling past the hero buttons it is on screen ({s})")
    pg.evaluate("document.querySelector('#contact').scrollIntoView()"); pg.wait_for_timeout(1800); s = pg.evaluate(STATE); check(not s["shown"], f"at the contact form it steps aside ({s})")
    pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(1800); s = pg.evaluate(STATE); check(not s["shown"], f"back at the top it is tucked away again ({s})")
    ctx.close()
    print("3. the script is missing (404): the page drops its js flag at once and the bar stays visible")
    MODE.update(delay=0, fail=True)
    ctx = phone(b); pg = ctx.new_page(); pg.goto(base + "index.html"); pg.wait_for_timeout(1200); s = pg.evaluate(STATE)
    check((not s["js"]) and s["shown"] and not s["auto"], f"({s})")
    ctx.close()
    print("4. the script is stuck for 9 s: after the 6 s safety timer the bar shows")
    MODE.update(delay=9000, fail=False)
    ctx = phone(b); pg = ctx.new_page(); pg.goto(base + "index.html", wait_until="commit")
    s = sample(pg, 7200, every=150)
    early = [t for t, x in s if t < 5500 and x["shown"]]
    late = [x for t, x in s if t > 6600]
    check(not early and late and all(x["shown"] and not x["js"] for x in late), f"shown before 5.5 s: {len(early)}; after 6.6 s shown/js-off: {[ (x['shown'], x['js']) for x in late][-1:] }")
    ctx.close()
    print("5. desktop 1280x800: no bar at all")
    MODE.update(delay=0, fail=False)
    ctx = b.new_context(viewport={"width": 1280, "height": 800}); pg = ctx.new_page(); pg.goto(base + "index.html"); pg.wait_for_function("window.__glpReady === true"); pg.evaluate("window.scrollTo(0, 1500)"); pg.wait_for_timeout(700)
    s = pg.evaluate(STATE); check(not s["shown"], f"({s})")
    ctx.close()
    b.close()
srv.shutdown()
print("FAILS", len(fails))
sys.exit(1 if fails else 0)

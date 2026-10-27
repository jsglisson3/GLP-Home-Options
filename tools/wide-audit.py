#!/usr/bin/env python3
"""Do all 8 pages hold up on tablets, laptops and phones held sideways?

Run:   python3 tools/wide-audit.py [shots_folder]        It must print  FAILS 0.
(mobile-audit.py covers phones held upright, 320 to 430 px wide; this covers everything wider and the landscape phone sizes.)

It serves this folder on a throwaway port and opens every root page at 11 sizes (600, 700, 768, 820, 900, 1024, 1180, 1280 px wide,
and phones held sideways at 667x375, 844x390 and 932x430; touch on for all but 900 and 1280) with outside requests blocked. For each
page and size it checks: no sideways scroll; nothing sticking out past the right edge; the header shows either the menu bar or the
Menu button (never neither); the menu bar never wraps to two lines; the headline does not start below the first screen.
Give a folder name and it also saves a first-screen picture of every page and size there (keep the folder outside the project).
"""
import functools, http.server, os, pathlib, socketserver, sys, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = sys.argv[1] if len(sys.argv) > 1 else None
if SHOTS: os.makedirs(SHOTS, exist_ok=True)
PAGES = _site.page_slugs()   # every page in the folder, found by tools/_site.py
# (label, width, height, touch)
SIZES = [("w600", 600, 900, True), ("w700", 700, 900, True), ("w768", 768, 1024, True), ("w820", 820, 1180, True), ("w900", 900, 1100, False),
         ("w1024", 1024, 768, True), ("w1180", 1180, 820, True), ("w1280", 1280, 800, False),
         ("sideways667", 667, 375, True), ("sideways844", 844, 390, True), ("sideways932", 932, 430, True)]

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS = """() => {
  const vw = document.documentElement.clientWidth;
  const over = document.documentElement.scrollWidth - vw;
  const offenders = [];
  // content inside a sideways scroller (the Home photo carousel, Checkpoint 47) is meant to run past the edge: the scroller clips it, and the
  // scroller's own box and the page's sideways scroll ("over") are still checked
  const inScroller = e => !!(e.parentElement && e.parentElement.closest('.car-track'));   // only the carousel: other scrollers (the compare table) must still fit
  document.querySelectorAll('body *').forEach(e => {
    const cs = getComputedStyle(e); if (cs.position === 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') return;
    if (inScroller(e)) return;
    const r = e.getBoundingClientRect(); if (r.width === 0) return;
    if (r.right > vw + 1) offenders.push(e.tagName.toLowerCase() + ' right edge at ' + Math.round(r.right));
  });
  const nav = document.querySelector('.hdr .nav'); const navShown = nav ? getComputedStyle(nav).display !== 'none' : false;
  let navLines = null;
  if (navShown) navLines = new Set([...nav.querySelectorAll('a')].map(a => Math.round(a.getBoundingClientRect().top))).size;
  const menuBtn = document.querySelector('.hdr .menu-btn'); const menuShown = menuBtn ? getComputedStyle(menuBtn).display !== 'none' : false;
  const h1 = document.querySelector('h1'); const h1r = h1 ? h1.getBoundingClientRect() : null;
  return {over, offenders: offenders.slice(0, 3), navShown, navLines, menuShown, h1Top: h1r ? Math.round(h1r.top) : null, vh: innerHeight};
}"""

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for label, w, h, touch in SIZES:
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=touch, is_mobile=touch and w < 1000, reduced_motion="reduce")
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        for name in PAGES:
            pg = ctx.new_page()
            pg.goto(BASE + name + ".html", wait_until="load"); pg.wait_for_timeout(700)
            r = pg.evaluate(JS); problems = []
            if r["over"] > 0: problems.append(f"sideways scroll of {r['over']} px")
            if r["offenders"]: problems.append("sticks out past the right edge: " + "; ".join(r["offenders"]))
            if r["navShown"] and r["navLines"] and r["navLines"] > 1: problems.append(f"the menu bar wraps to {r['navLines']} lines")
            if not r["navShown"] and not r["menuShown"]: problems.append("no menu bar and no Menu button")
            if r["h1Top"] is not None and r["h1Top"] > r["vh"]: problems.append(f"the headline starts below the first screen (top at {r['h1Top']} of {r['vh']})")
            if problems:
                fails.append(f"{label} {name}")
                print("FAIL  " + f"{label:12s} {name:21s} " + " | ".join(problems))
            if SHOTS: pg.screenshot(path=os.path.join(SHOTS, f"{label}_{name}.png"))
            pg.close()
        ctx.close()
    b.close()
print(f"checked {len(PAGES)} pages at {len(SIZES)} sizes")
print("\nFAILS", len(fails))
raise SystemExit(1 if fails else 0)

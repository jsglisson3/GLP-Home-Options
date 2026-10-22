#!/usr/bin/env python3
"""Full-page screenshots of the built pages, for before/after comparisons (Session 5 and later).

Usage:   python3 tools/shots.py OUTDIR [page ...] [--widths=320,390,768,1024,1440]
         (pages default to all 7, names without .html; widths default to 1440,390)
Example: python3 tools/shots.py ../shots-before
         ...make the change...
         python3 tools/shots.py ../shots-after
         python3 tools/shots-diff.py ../shots-before ../shots-after

Needs Playwright with Chromium. It serves the project folder itself (no other server needed),
blocks outside requests so the GoHighLevel form cannot change the picture, turns motion off so
animations cannot, scrolls down the page first (photos use lazy loading, so they stay blank
otherwise), hides the phone bottom bar, and writes OUTDIR/<page>_<width>.png at 1440 and 390 wide.
Keep OUTDIR outside the project folder, or it will be picked up by the checkpoint tool.
"""
import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL = ["index", "options", "about", "new-homes", "contact", "privacy-policy", "terms-of-service"]
WIDTHS = [(1440, False), (390, True)]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    out = os.path.abspath(sys.argv[1])
    args = sys.argv[2:]
    widths = WIDTHS
    for a in list(args):
        if a.startswith("--widths="):
            widths = [(int(x), int(x) < 600) for x in a.split("=", 1)[1].split(",") if x]
            args.remove(a)
    pages = args or ALL
    os.makedirs(out, exist_ok=True)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=ROOT))
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, mobile in widths:
            c = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1, has_touch=mobile,
                              is_mobile=mobile, reduced_motion="reduce")
            c.route("**/*", lambda r: r.continue_() if r.request.url.startswith(f"http://127.0.0.1:{port}") else r.abort())
            for name in pages:
                pg = c.new_page()
                pg.goto(f"http://127.0.0.1:{port}/{name}.html", wait_until="load")
                pg.wait_for_timeout(1200)
                h = pg.evaluate("document.documentElement.scrollHeight")
                y = 0
                while y < h:
                    pg.evaluate(f"window.scrollTo(0,{y})")
                    pg.wait_for_timeout(160)
                    y += 650
                pg.wait_for_timeout(1000)
                pg.evaluate("window.scrollTo(0,0)")
                pg.evaluate("document.querySelectorAll('.rv').forEach(e=>e.classList.add('in'))")
                pg.add_style_tag(content=".mobile-bar{display:none!important}")
                pg.wait_for_timeout(600)
                path = os.path.join(out, f"{name}_{w}.png")
                pg.screenshot(path=path, full_page=True)
                print("wrote", path, "height", pg.evaluate("document.documentElement.scrollHeight"))
                pg.close()
            c.close()
        b.close()
    srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())

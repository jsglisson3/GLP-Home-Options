"""Does a change alter how anything looks?   (added at Checkpoint 32)

Run:   python3 tools/computed-diff.py <folder A> <folder B>        It must print  PAGES WITH DIFFERENCES 0.   (needs: pip install playwright; playwright install chromium)

Compares two copies of the site (say, last checkpoint and this one) by asking the browser, for EVERY element on every page at seven screen widths
(320 to 1920 px), where it is, how big it is and every style value it computed. Zero differences means the change is invisible to modern browsers.
Pictures are not compared on purpose: full-page screenshots of the same page differ from run to run (photos decode at different moments), so
that test cries wolf; computed styles do not. Used at Checkpoint 32 to show the older-phone fallback lines change nothing in a modern browser
(56 page-and-width pairs, 22,771 elements, 0 differences). It reads the style values in one step and compares them as a set, because the order a browser
lists them in can vary from load to load."""
import sys, threading, functools, http.server, socketserver, json
from playwright.sync_api import sync_playwright
if len(sys.argv) < 3: sys.exit(__doc__)
A, B = sys.argv[1], sys.argv[2]
import _site  # finds the pages
pages = [x for x in _site.page_slugs(A, include_404=False) if x in _site.page_slugs(B, include_404=False)]   # pages in BOTH folders; a page only one folder has is listed below
only = sorted(set(_site.page_slugs(A, include_404=False)) ^ set(_site.page_slugs(B, include_404=False)))
if only: print("NOT COMPARED (in only one folder):", ", ".join(only))
widths = [(320, 700), (375, 812), (414, 896), (768, 1024), (1024, 768), (1280, 800), (1920, 1080)]
socketserver.ThreadingTCPServer.allow_reuse_address = True
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def handle(self):
        try: super().handle()
        except (BrokenPipeError, ConnectionResetError): pass
def serve(d, port):
    s = socketserver.ThreadingTCPServer(("127.0.0.1", port), functools.partial(Q, directory=d)); s.daemon_threads = True
    threading.Thread(target=s.serve_forever, daemon=True).start()
serve(A, 8761); serve(B, 8762)
JS = """() => {
  const out = [];
  const els = document.querySelectorAll('html, body, body *');
  els.forEach((el, i) => {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    const parts = [];
    for (const p of cs) parts.push(p + ':' + cs.getPropertyValue(p));
    out.push([el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\\s+/).join('.') : ''), [r.x, r.y, r.width, r.height].map(v => Math.round(v * 100) / 100).join(','), parts.join('\\n')]);
  });
  return out;
}"""
DETAIL = """(i) => { const el = document.querySelectorAll('html, body, body *')[i]; const cs = getComputedStyle(el); const o = {}; for (const p of cs) o[p] = cs.getPropertyValue(p); return o; }"""
def load(pg, port, name):
    pg.goto(f"http://127.0.0.1:{port}/{name}.html", wait_until="load")
    pg.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important}")
    pg.evaluate("document.querySelectorAll('img').forEach(i=>{i.loading='eager'})")
    pg.wait_for_timeout(1300)
bad = 0; total = 0; elems = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for (w, h) in widths:
        ctx = b.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce")
        pa, pb = ctx.new_page(), ctx.new_page()
        for name in pages:
            load(pa, 8761, name); load(pb, 8762, name)
            ra, rb = pa.evaluate(JS), pb.evaluate(JS)
            total += 1; elems += len(ra)
            diffs = []
            if len(ra) != len(rb): diffs.append(f"element count {len(ra)} vs {len(rb)}")
            else:
                for i, (x, y) in enumerate(zip(ra, rb)):
                    da = dict(l.split(":", 1) for l in x[2].split("\n") if ":" in l); db = dict(l.split(":", 1) for l in y[2].split("\n") if ":" in l)
                    if x[1] != y[1] or da != db or x[0] != y[0]:
                        what = []
                        if x[0] != y[0]: what.append(f"element {x[0]} vs {y[0]}")
                        if x[1] != y[1]: what.append(f"box {x[1]} vs {y[1]}")
                        if da != db:
                            what.append("style " + ", ".join(f"{k}: {da.get(k)} -> {db.get(k)}" for k in sorted(set(da) | set(db)) if da.get(k) != db.get(k))[:260])
                        diffs.append(f"{x[0][:50]}: " + "; ".join(what))
            if diffs: bad += 1
            print(f"{w:>5} {name:<18} {len(ra):>5} elements  " + ("same" if not diffs else f"{len(diffs)} DIFFERENCES: " + " | ".join(diffs[:5])), flush=True)
        ctx.close()
    b.close()
print("PAGES WITH DIFFERENCES", bad, "of", total, "checked", elems, "elements")
sys.exit(1 if bad else 0)

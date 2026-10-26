#!/usr/bin/env python3
"""Phone audit for the GLP Home Options site: the numbers behind "is the mobile version elite?".

Run:   python3 tools/mobile-audit.py [page.html ...]        (needs: pip install playwright; playwright install chromium)
For every page at 320, 360, 390 and 430 px wide (touch on, outside requests blocked) it reports:
  sideways overflow; things wider than the screen; text under 14 px; tap targets under 44 px (links inside a sentence are exempt);
  form fields under 16 px (iOS zooms the page in on them); images that are far bigger than they are shown; images with no
  width and height (the page jumps as they load).
Then, at 390 px with a slow phone (4x slower processor, slow 4G), it reports the largest paint, layout shift, total bytes and
request count. It changes nothing. Goal: no "overflow", no tiny tap targets, no zoom-prone fields, LCP under 2.5 s, CLS under 0.1.
"""
import functools, http.server, json, pathlib, socketserver, sys, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sys.argv[1:] or _site.page_files()   # every page in the folder, found by tools/_site.py
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()

PROBE = r"""
() => {
  const W = window.innerWidth, out = {W, overflow: Math.max(0, document.documentElement.scrollWidth - W)};
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0; };
  const sel = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const clipped = e => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p); if (/(hidden|auto|scroll|clip)/.test(o.overflowX)) return true; } return false; };
  out.wide = [...document.body.querySelectorAll('*')].filter(e => vis(e) && !clipped(e) && e.getBoundingClientRect().right > W + 1 && getComputedStyle(e).position !== 'fixed').slice(0, 5).map(sel);
  const small = new Map();
  document.body.querySelectorAll('*').forEach(e => { if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2) || !vis(e)) return; const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 14) small.set(sel(e) + ' ' + fs + 'px', (small.get(sel(e) + ' ' + fs + 'px') || 0) + 1); });
  out.smallText = [...small.entries()].slice(0, 6).map(([k, v]) => k + ' x' + v);
  const inline = a => { const p = a.closest('p,li,dd,td'); const d = getComputedStyle(a).display;   // the phone number in a sentence is an inline-block (class nb) so it moves whole: still an in-sentence link
    return p && a.parentElement !== document.body && (d === 'inline' || (d === 'inline-block' && a.classList.contains('nb'))) && a.textContent.trim().length < p.textContent.trim().length - 8; };
  out.tap = [...document.querySelectorAll('a,button,summary,input:not([type=hidden]),select,textarea,[role=button]')].filter(e => vis(e) && !inline(e)).map(e => { const r = e.getBoundingClientRect(); return [sel(e), Math.round(r.width), Math.round(r.height)]; }).filter(x => x[1] < 44 || x[2] < 44).slice(0, 8).map(x => x[0] + ' ' + x[1] + 'x' + x[2]);
  out.zoomFields = [...document.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(e => vis(e) && parseFloat(getComputedStyle(e).fontSize) < 16).map(sel).slice(0, 6);
  out.bigImgs = [...document.images].filter(i => i.naturalWidth && i.getBoundingClientRect().width > 0 && i.naturalWidth > i.getBoundingClientRect().width * 3).map(i => i.getAttribute('src').split('/').pop() + ' ' + i.naturalWidth + 'px shown at ' + Math.round(i.getBoundingClientRect().width)).slice(0, 6);
  out.noDims = [...document.images].filter(i => !i.getAttribute('width') || !i.getAttribute('height')).map(i => (i.getAttribute('src') || '').split('/').pop()).slice(0, 6);
  return out;
}
"""

def scroll_through(pg):
    h = pg.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        pg.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})"); pg.wait_for_timeout(60); y += 600
    pg.evaluate("window.scrollTo({top: 0, behavior: 'instant'})"); pg.wait_for_timeout(200)

with sync_playwright() as p:
    b = p.chromium.launch()
    def ctx(w):
        c = b.new_context(viewport={"width": w, "height": 800 if w < 400 else 900}, is_mobile=True, has_touch=True, device_scale_factor=3)
        c.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        return c
    print("=== LAYOUT AT PHONE WIDTHS ===")
    for page in PAGES:
        for w in (320, 360, 390, 430):
            c = ctx(w); pg = c.new_page(); pg.goto(BASE + page); pg.wait_for_timeout(900)
            pg.mouse.move(50, 200); pg.mouse.wheel(0, 50); scroll_through(pg)
            r = pg.evaluate(PROBE); c.close()
            bad = {k: v for k, v in r.items() if v and k not in ("W",)}
            print(f"{page:20s} {w:>3}px  " + ("clean" if not bad else json.dumps(bad, ensure_ascii=False)))
    print("\n=== SPEED ON A SLOW PHONE (390 px, 4x slower processor, slow 4G) ===")
    for page in PAGES:
        c = ctx(390); pg = c.new_page(); cdp = c.new_cdp_session(pg)
        cdp.send("Network.enable"); cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        pg.add_init_script("""window.__m = {lcp: 0, cls: 0}; new PerformanceObserver(l => { for (const e of l.getEntries()) window.__m.lcp = e.startTime; }).observe({type: 'largest-contentful-paint', buffered: true});
          new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__m.cls += e.value; }).observe({type: 'layout-shift', buffered: true});""")
        pg.goto(BASE + page, wait_until="load"); pg.wait_for_timeout(2500)
        m = pg.evaluate("""() => { const r = performance.getEntriesByType('resource'); const nav = performance.getEntriesByType('navigation')[0];
          return {lcp: Math.round(window.__m.lcp), cls: +window.__m.cls.toFixed(3), kb: Math.round((r.reduce((s, e) => s + (e.encodedBodySize || 0), 0) + (nav.encodedBodySize || 0)) / 1024), reqs: r.length + 1, load: Math.round(nav.loadEventEnd)}; }""")
        c.close()
        print(f"{page:20s} LCP {m['lcp']:>5} ms   CLS {m['cls']:<6} load {m['load']:>5} ms   {m['kb']:>5} KB in {m['reqs']} requests (above the fold and the rest that loaded)")
    b.close()

#!/usr/bin/env python3
"""Does any paragraph, list item, question or caption end on one lonely word?   (a "single-word last line")

Run:   python3 tools/orphan-check.py        It prints each one it finds and  FAILS 0  when there are 6 or fewer.
It serves this folder on a throwaway port and opens all 8 pages at six widths (320, 390, 820, 1024, 1280 and 1440 px) in Chromium, then
measures where every text block breaks its lines. css/site.css asks the browser to avoid lonely last words (`text-wrap: pretty` on
paragraphs, `balance` on list items, questions and table cells); Chrome, Edge and Safari obey, other browsers ignore it.
At Checkpoint 27 the count went from 208 to 4. The 4 known ones: the two-word label "COMING SOON . CHATTANOOGA" at 320 px, one Terms of
Service line at 320 px (legal text is not touched), and two net sheet labels ("Repairs and prep", "Cost of waiting") at 1024 px. After
editing words, run this: a new lonely word usually means a small rewording (or a non-breaking space, `&nbsp;`, between the last two words,
as in "stays&nbsp;confidential.").
"""
import functools, http.server, pathlib, socketserver, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = _site.page_slugs()   # every page in the folder, found by tools/_site.py
WIDTHS = [(320, 700), (390, 844), (820, 1180), (1024, 768), (1280, 800), (1440, 900)]
LIMIT = 6

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS = r"""() => {
  const BLOCKS = 'p, li, dd, dt, figcaption, summary, h1, h2, h3, h4, blockquote, td, th';
  const NESTED = 'p, li, dd, dt, figcaption, summary, h1, h2, h3, h4, blockquote';
  const out = [];
  document.querySelectorAll(BLOCKS).forEach(el => {
    if (el.closest('.mnav, .lb, template, noscript')) return;
    const cs0 = getComputedStyle(el); if (cs0.display === 'none' || cs0.visibility === 'hidden') return;
    if (el.closest('details:not([open])') && el.tagName !== 'SUMMARY') return;
    if (el.closest('thead') && el.closest('table.cmp') && innerWidth <= 700) return;   // the phone table hides its header row
    if (el.querySelector(NESTED)) return;
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const words = []; let n;
    while ((n = tw.nextNode())) {
      const pe = n.parentElement; const cs = getComputedStyle(pe);
      if (cs.display === 'none' || cs.visibility === 'hidden' || pe.closest('.vh, svg, script, style')) continue;
      const re = /\S+/g; let m;
      while ((m = re.exec(n.nodeValue))) {
        const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
        const rc = r.getClientRects(); if (!rc.length) continue;
        words.push({w: m[0], top: rc[rc.length - 1].top, bottom: rc[rc.length - 1].bottom});
      }
    }
    if (words.length < 3) return;
    const lines = [];
    words.forEach(x => { const l = lines.find(L => Math.abs(L.top - x.top) < 5 || (x.top < L.bottom - 4 && x.bottom > L.top + 4)); if (l) l.ws.push(x.w); else lines.push({top: x.top, bottom: x.bottom, ws: [x.w]}); });
    if (lines.length < 2) return;
    lines.sort((a, b) => a.top - b.top);
    const last = lines[lines.length - 1];
    if (last.ws.length === 1) out.push({tag: el.tagName.toLowerCase(), last: last.ws[0], lines: lines.length, text: (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60)});
  });
  return out;
}"""

found = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for (w, h) in WIDTHS:
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, has_touch=w < 1000, is_mobile=w < 600, reduced_motion="reduce")
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        for name in PAGES:
            pg = ctx.new_page(); pg.goto(BASE + name + ".html", wait_until="load"); pg.wait_for_timeout(500)
            for o in pg.evaluate(JS):
                found.append(o)
                print(f"{w:5d} px  {name:17s} <{o['tag']}> {o['lines']} lines, last line is just {o['last']!r}   | {o['text']}")
            pg.close()
        ctx.close()
    b.close()
print(f"\nsingle-word last lines: {len(found)} (limit {LIMIT})")
print("\nFAILS", 0 if len(found) <= LIMIT else len(found) - LIMIT)
raise SystemExit(0 if len(found) <= LIMIT else 1)

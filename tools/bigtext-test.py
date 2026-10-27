#!/usr/bin/env python3
"""Does everything still work when a reader makes the text bigger?   (added at Checkpoint 28, letters mode added at Checkpoint 29)

Run:   python3 tools/bigtext-test.py [folder]        It must print  FAILS 0.   (needs: pip install playwright; playwright install chromium)

Older homeowners are a big part of the audience, and many of them enlarge their text. Three ways people do it, all tested:
  A) "root": the page's root text size grows (the way a phone's text zoom can behave: rem and em lengths grow with the text).
     Simulated by setting the root text size to 125%, 150% and 200% at 390, 360 and 320 px wide.
  B) "default font": in a laptop or tablet browser (Chrome or Edge: Settings > Appearance > Font size) the browser's default font gets bigger.
     Simulated with the DevTools "default font size" setting (20 px is "Large", 24 px "Very large") at 820, 1024, 1280, 1440, 1600 and 1920 px wide.
  G) "letters": only the letters grow, and the screen width, the px caps and the rem lengths stay put. This is how Android Chrome's font
     size and the iPhone Safari "aA" text size really behave, so it is the strictest test. Simulated by multiplying every element's text size
     by 125%, 150% or 200% (phones 390, 360, 320 and 412; tablets 768 to 1180; two phones held sideways). Not run at 1200 px and wider:
     laptop and desktop browsers do not enlarge letters on their own (they use the font setting, mode B, or page zoom, which is the same as a
     narrower screen), and on Home the "now building" card keeps its one-row layout from 1200 px up, so an Android tablet held sideways at
     1280 px with a big font setting is a known gap.
For every page and every size (with every FAQ answer opened) it checks:
  no sideways scroll; nothing sticks out past the right or left edge; no text sticks out of its own box (a button, a card, a cell);
  no piece of text runs into another piece of text; the header shows the menu bar on one line or the Menu button fully on the screen;
  on phones the bottom call bar keeps all three buttons on the screen; the "skip to content" link stays hidden.
Then, on phones, with the page scrolled down so the bottom call bar is showing, it opens the Menu and the Our work photo viewer at 100%, 125%,
150% and 200% text (and at three short phones at the normal text size: 320x568, 360x640, 375x667): every menu item can be scrolled into view
above the bar, nothing sticks out of the menu, the Menu button stays on the screen; every viewer button, the photo and its caption stay on the
screen without overlapping.
The 200% phone sizes at 320 px, the 24 px default font at 820 px and 200% letters at 1024 px and wider are not checked (extreme corners);
everything else must pass.
Two layers keep the page usable. (1) The px caps (min(Xrem,Ypx)) hold the logo and the Menu word at their normal size when the browser's
default font grows (modes A and B). (2) The structure does not depend on the caps: the logo can shrink and wrap, the Menu button never
shrinks, buttons and cards wrap onto a new row instead of overflowing (mode G, where the caps cannot help). Every width breakpoint in
css/site.css is written in em (61.25em is 980px at the normal size), so layouts fold earlier when the browser's default font gets bigger;
that is why mode B needs the DevTools setting (it moves the em in a media query; a root text scale does not).
Give a folder name to test a copy of the site instead of this project (used to compare before and after a change). Run on the Checkpoint 27
pages it fails most of its combinations (the Menu button off the screen, a bottom bar that loses a button, text running into other text);
at Checkpoint 29 it fails none.
"""
import functools, http.server, pathlib, socketserver, sys, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
PAGES = _site.page_slugs()   # every page in the folder, found by tools/_site.py
# (label, width, height, mode, amount): mode "scale" = root text size in percent (A), "font" = browser default font size in px (B), "letters" = every element's text size in percent (G)
RUNS = [("phone 390", 390, 844, "scale", p) for p in (125, 150, 200)] + \
       [("phone 360", 360, 740, "scale", p) for p in (125, 150, 200)] + \
       [("phone 320", 320, 700, "scale", p) for p in (125, 150)] + \
       [("tablet 820", 820, 1100, "font", 20)] + \
       [("laptop 1024", 1024, 768, "font", px) for px in (20, 24)] + \
       [("laptop 1280", 1280, 800, "font", px) for px in (20, 24)] + \
       [("desktop 1440", 1440, 900, "font", px) for px in (20, 24)] + \
       [("desktop 1600", 1600, 900, "font", px) for px in (20, 24)] + \
       [("desktop 1920", 1920, 1080, "font", px) for px in (20, 24)] + \
       [("phone 390", 390, 844, "letters", p) for p in (125, 150, 200)] + \
       [("phone 360", 360, 740, "letters", p) for p in (125, 150, 200)] + \
       [("phone 320", 320, 700, "letters", p) for p in (125, 150)] + \
       [("phone 412", 412, 915, "letters", p) for p in (150, 200)] + \
       [("sideways 844", 844, 390, "letters", 150), ("sideways 667", 667, 375, "letters", 150)] + \
       [("tablet 768", 768, 1024, "letters", p) for p in (125, 150, 200)] + \
       [("tablet 820", 820, 1180, "letters", p) for p in (125, 150, 200)] + \
       [("tablet 1024", 1024, 768, "letters", p) for p in (125, 150)] + \
       [("tablet 1180", 1180, 820, "letters", p) for p in (125, 150)]

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
class Threaded(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True
srv = Threaded(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()

JS = r"""() => {
  const vw = document.documentElement.clientWidth;
  const label = e => e.tagName.toLowerCase() + (typeof e.className === 'string' && e.className ? '.' + e.className.trim().split(/\s+/)[0] : '');
  const skipThese = '.mnav, template, noscript, svg, .vh, .skip, .lb:not([open]), thead';
  const probs = [];
  const over = document.documentElement.scrollWidth - vw;
  if (over > 0) probs.push('sideways scroll of ' + over + ' px');
  const past = [];
  // content inside a sideways scroller (the Home photo carousel, Checkpoint 47) is meant to run past the edge: the scroller clips it, and the
  // scroller's own box, and the page as a whole ("sideways scroll" above), are still checked
  const inScroller = e => !!(e.parentElement && e.parentElement.closest('.car-track'));   // only the carousel: other scrollers (the compare table) must still fit
  document.querySelectorAll('body *').forEach(e => {
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return;
    if (e.closest(skipThese) || inScroller(e)) return;
    const r = e.getBoundingClientRect(); if (r.width === 0 || r.height === 0) return;
    if (r.right > vw + 1 || r.left < -1) past.push(label(e) + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
  });
  if (past.length) probs.push(past.length + ' past the edge, e.g. ' + past.slice(0, 2).join('; '));
  const stick = [];
  document.querySelectorAll('body *').forEach(e => {
    if (e.closest(skipThese)) return;
    const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || cs.display === 'inline') return;
    if (/(auto|scroll)/.test(cs.overflowX) || e.clientWidth < 2) return;
    if (![...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())) return;
    if (e.scrollWidth > e.clientWidth + 1) stick.push(label(e) + ' ' + e.scrollWidth + '>' + e.clientWidth + ' "' + e.textContent.trim().replace(/\s+/g, ' ').slice(0, 22) + '"');
  });
  if (stick.length) probs.push(stick.length + ' text sticks out of its box, e.g. ' + stick.slice(0, 2).join('; '));
  // no piece of text may run into another piece of text (compares the line boxes of every text run, trimmed to the letters' height; skips the fixed header and bar)
  const lines = [], tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let tn;
  while ((tn = tw.nextNode())) {
    if (!tn.nodeValue.trim()) continue;
    const pe = tn.parentElement; if (!pe || pe.closest(skipThese)) continue;
    let hide = false;
    for (let e = pe; e && e !== document.documentElement; e = e.parentElement) {
      const c = getComputedStyle(e);
      if (c.display === 'none' || c.visibility === 'hidden' || parseFloat(c.opacity) === 0 || c.position === 'fixed' || c.position === 'sticky') { hide = true; break; }
    }
    if (hide || (pe.closest('details:not([open])') && !pe.closest('summary'))) continue;
    const rg = document.createRange(); rg.selectNodeContents(tn);
    [...rg.getClientRects()].forEach(x => { if (x.width > 1 && x.height > 1) lines.push({l: x.left, t: x.top + x.height * 0.14 + scrollY, r: x.right, b: x.bottom - x.height * 0.14 + scrollY, pe, s: tn.nodeValue.trim().replace(/\s+/g, ' ').slice(0, 18)}); });
  }
  lines.sort((a, b) => a.t - b.t);
  const runs = [];
  for (let i = 0; i < lines.length; i++) for (let j = i + 1; j < lines.length; j++) {
    const a = lines[i], c = lines[j]; if (c.t >= a.b - 6) break;
    if (a.pe === c.pe || a.pe.contains(c.pe) || c.pe.contains(a.pe)) continue;
    if (Math.min(a.r, c.r) - Math.max(a.l, c.l) >= 3 && Math.min(a.b, c.b) - Math.max(a.t, c.t) >= 6) runs.push('"' + a.s + '" and "' + c.s + '"');
  }
  if (runs.length) probs.push(runs.length + ' text runs into other text, e.g. ' + runs.slice(0, 2).join('; '));
  // header
  const nav = document.querySelector('.hdr .nav'), mb = document.querySelector('.hdr .menu-btn'), brand = document.querySelector('.hdr .brand');
  const navShown = nav && getComputedStyle(nav).display !== 'none', menuShown = mb && getComputedStyle(mb).display !== 'none';
  if (!navShown && !menuShown) probs.push('header: no menu bar and no Menu button');
  if (menuShown) {
    const m = mb.getBoundingClientRect(), b = brand.getBoundingClientRect();
    if (m.right > vw - 2 || m.left < 0) probs.push('header: the Menu button is off the screen (' + Math.round(m.left) + '..' + Math.round(m.right) + ' of ' + vw + ')');
    if (b.right > m.left - 2) probs.push('header: the logo runs into the Menu button');
  }
  if (navShown) {
    const tops = new Set([...nav.querySelectorAll('a')].map(a => Math.round(a.getBoundingClientRect().top)));
    if (tops.size > 1) probs.push('header: the menu bar wraps to ' + tops.size + ' lines');
    ['.hdr-cta', '.hdr-fb'].forEach(sel => { const x = document.querySelector('.hdr ' + sel); if (x && getComputedStyle(x).display !== 'none') { const r = x.getBoundingClientRect(); if (r.right > vw - 2) probs.push('header: ' + sel + ' is off the screen'); } });
  }
  // bottom call bar (phones)
  const bar = document.querySelector('.mobile-bar');
  if (bar && getComputedStyle(bar).display !== 'none') {
    bar.classList.add('on');
    const rs = [...bar.querySelectorAll('a')].map(a => a.getBoundingClientRect());
    if (rs.length !== 3 || rs.some(r => r.left < -1 || r.right > vw + 1 || r.width < 40)) probs.push('call bar: a button is off the screen or squeezed');
  }
  // skip link hidden
  const sk = document.querySelector('.skip'); if (sk) { const r = sk.getBoundingClientRect(); if (r.bottom > 0) probs.push('the skip link peeks into view'); }
  return probs;
}"""

# the open Menu and the photo viewer on phones (width, height, text percent)
OVERLAY_RUNS = [(320, 568, 100, "scale"), (360, 640, 100, "scale"), (375, 667, 100, "scale"), (390, 844, 100, "scale"), (412, 915, 100, "scale"),
                (390, 844, 125, "scale"), (390, 844, 150, "scale"), (390, 844, 200, "scale"), (360, 740, 150, "scale"), (360, 740, 200, "scale"),
                (320, 700, 125, "scale"), (320, 700, 150, "scale"),
                (375, 667, 125, "letters"), (390, 844, 150, "letters"), (390, 844, 200, "letters"), (360, 740, 150, "letters"), (360, 740, 200, "letters"),
                (320, 700, 125, "letters"), (320, 700, 150, "letters"), (412, 915, 150, "letters")]
MENU_JS = r"""() => {
  const probs = [], vw = document.documentElement.clientWidth, vh = innerHeight;
  const panel = document.querySelector('.mnav'); if (!panel || getComputedStyle(panel).display === 'none') return ['the menu did not open'];
  const pr = panel.getBoundingClientRect();
  if (pr.left < -1 || pr.right > vw + 1) probs.push('the panel sticks out sideways ' + Math.round(pr.left) + '..' + Math.round(pr.right));
  if (panel.scrollWidth > panel.clientWidth + 1) probs.push('the panel content is wider than the panel ' + panel.scrollWidth + '>' + panel.clientWidth);
  const items = [...panel.querySelectorAll('a, button')].filter(e => getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0);
  items.forEach(e => { const r = e.getBoundingClientRect(); if (r.left < -1 || r.right > vw + 1) probs.push('an item is off the side: ' + e.textContent.trim().slice(0, 20) + ' ' + Math.round(r.left) + '..' + Math.round(r.right)); });
  panel.querySelectorAll('*').forEach(e => { const cs = getComputedStyle(e);
    if (e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 2 && [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim()) && !/(auto|scroll)/.test(cs.overflowX) && cs.display !== 'inline')
      probs.push('text sticks out: ' + e.tagName.toLowerCase() + ' ' + e.scrollWidth + '>' + e.clientWidth + ' "' + e.textContent.trim().slice(0, 20) + '"'); });
  panel.scrollTop = panel.scrollHeight;   // can the last item be reached? look at what is on top of it
  const last = items[items.length - 1], lr = last.getBoundingClientRect();
  const hit = document.elementFromPoint(lr.left + lr.width / 2, Math.max(lr.top + 4, Math.min(lr.bottom - 4, vh - 1)));
  if (!(hit && (hit === last || last.contains(hit)))) probs.push('the last menu item is covered by ' + (hit ? hit.tagName.toLowerCase() : 'nothing') + ' (item at y ' + Math.round(lr.top) + '..' + Math.round(lr.bottom) + ' of ' + vh + ')');
  if (lr.bottom > vh + 1) probs.push('the last menu item is below the screen (' + Math.round(lr.bottom) + ' > ' + vh + ')');
  const m = document.querySelector('.hdr .menu-btn').getBoundingClientRect();
  if (m.right > vw - 2 || m.left < 0) probs.push('the Menu button is off the screen');
  return probs;
}"""
VIEWER_JS = r"""() => {
  const probs = [], vw = document.documentElement.clientWidth, vh = innerHeight;
  const lb = document.querySelector('dialog.lb[open]'); if (!lb) return ['the viewer did not open'];
  const parts = {close: '.lb-close', prev: '.lb-prev', next: '.lb-next', count: '.lb-count', caption: '.lb-cap', photo: '.lb-img'}, R = {};
  for (const k in parts) { const e = lb.querySelector(parts[k]); if (!e) { probs.push('missing ' + k); continue; } R[k] = e.getBoundingClientRect(); const r = R[k];
    if (r.left < -1 || r.right > vw + 1 || r.top < -1 || r.bottom > vh + 1) probs.push(k + ' is off the screen'); }
  const keys = Object.keys(R);
  for (let i = 0; i < keys.length; i++) for (let j = i + 1; j < keys.length; j++) { const a = R[keys[i]], b = R[keys[j]];
    if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 3 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 3) probs.push(keys[i] + ' overlaps ' + keys[j]); }
  if (R.photo && R.photo.height < 120) probs.push('the photo is only ' + Math.round(R.photo.height) + ' px tall');
  return probs;
}"""

# mode G: every element's text size times n (the root size, the lengths and the px caps stay as they are)
LETTERS_JS = r"""(n) => { const els = [...document.querySelectorAll('body, body *')];
  const sizes = els.map(e => parseFloat(getComputedStyle(e).fontSize));
  els.forEach((e, i) => e.style.setProperty('font-size', (sizes[i] * n) + 'px', 'important')); }"""

fails = []
checked = 0
checked_overlays = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for (label, w, h, mode, amount) in RUNS:
        mobile = w < 700 or mode == "letters" and w <= 1366
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=mobile, has_touch=w < 1000 or mode == "letters" and w <= 1366, reduced_motion="reduce")
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        for name in PAGES:
            pg = ctx.new_page()
            if mode == "font":
                cdp = ctx.new_cdp_session(pg); cdp.send("Page.enable"); cdp.send("Page.setFontSizes", {"fontSizes": {"standard": amount, "fixed": 16}})
            pg.goto(BASE + name + ".html", wait_until="load")
            pg.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}")
            pg.wait_for_timeout(250)
            for y in range(0, 14000, 700):
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(15)
            pg.evaluate("window.scrollTo(0,0)")
            if mode == "scale":
                pg.evaluate(f"document.documentElement.style.fontSize = '{amount}%'")
            elif mode == "letters":
                pg.evaluate(f"({LETTERS_JS})({amount / 100})")
            pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")   # every FAQ answer open, so long words in the answers are tested too
            pg.wait_for_timeout(300)
            probs = pg.evaluate(JS)
            checked += 1
            tag = {"scale": f"{amount}% root", "letters": f"{amount}% letters", "font": f"default font {amount}px"}[mode]
            if probs:
                fails.append((label, tag, name))
                print(f"FAIL  {label:12s} {tag:18s} {name:17s} " + " | ".join(probs))
            pg.close()
        ctx.close()
    for (w, h, pct, omode) in OVERLAY_RUNS:
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=True, has_touch=True, reduced_motion="reduce")
        ctx.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
        for name, kind in (("index", "menu"), ("work", "photo viewer")):
            pg = ctx.new_page(); pg.goto(BASE + name + ".html", wait_until="load")
            pg.add_style_tag(content="*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}")
            pg.wait_for_timeout(250)
            for y in range(0, 6000, 700):
                pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(15)
            pg.evaluate("window.scrollTo(0,0)")
            if omode == "letters":
                pg.evaluate(f"({LETTERS_JS})({pct / 100})")
            else:
                pg.evaluate(f"document.documentElement.style.fontSize = '{pct}%'")
            pg.wait_for_timeout(300)
            if kind == "menu":
                for y in range(0, 2600, 400):      # scroll down so the bottom bar slides in, as it does for a real visitor
                    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(40)
                pg.wait_for_timeout(700)
                pg.evaluate("document.querySelector('.hdr .menu-btn').click()"); pg.wait_for_timeout(300)
                probs = pg.evaluate(MENU_JS)
            else:
                pg.evaluate("document.querySelector('.work-grid a').click()"); pg.wait_for_timeout(500)
                probs = pg.evaluate(VIEWER_JS)
            checked_overlays += 1
            if probs:
                fails.append((f"phone {w}x{h}", f"{pct}% {omode}", kind))
                print(f"FAIL  phone {w}x{h:<4d} {pct}% {omode:8s}{'':6s} {kind:17s} " + " | ".join(probs))
            pg.close()
        ctx.close()
    b.close()
print(f"checked {checked} page and size combinations, and {checked_overlays} open-menu and photo-viewer combinations")
print("\nFAILS", len(fails))
raise SystemExit(1 if fails else 0)

#!/usr/bin/env python3
"""Keeps the phone number and "short-term" in one piece.   (added at Checkpoint 36)

Usage:  python3 tools/nobreak-test.py        Prints FAILS 0 when everything is right.

tools/build-pages.py wraps every "(423) 451-5707" and every "short-term" that sits in the page's text in <span class="nb"> (white-space: nowrap),
so a narrow phone never puts half a phone number on one line and half on the next, and "short-" never ends a line. This checks:
  1. COVERAGE: every phone number and every "short-term" in the visible text of every page is inside a .nb wrapper.
  2. STRUCTURE: a .nb never sits next to other loose text inside a flex or grid parent (there the text and the wrapper would turn into
     two separate cells, which is how "short-term" once dropped into the 24 px icon column of a checklist). Wrap the words in a <span> instead.
  2b. STYLE: a .nb stays a plain run of text: its display is inline (inline-block for the phone number) and its text size equals the text size around it.
     (A rule such as `.card li span{display:block;font-size:.97rem}` also hits a wrapper nested in that span: the wrapper became a block on its own line
     and its text shrank a second time. Found at Checkpoint 36 on the Options page, "How it works", step 2.)
  3. NEVER SPLIT: on every page, at nine screen widths and three text sizes (normal, 150%, 200%), each wrapper stays on one line. The one
     exception is the phone number, which may wrap at its space only when it is wider than the whole block around it (a 320 px phone with
     the text at 150% or more); there it must wrap rather than run off the screen. The contact tiles and the footer link may wrap as before.
  4. The labels on buttons that carry the number read "Call (423) 451-5707" with one normal space and the number whole.
Needs Playwright with Chromium.
"""
import functools, http.server, pathlib, socketserver, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index", "options", "about", "work", "new-homes", "contact", "privacy-policy", "terms-of-service", "404"]
WIDTHS = [320, 360, 375, 390, 412, 600, 768, 1024, 1440]
SIZES = ["", "150%", "200%"]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)
        print("  FAIL ", msg)
    return ok


COVERAGE = """()=>{const bad=[]; const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  while(w.nextNode()){const n=w.currentNode; const p=n.parentElement; if(!p||/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName)) continue;
    const t=n.textContent; if(!/\\(423\\) 451-5707|short-term/i.test(t)) continue; if(p.closest('.nb')) continue;
    bad.push(t.replace(/\\s+/g,' ').trim().slice(0,80));}
  return bad}"""
STRUCTURE = """()=>{const bad=[]; document.querySelectorAll('.nb').forEach(n=>{const p=n.parentElement; const d=getComputedStyle(p).display;
  if(/flex|grid/.test(d)&&[...p.childNodes].some(c=>c!==n&&c.nodeType===3&&c.textContent.trim().length>0)) bad.push(p.tagName.toLowerCase()+'.'+p.className+' | '+(p.textContent||'').replace(/\\s+/g,' ').slice(0,60));});
  return bad}"""
SPLIT = """()=>{const bad=[]; document.querySelectorAll('.nb').forEach(n=>{
  const r=document.createRange(); r.selectNodeContents(n); const rs=[...r.getClientRects()].filter(x=>x.width>0&&x.height>0);
  if(!rs.length) return;                                                       // not on screen (menu closed, bar hidden, and so on)
  const tops=[]; rs.forEach(x=>{if(!tops.some(t=>Math.abs(t-x.top)<x.height*0.6)) tops.push(x.top)});
  if(tops.length<2) return;                                                    // one line: fine
  const ctx=n.textContent+' | '+(n.parentElement.textContent||'').replace(/\\s+/g,' ').slice(0,60);
  if(n.classList.contains('ph')){                                              // the phone number may wrap only when it cannot fit on a line of the block around it
    const sv=['white-space','display'].map(k=>[k,n.style.getPropertyValue(k),n.style.getPropertyPriority(k)]);               // important: the stylesheet's own display rule for a wrapper is !important
    n.style.setProperty('white-space','nowrap','important'); n.style.setProperty('display','inline','important');
    const nat=n.getBoundingClientRect().width; sv.forEach(([k,v,pr])=>{n.style.removeProperty(k); if(v) n.style.setProperty(k,v,pr);});
    let c=n.parentElement; while(c&&getComputedStyle(c).display==='inline') c=c.parentElement;
    const cs=getComputedStyle(c); let avail=c.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    if(/flex/.test(cs.display)){                                               // next to an icon in a row: the icon and the gaps are not room for the number
      const others=[...c.children].filter(x=>x!==n&&!x.contains(n)&&!n.contains(x)); const kin=[...c.children].find(x=>x===n||x.contains(n));
      avail-=others.reduce((s,x)=>s+(x.getClientRects().length?x.getBoundingClientRect().width:0),0)+(parseFloat(cs.columnGap)||0)*(c.children.length-1);
      if(kin&&kin!==n) avail=Math.min(avail,kin.getBoundingClientRect().width);}
    if(nat<=avail+0.5) bad.push('split although it fits ('+Math.round(nat)+'px in '+Math.round(avail)+'px): '+ctx);
    return;}
  if(getComputedStyle(n).whiteSpace==='nowrap') bad.push('split: '+ctx);});    // "short-term" and other nowrap pieces never split (the contact tiles and the footer link may wrap)
  return bad}"""
STYLE = """()=>{const bad=[]; document.querySelectorAll('.nb').forEach(n=>{const cs=getComputedStyle(n); const p=n.parentElement; if(!p||!n.getClientRects().length) return;
  if(n.closest('.ftr-col,.reach')) return;                                        // the contact tiles and the footer link are blocks of their own, by design
  const pd=getComputedStyle(p).display; const flexItem=/flex|grid/.test(pd);       // a flex or grid item is blockified by the browser itself
  const want=n.classList.contains('ph')?'inline-block':'inline'; const ps=parseFloat(getComputedStyle(p).fontSize), ns=parseFloat(cs.fontSize);
  const where=p.tagName.toLowerCase()+'.'+p.className+' | '+(p.textContent||'').replace(/\\s+/g,' ').slice(0,60);
  if(!flexItem && cs.display!==want) bad.push('display is '+cs.display+' (should be '+want+'): '+where);
  if(Math.abs(ps-ns)>0.05) bad.push('text size '+ns+'px, surrounding text '+ps+'px: '+where);
  if(parseFloat(cs.marginTop)||parseFloat(cs.marginBottom)||parseFloat(cs.paddingTop)||parseFloat(cs.paddingBottom)) bad.push('has vertical margin or padding: '+where);});
  return bad}"""
LABELS = """()=>[...document.querySelectorAll('.btn .bl')].map(b=>b.textContent)"""

with sync_playwright() as p:
    b = p.chromium.launch()
    total_nb = 0
    for page in PAGES:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
        pg = ctx.new_page()
        pg.route("**/*", lambda r: r.abort() if not r.request.url.startswith("http://127.0.0.1") else r.continue_())
        pg.goto(f"http://127.0.0.1:{port}/{page}.html", wait_until="load")
        pg.keyboard.press("Shift")
        n = pg.evaluate("document.querySelectorAll('.nb').length")
        total_nb += n
        for t in pg.evaluate(COVERAGE):
            check(False, f"{page}: not wrapped: {t!r}")
        for t in pg.evaluate(STRUCTURE):
            check(False, f"{page}: wrapper sits next to loose text in a flex/grid parent: {t}")
        for vw in (1440, 390):
            pg.set_viewport_size({"width": vw, "height": 900}); pg.wait_for_timeout(60)
            for t in pg.evaluate(STYLE):
                check(False, f"{page} {vw}px: wrapper is not a plain run of text: {t}")
        pg.set_viewport_size({"width": 1440, "height": 900})
        for t in pg.evaluate(LABELS):
            check(" " not in t and t.count("  ") == 0, f"{page}: button label {t!r} has an odd space")
            if "(423)" in t:
                check(t in ("Call (423) 451-5707", "Call or text (423) 451-5707"), f"{page}: unexpected number label {t!r}")
        for w in WIDTHS:
            for size in SIZES:
                pg.set_viewport_size({"width": w, "height": 900})
                pg.evaluate("(s)=>{document.documentElement.style.fontSize=s}", size)
                pg.wait_for_timeout(30)
                for t in pg.evaluate(SPLIT):
                    check(False, f"{page} {w}px text {size or '100%'}: split across lines: {t}")
        ctx.close()
    print(f"checked {len(PAGES)} pages ({total_nb} wrapped phrases): coverage, structure, never split at {len(WIDTHS)} widths x {len(SIZES)} text sizes")
    b.close()
srv.shutdown()
print("FAILS", len(fails))
raise SystemExit(1 if fails else 0)

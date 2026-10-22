#!/usr/bin/env python3
"""Accessibility + layout smoke test for the GLP Home Options site.

What it does (offline, nothing leaves your machine): serves this folder on a throwaway local port, opens each page in
Chromium at desktop (1440), tablet (820) and phone (390, touch) sizes plus a phone with "reduce motion" turned on,
scrolls the whole page so every reveal/lazy image fires, then reports:
  - axe-core violations (WCAG 2.0/2.1/2.2 A + AA and best-practice rules), plus the "needs review" color-contrast items
  - broken images, sideways scrolling, interactive elements smaller than 44px, JS errors
  - the phone menu opened (Home page), re-scanned with axe
Screenshots of each run go to a temp folder that is printed at the top.

Setup (once):   pip install playwright pillow && playwright install chromium && npm i axe-core
Run (from the folder where you ran npm i):   python /path/to/tools/a11y-check.py [page.html ...]
Goal: 0 violations everywhere. Re-run after any big change.
"""
import asyncio, functools, http.server, pathlib, socketserver, sys, tempfile, threading
import _site  # lets the 404 page's /GLP-Home-Options/... addresses work on the local server
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sys.argv[1:] or ["index.html", "options.html", "about.html", "work.html", "new-homes.html", "contact.html", "privacy-policy.html", "terms-of-service.html", "404.html"]
OUT = pathlib.Path(tempfile.mkdtemp(prefix="glp-check-"))
AXE_PATH = pathlib.Path("node_modules/axe-core/axe.min.js")
AXE = AXE_PATH.read_text()
print("screenshots ->", OUT)

class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k):
        pass


handler = functools.partial(_Quiet, directory=str(ROOT))
srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
BASE = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()

CONFIGS = [
    ("desk", dict(viewport={"width": 1440, "height": 900}, is_mobile=False), False),
    ("tablet", dict(viewport={"width": 820, "height": 1180}, is_mobile=False), False),
    ("phone", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True), False),
    ("phone-reduced-motion", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True), True),
]
TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]


async def scroll_all(pg):
    h = await pg.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        await pg.evaluate(f"window.scrollTo(0,{y})")
        await pg.wait_for_timeout(110)
        y += 450
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
    await pg.wait_for_timeout(700)
    await pg.evaluate("window.scrollTo(0,0)")
    await pg.wait_for_timeout(300)


async def axe(pg, label):
    await pg.add_script_tag(content=AXE)
    res = await pg.evaluate("(tags)=>axe.run(document,{runOnly:{type:'tag',values:tags}})", TAGS)
    viol = res["violations"]
    review = [i for i in res["incomplete"] if i["id"] == "color-contrast"]
    print(f"  [{label}] axe: {len(viol)} violation types, {len(res['passes'])} rules passed" +
          (f", {sum(len(i['nodes']) for i in review)} contrast items need a human look" if review else ""))
    for v in viol:
        print("   -", v["id"], v["impact"], len(v["nodes"]), "nodes |", v["help"])
        for n in v["nodes"][:4]:
            print("       ", n["target"], "|", (n.get("failureSummary") or "").replace("\n", " ")[:200])
    return len(viol)


async def main():
    bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for page_name in PAGES:
            for name, opts, reduce in CONFIGS:
                ctx = await b.new_context(device_scale_factor=1, reduced_motion="reduce" if reduce else "no-preference", **opts)
                pg = await ctx.new_page()
                errs = []
                pg.on("pageerror", lambda e: errs.append(str(e)))
                # keep the test hermetic: only our own server (the contact-form embed is blocked on purpose)
                await pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith(BASE) else r.abort())
                await pg.goto(BASE + page_name)
                await pg.wait_for_timeout(700)
                await pg.add_style_tag(content="html{scroll-behavior:auto!important}")
                await scroll_all(pg)
                print(f"== {page_name} @ {name}")
                broken = await pg.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'))")
                if broken: print("  BROKEN IMAGES:", broken); bad += 1
                if await pg.evaluate("document.documentElement.scrollWidth > innerWidth"): print("  SIDEWAYS OVERFLOW"); bad += 1
                small = await pg.evaluate("""() => [...document.querySelectorAll('a, button, summary, input, select, textarea')].filter(e=>{
                    const r=e.getBoundingClientRect(), cs=getComputedStyle(e);
                    return r.width>0 && r.height>0 && cs.visibility!=='hidden' && (r.height<44 || r.width<44)
                      && !e.closest('p, li, dd, .vh, .faq-side') && !e.classList.contains('skip') && !e.closest('[hidden]');
                  }).map(e=>[e.tagName,(e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,28),Math.round(e.getBoundingClientRect().width),Math.round(e.getBoundingClientRect().height)])""")
                if small: print("  small tap targets (<44px):", small[:10])
                if errs: print("  JS ERRORS:", errs); bad += 1
                bad += await axe(pg, "page")
                if name == "phone" and page_name == "index.html":
                    await pg.evaluate("window.scrollTo(0,0)")
                    await pg.click(".menu-btn")
                    await pg.wait_for_timeout(300)
                    await pg.screenshot(path=str(OUT / "phone-menu-open.png"))
                    bad += await axe(pg, "phone menu open")
                    await pg.click(".menu-btn")
                if name in ("desk", "phone") and page_name == "work.html":
                    # the photo viewer: open it, scan it, step with the arrow key, then Esc must close it and hand focus back
                    await pg.evaluate("window.scrollTo(0,0)")
                    first = pg.locator(".work-grid a").first
                    await first.click()
                    await pg.wait_for_timeout(300)
                    await pg.screenshot(path=str(OUT / f"work-viewer-{name}.png"))
                    bad += await axe(pg, "photo viewer open")
                    shown = await pg.evaluate("document.querySelector('.lb-count').textContent")
                    await pg.keyboard.press("ArrowRight")
                    await pg.wait_for_timeout(150)
                    stepped = await pg.evaluate("document.querySelector('.lb-count').textContent")
                    await pg.keyboard.press("Escape")
                    await pg.wait_for_timeout(150)
                    back = await pg.evaluate("document.activeElement === document.querySelector('.work-grid a')")
                    closed = await pg.evaluate("!document.querySelector('.lb').open")
                    print(f"  viewer: opened at '{shown}', arrow key -> '{stepped}', Esc closes: {closed}, focus back on photo: {back}")
                    if shown == stepped or not closed or not back:
                        print("  VIEWER PROBLEM"); bad += 1
                await pg.screenshot(path=str(OUT / f"{page_name.replace('.html','')}-{name}.png"), full_page=True)
                await ctx.close()
        await b.close()
    print("\nRESULT:", "all clear" if bad == 0 else f"{bad} problem(s) above")
    srv.shutdown()


asyncio.run(main())

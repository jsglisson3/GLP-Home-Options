#!/usr/bin/env python3
"""Tests the "page not found" page (404.html) the way GitHub Pages serves it.

Usage:  python3 tools/notfound-test.py
It starts a small server that behaves like GitHub Pages for a project site: files under /GLP-Home-Options/ are served as they are,
/GLP-Home-Options/about also finds about.html, and ANYTHING ELSE under that folder gets the status 404 with the body of 404.html, at any depth.
Then, for several missing addresses (shallow, deep, a missing folder, a mistyped page), in a real browser it checks:
  - the status is 404 and the page is the friendly one (title, headline, noindex, the way to the home page and the phone number);
  - the stylesheet, script, fonts, logo and icons all load from the right place (this is what breaks when links are relative);
  - every link on it leads to a real page (status 200), including the five page links and the call, text and Facebook links being well formed;
  - the header, the page and the phone bar look right (no sideways scroll at 320, 390, 768 and 1440 px, a visible headline, visible icons);
  - clicking "Go to the home page" really lands on the home page;
  - the page runs its script without errors and makes no failed requests.
If SITE in tools/build-pages.py changes to the real domain (BASE "/"), this test follows it. Prints FAILS 0 when everything is right.
"""
import functools, http.server, mimetypes, os, pathlib, re, threading
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = re.search(r'^SITE = "([^"]+)"', (ROOT / "tools" / "build-pages.py").read_text(encoding="utf-8"), re.M).group(1)
BASE = urlsplit(SITE).path or "/"


class GH(http.server.BaseHTTPRequestHandler):
    """A tiny stand-in for GitHub Pages serving a project site at BASE."""

    def log_message(self, *a):
        pass

    def _send(self, status, body, ctype):
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if not path.startswith(BASE):
            return self._send(404, b'Not found (outside the project folder)', 'text/plain')
        rel = path[len(BASE):]
        f = (ROOT / rel).resolve() if rel else ROOT / 'index.html'
        inside = str(f).startswith(str(ROOT))
        if inside and f.is_dir() and (f / 'index.html').is_file():
            f = f / 'index.html'
        elif inside and not f.is_file() and (f.parent / (f.name + '.html')).is_file() and not rel.endswith('/'):
            f = f.parent / (f.name + '.html')            # /about finds about.html, as on GitHub Pages
        if inside and f.is_file():
            ctype = mimetypes.guess_type(str(f))[0] or 'application/octet-stream'
            return self._send(200, f.read_bytes(), ctype + ('; charset=utf-8' if ctype.startswith('text/') or ctype in ('application/javascript',) else ''))
        return self._send(404, (ROOT / '404.html').read_bytes(), 'text/html; charset=utf-8')


srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), GH)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
ORIGIN = f'http://127.0.0.1:{port}'

fails = 0


def check(ok, msg):
    global fails
    if not ok:
        fails += 1
        print('BAD', msg)
    return ok


# every icon the page uses must exist in the page's own icon sprite, and each one that is on screen must have a size
ICONS_JS = """()=>{const hidden=e=>{for(let n=e;n;n=n.parentElement){if(getComputedStyle(n).display==='none')return true}return false};
  return [...document.querySelectorAll('svg use')].filter(u=>(u.getAttribute('href')||'').startsWith('#')).map(u=>{const id=u.getAttribute('href').slice(1); const sv=u.closest('svg'); const s=sv.getBoundingClientRect();
    return [id, !!document.getElementById(id), hidden(sv)||(s.width>0&&s.height>0)]})}"""
MISSING = ['nope', 'nope.html', 'a/b/c/d/missing-page.html', 'css/', 'optoins.html', 'work/old-project', 'images/not-here.jpg']
PAGE_LINKS = ['index.html', 'options.html', 'about.html', 'work.html', 'new-homes.html', 'contact.html']

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
        pg = ctx.new_page()
        errs, failed, bad = [], [], []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'status of 404' not in m.text else None)
        pg.on('requestfailed', lambda r: failed.append(r.url) if r.url.startswith(ORIGIN) and 'ERR_ABORTED' not in (r.failure or '') else None)   # a photo cancelled because we clicked away is not a failure
        pg.on('response', lambda r: bad.append((r.status, r.url)) if r.url.startswith(ORIGIN) and r.status >= 400 and r.request.resource_type != 'document' else None)
        pg.route('**/*', lambda r: r.abort() if not r.request.url.startswith(ORIGIN) else r.continue_())

        for miss in MISSING:
            url = f'{ORIGIN}{BASE}{miss}'
            resp = pg.goto(url, wait_until='load')
            pg.wait_for_timeout(150)
            tag = f'{BASE}{miss}'
            check(resp.status == 404, f'{tag}: status {resp.status}, expected 404')
            info = pg.evaluate("""()=>({title:document.title, h1:document.querySelector('h1').textContent.replace(/\\s+/g,' ').trim(),
                robots:(document.querySelector('meta[name=robots]')||{}).content||'', lang:document.documentElement.lang,
                hdrPos:getComputedStyle(document.querySelector('.hdr')).position, h1Size:parseFloat(getComputedStyle(document.querySelector('h1')).fontSize),
                fontOk:[...document.fonts].some(f=>/Plus Jakarta/.test(f.family)&&f.status==='loaded'),
                css:[...document.styleSheets].some(s=>/css\\/site\\.css/.test(s.href||'')), imgs:[...document.images].map(i=>[i.src.split('/').pop(), i.complete&&i.naturalWidth>0]),
                phone:document.body.innerText.includes('(423) 451-5707'), tel:!!document.querySelector('a[href="tel:+14234515707"]'),
                hasHome:[...document.querySelectorAll('a')].some(a=>/Go to the home page/.test(a.textContent)),
                bodyBg:getComputedStyle(document.body).backgroundColor})""")
            check(info['title'] == 'Page not found | GLP Home Options', f'{tag}: title {info["title"]!r}')
            check(info['h1'].startswith('That page isn’t here.') or info['h1'].startswith("That page isn't here."), f'{tag}: headline {info["h1"]!r}')
            check('noindex' in info['robots'], f'{tag}: robots meta {info["robots"]!r}')
            check(info['css'] and info['hdrPos'] == 'sticky' and info['h1Size'] >= 30, f'{tag}: stylesheet not applied {info}')
            check(info['fontOk'], f'{tag}: the site font did not load')
            check(all(ok for _, ok in info['imgs']) and len(info['imgs']) >= 1, f'{tag}: an image failed {info["imgs"]}')
            check(info['phone'] and info['tel'] and info['hasHome'], f'{tag}: missing the phone number or the way home {info}')
            icons = pg.evaluate(ICONS_JS)
            check(icons and all(ok and vis for _, ok, vis in icons), f'{tag}: an icon is missing or has no size {icons}')
        print(f'checked {len(MISSING)} missing addresses: status 404, friendly page, noindex, css/font/logo/icons load, phone and home link present')

        # ---- the icons that only show on a phone (menu button, call and text bar) have to be there too
        pg.set_viewport_size({'width': 390, 'height': 844})
        pg.goto(f'{ORIGIN}{BASE}nope', wait_until='load')
        icons = pg.evaluate(ICONS_JS)
        check(icons and all(ok and vis for _, ok, vis in icons), f'phone width: an icon is missing or has no size {icons}')
        shown = pg.evaluate("()=>[...document.querySelectorAll('svg use')].filter(u=>u.closest('svg').getBoundingClientRect().width>0).map(u=>u.getAttribute('href'))")
        check({'#i-menu', '#i-phone', '#i-sms'} <= set(shown), f'phone width: expected the menu, phone and text icons on screen, saw {shown}')
        pg.set_viewport_size({'width': 1440, 'height': 900})

        # ---- every link on the page works
        pg.goto(f'{ORIGIN}{BASE}a/b/c/missing.html', wait_until='load')
        links = pg.evaluate("()=>[...document.querySelectorAll('a[href]')].map(a=>[a.getAttribute('href'), a.href, a.textContent.replace(/\\s+/g,' ').trim()])")
        seen = set()
        for raw, absu, text in links:
            if raw.startswith('#'):
                check(pg.evaluate("(id)=>!!document.getElementById(id)", raw[1:]), f'in-page link {raw} has no target')
                continue
            if raw.startswith(('tel:', 'sms:', 'mailto:')):
                check(re.fullmatch(r'(tel|sms):\+1423\d{7}|mailto:[^@\s]+@[^@\s]+', raw) is not None, f'contact link looks wrong: {raw}')
                continue
            if raw.startswith('https://'):
                check(raw.startswith('https://www.facebook.com/'), f'unexpected outside link {raw}')
                continue
            u = urlsplit(absu)
            key = u.path
            if key in seen:
                continue
            seen.add(key)
            r = pg.request.get(f'{ORIGIN}{u.path}')
            check(r.status == 200, f'link "{text}" -> {raw} -> {r.status}')
        for page in PAGE_LINKS:
            check(any(urlsplit(a).path == f'{BASE}{page}' for _, a, _ in links), f'404 page does not link to {page}')
        print(f'checked {len(links)} links on the 404 page (all internal ones return 200, contact links well formed)')

        # ---- no sideways scroll, nothing cut off, at the common widths
        for w in (320, 390, 768, 1440):
            pg.set_viewport_size({'width': w, 'height': 900})
            pg.goto(f'{ORIGIN}{BASE}x/y/z', wait_until='load')
            m = pg.evaluate("""()=>{const h=document.querySelector('h1').getBoundingClientRect(); const bs=[...document.querySelectorAll('.phero .btn')].map(e=>e.getBoundingClientRect());
               const nav=document.querySelector('.nf-links'); const nr=nav?nav.getBoundingClientRect():null;
               return {sw:document.documentElement.scrollWidth, iw:innerWidth, h1:[Math.round(h.left),Math.round(h.right)], btns:bs.map(r=>[Math.round(r.left),Math.round(r.right),Math.round(r.height)]),
                       navRight:nr?Math.round(nr.right):null, navLinks:nav?[...nav.querySelectorAll('a')].map(a=>Math.round(a.getBoundingClientRect().height)):[]}}""")
            check(m['sw'] <= m['iw'], f'{w}px: sideways scroll {m}')
            check(m['h1'][0] >= 0 and m['h1'][1] <= w, f'{w}px: headline leaves the screen {m}')
            check(all(0 <= bt[0] and bt[1] <= w and bt[2] >= 52 for bt in m['btns']), f'{w}px: a button leaves the screen or is under 52px tall {m}')
            check(m['navRight'] is not None and m['navRight'] <= w and all(hh >= 44 for hh in m['navLinks']), f'{w}px: page links {m}')
        pg.set_viewport_size({'width': 1440, 'height': 900})

        # ---- the way home works
        pg.goto(f'{ORIGIN}{BASE}deep/missing/page.html', wait_until='load')
        pg.click('text=Go to the home page')
        pg.wait_for_load_state('load')
        check(urlsplit(pg.url).path == f'{BASE}index.html' and 'GLP Home Options' in pg.title() and 'Page not found' not in pg.title(), f'"Go to the home page" landed on {pg.url} ({pg.title()})')
        pg.goto(f'{ORIGIN}{BASE}deep/missing/page.html', wait_until='load')
        pg.click('.nf-links a[href$="options.html"]')
        pg.wait_for_load_state('load')
        check(urlsplit(pg.url).path == f'{BASE}options.html', f'Your options link landed on {pg.url}')

        # ---- the real pages still work when served the same way (the extensionless address too), and the 404 file itself is reachable
        check(pg.request.get(f'{ORIGIN}{BASE}about').status == 200, '/about should find about.html')
        check(pg.request.get(f'{ORIGIN}{BASE}404.html').status == 200, '404.html should be reachable directly')
        check(pg.request.get(f'{ORIGIN}{BASE}').status == 200, 'the folder address should serve the home page')

        print('page errors:', errs, '| failed local requests:', failed, '| local 4xx/5xx sub-requests:', bad)
        check(not errs, f'page errors {errs}')
        check(not failed, f'failed requests {failed}')
        check(not [x for x in bad if not x[1].endswith('not-here.jpg')], f'sub-requests that failed {bad}')
        b.close()
finally:
    srv.shutdown()
print('FAILS', fails)
raise SystemExit(1 if fails else 0)

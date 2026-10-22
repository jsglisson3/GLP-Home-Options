#!/usr/bin/env python3
"""How tall is a page, section by section, and how many words does it have?

Usage:  python3 tools/page-size.py options        (page name without .html; default options)
Prints total height, the word count of <main>, and each section's height at 1440 px (laptop) and 390 px (phone).
Use it before and after trimming a page.
"""
import sys, threading, http.server, functools, os, json
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
h=functools.partial(Q,directory=ROOT)
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),h)
port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
page_name=sys.argv[1] if len(sys.argv)>1 else 'options'
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,touch) in [(1440,False),(390,True)]:
        ctx=b.new_context(viewport={'width':w,'height':900},has_touch=touch,is_mobile=touch,reduced_motion='reduce')
        pg=ctx.new_page()
        pg.route('**/*',lambda r: r.abort() if not r.request.url.startswith('http://127.0.0.1') else r.continue_())
        pg.goto(f'http://127.0.0.1:{port}/{page_name}.html',wait_until='load')
        pg.keyboard.press('Shift')
        res=pg.evaluate('''()=>{
          const out=[];
          document.querySelectorAll('main > section, main > div > section, body > section, section').forEach(s=>{
            const r=s.getBoundingClientRect();
            const id=s.id||s.className.split(' ').slice(0,2).join('.');
            if(out.find(o=>o.id===id && o.h===Math.round(r.height))) return;
            out.push({id, h:Math.round(r.height)});
          });
          const words=(document.querySelector('main')||document.body).innerText.trim().split(/\\s+/).length;
          return {total:document.documentElement.scrollHeight, words, sections:out};
        }''')
        print(w, json.dumps(res))
        ctx.close()
    b.close()
srv.shutdown()

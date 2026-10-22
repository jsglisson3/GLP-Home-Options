#!/usr/bin/env python3
"""Tests the seller net sheet (Home page) in a real browser against an independent calculation.

Usage:  python3 tools/netsheet-test.py
It opens the cost fields, types four sets of numbers (the defaults, zero costs, negative equity, and a case where selling
direct nets more) and checks every \"You keep\" total to the dollar. Run it after ANY change to calc() in js/site.js or to the
net sheet markup. Prints FAILS 0 when everything matches. Needs Playwright with Chromium.
"""
import threading, http.server, functools, json, re
from playwright.sync_api import sync_playwright
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=ROOT))
port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()

def ref(payoff,price,comm,close,repairs,carry,months,offer):
    commAmt=price*comm/100; closeAmt=price*close/100; carryAmt=carry*months
    netList=price-payoff-commAmt-closeAmt-repairs-carryAmt
    netDirect=offer-payoff
    return round(netList),round(netDirect)

def money(t):
    t=t.replace('−','-').replace('$','').replace(',','')
    return int(t)

cases=[
 dict(payoff=150000,price=300000,comm=6,close=2.5,repairs=8000,carry=1800,months=2.5,offer=255000),
 dict(payoff=0,price=250000,comm=5,close=2,repairs=0,carry=0,months=0,offer=200000),
 dict(payoff=220000,price=240000,comm=6,close=3,repairs=15000,carry=2100,months=3,offer=190000),
 dict(payoff=90000,price=180000,comm=6,close=2.5,repairs=4000,carry=900,months=1.5,offer=170000),
]
fails=0
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
    pg=ctx.new_page()
    errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.route('**/*',lambda r: r.abort() if not r.request.url.startswith('http://127.0.0.1') else r.continue_())
    pg.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load')
    pg.keyboard.press('Shift')
    pg.click('details.costs-more summary')
    # defaults
    d=pg.evaluate("()=>({list:document.getElementById('r-netlist').textContent,direct:document.getElementById('r-netdirect').textContent,verdict:document.getElementById('verdict').textContent,sub:document.getElementById('verdict-sub').textContent})")
    print('defaults',d)
    for c in cases:
        for k,v in c.items():
            pg.fill('#'+{'payoff':'payoff','price':'price','comm':'comm','close':'close','repairs':'repairs','carry':'carry','months':'months','offer':'offer'}[k],str(v))
        pg.dispatch_event('#offer','input')
        r=pg.evaluate("()=>({list:document.getElementById('r-netlist').textContent,direct:document.getElementById('r-netdirect').textContent,verdict:document.getElementById('verdict').textContent})")
        el,ed=ref(**c)
        gl,gd=money(r['list']),money(r['direct'])
        ok=(gl==el and gd==ed)
        fails+= (not ok)
        print('OK ' if ok else 'BAD',c,'->',r,'expected',el,ed)
    print('page errors (a blocked outside request is expected):',errs)
    # details open/close works and inputs are inside the form
    print(pg.evaluate("()=>({inForm:document.querySelectorAll('#calc input').length, details:!!document.querySelector('#calc details.costs-more'), open:document.querySelector('details.costs-more').open})"))
    b.close()
srv.shutdown()
print('FAILS',fails)

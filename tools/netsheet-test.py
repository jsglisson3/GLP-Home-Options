#!/usr/bin/env python3
"""Tests the seller net sheet (Home page) in a real browser against an independent calculation.

Usage:  python3 tools/netsheet-test.py
It opens the cost fields, types sets of numbers and checks, to the dollar:
  1. every "You keep" total (four fixed cases, then 150 random ones, computed in exactly the same order as the page);
  2. the break-even line ("a cash offer above $X keeps more in your pocket than listing"): it matches the independent number,
     it does not change when the cash offer or the mortgage changes, it is hidden when it would be meaningless (no price, costs above
     the price), and, the real proof, typing that very number in as the cash offer makes the two "You keep" totals equal,
     $600 above it makes selling direct win by $600, and $600 below it makes listing win by $600;
  3. "Print my numbers": the button sets up the print layout, fills in the list of typed numbers and the date, and cleans up after
     itself; the printed page (a real PDF made by Chromium, with background colors OFF the way printers default) is ONE page on Letter and
     on A4, shows the sheets, the answer and the way to reach us, and shows none of the rest of the page.
Run it after ANY change to calc() in js/site.js, to the net sheet markup, or to the print rules. Prints FAILS 0 when everything matches.
Needs Playwright with Chromium, and pdftotext/pdfinfo (poppler) for the printed-page checks.
"""
import functools, http.server, math, os, random, re, subprocess, tempfile, threading
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

fails = 0


def check(ok, msg):
    global fails
    if not ok:
        fails += 1
        print('BAD', msg)
    return ok


def usd(v):
    """Same as usd() in js/site.js."""
    return ('−$' if v < 0 else '$') + format(int(math.floor(abs(v) + 0.5)), ',')


def calc(payoff, price, comm, close, repairs, carry, months, offer):
    """The page's own arithmetic, in the same order, so even the floating-point rounding matches."""
    c, k = comm / 100, close / 100
    comm_amt, close_amt, carry_amt = price * c, price * k, carry * months
    net_list = price - payoff - comm_amt - close_amt - repairs - carry_amt
    net_direct = offer - payoff
    be = price - comm_amt - close_amt - repairs - carry_amt
    return net_list, net_direct, be


def money(t):
    return int(t.replace('−', '-').replace('$', '').replace(',', ''))


FIELDS = ['payoff', 'price', 'comm', 'close', 'repairs', 'carry', 'months', 'offer']
cases = [
    dict(payoff=150000, price=300000, comm=6, close=2.5, repairs=8000, carry=1800, months=2.5, offer=255000),
    dict(payoff=0, price=250000, comm=5, close=2, repairs=0, carry=0, months=0, offer=200000),
    dict(payoff=220000, price=240000, comm=6, close=3, repairs=15000, carry=2100, months=3, offer=190000),
    dict(payoff=90000, price=180000, comm=6, close=2.5, repairs=4000, carry=900, months=1.5, offer=170000),
]
rnd = random.Random(36)
random_cases = []
for _ in range(150):
    price = rnd.randrange(60, 900) * 1000                  # a multiple of 1,000, so every cost is a whole dollar
    random_cases.append(dict(
        payoff=rnd.randrange(0, int(price * 0.95) // 1000) * 1000, price=price,
        comm=rnd.choice([0, 1, 2, 3, 4, 4.5, 5, 5.5, 6, 7]), close=rnd.choice([0, 1, 1.5, 2, 2.5, 3, 4]),
        repairs=rnd.randrange(0, 40) * 500, carry=rnd.randrange(0, 40) * 100, months=rnd.choice([0, 1, 1.5, 2, 2.5, 3, 4, 6]),
        offer=rnd.randrange(40, int(price / 1000) + 20) * 1000))


def fill_all(pg, c):
    for k in FIELDS:
        pg.fill('#' + k, str(c[k]))
    pg.dispatch_event('#offer', 'input')


def read(pg):
    return pg.evaluate("""()=>{const g=id=>document.getElementById(id);
      return {list:g('r-netlist').textContent, direct:g('r-netdirect').textContent, verdict:g('verdict').textContent,
              be:g('breakeven').textContent, beHidden:g('breakeven').hidden,
              beVisible:g('breakeven').getClientRects().length>0, beStrong:(g('breakeven').querySelector('strong')||{}).textContent||''}}""")


def pdf_check(pg, label, paper):
    """Make the printed page the way a printer driver does and look at the PDF."""
    pdf = os.path.join(tempfile.mkdtemp(), f'sheet-{paper}.pdf')
    m = '0.75in' if paper == 'Letter 0.75in margins' else '0.5in'
    kw = dict(path=pdf, print_background=False, prefer_css_page_size=False, margin=dict(top=m, bottom=m, left=m, right=m))
    kw['format'] = 'A4' if paper == 'A4' else 'Letter'
    pg.pdf(**kw)
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    text = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout)
    check(pages == 1, f'{label} {paper}: printed page count {pages}, expected 1')
    return pdf, text


try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.route('**/*', lambda r: r.abort() if not r.request.url.startswith('http://127.0.0.1') else r.continue_())
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        pg.keyboard.press('Shift')
        pg.click('details.costs-more summary')

        # ---- the defaults the page opens with
        d = read(pg)
        print('defaults', d)
        nl, nd, be = calc(**cases[0])
        check(money(d['list']) == round(nl) and money(d['direct']) == round(nd), f'defaults totals {d}')
        check(not d['beHidden'] and d['beVisible'] and d['beStrong'] == usd(be), f'default break-even shows {usd(be)}: {d}')
        check(d['be'] == f'On these numbers, a cash offer above {usd(be)} keeps more in your pocket than listing.', f'default break-even wording: {d["be"]!r}')

        # ---- 1 + 2. totals and break-even, fixed cases then random ones
        n = 0
        for c in cases + random_cases:
            fill_all(pg, c)
            r = read(pg)
            nl, nd, be = calc(**c)
            ok = (r['list'] == usd(nl)) and (r['direct'] == usd(nd))
            check(ok, f'totals {c} -> {r["list"]}/{r["direct"]} expected {usd(nl)}/{usd(nd)}')
            show = c['price'] > 0 and be > 0 and be <= c['price']
            if show:
                check(not r['beHidden'] and r['beVisible'] and r['beStrong'] == usd(be), f'break-even {c} -> {r} expected {usd(be)}')
            else:
                check(r['beHidden'] and not r['beVisible'] and r['be'] == '', f'break-even should be hidden {c} -> {r}')
            n += 1
        print(f'checked {n} cases (4 fixed + {len(random_cases)} random): totals and break-even line')

        # ---- the proof: the break-even number is the cash offer where the two sides meet
        meet = 0
        for c in cases + random_cases[:60]:
            nl, nd, be = calc(**c)
            if not (c['price'] > 0 and 0 < be <= c['price']):
                continue
            c2 = dict(c, offer=int(round(be)))
            fill_all(pg, c2)
            r = read(pg)
            check(r['list'] == r['direct'], f'offer = break-even should tie: {c2} -> {r["list"]} vs {r["direct"]}')
            check(r['verdict'].startswith('About the same'), f'offer = break-even should say about the same: {r["verdict"]!r}')
            fill_all(pg, dict(c, offer=int(round(be)) + 600))
            r = read(pg)
            check('selling direct' in r['verdict'] and '$600' in r['verdict'], f'$600 above break-even should favor selling direct by $600: {r["verdict"]!r} {c}')
            fill_all(pg, dict(c, offer=int(round(be)) - 600))
            r = read(pg)
            check('by listing' in r['verdict'] and '$600' in r['verdict'], f'$600 below break-even should favor listing by $600: {r["verdict"]!r} {c}')
            meet += 1
        print(f'checked {meet} cases: break-even offer ties, +$600 wins direct by $600, -$600 wins listing by $600')

        # ---- the break-even number ignores the cash offer and the mortgage (it cannot depend on them)
        base = dict(cases[0])
        fill_all(pg, base)
        want = read(pg)['beStrong']
        for o, m in [(1, 0), (100000, 250000), (999999, 12345), (0, 0)]:
            fill_all(pg, dict(base, offer=o, payoff=m))
            check(read(pg)['beStrong'] == want, f'break-even moved when offer={o} payoff={m}')

        # ---- hidden when it would mean nothing
        for label, c in [
            ('no sale price', dict(base, price=0)),
            ('costs above the price', dict(base, repairs=400000)),
            ('negative repairs push it above the price', dict(base, repairs=-50000)),
            ('empty price', None),
        ]:
            if c is None:
                fill_all(pg, base); pg.fill('#price', ''); pg.dispatch_event('#price', 'input')
            else:
                fill_all(pg, c)
            r = read(pg)
            check(r['beHidden'] and not r['beVisible'] and r['be'] == '', f'break-even should be hidden for {label}: {r}')
        fill_all(pg, base)
        check(not read(pg)['beHidden'], 'break-even comes back after the numbers are sensible again')

        # ---- 3. Print my numbers: the button, the list of typed numbers, the date, the clean-up
        info = pg.evaluate("""()=>{const b=document.getElementById('print-sheet');
          return {exists:!!b, text:b&&b.textContent.trim(), type:b&&b.type, shown:b&&b.getClientRects().length>0,
                  inForm:!!(b&&b.closest('#calc')), rows:document.querySelectorAll('#p-inputs div').length,
                  printOnlyShown:[...document.querySelectorAll('.print-only')].filter(e=>e.getClientRects().length>0).length}}""")
        print('print button', info)
        check(info['exists'] and info['text'] == 'Print my numbers' and info['type'] == 'button' and info['shown'], f'print button: {info}')
        check(not info['inForm'], 'print button must not sit inside the form')
        check(info['rows'] == 8, f'8 typed-number rows ready at load, found {info["rows"]}')
        check(info['printOnlyShown'] == 0, f'print-only blocks must be hidden on screen, {info["printOnlyShown"]} showing')
        pg.evaluate("()=>{window.__printed=0; window.print=function(){window.__printed++}}")
        fill_all(pg, dict(base))
        pg.click('#print-sheet')
        st = pg.evaluate("""()=>({printed:window.__printed, cls:document.documentElement.classList.contains('print-sheet'),
              date:document.getElementById('p-date').textContent,
              rows:[...document.querySelectorAll('#p-inputs div')].map(d=>d.querySelector('dt').textContent+'='+d.querySelector('dd').textContent)})""")
        print('after click', st)
        check(st['printed'] == 1 and st['cls'], f'click should call print once and set the layout class: {st}')
        check(re.fullmatch(r'[A-Z][a-z]+ \d{1,2}, \d{4}', st['date']) is not None, f'date text: {st["date"]!r}')
        want_rows = ['Still owed on the mortgage=$150,000', 'What it might sell for if listed=$300,000', 'Cash offer compared=$255,000',
                     'Agent commission=6%', 'Seller closing costs=2.5%', 'Repairs and prep=$8,000', 'Monthly cost while listed=$1,800', 'Months to sell=2.5']
        check(st['rows'] == want_rows, f'typed-number rows {st["rows"]}')
        # the numbers in the list follow the typing
        pg.evaluate("()=>document.documentElement.classList.remove('print-sheet')")
        pg.fill('#price', '412000'); pg.dispatch_event('#price', 'input')
        rows = pg.evaluate("()=>[...document.querySelectorAll('#p-inputs dd')].map(d=>d.textContent)")
        check(rows[1] == '$412,000', f'typed-number list should follow typing, got {rows}')
        fill_all(pg, dict(base))

        # screen view with the print class on and the screen media: nothing changes (all print rules are inside @media print)
        pg.evaluate("()=>document.documentElement.classList.add('print-sheet')")
        scr = pg.evaluate("()=>({hdr:getComputedStyle(document.querySelector('.hdr')).display, calc:getComputedStyle(document.getElementById('calc')).display, po:getComputedStyle(document.querySelector('.print-only')).display})")
        check(scr['hdr'] != 'none' and scr['calc'] != 'none' and scr['po'] == 'none', f'print class must not change the screen view: {scr}')
        pg.evaluate("()=>window.dispatchEvent(new Event('afterprint'))")
        check(pg.evaluate("()=>!document.documentElement.classList.contains('print-sheet')"), 'afterprint should remove the layout class')

        # ---- the printed pages themselves (real Chromium PDF, background colors off)
        for paper in ('Letter', 'A4', 'Letter 0.75in margins'):
            pg.evaluate("()=>{document.documentElement.classList.add('print-sheet')}")
            for label, c in [('default', cases[0]), ('listing wins big', cases[2]), ('direct wins', cases[3]),
                             ('big numbers', dict(payoff=1250000, price=3400000, comm=6, close=2.5, repairs=125000, carry=9800, months=6, offer=2900000))]:
                fill_all(pg, c)
                pg.evaluate("()=>{document.documentElement.classList.add('print-sheet'); document.getElementById('p-date').textContent='October 22, 2026'}")
                pdf, text = pdf_check(pg, label, paper)
                nl, nd, be = calc(**c)
                for need in ['GLP Home Options', 'Seller net sheet', 'What would you actually', 'walk away with', 'If you list', 'If you sell to us',
                             'You keep', usd(nl), usd(nd), usd(c['price']), usd(c['offer']), usd(c['payoff']),
                             'Estimates for information only', '(423) 451-5707', 'info@glphomeoptions.com', 'PO Box 55, Hixson, TN', 'October 22, 2026',
                             'Still owed on the mortgage', 'Months to sell']:
                    check(need in text, f'{label} {paper}: printed page is missing {need!r}')
                if 0 < be <= c['price']:
                    check(f'cash offer above {usd(be)}' in text, f'{label} {paper}: printed page is missing the break-even line')
                for banned in ['Skip to', 'Get my options', 'Go over these numbers', 'Print my numbers', 'Terms of Service', 'Privacy Policy',
                               'Frequently', 'Change the costs we assumed', 'Example figures', 'Try your own numbers', 'Call or text us', 'Ask a question']:
                    check(banned not in text, f'{label} {paper}: printed page should not show {banned!r}')
                if label == 'default' and paper == 'Letter':
                    keep = os.environ.get('NETSHEET_PDF_OUT')
                    if keep:
                        os.replace(pdf, keep)
            pg.evaluate("()=>{document.documentElement.classList.remove('print-sheet')}")
        print('printed page: one page on Letter (0.5in and 0.75in margins) and A4 for 4 different sheets; has the sheets, answer and contact line; nothing else from the page')

        # colors in the printed view: the answer box must be dark text on white, never white-on-white
        pg.emulate_media(media='print')
        pg.evaluate("()=>document.documentElement.classList.add('print-sheet')")
        col = pg.evaluate("""()=>{const out={};
          const cs=(sel)=>{const e=document.querySelector(sel); return e?getComputedStyle(e):null};
          for(const sel of ['.verdict','.verdict .big','.verdict .big span','.verdict-sub, #verdict-sub','.verdict .breakeven','.verdict .breakeven strong','.sheet dt','.sheet dd','.sheet h4','.print-inputs dd','.netsheet-head h2','.print-contact']){
            const s=cs(sel); if(!s) { out[sel]='missing'; continue; } out[sel]=[s.color,s.backgroundColor,s.display];}
          return out}""")
        print('print colors', col)
        def lum(c):
            m = re.match(r'rgba?\((\d+), (\d+), (\d+)', c)
            return (int(m.group(1)) * 299 + int(m.group(2)) * 587 + int(m.group(3)) * 114) / 1000 if m else None
        for sel, v in col.items():
            if v == 'missing':
                check(False, f'print colors: {sel} not found'); continue
            color, bg, disp = v
            check(disp != 'none', f'print: {sel} is hidden')
            check(lum(color) is not None and lum(color) < 110, f'print: {sel} text color {color} is too light for white paper')
            check(bg in ('rgba(0, 0, 0, 0)', 'rgb(255, 255, 255)'), f'print: {sel} background {bg} would not print reliably')
        hidden = pg.evaluate("""()=>['.hdr','.mobile-bar','.ftr','#calc','.res-actions','#paths','#story','#how','#faq','#contact','.pano','#about','#building','.hero','.netsheet-head .lede']
              .map(s=>[s, document.querySelector(s)? getComputedStyle(document.querySelector(s)).display : 'missing'])""")
        for s, disp in hidden:
            check(disp == 'none', f'print: {s} should be hidden in the printed net sheet, display={disp}')
        # without the class, the normal page still prints the way it did before (only header and mobile bar hidden), and the print-only bits stay off
        pg.evaluate("()=>document.documentElement.classList.remove('print-sheet')")
        plain = pg.evaluate("""()=>({po:[...document.querySelectorAll('.print-only')].map(e=>getComputedStyle(e).display),
              faq:getComputedStyle(document.querySelector('#faq')).display, ftr:getComputedStyle(document.querySelector('.ftr')).display,
              hdr:getComputedStyle(document.querySelector('.hdr')).display, calc:getComputedStyle(document.getElementById('calc')).display})""")
        check(all(x == 'none' for x in plain['po']) and plain['faq'] != 'none' and plain['ftr'] != 'none' and plain['hdr'] == 'none' and plain['calc'] != 'none',
              f'plain page print (Ctrl+P on the whole page) should be unchanged: {plain}')
        pg.emulate_media(media='screen')

        # ---- screen layout of the new line and the two buttons, no sideways scroll
        for w in (1440, 1024, 768, 390, 320):
            pg.set_viewport_size({'width': w, 'height': 900})
            fill_all(pg, cases[0])
            m = pg.evaluate("""()=>{const r=e=>e.getBoundingClientRect(), a=document.querySelector('.res-actions'), bs=[...a.querySelectorAll('.btn')].map(r),
               be=document.getElementById('breakeven'), v=document.querySelector('.verdict'), vr=r(v), br=r(be);
               return {sw:document.documentElement.scrollWidth, iw:innerWidth, btns:bs.map(x=>[Math.round(x.left),Math.round(x.right),Math.round(x.top),Math.round(x.height)]),
                       ar:[Math.round(r(a).left),Math.round(r(a).right)], beInside:br.left>=vr.left-0.5&&br.right<=vr.right+0.5, beSW:be.scrollWidth<=be.clientWidth+1,
                       h:bs.map(x=>x.height)}}""")
            check(m['sw'] <= m['iw'], f'{w}px: sideways scroll {m}')
            check(m['beInside'] and m['beSW'], f'{w}px: break-even line spills out of the answer box {m}')
            check(all(x >= 52 for x in m['h']), f'{w}px: buttons shorter than 52px {m["h"]}')
            check(all(bt[0] >= m['ar'][0] - 0.5 and bt[1] <= m['ar'][1] + 0.5 for bt in m['btns']), f'{w}px: a button leaves its row {m}')
            print(w, m['btns'])
        pg.set_viewport_size({'width': 1440, 'height': 900})

        # ---- keyboard: the button is reachable and says what it does
        nm = pg.evaluate("()=>{const b=document.getElementById('print-sheet'); return {tab:b.tabIndex, name:b.textContent.trim()}}")
        check(nm['tab'] == 0 and nm['name'] == 'Print my numbers', f'print button accessibility {nm}')

        print('page errors (a blocked outside request is expected):', errs)
        # no JavaScript: the print button and the break-even line stay out of the way, the rest of the sheet is unchanged
        ctx2 = b.new_context(viewport={'width': 1440, 'height': 900}, java_script_enabled=False)
        p2 = ctx2.new_page()
        p2.route('**/*', lambda r: r.abort() if not r.request.url.startswith('http://127.0.0.1') else r.continue_())
        p2.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        shown = p2.locator('#print-sheet').is_visible()
        be_shown = p2.locator('#breakeven').is_visible()
        check(not shown, 'without JavaScript the print button should not show')
        check(not be_shown, 'without JavaScript the empty break-even line should not show')
        b.close()
finally:
    srv.shutdown()
print('FAILS', fails)
raise SystemExit(1 if fails else 0)

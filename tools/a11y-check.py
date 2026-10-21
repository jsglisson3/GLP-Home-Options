import asyncio, json, sys, tempfile, pathlib
# Usage: pip install playwright && playwright install chromium && npm i axe-core   (run from the folder that has node_modules)
# Then: python tools/a11y-check.py   -> scans phone + desktop, light + dark, prints violations, saves screenshots to a temp folder
from playwright.async_api import async_playwright
SITE=(pathlib.Path(__file__).resolve().parents[1]/'index.html').as_uri()
OUT=tempfile.mkdtemp(prefix='glp-check-')+'/'
print('screenshots ->',OUT)
AXE=open('node_modules/axe-core/axe.min.js').read()
async def scroll_all(pg):
    h = await pg.evaluate('document.documentElement.scrollHeight')
    y=0
    while y<h:
        await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(120); y+=500
    await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(300)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vp, mobile, scheme in [('desk-light',{'width':1366,'height':900},False,'light'),('phone-light',{'width':390,'height':844},True,'light'),('phone-dark',{'width':390,'height':844},True,'dark'),('desk-dark',{'width':1366,'height':900},False,'dark')]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile, color_scheme=scheme)
            pg = await ctx.new_page()
            errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.route('**/*', lambda r: r.abort() if not r.request.url.startswith('file:') else r.continue_())
            await pg.goto(SITE); await pg.wait_for_timeout(500)
            await scroll_all(pg)
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"); await pg.wait_for_timeout(900)
            print('  broken images:', await pg.evaluate('[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute("src"))'))
            await pg.add_script_tag(content=AXE)
            res = await pg.evaluate('axe.run(document, {runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21a","wcag21aa","wcag22aa","best-practice"]}})')
            viol = res['violations']
            print(f'== {name}: {len(viol)} violation types, {len(res["passes"])} rules passed, js errors {errs}')
            for v in viol:
                print('  -', v['id'], v['impact'], len(v['nodes']), 'nodes |', v['help'])
                for n in v['nodes'][:3]:
                    print('      ', n['target'], '|', (n.get('failureSummary') or '').replace('\n',' ')[:170])
            # tap-target audit for interactive elements (<44px high or wide), visible only
            small = await pg.evaluate('''() => [...document.querySelectorAll('a, button, summary, input, select, textarea')].filter(e=>{const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); return r.width>0 && r.height>0 && cs.visibility!=='hidden' && (r.height<44 || r.width<44) && !e.closest('p, li.assure, .vh') && !e.classList.contains('skip')}).map(e=>[e.tagName, (e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,30), Math.round(e.getBoundingClientRect().width), Math.round(e.getBoundingClientRect().height)])''')
            print('  small targets:', small[:12])
            ow = await pg.evaluate('document.documentElement.scrollWidth > innerWidth')
            print('  horizontal overflow:', ow)
            await pg.screenshot(path=OUT+f'{name}.png', full_page=True)
            await ctx.close()
        await b.close()
asyncio.run(main())

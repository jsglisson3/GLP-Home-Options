#!/usr/bin/env python3
"""Renders tools/og-card.html to images/og-card.jpg (1200x630).

Needs: pip install playwright pillow  (and a Chromium for Playwright). Serves the project folder on a throwaway local port so fonts load.
    python3 tools/make-og.py
"""
import asyncio, http.server, socketserver, threading, pathlib, functools
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k):
        pass


handler = functools.partial(_Quiet, directory=str(ROOT))
srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        await pg.goto(f"http://127.0.0.1:{port}/tools/og-card.html")
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path="/tmp/og-card.png")
        await b.close()
asyncio.run(main())
Image.open("/tmp/og-card.png").convert("RGB").save(ROOT / "images" / "og-card.jpg", quality=88, optimize=True, progressive=True)
print("wrote images/og-card.jpg")
srv.shutdown()

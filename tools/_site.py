"""Shared by the test tools (import it for its side effect):  import _site

The 404 page (404.html) links to its styles, script, fonts and pictures with root-absolute addresses such as
/GLP-Home-Options/css/site.css, so that it still works when GitHub Pages shows it for a missing address several folders deep.
The tools serve the site folder at the top of a small local server, so those addresses would not be found.
This makes the server treat an address that starts with the site's base folder (read from SITE in tools/build-pages.py;
"/GLP-Home-Options/" on the preview address, "/" on the real domain, where nothing needs to change) as the same file at the top.
tools/notfound-test.py does the stricter job of serving the site exactly like GitHub Pages does.
"""
import http.server
import pathlib
import re
from urllib.parse import urlsplit

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SITE = re.search(r'^SITE = "([^"]+)"', (_ROOT / "tools" / "build-pages.py").read_text(encoding="utf-8"), re.M).group(1)
BASE = urlsplit(_SITE).path or "/"

if BASE != "/" and not getattr(http.server.SimpleHTTPRequestHandler, "_glp_base", False):
    _orig = http.server.SimpleHTTPRequestHandler.translate_path

    def _translate(self, path):
        if path.startswith(BASE):
            path = "/" + path[len(BASE):]
        return _orig(self, path)

    http.server.SimpleHTTPRequestHandler.translate_path = _translate
    http.server.SimpleHTTPRequestHandler._glp_base = True

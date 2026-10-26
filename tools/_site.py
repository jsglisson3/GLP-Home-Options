"""Shared by the test tools (import it for its side effect):  import _site

The 404 page (404.html) links to its styles, script, fonts and pictures with root-absolute addresses such as
/GLP-Home-Options/css/site.css, so that it still works when GitHub Pages shows it for a missing address several folders deep.
The tools serve the site folder at the top of a small local server, so those addresses would not be found.
This makes the server treat an address that starts with the site's base folder (read from SITE in tools/build-pages.py;
"/GLP-Home-Options/" on the preview address, "/" on the real domain, where nothing needs to change) as the same file at the top.
tools/notfound-test.py does the stricter job of serving the site exactly like GitHub Pages does.
"""
import http.server
import os
import pathlib
import re
from urllib.parse import urlsplit

_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SRC = (_ROOT / "tools" / "build-pages.py").read_text(encoding="utf-8")
# The builder's launch switch (LIVE = False: preview on github.io; True: the real domain). GLP_BUILD=live or =preview is how tools/seo-check.py tests both builds.
LIVE = re.search(r"^LIVE = (True|False)", _SRC, re.M).group(1) == "True"
if os.environ.get("GLP_BUILD") in ("live", "preview"):
    LIVE = os.environ["GLP_BUILD"] == "live"
SITE = (re.search(r'^REAL = "([^"]+)"', _SRC, re.M).group(1) + "/") if LIVE else re.search(r'^PREVIEW = "([^"]+)"', _SRC, re.M).group(1)
BASE = urlsplit(SITE).path or "/"

# The pages the tools test. They are DISCOVERED in the site folder, so a new page is tested without anyone remembering to add it to eleven lists.
_ORDER = ["index", "options", "about", "work", "new-homes", "contact", "privacy-policy", "terms-of-service", "404"]   # the usual order; later pages follow A to Z


def page_slugs(root=None, include_404=True):
    """Every real page in a site folder (default: this project), as slugs such as "index" and "new-homes".
    A redirect stub (calculator.html in a launch build) is not a page and is left out."""
    folder = pathlib.Path(root) if root else _ROOT
    found = set()
    for p in folder.glob("*.html"):
        if 'http-equiv="refresh"' not in p.read_text(encoding="utf-8", errors="replace")[:3000]:
            found.add(p.stem)
    slugs = [x for x in _ORDER if x in found] + sorted(x for x in found if x not in _ORDER)
    return slugs if include_404 else [x for x in slugs if x != "404"]


def page_files(root=None, include_404=True):
    """The same pages as file names ("index.html")."""
    return [x + ".html" for x in page_slugs(root, include_404)]


if BASE != "/" and not getattr(http.server.SimpleHTTPRequestHandler, "_glp_base", False):
    _orig = http.server.SimpleHTTPRequestHandler.translate_path

    def _translate(self, path):
        if path.startswith(BASE):
            path = "/" + path[len(BASE):]
        return _orig(self, path)

    http.server.SimpleHTTPRequestHandler.translate_path = _translate
    http.server.SimpleHTTPRequestHandler._glp_base = True

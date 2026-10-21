#!/usr/bin/env python3
"""Checks every page for broken internal links, missing in-page anchors, missing images/styles/scripts, and duplicate ids.

    python3 tools/check-links.py

Offline and instant. Run it after tools/build-pages.py. Exits with an error if anything is wrong.
(External links such as Facebook and the GoHighLevel form are not fetched.)
"""
import pathlib
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted(p for p in ROOT.glob("*.html"))


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.dupes, self.links, self.assets = set(), [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                self.dupes.append(a["id"])
            self.ids.add(a["id"])
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        if tag in ("img", "script", "source") and a.get("src"):
            self.assets.append(a["src"])
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "preload"):
            self.assets.append(a["href"])


scans = {}
for p in PAGES:
    s = Scan()
    s.feed(p.read_text(encoding="utf-8"))
    scans[p.name] = s

problems = []
total = 0
for name, s in scans.items():
    for d in s.dupes:
        problems.append(f"{name}: duplicate id '{d}'")
    for href in s.links:
        total += 1
        if href.startswith(("tel:", "mailto:", "sms:", "javascript:")):
            continue
        u = urlsplit(href)
        if u.scheme in ("http", "https"):
            continue
        target = name if not u.path else u.path
        t = scans.get(target)
        if t is None:
            problems.append(f"{name}: link to missing page '{href}'")
            continue
        if u.fragment and u.fragment != "top" and unquote(u.fragment) not in t.ids:
            problems.append(f"{name}: '{href}' points at an id that doesn't exist on {target}")
    for src in s.assets:
        u = urlsplit(src)
        if u.scheme in ("http", "https", "data") or not u.path:
            continue
        if not (ROOT / unquote(u.path)).exists():
            problems.append(f"{name}: missing file '{src}'")

print(f"checked {len(PAGES)} pages, {total} links")
if problems:
    print("\n".join("  - " + p for p in problems))
    sys.exit(1)
print("all internal links, anchors, images and scripts resolve; no duplicate ids")

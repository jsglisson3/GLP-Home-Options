#!/usr/bin/env python3
"""Is the review path safe? Checks the real review facts, then proves the review page and the "What homeowners say" band in a throwaway copy.

    python3 tools/reviews-check.py            about a minute; changes nothing in this folder
    python3 tools/reviews-check.py --keep     also leaves the throwaway copy and prints where it is (open its pages, or run the browser tools on it:
                                              python3 tools/mobile-audit.py   from inside that folder)

1. THE FACTS (tools/reviews_data.py, empty today). They must break no rule; a rating that was last read off the listing more than 35 days ago is a
   warning and more than 62 days ago is a failure (re-read the two numbers on the listing and change CHECKED).
2. THE SAVED PAGES AGREE WITH THE FACTS. With no Google review link on file there is no review.html and no "What homeowners say" band on any page;
   with one, there is. (A build cannot disagree with the facts, but a hand-copied page can.)
3. THE DEMO. A copy of the site is built with obviously fake facts (the demo data never touches this folder, and the builder has no demo switch, so fake
   reviews can never be published). In the demo:
   - review.html exists in the preview and the launch build, is kept out of search in both (noindex, no canonical), is not in sitemap.xml,
     sends everyone to the same Google link, and offers Facebook and a phone call for people with no Google account
   - Home and About show the band: the average and count, the "As of" month, the link to every review, a labeled selection of quotes, no stars,
     no review or rating data for search engines
   - tools/seo-check.py, tools/check-links.py and tools/notfound-test.py pass on the demo
   - tools/claims-check.py FAILS on the demo until a line in tools/claims-allow.txt allows it (so showing real numbers always needs a human "yes")
   - each rule in tools/reviews_data.py really refuses what it should (a link that is not Google's, an average that is not on the listing's scale,
     a quote without permission, an owner's or relative's review, a quote that is too long, and so on)
   - the page builder stops, with a clear message, when the facts break a rule
Prints FAILS 0 when everything is right.
"""
import datetime
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import reviews_data as REV  # noqa: E402

fails = []
warns = []


def check(ok, msg):
    if not ok:
        fails.append(msg)
    print(("  ok    " if ok else "  FAIL  ") + msg)


def warn(msg):
    warns.append(msg)
    print("  WARN  " + msg)


def demo_module_source():
    """The real tools/reviews_data.py with its facts replaced by obviously fake ones, so the rules checked are the real rules."""
    src = (TOOLS / "reviews_data.py").read_text(encoding="utf-8")
    fakes = {
        "GOOGLE_REVIEW_URL": '"https://g.page/r/DEMO-ONLY-NOT-A-REAL-LINK/review"',
        "GOOGLE_PROFILE_URL": '"https://www.google.com/maps/place/DEMO-ONLY-NOT-A-REAL-LISTING"',
        "GOOGLE_RATING": "4.8",
        "GOOGLE_COUNT": "12",
        "CHECKED": '"2026-01-15"',
    }
    for name, val in fakes.items():
        src, n = re.subn(rf"^{name} = .*$", f"{name} = {val}", src, count=1, flags=re.M)
        assert n == 1, name
    quotes = '''QUOTES = [
    dict(text="DEMO ONLY, NOT A REAL REVIEW. They explained every option and never pushed.", source="Google", month="2026-01",
         name="Demo A.", place="Demoville", permission="demo", insider=False),
    dict(text="DEMO ONLY, NOT A REAL REVIEW. A plain, honest conversation about the house.", source="Google", month="2025-12",
         name="", place="", permission="demo", insider=False),
    dict(text="DEMO ONLY, NOT A REAL NOTE. Thank you for the time you took with us.", source="Direct", month="2025-11",
         name="Demo B.", place="", permission="demo written yes", insider=False),
]'''
    src, n = re.subn(r"^QUOTES = \[\]$", quotes, src, count=1, flags=re.M)
    assert n == 1
    return src


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas, self.links, self.hrefs, self.text, self.ids, self.ld = {}, [], [], [], set(), []
        self._ld = False
        self._buf = ""
        self.title = ""
        self._t = False
        self.anchors = []   # (href, attrs)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "meta" and (a.get("name") or a.get("property")):
            self.metas.setdefault(a.get("name") or a.get("property"), a.get("content", ""))
        elif tag == "link" and a.get("rel"):
            self.links.append((a["rel"], a.get("href", "")))
        elif tag == "a" and a.get("href") is not None:
            self.hrefs.append(a["href"])
            self.anchors.append((a["href"], a))
        elif tag == "title":
            self._t = True
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._ld, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False
        elif tag == "script" and self._ld:
            self._ld = False
            self.ld.append(self._buf)

    def handle_data(self, data):
        if self._t:
            self.title += data
        elif self._ld:
            self._buf += data
        else:
            self.text.append(data)


def scan(path):
    s = Scan()
    s.feed(pathlib.Path(path).read_text(encoding="utf-8"))
    return s


def run(cmd, cwd, env=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=dict(os.environ, **(env or {})))


def make_tree(mode_files=True):
    """A scratch copy of the site's sources with the demo facts. Returns the folder."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="glp-reviews-demo-"))
    for d in ("tools", "css", "js", "images", "fonts"):
        shutil.copytree(ROOT / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
    (tmp / "tools" / "reviews_data.py").write_text(demo_module_source(), encoding="utf-8")
    return tmp


# ----------------------------------------------------------------------------------------------------------------------------- 1. the facts
def facts_checks():
    print("1. The real facts (tools/reviews_data.py)")
    probs = REV.problems()
    check(not probs, "the facts break no rule" + ("" if not probs else ": " + "; ".join(probs)))
    empty = not (REV.GOOGLE_REVIEW_URL or REV.GOOGLE_PROFILE_URL or REV.GOOGLE_RATING is not None or REV.QUOTES)
    if empty:
        print("  note  EMPTY, as it should be today: nothing about reviews is shown anywhere")
        return empty
    if REV.CHECKED:
        try:
            age = (datetime.date.today() - datetime.date.fromisoformat(REV.CHECKED)).days
        except ValueError:
            age = None
        if age is not None:
            check(age >= 0, f"CHECKED is not in the future ({REV.CHECKED})")
            check(age <= 62, f"the rating and count were read off the listing {age} days ago (more than 62 is too old to show; read them again and change CHECKED)")
            if 35 < age <= 62:
                warn(f"the rating and count were read off the listing {age} days ago; read them again soon and change CHECKED")
    return empty


# ----------------------------------------------------------------------------------------------------------------------------- 2. saved pages
def saved_checks():
    print("2. The saved pages agree with the facts")
    review = ROOT / "review.html"
    check(review.exists() == bool(REV.GOOGLE_REVIEW_URL),
          f"review.html is {'present' if review.exists() else 'absent'}, and there {'is' if REV.GOOGLE_REVIEW_URL else 'is no'} Google review link on file")
    nums = REV.shown_numbers() if not REV.problems() else None
    wants_band = bool(nums) or any(q.get("source") == "Direct" for q in REV.QUOTES)
    for name in ("index.html", "about.html"):
        p = ROOT / name
        s = scan(p)
        check(("reviews" in s.ids) == wants_band, f"{name}: the \"What homeowners say\" band is {'there' if 'reviews' in s.ids else 'absent'}, as the facts say")
    for p in sorted(ROOT.glob("*.html")):
        s = scan(p)
        for raw in s.ld:
            bad = [k for k in ("AggregateRating", "ratingValue", "reviewCount", '"Review"', "starRating") if k in raw]
            check(not bad, f"{p.name}: no review or rating data for search engines ({', '.join(bad) or 'none'})")


# ----------------------------------------------------------------------------------------------------------------------------- 3. demo
def rule_checks():
    """Each rule really refuses what it should: set one bad fact at a time on the real module and see problems() complain."""
    print("3a. Each rule refuses what it should")
    good = dict(GOOGLE_REVIEW_URL="https://g.page/r/DEMO-ONLY-NOT-A-REAL-LINK/review", GOOGLE_PROFILE_URL="https://www.google.com/maps/place/DEMO-ONLY",
                GOOGLE_RATING=4.8, GOOGLE_COUNT=12, CHECKED="2026-01-15", MIN_SHOWN=5, QUOTES=[])
    q = dict(text="Demo quote.", source="Google", month="2026-01", name="", place="", permission="demo", insider=False)
    saved = {k: getattr(REV, k) for k in good}

    def problems_with(**over):
        for k, v in {**good, **over}.items():
            setattr(REV, k, v)
        try:
            return REV.problems()
        finally:
            for k, v in saved.items():
                setattr(REV, k, v)

    check(problems_with() == [], "a complete, plausible set of demo facts breaks no rule")
    bad = {
        "a review link that is not on Google": dict(GOOGLE_REVIEW_URL="https://example.com/review-us-now-please"),
        "a review link without https": dict(GOOGLE_REVIEW_URL="http://g.page/r/DEMO-ONLY-NOT-A-REAL-LINK/review"),
        "a rating with no count": dict(GOOGLE_COUNT=None),
        "a count with no rating": dict(GOOGLE_RATING=None),
        "an average above 5": dict(GOOGLE_RATING=5.5),
        "an average rounded to two decimals": dict(GOOGLE_RATING=4.85),
        "a count of zero": dict(GOOGLE_COUNT=0),
        "no date for when the numbers were read": dict(CHECKED=""),
        "a date that is not a date": dict(CHECKED="2026-13-45"),
        "a rating without a listing to read the reviews on": dict(GOOGLE_PROFILE_URL=""),
        "a quote with no permission on record": dict(QUOTES=[{**q, "permission": ""}]),
        "a quote by an owner, relative or employee": dict(QUOTES=[{**q, "insider": True}]),
        "a quote with no insider answer at all": dict(QUOTES=[{k: v for k, v in q.items() if k != "insider"}]),
        "a quote from a source that does not exist": dict(QUOTES=[{**q, "source": "Yelp"}]),
        "a quote with no month": dict(QUOTES=[{**q, "month": ""}]),
        "a quote that is far too long": dict(QUOTES=[{**q, "text": "word " * 120}]),
        "a quote with markup in it": dict(QUOTES=[{**q, "text": "<b>Great</b>"}]),
        "an empty quote": dict(QUOTES=[{**q, "text": "  "}]),
        "more Google quotes than Google reviews": dict(GOOGLE_COUNT=1, GOOGLE_RATING=5.0, QUOTES=[q, q]),
        "a Google quote with no count of reviews": dict(GOOGLE_RATING=None, GOOGLE_COUNT=None, CHECKED="", QUOTES=[q]),
        "a made-up key on a quote": dict(QUOTES=[{**q, "stars": 5}]),
        "a minimum of zero": dict(MIN_SHOWN=0),
    }
    for what, over in bad.items():
        p = problems_with(**over)
        check(bool(p), f"refused: {what}")


def demo_checks(keep):
    print("3b. The demo build (fake facts, in a throwaway copy)")
    tree = make_tree()
    try:
        results = {}
        for mode in ("preview", "live"):
            r = run([sys.executable, "tools/build-pages.py"], tree, {"GLP_BUILD": mode})
            check(r.returncode == 0, f"the demo builds as {mode}" + ("" if r.returncode == 0 else "\n" + r.stdout[-600:] + r.stderr[-600:]))
            if r.returncode != 0:
                return
            snap = pathlib.Path(tempfile.mkdtemp(prefix=f"glp-reviews-{mode}-"))
            for f in tree.glob("*"):
                if f.is_file():
                    shutil.copy(f, snap / f.name)
            results[mode] = snap
        pre, live = results["preview"], results["live"]
        try:
            for mode, folder in results.items():
                rv = folder / "review.html"
                check(rv.exists(), f"{mode}: review.html is built")
                if not rv.exists():
                    continue
                s = scan(rv)
                robots = s.metas.get("robots", "")
                check("noindex" in robots, f"{mode}: review.html says noindex ({robots!r})")
                check(not [h for r_, h in s.links if r_ == "canonical"], f"{mode}: review.html names no canonical address")
                check(s.title.strip() == "Share your experience | GLP Home Options" and 15 <= len(s.title.strip()) <= 65, f"{mode}: review.html title is plain ({s.title.strip()!r})")
                desc = s.metas.get("description", "")
                check(60 <= len(desc) <= 160, f"{mode}: review.html description is {len(desc)} characters (60 to 160)")
                demo_link = "https://g.page/r/DEMO-ONLY-NOT-A-REAL-LINK/review"
                mains = [a for h, a in s.anchors if h == demo_link]
                check(len(mains) == 1, f"{mode}: the one Google review button is on the page exactly once ({len(mains)})")
                if mains:
                    a = mains[0]
                    check(a.get("target") == "_blank" and "noopener" in (a.get("rel") or ""), f"{mode}: the review button opens a new tab safely")
                hs = " ".join(s.hrefs)
                check("facebook.com" in hs, f"{mode}: review.html offers Facebook for people with no Google account")
                check(any(h.startswith("tel:") for h in s.hrefs), f"{mode}: review.html offers a phone call")
                text = re.sub(r"\s+", " ", " ".join(s.text)).lower()
                for word in ("5-star", "five star", "five-star", "if you're happy", "if you were happy", "discount", "gift", "reward", "free "):
                    check(word not in text, f"{mode}: review.html never says {word!r}")
                check("never ask anyone to change or take one down" in text and "don't give anything in return" in text.replace("’", "'"),
                      f"{mode}: review.html says nothing is given in return and no one is asked to change or remove a review")
                # the bands
                for name in ("index.html", "about.html"):
                    p = scan(folder / name)
                    check("reviews" in p.ids, f"{mode}: {name} shows the band")
                    t = re.sub(r"\s+", " ", " ".join(p.text))
                    check("4.8 on Google" in t and "from 12 reviews" in t, f"{mode}: {name} says 4.8 on Google, from 12 reviews")
                    check("As of January 2026" in t, f"{mode}: {name} says when the numbers were read")
                    check("A selection: 2 of our 12 Google reviews, quoted exactly." in t.replace("’", "'"), f"{mode}: {name} labels the Google quotes a selection")
                    check("Sent to us" in t and "shared with the writer" in t.replace("’", "'"), f"{mode}: {name} labels the note that was sent to us")
                    check(any(h == "https://www.google.com/maps/place/DEMO-ONLY-NOT-A-REAL-LISTING" for h in p.hrefs), f"{mode}: {name} links to every review on Google")
                    for raw in p.ld:
                        bad = [k for k in ("AggregateRating", "ratingValue", "reviewCount", '"Review"', "starRating") if k in raw]
                        check(not bad, f"{mode}: {name} structured data has no review or rating markup ({', '.join(bad) or 'none'})")
                    if name == "index.html":
                        check(raw_has_same_as(p, "https://www.google.com/maps/place/DEMO-ONLY-NOT-A-REAL-LISTING"),
                              f"{mode}: {name} tells search engines the Google listing is the same business (sameAs)")
            # not in the sitemap
            sm = (live / "sitemap.xml").read_text(encoding="utf-8")
            check("review" not in sm, "live: sitemap.xml does not list the review page")
            # keep it all in one place and run the other tools on the demo tree
            # saved pages in the tree must be the preview build for the other tools
            r = run([sys.executable, "tools/build-pages.py"], tree, {"GLP_BUILD": "preview"})
            check(r.returncode == 0, "the demo preview is rebuilt for the other tools")
            for tool, expect in (("check-links", 0), ("seo-check", 0), ("notfound-test", 0)):
                r = run([sys.executable, f"tools/{tool}.py"], tree, timeout=600)
                last = [x for x in (r.stdout + r.stderr).strip().splitlines() if x.strip()][-1:] or [""]
                check(r.returncode == expect, f"tools/{tool}.py on the demo: exit {r.returncode} ({last[0][:100]})")
            r = run([sys.executable, "tools/claims-check.py"], tree)
            out = r.stdout + r.stderr
            hit_pages = sorted(set(re.findall(r"NEEDS A DECISION \[[^\]]+\] (\S+\.html):", out)))
            check(r.returncode != 0 and {"index.html", "about.html", "review.html"} <= set(hit_pages),
                  f"tools/claims-check.py FAILS on the demo's rating, count and star wording until a human allows them (pages flagged: {', '.join(hit_pages)})")
            allow = tree / "tools" / "claims-allow.txt"
            lines = "".join(f"{pg} | {sub} | demo: a real fact, read off the listing on 2026-01-15 and checked by a person\n" for pg in ("index.html", "about.html")
                            for sub in ("4.8 on google", "from 12 reviews", "of our 12 google reviews"))
            lines += "review.html | tap the stars | instructions to the reviewer; no rating is claimed\n"
            allow.write_text(allow.read_text(encoding="utf-8").rstrip("\n") + "\n" + lines, encoding="utf-8")
            r = run([sys.executable, "tools/claims-check.py"], tree)
            check(r.returncode == 0, "tools/claims-check.py passes once those lines are in tools/claims-allow.txt" + ("" if r.returncode == 0 else "\n" + (r.stdout + r.stderr)[-900:]))
        finally:
            for f in results.values():
                shutil.rmtree(f, ignore_errors=True)
        r = run([sys.executable, "tools/build-pages.py"], tree, {"GLP_BUILD": "preview"})
        # the builder stops when the facts break a rule
        bad_src = (tree / "tools" / "reviews_data.py").read_text(encoding="utf-8").replace("GOOGLE_COUNT = 12", "GOOGLE_COUNT = None")
        (tree / "tools" / "reviews_data.py").write_text(bad_src, encoding="utf-8")
        r = run([sys.executable, "tools/build-pages.py"], tree)
        check(r.returncode != 0 and "GOOGLE_RATING and GOOGLE_COUNT go together" in (r.stdout + r.stderr), "the page builder stops with a clear message when the facts break a rule")
        if keep:
            (tree / "tools" / "reviews_data.py").write_text(demo_module_source(), encoding="utf-8")
            run([sys.executable, "tools/build-pages.py"], tree, {"GLP_BUILD": "preview"})
            print(f"\nDEMO FOLDER KEPT: {tree}\n(delete it when done; it holds fake facts and must never be copied into the project)")
    finally:
        if not keep:
            shutil.rmtree(tree, ignore_errors=True)


def raw_has_same_as(scan_obj, url):
    return any(url in raw and "sameAs" in raw for raw in scan_obj.ld)


def main():
    keep = "--keep" in sys.argv[1:]
    empty = facts_checks()
    saved_checks()
    rule_checks()
    demo_checks(keep)
    print(f"WARNINGS {len(warns)}")
    print("FAILS", len(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

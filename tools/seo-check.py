#!/usr/bin/env python3
"""Is the site ready to be found, in BOTH states: the preview (kept out of search) and the launch build (the real domain)?

    python3 tools/seo-check.py

It never changes the saved pages. It copies the tools, styles, scripts, pictures and fonts into two scratch folders, builds the site once as the
PREVIEW (GLP_BUILD=preview) and once as the LAUNCH build (GLP_BUILD=live; see LIVE at the top of tools/build-pages.py), and checks both.

Every page, both states
  - a language, a title (15 to 65 characters) and a description (60 to 160), both different on every page; exactly one H1; a picture always has an alt attribute
  - structured data: every block is valid JSON, has a type, repeats nothing a visitor cannot see, and carries NO review or rating markup, in JSON-LD or as
    microdata (the site has no real reviews yet, and Google does not show stars for a business's own reviews; see research/launch-checklist.md before ever
    changing this); Home and Contact each carry the business and Home the site name, with one id, the right address, real pictures and, in the FAQ blocks,
    the same answers a visitor reads; the postal address in the markup is the ADDRESS line written once at the top of tools/build-pages.py
  - every page can be reached from the home page by following links, so nothing is an orphan
  - one set of contact details: the phone number, email and address on every page (text, links, share text, structured data) are exactly the ones
    written once at the top of tools/build-pages.py (PHONE, EMAIL, ADDRESS), so the site, the Google listing and every directory can match
  - the robots tags: every robots-style tag on a page is read (robots, googlebot, bingbot), because Google obeys the most restrictive one
PREVIEW build
  - every page, even the legal pages and the page-not-found page, carries exactly one robots tag, noindex, nofollow ; no page names a canonical address ;
    no page names an address on the real domain ; there is no sitemap.xml, robots.txt or CNAME (a CNAME would take the preview address offline)
LAUNCH build
  - no page says noindex, except the page-not-found page and the review page ; the eight pages meant for search are all indexable ; every one names itself
    as canonical, inside the head, on the real domain, and the share tags (og:title, description, image, url and the card type) are all there and agree
  - nothing mentions github.io or the preview account anywhere (pages, sitemap, robots.txt, structured data, styles, scripts), in any capitalisation
  - sitemap.xml lists exactly the pages that may be searched, each one a real file ; robots.txt allows everything and names the sitemap ; CNAME is the domain ;
    _redirects holds exactly the old-address moves and nothing else (a catch-all to the home page would look like a soft 404 to Google)
  - links, anchors, pictures, styles and scripts all resolve (tools/check-links.py run on the launch build)
The saved pages in this folder must match a fresh build of whichever state LIVE says they are in.
Prints FAILS 0 when everything is right.

    python3 tools/seo-check.py --launch

The same checks, plus the ones that must pass on launch day but are open on purpose today: the launch build may not still carry the visible
"Draft for review" note on a page that can be searched (the two legal pages, until a Tennessee attorney has read them; research/launch-checklist.md,
decision 7). Today it prints FAILS 2 for that reason, and that is the right answer.

What this check cannot know: whether REAL (the domain, with or without www) is the one Jeremy and Joey chose; it is read from the builder, so look at the
line it prints. Where a real host behaves differently from the files (GitHub Pages, Cloudflare Pages), only a visit after launch can tell.
"""
import html
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import _site  # noqa: E402,F401  (the launch switch as the tools see it)
import reviews_data as REV  # noqa: E402  (the Google hosts a review or listing link may use)

TITLE_MIN, TITLE_MAX = 15, 65
DESC_MIN, DESC_MAX = 60, 160
# Markup that would claim reviews or ratings. The site has none, and a business's own reviews earn no stars in Google anyway.
FORBIDDEN_LD = {"AggregateRating", "Review", "Rating", "ReviewRating", "starRating", "reviewCount", "ratingValue", "ratingCount", "bestRating",
                "aggregateRating", "review", "reviews", "reviewBody", "itemReviewed"}
# The pages meant to be found. A launch build must make every one of them indexable, name it in the sitemap and keep it out of the noindex set; the only
# pages allowed to stay out of search are the page-not-found page and the review page. Written here on purpose, not read from the builder's own flags.
MUST_BE_SEARCHABLE = {"index.html", "options.html", "about.html", "work.html", "new-homes.html", "contact.html", "privacy-policy.html", "terms-of-service.html"}
MAY_STAY_OUT = {"404.html", "review.html"}
SHARE_PAGES = MUST_BE_SEARCHABLE - {"privacy-policy.html", "terms-of-service.html"}   # these carry a full share card; the two legal pages carry none, and need none
ROBOTS_NAMES = ("robots", "googlebot", "googlebot-news", "bingbot")
PHONE_RX = re.compile(r"(?<![\d$,.])(?:\+?1[\s.-]?)?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-](\d{4})(?!\d)")   # (423) 451-5707, 423-451-5707, 423.451.5707 ...
EMAIL_RX = re.compile(r"[A-Za-z0-9._+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)
    print(("  ok    " if ok else "  FAIL  ") + msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.lang, self.h1, self.metas, self.links = "", None, 0, {}, []
        self.imgs_no_alt, self.ld, self.hrefs, self.text = 0, [], [], []
        self.refresh, self.ids = None, set()
        self.robots_all, self.in_head, self.canon_outside_head, self.microdata, self.icon_sizes = [], False, 0, 0, []
        self._in_title = self._in_ld = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if any(k in a for k in ("itemscope", "itemtype", "itemprop", "typeof", "vocab")):
            self.microdata += 1
        if tag == "head":
            self.in_head = True
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.metas.setdefault(key, a.get("content", ""))
                if key.lower() in ROBOTS_NAMES:
                    self.robots_all.append((key.lower(), a.get("content", "").lower()))
            if (a.get("http-equiv") or "").lower() == "refresh":
                self.refresh = a.get("content", "")
        elif tag == "link" and a.get("rel"):
            self.links.append((a["rel"], a.get("href", "")))
            if a["rel"] == "canonical" and not self.in_head:
                self.canon_outside_head += 1
            if a["rel"] == "icon":
                self.icon_sizes.append(a.get("sizes", ""))
        elif tag == "img" and "alt" not in a:
            self.imgs_no_alt += 1
        elif tag == "a" and a.get("href") is not None:
            self.hrefs.append(a["href"])
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            self.ld.append(self._buf)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_ld:
            self._buf += data
        else:
            self.text.append(data)

    def canonical(self):
        return [h for r, h in self.links if r == "canonical"]

    def robots(self):
        """Every robots-style tag, joined: when tags disagree Google applies the most restrictive, so one noindex anywhere counts."""
        return " ".join(c for _, c in self.robots_all)


def build(mode):
    """Build the site in a scratch folder as 'preview' or 'live'; return the folder."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"glp-seo-{mode}-"))
    for d in ("tools", "css", "js", "images", "fonts"):
        shutil.copytree(ROOT / d, tmp / d, ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
    r = subprocess.run([sys.executable, str(tmp / "tools" / "build-pages.py")], cwd=tmp, capture_output=True, text=True, timeout=120,
                       env=dict(os.environ, GLP_BUILD=mode))
    if r.returncode != 0:
        print("  the page builder stopped with an error:\n" + (r.stderr or r.stdout))
        sys.exit(1)
    return tmp


def load(folder):
    """(pages, stubs): the real pages, and the small redirect pages a launch build adds for old addresses."""
    pages, stubs = {}, {}
    for p in sorted(folder.glob("*.html")):
        s = Page()
        s.feed(p.read_text(encoding="utf-8"))
        (stubs if s.refresh is not None else pages)[p.name] = s
    return pages, stubs


def builder_module(folder):
    spec = importlib.util.spec_from_file_location("build_pages_scratch", folder / "tools" / "build-pages.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ld_types(obj):
    """Every @type and every key anywhere inside a structured-data block."""
    types, keys = set(), set()

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                keys.add(k)
                if k == "@type":
                    types.update(v if isinstance(v, list) else [v])
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return types, keys


def strings(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k != "@context":   # the vocabulary address is not an address of the site
                yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)
    elif isinstance(obj, str):
        yield obj


def norm(t):
    """Text as a reader sees it: entities decoded, curly quotes and dashes flattened, every kind of space one space."""
    t = html.unescape(t)
    for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u2013", "-"), ("\u2014", "-"), ("\u00a0", " "), ("\u202f", " "), ("\u2060", "")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def flat(t):
    """Text with every space removed, to compare wording without caring how a link or a line break was spaced."""
    return re.sub(r"\s+", "", norm(t))


def common(pages, label, utility=()):
    print(f"{label}: every page")
    titles, descs = {}, {}
    for name, s in pages.items():
        t = html.unescape(s.title).strip()
        d = html.unescape(s.metas.get("description", "")).strip()
        titles.setdefault(t, []).append(name)
        descs.setdefault(d, []).append(name)
        check(s.lang == "en", f"{name}: <html lang=\"en\"> ({s.lang})")
        check(TITLE_MIN <= len(t) <= TITLE_MAX, f"{name}: title is {len(t)} characters (want {TITLE_MIN} to {TITLE_MAX})")
        check(DESC_MIN <= len(d) <= DESC_MAX, f"{name}: description is {len(d)} characters (want {DESC_MIN} to {DESC_MAX})")
        check(s.h1 == 1, f"{name}: exactly one H1 ({s.h1})")
        check(s.imgs_no_alt == 0, f"{name}: every picture has an alt attribute ({s.imgs_no_alt} without)")
        check(s.microdata == 0, f"{name}: no microdata or RDFa (the site's structured data is JSON-LD only; {s.microdata} found)")
        check(any(z in s.icon_sizes for z in ("48x48", "96x96", "144x144", "192x192")),
              f"{name}: a favicon whose size is a multiple of 48 px is linked, which is what Google asks for ({s.icon_sizes})")
        check("width=device-width" in s.metas.get("viewport", ""), f"{name}: viewport tag")
        visible = re.sub(r"\s+", " ", html.unescape(" ".join(s.text))).strip()
        for i, raw in enumerate(s.ld):
            try:
                obj = json.loads(raw)
            except ValueError as e:
                check(False, f"{name}: structured data block {i + 1} is not valid JSON ({e})")
                continue
            types, keys = ld_types(obj)
            check(obj.get("@context") == "https://schema.org" and types, f"{name}: structured data block {i + 1} has a context and a type ({', '.join(sorted(types))})")
            bad = (types | keys) & FORBIDDEN_LD
            check(not bad, f"{name}: structured data {i + 1} has no review or rating markup ({', '.join(sorted(bad)) or 'none'})")
            if "FAQPage" in types:   # a question and its answer in the markup must be on the page for a visitor to read
                missing = [q["name"] for q in obj["mainEntity"] if norm(q["name"]) not in norm(visible)]
                check(not missing, f"{name}: every FAQ question in the markup is also on the page ({len(obj['mainEntity'])} questions; missing: {missing[:2]})")
                page_flat = flat(visible).replace("(opensinanewtab)", "")   # spaces vary around links; the hidden "(opens in a new tab)" is not part of the answer
                off = [q["name"] for q in obj["mainEntity"] if flat(q["acceptedAnswer"]["text"]) not in page_flat]
                check(not off, f"{name}: every FAQ answer in the markup is also on the page word for word ({len(obj['mainEntity'])} answers; different: {off[:2]})")
    for t, names in titles.items():
        check(len(names) == 1, f"title used once: {t[:50]!r} ({', '.join(names)})")
    for d, names in descs.items():
        check(len(names) == 1, f"description used once: {d[:50]!r} ({', '.join(names)})")
    # every page reachable from the home page
    seen, todo = {"index.html"}, ["index.html"]
    while todo:
        cur = todo.pop()
        for h in pages[cur].hrefs:
            h = urldefrag(h)[0]
            if h in pages and h not in seen:
                seen.add(h)
                todo.append(h)
    orphans = sorted(n for n in pages if n not in seen and n not in utility)   # utility pages (page not found, the review page) are pointed to, never linked
    check(not orphans, f"every page can be reached from the home page by links (orphans: {orphans})")


def nap_checks(pages, label, bp):
    """Name, address, phone: the same everywhere a visitor, a crawler or a structured-data reader can see them."""
    print(f"{label}: one set of contact details")
    want_phone = re.sub(r"\D", "", bp.PHONE_TEL)[-10:]
    for name, s in pages.items():
        visible = html.unescape(" ".join(s.text))
        shown = visible + " " + html.unescape(s.metas.get("description", "") + " " + s.metas.get("og:description", ""))
        found = {"".join(m.groups()) for m in PHONE_RX.finditer(shown)}
        linked = {re.sub(r"\D", "", h)[-10:] for h in s.hrefs if h.startswith(("tel:", "sms:"))}
        check(found == {want_phone}, f"{name}: every phone number written on the page is {bp.PHONE} ({sorted(found)})")
        check(linked == {want_phone}, f"{name}: every call and text link goes to {bp.PHONE} ({sorted(linked)})")
        emails = set(EMAIL_RX.findall(shown)) | {h[len('mailto:'):].split('?')[0] for h in s.hrefs if h.startswith("mailto:")}
        check(emails == {bp.EMAIL}, f"{name}: every email on the page is {bp.EMAIL} ({sorted(emails)})")
        check(bp.ADDRESS in re.sub(r"\s+", " ", visible), f"{name}: the address line reads {bp.ADDRESS!r}")
        for i, raw in enumerate(s.ld):
            obj = json.loads(raw)
            if obj.get("@type") == "LocalBusiness":
                check(obj.get("telephone") == bp.PHONE_LD, f"{name}: structured data phone is {bp.PHONE_LD} ({obj.get('telephone')})")
                check(obj.get("email") == bp.EMAIL, f"{name}: structured data email is {bp.EMAIL} ({obj.get('email')})")
                check(obj.get("name") == "GLP Home Options", f"{name}: structured data name is GLP Home Options ({obj.get('name')})")


def ld_checks(pages, label, bp, site, own_url, folder):
    """The business, the site name, the breadcrumb and the pictures in the structured data: present, on the right address, true to ADDRESS."""
    print(f"{label}: structured data names the right business, address and pictures")
    ids = set()
    for name, s in pages.items():
        by_type = {}
        for raw in s.ld:
            try:
                o = json.loads(raw)
            except ValueError:
                continue
            by_type.setdefault(o.get("@type"), []).append(o)
        if name in ("index.html", "contact.html"):
            check(len(by_type.get("LocalBusiness", [])) == 1, f"{name}: one LocalBusiness block ({len(by_type.get('LocalBusiness', []))})")
        if name == "index.html":
            check(len(by_type.get("WebSite", [])) == 1, f"{name}: one WebSite block, which gives Google the site's name ({len(by_type.get('WebSite', []))})")
        for o in by_type.get("LocalBusiness", []):
            ids.add(o.get("@id"))
            check(o.get("@id") == site + "#business", f"{name}: the business id is {site}#business ({o.get('@id')})")
            check(o.get("url") == site, f"{name}: the business address is {site} ({o.get('url')})")
            for k in ("image", "logo"):
                v = o.get(k, "")
                check(v.startswith(site + "images/") and (folder / v[len(site):]).is_file(), f"{name}: the business {k} is a real picture on this site ({v})")
            a = o.get("address", {})
            first = f"PO Box {a['postOfficeBoxNumber']}" if "postOfficeBoxNumber" in a else a.get("streetAddress", "")
            line = ", ".join(x for x in (first, a.get("addressLocality", ""), (a.get("addressRegion", "") + " " + a.get("postalCode", "")).strip()) if x)
            check(line == bp.ADDRESS, f"{name}: the postal address in the markup is the ADDRESS line {bp.ADDRESS!r} ({line!r})")
        for o in by_type.get("WebSite", []):
            check(o.get("@id") == site + "#website" and o.get("url") == site, f"{name}: the site-name block names {site} ({o.get('url')})")
            check(o.get("publisher", {}).get("@id") == site + "#business", f"{name}: the site belongs to the business ({o.get('publisher')})")
        for o in by_type.get("BreadcrumbList", []):
            items = o.get("itemListElement", [])
            check(len(items) == 2 and items[0].get("item") == site, f"{name}: the breadcrumb starts at {site}")
            check(len(items) == 2 and items[-1].get("item") == own_url(name), f"{name}: the breadcrumb ends at the page's own address {own_url(name)} ({items[-1].get('item') if items else None})")
    check(len(ids) <= 1, f"every page names the business with the same id ({sorted(map(str, ids))})")


def preview_checks(folder, pages, launch_files):
    print("PREVIEW build: kept out of search")
    for name, s in pages.items():
        check(s.robots_all == [("robots", "noindex, nofollow")], f"{name}: exactly one robots tag, noindex, nofollow ({s.robots_all})")
        check(not s.canonical(), f"{name}: no canonical address yet ({s.canonical()})")
        found = re.findall(r"(?i)(?:https?:)?//(?:www\.)?glphomeoptions\.com\S{0,30}", (folder / name).read_text(encoding="utf-8"))
        check(not found, f"{name}: names no address on the real domain, which is not live yet ({found[:2]})")
    for f in launch_files:
        check(not (folder / f).exists(), f"no {f} in a preview build")


def live_checks(folder, pages, stubs, real, redirects, utility=(), launch=False):
    print("LAUNCH build: the real domain")
    domain = urlsplit(real).netloc
    check(re.fullmatch(r"https://[a-z0-9-]+(\.[a-z0-9-]+)+", real) is not None, f"REAL is https, lower case, no trailing slash ({real}); it is the address everything below follows, so check it is the one chosen")
    check(set(utility) <= MAY_STAY_OUT, f"only the page-not-found page and the review page are kept out of search (kept out: {sorted(utility)})")
    check(MUST_BE_SEARCHABLE <= set(pages) - set(utility), f"all {len(MUST_BE_SEARCHABLE)} pages meant for search are built and not in the noindex set (missing: {sorted(MUST_BE_SEARCHABLE - (set(pages) - set(utility)))})")
    expected = {}
    for name, s in pages.items():
        robots = s.robots()
        if name in utility:
            check("noindex" in robots, f"{name}: stays out of search ({robots!r})")
            check(not s.canonical(), f"{name}: no canonical")
            continue
        url = real + "/" if name == "index.html" else f"{real}/{name[:-len('.html')]}"   # no .html: the old site's addresses, and what every host serves
        expected[name] = url
        check(not re.search(r"noindex|nofollow|\bnone\b|noarchive|nosnippet", robots), f"{name}: may be indexed, in every robots tag (robots tags: {s.robots_all})")
        check(s.canonical() == [url], f"{name}: canonical is {url} ({s.canonical()})")
        check(s.canon_outside_head == 0, f"{name}: the canonical sits inside the head ({s.canon_outside_head} outside)")
        if name in SHARE_PAGES:
            for k in ("og:title", "og:description", "og:image", "og:url", "og:type", "twitter:card"):
                check(bool(s.metas.get(k)), f"{name}: share tag {k} is there")
        if name in SHARE_PAGES or "og:url" in s.metas:
            check(s.metas.get("og:url") == url, f"{name}: og:url agrees with the canonical ({s.metas.get('og:url')})")
            check(s.metas.get("og:image", "").startswith(real + "/images/"), f"{name}: share picture is on the real domain ({s.metas.get('og:image')})")
            img = folder / urlsplit(s.metas.get("og:image", "")).path.lstrip("/")
            check(img.is_file(), f"{name}: the share picture file exists ({img.name})")
        for i, raw in enumerate(s.ld):
            for v in strings(json.loads(raw)):
                if v.startswith("http"):
                    check(urlsplit(v).netloc in (domain, "www.facebook.com") or urlsplit(v).netloc in REV.GOOGLE_HOSTS,
                          f"{name}: structured data address {v[:60]} is the real domain, Facebook or Google")
                    if urlsplit(v).netloc == domain and v.rstrip("/") != real:
                        path = urlsplit(v).path
                        known = {urlsplit(u).path for u in expected.values()} | {"/"}
                        if path.startswith("/images/"):
                            check((folder / path.lstrip("/")).is_file(), f"{name}: structured data picture {v[:70]} is a real file")
                        else:
                            check(path in known, f"{name}: structured data address {v[:70]} is a real page")
    # old addresses: a stub page for each, and the same move for hosts that can do a real 301
    for old, new in redirects.items():
        st = stubs.get(f"{old}.html")
        check(st is not None, f"/{old} (an old address) has a page that jumps to {new}")
        if st is not None:
            check(st.refresh.replace(" ", "") == f"0;url={new}", f"{old}.html jumps at once to {new} ({st.refresh})")
            check(st.canonical() == [real + "/"], f"{old}.html names the home page as its canonical ({st.canonical()})")
            check("noindex" not in st.robots(), f"{old}.html is not marked noindex ({st.robots_all})")
        path, _, frag = new.partition("#")
        target = pages.get((path.strip("/") or "index") + ".html")
        check(target is not None and (not frag or frag in target.ids), f"{new} is a real place on the site")
    rd = folder / "_redirects"
    check(rd.exists(), "_redirects is written (for hosts that can send a real 301)")
    if rd.exists():
        lines = [" ".join(x.split()) for x in rd.read_text(encoding="utf-8").splitlines() if x.strip()]
        for old, new in redirects.items():
            check(f"/{old} {new} 301" in lines, f"_redirects sends /{old} to {new} with a 301")
        check(sorted(lines) == sorted(f"/{old} {new} 301" for old, new in redirects.items()), f"_redirects holds only the old-address moves, no catch-all ({len(lines)} lines)")
    # nothing of the preview left anywhere
    leaks = []
    for p in sorted(list(folder.iterdir()) + list((folder / "css").glob("*.css")) + list((folder / "js").glob("*.js"))):
        if p.is_file() and p.suffix in (".html", ".xml", ".txt", ".css", ".js", "") and re.search(r"(?i)github\.io|jsglisson3", p.read_text(encoding="utf-8", errors="replace")):
            leaks.append(p.relative_to(folder).as_posix())
    check(not leaks, f"nothing mentions github.io or the preview account, in any capitalisation (found in: {leaks})")
    if launch:   # the part of launch day that is open on purpose today
        print("LAUNCH GATE (--launch): content that must be ready before the switch is flipped")
        for name in sorted(expected):
            shown = norm(" ".join(pages[name].text))
            check("Draft for review" not in shown, f"{name}: no visible \"Draft for review\" note on a page that can be searched (decision 7 in research/launch-checklist.md)")
    # sitemap
    sm = folder / "sitemap.xml"
    check(sm.exists(), "sitemap.xml is written")
    if sm.exists():
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [e.text for e in ET.parse(sm).getroot().findall("s:url/s:loc", ns)]
        check(sorted(locs) == sorted(expected.values()), f"sitemap.xml lists exactly the {len(expected)} pages that may be searched ({len(locs)} listed)")
        check(len(locs) == len(set(locs)), "sitemap.xml lists no page twice")
        check(not ET.parse(sm).getroot().findall("s:url/s:lastmod", ns), "sitemap.xml carries no <lastmod> (a date that is wrong is worse than none)")
        for u in locs:
            path = urlsplit(u).path.lstrip("/")
            f = folder / ((path + ".html") if path else "index.html")
            check(f.is_file(), f"sitemap entry {u} is a real file")
    rb = folder / "robots.txt"
    check(rb.exists(), "robots.txt is written")
    if rb.exists():
        lines = [x.strip() for x in rb.read_text(encoding="utf-8").splitlines() if x.strip() and not x.startswith("#")]
        check("User-agent: *" in lines and "Allow: /" in lines, "robots.txt lets every crawler in")
        check(not any(x.lower().startswith("disallow") and x.split(":", 1)[1].strip() for x in lines), "robots.txt blocks nothing")
        check(f"Sitemap: {real}/sitemap.xml" in lines, "robots.txt names the sitemap")
    cn = folder / "CNAME"
    check(cn.exists() and cn.read_text(encoding="utf-8") == domain + "\n", f"CNAME is {domain}")
    env = dict(os.environ, GLP_BUILD="live")
    r = subprocess.run([sys.executable, str(folder / "tools" / "check-links.py")], cwd=folder, capture_output=True, text=True, env=env, timeout=120)
    check(r.returncode == 0, "links, anchors, pictures, styles and scripts resolve in the launch build" + ("" if r.returncode == 0 else "\n" + r.stdout + r.stderr))


def way_back_check(live_folder, launch_files):
    """The way back (research/launch-checklist.md, section E): a tree that was built as the launch version, rebuilt as the preview, keeps no launch file."""
    print("The way back: a preview rebuild over a launch build")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="glp-seo-back-"))
    try:
        shutil.copytree(live_folder, tmp, dirs_exist_ok=True)
        r = subprocess.run([sys.executable, str(tmp / "tools" / "build-pages.py")], cwd=tmp, capture_output=True, text=True, timeout=120,
                           env=dict(os.environ, GLP_BUILD="preview"))
        check(r.returncode == 0, "the preview rebuild over a launch build runs" + ("" if r.returncode == 0 else "\n" + r.stdout + r.stderr))
        left = [f for f in launch_files if (tmp / f).exists()]
        check(not left, f"after it, no launch file is left behind (left: {left})")
        robots_left = [p.name for p in tmp.glob("*.html") if "noindex" not in p.read_text(encoding="utf-8")]
        check(not robots_left, f"after it, every page is noindex again (not: {robots_left})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def saved_checks(fresh_by_mode, launch_files):
    print("The saved pages in this folder")
    src = (TOOLS / "build-pages.py").read_text(encoding="utf-8")
    m = re.search(r"^LIVE\s*=\s*(\S+)\s*$", src, re.M)
    check(m is not None and m.group(1) in ("True", "False"), f"LIVE is written exactly True or False in tools/build-pages.py ({m.group(1) if m else 'not found'})")
    mode = "live" if m and m.group(1) == "True" else "preview"
    print(f"  LIVE says: {mode}")
    folder = fresh_by_mode[mode]
    for p in sorted(folder.glob("*.html")):
        saved = ROOT / p.name
        ok = saved.exists() and saved.read_bytes().replace(b"\r\n", b"\n") == p.read_bytes()
        check(ok, f"{p.name} matches a fresh {mode} build")
    for f in launch_files:
        check((ROOT / f).exists() == (folder / f).exists(), f"{f} is {'present' if (folder / f).exists() else 'absent'}, as a {mode} build has it")
        if (folder / f).exists() and (ROOT / f).exists():
            check((ROOT / f).read_bytes().replace(b"\r\n", b"\n") == (folder / f).read_bytes(), f"{f} matches a fresh {mode} build")


def main():
    real = re.search(r'^REAL = "([^"]+)"', (TOOLS / "build-pages.py").read_text(encoding="utf-8"), re.M).group(1)
    built = {}
    try:
        for mode in ("preview", "live"):
            built[mode] = build(mode)
        os.environ["GLP_BUILD"] = "live"
        bp = builder_module(built["live"])   # the builder as the launch build ran it: its list of launch files and old addresses
        pv, _ = load(built["preview"])
        lv, stubs = load(built["live"])
        launch = "--launch" in sys.argv
        utility = {p["file"] for p in bp.EXTRA_PAGES + bp.UTILITY_PAGES if p.get("noindex")}   # the 404 page and the review page: noindex, pointed to but never linked
        common(pv, "PREVIEW", utility)
        nap_checks(pv, "PREVIEW", bp)
        ld_checks(pv, "PREVIEW", bp, bp.PREVIEW, lambda n: bp.PREVIEW if n == "index.html" else bp.PREVIEW + n, built["preview"])
        preview_checks(built["preview"], pv, bp.SITE_FILES)
        common(lv, "LAUNCH", utility)
        nap_checks(lv, "LAUNCH", bp)
        ld_checks(lv, "LAUNCH", bp, real + "/", lambda n: real + "/" if n == "index.html" else f"{real}/{n[:-len('.html')]}", built["live"])
        live_checks(built["live"], lv, stubs, real, bp.REDIRECTS, utility, launch)
        way_back_check(built["live"], bp.SITE_FILES)
        saved_checks(built, bp.SITE_FILES)
    finally:
        for f in built.values():
            shutil.rmtree(f, ignore_errors=True)
    print("FAILS", len(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

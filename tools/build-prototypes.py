#!/usr/bin/env python3
"""Build the Session 3 hero prototypes. They are NOT part of the live site.

Reads the generated index.html (run tools/build-pages.py first) and writes two copies of the Home page that differ ONLY in the hero:

  proto-hero-a.html   A, people-led: the live hero with the Session 3 trims (no floating blobs; the photo and the three small
                      facts are held still).
  proto-hero-b.html   B, numbers-led: headline and actions on the left; on the right a side-by-side card of Joey's own listing-vs-
                      direct numbers, with Joey and Ethan as small portraits under it. The stats strip is hidden in B because the
                      card now carries the same numbers.

Both pages add css/proto.css (the warm "cream" surface test and every prototype-only rule), js/proto.js (the Cool/Warm toggle), a
PROTOTYPE bar, and keep `noindex`. Nothing in css/site.css, js/site.js, tools/build-pages.py or tools/pages/ is touched.

The hero wording and the table wording are READ from the live page, so the prototypes cannot drift from it: if the live wording
of one of the five table rows changes, this script stops and says so instead of publishing a stale copy.

Re-run it after any change to the Home page while the prototypes exist:  python3 tools/build-prototypes.py
When the hero is chosen (Session 6) delete: proto-hero-a.html, proto-hero-b.html, css/proto.css, js/proto.js,
images/joey-avatar.jpg, images/ethan-avatar.jpg and this file. (Run tools/checkpoint.py --write afterwards.)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
PROTO_CSS = "css/proto.css?v=1"
PROTO_JS = "js/proto.js?v=1"

# Square crops (left, top, right, bottom) of the two portraits that already sit on the Our story page, saved as small avatars.
AVATARS = {
    "images/joey-avatar.jpg": ("images/joey.jpg", (120, 40, 440, 360)),
    "images/ethan-avatar.jpg": ("images/ethan.jpg", (135, 55, 455, 375)),
}

# The five rows B shows. Wording must equal the live table (checked below); only <strong> is added, to lift the numbers.
ROWS = [
    ("Timeline",
     "45–90+ days", "<strong>45–90+ days</strong>",
     "7–14 days, on your schedule", "<strong>7–14 days</strong>, on your schedule"),
    ("Commission and fees",
     "About 6% of the sale price", "About <strong>6%</strong> of the sale price",
     "None (0%)", "<strong>None (0%)</strong>"),
    ("Closing costs",
     "About 2–3%, paid by the seller", "About <strong>2–3%</strong>, paid by the seller",
     "We pay them", "<strong>We pay them</strong>"),
    ("Repairs",
     "Usually needed for top dollar", "Usually needed for top dollar",
     "None. Sold as-is", "<strong>None.</strong> Sold as-is"),
    ("Usually nets the most",
     "Yes, when the home is move-in ready", "Yes, when the home is move-in ready",
     "Trades some price for speed and certainty", "Trades some price for speed and certainty"),
]


def die(msg):
    sys.exit("build-prototypes: " + msg)


def plain(html):
    return re.sub(r"<[^>]+>", "", html)


def ensure_avatars():
    """Create the two avatar crops if they are missing (needs Pillow only in that case)."""
    for out, (src, box) in AVATARS.items():
        dst = ROOT / out
        if dst.exists():
            continue
        try:
            from PIL import Image
        except ImportError:
            die("%s is missing and Pillow is not installed to make it" % out)
        im = Image.open(ROOT / src).convert("RGB").crop(box).resize((112, 112), Image.LANCZOS)
        im.save(dst, "JPEG", quality=84, optimize=True, progressive=True)
        print("  made", out, dst.stat().st_size, "bytes")


def split_page():
    if not SRC.exists():
        die("index.html not found. Run python3 tools/build-pages.py first.")
    src = SRC.read_text(encoding="utf-8")
    h0 = src.find('<section class="hero" aria-labelledby="h1">')
    if h0 < 0:
        die("cannot find the live hero section in index.html")
    h1 = src.find("</section>", h0) + len("</section>")
    hero = src[h0:h1]
    if "<section" in hero[10:]:
        die("the hero now contains a nested <section>; update this script")
    if not src[h1:].lstrip().startswith('<div class="after-hero">'):
        die("the hero is no longer followed by .after-hero; update this script")
    return src, h0, h1, hero


def hero_a(hero):
    out = re.sub(r'[ \t]*(?:<i class="blob b\d"></i>)+[ \t]*\n', "", hero)
    if "blob" in out or out == hero:
        die("could not remove the three blob elements from the hero")
    return out


def live_rows(src):
    rows = re.findall(
        r'<tr><th scope="row">(.*?)</th><td data-label="Listing">(.*?)</td>'
        r'<td data-label="Direct to GLP" class="us">(.*?)</td></tr>', src)
    return {r[0]: (r[1], r[2]) for r in rows}


def hero_b(hero_clean, src):
    # reuse the live background art and the live copy block (pill, headline, lede, buttons, micro line)
    bg0 = hero_clean.index('<div class="hero-bg"')
    bg1 = hero_clean.index("</div>", bg0) + len("</div>")
    hero_bg = hero_clean[bg0:bg1]
    c0 = hero_clean.index('<div class="hero-copy">')
    c1 = hero_clean.index('<div class="hero-visual">')
    hero_copy = hero_clean[c0:c1].rstrip()
    if not hero_copy.endswith("</div>"):
        die("unexpected end of the hero copy block")

    live = live_rows(src)
    body = []
    for label, l_plain, l_html, g_plain, g_html in ROWS:
        if label not in live:
            die("the live comparison table no longer has the row %r" % label)
        if live[label][0] != l_plain or live[label][1] != g_plain:
            die("wording of the live table row %r changed.\n  live:  %r | %r\n  proto: %r | %r"
                % (label, live[label][0], live[label][1], l_plain, g_plain))
        if plain(l_html) != l_plain or plain(g_html) != g_plain:
            die("emphasis markup for %r changes the words" % label)
        # each cell's words sit inside ONE span so the phone layout (a two-column grid per cell) sees a single item
        body.append('<tr><th scope="row">%s</th><td data-label="Listing"><span class="hb-v">%s</span></td>'
                    '<td data-label="Direct to GLP" class="us"><span class="hb-v">%s</span></td></tr>' % (label, l_html, g_html))
    rows = "\n            ".join(body)

    visual = """<div class="hero-visual hb-visual">
        <section class="hb-card" aria-labelledby="hb-h">
          <div class="hb-head">
            <span class="eyebrow">Side by side</span>
            <h2 class="hb-title" id="hb-h">Two common paths, <span class="ital">in plain numbers.</span></h2>
          </div>
          <table class="hb-table">
            <caption class="vh">Listing with an agent compared with selling direct to GLP</caption>
            <thead><tr><th scope="col"><span class="vh">What you are comparing</span></th><th scope="col">Listing with an agent</th><th scope="col" class="us"><span class="us-badge">GLP</span>Selling direct to us</th></tr></thead>
            <tbody>
            %s
            </tbody>
          </table>
          <div class="hb-foot">
            <p class="hb-note">Typical figures, not a promise. Neither path is always better. <a href="#compare">See the full comparison.</a></p>
            <div class="hb-people">
              <span class="hb-avs" aria-hidden="true"><img src="images/joey-avatar.jpg" alt="" width="56" height="56" decoding="async"><img src="images/ethan-avatar.jpg" alt="" width="56" height="56" decoding="async"></span>
              <p><b>Joey &amp; Ethan</b><span>Co-founders · Hixson, TN</span></p>
            </div>
          </div>
        </section>
      </div>""" % rows

    return ('<section class="hero hero-b" aria-labelledby="h1">\n    ' + hero_bg +
            '\n    <div class="wrap hero-grid">\n      ' + hero_copy + "\n\n      " + visual +
            "\n    </div>\n  </section>")


BAR = """<aside class="proto-bar" aria-label="Prototype controls">
  <div class="wrap proto-in">
    <p class="proto-tag">Prototype</p>
    <p class="proto-note">Hero test only. The live home page is unchanged.</p>
    <ul class="proto-nav">
      <li><a href="proto-hero-a.html" data-base="proto-hero-a.html"%(a)s>A people-led</a></li>
      <li><a href="proto-hero-b.html" data-base="proto-hero-b.html"%(b)s>B numbers-led</a></li>
      <li><a href="index.html">Live home page</a></li>
    </ul>
    <div class="proto-seg" role="group" aria-label="Hero surface">
      <span class="proto-lab" aria-hidden="true">Surface</span>
      <button type="button" data-surface="cool" aria-pressed="true">Cool</button>
      <button type="button" data-surface="warm" aria-pressed="false">Warm</button>
    </div>
  </div>
</aside>

"""

HEAD_SCRIPT = ("<script>try{if(/[?&]surface=warm/.test(location.search))"
               "document.documentElement.setAttribute('data-surface','warm')}catch(e){}</script>\n")


def assemble(src, h0, h1, hero_html, which):
    page = src[:h0] + hero_html + src[h1:]
    names = {"a": "A, people-led", "b": "B, numbers-led"}
    # title
    page, n = re.subn(r"<title>.*?</title>", "<title>PROTOTYPE %s hero | GLP Home Options</title>" % names[which], page, count=1)
    if n != 1:
        die("title not found")
    # stylesheet, early surface script
    css = '<link rel="stylesheet" href="css/site.css?v='
    i = page.index(css)
    j = page.index(">", i) + 1
    page = page[:j] + '\n<link rel="stylesheet" href="%s">\n' % PROTO_CSS + HEAD_SCRIPT.rstrip("\n") + page[j:]
    # B shows a small portrait strip instead of the big photo, so it does not preload the photo
    if which == "b":
        page, n = re.subn(r'<link rel="preload" href="images/joey-ethan-bridge\.jpg"[^>]*>\n', "", page, count=1)
        if n != 1:
            die("photo preload not found")
    # body class and the bar (in normal flow, above the sticky header)
    if '<body id="top">' not in page:
        die("body tag not found")
    page = page.replace('<body id="top">', '<body id="top" class="proto-%s">' % which, 1)
    bar = BAR % {"a": ' aria-current="page"' if which == "a" else "", "b": ' aria-current="page"' if which == "b" else ""}
    if '<header class="hdr" id="hdr">' not in page:
        die("header not found")
    page = page.replace('<header class="hdr" id="hdr">', bar + '<header class="hdr" id="hdr">', 1)
    # script after the site script
    tag = '<script src="js/site.js?v='
    i = page.index(tag)
    j = page.index("</script>", i) + len("</script>")
    page = page[:j] + '\n<script src="%s" defer></script>' % PROTO_JS + page[j:]
    return page


def main():
    ensure_avatars()
    src, h0, h1, hero = split_page()
    clean = hero_a(hero)
    pages = {
        "proto-hero-a.html": assemble(src, h0, h1, clean, "a"),
        "proto-hero-b.html": assemble(src, h0, h1, hero_b(clean, src), "b"),
    }
    for name, html in pages.items():
        (ROOT / name).write_text(html, encoding="utf-8", newline="\n")
        print("wrote %s (%d bytes)" % (name, len(html.encode("utf-8"))))


if __name__ == "__main__":
    main()

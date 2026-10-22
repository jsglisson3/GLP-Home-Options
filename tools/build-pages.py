#!/usr/bin/env python3
"""Builds every page of the site from shared parts.

    python3 tools/build-pages.py

Why this exists: GitHub Pages serves plain files (no build step on the server), but the header, footer, icon sprite,
FAQ and contact blocks repeat on every page. This script keeps ONE copy of each and writes the finished pages.
Commit the generated .html files; the site itself stays plain HTML, CSS and JavaScript.

Where things live
  tools/pages/<page>.html   the <main> content of each page (index, options, about, work, new-homes, contact)
  tools/pages/_sprite.html  the icon sprite and the gable clip-path (see clean_sprite() below for why it is cleaned on read)
  tools/legal_text.py       the wording of the Privacy Policy and Terms (a plain-words draft, not lawyer-reviewed)
  tools/gallery_data.py     the photos on the Our work page (file, alt text, caption). tools/process-photos.py prepares new ones
  this file                 header, footer, mobile bar, FAQ text, titles and descriptions, structured data

Tokens you can use inside tools/pages/*.html
  [[herobg]] [[crumbs]] [[fb-button]]        shared bits
  [[contact-href]] [[home]] [[new-homes-href]] [[fb]]   links that depend on which page you are on
  [[faq home]] [[faq options]] ...           FAQ list (also feeds the FAQPage structured data, so they can never drift apart)
  [[cta options]] ...                        the closing call-to-action band
  [[gallery building]] [[gallery closed]]    a photo grid from tools/gallery_data.py (the Our work page)
  [[contact home]] [[contact page]]          the contact section (reach tiles, next steps, form)
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import gallery_data as GAL  # noqa: E402
import legal_text as LEGAL  # noqa: E402

# ------------------------------------------------------------------ site facts (change them here, once)
SITE = "https://jsglisson3.github.io/GLP-Home-Options/"   # the preview address. Swap for the real domain at launch.
REAL = "https://glphomeoptions.com"
FB = "https://www.facebook.com/profile.php?id=61588492362641"
PHONE_TEL, PHONE_SMS, PHONE = "tel:+14234515707", "sms:+14234515707", "(423) 451-5707"
EMAIL = "info@glphomeoptions.com"
BOOK = "https://links.voiseai.com/widget/booking/cM59fR3vJlAVRy08Depz"
FORM_ID = "c36UOOc2pkosxfvRfjZJ"
CSS_V, JS_V = 41, 20
HERO_SET = ' imagesrcset="images/joey-ethan-bridge.jpg 800w, images/joey-ethan-bridge-1200.jpg 1200w, images/joey-ethan-bridge-2x.jpg 1600w" imagesizes="(max-width:980px) 90vw, 460px"'
# The construction business may get its own site. When it does, point this one link at it (header, footer, menu and
# the "Now building" teasers all follow).
NEW_HOMES = "new-homes.html"

ICON = lambda n, cls="i": f'<svg class="{cls}" aria-hidden="true"><use href="#i-{n}"/></svg>'  # noqa: E731
NEWTAB = '<span class="vh"> (opens in a new tab)</span>'

# ------------------------------------------------------------------ pages
PAGES = [
    dict(slug="index", file="index.html", crumb=None, ghl=True, preload=["images/joey-ethan-bridge.jpg"],
         title="GLP Home Options | Real Home Options for Chattanooga Homeowners",
         desc="Joey and Ethan help Chattanooga homeowners compare their options: sell with no repairs in as little as 7 days, list for the best price, "
              "keep the home, or look at other options like seller financing and lease options. Local, with no pressure. Call or text (423) 451-5707.",
         og_title="GLP Home Options | Real home options. Clear next steps.",
         og_desc="Sell with no repairs, list for the best price, or keep it. Joey and Ethan lay out the real numbers in plain English. No pressure, just solutions.",
         ld=["business", "faq:home"]),
    dict(slug="options", file="options.html", crumb="Your options", preload=[],
         title="Your Home Options in Chattanooga | GLP Home Options",
         desc="Sell directly with no repairs in 7–14 days, list with an agent, keep your home, or look at seller financing and lease options. Every Chattanooga option side by side, in plain English.",
         og_title="Every option for your home, side by side | GLP Home Options",
         og_desc="Sell with no repairs, list for the best price, keep the home, or find another way. What each path costs, how long it takes, and who it fits.",
         ld=["faq:options", "crumbs"]),
    dict(slug="about", file="about.html", crumb="Our story", preload=["images/joey.jpg", "images/ethan.jpg"],
         title="Our Story: Meet Joey & Ethan | GLP Home Options",
         desc="Meet Joey and Ethan, co-founders of GLP Home Options in Hixson, TN. Guides, not gurus: clear options, honest advice, and no pressure for Chattanooga homeowners.",
         og_title="Guides, not gurus. Meet Joey & Ethan | GLP Home Options",
         og_desc="Two local co-founders, one simple promise: every option for your home, laid out in plain English. No pressure, just solutions.",
         ld=["crumbs"]),
    dict(slug="work", file="work.html", crumb="Our work", preload=[], js=["gallery"],
         title="Our Work: Renovations, Builds and Closings | GLP Home Options",
         desc="Photos from renovations, the new home we're building in Chattanooga, and a recent closing, from Joey and Ethan at GLP Home Options in Hixson, TN.",
         og_title="Our work: renovations, builds and closings | GLP Home Options",
         og_desc="Photos from the job sites and a recent closing in Chattanooga.",
         ld=["crumbs"]),
    dict(slug="new-homes", file="new-homes.html", crumb="New homes", preload=["images/build-exterior.jpg"],
         title="Affordable New Homes in Chattanooga | GLP Home Options",
         desc="A new home we're building in Chattanooga for first-time buyers and families: 3 bed, 2 bath on 0.6+ acres, priced in the mid $200s. Ask about getting in early.",
         og_title="Affordable new homes, built right here | GLP Home Options",
         og_desc="3 bed, 2 bath on 0.6+ acres in Chattanooga, priced in the mid $200s. Ask about getting in before it's listed.",
         ld=["faq:homes", "crumbs"]),
    dict(slug="contact", file="contact.html", crumb="Contact", ghl=True, preload=[],
         title="Contact Us: Call, Text, or Send Details | GLP Home Options",
         desc="Call or text (423) 451-5707, email, book a call, or send a few details. Joey or Ethan will get back to you. No pressure, no obligation.",
         og_title="Let's talk about your home | GLP Home Options",
         og_desc="Call, text, email, or send a few details. You'll talk to Joey or Ethan. No pressure, no scripts.",
         ld=["business", "crumbs"]),
]
for p in PAGES:
    p.setdefault("ghl", False)
    p.setdefault("legal", False)

LEGAL_PAGES = [
    dict(slug="privacy", file=LEGAL.PRIVACY["file"], crumb=None, ghl=False, legal=True, preload=[], ld=[],
         title="Privacy Policy | GLP Home Options", desc=LEGAL.PRIVACY["meta"], data=LEGAL.PRIVACY),
    dict(slug="terms", file=LEGAL.TERMS["file"], crumb=None, ghl=False, legal=True, preload=[], ld=[],
         title="Terms of Service | GLP Home Options", desc=LEGAL.TERMS["meta"], data=LEGAL.TERMS),
]

# ------------------------------------------------------------------ FAQ text (the visible list and the structured data both come from here)
LINK_FB = f'<a href="{FB}" target="_blank" rel="noopener">our Facebook page{NEWTAB}</a>'
FAQ = {
    "home": [
        ("Do I have to sell to you if I reach out?",
         "No. The first conversation is free and there's no obligation. We'll show you every realistic option, including listing with an agent or keeping the home, and you decide what's right."),
        ("How do I know GLP is legit?",
         f'Fair question. You deal directly with Joey or Ethan, and you can reach us anytime at <a href="{PHONE_TEL}">{PHONE}</a> or <a href="mailto:{EMAIL}">{EMAIL}</a>. '
         f'You can see our recent closing and the home we\'re building on <a href="work.html">our work page</a> and {LINK_FB}. And you\'re always free to have your own attorney or title company review anything before you sign.'),
        ("How fast can you close, and what does it cost me?",
         "As little as 7 days, and usually 7 to 14. You pick the closing date, so if you need more time to move, that works too. "
         "We buy the house as it is, so there are no repairs, no cleaning, and no showings, just one visit so we can see the home. "
         "There are no commissions or fees, and we pay the closing costs on a direct sale."),
        ("Why would I list instead of taking a cash offer?",
         "If your home is ready to move into and you aren't in a hurry, listing on the open market usually brings in the most money. We'll tell you plainly if that's your best move."),
        ("What if I want to keep my home but I'm struggling?",
         "We can help you think through refinancing, renting the property out, or other ways to get past short-term financial trouble so you can stay."),
        ("Do you offer seller financing or lease options?",
         'Yes. If the usual paths don\'t fit your situation, we can look at other setups together, like seller financing (you carry the loan instead of a bank) or a lease option (a buyer rents first and can choose to buy later). <a href="options.html#creative">See how they work.</a>'),
        ("Can you help me figure out where to go next?",
         "Often, yes. In a recent sale the owners needed a place to move, so we worked around their timeline and helped them find a rental."),
        ("What areas do you serve?",
         "We work in Chattanooga and the surrounding counties, generally within about an hour of the city, in Tennessee and Georgia. We're based in Hixson. Not sure whether your address is in our area? Call or text us and we'll tell you."),
        ("Do you build homes too?",
         'Yes. We build affordable new homes in Chattanooga for first-time buyers and families. Ask us what\'s coming up next. <a href="[[new-homes-href]]">See what we\'re building.</a>'),
    ],
    "options": [
        ("What does “as-is” mean?",
         "It means you sell the home in the condition it's in today. If you sell directly to us, there are no repairs, no cleaning, and no showings. We just visit once so we can see the house."),
        ("Will I get less money selling directly than listing?",
         "A direct offer is often lower than the best-case listing price, because you're trading some price for speed, certainty, and skipping repairs, showings, and months of house payments and bills. "
         'Once commission, closing costs, and those costs come out, the gap can be smaller than it first looks. Run your own numbers on <a href="[[home]]#netsheet">the net sheet</a>.'),
        ("How do I know which option is right for me?",
         "Start with what matters most: speed, price, or staying put. Then talk to us. We'll go over the numbers together and tell you what we'd do in your position."),
        ("What are seller financing and a lease option?",
         "With seller financing, the seller carries the loan instead of a bank, and the buyer pays the seller over time under agreed terms. "
         "With a lease option, a buyer rents the home with the option to buy it later at an agreed price, and doesn't have to buy. "
         "Terms vary, so have your own attorney or title company review any agreement before you sign."),
        ("Do I have to decide on the first call?",
         "No. The first conversation is free, with no obligation. Take the time you need."),
    ],
    "homes": [
        ("Is the home available yet?",
         "Not yet. It's coming soon. Ask us about getting in before it's listed."),
        ("What's the price, and how big is it?",
         "We're pricing it in the mid $200s. It has three bedrooms and two baths on 0.6+ acres in Chattanooga. Reach out and we'll go over the details with you."),
        ("I'm a first-time buyer. Can I get help with the down payment?",
         "Possibly. Down payment assistance exists for many first-time buyers, and what you qualify for depends on your situation and your lender. Ask us and we'll talk it through."),
        ("Will you build more homes?",
         "We're building affordable homes right here in Chattanooga. Ask us what's coming up next."),
        ("Do you help people sell their homes, too?",
         'Yes. We help Chattanooga homeowners compare every option, including selling directly to us. <a href="options.html">See your options.</a>'),
    ],
}
FAQ["contact"] = [q for q in FAQ["home"] if q[0] in (
    "Do I have to sell to you if I reach out?", "How do I know GLP is legit?", "What areas do you serve?")]

CTAS = {
    "options": ("Ready when you are", "Not sure which path fits? <span class=\"ital\">Tell us what's going on.</span>",
                "We'll go over the numbers together and tell you what we'd do in your position."),
    "about": ("Let's talk", "Ready to talk it through? <span class=\"ital\">We're a call away.</span>",
              "You'll talk to Joey or Ethan. We'll listen first, show you every option, and let you decide."),
    "homes": ("Be first to know", "Want to see it <span class=\"ital\">before it's listed?</span>",
              "Ask about getting in early, or about down payment assistance if you're a first-time buyer. You'll talk to Joey or Ethan."),
    "work": ("Let's talk", "Have a house on your mind? <span class=\"ital\">Tell us about it.</span>",
             "You'll talk to Joey or Ethan. We'll listen first, show you every option, and let you decide."),
}

RIDGE = ('<svg class="ridge" viewBox="0 0 1440 240" preserveAspectRatio="none" focusable="false">'
         '<path class="r1" d="M0 150 L150 138 C200 104 224 88 270 84 L560 80 C612 82 634 104 690 128 C770 160 850 130 930 104 C990 84 1050 78 1110 92 C1190 110 1230 146 1310 140 C1370 136 1410 120 1440 124 L1440 240 L0 240Z"/>'
         '<path class="r2" d="M0 176 C120 150 220 142 330 164 C450 188 540 200 660 178 C790 154 880 118 1010 130 C1140 142 1260 190 1440 160 L1440 240 L0 240Z"/>'
         '<path class="r3" d="M0 208 C180 186 300 190 460 206 C620 222 760 214 900 196 C1060 176 1240 176 1440 206 L1440 240 L0 240Z"/></svg>')

def clean_sprite(text):
    """Return the icon sprite exactly as it should appear inside the pages.

    When Claude saves a file to your computer, the transfer can stamp an invisible "Content Credentials" (provenance)
    block onto it. For a standalone SVG like this sprite that shows up as an xmlns:c2pa attribute plus a <metadata>
    element (about 8 KB of base64). That tag belongs to the sprite *file*, not to the pages, so it is left out of the
    generated HTML. The leading comment is the file's own header (it also keeps the file from being mistaken for a
    standalone image). Neither belongs in the pages.
    """
    text = re.sub(r"^\s*<!--.*?-->\s*", "", text, count=1, flags=re.S)
    text = re.sub(r"\s+xmlns:c2pa=\"[^\"]*\"", "", text)
    text = re.sub(r"<metadata>.*?</metadata>", "", text, flags=re.S)
    return text.strip()


SPRITE = clean_sprite((TOOLS / "pages" / "_sprite.html").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ link helpers (home page uses in-page anchors, other pages point at index.html)
def is_home(pg):
    return pg["slug"] == "index"


def home_href(pg):
    return "#top" if is_home(pg) else "index.html"


def sec(pg, anchor):
    return f"#{anchor}" if is_home(pg) else f"index.html#{anchor}"


def contact_href(pg):
    return "#contact" if pg["slug"] in ("index", "contact") else "contact.html#contact"


# ------------------------------------------------------------------ shared pieces
def head(pg):
    url = SITE if is_home(pg) else SITE + pg["file"]
    real = REAL + "/" + ("" if is_home(pg) else pg["file"])
    pre = "".join(f'<link rel="preload" href="{u}" as="image" fetchpriority="high"{HERO_SET if u.endswith("joey-ethan-bridge.jpg") else ""}>\n' for u in pg["preload"][:1])
    ital = "" if pg["legal"] else '<link rel="preload" href="fonts/fraunces-latin-wght-italic.woff2" as="font" type="font/woff2" crossorigin>\n'
    og = ""
    if not pg["legal"]:
        og = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="GLP Home Options">
<meta property="og:title" content="{html.escape(pg['og_title'], quote=True)}">
<meta property="og:description" content="{html.escape(pg['og_desc'], quote=True)}">
<meta property="og:image" content="{SITE}images/og-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="GLP Home Options: Real home options. Clear next steps.">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
'''
    ld = "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in ld_blocks(pg))
    return f'''<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(pg['title'])}</title>
<meta name="description" content="{html.escape(pg['desc'], quote=True)}">
<meta name="theme-color" content="#2d4855">
<!-- DRAFT: delete this noindex line, and un-comment the canonical below, when the site goes live on the real domain -->
<meta name="robots" content="noindex, nofollow">
<!-- <link rel="canonical" href="{real}"> -->
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="images/favicon-512.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
{og}<link rel="preload" href="fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{ital}{pre}<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__glpReady)document.documentElement.classList.remove('js')}},6000)</script>
<link rel="stylesheet" href="css/site.css?v={CSS_V}">
{ld}</head>'''


def strip_tags(t):
    t = re.sub(r'<span class="vh">.*?</span>', "", t)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()


def ld_blocks(pg):
    out = []
    for key in pg["ld"]:
        if key == "business":
            out.append({
                "@context": "https://schema.org", "@type": "LocalBusiness", "name": "GLP Home Options", "legalName": "GL Partners LLC",
                "description": "Chattanooga home options: sell directly with no repairs, list with an agent, keep your home, or another arrangement like seller financing or a lease option. Plus affordable new homes.",
                "telephone": "+1-423-451-5707", "email": EMAIL, "url": REAL,
                "image": SITE + "images/joey-ethan-bridge.jpg", "logo": SITE + "images/glp-mark.png",
                "address": {"@type": "PostalAddress", "postOfficeBoxNumber": "55", "addressLocality": "Hixson", "addressRegion": "TN", "addressCountry": "US"},
                "areaServed": [{"@type": "City", "name": "Chattanooga, TN"}, "Counties within about an hour of Chattanooga, in Tennessee and Georgia"],
                "founder": [{"@type": "Person", "name": "Joey"}, {"@type": "Person", "name": "Ethan"}],
                "sameAs": [FB]})
        elif key.startswith("faq:"):
            items = FAQ[key[4:]]
            out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(resolve_links(pg, a))}} for q, a in items]})
        elif key == "crumbs":
            out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": REAL + "/"},
                {"@type": "ListItem", "position": 2, "name": pg["crumb"], "item": REAL + "/" + pg["file"]}]})
    return out


def image_size(rel):
    """Width and height of a JPEG or PNG, read from the file itself, so a page can never disagree with its photo."""
    data = (ROOT / rel).read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        m = data[i + 1]
        if m == 0xFF or m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 1 if m == 0xFF else 2
            continue
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):   # a "start of frame" block holds the size
            return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
        i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
    raise ValueError(f"cannot read the size of {rel}")


def gallery(group):
    """The photo grid for one group in tools/gallery_data.py. Each photo is a plain link to the larger picture
    (it works with no JavaScript); js/gallery.js adds the viewer on top."""
    items = [g for g in GAL.GALLERY if g["group"] == group]
    if not items:
        sys.exit(f"gallery '{group}': no photos in tools/gallery_data.py")
    out, ratios = [], set()
    for g in items:
        w, h = image_size(g["img"])
        ratios.add(round(w / h, 2))
        full = g.get("full") or g["img"]
        out.append(
            f'  <li class="work-item rv"><figure><a href="{full}"><img src="{g["img"]}" alt="{html.escape(g["alt"], quote=True)}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"></a>'
            f'<figcaption>{html.escape(g["caption"])}</figcaption></figure></li>')
    # photos that are all the same shape sit in tidy rows; mixed shapes flow into columns
    rows = " work-rows" if len(items) >= 3 and len(ratios) == 1 else ""
    return f'<ul class="work-grid{rows}" data-stagger>\n' + "\n".join(out) + "\n      </ul>"


def fb_button():
    return (f'<a class="fb-btn" href="{FB}" target="_blank" rel="noopener">{ICON("fb-logo", "fb-logo")}'
            f'<span><b>Follow us on Facebook</b><small>Recent closings and builds</small>{NEWTAB}</span></a>')


def brand(pg, lazy=False):
    la = ' loading="lazy"' if lazy else ""
    return (f'<a class="brand" href="{home_href(pg)}"><img src="images/glp-mark.png" alt="" width="240" height="132"{la}>'
            '<span class="wordmark"><b>GLP</b> <span class="wm-sub"><i>HOME</i> <i>OPTIONS</i></span></span></a>')


def header(pg):
    cur = pg["slug"]

    def link(slug, label, href):
        return f'<a href="{href}"' + (' class="active" aria-current="page"' if cur == slug else "") + f">{label}</a>"

    nav = "\n      ".join([
        link("options", "Your options", "options.html"),
        f'<a href="{sec(pg, "numbers")}">The numbers</a>',
        link("about", "Our story", "about.html"),
        link("work", "Our work", "work.html"),
        link("new-homes", "New homes", NEW_HOMES),
        link("contact", "Contact", "contact.html"),
    ])
    mnav = "\n      ".join([
        link("options", "Your options", "options.html"),
        f'<a href="{sec(pg, "how")}">How it works</a>',
        f'<a href="{sec(pg, "numbers")}">Compare &amp; net sheet</a>',
        link("about", "Our story", "about.html"),
        link("work", "Our work", "work.html"),
        link("new-homes", "New homes", NEW_HOMES),
        f'<a href="{sec(pg, "faq")}">FAQ</a>',
        link("contact", "Contact", "contact.html"),
    ])
    return f'''<header class="hdr" id="hdr">
  <div class="wrap hdr-row">
    {brand(pg)}
    <nav class="nav" aria-label="Main">
      {nav}
    </nav>
    <a class="hdr-fb" href="{FB}" target="_blank" rel="noopener" aria-label="GLP Home Options on Facebook (opens in a new tab)" title="GLP Home Options on Facebook">{ICON("fb-logo", "fb-logo")}</a>
    <a class="btn btn-primary btn-sm hdr-cta" href="{contact_href(pg)}">Get my options</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">{ICON("menu")}<span>Menu</span></button>
  </div>
  <div class="mnav" id="mnav" hidden>
    <nav aria-label="Sections">
      {mnav}
    </nav>
    <a class="mnav-fb" href="{FB}" target="_blank" rel="noopener">{ICON("fb-logo", "fb-logo")}<span><b>Follow us on Facebook</b><small>Recent closings and builds</small>{NEWTAB}</span></a>
    <div class="mnav-cta">
      <a class="btn btn-primary" href="{PHONE_TEL}">{ICON("phone")}Call</a>
      <a class="btn btn-ghost" href="{PHONE_SMS}">{ICON("sms")}Text</a>
    </div>
  </div>
</header>'''


def footer(pg):
    return f'''<footer class="ftr">
  <div class="wrap ftr-grid">
    <div class="ftr-brand">
      {brand(pg, lazy=True)}
      <p>Real home options and clear next steps for Chattanooga homeowners. Based in Hixson, TN.</p>
      {fb_button()}
    </div>
    <nav class="ftr-col" aria-label="Explore">
      <h2>Explore</h2>
      <a href="options.html">Your options</a><a href="{sec(pg, "how")}">How it works</a><a href="{sec(pg, "numbers")}">Compare &amp; net sheet</a><a href="about.html">Our story</a><a href="work.html">Our work</a><a href="{NEW_HOMES}">New homes</a><a href="{sec(pg, "faq")}">FAQ</a><a href="contact.html">Contact</a>
    </nav>
    <div class="ftr-col">
      <h2>Contact</h2>
      <a href="{PHONE_TEL}">{PHONE}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <span>PO Box 55, Hixson, TN</span>
      <span>Serving Chattanooga &amp; surrounding counties</span>
    </div>
    <nav class="ftr-col" aria-label="Legal">
      <h2>Legal</h2>
      <a href="privacy-policy.html">Privacy Policy</a>
      <a href="terms-of-service.html">Terms of Service</a>
    </nav>
  </div>
  <div class="wrap ftr-base">
    <p>&copy; <span id="yr">2026</span> GLP Home Options (legal entity: GL Partners LLC). All rights reserved.</p>
    <p>This site is for informational purposes only and is not legal, tax, or financial advice.</p>
  </div>
</footer>'''


def bar(pg):
    return f'''<nav class="mobile-bar" aria-label="Quick contact">
  <a class="mb-call" href="{PHONE_TEL}">{ICON("phone")}Call</a>
  <a class="mb-text" href="{PHONE_SMS}">{ICON("sms")}Text</a>
  <a class="mb-go" href="{contact_href(pg)}">Get my options</a>
</nav>'''


def herobg():
    return f'''<div class="hero-bg" aria-hidden="true">
      <canvas class="topo" data-tone="dark"></canvas>
      {RIDGE}
    </div>'''


def crumbs(pg):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li>'
            f'<li><span aria-current="page">{pg["crumb"]}</span></li></ol></nav>')


def faq_list(pg, key):
    out = []
    for i, (q, a) in enumerate(FAQ[key]):
        out.append(f'        <details class="rv"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>')
    return "\n".join(out)


def cta_band(pg, key):
    eyebrow, h2, lede = CTAS[key]
    return f'''<section class="cta-band" aria-labelledby="cta-h">
    <div class="cta-bg" aria-hidden="true"><canvas class="topo" data-tone="light"></canvas></div>
    <div class="wrap cta-grid">
      <div class="cta-copy rv">
        <span class="eyebrow on-dark">{eyebrow}</span>
        <h2 id="cta-h">{h2}</h2>
        <p class="lede">{lede}</p>
      </div>
      <div class="cta-actions rv" data-d="1">
        <a class="btn btn-light btn-lg" href="{contact_href(pg)}">Send us a few details{ICON("arrow")}</a>
        <a class="btn btn-outline-light btn-lg" href="{PHONE_TEL}">{ICON("phone")}Call or text {PHONE}</a>
        <p class="cta-note">No obligation, no spam. Your information is kept confidential.</p>
      </div>
    </div>
  </section>'''


def reach(page=False):
    # On the Contact page the heading block (see contact_section) is plain, with no fade, so the first paragraph counts as painted
    # the moment the page paints (a fading block counts only when its fade ends). The Call and Text tiles are on the first screen too:
    # they are marked "in" (with the same stagger value the script would set) and fade in from the stylesheet alone instead of waiting
    # for site.js. Elsewhere the script reveals the tiles on scroll.
    def tile(i):
        return f'class="reach-item rv in" style="--d:{i}"' if page and i < 2 else 'class="reach-item rv"'
    return f'''<div class="reach" data-stagger>
          <a {tile(0)} href="{PHONE_TEL}">
            <span class="ico" aria-hidden="true">{ICON("phone")}</span>
            <span class="txt"><small>Call</small><b>{PHONE}</b></span><span class="go" aria-hidden="true">Call</span>
          </a>
          <a {tile(1)} href="{PHONE_SMS}">
            <span class="ico" aria-hidden="true">{ICON("sms")}</span>
            <span class="txt"><small>Text</small><b>{PHONE}</b></span><span class="go" aria-hidden="true">Text</span>
          </a>
          <a class="reach-item rv" href="mailto:{EMAIL}">
            <span class="ico" aria-hidden="true">{ICON("mail")}</span>
            <span class="txt"><small>Email</small><b class="sm">{EMAIL}</b></span><span class="go" aria-hidden="true">Email</span>
          </a>
          <a class="reach-item rv" href="{BOOK}" target="_blank" rel="noopener">
            <span class="ico" aria-hidden="true">{ICON("cal")}</span>
            <span class="txt"><small>Prefer a set time?</small><b class="sm">Book a call with us{NEWTAB}</b></span><span class="go" aria-hidden="true">Book</span>
          </a>
          <a class="reach-item rv" href="{FB}" target="_blank" rel="noopener">
            <span class="ico" aria-hidden="true">{ICON("fb-logo", "fb-logo")}</span>
            <span class="txt"><small>Recent closings and builds</small><b class="sm">Find us on Facebook{NEWTAB}</b></span><span class="go" aria-hidden="true">Visit</span>
          </a>
        </div>'''


def contact_section(pg, page=False):
    if page:
        top = f'''{crumbs(pg)}
          <span class="eyebrow on-dark">Contact</span>
          <h1 id="contact-h">Let's talk about your home. <span class="ital">No pressure, no scripts.</span></h1>'''
    else:
        top = '''<span class="eyebrow on-dark">Let's start a conversation</span>
          <h2 id="contact-h">Want to talk it through? <span class="ital">Call or text Joey or Ethan.</span></h2>'''
    # On the Contact page the H1 sits directly above these two headings, so they are H2s there
    # (looks identical: the .h3 class carries the H3 styling). On the home page the section title is an H2, so H3 is right.
    hx = "h2" if page else "h3"
    return f'''<section class="contact{" contact-page" if page else ""}" id="contact" aria-labelledby="contact-h">
    <div class="contact-bg" aria-hidden="true"><canvas class="topo" data-tone="light"></canvas></div>
    <div class="wrap contact-grid">
      <div class="contact-copy">
        <div{"" if page else ' class="rv"'}>
          {top}
          <p class="lede">Call or text anytime, or send a few details. You'll talk to Joey or Ethan, and your information stays&nbsp;confidential.</p>
        </div>
        {reach(page)}
        <div class="next rv">
          <{hx} class="h3">What happens next?</{hx}>
          <ol>
            <li><span class="num" aria-hidden="true">1</span>We talk through your situation.</li>
            <li><span class="num" aria-hidden="true">2</span>We go over your options together.</li>
            <li><span class="num" aria-hidden="true">3</span>You decide what's best for you.</li>
          </ol>
        </div>
      </div>

      <div class="form-card rv{' in" style="--d:2' if page else ''}" data-d="2">
        <p class="form-who"><span class="avs" aria-hidden="true"><img src="images/joey-avatar.jpg" alt="" width="112" height="112"{"" if page else ' loading="lazy"'} decoding="async"><img src="images/ethan-avatar.jpg" alt="" width="112" height="112"{"" if page else ' loading="lazy"'} decoding="async"></span><span><b>Joey &amp; Ethan</b><small>Co-founders<span class="sep"> · </span><span class="loc">Hixson, TN</span></small></span></p>
        <{hx} class="h3">Thinking about selling, or not sure yet?</{hx}>
        <p class="sub">Share a few details and Joey or Ethan will get back to you. There's no obligation.</p>
        <div class="ghl">
          <iframe src="https://links.voiseai.com/widget/form/{FORM_ID}" loading="lazy" style="width:100%;height:760px;border:none;border-radius:10px" id="inline-{FORM_ID}" data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="GLP Home Options lead form" data-height="760" data-layout-iframe-id="inline-{FORM_ID}" data-form-id="{FORM_ID}" title="Contact form: send GLP Home Options a few details about your home"></iframe>
        </div>
        <p class="form-alt">Form not loading? Call or text <a href="{PHONE_TEL}">{PHONE}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </div>
    </div>
  </section>'''


def resolve_links(pg, text):
    nh = NEW_HOMES
    return (text.replace("[[home]]", "" if is_home(pg) else "index.html")
                .replace("[[contact-href]]", contact_href(pg))
                .replace("[[new-homes-href]]", nh)
                .replace("[[fb]]", FB))


def expand(pg, text):
    def sub(m):
        tok = m.group(1).strip()
        if tok == "herobg":
            return herobg()
        if tok == "crumbs":
            return crumbs(pg)
        if tok == "fb-button":
            return fb_button()
        if tok.startswith("faq "):
            return faq_list(pg, tok.split(" ", 1)[1])
        if tok.startswith("cta "):
            return cta_band(pg, tok.split(" ", 1)[1])
        if tok.startswith("gallery "):
            return gallery(tok.split(" ", 1)[1])
        if tok == "contact home":
            return contact_section(pg, page=False)
        if tok == "contact page":
            return contact_section(pg, page=True)
        return m.group(0)
    text = re.sub(r"\[\[([^\]]+)\]\]", sub, text)
    return resolve_links(pg, text)


def scripts(pg):
    s = ""
    if pg["ghl"]:
        s += '<script src="https://links.voiseai.com/js/form_embed.js" async></script>\n'
    # if site.js fails to load, drop the "js" class at once so no section stays hidden waiting for it (the head also has a 6 s safety timer)
    s += f'<script src="js/site.js?v={JS_V}" defer onerror=\'document.documentElement.classList.remove("js")\'></script>'
    for name in pg.get("js", []):   # scripts only one page needs (the Our work photo viewer)
        s += f'\n<script src="js/{name}.js?v={JS_V}" defer></script>'
    return s


APOS = re.compile(r"(?<=\w)'")
ATTR = re.compile(r'\b(alt|title|content|aria-label)="([^"]*)"')
TOKENS = re.compile(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>|[^<]+", re.S)


def curly(page):
    """Curly apostrophes (it's -> it\u2019s) in the visible text, alt text, meta text and JSON-LD of a built page; never in scripts,
    styles, tags or addresses. The page sources keep plain apostrophes, so anyone editing a page types them normally.
    Guard: the built page may differ from its input in the apostrophe character and nothing else."""
    def one(tok):
        if tok.startswith("<script"):
            return APOS.sub("\u2019", tok) if "application/ld+json" in tok[:tok.find(">")] else tok
        if tok.startswith(("<style", "<!--")):
            return tok
        if tok.startswith("<"):
            return ATTR.sub(lambda m: f'{m.group(1)}="{APOS.sub(chr(0x2019), m.group(2))}"', tok)
        return APOS.sub("\u2019", tok)
    out = "".join(one(t.group(0)) for t in TOKENS.finditer(page))
    if out.replace("\u2019", "'") != page.replace("\u2019", "'"):
        sys.exit("curly(): it changed something other than apostrophes; the page was not written")
    return out


def render(pg, main):
    return f'''<!doctype html>
<html lang="en">
{head(pg)}
<body id="top">
<a class="skip" href="#main">Skip to main content</a>

<!-- Icon sprite + the gable shape used to frame photos (echoes the roofline in the logo) -->
{SPRITE}

{header(pg)}

<main id="main" tabindex="-1">
{main.strip(chr(10))}
</main>

{footer(pg)}

{bar(pg)}

{scripts(pg)}
</body>
</html>
'''


def legal_main(d):
    body = "\n".join("        <h2>{}</h2>\n".format(h) + "\n".join("        " + p for p in ps) for h, ps in d["sections"])
    return f'''  <section class="doc-hero">
    <div class="wrap">
      <span class="eyebrow">Legal</span>
      <h1>{d['title']}</h1>
      <p class="lede">{d['lede']}</p>
    </div>
  </section>
  <section class="doc">
    <div class="wrap">
      <article class="doc-card">
        <p>{d['intro']}</p>
{body}
        {LEGAL.NOTE}
      </article>
    </div>
  </section>'''


def main():
    for pg in PAGES:
        src = (TOOLS / "pages" / f"{pg['slug']}.html").read_text(encoding="utf-8")
        out = curly(render(pg, expand(pg, src)))
        left = re.findall(r"\[\[[^\]]+\]\]", out)
        if left:
            sys.exit(f"{pg['file']}: unresolved tokens {left}")
        (ROOT / pg["file"]).write_text(out, encoding="utf-8")
        print("wrote", pg["file"], f"({len(out) // 1024} KB)")
    for pg in LEGAL_PAGES:
        out = curly(render(pg, legal_main(pg["data"])))
        (ROOT / pg["file"]).write_text(out, encoding="utf-8")
        print("wrote", pg["file"], f"({len(out) // 1024} KB)")


if __name__ == "__main__":
    main()

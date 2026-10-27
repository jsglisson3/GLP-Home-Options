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
  [[phone]] [[tel]] [[sms]] [[email]] [[address]]   the business details, written once at the top of this file (never type them into a page)
  [[proof]] (alone on its line)   the "What homeowners say" band: nothing until tools/reviews_data.py holds real facts
  [[review-url]] [[newtab]]   the review page only (built when tools/reviews_data.py has a Google review link)
  [[contact-href]] [[home]] [[new-homes-href]] [[fb]]   links that depend on which page you are on
  [[contact-href sell]] (or keep, new, unsure)   the same link, and the contact form opens with that choice ticked (add data-topic="sell" to the button too; an unknown choice stops the build)
  [[faq home]] [[faq options]] ...           FAQ list (also feeds the FAQPage structured data, so they can never drift apart)
  [[cta options]] ...                        the closing call-to-action band
  [[gallery building]] [[gallery closed]]    a photo grid from tools/gallery_data.py (the Our work page)
  [[carousel renovating]]                     a sideways photo strip from the same photos (Home, Checkpoint 47)
  [[contact home]] [[contact page]]          the contact section (reach tiles, next steps, form)
"""
import html
import json
import os
import pathlib
import re
import sys
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import form_text as FORM  # noqa: E402
import gallery_data as GAL  # noqa: E402
import legal_text as LEGAL  # noqa: E402
import reviews_data as REV  # noqa: E402

# Real review facts live in tools/reviews_data.py (empty today). If they break a rule the site is not built, so a wrong rating can never be published.
_rv = REV.problems()
if _rv:
    sys.exit("tools/reviews_data.py breaks a rule:\n  - " + "\n  - ".join(_rv))

# ------------------------------------------------------------------ THE LAUNCH SWITCH (one line) and site facts (change them here, once)
#   LIVE = False  PREVIEW (today). The github.io address. Every page says noindex, nofollow. No canonical tag, no sitemap.xml, no robots.txt, no CNAME.
#   LIVE = True   LAUNCH. The real domain. noindex is gone, every page names its own address (canonical), and sitemap.xml, robots.txt and CNAME are written.
# Do not flip it on its own: follow research/launch-checklist.md (domain, Search Console, Google Business Profile, redirects, a way back).
# `python3 tools/seo-check.py` builds the live version in a scratch folder and tests both states without touching the saved pages.
LIVE = False
if os.environ.get("GLP_BUILD"):   # only tools/seo-check.py and a test copy set this, to build either state in a scratch folder
    if os.environ["GLP_BUILD"] not in ("live", "preview"):
        sys.exit('GLP_BUILD must be exactly "live" or "preview" (or not set at all), not ' + repr(os.environ["GLP_BUILD"]))
    LIVE = os.environ["GLP_BUILD"] == "live"
PREVIEW = "https://jsglisson3.github.io/GLP-Home-Options/"   # the preview address (a sub-path of github.io)
REAL = "https://glphomeoptions.com"                           # the real domain, no trailing slash
SITE = (REAL + "/") if LIVE else PREVIEW                      # every address a page writes about itself starts here
FB = "https://www.facebook.com/profile.php?id=61588492362641"
PHONE_TEL, PHONE_SMS, PHONE = "tel:+14234515707", "sms:+14234515707", "(423) 451-5707"
EMAIL = "info@glphomeoptions.com"
PHONE_LD = "+{}-{}-{}-{}".format(PHONE_TEL[5], PHONE_TEL[6:9], PHONE_TEL[9:12], PHONE_TEL[12:])   # "+1-423-451-5707" for structured data, from PHONE_TEL
ADDRESS = "PO Box 55, Hixson, TN"   # the one public address line (footer, Contact page, print sheet, Privacy page); the Google listing must show the same business details. Joey decides what goes here (see research/launch-checklist.md, decision 3).
BOOK = "https://links.voiseai.com/widget/booking/cM59fR3vJlAVRy08Depz"
# The contact form (Checkpoint 46) is ours, not a frame from another company (the old GoHighLevel form was c36UOOc2pkosxfvRfjZJ). Where it sends what a visitor types:
#   ""            (today) nowhere yet. The form puts the details into a ready-made text or email and the visitor's own phone or mail app sends it; the page says plainly that nothing has been sent until they do.
#   "https://..." the address that receives the form (see research/form-wiring.md). The form then sends it there itself and says "Thank you"; if that ever fails, the visitor gets the text/email hand-off instead.
# Change this one line when the receiving end exists; nothing else needs touching. tools/seo-check.py insists it is empty or an https address.
# FORM_FORMAT is how the details are posted there: "json" (one block of text, the default) or "form" (name=value&name=value, as an ordinary web form is sent, which most
# form services and Zapier-style catch-hooks expect). Both go straight out with no permission check first, so the receiving end only has to allow this site (CORS).
FORM_ENDPOINT = ""
FORM_FORMAT = "json"
CSS_V, JS_V = 52, 26
HERO_SET = ' imagesrcset="images/joey-ethan-bridge.jpg 800w, images/joey-ethan-bridge-1200.jpg 1200w, images/joey-ethan-bridge-2x.jpg 1600w" imagesizes="(max-width:980px) 90vw, 460px"'
# The construction business may get its own site. When it does, point this one link at it (header, footer, menu and
# the "Now building" teasers all follow).
NEW_HOMES = "new-homes.html"

ICON = lambda n, cls="i": f'<svg class="{cls}" aria-hidden="true"><use href="#i-{n}"/></svg>'  # noqa: E731
NEWTAB = '<span class="vh"> (opens in a new tab)</span>'

# ------------------------------------------------------------------ pages
PAGES = [
    dict(slug="index", file="index.html", crumb=None, js=["form"], preload=["images/joey-ethan-bridge.jpg"],
         title="GLP Home Options | Real Home Options for Chattanooga Homeowners",
         desc=f"Joey and Ethan help Chattanooga homeowners compare every option: sell with no repairs in as little as 7 days, list, or keep the home. Call {PHONE}.",
         og_title="GLP Home Options | Real home options. Clear next steps.",
         og_desc="Sell with no repairs, list for the best price, or keep it. Joey and Ethan lay out the real numbers in plain English. No pressure, just solutions.",
         ld=["business", "website", "faq:home"]),
    dict(slug="options", file="options.html", crumb="Your options", preload=[],
         title="Your Home Options in Chattanooga | GLP Home Options",
         desc="Sell directly with no repairs in 7–14 days, list with an agent, keep your home, or look at seller financing. See every option side by side in plain English.",
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
         desc="A new home we're building in Chattanooga: 3 bed, 2 bath on 0.6+ acres, priced in the mid $200s. Want to see it before it's listed? Ask us.",
         og_title="Affordable new homes, built right here | GLP Home Options",
         og_desc="3 bed, 2 bath on 0.6+ acres in Chattanooga, priced in the mid $200s. Want to see it before it's listed? Ask us.",
         ld=["faq:homes", "crumbs"]),
    dict(slug="contact", file="contact.html", crumb="Contact", js=["form"], preload=[],
         title="Contact Us: Call, Text, or Send Details | GLP Home Options",
         desc=f"Call or text {PHONE}, email, book a call, or send a few details. Joey or Ethan will get back to you. No pressure, no obligation.",
         og_title="Let's talk about your home | GLP Home Options",
         og_desc="Call, text, email, or send a few details. You'll talk to Joey or Ethan. No pressure, no scripts.",
         ld=["business", "crumbs"]),
]
for p in PAGES:
    p.setdefault("legal", False)

LEGAL_PAGES = [
    dict(slug="privacy", file=LEGAL.PRIVACY["file"], crumb=None, legal=True, preload=[], ld=[],
         title="Privacy Policy | GLP Home Options", desc=LEGAL.PRIVACY["meta"], data=LEGAL.PRIVACY),
    dict(slug="terms", file=LEGAL.TERMS["file"], crumb=None, legal=True, preload=[], ld=[],
         title="Terms of Service | GLP Home Options", desc=LEGAL.TERMS["meta"], data=LEGAL.TERMS),
]

# The "page not found" page. GitHub Pages shows 404.html for ANY address that does not exist, at any depth (/GLP-Home-Options/a/b/c), so
# its links and files are written from the site's root (see absolutize()). Like the legal pages it has no share card.
EXTRA_PAGES = [
    dict(slug="404", file="404.html", crumb=None, legal=True, preload=[], ld=[], noindex=True,
         title="Page not found | GLP Home Options",
         desc=f"That page isn't here. Start from the home page, or call or text {PHONE} and we'll help.",
         og_title="", og_desc=""),
]

# Pages that exist only when real facts exist. The review page ("Share your experience") is built once a Google review link is typed into
# tools/reviews_data.py; until then there is no review.html at all. It is kept out of search (noindex, even in the launch build), out of the menu and
# out of sitemap.xml: it is the page a thank-you card or a text points to, not a page to find through search.
UTILITY_PAGES = []
if REV.GOOGLE_REVIEW_URL:
    UTILITY_PAGES.append(dict(slug="review", file="review.html", crumb=None, legal=True, preload=[], ld=[], noindex=True,
                              title="Share your experience | GLP Home Options",
                              desc="Thank you for letting Joey and Ethan help. If you would like to, you can share your honest experience on Google. It takes about two minutes.",
                              og_title="", og_desc=""))
OPTIONAL_PAGES = ("review.html",)   # a build deletes these when the facts that justify them are gone, so no stale page stays behind

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
        ("What areas do you serve?",
         "We work in Chattanooga and the surrounding counties, generally within about an hour of the city, in Tennessee and Georgia. We're based in Hixson. Not sure whether your address is in our area? Call or text us and we'll tell you."),
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
         "Not yet. It's coming soon. Want to see it before it's listed? Ask us."),
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
              "Ask us about the home, or about down payment assistance if you're a first-time buyer. You'll talk to Joey or Ethan."),
    "work": ("Let's talk", "Have a house on your mind? <span class=\"ital\">Tell us about it.</span>",
             "You'll talk to Joey or Ethan. We'll listen first, show you every option, and let you decide."),
}

# The closing band's main button says "Get my options" like every other main button; New homes keeps its own (the page is about one home).
CTA_LABEL = {"homes": "Ask about this home"}
# What the form should already have ticked when a visitor arrives from that band's button (tools/form_text.py TOPICS). The bands with no entry leave it open.
CTA_TOPIC = {"homes": "new", "options": "unsure"}

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


def page_url(pg):
    """The address a page names as its own (canonical tag, share card, sitemap, structured data).

    Live: the real domain with no ".html" (/about, /options, /contact ...). Those are the addresses the old site used, every host serves them,
    and Cloudflare Pages even redirects the ".html" form to this one, so a canonical that kept ".html" would fight the host there.
    Preview: the github.io address with its ".html", as before. (Links inside the site keep ".html" so the pages also open from a plain folder.)"""
    if is_home(pg):
        return SITE
    return SITE + (pg["file"][:-len(".html")] if LIVE else pg["file"])


def home_href(pg):
    return "#top" if is_home(pg) else "index.html"


def sec(pg, anchor):
    return f"#{anchor}" if is_home(pg) else f"index.html#{anchor}"


def contact_href(pg, topic=None):
    """Where a button that leads to the form points. On Home and Contact that is the form's own section. From any other page it is the Contact page, and a
    topic (one of tools/form_text.py TOPICS) rides along as ?for=... so the form opens with that choice already made (js/form.js reads it)."""
    if pg["slug"] in ("index", "contact"):
        return "#contact"
    if topic and topic not in dict(FORM.TOPICS):
        sys.exit(f"contact_href: unknown topic {topic!r} (tools/form_text.py TOPICS)")
    return "contact.html" + (f"?for={topic}" if topic else "") + "#contact"


# ------------------------------------------------------------------ shared pieces
def head(pg):
    url = page_url(pg)
    if not LIVE:
        # PREVIEW: nothing here may be indexed, and no page names an address of its own yet
        index_tags = ('<!-- PREVIEW build (LIVE = False in tools/build-pages.py). At launch set LIVE = True and rebuild: noindex goes and the canonical comes. '
                      'See research/launch-checklist.md. -->\n<meta name="robots" content="noindex, nofollow">\n')
    elif pg.get("noindex"):
        index_tags = '<meta name="robots" content="noindex">\n'   # utility pages (page not found, review links) stay out of search even when live
    else:
        index_tags = f'<link rel="canonical" href="{url}">\n'      # live: no robots tag at all means "index, follow"
    pre ="".join(f'<link rel="preload" href="{u}" as="image" fetchpriority="high"{HERO_SET if u.endswith("joey-ethan-bridge.jpg") else ""}>\n' for u in pg["preload"][:1])
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
{index_tags}<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="images/favicon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="images/favicon-96.png">
<link rel="icon" type="image/png" sizes="512x512" href="images/favicon-512.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
{og}<link rel="preload" href="fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{ital}{pre}<script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__glpReady||(document.getElementById('lf')&&!window.__glpForm))document.documentElement.classList.remove('js')}},6000)</script>
<link rel="stylesheet" href="css/site.css?v={CSS_V}">
{ld}</head>'''


def strip_tags(t):
    t = re.sub(r'<span class="vh">.*?</span>', "", t)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()


def address_ld():
    """The structured-data address, written from ADDRESS so the visible line and the markup can never disagree.
    Understands "PO Box 55, Hixson, TN" and "123 Main St, Hixson, TN 37343"; any other shape stops the build until this function is taught it."""
    m = re.fullmatch(r"(?:(?:PO|P\.O\.) Box (\d+)|(.+?)), ([A-Za-z .'-]+), ([A-Z]{2})(?: (\d{5}))?", ADDRESS)
    if not m:
        sys.exit(f"ADDRESS {ADDRESS!r} has a shape the structured data cannot be written from; teach address_ld() in tools/build-pages.py about it")
    box, street, city, state, zip_code = m.groups()
    out = {"@type": "PostalAddress"}
    out.update({"postOfficeBoxNumber": box} if box else {"streetAddress": street})
    out.update({"addressLocality": city, "addressRegion": state})
    if zip_code:
        out["postalCode"] = zip_code
    out["addressCountry"] = "US"
    return out


def ld_blocks(pg):
    out = []
    for key in pg["ld"]:
        if key == "business":
            out.append({
                "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "#business", "name": "GLP Home Options", "legalName": "GL Partners LLC",
                "description": "Chattanooga home options: sell directly with no repairs, list with an agent, keep your home, or another arrangement like seller financing or a lease option. Plus affordable new homes.",
                "telephone": PHONE_LD, "email": EMAIL, "url": SITE,
                "image": SITE + "images/joey-ethan-bridge.jpg", "logo": SITE + "images/glp-mark.png",
                "address": address_ld(),
                "areaServed": [{"@type": "City", "name": "Chattanooga, TN"}, "Counties within about an hour of Chattanooga, in Tennessee and Georgia"],
                "founder": [{"@type": "Person", "name": "Joey"}, {"@type": "Person", "name": "Ethan"}],
                "sameAs": [FB] + ([REV.GOOGLE_PROFILE_URL] if REV.GOOGLE_PROFILE_URL else [])})
        elif key.startswith("faq:"):
            items = FAQ[key[4:]]
            out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(resolve_links(pg, a))}} for q, a in items]})
        elif key == "website":
            # Tells Google the site's name for the line above a result. Name and address only: nothing here a visitor cannot see.
            out.append({"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "#website", "name": "GLP Home Options", "url": SITE,
                        "publisher": {"@id": SITE + "#business"}})
        elif key == "crumbs":
            out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": pg["crumb"], "item": page_url(pg)}]})
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


def carousel(group):
    """A sideways photo strip for one group in tools/gallery_data.py (Home, Checkpoint 47; Jeremy, Oct 27: "don't be afraid to add a carousel").
    The same photos, alt text and captions as the Our work page, so nothing new is claimed. It never moves by itself: a visitor swipes it on a
    phone, or uses the Previous/Next buttons or the arrow keys on a computer. With no JavaScript the strip still scrolls sideways; the buttons
    (added by js/site.js) stay hidden. Photos keep their own shape (no cropping): each one is as tall as the strip and as wide as it needs."""
    items = [g for g in GAL.GALLERY if g["group"] == group]
    if not items:
        sys.exit(f"carousel '{group}': no photos in tools/gallery_data.py")
    out = []
    for g in items:
        w, h = image_size(g["img"])
        out.append(
            f'          <li class="car-slide"><figure><img src="{g["img"]}" alt="{html.escape(g["alt"], quote=True)}" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async"><figcaption>{html.escape(g["caption"])}</figcaption></figure></li>')
    return (f'<div class="car-track" id="car-{group}" role="region" aria-label="Photos from our job sites ({len(items)} photos, scroll sideways for more)" tabindex="0">\n'
            f'        <ul class="car-list">\n' + "\n".join(out) + '\n        </ul>\n      </div>')


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
      <span>{ADDRESS}</span>
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


def proof_block(pg):
    """The "What homeowners say" band: no markup at all until tools/reviews_data.py holds real facts (and, for the average and the public quotes,
    at least MIN_SHOWN reviews). Plain words and plain links: no stars, and no review or rating data for search engines. The rules are in that file."""
    nums = REV.shown_numbers()
    quotes = [q for q in REV.QUOTES if nums or q["source"] == "Direct"][:3]   # public quotes only come with the numbers; at most three, newest first
    if not nums and not quotes:
        return ""
    if nums:
        rating, count, month = nums
        h2 = f'{rating:.1f} on Google, <span class="ital">from {count} review{"" if count == 1 else "s"}.</span>'
        lede = (f'As of {month}. <a href="{html.escape(REV.GOOGLE_PROFILE_URL, quote=True)}" target="_blank" rel="noopener">'
                f'Read every review on Google{NEWTAB}</a>.')
    else:
        h2, lede = 'Notes from <span class="ital">homeowners we helped.</span>', "Shared with the writers\u2019 permission."
    label = {"Google": "Google", "Facebook": "Facebook", "Direct": "Sent to us"}
    cards = []
    for q in quotes:
        who = ", ".join(x for x in (q.get("name", ""), q.get("place", "")) if x)
        when = f'{label[q["source"]]}, {REV.month_label(q["month"])}'
        by = html.escape(f"{who} \u00b7 {when}" if who else when)
        cards.append(f'<li class="proof rv"><p class="q">&ldquo;{html.escape(q["text"], quote=False)}&rdquo;</p><p class="by">{by}</p></li>')
    grid = ""
    if cards:
        grid = f'      <ul class="proofs n{len(cards)}" data-stagger>\n        ' + "\n        ".join(cards) + "\n      </ul>\n"
    notes = []
    g = sum(1 for q in quotes if q["source"] == "Google")
    if g:
        notes.append(f"A selection: {g} of our {REV.GOOGLE_COUNT} Google reviews, quoted exactly.")
    if any(q["source"] == "Direct" for q in quotes):
        notes.append("Notes marked \u201cSent to us\u201d were shared with the writer\u2019s permission.")
    fine = f'      <p class="fine honest mid rv">{" ".join(notes)}</p>\n' if notes else ""
    return f'''  <section class="sec sec-slim" id="reviews" aria-labelledby="reviews-h">
    <div class="wrap">
      <div class="head center rv">
        <h2 id="reviews-h">{h2}</h2>
        <p class="lede">{lede}</p>
      </div>
{grid}{fine}    </div>
  </section>

'''


def faq_list(pg, key):
    out = []
    for i, (q, a) in enumerate(FAQ[key]):
        out.append(f'        <details class="rv"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>')
    return "\n".join(out)


def cta_band(pg, key):
    _label, h2, lede = CTAS[key]   # the first value was the small label above the heading (removed at Checkpoint 47)
    label = CTA_LABEL.get(key, "Get my options")
    topic = CTA_TOPIC.get(key)   # the form opens with this choice already made
    return f'''<section class="cta-band" aria-labelledby="cta-h">
    <div class="cta-bg" aria-hidden="true"><canvas class="topo" data-tone="light"></canvas></div>
    <div class="wrap cta-grid">
      <div class="cta-copy rv">
        <h2 id="cta-h">{h2}</h2>
        <p class="lede">{lede}</p>
      </div>
      <div class="cta-actions rv" data-d="1">
        <a class="btn btn-light btn-lg" href="{contact_href(pg, topic)}"{f' data-topic="{topic}"' if topic else ""}>{label}</a>
        <a class="btn btn-outline-light btn-lg" href="{PHONE_TEL}">{ICON("phone")}<span class="bl">Call or text {PHONE}</span></a>
        <p class="cta-note">No obligation, no spam. Your information is kept confidential.</p>
      </div>
    </div>
  </section>'''


def ask_people():
    """A face and a promise near the top of the Options page (review N25): who answers the phone. Same look as the card on the form."""
    return ('<p class="form-who ask-people"><span class="avs" aria-hidden="true">'
            '<img src="images/joey-avatar.jpg" alt="" width="112" height="112" decoding="async">'
            '<img src="images/ethan-avatar.jpg" alt="" width="112" height="112" decoding="async"></span>'
            '<span><b>Questions? Joey or Ethan will answer.</b><small>Co-founders<span class="sep"> · </span><span class="loc">Hixson, TN</span></small></span></p>')


def reach(page=False, part="main"):
    """The tiles for the other ways to reach us, in two groups: "main" is Call and Text (they sit right under the heading, because the heading and the first
    line say "call or text"), "more" is Email, Book a call and Facebook (they follow the form, or sit under the first group in the wide layout)."""
    # Since Checkpoint 47 nothing fades in (the .rv / "in" classes are kept only as harmless hooks), so every tile paints with the page.
    # Before that, the Contact page's Call and Text tiles were marked "in" so they faded in from the stylesheet alone, without waiting for site.js.
    def tile(i):
        return f'class="reach-item rv in" style="--d:{i}"' if page and i < 2 else 'class="reach-item rv"'
    if part == "main":
        return f'''<div class="reach reach-main" data-stagger>
          <a {tile(0)} href="{PHONE_TEL}">
            <span class="ico" aria-hidden="true">{ICON("phone")}</span>
            <span class="txt"><small>Call</small><b>{PHONE}</b></span><span class="go" aria-hidden="true">Call</span>
          </a>
          <a {tile(1)} href="{PHONE_SMS}">
            <span class="ico" aria-hidden="true">{ICON("sms")}</span>
            <span class="txt"><small>Text</small><b>{PHONE}</b></span><span class="go" aria-hidden="true">Text</span>
          </a>
        </div>'''
    return f'''<div class="reach reach-more" data-stagger>
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


def lead_form(pg, page=False):
    """The contact form: ours, in the site's own look (Checkpoint 46).

    It replaced the GoHighLevel frame, which could not be styled from here, loaded slowly and looked like a bolt-on (DESIGN_SYSTEM 8c). The behavior (checking,
    phone formatting, the ready-made text or email, the endpoint, the thank-you) is js/form.js. Until the form is connected to a place that receives it
    (FORM_ENDPOINT, research/form-wiring.md) the visitor's own text or email app does the sending, and the page says plainly that nothing has been sent yet.
    The two text-message boxes use Joey's exact wording (tools/form_text.py); tools/form-test.py fails if it ever changes.
    Without JavaScript the form cannot work, so the stylesheet hides it and shows a call/text/email card instead (html:not(.js))."""
    hx = "h2" if page else "h3"   # the card's own heading (the section title is the H1 on Contact and an H2 on Home)
    hy = hx   # the heading of a panel that replaces the form once it is sent: the same level as the form's own (the form is hidden while the panel shows)
    lazy = "" if page else ' loading="lazy"'
    pills = "\n".join(f'            <label class="pill"><input type="radio" name="topic" value="{v}"><span>{lab}</span></label>' for v, lab in FORM.TOPICS)
    chans = "\n".join(f'              <label class="pill"><input type="radio" name="channel" value="{v}"><span>{lab}</span></label>' for v, lab in FORM.CHANNELS)
    svc = html.escape(FORM.CONSENT_SERVICE, quote=False)
    mkt = html.escape(FORM.CONSENT_MARKETING, quote=False)
    # What the main button says depends on what it does. With a receiving end it sends ("Send to Joey & Ethan"); without one (today) it only prepares a message the
    # visitor's own app sends, and a button that says "Send" would let people believe it had gone (review of Oct 26: the likeliest way to lose a lead today).
    send_label = "Send to Joey &amp; Ethan" if FORM_ENDPOINT else "Get my message ready"
    return f'''<div class="form-card rv{' in" style="--d:2' if page else ''}" data-d="2">
        <p class="form-who"><span class="avs" aria-hidden="true"><img src="images/joey-avatar.jpg" alt="" width="112" height="112"{lazy} decoding="async"><img src="images/ethan-avatar.jpg" alt="" width="112" height="112"{lazy} decoding="async"></span><span><b>Joey &amp; Ethan</b><small>Co-founders<span class="sep"> · </span><span class="loc">Hixson, TN</span></small></span></p>
        <div class="lf-wrap">
          <form class="lf" id="lf" novalidate method="post" onsubmit="return false" data-endpoint="{FORM_ENDPOINT}" data-format="{FORM_FORMAT}" data-consent-version="{FORM.consent_version()}" data-sms="{PHONE_SMS}" data-mail="{EMAIL}" aria-labelledby="lf-h">
            <div class="lf-head">
              <{hx} class="h3" id="lf-h">Thinking about selling, or not sure yet?</{hx}>
              <p class="sub">Joey or Ethan will get back to you. There's no obligation, and only your name and phone number are required.</p>
            </div>
            <div class="lf-sum" id="lf-sum" tabindex="-1" hidden></div>
            <fieldset class="lf-pills">
              <legend>What can we help with? <span class="lf-opt">(optional)</span></legend>
              <div class="lf-pillrow">
{pills}
              </div>
            </fieldset>
            <div class="field" data-f="name">
              <label for="lf-name">Your name</label>
              <div class="input"><input id="lf-name" name="name" type="text" autocomplete="name" autocapitalize="words" enterkeyhint="next" spellcheck="false" maxlength="80" required aria-describedby="lf-name-err"></div>
              <p class="lf-err" id="lf-name-err" hidden></p>
            </div>
            <div class="field" data-f="phone">
              <label for="lf-phone">Phone number</label>
              <div class="input"><input id="lf-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" enterkeyhint="done" maxlength="24" required aria-describedby="lf-phone-err lf-phone-hint"></div>
              <p class="lf-err" id="lf-phone-err" hidden></p>
              <p class="hint" id="lf-phone-hint">So Joey or Ethan can reach you about your request.</p>
            </div>
            <details class="lf-more" id="lf-more">
              <summary><span class="lf-more-t">Add an email, your address, or a note</span><span class="lf-opt">optional</span></summary>
              <div class="lf-more-body">
                <div class="field" data-f="email">
                  <label for="lf-email">Email address</label>
                  <div class="input"><input id="lf-email" name="email" type="email" inputmode="email" autocomplete="email" autocapitalize="off" enterkeyhint="next" spellcheck="false" maxlength="120" aria-describedby="lf-email-err"></div>
                  <p class="lf-err" id="lf-email-err" hidden></p>
                </div>
                <fieldset class="lf-pills lf-chan">
                  <legend>Best way to reach you</legend>
                  <div class="lf-pillrow">
{chans}
                  </div>
                </fieldset>
                <div class="field" data-f="address">
                  <label for="lf-address">Home address or ZIP code</label>
                  <div class="input"><input id="lf-address" name="address" type="text" autocomplete="address-line1" enterkeyhint="next" maxlength="120" aria-describedby="lf-address-hint"></div>
                  <p class="hint" id="lf-address-hint">Helps us look up your home before we talk. Leave it blank if you'd rather talk first.</p>
                </div>
                <div class="field" data-f="message">
                  <label for="lf-message">Anything else you'd like us to know?</label>
                  <textarea id="lf-message" name="message" rows="4" maxlength="600" aria-describedby="lf-message-hint"></textarea>
                  <p class="hint" id="lf-message-hint">What's going on, what you're hoping for, or a good time to reach you. Up to 600 characters.</p>
                </div>
              </div>
            </details>
            <div class="lf-hp vh" aria-hidden="true"><label for="lf-web">Website</label><input id="lf-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
            <fieldset class="lf-consent">
              <legend>Text messages <span class="lf-opt">(optional)</span></legend>
              <div class="lf-checks">
                <label class="check"><input type="checkbox" name="consent_service" value="yes"><span>{svc}</span></label>
                <label class="check"><input type="checkbox" name="consent_marketing" value="yes"><span>{mkt}</span></label>
              </div>
            </fieldset>
            <div class="lf-go">
              <button class="btn btn-primary btn-lg lf-send" type="submit"><span class="lf-send-t">{send_label}</span></button>
              <p class="lf-status vh" id="lf-status" role="status" aria-live="polite"></p>
              <p class="lf-note">No obligation, no spam. Your information is kept confidential.</p>
              <p class="lf-legal"><a href="privacy-policy.html" target="_blank" rel="noopener">Privacy Policy{NEWTAB}</a><span class="dot" aria-hidden="true"> · </span><a href="terms-of-service.html" target="_blank" rel="noopener">Terms of Service{NEWTAB}</a></p>
            </div>
          </form>

          <div class="lf-panel lf-hand" id="lf-hand" role="region" aria-labelledby="lf-hand-h" tabindex="-1" hidden>
            <span class="lf-badge" aria-hidden="true">{ICON("sms")}</span>
            <{hy} class="h3" id="lf-hand-h">Your message is ready to send</{hy}>
            <p class="lf-lede" id="lf-lede-sms" data-v="sms">Nothing has been sent yet. Press &ldquo;Text it to Joey &amp; Ethan&rdquo;, then press Send in your messages app, and it goes straight to Joey and Ethan. If nothing opens, press &ldquo;Copy my message&rdquo; below and paste it into a text, or call us.</p>
            <p class="lf-lede" id="lf-lede-mail" data-v="mail" hidden>Nothing has been sent yet. Press &ldquo;Email it to Joey &amp; Ethan&rdquo;, then press Send in your email app, and it goes straight to Joey and Ethan. If nothing opens, press &ldquo;Copy my message&rdquo; below and paste it into an email, or call us.</p>
            <p class="lf-lede" id="lf-lede-fail" data-v="fail" hidden>Your details are still here. To be sure Joey and Ethan get them, send them by text or email instead, or call <a class="nb ph" href="{PHONE_TEL}">{PHONE}</a> and we'll take it from there.</p>
            <div class="lf-actions">
              <a class="btn btn-primary btn-lg" id="lf-sms" href="{PHONE_SMS}">{ICON("sms")}<span id="lf-sms-t">Text it to Joey &amp; Ethan</span></a>
              <a class="btn btn-ghost btn-lg" id="lf-mail" href="mailto:{EMAIL}">{ICON("mail")}<span id="lf-mail-t">Or email it instead</span></a>
            </div>
            <div class="lf-msgbox"><p class="lf-msg-l" id="lf-msg-l">Here's what it says</p><pre class="lf-msg" id="lf-msg" translate="no"></pre></div>
            <ul class="lf-mini">
              <li><button type="button" id="lf-copy">{ICON("copy")}Copy my message</button></li>
              <li><button type="button" id="lf-edit">{ICON("edit")}Change my details</button></li>
              <li><a href="{PHONE_TEL}">{ICON("phone")}<span>Call {PHONE}</span></a></li>
            </ul>
            <p class="lf-live" id="lf-live" role="status" aria-live="polite"></p>
          </div>

          <div class="lf-panel lf-done" id="lf-done" role="region" aria-labelledby="lf-done-h" tabindex="-1" hidden>
            <span class="lf-badge ok" aria-hidden="true">{ICON("check", "i lf-tick")}</span>
            <{hy} class="h3" id="lf-done-h">Thank you<span id="lf-first"></span>.</{hy}>
            <p class="lf-lede">We have your details, and Joey or Ethan will be in touch. If it can't wait, call or text <a class="nb ph" href="{PHONE_TEL}">{PHONE}</a>.</p>
            <ul class="lf-mini">
              <li><button type="button" id="lf-again">{ICON("edit")}Send another message</button></li>
            </ul>
          </div>
        </div>

        <div class="lf-nojs">
          <p class="lf-nojs-h">The form isn't available right now.</p>
          <p class="lf-nojs-p">Call or text us instead and we'll take it from there.</p>
          <div class="lf-nojs-btns">
            <a class="btn btn-primary" href="{PHONE_TEL}">{ICON("phone")}<span class="bl">Call {PHONE}</span></a>
            <a class="btn btn-ghost" href="{PHONE_SMS}">{ICON("sms")}Text us</a>
          </div>
          <p class="lf-nojs-alt"><a href="mailto:{EMAIL}">Email us</a></p>
        </div>
        <p class="form-alt">Prefer to talk? Call or text <a class="nb ph" href="{PHONE_TEL}">{PHONE}</a>, or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </div>'''


def contact_section(pg, page=False):
    if page:
        top = f'''{crumbs(pg)}
          <h1 id="contact-h">Let's talk. <span class="ital">No pressure, no scripts.</span></h1>'''
    else:
        top = '''<h2 id="contact-h">Want to talk it through? <span class="ital">Call or text Joey or Ethan.</span></h2>'''
    # On the Contact page the H1 sits directly above these two headings, so they are H2s there
    # (looks identical: the .h3 class carries the H3 styling). On the home page the section title is an H2, so H3 is right.
    hx = "h2" if page else "h3"
    # The order here is the reading order AND the tab order: heading, Call and Text (the heading and the first line say "call or text"), the form, then
    # Email, Book a call and Facebook, then what happens next. On a phone that is one column, so the form follows the two tiles at once instead of a full
    # screen of them; from 60em up the stylesheet puts the form in the right-hand column and the tiles and steps in the left.
    # Checkpoint 47: on Home the three steps already appear higher up (How it works), so phones skip this list there (.next-home); on wide screens
    # it stays beside the form so the left column does not end halfway down it
    next_steps = f'''      <div class="next{"" if page else " next-home"} rv">
        <{hx} class="h3">What happens next?</{hx}>
        <ol>
          <li><span class="num" aria-hidden="true">1</span>We talk through your situation.</li>
          <li><span class="num" aria-hidden="true">2</span>We go over your options together.</li>
          <li><span class="num" aria-hidden="true">3</span>You decide what's best for you.</li>
        </ol>
      </div>'''
    # Checkpoint 48: on the Contact page at desktop width the left column ended about 690 px above the bottom of the form; the photo of the two people
    # a visitor will talk to fills it (the same photo and words as the Home hero, nothing new claimed). Phones and tablets never download it (hidden
    # there and marked lazy); on a computer it sits near the first screen, so the browser fetches it with the page.
    photo = '''
      <figure class="contact-photo rv">
        <img src="images/joey-ethan-bridge.jpg" srcset="images/joey-ethan-bridge.jpg 800w, images/joey-ethan-bridge-1200.jpg 1200w" sizes="(min-width:60.0625em) 540px, 1px" alt="Joey and Ethan, co-founders of GLP Home Options, smiling on the Walnut Street Bridge in Chattanooga" width="800" height="636" loading="lazy" decoding="async">
        <figcaption><b>Joey &amp; Ethan</b><span>Co-founders, Hixson, TN</span></figcaption>
      </figure>''' if page else ""
    return f'''<section class="contact{" contact-page" if page else ""}" id="contact" aria-labelledby="contact-h">
    <div class="contact-bg" aria-hidden="true"><canvas class="topo" data-tone="light"></canvas></div>
    <div class="wrap contact-grid">
      <div class="contact-top{"" if page else " rv"}">
        {top}
        <p class="lede">Call or text anytime, or send a few details. You'll talk to Joey or Ethan, and your information stays&nbsp;confidential.</p>
      </div>

      {reach(page, "main")}

      {lead_form(pg, page)}

      {reach(page, "more")}

{next_steps}{photo}
    </div>
  </section>'''


def resolve_links(pg, text):
    nh = NEW_HOMES
    text = re.sub(r"\[\[contact-href ([a-z]+)\]\]", lambda m: contact_href(pg, m.group(1)), text)   # [[contact-href sell]]: the same link, with the form's topic
    return (text.replace("[[home]]", "" if is_home(pg) else "index.html")
                .replace("[[contact-href]]", contact_href(pg))
                .replace("[[new-homes-href]]", nh)
                .replace("[[fb]]", FB))


def expand(pg, text):
    block = proof_block(pg)   # "" until real review facts exist; then [[proof]], alone on its line, becomes the band (and its line vanishes when empty)
    text = re.sub(r"^[ \t]*\[\[proof\]\][ \t]*\n", lambda m: block, text, flags=re.M)

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
        if tok.startswith("carousel "):
            return carousel(tok.split(" ", 1)[1])
        if tok == "phone":
            return PHONE
        if tok == "tel":
            return PHONE_TEL
        if tok == "sms":
            return PHONE_SMS
        if tok == "email":
            return EMAIL
        if tok == "address":
            return ADDRESS
        if tok == "review-url":
            return html.escape(REV.GOOGLE_REVIEW_URL, quote=True)
        if tok == "newtab":
            return NEWTAB
        if tok == "ask-people":
            return ask_people()
        if tok == "contact home":
            return contact_section(pg, page=False)
        if tok == "contact page":
            return contact_section(pg, page=True)
        return m.group(0)
    text = re.sub(r"\[\[([^\]]+)\]\]", sub, text)
    return resolve_links(pg, text)


def scripts(pg):
    s = ""
    # if site.js fails to load, drop the "js" class at once so no section stays hidden waiting for it (the head also has a 6 s safety timer)
    s += f'<script src="js/site.js?v={JS_V}" defer onerror=\'document.documentElement.classList.remove("js")\'></script>'
    for name in pg.get("js", []):   # scripts only one page needs (the Our work photo viewer, the contact form)
        # the form cannot work without its script, so if that fails to load the page drops its "js" class at once: the form gives way to the call/text/email card
        s += f'\n<script src="js/{name}.js?v={JS_V}" defer' + (' onerror=\'document.documentElement.classList.remove("js")\'' if name == "form" else "") + '></script>'
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


BASE = urlsplit(SITE).path or "/"   # "/GLP-Home-Options/" on the preview address, "/" on the real domain (it follows SITE)
URL_ATTR = re.compile(r'\b(href|src)="([^"]*)"')
NOT_RELATIVE = ("#", "/", "http:", "https:", "mailto:", "tel:", "sms:", "data:", "javascript:")


def absolutize(page):
    """Writes every relative link and file in a page from the site's root: "css/site.css" becomes "/GLP-Home-Options/css/site.css".
    Only for the 404 page, which can be shown at any depth. Left alone: in-page "#" links (the icon sprite uses them), full web
    addresses, mailto/tel/sms, scripts' and styles' contents. Guard: taking the prefix off again must give back exactly the input."""
    def fix(m):
        v = m.group(2)
        return m.group(0) if not v or v.startswith(NOT_RELATIVE) else f'{m.group(1)}="{BASE}{v}"'
    out = []
    for m in TOKENS.finditer(page):
        tok = m.group(0)
        if tok.startswith("<script"):
            end = tok.index(">") + 1
            tok = URL_ATTR.sub(fix, tok[:end]) + tok[end:]
        elif tok.startswith("<") and not tok.startswith(("<style", "<!--")):
            tok = URL_ATTR.sub(fix, tok)
        out.append(tok)
    res = "".join(out)
    if re.sub(r'\b(href|src)="' + re.escape(BASE), r'\1="', res) != page:
        sys.exit("absolutize(): it changed something other than link prefixes; the page was not written")
    return res


NOBREAK = re.compile(re.escape(PHONE) + "|short-term")


def nobreak(page):
    """Keeps the phone number (and the word "short-term") on one line, whatever the screen width or text size (review N26, N31).

    Every occurrence inside running text is wrapped: "short-term" in <span class="nb"> (white-space: nowrap), the phone number in
    <span class="nb ph"> (a small inline block: it moves to the next line whole, and only when even a full line is too narrow for it, which
    is a small phone with the text blown up to 150% or more, does it wrap at its one space instead of running off the screen).
    Left alone: tags and attributes, scripts, styles, comments, the <title>, and anything already inside an .nb element.
    (The contact tiles and the footer link are wrapped too, and the stylesheet lets them wrap as they always did.)
    Guard: taking the wrappers out again must give back exactly the input."""
    out, prev, in_title = [], "", False
    for m in TOKENS.finditer(page):
        tok = m.group(0)
        if tok.startswith("<"):
            if tok.startswith("<title"):
                in_title = True
            elif tok.startswith("</title"):
                in_title = False
            if not tok.startswith(("<script", "<style", "<!--")):
                prev = tok
            out.append(tok)
            continue
        if in_title or not NOBREAK.search(tok) or re.search(r'class="[^"]*\bnb\b', prev):
            out.append(tok)
            continue
        out.append(NOBREAK.sub(lambda x: f'<span class="nb{" ph" if x.group(0) == PHONE else ""}">{x.group(0)}</span>', tok))
    res = "".join(out)
    strip = lambda s: re.sub(r'<span class="nb(?: ph)?">(' + NOBREAK.pattern + r")</span>", r"\1", s)  # noqa: E731
    if strip(res) != strip(page):
        sys.exit("nobreak(): it changed something other than the wrappers; the page was not written")
    return res


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


# Old addresses of the previous site that no longer have a page of their own: {old path: where it goes now}.
# GitHub Pages cannot send a real "moved permanently" answer, so each one gets a small page that jumps straight to the new place (Google treats a
# zero-second jump as permanent); hosts that can (Netlify, Cloudflare Pages) also read the _redirects file. Add a line here for any other old address.
REDIRECTS = {"calculator": "/#netsheet"}
SITE_FILES = ("sitemap.xml", "robots.txt", "CNAME", "_redirects") + tuple(f"{old}.html" for old in REDIRECTS)   # written only by a LIVE build; a preview build removes them


def redirect_stub(target):
    """A tiny page that sends the visitor (and Google) to `target`, a path on this site such as "/#netsheet"."""
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>One moment | GLP Home Options</title>\n<link rel="canonical" href="{SITE}">\n'
            f'<meta http-equiv="refresh" content="0; url={target}">\n<script>location.replace({json.dumps(target)})</script>\n</head>\n'
            f'<body>\n<p>Taking you to the right page. If nothing happens, <a href="{target}">tap here</a>.</p>\n</body>\n</html>\n')


def site_files():
    """The small files only the launch needs, as {name: text}. Empty in a preview build.

    sitemap.xml  every page that may be searched (not the page-not-found page or any page marked noindex), at the address it names as its own.
                 No <lastmod>: a date that is wrong is worse than none, and Google treats it as optional.
    robots.txt   everyone may crawl; says where the sitemap is. (A page is kept out of search with its noindex tag, never with a Disallow line:
                 a crawler that may not fetch a page can never see the tag.)
    CNAME        tells GitHub Pages which domain this site answers to. Without it the real domain would not open the site.
    _redirects   the same moves as the stubs, in the form Netlify and Cloudflare Pages read (GitHub Pages ignores the file).
    <old>.html   one stub per entry in REDIRECTS (see above).
    """
    if not LIVE:
        return {}
    urls = [page_url(p) for p in PAGES + LEGAL_PAGES + EXTRA_PAGES + UTILITY_PAGES if not p.get("noindex")]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\n" for u in urls) + "</urlset>\n")
    robots = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n"
    files = {"sitemap.xml": sitemap, "robots.txt": robots, "CNAME": urlsplit(REAL).netloc + "\n",
             "_redirects": "".join(f"/{old}  {new}  301\n" for old, new in REDIRECTS.items())}
    for old, new in REDIRECTS.items():
        files[f"{old}.html"] = redirect_stub(new)
    return files


def main():
    for pg in PAGES:
        src = (TOOLS / "pages" / f"{pg['slug']}.html").read_text(encoding="utf-8")
        out = nobreak(curly(render(pg, expand(pg, src))))
        left = re.findall(r"\[\[[^\]]+\]\]", out)
        if left:
            sys.exit(f"{pg['file']}: unresolved tokens {left}")
        (ROOT / pg["file"]).write_text(out, encoding="utf-8")
        print("wrote", pg["file"], f"({len(out) // 1024} KB)")
    for pg in EXTRA_PAGES:
        src = (TOOLS / "pages" / f"{pg['slug']}.html").read_text(encoding="utf-8")
        out = absolutize(nobreak(curly(render(pg, expand(pg, src)))))
        left = re.findall(r"\[\[[^\]]+\]\]", out)
        if left:
            sys.exit(f"{pg['file']}: unresolved tokens {left}")
        (ROOT / pg["file"]).write_text(out, encoding="utf-8")
        print("wrote", pg["file"], f"({len(out) // 1024} KB)")
    for pg in UTILITY_PAGES:
        src = (TOOLS / "pages" / f"{pg['slug']}.html").read_text(encoding="utf-8")
        out = nobreak(curly(render(pg, expand(pg, src))))
        left = re.findall(r"\[\[[^\]]+\]\]", out)
        if left:
            sys.exit(f"{pg['file']}: unresolved tokens {left}")
        (ROOT / pg["file"]).write_text(out, encoding="utf-8")
        print("wrote", pg["file"], f"({len(out) // 1024} KB)")
    built_names = {pg["file"] for pg in UTILITY_PAGES}
    for name in OPTIONAL_PAGES:
        if name not in built_names and (ROOT / name).exists():
            (ROOT / name).unlink()   # the facts for this page were removed from tools/reviews_data.py
            print("removed", name, "(its facts are gone from tools/reviews_data.py)")
    for pg in LEGAL_PAGES:
        out = nobreak(curly(render(pg, expand(pg, legal_main(pg["data"])))))   # expand() fills the business-detail tokens in the legal wording
        left = re.findall(r"\[\[[^\]]+\]\]", out)
        if left:
            sys.exit(f"{pg['file']}: unresolved tokens {left}")
        (ROOT / pg["file"]).write_text(out, encoding="utf-8")
        print("wrote", pg["file"], f"({len(out) // 1024} KB)")
    files = site_files()
    for name in SITE_FILES:
        path = ROOT / name
        if name in files:
            path.write_text(files[name], encoding="utf-8", newline="\n")
            print("wrote", name)
        elif path.exists():
            path.unlink()   # a preview build never leaves a launch file behind (a CNAME would take the preview address offline)
            print("removed", name, "(preview build)")
    print(("LIVE build: the real domain" if LIVE else "PREVIEW build: every page says noindex")
          + ("  (GLP_BUILD is set in this shell and overrides LIVE in this file)" if os.environ.get("GLP_BUILD") else ""))


if __name__ == "__main__":
    main()

"""Real review facts. The ONE place they go. Everything here is EMPTY on purpose.

GLP Home Options has no Google listing and no reviews yet (the Facebook page says "Not yet rated, 0 reviews"). Until a real value is typed here:
  - no review page is built, and no review link, rating, count or quote appears anywhere on the site;
  - nothing about reviews is added to the search data (Google shows no stars for a business's own reviews, so that markup could only add risk).

Read research/review-kit.md first. After typing anything here, in this order:
  python3 tools/reviews-check.py   checks the facts below against the rules, then builds a throwaway copy to prove the pages still hold up
  python3 tools/build-pages.py     refuses to build if the facts below break a rule (problems() below)
  python3 tools/claims-check.py    a shown rating or review count is a claim: it fails until a line in tools/claims-allow.txt says it is real
                                   (that line is the human "yes": who looked, when, and where the proof is kept). It cannot judge a quote:
                                   the `permission` line in QUOTES (below) and a person's look at the public review do that
Then re-check the two numbers on the real listing every month and change CHECKED; `python3 tools/reviews-check.py` warns when it is old.

The rules (each one is checked below or by reviews-check.py; the sources are in the private research report and research/review-kit.md):
  - Real only. A rating, a count or a quote is copied from the public listing or from a note someone sent us. Nothing is typed from memory or rounded up.
  - Everyone is asked the same way (the review link is the same for every customer); the page never filters by stars and nothing is given in return.
  - A quote is quoted exactly (shortened only with a visible ellipsis), says where it came from and the month, and is labeled a selection ("3 of 14").
  - A first name or a town is shown only if that person said yes. A review by an owner, relative, employee or business partner is never shown as a customer's.
  - No star markup, no AggregateRating or Review data on any page. The numbers are plain text for visitors, not for search results.
"""
import datetime
import re
from urllib.parse import urlsplit

# The link people tap to WRITE a review. Copy it exactly as the Google Business Profile gives it (Read reviews > "Get more reviews"); many guides show
# it as https://g.page/r/ABC123xyz/review but Google's own pages do not show its shape, so test it on a phone first. While this is empty, no review page is built.
GOOGLE_REVIEW_URL = ""

# The public listing: what "Read every review on Google" opens, and a link that tells search engines this site and that listing are the same business.
GOOGLE_PROFILE_URL = ""

# The average and the number of Google reviews, EXACTLY as the public listing shows them today (for example 4.9 and 14), and the day you read them.
GOOGLE_RATING = None
GOOGLE_COUNT = None
CHECKED = ""            # "2027-03-02": shown as "As of March 2027". Re-check the listing every month.

# The average and the count are shown only from this many reviews up. Two or three reviews are honest but prove little, and a 5.0 from two people
# reads as thin. Joey decides the number; below it the page shows no rating at all.
MIN_SHOWN = 5

# Chosen real reviews and thank-you notes, newest first. Empty until there are real ones. One example, commented out:
#
# QUOTES = [
#     dict(text="Exactly what they wrote, word for word. Shorten only with a visible ellipsis …",
#          source="Google",        # "Google" (a public review), "Facebook" (a public recommendation) or "Direct" (a note they sent us)
#          month="2027-03",        # the month they wrote it
#          name="Pat",             # a first name or an initial; leave "" unless they said yes to it being shown
#          place="Hixson",         # a neighborhood or town; leave "" unless they said yes
#          permission="Public Google review; screenshot saved 2027-03-02 with the closing papers",   # what we hold. For "Direct": their written yes
#          insider=False),         # True if the writer is an owner, a relative, an employee or a business partner: such items are refused
# ]
QUOTES = []

SOURCES = ("Google", "Facebook", "Direct")
# Hosts a Google review or listing link may use. Anything else is refused: a typo here would send a thank-you card to the wrong place.
GOOGLE_HOSTS = ("g.page", "search.google.com", "www.google.com", "google.com", "maps.google.com", "maps.app.goo.gl", "goo.gl")
MAX_QUOTE = 420


def _bad_url(url, what):
    u = urlsplit(url)
    if u.scheme != "https" or u.netloc.lower() not in GOOGLE_HOSTS or len(url) < 20:
        return f"{what} must be a full https link on Google (for example https://g.page/r/ABC123xyz/review), not {url!r}"
    return None


def shown_numbers():
    """(rating, count, month label) when the average and count may be shown, else None."""
    if GOOGLE_RATING is None or GOOGLE_COUNT is None or GOOGLE_COUNT < MIN_SHOWN:
        return None
    month = datetime.date.fromisoformat(CHECKED)
    return GOOGLE_RATING, GOOGLE_COUNT, month.strftime("%B %Y")


def month_label(ym):
    return datetime.date.fromisoformat(ym + "-01").strftime("%B %Y")


def problems():
    """Every rule the facts above break, as plain sentences. The builder stops if this is not empty. It never looks at today's date, so a build
    that worked yesterday works tomorrow; staleness is reviews-check.py's job."""
    out = []
    for url, what in ((GOOGLE_REVIEW_URL, "GOOGLE_REVIEW_URL"), (GOOGLE_PROFILE_URL, "GOOGLE_PROFILE_URL")):
        if url:
            msg = _bad_url(url, what)
            if msg:
                out.append(msg)
    if (GOOGLE_RATING is None) != (GOOGLE_COUNT is None):
        out.append("GOOGLE_RATING and GOOGLE_COUNT go together: type both, or neither")
    if GOOGLE_RATING is not None:
        if not isinstance(GOOGLE_RATING, (int, float)) or not 1.0 <= GOOGLE_RATING <= 5.0 or round(GOOGLE_RATING, 1) != GOOGLE_RATING:
            out.append(f"GOOGLE_RATING must be an average from 1.0 to 5.0 with one decimal, as the listing shows it (got {GOOGLE_RATING!r})")
        if not isinstance(GOOGLE_COUNT, int) or isinstance(GOOGLE_COUNT, bool) or GOOGLE_COUNT < 1:
            out.append(f"GOOGLE_COUNT must be a whole number of 1 or more, as the listing shows it (got {GOOGLE_COUNT!r})")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", CHECKED or ""):
            out.append("CHECKED must be the day you read the rating and count off the listing, like 2027-03-02")
        else:
            try:
                datetime.date.fromisoformat(CHECKED)
            except ValueError:
                out.append(f"CHECKED is not a real date ({CHECKED!r})")
        if not GOOGLE_PROFILE_URL:
            out.append("a rating needs GOOGLE_PROFILE_URL, so every visitor can open the listing and read the reviews for themselves")
    if not isinstance(MIN_SHOWN, int) or MIN_SHOWN < 1:
        out.append("MIN_SHOWN must be a whole number of 1 or more")
    google = 0
    for i, q in enumerate(QUOTES, 1):
        who = f"QUOTES item {i}"
        if not isinstance(q, dict):
            out.append(f"{who} must be a dict like the example at the top of this file")
            continue
        unknown = set(q) - {"text", "source", "month", "name", "place", "permission", "insider"}
        if unknown:
            out.append(f"{who} has unknown keys {sorted(unknown)}")
        text = q.get("text", "")
        if not isinstance(text, str) or not text.strip():
            out.append(f"{who}: text is empty")
        elif len(text) > MAX_QUOTE:
            out.append(f"{who}: text is {len(text)} characters (over {MAX_QUOTE}); shorten it with a visible ellipsis, never by rewording")
        elif "\n" in text or "<" in text or ">" in text:
            out.append(f"{who}: text has line breaks or markup; type it as plain words")
        if q.get("source") not in SOURCES:
            out.append(f"{who}: source must be one of {SOURCES}")
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", q.get("month", "") or ""):
            out.append(f"{who}: month must look like 2027-03")
        if not (q.get("permission") or "").strip():
            out.append(f"{who}: permission says what we hold (a saved screenshot of the public review, or their written yes for a note) and is empty")
        if q.get("insider") is not False:
            out.append(f"{who}: insider must be False. A review by an owner, relative, employee or business partner is never shown as a customer's")
        if q.get("source") == "Google":
            google += 1
    if google:
        if GOOGLE_COUNT is None:
            out.append("Google quotes need GOOGLE_COUNT, because a quote is labeled a selection (for example 3 of 14)")
        elif google > GOOGLE_COUNT:
            out.append(f"{google} Google quotes but GOOGLE_COUNT is {GOOGLE_COUNT}")
    return out

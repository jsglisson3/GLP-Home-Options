#!/usr/bin/env python3
"""How easy is each page to read?  (a yardstick for the plain-talk pass; it changes nothing)

Run:   python3 tools/readability.py            all 8 pages
       python3 tools/readability.py options    one page (name without .html)
       python3 tools/readability.py --words    also list the hard or "industry" words found on each page

For each page it reads the text inside <main> (not the menu, footer, scripts or the hidden structured data) and prints:
  words, sentences, average words per sentence, Flesch Reading Ease (higher is easier; 60-70 is plain English),
  Flesch-Kincaid grade (US school grade; 8 or lower is a good target for this audience), and how many jargon words
  from the list below appear.  Syllables are counted by a simple rule, so the numbers are a *yardstick* (compare before
  and after), not an exact score.  Short labels, button text and table rows are skipped when they are not sentences (under 6 words,
  or under 4 words that do not end with a full stop, question mark or exclamation mark), so they do not distort the average.
"""
import html, pathlib, re, sys

import _site  # finds the pages

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = _site.page_slugs()   # every page in the folder

# words an ordinary homeowner may not use every day; each needs a plain word or a short explanation in the same sentence
JARGON = [
    "mls", "equity", "carrying costs", "carrying cost", "as-is", "off-market", "title company", "escrow", "contingency", "contingencies",
    "proceeds", "net proceeds", "payoff", "closing costs", "commission", "leverage", "liquidity", "appraisal", "assignment", "wholesal",
    "seller financing", "lease option", "refinanc", "foreclos", "probate", "lien", "arm's length", "fair market value", "market value",
    "comps", "due diligence", "earnest money", "capital gains", "amortiz", "underwater", "short sale", "turnkey", "fiduciary",
]


def main_text(fn):
    s = (ROOT / f"{fn}.html").read_text(encoding="utf-8")
    m = re.search(r"<main.*?</main>", s, re.S)
    t = m.group(0) if m else s
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<noscript.*?</noscript>", " ", t, flags=re.S)
    t = re.sub(r"<(br|/p|/h\d|/li|/div|/section|/tr|/td|/th|/dt|/dd|/summary|/button|/figcaption|/label|/legend)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", " - ")
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in t.split("\n")]
    return [ln for ln in lines if ln]


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def analyse(fn, show_words=False):
    lines = main_text(fn)
    sentences, words_all = [], 0
    for ln in lines:
        ws = re.findall(r"[A-Za-z][A-Za-z'\-]*|\d[\d,\.]*", ln)
        words_all += len(ws)
        # a label, a button, a price or a table row is not prose: keep a line only if it has 6+ words, or 4+ words and ends like a sentence
        if len(ws) < 4 or (len(ws) < 6 and not re.search(r"[.!?]['\")]*$", ln)):
            continue
        # split a line into sentences on . ! ? followed by a space and a capital letter or a quote
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z\"'(])", ln):
            pw = re.findall(r"[A-Za-z][A-Za-z'\-]*|\d[\d,\.]*", part)
            if len(pw) >= 3:
                sentences.append(pw)
    nwords = sum(len(s) for s in sentences)
    nsent = max(1, len(sentences))
    syl = sum(syllables(w) for s in sentences for w in s if re.match(r"[A-Za-z]", w))
    alpha = max(1, sum(1 for s in sentences for w in s if re.match(r"[A-Za-z]", w)))
    wps = nwords / nsent
    spw = syl / alpha
    fre = 206.835 - 1.015 * wps - 84.6 * spw
    fk = 0.39 * wps + 11.8 * spw - 15.59
    blob = " " + " ".join(lines).lower() + " "
    hits = {}
    for j in JARGON:
        n = len(re.findall(r"(?<![a-z])" + re.escape(j), blob))
        if n:
            hits[j] = n
    longest = sorted(sentences, key=len, reverse=True)[:3]
    return dict(page=fn, words=words_all, sentences=nsent, wps=wps, fre=fre, fk=fk, jargon=hits, longest=[" ".join(s) for s in longest])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show = "--words" in sys.argv
    pages = args or PAGES
    print(f"{'page':<18}{'words':>6}{'sent.':>7}{'w/sent':>8}{'ease':>7}{'grade':>7}  jargon words")
    tot_w = tot_s = 0
    for p in pages:
        r = analyse(p, show)
        tj = sum(r["jargon"].values())
        print(f"{r['page']:<18}{r['words']:>6}{r['sentences']:>7}{r['wps']:>8.1f}{r['fre']:>7.0f}{r['fk']:>7.1f}  {tj}")
        if show:
            if r["jargon"]:
                print("    jargon:", ", ".join(f"{k} x{v}" for k, v in sorted(r["jargon"].items(), key=lambda kv: -kv[1])))
            for s in r["longest"]:
                print("    long  :", s[:230] + ("..." if len(s) > 230 else ""))
    print("\nease: 60-70 = plain English, 70+ = easy.  grade: US school grade (8 or lower is the target).  Syllables are estimated, so use it to compare before and after.")


if __name__ == "__main__":
    main()

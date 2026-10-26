#!/usr/bin/env python3
"""Claims check: guards the standing rule "never invent reviews, licenses, years in business,
awards, results or business claims we cannot verify" (see CONTENT_CLAIMS.md).

It reads the 7 built pages (visible text, image alt text, page titles, meta descriptions and
the JSON-LD structured data) and looks for words that usually mean a credential, a rating or a
result. Each hit must be covered by a line in tools/claims-allow.txt (a short piece of the
surrounding text and the reason it is fine); otherwise the check fails.

It also prints, for a human to eyeball, how often "soft" claims appear (free, anytime, no fees,
cash offer, seller financing ...). Those are tracked in CONTENT_CLAIMS.md; the counts are a reminder.

Usage:  python3 tools/claims-check.py            (run from the project root)
Exit code 0 = clear, 1 = something needs a decision.
"""
import glob
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HARD = [
    ("credential", r"\b(licen[sc]ed|licen[sc]es?|insured|bonded|certified|accredited)\b"),
    ("award", r"\baward[- ]?winning\b|\bawards?\b"),
    ("rating", r"\b(rated|ratings?|stars?)\b|aggregateRating|reviewCount|ratingValue"),
    ("testimonial", r"\btestimonials?\b"),
    ("customer reviews", r"\b(customer|client|seller|buyer|google|5-star|five-star|verified) reviews?\b"),
    ("rating shown", r"\b\d(?:\.\d)? on (?:google|facebook)\b"),   # "4.9 on Google": a number about us that a visitor will believe
    ("review count", r"\b\d[\d,]*\s+(?:google |facebook )?reviews?\b"),
    ("guarantee", r"\bguarantee[ds]?\b"),
    ("superlative", r"#\s?1\b|\bnumber (?:one|1)\b|\btop[- ]rated\b|\bbest[- ](?:in|of)\b|\bleading\b|\bpremier\b|\bmost trusted\b"),
    ("years / founding", r"\byears? (?:of experience|in business|in the business)\b|\bsince (?:19|20)\d\d\b|\bestablished\b|\bfounded (?:in|on)\b"),
    ("results count", r"\b\d[\d,]*\+?\s+(?:homes|houses|families|sellers|closings|clients|customers|deals)\b"),
    ("third-party seal", r"\bBBB\b|Better Business Bureau"),
]
SOFT = [
    ("free", r"\bfree\b"), ("anytime", r"\banytime\b"), ("no obligation", r"\bno obligation\b"),
    ("no fees", r"\bno (?:hidden )?fees?\b"), ("$0", r"\$0\b"), ("cash offer", r"\bcash offer\b"),
    ("as little as", r"\bas little as\b"), ("within an hour", r"\bwithin (?:about )?an hour\b"),
    ("seller financing", r"\bseller financing\b"), ("lease option(s)", r"\blease options?\b"),
    ("down payment assistance", r"\bdown payment assistance\b"), ("MLS", r"\bMLS\b"), ("fair", r"\bfair\b"),
]


def page_text(path):
    s = open(path, encoding="utf-8").read()
    parts = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S):
        try:
            parts.append(json.dumps(json.loads(m.group(1)), ensure_ascii=False))
        except ValueError:
            parts.append(m.group(1))
    parts += re.findall(r'<title>(.*?)</title>', s, flags=re.S)
    parts += re.findall(r'<meta[^>]+(?:name="description"|property="og:(?:title|description)")[^>]*content="([^"]*)"', s)
    parts += re.findall(r'<meta[^>]+content="([^"]*)"[^>]+(?:name="description"|property="og:(?:title|description)")', s)
    parts += re.findall(r'\balt="([^"]*)"', s)
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S)
    body = re.sub(r"<svg.*?</svg>", " ", body, flags=re.S)
    parts.append(re.sub(r"<[^>]+>", " ", body))
    return re.sub(r"\s+", " ", html.unescape(" ".join(parts)))


def load_allow():
    allow = []
    p = os.path.join(ROOT, "tools", "claims-allow.txt")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            bits = [b.strip() for b in line.split("|")]
            if len(bits) >= 3:
                allow.append((bits[0], bits[1].lower(), bits[2]))
    return allow


def main():
    allow = load_allow()
    bad = 0
    used = set()
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    soft_counts = {}
    for path in pages:
        name = os.path.basename(path)
        text = page_text(path)
        low = text.lower()
        for label, pat in HARD:
            for m in re.finditer(pat, text, flags=re.I):
                ok = False
                for i, (pg, sub, why) in enumerate(allow):
                    if pg not in ("*", name):
                        continue
                    # the allowed phrase must actually cover the matched word, not just sit near it
                    for a in re.finditer(re.escape(sub), low):
                        if a.start() <= m.start() and m.end() <= a.end():
                            used.add(i)
                            ok = True
                            break
                    if ok:
                        break
                if not ok:
                    bad += 1
                    ctx = text[max(0, m.start() - 60): m.end() + 60]
                    print(f"  NEEDS A DECISION [{label}] {name}: ...{ctx}...")
        for label, pat in SOFT:
            n = len(re.findall(pat, text, flags=re.I))
            if n:
                soft_counts.setdefault(label, {})[name] = n
    unused = [a for i, a in enumerate(allow) if i not in used]
    for pg, sub, why in unused:
        print(f"  note: allowlist line no longer matches anything ({pg} | {sub}): remove it if the text is gone")
    print("\nSoft claims (counts per page; each is tracked in CONTENT_CLAIMS.md):")
    for k, v in sorted(soft_counts.items()):
        print(f"  {k:28s} " + ", ".join(f"{p.replace('.html','')} {n}" for p, n in sorted(v.items())))
    print()
    if bad:
        print(f"RESULT: {bad} hit(s) need a decision. Fix the text, or add a line to tools/claims-allow.txt with the reason.")
        return 1
    print(f"RESULT: clear. {len(pages)} pages checked; every credential, rating, award, guarantee, result or founding-year word is covered by tools/claims-allow.txt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

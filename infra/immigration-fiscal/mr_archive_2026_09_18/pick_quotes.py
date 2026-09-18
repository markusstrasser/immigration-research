#!/usr/bin/env python3
"""Pull one verbatim quote per chosen load-bearing post; asserts each quote is in the fetched body."""
import json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
PICKS = [
    ("2024/05/the-fiscal-impact-of-low-skill-immigration", "Overall the NAS concluded"),
    ("2024/05/tc-on-less-skilled-immigrants", "According to new research from economists"),
    ("2015/09/open-borders-and-welfare", "Milton Friedman famously said"),
    ("2021/08/hispanics-and-white-criminality", "Hispanics are slightly less likely to be jailed"),
    ("2019/05/caplan-weinersmith-and-open-borders", "The simplest argument against open borders"),
    ("2026/08/immigrant-earnings-assimilation", "converge, or come close to converging"),
    ("2023/12/immigration-backlash", "Recent inflows of unauthorized migrants increase the vote share"),
    ("2024/09/cutting-welfare-for-immigrants", "immigration flows and a welfare state are complements"),
    ("2025/09/michael-clemens-on-h1-b", "caused 30–50 percent of all productivity growth"),
    ("2026/01/low-skilled-immigration-into-the-uk", "The literature does not support the claim"),
    ("2026/01/negative-political-externalities", "one needs to admit that immigration has gone well enough"),
    ("2019/05/state-and-local-policy", "State and local governments are making immigration policy"),
    ("2024/04/updated-estimates-on-immigration-and-wages", "positive and significant effect"),
    ("2025/01/do-migrants-pay-their-way", "second-generation migrants contribute very similarly"),
    ("2026/02/the-economics-of-mass-deportation", "native real wages fall in every state"),
]

recs = {}
for line in open(os.path.join(BASE, "derived/mr_posts.jsonl"), encoding="utf-8"):
    r = json.loads(line)
    recs[r["url"]] = r

def norm(t):
    return re.sub(r"\s+", " ", t).strip()

for frag, anchor in PICKS:
    hit = next((r for u, r in recs.items() if frag in u), None)
    if hit is None:
        print(f"!! MISSING POST {frag}")
        continue
    body = norm(hit["body_text"])
    i = body.find(anchor)
    if i < 0:
        print(f"!! ANCHOR NOT FOUND {frag} :: {anchor}")
        continue
    start = body.rfind(". ", 0, i)
    start = 0 if start < 0 else start + 2
    ABBREV = ("St.", "Dr.", "Mr.", "Mrs.", "Ms.", "Prof.", "U.S.", "U.K.", "e.g.", "i.e.",
              "vs.", "Jr.", "Sr.", "No.", "Fig.", "approx.")
    end, cursor = -1, i
    while True:
        j = body.find(". ", cursor)
        if j < 0:
            end = len(body)
            break
        tail = body[max(0, j - 10):j + 1]
        if any(tail.endswith(a) for a in ABBREV):
            cursor = j + 2
            continue
        end = j + 1
        break
    quote = body[start:end].strip()
    # the leading "> " is this pipeline's blockquote marker, not part of the post text
    cut = quote.rfind("> ", 0, max(1, i - start) + 1)
    if cut >= 0:
        quote = quote[cut + 2:].strip()
    words = quote.split()
    if len(words) > 55:
        quote = " ".join(words[:55])
    assert quote in body, frag
    print(f"- **{hit['author']}, {hit['date'][:10]} — {hit['title']}**")
    print(f"  {hit['url']}")
    print(f"  > {quote}")
    print()

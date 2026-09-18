#!/usr/bin/env python3
"""Helper: rank fetched posts by how directly they bear on the parent's scorecard rows.

Scorecard surfaces (research/immigration-claim-scorecard-2026-09-18.md sections 1-3):
fiscal net position, the generational/second-generation unit, crime comparators, the
open-borders/world-GDP magnitude, the wage null, welfare use, and local incidence.
Prints the top N with matched surfaces so a human picks the final 15.
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SURFACES = {
    "fiscal-net": r"net fiscal|fiscal (?:burden|cost|impact|effect|balance)|taxpayer\w*|"
                  r"pay more in taxes|welfare state|fiscal positive|public finance",
    "second-generation": r"second[- ]generation|third[- ]generation|children of immigrant\w*|"
                         r"descendant\w*|assimilat\w*|intergenerational|converg\w*",
    "crime-comparator": r"crime rate\w*|incarcerat\w*|homicide\w*|imprison\w*|criminal\w*|"
                        r"convict\w*|less crime|more crime",
    "open-borders-magnitude": r"open borders|double world|world gdp|trillion|place premium|"
                              r"free migration|clemens",
    "wage-null": r"wage\w*|mariel|labor market|displace\w*|borjas|card\b|peri\b",
    "welfare-use": r"welfare use|food stamps|snap\b|means-tested|public benefit\w*|medicaid",
    "local-incidence": r"\bschool\w*|\bhousing\b|\brent\w*|\bshelter\w*|\blocal government\b|"
                       r"\bcounty\b|\bstate and local\b",
    "high-skill": r"h-?1b|high[- ]skill|inventor\w*|\bstem\b|talent",
}
RECENT = re.compile(r"/20(1[5-9]|2[0-6])/")

recs = [json.loads(l) for l in open(os.path.join(BASE, "derived/mr_posts.jsonl"), encoding="utf-8")]
scored = []
for r in recs:
    body = r.get("body_text") or ""
    if len(body) < 200:
        continue
    hits = {k: len(re.findall(p, body, re.I)) for k, p in SURFACES.items()}
    live = {k: v for k, v in hits.items() if v}
    if len(live) < 2:
        continue
    score = sum(min(v, 5) for v in live.values()) + 3 * len(live)
    if RECENT.search(r["url"]):
        score += 4
    if re.search(r"\d", body):
        score += 2
    scored.append((score, r, live))
scored.sort(key=lambda t: -t[0])
n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for score, r, live in scored[:n]:
    print(f"{score:3d} {r['date'][:10]} {r['author'][:14]:14s} {r['title'][:62]}")
    print(f"     {r['url']}")
    print(f"     surfaces: {live}")

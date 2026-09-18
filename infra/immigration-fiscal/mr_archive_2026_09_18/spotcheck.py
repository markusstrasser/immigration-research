#!/usr/bin/env python3
"""Verification: print title/author/date from mr_posts.jsonl next to the raw cached HTML byline."""
import hashlib, json, os, random, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(l) for l in open(os.path.join(BASE, "derived/mr_posts.jsonl"), encoding="utf-8")]
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 20260918)
for r in random.sample(recs, 5):
    p = os.path.join(BASE, "_cache/posts", hashlib.sha1(r["url"].encode()).hexdigest() + ".html")
    raw = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r'<div class="byline">(.*?)(?:</header>|<!-- /\.byline -->)', raw, re.S)
    by = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else "(no byline div)"
    t = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', raw, re.S)
    rawtitle = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t.group(1))).strip() if t else "(none)"
    print("URL      ", r["url"])
    print("  jsonl  title=", repr(r["title"]))
    print("         author=", repr(r["author"]), " date=", repr(r["date"]),
          " src=", r["fetch_source"], " wb_ts=", r["wayback_timestamp"])
    print("  rawhtml title=", repr(rawtitle))
    print("          byline=", repr(by[:160]))
    print("  MATCH  title:", r["title"] == rawtitle,
          "| author-in-byline:", r["author"] in by,
          "| date-in-raw:", (r["date"][:10] in raw) or (r["date"][:7] in raw))
    print()

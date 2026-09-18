#!/usr/bin/env python3
"""Phase 2: build derived/mr_candidates.csv from slug regex + Firecrawl site search + exa/map URL files."""
import csv, json, os, re, sys, time
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
DERIVED = os.path.join(BASE, "derived")
CACHE = os.path.join(BASE, "_cache", "search")
os.makedirs(CACHE, exist_ok=True)

SLUG_RE = re.compile(
    r"immigra|migrant|migration|mexic|hispanic|latino|latin-america|border|deport|asylum|"
    r"refugee|open-borders|h-1b|h1b|visa|naturaliz|remittance|borjas|caplan|nowrasteh|clemens|"
    r"peri|mariel|amnesty|dreamer|daca|undocumented|illegal|assimilat|enclave|nativis|diversity|"
    r"huntington|sailer|puerto-ric|cuban|salvador|guatemal|hondur|venezuel|haiti", re.I)

KEYWORDS = ["immigration", "immigrants", "Mexican", "Mexico", "Hispanic", "Latino",
            "open borders", "border", "deportation", "asylum"]

CREDIT_CAP = int(os.environ.get("SEARCH_CREDIT_CAP", "100"))
MAX_PAGES_PER_KW = int(os.environ.get("MAX_PAGES_PER_KW", "10"))
KEY = os.environ.get("FIRECRAWL_API_KEY", "")


def fc_scrape(url, cache_name):
    """Return html (cached on disk). Returns (html, used_credit:bool)."""
    path = os.path.join(CACHE, cache_name)
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        return open(path, encoding="utf-8").read(), False
    r = requests.post("https://api.firecrawl.dev/v1/scrape",
                      headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                      json={"url": url, "formats": ["html"], "onlyMainContent": False,
                            "proxy": "stealth", "timeout": 60000}, timeout=180)
    if r.status_code != 200:
        print(f"  [fc-fail] {url} status={r.status_code}", flush=True)
        return None, True
    d = r.json()
    html = (d.get("data") or {}).get("html", "")
    if not html:
        print(f"  [fc-empty] {url}", flush=True)
        return None, True
    open(path, "w", encoding="utf-8").write(html)
    return html, True


ENTRY_RE = re.compile(r'<h2 class="entry-title"><a href="([^"]+)"[^>]*>(.*?)</a>', re.S)
FOUND_RE = re.compile(r"[Rr]esults? for.{0,120}?([\d,]+)\s*found", re.S)


def parse_search(html):
    urls = [(u, re.sub(r"<[^>]+>", "", t).strip()) for u, t in ENTRY_RE.findall(html)]
    m = FOUND_RE.search(html)
    found = int(m.group(1).replace(",", "")) if m else None
    return urls, found


def main():
    cands = {}   # url -> dict(sources=set, title)

    def add(url, source, title=""):
        url = url.split("#")[0].strip()
        if not url.startswith("http"):
            return
        e = cands.setdefault(url, {"sources": set(), "title": ""})
        e["sources"].add(source)
        if title and not e["title"]:
            e["title"] = title

    # 1. slug regex over the full sitemap
    allp = os.path.join(DERIVED, "mr_posts_all.csv")
    n_all = 0
    with open(allp, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n_all += 1
            if SLUG_RE.search(row["slug"]):
                add(row["url"], "slug-keyword")
    print(f"[slug] {n_all} posts scanned, {len(cands)} slug hits", flush=True)

    # 2. exa + map url files (exa urls are sometimes truncated; resolve by prefix against the sitemap)
    sitemap_urls = []
    with open(allp, encoding="utf-8") as f:
        sitemap_urls = [r["url"] for r in csv.DictReader(f)]

    def resolve(u):
        if u in cands or u.endswith(".html"):
            return [u]
        hits = [s for s in sitemap_urls if s.startswith(u)]
        return hits if hits else [u]

    for path, src in [("/tmp/mr_exa_urls.txt", "exa"), ("/tmp/mr_map_urls.txt", "map")]:
        n, resolved = 0, 0
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                u = line.strip()
                if u.startswith("http") and "marginalrevolution.com" in u:
                    n += 1
                    for r in resolve(u):
                        if r != u:
                            resolved += 1
                        add(r, src)
        print(f"[{src}] {n} urls from {path} ({resolved} prefix-resolved); candidate pool {len(cands)}", flush=True)

    # 3. Firecrawl site search, round-robin across keywords under the credit cap
    credits = 0
    found_counts = {}
    pages_done = {k: 0 for k in KEYWORDS}
    exhausted = set()
    page = 1
    while page <= MAX_PAGES_PER_KW and credits < CREDIT_CAP:
        for kw in KEYWORDS:
            if credits >= CREDIT_CAP or kw in exhausted:
                continue
            q = kw.replace(" ", "+")
            url = (f"https://marginalrevolution.com/?s={q}" if page == 1
                   else f"https://marginalrevolution.com/page/{page}/?s={q}")
            cname = f"{re.sub(r'[^a-z0-9]+', '_', kw.lower())}_p{page}.html"
            html, used = fc_scrape(url, cname)
            if used:
                credits += 1
                time.sleep(1.0)
            if not html:
                exhausted.add(kw)
                continue
            urls, found = parse_search(html)
            if found is not None and kw not in found_counts:
                found_counts[kw] = found
            for u, t in urls:
                add(u, f"site-search:{kw}", t)
            pages_done[kw] = page
            print(f"[search] kw={kw!r} page={page} results={len(urls)} found={found_counts.get(kw)} "
                  f"credits={credits} pool={len(cands)}", flush=True)
            if len(urls) == 0:
                exhausted.add(kw)
        page += 1

    out = os.path.join(DERIVED, "mr_candidates.csv")
    rows = []
    for u, e in sorted(cands.items()):
        m = re.search(r"/(\d{4})/(\d{2})/", u)
        rows.append({"url": u, "date": f"{m.group(1)}-{m.group(2)}" if m else "",
                     "slug": re.sub(r"\.html?$", "", u.rstrip("/").split("/")[-1]),
                     "title": e["title"], "source": "|".join(sorted(e["sources"]))})
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "date", "slug", "title", "source"])
        w.writeheader()
        w.writerows(rows)
    meta = {"candidates": len(rows), "search_credits_used": credits,
            "found_counts": found_counts, "pages_done": pages_done}
    json.dump(meta, open(os.path.join(DERIVED, "search_meta.json"), "w"), indent=2)
    print(f"CANDIDATES: {len(rows)} -> {out}", flush=True)
    print("META " + json.dumps(meta), flush=True)


if __name__ == "__main__":
    main()

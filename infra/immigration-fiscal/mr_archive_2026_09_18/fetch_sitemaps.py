#!/usr/bin/env python3
"""Phase 1: fetch MR post sitemaps via Wayback (id_ raw), parse to derived/mr_posts_all.csv."""
import csv, os, re, sys, time
import requests
from lxml import etree

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "_cache", "sitemaps")
DERIVED = os.path.join(BASE, "derived")
os.makedirs(CACHE, exist_ok=True)
os.makedirs(DERIVED, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
SESS = requests.Session()
SESS.headers.update(UA)


def wayback_get(url, tries=10):
    wb = f"https://web.archive.org/web/2026id_/{url}"
    for attempt in range(1, tries + 1):
        try:
            r = SESS.get(wb, timeout=120, allow_redirects=True)
            if r.status_code == 200 and b"<loc>" in r.content:
                ts = ""
                m = re.search(r"/web/(\d{14})id_/", r.url)
                if m:
                    ts = m.group(1)
                return r.content, ts
            print(f"  [retry {attempt}] {url} status={r.status_code} len={len(r.content)}", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"  [retry {attempt}] {url} error={type(e).__name__}: {e}", flush=True)
        time.sleep(min(60, 5 * attempt))
    return None, ""


def parse(xml_bytes):
    root = etree.fromstring(xml_bytes)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    out = []
    for u in root.findall("s:url", ns):
        loc = u.findtext("s:loc", default="", namespaces=ns).strip()
        mod = u.findtext("s:lastmod", default="", namespaces=ns).strip()
        if loc:
            out.append((loc, mod))
    return out


def slug_of(url):
    p = url.rstrip("/").split("/")[-1]
    return re.sub(r"\.html?$", "", p)


def date_of(url, lastmod):
    m = re.search(r"/(\d{4})/(\d{2})/", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return lastmod[:7] if lastmod else ""


def main():
    # Wayback's newest snapshot of the sitemap set is 2026-02-01, so sitemap40 there holds only
    # 91 posts and sitemap41 does not exist. The live tails (fetched once via Firecrawl stealth,
    # cached as live-post-sitemap40/41.xml) carry Feb-Sep 2026.
    names = ["post-sitemap.xml"] + [f"post-sitemap{i}.xml" for i in range(2, 41)]
    names += ["live-post-sitemap40.xml", "live-post-sitemap41.xml"]
    rows = []
    seen = set()
    for name in names:
        path = os.path.join(CACHE, name)
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            data = open(path, "rb").read()
            print(f"[cache] {name} {len(data)}B", flush=True)
        elif name.startswith("live-"):
            print(f"[MISS] {name} — live copy absent from _cache/sitemaps", flush=True)
            continue
        else:
            data, ts = wayback_get(f"https://marginalrevolution.com/{name}")
            if data is None:
                print(f"[MISS] {name} — wayback failed after retries", flush=True)
                continue
            open(path, "wb").write(data)
            print(f"[ok] {name} {len(data)}B ts={ts}", flush=True)
            time.sleep(1.1)
        try:
            entries = parse(data)
        except Exception as e:  # noqa: BLE001
            print(f"[parse-fail] {name}: {e}", flush=True)
            continue
        n_new = 0
        for loc, mod in entries:
            if loc in seen:
                continue
            seen.add(loc)
            rows.append({"url": loc, "date": date_of(loc, mod), "lastmod": mod,
                         "slug": slug_of(loc), "sitemap": name})
            n_new += 1
        print(f"     {name}: {len(entries)} urls, {n_new} new, running total {len(rows)}", flush=True)

    out = os.path.join(DERIVED, "mr_posts_all.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "date", "lastmod", "slug", "sitemap"])
        w.writeheader()
        w.writerows(rows)
    print(f"TOTAL posts: {len(rows)} -> {out}", flush=True)


if __name__ == "__main__":
    main()

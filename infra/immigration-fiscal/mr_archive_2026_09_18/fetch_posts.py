#!/usr/bin/env python3
"""Phase 3: fetch candidate posts -> derived/mr_posts.jsonl.

Wayback first, Firecrawl stealth fallback. All Internet Archive traffic (replay + CDX) passes
through one global token bucket at <= 1 request/second, so a small worker pool raises throughput
to the rate cap instead of stalling on IA's intermittent "Temporarily Offline" 403s. A URL that
hits an outage is deferred to a later pass rather than blocking its worker for ten minutes.
Every page is written to _cache/posts/<sha1>.html the moment it arrives.
"""
import csv, hashlib, json, os, re, threading, time
from concurrent.futures import ThreadPoolExecutor

import requests
from lxml import html as LH

BASE = os.path.dirname(os.path.abspath(__file__))
DERIVED = os.path.join(BASE, "derived")
PCACHE = os.path.join(BASE, "_cache", "posts")
os.makedirs(PCACHE, exist_ok=True)
os.makedirs(DERIVED, exist_ok=True)

KEY = os.environ.get("FIRECRAWL_API_KEY", "")
FC_CAP = int(os.environ.get("FETCH_CREDIT_CAP", "100"))
LIMIT = int(os.environ.get("FETCH_LIMIT", "0"))
WORKERS = int(os.environ.get("FETCH_WORKERS", "4"))
PASSES = int(os.environ.get("FETCH_PASSES", "4"))
IA_INTERVAL = float(os.environ.get("IA_INTERVAL", "1.05"))

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

_bucket_lock = threading.Lock()
_last_call = [0.0]
_io_lock = threading.Lock()
_fc_lock = threading.Lock()
_fc_used = [0]
CDX_STATE = {"down_until": 0.0, "fails": 0}
_local = threading.local()


def sess():
    if not hasattr(_local, "s"):
        _local.s = requests.Session()
        _local.s.headers.update(UA)
    return _local.s


def ia_get(url, timeout=90):
    """Every Internet Archive request goes through here: <= 1/second across all workers."""
    with _bucket_lock:
        wait = IA_INTERVAL - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
    return sess().get(url, timeout=timeout, allow_redirects=True)


def h_of(url):
    return hashlib.sha1(url.encode()).hexdigest()


def _is_offline(text):
    return "Temporarily Offline" in text[:4000]


def _good(text):
    return "entry-content" in text and "Attention Required" not in text[:4000]


def cdx_captures(url, limit=8):
    """(timestamps of 200-status captures, newest first; whether CDX answered)."""
    if time.time() < CDX_STATE["down_until"]:
        return [], False
    q = ("http://web.archive.org/cdx/search/cdx?url=" + requests.utils.quote(url, safe="") +
         "&output=json&fl=timestamp,statuscode,length&filter=statuscode:200"
         "&collapse=timestamp:6&limit=-" + str(limit))
    try:
        r = ia_get(q, timeout=60)
        if _is_offline(r.text) or r.status_code != 200:
            raise RuntimeError("cdx unavailable")
        body = r.text.strip()
        CDX_STATE["fails"] = 0
        if not body:
            return [], True
        rows = r.json()
        return [row[0] for row in rows[1:]][::-1], True
    except Exception:  # noqa: BLE001
        CDX_STATE["fails"] += 1
        if CDX_STATE["fails"] >= 5:
            CDX_STATE["down_until"] = time.time() + 900
            CDX_STATE["fails"] = 0
            print("  [cdx] circuit open for 15 min", flush=True)
        return [], False


def wayback(url):
    """Return (html, timestamp, err). err 'wayback-offline' means: retry in a later pass."""
    err = "wayback-unknown"
    offline_hits = 0
    queue = [(f"https://web.archive.org/web/2024id_/{url}", "")]
    tried, cdx_done = set(), False
    while queue or not cdx_done:
        if not queue:
            caps, ok = cdx_captures(url)
            cdx_done = True
            for ts in caps:
                if ts not in tried:
                    tried.add(ts)
                    queue.append((f"https://web.archive.org/web/{ts}id_/{url}", ts))
            if not ok:
                return None, "", "wayback-offline"
            if not queue:
                return None, "", err if err != "wayback-unknown" else "wayback-no-capture"
        wb, ts_hint = queue.pop(0)
        try:
            r = ia_get(wb)
            if r.status_code == 200 and _good(r.text):
                m = re.search(r"/web/(\d{14})id_/", r.url)
                return r.text, (m.group(1) if m else ts_hint), None
            if _is_offline(r.text):
                # IA is flapping: defer to a later pass instead of parking a worker on a sleep
                offline_hits += 1
                return None, "", "wayback-offline"
            err = ("wayback-blocked-capture" if r.status_code == 200
                   else f"wayback-{r.status_code}")
        except Exception as e:  # noqa: BLE001
            err = f"wayback-{type(e).__name__}"
            time.sleep(3)
    return None, "", err


def firecrawl(url, tries=4):
    """Stealth scrape. 429 is Firecrawl's concurrency limit, not a spent credit: back off and
    retry, and only count a credit against the cap when a request actually reaches the scraper."""
    for a in range(1, tries + 1):
        with _fc_lock:
            if _fc_used[0] >= FC_CAP:
                return None, "fc-cap-reached"
        try:
            r = requests.post("https://api.firecrawl.dev/v1/scrape",
                              headers={"Authorization": f"Bearer {KEY}",
                                       "Content-Type": "application/json"},
                              json={"url": url, "formats": ["html"], "onlyMainContent": False,
                                    "proxy": "stealth", "timeout": 60000}, timeout=200)
        except Exception as e:  # noqa: BLE001
            time.sleep(5 * a)
            continue
        if r.status_code == 429:
            time.sleep(15 * a)
            continue
        with _fc_lock:
            _fc_used[0] += 1
        if r.status_code != 200:
            return None, f"fc-{r.status_code}"
        h = (r.json().get("data") or {}).get("html", "")
        return (h, None) if h else (None, "fc-empty")
    return None, "fc-429-exhausted"


SIGNED_QUERY_RE = re.compile(r"[?&](?:X-Amz-[A-Za-z]+|AWSAccessKeyId|Signature)=", re.I)


def strip_signed_query(href):
    # A presigned link is expired on arrival, and its credential parameter reads as a leaked
    # key to secret scanners (GitHub push protection blocked the 2026-09-21 push on one).
    return href.split("?", 1)[0] if SIGNED_QUERY_RE.search(href) else href


def node_text(el):
    parts = []
    for child in el.iterchildren():
        tag = (child.tag if isinstance(child.tag, str) else "").lower()
        txt = re.sub(r"[ \t]+", " ", child.text_content()).strip()
        if not txt:
            continue
        if tag == "blockquote":
            parts.append("\n".join("> " + ln.strip() for ln in txt.split("\n") if ln.strip()))
        else:
            parts.append(txt)
    if not parts:
        parts = [re.sub(r"[ \t]+", " ", el.text_content()).strip()]
    return "\n\n".join(parts).strip()


def parse_post(doc_html, url):
    doc = LH.fromstring(doc_html)

    def first(xp):
        r = doc.xpath(xp)
        return r[0] if r else None

    t = first('//h1[contains(@class,"entry-title")]')
    title = t.text_content().strip() if t is not None else ""
    if not title:
        m = re.search(r"<title>(.*?)</title>", doc_html, re.S)
        title = re.sub(r"\s*\|\s*Marginal REVOLUTION.*$", "", m.group(1)).strip() if m else ""

    author = "unknown"
    a = first('//div[contains(@class,"byline")]//span[contains(@class,"author")]')
    if a is None:
        a = first('//span[contains(@class,"author")]')
    if a is not None:
        c = re.sub(r"\s+", " ", a.text_content()).strip()
        if c:
            author = c

    date = ""
    tm = first('//time[contains(@class,"entry-date")]')
    if tm is not None:
        date = (tm.get("datetime") or tm.text_content()).strip()
    if not date:
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', doc_html)
        if m:
            date = m.group(1)
    if not date:
        m = re.search(r"/(\d{4})/(\d{2})/", url)
        if m:
            date = f"{m.group(1)}-{m.group(2)}"

    cats = []
    art = first('//article[contains(@class,"post-")]')
    if art is not None:
        cats = sorted({c[len("category-"):] for c in (art.get("class") or "").split()
                       if c.startswith("category-")})
    tags = sorted({re.sub(r"\s+", " ", e.text_content()).strip()
                   for e in doc.xpath('//a[@rel="tag" or @rel="category tag"]')})

    ce = first('//div[contains(@class,"entry-content")]')
    body = node_text(ce) if ce is not None else ""
    links = []
    if ce is not None:
        for e in ce.xpath(".//a[@href]"):
            href = re.sub(r"^https?://web\.archive\.org/web/\d+[a-z_]*/", "", e.get("href", ""))
            if href.startswith("http"):
                links.append(strip_signed_query(href))
    return {"title": title, "author": author, "date": date, "categories": cats, "tags": tags,
            "body_text": body, "links": sorted(set(links))}


def handle(row, out_f, counters, allow_fc):
    url = row["url"]
    cpath = os.path.join(PCACHE, h_of(url) + ".html")
    mpath = cpath + ".meta"
    if os.path.exists(cpath) and os.path.getsize(cpath) > 2000:
        doc = open(cpath, encoding="utf-8", errors="replace").read()
        meta = json.load(open(mpath)) if os.path.exists(mpath) else {}
        src, ts = meta.get("fetch_source", "cache"), meta.get("wayback_timestamp", "")
    else:
        doc, ts, err = wayback(url)
        src = "wayback"
        if doc is None and err == "wayback-offline" and not allow_fc:
            return ("defer", err)
        if doc is None and allow_fc:
            doc, err2 = firecrawl(url)
            src, ts = "firecrawl", ""
            err = err2 or err
        if doc is None:
            return ("miss", err)
        with _io_lock:
            open(cpath, "w", encoding="utf-8").write(doc)
            json.dump({"fetch_source": src, "wayback_timestamp": ts}, open(mpath, "w"))
    try:
        rec = parse_post(doc, url)
    except Exception as e:  # noqa: BLE001
        return ("miss", f"parse-{type(e).__name__}")
    rec.update({"url": url, "fetch_source": src, "wayback_timestamp": ts,
                "candidate_source": row.get("source", "")})
    with _io_lock:
        out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out_f.flush()
        counters["ok"] += 1
        n = counters["ok"]
    if n % 25 == 0:
        print(f"  ok={n} fc={_fc_used[0]} author={rec['author'][:18]!r} "
              f"len={len(rec['body_text'])} {url[-48:]}", flush=True)
    return ("ok", None)


def main():
    cand_file = os.environ.get("CAND_FILE") or os.path.join(DERIVED, "mr_candidates.csv")
    cands = list(csv.DictReader(open(cand_file, encoding="utf-8")))
    if os.environ.get("PRESERVE_ORDER") != "1":
        cands.sort(key=lambda r: (r.get("source", "") == "map", r.get("url", "")))
    if LIMIT:
        cands = cands[:LIMIT]

    outp = os.path.join(DERIVED, "mr_posts.jsonl")
    done = set()
    if os.path.exists(outp):
        for line in open(outp, encoding="utf-8"):
            try:
                done.add(json.loads(line)["url"])
            except Exception:  # noqa: BLE001
                pass
    todo = [r for r in cands if r["url"] not in done]
    print(f"candidates={len(cands)} already_done={len(done)} todo={len(todo)} "
          f"workers={WORKERS} fc_cap={FC_CAP}", flush=True)

    counters = {"ok": 0}
    misses = {}
    out_f = open(outp, "a", encoding="utf-8")
    for p in range(1, PASSES + 1):
        if not todo:
            break
        allow_fc = (p == PASSES)
        deferred = []
        t0 = time.time()
        print(f"=== pass {p}/{PASSES}: {len(todo)} urls (firecrawl_fallback={allow_fc})", flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            for row, (status, err) in zip(todo, ex.map(
                    lambda r: handle(r, out_f, counters, allow_fc), todo)):
                if status == "defer":
                    deferred.append(row)
                elif status == "miss":
                    misses[row["url"]] = err
                    print(f"  MISS {row['url'][-52:]} ({err})", flush=True)
                else:
                    misses.pop(row["url"], None)
        print(f"=== pass {p} done in {time.time()-t0:.0f}s ok_total={counters['ok']} "
              f"deferred={len(deferred)} misses={len(misses)} fc={_fc_used[0]}", flush=True)
        todo = deferred
        if todo and p < PASSES:
            print("  waiting 120s for the Internet Archive before the next pass", flush=True)
            time.sleep(120)
    for row in todo:
        misses[row["url"]] = "wayback-offline-after-all-passes"
    out_f.close()
    json.dump([{"url": u, "reason": e} for u, e in sorted(misses.items())],
              open(os.path.join(DERIVED, "fetch_misses.json"), "w"), indent=2)
    print(f"FETCHED new={counters['ok']} misses={len(misses)} firecrawl_credits={_fc_used[0]}",
          flush=True)


if __name__ == "__main__":
    main()

"""Fetch the PISA 2015 and 2022 student SPSS zips with parallel HTTP range requests.

webfs.oecd.org serves ~0.15-0.2 MB/s per connection but honours byte ranges (206), so 8 MB chunks are fetched
by 32 threads and written into place. Each chunk is retried; the final size must equal Content-Length.
Usage: python3 fetch_microdata.py   (writes _cache/microdata/stu2015_spss.zip, stu2022_spss.zip)
"""
import concurrent.futures as cf, os, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0"}
FILES = {"_cache/microdata/stu2022_spss.zip": "https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip",
         "_cache/microdata/stu2015_spss.zip": "https://webfs.oecd.org/pisa/PUF_SPSS_COMBINED_CMB_STU_QQQ.zip"}
CHUNK = 8 << 20


def size(url):
    req = urllib.request.Request(url, method="HEAD", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"])


def fetch(url, path, lo, hi):
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={**UA, "Range": f"bytes={lo}-{hi}"})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            if len(data) != hi - lo + 1:
                raise IOError(f"short read {len(data)}")
            with open(path, "r+b") as f:
                f.seek(lo); f.write(data)
            return hi - lo + 1
        except Exception as e:  # retry transient failures
            time.sleep(2 * (attempt + 1)); err = e
    raise RuntimeError(f"{url} {lo}-{hi}: {err}")


def main():
    jobs = []
    for path, url in FILES.items():
        n = size(url)
        if os.path.exists(path) and os.path.getsize(path) == n and os.path.exists(path + ".done"):
            continue
        with open(path, "wb") as f:
            f.truncate(n)
        jobs += [(url, path, lo, min(lo + CHUNK, n) - 1) for lo in range(0, n, CHUNK)]
    t0, got = time.time(), 0
    with cf.ThreadPoolExecutor(32) as ex:
        for k in cf.as_completed([ex.submit(fetch, *j) for j in jobs]):
            got += k.result()
    for path, url in FILES.items():
        assert os.path.getsize(path) == size(url), path
        open(path + ".done", "w").write("ok\n")
    print(f"fetched {got / 1e6:.0f} MB in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()

"""Parallel range-request download of the AHS 2023 national PUF."""
import pathlib, sys, requests
from concurrent.futures import ThreadPoolExecutor
CD = pathlib.Path(__file__).parent/"_cache"
URL = ("https://www2.census.gov/programs-surveys/ahs/2023/"
       "AHS%202023%20National%20PUF%20v1.0%20Flat%20CSV.zip")
OUT = CD/"ahs2023_flat_par.zip"
h = requests.head(URL, allow_redirects=True, timeout=60)
total = int(h.headers["content-length"])
print("size", total, "accept-ranges", h.headers.get("accept-ranges"))
N = 12; step = total//N
parts = [(i, i*step, (total-1 if i == N-1 else (i+1)*step-1)) for i in range(N)]
def get(p):
    i, a, b = p
    f = CD/f"ahs.part{i}"
    if f.exists() and f.stat().st_size == b-a+1: return i
    for attempt in range(6):
        try:
            r = requests.get(URL, headers={"Range": f"bytes={a}-{b}"},
                             stream=True, timeout=180)
            r.raise_for_status()
            with open(f, "wb") as fh:
                for c in r.iter_content(1 << 20): fh.write(c)
            if f.stat().st_size == b-a+1: return i
        except Exception as e:
            print(i, "retry", e, file=sys.stderr)
    raise RuntimeError(f"part {i} failed")
with ThreadPoolExecutor(N) as ex:
    for i in ex.map(get, parts): print("done part", i, flush=True)
with open(OUT, "wb") as o:
    for i, _, _ in parts:
        o.write((CD/f"ahs.part{i}").read_bytes())
print("assembled", OUT.stat().st_size, "expected", total)
for i, _, _ in parts: (CD/f"ahs.part{i}").unlink()

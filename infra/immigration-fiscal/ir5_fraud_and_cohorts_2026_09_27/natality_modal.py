"""Tabulate US birth records by mother's birthplace and Hispanic origin, 1980-2010, on Modal.

Each year's raw NCHS natality zip (NBER mirror) is streamed inside a Modal container and
reduced to counts over a few fixed-width fields; nothing but the counts leaves the container.
Field positions come from NBER's Stata dictionaries (`_cache/dct/natalityYYYY.dct`), parsed
locally and shipped with the call. Results land in a modal.Dict keyed by run id and year, so
a dead local client loses nothing.

    modal run --detach natality_modal.py::launch --run-id r1      # spawn
    uv run --no-project --with modal python3 natality_modal.py collect r1   # write _cache json
"""
import json
import re
import sys
from pathlib import Path

import modal

HERE = Path(__file__).resolve().parent
YEARS = list(range(1980, 2011))
# Variables to cross-tabulate, by NBER dictionary name, whichever the year carries.
WANT = ["restatus", "recwt", "mplbir", "mplbirr", "umbstate", "mbstate_rec", "mbcntry",
        "origm", "ormoth", "umhisp",
        # live birth order recode (run r2 onward): 1980-2002 livord9, 2003+ lbo_rec
        "livord9", "lbo_rec"]
DICT_NAME = "ir5-natality-counts"

app = modal.App("ir5-natality")
image = modal.Image.debian_slim().apt_install("curl", "unzip")


def field_specs(year: int) -> list[tuple[str, int, int]]:
    text = (HERE / "_cache" / "dct" / f"natality{year}.dct").read_text(errors="replace")
    specs = {}
    for m in re.finditer(r"_column\(\s*(\d+)\s*\)\s+\S+\s+(\w+)\s+%(\d+)[fs]", text):
        start, name, width = int(m.group(1)), m.group(2), int(m.group(3))
        if name in WANT and name not in specs:
            specs[name] = (name, start, width)
    return [specs[n] for n in WANT if n in specs]


@app.function(image=image, timeout=3600, cpu=1.0, memory=2048,
              retries=modal.Retries(initial_delay=5.0, max_retries=3))
def tabulate(year: int, specs: list, run_id: str) -> dict:
    import collections
    import subprocess

    base = f"https://data.nber.org/nvss/natality/inputs/raw/{year}/"
    listing = subprocess.run(["curl", "-sS", "--fail", "--retry", "5", "-A", "Mozilla/5.0", base],
                             capture_output=True, text=True, check=True).stdout
    zips = sorted(set(re.findall(r'href="([^"?/]+\.zip)"', listing)))
    zips = [z for z in zips if "ps" not in z.lower()]
    if len(zips) != 1:
        raise RuntimeError(f"{year}: expected one US zip, found {zips}")
    path = f"/tmp/{zips[0]}"
    subprocess.run(["curl", "-sS", "--fail", "--retry", "5", "-A", "Mozilla/5.0", "-o", path,
                    base + zips[0]], check=True)
    members = subprocess.run(["unzip", "-Z1", path], capture_output=True, text=True,
                             check=True).stdout.split()
    counts = collections.Counter()
    lengths = collections.Counter()
    n = 0
    proc = subprocess.Popen(["unzip", "-p", path], stdout=subprocess.PIPE)
    for raw in proc.stdout:
        line = raw.decode("latin-1").rstrip("\r\n")
        if not line.strip():
            continue
        n += 1
        lengths[len(line)] += 1
        key = tuple(line[s - 1:s - 1 + w] for _, s, w in specs)
        counts[key] += 1
    if proc.wait() != 0:
        raise RuntimeError(f"{year}: unzip exit {proc.returncode}")
    out = {"year": year, "zip": zips[0], "members": members, "records": n,
           "line_lengths": dict(lengths.most_common(5)), "fields": [s[0] for s in specs],
           "specs": specs, "counts": [[list(k), v] for k, v in counts.items()]}
    modal.Dict.from_name(DICT_NAME, create_if_missing=True)[f"{run_id}.{year}"] = out
    print(f"{year}: {n} records, {len(counts)} cells")
    return {"year": year, "records": n}


@app.function(image=image, timeout=7200)
def driver(jobs: list, run_id: str) -> None:
    for r in tabulate.starmap([(y, s, run_id) for y, s in jobs], return_exceptions=True,
                              order_outputs=False):
        print(r)
    modal.Dict.from_name(DICT_NAME, create_if_missing=True)[f"{run_id}.done"] = True


DOC_URLS = [
    "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/Nat1980doc.pdf",
    "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/Nat1989doc.pdf",
    "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/Nat2003doc.pdf",
    "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/Nat2004doc.pdf",
    "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/UserGuide2005.pdf",
    "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/DVS/natality/UserGuide2009.pdf",
    "https://www.cdc.gov/nchs/data/statab/natfinal2003.annvol1_01.pdf",
    "https://www.cdc.gov/nchs/data/nvsr/nvsr61/nvsr61_01.pdf",
]
doc_image = modal.Image.debian_slim().apt_install("curl", "poppler-utils")


@app.function(image=doc_image, timeout=1800)
def fetch_docs(run_id: str) -> None:
    import subprocess
    d = modal.Dict.from_name(DICT_NAME, create_if_missing=True)
    for url in DOC_URLS:
        name = url.rsplit("/", 1)[1]
        try:
            # ftp.cdc.gov serves an incomplete chain that Debian's curl rejects (exit 60);
            # the content check below (PDF magic + text) replaces chain validation there.
            insecure = ["-k"] if "ftp.cdc.gov" in url else []
            subprocess.run(["curl", "-sS", "--fail", "--retry", "5", *insecure, "-A",
                            "Mozilla/5.0", "-o", f"/tmp/{name}", url], check=True)
            if open(f"/tmp/{name}", "rb").read(5) != b"%PDF-":
                raise RuntimeError("not a PDF")
            text = subprocess.run(["pdftotext", "-layout", f"/tmp/{name}", "-"],
                                  capture_output=True, text=True, check=True).stdout
            d[f"{run_id}.doc.{name}"] = {"url": url, "text": text}
            print(name, len(text))
        except Exception as e:  # recorded, not swallowed: collect reports the gap
            d[f"{run_id}.doc.{name}"] = {"url": url, "error": repr(e)}
            print(name, "ERROR", e)


@app.local_entrypoint()
def docs(run_id: str):
    print("spawned", fetch_docs.spawn(run_id).object_id)


@app.local_entrypoint()
def launch(run_id: str, years: str = ""):
    ys = [int(y) for y in years.split(",")] if years else YEARS
    jobs = [(y, field_specs(y)) for y in ys]
    call = driver.spawn(jobs, run_id)
    print("spawned", call.object_id, "years", ys)


def collect(run_id: str) -> None:
    d = modal.Dict.from_name(DICT_NAME)
    got = {}
    for y in YEARS:
        try:
            got[y] = d[f"{run_id}.{y}"]
        except KeyError:
            pass
    out = HERE / "_cache" / f"natality_counts_{run_id}.json"
    out.write_text(json.dumps(got))
    missing = [y for y in YEARS if y not in got]
    print(f"wrote {out}: {len(got)} years; missing {missing}")
    if missing:
        sys.exit(3)


def collect_docs(run_id: str) -> None:
    d = modal.Dict.from_name(DICT_NAME)
    out_dir = HERE / "_cache" / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)
    bad = []
    for url in DOC_URLS:
        name = url.rsplit("/", 1)[1]
        try:
            rec = d[f"{run_id}.doc.{name}"]
        except KeyError:
            bad.append(name)
            continue
        if "error" in rec:
            bad.append(f"{name}: {rec['error']}")
            continue
        (out_dir / (name + ".txt")).write_text(rec["text"])
    print("docs missing/failed:", bad)
    if bad:
        sys.exit(3)


if __name__ == "__main__" and len(sys.argv) >= 3 and sys.argv[1] == "collect":
    collect(sys.argv[2])
if __name__ == "__main__" and len(sys.argv) >= 3 and sys.argv[1] == "collect_docs":
    collect_docs(sys.argv[2])

"""Fetch the lane's public inputs into _cache/ with curl (Python urllib fails TLS on this machine).

- County population: Census intercensal estimates 2000-2010 (co-est00int-tot.csv) and 2010-2020
  (cc-est2020int-agesex-all.csv). 2022 comes from the local cc-est2023-alldata.csv.
- County Business Patterns 2007 (cbp07co.zip); 2012, 2017 and 2022 are local copies.
- Census API: 2000 SF3 PCT019 (foreign-born by country of birth) and ACS 5-year B05006 for
  2009, 2014, 2019 and 2024 (windows centred on 2007, 2012, 2017 and 2022), all counties.
- BLS API: CPI-U (CUUR0000SA0) monthly values for 1997, averaged and rounded to one decimal as BLS
  publishes annual averages before 2007; the composition lane's cpi.json starts in 2000.

The API key is read from CENSUS_API_KEY and never printed; curl errors are redacted.
Cached files are skipped, so a rerun is offline.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
FILES = {
    "pep/co-est00int-tot.csv":
        "https://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/county/co-est00int-tot.csv",
    "pep/cc-est2020int-agesex-all.csv":
        "https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/intercensal/county/asrh/cc-est2020int-agesex-all.csv",
    "cbp/cbp07co.zip": "https://www2.census.gov/programs-surveys/cbp/datasets/2007/cbp07co.zip",
}
ACS_YEARS = [2009, 2014, 2019, 2024]


def redact(text):
    return re.sub(r"key=[A-Za-z0-9]+", "key=<KEY>", text)


def curl(url, dest, tries=5):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(1, tries + 1):
        proc = subprocess.run(["curl", "-sS", "-f", "-L", "--max-time", "600", "-o", str(tmp), url],
                              capture_output=True, text=True)
        if proc.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.rename(dest)
            return
        print(f"  [retry {attempt}] {redact(url)[:120]}: rc={proc.returncode} {redact(proc.stderr)[:200]}", flush=True)
        time.sleep(3 * attempt)
    raise SystemExit(f"[BLOCKED] fetch failed: {redact(url)}")


def variables(dataset, group):
    meta = CACHE / "api" / f"{dataset.replace('/', '_')}_{group}_vars.json"
    if not meta.exists():
        curl(f"https://api.census.gov/data/{dataset}/groups/{group}.json", meta)
    labels = json.loads(meta.read_text())["variables"]
    keep = sorted(k for k in labels if k.startswith(group) and (k.endswith("E") or dataset.startswith("2000/")))
    return keep


def api_table(dataset, group, key):
    dest = CACHE / "api" / f"{dataset.replace('/', '_')}_{group}_county.json"
    if dest.exists():
        return
    names = variables(dataset, group)
    merged = None
    for i in range(0, len(names), 45):
        chunk = names[i:i + 45]
        part = CACHE / "api" / f"part_{i}.json"
        url = (f"https://api.census.gov/data/{dataset}?get={','.join(chunk)}&for=county:*&in=state:*&key={key}")
        curl(url, part)
        rows = json.loads(part.read_text())
        part.unlink()
        head, body = rows[0], rows[1:]
        idx = {(r[head.index("state")], r[head.index("county")]): r for r in body}
        if merged is None:
            merged = {"header": ["state", "county"], "rows": {k: list(k) for k in idx}}
        for k in merged["rows"]:
            if k not in idx:
                raise SystemExit(f"[BLOCKED] {dataset} {group}: county {k} missing from a chunk")
        merged["header"] += chunk
        for k, r in idx.items():
            merged["rows"][k] += [r[head.index(v)] for v in chunk]
    out = [merged["header"]] + [merged["rows"][k] for k in sorted(merged["rows"])]
    dest.write_text(json.dumps(out))
    print(f"[ok  ] {dataset} {group}: {len(out) - 1} counties, {len(merged['header']) - 2} cells", flush=True)


def cpi_1997():
    dest = CACHE / "cpi_extra.json"
    if dest.exists():
        return
    raw = CACHE / "bls_cpi_1997.json"
    payload = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": "1997", "endyear": "1997"})
    proc = subprocess.run(["curl", "-sS", "-f", "--max-time", "120", "-X", "POST", "-H", "Content-Type: application/json",
                           "-d", payload, "-o", str(raw), "https://api.bls.gov/publicAPI/v1/timeseries/data/"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"[BLOCKED] BLS fetch failed: {proc.stderr[:200]}")
    data = json.loads(raw.read_text())["Results"]["series"][0]["data"]
    months = [float(x["value"]) for x in data if x["year"] == "1997" and x["period"] in {f"M{m:02d}" for m in range(1, 13)}]
    if len(months) != 12:
        raise SystemExit(f"[BLOCKED] BLS returned {len(months)} months for 1997")
    dest.write_text(json.dumps({"1997": round(sum(months) / 12, 1)}) + "\n")
    print(f"[ok  ] CPI-U 1997 annual average {round(sum(months) / 12, 1)}", flush=True)


def main():
    cpi_1997()
    for rel, url in FILES.items():
        dest = CACHE / rel
        if dest.exists():
            print(f"[skip] {rel}", flush=True)
            continue
        curl(url, dest)
        print(f"[ok  ] {rel} {dest.stat().st_size:,} bytes", flush=True)
    key = os.environ.get("CENSUS_API_KEY", "")
    todo = [("2000/dec/sf3", "PCT019")] + [(f"{y}/acs/acs5", "B05006") for y in ACS_YEARS]
    if any(not (CACHE / "api" / f"{d.replace('/', '_')}_{g}_county.json").exists() for d, g in todo) and not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY not set: source acquire/config.local.env")
    for dataset, group in todo:
        api_table(dataset, group, key)
    return 0


if __name__ == "__main__":
    sys.exit(main())

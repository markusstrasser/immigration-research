#!/usr/bin/env python3
"""Submit, poll and download the IPUMS USA extracts this lane uses. Microdata stay in _cache/.

core — Census 2000 5%, ACS 2010 (1%) and ACS 2009-2011 3-year (3%), persons aged 16-64. All three
       carry 2000-vintage PUMAs, so one Geocorr PUMA->county file maps them to fixed 2013 CBSAs.
       Wages (INCWAGE, WKSWORK2, UHRSWORK, CLASSWKR), commute (TRANTIME, TRANWORK), nativity
       (BPL, CITIZEN), education (EDUCD) and employment (EMPSTAT) for natives and immigrants.
pre  — Census 1990 5%, the same variables, for a 1990-2000 pre-trend placebo. MET2013 is not
       available for 1990 (the API rejects it), so the geography is METAREA (1990 MSAs) and COUNTYFIP.

The key is read from IPUMS_API_KEY (environment or ../acquire/config.local.env) and never printed.
Client pattern copied from ../crime_selection_cohorts_2026_09_23/ipums_extract.py (ranged parallel
download: IPUMS serves one stream at about 40 KB/s).

Usage, from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23/ipums_extract.py submit core pre
  ... status | wait [--max-minutes 60] | download
"""
import argparse
import hashlib
import json
import os
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "ipums"
STATE = CACHE / "extracts.json"
API = "https://api.ipums.org"
AGES = [f"{a:03d}" for a in range(16, 65)]
VARS = ["PERWT", "STATEFIP", "PUMA", "MET2013", "GQ", "AGE", "SEX", "BPL", "CITIZEN", "YRIMMIG",
        "HISPAN", "EDUC", "EMPSTAT", "CLASSWKR", "WKSWORK2", "UHRSWORK", "INCWAGE", "TRANTIME",
        "TRANWORK", "SCHOOL"]
EXTRACTS = {
    "core": {
        "description": "immigration-research ancestry_iv_congestion_wages: 2000 5%, 2010 ACS, 2009-11 ACS, ages 16-64",
        "samples": ["us2000a", "us2010a", "us2011c"],
        "variables": VARS,
        "select": {"AGE": AGES},
    },
    "pre": {
        "description": "immigration-research ancestry_iv_congestion_wages: 1990 5% ages 16-64, pre-trend placebo",
        "samples": ["us1990a"],
        "variables": [v for v in VARS if v != "MET2013"] + ["METAREA", "COUNTYFIP"],
        "select": {"AGE": AGES},
    },
}


def api_key() -> str:
    key = os.environ.get("IPUMS_API_KEY", "")
    env = HERE.parent / "acquire" / "config.local.env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("IPUMS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("[BLOCKED] IPUMS_API_KEY missing")
    return key


def call(method: str, path: str, key: str, **kw) -> requests.Response:
    r = requests.request(method, f"{API}{path}", headers={"Authorization": key}, timeout=120, **kw)
    if r.status_code >= 400:
        raise SystemExit(f"[FAILED] {method} {path}: {r.status_code} {r.text[:600]}")
    return r


def load_state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def submit(key: str, name: str) -> None:
    spec = EXTRACTS[name]
    # IPUMS USA extracts carry the detailed twin (EDUCD, BPLD, EMPSTATD) of each requested variable
    variables = {v: {} for v in spec["variables"]}
    for v, codes in spec["select"].items():
        variables[v] = {"caseSelections": {"general": codes}}
    body = {"description": spec["description"], "dataStructure": {"rectangular": {"on": "P"}},
            "dataFormat": "csv", "samples": {s: {} for s in spec["samples"]}, "variables": variables}
    number = call("POST", "/extracts?collection=usa&version=2", key, json=body).json()["number"]
    state = load_state()
    state[name] = {"number": number, "submitted": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    CACHE.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))
    print(f"submitted {name}: extract {number}")


def status(key: str, number: int) -> dict:
    return call("GET", f"/extracts/{number}?collection=usa&version=2", key).json()


def fetch(url: str, key: str, out: Path) -> None:
    tmp = out.with_suffix(out.suffix + ".part")
    for attempt in range(1, 9):
        have = tmp.stat().st_size if tmp.exists() else 0
        headers = {"Authorization": key, **({"Range": f"bytes={have}-"} if have else {})}
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(30, 120)) as r:
                if have and r.status_code != 206:
                    tmp.unlink()
                    continue
                r.raise_for_status()
                with open(tmp, "ab") as f:
                    for chunk in r.iter_content(chunk_size=1 << 20):
                        f.write(chunk)
            tmp.replace(out)
            return
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout) as exc:
            print(f"  attempt {attempt}: {type(exc).__name__}; resuming")
            time.sleep(min(60, 5 * attempt))
    raise SystemExit(f"[FAILED] download incomplete: {out}")


def fetch_parallel(url: str, key: str, out: Path, total: int, parts: int = 16) -> None:
    from concurrent.futures import ThreadPoolExecutor
    size = -(-total // parts)
    spans = [(i, i * size, min(total, (i + 1) * size) - 1) for i in range(parts) if i * size < total]

    def one(span):
        i, lo, hi = span
        piece = out.with_suffix(out.suffix + f".{i:02d}")
        for attempt in range(1, 12):
            have = piece.stat().st_size if piece.exists() else 0
            if have == hi - lo + 1:
                return piece
            try:
                with requests.get(url, headers={"Authorization": key, "Range": f"bytes={lo + have}-{hi}"},
                                  stream=True, timeout=(30, 120)) as r:
                    if r.status_code != 206:
                        raise requests.exceptions.ConnectionError(f"status {r.status_code}")
                    with open(piece, "ab") as f:
                        for chunk in r.iter_content(chunk_size=1 << 16):
                            f.write(chunk)
            except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout):
                time.sleep(min(60, 5 * attempt))
        if piece.exists() and piece.stat().st_size == hi - lo + 1:
            return piece
        raise SystemExit(f"[FAILED] chunk {i} of {out.name} incomplete")

    with ThreadPoolExecutor(parts) as ex:
        pieces = list(ex.map(one, spans))
    joined = out.with_suffix(out.suffix + ".part")
    with open(joined, "wb") as f:
        for p in pieces:
            f.write(p.read_bytes())
    if joined.stat().st_size != total:
        raise SystemExit(f"[FAILED] {out.name}: {joined.stat().st_size} of {total} bytes")
    joined.replace(out)
    for p in pieces:
        p.unlink()


def download(key: str, only: list[str] | None = None) -> None:
    for name, rec in load_state().items():
        if only and name not in only:
            continue
        info = status(key, rec["number"])
        if info.get("status") != "completed":
            print(f"{name}: extract {rec['number']} is {info.get('status')}; skipped")
            continue
        links = info["downloadLinks"]
        out = CACHE / f"{name}.csv.gz"
        if not out.exists():
            fetch_parallel(links["data"]["url"], key, out, int(links["data"]["bytes"]))
            fetch(links["ddiCodebook"]["url"], key, CACHE / f"{name}.xml")
        digest = hashlib.sha256(out.read_bytes()).hexdigest()
        rec.update(bytes=out.stat().st_size, sha256=digest, samples=sorted(info.get("samples", {})),
                   variables=sorted(info.get("variables", {})))
        state = load_state(); state[name] = rec; STATE.write_text(json.dumps(state, indent=2))
        print(f"{name}: {out.name} {out.stat().st_size / 1e6:.1f} MB sha256 {digest[:16]}")


def wait(key: str, max_minutes: float, only: list[str] | None = None) -> None:
    started = time.time()
    while True:
        pending = []
        for name, rec in load_state().items():
            if only and name not in only:
                continue
            st = status(key, rec["number"]).get("status")
            print(f"{time.strftime('%H:%M:%S')} {name} extract {rec['number']}: {st}", flush=True)
            if st in ("failed", "canceled"):
                raise SystemExit(f"[FAILED] {name} {st}")
            if st != "completed":
                pending.append(name)
        if not pending:
            return
        if time.time() - started > max_minutes * 60:
            raise SystemExit(f"[BLOCKED] still pending after {max_minutes} min: {pending}")
        time.sleep(45)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["submit", "status", "wait", "download"])
    p.add_argument("name", nargs="*", choices=list(EXTRACTS))
    p.add_argument("--max-minutes", type=float, default=60)
    a = p.parse_args()
    key = api_key()
    if a.command == "submit":
        for name in a.name:
            submit(key, name)
    elif a.command == "status":
        for name, rec in load_state().items():
            print(name, rec["number"], status(key, rec["number"]).get("status"))
    elif a.command == "wait":
        wait(key, a.max_minutes, a.name or None)
    else:
        download(key, a.name or None)


if __name__ == "__main__":
    main()

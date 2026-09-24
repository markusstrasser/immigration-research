#!/usr/bin/env python3
"""Submit, wait for and download the two IPUMS-CPS ASEC extracts this lane reads.

  main   ASEC 1999-2025, every person: reason for moving (WHYMOVE), one-year migration
         (MIGRATE1, MIGSTA1), residence (STATEFIP, COUNTY, METFIPS), nativity, ethnicity,
         education, income, tenure and the ASEC person weight.
  repwt  ASEC 2005-2025, interstate movers only (MIGRATE1 = 5): the 160 person replicate
         weights, for standard errors. Replicate weights start in 2005.

IPUMS carries no county or metro of residence one year ago (its ASEC migration group is
MIGRATE1, MIGSTA1, MIGRATE5, MIGSTA5, MIG5*, COUNTRY and WHYMOVE, read 2026-09-24 at
https://cps.ipums.org/cps-action/variables/group/asec_mig), so the origin of an interstate
mover is known only to the state.

Fetches go through curl (Python urllib fails TLS on this machine). The API key is passed to
curl on stdin as a config line, so it never appears in argv, logs or output.

Usage, from the repository root:
  set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
  uv run --no-project python3 infra/immigration-fiscal/movers_reasons_2026_09_24/fetch_ipums.py run
  ... fetch_ipums.py status
  ... fetch_ipums.py download
`run` submits only the extracts the manifest does not already hold, waits, and downloads
whatever is missing or fails its recorded sha256.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "ipums"
MANIFEST = CACHE / "manifest.json"
API = "https://api.ipums.org"
COLLECTION = "cps"
POLL_SECONDS = 45
MAX_WAIT_SECONDS = 5 * 3600

FLAGGED = {"WHYMOVE", "MIGRATE1", "MIGSTA1"}
EXTRACTS = {
    "main": {
        "description": "immigration-research movers_reasons_2026_09_24 main: ASEC 1999-2025 reason for moving",
        "first_year": 1999,
        "variables": ["STATEFIP", "COUNTY", "COUNTYERR", "METFIPS", "MIGRATE1", "MIGSTA1", "WHYMOVE",
                      "NATIVITY", "BPL", "CITIZEN", "HISPAN", "RACE", "AGE", "SEX", "EDUC", "INCTOT",
                      "HHINCOME", "OWNERSHP", "RELATE", "HFLAG", "ASECWT", "CPI99"],
        "case_selections": {},
    },
    "repwt": {
        "description": "immigration-research movers_reasons_2026_09_24 repwt: ASEC 2005-2025 interstate movers, REPWTP",
        "first_year": 2005,
        "variables": ["STATEFIP", "MIGRATE1", "MIGSTA1", "WHYMOVE", "BPL", "AGE", "HFLAG", "ASECWT", "REPWTP"],
        "case_selections": {"MIGRATE1": ["5"]},
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
        raise SystemExit("[BLOCKED] IPUMS_API_KEY missing (environment or acquire/config.local.env)")
    return key


def curl(args: list[str], key: str, *, check_json: bool = True, retry: bool = True):
    """Run curl with the Authorization header supplied on stdin; return parsed JSON or bytes.

    A POST is sent once (retry=False): a retried submission could create a duplicate extract.
    """
    cfg = f'header = "Authorization: {key}"\n'
    retry_args = ["--retry", "4", "--retry-delay", "5"] if retry else []
    r = subprocess.run(["curl", "-sS", "--fail-with-body", *retry_args,
                        "--max-time", "300", "--config", "-", *args],
                       input=cfg.encode(), capture_output=True)
    body = r.stdout
    if r.returncode != 0:
        msg = body.decode(errors="replace")[:600].replace(key, "<key>")
        err = r.stderr.decode(errors="replace")[:300].replace(key, "<key>")
        raise SystemExit(f"[FAILED] curl rc={r.returncode}: {err} {msg}")
    if check_json:
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise SystemExit(f"[FAILED] non-JSON reply: {body[:300]!r}")
    return body


def asec_samples(key: str, first_year: int) -> list[str]:
    names, page = [], 1
    while True:
        data = curl([f"{API}/metadata/{COLLECTION}/samples?version=2&pageSize=500&pageNumber={page}"], key)
        rows = data.get("data", [])
        names += [d["name"] for d in rows
                  if d["name"].endswith("_03s") and first_year <= int(d["name"][3:7]) <= 2025]
        if not data.get("links", {}).get("nextPage") or not rows:
            break
        page += 1
    expected = 2025 - first_year + 1
    if len(set(names)) != expected:
        raise SystemExit(f"[FAILED] expected {expected} ASEC samples {first_year}-2025, found {sorted(names)}")
    return sorted(set(names))


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def save_manifest(m: dict) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2) + "\n")


def submit(key: str, name: str) -> int:
    spec = EXTRACTS[name]
    samples = asec_samples(key, spec["first_year"])
    variables = {}
    for v in spec["variables"]:
        entry = {}
        if v in FLAGGED and name == "main":
            entry["dataQualityFlags"] = True
        if v in spec["case_selections"]:
            entry["caseSelections"] = {"general": spec["case_selections"][v]}
        variables[v] = entry
    body = {"description": spec["description"], "dataStructure": {"rectangular": {"on": "P"}},
            "dataFormat": "csv", "samples": {s: {} for s in samples}, "variables": variables}
    if spec["case_selections"]:
        body["caseSelectWho"] = "individuals"
    CACHE.mkdir(parents=True, exist_ok=True)
    req = CACHE / f"request_{name}.json"
    req.write_text(json.dumps(body, indent=2))
    reply = curl(["-X", "POST", "-H", "Content-Type: application/json", "--data-binary", f"@{req}",
                  f"{API}/extracts?collection={COLLECTION}&version=2"], key, retry=False)
    number = reply["number"]
    print(f"  submitted {name}: extract {number}, {len(samples)} samples {samples[0]}..{samples[-1]}, "
          f"{len(variables)} variables")
    m = load_manifest()
    m[name] = {"extract_number": number, "samples": samples, "variables": spec["variables"],
               "case_selections": spec["case_selections"], "submitted": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    save_manifest(m)
    return number


def status(key: str, number: int) -> dict:
    return curl([f"{API}/extracts/{number}?collection={COLLECTION}&version=2"], key)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch_file(key: str, url: str, out: Path) -> None:
    """Resumable download; IPUMS drops long streams mid-way (seen 2026-09-22)."""
    tmp = out.with_name(out.name + ".part")
    for attempt in range(1, 9):
        cfg = f'header = "Authorization: {key}"\n'
        r = subprocess.run(["curl", "-sS", "--fail", "-L", "-C", "-", "--max-time", "3600", "--config", "-",
                            "-o", str(tmp), url], input=cfg.encode(), capture_output=True)
        if r.returncode == 0:
            break
        err = r.stderr.decode(errors="replace")[:200].replace(key, "<key>")
        print(f"  ! attempt {attempt} for {out.name}: curl rc={r.returncode} {err}; resuming")
        time.sleep(min(60, 5 * attempt))
    else:
        raise SystemExit(f"[FAILED] {out.name} incomplete after 8 attempts; partial kept at {tmp}")
    tmp.replace(out)


def download(key: str, name: str) -> None:
    m = load_manifest()
    if name not in m:
        raise SystemExit(f"[BLOCKED] no submitted extract recorded for {name}")
    number = m[name]["extract_number"]
    info = status(key, number)
    if info.get("status") != "completed":
        raise SystemExit(f"[BLOCKED] extract {number} ({name}) is {info.get('status')}, not completed")
    links = info["downloadLinks"]
    targets = {"data": CACHE / f"cps_{name}.csv.gz", "ddiCodebook": CACHE / f"cps_{name}.xml"}
    for link, out in targets.items():
        rec = m[name].get("files", {}).get(out.name)
        if out.exists() and rec and sha256(out) == rec["sha256"]:
            print(f"  = {out.name} present, sha256 matches")
            continue
        fetch_file(key, links[link]["url"], out)
        m[name].setdefault("files", {})[out.name] = {"bytes": out.stat().st_size, "sha256": sha256(out),
                                                     "downloaded": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
        save_manifest(m)
        print(f"  downloaded {out.name} ({out.stat().st_size / 1e6:.1f} MB)")
    # content check, never size alone: the codebook must name every requested variable
    ddi = targets["ddiCodebook"].read_text(errors="replace")
    missing = [v for v in m[name]["variables"] if v != "REPWTP" and f'name="{v}"' not in ddi]
    if missing:
        raise SystemExit(f"[FAILED] {name} codebook lacks {missing}")


def wait(key: str, number: int) -> None:
    started = time.time()
    while True:
        st = status(key, number).get("status")
        print(f"  extract {number}: {st} ({int(time.time() - started)}s)", flush=True)
        if st == "completed":
            return
        if st in ("failed", "canceled"):
            raise SystemExit(f"[FAILED] extract {number} {st}")
        if time.time() - started > MAX_WAIT_SECONDS:
            raise SystemExit(f"[BLOCKED] extract {number} still {st} after {MAX_WAIT_SECONDS}s")
        time.sleep(POLL_SECONDS)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["run", "submit", "status", "download"])
    p.add_argument("--only", choices=sorted(EXTRACTS))
    a = p.parse_args()
    key = api_key()
    names = [a.only] if a.only else list(EXTRACTS)
    m = load_manifest()
    if a.command in ("submit", "run"):
        for n in names:
            if n not in m:
                submit(key, n)
        m = load_manifest()
    if a.command == "status":
        for n in names:
            if n in m:
                info = status(key, m[n]["extract_number"])
                print(n, json.dumps({k: info.get(k) for k in ("number", "status", "dataFormat")}))
        return
    if a.command in ("run", "download"):
        for n in names:
            if a.command == "run":
                wait(key, m[n]["extract_number"])
            download(key, n)


if __name__ == "__main__":
    main()

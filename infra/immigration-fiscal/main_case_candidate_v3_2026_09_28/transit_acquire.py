#!/usr/bin/env python3
"""Fetch every external input of the transit riders' key into _cache/transit/ and check it against pinned hashes.

    uv run --no-project python3 infra/immigration-fiscal/main_case_candidate_v3_2026_09_28/transit_acquire.py

Inputs (all public; the Census API needs the key in the untracked acquire/config.local.env):
- NHTS 2022 NextGen public-use V2.1 csv files, its codebook, weighting report, user's guide and derived-variable
  definitions (nhts.ornl.gov);
- NHTS 2017 public-use v1.2 csv files, its 98 person replicate weights, codebook and user's guide;
- Census API: ACS 2024 1-year S0201 (Selected Population Profile) for POPGROUP 001 total, 400 Hispanic or Latino and
  4015 Mexican (the 2024 code for the Mexican origin group; 401 returns HTTP 204 for 2024); ACS 2024 1-year B01003,
  B08301 and B08105I for the U.S.; and the 2024 Annual Survey of State and Local Government Finances
  (timeseries/govslocalfin, state and local, $1,000) for transit utility revenue (LF0073), transit current operations
  (LF0216) and transit capital outlay (LF0217), by state and for the U.S.

A file already present with its pinned sha256 is left alone. A missing file is fetched with curl (Python urllib
fails TLS on this machine), its content is validated, and it must then match its pin. Any mismatch, failed fetch or
invalid content prints a line starting [BLOCKED] and exits 1. The Census key is passed to curl on stdin (never in
argv), never printed, and never written: the manifest records each URL without it. The User-Agent is generic.
Writes _cache/transit/manifest.json (url, bytes, sha256 per file; no timestamps).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
CACHE = LANE / "_cache" / "transit"
KEY_FILE = ROOT / "infra" / "immigration-fiscal" / "acquire" / "config.local.env"
UA = "research-script/1.0"
NHTS = "https://nhts.ornl.gov/media"
API = "https://api.census.gov/data"


def _q(base: str, **params: str) -> str:
    return base + "?" + "&".join(f"{k}={v}" for k, v in params.items())


S0201_GET = "NAME,POPGROUP,POPGROUP_LABEL,S0201_001E,S0201_168E,S0201_171E,S0201_174E"
DETAIL_GET = ("NAME,B01003_001E,B08301_001E,B08301_001M,B08301_010E,B08301_010M,B08301_011E,B08301_012E,"
              "B08301_013E,B08301_014E,B08301_015E,B08301_016E,B08301_021E,B08105I_001E,B08105I_004E,B08105I_004M")
GOVS_GET = "AGG_DESC,AGG_DESC_LABEL,GOVTYPE,GOVTYPE_LABEL,NAME,YEAR,AMOUNT"
HISP_GET = "NAME,B01003_001E,B03003_001E,B03003_003E,B08301_001E,B08301_010E,B08105I_001E,B08105I_004E"

# name -> url (without any key), key (needs the Census key), kind (content validator), note
FILES: dict[str, dict] = {
    "nhts2022_csv.zip": dict(
        url=f"{NHTS}/2022/download/csv.zip", kind="zip:perv2pub.csv,tripv2pub.csv,hhv2pub.csv",
        note="2022 NextGen NHTS public use V2.1, csv"),
    "nhts2022_codebook.xlsx": dict(
        url=f"{NHTS}/2022/doc/codebook.xlsx", kind="zip:",
        note="2022 NHTS codebook with frequencies and weighted sums"),
    "nhts2022_weighting_memo.pdf": dict(
        url=f"{NHTS}/2022/doc/2022%20NextGen%20NHTS%20Weighting%20Memo.pdf", kind="pdf",
        note="2022 NHTS Weighting Report: Table 15 weight sums (p.32); variance estimation (p.33)"),
    "nhts2022_users_guide.pdf": dict(
        url=f"{NHTS}/2022/doc/2022%20NextGen%20NHTS%20User's%20Guide%20V201_PubUse.pdf", kind="pdf",
        note="2022 NHTS Data User Guide: no replicate weights; strata STRATUMID, PSU HOUSEID (p.28)"),
    "nhts2022_derived_variables.pdf": dict(
        url=f"{NHTS}/2022/doc/2022%20NextGen%20NHTS%20Derived%20Variables-PubUseV2.1.pdf", kind="pdf",
        note="2022 NHTS derived variables: PUBTRANS, TRIPMODE, TRIPPURP definitions (pp.16-18)"),
    "nhts2017_csv.zip": dict(
        url=f"{NHTS}/2016/download/csv.zip", kind="zip:perpub.csv,trippub.csv,hhpub.csv",
        note="2017 NHTS public use v1.2, csv"),
    "nhts2017_replicates_csv.zip": dict(
        url=f"{NHTS}/2016/download/ReplicatesCSV.zip", kind="zip:perwgt.csv,hhwgt.csv",
        note="2017 NHTS 98 jackknife replicate weights (person, household)"),
    "nhts2017_codebook_v1.2.xlsx": dict(
        url=f"{NHTS}/2017/doc/codebook_v1.2.xlsx", kind="zip:",
        note="2017 NHTS codebook v1.2 with frequencies and weighted sums"),
    "nhts2017_users_guide.pdf": dict(
        url=f"{NHTS}/2017/doc/NHTS2017_UsersGuide_04232019_1.pdf", kind="pdf",
        note="2017 NHTS User's Guide: Table 7-1 weight sums; 7.12 replicate SE formula and worked example"),
}
for _pg in ("001", "400", "4015"):
    FILES[f"census_acs1_2024_s0201_popgroup_{_pg}.json"] = dict(
        url=_q(f"{API}/2024/acs/acs1/spp", get=S0201_GET, **{"for": "us:1"}, POPGROUP=_pg), key=True,
        kind="census:1", note=f"ACS 2024 1-year S0201, POPGROUP {_pg}, United States")
FILES["census_acs1_2024_detail_us.json"] = dict(
    url=_q(f"{API}/2024/acs/acs1", get=DETAIL_GET, **{"for": "us:1"}), key=True, kind="census:1",
    note="ACS 2024 1-year B01003, B08301, B08105I, United States")
for _y in ("2017", "2022", "2024"):
    FILES[f"census_acs1_{_y}_hispanic_commute_us.json"] = dict(
        url=_q(f"{API}/{_y}/acs/acs1", get=HISP_GET, **{"for": "us:1"}), key=True, kind="census:1",
        note=f"ACS {_y} 1-year B01003, B03003, B08301, B08105I: published Hispanic commute RU, United States")
for _code in ("LF0073", "LF0216", "LF0217"):
    for _geo, _n in (("state:*", 51), ("us:1", 1)):
        _tag = "states" if _geo.startswith("state") else "us"
        FILES[f"census_govslocalfin_2024_{_code}_{_tag}.json"] = dict(
            url=_q(f"{API}/timeseries/govslocalfin", get=GOVS_GET, **{"for": _geo}, time="2024",
                   AGG_DESC=_code, GOVTYPE="001"),
            key=True, kind=f"census:{_n}",
            note=f"Annual Survey of State and Local Government Finances 2024, {_code}, state and local, {_tag}")

# sha256 of each file, pinned after the first fetch (2026-09-28). transit_key.py verifies against this same table.
PINS: dict[str, str] = {
    "census_acs1_2017_hispanic_commute_us.json": "4c5d84c7cb0bd63feb3caf550bd936c4b6bfd7308b20060e3c3a3d8150feeed6",
    "census_acs1_2022_hispanic_commute_us.json": "7abc1c17847ac73ff3f7c863b24177f1403fe5ecba90c3e6c4a2cec76dff249d",
    "census_acs1_2024_hispanic_commute_us.json": "32274b6c21aeb99329bfe919b39dc03d9d1a822885c4d811419858b08f25260c",
    "census_acs1_2024_detail_us.json": "9ae0818385c996e290d98db1ae5e4408884242b2c2f60d575b11dba6eb62936d",
    "census_acs1_2024_s0201_popgroup_001.json": "7f9ff6e1f43e6ecfe532225860b5c0447a9170c0b295d4d36b82ca0e7050f45c",
    "census_acs1_2024_s0201_popgroup_400.json": "f1feb0e5414db47beaadd75702a0f0e15a4d39c762638c05db81704f1ea18869",
    "census_acs1_2024_s0201_popgroup_4015.json": "deab1b1add0921bffa2d831669fd5c3c1e61bbbecde22eb107be08d4b2a116da",
    "census_govslocalfin_2024_LF0073_states.json": "39e38c69279ad4a23c1f1af11a7d246ffa5b6ac8aa4c14b897dbe7de5f3a2bcc",
    "census_govslocalfin_2024_LF0073_us.json": "dd123c89fe400bf2074f4fb27b5bac2c98bb4fe897d38a268fd243aab0dbe02a",
    "census_govslocalfin_2024_LF0216_states.json": "d6cba6ec52504a2e6ba3e3615662b9a56e47327efe8476bd4ddbb9bd9f26946f",
    "census_govslocalfin_2024_LF0216_us.json": "d177d73f786872bbb5a1e838c9c770c5c7eddb0f04d0fc2f73b137079ef1ee8b",
    "census_govslocalfin_2024_LF0217_states.json": "cf33cbfdcf2b36e31a5fe90309e85290af1c8d8cf76a16acaeae7b16e8f4e201",
    "census_govslocalfin_2024_LF0217_us.json": "ca8eb5ea04d09fbadc083b102c94aa7d33a31fb0c49c4ed5e812fdd94c65604d",
    "nhts2017_codebook_v1.2.xlsx": "441cc155d34bec26a7a2916c311fbd7efdadffab9e4335090d81b14f7c5fc672",
    "nhts2017_csv.zip": "4f1917d9470fbf351c325ee9fe7d4cdbf71715775d0e0c974ca57861b4d8704d",
    "nhts2017_replicates_csv.zip": "730c3634c0adc6945ab60436b19924e221df516970560e46585fc5613148cc46",
    "nhts2017_users_guide.pdf": "b0e7253570326efa92d52e0ec5423d5ea52441f05c88ea1225224c86f22d9f68",
    "nhts2022_codebook.xlsx": "7e10ff62be0a72b03528f2469e8da850b335b7d761cf6efdfe9eba9b8a513d96",
    "nhts2022_csv.zip": "64530c396d5f164d2259a22f7042f27bee5147babcd367568ddbfafe6c8bf34c",
    "nhts2022_derived_variables.pdf": "2906973e00ad4174187e41dfc14ec628fbec9dd5fe3ad33592199367e3c78a72",
    "nhts2022_users_guide.pdf": "bc0e7dc4546db3ff6a465fca928c29f4ecb7fbfe23d44ee7e57add4602d3ba0c",
    "nhts2022_weighting_memo.pdf": "b78a7cf7fdafbe346d629317cd33519f35e36abd2593d94384adaf132a069223",
}


def blocked(msg: str) -> None:
    print(f"[BLOCKED] {msg}")
    sys.exit(1)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def census_key() -> str:
    key = os.environ.get("CENSUS_API_KEY", "").strip()
    if not key and KEY_FILE.is_file():
        for line in KEY_FILE.read_text().splitlines():
            name, _, value = line.partition("=")
            if name.strip().removeprefix("export ").strip() == "CENSUS_API_KEY":
                key = value.strip().strip('"').strip("'")
    if not key:
        blocked(f"no CENSUS_API_KEY in the environment or {KEY_FILE.relative_to(ROOT)}")
    return key


def fetch(url: str, dest: Path, key: str | None) -> None:
    full = url + (f"&key={key}" if key else "")
    cfg = 'url = "' + full.replace('"', "%22") + '"\n'
    r = subprocess.run(["curl", "-sS", "--fail", "--retry", "3", "--max-time", "1800", "-A", UA, "-o", str(dest),
                        "-K", "-"], input=cfg, text=True, capture_output=True)
    if r.returncode != 0:
        err = (r.stderr or "").strip()
        if key:
            err = err.replace(key, "[REDACTED]")
        dest.unlink(missing_ok=True)
        blocked(f"fetch {dest.name}: curl rc={r.returncode} {err[-300:]}")


def validate(path: Path, kind: str) -> None:
    if kind.startswith("zip:"):
        try:
            with zipfile.ZipFile(path) as z:
                names = set(z.namelist())
                bad = z.testzip()
        except zipfile.BadZipFile as e:
            blocked(f"{path.name} is not a valid zip: {e}")
        if bad:
            blocked(f"{path.name}: corrupt member {bad}")
        want = [m for m in kind[4:].split(",") if m]
        if missing := [m for m in want if m not in names]:
            blocked(f"{path.name}: missing members {missing}")
    elif kind == "pdf":
        data = path.read_bytes()
        if not data.startswith(b"%PDF") or b"%%EOF" not in data[-2048:]:
            blocked(f"{path.name}: not a complete PDF")
    elif kind.startswith("census:"):
        try:
            rows = json.loads(path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            blocked(f"{path.name}: not Census API JSON ({type(e).__name__}); a missing or invalid key returns HTML")
        n = int(kind.split(":")[1])
        if not (isinstance(rows, list) and rows and isinstance(rows[0], list) and len(rows) - 1 == n):
            got = len(rows) - 1 if isinstance(rows, list) else "?"
            blocked(f"{path.name}: expected a header and {n} rows, got {got}")
    else:
        blocked(f"{path.name}: unknown validator {kind}")


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    unpinned, manifest = [], []
    key = None
    for name in sorted(FILES):
        spec, path, pin = FILES[name], CACHE / name, PINS.get(name)
        if path.is_file() and pin and sha256(path) == pin:
            status = "ok"
        elif path.is_file() and pin:
            blocked(f"{name}: sha256 {sha256(path)} != pinned {pin}; delete the file to refetch, "
                    "or re-pin with a reason")
        else:
            if not path.is_file():
                if spec.get("key") and key is None:
                    key = census_key()
                tmp = path.with_name(path.name + ".part")
                fetch(spec["url"], tmp, key if spec.get("key") else None)
                validate(tmp, spec["kind"])
                tmp.replace(path)
            validate(path, spec["kind"])
            got = sha256(path)
            if pin and got != pin:
                blocked(f"{name}: fetched sha256 {got} != pinned {pin}")
            if not pin:
                unpinned.append((name, got))
            status = "fetched" if pin else "UNPINNED"
        manifest.append(dict(file=f"_cache/transit/{name}", url=spec["url"], bytes=path.stat().st_size,
                             sha256=sha256(path), note=spec["note"]))
        print(f"[acquire] {status:8s} {name} {path.stat().st_size} bytes")
    (CACHE / "manifest.json").write_text(json.dumps({"files": manifest}, indent=1, sort_keys=True) + "\n")
    if unpinned:
        for name, got in unpinned:
            print(f"[PIN] {name} {got}")
        blocked(f"{len(unpinned)} file(s) have no pinned sha256; pin them in PINS")
    print(f"[acquire] {len(manifest)} files verified; manifest _cache/transit/manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

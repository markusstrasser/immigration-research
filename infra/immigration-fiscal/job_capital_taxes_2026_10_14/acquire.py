#!/usr/bin/env python3
"""Fetch the public inputs of the job-capital taxes lane into _cache/ (idempotent, pinned).

  bea_s6        BEA NIPA Section 6 workbook (Table 6.18D, taxes on corporate income by industry; 2026 annual update).
  bea_fa3/4/5   BEA Fixed Assets Sections 3 (net stocks by industry), 4 (nonresidential by legal form) and 5
                (residential by legal form and tenure).
  bea_sut       BEA supply-use tables (Use_Summary.xlsx: other taxes on production, value added and the use of
                real-estate and rental services by industry, 2024).
  frb_z1        Federal Reserve Z.1, release of 2026-09-11 (CSV files): business real estate at market value.
  irs_ftc       IRS SOI, Corporate Foreign Tax Credit, Tax Year 2021 (SOI Bulletin, Summer 2025).
  irs_p5655     IRS Publication 5655 (Rev. 2024), Corporate Income Tax Returns, Tax Year 2021.
  census_ind    Census Bureau 2022 industry code list with crosswalk (the CPS ASEC 2025 industry codes).
  ota_summary   Treasury OTA, Summary of OTA Distribution Methodology (May 2021).
  ota_wp111     Treasury OTA Working Paper 111, Power and Frerick, "Have Excess Returns to Corporations Been Increasing
                Over Time?" (November 2016; National Tax Journal 69(4), 2016): the normal-return share of the
                corporate base by period and by industry.
  tf_tpp        Tax Foundation, Personal Property Tax Exemptions for Small Businesses (2023-12-07): the national share
                of property tax collections from tangible personal property.

Fetches go through curl. No key is needed and no personal identifier is sent; the user agent is generic.

  uv run --no-project python3 infra/immigration-fiscal/job_capital_taxes_2026_10_14/acquire.py
  uv run --no-project python3 infra/immigration-fiscal/job_capital_taxes_2026_10_14/acquire.py --check

Without --check, a missing file is fetched and inputs/pins.json gains its sha256 (a pinned file that changed stops the
run). With --check, nothing is fetched: every pinned file must exist with its sha256. The analysis scripts verify the
same pins when they read a file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
PINS = HERE / "inputs" / "pins.json"
UA = "research-script/1.0"
FILES = {
    "bea_Section6All_xls.xlsx": "https://apps.bea.gov/national/Release/XLS/Survey/Section6All_xls.xlsx",
    "bea_fa_Section3All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section3All_xls.xlsx",
    "bea_fa_Section4All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section4All_xls.xlsx",
    "bea_fa_Section5All_xls.xlsx": "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section5All_xls.xlsx",
    "bea_SUPPLY-USE.zip": "https://apps.bea.gov/industry/release/zip/SUPPLY-USE.zip",
    "frb_z1_20260911_csv_files.zip": "https://www.federalreserve.gov/releases/z1/20260911/z1_csv_files.zip",
    "irs_soi_coftc_ty2021.pdf": "https://www.irs.gov/pub/irs-soi/soi-a-coftc-id2503.pdf",
    "irs_p5655_ty2021.pdf": "https://www.irs.gov/pub/irs-prior/p5655--2024.pdf",
    "census_2022_industry_code_list.xlsx":
        "https://www2.census.gov/programs-surveys/demo/guidance/industry-occupation/2022-Census-Industry-Code-List-with-Crosswalk.xlsx",
    "treasury_ota_summary_2021.pdf":
        "https://home.treasury.gov/system/files/131/Summary-of-OTA-Distribution-Methodology-05102021.pdf",
    "treasury_ota_wp111_2016.pdf": "https://home.treasury.gov/system/files/131/wp-111.pdf",
    "taxfoundation_tpp_2023.html":
        "https://taxfoundation.org/research/all/state/personal-property-tax-exemption-small-business/",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def curl_to(url: str, out: Path, attempts: int = 4) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.name + ".part")
    cfg = f'url = "{url}"\noutput = "{tmp}"\nuser-agent = "{UA}"\n'
    for a in range(1, attempts + 1):
        r = subprocess.run(["curl", "-sS", "--fail", "-L", "--max-time", "600", "--config", "-"],
                           input=cfg.encode(), capture_output=True)
        if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
            tmp.replace(out)
            return
        print(f"  ! attempt {a} {url}: rc={r.returncode} {r.stderr.decode(errors='replace')[:160]}")
        time.sleep(4 * a)
    if tmp.exists():
        tmp.unlink()
    raise SystemExit(f"[BLOCKED] could not fetch {url}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="verify pinned files only; fetch nothing")
    args = ap.parse_args()
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    if args.check:
        bad = [name for name in FILES if name not in pins or not (CACHE / name).exists()
               or sha256(CACHE / name) != pins[name]["sha256"]]
        if bad:
            raise SystemExit(f"[BLOCKED] missing or changed inputs: {', '.join(bad)}")
        print(f"ok: {len(FILES)} pinned inputs")
        return
    for name, url in FILES.items():
        out = CACHE / name
        if not out.exists():
            curl_to(url, out)
            print(f"fetched {name} ({out.stat().st_size:,} bytes)")
        digest = sha256(out)
        if name in pins and pins[name]["sha256"] != digest:
            raise SystemExit(f"[BLOCKED] {name} changed: pinned {pins[name]['sha256'][:12]}, now {digest[:12]}")
        pins[name] = {"url": url, "bytes": out.stat().st_size, "sha256": digest}
    PINS.write_text(json.dumps(dict(sorted(pins.items())), indent=1) + "\n")
    print(f"pinned {len(pins)} inputs in {PINS.relative_to(HERE)}")


if __name__ == "__main__":
    sys.exit(main())

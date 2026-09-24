#!/usr/bin/env python3
"""Download the DOL enforcement bulk files this lane uses and reduce them to compact extracts.

The old enforcedata.dol.gov catalog now redirects to the DOL Open Data Portal. Its API needs a key,
but the portal's "Download Data" link serves each dataset as one zip without a key:
  https://data.dol.gov/data-catalog/<AGENCY>/<api_url>/<AGENCY>_<api_url>.zip
(the URL pattern is the portal's own, from its main JS bundle; dataset ids from
https://apiprod.dol.gov/v4/datasets: WHD enforcement 10362, OSHA inspection 10334, OSHA violation 10338).

Outputs (all in _cache/dol/, ignored):
  <AGENCY>_<api_url>.zip            the bulk file as served
  whd_cases.csv.gz                  every WHD case row (all chunk members), the columns the lane uses
  osha_inspections.csv.gz           OSHA inspections opened FY2005 on, the columns the lane uses
  osha_violation_penalties.csv.gz   OSHA violation penalties summed per inspection (FY2005 on)
and one manifest row per fetched file in derived/fetch_manifest_dol.json (bytes, sha256, members,
header, row count, expected keys present).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/compliance_gap_2026_09_24/fetch_dol.py [whd] [osha]
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import subprocess
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "dol"
MANIFEST = HERE / "derived" / "fetch_manifest_dol.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")
BASE = "https://data.dol.gov/data-catalog"
FILES = {
    "whd": [("WHD", "enforcement")],
    "osha": [("OSHA", "inspection"), ("OSHA", "violation")],
}
# columns each reduced file keeps; a missing one stops the run
WHD_KEEP = ["case_id", "trade_nm", "legal_name", "st_cd", "zip_cd", "naic_cd", "naics_code_description",
            "case_violtn_cnt", "cmp_assd", "ee_violtd_cnt", "bw_atp_amt", "ee_atp_cnt",
            "findings_start_date", "findings_end_date", "flsa_violtn_cnt", "flsa_repeat_violator",
            "flsa_bw_atp_amt", "flsa_ee_atp_cnt", "flsa_mw_bw_atp_amt", "flsa_ot_bw_atp_amt",
            "flsa_15a3_bw_atp_amt", "flsa_cmp_assd_amt", "flsa_cl_violtn_cnt", "flsa_cl_minor_cnt",
            "flsa_cl_cmp_assd_amt", "h2a_violtn_cnt", "h2a_bw_atp_amt", "h2a_ee_atp_cnt",
            "h2a_cmp_assd_amt", "mspa_violtn_cnt", "mspa_bw_atp_amt", "mspa_ee_atp_cnt",
            "mspa_cmp_assd_amt", "sca_violtn_cnt", "sca_bw_atp_amt", "dbra_violtn_cnt",
            "dbra_bw_atp_amt", "fmla_violtn_cnt", "fmla_bw_atp_amt", "load_dt"]
OSHA_INSP_KEEP = ["activity_nr", "reporting_id", "state_flag", "estab_name", "site_state", "site_zip",
                  "owner_type", "adv_notice", "safety_hlth", "sic_code", "naics_code", "insp_type",
                  "insp_scope", "union_status", "nr_in_estab", "open_date", "case_mod_date",
                  "close_conf_date", "close_case_date"]
OSHA_VIOL_KEEP = ["activity_nr", "citation_id", "delete_flag", "viol_type", "issuance_date",
                  "current_penalty", "initial_penalty", "nr_instances", "nr_exposed", "gravity"]
FIRST_OPEN = "2004-10-01"  # FY2005 start; the lane's WHD file also starts at FY2005


def curl(url: str, out: Path) -> None:
    tmp = out.with_suffix(out.suffix + ".part")
    cmd = ["curl", "-sS", "--fail", "-L", "-A", UA, "-H", 'sec-ch-ua: "Chromium";v="128"',
           "--retry", "5", "--retry-delay", "10", "-C", "-", "-o", str(tmp), url]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        raise SystemExit(f"[FAILED] curl {url}: exit {r.returncode}")
    tmp.replace(out)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def save_manifest(m: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n")


def members(zpath: Path) -> list[zipfile.ZipInfo]:
    with zipfile.ZipFile(zpath) as z:
        return [i for i in z.infolist() if not i.is_dir()]


def csv_rows(zpath: Path, member: str):
    """Stream one CSV member as dict rows (utf-8, undecodable bytes replaced)."""
    z = zipfile.ZipFile(zpath)
    raw = z.open(member)
    text = io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline="")
    return csv.DictReader(text)


def reduce_members(zpath: Path, names: list[str], keep: list[str], out: Path, row_filter=None) -> dict:
    """Write the kept columns of every member (same header required) into one csv.gz."""
    n_in = n_out = 0
    per_member = []
    header0 = None
    tmp = out.with_suffix(out.suffix + ".part")
    with gzip.open(tmp, "wt", newline="") as g:
        w = csv.writer(g, lineterminator="\n")
        w.writerow(keep)
        for member in names:
            reader = csv_rows(zpath, member)
            header = [h.strip() for h in reader.fieldnames]
            if header0 is None:
                header0 = header
            elif header != header0:
                raise SystemExit(f"[FAILED] {zpath.name}/{member}: header differs from the first member")
            inv = {h.lower(): h for h in reader.fieldnames}
            missing = [k for k in keep if k not in inv]
            if missing:
                raise SystemExit(f"[FAILED] {zpath.name}/{member}: expected columns missing: {missing}")
            m_in = 0
            for row in reader:
                m_in += 1
                vals = [(row.get(inv[k]) or "").strip() for k in keep]
                if row_filter and not row_filter(dict(zip(keep, vals))):
                    continue
                w.writerow(vals)
                n_out += 1
                if (n_in + m_in) % 2_000_000 == 0:
                    print(f"  {member}: {n_in + m_in:,} rows read, {n_out:,} kept", flush=True)
            n_in += m_in
            per_member.append({"member": member, "rows": m_in})
    tmp.replace(out)
    return {"members": per_member, "header": header0, "rows": n_in, "rows_kept": n_out,
            "expected_keys_present": True, "reduced_file": out.name}


def fetch_all(which: list[str]) -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    m = load_manifest()
    for group in which:
        for agency, api in FILES[group]:
            name = f"{agency}_{api}"
            url = f"{BASE}/{agency}/{api}/{name}.zip"
            zpath = CACHE / f"{name}.zip"
            if not zpath.exists():
                t = time.time()
                print(f"downloading {url}", flush=True)
                curl(url, zpath)
                print(f"  {zpath.stat().st_size / 1e6:.1f} MB in {time.time() - t:.0f}s", flush=True)
            digest = sha256(zpath)
            rec = m.get(name, {})
            if rec.get("sha256") == digest and rec.get("reduced"):
                print(f"{name}: unchanged, reduced files present")
                continue
            mem = members(zpath)
            rec = {"url": url, "bytes": zpath.stat().st_size, "sha256": digest,
                   "fetched": time.strftime("%Y-%m-%d"),
                   "members": [{"name": i.filename, "bytes": i.file_size} for i in mem]}
            csvs = [i.filename for i in mem if i.filename.lower().endswith(".csv")]
            print(f"{name}: members {[(i.filename, i.file_size) for i in mem]}", flush=True)
            reduced = []
            data = [c for c in csvs if "dictionary" not in c.lower() and "metadata" not in c.lower()]
            if not data:
                raise SystemExit(f"[FAILED] {name}: no data CSV among {csvs}")
            if name == "WHD_enforcement":
                reduced.append(reduce_members(zpath, data, WHD_KEEP, CACHE / "whd_cases.csv.gz"))
            elif name == "OSHA_inspection":
                reduced.append(reduce_members(zpath, data, OSHA_INSP_KEEP, CACHE / "osha_inspections.csv.gz",
                                              row_filter=lambda r: r["open_date"][:10] >= FIRST_OPEN))
            elif name == "OSHA_violation":
                reduced.append(reduce_members(zpath, data, OSHA_VIOL_KEEP, CACHE / "osha_violations.csv.gz",
                                              row_filter=lambda r: r["delete_flag"] != "X"
                                              and r["issuance_date"][:10] >= FIRST_OPEN))
            rec["reduced"] = reduced
            m[name] = rec
            save_manifest(m)
            for r in reduced:
                print(f"  {len(r['members'])} member(s): {r['rows']:,} rows, {r['rows_kept']:,} kept -> {r['reduced_file']}")


if __name__ == "__main__":
    args = sys.argv[1:] or ["whd", "osha"]
    fetch_all(args)

#!/usr/bin/env python3
"""ACS 2024 1-year PUMS earnings/income gaps for the ledger's comparison groups.

Independent-survey replication of the CPS-based common-age wage and income gaps.
Reads only the needed columns from the person-file parts, applies ADJINC,
restricts to the household population, and computes group x age-band
means plus common-age per-person and age-matched aggregate gaps with the 80
replicate weights (variance 4/80 * sum((rep - full)^2)).

Writes derived/acs_gaps.csv, derived/acs_cells.csv and derived/audit.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as C  # noqa: E402

DATA = Path("/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr")
ZIP = DATA / "csv_pus.zip"
SRC_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip"
OUT = HERE / "derived"

REPS = [f"PWGTP{i}" for i in range(1, 81)]
# The 2024 1-year person PUMS names the state field STATE (not ST) and carries no
# TYPEHUGQ column; the housing-unit/group-quarters distinction is encoded in
# SERIALNO as the characters at positions 4:6 ("HU" or "GQ"). RELSHIPP 37/38
# (institutionalized / noninstitutionalized group quarters) is used as a cross-check.
COLS = (["SERIALNO", "SPORDER", "PWGTP", "STATE", "AGEP", "SEX", "NATIVITY", "POBP",
         "HISP", "RAC1P", "RELSHIPP", "WAGP", "PINCP", "PERNP", "ADJINC", "ESR"] + REPS)

CA, TX = 6, 48
GROUPS = {
    "mexico_born": lambda d: d.POBP.eq(303),
    "usborn_mexican_selfid": lambda d: d.NATIVITY.eq(1) & d.HISP.eq(2),
    "native_nh_white": lambda d: d.NATIVITY.eq(1) & d.HISP.eq(1) & d.RAC1P.eq(1),
    "all_native": lambda d: d.NATIVITY.eq(1),
}
REFERENCE = "native_nh_white"
VALUES = ["WAGP", "PINCP", "PERNP"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(zip_path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(zip_path) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        if not members:
            raise SystemExit(f"[BLOCKED] no csv members in {zip_path}")
        for name in members:
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                part = pd.read_csv(fh, usecols=COLS, dtype={"SERIALNO": str})
            part = part.rename(columns={"STATE": "ST"})
            hu = part.SERIALNO.str.slice(4, 6).eq("HU")
            gq_rel = part.RELSHIPP.isin([37, 38])
            if (hu & gq_rel).any() or (~hu & ~gq_rel).any():
                raise SystemExit("[BLOCKED] SERIALNO housing-unit flag disagrees with RELSHIPP 37/38")
            part = part[hu]
            frames.append(part)
    d = pd.concat(frames, ignore_index=True)
    print(f"[read] household-population person records: {len(d):,}", flush=True)
    return d


def table(d: pd.DataFrame, domain: str) -> tuple[list, list]:
    band = C.bands_of(d.AGEP.to_numpy())
    weights = d[["PWGTP"] + REPS].to_numpy(dtype=float)
    adj = d.ADJINC.to_numpy(dtype=float) / 1_000_000.0
    values = {k: d[k].fillna(0).to_numpy(dtype=float) * adj for k in VALUES}
    masks = {n: f(d).to_numpy() for n, f in GROUPS.items()}
    cells = {n: C.cell_totals(m, band, weights, values) for n, m in masks.items()}

    n0 = cells[REFERENCE]["n"][:, 0]
    shares = n0 / n0.sum()

    age = d.AGEP.to_numpy()
    esr = d.ESR.to_numpy()
    employed = np.isin(esr, [1, 2, 4, 5])

    rows = []
    for name, cell in cells.items():
        for b in range(C.NBANDS):
            row = dict(survey="ACS", domain=domain, group=name, band=C.BAND_LABELS[b])
            pop, pop_se = C.sdr(cell["n"][b], 80)
            row.update(population=pop, population_se=pop_se)
            for key in VALUES:
                e, s = C.sdr(C.safe_div(cell[key], cell["n"])[b], 80)
                row[f"mean_{key}"] = e
                row[f"mean_{key}_se"] = s
            rows.append(row)
        row = dict(survey="ACS", domain=domain, group=name, band="all")
        pop, pop_se = C.sdr(cell["n"].sum(axis=0), 80)
        row.update(population=pop, population_se=pop_se)
        for key in VALUES:
            e, s = C.sdr(C.crude_mean(cell, key), 80)
            row[f"mean_{key}"] = e
            row[f"mean_{key}_se"] = s
        rows.append(row)

    # employment rate, 16+
    for name, m in masks.items():
        sel = m & (age >= 16)
        w = weights[sel]
        num = employed[sel].astype(float) @ w
        den = w.sum(axis=0)
        e, s = C.sdr(num / den, 80)
        rows.append(dict(survey="ACS", domain=domain, group=name, band="16+",
                         population=float(den[0]), population_se=np.nan,
                         employment_rate=e, employment_rate_se=s))

    gaps = []
    for name, cell in cells.items():
        if name == REFERENCE:
            continue
        for key in VALUES:
            v = C.common_age_gap(cell, cells[REFERENCE], key, shares)
            e, s = C.sdr(v, 80)
            a = C.age_matched_total_gap(cell, cells[REFERENCE], key)
            ae, ase = C.sdr(a, 80)
            gaps.append(dict(survey="ACS", domain=domain, group=name, reference=REFERENCE,
                             variable=key,
                             common_age_gap_per_person=e, common_age_gap_se=s,
                             common_age_ci_low=e - 1.96 * s, common_age_ci_high=e + 1.96 * s,
                             age_matched_gap_bn=ae / 1e9, age_matched_gap_bn_se=ase / 1e9))
    return rows, gaps


def gate3(national_household_pop: float) -> dict:
    """Compare the PUMS household-population total with the published ACS table."""
    key = ""
    cfg = HERE.parent / "acquire/config.local.env"
    if cfg.exists():
        for line in cfg.read_text().splitlines():
            t = line.strip()
            if t.startswith("export "):
                t = t[len("export "):]
            if t.startswith("CENSUS_API_KEY="):
                key = t.split("=", 1)[1].strip().strip('"').strip("'")
    url = "https://api.census.gov/data/2024/acs/acs1?get=NAME,B25008_001E&for=us:1"
    if key:
        url += f"&key={key}"
    try:
        with urllib.request.urlopen(url, timeout=60) as fh:
            payload = json.loads(fh.read().decode())
        published = float(payload[1][1])
        ratio = national_household_pop / published
        return {"status": "checked", "source": "ACS 2024 1-year B25008_001E via API",
                "published": published, "pums_weighted": national_household_pop,
                "ratio": ratio, "within_0.5pct": bool(abs(ratio - 1) < 0.005)}
    except Exception as exc:  # noqa: BLE001
        return {"status": "skipped", "reason": f"{type(exc).__name__}: {exc}",
                "pums_weighted": national_household_pop}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", type=Path, default=ZIP)
    args = ap.parse_args()
    if not args.zip.exists():
        raise SystemExit(f"[BLOCKED] ACS PUMS zip not found: {args.zip}")
    OUT.mkdir(parents=True, exist_ok=True)

    digest = sha256(args.zip)
    d = load(args.zip)

    rows, gaps = table(d, "national")
    national_pop = float(d.PWGTP.sum())
    for code, label in [(CA, "CA"), (TX, "TX")]:
        sub = d[d.ST.eq(code)]
        r2, g2 = table(sub, label)
        rows += r2
        gaps += g2

    pd.DataFrame(rows).to_csv(OUT / "acs_cells.csv", index=False)
    pd.DataFrame(gaps).to_csv(OUT / "acs_gaps.csv", index=False)

    audit = {
        "acs_source_url": SRC_URL,
        "acs_zip": str(args.zip),
        "acs_zip_bytes": args.zip.stat().st_size,
        "acs_zip_sha256": digest,
        "content_length_probe": 602847146,
        "df_free_at_probe": "73Gi available on /System/Volumes/Data",
        "household_person_records": int(len(d)),
        "replicate_weights": 80,
        "variance": "4/80 * sum((rep - full)^2)",
        "adjinc_applied": "WAGP, PINCP, PERNP multiplied by ADJINC/1e6",
        "domain": "SERIALNO[4:6] == 'HU' (housing unit; group quarters excluded). "
                  "The 2024 1-year person PUMS has no TYPEHUGQ column; this flag was "
                  "verified to agree exactly with RELSHIPP not in {37,38}.",
        "state_field": "STATE (the 2024 file does not use ST)",
        "group_definitions": {
            "mexico_born": "POBP == 303",
            "usborn_mexican_selfid": "NATIVITY == 1 & HISP == 2",
            "native_nh_white": "NATIVITY == 1 & HISP == 1 & RAC1P == 1",
            "all_native": "NATIVITY == 1",
        },
        "gate3_household_population": gate3(national_pop),
    }
    (OUT / "audit.json").write_text(json.dumps(audit, indent=2))
    print(f"[done] wrote {OUT/'acs_gaps.csv'}", flush=True)


if __name__ == "__main__":
    main()

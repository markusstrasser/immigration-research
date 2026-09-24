"""ACS 2024 1-year PUMS: a second survey beside the CPS for the Hispanic shares of recipients.

The ACS asks about SNAP (household, FS), public assistance income (person, PAP) and Medicaid or
means-tested coverage (person, HINS4); it has no WIC, housing-assistance or unemployment item.
Its samples are about 25 times the CPS's, so it separates CPS sampling noise from reporting
differences, and it gives the union's share of Hispanic recipients by state. The union is
approximated as Mexican origin (HISP = 02) or born in Mexico (POBP = 303), as in the LTSS lane;
the ACS has no parental birthplace.

Measures, by state and nationally (STATE; 50 states and DC):
- snap_households: households (TYPEHUGQ = 1) with FS = 1, Hispanic householder (HHLDRHISP > 1);
- snap_persons: persons in those households;
- pap_persons: persons with PAP > 0;
- medicaid_persons: persons with HINS4 = 1;
- low_income_persons: persons with POVPIP < 200 (fallback for the union's share of Hispanics);
- all_persons: every person, the premise check that Hispanic is close to Mexican in TX, CA, AZ,
  NM and NV.
Replicate SEs: sqrt(4/80 * sum over 80 replicates of (theta_r - theta_0)^2).

Writes derived/acs_recipients_2024.csv. Run from the repo root (reads about 3.4 GB of CSV in chunks):
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/acs_check.py
"""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ACS = Path("/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr")
PREP = [f"PWGTP{i}" for i in range(1, 81)]
HREP = [f"WGTP{i}" for i in range(1, 81)]
ABBR = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
        13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
        23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
        32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
        41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT",
        51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}
PARTS = ["total", "hisp", "union", "union_hisp", "mex_hisp"]


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def accumulate(acc, measure, state, mask, weights, parts):
    """Add weighted sums per state for each part into acc[(measure, part)] (states x 81)."""
    for part, pm in parts.items():
        m = mask & pm
        if not m.any():
            continue
        sums = pd.DataFrame(weights[m]).groupby(state[m]).sum()
        key = (measure, part)
        acc[key] = sums if key not in acc else acc[key].add(sums, fill_value=0)


def main():
    hz, pz = ACS / "csv_hus.zip", ACS / "csv_pus.zip"
    hcols = ["SERIALNO", "STATE", "TYPEHUGQ", "FS", "HHLDRHISP", "WGTP", *HREP]
    pcols = ["SERIALNO", "STATE", "PWGTP", *PREP, "HISP", "POBP", "HINS4", "PAP", "POVPIP"]
    acc = {}
    fs_of = []
    with zipfile.ZipFile(hz) as z:
        for member in ("psam_husa.csv", "psam_husb.csv"):
            for h in pd.read_csv(z.open(member), usecols=hcols, chunksize=400_000,
                                 dtype={"SERIALNO": str}):
                hu = h.TYPEHUGQ.eq(1).to_numpy()
                snap = hu & h.FS.eq(1).to_numpy()
                w = h[["WGTP", *HREP]].to_numpy(float)
                hisp = h.HHLDRHISP.gt(1).to_numpy()
                mex = h.HHLDRHISP.eq(2).to_numpy()
                accumulate(acc, "snap_households", h.STATE.to_numpy(), snap, w,
                           {"total": np.ones(len(h), bool), "hisp": hisp, "union": mex,
                            "union_hisp": mex, "mex_hisp": mex})
                fs_of.append(h.loc[snap, ["SERIALNO"]])
    snap_serials = set(pd.concat(fs_of).SERIALNO)
    with zipfile.ZipFile(pz) as z:
        for member in ("psam_pusa.csv", "psam_pusb.csv"):
            for p in pd.read_csv(z.open(member), usecols=pcols, chunksize=400_000,
                                 dtype={"SERIALNO": str}):
                w = p[["PWGTP", *PREP]].to_numpy(float)
                hisp = p.HISP.gt(1).to_numpy()
                mex = p.HISP.eq(2).to_numpy()
                union = mex | p.POBP.eq(303).to_numpy()
                parts = {"total": np.ones(len(p), bool), "hisp": hisp, "union": union,
                         "union_hisp": union & hisp, "mex_hisp": mex}
                st = p.STATE.to_numpy()
                accumulate(acc, "snap_persons", st, p.SERIALNO.isin(snap_serials).to_numpy(), w, parts)
                accumulate(acc, "pap_persons", st, p.PAP.fillna(0).gt(0).to_numpy(), w, parts)
                accumulate(acc, "medicaid_persons", st, p.HINS4.eq(1).to_numpy(), w, parts)
                accumulate(acc, "low_income_persons", st, p.POVPIP.fillna(999).lt(200).to_numpy(), w, parts)
                accumulate(acc, "all_persons", st, np.ones(len(p), bool), w, parts)
    rows = []
    for measure in ["snap_households", "snap_persons", "pap_persons", "medicaid_persons",
                    "low_income_persons", "all_persons"]:
        tables = {part: acc[(measure, part)].reindex(sorted(ABBR)).fillna(0) for part in PARTS}
        geos = [("US", slice(None))] + [(ABBR[s], [s]) for s in sorted(ABBR)]
        for geo, sel in geos:
            vals = {part: tables[part].loc[sel].to_numpy().sum(axis=0) for part in PARTS}
            row = dict(measure=measure, geography=geo, total=vals["total"][0])
            for name, num, den in [("hisp_share", "hisp", "total"), ("union_share", "union", "total"),
                                   ("union_in_hisp", "union_hisp", "hisp"), ("mex_in_hisp", "mex_hisp", "hisp")]:
                with np.errstate(invalid="ignore", divide="ignore"):
                    r = vals[num] / vals[den]
                row[name] = r[0]
                row[name + "_se"] = float(np.sqrt(4 / 80 * np.square(r[1:] - r[0]).sum()))
            rows.append(row)
    out = pd.DataFrame(rows)
    us = out[(out.measure == "all_persons") & (out.geography == "US")].total.iloc[0]
    if not 3.30e8 < us < 3.45e8:
        raise SystemExit(f"[GATE FAIL] ACS 2024 total population {us:,.0f}")
    out.to_csv(HERE / "derived/acs_recipients_2024.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 200)
    show = out[out.geography.isin(["US", "TX", "CA", "AZ", "NM", "NV"])]
    print(show.round(4).to_string(index=False))
    print(f"[gate] ACS 2024 resident population {us:,.0f}; archives {sha(hz)[:12]} {sha(pz)[:12]}")


if __name__ == "__main__":
    main()

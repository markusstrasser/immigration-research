"""Cross-check of the IPUMS-based estimates on the Census Bureau's own ACS PUMS file, with the
80 successive-difference replicate weights.

The 2010-14 arrival cohort's main survey is the 2015 ACS. This script rebuilds that cohort from
the local 2015 1-year person PUMS (SCHL detailed grades, POBP = 303, YOEP, AGEP, SEX, PWGTP and
PWGTP1-80), places it with the same origin reference as position.py, and compares (a) the point
estimates with the IPUMS-based main table and (b) the linearised cluster SE used throughout with
the replicate-weight SE (Census formula: SE = sqrt(4/80 * sum_r (theta_r - theta)^2)). It also
reports the share of these records whose SCHL was allocated (FSCHLP = 1) and the estimates with
allocated records dropped: the Census Bureau imputes missing schooling from donors that are not
matched on place of birth.

  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/acs_pums_check.py
"""
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import position as P  # noqa: E402
from levels import FIVE  # noqa: E402

ROOT = HERE.parents[2]
ZIP = ROOT / "sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_2015.zip"
YEAR, C0, C1 = 2015, 2010, 2014
# ACS SCHL (2008+) -> shared scale
SCHL = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, 12: 9, 13: 10, 14: 11, 15: 12,
        16: 13, 17: 13, 18: 13, 19: 14, 20: 15, 21: 16, 22: 16, 23: 16, 24: 16}
REP = [f"pwgtp{i}" for i in range(1, 81)]   # lowercase in the 2015 file


def load() -> pd.DataFrame:
    cols = ["SERIALNO", "SPORDER", "POBP", "AGEP", "SEX", "SCHL", "FSCHLP", "YOEP", "CIT", "SCH", "PWGTP"] + REP
    parts = []
    with zipfile.ZipFile(ZIP) as z:
        for m in ("ss15pusa.csv", "ss15pusb.csv"):
            for ch in pd.read_csv(z.open(m), usecols=cols, chunksize=500_000):
                parts.append(ch[ch.POBP == 303])
    d = pd.concat(parts, ignore_index=True)
    d = d[d.SCHL.notna() & d.YOEP.between(C0, C1)].copy()
    d["BIRTHYR"] = YEAR - d.AGEP            # IPUMS BIRTHYR for the ACS is YEAR - AGE
    d["arr_age"] = d.AGEP - (YEAR - d.YOEP)
    d = d[d.arr_age >= 20].copy()
    d["lo"] = d.SCHL.astype(int).map(SCHL)
    d["hi"] = d["lo"]
    d["sex"] = d.SEX.map({1: "H", 2: "M"})
    d["YEAR"], d["SERIAL"], d["PERWT"] = YEAR, d.SERIALNO, d.PWGTP
    return d


def main() -> None:
    origin = P.Origin(P.OUT / "origin_levels.csv")
    everyone = load()
    rows = []
    for subset, d in (("all records", everyone), ("SCHL not allocated", everyone[everyone.FSCHLP == 0].copy())):
        rows += estimates(origin, d, subset)
    out = pd.DataFrame(rows)
    alloc = float((everyone.PWGTP * (everyone.FSCHLP == 1)).sum() / everyone.PWGTP.sum())
    main_tab = pd.read_csv(P.OUT / "position_main.csv")
    ip = main_tab[(main_tab.cohort == f"{C0}-{C1}") & (main_tab.sex == "P")].iloc[0]
    ipums = {"ridit": ip.ridit, "q1": ip.q1, "q5": ip.q5, "mig_c1": ip.mig_c1_none_primary_incomplete,
             "mig_c5": ip.mig_c5_tertiary, "diff_c1": ip.diff_c1_none_primary_incomplete, "diff_c5": ip.diff_c5_tertiary}
    out["estimate_ipums_main"] = out.statistic.map(ipums)
    out.insert(0, "check", f"ACS {YEAR} PUMS, Mexico-born arrived {C0}-{C1} at age 20+, n={len(everyone)}, "
                           f"weighted share with SCHL allocated {alloc:.4f}")
    out.to_csv(P.OUT / "acs_pums_check.csv", index=False, float_format="%.5f")
    print(out.to_string(index=False, float_format=lambda x: f"{x:.4f}"))


def estimates(origin: "P.Origin", d: pd.DataFrame, subset: str) -> list[dict]:
    census = P.ref_census(d, "nearest", P.MAIN_REF[C0])
    ridit, quint, mig5, mex5, bins = P.person_scores(d, origin, census, "own", FIVE, "empirical", {}, C0)
    stats = {"ridit": ridit, "q1": quint[:, 0], "q5": quint[:, 4],
             "mig_c1": mig5[:, 0], "mig_c5": mig5[:, 4], "diff_c1": mig5[:, 0] - mex5[:, 0],
             "diff_c5": mig5[:, 4] - mex5[:, 4]}
    cl = d.SERIAL.astype(str).to_numpy()
    w = d.PWGTP.to_numpy(float)
    rows = []
    for name, y in stats.items():
        theta, se_lin = P.lin_se(y, w, cl)
        reps = np.array([(d[r].to_numpy(float) * y).sum() / d[r].to_numpy(float).sum() for r in REP])
        se_rep = float(np.sqrt(4 / 80 * ((reps - theta) ** 2).sum()))
        rows.append({"subset": subset, "n": len(d), "statistic": name, "estimate_pums": theta,
                     "se_linearised": se_lin, "se_replicate": se_rep, "ratio_rep_to_lin": se_rep / se_lin})
    return rows


if __name__ == "__main__":
    main()

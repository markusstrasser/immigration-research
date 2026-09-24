"""Class size as a second measure of the same resource loss: how teachers follow pupils within districts.

Teachers (FTE): CCD fall 2000 from the Urban Institute directory endpoint (this lane's pull_ccd.py,
teachers_total_fte); CCD 2018-19 and 2023-24 LEA staff files (NCES file 059, STAFF = Teachers,
TOTAL_INDICATOR = "Derived - Major Staffing Category"). Pupils: F-33 V33 of the matching fiscal year
(fall 2000 = FY2001, fall 2018 = FY2019, fall 2023 = FY2024), so the ratio uses one pupil concept.
New York City's CCD geographic districts are merged into F-33's single unit.

  ld_2000_2018   log teachers change on log pupils change, FY2001 -> FY2019 | state
  ld_2018_2023   the same, FY2019 -> FY2024 | state
Pupil-weighted (base-year pupils) and unweighted; standard errors clustered by state. Districts with
at least 100 pupils, a pupil-teacher ratio of 5-40 at both ends, in one F-33 spell.

This measure is shown beside the spending channel and never added to it (brief, task 3).
Writes derived/class_size_elasticities.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow --with pyfixest \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/class_size.py
"""
import io
import sys
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import district_covariates as dc  # noqa: E402
from estimate_functions import load  # noqa: E402

OUT = HERE / "derived"
NCES = HERE / "_cache" / "nces"
STAFF = {2018: "ccd_lea_059_1819_l_1a_091019", 2023: "ccd_lea_059_2324_l_1a_073124"}
FY = {2000: 2001, 2018: 2019, 2023: 2024}


def teachers(fall):
    if fall == 2000:
        d = dc.directory(2000)
        d["t"] = pd.to_numeric(d.teachers_total_fte, errors="coerce")
        d = d[d.t.ge(0)]
        names = d.set_index("leaid").lea_name
        d = dc._nyc(d[["leaid", "t"]].copy(), names[~names.index.duplicated()])
        return d.groupby("leaid").t.sum()
    name = STAFF[fall]
    with zipfile.ZipFile(NCES / f"{name}.zip") as z:
        raw = z.read(f"{name}.csv")
    s = pd.read_csv(io.BytesIO(raw), dtype=str, encoding="latin-1",
                    usecols=["LEAID", "LEA_NAME", "STAFF", "STAFF_COUNT", "TOTAL_INDICATOR"])
    s = s[s.STAFF.eq("Teachers") & s.TOTAL_INDICATOR.eq("Derived - Major Staffing Category")].copy()
    s["t"] = pd.to_numeric(s.STAFF_COUNT, errors="coerce")
    s = s[s.t.ge(0)].rename(columns={"LEAID": "leaid"})
    s = dc._nyc(s[["leaid", "t"]].copy(), s.set_index("leaid").LEA_NAME[~s.set_index("leaid").index.duplicated()])
    return s.groupby("leaid").t.sum()


def main():
    d, _ = load(2024)
    rows, national = [], []
    for a, b in [(2000, 2018), (2018, 2023)]:
        ta, tb = teachers(a), teachers(b)
        x = d[d.year.eq(FY[a])].set_index("leaid")
        y = d[d.year.eq(FY[b])].set_index("leaid")
        common = x.index.intersection(y.index).intersection(ta.index).intersection(tb.index)
        common = common[x.loc[common, "spell"].values == y.loc[common, "spell"].values]
        f = pd.DataFrame({"fips": x.loc[common, "fips"], "na": x.loc[common, "V33"], "nb": y.loc[common, "V33"],
                          "ta": ta.loc[common], "tb": tb.loc[common]})
        f = f[f.ta.gt(0) & f.tb.gt(0)]
        f = f[(f.na / f.ta).between(5, 40) & (f.nb / f.tb).between(5, 40)]
        f["dlnN"], f["dlnT"] = np.log(f.nb / f.na), np.log(f.tb / f.ta)
        for wname, w in [("unweighted", None), ("pupils", "na")]:
            m = pf.feols("dlnT ~ dlnN | fips", data=f, vcov={"CRV1": "fips"}, weights=w)
            bb, se = float(m.coef()["dlnN"]), float(m.se()["dlnN"])
            rows.append({"spec": f"ld_{a}_{b}", "weight": wname, "teacher_elasticity": bb, "se": se,
                         "ci_low": bb - 1.96 * se, "ci_high": bb + 1.96 * se, "n_districts": int(m._N),
                         "ptr_start_pw": float(f.na.sum() / f.ta.sum()), "ptr_end_pw": float(f.nb.sum() / f.tb.sum())})
        national.append({"fall": b, "teachers_fte_m": float(tb.sum() / 1e6)})
    r = pd.DataFrame(rows)
    OUT.mkdir(exist_ok=True)
    r.to_csv(OUT / "class_size_elasticities.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(r.to_string(index=False))
    print(national)


if __name__ == "__main__":
    sys.exit(main())

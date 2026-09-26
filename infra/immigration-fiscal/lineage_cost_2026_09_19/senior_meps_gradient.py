"""Age gradients of care received, MEPS-HC 2022 (HC-243) and 2023 (HC-251), for pricing an
unauthorized senior's uncompensated care.

The uncompensated-care lane prices $1,524 per uninsured person-year at all ages. No survey
measures the uninsured past 65 (MEPS has 37 full-year uninsured aged 65+ in 2022-23), so this
reports two measured gradients and leaves the extrapolation to `senior_pricing_inputs.json`:

- among the full-year uninsured (INSCOVyy == 3), mean payments at 55-64 over the 0-64 mean,
  for everyone and for the foreign-born of Mexican origin (BORNUSA 2, HISPNCAT 1);
- among all persons, mean payments at 65-74, 75+ and 65+ over 55-64, the rise in care
  received past 65 when coverage is not the constraint.

Payments are MEPS total expenditure (all payers), not charges. Two years pooled with each
year's weight halved; Taylor SEs on the strata and PSUs.

Inputs: `_cache/meps/h243.dta` and `_cache/meps/h251.dta`, unzipped from
https://meps.ahrq.gov/data_files/pufs/h243dta.zip and .../h251dta.zip (ignored by git).
Run from the repository root:
    uv run --no-project python3 infra/immigration-fiscal/lineage_cost_2026_09_19/senior_meps_gradient.py
Writes derived/senior_meps_gradient.csv.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FILES = {22: HERE / "_cache/meps/h243.dta", 23: HERE / "_cache/meps/h251.dta"}
# The researcher's figures in senior_pricing_sources.md Q4 (table 4b), reproduced as a gate.
GATE = {("uninsured", "all", "55-64"): 1974.0, ("uninsured", "all", "0-64"): 1201.0,
        ("uninsured", "foreign_born_mexican", "55-64"): 1243.0}


def load(yy: int) -> pd.DataFrame:
    cols = [f"INSCOV{yy}", f"AGE{yy}X", f"PERWT{yy}F", "VARSTR", "VARPSU", f"TOTEXP{yy}",
            "BORNUSA", "HISPNCAT"]
    df = pd.read_stata(FILES[yy], columns=cols, convert_categoricals=False)
    df.columns = ["inscov", "age", "wt", "strat", "psu", "totexp", "bornusa", "hispcat"]
    df["strat"] = f"{yy}_" + df["strat"].astype(str)
    df["wt"] = df["wt"] / len(FILES)
    return df[df["wt"] > 0]


def mean_se(d: pd.DataFrame) -> tuple[float, float]:
    w, x = d["wt"].to_numpy(float), d["totexp"].to_numpy(float)
    m = (w * x).sum() / w.sum()
    z = w * (x - m) / w.sum()
    tot = pd.DataFrame({"s": d["strat"].to_numpy(), "p": d["psu"].to_numpy(), "z": z}) \
        .groupby(["s", "p"])["z"].sum().reset_index()
    var = 0.0
    for _, sg in tot.groupby("s"):
        n = len(sg)
        if n > 1:
            var += n / (n - 1) * ((sg["z"] - sg["z"].mean()) ** 2).sum()
    return float(m), float(np.sqrt(var))


def main() -> None:
    d = pd.concat([load(yy) for yy in FILES], ignore_index=True)
    bands = {"0-64": (0, 64), "55-64": (55, 64), "65-74": (65, 74), "75+": (75, 200), "65+": (65, 200)}
    pops = {("uninsured", "all"): d[d.inscov == 3],
            ("uninsured", "foreign_born_mexican"): d[(d.inscov == 3) & (d.bornusa == 2) & (d.hispcat == 1)],
            ("everyone", "all"): d}
    rows = []
    for (cover, grp), sub in pops.items():
        for band, (lo, hi) in bands.items():
            cell = sub[(sub.age >= lo) & (sub.age <= hi)]
            m, se = mean_se(cell)
            rows.append(dict(coverage=cover, group=grp, ages=band, n=len(cell),
                             mean_payments=round(m, 2), se=round(se, 2)))
    out = pd.DataFrame(rows)
    get = lambda c, g, a: float(out[(out.coverage == c) & (out.group == g) & (out.ages == a)].mean_payments.iloc[0])
    for (c, g, a), v in GATE.items():
        if abs(get(c, g, a) - v) > 1.0:
            raise SystemExit(f"[BLOCKED] {c}/{g}/{a} {get(c, g, a):.1f} does not reproduce {v}")
    ratios = [
        ("uninsured_55_64_over_0_64", get("uninsured", "all", "55-64") / get("uninsured", "all", "0-64")),
        ("uninsured_fb_mexican_55_64_over_all_0_64",
         get("uninsured", "foreign_born_mexican", "55-64") / get("uninsured", "all", "0-64")),
        ("everyone_65_74_over_55_64", get("everyone", "all", "65-74") / get("everyone", "all", "55-64")),
        ("everyone_75plus_over_55_64", get("everyone", "all", "75+") / get("everyone", "all", "55-64")),
        ("everyone_65plus_over_55_64", get("everyone", "all", "65+") / get("everyone", "all", "55-64")),
    ]
    ratio_rows = pd.DataFrame([dict(coverage="ratio", group=k, ages="", n=0, mean_payments=round(v, 6), se=np.nan)
                               for k, v in ratios])
    (HERE / "derived").mkdir(exist_ok=True)
    pd.concat([out, ratio_rows], ignore_index=True).to_csv(HERE / "derived/senior_meps_gradient.csv",
                                                           index=False, lineterminator="\n")
    print(out.to_string(index=False))
    for k, v in ratios:
        print(f"{k:45s} {v:.3f}")


if __name__ == "__main__":
    main()

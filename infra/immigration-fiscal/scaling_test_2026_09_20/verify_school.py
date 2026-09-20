"""Independent closed-form FWL check of the eight primary school regressions."""
import hashlib
import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t
from verification_guards import exact_models, finite_values

HERE = Path(__file__).resolve().parent
OUT = HERE/"derived"
(OUT/"school_verification.json").unlink(missing_ok=True)
audit = json.loads((OUT/"audit.json").read_text())
for path, expected in audit["inputs"].items():
    if hashlib.sha256(Path(path).read_bytes()).hexdigest() != expected:
        raise ValueError(f"Input drift: {path}")
for name, expected in audit["outputs"].items():
    if hashlib.sha256((OUT/f"{name}.csv").read_bytes()).hexdigest() != expected:
        raise ValueError(f"Output drift: {name}")
original = pd.read_csv(HERE.parent/"school_flight_2026_09_18/derived/district_panel.csv", dtype={"leaid": str})
original = original.loc[original.fips.ne(11)].copy()
results = pd.read_csv(OUT/"school_estimates.csv").query(
    "sample == 'existing_screen' and spec in ['cross_2019','within_district_state_year']")
exact_models(results, ["outcome", "spec", "weighted"],
             product(["log_current", "log_instruction"],
                     ["cross_2019", "within_district_state_year"], [False, True]),
             ["beta", "se", "low95", "high95", "n"])
errors = []
for row in results.to_dict("records"):
    raw = "exp_current_elsec_total" if row["outcome"] == "log_current" else "exp_current_instruction_total"
    d = original.loc[original[raw].gt(0)].copy()
    if row["spec"] == "cross_2019":
        d = d.loc[d.year.eq(2019)].copy()
        d["w"] = d.pupils if row["weighted"] else 1.
        absorbed = d.fips.nunique()
    else:
        valid = d.groupby("leaid").year.nunique().eq(3)
        d = d.loc[d.leaid.isin(valid.index[valid])].copy()
        initial = d.loc[d.year.eq(2000)].set_index("leaid").pupils
        d["w"] = d.leaid.map(initial) if row["weighted"] else 1.
        d["state_year"] = d.fips.astype(str)+"_"+d.year.astype(str)
        absorbed = d.leaid.nunique()+d.state_year.nunique()-d.fips.nunique()
    finite_values(d[["pupils", raw, "defl", "w"]])
    if (d[["pupils", raw, "defl", "w"]] <= 0).any().any() or d.duplicated(["leaid", "year"]).any():
        raise ValueError("Invalid school panel values or keys")
    d["x"], d["y"] = np.log(d.pupils), np.log(d[raw]*d.defl)
    def mean(column, group):
        return (d[column]*d.w).groupby(d[group]).transform("sum")/d.w.groupby(d[group]).transform("sum")
    for column in ["x", "y"]:
        if row["spec"] == "cross_2019":
            d[column+"r"] = d[column]-mean(column, "fips")
        else:
            d[column+"r"] = d[column]-mean(column, "leaid")-mean(column, "state_year")+mean(column, "fips")
    xx = (d.w*d.xr**2).sum()
    beta = (d.w*d.xr*d.yr).sum()/xx
    scores = (d.w*d.xr*(d.yr-beta*d.xr)).groupby(d.fips).sum()
    n, g, k = len(d), d.fips.nunique(), absorbed+1
    se = np.sqrt((scores**2).sum()/xx**2 * g/(g-1)*(n-1)/(n-k))
    interval = beta+t.ppf(.975, g-1)*np.array([-se, se])
    finite_values([beta, se, *interval])
    error = max(abs(beta-row["beta"]), abs(se-row["se"]), abs(interval[0]-row["low95"]), abs(interval[1]-row["high95"]))
    finite_values(error)
    if error > 1e-9 or n != row["n"]:
        raise ValueError(f"Independent regression mismatch: {row}: {error}")
    errors.append(float(error))
result = dict(verified_primary_models=len(errors), max_abs_error=max(errors),
              method="Closed-form balanced-panel FWL and scalar cluster scores; producer not imported")
(OUT/"school_verification.json").write_text(json.dumps(result, indent=2)+"\n")
print(result)

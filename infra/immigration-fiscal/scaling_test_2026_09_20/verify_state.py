"""Independent FWL coefficient and cluster covariance check."""
from pathlib import Path
from itertools import product
import json
import hashlib
import numpy as np
import pandas as pd
from verification_guards import exact_models, finite_values
HERE=Path(__file__).resolve().parent / "derived" / "state"
receipt = HERE/"verification.json"
receipt.unlink(missing_ok=True)
audit=json.loads((HERE/"audit.json").read_text())
for name, expected in audit["hashes"].items():
    if hashlib.sha256((Path(__file__).resolve().parent.parent/name).read_bytes()).hexdigest() != expected:
        raise ValueError(f"Input drift: {name}")
for name, expected in audit["output_hashes"].items():
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != expected:
        raise ValueError(f"Output drift: {name}")
if hashlib.sha256((Path(__file__).parent/"state_analyze.py").read_bytes()).hexdigest() != audit["producer_sha256"]:
    raise ValueError("Producer drift")
d=pd.read_csv(HERE/"panel.csv")
r=pd.read_csv(HERE/"estimates.csv")
functions = ["k12", "higher_core", "admin", "police", "fire", "highways_nontoll",
             "parks", "libraries", "health", "hospitals"]
samples = {"all": [2012, 2017, 2018, 2019, 2021, 2022, 2023],
           "census": [2012, 2017, 2022], "pre2020": [2012, 2017, 2018, 2019]}
exact_models(r, ["function", "sample", "model"],
             product(functions, samples, ["year_fe", "state_year_fe"]),
             ["beta", "se_cluster_state_CR1", "ci_low", "ci_high", "n", "clusters", "ci_df"])
finite_values(d[["population"]+functions])
if d.duplicated(["state", "year"]).any() or (d[["population"]+functions] <= 0).any().any():
    raise ValueError("Invalid panel keys or nonpositive values")
errors=[]
for row in r.to_dict("records"):
    years=list(map(int,row["years"].split(";")))
    if years != samples[row["sample"]]:
        raise ValueError("Unexpected year coverage")
    z=d.loc[d.year.isin(years), ["state","year","population",row["function"]]].copy()
    z["x"]=np.log(z.population)
    z["y"]=np.log(z[row["function"]])
    for name in ["x","y"]:
        if row["model"]=="state_year_fe":
            z[name+"r"]=z[name]-z.groupby("state")[name].transform("mean")-z.groupby("year")[name].transform("mean")+z[name].mean()
        else:
            z[name+"r"]=z[name]-z.groupby("year")[name].transform("mean")
    beta=(z.xr*z.yr).sum()/(z.xr*z.xr).sum()
    z["score"]=z.xr*(z.yr-beta*z.xr)
    n=len(z);G=z.state.nunique();K=2+len(years)-1+(G-1 if row["model"]=="state_year_fe" else 0)
    variance=(z.groupby("state").score.sum()**2).sum()/(z.xr*z.xr).sum()**2*(G/(G-1))*((n-1)/(n-K))
    se=np.sqrt(variance)
    finite_values([beta, se, row["beta"], row["se_cluster_state_CR1"]])
    error=max(abs(beta-row["beta"]),abs(se-row["se_cluster_state_CR1"]))
    finite_values(error)
    if error>1e-8 or n != 50*len(years) or n != row["n"] or G != 50 or row["clusters"] != G or row["ci_df"] != G-1:
        raise ValueError(f"Independent mismatch {row}: {error}")
    errors.append(error)
result={"verified_models":len(errors),"max_abs_coefficient_or_se_difference":max(errors),"method":"balanced-panel FWL residualization and scalar cluster scores; producer not imported"}
(HERE/"verification.json").write_text(json.dumps(result,indent=2))
print(result)

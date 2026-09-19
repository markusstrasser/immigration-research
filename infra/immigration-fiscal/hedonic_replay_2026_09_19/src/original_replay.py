"""Translate the archived Saiz-Wachter Table 1 commands; no Stata execution."""
from pathlib import Path
import hashlib
from importlib.metadata import version
import json
import sys

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parents[1]
SOURCE = LANE / "_cache/original/DATAAEJPOL2009-0191"
DATA = SOURCE / "DATAAEJPOLICY_MS_2009_191.dta"
OUT = LANE / "derived"
sys.path.insert(0, str(LANE.parent / "hedonic_composition_2026_09_19/src"))
import estim

SES = ["l1sharebach", "l1loinc", "l1shanhwhite", "l1shaless25",
       "l1shamore65", "l1shafakid", "l1shaown", "l1vacrat", "l1loden"]
PRETREND = ["shawa", "shacim", "l1loval", "l1dloval", "l1dloinc"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(d, columns):
    return hashlib.sha256(d[columns].to_csv(index=False, float_format="%.17g").encode()).hexdigest()


def load():
    assert sha(DATA) == "56ed0dcb0472cdeb75dd88a3938fbd32d831463bd696afda1cc6a765ffe5d833"
    d = pd.read_stata(DATA, convert_categoricals=False)
    numeric = d.select_dtypes(include="number").columns
    d[numeric] = d[numeric].astype(float)
    assert not d.duplicated(["tract", "year"]).any()
    # Stata wildcards follow dataset order, not alphabetical order.
    controls = [c for c in d if c.startswith("cha")]
    controls += [c for c in d if c.startswith("Ql1")]
    controls += SES
    assert len(controls) == 43
    d = d[~d.year.isin([1970, 1980]) & d.immicapmsa.notna() & (d.immicapmsa > .05)]
    assert d.msayear.nunique() == 122
    return d, controls


def sample(d, controls, outcome="dloval", iv=None, require=None):
    cols = list(dict.fromkeys([outcome, "dforeigncap", "l1own", "msayear", "tract"]
                             + controls + (iv or []) + (require or [])))
    return d[np.isfinite(d[cols]).all(axis=1) & (d.l1own > 0)].copy()


def design(d, controls, outcome="dloval", iv=None):
    columns = list(dict.fromkeys([outcome, "dforeigncap"] + controls + (iv or [])))
    x = d[columns].copy()
    for c in controls + (iv or []):
        # Repeated variables are disallowed: their transformations must be unique.
        assert (controls + (iv or [])).count(c) == 1
        x[c] = (x[c] - x[c].mean()) / x[c].std()
    w = d.l1own / d.l1own.mean()
    dm = estim.wdemean(x, columns, d.msayear, w)
    return x, dm, w


def fit(d, arm, controls, outcome="dloval", iv=None, require=None):
    d = sample(d, controls, outcome, iv, require)
    _, dm, w = design(d, controls, outcome, iv)
    kfe = d.msayear.nunique()
    if iv:
        res = estim.tsls(dm[outcome], dm[["dforeigncap"]], dm[controls], dm[iv],
                         w, d.tract, ["dforeigncap"], controls, k_absorbed=kfe)
    else:
        res = estim.wls(dm[outcome], dm[["dforeigncap"] + controls], w, d.tract,
                        ["dforeigncap"] + controls, k_absorbed=kfe)
    row = estim.row(res, "dforeigncap")
    row.pop("J_p", None)  # Not a verified Stata ivreg2 Hansen J implementation.
    row.pop("J_status", None)
    n, k, g = len(d), 1 + len(controls) + kfe, d.tract.nunique()
    correction = g / (g - 1) * (n - 1) / (n - k)
    tss = float(np.sum(w * (d[outcome] - np.average(d[outcome], weights=w)) ** 2))
    row.update(arm=arm, controls=len(controls), msa_periods=kfe,
               se_asymptotic=row["se"] / np.sqrt(correction),
               se_finite_sample=row["se"], covariance="cluster_finite_sample",
               r2_overall=1 - float(res["resid"] @ res["resid"]) / tss,
               row_hash=digest(d, ["tract", "year"]),
               matrix_hash=digest(d, [outcome, "dforeigncap", "l1own", "msayear", "tract"] + controls + (iv or [])))
    # ivreg2 defaults to asymptotic covariance; areg/ivreg use finite-sample scaling.
    if arm in {"table1_col5", "table1_col6"}:
        row["se"] = row["se_asymptotic"]
        row["t"] = row["coef"] / row["se"]
        row["covariance"] = "cluster_asymptotic_ivreg2_no_small"
    return row


def specs(controls):
    return [
        ("table1_col1", [], None, ["l1shanhwhite"]),
        ("table1_col2", controls, None, None),
        ("table1_col3", controls + PRETREND, None, None),
        ("table1_col4", controls, ["pull"], None),
        ("table1_col5", controls + ["l1foreigncap"], ["pull", "pulli", "pullmsa"], None),
        ("table1_col6", controls + ["l1foreigncap", "pull"], ["pulli", "pullmsa"], None),
    ]


def first_stage(d, controls, iv, arm, require=None):
    d = sample(d, controls, "dforeigncap", iv, require)
    _, dm, w = design(d, controls, "dforeigncap", iv)
    names = iv + controls
    res = estim.wls(dm.dforeigncap, dm[names], w, d.tract, names,
                    k_absorbed=d.msayear.nunique())
    q = len(iv)
    beta = res["beta"][:q]
    f = float(beta @ np.linalg.solve(res["V"][:q, :q], beta) / q)
    # Also compute the classical excluded-instrument F as a diagnostic.
    rw = np.sqrt(w.to_numpy())
    y, x = dm.dforeigncap.to_numpy() * rw, dm[names].to_numpy() * rw[:, None]
    classical_v = np.linalg.inv(x.T @ x) * (res["resid"] @ res["resid"]) / (len(d) - len(names) - d.msayear.nunique())
    classical_f = float(beta @ np.linalg.solve(classical_v[:q, :q], beta) / q)
    rows = []
    for c in iv + (["l1foreigncap"] if "l1foreigncap" in controls else []):
        i = names.index(c)
        rows.append(dict(arm=arm, variable=c, coef=res["beta"][i] / d[c].std(),
                         se=res["se"][i] / d[c].std(), F_cluster=f, F_classical=classical_f,
                         n=len(d), clusters=d.tract.nunique(), row_hash=digest(d, ["tract", "year"])))
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    d, controls = load()
    rows = [fit(d, arm, c, iv=z, require=r) for arm, c, z, r in specs(controls)]
    # Paper prose lists high-school dropout, which the archived commands omit.
    rows.append(fit(d, "baseline_add_paper_dropout", controls + ["l1sharedrop"]))
    rows.append(fit(d, "col3_without_archived_land_use", controls + PRETREND[2:]))
    # Recover appendix median-value result and isolate the outcome on identical rows.
    rows.append(fit(d, "appendix_table2_col4_median", controls, outcome="dlomval"))
    common = sample(sample(d, controls), controls, outcome="dlomval")
    rows.append(fit(common, "matched_mean", controls))
    rows.append(fit(common, "matched_median", controls, outcome="dlomval"))
    assert rows[-1]["row_hash"] == rows[-2]["row_hash"]
    results = pd.DataFrame(rows)
    results.to_csv(OUT / "original_results.csv", index=False)
    first = []
    for arm, c, z, required in specs(controls)[3:]:
        first += first_stage(d, c, z, arm + "_estimation_rows", ["dloval"])
    first += first_stage(d, controls, ["pull"], "appendix_table3_col1")
    first += first_stage(d, controls + ["l1foreigncap", "pull"], ["pulli", "pullmsa"], "appendix_table3_col2")
    pd.DataFrame(first).to_csv(OUT / "original_first_stages.csv", index=False)
    targets = json.loads((LANE / "table1_targets.json").read_text())
    matches = []
    for target, row in zip(targets["columns"], rows):
        matches.append(dict(column=target["column"], n_match=bool(row["n"] == target["n"]),
                            coef_match=bool(abs(row["coef"] - target["coef"]) <= .0005),
                            se_match=bool(abs(row["se"] - target["se"]) <= .0005),
                            asymptotic_se_match=bool(abs(row["se_asymptotic"] - target["se"]) <= .0005)))
    manifest = dict(data_sha256=sha(DATA), author_code_sha256=sha(SOURCE / "AEJPOLICY-MS2009-0191.do"),
                    supplemental_code_sha256=sha(SOURCE / "AEJPOLICY-MS2009-0191-SUPPLEMENTAL-RESULTS.do"),
                    translation_sha256=sha(Path(__file__)), estimator_sha256=sha(Path(estim.__file__)),
                    packages={p: version(p) for p in ["numpy", "pandas", "scipy"]},
                    controls=controls, archived_control_count=len(controls),
                    interpretation="Python translation; raw construction and native Stata execution not reproduced",
                    table1_matches=matches)
    (OUT / "original_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(results[["arm", "coef", "se", "se_asymptotic", "n", "F_first", "r2_overall"]].to_string(index=False))
    print(pd.DataFrame(first).drop(columns="row_hash").to_string(index=False))
    print(json.dumps(matches, indent=2))


if __name__ == "__main__":
    main()

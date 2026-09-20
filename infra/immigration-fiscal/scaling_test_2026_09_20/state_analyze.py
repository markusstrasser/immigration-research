"""Descriptive state-service scaling; no causal immigration calibration."""
from pathlib import Path
import hashlib
import json
import zipfile
import numpy as np
import pandas as pd
from scipy.stats import t

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "derived" / "state"
YEARS = [2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
FUNCTIONS = {"k12": ["E12"], "higher_core": ["E16"], "admin": ["E23", "E29", "E31"],
             "police": ["E62"], "fire": ["E24"], "highways_nontoll": ["E44"],
             "parks": ["E61"], "libraries": ["E52"], "health": ["E32"], "hospitals": ["E36"]}
CODES = sorted(set(sum(FUNCTIONS.values(), []) + ["E18", "E45"]))
EXPECTED = json.loads((ROOT/"administration_response_2026_09_20/inputs.sha256.json").read_text())
HASHES = {}


def pin(path):
    key = str(path.relative_to(ROOT))
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    if EXPECTED.get(key) != value:
        raise ValueError(f"Unreviewed source bytes: {key}")
    HASHES[key] = value


def member(z, ending):
    hits = [x for x in z.namelist() if Path(x).name.lower() == ending.lower()]
    if len(hits) != 1:
        raise ValueError(f"Expected exactly one {ending}: {hits}")
    return hits[0]


def extract():
    rows = []
    missing = []
    for year in YEARS:
        path = ROOT/f"local_spending_composition_2026_09_18/_cache/indunit_{year}.zip"
        pin(path)
        with zipfile.ZipFile(path) as z:
            mapping = {0: 0}
            if year == 2012:
                for line in z.read(member(z, "Fin_GID_2012.txt")).decode("latin-1").splitlines():
                    if len(line) >= 118 and line[:2].isdigit() and line[113:115].isdigit():
                        old, new = int(line[:2]), int(line[113:115])
                        if old in mapping and mapping[old] != new:
                            raise ValueError("Inconsistent state mapping")
                        mapping[old] = new
            for line in z.read(member(z, f"{year%100}statetypepu.txt")).decode("latin-1").splitlines():
                parts = line.split()
                if len(parts) < 2 or parts[1] not in CODES:
                    continue
                statelevel, code = parts[:2]
                if len(statelevel) != 3 or statelevel[2] != "1":
                    continue
                state = int(statelevel[:2])
                if year == 2012:
                    state = mapping[state]
                if len(parts) == 2:
                    missing.append([year, state, code])
                    continue
                if len(parts) != 5:
                    raise ValueError(f"Unrecognized selected record {line!r}")
                amount, cv, vintage = float(parts[2]), float(parts[3]), int(parts[4])
                if vintage != year % 100 or amount < 0 or cv < 0:
                    raise ValueError(f"Invalid values {line!r}")
                rows.append([year, state, code, amount, cv])
    d = pd.DataFrame(rows, columns=["year", "state", "code", "amount_thousands", "cv"])
    if d.duplicated(["year", "state", "code"]).any():
        raise ValueError("Duplicate finance keys")
    return d, missing


def validate(d):
    p = ROOT/"macro_closure_2026_09_19/_cache/finance_2022_us_combined.json"
    pin(p)
    api = json.loads(p.read_text())
    values = {r[0]: float(r[6]) for r in api[1:]}
    # LF higher education includes auxiliary E18; highways includes toll E45.
    bridges = {"LF0114": ["E12"], "LF0111": ["E16", "E18"], "LF0181": ["E23"],
               "LF0190": ["E29"], "LF0187": ["E31"], "LF0154": ["E62"], "LF0157": ["E24"],
               "LF0142": ["E44", "E45"], "LF0169": ["E61"], "LF0121": ["E52"],
               "LF0133": ["E32"], "LF0130": ["E36"]}
    national = d.query("year == 2022 and state == 0").set_index("code").amount_thousands
    anchors = []
    for field, codes in bridges.items():
        actual = national.loc[codes].sum()
        anchors.append({"api_field": field, "codes": "+".join(codes), "observed_thousands": actual,
                        "api_thousands": values[field], "difference": actual-values[field]})
        if actual != values[field]:
            raise ValueError(f"API anchor mismatch {field}: {actual} vs {values[field]}")
    max_error = 0
    for (year, code), g in d.groupby(["year", "code"]):
        actual = g.loc[g.state.ne(0), "amount_thousands"].sum()
        expected = g.loc[g.state.eq(0), "amount_thousands"].item()
        max_error = max(max_error, abs(actual-expected))
        if abs(actual-expected) > 52:
            raise ValueError(f"State sum mismatch {year} {code}: {actual-expected}")
    return anchors, max_error


def panel(d):
    p = ROOT/"tiebout_sorting_2026_09_18/_cache/state_covariates.csv"
    pin(p)
    pop = pd.read_csv(p)[["state", "year", "B01003_001E"]].rename(columns={"B01003_001E": "population"})
    pop[["state", "year"]] = pop[["state", "year"]].astype(int)
    if pop.duplicated(["state", "year"]).any():
        raise ValueError("Duplicate population keys")
    wide = d.loc[~d.state.isin([0, 11, 72])].pivot(index=["state", "year"], columns="code", values="amount_thousands").reset_index()
    wide = wide.merge(pop, on=["state", "year"], how="left", validate="one_to_one")
    gaps = sorted(wide.loc[wide.population.isna(), "year"].unique().tolist())
    if gaps != [2020]:
        raise ValueError(f"Unexpected population gaps {gaps}")
    wide = wide.loc[wide.year.ne(2020)].copy()
    if len(wide) != 350 or wide.state.nunique() != 50 or wide.population.le(0).any():
        raise ValueError("Unexpected panel dimensions")
    for function, codes in FUNCTIONS.items():
        wide[function] = wide[codes].sum(axis=1, min_count=len(codes))
    return wide


def fit(d, function, model, sample):
    d = d.loc[d[function].gt(0) & d.population.gt(0)].copy()
    y = np.log(d[function].to_numpy())
    x = np.log(d.population.to_numpy())
    terms = [np.ones((len(d), 1)), x[:, None], pd.get_dummies(d.year, drop_first=True).to_numpy(dtype=float)]
    if model == "state_year_fe":
        terms.append(pd.get_dummies(d.state, drop_first=True).to_numpy(dtype=float))
    X = np.column_stack(terms)
    n, k = X.shape
    if np.linalg.matrix_rank(X) != k:
        raise ValueError("Rank deficient model")
    bread = np.linalg.inv(X.T@X)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    errors = y-X@beta
    clusters = d.state.to_numpy()
    unique = np.unique(clusters)
    G = len(unique)
    scores = np.array([X[clusters==g].T@errors[clusters==g] for g in unique])
    covariance = bread@(scores.T@scores)@bread*(G/(G-1))*((n-1)/(n-k))
    se = float(np.sqrt(covariance[1,1]))
    critical = float(t.ppf(0.975, G-1))
    b = float(beta[1])
    return {"function": function, "model": model, "sample": sample, "beta": b, "se_cluster_state_CR1": se,
            "ci_low": b-critical*se, "ci_high": b+critical*se, "n": n, "clusters": G,
            "ci_df": G-1, "years": ";".join(map(str, sorted(d.year.unique()))),
            "p_beta_equals_1": 2*float(t.sf(abs((b-1)/se), G-1)),
            "p_beta_equals_0_85": 2*float(t.sf(abs((b-.85)/se), G-1)),
            "p_beta_equals_0_75": 2*float(t.sf(abs((b-.75)/se), G-1))}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = OUT/"audit.json"
    if receipt.exists():
        receipt.unlink()
    raw, missing = extract()
    anchors, max_error = validate(raw)
    d = panel(raw)
    results = []
    for function in FUNCTIONS:
        for sample, subset in [("all", d), ("census", d.loc[d.year.isin([2012,2017,2022])]), ("pre2020", d.loc[d.year.lt(2020)])]:
            for model in ["year_fe", "state_year_fe"]:
                results.append(fit(subset, function, model, sample))
    raw.to_csv(OUT/"selected_finance.csv", index=False)
    d.to_csv(OUT/"panel.csv", index=False)
    pd.DataFrame(results).to_csv(OUT/"estimates.csv", index=False)
    pd.DataFrame(anchors).to_csv(OUT/"national_2022_anchors.csv", index=False)
    outputs = ["selected_finance.csv", "panel.csv", "estimates.csv", "national_2022_anchors.csv"]
    (OUT/"audit.json").write_text(json.dumps({"hashes": HASHES,
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "output_hashes": {name: hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in outputs},
        "panel_n": len(d), "states": d.state.nunique(),
        "missing_records": missing, "missing_population_year_excluded": 2020,
        "max_national_state_sum_rounding_thousands": max_error,
        "missing_outcomes": {f: int(d[f].isna().sum()) for f in FUNCTIONS},
        "zero_outcomes": {f: int(d[f].eq(0).sum()) for f in FUNCTIONS},
        "model_count": len(results), "inference": "two-sided t(G-1), state-clustered CR1; no multiplicity adjustment"}, indent=2))
    print(pd.DataFrame(results).query("sample == 'all'")[["function","model","beta","ci_low","ci_high","n"]].to_string(index=False))


if __name__ == "__main__":
    main()

"""Attack on item 3 of main_case_candidate_2026_09_28: is the road stock's response measurable here?

The candidate puts the fixed stock beside the range because "no measured response here supports it or excludes it:
the operations regressions do not measure the stock". The low-end road response (0.727 across states) is fitted on
state-local current operations (Census code E44, scaling_test_2026_09_20). The same pinned Census files carry nontoll
highway construction (F44), the capital outlay that builds and replaces the stock. If the stock scales with
population across states, construction does too. This probe refits the scaling test's own model on F44.

Read-only; writes nothing. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/candidate_attack_2026_09_28/probe_road_stock.py
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import io
import zipfile

import numpy as np
import pandas as pd
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]  # infra/immigration-fiscal
YEARS = [2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
CODES = ["E44", "F44", "E45", "F45"]
S = 0.12024478903339636
r_of = lambda b: (1 - (1 - S) ** b) / S


def extract():
    rows = []
    for year in YEARS:
        with zipfile.ZipFile(ROOT / f"local_spending_composition_2026_09_18/_cache/indunit_{year}.zip") as z:
            mapping = {0: 0}
            if year == 2012:  # scaling_test_2026_09_20/state_analyze.py extract(): the 2012 state recode
                name = [x for x in z.namelist() if Path(x).name.lower() == "fin_gid_2012.txt"][0]
                for line in z.read(name).decode("latin-1").splitlines():
                    if len(line) >= 118 and line[:2].isdigit() and line[113:115].isdigit():
                        mapping[int(line[:2])] = int(line[113:115])
            name = [x for x in z.namelist() if Path(x).name.lower() == f"{year % 100}statetypepu.txt"][0]
            for line in z.read(name).decode("latin-1").splitlines():
                p = line.split()
                if len(p) != 5 or p[1] not in CODES or len(p[0]) != 3 or p[0][2] != "1":
                    continue
                state = int(p[0][:2])
                rows.append([year, mapping[state] if year == 2012 else state, p[1], float(p[2])])
    d = pd.DataFrame(rows, columns=["year", "state", "code", "amount"])
    return d.pivot_table(index=["state", "year"], columns="code", values="amount").reset_index()


def fit(d, y, extra=(), fe="year"):
    d = d.loc[d[y].gt(0)]
    cols = [np.log(d.population.to_numpy())] + [d[e].to_numpy(float) for e in extra]
    terms = [np.ones(len(d))] + cols + [pd.get_dummies(d.year, drop_first=True).to_numpy(float)]
    if fe == "state_year":
        terms.append(pd.get_dummies(d.state, drop_first=True).to_numpy(float))
    X = np.column_stack(terms)
    yy = np.log(d[y].to_numpy())
    n, k = X.shape
    bread = np.linalg.inv(X.T @ X)
    beta = np.linalg.lstsq(X, yy, rcond=None)[0]
    err = yy - X @ beta
    cl = d.state.to_numpy()
    groups = np.unique(cl)
    G = len(groups)
    sc = np.array([X[cl == g].T @ err[cl == g] for g in groups])
    cov = bread @ (sc.T @ sc) @ bread * (G / (G - 1)) * ((n - 1) / (n - k))
    se = float(np.sqrt(cov[1, 1]))
    return float(beta[1]), se, float(t.ppf(0.975, G - 1)), n, G


w = extract()
pop = pd.read_csv(ROOT / "tiebout_sorting_2026_09_18/_cache/state_covariates.csv")[["state", "year", "B01003_001E"]]
pop = pop.rename(columns={"B01003_001E": "population"}).astype({"state": int, "year": int})
d = w.loc[~w.state.isin([0, 11, 72])].merge(pop, on=["state", "year"], how="left")
d = d.loc[d.year.ne(2020)].copy()
with zipfile.ZipFile(ROOT / "service_response_long_run_2026_09_27/_cache/2020_Gaz_counties_national.zip") as z:
    g = pd.read_csv(io.StringIO(z.read("2020_Gaz_counties_national.txt").decode("latin-1")), sep="\t", dtype={"GEOID": str})
g.columns = [c.strip() for c in g.columns]
land = g.assign(state=g.GEOID.str[:2].astype(int)).groupby("state").ALAND.sum()
d["log_land"] = np.log(d.state.map(land))
p12 = d.loc[d.year.eq(2012)].set_index("state").population
p23 = d.loc[d.year.eq(2023)].set_index("state").population
d["growth"] = d.state.map(np.log(p23 / p12))
d["total"] = d.E44 + d.F44

pub = pd.read_csv(ROOT / "scaling_test_2026_09_20/derived/state/panel.csv")
chk = d.merge(pub[["state", "year", "highways_nontoll"]], on=["state", "year"])
print(f"[gate] panel {len(d)} rows, {d.state.nunique()} states; E44 equals the scaling test's highways_nontoll on "
      f"{int((chk.E44 == chk.highways_nontoll).sum())}/{len(chk)} rows")
b, se, crit, n, G = fit(d, "E44")
print(f"[gate] E44, year effects: {b:.6f} (the scaling test's 0.726607)")
nat = d.groupby("year")[["E44", "F44"]].sum().mean()
print(f"  mean over years of the 50-state sums ($bn): operations E44 {nat.E44 / 1e6:.1f}, construction F44 {nat.F44 / 1e6:.1f}\n")

print(f"{'outcome':32s} {'model':28s} {'b':>7s} {'SE':>6s} {'95% CI':>16s} {'r(b)':>7s}  n  states")
for y, lab in [("E44", "operations (E44)"), ("F44", "construction (F44)"), ("total", "operations + construction")]:
    for extra, fe, mlab in [((), "year", "year effects"), (("log_land",), "year", "+ log land"),
                            (("log_land", "growth"), "year", "+ log land + growth 2012-23"),
                            ((), "state_year", "state and year effects")]:
        b, se, crit, n, G = fit(d, y, extra, fe)
        print(f"{lab:32s} {mlab:28s} {b:7.3f} {se:6.3f} [{b - crit * se:6.3f}, {b + crit * se:6.3f}] {r_of(b):7.4f} {n:3d} {G}")
# Lumpiness: construction averaged over the seven years, one cross-section of 50 states.
m = d.groupby("state").agg(F44=("F44", "mean"), E44=("E44", "mean"), population=("population", "mean"), log_land=("log_land", "first"))
for y in ("E44", "F44"):
    X = np.column_stack([np.ones(len(m)), np.log(m.population), m.log_land])
    beta, res, *_ = np.linalg.lstsq(X, np.log(m[y]), rcond=None)
    e = np.log(m[y]) - X @ beta
    V = np.linalg.inv(X.T @ X) * (e @ e) / (len(m) - 3)
    print(f"{'state means, ' + y:32s} {'+ log land (50 obs, OLS)':28s} {beta[1]:7.3f} {np.sqrt(V[1, 1]):6.3f} {'':16s} {r_of(beta[1]):7.4f}  50")

"""Disconfirmation check on the low-end highway and park responses: do they survive a land-area control?

The low end reads the across-state elasticity of state-local current operations on population
(scaling_test_2026_09_20, year effects): 0.727 for nontoll highways, 0.948 for parks. Small-population
states include large, sparse ones (Alaska, Montana, Wyoming, the Dakotas) with long road networks per
resident, so part of that slope could be geography rather than scale. A removal of the group takes
residents out of existing states and metros without changing their land. This script refits the
scaling test's own model (log spending on log population, year effects, state-clustered CR1, t(49)) with
log land area added, after reproducing its published estimates exactly.

Land area: 2020 Census Gazetteer counties file, ALAND summed by state. Fetched once into _cache/:
  https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2020_Gazetteer/2020_Gaz_counties_national.zip
Writes derived/land_check.csv and derived/gates_land.json; stops with [BLOCKED] on a failed gate.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/service_response_long_run_2026_09_27/land_check.py
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
PANEL = FISCAL / "scaling_test_2026_09_20" / "derived" / "state" / "panel.csv"
ESTIMATES = FISCAL / "scaling_test_2026_09_20" / "derived" / "state" / "estimates.csv"
GAZ = HERE / "_cache" / "2020_Gaz_counties_national.zip"
GAZ_SHA = "02ef546e4c4f9c032c19616eabb9526caa016f778f41ede3b8c9755dacce20ef"
T975_49 = 2.009575234489209  # t(0.975, 49 df), the scaling test's critical value (scipy.stats.t.ppf); gated below
FUNCTIONS = ("highways_nontoll", "parks", "admin")
GATES: list[dict] = []


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def fit(d, function, extra=None):
    """The scaling test's fit(): OLS with year effects, state-clustered CR1; returns every slope."""
    d = d.loc[d[function].gt(0) & d.population.gt(0)]
    y = np.log(d[function].to_numpy())
    names = ["log_population"] + ([extra] if extra else [])
    cols = [np.log(d.population.to_numpy())] + ([np.log(d[extra].to_numpy())] if extra else [])
    X = np.column_stack([np.ones(len(d))] + cols + [pd.get_dummies(d.year, drop_first=True).to_numpy(dtype=float)])
    n, k = X.shape
    if np.linalg.matrix_rank(X) != k:
        raise SystemExit("[BLOCKED] rank-deficient model")
    bread = np.linalg.inv(X.T @ X)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    err = y - X @ beta
    cl = d.state.to_numpy()
    groups = np.unique(cl)
    G = len(groups)
    scores = np.array([X[cl == g].T @ err[cl == g] for g in groups])
    cov = bread @ (scores.T @ scores) @ bread * (G / (G - 1)) * ((n - 1) / (n - k))
    out = {}
    for i, name in enumerate(names, start=1):
        se = float(np.sqrt(cov[i, i]))
        out[name] = {"b": float(beta[i]), "se": se, "ci": [float(beta[i]) - T975_49 * se, float(beta[i]) + T975_49 * se]}
    return out, n, G


def main():
    print("[inputs]")
    gate("gazetteer file is the fetched one", hashlib.sha256(GAZ.read_bytes()).hexdigest() == GAZ_SHA, GAZ_SHA[:12])
    with zipfile.ZipFile(GAZ) as z:
        text = z.read("2020_Gaz_counties_national.txt").decode("latin-1")
    g = pd.read_csv(io.StringIO(text), sep="\t", dtype={"GEOID": str})
    g.columns = [c.strip() for c in g.columns]
    g["state"] = g.GEOID.str[:2].astype(int)
    land = g.groupby("state").ALAND.sum().rename("land_m2").reset_index()
    panel = pd.read_csv(PANEL)
    d = panel.merge(land, on="state", how="left", validate="many_to_one")
    gate("every panel state has land area", d.land_m2.notna().all() and d.state.nunique() == 50 and len(d) == 350,
         f"{d.state.nunique()} states, {len(d)} rows")
    gate("US land area is the gazetteer's 3.53m sq mi (50 states + DC + PR)",
         abs(g.ALAND_SQMI.sum() / 1e6 - 3.53) < 0.02, f"{g.ALAND_SQMI.sum() / 1e6:.3f}m sq mi")
    pub = {(r["function"], r["model"]): r for r in csv.DictReader(ESTIMATES.open()) if r["sample"] == "all"}

    print("\n[reproduce, then add land]")
    rows = []
    for f in FUNCTIONS:
        base, n, G = fit(d, f)
        p = pub[(f, "year_fe")]
        gate(f"{f}: reproduces the scaling test's year-effects estimate",
             abs(base["log_population"]["b"] - float(p["beta"])) < 1e-12 and abs(base["log_population"]["se"] - float(p["se_cluster_state_CR1"])) < 1e-12
             and abs(base["log_population"]["ci"][0] - float(p["ci_low"])) < 1e-9, f"{base['log_population']['b']:.6f}")
        withland, _, _ = fit(d, f, "land_m2")
        rows.append({"function": f, "model": "year_fe", "control": "none", "slope": "log_population", **base["log_population"], "n": n, "states": G})
        for name, v in withland.items():
            rows.append({"function": f, "model": "year_fe", "control": "log_land_area", "slope": name, **v, "n": n, "states": G})
    corr = float(np.corrcoef(np.log(d.population), np.log(d.land_m2))[0, 1])

    if not all(x["passed"] for x in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not x['passed'] for x in GATES)} gate(s) failed; nothing written")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["function", "model", "control", "slope", "b", "se", "ci_low", "ci_high", "n", "states"])
    for r in rows:
        w.writerow([r["function"], r["model"], r["control"], r["slope"], f"{r['b']:.10g}", f"{r['se']:.10g}",
                    f"{r['ci'][0]:.10g}", f"{r['ci'][1]:.10g}", r["n"], r["states"]])
    (HERE / "derived" / "land_check.csv").write_text(buf.getvalue())
    (HERE / "derived" / "gates_land.json").write_text(json.dumps({"gates": GATES, "corr_log_pop_log_land": corr,
                                                                 "gazetteer_sha256": GAZ_SHA}, indent=1) + "\n")
    print(f"\n  corr(log population, log land) = {corr:.3f}")
    for r in rows:
        print(f"  {r['function']:17s} {r['control']:14s} {r['slope']:15s} {r['b']:.4f} (SE {r['se']:.4f}) [{r['ci'][0]:.3f}, {r['ci'][1]:.3f}]")
    print(f"all {len(GATES)} gates passed")


if __name__ == "__main__":
    main()

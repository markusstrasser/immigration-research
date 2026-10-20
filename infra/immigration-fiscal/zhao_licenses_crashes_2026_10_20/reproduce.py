"""Offline port of Zhao main_results.do; downloaded Stata code is never executed.

Uses pandas/pyreadstat and a NumPy within estimator because pyfixest is absent
from the offline cache. See README for the explicit [DEGRADED] inference limits.
Run from repo root: UV_OFFLINE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project
python3 infra/immigration-fiscal/zhao_licenses_crashes_2026_10_20/reproduce.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import resource
import time

import numpy as np
import pandas as pd
import pyreadstat

HERE = Path(__file__).resolve().parent
RAW = HERE / "_cache/osf"
OUT = HERE / "derived"
CONTROLS = ["log_pop", "unemployment", "fuelexp", "road", "policexp"]
ADOPTION = {5: 2015, 6: 2015, 7: 2015, 8: 2015, 9: 2014,
            14: 2014, 21: 2014, 29: 2014, 46: 2014, 12: 2016}
DROP = [8, 9, 12, 48, 15]
EVENTS = [-6, -5, -4, -3, -2, 0, 1, 2, 3]


def write(name, rows):
    assert rows, f"[BLOCKED] empty output {name}"
    with (OUT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def verify_inputs():
    rows = []
    for line in (RAW / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        p = RAW / name
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"[BLOCKED] SHA256 mismatch: {name}")
        rows.append(dict(file=name, sha256=actual, bytes=p.stat().st_size,
                         osf_project_url="https://osf.io/x3u7y/"))
    write("input_hashes.csv", rows)


def load(name):
    d, meta = pyreadstat.read_dta(RAW / name, apply_value_formats=False)
    # pyreadstat/pandas can expose Stata integer columns as Python-object arrays.
    # Explicit numeric conversion raises on unexpected text instead of coercing it.
    for col in d.columns.difference(["county"]):
        d[col] = pd.to_numeric(d[col], errors="raise").astype(float)
    if d.duplicated(["county2", "year"]).any():
        raise RuntimeError(f"[BLOCKED] duplicate county-year: {name}")
    d = d[d.year <= 2018].copy()
    d["adoption"] = d.state2.map(ADOPTION).fillna(0).astype(int)
    d["treated"] = ((d.adoption > 0) & (d.year >= d.adoption)).astype(float)
    for target, original in [("log_pop", "pop"), ("fuelexp", "fuel"),
                             ("road", "regularhighway"), ("policexp", "police")]:
        d[target] = np.log(d[original].where(d[original] > 0))
    return d, meta


def demean(a, code):
    counts = np.bincount(code)
    means = np.column_stack([np.bincount(code, weights=a[:, j]) / counts
                             for j in range(a.shape[1])])
    return a - means[code]


def within(a, codes):
    a = a.copy()
    for _ in range(1000):
        old = a.copy()
        for code in codes:
            a = demean(a, code)
        if np.max(np.abs(old - a)) < 1e-11:
            return a
    raise RuntimeError("[BLOCKED] fixed-effects projection failed to converge")


def tcritical(df):
    """Student t 97.5th percentile by Simpson integration and bisection."""
    grid = np.linspace(0, 1, 2049)
    norm = math.exp(math.lgamma((df + 1) / 2) - math.lgamma(df / 2)) / math.sqrt(df * math.pi)
    lo, hi = 1., 4.
    for _ in range(40):
        mid = (lo + hi) / 2
        f = norm * (1 + (mid * grid) ** 2 / df) ** (-(df + 1) / 2)
        area = mid / 2048 / 3 * (f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum())
        if area < .475:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def fit(d, outcome, regressors, verify=False):
    cols = [outcome] + regressors
    s = d.replace([np.inf, -np.inf], np.nan).dropna(subset=cols + ["county2", "year", "state2"]).copy()
    codes = [pd.factorize(s[k], sort=True)[0] for k in ["county2", "year"]]
    a = within(s[cols].to_numpy(float), codes)
    y, x = a[:, 0], a[:, 1:]
    b, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != len(regressors):
        raise RuntimeError(f"[BLOCKED] rank deficient: {outcome} {regressors}")
    u = y - x @ b
    cluster = pd.factorize(s.state2, sort=True)[0]
    g = cluster.max() + 1
    scores = np.column_stack([np.bincount(cluster, weights=x[:, j] * u)
                              for j in range(x.shape[1])])
    bread = np.linalg.inv(x.T @ x)
    cr0 = bread @ scores.T @ scores @ bread
    # Counties nest in states. Count slopes, year indicators, and the constant;
    # do not subtract all county FE again. Preserve CR0 alongside this convention.
    k = len(regressors) + s.year.nunique()
    scale = g / (g - 1) * (len(s) - 1) / (len(s) - k)
    v = cr0 * scale
    if verify:
        # Independent FWL route: county-within, explicit year dummies.
        yd = pd.get_dummies(s.year, drop_first=True).to_numpy(float)
        ref = demean(np.column_stack([s[cols].to_numpy(float), yd]), codes[0])
        xr = ref[:, 1:]
        br = np.linalg.lstsq(xr, ref[:, 0], rcond=None)[0]
        ur = ref[:, 0] - xr @ br
        sr = np.column_stack([np.bincount(cluster, weights=xr[:, j] * ur)
                              for j in range(xr.shape[1])])
        ir = np.linalg.inv(xr.T @ xr)
        vr = ir @ sr.T @ sr @ ir
        np.testing.assert_allclose(b, br[:len(b)], atol=1e-9, rtol=1e-8)
        np.testing.assert_allclose(cr0, vr[:len(b), :len(b)], atol=1e-10, rtol=1e-7)
    return b, v, cr0, s, scale, k


def regression_row(d, sample, raw, transform="log1p"):
    d = d.copy()
    d["outcome"] = np.log1p(d[raw]) if transform == "log1p" else np.arcsinh(d[raw])
    b, v, cr0, s, scale, k = fit(d, "outcome", ["treated"] + CONTROLS, verify=True)
    se = math.sqrt(v[0, 0])
    critical = tcritical(s.state2.nunique() - 1)
    return dict(sample=sample, outcome=raw, transform=transform,
                coefficient=b[0], se_state_cluster=se, se_cr0=math.sqrt(cr0[0, 0]),
                ci95_low=b[0] - critical * se, ci95_high=b[0] + critical * se,
                pct_log1p_approx=100 * b[0] if transform == "log1p" else "",
                pct_one_plus_outcome=100 * np.expm1(b[0]) if transform == "log1p" else "",
                n=len(s), counties=s.county2.nunique(), states=s.state2.nunique(),
                year_min=int(s.year.min()), year_max=int(s.year.max()),
                mean_outcome=s[raw].mean(), mean_treated_post=s.loc[s.treated == 1, raw].mean(),
                cr1_multiplier=scale, counted_parameters=k, verification="FWL coefficient and CR0 PASS")


def event_studies(d):
    """Exact finite event list in main_results.do, after its persistent state drops.

    Interaction-weighted points use observed cohort shares at each relative time.
    IW covariance is conditional on shares, not eventstudyinteract's full V_iw.
    """
    d = d.copy()
    d["rel"] = d.year - d.adoption
    eventcols = []
    interact = []
    for e in EVENTS:
        name = f"event_{'m' if e < 0 else 'p'}{abs(e)}"
        d[name] = ((d.adoption > 0) & (d.rel == e)).astype(float)
        eventcols.append(name)
        for cohort in sorted(d.loc[d.adoption > 0, "adoption"].unique()):
            col = f"{name}_cohort{cohort}"
            if ((d.adoption == cohort) & (d.rel == e)).any():
                d[col] = ((d.adoption == cohort) & (d.rel == e)).astype(float)
                interact.append((e, cohort, col))
    rows, weights = [], []
    for outcome in ["total", "non_hit_and_run", "hit_and_run"]:
        d["outcome"] = np.log1p(d[outcome])
        for method, regressors in [("TWFE_event", eventcols),
                                    ("SA_interaction_weighted", [c for _, _, c in interact])]:
            b, v, cr0, s, scale, k = fit(d, "outcome", regressors + CONTROLS, verify=True)
            for e, name in zip(EVENTS, eventcols):
                w = np.zeros(len(b))
                if method == "TWFE_event":
                    w[regressors.index(name)] = 1
                else:
                    cells = [(cohort, col, int(((s.adoption == cohort) & (s.rel == e)).sum()))
                             for ee, cohort, col in interact if ee == e]
                    total = sum(n for _, _, n in cells)
                    for cohort, col, n in cells:
                        w[regressors.index(col)] = n / total
                        weights.append(dict(outcome=outcome, event_time=e, cohort=cohort,
                                            n=n, share=n / total))
                se = math.sqrt(w @ v @ w)
                critical = tcritical(s.state2.nunique() - 1)
                rows.append(dict(method=method, outcome=outcome, event_time=e,
                                 coefficient=w @ b, se_state_cluster=se,
                                 ci95_low=w @ b - critical * se, ci95_high=w @ b + critical * se,
                                 n=len(s), states=s.state2.nunique(),
                                 uncertainty="conditional on cohort shares" if method.startswith("SA") else "CR1",
                                 verification="FWL coefficient and CR0 PASS"))
    write("event_studies.csv", rows)
    write("sa_cohort_weights.csv", weights)


def inventory_do_files():
    """Audit every data-file reference; aliases are explicit, never guessed silently."""
    import re
    aliases = {"county_level_crash_clean.dta": "county_crash_data_clean.dta",
               "addtional_estimates_clean.dta": "additional_estimates_clean.dta"}
    rows = []
    for name in ["master.do", "main_results.do", "appendix.do", "figures.do"]:
        for i, line in enumerate((RAW / name).read_text().splitlines(), 1):
            if not re.match(r"\s*(use|merge)\b", line):
                continue
            for match in re.finditer(r'"([^"\n]+\.dta)"', line):
                ref = match.group(1)
                base = Path(ref).name
                mapped = aliases.get(base, base)
                status = "present" if (RAW / mapped).exists() else "absent_source"
                if base in ["Placebo estimate 3.dta", "coefficient.dta"]:
                    status = "generated_intermediate"
                rows.append(dict(do_file=name, line=i, reference=ref, mapped_name=mapped,
                                 status=status))
    write("do_file_inputs.csv", rows)


def main():
    started = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    verify_inputs()
    inventory_do_files()
    write("software.csv", [dict(package=name, version=version) for name, version in
                           [("numpy", np.__version__), ("pandas", pd.__version__),
                            ("pyreadstat", pyreadstat.__version__)]])
    d, meta = load("county_crash_data_clean.dta")
    assert not (d.state2 == 46).any(), "[BLOCKED] primary panel unexpectedly includes Vermont"
    assert np.array_equal(d.total, d.hit_and_run + d.non_hit_and_run), "[BLOCKED] crash partition"
    reduced = d[~d.state2.isin(DROP)].copy()
    main_outcomes = ["total", "non_hit_and_run", "hit_and_run", "pedestrian", "non_pedestrian",
                     "ped_hit", "non_ped_hit", "ped_non_hit", "non_ped_non_hit"]
    rows = [regression_row(d, "main", raw) for raw in main_outcomes]
    for j, label in enumerate("ABCDEFGH"):
        hours = list("abcdefghijklmnopqrstuvwx"[j * 3:(j + 1) * 3])
        # Stata '+' propagates a missing hour; never fill it with zero.
        d[f"hours_{label}"] = d[hours].sum(axis=1, skipna=False)
        rows.append(regression_row(d, "main_time_of_day", f"hours_{label}"))
    for sample, frame in [("mechanism_all", d), ("mechanism_high_coverage", reduced)]:
        rows += [regression_row(frame, sample, raw) for raw in ["speeding", "drowsy", "distracted"]]
    rows += [regression_row(reduced, "ihs_after_persistent_drops", raw, "asinh")
             for raw in ["total", "non_hit_and_run", "hit_and_run"]]
    full, _ = load("full_sample_clean.dta")
    rows += [regression_row(full, "full_with_vermont", raw)
             for raw in ["total", "non_hit_and_run", "hit_and_run"]]
    write("regressions.csv", rows)
    mainrow = rows[0]
    beta = mainrow["coefficient"]
    mean = mainrow["mean_outcome"]
    conversions = [
        ("abstract_percent", 5., "percent", "Reported in supplied brief; paper unavailable"),
        ("abstract_level", .46, "crashes/county-year", "Reported in supplied brief; paper unavailable"),
        ("beta_times_100", beta * 100, "percent approximation", "Effect on log(1+total)"),
        ("expm1_beta_times_100", np.expm1(beta) * 100, "percent of 1+total", "Not literal percent of total"),
        ("gap_beta_vs_abstract", beta * 100 - 5, "percentage points", "Approximation versus abstract"),
        ("beta_times_mean", beta * mean, "crashes/county-year", "Descriptive plug-in; not a level ATT"),
        ("gap_beta_mean_vs_abstract", beta * mean - .46, "crashes/county-year", "Descriptive plug-in gap"),
        ("expm1_times_mean_plus_one", np.expm1(beta) * (mean + 1), "crashes/county-year",
         "Alternative plug-in respecting +1; not a retransformed causal level ATT"),
    ]
    write("abstract_comparison.csv", [dict(quantity=q, value=float(v), unit=u, interpretation=i)
                                       for q, v, u, i in conversions])
    states = []
    for state, sub in d.groupby("state2", sort=True):
        states.append(dict(state2=int(state), state=sub.county.iloc[0].split(" - ")[0],
                           adoption=ADOPTION.get(int(state), 0), rows=len(sub),
                           counties=sub.county2.nunique(), year_min=int(sub.year.min()),
                           year_max=int(sub.year.max()), excluded_after_mechanism=int(state in DROP)))
    write("sample_states.csv", states)
    write("sample_audit.csv", [dict(
        sample=name, n=len(frame), counties=frame.county2.nunique(), states=frame.state2.nunique(),
        year_min=int(frame.year.min()), year_max=int(frame.year.max()),
        balanced_county_year_capacity=frame.county2.nunique() * frame.year.nunique(),
        absent_county_year_cells=frame.county2.nunique() * frame.year.nunique() - len(frame),
        total_zeros=int((frame.total == 0).sum()), controls_missing=int(frame[CONTROLS].isna().any(axis=1).sum()),
        mean_total=frame.total.mean(), mean_non_hit=frame.non_hit_and_run.mean(), mean_hit=frame.hit_and_run.mean())
        for name, frame in [("main", d), ("after_persistent_drops", reduced), ("full_with_vermont", full)]])
    event_studies(reduced)
    live = json.loads((HERE.parent / "live_case.json").read_text())
    write("integration_delta.csv", [dict(case=live["key"], case_lane=live["lane"],
        fiscal_delta_bn=0, social_crash_delta_bn=0,
        rule="No licensing multiplier applied: policy effect has unmatched population/outcome; observed risk inputs retained")])
    print("[DEGRADED] NumPy port: pyfixest unavailable offline; no Stata output for parity.")
    print("PASS: input hashes, county-year uniqueness, crash partition, independent FWL coefficient/CR0 checks")
    print(f"main beta={beta:.12f}; cluster SE={mainrow['se_state_cluster']:.12f}")
    print(f"runtime_seconds={time.perf_counter() - started:.3f}; peak_rss_native_units={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()

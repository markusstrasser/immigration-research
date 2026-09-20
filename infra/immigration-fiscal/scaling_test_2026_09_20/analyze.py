"""Descriptive scaling tests; no slope is automatically a causal fiscal response."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = HERE / "derived"
SCHOOL = BASE / "school_flight_2026_09_18"
WAVES = [2000, 2010, 2019]
INPUTS = {}


def pin(path):
    with Path(path).open("rb") as f:
        INPUTS[str(path)] = hashlib.file_digest(f, "sha256").hexdigest()
    return path


def absorb(matrix, groups, weights):
    m = np.asarray(matrix, float).copy()
    codes = [pd.factorize(g)[0] for g in groups]
    for _ in range(1000):
        prior = m.copy()
        for code in codes:
            den = np.bincount(code, weights=weights)
            for j in range(m.shape[1]):
                means = np.bincount(code, weights=weights*m[:, j])/den
                m[:, j] -= means[code]
        if np.max(np.abs(m-prior)) < 1e-10:
            return m
    raise ValueError("Fixed effects did not converge")


def fit(data, y, xs, groups, absorbed_df, weight=None):
    cols = [y, *xs]
    values = data[cols].to_numpy(float)
    weights = np.ones(len(data)) if weight is None else data[weight].to_numpy(float)
    if not np.isfinite(values).all() or not np.isfinite(weights).all() or (weights <= 0).any():
        raise ValueError("Nonfinite or invalid regression input")
    weights = weights/weights.mean()
    m = absorb(values, [data[g] for g in groups], weights)
    yw, xw = m[:, 0]*np.sqrt(weights), m[:, 1:]*np.sqrt(weights[:, None])
    b, _, rank, _ = np.linalg.lstsq(xw, yw, rcond=None)
    n, k = len(data), absorbed_df+len(xs)
    if rank != len(xs) or n <= k:
        raise ValueError("Unidentified or saturated model")
    residual = yw-xw@b
    cluster = pd.factorize(data.fips)[0]
    g = cluster.max()+1
    if g < 3:
        raise ValueError("Insufficient state clusters")
    scores = np.column_stack([np.bincount(cluster, weights=xw[:, j]*residual) for j in range(len(xs))])
    bread = np.linalg.inv(xw.T@xw)
    covariance = bread@scores.T@scores@bread * (g/(g-1))*((n-1)/(n-k))
    se = np.sqrt(np.maximum(np.diag(covariance), 0))
    crit = t.ppf(.975, g-1)
    rows = []
    for j, term in enumerate(xs):
        row = dict(term=term, beta=b[j], se=se[j], low95=b[j]-crit*se[j], high95=b[j]+crit*se[j],
                   n=n, districts=data.leaid.nunique(), states=g, weighted=weight is not None)
        for label, null in [("linear", 1.), ("three_quarters", .75), ("five_sixths", 5/6), ("point85", .85)]:
            row[f"p_{label}"] = 2*t.sf(abs((b[j]-null)/se[j]), g-1) if se[j] else float(b[j] == null)
        rows.append(row)
    return rows


def load():
    panel = pd.read_csv(pin(SCHOOL/"derived/district_panel.csv"), dtype={"leaid": str})
    if panel.duplicated(["leaid", "year"]).any() or sorted(panel.year.unique()) != WAVES:
        raise ValueError("District keys or waves changed")
    if not np.allclose(panel.pp_current*panel.pupils, panel.exp_current_elsec_total*panel.defl):
        raise ValueError("Current expenditure/enrollment identity failed")
    # Reconstruct a broader sample, removing the old expenditure and Hispanic-data screens.
    parts = {}
    for kind in ["fin", "dir"]:
        files = [p for year in WAVES for p in sorted((SCHOOL/"_cache/dist").glob(f"{kind}_{year}_*.csv"))]
        if not files:
            raise ValueError("Missing raw source files")
        parts[kind] = pd.concat([pd.read_csv(pin(p), dtype={"leaid": str}) for p in files], ignore_index=True)
        if parts[kind].duplicated(["leaid", "year"]).any():
            raise ValueError("Duplicate raw district rows")
        if not parts[kind].groupby("year").fips.nunique().eq(51).all():
            raise ValueError("Incomplete raw state coverage")
    d = parts["fin"].merge(parts["dir"][["leaid", "year", "fips", "agency_type", "agency_charter_indicator"]],
                           on=["leaid", "year", "fips"], validate="one_to_one")
    cpi = pd.read_csv(pin(SCHOOL/"_cache/cpiaucsl_annual.csv"))
    cpi["year"] = pd.to_datetime(cpi.observation_date).dt.year
    cpi = cpi.set_index("year").CPIAUCSL
    d["defl"] = d.year.map(cpi.loc[2020]/cpi)
    d["pupils"] = pd.to_numeric(d.enrollment_fall_responsible, errors="coerce")
    d = d.loc[d.agency_type.isin([1, 2]) & d.agency_charter_indicator.ne(1) &
              d.pupils.ge(100) & d.exp_current_elsec_total.gt(0)].copy()
    out = {}
    for label, sample in [("existing_screen", panel), ("broader_screen", d)]:
        sample = sample.loc[sample.fips.ne(11)].copy()  # DC has one district; cannot hold it out within state.
        sample["log_pupils"] = np.log(sample.pupils)
        for raw, name in [("exp_current_elsec_total", "log_current"),
                          ("exp_current_instruction_total", "log_instruction")]:
            sample[name] = np.log((sample[raw]*sample.defl).where(sample[raw] > 0))
        sample["state_year"] = sample.fips.astype(str)+"_"+sample.year.astype(str)
        out[label] = sample
    return out


def balanced(d, outcome):
    d = d.dropna(subset=[outcome]).copy()
    ids = d.groupby("leaid").year.nunique()
    d = d.loc[d.leaid.isin(ids.index[ids.eq(3)])].copy()
    if d.groupby("leaid").fips.nunique().max() != 1:
        raise ValueError("District crosses state boundaries")
    first = d.loc[d.year.eq(2000)].set_index("leaid").pupils
    d["base_pupils"] = d.leaid.map(first)
    return d


def estimates(samples):
    results = []
    for label, d in samples.items():
        for outcome in ["log_current", "log_instruction"]:
            cross = d.loc[d.year.eq(2019)].dropna(subset=[outcome])
            b = balanced(d, outcome)
            for weighted in [False, True]:
                c = cross.copy()
                c["cross_pupils"] = c.pupils
                specifications = [
                    ("cross_2019", c, ["fips"], c.fips.nunique(), "cross_pupils"),
                    ("within_district_state_year", b, ["leaid", "state_year"],
                     b.leaid.nunique()+b.state_year.nunique()-b.fips.nunique(), "base_pupils"),
                ]
                for spec, sub, fes, df, weight in specifications:
                    for r in fit(sub, outcome, ["log_pupils"], fes, df, weight if weighted else None):
                        results.append(dict(sample=label, outcome=outcome, spec=spec, **r))
            if outcome == "log_current":
                for name, mask in [("small", cross.pupils.lt(1000)),
                                   ("medium", cross.pupils.between(1000, 9999)),
                                   ("large", cross.pupils.ge(10000))]:
                    sub = cross.loc[mask]
                    for r in fit(sub, outcome, ["log_pupils"], ["fips"], sub.fips.nunique()):
                        results.append(dict(sample=label, outcome=outcome, spec=f"cross_{name}", **r))
            pair = b.loc[b.year.isin([2010, 2019])].pivot(index="leaid", columns="year", values=[outcome, "log_pupils"])
            diff = pd.DataFrame({"leaid": pair.index,
                "dy": pair[outcome][2019].to_numpy()-pair[outcome][2010].to_numpy(),
                "dx": pair.log_pupils[2019].to_numpy()-pair.log_pupils[2010].to_numpy()})
            diff["fips"] = diff.leaid.map(b.drop_duplicates("leaid").set_index("leaid").fips)
            diff["base_pupils"] = diff.leaid.map(b.drop_duplicates("leaid").set_index("leaid").base_pupils)
            diff["grow"] = diff.dx.clip(lower=0)
            diff["shrink"] = diff.dx.clip(upper=0)
            for spec, sub, terms in [("long_difference", diff, ["dx"]),
                                     ("long_difference_asymmetric", diff, ["grow", "shrink"]),
                                     ("long_difference_small_changes", diff.loc[diff.dx.abs().le(.2)], ["dx"])]:
                for weighted in [False, True]:
                    for r in fit(sub, "dy", terms, ["fips"], sub.fips.nunique(), "base_pupils" if weighted else None):
                        results.append(dict(sample=label, outcome=outcome, spec=spec, **r))
    return pd.DataFrame(results)


def predict_cv(d):
    d = d.loc[d.year.eq(2019)].copy()
    counts = d.groupby("fips").size()
    excluded_states = counts.index[counts.lt(5)].tolist()
    excluded_rows = int(d.fips.isin(excluded_states).sum())
    d = d.loc[~d.fips.isin(excluded_states)].copy()
    d["hash"] = d.leaid.map(lambda s: hashlib.sha256(s.encode()).hexdigest())
    d = d.sort_values(["fips", "hash"])
    d["fold"] = d.groupby("fips").cumcount()%5
    rows = []
    for name, slope in [("three_quarters", .75), ("five_sixths", 5/6), ("point85", .85), ("linear", 1.), ("free", None)]:
        errors = []
        for fold in range(5):
            train, test = d.loc[d.fold.ne(fold)], d.loc[d.fold.eq(fold)]
            if slope is None:
                means = train.groupby("fips")[["log_current", "log_pupils"]].transform("mean")
                z = train[["log_current", "log_pupils"]]-means
                beta = np.dot(z.log_pupils, z.log_current)/np.dot(z.log_pupils, z.log_pupils)
            else:
                beta = slope
            alpha = (train.log_current-beta*train.log_pupils).groupby(train.fips).mean()
            intercept = test.fips.map(alpha)
            if intercept.isna().any():
                raise ValueError("Held-out state absent from training")
            errors.extend((test.log_current-intercept-beta*test.log_pupils).tolist())
        rows.append(dict(model=name, n=len(errors), log_rmse=np.sqrt(np.mean(np.square(errors))),
                         excluded_states=','.join(map(str, excluded_states)), excluded_rows=excluded_rows))
    return pd.DataFrame(rows)


def finite_response(beta, share):
    if not 0 < share < 1 or not np.isfinite(beta):
        raise ValueError("Invalid finite-response argument")
    return -np.expm1(beta*np.log1p(-share))/share


def fiscal_bridge():
    # Pure theory illustrations never replace the CBO-informed category sensitivity.
    annual = BASE/"full_account_2026_09_20/derived"
    for audit_name in ["audit.json", "welfare_audit.json", "service_response_audit.json"]:
        audit = json.loads(pin(annual/audit_name).read_text())
        for source, expected in audit["source_hashes"].items():
            if hashlib.sha256(Path(source).read_bytes()).hexdigest() != expected:
                raise ValueError(f"Fiscal source drift: {source}")
        for name, expected in audit["outputs"].items():
            if hashlib.sha256((annual/f"{name}.csv").read_bytes()).hexdigest() != expected:
                raise ValueError(f"Fiscal output drift: {name}")
    cases = pd.read_csv(pin(annual/"headline_cases.csv"))
    pools = pd.read_csv(pin(annual/"response_pools.csv")).query(
        "receipt_scenario == 'cbo_collective' and spending_scenario == 'complete_preferred_F_per_capita'")
    accounts = pd.read_csv(pin(annual/"accounts.csv"))
    shares = (accounts.target_population/accounts.resident_population).unique()
    if len(shares) != 1 or pools.allocation.duplicated().any():
        raise ValueError("Ambiguous fiscal inputs")
    s = float(shares[0])
    rows = []
    betas = [("biology_075", .75), ("network_5over6", 5/6), ("urban_085", .85), ("proportional", 1.)]
    for name, beta in betas:
        r = finite_response(beta, s)
        for b in cases.itertuples():
            services = pools.set_index("allocation").loc[b.allocation, "services_bn"]
            rows.append(dict(model=name, beta=beta, national_target_share=s, finite_response=r,
                allocation=b.allocation, normalization=b.normalization,
                welfare_bn=b.welfare_bn+(1-r)*services,
                status="UNIFORM_THEORY_TRANSFER_NOT_ESTIMATED_IMMIGRATION_EFFECT"))
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(exist_ok=True)
    receipt = OUT/"audit.json"
    if receipt.exists():
        receipt.unlink()  # Derived receipt cannot survive a failed regeneration.
    samples = load()
    est = estimates(samples)
    cv = pd.concat([predict_cv(d).assign(sample=label) for label, d in samples.items()], ignore_index=True)
    coverage = pd.DataFrame([dict(sample=label, year=year, rows=len(d), districts=d.leaid.nunique(),
        pupils=d.pupils.sum()) for label, sample in samples.items() for year, d in sample.groupby("year")])
    tables = {"school_estimates": est, "school_cv": cv, "school_coverage": coverage,
              "theory_fiscal_scenarios": fiscal_bridge()}
    for name, table in tables.items():
        table.to_csv(OUT/f"{name}.csv", index=False)
    for p in [Path(__file__), HERE/"README.md", SCHOOL/"build_districts.py"]:
        pin(p)
    audit = dict(inputs=INPUTS, outputs={name: hashlib.sha256((OUT/f"{name}.csv").read_bytes()).hexdigest() for name in tables},
        status="DESCRIPTIVE_SCALING_NOT_CAUSAL_RESPONSE", inference="state-cluster CR1; t(G-1); absorbed degrees of freedom",
        school_units="2020 dollars/current expenditure; same-year F33 pupils", waves=WAVES,
        scope="50 states; DC excluded for held-out state-intercept support", quality="not observed")
    receipt.write_text(json.dumps(audit, indent=2)+"\n")
    print(est.query("sample == 'existing_screen' and outcome == 'log_current' and not weighted")[["spec", "term", "beta", "low95", "high95", "n"]].to_string(index=False))
    print(cv.to_string(index=False))


if __name__ == "__main__":
    main()

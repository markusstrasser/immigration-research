"""Long-difference estimates of local administration spending's elasticity with respect to population.

Model, county c in state s over window t0 -> t1:
    dln(real outcome)_c = beta * dln(population)_c + gamma * ln(population_t0)_c + state_s + e_c
Stacked 2012->2017 and 2017->2022 differences use state x period effects. Weights: base-year
population, or none. Standard errors cluster by state (CR1).

Instruments (built in build_panel.py):
  (a) bartik     industry-mix employment shock, leave-one-out national growth, base-year shares
  (b) imm        immigrant settlement shift-share, 2000 origin shares, leave-one-out national change
      imm_nomex  the same without Mexico;  imm_mex  Mexico alone (diagnostic)
  (c) bartik + imm, with Hansen's J
Every IV row reports the first stage, the reduced form, the Montiel Olea-Pflueger effective F and
the Anderson-Rubin 95% set. Checks: pre-period placebos, leaving out the 25 largest counties,
dropping county areas without a county government (consolidated city-counties, independent cities),
1% trims, Rotemberg weights and a drop-top-5-industries Bartik, controls for the industry-mix pay
shock and for actual income growth (a potentially bad control), outcome variants, and cross-sectional
scale elasticities in levels.

Outputs: derived/estimates.csv, derived/rotemberg.csv, derived/cross_section.csv,
derived/estimates_summary.json.
"""
import json
import math
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
sys.path.insert(0, str(HERE))
import iv  # noqa: E402

OUTCOMES = {
    "admin": ["e23", "e29", "e31"],
    "admin_judicial": ["e23", "e29", "e31", "e25"],
    "admin_direct": ["d23", "d29", "d31"],
    "admin_judicial_direct": ["d23", "d29", "d31", "d25"],
    "central_buildings": ["e29", "e31"],
    "financial_admin": ["e23"],
    "central_staff": ["e29"],
    "public_buildings": ["e31"],
}
WINDOWS = {"1222": (2012, 2022), "0717": (2007, 2017), "1217": (2012, 2017), "1722": (2017, 2022),
           "0712": (2007, 2012)}
INCOME_YEARS = {"1222": (2012, 2022), "0717": (2009, 2017), "1217": (2012, 2017), "1722": (2017, 2022),
                "0712": (2009, 2012)}
MOP_CRITICAL = 23.109  # tau = 10%, 5% test; the simplified critical value, conservative for L = 2
ROWS = []

panel = pd.read_csv(DERIVED / "panel.csv", dtype={"fips": str, "state": str})


def outcome(df, name, year):
    cols = [f"{i}_{year}" for i in OUTCOMES[name]]
    return df[cols].sum(axis=1, min_count=len(cols))


def long_difference(window, name, bartik_col=None):
    t0, t1 = WINDOWS[window]
    d = panel.copy()
    y0, y1 = outcome(d, name, t0), outcome(d, name, t1)
    d["y0"], d["y1"] = y0, y1
    d = d[(d.y0 > 0) & (d.y1 > 0)].copy()
    d["dy"] = np.log(d.y1 / d.y0)
    d["dx"] = np.log(d[f"pop_{t1}"] / d[f"pop_{t0}"])
    d["lnpop0"] = np.log(d[f"pop_{t0}"])
    d["w"] = d[f"pop_{t0}"]
    d["bartik"] = d[bartik_col or f"bartik_{window}"]
    d["bartik_pay"] = d[f"bartik_pay_{window}"]
    for k in ("imm", "imm_nomex", "imm_mex", "dfbshare"):
        d[k] = d[f"{k}_{window}"]
    a, b = INCOME_YEARS[window]
    d["dlninc"] = np.log(d[f"medhhinc_{b}"] / d[f"medhhinc_{a}"])
    d["period"] = window
    d["fe"] = d.state
    return d.dropna(subset=["bartik", "imm", "imm_nomex"]).reset_index(drop=True)


def stacked(name, fixed_shares=True):
    a = long_difference("1217", name)
    b = long_difference("1722", name, "bartik_1722_s12" if fixed_shares else None)
    d = pd.concat([a, b], ignore_index=True)
    d["fe"] = d.state + "_" + d.period
    return d


def stacked_early(name, fixed_shares=True):
    """Break-free stacked design: 2007->2012 and 2012->2017, no 2022 wave."""
    a = long_difference("0712", name)
    b = long_difference("1217", name, "bartik_1217_s07" if fixed_shares else None)
    d = pd.concat([a, b], ignore_index=True)
    d["fe"] = d.state + "_" + d.period
    return d


def prepare(d, y, x, Z, controls, weighted):
    W = [np.ones(len(d))] + [d[c].to_numpy(float) for c in controls]
    W.append(pd.get_dummies(d.fe, drop_first=True, dtype=float).to_numpy())
    W = np.column_stack(W)
    Zm = np.column_stack([d[z].to_numpy(float) for z in Z]) if Z else None
    weights = d.w.to_numpy(float) if weighted else np.ones(len(d))
    return iv.Prepared(d[y].to_numpy(float), d[x].to_numpy(float), Zm, W, weights, d.state.to_numpy())


def fmt(v):
    return ";".join(f"{float(x):.6g}" for x in np.atleast_1d(v))


def run(d, *, window, outcome_name, sample, instruments=(), controls=("lnpop0",), weighted=True, y="dy", x="dx",
        method=None, note=""):
    d = d.dropna(subset=[y, x] + list(instruments) + list(controls))
    p = prepare(d, y, x, list(instruments), list(controls), weighted)
    row = {"window": window, "outcome": outcome_name, "sample": sample, "weighted": weighted,
           "method": method or ("OLS" if not instruments else "2SLS"), "instruments": "+".join(instruments),
           "controls": "+".join(controls), "n": p.n, "clusters": p.G, "note": note}
    if not instruments:
        r = iv.ols(p)
        row.update(beta=r["beta"], se=r["se"])
    else:
        r = iv.tsls(p, grid=(-6.0, 6.0, 0.001))
        row.update(beta=r["beta"], se=r["se"], fs_coef=fmt(r["pi"]), fs_se=fmt(r["pi_se"]), F_eff=r["F_eff"],
                   F_robust=r["F_robust"], rf_coef=fmt(r["gamma"]), rf_se=fmt(r["gamma_se"]),
                   ar_type=r["ar"]["type"], ar_lo=r["ar"]["lo"], ar_hi=r["ar"]["hi"],
                   ar_pieces=json.dumps(r["ar"].get("pieces", "")) if r["ar"].get("pieces") else "",
                   J=r.get("J", math.nan), J_p=r.get("J_p", math.nan), beta_gmm=r.get("beta_gmm", math.nan))
    row["ci_lo"] = row["beta"] - 1.96 * row["se"]
    row["ci_hi"] = row["beta"] + 1.96 * row["se"]
    ROWS.append(row)
    return row


IV_SETS = [("bartik",), ("imm",), ("imm_nomex",), ("imm_mex",), ("bartik", "imm"), ("bartik", "imm_nomex")]


def core(d, window, name, sample, weighted_both=True, sets=IV_SETS, controls=("lnpop0",), note=""):
    for weighted in ((True, False) if weighted_both else (True,)):
        run(d, window=window, outcome_name=name, sample=sample, weighted=weighted, controls=controls, note=note)
        for z in sets:
            run(d, window=window, outcome_name=name, sample=sample, instruments=z, weighted=weighted,
                controls=controls, note=note)


def largest(n, year):
    return set(panel.nlargest(n, f"pop_{year}").fips)


def trimmed(d, q=0.01):
    lo, hi = d.dy.quantile(q), d.dy.quantile(1 - q)
    return d[(d.dy >= lo) & (d.dy <= hi)]


def rotemberg_rows(window, name, weighted, npz_name=None):
    d = long_difference(window, name)
    z = np.load(CACHE / f"bartik_{npz_name or window}.npz")
    idx = {u: i for i, u in enumerate(z["units"].tolist())}
    rows_ix = np.array([idx[f] for f in d.fips])
    comps = (z["Z"] * z["G"])[rows_ix]
    shares = z["Z"][rows_ix]
    p = prepare(d, "dy", "dx", ["bartik"], ["lnpop0"], weighted)
    alpha, beta_k, beta = iv.rotemberg(p, comps)
    check = iv.tsls(p)["beta"]
    groups = z["groups"].tolist()
    out = pd.DataFrame({"window": window, "outcome": name, "weighted": weighted, "industry": groups, "alpha": alpha,
                        "beta_k": beta_k, "national_growth": z["national_growth"], "national_emp0": z["national_emp0"],
                        "mean_share": shares.mean(axis=0)})
    out["rank"] = out.alpha.abs().rank(ascending=False, method="first").astype(int)
    top5 = out.nsmallest(5, "rank").industry.tolist()
    keep = [i for i, g in enumerate(groups) if g not in top5]
    d = d.assign(bartik_drop5=comps[:, keep].sum(axis=1), share_kept=shares[:, keep].sum(axis=1))
    return out, beta, check, top5, d


def cross_section():
    rows = []
    for year in (2002, 2007, 2012, 2017, 2022):
        for name in ("admin", "admin_judicial", "admin_judicial_direct"):
            d = panel.copy()
            d["y"] = outcome(d, name, year)
            d = d[d.y > 0].copy()
            d["ly"], d["lp"] = np.log(d.y), np.log(d[f"pop_{year}"])
            d["w"], d["fe"] = d[f"pop_{year}"], d.state
            for fe in (False, True):
                for weighted in (True, False):
                    dd = d.assign(fe=d.state if fe else "all")
                    p = prepare(dd, "ly", "lp", [], [], weighted)
                    r = iv.ols(p)
                    rows.append({"level": "county", "year": year, "outcome": name, "state_fe": fe, "weighted": weighted,
                                 "beta": r["beta"], "se": r["se"], "n": p.n})
            s = d.groupby("state").agg(y=("y", "sum"), pop=(f"pop_{year}", "sum")).reset_index()
            s["ly"], s["lp"], s["w"], s["fe"] = np.log(s.y), np.log(s["pop"]), s["pop"], "all"
            p = prepare(s, "ly", "lp", [], [], False)
            r = iv.ols(p)
            rows.append({"level": "state sum of county areas (local only)", "year": year, "outcome": name,
                         "state_fe": False, "weighted": False, "beta": r["beta"], "se": r["se"], "n": p.n})
    rows += state_cross_section()
    return pd.DataFrame(rows)


def state_cross_section():
    """Cross-state elasticity by census year, state and local combined (level 1), direct expenditure
    E/F/G on 23+25+29+31, from the Census state-by-level files; the 2022 row is the analogue of
    scaling_check.py's 0.842 (published Table 1 lines 106-109, 50 states)."""
    comp = FISCAL / "local_spending_composition_2026_09_18" / "_cache"
    rows = []
    raw_pop = {}
    for f, years in (("pep/cc-est2020int-agesex-all.csv", {"4": 2012, "9": 2017}),):
        t = pd.read_csv(CACHE / f, usecols=["SUMLEV", "STATE", "YEAR", "POPESTIMATE"], encoding="latin-1")
        t = t[t.YEAR.astype(str).isin(years)]
        for (st, yr), v in t.groupby(["STATE", "YEAR"]).POPESTIMATE.sum().items():
            raw_pop[(int(st), years[str(yr)])] = float(v)
    t = pd.read_csv(FISCAL.parents[1] / "sources/immigration-fiscal/data/external/census_county_pop/cc-est2023-alldata.csv",
                    usecols=["STATE", "YEAR", "AGEGRP", "TOT_POP"], encoding="latin-1")
    t = t[(t.YEAR == 4) & (t.AGEGRP == 0)]
    for st, v in t.groupby("STATE").TOT_POP.sum().items():
        raw_pop[(int(st), 2022)] = float(v)
    gid_map = {}
    with zipfile.ZipFile(comp / "indunit_2012.zip") as zf:
        for line in zf.read("Fin_GID_2012.txt").decode("latin-1").splitlines():
            if len(line) >= 118 and line[:2].isdigit() and line[113:115].isdigit():
                gid_map[int(line[:2])] = int(line[113:115])
    for year in (2012, 2017, 2022):
        with zipfile.ZipFile(comp / f"indunit_{year}.zip") as zf:
            name = next(n for n in zf.namelist() if n.lower().endswith(f"{str(year)[2:]}statetypepu.txt"))
            text = zf.read(name).decode("latin-1").splitlines()
        spend = {}
        for line in text:
            parts = line.split()
            if len(parts) < 3 or len(parts[0]) != 3 or parts[0][2] != "1":
                continue
            code = parts[1]
            if code[0] in "EFG" and code[1:] in ("23", "25", "29", "31"):
                st = int(parts[0][:2])
                st = gid_map.get(st, st) if year == 2012 else st
                spend[st] = spend.get(st, 0.0) + float(parts[2])
        states = sorted(s for s in spend if s not in (0, 11) and (s, year) in raw_pop)
        d = pd.DataFrame({"state": [str(s) for s in states], "ly": np.log([spend[s] for s in states]),
                          "lp": np.log([raw_pop[(s, year)] for s in states])})
        d["w"], d["fe"] = 1.0, "all"
        p = prepare(d, "ly", "lp", [], [], False)
        r = iv.ols(p)
        X = np.column_stack([np.ones(len(d)), d.lp])
        b, *_ = np.linalg.lstsq(X, d.ly, rcond=None)
        e = d.ly - X @ b
        se_h = float(np.sqrt(np.linalg.inv(X.T @ X)[1, 1] * (e @ e) / (len(d) - 2)))
        rows.append({"level": "state, state+local combined (Census state-by-level files)", "year": year,
                     "outcome": "direct 23+25+29+31", "state_fe": False, "weighted": False, "beta": r["beta"],
                     "se": se_h, "n": len(d)})
    return rows


KEY_SPECS = [  # (label, window, instruments, note); outcome admin, sample all, controls lnpop0, weighted
    ("brief main: 2012-2022, Bartik + immigrant", "1222", "bartik+imm", None),
    ("brief main: 2012-2022, Bartik", "1222", "bartik", None),
    ("brief main: 2012-2022, immigrant", "1222", "imm", None),
    ("break-free long difference 2007-2017, Bartik", "0717", "bartik", None),
    ("break-free stacked 2007-12 and 2012-17, Bartik", "stacked 0712+1217", "bartik", "2007 shares for both periods"),
    ("break-free stacked 2007-12 and 2012-17, Bartik + immigrant", "stacked 0712+1217", "bartik+imm", "2007 shares for both periods"),
    ("break-free stacked 2007-12 and 2012-17, OLS", "stacked 0712+1217", "", "2007 shares for both periods"),
    ("2012-2022 OLS", "1222", "", None),
]


def ar_contains(r, v):
    t = r["ar_type"]
    if t == "real line":
        return True
    if str(t).startswith("empty"):
        return False
    if t == "two rays":
        return v <= r["ar_lo"] or v >= r["ar_hi"]
    if isinstance(r.get("ar_pieces"), str) and r["ar_pieces"]:
        return any(a - 1e-9 <= v <= b + 1e-9 for a, b in json.loads(r["ar_pieces"]))
    return r["ar_lo"] <= v <= r["ar_hi"]


def ar_tally(est):
    """How many 95% Anderson-Rubin sets for the primary outcome exclude 0, 0.59, 0.84 and 1."""
    iv_rows = est[(est.method == "2SLS") & (est.outcome == "admin")]
    groups = {
        "all instruments": iv_rows,
        "Bartik only": iv_rows[iv_rows.instruments.isin(["bartik", "bartik_drop5"])],
        "Bartik only, weighted, windows without the 2022 wave or the 2007-12 recession window":
            iv_rows[iv_rows.instruments.isin(["bartik", "bartik_drop5"]) & (iv_rows.weighted == True)
                    & iv_rows.window.isin(["0717", "1217", "stacked 0712+1217"])],
    }
    out = {}
    for name, g in groups.items():
        rec = {"specs": len(g)}
        for v in (0.0, 0.59, 0.84, 1.0):
            rec[f"exclude_{v}"] = int(sum(not ar_contains(r, v) for r in g.to_dict("records")))
        rec["beta_min"], rec["beta_max"] = float(g.beta.min()), float(g.beta.max())
        rec["F_eff_min"] = float(g.F_eff.min())
        out[name] = rec
    return out


def key_results(est, cs):
    key, points = [], []
    for label, window, inst, note in KEY_SPECS:
        m = est[(est.window == window) & (est.outcome == "admin") & (est["sample"] == "all") & (est.weighted == True)
                & (est.controls == "lnpop0") & (est.instruments.fillna("") == inst)]
        m = m[m.note.isna() | (m.note == "")] if note is None else m[m.note == note]
        if len(m) != 1:
            raise SystemExit(f"[BLOCKED] key spec {label} matched {len(m)} rows")
        r = m.iloc[0].to_dict()
        rec = {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in r.items()}
        rec["label"] = label
        key.append(rec)
        points.append({"label": f"{label}: point", "elasticity": r["beta"]})
        if inst:
            for end in ("ar_lo", "ar_hi"):
                if math.isfinite(r[end]):
                    points.append({"label": f"{label}: Anderson-Rubin {end[-2:]}", "elasticity": r[end]})
        else:
            points += [{"label": f"{label}: 95% {e}", "elasticity": r[f"ci_{e}"]} for e in ("lo", "hi")]
    key.append({"label": "Anderson-Rubin tally", **ar_tally(est)})
    c = cs[(cs.level == "county") & (cs.year == 2017) & (cs.outcome == "admin") & cs.state_fe & cs.weighted].iloc[0]
    key.append({"label": "county cross-section in levels, 2017, state effects, weighted", "beta": c.beta, "se": c.se, "n": int(c.n)})
    points.append({"label": "county cross-section in levels 2017 (not causal)", "elasticity": float(c.beta)})
    return key, points


def main():
    DERIVED.mkdir(exist_ok=True)
    rot_out = []
    summary = {"windows": {}}
    # ---- main outcome, every window
    for window in ("1222", "0717", "0712"):
        d = long_difference(window, "admin")
        core(d, window, "admin", "all")
        top25 = largest(25, WINDOWS[window][0])
        core(d[~d.fips.isin(top25)], window, "admin", "drop 25 largest")
        core(d[d.no_county_govt == 0], window, "admin", "drop areas without a county government")
        core(trimmed(d), window, "admin", "trim 1% tails of outcome change")
        for weighted in (True, False):
            run(d, window=window, outcome_name="admin", sample="all", instruments=("bartik",), weighted=weighted,
                controls=("lnpop0", "bartik_pay"), note="controls for industry-mix pay-per-worker shock")
            run(d, window=window, outcome_name="admin", sample="all", instruments=("bartik",), weighted=weighted,
                controls=("lnpop0", "dlninc"), note="controls for actual median household income growth (bad control)")
            run(d, window=window, outcome_name="admin", sample="all", instruments=("bartik", "imm"), weighted=weighted,
                controls=("lnpop0", "bartik_pay"), note="controls for industry-mix pay-per-worker shock")
            run(d, window=window, outcome_name="admin", sample="all", instruments=("imm",), weighted=weighted,
                controls=("lnpop0", "dlninc"), note="controls for actual median household income growth (bad control)")
            # (b)'s first stage on the foreign-born share, not only on population
            run(d, window=window, outcome_name="foreign-born share change", sample="all", x="imm", y="dfbshare",
                weighted=weighted, method="first stage on foreign-born share (OLS of dfbshare on imm)")
            run(d, window=window, outcome_name="foreign-born share change", sample="all", x="imm_nomex", y="dfbshare",
                weighted=weighted, method="first stage on foreign-born share (OLS of dfbshare on imm_nomex)")
            rot, beta, check, top5, dd = rotemberg_rows(window, "admin", weighted)
            rot_out.append(rot)
            summary["windows"].setdefault(window, {})[f"rotemberg_top5_{'w' if weighted else 'u'}"] = top5
            if abs(beta - check) > 1e-5 * max(1.0, abs(check)):  # panel.csv stores the instrument to 8 decimals
                raise SystemExit(f"[BLOCKED] Rotemberg decomposition does not add up: {beta} vs {check}")
            run(dd, window=window, outcome_name="admin", sample="all", instruments=("bartik_drop5",), weighted=weighted,
                note=f"Bartik without top-5 Rotemberg industries {top5}")
            run(dd, window=window, outcome_name="admin", sample="all", instruments=("bartik_drop5",), weighted=weighted,
                controls=("lnpop0", "share_kept"), note=f"Bartik without top-5 industries, controls for sum of kept shares")
        # outcome variants
        for name in ("admin_judicial", "admin_direct", "admin_judicial_direct", "central_buildings",
                     "financial_admin", "central_staff", "public_buildings"):
            core(long_difference(window, name), window, name, "all",
                 sets=[("bartik",), ("imm",), ("imm_nomex",), ("bartik", "imm")])
    # ---- stacked five-year differences
    d = stacked("admin", fixed_shares=True)
    core(d, "stacked 1217+1722", "admin", "all", note="2012 shares for both periods")
    core(d[~d.fips.isin(largest(25, 2012))], "stacked 1217+1722", "admin", "drop 25 largest", note="2012 shares")
    core(d[d.no_county_govt == 0], "stacked 1217+1722", "admin", "drop areas without a county government", note="2012 shares")
    core(trimmed(d), "stacked 1217+1722", "admin", "trim 1% tails of outcome change", note="2012 shares")
    core(stacked("admin", fixed_shares=False), "stacked 1217+1722", "admin", "all",
         sets=[("bartik",), ("bartik", "imm")], note="start-of-period shares")
    for name in ("admin_judicial", "central_buildings", "admin_judicial_direct"):
        core(stacked(name), "stacked 1217+1722", name, "all", sets=[("bartik",), ("imm",), ("bartik", "imm")],
             note="2012 shares for both periods")
    # ---- break-free stacked differences, 2007->2012 and 2012->2017 (added: the 2022 wave carries a reporting break)
    label = "stacked 0712+1217"
    d = stacked_early("admin", fixed_shares=True)
    core(d, label, "admin", "all", note="2007 shares for both periods")
    core(d[~d.fips.isin(largest(25, 2007))], label, "admin", "drop 25 largest", note="2007 shares")
    core(d[d.no_county_govt == 0], label, "admin", "drop areas without a county government", note="2007 shares")
    core(trimmed(d), label, "admin", "trim 1% tails of outcome change", note="2007 shares")
    for weighted in (True, False):
        run(d, window=label, outcome_name="admin", sample="all", instruments=("bartik",), weighted=weighted,
            controls=("lnpop0", "bartik_pay"), note="2007 shares; controls for industry-mix pay-per-worker shock")
        run(d, window=label, outcome_name="admin", sample="all", instruments=("bartik",), weighted=weighted,
            controls=("lnpop0", "dlninc"), note="2007 shares; controls for actual median household income growth (bad control)")
    core(stacked_early("admin", fixed_shares=False), label, "admin", "all",
         sets=[("bartik",), ("bartik", "imm")], note="start-of-period shares")
    for name in ("admin_judicial", "central_buildings", "admin_judicial_direct", "admin_direct"):
        core(stacked_early(name), label, name, "all", sets=[("bartik",), ("imm",), ("bartik", "imm")],
             note="2007 shares for both periods")
    # single five-year periods
    for window in ("1217", "1722"):
        core(long_difference(window, "admin", "bartik_1722_s12" if window == "1722" else None), window, "admin", "all",
             sets=[("bartik",), ("imm",), ("imm_nomex",), ("bartik", "imm")],
             note="2012 shares" if window == "1722" else "")
    core(long_difference("1217", "admin", "bartik_1217_s07"), "1217", "admin", "all", sets=[("bartik",), ("bartik", "imm")],
         note="2007 shares")
    # stacked placebos: each period's instrument against the preceding five-year change
    for label, parts in (("stacked 0712+1217", [("0712", None, 2002, 2007), ("1217", "bartik_1217_s07", 2007, 2012)]),
                         ("stacked 1217+1722", [("1217", None, 2007, 2012), ("1722", "bartik_1722_s12", 2012, 2017)])):
        frames = []
        for window, col, a, b in parts:
            dd = long_difference(window, "admin", col)
            ya, yb = outcome(dd, "admin", a), outcome(dd, "admin", b)
            dd["pre"] = np.log(yb / ya).where((ya > 0) & (yb > 0))
            dd["prepop"] = np.log(dd[f"pop_{b}"] / dd[f"pop_{a}"])
            frames.append(dd)
        dd = pd.concat(frames, ignore_index=True)
        dd["fe"] = dd.state + "_" + dd.period
        dd = dd.dropna(subset=["pre"])
        for z in ("bartik", "imm"):
            for weighted in (True, False):
                run(dd, window=label, outcome_name="placebo: preceding five-year outcome change", sample="all", y="pre",
                    x=z, weighted=weighted, method=f"placebo reduced form (OLS of pre-period change on {z})")
                run(dd, window=label, outcome_name="placebo: preceding five-year population change", sample="all",
                    y="prepop", x=z, weighted=weighted, method=f"placebo reduced form (OLS of pre-period change on {z})")
                run(dd, window=label, outcome_name="main-period reduced form, same sample", sample="placebo sample",
                    y="dy", x=z, weighted=weighted, method=f"reduced form (OLS of outcome change on {z})")
    # ---- pre-period placebos: each window's instrument against earlier changes
    placebo = {"1222": [("outcome", 2002, 2012), ("outcome", 2007, 2012), ("population", 2002, 2012), ("population", 2007, 2012)],
               "0717": [("outcome", 1997, 2007), ("outcome", 2002, 2007), ("population", 2002, 2007)],
               "0712": [("outcome", 1997, 2007), ("outcome", 2002, 2007), ("population", 2002, 2007)]}
    for window, tests in placebo.items():
        base = long_difference(window, "admin")
        for kind, a, b in tests:
            dd = base.copy()
            if kind == "outcome":
                ya, yb = outcome(dd, "admin", a), outcome(dd, "admin", b)
                dd["pre"] = np.log(yb / ya).where((ya > 0) & (yb > 0))
            else:
                dd["pre"] = np.log(dd[f"pop_{b}"] / dd[f"pop_{a}"])
            dd = dd.dropna(subset=["pre"])
            for z in ("bartik", "imm", "imm_nomex"):
                for weighted in (True, False):
                    run(dd, window=window, outcome_name=f"placebo: {kind} change {a}->{b}", sample="all", y="pre", x=z,
                        weighted=weighted, method=f"placebo reduced form (OLS of pre-period change on {z})")
                    run(dd, window=window, outcome_name=f"main-period reduced form, same sample", sample=f"placebo {kind} {a}->{b} sample",
                        y="dy" if kind == "outcome" else "dx", x=z, weighted=weighted,
                        method=f"reduced form (OLS of {'outcome' if kind == 'outcome' else 'population'} change on {z})")
    est = pd.DataFrame(ROWS)
    est.to_csv(DERIVED / "estimates.csv", index=False, float_format="%.6g")
    pd.concat(rot_out).to_csv(DERIVED / "rotemberg.csv", index=False, float_format="%.6g")
    cs = cross_section()
    cs.to_csv(DERIVED / "cross_section.csv", index=False, float_format="%.6g")
    summary["n_rows"] = len(est)
    summary["key"], summary["map_points"] = key_results(est, cs)
    (DERIVED / "estimates_summary.json").write_text(
        json.dumps(summary, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)) + "\n")
    print(f"[done] {len(est)} estimates, {len(cs)} cross-section rows", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

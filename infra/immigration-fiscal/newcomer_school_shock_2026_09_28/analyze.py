"""School fixed-effects estimates for the 2022-2024 newcomer surge in NYC, Chicago and Denver.

Reads the city panels in derived/ (built by build_nyc.py, build_chicago.py, build_denver.py) and the statewide
scale-score SDs (derived/scale_sd.csv, from extract_scale_sd.py). Writes:
  derived/exposure_by_school.csv      one row per city x school: the intensity X and its parts
  derived/exposure_summary.csv        citywide counts by year and the distribution of X
  derived/estimates.csv               every coefficient: city, block, outcome, spec, term, coef, se, ...
  derived/analysis_audit.json         input hashes, samples, pre-trend Wald tests

Design. Exposure is the net inflow of newcomers between the October count of 2021 and the October count of 2024,
per pupil enrolled in 2021-22: X = (count_2025 - count_2022) / enrollment_2022 (years are spring years). The count
is English learners in NYC (demographic snapshot) and Chicago (CPS 20th day) and CDE "Immigrant" pupils in
Denver. Event study: y = unit FE + time FE + sum_k b_k * X * 1[year = k], base year 2022, SEs clustered by school.
Coefficients are reported per unit of X and per 10 percentage points (x 0.1).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
        infra/immigration-fiscal/newcomer_school_shock_2026_09_28/analyze.py
"""

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
D = LANE / "derived"
BASE = 2022
PEAK = 2025
MIN_ENROLL = 100

INPUTS = ["nyc_schools.csv", "nyc_scores.csv", "nyc_class_size.csv", "chicago_schools.csv", "chicago_scores.csv",
          "denver_schools.csv", "denver_scores.csv", "scale_sd.csv"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------------------------------- statistics
def gammaincc(a, x):
    """Regularized upper incomplete gamma Q(a, x) (Numerical Recipes gser/gcf)."""
    if x <= 0:
        return 1.0
    gln = math.lgamma(a)
    if x < a + 1:
        ap, s, d = a, 1.0 / a, 1.0 / a
        for _ in range(500):
            ap += 1
            d *= x / ap
            s += d
            if abs(d) < abs(s) * 1e-14:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - gln)
    b, c, dd = x + 1 - a, 1e300, 1.0 / (x + 1 - a)
    h = dd
    for i in range(1, 500):
        an = -i * (i - a)
        b += 2
        dd = an * dd + b
        dd = 1e-300 if abs(dd) < 1e-300 else dd
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        dd = 1.0 / dd
        de = dd * c
        h *= de
        if abs(de - 1) < 1e-14:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def design(df, regs, time, extra_fe):
    parts = [df[regs].astype(float), pd.get_dummies(df[time].astype(str), prefix="t", drop_first=True, dtype=float)]
    for fe in extra_fe:
        parts.append(pd.get_dummies(df[fe].astype(str), prefix=fe, drop_first=True, dtype=float))
    return pd.concat(parts, axis=1)


def fe_fit(df, y, regs, unit, time, weight, cluster, extra_fe=()):
    """WLS with unit FE (within transformation; weights constant within unit) and time dummies; CR1 by cluster."""
    df = df.dropna(subset=[y] + regs + [weight]).copy()
    df = df[df[weight] > 0]
    # singleton units carry no within information
    df = df[df.groupby(unit)[y].transform("size") > 1]
    if df[unit].nunique() < 20:
        return None
    if (df.groupby(unit)[weight].nunique() > 1).any():
        raise SystemExit(f"[BLOCKED] weight {weight} varies within unit")
    X = design(df, regs, time, extra_fe)
    cols = list(X.columns)
    Xm = X - X.groupby(df[unit]).transform("mean")
    ym = df[y].astype(float) - df.groupby(unit)[y].transform("mean")
    keep = [c for c in cols if (Xm[c].abs() > 1e-12).any()]
    Xm = Xm[keep].to_numpy()
    yv = ym.to_numpy()
    w = df[weight].to_numpy(dtype=float)
    XtW = Xm.T * w
    A = XtW @ Xm
    Ainv = np.linalg.pinv(A)
    b = Ainv @ (XtW @ yv)
    e = yv - Xm @ b
    g = df[cluster].to_numpy()
    order = np.argsort(g, kind="stable")
    gs, idx = np.unique(g[order], return_index=True)
    score = (Xm * (w * e)[:, None])[order]
    S = np.add.reduceat(score, idx, axis=0)
    G, N, K = len(gs), len(yv), Xm.shape[1]
    V = Ainv @ (S.T @ S) @ Ainv * (G / (G - 1)) * ((N - 1) / (N - K))
    out = {c: (float(b[i]), float(math.sqrt(max(V[i, i], 0.0)))) for i, c in enumerate(keep)}
    return {"coef": out, "V": V, "cols": keep, "n": N, "units": int(df[unit].nunique()), "clusters": G}


def iv_fit(df, y, endog, instr, unit, time, weight, cluster, extra_fe=()):
    """2SLS with unit FE absorbed and time dummies as exogenous regressors; CR1 by cluster."""
    df = df.dropna(subset=[y] + endog + instr + [weight]).copy()
    df = df[(df[weight] > 0) & (df.groupby(unit)[y].transform("size") > 1)]
    W = design(df, [], time, extra_fe)
    dm = lambda M: (M - M.groupby(df[unit]).transform("mean")).to_numpy(dtype=float)
    Xe, Z, Wx = dm(df[endog].astype(float)), dm(df[instr].astype(float)), dm(W)
    Wx = Wx[:, np.abs(Wx).sum(axis=0) > 1e-12]
    yv = dm(df[[y]].astype(float))[:, 0]
    w = df[weight].to_numpy(dtype=float)
    Zf = np.c_[Z, Wx]
    ZtW = Zf.T * w
    Xhat = Zf @ np.linalg.pinv(ZtW @ Zf) @ (ZtW @ Xe)
    Xh, Xa = np.c_[Xhat, Wx], np.c_[Xe, Wx]
    A = (Xh.T * w) @ Xh
    Ainv = np.linalg.pinv(A)
    b = Ainv @ ((Xh.T * w) @ yv)
    e = yv - Xa @ b
    g = df[cluster].to_numpy()
    order = np.argsort(g, kind="stable")
    gs, idx = np.unique(g[order], return_index=True)
    S = np.add.reduceat((Xh * (w * e)[:, None])[order], idx, axis=0)
    G, N, K = len(gs), len(yv), Xh.shape[1]
    V = Ainv @ (S.T @ S) @ Ainv * (G / (G - 1)) * ((N - 1) / (N - K))
    # first-stage strength: partial F of the excluded instruments for each endogenous regressor (cluster-robust Wald / q)
    fs = []
    for j in range(len(endog)):
        Af = (Zf.T * w) @ Zf
        Afi = np.linalg.pinv(Af)
        bf = Afi @ ((Zf.T * w) @ Xe[:, j])
        ef = Xe[:, j] - Zf @ bf
        Sf = np.add.reduceat((Zf * (w * ef)[:, None])[order], idx, axis=0)
        Vf = Afi @ (Sf.T @ Sf) @ Afi * (G / (G - 1)) * ((N - 1) / (N - Zf.shape[1]))
        q = len(instr)
        bz, Vz = bf[:q], Vf[:q, :q]
        fs.append(float(bz @ np.linalg.pinv(Vz) @ bz) / q)
    cols = endog
    out = {c: (float(b[i]), float(math.sqrt(max(V[i, i], 0.0)))) for i, c in enumerate(cols)}
    return {"coef": out, "V": V, "cols": cols + [f"w{i}" for i in range(Wx.shape[1])], "n": N,
            "units": int(df[unit].nunique()), "clusters": G, "first_stage_F": fs}


def wald(fit, terms):
    terms = [t for t in terms if t in fit["cols"]]
    if not terms:
        return None
    ix = [fit["cols"].index(t) for t in terms]
    b = np.array([fit["coef"][t][0] for t in terms])
    V = fit["V"][np.ix_(ix, ix)]
    stat = float(b @ np.linalg.pinv(V) @ b)
    return stat, len(terms), gammaincc(len(terms) / 2.0, stat / 2.0)


# ----------------------------------------------------------------------------------------------- exposure
def intensity(panel, count, enroll, base=BASE, peak=PEAK):
    w = panel.pivot_table(index="school", columns="year", values=[count, enroll], aggfunc="first")
    out = pd.DataFrame({
        "count_base": w[count].get(base), "count_peak": w[count].get(peak),
        "count_mid": w[count].get(peak - 1), "enroll_base": w[enroll].get(base),
    })
    out["X"] = (out.count_peak - out.count_base) / out.enroll_base
    out["X_2024"] = (out.count_mid - out.count_base) / out.enroll_base
    out = out[(out.enroll_base >= MIN_ENROLL)].dropna(subset=["X"])
    return out


def share_by_year(panel, count, enroll, X):
    """N_st = (count_t - count_base) / enroll_base for t > base, else 0."""
    p = panel[["school", "year", count]].merge(X[["count_base", "enroll_base"]], left_on="school", right_index=True)
    p["N"] = np.where(p.year > BASE, (p[count] - p.count_base) / p.enroll_base, 0.0)
    return p[["school", "year", "N"]]


# ----------------------------------------------------------------------------------------------- panels
def sd_table():
    s = pd.read_csv(D / "scale_sd.csv")
    s["subject"] = s.subject.str.lower()
    s = s[s.state.isin(["NY", "CO", "IL"])]
    return {(r.state, int(r.year), r.subject, str(r.grade)): (float(r["mean"]), float(r.sd)) for _, r in s.iterrows()}


def nyc():
    s = pd.read_csv(D / "nyc_schools.csv", dtype={"dbn": str}, low_memory=False)
    s = s[s.district <= 32].rename(columns={"dbn": "school"})
    X = intensity(s, "ell_n", "enroll_total")
    # shelter-routed newcomer counts from the allocation memos: SAM 65 ($2,000 per first-time entrant in temporary
    # housing, Jul-Oct 2022, schools with 6+) and SAM 90 (about $50 per first-time admit in temporary housing,
    # Jul 2023-Feb 2024, extra weight for 2024 entrants, $600 floor): a weighted count, not a head count
    sam = s.pivot_table(index="school", columns="year", values=["sam65_open_arms_alloc", "sam90_sth_increase_alloc"],
                        aggfunc="first")
    X["sam65_n"] = (sam["sam65_open_arms_alloc"].get(2023) / 2000.0).reindex(X.index).fillna(0.0)
    X["sam90_wn"] = (sam["sam90_sth_increase_alloc"].get(2024) / 50.0).reindex(X.index).fillna(0.0)
    X["Z_sam"] = (X.sam65_n + X.sam90_wn) / X.enroll_base
    # the $600 SAM 90 floor gives every school with any admit 12 weighted students; drop floor-only allocations
    X["Z_sam2"] = (X.sam65_n + X.sam90_wn.where(X.sam90_wn > 12.0 + 1e-9, 0.0)) / X.enroll_base
    b22 = s[s.year == BASE].set_index("school")
    b19 = s[s.year == 2019].set_index("school")
    X["ell_share22"] = (b22.ell_n / b22.enroll_total).reindex(X.index)
    X["eni22"] = b22.eni.reindex(X.index)
    X["dlnenr_19_22"] = (np.log(b22.enroll_total) - np.log(b19.enroll_total)).reindex(X.index)
    sc = pd.read_csv(D / "nyc_scores.csv", dtype={"dbn": str, "grade": str}, low_memory=False)
    sc = sc.rename(columns={"dbn": "school"})
    sc = sc[sc.school.str[:2].astype(int) <= 32]
    return s, X, sc


def denver():
    s = pd.read_csv(D / "denver_schools.csv", dtype={"school_id": str}, low_memory=False)
    s = s.rename(columns={"school_id": "school"})
    # a blank immigrant or EL cell means 0-3 pupils (0-15 in 2018 and 2020); counted as 0 here
    for c in ("immigrant_n", "el_n"):
        s[c + "0"] = s[c].fillna(0.0)
    X = intensity(s, "immigrant_n0", "enroll_total")
    Xel = intensity(s, "el_n0", "enroll_total")
    X["X_el"] = Xel["X"].reindex(X.index)
    b22 = s[s.year == BASE].set_index("school")
    b19 = s[s.year == 2019].set_index("school")
    X["el_share22"] = (b22.el_n0 / b22.enroll_total).reindex(X.index)
    X["dlnenr_19_22"] = (np.log(b22.enroll_total) - np.log(b19.enroll_total)).reindex(X.index)
    sc = pd.read_csv(D / "denver_scores.csv", dtype={"school_id": str, "grade": str}, low_memory=False)
    sc = sc.rename(columns={"school_id": "school"})
    return s, X, sc


def chicago():
    s = pd.read_csv(D / "chicago_schools.csv", dtype={"school_id": str, "cps_school_id": str}, low_memory=False)
    s = s[s.row_source == "isbe"].rename(columns={"school_id": "school"})
    X = intensity(s, "cps20_el_n", "cps20_enroll_total")
    sc = pd.read_csv(D / "chicago_scores.csv", dtype={"school_id": str, "cps_school_id": str, "grade": str},
                     low_memory=False)
    sc = sc.rename(columns={"school_id": "school"})
    return s, X, sc


# ----------------------------------------------------------------------------------------------- estimation
ROWS = []
WALD = []


def record(city, block, outcome, spec, fit, terms, extra=None):
    if fit is None:
        ROWS.append({"city": city, "block": block, "outcome": outcome, "spec": spec, "term": "NA",
                     "note": "fewer than 20 units"})
        return
    for t in terms:
        if t not in fit["coef"]:
            continue
        b, se = fit["coef"][t]
        ROWS.append({"city": city, "block": block, "outcome": outcome, "spec": spec, "term": t,
                     "coef": b, "se": se, "coef_per10pp": 0.1 * b, "se_per10pp": 0.1 * se,
                     "n_obs": fit["n"], "n_units": fit["units"], "n_clusters": fit["clusters"],
                     **(extra or {})})


def year_interactions(df, cols, years):
    """Baseline covariate x year dummies (base year omitted), to let schools that looked alike in 2022 trend alike."""
    names = []
    for c in cols:
        for k in years:
            if k == BASE:
                continue
            n = f"{c}_x_{k}"
            df[n] = df[c] * (df.year == k)
            names.append(n)
    return names


def event_study(city, block, outcome, spec, df, y, xcol, unit, time, weight, years, pre_years, controls=(),
                extra_fe=(), trend=False):
    df = df.copy()
    terms = []
    for k in years:
        if k == BASE or (trend and k < BASE):
            continue
        t = f"X_{k}"
        df[t] = df[xcol] * (df.year == k)
        terms.append(t)
    ctl = year_interactions(df, list(controls), years) if controls else []
    if trend:
        # linear trend in X fitted on the pre years; post terms are deviations from its extrapolation
        df["X_trend"] = df[xcol] * (df.year - BASE)
        ctl = ctl + ["X_trend"]
    df = df.dropna(subset=list(controls)) if controls else df
    fit = fe_fit(df, y, terms + ctl, unit, time, weight, "school", extra_fe)
    if trend:
        record(city, block, outcome, spec, fit, terms + ["X_trend"])
        return fit
    record(city, block, outcome, spec, fit, terms)
    if fit is not None:
        wd = wald(fit, [f"X_{k}" for k in pre_years])
        if wd:
            WALD.append({"city": city, "block": block, "outcome": outcome, "spec": spec,
                         "pre_years": pre_years, "wald": wd[0], "df": wd[1], "p": wd[2]})
    post = [k for k in years if k > BASE]
    df["X_post"] = df[xcol] * (df.year > BASE)
    fit2 = fe_fit(df, y, ["X_post"] + ctl, unit, time, weight, "school", extra_fe)
    record(city, block, outcome, spec + "|pooled_post" + "".join(f"_{k}" for k in post), fit2, ["X_post"])
    return fit


def achievement_grade_panel(sc, state, sdt, group_filter, years, subject):
    """Grade rows 3-8 -> z = (mean - state mean) / state SD; unit = school x grade; time = grade x year."""
    g = sc[group_filter(sc) & sc.grade.isin(["3", "4", "5", "6", "7", "8"]) & (sc.subject == subject)].copy()
    g = g[g.year.isin(years)]
    key = list(zip([state] * len(g), g.year.astype(int), g.subject, g.grade))
    ms = [sdt.get(k) for k in key]
    g["state_mean"] = [m[0] if m else np.nan for m in ms]
    g["state_sd"] = [m[1] if m else np.nan for m in ms]
    g["z"] = (g.mean_scale_score - g.state_mean) / g.state_sd
    g["unit"] = g.school + "_" + g.grade
    g["time"] = g.grade + "_" + g.year.astype(str)
    base_n = g[g.year == BASE].set_index("unit").n_tested
    g["w_base"] = g.unit.map(base_n)
    g["one"] = 1.0
    return g


def run_nyc(audit):
    s, X, sc = nyc()
    sdt = sd_table()
    years_sd = [2018, 2019, 2022, 2023, 2024, 2025]
    pre = [2018, 2019]
    for subject in ("ela", "math"):
        for cat, lab in (("Never ELL", "never_ell"), ("Ever ELL", "ever_ell"), ("All Students", "all")):
            g = achievement_grade_panel(sc, "NY", sdt, lambda d, c=cat: d.category == c, years_sd, subject)
            g = g.merge(X, left_on="school", right_index=True)
            for xcol in ("X", "X_2024", "Z_sam"):
                for wcol in ("w_base", "one"):
                    spec = f"grade_rows|{xcol}|{'w_base_n' if wcol == 'w_base' else 'unweighted'}"
                    if lab != "never_ell" and (xcol != "X"):
                        continue
                    event_study("nyc", "achievement", f"{lab}_{subject}_z", spec, g.dropna(subset=["z"]), "z", xcol,
                                "unit", "time", wcol if wcol == "one" else "w_base", years_sd, pre)
            if lab == "never_ell":
                g["dist_year"] = g.school.str[:2] + "_" + g.year.astype(str)
                gz = g.dropna(subset=["z"])
                base = ("nyc", "achievement", f"{lab}_{subject}_z")
                event_study(*base, "grade_rows|X|w_base_n|district_x_year", gz, "z", "X", "unit", "time", "w_base",
                            years_sd, pre, extra_fe=("dist_year",))
                event_study(*base, "grade_rows|X|w_base_n|ctrl_base_x_year", gz, "z", "X", "unit", "time", "w_base",
                            years_sd, pre, controls=("ell_share22", "eni22", "dlnenr_19_22"))
                event_study(*base, "grade_rows|X|w_base_n|linear_pretrend", gz, "z", "X", "unit", "time", "w_base",
                            years_sd, pre, trend=True)
                for zc in ("Z_sam2",):
                    event_study(*base, f"grade_rows|{zc}|w_base_n", gz, "z", zc, "unit", "time", "w_base", years_sd, pre)
                    event_study(*base, f"grade_rows|{zc}|w_base_n|district_x_year", gz, "z", zc, "unit", "time",
                                "w_base", years_sd, pre, extra_fe=("dist_year",))
                # 2SLS: X instrumented by the shelter-routed memo intensity, year by year and pooled
                gi = gz.copy()
                endog, instr = [], []
                for k in years_sd:
                    if k == BASE:
                        continue
                    gi[f"X_{k}"] = gi.X * (gi.year == k)
                    gi[f"Z_{k}"] = gi.Z_sam2 * (gi.year == k)
                    endog.append(f"X_{k}")
                    instr.append(f"Z_{k}")
                fit = iv_fit(gi, "z", endog, instr, "unit", "time", "w_base", "school")
                record(*base, "grade_rows|X_iv_Z_sam2|w_base_n", fit, endog,
                       {"note": "first-stage F " + " ".join(f"{f:.1f}" for f in fit["first_stage_F"])})
                gi["X_post"] = gi.X * (gi.year > BASE)
                gi["Z_post"] = gi.Z_sam2 * (gi.year > BASE)
                fit = iv_fit(gi, "z", ["X_post"], ["Z_post"], "unit", "time", "w_base", "school")
                record(*base, "grade_rows|X_iv_Z_sam2|w_base_n|pooled_post_2023_2024_2025", fit, ["X_post"],
                       {"note": f"first-stage F {fit['first_stage_F'][0]:.1f}"})
                # time-varying share: newcomer share measured at the October count of each school year
                N = share_by_year(s, "ell_n", "enroll_total", X)
                gg = g.merge(N, on=["school", "year"], how="left").dropna(subset=["N", "z"])
                fit = fe_fit(gg, "z", ["N"], "unit", "time", "w_base", "school")
                record("nyc", "achievement", f"{lab}_{subject}_z", "grade_rows|N_share_t|w_base_n", fit, ["N"])
                # scale points, through 2026 (no 2026 SD published)
                gp = achievement_grade_panel(sc, "NY", sdt, lambda d, c=cat: d.category == c,
                                             years_sd + [2026], subject).merge(X, left_on="school", right_index=True)
                # flight: never-ELL test takers per school-grade (published even where scores are suppressed)
                gl = gp[gp.n_tested > 0].copy()
                gl["ln_n"] = np.log(gl.n_tested)
                event_study("nyc", "composition", f"{lab}_{subject}_ln_n_tested", "grade_rows|X|w_base_n", gl,
                            "ln_n", "X", "unit", "time", "w_base", years_sd + [2026], pre)
                gp = gp.dropna(subset=["mean_scale_score"])
                gp = gp.assign(pts=gp.mean_scale_score)
                event_study("nyc", "achievement", f"{lab}_{subject}_points", "grade_rows|X|w_base_n", gp, "pts", "X",
                            "unit", "time", "w_base", years_sd + [2026], pre)
    # school-level resources, all schools in districts 1-32
    r = s.merge(X, left_on="school", right_index=True)
    r["ln_enroll"] = np.log(r.enroll_total.where(r.enroll_total > 0))
    r["ln_teach"] = np.log(r.num_teach.where(r.num_teach > 0))
    r["ln_exp"] = np.log(r.exp_total.where(r.exp_total > 0))
    r["ln_exp_sl"] = np.log(r.exp_state_local.where(r.exp_state_local > 0))
    r["ptr_own"] = r.enroll_total / r.num_teach.where(r.num_teach > 0)
    r["ln_ppe"] = np.log(r.ppe_total.where(r.ppe_total > 0))
    r["w_enroll"] = r.enroll_base
    yrs = list(range(2018, 2027))
    for out, years, pre_y in (("ln_enroll", yrs, [2018, 2019, 2020, 2021]),
                              ("ln_teach", list(range(2018, 2026)), [2018, 2019, 2020, 2021]),
                              ("ptr_own", list(range(2018, 2026)), [2018, 2019, 2020, 2021]),
                              ("ln_exp", list(range(2019, 2026)), [2019, 2020, 2021]),
                              ("ln_exp_sl", list(range(2019, 2026)), [2019, 2020, 2021]),
                              ("ln_ppe", list(range(2019, 2026)), [2019, 2020, 2021]),
                              ("k5_avg_class", [2018, 2019, 2020, 2022, 2023, 2024, 2025, 2026], [2018, 2019, 2020])):
        rr = r[r.year.isin(years)].copy()
        event_study("nyc", "resources", out, "school_rows|X|w_enroll", rr, out, "X", "school", "year", "w_enroll",
                    years, pre_y)
        rr["dist_year"] = rr.school.str[:2] + "_" + rr.year.astype(str)
        event_study("nyc", "resources", out, "school_rows|X|w_enroll|district_x_year", rr, out, "X", "school", "year",
                    "w_enroll", years, pre_y, extra_fe=("dist_year",))
        event_study("nyc", "resources", out, "school_rows|Z_sam2|w_enroll", rr, out, "Z_sam2", "school", "year",
                    "w_enroll", years, pre_y)
        if out in ("ln_exp", "ln_exp_sl", "ln_ppe"):
            # FY2024 reporting break: school-level spending rose 56% at the median while the citywide per-pupil
            # figure rose 12%; let the break load on baseline spending per pupil
            base_ppe = r[r.year == BASE].set_index("school").ppe_total
            rr = rr.assign(lnppe22=np.log(rr.school.map(base_ppe)))
            for k in years:
                rr[f"b_{k}"] = rr.lnppe22 * (rr.year == k)
            ctl = [f"b_{k}" for k in years if k != BASE]
            dfc = rr.copy()
            terms = []
            for k in years:
                if k == BASE:
                    continue
                dfc[f"X_{k}"] = dfc.X * (dfc.year == k)
                terms.append(f"X_{k}")
            fit = fe_fit(dfc, out, terms + ctl, "school", "year", "w_enroll", "school")
            record("nyc", "resources", out, "school_rows|X|w_enroll|ctrl_lnppe2022_x_year", fit, terms)
    # within-year class-size change, November to June (reports exist from 2023-24)
    cs = pd.read_csv(D / "nyc_class_size.csv", dtype={"dbn": str}).rename(columns={"dbn": "school"})
    piv = cs.pivot_table(index=["school", "year"], columns="timing", values="k5_avg_class", aggfunc="first").reset_index()
    piv = piv.merge(X, left_on="school", right_index=True)
    for yr in (2024, 2025, 2026):
        p = piv[(piv.year == yr)].dropna(subset=["nov", "jun"])
        if len(p) > 50:
            A = np.c_[np.ones(len(p)), p.X]
            b = np.linalg.lstsq(A, p.jun - p.nov, rcond=None)[0]
            e = (p.jun - p.nov) - A @ b
            V = np.linalg.pinv(A.T @ A) @ (A.T * e.to_numpy() ** 2) @ A @ np.linalg.pinv(A.T @ A) * len(p) / (len(p) - 2)
            ROWS.append({"city": "nyc", "block": "resources", "outcome": "k5_class_jun_minus_nov",
                         "spec": f"cross_section_{yr}|X|unweighted|HC1", "term": "X", "coef": b[1],
                         "se": math.sqrt(V[1, 1]), "coef_per10pp": 0.1 * b[1], "se_per10pp": 0.1 * math.sqrt(V[1, 1]),
                         "n_obs": len(p), "n_units": len(p), "n_clusters": len(p), "mean_dep": float((p.jun - p.nov).mean())})
    audit["nyc"] = {"schools_with_X": int(len(X)), "X_mean": float(X.X.mean()),
                    "X_enroll_weighted_mean": float((X.X * X.enroll_base).sum() / X.enroll_base.sum()),
                    "corr_X_Zsam": float(X.X.corr(X.Z_sam)), "sam65_n_sum": float(X.sam65_n.sum()),
                    "sam90_weighted_n_sum": float(X.sam90_wn.sum())}
    return X


def run_denver(audit):
    s, X, sc = denver()
    sdt = sd_table()
    years = [2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026]
    for subject in ("ela", "math"):
        for grp, lab, yrs, pre in (("phlote_na_nr", "never_el", [2019, 2021, 2022, 2023, 2024, 2025, 2026], [2019, 2021]),
                                   ("not_el", "not_el", [2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025, 2026],
                                    [2017, 2018, 2019, 2021]),
                                   ("all", "all", years, [2017, 2018, 2019, 2021])):
            if lab == "not_el":
                filt = lambda d: (d.group == "not_el") | ((d.group == "phlote_fell_na") & d.year.isin([2017, 2018]))
            else:
                filt = lambda d, gname=grp: d.group == gname
            g = achievement_grade_panel(sc, "CO", sdt, filt, yrs, subject).merge(X, left_on="school", right_index=True)
            for xcol in (("X", "X_2024", "X_el") if lab == "never_el" else ("X",)):
                for wcol in (("w_base", "one") if lab == "never_el" else ("w_base",)):
                    spec = f"grade_rows|{xcol}|{'w_base_n' if wcol == 'w_base' else 'unweighted'}"
                    event_study("denver", "achievement", f"{lab}_{subject}_z", spec, g.dropna(subset=["z"]), "z",
                                xcol, "unit", "time", wcol, yrs, pre)
            if lab == "never_el":
                gz = g.dropna(subset=["z"])
                event_study("denver", "achievement", f"{lab}_{subject}_z", "grade_rows|X|w_base_n|ctrl_base_x_year",
                            gz, "z", "X", "unit", "time", "w_base", yrs, pre, controls=("el_share22", "dlnenr_19_22"))
                N = share_by_year(s, "immigrant_n0", "enroll_total", X)
                gg = g.merge(N, on=["school", "year"], how="left").dropna(subset=["N", "z"])
                fit = fe_fit(gg, "z", ["N"], "unit", "time", "w_base", "school")
                record("denver", "achievement", f"{lab}_{subject}_z", "grade_rows|N_share_t|w_base_n", fit, ["N"])
                gl = g[g.n_tested > 0].copy()
                gl["ln_n"] = np.log(gl.n_tested)
                event_study("denver", "composition", f"{lab}_{subject}_ln_n_tested", "grade_rows|X|w_base_n", gl,
                            "ln_n", "X", "unit", "time", "w_base", yrs, pre)
    r = s.merge(X, left_on="school", right_index=True)
    r["ln_enroll"] = np.log(r.enroll_total.where(r.enroll_total > 0))
    r["ln_teach"] = np.log(r.teacher_fte.where(r.teacher_fte > 0))
    r["ptr"] = r.pupil_teacher_ratio
    r["ln_site_exp"] = np.log((r.ppe_site_total * r.ppe_membership).where(r.ppe_site_total > 0))
    r["ln_site_ppe"] = np.log(r.ppe_site_total.where(r.ppe_site_total > 0))
    r["w_enroll"] = r.enroll_base
    for out, yrs, pre in (("ln_enroll", list(range(2017, 2027)), [2017, 2018, 2019, 2020, 2021]),
                          ("ln_teach", list(range(2017, 2027)), [2017, 2018, 2019, 2020, 2021]),
                          ("ptr", list(range(2017, 2027)), [2017, 2018, 2019, 2020, 2021]),
                          ("ln_site_exp", list(range(2019, 2026)), [2019, 2020, 2021]),
                          ("ln_site_ppe", list(range(2019, 2026)), [2019, 2020, 2021])):
        event_study("denver", "resources", out, "school_rows|X|w_enroll", r[r.year.isin(yrs)], out, "X", "school",
                    "year", "w_enroll", yrs, pre)
    audit["denver"] = {"schools_with_X": int(len(X)), "X_mean": float(X.X.mean()),
                       "X_enroll_weighted_mean": float((X.X * X.enroll_base).sum() / X.enroll_base.sum()),
                       "corr_X_Xel": float(X.X.corr(X.X_el))}
    return X


def run_chicago(audit):
    s, X, sc = chicago()
    elem = set(s[s.school_type.fillna("").str.upper().str.contains("ELEMENTARY")].school)
    # non-EL = all minus EL at school level (ISBE counts); rows with EL counts hidden under 10 carry bounds
    d = sc[(sc.source == "derived_all_minus_el") & sc.school.isin(elem)].copy()
    d["pct"] = d.pct_proficient.where(d.pct_proficient.notna(), (d.pct_proficient_min + d.pct_proficient_max) / 2)
    d["exact"] = (d.pct_proficient_method == "all_minus_el").astype(int)
    d["one"] = 1.0
    years = [2018, 2019, 2021, 2022, 2023]
    for subject in ("ela", "math"):
        g = d[(d.subject == subject) & d.year.isin(years)].merge(X, left_on="school", right_index=True)
        base_n = g[g.year == BASE].set_index("school").n_tested
        g["w_base"] = g.school.map(base_n)
        g["unit"] = g.school
        g["time"] = g.year
        for xcol in ("X", "X_2024"):
            for wcol in ("w_base", "one"):
                event_study("chicago", "achievement", f"non_el_{subject}_pct_prof", f"school_rows|{xcol}|"
                            f"{'w_base_n' if wcol == 'w_base' else 'unweighted'}", g.dropna(subset=["pct"]), "pct",
                            xcol, "unit", "time", wcol, years, [2018, 2019, 2021])
        ge = g[g.exact == 1]
        event_study("chicago", "achievement", f"non_el_{subject}_pct_prof", "school_rows|X|w_base_n|exact_only",
                    ge.dropna(subset=["pct"]), "pct", "X", "unit", "time", "w_base", years, [2018, 2019, 2021])
    r = s.merge(X, left_on="school", right_index=True)
    r["ln_enroll"] = np.log(r.cps20_enroll_total.where(r.cps20_enroll_total > 0))
    r["ln_teach_sep"] = np.log(r.cps_teacher_fte_sep30.where(r.cps_teacher_fte_sep30 > 0))
    r["ln_teach_mar"] = np.log(r.cps_teacher_fte_mar31.where(r.cps_teacher_fte_mar31 > 0))
    r["ln_site_exp"] = np.log((r.ppe_site_total * r.ppe_enroll).where(r.ppe_site_total > 0))
    r["ln_site_ppe"] = np.log(r.ppe_site_total.where(r.ppe_site_total > 0))
    r["w_enroll"] = r.enroll_base
    for out, yrs, pre in (("ln_enroll", list(range(2017, 2026)), [2017, 2018, 2019, 2020, 2021]),
                          ("ln_teach_sep", list(range(2017, 2026)), [2017, 2018, 2019, 2020, 2021]),
                          ("ln_teach_mar", list(range(2017, 2026)), [2017, 2018, 2019, 2020, 2021]),
                          ("class_size_avg", list(range(2017, 2026)), [2017, 2018, 2019, 2020, 2021]),
                          ("ln_site_exp", list(range(2019, 2026)), [2019, 2020, 2021]),
                          ("ln_site_ppe", list(range(2019, 2026)), [2019, 2020, 2021])):
        event_study("chicago", "resources", out, "school_rows|X|w_enroll", r[r.year.isin(yrs)], out, "X", "school",
                    "year", "w_enroll", yrs, pre)
    audit["chicago"] = {"schools_with_X": int(len(X)), "X_mean": float(X.X.mean()),
                        "X_enroll_weighted_mean": float((X.X * X.enroll_base).sum() / X.enroll_base.sum()),
                        "elementary_schools": len(elem)}
    return X


def fmt(v):
    if v is None or (isinstance(v, float) and not math.isfinite(v)):
        return ""
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    if isinstance(v, (float, np.floating)):
        return f"{float(v):.6g}"
    if isinstance(v, list):
        return " ".join(str(x) for x in v)
    return str(v)


def write(path, rows, header):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow([fmt(r.get(h)) for h in header])


def main():
    audit = {"inputs": {n: sha256(D / n) for n in INPUTS}, "base_year": BASE, "peak_year": PEAK,
             "min_enroll_base": MIN_ENROLL}
    xs = {"nyc": run_nyc(audit), "denver": run_denver(audit), "chicago": run_chicago(audit)}
    ex = []
    for city, X in xs.items():
        for school, r in X.sort_index().iterrows():
            ex.append({"city": city, "school": school, **{k: r[k] for k in X.columns}})
    cols = ["city", "school", "count_base", "count_mid", "count_peak", "enroll_base", "X", "X_2024", "sam65_n",
            "sam90_wn", "Z_sam", "Z_sam2", "X_el", "ell_share22", "eni22", "el_share22", "dlnenr_19_22"]
    write(D / "exposure_by_school.csv", ex, cols)
    summ = []
    for city, X in xs.items():
        q = X.X.quantile([0.1, 0.5, 0.9, 0.99])
        summ.append({"city": city, "schools": len(X), "count_base_sum": X.count_base.sum(),
                     "count_peak_sum": X.count_peak.sum(), "enroll_base_sum": X.enroll_base.sum(),
                     "X_p10": q[0.1], "X_p50": q[0.5], "X_p90": q[0.9], "X_p99": q[0.99],
                     "share_X_ge_05": (X.X >= 0.05).mean(), "share_X_ge_10": (X.X >= 0.10).mean(),
                     "X_sd": X.X.std()})
    write(D / "exposure_summary.csv", summ, list(summ[0].keys()))
    hdr = ["city", "block", "outcome", "spec", "term", "coef", "se", "coef_per10pp", "se_per10pp", "n_obs",
           "n_units", "n_clusters", "mean_dep", "note"]
    ROWS.sort(key=lambda r: (r["city"], r["block"], r["outcome"], r["spec"], r["term"]))
    write(D / "estimates.csv", ROWS, hdr)
    WALD.sort(key=lambda r: (r["city"], r["block"], r["outcome"], r["spec"]))
    audit["pretrend_wald"] = [{k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()} for r in WALD]
    (D / "analysis_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True, default=float) + "\n")
    print(f"estimates: {len(ROWS)} rows; wald tests: {len(WALD)}")


if __name__ == "__main__":
    main()

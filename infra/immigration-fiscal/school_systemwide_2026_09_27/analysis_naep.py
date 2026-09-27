"""Test 2: do state NAEP scores of white and non-English-learner pupils fall where the English-learner,
Hispanic or immigrant share of enrollment rose? State and year fixed effects, SEs clustered by state.

Outputs (derived/):
  naep_estimates.csv   every coefficient: per 10-point change in the share, in NAEP points (per cell)
                       or in national student SDs (pooled over the four grade-subject cells)
  naep_eventstudy.csv  coefficients of the 2003→2019 share change interacted with each wave
  shares_summary.csv   observed share changes by state, 2003→2019 and 2019→2024

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_naep.py
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from panel import ALL_YEARS, CELLS, MAIN_YEARS, build  # noqa: E402
from stats_util import ols, t_quantile  # noqa: E402

OUT = HERE / "derived"
TREAT = {  # name: (column, label)
    "hisp": ("hisp_share", "Hispanic share of K-12 enrollment, CCD (fall t-1)"),
    "el": ("el_identified_pct_all", "English learners identified by NAEP, % of the grade's pupils"),
    "imm": ("imm_origin_share_617", "Children 6-17 with a foreign-born parent, ACS"),
    "fb": ("fb_share_u18", "Foreign-born share of under-18s, ACS"),
}
OUTCOMES = ["white", "nonel", "white_nonel", "all", "white_p10", "white_p90", "black", "hisp_nonel"]
FIELDS = ["test", "spec", "treatment", "outcome", "cell", "units", "beta_per10", "se", "ci95_lo", "ci95_hi", "p",
          "mde80", "n_obs", "n_states", "years", "note"]


def fmt(x, nd=4):
    return "" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nd}f}"


def record(rows, res, name, **meta):
    r = res[name]
    q = t_quantile(0.975, r["dof"])
    b, se = 10 * r["coef"], 10 * r["se"]
    rows.append({**meta, "beta_per10": fmt(b), "se": fmt(se), "ci95_lo": fmt(b - q * se), "ci95_hi": fmt(b + q * se),
                 "p": fmt(r["p"]), "mde80": fmt((q + 0.8416) * se), "n_obs": r["n"], "n_states": r["clusters"]})


def stack(p, years, outcome):
    """Pooled panel over the four cells, outcome in national student SDs (2019 all-student SD)."""
    d = p[p.year.isin(years)].copy()
    d["z"] = d[outcome] / d.sd2019
    d["cell_state"] = d.cell + "|" + d.state
    d["cell_year"] = d.cell + "|" + d.year.astype(str)
    d["region_cell_year"] = d.region + "|" + d.cell_year
    return d


def twfe(rows, p, tkey, outcome, years, spec, extra_fe=(), controls=(), weight=None, trend=False, note=""):
    col = TREAT[tkey][0]
    d = stack(p, years, outcome)
    x = [col] + list(controls)
    fe = ["cell_state", "cell_year"] + list(extra_fe)
    if trend:  # state-by-cell linear trends
        keys = sorted(d.cell_state.unique())
        tr = pd.DataFrame({"tr_" + k: np.where(d.cell_state == k, d.year - 2003, 0.0) for k in keys}, index=d.index)
        d = pd.concat([d, tr], axis=1)
        x = x + ["tr_" + k for k in keys[1:]]
    res = ols(d, "z", x, fe=fe, cluster="state", weight=weight)
    record(rows, res, col, test="naep", spec=spec, treatment=tkey, outcome=outcome, cell="pooled", units="SD",
           years=f"{min(years)}-{max(years)}", note=note)
    if spec == "twfe" and not controls:
        for subject, grade in CELLS:
            c = d[(d.subject == subject) & (d.grade == grade)]
            r = ols(c, outcome, [col], fe=["state", "year"], cluster="state", weight=weight)
            record(rows, r, col, test="naep", spec=spec, treatment=tkey, outcome=outcome,
                   cell=f"{subject[:4]}{grade}", units="points", years=f"{min(years)}-{max(years)}", note=note)


def long_diff(rows, p, tkey, outcome, y0, y1, spec, note=""):
    col = TREAT[tkey][0]
    a = p[p.year == y0].set_index(["cell", "state"])
    b = p[p.year == y1].set_index(["cell", "state"])
    d = pd.DataFrame({"dy": (b[outcome] - a[outcome]) / b.sd2019, "dx": b[col] - a[col]}).dropna().reset_index()
    d = d.rename(columns={"dx": col})
    res = ols(d, "dy", [col], fe=["cell"], cluster="state")
    record(rows, res, col, test="naep", spec=spec, treatment=tkey, outcome=outcome, cell="pooled", units="SD",
           years=f"{y0}->{y1}", note=note)
    for cell in sorted(d.cell.unique()):
        c = d[d.cell == cell].copy()
        c["dy_pts"] = c.dy * p[(p.cell == cell)].sd2019.iloc[0]
        r = ols(c, "dy_pts", [col], cluster=None)
        record(rows, r, col, test="naep", spec=spec, treatment=tkey, outcome=outcome, cell=cell, units="points",
               years=f"{y0}->{y1}", note=note + "; HC1")


def first_diff(rows, p, tkey, outcome, years):
    col = TREAT[tkey][0]
    d = stack(p, years, outcome).sort_values(["cell", "state", "year"])
    g = d.groupby(["cell", "state"])
    d["dz"] = g.z.diff()
    d["dx"] = g[col].diff()
    d = d.dropna(subset=["dz", "dx"]).rename(columns={"dx": "dx_" + col})
    res = ols(d, "dz", ["dx_" + col], fe=["cell_year"], cluster="state")
    record(rows, res, "dx_" + col, test="naep", spec="first_diff", treatment=tkey, outcome=outcome, cell="pooled",
           units="SD", years=f"{min(years)}-{max(years)}", note="consecutive-wave changes, cell-by-year FE")


def lead_test(rows, p, tkey, outcome):
    """Next wave's share added to the current share, 2003–2017 waves (lead defined through 2019)."""
    col = TREAT[tkey][0]
    d = stack(p, MAIN_YEARS, outcome).sort_values(["cell", "state", "year"])
    d["lead_" + col] = d.groupby(["cell", "state"])[col].shift(-1)
    d = d[d.year <= 2017]
    res = ols(d, "z", [col, "lead_" + col], fe=["cell_state", "cell_year"], cluster="state")
    record(rows, res, "lead_" + col, test="naep", spec="lead", treatment=tkey, outcome=outcome, cell="pooled",
           units="SD", years="2003-2017", note="coefficient on the next wave's share, current share held fixed")


def event_study(ev_rows, p, tkey, outcome):
    """y = state + wave FE + sum_k delta_k * (share change 2003→2019) * 1[wave = k]; base wave 2003.
    Pre-period waves: math 1996/2000, reading 1998/2002 (states that volunteered for state NAEP)."""
    col = TREAT[tkey][0]
    for subject, grade in CELLS:
        c = p[(p.subject == subject) & (p.grade == grade)].copy()
        dx = (c[c.year == 2019].set_index("state")[col] - c[c.year == 2003].set_index("state")[col]).rename("D")
        c = c.merge(dx, left_on="state", right_index=True).dropna(subset=[outcome, "D"])
        waves = sorted(w for w in c.year.unique() if w <= 2019 and w != 2003)
        c = c[c.year <= 2019]
        names = []
        for w in waves:
            c[f"D_{w}"] = np.where(c.year == w, c.D, 0.0)
            names.append(f"D_{w}")
        res = ols(c, outcome, names, fe=["state", "year"], cluster="state")
        for w, nm in zip(waves, names):
            r = res[nm]
            q = t_quantile(0.975, r["dof"])
            ev_rows.append({"treatment": tkey, "outcome": outcome, "cell": f"{subject[:4]}{grade}", "wave": w,
                            "delta_per10_points": fmt(10 * r["coef"]), "se": fmt(10 * r["se"]),
                            "ci95_lo": fmt(10 * (r["coef"] - q * r["se"])), "ci95_hi": fmt(10 * (r["coef"] + q * r["se"])),
                            "p": fmt(r["p"]), "n_states_wave": int(c[c.year == w].state.nunique()),
                            "n_obs": r["n"]})


def pre_placebo(rows, p, tkey, outcome):
    """Change over the pre-period (math 2000→2003, reading 1998→2003) on the 2003→2019 share change."""
    col = TREAT[tkey][0]
    parts = []
    for subject, grade in CELLS:
        c = p[(p.subject == subject) & (p.grade == grade)].set_index("state")
        y0 = 2000 if subject == "mathematics" else 1998
        dy = (c[c.year == 2003][outcome] - c[c.year == y0][outcome]) / c[c.year == 2003].sd2019
        D = c[c.year == 2019][col] - c[c.year == 2003][col]
        parts.append(pd.DataFrame({"dy": dy, col: D, "cell": f"{subject[:4]}{grade}"}).dropna().reset_index())
    d = pd.concat(parts)
    res = ols(d, "dy", [col], fe=["cell"], cluster="state")
    record(rows, res, col, test="naep", spec="placebo_pre", treatment=tkey, outcome=outcome, cell="pooled",
           units="SD", years="pre->2003 on 2003->2019 share change",
           note="pre-period score change (math 2000->2003, reading 1998->2003) on the later share change")


def shares_summary(p):
    out = []
    first = p[(p.cell == "math8")]
    for tkey, (col, label) in TREAT.items():
        for y0, y1 in [(2003, 2019), (2007, 2019), (2019, 2024)]:
            a = first[first.year == y0].set_index("state")[col]
            b = first[first.year == y1].set_index("state")[col]
            d = (b - a).dropna()
            if len(d) == 0:
                continue
            out.append({"treatment": tkey, "label": label, "from": y0, "to": y1, "n_states": len(d),
                        "mean_level_from": fmt(a.loc[d.index].mean(), 2), "mean_level_to": fmt(b.loc[d.index].mean(), 2),
                        "mean_change": fmt(d.mean(), 2), "sd_change": fmt(d.std(ddof=1), 2),
                        "p10_change": fmt(d.quantile(0.1), 2), "p90_change": fmt(d.quantile(0.9), 2),
                        "min_change": f"{d.min():.2f} ({d.idxmin()})", "max_change": f"{d.max():.2f} ({d.idxmax()})"})
    return out


def write(path, rows, fields):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    p = build()
    p["ccd_w"] = p.ccd_total
    rows, ev = [], []
    for tkey in TREAT:
        yrs = MAIN_YEARS if tkey in ("hisp", "el") else [y for y in MAIN_YEARS if y >= (2007 if tkey == "imm" else 2005)]
        for outcome in OUTCOMES:
            twfe(rows, p, tkey, outcome, yrs, "twfe")
        for outcome in ["white", "nonel", "white_nonel"]:
            twfe(rows, p, tkey, outcome, yrs, "twfe_region_year", extra_fe=["region_cell_year"],
                 note="adds Census-region-by-cell-by-year FE")
            twfe(rows, p, tkey, outcome, yrs, "twfe_weighted", weight="ccd_w", note="weighted by CCD enrollment")
            twfe(rows, p, tkey, outcome, yrs, "twfe_no_dc", note="excludes DC")
            if tkey in ("hisp", "el"):
                twfe(rows, p, tkey, outcome, yrs, "twfe_state_trends", trend=True,
                     note="adds state-by-cell linear trends")
            twfe(rows, p, tkey, outcome, ALL_YEARS if tkey in ("hisp", "el") else [y for y in ALL_YEARS if y >= yrs[0]],
                 "twfe_with_2022_2024", note="pandemic waves included")
            first_diff(rows, p, tkey, outcome, yrs)
            lead_test(rows, p, tkey, outcome) if tkey in ("hisp", "el") else None
            long_diff(rows, p, tkey, outcome, yrs[0], 2019, "long_diff")
            long_diff(rows, p, tkey, outcome, 2019, 2024, "long_diff_pandemic",
                      note="2019->2024 score change on the 2019->2024 share change")
        # white students with composition controls (school-lunch eligibility; grade 8 parental college)
        twfe(rows, p, tkey, "white", yrs, "twfe_composition", controls=["white_nslp"],
             note="controls: % of white pupils eligible for school lunch")
        if tkey in ("hisp", "el"):
            for outcome in ["white", "nonel", "white_nonel", "all"]:
                event_study(ev, p, tkey, outcome)
                pre_placebo(rows, p, tkey, outcome)
    # the no-DC spec needs DC removed: rerun those rows on the filtered panel
    rows = [r for r in rows if r["spec"] != "twfe_no_dc"]
    q = p[p.state != "DC"]
    for tkey in TREAT:
        yrs = MAIN_YEARS if tkey in ("hisp", "el") else [y for y in MAIN_YEARS if y >= (2007 if tkey == "imm" else 2005)]
        for outcome in ["white", "nonel", "white_nonel"]:
            twfe(rows, q, tkey, outcome, yrs, "twfe_no_dc", note="excludes DC")
    OUT.mkdir(exist_ok=True)
    key = lambda r: (r["treatment"], r["outcome"], r["spec"], r["cell"])
    write(OUT / "naep_estimates.csv", sorted(rows, key=key), FIELDS)
    write(OUT / "naep_eventstudy.csv", sorted(ev, key=lambda r: (r["treatment"], r["outcome"], r["cell"], r["wave"])),
          ["treatment", "outcome", "cell", "wave", "delta_per10_points", "se", "ci95_lo", "ci95_hi", "p",
           "n_states_wave", "n_obs"])
    write(OUT / "shares_summary.csv", shares_summary(p),
          ["treatment", "label", "from", "to", "n_states", "mean_level_from", "mean_level_to", "mean_change",
           "sd_change", "p10_change", "p90_change", "min_change", "max_change"])
    print(f"estimates={len(rows)} eventstudy={len(ev)}")


if __name__ == "__main__":
    main()

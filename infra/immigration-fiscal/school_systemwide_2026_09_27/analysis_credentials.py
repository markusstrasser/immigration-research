"""Test 5: credential inflation. Did graduation rates rise relative to the same cohort's NAEP grade-8
scores four years earlier more where the English-learner, Hispanic or immigrant share grew? Did states
with faster share growth drop their exit exams?

Graduation: state ACGR (cohorts 2011–2022; subgroups from 2013) and AFGR (1991–2013; white from the
CCD tables), from credentials/derived/ (NCES Digest tables 219.46, 219.35, 219.40/41 and the CCD AFGR
table). The cohort graduating in spring c sat NAEP grade 8 in spring c-4.
Model: rate(s,c) = state FE + cohort FE + b * share(s) + d * NAEP8(s,c-4) + e, SEs clustered by state.
b > 0 means graduation rose more than the cohort's measured achievement where the share rose.

Exit exams: the states requiring one in NCES Digest Table 234.30, 2013 edition (EPE Research Center,
August 2013), against the 2022 edition (ECS, February 2019), both parsed with code in credentials/.

Writes derived/credential_estimates.csv and derived/exit_exam_states.csv. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/analysis_credentials.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analysis_naep import FIELDS, record, write  # noqa: E402
from panel import build  # noqa: E402
from stats_util import ols  # noqa: E402

CRED = HERE / "credentials" / "derived"
OUT = HERE / "derived"


def naep8(p):
    """Grade-8 NAEP of each cohort: mean of math and reading, in 2019 national SDs, by group."""
    q = p[(p.grade == 8) & (p.year >= 2003)].copy()  # both subjects in every wave from 2003
    out = []
    for grp, col in (("all", "all"), ("white", "white"), ("hispanic", "hisp")):
        q["z"] = q[col] / q.sd2019
        m = q.groupby(["state", "year"]).z.mean().rename("naep8_z").reset_index()
        m["group"] = grp
        out.append(m)
    n = pd.concat(out)
    n["cohort"] = n.year + 4
    return n.drop(columns="year")


def shares(p):
    s = pd.read_csv(HERE / "derived" / "state_shares.csv")
    hs = s[["state", "fall_year", "hisp_share"]].copy()
    hs["cohort"] = hs.fall_year + 1  # the senior year's fall
    imm = s[["state", "fall_year", "imm_origin_share_617"]].rename(columns={"fall_year": "cohort"})
    el = p[p.grade == 8].groupby(["state", "year"]).el_identified_pct_all.mean().rename("el8").reset_index()
    el["cohort"] = el.year + 4  # the cohort's own EL share at grade 8
    return hs.drop(columns="fall_year"), imm, el.drop(columns="year")


def grad():
    a = pd.read_csv(CRED / "acgr_state.csv")
    a = a[a.rate_flag.isna() & a.rate.notna()][["state", "cohort_end_year", "subgroup", "rate"]]
    a = a.rename(columns={"cohort_end_year": "cohort"})
    a["measure"] = "acgr"
    f = pd.read_csv(CRED / "afgr_state.csv")
    f = f[(f.sex == "total") & f.rate_flag.isna() & f.rate.notna()][["state", "school_year_end", "subgroup", "rate"]]
    f = f.rename(columns={"school_year_end": "cohort"})
    f["measure"] = "afgr"
    g = pd.concat([a, f])
    g["group"] = g.subgroup.map({"all": "all", "white": "white", "hispanic": "hispanic"})
    return g.dropna(subset=["group"])


def exit_exams(p):
    """Among the states requiring an exit exam in the 2013 Digest snapshot, did those that no longer
    required one in the 2019 snapshot see faster share growth? Linear probability of dropping on each
    share measure, HC1 SEs, and a permutation p that shuffles the dropped label over the 2013 states."""
    snap = pd.read_csv(CRED / "exit_exam_digest_snapshots.csv")
    had = sorted(snap[(snap.snapshot_year == 2013) & (snap.exit_exam_required == "Yes")].state)
    kept = set(snap[(snap.snapshot_year == 2019) & (snap.exit_exam_required == "Yes")].state)
    d = pd.DataFrame({"state": had})
    d["dropped"] = (~d.state.isin(kept)).astype(float)
    s = pd.read_csv(HERE / "derived" / "state_shares.csv").set_index(["state", "fall_year"])
    el = p.groupby(["state", "year"]).el_identified_pct_all.mean()  # mean over the four NAEP cells
    get = lambda ser, st, yr: ser.get((st, yr), np.nan)
    d["hisp_2012"] = [get(s.hisp_share, st, 2012) for st in d.state]
    d["hisp_chg_2002_2012"] = [get(s.hisp_share, st, 2012) - get(s.hisp_share, st, 2002) for st in d.state]
    d["hisp_chg_2012_2018"] = [get(s.hisp_share, st, 2018) - get(s.hisp_share, st, 2012) for st in d.state]
    d["el_2013"] = [get(el, st, 2013) for st in d.state]
    d["el_chg_2003_2013"] = [get(el, st, 2013) - get(el, st, 2003) for st in d.state]
    d["imm_2013"] = [get(s.imm_origin_share_617, st, 2013) for st in d.state]
    d["imm_chg_2007_2013"] = [get(s.imm_origin_share_617, st, 2013) - get(s.imm_origin_share_617, st, 2007)
                              for st in d.state]
    rng = np.random.default_rng(20260928)
    rows = []
    for col in ("hisp_2012", "hisp_chg_2002_2012", "hisp_chg_2012_2018", "el_2013", "el_chg_2003_2013",
                "imm_2013", "imm_chg_2007_2013"):
        dd = d.dropna(subset=[col]).reset_index(drop=True)
        res = ols(dd, "dropped", [col])
        draws = np.array([ols(dd.assign(dropped=rng.permutation(dd.dropped.to_numpy())), "dropped", [col])[col]["coef"]
                          for _ in range(2000)])
        base = res[col]["coef"]
        record(rows, res, col, test="exit_exam", spec="lpm_hc1", treatment=col, outcome="dropped_exit_exam",
               cell="state", units="probability of dropping (0-1)", years="2013 snapshot -> 2019 snapshot",
               note=(f"{int(dd.dropped.sum())} of {len(dd)} dropped; mean {col}: dropped "
                     f"{dd[dd.dropped == 1][col].mean():.2f}, kept {dd[dd.dropped == 0][col].mean():.2f}; "
                     f"permutation p {(np.sum(np.abs(draws) >= abs(base) - 1e-15) + 1) / 2001:.3f}"))
    return rows, d


def main():
    p = build()
    n8 = naep8(p)
    hs, imm, el = shares(p)
    g = grad().merge(n8, on=["state", "cohort", "group"], how="inner")
    g = g.merge(hs, on=["state", "cohort"], how="left").merge(imm, on=["state", "cohort"], how="left")
    g = g.merge(el, on=["state", "cohort"], how="left")
    rows = []
    tre = {"hisp": "hisp_share", "el": "el8", "imm": "imm_origin_share_617"}
    for measure, cohorts, label in (("acgr", range(2011, 2020), "ACGR cohorts 2011-2019"),
                                    ("acgr", range(2011, 2023), "ACGR cohorts 2011-2022 (pandemic cohorts included)"),
                                    ("afgr", range(2003, 2014), "AFGR cohorts 2007-2013")):
        for group in ("all", "white"):
            d = g[(g.measure == measure) & (g.group == group) & g.cohort.isin(cohorts)]
            if d.cohort.nunique() < 3:
                continue
            for tkey, col in tre.items():
                dd = d.dropna(subset=[col, "naep8_z", "rate"])
                if dd.cohort.nunique() < 3:
                    continue
                spec = f"{measure}_{min(cohorts)}_{max(cohorts)}"
                res = ols(dd, "rate", [col, "naep8_z"], fe=["state", "cohort"], cluster="state")
                record(rows, res, col, test="credential", spec=spec, treatment=tkey, outcome=f"{group}_grad_rate",
                       cell="state", units="grad-rate points", years=f"{dd.cohort.min()}-{dd.cohort.max()}",
                       note=f"{label}; controls for the cohort's grade-8 NAEP")
                r0 = ols(dd, "rate", [col], fe=["state", "cohort"], cluster="state")
                record(rows, r0, col, test="credential", spec=spec + "_no_naep_control", treatment=tkey,
                       outcome=f"{group}_grad_rate", cell="state", units="grad-rate points",
                       years=f"{dd.cohort.min()}-{dd.cohort.max()}", note=label)
                # pre-trend check: the share of the next usable cohort (c+2), current share held
                nxt = dd[["state", "cohort", col]].assign(cohort=dd.cohort - 2).rename(columns={col: "lead"})
                dl = dd.merge(nxt, on=["state", "cohort"], how="inner")
                if dl.cohort.nunique() >= 3:
                    rl = ols(dl, "rate", [col, "lead", "naep8_z"], fe=["state", "cohort"], cluster="state")
                    record(rows, rl, "lead", test="credential", spec=spec + "_lead", treatment=tkey,
                           outcome=f"{group}_grad_rate", cell="state", units="grad-rate points",
                           years=f"{dl.cohort.min()}-{dl.cohort.max()}",
                           note="next usable cohort's share (c+2), current share and grade-8 NAEP held")
                # NAEP-graduation link itself (per 1 SD of grade-8 NAEP), a check that the control bites
                rows.append({"test": "credential", "spec": spec + "_naep8_slope", "treatment": tkey,
                             "outcome": f"{group}_grad_rate", "cell": "state", "units": "grad-rate points per 1 SD",
                             "beta_per10": f"{res['naep8_z']['coef']:.4f}", "se": f"{res['naep8_z']['se']:.4f}",
                             "ci95_lo": "", "ci95_hi": "", "p": f"{res['naep8_z']['p']:.4f}", "mde80": "",
                             "n_obs": res["naep8_z"]["n"], "n_states": res["naep8_z"]["clusters"],
                             "years": f"{dd.cohort.min()}-{dd.cohort.max()}",
                             "note": "coefficient on the cohort's grade-8 NAEP (SD), not per 10 points"})
    ex_rows, ex_states = exit_exams(p)
    rows += ex_rows
    write(OUT / "credential_estimates.csv", sorted(rows, key=lambda r: (r["outcome"], r["treatment"], r["spec"])),
          FIELDS)
    ex_states.round(4).to_csv(OUT / "exit_exam_states.csv", index=False, lineterminator="\n")
    print(f"estimates={len(rows)}; exit-exam states={len(ex_states)}, dropped={int(ex_states.dropped.sum())}")


if __name__ == "__main__":
    main()

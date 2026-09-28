"""Is women's pay less tied to measured skill? NLSY97, G2 Hispanic and G3+ non-Hispanic white, by sex.

Reads this lane's selected fields (`extract.py`, ignored `_cache/`) and the hash-pinned parent-linkage
generation assignment. The person-year construction, worker definition, education and AFQT cells,
Rao-Wu bootstrap and gap decomposition are copied from `career_trajectories_2026_09_29/analyze.py`
(unchanged); the positive control asserts that this pull reproduces that lane's gaps exactly.
Writes to `derived/`:

  positive_control.csv  this lane's gaps at 25-27 and 35-40 beside the career lane's gaps.csv
  main_job.csv          main-job coverage and the class-of-worker carry-forward check against 2023's roster
  slopes.csv            Task 1: log hourly pay on AFQT percentile (per 10 points), by sex, group, sector
  sector_shares.csv     Task 2: class of worker and credential-pay sector shares of worker-years at 35-40
  sector_gaps.csv       Task 3: hourly-pay gap to G3+ white of the same sex, by sector and adjustment arm
  place_gaps.csv        Task 3c: regression gap with education x AFQT cells, then adding region and CBSA status
  selection.csv         Task 4: median log hourly-pay gaps with non-workers imputed
  partner_shares.csv    Task 5: marital/cohabitation status and partner-earnings shares of worker-years at 35-40
  partner_gaps.csv      Task 5: hourly-pay gap against white references restricted by partnership status
  partner_controls.csv  Task 5: regression gap with education x AFQT cells plus marital and partner-earnings controls
  partner_cells.csv     Task 5b: gap reweighted within marital-status (or partner-earnings) cells, pooled over cells
  test_scores.csv       Task 6: gaps with the reference reweighted to education x math-only (AR+MK) or verbal-only
                        (WK+PC) score terciles instead of AFQT terciles; mean score percentiles by group

Math and verbal scores rebuild the NLS AFQT recipe on subsets of the CAT-ASVAB ability estimates: each subtest's
theta is turned into a weighted percentile within three-month birth cohorts, AR + MK (or WK + PC) are summed and
re-percentiled the same way. NLS used custom ASVAB weights; this uses the 1997 base weight, and a rebuilt full AFQT
(MK + AR + 2 x verbal) is compared with the published percentile as a check. Only respondents with a published
AFQT get a subtest score, so the missing-score cell is unchanged.

Main job: CV_MAINJOB_FLG, the roster loop of the current or most recent employer as of the interview
(codebook). Pay is the career lane's annual earnings over annual hours for the calendar year before that
interview, so the job and the pay year overlap but are not the same period.
Class of worker (YEMP-58500) is asked only of employers not continuing from the last interview; for a
continuing employer the latest earlier answer for the same employer UID (YEMP_UID) is carried forward.
Self-employment comes from the roster flag YEMP_SELFEMP.
Partnership: CV_MARSTAT at the interview (never married / married / separated / divorced / widowed, each
cohabiting or not). Partner earnings are the spouse/partner wage and salary income for the same calendar year
as the respondent's pay (YINC-2400/2600; the YINC-2700 bracket midpoint where only a bracket was given; $300,000
for the open top bracket), asked of respondents married or living with a partner that year (YINC-2350).
Credential-pay sector: 2002 Census industry 7860-7890 (education), 7970-8290 (health care), 8370-8470
(social assistance), 9370-9590 (public administration), 9670-9890 (military), or a government or
armed-forces class of worker in any industry.
"""
import csv
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
FAMILY = ROOT / "infra/immigration-fiscal/new_datasets_2026_09_17/derived/nlsy_family/family_analysis_rows.csv"
FAMILY_SHA = "8372ae35fe32bd97d8a17ca40d11f6c9b158cb32f1499c7e2f5fb5df13e837a6"
CAREER_GAPS = ROOT / "infra/immigration-fiscal/career_trajectories_2026_09_29/derived/gaps.csv"
OUT = LANE / "derived"
ROUNDS = list(range(1998, 2012)) + list(range(2013, 2024, 2))
JOB_ROUNDS = list(range(2013, 2024, 2))
COW_ROUNDS = [1997] + ROUNDS
ENTRY, LATE = (25, 27), (35, 40)
REF, G2 = "G3+ NH white", "G2 Hispanic"
TARGETS = ["G2 Hispanic", "G3+ Hispanic", "G1 Hispanic"]
SEXES = {1: "men", 2: "women"}
MIN_HOURS, PAY_RANGE = 100, (2.0, 500.0)
B, SEED, SMALL = 300, 20260929, 100
EDU = {0: "no degree", 1: "GED", 2: "high school", 3: "associate", 4: "bachelor+", 5: "bachelor+",
       6: "bachelor+", 7: "bachelor+"}
STATS = ["total", "employment", "conditional", "weeks", "hours_per_week", "hourly_pay", "bridge",
         "log_earnings_workers"]
IND = [("education", 7860, 7890), ("health care", 7970, 8290), ("social assistance", 8370, 8470),
       ("public administration", 9370, 9590), ("military", 9670, 9890)]
COW = {1: "government", 2: "private for-profit", 3: "non-profit", 4: "private for-profit", 5: "government"}
MARSTAT = {1: "cohabiting", 2: "never married, not cohabiting", 3: "married, spouse present",
           4: "previously married or spouse absent, not cohabiting", 5: "cohabiting",
           6: "previously married or spouse absent, not cohabiting", 7: "cohabiting",
           8: "previously married or spouse absent, not cohabiting", 9: "cohabiting",
           10: "previously married or spouse absent, not cohabiting"}
SP_BRACKET = {1: 2500.0, 2: 7500.0, 3: 17500.0, 4: 37500.0, 5: 75000.0, 6: 175000.0, 7: 300000.0}
LOW = -10.0  # imputed log pay below any worker's (the pay floor is log 2 = 0.69)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.file_digest(fh, "sha256").hexdigest()


def write(name, rows, cols):
    with open(OUT / name, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([f"{r[c]:.6g}" if isinstance(r[c], (float, np.floating)) else r[c] for c in cols])


def se(v):
    return float(np.std(v[1:], ddof=1))


# ---- Career-lane construction (copied from career_trajectories_2026_09_29/analyze.py) -------------------
assert sha(FAMILY) == FAMILY_SHA, "[BLOCKED] parent-linkage rows changed; review before use"
d = pd.read_parquet(LANE / "_cache/nlsy_selected.parquet")
fam = pd.read_csv(FAMILY, usecols=["R0000100", "linked_coarse"]).rename(columns={"R0000100": "pubid"})
d = d.merge(fam, on="pubid", how="left", validate="one_to_one")
assert d.linked_coarse.notna().all() and len(d) == 8984
his, white = d.key_hispanic.eq(1), d.key_hispanic.eq(0) & d.key_race.eq(1)
gen = d.linked_coarse.str[:2]
d["group"] = np.select(
    [his & gen.eq("G2"), his & gen.eq("G3"), his & gen.eq("G1"), white & gen.eq("G3"), his & gen.eq("Ge")],
    ["G2 Hispanic", "G3+ Hispanic", "G1 Hispanic", REF, "Hispanic, generation unresolved"], "other")
deg = pd.Series(np.nan, index=d.index)
for y in range(1998, 2012):
    v = d[f"degree_{y}"]
    deg = deg.mask(v.ge(0) & (y <= d.birth_year + 25), v)
d["edu25"] = deg.map(EDU).fillna("unknown")
afqt = d.afqt_pct.where(d.afqt_pct.ge(0))
q1, q2 = afqt.quantile([1 / 3, 2 / 3])
d["afqt3"] = np.select([afqt.isna(), afqt.le(q1), afqt.le(q2)], ["missing", "T1", "T2"], "T3")
d["edu_afqt"] = d.edu25 + "|" + d.afqt3
d["afqt10"] = afqt / 10000.0  # percentile (3 implied decimals) in units of 10 points


def theta(t):
    pos, neg = d[f"theta_{t}_pos"], d[f"theta_{t}_neg"]
    assert not (pos.ge(0) & neg.ge(0)).any(), t
    return pd.Series(np.where(pos.ge(0), pos / 1000.0, np.where(neg.ge(0), -neg / 1000.0, np.nan)), index=d.index)


def cohort_pct(v):
    """Weighted percent of the birth-quarter cohort scoring strictly below (1997 base weight)."""
    out = pd.Series(np.nan, index=d.index)
    ok = v.notna() & afqt.notna()
    q = d.birth_year * 4 + (d.birth_month - 1) // 3
    for _, idx in v[ok].groupby(q[ok]).groups.items():
        x, w = v[idx].to_numpy(), d.weight_1997[idx].to_numpy(float)
        o = np.argsort(x, kind="stable")
        below = np.concatenate([[0.0], np.cumsum(w[o])])[np.searchsorted(x[o], x, side="left")]
        out[idx] = 100.0 * below / w.sum()
    return out


sub = {t: cohort_pct(theta(t)) for t in ("ar", "mk", "wk", "pc")}
verbal_raw = cohort_pct(sub["wk"] + sub["pc"])
scores = {"math": cohort_pct(sub["ar"] + sub["mk"]), "verbal": verbal_raw,
          "afqt_rebuilt": cohort_pct(sub["mk"] + sub["ar"] + 2 * verbal_raw)}
for name in ("math", "verbal"):
    v = scores[name]
    t1, t2 = v.quantile([1 / 3, 2 / 3])
    d[f"{name}3"] = np.select([v.isna(), v.le(t1), v.le(t2)], ["missing", "T1", "T2"], "T3")
    d[f"edu_{name}"] = d.edu25 + "|" + d[f"{name}3"]
d["w0"] = d.weight_1997 / 100.0
per = d.set_index("pubid")

parts = []
for Y in ROUNDS:
    t = Y - 1
    wa, wg, ba, bu = (d[f"{k}_{Y}"] for k in ("wage_any", "wage", "bus_any", "bus"))
    interviewed = d[f"weight_{Y}"].gt(0)
    wage = np.where(wa.eq(0), 0.0, np.where(wa.eq(1) & wg.ge(0), wg, np.nan))
    bus = np.where(ba.eq(0) | (interviewed & ba.eq(-4)), 0.0,
                   np.where(ba.eq(1) & ~bu.between(-5, -1), bu, np.nan))
    parts.append(pd.DataFrame(dict(
        pubid=d.pubid, year=t, round=Y, age=t - d.birth_year, interviewed=interviewed,
        wage=wage, bus=bus, weeks=d[f"weeks_{t}"].where(d[f"weeks_{t}"].ge(0)),
        hours=d[f"hours_{t}"].where(d[f"hours_{t}"].ge(0)), w_round=d[f"weight_{Y}"] / 100.0,
        degree_now=d[f"degree_{Y}"].map(EDU).fillna("unknown"))))
py = pd.concat(parts, ignore_index=True)
py = py[py.interviewed & py.age.between(20, 42)].copy()
py["earn"] = (py.wage + py.bus).clip(lower=0)
py["pay"] = py.earn / py.hours.where(py.hours.gt(0))
py = py.join(per[["sex", "group", "w0"]], on="pubid")
py["valid"] = py.earn.notna() & py.weeks.notna() & py.hours.notna()
py["worker"] = (py.valid & py.earn.gt(0) & py.hours.ge(MIN_HOURS) & py.weeks.gt(0)
                & py.pay.between(*PAY_RANGE))
py["lpay"] = np.log(py.pay.where(py.worker))

rng = np.random.default_rng(SEED)
strata = np.sort(per.vstrat.unique())
assert all(set(per.vpsu[per.vstrat.eq(s)]) == {1, 2} for s in strata)
pick = rng.integers(1, 3, size=(len(strata), B))
sidx = np.searchsorted(strata, per.vstrat.to_numpy())
R = pd.DataFrame(np.hstack([np.ones((len(per), 1)), 2.0 * (per.vpsu.to_numpy()[:, None] == pick[sidx])]),
                 index=per.index)


def person_sums(x, wcol):
    w, e, wk, hr, pay = (x[c].to_numpy(float) for c in (wcol, "earn", "weeks", "hours", "pay"))
    dec = (e > 0) & (hr >= MIN_HOURS) & (wk > 0) & (pay >= PAY_RANGE[0]) & (pay <= PAY_RANGE[1])
    lg = lambda a: np.log(np.where(dec, a, 1.0))
    m = pd.DataFrame({"W": w, "E": w * e, "P": w * (e > 0), "ANY": w * (wk > 0), "WK": w * wk, "HR": w * hr,
                      "WD": w * dec, "LE": w * lg(e), "LW": w * lg(wk), "LH": w * lg(hr / np.where(wk > 0, wk, 1)),
                      "LP": w * lg(pay), "N": 1.0, "ND": dec.astype(float)})
    return m.groupby(x.pubid.to_numpy()).sum()


def totals(ps, ids):
    a = ps.loc[ids]
    r = R.loc[a.index].to_numpy()
    return {k: a[k].to_numpy() @ r for k in a.columns}


def reweighted(ps, ref_ids, tgt_ids, cells):
    """Reference sums reweighted so its weight share in each cell matches the target group's."""
    cr, ct = cells.loc[ref_ids], cells.loc[tgt_ids]
    wt, wr = totals(ps, tgt_ids)["W"], totals(ps, ref_ids)["W"]
    out, lost = None, 0.0
    for c in sorted(set(ct) | set(cr)):
        st = totals(ps, ct.index[ct.eq(c)])["W"] / wt if ct.eq(c).any() else np.zeros(B + 1)
        if not cr.eq(c).any():
            lost += st[0]
            continue
        tr = totals(ps, cr.index[cr.eq(c)])
        sr = tr["W"] / wr
        phi = np.divide(st, sr, out=np.zeros_like(st), where=sr > 0)
        part = {k: phi * v for k, v in tr.items()}
        out = part if out is None else {k: out[k] + part[k] for k in out}
    return out, lost


def derive(g, r):
    s = {"total": np.log(g["E"] / g["W"]) - np.log(r["E"] / r["W"]),
         "employment": np.log(g["P"] / g["W"]) - np.log(r["P"] / r["W"])}
    s["conditional"] = s["total"] - s["employment"]
    for k, name in [("LW", "weeks"), ("LH", "hours_per_week"), ("LP", "hourly_pay"), ("LE", "log_earnings_workers")]:
        s[name] = g[k] / g["WD"] - r[k] / r["WD"]
    s["bridge"] = s["conditional"] - s["log_earnings_workers"]
    return s


def window(x, label, wcol, arms, targets=TARGETS, stats=STATS, keep=None):
    gaps = []
    for sx, sname in SEXES.items():
        xs = x[x.sex.eq(sx)]
        ps = person_sums(xs, wcol)
        grp = per.group.loc[ps.index]
        ref_ids = ps.index[grp.eq(REF)]
        tr = totals(ps, ref_ids)
        for g in targets:
            ids = ps.index[grp.eq(g)]
            tg = totals(ps, ids)
            for arm in arms:
                ref, lost = (tr, 0.0) if arm == "raw" else reweighted(ps, ref_ids, ids, per[arm])
                s = derive(tg, ref)
                if keep is not None:
                    keep[(label, sname, g, arm)] = s
                for k in stats:
                    gaps.append(dict(window=label, weight=wcol, arm=arm, sex=sname, group=g, n_persons=len(ids),
                                     n_person_years=int(tg["N"][0]), n_worker_years=int(tg["ND"][0]),
                                     n_ref_persons=len(ref_ids), n_ref_worker_years=int(tr["ND"][0]),
                                     small_cell=len(ids) < SMALL, unsupported_share=lost, stat=k,
                                     estimate=s[k][0], se=se(s[k])))
    return gaps


# ---- Positive control -------------------------------------------------------------------------------------
rows = py[py.valid & py.group.isin([REF, *TARGETS])].copy()
mine = []
for lo, hi in (ENTRY, LATE):
    mine += window(rows[rows.age.between(lo, hi)], f"age {lo}-{hi}", "w_round", ["raw", "edu25", "edu_afqt"])
lane = pd.read_csv(CAREER_GAPS, dtype=str)
key = ["window", "weight", "arm", "sex", "group", "stat"]
fmt = lambda v: f"{v:.6g}"
pc = []
for r in mine:
    m = lane
    for k in key:
        m = m[m[k].eq(r[k])]
    assert len(m) == 1, r
    pc.append(dict(**{k: r[k] for k in key}, n_persons=r["n_persons"], estimate=r["estimate"], se=r["se"],
                   career_estimate=m.estimate.iloc[0], career_se=m.se.iloc[0],
                   identical=fmt(r["estimate"]) == m.estimate.iloc[0] and fmt(r["se"]) == m.se.iloc[0]))
assert all(p["identical"] for p in pc), "[BLOCKED] positive control: career-lane gaps not reproduced"
write("positive_control.csv", [p for p in pc if p["group"] == G2], list(pc[0]))
print("positive control: reproduced", len(pc), "career-lane gap cells exactly")

# ---- Main job, class of worker, sector --------------------------------------------------------------------
cols = set(d.columns)


def loop_value(stem, Y, loop):
    """Value of a per-employer field at each respondent's given roster loop (NaN where absent)."""
    out = np.full(len(d), np.nan)
    for k in range(1, 20):
        c = f"{stem}_{Y}_{k:02d}"
        if c in cols:
            m = loop.eq(k).to_numpy()
            out[m] = d.loc[m, c].to_numpy(float)
    return out


# Every class-of-worker answer, keyed by respondent, employer UID and round.
answers = []
for Y in COW_ROUNDS:
    for k in range(1, 20):
        u, c = f"uid_{Y}_{k:02d}", f"cow_asked_{Y}_{k:02d}"
        if u in cols and c in cols:
            a = d[["pubid", u, c]].set_axis(["pubid", "uid", "cow"], axis=1)
            answers.append(a[a.uid.gt(0) & a.cow.between(1, 5)].assign(round=Y))
answers = pd.concat(answers, ignore_index=True)

jobs, job_cov = [], []
for Y in JOB_ROUNDS:
    loop = d[f"mainjob_{Y}"].where(d[f"mainjob_{Y}"].ge(1))
    j = pd.DataFrame({"pubid": d.pubid, "round": Y, "loop": loop, **{
        s: loop_value(s, Y, loop) for s in ("uid", "selfemp", "jobtype", "ind", "occ", "dli", "cow_asked",
                                            "cow_roster")},
        "region": d[f"region_{Y}"], "msa": d[f"msa_{Y}"]})
    j = j[j.loop.notna()]
    # Latest class-of-worker answer for the same employer in this or an earlier round.
    a = answers[answers["round"].le(Y)].sort_values("round").drop_duplicates(["pubid", "uid"], keep="last")
    j = j.merge(a.rename(columns={"cow": "cow_carried", "round": "cow_round"}), on=["pubid", "uid"], how="left")
    j["cow"] = np.where(j.cow_asked.between(1, 5), j.cow_asked, j.cow_carried)
    jobs.append(j)
jobs = pd.concat(jobs, ignore_index=True)
jobs["self_employed"] = jobs.selfemp.eq(1)
jobs["cls"] = np.where(jobs.self_employed, "self-employed", jobs.cow.map(COW).fillna("unknown"))
ind_group = pd.Series("other industry", index=jobs.index).where(jobs.ind.gt(0), "industry unknown")
for name, lo, hi in IND:
    ind_group = ind_group.mask(jobs.ind.between(lo, hi), name)
jobs["ind_group"] = ind_group
jobs["credential"] = jobs.ind_group.isin([n for n, _, _ in IND]) | jobs.cls.eq("government")
jobs["sector"] = np.select([jobs.credential, jobs.ind_group.eq("industry unknown")],
                           ["credential-pay", "unknown"], "other")

# Check the carry-forward against 2023's roster class of worker (filled for every employer that round).
j23 = jobs[jobs["round"].eq(2023) & ~jobs.self_employed]
both = j23.cow.between(1, 5) & j23.cow_roster.between(1, 5)
cont = both & j23.dli.eq(1)
for label, m in [("2023 employee main jobs, class known both ways", both),
                 ("  of which continuing from the last interview (carried forward)", cont)]:
    job_cov.append(dict(round=2023, measure=label, n=int(m.sum()),
                        agree=int((m & j23.cow.eq(j23.cow_roster)).sum())))
for Y in JOB_ROUNDS:
    jy = jobs[jobs["round"].eq(Y)]
    emp = jy[~jy.self_employed]
    for label, n, k in [("main jobs; industry coded", len(jy), jy.ind.gt(0).sum()),
                        ("main jobs; self-employed", len(jy), jy.self_employed.sum()),
                        ("employee main jobs; class of worker known", len(emp), emp.cow.between(1, 5).sum()),
                        ("employee main jobs continuing from last interview; class known", emp.dli.eq(1).sum(),
                         (emp.dli.eq(1) & emp.cow.between(1, 5)).sum())]:
        job_cov.append(dict(round=Y, measure=label, n=int(n), agree=int(k)))
write("main_job.csv", job_cov, ["round", "measure", "n", "agree"])
print(pd.DataFrame(job_cov).to_string())

py = py.merge(jobs[["pubid", "round", "cls", "ind_group", "sector", "region", "msa", "ind", "occ"]],
              on=["pubid", "round"], how="left")
py["sector"] = py.sector.fillna("no main job")
py["cls"] = py.cls.fillna("no main job")
py["ind_group"] = py.ind_group.fillna("no main job")
py["place"] = (py.region.where(py.region.between(1, 4)).fillna(0).astype(int).astype(str) + "|"
               + py.msa.where(py.msa.between(1, 4)).fillna(0).astype(int).astype(str))
partner = []
for Y in JOB_ROUNDS:
    spw = np.where(d[f"sp_wage_any_{Y}"].eq(0), 0.0,
                   np.where(d[f"sp_wage_{Y}"].ge(0), d[f"sp_wage_{Y}"], d[f"sp_wage_bracket_{Y}"].map(SP_BRACKET)))
    partner.append(pd.DataFrame({"pubid": d.pubid, "round": Y, "marstat": d[f"marstat_{Y}"].map(MARSTAT),
                                 "sp_any": d[f"sp_any_{Y}"],
                                 "sp_earn": np.where(d[f"sp_any_{Y}"].eq(1), spw, np.nan)}))
py = py.merge(pd.concat(partner, ignore_index=True), on=["pubid", "round"], how="left")
py["marstat"] = py.marstat.fillna("unknown")
py["partnered"] = py.marstat.isin(["cohabiting", "married, spouse present"])
late = py[py.age.between(*LATE)].copy()
lw = late[late.worker].copy()


# ---- Task 1: pay-AFQT slope -------------------------------------------------------------------------------
def wls(x, design, wcol="w_round"):
    """Coefficients (B+1 replicates) of a weighted regression of log pay on the design columns."""
    X = design.to_numpy(float)
    y = x.lpay.to_numpy()
    w = x[wcol].to_numpy()[:, None] * R.loc[x.pubid].to_numpy()
    out = np.empty((B + 1, X.shape[1]))
    for b in range(B + 1):
        Xw = X * w[:, b][:, None]
        out[b] = np.linalg.lstsq(Xw.T @ X, Xw.T @ y, rcond=None)[0]
    return out


def dummies(s, prefix):
    return pd.get_dummies(s, prefix=prefix, drop_first=True, dtype=float)


slopes, slope_draws = [], {}
lw_afqt = lw[lw.pubid.map(per.afqt10).notna()].copy()
lw_afqt["afqt10"] = lw_afqt.pubid.map(per.afqt10).to_numpy()
samples = {"G3+ NH white": lw_afqt.group.eq(REF), "G2 Hispanic": lw_afqt.group.eq(G2),
           "pooled (all respondents)": pd.Series(True, index=lw_afqt.index)}
for gname, gm in samples.items():
    for sector in ("all", "credential-pay", "other"):
        for sx, sname in SEXES.items():
            x = lw_afqt[gm & lw_afqt.sex.eq(sx) & (lw_afqt.sector.eq(sector) if sector != "all" else True)]
            for spec in ("AFQT", "AFQT + degree"):
                X = pd.DataFrame({"const": 1.0, "afqt10": x.afqt10}, index=x.index)
                if spec != "AFQT":
                    X = X.join(dummies(x.degree_now, "deg"))
                beta = wls(x, X)[:, 1]
                slope_draws[(gname, sector, sname, spec)] = beta
                slopes.append(dict(group=gname, sector=sector, sex=sname, spec=spec, n_persons=x.pubid.nunique(),
                                   n_worker_years=len(x), slope_per_10_afqt=beta[0], se=se(beta)))
        for spec in ("AFQT", "AFQT + degree"):
            diff = slope_draws[(gname, sector, "women", spec)] - slope_draws[(gname, sector, "men", spec)]
            slopes.append(dict(group=gname, sector=sector, sex="women minus men", spec=spec, n_persons=0,
                               n_worker_years=0, slope_per_10_afqt=diff[0], se=se(diff)))
    for sname in SEXES.values():
        for spec in ("AFQT", "AFQT + degree"):
            diff = (slope_draws[(gname, "credential-pay", sname, spec)] - slope_draws[(gname, "other", sname, spec)])
            slopes.append(dict(group=gname, sector="credential-pay minus other", sex=sname, spec=spec, n_persons=0,
                               n_worker_years=0, slope_per_10_afqt=diff[0], se=se(diff)))
write("slopes.csv", slopes, list(slopes[0]))

# ---- Task 2: sector shares of worker-years at 35-40 --------------------------------------------------------
shares = []
for sx, sname in SEXES.items():
    for g in (REF, G2):
        x = lw[lw.sex.eq(sx) & lw.group.eq(g)]
        w = x.w_round.to_numpy()[:, None] * R.loc[x.pubid].to_numpy()
        for var in ("sector", "cls", "ind_group"):
            for level in sorted(lw[var].unique()):
                m = x[var].eq(level).to_numpy(float)
                all_share = (m @ w) / w.sum(0)
                known = x.sector.isin(["credential-pay", "other"]).to_numpy(float)
                known_share = (m * known) @ w / (known @ w)
                shares.append(dict(sex=sname, group=g, variable=var, level=level, n_persons=x.pubid.nunique(),
                                   n_worker_years=len(x), n_in_level=int(m.sum()), share=all_share[0],
                                   se=se(all_share), share_of_known_sector=known_share[0],
                                   se_known=se(known_share)))
write("sector_shares.csv", shares, list(shares[0]))

# ---- Task 3: where the premium sits -------------------------------------------------------------------------
sector_gaps, draws = [], {}
subsets = {"all workers": lw.index, "credential-pay sector": lw.index[lw.sector.eq("credential-pay")],
           "other sectors": lw.index[lw.sector.eq("other")],
           "other sectors, employees": lw.index[lw.sector.eq("other") & lw.cls.ne("self-employed")],
           "government employer": lw.index[lw.cls.eq("government")],
           "credential industries, private or non-profit": lw.index[
               lw.sector.eq("credential-pay") & lw.cls.isin(["private for-profit", "non-profit"])]}
for label, idx in subsets.items():
    g_ = window(lw.loc[idx], label, "w_round", ["raw", "edu25", "edu_afqt", "edu_math"], targets=[G2],
                stats=["hourly_pay"], keep=draws)
    sector_gaps += g_
for sname in SEXES.values():
    for arm in ("raw", "edu25", "edu_afqt", "edu_math"):
        for a, b_ in [("credential-pay sector", "other sectors"), ("credential-pay sector", "other sectors, employees")]:
            diff = draws[(a, sname, G2, arm)]["hourly_pay"] - draws[(b_, sname, G2, arm)]["hourly_pay"]
            sector_gaps.append(dict(window=f"{a} minus {b_}", weight="w_round", arm=arm, sex=sname, group=G2,
                                    n_persons=0, n_person_years=0, n_worker_years=0, n_ref_persons=0,
                                    n_ref_worker_years=0, small_cell=False, unsupported_share=0.0,
                                    stat="hourly_pay", estimate=diff[0], se=se(diff)))
for label in subsets:
    for arm in ("raw", "edu25", "edu_afqt", "edu_math"):
        diff = draws[(label, "women", G2, arm)]["hourly_pay"] - draws[(label, "men", G2, arm)]["hourly_pay"]
        sector_gaps.append(dict(window=label, weight="w_round", arm=arm, sex="women minus men", group=G2,
                                n_persons=0, n_person_years=0, n_worker_years=0, n_ref_persons=0,
                                n_ref_worker_years=0, small_cell=False, unsupported_share=0.0,
                                stat="hourly_pay", estimate=diff[0], se=se(diff)))
write("sector_gaps.csv", sector_gaps, list(sector_gaps[0]))

place = []
for sx, sname in SEXES.items():
    x = lw[lw.sex.eq(sx) & lw.group.isin([REF, G2])].copy()
    x["edu_afqt"] = x.pubid.map(per.edu_afqt).to_numpy()
    base = pd.DataFrame({"const": 1.0, "g2": x.group.eq(G2).astype(float)}, index=x.index).join(
        dummies(x.edu_afqt, "cell"))
    specs = {"education x AFQT cells": base, "+ region": base.join(dummies(x.region.fillna(0), "reg")),
             "+ region x CBSA status": base.join(dummies(x.place, "place")),
             "+ region x CBSA status + credential-pay sector": base.join(dummies(x.place, "place")).assign(
                 cred=x.sector.eq("credential-pay").astype(float), unk=x.sector.isin(["unknown", "no main job"])
                 .astype(float))}
    for spec, X in specs.items():
        beta = wls(x, X)[:, 1]
        place.append(dict(sex=sname, spec=spec, n_g2_persons=x[x.group.eq(G2)].pubid.nunique(),
                          n_ref_persons=x[x.group.eq(REF)].pubid.nunique(), n_worker_years=len(x),
                          gap=beta[0], se=se(beta)))
    for g in (REF, G2):
        xg = x[x.group.eq(g)]
        for reg in (1, 2, 3, 4):
            place.append(dict(sex=sname, spec=f"{g}: share of worker-years in region {reg}", n_g2_persons=0,
                              n_ref_persons=0, n_worker_years=len(xg),
                              gap=float(np.average(xg.region.eq(reg), weights=xg.w_round)), se=np.nan))
write("place_gaps.csv", place, list(place[0]))


# ---- Task 4: selection (median gaps with non-workers imputed) ---------------------------------------------
def wmedian(v, w):
    o = np.argsort(v, kind="stable")
    c = np.cumsum(w[o])
    return v[o][np.searchsorted(c, 0.5 * c[-1])]


pv = late[late.valid & late.group.isin([REF, G2])]
person = pd.DataFrame({"lpay": pv.groupby("pubid").lpay.mean(), "w": pv.groupby("pubid").w_round.mean()})
person = person.join(per[["sex", "group", "edu_afqt", "degree_last"]])
near = py[py.worker & (py.age.between(31, 34) | py.age.between(41, 42))].groupby("pubid").lpay.mean()
person["near"] = near.reindex(person.index)
low_deg = person.degree_last.between(0, 2)  # no degree, GED or high school diploma at last interview
nonworker = person.lpay.isna()
rules = {
    "workers only": person.lpay,
    "non-workers below the median (bound)": person.lpay.fillna(LOW),
    "Neal-2004-style: nearest-year pay; else below median without post-secondary degree; else dropped":
        person.lpay.fillna(person.near).fillna(pd.Series(LOW, index=person.index).where(low_deg)),
}
selection = []
for sx, sname in SEXES.items():
    for rule, val in rules.items():
        p = person[person.sex.eq(sx)].assign(v=val).dropna(subset=["v"])
        wr = p.w.to_numpy()[:, None] * R.loc[p.index].to_numpy()
        tg, rf = p.group.eq(G2).to_numpy(), p.group.eq(REF).to_numpy()
        # Equal-AFQT arm: reference reweighted to the G2 Hispanic education x AFQT cell shares.
        cells = p.edu_afqt.to_numpy()
        phi = np.zeros_like(wr)
        for c in np.unique(cells[tg]):
            ct, cr = tg & (cells == c), rf & (cells == c)
            if cr.any():
                den = wr[cr].sum(0) / wr[rf].sum(0)
                phi[cr] = np.divide(wr[ct].sum(0) / wr[tg].sum(0), den, out=np.zeros_like(den), where=den > 0)
        v = p.v.to_numpy()
        nw = nonworker.loc[p.index].to_numpy(float)
        for arm in ("raw", "edu_afqt"):
            est = np.array([wmedian(v[tg], wr[tg, b]) - wmedian(v[rf], wr[rf, b] * (phi[rf, b] if arm != "raw" else 1))
                            for b in range(B + 1)])
            selection.append(dict(sex=sname, rule=rule, arm=arm, n_g2=int(tg.sum()), n_ref=int(rf.sum()),
                                  n_g2_imputed_low=int((tg & (v == LOW)).sum()),
                                  n_ref_imputed_low=int((rf & (v == LOW)).sum()),
                                  share_g2_nonworker_in_sample=float(np.average(nw[tg], weights=wr[tg, 0])),
                                  share_ref_nonworker_in_sample=float(np.average(nw[rf], weights=wr[rf, 0] * (phi[rf, 0] if arm != "raw" else 1))),
                                  median_gap=est[0], se=se(est),
                                  replicates_median_at_imputed=int(sum(e < LOW / 2 or e > -LOW / 2 for e in est))))
write("selection.csv", selection, list(selection[0]))
print(pd.DataFrame(selection)[["sex", "rule", "arm", "n_g2", "n_ref", "median_gap", "se"]].to_string())


# ---- Task 5: the reference group (partnership and partner earnings) ---------------------------------------
# Partner-earnings terciles among partnered worker-years at 35-40, per sex (all respondents, round weights).
lw["sp_cat"] = np.where(lw.sp_any.eq(0), "no spouse or partner", "partner earnings unknown")
cuts = {}
for sx in SEXES:
    pw = lw[lw.sex.eq(sx) & lw.sp_any.eq(1) & lw.sp_earn.notna()]
    o = np.argsort(pw.sp_earn.to_numpy(), kind="stable")
    cw = np.cumsum(pw.w_round.to_numpy()[o]) / pw.w_round.sum()
    cuts[sx] = [pw.sp_earn.to_numpy()[o][np.searchsorted(cw, q)] for q in (1 / 3, 2 / 3)]
    m = lw.sex.eq(sx) & lw.sp_any.eq(1) & lw.sp_earn.notna()
    lw.loc[m, "sp_cat"] = np.select([lw.sp_earn[m].le(cuts[sx][0]), lw.sp_earn[m].le(cuts[sx][1])],
                                    ["partner earnings tercile 1", "partner earnings tercile 2"],
                                    "partner earnings tercile 3")
print("partner-earnings tercile cut points:", {SEXES[k]: v for k, v in cuts.items()})

pshares = []
for sx, sname in SEXES.items():
    for g in (REF, G2):
        x = lw[lw.sex.eq(sx) & lw.group.eq(g)]
        w = x.w_round.to_numpy()[:, None] * R.loc[x.pubid].to_numpy()
        for var in ("marstat", "sp_cat"):
            for level in sorted(lw[var].unique()):
                sh = (x[var].eq(level).to_numpy(float) @ w) / w.sum(0)
                pshares.append(dict(sex=sname, group=g, variable=var, level=level, n_persons=x.pubid.nunique(),
                                    n_worker_years=len(x), n_in_level=int(x[var].eq(level).sum()),
                                    share=sh[0], se=se(sh), tercile_cuts=f"{cuts[sx][0]:.0f}|{cuts[sx][1]:.0f}"))
write("partner_shares.csv", pshares, list(pshares[0]))

top = lw.sp_cat.eq("partner earnings tercile 3")
never = lw.marstat.eq("never married, not cohabiting")
alone = ~lw.partnered & lw.marstat.ne("unknown")
is_ref, is_g2 = lw.group.eq(REF), lw.group.eq(G2)
refsets = {
    "all G3+ white (baseline)": (is_ref, is_g2),
    "(a1) white reference never married and not cohabiting; all G2": (is_ref & never, is_g2),
    "(a2) white reference not married or cohabiting; all G2": (is_ref & alone, is_g2),
    "(a3) both not married or cohabiting": (is_ref & alone, is_g2 & alone),
    "(a4) both married or cohabiting": (is_ref & lw.partnered, is_g2 & lw.partnered),
    "(a5) white reference with a top-tercile-earning partner; all G2": (is_ref & top, is_g2),
}
pgaps = []
for label, (mr, mg) in refsets.items():
    pgaps += window(lw[mr | mg], label, "w_round", ["raw", "edu25", "edu_afqt"], targets=[G2],
                    stats=["hourly_pay"])
write("partner_gaps.csv", pgaps, list(pgaps[0]))

pctl = []
for sx, sname in SEXES.items():
    x = lw[lw.sex.eq(sx) & lw.group.isin([REF, G2])].copy()
    x["edu_afqt"] = x.pubid.map(per.edu_afqt).to_numpy()
    base = pd.DataFrame({"const": 1.0, "g2": x.group.eq(G2).astype(float)}, index=x.index).join(
        dummies(x.edu_afqt, "cell"))
    mar = dummies(x.marstat.where(x.marstat.ne("never married, not cohabiting"), "0 never married"), "mar")
    spc = dummies(x.sp_cat.where(x.sp_cat.ne("no spouse or partner"), "0 none"), "sp")
    specs = {"education x AFQT cells": base, "+ marital/cohabitation status": base.join(mar),
             "+ marital status + partner-earnings tercile": base.join(mar).join(spc),
             "+ marital status + partner earnings + region x CBSA": base.join(mar).join(spc).join(
                 dummies(x.place, "place"))}
    for spec, X in specs.items():
        beta = wls(x, X)
        for j, name in enumerate(X.columns):
            if name == "g2" or name.startswith(("mar_", "sp_")):
                pctl.append(dict(sex=sname, spec=spec, term=name,
                                 n_g2_persons=x[x.group.eq(G2)].pubid.nunique(),
                                 n_ref_persons=x[x.group.eq(REF)].pubid.nunique(), n_worker_years=len(x),
                                 coef=beta[0, j], se=se(beta[:, j])))
write("partner_controls.csv", pctl, list(pctl[0]))
print(pd.DataFrame(pctl).query("term == 'g2'").to_string())


# Task 5b: reweighting within marital-status (or partner-earnings) cells, pooled with G2 worker-year cell shares.
pcells = []
for cellvar in ("marstat", "sp_cat"):
    levels = [c for c in sorted(lw[cellvar].unique()) if c not in ("unknown", "partner earnings unknown")]
    both = lw[lw.group.isin([REF, G2])]
    cdraws = {}
    for c in levels:
        cdraws[c] = {}
        window(both[both[cellvar].eq(c)], c, "w_round", ["raw", "edu_afqt", "edu_math"], targets=[G2],
               stats=["hourly_pay"], keep=cdraws[c])
    for sx, sname in SEXES.items():
        x = both[both.sex.eq(sx)]
        g2 = x[x.group.eq(G2) & x[cellvar].isin(levels)]
        wg = g2.w_round.to_numpy()[:, None] * R.loc[g2.pubid].to_numpy()
        share = {c: (g2[cellvar].eq(c).to_numpy(float) @ wg) / wg.sum(0) for c in levels}
        for arm in ("raw", "edu_afqt", "edu_math"):
            for c in levels:
                gd = cdraws[c][(c, sname, G2, arm)]["hourly_pay"]
                pcells.append(dict(cells=cellvar, sex=sname, arm=arm, cell=c,
                                   n_g2_persons=x[x.group.eq(G2) & x[cellvar].eq(c)].pubid.nunique(),
                                   n_ref_persons=x[x.group.eq(REF) & x[cellvar].eq(c)].pubid.nunique(),
                                   g2_share=share[c][0], estimate=gd[0], se=se(gd)))
            pooled = sum(share[c] * cdraws[c][(c, sname, G2, arm)]["hourly_pay"] for c in levels)
            pcells.append(dict(cells=cellvar, sex=sname, arm=arm, cell="pooled over cells",
                               n_g2_persons=g2.pubid.nunique(), n_ref_persons=x[x.group.eq(REF)].pubid.nunique(),
                               g2_share=1.0, estimate=pooled[0], se=se(pooled)))
write("partner_cells.csv", pcells, list(pcells[0]))

# ---- Task 6: math-only and verbal-only test scores ---------------------------------------------------------
tests = []
x = rows[rows.age.between(*LATE)]
for r in window(x, "age 35-40", "w_round", ["edu_afqt", "edu_math", "edu_verbal"], targets=[G2],
                stats=["total", "employment", "hourly_pay"]):
    tests.append(dict(kind="gap", sex=r["sex"], group=r["group"], arm=r["arm"], stat=r["stat"],
                      n_persons=r["n_persons"], n_ref_persons=r["n_ref_persons"], estimate=r["estimate"],
                      se=r["se"]))
ok = afqt.notna()
tests.append(dict(kind="check", sex="all", group="all with AFQT", arm="afqt_rebuilt", stat="corr with published",
                  n_persons=int(ok.sum()), n_ref_persons=0,
                  estimate=float(np.corrcoef(scores["afqt_rebuilt"][ok], afqt[ok])[0, 1]), se=np.nan))
for sx, sname in SEXES.items():
    for g in (REF, G2):
        m = d.sex.eq(sx) & d.group.eq(g) & ok
        wr = d.weight_1997[m].to_numpy(float)[:, None] * R.loc[d.pubid[m]].to_numpy()
        for name, v in [("afqt", afqt / 1000.0), ("math", scores["math"]), ("verbal", scores["verbal"])]:
            mean = v[m].to_numpy() @ wr / wr.sum(0)
            tests.append(dict(kind="mean percentile", sex=sname, group=g, arm=name, stat="mean",
                              n_persons=int(m.sum()), n_ref_persons=0, estimate=mean[0], se=se(mean)))
write("test_scores.csv", tests, list(tests[0]))
print(pd.DataFrame(tests).to_string())

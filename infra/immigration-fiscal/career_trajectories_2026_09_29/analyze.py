"""NLSY97 career trajectories: G2, G3+ and G1 Hispanic against G3+ non-Hispanic white, by sex.

Reads the lane's selected fields (`extract.py`, ignored `_cache/`) and the parent-linkage generation
assignment (`new_datasets_2026_09_17/nlsy/analyze_family.py`, hash-pinned). Writes to `derived/`:

  coverage.csv       person-years by group: valid, bracket-only earnings, other missing
  person_counts.csv  respondents by group and sex; entry, late and balanced panels; Mexican self-ID share
  levels.csv         weighted outcome levels by age window, group and sex
  gaps.csv           gap to G3+ white of the same sex, decomposed, by window, weight and adjustment arm
  growth.csv         within-person change 25-27 -> 35-40 (two-period person fixed effects), base and IPW
  attrition.csv      entry-window outcomes of people seen and not seen at 35-40

Earnings are wage/salary income plus business/farm income for the calendar year before each interview,
including verified zeros (answered no to both), floored at zero; bracket-only answers are missing.
Weeks and hours come from the event-history created variables for the same calendar year.
Gap decomposition (exact): log(mean earnings incl. zeros) gap = log employment-share gap
  + [mean log weeks + mean log hours per week + mean log hourly pay] gaps among workers with at least
  100 hours and hourly pay in [$2, $500] + a bridge term (dispersion and the worker-sample restriction).
Standard errors: Rao-Wu rescaling bootstrap over the NLSY97 variance PSUs within strata (VSTRAT/VPSU,
two PSUs per stratum), 300 replicates, fixed seed. Education reweighting shares are re-estimated in each
replicate; the IPW attrition model is fitted once and held fixed across replicates.
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
OUT = LANE / "derived"
ROUNDS = list(range(1998, 2012)) + list(range(2013, 2024, 2))
BINS = [(20, 24), (25, 27), (28, 30), (31, 33), (34, 36), (37, 39), (40, 42)]
ENTRY, LATE = (25, 27), (35, 40)
REF = "G3+ NH white"
TARGETS = ["G2 Hispanic", "G3+ Hispanic", "G1 Hispanic"]
SEXES = {1: "men", 2: "women"}
MIN_HOURS, PAY_RANGE = 100, (2.0, 500.0)
B, SEED, SMALL = 300, 20260929, 100
EDU = {0: "no degree", 1: "GED", 2: "high school", 3: "associate", 4: "bachelor+", 5: "bachelor+",
       6: "bachelor+", 7: "bachelor+"}
STATS = ["total", "employment", "conditional", "weeks", "hours_per_week", "hourly_pay", "bridge",
         "log_earnings_workers"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.file_digest(fh, "sha256").hexdigest()


def write(name, rows, cols):
    with open(OUT / name, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([f"{r[c]:.6g}" if isinstance(r[c], (float, np.floating)) else r[c] for c in cols])


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
# Highest degree reported by the latest round held no later than the calendar year the respondent turned 25.
deg = pd.Series(np.nan, index=d.index)
for y in range(1998, 2012):
    v = d[f"degree_{y}"]
    deg = deg.mask(v.ge(0) & (y <= d.birth_year + 25), v)
d["edu25"] = deg.map(EDU).fillna("unknown")
afqt = d.afqt_pct.where(d.afqt_pct.ge(0))
q1, q2 = afqt.quantile([1 / 3, 2 / 3])
d["afqt3"] = np.select([afqt.isna(), afqt.le(q1), afqt.le(q2)], ["missing", "T1", "T2"], "T3")
d["edu_afqt"] = d.edu25 + "|" + d.afqt3
d["mexican_any"] = d[["origin_1", "origin_2", "origin_3"]].isin([21, 22, 23]).any(axis=1)
d["origin_answered"] = d.origin_1.gt(0)
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
        pubid=d.pubid, year=t, age=t - d.birth_year, interviewed=interviewed,
        bracket_only=(wa.eq(1) & wg.isin([-1, -2])) | (ba.eq(1) & bu.isin([-1, -2])),
        wage=wage, bus=bus, weeks=d[f"weeks_{t}"].where(d[f"weeks_{t}"].ge(0)),
        hours=d[f"hours_{t}"].where(d[f"hours_{t}"].ge(0)), w_round=d[f"weight_{Y}"] / 100.0)))
py = pd.concat(parts, ignore_index=True)
py = py[py.interviewed & py.age.between(20, 42)].copy()
py["earn"] = (py.wage + py.bus).clip(lower=0)
py["pay"] = py.earn / py.hours.where(py.hours.gt(0))
py = py.join(per[["sex", "group", "w0"]], on="pubid")
py["valid"] = py.earn.notna() & py.weeks.notna() & py.hours.notna()

coverage = []
for (sx, g), x in py[py.group.isin([REF, *TARGETS])].groupby(["sex", "group"]):
    coverage.append(dict(sex=SEXES[sx], group=g, person_years_interviewed=len(x), valid=int(x.valid.sum()),
                         bracket_only_earnings=int(x.bracket_only.sum()),
                         other_missing_earnings=int((x.earn.isna() & ~x.bracket_only).sum()),
                         missing_weeks_or_hours=int((x.earn.notna() & ~x.valid).sum())))
write("coverage.csv", coverage, list(coverage[0]))
rows = py[py.valid & py.group.isin([REF, *TARGETS])].copy()

# Rao-Wu bootstrap: each replicate keeps one of the two PSUs in every stratum at double weight.
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


def level(t):
    return dict(mean_earnings=t["E"][0] / t["W"][0], share_positive_earnings=t["P"][0] / t["W"][0],
                share_any_weeks=t["ANY"][0] / t["W"][0], mean_weeks=t["WK"][0] / t["W"][0],
                mean_hours=t["HR"][0] / t["W"][0], mean_log_hourly_pay=t["LP"][0] / t["WD"][0])


def window(x, label, wcol, arms):
    gaps, levels = [], []
    for sx, sname in SEXES.items():
        xs = x[x.sex.eq(sx)]
        ps = person_sums(xs, wcol)
        grp = per.group.loc[ps.index]
        ref_ids = ps.index[grp.eq(REF)]
        tr = totals(ps, ref_ids)
        levels.append(dict(window=label, weight=wcol, sex=sname, group=REF, n_persons=len(ref_ids),
                           n_person_years=int(tr["N"][0]), **level(tr)))
        for g in TARGETS:
            ids = ps.index[grp.eq(g)]
            tg = totals(ps, ids)
            levels.append(dict(window=label, weight=wcol, sex=sname, group=g, n_persons=len(ids),
                               n_person_years=int(tg["N"][0]), **level(tg)))
            for arm in arms:
                ref, lost = (tr, 0.0) if arm == "raw" else reweighted(ps, ref_ids, ids, per[arm])
                s = derive(tg, ref)
                for k in STATS:
                    gaps.append(dict(window=label, weight=wcol, arm=arm, sex=sname, group=g, n_persons=len(ids),
                                     n_person_years=int(tg["N"][0]), n_worker_years=int(tg["ND"][0]),
                                     small_cell=len(ids) < SMALL, unsupported_share=lost, stat=k,
                                     estimate=s[k][0], se=np.std(s[k][1:], ddof=1)))
    return gaps, levels


gaps, levels = [], []
for lo, hi in BINS:
    if (lo, hi) != ENTRY:
        g_, l_ = window(rows[rows.age.between(lo, hi)], f"age {lo}-{hi}", "w_round", ["raw"])
        gaps += g_; levels += l_
for (lo, hi) in (ENTRY, LATE):
    x = rows[rows.age.between(lo, hi)]
    for wcol in ("w_round", "w0"):
        g_, l_ = window(x, f"age {lo}-{hi}", wcol, ["raw", "edu25", "edu_afqt"] if wcol == "w_round" else ["raw"])
        gaps += g_; levels += l_
for yr, lab in [(2020, "income year 2020 (ages 36-40)"), (2022, "income year 2022 (ages 38-42)")]:
    g_, l_ = window(rows[rows.year.eq(yr)], lab, "w_round", ["raw"])
    gaps += g_; levels += l_
write("gaps.csv", gaps, list(gaps[0]))
write("levels.csv", levels, list(levels[0]))


def person_window(x, lo, hi):
    x = x[x.age.between(lo, hi)]
    pos = x[x.earn > 0]
    return pd.DataFrame({"e": x.groupby("pubid").earn.mean(), "p": (x.earn > 0).groupby(x.pubid).mean(),
                         "l": np.log(pos.earn).groupby(pos.pubid).mean()})


ent, late = person_window(rows, *ENTRY), person_window(rows, *LATE)
panel = ent.join(late, lsuffix="0", rsuffix="1", how="left")
panel["stay"] = panel.e1.notna()
panel = panel.join(per[["sex", "group", "w0", "birth_year", "edu25"]])


def logit_prob(X, y):
    beta = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ beta))
        step = np.linalg.solve(X.T @ (X * (p * (1 - p))[:, None]) + 1e-8 * np.eye(X.shape[1]), X.T @ (y - p))
        beta += step
        if np.abs(step).max() < 1e-10:
            break
    return 1 / (1 + np.exp(-X @ beta))


panel["ipw"] = np.nan
for sx in SEXES:
    m = panel.sex.eq(sx)
    z = panel[m]
    X = pd.get_dummies(z[["group", "edu25"]].assign(by=z.birth_year.astype(str)), drop_first=True, dtype=float)
    X = np.column_stack([np.ones(m.sum()), X.to_numpy(), np.log1p(z.e0), z.p0])
    panel.loc[m, "ipw"] = 1 / np.clip(logit_prob(X, z.stay.to_numpy(float)), 0.05, 1)

growth = []
for arm in ("base weight 1997", "base weight x IPW"):
    b = panel[panel.stay].copy()
    b["w"] = b.w0 * (b.ipw if arm.endswith("IPW") else 1.0)
    for sx, sname in SEXES.items():
        bs = b[b.sex.eq(sx)]
        bl = bs.l0.notna() & bs.l1.notna()
        c = pd.DataFrame({"W": bs.w, "E0": bs.w * bs.e0, "E1": bs.w * bs.e1, "P0": bs.w * bs.p0, "P1": bs.w * bs.p1,
                          "WL": bs.w * bl, "L0": bs.w * bs.l0.where(bl, 0), "L1": bs.w * bs.l1.where(bl, 0),
                          "N": 1.0, "NL": bl.astype(float)})
        sums = {g: {k: c.loc[bs.group.eq(g), k].to_numpy() @ R.loc[bs.index[bs.group.eq(g)]].to_numpy()
                    for k in c.columns} for g in [REF, *TARGETS]}
        r = sums[REF]
        for g in TARGETS:
            t = sums[g]
            s = {"earnings_gap_entry": np.log(t["E0"] / t["W"]) - np.log(r["E0"] / r["W"]),
                 "earnings_gap_late": np.log(t["E1"] / t["W"]) - np.log(r["E1"] / r["W"]),
                 "employment_gap_entry": np.log(t["P0"] / t["W"]) - np.log(r["P0"] / r["W"]),
                 "employment_gap_late": np.log(t["P1"] / t["W"]) - np.log(r["P1"] / r["W"]),
                 "log_earnings_gap_entry_workers_both": t["L0"] / t["WL"] - r["L0"] / r["WL"],
                 "log_earnings_gap_late_workers_both": t["L1"] / t["WL"] - r["L1"] / r["WL"]}
            s["earnings_growth_gap"] = s["earnings_gap_late"] - s["earnings_gap_entry"]
            s["employment_growth_gap"] = s["employment_gap_late"] - s["employment_gap_entry"]
            s["within_person_log_growth_gap"] = (s["log_earnings_gap_late_workers_both"]
                                                 - s["log_earnings_gap_entry_workers_both"])
            for k, v in s.items():
                growth.append(dict(arm=arm, sex=sname, group=g, n_persons=int(t["N"][0]),
                                   n_workers_both=int(t["NL"][0]), small_cell=t["N"][0] < SMALL, stat=k,
                                   estimate=v[0], se=np.std(v[1:], ddof=1)))
write("growth.csv", growth, list(growth[0]))

attr = []
for (sx, g), z in panel.groupby(["sex", "group"]):
    if g not in [REF, *TARGETS]:
        continue
    for stay, y in z.groupby("stay"):
        w = y.w0
        attr.append(dict(sex=SEXES[sx], group=g, seen_at_35_40=bool(stay), n_persons=len(y),
                         mean_earnings_25_27=np.average(y.e0, weights=w), employment_share_25_27=np.average(y.p0, weights=w),
                         mean_log_earnings_25_27_workers=np.average(y.l0.dropna(), weights=w[y.l0.notna()])))
write("attrition.csv", attr, list(attr[0]))

counts = []
for (sx, g), z in d.groupby(["sex", "group"]):
    if g not in [REF, *TARGETS, "Hispanic, generation unresolved"]:
        continue
    ids = z.pubid
    counts.append(dict(sex=SEXES[sx], group=g, respondents_1997=len(z),
                       with_entry_window=int(ids.isin(ent.index).sum()), with_late_window=int(ids.isin(late.index).sum()),
                       balanced=int(ids.isin(panel.index[panel.stay]).sum()),
                       origin_answered=int(z.origin_answered.sum()),
                       mexican_origin_any_mention=int((z.mexican_any & z.origin_answered).sum()),
                       mexican_share_weighted=float(np.average(z.mexican_any[z.origin_answered], weights=z.w0[z.origin_answered]))
                       if z.origin_answered.any() else np.nan))
write("person_counts.csv", counts, list(counts[0]))
print(pd.DataFrame(counts).to_string())

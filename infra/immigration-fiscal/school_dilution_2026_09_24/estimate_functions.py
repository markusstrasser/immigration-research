"""How school spending by function moves with enrollment, within districts and across states.

Task 1 of the brief. Every specification below is written to derived/function_elasticities.csv,
null and inconvenient ones included. Units: real 2024 dollars (CPI-U fiscal-year means).

Sample: regular districts (F-33 SCHLEV 01, 02, 03) in the 50 states and DC with an NCES ID, at least
100 pupils (V33), positive current and instructional spending, and current spending per pupil of
$4,000-$80,000 in 2024 dollars. A district's series is split into spells wherever V33 moves by more
than 0.4 log points in a year (consolidations, splits, reporting breaks); each spell gets its own fixed
effect. One-year V33 spikes that reverse (both moves above 0.25 log points, opposite signs) are dropped.
Main window FY2000-FY2019 (CBO's 1999-2000 to 2019-20 window, pre-COVID); FY2000-FY2024 is reported
beside it.

Estimators, each unweighted and pupil-weighted, standard errors clustered by state:
  fe_log   log spending ~ log pupils | spell + state-year           (elasticity)
  fe_level spending/Nbar ~ pupils/Nbar | spell + state-year        (marginal $ per pupil; additive)
  fd       one-year change in log spending ~ change in log pupils | state-year
  fd_asym  the same with separate slopes for growth and decline
  dl3      one-year change on this and the two previous years' pupil changes; cumulative response
  ld       stacked long differences over 2000-05, 05-10, 10-15, 15-19 | state x window
  ld19     one difference, FY2000 to FY2019 | state
  state    CBO's design on F-33 state totals: yearly change in spending per pupil relative to the
           nation on the yearly change in pupils relative to the nation, state fixed effects

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow --with pyfixest \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/estimate_functions.py
"""
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FUNCS = ["current", "instruction", "pupil_support", "instr_staff", "gen_admin", "school_admin", "business", "om",
         "transport", "support_other", "other_elsec", "capital_outlay", "interest",
         "instr_support", "administration", "support_total"]
GROUPS = {"instr_support": ["pupil_support", "instr_staff"], "administration": ["gen_admin", "school_admin", "business"]}
CURRENT_PARTS = ["instruction", "pupil_support", "instr_staff", "gen_admin", "school_admin", "business", "om",
                 "transport", "support_other", "other_elsec"]
PP_BAND = (4_000.0, 80_000.0)
MIN_PUPILS = 100
SPELL_BREAK = 0.4
SPIKE = 0.25
LD_WINDOWS = [(2000, 2005), (2005, 2010), (2010, 2015), (2015, 2019)]


def load(last_year):
    d = pd.read_parquet(HERE / "_cache" / "panel.parquet")
    d["support_total"] = d["TCURSSVC"]
    for g, parts in GROUPS.items():
        d[g] = d[parts].sum(axis=1)
    d = d[d.SCHLEV.isin(["01", "02", "03"]) & d.leaid.ne("") & d.fips.le(56) & d.year.le(last_year)].copy()
    for f in FUNCS:
        d[f] = d[f] * d.defl_2024
    d = d[d.V33.ge(MIN_PUPILS) & d.current.gt(0) & d.instruction.gt(0)]
    d = d[(d.current / d.V33).between(*PP_BAND)]
    d = d.groupby(["leaid", "year"], as_index=False).first()    # duplicate NCES IDs within a year, if any
    d = d.sort_values(["leaid", "year"]).reset_index(drop=True)
    d["lnN"] = np.log(d.V33)
    prev_year = d.groupby("leaid").year.shift()
    d["dlnN"] = np.where(prev_year.eq(d.year - 1), d.lnN - d.groupby("leaid").lnN.shift(), np.nan)
    nxt = d.groupby("leaid").dlnN.shift(-1)
    spike = d.dlnN.abs().gt(SPIKE) & nxt.abs().gt(SPIKE) & (np.sign(d.dlnN) != np.sign(nxt))
    d = d[~spike].copy()
    # recompute after dropping spikes
    prev_year = d.groupby("leaid").year.shift()
    d["dlnN"] = np.where(prev_year.eq(d.year - 1), d.lnN - d.groupby("leaid").lnN.shift(), np.nan)
    brk = d.dlnN.abs().gt(SPELL_BREAK).astype(int)
    d["spell"] = d.leaid + "_" + brk.groupby(d.leaid).cumsum().astype(str)
    d.loc[d.dlnN.abs().gt(SPELL_BREAK), "dlnN"] = np.nan          # a break is not a change within a spell
    d["nbar"] = d.groupby("spell").V33.transform("mean")
    d["nyears"] = d.groupby("spell").year.transform("size")
    d = d[d.nyears.ge(3)].copy()
    d["stateyear"] = d.fips.astype(int) * 10000 + d.year
    return d, int(spike.sum())


def fit(formula, data, weights=None):
    m = pf.feols(formula, data=data, vcov={"CRV1": "fips"}, weights=weights)
    return m


def row(spec, func, weight, m, term, extra=None):
    b, se = float(m.coef()[term]), float(m.se()[term])
    r = {"spec": spec, "function": func, "weight": weight, "term": term, "beta": b, "se": se,
         "ci_low": b - 1.96 * se, "ci_high": b + 1.96 * se, "n_obs": int(m._N)}
    if extra:
        r.update(extra)
    return r


def district_specs(d, window_label):
    rows = []
    sw = d.groupby("spell").V33.transform("mean")
    d = d.assign(w_pupil=sw, lag_pupils=d.groupby("spell").V33.shift())
    for f in FUNCS:
        pos = d[d[f] > 0].copy()
        pos["ly"] = np.log(pos[f])
        zero_share = 1 - len(pos) / len(d)
        for wname, w in [("unweighted", None), ("pupils", "w_pupil")]:
            m = fit("ly ~ lnN | spell + stateyear", pos, w)
            rows.append(row(f"fe_log_{window_label}", f, wname, m, "lnN", {"zero_rows_dropped": zero_share}))
        lv = d.assign(y=d[f] / d.nbar, x=d.V33 / d.nbar)
        avg_pw = d[f].sum() / d.V33.sum()
        avg_uw = (d[f] / d.V33).mean()
        for wname, w, avg in [("unweighted", None, avg_uw), ("pupils", "w_pupil", avg_pw)]:
            m = fit("y ~ x | spell + stateyear", lv, w)
            r = row(f"fe_level_{window_label}", f, wname, m, "x", {"avg_cost_per_pupil": avg})
            r["response_ratio"] = r["beta"] / avg
            r["response_ci_low"], r["response_ci_high"] = r["ci_low"] / avg, r["ci_high"] / avg
            rows.append(r)
        # one-year differences within spells
        fd = pos.assign(dly=pos.groupby("spell").ly.diff())
        fd = fd[fd.dlnN.notna() & fd.dly.notna() & fd.groupby("spell").year.diff().eq(1)]
        fd = fd.assign(lag_pupils=fd.lag_pupils.fillna(fd.V33))
        for wname, w in [("unweighted", None), ("pupils", "lag_pupils")]:
            m = fit("dly ~ dlnN | stateyear", fd, w)
            rows.append(row(f"fd_{window_label}", f, wname, m, "dlnN"))
            a = fd.assign(up=fd.dlnN.clip(lower=0), down=fd.dlnN.clip(upper=0))
            m = fit("dly ~ up + down | stateyear", a, w)
            rows.append(row(f"fd_asym_{window_label}", f, wname, m, "up"))
            rows.append(row(f"fd_asym_{window_label}", f, wname, m, "down"))
        # distributed lag: this and two previous years
        dl = fd.copy()
        g = dl.groupby("spell")
        dl["dlnN_1"] = g.dlnN.shift(1)
        dl["dlnN_2"] = g.dlnN.shift(2)
        ok = g.year.shift(2).eq(dl.year - 2)
        dl = dl[ok & dl.dlnN_1.notna() & dl.dlnN_2.notna()]
        for wname, w in [("unweighted", None), ("pupils", "lag_pupils")]:
            m = fit("dly ~ dlnN + dlnN_1 + dlnN_2 | stateyear", dl, w)
            cum = float(m.coef()[["dlnN", "dlnN_1", "dlnN_2"]].sum())
            V = m._vcov
            names = list(m.coef().index)
            idx = [names.index(t) for t in ["dlnN", "dlnN_1", "dlnN_2"]]
            se = float(np.sqrt(np.asarray(V)[np.ix_(idx, idx)].sum()))
            rows.append({"spec": f"dl3_{window_label}", "function": f, "weight": wname, "term": "cumulative_3yr",
                         "beta": cum, "se": se, "ci_low": cum - 1.96 * se, "ci_high": cum + 1.96 * se,
                         "n_obs": int(m._N)})
    return rows


def long_differences(d, label):
    rows = []
    wide = {}
    for a, b in LD_WINDOWS:
        x = d[d.year.eq(a)].set_index("leaid")
        y = d[d.year.eq(b)].set_index("leaid")
        common = x.index.intersection(y.index)
        # same spell at both ends: no consolidation break in between
        common = common[(x.loc[common, "spell"].values == y.loc[common, "spell"].values)]
        part = pd.DataFrame({"leaid": common, "fips": x.loc[common, "fips"].values, "window": f"{a}_{b}",
                             "dlnN": np.log(y.loc[common, "V33"].values / x.loc[common, "V33"].values),
                             "w": x.loc[common, "V33"].values})
        for f in FUNCS:
            ok = (x.loc[common, f].values > 0) & (y.loc[common, f].values > 0)
            part[f"dly_{f}"] = np.where(ok, np.log(np.where(ok, y.loc[common, f].values, 1) /
                                                   np.where(ok, x.loc[common, f].values, 1)), np.nan)
        wide[(a, b)] = part
    stacked = pd.concat(wide.values(), ignore_index=True)
    stacked["state_window"] = stacked.fips.astype(int).astype(str) + "_" + stacked.window
    for f in FUNCS:
        s = stacked[stacked[f"dly_{f}"].notna()].rename(columns={f"dly_{f}": "dly"})
        for wname, w in [("unweighted", None), ("pupils", "w")]:
            m = fit("dly ~ dlnN | state_window", s, w)
            rows.append(row(f"ld_stacked_{label}", f, wname, m, "dlnN"))
    # one 19-year difference
    x = d[d.year.eq(2000)].set_index("leaid")
    y = d[d.year.eq(2019)].set_index("leaid")
    common = x.index.intersection(y.index)
    common = common[(x.loc[common, "spell"].values == y.loc[common, "spell"].values)]
    base = pd.DataFrame({"fips": x.loc[common, "fips"].values,
                         "dlnN": np.log(y.loc[common, "V33"].values / x.loc[common, "V33"].values),
                         "w": x.loc[common, "V33"].values})
    for f in FUNCS:
        ok = (x.loc[common, f].values > 0) & (y.loc[common, f].values > 0)
        s = base[ok].assign(dly=np.log(y.loc[common, f].values[ok] / x.loc[common, f].values[ok]))
        for wname, w in [("unweighted", None), ("pupils", "w")]:
            m = fit("dly ~ dlnN | fips", s, w)
            rows.append(row("ld19_2000_2019", f, wname, m, "dlnN"))
    return rows


def state_cbo(last_year):
    """CBO's design on F-33 state totals (all systems with pupils), FY2000 to last_year."""
    p = pd.read_parquet(HERE / "_cache" / "panel.parquet")
    p = p[p.fips.le(56) & p.year.le(last_year)].copy()      # every system: service agencies' spending counts
    p["support_total"] = p["TCURSSVC"]
    for g, parts in GROUPS.items():
        p[g] = p[parts].sum(axis=1)
    p["net_federal"] = p.current - p.TFEDREV.fillna(0)
    funcs = FUNCS + ["net_federal"]
    s = p.groupby(["fips", "year"])[funcs + ["V33"]].sum().reset_index().sort_values(["fips", "year"])
    nat = s.groupby("year")[funcs + ["V33"]].sum()
    lN = np.log(s.V33)
    g_n = lN - lN.groupby(s.fips).shift()
    ng_n = np.log(nat.V33).diff()
    rows = []
    for f in funcs:
        lpp = np.log(s[f].where(s[f] > 0) / s.V33)
        g_pp = lpp - lpp.groupby(s.fips).shift()
        nlpp = np.log(nat[f].where(nat[f] > 0) / nat.V33)
        t = pd.DataFrame({"fips": s.fips, "year": s.year, "y": g_pp - s.year.map(nlpp.diff()),
                          "x": g_n - s.year.map(ng_n), "w": s.V33.groupby(s.fips).shift()}).dropna()
        t["up"], t["down"] = t.x.clip(lower=0), t.x.clip(upper=0)
        # one long difference per state, FY2000 -> last year: the state-level long-run counterpart
        first, last = s[s.year.eq(2000)].set_index("fips"), s[s.year.eq(last_year)].set_index("fips")
        okf = (first[f] > 0) & (last[f] > 0)
        ld = pd.DataFrame({"dly": np.log(last[f][okf] / first[f][okf]),
                           "dlnN": np.log(last.V33[okf] / first.V33[okf]), "w": first.V33[okf]})
        for wname, w in [("unweighted", None), ("pupils", "w")]:
            m = pf.feols("dly ~ dlnN", data=ld, vcov="hetero", weights=w)
            r = row(f"state_ld_2000_{last_year}", f, wname, m, "dlnN")
            r["implied_total_response"] = r["beta"]
            rows.append(r)
        for wname, w in [("unweighted", None), ("pupils", "w")]:
            m = pf.feols("y ~ x | fips", data=t, vcov={"CRV1": "fips"}, weights=w)
            r = row(f"state_cbo_{last_year}", f, wname, m, "x")
            r["implied_total_response"] = 1 + r["beta"]
            rows.append(r)
            m = pf.feols("y ~ up + down | fips", data=t, vcov={"CRV1": "fips"}, weights=w)
            for term in ("up", "down"):
                r = row(f"state_cbo_asym_{last_year}", f, wname, m, term)
                r["implied_total_response"] = 1 + r["beta"]
                rows.append(r)
    return rows


def shares(d):
    """Pupil-weighted share of current spending by function in the sample."""
    tot = d.current.sum()
    return {f: float(d[f].sum() / tot) for f in FUNCS}


def main():
    OUT.mkdir(exist_ok=True)
    rows, meta = [], {}
    for last, label in [(2019, "fy2000_2019"), (2024, "fy2000_2024")]:
        d, spikes = load(last)
        meta[label] = {"rows": len(d), "districts": int(d.leaid.nunique()), "spells": int(d.spell.nunique()),
                       "spike_rows_dropped": spikes, "pupils_mean_per_year": float(d.groupby("year").V33.sum().mean()),
                       "shares_of_current": shares(d)}
        rows += district_specs(d, label)
        if last == 2019:
            rows += long_differences(d, label)
        rows += state_cbo(last)
        cov = d.groupby("year").agg(districts=("leaid", "nunique"), pupils=("V33", "sum")).reset_index()
        cov.to_csv(OUT / f"sample_coverage_{label}.csv", index=False, lineterminator="\n")
        print(f"{label}: {meta[label]['rows']} rows, {meta[label]['districts']} districts", flush=True)
    r = pd.DataFrame(rows)
    r.to_csv(OUT / "function_elasticities.csv", index=False, lineterminator="\n", float_format="%.6f")
    (OUT / "function_sample.json").write_text(json.dumps(meta, indent=1) + "\n")
    show = r[r.function.isin(["current", "instruction", "instr_support", "administration", "om", "capital_outlay",
                              "interest"]) & r.weight.eq("pupils")]
    print(show[["spec", "function", "term", "beta", "se"]].to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())

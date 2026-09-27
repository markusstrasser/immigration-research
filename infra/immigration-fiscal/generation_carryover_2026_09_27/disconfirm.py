"""Is the G3 -> G4+ stall an artifact of region, age or period?

CPS 2022-2025 (both-biological-parents frame): state composition of observed G3 and G4+;
gaps against whites matched on age band x sex x state group; excluding New Mexico and Colorado
(the 1848/Hispano settlement states); Texas-only and California-only.
GSS 2000-2024: G3 vs G4+ gaps with whites matched on census region (four-region coding only);
South and West separately; by survey period and by age half.
"""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cps = _load("carry_cps", HERE / "analyze_cps.py")
gss = _load("carry_gss", HERE / "analyze_gss.py")

STATE_GROUP = {6: 1, 48: 2, 35: 3, 8: 4, 4: 5}  # CA, TX, NM, CO, AZ; 0 = elsewhere
STATE_NAME = {0: "elsewhere", 1: "CA", 2: "TX", 3: "NM", 4: "CO", 5: "AZ"}
MEAS = ["ba_plus", "ba_plus_22plus", "employed", "earnings_worker_mean", "ledger_partial_per_adult"]


def se(v):
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def cps_specs(p, nyears):
    W = p[cps.REPS].to_numpy(float) / nyears
    sg = p.GESTFIPS.map(STATE_GROUP).fillna(0).astype(int).to_numpy()
    age = p.A_AGE.to_numpy()
    sex = p.A_SEX.to_numpy()
    coarse = np.digitize(age, [25, 30, 35]) * 2 + (sex - 1)
    fine = cps.age_cells(age, sex, "cores")
    frame = p.A_AGE.ge(18).to_numpy() & p.both.to_numpy()
    specs = {
        "baseline_age_sex": (np.ones(len(p), bool), fine),
        "matched_age_sex_state": (np.ones(len(p), bool), coarse * 6 + sg),
        "excluding_NM_CO": (~np.isin(sg, [3, 4]), fine),
        "Texas_only": (sg == 2, coarse),
        "California_only": (sg == 1, coarse),
        "outside_CA_TX_NM_CO_AZ": (sg == 0, coarse),
    }
    rows, comp = [], []
    for gname in ["G3_obs", "G4plus_obs"]:
        use = frame & p[gname].to_numpy()
        tot = W[use, 0].sum()
        for k, name in STATE_NAME.items():
            comp.append(dict(source="CPS_ASEC_2022_2025", frame="cores_both adults 18+", generation=gname, state_group=name,
                             n=int((use & (sg == k)).sum()), share=float(W[use & (sg == k), 0].sum() / tot)))
    ref_all = frame & p.white3plus.to_numpy()
    for k, name in STATE_NAME.items():
        comp.append(dict(source="CPS_ASEC_2022_2025", frame="cores_both adults 18+", generation="white3plus", state_group=name,
                         n=int((ref_all & (sg == k)).sum()), share=float(W[ref_all & (sg == k), 0].sum() / W[ref_all, 0].sum())))
    for spec, (sub, cell) in specs.items():
        gaps = {}
        for m in MEAS:
            fv, fvalid, kind, unit = cps.MEASURES[m]
            x = fv(p).to_numpy(float)
            ok = frame & sub & fvalid(p).to_numpy()
            ref = ok & p.white3plus.to_numpy()
            sc = 100 if unit == "pct" else 1
            for gname in ["G3_obs", "G4plus_obs"]:
                use = ok & p[gname].to_numpy()
                if use.sum() < 10:
                    continue
                wr, unc = cps.reweight(cell[use], W[use], cell[ref], W[ref])
                g = (cps.stat(kind, x[use], W[use]) - cps.stat(kind, x[ref], wr)) * sc
                gaps[(m, gname)] = g
                rows.append(dict(source="CPS_ASEC_2022_2025", spec=spec, measure=m, generation=gname, n=int(use.sum()),
                                 gap=float(g[0]), se=se(g), ref_cells_uncovered_share=unc))
            if (m, "G3_obs") in gaps and (m, "G4plus_obs") in gaps:
                d = gaps[(m, "G4plus_obs")] - gaps[(m, "G3_obs")]
                rows.append(dict(source="CPS_ASEC_2022_2025", spec=spec, measure=m, generation="G4plus_minus_G3",
                                 n=int((ok & p.G4plus_obs.to_numpy()).sum()), gap=float(d[0]), se=se(d),
                                 ref_cells_uncovered_share=np.nan))
    return rows, comp


def gss_specs():
    d = gss.load()
    import pyreadstat
    # Row order is preserved by load(); re-read region aligned on the same filter.
    full, _ = pyreadstat.read_dta(gss.SRC, usecols=gss.COLS + ["region"], encoding="latin1")
    full = full.apply(pd.to_numeric, errors="coerce")
    full = full[full.year.ge(2000) & full.wtssps.gt(0)]
    assert len(full) == len(d)
    d["region"] = full.region.to_numpy()
    d = d[(d.grp != "") | d.G3plus_all].reset_index(drop=True)
    rng = np.random.default_rng(7)
    specs = {
        "baseline_age_sex": (np.ones(len(d), bool), d.cell.to_numpy()),
        "matched_age_sex_region": (np.ones(len(d), bool), d.cell.to_numpy() * 10 + d.region.fillna(0).astype(int).to_numpy()),
        # This release codes REGION as the four census regions only (1 NE, 2 MW, 3 South, 4 West),
        # so New Mexico/Colorado cannot be isolated in GSS; the CPS specs do that.
        "South_only": (d.region.eq(3).to_numpy(), d.cell.to_numpy()),
        "West_only": (d.region.eq(4).to_numpy(), d.cell.to_numpy()),
        "years_2000_2012": (d.year.le(2012).to_numpy(), d.cell.to_numpy()),
        "years_2014_2024": (d.year.ge(2014).to_numpy(), d.cell.to_numpy()),
        "ages_25_44": (d.age.between(25, 44).to_numpy(), d.cell.to_numpy()),
        "ages_45_64": (d.age.between(45, 64).to_numpy(), d.cell.to_numpy()),
    }
    comp = []
    x = d[d.age.between(25, 64)]
    for g in ["M_G3_generic", "M_G4plus_generic", "W"]:
        s = x[x.grp.eq(g)]
        for reg, sh in (s.groupby("region").wtssps.sum() / s.wtssps.sum()).items():
            comp.append(dict(source="GSS_2000_2024", frame="ages 25-64", generation=g, state_group=f"region_{int(reg)}",
                             n=int(s.region.eq(reg).sum()), share=float(sh)))
    rows = []
    clu = pd.factorize(d.clu)[0]
    strata = pd.factorize(d.year.astype(int).astype(str) + "_" + d.vstrat.astype("Int64").astype(str))[0]
    cl_str = pd.Series(strata).groupby(clu).first().to_numpy()
    groups = [np.flatnonzero(cl_str == s) for s in range(cl_str.max() + 1)]
    mults = []
    for _ in range(200):
        mult = np.zeros(clu.max() + 1)
        for cl in groups:
            np.add.at(mult, rng.choice(cl, size=len(cl), replace=True), 1)
        mults.append(mult[clu])
    for spec, (sub, cell) in specs.items():
        for m in ["ba_plus", "less_than_hs", "educ_years", "employed", "log_realrinc"]:
            col, sc = gss.MEASURES[m]
            ok = sub & d.age.between(25, 64).to_numpy() & d[col].notna().to_numpy() & d.sex.isin([1, 2]).to_numpy()
            ref = ok & d.grp.eq("W").to_numpy()

            def one(w):
                out = {}
                for g in ["G3_generic", "G4plus_generic"]:
                    use = ok & d.grp.eq("M_" + g).to_numpy()
                    if use.sum() < 10:
                        out[g], out[g + "_unc"] = np.nan, np.nan
                        continue
                    cg, cr = cell[use].astype(int), cell[ref].astype(int)
                    k = int(max(cg.max(), cr.max())) + 1
                    s_g = np.bincount(cg, weights=w[use], minlength=k)
                    s_r = np.bincount(cr, weights=w[ref], minlength=k)
                    f = np.divide(s_g / s_g.sum(), s_r, out=np.zeros(k), where=s_r > 0)
                    wr = w[ref] * f[cr]
                    out[g] = (np.average(d[col].to_numpy()[use], weights=w[use]) - np.average(d[col].to_numpy()[ref], weights=wr)) * sc
                    out[g + "_unc"] = float(s_g[s_r == 0].sum() / s_g.sum())
                return out
            base = one(d.wtssps.to_numpy())
            bs = []
            for mlt in mults:
                try:
                    bs.append(one(d.wtssps.to_numpy() * mlt))
                except (ZeroDivisionError, ValueError):
                    continue
            for g in ["G3_generic", "G4plus_generic"]:
                rows.append(dict(source="GSS_2000_2024", spec=spec, measure=m, generation=g,
                                 n=int((ok & d.grp.eq("M_" + g).to_numpy()).sum()), gap=float(base[g]),
                                 se=float(np.nanstd([b[g] for b in bs], ddof=1)), ref_cells_uncovered_share=base[g + "_unc"]))
            diff = [b["G4plus_generic"] - b["G3_generic"] for b in bs]
            rows.append(dict(source="GSS_2000_2024", spec=spec, measure=m, generation="G4plus_minus_G3",
                             n=int((ok & d.grp.eq("M_G4plus_generic").to_numpy()).sum()),
                             gap=float(base["G4plus_generic"] - base["G3_generic"]), se=float(np.nanstd(diff, ddof=1)),
                             ref_cells_uncovered_share=np.nan))
    return rows, comp


def write(rows, name):
    with open(HERE / "derived" / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    p, _ = cps.build([2022, 2023, 2024, 2025])
    r1, c1 = cps_specs(p, 4)
    r2, c2 = gss_specs()
    write(r1 + r2, "disconfirmation.csv")
    write(c1 + c2, "disconfirmation_composition.csv")
    pd.set_option("display.width", 250)
    print(pd.DataFrame(c1 + c2).round(3).to_string(index=False))
    print(pd.DataFrame(r1 + r2).round(2).to_string(index=False))


if __name__ == "__main__":
    main()

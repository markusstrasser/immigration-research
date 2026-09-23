#!/usr/bin/env python3
"""Institutional residence of men 18-40 in the 1980, 1990 and 2000 5% censuses (IPUMS USA extract
`census`): Mexico-born immigrants by years since arrival against US-born men, all foreign-born men
for the Butcher-Piehl replication, and US-born interstate movers against stayers.

Definitions (fixed across years):
  institutional   GQ == 3 (every institution type; the ACS series uses the same concept)
  correctional    GQTYPE == 2, identified in 1980 only (1990/2000 public files code "institution")
  US-born         BPL < 100 (50 states, DC, "Native American", "United States, ns")
  Mexico-born     BPL == 200 and CITIZEN != 1 (drops people born in Mexico to US-citizen parents)
  foreign-born    150 <= BPL < 900 and CITIZEN != 1 (Butcher and Piehl's immigrant definition)
  years in US     survey year minus YRIMMIG; 1980 and 1990 report arrival intervals, whose bins
                  line up with 0-5 / 6-10 / 11-15 (1975-80, 1970-74, 1965-69 in 1980;
                  1985-90, 1980-84, 1975-79 in 1990; single years in 2000)
  mover           US-born with BPL (state of birth) != STATEFIP (state of residence)
Standard errors: delete-a-group jackknife over 80 household groups (SERIAL mod 80).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/analyze_census.py
Out: _cache/census_cells.parquet (aggregates), derived/census_cohort_rates.csv,
     census_cohort_education.csv, census_movers.csv, census_ysm_profile_2000.csv; with extract
     `census_q` present also census_allocation.csv, census_cohort_rates_reported_only.csv,
     census_allocation_reassignment.csv, census_allocation_mexorig.csv and
     census_cohort_reassigned.csv (extract `census_inst_q`, if present, adds the citizenship
     flag of institutional records to the reassignment)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cohort_lib import R, educ3, standardized, summarize, wcols  # noqa: E402

CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
USECOLS = ["YEAR", "SERIAL", "PERNUM", "PERWT", "GQ", "GQTYPE", "STATEFIP", "AGE", "SEX", "BPL", "CITIZEN",
           "YRIMMIG", "HISPAN", "RACE", "EDUC"]
# IPUMS codes the 1980/1990 arrival intervals by their first year; verified against the data below.
INTERVAL_BINS = {
    1980: {1975: "0-5", 1970: "6-10", 1965: "11-15"},
    1990: {1987: "0-5", 1985: "0-5", 1982: "6-10", 1980: "6-10", 1975: "11-15"},
}


def load(flags: bool = False) -> pd.DataFrame:
    df = pd.read_csv(CACHE / "ipums" / "census.csv.gz", usecols=USECOLS)
    if not (df.SEX.eq(1).all() and df.AGE.between(18, 40).all()):
        raise SystemExit("[FAILED] case selection did not hold: extract has women or ages outside 18-40")
    if flags:
        q = pd.read_csv(CACHE / "ipums" / "census_q.csv.gz",
                        usecols=["YEAR", "SERIAL", "PERNUM", "QBPL", "QYRIMM"])
        df = df.join(q.set_index(["YEAR", "SERIAL", "PERNUM"]), on=["YEAR", "SERIAL", "PERNUM"])
        if df[["QBPL", "QYRIMM"]].isna().any().any():
            raise SystemExit("[FAILED] census_q does not cover every record of census (join left gaps)")
    return df


def classify(df: pd.DataFrame) -> pd.DataFrame:
    us = df.BPL < 100
    mex = (df.BPL == 200) & (df.CITIZEN != 1)
    fb = (df.BPL >= 150) & (df.BPL < 900) & (df.CITIZEN != 1)
    df["pop"] = np.select([us, mex, fb], ["us", "mex", "fb_other"], "drop")
    df = df[df["pop"] != "drop"].copy()
    nh = df.HISPAN == 0
    df["sub"] = np.select([nh & (df.RACE == 1), nh & (df.RACE == 2), df.HISPAN == 1, df.HISPAN.between(2, 4)],
                          ["nhw", "nhb", "mexorig", "hisp_other"], "other")
    df["mover"] = "na"
    inus = (df["pop"] == "us") & (df.BPL <= 56)
    df.loc[inus, "mover"] = np.where(df.loc[inus, "BPL"] == df.loc[inus, "STATEFIP"], "stayer", "mover")
    df["ysm"] = "na"
    for year, codes in INTERVAL_BINS.items():
        m = (df.YEAR == year) & (df["pop"] != "us")
        df.loc[m, "ysm"] = df.loc[m, "YRIMMIG"].map(codes).fillna("16+").to_numpy()
    m = (df.YEAR == 2000) & (df["pop"] != "us")
    ysm = 2000 - df.loc[m, "YRIMMIG"]
    df.loc[m, "ysm"] = np.select([ysm <= 5, ysm <= 10, ysm <= 15], ["0-5", "6-10", "11-15"], "16+")
    df.loc[(df["pop"] != "us") & ~df.YRIMMIG.between(1790, 2000), "ysm"] = "unknown"
    df["educ3"] = educ3(df.EDUC)
    # naturalized immigrants cannot be held in immigration detention or deported
    df["cit"] = np.where(df["pop"] == "us", "na", np.where(df.CITIZEN == 2, "nat", "non"))
    df["inst"] = (df.GQ == 3).astype(float)
    df["corr"] = (df.GQTYPE == 2).astype(float)
    df["jk"] = df.SERIAL % R
    return df


def cells(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Aggregate to keys x jackknife group, then build 81 weight columns: 0 = full sample,
    k = 1..80 = full sample minus group k-1, rescaled by 80/79."""
    df = df.assign(w=df.PERWT, wi=df.PERWT * df["inst"], wc=df.PERWT * df["corr"], n=1, n_inst=df["inst"])
    g = df.groupby(keys + ["jk"], observed=True)[["w", "wi", "wc", "n", "n_inst"]].sum()
    out = []
    for src, prefix in (("w", "w"), ("wi", "i"), ("wc", "c")):
        wide = g[src].unstack("jk", fill_value=0.0).reindex(columns=range(R), fill_value=0.0)
        full = wide.sum(axis=1)
        reps = (full.to_numpy()[:, None] - wide.to_numpy()) * R / (R - 1)
        out.append(pd.DataFrame(np.column_stack([full.to_numpy(), reps]), index=wide.index,
                                columns=wcols(prefix)))
    counts = g[["n", "n_inst"]].groupby(level=keys).sum()
    return pd.concat(out + [counts], axis=1).reset_index()


def crude(c: pd.DataFrame, num: str = "i") -> tuple[float, float]:
    w = c[wcols("w")].to_numpy().sum(axis=0)
    i = c[wcols(num)].to_numpy().sum(axis=0)
    return summarize(i / w, "jk")


def rows_for(c: pd.DataFrame) -> list[dict]:
    out = []
    refs = {"us_all": c[c["pop"] == "us"], "us_nhw": c[(c["pop"] == "us") & (c["sub"] == "nhw")],
            "us_mexorig": c[(c["pop"] == "us") & (c["sub"] == "mexorig")]}
    for year in (1980, 1990, 2000):
        cy = c[c.YEAR == year]
        mex = cy[cy["pop"] == "mex"]
        for label, grp in (("mexico_born", mex),
                           ("mexico_born_naturalized", mex[mex.cit == "nat"]),
                           ("mexico_born_noncitizen", mex[mex.cit == "non"]),
                           ("all_foreign_born", cy[cy["pop"].isin(["mex", "fb_other"])])):
            for ysm in ("0-5", "6-10", "11-15", "16+", "all"):
                t = grp if ysm == "all" else grp[grp.ysm == ysm]
                if t.empty:
                    continue
                for num in (("i", "c") if year == 1980 else ("i",)):
                    rate, se = crude(t, num)
                    row = dict(year=year, group=label, ysm=ysm,
                               outcome="institutional" if num == "i" else "correctional",
                               n=int(t.n.sum()), n_inst=int(t.n_inst.sum()), weighted=float(t.w0.sum()),
                               rate=rate, rate_se=se)
                    for rname, ref in refs.items():
                        ref_y = ref[ref.YEAR == year]
                        rr, _ = crude(ref_y, num)
                        s = standardized(t, ref_y, ["AGE"], num)
                        ratio, ratio_se = summarize(s["ratio"], "jk")
                        crude_ratio, crude_se = summarize(
                            (t[wcols(num)].to_numpy().sum(0) / t[wcols("w")].to_numpy().sum(0))
                            / (ref_y[wcols(num)].to_numpy().sum(0) / ref_y[wcols("w")].to_numpy().sum(0)), "jk")
                        row.update({f"{rname}_rate": rr, f"{rname}_expected": float(s["expected"][0]),
                                    f"ratio_age_{rname}": ratio, f"ratio_age_{rname}_se": ratio_se,
                                    f"ratio_crude_{rname}": crude_ratio, f"ratio_crude_{rname}_se": crude_se})
                    out.append(row)
    return out


def education_rows(c: pd.DataFrame) -> list[dict]:
    """Adult arrivals only (age >= 18 + upper end of the years-in-US bin, so every man arrived at 18+).
    Ratio standardized on single year of age x education against each US-born reference."""
    out = []
    upper = {"0-5": 5, "6-10": 10, "11-15": 15}
    for year in (1980, 1990, 2000):
        cy = c[c.YEAR == year]
        us = cy[cy["pop"] == "us"]
        refs = {"us_all": us, "us_nhw": us[us["sub"] == "nhw"], "us_mexorig": us[us["sub"] == "mexorig"]}
        for ysm, hi in upper.items():
            t = cy[(cy["pop"] == "mex") & (cy.ysm == ysm) & (cy.AGE >= 18 + hi)]
            for edu in ("all", "lt12", "g12", "col", "g12+"):
                te = t if edu == "all" else t[t.educ3.isin(["g12", "col"])] if edu == "g12+" else t[t.educ3 == edu]
                if te.n.sum() == 0:
                    continue
                rate, se = crude(te)
                row = dict(year=year, ysm=ysm, adult_arrival_ages=f"{18 + hi}-40", educ=edu, n=int(te.n.sum()),
                           n_inst=int(te.n_inst.sum()), rate=rate, rate_se=se)
                for rname, ref in refs.items():
                    s_age = standardized(te, ref, ["AGE"])
                    s_edu = standardized(te, ref, ["AGE", "educ3"])
                    row[f"ratio_age_{rname}"], row[f"ratio_age_{rname}_se"] = summarize(s_age["ratio"], "jk")
                    row[f"ratio_age_educ_{rname}"], row[f"ratio_age_educ_{rname}_se"] = summarize(s_edu["ratio"], "jk")
                out.append(row)
    return out


def mover_rows(c: pd.DataFrame) -> list[dict]:
    """US-born movers (outside birth state) vs stayers, by race/ethnicity; age-standardized difference
    and ratio (movers' observed rate against stayers' rates at movers' ages), and age x education."""
    out = []
    groups = {"all": None, "nhw": ["nhw"], "nhb": ["nhb"], "hispanic": ["mexorig", "hisp_other"]}
    for year in (1980, 1990, 2000):
        cy = c[(c.YEAR == year) & (c["pop"] == "us") & (c.mover != "na")]
        for g, subs in groups.items():
            cg = cy if subs is None else cy[cy["sub"].isin(subs)]
            mv, st = cg[cg.mover == "mover"], cg[cg.mover == "stayer"]
            rm, sem = crude(mv)
            rs, ses = crude(st)
            diff, diff_se = summarize(rate_vec(mv) - rate_vec(st), "jk")
            s_age = standardized(mv, st, ["AGE"])
            s_edu = standardized(mv, st, ["AGE", "educ3"])
            gap_age, gap_age_se = summarize(s_age["observed"] - s_age["expected"], "jk")
            gap_edu, gap_edu_se = summarize(s_edu["observed"] - s_edu["expected"], "jk")
            out.append(dict(year=year, source="census 5%", group=g, n_movers=int(mv.n.sum()),
                            n_stayers=int(st.n.sum()), mover_share=float(mv.w0.sum() / cg.w0.sum()),
                            movers_rate=rm, movers_rate_se=sem, stayers_rate=rs, stayers_rate_se=ses,
                            crude_gap_pp=100 * diff, crude_gap_pp_se=100 * diff_se,
                            age_std_gap_pp=100 * gap_age, age_std_gap_pp_se=100 * gap_age_se,
                            age_educ_std_gap_pp=100 * gap_edu, age_educ_std_gap_pp_se=100 * gap_edu_se,
                            ratio_age=float(s_age["ratio"][0]),
                            ratio_age_se=summarize(s_age["ratio"], "jk")[1],
                            ratio_age_educ=float(s_edu["ratio"][0]),
                            ratio_age_educ_se=summarize(s_edu["ratio"], "jk")[1]))
    return out


def rate_vec(c: pd.DataFrame, num: str = "i") -> np.ndarray:
    return c[wcols(num)].to_numpy().sum(axis=0) / c[wcols("w")].to_numpy().sum(axis=0)


def allocation(df: pd.DataFrame, df_raw: pd.DataFrame) -> pd.DataFrame:
    """IPUMS flags QBPL/QYRIMM (0 = as reported, >0 = edited or allocated). Writes allocation shares
    and the cohort table re-run on records with birthplace (and, for immigrants, arrival year) as
    reported. Dropping edited records removes institutional records disproportionately."""
    df = df.assign(bpl_alloc=df.QBPL > 0, yr_alloc=(df.QYRIMM > 0) & (df["pop"] != "us"))
    share = []
    for (year, pop, inst), t in df.groupby(["YEAR", "pop", "inst"]):
        w = t.PERWT.sum()
        share.append(dict(year=year, pop=pop, institutional=bool(inst), n=len(t),
                          bpl_allocated=float(t.PERWT[t.bpl_alloc].sum() / w),
                          arrival_year_allocated=float(t.PERWT[t.yr_alloc].sum() / w)))
    pd.DataFrame(share).to_csv(DERIVED / "census_allocation.csv", index=False, float_format="%.4g")
    kept = df[~df.bpl_alloc & ~df.yr_alloc]
    c = cells(kept, ["YEAR", "pop", "sub", "mover", "ysm", "cit", "AGE", "educ3"])
    pd.DataFrame(rows_for(c)).to_csv(DERIVED / "census_cohort_rates_reported_only.csv", index=False,
                                     float_format="%.6g")
    return reassignment(df_raw)


def reassignment(raw: pd.DataFrame) -> pd.DataFrame:
    """Sensitivity for birthplace allocation. The census resolved a missing birthplace to a US state
    or, in 1980 and 1990, to "abroad, country unknown" (BPL 900+, dropped from the main tables), and
    never to Mexico in 1980 or 1990. Variants, each within year x race/Hispanic origin x
    institutional status:
      country        abroad-unknown records are spread over foreign birthplaces in the mix of
                     reported foreign-born records (uses only what the census itself recorded);
      nativity_high  also spreads every record whose birthplace was allocated to a US state over
                     nativity groups in the mix of reported records, except 1990 institutional
                     records whose citizenship item (which offers "born in the United States") was
                     reported (extract census_inst_q; the 1980 file asks citizenship of the
                     foreign-born only and the 2000 file never flags it for the US-born);
      nativity_low   as nativity_high, but only the 1990 institutional share with both items
                     allocated is spread in 1980, 2000 and among non-institutional records.
    Spreading non-institutional records enlarges the Mexico-born denominator (conservative).
    Scaling each group's institutional count by k and its population by d moves the
    age-standardized ratio by (k_mex / d_mex) / (k_ref / d_ref), if the reassignment falls evenly
    over ages and years-in-US bins. Also writes the diagnostic behind it: the foreign-born share
    among Mexican-origin institutional men with a reported and with an allocated birthplace."""
    d = raw[["YEAR", "SERIAL", "PERNUM", "PERWT", "GQ", "BPL", "CITIZEN", "HISPAN", "RACE", "QBPL"]].copy()
    nh = d.HISPAN == 0
    d["sub"] = np.select([nh & (d.RACE == 1), nh & (d.RACE == 2), d.HISPAN == 1, d.HISPAN.between(2, 4)],
                         ["nhw", "nhb", "mexorig", "hisp_other"], "other")
    d["nat"] = np.select([d.BPL < 100, (d.BPL == 200) & (d.CITIZEN != 1),
                          (d.BPL >= 150) & (d.BPL < 900) & (d.CITIZEN != 1), d.BPL >= 900],
                         ["us", "mex", "fb_other", "fb_unknown"], "other")
    d["inst"] = d.GQ == 3
    d["unknown"] = (d.QBPL > 0) & (d.nat == "us")
    d["p_low"] = np.nan
    source = "QBPL only"
    iq = CACHE / "ipums" / "census_inst_q.csv.gz"
    if iq.exists():
        q = pd.read_csv(iq, usecols=["YEAR", "SERIAL", "PERNUM", "QCITIZEN"])
        qc = d.join(q.set_index(["YEAR", "SERIAL", "PERNUM"]), on=["YEAR", "SERIAL", "PERNUM"]).QCITIZEN
        if qc[d.inst].isna().any():
            raise SystemExit("[FAILED] census_inst_q does not cover every institutional record")
        m90 = d.inst & d.unknown & (d.YEAR == 1990)
        p1990 = d.PERWT[m90 & (qc > 0)].sum() / d.PERWT[m90].sum()
        d.loc[m90 & ~(qc > 0), "unknown"] = False
        d["p_low"] = np.where(d.inst & (d.YEAR == 1990), 1.0, p1990)
        source = f"QBPL; QCITIZEN for 1990 institutional records (both allocated: {p1990:.3f})"
    diag = []
    for year, t in d[d.inst & (d["sub"] == "mexorig")].groupby("YEAR"):
        for alloc, g in t.groupby(t.QBPL > 0):
            w = g.groupby("nat").PERWT.sum()
            diag.append(dict(year=year, birthplace="allocated" if alloc else "reported", records=len(g),
                             weighted=float(w.sum()), share_mexico=float(w.get("mex", 0) / w.sum()),
                             share_abroad_unknown=float(w.get("fb_unknown", 0) / w.sum()),
                             share_foreign=float(w.reindex(["mex", "fb_other", "fb_unknown"]).fillna(0).sum() / w.sum())))
    pd.DataFrame(diag).to_csv(DERIVED / "census_allocation_mexorig.csv", index=False, float_format="%.4g")
    variants = ["country", "nativity_high"] + (["nativity_low"] if d.p_low.notna().all() else [])
    rows = []
    for year, t in d.groupby("YEAR"):
        out = {}
        for variant in ["as_published"] + variants:
            tot = {}
            for (sub, inst), g in t.groupby(["sub", "inst"]):
                rep = g[g.QBPL == 0].groupby("nat").PERWT.sum().reindex(["us", "mex", "fb_other", "other"], fill_value=0.0)
                cur = g.groupby("nat").PERWT.sum().reindex(["us", "mex", "fb_other", "other", "fb_unknown"], fill_value=0.0)
                if variant != "as_published":
                    fb = rep[["mex", "fb_other"]]
                    cur[["mex", "fb_other"]] += cur["fb_unknown"] * (fb / fb.sum() if fb.sum() else 0.0)
                if variant.startswith("nativity"):
                    share = g.p_low if variant == "nativity_low" else 1.0
                    u = (g.PERWT * g.unknown * share).sum()
                    cur["us"] -= u
                    cur[["us", "mex", "fb_other", "other"]] += u * rep / rep.sum()
                tot[(sub, inst)] = cur
            tot = pd.DataFrame(tot).T
            tot.index.names = ["sub", "inst"]
            inst = tot.xs(True, level="inst")
            pop = tot.groupby(level="sub").sum()
            out[variant] = {"mex": (inst["mex"].sum(), pop["mex"].sum()),
                            "us_all": (inst["us"].sum(), pop["us"].sum()),
                            "us_nhw": (inst.loc["nhw", "us"], pop.loc["nhw", "us"]),
                            "us_mexorig": (inst.loc["mexorig", "us"], pop.loc["mexorig", "us"])}
        base = out["as_published"]
        for variant in variants:
            rate = {g: (out[variant][g][0] / out[variant][g][1]) / (base[g][0] / base[g][1]) for g in base}
            rows.append(dict(year=year, variant=variant, nativity_flags=source,
                             inst_unknown_nativity_weighted=float(t.PERWT[t.unknown & t.inst].sum()),
                             inst_abroad_unknown_weighted=float(t.PERWT[(t.nat == "fb_unknown") & t.inst].sum()),
                             **{f"rate_scale_{g}": float(v) for g, v in rate.items()},
                             **{f"multiplier_{g}": float(rate["mex"] / rate[g]) for g in ("us_all", "us_nhw", "us_mexorig")}))
    mult = pd.DataFrame(rows)
    mult.to_csv(DERIVED / "census_allocation_reassignment.csv", index=False, float_format="%.4g")
    return mult


def profile_2000(df: pd.DataFrame) -> pd.DataFrame:
    """Mexico-born men 18-40 in 2000 by single year since arrival (the only census with single
    years): an arrival-year spike would mark immigration custody, as it does in the ACS."""
    m = df[(df.YEAR == 2000) & (df["pop"] == "mex") & df.YRIMMIG.between(1790, 2000)].copy()
    m["ysm1"] = (2000 - m.YRIMMIG).clip(upper=16)
    c = cells(m, ["ysm1"])
    rows = []
    for y, t in c.groupby("ysm1"):
        rate, se = crude(t)
        rows.append(dict(ysm=int(y) if y < 16 else "16+", n=int(t.n.sum()), n_inst=int(t.n_inst.sum()), rate=rate, rate_se=se))
    return pd.DataFrame(rows)


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    flags = (CACHE / "ipums" / "census_q.csv.gz").exists()
    raw = load(flags=flags)
    df = classify(raw.copy())
    if flags:
        mult = allocation(df, raw)
        print("  ✓ derived/census_allocation.csv, census_cohort_rates_reported_only.csv, "
              "census_allocation_reassignment.csv")
    else:
        print("  ! census_q.csv.gz absent: allocation check skipped")
    for year in (1980, 1990):
        vals = sorted(df.loc[(df.YEAR == year) & (df["pop"] != "us"), "YRIMMIG"].unique())
        print(f"  {year} YRIMMIG codes among foreign-born: {vals}")
    print(df.groupby("YEAR").agg(n=("PERWT", "size"), w=("PERWT", "sum"), wmin=("PERWT", "min"),
                                  wmax=("PERWT", "max")).to_string())
    keys = ["YEAR", "pop", "sub", "mover", "ysm", "cit", "AGE", "educ3"]
    c = cells(df, keys)
    c.to_parquet(CACHE / "census_cells.parquet")
    rates = pd.DataFrame(rows_for(c))
    rates.to_csv(DERIVED / "census_cohort_rates.csv", index=False, float_format="%.6g")
    if flags:
        r = rates[(rates.group == "mexico_born") & (rates.outcome == "institutional")]
        r = r[["year", "ysm", "ratio_age_us_all", "ratio_age_us_nhw", "ratio_age_us_mexorig"]].merge(
            mult[["year", "variant", "multiplier_us_all", "multiplier_us_nhw", "multiplier_us_mexorig"]], on="year")
        for ref in ("us_all", "us_nhw", "us_mexorig"):
            r[f"ratio_age_{ref}_reassigned"] = r[f"ratio_age_{ref}"] * r[f"multiplier_{ref}"]
        r.to_csv(DERIVED / "census_cohort_reassigned.csv", index=False, float_format="%.4g")
    pd.DataFrame(education_rows(c)).to_csv(DERIVED / "census_cohort_education.csv", index=False,
                                           float_format="%.6g")
    pd.DataFrame(mover_rows(c)).to_csv(DERIVED / "census_movers.csv", index=False, float_format="%.6g")
    profile_2000(df).to_csv(DERIVED / "census_ysm_profile_2000.csv", index=False, float_format="%.6g")
    print("  ✓ derived/census_cohort_rates.csv, census_cohort_education.csv, census_movers.csv, "
          "census_ysm_profile_2000.csv")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Institutional residence of Mexico-born men 18-40 by years since arrival, ACS 1-year 2006-2024
(no 2020), against US-born men of the same ages.

Mexico-born side: IPUMS extract `acs_mex` (BPL 200, CITIZEN != 1), person weight plus the 80
successive-difference replicate weights (REPWTP1-80), so its SEs follow the Census Bureau formula.
US-born side: Census API tabulations by single year of age x education (`acs_reference.py`),
main weight only, held fixed across replicates. Its sampling error is ignored in the SEs; the
US-born sample is 20-60 times larger per cell, and `analyze_movers.py` sizes the omission by
reporting the US-born rate's own jackknife SE for 2019, 2023 and 2024.

Institutional = GQ 3 (the ACS TYPE/TYPEHUGQ 2 concept: every institution, ICE detention included).
Years in US = survey year - YRIMMIG.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/crime_selection_cohorts_2026_09_23/analyze_acs.py
Out: _cache/acs_mex_cells.parquet, derived/acs_cohort_rates.csv, acs_cohort_pooled.csv,
     acs_ysm_profile.csv, acs_cohort_education.csv, acs_api_crosscheck.csv, acs_allocation.csv,
     acs_se_calibration.csv, acs_cohort_pooled_by_citizenship.csv
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cohort_lib import BINS, R, educ3, standardized, summarize, wcols  # noqa: E402

CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
YEARS = [y for y in range(2006, 2025) if y != 2020]
PERIODS = {"2006-2010": range(2006, 2011), "2011-2015": range(2011, 2016),
           "2016-2019": range(2016, 2020), "2021-2024": range(2021, 2025)}
REFS = ("us_all", "us_nhw", "us_mexorig")


def load_mex() -> pd.DataFrame:
    rep = [f"REPWTP{k}" for k in range(1, R + 1)]
    cols = ["YEAR", "SERIAL", "PERWT", "GQ", "AGE", "SEX", "BPL", "CITIZEN", "YRIMMIG", "EDUC"] + rep
    df = pd.read_csv(CACHE / "ipums" / "acs_mex.csv.gz", usecols=cols)
    if not (df.SEX.eq(1).all() and df.AGE.between(18, 40).all() and df.BPL.eq(200).all()):
        raise SystemExit("[FAILED] acs_mex case selection did not hold")
    df = df[df.CITIZEN != 1].copy()
    df["ysm1"] = (df.YEAR - df.YRIMMIG).where(df.YRIMMIG > 0)
    df["ysm1"] = df["ysm1"].clip(upper=16)
    df["educ3"] = educ3(df.EDUC)
    df["cit"] = np.where(df.CITIZEN == 2, "nat", "non")  # naturalized cannot be in ICE custody
    df["inst"] = (df.GQ == 3).astype(float)
    return df


def mex_cells(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["YEAR", "ysm1", "cit", "AGE", "educ3"]
    w = np.column_stack([df.PERWT.to_numpy()] + [df[f"REPWTP{k}"].to_numpy() for k in range(1, R + 1)])
    frame = pd.DataFrame(w, columns=wcols("w"))
    frame[wcols("i")] = w * df["inst"].to_numpy()[:, None]
    frame[keys] = df[keys].to_numpy()
    frame["n"] = 1
    frame["n_inst"] = df["inst"].to_numpy()
    c = frame.groupby(keys, dropna=False).sum().reset_index()
    c["ysm1"] = c["ysm1"].astype(float)
    c["AGE"] = c["AGE"].astype(int)
    c["YEAR"] = c["YEAR"].astype(int)
    return c


def reference() -> pd.DataFrame:
    ref = pd.read_csv(CACHE / "acs_reference.csv")
    ref["group"] = ref["group"].map({"all": "us_all", "nhw": "us_nhw", "mex": "us_mexorig"})
    ref = ref.rename(columns={"year": "YEAR", "age": "AGE"})
    # fixed reference: every replicate equals the full-sample value
    reps = {**{f"w{k}": ref["pop"] for k in range(R + 1)}, **{f"i{k}": ref["inst"] for k in range(R + 1)}}
    return pd.concat([ref, pd.DataFrame(reps)], axis=1)


def bin_of(ysm1: pd.Series) -> pd.Series:
    out = pd.Series("16+", index=ysm1.index, dtype=object)
    for label, lo, hi in BINS:
        out[(ysm1 >= lo) & (ysm1 <= hi)] = label
    out[ysm1.isna()] = "unknown"
    return out


def cohort_rows(c: pd.DataFrame, ref: pd.DataFrame, periods: dict) -> list[dict]:
    out = []
    c = c.assign(bin=bin_of(c.ysm1))
    for pname, years in periods.items():
        cp = c[c.YEAR.isin(list(years))]
        for b in ("0-5", "3-5", "6-10", "11-15", "16+", "all"):
            # 3-5 drops the arrival year and the next two, where immigration custody dominates
            t = cp if b == "all" else cp[cp.ysm1.between(3, 5)] if b == "3-5" else cp[cp["bin"] == b]
            if t.empty:
                continue
            w = t[wcols("w")].to_numpy().sum(0)
            i = t[wcols("i")].to_numpy().sum(0)
            rate, rate_se = summarize(i / w, "sdr")
            row = dict(period=pname, ysm=b, n=int(t.n.sum()), n_inst=int(t.n_inst.sum()),
                       weighted_per_year=float(w[0] / len(set(t.YEAR))), rate=rate, rate_se=rate_se)
            for rname in REFS:
                # expected counts summed year by year, each year against its own reference
                obs = np.zeros(R + 1)
                exp = np.zeros(R + 1)
                for y in sorted(set(t.YEAR)):
                    ty = t[t.YEAR == y]
                    ry = ref[(ref.YEAR == y) & (ref.group == rname)]
                    s = standardized(ty, ry, ["AGE"])
                    wy = ty[wcols("w")].to_numpy().sum(0)
                    obs += s["observed"] * wy
                    exp += s["expected"] * wy
                ratio, ratio_se = summarize(obs / exp, "sdr")
                rr = ref[ref.YEAR.isin(list(years)) & (ref.group == rname)]
                row.update({f"{rname}_rate": float(rr.inst.sum() / rr["pop"].sum()),
                            f"{rname}_expected": float(exp[0] / w[0]),
                            f"ratio_age_{rname}": ratio, f"ratio_age_{rname}_se": ratio_se})
            out.append(row)
    return out


def education_rows(c: pd.DataFrame, ref: pd.DataFrame) -> list[dict]:
    out = []
    c = c.assign(bin=bin_of(c.ysm1))
    upper = {"0-5": 5, "6-10": 10, "11-15": 15}
    for pname, years in PERIODS.items():
        for b, hi in upper.items():
            t = c[c.YEAR.isin(list(years)) & (c["bin"] == b) & (c.AGE >= 18 + hi)]
            for edu in ("all", "lt12", "g12", "col", "g12+"):
                te = t if edu == "all" else t[t.educ3.isin(["g12", "col"])] if edu == "g12+" else t[t.educ3 == edu]
                if te.n.sum() == 0:
                    continue
                w = te[wcols("w")].to_numpy().sum(0)
                i = te[wcols("i")].to_numpy().sum(0)
                rate, rate_se = summarize(i / w, "sdr")
                row = dict(period=pname, ysm=b, adult_arrival_ages=f"{18 + hi}-40", educ=edu,
                           n=int(te.n.sum()), n_inst=int(te.n_inst.sum()), rate=rate, rate_se=rate_se)
                for rname in REFS:
                    for strata, tag in ((["AGE"], "age"), (["AGE", "educ3"], "age_educ")):
                        obs = np.zeros(R + 1)
                        exp = np.zeros(R + 1)
                        for y in sorted(set(te.YEAR)):
                            ty = te[te.YEAR == y]
                            ry = ref[(ref.YEAR == y) & (ref.group == rname)]
                            s = standardized(ty, ry, strata)
                            wy = ty[wcols("w")].to_numpy().sum(0)
                            obs += s["observed"] * wy
                            exp += s["expected"] * wy
                        row[f"ratio_{tag}_{rname}"], row[f"ratio_{tag}_{rname}_se"] = summarize(obs / exp, "sdr")
                out.append(row)
    return out


def ysm_profile(c: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pname, years in PERIODS.items():
        cp = c[c.YEAR.isin(list(years))]
        for ysm, t in cp.groupby("ysm1"):
            w = t[wcols("w")].to_numpy().sum(0)
            i = t[wcols("i")].to_numpy().sum(0)
            rate, se = summarize(i / w, "sdr")
            mean_age = float((t.AGE * t.w0).sum() / t.w0.sum())
            rows.append(dict(period=pname, ysm=int(ysm), n=int(t.n.sum()), n_inst=int(t.n_inst.sum()),
                             mean_age=mean_age, rate=rate, rate_se=se))
    return pd.DataFrame(rows)


def crosscheck(c: pd.DataFrame) -> pd.DataFrame:
    """Same people, two processing chains: IPUMS microdata vs Census API tabulate (main weight)."""
    rows = []
    c = c.assign(bin=bin_of(c.ysm1))
    for y in YEARS:
        for label, _, _ in BINS:
            t = c[(c.YEAR == y) & (c["bin"] == label)]
            api = json.loads((CACHE / "api" / f"tab_mex_ysm{label}_{y}.json").read_text())
            col = {list(h.values())[0]: i for i, h in enumerate(api[0]) if isinstance(h, dict)}
            body = [r for r in api[1:] if r[-1] in ("4", "5")]
            api_pop = sum(sum(r[i] for i in col.values()) for r in body)
            api_inst = sum(r[col["2"]] for r in body)
            rows.append(dict(year=y, ysm=label, ipums_weighted=float(t.w0.sum()), api_weighted=api_pop,
                             ipums_inst=float(t.i0.sum()), api_inst=api_inst))
    return pd.DataFrame(rows)


def _tab(name: str, nflags: int) -> list[tuple]:
    """Census API tabulate response -> [(flag values..., population, institutional)]."""
    api = json.loads((CACHE / "api" / name).read_text())
    col = {list(h.values())[0]: i for i, h in enumerate(api[0]) if isinstance(h, dict)}
    return [(*r[-nflags:], sum(r[i] for i in col.values()), r[col["2"]]) for r in api[1:]]


def allocation() -> pd.DataFrame:
    """Census API tabulations by allocation flag (main weight, crude rates, men 18-40): share of
    Mexico-born institutional records whose year of entry or birthplace was imputed, the rate among
    records with both reported, and a symmetric check that drops birthplace-imputed records on both
    the Mexico-born and the US-born side (crude ratios, not age-standardized)."""
    rows = []
    for y in YEARS:
        us = _tab(f"tab_us_alloc_{y}.json", 1)
        us_all = sum(b[2] for b in us) / sum(b[1] for b in us)
        us_rep = [b for b in us if b[0] == "0"]
        us_pobp_rep = sum(b[2] for b in us_rep) / sum(b[1] for b in us_rep)
        us_inst = sum(b[2] for b in us)
        for label, _, _ in BINS:
            body = _tab(f"tab_mex_alloc_ysm{label}_{y}.json", 2)
            pop = sum(b[2] for b in body)
            inst = sum(b[3] for b in body)
            rep = [b for b in body if b[0] == "0" and b[1] == "0"]
            pobp_rep = [b for b in body if b[1] == "0"]
            rate_pobp_rep = sum(b[3] for b in pobp_rep) / sum(b[2] for b in pobp_rep)
            rows.append(dict(year=y, ysm=label, rate_all=inst / pop,
                             inst_share_yoep_imputed=sum(b[3] for b in body if b[0] == "1") / inst if inst else np.nan,
                             inst_share_pobp_imputed=sum(b[3] for b in body if b[1] == "1") / inst if inst else np.nan,
                             pop_share_yoep_imputed=sum(b[2] for b in body if b[0] == "1") / pop,
                             rate_reported_only=sum(b[3] for b in rep) / sum(b[2] for b in rep),
                             rate_pobp_reported=rate_pobp_rep,
                             us_rate_all=us_all, us_rate_pobp_reported=us_pobp_rep,
                             us_inst_share_pobp_imputed=sum(b[2] for b in us if b[0] == "1") / us_inst,
                             crude_ratio_all=(inst / pop) / us_all,
                             crude_ratio_pobp_reported_both=rate_pobp_rep / us_pobp_rep))
    return pd.DataFrame(rows)


def jk_calibration(df: pd.DataFrame, c: pd.DataFrame) -> pd.DataFrame:
    """Same rate, two SEs: Census replicate weights (SDR) vs the household-group jackknife that
    analyze_movers.py must use (SERIAL mod 80). Pooled periods x years-in-US bins."""
    from analyze_census import cells as jk_cells
    d = df.assign(jk=df.SERIAL % R, corr=0.0, bin=bin_of(df.ysm1))
    j = jk_cells(d, ["YEAR", "bin"])
    c = c.assign(bin=bin_of(c.ysm1))
    rows = []
    for pname, years in PERIODS.items():
        for b in ("0-5", "6-10", "11-15", "all"):
            sel_c = c[c.YEAR.isin(list(years)) & ((c["bin"] == b) if b != "all" else True)]
            sel_j = j[j.YEAR.isin(list(years)) & ((j["bin"] == b) if b != "all" else True)]
            r_sdr = sel_c[wcols("i")].to_numpy().sum(0) / sel_c[wcols("w")].to_numpy().sum(0)
            r_jk = sel_j[wcols("i")].to_numpy().sum(0) / sel_j[wcols("w")].to_numpy().sum(0)
            est, se_sdr = summarize(r_sdr, "sdr")
            _, se_jk = summarize(r_jk, "jk")
            rows.append(dict(period=pname, ysm=b, rate=est, se_sdr=se_sdr, se_jk=se_jk, jk_over_sdr=se_jk / se_sdr))
    return pd.DataFrame(rows)


def main() -> None:
    DERIVED.mkdir(exist_ok=True)
    allocation().to_csv(DERIVED / "acs_allocation.csv", index=False, float_format="%.6g")
    df = load_mex()
    c = mex_cells(df)
    jk_calibration(df, c).to_csv(DERIVED / "acs_se_calibration.csv", index=False, float_format="%.6g")
    c.to_parquet(CACHE / "acs_mex_cells.parquet")
    ref = reference()
    yearly = {str(y): [y] for y in YEARS}
    pd.DataFrame(cohort_rows(c, ref, yearly)).rename(columns={"period": "year"}).to_csv(
        DERIVED / "acs_cohort_rates.csv", index=False, float_format="%.6g")
    pd.DataFrame(cohort_rows(c, ref, PERIODS)).to_csv(DERIVED / "acs_cohort_pooled.csv", index=False,
                                                      float_format="%.6g")
    by_cit = [dict(citizenship=cit, **row) for cit in ("nat", "non")
              for row in cohort_rows(c[c.cit == cit], ref, PERIODS)]
    pd.DataFrame(by_cit).to_csv(DERIVED / "acs_cohort_pooled_by_citizenship.csv", index=False, float_format="%.6g")
    ysm_profile(c).to_csv(DERIVED / "acs_ysm_profile.csv", index=False, float_format="%.6g")
    pd.DataFrame(education_rows(c, ref)).to_csv(DERIVED / "acs_cohort_education.csv", index=False,
                                                float_format="%.6g")
    x = crosscheck(c)
    x.to_csv(DERIVED / "acs_api_crosscheck.csv", index=False, float_format="%.6g")
    worst = float(((x.ipums_weighted - x.api_weighted).abs() / x.api_weighted).max())
    print(f"  IPUMS vs API weighted totals, worst relative gap: {worst:.2e}")
    print("  ✓ derived/acs_cohort_rates.csv, acs_cohort_pooled.csv, acs_ysm_profile.csv, "
          "acs_cohort_education.csv, acs_api_crosscheck.csv")


if __name__ == "__main__":
    main()

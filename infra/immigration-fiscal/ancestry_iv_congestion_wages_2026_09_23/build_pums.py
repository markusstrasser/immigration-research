"""Metro wage, employment and commute panel from IPUMS USA microdata (Census 2000 5%, ACS 2010,
ACS 2009-2011 3-year), on fixed February-2013 CBSAs.

Geography: STATEFIP + PUMA (2000 vintage in all three samples) -> county by the Geocorr 2000
allocation factor the displacement lane uses (its _cache/xwalk_puma2k.csv), then county -> the
2013 OMB delineation, metropolitan areas only. Sums are allocated, means are ratios of allocated sums.

Definitions (persons in households; group quarters GQ 3-4 dropped)
  foreign-born   BPL >= 150 and CITIZEN != 1 (born abroad of American parents are native, as in
                 Census tables); Mexico-born BPL == 200
  education      EDUCD: <62 less than high school; 62-64 high school or GED; 65-100 some college or
                 associate; 101 bachelor's; 110+ graduate. "no BA" = the first three.
  employed       EMPSTAT == 1 (survey week); hours supplied = UHRSWORK x weeks (WKSWORK2 midpoint)
  wage sample    natives 25-64, wage and salary workers (CLASSWKR 2), INCWAGE > 0, not enrolled
                 (SCHOOL 1). Full-time full-year: WKSWORK2 == 6 (50-52 weeks) and UHRSWORK >= 35;
                 weekly wage INCWAGE/51. Hourly (all wage workers): INCWAGE/(weeks midpoint x UHRSWORK).
                 Real hourly wage kept inside [2, 200] 1999 dollars (CPI-U deflators below).
  composition    within each sample, the natives' national mean log wage in each cell of 5-year
                 age (8) x sex (2) x education (5) is removed; a metro's adjusted wage is its mean
                 residual. The 2010-2000 change is therefore the change relative to the nation,
                 holding the metro's age-sex-education mix fixed.
  commute        TRANTIME minutes, workers who did not work at home (TRANWORK 10-70; 80 is worked
                 at home); car = 10-15; public transport 31-37 and 39 (taxicab 38 excluded, as in ACS)

Writes derived/pums_metro.csv (one row per CBSA x sample) and derived/pums_checks.json.
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DT = HERE.parent / "displacement_transfers_2026_09_18"
DERIVED = HERE / "derived"
# CPI-U annual averages (BLS CUUR0000SA0): 1989 124.0, 1999 166.6, 2010 218.056, 2011 224.939
DEFLATE = {1990: 166.6 / 124.0, 2000: 1.0, 2010: 166.6 / 218.056, 2011: 166.6 / 224.939}
WEEKS_MID = {1: 7.0, 2: 20.0, 3: 33.0, 4: 43.5, 5: 48.5, 6: 51.0}
USECOLS = ["YEAR", "SAMPLE", "PERWT", "STATEFIP", "PUMA", "GQ", "AGE", "SEX", "BPL", "CITIZEN",
           "HISPAN", "EDUCD", "EMPSTAT", "CLASSWKR", "WKSWORK2", "UHRSWORK", "INCWAGE", "TRANTIME",
           "TRANWORK", "SCHOOL"]


def educ5(educd):
    e = np.full(len(educd), -1, dtype=np.int8)
    e[(educd >= 2) & (educd < 62)] = 0
    e[(educd >= 62) & (educd <= 64)] = 1
    e[(educd >= 65) & (educd <= 100)] = 2
    e[educd == 101] = 3
    e[educd >= 110] = 4
    return e


def prepare(d: pd.DataFrame) -> pd.DataFrame:
    d = d[~d.GQ.isin([3, 4])].copy()
    d["fb"] = ((d.BPL >= 150) & (d.CITIZEN != 1)).astype(np.int8)
    d["mex"] = (d.BPL == 200).astype(np.int8)
    d["edu"] = educ5(d.EDUCD.to_numpy())
    d["emp"] = (d.EMPSTAT == 1).astype(np.int8)
    wk = d.WKSWORK2.map(WEEKS_MID).fillna(0.0)
    d["hours"] = np.where(d.UHRSWORK > 0, d.UHRSWORK * wk, 0.0)
    year = d.YEAR.iloc[0]  # multi-year samples carry their last year, and dollars of that year
    real = d.INCWAGE.where(d.INCWAGE < 999998, np.nan) * DEFLATE[int(year)]
    hourly = real / (wk * d.UHRSWORK).replace(0, np.nan)
    ok = ((d.fb == 0) & d.AGE.between(25, 64) & (d.CLASSWKR == 2) & (d.SCHOOL == 1)
          & (real > 0) & (d.edu >= 0) & hourly.between(2, 200))
    d["wage_ok"] = ok.astype(np.int8)
    d["ftfy"] = (ok & (d.WKSWORK2 == 6) & (d.UHRSWORK >= 35)).astype(np.int8)
    d["lnweek"] = np.where(d.ftfy == 1, np.log(real / 51.0), np.nan)
    d["lnhour"] = np.where(ok, np.log(hourly), np.nan)
    d["age5"] = ((d.AGE.clip(25, 64) - 25) // 5).astype(np.int8)
    d["commuter"] = ((d.TRANWORK >= 10) & (d.TRANWORK <= 70) & (d.TRANTIME > 0)).astype(np.int8)
    d["car"] = (d.commuter.astype(bool) & d.TRANWORK.between(10, 15)).astype(np.int8)
    return d


def residualize(d: pd.DataFrame, col: str, flag: str) -> pd.Series:
    """Natives' log wage minus the national mean of its age5 x sex x edu cell, within the sample."""
    s = d[d[flag] == 1]
    w = s.PERWT
    key = [s.age5, s.SEX, s.edu]
    num = (s[col] * w).groupby(key).transform("sum")
    den = w.groupby(key).transform("sum")
    r = pd.Series(np.nan, index=d.index)
    r.loc[s.index] = s[col] - num / den
    return r


def puma_sums(d: pd.DataFrame, key: np.ndarray | None = None) -> pd.DataFrame:
    """Weighted sums per state x PUMA (or per any integer key, e.g. 1990 county), one column at
    a time (np.bincount), so a 9m-row sample never materialises a 60-column float frame."""
    w = d.PERWT.to_numpy(dtype=float)
    nat, fb, mex = (d.fb == 0).to_numpy(), (d.fb == 1).to_numpy(), (d.mex == 1).to_numpy()
    emp = (d.emp == 1).to_numpy()
    age = d.AGE.between(25, 64).to_numpy()
    edu = d.edu.to_numpy()
    noba, ba, hsl = (edu >= 0) & (edu <= 2), edu >= 3, (edu >= 0) & (edu <= 1)
    col_up = edu >= 2
    hours, tt, tw = d.hours.to_numpy(), d.TRANTIME.to_numpy(dtype=float), d.TRANWORK.to_numpy()
    commuter, car = d.commuter.to_numpy() == 1, d.car.to_numpy() == 1
    transit = (tw >= 31) & (tw <= 39) & (tw != 38)
    cols = {
        "pop": lambda: w,
        "pop_fb": lambda: w * fb,
        "emp": lambda: w * emp,
        "emp_fb": lambda: w * (emp & fb),
        "emp_mex": lambda: w * (emp & mex),
        "emp2564_noba": lambda: w * (emp & age & noba),
        "emp2564_ba": lambda: w * (emp & age & ba),
        "emp2564_hsl": lambda: w * (emp & age & hsl),
        "emp2564_somecol_up": lambda: w * (emp & age & col_up),
        "emp2564_noba_fb": lambda: w * (emp & age & noba & fb),
        "emp2564_ba_fb": lambda: w * (emp & age & ba & fb),
        "emp2564_noba_mex": lambda: w * (emp & age & noba & mex),
        "emp2564_hsl_fb": lambda: w * (emp & age & hsl & fb),
        "emp2564_nat": lambda: w * (emp & age & nat),
        "hrs2564_noba": lambda: w * (age & noba) * hours,
        "hrs2564_ba": lambda: w * (age & ba) * hours,
        "hrs2564_hsl": lambda: w * (age & hsl) * hours,
        "hrs2564_somecol_up": lambda: w * (age & col_up) * hours,
        "hrs_all": lambda: w * hours,
        "hrs_fb": lambda: w * fb * hours,
        "commuters": lambda: w * commuter,
        "commute_min": lambda: w * commuter * tt,
        "commuters_nat": lambda: w * (commuter & nat),
        "commute_min_nat": lambda: w * (commuter & nat) * tt,
        "car_nat": lambda: w * (car & nat),
        "car_min_nat": lambda: w * (car & nat) * tt,
        "car_all": lambda: w * car,
        "car_min_all": lambda: w * car * tt,
        "workers_nat": lambda: w * (nat & (tw > 0)),
        "home_nat": lambda: w * (nat & (tw == 80)),
        "transit_nat": lambda: w * (nat & transit),
        "workers": lambda: w * (tw > 0),
        "home": lambda: w * (tw == 80),
        "transit": lambda: w * transit,
    }
    for grp, mask in (("noba", noba), ("ba", ba), ("hsl", hsl), ("somecol", edu == 2)):
        for kind in ("week", "hour"):
            flag = (d.ftfy if kind == "week" else d.wage_ok).to_numpy() == 1
            m = flag & mask
            res = np.nan_to_num(d[f"res_{kind}"].to_numpy(dtype=float))
            raw = np.nan_to_num(d[f"ln{kind}"].to_numpy(dtype=float))
            cols[f"n_{kind}_{grp}"] = (lambda m=m: w * m)
            cols[f"r_{kind}_{grp}"] = (lambda m=m, res=res: np.where(m, w * res, 0.0))
            cols[f"raw_{kind}_{grp}"] = (lambda m=m, raw=raw: np.where(m, w * raw, 0.0))
            cols[f"obs_{kind}_{grp}"] = (lambda m=m: m.astype(float))
    if key is None:
        key = d.STATEFIP.to_numpy(dtype=np.int64) * 100000 + d.PUMA.to_numpy(dtype=np.int64)
    uniq, inv = np.unique(key, return_inverse=True)
    out = {"STATEFIP": uniq // 100000, "PUMA": uniq % 100000, "key": uniq}
    for name, fn in cols.items():
        out[name] = np.bincount(inv, weights=fn(), minlength=len(uniq))
    return pd.DataFrame(out)


def load_geo():
    xw = pd.read_csv(DT / "_cache" / "xwalk_puma2k.csv", dtype=str)
    xw["state"] = xw.state.astype(int)
    xw["puma"] = xw.puma2k.astype(int)
    xw["cofips"] = xw.county.str.zfill(5)
    xw["afact"] = pd.to_numeric(xw.afact, errors="coerce")
    d = pd.read_excel(DT / "_cache" / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    return xw[["state", "puma", "cofips", "afact"]], d[["cofips", "cbsa"]]


def main():
    src = CACHE / "ipums" / "core.csv.gz"
    if not src.exists():
        sys.exit("[BLOCKED] _cache/ipums/core.csv.gz missing; run ipums_extract.py download core")
    parts, checks = [], {}
    dtypes = {c: "int32" for c in USECOLS if c != "PERWT"}
    dtypes["PERWT"] = "float64"
    reader = pd.read_csv(src, usecols=USECOLS, dtype=dtypes, chunksize=3_000_000)
    for i, chunk in enumerate(reader):
        for samp, d in chunk.groupby("SAMPLE"):
            parts.append((samp, d))
        print(f"  read chunk {i} rows {len(chunk):,}", flush=True)
    by = {}
    for samp, d in parts:
        by.setdefault(samp, []).append(d)
    xw, cb = load_geo()
    out = []
    for samp, ds in sorted(by.items()):
        d = prepare(pd.concat(ds, ignore_index=True))
        d["res_week"] = residualize(d, "lnweek", "ftfy")
        d["res_hour"] = residualize(d, "lnhour", "wage_ok")
        checks[str(samp)] = dict(rows=int(len(d)), pop=float(d.PERWT.sum()),
                                 fb_share=float((d.PERWT * d.fb).sum() / d.PERWT.sum()),
                                 ftfy_native_obs=int(d.ftfy.sum()), wage_native_obs=int(d.wage_ok.sum()),
                                 commuters=float((d.PERWT * d.commuter).sum()))
        p = puma_sums(d)
        m = p.merge(xw, left_on=["STATEFIP", "PUMA"], right_on=["state", "puma"], how="left", indicator=True)
        miss = float((m._merge != "both").mean())
        checks[str(samp)]["puma_merge_miss"] = miss
        m = m[m._merge == "both"]
        num = [c for c in p.columns if c not in ("STATEFIP", "PUMA", "key")]
        m[num] = m[num].mul(m.afact, axis=0)
        if samp == 200001:
            # county sums for the 1990-footprint pre-trend (build_pums_1990.py); intermediate only
            m.groupby("cofips")[num].sum().reset_index().to_csv(CACHE / "pums_county_2000.csv", index=False)
        j = m.merge(cb, on="cofips", how="inner")
        g = j.groupby("cbsa")[num].sum().reset_index()
        g["sample"] = samp
        out.append(g)
        print(f"sample {samp}: rows {len(d):,}, PUMA merge miss {miss:.4f}, CBSAs {len(g)}", flush=True)
    panel = pd.concat(out, ignore_index=True)
    DERIVED.mkdir(exist_ok=True)
    # obs_* are allocation-weighted observation counts: the effective sample behind each metro mean
    panel.to_csv(DERIVED / "pums_metro.csv", index=False)
    (DERIVED / "pums_checks.json").write_text(json.dumps(checks, indent=1))
    print(json.dumps(checks, indent=1))


if __name__ == "__main__":
    main()

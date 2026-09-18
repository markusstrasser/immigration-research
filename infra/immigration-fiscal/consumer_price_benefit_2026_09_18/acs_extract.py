#!/usr/bin/env python3
"""ACS 2024 1-year PUMS extraction for the consumer-price / native-hours lane.

Produces:
  derived/industry_shares.csv   -- employment and Mexico-born shares in the
                                   immigrant-intensive industry groups (national, CA, TX)
  derived/lowskill_share.csv    -- Cortes treatment variable: low-skilled (HS-dropout)
                                   immigrants / civilian labor force, and the Mexico-born part
  derived/women_top_quartile.csv-- native college-educated employed women in the top quartile
                                   of the female hourly-wage distribution: count, hours, wage
  derived/households.csv        -- native-headed household (consumer-unit proxy) counts
  derived/acs_audit.json        -- gates and file hashes

Uses the 80 replicate weights (variance = 4/80 * sum((rep-full)^2)) for the headline
population counts.  Single pass, rows age>=16 retained; float32 for replicate weights.
"""
from __future__ import annotations

import hashlib, json, sys, zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)
DATA = Path("/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr")
ZIP = DATA / "csv_pus.zip"
SRC_URL = "https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip"

REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = ["SERIALNO", "SPORDER", "PWGTP", "STATE", "AGEP", "SEX", "NATIVITY", "POBP",
        "HISP", "RAC1P", "RELSHIPP", "SCHL", "ESR", "INDP", "OCCP", "WAGP", "PERNP",
        "WKHP", "WKWN", "ADJINC", "COW"] + REPS

MEXICO_POBP = 303  # Mexico

# --- Cortes-style immigrant-intensive industry groups (2024 ACS INDP codes) -------------
# Tier 1 = the six services in her reduced-form price regression (Table 3 note):
#   baby-sitting, housekeeping, gardening, dry cleaning, shoe repair, barber shops.
# Tier 2 = other personal/non-traded services that map to CEX lines.
# Tier 3 = food away from home (restaurants) and construction, which Cortes's CPI sample
#   handles differently (construction is explicitly OMITTED from her price analysis).
IND_GROUPS = {
    "t1_private_households":        [9290],
    "t1_bldg_dwelling_services":    [7690],
    "t1_landscaping":               [7770],
    "t1_drycleaning_laundry":       [9070],
    "t1_child_care":                [8470],
    "t1_barber_beauty_nail_other":  [8970, 8980, 8990],
    "t2_household_goods_repair":    [8891],
    "t2_auto_repair_carwash":       [8770, 8780],
    "t3_food_services":             [8680, 8690],
    "t3_construction":              [770],
}
TIER1 = [k for k in IND_GROUPS if k.startswith("t1_")]
TIER2 = [k for k in IND_GROUPS if k.startswith("t2_")]
TIER3 = [k for k in IND_GROUPS if k.startswith("t3_")]

# Occupation cross-check (2018 SOC-based ACS OCCP codes)
OCC_GROUPS = {
    "occ_maids_housekeeping":  [4230],
    "occ_bldg_cleaning_other": [4220, 4240, 4251, 4252, 4255],
    "occ_grounds_maintenance": [4251],
    "occ_childcare_workers":   [4600],
    "occ_cooks_food_prep":     [4020, 4030],
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load() -> pd.DataFrame:
    frames = []
    dtypes = {c: "float32" for c in REPS}
    dtypes.update({"SERIALNO": str, "INDP": "float64", "OCCP": "float64",
                   "SCHL": "float64", "ESR": "float64", "COW": "float64"})
    with zipfile.ZipFile(ZIP) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        if len(members) != 2:
            raise SystemExit(f"[BLOCKED] expected 2 csv members, got {members}")
        for name in members:
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                for chunk in pd.read_csv(fh, usecols=COLS, dtype=dtypes, chunksize=400_000,
                                         low_memory=False):
                    frames.append(chunk[chunk.AGEP >= 16].copy())
    df = pd.concat(frames, ignore_index=True)
    print(f"[loaded] {len(df):,} person records aged 16+", flush=True)
    return df


def sdr(vec: np.ndarray) -> tuple[float, float]:
    vec = np.asarray(vec, dtype=float)
    return float(vec[0]), float(np.sqrt(4.0 / 80.0 * np.square(vec[1:] - vec[0]).sum()))


def main() -> None:
    df = load()
    W = df[["PWGTP"] + REPS].to_numpy(dtype=np.float64)   # (n, 81)
    adj = df["ADJINC"].to_numpy() / 1_000_000.0

    native = df.NATIVITY.to_numpy() == 1
    foreign = ~native
    mexborn = df.POBP.to_numpy() == MEXICO_POBP
    schl = df.SCHL.to_numpy()
    dropout = schl <= 15                      # less than a high-school diploma
    nocollege = schl <= 19                    # no associate's degree or higher
    college = schl >= 21                      # bachelor's or higher
    esr = df.ESR.to_numpy()
    employed = np.isin(esr, [1, 2])
    clf = np.isin(esr, [1, 2, 3])             # civilian labor force
    state = df.STATE.to_numpy()
    indp = df.INDP.to_numpy()
    occp = df.OCCP.to_numpy()
    female = df.SEX.to_numpy() == 2

    geos = {"US": np.ones(len(df), dtype=bool), "CA": state == 6, "TX": state == 48}

    # ---------- 1. Cortes treatment variable: low-skilled immigrants / labor force ----------
    rows = []
    for gname, gmask in geos.items():
        lf = gmask & clf
        den = W[lf].sum(axis=0)
        defs = {
            "fb_dropout":        gmask & clf & foreign & dropout,
            "fb_nocollege":      gmask & clf & foreign & nocollege,
            "mexborn_dropout":   gmask & clf & foreign & dropout & mexborn,
            "mexborn_nocollege": gmask & clf & foreign & nocollege & mexborn,
            "mexborn_all":       gmask & clf & mexborn,
        }
        for dname, dmask in defs.items():
            num = W[dmask].sum(axis=0)
            share = num / den
            pt, se = sdr(share)
            npt, nse = sdr(num)
            rows.append(dict(geo=gname, numerator=dname, labor_force=den[0],
                             count=npt, count_se=nse, share=pt, share_se=se))
    pd.DataFrame(rows).to_csv(OUT / "lowskill_share.csv", index=False)
    print("[done] lowskill_share.csv", flush=True)

    # ---------- 2. Industry / occupation employment shares ----------
    rows = []
    for gname, gmask in geos.items():
        base_emp = gmask & employed
        tot_emp = W[base_emp].sum(axis=0)[0]
        sets = {k: np.isin(indp, v) for k, v in IND_GROUPS.items()}
        sets.update({k: np.isin(occp, v) for k, v in OCC_GROUPS.items()})
        sets["t1_all"] = np.any([np.isin(indp, IND_GROUPS[k]) for k in TIER1], axis=0)
        sets["t12_all"] = np.any([np.isin(indp, IND_GROUPS[k]) for k in TIER1 + TIER2], axis=0)
        sets["t123_all"] = np.any([np.isin(indp, IND_GROUPS[k]) for k in TIER1 + TIER2 + TIER3], axis=0)
        for sname, smask in sets.items():
            m = base_emp & smask
            emp = W[m].sum(axis=0)
            mex = W[m & mexborn].sum(axis=0)
            mexd = W[m & mexborn & dropout].sum(axis=0)
            mexn = W[m & mexborn & nocollege].sum(axis=0)
            fbd = W[m & foreign & dropout].sum(axis=0)
            fbn = W[m & foreign & nocollege].sum(axis=0)
            if emp[0] <= 0:
                continue
            e_pt, e_se = sdr(emp)
            rows.append(dict(
                geo=gname, group=sname, employment=e_pt, employment_se=e_se,
                share_of_total_employment=e_pt / tot_emp,
                mexborn=mex[0], mexborn_share=mex[0] / e_pt,
                mexborn_dropout=mexd[0], mexborn_dropout_share=mexd[0] / e_pt,
                mexborn_nocollege=mexn[0], mexborn_nocollege_share=mexn[0] / e_pt,
                fb_dropout=fbd[0], fb_dropout_share=fbd[0] / e_pt,
                fb_nocollege=fbn[0], fb_nocollege_share=fbn[0] / e_pt,
            ))
    pd.DataFrame(rows).to_csv(OUT / "industry_shares.csv", index=False)
    print("[done] industry_shares.csv", flush=True)

    # ---------- 3. Native college-educated employed women, top wage quartile ----------
    wagp = df["WAGP"].fillna(0).to_numpy() * adj
    pernp = df["PERNP"].fillna(0).to_numpy() * adj
    wkhp = df["WKHP"].to_numpy()
    wkwn = df["WKWN"].to_numpy()
    hours_yr = wkhp * wkwn
    with np.errstate(invalid="ignore", divide="ignore"):
        hwage = np.where(hours_yr > 0, pernp / hours_yr, np.nan)

    # top quartile of the hourly wage distribution among ALL employed women with
    # positive hours and positive earnings (Cortes-Tessada's reference distribution)
    base_w = employed & female & (hours_yr > 0) & (pernp > 0) & np.isfinite(hwage)
    ww = W[base_w, 0]
    hw = hwage[base_w]
    order = np.argsort(hw)
    cw = np.cumsum(ww[order]) / ww.sum()
    p75 = float(hw[order][np.searchsorted(cw, 0.75)])
    p25 = float(hw[order][np.searchsorted(cw, 0.25)])
    p50 = float(hw[order][np.searchsorted(cw, 0.50)])
    print(f"[quantiles] female employed hourly wage p25={p25:.2f} p50={p50:.2f} p75={p75:.2f}", flush=True)

    rows = []
    defs = {
        "all_employed_women":               base_w,
        "topq_all_women":                   base_w & (hwage >= p75),
        "topq_native_women":                base_w & (hwage >= p75) & native,
        "topq_native_college_women":        base_w & (hwage >= p75) & native & college,
        "native_college_employed_women":    base_w & native & college,
    }
    for dname, dmask in defs.items():
        n = W[dmask].sum(axis=0)
        n_pt, n_se = sdr(n)
        wsum = (W[dmask, 0]).sum()
        mean_hours_wk = float((W[dmask, 0] * wkhp[dmask]).sum() / wsum)
        mean_weeks = float((W[dmask, 0] * wkwn[dmask]).sum() / wsum)
        mean_hours_yr = float((W[dmask, 0] * hours_yr[dmask]).sum() / wsum)
        mean_earn = float((W[dmask, 0] * pernp[dmask]).sum() / wsum)
        mean_wage = float((W[dmask, 0] * pernp[dmask]).sum() / (W[dmask, 0] * hours_yr[dmask]).sum())
        rows.append(dict(group=dname, count=n_pt, count_se=n_se,
                         mean_usual_hours_week=mean_hours_wk, mean_weeks=mean_weeks,
                         mean_annual_hours=mean_hours_yr, mean_annual_earnings=mean_earn,
                         aggregate_hourly_wage=mean_wage,
                         total_annual_hours_bn=float((W[dmask, 0] * hours_yr[dmask]).sum() / 1e9),
                         total_earnings_bn=float((W[dmask, 0] * pernp[dmask]).sum() / 1e9)))
    out = pd.DataFrame(rows)
    out["female_wage_p25"] = p25
    out["female_wage_p50"] = p50
    out["female_wage_p75"] = p75
    out.to_csv(OUT / "women_top_quartile.csv", index=False)
    print("[done] women_top_quartile.csv", flush=True)

    # ---------- 4. Household counts (consumer-unit proxy) ----------
    # Householder = RELSHIPP 20; housing units only (SERIALNO chars 4:6 == 'HU').
    hu = df.SERIALNO.str.slice(4, 6).to_numpy() == "HU"
    head = (df.RELSHIPP.to_numpy() == 20) & hu
    rows = []
    for dname, dmask in {"all_households": head,
                         "native_head_households": head & native,
                         "mexborn_head_households": head & mexborn}.items():
        n = W[dmask].sum(axis=0)
        pt, se = sdr(n)
        rows.append(dict(group=dname, households=pt, households_se=se))
    pd.DataFrame(rows).to_csv(OUT / "households.csv", index=False)
    print("[done] households.csv", flush=True)

    # ---------- audit ----------
    tot_pop16 = float(W[:, 0].sum())
    audit = dict(
        source_url=SRC_URL, zip_path=str(ZIP), zip_sha256=sha256(ZIP),
        n_records_age16plus=int(len(df)), weighted_pop_16plus=tot_pop16,
        female_wage_p25=p25, female_wage_p50=p50, female_wage_p75=p75,
        adjinc_unique=[float(x) for x in np.unique(adj)],
        civilian_lf_us=float(W[clf, 0].sum()),
        employed_us=float(W[employed, 0].sum()),
        mexborn_16plus=float(W[mexborn, 0].sum()),
    )
    (OUT / "acs_audit.json").write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2)[:900], flush=True)


if __name__ == "__main__":
    main()

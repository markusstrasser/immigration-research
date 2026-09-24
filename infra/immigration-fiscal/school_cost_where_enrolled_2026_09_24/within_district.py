"""Within-district allocation: do the group's pupils attend the higher-spending schools of their district?

NCES School-Level Finance Survey FY2022 (school year 2021-22, provisional 1a): school current
expenditure for elementary-secondary education (TCURELSCS, all funds; TCURELSCSE, excluding federal
funds) and membership (MEMBER). "Districtwide" records (8th character of NCESSCH = "D") hold spending
not reported down to schools; it is spread equally over the district's pupils, so it moves nothing.
School Hispanic membership comes from the CCD 2021-22 school file (ccd.school_2122). The Mexican share
of Hispanics is taken as uniform across a district's schools (no school-level origin data exist).

For each district: f_l = Hispanic-weighted school spending per pupil / all-pupil school spending per
pupil. The national factor weights f_l by the group's pupils in the district (weighting.py, 2023-24);
districts without usable school data get f_l = 1. Writes derived/within_district.json and
derived/within_district_by_state.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/within_district.py
"""
import json
import sys
import zipfile

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ccd  # noqa: E402
from weighting import NYC_F33, build  # noqa: E402

SLFS = HERE / "_cache/slfs22_data_2025047_4_0_1.zip"
PPS_BAND = (2_000.0, 100_000.0)     # school spending per pupil kept; outside is a reporting artefact
MIN_SCHOOLS = 2                     # a district with one school has no within-district allocation


def read_slfs():
    with zipfile.ZipFile(SLFS) as z:
        s = pd.read_csv(z.open("slfs22_1a.txt"), sep="\t", encoding="latin-1",
                        dtype={"NCESSCH": str, "LEAID": str, "FIPST": str, "CCDNF": str, "SCH_TYPE": str},
                        usecols=["NCESSCH", "LEAID", "FIPST", "SCH_TYPE", "CCDNF", "MEMBER", "TCURELSCS", "TCURELSCSE"])
    for c in ["MEMBER", "TCURELSCS", "TCURELSCSE"]:
        s[c] = pd.to_numeric(s[c], errors="coerce")
    s["districtwide"] = s.NCESSCH.str[7].eq("D")
    return s


def factor(s, spend):
    """Per-district within-district factor for the spending column `spend`."""
    resid = s[s.districtwide].groupby("LEAID")[spend].sum()
    sch = s[~s.districtwide & s.MEMBER.gt(0) & s[spend].gt(0)].copy()
    sch["pps"] = sch[spend] / sch.MEMBER
    sch = sch[sch.pps.between(*PPS_BAND)]
    members = sch.groupby("LEAID").MEMBER.sum()
    sch["pps"] += sch.LEAID.map(resid).fillna(0) / sch.LEAID.map(members)
    g = sch.groupby("LEAID")
    out = pd.DataFrame({
        "schools": g.size(), "members": members,
        "hisp": g.tot_hisp.sum(), "all_ccd": g.tot_all.sum(),
        "pp_all": g.apply(lambda b: np.average(b.pps, weights=b.tot_all) if b.tot_all.sum() > 0 else np.nan),
        "pp_hisp": g.apply(lambda b: np.average(b.pps, weights=b.tot_hisp) if b.tot_hisp.sum() > 0 else np.nan),
    })
    out = out[out.schools.ge(MIN_SCHOOLS) & out.hisp.gt(0)]
    out["f"] = out.pp_hisp / out.pp_all
    return out


def main():
    s = read_slfs()
    counts = ccd.school_2122()
    for c in ["tot_all", "tot_hisp"]:
        counts[c] = pd.to_numeric(counts[c])
    s = s.merge(counts[["NCESSCH", "tot_all", "tot_hisp"]], on="NCESSCH", how="left")
    s[["tot_all", "tot_hisp"]] = s[["tot_all", "tot_hisp"]].fillna(0)
    d, _ = build()
    grp = d.groupby("LEAID").w_mex_dist.sum()
    # CCD 2021-22 also splits NYC into geographic districts; SLFS reports schools under those LEAs too,
    # so NYC's within-district factor is computed across the city by mapping them to the F-33 unit.
    names = ccd.lea_directory_2324().set_index("LEAID").LEA_NAME
    nyc_leas = set(names.index[names.fillna("").str.startswith("NEW YORK CITY GEOGRAPHIC DISTRICT")])
    s.loc[s.LEAID.isin(nyc_leas), "LEAID"] = NYC_F33
    results, by_state = {}, []
    for spend in ["TCURELSCS", "TCURELSCSE"]:
        f = factor(s, spend)
        w = grp.reindex(f.index).fillna(0)
        covered = float(w.sum() / grp.sum())
        f_cov = float(np.average(f.f, weights=w)) if w.sum() > 0 else np.nan
        results[spend] = dict(
            districts_with_factor=int(len(f)), group_pupil_coverage=covered,
            factor_covered_districts=f_cov, factor_all_districts=1 + (f_cov - 1) * covered,
            schools_used=int(f.schools.sum()),
            hispanic_share_of_ccd_members_matched=float(s.tot_hisp[~s.districtwide].sum() / s.tot_all[~s.districtwide].sum()),
        )
        f["fips"] = f.index.str[:2].astype(int)
        f["group_pupils"] = w
        for fips, b in f.groupby("fips"):
            if b.group_pupils.sum() > 0:
                by_state.append(dict(fips=fips, spend=spend, districts=len(b), group_pupils=b.group_pupils.sum(),
                                     factor=np.average(b.f, weights=b.group_pupils)))
    out = HERE / "derived"
    results["slfs_records"] = int(len(s))
    results["slfs_districtwide_records"] = int(s.districtwide.sum())
    results["ccd_match_share_of_school_records"] = float(s.tot_all[~s.districtwide].gt(0).mean())
    results["note"] = ("School-level current expenditure, FY2022; Hispanic school weights from CCD 2021-22; "
                       "districts weighted by the group's 2023-24 pupils; uncovered districts count as 1.")
    (out / "within_district.json").write_text(json.dumps(results, indent=1) + "\n")
    pd.DataFrame(by_state).to_csv(out / "within_district_by_state.csv", index=False, lineterminator="\n",
                                  float_format="%.6f")
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()

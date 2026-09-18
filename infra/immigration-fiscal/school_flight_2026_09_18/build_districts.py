"""District-year panel: F-33 finance x CCD enrollment-by-race x CCD directory.

Waves 2000, 2005, 2010, 2015, 2020 (Urban's F-33 redistribution stops at 2020).
Money is deflated to 2020 dollars with the FRED CPI-U annual average
(_cache/cpiaucsl_annual.csv, series CPIAUCSL).

Screens, all reported: regular operating districts only (agency_type 1 and 2, i.e.
regular local school districts and supervisory-union components), non-charter,
enrollment >= 100, per-pupil current spending inside [3,000, 80,000] in 2020 dollars
-- the same plausibility band as ledger_absolute_2026_09_17/district_differential.py.
CCD negative values (-1 missing, -2 not applicable, -3 suppressed) are set to missing.
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache" / "dist"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)
PP_MIN, PP_MAX = 3_000.0, 80_000.0


def neg_to_nan(s):
    s = pd.to_numeric(s, errors="coerce")
    return s.where(s >= 0)


def load(kind):
    fs = sorted(CACHE.glob(f"{kind}_*.csv"))
    if not fs:
        raise SystemExit(f"no {kind} files")
    d = pd.concat((pd.read_csv(f, dtype={"leaid": str, "county_code": str, "cbsa": str})
                   for f in fs), ignore_index=True)
    d["leaid"] = d.leaid.str.strip().str.zfill(7)
    return d


def main():
    cpi = pd.read_csv(HERE / "_cache" / "cpiaucsl_annual.csv")
    cpi["year"] = pd.to_datetime(cpi.observation_date).dt.year
    cpi = cpi.set_index("year")["CPIAUCSL"]
    base = cpi.loc[2020]

    fin, enr, dr = load("fin"), load("enr"), load("dir")
    print(f"fin {len(fin):,}  enr {len(enr):,}  dir {len(dr):,}")
    # Keep only waves pulled for every state in all three files: a part-coverage wave
    # would enter the panel with a handful of states and break the state-year effects.
    cov = {k: set(df.groupby("year").fips.nunique().pipe(lambda s: s[s >= 51]).index)
           for k, df in (("fin", fin), ("enr", enr), ("dir", dr))}
    full = sorted(set.intersection(*cov.values()))
    part = sorted(set(fin.year) | set(enr.year) | set(dr.year)) 
    print(f"waves with all 51 states in fin+enr+dir: {full}; "
          f"dropping part-coverage waves: {[y for y in part if y not in full]}")
    fin, enr, dr = (df[df.year.isin(full)] for df in (fin, enr, dr))

    d = (dr.merge(enr, on=["year", "fips", "leaid"], how="inner", suffixes=("", "_e"))
           .merge(fin, on=["year", "fips", "leaid"], how="inner", suffixes=("", "_f")))
    print(f"joined district-years: {len(d):,}")

    for c in ("enr_total", "enr_white", "enr_black", "enr_hisp", "enr_asian",
              "enrollment", "english_language_learners", "enrollment_fall_responsible",
              "rev_total", "rev_local_total", "rev_local_prop_tax", "rev_state_total",
              "rev_fed_total", "exp_current_elsec_total", "exp_current_instruction_total"):
        d[c] = neg_to_nan(d[c])

    d["defl"] = d.year.map(lambda y: base / cpi.loc[y])
    # Per-pupil denominators use the F-33's OWN membership count for the finance year
    # (ENROLL / V33), not the CCD count: Urban's CCD enrolment year is the following
    # autumn, so dividing FY finance by CCD enrolment mixes two school years. CCD counts
    # are used only for the race SHARES, where the one-year offset is immaterial.
    pupils = d.enrollment_fall_responsible.where(d.enrollment_fall_responsible > 0)
    d["pupils"] = pupils
    ccd_pupils = d.enr_total.where(d.enr_total > 0)
    for c, nm in (("exp_current_elsec_total", "pp_current"),
                  ("exp_current_instruction_total", "pp_instruction"),
                  ("rev_local_total", "pp_rev_local"),
                  ("rev_local_prop_tax", "pp_rev_proptax"),
                  ("rev_state_total", "pp_rev_state"),
                  ("rev_fed_total", "pp_rev_fed"),
                  ("rev_total", "pp_rev_total")):
        d[nm] = d[c] * d.defl / pupils

    d["hisp_share"] = d.enr_hisp / ccd_pupils
    d["white_share"] = d.enr_white / ccd_pupils
    d["black_share"] = d.enr_black / ccd_pupils
    d["asian_share"] = d.enr_asian / ccd_pupils
    d["ell_share"] = d.english_language_learners / ccd_pupils
    # Herfindahl-based ethnic fractionalisation over the five reported groups
    other = (ccd_pupils - d[["enr_white", "enr_black", "enr_hisp", "enr_asian"]].sum(axis=1)) \
        .clip(lower=0)
    sh = pd.concat([d.white_share, d.black_share, d.hisp_share, d.asian_share,
                    other / ccd_pupils], axis=1)
    d["elf"] = 1.0 - (sh ** 2).sum(axis=1)

    n0 = len(d)
    keep = (d.agency_type.isin([1, 2])
            & (d.agency_charter_indicator != 1)
            & (d.pupils >= 100)
            & d.pp_current.between(PP_MIN, PP_MAX)
            & d.hisp_share.between(0, 1))
    d = d[keep].copy()
    print(f"screens kept {len(d):,} of {n0:,} district-years")

    cc = pd.read_csv(HERE / "_cache" / "county_controls.csv", dtype={"cofips": str})
    cc["cofips"] = cc.cofips.str.zfill(5)
    d["cofips"] = d.county_code.astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(5)
    d = d.merge(cc[["year", "cofips", "share65", "mhi"]], on=["year", "cofips"], how="left")
    print(f"county elderly share matched for {d.share65.notna().mean():.3f} of rows")

    # crude local tax effort: local revenue per pupil scaled by county median household
    # income, so a district is not counted as trying harder merely because it is richer.
    # 2005 carries the 2000 SF1 elderly share and has no ACS median income, so effort is
    # missing in that wave by construction.
    d["local_effort"] = d.pp_rev_local / d.mhi.where(d.mhi > 0)
    d["proptax_effort"] = d.pp_rev_proptax / d.mhi.where(d.mhi > 0)
    d["state_year"] = d.fips.astype(str) + "_" + d.year.astype(str)
    d = d.sort_values(["leaid", "year"])
    d.to_csv(DERIVED / "district_panel.csv", index=False)
    print(f"wrote district_panel.csv: {len(d):,} rows, {d.leaid.nunique():,} districts, "
          f"years {sorted(d.year.unique())}")
    print(d.groupby("year").apply(
        lambda g: pd.Series({
            "districts": len(g),
            "pupils_m": g.pupils.sum() / 1e6,
            "hisp_share": (g.hisp_share * g.pupils).sum() / g.pupils.sum(),
            "pp_current_2020$": (g.pp_current * g.pupils).sum() / g.pupils.sum(),
            "pp_rev_local_2020$": (g.pp_rev_local * g.pupils).sum() / g.pupils.sum(),
        }), include_groups=False))


if __name__ == "__main__":
    main()
